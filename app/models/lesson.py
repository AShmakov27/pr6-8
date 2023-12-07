from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Lesson(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    subject: str
