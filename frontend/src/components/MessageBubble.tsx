import { User, Bot, Lightbulb } from 'lucide-react'
import { Message } from '../types'
import { clsx } from 'clsx'

interface MessageBubbleProps {
  message: Message
}

const MessageBubble = ({ message }: MessageBubbleProps) => {
  const isUser = message.role === 'user'

  return (
    <div className={clsx('flex gap-3', isUser ? 'justify-end' : 'justify-start')}>
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className={clsx('flex flex-col max-w-[70%]', isUser && 'items-end')}>
        <div className={clsx('chat-message', isUser ? 'user' : 'assistant')}>
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
        </div>
        
        {message.conceptsUsed && message.conceptsUsed.length > 0 && (
          <div className="mt-2 flex items-center gap-2 text-xs text-gray-500">
            <Lightbulb className="w-3 h-3" />
            <span>AI Concepts: {message.conceptsUsed.join(', ')}</span>
          </div>
        )}
        
        <span className="text-xs text-gray-400 mt-1">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  )
}

export default MessageBubble
