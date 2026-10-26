"""
Reasoning and Knowledge Representation package for Learnify AI (Phase 3 - Hiran Antony).
Provides:
- First-Order Logic Predicates, Terms, Horn Clauses
- Robinson Unification Algorithm
- Propositional Resolution Consistency Engine
- Horn-Clause SLD Resolution Engine
- Declarative Rules and Named Policies
- Forward Chaining Engine
- Backward Chaining Diagnostic Prover
- Nonmonotonic Exception Reasoning
- Bayesian Probabilistic Intent Classifier
- WhatIf Counterfactual Comparison
"""

from app.reasoning.predicates import (
    Term,
    Constant,
    Variable,
    CompoundTerm,
    Predicate,
    HornClause,
    apply_substitution,
    standardize_apart,
    parse_term,
    parse_predicate,
)
from app.reasoning.unification import (
    unify,
    UnificationResult,
    occurs_check,
)
from app.reasoning.propositional_resolution import (
    Literal,
    Clause,
    ResolutionStep,
    ConsistencyReport,
    resolve_clauses,
    check_consistency,
    parse_clause,
)
from app.reasoning.horn_resolution import (
    HornResolutionEngine,
    SLDStep,
    SLDProofResult,
)
from app.reasoning.facts import (
    Fact,
    FactBase,
    VerificationStatus,
    FactConflict,
)
from app.reasoning.rules import (
    RuleCondition,
    RuleConclusion,
    Rule,
    Policy,
    ConditionOperator,
)
from app.reasoning.forward_chaining import (
    ForwardChainingEngine,
    ForwardChainingResult,
    ForwardStep,
)
from app.reasoning.backward_chaining import (
    BackwardChainingEngine,
    BackwardChainingResult,
    BackwardProofNode,
)
from app.reasoning.exceptions import (
    NonmonotonicEngine,
    RevisionReport,
    OverrideRecord,
)
from app.reasoning.bayesian import (
    NaiveBayesIntentClassifier,
    BayesianClassificationResult,
    bayesian_classifier,
    tokenize,
)
from app.reasoning.explanations import (
    WhatIfComparisonReport,
    compare_scenarios,
)

__all__ = [
    "Term",
    "Constant",
    "Variable",
    "CompoundTerm",
    "Predicate",
    "HornClause",
    "apply_substitution",
    "standardize_apart",
    "parse_term",
    "parse_predicate",
    "unify",
    "UnificationResult",
    "occurs_check",
    "Literal",
    "Clause",
    "ResolutionStep",
    "ConsistencyReport",
    "resolve_clauses",
    "check_consistency",
    "parse_clause",
    "HornResolutionEngine",
    "SLDStep",
    "SLDProofResult",
    "Fact",
    "FactBase",
    "VerificationStatus",
    "FactConflict",
    "RuleCondition",
    "RuleConclusion",
    "Rule",
    "Policy",
    "ConditionOperator",
    "ForwardChainingEngine",
    "ForwardChainingResult",
    "ForwardStep",
    "BackwardChainingEngine",
    "BackwardChainingResult",
    "BackwardProofNode",
    "NonmonotonicEngine",
    "RevisionReport",
    "OverrideRecord",
    "NaiveBayesIntentClassifier",
    "BayesianClassificationResult",
    "bayesian_classifier",
    "tokenize",
    "WhatIfComparisonReport",
    "compare_scenarios",
]
