#!/usr/bin/env bash

CONF=${1:-conf.json}


DB=$(jq -r '.dbserver.db' $CONF)
USER=$(jq -r '.dbserver.user' $CONF)
PASSWORD=$(jq -r '.dbserver.password' $CONF)
HOST=$(jq -r '.dbserver.host' $CONF)
hparts=(${HOST//\/\// })

FINALHOST="${hparts[0]}//$USER:$PASSWORD@${hparts[1]}"

echo $FINALHOST
curl -k -X PUT $FINALHOST/$DB

curl -k -X PUT -d @auth.json $FINALHOST/$DB/_design/_auth
curl -k -X PUT -d @list.json $FINALHOST/$DB/_design/list
curl -k -X PUT -d @search.json $FINALHOST/$DB/_design/search
