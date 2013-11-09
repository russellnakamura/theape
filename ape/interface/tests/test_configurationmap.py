
#python standard-library
import unittest
from StringIO import StringIO
import random
import textwrap
from datetime import timedelta, datetime

# third-party
from mock import MagicMock, patch, mock_open

# this package
from ape.interface.configurationmap import ConfigurationMap
from ape.commoncode.errors import ConfigurationError


RANDOM_MIN = random.randint(-100,0)
RANDOM_MAX = random.randint(0, 100)
config = StringIO('''
[DEFAULT]
config_glob = *.ini
''')

sub_config = StringIO('''
[APE]
umma=gumma
alpha = a, b, c
beta = a:x, b:y
gamma = z:q, w:r
''')

sub_config_2 = StringIO('''
[SUBConfig2]
ten = 10
x = 2.5
not_true = False
''')

SUBCONFIG2 = 'SUBConfig2'

configs = [config, sub_config, sub_config_2]
def config_effect(name):
    return configs.pop(0)


class TestConfigurationMap(unittest.TestCase):
    def setUp(self):
        self.filename = 'filename.ini'
        self.config = ConfigurationMap(self.filename)
        self.config._logger = MagicMock()
        return 
        
    def test_constructor(self):
        """
        Does the signature match what's expected?
        """
        self.assertEqual(self.filename, self.config.filename)
        with self.assertRaises(TypeError):
            ConfigurationMap()
        return

    def test_parser(self):
        """
        Does the parser get the right values from the sample string?
        """
        iglob = MagicMock()
        m = mock_open()
        m.side_effect = config_effect
        iglob.return_value = ['ape.ini', 'beep.ini']
        with patch('__builtin__.open', m):
            with patch('glob.iglob', iglob):
                parser = self.config.parser
        self.assertTrue(self.config.has_option('DEFAULT', 'config_glob'))
        iglob.assert_called_with('*.ini')
        self.assertEqual(self.config.get('APE', 'umma'), 'gumma')
        self.assertIsNone(self.config.get('APE', 'amma', optional=True))
        self.assertEqual(sorted(self.config.sections), 'APE SUBConfig2'.split())
        self.assertEqual(sorted(self.config.options(SUBCONFIG2)), 'config_glob not_true ten x'.split())
        self.assertEqual(self.config.get_int(SUBCONFIG2, 'ten'), 10)
        with self.assertRaises(ConfigurationError):
            self.config.get_int(SUBCONFIG2, 'x')
        self.assertEqual(self.config.get_float(SUBCONFIG2, 'x'), 2.5)
        self.assertFalse(self.config.get_boolean(SUBCONFIG2, 'not_true'))
        self.assertEqual(self.config.get_list('APE', 'alpha'), 'a b c'.split())
        self.assertEqual(self.config.get_tuple('APE', 'alpha'), tuple('a b c'.split()))
        self.assertItemsEqual(self.config.get_dictionary('APE', 'beta').keys(), 'a b'.split())
        self.assertItemsEqual(self.config.get_dictionary('APE', 'beta').values(), 'x y'.split())
        self.assertItemsEqual(self.config.get_ordered_dictionary('APE', 'gamma').keys(), 'z w'.split())
        named = self.config.get_named_tuple('APE', 'gamma')
        self.assertEqual(named.z, 'q')
        return

    def test_get_relativetime(self):
        """
        Does it get a timedelta from the configuration?
        """
        m = mock_open()

        weeks = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        days = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        hours = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        minutes = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        seconds = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        source = '{w} wks {d} days {s} sec {m} minu {h} hrs'.format(w=weeks,
                                                                    d=days,
                                                                    s=seconds,
                                                                    m=minutes,
                                                                    h=hours)
        timeconfig = StringIO(textwrap.dedent('''
        [RELATIVE]
        sometime = {s}
        ''').format(s=source))

        m.return_value = timeconfig
        with patch('__builtin__.open', m):
            config = ConfigurationMap('relative.ini')
            delta = config.get_relativetime('RELATIVE', 'sometime')

        expected = timedelta(weeks=weeks,
                             days=days,
                             hours=hours,
                             seconds=seconds,
                             minutes=minutes)
        self.assertTrue(delta == expected)
        return

    def test_get_absolutetime(self):
        """
        Does it get a datetime object?
        """
        m = mock_open()

        year = random.randint(1000,3000)
        month = random.randint(1,12)

        day = random.randint(1, 28)
        hour = random.randint(0, 24)
        minute = random.randint(0, 60)
        seconds = random.randint(0, 60)
        source = '{y}-{mo}-{d} {h}:{mi}:{s}'.format(y=year,
                                                    mo=month,
                                                    d=day,
                                                    h=hour,
                                                    mi=minute,
                                                    s=seconds)
        timeconfig = StringIO(textwrap.dedent('''
        [ABSOLUTE]
        sometime = {s}
        ''').format(s=source))

        m.return_value = timeconfig
        with patch('__builtin__.open', m):
            config = ConfigurationMap('relative.ini')
            delta = config.get_datetime('ABSOLUTE', 'sometime')

        expected = datetime(year=year,
                            month=month,
                            day=day,
                            hour=hour,
                            minute=minute,
                            second=seconds)
        self.assertTrue(delta == expected)
        return



if __name__ == '__main__':
        m = mock_open()

        weeks = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        days = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        hours = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        minutes = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        seconds = round(random.uniform(RANDOM_MIN, RANDOM_MAX), 1)
        source = '{w} wks {d} days {s} sec {m} minu {h} hrs'.format(w=weeks,
                                                                    d=days,
                                                                    s=seconds,
                                                                    m=minutes,
                                                                    h=hours)
        timeconfig = StringIO(textwrap.dedent('''
        [RELATIVE]
        sometime = {s}
        ''').format(s=source))

        m.return_value = timeconfig

        with patch('__builtin__.open', m):
            config = ConfigurationMap('relative.ini')
            delta = config.get_timedelta('RELATIVE', 'sometime')
        import pudb; pudb.set_trace()
        expected = timedelta(weeks=weeks,
                             days=days,                             
                             hours=hours,
                             minutes=minutes,                             
                             seconds=seconds)

    
