import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urldefrag, urljoin

from index import update_index

def crawl(root: str, server: str = None, index_dir: str = "indexdir"):
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
                if target not in visited and target not in agenda:  # only add the link to the agenda if it hasn't been visited yet
                    print("Adding ", target)
                    agenda.append(target)           # add the link to the agenda to make sure it gets crawled later
        
        print("Crawling finished. Visited", len(visited), "pages.")
        update_index(soup, url, index_dir)
