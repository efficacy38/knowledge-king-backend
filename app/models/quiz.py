from sqlalchemy import Column, String, JSON, DateTime, Boolean
from datetime import datetime
from app.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    quiz_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    questions = Column(JSON)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)