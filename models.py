from pydantic import BaseModel , field_validator, ValidationError

class Employee(BaseModel):
    first_name :str
    last_name:str
    salary: int
    age : float
    city :str

    @field_validator("first_name", "last_name")
    def validate_name(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError("Firstname and Lastname be at least 3 characters long")
        if not value[0].isupper():
            raise ValueError("First name and Last Name must start with a capital letter")
        return value
