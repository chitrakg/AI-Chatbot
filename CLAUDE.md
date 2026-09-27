# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
# Activate the virtual environment first
source .venv/bin/activate

# Run the chatbot (loads docs, builds/loads vector store, starts Q&A loop)
python main.py
```

The first run builds `./chroma_db` from documents in `./docs`. Subsequent runs reuse the persisted store.

## Environment Setup

Copy `.env` and set the required variable:

```
LLAMA_MODEL_PATH=/path/to/your/model.gguf   # local llama-cpp-compatible model
CHUNK_SIZE=500                               # optional override
CHUNK_OVERLAP=50                             # optional override
```

Install dependencies into the existing `.venv`:

```bash
pip install -r requirements.txt
```

## Architecture

This is a local RAG (Retrieval-Augmented Generation) pipeline with three stages wired together in `main.py`:

1. **Document loading** (`src/loader.py`) — scans `./docs/` and dispatches to LangChain loaders by extension (`.pdf` → `PyPDFLoader`, `.md` → `UnstructuredMarkdownLoader`, `.txt` → `TextLoader`).

2. **Indexing** (`src/indexer.py`) — splits documents with `RecursiveCharacterTextSplitter`, embeds chunks with `SentenceTransformerEmbeddings` (`all-MiniLM-L6-v2`), and persists to a local ChromaDB store at `./chroma_db/`. Chunk size and overlap are controlled by `.env`.

3. **Chat loop** (`src/chat.py`) — builds a LangChain `RetrievalQA` chain backed by a local `LlamaCpp` model (path from `LLAMA_MODEL_PATH`), then runs an interactive input loop that prints answers and the top-3 source chunks.

**Key dependency versions:** LangChain `>=0.0.262` (pre-v0.1 API), `llama-cpp-python` for local inference, ChromaDB `>=0.4.3` for vector storage.

## Notes

- `chroma_db/` is `.gitignore`d — delete it to force a full re-index on next run.
- `src/indexer.py` currently has duplicated imports and two `load_dotenv()` / `CHUNK_SIZE` assignments — the second block shadows the first.
- `src/loader.py` has a stray markdown heading (`### 4. \`src/loader.py\``) at line 1 that is part of the file content.
- The notebook `src/try.ipynb` is exploratory scratch space.
