from bookmark.build.strict.indexing import load_index
from bookmark.fetch_text.utils import get_data_as_pages

import json
from functools import partial

configs = None
with open('config.json', 'r') as f:
    configs = json.load(f)

FONT_SIZE_IN_PIXELS = configs['FONT_SIZE_IN_PIXELS']
FONT_PATH_PRIMARY = configs['FONT_PATH_PRIMARY']


class Result(object):
    def __init__(self):
        self.remaining = False
        self.pagelen = 10
        self.len = 0
        self.pageno = []
        self.path = []
        self.keywords = []
        self.description = []
        self.display = []
        self.ix = load_index(configs['INDEX_DIR'], partial(get_data_as_pages,
                                                           data_dir=configs['PDF_DIR'],
                                                           desc_size=configs['DESC_LEN'],
                                                           desc_threshold=configs['DESC_THRESHOLD']))


class ResultView(object):
    def __init__(self):
        self.list_changed = False
        self.selection_idx = -1


class SearchView(object):
    def __init__(self):
        self.text_val = ""
        self.text_changed = ""
        self.check1 = True
        self.check1_clicked = False