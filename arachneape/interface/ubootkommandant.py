
# this package
from arachneape.commoncode.baseclass import BaseClass
from arachneape.commoncode.strings import RED, BOLD, RESET
from arachneape.plugins.quartermaster import QuarterMaster


def try_except(method):
    """
    A decorator method to catch Exceptions

    :param:

     - `func`: A function to call
    """
    def wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as error:
            red_error = "{red}{bold}{{error}}{reset}".format(red=RED,
                                                             bold=BOLD,
                                                             reset=RESET)
            crash_notice = "{bold}********** Oops, I Crapped My Pants **********{reset}".format(red=RED,
                                                                             bold=BOLD,
                                                                             reset=RESET)
            self.logger.error(crash_notice)
            
            import traceback
            import sys
            import os
            
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb_info = traceback.extract_tb(exc_tb)
            filename, linenum, funcname, source = tb_info[-1]
            
            self.logger.error(red_error.format(error=error))
            self.logger.error(red_error.format(error="Failed Line: {0}".format(source)))
            self.logger.error(red_error.format(error="In Function: {0}".format(funcname)))
            self.logger.error(red_error.format(error="In File: {0}".format(os.path.basename(filename))))
            self.logger.error(red_error.format(error="At Line: {0}".format(linenum)))
            self.logger.debug(traceback.format_exc())
    return wrapped


class UbootKommandant(BaseClass):
    """
    a subcommand holder
    """
    def __init__(self):
        """
        UbootKommandant Constructor
        """
        super(UbootKommandant, self).__init__()
        self._quartermaster = None
        return

    @property
    def quartermaster(self):
        """
        A quartermaster for the plugins
        """
        if self._quartermaster is None:
            self._quartermaster = QuarterMaster()
        return self._quartermaster

    @try_except
    def list_plugins(self, args):
        """
        Calls the QuarterMaster and lists plugins

        :param:

         - `args`: not used
        """
        self.quartermaster.list_plugins()
        return

    @try_except
    def run(self, args):
        """
        Builds and runs the code
        """
        plugin = self.quartermaster.get_plugin('ArachneApe')
        ape = plugin().product
        if args.trace:
            from trace import Trace
        
            tracer = Trace(trace=True,
                           ignoremods= ['__init__', 'handlers',
                                        'threading', 'genericpath',
                                        'posixpath'],
                           timing=True)
            tracer.runfunc(ape)
        else:
            ape()
        return

    @try_except
    def fetch(self, args):
        """
        'fetch' a sample plugin config-file

        :param:

         - `args`: namespace with 'names' list attribute
        """
        for name in args.names:
            self.logger.debug("Getting Plugin: {0}".format(name))
            plugin = self.quartermaster.get_plugin(name)
            # the quartermaster returns definitions, not instances
            plugin().fetch_config()
        return

    @try_except
    def check(self, args):
        """
        Builds and checks the configuration

        :param:

         - `args`: namespace with `configfiles` list
        """
        self.logger.warning('UbootKommandant.check has not been implemented')
        return

    @try_except
    def handle_help(self, args):
        """
        Sends a help message to stdout

        :param:

         - `args`: namespace with 'name' and width attributes
        """
        plugin = self.quartermaster.get_plugin(args.name)
        try:
            plugin().help(args.width)
        except TypeError as error:
            self.logger.debug(error)
            print "'{0}' is not a known plugin.\n".format(args.name)
            print "These are the known plugins:\n"
            self.quartermaster.list_plugins()
        return
#


# python standard library
import unittest

# third-party
from mock import MagicMock, patch


class TestUbootKommandant(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock('uboot_logger')
        self.subcommander = UbootKommandant()
        self.subcommander._logger = self.logger
        return

    def test_list_plugins(self):
        """
        Does it call the quarter master's list_plugins?
        """
        qm = MagicMock()
        #with patch('arachneape.plugins.quartermaster.QuarterMaster', qm):
        #    self.subcommander.list_plugins()
        #qm.list_plugins.assert_called_with()
        return
# end TestUbootKommandant
