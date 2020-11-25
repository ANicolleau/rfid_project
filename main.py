from nfc_reader import NfcReader
from exception.exception import NoNfcReaderException
from log.logger import logger
import optparse

contributors = ['Antoine Nicolleau']
parser = optparse.OptionParser

try:
    print(u'Welcome to our NFC Reader Application.\n\n'
          u'Before continue, check if your NFC Reader is connected to your computer. '
          u'Press Enter to continue')
    input()
    nfc_reader = NfcReader()
    readers = nfc_reader.get_readers()
    if len(readers) > 1:
        selected_reader = None
        print(u'We found more than one NFC reader connected to your computer :')
        for reader_id, reader_name in enumerate(readers):
            print('%d : %s' % (reader_id, reader_name))
        print(u'Please choose the NFC reader you want to use by entering its id')

        while not isinstance(selected_reader, int):
            try:
                selected_reader = int(input())
            except ValueError:
                selected_reader = None
                logger.warning(u'It\'s not a valid input. Please choose a number in list')
            if selected_reader and selected_reader > len(readers) - 1:
                selected_reader = None
                logger.warning(
                    u'It\'s not a valid input cause your entry is greater than the size of the list'
                    u'. Please choose a number in list.')
    else:
        selected_reader = 0

    nfc_reader.get_connection(selected_reader)

except NoNfcReaderException:
    logger.error('Aucun Lecteur NFC trouvé')
