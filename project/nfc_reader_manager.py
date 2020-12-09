from smartcard.CardConnectionDecorator import CardConnectionDecorator
from smartcard.System import readers

from project.exception.exception import NoNfcReaderException


class NfcReadersManager(object):
    def __init__(self):
        # type: () -> None
        self.readers = readers()  # type: readers
        self.reader = None

        if not self.readers:
            raise NoNfcReaderException()

    def set_connection(self, reader_number_in_list):
        # type: (int) -> None
        self.reader = self.readers[reader_number_in_list].createConnection()

    def get_readers(self):
        # type: () -> readers
        return self.readers

    def set_readers(self):
        # type: () -> None
        self.readers = readers()

    def get_reader(self):
        # type: () -> CardConnectionDecorator
        return self.reader

    def set_reader(self, reader):
        # type: (CardConnectionDecorator) -> None
        self.reader = reader
