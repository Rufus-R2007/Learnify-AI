import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  GitBranch,
  Search,
  CheckCircle2,
  Clock,
  AlertCircle,
  Calendar,
  RefreshCw,
  Play,
  Check,
  ChevronRight,
  Info,
  Sliders,
  ZoomIn,
  ZoomOut,
  Cpu,
  ShieldCheck,
  RotateCcw,
  CheckSquare,
  Square,
} from 'lucide-react';
import {
  PathForgeTopic,
  PathForgeGraphResponse,
  LearningPlanResponse,
  CompareAlgorithmsResponse,
  StudyScheduleResponse,
  TraceStep,
  Message
} from '../types';
import {
  getPathForgeTopics,
  getPathForgeGraph,
  planLearningPath,
  compareAlgorithms,
  generateStudySchedule
} from '../services/api';

interface PathForgeViewProps {
  onBackToChat: () => void;
  onSyncTraceToProofLens?: (message: Message) => void;
  initialGoalTopicId?: string | null;
}

type TabType = 'planner' | 'explorer' | 'scheduler' | 'trace';

export const PathForgeView: React.FC<PathForgeViewProps> = ({
  onBackToChat,
  onSyncTraceToProofLens,
  initialGoalTopicId,
}) => {
  // Global state
  const [activeTab, setActiveTab] = useState<TabType>('planner');
  const [topics, setTopics] = useState<PathForgeTopic[]>([]);
  const [graphData, setGraphData] = useState<PathForgeGraphResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Planner state
  const [selectedGoalId, setSelectedGoalId] = useState<string>(
    initialGoalTopicId || 'topic-machine-learning'
  );
  const [selectedStartId, setSelectedStartId] = useState<string>('topic-python-basics');
  const [knownTopicIds, setKnownTopicIds] = useState<string[]>([
    'topic-programming-fundamentals',
    'topic-python-basics'
  ]);
  const [selectedAlgo, setSelectedAlgo] = useState<string>('bfs');
  const [searchFilter, setSearchFilter] = useState<string>('');
  const [isPlanning, setIsPlanning] = useState<boolean>(false);
  const [currentPlan, setCurrentPlan] = useState<LearningPlanResponse | null>(null);
  const [graphViewMode, setGraphViewMode] = useState<'graph' | 'list'>('graph');

  // Graph canvas state
  const [zoomLevel, setZoomLevel] = useState<number>(1);
  const [panOffset, setPanOffset] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const isDraggingRef = useRef(false);
  const dragStartRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  // Algorithm Explorer state
  const [compareStartId, setCompareStartId] = useState<string>('topic-programming-fundamentals');
  const [compareGoalId, setCompareGoalId] = useState<string>('topic-machine-learning');
  const [isComparing, setIsComparing] = useState<boolean>(false);
  const [compareResults, setCompareResults] = useState<CompareAlgorithmsResponse | null>(null);

  // Study Scheduler state
  const [availableDays, setAvailableDays] = useState<string[]>([
    'Monday',
    'Wednesday',
    'Friday'
  ]);
  const [maxDailyHours, setMaxDailyHours] = useState<number>(2);
  const [preferredSessionHours, setPreferredSessionHours] = useState<number>(1);
  const [planningWeeks, setPlanningWeeks] = useState<number>(2);
  const [isScheduling, setIsScheduling] = useState<boolean>(false);
  const [scheduleResult, setScheduleResult] = useState<StudyScheduleResponse | null>(null);

  // Active trace for ProofLens view
  const [activeTrace, setActiveTrace] = useState<TraceStep[]>([]);
  const [traceTitle, setTraceTitle] = useState<string>('PathForge Execution Trace');

  // Initial data loading
  useEffect(() => {
    let isMounted = true;
    const loadInitialData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [topicsRes, graphRes] = await Promise.all([
          getPathForgeTopics(),
          getPathForgeGraph(),
        ]);
        if (!isMounted) return;
        setTopics(topicsRes.topics);
        setGraphData(graphRes);

        // Pre-generate a default plan
        const defaultGoal = initialGoalTopicId || 'topic-machine-learning';
        setSelectedGoalId(defaultGoal);
        const planRes = await planLearningPath(
          defaultGoal,
          ['topic-programming-fundamentals', 'topic-python-basics'],
          'topic-python-basics',
          'bfs'
        );
        if (isMounted) {
          setCurrentPlan(planRes);
          setActiveTrace(planRes.trace || []);
          setTraceTitle(`Topological Path Planning: ${planRes.goal_topic_name}`);
        }
      } catch (err: unknown) {
        if (!isMounted) return;
        console.error('Failed to load PathForge data:', err);
        setError(err instanceof Error ? err.message : 'Failed to connect to PathForge services.');
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    loadInitialData();
    return () => {
      isMounted = false;
    };
  }, [initialGoalTopicId]);

  // Handle plan generation
  const handleGeneratePath = async (algoToUse?: string) => {
    if (!selectedGoalId) return;
    setIsPlanning(true);
    setError(null);
    try {
      const res = await planLearningPath(
        selectedGoalId,
        knownTopicIds,
        selectedStartId || null,
        algoToUse || selectedAlgo
      );
      setCurrentPlan(res);
      setActiveTrace(res.trace || []);
      setTraceTitle(`Learning Path: ${res.goal_topic_name} (${(algoToUse || selectedAlgo).toUpperCase()})`);

      if (onSyncTraceToProofLens && res.trace) {
        const syntheticMessage: Message = {
          id: `pathforge-${Date.now()}`,
          role: 'assistant',
          content: `PathForge planned a complete learning journey for **${res.goal_topic_name}** using ${res.algorithm_used.toUpperCase()}. Requires ${res.remaining_prerequisites.length} remaining topics (${res.total_estimated_hours} estimated hours).`,
          timestamp: new Date(),
          conceptsUsed: [
            res.algorithm_used.toUpperCase(),
            'Topological Sorting',
            'Prerequisite Closure',
            'Search Techniques'
          ],
          matchScore: 1.0,
          sources: [
            {
              id: 'src-pathforge-graph',
              name: 'Curriculum Knowledge Graph',
              description: 'Phase 2 Search & Prerequisite Engine',
            },
          ],
          trace: res.trace,
          status: 'answered',
        };
        onSyncTraceToProofLens(syntheticMessage);
      }
    } catch (err: unknown) {
      console.error('Path planning failed:', err);
      setError(err instanceof Error ? err.message : 'Path planning failed.');
    } finally {
      setIsPlanning(false);
    }
  };

  // Handle algorithm comparison
  const handleRunComparison = async () => {
    if (!compareStartId || !compareGoalId) return;
    setIsComparing(true);
    setError(null);
    try {
      const res = await compareAlgorithms(compareStartId, compareGoalId);
      setCompareResults(res);
    } catch (err: unknown) {
      console.error('Algorithm comparison failed:', err);
      setError(err instanceof Error ? err.message : 'Algorithm comparison failed.');
    } finally {
      setIsComparing(false);
    }
  };

  // Handle study scheduling
  const handleGenerateSchedule = async () => {
    if (!selectedGoalId) return;
    setIsScheduling(true);
    setError(null);
    try {
      const res = await generateStudySchedule({
        goalTopicId: selectedGoalId,
        knownTopicIds,
        availableDays,
        maxDailyHours,
        preferredSessionHours,
        planningWeeks,
      });
      setScheduleResult(res);
      if (res.trace && res.trace.length > 0) {
        setActiveTrace(res.trace);
        setTraceTitle(`CSP Study Scheduling Backtracking Trace`);
      }
    } catch (err: unknown) {
      console.error('Study scheduling failed:', err);
      setError(err instanceof Error ? err.message : 'Study scheduling failed.');
    } finally {
      setIsScheduling(false);
    }
  };

  // Toggle known topics
  const toggleKnownTopic = (topicId: string) => {
    setKnownTopicIds((prev) =>
      prev.includes(topicId) ? prev.filter((id) => id !== topicId) : [...prev, topicId]
    );
  };

  // Toggle day selection
  const toggleDay = (day: string) => {
    setAvailableDays((prev) =>
      prev.includes(day)
        ? prev.length > 1
          ? prev.filter((d) => d !== day)
          : prev
        : [...prev, day]
    );
  };

  // Selected goal topic object
  const currentGoalTopic = useMemo(
    () => topics.find((t) => t.id === selectedGoalId),
    [topics, selectedGoalId]
  );

  // Filtered topics list for dropdown search
  const filteredTopics = useMemo(() => {
    if (!searchFilter.trim()) return topics;
    const q = searchFilter.toLowerCase();
    return topics.filter(
      (t) =>
        t.name.toLowerCase().includes(q) ||
        t.description.toLowerCase().includes(q) ||
        (t.category && t.category.toLowerCase().includes(q))
    );
  }, [topics, searchFilter]);

  // Node coordinates calculation for SVG layout
  // Organizes 23 nodes in structured academic tiers (Unit I foundational at bottom/left to Unit IV/V at right)
  const nodeLayout = useMemo(() => {
    if (!topics.length) return new Map<string, { x: number; y: number; unit: number }>();
    const positions = new Map<string, { x: number; y: number; unit: number }>();

    // Layer grouping by Unit
    const unitsMap: Record<number, PathForgeTopic[]> = { 1: [], 2: [], 3: [], 4: [], 5: [] };
    topics.forEach((t) => {
      const u = t.unit || 1;
      if (!unitsMap[u]) unitsMap[u] = [];
      unitsMap[u].push(t);
    });

    const tierX = { 1: 120, 2: 380, 3: 650, 4: 920, 5: 1180 };

    Object.entries(unitsMap).forEach(([unitStr, unitTopics]) => {
      const unit = Number(unitStr);
      const baseX = tierX[unit as keyof typeof tierX] || 500;
      const count = unitTopics.length;
      const spacing = 110;
      const startY = 120 + Math.max(0, (5 - count) * 40);

      unitTopics.forEach((topic, idx) => {
        // Slight staggered offset for readability
        const stagger = (idx % 2) * 20;
        positions.set(topic.id, {
          x: baseX + stagger,
          y: startY + idx * spacing,
          unit,
        });
      });
    });

    return positions;
  }, [topics]);

  // SVG Mouse handlers for dragging/panning
  const handleMouseDown = (e: React.MouseEvent<SVGSVGElement>) => {
    if (e.button !== 0) return;
    isDraggingRef.current = true;
    dragStartRef.current = { x: e.clientX - panOffset.x, y: e.clientY - panOffset.y };
  };

  const handleMouseMove = (e: React.MouseEvent<SVGSVGElement>) => {
    if (!isDraggingRef.current) return;
    setPanOffset({
      x: e.clientX - dragStartRef.current.x,
      y: e.clientY - dragStartRef.current.y,
    });
  };

  const handleMouseUp = () => {
    isDraggingRef.current = false;
  };

  // Selected node details object
  const activeNodeDetails = useMemo(() => {
    if (!selectedNodeId) return null;
    return topics.find((t) => t.id === selectedNodeId) || null;
  }, [selectedNodeId, topics]);

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-50 overflow-hidden select-none">
      {/* 1. Header Bar */}
      <header className="px-6 py-3.5 bg-white border-b border-slate-200/80 flex flex-wrap items-center justify-between gap-3 shrink-0 shadow-2xs">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-brand-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
            <GitBranch className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-base font-bold text-slate-900 tracking-tight">PathForge</h1>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
                Phase 2 Engine
              </span>
              <span className="hidden md:inline-flex items-center text-[10px] text-slate-500 font-mono bg-slate-100 px-2 py-0.5 rounded">
                Unit II Search & Planning
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Goal-Oriented Curriculum Planning, Directed Search & CSP Timetable Generator
            </p>
          </div>
        </div>

        {/* Tab Switcher & Return to Chat */}
        <div className="flex items-center space-x-2">
          <div className="bg-slate-100 p-1 rounded-xl flex items-center space-x-1">
            <button
              onClick={() => setActiveTab('planner')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'planner'
                  ? 'bg-white text-indigo-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Study Path
            </button>
            <button
              onClick={() => setActiveTab('explorer')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'explorer'
                  ? 'bg-white text-indigo-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Algorithm Explorer
            </button>
            <button
              onClick={() => setActiveTab('scheduler')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'scheduler'
                  ? 'bg-white text-indigo-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              CSP Scheduler
            </button>
            <button
              onClick={() => setActiveTab('trace')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center space-x-1 ${
                activeTab === 'trace'
                  ? 'bg-white text-indigo-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
              <span>Live Trace</span>
              {activeTrace.length > 0 && (
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse ml-0.5" />
              )}
            </button>
          </div>

          <button
            onClick={onBackToChat}
            className="px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-medium text-slate-700 hover:bg-slate-100 transition-colors"
          >
            Back to Chat
          </button>
        </div>
      </header>

      {/* Global Error Banner */}
      {error && (
        <div className="px-6 py-2.5 bg-rose-50 border-b border-rose-200 text-xs text-rose-800 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
          <button
            onClick={() => setError(null)}
            className="text-rose-600 font-bold hover:underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* 2. Main Workspace Content Area */}
      <div className="flex-1 overflow-hidden flex flex-col">
        {loading ? (
          <div className="flex-1 flex flex-col items-center justify-center p-8 space-y-3">
            <div className="w-10 h-10 rounded-full border-3 border-indigo-200 border-t-indigo-600 animate-spin" />
            <p className="text-xs font-semibold text-slate-600">
              Loading Curriculum Knowledge Graph & Search Engines...
            </p>
          </div>
        ) : (
          <>
            {/* ========================================================= */}
            {/* TAB 1: STUDY PATH PLANNER */}
            {/* ========================================================= */}
            {activeTab === 'planner' && (
              <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
                {/* Left Panel: Configuration & Parameters */}
                <aside className="w-full lg:w-96 bg-white border-r border-slate-200/80 p-5 flex flex-col overflow-y-auto shrink-0 space-y-5">
                  <div>
                    <h2 className="text-sm font-bold text-slate-900 tracking-tight flex items-center space-x-2">
                      <Sliders className="w-4 h-4 text-indigo-600" />
                      <span>Configure Learning Goal</span>
                    </h2>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Select your target goal and state your prior knowledge.
                    </p>
                  </div>

                  {/* Target Goal Selector */}
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold uppercase tracking-wider text-slate-500">
                      Target Learning Goal
                    </label>
                    <div className="relative mb-1">
                      <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
                      <input
                        type="text"
                        placeholder="Filter goal topics..."
                        value={searchFilter}
                        onChange={(e) => setSearchFilter(e.target.value)}
                        className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs placeholder:text-slate-400 focus:outline-hidden focus:ring-1 focus:ring-indigo-500"
                      />
                    </div>
                    <div className="relative">
                      <select
                        value={selectedGoalId}
                        onChange={(e) => {
                          setSelectedGoalId(e.target.value);
                          setSelectedNodeId(e.target.value);
                        }}
                        className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-900 focus:outline-hidden focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all appearance-none pr-8 cursor-pointer"
                      >
                        {filteredTopics.map((topic) => (
                          <option key={topic.id} value={topic.id}>
                            Unit {topic.unit}: {topic.name}
                          </option>
                        ))}
                      </select>
                      <ChevronRight className="w-4 h-4 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none rotate-90" />
                    </div>

                    {currentGoalTopic && (
                      <p className="text-[11px] text-slate-500 leading-relaxed bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                        {currentGoalTopic.description}
                      </p>
                    )}
                  </div>

                  {/* Optional Starting Node */}
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center justify-between">
                      <span>Start Node (Single-Path Route)</span>
                      <span className="text-[10px] text-slate-400 font-normal">Optional</span>
                    </label>
                    <select
                      value={selectedStartId}
                      onChange={(e) => setSelectedStartId(e.target.value)}
                      className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all appearance-none pr-8 cursor-pointer"
                    >
                      <option value="">No single start (prerequisite closure only)</option>
                      {topics
                        .filter((t) => t.id !== selectedGoalId)
                        .map((topic) => (
                          <option key={topic.id} value={topic.id}>
                            {topic.name} (Unit {topic.unit})
                          </option>
                        ))}
                    </select>
                  </div>

                  {/* Algorithm Selector */}
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold uppercase tracking-wider text-slate-500">
                      Search Strategy
                    </label>
                    <div className="grid grid-cols-2 gap-1.5">
                      {[
                        { id: 'bfs', label: 'BFS', desc: 'Shortest edges' },
                        { id: 'bidirectional', label: 'Bidirectional', desc: 'Dual-frontier' },
                        { id: 'best_first', label: 'Greedy Best-First', desc: 'Heuristic-guided' },
                        { id: 'dfs', label: 'DFS', desc: 'Deep dependency' },
                      ].map((algo) => (
                        <button
                          key={algo.id}
                          onClick={() => setSelectedAlgo(algo.id)}
                          className={`p-2 rounded-xl text-left border transition-all ${
                            selectedAlgo === algo.id
                              ? 'bg-indigo-50/80 border-indigo-300 text-indigo-900 shadow-2xs'
                              : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                          }`}
                        >
                          <div className="text-xs font-bold">{algo.label}</div>
                          <div className="text-[10px] text-slate-500">{algo.desc}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Prior Knowledge Multi-Selection */}
                  <div className="space-y-2 flex-1 flex flex-col min-h-0">
                    <div className="flex items-center justify-between">
                      <label className="text-xs font-bold uppercase tracking-wider text-slate-500">
                        Already Mastered ({knownTopicIds.length})
                      </label>
                      <div className="flex items-center space-x-1.5 text-[11px]">
                        <button
                          onClick={() =>
                            setKnownTopicIds([
                              'topic-programming-fundamentals',
                              'topic-python-basics',
                              'topic-linear-algebra'
                            ])
                          }
                          className="text-indigo-600 hover:underline"
                        >
                          Common Baseline
                        </button>
                        <span className="text-slate-300">|</span>
                        <button
                          onClick={() => setKnownTopicIds([])}
                          className="text-slate-500 hover:underline"
                        >
                          Clear
                        </button>
                      </div>
                    </div>

                    <div className="flex-1 overflow-y-auto max-h-48 border border-slate-200 rounded-xl p-2 bg-slate-50/50 space-y-1">
                      {topics
                        .filter((t) => t.id !== selectedGoalId)
                        .map((topic) => {
                          const isKnown = knownTopicIds.includes(topic.id);
                          return (
                            <button
                              key={topic.id}
                              onClick={() => toggleKnownTopic(topic.id)}
                              className={`w-full text-left px-2 py-1.5 rounded-lg text-xs flex items-center justify-between transition-colors ${
                                isKnown
                                  ? 'bg-emerald-50 text-emerald-800 font-medium border border-emerald-200/60'
                                  : 'text-slate-600 hover:bg-white hover:text-slate-900'
                              }`}
                            >
                              <div className="flex items-center space-x-2 truncate">
                                {isKnown ? (
                                  <CheckSquare className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                                ) : (
                                  <Square className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                                )}
                                <span className="truncate">{topic.name}</span>
                              </div>
                              <span className="text-[10px] text-slate-400 font-mono shrink-0">
                                U{topic.unit}
                              </span>
                            </button>
                          );
                        })}
                    </div>
                  </div>

                  {/* Submit Button */}
                  <button
                    onClick={() => handleGeneratePath()}
                    disabled={isPlanning}
                    className="w-full py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-sm shadow-indigo-600/20 hover:shadow-md transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
                  >
                    {isPlanning ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        <span>Searching Knowledge Graph...</span>
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4 fill-current" />
                        <span>Generate Learning Plan</span>
                      </>
                    )}
                  </button>
                </aside>

                {/* Center / Right: Interactive Knowledge Graph & Journey Flow */}
                <main className="flex-1 flex flex-col overflow-hidden bg-slate-50/50">
                  {/* Action Strip: Metrics & View Toggle */}
                  <div className="px-5 py-3 bg-white border-b border-slate-200/80 flex flex-wrap items-center justify-between gap-3 shadow-2xs">
                    <div className="flex items-center space-x-4">
                      {currentPlan && (
                        <div className="flex items-center space-x-3 text-xs">
                          <div className="flex items-center space-x-1.5">
                            <span className="text-slate-400">Total in Path:</span>
                            <span className="font-bold text-slate-900 font-mono">
                              {currentPlan.all_prerequisites.length + 1}
                            </span>
                          </div>
                          <span className="text-slate-300">•</span>
                          <div className="flex items-center space-x-1.5">
                            <span className="text-slate-400">Mastered:</span>
                            <span className="font-bold text-emerald-600 font-mono">
                              {currentPlan.already_mastered.length}
                            </span>
                          </div>
                          <span className="text-slate-300">•</span>
                          <div className="flex items-center space-x-1.5">
                            <span className="text-slate-400">To Study:</span>
                            <span className="font-bold text-indigo-600 font-mono">
                              {currentPlan.remaining_prerequisites.length}
                            </span>
                          </div>
                          <span className="text-slate-300">•</span>
                          <div className="flex items-center space-x-1.5">
                            <Clock className="w-3.5 h-3.5 text-slate-400" />
                            <span className="font-bold text-slate-900 font-mono">
                              {currentPlan.total_estimated_hours} hrs
                            </span>
                          </div>
                        </div>
                      )}
                    </div>

                    <div className="flex items-center space-x-2">
                      <div className="bg-slate-100 p-1 rounded-lg flex items-center space-x-1">
                        <button
                          onClick={() => setGraphViewMode('graph')}
                          className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                            graphViewMode === 'graph'
                              ? 'bg-white text-indigo-700 shadow-2xs'
                              : 'text-slate-600 hover:text-slate-900'
                          }`}
                        >
                          Visual Graph
                        </button>
                        <button
                          onClick={() => setGraphViewMode('list')}
                          className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                            graphViewMode === 'list'
                              ? 'bg-white text-indigo-700 shadow-2xs'
                              : 'text-slate-600 hover:text-slate-900'
                          }`}
                        >
                          Step-by-Step List
                        </button>
                      </div>

                      {graphViewMode === 'graph' && (
                        <div className="flex items-center space-x-1 border-l border-slate-200 pl-2">
                          <button
                            onClick={() => setZoomLevel((z) => Math.min(z + 0.15, 2.0))}
                            className="p-1 rounded text-slate-500 hover:bg-slate-100"
                            title="Zoom In"
                          >
                            <ZoomIn className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => setZoomLevel((z) => Math.max(z - 0.15, 0.5))}
                            className="p-1 rounded text-slate-500 hover:bg-slate-100"
                            title="Zoom Out"
                          >
                            <ZoomOut className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => {
                              setZoomLevel(1);
                              setPanOffset({ x: 0, y: 0 });
                            }}
                            className="p-1 rounded text-slate-500 hover:bg-slate-100"
                            title="Reset View"
                          >
                            <RotateCcw className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Viewport: Interactive Graph Canvas OR Step List */}
                  {graphViewMode === 'graph' ? (
                    <div className="flex-1 relative overflow-hidden bg-slate-900 select-none">
                      {/* Graph Legend Overlay */}
                      <div className="absolute top-4 left-4 z-10 bg-slate-900/80 backdrop-blur-md p-3 rounded-xl border border-slate-700/80 text-[11px] text-slate-300 space-y-1.5 shadow-lg pointer-events-none">
                        <div className="font-bold text-slate-100 text-xs mb-1">
                          Curriculum Graph Semantics
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-purple-500 border border-purple-300" />
                          <span>Target Goal Node</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                          <span>Mastered (Known) Topic</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 ring-2 ring-indigo-300" />
                          <span>Shortest Route Path</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-sky-500" />
                          <span>Mandatory Prerequisite</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="w-4 h-0.5 bg-indigo-400" />
                          <span>A → B (A required for B)</span>
                        </div>
                      </div>

                      {/* Interactive SVG Canvas */}
                      <svg
                        className="w-full h-full cursor-grab active:cursor-grabbing"
                        onMouseDown={handleMouseDown}
                        onMouseMove={handleMouseMove}
                        onMouseUp={handleMouseUp}
                      >
                        <defs>
                          <marker
                            id="arrowhead-default"
                            markerWidth="8"
                            markerHeight="6"
                            refX="7"
                            refY="3"
                            orient="auto"
                          >
                            <polygon points="0 0, 8 3, 0 6" fill="#64748b" />
                          </marker>
                          <marker
                            id="arrowhead-active"
                            markerWidth="10"
                            markerHeight="8"
                            refX="9"
                            refY="4"
                            orient="auto"
                          >
                            <polygon points="0 0, 10 4, 0 8" fill="#818cf8" />
                          </marker>
                          <marker
                            id="arrowhead-goal"
                            markerWidth="10"
                            markerHeight="8"
                            refX="9"
                            refY="4"
                            orient="auto"
                          >
                            <polygon points="0 0, 10 4, 0 8" fill="#c084fc" />
                          </marker>
                        </defs>

                        <g
                          transform={`translate(${panOffset.x}, ${panOffset.y}) scale(${zoomLevel})`}
                        >
                          {/* Unit Columns Background Indicators */}
                          {[1, 2, 3, 4, 5].map((u) => {
                            const tierX = { 1: 120, 2: 380, 3: 650, 4: 920, 5: 1180 };
                            const x = tierX[u as keyof typeof tierX] || 500;
                            return (
                              <g key={u}>
                                <line
                                  x1={x}
                                  y1={40}
                                  x2={x}
                                  y2={800}
                                  stroke="#334155"
                                  strokeDasharray="4 4"
                                  strokeWidth="1"
                                />
                                <text
                                  x={x}
                                  y={70}
                                  fill="#64748b"
                                  fontSize="11"
                                  fontFamily="sans-serif"
                                  textAnchor="middle"
                                  fontWeight="bold"
                                >
                                  UNIT {u}
                                </text>
                              </g>
                            );
                          })}

                          {/* Render Directed Edges */}
                          {graphData?.edges.map((edge, idx) => {
                            const srcPos = nodeLayout.get(edge.source);
                            const tgtPos = nodeLayout.get(edge.target);
                            if (!srcPos || !tgtPos) return null;

                            // Check if this edge is part of shortest path
                            const isShortestPathEdge =
                              currentPlan?.shortest_path_nodes &&
                              currentPlan.shortest_path_nodes.includes(edge.source) &&
                              currentPlan.shortest_path_nodes.includes(edge.target) &&
                              currentPlan.shortest_path_nodes.indexOf(edge.target) ===
                                currentPlan.shortest_path_nodes.indexOf(edge.source) + 1;

                            const isPrereqEdge =
                              currentPlan?.all_prerequisites.includes(edge.source) &&
                              (currentPlan.all_prerequisites.includes(edge.target) ||
                                edge.target === selectedGoalId);

                            // Smooth curved bezier line
                            const dx = tgtPos.x - srcPos.x;
                            const cx1 = srcPos.x + dx * 0.5;
                            const cy1 = srcPos.y;
                            const cx2 = srcPos.x + dx * 0.5;
                            const cy2 = tgtPos.y;

                            return (
                              <path
                                key={idx}
                                d={`M ${srcPos.x} ${srcPos.y} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${tgtPos.x} ${tgtPos.y}`}
                                fill="none"
                                stroke={
                                  isShortestPathEdge
                                    ? '#818cf8'
                                    : isPrereqEdge
                                    ? '#38bdf8'
                                    : '#334155'
                                }
                                strokeWidth={isShortestPathEdge ? '3' : isPrereqEdge ? '2' : '1.2'}
                                strokeDasharray={isShortestPathEdge ? 'none' : 'none'}
                                markerEnd={
                                  isShortestPathEdge
                                    ? 'url(#arrowhead-active)'
                                    : edge.target === selectedGoalId
                                    ? 'url(#arrowhead-goal)'
                                    : 'url(#arrowhead-default)'
                                }
                                opacity={
                                  currentPlan
                                    ? isShortestPathEdge || isPrereqEdge
                                      ? 1
                                      : 0.35
                                    : 0.7
                                }
                              />
                            );
                          })}

                          {/* Render Topic Nodes */}
                          {topics.map((topic) => {
                            const pos = nodeLayout.get(topic.id);
                            if (!pos) return null;

                            const isGoal = topic.id === selectedGoalId;
                            const isMastered = knownTopicIds.includes(topic.id);
                            const isInShortestPath =
                              currentPlan?.shortest_path_nodes?.includes(topic.id);
                            const isRemainingPrereq =
                              currentPlan?.remaining_prerequisites?.includes(topic.id);
                            const isSelected = selectedNodeId === topic.id;

                            let nodeFill = '#1e293b';
                            let nodeStroke = '#475569';
                            let strokeWidth = '2';

                            if (isGoal) {
                              nodeFill = '#7e22ce';
                              nodeStroke = '#c084fc';
                              strokeWidth = '3';
                            } else if (isMastered) {
                              nodeFill = '#065f46';
                              nodeStroke = '#34d399';
                              strokeWidth = '2.5';
                            } else if (isInShortestPath) {
                              nodeFill = '#4338ca';
                              nodeStroke = '#818cf8';
                              strokeWidth = '3';
                            } else if (isRemainingPrereq) {
                              nodeFill = '#0369a1';
                              nodeStroke = '#38bdf8';
                              strokeWidth = '2.5';
                            }

                            return (
                              <g
                                key={topic.id}
                                transform={`translate(${pos.x}, ${pos.y})`}
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setSelectedNodeId(topic.id);
                                }}
                                className="cursor-pointer group"
                              >
                                {isGoal && (
                                  <circle
                                    r="34"
                                    fill="none"
                                    stroke="#c084fc"
                                    strokeWidth="2"
                                    opacity="0.4"
                                    className="animate-pulse"
                                  />
                                )}

                                <circle
                                  r="26"
                                  fill={nodeFill}
                                  stroke={isSelected ? '#f8fafc' : nodeStroke}
                                  strokeWidth={isSelected ? '4' : strokeWidth}
                                  className="transition-all duration-200 group-hover:scale-110"
                                />

                                {/* Icon / Label inside node */}
                                {isMastered ? (
                                  <text
                                    y="4"
                                    fill="#ecfdf5"
                                    fontSize="14"
                                    textAnchor="middle"
                                    fontWeight="bold"
                                  >
                                    ✓
                                  </text>
                                ) : (
                                  <text
                                    y="4"
                                    fill="#f8fafc"
                                    fontSize="11"
                                    textAnchor="middle"
                                    fontWeight="bold"
                                  >
                                    {topic.estimated_hours || 2}h
                                  </text>
                                )}

                                {/* Topic Label below node */}
                                <text
                                  y="40"
                                  fill={isGoal ? '#e9d5ff' : '#f1f5f9'}
                                  fontSize="11"
                                  fontWeight={isGoal || isSelected ? 'bold' : 'normal'}
                                  fontFamily="sans-serif"
                                  textAnchor="middle"
                                  className="pointer-events-none drop-shadow"
                                >
                                  {topic.name.length > 20
                                    ? topic.name.slice(0, 18) + '...'
                                    : topic.name}
                                </text>
                              </g>
                            );
                          })}
                        </g>
                      </svg>

                      {/* Selected Node Inspector Flyout */}
                      {activeNodeDetails && (
                        <div className="absolute bottom-4 right-4 z-10 w-80 bg-white/95 backdrop-blur-md p-4 rounded-2xl border border-slate-200 shadow-xl text-xs space-y-2.5">
                          <div className="flex items-center justify-between">
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-50 text-indigo-700">
                              Unit {activeNodeDetails.unit} • {activeNodeDetails.category || 'Topic'}
                            </span>
                            <button
                              onClick={() => setSelectedNodeId(null)}
                              className="text-slate-400 hover:text-slate-600"
                            >
                              ✕
                            </button>
                          </div>
                          <div>
                            <h4 className="font-bold text-slate-900 text-sm">
                              {activeNodeDetails.name}
                            </h4>
                            <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                              {activeNodeDetails.description}
                            </p>
                          </div>
                          <div className="flex items-center justify-between text-[11px] pt-1 border-t border-slate-100 text-slate-600">
                            <span>Estimated Effort:</span>
                            <span className="font-bold text-slate-900">
                              {activeNodeDetails.estimated_hours || 2} study hours
                            </span>
                          </div>
                          <div className="pt-2 flex items-center space-x-2">
                            <button
                              onClick={() => {
                                setSelectedGoalId(activeNodeDetails.id);
                                handleGeneratePath();
                              }}
                              className="flex-1 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-[11px] text-center"
                            >
                              Set as Goal
                            </button>
                            <button
                              onClick={() => toggleKnownTopic(activeNodeDetails.id)}
                              className={`flex-1 py-1.5 rounded-lg border font-medium text-[11px] text-center ${
                                knownTopicIds.includes(activeNodeDetails.id)
                                  ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                                  : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                              }`}
                            >
                              {knownTopicIds.includes(activeNodeDetails.id)
                                ? 'Mark Unlearned'
                                : 'Mark Mastered'}
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    /* Step-by-Step Accessible List View */
                    <div className="flex-1 overflow-y-auto p-6 space-y-3">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                          Topological Prerequisite Learning Journey ({currentPlan?.planned_journey.length || 0} Stages)
                        </h3>
                        <span className="text-xs text-slate-400">
                          Topologically sorted dependency order
                        </span>
                      </div>

                      {currentPlan?.planned_journey && currentPlan.planned_journey.length > 0 ? (
                        currentPlan.planned_journey.map((item) => {
                          const isMastered = item.status === 'completed';
                          const isGoal = item.topic_id === selectedGoalId;

                          return (
                            <div
                              key={item.topic_id}
                              className={`p-4 rounded-xl border transition-all ${
                                isGoal
                                  ? 'bg-purple-50/70 border-purple-200 shadow-2xs'
                                  : isMastered
                                  ? 'bg-emerald-50/50 border-emerald-200/80'
                                  : 'bg-white border-slate-200 shadow-2xs'
                              }`}
                            >
                              <div className="flex items-start justify-between gap-3">
                                <div className="flex items-start space-x-3">
                                  <div
                                    className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 ${
                                      isGoal
                                        ? 'bg-purple-600 text-white'
                                        : isMastered
                                        ? 'bg-emerald-600 text-white'
                                        : 'bg-indigo-100 text-indigo-700'
                                    }`}
                                  >
                                    {String(item.step_number).padStart(2, '0')}
                                  </div>

                                  <div>
                                    <div className="flex items-center space-x-2">
                                      <h4 className="text-xs font-bold text-slate-900">
                                        {item.name}
                                      </h4>
                                      <span className="text-[10px] px-2 py-0.2 rounded-full bg-slate-100 text-slate-600 font-medium">
                                        Unit {item.unit}
                                      </span>
                                      {isGoal && (
                                        <span className="text-[10px] px-2 py-0.2 rounded-full bg-purple-100 text-purple-700 font-bold">
                                          Primary Goal
                                        </span>
                                      )}
                                      {isMastered && (
                                        <span className="text-[10px] px-2 py-0.2 rounded-full bg-emerald-100 text-emerald-800 font-semibold flex items-center">
                                          <Check className="w-3 h-3 mr-0.5" /> Already Mastered
                                        </span>
                                      )}
                                    </div>
                                    <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                                      {item.description}
                                    </p>
                                    <div className="flex flex-wrap items-center gap-2 mt-2 text-[10px] text-slate-500">
                                      <span className="font-semibold text-slate-700">
                                        Role in Plan:
                                      </span>
                                      <span className="bg-slate-100 px-2 py-0.5 rounded text-slate-600">
                                        {item.reason_included}
                                      </span>
                                      {item.direct_prerequisites.length > 0 && (
                                        <>
                                          <span className="font-semibold text-slate-700 ml-2">
                                            Requires:
                                          </span>
                                          <span className="font-mono text-indigo-600">
                                            {item.direct_prerequisites.join(', ')}
                                          </span>
                                        </>
                                      )}
                                    </div>
                                  </div>
                                </div>

                                <div className="text-right shrink-0">
                                  <span className="text-xs font-mono font-bold text-slate-900 block">
                                    {item.estimated_hours} hrs
                                  </span>
                                  <span className="text-[10px] text-slate-400">estimated</span>
                                </div>
                              </div>
                            </div>
                          );
                        })
                      ) : (
                        <div className="p-8 text-center text-slate-400 text-xs">
                          No journey planned yet. Click "Generate Learning Plan" on the left.
                        </div>
                      )}
                    </div>
                  )}
                </main>
              </div>
            )}

            {/* ========================================================= */}
            {/* TAB 2: ALGORITHM EXPLORER */}
            {/* ========================================================= */}
            {activeTab === 'explorer' && (
              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {/* Header & Controls */}
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-4">
                  <div>
                    <h2 className="text-sm font-bold text-slate-900 tracking-tight flex items-center space-x-2">
                      <Cpu className="w-4 h-4 text-indigo-600" />
                      <span>Search Algorithm Empirical Benchmark</span>
                    </h2>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Compare classical uninformed (BFS, DFS) and informed (Greedy Best-First) search algorithms on the exact same graph query.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
                    <div>
                      <label className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-1">
                        Starting Topic
                      </label>
                      <select
                        value={compareStartId}
                        onChange={(e) => setCompareStartId(e.target.value)}
                        className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-800"
                      >
                        {topics.map((t) => (
                          <option key={t.id} value={t.id}>
                            {t.name} (Unit {t.unit})
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-1">
                        Target Goal Topic
                      </label>
                      <select
                        value={compareGoalId}
                        onChange={(e) => setCompareGoalId(e.target.value)}
                        className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-800"
                      >
                        {topics.map((t) => (
                          <option key={t.id} value={t.id}>
                            {t.name} (Unit {t.unit})
                          </option>
                        ))}
                      </select>
                    </div>

                    <button
                      onClick={handleRunComparison}
                      disabled={isComparing}
                      className="py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-sm transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
                    >
                      {isComparing ? (
                        <>
                          <RefreshCw className="w-4 h-4 animate-spin" />
                          <span>Running Benchmark...</span>
                        </>
                      ) : (
                        <>
                          <Play className="w-4 h-4 fill-current" />
                          <span>Benchmark All 4 Algorithms</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* Benchmark Results Grid */}
                {compareResults ? (
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      {compareResults.results.map((res, i) => (
                        <div
                          key={i}
                          className="bg-white rounded-2xl border border-slate-200 shadow-xs p-5 flex flex-col justify-between space-y-3"
                        >
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-xs font-bold uppercase tracking-wider text-indigo-700">
                                {res.algorithm}
                              </span>
                              <span
                                className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                                  res.path_found
                                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                    : 'bg-rose-50 text-rose-700 border border-rose-200'
                                }`}
                              >
                                {res.path_found ? 'Target Reached' : 'Unreachable'}
                              </span>
                            </div>

                            {/* Metrics Strip */}
                            <div className="grid grid-cols-2 gap-2 my-3 text-center">
                              <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                                <span className="text-[10px] text-slate-400 uppercase font-semibold block">
                                  Path Edges
                                </span>
                                <span className="text-sm font-bold text-slate-900 font-mono">
                                  {res.edge_count}
                                </span>
                              </div>
                              <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">
                                <span className="text-[10px] text-slate-400 uppercase font-semibold block">
                                  Nodes Explored
                                </span>
                                <span className="text-sm font-bold text-indigo-600 font-mono">
                                  {res.nodes_explored_count}
                                </span>
                              </div>
                            </div>

                            <div className="text-[11px] text-slate-600 flex items-center justify-between pb-2 border-b border-slate-100">
                              <span className="text-slate-400">Runtime:</span>
                              <span className="font-mono font-semibold text-slate-800">
                                {res.duration_ms.toFixed(2)} ms
                              </span>
                            </div>

                            {/* Path sequence */}
                            <div className="pt-2">
                              <span className="text-[10px] font-bold uppercase text-slate-400 block mb-1">
                                Discovered Route:
                              </span>
                              {res.path.length > 0 ? (
                                <div className="text-[11px] font-mono text-slate-700 bg-slate-50 p-2 rounded-lg border border-slate-100 break-words leading-relaxed">
                                  {res.path.join(' → ')}
                                </div>
                              ) : (
                                <div className="text-[11px] text-slate-400 italic">
                                  No directed path exists
                                </div>
                              )}
                            </div>
                          </div>

                          {/* Optimality Note */}
                          <div className="p-2 bg-slate-50 rounded-lg text-[10px] text-slate-500 leading-tight border border-slate-100">
                            <strong>Note:</strong> {res.optimality_note}
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Scientific Analysis Card */}
                    <div className="bg-indigo-50/70 border border-indigo-200/80 rounded-2xl p-5 text-xs text-indigo-950 space-y-2">
                      <div className="flex items-center space-x-2 text-indigo-800 font-bold">
                        <Info className="w-4 h-4" />
                        <span>Academic Analysis: Uninformed vs. Informed Search on Directed Graphs</span>
                      </div>
                      <p className="leading-relaxed text-indigo-900">
                        {compareResults.explanation}
                      </p>
                      <div className="pt-2 text-[11px] text-indigo-800/80 leading-relaxed border-t border-indigo-200/60">
                        <strong>Correctness Distinctions:</strong>
                        <ul className="list-disc pl-5 mt-1 space-y-1">
                          <li>
                            <strong>BFS & Bidirectional:</strong> Guarantee shortest paths in edge count on unweighted graphs. Directed Bidirectional search expands forward from start and backward along incoming edges from target.
                          </li>
                          <li>
                            <strong>Greedy Best-First:</strong> Prioritizes nodes closest to goal according to heuristic $h(n)$. It is informed but <em>not guaranteed optimal</em> without an admissible evaluation function ($A^*$).
                          </li>
                          <li>
                            <strong>Prerequisite Ordering vs. Single Path:</strong> Finding a shortest connection does not replace full prerequisite closure. A student reaching Machine Learning must complete Linear Algebra and Probability even if they do not lie on the shortest single-path edge sequence!
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="bg-white p-12 rounded-2xl border border-slate-200 text-center text-slate-400 text-xs">
                    Select a start topic and goal topic above and click "Benchmark All 4 Algorithms" to inspect real execution metrics.
                  </div>
                )}
              </div>
            )}

            {/* ========================================================= */}
            {/* TAB 3: CSP STUDY SCHEDULER */}
            {/* ========================================================= */}
            {activeTab === 'scheduler' && (
              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {/* Header & Constraints Form */}
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-4">
                  <div>
                    <h2 className="text-sm font-bold text-slate-900 tracking-tight flex items-center space-x-2">
                      <Calendar className="w-4 h-4 text-indigo-600" />
                      <span>Constraint Satisfaction Problem (CSP) Study Scheduler</span>
                    </h2>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Uses Backtracking Search to assign topic sessions to valid timetable slots while strictly respecting daily limits, non-overlapping times, and prerequisite order.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {/* Available Days */}
                    <div className="space-y-1.5">
                      <label className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">
                        Available Study Days
                      </label>
                      <div className="flex flex-wrap gap-1">
                        {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].map(
                          (day) => {
                            const isSelected = availableDays.includes(day);
                            return (
                              <button
                                key={day}
                                onClick={() => toggleDay(day)}
                                className={`px-2 py-1 rounded-lg text-xs font-semibold transition-all ${
                                  isSelected
                                    ? 'bg-indigo-600 text-white'
                                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                }`}
                              >
                                {day.slice(0, 3)}
                              </button>
                            );
                          }
                        )}
                      </div>
                    </div>

                    {/* Daily Max Hours */}
                    <div className="space-y-1.5">
                      <label className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">
                        Max Hours / Day: <span className="text-indigo-600">{maxDailyHours}h</span>
                      </label>
                      <input
                        type="range"
                        min="1"
                        max="6"
                        value={maxDailyHours}
                        onChange={(e) => setMaxDailyHours(Number(e.target.value))}
                        className="w-full accent-indigo-600 cursor-pointer"
                      />
                      <div className="flex justify-between text-[10px] text-slate-400">
                        <span>1 hr</span>
                        <span>3 hrs</span>
                        <span>6 hrs</span>
                      </div>
                    </div>

                    {/* Session Block Duration */}
                    <div className="space-y-1.5">
                      <label className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">
                        Session Block Duration
                      </label>
                      <div className="flex items-center space-x-2">
                        {[1, 2].map((dur) => (
                          <button
                            key={dur}
                            onClick={() => setPreferredSessionHours(dur)}
                            className={`flex-1 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
                              preferredSessionHours === dur
                                ? 'bg-indigo-50 border-indigo-300 text-indigo-700'
                                : 'bg-slate-50 border-slate-200 text-slate-600'
                            }`}
                          >
                            {dur} Hour{dur > 1 ? 's' : ''}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Horizon Weeks */}
                    <div className="space-y-1.5">
                      <label className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">
                        Planning Horizon
                      </label>
                      <div className="flex items-center space-x-2">
                        {[1, 2, 3, 4].map((w) => (
                          <button
                            key={w}
                            onClick={() => setPlanningWeeks(w)}
                            className={`flex-1 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
                              planningWeeks === w
                                ? 'bg-indigo-50 border-indigo-300 text-indigo-700'
                                : 'bg-slate-50 border-slate-200 text-slate-600'
                            }`}
                          >
                            {w}w
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="pt-2 flex justify-end">
                    <button
                      onClick={handleGenerateSchedule}
                      disabled={isScheduling}
                      className="py-2.5 px-5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-sm transition-all flex items-center space-x-2 disabled:opacity-50"
                    >
                      {isScheduling ? (
                        <>
                          <RefreshCw className="w-4 h-4 animate-spin" />
                          <span>Executing Backtracking CSP Solver...</span>
                        </>
                      ) : (
                        <>
                          <Play className="w-4 h-4 fill-current" />
                          <span>Generate Study Schedule</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* Scheduler Results */}
                {scheduleResult ? (
                  <div className="space-y-4">
                    {/* Status & Constraint Metrics */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
                        <span className="text-[10px] text-slate-400 uppercase font-semibold block">
                          Feasibility Status
                        </span>
                        <div className="flex items-center space-x-1.5 mt-1">
                          {scheduleResult.is_feasible ? (
                            <span className="inline-flex items-center text-xs font-bold text-emerald-700">
                              <CheckCircle2 className="w-4 h-4 mr-1 text-emerald-500" />
                              Valid Timetable Found
                            </span>
                          ) : (
                            <span className="inline-flex items-center text-xs font-bold text-rose-700">
                              <AlertCircle className="w-4 h-4 mr-1 text-rose-500" />
                              Infeasible / Over Capacity
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
                        <span className="text-[10px] text-slate-400 uppercase font-semibold block">
                          Hours Required vs Capacity
                        </span>
                        <div className="text-xs font-bold text-slate-900 font-mono mt-1">
                          {scheduleResult.total_hours_required}h required / {scheduleResult.available_capacity_hours}h max
                        </div>
                      </div>

                      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
                        <span className="text-[10px] text-slate-400 uppercase font-semibold block">
                          CSP Backtracks Triggered
                        </span>
                        <div className="text-xs font-bold text-indigo-600 font-mono mt-1">
                          {scheduleResult.backtrack_count} backtracks ({scheduleResult.assignments_tried} assignments)
                        </div>
                      </div>

                      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
                        <span className="text-[10px] text-slate-400 uppercase font-semibold block">
                          Solver Duration
                        </span>
                        <div className="text-xs font-bold text-slate-900 font-mono mt-1">
                          {scheduleResult.duration_ms.toFixed(2)} ms
                        </div>
                      </div>
                    </div>

                    {/* Infeasibility or Feasibility Explanation */}
                    <div
                      className={`p-4 rounded-xl border text-xs leading-relaxed ${
                        scheduleResult.is_feasible
                          ? 'bg-emerald-50/60 border-emerald-200 text-emerald-950'
                          : 'bg-rose-50/70 border-rose-200 text-rose-950'
                      }`}
                    >
                      <strong className="block mb-1">
                        {scheduleResult.is_feasible
                          ? 'Timetable Constraint Verification:'
                          : 'Constraint Conflict Explanation:'}
                      </strong>
                      <p>{scheduleResult.explanation}</p>
                    </div>

                    {/* Scheduled Timetable Sessions */}
                    {scheduleResult.is_feasible && scheduleResult.sessions.length > 0 && (
                      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-3">
                        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                          Assigned Study Sessions ({scheduleResult.sessions.length} sessions)
                        </h3>

                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                          {scheduleResult.sessions.map((session, idx) => (
                            <div
                              key={idx}
                              className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80 hover:bg-white hover:shadow-xs transition-all space-y-1.5"
                            >
                              <div className="flex items-center justify-between">
                                <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-indigo-100 text-indigo-800 font-mono">
                                  {session.day} Slot {session.slot_index + 1}
                                </span>
                                <span className="text-[10px] text-slate-500 font-semibold">
                                  {session.duration_hours} hr
                                </span>
                              </div>
                              <h4 className="text-xs font-bold text-slate-900 truncate">
                                {session.topic_name}
                              </h4>
                              <div className="text-[10px] text-slate-400 flex items-center justify-between">
                                <span>Part {session.session_number} of {session.total_sessions_for_topic}</span>
                                <span className="text-emerald-600 font-medium">✓ Consistent</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="bg-white p-12 rounded-2xl border border-slate-200 text-center text-slate-400 text-xs">
                    Configure your available days and time limits above and click "Generate Study Schedule" to run the CSP solver.
                  </div>
                )}
              </div>
            )}

            {/* ========================================================= */}
            {/* TAB 4: LIVE SEARCH EXECUTION TRACE (PROOFLENS) */}
            {/* ========================================================= */}
            {activeTab === 'trace' && (
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-xl bg-brand-50 border border-brand-200 flex items-center justify-center text-brand-600">
                      <ShieldCheck className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-slate-900">{traceTitle}</h3>
                      <p className="text-xs text-slate-500">
                        Inspecting real algorithmic execution stages, timing, and evidence grounding.
                      </p>
                    </div>
                  </div>

                  <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                    {activeTrace.length} Execution Stages
                  </span>
                </div>

                {activeTrace.length > 0 ? (
                  <div className="space-y-2.5">
                    {activeTrace.map((step, idx) => (
                      <div
                        key={step.id || idx}
                        className="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs space-y-2"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2.5">
                            <span className="w-6 h-6 rounded-md bg-indigo-50 text-indigo-700 border border-indigo-200 text-[11px] font-bold flex items-center justify-center">
                              {String(idx + 1).padStart(2, '0')}
                            </span>
                            <div>
                              <div className="flex items-center space-x-2">
                                <span className="text-xs font-bold text-slate-900">
                                  {step.stage}
                                </span>
                                <span className="text-[9px] uppercase px-1.5 py-0.2 rounded font-semibold bg-slate-100 text-slate-600">
                                  {step.execution_type}
                                </span>
                              </div>
                              <span className="text-[11px] text-slate-500">{step.method}</span>
                            </div>
                          </div>

                          <span className="text-xs font-mono font-bold text-slate-700">
                            {step.duration_ms.toFixed(2)} ms
                          </span>
                        </div>

                        <p className="text-xs text-slate-600 leading-relaxed pl-8">
                          {step.description}
                        </p>

                        {(step.input_summary || step.output_summary) && (
                          <div className="pl-8 grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 text-[11px]">
                            {step.input_summary && (
                              <div className="p-2 bg-slate-50 rounded-lg border border-slate-100 font-mono text-[10px] text-slate-700">
                                <strong className="text-slate-500 block">Input:</strong>
                                {step.input_summary}
                              </div>
                            )}
                            {step.output_summary && (
                              <div className="p-2 bg-slate-50 rounded-lg border border-slate-100 font-mono text-[10px] text-slate-700">
                                <strong className="text-slate-500 block">Output:</strong>
                                {step.output_summary}
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="bg-white p-12 rounded-2xl border border-slate-200 text-center text-slate-400 text-xs">
                    No execution trace captured yet. Run a search path, benchmark comparison, or schedule in the other tabs.
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default PathForgeView;
