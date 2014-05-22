
# python standard library
import os
import importlib
import inspect
import pkg_resources
import pkgutil


class RyeMother(object):
    """
    A gatherer of child classes
    """
    def __init__(self, exclusions='index.py __init__.py'.split(),
                 group=None, name=None,
                 keyfunction=None):
        """
        Rye Mother constructor

        :param:

         - `exclusions`: list of filenames to ignore
         - `group`: group-name from the setup.py entry_points
         - `name`: name of entry in group
         - `keyfunction`: a function to transform the dictionary keys
        """
        self.group = group
        self.name = name
        self.exclusions = exclusions
        self.keyfunction = keyfunction
        return
        
    def __call__(self, parent, group=None, name=None, keyfunction=None):
        """
        The main interface

        :param:

         - `parent`: parent class whose children to gather
         - `group`: [<group.name>] entry from setup.py entry_points
         - `name`: name given in the entry_point 
         - `keyfunction`: function to transform the keys of the dict

        :return: dict of name:class definition
        """
        if group is None:
            group = self.group
            
        if name is None:
            name = self.name
            
        def is_child(candidate):
            # this is a filter for inspect.getmembers
            # returns True if candidate object has the correct parent class
            return hasattr(candidate, '__base__') and candidate.__base__ is parent

        if keyfunction is None:
            keyfunction = self.keyfunction
            
        children = {}

        module = pkg_resources.load_entry_point('ape', group, name)
        dirname = os.path.dirname(module.__file__)
        prefix = module.__package__ + '.'
        names = (name for loader, name, is_pkg in pkgutil.iter_modules([dirname],prefix) if not is_pkg)
        modules = (importlib.import_module(name) for name in names)

        for module in modules:
            # members is a list of children in the module
            members = inspect.getmembers(module, predicate=is_child)
            for member in members:
                # member is a name, class definition tuple
                name, definition = member
                if keyfunction:
                    name = keyfunction(name)
                children[name] = definition
        return children
