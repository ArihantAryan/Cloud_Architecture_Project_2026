"""
Run this once (and again any time you edit the knowledge base) to build the
Chroma vector store:

    python -m app.build_index
"""

from app.rag_pipeline import build_vector_store
from app import config


def main():
    print(f"Loading documents from: {config.KNOWLEDGE_BASE_DIR}")
    vector_store = build_vector_store(persist=True)
    count = vector_store._collection.count()
    print(f"Vector store built and persisted to: {config.VECTOR_STORE_DIR}")
    print(f"Total chunks indexed: {count}")


if __name__ == "__main__":
    main()
