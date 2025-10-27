from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    estimated_time: Optional[int] = Field(None, ge=0, le=1440)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    category: Optional[str] = Field(None, pattern="^(work|personal|urgent)$")
    estimated_time: Optional[int] = Field(None, ge=0, le=1440)


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    category: str
    estimated_time: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
