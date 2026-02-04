from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status

from app.core import session_dependency
from app.schemas import BookRead, BookCreate, BookUpdate
from app.services import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(data: BookCreate, session: session_dependency):
    service = BookService(session)
    book = await service.create(data)
    return book


@router.get("/", response_model=list[BookRead])
async def get_books(
    session: session_dependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    service = BookService(session)
    return await service.get_all(offset, limit)


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, session: session_dependency):
    service = BookService(session)
    book = await service.get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return book


@router.patch("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, data: BookUpdate, session: session_dependency):
    service = BookService(session)
    book = await service.get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return await service.update(book, data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: session_dependency):
    service = BookService(session)
    book = await service.get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    await service.delete(book)
