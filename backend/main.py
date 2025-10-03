from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
import os
import random
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/todoapp")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class TodoDB(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, default="")
    completed = Column(Boolean, default=False)

# Pydantic Models
class TodoCreate(BaseModel):
    title: str
    description: str = ""

class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    
    class Config:
        orm_mode = True

# Chat Models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Note: Tables are now managed by Liquibase migrations
# Base.metadata.create_all(bind=engine) - Removed in favor of Liquibase

# FastAPI app
app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/todos", response_model=List[Todo])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoDB).all()
    return todos

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoDB(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

@app.post("/chat", response_model=ChatResponse)
def chat(message: ChatMessage):
    """
    Chat endpoint that provides AI assistant responses.
    This is a stubbed implementation using keyword matching.
    In a real implementation, this would call an actual LLM API.
    """
    user_message = message.message
    user_lower = user_message.lower()
    
    if "hello" in user_lower or "hi" in user_lower:
        responses = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! Nice to meet you. What's on your mind?"
        ]
    elif "how are you" in user_lower:
        responses = [
            "I'm doing great, thank you for asking! How about you?",
            "I'm functioning well! How can I assist you today?"
        ]
    elif "thank" in user_lower:
        responses = [
            "You're welcome! Is there anything else I can help with?",
            "Happy to help! Let me know if you need anything else."
        ]
    elif "bye" in user_lower or "goodbye" in user_lower:
        responses = [
            "Goodbye! Have a great day!",
            "See you later! Feel free to come back anytime."
        ]
    elif "help" in user_lower:
        responses = [
            "I'm here to help! You can ask me questions about the Proto Stack application, or just chat with me.",
            "I can help with various topics. What would you like to know?"
        ]
    else:
        responses = [
            f"That's an interesting point about '{user_message}'. Tell me more!",
            f"I understand you mentioned '{user_message}'. Can you elaborate?",
            "That's a great question! In a full implementation, I'd provide a detailed response.",
            "Interesting! I'd love to help with that. This is a demo chatbot, so my responses are limited.",
        ]
    
    return ChatResponse(response=random.choice(responses))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)