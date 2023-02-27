import logging
import json
from config.embeddings_processor_config import EmbeddingsProcessorConfig
from minio_utils.minio_client import MinioClient

from keras_facenet import FaceNet
import numpy as np
from pymilvus import Collection
from kafka import KafkaConsumer
from prometheus_client import Counter

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

__consumed_metric = Counter('events_consumed', 'Events consumed')
__embeddings_metric = Counter('embeddings', 'Events processed')


class ImagesProcessor:

    def __init__(self, milvus_collection: Collection, minio_client: MinioClient,
                 consumer: KafkaConsumer, processor_config: EmbeddingsProcessorConfig):
        self.__milvus_collection = milvus_collection
        self.__model = FaceNet()
        self.__minio_client = minio_client
        self.__consumer = consumer
        self.__batch_size = processor_config.get_batch_size()
        # TODO: Move face_threshold to specific flavour of EmbeddingsProcessorConfig

    def init(self):
        global __consumed_metric
        face_threshold = 0.95

        events = []

        for message in self.__consumer:
            log.debug("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                     message.offset, message.key,
                                                     message.value))
            events.append(json.loads(message.value))
            __consumed_metric.inc(1)
            if len(events) >= self.__batch_size:
                self.__process_batch(events, face_threshold)
                events = []

    def __process_batch(self, events, face_threshold):
        global __embeddings_metric

        embeddings = []

        for event in events:

            try:
                if 's3_object' not in event:
                    raise KeyError(f"Mandatory key s3_object not present in event {event}")

                s3_img_path = f"{event['s3_object']}"
                image = self.__minio_client.fetch_image(s3_img_path)
                detections = self.__model.extract(image, threshold=face_threshold)
                result = detections[0]["embedding"]
                normalized_result = result / np.linalg.norm(result)
                embeddings.append(normalized_result)
                __embeddings_metric.inc(1)

            except Exception as e:
                log.error(f"Error while retrieving image from minio on event: {event}", e)

        data = [
            [event["poi_id"] for event in events],
            [event["item_id"] for event in events],
            [event["s3_path"] for event in events],
            [em for em in embeddings]
        ]

        self.__milvus_collection.insert(data)
        __embeddings_metric.inc(len(events))

        log.info(f"Insert finished for {len(events)} events")
