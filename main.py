from typing import Optional
from fastapi import FastAPI, HTTPException
from models import Student, UpdateStudent, PartialUpdateStudent

app = FastAPI()

students = [
    Student(
        id=1,
        first_name='mohammad',
        last_name='saify',
        major='engineering',
        gender='male',
    ),
    Student(
        id=2,
        first_name='potato',
        last_name='potato',
        major='potato',
        gender='female',
    )
]


@app.get('/students')
def get_students(major: Optional[str] = None, gender: Optional[str] = None):
    if major and gender:
        filterd_students = list(
            filter(lambda std: std.major == major or std.gender == gender, students))
        return filterd_students
    if major:
        filterd_students = list(
            filter(lambda std: std.major == major, students))
        return filterd_students
    if gender:
        filterd_students = list(
            filter(lambda std: std.gender == gender, students))
        return filterd_students
    return students


@app.get('/students/{student_id}')
def get_students(student_id: int):
    for std in students:
        if std.id == student_id:
            return std
    raise HTTPException(
        status_code=404,
        detail=f'Student with id: {student_id} dosen\'t exist'
    )


@app.post('/students')
def add_student(student: Student):
    students.append(student)
    return 'Student added successfully'


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for std in students:
        if std.id == student_id:
            students.remove(std)
            return 'Student removed successfully'
    raise HTTPException(
        status_code=404,
        detail=f'Student with id: {student_id} dosen\'t exist'
    )


@app.patch("/students/{student_id}")
def update_student_sepcifec_info(student_id: int, student: PartialUpdateStudent):
    for std in students:
        if std.id == student_id:
            if student.first_name is not None:
                std.first_name = student.first_name
            if student.middle_name is not None:
                std.middle_name = student.middle_name
            if student.last_name is not None:
                std.last_name = student.last_name
            if student.major is not None:
                std.major = student.major
            if student.gender is not None:
                std.gender = student.gender
            return 'Student updated successfully'
    raise HTTPException(
        status_code=404,
        detail=f'Student with id: {student_id} dosen\'t exist'
    )


@app.put("/students/{student_id}")
def update_student_info(student_id: int, student: UpdateStudent):
    for std in students:
        if std.id == student_id:
            students.remove(std)
            std = {'id': student_id, **student.dict()}
            students.append(std)
            return 'Student updated successfully'
    raise HTTPException(
        status_code=404,
        detail=f'Student with id: {student_id} dosen\'t exist'
    )
