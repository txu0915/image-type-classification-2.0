import apache_beam as beam

from com.homedepot.product_classifier.constants import Constants

class ClassifiedOutputAsInputMergedFullDoFn(beam.DoFn):
    def process(self, element):
        (oms_id, dtls) = element
        image_classify_full_iter = dtls['image_classify_full_tag']
        image_classify_delta_iter = dtls['image_classify_delta_tag']

        if image_classify_full_iter and image_classify_delta_iter:
            for image_classify_delta_list in image_classify_delta_iter:
                if image_classify_delta_list:
                    category, image_url, image_available, predictions= image_classify_delta_list.split(Constants.PIPE)
                    yield category + Constants.PIPE + oms_id + Constants.PIPE + image_url + Constants.PIPE + image_available + Constants.PIPE + predictions

        elif image_classify_full_iter and not image_classify_delta_iter:
            for image_classify_full_list in image_classify_full_iter:
                if image_classify_full_list:
                    category, image_url, image_available, predictions = image_classify_full_list.split(Constants.PIPE)
                    yield category + Constants.PIPE + oms_id + Constants.PIPE + image_url + Constants.PIPE + image_available + Constants.PIPE + predictions


        elif not image_classify_full_iter and image_classify_delta_iter:
            for image_classify_delta_list in image_classify_delta_iter:
                if image_classify_delta_list:
                    category, image_url, image_available, predictions = image_classify_delta_list.split(Constants.PIPE)
                    yield category + Constants.PIPE + oms_id + Constants.PIPE + image_url + Constants.PIPE + image_available + Constants.PIPE + predictions