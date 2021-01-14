import pytest
from com.homedepot.product_classifier.utils.GenericUtils import *


class TestGenericUtils(GenericUtils):
    def test_get_date(self):
        ans = GenericUtils.get_date(0)
        assert ans == str(datetime.now().date())

    def test_bucket_path_details(self):
        my_str = "gs://hd-datascience-np-artifacts/tianlong/image_type_classifier/Classifiers/"
        assert GenericUtils.bucket_path_details(my_str) == \
               ['gs:','','hd-datascience-np-artifacts','tianlong/image_type_classifier/Classifiers/']


    def test_generate_image_classification_json(self):

        ans = {'oms_id': '001XX202', 'label': 'closeup', 'category': 'chair', 'image_available': 'y',
                     'image_url': 'www.google.com', 'predictions': 'lifestyle'}
        omsid = '001XX202'
        label = 'closeup'
        category = 'chair'
        image_available = 'y'
        image_url = 'www.google.com'
        predictions = 'lifestyle'
        assert GenericUtils.generate_image_classification_json(omsid,label,category,image_available,image_url,predictions) == ans

