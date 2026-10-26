"""
Learnify AI Search & Planning Module (Phase 2 - Unit II).
Manual implementations of Classical AI Search & Planning Algorithms:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Bidirectional Search
- Greedy Best-First Search
- Prerequisite Closure & Topological Planning
- Constraint Satisfaction & Backtracking Scheduler
"""

from app.search.graph import LearningGraph, TopicNode
from app.search.bfs import breadth_first_search, BFSResult
from app.search.dfs import depth_first_search, DFSResult
from app.search.bidirectional import bidirectional_search, BidirectionalResult
from app.search.best_first import greedy_best_first_search, BestFirstResult
from app.search.prerequisites import (
    generate_learning_plan,
    get_prerequisite_closure,
    topological_sort,
    LearningPlan,
    PlannedTopicItem,
)
from app.search.constraints import TimeSlot, SessionVariable, StudyPreferences
from app.search.scheduler import solve_study_schedule, ScheduleResult, ScheduledSession

__all__ = [
    "LearningGraph",
    "TopicNode",
    "breadth_first_search",
    "BFSResult",
    "depth_first_search",
    "DFSResult",
    "bidirectional_search",
    "BidirectionalResult",
    "greedy_best_first_search",
    "BestFirstResult",
    "generate_learning_plan",
    "get_prerequisite_closure",
    "topological_sort",
    "LearningPlan",
    "PlannedTopicItem",
    "TimeSlot",
    "SessionVariable",
    "StudyPreferences",
    "solve_study_schedule",
    "ScheduleResult",
    "ScheduledSession",
]
