"""
FastAPI Router for Symbolic Reasoning & Logic Engine (Phase 3 - Hiran Antony).
Provides endpoints for:
- Listing and inspecting declarative policies and production rules
- Data-driven forward chaining scenario evaluation with ProofLens traces
- Goal-driven backward chaining and SLD-resolution proofs
- Propositional resolution consistency checking
- Bayesian intent estimation
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.models.schemas import (
    EvaluateScenarioRequest,
    ProveGoalRequest,
    ConsistencyCheckRequest,
    IntentClassificationRequest,
)
from app.services.reasoning_service import reasoning_service
from app.database import (
    get_all_policies,
    get_policy_by_id,
    get_all_rules,
    get_rules_for_policy,
)

router = APIRouter()


@router.get("/policies")
async def list_policies():
    """List all available academic policies with declarative rules."""
    policies = get_all_policies()
    return {
        "total": len(policies),
        "policies": policies,
    }


@router.get("/policies/{policy_id}")
async def get_policy(policy_id: str):
    """Retrieve full specification of a single academic policy and its rules."""
    policy = get_policy_by_id(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail=f"Policy '{policy_id}' not found.")
    return policy


@router.get("/rules")
async def list_rules(policy_id: Optional[str] = Query(None, description="Optional policy filter")):
    """List declarative rules, optionally filtered by policy ID."""
    if policy_id:
        rules = get_rules_for_policy(policy_id)
    else:
        rules = get_all_rules()
    return {
        "total": len(rules),
        "rules": rules,
    }


@router.post("/evaluate")
async def evaluate_scenario(req: EvaluateScenarioRequest):
    """
    Evaluate scenario inputs against a named policy using forward chaining.
    Returns derived conclusions, satisfied/missing conditions, and measured ProofLens trace.
    """
    try:
        result, traces = reasoning_service.evaluate_scenario(
            policy_id=req.policy_id,
            scenario_facts=req.scenario_facts,
            entity_id=req.entity_id,
            target_predicate=req.target_predicate,
        )
        return {
            "result": result.to_dict(),
            "trace": [t.model_dump() for t in traces],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reasoning evaluation failed: {str(e)}")


@router.post("/prove")
async def prove_goal(req: ProveGoalRequest):
    """
    Diagnose or prove a target goal using backward chaining and SLD resolution.
    Returns status (PROVEN, DISPROVEN, UNKNOWN, CONFLICT) and proof tree.
    """
    try:
        result, traces = reasoning_service.prove_goal(
            policy_id=req.policy_id,
            goal_predicate=req.goal,
            desired_value=req.desired_value,
            entity_id=req.entity_id,
            scenario_facts=req.scenario_facts,
        )
        return {
            "proof": result.to_dict(),
            "trace": [t.model_dump() for t in traces],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Goal diagnosis failed: {str(e)}")


@router.post("/consistency")
async def check_consistency(req: ConsistencyCheckRequest):
    """
    Validate policy logical consistency using propositional resolution.
    Detects contradictions (derivation of empty clause) or proves satisfiability.
    """
    try:
        report = reasoning_service.check_policy_consistency(req.policy_id)
        return report.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Consistency check failed: {str(e)}")


@router.post("/classify-intent")
async def classify_intent(req: IntentClassificationRequest):
    """
    Classify a student query into academic intent categories using Bayes' Theorem
    with Laplace smoothing.
    """
    try:
        result = reasoning_service.classify_intent(req.query)
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bayesian classification failed: {str(e)}")
