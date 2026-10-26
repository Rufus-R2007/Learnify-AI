"""
Backward Chaining Goal-Driven Diagnostic Engine for Learnify AI (Unit IV - Concept 8).
Answers student queries like "Why am I eligible?" or "Why am I not eligible?":
- Recursively decomposes the target goal into required prerequisite conditions
- Traverses matching declarative rules and facts in working memory
- Distinguishes PROVEN, DISPROVEN, UNKNOWN, and CONFLICT states
- Pinpoints exact missing or unsatisfied conditions without conflating unknown with false
- Connects to Horn-clause SLD resolution for formal predicate verification
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from app.reasoning.facts import Fact, FactBase
from app.reasoning.rules import Rule, Policy, RuleCondition, ConditionOperator
from app.reasoning.horn_resolution import HornResolutionEngine, SLDProofResult
from app.reasoning.predicates import Predicate, Constant, Variable


class BackwardProofNode:
    """A node in the backward reasoning explanation tree."""

    def __init__(
        self,
        goal: str,
        status: str,  # PROVEN, DISPROVEN, UNKNOWN, CONFLICT
        rule_id: Optional[str] = None,
        rule_name: Optional[str] = None,
        supporting_facts: Optional[Dict[str, Any]] = None,
        unsatisfied_reasons: Optional[List[str]] = None,
        missing_conditions: Optional[List[str]] = None,
        subnodes: Optional[List["BackwardProofNode"]] = None,
    ):
        self.goal = goal
        self.status = status
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.supporting_facts = supporting_facts or {}
        self.unsatisfied_reasons = unsatisfied_reasons or []
        self.missing_conditions = missing_conditions or []
        self.subnodes = subnodes or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "status": self.status,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "supporting_facts": self.supporting_facts,
            "unsatisfied_reasons": self.unsatisfied_reasons,
            "missing_conditions": self.missing_conditions,
            "subnodes": [s.to_dict() for s in self.subnodes],
        }


class BackwardChainingResult:
    """Outcome of goal-driven diagnostic evaluation."""

    def __init__(
        self,
        target_goal: str,
        target_value: Any,
        status: str,  # PROVEN, DISPROVEN, UNKNOWN, CONFLICT
        entity_id: str,
        proven: bool,
        matching_rules: List[Rule],
        supporting_facts: Dict[str, Any],
        missing_conditions: List[str],
        contradictions: List[str],
        proof_tree: BackwardProofNode,
        explanation: str,
        sld_result: Optional[SLDProofResult] = None,
    ):
        self.target_goal = target_goal
        self.target_value = target_value
        self.status = status
        self.entity_id = entity_id
        self.proven = proven
        self.matching_rules = matching_rules
        self.supporting_facts = supporting_facts
        self.missing_conditions = missing_conditions
        self.contradictions = contradictions
        self.proof_tree = proof_tree
        self.explanation = explanation
        self.sld_result = sld_result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_goal": self.target_goal,
            "target_value": self.target_value,
            "status": self.status,
            "entity_id": self.entity_id,
            "proven": self.proven,
            "matching_rules": [r.to_dict() for r in self.matching_rules],
            "supporting_facts": self.supporting_facts,
            "missing_conditions": self.missing_conditions,
            "contradictions": self.contradictions,
            "proof_tree": self.proof_tree.to_dict(),
            "explanation": self.explanation,
            "sld_trace": self.sld_result.to_dict() if self.sld_result else None,
        }


class BackwardChainingEngine:
    """
    Goal-driven backward chaining reasoning engine.
    """

    def __init__(self, policy: Policy):
        self.policy = policy

    def _resolve_subgoal(
        self,
        fact_base: FactBase,
        entity_id: str,
        predicate: str,
        expected_value: Any,
        depth: int = 0,
        visited: Optional[Set[str]] = None,
    ) -> Tuple[bool, Optional[Any], Optional[BackwardProofNode]]:
        """
        Recursively resolve an antecedent premise through stored facts or antecedent rules.
        """
        if visited is None:
            visited = set()

        # 1. Direct fact lookup
        val = fact_base.get_fact_value(predicate, entity_id)
        if val is not None:
            return True, val, None

        if depth > 10 or predicate in visited:
            return False, None, None

        new_visited = visited | {predicate}

        # 2. Check candidate rules deriving this predicate
        candidate_rules = [
            r for r in self.policy.rules
            if r.conclusion.predicate == predicate
        ]
        candidate_rules.sort(key=lambda r: r.priority, reverse=True)

        for rule in candidate_rules:
            rule_all_met = True
            rule_facts: Dict[str, Any] = {}
            subnodes: List[BackwardProofNode] = []

            for cond in rule.conditions:
                resolved, cond_val, subnode = self._resolve_subgoal(
                    fact_base, entity_id, cond.predicate, cond.expected_value, depth + 1, new_visited
                )
                if resolved and cond.evaluate(cond_val):
                    rule_facts[cond.predicate] = cond_val
                    if subnode:
                        subnodes.append(subnode)
                else:
                    rule_all_met = False
                    break

            if rule_all_met:
                node = BackwardProofNode(
                    goal=f"Prove Subgoal '{predicate} = {rule.conclusion.value}'",
                    status="PROVEN",
                    rule_id=rule.id,
                    rule_name=rule.name,
                    supporting_facts=rule_facts,
                    subnodes=subnodes,
                )
                return True, rule.conclusion.value, node

        return False, None, None

    def diagnose_goal(
        self,
        fact_base: FactBase,
        entity_id: str,
        goal_predicate: str = "eligible",
        desired_value: Any = True,
    ) -> BackwardChainingResult:
        """
        Investigate whether a goal (e.g. eligible = True) can be proven for entity_id.
        Distinguishes PROVEN, DISPROVEN, UNKNOWN, and CONFLICT.
        """
        # First check for factual conflicts in working memory
        conflicts = fact_base.detect_conflicts()
        if conflicts:
            conflict_descs = [c.description for c in conflicts]
            root_node = BackwardProofNode(
                goal=f"{goal_predicate} = {desired_value}",
                status="CONFLICT",
                unsatisfied_reasons=conflict_descs,
            )
            return BackwardChainingResult(
                target_goal=goal_predicate,
                target_value=desired_value,
                status="CONFLICT",
                entity_id=entity_id,
                proven=False,
                matching_rules=[],
                supporting_facts={},
                missing_conditions=[],
                contradictions=conflict_descs,
                proof_tree=root_node,
                explanation=f"Cannot evaluate goal due to contradictory facts: {'; '.join(conflict_descs)}",
            )

        # Find rules whose conclusion matches target goal
        matching_rules = [
            r for r in self.policy.rules
            if r.conclusion.predicate == goal_predicate and r.conclusion.value == desired_value
        ]
        # Sort by priority descending (exceptions first)
        matching_rules.sort(key=lambda r: r.priority, reverse=True)

        if not matching_rules:
            root_node = BackwardProofNode(
                goal=f"{goal_predicate} = {desired_value}",
                status="UNKNOWN",
                unsatisfied_reasons=[f"No production rule derives '{goal_predicate} = {desired_value}'"],
            )
            return BackwardChainingResult(
                target_goal=goal_predicate,
                target_value=desired_value,
                status="UNKNOWN",
                entity_id=entity_id,
                proven=False,
                matching_rules=[],
                supporting_facts={},
                missing_conditions=[goal_predicate],
                contradictions=[],
                proof_tree=root_node,
                explanation=f"No rules in policy '{self.policy.name}' establish '{goal_predicate} = {desired_value}'.",
            )

        # Investigate candidate rules
        all_missing_conditions: Set[str] = set()
        all_unsatisfied_reasons: List[str] = []
        rule_subnodes: List[BackwardProofNode] = []

        proven_rule: Optional[Rule] = None
        proven_facts: Dict[str, Any] = {}

        for rule in matching_rules:
            rule_missing: List[str] = []
            rule_unsatisfied: List[str] = []
            rule_facts: Dict[str, Any] = {}
            rule_all_met = True

            for cond in rule.conditions:
                resolved, val, subnode = self._resolve_subgoal(
                    fact_base, entity_id, cond.predicate, cond.expected_value
                )
                if not resolved:
                    rule_missing.append(f"{cond.predicate} (required {cond.operator.value} {cond.expected_value})")
                    all_missing_conditions.add(cond.predicate)
                    rule_all_met = False
                elif cond.evaluate(val):
                    rule_facts[cond.predicate] = val
                    if subnode:
                        rule_subnodes.append(subnode)
                else:
                    reason = (
                        f"Condition '{cond.predicate}' not met: actual value '{val}' "
                        f"does not satisfy '{cond.operator.value} {cond.expected_value}'"
                    )
                    rule_unsatisfied.append(reason)
                    all_unsatisfied_reasons.append(reason)
                    rule_all_met = False

            if rule_all_met:
                rule_node = BackwardProofNode(
                    goal=f"Apply Rule {rule.id}",
                    status="PROVEN",
                    rule_id=rule.id,
                    rule_name=rule.name,
                    supporting_facts=rule_facts,
                )
                rule_subnodes.append(rule_node)
                proven_rule = rule
                proven_facts = rule_facts
                break
            else:
                rule_status = "UNKNOWN" if rule_missing and not rule_unsatisfied else "DISPROVEN"
                rule_node = BackwardProofNode(
                    goal=f"Evaluate Rule {rule.id}",
                    status=rule_status,
                    rule_id=rule.id,
                    rule_name=rule.name,
                    supporting_facts=rule_facts,
                    unsatisfied_reasons=rule_unsatisfied,
                    missing_conditions=rule_missing,
                )
                rule_subnodes.append(rule_node)

        # Run Horn resolution engine for formal SLD proof trace
        sld_result: Optional[SLDProofResult] = None
        try:
            clauses = [r.to_horn_clause() for r in self.policy.rules] + fact_base.to_horn_clauses()
            horn_engine = HornResolutionEngine(clauses)
            goal_pred = Predicate(goal_predicate, [Constant(entity_id), Constant(desired_value)])
            sld_result = horn_engine.prove(goal_pred)
        except Exception:
            pass

        if proven_rule:
            root_node = BackwardProofNode(
                goal=f"{goal_predicate} = {desired_value}",
                status="PROVEN",
                rule_id=proven_rule.id,
                rule_name=proven_rule.name,
                supporting_facts=proven_facts,
                subnodes=rule_subnodes,
            )
            explanation = (
                f"Goal '{goal_predicate} = {desired_value}' is PROVEN by rule '{proven_rule.name}' ({proven_rule.id}). "
                f"All required premises are satisfied by verified student facts: {proven_facts}."
            )
            return BackwardChainingResult(
                target_goal=goal_predicate,
                target_value=desired_value,
                status="PROVEN",
                entity_id=entity_id,
                proven=True,
                matching_rules=matching_rules,
                supporting_facts=proven_facts,
                missing_conditions=[],
                contradictions=[],
                proof_tree=root_node,
                explanation=explanation,
                sld_result=sld_result,
            )

        if all_missing_conditions and not all_unsatisfied_reasons:
            root_node = BackwardProofNode(
                goal=f"{goal_predicate} = {desired_value}",
                status="UNKNOWN",
                missing_conditions=sorted(list(all_missing_conditions)),
                subnodes=rule_subnodes,
            )
            explanation = (
                f"Goal '{goal_predicate} = {desired_value}' status is UNKNOWN. "
                f"Missing required information for condition(s): {', '.join(sorted(all_missing_conditions))}."
            )
            return BackwardChainingResult(
                target_goal=goal_predicate,
                target_value=desired_value,
                status="UNKNOWN",
                entity_id=entity_id,
                proven=False,
                matching_rules=matching_rules,
                supporting_facts={},
                missing_conditions=sorted(list(all_missing_conditions)),
                contradictions=[],
                proof_tree=root_node,
                explanation=explanation,
                sld_result=sld_result,
            )

        # Explicitly disproven
        root_node = BackwardProofNode(
            goal=f"{goal_predicate} = {desired_value}",
            status="DISPROVEN",
            unsatisfied_reasons=all_unsatisfied_reasons,
            missing_conditions=sorted(list(all_missing_conditions)),
            subnodes=rule_subnodes,
        )
        explanation = (
            f"Goal '{goal_predicate} = {desired_value}' is DISPROVEN. "
            f"Premises failed: {'; '.join(all_unsatisfied_reasons)}."
        )
        return BackwardChainingResult(
            target_goal=goal_predicate,
            target_value=desired_value,
            status="DISPROVEN",
            entity_id=entity_id,
            proven=False,
            matching_rules=matching_rules,
            supporting_facts={},
            missing_conditions=sorted(list(all_missing_conditions)),
            contradictions=[],
            proof_tree=root_node,
            explanation=explanation,
            sld_result=sld_result,
        )
