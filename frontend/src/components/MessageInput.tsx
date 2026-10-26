import React, { useState, useRef, useEffect, KeyboardEvent } from 'react';
import { Send, Loader2, CornerDownLeft } from 'lucide-react';

interface MessageInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

export const MessageInput: React.FC<MessageInputProps> = ({ onSend, isLoading, disabled }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 140)}px`;
    }
  }, [input]);

  const handleSubmit = () => {
    const trimmed = input.trim();
    if (trimmed && !isLoading && !disabled) {
      onSend(trimmed);
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const isExceeded = input.length > 1000;
  const canSubmit = input.trim().length > 0 && !isLoading && !disabled && !isExceeded;

  return (
    <div className="w-full">
      <div className="relative rounded-2xl border border-slate-200/90 bg-white shadow-sm focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-500/10 transition-all">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask an academic question about AI concepts, search, agents, or logic..."
          disabled={isLoading || disabled}
          rows={1}
          maxLength={1000}
          className="w-full px-4 pt-3.5 pb-10 text-xs sm:text-sm text-slate-800 placeholder-slate-400 bg-transparent resize-none focus:outline-none min-h-[52px] max-h-[140px]"
        />

        {/* Action Bar Footer inside Input */}
        <div className="absolute bottom-2 left-3 right-2 flex items-center justify-between pointer-events-none">
          <div className="flex items-center space-x-2 text-[11px] text-slate-400 pointer-events-auto">
            <span className="hidden sm:inline-flex items-center">
              <CornerDownLeft className="w-3 h-3 mr-1" />
              Press Enter to send
            </span>
            <span className={`text-[10px] ${isExceeded ? 'text-rose-600 font-bold' : ''}`}>
              {input.length}/1000
            </span>
          </div>

          <button
            onClick={handleSubmit}
            disabled={!canSubmit}
            className={`pointer-events-auto p-2 rounded-xl text-white transition-all flex items-center justify-center ${
              canSubmit
                ? 'bg-brand-600 hover:bg-brand-700 shadow-sm shadow-brand-600/30 active:scale-95'
                : 'bg-slate-200 text-slate-400 cursor-not-allowed'
            }`}
            aria-label="Send message"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin text-white" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default MessageInput;
