import React, { useState } from 'react';
import { Target, Shield, CheckCircle2, AlertCircle, ArrowUpRight, ArrowDownRight, Sliders, Layers, Sparkles } from 'lucide-react';

export const DecisionView: React.FC = () => {
  const [selectedAction, setSelectedAction] = useState('ALL');
  const [testInput, setTestInput] = useState('BTC/USD bullish breakout with 88% confidence and positive sentiment');
  const [testResult, setTestResult] = useState<any>(null);

  const activeDecisions = [
    {
      id: 'DEC-000142',
      pair: 'BTC/USD',
      action: 'BUY',
      bias: 'STRONG_BULLISH',
      confidence: 88.0,
      score: 84.5,
      sentiment: 'positive',
      risk: 'LOW',
      riskScore: 22.0,
      positionSize: 'FULL',
      rewardRisk: 3.2,
      entryCondition: 'Immediate market limit entry on 1h close above $94,200',
      exitCondition: 'ATR trailing SL at $92,400 or Take Profit 2 at $98,500',
      rationale: 'Conditions meet BUY threshold. Positive sentiment, multi-timeframe alignment 5/5, confidence 88%, risk LOW.',
      timestamp: '2026-08-18 08:30:12',
    },
    {
      id: 'DEC-000141',
      pair: 'SOL/USD',
      action: 'BUY',
      bias: 'STRONG_BULLISH',
      confidence: 91.0,
      score: 89.0,
      sentiment: 'positive',
      risk: 'LOW',
      riskScore: 18.5,
      positionSize: 'FULL',
      rewardRisk: 3.5,
      entryCondition: 'Breakout pullback retest at $192.00',
      exitCondition: 'Stop Loss at $184.00 or TP3 at $218.00',
      rationale: 'Strong momentum breakout with volume expansion 2.4x. Risk LOW, reward/risk 3.5:1.',
      timestamp: '2026-08-18 08:28:44',
    },
    {
      id: 'DEC-000140',
      pair: 'ETH/USD',
      action: 'BUY',
      bias: 'BULLISH',
      confidence: 83.0,
      score: 79.5,
      sentiment: 'positive',
      risk: 'MEDIUM',
      riskScore: 32.0,
      positionSize: 'NORMAL',
      rewardRisk: 2.4,
      entryCondition: 'Support bounce confirmation at $3,100',
      exitCondition: 'Trailing Stop at $3,040 or TP2 at $3,280',
      rationale: 'Accumulation pattern verified by knowledge graph. Risk MEDIUM, reward/risk 2.4:1.',
      timestamp: '2026-08-18 08:25:01',
    },
    {
      id: 'DEC-000139',
      pair: 'ADA/USD',
      action: 'HOLD',
      bias: 'NEUTRAL_BEARISH',
      confidence: 58.0,
      score: 46.0,
      sentiment: 'negative',
      risk: 'HIGH',
      riskScore: 68.0,
      positionSize: 'NO_POSITION',
      rewardRisk: 1.2,
      entryCondition: 'Wait for directional breakout confirmation',
      exitCondition: 'No position active',
      rationale: 'Conditions do not meet BUY threshold. High uncertainty and bearish flag pattern.',
      timestamp: '2026-08-18 08:20:19',
    },
  ];

  const handleRunDecisionTest = () => {
    setTestResult({
      id: `DEC-${Math.floor(100000 + Math.random() * 900000)}`,
      action: 'BUY',
      bias: 'STRONG_BULLISH',
      confidence: 86.5,
      score: 82.0,
      sentiment: 'positive',
      risk: 'LOW',
      risk_score: 24.5,
      position_size: 'FULL (Optimal Kelly Allocation)',
      reward_risk_ratio: '3.1 : 1',
      entry_rule: 'LONG on 15m breakout retest with volume > 1.5x MA',
      exit_rule: 'Invalidation trigger at 1.5x ATR trailing stop ($92,850)',
      conflicts_detected: 0,
      evidence_points: 6,
      rationale: 'All parameters verified: Sentiment=Positive, Confidence=86.5%, Risk=LOW, Strategy=Breakout Follow-through.',
      timestamp: new Date().toISOString(),
    });
  };

  const filteredDecisions = activeDecisions.filter((d) => {
    if (selectedAction !== 'ALL' && d.action !== selectedAction) return false;
    return true;
  });

  return (
    <div id="decision-view" className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Target className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Decision Support & Strategy Engine v2.0
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Multi-Factor Risk Assessment, Position Sizing, Dynamic Entry/Exit Conditions & Execution Rationale
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-white font-bold">DECISION ENGINE ONLINE</span>
        </div>
      </div>

      {/* Decision Summary Counters */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Total Decisions Made</span>
          <span className="text-xl font-bold font-mono text-white mt-1 block">142 Executed</span>
          <span className="text-[10px] text-emerald-400 mt-1 block font-mono">100% Rule Compliance</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">BUY Decisions</span>
          <span className="text-xl font-bold font-mono text-emerald-400 mt-1 block">98 Orders (69%)</span>
          <span className="text-[10px] text-[#5F6B78] mt-1 block font-mono">Threshold &gt; 70 Score</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">HOLD / Filtered Out</span>
          <span className="text-xl font-bold font-mono text-amber-400 mt-1 block">34 Cases (24%)</span>
          <span className="text-[10px] text-[#5F6B78] mt-1 block font-mono">Risk Protection Active</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Avg Reward/Risk Ratio</span>
          <span className="text-xl font-bold font-mono text-cyan-400 mt-1 block">2.9 : 1</span>
          <span className="text-[10px] text-cyan-400/80 mt-1 block font-mono">Min Requirement: 1.5 : 1</span>
        </div>
      </div>

      {/* Decision Engine Sandbox Tester */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            Decision Engine & Strategy Generator Sandbox
          </h3>
          <span className="text-xs text-[#5F6B78] font-mono">Core Module: decision_engine.py & strategy.py</span>
        </div>

        <div className="space-y-3">
          <label className="text-xs text-white font-bold block">Input Multi-Module Intelligence Payload</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={testInput}
              onChange={(e) => setTestInput(e.target.value)}
              placeholder="Enter analysis context, sentiment, and signals..."
              className="flex-1 px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-emerald-500"
            />
            <button
              onClick={handleRunDecisionTest}
              className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-600/30 flex items-center gap-2 cursor-pointer"
            >
              <Target className="w-3.5 h-3.5" />
              <span>Generate Decision</span>
            </button>
          </div>

          {testResult && (
            <div className="p-4 rounded-xl bg-[#0B0F14] border border-emerald-500/30 space-y-3 font-mono text-xs">
              <div className="flex items-center justify-between">
                <span className="text-emerald-400 font-bold">DECISION ENGINE VERDICT: {testResult.id}</span>
                <span className="text-[10px] text-[#5F6B78]">{testResult.timestamp}</span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <div className="p-2.5 rounded-lg bg-[#131A22] border border-[#26313D]">
                  <div className="text-[10px] text-[#8D9AAA]">Action</div>
                  <div className="text-emerald-400 font-bold text-base mt-0.5">{testResult.action}</div>
                </div>
                <div className="p-2.5 rounded-lg bg-[#131A22] border border-[#26313D]">
                  <div className="text-[10px] text-[#8D9AAA]">Confidence Score</div>
                  <div className="text-white font-bold text-base mt-0.5">{testResult.confidence}%</div>
                </div>
                <div className="p-2.5 rounded-lg bg-[#131A22] border border-[#26313D]">
                  <div className="text-[10px] text-[#8D9AAA]">Risk Level</div>
                  <div className="text-emerald-400 font-bold text-base mt-0.5">{testResult.risk}</div>
                </div>
                <div className="p-2.5 rounded-lg bg-[#131A22] border border-[#26313D]">
                  <div className="text-[10px] text-[#8D9AAA]">Reward / Risk</div>
                  <div className="text-cyan-400 font-bold text-base mt-0.5">{testResult.reward_risk_ratio}</div>
                </div>
              </div>

              <div className="p-3 bg-[#131A22] rounded-lg border border-[#26313D]/60 space-y-1.5 font-mono text-xs">
                <div className="text-[#8D9AAA]">
                  Strategy Entry: <span className="text-white">{testResult.entry_rule}</span>
                </div>
                <div className="text-[#8D9AAA]">
                  Strategy Exit: <span className="text-white">{testResult.exit_rule}</span>
                </div>
                <div className="text-[#8D9AAA]">
                  Position Sizing: <span className="text-emerald-400 font-bold">{testResult.position_size}</span>
                </div>
              </div>

              <div className="text-[11px] text-[#8D9AAA] font-sans bg-[#131A22] p-2.5 rounded-lg border border-[#26313D]/40">
                Rationale: {testResult.rationale}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Decision Cards List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between pb-2">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Shield className="w-4 h-4 text-emerald-400" />
            Active Strategy Decisions ({filteredDecisions.length})
          </h3>

          <div className="flex gap-2">
            {['ALL', 'BUY', 'HOLD', 'SELL'].map((action) => (
              <button
                key={action}
                onClick={() => setSelectedAction(action)}
                className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-all cursor-pointer ${
                  selectedAction === action
                    ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                    : 'bg-[#131A22] text-[#8D9AAA] hover:text-white border border-[#26313D]'
                }`}
              >
                {action}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredDecisions.map((decision) => (
            <div
              key={decision.id}
              className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-3.5 shadow-lg hover:border-emerald-500/40 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <span className="font-mono font-bold text-base text-white">{decision.pair}</span>
                  <span className="text-xs font-mono text-[#5F6B78]">{decision.id}</span>
                </div>
                <div className="flex items-center gap-2 font-mono text-xs">
                  <span
                    className={`font-bold px-2.5 py-0.5 rounded border ${
                      decision.action === 'BUY'
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                    }`}
                  >
                    ACTION: {decision.action}
                  </span>
                  <span className="bg-[#1A2530] text-cyan-400 font-bold px-2 py-0.5 rounded border border-[#26313D]">
                    R:R {decision.rewardRisk}:1
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2 font-mono text-xs">
                <div className="p-2 bg-[#1A2530] rounded-lg">
                  <span className="text-[10px] text-[#5F6B78] block">Confidence</span>
                  <span className="font-bold text-white">{decision.confidence}%</span>
                </div>
                <div className="p-2 bg-[#1A2530] rounded-lg">
                  <span className="text-[10px] text-[#5F6B78] block">Risk Rating</span>
                  <span className="font-bold text-emerald-400">{decision.risk} ({decision.riskScore}%)</span>
                </div>
                <div className="p-2 bg-[#1A2530] rounded-lg">
                  <span className="text-[10px] text-[#5F6B78] block">Position Sizing</span>
                  <span className="font-bold text-purple-400">{decision.positionSize}</span>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#0B0F14] border border-[#26313D]/60 space-y-1.5 font-mono text-[11px]">
                <div className="text-[#8D9AAA]">
                  Entry: <span className="text-white">{decision.entryCondition}</span>
                </div>
                <div className="text-[#8D9AAA]">
                  Exit: <span className="text-white">{decision.exitCondition}</span>
                </div>
              </div>

              <p className="text-xs text-[#8D9AAA] font-sans leading-relaxed pt-1 border-t border-[#26313D]/60">
                {decision.rationale}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
