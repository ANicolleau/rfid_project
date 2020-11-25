from smartcard.ATR import ATR
from smartcard.util import toHexString
from exception.exception import NoNfcReaderException
from smartcard.System import readers
from smartcard.CardConnectionDecorator import CardConnectionDecorator


class NfcReader(object):
    def __init__(self):
        # type: () -> None
        self.readers = readers()  # type: readers
        if not self.readers:
            raise NoNfcReaderException()

    def get_connection(self, reader_number_in_list):
        # type: (int) -> CardConnectionDecorator
        return self.readers[reader_number_in_list].createConnection()

    def get_readers(self):
        # type: () -> readers
        return self.readers

    def set_readers(self):
        # type: () -> None
        self.readers = readers()

# r = readers()
#
# print(readers())
#
# connection = r[0].createConnection()
# print(connection)
# connection.connect()
#
# atr = ATR([0x3B, 0x9E, 0x95, 0x80, 0x1F, 0xC3, 0x80, 0x31, 0xA0, 0x73,
#            0xBE, 0x21, 0x13, 0x67, 0x29, 0x02, 0x01, 0x01, 0x81,
#            0xCD, 0xB9])
#
# print(atr)
# print('historical bytes: ', toHexString(atr.getHistoricalBytes()))
# print('checksum: ', "0x%X" % atr.getChecksum())
# print('checksum OK: ', atr.checksumOK)
# print('T0  supported: ', atr.isT0Supported())
# print('T1  supported: ', atr.isT1Supported())
# print('T15 supported: ', atr.isT15Supported())
