from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.session import create_db_tables
from app.api.router import master_router


@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan_handler,)

app.include_router(router=master_router)

