import pytest
from uuid import uuid4, UUID
from datetime import datetime

from app.services.attendance_service import AttendanceService
from app.models.student import Statuses
from app.repositories.local_student_repo import StudentRepo
from app.repositories.local_lesson_repo import LessonRepo


@pytest.fixture(scope='session')
def attendance_service() -> AttendanceService:
    return AttendanceService(StudentRepo(clear=True))


@pytest.fixture()
def lesson_repo() -> LessonRepo:
    return LessonRepo()


@pytest.fixture(scope='session')
def first_student_data() -> tuple[UUID, str]:
    return (uuid4(), 'test')


@pytest.fixture(scope='session')
def second_student_data() -> tuple[UUID, str]:
    return (uuid4(), 'test_2')


def test_empty_students(attendance_service: AttendanceService) -> None:
    assert attendance_service.get_students() == []


def test_create_first_student(
    first_student_data: tuple[UUID, str],
    attendance_service: AttendanceService
) -> None:
    id, FIO = first_student_data
    student = attendance_service.create_student(id, FIO)
    assert student.id == id
    assert student.FIO == FIO
    assert student.status == Statuses.ABSENT
    assert student.lesson_id == None


def test_create_first_student_repeat(
    first_student_data: tuple[UUID, str],
    attendance_service: AttendanceService
) -> None:
    id, FIO = first_student_data
    with pytest.raises(KeyError):
        attendance_service.create_student(id, FIO)


def test_create_second_student(
    second_student_data: tuple[UUID, str],
    attendance_service: AttendanceService
) -> None:
    id, FIO = second_student_data
    student = attendance_service.create_student(id, FIO)
    assert student.id == id
    assert student.FIO == FIO
    assert student.status == Statuses.ABSENT
    assert student.lesson_id == None


def test_get_students_full(
    first_student_data: tuple[UUID, str],
    second_student_data: tuple[UUID, str],
    attendance_service: AttendanceService
) -> None:
    students = attendance_service.get_students()
    assert len(students) == 2
    assert students[0].id == first_student_data[0]
    assert students[1].id == second_student_data[0]


def test_set_lesson_status_error(
    first_student_data: tuple[UUID, str],
    attendance_service: AttendanceService,
    lesson_repo: LessonRepo
) -> None:
    with pytest.raises(ValueError):
        attendance_service.set_lesson(
            first_student_data[0], lesson_repo.get_lessons()[0].id)


def test_set_lesson_lesson_error(
    attendance_service: AttendanceService,
    lesson_repo: LessonRepo
) -> None:
    with pytest.raises(KeyError):
        attendance_service.set_lesson(
            uuid4(), lesson_repo.get_lessons()[0].id)


def test_set_lesson_lesson_error(
    first_student_data: tuple[UUID, str],
    attendance_service: AttendanceService
) -> None:
    with pytest.raises(ValueError):
        attendance_service.set_lesson(first_student_data[0], uuid4())


def test_attend_student_not_found(
    attendance_service: AttendanceService
) -> None:
    with pytest.raises(KeyError):
        attendance_service.attend_student(uuid4())


def test_attend_student(
    first_student_data: tuple[UUID, str],
    attendance_service: AttendanceService
) -> None:
    student = attendance_service.attend_student(first_student_data[0])
    assert student.status == Statuses.ATTEND
    assert student.id == first_student_data[0]


def test_set_lesson(
    first_student_data: tuple[UUID, str],
    attendance_service: AttendanceService,
    lesson_repo: LessonRepo
) -> None:
    lesson = lesson_repo.get_lessons()[0]
    student = attendance_service.set_lesson(
        first_student_data[0], lesson.id)
    assert student.status == Statuses.ATTEND
    assert student.id == first_student_data[0]
    assert student.lesson_id == lesson.id


def test_change_lesson(
    first_student_data: tuple[UUID, str],
    attendance_service: AttendanceService,
    lesson_repo: LessonRepo
) -> None:
    lesson = lesson_repo.get_lessons()[1]
    student = attendance_service.set_lesson(
        first_student_data[0], lesson.id)
    assert student.status == Statuses.ATTEND
    assert student.id == first_student_data[0]
    assert student.lesson_id == lesson.id

