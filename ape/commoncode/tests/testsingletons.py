
# python standard library
import unittest

# third party
from mock import MagicMock

# this package
import ape.commoncode.singletons as singletons
from ape.components.component import Composite
from singletonimporter import test_singleton_1
from ape import DontCatchError
from ape.parts.storage.filestorage import FileStorage


class TestSingletons(unittest.TestCase):
    def setUp(self):
        self.name = 'tester'
        self.singleton = singletons.get_composite(self.name)
        return
    
    def test_composite_singleton(self):
        """
        Does it get the same singleton until refreshed?
        """
        self.assertIsInstance(self.singleton, Composite)
        singleton2 = singletons.get_composite(self.name)
        self.assertIs(self.singleton, singleton2)
        return

    def test_composite_category(self):
        """
        Does using a different name change the singleton?
        """
        singleton_2 = singletons.get_composite('newname')
        self.assertIsNot(singleton_2, self.singleton)
        return

    def test_composite_singleton_import(self):
        """
        Does importing the same singleton from another module get the same object
        """
        self.assertIs(self.singleton, test_singleton_1)
        return

    def test_refresh(self):
        """
        Does refreshing the singletons create a new object?
        """        
        singletons.refresh()
        new_singleton = singletons.get_composite(self.name)
        self.assertIsNot(self.singleton, new_singleton)
        return

    def test_default_error(self):
        """
        Is the default composite error a DontCatchError?
        """
        class TestComponent(object):
            def __call__(self):
                raise DontCatchError()

            def check_rep(self):
                return
            
        component = TestComponent()
        
        self.singleton.add(component)

        # this catches the DontCatchError
        self.singleton()

        class CrashComponent(object):
            def __call__(self):
                raise IndexError('a random error')            
            def check_rep(self):
                return

        component2 = CrashComponent()
        self.singleton.add(component2)

        # this crashes with the IndexError
        with self.assertRaises(IndexError):
            self.singleton()
# end TestSingletons


class TestFileSingleton(unittest.TestCase):
    def setUp(self):
        self.name = 'tester'
        self.singleton = singletons.get_filestorage(self.name)
        return

    def test_file_singleton(self):
        """
        Does it get the same FileStorage
        """
        self.assertIsInstance(self.singleton, FileStorage)
        singleton2 = singletons.get_filestorage(self.name)
        self.assertIs(singleton2, self.singleton)
        return
# end TestFileSingleton
