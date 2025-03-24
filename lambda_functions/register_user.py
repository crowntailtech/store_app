import json
import os
import hashlib
from pymongo import MongoClient

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
        
        if event.get("httpMethod", "") == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"message": "CORS check passed"})
            }

        body = json.loads(event["body"])
        name = body.get("name")
        email = body.get("email")
        password = body.get("password")

        if not name or not email or not password:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "All fields are required"})
            }

        if collection.find_one({"email": email}):
            return {
                "statusCode": 409,
                "headers": headers,
                "body": json.dumps({"error": "User already exists"})
            }

        hashed_password = hash_password(password)
        collection.insert_one({"name": name, "email": email, "password": hashed_password})

        return {
            "statusCode": 201,
            "headers": headers,
            "body": json.dumps({"success": True, "message": "User registered successfully"})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": "Internal Server Error", "details": str(e)})
        }
