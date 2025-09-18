import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "smart-city-assistant")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in the .env file")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

def get_pinecone_index():
    """Initializes and returns the Pinecone index."""
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        # Create the index if it doesn't exist.
        # Dimension 384 is for the 'all-MiniLM-L6-v2' sentence transformer.
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=384, 
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1' # You can change this to your preferred region
            )
        )
    return pc.Index(PINECONE_INDEX_NAME)

# Get the index instance to be used by other modules
index = get_pinecone_index()
