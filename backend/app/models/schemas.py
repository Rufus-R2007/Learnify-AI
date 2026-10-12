"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Message(BaseModel):
    """Single message in conversation"""
    id: str
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str
    timestamp: datetime
    conceptsUsed: Optional[List[str]] = None


class ChatRequest(BaseModel):
    """Request body for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=1000)
    context: Optional[List[Message]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is artificial intelligence?",
                "context": []
            }
        }


class ChatResponse(BaseModel):
    """Response body for chat endpoint"""
    response: str
    conceptsUsed: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Artificial Intelligence is...",
                "conceptsUsed": ["Knowledge Representation", "Search Algorithm"],
                "confidence": 0.85
            }
        }


class AIUnit(BaseModel):
    """AI syllabus unit representation"""
    id: int
    name: str
    concepts: List[str]
    implemented: bool = False
