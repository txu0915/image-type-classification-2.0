import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from zope.interface import implementer

from com.homedepot.product_classifier.options.ProductClassificationOptions import ProductClassificationOptions
from com.homedepot.product_classifier.pipelines.DataFlowPipeline import DataFlowPipeline
from com.homedepot.product_classifier.transformations.CatgpenrelTransformations import CatgpenrelTransformations
from com.homedepot.product_classifier.transformations.ProductImageJsonTransformations import ProductImageJsonTransformations
from com.homedepot.product_classifier.dofunctions.ProductCategoryImageTransformDoFn import ProductCategoryImageTransformDoFn
from com.homedepot.product_classifier.dofunctions.ProductCategoryImageInputDeltaDoFn import ProductCategoryImageInputDeltaDoFn
from com.homedepot.product_classifier.dofunctions.ProductImageClassificationDoFn import ProductImageClassificationDoFn
from com.homedepot.product_classifier.utils.GoogleCloudUtils import GoogleCloudUtils

""" Image Classification Delta Pipeline to generate Delta-Mode image classification output"""
@implementer(DataFlowPipeline)
class ImageClassificationDeltaPipeline():
    pipeline = None
    productionClassificationOptions = None

    """ Function to create pipeline with pipeline options
        Input Parameters : command line arguments 
    """

    def create_pipeline(self, argv):
        options = PipelineOptions(argv)
        self.productionClassificationOptions = options.view_as(ProductClassificationOptions)
        self.pipeline = beam.Pipeline(options=self.productionClassificationOptions)

    """ Function to execute pipeline with pipeline options
    """

    def execute(self):
        catgpenrel_dtls_path = self.productionClassificationOptions.catgpenRelFile
        product_json_dtls_path = self.productionClassificationOptions.productJsonDtlsFile
        previous_catgpenrel_dtls_path = self.productionClassificationOptions.catgpenRelFilePreviousDate
        previous_product_json_dtls_path = self.productionClassificationOptions.productJsonDtlsFilePreviousDate

        product_category_dtls_collection = self.pipeline | 'CategoryFilteredDtls' >> CatgpenrelTransformations(catgpenrel_dtls_path)
        product_image_dtls_collection = self.pipeline | 'ProductImageDtls' >> ProductImageJsonTransformations(product_json_dtls_path)
        product_category_image_dtls_collection = ({'product_category_dtls_tag': product_category_dtls_collection,'product_image_dtls_tag': product_image_dtls_collection} | 'ProductGroupBy' >> beam.CoGroupByKey())
        product_dtls_final_collection = product_category_image_dtls_collection | 'ProductDetails' >> beam.ParDo(ProductCategoryImageTransformDoFn())


        previous_product_category_dtls_collection = self.pipeline | 'PreviousCategoryFilteredDtls' >> CatgpenrelTransformations(previous_catgpenrel_dtls_path)
        previous_product_image_dtls_collection = self.pipeline | 'PreviousProductImageDtls' >> ProductImageJsonTransformations(previous_product_json_dtls_path)
        previous_product_category_image_dtls_collection = ({'product_category_dtls_tag': previous_product_category_dtls_collection,'product_image_dtls_tag': previous_product_image_dtls_collection} | 'ProductGroupByPrevious' >> beam.CoGroupByKey())
        Previous_product_dtls_final_collection = previous_product_category_image_dtls_collection | 'ProductDetailsPrevious' >> beam.ParDo(ProductCategoryImageTransformDoFn())

        ## Computing Delta from here...
        # Merging before & after input data sets
        product_dtls_merged_full_collection = ({'current_product_dtls_tag': product_dtls_final_collection,'previous_product_dtls_tag': Previous_product_dtls_final_collection} | 'ProductGroupByDelta' >> beam.CoGroupByKey())
        # Calculate and return the delta inputs
        product_dtls_delta_collection = product_dtls_merged_full_collection | 'CalculateDelta' >> beam.ParDo(ProductCategoryImageInputDeltaDoFn())
        ## End of computing Delta...

        image_classifier_tree_file_path = self.productionClassificationOptions.imageClassifierTreeFilePath
        image_classifier_info_file_path = self.productionClassificationOptions.imageClassifierInfoFilePath
        image_classifier_output_path = self.productionClassificationOptions.imageClassificationOutputPath_Delta
        num_shards = int(self.productionClassificationOptions.numShards)
        mode = self.productionClassificationOptions.executionMode

        product_image_predict_collection = product_dtls_delta_collection | 'ImageClassification' >> beam.ParDo(ProductImageClassificationDoFn(), image_classifier_tree_file_path, image_classifier_info_file_path, mode)
        product_image_predict_collection | 'ImageClassifyWriter' >> beam.io.WriteToText(image_classifier_output_path, append_trailing_newlines=True,num_shards=num_shards)

        pipeline_result = self.pipeline.run()
        state = pipeline_result.wait_until_finish()
        result = GoogleCloudUtils.data_flow_job_status(state)
        return result

