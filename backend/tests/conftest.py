import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from uuid import uuid4


@pytest.fixture
def mock_db_connection():
    """Fixture providing mocked database connection"""
    connection = AsyncMock()
    return connection


@pytest.fixture
def sample_task_data():
    """Fixture providing sample task data"""
    return {
        "id": uuid4(),
        "title": "Complete project report",
        "description": "Write the quarterly project report",
        "category": "work",
        "estimated_time": 120,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


@pytest.fixture
def sample_task_row(sample_task_data):
    """Fixture providing sample database row"""
    row = MagicMock()
    for key, value in sample_task_data.items():
        row.__getitem__.return_value = value
        setattr(row, key, value)
        row.__getitem__.side_effect = lambda k: sample_task_data.get(k)
    return row
