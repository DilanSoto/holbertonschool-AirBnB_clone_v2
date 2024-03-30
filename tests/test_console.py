#!/usr/bin/python3

import unittest
from unittest.mock import patch
from io import StringIO
import console
from console import HBNBCommand
import pep8


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")

    def test_emptyline(self):
        """Test for emptyline method"""
        cmd = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd.emptyline()
            self.assertEqual(f.getvalue(), '')

    def test_do_quit(self):
        """Test for do_quit method"""
        cmd = HBNBCommand()
        self.assertTrue(cmd.do_quit(''))

    def test_do_EOF(self):
        """Test for do_EOF method"""
        cmd = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(cmd.do_EOF(''))
            self.assertEqual(f.getvalue(), '\n')

    def test_do_create(self):
        """Test for do_create method"""
        cmd = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd.do_create('BaseModel')
            output = f.getvalue().strip()
            self.assertTrue(len(output) > 0)
            self.assertEqual(output, cmd.do_create('BaseModel'))

    def test_do_show(self):
        """Test for do_show method"""
        cmd = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd.do_show('BaseModel 123')
            output = f.getvalue().strip()
            self.assertEqual(output, '** no instance found **')

    def test_do_destroy(self):
        """Test for do_destroy method"""
        cmd = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd.do_destroy('BaseModel 123')
            output = f.getvalue().strip()
            self.assertEqual(output, '** no instance found **')

    def test_do_all(self):
        """Test for do_all method"""
        cmd = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd.do_all('')
            output = f.getvalue().strip()
            self.assertEqual(output, '')

    def test_do_update(self):
        """Test for do_update method"""
        cmd = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd.do_update('BaseModel 123')
            output = f.getvalue().strip()
            self.assertEqual(output, '** no instance found **')

    def test_count(self):
        """Test for count method"""
        cmd = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd.count('BaseModel')
            output = f.getvalue().strip()
            self.assertEqual(output, '0')

    def test_strip_clean(self):
        """Test for strip_clean method"""
        cmd = HBNBCommand()
        args = ['BaseModel', 'create()']
        result = cmd.strip_clean(args)
        self.assertEqual(result, 'BaseModel create()')

    def test_default(self):
        """Test for default method"""
        cmd = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd.default('BaseModel.all()')
            output = f.getvalue().strip()
            self.assertEqual(output, '')


if __name__ == '__main__':
    unittest.main()