from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config_reader import settings


# create engine
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)
# create sessionmaker
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
 

async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)