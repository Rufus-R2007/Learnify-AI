# Learnify AI — AI-Powered Chatbot for Student Queries

[![Phase 2 Complete](https://img.shields.io/badge/Phase%202-Search%20Algorithms%20%26%20PathForge-indigo?style=for-the-badge)](https://github.com/Rufus-R2007/Learnify-AI)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-teal?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-blue?style=flat-square&logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-purple?style=flat-square&logo=vite)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-cyan?style=flat-square&logo=tailwindcss)](https://tailwindcss.com/)
[![Tests Passing](https://img.shields.io/badge/Tests-39%20Passing-brightgreen?style=flat-square)](backend/tests/)

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

### Innovation C — WhatIf Lab (Integration Interfaces Ready — Phase 3)
Rule-based academic decision-support workbench using Forward and Backward Chaining inference. Phase 1 & 2 establish the `RuleEngine` interface, knowledge schemas, and ProofLens event protocols.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Lucide React icons, native SVG visualization |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, SQLite (`sqlite3` built-in module), pure Python search data structures (`deque`, `heapq`) |
| **Testing** | `pytest` with FastAPI `TestClient`, TypeScript compiler (`tsc`), ESLint |
| **Environment** | 100% Local execution — **No paid APIs, API keys, Docker, or external cloud accounts required** |

---

## 👥 University Team Members & Responsibilities

| Registration No. | Name | Phase | Primary Scope | Status |
|---|---|:---:|---|:---:|
| **URK25CS1090** | **Rufus Samuel R** | **Phase 1** | **Foundation, Intelligent Agent Architecture, ProofLens UI, Knowledge Base & Seed Data** | **Completed & Tested** |
| **URK25CS1063** | **Yogith Joy J** | **Phase 2** | **Graph Search (BFS, DFS, Bidirectional, Best-First), PathForge Engine, CSP Backtracking Scheduler** | **Completed & Tested (39/39 Tests)** |
| URK25CS1034 | Hiran Antony | Phase 3 | Knowledge Representation (Semantic Nets, FOL), WhatIf Lab Rule Engine | Planned |
| URK25CS1016 | Naveen Kumar | Phase 4 | Machine Learning Classification, Expert System Shell, Evaluation Benchmarks | Planned |

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
| **III** | Knowledge Representation | Semantic Networks & Frames | Concept ontology linking topics, prerequisites, and outcomes | Phase 3 (Hiran) | Planned |
| **III** | Knowledge Representation | Propositional Logic | Academic eligibility criteria verification | Phase 3 (Hiran) | Planned |
| **III** | Knowledge Representation | First-Order Predicate Logic (FOL) | Formal prerequisite statements (e.g., `HasPrereq(x, y)`) | Phase 3 (Hiran) | Planned |
| **III** | Knowledge Representation | Resolution Refutation | Automated theorem proving for syllabus requirements | Phase 3 (Hiran) | Planned |
| **III** | Knowledge Representation | Ontologies & Description Logic | Unified curriculum taxonomy for computer science subjects | Phase 3 (Hiran) | Planned |
| **IV** | Rule-Based Reasoning | Production Rules (IF-THEN) | Academic policy rules execution for WhatIf Lab | Phase 3 (Hiran) | Planned |
| **IV** | Rule-Based Reasoning | Forward Chaining | Inferring academic standing from completed credits | Phase 3 (Hiran) | Planned |
| **IV** | Rule-Based Reasoning | Backward Chaining | Determining missing prerequisites needed for course enrollment | Phase 3 (Hiran) | Planned |
| **IV** | Rule-Based Reasoning | Conflict Resolution Strategies | Prioritizing competing academic guidelines (recency, specificity) | Phase 3 (Hiran) | Planned |
| **IV** | Rule-Based Reasoning | Truth Maintenance Systems (TMS) | Tracking assumptions and rollbacks in WhatIf simulations | Phase 3 (Hiran) | Planned |
| **V** | Learning & Expert Systems | Expert System Architecture | End-to-end academic advisor expert system shell | Phase 4 (Naveen) | Planned |
| **V** | Learning & Expert Systems | Supervised Learning | Intent classification and query difficulty scoring | Phase 4 (Naveen) | Planned |
| **V** | Learning & Expert Systems | Uncertainty Handling (Bayes/CF) | Probabilistic student success estimation in WhatIf Lab | Phase 4 (Naveen) | Planned |
| **V** | Learning & Expert Systems | Decision Trees | Interpretable course recommendation trees | Phase 4 (Naveen) | Planned |
| **V** | Learning & Expert Systems | System Evaluation | Precision/recall evaluation on student query benchmarks | Phase 4 (Naveen) | Planned |

---

## ⚡ Quickstart & Installation

### Prerequisites
- Python 3.9+ (Python 3.14 tested and verified)
- Node.js 18+ & npm (Node v24 tested and verified)

### 1. Clone & Setup Repository
```bash
git clone https://github.com/Rufus-R2007/Learnify-AI.git
cd Learnify-AI
git checkout phase/1-foundation-rufus
```

### 2. Backend Setup & Run
```bash
cd backend
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
Runs 21 comprehensive test cases validating all 12 core Phase 1 requirements:
```bash
cd backend
pytest
```
*All 21 test cases pass in < 1.0s.*

### Frontend Compilation & Linting
```bash
cd frontend
npm run build
npm run lint
```
*TypeScript type-checks with zero errors; ESLint reports zero warnings.*

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health status and active features |
| `POST` | `/api/chat/` | Main conversational endpoint with ProofLens trace |
| `GET` | `/api/chat/concepts` | Official 5-Unit Syllabus implementation matrix |
| `GET` | `/api/knowledge/` | List verified syllabus knowledge records (supports `?search=` and `?unit=`) |
| `GET` | `/api/knowledge/{id}` | Inspect a single knowledge record with provenance details |
| `GET` | `/api/knowledge/faqs` | List system educational FAQs |

---

## 💡 Verified Demonstration Scenarios

1. **Academic Definition**: Ask *"What is artificial intelligence?"* — Grounded Russell & Norvig definition returned with live ProofLens trace.
2. **Contextual Follow-Up**: Ask *"Explain breadth-first search."* followed by *"Where is it useful?"* — Model-based state resolves "it" to BFS and displays applications.
3. **Institutional Guardrail**: Ask *"What is my current attendance percentage?"* — Truthful refusal explaining that personal records are disconnected, preventing hallucinations.
4. **Epistemic Uncertainty**: Ask an out-of-domain query (*"How to bake cookies?"*) — Honest uncertainty statement without fabricating syllabus facts.
5. **Knowledge Explorer**: Click *"Knowledge Explorer"* to browse 20+ curriculum topics across Units I–V.
