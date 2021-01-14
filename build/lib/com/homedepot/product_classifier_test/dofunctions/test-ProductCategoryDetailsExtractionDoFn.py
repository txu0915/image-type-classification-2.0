import pytest
from com.homedepot.product_classifier_test.dofunctions.do_functions_to_test import *
import json


## By testing below, CatgpenrelTransformations covered implicitly
class TestProductCategoryDetailsExtractionDoFn():
    def test_process(self):
        category_input = '036d1251-c31e-4f5a-95dc-89b0242ae1e5|100000001|0'
        category_output = [('100000001', '036d1251-c31e-4f5a-95dc-89b0242ae1e5')]
        assert ProductCategoryDetailsExtractionDoFn.process('dd',category_input) == category_output