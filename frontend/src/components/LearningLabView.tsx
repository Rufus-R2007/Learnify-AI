import React, { useState, useEffect } from 'react';
import {
  Brain,
  Sparkles,
  Zap,
  CheckCircle2,
  XCircle,
  Clock,
  Database,
  ArrowRight,
  RefreshCw,
  Search,
  BookOpen,
  Layers,
  BarChart3,
  ThumbsUp,
  ThumbsDown,
  Cpu
} from 'lucide-react';
import {
  getMemoryStats,
  getMemoryItems,
  invalidateMemory,
  getFeedbackList,
  reviewFeedback,
  getKnowledgeHistory,
  getMLMetrics,
  predictIntent,
  getCurriculumAnalogies,
} from '../services/api';
import {
  MemoryStatsResponse,
  MemoryItem,
  FeedbackItem,
  KnowledgeHistoryItem,
  MLMetricsResponse,
  RelatedCase,
} from '../types';

interface LearningLabViewProps {
  onBackToChat: () => void;
  onAskQuestion?: (query: string) => void;
}

type TabType = 'advice' | 'rote' | 'inductive' | 'analogy' | 'architecture';

export const LearningLabView: React.FC<LearningLabViewProps> = ({
  onBackToChat,
  onAskQuestion,
}) => {
  const [activeTab, setActiveTab] = useState<TabType>('advice');

  // --- Concept 1 State (Rote Learning) ---
  const [memoryStats, setMemoryStats] = useState<MemoryStatsResponse | null>(null);
  const [memoryItems, setMemoryItems] = useState<MemoryItem[]>([]);
  const [loadingMemory, setLoadingMemory] = useState(false);
  const [invalidating, setInvalidating] = useState(false);

  // --- Concept 2 State (Learning by Taking Advice) ---
  const [feedbacks, setFeedbacks] = useState<FeedbackItem[]>([]);
  const [selectedFeedback, setSelectedFeedback] = useState<FeedbackItem | null>(null);
  const [feedbackFilter, setFeedbackFilter] = useState<string>('ALL');
  const [reviewerNotes, setReviewerNotes] = useState('Verified correct by faculty reviewer Naveen Kumar.');
  const [updateKnowledgeCheck, setUpdateKnowledgeCheck] = useState(true);
  const [reviewing, setReviewing] = useState(false);
  const [reviewMessage, setReviewMessage] = useState<string | null>(null);
  const [historyItems, setHistoryItems] = useState<KnowledgeHistoryItem[]>([]);

  // --- Concept 3 State (Inductive Learning) ---
  const [mlMetrics, setMlMetrics] = useState<MLMetricsResponse | null>(null);
  const [sandboxQuery, setSandboxQuery] = useState('What are the prerequisites for learning Bayesian networks?');
  const [sandboxResult, setSandboxResult] = useState<{
    predicted_category: string;
    confidence: number;
    is_uncertain: boolean;
    class_probabilities: Record<string, number>;
  } | null>(null);
  const [classifying, setClassifying] = useState(false);

  // --- Concept 4 State (Analogy) ---
  const [analogyQuery, setAnalogyQuery] = useState('How does heuristic evaluation guide search?');
  const [analogyResults, setAnalogyResults] = useState<RelatedCase[]>([]);
  const [searchingAnalogy, setSearchingAnalogy] = useState(false);

  // Load Initial Data
  useEffect(() => {
    loadMemoryData();
    loadFeedbackData();
    loadHistoryData();
    loadMLMetricsData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadMemoryData = async () => {
    try {
      setLoadingMemory(true);
      const [stats, items] = await Promise.all([getMemoryStats(), getMemoryItems(30)]);
      setMemoryStats(stats);
      setMemoryItems(items);
    } catch (e) {
      console.error('Failed to load memory data', e);
    } finally {
      setLoadingMemory(false);
    }
  };

  const loadFeedbackData = async () => {
    try {
      const list = await getFeedbackList();
      setFeedbacks(list);
      if (list.length > 0 && !selectedFeedback) {
        setSelectedFeedback(list[0]);
      }
    } catch (e) {
      console.error('Failed to load feedback list', e);
    }
  };

  const loadHistoryData = async () => {
    try {
      const history = await getKnowledgeHistory();
      setHistoryItems(history);
    } catch (e) {
      console.error('Failed to load history', e);
    }
  };

  const loadMLMetricsData = async () => {
    try {
      const metrics = await getMLMetrics();
      setMlMetrics(metrics);
    } catch (e) {
      console.error('Failed to load ML metrics', e);
    }
  };

  const handleInvalidateMemory = async () => {
    try {
      setInvalidating(true);
      await invalidateMemory();
      await loadMemoryData();
    } catch (e) {
      console.error('Failed to invalidate memory', e);
    } finally {
      setInvalidating(false);
    }
  };

  const handleReview = async (decision: 'APPROVED' | 'REJECTED') => {
    if (!selectedFeedback) return;
    try {
      setReviewing(true);
      setReviewMessage(null);
      const res = await reviewFeedback(selectedFeedback.id, {
        decision,
        reviewer_notes: reviewerNotes,
        update_knowledge: updateKnowledgeCheck,
      });
      setReviewMessage(res.message);
      await loadFeedbackData();
      await loadHistoryData();
      await loadMemoryData();
    } catch (e) {
      setReviewMessage(e instanceof Error ? e.message : 'Review action failed');
    } finally {
      setReviewing(false);
    }
  };

  const handleRunIntentSandbox = async () => {
    if (!sandboxQuery.trim()) return;
    try {
      setClassifying(true);
      const res = await predictIntent(sandboxQuery.trim());
      setSandboxResult(res);
    } catch (e) {
      console.error('Classification failed', e);
    } finally {
      setClassifying(false);
    }
  };

  const handleRunAnalogySearch = async () => {
    if (!analogyQuery.trim()) return;
    try {
      setSearchingAnalogy(true);
      const matches = await getCurriculumAnalogies(analogyQuery.trim(), 4);
      setAnalogyResults(matches);
    } catch (e) {
      console.error('Analogy search failed', e);
    } finally {
      setSearchingAnalogy(false);
    }
  };

  const filteredFeedbacks = feedbacks.filter((f) => {
    if (feedbackFilter === 'ALL') return true;
    return f.status === feedbackFilter;
  });

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-50 overflow-hidden font-sans">
      {/* Top Header */}
      <div className="bg-white border-b border-slate-200 px-6 py-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-lg font-bold text-slate-900 tracking-tight">
                Learning & Quality Assurance Lab
              </h1>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200">
                Unit V • Phase 4 Live
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Machine Learning, Expert Systems & Continuous Improvement (Lead: Naveen Kumar — URK25CS1016)
            </p>
          </div>
        </div>

        <button
          onClick={onBackToChat}
          className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 shadow-2xs transition-all"
        >
          <span>Return to Chat</span>
          <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
        </button>
      </div>

      {/* Concept Navigation Bar */}
      <div className="bg-white border-b border-slate-200 px-6 flex space-x-1 overflow-x-auto">
        <button
          onClick={() => setActiveTab('advice')}
          className={`py-3 px-4 text-xs font-medium border-b-2 flex items-center space-x-2 transition-all ${
            activeTab === 'advice'
              ? 'border-purple-600 text-purple-700 font-bold'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <ThumbsUp className="w-3.5 h-3.5" />
          <span>Taking Advice (Reviewer Desk)</span>
          {feedbacks.filter((f) => f.status === 'PENDING').length > 0 && (
            <span className="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800">
              {feedbacks.filter((f) => f.status === 'PENDING').length}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('rote')}
          className={`py-3 px-4 text-xs font-medium border-b-2 flex items-center space-x-2 transition-all ${
            activeTab === 'rote'
              ? 'border-purple-600 text-purple-700 font-bold'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Zap className="w-3.5 h-3.5" />
          <span>Rote Learning (Memory Cache)</span>
          {memoryStats && (
            <span className="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
              {memoryStats.valid_entries} cached
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveTab('inductive')}
          className={`py-3 px-4 text-xs font-medium border-b-2 flex items-center space-x-2 transition-all ${
            activeTab === 'inductive'
              ? 'border-purple-600 text-purple-700 font-bold'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <BarChart3 className="w-3.5 h-3.5" />
          <span>Inductive ML (Intent Classifier)</span>
          <span className="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-indigo-100 text-indigo-800">
            85.7% Acc
          </span>
        </button>

        <button
          onClick={() => setActiveTab('analogy')}
          className={`py-3 px-4 text-xs font-medium border-b-2 flex items-center space-x-2 transition-all ${
            activeTab === 'analogy'
              ? 'border-purple-600 text-purple-700 font-bold'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" />
          <span>Analogy (Case-Based Reasoning)</span>
        </button>

        <button
          onClick={() => setActiveTab('architecture')}
          className={`py-3 px-4 text-xs font-medium border-b-2 flex items-center space-x-2 transition-all ${
            activeTab === 'architecture'
              ? 'border-purple-600 text-purple-700 font-bold'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>Expert System Synthesis</span>
        </button>
      </div>

      {/* Main Tab Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* ========================================================================= */}
        {/* TAB 1: LEARNING BY TAKING ADVICE (CONCEPT 2) */}
        {/* ========================================================================= */}
        {activeTab === 'advice' && (
          <div className="max-w-6xl mx-auto space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-base font-bold text-slate-900">
                    Concept 2: Learning by Taking Advice & Human-in-the-Loop Review
                  </h2>
                  <p className="text-xs text-slate-500 mt-1 max-w-3xl leading-relaxed">
                    Student feedback and suggested corrections enter a staging workflow. An authorized evaluator reviews proposed knowledge changes. Upon approval, the authoritative curriculum database is updated, an immutable audit log is created, and stale rote cache entries are invalidated.
                  </p>
                </div>
                <button
                  onClick={loadFeedbackData}
                  className="p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
                  title="Refresh feedback list"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>

              {/* Status Filter Buttons */}
              <div className="flex items-center space-x-2 mt-4 pt-3 border-t border-slate-100">
                <span className="text-xs font-semibold text-slate-500">Filter Status:</span>
                {(['ALL', 'PENDING', 'APPROVED', 'REJECTED'] as const).map((st) => (
                  <button
                    key={st}
                    onClick={() => setFeedbackFilter(st)}
                    className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                      feedbackFilter === st
                        ? 'bg-purple-600 text-white shadow-2xs'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {st}
                  </button>
                ))}
              </div>
            </div>

            {/* Split Desk: Left List, Right Inspector */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Feedback List (5 cols) */}
              <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-200/80 overflow-hidden shadow-xs flex flex-col h-[520px]">
                <div className="p-3.5 bg-slate-50/70 border-b border-slate-200/80 flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    Submissions ({filteredFeedbacks.length})
                  </span>
                </div>
                <div className="flex-1 overflow-y-auto divide-y divide-slate-100">
                  {filteredFeedbacks.length === 0 ? (
                    <div className="p-8 text-center text-slate-400 text-xs">
                      No feedback submissions found matching filter.
                    </div>
                  ) : (
                    filteredFeedbacks.map((item) => (
                      <button
                        key={item.id}
                        onClick={() => {
                          setSelectedFeedback(item);
                          setReviewMessage(null);
                        }}
                        className={`w-full p-4 text-left transition-all hover:bg-slate-50 ${
                          selectedFeedback?.id === item.id ? 'bg-purple-50/70 border-l-4 border-purple-600' : ''
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span
                            className={`inline-flex items-center text-[10px] font-bold px-2 py-0.5 rounded-full ${
                              item.status === 'APPROVED'
                                ? 'bg-emerald-100 text-emerald-800'
                                : item.status === 'REJECTED'
                                ? 'bg-rose-100 text-rose-800'
                                : 'bg-amber-100 text-amber-800'
                            }`}
                          >
                            {item.status}
                          </span>
                          <span className="text-[10px] text-slate-400">
                            {new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </span>
                        </div>
                        <p className="text-xs font-semibold text-slate-800 truncate mb-1">
                          {item.query}
                        </p>
                        <div className="flex items-center space-x-1 text-[11px] text-slate-500">
                          {item.feedback_type === 'helpful' ? (
                            <ThumbsUp className="w-3 h-3 text-emerald-600" />
                          ) : (
                            <ThumbsDown className="w-3 h-3 text-amber-600" />
                          )}
                          <span className="truncate">
                            {item.suggested_correction ? 'Has suggested correction' : 'Rating only'}
                          </span>
                        </div>
                      </button>
                    ))
                  )}
                </div>
              </div>

              {/* Inspector & Review Desk (7 cols) */}
              <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs flex flex-col justify-between">
                {selectedFeedback ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                      <div>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-purple-600">
                          Advice Submission Review
                        </span>
                        <h3 className="text-sm font-bold text-slate-900 mt-0.5">
                          {selectedFeedback.query}
                        </h3>
                      </div>
                      <span className="text-xs font-mono text-slate-400">
                        {selectedFeedback.id}
                      </span>
                    </div>

                    {/* Original Answer Preview */}
                    <div>
                      <span className="text-[11px] font-semibold text-slate-500 block mb-1">
                        Original Bot Response:
                      </span>
                      <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/70 text-xs text-slate-700 max-h-24 overflow-y-auto">
                        {selectedFeedback.original_answer}
                      </div>
                    </div>

                    {/* Suggested Correction */}
                    <div>
                      <span className="text-[11px] font-semibold text-slate-500 block mb-1">
                        Suggested Advice / Correction:
                      </span>
                      {selectedFeedback.suggested_correction ? (
                        <div className="p-3 bg-purple-50/60 rounded-xl border border-purple-200 text-xs text-purple-900 max-h-36 overflow-y-auto font-medium">
                          {selectedFeedback.suggested_correction}
                        </div>
                      ) : (
                        <p className="text-xs text-slate-400 italic">No text correction suggested.</p>
                      )}
                    </div>

                    {/* Review Controls */}
                    <div className="pt-3 border-t border-slate-100 space-y-3">
                      <div>
                        <label className="text-[11px] font-semibold text-slate-600 block mb-1">
                          Reviewer Assessment Notes:
                        </label>
                        <input
                          type="text"
                          value={reviewerNotes}
                          onChange={(e) => setReviewerNotes(e.target.value)}
                          className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-purple-500"
                          placeholder="Reason for approval/rejection..."
                        />
                      </div>

                      <div className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          id="updateKbCheck"
                          checked={updateKnowledgeCheck}
                          onChange={(e) => setUpdateKnowledgeCheck(e.target.checked)}
                          className="rounded border-slate-300 text-purple-600 focus:ring-purple-500"
                        />
                        <label htmlFor="updateKbCheck" className="text-xs font-medium text-slate-700">
                          Automatically update authoritative knowledge base and invalidate affected memory cache upon approval
                        </label>
                      </div>

                      {reviewMessage && (
                        <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-800">
                          {reviewMessage}
                        </div>
                      )}

                      <div className="flex items-center space-x-3 pt-2">
                        <button
                          disabled={reviewing || selectedFeedback.status === 'APPROVED'}
                          onClick={() => handleReview('APPROVED')}
                          className="flex-1 py-2 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-semibold text-xs shadow-xs transition-all flex items-center justify-center space-x-1.5"
                        >
                          <CheckCircle2 className="w-4 h-4" />
                          <span>Approve Advice & Update KB</span>
                        </button>
                        <button
                          disabled={reviewing || selectedFeedback.status === 'REJECTED'}
                          onClick={() => handleReview('REJECTED')}
                          className="py-2 px-4 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-700 text-slate-700 font-semibold text-xs border border-slate-200 transition-all flex items-center justify-center space-x-1.5"
                        >
                          <XCircle className="w-4 h-4" />
                          <span>Reject Advice</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="p-12 text-center text-slate-400 text-xs">
                    Select a submission from the list on the left.
                  </div>
                )}
              </div>
            </div>

            {/* Knowledge Update Audit History */}
            <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
                Immutable Knowledge Audit Provenance ({historyItems.length})
              </h3>
              {historyItems.length === 0 ? (
                <p className="text-xs text-slate-400">No knowledge modifications recorded yet.</p>
              ) : (
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {historyItems.map((h) => (
                    <div key={h.id} className="p-3 rounded-xl bg-slate-50 border border-slate-200/70 text-xs">
                      <div className="flex items-center justify-between text-[11px] text-slate-500 mb-1">
                        <span className="font-mono font-bold text-purple-700">Record: {h.knowledge_id}</span>
                        <span>{new Date(h.updated_at).toLocaleString()}</span>
                      </div>
                      <p className="text-slate-800 text-[11px] font-medium truncate">
                        <span className="text-emerald-700 font-bold">New:</span> {h.new_content}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 2: ROTE LEARNING (CONCEPT 1) */}
        {/* ========================================================================= */}
        {activeTab === 'rote' && (
          <div className="max-w-6xl mx-auto space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs flex items-start justify-between">
              <div>
                <h2 className="text-base font-bold text-slate-900">
                  Concept 1: Rote Learning (Verified Solution Memory Cache)
                </h2>
                <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
                  Frequently verified student queries are retained in high-speed SQLite solution memory. Repeated queries retrieve cached solutions with measured latency under 1ms, eliminating redundant inference while strictly guarding against caching individualized or private student data.
                </p>
              </div>

              <button
                disabled={invalidating}
                onClick={handleInvalidateMemory}
                className="py-2 px-3.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 text-xs font-semibold shadow-2xs transition-all flex items-center space-x-1.5"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${invalidating ? 'animate-spin' : ''}`} />
                <span>Invalidate All Memory</span>
              </button>
            </div>

            {/* Quick Metrics */}
            {memoryStats && (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="bg-white rounded-xl p-4 border border-slate-200/80 shadow-xs text-center">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Total Cached Queries
                  </span>
                  <span className="text-2xl font-bold text-slate-900 mt-1 block">
                    {memoryStats.total_cached_queries}
                  </span>
                </div>
                <div className="bg-white rounded-xl p-4 border border-slate-200/80 shadow-xs text-center">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Valid Live Entries
                  </span>
                  <span className="text-2xl font-bold text-emerald-600 mt-1 block">
                    {memoryStats.valid_entries}
                  </span>
                </div>
                <div className="bg-white rounded-xl p-4 border border-slate-200/80 shadow-xs text-center">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Total Cache Hits
                  </span>
                  <span className="text-2xl font-bold text-purple-600 mt-1 block">
                    {memoryStats.total_hits}
                  </span>
                </div>
                <div className="bg-white rounded-xl p-4 border border-slate-200/80 shadow-xs text-center">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Typical Hit Latency
                  </span>
                  <span className="text-2xl font-bold text-teal-600 mt-1 block font-mono">
                    &lt; 1 ms
                  </span>
                </div>
              </div>
            )}

            {/* Live Cache Table */}
            <div className="bg-white rounded-2xl border border-slate-200/80 overflow-hidden shadow-xs">
              <div className="p-4 bg-slate-50/70 border-b border-slate-200 flex items-center justify-between">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                  Verified Memory Cache Items ({memoryItems.length})
                </h3>
                <button
                  onClick={loadMemoryData}
                  className="text-xs text-purple-600 hover:text-purple-800 font-semibold"
                >
                  Refresh
                </button>
              </div>

              {loadingMemory ? (
                <div className="p-8 text-center text-slate-400 text-xs">Loading memory table...</div>
              ) : memoryItems.length === 0 ? (
                <div className="p-8 text-center text-slate-400 text-xs">
                  Memory cache is empty. Ask queries in the chatbot to populate rote memory!
                </div>
              ) : (
                <div className="divide-y divide-slate-100 max-h-96 overflow-y-auto">
                  {memoryItems.map((item) => (
                    <div key={item.id} className="p-4 flex items-center justify-between hover:bg-slate-50/60">
                      <div className="min-w-0 pr-4">
                        <div className="flex items-center space-x-2 mb-1">
                          <span
                            className={`px-1.5 py-0.2 rounded text-[10px] font-bold ${
                              item.is_valid
                                ? 'bg-emerald-100 text-emerald-800'
                                : 'bg-slate-200 text-slate-600 line-through'
                            }`}
                          >
                            {item.is_valid ? 'LIVE' : 'INVALIDATED'}
                          </span>
                          <span className="text-xs font-bold text-slate-900 truncate">
                            {item.normalized_query}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-500 truncate max-w-xl">
                          {item.answer_text}
                        </p>
                      </div>

                      <div className="flex items-center space-x-4 shrink-0 text-right">
                        <div>
                          <span className="text-[10px] uppercase font-semibold text-slate-400 block">Hits</span>
                          <span className="text-xs font-mono font-bold text-purple-700">{item.hit_count}</span>
                        </div>
                        {onAskQuestion && item.is_valid === 1 && (
                          <button
                            onClick={() => onAskQuestion(item.normalized_query)}
                            className="px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-purple-50 text-purple-700 hover:bg-purple-100 transition-all"
                          >
                            Test Query
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 3: INDUCTIVE LEARNING (CONCEPT 3) */}
        {/* ========================================================================= */}
        {activeTab === 'inductive' && (
          <div className="max-w-6xl mx-auto space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
              <h2 className="text-base font-bold text-slate-900">
                Concept 3: Inductive Learning (scikit-learn Intent Classifier)
              </h2>
              <p className="text-xs text-slate-500 mt-1 max-w-3xl leading-relaxed">
                A supervised machine learning model (TF-IDF Vectorizer + Logistic Regression) trained on 175 original student curriculum queries across 7 distinct categories. Evaluated on a strictly held-out test split, reporting actual measured test accuracy, precision, recall, and confusion matrix.
              </p>
            </div>

            {/* Measured Metrics Cards */}
            {mlMetrics && (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="bg-white rounded-xl p-4 border border-slate-200/80 shadow-xs text-center">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Held-Out Test Accuracy
                  </span>
                  <span className="text-2xl font-bold text-indigo-600 mt-1 block">
                    {(mlMetrics.accuracy * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="bg-white rounded-xl p-4 border border-slate-200/80 shadow-xs text-center">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Macro F1-Score
                  </span>
                  <span className="text-2xl font-bold text-purple-600 mt-1 block font-mono">
                    {mlMetrics.macro_f1.toFixed(4)}
                  </span>
                </div>
                <div className="bg-white rounded-xl p-4 border border-slate-200/80 shadow-xs text-center">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Macro Precision
                  </span>
                  <span className="text-2xl font-bold text-teal-600 mt-1 block font-mono">
                    {mlMetrics.macro_precision.toFixed(4)}
                  </span>
                </div>
                <div className="bg-white rounded-xl p-4 border border-slate-200/80 shadow-xs text-center">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Dataset Split
                  </span>
                  <span className="text-xs font-semibold text-slate-700 mt-2 block">
                    {mlMetrics.training_samples} Train / {mlMetrics.test_samples} Test
                  </span>
                </div>
              </div>
            )}

            {/* Live Intent Classification Sandbox */}
            <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs space-y-4">
              <div className="flex items-center space-x-2">
                <Sparkles className="w-4 h-4 text-purple-600" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Live Intent Classifier Sandbox
                </h3>
              </div>

              <div className="flex items-center space-x-2">
                <input
                  type="text"
                  value={sandboxQuery}
                  onChange={(e) => setSandboxQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleRunIntentSandbox()}
                  className="flex-1 px-4 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-purple-500 shadow-2xs"
                  placeholder="Type any student query to test real-time inductive intent prediction..."
                />
                <button
                  disabled={classifying}
                  onClick={handleRunIntentSandbox}
                  className="py-2 px-4 rounded-xl bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white font-semibold text-xs shadow-xs transition-all"
                >
                  {classifying ? 'Predicting...' : 'Predict Intent'}
                </button>
              </div>

              {sandboxResult && (
                <div className="p-4 rounded-xl bg-purple-50/60 border border-purple-200 space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-[10px] uppercase font-bold text-purple-600">
                        Predicted Category:
                      </span>
                      <h4 className="text-sm font-bold text-slate-900 mt-0.5">
                        {sandboxResult.predicted_category}
                      </h4>
                    </div>
                    <div className="text-right">
                      <span className="text-[10px] uppercase font-bold text-slate-400">
                        Confidence
                      </span>
                      <span className="text-sm font-bold font-mono text-purple-700 block">
                        {(sandboxResult.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  {/* Probability distribution bars */}
                  <div className="space-y-1.5 pt-2 border-t border-purple-100">
                    <span className="text-[10px] font-semibold text-slate-500 block">
                      Category Probability Distribution:
                    </span>
                    {Object.entries(sandboxResult.class_probabilities)
                      .sort((a, b) => b[1] - a[1])
                      .map(([cat, prob]) => (
                        <div key={cat} className="flex items-center space-x-2 text-[11px]">
                          <span className="w-36 truncate text-slate-600">{cat}</span>
                          <div className="flex-1 bg-slate-200 h-2 rounded-full overflow-hidden">
                            <div
                              className="bg-purple-600 h-full rounded-full transition-all"
                              style={{ width: `${Math.round(prob * 100)}%` }}
                            />
                          </div>
                          <span className="w-12 text-right font-mono text-slate-600 text-[10px]">
                            {(prob * 100).toFixed(1)}%
                          </span>
                        </div>
                      ))}
                  </div>
                </div>
              )}
            </div>

            {/* Confusion Matrix Table */}
            {mlMetrics && (
              <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs overflow-x-auto">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
                  Confusion Matrix (Held-Out Test Set)
                </h3>
                <table className="w-full text-xs text-center border-collapse">
                  <thead>
                    <tr className="bg-slate-50 text-[10px] font-bold text-slate-500 uppercase">
                      <th className="p-2 text-left">Actual \ Predicted</th>
                      {mlMetrics.classes.map((c) => (
                        <th key={c} className="p-2 truncate max-w-[90px]" title={c}>
                          {c.slice(0, 8)}...
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {mlMetrics.confusion_matrix.map((row, rIdx) => (
                      <tr key={rIdx} className="border-t border-slate-100">
                        <td className="p-2 text-left font-semibold text-slate-700 truncate max-w-[130px]" title={mlMetrics.classes[rIdx]}>
                          {mlMetrics.classes[rIdx]}
                        </td>
                        {row.map((val, cIdx) => (
                          <td
                            key={cIdx}
                            className={`p-2 font-mono font-bold ${
                              rIdx === cIdx
                                ? val > 0 ? 'bg-indigo-50 text-indigo-700 font-extrabold' : 'text-slate-400'
                                : val > 0 ? 'bg-rose-50 text-rose-700' : 'text-slate-300'
                            }`}
                          >
                            {val}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 4: ANALOGY / CASE-BASED REASONING (CONCEPT 4) */}
        {/* ========================================================================= */}
        {activeTab === 'analogy' && (
          <div className="max-w-6xl mx-auto space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
              <h2 className="text-base font-bold text-slate-900">
                Concept 4: Learning by Analogy (Case-Based Reasoning)
              </h2>
              <p className="text-xs text-slate-500 mt-1 max-w-3xl leading-relaxed">
                Case-based reasoning retrieves solved curriculum problems similar to incoming queries via TF-IDF cosine similarity. Crucially, strict policy guardrails prevent individualized or rule queries (such as attendance percentage checks) from blindly borrowing precedent outcomes; instead, they route to WhatIf Lab.
              </p>
            </div>

            {/* Analogy Search Bar */}
            <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs space-y-4">
              <div className="flex items-center space-x-2">
                <Search className="w-4 h-4 text-purple-600" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Test Case-Based Analogy Matching
                </h3>
              </div>

              <div className="flex items-center space-x-2">
                <input
                  type="text"
                  value={analogyQuery}
                  onChange={(e) => setAnalogyQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleRunAnalogySearch()}
                  className="flex-1 px-4 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-purple-500 shadow-2xs"
                  placeholder="Enter a curriculum problem or concept..."
                />
                <button
                  disabled={searchingAnalogy}
                  onClick={handleRunAnalogySearch}
                  className="py-2 px-4 rounded-xl bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white font-semibold text-xs shadow-xs transition-all"
                >
                  {searchingAnalogy ? 'Matching...' : 'Find Analogies'}
                </button>
              </div>

              {/* Analogy Results */}
              <div className="space-y-3 pt-2">
                {analogyResults.length === 0 ? (
                  <p className="text-xs text-slate-400 italic">
                    Click &quot;Find Analogies&quot; to inspect solved curriculum case matches.
                  </p>
                ) : (
                  analogyResults.map((item) => (
                    <div
                      key={item.id}
                      className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 hover:border-purple-300 transition-all text-xs"
                    >
                      <div className="flex items-center justify-between mb-1.5">
                        <div className="flex items-center space-x-2">
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800">
                            Unit {item.unit} • {item.category}
                          </span>
                          <span className="font-bold text-slate-900">{item.question}</span>
                        </div>
                        <span className="font-mono font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded-md">
                          {Math.round(item.similarity * 100)}% Match
                        </span>
                      </div>
                      <p className="text-slate-600 text-[11px] leading-relaxed">
                        {item.solution_preview}
                      </p>
                      {onAskQuestion && (
                        <div className="mt-2.5 pt-2 border-t border-slate-200/60 flex justify-end">
                          <button
                            onClick={() => onAskQuestion(item.question)}
                            className="inline-flex items-center space-x-1 text-[11px] font-semibold text-purple-600 hover:text-purple-800"
                          >
                            <span>Ask This in Chat</span>
                            <ArrowRight className="w-3 h-3" />
                          </button>
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 5: EXPERT SYSTEM UNIFIED ARCHITECTURE (CONCEPT 5) */}
        {/* ========================================================================= */}
        {activeTab === 'architecture' && (
          <div className="max-w-6xl mx-auto space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs">
              <h2 className="text-base font-bold text-slate-900">
                Concept 5: Unified Expert System Architecture
              </h2>
              <p className="text-xs text-slate-500 mt-1 max-w-3xl leading-relaxed">
                Learnify AI integrates the 5 textbook components of classical and modern Expert Systems into a seamless pipeline, combining classical symbolic logic and search with inductive machine learning and adaptive memory.
              </p>
            </div>

            {/* Architecture Blocks Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-2">
                <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-700 flex items-center justify-center font-bold">
                  <Database className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-bold text-slate-900">1. Knowledge Base</h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Curated domain ontology, verified facts, topic dependency graph, and declarative policies (Units I & III).
                </p>
                <div className="pt-2 text-[10px] font-mono text-teal-700 font-semibold">
                  Source: SQLite tables + Coursework
                </div>
              </div>

              <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-2">
                <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-700 flex items-center justify-center font-bold">
                  <Search className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-bold text-slate-900">2. Search & Planning Engine</h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  PathForge curriculum search using BFS, DFS, Bidirectional Search, Greedy Best-First, and CSP backtracking (Unit II).
                </p>
                <div className="pt-2 text-[10px] font-mono text-indigo-700 font-semibold">
                  Service: PathForge
                </div>
              </div>

              <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-2">
                <div className="w-8 h-8 rounded-lg bg-rose-50 text-rose-700 flex items-center justify-center font-bold">
                  <Cpu className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-bold text-slate-900">3. Inference Engine</h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  WhatIf Lab forward chaining deduction, backward goal diagnosis, nonmonotonic exception overrides, and resolution (Units III & IV).
                </p>
                <div className="pt-2 text-[10px] font-mono text-rose-700 font-semibold">
                  Service: WhatIf Lab Reasoning Engine
                </div>
              </div>

              <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-2">
                <div className="w-8 h-8 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center font-bold">
                  <Brain className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-bold text-slate-900">4. Learning Engine</h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Continuous improvement via Rote memory caching, Human advice ingestion, TF-IDF Logistic Regression intent classification, and Case-Based analogy (Unit V).
                </p>
                <div className="pt-2 text-[10px] font-mono text-purple-700 font-semibold">
                  Module: Learning Engine (Naveen Kumar)
                </div>
              </div>

              <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-2">
                <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center font-bold">
                  <Clock className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-bold text-slate-900">5. Explanation Facility</h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  ProofLens real-time audit window exposing exact duration, algorithms invoked, intermediate steps, and grounding evidence (Rufus Samuel).
                </p>
                <div className="pt-2 text-[10px] font-mono text-blue-700 font-semibold">
                  Component: ProofLens
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LearningLabView;
