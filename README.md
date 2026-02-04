# Book Management API

A modern, async REST API for managing books built with FastAPI and SQLModel.

## Features

- **Async/Await** - Non-blocking I/O with async SQLite
- **Type Safety** - Full type hints with Pydantic validation
- **Auto Documentation** - Interactive Swagger UI at `/docs`
- **Clean Architecture** - Separated models, schemas, services, and routers
- **Docker Ready** - Containerized with locked dependencies via uv

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| ORM | SQLModel (SQLAlchemy + Pydantic) |
| Database | SQLite (async via aiosqlite) |
| Package Manager | uv |
| Testing | pytest + httpx |

## Project Structure

```
app/
├── main.py           # Application entry point
├── core/
│   ├── config.py     # Environment settings
│   ├── database.py   # Async database engine
│   └── lifespan.py   # Startup/shutdown events
├── models/           # Database models (ORM)
│   └── book.py
├── schemas/          # Request/Response schemas
│   └── book.py
├── services/         # Business logic
│   └── book.py
└── routers/          # API endpoints
    └── books.py
```

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Docker

# Install dependencies
uv sync

# Run the server
uv run fastapi dev app/main.py
uv run uvicorn app.main:app --reload
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/books/` | Create a new book |
| `GET` | `/books/` | List all books (paginated) |
| `GET` | `/books/{id}` | Get a book by ID |
| `PATCH` | `/books/{id}` | Update a book |
| `DELETE` | `/books/{id}` | Delete a book |

### Example Request

```bash
# Create a book
curl -X POST http://localhost:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Pragmatic Programmer",
    "publisher": "Addison-Wesley",
    "publication_date": "2019-09-13",
    "page_count": 352,
    "language": "English"
  }'
```

### Example Response

```json
{
  "id": 1,
  "title": "The Pragmatic Programmer",
  "publisher": "Addison-Wesley",
  "publication_date": "2019-09-13",
  "page_count": 352,
  "language": "English"
}
```

## Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Docker

```bash
# Build the image
docker build -t book-api .

# Run the container
docker run -p 8000:8000 book-api
```

## Testing

```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest
```

## Configuration

Create a `.env` file (see `.env.example`):

```env
APP_NAME=Book Management API
DEBUG=false
DATABASE_URL=sqlite+aiosqlite:///database.db
```

## License

MIT
