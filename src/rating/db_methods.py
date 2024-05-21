import uuid
from typing import Any, Dict
from uuid import UUID

from config import async_session_maker
from src.rating.models import RatingModel

from sqlalchemy import delete, select, update


class DBController:
    def __init__(self):
        self.session = async_session_maker()

    async def create_rating(self, data: dict) -> dict[str, Any]:
        rating = RatingModel(**data)
        self.session.add(rating)
        await self.session.commit()
        return {
            'id': rating.id,
            'auto': rating.auto,
            'rating': rating.rating,
            'date': rating.date,
            'comment': rating.comment
        }

    async def get_ratings(self) -> list[dict[str, Any]]:
        res = await self.session.execute(select(RatingModel))
        return [{
            'id': row[0].id,
            'auto': row[0].auto,
            'rating': row[0].rating,
            'date': row[0].date,
            'comment': row[0].comment
        } for row in res.fetchall()]

    async def get_rating(self, rating_id: uuid.UUID) -> dict[str, Any]:
        res = await self.session.execute(select(RatingModel).where(RatingModel.id == rating_id))
        row = res.fetchone()
        if row is None:
            return {}

        return {
            'id': row[0].id,
            'auto': row[0].auto,
            'rating': row[0].rating,
            'date': row[0].date,
            'comment': row[0].comment
        }

    async def delete_rating(self, rating_id: uuid.UUID) -> dict[str, UUID]:
        await self.session.execute(delete(RatingModel).where(RatingModel.id == rating_id))
        await self.session.commit()
        return {'id': rating_id}

    async def update_rating(self, rating_id: uuid.UUID, data: dict[str, Any]):
        await self.session.execute(update(RatingModel).where(RatingModel.id == rating_id).values(**data))
        await self.session.commit()
        res = await self.session.execute(select(RatingModel).where(RatingModel.id == rating_id))
        row = res.fetchone()

        if row is None:
            return {}

        return {
            'id': row[0].id,
            'auto': row[0].auto,
            'rating': row[0].rating,
            'date': row[0].date,
            'comment': row[0].comment
        }
