import { useState, useRef, useEffect } from 'react'
import { Message } from '../types'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import { sendMessage } from '../services/api'

interface ChatInterfaceProps {
  messages: Message[]
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>
}

const ChatInterface = ({ messages, setMessages }: ChatInterfaceProps) => {
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Call API
      const response = await sendMessage(content, messages)
      
      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
        conceptsUsed: response.conceptsUsed,
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please make sure the backend server is running on http://localhost:8000',
        timestamp: new Date(),
      }

      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg h-[calc(100vh-200px)] flex flex-col">
      <div className="flex-1 overflow-y-auto p-4">
        <MessageList messages={messages} />
        <div ref={messagesEndRef} />
      </div>
      <div className="border-t border-gray-200 p-4">
        <MessageInput onSend={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  )
}

export default ChatInterface
