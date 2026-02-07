from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

DATA_PATH = "data/rules.txt"
DB_PATH = "chroma_db"

def load_rules():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        blocks = f.read().split("\n\n")

    docs = []
    for block in blocks:
        lines = block.strip().split("\n")
        if not lines or not lines[0].startswith("[ROW"):
            continue

        row = lines[0].replace("[ROW:", "").replace("]", "")
        source = lines[1].replace("Source:", "").strip()
        text = " ".join(lines[3:]).strip()

        docs.append(
            Document(
                page_content=text,
                metadata={"row": row, "source": source}
            )
        )

    return docs


def ingest():
    embeddings = OllamaEmbeddings(
        model="embeddinggemma",
        base_url="http://localhost:11434"
    )

    docs = load_rules()

    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    print(f"✅ Ingested {len(docs)} regulatory rules")


if __name__ == "__main__":
    ingest()
