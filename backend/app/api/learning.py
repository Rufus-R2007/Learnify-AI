"""
Phase 4 Learning & Expert Systems API Router (Unit V - Naveen Kumar).
Exposes REST endpoints for:
- Concept 1: Rote Learning (Verified Solution Memory Cache inspection & invalidation)
- Concept 2: Learning by Taking Advice (Feedback submission & reviewer workflow)
- Concept 3: Inductive Learning (Authentic ML intent classifier evaluation metrics)
- Concept 4: Learning by Analogy (Case-Based Reasoning query & similarity guidance)
- Concept 5: Expert Systems (Integrated multi-paradigm architecture overview)
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional, Dict, Any

from app.models.schemas import (
    FeedbackCreateRequest,
    FeedbackReviewRequest,
    FeedbackItem,
    MemoryStatsResponse,
    MLMetricsResponse,
)
from app.database import (
    submit_feedback,
    get_all_feedback,
    get_feedback_by_id,
    review_feedback,
    get_verified_memory,
    invalidate_verified_memory,
    get_memory_stats,
    get_all_memory,
    get_knowledge_history,
)
from app.ml.intent_classifier import intent_classifier
from app.services.analogy_engine import analogy_engine

router = APIRouter(prefix="/learning", tags=["Learning & Expert Systems (Unit V)"])


# --------------------------------------------------------------------------
# Concept 2: Learning by Taking Advice (Human Feedback & Reviewer Workflow)
# --------------------------------------------------------------------------

@router.post("/feedback/", status_code=status.HTTP_201_CREATED)
def submit_student_feedback(payload: FeedbackCreateRequest):
    """
    Learning by Taking Advice: Submit student feedback or suggested correction.
    Feedback is stored in SQLite with status 'PENDING'.
    Only authorized reviewer approval can update authoritative knowledge.
    """
    res = submit_feedback(
        query=payload.query,
        original_answer=payload.original_answer,
        feedback_type=payload.feedback_type,
        comment=payload.comment,
        suggested_correction=payload.suggested_correction,
        target_knowledge_id=payload.target_knowledge_id,
        message_id=payload.message_id,
    )
    return res


@router.get("/feedback/", response_model=List[FeedbackItem])
def list_feedback(status: Optional[str] = Query(None, description="Filter by 'PENDING', 'APPROVED', or 'REJECTED'")):
    """List student feedback submissions for reviewer inspection."""
    records = get_all_feedback(status=status)
    return [FeedbackItem(**r) for r in records]


@router.get("/feedback/{feedback_id}", response_model=FeedbackItem)
def get_single_feedback(feedback_id: str):
    """Retrieve single feedback record by ID."""
    fb = get_feedback_by_id(feedback_id)
    if not fb:
        raise HTTPException(status_code=404, detail=f"Feedback '{feedback_id}' not found.")
    return FeedbackItem(**fb)


@router.post("/feedback/{feedback_id}/review")
def review_student_feedback(feedback_id: str, payload: FeedbackReviewRequest):
    """
    Reviewer Workflow: Approve or reject submitted advice.
    When APPROVED with a suggested correction:
    1. Updates the authoritative knowledge record.
    2. Logs provenance in knowledge_history.
    3. Invalidates affected verified rote memory so subsequent queries reflect updated knowledge.
    """
    try:
        res = review_feedback(
            feedback_id=feedback_id,
            decision=payload.decision,
            reviewer_notes=payload.reviewer_notes or "",
            update_knowledge=payload.update_knowledge,
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/knowledge-history")
def list_knowledge_history(knowledge_id: Optional[str] = None):
    """Audit trail showing provenance of knowledge base updates made via approved advice."""
    return get_knowledge_history(knowledge_id=knowledge_id)


# --------------------------------------------------------------------------
# Concept 1: Rote Learning (Verified Solution Memory Cache)
# --------------------------------------------------------------------------

@router.get("/memory/stats", response_model=MemoryStatsResponse)
def get_verified_memory_stats():
    """Retrieve operational statistics of the Rote Learning verified answer cache."""
    stats = get_memory_stats()
    return MemoryStatsResponse(**stats)


@router.get("/memory/items")
def list_verified_memory():
    """List all verified memory entries currently stored in SQLite."""
    return get_all_memory()


@router.post("/memory/invalidate")
def invalidate_memory(
    scope: Optional[str] = Query(None, description="Scope to invalidate (e.g. 'academic')"),
    source_id: Optional[str] = Query(None, description="Invalidate memory referencing this source ID")
):
    """
    Rote Learning Invalidation: Mark affected memory cache entries invalid
    when underlying knowledge records change.
    """
    count = invalidate_verified_memory(scope=scope, source_id=source_id)
    return {
        "success": True,
        "invalidated_count": count,
        "message": f"Successfully invalidated {count} verified memory entries."
    }


# --------------------------------------------------------------------------
# Concept 3: Inductive Learning (ML Intent Classifier Evaluation & Predictions)
# --------------------------------------------------------------------------

@router.get("/ml-metrics", response_model=MLMetricsResponse)
def get_ml_metrics():
    """
    Retrieve real measured evaluation metrics for the TF-IDF + Logistic Regression
    intent classifier evaluated on held-out test data.
    """
    metrics = intent_classifier.get_metrics()
    return MLMetricsResponse(**metrics)


@router.post("/predict-intent")
def predict_intent(query: str = Query(..., description="Query text to classify")):
    """Run real-time inference through the trained TF-IDF + Logistic Regression intent classifier."""
    return intent_classifier.predict(query)


# --------------------------------------------------------------------------
# Concept 4: Learning by Analogy (Case-Based Reasoning Guidance)
# --------------------------------------------------------------------------

@router.get("/analogies")
def get_analogies(query: str = Query(..., description="Student query to find analogies for")):
    """
    Retrieve similar solved question cases using TF-IDF vectors and Cosine Similarity.
    Enforces safety guards for individualized policy queries.
    """
    return analogy_engine.get_analogy_guidance(query)


# --------------------------------------------------------------------------
# Concept 5: Expert Systems Architecture Overview
# --------------------------------------------------------------------------

@router.get("/expert-system-architecture")
def get_expert_system_architecture():
    """
    Architectural documentation of the integrated Learnify AI Expert System,
    uniting Knowledge Base, Inference Engine, Search Engine, Learning Engine,
    and ProofLens Explanation Facility.
    """
    return {
        "system_name": "Learnify AI Expert Assistant",
        "subsystems": {
            "knowledge_base": {
                "unit": "Units I & III",
                "components": ["Curated Knowledge Records", "Verified Facts (SQLite)", "Declarative Rules", "FAQ Base"]
            },
            "inference_engine": {
                "unit": "Units III & IV",
                "components": [
                    "Data-Driven Forward Chaining",
                    "Goal-Driven Backward Chaining",
                    "First-Order Unification",
                    "SLD Horn Resolution",
                    "Nonmonotonic Exception Overrides",
                    "Bayesian Posterior Reasoning"
                ]
            },
            "search_engine": {
                "unit": "Unit II",
                "components": [
                    "Breadth-First Search (BFS)",
                    "Depth-First Search (DFS)",
                    "Bidirectional Search",
                    "Greedy Best-First Search",
                    "Topological Prerequisite Ordering",
                    "CSP Backtracking Scheduler"
                ]
            },
            "learning_engine": {
                "unit": "Unit V",
                "components": [
                    "Rote Learning (Verified Solution Memory Cache)",
                    "Learning by Taking Advice (Human Feedback Review & Knowledge Updates)",
                    "Inductive Learning (scikit-learn TF-IDF + Logistic Regression Intent Classifier)",
                    "Learning by Analogy (Case-Based Reasoning via Cosine Similarity)"
                ]
            },
            "explanation_facility": {
                "name": "ProofLens",
                "components": [
                    "Step-by-step Trace Generation",
                    "Algorithm Execution Badging",
                    "Audited Latency Measurement",
                    "Knowledge Grounding & Provenance"
                ]
            }
        }
    }
