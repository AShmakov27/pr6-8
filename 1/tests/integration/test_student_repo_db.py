import pytest
from uuid import uuid4

from app.models.student import Student, Statuses
from app.repositories.db_student_repo import StudentRepo
from app.repositories.local_lesson_repo import LessonRepo


@pytest.fixture()
def student_repo() -> StudentRepo:
    repo = StudentRepo()
    return repo


@pytest.fixture(scope='session')
def lesson_repo() -> LessonRepo:
    return LessonRepo()


@pytest.fixture(scope='session')
def first_student() -> Student:
    return Student(id=uuid4(), FIO='test', status=Statuses.ABSENT)


@pytest.fixture(scope='session')
def second_student() -> Student:
    return Student(id=uuid4(), FIO='test2', status=Statuses.ATTEND)


def test_empty_list(student_repo: StudentRepo) -> None:
    assert student_repo.get_deliveries() == []


def test_add_first_student(first_student: Student, student_repo: StudentRepo) -> None:
    assert student_repo.create_student(first_student) == first_student


def test_add_first_student_repeat(first_student: Student, student_repo: StudentRepo) -> None:
    with pytest.raises(KeyError):
        student_repo.create_student(first_student)


def test_get_student_by_id(first_student: Student, student_repo: StudentRepo) -> None:
    assert student_repo.get_student_by_id(
        first_student.id) == first_student


def test_get_student_by_id_error(student_repo: StudentRepo) -> None:
    with pytest.raises(KeyError):
        student_repo.get_student_by_id(uuid4())


def test_add_second_student(first_student: Student, second_student: Student, student_repo: StudentRepo) -> None:
    assert student_repo.create_student(second_student) == second_student
    deliveries = student_repo.get_students()
    assert len(deliveries) == 2
    assert deliveries[0] == first_student
    assert deliveries[1] == second_student


def test_set_status(first_student: Student, student_repo: StudentRepo) -> None:
    first_student.status = Statuses.ABSENT
    assert student_repo.set_status(
        first_student).status == first_student.status

    first_student.status = Statuses.ABSENT
    assert student_repo.set_status(
        first_student).status == first_student.status


def test_set_lesson(first_student: Student, lesson_repo: LessonRepo, student_repo: StudentRepo) -> None:
    first_student.lesson_id = lesson_repo.get_lessons()[0].id
    assert student_repo.set_lesson(
        first_student).lesson_id == lesson_repo.get_lessons()[0].id


def test_change_deliveryman(first_student: Student, lesson_repo: LessonRepo, student_repo: StudentRepo) -> None:
    first_student.deliveryman = lesson_repo.get_lessons()[1].id
    assert student_repo.set_lesson(
        first_student).lesson_id == lesson_repo.get_lessons()[1].id