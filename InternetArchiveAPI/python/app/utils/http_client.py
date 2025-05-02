"""
HTTP client for making requests to the Internet Archive API
"""
import requests
from typing import Dict, Any, Optional


class HttpClient:
    """
    HTTP client for making requests to external APIs
    """
    
    @staticmethod
    def get(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the specified URL
        
        Args:
            url: The URL to make the request to
            params: Optional query parameters
            
        Returns:
            The response as a dictionary
            
        Raises:
            requests.RequestException: If the request fails
        """
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() 