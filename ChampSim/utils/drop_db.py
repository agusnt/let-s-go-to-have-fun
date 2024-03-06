#!/usr/bin/env python3

'''
Drop the collection of the given database

Arguments:
    @1 -> JSON with the database information

@Author: Navarro-Torres, Agustin 
@Email: agustin.navarro@um.es, agusnavarro11@gmail.com
'''

import sys
import json 

from pymongo import MongoClient

##############################################################################
# Main
##############################################################################
if __name__ == "__main__":
    info = json.load(open(sys.argv[1]))
    client = MongoClient(info['connect'])
    print("Connected to DB")
    db = client[info['db']] # Connect to DB
    # Check if collection exists
    collection = db[info['collection']] # Connect to collection
    if info['collection'] in db.list_collection_names(): 
        print("Erase collection to avoid future duplicated issues")
        collection.drop() # Remove collection that already exists
    client.close()
