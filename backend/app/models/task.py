from datetime import datetime
from uuid import UUID
from typing import Optional


class Task:
    """Domain model representing a task entity"""

    def __init__(
        self,
        id: UUID,
        title: str,
        description: Optional[str],
        category: str,
        estimated_time: Optional[int],
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.estimated_time = estimated_time
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "estimated_time": self.estimated_time,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
