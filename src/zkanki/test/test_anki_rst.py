import unittest, argparse, sys
from anki_rst import *
from ankiconnector import *


class TestAnkiRST(unittest.TestCase):

    def setUp(self):

        self.assertNotIn('ZkankiTestDeck', invoke('deckNames'))
        invoke('createDeck', deck='ZkankiTestDeck')

    def tearDown(self):

        invoke('deleteDecks', decks=['ZkankiTestDeck'], cardsToo=True)
        self.assertNotIn('ZkankiTestDeck', invoke('deckNames'))

    def testAnkiNote(self):
        nid = invoke('addNote', note=AnkiNote())
        invoke('guiBrowse', query='nid:'+str(nid))
        evaluation = raw_input('Inspect Anki guiBrowser.'
                               'p for pass, other for fail: ')
        self.assertEqual(evaluation, 'p', msg=evaluation)

if __name__ == '__main__':
    unittest.main()

