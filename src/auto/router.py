from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form

from src.auth.db import User
from src.auth.manager import fastapi_users
from src.auto.db_methods import DBController
from src.auto.schemas import AutoResponseSchema, DeletedSchema

router = APIRouter(
    prefix="/auto",
    tags=["auto"]
)

current_user = fastapi_users.current_user()
db_controller = DBController()


@router.post("/create", response_model=AutoResponseSchema)
async def create_auto(
        model: str = Form(...),
        car_make: str = Form(...),
        year: int = Form(...),
        gis_number: str = Form(...),
        file: UploadFile = File(...),
        user: User = Depends(current_user)
):
    allowed_content_types = ["image/png", "image/jpeg", "image"]
    if file.content_type not in allowed_content_types:
        raise HTTPException(status_code=405, detail="Unsupported file type")

    payload = {
        'creator': user.id,
        'model': model,
        'car_make': car_make,
        'year': year,
        'gis_number': gis_number,
        'photo': await file.read()
    }

    auto = await db_controller.create_auto(payload)
    return {
        'id': auto.id,
        'creator': auto.creator,
        'model': auto.model,
        'car_make': auto.car_make,
        'year': auto.year,
        'gis_number': auto.gis_number,
        'photo': str(auto.photo)
    }


@router.get("/all", response_model=list[AutoResponseSchema])
async def all_auto():
    return await db_controller.get_autos()


@router.get("/{auto_id}", response_model=AutoResponseSchema)
async def get_auto(auto_id: UUID):
    res = await db_controller.get_auto(auto_id)

    if not res:
        raise HTTPException(status_code=404, detail="Not found")

    return res


@router.delete("/{auto_id}", response_model=DeletedSchema)
async def delete_auto(auto_id: UUID, user: User = Depends(current_user)):
    return await db_controller.delete_auto(auto_id)


@router.put("/{auto_id}", response_model=AutoResponseSchema)
async def update_auto(
        auto_id: UUID,
        model: str = Form(...),
        car_make: str = Form(...),
        year: int = Form(...),
        gis_number: str = Form(...),
        file: UploadFile = File(...),
        user: User = Depends(current_user)
):
    payload = {
        'creator': user.id,
        'model': model,
        'car_make': car_make,
        'year': year,
        'gis_number': gis_number,
        'photo': await file.read(),
    }
    res = await db_controller.update_auto(auto_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Not found")

    return res
