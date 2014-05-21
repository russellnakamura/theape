
# python standard library
import unittest
import os

#the ape
from ape.commoncode.ryemother import RyeMother
# testing only
from basetest import BaseTest
from  children import Boy
from children import Girl


class TestRyeMother(unittest.TestCase):
    def test_constructor(self):
        """
        Does it build?
        """
        rye_mother = RyeMother(dirname=__file__, package=__package__)
        self.assertEqual(rye_mother.dirname, __file__)
        self.assertEqual(rye_mother.package, __package__)
        
        rye_mother = RyeMother()
        self.assertEqual(os.path.dirname(rye_mother.dirname) + '/tests' ,
                         os.path.dirname(__file__))
        self.assertEqual(rye_mother.package,
                         '.'.join(__package__.split('.')[:-1]))
        return

    def test_call(self):
        """
        Does it find the children?
        """
        # I think in many cases I want a lower-cased name
        rye_mother = RyeMother(__file__, package=__package__,
                               keyfunction=lambda k: getattr(k, 'lower')())
        self.assertTrue(rye_mother._package is not None)
        print 'calling the rye mother'
        children = rye_mother(BaseTest)
        self.assertIs(children['boy'], Boy)
        self.assertEqual(children['girl']().name, 'girl')
        
        # try without the lower-cased keys
        rye_mother.keyfunction = None
        children = rye_mother(BaseTest)
        self.assertEqual(children['Boy']().name, 'boy')
        self.assertIs(children['Girl'], Girl)
        return
