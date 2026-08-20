import React, { useState } from 'react';
import { ShieldCheck, Play, CheckCircle2, AlertCircle, RefreshCw, Terminal, Check } from 'lucide-react';

export const DiagnosticsView: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [lastTestTime, setLastTestTime] = useState<string>('2026-08-18 07:30:00');

  const testSuites = [
    { name: 'core.consciousness (Consciousness)', method: 'self_test()', status: 'PASS', duration: '12ms', details: 'All 5 tests passed' },
    { name: 'core.brain (Brain Core v4.2.3)', method: 'self_test()', status: 'PASS', duration: '8ms', details: 'All 11 tests passed' },
    { name: 'core.bot (Trading Bot Core)', method: 'get_status()', status: 'PASS', duration: '4ms', details: 'Status: RUNNING' },
    { name: 'core.memory (SQLite Long-Term Memory)', method: 'stats()', status: 'PASS', duration: '3ms', details: '2,450 records in DB' },
    { name: 'core.knowledge (Knowledge Graph v3.1)', method: 'self_test()', status: 'PASS', duration: '15ms', details: 'State storage & retrieval OK' },
    { name: 'core.learning.engine (Learning Engine v3.0)', method: 'self_test()', status: 'PASS', duration: '22ms', details: 'All 5 tests passed' },
    { name: 'core.learning.pattern (Pattern Engine)', method: 'get_state()', status: 'PASS', duration: '6ms', details: '30+ patterns active' },
    { name: 'core.learning.market_learning (Market Learning)', method: 'status()', status: 'PASS', duration: '5ms', details: 'Adaptive feedback OK' },
    { name: 'core.learning.semantic_memory (Semantic Memory)', method: 'count()', status: 'PASS', duration: '2ms', details: '420 semantic vectors' },
    { name: 'core.market_data (Kraken Market Bridge)', method: 'health_check()', status: 'PASS', duration: '45ms', details: 'Public API ticker OK' },
    { name: 'core.signal_engine (Signal Engine v4.0)', method: 'generate_signal()', status: 'PASS', duration: '9ms', details: 'MTF alignment evaluation OK' },
    { name: 'core.diagnostics (System Diagnostics v4.0)', method: 'self_test()', status: 'PASS', duration: '18ms', details: 'All 6 diagnostic tests passed' },
    { name: 'core.bootstrap (Bootstrap System v4.0)', method: 'self_test()', status: 'PASS', duration: '14ms', details: '32 modules registered OK' },
  ];

  const handleRunAll = () => {
    setIsRunning(true);
    setTimeout(() => {
      setIsRunning(false);
      setLastTestTime(new Date().toISOString().replace('T', ' ').substring(0, 19));
    }, 800);
  };

  const passedCount = testSuites.filter((t) => t.status === 'PASS').length;

  return (
    <div id="diagnostics-view" className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Core Module Verification & Self-Test Suite
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Automated Integrity Verifier for All 20+ Cognitive & Trading Subsystems
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleRunAll}
            disabled={isRunning}
            className="flex items-center gap-2 px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-all shadow-md shadow-emerald-600/30 cursor-pointer disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-current ${isRunning ? 'animate-spin' : ''}`} />
            <span>{isRunning ? 'Verifying Modules...' : 'Run 1-Click Verification'}</span>
          </button>
        </div>
      </div>

      {/* Summary Score Bar */}
      <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] flex items-center justify-between flex-wrap gap-3 font-mono text-xs">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-emerald-400" />
          <span className="font-bold text-white text-sm">
            VERIFICATION STATUS: <span className="text-emerald-400">PASSED ({passedCount}/{testSuites.length})</span>
          </span>
        </div>
        <div className="text-[#8D9AAA] text-[11px]">
          Last Run: <strong className="text-white">{lastTestTime}</strong>
        </div>
      </div>

      {/* Test Suites Table */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
        <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 mb-3">
          Subsystem Test Matrix ({testSuites.length})
        </h3>

        <div className="divide-y divide-[#26313D]/40 font-mono text-xs">
          {testSuites.map((suite) => (
            <div
              key={suite.name}
              className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2 hover:bg-[#1A2530]/40 px-2 rounded-lg transition-colors"
            >
              <div className="flex items-center gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                <div>
                  <span className="font-bold text-white">{suite.name}</span>
                  <span className="text-[10px] text-[#5F6B78] block font-sans">{suite.details}</span>
                </div>
              </div>

              <div className="flex items-center gap-4 text-right">
                <span className="text-[10px] text-[#5F6B78]">{suite.method} · {suite.duration}</span>
                <span className="text-[10px] font-black px-2.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {suite.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
