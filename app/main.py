from fastapi import FastAPI

from app.core import settings, lifespan
from app.routers import books_router

app = FastAPI(
    title=settings.APP_NAME,
    description="A modern async API for managing books using FastAPI and SQLModel.",
    lifespan=lifespan,
)

app.include_router(books_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
