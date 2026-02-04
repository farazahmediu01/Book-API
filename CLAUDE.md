# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI async CRUD API for book management using SQLModel and async SQLite.

## Commands

```bash
# Install dependencies
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Run the application
uvicorn app.main:app --reload

# Run tests
pytest

# Docker build and run
docker build -t book-api .
docker run -p 8000:8000 book-api
```

## Architecture

```
app/
├── main.py           # FastAPI app entry point
├── core/             # Configuration, database, lifecycle
├── models/           # SQLModel ORM models (database tables)
├── schemas/          # Pydantic request/response schemas
├── routers/          # API route handlers (thin layer)
└── services/         # Business logic
```

**Data flow:** Router → Service → Model

- **models/** - SQLModel classes with `table=True` for ORM
- **schemas/** - Pure Pydantic models for API validation
- **services/** - Contains business logic, receives session from router
- **routers/** - Validates input, calls service, returns response
