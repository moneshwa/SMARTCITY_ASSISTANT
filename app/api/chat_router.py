from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_service import ask_llm

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

@router.post("/ask", tags=["Chat Assistant"])
async def ask_assistant(request: ChatRequest):
    """
    Receives a prompt from the user and returns a response from the LLM.
    """
    try:
        # We can create a more sophisticated prompt or system message later
        # For now, we'll pass the user's prompt directly to the LLM
        response_text = ask_llm(request.prompt)
        return {"status": "success", "response": response_text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
