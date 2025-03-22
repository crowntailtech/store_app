import json
import boto3
import os
from pymongo import MongoClient

# Initialize AWS S3 client
s3_client = boto3.client("s3")

# Initialize MongoDB client
mongo_uri = os.environ["MONGO_URI"]
client = MongoClient(mongo_uri)
db = client["CloudStore"]  # Update with your database name
collection = db["Products"]  # Update with your collection name

def lambda_handler(event, context):
    """Fetch product details by ID and return the S3 image URL."""
    product_id = event["pathParameters"]["id"]

    # Fetch product details from MongoDB
    product = collection.find_one({"_id": product_id})

    if not product:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Product not found."})
        }

    # Construct S3 URL (assuming file format is `{id}.jpg`)
    bucket_name = os.environ["S3_BUCKET"]
    image_key = f"products/{product_id}.jpg"
    image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_key}"

    # Check if the file exists in S3
    try:
        s3_client.head_object(Bucket=bucket_name, Key=image_key)
        product["image_url"] = image_url  # ✅ Add image URL if exists
    except Exception:
        product["image_url"] = None  # ✅ No image found

    # Convert ObjectId to string for JSON response
    product["_id"] = str(product["_id"])

    return {
        "statusCode": 200,
        "body": json.dumps(product)
    }
