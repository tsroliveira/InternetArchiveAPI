"""
Video model representing a detailed Internet Archive video item
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class VideoPlaybackUrl:
    """
    Represents a playback URL for a video
    """
    format: str
    url: str
    
    def to_dict(self) -> Dict[str, str]:
        """
        Convert the playback URL object to a dictionary
        """
        return {
            "format": self.format,
            "url": self.url
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "VideoPlaybackUrl":
        """
        Create a VideoPlaybackUrl object from a dictionary
        """
        return cls(
            format=data.get("format", "Unknown"),
            url=data.get("url", "")
        )


@dataclass
class Video:
    """
    Represents a detailed video item from the Internet Archive
    """
    identifier: str
    title: str
    description: Optional[str] = None
    creator: Optional[str] = None
    date: Optional[str] = None
    subject: Optional[List[str]] = field(default_factory=list)
    collection: Optional[List[str]] = field(default_factory=list)
    thumbnail_url: Optional[str] = None
    playback_urls: List[VideoPlaybackUrl] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the video object to a dictionary
        """
        return {
            "identifier": self.identifier,
            "title": self.title,
            "description": self.description,
            "creator": self.creator,
            "date": self.date,
            "subject": self.subject,
            "collection": self.collection,
            "thumbnail_url": self.thumbnail_url,
            "playback_urls": [url.to_dict() for url in self.playback_urls],
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Video":
        """
        Create a Video object from a dictionary
        """
        # Process playback URLs if present
        playback_urls = []
        if "playback_urls" in data:
            playback_urls = [
                VideoPlaybackUrl.from_dict(url_data) 
                for url_data in data.get("playback_urls", [])
            ]
        
        # Process collections if present
        collections = data.get("collection", [])
        if isinstance(collections, str):
            collections = [collections]
        
        # Process subjects if present
        subjects = data.get("subject", [])
        if isinstance(subjects, str):
            subjects = [subjects]
        
        return cls(
            identifier=data.get("identifier", ""),
            title=data.get("title", ""),
            description=data.get("description", None),
            creator=data.get("creator", None),
            date=data.get("date", None),
            subject=subjects,
            collection=collections,
            thumbnail_url=data.get("thumbnail_url", None),
            playback_urls=playback_urls,
            metadata=data.get("metadata", {})
        ) 