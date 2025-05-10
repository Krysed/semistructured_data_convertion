#!/usr/bin/env bash

set -euo pipefail

CONTAINER_NAME="fastapi-app"
COPY_PATH="$(pwd)/tmp/"
FILE_PATH="/app/data/"
FILE_NAME="generated_users.xml"

docker cp "${CONTAINER_NAME}":"${FILE_PATH}${FILE_NAME}" "${COPY_PATH}"
