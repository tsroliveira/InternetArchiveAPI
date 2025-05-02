"""
Collection model representing an Internet Archive film collection
"""
from dataclasses import dataclass, field
from typing import List, Optional
from .film import Film


@dataclass
class Collection:
    """
    Represents a collection of films from the Internet Archive
    """
    identifier: str
    title: str
    description: Optional[str] = None
    qin: Optional[str] = None
    fields: Optional[str] = None
    rows: Optional[int] = None
    page: Optional[int] = None
    thumbnail_url: Optional[str] = None
    films: List[Film] = field(default_factory=list)

    def to_dict(self) -> dict:
        """
        Convert the collection object to a dictionary
        """
        return {
            "identifier": self.identifier,
            "title": self.title,
            "description": self.description,
            "qin": self.qin,
            "fields": self.fields,
            "rows": self.rows,
            "page": self.page,
            "thumbnail_url": self.thumbnail_url,
            "films": [film.to_dict() for film in self.films]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Collection":
        """
        Create a Collection object from a dictionary
        """
        films_data = data.get("films", [])
        films = [Film.from_dict(film_data) for film_data in films_data]
        
        return cls(
            identifier=data.get("identifier", ""),
            title=data.get("title", ""),
            description=data.get("description", None),
            qin=data.get("qin", None),
            fields=data.get("fields", None),
            rows=data.get("rows", None),
            page=data.get("page", None),
            thumbnail_url=data.get("thumbnail_url", None),
            films=films
        ) 