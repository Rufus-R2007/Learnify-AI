"""
Learnify AI - AI-Powered Chatbot for Student Queries
Main FastAPI application entry point with startup database seeding,
CORS middleware, and routers for Chat, ProofLens, and Knowledge Explorer.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, knowledge, pathforge
from app.core.config import settings
from app.database import init_db, seed_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("learnify")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler: initializes SQLite schema and seeds knowledge base."""
    logger.info("Initializing Learnify AI database...")
    init_db()
    seed_db()
    logger.info("Database initialized and seeded successfully.")
    yield
    logger.info("Shutting down Learnify AI...")


# Create FastAPI app
app = FastAPI(
    title="Learnify AI API",
    description="Intelligent Conversational Student-Support Platform powered by Unit I Foundations, Unit II Search & Planning (PathForge), Transparent ProofLens Tracing, and SQLite Knowledge Base.",
    version="2.0.0",
    lifespan=lifespan,
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
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])
app.include_router(pathforge.router, prefix="/api/pathforge", tags=["pathforge"])


@app.get("/")
async def root():
    """Root endpoint with API overview and Phase 2 metadata"""
    return {
        "name": "Learnify AI",
        "description": "AI-Powered Chatbot for Student Queries and Intelligent Planning",
        "version": "2.0.0",
        "phase": 2,
        "responsible_developers": {
            "Phase 1": "URK25CS1090 — Rufus Samuel R",
            "Phase 2": "URK25CS1063 — Yogith Joy J"
        },
        "status": "operational",
        "signature_innovations": {
            "ProofLens": "Operational (Phase 1 & 2 Live Tracing)",
            "PathForge": "Operational (Phase 2 - Search Algorithms & Study Planning)",
            "WhatIf Lab": "Prepared interfaces (Phase 3)"
        },
        "ai_capabilities": [
            "Perception & Input Normalization",
            "Model-Based Context & Anaphora Tracking",
            "Goal-Oriented Action Selection",
            "Knowledge Representation & Retrieval",
            "Uninformed Graph Search (BFS & DFS)",
            "Bidirectional Search (Meeting Detection)",
            "Informed Greedy Best-First Search (Heuristic)",
            "Topological Dependency Ordering & Prerequisite Closure",
            "Constraint Satisfaction & Backtracking Scheduler",
            "Truthful Uncertainty Handling",
            "ProofLens Measured Execution Tracing"
        ]
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint for automated status verification."""
    return {
        "status": "healthy",
        "service": "Learnify AI Backend",
        "phase": 2,
        "database": "sqlite3",
        "features": {
            "chat": "active",
            "prooflens": "active",
            "knowledge_explorer": "active",
            "pathforge": "active",
            "syllabus_tracker": "active"
        }
    }


if __name__ == "__main__":
    import uvicorn
    # Initialize DB synchronously if run as script
    init_db()
    seed_db()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
