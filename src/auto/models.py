import uuid

from sqlalchemy import Column, UUID, String, LargeBinary
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class AutoModel(Base):
    __tablename__ = 'autos'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator = Column(UUID(as_uuid=True), nullable=False)
    model = Column(String, nullable=False)
    photo = Column(LargeBinary, nullable=False)
