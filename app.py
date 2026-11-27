from crawler import crawl, get_clean_text, search

# ROOT_URL = "https://info.cern.ch/hypertext/WWW"
# SERVER_ADDRESS = "info.cern.ch/hypertext/WWW"
ROOT_URL = "https://mic-lab.de/"
SERVER_ADDRESS = "mic-lab.de"

if __name__ == "__main__":
    index = crawl(ROOT_URL, SERVER_ADDRESS)

    query = input("Enter your search: ")        #get search keywords from user
    query_clean = get_clean_text(query)
    query_keywords = query_clean.split()                      #split the query into individual keywords
    search(query_keywords, index)