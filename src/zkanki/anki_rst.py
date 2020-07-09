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

def rst_to_soup(rst):

    html = publish_parts(rst, writer_name='html')['html_body']
    return BeautifulSoup(html, 'html.parser')

def soup_text_to_cloze(soup_text):

    for cloze in soup_text.find_all('em'):
        try:
            cloze.replace_with('{{'+cloze['class'][0]+'::'+cloze.string+'}}')
        except KeyError:
            pass # Not a cloze deletion
    soup_text.h1.decompose()
    return ''.join(str(x) for x in soup_text.contents)

def soup_extra_to_extra(soup_extra):

    soup_extra.details.summary.decompose()
    return ''.join(str(x) for x in soup_extra.details.contents)
    
def soup_footer_to_tags(soup_footer):

    tagtup = [f for f in soup_footer.stripped_strings]
    assert tagtup[0] == 'tags:'
    return tagtup[1].split()
    
    
def rst_to_anki_note(rst):

    soup = rst_to_soup(rst)

    text = soup_text_to_cloze(soup.find(id='text'))
    extra = soup_extra_to_extra(soup.find(id='extra'))
    tags = soup_footer_to_tags(soup.find(class_='footer'))

    return AnkiNote(fields = {'Text': text, 'Extra': extra}, tags=tags)
                
