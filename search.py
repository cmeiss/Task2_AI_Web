from typing import List
from whoosh import index
from whoosh.qparser import QueryParser

def whoosh_search(query_keywords: List[str], index_dir: str = "indexdir"):
    ix = index.open_dir(index_dir)

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_keywords)
        results = searcher.search(query)
        print(results)
        print("Found", len(results), "pages containing the keyword(s).")