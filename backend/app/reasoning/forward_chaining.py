"""
Forward Chaining Data-Driven Inference Engine for Learnify AI (Unit IV - Concept 7).
Implements forward chaining deduction:
- Matches initial fact state against declarative rule prerequisites
- Iteratively fires active rules and records newly derived conclusions
- Prevents duplicate activations and guarantees safe termination at a fixed point
- Integrates nonmonotonic exception overrides and priority resolution
- Explicitly distinguishes unknown/missing information from false conclusions
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from app.reasoning.facts import Fact, FactBase, VerificationStatus
from app.reasoning.rules import Rule, Policy, RuleCondition, ConditionOperator


class ForwardStep:
    """Record of an activated rule firing during forward inference."""

    def __init__(
        self,
        step_id: int,
        rule_id: str,
        rule_name: str,
        matched_facts: Dict[str, Any],
        derived_predicate: str,
        derived_value: Any,
        is_exception: bool,
        overridden_rule_id: Optional[str] = None,
    ):
        self.step_id = step_id
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.matched_facts = matched_facts
        self.derived_predicate = derived_predicate
        self.derived_value = derived_value
        self.is_exception = is_exception
        self.overridden_rule_id = overridden_rule_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step_id,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "matched_facts": self.matched_facts,
            "derived_conclusion": {self.derived_predicate: self.derived_value},
            "is_exception": self.is_exception,
            "overridden_rule_id": self.overridden_rule_id,
        }


class ForwardChainingResult:
    """Complete evaluation report of forward-chaining inference over a scenario."""

    def __init__(
        self,
        policy_id: str,
        entity_id: str,
        final_decision: Any,
        decision_status: str,
        initial_facts: Dict[str, Any],
        derived_facts: Dict[str, Any],
        activated_rules: List[Rule],
        overridden_rules: List[Rule],
        satisfied_conditions: List[Dict[str, Any]],
        unsatisfied_conditions: List[Dict[str, Any]],
        missing_facts: List[str],
        fired_steps: List[ForwardStep],
        explanation: str,
    ):
        self.policy_id = policy_id
        self.entity_id = entity_id
        self.final_decision = final_decision
        self.decision_status = decision_status
        self.initial_facts = initial_facts
        self.derived_facts = derived_facts
        self.activated_rules = activated_rules
        self.overridden_rules = overridden_rules
        self.satisfied_conditions = satisfied_conditions
        self.unsatisfied_conditions = unsatisfied_conditions
        self.missing_facts = missing_facts
        self.fired_steps = fired_steps
        self.explanation = explanation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "entity_id": self.entity_id,
            "final_decision": self.final_decision,
            "decision_status": self.decision_status,
            "initial_facts": self.initial_facts,
            "derived_facts": self.derived_facts,
            "activated_rules": [r.to_dict() for r in self.activated_rules],
            "overridden_rules": [r.to_dict() for r in self.overridden_rules],
            "satisfied_conditions": self.satisfied_conditions,
            "unsatisfied_conditions": self.unsatisfied_conditions,
            "missing_facts": self.missing_facts,
            "fired_steps": [s.to_dict() for s in self.fired_steps],
            "explanation": self.explanation,
        }


class ForwardChainingEngine:
    """
    Data-driven forward chaining inference engine for academic decision rules.
    """

    def __init__(self, policy: Policy, max_iterations: int = 50):
        self.policy = policy
        self.max_iterations = max_iterations

    def run(
        self,
        fact_base: FactBase,
        entity_id: str,
        target_predicate: str = "eligible",
    ) -> ForwardChainingResult:
        """
        Execute forward chaining from initial facts in fact_base until fixed point.
        Returns detailed ForwardChainingResult with proof provenance.
        """
        # Working memory holds known facts: predicate -> value
        working_memory: Dict[str, Any] = {}
        for f in fact_base.find_facts(entity_id=entity_id):
            working_memory[f.predicate] = f.value

        initial_facts_snapshot = dict(working_memory)
        derived_facts: Dict[str, Any] = {}
        fired_rule_ids: Set[str] = set()
        activated_rules: List[Rule] = []
        overridden_rules: List[Rule] = []
        fired_steps: List[ForwardStep] = []

        all_satisfied_conditions: List[Dict[str, Any]] = []
        all_unsatisfied_conditions: List[Dict[str, Any]] = []
        missing_facts: Set[str] = set()

        step_counter = 1
        iteration = 0

        # Sort rules by priority descending (exceptions and high-priority rules evaluate first)
        sorted_rules = sorted(self.policy.rules, key=lambda r: r.priority, reverse=True)

        while iteration < self.max_iterations:
            iteration += 1
            new_conclusion_derived = False

            for rule in sorted_rules:
                if rule.id in fired_rule_ids:
                    continue

                # Check if this rule is already overridden by a previously fired exception
                if any(r.overrides_rule_id == rule.id for r in activated_rules):
                    if rule not in overridden_rules:
                        overridden_rules.append(rule)
                    continue

                rule_conditions_met = True
                matched_facts_for_rule: Dict[str, Any] = {}

                for cond in rule.conditions:
                    if cond.predicate not in working_memory:
                        missing_facts.add(cond.predicate)
                        rule_conditions_met = False
                        all_unsatisfied_conditions.append({
                            "rule_id": rule.id,
                            "predicate": cond.predicate,
                            "operator": cond.operator.value,
                            "expected": cond.expected_value,
                            "actual": None,
                            "status": "MISSING",
                        })
                        continue

                    actual = working_memory[cond.predicate]
                    if cond.evaluate(actual):
                        matched_facts_for_rule[cond.predicate] = actual
                        all_satisfied_conditions.append({
                            "rule_id": rule.id,
                            "predicate": cond.predicate,
                            "operator": cond.operator.value,
                            "expected": cond.expected_value,
                            "actual": actual,
                            "status": "SATISFIED",
                        })
                    else:
                        rule_conditions_met = False
                        all_unsatisfied_conditions.append({
                            "rule_id": rule.id,
                            "predicate": cond.predicate,
                            "operator": cond.operator.value,
                            "expected": cond.expected_value,
                            "actual": actual,
                            "status": "UNSATISFIED",
                        })

                if rule_conditions_met:
                    # Fire rule!
                    fired_rule_ids.add(rule.id)
                    activated_rules.append(rule)

                    # If this rule overrides a previously fired rule, neutralize previous rule
                    if rule.is_exception and rule.overrides_rule_id:
                        for prev_r in list(activated_rules):
                            if prev_r.id == rule.overrides_rule_id:
                                overridden_rules.append(prev_r)

                    conc_pred = rule.conclusion.predicate
                    conc_val = rule.conclusion.value

                    working_memory[conc_pred] = conc_val
                    derived_facts[conc_pred] = conc_val
                    new_conclusion_derived = True

                    # Add to fact_base as derived fact
                    fact_base.add_fact(Fact(
                        id=f"derived-{conc_pred}-{entity_id}-{step_counter}",
                        predicate=conc_pred,
                        entity_id=entity_id,
                        value=conc_val,
                        source_id=rule.source_id,
                        verification_status=VerificationStatus.VERIFIED,
                        policy_id=self.policy.id,
                        context=f"Derived by rule '{rule.id}' during forward chaining",
                    ))

                    step = ForwardStep(
                        step_id=step_counter,
                        rule_id=rule.id,
                        rule_name=rule.name,
                        matched_facts=matched_facts_for_rule,
                        derived_predicate=conc_pred,
                        derived_value=conc_val,
                        is_exception=rule.is_exception,
                        overridden_rule_id=rule.overrides_rule_id,
                    )
                    fired_steps.append(step)
                    step_counter += 1

            if not new_conclusion_derived:
                # Fixed point reached: working memory closed under deduction
                break

        # Determine final decision on target predicate
        final_decision = working_memory.get(target_predicate, None)

        if final_decision is True:
            decision_status = "SATISFIED"
            if any(r.is_exception for r in activated_rules):
                decision_status = "OVERRIDDEN_BY_EXCEPTION"
            explanation = (
                f"Criteria for '{self.policy.name}' successfully satisfied. "
                f"Derived {len(derived_facts)} conclusion(s) across {len(fired_steps)} rule activation(s)."
            )
        elif final_decision is False:
            decision_status = "UNSATISFIED"
            explanation = (
                f"Criteria for '{self.policy.name}' not satisfied based on evaluated conditions. "
                f"Unsatisfied conditions identified in active rules."
            )
        elif missing_facts:
            decision_status = "INCOMPLETE_INFO"
            explanation = (
                f"Decision cannot be determined definitively. Missing required factual information for: "
                f"{', '.join(sorted(missing_facts))}."
            )
        else:
            decision_status = "UNSATISFIED"
            final_decision = False
            explanation = f"Default policy decision applied: '{self.policy.default_decision}'."

        return ForwardChainingResult(
            policy_id=self.policy.id,
            entity_id=entity_id,
            final_decision=final_decision,
            decision_status=decision_status,
            initial_facts=initial_facts_snapshot,
            derived_facts=derived_facts,
            activated_rules=activated_rules,
            overridden_rules=overridden_rules,
            satisfied_conditions=all_satisfied_conditions,
            unsatisfied_conditions=all_unsatisfied_conditions,
            missing_facts=sorted(list(missing_facts)),
            fired_steps=fired_steps,
            explanation=explanation,
        )
