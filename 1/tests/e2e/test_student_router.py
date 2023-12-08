import time
import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

from app.models.student import Student, Statuses


time.sleep(5)
base_url = 'http://localhost:8080/api'


@pytest.fixture(scope='session')
def first_student_data() -> tuple[UUID, str]:
    return (uuid4(), 'test')


@pytest.fixture(scope='session')
def second_student_data() -> tuple[UUID, str]:
    return (uuid4(), 'test_2')


def test_add_student_first_success(
    first_student_data: tuple[UUID, str]
) -> None:
    id, FIO = first_student_data
    student = Student.model_validate(requests.post(f'{base_url}/student/add', json={
        'id': id.hex,
        'FIO': FIO
    }).json())
    assert student.id == id
    assert student.status == Statuses.ABSENT
    assert student.FIO == FIO


def test_add_student_first_repeat_error(
    first_student_data: tuple[UUID, str]
) -> None:
    id, FIO = first_student_data
    result = requests.post(f'{base_url}/student/add', json={
        'id': id.hex,
        'FIO': FIO
    })

    assert result.status_code == 400


def test_attend_student_not_found() -> None:
    result = requests.post(f'{base_url}/student/{uuid4()}/attend')

    assert result.status_code == 404


def test_add_student_second_success(
    second_student_data: tuple[UUID, str]
) -> None:
    id, FIO = second_student_data
    student = Student.model_validate(requests.post(f'{base_url}/student/add', json={
        'id': id.hex,
        'FIO': FIO
    }).json())
    assert student.id == id
    assert student.status == Statuses.ABSENT
    assert student.FIO == FIO


def test_set_lesson_student_not_found() -> None:
    result = requests.post(
        f'{base_url}/student/{uuid4()}/appoint', json={'lesson_id': uuid4().hex})

    assert result.status_code == 404


def test_set_lesson_lesson_not_found(
    first_student_data: tuple[UUID, str]
) -> None:
    id = first_student_data[0]
    result = requests.post(
        f'{base_url}/student/{id}/appoint', json={'lesson_id': uuid4().hex})

    assert result.status_code == 400


def test_set_lesson_status_error(
    first_student_data: tuple[UUID, str]
) -> None:
    id = first_student_data[0]
    result = requests.post(f'{base_url}/student/{id}/appoint',
                           json={'lesson_id': '45309954-8e3c-4635-8066-b342f634252c'})

    assert result.status_code == 400


def test_attend_student_success(
    second_student_data: tuple[UUID, str]
) -> None:
    id, FIO = second_student_data
    student = Student.model_validate_json(requests.post(
        f'{base_url}/student/{id}/attend').text)
    assert student.id == id
    assert student.status == Statuses.ATTEND
    assert student.FIO == FIO


def test_set_lesson_success(
    second_student_data: tuple[UUID, str]
) -> None:
    id, FIO = second_student_data
    student = Student.model_validate_json(requests.post(f'{base_url}/student/{id}/appoint',
                                                          json={'lesson_id': '45309954-8e3c-4635-8066-b342f634252c'}).text)

    assert student.id == id
    assert student.status == Statuses.ATTEND
    assert student.FIO == FIO
