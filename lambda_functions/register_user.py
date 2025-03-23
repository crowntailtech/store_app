# ✅ Lambda function: register_user.py
import json
import os
from pymongo import MongoClient
from passlib.hash import bcrypt

# Environment variables
MONGO_URI = os.environ["MONGO_URI"]

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["CloudStore"]
collection = db["Users"]

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        name = body.get("name")
        email = body.get("email")
        password = body.get("password")

        if not name or not email or not password:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "All fields are required."})
            }

        # Check if user already exists
        if collection.find_one({"email": email}):
            return {
                "statusCode": 409,
                "body": json.dumps({"error": "User already exists with this email."})
            }

        # Hash password
        hashed_password = bcrypt.hash(password)

        # Insert user
        collection.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "User registered successfully."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
