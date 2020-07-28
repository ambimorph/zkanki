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
        
    def test_add_file_to_kasten(self):

        self.skipTest('')

        file_name = self.kasten.add_file_to_kasten('test/example_file.rst')
        nid = os.path.splitext(os.path.basename(file_name))[0]
        invoke('guiBrowse', query='nid:'+ nid)
        evaluation = raw_input('Inspect Anki guiBrowser.'
                               'p for pass, other for fail: ')
        self.assertEqual(evaluation, 'p', msg=evaluation)

    def test_kasten_to_anki_update(self):

        self.skipTest('')

        new_file_name = self.kasten.new_file(fields={'Text': 'Some text',
                                                     'Extra': 'e',},
                                                     tags=['a','b','c'])
        self.assertTrue(self.kasten.file_in_kasten(os.path.join(self.kasten.kasten_path, new_file_name)), new_file_name)
        
        with open(os.path.join(self.kasten.kasten_path, new_file_name), 'r+') as f:
            rst = f.read()
            f.seek(0)
            f.truncate()
            f.write(rst.replace('Some text', 'Some :c1:`other` text'))
        self.kasten.kasten_to_anki_update(new_file_name)
        
        nid = os.path.splitext(os.path.basename(new_file_name))[0]
        invoke('guiBrowse', query='nid:'+ nid)
        evaluation = raw_input('Inspect Anki guiBrowser.'
                               'p for pass, other for fail: ')
        self.assertEqual(evaluation, 'p', msg=evaluation)

    def test_anki_to_kasten(self):

        anki_note = AnkiNote()
        nid = invoke('addNote', note=anki_note)
        kasten_file_name = self.kasten.anki_to_kasten(nid)
        with open(os.path.join(self.kasten.kasten_path, kasten_file_name), 'r') as f:
            file_contents = f.read()
        expected = '.. footer::\n   :tags: test\n\n\n\nText\n----\n\nText should contain one {{c1:cloze}}, Extra "Something extra", and the tag is "test".\n\nExtra\n-----\n\n.. raw:: html\n\n    <details><summary>See More</summary>\n\nSomething extra\n\n.. raw:: html\n\n    </details>'
        self.assertEqual(file_contents, expected, '\n----\n'+repr(file_contents)+'\n----\n')

        

if __name__ == '__main__':
    unittest.main()
