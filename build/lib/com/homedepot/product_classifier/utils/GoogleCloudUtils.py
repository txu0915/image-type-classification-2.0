import logging
import sys

from apache_beam.runners.runner import PipelineState
from google.cloud import storage


class GoogleCloudUtils:
    @staticmethod
    def delete_gcs_objects(bucketName, folder):
        print('Deleting objects from the bucket ', bucketName, folder)
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucketName)
        try:
            bucket.delete_blobs(blobs=bucket.list_blobs(prefix=folder))
        except Exception as e:
            logging.error('Error in running deleteGcsObjects method', exc_info=True)
            sys.exit(-1)

    @staticmethod
    def data_flow_job_status(state):
        try:
            if state == PipelineState.DONE:
                return 0
            else:
                return -1
        except Exception as e:
            logging.error('Error in dataflowJobStatus method', exc_info=True)
