import os
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
password = os.getenv("mongo_password")
client_str = f"mongodb+srv://jiechenmc:{password}@freecluster.tqyba.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(client_str)
db = client.get_database(os.getenv("mongo_database"))
collection = db.get_collection(os.getenv("mongo_collection"))

tags_metadata = [
    {
        "name":
        "Course Data",
        "description":
        "You can search by Section: **CSE214**, Course Name: **Data Structures**, Instructor Name: **Tripathi**, or by Term: **Spring 2022**",
    },
]

description = """
Professor Comments 🚀

## Course Data

You will be able to:

* **Read comments for classes** 
* **Read grade distribution data for classes**
"""

input_validator = "[^\.\"\']+"

app = FastAPI(title="Professor Comments",
              description=description,
              swagger_ui_parameters={"defaultModelsExpandDepth": -1},
              openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


class Record(BaseModel):
    Section: str
    Term: str
    Course_Title: str | None
    Instructors: str | None
    Comments: str
    Grades: str

    class Config:
        schema_extra = {
            "example": {
                "Section": "CSE214-R01",
                "Term": "Fall 2015",
                "Course Title": "COMPUTER SCIENCE II",
                "Instructors": "Chen-Wei Wang",
                "Comments": "[...]",
                "Grades": "[...]"
            }
        }


def parse_json(data):
    return json_util.loads(json_util.dumps(data))


def find(collection: MongoClient, field: str, q: str) -> list[Record]:
    return parse_json(
        collection.find({field: {
            "$regex": q,
            "$options": "i"
        }}, {"_id": False}))


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/api/section/", response_model=list[Record], tags=["Course Data"])
async def get_by_section(section: str = Query(
    default=...,
    min_length=6,
    max_length=10,
    regex=input_validator,
    description="Search by course number: **CSE214**")):

    return JSONResponse(find(collection, "Section", section))


@app.get("/api/course/", response_model=list[Record], tags=["Course Data"])
async def get_by_course(course: str = Query(
    default=...,
    regex=input_validator,
    description="Search by course name: **Data Structures**")):

    return JSONResponse(find(collection, "Course Title", course))


@app.get("/api/instructor/", response_model=list[Record], tags=["Course Data"])
async def get_by_instructor(name: str = Query(
    default=...,
    regex=input_validator,
    description="Search by instructor name: **Tripathi**")):

    return JSONResponse(find(collection, "Instructors", name))


@app.get("/api/term/", response_model=list[Record], tags=["Course Data"])
async def get_by_term(term: str = Query(
    default=...,
    regex=input_validator,
    description="Search by term: **Spring 2022**")):

    return JSONResponse(find(collection, "Term", term))