import boto3
import json
import os
import pymongo
from bson.objectid import ObjectId
from requests_toolbelt.multipart import decoder
import base64

# MongoDB setup
MONGO_URI = os.environ["MONGO_URI"]
client = pymongo.MongoClient(MONGO_URI)
db = client["CloudStore"]
collection = db["Products"]

# S3 setup
s3_client = boto3.client("s3")
S3_BUCKET = os.environ["S3_BUCKET"]

def lambda_handler(event, context):
    try:
        # Step 1: Decode the base64-encoded body
        content_type = event["headers"].get("Content-Type") or event["headers"].get("content-type")
        body = base64.b64decode(event["body"])

        # Step 2: Parse multipart data
        multipart_data = decoder.MultipartDecoder(body, content_type)

        # Step 3: Extract parts
        form_data = {}
        image_content = None

        for part in multipart_data.parts:
            content_disposition = part.headers[b'Content-Disposition'].decode()
            if 'filename' in content_disposition:
                # It's the file
                image_content = part.content
            else:
                # It's a regular field
                name = content_disposition.split('name="')[1].split('"')[0]
                form_data[name] = part.text

        # Step 4: Create product
        product = {
            "name": form_data["name"],
            "price": float(form_data["price"]),
            "currency": form_data["currency"]
        }

        result = collection.insert_one(product)
        product_id = str(result.inserted_id)

        image_url = None
        if image_content:
            s3_key = f"products/{product_id}.jpg"
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=image_content,
                ContentType="image/jpeg"
            )
            image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"

        return {
            "statusCode": 201,
            "body": json.dumps({
                "success": True,
                "message": "Product added",
                "product_id": product_id,
                "image_url": image_url
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
