import { Menu, ShieldCheck, Plus, BookOpen, GitBranch } from 'lucide-react';

interface HeaderProps {
  onToggleSidebar: () => void;
  onToggleProofLens: () => void;
  isProofLensOpen: boolean;
  hasTrace: boolean;
  onOpenKnowledge: () => void;
  onNewChat: () => void;
  onOpenPathForge?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  onToggleSidebar,
  onToggleProofLens,
  isProofLensOpen,
  hasTrace,
  onOpenKnowledge,
  onNewChat,
  onOpenPathForge,
}) => {
  return (
    <header className="h-14 border-b border-slate-200/80 bg-white/95 backdrop-blur-xs px-4 flex items-center justify-between z-10 shrink-0">
      {/* Left: Mobile Menu Toggle & Title */}
      <div className="flex items-center space-x-3">
        <button
          onClick={onToggleSidebar}
          className="lg:hidden p-1.5 rounded-lg text-slate-500 hover:text-slate-700 hover:bg-slate-100 transition-colors"
          aria-label="Open sidebar"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-2">
          <span className="text-sm font-bold text-slate-900 tracking-tight">Learnify AI</span>
          <span className="hidden sm:inline-block px-2 py-0.5 rounded text-[10px] font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200">
            Phase 2: Search & Planning
          </span>
        </div>
      </div>

      {/* Right: Quick Actions & ProofLens Toggle */}
      <div className="flex items-center space-x-2">
        {onOpenPathForge && (
          <button
            onClick={onOpenPathForge}
            className="hidden sm:inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200/60 transition-colors"
          >
            <GitBranch className="w-3.5 h-3.5 text-indigo-600" />
            <span>PathForge</span>
          </button>
        )}

        <button
          onClick={onOpenKnowledge}
          className="hidden md:inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-medium text-slate-600 hover:bg-slate-100 transition-colors"
        >
          <BookOpen className="w-3.5 h-3.5" />
          <span>Knowledge</span>
        </button>

        <button
          onClick={onNewChat}
          className="inline-flex items-center space-x-1 px-2.5 py-1.5 rounded-xl text-xs font-medium text-slate-600 hover:bg-slate-100 transition-colors"
          title="Start fresh conversation"
        >
          <Plus className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">New Chat</span>
        </button>

        <button
          onClick={onToggleProofLens}
          className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
            isProofLensOpen
              ? 'bg-brand-600 text-white shadow-xs'
              : 'bg-white hover:bg-brand-50 text-slate-700 hover:text-brand-700 border border-slate-200'
          }`}
          aria-label="Toggle ProofLens panel"
        >
          <ShieldCheck className="w-4 h-4" />
          <span>ProofLens</span>
          {hasTrace && (
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          )}
        </button>
      </div>
    </header>
  );
};

export default Header;
