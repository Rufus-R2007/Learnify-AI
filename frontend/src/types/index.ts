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
  | 'fallback';

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
