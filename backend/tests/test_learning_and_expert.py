"""
Unit V Automated Test Suite: Machine Learning, Expert Systems & Quality Assurance.
Developer: URK25CS1016 — Naveen Kumar

Tests all five learning concepts:
1. Concept 1: Rote Learning (Verified Solution Memory Cache & Invalidation)
2. Concept 2: Learning by Taking Advice (Feedback submission, reviewer approval, knowledge updates)
3. Concept 3: Inductive Learning (scikit-learn TF-IDF + Logistic Regression Intent Classifier)
4. Concept 4: Learning by Analogy (Case-Based Reasoning via Cosine Similarity & Policy Safeguards)
5. Concept 5: Expert Systems (Integrated multi-paradigm query processing & ProofLens tracing)
"""

import os
import sys

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import (
    init_db,
    seed_db,
    get_verified_memory,
    store_verified_memory,
    invalidate_verified_memory,
    get_memory_stats,
    submit_feedback,
    review_feedback,
    get_feedback_by_id,
    get_all_feedback,
    get_knowledge_by_id,
    get_knowledge_history,
)
from app.ml.intent_classifier import intent_classifier
from app.services.analogy_engine import analogy_engine


@pytest.fixture(scope="module")
def client():
    init_db()
    seed_db()
    with TestClient(app) as test_client:
        yield test_client


# =========================================================================
# Concept 1: Rote Learning Tests
# =========================================================================

def test_rote_learning_cache_hit_and_miss(client):
    """
    Rote Learning: First execution performs knowledge retrieval and caches.
    Second identical/normalized execution retrieves from memory cache (HIT).
    """
    # Invalidate existing memory to guarantee fresh start for this test
    invalidate_verified_memory()

    # Turn 1: Fresh query -> Cache MISS, knowledge retrieved, then cached
    res1 = client.post("/api/chat/", json={"message": "What is artificial intelligence?"})
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["status"] == "answered"
    assert data1["roteMemoryHit"] is False

    traces1 = data1["trace"]
    mem_steps1 = [t for t in traces1 if t["execution_type"] == "rote_learning"]
    assert len(mem_steps1) >= 1
    assert "Cache MISS" in mem_steps1[0]["output_summary"]

    # Turn 2: Exact or normalized duplicate -> Cache HIT (Rote Learning)
    res2 = client.post("/api/chat/", json={"message": "What is artificial intelligence?"})
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["roteMemoryHit"] is True
    assert "Rote Learning (Verified Memory)" in data2["conceptsUsed"]

    traces2 = data2["trace"]
    hit_steps = [t for t in traces2 if t["execution_type"] == "rote_learning" and "Cache HIT" in t["output_summary"]]
    assert len(hit_steps) >= 1
    assert hit_steps[0]["status"] == "completed"


def test_rote_memory_invalidation_after_source_change():
    """
    Rote Learning: Invalidation ensures stale cached responses are not reused
    after underlying knowledge changes.
    """
    # Seed a memory entry
    q = "test rote caching topic"
    mem_id = store_verified_memory(
        normalized_query=q,
        answer_text="Test verified answer content.",
        concepts=["Rote Learning"],
        sources=[{"id": "src-coursework", "name": "Course Materials"}],
        scope="academic"
    )
    assert mem_id is not None

    # Verify hit
    cached = get_verified_memory(q)
    assert cached is not None
    assert cached["answer_text"] == "Test verified answer content."

    # Invalidate cache
    inv_count = invalidate_verified_memory()
    assert inv_count >= 1

    # Verify lookup returns None after invalidation
    cached_after = get_verified_memory(q)
    assert cached_after is None


def test_rote_memory_rejects_individualized_data():
    """
    Safety Guard: Memory cache must NEVER store private student records,
    attendance percentages, or individualized decision outcomes.
    """
    unsafe_queries = [
        "my attendance percentage is 68%",
        "what is my gpa?",
        "check student_01 exam marks",
        "hypothetical fee query"
    ]
    for uq in unsafe_queries:
        res = store_verified_memory(
            normalized_query=uq,
            answer_text="Private result",
            concepts=[],
            sources=[],
            scope="academic"
        )
        assert res is None, f"Memory cache should have rejected unsafe query: {uq}"


# =========================================================================
# Concept 2: Learning by Taking Advice Tests
# =========================================================================

def test_feedback_submission(client):
    """
    Learning by Taking Advice: Students can submit feedback and suggested corrections.
    Initial status must be PENDING.
    """
    payload = {
        "query": "What is depth-first search?",
        "original_answer": "DFS explores nodes deeply using a stack.",
        "feedback_type": "not_helpful",
        "comment": "The explanation could mention space complexity.",
        "suggested_correction": "Depth-first search (DFS) systematically traverses branches using a LIFO stack with linear space complexity O(bm).",
        "target_knowledge_id": "k-dfs-def"
    }
    response = client.post("/api/learning/feedback/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["status"] == "PENDING"

    # Verify stored in database
    fb_record = get_feedback_by_id(data["id"])
    assert fb_record is not None
    assert fb_record["feedback_type"] == "not_helpful"
    assert fb_record["status"] == "PENDING"


def test_learning_by_taking_advice_approval_workflow(client):
    """
    Learning by Taking Advice: Reviewer approves submitted correction.
    1. Knowledge record is updated with improved explanation.
    2. Provenance is logged in knowledge_history.
    3. Affected memory cache is invalidated.
    4. Subsequent query receives the improved answer.
    """
    # Step 1: Submit suggested correction for BFS
    improved_bfs_content = (
        "Breadth-First Search (BFS) is an uninformed graph traversal strategy that systematically "
        "expands the shallowest unexpanded node first using a FIFO queue. BFS is complete and optimal "
        "when all step costs are equal, with time and space complexity O(b^d)."
    )
    fb_res = client.post("/api/learning/feedback/", json={
        "query": "What is breadth-first search?",
        "original_answer": "BFS expands shallowest nodes using a queue.",
        "feedback_type": "helpful",
        "suggested_correction": improved_bfs_content,
        "target_knowledge_id": "k-bfs"
    })
    assert fb_res.status_code == 201
    fb_id = fb_res.json()["id"]

    # Step 2: Reviewer approves the feedback
    rev_res = client.post(f"/api/learning/feedback/{fb_id}/review", json={
        "decision": "APPROVED",
        "reviewer_notes": "Verified correct by faculty reviewer Naveen Kumar.",
        "update_knowledge": True
    })
    assert rev_res.status_code == 200
    rev_data = rev_res.json()
    assert rev_data["status"] == "APPROVED"
    assert rev_data["knowledge_updated"] is True

    # Step 3: Verify knowledge table was actually updated
    updated_k = get_knowledge_by_id("k-bfs")
    assert updated_k is not None
    assert "time and space complexity O(b^d)" in updated_k["content"]

    # Step 4: Verify knowledge history recorded the provenance
    history = get_knowledge_history("k-bfs")
    assert len(history) >= 1
    assert history[0]["new_content"] == improved_bfs_content

    # Step 5: Verify subsequent chatbot query receives the updated knowledge
    chat_res = client.post("/api/chat/", json={"message": "What is breadth-first search?"})
    assert chat_res.status_code == 200
    assert "time and space complexity O(b^d)" in chat_res.json()["response"]


def test_feedback_rejection_isolation(client):
    """
    Unapproved advice must NOT modify authoritative knowledge records.
    """
    original_k = get_knowledge_by_id("k-ai-definition")
    orig_content = original_k["content"]

    # Submit bad correction
    fb_res = client.post("/api/learning/feedback/", json={
        "query": "What is artificial intelligence?",
        "original_answer": orig_content,
        "feedback_type": "not_helpful",
        "suggested_correction": "AI is just magic computer electricity.",
        "target_knowledge_id": "k-ai-definition"
    })
    fb_id = fb_res.json()["id"]

    # Reviewer rejects
    rev_res = client.post(f"/api/learning/feedback/{fb_id}/review", json={
        "decision": "REJECTED",
        "reviewer_notes": "Rejected: inaccurate unscientific definition.",
        "update_knowledge": True
    })
    assert rev_res.status_code == 200
    assert rev_res.json()["status"] == "REJECTED"
    assert rev_res.json()["knowledge_updated"] is False

    # Verify knowledge record remained unchanged
    k_after = get_knowledge_by_id("k-ai-definition")
    assert k_after["content"] == orig_content


# =========================================================================
# Concept 3: Inductive Learning (ML Intent Classifier) Tests
# =========================================================================

def test_inductive_learning_classifier_accuracy():
    """
    Inductive Learning: scikit-learn TF-IDF + Logistic Regression evaluated
    on strictly held-out test split (80/20 stratified).
    Verifies actual measured metrics against quality thresholds.
    """
    metrics = intent_classifier.get_metrics()
    assert metrics["held_out_evaluated"] is True
    assert metrics["train_samples"] >= 100
    assert metrics["test_samples"] >= 25

    # True measured metrics check
    assert metrics["overall_accuracy"] >= 0.80, f"Expected accuracy >= 0.80, got {metrics['overall_accuracy']}"
    assert metrics["macro_f1"] >= 0.80, f"Expected macro F1 >= 0.80, got {metrics['macro_f1']}"
    assert len(metrics["classes"]) == 7


def test_intent_predictions_on_sample_curriculum_queries():
    """
    Test real ML inference across distinct student intent categories.
    """
    test_cases = [
        ("What is artificial intelligence?", "academic_concept"),
        ("What should I learn before neural networks?", "prerequisite_path"),
        ("Make a weekly study schedule", "study_schedule"),
        ("Am I eligible with 68% attendance?", "academic_rule"),
        ("Why was this decision made?", "explanation_request"),
        ("Hello", "greeting"),
        ("Book a flight to Paris", "unsupported")
    ]

    for query, expected_intent in test_cases:
        pred = intent_classifier.predict(query)
        assert pred["intent"] == expected_intent, f"Query '{query}' expected '{expected_intent}', got '{pred['intent']}'"
        assert 0.0 <= pred["confidence"] <= 1.0
        assert pred["model_version"] == intent_classifier.MODEL_VERSION


def test_intent_classifier_uncertainty_handling():
    """
    Test that low confidence out-of-distribution queries are flagged as uncertain.
    """
    pred = intent_classifier.predict("asdfghjk qwerty xyz123")
    assert pred["intent"] == "unsupported" or pred["is_confident"] is False


# =========================================================================
# Concept 4: Learning by Analogy (Case-Based Reasoning) Tests
# =========================================================================

def test_analogy_case_retrieval_and_safeguards():
    """
    Learning by Analogy: Retrieves similar solved questions via TF-IDF cosine similarity.
    Safeguard: Rule/eligibility questions must NOT blindly copy outcomes.
    """
    # 1. Conceptual query analogy matching
    res = analogy_engine.find_similar_cases("How does Breadth First Search operate?", top_k=3)
    assert len(res) >= 1
    top_case = res[0]
    assert "bfs" in top_case["question"].lower() or "search" in top_case["question"].lower()
    assert top_case["similarity_score"] > 0.15

    # 2. Individualized query safeguard verification
    guidance = analogy_engine.get_analogy_guidance("Am I eligible with 65% attendance?")
    assert guidance["is_individualized_query"] is True
    assert guidance["guard_notice"] is not None
    assert "Policy Notice" in guidance["guard_notice"]


# =========================================================================
# Concept 5: Expert Systems & End-to-End Pipeline Tests
# =========================================================================

def test_expert_system_end_to_end_pipeline(client):
    """
    Expert System: Unifies ML classification, Search, Reasoning,
    Knowledge Retrieval, Analogy, and ProofLens into a single pipeline.
    """
    # Ask a conceptual question
    response = client.post("/api/chat/", json={"message": "What is an intelligent agent?"})
    assert response.status_code == 200
    data = response.json()

    # Check ML intent fields
    assert data["mlIntent"] == "academic_concept"
    assert data["mlConfidence"] is not None
    assert data["mlModelVersion"] == intent_classifier.MODEL_VERSION

    # Check Analogy cases are included
    assert isinstance(data["relatedCases"], list)

    # Check ProofLens trace contains all multi-paradigm events
    traces = data["trace"]
    exec_types = {t["execution_type"] for t in traces}
    assert "inductive_learning" in exec_types
    assert "expert_system" in exec_types


def test_learning_api_endpoints(client):
    """
    Test all REST endpoints in /api/learning/.
    """
    # 1. ML metrics endpoint
    metrics_res = client.get("/api/learning/ml-metrics")
    assert metrics_res.status_code == 200
    assert metrics_res.json()["overall_accuracy"] >= 0.80

    # 2. Memory stats endpoint
    mem_res = client.get("/api/learning/memory/stats")
    assert mem_res.status_code == 200
    assert "total_entries" in mem_res.json()

    # 3. Analogies endpoint
    ana_res = client.get("/api/learning/analogies?query=Explain%20heuristics%20in%20A*%20search")
    assert ana_res.status_code == 200
    assert "similar_cases" in ana_res.json()

    # 4. Expert system architecture endpoint
    arch_res = client.get("/api/learning/expert-system-architecture")
    assert arch_res.status_code == 200
    assert "subsystems" in arch_res.json()
    assert "inference_engine" in arch_res.json()["subsystems"]
    assert "learning_engine" in arch_res.json()["subsystems"]
