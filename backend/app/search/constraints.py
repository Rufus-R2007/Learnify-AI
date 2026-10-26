"""
Constraint Satisfaction Problem (CSP) definitions for Learnify AI (Phase 2).
Defines Variables, Domains, Constraints, and Preference models for the Study Scheduler.
"""

from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class TimeSlot:
    """A discrete assignable study slot within the planning horizon."""
    day: str             # e.g., "Monday"
    day_index: int       # 0-indexed chronological day number in schedule horizon
    slot_index: int      # 0-indexed slot on that day
    duration_hours: int  # Duration of the slot (typically 1 or 2 hours)

    def to_key(self) -> Tuple[int, int]:
        return (self.day_index, self.slot_index)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "day_index": self.day_index,
            "slot_index": self.slot_index,
            "duration_hours": self.duration_hours,
        }


@dataclass
class SessionVariable:
    """
    CSP Variable representing a single study session for a topic.
    A topic requiring 4 hours with preferred 2-hour sessions is split into 2 variables.
    """
    var_id: str
    topic_id: str
    topic_name: str
    session_index: int
    duration_hours: int
    prerequisite_topic_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "var_id": self.var_id,
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "session_index": self.session_index,
            "duration_hours": self.duration_hours,
            "prerequisite_topic_ids": list(self.prerequisite_topic_ids),
        }


@dataclass
class StudyPreferences:
    """Student availability and scheduling preferences."""
    available_days: List[str]            # e.g. ["Monday", "Wednesday", "Friday", "Saturday"]
    max_daily_hours: int = 2             # Maximum hours student can study in a single day
    preferred_session_hours: int = 1     # 1 or 2 hour blocks
    busy_slots: List[Dict[str, Any]] = field(default_factory=list) # e.g. [{"day": "Monday", "slot_index": 0}]
    planning_weeks: int = 2              # Horizon in weeks (default 2 weeks = 14 days)

    def get_effective_max_hours(self) -> int:
        return max(1, min(self.max_daily_hours, 8))


def is_assignment_consistent(
    var: SessionVariable,
    slot: TimeSlot,
    current_assignment: Dict[str, TimeSlot],
    variables_map: Dict[str, SessionVariable],
    prefs: StudyPreferences,
) -> Tuple[bool, Optional[str]]:
    """
    Validate all CSP constraints for assigning 'slot' to 'var':
    1. No overlapping sessions: slot cannot already be occupied by another variable.
    2. Daily study time constraint: sum of hours assigned on that day + slot.duration <= max_daily_hours.
    3. Prerequisite constraint: all sessions of any prerequisite topic must be scheduled
       strictly before this slot: (prereq.day_index < slot.day_index) or
       (prereq.day_index == slot.day_index and prereq.slot_index < slot.slot_index).
    4. Intra-topic session order constraint: session_index i must be scheduled after session_index i-1.
    """
    # 1. Non-overlapping check
    for other_var_id, other_slot in current_assignment.items():
        if (other_slot.day_index, other_slot.slot_index) == (slot.day_index, slot.slot_index):
            return False, f"Slot {slot.day} (slot {slot.slot_index}) is already occupied by {other_var_id}."

    # 2. Daily limit check
    day_assigned_hours = sum(
        variables_map[other_id].duration_hours
        for other_id, other_slot in current_assignment.items()
        if other_slot.day_index == slot.day_index
    )
    if day_assigned_hours + var.duration_hours > prefs.get_effective_max_hours():
        return False, f"Daily limit exceeded for {slot.day}: {day_assigned_hours + var.duration_hours}h > {prefs.get_effective_max_hours()}h."

    # 3. Intra-topic session ordering check (session 1 must come before session 2 of the same topic)
    if var.session_index > 0:
        prev_session_id = f"{var.topic_id}:session_{var.session_index - 1}"
        if prev_session_id in current_assignment:
            prev_slot = current_assignment[prev_session_id]
            if (slot.day_index < prev_slot.day_index) or (
                slot.day_index == prev_slot.day_index and slot.slot_index <= prev_slot.slot_index
            ):
                return False, f"Session {var.session_index} of {var.topic_name} must occur after session {var.session_index - 1}."

    # 4. Prerequisite precedence check
    for prereq_id in var.prerequisite_topic_ids:
        # Check all sessions of the prerequisite that have been assigned so far
        for other_var_id, other_slot in current_assignment.items():
            other_var = variables_map[other_var_id]
            if other_var.topic_id == prereq_id:
                # Prerequisite session must be strictly before current session
                if (slot.day_index < other_slot.day_index) or (
                    slot.day_index == other_slot.day_index and slot.slot_index <= other_slot.slot_index
                ):
                    return False, f"Prerequisite {other_var.topic_name} must be scheduled before {var.topic_name}."

    return True, None
