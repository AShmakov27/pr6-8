import enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from .lesson import Lesson 


class Marks(enum.Enum):
    UNSATISFACTORY   = '2'
    SATISFACTORY   = '3'
    GOOD = '4'
    EXCELLENT = '5'


class Student(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    FIO: str
    mark: Marks | None = None
    lesson_id: UUID | None = None


class CreateStudentRequest(BaseModel):
    id: UUID
    FIO: str
