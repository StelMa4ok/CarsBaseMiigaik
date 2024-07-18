import base64
import datetime
import uuid
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.auth.db import User, get_user_db
from src.auth.manager import fastapi_users
from src.auto.db_methods import DBController
from src.rating.db_methods import DBController as RatingDBController

router = APIRouter(
    tags=["pages"],
)

templates = Jinja2Templates(directory="templates")

current_user = fastapi_users.current_user(optional=True)
user_manager = fastapi_users.get_user_manager(get_user_db)

db_controller = DBController()
rating_db_controller = RatingDBController()


@router.get("/login")
async def login_page_router(req: Request, user: Optional[User] = Depends(current_user)):
    if user:
        return RedirectResponse("/")
    return templates.TemplateResponse("login.html", {"request": req})


@router.get("/reg")
async def register_page_router(req: Request, user: Optional[User] = Depends(current_user)):
    if user:
        return RedirectResponse("/")
    return templates.TemplateResponse("register.html", {"request": req})


@router.get("/")
async def main_page_router(req: Request,
                           user: Optional[User] = Depends(current_user),
                           manager: SQLAlchemyUserDatabase = Depends(get_user_db)
                           ):

    auto_list = await db_controller.get_autos()
    for auto in auto_list:
        auto['photo'] = base64.b64encode(auto['photo']).decode('utf-8')
        creator = await manager.get(auto['creator'])
        auto['creator'] = creator.email

        ratings = await rating_db_controller.get_ratings_by_auto(auto['id'])
        if len(ratings):
            average_rating = round(sum([el["rating"] for el in ratings])/len(ratings), 2)

            auto["average_rating"] = average_rating

    context = {
        "request": req,
        "auto_list": auto_list,
        "user": user,
    }
    return templates.TemplateResponse("main.html", context)


@router.get("/feedback/{auto_id}")
async def set_feedback_page_router(auto_id: uuid.UUID,
                                   req: Request,
                                   user: Optional[User] = Depends(current_user)
                                   ):
    if not user:
        return RedirectResponse("/login")

    contex = {
        "request": req
    }

    return templates.TemplateResponse("set_feedback.html", contex)


@router.get("/add-car")
async def add_card_page_router(req: Request,
                               user: Optional[User] = Depends(current_user)
                               ):
    if not user:
        return RedirectResponse("/login")

    context = {
        "request": req,
        "current_year": datetime.datetime.now().year
    }

    return templates.TemplateResponse("add_car.html", context)
