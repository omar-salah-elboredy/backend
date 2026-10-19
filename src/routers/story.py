# We write a router for the story endpoints. This router will handle all the requests related to stories, such as creating, reading, updating, and deleting stories.

import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session
from src.core.story_generate import StoryGenerator
from src.db.database import get_db, SessionLocal

from src.models.job import StoryJob
from src.schemas.job import StoryJobResponse

from src.models.story import Story, StoryNode
from src.schemas.story import CompleteStoryNodeResponse, CompleteStoryResponse, CreateStoryRequest

from src.core.solr_client import search_stories

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
                    response: Response, 
                    db: Session = Depends(get_db), 
                    session_id: str = Depends(get_current_session_id),
                ):
    
    response.set_cookie(key="session_id", value=session_id, httponly=True, secure = True)
    # Create a new story job in the database with status "pending"
    job_id = str(uuid.uuid4())
    
    job = StoryJob(
        id=job_id,
        theme=request.theme,
        status="pending",
        created_at=datetime.now(timezone.utc),
        session_id=session_id
    )
    db.add(job)
    db.commit()

    background_tasks.add_task(generate_story_task, job_id=job_id, theme=request.theme, session_id=session_id)

    return job
 
def generate_story_task(job_id: str, theme: str, session_id: str):
    # This function will be run in the background to generate the story based on the theme.
    db = SessionLocal()

    # Update the job status to "completed"
    try:
        job = db.query(StoryJob).filter(StoryJob.id == job_id).first()
        if job is not None:
            try: 
                job.status = "processing"
                db.commit()
            
                story = StoryGenerator.generate_story(db, session_id, theme)
            
                job.story_id = story.id
                job.status = "completed"
                job.completed_at = datetime.now(timezone.utc)
                db.commit()
            except Exception as e:
                print(f"Error occurred while generating story: {e}")
                job.status = "failed"
                job.completed_at = datetime.now(timezone.utc)
                job.error_message = str(e)
                db.commit()
        else:
            print("Job not found")
        
    except Exception as e:
        print(f"Error occurred while updating job status: {e}")
    finally:
        db.close()

@router.get("/story/{story_id}/complete", response_model=CompleteStoryResponse,
            responses={500: {"description": "Story root node not found!"},
                       404: {"description": "Story not found in our system, please check again."}})
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    # Fetch the story and its nodes from the database
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    complete_story = build_complete_story_tree(db, story)
    return complete_story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found!")
    
    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse.model_validate(node)
        node_dict[node.id] = node_response

    return CompleteStoryResponse(
        id=story.id,
        story_name=story.story_name,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )

@router.get("/search", responses={400: {"description": "Search query cannot be empty."},
                                  500: {"description":"Search cluster temporarily unavailable"}})
def search_all_stories(q: str, db: Session = Depends(get_db)):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
    try:
        search_res = search_stories(q)
        formatted_matches = []

        for doc in search_res:
            formatted_matches.append({
                "node_id": doc.get("id", "").replace("node_", ""), # Cleans 'node_12' down to '12'
                "story_id": doc.get("story_id_i"),
                "snippet": doc.get("content_t"),
                "indexed_at": doc.get("timestamp_dt")
            })
            
        return {
            "query": q,
            "total_matches": len(formatted_matches),
            "results": formatted_matches
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Search cluster temporarily unavailable: {str(e)}"
        )