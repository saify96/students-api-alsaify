from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator


def enum_to_string(cls) -> str:
    return ', '.join([f'{e.name}' for e in cls])


class Gender(Enum):
    male = 'male'
    female = 'female'


class PostStudent(BaseModel):
    first_name: str = Field(example='first name')
    middle_name: Optional[str] = Field(example='middle name')
    last_name: str = Field(example='last name')
    major: str = Field(example='the major')
    gender: Gender

    @validator('gender')
    def validate_gender(cls, value: str):
        try:
            value = Gender(value)
        except ValueError:
            ValueError('This gender is not available')
        return value


class PatchStudent(BaseModel):
    first_name: Optional[str] = Field(example='first name')
    middle_name: Optional[str] = Field(example='middle name')
    last_name: Optional[str] = Field(example='last name')
    major: Optional[str] = Field(example='the major')
    gender: Optional[Gender]

    @validator('gender')
    def validate_gender(cls, value: str):
        try:
            value = Gender(value)
        except ValueError:
            ValueError('This gender is not available')
        return value


class PutStudent(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    major: str
    gender: str


class StudentResponse(BaseModel):
    id: int = Field(example=1234)
    first_name: Optional[str] = Field(example='first name')
    middle_name: Optional[str] = Field(example='middle name')
    last_name: Optional[str] = Field(example='last name')
    major: Optional[str] = Field(example='the major')
    gender: Optional[str] = Field(example=enum_to_string(Gender))
