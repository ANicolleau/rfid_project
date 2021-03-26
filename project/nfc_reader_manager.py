from smartcard.CardConnectionDecorator import CardConnectionDecorator
from smartcard.System import readers
from typing import Optional, List
from exception.exception import NoNfcReaderException
from smartcard.util import toHexString


class NfcReadersManager(object):
    def __init__(self):
        # type: () -> None
        self.readers = readers()  # type: readers
        self.reader = None  # type: Optional[CardConnectionDecorator]
        self.card_atr = []  # type: List

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

    def dump_card(self):
        self.card_atr = self.reader.getATR()
        print(u'Your card ATR is : %s' % self.card_atr)

    def paste_on_card(self):
        print(u'ATR saved in card')
        return self.reader.transmit(toHexString(self.card_atr))
