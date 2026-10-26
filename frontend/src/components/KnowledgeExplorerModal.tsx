import React, { useState, useEffect, useCallback } from 'react';
import {
  Search,
  BookOpen,
  X,
  MessageSquare,
  Loader2
} from 'lucide-react';
import { KnowledgeRecord } from '../types';
import { getKnowledgeList } from '../services/api';

interface KnowledgeExplorerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAskQuestion: (question: string) => void;
}

export const KnowledgeExplorerModal: React.FC<KnowledgeExplorerModalProps> = ({
  isOpen,
  onClose,
  onAskQuestion,
}) => {
  const [records, setRecords] = useState<KnowledgeRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedUnit, setSelectedUnit] = useState<number | undefined>(undefined);
  const [selectedRecord, setSelectedRecord] = useState<KnowledgeRecord | null>(null);

  const loadRecords = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getKnowledgeList(searchTerm || undefined, selectedUnit);
      setRecords(data.records);
      if (data.records.length > 0 && !selectedRecord) {
        setSelectedRecord(data.records[0]);
      }
    } catch (err) {
      console.error('Failed to load knowledge records:', err);
    } finally {
      setLoading(false);
    }
  }, [searchTerm, selectedUnit, selectedRecord]);

  useEffect(() => {
    if (isOpen) {
      loadRecords();
    }
  }, [isOpen, loadRecords]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadRecords();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-900/50 backdrop-blur-xs">
      <div className="bg-white w-full max-w-5xl h-[88vh] rounded-2xl shadow-2xl border border-slate-200/80 flex flex-col overflow-hidden animate-fade-in">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200/80 flex items-center justify-between bg-slate-50/70">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-brand-600 flex items-center justify-center text-white shadow-xs">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">Knowledge Explorer</h2>
              <p className="text-xs text-slate-500">
                Verified curriculum records and syllabus materials (Units I–V)
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

        {/* Search & Filter Bar */}
        <div className="px-6 py-3 border-b border-slate-100 bg-white flex flex-col sm:flex-row gap-3 items-center justify-between">
          <form onSubmit={handleSearchSubmit} className="relative w-full sm:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search knowledge records..."
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200/90 rounded-xl focus:outline-none focus:border-brand-500"
            />
          </form>

          {/* Unit Filter Tabs */}
          <div className="flex items-center space-x-1 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
            <button
              onClick={() => setSelectedUnit(undefined)}
              className={`px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                selectedUnit === undefined
                  ? 'bg-brand-600 text-white font-semibold'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              All Units
            </button>
            {[1, 2, 3, 4, 5].map((u) => (
              <button
                key={u}
                onClick={() => setSelectedUnit(u)}
                className={`px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                  selectedUnit === u
                    ? 'bg-brand-600 text-white font-semibold'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Unit {u}
              </button>
            ))}
          </div>
        </div>

        {/* Body: Split List & Detail */}
        <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
          {/* Left List */}
          <div className="w-full md:w-80 border-r border-slate-200/80 overflow-y-auto p-3 space-y-1.5 bg-slate-50/50">
            {loading ? (
              <div className="flex flex-col items-center justify-center p-8 text-slate-400">
                <Loader2 className="w-6 h-6 animate-spin mb-2 text-brand-600" />
                <span className="text-xs">Loading records...</span>
              </div>
            ) : records.length === 0 ? (
              <div className="text-center p-6 text-xs text-slate-400">
                No matching knowledge records found.
              </div>
            ) : (
              records.map((rec) => {
                const isSelected = selectedRecord?.id === rec.id;
                return (
                  <button
                    key={rec.id}
                    onClick={() => setSelectedRecord(rec)}
                    className={`w-full text-left p-3 rounded-xl border transition-all ${
                      isSelected
                        ? 'bg-white border-brand-500 shadow-xs'
                        : 'bg-white/80 hover:bg-white border-slate-200/70 hover:border-slate-300'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] font-bold text-brand-700 bg-brand-50 px-1.5 py-0.5 rounded">
                        Unit {rec.unit || 'I'}
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono">
                        {rec.id}
                      </span>
                    </div>
                    <h3 className="text-xs font-semibold text-slate-900 line-clamp-1 mb-1">
                      {rec.title}
                    </h3>
                    <p className="text-[11px] text-slate-500 line-clamp-2 leading-relaxed">
                      {rec.content}
                    </p>
                  </button>
                );
              })
            )}
          </div>

          {/* Right Detail Pane */}
          <div className="flex-1 overflow-y-auto p-6 bg-white">
            {selectedRecord ? (
              <div className="max-w-2xl space-y-6">
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-brand-100 text-brand-700">
                      Unit {selectedRecord.unit}: {selectedRecord.topic_name || 'AI Curriculum'}
                    </span>
                    <span className="text-xs font-mono text-slate-400">
                      ID: {selectedRecord.id}
                    </span>
                  </div>
                  <h2 className="text-xl font-bold text-slate-900">
                    {selectedRecord.title}
                  </h2>
                </div>

                {/* Content Box */}
                <div className="p-4 rounded-2xl bg-slate-50/80 border border-slate-200/80 text-sm leading-relaxed text-slate-800">
                  {selectedRecord.content}
                </div>

                {/* Provenance Metadata */}
                <div className="p-4 rounded-xl border border-slate-200/70 bg-white space-y-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                    Provenance & Citations
                  </h4>
                  <div className="text-xs text-slate-600">
                    <strong className="text-slate-800">Source:</strong>{' '}
                    {selectedRecord.source_name || 'Standard Reference'}
                  </div>
                  {selectedRecord.source_desc && (
                    <p className="text-xs text-slate-500">{selectedRecord.source_desc}</p>
                  )}
                  {selectedRecord.keywords && (
                    <div className="pt-2 flex flex-wrap gap-1">
                      {selectedRecord.keywords.split(',').map((kw, i) => (
                        <span
                          key={i}
                          className="px-2 py-0.5 rounded text-[10px] bg-slate-100 text-slate-600"
                        >
                          #{kw.trim()}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Action: Ask in Chat */}
                <div className="pt-2">
                  <button
                    onClick={() => {
                      onAskQuestion(`Tell me about ${selectedRecord.title}`);
                      onClose();
                    }}
                    className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold shadow-sm transition-all"
                  >
                    <MessageSquare className="w-4 h-4" />
                    <span>Ask Chatbot about this Concept</span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-slate-400 text-sm">
                Select a knowledge record from the left list to view details.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeExplorerModal;
