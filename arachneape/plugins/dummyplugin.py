
# python standard library
from collections import OrderedDict

# this package
from base_plugin import BasePlugin
from arachneape.components.helppage.helppage import HelpPage


DESCRIPTION = """{bold}DummyClass{reset} logs its calls and then returns. It is meant to be used as changes are made to the infrastructure so that the {blue}ArachneApe{reset} can be tested without using and other components."""
EXAMPLES = """{bold}dummy(){reset}"""
NOTE = "The {bold}DummyClass{reset} will change as the infrastructure changes. In particular the building and testing of plugins and components will likely evolve once real plugins are created."


output_documentation = __name__ == '__builtin__'


class DummyPlugin(BasePlugin):
    """
    A plugin to test the infrastructure (a no-op)
    """
    def __init__(self, *args, **kwargs):
        super(DummyPlugin, self).__init__(*args, **kwargs)
        return

    @property
    def sections(self):
        """
        An ordered dict for the help page
        """
        if self._sections is None:
            bold = "{bold}"
            blue = '{blue}'
            reset = '{reset}'
            red = '{red}'
            space = ' '
            
            self._sections = OrderedDict()
            self._sections['Name'] = (bold + 'DummyClass' + reset +
                                        ' -- a no-op')
            self._sections['Description'] = DESCRIPTION
            self._sections['Example'] = EXAMPLES
            self._sections['Note'] = NOTE
        return self._sections

    @property
    def product(self):
        """
        builds and returns a DummyClass         
        """
        if self._product is None:
            self._product = DummyClass()
        return self._product

    @property
    def fetch_config(self):
        """
        prints a message saying there is no configuration
        """
        print "DummyConfig needs no configuration"
        return
# endi class DummyConfig    
