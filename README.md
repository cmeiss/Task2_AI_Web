# Task2_AI_Web: Search Engine

Constructs a simple search engine with four components:
- crawler
- index
- query parser and search algorithm
- user frontend


## Structure
```
Task2_AI_Web/
├── requirements.txt           
├── crawler.py                 # Contains crawler
├── index.py                   # Uses whoosh to update the index given a url
├── search.py                  # Contains query parser and search algorithm
├── app.py                     # Main entry point containing search engine
│
├── indexdir/                  # Directory for index files created by whoosh 

```


## Crawler
Given a start URL, this crawler crawls all reachable HTML pages on a single server without following links on the pages. 
We create an index dictionary, where each keyword is mapped to the URLs. The user is then asked for search terms and gets a list of links to and the amount of pages containing all of the keywords.

## Index

## Search

## App
