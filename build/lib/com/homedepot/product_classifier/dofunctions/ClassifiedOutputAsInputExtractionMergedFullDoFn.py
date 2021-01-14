import apache_beam as beam
import json

from com.homedepot.product_classifier.constants import Constants

class ClassifiedOutputAsInputExtractionMergedFullDoFn(beam.DoFn):

    def process(self, element):
        image_url_dict = json.loads(element)
        oms_id = image_url_dict['oms_id']
        image_url = image_url_dict['image_url']
        category = image_url_dict['category']
        image_available = image_url_dict['image_available']
        predictions = str(image_url_dict['predictions'])

        return [(oms_id,category+Constants.PIPE+image_url+Constants.PIPE+image_available+Constants.PIPE+predictions)]