from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import random
import uuid

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./quizzes.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Models
class Quiz(Base):
    __tablename__ = "quizzes"
    quiz_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    questions = Column(JSON)

Base.metadata.create_all(bind=engine)

# Load questions from question.json
with open("questions.json", "r") as file:
    questions = json.load(file)

class QuizResponse(BaseModel):
    quiz_id: str
    user_id: str
    questions: list

@app.post("/quiz/", response_model=QuizResponse)
def create_quiz(user_id: str):
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    db = SessionLocal()
    existing_quiz = db.query(Quiz).filter(Quiz.user_id == user_id).first()
    if existing_quiz:
        db.close()
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
    db.close()
    
    return {
        "quiz_id": quiz_id,
        "user_id": user_id,
        "questions": selected_questions
    }

@app.post("/quiz/{quiz_id}/commit")
# commit and return the number of correct answers
def commit_quiz(quiz_id: str, answers: dict):
    db = SessionLocal()
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        db.close()
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    correct_answers = 0
    for question in quiz.questions:
        if question["id"] in answers and answers[question["id"]] == question["answer"]:
            correct_answers += 1
    
    db.close()
    return {
        "quiz_id": quiz.quiz_id,
        "user_id": quiz.user_id,
        "correct_answers": correct_answers
    }

@app.head("/quiz/{quiz_id}")
def check_quiz_exists(quiz_id: str):
    db = SessionLocal()
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    db.close()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"quiz_id": quiz.quiz_id}

@app.get("/quiz/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: str):
    db = SessionLocal()
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    db.close()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {
        "quiz_id": quiz.quiz_id,
        "user_id": quiz.user_id,
        "questions": quiz.questions
    }

@app.post("/quizzes/{quiz_id}/verify")
def verify_quiz(quiz_id: str, answers: dict):
    db = SessionLocal()
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    db.close()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    correct_answers = 0
    for question in quiz.questions:
        if question["id"] in answers and answers[question["id"]] == question["answer"]:
            correct_answers += 1
    
    return {
        "quiz_id": quiz.quiz_id,
        "user_id": quiz.user_id,
        "questions": quiz.questions,
        "correct_answers": correct_answers
    }