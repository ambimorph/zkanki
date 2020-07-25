import unittest
from ankiconnector import *
from kasten import *

class TestKasten(unittest.TestCase):

    def setUp(self):

        self.assertFalse(os.path.exists('.kasten'))
        self.kasten = Kasten(kasten_path='.kasten')
        
        self.assertNotIn('ZkankiTestDeck', invoke('deckNames'))
        invoke('createDeck', deck='ZkankiTestDeck')

    def tearDown(self):

        invoke('deleteDecks', decks=['ZkankiTestDeck'], cardsToo=True)
        self.assertNotIn('ZkankiTestDeck', invoke('deckNames'))

        self.kasten.delete_kasten()

    def test_new_file(self):

        new_file_name = self.kasten.new_file(fields={'Text': 't',
                                                     'Extra': 'e',},
                                                     tags=['a','b','c'])
        self.assertTrue(self.kasten.file_in_kasten(os.path.join(self.kasten.kasten_path, new_file_name)), new_file_name)
        

if __name__ == '__main__':
    unittest.main()
