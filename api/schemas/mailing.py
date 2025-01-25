from pydantic import BaseModel, ConfigDict
from enum import Enum


class Genders(Enum):
    male = "мужской"
    female = "женский"


class MailingCreateSchema(BaseModel):
    min_age: int | None = None
    max_age: int | None = None
    gender: Genders | None = None
    text: str


class MailingUpdateSchema(BaseModel):
    min_age: int | None = None
    max_age: int | None = None
    gender: Genders | None = None
    text: str | None = None


class MailingSchema(BaseModel):
    id: int
    min_age: int | None = None
    max_age: int | None = None
    gender: Genders | None = None
    text: str

    model_config = ConfigDict(from_attributes=True)

