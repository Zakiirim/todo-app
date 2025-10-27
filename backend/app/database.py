import asyncpg
from typing import Optional
from backend.app.config import get_settings


class DatabaseConnectionPool:
    """Singleton pattern: manages a single database connection pool instance"""

    _instance: Optional["DatabaseConnectionPool"] = None
    _pool: Optional[asyncpg.Pool] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self):
        """Initialize connection pool with configured min/max connections"""
        if self._pool is None:
            settings = get_settings()
            # Extract connection parameters from URL
            url = settings.database_url.replace(
                "postgresql+asyncpg://", "postgresql://"
            )
            self._pool = await asyncpg.create_pool(
                url,
                min_size=settings.db_pool_min_size,
                max_size=settings.db_pool_max_size,
            )

    async def close(self):
        """Close connection pool on application shutdown"""
        if self._pool:
            await self._pool.close()
            self._pool = None

    def get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError(
                "Database pool not initialized. Call initialize() first."
            )
        return self._pool


async def get_db_connection():
    """Dependency injection: provides database connection to FastAPI routes"""
    db_pool = DatabaseConnectionPool()
    pool = db_pool.get_pool()
    async with pool.acquire() as connection:
        yield connection
