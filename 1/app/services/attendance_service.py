from uuid import UUID
from fastapi import Depends
from datetime import datetime

from app.models.student import Student, Statuses
from app.repositories.db_student_repo import StudentRepo
from app.repositories.local_lesson_repo import LessonRepo


class AttendanceService():
    student_repo: StudentRepo
    lesson_repo: LessonRepo

    def __init__(self, student_repo: StudentRepo = Depends(StudentRepo)) -> None:
        self.student_repo = student_repo
        self.lesson_repo = LessonRepo()

    def get_students(self) -> list[Student]:
        return self.student_repo.get_students()

    def create_student(self, id: UUID, FIO: str) -> Student:
        student = Student(id=id, FIO=FIO, status=Statuses.ABSENT)
        return self.student_repo.create_student(student)

    def attend_student(self, id: UUID) -> Student:
        student = self.student_repo.get_student_by_id(id)
        if student.status != Statuses.ABSENT:
            raise ValueError

        student.status = Statuses.ATTEND
        return self.student_repo.set_status(student)

    def set_lesson(self, student_id, lesson_id) -> Student:
        student = self.student_repo.get_student_by_id(student_id)

        try:
            lesson = self.lesson_repo.get_lesson_by_id(lesson_id)
        except KeyError:
            raise ValueError

        if student.status != Statuses.ATTEND:
            raise ValueError

        student.lesson_id = lesson.id
        return self.student_repo.set_lesson(student)
        