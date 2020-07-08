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
        self.skipTest("")
        nid = invoke('addNote', note=AnkiNote())
        invoke('guiBrowse', query='nid:'+str(nid))
        evaluation = raw_input('Inspect Anki guiBrowser.'
                               'p for pass, other for fail: ')
        self.assertEqual(evaluation, 'p', msg=evaluation)

    def test_rst_to_anki_note(self):

        with open('test/example_file.rst', 'r') as f:
            rst = f.read()

        note = rst_to_anki_note(rst)
        expected = {'fields': {'Text': '\n\n<p>This section is all that will show in {{c1::Anki}} as the query\nand must contain at least one {{c2::cloze deletion}},\nrepresented with {{c3::reST emphasis}} tags labelled as <em>ci</em>.</p>\n<p>In terms of a Zettel,\nI see it as a concise {{c4::summary}}.</p>\n', 'Extra': '<p>The other fields are folded in the "See More".</p>\n<p>Links can be made throughout this section.\nIf a link refers to a file that is an Anki note\nit will have the form <tt class="docutils literal">`nid1234567890123 <span class="pre">&lt;filename&gt;`_</span></tt>\nwhich renders:\n<a class="reference external" href="filename">nid1234567890123</a></p>\n<p>There can also be footnotes\nLorem ipsum <a class="footnote-reference" href="#f1" id="id1">[1]</a> dolor sit amet ... <a class="footnote-reference" href="#f2" id="id2">[2]</a>.</p>\n<p class="rubric">Footnotes</p>\n<table class="docutils footnote" frame="void" id="f1" rules="none">\n<colgroup><col class="label"/><col/></colgroup>\n<tbody valign="top">\n<tr><td class="label"><a class="fn-backref" href="#id1">[1]</a></td><td>Text of the first footnote.</td></tr>\n</tbody>\n</table>\n<table class="docutils footnote" frame="void" id="f2" rules="none">\n<colgroup><col class="label"/><col/></colgroup>\n<tbody valign="top">\n<tr><td class="label"><a class="fn-backref" href="#id2">[2]</a></td><td>Text of the second footnote.</td></tr>\n</tbody>\n</table>\n'}, 'modelName': 'Zkanki-cloze', 'deckName': 'ZkankiTestDeck', 'tags': [u'test,', u'zkanki']}
        self.assertDictEqual(expected, note, note)

if __name__ == '__main__':
    unittest.main()

