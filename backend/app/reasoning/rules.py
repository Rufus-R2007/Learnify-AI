"""
Declarative Academic Decision Rules and Policies for Learnify AI (Unit IV - Concept 6).
Represents knowledge declaratively as structured data, separated from inference procedures:
- Stable rule identifiers and descriptions
- Declarative condition operators evaluated safely without eval()
- Named policies with configurable thresholds and versioning
- Exception relationships and rule priority weighting
- Prominent illustrative academic policy disclaimers
"""

from typing import List, Dict, Any, Optional, Union
from enum import Enum
from app.reasoning.predicates import Predicate, HornClause, Variable, Constant


class ConditionOperator(str, Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    IS_TRUE = "is_true"
    IS_FALSE = "is_false"
    IN = "in"


class RuleCondition:
    """
    A single declarative prerequisite condition for a rule.
    Evaluated using safe deterministic comparison operators without eval().
    """

    def __init__(
        self,
        predicate: str,
        operator: Union[ConditionOperator, str],
        expected_value: Any,
        description: Optional[str] = None,
    ):
        self.predicate = predicate
        self.operator = (
            operator if isinstance(operator, ConditionOperator)
            else ConditionOperator(operator)
        )
        self.expected_value = expected_value
        self.description = description or f"{predicate} {self.operator.value} {expected_value}"

    def evaluate(self, actual_value: Any) -> bool:
        """Evaluate condition against an actual value safely without eval()."""
        if actual_value is None:
            return False

        op = self.operator
        exp = self.expected_value

        try:
            if op == ConditionOperator.EQUALS:
                return actual_value == exp
            elif op == ConditionOperator.NOT_EQUALS:
                return actual_value != exp
            elif op == ConditionOperator.GREATER_EQUAL:
                return float(actual_value) >= float(exp)
            elif op == ConditionOperator.LESS_EQUAL:
                return float(actual_value) <= float(exp)
            elif op == ConditionOperator.GREATER_THAN:
                return float(actual_value) > float(exp)
            elif op == ConditionOperator.LESS_THAN:
                return float(actual_value) < float(exp)
            elif op == ConditionOperator.IS_TRUE:
                return bool(actual_value) is True
            elif op == ConditionOperator.IS_FALSE:
                return bool(actual_value) is False
            elif op == ConditionOperator.IN:
                return actual_value in exp
        except (ValueError, TypeError):
            return False

        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "predicate": self.predicate,
            "operator": self.operator.value,
            "expected_value": self.expected_value,
            "description": self.description,
        }

    def __repr__(self) -> str:
        return f"{self.predicate} {self.operator.value} {self.expected_value}"


class RuleConclusion:
    """The conclusion asserted when all conditions of a rule are satisfied."""

    def __init__(self, predicate: str, value: Any, description: Optional[str] = None):
        self.predicate = predicate
        self.value = value
        self.description = description or f"{predicate} = {value}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "predicate": self.predicate,
            "value": self.value,
            "description": self.description,
        }

    def __repr__(self) -> str:
        return f"{self.predicate} = {self.value}"


class Rule:
    """
    A declarative production rule:
    IF condition_1 AND condition_2 ... THEN conclusion
    """

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        policy_id: str,
        conditions: List[RuleCondition],
        conclusion: RuleConclusion,
        priority: int = 10,
        is_exception: bool = False,
        overrides_rule_id: Optional[str] = None,
        source_id: str = "src-demo",
    ):
        self.id = id
        self.name = name
        self.description = description
        self.policy_id = policy_id
        self.conditions = list(conditions)
        self.conclusion = conclusion
        self.priority = priority
        self.is_exception = is_exception
        self.overrides_rule_id = overrides_rule_id
        self.source_id = source_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "policy_id": self.policy_id,
            "conditions": [c.to_dict() for c in self.conditions],
            "conclusion": self.conclusion.to_dict(),
            "priority": self.priority,
            "is_exception": self.is_exception,
            "overrides_rule_id": self.overrides_rule_id,
            "source_id": self.source_id,
        }

    def to_horn_clause(self, entity_var: str = "X") -> HornClause:
        """Convert into a First-Order Horn Clause representation."""
        v = Variable(entity_var)
        head = Predicate(self.conclusion.predicate, [v, Constant(self.conclusion.value)])
        body = [Predicate(c.predicate, [v, Constant(c.expected_value)]) for c in self.conditions]
        return HornClause(head, body)

    def __repr__(self) -> str:
        cond_str = " AND ".join(repr(c) for c in self.conditions)
        exc_tag = f" [EXCEPTION overrides {self.overrides_rule_id}]" if self.is_exception else ""
        return f"Rule({self.id}: IF {cond_str} THEN {self.conclusion}{exc_tag})"


class Policy:
    """
    An academic eligibility or decision policy grouping declarative rules.
    Every policy includes an explicit disclaimer stating it is illustrative.
    """

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        rules: List[Rule],
        default_decision: str = "INELIGIBLE",
        version: str = "1.0.0",
        is_illustrative: bool = True,
        disclaimer: str = (
            "Illustrative academic policy for demonstration. "
            "This is not an official institutional eligibility decision."
        ),
    ):
        self.id = id
        self.name = name
        self.description = description
        self.rules = list(rules)
        self.default_decision = default_decision
        self.version = version
        self.is_illustrative = is_illustrative
        self.disclaimer = disclaimer

    def get_rule_by_id(self, rule_id: str) -> Optional[Rule]:
        for r in self.rules:
            if r.id == rule_id:
                return r
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "is_illustrative": self.is_illustrative,
            "disclaimer": self.disclaimer,
            "default_decision": self.default_decision,
            "total_rules": len(self.rules),
            "rules": [r.to_dict() for r in self.rules],
        }

    def __repr__(self) -> str:
        return f"Policy({self.id} v{self.version}: '{self.name}', {len(self.rules)} rules)"
