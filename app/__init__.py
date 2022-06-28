import os
import json
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util
from fastapi.responses import RedirectResponse

load_dotenv()
pw = os.getenv("mongo_password")
client = MongoClient(
    f"mongodb+srv://jiechenmc:{pw}@freecluster.tqyba.mongodb.net/?retryWrites=true&w=majority"
)
db = client.get_database(os.getenv("mongo_database"))
collection = db.get_collection(os.getenv("mongo_collection"))

app = FastAPI()


def parse_json(data):
    return json.loads(json_util.dumps(data))


def find(collection: MongoClient, field: str, q: str) -> list:
    return parse_json(
        collection.find({field: {
            "$regex": q,
            "$options": "i"
        }}, {"_id": False}))


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.get("/api/section/")
async def section(section: str):
    return find(collection, "Section", section)


@app.get("/api/course/")
async def course(course: str):
    return find(collection, "Course Title", course)


@app.get("/api/instructor/")
async def instructor(name: str):
    return find(collection, "Instructors", name)


@app.get("/api/term/")
async def term(term: str):
    return find(collection, "Term", term)