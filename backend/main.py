"""
Learnify AI - AI-Powered Chatbot for Student Queries
Main FastAPI application entry point with startup database seeding,
CORS middleware, and routers for Chat, ProofLens, and Knowledge Explorer.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, knowledge, pathforge, reasoning, whatif, learning
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
    description="Intelligent Conversational Student-Support Platform powered by Unit I Foundations, Unit II Search & Planning (PathForge), Unit III & IV Knowledge Representation, Symbolic Logic & WhatIf Lab, Unit V Learning & Expert Systems, and ProofLens Tracing.",
    version="4.0.0",
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
app.include_router(reasoning.router, prefix="/api/reasoning", tags=["reasoning"])
app.include_router(whatif.router, prefix="/api/whatif", tags=["whatif"])
app.include_router(learning.router, prefix="/api", tags=["learning"])


@app.get("/")
async def root():
    """Root endpoint with API overview and Phase 4 metadata"""
    return {
        "name": "Learnify AI",
        "description": "AI-Powered Chatbot for Student Queries, Planning, Symbolic Reasoning & Learning Systems",
        "version": "4.0.0",
        "phase": 4,
        "responsible_developers": {
            "Phase 1": "URK25CS1090 — Rufus Samuel R",
            "Phase 2": "URK25CS1063 — Yogith Joy J",
            "Phase 3": "URK25CS1034 — Hiran Antony",
            "Phase 4": "URK25CS1016 — Naveen Kumar"
        },
        "status": "operational",
        "signature_innovations": {
            "ProofLens": "Operational (Full Multi-Paradigm Execution & ML Tracing)",
            "PathForge": "Operational (Search Algorithms & CSP Study Planning)",
            "WhatIf Lab": "Operational (Explainable Logic & Academic Decision Simulator)"
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
            "First-Order Predicate Logic & Terms",
            "Robinson Unification with Occurs-Check",
            "Propositional Resolution & Contradiction Detection",
            "Horn-Clause SLD Resolution Engine",
            "Data-Driven Forward Chaining",
            "Goal-Driven Diagnostic Backward Chaining",
            "Nonmonotonic Exception Reasoning & Overrides",
            "Bayesian Probabilistic Intent Estimation",
            "Rote Learning & Verified Solution Caching",
            "Learning by Taking Advice (Human Feedback & Knowledge Updates)",
            "Inductive Learning (scikit-learn TF-IDF + Logistic Regression Intent Classifier)",
            "Learning by Analogy (Case-Based Reasoning via Cosine Similarity)",
            "Integrated Expert System Architecture",
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
        "phase": 4,
        "database": "sqlite3",
        "features": {
            "chat": "active",
            "prooflens": "active",
            "knowledge_explorer": "active",
            "pathforge": "active",
            "whatif_lab": "active",
            "symbolic_reasoning": "active",
            "learning_engine": "active",
            "intent_classifier": "active",
            "rote_memory": "active",
            "case_based_analogy": "active",
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
