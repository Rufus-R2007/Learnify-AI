"""
Bidirectional Breadth-First Search for Learnify AI (Phase 2).
Finds the shortest directed path between a student's current topic and target topic
by searching simultaneously forward from the start and backward (along reverse edges) from the target.
Strictly respects directed edges:
  Forward: u -> v via graph.get_outgoing(u)
  Backward: u <- v via graph.get_incoming(v)
"""

import time
from collections import deque
from typing import List, Dict, Optional, Set, Any
from app.search.graph import LearningGraph


class BidirectionalResult:
    def __init__(
        self,
        start_node: str,
        target_node: str,
        reachable: bool,
        path: List[str],
        edge_count: int,
        meeting_node: Optional[str],
        forward_visited: List[str],
        reverse_visited: List[str],
        visited_nodes: List[str],
        explored_count: int,
        duration_ms: float,
    ):
        self.algorithm = "bidirectional"
        self.start_node = start_node
        self.target_node = target_node
        self.reachable = reachable
        self.path = path
        self.edge_count = edge_count
        self.meeting_node = meeting_node
        self.forward_visited = forward_visited
        self.reverse_visited = reverse_visited
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
            "meeting_node": self.meeting_node,
            "forward_visited": self.forward_visited,
            "reverse_visited": self.reverse_visited,
            "visited_nodes": self.visited_nodes,
            "explored_count": self.explored_count,
            "duration_ms": self.duration_ms,
        }


def bidirectional_search(
    graph: LearningGraph,
    start_node: str,
    target_node: str
) -> BidirectionalResult:
    """
    Execute Bidirectional Breadth-First Search on a directed LearningGraph.
    
    Traverses forward edges from start_node and reverse edges from target_node,
    detecting when the frontiers intersect at a meeting point.
    """
    t0 = time.perf_counter()

    if not graph.has_node(start_node) or not graph.has_node(target_node):
        duration_ms = (time.perf_counter() - t0) * 1000.0
        return BidirectionalResult(
            start_node=start_node,
            target_node=target_node,
            reachable=False,
            path=[],
            edge_count=0,
            meeting_node=None,
            forward_visited=[],
            reverse_visited=[],
            visited_nodes=[],
            explored_count=0,
            duration_ms=round(duration_ms, 3),
        )

    # Trivial case: start is target
    if start_node == target_node:
        duration_ms = (time.perf_counter() - t0) * 1000.0
        return BidirectionalResult(
            start_node=start_node,
            target_node=target_node,
            reachable=True,
            path=[start_node],
            edge_count=0,
            meeting_node=start_node,
            forward_visited=[start_node],
            reverse_visited=[target_node],
            visited_nodes=[start_node],
            explored_count=1,
            duration_ms=round(duration_ms, 3),
        )

    forward_queue: deque[str] = deque([start_node])
    reverse_queue: deque[str] = deque([target_node])

    forward_visited_set: Set[str] = {start_node}
    reverse_visited_set: Set[str] = {target_node}

    forward_visited_order: List[str] = []
    reverse_visited_order: List[str] = []

    forward_parent: Dict[str, Optional[str]] = {start_node: None}
    reverse_parent: Dict[str, Optional[str]] = {target_node: None}

    meeting_node: Optional[str] = None

    while forward_queue and reverse_queue:
        # Balanced expansion: expand the frontier with fewer elements
        if len(forward_queue) <= len(reverse_queue):
            # Forward step: follow outgoing directed edges (prerequisite -> dependent)
            current = forward_queue.popleft()
            forward_visited_order.append(current)

            for neighbor in graph.get_outgoing(current):
                if neighbor in reverse_visited_set:
                    # Frontiers meet!
                    meeting_node = neighbor
                    forward_parent[neighbor] = current
                    forward_visited_set.add(neighbor)
                    forward_visited_order.append(neighbor)
                    break

                if neighbor not in forward_visited_set:
                    forward_visited_set.add(neighbor)
                    forward_parent[neighbor] = current
                    forward_queue.append(neighbor)

            if meeting_node:
                break
        else:
            # Backward step: follow incoming directed edges in reverse (dependent -> prerequisite)
            current = reverse_queue.popleft()
            reverse_visited_order.append(current)

            for predecessor in graph.get_incoming(current):
                if predecessor in forward_visited_set:
                    # Frontiers meet!
                    meeting_node = predecessor
                    reverse_parent[predecessor] = current
                    reverse_visited_set.add(predecessor)
                    reverse_visited_order.append(predecessor)
                    break

                if predecessor not in reverse_visited_set:
                    reverse_visited_set.add(predecessor)
                    reverse_parent[predecessor] = current
                    reverse_queue.append(predecessor)

            if meeting_node:
                break

    duration_ms = (time.perf_counter() - t0) * 1000.0

    # Combine unique visited nodes in exploration order
    combined_visited: List[str] = []
    seen = set()
    for n in forward_visited_order + reverse_visited_order:
        if n not in seen:
            seen.add(n)
            combined_visited.append(n)

    if not meeting_node:
        return BidirectionalResult(
            start_node=start_node,
            target_node=target_node,
            reachable=False,
            path=[],
            edge_count=0,
            meeting_node=None,
            forward_visited=forward_visited_order,
            reverse_visited=reverse_visited_order,
            visited_nodes=combined_visited,
            explored_count=len(combined_visited),
            duration_ms=round(duration_ms, 3),
        )

    # Reconstruct path from start_node to meeting_node
    forward_path: List[str] = []
    curr: Optional[str] = meeting_node
    while curr is not None:
        forward_path.append(curr)
        curr = forward_parent.get(curr)
    forward_path.reverse()

    # Reconstruct path from meeting_node to target_node
    backward_path: List[str] = []
    curr = reverse_parent.get(meeting_node)
    while curr is not None:
        backward_path.append(curr)
        curr = reverse_parent.get(curr)

    full_path = forward_path + backward_path

    return BidirectionalResult(
        start_node=start_node,
        target_node=target_node,
        reachable=True,
        path=full_path,
        edge_count=len(full_path) - 1,
        meeting_node=meeting_node,
        forward_visited=forward_visited_order,
        reverse_visited=reverse_visited_order,
        visited_nodes=combined_visited,
        explored_count=len(combined_visited),
        duration_ms=round(duration_ms, 3),
    )
