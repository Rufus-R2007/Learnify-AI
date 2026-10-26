"""
SLD-Resolution for First-Order Horn Clauses for Learnify AI (Unit III - Concept 5).
Implements goal-directed SLD (Selective Linear Definite clause) resolution using Robinson's
unification algorithm.

Note:
This engine specifically operates on Horn clauses (definite clauses with at most one positive
literal in the head) rather than unrestricted first-order theorem proving. This provides
guaranteed decider properties for polynomial-complexity academic policy proofs.
"""

from typing import List, Dict, Optional, Set, Tuple, Any
from app.reasoning.predicates import (
    Predicate,
    HornClause,
    Term,
    Variable,
    Constant,
    apply_substitution,
    standardize_apart,
    parse_predicate,
)
from app.reasoning.unification import unify, UnificationResult


class SLDStep:
    """A single execution step in the SLD derivation tree."""

    def __init__(
        self,
        step_id: int,
        depth: int,
        selected_goal: Predicate,
        candidate_clause: HornClause,
        unification_bindings: Dict[str, Term],
        resulting_subgoals: List[Predicate],
    ):
        self.step_id = step_id
        self.depth = depth
        self.selected_goal = selected_goal
        self.candidate_clause = candidate_clause
        self.unification_bindings = unification_bindings
        self.resulting_subgoals = resulting_subgoals

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step_id,
            "depth": self.depth,
            "selected_goal": repr(self.selected_goal),
            "matched_clause": repr(self.candidate_clause),
            "unification": {k: repr(v) for k, v in self.unification_bindings.items()},
            "resulting_subgoals": [repr(g) for g in self.resulting_subgoals],
        }


class SLDProofResult:
    """Complete diagnostic report for an SLD resolution proof attempt."""

    def __init__(
        self,
        goal: Predicate,
        proven: bool,
        substitutions: Dict[str, Term],
        rules_used: List[HornClause],
        facts_used: List[HornClause],
        missing_premises: List[Predicate],
        steps: List[SLDStep],
        status: str,
        explanation: str,
    ):
        self.goal = goal
        self.proven = proven
        self.substitutions = substitutions
        self.rules_used = rules_used
        self.facts_used = facts_used
        self.missing_premises = missing_premises
        self.steps = steps
        self.status = status
        self.explanation = explanation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_goal": repr(self.goal),
            "proven": self.proven,
            "status": self.status,
            "substitutions": {k: repr(v) for k, v in self.substitutions.items()},
            "rules_used": [repr(r) for r in self.rules_used],
            "facts_used": [repr(f) for f in self.facts_used],
            "missing_premises": [repr(m) for m in self.missing_premises],
            "total_steps": len(self.steps),
            "steps": [s.to_dict() for s in self.steps],
            "explanation": self.explanation,
        }


class HornResolutionEngine:
    """
    SLD-Resolution engine for definite Horn clauses.
    Uses Robinson's unification with variable standardizing and cycle protection.
    """

    def __init__(self, clauses: Optional[List[HornClause]] = None, max_depth: int = 15):
        self.clauses = list(clauses or [])
        self.max_depth = max_depth

    def add_clause(self, clause: HornClause) -> None:
        self.clauses.append(clause)

    def prove(self, goal: Predicate) -> SLDProofResult:
        """
        Attempt to prove the target goal using SLD resolution over stored Horn clauses.
        Returns SLDProofResult with complete proof tree or diagnostic missing premises.
        """
        steps: List[SLDStep] = []
        rules_used: List[HornClause] = []
        facts_used: List[HornClause] = []
        missing_premises: List[Predicate] = []
        step_counter = [1]  # Mutable cell for step counter across recursive calls

        success, final_subst = self._sld_solve(
            goals=[goal],
            subst={},
            depth=0,
            call_stack=[],
            steps=steps,
            rules_used=rules_used,
            facts_used=facts_used,
            missing_premises=missing_premises,
            step_counter=step_counter,
        )

        # Filter out temporary standardized variables from final output substitutions
        target_vars = goal.get_variables()
        filtered_subst = {
            k: v for k, v in final_subst.items()
            if (not target_vars or k in target_vars) and not ("_" in k and k.split("_")[-1].isdigit())
        }

        if success:
            explanation = (
                f"Goal '{goal}' successfully PROVEN via SLD-resolution in {len(steps)} steps. "
                f"Resolved using {len(rules_used)} rule(s) and {len(facts_used)} fact(s)."
            )
            return SLDProofResult(
                goal=goal,
                proven=True,
                substitutions=filtered_subst,
                rules_used=rules_used,
                facts_used=facts_used,
                missing_premises=[],
                steps=steps,
                status="PROVEN",
                explanation=explanation,
            )
        elif missing_premises:
            explanation = (
                f"Goal '{goal}' CANNOT BE PROVEN. Missing required premise(s): "
                f"{', '.join(repr(m) for m in missing_premises)}."
            )
            return SLDProofResult(
                goal=goal,
                proven=False,
                substitutions={},
                rules_used=rules_used,
                facts_used=facts_used,
                missing_premises=missing_premises,
                steps=steps,
                status="UNKNOWN",
                explanation=explanation,
            )
        else:
            explanation = f"Goal '{goal}' could not be proven from available clauses (search space exhausted)."
            return SLDProofResult(
                goal=goal,
                proven=False,
                substitutions={},
                rules_used=rules_used,
                facts_used=facts_used,
                missing_premises=[],
                steps=steps,
                status="FAILED",
                explanation=explanation,
            )

    def _sld_solve(
        self,
        goals: List[Predicate],
        subst: Dict[str, Term],
        depth: int,
        call_stack: List[Predicate],
        steps: List[SLDStep],
        rules_used: List[HornClause],
        facts_used: List[HornClause],
        missing_premises: List[Predicate],
        step_counter: List[int],
    ) -> Tuple[bool, Dict[str, Term]]:
        """Recursive SLD-derivation worker with backtracking and cycle protection."""
        if not goals:
            return True, subst

        if depth >= self.max_depth:
            # Recursion depth limit reached
            return False, subst

        # Select leftmost goal
        current_goal = apply_substitution(goals[0], subst)

        # Cycle check: prevent infinite recursion
        if any(current_goal == g for g in call_stack):
            return False, subst

        remaining_goals = goals[1:]
        matched_any_candidate = False

        for original_clause in self.clauses:
            # Standardize apart variables to avoid variable capture
            clause = standardize_apart(original_clause, step_counter[0])

            unif = unify(current_goal, clause.head, subst)
            if unif.success:
                matched_any_candidate = True
                new_subst = unif.substitutions

                # Build new subgoals: replace current_goal with clause.body
                new_subgoals = [apply_substitution(b, new_subst) for b in clause.body] + remaining_goals

                step = SLDStep(
                    step_id=step_counter[0],
                    depth=depth,
                    selected_goal=current_goal,
                    candidate_clause=original_clause,
                    unification_bindings=unif.substitutions,
                    resulting_subgoals=new_subgoals,
                )
                steps.append(step)
                step_counter[0] += 1

                if original_clause.is_fact:
                    if original_clause not in facts_used:
                        facts_used.append(original_clause)
                else:
                    if original_clause not in rules_used:
                        rules_used.append(original_clause)

                # Recurse down this SLD branch
                sub_success, sub_subst = self._sld_solve(
                    goals=new_subgoals,
                    subst=new_subst,
                    depth=depth + 1,
                    call_stack=call_stack + [current_goal],
                    steps=steps,
                    rules_used=rules_used,
                    facts_used=facts_used,
                    missing_premises=missing_premises,
                    step_counter=step_counter,
                )

                if sub_success:
                    return True, sub_subst

        if not matched_any_candidate:
            if current_goal not in missing_premises:
                missing_premises.append(current_goal)

        return False, subst
