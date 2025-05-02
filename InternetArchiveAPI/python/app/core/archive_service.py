"""
Service for interacting with the Internet Archive API
"""
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from ..utils.http_client import HttpClient
from ..models.film import Film
from ..models.collection import Collection

# Load environment variables

load_dotenv()


class ArchiveService:
    """
    Service for interacting with the Internet Archive API
    """
    # Get base URL from environment variable, with fallback to default value
    BASE_URL = os.getenv("ARCHIVE_API_BASE_URL", "https://archive.org/advancedsearch.php")
    
    def __init__(self):
        self.http_client = HttpClient()
    
    def search_collections(self, 
                        collection: str = "*", 
                        mediatype: str = "movies", 
                        page: int = 1, 
                        rows: int = 10, 
                        sort: str = "stars desc") -> Dict[str, Any]:
        """
        Search for film collections
        
        Args:
            collection: The collection to search for
            mediatype: The media type to filter by
            page: The page number to fetch
            rows: The number of rows to fetch per page
            sort: The sorting criteria
            
        Returns:
            A dictionary with the complete response including collections
        """
        # Use exactly the same query that works with curl, but with flexible parameters
        sort_param = sort.replace(" ", "+")  # "stars desc" >> "stars+desc"
        
        print(f"Searching: collection:({collection}) AND mediatype:({mediatype}) with sort={sort_param}, rows={rows}, page={page}")
        
        params = {
            "q": f"collection:({collection}) AND mediatype:({mediatype})",
            "fl": "identifier,title,description",
            "rows": rows,
            "page": page,
            "output": "json",
            "sort": sort_param
        }
        
        # Manually construct the URL to ensure the correct format
        url_params = "&".join([f"{k}={v}" for k, v in params.items()])
        full_url = f"{self.BASE_URL}?{url_params}"
        print(f"Full URL: {full_url}")
        
        api_response = self.http_client.get(full_url)
        
        # Verify if we received a valid response
        if not api_response:
            print("Empty API response")
            return {
                "response": {
                    "numFound": 0,
                    "start": 0,
                    "qin": f"collection:({collection}) AND mediatype:({mediatype})",
                    "fields": "identifier,title,description",
                    "rows": rows,
                    "description": "No results found",
                    "docs": []
                }
            }
        
        # Process the response to add thumbnails to the documents
        if "response" in api_response and "docs" in api_response["response"]:
            docs = api_response["response"]["docs"]
            for doc in docs:
                doc["thumbnail_url"] = f"https://archive.org/services/img/{doc.get('identifier')}"
        
        # Get the original query parameters
        original_params = api_response.get("responseHeader", {}).get("params", {})
        
        # Create a formatted response without the responseHeader
        formatted_response = {
            "response": {
                **api_response.get("response", {}),
                "qin": original_params.get("qin", f"collection:({collection}) AND mediatype:({mediatype})"),
                "fields": original_params.get("fields", "identifier,title,description"),
                "rows": rows,
                "description": f"Explore results for all collections of videos in Internet Archive API: Collection=({collection}) and MediaType=({mediatype})"
            }
        }
        
        resp = formatted_response["response"]
        docs = resp.pop("docs", [])
        ordered_response = {k: resp[k] for k in resp}
        ordered_response["docs"] = docs

        return ordered_response
    
    def search_films_by_collection(self, collection_id: str, page: int = 1, rows: int = 10, sort: str = "stars desc") -> List[Film]:
        """
        Search for films within a specific collection
        
        Args:
            collection_id: The identifier of the collection
            page: The page number to fetch
            rows: The number of rows to fetch per page
            sort: The sorting criteria
            
        Returns:
            A list of Film objects
        """
        params = {
            "q": f"collection:({collection_id}) AND mediatype:(movies)",
            "fl": "identifier,title,description",
            "rows": rows,
            "page": page,
            "output": "json",
            "sort": sort.replace(" ", "+")
        }
        
        url_params = "&".join([f"{k}={v}" for k, v in params.items()])
        full_url = f"{self.BASE_URL}?{url_params}"
        
        response = self.http_client.get(full_url)
        header_params = response.get("responseHeader", {}).get("params", {})
        results = response.get("response", {}).get("docs", [])

        print(f"Header Params: {header_params}")

        films = []
        for result in results:
            film = Film.from_dict(result)
            # Add thumbnail URL
            film.thumbnail_url = f"https://archive.org/services/img/{film.identifier}"
            films.append(film)
            
        return films
    
    def get_collection_with_films(self, collection_id: str, film_rows: int = 10, page: int = 1) -> Optional[Collection]:
        """
        Get a collection by its identifier and include its films
        
        Args:
            collection_id: The identifier of the collection
            film_rows: The number of films to include
            page: The page number for films pagination
            
        Returns:
            A Collection object with films, or None if not found
        """

        params = {
            "q": f"identifier:({collection_id})",
            "fl": "identifier,title,description",
            "rows": 1,
            "output": "json"
        }
        
        response = self.http_client.get(self.BASE_URL, params=params)
        results = response.get("response", {}).get("docs", [])
        
        if not results:
            return None
        
        collection_data = results[0]
        collection = Collection.from_dict(collection_data)
        
        # Get the original query parameters
        header_params = response.get("responseHeader", {}).get("params", {})
        
        collection.qin      = header_params.get("qin", None)
        collection.fields   = header_params.get("fields", None)
        collection.rows     = film_rows
        collection.page     = page

        # Add thumbnail URL for the collection
        collection.thumbnail_url = f"https://archive.org/services/img/{collection.identifier}"

        # Now get the films for this collection, using the specified page
        films = self.search_films_by_collection(collection_id, page=page, rows=film_rows)
        collection.films = films
        
        return collection
        
    def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific video
        
        Args:
            video_id: The identifier of the video
            
        Returns:
            A dictionary with video details, or None if not found
        """
        # First, get the basic metadata for the video
        params = {
            "q": f"identifier:({video_id})",
            "fl": "identifier,title,description,creator,date,subject,publicdate,addeddate,mediatype,collection",
            "rows": 1,
            "output": "json"
        }
        
        response = self.http_client.get(self.BASE_URL, params=params)
        results = response.get("response", {}).get("docs", [])
        
        if not results:
            return None
        
        video_data = results[0]
        
        # Get the additional metadata including files for thumbnails and playback URLs
        item_metadata_url = f"https://archive.org/metadata/{video_id}"
        item_metadata = self.http_client.get(item_metadata_url)
        
        # Extract thumbnail URL
        thumbnail_url = None
        files = item_metadata.get("files", [])
        for file in files:
            if file.get("name", "").endswith(".jpg") and "thumb" in file.get("name", ""):
                thumbnail_url = f"https://archive.org/download/{video_id}/{file.get('name')}"
                break
        
        # Fallback thumbnail if none found
        if not thumbnail_url:
            thumbnail_url = f"https://archive.org/services/img/{video_id}"
        
        # Extract playback URLs (video files)
        playback_urls = []
        for file in files:
            # Look for MP4, WebM, or other video formats
            if file.get("name", "").endswith((".mp4", ".webm", ".avi", ".mov")):
                playback_urls.append({
                    "format": file.get("format", "Unknown"),
                    "url": f"https://archive.org/download/{video_id}/{file.get('name')}"
                })
        
        # Combine the data into a comprehensive video details object
        video_details = {
            **video_data,
            "thumbnail_url": thumbnail_url,
            "playback_urls": playback_urls,
            "metadata": item_metadata.get("metadata", {})
        }
        
        return video_details 