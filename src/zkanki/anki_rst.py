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

def rst_to_anki_note(rst):

    html = publish_parts(rst, writer_name='html')['html_body']
    soup = BeautifulSoup(html, 'html.parser')

    textobj = soup.find(id='text')
    for cloze in textobj.find_all('em'):
        try:
            cloze.replace_with('{{'+cloze['class'][0]+'::'+cloze.string+'}}')
        except KeyError:
            pass # Not a cloze deletion
    textobj.h1.decompose()
    text = ''.join(str(x) for x in textobj.contents)

    extraobj = soup.find(id='extra')
    extraobj.details.summary.decompose()
    extra = ''.join(str(x) for x in extraobj.details.contents)

    footer = soup.find(class_='footer')
    tagtup = [f for f in footer.stripped_strings]
    tags = tagtup[1].split()

    return AnkiNote(fields = {'Text': text, 'Extra': extra}, tags=tags)
                
