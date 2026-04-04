import os
import json
from pathlib import Path
from typing import List, Tuple

# ChromaDB for local vector storage — fully offline
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("⚠️  ChromaDB not found. RAG disabled. Install with: pip install chromadb")

DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / ".chromadb"
COLLECTION_NAME = "eduvoice_curriculum"

_client = None
_collection = None


def get_collection():
    """Initialize and return ChromaDB collection."""
    global _client, _collection
    
    if not CHROMA_AVAILABLE:
        return None
    
    if _collection is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        
        # Use a lightweight sentence transformer for embeddings — offline
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"}
        )
    
    return _collection


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks for better retrieval.
    
    Args:
        text: Full document text
        chunk_size: Characters per chunk
        overlap: Overlapping characters between chunks
    
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def index_documents():
    """
    Index all documents in the docs/ folder into ChromaDB.
    Call this once when new documents are added.
    """
    collection = get_collection()
    if collection is None:
        print("RAG not available.")
        return
    
    DOCS_DIR.mkdir(exist_ok=True)
    doc_files = list(DOCS_DIR.glob("*.txt")) + list(DOCS_DIR.glob("*.md"))
    
    if not doc_files:
        print(f"No documents found in {DOCS_DIR}. Add .txt or .md curriculum files.")
        return
    
    print(f"Indexing {len(doc_files)} document(s)...")
    
    all_chunks = []
    all_ids = []
    all_metadata = []
    
    for doc_path in doc_files:
        text = doc_path.read_text(encoding="utf-8", errors="ignore")
        chunks = chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_path.stem}_{i}"
            all_chunks.append(chunk)
            all_ids.append(chunk_id)
            all_metadata.append({"source": doc_path.name, "chunk": i})
    
    # Upsert in batches
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        collection.upsert(
            documents=all_chunks[i:i+batch_size],
            ids=all_ids[i:i+batch_size],
            metadatas=all_metadata[i:i+batch_size]
        )
    
    print(f"✅ Indexed {len(all_chunks)} chunks from {len(doc_files)} documents.")


def retrieve(query: str, n_results: int = 3) -> str:
    """
    Retrieve relevant curriculum context for a query.
    
    Args:
        query: The child's question
        n_results: Number of chunks to retrieve
    
    Returns:
        Concatenated relevant context string, or empty string if none
    """
    collection = get_collection()
    if collection is None or collection.count() == 0:
        return ""
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, collection.count())
        )
        
        if not results["documents"] or not results["documents"][0]:
            return ""
        
        context_parts = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            context_parts.append(f"[From {meta['source']}]\n{doc}")
        
        return "\n\n".join(context_parts)
    
    except Exception as e:
        print(f"RAG retrieval error: {e}")
        return ""


def augment_prompt(question: str) -> str:
    """
    Augment a question with relevant curriculum context.
    
    Args:
        question: The child's question
    
    Returns:
        Augmented prompt with context injected, or original question if no context
    """
    context = retrieve(question)
    
    if not context:
        return question
    
    return f"""Use the following curriculum context to help answer the question accurately.
If the context is not relevant, just answer from your general knowledge.

CURRICULUM CONTEXT:
{context}

QUESTION: {question}"""


if __name__ == "__main__":
    print("Indexing docs folder...")
    index_documents()
    
    test_query = "What is photosynthesis?"
    print(f"\nTesting retrieval for: '{test_query}'")
    context = retrieve(test_query)
    print(f"Retrieved context:\n{context if context else 'No context found (add docs to docs/ folder)'}")
