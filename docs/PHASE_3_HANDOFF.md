# Learnify AI — Phase 3 Handoff Documentation

**Prepared By:** Yogith Joy J (URK25CS1063) — Phase 2 Lead (Search Algorithms, PathForge & Planning)  
**For:** Hiran Antony (URK25CS1034) — Phase 3 Lead (Knowledge Representation & Reasoning)  
**Project:** Learnify AI — AI-Powered University Chatbot & Academic Decision System  
**Repository:** `https://github.com/Rufus-R2007/Learnify-AI`  
**Working Base:** `phase/2-search-yogith` -> `main`

---

## 1. Executive Summary of Phase 2 Deliverables

Phase 2 successfully accomplished the goals of **Unit II: Problem-Solving Strategies and Search Techniques**, satisfying Course Outcome **CO2**:
> *Develop uninformed and informed search techniques for AI problem-solving tasks.*

All search algorithms were implemented manually in pure Python standard libraries without external graph search libraries.

### 1.1 Core Algorithms Implemented
1. **Breadth-First Search (BFS)** (`backend/app/search/bfs.py`):
   - Unweighted shortest-path directed search using `collections.deque`, visited set, and parent reconstruction.
2. **Depth-First Search (DFS)** (`backend/app/search/dfs.py`):
   - Graph exploration, path discovery, and recursion-stack cycle detection for prerequisite validation.
3. **Bidirectional Search** (`backend/app/search/bidirectional.py`):
   - Dual-frontier search expanding forward from start and backward along incoming edges from target, detecting intersection and matching BFS shortest path length.
4. **Greedy Best-First Search** (`backend/app/search/best_first.py`):
   - Informed priority-queue (`heapq`) search driven by a deterministic lexical and curricular distance heuristic.
5. **Topological Prerequisite Planner** (`backend/app/search/prerequisites.py`):
   - Complete dependency closure gathering all transitive branches, cycle checking, known topic subtraction, and Kahn's algorithm topological DAG ordering.
6. **Constraint Satisfaction & Backtracking Scheduler** (`backend/app/search/constraints.py`, `scheduler.py`):
   - Formal CSP model (Variables, Domains, Constraints) with recursive backtracking search enforcing daily study limits, non-overlapping sessions, available days, and prerequisite precedence order.

### 1.2 PathForge Signature Innovation
The interactive PathForge workbench (`frontend/src/components/PathForgeView.tsx`) delivers:
- **Interactive Knowledge Graph:** SVG canvas rendering 23 curriculum topic nodes across Units 1–5 with directed prerequisite arrows ($A \to B$), zoom/pan controls, and node inspection flyouts.
- **Topological Learning Journey:** Step-by-step ordered learning pathway detailing why each topic is included, direct prerequisites, and estimated study hours.
- **Multi-Algorithm Benchmark:** Side-by-side empirical benchmark of BFS, Bidirectional, Greedy Best-First, and DFS showing path length, nodes explored, runtime ms, and optimality explanations.
- **CSP Backtracking Study Scheduler:** Interactive weekly timetable generator with real backtrack counts, feasibility verification, and honest diagnostic capacity warnings.
- **ProofLens Live Trace:** Full execution timeline recording each search and planning stage, duration, input summary, output summary, and evidence IDs.

### 1.3 Test Suite & Quality Verification
- **Automated Tests:** 39 tests passing (`pytest tests/`) covering all 18 Phase 2 requirements + 21 Phase 1 regression tests.
- **Frontend Build:** Clean Vite + TypeScript build (`npm run build`) with zero lint or bundling errors.

---

## 2. API Endpoints Available for Phase 3

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/pathforge/topics` | GET | List all curriculum topics with estimated hours and prerequisites |
| `/api/pathforge/topics/{topic_id}` | GET | Get single topic metadata and dependencies |
| `/api/pathforge/graph` | GET | Directed node and edge payload for visualization |
| `/api/pathforge/path` | POST | Generate topological learning journey + search route |
| `/api/pathforge/compare` | POST | Benchmark BFS, Bidirectional, Greedy Best-First, DFS |
| `/api/pathforge/schedule` | POST | Solve study timetable via CSP Backtracking search |
| `/api/chat/` | POST | Chatbot agent supporting natural language planning queries |
| `/api/chat/concepts` | GET | Five-unit syllabus tracking matrix |

---

## 3. Phase 3 Architecture & Integration Roadmap for Hiran Antony

### 3.1 Learning Unit Focus
- **Unit III: Knowledge Representation and Reasoning**
- **Course Outcome:** CO3 — *Demonstrate knowledge representation formalisms and rule-based reasoning engines for academic scenario analysis.*

### 3.2 Signature Innovation for Phase 3: WhatIf Lab
- **Concept:** An interactive academic decision-support workbench allowing students to simulate "What-If" academic scenarios (e.g., prerequisite waivers, grading policies, credit loads).
- **Core Engine:** Pure Python rule engine implementing:
  1. **Forward Chaining:** Data-driven inference from student facts (e.g. credits completed, exam scores) to derived conclusions (academic standing, elective eligibility).
  2. **Backward Chaining:** Goal-driven inference determining whether a student qualifies for honors, graduation, or a specific specialization goal.
  3. **First-Order Logic / Predicate Calculus:** Formal knowledge representation using predicates:
     `Requires(course, prerequisite)`, `Completed(student, course)`, `Eligible(student, elective)`.

### 3.3 Prepared Extension Points in Codebase
1. **Rule Engine Interface:**
   `backend/app/core/interfaces.py` already contains:
   ```python
   class RuleEngine(ABC):
       @abstractmethod
       def forward_chain(self, facts: List[str]) -> List[str]:
           pass
           
       @abstractmethod
       def backward_chain(self, goal: str, facts: List[str]) -> bool:
           pass
   ```
2. **Database Integration:**
   Extend SQLite database (`backend/app/database.py`) with rules and facts tables:
   - `rules (id, name, conditions_json, conclusion, description, unit)`
   - `student_scenarios (id, student_id, facts_json, created_at)`
3. **Agent Integration:**
   In `backend/app/services/agent.py`, extend query handling to recognize rule-based queries (e.g. *"Can I take Deep Learning if I have a prerequisite waiver?"*) and dispatch them to the rule engine while attaching inference step traces to ProofLens.
4. **Frontend View:**
   - In `frontend/src/components/Sidebar.tsx`, the `WhatIf Lab` nav item is already established.
   - Build `frontend/src/components/WhatIfLabView.tsx` and wire it in `frontend/src/App.tsx` when `activeView === 'whatif'`, replacing `FutureModuleModal`.

---

## 4. How to Run & Validate Phase 2

### Backend Test Suite
```bash
cd backend
.\venv\Scripts\activate
pytest -v
```
Expected output: **39 passed in ~1.5s**.

### Running Local Development Servers
**Backend:**
```bash
cd backend
.\venv\Scripts\python -m uvicorn main:app --reload --port 8000
```
**Frontend:**
```bash
cd frontend
npm run dev
```
Navigate to `http://127.0.0.1:3000/` or `http://localhost:5173/`.
Click **PathForge** in the sidebar or top header to demonstrate the interactive curriculum planning engine.
