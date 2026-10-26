"""
Learning by Analogy / Case-Based Reasoning Engine (Phase 4 - Unit V Concept 4).
Developer: URK25CS1016 — Naveen Kumar

Matches incoming student queries against approved solved question cases using
TF-IDF vectors and Cosine Similarity.

Critical Safety Requirement:
Individualized or rule-dependent queries (e.g. attendance percentage, exemptions,
disciplinary clearance) must NOT blindly copy decisions from other students.
The analogy engine flags such queries and routes them to the symbolic reasoning engine.
"""

import re
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.database import get_all_cases, get_case_by_id


class AnalogyEngine:
    """
    Case-Based Reasoning & Learning by Analogy:
    Compares novel student queries to curated past solved cases.
    """

    # Questions containing these patterns require individualized symbolic reasoning
    # rather than analogy copy-paste
    INDIVIDUALIZED_PATTERNS = [
        r'\bmy attendance\b',
        r'\b\d{1,3}\s*%\b',
        r'\b\d{1,3}\s*percent\b',
        r'\bexemption\b',
        r'\bwaiver\b',
        r'\bmy gpa\b',
        r'\bmy marks\b',
        r'\beligible with\b',
        r'\bam i eligible\b',
        r'\bwill i be eligible\b',
        r'\bmedical\b',
    ]

    def __init__(self, min_similarity_threshold: float = 0.15):
        self.min_similarity_threshold = min_similarity_threshold
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._case_vectors = None
        self._cases: List[Dict[str, Any]] = []
        self._refresh_case_base()

    def _refresh_case_base(self) -> None:
        """Load cases from database and fit TF-IDF vectorizer."""
        self._cases = get_all_cases()
        if not self._cases:
            return

        corpus = [
            f"{c['question']} {c.get('keywords', '')} {c.get('solution_preview', '')} {c.get('category', '')}"
            for c in self._cases
        ]

        self._vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True
        )
        self._case_vectors = self._vectorizer.fit_transform(corpus)

    def is_individualized_query(self, query: str) -> bool:
        """
        Safety Guard: Determine if query involves personal or rule-dependent
        variables where analogy copying would be incorrect.
        """
        q_lower = query.lower()
        return any(re.search(pat, q_lower) for pat in self.INDIVIDUALIZED_PATTERNS)

    def find_similar_cases(
        self,
        query: str,
        top_k: int = 3,
        exclude_case_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve top similar solved questions via TF-IDF cosine similarity.
        Enforces safety guard for individualized queries.
        """
        if not self._cases or self._vectorizer is None or self._case_vectors is None:
            self._refresh_case_base()
            if not self._cases:
                return []

        cleaned_query = query.strip()
        if not cleaned_query:
            return []

        is_indiv = self.is_individualized_query(cleaned_query)

        query_vec = self._vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(query_vec, self._case_vectors)[0]

        scored_cases = []
        for idx, score in enumerate(similarities):
            case = self._cases[idx]
            if exclude_case_id and case["id"] == exclude_case_id:
                continue

            sim_score = float(score)
            if sim_score >= self.min_similarity_threshold:
                scored_cases.append({
                    "id": case["id"],
                    "question": case["question"],
                    "solution_preview": case["solution_preview"],
                    "topic_name": case.get("topic_name", "AI Curriculum"),
                    "category": case.get("category", "General"),
                    "unit": case.get("unit", 1),
                    "knowledge_id": case.get("knowledge_id"),
                    "similarity_score": round(sim_score, 4),
                    "is_individualized_warning": is_indiv and case.get("unit") == 4
                })

        # Rank descending by similarity score
        scored_cases.sort(key=lambda c: c["similarity_score"], reverse=True)
        return scored_cases[:top_k]

    def get_analogy_guidance(self, query: str) -> Dict[str, Any]:
        """
        Return structured guidance based on analogous cases.
        """
        is_indiv = self.is_individualized_query(query)
        similar_cases = self.find_similar_cases(query, top_k=3)

        guard_notice = None
        if is_indiv:
            guard_notice = (
                "[Policy Notice] Academic decisions depend on specific numerical "
                "conditions (attendance percentage, assignment submission, approved exemptions). "
                "The analogy system avoids copying individual outcomes; please consult the WhatIf Lab rule simulator."
            )

        return {
            "query": query,
            "has_analogies": len(similar_cases) > 0,
            "is_individualized_query": is_indiv,
            "guard_notice": guard_notice,
            "similar_cases": similar_cases,
            "count": len(similar_cases)
        }


# Global singleton instance
analogy_engine = AnalogyEngine()
