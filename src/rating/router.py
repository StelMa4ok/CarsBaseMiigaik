from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from src.auth.manager import fastapi_users
from src.rating.db_methods import DBController
from src.rating.schemas import RatingCreateSchema, RatingResponseSchema, DeletedSchema

router = APIRouter(
    prefix="/rating",
    tags=["rating"]
)


db_controller = DBController()
current_user = fastapi_users.current_user()


@router.post("/create", response_model=RatingResponseSchema)
async def create_rating(data: RatingCreateSchema):
    if 1 <= data.rating <= 5:
        return await db_controller.create_rating(data.dict())
    raise HTTPException(status_code=400, detail='Rating must be between 1 and 5')


@router.get("/all", response_model=list[RatingResponseSchema])
async def all_rating():
    return await db_controller.get_ratings()


@router.get("/{rating_id}", response_model=RatingResponseSchema)
async def get_rating(rating_id: UUID):
    return await db_controller.get_rating(rating_id)


@router.delete("/{rating_id}", response_model=DeletedSchema)
async def delete_rating(rating_id: UUID):
    return await db_controller.delete_rating(rating_id)


@router.put("/{rating_id}", response_model=RatingResponseSchema)
async def update_rating(rating_id: UUID, data: RatingCreateSchema):
    return await db_controller.update_rating(rating_id, data.dict())
