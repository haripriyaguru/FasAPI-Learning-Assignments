from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
import uvicorn

app = FastAPI()


# -------------------------
# MongoDB Connection
# -------------------------

client = MongoClient("mongodb://localhost:27017")

database = client["student_database"]

students_collection = database["students"]


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {
        "message": "MongoDB FastAPI API"
    }


# -------------------------
# Create Student
# -------------------------

@app.post("/students")
def create_student(
    name: str,
    age: int,
    department: str
):

    student = {
        "name": name,
        "age": age,
        "department": department
    }

    result = students_collection.insert_one(student)

    return {
        "message": "Student created successfully",
        "id": str(result.inserted_id)
    }


# -------------------------
# Get All Students
# -------------------------

@app.get("/students")
def get_students():

    students = list(
        students_collection.find()
    )

    for student in students:
        student["_id"] = str(student["_id"])

    return students


# -------------------------
# Get Student by ID
# -------------------------

@app.get("/students/{student_id}")
def get_student(student_id: str):

    student = students_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    if student is None:
        return {
            "message": "Student not found"
        }

    student["_id"] = str(student["_id"])

    return student


# -------------------------
# Update Student
# -------------------------

@app.put("/students/{student_id}")
def update_student(
    student_id: str,
    name: str,
    age: int,
    department: str
):

    result = students_collection.update_one(
        {"_id": ObjectId(student_id)},
        {
            "$set": {
                "name": name,
                "age": age,
                "department": department
            }
        }
    )

    if result.matched_count == 0:
        return {
            "message": "Student not found"
        }

    return {
        "message": "Student updated successfully"
    }


# -------------------------
# Delete Student
# -------------------------

@app.delete("/students/{student_id}")
def delete_student(student_id: str):

    result = students_collection.delete_one(
        {"_id": ObjectId(student_id)}
    )

    if result.deleted_count == 0:
        return {
            "message": "Student not found"
        }

    return {
        "message": "Student deleted successfully"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
