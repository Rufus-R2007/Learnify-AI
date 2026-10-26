"""
Intelligent Agent Architecture for Learnify AI (Phase 1 - Unit I Foundations).

Implements the foundational concepts of Artificial Intelligence:
1. Practical AI Pipeline:
   Input -> Query Analysis -> Intent/Goal Selection -> Knowledge Retrieval -> Response Assembly -> Verification -> Output
2. Behavioral Characteristics of Intelligent Agents:
   - Perception: normalizes, tokenizes, and extracts features from queries
   - Reactivity: handles greetings and deterministic requests promptly
   - Context awareness: model-based state tracking resolves anaphoric follow-up queries (e.g. "where is it used?")
   - Goal orientation: classifies user goal and chooses appropriate problem-solving action
   - Rational response selection: answers with grounded facts or honestly acknowledges missing information
3. Agent Architectures:
   - Simple Reflex Behavior for immediate deterministic responses
   - Model-Based Behavior for multi-turn conversational context tracking
   - Goal-Based Behavior for task routing and strategy selection
4. Problem-Solving State representation:
   Tracks (current_state, user_goal, available_actions, selected_action, result, status)
"""

import time
import re
from typing import List, Dict, Tuple, Optional, Any
from app.models.schemas import (
    TraceStep,
    SourceReference,
    ChatResponse,
    ResponseStatus,
    StepStatus,
    ExecutionType,
)
from app.database import (
    search_knowledge,
    search_faqs,
    get_all_knowledge,
)
from app.services.pathforge_service import pathforge_service
from app.services.reasoning_service import reasoning_service
from app.reasoning.bayesian import bayesian_classifier

# Common English conversational stopwords to filter out for keyword search
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
    "during", "each", "few", "for", "from", "further", "had", "hadn't", "has",
    "hasn't", "have", "haven't", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn't", "it",
    "its", "itself", "just", "me", "more", "most", "mustn't", "my", "myself", "no",
    "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our",
    "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "should",
    "shouldn't", "so", "some", "such", "than", "that", "the", "their", "theirs",
    "them", "themselves", "then", "there", "these", "they", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
    "were", "weren't", "what", "when", "where", "which", "while", "who", "whom",
    "why", "with", "won't", "would", "wouldn't", "you", "your", "yours", "yourself",
    "yourselves", "tell", "explain", "describe", "give", "please", "can you"
}

# Recognized educational concepts in Unit I-V for context extraction
AI_ENTITIES = {
    "artificial intelligence": ["ai", "artificial intelligence"],
    "machine learning": ["ml", "machine learning", "supervised", "unsupervised"],
    "neural networks": ["neural networks", "neural network", "deep learning", "perceptron"],
    "breadth-first search": ["bfs", "breadth-first search", "breadth first search"],
    "depth-first search": ["dfs", "depth-first search", "depth first search"],
    "bidirectional search": ["bidirectional", "bidirectional search"],
    "heuristic search": ["heuristic", "a*", "a-star", "hill climbing", "informed search"],
    "constraint satisfaction": ["csp", "constraint satisfaction", "backtracking", "constraints"],
    "intelligent agents": ["agent", "agents", "intelligent agent", "reflex agent", "rational agent"],
    "knowledge representation": ["knowledge representation", "semantic network", "frames", "ontology"],
    "predicate logic": ["predicate logic", "first-order logic", "fol", "quantifiers"],
    "propositional logic": ["propositional logic", "boolean logic"],
    "forward chaining": ["forward chaining", "data-driven"],
    "backward chaining": ["backward chaining", "goal-driven"],
    "bayesian reasoning": ["bayesian", "bayesian reasoning", "bayes", "belief network"],
    "expert systems": ["expert system", "expert systems", "mycin", "inference engine"],
    "problem solving": ["problem solving", "state space", "state spaces"],
    "linear algebra": ["linear algebra", "matrices", "vectors", "eigenvalues"],
    "probability": ["probability", "random variable"],
    "statistics": ["statistics", "hypothesis testing"],
    "discrete mathematics": ["discrete math", "discrete mathematics"],
    "python basics": ["python", "python basics"],
    "programming fundamentals": ["programming", "programming fundamentals"],
    "study preparation": ["exam", "prepare", "study", "resources", "tips"]
}

# Keyword to canonical topic ID map for PathForge planning queries
TOPIC_QUERY_MAP = [
    ("neural networks", "topic-neural-networks"),
    ("neural network", "topic-neural-networks"),
    ("deep learning", "topic-neural-networks"),
    ("machine learning", "topic-machine-learning"),
    ("bayesian reasoning", "topic-bayesian"),
    ("bayesian", "topic-bayesian"),
    ("bayes", "topic-bayesian"),
    ("expert systems", "topic-expert-systems"),
    ("expert system", "topic-expert-systems"),
    ("heuristic search", "topic-heuristic-search"),
    ("heuristics", "topic-heuristic-search"),
    ("a*", "topic-heuristic-search"),
    ("constraint satisfaction", "topic-csp-search"),
    ("csp", "topic-csp-search"),
    ("backtracking", "topic-csp-search"),
    ("bidirectional search", "topic-bidirectional-search"),
    ("bidirectional", "topic-bidirectional-search"),
    ("breadth-first search", "topic-search-bfs-dfs"),
    ("breadth first search", "topic-search-bfs-dfs"),
    ("bfs", "topic-search-bfs-dfs"),
    ("depth-first search", "topic-search-bfs-dfs"),
    ("depth first search", "topic-search-bfs-dfs"),
    ("dfs", "topic-search-bfs-dfs"),
    ("search algorithms", "topic-search-bfs-dfs"),
    ("predicate logic", "topic-predicate-logic"),
    ("first-order logic", "topic-predicate-logic"),
    ("first order logic", "topic-predicate-logic"),
    ("fol", "topic-predicate-logic"),
    ("propositional logic", "topic-prop-logic"),
    ("forward chaining", "topic-forward-backward"),
    ("backward chaining", "topic-forward-backward"),
    ("knowledge representation", "topic-knowledge-rep"),
    ("semantic networks", "topic-knowledge-rep"),
    ("intelligent agents", "topic-intelligent-agents"),
    ("state spaces", "topic-state-spaces"),
    ("problem solving", "topic-problem-solving"),
    ("linear algebra", "topic-linear-algebra"),
    ("probability", "topic-probability"),
    ("statistics", "topic-statistics"),
    ("discrete mathematics", "topic-discrete-math"),
    ("discrete math", "topic-discrete-math"),
    ("python basics", "topic-python-basics"),
    ("python", "topic-python-basics"),
    ("programming", "topic-prog-fund"),
    ("ai foundations", "topic-ai-foundations"),
    ("artificial intelligence", "topic-ai-foundations"),
]


class PerceptionModule:
    """
    Perception: Interprets and normalizes submitted user queries.
    Cleans text, tokenizes, and extracts meaningful keywords.
    """

    @staticmethod
    def process(raw_text: str) -> Dict[str, Any]:
        cleaned = raw_text.strip()
        lower = cleaned.lower()
        # Remove punctuation for tokenization
        tokens = re.findall(r'\b[a-zA-Z0-9_\-\*]+\b', lower)
        # Filter stopwords while preserving key terms
        keywords = [t for t in tokens if t not in STOPWORDS or len(t) <= 2 and t in {"ai", "ml"}]

        # Check for identified AI entity mentions
        detected_entities = []
        for entity_canonical, variations in AI_ENTITIES.items():
            if any(var in lower for var in variations):
                detected_entities.append(entity_canonical)

        return {
            "raw": cleaned,
            "normalized": lower,
            "tokens": tokens,
            "keywords": keywords,
            "detected_entities": detected_entities,
        }


class ModelBasedState:
    """
    Model-Based Agent Component:
    Maintains internal model of conversational context across turns.
    Resolves anaphora / pronouns (e.g., 'where is it used?', 'tell me more about it')
    by identifying the active topic from recent message history.
    """

    ANAPHORA_PATTERNS = [
        r'\bwhere is it (used|useful|applied)\b',
        r'\bhow does it (work|operate)\b',
        r'\bwhat is it used for\b',
        r'\bwhat are its (advantages|disadvantages|applications|properties|limitations)\b',
        r'\btell me more about (it|that|this)\b',
        r'\bwhy use (it|this)\b',
        r'\bexplain (it|this|that)\b',
        r'\bwhen should (i|we) use (it|this)\b',
        r'\bcompare it\b',
    ]

    @classmethod
    def resolve_context(cls, perception: Dict[str, Any], context: Optional[List[Dict[str, Any]]]) -> Tuple[str, Optional[str], bool]:
        """
        Returns:
            (augmented_query, resolved_entity_or_topic, was_context_used)
        """
        query_lower = perception["normalized"]

        # Check if query contains anaphoric pronouns referring back
        has_anaphora = any(re.search(pat, query_lower) for pat in cls.ANAPHORA_PATTERNS) or (
            ("it" in perception["tokens"] or "its" in perception["tokens"] or "that" in perception["tokens"])
            and len(perception["keywords"]) <= 3
        )

        if not has_anaphora or not context:
            return perception["raw"], None, False

        # Inspect context from newest to oldest for an antecedent topic
        antecedent = None
        for msg in reversed(context):
            content = msg.get("content", "").lower()
            # Check for AI entities mentioned in prior messages
            for entity, variations in AI_ENTITIES.items():
                if any(var in content for var in variations):
                    antecedent = entity
                    break
            if antecedent:
                break

        if antecedent:
            # Augment query with resolved antecedent
            augmented = f"{perception['raw']} (referring to {antecedent})"
            return augmented, antecedent, True

        return perception["raw"], None, False


class GoalOrientedClassifier:
    """
    Goal-Based Agent Component:
    Determines user's intent/goal and selects candidate action.
    """

    GREETING_TRIGGERS = {"hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "howdy"}
    CAPABILITY_TRIGGERS = {"what can you do", "help", "who are you", "what are you", "features", "capabilities"}
    
    # Private student records and institutional policies that should NEVER be fabricated
    INSTITUTIONAL_TRIGGERS = [
        "my attendance", "attendance percentage", "attendance record",
        "my marks", "my grades", "my cgpa", "my gpa", "my roll number", "my register number",
        "tuition fee", "hostel fee", "bus fee", "semester fee",
        "exam date for karunya", "karunya attendance", "karunya semester",
        "scholarship criteria", "my timetable", "my class"
    ]

    PATHFORGE_PLANNING_TRIGGERS = [
        "how do i start learning", "how to start learning", "how do i begin learning", "how can i learn",
        "what should i learn before", "what do i need to know before", "what do i need to learn before",
        "what to learn before", "prerequisites for", "prerequisite for", "prerequisites of", "prerequisite of",
        "prerequisites before", "create a study path", "create a learning path", "generate a study path",
        "generate a learning path", "plan my ai studies", "plan my studies", "study path to learn",
        "study path for", "path to learn", "learning path for", "learning path to",
        "show me the prerequisites", "show prerequisites", "what are the prerequisites",
        "how to reach", "how can i reach", "route to", "route from"
    ]

    STUDY_GUIDANCE_TRIGGERS = [
        "how to prepare", "study plan", "exam prep", "how do i study",
        "prepare for exam", "what do i need to know before studying", "study resources"
    ]

    LOGICAL_REASONING_TRIGGERS = [
        "demo policy", "sample policy", "exam policy", "eligibility policy", "whatif", "what if",
        "am i eligible", "why am i eligible", "why am i not eligible", "why did i fail",
        "what requirements", "what do i need to satisfy", "attendance condition",
        "approved exemption", "medical exemption", "medical waiver", "approved waiver",
        "simulate my eligibility", "simulate eligibility", "what happens if my attendance",
        "if my attendance", "if attendance improves", "what if an approved", "missing conditions",
        "which conditions are still missing", "what do i need to satisfy to become eligible",
        "under this example", "under the demo", "under this policy", "satisfy the attendance"
    ]

    @classmethod
    def identify_goal(cls, normalized_text: str, keywords: List[str]) -> str:
        # 1. Simple Reflex: Greetings
        clean_text = normalized_text.strip("?!., ")
        if clean_text in cls.GREETING_TRIGGERS or any(normalized_text.startswith(g + " ") for g in cls.GREETING_TRIGGERS):
            return "GOAL_GREETING"

        # 2. Simple Reflex: Capabilities
        if any(cap in normalized_text for cap in cls.CAPABILITY_TRIGGERS):
            return "GOAL_CAPABILITY"

        # 3. Institutional / Private data guardrail (protected student records)
        # CRITICAL: Guardrails MUST precede reasoning and probabilistic classifiers
        if any(inst in normalized_text for inst in cls.INSTITUTIONAL_TRIGGERS) or (
            "attendance" in normalized_text and ("my" in normalized_text or "percentage" in normalized_text)
        ):
            return "GOAL_PERSONAL_OR_INSTITUTIONAL"

        # 4. Phase 3: Logical Reasoning, WhatIf Lab & Academic Policy Simulation
        if any(rt in normalized_text for rt in cls.LOGICAL_REASONING_TRIGGERS):
            return "GOAL_LOGICAL_REASONING"

        # Probabilistic Routing via Bayes' Theorem
        bayes_eval = bayesian_classifier.classify(normalized_text)
        if bayes_eval.predicted_category == "INTENT_REASONING_POLICY" and not bayes_eval.is_uncertain:
            return "GOAL_LOGICAL_REASONING"

        # 4. PathForge Planning & Prerequisite Search (Phase 2 Signature Engine)
        if any(pt in normalized_text for pt in cls.PATHFORGE_PLANNING_TRIGGERS):
            return "GOAL_PATHFORGE_PLANNING"

        # 5. Study guidance & exam preparation
        if any(guide in normalized_text for guide in cls.STUDY_GUIDANCE_TRIGGERS):
            return "GOAL_STUDY_GUIDANCE"

        # 6. FAQ about Learnify AI
        if "learnify" in normalized_text or "what is this app" in normalized_text or "how does prooflens work" in normalized_text:
            return "GOAL_FAQ"

        # 7. Default to academic knowledge retrieval if keywords exist
        if keywords:
            return "GOAL_KNOWLEDGE_QUERY"

        return "GOAL_UNKNOWN"


class IntelligentAgent:
    """
    Main Phase 1 Intelligent Agent.
    Coordinates the pipeline and measures accurate ProofLens trace events.
    """

    def process(self, query: str, context: Optional[List[Dict[str, Any]]] = None) -> ChatResponse:
        traces: List[TraceStep] = []
        concepts_used: List[str] = []
        step_counter = 1

        # ---------------------------------------------------------
        # STAGE 1: Perception & Query Analysis
        # ---------------------------------------------------------
        t0 = time.perf_counter()
        perception = PerceptionModule.process(query)
        t_duration_1 = (time.perf_counter() - t0) * 1000.0

        traces.append(TraceStep(
            id=f"step-{step_counter}",
            stage="Query Analysis",
            method="Lexical Normalization & Entity Detection",
            description="Normalized query text, removed punctuation, extracted search tokens and candidate entities.",
            status=StepStatus.COMPLETED,
            input_summary=f"Raw text ({len(query)} chars): '{query}'",
            output_summary=f"Keywords: {perception['keywords'][:6]}, Entities: {perception['detected_entities']}",
            evidence_ids=[],
            duration_ms=round(t_duration_1, 3),
            execution_type=ExecutionType.REFLEX,
        ))
        step_counter += 1
        concepts_used.append("Perception & Input Normalization")

        # ---------------------------------------------------------
        # STAGE 2: Model-Based Context Resolution (Anaphora)
        # ---------------------------------------------------------
        t0 = time.perf_counter()
        resolved_query, antecedent, was_context_used = ModelBasedState.resolve_context(perception, context)
        t_duration_2 = (time.perf_counter() - t0) * 1000.0

        if was_context_used:
            traces.append(TraceStep(
                id=f"step-{step_counter}",
                stage="Context Resolution",
                method="Model-Based Anaphora Resolution",
                description=f"Resolved anaphoric reference ('it'/'that') to antecedent topic: '{antecedent}'.",
                status=StepStatus.COMPLETED,
                input_summary=f"Query: '{query}', Context turns: {len(context or [])}",
                output_summary=f"Resolved query: '{resolved_query}' (antecedent: {antecedent})",
                evidence_ids=[],
                duration_ms=round(t_duration_2, 3),
                execution_type=ExecutionType.MODEL_BASED,
            ))
            step_counter += 1
            concepts_used.append("Model-Based State Tracking")
            # Update keywords with resolved antecedent
            antecedent_tokens = re.findall(r'\b[a-zA-Z0-9_\-\*]+\b', antecedent.lower())
            search_terms = list(set(perception["keywords"] + antecedent_tokens))
        else:
            traces.append(TraceStep(
                id=f"step-{step_counter}",
                stage="Context Resolution",
                method="Model-Based Context Inspection",
                description="Checked conversation history; no unresolved anaphora detected.",
                status=StepStatus.SKIPPED,
                input_summary=f"Query: '{query}', History: {len(context or [])} messages",
                output_summary="Self-contained query; no context expansion needed.",
                evidence_ids=[],
                duration_ms=round(t_duration_2, 3),
                execution_type=ExecutionType.MODEL_BASED,
            ))
            step_counter += 1
            search_terms = perception["keywords"]

        # ---------------------------------------------------------
        # STAGE 3: Goal & Intent Selection (Goal-Based Agent)
        # ---------------------------------------------------------
        t0 = time.perf_counter()
        goal = GoalOrientedClassifier.identify_goal(perception["normalized"], perception["keywords"])
        t_duration_3 = (time.perf_counter() - t0) * 1000.0

        traces.append(TraceStep(
            id=f"step-{step_counter}",
            stage="Goal Identification",
            method="Goal-Oriented Rule-Based Classifier",
            description=f"Identified primary student goal: '{goal}'.",
            status=StepStatus.COMPLETED,
            input_summary=f"Normalized input: '{perception['normalized']}'",
            output_summary=f"Selected Goal: {goal}",
            evidence_ids=[],
            duration_ms=round(t_duration_3, 3),
            execution_type=ExecutionType.GOAL_BASED,
        ))
        step_counter += 1
        concepts_used.append("Goal-Based Action Selection")

        # ---------------------------------------------------------
        # STAGE 4: Execute Strategy Based on Goal
        # ---------------------------------------------------------

        # CASE A: GREETING (Simple Reflex)
        if goal == "GOAL_GREETING":
            concepts_used.append("Simple Reflex Agent")
            traces.append(TraceStep(
                id=f"step-{step_counter}",
                stage="Response Assembly",
                method="Simple Reflex Response Mapping",
                description="Selected deterministic welcome message without querying knowledge base.",
                status=StepStatus.COMPLETED,
                input_summary="Greeting percept",
                output_summary="Welcome message assembled with suggested questions",
                evidence_ids=[],
                duration_ms=0.12,
                execution_type=ExecutionType.REFLEX,
            ))
            return ChatResponse(
                response="Hello! I'm Learnify AI, your intelligent academic assistant for Artificial Intelligence. "
                         "You can ask me conceptual questions about search algorithms, intelligent agents, logic, "
                         "knowledge representation, or study preparation. What would you like to explore today?",
                conceptsUsed=concepts_used,
                confidence=None,
                matchScore=1.0,
                sources=[SourceReference(id="src-coursework", name="Learnify AI Course Materials", description="System Greeting")],
                trace=traces,
                status=ResponseStatus.GREETING,
                suggestions=[
                    "What is artificial intelligence?",
                    "What is breadth-first search?",
                    "Explain the types of intelligent agents",
                    "How does an expert system work?"
                ]
            )

        # CASE B: CAPABILITY INQUIRY (Simple Reflex)
        if goal == "GOAL_CAPABILITY":
            concepts_used.append("Simple Reflex Agent")
            traces.append(TraceStep(
                id=f"step-{step_counter}",
                stage="Response Assembly",
                method="Reflex Capability Mapping",
                description="Returned documented system capabilities and supported curriculum units.",
                status=StepStatus.COMPLETED,
                input_summary="Capability query",
                output_summary="System capabilities summarized across Units I-V",
                evidence_ids=[],
                duration_ms=0.14,
                execution_type=ExecutionType.REFLEX,
            ))
            return ChatResponse(
                response="Learnify AI is designed to support student queries across five AI learning units:\n\n"
                         "• Unit I: Foundations of AI, Intelligent Agents, and Problem Solving\n"
                         "• Unit II: Search Strategies (BFS, DFS, Heuristics, A*)\n"
                         "• Unit III: Knowledge Representation & Predicate Logic\n"
                         "• Unit IV: Rule-Based Systems (Forward & Backward Chaining)\n"
                         "• Unit V: Learning & Expert Systems\n\n"
                         "Every response is transparently traced in the ProofLens panel on the right.",
                conceptsUsed=concepts_used,
                confidence=None,
                matchScore=1.0,
                sources=[SourceReference(id="src-coursework", name="Learnify AI Syllabus Specification", description="Syllabus overview")],
                trace=traces,
                status=ResponseStatus.ANSWERED,
                suggestions=[
                    "What is artificial intelligence?",
                    "Compare BFS and DFS",
                    "Explain forward and backward chaining"
                ]
            )

        # CASE C: INSTITUTIONAL / PERSONAL DATA (Guardrail: Truthful Uncertainty)
        if goal == "GOAL_PERSONAL_OR_INSTITUTIONAL":
            concepts_used.append("Rational Agent Behavior")
            concepts_used.append("Epistemic Uncertainty Handling")

            t0 = time.perf_counter()
            traces.append(TraceStep(
                id=f"step-{step_counter}",
                stage="Grounding Verification",
                method="Private & Institutional Data Policy Guard",
                description="Detected query for private student records or official institutional policy.",
                status=StepStatus.FALLBACK,
                input_summary=f"Protected domain query: '{perception['raw']}'",
                output_summary="Personal/institutional data is disconnected. Acknowledged missing information.",
                evidence_ids=[],
                duration_ms=round((time.perf_counter() - t0) * 1000.0, 3),
                execution_type=ExecutionType.VERIFICATION,
            ))

            return ChatResponse(
                response="I do not have access to your private student records, personal attendance percentage, "
                         "internal marks, or official university administrative schedules.\n\n"
                         "To view your official attendance or examination schedule, please log in to your university's "
                         "official student portal or consult the academic office directly.\n\n"
                         "*(Note: Illustrative demo data — not official institutional policy. Learnify AI strictly avoids "
                         "generating fictitious personal information.)*",
                conceptsUsed=concepts_used,
                confidence=None,
                matchScore=None,
                sources=[SourceReference(id="src-demo", name="Illustrative Demo Data", description="Illustrative demo data — not official institutional policy")],
                trace=traces,
                status=ResponseStatus.UNSUPPORTED,
                suggestions=[
                    "What is artificial intelligence?",
                    "What are the types of intelligent agents?",
                    "Help me prepare for an exam"
                ],
                missingInfo="Personal attendance and student portal records are not connected."
            )

        # CASE PATHFORGE_PLANNING: Intelligent Study & Prerequisite Planning (Phase 2 Signature Engine)
        if goal == "GOAL_PATHFORGE_PLANNING":
            concepts_used.append("Goal-Oriented Action Selection")
            concepts_used.append("Prerequisite Closure Traversal")
            concepts_used.append("Topological Dependency Planning")
            concepts_used.append("PathForge Planning Engine")

            # Resolve target topic from query and context
            resolved_topic_id = None
            query_normalized = perception["normalized"]
            for trigger_name, tid in TOPIC_QUERY_MAP:
                if trigger_name in query_normalized or (antecedent and trigger_name in antecedent.lower()):
                    resolved_topic_id = tid
                    break

            if resolved_topic_id:
                plan_result = pathforge_service.plan_learning_journey(
                    goal_topic_id=resolved_topic_id,
                    algorithm="bfs"
                )

                if plan_result.get("success"):
                    goal_info = plan_result["goal"]
                    plan_data = plan_result["plan"]
                    remaining_items = plan_data.get("ordered_plan", [])
                    total_hours = plan_data.get("total_estimated_hours", 0)

                    # Build markdown response
                    lines = [
                        f"### 🗺️ PathForge Learning Path: **{goal_info['name']}**\n",
                        f"To master **{goal_info['name']}** ({goal_info.get('category', 'Curriculum')}, Unit {goal_info.get('unit', 'V')}), "
                        f"PathForge's classical search engine has verified the curriculum graph and topologically ordered all mandatory prerequisites:\n",
                    ]

                    if remaining_items:
                        lines.append("**Recommended Learning Sequence:**")
                        for idx, item in enumerate(remaining_items, 1):
                            lines.append(f"{idx}. **{item['name']}** (Unit {item['unit']}, ~{item['estimated_hours']}h) — *{item['reason']}*")
                        lines.append(f"\n📊 **Total Estimated Effort:** ~{total_hours} study hours across {len(remaining_items)} topics.")
                    else:
                        lines.append("All prerequisites for this topic are already satisfied!")

                    lines.append(
                        "\n---\n"
                        "💡 **Interactive Visualization & Scheduling:**\n"
                        "• Open **PathForge** in the sidebar to inspect the interactive directed knowledge graph.\n"
                        "• Use the **Algorithm Explorer** to compare BFS, Bidirectional Search, and Greedy Best-First Search.\n"
                        "• Use the **Study Planner** to generate a conflict-free study schedule based on your weekly availability."
                    )

                    response_text = "\n".join(lines)

                    # Append PathForge trace steps to the existing perception/context trace
                    for trace_dict in plan_result.get("trace", []):
                        step_counter += 1
                        traces.append(TraceStep(
                            id=f"step-{step_counter}",
                            stage=trace_dict.get("stage", "Planning"),
                            method=trace_dict.get("method", "PathForge"),
                            description=trace_dict.get("description", ""),
                            status=StepStatus(trace_dict.get("status", "completed")),
                            input_summary=trace_dict.get("input_summary"),
                            output_summary=trace_dict.get("output_summary"),
                            evidence_ids=trace_dict.get("evidence_ids", []),
                            duration_ms=trace_dict.get("duration_ms", 0.1),
                            execution_type=ExecutionType.GOAL_BASED,
                        ))

                    return ChatResponse(
                        response=response_text,
                        conceptsUsed=concepts_used,
                        confidence=None,
                        matchScore=1.0,
                        sources=[
                            SourceReference(
                                id="src-textbook",
                                name="AI: A Modern Approach (Russell & Norvig)",
                                description="Curriculum Prerequisite Knowledge Graph"
                            ),
                            SourceReference(
                                id="src-coursework",
                                name="Learnify AI Course Materials",
                                description="Unit II Search & Planning Foundations"
                            )
                        ],
                        trace=traces,
                        status=ResponseStatus.ANSWERED,
                        suggestions=[
                            f"How do I study {goal_info['name']}?",
                            "Open PathForge to explore the topic graph",
                            "Plan my AI studies for this week"
                        ]
                    )

            # If no specific topic matched or generic planning request
            all_topics = pathforge_service.get_topics()
            sample_topics = [t["name"] for t in all_topics if t["unit"] in (2, 4, 5)][:5]
            clarification_text = (
                "I can generate an intelligent study path and prerequisite roadmap for you! "
                "Which specific topic would you like to plan for?\n\n"
                "Popular options in our curriculum include:\n"
                + "\n".join(f"• **{name}**" for name in sample_topics) +
                "\n\nYou can also click **PathForge** in the left sidebar to explore the full interactive graph and select your target topic visually."
            )
            return ChatResponse(
                response=clarification_text,
                conceptsUsed=concepts_used,
                confidence=None,
                matchScore=None,
                sources=[],
                trace=traces,
                status=ResponseStatus.NEEDS_CLARIFICATION,
                suggestions=[
                    "What should I learn before neural networks?",
                    "How do I start learning machine learning?",
                    "Show me the prerequisites for Bayesian reasoning"
                ],
                missingInfo="Target learning topic was not specified in the planning query."
            )

        # CASE LOGICAL_REASONING: Academic Decision Reasoning & WhatIf Simulation (Phase 3 Signature Innovation)
        if goal == "GOAL_LOGICAL_REASONING":
            concepts_used.append("Knowledge Representation & Predicate Logic")
            concepts_used.append("Rule-Based Symbolic Reasoning")
            concepts_used.append("Bayesian Intent Classification")
            concepts_used.append("WhatIf Academic Decision Simulator")

            query_lower = perception["normalized"]

            # Select applicable policy
            if any(w in query_lower for w in ["exemption", "waiver", "medical", "approved exemption", "sports"]):
                policy_id = "policy-exception-waiver-v1"
            elif any(w in query_lower for w in ["lab", "clearance", "incomplete", "laboratory"]):
                policy_id = "policy-incomplete-info-v1"
            elif any(w in query_lower for w in ["honors", "gpa", "conduct", "merit"]):
                policy_id = "policy-academic-honors-v1"
            else:
                policy_id = "policy-exam-eligibility-v1"

            # Parse hypothetical scenario inputs
            scenario_inputs: Dict[str, Any] = {}

            # Parse attendance percentage if provided (e.g. "78%", "78 percent")
            att_match = re.search(r'(\d{1,3})\s*(?:%|percent)', query_lower)
            if att_match:
                scenario_inputs["attendance_percentage"] = float(att_match.group(1))

            # Parse assignment completion if mentioned
            if "assignment" in query_lower:
                if any(neg in query_lower for neg in ["not completed", "incomplete", "didn't", "did not", "failed"]):
                    scenario_inputs["assignment_completed"] = False
                elif any(pos in query_lower for pos in ["completed", "submitted", "done", "yes"]):
                    scenario_inputs["assignment_completed"] = True

            # Parse exemption
            if any(w in query_lower for w in ["exemption", "waiver", "medical"]):
                if any(neg in query_lower for neg in ["no exemption", "without exemption", "not approved"]):
                    scenario_inputs["approved_exemption"] = False
                else:
                    scenario_inputs["approved_exemption"] = True

            # Check if this is a diagnostic backward reasoning question ("Why am I...", "Why did I...", "Explain why...")
            is_diagnostic_why = any(w in query_lower for w in ["why am i", "why did i", "why not", "why", "explain why", "missing condition"])

            if is_diagnostic_why:
                concepts_used.append("Goal-Driven Backward Chaining")
                concepts_used.append("First-Order Horn Resolution")
                backward_res, diag_traces = reasoning_service.prove_goal(
                    policy_id=policy_id,
                    goal_predicate="eligible",
                    desired_value=True,
                    entity_id="student_01",
                    scenario_facts=scenario_inputs if scenario_inputs else None,
                )

                policy_obj = reasoning_service.load_policy(policy_id)

                lines = [
                    f"### 🧠 Diagnostic Reasoning: **{policy_obj.name}**\n",
                    f"> ℹ️ *{policy_obj.disclaimer}*\n",
                    f"**Target Goal:** `eligible(student_01) = True`\n",
                    f"**Proof Status:** `{backward_res.status}`\n",
                    f"**Explanation:** {backward_res.explanation}\n"
                ]

                if backward_res.supporting_facts:
                    lines.append("\n**Supporting Verified Facts:**")
                    for k, v in backward_res.supporting_facts.items():
                        lines.append(f"• `{k}`: **{v}**")

                if backward_res.missing_conditions:
                    lines.append("\n⚠️ **Unresolved Missing Information:**")
                    for m in backward_res.missing_conditions:
                        lines.append(f"• Condition `{m}` is missing or unverified.")

                lines.append(
                    "\n---\n"
                    "💡 **Explore in WhatIf Lab:**\n"
                    "• Open **WhatIf Lab** in the sidebar to simulate changing attendance or toggling approved exceptions.\n"
                    "• Inspect the full interactive proof tree and rule dependencies."
                )

                for dt in diag_traces:
                    step_counter += 1
                    dt.id = f"step-{step_counter}"
                    traces.append(dt)

                return ChatResponse(
                    response="\n".join(lines),
                    conceptsUsed=concepts_used,
                    confidence=None,
                    matchScore=1.0,
                    sources=[SourceReference(id="src-demo", name="Learnify AI WhatIf Rules", description="Illustrative Academic Decision Policy")],
                    trace=traces,
                    status=ResponseStatus.ANSWERED,
                    suggestions=[
                        "What if my attendance improves to 78%?",
                        "What if an approved exemption applies?",
                        "Am I eligible under the demo policy?"
                    ]
                )

            # Otherwise, evaluate forward chaining scenario
            concepts_used.append("Data-Driven Forward Chaining")
            concepts_used.append("Nonmonotonic Exception Reasoning")
            eval_res, eval_traces = reasoning_service.evaluate_scenario(
                policy_id=policy_id,
                scenario_facts=scenario_inputs,
                entity_id="student_01",
                target_predicate="eligible",
            )

            policy_obj = reasoning_service.load_policy(policy_id)

            status_badge = "✅ ELIGIBLE (Requirements Satisfied)" if eval_res.final_decision is True else "❌ INELIGIBLE (Requirements Not Met)"
            if eval_res.decision_status == "OVERRIDDEN_BY_EXCEPTION":
                status_badge = "🛡️ ELIGIBLE VIA EXCEPTION OVERRIDE"
            elif eval_res.decision_status == "INCOMPLETE_INFO":
                status_badge = "⚠️ UNRESOLVED (Incomplete Information)"

            lines = [
                f"### ⚖️ Academic Decision Simulator: **{policy_obj.name}**\n",
                f"> ℹ️ *{policy_obj.disclaimer}*\n",
                f"**Decision:** **{status_badge}**\n",
                f"**Summary:** {eval_res.explanation}\n",
                "\n**Evaluated Scenario Facts:**",
            ]

            for k, v in eval_res.initial_facts.items():
                is_hyp = k in scenario_inputs
                tag = "(hypothetical input)" if is_hyp else "(baseline record)"
                lines.append(f"• `{k}`: **{v}** *{tag}*")

            if eval_res.satisfied_conditions:
                lines.append("\n**Satisfied Requirements:**")
                for sc in eval_res.satisfied_conditions[:4]:
                    lines.append(f"• ✅ `{sc['predicate']}` {sc['operator']} {sc['expected']} (actual: `{sc['actual']}`)")

            if eval_res.unsatisfied_conditions:
                lines.append("\n**Unsatisfied Requirements:**")
                for uc in eval_res.unsatisfied_conditions[:3]:
                    lines.append(f"• ❌ `{uc['predicate']}` requires `{uc['operator']} {uc['expected']}` (actual: `{uc['actual']}`)")

            if eval_res.overridden_rules:
                lines.append("\n**Nonmonotonic Exception Overrides:**")
                for ov in eval_res.overridden_rules:
                    lines.append(f"• 🛡️ Rule `{ov.id}` ({ov.name}) was overridden by active exemption.")

            lines.append(
                "\n---\n"
                "💡 **Next Steps:**\n"
                "• Click **WhatIf Lab** in the left sidebar to adjust attendance sliders, toggle exemptions, and see instant counterfactual diffs.\n"
                "• Ask me: *'Why am I not eligible?'* or *'What if my attendance improves to 78%?'*"
            )

            for et in eval_traces:
                step_counter += 1
                et.id = f"step-{step_counter}"
                traces.append(et)

            return ChatResponse(
                response="\n".join(lines),
                conceptsUsed=concepts_used,
                confidence=None,
                matchScore=1.0,
                sources=[SourceReference(id="src-demo", name="Learnify AI WhatIf Rules", description="Illustrative Academic Decision Policy")],
                trace=traces,
                status=ResponseStatus.ANSWERED,
                suggestions=[
                    "Why am I not eligible?",
                    "What if my attendance improves to 78%?",
                    "What if an approved medical waiver applies?"
                ]
            )

        # CASE D: FAQ RETRIEVAL
        if goal == "GOAL_FAQ":
            t0 = time.perf_counter()
            faq_results = search_faqs(search_terms)
            t_duration_faq = (time.perf_counter() - t0) * 1000.0

            if faq_results:
                best_faq = faq_results[0]
                traces.append(TraceStep(
                    id=f"step-{step_counter}",
                    stage="Knowledge Retrieval",
                    method="FAQ Database Matcher",
                    description=f"Retrieved matching FAQ entry '{best_faq['question']}'.",
                    status=StepStatus.COMPLETED,
                    input_summary=f"Terms: {search_terms}",
                    output_summary=f"Matched FAQ ID: {best_faq['id']} (Score: {best_faq['relevance_score']})",
                    evidence_ids=[best_faq['id']],
                    duration_ms=round(t_duration_faq, 3),
                    execution_type=ExecutionType.RETRIEVAL,
                ))
                step_counter += 1

                concepts_used.append("FAQ Knowledge Retrieval")
                return ChatResponse(
                    response=best_faq["answer"],
                    conceptsUsed=concepts_used,
                    confidence=None,
                    matchScore=best_faq["relevance_score"],
                    sources=[SourceReference(id="src-demo", name="Learnify AI System Documentation", description="FAQ Entry")],
                    trace=traces,
                    status=ResponseStatus.ANSWERED,
                    suggestions=[
                        "What is artificial intelligence?",
                        "What topics can you help with?",
                        "How accurate are the answers?"
                    ]
                )

        # CASE E: ACADEMIC KNOWLEDGE RETRIEVAL (Primary Pipeline)
        t0 = time.perf_counter()
        knowledge_matches = search_knowledge(search_terms)
        t_duration_retrieval = (time.perf_counter() - t0) * 1000.0

        traces.append(TraceStep(
            id=f"step-{step_counter}",
            stage="Knowledge Retrieval",
            method="Inverted Term-Frequency & Weighted Keyword Matcher",
            description=f"Searched SQLite knowledge base for terms {search_terms}. Found {len(knowledge_matches)} candidate records.",
            status=StepStatus.COMPLETED,
            input_summary=f"Search terms: {search_terms}",
            output_summary=f"Found {len(knowledge_matches)} candidates. Top match ID: {knowledge_matches[0]['id'] if knowledge_matches else 'none'}",
            evidence_ids=[k['id'] for k in knowledge_matches[:3]],
            duration_ms=round(t_duration_retrieval, 3),
            execution_type=ExecutionType.RETRIEVAL,
        ))
        step_counter += 1
        concepts_used.append("Lexical Knowledge Retrieval")

        # ---------------------------------------------------------
        # STAGE 5: Grounding & Verification
        # ---------------------------------------------------------
        t0 = time.perf_counter()
        if knowledge_matches and knowledge_matches[0]["relevance_score"] >= 0.15:
            top_record = knowledge_matches[0]
            t_duration_verif = (time.perf_counter() - t0) * 1000.0

            traces.append(TraceStep(
                id=f"step-{step_counter}",
                stage="Evidence Verification",
                method="Provenance & Relevance Verification",
                description=f"Verified top candidate '{top_record['title']}' satisfies relevance threshold (Score: {top_record['relevance_score']}).",
                status=StepStatus.COMPLETED,
                input_summary=f"Candidate: {top_record['id']} from source '{top_record.get('source_name')}'",
                output_summary="Verified grounded record against curated syllabus knowledge.",
                evidence_ids=[top_record['id']],
                duration_ms=round(t_duration_verif, 3),
                execution_type=ExecutionType.VERIFICATION,
            ))
            step_counter += 1
            concepts_used.append("Knowledge Grounding & Verification")

            # ---------------------------------------------------------
            # STAGE 6: Response Assembly
            # ---------------------------------------------------------
            t0 = time.perf_counter()
            assembled_text = top_record["content"]
            t_duration_assembly = (time.perf_counter() - t0) * 1000.0

            traces.append(TraceStep(
                id=f"step-{step_counter}",
                stage="Response Assembly",
                method="Grounded Synthesis & Source Attachment",
                description="Assembled final student response citing authoritative source reference.",
                status=StepStatus.COMPLETED,
                input_summary=f"Record title: '{top_record['title']}'",
                output_summary=f"Response generated ({len(assembled_text)} characters)",
                evidence_ids=[top_record['id']],
                duration_ms=round(t_duration_assembly, 3),
                execution_type=ExecutionType.ASSEMBLY,
            ))

            # Build source reference
            sources = [
                SourceReference(
                    id=top_record.get("source_id", "src-coursework"),
                    name=top_record.get("source_name", "Learnify AI Course Materials"),
                    description=top_record.get("source_desc", "Curated syllabus record")
                )
            ]

            # Generate smart follow-up suggestions
            suggestions = self._generate_suggestions(top_record["id"])

            return ChatResponse(
                response=assembled_text,
                conceptsUsed=concepts_used,
                confidence=None,
                matchScore=top_record["relevance_score"],
                sources=sources,
                trace=traces,
                status=ResponseStatus.ANSWERED,
                suggestions=suggestions
            )

        else:
            # Fallback: Honest Uncertainty without fabrication
            t_duration_verif = (time.perf_counter() - t0) * 1000.0
            traces.append(TraceStep(
                id=f"step-{step_counter}",
                stage="Evidence Verification",
                method="Uncertainty & Out-of-Distribution Guard",
                description="No curated knowledge record exceeded relevance threshold.",
                status=StepStatus.FALLBACK,
                input_summary=f"Query terms: {search_terms}",
                output_summary="Acknowledged absent knowledge instead of fabricating facts.",
                evidence_ids=[],
                duration_ms=round(t_duration_verif, 3),
                execution_type=ExecutionType.VERIFICATION,
            ))

            concepts_used.append("Epistemic Uncertainty Handling")
            return ChatResponse(
                response=f"I don't have verified records in my curated knowledge base covering '{query}'.\n\n"
                         "As an educational assistant adhering to truthful reasoning principles, I only provide grounded "
                         "answers from verified AI curriculum sources rather than inventing information.\n\n"
                         "You can ask me about topics like:\n"
                         "• Artificial Intelligence foundations & Turing Test\n"
                         "• Intelligent agent types & architectures\n"
                         "• Breadth-First Search (BFS) & Depth-First Search (DFS)\n"
                         "• Heuristic Search and A*\n"
                         "• Knowledge representation, predicate logic, and chaining\n"
                         "• Expert systems and machine learning fundamentals",
                conceptsUsed=concepts_used,
                confidence=None,
                matchScore=0.0,
                sources=[],
                trace=traces,
                status=ResponseStatus.NEEDS_CLARIFICATION,
                suggestions=[
                    "What is artificial intelligence?",
                    "What is breadth-first search?",
                    "What are the types of intelligent agents?",
                    "How does an expert system work?"
                ],
                missingInfo=f"No matching syllabus records found for query terms: {search_terms}"
            )

    @staticmethod
    def _generate_suggestions(record_id: str) -> List[str]:
        """Generate meaningful contextual follow-ups based on the answered record."""
        suggestions_map = {
            "k-ai-definition": [
                "What are the applications of artificial intelligence?",
                "What is an intelligent agent?",
                "What is the Turing test?"
            ],
            "k-agent-definition": [
                "What are the types of intelligent agents?",
                "What are the properties of agent environments?",
                "Explain breadth-first search."
            ],
            "k-agent-types": [
                "What is the difference between reflex and model-based agents?",
                "What are agent environment properties?",
                "What is problem-solving in AI?"
            ],
            "k-bfs": [
                "Where is it useful?",
                "Compare BFS and DFS",
                "What is the space complexity of BFS?"
            ],
            "k-dfs": [
                "Compare BFS and DFS",
                "Why is DFS not always complete?",
                "What is heuristic search?"
            ],
            "k-bfs-vs-dfs": [
                "What is heuristic search and A*?",
                "Explain iterative deepening search",
                "What is hill climbing?"
            ],
            "k-heuristic-search": [
                "What makes a heuristic admissible?",
                "Explain hill climbing search",
                "What is knowledge representation?"
            ],
            "k-knowledge-rep": [
                "Explain predicate logic",
                "What is semantic network representation?",
                "What is forward chaining?"
            ],
            "k-predicate-logic": [
                "Compare propositional and predicate logic",
                "Explain forward and backward chaining",
                "How do expert systems use logic?"
            ],
            "k-forward-chaining": [
                "Compare forward and backward chaining",
                "When is backward chaining preferred?",
                "What is an expert system?"
            ],
            "k-backward-chaining": [
                "Compare forward and backward chaining",
                "How does MYCIN use backward chaining?",
                "What is an expert system?"
            ],
            "k-expert-systems": [
                "What are the main components of an expert system?",
                "How do expert systems handle uncertainty?",
                "What are the prerequisites for machine learning?"
            ],
            "k-machine-learning": [
                "What are the prerequisites for studying machine learning?",
                "What is the difference between supervised and unsupervised learning?",
                "How does ML relate to traditional AI?"
            ],
            "k-ml-prerequisites": [
                "What is machine learning?",
                "Recommend study resources for AI",
                "How to prepare for an AI exam?"
            ],
            "k-exam-prep": [
                "Recommended study resources for AI",
                "Compare BFS and DFS",
                "What is the Turing test?"
            ],
        }
        return suggestions_map.get(record_id, [
            "What is artificial intelligence?",
            "What is breadth-first search?",
            "Explain the types of intelligent agents"
        ])


# Singleton agent instance
agent = IntelligentAgent()
