from docutils.core import publish_parts
from bs4 import BeautifulSoup
import re, pypandoc

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

    def hack_newlines(txt):
        """
        For some reason docutils keeps '\n's when parsing
        """
        return txt#.replace('>\n<', '><').replace('\n', '<br>')

    html = publish_parts(rst, writer_name='html')['html_body']
    return BeautifulSoup(hack_newlines(html), 'html.parser')

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
                
class RSTNote():
    def __init__(self, *args, **kwargs):
        self.text = kwargs.get('text', '')
        self.extra = kwargs.get('extra', '')
        self.tags = kwargs.get('tags', [])

    def make_footer(self):
        return '.. footer::\n   :tags: ' + ' '.join(self.tags)

    def make_cloze_roles(self):

        """
        Pandoc *sometimes inserts an escape before my backticks,
        so I'm catching only those escaped backticks 
        that happen in the cloze translations.
        It also randomly inserts newlines,
        which is a dilemma.
        For now I will simply remove them, 
        since the cloze text is intended to be short.
        """

        def clozerepl(matchobj):
            return ':c'+matchobj.group(1)+':`'+matchobj.group(2)+'removeme`'

        t0 = re.sub(r'{{c([0-9]+)::(.+?)}}', clozerepl, self.text)
        clozeIDs = [r[1] for r in set(re.findall('(:)(c[0-9]+)(:)', t0))]
        t1 = pypandoc.convert_text(t0, 'rst', format='html', extra_args=['--wrap=preserve'])
        t2 = re.sub(r'removeme\\*', '', t1)
        text = re.sub('(?<![\n])(\r?\n)(?![\n])', ' ', t2)
        roles = '\n'.join(['.. role:: '+c+'(emphasis)' for c in sorted(clozeIDs)])

        return (roles, text.strip())

    def parse_extra(self):

        """
        We'll deal with isome issues in literals, links, and footnotes,
        and remove the tables pypandoc makes for footnotes
        """

        soup_extra = BeautifulSoup(self.extra, "html.parser")
        if soup_extra.find():

            for literal in soup_extra.find_all('tt'):  
                literal.name = 'pre'
                literal['class'] = 'myliteral'
                #print literal.tag, literal.contents
                #literal.replace_with(soup_extra.new_tag('pre'))
                #print literal.tag, literal.contents

            
            for table in soup_extra.find_all('table'):
                table.insert_after('endtable')
    
            for fn in soup_extra.find_all('a'):
                if fn['class'][0] == u"footnote-reference":
                    fn.replace_with('['+fn['href']+']replacethiswithanunderscore')
            
            for fnt in soup_extra.find_all('table'):
                if fnt['class'] == ["docutils", "footnote"]:
                    fnt.replace_with('<p>.. [#f'+str(fnt.a['href'])[3:]+'] '
                                     + fnt.find_all('td')[1].string+'</p>')
    
            text = "".join(str(x) for x in soup_extra.contents)
            def rubricrepl(matchobj):
                return '.. rubric:: ' + matchobj.group(1)
            text = re.sub(r'<p class="rubric">(\w+)</p>', rubricrepl, text)
            text = pypandoc.convert_text(text, 'rst', format='html', extra_args=['--wrap=preserve'])
            def literalrepl(matchobj):
                return ' ``' + matchobj.group(2) + '`` '
            rexp = re.compile(r'\n\n.. code:: myliteral(\s+)(.+)\n')
            text = re.sub(rexp, literalrepl, text)
            text = text.replace('replacethiswithanunderscore', '_')
            text = text.replace('`__', '`_')
            text = text.replace('\n\nendtable\n', '')
            text = '\n'.join([line.strip() for line in text.splitlines()])
    
            return text
    
        return self.extra

    def __repr__(self):

        return self.make_footer() + '\n\n' + \
            '\n\nText\n----\n\n'.join(self.make_cloze_roles()) + \
            '\n\nExtra\n-----\n\n.. raw:: html\n\n    <details><summary>See More</summary>\n\n' + \
            self.parse_extra() + \
            '\n\n.. raw:: html\n\n    </details>'
            


        
def anki_note_to_rst(anki_note):

    return RSTNote(text=anki_note['fields']['Text'],
                     extra=anki_note['fields']['Extra'],
                     tags=anki_note['tags'])
