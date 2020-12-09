import optparse

import inquirer
from smartcard.Exceptions import NoCardException
from smartcard.util import toHexString

from project.exception import NoNfcReaderException
from project.log import logger
from project.nfc_reader_manager import NfcReadersManager

parser = optparse.OptionParser

try:
    print(u'Welcome to our NFC Reader Application.\n\n'
          u'Before continue, check if your NFC Reader is connected to your computer. '
          u'Press Enter to continue')
    input()
    nfc_reader_manager = NfcReadersManager()
    readers = nfc_reader_manager.get_readers()

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

    nfc_reader_manager.set_connection(selected_reader)
    nfc_reader = nfc_reader_manager.get_reader()
    print('If your badge is on your NFC reader, press enter to continue')
    input()

    card_is_connected = False
    while not card_is_connected:
        try:
            nfc_reader.connect()
            card_is_connected = True
        except NoCardException:
            logger.error('No NFC chip found, press ENTER to retry')
            input()
    card_ATR = nfc_reader.getATR()
    card_ATR_hexadecimal = toHexString(nfc_reader.getATR())
    print('card_ATR : %s' % card_ATR)
    print('card_ATR_hexadecimal : %s' % card_ATR_hexadecimal)

    # TODO Faire les 5 points cités dessous
    options = [
        inquirer.List('user_choose', message='What do you want to do ?',
                      choices=[
                          '1 : Dump of your NFC chip',
                          '2 : Copy your NFC chip',
                          '3 : Read your NFC chip',
                          '4 : Write on your NFC chip',
                          '5 : Exit'
                      ], carousel=False)
    ]
    answers = inquirer.prompt(options)
    print(answers)
    print('ATR of your badge : %s' % nfc_reader.getATR())

except NoNfcReaderException:
    logger.error('Aucun Lecteur NFC trouvé')
