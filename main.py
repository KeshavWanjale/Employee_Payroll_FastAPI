from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from configurations import collection
from schemas import user_entities
from models import Employee
from bson import ObjectId

app = FastAPI()

class EmployeeResponse(BaseModel):
    status_code: int
    message: str
    data: dict

class EmployeeListResponse(BaseModel):
    status_code: int
    message: str
    data: list[dict]

@app.get("/", response_model=dict[str,str])
def read_root():
    return {"message": "Hello, World!"}

@app.get("/employees", response_model=EmployeeListResponse)
def get_employees():
    data = collection.find()
    employees = user_entities(data)
    return {
        "status_code": status.HTTP_200_OK,
        "message": "Employees retrieved successfully",
        "data": employees
    }

@app.post("/employees", response_model=EmployeeResponse)
def create_employee(emp: Employee):
    try:
        response = collection.insert_one(dict(emp))
        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "Employee created successfully",
            "data": {"id": str(response.inserted_id)}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {e}"
        )

@app.put("/employees/{emp_id}", response_model=EmployeeResponse)
def update_employees(emp_id: str, emp: Employee):
    try:
        id = ObjectId(emp_id)
        update_result = collection.update_one(
            {"_id": id},
            {"$set": dict(emp)}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        return {
            "status_code": status.HTTP_200_OK,
            "message": "Employee details updated successfully",
            "data": {"id": emp_id}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {e}"
        )

@app.delete("/employees/{emp_id}", response_model=EmployeeResponse)
def delete_employee(emp_id: str):
    try:
        id = ObjectId(emp_id)
        delete_result = collection.delete_one({"_id": id})
        
        if delete_result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        return {
            "status_code": status.HTTP_204_NO_CONTENT,
            "message": "Employee deleted successfully",
            "data": {}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {e}"
        )