# Intent to make a story, INPROGRESS, COMPLETED, FAILED

## Frontend will send a request to create a story with a name and title, and the backend will create a story with a root node. The root node will have no content, and the options will be an empty array. The frontend will then send requests to add nodes to the story, and the backend will update the story with the new nodes.
## Backend will also handle the logic for determining if a node is a winning ending or not, and will update the story accordingly. The frontend will then display the story to the user, and allow them to make choices that will lead to different endings.


from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class StoryJob(Base):
    __tablename__ = "story_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    story_id = Column(Integer, nullable=True)
    status = Column(String)  # INPROGRESS, COMPLETED, FAILED
    theme = Column(String)  # Theme of the story
    session_id = Column(String)  # Session ID for the story
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    error_message = Column(String, nullable=True)  # Error message if the job failed
    completed_at = Column(DateTime(timezone=True), nullable=True)  # Timestamp when the job was completed
    
    story = relationship("Story", back_populates="jobs")