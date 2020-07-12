from bookmark.build.strict.indexing import load_index
from bookmark.fetch_text.utils import get_data_as_pages


class Result(object):
    def __init__(self):
        self.search_result_remaining = False
        self.search_pagelen = 10
        self.search_result_len = 0
        self.search_result_pageno = []
        self.search_result_path = []
        self.search_result_display = []
        self.ix = load_index('/home/aaditya/Code/summer_20/bookmark/indexdir', get_data_as_pages)


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