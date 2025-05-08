#!/usr/bin/env bash

set -eu

CONFIG_FILE="/docker-entrypoint-initdb.d/db_config.json"
USERNAME=$(jq -r .username "$CONFIG_FILE")
PASSWORD=$(jq -r .password "$CONFIG_FILE")

mongo <<EOF
use admin
db.createUser({
  user: "$USERNAME",
  pwd: "$PASSWORD",
  roles: [ { role: "root", db: "admin" } ]
})
EOF
