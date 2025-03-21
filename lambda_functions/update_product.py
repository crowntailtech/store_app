import json
import boto3
import os

def lambda_handler(event, context):
    """Update product details."""
    product_id = event["pathParameters"]["id"]
    body = json.loads(event["body"])
    
    # Simulated database update
    updated_data = {
        "id": product_id,
        "name": body.get("name"),
        "price": body.get("price"),
        "description": body.get("description")
    }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Product updated successfully.", "updated_product": updated_data})
    }
