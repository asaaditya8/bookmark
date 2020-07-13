from bookmark.build.strict.indexing import load_index
from bookmark.fetch_text.utils import get_data_as_pages

import json
from functools import partial

configs = None
with open('config.json', 'r') as f:
    configs = json.load(f)


class Result(object):
    def __init__(self):
        self.search_result_remaining = False
        self.search_pagelen = 10
        self.search_result_len = 0
        self.search_result_pageno = []
        self.search_result_path = []
        self.search_result_display = []
        self.ix = load_index(configs['INDEX_DIR'], partial(get_data_as_pages, configs['PDF_DIR']))


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