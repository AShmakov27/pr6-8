import enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from .lesson import Lesson 


class Statuses(enum.Enum):
    ABSENT = 'absent'
    ATTEND = 'attend'


class Student(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    FIO: str
    status: Statuses | None = None
    lesson_id: UUID | None = None


class CreateStudentRequest(BaseModel):
    id: UUID
    FIO: str
