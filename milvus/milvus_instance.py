import logging
import sys
import time
from pymilvus import connections, Collection, utility
from flask import g

from config.milvus_config import MilvusConfig
from . import collection_manager

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class MilvusInstance:

    def __init__(self, config: MilvusConfig):
        self.__config = config
        self.__milvus_connection_alias = config.get_service_name() + "-milvus-conn"
        self.__collection = config.get_collection()
        self.__collection_name = self.__collection['collection_name']

    def bootstrap(self):
        log.info("Bootstrapping milvus...")

        self.__connect(self.__config)

        if utility.has_collection(collection_name=self.__collection_name, using=self.__milvus_connection_alias):
            log.info(f"Collection {self.__collection_name} is already present in milvus. Skipping creation...")
        else:
            try:
                new_collection = collection_manager.create_collection(self.__config.get_collection(),
                                                                      self.__config.get_host(),
                                                                      self.__config.get_port())
                log.info(f"Created new collection:\n name: {new_collection.name}\nschema: {new_collection.schema} "
                         f"and index: {new_collection.indexes}")
            except Exception as e:
                raise Exception(f'Error while creating connection in Milvus: {e}')

        return self.__get_collection()

    def __connect(self, config: MilvusConfig):
        milvus_host = config.get_host()
        milvus_port = config.get_port()

        log.info(f'Proceeding to establish connection with Milvus on host: {milvus_host} - port {milvus_port} '
                 f'with alias: {self.__milvus_connection_alias}')

        try:
            connections.connect(alias=self.__milvus_connection_alias, host=milvus_host, port=milvus_port)
            log.info("Connection to Milvus successfully established")
        except Exception as e:
            raise Exception(f'Error while establishing connection to Milvus: {e}')

    def __get_collection(self):
        waiting_time_secs = 1
        increment_secs = 2
        retries = 5

        try:
            for _ in range(retries):
                if connections.has_connection(self.__milvus_connection_alias):
                    log.info(f'Attempting to retrieve Milvus connection: {self.__collection_name}')
                    return Collection(self.__collection_name, using=self.__milvus_connection_alias)

                log.info(f'Milvus connection still not ready. Will sleep for {waiting_time_secs} seconds...')
                time.sleep(waiting_time_secs)
                waiting_time_secs = waiting_time_secs + increment_secs

        except Exception as e:
            log.error(f'Error while establishing connection to Milvus: {e}')
            raise Exception("Milvus collection could not be retrieved")

    def disconnect(self):
        if 'collection' in g:
            log.info(f'Proceeding to close connection with alias: {self.__milvus_connection_alias}')

            try:
                connections.disconnect(self.__milvus_connection_alias)
                _is_milvus_connected = False
                log.info("Connection to Milvus successfully closed")
            except Exception as e:
                log.error(f'"Error while establishing connection to Milvus: {e}')
