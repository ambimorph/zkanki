import yaml, os
from anki_rst import *
from ankiconnector import *

class Kasten:
    """
    The Kasten is a directory that will hard link to files
    considered in the Kasten with names being the Anki ID
    """
    def __init__(self, *args, **kwargs):
        # Sets up a directory for the Kasten

        self.kasten_path = kwargs.get('kasten_path', self.getDirFromConfig)
        try:
            os.mkdir(self.kasten_path)
        except OSError:
            pass

    def getDirFromConfig(self):
        with open('../../config.yml') as f:
            self.kasten_path = os.path.join(os.path.expanduser('~'),
                                                yaml.load(f)['kasten_path'])

    def delete_kasten(self):

        for z in [os.path.join(self.kasten_path, name)
                  for name in os.listdir(self.kasten_path)]:
            os.remove(z)
        os.rmdir(self.kasten_path)

    def get_anki_note_ID(self, fullpath):
        # Finds the identical file (by inode) in the Kasten, if there is one
        if os.path.dirname(fullpath) == self.kasten_path:
            if os.path.exists(fullpath):
                return int(os.path.splitext(os.path.basename(fullpath))[0])
            else:
                return
        
        zettel = [os.path.join(self.kasten_path,name)
                  for name in os.listdir(self.kasten_path)]
        try:
            links = [z for z in zettel if os.path.samefile(fullpath, z)]
        except OSError:
            return
        if len(links) > 1: raise ValueError('Duplicate notes.')
        try:
            return links[0]
        except IndexError:
            return

    def file_in_kasten(self, fname):
        return self.get_anki_note_ID(fname) is not None

    def new_file(self, **kwargs):

        anki_note = AnkiNote(**kwargs)
        nid = invoke('addNote', note=anki_note)
        fname = os.path.join(self.kasten_path, str(nid) + '.rst')
        rst_str = str(anki_note_to_rst(anki_note))
        with open(fname, 'w') as f:
            f.write(rst_str)
        assert self.file_in_kasten(fname)
        return os.path.basename(fname)
            
    def add_file_to_kasten(self, fname):
        if self.get_anki_note_ID(fname) is not None:
            raise Exception('File already in Kasten')
        with open(fname, 'r') as f:
            rst = f.read()
        anki_note = rst_to_anki_note(rst)
        nid = invoke('addNote', note=anki_note)
        kasten_filename = str(nid) + '.rst'
        os.link(fname, os.path.join(self.kasten_path, kasten_filename))
        return kasten_filename


    def kasten_to_anki_update(self, kasten_filename):

        with open(os.path.join(self.kasten_path,kasten_filename), 'r') as f:
            rst = f.read()
        anki_note = rst_to_anki_note(rst)
        anki_note['id'] = int(os.path.splitext(os.path.basename(kasten_filename))[0])
        invoke('updateNoteFields', note=anki_note)
