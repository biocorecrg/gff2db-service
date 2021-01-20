#!/usr/bin/env bash

DB=${1:-gff}
USER=${2:-admin}
PASSWD=${3:-mypassword}
HOST=${4:-localhost}
PORT=${5:-5984}

curl -X PUT http://$USER:$PASSWD@$HOST:$PORT/$DB

curl -X PUT -d @auth.json http://$USER:$PASSWD@$HOST:$PORT/$DB/_design/_auth

curl -X PUT -d @list.json http://$USER:$PASSWD@$HOST:$PORT/$DB/_design/list

curl -X PUT -d @search.json http://$USER:$PASSWD@$HOST:$PORT/$DB/_design/search

curl -X PUT -d @coords.json http://$USER:$PASSWD@$HOST:$PORT/$DB/_design/coords
