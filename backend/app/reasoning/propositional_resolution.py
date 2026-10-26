"""
Propositional Resolution and Policy Consistency Engine for Learnify AI (Unit III - Concept 4).
Validates whether a set of academic policy conditions or constraints is logically consistent.
Detects provable contradictions (derivation of the empty clause $\square$) using systematic resolution.
"""

from typing import List, Set, FrozenSet, Tuple, Optional, Dict, Any


class Literal:
    """A propositional literal: a variable or its negation (e.g. P or ~P)."""

    def __init__(self, name: str, negated: bool = False):
        self.name = name.strip()
        self.negated = negated

    def complement(self) -> "Literal":
        """Return the complementary literal (~L if L, L if ~L)."""
        return Literal(self.name, not self.negated)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Literal):
            return self.name == other.name and self.negated == other.negated
        return False

    def __hash__(self) -> int:
        return hash(("literal", self.name, self.negated))

    def __repr__(self) -> str:
        return f"~{self.name}" if self.negated else self.name


class Clause:
    """A disjunctive clause represented as a frozenset of literals: (L1 | L2 | ... | Ln)."""

    def __init__(self, literals: Optional[Any] = None):
        if literals is None:
            self.literals: FrozenSet[Literal] = frozenset()
        elif isinstance(literals, (set, frozenset, list, tuple)):
            self.literals = frozenset(literals)
        elif isinstance(literals, Literal):
            self.literals = frozenset([literals])
        else:
            raise TypeError(f"Cannot initialize Clause from {type(literals)}")

    @property
    def is_empty(self) -> bool:
        """The empty clause (represented as Box or False) signifies a logical contradiction."""
        return len(self.literals) == 0

    @property
    def is_tautology(self) -> bool:
        """Check if clause contains both P and ~P, making it vacuously true."""
        names = {l.name for l in self.literals if not l.negated}
        neg_names = {l.name for l in self.literals if l.negated}
        return bool(names & neg_names)

    def __len__(self) -> int:
        return len(self.literals)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Clause):
            return self.literals == other.literals
        return False

    def __hash__(self) -> int:
        return hash(self.literals)

    def __repr__(self) -> str:
        if self.is_empty:
            return "[]"  # Contradiction / empty clause
        return " | ".join(sorted(repr(lit) for lit in self.literals))


class ResolutionStep:
    """A record of a single binary resolution step between two clauses."""

    def __init__(
        self,
        step_id: int,
        parent1: Clause,
        parent2: Clause,
        resolved_literal: Literal,
        resolvent: Clause,
        is_contradiction: bool,
    ):
        self.step_id = step_id
        self.parent1 = parent1
        self.parent2 = parent2
        self.resolved_literal = resolved_literal
        self.resolvent = resolvent
        self.is_contradiction = is_contradiction

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step_id,
            "clause1": repr(self.parent1),
            "clause2": repr(self.parent2),
            "cancelled_literal": repr(self.resolved_literal),
            "derived_resolvent": repr(self.resolvent),
            "contradiction_derived": self.is_contradiction,
        }


class ConsistencyReport:
    """Result of propositional resolution consistency checking."""

    def __init__(
        self,
        is_consistent: bool,
        contradiction_found: bool,
        initial_clauses: List[Clause],
        derived_clauses: List[Clause],
        steps: List[ResolutionStep],
        explanation: str,
    ):
        self.is_consistent = is_consistent
        self.contradiction_found = contradiction_found
        self.initial_clauses = initial_clauses
        self.derived_clauses = derived_clauses
        self.steps = steps
        self.explanation = explanation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_consistent": self.is_consistent,
            "contradiction_found": self.contradiction_found,
            "initial_clauses": [repr(c) for c in self.initial_clauses],
            "total_steps": len(self.steps),
            "resolution_trace": [s.to_dict() for s in self.steps],
            "explanation": self.explanation,
        }


def resolve_clauses(c1: Clause, c2: Clause) -> List[Tuple[Literal, Clause]]:
    """
    Compute all non-tautological resolvents between two clauses.
    For each complementary pair (L in c1, ~L in c2), yields (L, resolvent).
    """
    resolvents: List[Tuple[Literal, Clause]] = []
    for l1 in c1.literals:
        comp = l1.complement()
        if comp in c2.literals:
            # Resolvent is (c1 - {l1}) | (c2 - {comp})
            remaining1 = {l for l in c1.literals if l != l1}
            remaining2 = {l for l in c2.literals if l != comp}
            merged = Clause(remaining1 | remaining2)
            if not merged.is_tautology:
                resolvents.append((l1, merged))
    return resolvents


def check_consistency(clauses: List[Clause], max_iterations: int = 150) -> ConsistencyReport:
    """
    Run propositional resolution to determine whether the set of clauses is logically consistent.
    Returns a ConsistencyReport with full derivation steps.
    """
    # Filter out initial tautologies
    working_set: Set[Clause] = {c for c in clauses if not c.is_tautology}
    for c in working_set:
        if c.is_empty:
            return ConsistencyReport(
                is_consistent=False,
                contradiction_found=True,
                initial_clauses=clauses,
                derived_clauses=[],
                steps=[],
                explanation="Contradiction already explicitly present in input: empty clause provided.",
            )

    steps: List[ResolutionStep] = []
    step_counter = 1
    new_clauses_derived: List[Clause] = []

    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        new_in_iteration: Set[Clause] = set()
        clause_list = list(working_set)

        found_contradiction = False
        for i in range(len(clause_list)):
            for j in range(i + 1, len(clause_list)):
                c1 = clause_list[i]
                c2 = clause_list[j]

                for lit, resolvent in resolve_clauses(c1, c2):
                    if resolvent not in working_set:
                        new_in_iteration.add(resolvent)
                        new_clauses_derived.append(resolvent)
                        is_contra = resolvent.is_empty

                        step = ResolutionStep(
                            step_id=step_counter,
                            parent1=c1,
                            parent2=c2,
                            resolved_literal=lit,
                            resolvent=resolvent,
                            is_contradiction=is_contra,
                        )
                        steps.append(step)
                        step_counter += 1

                        if is_contra:
                            found_contradiction = True
                            return ConsistencyReport(
                                is_consistent=False,
                                contradiction_found=True,
                                initial_clauses=clauses,
                                derived_clauses=new_clauses_derived,
                                steps=steps,
                                explanation=(
                                    f"Contradiction derived at step {step.step_id} by resolving "
                                    f"'{c1}' and '{c2}' on literal '{lit}'. "
                                    f"The clause set is mathematically unsatisfiable."
                                ),
                            )

        if not new_in_iteration:
            # Fixed point reached: no new clauses can be derived
            break

        working_set.update(new_in_iteration)

    return ConsistencyReport(
        is_consistent=True,
        contradiction_found=False,
        initial_clauses=clauses,
        derived_clauses=new_clauses_derived,
        steps=steps,
        explanation=(
            f"Resolution terminated after {len(steps)} inference steps without deriving an empty clause. "
            f"The policy conditions are logically consistent and satisfiable."
        ),
    )


def parse_clause(text: str) -> Clause:
    """
    Parse a clause string like "P | ~Q | R" or "satisfies_attendance | exception_approved".
    """
    text = text.strip()
    if text == "[]":
        return Clause([])
    parts = [p.strip() for p in text.split("|") if p.strip()]
    lits: List[Literal] = []
    for p in parts:
        if p.startswith("~") or p.startswith("!"):
            lits.append(Literal(p[1:].strip(), negated=True))
        else:
            lits.append(Literal(p, negated=False))
    return Clause(lits)
