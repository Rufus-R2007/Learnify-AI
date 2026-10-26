"""
AI Service - Core orchestration service for Learnify AI.
Delegates to the IntelligentAgent pipeline (Phase 1) while providing
an extensible facade for future engines (Phase 2 Search, Phase 3 Rule, Phase 4 Learning).
"""

from typing import List, Dict, Tuple, Optional, Any
from app.services.agent import agent, IntelligentAgent
from app.models.schemas import ChatResponse


class AIService:
    """
    Main AI service facade handling intelligent student queries.
    Phase 1: Integrates the Unit I Intelligent Agent with SQLite Knowledge Base and ProofLens.
    Phase 2: Will integrate SearchEngine & PathForge graph search.
    Phase 3: Will integrate RuleEngine & WhatIf Lab logical inference.
    Phase 4: Will integrate LearningEngine & intent evaluation.
    """

    def __init__(self):
        self.agent: IntelligentAgent = agent

    def process_query_full(self, query: str, context: Optional[List[Dict[str, Any]]] = None) -> ChatResponse:
        """
        Execute full intelligent pipeline returning typed ChatResponse with ProofLens trace.
        """
        return self.agent.process(query, context)

    def process_query(self, query: str, context: Optional[List[Dict[str, Any]]] = None) -> Tuple[str, List[str], Optional[float]]:
        """
        Backward-compatible method returning (response_text, concepts_used, match_score).
        """
        result = self.process_query_full(query, context)
        return (result.response, result.conceptsUsed, result.matchScore)


# Singleton instance
ai_service = AIService()
