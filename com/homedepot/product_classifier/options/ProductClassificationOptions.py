from apache_beam.options.pipeline_options import PipelineOptions


class ProductClassificationOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--catgpenRelFile',help='product category details file path',required=False)
        parser.add_argument('--productJsonDtlsFile',help='input path for product images json',required=False)
        parser.add_argument('--imageClassifierInfoFilePath', help='image classifiers path ', required=False)
        parser.add_argument('--imageClassifierTreeFilePath', help='image classifiers tree file path ', required=False)
        parser.add_argument('--imageClassificationOutputPath', help='Fullfeed image classification output path (normal process)', required=False)
        parser.add_argument('--numShards', help='number of files to writes', required=False)
        parser.add_argument('--executionMode', help='dataflow or local mode', required=False)

        parser.add_argument('--catgpenRelFilePreviousDate',help='previous input path for category details', required=False)
        parser.add_argument('--productJsonDtlsFilePreviousDate', help='previous input path for product image json', required=False)

        parser.add_argument('--imageClassificationOutputPath_Delta', help='Delta-mode image classification output path', required=False)
        parser.add_argument('--imageClassificationOutputPath_MergedFull',help='Merged-full image classification output path', required=False)



