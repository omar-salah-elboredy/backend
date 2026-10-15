from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from src.db.database import Base
from datetime import datetime

class Story(Base):
    __tablename__ = "stories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    story_name: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    session_id: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    nodes = relationship("StoryNode", back_populates="story")
    jobs = relationship("StoryJob", back_populates="story", cascade="all, delete-orphan")  # Ensure that jobs are deleted when the story is deleted

class StoryNode(Base):
    __tablename__ = "story_nodes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    story_id: Mapped[int] = mapped_column(Integer, ForeignKey("stories.id"), index=True)
    content: Mapped[str] = mapped_column(String)
    options = Column(JSON)  # Store options as a JSON array
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_root: Mapped[bool] = mapped_column(Boolean, default=False)
    is_ending: Mapped[bool] = mapped_column(Boolean, default=False)
    is_winning_ending: Mapped[bool] = mapped_column(Boolean, default=False)

    story = relationship("Story", back_populates="nodes")