import os
from dotenv import load_dotenv
from langchain.llms import LlamaCpp
from langchain.chains import RetrievalQA

load_dotenv()
LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH")

def make_qa_chain(vector_store):
    """Returns a RetrievalQA chain using a local Llama model."""
    llm = LlamaCpp(
        model_path=LLAMA_MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        temperature=0.1,
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True
    )
    return qa

def ask_loop(qa_chain):
    print("\n📝 Enter your question (or 'exit' to quit):")
    while True:
        q = input("→ ")
        if q.lower() in ("exit", "quit"):
            break
        resp = qa_chain(q)
        print("\n📖 Answer:\n", resp["result"])
        # optional: show which chunks it used
        print("\n🗂️  Sources:")
        for doc in resp["source_documents"][:3]:
            print(f" • {doc.metadata.get('source', '<no source>')}")
        print("\n" + "-"*40)