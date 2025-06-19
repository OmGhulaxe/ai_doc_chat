
from unstructured.partition.auto import partition
from typing import List

def parse_document(path: str) -> List[str]:
    """
    Parses the file at `path` using unstructured.io and returns a list of text chunks.
    """
    elements = partition(filename=path)
    texts = [el.text.strip() for el in elements if hasattr(el, "text") and el.text]
    return [text for text in texts if text.strip()]
