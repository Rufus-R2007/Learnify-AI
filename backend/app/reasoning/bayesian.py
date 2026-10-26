"""
Bayesian Probabilistic Intent Classifier for Learnify AI (Unit IV - Concept 10).
Applies Bayes' Theorem with Laplace Smoothing over a curated educational query corpus
to route ambiguous student questions:
- Calculates genuine prior probabilities from category distributions
- Computes conditional likelihoods with Laplace smoothing (alpha = 1.0)
- Applies Bayes' Theorem to yield normalized posterior probabilities:
    P(Category | Query) = P(Category) * Prod(P(w_i | Category)) / P(Query)
- Explicitly flags uncertain classifications when confidence is ambiguous
- Transparently documents prior, likelihood, and posterior calculation steps
"""

import math
import re
from typing import List, Dict, Tuple, Optional, Any, Set


# Curated labeled training corpus for academic intent classification
CURATED_TRAINING_CORPUS: List[Tuple[str, str]] = [
    # 1. INTENT_REASONING_POLICY (WhatIf Lab, exam eligibility, rules, attendance, exceptions)
    ("Am I eligible under the exam policy?", "INTENT_REASONING_POLICY"),
    ("What if my attendance improves to 78 percent?", "INTENT_REASONING_POLICY"),
    ("Why am I not eligible for the examination?", "INTENT_REASONING_POLICY"),
    ("Can I get an exception with an approved medical certificate?", "INTENT_REASONING_POLICY"),
    ("What are the requirements to sit for exams under the demo policy?", "INTENT_REASONING_POLICY"),
    ("Check my eligibility under the demo rules", "INTENT_REASONING_POLICY"),
    ("What happens if my attendance is 68 percent and assignments completed?", "INTENT_REASONING_POLICY"),
    ("Does medical waiver override the attendance threshold?", "INTENT_REASONING_POLICY"),
    ("Am I qualified for exam under this policy?", "INTENT_REASONING_POLICY"),
    ("Explain why I failed the attendance condition", "INTENT_REASONING_POLICY"),
    ("What if an approved exemption applies to my case?", "INTENT_REASONING_POLICY"),
    ("Simulate my eligibility scenario with 75 percent attendance", "INTENT_REASONING_POLICY"),

    # 2. INTENT_COURSE_INFO (Definitions, syllabus knowledge, AI concepts)
    ("What is artificial intelligence?", "INTENT_COURSE_INFO"),
    ("Define breadth-first search and depth-first search", "INTENT_COURSE_INFO"),
    ("What are intelligent agents and reflex behavior?", "INTENT_COURSE_INFO"),
    ("Explain heuristic search and greedy best first", "INTENT_COURSE_INFO"),
    ("What is predicate logic in artificial intelligence?", "INTENT_COURSE_INFO"),
    ("Explain the difference between forward and backward chaining", "INTENT_COURSE_INFO"),
    ("What is knowledge representation and semantic networks?", "INTENT_COURSE_INFO"),
    ("How does an expert system work?", "INTENT_COURSE_INFO"),
    ("What are neural networks and deep learning?", "INTENT_COURSE_INFO"),
    ("Explain propositional resolution and truth tables", "INTENT_COURSE_INFO"),

    # 3. INTENT_LEARNING_GUIDANCE (PathForge, study planning, prerequisites, timetables)
    ("How should I plan my study schedule this week?", "INTENT_LEARNING_GUIDANCE"),
    ("What prerequisites do I need before learning neural networks?", "INTENT_LEARNING_GUIDANCE"),
    ("Show me the PathForge learning journey for machine learning", "INTENT_LEARNING_GUIDANCE"),
    ("Help me organize my study timetable with constraint satisfaction", "INTENT_LEARNING_GUIDANCE"),
    ("What topics should I study before Bayesian reasoning?", "INTENT_LEARNING_GUIDANCE"),
    ("Create a weekly study plan for artificial intelligence", "INTENT_LEARNING_GUIDANCE"),
    ("Which sequence of topics gives the shortest learning path?", "INTENT_LEARNING_GUIDANCE"),
    ("How to prepare for AI exam step by step?", "INTENT_LEARNING_GUIDANCE"),

    # 4. INTENT_GENERAL (Greetings, capabilities, meta-inquiry)
    ("Hello there, good morning", "INTENT_GENERAL"),
    ("Hi Learnify AI", "INTENT_GENERAL"),
    ("What can you do?", "INTENT_GENERAL"),
    ("Who made this application?", "INTENT_GENERAL"),
    ("Help me get started with this chatbot", "INTENT_GENERAL"),
    ("Greetings assistant", "INTENT_GENERAL"),
]


def tokenize(text: str) -> List[str]:
    """Tokenize query into lowercase alphanumeric words."""
    return re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower())


class BayesianClassificationResult:
    """Documented outcome of Bayesian intent estimation."""

    def __init__(
        self,
        query: str,
        predicted_category: str,
        posterior_probabilities: Dict[str, float],
        prior_probabilities: Dict[str, float],
        log_likelihoods: Dict[str, float],
        is_uncertain: bool,
        smoothing_alpha: float,
        tokens_analyzed: List[str],
        explanation: str,
    ):
        self.query = query
        self.predicted_category = predicted_category
        self.posterior_probabilities = posterior_probabilities
        self.prior_probabilities = prior_probabilities
        self.log_likelihoods = log_likelihoods
        self.is_uncertain = is_uncertain
        self.smoothing_alpha = smoothing_alpha
        self.tokens_analyzed = tokens_analyzed
        self.explanation = explanation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "predicted_category": self.predicted_category,
            "posterior_probabilities": {k: round(v, 4) for k, v in self.posterior_probabilities.items()},
            "prior_probabilities": {k: round(v, 4) for k, v in self.prior_probabilities.items()},
            "is_uncertain": self.is_uncertain,
            "smoothing_alpha": self.smoothing_alpha,
            "tokens": self.tokens_analyzed,
            "explanation": self.explanation,
        }


class NaiveBayesIntentClassifier:
    """
    Multinomial Naive Bayes text classifier with Laplace smoothing.
    Demonstrates probabilistic reasoning using Bayes' Theorem for student query routing.
    """

    def __init__(
        self,
        corpus: Optional[List[Tuple[str, str]]] = None,
        alpha: float = 1.0,
        uncertainty_threshold: float = 0.50,
    ):
        self.corpus = corpus or CURATED_TRAINING_CORPUS
        self.alpha = alpha
        self.uncertainty_threshold = uncertainty_threshold

        self.categories: Set[str] = set()
        self.category_doc_counts: Dict[str, int] = {}
        self.category_word_counts: Dict[str, int] = {}
        self.word_freqs_by_cat: Dict[str, Dict[str, int]] = {}
        self.vocabulary: Set[str] = set()
        self.total_docs: int = 0
        self.priors: Dict[str, float] = {}

        self._train()

    def _train(self) -> None:
        """Calculate word counts, vocabulary, and category priors from corpus."""
        self.total_docs = len(self.corpus)

        for text, cat in self.corpus:
            self.categories.add(cat)
            self.category_doc_counts[cat] = self.category_doc_counts.get(cat, 0) + 1
            tokens = tokenize(text)
            if cat not in self.word_freqs_by_cat:
                self.word_freqs_by_cat[cat] = {}
            for t in tokens:
                self.vocabulary.add(t)
                self.word_freqs_by_cat[cat][t] = self.word_freqs_by_cat[cat].get(t, 0) + 1
                self.category_word_counts[cat] = self.category_word_counts.get(cat, 0) + 1

        # Calculate prior P(Category)
        for cat in self.categories:
            self.priors[cat] = self.category_doc_counts[cat] / float(self.total_docs)

    def classify(self, query: str) -> BayesianClassificationResult:
        """
        Estimate category posterior probability P(C | Query) using Bayes' Rule:
        P(C | w1...wn) proportional to P(C) * Prod_i P(wi | C)
        """
        tokens = tokenize(query)
        vocab_size = len(self.vocabulary)

        log_posteriors: Dict[str, float] = {}
        log_likelihoods: Dict[str, float] = {}

        for cat in self.categories:
            # Prior log P(C)
            prior = self.priors[cat]
            log_prob = math.log(prior)
            log_lik = 0.0

            total_words_in_cat = self.category_word_counts.get(cat, 0)
            denom = total_words_in_cat + self.alpha * vocab_size

            for t in tokens:
                # Laplace smoothing: P(t | C) = (count + alpha) / (total_words + alpha * |V|)
                freq = self.word_freqs_by_cat.get(cat, {}).get(t, 0)
                word_prob = (freq + self.alpha) / float(denom)
                log_prob += math.log(word_prob)
                log_lik += math.log(word_prob)

            log_posteriors[cat] = log_prob
            log_likelihoods[cat] = log_lik

        # Normalization using softmax (log-sum-exp trick to avoid numerical underflow)
        max_log = max(log_posteriors.values())
        exp_posteriors = {c: math.exp(lp - max_log) for c, lp in log_posteriors.items()}
        sum_exp = sum(exp_posteriors.values())
        posteriors = {c: exp_posteriors[c] / sum_exp for c in self.categories}

        best_cat = max(posteriors, key=posteriors.get)
        best_prob = posteriors[best_cat]
        is_uncertain = best_prob < self.uncertainty_threshold

        explanation = (
            f"Bayes' Theorem classified query into '{best_cat}' with posterior P = {best_prob:.3f} "
            f"(Priors: {', '.join(f'{k}: {v:.2f}' for k, v in self.priors.items())}; "
            f"Laplace smoothing alpha = {self.alpha})."
        )
        if is_uncertain:
            explanation += " Probabilistic confidence is below threshold; clarification recommended."

        return BayesianClassificationResult(
            query=query,
            predicted_category=best_cat,
            posterior_probabilities=posteriors,
            prior_probabilities=self.priors,
            log_likelihoods=log_likelihoods,
            is_uncertain=is_uncertain,
            smoothing_alpha=self.alpha,
            tokens_analyzed=tokens,
            explanation=explanation,
        )


# Global singleton classifier instance
bayesian_classifier = NaiveBayesIntentClassifier()
