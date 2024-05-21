import datetime
import uuid

from sqlalchemy import Column, UUID, ForeignKey, Integer, DateTime, String, CheckConstraint
from sqlalchemy.orm import DeclarativeBase

from src.auto.models import AutoModel


class Base(DeclarativeBase):
    pass


class RatingModel(Base):
    __tablename__ = 'ratings'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auto = Column(UUID, ForeignKey(AutoModel.id, ondelete='CASCADE'))
    rating = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    comment = Column(String())

    __table_args__ = (
        CheckConstraint('rating >= 1', name='rating_min'),  # Минимальное значение рейтинга
        CheckConstraint('rating <= 5', name='rating_max'),  # Максимальное значение рейтинга
    )
