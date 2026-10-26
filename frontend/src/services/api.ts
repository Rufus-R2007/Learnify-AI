import axios from 'axios';
import {
  ChatRequest,
  ChatResponse,
  Message,
  ConceptsResponse,
  KnowledgeListResponse,
  KnowledgeRecord,
  HealthResponse,
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

export default api;
