import pytest
from uuid import UUID, uuid4

from app.models.lesson import Lesson
from app.repositories.local_lesson_repo import LessonRepo


@pytest.fixture()
def lesson_list() -> list[Lesson]:
    return [
        Lesson(id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
                    subject='Math'),
        Lesson(id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                    subject='History'),
        Lesson(id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
                    subject='Biology')
    ]


@pytest.fixture()
def lesson_repo() -> LessonRepo:
    return LessonRepo()


def test_lesson_list(lesson_list: list[Lesson], lesson_repo: LessonRepo):
    assert lesson_repo.get_lessons() == lesson_list


def test_get_lesson_by_id(lesson_list: list[Lesson], lesson_repo: LessonRepo):
    assert lesson_repo.get_lesson_by_id(
        lesson_list[0].id) == lesson_list[0]


def test_get_lesson_by_id_error(lesson_repo: LessonRepo):
    with pytest.raises(KeyError):
        lesson_repo.get_lesson_by_id(uuid4())
