from sqlalchemy import Column, String, JSON
from app.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    quiz_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    questions = Column(JSON)