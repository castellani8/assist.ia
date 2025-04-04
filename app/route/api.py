from fastapi import APIRouter, Request
from app.services.gemini import get_gemini_response
import os
from pydantic import BaseModel

router = APIRouter()

class AskRequest(BaseModel):
    instructions: str = os.getenv("DEFAULT_INSTRUCTIONS")
    question: str

@router.post("/api/ask")
def read_root(request: AskRequest):
    instructions = request.instructions
    prompt = request.question
    response = get_gemini_response(instructions+"\n\n"+prompt)
    return {"response": response}