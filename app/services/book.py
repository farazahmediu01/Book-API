from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Book
from app.schemas import BookCreate, BookUpdate


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: BookCreate) -> Book:
        book = Book.model_validate(data)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Book]:
        statement = select(Book).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, book_id: int) -> Book | None:
        return await self.session.get(Book, book_id)

    async def update(self, book: Book, data: BookUpdate) -> Book:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(book, key, value)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete(self, book: Book) -> None:
        await self.session.delete(book)
        await self.session.commit()
