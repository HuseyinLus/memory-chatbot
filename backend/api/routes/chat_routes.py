from fastapi import APIRouter
from pydantic import BaseModel
from core.ai_core import ask

router = APIRouter(prefix="/chat", tags=["Chat"])

class Message(BaseModel):
    question: str
    thread_id: int = 1


@router.post("/ask")
def ask_to_bot(message: Message):
    answer = ask(message.question,message.thread_id)
    return {"question": message.question,"answer": answer}

