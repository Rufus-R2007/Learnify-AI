import { Message } from '../types'
import MessageBubble from './MessageBubble'

interface MessageListProps {
  messages: Message[]
}

const MessageList = ({ messages }: MessageListProps) => {
  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
    </div>
  )
}

export default MessageList
