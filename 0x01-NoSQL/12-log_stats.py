#!/usr/bin/env python3
'''Provide some stats about Nginx logs stored in mongoDB'''

if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient("localhost", 27017)
    db = client["logs"]
    collection = db["nginx"]
    print("{} logs".format(collection.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print("\tmethod {}: {}".format(
            method,
            collection.count_documents({"method": method})
        ))

    print("{} status check".format(
        collection.count_documents({'method': 'GET', 'path': '/status'})
    ))
