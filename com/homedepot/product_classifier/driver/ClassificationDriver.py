from zope.interface import implementer

from com.homedepot.product_classifier.driver.GenericDriver import GenericDriver
from com.homedepot.product_classifier.pipelines.ImageClassificationFullPipeline import ImageClassificationFullPipeline
from com.homedepot.product_classifier.pipelines.ImageClassificationDeltaPipeline import ImageClassificationDeltaPipeline
from com.homedepot.product_classifier.pipelines.ImageClassificationMergedFullPipeline import ImageClassificationMergedFullPipeline

@implementer(GenericDriver)
class ClassificationDriver():
    result = -1

    def processor(self, argv):
        execution_mode = argv[2]
        if execution_mode == 'FULL':
            pipeline = ImageClassificationFullPipeline();
            pipeline.create_pipeline(argv)
            result = pipeline.execute()
            return result

        ## new added by Tianlong
        if execution_mode == 'DELTA':
            pipeline = ImageClassificationDeltaPipeline()
            pipeline.create_pipeline(argv)
            result = pipeline.execute()
            return result
        if execution_mode == 'MERGED_FULL':
            pipeline = ImageClassificationMergedFullPipeline()
            pipeline.create_pipeline(argv)
            result = pipeline.execute()
            return result
