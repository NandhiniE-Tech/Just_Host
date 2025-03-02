from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import ChatHistory
from pydantic import BaseModel
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI App
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Database Dependency with error handling
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        db.close()

# Pydantic Models
class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    response: str

# Chat Endpoint with improved error handling and logging
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Log the incoming request
        logger.info(f"Received chat request: {request.user_input}")
        
        # Simulated Bot Response
        bot_response = f"You said: {request.user_input}"
        
        # Create chat entry
        chat_entry = ChatHistory(
            user_input=request.user_input,
            bot_response=bot_response,
            query_start_time=datetime.utcnow(),
            response_time=datetime.utcnow(),
            session_id="12345",
            context_length=len(request.user_input),
            response_length=len(bot_response),
            confidence_score=100
        )
        
        # Add and commit with explicit error handling
        try:
            db.add(chat_entry)
            db.commit()
            logger.info("Successfully saved chat to database")
            db.refresh(chat_entry)
        except Exception as db_error:
            db.rollback()
            logger.error(f"Database commit error: {str(db_error)}")
            raise HTTPException(status_code=500, detail="Failed to save chat to database")
        
        return ChatResponse(response=bot_response)
        
    except Exception as e:
        logger.error(f"General error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health Check with DB connection test
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "error", "database": "disconnected"}