import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from app.models.lesson import Lesson
from app.models.student import Student, Statuses


@pytest.fixture()
def any_lesson() -> Lesson:
    return Lesson(id=uuid4(), subject='delliveryman')


def test_student_creation(any_lesson: Lesson):
    id = uuid4()
    FIO = 'test'
    status = Statuses.ABSENT
    delivery = Student(id=id, FIO=FIO, status=status, lesson_id=any_lesson)

    assert dict(delivery) == {'id': id, 'FIO': FIO, 'status': status, 'lesson_id': any_lesson}


def test_student_fio_required(any_lesson: Lesson):
    with pytest.raises(ValidationError):
        Student(id=uuid4(), status=Statuses.ATTEND, lesson_id=any_lesson)
