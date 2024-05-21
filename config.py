from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_NAME = "test.db"
DATABASE_URL = f"sqlite+aiosqlite:///./{DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
