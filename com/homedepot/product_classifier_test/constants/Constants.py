COMMA = ','
PIPE = '|'
FORWARD_SLASH = '/'
DOT = '.'
WHITE_THRESHOLD = 0.1
ASTERISK = '*'
IMAGE_SIZE = 224
EMPTY_LIST = []
EMPTY_STRING = ""
test_module_3_class = {
		"embeddings_extractor": ["gs://hd-datascience-np-artifacts/releases/com.homedepot.personalization/product-image-classifier-2.0/input-files/0.0.1/input-model-files/vgg16_embeddings_generic_3_class.h5", "gs://hd-datascience-np-artifacts/releases/com.homedepot.personalization/product-image-classifier-2.0/input-files/0.0.1/input-model-files/resnet50_embeddings_generic_3_class.h5"],
		"classifier": "gs://hd-datascience-np-artifacts/releases/com.homedepot.personalization/product-image-classifier-2.0/input-files/0.0.1/input-model-files/xgboost_random_image_filter_generic_3_class.h5",
		"classes": ["silo", "closeup", "lifestyle"],
		"opencv_feature_list": ["average_pixel_width", "touch_the_border", "dark_pctg"],
		"info": "This classifier distinguishes silo/closeup/lifestyle views"
	    }
test_module_10_class = {
            "embeddings_extractor": [],
            "classifier": "gs://hd-datascience-np-artifacts/releases/com.homedepot.personalization/product-image-classifier-2.0/input-files/0.0.1/input-model-files/vgg19_random_generic_10_class.h5",
            "classes": ["angled", "back", "front", "graphic", "lineart", "open", "set", "side", "swatch", "top"],
            "opencv_feature_list": [],
            "info": "This classifier distinguishes 10-class product views"
        }

test_cat_list = ['036d1251-c31e-4f5a-95dc-89b0242ae1e5','036d1251-c31e-4f5a-95dc-89b0242ae1e6']
test_img_list = [{
                                  'image_url': 'https://images.homedepot-static.com/productImages/02e7d98c-5f38-4472-9162-b2ca874cfbef/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                  'image_id': '02e7d98c-5f38-4472-9162-b2ca874cfbef'},
                              {
                                  'image_url': 'https://images.homedepot-static.com/productImages/421be4e1-9be2-4024-83f9-c21a54da2511/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                  'image_id': '421be4e1-9be2-4024-83f9-c21a54da2511'},
                              {
                                  'image_url': 'https://images.homedepot-static.com/productImages/756de539-5555-4485-9b68-cc448fc95aed/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                  'image_id': '756de539-5555-4485-9b68-cc448fc95aed'},
                              {
                                  'image_url': 'https://images.homedepot-static.com/productImages/70a7d748-6499-4d04-9b62-e178506b23d0/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                  'image_id': '70a7d748-6499-4d04-9b62-e178506b23d0'},
                              {
                                  'image_url': 'https://images.homedepot-static.com/productImages/80e42666-ffda-4279-bd59-d183010e2917/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                  'image_id': '80e42666-ffda-4279-bd59-d183010e2917'},
                              {
                                  'image_url': 'https://images.homedepot-static.com/productImages/f36c3cd5-21ab-47a0-a27d-b962946ce9de/svn/grey-innovative-textile-solutions-slipcovers-9050chaigrey-64_1000.jpg',
                                  'image_id': 'f36c3cd5-21ab-47a0-a27d-b962946ce9de'}]