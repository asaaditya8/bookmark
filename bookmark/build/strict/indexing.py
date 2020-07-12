from typing import Callable

from whoosh.index import create_in, open_dir, FileIndex
from whoosh.fields import *


def create_schema() -> Schema:
    return Schema(pageno=NUMERIC(stored=True), path=ID(stored=True), content=TEXT)


def create_new_index(indexdir : str) -> FileIndex:
    return create_in(indexdir, create_schema())


def build_index(ix: FileIndex, data_gen: Callable) -> None:
    writer = ix.writer()
    for path, pageno, text in data_gen():
        writer.add_document(pageno=pageno, path=path,
                            content=text)
    writer.commit()


def load_index(indexdir : str, data_gen: Callable):
    try:
        ix = open_dir(indexdir)
    except:
        ix = create_new_index(indexdir)
        build_index(ix, data_gen)

    return ix
