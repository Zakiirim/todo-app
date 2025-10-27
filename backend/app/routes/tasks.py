from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
import asyncpg

from backend.app.database import get_db_connection
from backend.app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from backend.app.repositories.task_repository import TaskRepository
from backend.app.services.task_service import TaskService


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def get_task_service(
    connection: asyncpg.Connection = Depends(get_db_connection),
) -> TaskService:
    """Dependency injection: provides TaskService with repository"""
    repository = TaskRepository(connection)
    return TaskService(repository)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate, service: TaskService = Depends(get_task_service)
):
    """Create new task with automatic categorization"""
    try:
        created_task = await service.create_task(
            title=task.title,
            description=task.description,
            estimated_time=task.estimated_time,
        )
        return created_task.to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}",
        )


@router.get("", response_model=List[TaskResponse])
async def get_all_tasks(service: TaskService = Depends(get_task_service)):
    """Retrieve all tasks"""
    try:
        tasks = await service.get_all_tasks()
        return [task.to_dict() for task in tasks]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}",
        )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    """Retrieve single task by ID"""
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task.to_dict()


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    """Update existing task"""
    updated_task = await service.update_task(
        task_id=task_id,
        title=task_update.title,
        description=task_update.description,
        category=task_update.category,
        estimated_time=task_update.estimated_time,
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return updated_task.to_dict()


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    """Delete task by ID"""
    deleted = await service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
