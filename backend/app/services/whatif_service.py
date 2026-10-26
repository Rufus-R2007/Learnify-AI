"""
WhatIf Lab Simulation & Comparison Service for Learnify AI (Phase 3 - Hiran Antony).
Provides the backend core for the WhatIf Academic Decision Simulator:
- Evaluates student scenario configurations against real declarative rules
- Calculates counterfactual differences between baseline and what-if adjustments
- Tracks rule activation deltas and overridden constraints
- Produces explainable decision summaries and ProofLens execution traces
"""

from typing import Dict, Any, List, Optional
from app.services.reasoning_service import reasoning_service
from app.reasoning.explanations import compare_scenarios, WhatIfComparisonReport
from app.database import get_all_policies, get_policy_by_id


# Standard baseline demonstration presets for WhatIf Lab
BASELINE_PRESETS: Dict[str, Dict[str, Any]] = {
    "policy-exam-eligibility-v1": {
        "attendance_percentage": 68,
        "assignment_completed": True,
    },
    "policy-exception-waiver-v1": {
        "attendance_percentage": 68,
        "assignment_completed": True,
        "approved_exemption": False,
    },
    "policy-incomplete-info-v1": {
        "attendance_percentage": 78,
        "assignment_completed": True,
        # Note: lab_clearance deliberately omitted to demonstrate missing info / UNKNOWN
    },
    "policy-academic-honors-v1": {
        "gpa": 3.82,
        "credits_completed": 64,
        "disciplinary_clearance": True,
    },
}


class WhatIfService:
    """
    Service managing WhatIf Lab simulation, baseline presets, and counterfactual comparison.
    """

    def get_policies(self) -> List[Dict[str, Any]]:
        """List all demonstration policies with their rules and baseline presets."""
        policies = get_all_policies()
        for p in policies:
            p["baseline_preset"] = BASELINE_PRESETS.get(p["id"], {})
        return policies

    def evaluate_scenario(
        self,
        policy_id: str,
        scenario_facts: Dict[str, Any],
        entity_id: str = "student_01",
    ) -> Dict[str, Any]:
        """
        Evaluate a scenario configuration and return structured decision report with ProofLens trace.
        """
        result, trace_steps = reasoning_service.evaluate_scenario(
            policy_id=policy_id,
            scenario_facts=scenario_facts,
            entity_id=entity_id,
        )

        return {
            "result": result.to_dict(),
            "trace": [t.model_dump() for t in trace_steps],
            "policy": reasoning_service.load_policy(policy_id).to_dict(),
        }

    def compare_scenarios(
        self,
        policy_id: str,
        baseline_facts: Dict[str, Any],
        modified_facts: Dict[str, Any],
        entity_id: str = "student_01",
    ) -> Dict[str, Any]:
        """
        Compare baseline and modified scenarios, computing exact counterfactual delta:
        - Which input facts changed (e.g. attendance 68% -> 78%)
        - How the decision outcome shifted
        - Which rules were newly activated, deactivated, or overridden
        - Natural language explanation of the change
        """
        res_baseline, trace_base = reasoning_service.evaluate_scenario(
            policy_id=policy_id,
            scenario_facts=baseline_facts,
            entity_id=entity_id,
        )

        res_modified, trace_mod = reasoning_service.evaluate_scenario(
            policy_id=policy_id,
            scenario_facts=modified_facts,
            entity_id=entity_id,
        )

        comparison_report = compare_scenarios(res_baseline, res_modified)

        return {
            "comparison": comparison_report.to_dict(),
            "baseline_result": res_baseline.to_dict(),
            "modified_result": res_modified.to_dict(),
            "baseline_trace": [t.model_dump() for t in trace_base],
            "modified_trace": [t.model_dump() for t in trace_mod],
            "policy": reasoning_service.load_policy(policy_id).to_dict(),
        }


# Global singleton instance
whatif_service = WhatIfService()
