import json
import boto3
import os
from pymongo import MongoClient
from bson import ObjectId

# Initialize AWS S3 client
s3_client = boto3.client("s3")

# Initialize MongoDB client
mongo_uri = os.environ["MONGO_URI"]
client = MongoClient(mongo_uri)
db = client["CloudStore"]
collection = db["Products"]

def lambda_handler(event, context):
    """Fetch product details by ID and return the S3 image URL."""
    product_id = event["pathParameters"]["id"]

    # Fetch product details from MongoDB
    product = collection.find_one({"_id": ObjectId(product_id)})

    if not product:
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Product not found."})
        }

    # Check for image inside products/{product_id}/original.{ext}
    bucket_name = os.environ["S3_BUCKET"]
    image_extensions = ["jpg", "jpeg", "png", "webp"]
    found_image = False

    for ext in image_extensions:
        image_key = f"products/{product_id}/original.{ext}"
        try:
            s3_client.head_object(Bucket=bucket_name, Key=image_key)
            product["image_url"] = f"https://{bucket_name}.s3.amazonaws.com/{image_key}"
            found_image = True
            break
        except Exception:
            continue

    if not found_image:
        product["image_url"] = None

    # Convert ObjectId to string
    product["_id"] = str(product["_id"])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(product)
    }
