import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class EmbeddingsProcessorConfig:

    def __init__(self, model, batch_size):
        """Initializer for Embeddings processor config"""
        self.__model = model
        self.__batch_size = batch_size

    @classmethod
    def from_flask_app(cls, current_app):
        """Initialize KafkaProducerConfig using the config contained in a given Flask app"""
        log.info("Initializing Embeddings processor config from Flask current app")
        config = current_app.config
        return cls(config.get('TRANSFORMER_MODEL'), config.get('EMBEDDING_BATCH_SIZE'))

    def get_model(self):
        return self.__model

    def get_batch_size(self):
        return self.__batch_size
