from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.vectorstore.document_embedder import process_and_embed_document
from app.vectorstore.document_retriever import search_documents

router = APIRouter()

@router.post("/upload-document", tags=["Vector Search"])
async def upload_document(file: UploadFile = File(...)):
    """
    Accepts a .txt file, processes it, and stores its embeddings in Pinecone.
    """
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Only .txt files are allowed.")

    try:
        # Read the file content
        contents = await file.read()
        document_text = contents.decode("utf-8")
        
        # Use the filename as the document's unique ID
        document_id = file.filename
        
        # Call the service to process and embed the document
        num_vectors = process_and_embed_document(document_text, document_id)
        
        return {
            "status": "success",
            "message": f"Successfully processed '{document_id}' and created {num_vectors} vectors."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

class SearchRequest(BaseModel):
    query: str

@router.post("/search-documents", tags=["Vector Search"])
async def search_documents_endpoint(request: SearchRequest):
    """
    Accepts a text query and returns the most relevant document chunks from Pinecone.
    """
    try:
        results = search_documents(request.query)
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
