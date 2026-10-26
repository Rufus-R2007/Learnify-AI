import { useState, useRef, useEffect } from 'react';
import { Loader2, AlertCircle, RefreshCw } from 'lucide-react';
import { Message } from '../types';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import WelcomeScreen from './WelcomeScreen';
import { sendMessage } from '../services/api';

interface ChatInterfaceProps {
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  activeMessage: Message | null;
  setActiveMessage: (message: Message | null) => void;
  onOpenProofLens: () => void;
  externalQuery?: string | null;
  onClearExternalQuery?: () => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  setMessages,
  activeMessage,
  setActiveMessage,
  onOpenProofLens,
  externalQuery,
  onClearExternalQuery,
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [lastFailedQuery, setLastFailedQuery] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    if (externalQuery) {
      handleSendMessage(externalQuery);
      if (onClearExternalQuery) {
        onClearExternalQuery();
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [externalQuery]);

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    setErrorMessage(null);
    setLastFailedQuery(null);

    // 1. Add user message
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // 2. Call backend API with conversation context
      const chatResponse = await sendMessage(content, messages);

      // 3. Assemble assistant message
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: chatResponse.response,
        timestamp: new Date(),
        conceptsUsed: chatResponse.conceptsUsed,
        confidence: chatResponse.confidence,
        matchScore: chatResponse.matchScore,
        sources: chatResponse.sources,
        trace: chatResponse.trace,
        status: chatResponse.status,
        suggestions: chatResponse.suggestions,
        missingInfo: chatResponse.missingInfo,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setActiveMessage(assistantMessage);
    } catch (err: unknown) {
      console.error('Error in chat interaction:', err);
      const detail = err instanceof Error ? err.message : 'Failed to connect to Learnify AI backend.';
      setErrorMessage(detail);
      setLastFailedQuery(content);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    if (lastFailedQuery) {
      handleSendMessage(lastFailedQuery);
    }
  };

  const hasUserMessages = messages.some((m) => m.role === 'user');

  return (
    <div className="flex-1 h-full flex flex-col bg-slate-50/60 overflow-hidden relative">
      {/* Scrollable Message Area */}
      <div className="flex-1 overflow-y-auto px-4 sm:px-6">
        {!hasUserMessages && messages.length <= 1 ? (
          <WelcomeScreen onSelectQuery={handleSendMessage} />
        ) : (
          <div className="max-w-3xl mx-auto w-full pb-4">
            <MessageList
              messages={messages}
              activeMessageId={activeMessage?.id || null}
              onSelectForProofLens={(msg) => {
                setActiveMessage(msg);
                onOpenProofLens();
              }}
              onSelectSuggestion={handleSendMessage}
            />

            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex items-center space-x-3 py-3 px-4 rounded-2xl bg-white border border-slate-200/80 shadow-xs max-w-sm animate-pulse-subtle">
                <Loader2 className="w-4 h-4 animate-spin text-brand-600 shrink-0" />
                <div className="text-xs text-slate-600">
                  <span className="font-semibold block text-slate-800">Processing query...</span>
                  <span className="text-[11px] text-slate-400">
                    Executing Unit I agent pipeline & recording ProofLens trace
                  </span>
                </div>
              </div>
            )}

            {/* Error Banner */}
            {errorMessage && (
              <div className="mt-3 p-3.5 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-start justify-between">
                <div className="flex items-start space-x-2">
                  <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold block">Connection Error</span>
                    <p className="text-rose-700 leading-normal">{errorMessage}</p>
                  </div>
                </div>
                {lastFailedQuery && (
                  <button
                    onClick={handleRetry}
                    className="ml-3 inline-flex items-center space-x-1 px-2.5 py-1 bg-white hover:bg-rose-100 text-rose-700 border border-rose-300 rounded-lg text-xs font-semibold shrink-0 transition-colors"
                  >
                    <RefreshCw className="w-3 h-3" />
                    <span>Retry</span>
                  </button>
                )}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Composer Footer */}
      <div className="p-3 sm:p-4 bg-white border-t border-slate-200/80 shrink-0">
        <div className="max-w-3xl mx-auto w-full">
          <MessageInput onSend={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
