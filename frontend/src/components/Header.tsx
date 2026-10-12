import { Brain, Sparkles } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Brain className="w-10 h-10 text-primary-600" />
              <Sparkles className="w-4 h-4 text-yellow-500 absolute -top-1 -right-1" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Learnify AI</h1>
              <p className="text-sm text-gray-600">AI-Powered Chatbot for Student Queries</p>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-4">
            <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs font-medium">
              Beta Version
            </span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
