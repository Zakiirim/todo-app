from typing import List, Optional
from uuid import UUID
import asyncpg
from backend.app.models.task import Task


class TaskRepository:
    """
    Repository pattern: abstracts database operations for Task entities.

    Provides clean interface for data access, hiding SQL implementation details.
    """

    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def create(
        self,
        title: str,
        description: Optional[str],
        category: str,
        estimated_time: Optional[int],
    ) -> Task:
        """Create new task with auto-generated UUID and timestamps"""
        row = await self.connection.fetchrow(
            """
            INSERT INTO tasks (title, description, category, estimated_time)
            VALUES ($1, $2, $3, $4)
            RETURNING id, title, description, category, estimated_time,
                      created_at, updated_at
            """,
            title,
            description,
            category,
            estimated_time,
        )
        return self._row_to_task(row)

    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Retrieve task by UUID"""
        row = await self.connection.fetchrow(
            """
            SELECT id, title, description, category, estimated_time,
                   created_at, updated_at
            FROM tasks
            WHERE id = $1
            """,
            task_id,
        )
        return self._row_to_task(row) if row else None

    async def get_all(self) -> List[Task]:
        """Retrieve all tasks ordered by creation date"""
        rows = await self.connection.fetch(
            """
            SELECT id, title, description, category, estimated_time,
                   created_at, updated_at
            FROM tasks
            ORDER BY created_at DESC
            """
        )
        return [self._row_to_task(row) for row in rows]

    async def update(
        self,
        task_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        estimated_time: Optional[int] = None,
    ) -> Optional[Task]:
        """Update task fields and refresh updated_at timestamp"""
        # Build dynamic update query for provided fields
        updates = []
        values = []
        param_count = 1

        if title is not None:
            updates.append(f"title = ${param_count}")
            values.append(title)
            param_count += 1

        if description is not None:
            updates.append(f"description = ${param_count}")
            values.append(description)
            param_count += 1

        if category is not None:
            updates.append(f"category = ${param_count}")
            values.append(category)
            param_count += 1

        if estimated_time is not None:
            updates.append(f"estimated_time = ${param_count}")
            values.append(estimated_time)
            param_count += 1

        if not updates:
            return await self.get_by_id(task_id)

        updates.append("updated_at = NOW()")
        values.append(task_id)

        query = f"""
            UPDATE tasks
            SET {", ".join(updates)}
            WHERE id = ${param_count}
            RETURNING id, title, description, category, estimated_time,
                      created_at, updated_at
        """

        row = await self.connection.fetchrow(query, *values)
        return self._row_to_task(row) if row else None

    async def delete(self, task_id: UUID) -> bool:
        """Delete task by UUID, returns True if task existed"""
        result = await self.connection.execute(
            "DELETE FROM tasks WHERE id = $1", task_id
        )
        return result == "DELETE 1"

    def _row_to_task(self, row: asyncpg.Record) -> Task:
        """Convert database row to Task domain model"""
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            category=row["category"],
            estimated_time=row["estimated_time"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
