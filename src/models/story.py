from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.database import Base

class Story(Base):
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    story_name = Column(String)
    title = Column(String)
    session_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    nodes = relationship("StoryNode", back_populates="story")
    jobs = relationship("StoryJob", back_populates="story", cascade="all, delete-orphan")  # Ensure that jobs are deleted when the story is deleted

class StoryNode(Base):
    __tablename__ = "story_nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
    content = Column(String)
    options = Column(JSON)  # Store options as a JSON array
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning_ending = Column(Boolean, default=False)

    story = relationship("Story", back_populates="nodes")