from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_NAME = "test.db"
DATABASE_URL = f"sqlite+aiosqlite:///./{DATABASE_NAME}"
engine = create_async_engine(DATABASE_URL)
