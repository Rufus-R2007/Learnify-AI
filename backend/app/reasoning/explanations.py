"""
Explainability & Counterfactual What-If Comparison Engine for Learnify AI (Unit IV).
Computes exact differences between original baseline scenarios and modified counterfactuals:
- Pinpoints changed student facts (e.g. attendance 68% -> 78%)
- Analyzes conclusion delta (e.g. Ineligible -> Eligible)
- Compares activated, newly triggered, deactivated, and overridden rules
- Synthesizes clear natural language explanations of why outcomes changed
"""

from typing import List, Dict, Any, Optional
from app.reasoning.forward_chaining import ForwardChainingResult


class WhatIfComparisonReport:
    """Detailed counterfactual comparison between baseline and modified WhatIf scenarios."""

    def __init__(
        self,
        policy_id: str,
        entity_id: str,
        changed_facts: List[Dict[str, Any]],
        previous_decision: Any,
        previous_status: str,
        current_decision: Any,
        current_status: str,
        decision_changed: bool,
        newly_activated_rules: List[Dict[str, Any]],
        deactivated_rules: List[Dict[str, Any]],
        overridden_rules: List[Dict[str, Any]],
        explanation: str,
    ):
        self.policy_id = policy_id
        self.entity_id = entity_id
        self.changed_facts = changed_facts
        self.previous_decision = previous_decision
        self.previous_status = previous_status
        self.current_decision = current_decision
        self.current_status = current_status
        self.decision_changed = decision_changed
        self.newly_activated_rules = newly_activated_rules
        self.deactivated_rules = deactivated_rules
        self.overridden_rules = overridden_rules
        self.explanation = explanation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "entity_id": self.entity_id,
            "changed_facts": self.changed_facts,
            "previous_outcome": {
                "decision": self.previous_decision,
                "status": self.previous_status,
            },
            "current_outcome": {
                "decision": self.current_decision,
                "status": self.current_status,
            },
            "decision_changed": self.decision_changed,
            "newly_activated_rules": self.newly_activated_rules,
            "deactivated_rules": self.deactivated_rules,
            "overridden_rules": self.overridden_rules,
            "explanation": self.explanation,
        }


def compare_scenarios(
    baseline_result: ForwardChainingResult,
    modified_result: ForwardChainingResult,
) -> WhatIfComparisonReport:
    """
    Examine two execution results to discover exactly why the outcome shifted.
    """
    # 1. Determine changed input facts
    all_keys = set(baseline_result.initial_facts.keys()) | set(modified_result.initial_facts.keys())
    changed_facts: List[Dict[str, Any]] = []

    for k in sorted(all_keys):
        v_orig = baseline_result.initial_facts.get(k)
        v_mod = modified_result.initial_facts.get(k)
        if v_orig != v_mod:
            delta_str = ""
            if isinstance(v_orig, (int, float)) and isinstance(v_mod, (int, float)):
                diff = v_mod - v_orig
                delta_str = f" ({'+' if diff > 0 else ''}{diff})"
            changed_facts.append({
                "predicate": k,
                "previous_value": v_orig,
                "modified_value": v_mod,
                "delta": delta_str,
            })

    # 2. Rule activation deltas
    base_active_ids = {r.id: r for r in baseline_result.activated_rules}
    mod_active_ids = {r.id: r for r in modified_result.activated_rules}

    newly_active = [
        {"id": r.id, "name": r.name, "description": r.description}
        for r_id, r in mod_active_ids.items()
        if r_id not in base_active_ids
    ]
    deactivated = [
        {"id": r.id, "name": r.name, "description": r.description}
        for r_id, r in base_active_ids.items()
        if r_id not in mod_active_ids
    ]
    overridden = [
        {"id": r.id, "name": r.name, "overrides": r.overrides_rule_id}
        for r in modified_result.overridden_rules
    ]

    decision_changed = (
        baseline_result.final_decision != modified_result.final_decision
        or baseline_result.decision_status != modified_result.decision_status
    )

    # 3. Synthesize natural language explanation
    explanation_parts: List[str] = []
    if changed_facts:
        fact_diff_descs = [f"'{f['predicate']}' changed from {f['previous_value']} to {f['modified_value']}" for f in changed_facts]
        explanation_parts.append(f"Inputs modified: {', '.join(fact_diff_descs)}.")

    if newly_active:
        explanation_parts.append(f"Newly triggered rule(s): {', '.join(r['name'] for r in newly_active)}.")

    if deactivated:
        explanation_parts.append(f"Deactivated rule(s): {', '.join(r['name'] for r in deactivated)}.")

    if overridden:
        explanation_parts.append(f"Overridden rule(s): {', '.join(r['id'] for r in overridden)}.")

    if decision_changed:
        explanation_parts.append(
            f"Result shifted from {baseline_result.decision_status} (decision: {baseline_result.final_decision}) "
            f"to {modified_result.decision_status} (decision: {modified_result.final_decision})."
        )
    else:
        explanation_parts.append(
            f"Outcome remained {modified_result.decision_status} (decision: {modified_result.final_decision})."
        )

    return WhatIfComparisonReport(
        policy_id=modified_result.policy_id,
        entity_id=modified_result.entity_id,
        changed_facts=changed_facts,
        previous_decision=baseline_result.final_decision,
        previous_status=baseline_result.decision_status,
        current_decision=modified_result.final_decision,
        current_status=modified_result.decision_status,
        decision_changed=decision_changed,
        newly_activated_rules=newly_active,
        deactivated_rules=deactivated,
        overridden_rules=overridden,
        explanation=" ".join(explanation_parts),
    )
