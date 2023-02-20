import logging
from kafka import KafkaConsumer

from config.kafka_consumer_config import KafkaConsumerConfig

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

__kafka_consumer = None


def init(config: KafkaConsumerConfig):
    global __kafka_consumer
    if __kafka_consumer is None:
        log.info(f'Initializing Kafka consumer with:\n- Bootstrap servers: {config.get_bootstrap_servers}\n- '
                 f'Topic: {config.get_topic_name}')
        # TODO: Parametrize for security settings
        __kafka_consumer = KafkaConsumer(config.get_topic_name(),
                                         auto_offset_reset=config.get_offset_reset(),
                                         bootstrap_servers=[config.get_bootstrap_servers()],
                                         group_id=config.get_group_id(),
                                         api_version=(0, 10))
    return __kafka_consumer
