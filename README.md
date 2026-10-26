# Learnify AI — AI-Powered Chatbot for Student Queries

[![Phase 3 Complete](https://img.shields.io/badge/Phase%203-Logic%2C%20Reasoning%20%26%20WhatIf%20Lab-teal?style=for-the-badge)](https://github.com/Rufus-R2007/Learnify-AI)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-teal?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-blue?style=flat-square&logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-purple?style=flat-square&logo=vite)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-cyan?style=flat-square&logo=tailwindcss)](https://tailwindcss.com/)
[![Tests Passing](https://img.shields.io/badge/Tests-60%20Passing-brightgreen?style=flat-square)](backend/tests/)

> **Learnify AI** is an intelligent conversational student-support platform designed to answer academic questions using grounded knowledge representation, search algorithms, logical reasoning, and expert system techniques. Every conclusion is transparently explainable through **ProofLens**.

---

## 🚀 Three Signature Innovations

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

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Lucide React icons, native SVG visualization |
| **Backend** | Python 3.11+ (Python 3.13 & 3.14 compatible), FastAPI, Pydantic v2, SQLite (`sqlite3` built-in module), pure Python search & reasoning data structures |
| **Testing** | `pytest` with FastAPI `TestClient`, TypeScript compiler (`tsc`), ESLint |
| **Environment** | 100% Local execution — **No paid APIs, API keys, Docker, or external cloud accounts required** |

---

## 👥 University Team Members & Responsibilities

| Registration No. | Name | Phase | Primary Scope | Status |
|---|---|:---:|---|:---:|
| **URK25CS1034** | **Hiran Antony R** | **Phase 3** | **Knowledge Representation, FOL Unification, Propositional & Horn Resolution, WhatIf Lab Simulator** | **Completed & Tested (60/60 Tests Passing)** |
| **URK25CS1063** | **Yogith Joy J** | **Phase 2** | **Graph Search (BFS, DFS, Bidirectional, Best-First), PathForge Engine, CSP Backtracking Scheduler** | **Completed & Tested** |
| **URK25CS1090** | **Rufus Samuel R** | **Phase 1** | **Foundation, Intelligent Agent Architecture, ProofLens UI, Knowledge Base & Seed Data** | **Completed & Tested** |
| URK25CS1016 | Naveen Kumar | Phase 4 | Machine Learning Classification, Expert System Shell, Evaluation Benchmarks | Planned (Upcoming Phase 4) |

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
| **V** | Learning & Expert Systems | Expert System Architecture | End-to-end academic advisor expert system shell | Phase 4 (Naveen) | Planned |
| **V** | Learning & Expert Systems | Supervised Learning | Machine learning classification and query difficulty scoring | Phase 4 (Naveen) | Planned |
| **V** | Learning & Expert Systems | Uncertainty Handling (Bayes/CF) | Quantitative confidence scores and certainty factor propagation | Phase 4 (Naveen) | Planned |
| **V** | Learning & Expert Systems | Decision Trees | Interpretable course recommendation trees | Phase 4 (Naveen) | Planned |
| **V** | Learning & Expert Systems | System Evaluation | Precision/recall evaluation on student query benchmarks | Phase 4 (Naveen) | Planned |

---

## ⚡ Quickstart & Installation

### Prerequisites
- Python 3.11+ (Python 3.13 & 3.14 tested and verified)
- Node.js 18+ & npm (Node v24 tested and verified)

### 1. Clone & Setup Repository
```bash
git clone https://github.com/Rufus-R2007/Learnify-AI.git
cd Learnify-AI
git checkout phase/3-reasoning-hiran
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
Runs all 60 comprehensive test cases across Phase 1, Phase 2, and Phase 3:
```bash
cd backend
python -m pytest -v
```
*All 60 test cases pass in ~2.0s.*
- `test_ai_agent.py`: 21 tests (Foundation, Agent, ProofLens, Grounding)
- `test_search_algorithms.py`: 18 tests (BFS, DFS, Bidirectional, Greedy Best-First, Kahn's Topological Sort, CSP Backtracking)
- `test_reasoning.py`: 21 tests (Atomic Facts, FOL, Robinson Unification, Propositional Resolution, SLD-Resolution, Forward Chaining, Backward Chaining, Nonmonotonic Overrides, Scenario Isolation, Bayesian Routing, WhatIf API)

### Frontend Compilation & Build
```bash
cd frontend
npm run build
```
*TypeScript type-checks with zero errors; Vite builds production bundle in < 5s.*

---

## 🔌 API Endpoints Reference

### Core & Chat (Phase 1)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health status and active features |
| `POST` | `/api/chat/` | Main conversational endpoint with ProofLens trace |
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

---

## 💡 Verified Demonstration Scenarios

1. **WhatIf Decision Simulator**: Navigate to *WhatIf Lab*, adjust student attendance from 68% to 78%, and observe immediate real-time transition from `NOT_SATISFIED` to `SATISFIED`.
2. **Nonmonotonic Exception Override**: Keep attendance at 68% and toggle *Approved Medical / Sports Waiver*. Observe that the exception rule overrides default attendance requirements, switching status to `OVERRIDDEN / ELIGIBLE`.
3. **Counterfactual Diff Mode**: Click *Compare with Baseline Scenario* to view side-by-side attribute deltas, rule activation transitions, and synthesized delta explanations.
4. **Why Am I Ineligible? Diagnostic**: Open the *Backward Diagnostic* tab and prove `exam_eligible(student_01)`. Inspect the exact SLD-resolution proof tree identifying missing conditions.
5. **Propositional Policy Consistency**: Open the *Resolution* tab and click *Check Consistency* to verify zero contradictory empty clauses ($\square$) are derivable.
6. **Chatbot Policy Queries**: In the chat assistant, ask *"Am I eligible for exams if my attendance is 78%?"* or *"What if I have an approved medical exemption?"* — The agent classifies intent via Bayes' theorem and responds with full ProofLens rule firing traces.
