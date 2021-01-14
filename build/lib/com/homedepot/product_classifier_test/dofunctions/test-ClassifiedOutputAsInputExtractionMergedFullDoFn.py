import pytest
from com.homedepot.product_classifier_test.dofunctions.do_functions_to_test import *
import json

class TestClassifiedOutputAsInputExtractionMergedFullDoFn():
    def test_process(self):
        classification = {'oms_id':'100000001','image_url':"https://images.homedepot-static.com/productImages/f36c3cd5***.jpg",
                          'category':'chair','image_available':'Y','predictions':'lifestyle'}
        element = json.dumps(classification)
        expected_output = [('100000001', 'chair|https://images.homedepot-static.com/productImages/f36c3cd5***.jpg|Y|lifestyle')]
        assert ClassifiedOutputAsInputExtractionMergedFullDoFn.process("dad",element) == expected_output