from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import uvicorn

app = FastAPI()


DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    department = Column(String)


Base.metadata.create_all(bind=engine)


class StudentCreate(BaseModel):
    name: str
    age: int
    department: str


@app.post("/students")
def create_student(student: StudentCreate):

    db = SessionLocal()

    new_student = Student(
        name=student.name,
        age=student.age,
        department=student.department
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    db.close()

    return new_student

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )