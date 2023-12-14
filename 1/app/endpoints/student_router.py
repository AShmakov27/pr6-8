from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body, Response
from app.services.attendance_service import AttendanceService
from app.models.student import Student, CreateStudentRequest
import prometheus_client


student_router = APIRouter(prefix='/student', tags=['Student'])
metrics_router = APIRouter(tags=['Metrics'])

get_students_count = prometheus_client.Counter(
    "get_students_count",
    "Number of get requests"
)

add_student_count = prometheus_client.Counter(
    "add_student_count",
    "Number of get requests"
)

@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )

@student_router.get('/')
def get_students(attendance_service: AttendanceService = Depends(AttendanceService)) -> list[Student]:
    get_students_count.inc(1)
    return attendance_service.get_students()

@student_router.post('/add')
def add_student(
    student_info: CreateStudentRequest,
    attendance_service: AttendanceService = Depends(AttendanceService)
) -> Student:
    try:
        add_student_count.inc(1)
        student = attendance_service.create_student(student_info.id, student_info.FIO)
        return student.dict()
    except KeyError:
        raise HTTPException(400, f'Student with id={student_info.id} already exists')

@student_router.post('/{id}/attend')
def attend_student(id: UUID, attendance_service: AttendanceService = Depends(AttendanceService)) -> Student:
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
