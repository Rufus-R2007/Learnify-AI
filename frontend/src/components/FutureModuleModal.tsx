import React from 'react';
import {
  GitBranch,
  FlaskConical,
  X,
  CheckCircle2
} from 'lucide-react';

interface FutureModuleModalProps {
  module: 'pathforge' | 'whatif' | null;
  onClose: () => void;
}

export const FutureModuleModal: React.FC<FutureModuleModalProps> = ({ module, onClose }) => {
  if (!module) return null;

  const isPathForge = module === 'pathforge';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
      <div className="bg-white w-full max-w-xl rounded-2xl shadow-2xl border border-slate-200/80 p-6 overflow-hidden animate-fade-in">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center space-x-3">
            <div
              className={`w-10 h-10 rounded-xl flex items-center justify-center text-white shadow-xs ${
                isPathForge ? 'bg-indigo-600' : 'bg-teal-600'
              }`}
            >
              {isPathForge ? (
                <GitBranch className="w-5 h-5" />
              ) : (
                <FlaskConical className="w-5 h-5" />
              )}
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-base font-bold text-slate-900">
                  {isPathForge ? 'PathForge Study Navigation' : 'WhatIf Lab Scenario Analyzer'}
                </h2>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200">
                  {isPathForge ? 'Phase 2 Module' : 'Phase 3 Module'}
                </span>
              </div>
              <p className="text-xs text-slate-500">
                {isPathForge
                  ? 'Responsible Developer: URK25CS1063 — Yogith Joy J'
                  : 'Responsible Developer: URK25CS1034 — Hiran Antony'}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="py-4 space-y-4">
          <div className="p-3.5 bg-slate-50 border border-slate-200/70 rounded-xl text-xs text-slate-600 leading-relaxed">
            <strong className="text-slate-900 block mb-1">
              {isPathForge ? 'Upcoming in Phase 2:' : 'Upcoming in Phase 3:'}
            </strong>
            {isPathForge
              ? 'PathForge will provide goal-oriented study-path generation powered by graph search (Breadth-First Search, Depth-First Search, and A* heuristic search) over curriculum prerequisite dependencies and course constraints.'
              : 'WhatIf Lab will provide an interactive academic decision-support workbench using rule-based reasoning (Forward Chaining and Backward Chaining), production rules, and truth maintenance.'}
          </div>

          {/* Phase 1 Preparation Status */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Phase 1 Architectural Foundation Ready:
            </h4>
            <div className="space-y-1.5 text-xs text-slate-700">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>
                  Backend extension interface established in{' '}
                  <code className="font-mono text-[11px] bg-slate-100 px-1 py-0.5 rounded">
                    backend/app/core/interfaces.py
                  </code>
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>
                  SQLite table <code className="font-mono text-[11px] bg-slate-100 px-1 py-0.5 rounded">topic_relationships</code>{' '}
                  seeded with prerequisite graph edges
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>
                  Extensible ProofLens trace contracts ready to render search trees & inference steps
                </span>
              </div>
            </div>
          </div>

          {/* Code Contract Preview */}
          <div className="p-3 bg-slate-900 rounded-xl text-slate-200 font-mono text-[11px] overflow-x-auto">
            <div className="text-slate-400 text-[10px] pb-1 border-b border-slate-800 flex items-center justify-between">
              <span>Prepared Interface</span>
              <span>Python 3.14</span>
            </div>
            <pre className="pt-2">
              {isPathForge
                ? `class SearchEngine(ABC):
    @abstractmethod
    def find_path(self, start: str, goal: str, algo="a_star"):
        """Computes optimal study path via A* or BFS."""
        pass`
                : `class RuleEngine(ABC):
    @abstractmethod
    def forward_chain(self, facts: List[str]) -> List[str]:
        """Infers new academic standing from facts."""
        pass`}
            </pre>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-2 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-medium transition-colors"
          >
            Acknowledge & Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default FutureModuleModal;
