# Learnify AI — Phase 2 Handoff Notes

**Prepared By:** Rufus Samuel R (URK25CS1090) — Phase 1 Lead  
**For:** Yogith Joy J (URK25CS1063) — Phase 2 Lead (Search & PathForge)

---

## 1. What Has Been Completed in Phase 1

1. **Working Full-Stack Foundation**:
   - FastAPI server with SQLite database and lifespan initialization.
   - React + TypeScript + Vite + Tailwind CSS frontend with ProofLens panel.
2. **Prepared Database Edges**:
   - Table `topic_relationships` in `learnify.db` contains prerequisite directed edges (e.g., `topic-ai-foundations` -> `topic-search-bfs-dfs` -> `topic-heuristic-search`).
3. **Prepared Extension Interface**:
   - `backend/app/core/interfaces.py` defines `SearchEngine(ABC)`:
     ```python
     class SearchEngine(ABC):
         @abstractmethod
         def find_path(self, start_topic_id: str, goal_topic_id: str, algorithm: str = "bfs") -> List[Dict[str, Any]]:
             pass
             
         @abstractmethod
         def get_prerequisites(self, topic_id: str) -> List[str]:
             pass
     ```
4. **UI Extension Points**:
   - Sidebar includes navigation for `PathForge` (`Phase 2`).
   - Modal preview in `FutureModuleModal.tsx` is ready to be swapped with the interactive graph visualization.

---

## 2. Phase 2 Tasks for Yogith Joy J

1. **Implement `SearchEngine`**:
   - Create `backend/app/services/search_engine.py` inheriting from `SearchEngine`.
   - Implement Uninformed Search: Breadth-First Search (BFS) and Depth-First Search (DFS) over topic prerequisite nodes.
   - Implement Informed Search: A* search using heuristic cost (e.g., estimated study hours or topic complexity difference).
2. **Expose PathForge API**:
   - Add `POST /api/pathforge/route` accepting `start_topic_id` and `goal_topic_id`.
   - Return ordered nodes, total path cost, and nodes expanded.
3. **Interactive PathForge UI**:
   - In `frontend/src/components/`, build `PathForgeView.tsx` showing the graph nodes and optimal path.
4. **Attach Search Trace to ProofLens**:
   - When a PathForge query runs, emit real ProofLens trace events (e.g. `Stage: Frontier Expansion`, `Method: A* Priority Queue`).
