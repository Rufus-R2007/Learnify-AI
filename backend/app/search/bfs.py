"""
Breadth-First Search (BFS) for Learnify AI (Phase 2).
Finds the unweighted shortest directed connection between two topics in the knowledge graph.
Uses standard Python collections.deque, visited set, and parent map.
"""

import time
from collections import deque
from typing import List, Dict, Optional, Any
from app.search.graph import LearningGraph


class BFSResult:
    def __init__(
        self,
        start_node: str,
        target_node: str,
        reachable: bool,
        path: List[str],
        edge_count: int,
        visited_nodes: List[str],
        explored_count: int,
        duration_ms: float,
    ):
        self.algorithm = "bfs"
        self.start_node = start_node
        self.target_node = target_node
        self.reachable = reachable
        self.path = path
        self.edge_count = edge_count
        self.visited_nodes = visited_nodes
        self.explored_count = explored_count
        self.duration_ms = duration_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "start_node": self.start_node,
            "target_node": self.target_node,
            "reachable": self.reachable,
            "path": self.path,
            "edge_count": self.edge_count,
            "visited_nodes": self.visited_nodes,
            "explored_count": self.explored_count,
            "duration_ms": self.duration_ms,
        }


def breadth_first_search(
    graph: LearningGraph,
    start_node: str,
    target_node: str
) -> BFSResult:
    """
    Execute Breadth-First Search on a directed LearningGraph.
    
    Traverses forward edges (parent -> child) to find the shortest
    path in terms of edge count from start_node to target_node.
    """
    t0 = time.perf_counter()

    if not graph.has_node(start_node) or not graph.has_node(target_node):
        duration_ms = (time.perf_counter() - t0) * 1000.0
        return BFSResult(
            start_node=start_node,
            target_node=target_node,
            reachable=False,
            path=[],
            edge_count=0,
            visited_nodes=[],
            explored_count=0,
            duration_ms=round(duration_ms, 3),
        )

    # Trivial case: start is target
    if start_node == target_node:
        duration_ms = (time.perf_counter() - t0) * 1000.0
        return BFSResult(
            start_node=start_node,
            target_node=target_node,
            reachable=True,
            path=[start_node],
            edge_count=0,
            visited_nodes=[start_node],
            explored_count=1,
            duration_ms=round(duration_ms, 3),
        )

    # Standard FIFO queue for BFS frontier
    queue: deque[str] = deque([start_node])
    visited: set[str] = {start_node}
    parent: Dict[str, Optional[str]] = {start_node: None}
    explored_order: List[str] = []

    target_found = False

    while queue:
        current = queue.popleft()
        explored_order.append(current)

        if current == target_node:
            target_found = True
            break

        # Explore outgoing neighbors (forward along prerequisite edges)
        for neighbor in graph.get_outgoing(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                if neighbor == target_node:
                    # Early goal detection
                    target_found = True
                    explored_order.append(neighbor)
                    break
        if target_found:
            break

    duration_ms = (time.perf_counter() - t0) * 1000.0

    if not target_found:
        return BFSResult(
            start_node=start_node,
            target_node=target_node,
            reachable=False,
            path=[],
            edge_count=0,
            visited_nodes=explored_order,
            explored_count=len(explored_order),
            duration_ms=round(duration_ms, 3),
        )

    # Reconstruct shortest path from target back to start
    path: List[str] = []
    curr: Optional[str] = target_node
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()

    return BFSResult(
        start_node=start_node,
        target_node=target_node,
        reachable=True,
        path=path,
        edge_count=len(path) - 1,
        visited_nodes=explored_order,
        explored_count=len(explored_order),
        duration_ms=round(duration_ms, 3),
    )
