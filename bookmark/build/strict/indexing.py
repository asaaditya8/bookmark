from functools import partial
from typing import Callable

import textacy
from tqdm import tqdm

from whoosh.index import create_in, open_dir, FileIndex
from whoosh.fields import *


def create_schema() -> Schema:
    return Schema(pageno=NUMERIC(stored=True), path=ID(stored=True), content=TEXT, keywords=STORED, description=STORED)


def create_new_index(indexdir : str) -> FileIndex:
    return create_in(indexdir, create_schema())


def build_index(ix: FileIndex, data_gen: Callable) -> None:
    writer = ix.writer()
    for path, pageno, text, keywords, description in tqdm(data_gen()):
        writer.add_document(pageno=pageno, path=path,
                            content=text, keywords=', '.join(keywords),
                            description=' '.join(description))
    writer.commit()


def load_index(indexdir : str, data_gen: Callable):
    try:
        ix = open_dir(indexdir)
    except:
        ix = create_new_index(indexdir)
        en = textacy.load_spacy_lang('en_core_web_sm')
        build_index(ix, partial(data_gen,
                                lang=en))

    return ix
