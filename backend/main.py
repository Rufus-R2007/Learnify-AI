"""
Learnify AI - AI-Powered Chatbot for Student Queries
Main FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title="Learnify AI API",
    description="AI-Powered Chatbot for Student Queries using Knowledge Representation, Search Algorithms, Logical Reasoning, and Expert Systems",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Learnify AI",
        "description": "AI-Powered Chatbot for Student Queries",
        "version": "0.1.0",
        "status": "operational",
        "ai_capabilities": [
            "Knowledge Representation",
            "Search Algorithms",
            "Logical Reasoning",
            "Rule-Based Inference",
            "Expert Systems"
        ]
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Learnify AI Backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
