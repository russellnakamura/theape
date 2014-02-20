
# python standard library
import copy
import csv

# the ape
from ape import BaseClass
from ape import ApeError


class CsvDictStorage(BaseClass):
    """
    A storage that writes to csv files
    """
    def __init__(self, headers,
                 path=None, storage=None):
        """
        CsvDictStorage constructor

        :param:

         - `path`: path to folder to store output-file in
         - `storage`: file-like object to use instead of creating one from 'path'
         - `headers`: list of column headers in order required
        """
        super(CsvDictStorage, self).__init__()
        self.path = path
        self.headers = headers
        self.storage = storage
        self.writer = None

        if not any((self.path, self.storage)):
            raise ApeError("Path or storage needed.")
        return

    def open(self, filename):
        """
        Opens the filename as a DictWriter

        :param:

         - `filename`: the name of the file to open

        :return: copy of self with open DictWriter as `writer`
        """
        new_writer = copy.copy(self)
        open_file = self.storage.open(filename)
        # DictWriter doesn't like keyword arguments
        new_writer.writer = csv.DictWriter(open_file,
                                         self.headers)

        return new_writer

    def writerow(self, row):
        """
        Writes the row to storage

        :param:

         - `row`: dict whose keys match the headers
        """
        return
        


if __name__ == "__main__":
    import pudb; pudb.set_trace()
    from mock import mock_open, patch
    mocked_file = mock_open()
    headers = 'able baker charley'.split()
    with patch('__builtin__.open', mocked_file, create=True):
        with open('test', 'w') as m:
            writer = csv.DictWriter(m,
                                    headers)
    
