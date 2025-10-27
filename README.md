# Smart Todo List

A task management app that automatically categorizes your todos. Built with React, FastAPI, and PostgreSQL.

## What it does

Add tasks and they get automatically sorted into work, personal, or urgent categories based on what you write. 
The app analyzes keywords to figure out which category fits best.

## Tech Stack

**Backend**
- FastAPI with async/await
- PostgreSQL + asyncpg
- Alembic for migrations
- pytest for testing

**Frontend**
- React + TypeScript
- Tailwind CSS
- Vite

**Infrastructure**
- Docker Compose for everything
- Includes database, backend, and frontend containers

## How to run

1. Make sure you have Docker and Docker Compose installed

2. Copy the environment files:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Start everything:
```bash
docker-compose up --build
```

4. Open http://localhost:5173

The backend API runs at http://localhost:8000 and you can see the API docs at http://localhost:8000/docs

## Architecture

The backend is organized into layers:
- **Routes** handle HTTP requests
- **Services** contain business logic (including the categorization)
- **Repositories** handle database operations

The frontend is a single-page React app that talks to the backend REST API.

Database migrations run automatically when you start the containers.

## Running tests

```bash
docker-compose exec backend pytest
```

## Useful commands

```bash
# Stop everything
docker-compose down

# Wipe the database and start fresh
docker-compose down -v

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```
