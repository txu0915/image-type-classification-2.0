import pytest
from com.homedepot.product_classifier_test.dofunctions.do_functions_to_test import *
import json

class TestProductCategoryImageInputDeltaDoFn():
    def test_process(self):
        (oms_id, details) = ('100000001', {'product_category_dtls_tag': [['036d1251-c31e-4f5a-95dc-89b0242ae1e6']],
                                           'product_image_dtls_tag':
                                               [[{
                                                       'image_url': 'https://images.homedepot-static.com/productImages/70a7d748-6499-4d04-9b62-e178506b23d0/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                                       'image_id': '70a7d748-6499-4d04-9b62-e178506b23d0'},
                                                   {
                                                       'image_url': 'https://images.homedepot-static.com/productImages/80e42666-ffda-4279-bd59-d183010e2917/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                                       'image_id': '80e42666-ffda-4279-bd59-d183010e2917'},
                                                   {
                                                       'image_url': 'https://images.homedepot-static.com/productImages/f36c3cd5-21ab-47a0-a27d-b962946ce9de/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                                       'image_id': 'f36c3cd5-21ab-47a0-a27d-b962946ce9de'}]]
                                           })
        previous_product_dtls_tag = ProductCategoryImageTransformDoFn.process('data', (oms_id, details))
        (oms_id, details) = ('100000001', {'product_category_dtls_tag': [['036d1251-c31e-4f5a-95dc-89b0242ae1e5']],
                                           'product_image_dtls_tag':
                                               [[{'image_url': 'https://images.homedepot-static.com/productImages/02e7d98c-5f38-4472-9162-b2ca874cfbef/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                                   'image_id': '02e7d98c-5f38-4472-9162-b2ca874cfbef'},
                                                   {
                                                       'image_url': 'https://images.homedepot-static.com/productImages/421be4e1-9be2-4024-83f9-c21a54da2511/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                                       'image_id': '421be4e1-9be2-4024-83f9-c21a54da2511'},
                                                   {
                                                       'image_url': 'https://images.homedepot-static.com/productImages/756de539-5555-4485-9b68-cc448fc95aed/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                                       'image_id': '756de539-5555-4485-9b68-cc448fc95aed'},
                                                   ]]
                                           })
        current_product_dtls_tag = ProductCategoryImageTransformDoFn.process('data',(oms_id,details))

        (oms_id,element) = ('100000001',{'current_product_dtls_tag':[current_product_dtls_tag[0][1]],'previous_product_dtls_tag':[previous_product_dtls_tag[0][1]]})
        ProductCategoryImageInputDeltaDoFn.process("dada",(oms_id,element))

        assert Exception