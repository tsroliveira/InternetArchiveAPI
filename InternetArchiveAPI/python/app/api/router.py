"""
FastAPI router for the Internet Archive API
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from ..core.archive_service import ArchiveService
from ..models.film import Film
from ..models.collection import Collection
from ..models.video import Video, VideoPlaybackUrl

router = APIRouter(prefix="/api/v1", tags=["archive"])

archive_service = ArchiveService()


@router.get("/explore", response_model=Dict[str, Any])
async def explore(
    collection: str = Query("*", description="The collection to search for"),
    page: int = Query(1, ge=1, description="Page number"),
    rows: int = Query(10, ge=1, le=100, description="Rows per page"),
    sort: str = Query("stars desc", description="Sort criteria")
):
    """
    Get a list of film collections for exploration
    """
    try:
        collections_response = archive_service.search_collections(
            collection=collection,
            page=page, 
            rows=rows, 
            sort=sort
        )
        return collections_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch collections: {str(e)}")


@router.get("/collections/{collection_id}", response_model=Dict[str, Any])
async def get_collection(
    collection_id: str,
    film_rows: int = Query(10, ge=1, le=100, description="Number of films to include"),
    page: int = Query(1, ge=1, description="Page number for films")
):
    """
    Get a collection by its identifier, including its films.
    Use film_rows to limit the number of films returned.
    Use page to paginate through the films in the collection.
    """
    try:
        collection = archive_service.get_collection_with_films(collection_id, film_rows=film_rows, page=page)
        if not collection:
            raise HTTPException(status_code=404, detail=f"Collection with ID {collection_id} not found")
        return collection.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch collection: {str(e)}")


@router.get("/collections/{collection_id}/items", response_model=List[Dict[str, Any]])
async def get_collection_items(
    collection_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    rows: int = Query(10, ge=1, le=100, description="Rows per page"),
    sort: str = Query("stars desc", description="Sort criteria")
):
    """
    Get videos (items) within a specific collection
    """
    try:
        films = archive_service.search_films_by_collection(collection_id, page=page, rows=rows, sort=sort)
        return [film.to_dict() for film in films]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {str(e)}")


@router.get("/videos/{video_id}", response_model=Dict[str, Any])
async def get_video_details(video_id: str):
    """
    Get detailed information about a specific video
    """
    try:
        video_details = archive_service.get_video_details(video_id)
        if not video_details:
            raise HTTPException(status_code=404, detail=f"Video with ID {video_id} not found")
        
        # Create a Video object from the details
        playback_urls = []
        for url_data in video_details.get("playback_urls", []):
            playback_urls.append(VideoPlaybackUrl(
                format=url_data.get("format", "Unknown"),
                url=url_data.get("url", "")
            ))
        
        video = Video(
            identifier=video_details.get("identifier", ""),
            title=video_details.get("title", ""),
            description=video_details.get("description", None),
            creator=video_details.get("creator", None),
            date=video_details.get("date", None),
            subject=video_details.get("subject", []),
            collection=video_details.get("collection", []),
            thumbnail_url=video_details.get("thumbnail_url", None),
            playback_urls=playback_urls,
            metadata=video_details.get("metadata", {})
        )
        
        return video.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch video details: {str(e)}") 