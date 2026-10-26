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
                    concept="Uninformed Search (BFS & DFS)",
                    use_case="Prerequisite topic graph traversal in PathForge",
                    phase=2,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::SearchEngine",
                    test_reference="tests/phase2/test_search.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Informed / Heuristic Search (A* & Greedy Best-First)",
                    use_case="Optimal study schedule pathfinding with time-budget heuristics",
                    phase=2,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::SearchEngine",
                    test_reference="tests/phase2/test_a_star.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Local Search & Hill Climbing",
                    use_case="Exam preparation schedule optimization",
                    phase=2,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::SearchEngine",
                    test_reference="tests/phase2/test_optimization.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Adversarial Search & Game Trees",
                    use_case="Competitive study quiz generation with Minimax principles",
                    phase=2,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::SearchEngine",
                    test_reference="tests/phase2/test_minimax.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit II",
                    concept="Constraint Satisfaction Problems (CSP)",
                    use_case="Course timetable and prerequisite constraint resolution",
                    phase=2,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::SearchEngine",
                    test_reference="tests/phase2/test_csp.py (planned)"
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
                    concept="Semantic Networks & Frames",
                    use_case="Concept ontology linking topics, prerequisites, and learning outcomes",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::KnowledgeEngine",
                    test_reference="tests/phase3/test_semantic_nets.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit III",
                    concept="Propositional Logic & Truth Tables",
                    use_case="Academic eligibility criteria validation",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::KnowledgeEngine",
                    test_reference="tests/phase3/test_prop_logic.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit III",
                    concept="First-Order Predicate Logic (FOL)",
                    use_case="Formal representation of course prerequisites (e.g. HasPrereq(x, y))",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::KnowledgeEngine",
                    test_reference="tests/phase3/test_fol.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit III",
                    concept="Inference Rules & Resolution Refutation",
                    use_case="Automated theorem proving for syllabus requirement satisfaction",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::KnowledgeEngine",
                    test_reference="tests/phase3/test_resolution.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit III",
                    concept="Ontologies & Description Logics",
                    use_case="Unified curriculum taxonomy for computer science subjects",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::KnowledgeEngine",
                    test_reference="tests/phase3/test_ontology.py (planned)"
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
                    concept="Production Rules (IF-THEN Systems)",
                    use_case="Academic policy rules execution for WhatIf Lab",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::RuleEngine",
                    test_reference="tests/phase3/test_rules.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="Forward Chaining (Data-Driven Inference)",
                    use_case="Inferring student academic standing from accumulated credits",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::RuleEngine",
                    test_reference="tests/phase3/test_forward_chain.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="Backward Chaining (Goal-Driven Diagnostic)",
                    use_case="Determining missing prerequisites needed to graduate or enroll",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::RuleEngine",
                    test_reference="tests/phase3/test_backward_chain.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="Conflict Resolution Strategies",
                    use_case="Prioritizing competing academic guidelines (recency, specificity)",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::RuleEngine",
                    test_reference="tests/phase3/test_conflict.py (planned)"
                ),
                SyllabusConceptItem(
                    unit="Unit IV",
                    concept="Truth Maintenance Systems (TMS)",
                    use_case="Tracking assumptions and rollbacks during WhatIf scenario simulations",
                    phase=3,
                    status="Planned",
                    source_reference="backend/app/core/interfaces.py::RuleEngine",
                    test_reference="tests/phase3/test_tms.py (planned)"
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
    return ConceptsResponse(units=units_data, phase_focus=1)
