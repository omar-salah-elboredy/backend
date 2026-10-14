# We write a router for the story endpoints. This router will handle all the requests related to stories, such as creating, reading, updating, and deleting stories.

import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session
from src.database import get_db, SessionLocal
from src.models.story import Story, StoryNode
from src.models.job import StoryJob
from src.schemas.story import StoryCreate, StoryResponse, StoryNodeCreate, StoryNodeResponse
from src.schemas.job import StoryJobResponse

router = APIRouter(
    prefix="/stories", # All endpoints in this router will be prefixed with /stories.
    tags=["stories"]
)

def get_current_session_id(session_id: str = Cookie(None)):
    # Nothing to do with authentication, this is just a way to track the user's session. If the session_id cookie is present, we use it. If not, we generate a new one.
    if not session_id:
        # If the session_id cookie is not present, generate a new one.
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(request: CreateStoryRequest, 
                    background_tasks: BackgroundTasks, 
                    db: Session = Depends(get_db), 
                    session_id: str = Depends(get_current_session_id)
                    response: Response):
    
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    # Create a new story job in the database with status "pending"
    job_id = str(uuid.uuid4())
    
    job = 
StoryJob(
        id=job_id,
        theme=request.theme,
        status="pending",
        created_at=datetime.utcnow(),
        session_id=session_id
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(generate_story_task, job_id=job_id, theme=request.theme, session_id=session_id)

    return job
 
def generate_story_task(job_id: str, theme: str, session_id: str):
    # This function will be run in the background to generate the story based on the theme.
    db = SessionLocal()

    # Update the job status to "completed"
    try:
        job = db.query(StoryJob).filter(StoryJob.id == job_id).first()
        if not job:
            print("Job not found")
        try: 
            job.status = "processing"
            db.commit()

            story = {} # TODO: Implement the story generation logic here based on the theme. For now, we will just create a dummy story.

            job.story_id = story.id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            print(f"Error occurred while generating story: {e}")
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error_message = str(e)
            db.commit()
    except Exception as e:
        print(f"Error occurred while updating job status: {e}")
    finally:
        db.close()

@router.get("/story/{job_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    # Fetch the story and its nodes from the database
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()
    
    # TODO: Parse the story and nodes into the CompleteStoryResponse schema and return it. For now, we will just return a dummy response.

    return story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    pass