### 4. `src/loader.py`

import os
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)

def load_documents(doc_dir: str):
    """Auto‐detect and load all supported docs in a directory."""
    docs = []
    for fn in os.listdir(doc_dir):
        path = os.path.join(doc_dir, fn)
        if fn.lower().endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif fn.lower().endswith(".md"):
            loader = UnstructuredMarkdownLoader(path)
        elif fn.lower().endswith((".txt", ".text")):
            loader = TextLoader(path, encoding="utf8")
        else:
            print(f"⚠️  Skipping unsupported file type: {fn}")
            continue
        docs.extend(loader.load())
    return docs