import datetime
import json
import logging
import threading

import apache_beam as beam
import gcsfs
import pandas as pd

from com.homedepot.product_classifier.constants import Constants
from com.homedepot.product_classifier.utils.ImageClassifierUtils import ImageClassifierUtils
from com.homedepot.product_classifier.utils.GenericUtils import GenericUtils

class ProductImageClassificationDoFn(beam.DoFn):
    class _ModelState(object):
        """Atomic representation of the in-memory state of the model."""

        def __init__(self, image_classifier_tree_file_path, image_classifier_info_file_path, mode):
            self.image_classifier_tree_file_path = image_classifier_tree_file_path
            self.image_classifier_info_file_path = image_classifier_info_file_path
            self.mode = mode
            self.classifier_tree_dict = self.generate_classifier_tree_module()
            self.classifier_modules_dict = self.generate_classifier_module()

        def generate_classifier_tree_module(self):
            if (self.mode == 'dataflow'):
                fs = gcsfs.GCSFileSystem()
                with fs.open(self.image_classifier_tree_file_path) as image_classifier_catalog:
                    classifier_tree_data_frame = pd.read_json(image_classifier_catalog, lines=True)
                    classifier_tree_dict = classifier_tree_data_frame.to_dict('records')[0]
            else:
                classifier_tree_data_frame = pd.read_json(self.image_classifier_tree_file_path, lines=True)
                classifier_tree_dict = classifier_tree_data_frame.to_dict('records')[0]
            return classifier_tree_dict;

        def generate_classifier_module(self):
            classifier_modules_dict = {}
            if (self.mode == 'dataflow'):
                fs = gcsfs.GCSFileSystem()
                with fs.open(self.image_classifier_info_file_path) as image_classifier_catalog:
                    image_classifier_data_frame = pd.read_json(image_classifier_catalog, lines=True)
                    image_classifier_dict = image_classifier_data_frame.to_dict('records')[0]
            else:
                image_classifier_data_frame = pd.read_json(self.image_classifier_info_file_path, lines=True)
                image_classifier_dict = image_classifier_data_frame.to_dict('records')[0]

            for classifier_module, classifier_module_dtls in image_classifier_dict.items():
                classifier_modules_dict[classifier_module] = ImageClassifierUtils.model_file_loader(
                    classifier_module_dtls)

            return classifier_modules_dict;

    _thread_local = threading.local()

    def __init__(self):
        self._model_state = None

    def process(self, element, image_classifier_tree_file_path, image_classifier_info_file_path, mode):
        if self._model_state is None:
            if (getattr(self._thread_local, "model_state", None) is None or
                    self._thread_local.model_state.image_classifier_tree_file_path != image_classifier_tree_file_path or
                    self._thread_local.model_state.image_classifier_info_file_path != image_classifier_info_file_path or
                    self._thread_local.model_state.mode != mode):
                start = datetime.datetime.now()
                self._thread_local.model_state = self._ModelState(image_classifier_tree_file_path,
                                                                  image_classifier_info_file_path, mode)
                print('time taken to load model %d', (datetime.datetime.now() - start).total_seconds())
            self._model_state = self._thread_local.model_state
        else:
            assert self._model_state.image_classifier_tree_file_path == image_classifier_tree_file_path
            assert self._model_state.image_classifier_info_file_path == image_classifier_info_file_path

        thread_classifier_tree_dict = self._model_state.classifier_tree_dict

        (oms_id, category_image_dtls_list) = element
        label=""
        processed_image_dict ={}
        image_classification_list = []
        for productCategoryImageDtlsVO in category_image_dtls_list:
                category_id = productCategoryImageDtlsVO.category_id;
                image_url_dtls_list = productCategoryImageDtlsVO.image_dtls_list;
                #print('category_id',category_id,'image_url_dtls_list',image_url_dtls_list)
                #image_classification_list = []
                for image_dtls_dict in image_url_dtls_list:
                    try:
                        image_url  =  image_dtls_dict['image_url']
                        image_id   =  image_dtls_dict['image_id']
                        if image_id in processed_image_dict:
                            json_data = processed_image_dict[image_id]
                            oms_id = json_data['oms_id']
                            label = json_data['label']
                            image_available =json_data['image_available']
                            image_url = json_data['image_url']
                            predictions = json_data['predictions']
                            #print("*****prediction, case 1:", predictions)
                            category_modified_json_data = GenericUtils.generate_image_classification_json(oms_id,label,category_id,image_available,image_url,predictions)
                            #print("******json, case 1:",category_modified_json_data)
                            image_classification_list.append(str(json.dumps(category_modified_json_data)))
                        else:
                            image_np_array = ImageClassifierUtils.download_image(image_url)
                            if image_np_array.size > 0:
                                if category_id in thread_classifier_tree_dict:
                                    classifier_tree = thread_classifier_tree_dict[category_id]
                                else:
                                    classifier_tree = thread_classifier_tree_dict['unfound_category']
                                predictions = ImageClassifierUtils.climb_classifier_tree(image_np_array, classifier_tree,
                                                                                         self._model_state.classifier_modules_dict,
                                                                                         [])
                                #print("*****prediction, case 2:",predictions)
                                image_available="Y"
                                json_data = GenericUtils.generate_image_classification_json(oms_id,label,category_id,image_available,image_url,predictions)
                                processed_image_dict[image_id] = json_data
                                #print("******json, case 2:",json_data)
                                image_classification_list.append(str(json.dumps(json_data)))
                    except Exception:
                        logging.error('Error in running ProductClassifierMain', exc_info=True)
                        image_available = "N"
                        predictions=""
                        json_data = GenericUtils.generate_image_classification_json(oms_id, label, category_id,image_available, image_url,predictions)
                        processed_image_dict[image_id]=json_data
                        image_classification_list.append(str(json.dumps(json_data)))

        if image_classification_list:
            for image_classification in image_classification_list:
              yield image_classification
