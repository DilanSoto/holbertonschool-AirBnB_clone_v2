#!/usr/bin/python3
"""
Handles the unittest for Basemodel
"""
import models
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """
    Unittest for Basemodel class
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor for our test objs
        """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """
        Set us up for a new test
        """
        pass

    def tearDown(self):
        """
        Tear us down after a test
        """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass
        except OSError as e:
            print(f"Error removing file: {e}")

    def test_default(self):
        """
        Test default values in our objs
        """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """
        Test that our Kwargs do no accept integer for keys
        """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """
        Testing save of our objs
        """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """
        Test the to string method
        """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """
        Test the todict() method
        """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """
        Tests the behavior when kwargs is None
        """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """
        Test with a single key=value
        """
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """
        Test type for our id's
        """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """
        Test the type of ur created_at attr
        """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """
        Test the update_at attr
        """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    def test_init(self):
        """
        Test the initialization of BaseModel instance
        """
        i = self.value()
        self.assertEqual(type(i.id), str)
        self.assertEqual(type(i.created_at), datetime.datetime)
        self.assertEqual(type(i.updated_at), datetime.datetime)

    def test_str_representation(self):
        """
        Test the string representation of BaseModel instance
        """
        i = self.value()
        expected_str = '[{}] ({}) {}'.format(self.name, i.id, i.__dict__)
        self.assertEqual(str(i), expected_str)

    def test_save_updates_updated_at(self):
        """
        Test that save() method updates the updated_at attribute
        """
        i = self.value()
        old_updated_at = i.updated_at
        i.save()
        self.assertNotEqual(old_updated_at, i.updated_at)

    def test_to_dict(self):
        """
        Test the to_dict() method of BaseModel instance
        """
        i = self.value()
        d = i.to_dict()
        self.assertEqual(type(d), dict)
        self.assertIn('__class__', d)
        self.assertEqual(d['__class__'], self.name)
        self.assertIn('id', d)
        self.assertEqual(d['id'], i.id)
        self.assertIn('created_at', d)
        self.assertEqual(d['created_at'], i.created_at.isoformat())
        self.assertIn('updated_at', d)
        self.assertEqual(d['updated_at'], i.updated_at.isoformat())

    def test_delete(self):
        """
        Test the delete() method of BaseModel instance
        """
        i = self.value()
        i.save()
        i.delete()
        self.assertNotIn(i, models.storage.all().values())