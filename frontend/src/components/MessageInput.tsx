import { useState, KeyboardEvent } from 'react'
import { Send, Loader2 } from 'lucide-react'

interface MessageInputProps {
  onSend: (message: string) => void
  isLoading: boolean
}

const MessageInput = ({ onSend, isLoading }: MessageInputProps) => {
  const [input, setInput] = useState('')

  const handleSubmit = () => {
    if (input.trim() && !isLoading) {
      onSend(input)
      setInput('')
    }
  }

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="flex gap-3 items-end">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Ask me anything about your studies..."
        disabled={isLoading}
        rows={1}
        className="input-field resize-none min-h-[48px] max-h-[120px]"
        style={{ 
          height: 'auto',
          overflowY: input.split('\n').length > 3 ? 'auto' : 'hidden'
        }}
      />
      <button
        onClick={handleSubmit}
        disabled={!input.trim() || isLoading}
        className="btn-primary flex-shrink-0 h-12 w-12 flex items-center justify-center"
        aria-label="Send message"
      >
        {isLoading ? (
          <Loader2 className="w-5 h-5 animate-spin" />
        ) : (
          <Send className="w-5 h-5" />
        )}
      </button>
    </div>
  )
}

export default MessageInput
