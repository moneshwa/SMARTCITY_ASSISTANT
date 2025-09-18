from .document_embedder import model  # Reuse the same embedding model
from .pinecone_client import index

def search_documents(query: str, top_k: int = 3):
    """
    Takes a text query, embeds it, and searches Pinecone for the most similar vectors.
    """
    try:
        # 1. Create an embedding for the user's query
        query_embedding = model.encode(query).tolist()

        # 2. Query Pinecone for the top_k most similar vectors
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # 3. Extract the text from the metadata of the results
        search_results = [
            {
                "text": match['metadata']['text'],
                "score": match['score']
            }
            for match in results['matches']
        ]
        
        return search_results
    
    except Exception as e:
        print(f"An error occurred during search: {e}")
        return []
