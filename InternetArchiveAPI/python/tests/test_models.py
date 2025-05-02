"""
Tests for the models package
"""
import unittest
import logging
from app.models.film import Film
from app.models.collection import Collection


logging.basicConfig(level=logging.DEBUG)

class TestFilmModel(unittest.TestCase):
    """
    Test cases for the Film model
    """
    
    def test_film_creation(self):
        """
        Test creating a Film object
        """
        film = Film(identifier="test_id", title="Test Film", description="Test Description")
        logging.debug(f"Created film: {film}")          # Log with logging example
        self.assertEqual(film.identifier, "test_id")
        self.assertEqual(film.title, "Test Film")
        self.assertEqual(film.description, "Test Description")
    
    def test_film_to_dict(self):
        """
        Test converting a Film object to a dictionary
        """
        film = Film(identifier="test_id", title="Test Film", description="Test Description")
        film_dict = film.to_dict()
        
        self.assertEqual(film_dict["identifier"], "test_id")
        self.assertEqual(film_dict["title"], "Test Film")
        self.assertEqual(film_dict["description"], "Test Description")
    
    def test_film_from_dict(self):
        """
        Test creating a Film object from a dictionary
        """
        film_dict = {
            "identifier": "test_id",
            "title": "Test Film",
            "description": "Test Description"
        }
        
        film = Film.from_dict(film_dict)
        
        self.assertEqual(film.identifier, "test_id")
        self.assertEqual(film.title, "Test Film")
        self.assertEqual(film.description, "Test Description")


class TestCollectionModel(unittest.TestCase):
    """
    Test cases for the Collection model
    """
    
    def test_collection_creation(self):
        """
        Test creating a Collection object
        """
        collection = Collection(
            identifier="test_collection_id", 
            title="Test Collection", 
            description="Test Collection Description"
        )
        
        self.assertEqual(collection.identifier, "test_collection_id")
        self.assertEqual(collection.title, "Test Collection")
        self.assertEqual(collection.description, "Test Collection Description")
        self.assertEqual(len(collection.films), 0)
    
    def test_collection_with_films(self):
        """
        Test creating a Collection object with films
        """
        film1 = Film(identifier="film1", title="Film 1", description="Film 1 Description")
        film2 = Film(identifier="film2", title="Film 2", description="Film 2 Description")
        
        collection = Collection(
            identifier="test_collection_id", 
            title="Test Collection", 
            description="Test Collection Description",
            films=[film1, film2]
        )
        
        self.assertEqual(len(collection.films), 2)
        self.assertEqual(collection.films[0].identifier, "film1")
        self.assertEqual(collection.films[1].identifier, "film2")
    
    def test_collection_to_dict(self):
        """
        Test converting a Collection object to a dictionary
        """
        film1 = Film(identifier="film1", title="Film 1", description="Film 1 Description")
        film2 = Film(identifier="film2", title="Film 2", description="Film 2 Description")
        
        collection = Collection(
            identifier="test_collection_id", 
            title="Test Collection", 
            description="Test Collection Description",
            films=[film1, film2]
        )
        
        collection_dict = collection.to_dict()
        
        self.assertEqual(collection_dict["identifier"], "test_collection_id")
        self.assertEqual(collection_dict["title"], "Test Collection")
        self.assertEqual(collection_dict["description"], "Test Collection Description")
        self.assertEqual(len(collection_dict["films"]), 2)
        self.assertEqual(collection_dict["films"][0]["identifier"], "film1")
        self.assertEqual(collection_dict["films"][1]["identifier"], "film2")


if __name__ == "__main__":
    unittest.main() 