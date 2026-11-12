import faiss
import numpy as np


def create_vector_database(chunks, embeddings):

    if len(chunks) == 0:
        raise ValueError("No chunks available.")

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    if embeddings.ndim != 2:
        raise ValueError("Embeddings must be a 2D array.")

    if embeddings.shape[0] != len(chunks):
        raise ValueError("Chunks and embeddings count do not match.")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


def search_vectors(index, query_embedding, top_k=3):

    if index.ntotal == 0:
        raise ValueError("Vector database is empty.")

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    ).reshape(1, -1)

    if query_embedding.shape[1] != index.d:
        raise ValueError("Query embedding dimension does not match.")

    top_k = min(top_k, index.ntotal)

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    return distances[0], indices[0]
