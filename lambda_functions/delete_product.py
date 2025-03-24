import json
import boto3
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# Setup
s3_client = boto3.client("s3")
bucket_name = os.environ["S3_BUCKET"]
mongo_uri = os.environ["MONGO_URI"]

client = MongoClient(mongo_uri)
db = client["CloudStore"]
collection = db["Products"]

def lambda_handler(event, context):
    product_id = event["pathParameters"]["id"]

    try:
        # 1. Delete the product from MongoDB
        result = collection.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Product not found in database."})
            }

        # 2. Delete all images from S3 folder: products/{product_id}/
        prefix = f"products/{product_id}/"
        existing = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if "Contents" in existing:
            for obj in existing["Contents"]:
                s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": f"✅ Product {product_id} and associated images deleted successfully."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "❌ Failed to delete product.", "details": str(e)})
        }
