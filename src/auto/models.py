import uuid

from sqlalchemy import Column, UUID, String, LargeBinary, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase

from src.auth.db import User


class Base(DeclarativeBase):
    pass


class AutoModel(Base):
    __tablename__ = 'autos'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator = Column(UUID, ForeignKey(User.id, ondelete='CASCADE'))
    model = Column(String, nullable=False)
    car_make = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    gis_number = Column(String, nullable=False)
    photo = Column(LargeBinary, nullable=False)
