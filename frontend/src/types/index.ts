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
