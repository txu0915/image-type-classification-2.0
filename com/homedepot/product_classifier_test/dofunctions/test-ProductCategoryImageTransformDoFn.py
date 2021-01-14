import pytest
from com.homedepot.product_classifier_test.dofunctions.do_functions_to_test import *
from com.homedepot.product_classifier_test.constants.Constants import *
from com.homedepot.product_classifier.pojo.ProductCategoryImageDtlsVO import ProductCategoryImageDtlsVO
import json
import os
import cv2

class TestProductCategoryImageTransformDoFn():
    def test_process(self):
        (oms_id, details) = ('100000001',{'product_category_dtls_tag':[test_cat_list],
                             'product_image_dtls_tag':[test_img_list]
                             })
        ProductCategoryImageTransformDoFn.process('ddd',(oms_id,details))

        expected_output = ProductCategoryImageDtlsVO(test_cat_list,test_img_list)
        #print(ProductCategoryImageTransformDoFn.process('ddd',(oms_id,details))[0][1])
        assert ProductCategoryImageTransformDoFn.process('ddd',(oms_id,details))[0][1][0].category_id == expected_output.category_id
        assert ProductCategoryImageTransformDoFn.process('ddd',(oms_id,details))[0][1][0].image_dtls_list == expected_output.image_dtls_list

