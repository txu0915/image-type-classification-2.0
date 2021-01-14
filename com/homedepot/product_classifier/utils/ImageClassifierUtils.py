import urllib3
import cv2
import gcsfs
import h5py
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from tensorflow.python.lib.io import file_io

from com.homedepot.product_classifier.constants import Constants
from com.homedepot.product_classifier.utils.OpenCVFeatureUtils import OpenCVFeatureUtils

urllib3.disable_warnings()

class ImageClassifierUtils:
    @staticmethod
    def keras_model_file_reader(model_dir):
        model_file = file_io.FileIO(model_dir, mode='rb')
        h5py_model_file = h5py.File(model_file, 'r')
        model = tf.keras.models.load_model(h5py_model_file, compile=False)
        return model

    @staticmethod
    def xgb_model_file_reader(model_dir):
        model_file = file_io.FileIO(model_dir, mode='rb')
        model = joblib.load(model_file)
        return model

    @staticmethod
    def create_image_url(image_dtls):
        if image_dtls[:6] != "https:":
            image_dtls = "https://idm.homedepot.com/assets/image/" + image_dtls[:2] + "/" + image_dtls + ".jpg"
            return image_dtls
        else:
            return image_dtls

    @staticmethod
    def download_image(url):
        http_response = urllib3.PoolManager().request('GET', url)
        image = np.asarray(bytearray(http_response.data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (Constants.IMAGE_SIZE, Constants.IMAGE_SIZE))
        return image

    @staticmethod
    def expand_features(f1, f2):
        return np.concatenate([f1, f2], axis=1)

    @staticmethod
    def generate_classifier_tree_module(imageClassifierTreeFilePath, mode):
        if (mode == 'dataflow'):
            fs = gcsfs.GCSFileSystem()
            with fs.open(imageClassifierTreeFilePath) as image_classifier_catalog:
                classifier_tree_data_frame = pd.read_json(image_classifier_catalog, lines=True)
                classifier_tree_map = classifier_tree_data_frame.to_dict('records')[0]
        else:
            classifier_tree_data_frame = pd.read_json(imageClassifierTreeFilePath, lines=True)
            classifier_tree_map = classifier_tree_data_frame.to_dict('records')[0]
        return classifier_tree_map;

    @staticmethod
    def generate_classifier_module(image_classifier_info_file_path, mode):
        classifier_modules_map = {}
        if (mode == 'dataflow'):
            fs = gcsfs.GCSFileSystem()
            with fs.open(image_classifier_info_file_path) as image_classifier_catalog:
                image_classifier_data_frame = pd.read_json(image_classifier_catalog, lines=True)
                image_classifier_dict = image_classifier_data_frame.to_dict('records')[0]
        else:
            image_classifier_data_frame = pd.read_json(image_classifier_info_file_path, lines=True)
            image_classifier_dict = image_classifier_data_frame.to_dict('records')[0]

        for classifier_module, classifier_module_dtls in image_classifier_dict.items():
            classifier_modules_map[classifier_module] = ImageClassifierUtils.model_file_loader(classifier_module_dtls)
        print("[Info] Classifier modules assembled successfully...")

        return classifier_modules_map;

    @staticmethod
    def model_file_loader(classifier_module_dtls):
        embedding_extractor_list = classifier_module_dtls["embeddings_extractor"]
        classes = classifier_module_dtls['classes']
        opencv_feature_list = classifier_module_dtls["opencv_feature_list"]
        # print(embedding_extractor_list, len(embedding_extractor_list))
        if embedding_extractor_list:
            classifier = ImageClassifierUtils.xgb_model_file_reader(classifier_module_dtls['classifier'])
            # print("[Info] xgboost classifier loaded...")
            vgg16 = ImageClassifierUtils.keras_model_file_reader(embedding_extractor_list[0])
            print('vgg16', type(vgg16))
            # print("[Info] VGG16 embedding_extractor_list loaded...")
            resnet = ImageClassifierUtils.keras_model_file_reader(embedding_extractor_list[1])
            print('resnet', type(resnet))
            # print("[Info] Resnet embedding_extractor_list loaded...")
            return {"embedding_extractor": [vgg16, resnet], "classifier": classifier, "classes": classes,
                    "opencv_feature_list": opencv_feature_list}
        else:
            classifier = ImageClassifierUtils.keras_model_file_reader(classifier_module_dtls['classifier'])
            print('Keras Model VGG19', type(classifier))

        print("[Info] Neural network model all-in-one loaded...")
        return {"embedding_extractor": [], "classifier": classifier, "classes": classes,
                "opencv_feature_list": opencv_feature_list}

    @staticmethod
    def classify_image_type(img, classifier_module):
        embedding_extractor = classifier_module['embedding_extractor']
        classes = classifier_module['classes']
        classifier = classifier_module['classifier']
        label_encoder = LabelEncoder()
        encoded_labels = label_encoder.fit_transform(np.array(classes))
        if embedding_extractor != []:
            opencv_feature_list = classifier_module["opencv_feature_list"]
            vgg16 = embedding_extractor[0]
            resnet = embedding_extractor[1]
            predicts = vgg16.predict(np.array([img]))
            # print("[Info] VGG16 predict successfully")
            predicts = ImageClassifierUtils.expand_features(predicts, resnet.predict(np.array([img])))
            # print(predicts.shape,"predicts shape")
            # print("[Info] Resnet predict successfully")
            cv_features = OpenCVFeatureUtils(opencv_feature_list, img).compute_feature()
            # print("opencv_features dims:",opencv_features.shape)
            # print("dominant color dims:", np.array([dominant_color(img)]).shape)
            # print(opencv_features.shape,"opencv feature shape")
            predicts = ImageClassifierUtils.expand_features(predicts, cv_features)
            # print(predicts.shape, "updated predicts shape")
            # print(predicts)
            xgb_features = xgb.DMatrix(predicts)
            decoded_labels = label_encoder.inverse_transform(classifier.predict(xgb_features).astype('int'))
            return decoded_labels
        decoded_labels = label_encoder.inverse_transform(classifier.predict(np.array([img])).argmax(axis=1))
        return decoded_labels


    @staticmethod
    def climb_classifier_tree(img, classifier_tree_dict, classifier_modules_dict, report=[]):
        # check exiting condition...
        k = list(classifier_tree_dict.keys())[0]
        classifier_current_level = classifier_modules_dict[k]
        prediction = ImageClassifierUtils.classify_image_type(img, classifier_current_level)[0]
        report.append({k: prediction})
        if classifier_tree_dict[k] == "leaf" or prediction not in classifier_tree_dict[k].keys():
            return report
        sub_tree = classifier_tree_dict[k][prediction]
        ImageClassifierUtils.climb_classifier_tree(img, sub_tree, classifier_modules_dict, report)
        return report
