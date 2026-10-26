import React, { useState, useEffect } from 'react';
import {
  GraduationCap,
  X,
  Users,
  CheckCircle2,
  Code2,
  FileCheck2,
  Layers,
  Loader2
} from 'lucide-react';
import { ConceptsResponse } from '../types';
import { getAIConcepts } from '../services/api';

interface SyllabusModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SyllabusModal: React.FC<SyllabusModalProps> = ({ isOpen, onClose }) => {
  const [conceptsData, setConceptsData] = useState<ConceptsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'syllabus' | 'team'>('syllabus');
  const [selectedUnitId, setSelectedUnitId] = useState<number>(1);

  useEffect(() => {
    if (isOpen) {
      loadSyllabus();
    }
  }, [isOpen]);

  const loadSyllabus = async () => {
    setLoading(true);
    try {
      const data = await getAIConcepts();
      setConceptsData(data);
    } catch (err) {
      console.error('Failed to load syllabus concepts:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const currentUnit = conceptsData?.units.find((u) => u.id === selectedUnitId);

  const teamMembers = [
    {
      regNo: 'URK25CS1063',
      name: 'Yogith Joy J',
      role: 'Phase 2 Lead',
      scope: 'Graph Search Algorithms (BFS, DFS, Bidirectional Search, Greedy Best-First), Prerequisite Topological Ordering, PathForge Interactive Engine, Constraint Satisfaction with Backtracking',
      status: 'Completed & Tested (18 Unit Tests Passing)',
      phase: 2,
      isCurrent: true,
    },
    {
      regNo: 'URK25CS1090',
      name: 'Rufus Samuel R',
      role: 'Phase 1 Lead',
      scope: 'Foundation, Intelligent Agent Architecture, ProofLens Transparent Trace Panel, SQLite Knowledge Base & Seed Data, Full-Stack UI/UX',
      status: 'Completed & Tested',
      phase: 1,
      isCurrent: false,
    },
    {
      regNo: 'URK25CS1034',
      name: 'Hiran Antony',
      role: 'Phase 3 Lead',
      scope: 'Knowledge Representation (Semantic Networks, Frames, Ontologies), First-Order Logic & Predicate Calculus, WhatIf Lab Rule-Based Engine (Forward & Backward Chaining)',
      status: 'Planned (Next Phase)',
      phase: 3,
      isCurrent: false,
    },
    {
      regNo: 'URK25CS1016',
      name: 'Naveen Kumar',
      role: 'Phase 4 Lead',
      scope: 'Machine Learning Classification, Expert System Shell, Uncertainty Reasoning (Bayesian & Certainty Factors), Quantitative Evaluation Benchmarks',
      status: 'Planned',
      phase: 4,
      isCurrent: false,
    },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-900/50 backdrop-blur-xs">
      <div className="bg-white w-full max-w-5xl h-[88vh] rounded-2xl shadow-2xl border border-slate-200/80 flex flex-col overflow-hidden animate-fade-in">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200/80 flex items-center justify-between bg-slate-50/70">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-brand-600 flex items-center justify-center text-white shadow-xs">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">
                AI Micro-Project Implementation Matrix
              </h2>
              <p className="text-xs text-slate-500">
                Five-Unit Syllabus Tracker & Team Distribution (Learnify AI)
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Top View Selector: Syllabus vs Team */}
        <div className="px-6 py-2.5 border-b border-slate-100 bg-white flex items-center space-x-3">
          <button
            onClick={() => setActiveTab('syllabus')}
            className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              activeTab === 'syllabus'
                ? 'bg-brand-50 text-brand-700 border border-brand-200'
                : 'text-slate-600 hover:bg-slate-50'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>5-Unit Syllabus Tracker</span>
          </button>

          <button
            onClick={() => setActiveTab('team')}
            className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              activeTab === 'team'
                ? 'bg-brand-50 text-brand-700 border border-brand-200'
                : 'text-slate-600 hover:bg-slate-50'
            }`}
          >
            <Users className="w-3.5 h-3.5" />
            <span>Team & Responsibilities (4 Members)</span>
          </button>
        </div>

        {/* Tab 1: Syllabus Matrix */}
        {activeTab === 'syllabus' && (
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Unit Selector Tabs */}
            <div className="px-6 py-2 bg-slate-50 border-b border-slate-200/70 flex items-center space-x-1 overflow-x-auto">
              {conceptsData?.units.map((unit) => (
                <button
                  key={unit.id}
                  onClick={() => setSelectedUnitId(unit.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors flex items-center space-x-1.5 ${
                    selectedUnitId === unit.id
                      ? 'bg-white text-slate-900 font-bold shadow-xs border border-slate-200'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                  }`}
                >
                  <span>Unit {unit.id}</span>
                  {unit.id === 1 ? (
                    <span className="w-2 h-2 rounded-full bg-emerald-500" title="Phase 1 Implemented" />
                  ) : (
                    <span className="w-2 h-2 rounded-full bg-slate-300" title="Planned" />
                  )}
                </button>
              ))}
            </div>

            {/* Current Unit Details Table */}
            <div className="flex-1 overflow-y-auto p-6 bg-white">
              {loading ? (
                <div className="flex flex-col items-center justify-center p-12 text-slate-400">
                  <Loader2 className="w-6 h-6 animate-spin mb-2 text-brand-600" />
                  <span className="text-xs">Loading syllabus matrix...</span>
                </div>
              ) : currentUnit ? (
                <div>
                  <div className="mb-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded">
                        Unit {currentUnit.id}
                      </span>
                      <h3 className="text-base font-bold text-slate-900">{currentUnit.theme}</h3>
                    </div>
                  </div>

                  <div className="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
                    <table className="w-full text-left text-xs border-collapse">
                      <thead>
                        <tr className="bg-slate-50 border-b border-slate-200 text-slate-600">
                          <th className="py-2.5 px-4 font-semibold">Concept</th>
                          <th className="py-2.5 px-4 font-semibold">Actual Application Use Case</th>
                          <th className="py-2.5 px-3 font-semibold text-center">Phase</th>
                          <th className="py-2.5 px-3 font-semibold text-center">Status</th>
                          <th className="py-2.5 px-4 font-semibold">Source / Test Reference</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {currentUnit.concepts.map((item, idx) => (
                          <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                            <td className="py-3 px-4 font-medium text-slate-900">{item.concept}</td>
                            <td className="py-3 px-4 text-slate-600 max-w-xs">{item.use_case}</td>
                            <td className="py-3 px-3 text-center">
                              <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">
                                P{item.phase}
                              </span>
                            </td>
                            <td className="py-3 px-3 text-center">
                              <span
                                className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                                  item.status === 'Implemented and tested'
                                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                    : 'bg-slate-100 text-slate-600'
                                }`}
                              >
                                {item.status === 'Implemented and tested' && (
                                  <CheckCircle2 className="w-3 h-3 mr-1 text-emerald-600" />
                                )}
                                {item.status}
                              </span>
                            </td>
                            <td className="py-3 px-4 font-mono text-[11px] text-slate-500">
                              {item.source_reference && (
                                <div className="flex items-center space-x-1 text-slate-700 truncate max-w-xs">
                                  <Code2 className="w-3 h-3 text-brand-600 shrink-0" />
                                  <span className="truncate">{item.source_reference}</span>
                                </div>
                              )}
                              {item.test_reference && (
                                <div className="flex items-center space-x-1 text-emerald-700 truncate max-w-xs mt-0.5">
                                  <FileCheck2 className="w-3 h-3 text-emerald-600 shrink-0" />
                                  <span className="truncate">{item.test_reference}</span>
                                </div>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        )}

        {/* Tab 2: Team Responsibilities */}
        {activeTab === 'team' && (
          <div className="flex-1 overflow-y-auto p-6 bg-slate-50/40">
            <div className="max-w-4xl mx-auto space-y-4">
              <div className="p-4 bg-brand-50 border border-brand-200 rounded-2xl">
                <h3 className="text-xs font-bold uppercase tracking-wider text-brand-800 mb-1">
                  University Artificial Intelligence Micro-Project
                </h3>
                <p className="text-xs text-brand-700 leading-relaxed">
                  Learnify AI is developed across four sequential phases by a team of four students.
                  Phase 1 establishes the verified foundations, intelligent agent architecture,
                  database, and the ProofLens transparent reasoning panel.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {teamMembers.map((member, i) => (
                  <div
                    key={i}
                    className={`p-5 rounded-2xl border transition-all ${
                      member.isCurrent
                        ? 'bg-white border-brand-500 shadow-md ring-2 ring-brand-500/10'
                        : 'bg-white border-slate-200/80 shadow-xs'
                    }`}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <div className="flex items-center space-x-2">
                          <h4 className="text-sm font-bold text-slate-900">{member.name}</h4>
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              member.isCurrent
                                ? 'bg-brand-600 text-white'
                                : 'bg-slate-100 text-slate-600'
                            }`}
                          >
                            Phase {member.phase}
                          </span>
                        </div>
                        <span className="text-xs font-mono text-slate-500">{member.regNo}</span>
                      </div>

                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                          member.isCurrent
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : 'bg-slate-100 text-slate-500'
                        }`}
                      >
                        {member.status}
                      </span>
                    </div>

                    <div className="text-xs text-slate-700 font-medium mb-1">{member.role}</div>
                    <p className="text-xs text-slate-500 leading-relaxed">{member.scope}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SyllabusModal;
