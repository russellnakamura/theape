
# python standard library
from abc import ABCMeta, abstractmethod, abstractproperty

# this package 
from arachneape.commoncode.baseclass import BaseClass


class BasePlugin(BaseClass):
    """
    An abstract base-class for plugins
    """
    __metaclass__ = ABCMeta
    def __init__(self, configuration=None):
        super(BasePlugin, self).__init__()
        self._logger = None
        self._help = None
        self._config = None
        self._product = None
        return

    @property
    def help(self):
        """
        A help string for this plugin
        """
        return "'{0}' offers you no help. Such is life.".format(self.__class__.__name__)

    @abstractproperty
    def product(self):
        """
        The plugin (BaseProduct implementation)
        """
        return

    @property    
    def config(self):
        """
        Get sample config-file snippet required by this plugin
        """
        return "'{0}' has no configuration sample.".format(self.__class__.__name__)

# end class BasePlugin                
