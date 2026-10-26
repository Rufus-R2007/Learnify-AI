# Learnify AI — Phase 4 Engineering Handoff Document

**To:** Naveen Kumar (URK25CS1016) — Phase 4 Lead: Learning & Expert Systems  
**From:** Hiran Antony R (URK25CS1034) — Phase 3 Lead: Knowledge Representation, Logical Reasoning & WhatIf Lab  
**Collaborators:** Yogith Joy J (URK25CS1063 — Phase 2), Rufus Samuel R (URK25CS1090 — Phase 1)  
**Project:** Learnify AI — AI-Powered Academic Assistant  
**Repository:** `https://github.com/Rufus-R2007/Learnify-AI`  
**Current Branch:** `phase/3-reasoning-hiran`  
**Test Suite Status:** 60/60 Tests Passing (Phase 1: 21, Phase 2: 18, Phase 3: 21)

---

## 1. Executive Summary & Current System State

Phase 3 has successfully implemented all requirements for **Unit III (Knowledge Representation & Logic)** and **Unit IV (Rule-Based & Symbolic Reasoning)**, alongside the signature **WhatIf Lab** academic decision simulator.

All code has been delivered directly into the existing repository without breaking Phase 1 conversational retrieval or Phase 2 PathForge search engines.

### Key Milestones Delivered in Phase 3:
1. **Unit III Symbolic Logic Modules (`backend/app/reasoning/`):**
   - Atomic facts with verification metadata (`VERIFIED`, `HYPOTHETICAL`, `CONTRADICTORY`) and conflict detection (`facts.py`).
   - First-Order Predicate Logic terms, constants, variables, predicates, and Horn clauses (`predicates.py`).
   - Robinson's Syntactic Unification algorithm with occurs-check and consistent multi-occurrence variable binding (`unification.py`).
   - Propositional Resolution consistency verifier detecting contradiction clauses ($\square$) (`propositional_resolution.py`).
   - Horn Clause SLD-Resolution prover with cycle avoidance and missing-premise detection (`horn_resolution.py`).

2. **Unit IV Rule-Based Reasoning Modules (`backend/app/reasoning/`):**
   - Declarative production rules and named policies with configurable thresholds and provenance (`rules.py`).
   - Forward Chaining data-driven deduction engine with fixed-point termination (`forward_chaining.py`).
   - Backward Chaining diagnostic prover building recursive SLD proof trees (`backward_chaining.py`).
   - Nonmonotonic belief revision with priority-based exception overrides (`exceptions.py`).
   - Naive Bayes Intent Classifier with Laplace smoothing ($\alpha=1.0$) routing natural language policy questions (`bayesian.py`).
   - Counterfactual scenario comparator computing exact attribute, rule activation, and status deltas (`explanations.py`).

3. **Signature Feature: WhatIf Lab Simulator (`frontend/src/components/WhatIfLabView.tsx`):**
   - 3-panel interactive decision simulator replacing the previous modal placeholder.
   - Left panel: Policy selector, attendance slider, assignment toggle, approved medical waiver override toggle, and GPA inputs.
   - Center panel: Real-time decision status hero card (`SATISFIED`, `NOT_SATISFIED`, `INCONCLUSIVE`, `OVERRIDDEN`), satisfied/missing condition cards, and side-by-side counterfactual comparison diffs.
   - Right panel: Step-by-step forward deduction trace, backward diagnostic goal prover ("Why am I eligible/ineligible?"), and propositional resolution consistency checker.
   - Seamless "Send to ProofLens" synchronization forwarding verified traces to the ProofLens panel.

---

## 2. Architecture & File Layout for Phase 4

```
Learnify-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py           # Conversational endpoint with Bayesian & Search routing
│   │   │   ├── knowledge.py      # Syllabus records and FAQ retrieval
│   │   │   ├── pathforge.py      # Phase 2: Search algorithms & CSP study scheduler
│   │   │   ├── reasoning.py      # Phase 3: Symbolic logic & rule endpoints
│   │   │   └── whatif.py         # Phase 3: WhatIf simulation & counterfactual diffs
│   │   ├── core/
│   │   │   ├── config.py         # App settings & CORS configuration
│   │   │   └── interfaces.py     # Base abstract interfaces (SearchEngine, RuleEngine, LearningEngine)
│   │   ├── models/
│   │   │   └── schemas.py        # Pydantic request/response models & ProofLens TraceStep
│   │   ├── reasoning/            # Pure Python symbolic reasoning algorithms
│   │   │   ├── predicates.py
│   │   │   ├── unification.py
│   │   │   ├── propositional_resolution.py
│   │   │   ├── horn_resolution.py
│   │   │   ├── facts.py
│   │   │   ├── rules.py
│   │   │   ├── forward_chaining.py
│   │   │   ├── backward_chaining.py
│   │   │   ├── exceptions.py
│   │   │   ├── bayesian.py
│   │   │   └── explanations.py
│   │   ├── search/               # Phase 2 graph search & CSP algorithms
│   │   └── services/
│   │       ├── agent.py          # Intelligent Agent coordinator
│   │       ├── reasoning_service.py # Phase 3 logic orchestrator
│   │       ├── whatif_service.py # Phase 3 WhatIf manager
│   │       └── search_service.py # Phase 2 PathForge manager
│   ├── database/
│   │   ├── schema.sql            # Core SQLite DDL (topics, policies, rules, verified facts)
│   │   └── seed_data.py          # Seed data for policies, rules, and student records
│   └── tests/
│       ├── test_ai_agent.py      # Phase 1: 21 tests
│       ├── test_search_algorithms.py # Phase 2: 18 tests
│       └── test_reasoning.py     # Phase 3: 21 tests
└── frontend/
    └── src/
        ├── components/
        │   ├── ChatInterface.tsx
        │   ├── Header.tsx
        │   ├── ProofLensPanel.tsx
        │   ├── Sidebar.tsx
        │   ├── PathForgeView.tsx   # Phase 2 view
        │   └── WhatIfLabView.tsx   # Phase 3 view
        ├── services/
        │   └── api.ts              # Axios API client methods
        └── types/
            └── index.ts            # Complete TypeScript interface declarations
```

---

## 3. Interfaces & Hooks Ready for Phase 4 Extension

### A. Machine Learning Intent Classification & Scoring
In `backend/app/reasoning/bayesian.py`:
- `NaiveBayesIntentClassifier` currently computes log-likelihood posteriors with Laplace smoothing for 3 classes:
  - `INTENT_REASONING_POLICY`
  - `INTENT_PATHFORGE_PLANNING`
  - `INTENT_GENERAL_KNOWLEDGE`
- **Phase 4 Opportunity:** Expand this into a full supervised machine learning classifier or decision tree in `backend/app/learning/` to predict query difficulty, course pass probabilities, or grade predictions.

### B. Certainty Factors & Uncertainty Propagation
In `backend/app/core/interfaces.py`:
- `ConfidenceScorer` and `LearningEngine` interfaces are defined for Phase 4 implementation.
- You can augment `RuleCondition` in `backend/app/reasoning/rules.py` with Certainty Factors ($CF \in [-1.0, 1.0]$) to implement MYCIN-style uncertainty combination:
  $$CF_{combined} = CF_1 + CF_2 \cdot (1 - CF_1)$$

### C. Decision Tree Recommenders in WhatIf Lab
- The WhatIf Lab view (`WhatIfLabView.tsx`) has extensible diagnostic tabs. You can easily add a 4th tab: **"ML Recommender / Decision Tree"** that presents an interactive decision tree guiding students to the fastest path to eligibility.

---

## 4. Running Tests & Development Servers

### Backend Test Suite
```bash
cd backend
python -m pytest -v
```
Expected output: **60 passed, 0 failed**.

### Running Backend Locally
```bash
cd backend
python main.py
```
Runs FastAPI at `http://localhost:8000` (Docs: `http://localhost:8000/docs`).

### Frontend Build & Development Server
```bash
cd frontend
npm run dev
```
Runs Vite dev server at `http://localhost:3000`.

To verify compilation and build:
```bash
cd frontend
npm run build
```
Builds cleanly with zero TypeScript errors.

---

## 5. Important Conventions & Guardrails
- **Illustrative Disclaimers:** When developing student recommendations or predictions, always maintain the clear disclaimer that data is for educational demonstration and does not represent official university records.
- **Scenario Isolation:** Always isolate hypothetical user inputs from authoritative verified facts (`fork_scenario` pattern in `backend/app/reasoning/facts.py`).
- **ProofLens Transparency:** When implementing Phase 4 algorithms (decision trees, certainty factors, supervised ML), measure accurate execution timings with `time.perf_counter()` and produce `TraceStep` records for ProofLens.

Best of luck with Phase 4! The foundation is solid, completely tested, and ready for your ML contributions.
