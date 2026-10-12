"""
Chat API endpoints for Learnify AI
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.ai_service import ai_service
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message and return AI-generated response
    
    Args:
        request: ChatRequest containing user message and optional context
        
    Returns:
        ChatResponse with AI-generated answer, concepts used, and confidence score
    """
    try:
        logger.info(f"Processing query: {request.message[:50]}...")
        
        # Convert context to list of dicts if present
        context = None
        if request.context:
            context = [msg.model_dump() for msg in request.context]
        
        # Process query using AI service
        response_text, concepts_used, confidence = ai_service.process_query(
            request.message,
            context
        )
        
        logger.info(f"Generated response with {len(concepts_used)} concepts")
        
        return ChatResponse(
            response=response_text,
            conceptsUsed=concepts_used,
            confidence=confidence
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@router.get("/concepts")
async def get_ai_concepts():
    """
    Get list of AI concepts that will be implemented
    
    Returns:
        Dictionary with units and their concepts
    """
    return {
        "units": [
            {
                "id": 1,
                "name": "Introduction and Knowledge Representation",
                "concepts": [
                    "AI Definition and History",
                    "Problem Characteristics",
                    "Production Systems",
                    "Knowledge Representation (Semantic Networks, Frames, Ontologies)"
                ],
                "implemented": False
            },
            {
                "id": 2,
                "name": "Search Algorithms",
                "concepts": [
                    "State Space Search",
                    "Uninformed Search (BFS, DFS, DLS, IDS)",
                    "Informed Search (Best-First, A*, Hill Climbing)",
                    "Adversarial Search (Minimax, Alpha-Beta Pruning)",
                    "Constraint Satisfaction Problems"
                ],
                "implemented": False
            },
            {
                "id": 3,
                "name": "Logic and Reasoning",
                "concepts": [
                    "Propositional Logic",
                    "First-Order Logic (Predicate Calculus)",
                    "Inference Rules (Modus Ponens, Resolution)",
                    "Forward and Backward Chaining",
                    "Unification"
                ],
                "implemented": False
            },
            {
                "id": 4,
                "name": "Rule-Based Systems",
                "concepts": [
                    "Production Rules",
                    "Conflict Resolution Strategies",
                    "Rete Algorithm",
                    "Truth Maintenance Systems"
                ],
                "implemented": False
            },
            {
                "id": 5,
                "name": "Expert Systems and Advanced Topics",
                "concepts": [
                    "Expert System Architecture",
                    "Knowledge Acquisition",
                    "Inference Engine Design",
                    "Uncertainty Handling (Bayesian, Fuzzy Logic)",
                    "Machine Learning Integration"
                ],
                "implemented": False
            }
        ]
    }
