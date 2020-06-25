
import unittest
import json

"""
There is a "manual" component to the tests
because I have to import from Anki and check for errors


CrowdAnki gives a dict including 'notes' which is a list.
Notes are dicts:
[u'tags',
 u'fields',
 u'__type__',
 u'note_model_uuid',
 u'flags',
 u'guid',
 u'data']
fields are a list

"""

class TestCrowdAnkiModify(unittest.TestCase):

    def setUp(self):

        with open ('TestDeck/deck.json', 'r') as f:
            self.orig = json.loads(f.read())

    def testImportNoChange(self):

        with open ('/Users/amber/zkanki/src/test/TestDeck01/deck.json', 'w') as f:
            json_str = json.dumps(self.orig, default=lambda o: o.__dict__, sort_keys=True, indent=2)
            f.write(json_str)

    def testImportTextChange(self):

        self.orig['notes'][1]['fields'][3] += ' or other'
        with open ('/Users/amber/zkanki/src/test/TestDeck01/deck.json', 'w') as f:
            json_str = json.dumps(self.orig, default=lambda o: o.__dict__, sort_keys=True, indent=2)
            f.write(json_str)

    def testImportRemoveTag(self):

        self.orig['notes'][0]['tags'].remove('questions')
        with open ('/Users/amber/zkanki/src/test/TestDeck01/deck.json', 'w') as f:
            json_str = json.dumps(self.orig, default=lambda o: o.__dict__, sort_keys=True, indent=2)
            f.write(json_str)
        

if __name__ == '__main__':
    unittest.main()
