from uuid import UUID

from fastapi import UploadFile, File, Form
from pydantic import BaseModel


class AutoResponseSchema(BaseModel):
    id: UUID
    creator: UUID
    model: str
    photo: str


class DeletedSchema(BaseModel):
    id: UUID


