"""
Prerequisite Closure and Dependency Planning for Learnify AI (Phase 2).
Computes complete transitive prerequisite closures, topological ordering (DAG sequencing),
known-topic exclusion, and estimated effort calculations.

Distinct from single-path search: guarantees all branching prerequisites are satisfied.
"""

from collections import deque
from typing import List, Dict, Set, Optional, Tuple, Any
from app.search.graph import LearningGraph, TopicNode


class PlannedTopicItem:
    def __init__(
        self,
        topic_id: str,
        name: str,
        unit: int,
        category: str,
        description: str,
        estimated_hours: int,
        reason: str,
        prerequisites: List[str],
        prerequisites_names: List[str],
        dependents: List[str],
        is_completed: bool = False,
        is_ready: bool = False,
    ):
        self.topic_id = topic_id
        self.name = name
        self.unit = unit
        self.category = category
        self.description = description
        self.estimated_hours = estimated_hours
        self.reason = reason
        self.prerequisites = prerequisites
        self.prerequisites_names = prerequisites_names
        self.dependents = dependents
        self.is_completed = is_completed
        self.is_ready = is_ready

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "name": self.name,
            "unit": self.unit,
            "category": self.category,
            "description": self.description,
            "estimated_hours": self.estimated_hours,
            "reason": self.reason,
            "prerequisites": self.prerequisites,
            "prerequisites_names": self.prerequisites_names,
            "dependents": self.dependents,
            "is_completed": self.is_completed,
            "is_ready": self.is_ready,
        }


class LearningPlan:
    def __init__(
        self,
        goal_topic_id: str,
        goal_name: str,
        is_valid: bool,
        required_topics_count: int,
        completed_topics_count: int,
        remaining_topics_count: int,
        total_estimated_hours: int,
        completed_topics: List[str],
        ordered_plan: List[PlannedTopicItem],
        all_required_ids: List[str],
        has_cycle: bool = False,
        cycle_details: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None,
    ):
        self.goal_topic_id = goal_topic_id
        self.goal_name = goal_name
        self.is_valid = is_valid
        self.required_topics_count = required_topics_count
        self.completed_topics_count = completed_topics_count
        self.remaining_topics_count = remaining_topics_count
        self.total_estimated_hours = total_estimated_hours
        self.completed_topics = completed_topics
        self.ordered_plan = ordered_plan
        self.all_required_ids = all_required_ids
        self.has_cycle = has_cycle
        self.cycle_details = cycle_details
        self.warnings = warnings or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal_topic_id": self.goal_topic_id,
            "goal_name": self.goal_name,
            "is_valid": self.is_valid,
            "required_topics_count": self.required_topics_count,
            "completed_topics_count": self.completed_topics_count,
            "remaining_topics_count": self.remaining_topics_count,
            "total_estimated_hours": self.total_estimated_hours,
            "completed_topics": self.completed_topics,
            "ordered_plan": [item.to_dict() for item in self.ordered_plan],
            "all_required_ids": self.all_required_ids,
            "has_cycle": self.has_cycle,
            "cycle_details": self.cycle_details,
            "warnings": self.warnings,
        }


def get_prerequisite_closure(graph: LearningGraph, goal_topic_id: str) -> Set[str]:
    """
    Compute transitive closure of all prerequisite topics for goal_topic_id
    by following incoming directed edges (predecessors) backward recursively.
    Includes the goal_topic_id itself.
    """
    closure: Set[str] = set()
    if not graph.has_node(goal_topic_id):
        return closure

    queue: deque[str] = deque([goal_topic_id])
    closure.add(goal_topic_id)

    while queue:
        current = queue.popleft()
        for prereq in graph.get_incoming(current):
            if prereq not in closure:
                closure.add(prereq)
                queue.append(prereq)

    return closure


def topological_sort(
    graph: LearningGraph,
    subset_ids: Set[str]
) -> Tuple[List[str], bool, Optional[List[str]]]:
    """
    Topological Sort of the induced subgraph defined by subset_ids using Kahn's algorithm.
    Ensures that for every directed edge u -> v (u is prerequisite for v),
    u appears strictly BEFORE v in the returned list.
    
    Returns: (ordered_ids, has_cycle, cycle_path)
    """
    # Compute in-degree within the subset
    # In-degree of v = number of u in subset_ids such that u is prerequisite for v
    in_degree: Dict[str, int] = {node_id: 0 for node_id in subset_ids}

    for u in subset_ids:
        for v in graph.get_outgoing(u):
            if v in subset_ids:
                in_degree[v] += 1

    # Queue of nodes with 0 in-degree (no remaining unfulfilled prerequisites)
    zero_in_degree = deque([node_id for node_id, deg in in_degree.items() if deg == 0])
    ordered: List[str] = []

    while zero_in_degree:
        u = zero_in_degree.popleft()
        ordered.append(u)

        for v in graph.get_outgoing(u):
            if v in subset_ids:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    zero_in_degree.append(v)

    if len(ordered) < len(subset_ids):
        # Cycle exists among remaining nodes!
        remaining = [nid for nid, deg in in_degree.items() if deg > 0]
        return ordered, True, remaining

    return ordered, False, None


def generate_learning_plan(
    graph: LearningGraph,
    goal_topic_id: str,
    known_topic_ids: Optional[List[str]] = None
) -> LearningPlan:
    """
    Produce a complete, topologically ordered study plan for goal_topic_id.
    Excludes explicitly mastered topics while ensuring all prerequisites of remaining topics
    are placed before them.
    """
    known_set = set(known_topic_ids or [])
    warnings: List[str] = []

    if not graph.has_node(goal_topic_id):
        return LearningPlan(
            goal_topic_id=goal_topic_id,
            goal_name="Unknown Goal Topic",
            is_valid=False,
            required_topics_count=0,
            completed_topics_count=0,
            remaining_topics_count=0,
            total_estimated_hours=0,
            completed_topics=[],
            ordered_plan=[],
            all_required_ids=[],
            warnings=[f"Topic '{goal_topic_id}' was not found in the knowledge graph."]
        )

    goal_node = graph.get_node(goal_topic_id)
    assert goal_node is not None
    goal_name = goal_node.name

    # Step 1: Transitive prerequisite closure
    all_required = get_prerequisite_closure(graph, goal_topic_id)

    # Check for cycles in full closure
    full_ordered, has_cycle, cycle_info = topological_sort(graph, all_required)
    if has_cycle:
        return LearningPlan(
            goal_topic_id=goal_topic_id,
            goal_name=goal_name,
            is_valid=False,
            required_topics_count=len(all_required),
            completed_topics_count=0,
            remaining_topics_count=len(all_required),
            total_estimated_hours=0,
            completed_topics=[],
            ordered_plan=[],
            all_required_ids=list(all_required),
            has_cycle=True,
            cycle_details=cycle_info,
            warnings=["Circular dependency detected in prerequisite chain! Invalid study path."]
        )

    # Step 2: Separate completed topics from remaining topics
    completed = sorted(list(all_required.intersection(known_set)))
    remaining_ids = all_required - set(completed)

    # Step 3: Topologically sort remaining topics
    ordered_remaining, rem_cycle, _ = topological_sort(graph, remaining_ids)

    # Step 4: Build rich planned topic items
    planned_items: List[PlannedTopicItem] = []
    satisfied_so_far = set(completed)
    total_hours = 0

    for tid in ordered_remaining:
        node = graph.get_node(tid)
        if not node:
            continue

        # Direct prerequisites
        direct_prereqs = [p for p in graph.get_incoming(tid) if p in all_required]
        prereq_names = [graph.get_node(p).name for p in direct_prereqs if graph.get_node(p)]

        # Determine inclusion reason
        if tid == goal_topic_id:
            reason = "Selected Target Learning Goal"
        elif goal_topic_id in graph.get_outgoing(tid):
            reason = f"Direct prerequisite for {goal_name}"
        else:
            # Find which dependent topic in the plan needs this
            dependents_in_plan = [d for d in graph.get_outgoing(tid) if d in all_required]
            dep_names = [graph.get_node(d).name for d in dependents_in_plan[:2] if graph.get_node(d)]
            if dep_names:
                reason = f"Prerequisite for {', '.join(dep_names)}"
            else:
                reason = f"Foundational prerequisite for {goal_name}"

        # Ready status: are all its prerequisites already in satisfied_so_far?
        is_ready = all(p in satisfied_so_far for p in direct_prereqs)

        planned_items.append(PlannedTopicItem(
            topic_id=tid,
            name=node.name,
            unit=node.unit,
            category=node.category,
            description=node.description,
            estimated_hours=node.estimated_hours,
            reason=reason,
            prerequisites=direct_prereqs,
            prerequisites_names=prereq_names,
            dependents=[d for d in graph.get_outgoing(tid) if d in all_required],
            is_completed=False,
            is_ready=is_ready,
        ))

        total_hours += node.estimated_hours
        satisfied_so_far.add(tid)

    if not planned_items and goal_topic_id in completed:
        warnings.append(f"You have already mastered all prerequisites and the target goal '{goal_name}'!")

    return LearningPlan(
        goal_topic_id=goal_topic_id,
        goal_name=goal_name,
        is_valid=True,
        required_topics_count=len(all_required),
        completed_topics_count=len(completed),
        remaining_topics_count=len(planned_items),
        total_estimated_hours=total_hours,
        completed_topics=completed,
        ordered_plan=planned_items,
        all_required_ids=list(all_required),
        has_cycle=False,
        cycle_details=None,
        warnings=warnings,
    )
