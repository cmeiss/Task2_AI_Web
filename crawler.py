import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urldefrag, urljoin
from typing import List
# NOTE: macht es Sinn, den Crawler als Objekt zu bauen?

# TODO: not sure if this makes sense to do -- right now I apply it to both website text and query 
def get_clean_text(text):
    """Clean text to get sensible keywords without punctuation"""
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    return clean_text

def print_results(visited, index):
    print("Crawling finished. Visited", len(visited), "pages.")
    print("Index contains", len(index), "keywords.")
    print("Sample index entries:")
    for keyword in list(index.keys())[:3]:  # print the first keyword and its associated URLs
        print(f"{keyword}: {index[keyword]}")

# TODO: only add to list if it is not already in there
def build_index(index, soup, url):
    text = soup.get_text(separator=" ", strip=True)  # get the text content of the page
    clean_text = get_clean_text(text)
    for keyword in clean_text.split():
        if keyword not in index:
            index[keyword] = []
        index[keyword].append(url)
    return index

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


def crawl(root: str, server: str = None):
    agenda = [root] # pages that need to be crawled
    visited = set() # pages that have already been crawled
    if not server:
        server = root.split("/")[2]     # the server that is being crawled -- works well but takes very long because it finds a lot of pages

    index = {}
    while agenda:
        url = agenda.pop()
        if url in visited: 
            continue

        visited.add(url)

        # Get the page
        r = requests.get(
            url,
            headers={"User-Agent": "AIWebPageCheck/1.0"},
            timeout=15,
        )
        # Check the status code and skip if not 200 OK or not HTML
        print("Get", r.status_code, r.url)
        if r.status_code !=200 or "text/html" not in r.headers.get("Content-Type", ""):
            continue

        soup = BeautifulSoup(r.content, "html.parser")
        for link in soup.select("a[href]"):
            # Get the absolute URL of the link, and remove any fragment (the part after #)
            target, _ = urldefrag(urljoin(r.url, link["href"]))
            if (target.startswith(f"https://{server}/")):       #check that link is on the same server
                print("Found ", target)
                if target not in visited:  # only add the link to the agenda if it hasn't been visited yet
                    agenda.append(target)           # add the link to the agenda to make sure it gets crawled later

            # NOTE: in original, we called build_index with url and not with target -- why?
            index = build_index(index, soup, target)
            print_results(visited, index)

        return index
