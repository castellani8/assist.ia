from fastapi import APIRouter, Request
from app.services.gemini import get_gemini_response
import os
from pydantic import BaseModel

router = APIRouter()

class AskRequest(BaseModel):
    question: str

@router.post("/api/ask")
def read_root(request: AskRequest):
    instructions = os.getenv("INSTRUCTIONS")
    print(request.question)
    prompt = request.question
    response = get_gemini_response(instructions+"\n\n"+prompt)
    return {"response": response}