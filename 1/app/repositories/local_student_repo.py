from uuid import UUID

from app.models.student import Student


students: list[Student] = []


class StudentRepo():
    def __init__(self, clear: bool = False) -> None:
        if clear:
            students.clear()

    def get_students(self) -> list[Student]:
        return students

    def get_student_by_id(self, id: UUID) -> Student:
        for s in students:
            if s.id == id:
                return s

        raise KeyError

    def create_student(self, student: Student) -> Student:
        if len([s for s in students if s.id == student.id]) > 0:
            raise KeyError

        students.append(student)
        return student

    def set_status(self, student: Student) -> Student:
        for s in students:
            if s.id == student.id:
                s.status = student.status
                break

        return student

    def set_lesson(self, student: Student) -> Student:
        for s in students:
            if s.id == student.id:
                s.lesson_id = student.lesson_id
                break

        return student
