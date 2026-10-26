import { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar, { ActiveView } from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import ProofLensPanel from './components/ProofLensPanel';
import KnowledgeExplorerModal from './components/KnowledgeExplorerModal';
import SyllabusModal from './components/SyllabusModal';
import FutureModuleModal from './components/FutureModuleModal';
import PathForgeView from './components/PathForgeView';
import WhatIfLabView from './components/WhatIfLabView';
import LearningLabView from './components/LearningLabView';
import { Message } from './types';
import { checkHealth } from './services/api';

export function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome-1',
      role: 'assistant',
      content:
        "Hello! I'm Learnify AI, your unified intelligent academic assistant for Artificial Intelligence (Phase 4). I integrate classical AI search in PathForge, logical reasoning & counterfactual analysis in WhatIf Lab, and a continuous learning engine with inductive ML intent classification, verified rote memory, human advice evaluation, and case-based analogy in Learning Lab. Every execution is transparently audited in ProofLens. What would you like to explore today?",
      timestamp: new Date(),
      conceptsUsed: ['Simple Reflex Agent', 'Problem Spaces & Search', 'First-Order Logic & Rules', 'Inductive ML & Rote Learning'],
      matchScore: 1.0,
      sources: [
        {
          id: 'src-coursework',
          name: 'Learnify AI Course Materials',
          description: 'System Welcome & Orientation',
        },
      ],
      trace: [
        {
          id: 'step-1',
          stage: 'Session Initialization',
          method: 'Simple Reflex Welcome Dispatch',
          description: 'Initialized conversational session and loaded Unit I & Unit II curriculum context.',
          status: 'completed',
          input_summary: 'Application start',
          output_summary: 'Orientation message prepared with Unit I-V capabilities',
          evidence_ids: [],
          duration_ms: 0.15,
          execution_type: 'reflex',
        },
      ],
      status: 'greeting',
      suggestions: [
        'How do I start learning machine learning?',
        'What should I learn before neural networks?',
        'Show me the prerequisites for Bayesian reasoning',
        'What is breadth-first search?',
      ],
    },
  ]);

  const [activeMessage, setActiveMessage] = useState<Message | null>(messages[0]);
  const [activeView, setActiveView] = useState<ActiveView>('chat');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isProofLensOpen, setIsProofLensOpen] = useState(true);
  const [backendHealthy, setBackendHealthy] = useState(true);

  // Modals and PathForge state
  const [isKnowledgeOpen, setIsKnowledgeOpen] = useState(false);
  const [isSyllabusOpen, setIsSyllabusOpen] = useState(false);
  const [futureModule, setFutureModule] = useState<'whatif' | null>(null);
  const [pendingQuery, setPendingQuery] = useState<string | null>(null);
  const [pathForgeGoalId, setPathForgeGoalId] = useState<string | null>(null);

  // Health check on mount and interval
  useEffect(() => {
    const verifyHealth = async () => {
      try {
        const res = await checkHealth();
        setBackendHealthy(res.status === 'healthy');
      } catch {
        setBackendHealthy(false);
      }
    };

    verifyHealth();
    const interval = setInterval(verifyHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleSelectView = (view: ActiveView) => {
    setActiveView(view);
    if (view === 'knowledge') {
      setIsKnowledgeOpen(true);
    } else if (view === 'pathforge') {
      setActiveView('pathforge');
    } else if (view === 'whatif') {
      setActiveView('whatif');
    } else if (view === 'learning') {
      setActiveView('learning');
    } else if (view === 'syllabus') {
      setIsSyllabusOpen(true);
    }
  };

  const handleNewChat = () => {
    const freshWelcome: Message = {
      id: `welcome-${Date.now()}`,
      role: 'assistant',
      content:
        "Started a fresh conversation. What topic in Artificial Intelligence would you like to study?",
      timestamp: new Date(),
      conceptsUsed: ['Simple Reflex Agent'],
      matchScore: 1.0,
      sources: [
        {
          id: 'src-coursework',
          name: 'Learnify AI Course Materials',
          description: 'Session reset',
        },
      ],
      trace: [
        {
          id: 'step-1',
          stage: 'Session Reset',
          method: 'Reflex State Clearing',
          description: 'Cleared conversation turn history while keeping core knowledge references active.',
          status: 'completed',
          duration_ms: 0.1,
          evidence_ids: [],
          execution_type: 'reflex',
        },
      ],
      status: 'greeting',
      suggestions: [
        'What is artificial intelligence?',
        'What is breadth-first search?',
        'What are the types of intelligent agents?',
      ],
    };

    setMessages([freshWelcome]);
    setActiveMessage(freshWelcome);
  };

  const handleOpenPathForge = (goalId?: string) => {
    if (goalId) {
      setPathForgeGoalId(goalId);
    }
    setActiveView('pathforge');
  };

  const handleOpenWhatIf = () => {
    setActiveView('whatif');
  };

  const handleAskFromKnowledge = (question: string) => {
    setPendingQuery(question);
    setActiveView('chat');
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 font-sans antialiased text-slate-900">
      {/* 1. Left Sidebar Navigation */}
      <Sidebar
        activeView={activeView}
        onSelectView={handleSelectView}
        onNewChat={handleNewChat}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        backendHealthy={backendHealthy}
      />

      {/* 2. Main Middle Workspace */}
      <div className="flex-1 flex flex-col min-w-0 h-full overflow-hidden">
        {/* Top Header */}
        <Header
          onToggleSidebar={() => setIsSidebarOpen((prev) => !prev)}
          onToggleProofLens={() => setIsProofLensOpen((prev) => !prev)}
          isProofLensOpen={isProofLensOpen}
          hasTrace={Boolean(activeMessage?.trace && activeMessage.trace.length > 0)}
          onOpenKnowledge={() => setIsKnowledgeOpen(true)}
          onNewChat={handleNewChat}
          onOpenPathForge={() => handleOpenPathForge()}
          onOpenWhatIf={handleOpenWhatIf}
          onOpenLearning={() => setActiveView('learning')}
        />

        {/* Center Workspace: Chat, PathForge, WhatIf Lab, or Learning Lab */}
        <div className="flex-1 flex overflow-hidden">
          {activeView === 'learning' ? (
            <LearningLabView
              onBackToChat={() => setActiveView('chat')}
              onAskQuestion={(q) => {
                setPendingQuery(q);
                setActiveView('chat');
              }}
            />
          ) : activeView === 'whatif' ? (
            <WhatIfLabView
              onBackToChat={() => setActiveView('chat')}
              onSyncTraceToProofLens={(syntheticMsg) => {
                setActiveMessage(syntheticMsg);
                setIsProofLensOpen(true);
              }}
            />
          ) : activeView === 'pathforge' ? (
            <PathForgeView
              onBackToChat={() => setActiveView('chat')}
              onSyncTraceToProofLens={(syntheticMsg) => {
                setActiveMessage(syntheticMsg);
                setIsProofLensOpen(true);
              }}
              initialGoalTopicId={pathForgeGoalId}
            />
          ) : (
            <ChatInterface
              messages={messages}
              setMessages={setMessages}
              activeMessage={activeMessage}
              setActiveMessage={setActiveMessage}
              onOpenProofLens={() => setIsProofLensOpen(true)}
              externalQuery={pendingQuery}
              onClearExternalQuery={() => setPendingQuery(null)}
            />
          )}

          {/* 3. Right Desktop ProofLens Panel */}
          {isProofLensOpen && (
            <div className="hidden lg:block w-96 shrink-0 h-full">
              <ProofLensPanel
                activeMessage={activeMessage}
                onClose={() => setIsProofLensOpen(false)}
              />
            </div>
          )}
        </div>
      </div>

      {/* Mobile / Tablet Slide-out Drawer for ProofLens */}
      {isProofLensOpen && (
        <div className="fixed inset-0 z-50 lg:hidden flex justify-end">
          <div
            className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs"
            onClick={() => setIsProofLensOpen(false)}
          />
          <div className="relative w-full max-w-md h-full bg-white shadow-2xl z-10">
            <ProofLensPanel
              activeMessage={activeMessage}
              onClose={() => setIsProofLensOpen(false)}
            />
          </div>
        </div>
      )}

      {/* 4. Modals */}
      <KnowledgeExplorerModal
        isOpen={isKnowledgeOpen}
        onClose={() => {
          setIsKnowledgeOpen(false);
          setActiveView('chat');
        }}
        onAskQuestion={(q) => {
          handleAskFromKnowledge(q);
          setIsKnowledgeOpen(false);
          setActiveView('chat');
        }}
      />

      <SyllabusModal
        isOpen={isSyllabusOpen}
        onClose={() => {
          setIsSyllabusOpen(false);
          setActiveView('chat');
        }}
      />

      <FutureModuleModal
        module={futureModule}
        onClose={() => {
          setFutureModule(null);
          setActiveView('chat');
        }}
      />
    </div>
  );
}

export default App;
