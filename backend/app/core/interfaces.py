"""
Extension interfaces for future project phases of Learnify AI.
Defines clean abstract base classes for:
- SearchEngine (Phase 2 - Yogith Joy J: Graph Search, A*, Prerequisite Navigation, PathForge)
- KnowledgeEngine (Phase 3 - Hiran Antony: Semantic Networks, Logic, Propositional & First-Order)
- RuleEngine (Phase 3 - Hiran Antony: Forward/Backward Chaining, Production Rules, WhatIf Lab)
- LearningEngine (Phase 4 - Naveen Kumar: ML Classification, Evaluation, Adaptive Intent)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class SearchEngine(ABC):
    """
    Interface for Phase 2 (Yogith Joy J).
    Responsible for graph search over knowledge topics, prerequisite route finding,
    and state-space planning for PathForge.
    """

    @abstractmethod
    def find_path(self, start_topic_id: str, goal_topic_id: str, algorithm: str = "bfs") -> List[Dict[str, Any]]:
        """
        Compute an optimal or heuristic learning sequence from start to goal topic.
        
        Args:
            start_topic_id: Current student knowledge state
            goal_topic_id: Target learning goal
            algorithm: 'bfs', 'dfs', 'a_star', or 'iddfs'
            
        Returns:
            List of topic nodes representing the ordered study path.
        """
        pass

    @abstractmethod
    def get_prerequisites(self, topic_id: str) -> List[str]:
        """Return the directed prerequisite chain for a given topic."""
        pass


class KnowledgeEngine(ABC):
    """
    Interface for Phase 3 (Hiran Antony).
    Responsible for structured knowledge representations, semantic networks,
    frames, and first-order predicate logic propositions.
    """

    @abstractmethod
    def query_semantic_network(self, entity: str, relation: str) -> List[str]:
        """Traverse semantic relationships (is-a, part-of, requires)."""
        pass

    @abstractmethod
    def evaluate_predicate(self, predicate: str, arguments: List[str]) -> bool:
        """Evaluate a first-order logic predicate against the knowledge base."""
        pass


class RuleEngine(ABC):
    """
    Interface for Phase 3 (Hiran Antony).
    Responsible for rule-based inference (forward and backward chaining)
    for the WhatIf Lab academic scenario analyzer.
    """

    @abstractmethod
    def forward_chain(self, facts: List[str]) -> List[str]:
        """
        Apply forward chaining to infer new derived facts from initial conditions.
        """
        pass

    @abstractmethod
    def backward_chain(self, goal: str, facts: List[str]) -> Dict[str, Any]:
        """
        Verify whether a goal can be proven given facts and production rules.
        """
        pass


class LearningEngine(ABC):
    """
    Interface for Phase 4 (Naveen Kumar).
    Responsible for learned intent classification, similarity embeddings,
    and evaluation benchmarks.
    """

    @abstractmethod
    def classify_intent(self, text: str) -> Dict[str, float]:
        """Return probability distribution over candidate intents."""
        pass

    @abstractmethod
    def compute_similarity(self, query: str, document: str) -> float:
        """Compute statistical or semantic similarity score between query and document."""
        pass
