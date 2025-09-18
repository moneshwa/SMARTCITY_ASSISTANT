from fastapi import APIRouter
from pydantic import BaseModel
from ..services.llm_service import ask_llm

# A Pydantic model to define the structure of the request body
# This tells FastAPI to expect a JSON object with a single key "text"
class PolicyRequest(BaseModel):
    text: str

# Create a new router
router = APIRouter()

@router.post("/summarize-policy", tags=["Policy Summarizer"])
async def summarize_policy(request: PolicyRequest):
    """
    Endpoint to summarize a policy text. It receives text and returns an AI-generated summary.
    """
    # We create a specific prompt for the summarization task
    prompt = f"""
    You are a smart city assistant. Please summarize the following policy document in simple, clear language for a citizen.
    Keep it concise and under 100 words.

    Document:
    {request.text}

    Summary:
    """

    # Send the complete prompt to the LLM service
    summary = ask_llm(prompt)

    return {"summary": summary}