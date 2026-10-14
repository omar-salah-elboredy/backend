import uuid
from typing import Optional
from fastapi import APIRouter, Depends, BackgroundTasks, Response, HTTPException, Cookie
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.job import StoryJob
from src.schemas.job import StoryJobResponse

router = APIRouter(
    prefix="/jobs",  # All endpoints in this router will be prefixed with /jobs.
    tags=["jobs"]
)

@router.get(
    "/{job_id}",
    response_model=StoryJobResponse,
    responses={404: {"description": "Job not found"}},
)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(StoryJob).filter(StoryJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job