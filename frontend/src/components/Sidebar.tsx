import React from 'react';
import {
  Brain,
  MessageSquarePlus,
  BookOpen,
  GitBranch,
  FlaskConical,
  GraduationCap,
  Circle,
  X
} from 'lucide-react';

export type ActiveView = 'chat' | 'knowledge' | 'pathforge' | 'whatif' | 'syllabus' | 'learning';

interface SidebarProps {
  activeView: ActiveView;
  onSelectView: (view: ActiveView) => void;
  onNewChat: () => void;
  isOpen: boolean;
  onClose: () => void;
  backendHealthy: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeView,
  onSelectView,
  onNewChat,
  isOpen,
  onClose,
  backendHealthy,
}) => {
  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed lg:static inset-y-0 left-0 z-50 w-72 bg-white border-r border-slate-200/80 flex flex-col transition-transform duration-200 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Brand Header */}
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20">
              <Brain className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-1.5">
                <h1 className="text-base font-bold text-slate-900 tracking-tight">Learnify AI</h1>
                <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-purple-50 text-purple-800 border border-purple-200">
                  Phase 4 Live
                </span>
              </div>
              <p className="text-[11px] text-slate-500">Student AI Assistant</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
            aria-label="Close menu"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Action: New Chat */}
        <div className="p-4">
          <button
            onClick={() => {
              onNewChat();
              onSelectView('chat');
              onClose();
            }}
            className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-medium text-xs shadow-sm shadow-brand-600/20 hover:shadow-md transition-all active:scale-[0.98]"
          >
            <MessageSquarePlus className="w-4 h-4" />
            <span>New Chat Session</span>
          </button>
        </div>

        {/* Navigation Sections */}
        <nav className="flex-1 px-3 py-2 space-y-1 overflow-y-auto">
          <div className="px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Workspace Modules
          </div>

          <button
            onClick={() => {
              onSelectView('chat');
              onClose();
            }}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeView === 'chat'
                ? 'bg-brand-50 text-brand-700 font-semibold'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <Brain className="w-4 h-4 text-brand-600" />
            <span>AI Chat Assistant</span>
          </button>

          <button
            onClick={() => {
              onSelectView('pathforge');
              onClose();
            }}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeView === 'pathforge'
                ? 'bg-indigo-50 text-indigo-700 font-semibold'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <GitBranch className="w-4 h-4 text-indigo-600" />
            <div className="flex-1 text-left flex items-center justify-between">
              <span>PathForge</span>
              <span className="text-[9px] px-1.5 py-0.5 rounded bg-indigo-100 text-indigo-800 font-bold">
                Phase 2
              </span>
            </div>
          </button>

          <button
            onClick={() => {
              onSelectView('whatif');
              onClose();
            }}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeView === 'whatif'
                ? 'bg-teal-50 text-teal-800 font-semibold'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <FlaskConical className="w-4 h-4 text-teal-600" />
            <div className="flex-1 text-left flex items-center justify-between">
              <span>WhatIf Lab</span>
              <span className="text-[9px] px-1.5 py-0.5 rounded bg-teal-100 text-teal-800 font-bold">
                Phase 3
              </span>
            </div>
          </button>

          <button
            onClick={() => {
              onSelectView('learning');
              onClose();
            }}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeView === 'learning'
                ? 'bg-purple-50 text-purple-800 font-semibold'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <Brain className="w-4 h-4 text-purple-600" />
            <div className="flex-1 text-left flex items-center justify-between">
              <span>Learning Lab</span>
              <span className="text-[9px] px-1.5 py-0.5 rounded bg-purple-100 text-purple-800 font-bold">
                Phase 4 Live
              </span>
            </div>
          </button>

          <button
            onClick={() => {
              onSelectView('knowledge');
              onClose();
            }}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeView === 'knowledge'
                ? 'bg-brand-50 text-brand-700 font-semibold'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <BookOpen className="w-4 h-4 text-slate-500" />
            <div className="flex-1 text-left flex items-center justify-between">
              <span>Knowledge Explorer</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-slate-100 text-slate-600 font-normal">
                25+ Records
              </span>
            </div>
          </button>

          <div className="pt-4 px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Academic Attribution
          </div>

          <button
            onClick={() => {
              onSelectView('syllabus');
              onClose();
            }}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeView === 'syllabus'
                ? 'bg-brand-50 text-brand-700 font-semibold'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <GraduationCap className="w-4 h-4 text-slate-500" />
            <div className="flex-1 text-left flex items-center justify-between">
              <span>Syllabus & Team</span>
              <span className="text-[9px] px-1.5 py-0.5 rounded bg-amber-50 text-amber-700 font-semibold">
                5 Units Complete
              </span>
            </div>
          </button>
        </nav>

        {/* Footer: Connection & Developer Info */}
        <div className="p-4 border-t border-slate-100 bg-slate-50/60 space-y-2">
          {/* Connection Status */}
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-500 text-[11px]">Backend API</span>
            <div className="flex items-center space-x-1.5">
              <Circle
                className={`w-2 h-2 fill-current ${
                  backendHealthy ? 'text-emerald-500 animate-pulse' : 'text-rose-500'
                }`}
              />
              <span
                className={`text-[11px] font-medium ${
                  backendHealthy ? 'text-emerald-700' : 'text-rose-600'
                }`}
              >
                {backendHealthy ? 'FastAPI 8000' : 'Disconnected'}
              </span>
            </div>
          </div>

          {/* Responsible Developers: Phase 4, Phase 3, Phase 2 & Phase 1 */}
          <div className="space-y-1.5 max-h-48 overflow-y-auto pr-0.5">
            <div className="p-2 rounded-xl bg-white border border-purple-300 shadow-2xs">
              <div className="flex items-center space-x-2 mb-0.5">
                <div className="w-5 h-5 rounded-md bg-purple-100 text-purple-800 flex items-center justify-center text-[10px] font-bold">
                  N
                </div>
                <div className="min-w-0">
                  <span className="text-xs font-bold text-slate-900 block truncate">
                    Naveen Kumar
                  </span>
                  <span className="text-[10px] text-purple-700 block font-mono">
                    URK25CS1016
                  </span>
                </div>
              </div>
              <p className="text-[10px] text-slate-500 leading-tight">
                Phase 4 Lead: Learning Engine & Expert Systems
              </p>
            </div>

            <div className="p-2 rounded-xl bg-white/90 border border-teal-300/80 shadow-2xs">
              <div className="flex items-center space-x-2 mb-0.5">
                <div className="w-5 h-5 rounded-md bg-teal-100 text-teal-800 flex items-center justify-center text-[10px] font-bold">
                  H
                </div>
                <div className="min-w-0">
                  <span className="text-xs font-bold text-slate-900 block truncate">
                    Hiran Antony R
                  </span>
                  <span className="text-[10px] text-teal-700 block font-mono">
                    URK25CS1034
                  </span>
                </div>
              </div>
              <p className="text-[10px] text-slate-500 leading-tight">
                Phase 3 Lead: Logic, Reasoning & WhatIf Lab
              </p>
            </div>

            <div className="p-2 rounded-xl bg-white/80 border border-indigo-200/80 shadow-2xs">
              <div className="flex items-center space-x-2 mb-0.5">
                <div className="w-5 h-5 rounded-md bg-indigo-100 text-indigo-700 flex items-center justify-center text-[10px] font-bold">
                  Y
                </div>
                <div className="min-w-0">
                  <span className="text-xs font-bold text-slate-900 block truncate">
                    Yogith Joy J
                  </span>
                  <span className="text-[10px] text-indigo-600 block font-mono">
                    URK25CS1063
                  </span>
                </div>
              </div>
              <p className="text-[10px] text-slate-500 leading-tight">
                Phase 2 Lead: PathForge & Search Algorithms
              </p>
            </div>

            <div className="p-2 rounded-xl bg-white/70 border border-slate-200/70 shadow-2xs">
              <div className="flex items-center space-x-2 mb-0.5">
                <div className="w-5 h-5 rounded-md bg-brand-100 text-brand-700 flex items-center justify-center text-[10px] font-bold">
                  R
                </div>
                <div className="min-w-0">
                  <span className="text-xs font-bold text-slate-900 block truncate">
                    Rufus Samuel R
                  </span>
                  <span className="text-[10px] text-slate-400 block font-mono">
                    URK25CS1090
                  </span>
                </div>
              </div>
              <p className="text-[10px] text-slate-500 leading-tight">
                Phase 1 Lead: Foundation, Agent & ProofLens
              </p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
