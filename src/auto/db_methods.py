from typing import Any
from uuid import UUID

from sqlalchemy import select, delete, update, column

from config import async_session_maker
from src.auto.models import AutoModel


class DBController:
    def __init__(self):
        self.session = async_session_maker()

    async def create_auto(self, data: dict) -> AutoModel:
        auto = AutoModel(**data)
        self.session.add(auto)
        await self.session.commit()
        return auto

    async def delete_auto(self, auto_id: UUID) -> dict[str, UUID]:
        await self.session.execute(delete(AutoModel).where(AutoModel.id == auto_id))
        await self.session.commit()
        return {'id': auto_id}

    async def get_autos(self) -> list[dict[str, str | Any]]:
        res = await self.session.execute(select(AutoModel))
        return [{
            'id': auto[0].id,
            'creator': auto[0].creator,
            'model': auto[0].model,
            'photo': str(auto[0].photo)
        } for auto in res.fetchall()]

    async def get_auto(self, auto_id: UUID) -> dict[str, Any]:
        res = await self.session.execute(select(AutoModel).where(AutoModel.id == auto_id))
        row = res.fetchone()
        if row is None:
            return {}

        return {
            'id': row[0].id,
            'creator': row[0].creator,
            'model': row[0].model,
            'photo': str(row[0].photo)
        }

    async def update_auto(self, auto_id: UUID, auto_data: dict) -> dict[str, str | Any]:
        await self.session.execute(update(AutoModel).where(AutoModel.id == auto_id).values(**auto_data).returning(column('id')))
        await self.session.commit()
        res = await self.session.execute(select(AutoModel).where(AutoModel.id == auto_id))
        row = res.fetchone()
        if row is None:
            return {}

        return {
            'id': row[0].id,
            'creator': row[0].creator,
            'model': row[0].model,
            'photo': str(row[0].photo)
        }
