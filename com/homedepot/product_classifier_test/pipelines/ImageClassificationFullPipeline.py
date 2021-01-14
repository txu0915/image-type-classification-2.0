import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from zope.interface import implementer

from com.homedepot.product_classifier.options.ProductClassificationOptions import ProductClassificationOptions
from com.homedepot.product_classifier.pipelines.DataFlowPipeline import DataFlowPipeline
from com.homedepot.product_classifier.transformations.CatgpenrelTransformations import CatgpenrelTransformations
from com.homedepot.product_classifier.transformations.ProductImageJsonTransformations import ProductImageJsonTransformations
from com.homedepot.product_classifier.dofunctions.ProductCategoryImageTransformDoFn import ProductCategoryImageTransformDoFn
from com.homedepot.product_classifier.dofunctions.ProductImageClassificationDoFn import ProductImageClassificationDoFn
from com.homedepot.product_classifier.utils.GoogleCloudUtils import GoogleCloudUtils

""" ImageClassificationPipeline to generate image classification output"""
@implementer(DataFlowPipeline)
class ImageClassificationFullPipeline():
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
        image_classifier_tree_file_path = self.productionClassificationOptions.imageClassifierTreeFilePath
        image_classifier_info_file_path = self.productionClassificationOptions.imageClassifierInfoFilePath
        image_classifier_output_path = self.productionClassificationOptions.imageClassificationOutputPath
        num_shards = int(self.productionClassificationOptions.numShards)
        mode =self.productionClassificationOptions.executionMode
        # if mode == 'dataflow' :
        #     classify_bucket_path_details = GenericUtils.bucket_path_details(image_classifier_output_path)
        #     classify_bucket_name= classify_bucket_path_details[2]
        #     classify_path_name = classify_bucket_path_details[3]
        #     print('classify_bucket_name',classify_bucket_name)
        #     print('classify_path_name', classify_path_name)
        #     GoogleCloudUtils.delete_gcs_objects(classify_bucket_name, classify_path_name)

        product_category_dtls_collection = self.pipeline | 'CategoryFilteredDtls' >> CatgpenrelTransformations(catgpenrel_dtls_path)
        product_image_dtls_collection = self.pipeline | 'ProductImageDtls' >> ProductImageJsonTransformations(product_json_dtls_path)
        product_category_image_dtls_collection = ({'product_category_dtls_tag': product_category_dtls_collection,
                                    'product_image_dtls_tag': product_image_dtls_collection}
                                   | 'ProductGroupBy' >> beam.CoGroupByKey())
        product_dtls_final_collection = product_category_image_dtls_collection | 'ProductDetails' >> beam.ParDo(ProductCategoryImageTransformDoFn())


        product_image_predict_collection = product_dtls_final_collection | 'ImageClassification' >> beam.ParDo(ProductImageClassificationDoFn(), image_classifier_tree_file_path,image_classifier_info_file_path, mode)
        product_image_predict_collection | 'ImageClassifyWriter' >> beam.io.WriteToText(image_classifier_output_path,append_trailing_newlines=True,num_shards=num_shards)

        pipeline_result = self.pipeline.run()

        state = pipeline_result.wait_until_finish()

        result = GoogleCloudUtils.data_flow_job_status(state)

        return result
