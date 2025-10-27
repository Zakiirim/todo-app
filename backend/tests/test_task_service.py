import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from backend.app.services.task_service import TaskService
from backend.app.models.task import Task
from datetime import datetime


@pytest.mark.asyncio
async def test_service_create_task_with_categorization():
    """Test Service layer: task creation with auto-categorization"""
    mock_repo = MagicMock()
    mock_task = Task(
        id=uuid4(),
        title="Project meeting",
        description="Discuss Q1 goals",
        category="work",
        estimated_time=60,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_repo.create = AsyncMock(return_value=mock_task)

    service = TaskService(mock_repo)
    task = await service.create_task(
        title="Project meeting", description="Discuss Q1 goals", estimated_time=60
    )

    assert task.category == "work"
    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_service_categorizes_urgent_task():
    """Test Service layer: urgent task categorization"""
    mock_repo = MagicMock()
    mock_task = Task(
        id=uuid4(),
        title="URGENT: Fix production issue",
        description="Critical bug",
        category="urgent",
        estimated_time=30,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_repo.create = AsyncMock(return_value=mock_task)

    service = TaskService(mock_repo)
    await service.create_task(
        title="URGENT: Fix production issue",
        description="Critical bug",
        estimated_time=30,
    )

    # Categorizer should detect 'urgent' keyword
    call_args = mock_repo.create.call_args
    assert call_args[1]["category"] == "urgent"


@pytest.mark.asyncio
async def test_service_get_task():
    """Test Service layer: retrieve single task"""
    mock_repo = MagicMock()
    task_id = uuid4()
    mock_task = Task(
        id=task_id,
        title="Test",
        description=None,
        category="personal",
        estimated_time=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_repo.get_by_id = AsyncMock(return_value=mock_task)

    service = TaskService(mock_repo)
    task = await service.get_task(task_id)

    assert task.id == task_id
    mock_repo.get_by_id.assert_called_once_with(task_id)


@pytest.mark.asyncio
async def test_service_update_task():
    """Test Service layer: task update"""
    mock_repo = MagicMock()
    updated_task = Task(
        id=uuid4(),
        title="Updated",
        description="New description",
        category="work",
        estimated_time=90,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_repo.update = AsyncMock(return_value=updated_task)

    service = TaskService(mock_repo)
    task = await service.update_task(
        task_id=updated_task.id, title="Updated"
    )

    mock_repo.update.assert_called_once()
