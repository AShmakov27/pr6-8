from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body

from app.services.attendance_service import AttendanceService
from app.models.student import Student, CreateStudentRequest


student_router = APIRouter(prefix='/student', tags=['Student'])


@student_router.get('/')
def get_students(attendance_service: AttendanceService = Depends(AttendanceService)) -> list[Student]:
    return attendance_service.get_students()

@student_router.post('/add')
def add_delivery(
    student_info: CreateStudentRequest,
    attendance_service: AttendanceService = Depends(AttendanceService)
) -> Student:
    try:
        student = attendance_service.create_student(student_info.id, student_info.FIO)
        return student.dict()
    except KeyError:
        raise HTTPException(400, f'Student with id={student_info.id} already exists')

@student_router.post('/{id}/attend')
def attend_delivery(id: UUID, attendance_service: AttendanceService = Depends(AttendanceService)) -> Student:
    try:
        student = attendance_service.attend_student(id)
        return student.dict()
    except KeyError:
        raise HTTPException(404, f'Student with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Student with id={id} can\'t be attend')

@student_router.post('/{id}/appoint')
def set_lesson(
    id: UUID,
    lesson_id: UUID = Body(embed=True),
    attendance_service: AttendanceService = Depends(AttendanceService)
) -> Student:
    try:
        student = attendance_service.set_lesson(id, lesson_id)
        return student.dict()
    except KeyError:
        raise HTTPException(404, f'Student with id={id} not found')
    except ValueError:
        raise HTTPException(400)
