import json
import gcsfs
import pandas as pd
import datetime
import threading

from com.homedepot.product_classifier.constants import Constants
from com.homedepot.product_classifier.utils.ImageClassifierUtils import ImageClassifierUtils
from com.homedepot.product_classifier.utils.GenericUtils import GenericUtils
from com.homedepot.product_classifier.pojo.ProductCategoryImageDtlsVO import ProductCategoryImageDtlsVO

### Functions modified a little bit to skip passing & handling beam and google cloud connectivity utilities...

class ProductJsonImgDtlsExtractorDoFn():
    def process(self, element):
        image_url_dict = json.loads(element)
        oms_id = image_url_dict['itemId']
        image_url_list = image_url_dict['imageUrl']
        filtered_image_list = []
        for image_url in image_url_list:
            image_url_tokens = image_url.split(Constants.FORWARD_SLASH)
            if (len(image_url_tokens) == 7):
                image_id = image_url_tokens[4]
                image_pixels_dtls = image_url_tokens[6]
                if (image_id is not None and image_pixels_dtls is not None and image_pixels_dtls.endswith('_1000.jpg')):
                    filtered_image_list.append({'image_url': image_url, 'image_id': image_id})
        return [(oms_id, filtered_image_list)]

class ProductCategoryDetailsExtractionDoFn():
    def process(self, element):
        category_id, oms_id, mark_for_delete = element.split(Constants.PIPE)
        return [(oms_id, category_id)]


class ProductCategoryImageTransformDoFn():
    ## Merging [(OMSID,filtered_image_list)] info with [(oms_id, category_id)] info
    def process(self, element):
        (oms_id, details) = element
        product_category_dtls_iter = details['product_category_dtls_tag']
        product_image_dtls_iter = details['product_image_dtls_tag']
        category_image_dtls_list = []
        if product_category_dtls_iter and product_image_dtls_iter:
            for category_id in product_category_dtls_iter:
                if category_id:
                    for product_image_list in product_image_dtls_iter:
                        if product_image_list:
                            category_image_dtls_list.append(ProductCategoryImageDtlsVO(category_id, product_image_list));
        if category_image_dtls_list:
            return [(oms_id, category_image_dtls_list)]


class ClassifiedOutputAsInputMergedFullDoFn():
    def process(self, element):
        #print(element)
        (oms_id, dtls) = element
        image_classify_full_iter = dtls['image_classify_full_tag']
        image_classify_delta_iter = dtls['image_classify_delta_tag']

        print(image_classify_full_iter, image_classify_delta_iter)
        if image_classify_full_iter and image_classify_delta_iter:
            for image_classify_delta_list in image_classify_delta_iter:
                if image_classify_delta_list:
                    category, image_url, image_available, predictions= image_classify_delta_list.split(Constants.PIPE)
                    print("case 1")
                    print(category + Constants.PIPE + oms_id + Constants.PIPE + image_url + Constants.PIPE + image_available + Constants.PIPE + predictions)
                    #yield category + Constants.PIPE + oms_id + Constants.PIPE + image_url + Constants.PIPE + image_available + Constants.PIPE + predictions
        elif image_classify_full_iter and not image_classify_delta_iter:
            for image_classify_full_list in image_classify_full_iter:
                if image_classify_full_list:
                    category, image_url, image_available, predictions = image_classify_full_list.split(Constants.PIPE)
                    print("case 2")
                    print(category + Constants.PIPE + oms_id + Constants.PIPE + image_url + Constants.PIPE + image_available + Constants.PIPE + predictions)
                    #yield category + Constants.PIPE + oms_id + Constants.PIPE + image_url + Constants.PIPE + image_available + Constants.PIPE + predictions
        elif not image_classify_full_iter and image_classify_delta_iter:
            for image_classify_delta_list in image_classify_delta_iter:
                if image_classify_delta_list:
                    category, image_url, image_available, predictions = image_classify_delta_list.split(Constants.PIPE)
                    print("case 3")
                    print(category + Constants.PIPE + oms_id + Constants.PIPE + image_url + Constants.PIPE + image_available + Constants.PIPE + predictions)
                    #yield category + Constants.PIPE + oms_id + Constants.PIPE + image_url + Constants.PIPE + image_available + Constants.PIPE + predictions

class ClassifiedOutputAsInputExtractionMergedFullDoFn():
    def process(self, element):
        image_url_dict = json.loads(element)
        oms_id = image_url_dict['oms_id']
        image_url = image_url_dict['image_url']
        category = image_url_dict['category']
        image_available = image_url_dict['image_available']
        predictions = str(image_url_dict['predictions'])
        print([predictions])
        return [(oms_id,category+Constants.PIPE+image_url+Constants.PIPE+image_available+Constants.PIPE+predictions)]

class ProductCategoryImageInputDeltaDoFn():

    def process(self, element):
        (oms_id, dtls) = element
        current_product_dtls_iter = dtls['current_product_dtls_tag']
        previous_product_dtls_iter = dtls['previous_product_dtls_tag']

        if current_product_dtls_iter and previous_product_dtls_iter:
            current_product_dtls_tuple = current_product_dtls_iter[0]
            previous_product_dtls_tuple = previous_product_dtls_iter[0]
            i = 0
            j = 0
            current_image_url_list = []
            current_category_id_list = []
            previous_image_url_list = []
            previous_category_id_list = []
            for currentProductCategoryImageDtlsVO in current_product_dtls_tuple:
                current_category_id = currentProductCategoryImageDtlsVO.category_id
                current_image_dtls_list = currentProductCategoryImageDtlsVO.image_dtls_list
                print(current_category_id, current_image_dtls_list)
                current_category_id_list.append(current_category_id)
                if i == 0:
                    for current_image_details_dict in current_image_dtls_list:
                        image_url = current_image_details_dict['image_url']
                        current_image_url_list.append(image_url)
                i = i + 1

            for previousProductCategoryImageDtlsVO in previous_product_dtls_tuple:
                previous_category_id = previousProductCategoryImageDtlsVO.category_id
                previous_image_dtls_list = previousProductCategoryImageDtlsVO.image_dtls_list
                print(previous_category_id,previous_image_dtls_list)
                previous_category_id_list.append(previous_category_id)
                if j == 0:
                    for previous_image_details_dict in previous_image_dtls_list:
                        image_url = previous_image_details_dict['image_url']
                        previous_image_url_list.append(image_url)
                    j = j + 1

            if not sorted(current_image_url_list) == sorted(previous_image_url_list):
                return [(oms_id, current_product_dtls_tuple)]

            elif not sorted(current_category_id_list) == sorted(previous_category_id_list):
                return [(oms_id, current_product_dtls_tuple)]

        elif current_product_dtls_iter and not previous_product_dtls_iter:
            current_product_dtls_tuple = current_product_dtls_iter[0]
            return [(oms_id, current_product_dtls_tuple)]
        else:
            pass

class ProductImageClassificationDoFn():
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
                            print('processed image found',oms_id,category_id,image_url[-9:])
                            category_modified_json_data = GenericUtils.generate_image_classification_json(oms_id,label,category_id,image_available,image_url,predictions)
                            #print("******json, case 1:",category_modified_json_data)
                            image_classification_list.append(str(json.dumps(category_modified_json_data)))
                        else:
                            print('first seen image',oms_id, category_id, image_url[-9:])
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
                        image_available = "N"
                        predictions=""
                        json_data = GenericUtils.generate_image_classification_json(oms_id, label, category_id,image_available, image_url,predictions)
                        processed_image_dict[image_id]=json_data
                        image_classification_list.append(str(json.dumps(json_data)))

        if image_classification_list:
            for image_classification in image_classification_list:
              yield image_classification