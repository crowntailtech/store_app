import json
import os
import pymongo
from pymongo.errors import ConnectionFailure

# ✅ Get MongoDB Connection String from Environment Variable
MONGO_URI = os.environ["MONGO_URI"]

# ✅ Initialize MongoDB Client (With Timeout)
try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.admin.command('ping')  # ✅ Test Connection
    db = client["CloudStore"]
    collection = db["Products"]
    print("✅ Successfully connected to MongoDB!")
except ConnectionFailure:
    print("❌ ERROR: Unable to connect to MongoDB!")

def lambda_handler(event, context):
    try:
        # ✅ Fetch All Products from MongoDB
        products = list(collection.find({}, {"_id": 1, "name": 1, "price": 1, "currency": 1}))

        # ✅ Convert `_id` to string
        for product in products:
            product["_id"] = str(product["_id"])

        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "products": products})
        }

    except ConnectionFailure:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to connect to MongoDB. Check your Atlas settings."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
