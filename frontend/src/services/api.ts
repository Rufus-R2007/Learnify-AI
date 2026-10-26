import axios from 'axios';
import {
  ChatRequest,
  ChatResponse,
  Message,
  ConceptsResponse,
  KnowledgeListResponse,
  KnowledgeRecord,
  HealthResponse,
  PathForgeTopic,
  PathForgeGraphResponse,
  LearningPlanResponse,
  CompareAlgorithmsResponse,
  StudyScheduleResponse,
  WhatIfPolicy,
  EvaluateWhatIfResponse,
  CompareWhatIfResponse,
  GoalProofResponse,
  ConsistencyCheckResponse,
  DeclarativeRule,
  FeedbackItem,
  FeedbackCreateRequest,
  FeedbackReviewRequest,
  MLMetricsResponse,
  MemoryStatsResponse,
  MemoryItem,
  KnowledgeHistoryItem,
  RelatedCase,
} from '../types';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

/**
 * Send a chat message to the backend API with conversation context.
 */
export const sendMessage = async (
  message: string,
  context: Message[] = []
): Promise<ChatResponse> => {
  try {
    const formattedContext = context
      .slice(-10) // Limit to last 10 messages for context window
      .map((msg) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        conceptsUsed: msg.conceptsUsed,
      }));

    const request: ChatRequest = {
      message,
      context: formattedContext,
    };

    const response = await api.post<ChatResponse>('/api/chat/', request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
        throw new Error(
          'Cannot connect to backend server. Please verify the FastAPI backend is running on http://localhost:8000'
        );
      }
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
    }
    throw new Error('An unexpected network or server error occurred while sending message');
  }
};

/**
 * Get the five-unit AI syllabus tracker.
 */
export const getAIConcepts = async (): Promise<ConceptsResponse> => {
  try {
    const response = await api.get<ConceptsResponse>('/api/chat/concepts');
    return response.data;
  } catch (error) {
    console.error('Error fetching AI concepts:', error);
    throw error;
  }
};

/**
 * Retrieve knowledge records with optional search filter and unit filtering.
 */
export const getKnowledgeList = async (
  search?: string,
  unit?: number
): Promise<KnowledgeListResponse> => {
  try {
    const params: Record<string, string | number> = {};
    if (search) params.search = search;
    if (unit !== undefined) params.unit = unit;

    const response = await api.get<KnowledgeListResponse>('/api/knowledge/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching knowledge records:', error);
    throw error;
  }
};

/**
 * Retrieve a single knowledge record by ID.
 */
export const getKnowledgeRecord = async (id: string): Promise<KnowledgeRecord> => {
  try {
    const response = await api.get<KnowledgeRecord>(`/api/knowledge/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching knowledge record ${id}:`, error);
    throw error;
  }
};

/**
 * Retrieve system FAQs.
 */
export const getFAQs = async (): Promise<Array<{ id: string; question: string; answer: string; category?: string; source_name?: string }>> => {
  try {
    const response = await api.get('/api/knowledge/faqs');
    return response.data.faqs || [];
  } catch (error) {
    console.error('Error fetching FAQs:', error);
    return [];
  }
};

/**
 * Check backend health status.
 */
export const checkHealth = async (): Promise<HealthResponse | { status: string }> => {
  try {
    const response = await api.get<HealthResponse>('/api/health');
    return response.data;
  } catch (error) {
    return { status: 'unavailable' };
  }
};

/**
 * PATHFORGE (PHASE 2) API CLIENT METHODS
 */

/**
 * Fetch all available curriculum topics for PathForge.
 */
export const getPathForgeTopics = async (): Promise<{ total: number; topics: PathForgeTopic[] }> => {
  try {
    const response = await api.get<{ total: number; topics: PathForgeTopic[] }>('/api/pathforge/topics');
    return response.data;
  } catch (error) {
    console.error('Error fetching PathForge topics:', error);
    throw error;
  }
};

/**
 * Fetch the complete curriculum directed knowledge graph for visualization.
 */
export const getPathForgeGraph = async (): Promise<PathForgeGraphResponse> => {
  try {
    const response = await api.get<PathForgeGraphResponse>('/api/pathforge/graph');
    return response.data;
  } catch (error) {
    console.error('Error fetching PathForge graph:', error);
    throw error;
  }
};

/**
 * Plan topological learning journey with prerequisite resolution and search route.
 */
export const planLearningPath = async (
  goalTopicId: string,
  knownTopicIds: string[] = [],
  startTopicId?: string | null,
  algorithm: string = 'bfs'
): Promise<LearningPlanResponse> => {
  try {
    const response = await api.post<LearningPlanResponse>('/api/pathforge/path', {
      goal_topic_id: goalTopicId,
      known_topic_ids: knownTopicIds,
      start_topic_id: startTopicId || undefined,
      algorithm,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to plan learning path');
  }
};

/**
 * Execute and compare BFS, Bidirectional Search, Greedy Best-First, and DFS.
 */
export const compareAlgorithms = async (
  startTopicId: string,
  goalTopicId: string
): Promise<CompareAlgorithmsResponse> => {
  try {
    const response = await api.post<CompareAlgorithmsResponse>('/api/pathforge/compare', {
      start_topic_id: startTopicId,
      goal_topic_id: goalTopicId,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to compare algorithms');
  }
};

/**
 * Generate a study schedule respecting constraints via Backtracking Search.
 */
export const generateStudySchedule = async (params: {
  goalTopicId: string;
  knownTopicIds?: string[];
  availableDays?: string[];
  maxDailyHours?: number;
  preferredSessionHours?: number;
  planningWeeks?: number;
}): Promise<StudyScheduleResponse> => {
  try {
    const response = await api.post<StudyScheduleResponse>('/api/pathforge/schedule', {
      goal_topic_id: params.goalTopicId,
      known_topic_ids: params.knownTopicIds || [],
      available_days: params.availableDays || ['Monday', 'Wednesday', 'Friday'],
      max_daily_hours: params.maxDailyHours || 2,
      preferred_session_hours: params.preferredSessionHours || 1,
      planning_weeks: params.planningWeeks || 2,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to generate study schedule');
  }
};

/**
 * =========================================================================
 * WHATIF LAB & SYMBOLIC REASONING (PHASE 3) API CLIENT METHODS
 * Developer: URK25CS1034 — Hiran Antony
 * =========================================================================
 */

/**
 * Fetch all policies configured with baseline presets for WhatIf Lab.
 */
export const getWhatIfPolicies = async (): Promise<{ total: number; policies: WhatIfPolicy[] }> => {
  try {
    const response = await api.get<{ total: number; policies: WhatIfPolicy[] }>('/api/whatif/policies');
    return response.data;
  } catch (error) {
    console.error('Error fetching WhatIf policies:', error);
    throw error;
  }
};

/**
 * Evaluate an interactive scenario against a declarative policy using forward chaining.
 */
export const evaluateWhatIfScenario = async (
  policyId: string,
  scenarioFacts: Record<string, unknown>,
  entityId: string = 'student_01'
): Promise<EvaluateWhatIfResponse> => {
  try {
    const response = await api.post<EvaluateWhatIfResponse>('/api/whatif/evaluate', {
      policy_id: policyId,
      scenario_facts: scenarioFacts,
      entity_id: entityId,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to evaluate WhatIf scenario');
  }
};

/**
 * Compare baseline and modified scenarios and compute exact counterfactual differences.
 */
export const compareWhatIfScenarios = async (
  policyId: string,
  baselineFacts: Record<string, unknown>,
  modifiedFacts: Record<string, unknown>,
  entityId: string = 'student_01'
): Promise<CompareWhatIfResponse> => {
  try {
    const response = await api.post<CompareWhatIfResponse>('/api/whatif/compare', {
      policy_id: policyId,
      baseline_facts: baselineFacts,
      modified_facts: modifiedFacts,
      entity_id: entityId,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to compare WhatIf scenarios');
  }
};

/**
 * Prove or diagnose a target goal using Backward Chaining and SLD-Resolution.
 */
export const proveReasoningGoal = async (
  policyId: string,
  goalPredicate: string,
  desiredValue: unknown = true,
  entityId: string = 'student_01',
  scenarioFacts?: Record<string, unknown>
): Promise<GoalProofResponse> => {
  try {
    const response = await api.post<GoalProofResponse>('/api/reasoning/prove', {
      policy_id: policyId,
      goal: goalPredicate,
      desired_value: desiredValue,
      entity_id: entityId,
      scenario_facts: scenarioFacts,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to diagnose goal via backward chaining');
  }
};

/**
 * Validate policy consistency using Propositional Resolution.
 */
export const checkPolicyConsistency = async (policyId: string): Promise<ConsistencyCheckResponse> => {
  try {
    const response = await api.post<ConsistencyCheckResponse>('/api/reasoning/consistency', {
      policy_id: policyId,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to check policy consistency');
  }
};

/**
 * Retrieve all declarative rules for a policy.
 */
export const getReasoningRules = async (policyId?: string): Promise<{ total: number; rules: DeclarativeRule[] }> => {
  try {
    const params = policyId ? { policy_id: policyId } : {};
    const response = await api.get<{ total: number; rules: DeclarativeRule[] }>('/api/reasoning/rules', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching reasoning rules:', error);
    throw error;
  }
};

// =========================================================================
// Phase 4: Machine Learning & Learning Engine API Functions
// =========================================================================

/**
 * Concept 2: Submit student feedback with optional suggested correction (Learning by Taking Advice).
 */
export const submitFeedback = async (payload: FeedbackCreateRequest): Promise<FeedbackItem> => {
  try {
    const response = await api.post<FeedbackItem>('/api/learning/feedback/', payload);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to submit feedback');
  }
};

/**
 * Concept 2: Retrieve all feedback submissions (with optional status filter: PENDING, APPROVED, REJECTED).
 */
export const getFeedbackList = async (status?: string): Promise<FeedbackItem[]> => {
  try {
    const params = status ? { status } : {};
    const response = await api.get<FeedbackItem[]>('/api/learning/feedback/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching feedback list:', error);
    throw error;
  }
};

/**
 * Concept 2: Retrieve a single feedback item by ID.
 */
export const getFeedbackById = async (id: string): Promise<FeedbackItem> => {
  try {
    const response = await api.get<FeedbackItem>(`/api/learning/feedback/${id}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error(`Failed to fetch feedback ${id}`);
  }
};

/**
 * Concept 2: Reviewer workflow — approve or reject feedback, optionally updating knowledge base.
 */
export const reviewFeedback = async (
  feedbackId: string,
  payload: FeedbackReviewRequest
): Promise<{ feedback_id: string; status: string; knowledge_updated: boolean; message: string }> => {
  try {
    const response = await api.post(`/api/learning/feedback/${feedbackId}/review`, payload);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to review feedback');
  }
};

/**
 * Concept 2: Retrieve knowledge modification history audit trail.
 */
export const getKnowledgeHistory = async (knowledgeId?: string): Promise<KnowledgeHistoryItem[]> => {
  try {
    const params = knowledgeId ? { knowledge_id: knowledgeId } : {};
    const response = await api.get<KnowledgeHistoryItem[]>('/api/learning/knowledge-history', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching knowledge history:', error);
    throw error;
  }
};

/**
 * Concept 1: Retrieve Rote Learning verified memory cache statistics.
 */
export const getMemoryStats = async (): Promise<MemoryStatsResponse> => {
  try {
    const response = await api.get<MemoryStatsResponse>('/api/learning/memory/stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching memory stats:', error);
    throw error;
  }
};

/**
 * Concept 1: Retrieve cached memory entries for inspection.
 */
export const getMemoryItems = async (limit: number = 50): Promise<MemoryItem[]> => {
  try {
    const response = await api.get<MemoryItem[]>('/api/learning/memory/items', { params: { limit } });
    return response.data;
  } catch (error) {
    console.error('Error fetching memory items:', error);
    throw error;
  }
};

/**
 * Concept 1: Invalidate verified memory entries (cache clearance).
 */
export const invalidateMemory = async (queryPattern?: string): Promise<{ invalidated: number; message: string }> => {
  try {
    const params = queryPattern ? { query_pattern: queryPattern } : {};
    const response = await api.post('/api/learning/memory/invalidate', null, { params });
    return response.data;
  } catch (error) {
    console.error('Error invalidating memory:', error);
    throw error;
  }
};

/**
 * Concept 3: Retrieve Inductive Learning scikit-learn classifier evaluation metrics.
 */
export const getMLMetrics = async (): Promise<MLMetricsResponse> => {
  try {
    const response = await api.get<MLMetricsResponse>('/api/learning/ml-metrics');
    return response.data;
  } catch (error) {
    console.error('Error fetching ML metrics:', error);
    throw error;
  }
};

/**
 * Concept 3: Predict student query intent via ML model.
 */
export const predictIntent = async (
  query: string
): Promise<{
  query: string;
  predicted_category: string;
  confidence: number;
  is_uncertain: boolean;
  class_probabilities: Record<string, number>;
  model_version: string;
}> => {
  try {
    const response = await api.post('/api/learning/predict-intent', { query });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to predict intent');
  }
};

/**
 * Concept 4: Retrieve related solved cases via analogy matching.
 */
export const getCurriculumAnalogies = async (query: string, maxCases: number = 3): Promise<RelatedCase[]> => {
  try {
    const response = await api.get<{ matches: RelatedCase[] }>('/api/learning/analogies', {
      params: { query, max_cases: maxCases },
    });
    return response.data.matches;
  } catch (error) {
    console.error('Error fetching analogies:', error);
    return [];
  }
};

/**
 * Concept 5: Retrieve unified expert system architectural component definitions.
 */
export const getExpertSystemArchitecture = async (): Promise<Record<string, unknown>> => {
  try {
    const response = await api.get('/api/learning/expert-system-architecture');
    return response.data;
  } catch (error) {
    console.error('Error fetching expert system architecture:', error);
    throw error;
  }
};

export default api;
