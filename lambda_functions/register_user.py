import json
import os
import bcrypt
from pymongo import MongoClient

# Load environment variables
MONGO_URI = os.environ["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["CloudStore"]
collection = db["Users"]  # Create a separate 'Users' collection

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
                "statusCode": 400,
                "body": json.dumps({"error": "Email already registered."})
            }

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Insert user record
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
            "body": json.dumps({"success": True, "message": "User registered successfully."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
