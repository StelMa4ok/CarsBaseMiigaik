import datetime
import uuid

from pydantic import BaseModel


class DeletedSchema(BaseModel):
    id: uuid.UUID


class RatingCreateSchema(BaseModel):
    auto: uuid.UUID
    rating: int
    comment: str = ''


class RatingResponseSchema(DeletedSchema, RatingCreateSchema):
    date: datetime.datetime
