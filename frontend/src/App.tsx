import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import Header from './components/Header'
import { Message } from './types'

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m Learnify AI, your intelligent student assistant. I can help you with academic queries using AI concepts like search algorithms, knowledge representation, logical reasoning, and expert systems. What would you like to learn about today?',
      timestamp: new Date(),
    }
  ])

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-primary-50 via-white to-blue-50">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-6 max-w-5xl">
        <ChatInterface messages={messages} setMessages={setMessages} />
      </main>
      <footer className="bg-white border-t border-gray-200 py-4">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          <p>Learnify AI — AI-Powered Chatbot for Student Queries</p>
          <p className="text-xs mt-1">Using Knowledge Representation • Search Algorithms • Logical Reasoning • Expert Systems</p>
        </div>
      </footer>
    </div>
  )
}

export default App
