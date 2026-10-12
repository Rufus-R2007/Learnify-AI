export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  conceptsUsed?: string[];
}

export interface ChatRequest {
  message: string;
  context?: Message[];
}

export interface ChatResponse {
  response: string;
  conceptsUsed: string[];
  confidence: number;
}

export interface AIUnit {
  id: number;
  name: string;
  concepts: string[];
  implemented: boolean;
}
