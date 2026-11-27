from typing import List
from whoosh import index
from whoosh.qparser import QueryParser

def search(query_keywords: List[str], index):
    """
    Search page for a user's query. 
    Args:
        query_keywords: List of strings, containing the search query
        index: index object
    Returns: list of unique pages containing all of the keywords

    """
    if len(query_keywords) > 1:         #check the number of keywords to determine whether intersection needs to be used to find all pages containing all keywords
        print("Searching for pages containing all keywords:", query_keywords)
        results = set(index.get(query_keywords[0], []))  # get set of URLs for the first keyword
        for keyword in query_keywords[1:]:
            results.intersection_update(index.get(keyword, []))  # for each additional keyword, update the results so that only URLs containing all keywords are retained
    else:
        print("Searching for pages containing the keyword:", query_keywords[0])
        results = set(index.get(query_keywords[0], []))  # get set of URLs for the single keyword, no need to look at intersections
    print(results)
    print("Found", len(results), "pages containing the keyword(s).")
    return results

def whoosh_search(query_keywords: List[str], index_dir: str = "indexdir"):
    ix = index.open_dir(index_dir)

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_keywords)
        results = searcher.search(query)
        print(results)
        print("Found", len(results), "pages containing the keyword(s).")
    #return results