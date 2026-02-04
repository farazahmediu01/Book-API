from sqlmodel import Field, SQLModel
from datetime import date


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(unique=True)
    publisher: str
    publication_date: date
    page_count: int
    language: str
