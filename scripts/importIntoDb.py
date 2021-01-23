import sys
import os
from cloudant.client import CouchDB
from BCBio import GFF
import json
import pprint

def main(argv):

    if len(sys.argv) < 1:
        sys.exit()

    gff_file = sys.argv[1]

    try:
        configfile = sys.argv[2]
    except IndexError:
    	configfile = "config.json"

    with open(configfile) as json_data_file:
        data = json.load(json_data_file)

    conn = dict()

    if "dbserver" in data:
        if "type" in data["dbserver"]:
        		conn["type"] = data["dbserver"]["type"]
        if "db" in data["dbserver"]:
        		conn["db"] = data["dbserver"]["db"]
        if "host" in data["dbserver"]:
        		conn["host"] = data["dbserver"]["host"]
        if "user" in data["dbserver"]:
        		conn["user"] = data["dbserver"]["user"]
        if "password" in data["dbserver"]:
        		conn["password"] = data["dbserver"]["password"]

    # TODO: Allow other systems such as Elasticsearch in the future

    client = CouchDB(conn["user"], conn["password"], url=conn["host"], connect=True)

    database = client[conn['db']]
    if not database.exists() :
        database = client.create_database(conn['db'])


    # TODO: Process GFF here

    gff_handle = open(gff_file)

    gene_store = {}

    limit_info = dict(gff_type=["gene", "lnc_RNA", "mRNA", "miRNA", "ncRNA",
    "ncRNA_gene", "pseudogene", "pseudogenic_transcript", "rRNA", "scRNA", "snRNA",
    "snoRNA", "tRNA"])

    iter = 0
    for rec in GFF.parse(gff_handle, target_lines=1000, limit_info=limit_info):
        features = rec.features
        for feature in features:
            #print(feature)
            print(feature.id)
            print(feature.type)
            location = feature.location
            start = location.start
            end = location.end
            strand = location.strand
            print( "%d, %d, %d" % ( start, end, strand ) )
            print(feature.qualifiers)
        iter = iter + 1
        if iter > 20 :
            break
    gff_handle.close()

    doc_set = []
    database.bulk_docs( doc_set );

if __name__ == "__main__":
	main(sys.argv[1:])
