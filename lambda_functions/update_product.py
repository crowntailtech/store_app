import json
import base64
import boto3
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_URI = os.environ["MONGO_URI"]
S3_BUCKET = os.environ["S3_BUCKET"]
s3_client = boto3.client("s3")

client = MongoClient(MONGO_URI)
db = client["CloudStore"]
collection = db["Products"]

def lambda_handler(event, context):
    product_id = event["pathParameters"]["id"]

    try:
        body = json.loads(event["body"])
        name = body.get("name")
        price = float(body.get("price"))
        currency = body.get("currency")

        # Update MongoDB
        collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"name": name, "price": price, "currency": currency}}
        )

        # Upload Base64 image to S3 if provided
        image_base64 = body.get("image_base64")
        image_type = body.get("image_type")  # e.g., "image/png"

        if image_base64 and image_type:
            extension = image_type.split("/")[-1]
            image_bytes = base64.b64decode(image_base64)
            image_key = f"products/{product_id}/original.{extension}"

            # Clean existing folder
            existing = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=f"products/{product_id}/")
            if "Contents" in existing:
                for obj in existing["Contents"]:
                    s3_client.delete_object(Bucket=S3_BUCKET, Key=obj["Key"])

            # Upload new image
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=image_key,
                Body=image_bytes,
                ContentType=image_type
            )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "PUT, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "message": "Product updated successfully.",
                "updated_product": {
                    "_id": product_id,
                    "name": name,
                    "price": price,
                    "currency": currency
                }
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
