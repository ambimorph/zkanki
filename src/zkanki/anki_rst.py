from docutils.core import publish_parts
from bs4 import BeautifulSoup

class AnkiNote(dict):
    def __init__(self, *args, **kwargs):
        self['deckName'] = kwargs.get('deckName', 'ZkankiTestDeck')
        self['modelName'] = kwargs.get('modelName', 'Zkanki-cloze')
        self['fields'] = kwargs.get('fields',
                                    {'Text': 'Text should contain one {{c1:cloze}}, '
                                     'Extra "Something extra", '
                                     'and the tag is "test".',
                                     'Extra': 'Something extra'})
        self['tags'] = kwargs.get('tags', ['test'])

        
                    
                
