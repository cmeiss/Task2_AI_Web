import os
from whoosh import index
from whoosh.fields import *


def get_schema():
  # TODO: do not know if this is right at all, seems very odd
  return Schema(url=ID(unique=True, stored=True), content=TEXT(stored=True))


def update_index(soup, target_url, index_dir: str = "indexdir"):
    # Create index if it does not already exist, open otherwise
    os.makedirs(index_dir, exist_ok=True)
    if not index.exists_in(index_dir):
        schema = get_schema()
        ix = index.create_in(index_dir, schema)
    else:
        ix = index.open_dir(index_dir)
    writer = ix.writer()

    # Update index
    text = soup.get_text(separator=" ", strip=True)  # get the text content of the page

    writer.add_document(url=target_url, content=text)
    writer.commit()