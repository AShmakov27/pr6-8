import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.lesson import Lesson


def test_lesson_creation():
    id = uuid4()
    subject = 'name'
    lesson = Lesson(id=id, subject=subject)

    assert dict(lesson) == {'id': id, 'subject': subject}


def test_lesson_subject_required():
    with pytest.raises(ValidationError):
        Lesson(id=id)
