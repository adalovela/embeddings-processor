import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class KafkaConsumerConfig:
    def __init__(self, bootstrap_servers, topic_name, group_id, api_version, security_protocol, sasl_mechanism, offset_reset):
        """Initialize KafkaConsumerConfig"""
        log.info("Initializing Kafka consumer config from the list of provided parameters")
        self.__bootstrap_servers = bootstrap_servers
        self.__topic_name = topic_name
        self.__group_id = group_id
        self.__api_version = api_version
        self.__security_protocol = security_protocol
        self.__sasl_mechanism = sasl_mechanism
        self.__offset_reset = offset_reset

    @classmethod
    def from_flask_app(cls, current_app):
        """Initialize KafkaProducerConfig using the config contained in a given Flask app"""
        log.info("Initializing Kafka consumer config from Flask current app")
        config = current_app.config
        return cls(config.get('KAFKA_BOOTSTRAP_SERVERS'),
                   config.get('KAFKA_TOPIC_NAME'),
                   config.get('KAFKA_CONSUMER_GROUP_ID'),
                   config.get('KAFKA_API_VERSION'),
                   config.get('KAFKA_SECURITY_PROTOCOL'),
                   config.get('KAFKA_SASL_MECHANISM'),
                   config.get('KAFKA_CONSUMER_OFFSET_RESET'))

    def get_bootstrap_servers(self):
        return self.__bootstrap_servers

    def get_topic_name(self):
        return self.__topic_name

    def get_group_id(self):
        return self.__group_id

    def get_api_version(self):
        return self.__api_version

    def get_security_protocol(self):
        return self.__security_protocol

    def get_offset_reset(self):
        return self.__offset_reset

    def get_sasl_mechanism(self):
        return self.__sasl_mechanism

