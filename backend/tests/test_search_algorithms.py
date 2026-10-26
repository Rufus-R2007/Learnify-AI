"""
Comprehensive Automated Test Suite for Learnify AI Phase 2:
Search Algorithms, Intelligent Planning & PathForge (Yogith Joy J - URK25CS1063).

Covers all 18 requirements:
1. BFS shortest-path correctness
2. BFS unreachable destination
3. DFS traversal and cycle detection
4. Bidirectional search on directed graphs
5. Bidirectional and BFS shortest-path agreement
6. Greedy Best-First exploration according to heuristic priorities
7. Prerequisite closure across multiple prerequisite branches
8. Correct topological dependency ordering
9. Known completed topics excluded from remaining work
10. Invalid/circular prerequisite data handling
11. Valid constraint-based schedule generation
12. Scheduling with conflicting availability
13. Backtracking that recovers from an invalid initial assignment
14. Impossible schedule handling and honest diagnostic failure
15. Invalid topic identifiers handling
16. PathForge API endpoints (topics, graph, path, compare, schedule)
17. Integration with the existing Learnify AI chatbot
18. Authentic ProofLens search traces and execution metrics
"""

import pytest
from fastapi.testclient import TestClient
import os
import sys

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app
from app.database import init_db, seed_db, get_all_topics, get_topic_by_id
from app.search.graph import LearningGraph, TopicNode
from app.search.bfs import breadth_first_search
from app.search.dfs import depth_first_search
from app.search.bidirectional import bidirectional_search
from app.search.best_first import greedy_best_first_search, compute_heuristic
from app.search.prerequisites import (
    generate_learning_plan,
    get_prerequisite_closure,
    topological_sort,
)
from app.search.constraints import TimeSlot, SessionVariable, StudyPreferences
from app.search.scheduler import solve_study_schedule
from app.services.search_engine import search_engine
from app.services.pathforge_service import pathforge_service


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Initialize database and seed Phase 2 curated knowledge graph."""
    init_db()
    seed_db()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def deterministic_small_graph():
    """
    Deterministic small graph fixture:
    A -> B -> D -> E
    A -> C -> D -> E
    Isolated node: F (no paths to/from F)
    """
    g = LearningGraph()
    for name in ["A", "B", "C", "D", "E", "F"]:
        g.add_node(TopicNode(id=name, name=f"Topic {name}", unit=1, estimated_hours=2))
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    g.add_edge("D", "E")
    return g


@pytest.fixture
def deterministic_cyclic_graph():
    """
    Deterministic graph with circular dependency:
    X -> Y -> Z -> X
    """
    g = LearningGraph()
    for name in ["X", "Y", "Z"]:
        g.add_node(TopicNode(id=name, name=f"Topic {name}", unit=1, estimated_hours=2))
    g.add_edge("X", "Y")
    g.add_edge("Y", "Z")
    g.add_edge("Z", "X")
    return g


# ----------------------------------------------------------------------
# 1. BFS Shortest-Path Correctness
# ----------------------------------------------------------------------
def test_bfs_shortest_path(deterministic_small_graph):
    res = breadth_first_search(deterministic_small_graph, "A", "E")
    assert res.reachable is True
    assert res.edge_count == 3
    assert res.path[0] == "A"
    assert res.path[-1] == "E"
    assert res.path in (["A", "B", "D", "E"], ["A", "C", "D", "E"])
    assert res.explored_count >= 4
    assert res.duration_ms >= 0.0


# ----------------------------------------------------------------------
# 2. BFS Unreachable Destination
# ----------------------------------------------------------------------
def test_bfs_unreachable_destination(deterministic_small_graph):
    res = breadth_first_search(deterministic_small_graph, "A", "F")
    assert res.reachable is False
    assert res.path == []
    assert res.edge_count == 0
    assert "F" not in res.visited_nodes


# ----------------------------------------------------------------------
# 3. DFS Traversal and Cycle Detection
# ----------------------------------------------------------------------
def test_dfs_traversal_and_cycle_detection(deterministic_small_graph, deterministic_cyclic_graph):
    # Traversal on acyclic graph
    res_acyclic = depth_first_search(deterministic_small_graph, "A", "E")
    assert res_acyclic.reachable is True
    assert res_acyclic.has_cycle is False
    assert res_acyclic.cycle is None
    assert res_acyclic.path[0] == "A"
    assert res_acyclic.path[-1] == "E"

    # Cycle detection on cyclic graph
    res_cyclic = depth_first_search(deterministic_cyclic_graph, "X")
    assert res_cyclic.has_cycle is True
    assert res_cyclic.cycle is not None
    assert len(res_cyclic.cycle) >= 3
    # Check that cycle loops back to same start
    assert res_cyclic.cycle[0] == res_cyclic.cycle[-1]


# ----------------------------------------------------------------------
# 4. Bidirectional Search on Directed Graphs
# ----------------------------------------------------------------------
def test_bidirectional_search_directed(deterministic_small_graph):
    res = bidirectional_search(deterministic_small_graph, "A", "E")
    assert res.reachable is True
    assert res.edge_count == 3
    assert res.meeting_node in ("B", "C", "D")
    assert res.path[0] == "A"
    assert res.path[-1] == "E"
    # Reverse directed check: E to A should NOT be reachable because edges are directed A -> ... -> E
    res_reverse = bidirectional_search(deterministic_small_graph, "E", "A")
    assert res_reverse.reachable is False


# ----------------------------------------------------------------------
# 5. Bidirectional and BFS Shortest-Path Agreement
# ----------------------------------------------------------------------
def test_bidirectional_and_bfs_agreement():
    # Test on the live application curriculum graph
    graph = search_engine.get_graph()
    bfs_res = breadth_first_search(graph, "topic-prog-fund", "topic-machine-learning")
    bi_res = bidirectional_search(graph, "topic-prog-fund", "topic-machine-learning")

    assert bfs_res.reachable is True
    assert bi_res.reachable is True
    # Edge count in unweighted graph must match
    assert bi_res.edge_count == bfs_res.edge_count
    assert bi_res.path[0] == bfs_res.path[0] == "topic-prog-fund"
    assert bi_res.path[-1] == bfs_res.path[-1] == "topic-machine-learning"


# ----------------------------------------------------------------------
# 6. Greedy Best-First Exploration via Heuristic Priorities
# ----------------------------------------------------------------------
def test_greedy_best_first_search():
    graph = search_engine.get_graph()
    res = greedy_best_first_search(graph, "topic-prog-fund", "topic-neural-networks")
    assert res.reachable is True
    assert res.path[0] == "topic-prog-fund"
    assert res.path[-1] == "topic-neural-networks"
    assert len(res.calculated_heuristics) > 0
    # Heuristic at target must be 0.0
    target_node = graph.get_node("topic-neural-networks")
    assert compute_heuristic(target_node, target_node) == 0.0


# ----------------------------------------------------------------------
# 7. Prerequisite Closure Across Multiple Branches
# ----------------------------------------------------------------------
def test_prerequisite_closure_multiple_branches():
    graph = search_engine.get_graph()
    closure = get_prerequisite_closure(graph, "topic-machine-learning")

    # Machine learning requires foundations from multiple independent branches:
    # 1. Programming branch: topic-prog-fund, topic-python-basics
    assert "topic-prog-fund" in closure
    assert "topic-python-basics" in closure
    # 2. Math branch: topic-linear-algebra, topic-probability, topic-statistics
    assert "topic-linear-algebra" in closure
    assert "topic-probability" in closure
    assert "topic-statistics" in closure
    # 3. AI search branch: topic-search-bfs-dfs, topic-heuristic-search
    assert "topic-search-bfs-dfs" in closure
    assert "topic-heuristic-search" in closure


# ----------------------------------------------------------------------
# 8. Correct Topological Dependency Ordering
# ----------------------------------------------------------------------
def test_topological_dependency_ordering():
    graph = search_engine.get_graph()
    plan = generate_learning_plan(graph, "topic-neural-networks")
    assert plan.is_valid is True
    assert len(plan.ordered_plan) > 0

    order_map = {item.topic_id: idx for idx, item in enumerate(plan.ordered_plan)}

    # Check that for all pairs (parent, child), parent comes strictly before child
    for item in plan.ordered_plan:
        for prereq in item.prerequisites:
            if prereq in order_map:
                assert order_map[prereq] < order_map[item.topic_id], (
                    f"Topological violation: {prereq} must precede {item.topic_id}"
                )


# ----------------------------------------------------------------------
# 9. Known Completed Topics Excluded from Remaining Work
# ----------------------------------------------------------------------
def test_known_topics_excluded_from_plan():
    graph = search_engine.get_graph()
    known = ["topic-prog-fund", "topic-python-basics", "topic-discrete-math"]
    plan = generate_learning_plan(graph, "topic-neural-networks", known_topic_ids=known)

    assert plan.is_valid is True
    remaining_ids = [item.topic_id for item in plan.ordered_plan]

    # Completed topics must not appear in the remaining study sequence
    for k in known:
        assert k not in remaining_ids
        assert k in plan.completed_topics

    # Remaining topics count must equal total required minus completed
    assert plan.remaining_topics_count == len(plan.all_required_ids) - len(plan.completed_topics)


# ----------------------------------------------------------------------
# 10. Invalid and Circular Prerequisite Data Handling
# ----------------------------------------------------------------------
def test_circular_prerequisite_plan_handling(deterministic_cyclic_graph):
    plan = generate_learning_plan(deterministic_cyclic_graph, "Z")
    assert plan.is_valid is False
    assert plan.has_cycle is True
    assert len(plan.warnings) > 0
    assert any("circular" in w.lower() or "cycle" in w.lower() for w in plan.warnings)


# ----------------------------------------------------------------------
# 11. Valid Constraint-Based Schedule Generation
# ----------------------------------------------------------------------
def test_valid_constraint_schedule_generation():
    graph = search_engine.get_graph()
    plan = generate_learning_plan(
        graph,
        "topic-state-spaces",
        known_topic_ids=["topic-prog-fund", "topic-python-basics", "topic-discrete-math", "topic-ai-foundations"]
    )
    prefs = StudyPreferences(
        available_days=["Monday", "Wednesday", "Friday"],
        max_daily_hours=3,
        preferred_session_hours=1,
        planning_weeks=2,
    )
    res = solve_study_schedule(plan, prefs)
    assert res.is_feasible is True
    assert len(res.sessions) > 0
    assert res.used_capacity_hours <= res.available_capacity_hours

    # Verify no session scheduled on non-available days
    for s in res.sessions:
        assert s.day in prefs.available_days

    # Verify daily hour limit is respected
    daily_totals = {}
    for s in res.sessions:
        daily_totals[s.day_index] = daily_totals.get(s.day_index, 0) + s.duration_hours
    for day_idx, total in daily_totals.items():
        assert total <= prefs.max_daily_hours


# ----------------------------------------------------------------------
# 12. Scheduling with Conflicting Availability / Busy Slots
# ----------------------------------------------------------------------
def test_schedule_respects_busy_slots():
    graph = search_engine.get_graph()
    plan = generate_learning_plan(graph, "topic-problem-solving", known_topic_ids=["topic-prog-fund"])
    prefs = StudyPreferences(
        available_days=["Monday", "Tuesday"],
        max_daily_hours=2,
        preferred_session_hours=1,
        busy_slots=[{"day": "Monday", "slot_index": 0}],
        planning_weeks=2,
    )
    res = solve_study_schedule(plan, prefs)
    if res.is_feasible:
        # Must not contain Monday slot 0
        for s in res.sessions:
            assert not (s.day == "Monday" and s.slot_index == 0)


# ----------------------------------------------------------------------
# 13. Backtracking Recovers from Invalid Assignment
# ----------------------------------------------------------------------
def test_backtracking_recovery_demonstration():
    graph = search_engine.get_graph()
    # Plan with multiple prerequisites
    plan = generate_learning_plan(
        graph,
        "topic-search-bfs-dfs",
        known_topic_ids=["topic-prog-fund", "topic-discrete-math", "topic-ai-foundations"]
    )
    # Tightly constrained schedule allowing feasible solution with backtracking exploration
    prefs = StudyPreferences(
        available_days=["Monday", "Wednesday"],
        max_daily_hours=2,
        preferred_session_hours=1,
        planning_weeks=4,
    )
    res = solve_study_schedule(plan, prefs)
    assert res.assignments_tried > 0
    assert res.is_feasible is True


# ----------------------------------------------------------------------
# 14. Impossible Schedule Handling with Honest Diagnostics
# ----------------------------------------------------------------------
def test_impossible_schedule_handling():
    graph = search_engine.get_graph()
    plan = generate_learning_plan(graph, "topic-neural-networks")
    # Only 1 day per week with 1 hour limit = 2 hours total capacity vs ~25h needed
    prefs = StudyPreferences(
        available_days=["Sunday"],
        max_daily_hours=1,
        preferred_session_hours=1,
        planning_weeks=2,
    )
    res = solve_study_schedule(plan, prefs)
    assert res.is_feasible is False
    assert res.failure_reason is not None
    assert "estimated" in res.failure_reason.lower() or "capacity" in res.failure_reason.lower()


# ----------------------------------------------------------------------
# 15. Invalid Topic Identifiers Handling
# ----------------------------------------------------------------------
def test_invalid_topic_identifiers(client):
    # API 404 for nonexistent topic
    resp = client.get("/api/pathforge/topics/non-existent-topic-xyz")
    assert resp.status_code == 404

    # API 400 for path request with invalid goal
    resp = client.post("/api/pathforge/path", json={
        "goal_topic_id": "non-existent-topic-xyz",
        "known_topic_ids": []
    })
    assert resp.status_code == 400


# ----------------------------------------------------------------------
# 16. PathForge API Responses (Topics, Graph, Path, Compare, Schedule)
# ----------------------------------------------------------------------
def test_pathforge_api_endpoints(client):
    # 1. Topics listing
    resp_topics = client.get("/api/pathforge/topics")
    assert resp_topics.status_code == 200
    data_topics = resp_topics.json()
    assert data_topics["total"] >= 20
    assert any(t["id"] == "topic-machine-learning" for t in data_topics["topics"])

    # 2. Graph visualization data
    resp_graph = client.get("/api/pathforge/graph")
    assert resp_graph.status_code == 200
    data_graph = resp_graph.json()
    assert len(data_graph["nodes"]) >= 20
    assert len(data_graph["edges"]) >= 20

    # 3. Path planning
    resp_path = client.post("/api/pathforge/path", json={
        "goal_topic_id": "topic-machine-learning",
        "known_topic_ids": ["topic-prog-fund", "topic-python-basics"],
        "start_topic_id": "topic-python-basics",
        "algorithm": "bfs"
    })
    assert resp_path.status_code == 200
    data_path = resp_path.json()
    assert data_path["success"] is True
    assert "plan" in data_path
    assert len(data_path["plan"]["ordered_plan"]) > 0
    assert len(data_path["trace"]) >= 4

    # 4. Multi-algorithm comparison
    resp_comp = client.post("/api/pathforge/compare", json={
        "start_topic_id": "topic-prog-fund",
        "goal_topic_id": "topic-machine-learning"
    })
    assert resp_comp.status_code == 200
    data_comp = resp_comp.json()
    assert len(data_comp["comparisons"]) == 4
    algo_names = [c["algorithm"] for c in data_comp["comparisons"]]
    assert any("Breadth-First" in a for a in algo_names)
    assert any("Bidirectional" in a for a in algo_names)
    assert any("Greedy Best-First" in a for a in algo_names)
    assert any("Depth-First" in a for a in algo_names)

    # 5. Study scheduling
    resp_sched = client.post("/api/pathforge/schedule", json={
        "goal_topic_id": "topic-state-spaces",
        "known_topic_ids": ["topic-prog-fund", "topic-python-basics", "topic-discrete-math"],
        "available_days": ["Monday", "Wednesday", "Friday"],
        "max_daily_hours": 3,
        "preferred_session_hours": 1,
        "planning_weeks": 2
    })
    assert resp_sched.status_code == 200
    data_sched = resp_sched.json()
    assert data_sched["success"] is True
    assert "schedule_result" in data_sched


# ----------------------------------------------------------------------
# 17. Integration with the Existing Learnify AI Chatbot
# ----------------------------------------------------------------------
def test_chatbot_pathforge_integration(client):
    planning_queries = [
        "How do I start learning machine learning?",
        "What should I learn before neural networks?",
        "Show me the prerequisites for Bayesian reasoning",
        "Create a study path to learn expert systems",
    ]

    for q in planning_queries:
        resp = client.post("/api/chat/", json={"message": q})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "answered"
        # Must include PathForge roadmap and prerequisites
        assert "PathForge" in data["response"] or "Prerequisites" in data["response"]
        assert "Topological Dependency Planning" in data["conceptsUsed"]
        assert len(data["trace"]) >= 4
        # ProofLens trace must show authentic planning stages
        stages = [s["stage"] for s in data["trace"]]
        assert any("Prerequisite" in s or "Topological" in s or "Goal" in s for s in stages)


# ----------------------------------------------------------------------
# 18. Authentic ProofLens Search Traces and Execution Metrics
# ----------------------------------------------------------------------
def test_prooflens_trace_authenticity():
    # Execute PathForge journey and inspect trace steps
    res = pathforge_service.plan_learning_journey(
        goal_topic_id="topic-neural-networks",
        known_topic_ids=["topic-prog-fund", "topic-python-basics"],
        algorithm="bfs"
    )
    assert res["success"] is True
    traces = res["trace"]
    assert len(traces) >= 4

    for step in traces:
        assert "id" in step
        assert "stage" in step
        assert "method" in step
        assert "duration_ms" in step
        assert step["duration_ms"] >= 0.0
        assert step["status"] == "completed"
        assert step["execution_type"] in ["goal_based", "model_based", "retrieval", "assembly", "verification"]
