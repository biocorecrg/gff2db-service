# Setting up CouchDB server

docker run --restart=unless-stopped --net=couchnet -d -p 5984:5984 -v $(pwd)/data:/opt/couchdb/data -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=mypassword --name couchdb3-gff ibmcom/couchdb3

Example with Gencode:

```
wget -c -t0 ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_36/gencode.v36.annotation.gff3.gz

bash prepareDB.sh /home/toniher/Documents/biocouch.json


```

