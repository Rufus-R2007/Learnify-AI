"""
FastAPI Router for WhatIf Lab Academic Decision Simulator (Phase 3 - Hiran Antony).
Provides endpoints for:
- Retrieving policies with baseline simulation presets
- Evaluating interactive WhatIf scenarios
- Performing counterfactual scenario comparisons (before vs after adjustments)
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.models.schemas import EvaluateScenarioRequest, WhatIfCompareRequest
from app.services.whatif_service import whatif_service

router = APIRouter()


@router.get("/policies")
async def get_whatif_policies():
    """Retrieve policies configured with interactive simulation presets for WhatIf Lab."""
    policies = whatif_service.get_policies()
    return {
        "total": len(policies),
        "policies": policies,
    }


@router.post("/evaluate")
async def evaluate_whatif_scenario(req: EvaluateScenarioRequest):
    """
    Evaluate an interactive student scenario in the WhatIf simulator.
    Returns decision status, satisfied conditions, activated rules, and ProofLens trace.
    """
    try:
        return whatif_service.evaluate_scenario(
            policy_id=req.policy_id,
            scenario_facts=req.scenario_facts,
            entity_id=req.entity_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation evaluation failed: {str(e)}")


@router.post("/compare")
async def compare_whatif_scenarios(req: WhatIfCompareRequest):
    """
    Compute exact counterfactual differences between baseline and modified scenarios:
    - What input facts changed
    - How the decision outcome shifted
    - Rule activation deltas (newly fired, deactivated, overridden)
    - Synthesized explanation
    """
    try:
        return whatif_service.compare_scenarios(
            policy_id=req.policy_id,
            baseline_facts=req.baseline_facts,
            modified_facts=req.modified_facts,
            entity_id=req.entity_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scenario comparison failed: {str(e)}")
