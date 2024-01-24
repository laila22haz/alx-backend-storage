#!/usr/bin/env python3
'''
Provide some stats about Nginx logs stored in mongoDB and
the top 10 of the most present IPs
'''

if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
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

    print("IPs:")
    stages = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    top_ips = list(collection.aggregate(stages))
    for ip in top_ips:
        print("\t{}: {}".format(ip["_id"], ip["count"]))
