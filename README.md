# Task2_AI_Web: Search Engine

Constructs a simple search engine with four components:
- crawler
- index
- query parser and search algorithm
- user frontend


## Structure
```
Task2_AI_Web/
├── requirements.txt           # Contains necessary 
├── crawler.py                 # Bootstrap: venv setup, dependency install, launches wizard.py
├── app.py                     # Main app containing search engine
│
├── index/                     # 

```


## Crawler
Given a start URL, this crawler crawls all reachable HTML pages on a single server without following links on the pages. 
We create an index dictionary, where each keyword is mapped to the URLs. The user is then asked for search terms and gets a list of links to and the amount of pages containing all of the keywords.
