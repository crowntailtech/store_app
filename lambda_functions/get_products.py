import json
import os
import pymongo

MONGO_URI = os.environ["MONGO_URI"]
client = pymongo.MongoClient(MONGO_URI)
db = client["CloudStore"]
collection = db["Products"]

def lambda_handler(event, context):
    try:
        products = list(collection.find({}, {"_id": 1, "name": 1, "price": 1, "currency": 1}))
        
        for product in products:
            product["_id"] = str(product["_id"])  # Convert ObjectId to string

        return {"statusCode": 200, "body": json.dumps(products)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
