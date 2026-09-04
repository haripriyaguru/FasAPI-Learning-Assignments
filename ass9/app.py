from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()


students = [
    {"id": 1, "name": "Hari"},
    {"id": 2, "name": "Priya"}
]


@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:

        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
