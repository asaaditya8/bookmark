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
            data.search_result_len = 0
            data.search_result_pageno.clear()
            data.search_result_path.clear()
            data.search_result_display.clear()
            for i, hit in enumerate(pages.results):
                data.search_result_pageno.append( str(hit.get('pageno') + 1) )
                data.search_result_path.append( hit.get('path') )
                data.search_result_display.append(f"{hit.get('path')}\nPage: {hit.get('pageno')+1}\nDESCRIPTION\n ")
                data.search_result_len += 1