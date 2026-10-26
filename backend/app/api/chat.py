"""
Chat API endpoints for Learnify AI.
Implements POST /api/chat/ and GET /api/chat/concepts with full ProofLens trace
and five-unit syllabus tracking.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    ConceptsResponse,
    SyllabusUnit,
    SyllabusConceptItem,
)
from app.services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process student query through the intelligent agent pipeline.
    Returns grounded answer, ProofLens trace events, source references,
    and actual AI concepts used.
    """
    try:
        logger.info(f"Processing query: {request.message[:60]}...")
        
        # Convert context if provided
        context_dicts = None
        if request.context:
            context_dicts = [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "conceptsUsed": msg.conceptsUsed,
                }
                for msg in request.context
            ]

        response = ai_service.process_query_full(request.message, context_dicts)
        logger.info(f"Generated response. Trace steps: {len(response.trace)}, Concepts: {len(response.conceptsUsed)}")
        return response

    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/concepts", response_model=ConceptsResponse)
async def get_ai_concepts() -> ConceptsResponse:
    """
    Get the official five-unit AI syllabus tracker for the micro-project.
    Provides honest status ('Implemented and tested', 'In progress', 'Planned')
    along with source-code references and test references.
    """
    units_data = [
        SyllabusUnit(
            id=1,
            name="Unit I",
            theme="Foundations of Artificial Intelligence",
            phase_coverage=[1],
            concepts=[
                SyllabusConceptItem(
                    unit="Unit I",
                    concept="Artificial Intelligence Concepts & Definitions",
                    use_case="Query normalization, perception, and educational AI concept definitions",
                    phase=1,
                    status="Implemented and tested",
                    source_reference="backend/app/services/agent.py::PerceptionModule",
                    test_reference="backend/tests/test_ai_agent.py::test_ai_definition_query"
                ),
                SyllabusConceptItem(
                    unit="Unit I",
                    concept="Applications of Artificial Intelligence",
                    use_case="Domain categorization of student queries (healthcare, education, search)",
                    phase=1,
                    status="Implemented and tested",
                    source_reference="backend/app/database.py::seed_db",
                    test_reference="backend/tests/test_ai_agent.py::test_applications_query"
                ),
                SyllabusConceptItem(
                    unit="Unit I",
                    concept="Behavioral Characteristics of Intelligent Agents",
                    use_case="Perception, reactivity, rational responses, and truthful uncertainty guards",
                    phase=1,
                    status="Implemented and tested",
                    source_reference="backend/app/services/agent.py::IntelligentAgent",
                    test_reference="backend/tests/test_ai_agent.py::test_agent_behavior_characteristics"
                ),
                SyllabusConceptItem(
                    unit="Unit I",
                    concept="Typical Intelligent Agents (Reflex & Model-Based)",
                    use_case="Simple reflex for greetings; model-based state for anaphora follow-ups",
                    phase=1,
                    status="Implemented and tested",
                    source_reference="backend/app/services/agent.py::ModelBasedState",
                    test_reference="backend/tests/test_ai_agent.py::test_followup_anaphora_resolution"
                ),
                SyllabusConceptItem(
                    unit="Unit I",
                    concept="Problem-Solving Approach & Formulations",
                    use_case="Internal state representation (current state, goal, actions, result)",
                    phase=1,
                    status="Implemented and tested",
                    source_reference="backend/app/services/agent.py::GoalOrientedClassifier",
                    test_reference="backend/tests/test_ai_agent.py::test_problem_solving_representation"
                ),
            ]
        ),
        SyllabusUnit(
            id=2,
            name="Unit II",
            theme="Problem-Solving Strategies and Search Techniques",
            phase_coverage=[2],
            concepts=[
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Breadth-First Search (BFS)",
                    use_case="Unweighted shortest directed pathfinding between curriculum topics in PathForge",
                    phase=2,
                    status="Implemented and tested",
                    source_reference="backend/app/search/bfs.py::breadth_first_search",
                    test_reference="backend/tests/test_search_algorithms.py::test_bfs_shortest_path"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Depth-First Search (DFS)",
                    use_case="Deep prerequisite chain traversal and 3-color recursion-stack cycle detection",
                    phase=2,
                    status="Implemented and tested",
                    source_reference="backend/app/search/dfs.py::depth_first_search",
                    test_reference="backend/tests/test_search_algorithms.py::test_dfs_traversal_and_cycle_detection"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Bidirectional Search",
                    use_case="Simultaneous forward and backward exploration meeting at an intersection",
                    phase=2,
                    status="Implemented and tested",
                    source_reference="backend/app/search/bidirectional.py::bidirectional_search",
                    test_reference="backend/tests/test_search_algorithms.py::test_bidirectional_search_directed"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Greedy Best-First Search & Heuristics",
                    use_case="Informed exploration using priority queue (heapq) and topic similarity heuristics",
                    phase=2,
                    status="Implemented and tested",
                    source_reference="backend/app/search/best_first.py::greedy_best_first_search",
                    test_reference="backend/tests/test_search_algorithms.py::test_greedy_best_first_search"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Problem Spaces, Prerequisite Closure & Topological Sequencing",
                    use_case="Transitive prerequisite closure and Kahn's algorithm DAG ordering for complete learning paths",
                    phase=2,
                    status="Implemented and tested",
                    source_reference="backend/app/search/prerequisites.py::generate_learning_plan",
                    test_reference="backend/tests/test_search_algorithms.py::test_prerequisite_closure_and_topological_sort"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Constraint Satisfaction Problems (CSP)",
                    use_case="Formulation of variables, domains, daily limits, and prerequisite precedence constraints",
                    phase=2,
                    status="Implemented and tested",
                    source_reference="backend/app/search/constraints.py::is_assignment_consistent",
                    test_reference="backend/tests/test_search_algorithms.py::test_csp_constraints_validation"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Backtracking Search",
                    use_case="Constraint propagation and backtracking recovery for feasible study schedule generation",
                    phase=2,
                    status="Implemented and tested",
                    source_reference="backend/app/search/scheduler.py::solve_study_schedule",
                    test_reference="backend/tests/test_search_algorithms.py::test_backtracking_schedule_generation"
                ),
            ]
        ),
        SyllabusUnit(
            id=3,
            name="Unit III",
            theme="Knowledge Representation and Logic",
            phase_coverage=[3],
            concepts=[
                SyllabusConceptItem(
                    unit="Unit III",
                    concept="Knowledge Representation & Epistemic Conflict Detection",
                    use_case="Structured educational facts with provenance, verification status, and conflict detection",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/facts.py::FactBase",
                    test_reference="backend/tests/test_reasoning.py::test_fact_storage_and_conflict_detection"
                ),
                SyllabusConceptItem(
                    unit="Unit III",
                    concept="First-Order Predicate Logic (Terms, Predicates & Clauses)",
                    use_case="Structured logical primitives (Constants, Variables, Compound Terms, Horn Clauses)",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/predicates.py::Predicate",
                    test_reference="backend/tests/test_reasoning.py::test_predicate_representation_and_substitution"
                ),
                SyllabusConceptItem(
                    unit="Unit III",
                    concept="Robinson's First-Order Unification Algorithm",
                    use_case="MGU discovery, variable binding, repeated variable consistency, and occurs-check",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/unification.py::unify",
                    test_reference="backend/tests/test_reasoning.py::test_unification_algorithm"
                ),
                SyllabusConceptItem(
                    unit="Unit III",
                    concept="Propositional Resolution Refutation",
                    use_case="Validating academic policy consistency and detecting formal contradictions",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/propositional_resolution.py::check_consistency",
                    test_reference="backend/tests/test_reasoning.py::test_propositional_resolution_consistency"
                ),
                SyllabusConceptItem(
                    unit="Unit III",
                    concept="Resolution in Predicate Logic (SLD-Resolution)",
                    use_case="Goal-directed proof derivation over definite Horn clauses with cycle prevention",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/horn_resolution.py::HornResolutionEngine",
                    test_reference="backend/tests/test_reasoning.py::test_horn_clause_sld_resolution"
                ),
            ]
        ),
        SyllabusUnit(
            id=4,
            name="Unit IV",
            theme="Rule-Based and Symbolic Reasoning",
            phase_coverage=[3],
            concepts=[
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="Declarative Production Rules & Named Policies",
                    use_case="Separation of declarative knowledge from procedural execution with safe operators",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/rules.py::Policy",
                    test_reference="backend/tests/test_reasoning.py::test_declarative_rule_evaluation"
                ),
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="Forward Chaining (Data-Driven Inference)",
                    use_case="Iterative deduction deriving academic eligibility conclusions from scenario facts",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/forward_chaining.py::ForwardChainingEngine",
                    test_reference="backend/tests/test_reasoning.py::test_forward_chaining_deduction"
                ),
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="Backward Chaining (Goal-Driven Diagnostic)",
                    use_case="Answering 'Why am I eligible?' with proof trees, missing conditions, and PROVEN/DISPROVEN/UNKNOWN states",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/backward_chaining.py::BackwardChainingEngine",
                    test_reference="backend/tests/test_reasoning.py::test_backward_chaining_diagnosis"
                ),
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="Nonmonotonic Reasoning & Exception Handling",
                    use_case="Defeasible belief revision: approved medical exemptions override default attendance rules",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/exceptions.py::NonmonotonicEngine",
                    test_reference="backend/tests/test_reasoning.py::test_nonmonotonic_exception_overrides"
                ),
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="Bayesian Reasoning & Probabilistic Intent Classification",
                    use_case="Probabilistic query routing via Bayes' Theorem with Laplace smoothing over curated dataset",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/reasoning/bayesian.py::NaiveBayesIntentClassifier",
                    test_reference="backend/tests/test_reasoning.py::test_bayesian_intent_classification"
                ),
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="WhatIf Lab Counterfactual Decision Simulator",
                    use_case="Interactive explainable AI decision simulator comparing before vs after scenario adjustments",
                    phase=3,
                    status="Implemented and tested",
                    source_reference="backend/app/services/whatif_service.py::WhatIfService",
                    test_reference="backend/tests/test_reasoning.py::test_whatif_scenario_comparison"
                ),
            ]
        ),
        SyllabusUnit(
            id=5,
            name="Unit V",
            theme="Learning and Expert Systems",
            phase_coverage=[4],
            concepts=[
                SyllabusConceptItem(
                    unit="Unit V",
                    concept="Expert System Architecture & Shells",
                    use_case="End-to-end academic advisor expert system shell",
                    phase=4,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::RuleEngine",
                    test_reference="tests/phase4/test_expert_system.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit V",
                    concept="Supervised Learning (Classification & Regression)",
                    use_case="Intent classification and query difficulty scoring",
                    phase=4,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::LearningEngine",
                    test_reference="tests/phase4/test_supervised.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit V",
                    concept="Uncertainty Handling (Bayesian Reasoning & Certainty Factors)",
                    use_case="Probabilistic student success prediction in WhatIf Lab",
                    phase=4,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::LearningEngine",
                    test_reference="tests/phase4/test_bayesian.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit V",
                    concept="Decision Trees & Information Gain",
                    use_case="Interpretable course recommendation trees",
                    phase=4,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::LearningEngine",
                    test_reference="tests/phase4/test_decision_trees.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit V",
                    concept="System Evaluation & Performance Metrics",
                    use_case="Automated precision/recall evaluation on student query benchmarks",
                    phase=4,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::LearningEngine",
                    test_reference="tests/phase4/test_evaluation.py (planned)"
                ),
            ]
        ),
    ]
    return ConceptsResponse(units=units_data, phase_focus=2)
