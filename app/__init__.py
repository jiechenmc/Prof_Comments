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
        "All queries are relative unless the exact match is entered; **'John' will match 'Carter Johnson', 'John Bailyn', etc...**",
    },
]

description = """
Professor Comments 🚀

## Introduction

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
                "Section":
                "CSE214-R01",
                "Term":
                "Summer 2014",
                "Course Title":
                "COMPUTER SCIENCE II",
                "Instructors":
                "Ahmad Esmaili",
                "Comments":
                "['I found the recitation exercises and discussions to be very helpful in extending our understanding of the material covered in the lectures. I liked the recitations a lot and the TAs were very helpful, not only in explaining the material and recitation exercises but also in responding to student questions through email and office hours.', \"This evaluation is for the TA's, not Professor Esmaili. The course is a recitation, not the actual lecture.\", 'This class was great for teaching me about computer programming and improving my study habits.', 'The concept of basic data structure.', \"This evaluation is for the TA's, not Professor Esmaili.\\nSince the TA's probably change every semester, its kind of difficult to say how the recitation can be improved.\", 'The teaching assistants need to clarify more and elaborate on material in recitation', 'I feel that the recitations are already the best, as they are.', 'I think this course is perfect.']",
                "Grades":
                "[('A', '8'), ('A-', '4'), ('B+', '4'), ('B', '6'), ('B-', '6'), ('C+', '5'), ('C', '4'), ('C-', '4'), ('D+', '3'), ('D', '0'), ('F', '0'), ('P', '0'), ('NC', '0'), ('I', '0'), ('W', '0')]"
            },
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
    max_length=10,
    regex=input_validator,
    description="Search by course number: **CSE214**")):

    return JSONResponse(find(collection, "Section", section))


@app.get("/api/course/", response_model=list[Record], tags=["Course Data"])
async def get_by_course(course: str = Query(
    default=...,
    regex=input_validator,
    description="Search by course name: **COMPUTER SCIENCE II**")):

    return JSONResponse(find(collection, "Course Title", course))


@app.get("/api/instructor/", response_model=list[Record], tags=["Course Data"])
async def get_by_instructor(name: str = Query(
    default=...,
    regex=input_validator,
    description="Search by instructor name: **Ahmad Esmaili**")):

    return JSONResponse(find(collection, "Instructors", name))


@app.get("/api/term/", response_model=list[Record], tags=["Course Data"])
async def get_by_term(term: str = Query(
    default=...,
    regex=input_validator,
    description="Search by term: **Summer 2014**")):

    return JSONResponse(find(collection, "Term", term))