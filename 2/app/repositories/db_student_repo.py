import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.student import Student as DBStudent
from app.repositories.local_lesson_repo import LessonRepo


class StudentRepo():
    db: Session
    lesson_repo: LessonRepo

    def __init__(self) -> None:
        self.db = next(get_db())
        self.lesson_repo = LessonRepo()

    def _map_to_model(self, student: DBStudent) -> Student:
        result = Student.from_orm(student)
        if student.lesson_id != None:
            result.lesson_id = self.lesson_repo.get_lesson_by_id(
                student.lesson_id)

        return result

    def _map_to_schema(self, student: Student) -> DBStudent:
        data = dict(student)
        data.pop('lesson', None)
        data['lesson_id'] = student.lesson_id if student.lesson_id else None
        result = DBStudent(**data)

        return result

    def get_students(self) -> list[Student]:
        students = []
        for s in self.db.query(DBStudent).all():
            students.append(self._map_to_model(s))
        return students

    def get_student_by_id(self, id: UUID) -> Student:
        student = self.db \
            .query(DBStudent) \
            .filter(DBStudent.id == id) \
            .first()

        if student == None:
            raise KeyError
        return self._map_to_model(student)

    def create_student(self, student: Student) -> Student:
        try:
            db_student = self._map_to_schema(student)
            self.db.add(db_student)
            self.db.commit()
            self.db.refresh(db_student)
            return self._map_to_model(db_student)
        except:
            traceback.print_exc()
            raise KeyError

    def set_mark(self, student: Student) -> Student:
        db_student = self.db.query(DBStudent).filter(
            DBStudent.id == student.id).first()
        db_student.mark = student.mark
        self.db.commit()
        return self._map_to_model(db_student)

    def set_lesson(self, student: Student) -> Student:
        db_student = self.db.query(DBStudent).filter(
            DBStudent.id == student.id).first()
        db_student.lesson_id = student.lesson_id
        self.db.commit()
        return self._map_to_model(db_student)
