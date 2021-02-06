import sys
import os
from cloudant.client import CouchDB
from BCBio import GFF
import json
import pprint
import time

def addQualifiers(doc, qualifiers):

    for qualifier in qualifiers:

        value = qualifiers[qualifier][0]

        if qualifier == "id" or qualifier == "parent" :
            parts = value.split(":")
            if len( parts ) > 1 :
                value = parts[1]

        if value.isdigit():
            value = int( value )
        doc[qualifier.lower()] = value

    return doc

def createDoc( feature, rec, genome ):

    location = feature.location
    start = location.start.position
    end = location.end.position
    strand = location.strand

    final_id = feature.id
    parts_id = feature.id.split(":")
    if len( parts_id ) > 1:
        final_id = parts_id[1]

    doc = {
        "_id": final_id,
        "type": feature.type,
        "chro": rec.id,
        "start": start,
        "end": end,
        "strand": strand,
        "genome": genome
    }

    doc = addQualifiers( doc, feature.qualifiers )

    return doc

def main(argv):

    if len(sys.argv) < 1:
        sys.exit()

    gff_file = sys.argv[1]

    try:
        genome = sys.argv[2]
    except IndexError:
        genome = "hg38"

    try:
        mol = sys.argv[3]
    except IndexError:
        mol = "all"

    try:
        configfile = sys.argv[4]
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

    gff_handle = open(gff_file)

    gene_store = {}

    limit_info = {}
    limit_info["gene"] = dict(gff_type=["gene", "ncRNA_gene", "pseudogene"])
    limit_info["transcript"] = dict(gff_type=[ "lnc_RNA", "mRNA", "miRNA", "ncRNA", "pseudogenic_transcript", "rRNA", "scRNA", "snRNA", "snoRNA", "tRNA", "trasncript"])
    limit_info["all"] = dict(gff_type=["gene", "ncRNA_gene", "pseudogene", "lnc_RNA", "mRNA", "miRNA", "ncRNA", "pseudogenic_transcript", "rRNA", "scRNA", "snRNA", "snoRNA", "tRNA", "transcript"])


    iter = 0
    docbatch = []
    for rec in GFF.parse(gff_handle, target_lines=1000, limit_info=limit_info[mol]):
        features = rec.features

        for feature in features:

            if feature.type not in limit_info[mol]["gff_type"]:
                continue
            doc = createDoc( feature, rec, genome )
            docbatch.append( doc )
            print( doc )
            iter = iter + 1


            subfeatures = feature.sub_features
            for subfeature in subfeatures:

                if subfeature.type not in limit_info[mol]["gff_type"]:
                    continue

                doc = createDoc( subfeature, rec )
                print( doc )
                docbatch.append( doc )
                iter = iter + 1


        if iter > 100 :
            # Process Dock docbatch
            database.bulk_docs( docbatch )
            time.sleep(1)
            docbatch = []
            iter = 0

    gff_handle.close()

    database.bulk_docs( docbatch )
    docbatch = []

if __name__ == "__main__":
	main(sys.argv[1:])
