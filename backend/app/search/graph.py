"""
Knowledge Graph data structures and Directed Graph representations for Learnify AI (Phase 2).

Conventions:
- Directed edge: parent_id -> child_id means parent_id is a PREREQUISITE for child_id.
- To reach or master a child topic, its prerequisite parent topics must be learned first.
- Forward search: follows outgoing edges (from prerequisite towards dependent topics).
- Reverse search: follows incoming edges (from goal towards its prerequisites).
"""

from typing import List, Dict, Optional, Tuple, Set, Any
from dataclasses import dataclass, field


@dataclass
class TopicNode:
    id: str
    name: str
    unit: int = 1
    category: str = "General"
    description: str = ""
    estimated_hours: int = 3
    prerequisites: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "category": self.category,
            "description": self.description,
            "estimated_hours": self.estimated_hours,
            "prerequisites": list(self.prerequisites),
            "dependents": list(self.dependents),
        }


class LearningGraph:
    """
    Directed Knowledge Graph of academic topics and prerequisite relationships.
    Strictly unweighted directed graph with manual standard Python data structures.
    """

    def __init__(self):
        self.nodes: Dict[str, TopicNode] = {}
        # Outgoing edges: parent -> children (prerequisite -> dependent)
        self.outgoing: Dict[str, List[str]] = {}
        # Incoming edges: child -> parents (dependent -> prerequisites)
        self.incoming: Dict[str, List[str]] = {}

    def add_node(self, node: TopicNode) -> None:
        self.nodes[node.id] = node
        if node.id not in self.outgoing:
            self.outgoing[node.id] = []
        if node.id not in self.incoming:
            self.incoming[node.id] = []

    def add_edge(self, parent_id: str, child_id: str) -> None:
        """Add directed edge: parent_id is a prerequisite for child_id."""
        if parent_id not in self.outgoing:
            self.outgoing[parent_id] = []
        if child_id not in self.incoming:
            self.incoming[child_id] = []

        if child_id not in self.outgoing[parent_id]:
            self.outgoing[parent_id].append(child_id)
        if parent_id not in self.incoming[child_id]:
            self.incoming[child_id].append(parent_id)

        # Update node internal lists if nodes exist
        if parent_id in self.nodes and child_id not in self.nodes[parent_id].dependents:
            self.nodes[parent_id].dependents.append(child_id)
        if child_id in self.nodes and parent_id not in self.nodes[child_id].prerequisites:
            self.nodes[child_id].prerequisites.append(parent_id)

    def get_node(self, node_id: str) -> Optional[TopicNode]:
        return self.nodes.get(node_id)

    def has_node(self, node_id: str) -> bool:
        return node_id in self.nodes

    def get_outgoing(self, node_id: str) -> List[str]:
        """Return nodes that require this node (forward dependents)."""
        return list(self.outgoing.get(node_id, []))

    def get_incoming(self, node_id: str) -> List[str]:
        """Return prerequisite nodes required by this node (backward predecessors)."""
        return list(self.incoming.get(node_id, []))

    def get_all_nodes(self) -> List[TopicNode]:
        return list(self.nodes.values())

    def detect_cycles(self) -> Tuple[bool, Optional[List[str]]]:
        """
        DFS cycle detection using 3-color state tracking:
        0 = WHITE (unvisited), 1 = GRAY (visiting on recursion stack), 2 = BLACK (visited).
        Returns (has_cycle, cycle_path_as_list_of_ids).
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        colors: Dict[str, int] = {node_id: WHITE for node_id in self.nodes}
        parent_map: Dict[str, Optional[str]] = {}

        def dfs(u: str, path: List[str]) -> Optional[List[str]]:
            colors[u] = GRAY
            path.append(u)

            for v in self.outgoing.get(u, []):
                if v not in colors:
                    continue
                if colors[v] == GRAY:
                    # Cycle detected! Extract cycle path
                    cycle_start_idx = path.index(v)
                    return path[cycle_start_idx:] + [v]
                if colors[v] == WHITE:
                    parent_map[v] = u
                    res = dfs(v, path)
                    if res:
                        return res

            path.pop()
            colors[u] = BLACK
            return None

        for node_id in self.nodes:
            if colors[node_id] == WHITE:
                cycle = dfs(node_id, [])
                if cycle:
                    return True, cycle

        return False, None

    @classmethod
    def from_database(
        cls,
        db_topics: List[Dict[str, Any]],
        db_relationships: List[Dict[str, str]]
    ) -> 'LearningGraph':
        """Factory: Build LearningGraph from database records."""
        graph = cls()
        for t in db_topics:
            node = TopicNode(
                id=t["id"],
                name=t["name"],
                unit=t.get("unit", 1),
                category=t.get("category", "General"),
                description=t.get("description", ""),
                estimated_hours=t.get("estimated_hours", 3),
                prerequisites=[],
                dependents=[],
            )
            graph.add_node(node)

        for rel in db_relationships:
            p = rel["parent_id"]
            c = rel["child_id"]
            graph.add_edge(p, c)

        return graph
