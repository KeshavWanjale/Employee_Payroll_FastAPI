from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class StudentSchema(BaseModel):
    name: str
    age: int
    major: str

STUDENTS = [
    {"id": 1, "name": "Alice", "age": 20, "major": "Computer Science"},
    {"id": 2, "name": "Bob", "age": 22, "major": "Mathematics"},
    {"id": 3, "name": "Charlie", "age": 19, "major": "Physics"},
    {"id": 4, "name": "David", "age": 21, "major": "Chemistry"},
    {"id": 5, "name": "Eve", "age": 23, "major": "Biology"},
]

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/students")
def get_students():
    return STUDENTS

# path parameter
@app.get("/students/{student_id}")
def get_student_by_id(student_id: int) -> dict:
    for student in STUDENTS:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

# query parameter
@app.get("/students-query")
def get_students(start: int = 0, end: int = 2):
    return STUDENTS[start : end]

@app.post("/add-student")
def add_student(body:StudentSchema):
    _id = STUDENTS[-1]['id']
    data = body.model_dump()
    data['id'] = _id+1
    STUDENTS.append(data)
    return STUDENTS

@app.put("/update-students/{student_id}")
def update_student(student_id: int, body: StudentSchema):
    for student in STUDENTS:
        if student["id"] == student_id:
            student.update(body.model_dump())
            return STUDENTS
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/delete-students/{student_id}")
def delete_student(student_id: int):
    for student in STUDENTS:
        if student["id"] == student_id:
            STUDENTS.pop(student_id-1)
            return STUDENTS
    raise HTTPException(status_code=404, detail="Student not found")