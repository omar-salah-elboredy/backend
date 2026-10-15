from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text of the story option.")
    nextNode: Dict[str, Any] = Field(description="The next node in the story tree that this option leads to.")

class StoryNodeLLM(BaseModel):
    content: str = Field(description="The content of the story node.")
    isEnding: bool = Field(description="Indicates whether this node is an ending node.")
    isWinningEnding: bool = Field(description="Indicates whether this node is a winning ending node.")
    options: Optional[List[StoryOptionLLM]] = Field(default=None, description="The list of options available at this story node.")

class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story.")
    rootNode: StoryNodeLLM = Field(description="The root node of the story tree")