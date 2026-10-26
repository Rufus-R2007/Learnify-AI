import React, { useState } from 'react';
import {
  ShieldCheck,
  Clock,
  Cpu,
  Layers,
  ChevronDown,
  ChevronRight,
  BookOpen,
  AlertCircle,
  Sparkles,
  X,
  CheckCircle2,
  AlertTriangle,
  FileText
} from 'lucide-react';
import { Message, TraceStep } from '../types';

interface ProofLensPanelProps {
  activeMessage: Message | null;
  onClose?: () => void;
}

export const ProofLensPanel: React.FC<ProofLensPanelProps> = ({ activeMessage, onClose }) => {
  const [expandedSteps, setExpandedSteps] = useState<Record<string, boolean>>({
    'step-1': true,
    'step-4': true,
  });

  const toggleStep = (stepId: string) => {
    setExpandedSteps((prev) => ({
      ...prev,
      [stepId]: !prev[stepId],
    }));
  };

  if (!activeMessage || activeMessage.role !== 'assistant') {
    return (
      <aside className="w-full h-full flex flex-col bg-white border-l border-slate-200/80 p-6 select-none">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-brand-50 border border-brand-200/60 flex items-center justify-center text-brand-600">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-slate-900 tracking-tight">ProofLens</h2>
              <p className="text-xs text-slate-500">Transparent AI Execution & Evidence</p>
            </div>
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              aria-label="Close panel"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        <div className="flex-1 flex flex-col items-center justify-center text-center p-6 text-slate-400">
          <div className="w-12 h-12 rounded-2xl bg-slate-50 border border-slate-200/60 flex items-center justify-center mb-3 text-slate-400">
            <Cpu className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-medium text-slate-700 mb-1">No Active Execution Trace</h3>
          <p className="text-xs text-slate-500 max-w-xs leading-relaxed">
            Submit a query in the chat or select any assistant response to inspect its verified reasoning stages, timing, and evidence.
          </p>
        </div>
      </aside>
    );
  }

  const traces: TraceStep[] = activeMessage.trace || [];
  const totalDuration = traces.reduce((acc, step) => acc + (step.duration_ms || 0), 0);
  const matchScorePercent = activeMessage.matchScore
    ? Math.round(activeMessage.matchScore * 100)
    : null;

  return (
    <aside className="w-full h-full flex flex-col bg-white border-l border-slate-200/80 overflow-hidden">
      {/* Panel Header */}
      <div className="px-5 py-4 border-b border-slate-200/80 bg-slate-50/70">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white shadow-sm shadow-brand-500/20">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-sm font-bold text-slate-900 tracking-tight">ProofLens</h2>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-brand-100 text-brand-700 uppercase tracking-wider">
                  Live Trace
                </span>
              </div>
              <p className="text-xs text-slate-500">Verified evidence & execution trace</p>
            </div>
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
              aria-label="Close ProofLens"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Quick Metrics Strip */}
        <div className="grid grid-cols-3 gap-2 pt-1 text-center">
          <div className="bg-white rounded-lg p-2 border border-slate-200/60 shadow-xs">
            <span className="text-[10px] uppercase font-semibold text-slate-400 block tracking-wider">
              Total Time
            </span>
            <div className="flex items-center justify-center space-x-1 mt-0.5 text-slate-700">
              <Clock className="w-3 h-3 text-slate-400" />
              <span className="text-xs font-mono font-bold text-slate-900">
                {totalDuration.toFixed(2)} ms
              </span>
            </div>
          </div>

          <div className="bg-white rounded-lg p-2 border border-slate-200/60 shadow-xs">
            <span className="text-[10px] uppercase font-semibold text-slate-400 block tracking-wider">
              Pipeline Steps
            </span>
            <div className="flex items-center justify-center space-x-1 mt-0.5 text-slate-700">
              <Layers className="w-3 h-3 text-slate-400" />
              <span className="text-xs font-bold text-slate-900">{traces.length} stages</span>
            </div>
          </div>

          <div className="bg-white rounded-lg p-2 border border-slate-200/60 shadow-xs">
            <span className="text-[10px] uppercase font-semibold text-slate-400 block tracking-wider">
              Grounding
            </span>
            <div className="flex items-center justify-center space-x-1 mt-0.5">
              {activeMessage.status === 'answered' ? (
                <span className="inline-flex items-center text-xs font-bold text-emerald-700">
                  <CheckCircle2 className="w-3 h-3 mr-0.5 text-emerald-500" />
                  {matchScorePercent ? `${matchScorePercent}%` : 'Verified'}
                </span>
              ) : activeMessage.status === 'greeting' ? (
                <span className="text-xs font-semibold text-brand-600">Reflex</span>
              ) : (
                <span className="inline-flex items-center text-xs font-semibold text-amber-700">
                  <AlertTriangle className="w-3 h-3 mr-0.5 text-amber-500" />
                  Guarded
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Scrollable Trace Content */}
      <div className="flex-1 overflow-y-auto px-5 py-4 space-y-5">
        {/* Missing information notice if present */}
        {activeMessage.missingInfo && (
          <div className="p-3 bg-amber-50/80 border border-amber-200/70 rounded-xl text-xs text-amber-900">
            <div className="flex items-start space-x-2">
              <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold block mb-0.5">Missing or Guarded Information:</span>
                <p className="text-amber-800 leading-relaxed">{activeMessage.missingInfo}</p>
              </div>
            </div>
          </div>
        )}

        {/* Trace Steps Progression */}
        <div>
          <div className="flex items-center justify-between mb-2.5">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Execution Timeline ({traces.length})
            </h3>
            <span className="text-[11px] text-slate-400">Chronological</span>
          </div>

          <div className="space-y-2">
            {traces.map((step, idx) => {
              const isExpanded = expandedSteps[step.id] ?? false;
              const isCompleted = step.status === 'completed';
              const isFallback = step.status === 'fallback';

              return (
                <div
                  key={step.id || idx}
                  className="rounded-xl border border-slate-200/80 bg-white shadow-xs overflow-hidden transition-all duration-150"
                >
                  <button
                    onClick={() => toggleStep(step.id)}
                    className="w-full px-3.5 py-2.5 flex items-center justify-between text-left hover:bg-slate-50/70 transition-colors"
                  >
                    <div className="flex items-center space-x-2.5 min-w-0">
                      <div
                        className={`w-6 h-6 rounded-md flex items-center justify-center text-[11px] font-bold shrink-0 ${
                          isCompleted
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : isFallback
                            ? 'bg-amber-50 text-amber-700 border border-amber-200'
                            : 'bg-slate-100 text-slate-500 border border-slate-200'
                        }`}
                      >
                        {String(idx + 1).padStart(2, '0')}
                      </div>
                      <div className="min-w-0">
                        <div className="flex items-center space-x-1.5">
                          <span className="text-xs font-semibold text-slate-900 truncate">
                            {step.stage}
                          </span>
                          <span
                            className={`text-[9px] uppercase px-1.5 py-0.2 rounded font-medium ${
                              step.execution_type === 'reflex'
                                ? 'bg-purple-50 text-purple-700'
                                : step.execution_type === 'model_based'
                                ? 'bg-blue-50 text-blue-700'
                                : step.execution_type === 'goal_based'
                                ? 'bg-indigo-50 text-indigo-700'
                                : step.execution_type === 'retrieval'
                                ? 'bg-teal-50 text-teal-700'
                                : 'bg-slate-100 text-slate-600'
                            }`}
                          >
                            {step.execution_type}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-500 truncate">{step.method}</p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2 shrink-0 ml-2">
                      <span className="text-[11px] font-mono text-slate-500">
                        {step.duration_ms.toFixed(2)}ms
                      </span>
                      {isExpanded ? (
                        <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                      ) : (
                        <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                      )}
                    </div>
                  </button>

                  {isExpanded && (
                    <div className="px-3.5 pb-3 pt-1 border-t border-slate-100 bg-slate-50/40 text-xs space-y-2">
                      <p className="text-slate-600 leading-relaxed text-[11px]">
                        {step.description}
                      </p>

                      {step.input_summary && (
                        <div className="p-2 bg-white rounded-lg border border-slate-200/60 font-mono text-[10px] text-slate-700 break-words">
                          <span className="font-semibold text-slate-500 block mb-0.5">Input:</span>
                          {step.input_summary}
                        </div>
                      )}

                      {step.output_summary && (
                        <div className="p-2 bg-white rounded-lg border border-slate-200/60 font-mono text-[10px] text-slate-700 break-words">
                          <span className="font-semibold text-slate-500 block mb-0.5">Output:</span>
                          {step.output_summary}
                        </div>
                      )}

                      {step.evidence_ids && step.evidence_ids.length > 0 && (
                        <div className="flex items-center space-x-1.5 pt-0.5 text-[10px] text-slate-500">
                          <FileText className="w-3 h-3 text-slate-400" />
                          <span>Evidence IDs:</span>
                          <span className="font-mono text-brand-700 font-medium">
                            {step.evidence_ids.join(', ')}
                          </span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Supporting Verified Sources */}
        <div>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
            Supporting Evidence & Sources
          </h3>

          {activeMessage.sources && activeMessage.sources.length > 0 ? (
            <div className="space-y-2">
              {activeMessage.sources.map((src, i) => (
                <div
                  key={src.id || i}
                  className="p-3 bg-slate-50 border border-slate-200/80 rounded-xl"
                >
                  <div className="flex items-center space-x-2 mb-1">
                    <BookOpen className="w-3.5 h-3.5 text-brand-600 shrink-0" />
                    <span className="text-xs font-semibold text-slate-900">{src.name}</span>
                  </div>
                  {src.description && (
                    <p className="text-[11px] text-slate-500 pl-5 leading-normal">
                      {src.description}
                    </p>
                  )}
                  <span className="inline-block mt-1 pl-5 text-[10px] font-mono text-slate-400">
                    ID: {src.id}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-3 bg-slate-50 border border-dashed border-slate-200 rounded-xl text-center text-xs text-slate-400">
              No authoritative textbook source attached for this response type.
            </div>
          )}
        </div>

        {/* Actual AI Concepts Used */}
        <div>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
            Unit I AI Concepts Involved
          </h3>
          <div className="flex flex-wrap gap-1.5">
            {activeMessage.conceptsUsed && activeMessage.conceptsUsed.length > 0 ? (
              activeMessage.conceptsUsed.map((concept, i) => (
                <span
                  key={i}
                  className="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-medium bg-brand-50 text-brand-700 border border-brand-200/60"
                >
                  <Sparkles className="w-3 h-3 mr-1 text-brand-500" />
                  {concept}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-400">No concepts tagged.</span>
            )}
          </div>
        </div>
      </div>
    </aside>
  );
};

export default ProofLensPanel;
