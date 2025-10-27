import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from backend.app.repositories.task_repository import TaskRepository


@pytest.mark.asyncio
async def test_repository_create_task(mock_db_connection, sample_task_row):
    """Test Repository pattern: task creation"""
    mock_db_connection.fetchrow = AsyncMock(return_value=sample_task_row)

    repository = TaskRepository(mock_db_connection)
    task = await repository.create(
        title="Test task", description="Description", category="work", estimated_time=60
    )

    assert task.title == sample_task_row.title
    mock_db_connection.fetchrow.assert_called_once()


@pytest.mark.asyncio
async def test_repository_get_by_id_found(mock_db_connection, sample_task_row):
    """Test Repository pattern: retrieve existing task"""
    mock_db_connection.fetchrow = AsyncMock(return_value=sample_task_row)

    repository = TaskRepository(mock_db_connection)
    task_id = uuid4()
    task = await repository.get_by_id(task_id)

    assert task is not None
    mock_db_connection.fetchrow.assert_called_once()


@pytest.mark.asyncio
async def test_repository_get_by_id_not_found(mock_db_connection):
    """Test Repository pattern: task not found"""
    mock_db_connection.fetchrow = AsyncMock(return_value=None)

    repository = TaskRepository(mock_db_connection)
    task = await repository.get_by_id(uuid4())

    assert task is None


@pytest.mark.asyncio
async def test_repository_get_all(mock_db_connection, sample_task_row):
    """Test Repository pattern: retrieve all tasks"""
    mock_db_connection.fetch = AsyncMock(
        return_value=[sample_task_row, sample_task_row]
    )

    repository = TaskRepository(mock_db_connection)
    tasks = await repository.get_all()

    assert len(tasks) == 2
    mock_db_connection.fetch.assert_called_once()


@pytest.mark.asyncio
async def test_repository_update_task(mock_db_connection, sample_task_row):
    """Test Repository pattern: task update"""
    mock_db_connection.fetchrow = AsyncMock(return_value=sample_task_row)

    repository = TaskRepository(mock_db_connection)
    updated_task = await repository.update(task_id=uuid4(), title="Updated title")

    assert updated_task is not None
    mock_db_connection.fetchrow.assert_called_once()


@pytest.mark.asyncio
async def test_repository_delete_task_success(mock_db_connection):
    """Test Repository pattern: successful deletion"""
    mock_db_connection.execute = AsyncMock(return_value="DELETE 1")

    repository = TaskRepository(mock_db_connection)
    result = await repository.delete(uuid4())

    assert result is True


@pytest.mark.asyncio
async def test_repository_delete_task_not_found(mock_db_connection):
    """Test Repository pattern: delete non-existent task"""
    mock_db_connection.execute = AsyncMock(return_value="DELETE 0")

    repository = TaskRepository(mock_db_connection)
    result = await repository.delete(uuid4())

    assert result is False
