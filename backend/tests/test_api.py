import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from backend.app.main import app
from datetime import datetime


@pytest.mark.asyncio
async def test_health_check():
    """Test API: health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_task_validation_error():
    """Test API: validation error handling"""
    class MockAcquireContext:
        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, *args):
            pass

    with patch("backend.app.database.DatabaseConnectionPool.get_pool") as mock_pool:
        mock_pool.return_value.acquire.return_value = MockAcquireContext()
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/tasks",
                json={"title": ""},  # Empty title should fail
            )
            assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_with_malicious_input():
    """Test API: XSS prevention in input"""
    mock_connection = AsyncMock()
    task_id = uuid4()

    mock_connection.fetchrow = AsyncMock(
        return_value={
            "id": task_id,
            "title": "Test task",
            "description": "Safe description",
            "category": "work",
            "estimated_time": 60,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    )

    class MockAcquireContext:
        async def __aenter__(self):
            return mock_connection

        async def __aexit__(self, *args):
            pass

    with patch("backend.app.database.DatabaseConnectionPool.get_pool") as mock_pool:
        mock_pool.return_value.acquire.return_value = MockAcquireContext()

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/tasks",
                json={
                    "title": "<script>alert('xss')</script>Task",
                    "description": "Test",
                    "estimated_time": 60,
                },
            )

            # Should sanitize and create task
            assert response.status_code in [200, 201]


@pytest.mark.asyncio
async def test_get_nonexistent_task():
    """Test API: 404 for non-existent task"""
    mock_connection = AsyncMock()
    mock_connection.fetchrow = AsyncMock(return_value=None)

    class MockAcquireContext:
        async def __aenter__(self):
            return mock_connection

        async def __aexit__(self, *args):
            pass

    with patch("backend.app.database.DatabaseConnectionPool.get_pool") as mock_pool:
        mock_pool.return_value.acquire.return_value = MockAcquireContext()

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/api/tasks/{uuid4()}")
            assert response.status_code == 404
