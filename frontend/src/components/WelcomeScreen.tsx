import React from 'react';
import {
  Sparkles,
  BookOpen,
  GitBranch,
  ShieldCheck,
  Search,
  ArrowRight,
  BrainCircuit,
  GraduationCap
} from 'lucide-react';

interface WelcomeScreenProps {
  onSelectQuery: (query: string) => void;
}

export const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onSelectQuery }) => {
  const suggestedQueries = [
    {
      title: 'Explain artificial intelligence',
      description: 'Foundational definitions, modern categories, and applications.',
      category: 'Unit I Foundations',
      icon: BrainCircuit,
    },
    {
      title: 'What is breadth-first search?',
      description: 'Queue-based uninformed search, optimality, and time complexity.',
      category: 'Unit II Search',
      icon: Search,
    },
    {
      title: 'How does an expert system work?',
      description: 'Knowledge bases, inference engines, and rule-based architectures.',
      category: 'Unit V Expert Systems',
      icon: BookOpen,
    },
    {
      title: 'Help me prepare for an exam',
      description: 'Strategic AI study preparation guidelines and review approaches.',
      category: 'Study Support',
      icon: GraduationCap,
    },
  ];

  return (
    <div className="max-w-3xl mx-auto py-8 px-4 flex flex-col items-center text-center">
      {/* Badge */}
      <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-brand-50 border border-brand-200/80 text-brand-700 text-xs font-medium mb-6 shadow-2xs">
        <Sparkles className="w-3.5 h-3.5 text-brand-500" />
        <span>Phase 1 — Foundation & Intelligent Agent Architecture</span>
      </div>

      {/* Hero Headline */}
      <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight mb-3">
        Your questions. Clear answers.{' '}
        <span className="text-brand-600 underline decoration-brand-200 underline-offset-4">
          Real reasoning.
        </span>
      </h1>

      <p className="text-sm sm:text-base text-slate-600 max-w-xl mb-8 leading-relaxed">
        Learnify AI helps students explore academic knowledge in Artificial Intelligence and inspect
        how the assistant reaches every conclusion through <strong className="text-slate-800">ProofLens</strong> — our transparent execution trace panel.
      </p>

      {/* Suggested Query Cards */}
      <div className="w-full text-left mb-8">
        <div className="flex items-center justify-between mb-3 px-1">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Suggested Academic Queries
          </span>
          <span className="text-xs text-slate-400">Click to run query</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {suggestedQueries.map((item, idx) => {
            const Icon = item.icon;
            return (
              <button
                key={idx}
                onClick={() => onSelectQuery(item.title)}
                className="group p-4 bg-white hover:bg-brand-50/50 rounded-2xl border border-slate-200/80 hover:border-brand-300 text-left transition-all duration-150 shadow-xs hover:shadow-sm flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 px-2 py-0.5 rounded-md border border-brand-100">
                      {item.category}
                    </span>
                    <Icon className="w-4 h-4 text-slate-400 group-hover:text-brand-600 transition-colors" />
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 group-hover:text-brand-700 transition-colors mb-1">
                    {item.title}
                  </h3>
                  <p className="text-xs text-slate-500 leading-normal">{item.description}</p>
                </div>

                <div className="mt-3 flex items-center text-xs font-medium text-brand-600 opacity-0 group-hover:opacity-100 transition-opacity">
                  <span>Submit query</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-1 transition-transform group-hover:translate-x-0.5" />
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Innovation Pillars Footer Banner */}
      <div className="w-full grid grid-cols-1 sm:grid-cols-3 gap-3 text-left">
        <div className="p-3.5 bg-white rounded-xl border border-slate-200/60 shadow-2xs">
          <div className="flex items-center space-x-2 text-brand-600 mb-1">
            <ShieldCheck className="w-4 h-4" />
            <h4 className="text-xs font-bold text-slate-900">ProofLens</h4>
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            Real backend stage metrics, durations, and verifiable knowledge citations.
          </p>
        </div>

        <div className="p-3.5 bg-white rounded-xl border border-slate-200/60 shadow-2xs">
          <div className="flex items-center space-x-2 text-indigo-600 mb-1">
            <GitBranch className="w-4 h-4" />
            <h4 className="text-xs font-bold text-slate-900">PathForge</h4>
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            Graph-based study navigation & prerequisite route planning (Phase 2).
          </p>
        </div>

        <div className="p-3.5 bg-white rounded-xl border border-slate-200/60 shadow-2xs">
          <div className="flex items-center space-x-2 text-teal-600 mb-1">
            <BookOpen className="w-4 h-4" />
            <h4 className="text-xs font-bold text-slate-900">WhatIf Lab</h4>
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            Rule-based forward & backward chaining academic scenario analyzer (Phase 3).
          </p>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;
