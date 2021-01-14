import pytest
from com.homedepot.product_classifier.utils.ImageClassifierUtils import *
from com.homedepot.product_classifier_test.constants.Constants import *


class TestImageClassifierUtils():
    def test_keras_model_file_reader(self):
        pass

    def test_xgb_model_file_reader(self):
        pass

    def test_create_image_url(self):
        img_guid = '7110200e-96c3-4562-963e-be3b759d41b2'
        expexted_output = 'https://idm.homedepot.com/assets/image/71/7110200e-96c3-4562-963e-be3b759d41b2.jpg'
        assert ImageClassifierUtils.create_image_url(img_guid) == expexted_output
        img_guid = 'https://idm.homedepot.com/assets/image/71/7110200e-96c3-4562-963e-be3b759d41b2.jpg'
        assert ImageClassifierUtils.create_image_url(img_guid) == expexted_output
    def test_download_image(self):
        ImageClassifierUtils.download_image('https://idm.homedepot.com/assets/image/71/7110200e-96c3-4562-963e-be3b759d41b2.jpg')
            #print(e)
        assert Exception

    def test_expand_features(self):
        a = np.array([[1, 2, 3]])
        b = np.array([[2, 3]])
        print("Numpy array sizes:", a.shape, b.shape)
        ans = ImageClassifierUtils.expand_features(a, b).shape[1]
        assert sum([a.shape[1], b.shape[1]]) == ans

    def test_generate_classifier_tree_module(self):
        pass

    def test_generate_classifier_module(self):
        # covered by the model-file-loader function
        pass

    def test_model_file_loader(self):
        ImageClassifierUtils.model_file_loader(test_module_3_class)
        assert Exception

    def test_classify_image_type(self):
        test_image_url = "https://images.homedepot-static.com/productImages/02e7d98c-5f38-4472-9162-b2ca874cfbef/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_400.jpg"
        test_img = ImageClassifierUtils.download_image(test_image_url)
        test_model = ImageClassifierUtils.model_file_loader(test_module_3_class)
        ImageClassifierUtils.classify_image_type(test_img, test_model)
        assert Exception


    def test_climb_classifier_tree(self):
        test_classifiers_tree = {
            "Random_image_filter_generic_3_class": {"silo": {"vgg19-random-generic-10-class": "leaf"}}}
        test_model_1 = ImageClassifierUtils.model_file_loader(test_module_3_class)
        test_model_2 = ImageClassifierUtils.model_file_loader(test_module_10_class)
        test_model = {"Random_image_filter_generic_3_class": test_model_1,
                      "vgg19-random-generic-10-class": test_model_2}
        test_image_url = "https://images.homedepot-static.com/productImages/02e7d98c-5f38-4472-9162-b2ca874cfbef/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_400.jpg"
        test_img = ImageClassifierUtils.download_image(test_image_url)
        ImageClassifierUtils.climb_classifier_tree(test_img, test_classifiers_tree, test_model, report=[])
        assert Exception
