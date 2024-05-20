import asyncio

import uvicorn
from fastapi import FastAPI

from config import DATABASE_URL, DATABASE_NAME
from src.auth.db import Base
from src.auth.manager import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate
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

if __name__ == "__main__":
    create_db(DATABASE_NAME)
    asyncio.run(create_tables(Base.metadata))

    uvicorn.run("main:app", host="127.0.0.1", log_level="info")