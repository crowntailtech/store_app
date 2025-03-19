import json
import os
import pymongo
from bson.objectid import ObjectId

MONGO_URI = os.environ["MONGO_URI"]
client = pymongo.MongoClient(MONGO_URI)
db = client["CloudStore"]
collection = db["Products"]

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        product = {
            "name": body["name"],
            "price": body["price"],
            "currency": body["currency"]
        }

        result = collection.insert_one(product)

        return {
            "statusCode": 201,
            "body": json.dumps({"success": True, "message": "Product added", "product_id": str(result.inserted_id)})
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
