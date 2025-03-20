import json
import boto3
import os

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    """Fetch product by ID and return the S3 image URL."""
    product_id = event["pathParameters"]["id"]
    
    # Construct S3 URL (assuming file format is `{id}.jpg`)
    bucket_name = os.environ["S3_BUCKET"]
    image_key = f"products/{product_id}.jpg"
    image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_key}"
    
    # Check if the file exists in S3
    try:
        s3_client.head_object(Bucket=bucket_name, Key=image_key)
    except Exception:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Product image not found."})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"id": product_id, "image_url": image_url})
    }
