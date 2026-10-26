"""
PathForge API endpoints for Learnify AI (Phase 2 - Unit II).
Exposes REST endpoints for:
- Topic retrieval and curriculum knowledge graph visualization
- Topological learning path planning with known topic exclusion
- Multi-algorithm execution and educational comparison (BFS, Bidirectional, Greedy Best-First, DFS)
- Constraint-satisfaction based study schedule generation with backtracking
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.services.pathforge_service import pathforge_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class PathRequest(BaseModel):
    goal_topic_id: str = Field(..., description="Target learning goal ID, e.g., 'topic-machine-learning'")
    known_topic_ids: Optional[List[str]] = Field(default_factory=list, description="List of topic IDs already mastered")
    start_topic_id: Optional[str] = Field(None, description="Optional starting node for single-path search")
    algorithm: Optional[str] = Field(default="bfs", description="Search algorithm: 'bfs', 'bidirectional', 'best_first', or 'dfs'")


class CompareRequest(BaseModel):
    start_topic_id: str = Field(..., description="Start topic ID")
    goal_topic_id: str = Field(..., description="Target goal topic ID")


class ScheduleRequest(BaseModel):
    goal_topic_id: str = Field(..., description="Target learning goal ID")
    known_topic_ids: Optional[List[str]] = Field(default_factory=list, description="Mastered topics to exclude")
    available_days: List[str] = Field(
        default=["Monday", "Wednesday", "Friday"],
        description="Available days of the week for study"
    )
    max_daily_hours: int = Field(default=2, ge=1, le=12, description="Maximum hours permitted per day")
    preferred_session_hours: int = Field(default=1, ge=1, le=4, description="Preferred duration for study blocks")
    planning_weeks: int = Field(default=2, ge=1, le=8, description="Horizon in weeks")


@router.get("/topics")
async def get_all_topics():
    """Retrieve all available curriculum topics with prerequisite lists, unit, and metadata."""
    try:
        topics = pathforge_service.get_topics()
        return {"total": len(topics), "topics": topics}
    except Exception as e:
        logger.error(f"Error retrieving topics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving topics: {str(e)}")


@router.get("/topics/{topic_id}")
async def get_topic_by_id(topic_id: str):
    """Retrieve detailed information and dependencies for a single topic."""
    topic = pathforge_service.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found.")
    return topic


@router.get("/graph")
async def get_graph():
    """Retrieve node and directed edge data formatted for interactive graph visualization."""
    try:
        return pathforge_service.get_graph_visualization_data()
    except Exception as e:
        logger.error(f"Error generating graph data: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating graph data: {str(e)}")


@router.post("/path")
async def generate_path(request: PathRequest):
    """
    Generate complete topological learning plan and optional directed search route.
    Returns ordered topics, completed topics, ProofLens execution trace, and route search.
    """
    try:
        result = pathforge_service.plan_learning_journey(
            goal_topic_id=request.goal_topic_id,
            known_topic_ids=request.known_topic_ids,
            start_topic_id=request.start_topic_id,
            algorithm=request.algorithm or "bfs",
        )
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to plan learning path"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating path: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating path: {str(e)}")


@router.post("/compare")
async def compare_algorithms(request: CompareRequest):
    """
    Execute and compare BFS, Bidirectional Search, Greedy Best-First Search, and DFS
    between the exact same start and goal topics.
    """
    try:
        result = pathforge_service.compare_algorithms(
            start_topic_id=request.start_topic_id,
            goal_topic_id=request.goal_topic_id,
        )
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Comparison failed"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing algorithms: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error comparing algorithms: {str(e)}")


@router.post("/schedule")
async def schedule_study(request: ScheduleRequest):
    """
    Solve Constraint Satisfaction Problem (CSP) using Backtracking Search
    to generate an academic study schedule respecting user constraints.
    """
    try:
        prefs_dict = {
            "available_days": request.available_days,
            "max_daily_hours": request.max_daily_hours,
            "preferred_session_hours": request.preferred_session_hours,
            "planning_weeks": request.planning_weeks,
        }
        result = pathforge_service.schedule_study_plan(
            goal_topic_id=request.goal_topic_id,
            known_topic_ids=request.known_topic_ids,
            preferences_dict=prefs_dict,
        )
        return result
    except Exception as e:
        logger.error(f"Error creating schedule: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error creating schedule: {str(e)}")
