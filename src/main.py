from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

from src.routers import story, job
from src.db.database import create_tables

create_tables()  # Ensure that the database tables are created before the application starts.

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application with CORS middleware.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
     # TO handle/coontrol specific origins, methods, and headers for cross-origin requests to interact with the FastAPI application.
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(story.router, prefix=settings.API_PREFIX, tags=["stories"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)