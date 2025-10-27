from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.app.config import get_settings
from backend.app.database import DatabaseConnectionPool
from backend.app.routes import tasks_router
import uvicorn


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Manage database connection pool lifecycle"""
    db_pool = DatabaseConnectionPool()
    await db_pool.initialize()
    yield
    await db_pool.close()


app = FastAPI(
    title="Smart Todo List API",
    description="Task management API with automatic categorization",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(tasks_router)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "todo-api", "version": "1.0.0"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
