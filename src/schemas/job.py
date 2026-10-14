from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class StoryJobBase(BaseModel):
    theme: str  # Theme of the story job

class StoryJobResponse(StoryJobBase):
    job_id: str | None = None  # Unique identifier for the job
    status: str  # Status of the job (e.g., pending, completed, failed)
    created_at: datetime  # Timestamp when the job was created
    story_id: Optional[int] = None  # ID of the associated story
    completed_at: Optional[datetime] = None  # Timestamp when the job was completed
    error : Optional[str] = None  # Error message if the job failed

    class Config:
        from_attributes = True  # Enable ORM mode to allow compatibility with SQLAlchemy models

class StoryJobCreate(StoryJobBase):
    pass  # Inherits all fields from StoryJobBase, used for creating new job entries