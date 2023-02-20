import logging
import json

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class MilvusConfig:

    def __init__(self, service_name, host, port, collection_json):
        """Initializer for Milvus instance config"""
        self.__service_name = service_name
        self.__host = host
        self.__port = port
        self.__collection = json.loads(collection_json)

    @classmethod
    def from_flask_app(cls, current_app):
        """Initialize MilvusConfig using the config contained in a given Flask app"""
        log.info("Initializing Milvus config from Flask current app")
        config = current_app.config
        return cls(config.get('SERVICE_NAME'), config.get('MILVUS_HOST'), config.get('MILVUS_PORT'), config.get('MILVUS_COLLECTION'))

    def get_service_name(self):
        return self.__service_name

    def get_host(self):
        return self.__host

    def get_port(self):
        return self.__port

    def get_collection(self):
        return self.__collection
