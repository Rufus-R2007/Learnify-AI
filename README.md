# Learnify AI — AI-Powered Chatbot for Student Queries

<div align="center">

![Learnify AI](https://img.shields.io/badge/Learnify-AI-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Foundation_Complete-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![React](https://img.shields.io/badge/React-18+-blue?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=flat-square&logo=fastapi)

**An intelligent student assistant that answers academic queries using knowledge representation, search algorithms, logical reasoning, rule-based inference, and expert-system techniques.**

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Project Objectives](#-project-objectives)
- [Proposed Features](#-proposed-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Current Implementation Status](#-current-implementation-status)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [How to Run](#-how-to-run)
- [API Documentation](#-api-documentation)
- [AI Syllabus Unit-Wise Implementation Plan](#-ai-syllabus-unit-wise-implementation-plan)
- [Unit-Wise Development Roadmap](#-unit-wise-development-roadmap)
- [Testing and Evaluation Plan](#-testing-and-evaluation-plan)
- [Project Limitations](#-project-limitations)
- [Future Enhancements](#-future-enhancements)
- [Team Members](#-team-members)
- [GitHub Development Workflow](#-github-development-workflow)

---

## 🎯 Project Overview

**Learnify AI** is a college AI micro-project that demonstrates the practical application of artificial intelligence concepts in building an intelligent chatbot for educational purposes. The system uses various AI techniques to understand student queries and provide accurate, contextual responses.

### Official Project Details

- **Project Name:** Learnify AI
- **Project Title:** AI-Powered Chatbot for Student Queries  
- **Purpose:** Implement and demonstrate 25 AI concepts across 5 core units of the AI syllabus
- **Target Audience:** College students seeking academic assistance

---

## 🔍 Problem Statement

Students often face challenges when seeking timely academic assistance:
- Difficulty accessing information outside classroom hours
- Limited availability of instructors for individual queries
- Time-consuming process of searching through course materials
- Need for instant clarification on concepts, schedules, and procedures

**Learnify AI** addresses these challenges by providing an intelligent, 24/7 available chatbot that can answer academic queries using AI techniques including knowledge representation, search algorithms, logical reasoning, and expert systems.

---

## 🎯 Project Objectives

1. ✅ **Build a functional chatbot** with modern web technologies (React + FastAPI)
2. 🔄 **Implement knowledge representation** techniques for storing academic information
3. 🔄 **Apply search algorithms** for efficient information retrieval
4. 🔄 **Demonstrate logical reasoning** and inference capabilities
5. 🔄 **Create rule-based systems** with forward/backward chaining
6. 🔄 **Develop expert system** architecture with uncertainty handling
7. 🔄 **Integrate learning** from examples and feedback

---

## ✨ Proposed Features

### Foundation Features (Implemented ✅)

- ✅ Modern, responsive chat interface
- ✅ Real-time message display
- ✅ RESTful API architecture
- ✅ TypeScript type safety
- ✅ Request validation with Pydantic
- ✅ CORS-enabled backend
- ✅ Modular component architecture
- ✅ Interactive API documentation (Swagger/ReDoc)

### AI Features (Planned 🔄)

#### Phase 1: Intelligent Agent (Unit I)
- 🔄 Agent-based architecture with defined goals and actions
- 🔄 Query preprocessing and understanding
- 🔄 Structured information retrieval
- 🔄 Response generation pipeline

#### Phase 2: Search Algorithms (Unit II)
- 🔄 Knowledge hierarchy representation
- 🔄 Breadth-First Search (BFS) implementation
- 🔄 Depth-First Search (DFS) implementation
- 🔄 Best-First Search with heuristics
- 🔄 Search algorithm comparison framework

#### Phase 3: Knowledge Representation (Unit III)
- 🔄 Structured knowledge base (JSON-based initially)
- 🔄 Predicate logic representations
- 🔄 Unification algorithm
- 🔄 Resolution in predicate logic
- 🔄 Logical inference demonstrations

#### Phase 4: Rule-Based Systems (Unit IV)
- 🔄 Production rule representation
- 🔄 Forward chaining inference
- 🔄 Backward chaining inference
- 🔄 Conflict resolution strategies
- 🔄 Uncertainty handling with probabilities
- 🔄 Bayesian reasoning demonstrations

#### Phase 5: Expert System (Unit V)
- 🔄 Integrated expert system architecture
- 🔄 Knowledge acquisition interface
- 🔄 Intent classification from examples
- 🔄 Explanation generation
- 🔄 Controlled feedback and learning mechanism

---

## 🛠️ Technology Stack

### Frontend
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite 5.2
- **Styling:** TailwindCSS 3.4
- **HTTP Client:** Axios 1.6
- **Icons:** Lucide React
- **State Management:** React Hooks

### Backend
- **Framework:** FastAPI 0.109 (Python 3.9+)
- **Server:** Uvicorn with async support
- **Validation:** Pydantic 2.6
- **API Design:** RESTful architecture
- **Logging:** Python logging module

### Development Tools
- **Version Control:** Git & GitHub
- **Package Managers:** npm (frontend), pip (backend)
- **Testing:** Pytest (backend), planned for frontend
- **Documentation:** Markdown, Swagger UI, ReDoc

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser (React)                      │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Header    │  │  Chat        │  │  Message         │   │
│  │  Component │  │  Interface   │  │  Components      │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
│           │              │                   │               │
│           └──────────────┴───────────────────┘               │
│                          │                                    │
│                    API Service (Axios)                       │
└──────────────────────────┼───────────────────────────────────┘
                           │
                           │ HTTP/REST
                           │
┌──────────────────────────▼───────────────────────────────────┐
│              FastAPI Backend (Python)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           API Routes (/api/chat/, /api/health)        │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                   │
│  ┌────────────────────────▼─────────────────────────────┐  │
│  │              AI Service (Query Processing)            │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                   │
│  ┌────────────────────────▼─────────────────────────────┐  │
│  │         AI Module Implementations (Future)            │  │
│  │  ┌──────────┬────────────┬─────────────┬──────────┐ │  │
│  │  │Knowledge │  Search    │   Logic &   │  Rule    │ │  │
│  │  │   Base   │ Algorithms │  Reasoning  │  Engine  │ │  │
│  │  └──────────┴────────────┴─────────────┴──────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Current Data Flow

1. **User Input:** Student types query in chat interface
2. **Frontend Processing:** Message validated and sent via Axios
3. **API Routing:** FastAPI routes request to chat endpoint
4. **Query Processing:** AI Service processes query (currently placeholder logic)
5. **Response Generation:** System returns response with confidence score
6. **UI Update:** Frontend displays response with concept tags

---

## 📊 Current Implementation Status

### Phase 0: Foundation — ✅ **COMPLETE** (100%)

**What exists and works:**

- ✅ **Frontend Application**
  - React 18 + TypeScript setup with Vite
  - Chat interface with Header, MessageList, MessageBubble, MessageInput components
  - API integration service with error handling
  - TailwindCSS styling with responsive design
  - Loading states and error messages

- ✅ **Backend Application**
  - FastAPI application structure
  - Main entry point (`main.py`) with CORS configuration
  - API router for chat endpoints
  - Pydantic schemas for request/response validation
  - Placeholder AI service with keyword-based responses
  - Health check endpoint

- ✅ **API Endpoints**
  - `GET /` - API information
  - `GET /api/health` - Health check
  - `POST /api/chat/` - Chat message processing
  - `GET /api/chat/concepts` - List all AI concepts
  - Interactive docs at `/docs` and `/redoc`

- ✅ **Configuration**
  - `.gitignore` for version control
  - `.env.example` files for environment configuration
  - `requirements.txt` for Python dependencies
  - `package.json` for Node dependencies

- ✅ **Documentation**
  - README.md (this file)
  - SETUP_GUIDE.md for installation
  - QUICKSTART.md for quick start
  - API_REFERENCE.md in docs folder

**What has been verified:**
- Backend starts successfully with `python main.py`
- Frontend builds and runs with `npm run dev`
- API endpoints respond correctly
- Health check returns `{"status": "healthy"}`
- Chat endpoint accepts messages and returns placeholder responses

### Phase 1-5: AI Implementation — ⏳ **NOT STARTED** (0%)

**Status:** Planned but not yet implemented

All 25 AI concepts from Units I-V are documented but not yet coded. The placeholder AI service in `backend/app/services/ai_service.py` contains only simple keyword matching logic.

---

## 🧠 AI Syllabus Unit-Wise Implementation Plan

This section provides a detailed, practical implementation plan for all 25 AI concepts across 5 units of the AI syllabus.

---

### **UNIT I: Foundations of Artificial Intelligence**

#### Selected Concepts:
1. Artificial Intelligence Concepts
2. Applications of Artificial Intelligence
3. Behavioral Characteristics of Intelligent Agents
4. Typical Intelligent Agents
5. Problem-Solving Approach

#### Implementation Plan:

**Step 1: Define the Student-Assistant Agent**

Specify the agent's:
- **Purpose:** Answer student academic queries using AI techniques
- **Inputs:** Natural language questions (text)
- **Outputs:** Informative responses with confidence scores and concept tags
- **Environment:** Web-based chat interface
- **Goals:** Provide accurate, helpful, timely responses
- **Actions:** Query preprocessing, knowledge retrieval, reasoning, response generation

Create agent specification document in `backend/app/ai/knowledge/agent_spec.md`.

**Step 2: Develop Query-Processing Pipeline**

Design modular workflow:

```
Student Input 
    → Query Preprocessing (tokenization, normalization)
    → Query Understanding (intent classification, entity extraction)
    → Information Retrieval (knowledge base search)
    → Reasoning (apply rules, inference)
    → Response Generation
```

Implement in `backend/app/ai/knowledge/query_pipeline.py`:
- `preprocess_query(text) -> tokens`
- `understand_query(tokens) -> intent, entities`
- `retrieve_information(intent, entities) -> candidates`
- `reason_about(candidates) -> conclusion`
- `generate_response(conclusion) -> text`

**Step 3: Define Agent Behavior**

Document in `docs/AGENT_BEHAVIOR.md` how the agent handles:
- **Supported questions:** Academic concepts, schedules, procedures
- **Missing information:** Return "Information not available" with suggestions
- **Ambiguous queries:** Ask clarifying questions
- **Out-of-scope:** Politely redirect or suggest alternatives

Implement behavior rules in `backend/app/ai/knowledge/agent_behavior.py`.

**Step 4: Demonstrate Problem-Solving**

Create test cases in `backend/tests/test_unit1.py`:
- Academic information query: "What is OOP?"
- Subject explanation: "Explain inheritance"
- Examination question: "When is the midterm exam?"
- Institutional procedure: "How to apply for revaluation?"

**Expected Outcome:**
- Structured intelligent agent architecture
- Documented query-processing workflow
- Working agent behavior demonstrations
- Test cases showing agent responses

**Status:** ⏳ Not Started

---

### **UNIT II: Problem-Solving Strategies and Search Techniques**

#### Selected Concepts:
1. Problem-Solving Methods
2. Breadth-First Search (BFS)
3. Depth-First Search (DFS)
4. Best-First Search
5. Heuristic Search Techniques

#### Implementation Plan:

**Step 1: Represent Knowledge Space**

Create hierarchical knowledge structure in `backend/app/ai/search/knowledge_graph.py`:

```python
knowledge_hierarchy = {
    "Computer Science": {
        "OOP": {
            "concepts": ["Classes", "Objects", "Inheritance", "Polymorphism"],
            "units": ["Unit 1", "Unit 2", "Unit 3"],
            "FAQs": [...]
        },
        "Data Structures": {...},
        "AI": {...}
    },
    "Mathematics": {...}
}
```

Store in JSON format: `backend/app/ai/search/knowledge_graph.json`

**Step 2: Implement Breadth-First Search (BFS)**

File: `backend/app/ai/search/bfs.py`

```python
def bfs_search(graph, start, goal, query_keywords):
    """
    Explore knowledge hierarchy level by level
    Returns: path, nodes_explored, success
    """
    queue = [start]
    visited = set()
    path = []
    
    while queue:
        node = queue.pop(0)
        if matches_query(node, query_keywords):
            return path + [node], len(visited), True
        # Add children to queue...
    
    return [], len(visited), False
```

**Step 3: Implement Depth-First Search (DFS)**

File: `backend/app/ai/search/dfs.py`

```python
def dfs_search(graph, start, goal, query_keywords):
    """
    Explore knowledge hierarchy depth-first
    Returns: path, nodes_explored, success
    """
    stack = [start]
    visited = set()
    path = []
    
    while stack:
        node = stack.pop()
        if matches_query(node, query_keywords):
            return path + [node], len(visited), True
        # Add children to stack...
    
    return [], len(visited), False
```

**Step 4: Implement Best-First Search**

File: `backend/app/ai/search/best_first.py`

```python
import heapq

def best_first_search(graph, start, query, heuristic_fn):
    """
    Use priority queue with heuristic evaluation
    Returns: path, nodes_explored, success
    """
    priority_queue = [(heuristic_fn(start, query), start)]
    visited = set()
    
    while priority_queue:
        score, node = heapq.heappop(priority_queue)
        if is_goal(node, query):
            return path, len(visited), True
        # Evaluate and add children...
    
    return [], len(visited), False
```

**Step 5: Design Heuristic Evaluation**

File: `backend/app/ai/search/heuristics.py`

Implement relevance scoring:

```python
def keyword_overlap_heuristic(node, query):
    """Score based on keyword matches"""
    node_keywords = extract_keywords(node)
    query_keywords = extract_keywords(query)
    overlap = len(set(node_keywords) & set(query_keywords))
    return overlap / max(len(query_keywords), 1)

def metadata_relevance_heuristic(node, query):
    """Score based on metadata matches (topic, difficulty, etc.)"""
    score = 0
    if node.topic in query: score += 0.5
    if node.difficulty == infer_difficulty(query): score += 0.3
    return score
```

Document limitations:
- Heuristics are hand-designed, not learned
- May not generalize to all query types
- Requires tuning and evaluation

**Step 6: Compare Search Methods**

File: `backend/app/ai/search/comparison.py`

Create test framework:

```python
def compare_search_algorithms(test_cases):
    """
    Evaluate BFS, DFS, Best-First on test queries
    Metrics: nodes explored, execution time, success rate
    """
    results = {
        "BFS": [],
        "DFS": [],
        "BestFirst": []
    }
    
    for test_case in test_cases:
        # Run each algorithm
        # Record metrics
        # Compare results
    
    return results
```

Test on:
- Simple queries (single concept)
- Complex queries (multiple concepts)
- Ambiguous queries

**Document findings:** No single algorithm is always best. Explain trade-offs:
- BFS: Complete, finds shortest path, but memory-intensive
- DFS: Memory-efficient, but may not find optimal path
- Best-First: Fast if heuristic is good, but depends on heuristic quality

**Expected Outcome:**
- Working search algorithms (BFS, DFS, Best-First)
- Knowledge hierarchy representation
- Heuristic evaluation functions
- Comparative analysis with test results

**Status:** ⏳ Not Started

---

### **UNIT III: Knowledge Representation and Logic**

#### Selected Concepts:
1. Representation and Mappings
2. Issues in Knowledge Representation
3. Predicate Logic: Representing Simple Facts
4. Unification Algorithm
5. Resolution in Predicate Logic

#### Implementation Plan:

**Step 1: Design Structured Knowledge Base**

File: `backend/app/ai/logic/knowledge_base.json`

Store facts separately from code:

```json
{
  "facts": [
    {"type": "Student", "name": "rufus"},
    {"type": "Enrolled", "student": "rufus", "course": "oop"},
    {"type": "Teaches", "faculty": "dr_smith", "course": "oop"},
    {"type": "Schedule", "course": "oop", "day": "monday", "time": "10am"}
  ],
  "rules": [
    {
      "id": "r1",
      "if": ["Enrolled(?s, ?c)", "Teaches(?f, ?c)"],
      "then": "HasInstructor(?s, ?f)"
    }
  ]
}
```

**Note:** These are illustrative examples, not verified institutional records.

**Step 2: Define Predicate Representations**

File: `backend/app/ai/logic/predicates.py`

```python
class Predicate:
    def __init__(self, name, args):
        self.name = name  # e.g., "Student", "Enrolled"
        self.args = args  # e.g., ["rufus"], ["rufus", "oop"]
    
    def __repr__(self):
        return f"{self.name}({', '.join(self.args)})"

# Examples:
# Student(rufus)
# Enrolled(rufus, oop)
# Teaches(dr_smith, oop)
```

**Step 3: Implement Unification Algorithm**

File: `backend/app/ai/logic/unification.py`

```python
def unify(term1, term2, substitution=None):
    """
    Unify two terms, returning substitution or None if unification fails
    
    Args:
        term1: First term (can contain variables like ?x)
        term2: Second term
        substitution: Current variable bindings
    
    Returns:
        Dictionary of variable substitutions or None
    """
    if substitution is None:
        substitution = {}
    
    # If terms are identical
    if term1 == term2:
        return substitution
    
    # If term1 is a variable
    if is_variable(term1):
        return unify_variable(term1, term2, substitution)
    
    # If term2 is a variable
    if is_variable(term2):
        return unify_variable(term2, term1, substitution)
    
    # If both are predicates, unify arguments
    if isinstance(term1, Predicate) and isinstance(term2, Predicate):
        if term1.name != term2.name:
            return None
        if len(term1.args) != len(term2.args):
            return None
        
        for arg1, arg2 in zip(term1.args, term2.args):
            substitution = unify(arg1, arg2, substitution)
            if substitution is None:
                return None
        
        return substitution
    
    return None
```

Test cases in `backend/tests/test_unification.py`:

```python
def test_unification():
    # Test 1: Unify Enrolled(?s, oop) with Enrolled(rufus, oop)
    result = unify(
        Predicate("Enrolled", ["?s", "oop"]),
        Predicate("Enrolled", ["rufus", "oop"])
    )
    assert result == {"?s": "rufus"}
    
    # Test 2: Unify Enrolled(?s, ?c) with Enrolled(rufus, oop)
    result = unify(
        Predicate("Enrolled", ["?s", "?c"]),
        Predicate("Enrolled", ["rufus", "oop"])
    )
    assert result == {"?s": "rufus", "?c": "oop"}
    
    # Test 3: Unification failure
    result = unify(
        Predicate("Student", ["rufus"]),
        Predicate("Course", ["oop"])
    )
    assert result is None
```

**Step 4: Demonstrate Resolution**

File: `backend/app/ai/logic/resolution.py`

Implement predicate logic resolution:

```python
def convert_to_clauses(knowledge_base):
    """Convert facts and rules to clause form"""
    clauses = []
    # Convert each fact and rule
    return clauses

def resolve(clause1, clause2):
    """
    Apply resolution to two clauses
    Returns: resolvent clause or None
    """
    # Find complementary literals
    # Apply unification
    # Generate resolvent
    pass

def prove_by_resolution(knowledge_base, query):
    """
    Prove query using resolution refutation
    
    Steps:
    1. Negate the query
    2. Convert to clause form
    3. Add to knowledge base
    4. Apply resolution until contradiction or no more resolvents
    """
    clauses = convert_to_clauses(knowledge_base)
    negated_query = negate(query)
    clauses.append(negated_query)
    
    while True:
        new_clauses = []
        for c1 in clauses:
            for c2 in clauses:
                resolvent = resolve(c1, c2)
                if resolvent == CONTRADICTION:
                    return True, get_proof_steps()
                if resolvent:
                    new_clauses.append(resolvent)
        
        if not new_clauses:
            return False, []
        
        clauses.extend(new_clauses)
```

Test example:

```
Given facts:
1. Student(rufus)
2. Enrolled(rufus, oop)
3. Enrolled(?s, ?c) → HasAccess(?s, materials)

Query: HasAccess(rufus, materials)?

Resolution proof:
- Negate query: ¬HasAccess(rufus, materials)
- Unify with rule conclusion
- Derive Enrolled(rufus, ?c) with {?c: oop}
- Match with fact 2
- Derive contradiction (empty clause)
- Therefore, query is TRUE
```

**Step 5: Handle Knowledge Representation Issues**

File: `backend/app/ai/logic/issues.py`

Document and handle:

```python
def handle_unknown_fact(query):
    """
    Closed-world assumption: unknown = false
    Open-world assumption: unknown = unknown
    """
    if query not in knowledge_base:
        return "Information not available"

def handle_conflicting_facts(fact1, fact2):
    """
    Detect contradictions
    Use timestamps or confidence scores to resolve
    """
    if contradicts(fact1, fact2):
        return resolve_conflict(fact1, fact2)

def handle_ambiguous_entities(name):
    """
    Multiple entities with same name
    Ask for clarification
    """
    candidates = find_entities(name)
    if len(candidates) > 1:
        return "Did you mean: " + ", ".join(candidates)
```

**Expected Outcome:**
- Structured knowledge base (JSON)
- Predicate representations
- Working unification algorithm with test cases
- Resolution prover with example proofs
- Documented handling of knowledge issues

**Status:** ⏳ Not Started

---

### **UNIT IV: Rule-Based and Symbolic Reasoning**

#### Selected Concepts:
1. Representing Knowledge Using Rules
2. Procedural vs Declarative Knowledge
3. Forward and Backward Reasoning
4. Symbolic Reasoning under Uncertainty
5. Bayes Theorem

#### Implementation Plan:

**Step 1: Create Rule Representation**

File: `backend/app/ai/rules/rule_base.json`

Separate rules from code:

```json
{
  "rules": [
    {
      "id": "r1",
      "name": "Exam Schedule Query",
      "condition": {
        "intent": "exam_schedule",
        "entities": ["course"]
      },
      "action": "retrieve_exam_schedule",
      "priority": 10
    },
    {
      "id": "r2",
      "name": "Concept Explanation",
      "condition": {
        "intent": "explain_concept",
        "entities": ["concept_name"]
      },
      "action": "retrieve_concept_definition",
      "priority": 8
    },
    {
      "id": "r3",
      "name": "Prerequisite Check",
      "condition": {
        "student_enrolled": true,
        "course_has_prerequisite": true
      },
      "action": "check_prerequisites_met",
      "priority": 9
    }
  ]
}
```

**Note:** Institution-specific policies must be verified before being treated as authoritative.

**Step 2: Implement Forward Chaining**

File: `backend/app/ai/rules/forward_chaining.py`

```python
def forward_chaining(knowledge_base, rules):
    """
    Data-driven reasoning: Start with facts, apply rules, derive conclusions
    
    Algorithm:
    1. Start with known facts
    2. Find applicable rules (conditions match facts)
    3. Execute rule actions, add new facts
    4. Repeat until no new facts derived
    
    Returns: derived_facts, reasoning_trace
    """
    facts = set(knowledge_base["facts"])
    derived = set()
    trace = []
    
    changed = True
    iteration = 0
    
    while changed and iteration < MAX_ITERATIONS:
        changed = False
        iteration += 1
        
        for rule in rules:
            # Check if rule conditions are satisfied
            if rule_conditions_met(rule, facts):
                # Execute rule action
                new_fact = execute_rule_action(rule, facts)
                
                if new_fact and new_fact not in facts:
                    facts.add(new_fact)
                    derived.add(new_fact)
                    trace.append({
                        "iteration": iteration,
                        "rule": rule["id"],
                        "derived": new_fact
                    })
                    changed = True
    
    return list(derived), trace
```

Test example:

```
Facts:
- Student(rufus)
- Enrolled(rufus, oop)

Rules:
- IF Enrolled(?s, ?c) THEN HasAccess(?s, course_materials)
- IF HasAccess(?s, course_materials) THEN CanSubmitAssignment(?s)

Forward Chaining:
Iteration 1: Apply Rule 1 → Derive HasAccess(rufus, course_materials)
Iteration 2: Apply Rule 2 → Derive CanSubmitAssignment(rufus)
No more rules apply. Done.
```

**Step 3: Implement Backward Chaining**

File: `backend/app/ai/rules/backward_chaining.py`

```python
def backward_chaining(knowledge_base, rules, goal):
    """
    Goal-driven reasoning: Start with goal, find rules that conclude it
    
    Algorithm:
    1. Start with goal
    2. Find rules that can prove goal
    3. Recursively prove rule conditions
    4. If all conditions proven, goal is proven
    
    Returns: success, proof_trace
    """
    def prove(goal, depth=0):
        # Base case: goal is a known fact
        if goal in knowledge_base["facts"]:
            return True, [f"Depth {depth}: {goal} is a known fact"]
        
        # Find rules that conclude this goal
        applicable_rules = find_rules_with_conclusion(rules, goal)
        
        for rule in applicable_rules:
            # Try to prove all conditions
            all_conditions_proven = True
            proof = [f"Depth {depth}: Trying rule {rule['id']}"]
            
            for condition in rule["conditions"]:
                success, subproof = prove(condition, depth + 1)
                proof.extend(subproof)
                
                if not success:
                    all_conditions_proven = False
                    break
            
            if all_conditions_proven:
                proof.append(f"Depth {depth}: Goal {goal} proven by rule {rule['id']}")
                return True, proof
        
        return False, [f"Depth {depth}: Cannot prove {goal}"]
    
    return prove(goal)
```

Test example:

```
Goal: CanSubmitAssignment(rufus)?

Backward chaining:
1. Find rule: IF HasAccess(?s, materials) THEN CanSubmitAssignment(?s)
2. Need to prove: HasAccess(rufus, materials)
3. Find rule: IF Enrolled(?s, ?c) THEN HasAccess(?s, materials)
4. Need to prove: Enrolled(rufus, ?c)
5. Check facts: Enrolled(rufus, oop) ✓
6. Backtrack: HasAccess(rufus, materials) ✓
7. Backtrack: CanSubmitAssignment(rufus) ✓
```

**Step 4: Add Uncertainty Handling**

File: `backend/app/ai/rules/uncertainty.py`

```python
class UncertainFact:
    def __init__(self, predicate, confidence):
        self.predicate = predicate
        self.confidence = confidence  # 0.0 to 1.0

def classify_query_intent(query, training_examples):
    """
    Classify intent with confidence score
    Returns: intent, confidence
    """
    # Simple baseline: keyword matching
    intent_scores = {}
    
    for intent, keywords in intent_keywords.items():
        score = keyword_overlap(query, keywords)
        intent_scores[intent] = score
    
    best_intent = max(intent_scores, key=intent_scores.get)
    confidence = intent_scores[best_intent]
    
    return best_intent, confidence

def handle_uncertain_classification(intent, confidence, threshold=0.7):
    """
    Handle low-confidence classifications
    """
    if confidence < threshold:
        return {
            "status": "uncertain",
            "message": "I'm not sure what you're asking. Could you rephrase?",
            "candidates": top_n_intents(intent_scores, n=3)
        }
    
    return {
        "status": "confident",
        "intent": intent,
        "confidence": confidence
    }
```

**Step 5: Demonstrate Bayes Theorem**

File: `backend/app/ai/rules/bayes.py`

```python
def bayes_theorem_example(query):
    """
    Calculate conditional probabilities for ambiguous query intents
    
    Example: Query "What is the schedule?"
    Could mean: exam schedule, class schedule, assignment schedule
    
    P(intent|query) = P(query|intent) * P(intent) / P(query)
    """
    # Prior probabilities (from historical data)
    priors = {
        "exam_schedule": 0.3,
        "class_schedule": 0.5,
        "assignment_schedule": 0.2
    }
    
    # Likelihoods (how likely query appears given intent)
    likelihoods = {
        "exam_schedule": compute_likelihood(query, "exam_schedule"),
        "class_schedule": compute_likelihood(query, "class_schedule"),
        "assignment_schedule": compute_likelihood(query, "assignment_schedule")
    }
    
    # Posterior probabilities
    evidence = sum(likelihoods[i] * priors[i] for i in priors)
    
    posteriors = {}
    for intent in priors:
        posteriors[intent] = (likelihoods[intent] * priors[intent]) / evidence
    
    return posteriors

# Example output:
# Query: "What is the schedule?"
# Priors: {exam: 0.3, class: 0.5, assignment: 0.2}
# Likelihoods: {exam: 0.4, class: 0.7, assignment: 0.3}
# Posteriors: {exam: 0.24, class: 0.70, assignment: 0.12}
# Most likely: class_schedule (70%)
```

Document where probabilities come from:
- Priors: Historical query distribution
- Likelihoods: Keyword/feature matching scores
- Update with actual data when available

**Step 6: Add Reasoning Explanations**

File: `backend/app/ai/rules/explanation.py`

```python
def generate_reasoning_trace(query, result, trace):
    """
    Generate human-readable explanation of reasoning process
    """
    explanation = f"Query: {query}\n\n"
    explanation += "Reasoning Steps:\n"
    
    for step in trace:
        explanation += f"{step['iteration']}. Applied rule '{step['rule']}'\n"
        explanation += f"   Derived: {step['derived']}\n"
    
    explanation += f"\nConclusion: {result}\n"
    
    return explanation
```

**Expected Outcome:**
- Rule representation system (JSON-based)
- Working forward chaining with reasoning trace
- Working backward chaining with proof trace
- Uncertainty handling with confidence scores
- Bayes theorem demonstration with example calculations
- Explanation generation for transparency

**Status:** ⏳ Not Started

---

### **UNIT V: Learning and Expert Systems**

#### Selected Concepts:
1. Learning by Taking Advice
2. Learning from Examples: Induction
3. Neural Network Learning
4. Expert Systems
5. Explanation-Based Learning

#### Implementation Plan:

**Step 1: Design Expert System Architecture**

File: `backend/app/ai/expert/architecture.py`

Integrate all previous modules:

```python
class ExpertSystem:
    """
    Complete expert system integrating all AI techniques
    """
    def __init__(self):
        self.knowledge_base = load_knowledge_base()
        self.rule_engine = RuleEngine()
        self.search_engine = SearchEngine()
        self.inference_engine = InferenceEngine()
        self.learning_module = LearningModule()
        self.explanation_module = ExplanationModule()
    
    def process_query(self, query, context):
        # 1. Preprocess query
        processed = self.preprocess(query)
        
        # 2. Classify intent
        intent, confidence = self.classify_intent(processed)
        
        # 3. Search knowledge base
        candidates = self.search_engine.search(intent, processed)
        
        # 4. Apply reasoning
        conclusion = self.inference_engine.reason(candidates, context)
        
        # 5. Generate response
        response = self.generate_response(conclusion, confidence)
        
        # 6. Generate explanation
        explanation = self.explanation_module.explain(
            query, response, self.get_trace()
        )
        
        return response, explanation, confidence
```

**Step 2: Support Knowledge Updates**

File: `backend/app/ai/expert/knowledge_update.py`

```python
class KnowledgeUpdateInterface:
    """
    Controlled interface for authorized knowledge updates
    """
    def add_fact(self, fact, source, verified=False):
        """
        Add new fact with metadata
        """
        if not verified:
            self.pending_facts.append({
                "fact": fact,
                "source": source,
                "timestamp": datetime.now()
            })
            return "Fact pending verification"
        
        self.knowledge_base.add(fact)
        self.log_update("fact_added", fact, source)
        return "Fact added successfully"
    
    def update_rule(self, rule_id, new_rule, verified=False):
        """
        Update existing rule with verification
        """
        if not verified:
            return "Rule updates require verification"
        
        old_rule = self.rule_base.get(rule_id)
        self.rule_base.update(rule_id, new_rule)
        self.log_update("rule_updated", old_rule, new_rule)
        return "Rule updated successfully"
    
    def validate_update(self, update):
        """
        Validate update before applying
        - Check format
        - Detect conflicts
        - Verify source authority
        """
        if not well_formed(update):
            return False, "Malformed update"
        
        if conflicts_with_existing(update):
            return False, "Conflicts with existing knowledge"
        
        return True, "Valid update"
```

**Step 3: Prepare Example Queries**

File: `backend/app/ai/expert/training_data.json`

Create labeled dataset:

```json
{
  "training_examples": [
    {
      "query": "When is the OOP midterm?",
      "intent": "exam_schedule",
      "entities": {"course": "oop", "exam_type": "midterm"}
    },
    {
      "query": "Explain polymorphism",
      "intent": "concept_explanation",
      "entities": {"concept": "polymorphism"}
    },
    {
      "query": "What is my attendance?",
      "intent": "attendance_query",
      "entities": {}
    },
    {
      "query": "How to apply for leave?",
      "intent": "procedure_info",
      "entities": {"procedure": "leave_application"}
    }
  ],
  "validation_examples": [...],
  "test_examples": [...]
}
```

Create at least 50 examples covering different intents.

**Step 4: Implement Example-Based Intent Classification**

File: `backend/app/ai/expert/intent_classifier.py`

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

class IntentClassifier:
    """
    Baseline classifier using TF-IDF + Naive Bayes
    """
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
    
    def train(self, training_examples):
        """
        Train classifier on labeled examples
        """
        queries = [ex["query"] for ex in training_examples]
        intents = [ex["intent"] for ex in training_examples]
        
        # Vectorize queries
        X = self.vectorizer.fit_transform(queries)
        
        # Train classifier
        self.classifier.fit(X, intents)
    
    def predict(self, query):
        """
        Predict intent for new query
        """
        X = self.vectorizer.transform([query])
        intent = self.classifier.predict(X)[0]
        probabilities = self.classifier.predict_proba(X)[0]
        confidence = max(probabilities)
        
        return intent, confidence
    
    def evaluate(self, test_examples):
        """
        Evaluate classifier on test set
        """
        queries = [ex["query"] for ex in test_examples]
        true_intents = [ex["intent"] for ex in test_examples]
        
        X = self.vectorizer.transform(queries)
        predicted_intents = self.classifier.predict(X)
        
        report = classification_report(true_intents, predicted_intents)
        return report
```

**Step 5: Demonstrate Neural Network Learning**

File: `backend/app/ai/expert/neural_classifier.py`

```python
import torch
import torch.nn as nn

class SimpleNeuralClassifier(nn.Module):
    """
    Simple feed-forward neural network for intent classification
    """
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

def train_neural_classifier(training_data, epochs=50):
    """
    Train neural network on intent classification task
    """
    model = SimpleNeuralClassifier(input_size=100, hidden_size=50, num_classes=10)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(epochs):
        # Training loop
        for batch in training_data:
            inputs, labels = batch
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        # Evaluate
        accuracy = evaluate_model(model, validation_data)
        print(f"Epoch {epoch}, Accuracy: {accuracy:.2f}")
    
    return model

def compare_classifiers(baseline, neural, test_data):
    """
    Compare baseline vs neural network
    """
    baseline_accuracy = evaluate(baseline, test_data)
    neural_accuracy = evaluate(neural, test_data)
    
    print("Comparison Results:")
    print(f"Baseline (TF-IDF + Naive Bayes): {baseline_accuracy:.2f}")
    print(f"Neural Network: {neural_accuracy:.2f}")
    
    # Note: For small datasets, simpler models often perform better
    # Neural networks require more data to show advantages
```

**Document:** Neural networks require sufficient training data. With small datasets (< 1000 examples), simpler methods like TF-IDF + Naive Bayes may perform equally well or better.

**Step 6: Investigate Explanation-Based Learning**

File: `backend/app/ai/expert/explanation_learning.py`

```python
class ExplanationBasedLearning:
    """
    Learn from reviewed incorrect responses
    """
    def __init__(self):
        self.feedback_log = []
        self.learned_rules = []
    
    def record_feedback(self, query, predicted, correct, user_feedback):
        """
        Record user feedback on responses
        """
        self.feedback_log.append({
            "query": query,
            "predicted_intent": predicted,
            "correct_intent": correct,
            "user_feedback": user_feedback,
            "timestamp": datetime.now()
        })
    
    def analyze_feedback(self):
        """
        Analyze feedback to identify patterns
        """
        # Group by error type
        error_patterns = {}
        
        for feedback in self.feedback_log:
            error_type = (feedback["predicted_intent"], feedback["correct_intent"])
            if error_type not in error_patterns:
                error_patterns[error_type] = []
            error_patterns[error_type].append(feedback["query"])
        
        return error_patterns
    
    def propose_rule_updates(self, error_patterns):
        """
        Propose new rules based on feedback patterns
        
        IMPORTANT: Proposals must be reviewed before being applied
        """
        proposals = []
        
        for (wrong, correct), queries in error_patterns.items():
            # Identify common features
            common_keywords = extract_common_keywords(queries)
            
            proposal = {
                "type": "intent_correction",
                "from": wrong,
                "to": correct,
                "trigger_keywords": common_keywords,
                "supporting_examples": queries,
                "status": "pending_review"
            }
            
            proposals.append(proposal)
        
        return proposals
    
    def apply_approved_learning(self, approved_proposal):
        """
        Apply approved learning updates
        """
        if approved_proposal["status"] != "approved":
            raise ValueError("Only approved proposals can be applied")
        
        # Update classifier training data
        # Add new rule to rule base
        # Log the change
        
        self.learned_rules.append(approved_proposal)
```

**Note:** Unreviewed feedback must not automatically change authoritative academic rules.

**Expected Outcome:**
- Integrated expert system architecture
- Knowledge update interface with verification
- Labeled intent classification dataset (50+ examples)
- Baseline classifier (TF-IDF + Naive Bayes)
- Optional neural network classifier
- Comparative evaluation results
- Explanation-based learning framework with controlled feedback

**Status:** ⏳ Not Started

---

### **Implementation Status Summary**

| Unit | Concept | Planned Implementation | Status | Verification Evidence |
|------|---------|----------------------|--------|----------------------|
| **UNIT I** | Artificial Intelligence Concepts | Agent specification and behavior | ⏳ Not Started | No implementation |
| I | Applications of AI | Student query answering demonstration | ⏳ Not Started | No implementation |
| I | Behavioral Characteristics of Agents | Agent behavior documentation | ⏳ Not Started | No implementation |
| I | Typical Intelligent Agents | Query-processing pipeline | ⏳ Not Started | No implementation |
| I | Problem-Solving Approach | Test cases with representative queries | ⏳ Not Started | No implementation |
| **UNIT II** | Problem-Solving Methods | Knowledge hierarchy design | ⏳ Not Started | No implementation |
| II | Breadth-First Search (BFS) | BFS algorithm implementation | ⏳ Not Started | No implementation |
| II | Depth-First Search (DFS) | DFS algorithm implementation | ⏳ Not Started | No implementation |
| II | Best-First Search | Best-first with heuristics | ⏳ Not Started | No implementation |
| II | Heuristic Search Techniques | Heuristic evaluation functions | ⏳ Not Started | No implementation |
| **UNIT III** | Representation and Mappings | Knowledge base JSON structure | ⏳ Not Started | No implementation |
| III | Issues in Knowledge Representation | Issue handling documentation | ⏳ Not Started | No implementation |
| III | Predicate Logic | Predicate class implementation | ⏳ Not Started | No implementation |
| III | Unification Algorithm | Unification function with tests | ⏳ Not Started | No implementation |
| III | Resolution in Predicate Logic | Resolution prover | ⏳ Not Started | No implementation |
| **UNIT IV** | Representing Knowledge Using Rules | Rule base JSON structure | ⏳ Not Started | No implementation |
| IV | Procedural vs Declarative Knowledge | Rule engine design | ⏳ Not Started | No implementation |
| IV | Forward and Backward Reasoning | Forward/backward chaining implementations | ⏳ Not Started | No implementation |
| IV | Symbolic Reasoning under Uncertainty | Uncertainty handling with confidence | ⏳ Not Started | No implementation |
| IV | Bayes Theorem | Bayesian probability example | ⏳ Not Started | No implementation |
| **UNIT V** | Learning by Taking Advice | Knowledge update interface | ⏳ Not Started | No implementation |
| V | Learning from Examples | Intent classifier with training data | ⏳ Not Started | No implementation |
| V | Neural Network Learning | Neural classifier implementation | ⏳ Not Started | No implementation |
| V | Expert Systems | Integrated expert system architecture | ⏳ Not Started | No implementation |
| V | Explanation-Based Learning | Feedback and learning framework | ⏳ Not Started | No implementation |

**Overall Progress:** 0/25 concepts implemented (0%)

**Foundation Status:** ✅ Complete (100%) - Frontend, backend, API, and documentation

**AI Implementation Status:** ⏳ Not Started (0%) - All AI concepts planned but not yet coded

---

## 📁 Project Structure

```
AI-Micro-Project/
├── frontend/                      # React TypeScript application
│   ├── public/                   # Static assets
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── Header.tsx
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── MessageInput.tsx
│   │   ├── services/             # API integration
│   │   │   └── api.ts
│   │   ├── types/                # TypeScript type definitions
│   │   │   └── index.ts
│   │   ├── styles/               # CSS styles
│   │   │   └── index.css
│   │   ├── App.tsx               # Main application component
│   │   └── main.tsx              # Entry point
│   ├── index.html
│   ├── package.json              # Dependencies and scripts
│   ├── tsconfig.json             # TypeScript configuration
│   ├── vite.config.ts            # Vite build configuration
│   ├── tailwind.config.js        # TailwindCSS configuration
│   └── .env.example              # Environment variables template
│
├── backend/                       # FastAPI Python application
│   ├── app/
│   │   ├── api/                  # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── chat.py           # Chat routes
│   │   ├── core/                 # Configuration
│   │   │   ├── __init__.py
│   │   │   └── config.py         # Settings
│   │   ├── models/               # Data models
│   │   │   ├── __init__.py
│   │   │   └── schemas.py        # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   │   ├── __init__.py
│   │   │   └── ai_service.py     # AI logic (placeholder)
│   │   └── __init__.py
│   ├── main.py                   # FastAPI application entry
│   ├── requirements.txt          # Python dependencies
│   ├── pytest.ini                # Pytest configuration
│   └── .env.example              # Environment variables template
│
├── docs/                          # Additional documentation
│   ├── API_REFERENCE.md
│   ├── CONTRIBUTING.md
│   ├── PROJECT_OVERVIEW.md
│   └── BUILD_SUMMARY.md
│
├── README.md                      # This file
├── SETUP_GUIDE.md                # Detailed setup instructions
├── QUICKSTART.md                 # Quick start guide
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore patterns
```

**Note:** Future AI implementations will add:
- `backend/app/ai/` directory with subdirectories for each unit:
  - `knowledge/` - Unit I implementations
  - `search/` - Unit II implementations
  - `logic/` - Unit III implementations
  - `rules/` - Unit IV implementations
  - `expert/` - Unit V implementations

---

## 🚀 Installation & Setup

### Prerequisites

Verify you have these installed:

```bash
node --version    # Should be 18+ 
python --version  # Should be 3.9+
git --version     # Any recent version
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/Rufus-R2007/AI-Micro-Project.git
cd AI-Micro-Project
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup

Open a **new terminal** window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### Step 4: Environment Configuration (Optional)

The application works with default settings. To customize:

**Backend** (`backend/.env`):
```env
API_V1_STR=/api
PROJECT_NAME=Learnify AI
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend** (`frontend/.env`):
```env
VITE_API_BASE_URL=http://localhost:8000
```

For more detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

---

## 💻 How to Run

### Running Backend and Frontend

You need **two terminal windows**:

#### Terminal 1: Start Backend

```bash
cd backend
# Activate virtual environment if not already active
venv\Scripts\activate          # Windows
source venv/bin/activate      # macOS/Linux

# Start server
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

Backend will be available at: `http://localhost:8000`

#### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

**Expected output:**
```
VITE v5.2.0  ready in 500 ms
➜  Local:   http://localhost:3000/
```

Frontend will be available at: `http://localhost:3000`

### Accessing the Application

1. Open browser: `http://localhost:3000`
2. You should see the Learnify AI chat interface
3. Type a message and press Enter or click Send
4. The bot will respond using placeholder logic

### Testing API Directly

```bash
# Health check
curl http://localhost:8000/api/health

# Get AI concepts
curl http://localhost:8000/api/chat/concepts

# Send chat message
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What is artificial intelligence?"}'
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Available Endpoints

#### 1. Root Endpoint
```http
GET /
```
Returns API metadata and capabilities.

**Response:**
```json
{
  "name": "Learnify AI",
  "description": "AI-Powered Chatbot for Student Queries",
  "version": "0.1.0",
  "status": "operational",
  "ai_capabilities": ["Knowledge Representation", "Search Algorithms", ...]
}
```

#### 2. Health Check
```http
GET /api/health
```
Verify backend service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Learnify AI Backend"
}
```

#### 3. Chat Endpoint
```http
POST /api/chat/
```
Process user message and generate response.

**Request Body:**
```json
{
  "message": "What is BFS?",
  "context": []
}
```

**Response:**
```json
{
  "response": "Breadth-First Search (BFS) is...",
  "conceptsUsed": ["Search Algorithm"],
  "confidence": 0.85
}
```

#### 4. Get AI Concepts
```http
GET /api/chat/concepts
```
List all 25 AI concepts organized by units.

**Response:**
```json
{
  "units": [
    {
      "id": 1,
      "name": "Introduction and Knowledge Representation",
      "concepts": [...],
      "implemented": false
    },
    ...
  ]
}
```

### Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** `http://localhost:8000/docs` - Test endpoints in browser
- **ReDoc:** `http://localhost:8000/redoc` - Alternative documentation view

For complete API reference with examples, see [docs/API_REFERENCE.md](docs/API_REFERENCE.md).

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests (Planned)

```bash
cd frontend
npm test
```

---

## 🤝 Contributing

Contributions are welcome! This is an educational project designed to demonstrate AI concepts.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Implement your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Areas for Contribution

- Implementing AI concepts from the roadmap
- Improving UI/UX
- Adding test coverage
- Documentation improvements
- Performance optimizations

---

## 📝 Development Notes

### Current Limitations

1. **AI Logic:** Currently uses placeholder responses. Real AI implementations are planned.
2. **Knowledge Base:** No persistent storage yet. In-memory only.
3. **Context Management:** Basic context handling. Advanced memory not implemented.
4. **Authentication:** No user authentication system.
5. **Deployment:** Not production-ready. Development only.

### Next Steps

1. **Immediate:**
   - Implement semantic network for knowledge representation
   - Add basic BFS/DFS search functionality
   - Create simple rule-based system

2. **Short-term:**
   - Implement propositional logic engine
   - Add A* search algorithm
   - Build forward/backward chaining

3. **Long-term:**
   - Complete all 25 AI concepts
   - Add persistent knowledge base
   - Deploy to production

---

## 📖 Learning Resources

### Recommended Reading

- **Artificial Intelligence: A Modern Approach** by Russell & Norvig
- **Expert Systems: Principles and Programming** by Giarratano & Riley
- **Artificial Intelligence** by Elaine Rich & Kevin Knight

### Online Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [AI Algorithms Visualization](https://www.cs.usfca.edu/~galles/visualization/)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Authors

**College AI Micro Project Team**

For questions or support, please open an issue on the repository.

---

## 🙏 Acknowledgments

- Inspiration from various open-source chatbot projects
- AI concepts from standard AI textbooks and curricula
- React and FastAPI communities for excellent documentation
- All contributors and supporters of this educational project

---

<div align="center">

**Learnify AI** — Empowering Students Through Intelligent Assistance

Made with ❤️ for education

</div>

## 🗺️ Unit-Wise Development Roadmap

### **Phase 0: Foundation** — ✅ COMPLETE

**Objective:** Set up development environment and basic application structure

**Tasks:**
- ✅ Create React frontend with TypeScript
- ✅ Set up FastAPI backend with Python
- ✅ Implement basic chat interface
- ✅ Create API integration
- ✅ Add configuration files
- ✅ Write initial documentation

**Deliverable:** Working chat application with placeholder responses

**Acceptance Criteria:**
- Both frontend and backend start without errors
- Health endpoint returns success
- Chat endpoint accepts messages and responds
- UI displays messages correctly

**Dependencies:** None

**Current Status:** ✅ Complete

**Files:**
- `frontend/src/` - React components
- `backend/app/` - FastAPI application
- Configuration and documentation files

---

### **Phase 1: Intelligent Agent (Unit I)** — ⏳ NOT STARTED

**Objective:** Design and implement intelligent agent architecture

**Tasks:**
1. Define agent specification (goals, actions, environment)
2. Implement query preprocessing pipeline
3. Create query understanding module
4. Define agent behavior for different scenarios
5. Create representative test cases

**Deliverable:** Structured agent with documented behavior

**Acceptance Criteria:**
- Agent specification document exists
- Query pipeline processes inputs correctly
- Agent handles supported, ambiguous, and unsupported queries appropriately
- Test cases demonstrate agent responses

**Dependencies:** Phase 0

**Estimated Duration:** 1 week

**Team Assignment:** 2 members (1 on architecture, 1 on testing)

**Current Status:** ⏳ Not Started

**Planned Files:**
- `backend/app/ai/knowledge/agent_spec.md`
- `backend/app/ai/knowledge/query_pipeline.py`
- `backend/app/ai/knowledge/agent_behavior.py`
- `backend/tests/test_unit1.py`

---

### **Phase 2: Search Engine (Unit II)** — ⏳ NOT STARTED

**Objective:** Implement search algorithms for knowledge retrieval

**Tasks:**
1. Design and create knowledge hierarchy (JSON)
2. Implement Breadth-First Search (BFS)
3. Implement Depth-First Search (DFS)
4. Implement Best-First Search with heuristics
5. Create heuristic evaluation functions
6. Compare algorithms on test cases
7. Document findings and trade-offs

**Deliverable:** Working search algorithms with comparative analysis

**Acceptance Criteria:**
- Knowledge hierarchy JSON exists with sample data
- All three search algorithms implemented
- Heuristics defined and documented
- Comparison results show metrics (nodes explored, time, success rate)
- Documentation explains when each algorithm is suitable

**Dependencies:** Phase 1

**Estimated Duration:** 2 weeks

**Team Assignment:** 2 members (1 on BFS/DFS, 1 on Best-First and heuristics)

**Current Status:** ⏳ Not Started

**Planned Files:**
- `backend/app/ai/search/knowledge_graph.json`
- `backend/app/ai/search/bfs.py`
- `backend/app/ai/search/dfs.py`
- `backend/app/ai/search/best_first.py`
- `backend/app/ai/search/heuristics.py`
- `backend/app/ai/search/comparison.py`
- `backend/tests/test_unit2.py`

---

### **Phase 3: Knowledge Representation (Unit III)** — ⏳ NOT STARTED

**Objective:** Implement logic-based knowledge representation and reasoning

**Tasks:**
1. Design structured knowledge base (JSON format)
2. Create predicate logic representations
3. Implement unification algorithm
4. Implement resolution in predicate logic
5. Create test cases for logical inference
6. Document knowledge representation issues and handling

**Deliverable:** Working logical inference system with test demonstrations

**Acceptance Criteria:**
- Knowledge base JSON with facts and rules exists
- Predicate class implemented
- Unification algorithm works correctly on test cases
- Resolution prover successfully proves test queries
- Documentation addresses handling of unknown facts, conflicts, ambiguity

**Dependencies:** Phase 2

**Estimated Duration:** 2 weeks

**Team Assignment:** 2 members (1 on predicates/unification, 1 on resolution/testing)

**Current Status:** ⏳ Not Started

**Planned Files:**
- `backend/app/ai/logic/knowledge_base.json`
- `backend/app/ai/logic/predicates.py`
- `backend/app/ai/logic/unification.py`
- `backend/app/ai/logic/resolution.py`
- `backend/app/ai/logic/issues.py`
- `backend/tests/test_unification.py`
- `backend/tests/test_resolution.py`

---

### **Phase 4: Reasoning Engine (Unit IV)** — ⏳ NOT STARTED

**Objective:** Implement rule-based reasoning with uncertainty handling

**Tasks:**
1. Create rule representation format (JSON)
2. Implement forward chaining algorithm
3. Implement backward chaining algorithm
4. Add uncertainty handling with confidence scores
5. Demonstrate Bayes theorem with examples
6. Generate reasoning explanations/traces

**Deliverable:** Rule-based inference engine with uncertainty handling

**Acceptance Criteria:**
- Rule base JSON with sample rules exists
- Forward chaining derives new facts correctly
- Backward chaining proves goals with proof traces
- Uncertainty handled appropriately (confidence thresholds)
- Bayes theorem example calculates probabilities correctly
- Reasoning traces are human-readable

**Dependencies:** Phase 3

**Estimated Duration:** 2 weeks

**Team Assignment:** 2 members (1 on forward/backward chaining, 1 on uncertainty/Bayes)

**Current Status:** ⏳ Not Started

**Planned Files:**
- `backend/app/ai/rules/rule_base.json`
- `backend/app/ai/rules/forward_chaining.py`
- `backend/app/ai/rules/backward_chaining.py`
- `backend/app/ai/rules/uncertainty.py`
- `backend/app/ai/rules/bayes.py`
- `backend/app/ai/rules/explanation.py`
- `backend/tests/test_unit4.py`

---

### **Phase 5: Expert System and Learning (Unit V)** — ⏳ NOT STARTED

**Objective:** Integrate all modules into expert system with learning capabilities

**Tasks:**
1. Design integrated expert system architecture
2. Create knowledge update interface with verification
3. Prepare labeled intent classification dataset (50+ examples)
4. Implement baseline classifier (TF-IDF + Naive Bayes)
5. Optionally implement neural network classifier
6. Compare classifier performance
7. Implement explanation-based learning framework
8. Document controlled feedback mechanism

**Deliverable:** Complete expert system with learning from examples

**Acceptance Criteria:**
- Expert system integrates all previous modules
- Knowledge update interface requires verification for changes
- Training dataset has at least 50 labeled examples
- Baseline classifier achieves reasonable accuracy
- Comparison shows baseline vs neural network results
- Explanation-based learning records and analyzes feedback
- Documentation explains that unreviewed feedback doesn't change authoritative rules

**Dependencies:** Phase 4

**Estimated Duration:** 3 weeks

**Team Assignment:** All 4 members (1 on architecture, 1 on classifiers, 1 on learning, 1 on testing)

**Current Status:** ⏳ Not Started

**Planned Files:**
- `backend/app/ai/expert/architecture.py`
- `backend/app/ai/expert/knowledge_update.py`
- `backend/app/ai/expert/training_data.json`
- `backend/app/ai/expert/intent_classifier.py`
- `backend/app/ai/expert/neural_classifier.py`
- `backend/app/ai/expert/explanation_learning.py`
- `backend/tests/test_unit5.py`

---

### **Phase 6: Integration and Evaluation** — ⏳ NOT STARTED

**Objective:** Integrate all modules and comprehensively evaluate the system

**Tasks:**
1. Integrate all AI modules into main application
2. Create comprehensive test suite with representative queries
3. Measure intent classification accuracy
4. Evaluate answer correctness against verified test set
5. Measure search performance (nodes explored, time)
6. Test logical inference correctness
7. Evaluate forward/backward chaining correctness
8. Measure average response times
9. Test handling of ambiguous and unsupported queries
10. Document all test results and limitations

**Deliverable:** Fully integrated system with documented evaluation results

**Acceptance Criteria:**
- All AI modules integrated into chatbot
- Test suite covers all 25 concepts
- Metrics collected and documented:
  - Intent classification accuracy
  - Answer correctness rate
  - Search algorithm performance
  - Inference correctness
  - Average response time
  - Handling of edge cases
- Limitations documented honestly
- Test results saved for project report

**Dependencies:** Phase 5

**Estimated Duration:** 2 weeks

**Team Assignment:** All 4 members (each testing different aspects)

**Current Status:** ⏳ Not Started

**Deliverable Files:**
- `backend/tests/integration_tests.py`
- `docs/EVALUATION_RESULTS.md`
- `docs/TEST_REPORT.md`

---

### **Roadmap Summary**

| Phase | Duration | Status | Dependencies |
|-------|----------|--------|--------------|
| Phase 0: Foundation | Completed | ✅ Complete | None |
| Phase 1: Intelligent Agent | 1 week | ⏳ Not Started | Phase 0 |
| Phase 2: Search Engine | 2 weeks | ⏳ Not Started | Phase 1 |
| Phase 3: Knowledge Representation | 2 weeks | ⏳ Not Started | Phase 2 |
| Phase 4: Reasoning Engine | 2 weeks | ⏳ Not Started | Phase 3 |
| Phase 5: Expert System & Learning | 3 weeks | ⏳ Not Started | Phase 4 |
| Phase 6: Integration & Evaluation | 2 weeks | ⏳ Not Started | Phase 5 |
| **Total** | **12 weeks** | **8% Complete** | - |

**Note:** Timeline assumes a 4-member team working part-time. Adjust based on actual team availability and progress.

---

## 🧪 Testing and Evaluation Plan

### Testing Strategy

#### Unit Testing
- Test each AI concept implementation independently
- Use Pytest framework for backend tests
- Aim for >80% code coverage
- Test both success and failure cases

**Files:** `backend/tests/test_unit*.py`

#### Integration Testing
- Test interactions between modules
- Verify query pipeline end-to-end
- Test knowledge base + reasoning + search integration

**Files:** `backend/tests/integration_tests.py`

#### System Testing
- Test complete chatbot functionality
- Representative student queries
- Edge cases (ambiguous, unsupported, malformed queries)

---

### Planned Evaluation Metrics

#### 1. Intent Classification Accuracy

**Measurement:**
```
Accuracy = (Correct Classifications / Total Test Queries) * 100%
```

**Test Set:** 50+ labeled queries covering all intent types

**Evaluation Method:**
1. Classify each test query
2. Compare predicted intent with true intent
3. Calculate accuracy, precision, recall, F1-score
4. Analyze confusion matrix for common errors

**Target:** >85% accuracy

**Status:** ⏳ Not yet measured (requires Phase 5 completion)

---

#### 2. Answer Correctness

**Measurement:**
```
Correctness = (Correct Answers / Total Queries) * 100%
```

**Test Set:** 100+ queries with manually verified correct answers

**Evaluation Method:**
1. Submit query to chatbot
2. Expert manually judges if response is correct, partially correct, or incorrect
3. Calculate correctness rate
4. Document common error types

**Criteria:**
- **Correct:** Factually accurate and complete
- **Partially Correct:** Some correct information but incomplete or contains minor errors
- **Incorrect:** Wrong information or completely off-topic

**Target:** >75% fully correct, >90% correct or partially correct

**Status:** ⏳ Not yet measured (requires Phase 6 completion)

---

#### 3. Search Algorithm Performance

**Metrics:**
- **Nodes Explored:** Number of nodes visited before finding answer
- **Execution Time:** Time taken to complete search (milliseconds)
- **Success Rate:** Percentage of queries successfully answered
- **Path Quality:** Optimality of path found (for Best-First)

**Evaluation Method:**
1. Run each algorithm (BFS, DFS, Best-First) on same test queries
2. Record nodes explored, time, success
3. Compare results across algorithms
4. Analyze when each algorithm performs best

**Test Cases:** 30+ queries varying in complexity

**Status:** ⏳ Not yet measured (requires Phase 2 completion)

---

#### 4. Logical Inference Correctness

**Measurement:**
```
Correctness = (Correct Inferences / Total Test Cases) * 100%
```

**Test Set:** 20+ logical reasoning problems with known correct conclusions

**Evaluation Method:**
1. Present premises and query to inference engine
2. Check if derived conclusion matches expected conclusion
3. Verify inference steps in reasoning trace
4. Test both successful proofs and unprovable queries

**Target:** 100% correctness on test cases

**Status:** ⏳ Not yet measured (requires Phase 3 completion)

---

#### 5. Forward/Backward Chaining Correctness

**Metrics:**
- **Correctness:** Does chaining derive/prove correct conclusions?
- **Completeness:** Does it find all derivable facts (forward) or prove goals when possible (backward)?
- **Efficiency:** Number of rule applications needed

**Evaluation Method:**
1. Create test knowledge bases with known derivable facts
2. Run forward chaining, verify all facts derived
3. Run backward chaining on provable goals, verify success
4. Run on unprovable goals, verify failure
5. Count rule applications

**Test Cases:** 15+ scenarios per chaining method

**Status:** ⏳ Not yet measured (requires Phase 4 completion)

---

#### 6. Response Time

**Measurement:**
```
Average Response Time = (Sum of Response Times) / Total Queries
```

**Evaluation Method:**
1. Submit 100+ queries to chatbot
2. Measure time from request to response (milliseconds)
3. Calculate average, median, 95th percentile
4. Identify slow queries and investigate causes

**Target:** 
- Average: <1000ms
- 95th percentile: <2000ms

**Status:** ⏳ Not yet measured (requires Phase 6 completion)

---

#### 7. Handling of Ambiguous/Unsupported Queries

**Qualitative Evaluation:**

Test how system handles:
- **Ambiguous Queries:** "What is the schedule?" (exam? class? assignment?)
- **Unsupported Queries:** Questions outside knowledge base
- **Malformed Queries:** Typos, incomplete sentences
- **Out-of-Scope:** Non-academic questions

**Evaluation Criteria:**
- Does system detect ambiguity and ask for clarification?
- Does system admit when it doesn't know?
- Are error messages helpful and polite?
- Does system recover gracefully from errors?

**Method:** Manual testing with 20+ edge case queries

**Status:** ⏳ Not yet evaluated (requires Phase 6 completion)

---

### Evaluation Documentation

All evaluation results will be documented in:
- `docs/EVALUATION_RESULTS.md` - Detailed metrics and analysis
- `docs/TEST_REPORT.md` - Test cases and results
- Project report - Summary for submission

**Note:** All metrics above are **planned evaluations**. No measurements have been collected yet as the AI implementations are not complete.

---

## ⚠️ Project Limitations

### Current Limitations (Foundation Phase)

1. **No Real AI Logic**
   - Current responses use simple keyword matching
   - No actual search algorithms implemented
   - No logical reasoning or inference
   - Placeholder confidence scores

2. **No Persistent Storage**
   - Knowledge base only in memory
   - No database integration
   - Chat history not saved between sessions

3. **Limited Context Management**
   - Basic message history
   - No advanced conversation state tracking
   - No user session management

4. **No Authentication**
   - No user login system
   - No authorization or access control
   - All users share same knowledge base

5. **Development Only**
   - Not production-ready
   - No deployment configuration
   - No load testing or scalability considerations

---

### Anticipated Limitations (After Implementation)

1. **Knowledge Base Scope**
   - Limited to manually entered information
   - Cannot access real-time institutional data
   - Requires regular updates by maintainers

2. **Natural Language Understanding**
   - May struggle with complex phrasings
   - Limited handling of context and pronouns
   - No support for multiple languages

3. **Search Limitations**
   - Heuristics are hand-designed, may not be optimal
   - Performance depends on knowledge structure
   - May not scale to very large knowledge bases

4. **Inference Limitations**
   - Limited to rules and facts in knowledge base
   - Cannot handle all types of logical reasoning
   - May produce incorrect inferences if rules are wrong

5. **Learning Limitations**
   - Requires labeled training data
   - Small datasets may limit classifier accuracy
   - Neural networks need substantial data to outperform baselines

6. **Uncertainty Handling**
   - Probability estimates may be rough
   - Bayesian reasoning requires accurate prior probabilities
   - Confidence scores may not always reflect true reliability

---

## 🔮 Future Enhancements

### Short-term (Next 3-6 months)

1. **Complete AI Implementation**
   - Implement all 25 AI concepts
   - Test and validate each component
   - Document results and limitations

2. **Persistent Storage**
   - Add PostgreSQL or MongoDB database
   - Store knowledge base permanently
   - Save user conversations and feedback

3. **Improved NLU**
   - Better intent classification
   - Entity extraction (dates, names, courses)
   - Handling of synonyms and variations

4. **User Authentication**
   - Student login system
   - Personalized responses based on user profile
   - Secure API endpoints

---

### Medium-term (6-12 months)

1. **Advanced Knowledge Base**
   - Integration with institutional databases
   - Automatic knowledge updates
   - Version control for knowledge

2. **Multi-Language Support**
   - Support for regional languages
   - Language detection and switching
   - Multilingual knowledge base

3. **Voice Interface**
   - Speech-to-text input
   - Text-to-speech output
   - Voice-based interaction

4. **Mobile Application**
   - React Native mobile app
   - Push notifications
   - Offline mode

---

### Long-term (1-2 years)

1. **Advanced ML Integration**
   - Integration with GPT/BERT models
   - Transfer learning from pre-trained models
   - Continuous learning from user interactions

2. **Collaborative Features**
   - Student discussion forums
   - Peer-to-peer help
   - Expert (teacher/TA) oversight

3. **Analytics Dashboard**
   - Usage statistics
   - Common queries analysis
   - Knowledge gap identification

4. **Integration with Learning Platforms**
   - Moodle integration
   - Canvas LMS integration
   - Automated assignment help

---

## 👥 Team Members

| Name | Roll Number | Role |
|------|-------------|------|
| Rufus Samuel R | URK25CS1090 | Team Lead, Backend Development |
| Yogith Joy J | URK25CS1063 | Frontend Development, UI/UX |
| Hiran Antony | URK25CS1034 | AI Implementation, Testing |
| Naveen Kumar | URK25CS1016 | Documentation, API Integration |

---

## 🔄 GitHub Development Workflow

### Repository Information
- **Repository:** https://github.com/Rufus-R2007/AI-Micro-Project
- **Main Branch:** `main`
- **Development Strategy:** Feature branches with pull requests

### Branch Strategy

```
main (production-ready code)
  │
  ├── feature/unit-1-agent (Phase 1)
  ├── feature/unit-2-search (Phase 2)
  ├── feature/unit-3-logic (Phase 3)
  ├── feature/unit-4-rules (Phase 4)
  └── feature/unit-5-expert (Phase 5)
```

### Workflow Steps

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/unit-X-description
   ```

2. **Develop and Test**
   - Write code
   - Add tests
   - Verify functionality locally

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: implement [concept] for Unit X"
   ```

   **Commit Message Format:**
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `test:` - Adding tests
   - `refactor:` - Code refactoring

4. **Push to GitHub**
   ```bash
   git push origin feature/unit-X-description
   ```

5. **Create Pull Request**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Select your feature branch
   - Add description of changes
   - Request review from team members

6. **Code Review**
   - Team members review code
   - Discuss changes and improvements
   - Address review comments

7. **Merge to Main**
   - After approval, merge PR
   - Delete feature branch
   - Pull latest main branch

### Collaboration Guidelines

1. **Before Starting Work**
   - Pull latest changes: `git pull origin main`
   - Create new feature branch
   - Check existing issues and PRs to avoid duplicate work

2. **During Development**
   - Commit frequently with clear messages
   - Push to GitHub regularly for backup
   - Update documentation as you code

3. **Before Committing**
   - Test your changes
   - Run linters/formatters
   - Ensure no secrets in code
   - Review your own changes

4. **Code Review Expectations**
   - Review PRs within 24 hours
   - Provide constructive feedback
   - Test code locally if possible
   - Approve or request changes

---

## 📖 Additional Documentation

For more detailed information, see:

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed installation and troubleshooting
- [QUICKSTART.md](QUICKSTART.md) - 5-minute quick start guide
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - Complete API documentation
- [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) - Contribution guidelines
- [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) - Detailed project overview
- [docs/BUILD_SUMMARY.md](docs/BUILD_SUMMARY.md) - Build status and file inventory

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Artificial Intelligence course instructors and teaching assistants
- Standard AI textbooks: Russell & Norvig, Giarratano & Riley
- React and FastAPI communities for excellent documentation
- Open-source contributors and educational resources

---

<div align="center">

**Learnify AI** — Empowering Students Through Intelligent Assistance

Built with ❤️ for education by the AI Micro Project Team

**Rufus Samuel R • Yogith Joy J • Hiran Antony • Naveen Kumar**

</div>
