import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
import chromadb
from chromadb.config import Settings

load_dotenv()

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))



from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

def build_vectorstore(documents):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)

    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # Use LangChain's Chroma wrapper
    vectorstore = Chroma.from_documents(
        chunks,
        embedder,
        persist_directory="./chroma_db"
    )
    return vectorstore