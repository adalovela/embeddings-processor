import logging

import boto3

from config.minio_config import MinioConfig
from PIL import Image

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class MinioClient:

    def __init__(self, config: MinioConfig):
        s3_resource = boto3.resource(endpoint_url=config.get_host(),
                                     aws_access_key_id=config.get_access_key(),
                                     aws_secret_access_key=config.get_secret_key())
        self.__bucket = s3_resource.Bucket(config.get_bucket_name())

    def fetch_image(self, object_path: str):
        log.info(f"Fetching image in path: {object_path}")
        try:
            s3_object = self.__bucket.Object(object_path)
            response = s3_object.get()
            return Image.open(response['Body'])
        except Exception as e:
            log.error(f"Error while fetching image in path: {object_path}", e)
