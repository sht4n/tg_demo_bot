import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_table, delete_table
from routers import ROUTERS


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_table()
    print("база очищена")
    await create_table()
    print("база готова к работе")
    yield
    print("выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(*ROUTERS)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        port=6432,
        reload=True,
    )