import logging

from minio import Minio
from minio.error import S3Error

from config.minio_config import MinioConfig

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class MinioInstance:

    def __init__(self, config: MinioConfig):
        self.__config = config

    def bootstrap(self):
        log.info("Bootstrapping minio client...")

        return Minio(
            self.__config.get_host(),
            access_key=self.__config.get_access_key(),
            secret_key=self.__config.get_secret_key(),
        )
