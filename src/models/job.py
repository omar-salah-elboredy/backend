# Intent to make a story, INPROGRESS, COMPLETED, FAILED

## Frontend will send a request to create a story with a name and title, and the backend will create a story with a root node. The root node will have no content, and the options will be an empty array. The frontend will then send requests to add nodes to the story, and the backend will update the story with the new nodes.
## Backend will also handle the logic for determining if a node is a winning ending or not, and will update the story accordingly. The frontend will then display the story to the user, and allow them to make choices that will lead to different endings.


from typing import Literal

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.database import Base
from datetime import datetime

JobStatus = Literal['pending', 'processing', 'completed', 'failed']
class StoryJob(Base):
    __tablename__ = "story_jobs"
    
    id = Column(String, primary_key=True, index=True)
    theme: Mapped[str] = mapped_column(String)  # Theme of the story
    status: Mapped[JobStatus] = mapped_column(String)
    session_id: Mapped[str] = mapped_column(String)  # Session ID for the story
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    story = relationship("Story", back_populates="jobs")
    story_id: Mapped[int] = mapped_column(Integer, ForeignKey("stories.id"), nullable=True)  # Link to the story that this job is creating
    error_message: Mapped[str] = mapped_column(String, nullable=True)  # Error message if the job failed
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()) # Timestamp when the job was completed

    def __str__(self):
        return self.id + " " + self.theme