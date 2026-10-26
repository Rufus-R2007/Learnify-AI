"""
Implementation of SearchEngine extension interface for Learnify AI (Phase 2 - Yogith Joy J).
Connects classical AI search algorithms (BFS, DFS, Bidirectional, Greedy Best-First)
to the core application interfaces.
"""

from typing import List, Dict, Any, Optional
from app.core.interfaces import SearchEngine
from app.search.graph import LearningGraph
from app.search.bfs import breadth_first_search
from app.search.dfs import depth_first_search
from app.search.bidirectional import bidirectional_search
from app.search.best_first import greedy_best_first_search
from app.search.prerequisites import (
    generate_learning_plan,
    get_prerequisite_closure,
    LearningPlan,
)
from app.database import get_all_topics, get_all_topic_relationships


class GraphSearchEngine(SearchEngine):
    """
    SearchEngine implementation for Phase 2.
    Implements search over curriculum prerequisite graphs and state spaces.
    """

    def __init__(self, graph: Optional[LearningGraph] = None):
        self._graph = graph or self._load_graph_from_db()

    def _load_graph_from_db(self) -> LearningGraph:
        topics = get_all_topics()
        relationships = get_all_topic_relationships()
        return LearningGraph.from_database(topics, relationships)

    def refresh_graph(self) -> None:
        """Reload graph from SQLite database."""
        self._graph = self._load_graph_from_db()

    def get_graph(self) -> LearningGraph:
        return self._graph

    def find_path(
        self,
        start_topic_id: str,
        goal_topic_id: str,
        algorithm: str = "bfs"
    ) -> List[Dict[str, Any]]:
        """
        Compute a directed learning sequence from start to goal topic.
        
        Args:
            start_topic_id: Starting topic or mastered topic state
            goal_topic_id: Target learning goal
            algorithm: 'bfs', 'dfs', 'bidirectional', or 'best_first'
            
        Returns:
            List of topic node dictionaries representing the path.
        """
        algo = algorithm.lower().strip()
        if algo == "dfs":
            result = depth_first_search(self._graph, start_topic_id, goal_topic_id)
        elif algo in ["bidirectional", "bi_bfs"]:
            result = bidirectional_search(self._graph, start_topic_id, goal_topic_id)
        elif algo in ["best_first", "greedy_best_first", "heuristic"]:
            result = greedy_best_first_search(self._graph, start_topic_id, goal_topic_id)
        else:
            result = breadth_first_search(self._graph, start_topic_id, goal_topic_id)

        path_nodes: List[Dict[str, Any]] = []
        for tid in result.path:
            node = self._graph.get_node(tid)
            if node:
                path_nodes.append(node.to_dict())
            else:
                path_nodes.append({"id": tid, "name": tid})

        return path_nodes

    def get_prerequisites(self, topic_id: str) -> List[str]:
        """Return the directed prerequisite IDs for a given topic."""
        return self._graph.get_incoming(topic_id)

    def get_prerequisite_closure(self, topic_id: str) -> List[str]:
        """Return the full transitive closure of prerequisite IDs."""
        return sorted(list(get_prerequisite_closure(self._graph, topic_id)))

    def plan_learning_path(
        self,
        goal_topic_id: str,
        known_topic_ids: Optional[List[str]] = None
    ) -> LearningPlan:
        """Produce a complete topologically ordered learning plan."""
        return generate_learning_plan(self._graph, goal_topic_id, known_topic_ids)


# Singleton instance for general backend use
search_engine = GraphSearchEngine()
