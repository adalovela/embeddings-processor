import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class MinioConfig:

    def __init__(self, host, port, access_key, secret_key):
        """Initializer for Minio config"""
        self.__host = host
        self.__port = port
        self.__access_key = access_key
        self.__secret_key = secret_key

    @classmethod
    def from_flask_app(cls, current_app):
        """Initialize MinioConfig using the config contained in a given Flask app"""
        log.info("Initializing Minio config from Flask current app")
        config = current_app.config
        return cls(config.get('MINIO_HOST'), config.get('MINIO_PORT'), config.get('MINIO_ACCESS_KEY'),
                   config.get('MINIO_SECRET_KEY'))

    def get_host(self):
        return self.__host

    def get_port(self):
        return self.__port

    def get_access_key(self):
        return self.__access_key

    def get_secret_key(self):
        return self.__secret_key


