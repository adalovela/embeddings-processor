import logging
import sys

import requests
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def create_collection(payload: dict, host: str, port: int):
    endpoint = f"http://{host}:9091/api/v1/collection"
    log.info(f"Proceeding to create a new collection in Milvus:")
    create_request = requests.post(endpoint, json=payload)

    if create_request.status_code == requests.codes.ok:
        log.info(f"Collection {payload['collection_name']} creation request: Response {create_request.status_code}")
    else:
        log.error(f"Error while creating Collection {payload['collection_name']}: Response {create_request.status_code}")
        sys.exit(1)


def create_collection_legacy(name):
    poi_id = FieldSchema(
        name="poi_id",
        dtype=DataType.VARCHAR,
        is_primary=True,
        auto_id=False,
        max_length=30
    )

    item_id = FieldSchema(
        name="item_id",
        dtype=DataType.VARCHAR,
        max_length=30
    )

    segment = FieldSchema(
        name="segment",
        dtype=DataType.INT8
    )

    embedding = FieldSchema(
        name="embedding",
        dtype=DataType.FLOAT_VECTOR,
        dim=384
    )

    schema = CollectionSchema(
        fields=[poi_id, item_id, segment, embedding],
        description="Embeddings for emails indexed by PoI IDs"
    )

    collection_name = name

    return Collection(
        name=collection_name,
        schema=schema,
        using='default',
        shards_num=2
    )

