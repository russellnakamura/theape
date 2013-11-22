
# python standard library
import unittest

# third-party
from mock import MagicMock, patch

# this package
from ape.parts.countdown.countdown import CountdownTimer, INFO


class TestCountdownTimer(unittest.TestCase):
    def setUp(self):
        # patch datetime
        self.datetime_patch = patch('datetime.datetime')
        self.datetime = self.datetime_patch.start()
        self.log_level = INFO
        self.logger = MagicMock()        

        self.repetitions = 2
        self.timer = CountdownTimer(repetitions=2, log_level=INFO)
        return

    def tearDown(self):
        """
        Stop the patches
        """
        self.datetime_patch.stop()
        return


    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.timer.repetitions, self.repetitions)
        self.assertEqual(self.timer.log_level, INFO)
        self.assertIsNone(self.timer.start)
        self.assertIsNone(self.timer.last_time)
        self.assertIsNone(self.timer._times)
        return

    def test_call(self):
        """
        Does it keep track of time for the right number of repetitions?
        """


        return
