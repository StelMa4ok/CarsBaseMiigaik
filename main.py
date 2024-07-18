import asyncio

import uvicorn
from fastapi import FastAPI

from config import DATABASE_NAME
from src.auth.db import Base as AuthBase
from src.auto.models import Base as AutoBase
from src.rating.models import Base as RatingBase
from src.auth.manager import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.auto.router import router as auto_router
from src.rating.router import router as rating_router
from src.pages.router import router as pages_router
from start_scripts import create_tables, create_db

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(auto_router)
app.include_router(rating_router)
app.include_router(pages_router)

if __name__ == "__main__":
    create_db(DATABASE_NAME)
    asyncio.run(create_tables(
        AuthBase.metadata,
        AutoBase.metadata,
        RatingBase.metadata
    ))

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
