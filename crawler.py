import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urldefrag, urljoin

from index import build_index, update_index
# NOTE: macht es Sinn, den Crawler als Objekt zu bauen?


def print_results(visited, index):
    print("Crawling finished. Visited", len(visited), "pages.")
    print("Index contains", len(index), "keywords.")
    print("Sample index entries:")
    for keyword in list(index.keys())[:3]:  # print the first keyword and its associated URLs
        print(f"{keyword}: {index[keyword]}")

def crawl(root: str, server: str = None, index_dir: str = "indexdir"):
    # TODO: broke sth here, crawling takes longer and re-visits
    agenda = [root] # pages that need to be crawled
    visited = set() # pages that have already been crawled
    if not server:
        server = root.split("/")[2]     # the server that is being crawled -- works well but takes very long because it finds a lot of pages

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
        # okay, thought about it again, target should be appended to agenda, so it should be crawled later 
        # -- something not right, does not seem to work
        update_index(soup, target, index_dir)
        #print_results(visited, index)
