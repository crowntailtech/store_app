import json
import base64
import boto3
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import mimetypes

MONGO_URI = os.environ["MONGO_URI"]
S3_BUCKET = os.environ["S3_BUCKET"]
s3_client = boto3.client("s3")

client = MongoClient(MONGO_URI)
db = client["CloudStore"]
collection = db["Products"]

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        name = body.get("name")
        price = float(body.get("price"))
        currency = body.get("currency")

        # Insert into MongoDB
        product = {
            "name": name,
            "price": price,
            "currency": currency
        }
        result = collection.insert_one(product)
        product_id = str(result.inserted_id)

        # Upload Base64 image to S3 if provided
        image_base64 = body.get("image_base64")
        image_type = body.get("image_type")  # e.g., image/png

        image_url = None
        if image_base64 and image_type:
            extension = image_type.split("/")[-1]
            image_bytes = base64.b64decode(image_base64)
            image_key = f"products/{product_id}/original.{extension}"

            print(f"Uploading image to: {image_key}")

            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=image_key,
                Body=image_bytes,
                ContentType=image_type
            )

            image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{image_key}"

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "success": True,
                "message": "Product added successfully",
                "product_id": product_id,
                "image_url": image_url
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }