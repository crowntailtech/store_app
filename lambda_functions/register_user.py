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
    try:
        body = json.loads(event["body"])

        name = body.get("name")
        email = body.get("email")
        password = body.get("password")

        if not name or not email or not password:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "All fields are required"})
            }

        # Check if user exists
        if collection.find_one({"email": email}):
            return {
                "statusCode": 409,
                "body": json.dumps({"error": "User already exists"})
            }

        # Hash the password using SHA-256
        hashed_password = hash_password(password)

        # Store user
        user = {
            "name": name,
            "email": email,
            "password": hashed_password
        }
        collection.insert_one(user)

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "User registered successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
