from typing import Optional

from fastapi import FastAPI, HTTPException, status

from models import PatchStudent, PostStudent, PutStudent, StudentResponse
from session import JSONResponse

app = FastAPI()

students = [
    StudentResponse(
        id=1,
        first_name='mohammad',
        last_name='saify',
        major='engineering',
        gender='male',
    ),
    StudentResponse(
        id=2,
        first_name='potato',
        last_name='potato',
        major='potato',
        gender='female',
    )
]


@app.get('/students', response_model=StudentResponse)
def get_students(major: Optional[str] = None,
                 gender: Optional[str] = None) -> JSONResponse:

    filtered_students = None

    if major and gender:
        filtered_students = list(
            filter(lambda std: std.major == major or std.gender == gender,
                   students))
    if major:
        filtered_students = list(
            filter(lambda std: std.major == major, students))
    if gender:
        filtered_students = list(
            filter(lambda std: std.gender == gender, students))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'data': students if not filtered_students else filtered_students
        }
    )


@app.get('/students/{student_id}')
def get_students_by_id(student_id: int) -> JSONResponse:
    # use lambda
    for student in students:
        if student.id == student_id:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'data': student})

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Student with id: {student_id} dose not exist'
    )


@app.post('/students')
def add_student(student: PostStudent) -> JSONResponse:
    try:
        students.append(student)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bad data')

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'data': student})


@app.delete("/students/{student_id}")
def delete_student(student_id: int) -> JSONResponse:
    for std in students:
        if std.id == student_id:
            students.remove(std)
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Student with id: {student_id} dose not exist'
    )


@app.patch("/students/{student_id}")
def update_student_sepcifec_info(student_id: int,
                                 student: PatchStudent) -> JSONResponse:
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
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={'data': student})
    raise HTTPException(
        status_code=404,
        detail=f'Student with id: {student_id} dosen\'t exist'
    )


@app.put("/students/{student_id}")
def update_student_info(student_id: int, student: PutStudent) -> JSONResponse:
    for std in students:
        if std.id == student_id:
            students.remove(std)
            std = {'id': student_id, **student.dict()}
            students.append(std)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'data': std}
            )
    raise HTTPException(
        status_code=404,
        detail=f'Student with id: {student_id} dose not exist'
    )
