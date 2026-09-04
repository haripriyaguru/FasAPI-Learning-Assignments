from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import uvicorn

app = FastAPI()


# Database
DATABASE_URL = "sqlite:///./school.db"

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


# Department Model
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    students = relationship(
        "Student",
        back_populates="department"
    )


# Student Model
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

    department_id = Column(
        Integer,
        ForeignKey("departments.id")
    )

    department = relationship(
        "Department",
        back_populates="students"
    )


# Create tables
Base.metadata.create_all(bind=engine)


# Home
@app.get("/")
def home():
    return {"message": "Student Department API"}


# Create Department
@app.post("/departments")
def create_department(name: str):

    db = SessionLocal()

    department = Department(name=name)

    db.add(department)
    db.commit()
    db.refresh(department)
    db.close()

    return department


# Get Departments
@app.get("/departments")
def get_departments():

    db = SessionLocal()

    departments = db.query(Department).all()

    db.close()

    return departments


# Create Student
@app.post("/students")
def create_student(
    name: str,
    age: int,
    department_id: int
):

    db = SessionLocal()

    student = Student(
        name=name,
        age=age,
        department_id=department_id
    )

    db.add(student)
    db.commit()
    db.refresh(student)
    db.close()

    return student


# Get Students
@app.get("/students")
def get_students():

    db = SessionLocal()

    students = db.query(Student).all()

    db.close()

    return students


# Get Students by Department
@app.get("/departments/{department_id}/students")
def get_students_by_department(department_id: int):

    db = SessionLocal()

    students = db.query(Student).filter(
        Student.department_id == department_id
    ).all()

    db.close()

    return students

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )