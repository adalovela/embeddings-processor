#!/usr/local/bin/zsh

curl -X 'POST' \
  'http://localhost:9091/api/v1/collection' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "collection_name": "emails",
    "schema": {
      "autoID": false,
      "description": "Emails embeddings",
      "fields": [
        {
          "name": "poi_id",
          "description": "PoI ID",
          "is_primary_key": true,
          "autoID": false,
          "data_type": 21,
          "type_params": [
            {
              "key": "max_length",
              "value": "30"
            }
          ]
        },
        {
          "name": "item_id",
          "description": "Item ID",
          "autoID": false,
          "data_type": 21,
          "type_params": [
            {
              "key": "max_length",
              "value": "30"
            }
          ]
        },
        {
          "name": "segment",
          "description": "Number of segment",
          "data_type": 5
        },
        {
          "name": "embedding",
          "description": "embedded vector of email segment",
          "data_type": 101,
          "type_params": [
            {
              "key": "dim",
              "value": "384"
            }
          ]
        }
      ],
      "name": "emails"
    }
  }'