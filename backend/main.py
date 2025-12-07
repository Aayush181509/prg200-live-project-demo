from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Student Management API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Student(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: int
    course: str
    enrolled_date: Optional[str] = None

# In-memory database
students_db = []
next_id = 1

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Management API"}

@app.get("/students", response_model=List[Student])
def get_students():
    """Get all students"""
    return students_db

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    """Get a specific student by ID"""
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/students", response_model=Student)
def create_student(student: Student):
    """Create a new student"""
    global next_id
    
    # Check if email already exists
    if any(s["email"] == student.email for s in students_db):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    student_dict = student.dict()
    student_dict["id"] = next_id
    student_dict["enrolled_date"] = datetime.now().strftime("%Y-%m-%d")
    
    students_db.append(student_dict)
    next_id += 1
    
    return student_dict

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student):
    """Update an existing student"""
    student_index = next((i for i, s in enumerate(students_db) if s["id"] == student_id), None)
    
    if student_index is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if email already exists for a different student
    if any(s["email"] == student.email and s["id"] != student_id for s in students_db):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    student_dict = student.dict()
    student_dict["id"] = student_id
    student_dict["enrolled_date"] = students_db[student_index]["enrolled_date"]
    
    students_db[student_index] = student_dict
    
    return student_dict

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """Delete a student"""
    student_index = next((i for i, s in enumerate(students_db) if s["id"] == student_id), None)
    
    if student_index is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    deleted_student = students_db.pop(student_index)
    
    return {"message": "Student deleted successfully", "student": deleted_student}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
