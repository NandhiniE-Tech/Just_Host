# bbh.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from RetrieverPrompt import get_answer
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base  # Import from your database file
from models import ChatHistory  # Import from your models file
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        db.close()

# Input and output models for validation
class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    response: str

# Define the main chat endpoint with database integration
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Log the incoming request
        logger.info(f"Received chat request: {request.user_input}")
        
        # Get start time
        start_time = datetime.utcnow()
        
        # Call the existing retrieval function
        chatbot_response = get_answer(request.user_input)
        
        # Get end time
        end_time = datetime.utcnow()
        
        # Create chat entry
        chat_entry = ChatHistory(
            user_input=request.user_input,
            bot_response=chatbot_response,
            query_start_time=start_time,
            response_time=end_time,
            session_id="12345",  # You might want to generate this dynamically
            context_length=len(request.user_input),
            response_length=len(chatbot_response),
            confidence_score=100,
            language="ta",  # Set to Tamil since it's a Tamil chatbot
            model_version="1.0"
        )
        
        # Save to database
        try:
            db.add(chat_entry)
            db.commit()
            logger.info("Successfully saved chat to database")
            db.refresh(chat_entry)
        except Exception as db_error:
            db.rollback()
            logger.error(f"Database commit error: {str(db_error)}")
            raise HTTPException(status_code=500, detail="Failed to save chat to database")
        
        return ChatResponse(response=chatbot_response)
        
    except Exception as e:
        logger.error(f"General error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint with database check
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "error", "database": "disconnected"}