from uuid import UUID
from fastapi import Depends
from datetime import datetime

from app.models.student import Student, Marks
from app.repositories.db_student_repo import StudentRepo
from app.repositories.local_lesson_repo import LessonRepo


class MarkService():
    student_repo: StudentRepo
    lesson_repo: LessonRepo

    def __init__(self, student_repo: StudentRepo = Depends(StudentRepo)) -> None:
        self.student_repo = student_repo
        self.lesson_repo = LessonRepo()

    def get_students(self) -> list[Student]:
        return self.student_repo.get_students()

    def create_student(self, id: UUID, FIO: str) -> Student:
        student = Student(id=id, FIO=FIO, mark=Marks.UNSATISFACTORY  )
        return self.student_repo.create_student(student)

    def satisfactory_student(self, id: UUID) -> Student:
        student = self.student_repo.get_student_by_id(id)
        if student.mark != Marks.UNSATISFACTORY  :
            raise ValueError

        student.mark = Marks.SATISFACTORY  
        return self.student_repo.set_mark(student)
    
    def good_student(self, id: UUID) -> Student:
        student = self.student_repo.get_student_by_id(id)
        if student.mark != Marks.UNSATISFACTORY  :
            raise ValueError

        student.mark = Marks.GOOD  
        return self.student_repo.set_mark(student)
    
    def excellent_student(self, id: UUID) -> Student:
        student = self.student_repo.get_student_by_id(id)
        if student.mark != Marks.UNSATISFACTORY  :
            raise ValueError

        student.mark = Marks.EXCELLENT  
        return self.student_repo.set_mark(student)

    def set_lesson(self, student_id, lesson_id) -> Student:
        student_id = self.student_repo.get_student_by_id(student_id)

        try:
            lesson = self.lesson_repo.get_lesson_by_id(lesson_id)
        except KeyError:
            raise ValueError

        if student_id.mark != Marks.SATISFACTORY  :
            raise ValueError

        student_id.lesson_id = lesson.id
        return self.student_repo.set_lesson(student_id)
        