import apache_beam as beam

from com.homedepot.product_classifier.dofunctions.ClassifiedOutputAsInputExtractionMergedFullDoFn import ClassifiedOutputAsInputExtractionMergedFullDoFn


class ClassifiedOutputAsInputTransformations(beam.PTransform):

    def __init__(self, product_json_dtls_path):
        self.product_json_dtls_path = product_json_dtls_path

    def expand(self, pcoll):
        return (pcoll
                | 'read classified output json' >> beam.io.ReadFromText(self.product_json_dtls_path, strip_trailing_newlines=True)
                | 'parse classified output json' >> beam.ParDo(ClassifiedOutputAsInputExtractionMergedFullDoFn()))