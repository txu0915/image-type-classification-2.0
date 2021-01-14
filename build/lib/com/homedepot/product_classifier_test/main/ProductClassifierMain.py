import logging
import sys
sys.path.append('/Users/tianlongxu/Documents/My_Projects/image-classification-2.0')

from com.homedepot.product_classifier.driver import ClassificationDriver


class ProductClassifierMain:
    generic_driver = None

    def product_image_classifier(argv):
        generic_driver = ClassificationDriver.ClassificationDriver();
        result = generic_driver.processor(argv)
        return result;

    if __name__ == "__main__":
        result = -1
        args = sys.argv
        try:
            switch = {'PRODUCT_CLASSIFIER': product_image_classifier(args)}
            result = switch.get(args[1])
            sys.exit(result)
        except Exception:
            logging.error('Error in running ProductClassifierMain', exc_info=True)
            sys.exit(result)
