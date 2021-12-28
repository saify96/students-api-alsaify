from pydantic import BaseModel
from typing import Optional


class Student(BaseModel):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    major: str
    gender: str


class PartialUpdateStudent(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    major: Optional[str]
    gender: Optional[str]


class UpdateStudent(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    major: str
    gender: str
