from sentence_transformers import SentenceTransformer
import faiss
from textwrap import wrap
import numpy as np

class EmbeddingError(Exception):
    """Base exception for embedding-related errors."""
    pass

class ChunkingError(EmbeddingError):
    """Raised when text chunking fails."""
    pass

class VectorStoreError(EmbeddingError):
    """Raised when vector store creation fails."""
    pass

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_vector_store(text):
    """
    Create a FAISS vector store from text content.
    
    Args:
        text: The text content to process
        
    Returns:
        tuple: (index, chunks, model) - FAISS index, text chunks, and embedding model
        
    Raises:
        ChunkingError: If text chunking fails or produces no valid chunks
        VectorStoreError: If vector store creation fails
    """
    try:
        # Validate input
        if not text or not isinstance(text, str):
            raise ChunkingError("Invalid text input: text must be a non-empty string")
        
        if len(text.strip()) < 100:
            raise ChunkingError("Text content is too short to process (minimum 100 characters required)")

        # Split into larger overlapping chunks 
        try:
            raw_chunks = wrap(text, 500)
        except Exception as e:
            raise ChunkingError(f"Failed to split text into chunks: {str(e)}")

        # Filter chunks
        chunks = [chunk.strip() for chunk in raw_chunks if len(chunk.strip()) > 100]

        if len(chunks) == 0:
            raise ChunkingError("No valid text chunks could be extracted. The content may be too short or contain only whitespace.")

        # Create embeddings
        try:
            embeddings = model.encode(chunks)
            embeddings = np.array(embeddings)
        except Exception as e:
            raise VectorStoreError(f"Failed to create embeddings: {str(e)}")

        # Validate embeddings
        if embeddings.shape[0] == 0:
            raise VectorStoreError("Embedding generation produced no results")

        # Create FAISS index
        try:
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)
        except Exception as e:
            raise VectorStoreError(f"Failed to create vector store index: {str(e)}")

        return index, chunks, model
        
    except (ChunkingError, VectorStoreError):
        # Re-raise our custom exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        raise VectorStoreError(f"Unexpected error during vector store creation: {str(e)}")