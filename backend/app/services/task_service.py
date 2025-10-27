from typing import List, Optional
from uuid import UUID
from backend.app.repositories.task_repository import TaskRepository
from backend.app.services.categorization.factory import CategorizerFactory
from backend.app.models.task import Task


class TaskService:
    """
    Service layer: orchestrates business logic between routes and repositories.

    Handles task categorization using Factory and Strategy patterns.
    """

    def __init__(self, repository: TaskRepository):
        self.repository = repository
        # Factory pattern: create categorizer instance
        self.categorizer = CategorizerFactory.create_categorizer("keyword")

    async def create_task(
        self, title: str, description: Optional[str], estimated_time: Optional[int]
    ) -> Task:
        """
        Create task with automatic categorization.

        Uses Strategy pattern via Factory to determine category from content.
        """
        category = self.categorizer.categorize(title, description)

        return await self.repository.create(
            title=title,
            description=description,
            category=category,
            estimated_time=estimated_time,
        )

    async def get_task(self, task_id: UUID) -> Optional[Task]:
        """Retrieve single task by ID"""
        return await self.repository.get_by_id(task_id)

    async def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks"""
        return await self.repository.get_all()

    async def update_task(
        self,
        task_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        estimated_time: Optional[int] = None,
    ) -> Optional[Task]:
        """Update task with provided fields"""
        return await self.repository.update(
            task_id=task_id,
            title=title,
            description=description,
            category=category,
            estimated_time=estimated_time,
        )

    async def delete_task(self, task_id: UUID) -> bool:
        """Delete task, returns success status"""
        return await self.repository.delete(task_id)
