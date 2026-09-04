from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import uvicorn

app = FastAPI()


# Database Configuration
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


# Student Model
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)


# Create Table
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Home
@app.get("/")
def home():
    return {"message": "Dependency Injection API"}


# Create Student
@app.post("/students")
def create_student(
    name: str,
    age: int,
    db: Session = Depends(get_db)
):

    student = Student(
        name=name,
        age=age
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


# Get All Students
@app.get("/students")
def get_students(
    db: Session = Depends(get_db)
):

    students = db.query(Student).all()

    return students

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )