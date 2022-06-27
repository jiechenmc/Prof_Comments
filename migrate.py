import pymongo
import os
import json
from dotenv import load_dotenv

load_dotenv()

pw = os.getenv("mongo_password")
client = pymongo.MongoClient(
    f"mongodb+srv://jiechenmc:{pw}@freecluster.tqyba.mongodb.net/?retryWrites=true&w=majority"
)

db = client.get_database(os.getenv("mongo_database"))

collection = db.get_collection(os.getenv("mongo_collection"))

with open("data.json", "r") as f:
    for line in f:
        data = json.loads(line)
        collection.insert_one(data)