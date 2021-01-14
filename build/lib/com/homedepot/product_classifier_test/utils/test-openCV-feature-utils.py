import pytest
from com.homedepot.product_classifier.utils.ImageClassifierUtils import ImageClassifierUtils
from com.homedepot.product_classifier.utils.OpenCVFeatureUtils import OpenCVFeatureUtils

class TestOpenCVFeatureUtils():
    def test_compute_feature(self):
        test_image_url = "https://images.homedepot-static.com/productImages/02e7d98c-5f38-4472-9162-b2ca874cfbef/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_400.jpg"
        test_img = ImageClassifierUtils.download_image(test_image_url)
        opencv_feature_list = ["average_pixel_width", "touch_the_border", "dark_pctg",
                               "rotation","dominant_color","number_of_object"]
        OpenCVFeatureUtils(opencv_feature_list, test_img).compute_feature()
        assert Exception

    def test_average_pixel_width(self):
        print("covered by test compute feature")
        assert Exception

    def test_touch_the_border(self):
        print("covered by test compute feature")
        assert Exception

    def test_perform_color_analysis(self):
        print("covered by test compute feature")
        assert Exception

    def test_rotation(self):
        print("covered by test compute feature")
        assert Exception

    def test_dominant_color(self):
        print("covered by test compute feature")
        assert Exception

    def test_number_of_object(self):
        print("covered by test compute feature")
        assert Exception


