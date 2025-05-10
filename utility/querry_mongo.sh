#!/usr/bin/env bash

set -euo pipefail

CONTAINER_NAME="mongodb"
DB_NAME="mydatabase"
COLLECTION="mycollection"
QUERY='{ "currency": "PLN" }'

docker exec -i $CONTAINER_NAME mongosh $DB_NAME --eval "db.getCollection('$COLLECTION').find($QUERY).limit(100).forEach(doc => printjson(doc))"
