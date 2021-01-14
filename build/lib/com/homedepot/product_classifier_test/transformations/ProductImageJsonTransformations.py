import apache_beam as beam

from com.homedepot.product_classifier.dofunctions.ProductJsonImgDtlsExtractorDoFn import ProductJsonImgDtlsExtractorDoFn


class ProductImageJsonTransformations(beam.PTransform):

    def __init__(self, product_json_dtls_path):
        self.product_json_dtls_path = product_json_dtls_path

    def expand(self, pcoll):
        return (pcoll
                | 'read product json' >> beam.io.ReadFromText(self.product_json_dtls_path, strip_trailing_newlines=True)
                | 'parse Product json' >> beam.ParDo(ProductJsonImgDtlsExtractorDoFn()))
