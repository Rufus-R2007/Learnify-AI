"""
Pydantic schemas for Learnify AI API.
Defines strict, typed models for requests, responses, execution traces,
knowledge records, and syllabus tracking across all phases.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Dict
from datetime import datetime
from enum import Enum


class ExecutionType(str, Enum):
    REFLEX = "reflex"
    MODEL_BASED = "model_based"
    GOAL_BASED = "goal_based"
    RETRIEVAL = "retrieval"
    VERIFICATION = "verification"
    ASSEMBLY = "assembly"
    FALLBACK = "fallback"
    ROTE_LEARNING = "rote_learning"
    INDUCTIVE_LEARNING = "inductive_learning"
    ANALOGY = "analogy"
    EXPERT_SYSTEM = "expert_system"


class StepStatus(str, Enum):
    COMPLETED = "completed"
    SKIPPED = "skipped"
    FALLBACK = "fallback"
    FAILED = "failed"


class ResponseStatus(str, Enum):
    ANSWERED = "answered"
    GREETING = "greeting"
    UNSUPPORTED = "unsupported"
    NEEDS_CLARIFICATION = "needs_clarification"


class TraceStep(BaseModel):
    """
    Structured execution event for ProofLens.
    Every step is backed by real measured execution in the backend pipeline.
    """
    id: str = Field(..., description="Unique step identifier, e.g., 'step-1'")
    stage: str = Field(..., description="Pipeline stage name")
    method: str = Field(..., description="Algorithm or technique used")
    description: str = Field(..., description="Brief explanation of what this step did")
    status: StepStatus = Field(default=StepStatus.COMPLETED)
    input_summary: Optional[str] = Field(None, description="Summary of input to this stage")
    output_summary: Optional[str] = Field(None, description="Summary of output from this stage")
    evidence_ids: List[str] = Field(default_factory=list, description="IDs of knowledge or FAQ records consulted")
    duration_ms: float = Field(..., description="Actual measured duration in milliseconds")
    execution_type: ExecutionType = Field(..., description="Agent behavior or architectural category")


class SourceReference(BaseModel):
    """Provenance and source documentation for grounded answers."""
    id: str
    name: str
    description: Optional[str] = None
    url: Optional[str] = None


class Message(BaseModel):
    """A conversational turn in the chat session."""
    id: Optional[str] = None
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str
    timestamp: Optional[datetime] = None
    conceptsUsed: Optional[List[str]] = None
    sources: Optional[List[SourceReference]] = None
    trace: Optional[List[TraceStep]] = None
    matchScore: Optional[float] = None
    status: Optional[str] = None


class ChatRequest(BaseModel):
    """Incoming request to the chat endpoint."""
    message: str = Field(..., min_length=1, max_length=1000, description="User query")
    context: Optional[List[Message]] = Field(default=None, description="Prior conversation messages")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "What is artificial intelligence?",
                "context": []
            }
        }
    )


class RelatedCase(BaseModel):
    """Analogous solved question retrieved through Case-Based Reasoning."""
    id: str
    question: str
    solution_preview: str
    topic_name: str
    category: str
    unit: int
    similarity_score: float
    is_individualized_warning: bool = False


class ChatResponse(BaseModel):
    """
    Documented extensible chat response for all four phases.
    Includes grounded answer, real concepts used, retrieval match score,
    verified sources, and measured ProofLens trace.
    """
    response: str = Field(..., description="Grounded answer text")
    conceptsUsed: List[str] = Field(default_factory=list, description="Actual AI concepts involved in processing")
    confidence: Optional[float] = Field(default=None, description="Deprecated or null; use matchScore for retrieval relevance")
    matchScore: Optional[float] = Field(default=None, description="Calibrated lexical retrieval relevance score (0.0 to 1.0)")
    sources: List[SourceReference] = Field(default_factory=list, description="Authoritative sources backing this response")
    trace: List[TraceStep] = Field(default_factory=list, description="Measured execution trace for ProofLens")
    status: ResponseStatus = Field(default=ResponseStatus.ANSWERED, description="Outcome status of the agent")
    suggestions: List[str] = Field(default_factory=list, description="Suggested follow-up or related questions")
    missingInfo: Optional[str] = Field(default=None, description="Explanation of what information was unavailable, if any")
    mlIntent: Optional[str] = Field(default=None, description="Predicted student intent from ML classifier")
    mlConfidence: Optional[float] = Field(default=None, description="Calibrated prediction probability of ML classifier")
    mlModelVersion: Optional[str] = Field(default=None, description="Active ML intent classification model version")
    roteMemoryHit: bool = Field(default=False, description="Whether answer was reused from verified rote memory cache")
    relatedCases: List[RelatedCase] = Field(default_factory=list, description="Related solved questions retrieved by Analogy Engine")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response": "Artificial Intelligence is the branch of computer science...",
                "conceptsUsed": [
                    "Intelligent Agent Architecture",
                    "Goal-Based Action Selection",
                    "Lexical Retrieval"
                ],
                "confidence": None,
                "matchScore": 0.88,
                "sources": [
                    {
                        "id": "src-textbook",
                        "name": "AI: A Modern Approach (Russell & Norvig)",
                        "description": "Standard AI textbook reference"
                    }
                ],
                "trace": [],
                "status": "answered",
                "suggestions": [
                    "What are the types of intelligent agents?",
                    "What is breadth-first search?"
                ]
            }
        }
    )


class KnowledgeRecord(BaseModel):
    """Detailed view of an educational knowledge record."""
    id: str
    title: str
    content: str
    keywords: Optional[str] = None
    topic_id: Optional[str] = None
    topic_name: Optional[str] = None
    unit: Optional[int] = None
    source_id: Optional[str] = None
    source_name: Optional[str] = None
    source_desc: Optional[str] = None
    relevance_score: Optional[float] = None


class KnowledgeListResponse(BaseModel):
    """Response containing all or filtered knowledge records."""
    total: int
    records: List[KnowledgeRecord]


class SyllabusConceptItem(BaseModel):
    """An item in the developer-facing five-unit syllabus matrix."""
    unit: str
    concept: str
    use_case: str
    phase: int
    status: str = Field(..., description="'Implemented and tested', 'In progress', or 'Planned'")
    source_reference: Optional[str] = None
    test_reference: Optional[str] = None


class SyllabusUnit(BaseModel):
    """A full syllabus unit containing its concept implementations."""
    id: int
    name: str
    theme: str
    concepts: List[SyllabusConceptItem]
    phase_coverage: List[int]


class ConceptsResponse(BaseModel):
    """Response returned by GET /api/chat/concepts"""
    units: List[SyllabusUnit]
    phase_focus: int = 1


# =========================================================================
# Phase 3 (Hiran Antony): Reasoning & WhatIf Lab Schemas
# =========================================================================

class EvaluateScenarioRequest(BaseModel):
    """Request payload to evaluate scenario facts against a policy."""
    policy_id: str = Field(..., description="ID of named policy, e.g. 'policy-exam-eligibility-v1'")
    scenario_facts: Dict[str, Any] = Field(..., description="Map of predicate names to values")
    entity_id: str = Field(default="student_01", description="Student or entity identifier")
    target_predicate: str = Field(default="eligible", description="Goal predicate to assess")


class ProveGoalRequest(BaseModel):
    """Request payload to prove a goal using backward chaining and SLD resolution."""
    policy_id: str = Field(..., description="ID of named policy")
    goal: str = Field(..., description="Target predicate to prove, e.g. 'eligible'")
    desired_value: Any = Field(default=True, description="Desired outcome value")
    entity_id: str = Field(default="student_01", description="Student identifier")
    scenario_facts: Optional[Dict[str, Any]] = Field(default=None, description="Optional overriding scenario inputs")


class ConsistencyCheckRequest(BaseModel):
    """Request payload to check logical consistency of policy rules."""
    policy_id: str = Field(..., description="ID of policy to validate")


class IntentClassificationRequest(BaseModel):
    """Request payload to classify student query intent via Bayes' Theorem."""
    query: str = Field(..., min_length=1, max_length=1000, description="Student natural language query")


class WhatIfCompareRequest(BaseModel):
    """Request payload to compare baseline scenario against modified scenario."""
    policy_id: str = Field(..., description="ID of named policy")
    baseline_facts: Dict[str, Any] = Field(..., description="Original input facts")
    modified_facts: Dict[str, Any] = Field(..., description="Modified counterfactual input facts")
    entity_id: str = Field(default="student_01", description="Student identifier")


# =========================================================================
# Phase 4 (Naveen Kumar): Unit V Learning & Expert Systems Schemas
# =========================================================================

class FeedbackCreateRequest(BaseModel):
    """Payload to submit student feedback or suggested correction."""
    message_id: Optional[str] = None
    query: str = Field(..., min_length=1, description="Original question asked")
    original_answer: str = Field(..., description="Assistant answer being evaluated")
    feedback_type: str = Field(..., pattern="^(helpful|not_helpful)$", description="'helpful' or 'not_helpful'")
    comment: Optional[str] = Field(default=None, description="Optional explanation of feedback")
    suggested_correction: Optional[str] = Field(default=None, description="Optional corrected explanation")
    target_knowledge_id: Optional[str] = Field(default=None, description="ID of associated knowledge record if known")


class FeedbackReviewRequest(BaseModel):
    """Reviewer decision payload for Learning by Taking Advice."""
    decision: str = Field(..., pattern="^(APPROVED|REJECTED)$", description="'APPROVED' or 'REJECTED'")
    reviewer_notes: Optional[str] = Field(default="", description="Reviewer commentary on the decision")
    update_knowledge: bool = Field(default=True, description="Whether approved correction updates knowledge base")


class FeedbackItem(BaseModel):
    """A feedback submission record."""
    id: str
    message_id: Optional[str] = None
    query: str
    original_answer: str
    feedback_type: str
    comment: Optional[str] = None
    suggested_correction: Optional[str] = None
    target_knowledge_id: Optional[str] = None
    status: str
    reviewer_notes: Optional[str] = None
    created_at: Optional[str] = None
    reviewed_at: Optional[str] = None


class MemoryStatsResponse(BaseModel):
    """Operational statistics for Rote Learning verified memory."""
    total_entries: int
    valid_entries: int
    invalidated_entries: int
    total_cache_hits: int


class MLMetricsResponse(BaseModel):
    """Authentic measured machine learning evaluation metrics."""
    model_version: str
    model_architecture: str
    random_seed: int
    train_samples: int
    test_samples: int
    total_dataset_size: int
    num_classes: int
    classes: List[str]
    overall_accuracy: float
    macro_precision: float
    macro_recall: float
    macro_f1: float
    confusion_matrix: List[List[int]]
    per_class_metrics: Dict[str, Any]
    held_out_evaluated: bool


