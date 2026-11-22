import requests
from bs4 import BeautifulSoup
from urllib.parse import urldefrag, urljoin

#-------------------crawler itself-------------------
# where to start crawling
root = "https://info.cern.ch/hypertext/WWW"

agenda = [root]                 # pages that need to be crawled

visited = set()                 # pages that have already been crawled

#server = root.split("/")[2]     # the server that is being crawled
server = "info.cern.ch/hypertext/WWW"   #line above works well but takes very long because it finds a lot of pages

index = {}                       # dictionary to store the URLs for each keyword

while agenda:
    url = agenda.pop()

    if url in visited:      #skip URLs that have already been visited
        continue

    visited.add(url)       # add current URL to the visited set

    # Get the page
    r = requests.get(
        url,
        headers={"User-Agent": "AIWebPageCheck/1.0"},
        timeout=15,
    )

    # Check the status code and skip if not 200 OK or not HTML
    print("Get", r.status_code, r.url)
    if r.status_code != 200 or "text/html" not in r.headers.get("Content-Type", ""):
        continue

    # Parse the page and find all links
    soup = BeautifulSoup(r.content, "html.parser")
    for link in soup.select("a[href]"):

        # Get the absolute URL of the link, and remove any fragment (the part after #)
        target, _ = urldefrag(urljoin(r.url, link["href"]))
        if (target.startswith(f"https://{server}/")):       #check that link is on the same server
            print("Found ", target)
            if target not in visited:  # only add the link to the agenda if it hasn't been visited yet
                agenda.append(target)           # add the link to the agenda to make sure it gets crawled later

    #----------get text contents and save as index -----------------
    text = soup.get_text(separator=" ", strip=True)  # get the text content of the page
    for keyword in text.lower().split():
        if keyword not in index:
            index[keyword] = []
        index[keyword].append(url)


#--------------------print overview of results-------------------
print("Crawling finished. Visited", len(visited), "pages.")
print("Index contains", len(index), "keywords.")
print("Sample index entries:")
for keyword in list(index.keys())[:1]:  # print the first keyword and its associated URLs
    print(f"{keyword}: {index[keyword]}")


#--------------------search pages for a user's query-------------------
query = input("Enter your search: ").lower()        #get search keywords from user
query_keywords = query.split()                      #split the query into individual keywords

if len(query_keywords) > 1:         #check the number of keywords to determine whether intersection needs to be used to find all pages containing all keywords
    print("Searching for pages containing all keywords:", query_keywords)
    results = set(index.get(query_keywords[0], []))  # get set of URLs for the first keyword
    for keyword in query_keywords[1:]:
        results.intersection_update(index.get(keyword, []))  # for each additional keyword, update the results so that only URLs containing all keywords are retained
else:
    print("Searching for pages containing the keyword:", query_keywords[0])
    results = set(index.get(query_keywords[0], []))  # get set of URLs for the single keyword, no need to look at intersections

print("Found", len(results), "pages containing the keyword(s).")

