import apache_beam as beam

from com.homedepot.product_classifier.constants import Constants


class ProductCategoryDetailsExtractionDoFn(beam.DoFn):
    def process(self, element):
        category_id, oms_id, mark_for_delete = element.split(Constants.PIPE)
        return [(oms_id, category_id)]
