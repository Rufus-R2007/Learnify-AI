import React, { useState, useEffect, useMemo } from 'react';
import {
  FlaskConical,
  Play,
  RotateCcw,
  GitCompare,
  ShieldCheck,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Sliders,
  CheckSquare,
  Square,
  ArrowRight,
  Info,
  BookmarkCheck,
} from 'lucide-react';
import {
  WhatIfPolicy,
  EvaluateWhatIfResponse,
  CompareWhatIfResponse,
  GoalProofResponse,
  ConsistencyCheckResponse,
  Message,
} from '../types';
import {
  getWhatIfPolicies,
  evaluateWhatIfScenario,
  compareWhatIfScenarios,
  proveReasoningGoal,
  checkPolicyConsistency
} from '../services/api';

interface WhatIfLabViewProps {
  onBackToChat: () => void;
  onSyncTraceToProofLens?: (message: Message) => void;
}

type DiagnosticTab = 'forward' | 'backward' | 'consistency';

export const WhatIfLabView: React.FC<WhatIfLabViewProps> = ({
  onBackToChat,
  onSyncTraceToProofLens
}) => {
  // Policies & selection state
  const [policies, setPolicies] = useState<WhatIfPolicy[]>([]);
  const [selectedPolicyId, setSelectedPolicyId] = useState<string>('policy-exam-eligibility-v1');
  const [loadingPolicies, setLoadingPolicies] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Active scenario input state
  const [entityId] = useState<string>('student_01');
  const [attendance, setAttendance] = useState<number>(68);
  const [assignmentCompleted, setAssignmentCompleted] = useState<boolean>(true);
  const [approvedExemption, setApprovedExemption] = useState<boolean>(false);
  const [gpa, setGpa] = useState<number>(3.82);
  const [creditsCompleted, setCreditsCompleted] = useState<number>(64);
  const [disciplinaryClearance, setDisciplinaryClearance] = useState<boolean>(true);
  const [includeLabClearance, setIncludeLabClearance] = useState<boolean>(false);
  const [labClearanceValue, setLabClearanceValue] = useState<boolean>(true);

  // Evaluation results
  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);
  const [evalResult, setEvalResult] = useState<EvaluateWhatIfResponse | null>(null);

  // Compare mode state
  const [isCompareMode, setIsCompareMode] = useState<boolean>(false);
  const [compareResult, setCompareResult] = useState<CompareWhatIfResponse | null>(null);
  const [baselineFactsState, setBaselineFactsState] = useState<Record<string, unknown>>({});

  // Right Diagnostic Panel State
  const [activeTab, setActiveTab] = useState<DiagnosticTab>('forward');
  const [selectedGoal, setSelectedGoal] = useState<string>('exam_eligible');
  const [isProving, setIsProving] = useState<boolean>(false);
  const [proofResult, setProofResult] = useState<GoalProofResponse | null>(null);

  // Consistency checker state
  const [isCheckingConsistency, setIsCheckingConsistency] = useState<boolean>(false);
  const [consistencyResult, setConsistencyResult] = useState<ConsistencyCheckResponse | null>(null);

  // Load policies on initial mount
  useEffect(() => {
    const fetchPolicies = async () => {
      try {
        setLoadingPolicies(true);
        const data = await getWhatIfPolicies();
        setPolicies(data.policies || []);
        if (data.policies && data.policies.length > 0) {
          const first = data.policies[0];
          setSelectedPolicyId(first.id);
          applyPolicyDefaults(first);
        }
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to load WhatIf policies from backend.');
      } finally {
        setLoadingPolicies(false);
      }
    };
    fetchPolicies();
  }, []);

  const activePolicy = useMemo(() => {
    return policies.find((p) => p.id === selectedPolicyId) || null;
  }, [policies, selectedPolicyId]);

  // Apply default presets whenever policy changes
  const applyPolicyDefaults = (policy: WhatIfPolicy) => {
    const preset = policy.baseline_preset || {};
    if (policy.id === 'policy-exam-eligibility-v1') {
      setAttendance(typeof preset.attendance_percentage === 'number' ? preset.attendance_percentage : 68);
      setAssignmentCompleted(typeof preset.assignment_completed === 'boolean' ? preset.assignment_completed : true);
      setApprovedExemption(false);
      setSelectedGoal('exam_eligible');
    } else if (policy.id === 'policy-exception-waiver-v1') {
      setAttendance(typeof preset.attendance_percentage === 'number' ? preset.attendance_percentage : 68);
      setAssignmentCompleted(typeof preset.assignment_completed === 'boolean' ? preset.assignment_completed : true);
      setApprovedExemption(typeof preset.approved_exemption === 'boolean' ? preset.approved_exemption : false);
      setSelectedGoal('exam_eligible');
    } else if (policy.id === 'policy-incomplete-info-v1') {
      setAttendance(typeof preset.attendance_percentage === 'number' ? preset.attendance_percentage : 78);
      setAssignmentCompleted(typeof preset.assignment_completed === 'boolean' ? preset.assignment_completed : true);
      setIncludeLabClearance(false);
      setSelectedGoal('semester_passed');
    } else if (policy.id === 'policy-academic-honors-v1') {
      setGpa(typeof preset.gpa === 'number' ? preset.gpa : 3.82);
      setCreditsCompleted(typeof preset.credits_completed === 'number' ? preset.credits_completed : 64);
      setDisciplinaryClearance(typeof preset.disciplinary_clearance === 'boolean' ? preset.disciplinary_clearance : true);
      setSelectedGoal('academic_honors');
    }
  };

  const handlePolicyChange = (newPolicyId: string) => {
    setSelectedPolicyId(newPolicyId);
    const pol = policies.find((p) => p.id === newPolicyId);
    if (pol) {
      applyPolicyDefaults(pol);
      setIsCompareMode(false);
      setCompareResult(null);
      setProofResult(null);
      setConsistencyResult(null);
    }
  };

  // Build the current fact payload based on the selected policy
  const buildCurrentFacts = (): Record<string, unknown> => {
    const facts: Record<string, unknown> = {};
    if (selectedPolicyId === 'policy-academic-honors-v1') {
      facts.gpa = gpa;
      facts.credits_completed = creditsCompleted;
      facts.disciplinary_clearance = disciplinaryClearance;
    } else if (selectedPolicyId === 'policy-incomplete-info-v1') {
      facts.attendance_percentage = attendance;
      facts.assignment_completed = assignmentCompleted;
      if (includeLabClearance) {
        facts.lab_clearance = labClearanceValue;
      }
    } else if (selectedPolicyId === 'policy-exception-waiver-v1') {
      facts.attendance_percentage = attendance;
      facts.assignment_completed = assignmentCompleted;
      facts.approved_exemption = approvedExemption;
    } else {
      // Default: Exam eligibility
      facts.attendance_percentage = attendance;
      facts.assignment_completed = assignmentCompleted;
    }
    return facts;
  };

  // Evaluate current scenario
  const handleEvaluate = async () => {
    if (!selectedPolicyId) return;
    try {
      setIsEvaluating(true);
      setError(null);
      const currentFacts = buildCurrentFacts();
      const res = await evaluateWhatIfScenario(selectedPolicyId, currentFacts, entityId);
      setEvalResult(res);

      if (isCompareMode && Object.keys(baselineFactsState).length > 0) {
        // Run comparison
        const comp = await compareWhatIfScenarios(
          selectedPolicyId,
          baselineFactsState,
          currentFacts,
          entityId
        );
        setCompareResult(comp);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Evaluation failed.');
    } finally {
      setIsEvaluating(false);
    }
  };

  // Evaluate automatically on initial load or policy change
  useEffect(() => {
    if (activePolicy) {
      handleEvaluate();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedPolicyId]);

  // Activate Compare Mode: record baseline facts and compare with modified
  const handleToggleCompare = async () => {
    if (!isCompareMode) {
      // Entering compare mode: lock current facts as baseline
      const currentFacts = buildCurrentFacts();
      setBaselineFactsState(currentFacts);
      setIsCompareMode(true);
    } else {
      setIsCompareMode(false);
      setCompareResult(null);
    }
  };

  // Reset inputs to baseline preset
  const handleResetToBaseline = () => {
    if (activePolicy) {
      applyPolicyDefaults(activePolicy);
    }
  };

  // Run Backward Chaining Goal Diagnosis
  const handleProveGoal = async () => {
    if (!selectedPolicyId || !selectedGoal) return;
    try {
      setIsProving(true);
      setError(null);
      const currentFacts = buildCurrentFacts();
      const res = await proveReasoningGoal(
        selectedPolicyId,
        selectedGoal,
        true,
        entityId,
        currentFacts
      );
      setProofResult(res);
      setActiveTab('backward');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Backward goal diagnosis failed.');
    } finally {
      setIsProving(false);
    }
  };

  // Run Propositional Resolution Consistency Check
  const handleCheckConsistency = async () => {
    if (!selectedPolicyId) return;
    try {
      setIsCheckingConsistency(true);
      setError(null);
      const res = await checkPolicyConsistency(selectedPolicyId);
      setConsistencyResult(res);
      setActiveTab('consistency');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Consistency check failed.');
    } finally {
      setIsCheckingConsistency(false);
    }
  };

  // Forward trace to ProofLens panel in main app
  const handleSyncToProofLens = () => {
    if (!onSyncTraceToProofLens) return;

    const trace = evalResult?.trace || [];
    const decision = evalResult?.result?.decision_status || 'SATISFIED';
    const explanation = evalResult?.result?.explanation || 'Scenario evaluation completed.';

    const syntheticMsg: Message = {
      id: `whatif-${Date.now()}`,
      role: 'assistant',
      content: `### WhatIf Lab Decision Simulation\n\n**Policy:** ${activePolicy?.name || selectedPolicyId}\n**Decision Status:** \`${decision}\`\n\n${explanation}\n\n*(Verified via Forward Chaining Deduction & Declarative Rule Engine)*`,
      timestamp: new Date(),
      conceptsUsed: [
        'Forward Chaining Deduction',
        'Declarative Production Rules',
        'First-Order Predicate Logic',
        'Truth Maintenance & Epistemic Uncertainty'
      ],
      matchScore: 1.0,
      sources: [
        {
          id: 'src-whatif-simulator',
          name: activePolicy?.name || 'Academic Policy Specification',
          description: activePolicy?.description || 'Declarative academic rule base'
        }
      ],
      trace: trace,
      status: 'answered'
    };

    onSyncTraceToProofLens(syntheticMsg);
  };

  const statusColor = (status?: string) => {
    switch (status) {
      case 'SATISFIED':
        return {
          bg: 'bg-emerald-50 border-emerald-300 text-emerald-800',
          badge: 'bg-emerald-600 text-white',
          icon: <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
        };
      case 'NOT_SATISFIED':
        return {
          bg: 'bg-rose-50 border-rose-300 text-rose-800',
          badge: 'bg-rose-600 text-white',
          icon: <XCircle className="w-5 h-5 text-rose-600 shrink-0" />
        };
      case 'INCONCLUSIVE':
        return {
          bg: 'bg-amber-50 border-amber-300 text-amber-800',
          badge: 'bg-amber-600 text-white',
          icon: <AlertCircle className="w-5 h-5 text-amber-600 shrink-0" />
        };
      case 'OVERRIDDEN':
        return {
          bg: 'bg-purple-50 border-purple-300 text-purple-800',
          badge: 'bg-purple-600 text-white',
          icon: <ShieldCheck className="w-5 h-5 text-purple-600 shrink-0" />
        };
      default:
        return {
          bg: 'bg-slate-50 border-slate-300 text-slate-800',
          badge: 'bg-slate-600 text-white',
          icon: <Info className="w-5 h-5 text-slate-600 shrink-0" />
        };
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-50 overflow-hidden font-sans">
      {/* 1. Header Toolbar */}
      <header className="px-6 py-3.5 bg-white border-b border-slate-200/80 flex items-center justify-between shadow-2xs z-10 shrink-0">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-600 to-emerald-500 flex items-center justify-center text-white shadow-md shadow-teal-500/20">
            <FlaskConical className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-base font-bold text-slate-900 tracking-tight">WhatIf Lab</h1>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-teal-50 text-teal-800 border border-teal-200">
                Phase 3 Live
              </span>
              <span className="hidden sm:inline-block text-[11px] text-slate-400">
                • Symbolic AI & Decision Workbench
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              Responsible Developer: <strong className="text-slate-700">URK25CS1034 — Hiran Antony</strong>
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {onSyncTraceToProofLens && evalResult?.trace && (
            <button
              onClick={handleSyncToProofLens}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-brand-50 hover:bg-brand-100 text-brand-700 border border-brand-200/80 transition-colors shadow-2xs"
              title="Sync current trace to ProofLens panel"
            >
              <ShieldCheck className="w-4 h-4 text-brand-600" />
              <span className="hidden sm:inline">Send to ProofLens</span>
            </button>
          )}

          <button
            onClick={onBackToChat}
            className="px-3 py-1.5 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200 transition-colors"
          >
            Back to Chat
          </button>
        </div>
      </header>

      {/* 2. Mandatory Illustrative Disclaimer Banner */}
      <div className="bg-amber-50/90 border-b border-amber-200 px-6 py-2 flex items-center space-x-2 text-xs text-amber-900 shrink-0">
        <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
        <span className="leading-tight">
          <strong>Illustrative Demo Data:</strong> Policies, thresholds, and student records are synthetic examples created exclusively to demonstrate symbolic logic, first-order resolution, and production rule engines. They do <em>not</em> represent official Karunya University regulations.
        </span>
      </div>

      {/* 3. Main 3-Panel Workspace */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-0 overflow-hidden">
        {/* =========================================================================
            PANEL 1: WHAT-IF INPUTS & POLICY SELECTOR (LEFT: 4 cols)
            ========================================================================= */}
        <section className="lg:col-span-4 bg-white border-r border-slate-200 flex flex-col h-full overflow-hidden">
          <div className="p-4 border-b border-slate-100 bg-slate-50/70 flex items-center justify-between shrink-0">
            <div className="flex items-center space-x-2">
              <Sliders className="w-4 h-4 text-teal-600" />
              <h2 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                1. Scenario Inputs
              </h2>
            </div>
            <div className="flex items-center space-x-1.5">
              <button
                onClick={handleResetToBaseline}
                className="p-1.5 rounded-lg text-slate-500 hover:text-slate-700 hover:bg-white text-xs border border-transparent hover:border-slate-200 transition-all flex items-center space-x-1"
                title="Reset sliders to policy baseline preset"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span className="text-[11px]">Reset</span>
              </button>
            </div>
          </div>

          <div className="flex-1 p-5 overflow-y-auto space-y-5">
            {/* Policy Selector */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-800 block">
                Target Policy & Regulations
              </label>
              {loadingPolicies ? (
                <div className="text-xs text-slate-400 py-2">Loading demonstration policies...</div>
              ) : (
                <select
                  value={selectedPolicyId}
                  onChange={(e) => handlePolicyChange(e.target.value)}
                  className="w-full text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 transition-all cursor-pointer"
                >
                  {policies.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name}
                    </option>
                  ))}
                </select>
              )}
              {activePolicy && (
                <p className="text-[11px] text-slate-500 leading-relaxed pt-1">
                  {activePolicy.description}
                </p>
              )}
            </div>

            <div className="border-t border-slate-100 pt-4 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                  Configurable Antecedents
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-mono">
                  {entityId}
                </span>
              </div>

              {/* Dynamic Inputs based on policy */}
              {selectedPolicyId === 'policy-academic-honors-v1' ? (
                /* Academic Honors Policy Inputs */
                <>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <label className="text-xs font-medium text-slate-700">Cumulative GPA</label>
                      <span className="text-xs font-bold text-teal-700 font-mono bg-teal-50 px-2 py-0.5 rounded">
                        {gpa.toFixed(2)} / 4.00
                      </span>
                    </div>
                    <input
                      type="range"
                      min={2.0}
                      max={4.0}
                      step={0.05}
                      value={gpa}
                      onChange={(e) => setGpa(parseFloat(e.target.value))}
                      className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600"
                    />
                    <div className="flex justify-between text-[10px] text-slate-400">
                      <span>2.00</span>
                      <span className="text-teal-600 font-semibold">Min 3.75 (Honors)</span>
                      <span>4.00</span>
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-medium text-slate-700 block">
                      Credits Completed
                    </label>
                    <input
                      type="number"
                      value={creditsCompleted}
                      onChange={(e) => setCreditsCompleted(parseInt(e.target.value) || 0)}
                      min={0}
                      max={180}
                      className="w-full text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-800"
                    />
                    <p className="text-[10px] text-slate-400">Honors requires ≥ 60 credit hours.</p>
                  </div>

                  <div className="pt-2">
                    <button
                      type="button"
                      onClick={() => setDisciplinaryClearance(!disciplinaryClearance)}
                      className={`w-full flex items-center justify-between p-3 rounded-xl border transition-all text-xs ${
                        disciplinaryClearance
                          ? 'bg-teal-50/70 border-teal-300 text-teal-900 font-semibold'
                          : 'bg-slate-50 border-slate-200 text-slate-600'
                      }`}
                    >
                      <div className="flex items-center space-x-2">
                        {disciplinaryClearance ? (
                          <CheckSquare className="w-4 h-4 text-teal-600" />
                        ) : (
                          <Square className="w-4 h-4 text-slate-400" />
                        )}
                        <span>Disciplinary Clearance Record</span>
                      </div>
                      <span className="text-[10px] font-mono text-slate-500">
                        {disciplinaryClearance ? 'CLEARED' : 'FLAGGED'}
                      </span>
                    </button>
                  </div>
                </>
              ) : selectedPolicyId === 'policy-incomplete-info-v1' ? (
                /* Incomplete Information Diagnostic Policy Inputs */
                <>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <label className="text-xs font-medium text-slate-700">Course Attendance</label>
                      <span className="text-xs font-bold text-teal-700 font-mono bg-teal-50 px-2 py-0.5 rounded">
                        {attendance}%
                      </span>
                    </div>
                    <input
                      type="range"
                      min={0}
                      max={100}
                      step={1}
                      value={attendance}
                      onChange={(e) => setAttendance(parseInt(e.target.value))}
                      className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600"
                    />
                  </div>

                  <div>
                    <button
                      type="button"
                      onClick={() => setAssignmentCompleted(!assignmentCompleted)}
                      className={`w-full flex items-center justify-between p-3 rounded-xl border transition-all text-xs ${
                        assignmentCompleted
                          ? 'bg-teal-50/70 border-teal-300 text-teal-900 font-semibold'
                          : 'bg-slate-50 border-slate-200 text-slate-600'
                      }`}
                    >
                      <div className="flex items-center space-x-2">
                        {assignmentCompleted ? (
                          <CheckSquare className="w-4 h-4 text-teal-600" />
                        ) : (
                          <Square className="w-4 h-4 text-slate-400" />
                        )}
                        <span>Continuous Assessment Assignments</span>
                      </div>
                      <span className="text-[10px] font-mono text-slate-500">
                        {assignmentCompleted ? 'COMPLETED' : 'PENDING'}
                      </span>
                    </button>
                  </div>

                  {/* Missing Fact Demonstration Toggle */}
                  <div className="p-3 bg-amber-50/60 border border-amber-200 rounded-xl space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-amber-900">Lab Clearance Record</span>
                      <span className="text-[10px] px-1.5 py-0.2 rounded bg-amber-200 text-amber-800 font-mono">
                        {includeLabClearance ? 'Recorded' : 'Unrecorded / Missing'}
                      </span>
                    </div>
                    <p className="text-[11px] text-amber-800 leading-tight">
                      When unrecorded, the agent marks conclusion as <code>INCONCLUSIVE</code> rather than assuming false.
                    </p>
                    <div className="flex items-center space-x-2 pt-1">
                      <button
                        type="button"
                        onClick={() => setIncludeLabClearance(!includeLabClearance)}
                        className="text-xs px-2.5 py-1 rounded-lg bg-amber-600 text-white font-medium hover:bg-amber-700 transition-colors"
                      >
                        {includeLabClearance ? 'Remove Record' : 'Record Lab Fact'}
                      </button>
                      {includeLabClearance && (
                        <button
                          type="button"
                          onClick={() => setLabClearanceValue(!labClearanceValue)}
                          className="text-xs px-2 py-1 rounded-lg bg-white border border-amber-300 text-amber-900"
                        >
                          Status: {labClearanceValue ? 'Passed (True)' : 'Failed (False)'}
                        </button>
                      )}
                    </div>
                  </div>
                </>
              ) : (
                /* Standard Exam Eligibility & Exception Waiver Inputs */
                <>
                  {/* Attendance Slider */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <label className="text-xs font-medium text-slate-700">Course Attendance</label>
                      <span
                        className={`text-xs font-bold font-mono px-2 py-0.5 rounded ${
                          attendance >= 75
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : attendance >= 65
                            ? 'bg-amber-50 text-amber-700 border border-amber-200'
                            : 'bg-rose-50 text-rose-700 border border-rose-200'
                        }`}
                      >
                        {attendance}%
                      </span>
                    </div>
                    <input
                      type="range"
                      min={0}
                      max={100}
                      step={1}
                      value={attendance}
                      onChange={(e) => setAttendance(parseInt(e.target.value))}
                      className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600"
                    />
                    <div className="flex justify-between text-[10px] text-slate-400">
                      <span>0%</span>
                      <span className="text-amber-600 font-semibold">65% (Waiver Req)</span>
                      <span className="text-emerald-600 font-semibold">75% (Standard)</span>
                      <span>100%</span>
                    </div>
                  </div>

                  {/* Assignment Toggle */}
                  <div>
                    <button
                      type="button"
                      onClick={() => setAssignmentCompleted(!assignmentCompleted)}
                      className={`w-full flex items-center justify-between p-3 rounded-xl border transition-all text-xs ${
                        assignmentCompleted
                          ? 'bg-teal-50/70 border-teal-300 text-teal-900 font-semibold'
                          : 'bg-slate-50 border-slate-200 text-slate-600'
                      }`}
                    >
                      <div className="flex items-center space-x-2">
                        {assignmentCompleted ? (
                          <CheckSquare className="w-4 h-4 text-teal-600" />
                        ) : (
                          <Square className="w-4 h-4 text-slate-400" />
                        )}
                        <span>Continuous Assessment Assignments</span>
                      </div>
                      <span className="text-[10px] font-mono text-slate-500">
                        {assignmentCompleted ? 'COMPLETED' : 'PENDING'}
                      </span>
                    </button>
                  </div>

                  {/* Approved Exemption Toggle (Nonmonotonic Override) */}
                  <div className="p-3 bg-purple-50/60 border border-purple-200 rounded-xl space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-purple-900 flex items-center space-x-1.5">
                        <ShieldCheck className="w-4 h-4 text-purple-600" />
                        <span>Approved Medical / Sports Waiver</span>
                      </span>
                      <span className="text-[10px] px-1.5 py-0.2 rounded bg-purple-200 text-purple-800 font-mono">
                        Nonmonotonic
                      </span>
                    </div>
                    <p className="text-[11px] text-purple-800 leading-tight">
                      When approved, this declarative exception overrides the default 75% attendance constraint down to 65%.
                    </p>
                    <button
                      type="button"
                      onClick={() => setApprovedExemption(!approvedExemption)}
                      className={`w-full flex items-center justify-between p-2 rounded-lg border text-xs font-medium transition-all ${
                        approvedExemption
                          ? 'bg-purple-600 text-white border-purple-600 shadow-2xs'
                          : 'bg-white text-purple-900 border-purple-200 hover:bg-purple-50'
                      }`}
                    >
                      <span>{approvedExemption ? '✓ Exception Approved' : 'No Exception Recorded'}</span>
                      <span className="text-[10px] opacity-80">
                        {approvedExemption ? 'Active Override' : 'Default Rules Apply'}
                      </span>
                    </button>
                  </div>
                </>
              )}
            </div>

            {/* Evaluate & Compare Action Buttons */}
            <div className="pt-2 space-y-2">
              <button
                onClick={handleEvaluate}
                disabled={isEvaluating}
                className="w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-xl bg-teal-600 hover:bg-teal-700 active:scale-[0.98] text-white font-semibold text-xs shadow-md shadow-teal-600/20 transition-all cursor-pointer disabled:opacity-50"
              >
                <Play className="w-4 h-4" />
                <span>{isEvaluating ? 'Evaluating Scenario...' : 'Evaluate What-If Scenario'}</span>
              </button>

              <button
                onClick={handleToggleCompare}
                className={`w-full flex items-center justify-center space-x-2 py-2 px-3 rounded-xl border text-xs font-medium transition-all ${
                  isCompareMode
                    ? 'bg-indigo-50 border-indigo-300 text-indigo-700 font-semibold'
                    : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
                }`}
              >
                <GitCompare className="w-4 h-4 text-indigo-600" />
                <span>
                  {isCompareMode ? 'Disable Comparison Mode' : 'Compare with Baseline Scenario'}
                </span>
              </button>
            </div>
          </div>
        </section>

        {/* =========================================================================
            PANEL 2: REAL-TIME DECISION & COUNTERFACTUAL OUTCOME (CENTER: 4 cols)
            ========================================================================= */}
        <section className="lg:col-span-4 bg-slate-50 border-r border-slate-200 flex flex-col h-full overflow-hidden">
          <div className="p-4 border-b border-slate-200 bg-white flex items-center justify-between shrink-0">
            <div className="flex items-center space-x-2">
              <BookmarkCheck className="w-4 h-4 text-teal-600" />
              <h2 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                2. Evaluation Outcome
              </h2>
            </div>
            {evalResult?.result?.decision_status && (
              <span
                className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider ${
                  statusColor(evalResult.result.decision_status).badge
                }`}
              >
                {evalResult.result.decision_status}
              </span>
            )}
          </div>

          <div className="flex-1 p-5 overflow-y-auto space-y-4">
            {error && (
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800">
                {error}
              </div>
            )}

            {/* Decision Status Hero Card */}
            {evalResult?.result && (
              <div
                className={`p-4 rounded-2xl border transition-all shadow-2xs ${
                  statusColor(evalResult.result.decision_status).bg
                }`}
              >
                <div className="flex items-start space-x-3 mb-2">
                  {statusColor(evalResult.result.decision_status).icon}
                  <div>
                    <h3 className="text-sm font-bold tracking-tight">
                      Decision:{' '}
                      {evalResult.result.decision_status === 'SATISFIED'
                        ? 'Eligible / Requirements Met'
                        : evalResult.result.decision_status === 'OVERRIDDEN'
                        ? 'Eligible via Exception Waiver'
                        : evalResult.result.decision_status === 'INCONCLUSIVE'
                        ? 'Inconclusive (Missing Information)'
                        : 'Not Eligible / Requirements Missing'}
                    </h3>
                    <p className="text-xs opacity-90 mt-1 leading-relaxed">
                      {evalResult.result.explanation}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Side-by-Side Counterfactual Comparison Card (If in Compare Mode) */}
            {isCompareMode && compareResult?.comparison && (
              <div className="p-4 bg-white border border-indigo-200 rounded-2xl shadow-sm space-y-3">
                <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                  <div className="flex items-center space-x-2">
                    <GitCompare className="w-4 h-4 text-indigo-600" />
                    <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                      Counterfactual Delta
                    </h4>
                  </div>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                      compareResult.comparison.decision_changed
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-slate-100 text-slate-600'
                    }`}
                  >
                    {compareResult.comparison.decision_changed ? 'Outcome Changed' : 'No Outcome Shift'}
                  </span>
                </div>

                {/* Transition Summary */}
                <div className="flex items-center justify-between p-2.5 bg-slate-50 rounded-xl text-xs">
                  <div className="text-center">
                    <span className="text-[10px] text-slate-400 block uppercase">Baseline</span>
                    <span className="font-bold text-slate-800">
                      {compareResult.comparison.baseline_status}
                    </span>
                  </div>
                  <ArrowRight className="w-4 h-4 text-indigo-500" />
                  <div className="text-center">
                    <span className="text-[10px] text-slate-400 block uppercase">Modified</span>
                    <span className="font-bold text-teal-700">
                      {compareResult.comparison.modified_status}
                    </span>
                  </div>
                </div>

                {/* Input Diffs */}
                <div className="space-y-1.5">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                    Changed Facts:
                  </span>
                  {compareResult.comparison.input_diffs.length === 0 ? (
                    <p className="text-xs text-slate-500 italic">No facts changed from baseline.</p>
                  ) : (
                    compareResult.comparison.input_diffs.map((diff, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between p-2 bg-slate-50 rounded-lg text-xs"
                      >
                        <span className="font-mono text-slate-700">{diff.predicate}</span>
                        <div className="flex items-center space-x-1.5 text-xs">
                          <span className="line-through text-slate-400">
                            {String(diff.baseline_value)}
                          </span>
                          <span className="font-bold text-teal-700">
                            {String(diff.modified_value)}
                          </span>
                        </div>
                      </div>
                    ))
                  )}
                </div>

                <p className="text-[11px] text-slate-600 bg-indigo-50/50 p-2.5 rounded-xl leading-relaxed">
                  {compareResult.comparison.delta_summary}
                </p>
              </div>
            )}

            {/* Satisfied Requirements */}
            <div className="p-4 bg-white border border-slate-200 rounded-2xl shadow-2xs space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-emerald-800 flex items-center space-x-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Satisfied Conditions</span>
                </span>
                <span className="text-[10px] font-mono text-slate-400">
                  {evalResult?.result?.satisfied_conditions?.length || 0} Met
                </span>
              </div>
              {evalResult?.result?.satisfied_conditions &&
              evalResult.result.satisfied_conditions.length > 0 ? (
                <div className="space-y-1.5 pt-1">
                  {evalResult.result.satisfied_conditions.map((sc, i) => (
                    <div
                      key={i}
                      className="p-2 bg-emerald-50/60 border border-emerald-100 rounded-lg text-xs text-emerald-900 flex items-start space-x-2"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 mt-0.5 shrink-0" />
                      <div className="min-w-0">
                        <span className="font-medium block">{sc.condition}</span>
                        <span className="text-[10px] text-emerald-700/80 font-mono">
                          Actual value: {String(sc.actual_value)} (via Rule {sc.rule_id})
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400 italic">No requirements met yet.</p>
              )}
            </div>

            {/* Unsatisfied Requirements */}
            {evalResult?.result?.unsatisfied_conditions &&
              evalResult.result.unsatisfied_conditions.length > 0 && (
                <div className="p-4 bg-white border border-rose-200 rounded-2xl shadow-2xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-rose-800 flex items-center space-x-1.5">
                      <XCircle className="w-3.5 h-3.5 text-rose-600" />
                      <span>Unsatisfied Conditions</span>
                    </span>
                    <span className="text-[10px] font-mono text-rose-600">
                      {evalResult.result.unsatisfied_conditions.length} Missing
                    </span>
                  </div>
                  <div className="space-y-1.5 pt-1">
                    {evalResult.result.unsatisfied_conditions.map((uc, i) => (
                      <div
                        key={i}
                        className="p-2 bg-rose-50/60 border border-rose-100 rounded-lg text-xs text-rose-900 space-y-0.5"
                      >
                        <div className="font-medium flex items-center justify-between">
                          <span>{uc.condition}</span>
                          <span className="text-[10px] font-mono text-rose-700">
                            Actual: {String(uc.actual_value)}
                          </span>
                        </div>
                        <p className="text-[10px] text-rose-700 leading-tight">{uc.reason}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            {/* Missing / Unrecorded Information (Epistemic Uncertainty) */}
            {evalResult?.result?.missing_facts && evalResult.result.missing_facts.length > 0 && (
              <div className="p-4 bg-amber-50 border border-amber-200 rounded-2xl shadow-2xs space-y-2">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="w-4 h-4 text-amber-600" />
                  <span className="text-xs font-bold text-amber-900">
                    Epistemic Uncertainty (Missing Facts)
                  </span>
                </div>
                <p className="text-xs text-amber-800 leading-relaxed">
                  The knowledge base contains no record for:{' '}
                  {evalResult.result.missing_facts.map((mf, i) => (
                    <code
                      key={i}
                      className="mx-1 px-1.5 py-0.5 bg-amber-100 text-amber-900 rounded font-mono text-[11px]"
                    >
                      {mf}
                    </code>
                  ))}
                  . Rather than falsifying, Learnify AI marks this state as indeterminate.
                </p>
              </div>
            )}
          </div>
        </section>

        {/* =========================================================================
            PANEL 3: SYMBOLIC REASONING & PROOFLENS TRACES (RIGHT: 4 cols)
            ========================================================================= */}
        <section className="lg:col-span-4 bg-white flex flex-col h-full overflow-hidden">
          {/* Diagnostic Tabs */}
          <div className="p-2 border-b border-slate-200 bg-slate-50/70 flex items-center justify-between shrink-0">
            <div className="flex items-center space-x-1">
              <button
                onClick={() => setActiveTab('forward')}
                className={`px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  activeTab === 'forward'
                    ? 'bg-white text-teal-700 font-bold shadow-2xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Forward Steps
              </button>
              <button
                onClick={() => setActiveTab('backward')}
                className={`px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  activeTab === 'backward'
                    ? 'bg-white text-teal-700 font-bold shadow-2xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Backward Diagnostic
              </button>
              <button
                onClick={() => setActiveTab('consistency')}
                className={`px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  activeTab === 'consistency'
                    ? 'bg-white text-teal-700 font-bold shadow-2xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Resolution
              </button>
            </div>
          </div>

          <div className="flex-1 p-5 overflow-y-auto space-y-4">
            {/* TAB 1: Forward Chaining Steps & Rule Activation Trace */}
            {activeTab === 'forward' && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                    Forward Deduction Trace
                  </span>
                  <span className="text-[10px] font-mono text-slate-400">
                    {evalResult?.result?.fired_steps?.length || 0} Rules Fired
                  </span>
                </div>

                {evalResult?.result?.fired_steps && evalResult.result.fired_steps.length > 0 ? (
                  <div className="space-y-2.5">
                    {evalResult.result.fired_steps.map((st) => (
                      <div
                        key={st.step}
                        className={`p-3 rounded-xl border text-xs space-y-1.5 transition-all ${
                          st.is_exception
                            ? 'bg-purple-50/60 border-purple-200 text-purple-950'
                            : 'bg-slate-50 border-slate-200 text-slate-800'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold flex items-center space-x-1.5">
                            <span className="w-4 h-4 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center text-[10px] font-mono">
                              {st.step}
                            </span>
                            <span>{st.rule_name}</span>
                          </span>
                          {st.is_exception && (
                            <span className="text-[9px] px-1.5 py-0.2 rounded bg-purple-200 text-purple-800 font-bold">
                              EXCEPTION OVERRIDE
                            </span>
                          )}
                        </div>

                        <div className="text-[11px] text-slate-600 font-mono bg-white/70 p-1.5 rounded border border-slate-200/60">
                          Derived:{' '}
                          <strong className="text-teal-700">
                            {JSON.stringify(st.derived_conclusion)}
                          </strong>
                        </div>

                        {st.overridden_rule_id && (
                          <p className="text-[10px] text-purple-700 italic">
                            Superseded rule <code>{st.overridden_rule_id}</code> via nonmonotonic priority.
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-center text-xs text-slate-400">
                    No declarative rules were triggered by this scenario input.
                  </div>
                )}
              </div>
            )}

            {/* TAB 2: Backward Chaining Goal Diagnostic */}
            {activeTab === 'backward' && (
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-800 block">
                    Diagnostic Query: "Why Am I Eligible / Ineligible?"
                  </label>
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={selectedGoal}
                      onChange={(e) => setSelectedGoal(e.target.value)}
                      placeholder="e.g. exam_eligible or academic_honors"
                      className="flex-1 text-xs bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-800 font-mono"
                    />
                    <button
                      onClick={handleProveGoal}
                      disabled={isProving}
                      className="px-3 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-xl text-xs font-semibold shadow-2xs transition-all disabled:opacity-50"
                    >
                      {isProving ? 'Diagnosing...' : 'Prove Goal'}
                    </button>
                  </div>
                </div>

                {proofResult?.proof && (
                  <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl space-y-3">
                    <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                      <span className="text-xs font-bold text-slate-900">
                        SLD Resolution Proof Tree
                      </span>
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider ${
                          proofResult.proof.status === 'PROVEN'
                            ? 'bg-emerald-100 text-emerald-800'
                            : proofResult.proof.status === 'CONFLICT'
                            ? 'bg-rose-100 text-rose-800'
                            : 'bg-amber-100 text-amber-800'
                        }`}
                      >
                        {proofResult.proof.status}
                      </span>
                    </div>

                    <p className="text-xs text-slate-700 leading-relaxed">
                      {proofResult.proof.explanation}
                    </p>

                    {/* Proven Path */}
                    {proofResult.proof.proven_path.length > 0 && (
                      <div className="space-y-1">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                          Proven Resolution Chain:
                        </span>
                        <div className="space-y-1 text-xs font-mono">
                          {proofResult.proof.proven_path.map((pathItem, idx) => (
                            <div
                              key={idx}
                              className="p-1.5 bg-emerald-50/70 border border-emerald-200 text-emerald-900 rounded flex items-center space-x-1.5"
                            >
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                              <span className="truncate">{pathItem}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Missing Subgoals */}
                    {proofResult.proof.missing_subgoals.length > 0 && (
                      <div className="space-y-1">
                        <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider">
                          Unsatisfied Subgoals:
                        </span>
                        <div className="space-y-1 text-xs font-mono">
                          {proofResult.proof.missing_subgoals.map((msg, idx) => (
                            <div
                              key={idx}
                              className="p-1.5 bg-rose-50/70 border border-rose-200 text-rose-900 rounded flex items-center space-x-1.5"
                            >
                              <XCircle className="w-3.5 h-3.5 text-rose-600 shrink-0" />
                              <span className="truncate">{msg}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* TAB 3: Propositional Resolution & Consistency Checker */}
            {activeTab === 'consistency' && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-800">
                      Propositional Resolution Consistency
                    </span>
                    <button
                      onClick={handleCheckConsistency}
                      disabled={isCheckingConsistency}
                      className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-2xs transition-all disabled:opacity-50"
                    >
                      {isCheckingConsistency ? 'Checking...' : 'Check Consistency'}
                    </button>
                  </div>
                  <p className="text-[11px] text-slate-500 leading-relaxed">
                    Applies the resolution theorem prover over all policy clauses to prove satisfiability or identify contradiction clauses ($\square$).
                  </p>
                </div>

                {consistencyResult && (
                  <div
                    className={`p-4 rounded-2xl border space-y-2.5 ${
                      consistencyResult.is_consistent
                        ? 'bg-emerald-50/70 border-emerald-200 text-emerald-950'
                        : 'bg-rose-50/70 border-rose-200 text-rose-950'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold flex items-center space-x-1.5">
                        {consistencyResult.is_consistent ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                        ) : (
                          <XCircle className="w-4 h-4 text-rose-600" />
                        )}
                        <span>
                          {consistencyResult.is_consistent
                            ? 'Policy Logically Consistent'
                            : 'Contradiction Detected'}
                        </span>
                      </span>
                      <span className="text-[10px] font-mono opacity-80">
                        {consistencyResult.execution_ms.toFixed(2)} ms
                      </span>
                    </div>

                    <p className="text-xs leading-relaxed">{consistencyResult.explanation}</p>

                    <div className="text-[10px] font-mono bg-white/60 p-2 rounded border border-slate-200 flex justify-between">
                      <span>Resolution Steps: {consistencyResult.steps_count}</span>
                      <span>Contradictions: {consistencyResult.contradictions_found}</span>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};

export default WhatIfLabView;
