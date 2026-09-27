import os
from src.loader import load_documents
from src.indexer import build_vectorstore
from src.chat import make_qa_chain, ask_loop

from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

if __name__ == "__main__":
    DOC_DIR = "./docs"
    VECTORSTORE_DIR = "./chroma_db"

    # 1. Load documents
    print("📄 Loading documents…")
    docs = load_documents(DOC_DIR)

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # 2. Build or load vector store using LangChain's Chroma wrapper
    if not os.path.isdir(VECTORSTORE_DIR) or not os.listdir(VECTORSTORE_DIR):
        print("🔨 Building vector store (this may take a minute)…")
        vs = build_vectorstore(docs)
    else:
        print("✅ Loaded existing vector store.")
        vs = Chroma(
            persist_directory=VECTORSTORE_DIR,
            embedding_function=embedding_function
        )

    # 3. Create QA chain & loop
    qa = make_qa_chain(vs)
    ask_loop(qa)