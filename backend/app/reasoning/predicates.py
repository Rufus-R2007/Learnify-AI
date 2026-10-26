"""
Predicate Logic Terms and Representations for Learnify AI (Unit III - Knowledge Representation & Logic).
Provides structured first-order predicate logic primitives:
- Constants, Variables, Compound Terms
- Predicates and Horn Clauses
- Substitution application and variable standardization
- Safe string parsing for logical expressions
"""

from typing import List, Dict, Union, Optional, Any, Set
import re


class Term:
    """Base class for all first-order logic terms."""
    pass


class Constant(Term):
    """A constant entity or atomic value in predicate logic (e.g. student_01, ai_course, 75)."""

    def __init__(self, value: Union[str, int, float, bool]):
        self.value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Constant):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(("constant", self.value))

    def __repr__(self) -> str:
        return str(self.value)


class Variable(Term):
    """A logical variable in predicate logic (e.g. X, Y, Student)."""

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Variable):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(("variable", self.name))

    def __repr__(self) -> str:
        return self.name


class CompoundTerm(Term):
    """A compound term f(t1, ..., tn) in first-order logic."""

    def __init__(self, functor: str, args: List[Term]):
        self.functor = functor
        self.args = list(args)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CompoundTerm):
            return self.functor == other.functor and self.args == other.args
        return False

    def __hash__(self) -> int:
        return hash(("compound", self.functor, tuple(self.args)))

    def __repr__(self) -> str:
        arg_str = ", ".join(repr(a) for a in self.args)
        return f"{self.functor}({arg_str})"


class Predicate:
    """
    A predicate P(t1, ..., tn) asserting a relation between terms.
    e.g. enrolled(student_01, ai_course)
         attendance_satisfied(X)
         eligible(X)
    """

    def __init__(self, name: str, args: List[Term], negated: bool = False):
        self.name = name
        self.args = list(args)
        self.negated = negated

    @property
    def arity(self) -> int:
        return len(self.args)

    def get_variables(self) -> Set[str]:
        """Collect all variable names present in predicate arguments."""
        vars_found: Set[str] = set()
        for a in self.args:
            if isinstance(a, Variable):
                vars_found.add(a.name)
            elif isinstance(a, CompoundTerm):
                vars_found.update(_get_vars_from_term(a))
        return vars_found

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Predicate):
            return (
                self.name == other.name
                and self.args == other.args
                and self.negated == other.negated
            )
        return False

    def __hash__(self) -> int:
        return hash(("predicate", self.name, tuple(self.args), self.negated))

    def __repr__(self) -> str:
        prefix = "~" if self.negated else ""
        if not self.args:
            return f"{prefix}{self.name}"
        arg_str = ", ".join(repr(a) for a in self.args)
        return f"{prefix}{self.name}({arg_str})"


def _get_vars_from_term(term: Term) -> Set[str]:
    if isinstance(term, Variable):
        return {term.name}
    if isinstance(term, CompoundTerm):
        res: Set[str] = set()
        for a in term.args:
            res.update(_get_vars_from_term(a))
        return res
    return set()


class HornClause:
    """
    A Horn clause in first-order logic:
    Head :- Body1, Body2, ..., BodyN
    When body is empty, it represents a definite Fact.
    """

    def __init__(self, head: Predicate, body: Optional[List[Predicate]] = None):
        self.head = head
        self.body = list(body or [])

    @property
    def is_fact(self) -> bool:
        return len(self.body) == 0

    def get_variables(self) -> Set[str]:
        vars_found = self.head.get_variables()
        for b in self.body:
            vars_found.update(b.get_variables())
        return vars_found

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, HornClause):
            return self.head == other.head and self.body == other.body
        return False

    def __repr__(self) -> str:
        if not self.body:
            return f"{self.head}."
        body_str = ", ".join(repr(b) for b in self.body)
        return f"{self.head} :- {body_str}."


def apply_substitution(target: Union[Term, Predicate, HornClause], subst: Dict[str, Term]) -> Any:
    """
    Recursively apply variable substitutions to terms, predicates, or Horn clauses.
    e.g. apply {X: student_01} to enrolled(X, ai_course) -> enrolled(student_01, ai_course)
    """
    if not subst:
        return target

    if isinstance(target, Variable):
        if target.name in subst:
            replacement = subst[target.name]
            # Recursively resolve chained substitutions if any
            return apply_substitution(replacement, subst)
        return target

    if isinstance(target, Constant):
        return target

    if isinstance(target, CompoundTerm):
        new_args = [apply_substitution(a, subst) for a in target.args]
        return CompoundTerm(target.functor, new_args)

    if isinstance(target, Predicate):
        new_args = [apply_substitution(a, subst) for a in target.args]
        return Predicate(target.name, new_args, negated=target.negated)

    if isinstance(target, HornClause):
        new_head = apply_substitution(target.head, subst)
        new_body = [apply_substitution(b, subst) for b in target.body]
        return HornClause(new_head, new_body)

    return target


def standardize_apart(clause: HornClause, suffix: Union[str, int]) -> HornClause:
    """
    Standardize variables apart by renaming each variable in the clause with a unique suffix.
    Prevents variable name collisions during SLD resolution steps.
    """
    variables = clause.get_variables()
    subst: Dict[str, Term] = {v: Variable(f"{v}_{suffix}") for v in variables}
    return apply_substitution(clause, subst)


def parse_term(text: str) -> Term:
    """
    Parse a string into a logical Term (Variable, Constant, or CompoundTerm).
    Variables start with uppercase or '?'. Constants are lowercase, numbers, or booleans.
    """
    text = text.strip()
    if not text:
        raise ValueError("Cannot parse empty string into a logical term")

    # Numbers
    if re.fullmatch(r"[-+]?\d+", text):
        return Constant(int(text))
    if re.fullmatch(r"[-+]?\d+\.\d+", text):
        return Constant(float(text))
    if text.lower() == "true":
        return Constant(True)
    if text.lower() == "false":
        return Constant(False)

    # Compound Term: functor(arg1, arg2)
    match_compound = re.fullmatch(r"([a-z_][a-zA-Z0-9_]*)\((.*)\)", text)
    if match_compound:
        functor = match_compound.group(1)
        raw_args = _split_args(match_compound.group(2))
        return CompoundTerm(functor, [parse_term(a) for a in raw_args])

    # Variable: starts with uppercase or ?
    if text.startswith("?") or (text[0].isupper() and text.isidentifier()):
        name = text[1:] if text.startswith("?") else text
        return Variable(name)

    # Constant: lowercase identifier or quoted string
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return Constant(text[1:-1])

    return Constant(text)


def parse_predicate(text: str) -> Predicate:
    """
    Parse a string representation of a predicate, e.g.:
    "enrolled(student_01, ai_course)"
    "~absent(X)"
    "eligible(student_01)"
    """
    text = text.strip()
    negated = False
    if text.startswith("~") or text.startswith("not "):
        negated = True
        text = text[1:].strip() if text.startswith("~") else text[4:].strip()

    match = re.fullmatch(r"([a-zA-Z_][a-zA-Z0-9_]*)(?:\((.*)\))?", text)
    if not match:
        raise ValueError(f"Invalid predicate format: '{text}'")

    name = match.group(1)
    args_str = match.group(2)
    if args_str is None or not args_str.strip():
        return Predicate(name, [], negated=negated)

    raw_args = _split_args(args_str)
    args = [parse_term(a) for a in raw_args]
    return Predicate(name, args, negated=negated)


def _split_args(args_str: str) -> List[str]:
    """Split comma-separated arguments while respecting nested parentheses and quotes."""
    args: List[str] = []
    current: List[str] = []
    paren_depth = 0
    in_quote = False
    quote_char = ""

    for ch in args_str:
        if ch in ('"', "'"):
            if not in_quote:
                in_quote = True
                quote_char = ch
            elif quote_char == ch:
                in_quote = False
                quote_char = ""
            current.append(ch)
        elif not in_quote:
            if ch == "(":
                paren_depth += 1
                current.append(ch)
            elif ch == ")":
                paren_depth -= 1
                current.append(ch)
            elif ch == "," and paren_depth == 0:
                args.append("".join(current).strip())
                current = []
            else:
                current.append(ch)
        else:
            current.append(ch)

    if current:
        args.append("".join(current).strip())
    return [a for a in args if a]
