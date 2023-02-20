import logging
import json
from config.embeddings_processor_config import EmbeddingsProcessorConfig

from sentence_transformers import SentenceTransformer
from pymilvus import Collection
from kafka import KafkaConsumer
from prometheus_client import Counter

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

__model = SentenceTransformer
__milvus_collection = Collection

__consumed_metric = Counter('events_consumed', 'Events consumed')
__embeddings_metric = Counter('embeddings', 'Events processed')


def init(milvus_collection: Collection, consumer: KafkaConsumer, processor_config: EmbeddingsProcessorConfig):
    global __model, __milvus_collection, __consumed_metric
    __model = SentenceTransformer(processor_config.get_model())
    __milvus_collection = milvus_collection
    batch_size = processor_config.get_batch_size()

    events = []

    for message in consumer:
        log.debug("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))
        events.append(json.loads(message.value))
        __consumed_metric.inc(1)
        if len(events) >= batch_size:
            __process_batch(events)
            events = []


def __process_batch(events):
    global __embeddings_metric
    sentences = [event["body"] for event in events]

    embeddings = __model.encode(sentences)

    data = [
        [event["poi_id"] for event in events],
        [event["item_id"] for event in events],
        [int(event["segment"]) for event in events],
        [em for em in embeddings]
    ]

    __milvus_collection.insert(data)
    __embeddings_metric.inc(len(events))

    log.info("Insert finished for {f_events_size} events".format(f_events_size=len(events)))
