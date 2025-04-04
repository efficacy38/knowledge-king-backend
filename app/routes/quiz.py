from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import json
import random
import uuid
from typing import Dict, Any

from app.database import get_db
from app.models.quiz import Quiz
from app.schemas.quiz import QuizResponse, QuizVerifyResponse

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
    responses={404: {"description": "Quiz not found"}}
)

# Load questions from question.json
try:
    with open("questions.json", "r") as file:
        questions = json.load(file)
except Exception as e:
    questions = []
    print(f"Error loading questions: {e}")

@router.post("/", response_model=QuizResponse)
def create_quiz(user_id: str, db: Session = Depends(get_db)):
    """Create a new quiz for a user"""
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    existing_quiz = db.query(Quiz).filter(Quiz.user_id == user_id).first()
    if existing_quiz:
        return {
            "quiz_id": existing_quiz.quiz_id,
            "user_id": existing_quiz.user_id,
            "questions": existing_quiz.questions
        }
    
    selected_questions = random.sample(questions, min(10, len(questions)))
    quiz_id = str(uuid.uuid4())
    new_quiz = Quiz(quiz_id=quiz_id, user_id=user_id, questions=selected_questions)
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    
    return {
        "quiz_id": quiz_id,
        "user_id": user_id,
        "questions": selected_questions
    }

@router.post("/{quiz_id}/commit")
def commit_quiz(quiz_id: str, answers: Dict[str, bool], db: Session = Depends(get_db)):
    """Submit answers and get the score"""
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    correct_answers = 0
    for question in quiz.questions:
        if str(question["id"]) in answers and answers[str(question["id"])] == question["answer"]:
            correct_answers += 1
    
    return {
        "quiz_id": quiz.quiz_id,
        "user_id": quiz.user_id,
        "correct_answers": correct_answers
    }

@router.head("/{quiz_id}")
def check_quiz_exists(quiz_id: str, db: Session = Depends(get_db)):
    """Check if a quiz exists"""
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"quiz_id": quiz.quiz_id}

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: str, db: Session = Depends(get_db)):
    """Get quiz details"""
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {
        "quiz_id": quiz.quiz_id,
        "user_id": quiz.user_id,
        "questions": quiz.questions
    }

@router.post("/{quiz_id}/verify", response_model=QuizVerifyResponse)
def verify_quiz(quiz_id: str, answers: Dict[str, bool], db: Session = Depends(get_db)):
    """Verify answers and return results with questions"""
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    correct_answers = 0
    for question in quiz.questions:
        if str(question["id"]) in answers and answers[str(question["id"])] == question["answer"]:
            correct_answers += 1
    
    return {
        "quiz_id": quiz.quiz_id,
        "user_id": quiz.user_id,
        "questions": quiz.questions,
        "correct_answers": correct_answers
    }