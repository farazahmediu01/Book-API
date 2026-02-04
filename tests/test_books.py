import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel

from app.main import app
from app.core.database import engine


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_create_book(client: AsyncClient):
    book_data = {
        "title": "Test Book",
        "publisher": "Test Publisher",
        "publication_date": "2024-01-01",
        "page_count": 200,
        "language": "English",
    }
    response = await client.post("/books/", json=book_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == book_data["title"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_books(client: AsyncClient):
    response = await client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
