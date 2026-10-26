# Learnify AI — AI-Powered Chatbot for Student Queries

[![Phase 4 Complete](https://img.shields.io/badge/Phase%204-ML%2C%20Expert%20Systems%20%26%20QA-purple?style=for-the-badge)](https://github.com/Rufus-R2007/Learnify-AI)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-teal?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-blue?style=flat-square&logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-purple?style=flat-square&logo=vite)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-cyan?style=flat-square&logo=tailwindcss)](https://tailwindcss.com/)
[![Tests Passing](https://img.shields.io/badge/Tests-72%20Passing-brightgreen?style=flat-square)](backend/tests/)

> **Learnify AI** is a unified intelligent conversational student-support platform covering all five syllabus units of the university Artificial Intelligence curriculum. Every response is grounded in authoritative curriculum knowledge, planned via search algorithms, evaluated through declarative logic, continuously improved by machine learning and adaptive memory, and transparently explained in **ProofLens**.

---

## 🚀 Four Signature Innovations

### Innovation A — ProofLens (Operational in Phase 1)
A transparent AI-execution and evidence inspection panel. For every query, ProofLens exposes:
- **Measured Pipeline Execution**: Input normalization, model-based context state tracking, goal identification, lexical retrieval, grounding verification, and response assembly.
- **Verifiable Timing**: Accurate measured millisecond duration (`time.perf_counter()`) for every stage.
- **Source Provenance**: Direct citation of authoritative textbook references (e.g., Russell & Norvig) and curated coursework.
- **Truthful Guardrails**: Explicit detection of disconnected personal/institutional data, preventing hallucinations.

### Innovation B — PathForge (Operational in Phase 2)
Goal-oriented prerequisite navigation and personalized study route finding using classical AI search:
- **Graph Search Algorithms**: Pure Python implementations of Breadth-First Search (BFS), Depth-First Search (DFS), Directed Bidirectional Search, and Greedy Best-First Search.
- **Topological Learning Journey**: Complete prerequisite closure calculation removing already-mastered concepts and Kahn's algorithm dependency ordering.
- **Interactive Visual Knowledge Graph**: Interactive SVG canvas displaying 23 curriculum topic nodes and 24 directed prerequisite relationships.
- **CSP Backtracking Study Scheduler**: Formal Constraint Satisfaction Problem model (Variables, Domains, Constraints) with recursive backtracking search enforcing daily limits, non-overlapping slots, and prerequisite order.
- **ProofLens Search Traces**: Authentic step-by-step frontier and backtracking execution events.

### Innovation C — WhatIf Lab (Operational in Phase 3)
Interactive academic decision-support workbench powered by First-Order Logic and Symbolic Rule-Based Reasoning:
- **First-Order Predicate Logic**: Atomic terms, variables, constants, compound terms, and Horn clauses with string serialization.
- **Robinson Unification Algorithm**: Full syntactic unification with variable-to-variable binding, repeated variable consistency, and strict occurs-check preventing infinite terms.
- **Propositional Resolution Engine**: CNF clause conversion, resolvent generation, and automated refutation theorem prover checking policy consistency or deriving contradiction ($\square$).
- **Horn Clause SLD-Resolution**: Goal-directed linear resolution over definite clauses with cycle detection and missing premise diagnostics.
- **Declarative Rule Engine**: Named policies (`policy-exam-eligibility-v1`, `policy-exception-waiver-v1`, `policy-incomplete-info-v1`, `policy-academic-honors-v1`) with configurable antecedent conditions and provenance.
- **Forward Chaining Deduction**: Data-driven iterative deduction deriving intermediate standing to final decisions with fixed-point termination.
- **Backward Chaining Prover**: Goal-driven diagnostic answering *"Why am I eligible or ineligible?"* by building recursive SLD proof trees.
- **Nonmonotonic Exception Overrides**: Priority-based belief revision allowing approved medical waivers or departmental exemptions to override default constraints without mutating authoritative verified records.
- **Naive Bayes Intent Routing**: Probabilistic classifier with Laplace smoothing ($\alpha=1.0$) routing natural language policy inquiries to the symbolic engine.
- **WhatIf 3-Panel Simulator**: Interactive frontend decision workbench (`WhatIfLabView.tsx`) with attendance sliders, exception toggles, side-by-side counterfactual diffs, and live ProofLens execution sync.

### Innovation D — Learning & Quality Assurance Lab (Operational in Phase 4)
Continuous improvement, adaptive memory, and machine learning engine implementing all Unit V concepts:
- **Concept 1 (Rote Learning)**: Verified solution memory cache in SQLite (`verified_memory`) with sub-millisecond retrieval latency (< 1.0 ms) on repeated queries, hit counters, and privacy safeguards barring individualized student data.
- **Concept 2 (Learning by Taking Advice)**: Student feedback ingestion with optional suggested corrections, human-in-the-loop reviewer approval desk, authoritative knowledge base updating, immutable audit logging (`knowledge_history`), and automatic cache invalidation.
- **Concept 3 (Inductive Learning)**: Supervised scikit-learn TF-IDF Vectorizer + Logistic Regression intent classifier evaluated on a held-out test split (140 train / 35 test samples) achieving **85.71% test accuracy** and **0.8549 macro F1-score** across 7 curriculum classes.
- **Concept 4 (Learning by Analogy)**: Case-based reasoning matching queries against 24 solved curriculum cases via cosine similarity, with strict policy safeguards routing individualized rule queries to WhatIf Lab.
- **Concept 5 (Unified Expert System Architecture)**: Synthesis of Knowledge Base, Search Engine, Inference Engine, Learning Engine, and Explanation Facility into a cohesive intelligent assistant.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Lucide React icons, native SVG visualization |
| **Backend** | Python 3.11+ (Python 3.13 & 3.14 compatible), FastAPI, Pydantic v2, scikit-learn, NumPy, Pandas, SQLite (`sqlite3` built-in module), pure Python search & reasoning data structures |
| **Testing** | `pytest` with FastAPI `TestClient`, TypeScript compiler (`tsc`), ESLint |
| **Environment** | 100% Local execution — **No paid APIs, API keys, Docker, or external cloud accounts required** |

---

## 👥 University Team Members & Responsibilities

| Registration No. | Name | Phase | Primary Scope | Status |
|---|---|:---:|---|:---:|
| **URK25CS1016** | **Naveen Kumar** | **Phase 4** | **Unit V: Learning Engine (Rote Learning, Taking Advice, Inductive ML Intent Classification, Analogy CBR), Expert System Synthesis, Final QA** | **Completed & Tested (72/72 Tests Passing)** |
| **URK25CS1034** | **Hiran Antony R** | **Phase 3** | **Units III & IV: Knowledge Representation, FOL Unification, Propositional & Horn Resolution, WhatIf Lab Simulator** | **Completed & Tested** |
| **URK25CS1063** | **Yogith Joy J** | **Phase 2** | **Unit II: Graph Search (BFS, DFS, Bidirectional, Best-First), PathForge Engine, CSP Backtracking Scheduler** | **Completed & Tested** |
| **URK25CS1090** | **Rufus Samuel R** | **Phase 1** | **Unit I: Foundation, Intelligent Agent Architecture, ProofLens UI, Knowledge Base & Seed Data** | **Completed & Tested** |

---

## 📚 Five-Unit Syllabus Coverage Tracker

| Unit | Syllabus Theme | Concept Group | Actual Application Use Case | Responsible Phase | Status |
|:---:|---|---|---|:---:|:---:|
| **I** | **Foundations of AI** | Artificial Intelligence Concepts | Query normalization, perception, and educational AI concept definitions | Phase 1 (Rufus) | **Implemented & Tested** |
| **I** | Foundations of AI | Applications of AI | Domain categorization of queries (Healthcare, Finance, Education) | Phase 1 (Rufus) | **Implemented & Tested** |
| **I** | Foundations of AI | Behavioral Characteristics of Agents | Perception, reactivity, rational responses, truthful uncertainty guards | Phase 1 (Rufus) | **Implemented & Tested** |
| **I** | Foundations of AI | Typical Intelligent Agents | Simple reflex for greetings; model-based state for anaphora follow-ups | Phase 1 (Rufus) | **Implemented & Tested** |
| **I** | Foundations of AI | Problem-Solving Formulation | Internal representation (state, goal, actions, result, status) | Phase 1 (Rufus) | **Implemented & Tested** |
| **II** | **Problem-Solving & Search** | Uninformed Search (BFS & DFS) | Prerequisite shortest route and dependency cycle validation in PathForge | Phase 2 (Yogith) | **Implemented & Tested** |
| **II** | Problem-Solving & Search | Bidirectional Search | Dual-frontier directed search connecting current knowledge to goal | Phase 2 (Yogith) | **Implemented & Tested** |
| **II** | Problem-Solving & Search | Informed Search (Greedy Best-First) | Heuristic-guided priority search over curriculum knowledge space | Phase 2 (Yogith) | **Implemented & Tested** |
| **II** | Problem-Solving & Search | Prerequisite Topological Ordering | Mandatory prerequisite closure and Kahn's DAG dependency sequence | Phase 2 (Yogith) | **Implemented & Tested** |
| **II** | Problem-Solving & Search | Constraint Satisfaction (CSP) & Backtracking | Study timetable generation with daily hours, slot limits, and prerequisite precedence | Phase 2 (Yogith) | **Implemented & Tested** |
| **III** | **Knowledge Representation** | Atomic Facts & Provenance | Structured educational fact storage, verified vs hypothetical records, conflict detection | Phase 3 (Hiran) | **Implemented & Tested** |
| **III** | Knowledge Representation | First-Order Predicate Logic (FOL) | Terms, constants, variables, predicates, compound terms, and Horn clauses | Phase 3 (Hiran) | **Implemented & Tested** |
| **III** | Knowledge Representation | Robinson Unification Algorithm | Syntactic unification with variable binding, repeated-variable consistency, and occurs-check | Phase 3 (Hiran) | **Implemented & Tested** |
| **III** | Knowledge Representation | Propositional Resolution | Refutation resolution over CNF clauses with contradiction detection ($\square$) | Phase 3 (Hiran) | **Implemented & Tested** |
| **III** | Knowledge Representation | Horn-Clause SLD-Resolution | Goal-directed linear resolution over definite clauses with cycle detection | Phase 3 (Hiran) | **Implemented & Tested** |
| **IV** | **Rule-Based Reasoning** | Declarative Rules & Policies | Named policy definitions with numeric thresholds, relational operators, and provenance | Phase 3 (Hiran) | **Implemented & Tested** |
| **IV** | Rule-Based Reasoning | Forward Chaining Deduction | Data-driven iterative deduction with fixed-point termination | Phase 3 (Hiran) | **Implemented & Tested** |
| **IV** | Rule-Based Reasoning | Backward Chaining Diagnostic Prover | Goal-directed "Why am I eligible/ineligible?" diagnostic generating SLD proof trees | Phase 3 (Hiran) | **Implemented & Tested** |
| **IV** | Rule-Based Reasoning | Nonmonotonic Exception Overrides | Priority-based belief revision overriding default rules upon approved exceptions | Phase 3 (Hiran) | **Implemented & Tested** |
| **IV** | Rule-Based Reasoning | Bayesian Intent Routing | Naive Bayes classifier with Laplace smoothing routing policy questions to reasoning | Phase 3 (Hiran) | **Implemented & Tested** |
| **V** | **Learning & Expert Systems** | Rote Learning | Verified solution memory cache with hit tracking and sub-ms latency | Phase 4 (Naveen) | **Implemented & Tested** |
| **V** | Learning & Expert Systems | Learning by Taking Advice | Feedback ingestion, reviewer approval workflow, and authoritative KB updates | Phase 4 (Naveen) | **Implemented & Tested** |
| **V** | Learning & Expert Systems | Inductive Learning | scikit-learn TF-IDF + Logistic Regression intent classifier (85.71% test accuracy) | Phase 4 (Naveen) | **Implemented & Tested** |
| **V** | Learning & Expert Systems | Learning by Analogy | Case-based reasoning matching solved cases with policy safeguard routing | Phase 4 (Naveen) | **Implemented & Tested** |
| **V** | Learning & Expert Systems | Expert System Architecture | 5-component unified architecture (KB, Search, Inference, Learning, ProofLens) | Phase 4 (Naveen) | **Implemented & Tested** |

---

## ⚡ Quickstart & Installation

### Prerequisites
- Python 3.11+ (Python 3.13 & 3.14 tested and verified)
- Node.js 18+ & npm (Node v24 tested and verified)

### 1. Clone & Setup Repository
```bash
git clone https://github.com/Rufus-R2007/Learnify-AI.git
cd Learnify-AI
```

### 2. Backend Setup & Run
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
*Backend runs on `http://localhost:8000` with Swagger UI at `http://localhost:8000/docs`.*

### 3. Frontend Setup & Run
```bash
cd ../frontend
npm install
npm run dev
```
*Frontend runs on `http://localhost:3000`.*

---

## 🧪 Testing

### Backend Automated Test Suite
Runs all 72 comprehensive test cases across all four project phases:
```bash
cd backend
python -m pytest -v
```
*All 72 test cases pass in ~2.7s.*
- `test_ai_agent.py`: 21 tests (Foundation, Agent, ProofLens, Grounding)
- `test_search_algorithms.py`: 18 tests (BFS, DFS, Bidirectional, Greedy Best-First, Kahn's Topological Sort, CSP Backtracking)
- `test_reasoning.py`: 21 tests (Atomic Facts, FOL, Robinson Unification, Propositional Resolution, SLD-Resolution, Forward Chaining, Backward Chaining, Nonmonotonic Overrides, Scenario Isolation, Bayesian Routing, WhatIf API)
- `test_learning_and_expert.py`: 12 tests (Rote Cache Hit/Miss, Memory Invalidation, Taking Advice Approval Desk, Inductive Classifier Accuracy & Uncertainty, Analogy Safeguards, End-to-End Expert System)

### Frontend Compilation & Quality
```bash
cd frontend
npm run lint
npm run build
```
*ESLint passes with 0 errors and 0 warnings; TypeScript compiles with zero errors; Vite builds production bundle in < 2.0s.*

---

## 🔌 API Endpoints Reference

### Core & Chat (Phase 1)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health status and active features |
| `POST` | `/api/chat/` | Main conversational endpoint with ProofLens trace, ML intent, and analogy suggestions |
| `GET` | `/api/chat/concepts` | Official 5-Unit Syllabus implementation matrix |
| `GET` | `/api/knowledge/` | List verified syllabus knowledge records |
| `GET` | `/api/knowledge/{id}` | Inspect a single knowledge record with provenance details |
| `GET` | `/api/knowledge/faqs` | List system educational FAQs |

### PathForge Search & Planning (Phase 2)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/pathforge/topics` | List curriculum topics |
| `GET` | `/api/pathforge/graph` | Directed prerequisite graph |
| `POST` | `/api/pathforge/path` | Optimal prerequisite learning route (BFS, DFS, Bidirectional, Best-First) |
| `POST` | `/api/pathforge/compare` | Multi-algorithm search comparison with explored order and metrics |
| `POST` | `/api/pathforge/schedule` | Constraint Satisfaction backtracking study scheduler |

### WhatIf Lab & Symbolic Reasoning (Phase 3)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/whatif/policies` | Retrieve policies configured with baseline simulation presets |
| `POST` | `/api/whatif/evaluate` | Forward-chaining evaluation of interactive scenario adjustments |
| `POST` | `/api/whatif/compare` | Exact counterfactual comparison between baseline and modified facts |
| `GET` | `/api/reasoning/policies` | List declarative policies with full rule definitions |
| `GET` | `/api/reasoning/rules` | Inspect declarative production rules and antecedents |
| `POST` | `/api/reasoning/prove` | Backward chaining goal diagnosis via SLD-resolution |
| `POST` | `/api/reasoning/consistency` | Validate policy logical consistency using Propositional Resolution |

### Learning Engine & Expert Systems (Phase 4)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/learning/feedback/` | Submit student advice with suggested correction |
| `GET` | `/api/learning/feedback/` | List staged feedback submissions for reviewer inspection |
| `POST` | `/api/learning/feedback/{id}/review` | Reviewer approval/rejection updating knowledge base and invalidating cache |
| `GET` | `/api/learning/knowledge-history` | Audit trail of knowledge base modifications |
| `GET` | `/api/learning/memory/stats` | Rote learning verified memory cache hit and latency statistics |
| `GET` | `/api/learning/memory/items` | Inspect cached memory query entries |
| `POST` | `/api/learning/memory/invalidate` | Invalidate verified memory entries |
| `GET` | `/api/learning/ml-metrics` | Inductive classifier held-out evaluation metrics & confusion matrix |
| `POST` | `/api/learning/predict-intent` | Interactive ML intent classification with class probabilities |
| `GET` | `/api/learning/analogies` | Case-based reasoning query matching against 24 solved cases |
| `GET` | `/api/learning/expert-system-architecture` | Subsystem definitions of the unified expert system |

---

## 💡 Faculty Demonstration Walkthrough Script (~3 Minutes)

1. **Scene 1: Conversational Intelligence & ProofLens**
   - Ask *"What is breadth-first search?"*
   - Observe the instant response and click **Inspect ProofLens**.
   - Note the chronological stages: Input Normalization, ML Intent Classification, Verified Memory Retrieval, Grounding Verification, and Response Assembly.
2. **Scene 2: Rote Learning Cache Hit (< 1ms)**
   - Ask the exact same question again: *"What is breadth-first search?"*
   - Observe the **`⚡ Rote Cache Hit (<1ms)`** badge on the response bubble and sub-millisecond execution time in ProofLens.
3. **Scene 3: Learning by Analogy**
   - Notice the **`💡 Related Solved Questions (Learning by Analogy)`** recommendations beneath the response.
   - Click one of the suggestions to see how the system assists students with related solved curriculum cases.
4. **Scene 4: Learning by Taking Advice (Student Submission)**
   - Click the **Thumbs Down** icon on any answer, enter a suggested correction (e.g. *"BFS uses a FIFO queue with space complexity O(b^d)"*), and click **Submit Advice**.
   - Observe the confirmation that advice was submitted to the reviewer desk.
5. **Scene 5: Reviewer Desk & Authoritative Update**
   - Click **Learning Lab** in the top navigation or sidebar.
   - Select the submitted advice in the **Reviewer Desk**, check *"Update authoritative knowledge base"*, and click **Approve Advice & Update KB**.
   - Note the instant audit log created in **Knowledge Modification History** and the automatic cache invalidation.
6. **Scene 6: Inductive ML Intent Classifier Sandbox**
   - Switch to the **Inductive ML** tab in Learning Lab.
   - Review genuine measured held-out test metrics: **85.71% Accuracy**, **0.8549 Macro F1**, and the **7x7 Confusion Matrix**.
   - Type queries in the live sandbox (e.g., *"Can I write exams with 72% attendance?"*) and watch real-time class probability distribution bars animate.
7. **Scene 7: PathForge Search & CSP Scheduler (Phase 2)**
   - Open **PathForge**, select **Machine Learning** as the target topic, and click **Find Prerequisite Path**.
   - Compare BFS, DFS, Bidirectional, and Greedy Best-First searches; then generate a conflict-free study schedule with CSP backtracking.
8. **Scene 8: WhatIf Lab Counterfactual Reasoning (Phase 3)**
   - Open **WhatIf Lab**, adjust student attendance below 75%, and toggle an **Approved Medical / Sports Waiver**.
   - Observe the nonmonotonic exception rule override the default requirement, proving eligibility without altering the database.
