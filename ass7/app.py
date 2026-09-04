from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Student(BaseModel):
    name: str
    age: int
    department: str


students = []


@app.post("/students")
def create_student(student: Student):
    students.append(student)

    return {
        "message": "Student created",
        "student": student
    }


@app.get("/students")
def get_students():
    return students

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )