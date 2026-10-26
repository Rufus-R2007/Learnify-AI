import React from 'react';
import { Message } from '../types';
import MessageBubble from './MessageBubble';

interface MessageListProps {
  messages: Message[];
  activeMessageId: string | null;
  onSelectForProofLens: (message: Message) => void;
  onSelectSuggestion: (query: string) => void;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  activeMessageId,
  onSelectForProofLens,
  onSelectSuggestion,
}) => {
  return (
    <div className="space-y-4 py-4">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
          isActiveInProofLens={activeMessageId === message.id}
          onSelectForProofLens={onSelectForProofLens}
          onSelectSuggestion={onSelectSuggestion}
        />
      ))}
    </div>
  );
};

export default MessageList;
