from crawler import crawl
from search import whoosh_search

# ROOT_URL = "https://info.cern.ch/hypertext/WWW"
# SERVER_ADDRESS = "info.cern.ch/hypertext/WWW"
ROOT_URL = "https://mic-lab.de/"
SERVER_ADDRESS = "mic-lab.de"
INDEX_DIR = "indexdir"

if __name__ == "__main__":
    crawl(ROOT_URL, SERVER_ADDRESS, INDEX_DIR)

    query = input("Enter your search: ")        #get search keywords from user
    whoosh_search(query, INDEX_DIR)