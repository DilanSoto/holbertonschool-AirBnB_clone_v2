#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_places(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.places), list)
        self.assertEqual(len(new.places), 0)

    def test_state_id_nullable(self):
        """ """
        new = self.value()
        self.assertEqual(new.state_id, None)

    def test_name_nullable(self):
        """ """
        new = self.value()
        self.assertEqual(new.name, None)

    def test_state_id_not_nullable(self):
        """ """
        with self.assertRaises(TypeError):
            new = self.value(state_id=None)

    def test_name_not_nullable(self):
        """ """
        with self.assertRaises(TypeError):
            new = self.value(name=None)(type(new.name), str)
