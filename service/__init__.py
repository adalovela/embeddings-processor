import logging
import sys

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from config.kafka_consumer_config import KafkaConsumerConfig
from config.embeddings_processor_config import EmbeddingsProcessorConfig
from config.milvus_config import MilvusConfig
from config.minio_config import MinioConfig
from pymilvus import Collection

from milvus.milvus_instance import MilvusInstance
from service import kafka_consumer, emails_processor
from minio_utils.minio_client import MinioInstance

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

__milvus_collection = Collection


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    metrics = PrometheusMetrics(app)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=False)
    else:
        app.config.from_mapping(test_config)

    @app.route('/start')
    def start():
        global __milvus_collection
        service_name = app.config.get("SERVICE_NAME")
        log.info(f'Starting up service {service_name}')

        try:
            minio_config = MinioConfig.from_flask_app(app)
            minio_instance = MinioInstance(minio_config)
            minio_instance.bootstrap()
        except Exception as e:
            log.error(f"Error while bootstrapping Minio: {e}")
            sys.exit(1)

        try:
            milvus_config = MilvusConfig.from_flask_app(app)
            milvus_instance = MilvusInstance(milvus_config)
            __milvus_collection = milvus_instance.bootstrap()
        except Exception as e:
            log.error(f"Error while bootstrapping Milvus: {e}")
            sys.exit(1)

        try:
            kafka_config = KafkaConsumerConfig.from_flask_app(app)
            consumer = kafka_consumer.init(kafka_config)
        except Exception as e:
            log.error(f"Error while bootstrapping Kafka: {e}")
            sys.exit(1)

        processor_config = EmbeddingsProcessorConfig.from_flask_app(app)
        processor.init(__milvus_collection, consumer, processor_config)

        log.info(f'Service {service_name} successfully started up')

    return app
