"""
Film model representing an Internet Archive film item
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Film:
    """
    Represents a film item from the Internet Archive
    """
    identifier: str
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert the film object to a dictionary
        """
        return {
            "identifier": self.identifier,
            "title": self.title,
            "description": self.description,
            "thumbnail_url": self.thumbnail_url
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Film":
        """
        Create a Film object from a dictionary
        """
        return cls(
            identifier=data.get("identifier", ""),
            title=data.get("title", ""),
            description=data.get("description", None),
            thumbnail_url=data.get("thumbnail_url", None)
        ) 