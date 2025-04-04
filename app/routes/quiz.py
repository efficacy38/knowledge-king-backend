from fastapi import APIRouter, HTTPException, Depends, Body
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
    
    existing_quiz = db.query(Quiz).filter(Quiz.user_id == user_id).order_by(Quiz.created_at.desc()).first()

    questions_without_answer = []
    if existing_quiz and existing_quiz.is_completed == "false":
    # remove answer attr from existing_quiz's questions
        if existing_quiz.questions:
            for question in existing_quiz.questions:
                question_without_answer = question.copy()
                question_without_answer.pop("answer", None)
                questions_without_answer.append(question_without_answer)
        
        # If the user already has an incomplete quiz, return it
        # without creating a new one
        return {
            "quiz_id": existing_quiz.quiz_id,
            "user_id": existing_quiz.user_id,
            "questions": questions_without_answer
        }
    
    # Select 10 random questions from the loaded questions
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

@router.head("/{quiz_id}")
def check_quiz_exists(quiz_id: str, db: Session = Depends(get_db)):
    """Check if a quiz is not completed"""
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    print("Quiz is_completed:", quiz.is_completed)
    # if quiz is_completed, return 404
    if quiz and quiz.is_completed == True:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"message": "Quiz not completed"}

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: str, db: Session = Depends(get_db)):
    """Get quiz details"""
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Remove answer attribute from questions
    questions_without_answer = []
    if quiz.questions:
        for question in quiz.questions:
            question_without_answer = question.copy()
            question_without_answer.pop("answer", None)
            questions_without_answer.append(question_without_answer)
    
    return {
        "quiz_id": quiz.quiz_id,
        "user_id": quiz.user_id,
        "questions": questions_without_answer
    }

@router.post("/{quiz_id}/verify", response_model=QuizVerifyResponse)
def verify_quiz(
    quiz_id: str, 
    answers: list[bool] = Body(
        ...,
        example=[True, False, True, True, False, True, False, True, True, False],
        description="List of boolean answers corresponding to the questions"
    ),
    db: Session = Depends(get_db)
):
    """
    Verify answers and return results with questions.
    
    Example request body:
    ```json
    [true, false, true, true, false, true, false, true, true, false]
    ```
    
    Where the values are boolean answers corresponding to the questions.
    """
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if len(answers) != len(quiz.questions):
        raise HTTPException(status_code=400, detail="Number of answers does not match number of questions")
    
    correct_answers = 0
    for idx, question in enumerate(quiz.questions):
        if idx < len(answers) and answers[idx] == question["answer"]:
            correct_answers += 1
    
    # Mark quiz as completed
    quiz.is_completed = True
    # commit changes to the database
    db.commit()
    db.refresh(quiz)
    # print current db's quiz
    print("Current quiz in DB:", quiz)
    # Remove answer attribute from questions
    
    return {
        "quiz_id": quiz.quiz_id,
        "questions": quiz.questions,
        "correct_answers": correct_answers
    }
