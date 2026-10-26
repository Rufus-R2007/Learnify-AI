"""
Knowledge Representation and Fact Storage for Learnify AI (Unit III - Concept 1).
Provides structured educational fact models with:
- Fact identifier and predicate type
- Structured arguments and values
- Provenance and source attribution
- Strict verification status: VERIFIED vs HYPOTHETICAL vs CONTRADICTORY
- Conflict and contradiction detection
- Conversion to Horn clauses for resolution
- Scenario isolation protecting verified facts from simulation mutations
"""

from typing import List, Dict, Any, Optional, Set
from enum import Enum
from datetime import datetime, timezone
from app.reasoning.predicates import Predicate, HornClause, Constant, Variable


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"                  # Authoritative institutional or course fact
    HYPOTHETICAL = "HYPOTHETICAL"          # User-supplied simulation input from WhatIf Lab
    UNVERIFIED = "UNVERIFIED"              # Self-reported or provisional statement
    CONTRADICTORY = "CONTRADICTORY"        # Direct factual conflict detected


class Fact:
    """
    A structured academic fact with full provenance and verification metadata.
    e.g. attendance_percent(student_01, 78) [VERIFIED, src-demo]
         approved_exemption(student_01, True) [HYPOTHETICAL, src-whatif-simulator]
    """

    def __init__(
        self,
        id: str,
        predicate: str,
        entity_id: str,
        value: Any,
        arguments: Optional[List[Any]] = None,
        source_id: str = "src-demo",
        verification_status: VerificationStatus = VerificationStatus.VERIFIED,
        policy_id: Optional[str] = None,
        context: Optional[str] = None,
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.predicate = predicate
        self.entity_id = entity_id
        self.value = value
        self.arguments = list(arguments) if arguments is not None else [entity_id]
        self.source_id = source_id
        self.verification_status = (
            verification_status if isinstance(verification_status, VerificationStatus)
            else VerificationStatus(verification_status)
        )
        self.policy_id = policy_id
        self.context = context
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()

    @property
    def is_hypothetical(self) -> bool:
        return self.verification_status == VerificationStatus.HYPOTHETICAL

    def to_predicate(self) -> Predicate:
        """Convert this fact into a First-Order Predicate."""
        terms = [Constant(str(a)) for a in self.arguments]
        if self.value is not None and str(self.value) not in [str(a) for a in self.arguments]:
            terms.append(Constant(self.value))
        return Predicate(self.predicate, terms)

    def to_horn_clause(self) -> HornClause:
        """Convert into a definite Horn fact (Horn clause with empty body)."""
        return HornClause(self.to_predicate(), [])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "predicate": self.predicate,
            "entity_id": self.entity_id,
            "value": self.value,
            "arguments": self.arguments,
            "source_id": self.source_id,
            "verification_status": self.verification_status.value,
            "policy_id": self.policy_id,
            "context": self.context,
            "created_at": self.created_at,
        }

    def __repr__(self) -> str:
        args_str = ", ".join(str(a) for a in self.arguments)
        val_str = f" = {self.value}" if self.value is not None else ""
        return f"{self.predicate}({args_str}){val_str} [{self.verification_status.value}]"


class FactConflict:
    """Represents a direct conflict or contradiction detected between two facts."""

    def __init__(self, predicate: str, entity_id: str, fact1: Fact, fact2: Fact, description: str):
        self.predicate = predicate
        self.entity_id = entity_id
        self.fact1 = fact1
        self.fact2 = fact2
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "predicate": self.predicate,
            "entity_id": self.entity_id,
            "fact_a": self.fact1.to_dict(),
            "fact_b": self.fact2.to_dict(),
            "conflict_description": self.description,
        }


class FactBase:
    """
    Working memory collection of facts with conflict checking and scenario isolation.
    """

    def __init__(self, facts: Optional[List[Fact]] = None):
        self._facts: List[Fact] = []
        if facts:
            for f in facts:
                self.add_fact(f)

    @property
    def facts(self) -> List[Fact]:
        return list(self._facts)

    def add_fact(self, fact: Fact) -> None:
        """Add a fact to memory, preventing identical duplicates."""
        for existing in self._facts:
            if (
                existing.predicate == fact.predicate
                and existing.entity_id == fact.entity_id
                and existing.arguments == fact.arguments
                and existing.value == fact.value
                and existing.verification_status == fact.verification_status
            ):
                return  # Skip duplicate
        self._facts.append(fact)

    def find_facts(self, predicate: Optional[str] = None, entity_id: Optional[str] = None) -> List[Fact]:
        """Query stored facts matching optional predicate name and entity id."""
        res = self._facts
        if predicate is not None:
            res = [f for f in res if f.predicate == predicate]
        if entity_id is not None:
            res = [f for f in res if f.entity_id == entity_id]
        return res

    def get_fact_value(self, predicate: str, entity_id: str) -> Optional[Any]:
        """Retrieve the value of a single fact, or None if missing."""
        matches = self.find_facts(predicate=predicate, entity_id=entity_id)
        if matches:
            return matches[-1].value
        return None

    def detect_conflicts(self) -> List[FactConflict]:
        """
        Scan facts for explicit contradictions.
        e.g. One record states assignment_completed = True while another states = False.
        Does not silently overwrite; surfaces real epistemic conflict.
        """
        conflicts: List[FactConflict] = []
        seen: Dict[Tuple[str, str], Fact] = {}

        for f in self._facts:
            key = (f.predicate, f.entity_id)
            if key in seen:
                prior = seen[key]
                if prior.value != f.value:
                    conflicts.append(FactConflict(
                        predicate=f.predicate,
                        entity_id=f.entity_id,
                        fact1=prior,
                        fact2=f,
                        description=(
                            f"Contradictory values detected for '{f.predicate}' on entity '{f.entity_id}': "
                            f"'{prior.value}' [{prior.source_id}] vs '{f.value}' [{f.source_id}]."
                        )
                    ))
            else:
                seen[key] = f

        return conflicts

    def to_horn_clauses(self) -> List[HornClause]:
        """Convert all stored facts into Horn clauses for SLD resolution."""
        return [f.to_horn_clause() for f in self._facts]

    def fork_scenario(self, scenario_inputs: Dict[str, Any], entity_id: str, policy_id: str) -> "FactBase":
        """
        Create an isolated scenario clone combining verified baseline facts
        with new hypothetical student inputs for WhatIf simulation.
        Crucial requirement: Ensures verified authoritative data is never mutated.
        """
        forked = FactBase()
        # Copy existing verified facts, skipping any predicate overridden by scenario inputs
        for f in self._facts:
            if f.entity_id == entity_id and f.predicate in scenario_inputs:
                continue  # Replace with hypothetical input
            forked.add_fact(f)

        # Inject hypothetical scenario facts
        for pred, val in scenario_inputs.items():
            hyp_fact = Fact(
                id=f"hyp-{pred}-{entity_id}",
                predicate=pred,
                entity_id=entity_id,
                value=val,
                arguments=[entity_id],
                source_id="src-whatif-simulator",
                verification_status=VerificationStatus.HYPOTHETICAL,
                policy_id=policy_id,
                context="Hypothetical student simulation input",
            )
            forked.add_fact(hyp_fact)

        return forked
