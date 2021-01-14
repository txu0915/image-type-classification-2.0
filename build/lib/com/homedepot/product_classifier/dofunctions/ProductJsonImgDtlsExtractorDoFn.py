import json

import apache_beam as beam

from com.homedepot.product_classifier.constants import Constants


class ProductJsonImgDtlsExtractorDoFn(beam.DoFn):

    def process(self, element):
        image_url_dict = json.loads(element)
        oms_id = image_url_dict['itemId']
        image_url_list = image_url_dict['imageUrl']
        filtered_image_list = []
        for image_url in image_url_list:
            image_url_tokens = image_url.split(Constants.FORWARD_SLASH)
            if (len(image_url_tokens) == 7):
                image_id = image_url_tokens[4]
                image_pixels_dtls = image_url_tokens[6]
                if (image_id is not None and image_pixels_dtls is not None and image_pixels_dtls.endswith('_1000.jpg')):
                    filtered_image_list.append({'image_url': image_url, 'image_id': image_id})
        return [(oms_id, filtered_image_list)]
