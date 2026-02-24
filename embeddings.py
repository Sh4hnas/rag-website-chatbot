from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_vector_store(text):

    # Split by sentences instead of raw newline
    chunks = text.split(".")
    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 20]

    if len(chunks) == 0:
        raise ValueError("No valid text chunks extracted from website.")

    embeddings = model.encode(chunks)

    embeddings = np.array(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, chunks, model