from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

DB_PATH = "chroma_db"

def retrieve_rules(query, k=3):
    embeddings = OllamaEmbeddings(
        model="embeddinggemma",
        base_url="http://localhost:11434"
    )

    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    results = db.similarity_search(query, k=k)

    print("\n🔍 Retrieved Rules:\n")
    for i, r in enumerate(results, 1):
        print(f"Result {i}")
        print(f"Row: {r.metadata['row']}")
        print(f"Source: {r.metadata['source']}")
        print(f"Text: {r.page_content}\n")

    return results
