from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from database import Base  # Import Base from database.py

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_input = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    query_start_time = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    response_time = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    session_id = Column(String(100))
    context_length = Column(Integer)
    response_length = Column(Integer)
    error_flag = Column(Boolean, default=False)
    error_message = Column(Text)
    source_documents = Column(JSON, nullable=True)
    confidence_score = Column(Integer)
    language = Column(String(50))
    model_version = Column(String(100))
    extra_metadata = Column(JSON, nullable=True)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
