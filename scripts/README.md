# Setting up CouchDB server

docker run --restart=unless-stopped --net=couchnet -d -p 5984:5984 -v $(pwd)/data:/opt/couchdb/data -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=mypassword --name couchdb3-gff ibmcom/couchdb3


