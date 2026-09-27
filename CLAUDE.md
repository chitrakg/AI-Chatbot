# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
source .venv/bin/activate
python main.py
```

The first run builds `./chroma_db` from documents in `./docs/`. Subsequent runs detect the non-empty directory and load the persisted store directly, skipping re-indexing.

To force a full re-index, delete the store before running:

```bash
rm -rf ./chroma_db && python main.py
```

## Environment Setup

Create a `.env` file with:

```
LLAMA_MODEL_PATH=/path/to/your/model.gguf   # required — any llama-cpp-compatible .gguf model
CHUNK_SIZE=500                               # optional
CHUNK_OVERLAP=50                             # optional
```

Install dependencies:

```bash
pip install -r requirements.txt
```

`scipy==1.13.1` is pinned to avoid a binary incompatibility on macOS Darwin 27 (see commit `cbbd97b`).

## Architecture

A local RAG pipeline with three stages orchestrated by `main.py`:

**1. Document loading (`src/loader.py`)**

`load_documents(doc_dir)` iterates `./docs/` and dispatches per file extension: `.pdf` → `PyPDFLoader`, `.md` → `UnstructuredMarkdownLoader`, `.txt`/`.text` → `TextLoader`. Unsupported extensions are silently skipped with a warning. Returns a flat list of LangChain `Document` objects.

**2. Indexing (`src/indexer.py`)**

`build_vectorstore(documents)` splits documents using `RecursiveCharacterTextSplitter` (defaults: `CHUNK_SIZE=500`, `CHUNK_OVERLAP=50`, both overridable via `.env`), embeds chunks with `SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")`, and persists to `./chroma_db/` via LangChain's `Chroma` wrapper.

When `main.py` loads an existing store it re-creates the `Chroma` object directly (bypassing `build_vectorstore`) using the same embedding function. The embedding model must therefore stay consistent between indexing and querying runs.

**3. Chat loop (`src/chat.py`)**

`make_qa_chain(vector_store)` builds a `RetrievalQA` chain (`chain_type="stuff"`) backed by a `LlamaCpp` instance (`n_ctx=2048`, `n_threads=4`, `temperature=0.1`). `ask_loop(qa_chain)` runs an interactive prompt that prints the answer and the top-3 source document paths per query.

**Key dependency versions:** LangChain `>=0.0.262` (pre-v0.1 API — uses `langchain.llms`, `langchain.chains`, `langchain.vectorstores`, `langchain.embeddings` directly), `llama-cpp-python>=0.1.86`, ChromaDB `>=0.4.3`.

## Known Issues in the Source

- **`src/indexer.py`** — the import block and `load_dotenv()` / `CHUNK_SIZE` / `CHUNK_OVERLAP` assignments are duplicated; the second block shadows the first. Safe to deduplicate.
- **`src/loader.py`** — line 1 contains a stray markdown heading (`### 4. \`src/loader.py\``) that is literal file content, not a comment. It is harmless but should be removed.
- **`src/try.ipynb`** — exploratory scratch notebook, not part of the pipeline.
