#!/bin/python
import optparse
import sys
import inquirer
from smartcard.Exceptions import NoCardException
from smartcard.util import toHexString

from exception.exception import NoNfcReaderException
from log.logger import logger
from nfc_reader_manager import NfcReadersManager

parser = optparse.OptionParser

print(u'Welcome to our NFC Reader Application.\n\n'
      u'Before continue, check if your NFC Reader is connected to your computer. '
      u'Press Enter to continue')
input()

try:
    nfc_reader_manager = NfcReadersManager()
except NoNfcReaderException:
    logger.error(u'Aucun Lecteur NFC trouvé')
    sys.exit(1)

readers = nfc_reader_manager.get_readers()
readers.append('lolo')
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
user_input = None
while user_input != 'EXIT':
    nfc_reader_manager.set_connection(selected_reader)
    nfc_reader = nfc_reader_manager.get_reader()
    print(u'If your badge is on your NFC reader, press enter to continue')
    input()

    card_is_connected = False
    while not card_is_connected:
        try:
            nfc_reader.connect()
            card_is_connected = True
        except NoCardException:
            logger.error(u'No NFC chip found, press ENTER to retry')
            input()

    card_ATR = nfc_reader.getATR()
    card_ATR_hexadecimal = toHexString(nfc_reader.getATR())
    print(u'card_ATR : %s' % card_ATR)
    print(u'card_ATR_hexadecimal : %s' % card_ATR_hexadecimal)

    # TODO Faire les 5 points cités dessous
    options = [
        inquirer.List(u'user_choose', message=u'What do you want to do ?',
                      choices=[
                          u'1 : Dump of your NFC chip',
                          u'2 : Copy on your NFC chip',
                          u'3 : Read your NFC chip',
                          u'4 : Write on your NFC chip',
                          u'5 : Exit'
                      ], carousel=False)
    ]
    answer = inquirer.prompt(options)['user_choose']
    print(u'Answer : %s' % answer)
    if u'1' in answer:
        print(u'You have choose : Dump of your NFC chip')
        print(nfc_reader_manager.dump_card())
    elif u'2' in answer:
        print(u'You have choose : Copy on your NFC chip')
    elif u'3' in answer:
        print(u'You have choose : Read your NFC chip')
    elif u'4' in answer:
        print(u'You have choose : Write on your NFC chip')
    elif u'5' in answer:
        print(u'Exiting..')
    print(u'ATR of your badge : %s' % nfc_reader.getATR())
