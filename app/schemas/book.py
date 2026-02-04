from pydantic import BaseModel
from datetime import date


class BookCreate(BaseModel):
    title: str
    publisher: str
    publication_date: date
    page_count: int
    language: str


class BookRead(BaseModel):
    id: int
    title: str
    publisher: str
    publication_date: date
    page_count: int
    language: str

    model_config = {"from_attributes": True}


class BookUpdate(BaseModel):
    title: str | None = None
    publisher: str | None = None
    publication_date: date | None = None
    page_count: int | None = None
    language: str | None = None
