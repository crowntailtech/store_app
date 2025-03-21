import json
import boto3
import os

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    """Delete product and remove its image from S3."""
    product_id = event["pathParameters"]["id"]
    
    bucket_name = os.environ["S3_BUCKET"]
    image_key = f"products/{product_id}.jpg"

    # Delete from S3
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=image_key)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to delete product image.", "details": str(e)})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Product {product_id} deleted successfully."})
    }
