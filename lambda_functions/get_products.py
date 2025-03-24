import json
import os
import pymongo
from pymongo.errors import ConnectionFailure
import boto3

# Get environment variables
MONGO_URI = os.environ["MONGO_URI"]
S3_BUCKET = os.environ["S3_BUCKET"]

# Initialize MongoDB Client
try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.admin.command('ping')
    db = client["CloudStore"]
    collection = db["Products"]
    print("✅ Successfully connected to MongoDB!")
except ConnectionFailure:
    print("❌ ERROR: Unable to connect to MongoDB!")

# S3 Client
s3_client = boto3.client("s3")

def lambda_handler(event, context):
    try:
        products = list(collection.find({}, {"_id": 1, "name": 1, "price": 1, "currency": 1}))

        for product in products:
            product_id = str(product["_id"])
            product["_id"] = product_id

            # Check inside folder: products/{product_id}/original.{ext}
            image_extensions = ["jpg", "jpeg", "png", "webp"]
            found = False

            for ext in image_extensions:
                image_key = f"products/{product_id}/original.{ext}"
                try:
                    s3_client.head_object(Bucket=S3_BUCKET, Key=image_key)
                    product["image_url"] = f"https://{S3_BUCKET}.s3.amazonaws.com/{image_key}"
                    found = True
                    break
                except Exception as e:
                    continue

            if not found:
                product["image_url"] = None

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "success": True,
                "products": products
            })
        }

    except ConnectionFailure:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": "Failed to connect to MongoDB. Check your Atlas settings."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": str(e)})
        }
