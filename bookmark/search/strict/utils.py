from whoosh.qparser import QueryParser


class SearchTextCommand:
    def __init__(self, text: str, pagenum: int, pagelen: int = 10):
        self.text = text
        self.pagenum = pagenum
        self.pagelen = pagelen

    def __call__(self, data):
        with data.ix.searcher() as searcher:
            query = QueryParser("content", data.ix.schema).parse(self.text)
            pages = searcher.search_page(query, self.pagenum, self.pagelen)
            data.remaining = pages.scored_length() < pages.total
            data.len = 0
            data.pageno.clear()
            data.path.clear()
            data.keywords.clear()
            data.description.clear()
            data.display.clear()
            for i, hit in enumerate(pages.results):
                data.pageno.append(str(hit.get('pageno') + 1))
                data.path.append(hit.get('path'))
                data.keywords.append(hit.get('keywords'))
                data.description.append(hit.get('description'))
                data.display.append('\n\n\n>\n\n\n')
                data.len += 1