import pytest
from com.homedepot.product_classifier_test.dofunctions.do_functions_to_test import *
import json

class TestClassifiedOutputAsInputMergedFullDoFn():
    def test_process(self):
        (oms_id, dtls) = ('100000001', {'image_classify_full_tag':["chair|https://images.homedepot-static.com/productImages/f36c3cd5***.jpg|Y|lifestyle"],
                                        'image_classify_delta_tag':["table|https://images.homedepot-static.com/productImages/dadad1371903***.jpg|Y|closeup"]})
        expected_output = "table|100000001|https://images.homedepot-static.com/productImages/dadad1371903***.jpg|Y|closeup"
        for i in ClassifiedOutputAsInputMergedFullDoFn.process('ddd',(oms_id,dtls)):
            #print(i)
            assert i == expected_output

        (oms_id, dtls) = ('100000001', {'image_classify_full_tag': ["chair|https://images.homedepot-static.com/productImages/f36c3cd5***.jpg|Y|lifestyle"],
                                        'image_classify_delta_tag': []})
        expected_output = "chair|100000001|https://images.homedepot-static.com/productImages/f36c3cd5***.jpg|Y|lifestyle"
        for i in ClassifiedOutputAsInputMergedFullDoFn.process('ddd',(oms_id,dtls)):
            #print(i)
            assert i == expected_output

        (oms_id, dtls) = ('100000001', {'image_classify_full_tag': [],
                                        'image_classify_delta_tag': ["table|https://images.homedepot-static.com/productImages/dadad1371903***.jpg|Y|closeup"]})
        expected_output = "table|100000001|https://images.homedepot-static.com/productImages/dadad1371903***.jpg|Y|closeup"
        for i in ClassifiedOutputAsInputMergedFullDoFn.process('ddd',(oms_id,dtls)):
            #print(i)
            assert i == expected_output
