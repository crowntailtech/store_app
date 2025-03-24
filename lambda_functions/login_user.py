import json
import os
import hashlib
from pymongo import MongoClient

# Setup MongoDB connection
MONGO_URI = os.environ["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["CloudStore"]
collection = db["Users"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    try:
        # Fix for CORS check (works with API Gateway)
        if event.get("httpMethod", "") == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"message": "CORS preflight passed"})
            }

        # Parse request body
        body = json.loads(event["body"])
        email = body.get("email")
        password = body.get("password")

        if not email or not password:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "Email and password are required"})
            }

        user = collection.find_one({"email": email})
        if not user:
            return {
                "statusCode": 404,
                "headers": headers,
                "body": json.dumps({"error": "User not found"})
            }

        if user["password"] != hash_password(password):
            return {
                "statusCode": 401,
                "headers": headers,
                "body": json.dumps({"error": "Invalid password"})
            }

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "success": True,
                "message": "Login successful",
                "user": {
                    "name": user["name"],
                    "email": user["email"]
                }
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
