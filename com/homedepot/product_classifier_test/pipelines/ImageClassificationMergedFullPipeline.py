import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from zope.interface import implementer

from com.homedepot.product_classifier.dofunctions.ClassifiedOutputAsInputMergedFullDoFn import ClassifiedOutputAsInputMergedFullDoFn
from com.homedepot.product_classifier.options.ProductClassificationOptions import ProductClassificationOptions
from com.homedepot.product_classifier.pipelines.DataFlowPipeline import DataFlowPipeline
from com.homedepot.product_classifier.transformations.ClassifiedOutputAsInputTransformations import ClassifiedOutputAsInputTransformations

from com.homedepot.product_classifier.utils.GoogleCloudUtils import GoogleCloudUtils


@implementer(DataFlowPipeline)
class ImageClassificationMergedFullPipeline():
    pipeline = None
    ProductClassificationOptions = None

    """ Function to create pipeline with pipeline options
        Input Parameters : command line arguments 
    """

    def create_pipeline(self, argv):
        options = PipelineOptions(argv)
        self.ProductClassificationOptions = options.view_as(ProductClassificationOptions)
        self.pipeline = beam.Pipeline(options=self.ProductClassificationOptions)

    """ Function to execute pipeline with pipeline options
    """


    def execute(self):
        mode = self.ProductClassificationOptions.executionMode
        num_shards = int(self.ProductClassificationOptions.numShards)
        image_classify_previous_full_output_path = self.ProductClassificationOptions.imageClassificationOutputPath
        image_classify_delta_output_path = self.ProductClassificationOptions.imageClassificationOutputPath_Delta
        image_classify_merged_output_path = self.ProductClassificationOptions.imageClassificationOutputPath_MergedFull


        # if mode == 'dataflow':
        #
        #     classify_bucket_path_details = GenericUtils.bucket_path_details(image_classify_merged_output_path)
        #     classify_bucket_name= classify_bucket_path_details[2]
        #     classify_path_name = classify_bucket_path_details[3]
        #
        #     GoogleCloudUtils.delete_gcs_objects(classify_bucket_name, classify_path_name)
        #
        #
        #     emebddings_bucket_path_details = GenericUtils.bucket_path_details(product_embed_merged_output_path)
        #     emebddings_bucket_name = emebddings_bucket_path_details[2]
        #     emebddings_path_name = emebddings_bucket_path_details[3]
        #
        #     GoogleCloudUtils.delete_gcs_objects(emebddings_bucket_name, emebddings_path_name)


        '''image classification merged full feed generation'''

        image_classify_full_transform_collection = self.pipeline | 'ImageFullTransform' >> ClassifiedOutputAsInputTransformations(image_classify_previous_full_output_path)

        image_classify_delta_transform_collection = self.pipeline | 'ImageDeltaTransform' >> ClassifiedOutputAsInputTransformations(image_classify_delta_output_path)

        classify_full_delta_join_collection = ({'image_classify_full_tag': image_classify_full_transform_collection,'image_classify_delta_tag': image_classify_delta_transform_collection}
                                               | 'ClassifiedOutputsGroupBy' >> beam.CoGroupByKey())
        classify_merged_full_collection = classify_full_delta_join_collection |'ImageClassifyMergedFull' >> beam.ParDo(ClassifiedOutputAsInputMergedFullDoFn())

        classify_merged_full_collection | 'ImageClassifyMergedFullWriter' >> beam.io.WriteToText(image_classify_merged_output_path,append_trailing_newlines=True,num_shards=num_shards)

        pipeline_result = self.pipeline.run()

        state = pipeline_result.wait_until_finish()

        result = GoogleCloudUtils.data_flow_job_status(state)

        return result