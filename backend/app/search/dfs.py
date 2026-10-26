"""
Depth-First Search (DFS) for Learnify AI (Phase 2).
Used to traverse prerequisite chains deeply, reconstruct reachable paths,
and detect circular dependencies using recursion-stack / visited-state tracking.
"""

import time
from typing import List, Dict, Optional, Tuple, Set, Any
from app.search.graph import LearningGraph


class DFSResult:
    def __init__(
        self,
        start_node: str,
        target_node: Optional[str],
        reachable: bool,
        path: List[str],
        visited_nodes: List[str],
        explored_count: int,
        has_cycle: bool,
        cycle: Optional[List[str]],
        duration_ms: float,
    ):
        self.algorithm = "dfs"
        self.start_node = start_node
        self.target_node = target_node
        self.reachable = reachable
        self.path = path
        self.visited_nodes = visited_nodes
        self.explored_count = explored_count
        self.has_cycle = has_cycle
        self.cycle = cycle
        self.duration_ms = duration_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "start_node": self.start_node,
            "target_node": self.target_node,
            "reachable": self.reachable,
            "path": self.path,
            "visited_nodes": self.visited_nodes,
            "explored_count": self.explored_count,
            "has_cycle": self.has_cycle,
            "cycle": self.cycle,
            "duration_ms": self.duration_ms,
        }


def depth_first_search(
    graph: LearningGraph,
    start_node: str,
    target_node: Optional[str] = None
) -> DFSResult:
    """
    Execute Depth-First Search from start_node.
    
    If target_node is provided, searches for a deep path from start to target.
    Simultaneously tracks the exploration stack to detect any cycles along the traversal.
    """
    t0 = time.perf_counter()

    if not graph.has_node(start_node) or (target_node and not graph.has_node(target_node)):
        duration_ms = (time.perf_counter() - t0) * 1000.0
        return DFSResult(
            start_node=start_node,
            target_node=target_node,
            reachable=False,
            path=[],
            visited_nodes=[],
            explored_count=0,
            has_cycle=False,
            cycle=None,
            duration_ms=round(duration_ms, 3),
        )

    visited_nodes: List[str] = []
    visited_set: Set[str] = set()
    on_stack: Set[str] = set()
    stack_path: List[str] = []
    found_target_path: Optional[List[str]] = None
    detected_cycle: Optional[List[str]] = None

    def dfs(current: str) -> bool:
        nonlocal detected_cycle, found_target_path

        visited_set.add(current)
        on_stack.add(current)
        visited_nodes.append(current)
        stack_path.append(current)

        if target_node and current == target_node and found_target_path is None:
            found_target_path = list(stack_path)

        for neighbor in graph.get_outgoing(current):
            if neighbor in on_stack:
                # Cycle detected!
                if detected_cycle is None:
                    idx = stack_path.index(neighbor)
                    detected_cycle = stack_path[idx:] + [neighbor]
            elif neighbor not in visited_set:
                dfs(neighbor)

        on_stack.remove(current)
        stack_path.pop()
        return found_target_path is not None

    dfs(start_node)
    duration_ms = (time.perf_counter() - t0) * 1000.0

    reachable = (target_node is not None and found_target_path is not None) or (target_node is None)
    path = found_target_path or []

    return DFSResult(
        start_node=start_node,
        target_node=target_node,
        reachable=reachable,
        path=path,
        visited_nodes=visited_nodes,
        explored_count=len(visited_nodes),
        has_cycle=detected_cycle is not None,
        cycle=detected_cycle,
        duration_ms=round(duration_ms, 3),
    )
