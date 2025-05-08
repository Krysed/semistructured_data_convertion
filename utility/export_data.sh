#!/usr/bin/env bash

set -euo pipefail

CONTAINER_NAME="mongodb"
DATABASE="mydatabase"
COLLECTION="mycollection"
OUTPUT_FILE="./tmp/exported_data.json"
FORMATED_JSON="./tmp/formated_json.json"

docker exec "$CONTAINER_NAME" mongoexport \
  --db="${DATABASE}" \
  --collection="${COLLECTION}" \
  --out="/tmp/export.json" \
  --jsonArray

docker cp "${CONTAINER_NAME}:/tmp/export.json" "${OUTPUT_FILE}" | jq '.' "${OUTPUT_FILE}" > "${FORMATED_JSON}"
