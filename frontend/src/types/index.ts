export type Role = 'user' | 'assistant';

export interface SourceReference {
  id: string;
  name: string;
  description?: string;
  url?: string;
}

export type ExecutionType =
  | 'reflex'
  | 'model_based'
  | 'goal_based'
  | 'retrieval'
  | 'verification'
  | 'assembly'
  | 'fallback'
  | 'search'
  | 'planning'
  | 'csp'
  | 'logical_deduction'
  | 'backward_chaining'
  | 'resolution'
  | 'unification'
  | 'rote_learning'
  | 'inductive_learning'
  | 'analogy'
  | 'expert_system';

export type StepStatus = 'completed' | 'skipped' | 'fallback' | 'failed';

export interface TraceStep {
  id: string;
  stage: string;
  method: string;
  description: string;
  status: StepStatus;
  input_summary?: string;
  output_summary?: string;
  evidence_ids: string[];
  duration_ms: number;
  execution_type: ExecutionType;
}

export interface RelatedCase {
  id: string;
  topic_id: string;
  topic_name: string;
  unit: number;
  category: string;
  question: string;
  solution_preview: string;
  knowledge_id?: string | null;
  similarity: number;
}

export interface Message {
  id: string;
  role: Role;
  content: string;
  timestamp: Date;
  conceptsUsed?: string[];
  confidence?: number | null;
  matchScore?: number | null;
  sources?: SourceReference[];
  trace?: TraceStep[];
  status?: string;
  suggestions?: string[];
  missingInfo?: string | null;
  mlIntent?: string | null;
  mlConfidence?: number | null;
  mlModelVersion?: string | null;
  roteMemoryHit?: boolean;
  relatedCases?: RelatedCase[];
}

export interface ChatRequest {
  message: string;
  context?: Array<{
    id?: string;
    role: string;
    content: string;
    conceptsUsed?: string[];
  }>;
}

export interface ChatResponse {
  response: string;
  conceptsUsed: string[];
  confidence: number | null;
  matchScore: number | null;
  sources: SourceReference[];
  trace: TraceStep[];
  status: 'answered' | 'greeting' | 'unsupported' | 'needs_clarification';
  suggestions: string[];
  missingInfo?: string | null;
  mlIntent?: string | null;
  mlConfidence?: number | null;
  mlModelVersion?: string | null;
  roteMemoryHit?: boolean;
  relatedCases?: RelatedCase[];
}

export interface KnowledgeRecord {
  id: string;
  title: string;
  content: string;
  keywords?: string;
  topic_id?: string;
  topic_name?: string;
  unit?: number;
  source_id?: string;
  source_name?: string;
  source_desc?: string;
  relevance_score?: number;
}

export interface KnowledgeListResponse {
  total: number;
  records: KnowledgeRecord[];
}

export interface SyllabusConceptItem {
  unit: string;
  concept: string;
  use_case: string;
  phase: number;
  status: string;
  source_reference?: string;
  test_reference?: string;
}

export interface SyllabusUnit {
  id: number;
  name: string;
  theme: string;
  concepts: SyllabusConceptItem[];
  phase_coverage: number[];
}

export interface ConceptsResponse {
  units: SyllabusUnit[];
  phase_focus: number;
}

export interface HealthResponse {
  status: string;
  service: string;
  phase: number;
  database: string;
  features: Record<string, string>;
}

// PathForge (Phase 2) Types
export interface PathForgeTopic {
  id: string;
  name: string;
  description: string;
  unit: number;
  category?: string;
  estimated_hours?: number;
  prerequisites?: string[];
  knowledge_record_id?: string;
  source_id?: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  relationship_type: string;
}

export interface PathForgeGraphResponse {
  nodes: PathForgeTopic[];
  edges: GraphEdge[];
  total_topics: number;
  total_edges: number;
}

export interface PlannedTopicItem {
  topic_id: string;
  name: string;
  description: string;
  unit: number;
  category?: string;
  estimated_hours: number;
  direct_prerequisites: string[];
  reason_included: string;
  step_number: number;
  status: 'completed' | 'pending';
}

export interface LearningPlanResponse {
  success: boolean;
  goal_topic_id: string;
  goal_topic_name: string;
  start_topic_id?: string | null;
  start_topic_name?: string | null;
  algorithm_used: string;
  shortest_path_nodes: string[];
  shortest_path_edges: number;
  shortest_path_reachable: boolean;
  all_prerequisites: string[];
  already_mastered: string[];
  remaining_prerequisites: string[];
  planned_journey: PlannedTopicItem[];
  total_estimated_hours: number;
  trace: TraceStep[];
  warnings: string[];
  error?: string;
}

export interface AlgorithmComparisonItem {
  algorithm: string;
  path_found: boolean;
  path: string[];
  edge_count: number;
  nodes_explored_count: number;
  explored_order: string[];
  duration_ms: number;
  optimality_note: string;
}

export interface CompareAlgorithmsResponse {
  success: boolean;
  start_topic: string;
  target_topic: string;
  results: AlgorithmComparisonItem[];
  explanation: string;
  error?: string;
}

export interface ScheduledSession {
  topic_id: string;
  topic_name: string;
  day: string;
  slot_index: number;
  duration_hours: number;
  session_number: number;
  total_sessions_for_topic: number;
}

export interface StudyScheduleResponse {
  success: boolean;
  is_feasible: boolean;
  sessions: ScheduledSession[];
  total_hours_scheduled: number;
  total_hours_required: number;
  available_capacity_hours: number;
  backtrack_count: number;
  assignments_tried: number;
  duration_ms: number;
  constraints_enforced: string[];
  explanation: string;
  trace: TraceStep[];
  warnings: string[];
}

// =========================================================================
// Phase 3: Knowledge Representation, Logical Reasoning & WhatIf Lab Types
// =========================================================================

export interface RuleConditionItem {
  predicate: string;
  operator: string;
  expected_value: unknown;
  variable_name?: string;
  threshold?: number;
  weight?: number;
}

export interface RuleConclusionItem {
  predicate: string;
  value: unknown;
  is_intermediate?: boolean;
}

export interface DeclarativeRule {
  id: string;
  policy_id: string;
  name: string;
  description: string;
  conditions: RuleConditionItem[];
  conclusion: RuleConclusionItem;
  priority: number;
  is_exception_rule: boolean;
  overrides_rule_id?: string | null;
  provenance: string;
}

export interface WhatIfPolicy {
  id: string;
  name: string;
  description: string;
  category: string;
  disclaimer: string;
  rules?: DeclarativeRule[];
  baseline_preset?: Record<string, unknown>;
}

export interface ForwardStepItem {
  step: number;
  rule_id: string;
  rule_name: string;
  matched_facts: Record<string, unknown>;
  derived_conclusion: Record<string, unknown>;
  is_exception: boolean;
  overridden_rule_id?: string | null;
}

export interface ForwardChainingEvaluationResult {
  policy_id: string;
  entity_id: string;
  final_decision: unknown;
  decision_status: 'SATISFIED' | 'NOT_SATISFIED' | 'INCONCLUSIVE' | 'CONFLICT' | 'OVERRIDDEN';
  initial_facts: Record<string, unknown>;
  derived_facts: Record<string, unknown>;
  activated_rules: DeclarativeRule[];
  overridden_rules: DeclarativeRule[];
  satisfied_conditions: Array<{ rule_id: string; condition: string; actual_value: unknown }>;
  unsatisfied_conditions: Array<{ rule_id: string; condition: string; actual_value: unknown; reason: string }>;
  missing_facts: string[];
  fired_steps: ForwardStepItem[];
  explanation: string;
}

export interface EvaluateWhatIfResponse {
  result: ForwardChainingEvaluationResult;
  trace: TraceStep[];
  policy?: WhatIfPolicy;
}

export interface InputDiffItem {
  predicate: string;
  baseline_value: unknown;
  modified_value: unknown;
  change_type: 'modified' | 'added' | 'removed' | 'unchanged';
}

export interface CounterfactualComparisonReport {
  policy_id: string;
  entity_id: string;
  decision_changed: boolean;
  baseline_decision: unknown;
  modified_decision: unknown;
  baseline_status: string;
  modified_status: string;
  input_diffs: InputDiffItem[];
  newly_activated_rules: string[];
  deactivated_rules: string[];
  newly_overridden_rules: string[];
  delta_summary: string;
}

export interface CompareWhatIfResponse {
  comparison: CounterfactualComparisonReport;
  baseline_result: ForwardChainingEvaluationResult;
  modified_result: ForwardChainingEvaluationResult;
  baseline_trace: TraceStep[];
  modified_trace: TraceStep[];
  policy?: WhatIfPolicy;
}

export interface GoalProofResult {
  goal: string;
  desired_value: unknown;
  status: 'PROVEN' | 'DISPROVEN' | 'UNKNOWN' | 'CONFLICT';
  entity_id: string;
  proven_path: string[];
  missing_subgoals: string[];
  conflicts: string[];
  proof_tree: unknown;
  explanation: string;
}

export interface GoalProofResponse {
  proof: GoalProofResult;
  trace: TraceStep[];
}

export interface ConsistencyCheckResponse {
  policy_id: string;
  is_consistent: boolean;
  contradictions_found: number;
  derived_empty_clauses: string[];
  steps_count: number;
  execution_ms: number;
  explanation: string;
}

// =========================================================================
// Phase 4: Machine Learning, Expert Systems & Learning Engine Types
// =========================================================================

export interface FeedbackItem {
  id: string;
  query: string;
  original_answer: string;
  feedback_type: 'helpful' | 'not_helpful';
  suggested_correction?: string | null;
  student_id?: string | null;
  target_knowledge_id?: string | null;
  message_id?: string | null;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  reviewer_notes?: string | null;
  created_at: string;
  reviewed_at?: string | null;
}

export interface FeedbackCreateRequest {
  query: string;
  original_answer: string;
  feedback_type: 'helpful' | 'not_helpful';
  suggested_correction?: string | null;
  student_id?: string | null;
  target_knowledge_id?: string | null;
  message_id?: string | null;
}

export interface FeedbackReviewRequest {
  decision: 'APPROVED' | 'REJECTED';
  reviewer_notes?: string;
  update_knowledge?: boolean;
}

export interface MLMetricsResponse {
  model_version: string;
  trained_at: string;
  algorithm: string;
  training_samples: number;
  test_samples: number;
  accuracy: number;
  macro_precision: number;
  macro_recall: number;
  macro_f1: number;
  classes: string[];
  per_class_report: Record<string, { precision: number; recall: number; f1_score: number; support: number }>;
  confusion_matrix: number[][];
}

export interface MemoryStatsResponse {
  total_cached_queries: number;
  valid_entries: number;
  invalidated_entries: number;
  total_hits: number;
  earliest_cache: string | null;
  latest_hit: string | null;
}

export interface MemoryItem {
  id: string;
  query_hash: string;
  normalized_query: string;
  answer_text: string;
  sources_json?: string;
  confidence: number;
  hit_count: number;
  created_at: string;
  last_accessed_at: string;
  is_valid: number;
}

export interface KnowledgeHistoryItem {
  id: string;
  knowledge_id: string;
  previous_content: string;
  new_content: string;
  feedback_id?: string | null;
  updated_at: string;
}

