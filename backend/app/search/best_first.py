"""
Greedy Best-First Search for Learnify AI (Phase 2).
Uses a priority queue (heapq) and a lightweight, deterministic heuristic
based on topic name/keyword overlap, category proximity, and syllabus unit proximity.

Note: Greedy Best-First Search expands nodes with the lowest estimated heuristic cost h(n)
to the goal. It is an informed search strategy, but is NOT guaranteed to find the optimal or
shortest path by edge count (unlike BFS).
"""

import time
import heapq
import re
from typing import List, Dict, Optional, Tuple, Set, Any
from app.search.graph import LearningGraph, TopicNode


class BestFirstResult:
    def __init__(
        self,
        start_node: str,
        target_node: str,
        reachable: bool,
        path: List[str],
        edge_count: int,
        visited_nodes: List[str],
        explored_count: int,
        calculated_heuristics: Dict[str, float],
        duration_ms: float,
    ):
        self.algorithm = "greedy_best_first"
        self.start_node = start_node
        self.target_node = target_node
        self.reachable = reachable
        self.path = path
        self.edge_count = edge_count
        self.visited_nodes = visited_nodes
        self.explored_count = explored_count
        self.calculated_heuristics = calculated_heuristics
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
            "calculated_heuristics": self.calculated_heuristics,
            "duration_ms": self.duration_ms,
        }


def compute_heuristic(node: TopicNode, target_node: TopicNode) -> float:
    """
    Deterministic, lightweight heuristic function h(n) estimating distance to goal.
    Combines:
    1. Lexical dissimilarity (Jaccard dissimilarity on normalized tokens)
    2. Category proximity
    3. Unit difference
    h(goal) is strictly 0.0.
    """
    if node.id == target_node.id:
        return 0.0

    # 1. Lexical overlap on name & description
    text_n = f"{node.name} {node.description}".lower()
    text_t = f"{target_node.name} {target_node.description}".lower()

    tokens_n = set(re.findall(r'\b[a-zA-Z0-9]+\b', text_n))
    tokens_t = set(re.findall(r'\b[a-zA-Z0-9]+\b', text_t))

    intersection = tokens_n.intersection(tokens_t)
    union = tokens_n.union(tokens_t)
    jaccard = (len(intersection) / len(union)) if union else 0.0
    lexical_dissimilarity = 1.0 - jaccard

    # 2. Category matching penalty
    if node.category == target_node.category:
        cat_penalty = 0.0
    elif any(k in node.category and k in target_node.category for k in ["AI", "Search", "Math", "Machine"]):
        cat_penalty = 1.0
    else:
        cat_penalty = 2.0

    # 3. Unit progression difference
    unit_diff = abs(node.unit - target_node.unit) * 0.5

    # Total heuristic value h(n) >= 0.0
    h = round(lexical_dissimilarity * 4.0 + cat_penalty * 1.5 + unit_diff * 0.5, 3)
    return max(0.1, h)


def greedy_best_first_search(
    graph: LearningGraph,
    start_node: str,
    target_node: str
) -> BestFirstResult:
    """
    Execute Greedy Best-First Search on a directed LearningGraph.
    Frontier is maintained as a min-heap sorted by h(n).
    """
    t0 = time.perf_counter()

    if not graph.has_node(start_node) or not graph.has_node(target_node):
        duration_ms = (time.perf_counter() - t0) * 1000.0
        return BestFirstResult(
            start_node=start_node,
            target_node=target_node,
            reachable=False,
            path=[],
            edge_count=0,
            visited_nodes=[],
            explored_count=0,
            calculated_heuristics={},
            duration_ms=round(duration_ms, 3),
        )

    target_obj = graph.get_node(target_node)
    start_obj = graph.get_node(start_node)
    assert target_obj is not None and start_obj is not None

    # Trivial case
    if start_node == target_node:
        duration_ms = (time.perf_counter() - t0) * 1000.0
        return BestFirstResult(
            start_node=start_node,
            target_node=target_node,
            reachable=True,
            path=[start_node],
            edge_count=0,
            visited_nodes=[start_node],
            explored_count=1,
            calculated_heuristics={start_node: 0.0},
            duration_ms=round(duration_ms, 3),
        )

    # Priority queue storing (h_val, tie_breaker_counter, node_id)
    pq: List[Tuple[float, int, str]] = []
    counter = 0

    initial_h = compute_heuristic(start_obj, target_obj)
    heapq.heappush(pq, (initial_h, counter, start_node))

    visited: Set[str] = set()
    parent: Dict[str, Optional[str]] = {start_node: None}
    explored_order: List[str] = []
    heuristics_map: Dict[str, float] = {start_node: initial_h}

    target_found = False

    while pq:
        h_val, _, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        explored_order.append(current)

        if current == target_node:
            target_found = True
            break

        for neighbor in graph.get_outgoing(current):
            if neighbor not in visited:
                neighbor_obj = graph.get_node(neighbor)
                if neighbor_obj is None:
                    continue
                neighbor_h = compute_heuristic(neighbor_obj, target_obj)
                heuristics_map[neighbor] = neighbor_h

                if neighbor not in parent:
                    parent[neighbor] = current

                counter += 1
                heapq.heappush(pq, (neighbor_h, counter, neighbor))

    duration_ms = (time.perf_counter() - t0) * 1000.0

    if not target_found:
        return BestFirstResult(
            start_node=start_node,
            target_node=target_node,
            reachable=False,
            path=[],
            edge_count=0,
            visited_nodes=explored_order,
            explored_count=len(explored_order),
            calculated_heuristics=heuristics_map,
            duration_ms=round(duration_ms, 3),
        )

    # Reconstruct path from target back to start
    path: List[str] = []
    curr: Optional[str] = target_node
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()

    return BestFirstResult(
        start_node=start_node,
        target_node=target_node,
        reachable=True,
        path=path,
        edge_count=len(path) - 1,
        visited_nodes=explored_order,
        explored_count=len(explored_order),
        calculated_heuristics=heuristics_map,
        duration_ms=round(duration_ms, 3),
    )
