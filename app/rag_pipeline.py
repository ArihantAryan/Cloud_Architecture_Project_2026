from pathlib import Path
from typing import List

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app import config


def _get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)


def load_and_chunk_documents(source_dir: Path = config.KNOWLEDGE_BASE_DIR) -> List[Document]:
    loader = DirectoryLoader(str(source_dir), glob="**/*.md", loader_cls=TextLoader)
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(raw_docs)
    return chunks


def build_vector_store(persist: bool = True) -> Chroma:
    chunks = load_and_chunk_documents()
    embeddings = _get_embeddings()

    persist_directory = str(config.VECTOR_STORE_DIR) if persist else None
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    if persist:
        vector_store.persist()
    return vector_store


def load_vector_store() -> Chroma:
    
    if not config.VECTOR_STORE_DIR.exists():
        raise FileNotFoundError(
            f"No vector store found at {config.VECTOR_STORE_DIR}. "
            
        )
    embeddings = _get_embeddings()
    return Chroma(persist_directory=str(config.VECTOR_STORE_DIR), embedding_function=embeddings)


def retrieve(query: str, vector_store: Chroma, k: int = config.RETRIEVAL_TOP_K) -> List[Document]:
    
    return vector_store.similarity_search(query, k=k)


def format_context(chunks: List[Document]) -> str:
    formatted = []
    for i, chunk in enumerate(chunks, start=1):
        source = Path(chunk.metadata.get("source", "unknown")).name
        formatted.append(f"[Source {i}: {source}]\n{chunk.page_content}")
    return "\n\n".join(formatted)
