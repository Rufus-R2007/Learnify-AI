"""
Nonmonotonic Reasoning and Exception Handling for Learnify AI (Unit IV - Concept 9).
Implements belief revision and defeasible reasoning over academic rules:
- General default rules overridden by specific approved exceptions
- Clean conclusion re-evaluation preventing contradictory conclusion appending
- Transparent tracking of overridden rules, defeated conclusions, and justifications
- Pure in-memory scenario isolation preserving authoritative database records
"""

from typing import List, Dict, Any, Optional, Tuple
from app.reasoning.facts import Fact, FactBase
from app.reasoning.rules import Rule, Policy
from app.reasoning.forward_chaining import ForwardChainingEngine, ForwardChainingResult


class OverrideRecord:
    """Record of an explicit rule defeat or nonmonotonic conclusion override."""

    def __init__(
        self,
        overridden_rule: Rule,
        exception_rule: Rule,
        defeated_conclusion: Dict[str, Any],
        superseding_conclusion: Dict[str, Any],
        justification: str,
    ):
        self.overridden_rule = overridden_rule
        self.exception_rule = exception_rule
        self.defeated_conclusion = defeated_conclusion
        self.superseding_conclusion = superseding_conclusion
        self.justification = justification

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overridden_rule_id": self.overridden_rule.id,
            "overridden_rule_name": self.overridden_rule.name,
            "exception_rule_id": self.exception_rule.id,
            "exception_rule_name": self.exception_rule.name,
            "defeated_conclusion": self.defeated_conclusion,
            "superseding_conclusion": self.superseding_conclusion,
            "justification": self.justification,
        }


class RevisionReport:
    """Diagnostic report comparing baseline scenario against exception-revised scenario."""

    def __init__(
        self,
        original_result: ForwardChainingResult,
        revised_result: ForwardChainingResult,
        overrides: List[OverrideRecord],
        conclusion_changed: bool,
        explanation: str,
    ):
        self.original_result = original_result
        self.revised_result = revised_result
        self.overrides = overrides
        self.conclusion_changed = conclusion_changed
        self.explanation = explanation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_outcome": {
                "decision": self.original_result.final_decision,
                "status": self.original_result.decision_status,
                "active_rules": [r.id for r in self.original_result.activated_rules],
            },
            "revised_outcome": {
                "decision": self.revised_result.final_decision,
                "status": self.revised_result.decision_status,
                "active_rules": [r.id for r in self.revised_result.activated_rules],
            },
            "conclusion_changed": self.conclusion_changed,
            "overrides": [o.to_dict() for o in self.overrides],
            "explanation": self.explanation,
        }


class NonmonotonicEngine:
    """
    Manages nonmonotonic rule overrides and belief revision for WhatIf scenarios.
    """

    def __init__(self, policy: Policy):
        self.policy = policy

    def evaluate_revision(
        self,
        baseline_factbase: FactBase,
        revised_inputs: Dict[str, Any],
        entity_id: str,
        target_predicate: str = "eligible",
    ) -> RevisionReport:
        """
        Evaluate baseline scenario, apply revised hypothetical inputs in an isolated fork,
        recompute outcomes, and document exact defeasible overrides.
        """
        engine = ForwardChainingEngine(self.policy)

        # Baseline evaluation
        orig_fork = baseline_factbase.fork_scenario({}, entity_id, self.policy.id)
        orig_res = engine.run(orig_fork, entity_id, target_predicate)

        # Revised evaluation
        rev_fork = baseline_factbase.fork_scenario(revised_inputs, entity_id, self.policy.id)
        rev_res = engine.run(rev_fork, entity_id, target_predicate)

        # Detect overrides
        overrides: List[OverrideRecord] = []
        for exc_rule in rev_res.activated_rules:
            if exc_rule.is_exception and exc_rule.overrides_rule_id:
                overridden = self.policy.get_rule_by_id(exc_rule.overrides_rule_id)
                if overridden:
                    # Find what conclusion was defeated
                    defeated = {overridden.conclusion.predicate: overridden.conclusion.value}
                    superseding = {exc_rule.conclusion.predicate: exc_rule.conclusion.value}
                    justification = (
                        f"Exception rule '{exc_rule.name}' ({exc_rule.id}) with priority {exc_rule.priority} "
                        f"superseded default rule '{overridden.name}' ({overridden.id}) because exception conditions were satisfied."
                    )
                    overrides.append(OverrideRecord(
                        overridden_rule=overridden,
                        exception_rule=exc_rule,
                        defeated_conclusion=defeated,
                        superseding_conclusion=superseding,
                        justification=justification,
                    ))

        conclusion_changed = orig_res.final_decision != rev_res.final_decision

        if overrides:
            override_names = ", ".join(f"'{o.overridden_rule.name}' by '{o.exception_rule.name}'" for o in overrides)
            explanation = (
                f"Nonmonotonic belief revision occurred: {override_names}. "
                f"Previous outcome '{orig_res.final_decision}' ({orig_res.decision_status}) "
                f"revised to '{rev_res.final_decision}' ({rev_res.decision_status})."
            )
        elif conclusion_changed:
            explanation = (
                f"Decision changed from '{orig_res.final_decision}' to '{rev_res.final_decision}' "
                f"due to updated scenario facts without triggering an exception rule."
            )
        else:
            explanation = (
                f"Decision remained '{rev_res.final_decision}' ({rev_res.decision_status}) "
                f"after incorporating updated scenario inputs."
            )

        return RevisionReport(
            original_result=orig_res,
            revised_result=rev_res,
            overrides=overrides,
            conclusion_changed=conclusion_changed,
            explanation=explanation,
        )
