from fastapi import APIRouter, Request, Header, Depends
import os
from pydantic import BaseModel
from fastapi import HTTPException
from dotenv import load_dotenv
from app.services.ai.rag import query

load_dotenv()

router = APIRouter()

class AskRequest(BaseModel):
    instructions: str = os.getenv("DEFAULT_INSTRUCTIONS")
    question: str

def verify_token(x_token: str = Header(...)):
    if os.getenv("ENABLE_AUTH") == "true":
        if x_token != os.getenv("TOKEN_SECRET"):
            raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/api/ask")
def read_root(request: AskRequest, _=Depends(verify_token)):
    instructions = request.instructions
    prompt = request.question
    response = query(instructions, prompt)
    return {"response": response}