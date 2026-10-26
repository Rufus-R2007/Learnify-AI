"""
Robinson's First-Order Unification Algorithm for Learnify AI (Unit III - Knowledge Representation & Logic).
Implements complete first-order term and predicate unification with:
- Constant-constant matching
- Variable binding & repeated variable consistency checks
- Compound term recursion
- Predicate name and arity verification
- Robinson occurs-check for circular term safety
- Idempotent most general unifier (MGU) computation
"""

from typing import Dict, Optional, Union, List
from app.reasoning.predicates import (
    Term,
    Constant,
    Variable,
    CompoundTerm,
    Predicate,
    apply_substitution,
)


class UnificationResult:
    """Detailed outcome of a unification attempt between two logical expressions."""

    def __init__(
        self,
        success: bool,
        substitutions: Optional[Dict[str, Term]] = None,
        failure_reason: Optional[str] = None,
        left_repr: Optional[str] = None,
        right_repr: Optional[str] = None,
    ):
        self.success = success
        self.substitutions = substitutions or {}
        self.failure_reason = failure_reason
        self.left_repr = left_repr
        self.right_repr = right_repr

    def __bool__(self) -> bool:
        return self.success

    def __repr__(self) -> str:
        if self.success:
            bindings = {k: repr(v) for k, v in self.substitutions.items()}
            return f"UnificationResult(SUCCESS, bindings={bindings})"
        return f"UnificationResult(FAILURE, reason='{self.failure_reason}')"


def occurs_check(var: Variable, term: Term, subst: Dict[str, Term]) -> bool:
    """
    Check if variable 'var' occurs inside 'term' to prevent infinite recursive terms.
    e.g. X = f(X) fails the occurs-check.
    """
    if var == term:
        return True

    if isinstance(term, Variable) and term.name in subst:
        return occurs_check(var, subst[term.name], subst)

    if isinstance(term, CompoundTerm):
        return any(occurs_check(var, a, subst) for a in term.args)

    return False


def unify(
    x: Union[Term, Predicate],
    y: Union[Term, Predicate],
    subst: Optional[Dict[str, Term]] = None,
) -> UnificationResult:
    """
    Compute the Most General Unifier (MGU) of two expressions x and y.
    Returns UnificationResult containing success status, substitution dictionary,
    and explanatory failure reason if unsuccessful.
    """
    working_subst = dict(subst or {})
    result = _unify_internal(x, y, working_subst)
    if result is None:
        return UnificationResult(
            success=False,
            failure_reason=f"Cannot unify {repr(x)} with {repr(y)}",
            left_repr=repr(x),
            right_repr=repr(y),
        )

    # Normalize substitutions to ensure fully dereferenced bindings
    normalized_subst: Dict[str, Term] = {}
    for k, v in result.items():
        normalized_subst[k] = apply_substitution(v, result)

    return UnificationResult(
        success=True,
        substitutions=normalized_subst,
        left_repr=repr(x),
        right_repr=repr(y),
    )


def _unify_internal(
    x: Union[Term, Predicate],
    y: Union[Term, Predicate],
    subst: Dict[str, Term],
) -> Optional[Dict[str, Term]]:
    """Internal recursive worker returning substitution dict or None on failure."""
    if subst is None:
        return None

    # If already identical, nothing new to bind
    if x == y:
        return subst

    # Variable on left
    if isinstance(x, Variable):
        return _unify_variable(x, y, subst)

    # Variable on right
    if isinstance(y, Variable):
        return _unify_variable(y, x, subst)

    # Compound terms: same functor and arity required
    if isinstance(x, CompoundTerm) and isinstance(y, CompoundTerm):
        if x.functor != y.functor or len(x.args) != len(y.args):
            return None
        current_subst = subst
        for a1, a2 in zip(x.args, y.args):
            current_subst = _unify_internal(a1, a2, current_subst)
            if current_subst is None:
                return None
        return current_subst

    # Predicates: same name, arity, and negation required
    if isinstance(x, Predicate) and isinstance(y, Predicate):
        if x.name != y.name or x.arity != y.arity or x.negated != y.negated:
            return None
        current_subst = subst
        for a1, a2 in zip(x.args, y.args):
            current_subst = _unify_internal(a1, a2, current_subst)
            if current_subst is None:
                return None
        return current_subst

    # Different constants or incompatible term types
    return None


def _unify_variable(
    var: Variable,
    x: Union[Term, Predicate],
    subst: Dict[str, Term],
) -> Optional[Dict[str, Term]]:
    """Bind a variable to a term while respecting existing substitutions and occurs-check."""
    if var.name in subst:
        return _unify_internal(subst[var.name], x, subst)

    if isinstance(x, Variable) and x.name in subst:
        return _unify_internal(var, subst[x.name], subst)

    # Occurs-check: variable cannot occur inside term x
    if isinstance(x, Term) and occurs_check(var, x, subst):
        return None

    if not isinstance(x, Term):
        # Cannot bind a variable directly to a predicate
        return None

    new_subst = dict(subst)
    new_subst[var.name] = x
    return new_subst
