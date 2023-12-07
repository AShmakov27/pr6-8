from uuid import UUID
import requests
from fastapi import APIRouter, Depends, HTTPException, Body

from app.services.mark_service import MarkService
from app.models.student import Student, CreateStudentRequest


student_router = APIRouter(prefix='/student', tags=['Student'])


@student_router.get('/')
def get_students(mark_service: MarkService = Depends(MarkService)) -> list[Student]:
    students = requests.get("http://attendance_service:80/api/student").json()
    for student_info in students:
        mark_service.create_student(student_info["id"], student_info["FIO"])

    return mark_service.get_students()

@student_router.post('/add')
def add_student(
    student_info: CreateStudentRequest,
    mark_service: MarkService = Depends(MarkService)
) -> Student:
    try:
        student = mark_service.create_student(student_info.id, student_info.FIO)
        return student.dict()
    except KeyError:
        raise HTTPException(400, f'Student with id={student_info.id} already exists')

@student_router.post('/{id}/satisfactory')
def satisfactory_student(id: UUID, mark_service: MarkService = Depends(MarkService)) -> Student:
    try:
        students = requests.get("http://attendance_service:80/api/student").json()

        student_info = next((student for student in students if student["id"] == str(id)), None)

        if student_info is None or student_info.get("status") != "attend":
            raise HTTPException(400, f'Student with id={id} is not attend and mark cannot be satisfactory')
        
        student = mark_service.satisfactory_student(id)
        return student.dict()
    except KeyError:
        raise HTTPException(404, f'Student with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Student mark with id={id} can\'t be satisfactory')

@student_router.post('/{id}/good')
def good_student(id: UUID, mark_service: MarkService = Depends(MarkService)) -> Student:
    try:
        students = requests.get("http://attendance_service:80/api/student").json()

        student_info = next((student for student in students if student["id"] == str(id)), None)

        if student_info is None or student_info.get("status") != "attend":
            raise HTTPException(400, f'Student with id={id} is not attend and mark cannot be good')
        
        student = mark_service.good_student(id)
        return student.dict()
    except KeyError:
        raise HTTPException(404, f'Student with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Student mark with id={id} can\'t be good')
    
@student_router.post('/{id}/excellent')
def excellent_student(id: UUID, mark_service: MarkService = Depends(MarkService)) -> Student:
    try:
        students = requests.get("http://attendance_service:80/api/student").json()

        student_info = next((student for student in students if student["id"] == str(id)), None)

        if student_info is None or student_info.get("status") != "attend":
            raise HTTPException(400, f'Student with id={id} is not attend and mark cannot be excellent')
        
        student = mark_service.excellent_student(id)
        return student.dict()
    except KeyError:
        raise HTTPException(404, f'Student with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Student mark with id={id} can\'t be excellent')

@student_router.post('/{id}/appoint')
def set_lesson(
    id: UUID,
    lesson_id: UUID = Body(embed=True),
    mark_service: MarkService = Depends(MarkService)
) -> Student:
    try:
        student = mark_service.set_lesson(id, lesson_id)
        return student.dict()
    except KeyError:
        raise HTTPException(404, f'Student with id={id} not found')
    except ValueError:
        raise HTTPException(400)
