"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.router import router as api_router

app = FastAPI(
    title="Internet Archive Feature Films API",
    description="API facade for accessing Internet Archive Video Content",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint returning API information
    """
    return {
        "name": "Internet Archive Feature Films API",
        "version": "0.1.0",
        "description": "API facade for accessing Internet Archive Video Content",
        "docs_url": "/docs",
        "explore_url": "/api/v1/explore",
        "endpoints": {
            "explore": "/api/v1/explore",
            "collection_details": "/api/v1/collections/{collection_id}",
            "collection_items": "/api/v1/collections/{collection_id}/items",
            "video_details": "/api/v1/videos/{video_id}"
        }
    } 