from fastapi import FastAPI
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from .database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await engine.dispose()
