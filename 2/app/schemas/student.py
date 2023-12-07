from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base
from app.models.student import Marks


class Student(Base):
    __tablename__ = 'students'

    id = Column(UUID(as_uuid=True), primary_key=True)
    FIO = Column(String, nullable=False)
    mark = Column(Enum(Marks), nullable=True)
    lesson_id = Column(UUID(as_uuid=True), nullable=True)
