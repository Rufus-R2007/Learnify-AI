"""
Reasoning Service Orchestrator for Learnify AI (Phase 3 - Hiran Antony).
Implements the core RuleEngine and KnowledgeEngine interfaces:
- Loads declarative policies and verified student facts from SQLite
- Executes forward chaining deduction and backward diagnostic goal proving
- Generates genuine, measured ProofLens TraceStep events for transparent inspection
- Validates policy consistency via propositional resolution
- Routes queries using Naive Bayes probabilistic intent estimation
"""

import time
import json
from typing import List, Dict, Any, Optional, Tuple
from app.core.interfaces import RuleEngine, KnowledgeEngine
from app.models.schemas import TraceStep, StepStatus, ExecutionType
from app.database import (
    get_all_policies,
    get_policy_by_id,
    get_rules_for_policy,
    get_verified_facts_for_entity,
)
from app.reasoning.predicates import Predicate, Constant, Variable, parse_predicate
from app.reasoning.facts import Fact, FactBase, VerificationStatus
from app.reasoning.rules import (
    Rule,
    Policy,
    RuleCondition,
    RuleConclusion,
    ConditionOperator,
)
from app.reasoning.forward_chaining import ForwardChainingEngine, ForwardChainingResult
from app.reasoning.backward_chaining import BackwardChainingEngine, BackwardChainingResult
from app.reasoning.exceptions import NonmonotonicEngine, RevisionReport
from app.reasoning.propositional_resolution import (
    Clause,
    Literal,
    check_consistency,
    ConsistencyReport,
)
from app.reasoning.horn_resolution import HornResolutionEngine, SLDProofResult
from app.reasoning.bayesian import (
    bayesian_classifier,
    BayesianClassificationResult,
)


class ReasoningService(RuleEngine, KnowledgeEngine):
    """
    Unified academic reasoning service combining First-Order Logic,
    Production Rules, and Bayesian Intent classification.
    """

    def __init__(self):
        pass

    # =====================================================================
    # Policy and Fact Loading
    # =====================================================================

    def load_policy(self, policy_id: str) -> Policy:
        """Construct a Policy domain object with typed Rules from SQLite."""
        raw = get_policy_by_id(policy_id)
        if not raw:
            raise ValueError(f"Policy with ID '{policy_id}' not found.")

        rules: List[Rule] = []
        for r in raw.get("rules", []):
            conditions: List[RuleCondition] = []
            for c in r.get("conditions", []):
                conditions.append(RuleCondition(
                    predicate=c["predicate"],
                    operator=ConditionOperator(c["operator"]),
                    expected_value=c["expected_value"],
                    description=c.get("description"),
                ))
            conc_data = r["conclusion"]
            conclusion = RuleConclusion(
                predicate=conc_data["predicate"],
                value=conc_data["value"],
                description=conc_data.get("description"),
            )
            rules.append(Rule(
                id=r["id"],
                name=r["name"],
                description=r["description"],
                policy_id=policy_id,
                conditions=conditions,
                conclusion=conclusion,
                priority=r.get("priority", 10),
                is_exception=r.get("is_exception", False),
                overrides_rule_id=r.get("overrides_rule_id"),
                source_id=r.get("source_id", "src-demo"),
            ))

        return Policy(
            id=raw["id"],
            name=raw["name"],
            description=raw["description"],
            rules=rules,
            default_decision=raw.get("default_decision", "INELIGIBLE"),
            version=raw.get("version", "1.0.0"),
            is_illustrative=raw.get("is_illustrative", True),
            disclaimer=raw.get("disclaimer", "Illustrative academic policy for demonstration."),
        )

    def load_factbase(self, entity_id: str = "student_01") -> FactBase:
        """Load verified authoritative facts for an entity from SQLite."""
        raw_facts = get_verified_facts_for_entity(entity_id)
        fact_base = FactBase()
        for f in raw_facts:
            fact_base.add_fact(Fact(
                id=f["id"],
                predicate=f["predicate"],
                entity_id=f["entity_id"],
                value=f["value"],
                arguments=f.get("arguments", [entity_id]),
                source_id=f.get("source_id", "src-demo"),
                verification_status=VerificationStatus(f.get("verification_status", "VERIFIED")),
                policy_id=f.get("policy_id"),
                context=f.get("context"),
                created_at=f.get("created_at"),
            ))
        return fact_base

    # =====================================================================
    # Forward Chaining & Evaluation with ProofLens Tracing
    # =====================================================================

    def evaluate_scenario(
        self,
        policy_id: str,
        scenario_facts: Dict[str, Any],
        entity_id: str = "student_01",
        target_predicate: str = "eligible",
    ) -> Tuple[ForwardChainingResult, List[TraceStep]]:
        """
        Evaluate scenario facts against a named policy using data-driven forward chaining.
        Returns the inference result alongside authentic, measured ProofLens trace events.
        """
        traces: List[TraceStep] = []
        step_id = 1

        # STAGE 1: Scenario Ingestion
        t0 = time.perf_counter()
        policy = self.load_policy(policy_id)
        base_factbase = self.load_factbase(entity_id)
        duration_1 = (time.perf_counter() - t0) * 1000.0

        traces.append(TraceStep(
            id=f"step-{step_id}",
            stage="Scenario Ingestion",
            method="Policy & Fact Isolation",
            description=f"Retrieved verified baseline facts for '{entity_id}' and isolated hypothetical scenario inputs.",
            status=StepStatus.COMPLETED,
            input_summary=f"Policy: '{policy_id}', Inputs: {scenario_facts}",
            output_summary=f"Loaded {len(base_factbase.facts)} verified baseline record(s).",
            evidence_ids=[f.id for f in base_factbase.facts[:3]],
            duration_ms=round(duration_1, 3),
            execution_type=ExecutionType.MODEL_BASED,
        ))
        step_id += 1

        # STAGE 2: Working Memory Formulation
        t0 = time.perf_counter()
        forked_factbase = base_factbase.fork_scenario(scenario_facts, entity_id, policy_id)
        active_facts_summary = {f.predicate: f.value for f in forked_factbase.find_facts(entity_id=entity_id)}
        duration_2 = (time.perf_counter() - t0) * 1000.0

        traces.append(TraceStep(
            id=f"step-{step_id}",
            stage="Working Memory Formulation",
            method="Hypothetical Forking",
            description="Merged baseline records with user scenario inputs into transient working memory.",
            status=StepStatus.COMPLETED,
            input_summary=f"Entity: '{entity_id}', Overrides: {list(scenario_facts.keys())}",
            output_summary=f"Active working memory established with {len(active_facts_summary)} predicates.",
            evidence_ids=["src-whatif-simulator"],
            duration_ms=round(duration_2, 3),
            execution_type=ExecutionType.MODEL_BASED,
        ))
        step_id += 1

        # STAGE 3: Forward Chaining Inference
        t0 = time.perf_counter()
        forward_engine = ForwardChainingEngine(policy)
        result = forward_engine.run(forked_factbase, entity_id, target_predicate)
        duration_3 = (time.perf_counter() - t0) * 1000.0

        traces.append(TraceStep(
            id=f"step-{step_id}",
            stage="Rule Matching & Deduction",
            method="Data-Driven Forward Chaining",
            description=f"Iteratively evaluated {len(policy.rules)} declarative rule(s) until deductive fixed point.",
            status=StepStatus.COMPLETED,
            input_summary=f"Rules tested: {len(policy.rules)}, Working facts: {len(active_facts_summary)}",
            output_summary=f"Fired {len(result.activated_rules)} rule(s); Derived {len(result.derived_facts)} conclusion(s).",
            evidence_ids=[r.id for r in result.activated_rules],
            duration_ms=round(duration_3, 3),
            execution_type=ExecutionType.GOAL_BASED,
        ))
        step_id += 1

        # STAGE 4: Defeasible Conflict & Exception Resolution
        t0 = time.perf_counter()
        if result.overridden_rules:
            overridden_names = ", ".join(r.name for r in result.overridden_rules)
            traces.append(TraceStep(
                id=f"step-{step_id}",
                stage="Exception Resolution",
                method="Nonmonotonic Precedence Evaluation",
                description=f"Exception rules successfully superseded default rules: {overridden_names}.",
                status=StepStatus.COMPLETED,
                input_summary=f"Overridden: {[r.id for r in result.overridden_rules]}",
                output_summary="Defeasible override applied; conclusions revised.",
                evidence_ids=[r.id for r in result.overridden_rules],
                duration_ms=round((time.perf_counter() - t0) * 1000.0, 3),
                execution_type=ExecutionType.VERIFICATION,
            ))
            step_id += 1

        # STAGE 5: Decision Synthesis
        t0 = time.perf_counter()
        duration_5 = (time.perf_counter() - t0) * 1000.0
        traces.append(TraceStep(
            id=f"step-{step_id}",
            stage="Decision Synthesis",
            method="Ground Truth Policy Mapping",
            description=f"Synthesized final outcome: '{result.final_decision}' ({result.decision_status}).",
            status=StepStatus.COMPLETED,
            input_summary=f"Target: '{target_predicate}'",
            output_summary=result.explanation,
            evidence_ids=["src-demo"],
            duration_ms=round(duration_5, 3),
            execution_type=ExecutionType.ASSEMBLY,
        ))

        return result, traces

    # =====================================================================
    # Backward Chaining & Diagnostic Goal Proving
    # =====================================================================

    def prove_goal(
        self,
        policy_id: str,
        goal_predicate: str,
        desired_value: Any = True,
        entity_id: str = "student_01",
        scenario_facts: Optional[Dict[str, Any]] = None,
    ) -> Tuple[BackwardChainingResult, List[TraceStep]]:
        """
        Prove a target goal using goal-driven backward chaining and SLD resolution.
        """
        traces: List[TraceStep] = []
        step_id = 1

        t0 = time.perf_counter()
        policy = self.load_policy(policy_id)
        base_factbase = self.load_factbase(entity_id)
        if scenario_facts:
            fact_base = base_factbase.fork_scenario(scenario_facts, entity_id, policy_id)
        else:
            fact_base = base_factbase

        traces.append(TraceStep(
            id=f"step-{step_id}",
            stage="Goal Initialization",
            method="Goal-Driven Diagnostic Setup",
            description=f"Initialized target goal '{goal_predicate} = {desired_value}' for entity '{entity_id}'.",
            status=StepStatus.COMPLETED,
            input_summary=f"Goal: '{goal_predicate} = {desired_value}'",
            output_summary=f"Target verified against policy '{policy.name}'.",
            evidence_ids=["src-demo"],
            duration_ms=round((time.perf_counter() - t0) * 1000.0, 3),
            execution_type=ExecutionType.GOAL_BASED,
        ))
        step_id += 1

        t0 = time.perf_counter()
        backward_engine = BackwardChainingEngine(policy)
        result = backward_engine.diagnose_goal(fact_base, entity_id, goal_predicate, desired_value)
        duration_diag = (time.perf_counter() - t0) * 1000.0

        traces.append(TraceStep(
            id=f"step-{step_id}",
            stage="Backward Chaining Verification",
            method="Recursive Subgoal Decomposition",
            description=f"Checked candidate rules and premises. Outcome: {result.status}.",
            status=StepStatus.COMPLETED if result.proven else StepStatus.FALLBACK,
            input_summary=f"Matching rules investigated: {len(result.matching_rules)}",
            output_summary=f"Result: {result.status}. Missing: {len(result.missing_conditions)}.",
            evidence_ids=[r.id for r in result.matching_rules],
            duration_ms=round(duration_diag, 3),
            execution_type=ExecutionType.VERIFICATION,
        ))

        return result, traces

    # =====================================================================
    # Propositional Resolution Consistency
    # =====================================================================

    def check_policy_consistency(self, policy_id: str) -> ConsistencyReport:
        """
        Convert policy rules into propositional clauses and apply resolution
        to prove logical consistency or detect formal contradictions.
        """
        policy = self.load_policy(policy_id)
        clauses: List[Clause] = []

        # Represent rules as clauses: (C1 & C2 -> Conc) <=> (~C1 | ~C2 | Conc)
        for r in policy.rules:
            lits: List[Literal] = []
            for cond in r.conditions:
                # ~cond
                lits.append(Literal(cond.predicate, negated=True))
            lits.append(Literal(r.conclusion.predicate, negated=False))
            clauses.append(Clause(lits))

        # Add illustrative mutual exclusivity constraint if rules define contrary outcomes
        clauses.append(Clause([
            Literal("eligible", negated=True),
            Literal("ineligible", negated=True),
        ]))

        return check_consistency(clauses)

    # =====================================================================
    # Bayesian Intent Classification
    # =====================================================================

    def classify_intent(self, query: str) -> BayesianClassificationResult:
        """Estimate query intent category using Bayes' Theorem with Laplace smoothing."""
        return bayesian_classifier.classify(query)

    # =====================================================================
    # RuleEngine & KnowledgeEngine Extension Interface Implementations
    # =====================================================================

    def forward_chain(self, facts: List[str]) -> List[str]:
        """Core RuleEngine interface implementation."""
        policy = self.load_policy("policy-exam-eligibility-v1")
        fact_base = FactBase()
        for f in facts:
            fact_base.add_fact(Fact(
                id=f"input-{f}",
                predicate=f,
                entity_id="student_01",
                value=True,
                source_id="src-api",
            ))
        engine = ForwardChainingEngine(policy)
        result = engine.run(fact_base, "student_01")
        return [f"{k}={v}" for k, v in result.derived_facts.items()]

    def backward_chain(self, goal: str, facts: List[str]) -> Dict[str, Any]:
        """Core RuleEngine interface implementation."""
        policy = self.load_policy("policy-exam-eligibility-v1")
        fact_base = FactBase()
        for f in facts:
            fact_base.add_fact(Fact(
                id=f"input-{f}",
                predicate=f,
                entity_id="student_01",
                value=True,
                source_id="src-api",
            ))
        engine = BackwardChainingEngine(policy)
        result = engine.diagnose_goal(fact_base, "student_01", goal, desired_value=True)
        return result.to_dict()

    def query_semantic_network(self, entity: str, relation: str) -> List[str]:
        """Core KnowledgeEngine interface implementation."""
        # Query verified facts or topic relationships matching relation
        fact_base = self.load_factbase(entity)
        matches = fact_base.find_facts(predicate=relation, entity_id=entity)
        return [str(m.value) for m in matches]

    def evaluate_predicate(self, predicate: str, arguments: List[str]) -> bool:
        """Core KnowledgeEngine interface implementation."""
        fact_base = self.load_factbase(arguments[0] if arguments else "student_01")
        matches = fact_base.find_facts(predicate=predicate)
        return len(matches) > 0


# Global singleton instance
reasoning_service = ReasoningService()
