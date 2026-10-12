import axios from 'axios'
import { ChatRequest, ChatResponse, Message } from '../types'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
})

/**
 * Send a chat message to the backend API
 * @param message - User's message
 * @param context - Previous conversation messages for context
 * @returns ChatResponse with AI-generated reply
 */
export const sendMessage = async (
  message: string,
  context: Message[] = []
): Promise<ChatResponse> => {
  try {
    const request: ChatRequest = {
      message,
      context: context.slice(-10), // Send only last 10 messages for context
    }

    const response = await api.post<ChatResponse>('/api/chat/', request)
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
        throw new Error('Cannot connect to backend server. Please ensure it is running on http://localhost:8000')
      }
      if (error.response) {
        throw new Error(error.response.data.detail || 'Server error occurred')
      }
    }
    throw new Error('An unexpected error occurred while sending message')
  }
}

/**
 * Get the list of AI concepts and units
 * @returns Array of AI units with concepts
 */
export const getAIConcepts = async () => {
  try {
    const response = await api.get('/api/chat/concepts')
    return response.data
  } catch (error) {
    console.error('Error fetching AI concepts:', error)
    throw error
  }
}

/**
 * Check backend health status
 * @returns Health status object
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health')
    return response.data
  } catch (error) {
    console.error('Error checking backend health:', error)
    return { status: 'unavailable' }
  }
}

/**
 * Get API root information
 * @returns API information object
 */
export const getAPIInfo = async () => {
  try {
    const response = await api.get('/')
    return response.data
  } catch (error) {
    console.error('Error fetching API info:', error)
    throw error
  }
}

export default api
