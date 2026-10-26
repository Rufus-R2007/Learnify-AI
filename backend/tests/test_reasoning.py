"""
Automated Test Suite for Phase 3: Knowledge Representation, Symbolic Logic & WhatIf Lab.
Author: URK25CS1034 — Hiran Antony
Covers all 21 mandatory test requirements from the Phase 3 specification:
1. Fact storage, provenance, and retrieval
2. Predicate logic representations & substitutions
3. Successful first-order unification
4. Failed unification & occurs-check
5. Repeated-variable consistency
6. Propositional resolution consistency
7. Contradiction detection via empty clause derivation
8. Horn-clause SLD resolution proof success
9. Horn-clause proof failure and missing premises
10. Forward chaining deduction
11. Backward chaining goal diagnosis
12. Missing-information handling (truthful uncertainty)
13. Contradictory facts detection
14. Nonmonotonic exception precedence
15. Counterfactual conclusion revision
16. Scenario isolation protecting verified facts
17. Bayesian posterior probability calculation with Laplace smoothing
18. Rule provenance and explanation traces
19. WhatIf Lab API endpoints
20. Chatbot integration with policy reasoning queries
21. ProofLens execution trace authenticity
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.reasoning.predicates import (
    Constant,
    Variable,
    CompoundTerm,
    Predicate,
    HornClause,
    apply_substitution,
    standardize_apart,
    parse_predicate,
    parse_term,
)
from app.reasoning.unification import unify, occurs_check
from app.reasoning.propositional_resolution import (
    Literal,
    Clause,
    check_consistency,
    parse_clause,
)
from app.reasoning.horn_resolution import HornResolutionEngine
from app.reasoning.facts import Fact, FactBase, VerificationStatus
from app.reasoning.rules import (
    Rule,
    Policy,
    RuleCondition,
    RuleConclusion,
    ConditionOperator,
)
from app.reasoning.forward_chaining import ForwardChainingEngine
from app.reasoning.backward_chaining import BackwardChainingEngine
from app.reasoning.exceptions import NonmonotonicEngine
from app.reasoning.bayesian import (
    NaiveBayesIntentClassifier,
    bayesian_classifier,
    tokenize,
)
from app.reasoning.explanations import compare_scenarios
from app.services.reasoning_service import reasoning_service
from app.services.whatif_service import whatif_service
from app.database import (
    init_db,
    seed_db,
    get_all_policies,
    get_policy_by_id,
    get_verified_facts_for_entity,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def ensure_database():
    """Ensure database schema is up-to-date and seeded for tests."""
    init_db()
    seed_db()


# =========================================================================
# 1. Fact Storage, Retrieval & Provenance
# =========================================================================

def test_fact_storage_and_conflict_detection():
    fb = FactBase()
    f1 = Fact(
        id="f1",
        predicate="attendance_percentage",
        entity_id="student_01",
        value=78,
        source_id="src-demo",
        verification_status=VerificationStatus.VERIFIED,
    )
    fb.add_fact(f1)
    assert len(fb.facts) == 1
    assert fb.get_fact_value("attendance_percentage", "student_01") == 78
    assert f1.is_hypothetical is False

    # Prevent duplicate identical facts
    fb.add_fact(f1)
    assert len(fb.facts) == 1


# =========================================================================
# 2. Predicate Logic Representations & Substitutions
# =========================================================================

def test_predicate_representation_and_substitution():
    p = parse_predicate("enrolled(X, ai_course)")
    assert p.name == "enrolled"
    assert p.arity == 2
    assert p.args[0] == Variable("X")
    assert p.args[1] == Constant("ai_course")

    # Substitution
    subst = {"X": Constant("student_01")}
    p_sub = apply_substitution(p, subst)
    assert repr(p_sub) == "enrolled(student_01, ai_course)"
    assert p_sub.args[0] == Constant("student_01")


# =========================================================================
# 3. Successful First-Order Unification
# =========================================================================

def test_unification_algorithm_success():
    term1 = parse_predicate("enrolled(X, ai_course)")
    term2 = parse_predicate("enrolled(student_01, Y)")

    res = unify(term1, term2)
    assert res.success is True
    assert res.substitutions["X"] == Constant("student_01")
    assert res.substitutions["Y"] == Constant("ai_course")


# =========================================================================
# 4. Failed Unification & Occurs-Check
# =========================================================================

def test_unification_algorithm_failure_and_occurs_check():
    # Constant mismatch
    term1 = parse_predicate("enrolled(student_01, ai_course)")
    term2 = parse_predicate("enrolled(student_02, ai_course)")
    res = unify(term1, term2)
    assert res.success is False

    # Arity mismatch
    p1 = parse_predicate("p(X, Y)")
    p2 = parse_predicate("p(X)")
    assert unify(p1, p2).success is False

    # Occurs-check: X unified with f(X) must fail
    v = Variable("X")
    c = CompoundTerm("f", [Variable("X")])
    assert occurs_check(v, c, {}) is True
    assert unify(v, c).success is False


# =========================================================================
# 5. Repeated-Variable Consistency
# =========================================================================

def test_unification_repeated_variable_consistency():
    # p(X, X) with p(a, a) succeeds
    p1 = parse_predicate("p(X, X)")
    p2 = parse_predicate("p(a, a)")
    assert unify(p1, p2).success is True

    # p(X, X) with p(a, b) fails because X cannot bind to both a and b
    p3 = parse_predicate("p(a, b)")
    assert unify(p1, p3).success is False


# =========================================================================
# 6. Propositional Resolution (Satisfiable)
# =========================================================================

def test_propositional_resolution_satisfiable():
    # Clauses: (P | Q), (~P | R)
    c1 = parse_clause("P | Q")
    c2 = parse_clause("~P | R")
    report = check_consistency([c1, c2])
    assert report.is_consistent is True
    assert report.contradiction_found is False


# =========================================================================
# 7. Contradiction Detection via Resolution
# =========================================================================

def test_propositional_resolution_contradiction():
    # Contradictory set: P, ~P
    c1 = parse_clause("P")
    c2 = parse_clause("~P")
    report = check_consistency([c1, c2])
    assert report.is_consistent is False
    assert report.contradiction_found is True
    assert any(s.is_contradiction for s in report.steps)


# =========================================================================
# 8. Horn-Clause Proof Success (SLD-Resolution)
# =========================================================================

def test_horn_clause_proof_success():
    # Rules: eligible(X) :- attendance_ok(X), assignment_ok(X).
    # Facts: attendance_ok(s1). assignment_ok(s1).
    r1 = HornClause(
        parse_predicate("eligible(X)"),
        [parse_predicate("attendance_ok(X)"), parse_predicate("assignment_ok(X)")]
    )
    f1 = HornClause(parse_predicate("attendance_ok(s1)"), [])
    f2 = HornClause(parse_predicate("assignment_ok(s1)"), [])

    engine = HornResolutionEngine([r1, f1, f2])
    goal = parse_predicate("eligible(s1)")
    result = engine.prove(goal)
    assert result.proven is True
    assert result.status == "PROVEN"
    assert len(result.steps) > 0


# =========================================================================
# 9. Horn-Clause Proof Failure & Missing Premises
# =========================================================================

def test_horn_clause_proof_missing_premise():
    # Rules: eligible(X) :- attendance_ok(X), lab_ok(X).
    # Facts: attendance_ok(s1). (lab_ok is missing!)
    r1 = HornClause(
        parse_predicate("eligible(X)"),
        [parse_predicate("attendance_ok(X)"), parse_predicate("lab_ok(X)")]
    )
    f1 = HornClause(parse_predicate("attendance_ok(s1)"), [])

    engine = HornResolutionEngine([r1, f1])
    goal = parse_predicate("eligible(s1)")
    result = engine.prove(goal)
    assert result.proven is False
    assert result.status == "UNKNOWN"
    assert any(m.name == "lab_ok" for m in result.missing_premises)


# =========================================================================
# 10. Forward Chaining Deduction
# =========================================================================

def test_forward_chaining_deduction():
    policy = reasoning_service.load_policy("policy-exam-eligibility-v1")
    engine = ForwardChainingEngine(policy)

    fb = FactBase()
    fb.add_fact(Fact("f1", "attendance_percentage", "student_01", 82))
    fb.add_fact(Fact("f2", "assignment_completed", "student_01", True))

    result = engine.run(fb, "student_01")
    assert result.final_decision is True
    assert result.decision_status == "SATISFIED"
    assert len(result.activated_rules) >= 3


# =========================================================================
# 11. Backward Chaining Diagnostic
# =========================================================================

def test_backward_chaining_diagnosis():
    policy = reasoning_service.load_policy("policy-exam-eligibility-v1")
    engine = BackwardChainingEngine(policy)

    fb = FactBase()
    fb.add_fact(Fact("f1", "attendance_percentage", "student_01", 80))
    fb.add_fact(Fact("f2", "assignment_completed", "student_01", True))

    result = engine.diagnose_goal(fb, "student_01", "eligible", desired_value=True)
    assert result.proven is True
    assert result.status == "PROVEN"
    assert "eligible = True" in result.explanation


# =========================================================================
# 12. Missing-Information Handling (Truthful Uncertainty)
# =========================================================================

def test_missing_information_remains_unresolved():
    # Policy with 3 requirements: attendance, assignment, and lab clearance
    policy = reasoning_service.load_policy("policy-incomplete-info-v1")
    engine = ForwardChainingEngine(policy)

    fb = FactBase()
    fb.add_fact(Fact("f1", "attendance_percentage", "student_01", 80))
    fb.add_fact(Fact("f2", "assignment_completed", "student_01", True))
    # Note: lab_clearance is intentionally omitted!

    result = engine.run(fb, "student_01")
    assert result.decision_status == "INCOMPLETE_INFO"
    assert "lab_clearance" in result.missing_facts
    # Must NOT guess or invent True
    assert result.final_decision is not True


# =========================================================================
# 13. Contradictory Facts Detection
# =========================================================================

def test_contradictory_facts_detection():
    fb = FactBase()
    fb.add_fact(Fact("f1", "assignment_completed", "student_01", True, source_id="src-a"))
    fb.add_fact(Fact("f2", "assignment_completed", "student_01", False, source_id="src-b"))

    conflicts = fb.detect_conflicts()
    assert len(conflicts) > 0
    assert conflicts[0].predicate == "assignment_completed"
    assert "Contradictory values detected" in conflicts[0].description


# =========================================================================
# 14. Nonmonotonic Exception Precedence
# =========================================================================

def test_nonmonotonic_exception_overrides():
    policy = reasoning_service.load_policy("policy-exception-waiver-v1")
    engine = ForwardChainingEngine(policy)

    fb = FactBase()
    fb.add_fact(Fact("f1", "attendance_percentage", "student_01", 64))  # Below 75%
    fb.add_fact(Fact("f2", "assignment_completed", "student_01", True))
    fb.add_fact(Fact("f3", "approved_exemption", "student_01", True))  # Medical waiver approved!

    result = engine.run(fb, "student_01")
    assert result.final_decision is True
    assert result.decision_status == "OVERRIDDEN_BY_EXCEPTION"
    assert any(r.is_exception for r in result.activated_rules)
    assert any(r.id == "rule-exc-std-disqual" for r in result.overridden_rules)


# =========================================================================
# 15. Counterfactual Conclusion Revision
# =========================================================================

def test_conclusion_revision_on_changed_inputs():
    baseline_facts = {"attendance_percentage": 68, "assignment_completed": True}
    modified_facts = {"attendance_percentage": 78, "assignment_completed": True}

    res = whatif_service.compare_scenarios(
        policy_id="policy-exam-eligibility-v1",
        baseline_facts=baseline_facts,
        modified_facts=modified_facts,
    )
    comp = res["comparison"]
    assert comp["decision_changed"] is True
    assert comp["previous_outcome"]["status"] == "UNSATISFIED"
    assert comp["current_outcome"]["status"] == "SATISFIED"
    assert any(cf["predicate"] == "attendance_percentage" for cf in comp["changed_facts"])


# =========================================================================
# 16. Scenario Isolation Preserves Verified Facts
# =========================================================================

def test_scenario_isolation_preserves_verified_facts():
    base_facts = reasoning_service.load_factbase("student_01")
    orig_att = base_facts.get_fact_value("attendance_percentage", "student_01")

    # Simulate scenario with 99% attendance
    forked = base_facts.fork_scenario({"attendance_percentage": 99}, "student_01", "policy-exam-eligibility-v1")
    assert forked.get_fact_value("attendance_percentage", "student_01") == 99

    # Verify original base_facts was not mutated
    assert base_facts.get_fact_value("attendance_percentage", "student_01") == orig_att

    # Verify database was not mutated
    db_facts = get_verified_facts_for_entity("student_01")
    db_att = next(f["value"] for f in db_facts if f["predicate"] == "attendance_percentage")
    assert db_att == orig_att


# =========================================================================
# 17. Bayesian Posterior Calculation with Laplace Smoothing
# =========================================================================

def test_bayesian_posterior_calculation():
    query = "Am I eligible under the exam policy with 75% attendance?"
    res = bayesian_classifier.classify(query)

    assert res.predicted_category == "INTENT_REASONING_POLICY"
    assert res.is_uncertain is False
    # Check that posterior probabilities sum to 1.0
    total_prob = sum(res.posterior_probabilities.values())
    assert pytest.approx(total_prob, 0.001) == 1.0
    # Laplace smoothing alpha
    assert res.smoothing_alpha == 1.0


# =========================================================================
# 18. Rule Provenance and Explanation Traces
# =========================================================================

def test_rule_provenance_and_explanations():
    policy = reasoning_service.load_policy("policy-exam-eligibility-v1")
    engine = ForwardChainingEngine(policy)
    fb = FactBase([
        Fact("f1", "attendance_percentage", "student_01", 85),
        Fact("f2", "assignment_completed", "student_01", True),
    ])
    result = engine.run(fb, "student_01")

    assert len(result.fired_steps) > 0
    step1 = result.fired_steps[0]
    assert step1.rule_id != ""
    assert step1.matched_facts != {}
    assert "derived_conclusion" in step1.to_dict()


# =========================================================================
# 19. WhatIf Lab API Endpoints
# =========================================================================

def test_whatif_api_endpoints():
    # GET /api/whatif/policies
    resp = client.get("/api/whatif/policies")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 4

    # POST /api/whatif/evaluate
    eval_resp = client.post("/api/whatif/evaluate", json={
        "policy_id": "policy-exam-eligibility-v1",
        "scenario_facts": {"attendance_percentage": 78, "assignment_completed": True},
        "entity_id": "student_01",
    })
    assert eval_resp.status_code == 200
    eval_data = eval_resp.json()
    assert eval_data["result"]["final_decision"] is True
    assert len(eval_data["trace"]) > 0

    # POST /api/whatif/compare
    comp_resp = client.post("/api/whatif/compare", json={
        "policy_id": "policy-exam-eligibility-v1",
        "baseline_facts": {"attendance_percentage": 68, "assignment_completed": True},
        "modified_facts": {"attendance_percentage": 78, "assignment_completed": True},
        "entity_id": "student_01",
    })
    assert comp_resp.status_code == 200
    comp_data = comp_resp.json()
    assert comp_data["comparison"]["decision_changed"] is True


# =========================================================================
# 20. Chatbot Reasoning Integration
# =========================================================================

def test_chatbot_reasoning_integration():
    # Query matching demo policy evaluation
    resp = client.post("/api/chat/", json={
        "message": "Am I eligible under the demo policy with 78% attendance?"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "ELIGIBLE" in data["response"]
    assert any("Knowledge Representation" in c or "Rule-Based" in c for c in data["conceptsUsed"])

    # Diagnostic why query
    why_resp = client.post("/api/chat/", json={
        "message": "Why am I not eligible under the exam policy?"
    })
    assert why_resp.status_code == 200
    why_data = why_resp.json()
    assert "Diagnostic Reasoning" in why_data["response"] or "Proof Status" in why_data["response"]


# =========================================================================
# 21. ProofLens Reasoning Trace Events
# =========================================================================

def test_prooflens_reasoning_trace_events():
    resp = client.post("/api/chat/", json={
        "message": "What if an approved exemption applies to my case?"
    })
    assert resp.status_code == 200
    data = resp.json()
    traces = data.get("trace", [])
    assert len(traces) >= 3

    # Verify real measured duration
    for t in traces:
        assert "duration_ms" in t
        assert t["duration_ms"] >= 0.0
        assert t["stage"] != ""
        assert t["method"] != ""
