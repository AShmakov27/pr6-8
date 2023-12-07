from uuid import UUID

from app.models.lesson import Lesson


lessons: list[Lesson] = [
    Lesson(id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
                subject='Math'),
    Lesson(id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
                subject='History'),
    Lesson(id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
                subject='Biology')
]

class LessonRepo():
    def get_lessons(self) -> list[Lesson]:
        return lessons

    def get_lesson_by_id(self, id: UUID) -> Lesson:
        for l in lessons:
            if l.id == id:
                return l

        raise KeyError
