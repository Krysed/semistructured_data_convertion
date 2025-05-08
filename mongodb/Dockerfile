FROM mongo:latest

COPY secrets/secrets.json /docker-entrypoint-initdb.d/db_config.json
COPY init_mongo.sh /docker-entrypoint-initdb.d/init_mongo.sh
