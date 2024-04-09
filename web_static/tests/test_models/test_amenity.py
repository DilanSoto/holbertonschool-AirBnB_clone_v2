
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from os import getenv


class TestAmenity(unittest.TestCase):
    def test_inheritance(self):
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertIsInstance(amenity, Base)

    def test_attributes(self):
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        self.assertIsInstance(amenity.name, Column)
        self.assertEqual(amenity.name.type, String(128))
        self.assertFalse(amenity.name.nullable)

    def test_relationship(self):
        if getenv("HBNB_TYPE_STORAGE") == "db":
            amenity = Amenity()
            self.assertTrue(hasattr(amenity, "place_amenities"))
            self.assertIsInstance(amenity.place_amenities, relationship)
            self.assertEqual(amenity.place_amenities.secondary,
                             'place_amenity')
            self.assertEqual(amenity.place_amenities.back_populates,
                             'amenities')


if __name__ == '__main__':
    unittest.main()
