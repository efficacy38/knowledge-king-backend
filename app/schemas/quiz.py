from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QuizResponse(BaseModel):
    quiz_id: str
    user_id: str
    questions: list

class QuizVerifyResponse(BaseModel):
    quiz_id: str
    questions: list
    correct_answers: int

class TransactionData(BaseModel):
    tx_hash: str
    user_addr: str
