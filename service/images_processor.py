import logging
import json
from config.embeddings_processor_config import EmbeddingsProcessorConfig
from minio_utils.minio_client import MinioInstance

from keras_facenet import FaceNet
import numpy as np
from pymilvus import Collection
from kafka import KafkaConsumer
from prometheus_client import Counter


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

__model = FaceNet
__milvus_collection = Collection
__minio_instance = MinioInstance

__consumed_metric = Counter('events_consumed', 'Events consumed')
__embeddings_metric = Counter('embeddings', 'Events processed')


def init(milvus_collection: Collection, minio_client: MinioInstance,
         consumer: KafkaConsumer, processor_config: EmbeddingsProcessorConfig):
    global __model, __milvus_collection, __consumed_metric, __minio_instance
    __milvus_collection = milvus_collection
    __model = FaceNet()
    __minio_instance = minio_client
    batch_size = processor_config.get_batch_size()
    # TODO: Move face_threshold to specific flavour of EmbeddingsProcessorConfig
    face_threshold = 0.95

    events = []

    for message in consumer:
        log.debug("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))
        events.append(json.loads(message.value))
        __consumed_metric.inc(1)
        if len(events) >= batch_size:
            __process_batch(events, face_threshold)
            events = []


def __process_batch(events, face_threshold):
    global __embeddings_metric

    embeddings = []

    for event in events:
        detections = __model.extract(event["s3_path"], threshold=face_threshold)
        result = detections[0]["embedding"]
        normalized_result = result / np.linalg.norm(result)
        embeddings.append(normalized_result)
        __embeddings_metric.inc(1)

    data = [
        [event["poi_id"] for event in events],
        [event["item_id"] for event in events],
        [event["s3_path"] for event in events],
        [em for em in embeddings]
    ]

    __milvus_collection.insert(data)
    __embeddings_metric.inc(len(events))

    log.info("Insert finished for {f_events_size} events".format(f_events_size=len(events)))
