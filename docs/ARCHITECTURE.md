# Learnify AI — System Architecture Document (Phase 1)

**Responsible Lead:** Rufus Samuel R (URK25CS1090)  
**Project Phase:** 1 — Foundation, Intelligent Agent Architecture, ProofLens UI

---

## 1. Architectural Overview

Learnify AI follows a decoupled client-server architecture designed for university-level explainability, modular extension across 4 phases, and strict grounding in educational knowledge without relying on opaque commercial LLM APIs.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        React + Vite Frontend                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────────┐ │
│  │  Sidebar & Nav   │  │  Chat Interface  │  │  ProofLens Live Panel │ │
│  │  • New Chat      │  │  • Messages      │  │  • Stage Timings (ms) │ │
│  │  • Explorer      │  │  • Suggestions   │  │  • Grounding Metrics  │ │
│  │  • Syllabus/Team │  │  • Composer      │  │  • Source Citations   │ │
│  └──────────────────┘  └──────────────────┘  └───────────────────────┘ │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │ HTTP / JSON
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         FastAPI Backend                                │
│                                                                        │
│   POST /api/chat/ ──────► IntelligentAgent.process()                   │
│                                │                                       │
│   STAGE 1: Perception & Analysis (Tokenization, Entity Detection)      │
│   STAGE 2: Model-Based Context Resolution (Anaphora Resolution)        │
│   STAGE 3: Goal-Oriented Classification (Reflex vs Academic vs Guard)  │
│   STAGE 4: Lexical Retrieval (Inverted Term Matching)                  │
│   STAGE 5: Evidence Grounding & Verification (Relevance Threshold)     │
│   STAGE 6: Response Assembly & ProofLens Trace Capture                 │
│                                │                                       │
│                                ▼                                       │
│                 SQLite Knowledge Base (learnify.db)                    │
│    • topics            • sources             • knowledge               │
│    • faq               • topic_relationships                           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Intelligent Agent Components (Unit I Concepts)

1. **`PerceptionModule` (`backend/app/services/agent.py`)**
   - Normalizes text, extracts non-stopword tokens, detects technical concepts (BFS, DFS, A*, ML, Logic, Expert Systems).
   - Concept: *Agent Perception & Input Filtering*.

2. **`ModelBasedState` (`backend/app/services/agent.py`)**
   - Keeps track of conversation turn history without requiring user accounts or third-party cookies.
   - Detects anaphoric expressions (e.g., *"Where is it used?"*, *"How does it work?"*) and resolves the antecedent entity from prior turns.
   - Concept: *Model-Based Reflex Agent with Internal State*.

3. **`GoalOrientedClassifier` (`backend/app/services/agent.py`)**
   - Classifies query into:
     - `GOAL_GREETING`: Handled via deterministic Reflex.
     - `GOAL_CAPABILITY`: Handled via documented capability mapping.
     - `GOAL_PERSONAL_OR_INSTITUTIONAL`: Handled via Truthful Uncertainty guard (refusing to invent attendance, marks, fees).
     - `GOAL_KNOWLEDGE_QUERY`: Routed to database search.
     - `GOAL_FAQ`: Routed to FAQ search.
   - Concept: *Goal-Based Agent Decision Making*.

4. **`ProofLensTracer`**
   - Measures precise execution timing via `time.perf_counter()`.
   - Records stage name, algorithm, input summary, output summary, duration in milliseconds, status, and supporting evidence IDs.

---

## 3. Database Schema

- **`sources`**: `(id, name, description, url)`
- **`topics`**: `(id, name, unit, description)`
- **`knowledge`**: `(id, title, content, topic_id, source_id, keywords, created_at)`
- **`faq`**: `(id, question, answer, category, source_id)`
- **`topic_relationships`**: `(parent_id, child_id, relationship)` — *Prerequisite graph edges for Phase 2 PathForge*.

Seeded with 20+ verified curriculum records covering Units I through V. All insertions use `INSERT OR IGNORE` ensuring 100% idempotent reproducibility.
