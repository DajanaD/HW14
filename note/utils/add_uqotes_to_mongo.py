import json
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost")

db = client.hw

with open ("quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)


for quote in quotes:
    author = db.authors.find_one({"fullname": quote["author"]})
    if author:
        db.quotes.insert_one({
            "quote" : quote["author"],
            "author" : ObjectId["_id"],
            "tags" : quote["tags"]
            
        })