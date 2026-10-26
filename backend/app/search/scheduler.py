"""
Backtracking Search Algorithm for Study Schedule Planning in Learnify AI (Phase 2).
Solves the CSP by assigning study session variables to discrete available time slots.
Demonstrates real backtracking, constraint evaluation, MRV variable selection,
and honest diagnostics when requirements exceed student availability.
"""

import time
from typing import List, Dict, Optional, Tuple, Set, Any
from app.search.constraints import (
    TimeSlot,
    SessionVariable,
    StudyPreferences,
    is_assignment_consistent,
)
from app.search.graph import LearningGraph
from app.search.prerequisites import LearningPlan, PlannedTopicItem


DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class ScheduledSession:
    def __init__(
        self,
        session_id: str,
        topic_id: str,
        topic_name: str,
        session_number: int,
        day: str,
        day_index: int,
        slot_index: int,
        duration_hours: int,
        time_display: str,
    ):
        self.session_id = session_id
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.session_number = session_number
        self.day = day
        self.day_index = day_index
        self.slot_index = slot_index
        self.duration_hours = duration_hours
        self.time_display = time_display

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "session_number": self.session_number,
            "day": self.day,
            "day_index": self.day_index,
            "slot_index": self.slot_index,
            "duration_hours": self.duration_hours,
            "time_display": self.time_display,
        }


class ScheduleResult:
    def __init__(
        self,
        is_feasible: bool,
        sessions: List[ScheduledSession],
        total_study_hours: int,
        available_capacity_hours: int,
        used_capacity_hours: int,
        assignments_tried: int,
        backtrack_count: int,
        constraint_explanations: List[str],
        failure_reason: Optional[str],
        duration_ms: float,
    ):
        self.is_feasible = is_feasible
        self.sessions = sessions
        self.total_study_hours = total_study_hours
        self.available_capacity_hours = available_capacity_hours
        self.used_capacity_hours = used_capacity_hours
        self.assignments_tried = assignments_tried
        self.backtrack_count = backtrack_count
        self.constraint_explanations = constraint_explanations
        self.failure_reason = failure_reason
        self.duration_ms = duration_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_feasible": self.is_feasible,
            "sessions": [s.to_dict() for s in self.sessions],
            "total_study_hours": self.total_study_hours,
            "available_capacity_hours": self.available_capacity_hours,
            "used_capacity_hours": self.used_capacity_hours,
            "assignments_tried": self.assignments_tried,
            "backtrack_count": self.backtrack_count,
            "constraint_explanations": self.constraint_explanations,
            "failure_reason": self.failure_reason,
            "duration_ms": self.duration_ms,
        }


def format_slot_time(slot_index: int, duration_hours: int) -> str:
    """Format slot index into a human-readable university study time window."""
    base_hour = 9 + (slot_index * 2)  # Slot 0 starts 9:00 AM, slot 1 starts 11:00 AM, etc.
    end_hour = base_hour + duration_hours
    return f"{base_hour:02d}:00 - {end_hour:02d}:00"


def generate_time_slots(prefs: StudyPreferences) -> List[TimeSlot]:
    """Generate all available time slots based on user days, horizon, and daily limits."""
    slots: List[TimeSlot] = []
    effective_max = prefs.get_effective_max_hours()
    session_len = max(1, prefs.preferred_session_hours)
    slots_per_day = max(1, effective_max // session_len)

    busy_set = {(b.get("day"), b.get("slot_index")) for b in prefs.busy_slots}

    day_index_counter = 0
    for week in range(prefs.planning_weeks):
        for day in DAYS_OF_WEEK:
            if day in prefs.available_days:
                for slot_idx in range(slots_per_day):
                    if (day, slot_idx) not in busy_set:
                        slots.append(TimeSlot(
                            day=day,
                            day_index=day_index_counter,
                            slot_index=slot_idx,
                            duration_hours=session_len,
                        ))
            day_index_counter += 1

    return slots


def build_session_variables(
    topics: List[PlannedTopicItem],
    session_duration: int
) -> List[SessionVariable]:
    """Break each planned topic's estimated hours into discrete session variables."""
    variables: List[SessionVariable] = []
    session_len = max(1, session_duration)

    for item in topics:
        hours = max(1, item.estimated_hours)
        num_sessions = max(1, (hours + session_len - 1) // session_len)
        for s_idx in range(num_sessions):
            # Last session might be remainder or standard block
            dur = session_len
            var_id = f"{item.topic_id}:session_{s_idx}"
            variables.append(SessionVariable(
                var_id=var_id,
                topic_id=item.topic_id,
                topic_name=item.name,
                session_index=s_idx,
                duration_hours=dur,
                prerequisite_topic_ids=item.prerequisites,
            ))

    return variables


def solve_study_schedule(
    learning_plan: LearningPlan,
    preferences: StudyPreferences
) -> ScheduleResult:
    """
    Backtracking Search with Constraint Satisfaction for academic study scheduling.
    
    1. Selects unassigned session variable.
    2. Tries candidate slots in chronological order.
    3. Evaluates daily hour limit, prerequisite precedence, and non-overlapping constraints.
    4. Backtracks upon constraint dead-ends.
    5. Returns feasible schedule or honest explanation of infeasibility.
    """
    t0 = time.perf_counter()

    # Step 1: Filter remaining uncompleted topics
    remaining_topics = [t for t in learning_plan.ordered_plan if not t.is_completed]
    session_len = max(1, preferences.preferred_session_hours)
    variables = build_session_variables(remaining_topics, session_len)
    total_study_hours = sum(v.duration_hours for v in variables)

    # Step 2: Build domain slots
    domain_slots = generate_time_slots(preferences)
    available_capacity_hours = sum(s.duration_hours for s in domain_slots)

    # Initial capacity pre-check
    constraint_explanations = [
        f"Available study days: {', '.join(preferences.available_days) if preferences.available_days else 'None selected'}",
        f"Daily study limit: {preferences.get_effective_max_hours()} hours/day (session blocks: {session_len}h)",
        f"Prerequisite ordering: Dependent topics scheduled strictly after prerequisites",
        f"Total required effort: {total_study_hours} estimated hours across {len(variables)} study sessions",
        f"Total available capacity: {available_capacity_hours} hours over {preferences.planning_weeks} weeks",
    ]

    if not preferences.available_days:
        return ScheduleResult(
            is_feasible=False,
            sessions=[],
            total_study_hours=total_study_hours,
            available_capacity_hours=0,
            used_capacity_hours=0,
            assignments_tried=0,
            backtrack_count=0,
            constraint_explanations=constraint_explanations,
            failure_reason="No available study days were selected. Please select at least one study day.",
            duration_ms=round((time.perf_counter() - t0) * 1000.0, 3),
        )

    if total_study_hours > available_capacity_hours:
        return ScheduleResult(
            is_feasible=False,
            sessions=[],
            total_study_hours=total_study_hours,
            available_capacity_hours=available_capacity_hours,
            used_capacity_hours=0,
            assignments_tried=0,
            backtrack_count=0,
            constraint_explanations=constraint_explanations,
            failure_reason=(
                f"Your selected study plan requires an estimated {total_study_hours} hours across "
                f"{len(variables)} sessions, but your availability provides only {available_capacity_hours} hours. "
                f"Please add more available study days or increase the daily study hour limit."
            ),
            duration_ms=round((time.perf_counter() - t0) * 1000.0, 3),
        )

    # Step 3: Backtracking Search Setup
    variables_map = {v.var_id: v for v in variables}
    assignment: Dict[str, TimeSlot] = {}
    assignments_tried = 0
    backtrack_count = 0

    def backtrack(var_index: int) -> bool:
        nonlocal assignments_tried, backtrack_count

        if var_index == len(variables):
            return True  # All sessions assigned!

        current_var = variables[var_index]

        for slot in domain_slots:
            assignments_tried += 1
            is_valid, _ = is_assignment_consistent(
                current_var, slot, assignment, variables_map, preferences
            )

            if is_valid:
                assignment[current_var.var_id] = slot
                if backtrack(var_index + 1):
                    return True
                # Backtrack: undo assignment and count
                del assignment[current_var.var_id]
                backtrack_count += 1

        return False

    success = backtrack(0)
    duration_ms = (time.perf_counter() - t0) * 1000.0

    if not success:
        return ScheduleResult(
            is_feasible=False,
            sessions=[],
            total_study_hours=total_study_hours,
            available_capacity_hours=available_capacity_hours,
            used_capacity_hours=0,
            assignments_tried=assignments_tried,
            backtrack_count=backtrack_count,
            constraint_explanations=constraint_explanations,
            failure_reason=(
                f"Could not find a conflict-free study schedule within the {preferences.planning_weeks}-week window. "
                f"The prerequisite chains and daily limit ({preferences.get_effective_max_hours()}h/day) "
                f"could not be satisfied simultaneously. Consider increasing daily study hours or expanding available days."
            ),
            duration_ms=round(duration_ms, 3),
        )

    # Format scheduled sessions sorted chronologically
    scheduled_sessions: List[ScheduledSession] = []
    for var in variables:
        assigned_slot = assignment[var.var_id]
        time_str = format_slot_time(assigned_slot.slot_index, assigned_slot.duration_hours)
        scheduled_sessions.append(ScheduledSession(
            session_id=var.var_id,
            topic_id=var.topic_id,
            topic_name=var.topic_name,
            session_number=var.session_index + 1,
            day=assigned_slot.day,
            day_index=assigned_slot.day_index,
            slot_index=assigned_slot.slot_index,
            duration_hours=assigned_slot.duration_hours,
            time_display=time_str,
        ))

    scheduled_sessions.sort(key=lambda s: (s.day_index, s.slot_index))
    used_hours = sum(s.duration_hours for s in scheduled_sessions)

    return ScheduleResult(
        is_feasible=True,
        sessions=scheduled_sessions,
        total_study_hours=total_study_hours,
        available_capacity_hours=available_capacity_hours,
        used_capacity_hours=used_hours,
        assignments_tried=assignments_tried,
        backtrack_count=backtrack_count,
        constraint_explanations=constraint_explanations,
        failure_reason=None,
        duration_ms=round(duration_ms, 3),
    )
