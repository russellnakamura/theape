
# python standard library
import os
import importlib
import inspect


class RyeMother(object):
    """
    A gatherer of child classes
    """
    def __init__(self, dirname=None, package=None,
                 exclusions='index.py __init__.py'.split(),
                 keyfunction=None):
        """
        Rye Mother constructor

        :param:

         - `dirname`: name of directory to search for modules
         - `package`: dotted notation up to modules of interest
         - `exclusions`: list of filenames to ignore
         - `keyfunction`: a function to transform the dictionary keys
        """
        self._dirname = dirname
        self._package = package
        self.exclusions = exclusions
        self.keyfunction = keyfunction
        return

    @property
    def dirname(self):
        """
        The directory to look for modules

        This was created so pweave will work
        """
        if self._dirname is None:
            self._dirname = __file__
        return self._dirname

    @property
    def package(self):
        """
        Dotted notation to package containing modules of interest
        """
        if self._package is None:
            self._package = __package__
        return self._package
        
    def __call__(self, parent, package=None, keyfunction=None):
        """
        The main interface

        :param:

         - `parent`: parent class whose children to gather
         - `package`: replacement dotted notation for import package
         - `keyfunction`: function to transform the keys of the dict

        :return: dict of name:class definition
        """
        if keyfunction is None:
            keyfunction = self.keyfunction
            
        if package is None:
            package = self.package

        def is_child(o):
            # this is a filter for inspect.getmembers
            return hasattr(o, '__base__') and o.__base__ is parent
        children = {}

        dirname = os.path.dirname(self.dirname)
        
        filenames = (name for name in os.listdir(dirname) if name.endswith('.py')
                     and name not in self.exclusions)
        basenames_extensions = (os.path.splitext(name) for name in filenames)

        modules = (importlib.import_module('.'.join((self.package, base)))
                   for base, extension in basenames_extensions)
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
