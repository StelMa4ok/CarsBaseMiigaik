import sqlite3
from pprint import pprint

from sqlalchemy import MetaData

from config import engine


def create_db(db_path: str):
    # Попытка соединения с базой данных, которое приведет к ее созданию, если она еще не существует
    conn = sqlite3.connect(db_path)
    conn.close()
    print(f'Database created: {db_path}')


async def create_tables(*metadata: MetaData):
    print('Creating tables...')
    async with engine.begin() as conn:
        for data in metadata:
            pprint(data.tables)
            await conn.run_sync(data.create_all)
