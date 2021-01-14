import apache_beam as beam
from apache_beam.pvalue import AsDict

from com.homedepot.product_classifier.dofunctions.ProductCategoryDetailsExtractionDoFn import \
    ProductCategoryDetailsExtractionDoFn


class CatgpenrelTransformations(beam.PTransform):

    def __init__(self, catgpenrel_path):
        self.catgpenrel_path = catgpenrel_path

    def expand(self, pcoll):
        return (pcoll
                | 'CatgpenrelReader' >> beam.io.ReadFromText(self.catgpenrel_path)
                | 'CategoryExtractor' >> beam.ParDo(ProductCategoryDetailsExtractionDoFn())
                )
