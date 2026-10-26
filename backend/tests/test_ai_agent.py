"""
Comprehensive automated test suite for Learnify AI (Phase 1).
Covers:
1. Backend health endpoint
2. Grounded knowledge retrieval
3. Greeting handling (Simple Reflex)
4. Follow-up context & anaphora resolution (Model-Based Agent)
5. Unknown / unsupported question handling (Truthful Uncertainty)
6. Non-fabrication of private / institutional data
7. Correct sources linked to retrieved answers
8. ProofLens trace events with real measured durations and stages
9. Absence of fictitious algorithms in conceptsUsed
10. Input validation (empty, max length, invalid formats)
11. Database seed reproducibility and idempotency
12. Knowledge API listing and single-item retrieval
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
from app.database import init_db, seed_db, get_all_knowledge, get_knowledge_by_id, search_knowledge


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure database schema and seed data are ready before tests run."""
    init_db()
    seed_db()


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


# -------------------------------------------------------------
# Test 1: Backend health endpoint
# -------------------------------------------------------------
def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Learnify AI Backend"
    assert data["phase"] in (1, 2, 3)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Learnify AI"
    assert data["phase"] in (1, 2, 3)


# -------------------------------------------------------------
# Test 2: Successful grounded knowledge retrieval
# -------------------------------------------------------------
def test_ai_definition_query(client):
    payload = {"message": "What is artificial intelligence?"}
    response = client.post("/api/chat/", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "answered"
    assert "Artificial Intelligence" in data["response"]
    assert len(data["sources"]) > 0
    assert data["matchScore"] is not None
    assert data["matchScore"] > 0.3
    # Check that sources contain textbook citation
    assert any("Russell & Norvig" in s["name"] or "AI" in s["name"] for s in data["sources"])


def test_bfs_retrieval(client):
    payload = {"message": "Explain breadth-first search"}
    response = client.post("/api/chat/", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "answered"
    assert "Breadth-First Search" in data["response"] or "FIFO" in data["response"]
    assert data["matchScore"] > 0.4
    assert len(data["trace"]) >= 4


def test_applications_query(client):
    payload = {"message": "What are the applications of artificial intelligence?"}
    response = client.post("/api/chat/", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "answered"
    assert "Healthcare" in data["response"] or "Finance" in data["response"] or "Transportation" in data["response"]


# -------------------------------------------------------------
# Test 3: Greeting handling (Simple Reflex)
# -------------------------------------------------------------
def test_greeting_handling(client):
    for greeting in ["Hello", "Hi", "Hey", "good morning"]:
        response = client.post("/api/chat/", json={"message": greeting})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "greeting"
        assert "Learnify AI" in data["response"]
        assert "Simple Reflex Agent" in data["conceptsUsed"]
        assert len(data["suggestions"]) > 0


# -------------------------------------------------------------
# Test 4: Follow-up context & anaphora resolution (Model-Based)
# -------------------------------------------------------------
def test_followup_anaphora_resolution(client):
    # Context where user previously discussed Breadth-First Search
    context = [
        {
            "id": "1",
            "role": "user",
            "content": "Explain breadth-first search."
        },
        {
            "id": "2",
            "role": "assistant",
            "content": "Breadth-First Search is an uninformed search algorithm that explores nodes level by level using a FIFO queue."
        }
    ]

    # Follow-up with pronoun "Where is it useful?"
    payload = {
        "message": "Where is it useful?",
        "context": context
    }
    response = client.post("/api/chat/", json=payload)
    assert response.status_code == 200
    data = response.json()

    # The agent should have resolved "it" to BFS
    assert data["status"] == "answered"
    assert "Model-Based State Tracking" in data["conceptsUsed"]
    # ProofLens trace must show anaphora resolution
    context_step = next((s for s in data["trace"] if s["stage"] == "Context Resolution"), None)
    assert context_step is not None
    assert context_step["status"] == "completed"
    assert "breadth-first search" in context_step["output_summary"].lower() or "bfs" in context_step["output_summary"].lower()


# -------------------------------------------------------------
# Test 5: Unknown or unsupported question handling
# -------------------------------------------------------------
def test_unknown_question_handling(client):
    # Query completely outside the syllabus
    payload = {"message": "How do I make chocolate chip cookies from scratch?"}
    response = client.post("/api/chat/", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "needs_clarification"
    # Agent must NOT invent a cookie recipe claiming it's an AI syllabus topic
    assert "don't have verified records" in data["response"].lower() or "curated" in data["response"].lower()
    assert "Epistemic Uncertainty Handling" in data["conceptsUsed"]
    assert len(data["sources"]) == 0
    assert data["missingInfo"] is not None


# -------------------------------------------------------------
# Test 6: No fabricated institution-specific information
# -------------------------------------------------------------
def test_no_fabricated_institutional_info(client):
    queries = [
        "What is my current attendance percentage?",
        "Can you tell me my attendance?",
        "What are the tuition fees for Karunya?",
        "What is my CGPA and semester marks?"
    ]

    for q in queries:
        response = client.post("/api/chat/", json={"message": q})
        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "unsupported"
        # Must explicitly acknowledge that personal / institutional records are not connected
        assert "do not have access to your private student records" in data["response"].lower() or "official student portal" in data["response"].lower()
        # Must not fabricate a random number percentage (e.g. "Your attendance is 85%")
        assert "Your attendance is" not in data["response"]
        assert "Illustrative demo data" in data["response"] or any("demo" in s["id"] for s in data["sources"])
        assert "Rational Agent Behavior" in data["conceptsUsed"]


# -------------------------------------------------------------
# Test 7: Correct sources linked to retrieved answers
# -------------------------------------------------------------
def test_sources_linked_to_knowledge(client):
    response = client.post("/api/chat/", json={"message": "What is an intelligent agent?"})
    assert response.status_code == 200
    data = response.json()

    assert len(data["sources"]) >= 1
    src = data["sources"][0]
    assert src["id"] in ["src-textbook", "src-coursework"]
    assert len(src["name"]) > 0


# -------------------------------------------------------------
# Test 8: Trace events corresponding to actual operations
# -------------------------------------------------------------
def test_prooflens_trace_integrity(client):
    response = client.post("/api/chat/", json={"message": "How does an expert system work?"})
    assert response.status_code == 200
    data = response.json()

    traces = data["trace"]
    assert len(traces) >= 4

    stages = [t["stage"] for t in traces]
    assert "Query Analysis" in stages
    assert "Goal Identification" in stages
    assert "Knowledge Retrieval" in stages

    for step in traces:
        assert step["id"].startswith("step-")
        assert step["method"] is not None and len(step["method"]) > 0
        assert step["duration_ms"] >= 0.0
        assert step["execution_type"] in ["reflex", "model_based", "goal_based", "retrieval", "verification", "assembly", "fallback"]


# -------------------------------------------------------------
# Test 9: No fictitious algorithms in conceptsUsed
# -------------------------------------------------------------
def test_no_fictitious_concepts_in_phase_1(client):
    response = client.post("/api/chat/", json={"message": "Explain depth-first search"})
    assert response.status_code == 200
    data = response.json()

    concepts = data["conceptsUsed"]
    # In Phase 1, graph search execution algorithms (e.g. "Graph BFS Execution", "A* Pathfinding")
    # did NOT execute. Only Phase 1 agent and retrieval concepts should appear!
    assert "A* Pathfinding Execution" not in concepts
    assert "Bayesian Network Inference Engine" not in concepts
    assert "Deep Neural Network" not in concepts


# -------------------------------------------------------------
# Test 10: Input validation and error handling
# -------------------------------------------------------------
def test_empty_input_validation(client):
    response = client.post("/api/chat/", json={"message": ""})
    assert response.status_code == 422  # Pydantic validation error for min_length=1


def test_excessive_length_validation(client):
    long_msg = "test " * 300  # > 1000 characters
    response = client.post("/api/chat/", json={"message": long_msg})
    assert response.status_code == 422


# -------------------------------------------------------------
# Test 11: Knowledge seed reproducibility and idempotency
# -------------------------------------------------------------
def test_seed_idempotency():
    initial_count = len(get_all_knowledge())
    assert initial_count >= 15

    # Run seed_db again to ensure it doesn't duplicate
    seed_db()
    after_count = len(get_all_knowledge())
    assert after_count == initial_count


# -------------------------------------------------------------
# Test 12: Knowledge Explorer and Syllabus API endpoints
# -------------------------------------------------------------
def test_knowledge_api_listing(client):
    response = client.get("/api/knowledge/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 15
    assert len(data["records"]) == data["total"]


def test_knowledge_api_single_item(client):
    response = client.get("/api/knowledge/k-ai-definition")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "k-ai-definition"
    assert "Artificial Intelligence" in data["title"]


def test_knowledge_api_404(client):
    response = client.get("/api/knowledge/non-existent-id")
    assert response.status_code == 404


def test_syllabus_concepts_api(client):
    response = client.get("/api/chat/concepts")
    assert response.status_code == 200
    data = response.json()
    assert len(data["units"]) == 5
    unit1 = data["units"][0]
    assert unit1["theme"] == "Foundations of Artificial Intelligence"
    # Units 1, 2, 3, 4 are marked implemented in Phase 3
    assert all(c["status"] == "Implemented and tested" for c in unit1["concepts"])
    unit2 = data["units"][1]
    assert all(c["status"] == "Implemented and tested" for c in unit2["concepts"])
    unit3 = data["units"][2]
    assert all(c["status"] == "Implemented and tested" for c in unit3["concepts"])
    unit4 = data["units"][3]
    assert all(c["status"] == "Implemented and tested" for c in unit4["concepts"])
    # Future unit (Unit V) must remain Planned for upcoming Phase 4
    unit5 = data["units"][4]
    assert all(c["status"] == "Planned" for c in unit5["concepts"])


def test_problem_solving_representation(client):
    response = client.post("/api/chat/", json={"message": "What do I need to know before studying machine learning?"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert "linear algebra" in data["response"].lower() or "mathematics" in data["response"].lower()


def test_agent_behavior_characteristics(client):
    # Test perception and rational response
    response = client.post("/api/chat/", json={"message": "What is the Turing test?"})
    assert response.status_code == 200
    data = response.json()
    assert "Turing" in data["response"]
    assert data["status"] == "answered"
