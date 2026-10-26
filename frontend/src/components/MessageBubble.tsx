import React, { useState } from 'react';
import {
  User,
  Bot,
  BookOpen,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Zap,
  Sparkles,
  ThumbsUp,
  ThumbsDown,
  Send,
  Lightbulb
} from 'lucide-react';
import { Message } from '../types';
import { submitFeedback } from '../services/api';

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

  // Feedback State
  const [feedbackGiven, setFeedbackGiven] = useState<'helpful' | 'not_helpful' | null>(null);
  const [showCorrectionBox, setShowCorrectionBox] = useState(false);
  const [suggestedCorrection, setSuggestedCorrection] = useState('');
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  const [feedbackSuccessMsg, setFeedbackSuccessMsg] = useState<string | null>(null);

  const handleSendFeedback = async (type: 'helpful' | 'not_helpful', correction?: string) => {
    try {
      setSubmittingFeedback(true);
      await submitFeedback({
        query: message.content.slice(0, 100),
        original_answer: message.content,
        feedback_type: type,
        suggested_correction: correction?.trim() || null,
        message_id: message.id,
      });
      setFeedbackGiven(type);
      setShowCorrectionBox(false);
      setFeedbackSuccessMsg(
        correction?.trim()
          ? 'Advice & correction submitted for reviewer approval!'
          : 'Thank you for your feedback!'
      );
    } catch (e) {
      console.error('Failed to submit feedback', e);
    } finally {
      setSubmittingFeedback(false);
    }
  };

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

        {/* Assistant Metadata Footer: ProofLens Action, Concepts, ML & Rote Badges */}
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

            {/* Rote Learning Cache Hit Badge */}
            {message.roteMemoryHit && (
              <span className="inline-flex items-center text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                <Zap className="w-3 h-3 mr-1 text-emerald-500" />
                Rote Cache Hit (&lt;1ms)
              </span>
            )}

            {/* ML Intent Badge */}
            {message.mlIntent && (
              <span className="inline-flex items-center text-[10px] font-semibold px-2 py-0.5 rounded-full bg-purple-50 text-purple-700 border border-purple-200">
                <Sparkles className="w-3 h-3 mr-1 text-purple-500" />
                ML: {message.mlIntent}
              </span>
            )}

            {/* Relevance Score Pill */}
            {matchScorePercent !== null && !message.roteMemoryHit && (
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

            {/* Human Advice Feedback Buttons (Concept 2) */}
            <div className="flex items-center space-x-1 ml-auto">
              {feedbackGiven ? (
                <span className="text-[10px] text-emerald-600 font-medium">
                  {feedbackSuccessMsg || 'Feedback noted'}
                </span>
              ) : (
                <>
                  <button
                    onClick={() => handleSendFeedback('helpful')}
                    disabled={submittingFeedback}
                    className="p-1 rounded-md text-slate-400 hover:text-emerald-600 hover:bg-slate-100 transition-colors"
                    title="Helpful response"
                  >
                    <ThumbsUp className="w-3 h-3" />
                  </button>
                  <button
                    onClick={() => setShowCorrectionBox((prev) => !prev)}
                    disabled={submittingFeedback}
                    className="p-1 rounded-md text-slate-400 hover:text-amber-600 hover:bg-slate-100 transition-colors"
                    title="Suggest a correction / Not helpful"
                  >
                    <ThumbsDown className="w-3 h-3" />
                  </button>
                </>
              )}
            </div>
          </div>
        )}

        {/* Suggestion / Correction Box (Concept 2: Learning by Taking Advice) */}
        {!isUser && showCorrectionBox && !feedbackGiven && (
          <div className="mt-2 w-full p-3 rounded-xl bg-purple-50/70 border border-purple-200 text-xs space-y-2 animate-fade-in">
            <span className="font-semibold text-purple-900 block text-[11px]">
              Suggest an authoritative correction or note:
            </span>
            <textarea
              rows={2}
              value={suggestedCorrection}
              onChange={(e) => setSuggestedCorrection(e.target.value)}
              placeholder="e.g., BFS has space complexity O(b^d), not O(b*m)..."
              className="w-full p-2 text-xs rounded-lg border border-purple-200 bg-white focus:outline-none focus:ring-1 focus:ring-purple-500"
            />
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => setShowCorrectionBox(false)}
                className="px-2.5 py-1 text-[11px] text-slate-500 hover:text-slate-700"
              >
                Cancel
              </button>
              <button
                disabled={submittingFeedback}
                onClick={() => handleSendFeedback('not_helpful', suggestedCorrection)}
                className="px-3 py-1 rounded-lg bg-purple-600 hover:bg-purple-700 text-white font-semibold text-[11px] shadow-2xs flex items-center space-x-1"
              >
                <Send className="w-3 h-3" />
                <span>Submit Advice</span>
              </button>
            </div>
          </div>
        )}

        {/* Analogy: Related Solved Curriculum Questions (Concept 4) */}
        {!isUser && message.relatedCases && message.relatedCases.length > 0 && (
          <div className="mt-3 w-full p-3 rounded-xl bg-amber-50/60 border border-amber-200/80">
            <div className="flex items-center space-x-1.5 mb-2 text-amber-900 font-semibold text-[11px]">
              <Lightbulb className="w-3.5 h-3.5 text-amber-600" />
              <span>Related Solved Curriculum Questions (Learning by Analogy):</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {message.relatedCases.map((rc) => (
                <button
                  key={rc.id}
                  onClick={() => onSelectSuggestion(rc.question)}
                  className="text-left px-2.5 py-1 rounded-lg bg-white hover:bg-amber-100 text-slate-800 text-[11px] border border-amber-200 transition-all flex items-center space-x-1.5 shadow-2xs"
                >
                  <span className="truncate max-w-xs">{rc.question}</span>
                  <span className="text-[10px] font-mono text-amber-700 shrink-0 font-bold">
                    {Math.round(rc.similarity * 100)}%
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Assistant Follow-up Suggestions */}
        {!isUser && message.suggestions && message.suggestions.length > 0 && (
          <div className="mt-2.5 flex flex-wrap gap-1.5">
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
