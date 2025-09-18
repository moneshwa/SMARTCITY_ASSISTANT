from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .pinecone_client import index

# Initialize the sentence transformer model
# This model creates 384-dimensional embeddings.
model = SentenceTransformer('all-MiniLM-L6-v2')

def process_and_embed_document(document_text: str, document_id: str):
    """
    Splits a document, creates embeddings, and upserts them to Pinecone.
    """
    # 1. Split the document into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(document_text)

    # 2. Create numerical embeddings for each chunk
    embeddings = model.encode(chunks).tolist()

    # 3. Prepare vectors in the format Pinecone expects
    vectors = []
    for i, chunk in enumerate(chunks):
        vector = {
            "id": f"{document_id}-{i}",
            "values": embeddings[i],
            "metadata": {"text": chunk, "document_id": document_id}
        }
        vectors.append(vector)
    
    # 4. Upload (upsert) the vectors to the Pinecone index
    if vectors:
        index.upsert(vectors=vectors)
    
    return len(vectors)
