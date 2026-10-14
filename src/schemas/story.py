# Database schemas to store story data in the database. These schemas define the structure of the data and how it will be stored in the database.
# in order to allow for easy serialization and deserialization of the data when interacting with the database.

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

# pydantic allows validation and serialization of data, making it easier to work with data in a structured way.
# BaseModel is a base class for creating data models that can be used to validate and serialize data.

class StoryOptionsSchema(BaseModel):
    option_text: str
    next_node_id: Optional[int] = None  # ID of the next node if this option is chosen

class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False

class CompleteStoryNodeResponse(StoryNodeBase):
    id: int
    options: List[StoryOptionsSchema] = []  # List of options for the node
    story_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # From attributes allows the model to be created from ORM objects, making it easier to work with database models.


class StoryBase(BaseModel):
    story_name: str
    title: str
    session_id: Optional[str] = None  # Session ID for the story, can be None if not provided

class CreateStoryRequest(BaseModel):
    theme: str  # Theme of the story

class CompleteStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse  # The root node of the story
    all_nodes: Dict[int, CompleteStoryNodeResponse] = {}  # Dictionary of all nodes in the story

    class Config:
        from_attributes = True  # From attributes allows the model to be created from ORM objects, making it easier to work with database models.