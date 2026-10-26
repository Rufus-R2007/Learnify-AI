import React from 'react';
import {
  User,
  Bot,
  BookOpen,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  ArrowRight
} from 'lucide-react';
import { Message } from '../types';

interface MessageBubbleProps {
  message: Message;
  isActiveInProofLens: boolean;
  onSelectForProofLens: (message: Message) => void;
  onSelectSuggestion: (query: string) => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  isActiveInProofLens,
  onSelectForProofLens,
  onSelectSuggestion,
}) => {
  const isUser = message.role === 'user';
  const matchScorePercent = message.matchScore
    ? Math.round(message.matchScore * 100)
    : null;

  return (
    <div
      className={`flex gap-3 animate-fade-in ${
        isUser ? 'justify-end' : 'justify-start'
      }`}
    >
      {/* Bot Icon */}
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-brand-600 text-white flex items-center justify-center shadow-xs mt-1">
          <Bot className="w-4 h-4" />
        </div>
      )}

      {/* Bubble Container */}
      <div
        className={`flex flex-col max-w-[85%] sm:max-w-[78%] ${
          isUser ? 'items-end' : 'items-start'
        }`}
      >
        {/* Main Content Bubble */}
        <div
          className={`px-4 py-3 rounded-2xl text-xs sm:text-sm leading-relaxed ${
            isUser
              ? 'bg-brand-600 text-white rounded-br-xs shadow-xs'
              : 'bg-white text-slate-800 border border-slate-200/90 rounded-bl-xs shadow-xs'
          }`}
        >
          <div className="whitespace-pre-wrap">{message.content}</div>

          {/* Sources Badge on Assistant messages */}
          {!isUser && message.sources && message.sources.length > 0 && (
            <div className="mt-3 pt-2.5 border-t border-slate-100 flex flex-wrap items-center gap-1.5">
              <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider flex items-center">
                <BookOpen className="w-3 h-3 mr-1 text-slate-400" />
                Source:
              </span>
              {message.sources.map((src, i) => (
                <span
                  key={i}
                  className="inline-flex items-center text-[11px] font-medium text-slate-600 bg-slate-50 border border-slate-200 px-2 py-0.5 rounded-md"
                  title={src.description || ''}
                >
                  {src.name}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Assistant Metadata Footer: ProofLens Action, Concepts, Match Score */}
        {!isUser && (
          <div className="mt-2 w-full flex flex-wrap items-center gap-2">
            {/* View in ProofLens Button */}
            <button
              onClick={() => onSelectForProofLens(message)}
              className={`inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-lg text-[11px] font-medium transition-all ${
                isActiveInProofLens
                  ? 'bg-brand-600 text-white shadow-xs'
                  : 'bg-white hover:bg-brand-50 text-brand-700 border border-brand-200 shadow-2xs'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>{isActiveInProofLens ? 'Viewing in ProofLens' : 'Inspect ProofLens'}</span>
            </button>

            {/* Relevance Score Pill */}
            {matchScorePercent !== null && (
              <span className="inline-flex items-center text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200/60">
                <CheckCircle2 className="w-3 h-3 mr-1 text-emerald-500" />
                {matchScorePercent}% Match
              </span>
            )}

            {/* Guarded / Missing info tag */}
            {message.status === 'unsupported' && (
              <span className="inline-flex items-center text-[10px] font-semibold px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
                <AlertTriangle className="w-3 h-3 mr-1 text-amber-500" />
                Truthful Guardrail
              </span>
            )}

            {/* AI Concepts Chips */}
            {message.conceptsUsed && message.conceptsUsed.length > 0 && (
              <div className="flex flex-wrap items-center gap-1">
                {message.conceptsUsed.slice(0, 3).map((concept, idx) => (
                  <span
                    key={idx}
                    className="text-[10px] text-slate-500 bg-slate-100/80 px-2 py-0.5 rounded"
                  >
                    {concept}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Assistant Follow-up Suggestions */}
        {!isUser && message.suggestions && message.suggestions.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {message.suggestions.map((suggestion, sIdx) => (
              <button
                key={sIdx}
                onClick={() => onSelectSuggestion(suggestion)}
                className="inline-flex items-center space-x-1 text-[11px] bg-white hover:bg-brand-50 text-slate-700 hover:text-brand-700 border border-slate-200/80 hover:border-brand-200 px-2.5 py-1 rounded-full transition-all text-left shadow-2xs"
              >
                <span>{suggestion}</span>
                <ArrowRight className="w-3 h-3 text-slate-400 shrink-0" />
              </button>
            ))}
          </div>
        )}

        {/* Timestamp */}
        <span className="text-[10px] text-slate-400 mt-1 px-1">
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </span>
      </div>

      {/* User Icon */}
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-slate-700 text-white flex items-center justify-center shadow-xs mt-1">
          <User className="w-4 h-4" />
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
