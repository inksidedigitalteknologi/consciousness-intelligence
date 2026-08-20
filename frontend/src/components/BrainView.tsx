import React, { useState } from 'react';
import { Brain, Cpu, Zap, Activity, CheckCircle2, AlertTriangle, Play, RefreshCw, Sparkles, Sliders } from 'lucide-react';

interface BrainViewProps {
  brainState: string;
  cycleCount: number;
  healthScore: number;
  onRefresh: () => void;
}

export const BrainView: React.FC<BrainViewProps> = ({
  brainState,
  cycleCount,
  healthScore,
  onRefresh,
}) => {
  const [activeInstance, setActiveInstance] = useState('default');
  const [isProcessing, setIsProcessing] = useState(false);

  const brainInstances = ['default', 'scalper_brain', 'swing_brain', 'macro_brain'];

  const handleObserveTest = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
    }, 600);
  };

  return (
    <div id="brain-view" className="space-y-6 pb-12">
      {/* Header */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Cognitive Brain Core v4.2.3
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Central Neural Controller & Metacognitive Reasoning Hub
            </p>
          </div>
        </div>

        {/* Brain Selector */}
        <div className="flex items-center gap-3">
          <span className="text-xs font-semibold text-[#8D9AAA]">Active Brain:</span>
          <select
            id="brain-instance-selector"
            value={activeInstance}
            onChange={(e) => setActiveInstance(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-[#1A2530] border border-[#26313D] text-white text-xs font-mono font-bold focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            {brainInstances.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>

          <button
            onClick={handleObserveTest}
            disabled={isProcessing}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-all shadow-md shadow-blue-600/30 cursor-pointer disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-current ${isProcessing ? 'animate-spin' : ''}`} />
            <span>{isProcessing ? 'Thinking...' : 'Trigger Cycle'}</span>
          </button>
        </div>
      </div>

      {/* Primary Metrics Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-3.5">
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">Brain State</div>
          <div className="text-xl font-black text-emerald-400 font-mono mt-1">{brainState}</div>
          <div className="text-[10px] text-[#5F6B78] mt-1">Autonomous Mode</div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">Cycles Processed</div>
          <div className="text-xl font-black text-white font-mono mt-1">#{cycleCount}</div>
          <div className="text-[10px] text-[#5F6B78] mt-1">Zero latency gap</div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">Health Score</div>
          <div className="text-xl font-black text-emerald-400 font-mono mt-1">{healthScore}%</div>
          <div className="text-[10px] text-[#5F6B78] mt-1">Auto-Healing Active</div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">Success Rate</div>
          <div className="text-xl font-black text-blue-400 font-mono mt-1">98.5%</div>
          <div className="text-[10px] text-[#5F6B78] mt-1">Zero fatal crashes</div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] col-span-2 lg:col-span-1">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">Memory Footprint</div>
          <div className="text-xl font-black text-purple-400 font-mono mt-1">12.8 MB</div>
          <div className="text-[10px] text-[#5F6B78] mt-1">2,450 records in DB</div>
        </div>
      </div>

      {/* Decision Support Box & Neural Flow */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Real-time Decision Support */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-400" />
              Real-Time Decision Support
            </h3>
            <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold border border-emerald-500/20">
              HIGH CONFIDENCE
            </span>
          </div>

          <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-[#8D9AAA]">Primary Recommended Action:</span>
              <span className="text-sm font-black px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                STRONG_BUY (BTC/USD & SOL/USD)
              </span>
            </div>

            <div className="space-y-1.5 text-xs text-[#E8EDF2]">
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span>Multi-timeframe consensus confirms bullish order book pressure above $68,000 baseline.</span>
              </div>
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span>RSI oscillator sits in healthy expansion band with minimal bearish divergence on 1h / 4h.</span>
              </div>
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span>ATR-based risk management recommends Stop Loss at 1.5x ATR below entry.</span>
              </div>
            </div>
          </div>

          {/* Reasoning Parameters */}
          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="p-2.5 rounded-lg bg-[#0B0F14] border border-[#26313D]">
              <div className="text-[10px] text-[#5F6B78] font-bold">Trend Bias</div>
              <div className="text-xs font-bold text-emerald-400 mt-0.5">BULLISH (+84)</div>
            </div>
            <div className="p-2.5 rounded-lg bg-[#0B0F14] border border-[#26313D]">
              <div className="text-[10px] text-[#5F6B78] font-bold">Risk Level</div>
              <div className="text-xs font-bold text-blue-400 mt-0.5">MODERATE</div>
            </div>
            <div className="p-2.5 rounded-lg bg-[#0B0F14] border border-[#26313D]">
              <div className="text-[10px] text-[#5F6B78] font-bold">Expected Horizon</div>
              <div className="text-xs font-bold text-purple-400 mt-0.5">4h - 24h</div>
            </div>
          </div>
        </div>

        {/* Neural Pipeline Telemetry */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <Cpu className="w-4 h-4 text-blue-400" />
              Cognitive Pipeline Stages
            </h3>
            <span className="text-xs text-[#5F6B78] font-mono">10 Subsystems</span>
          </div>

          <div className="space-y-2 font-mono text-xs">
            {[
              { stage: '1. Perception Pipeline', status: 'ACTIVE', latency: '2.1ms', note: 'OHLCV & Order Book tick parser' },
              { stage: '2. Short-Term Memory Buffer', status: 'ACTIVE', latency: '0.8ms', note: '50 items in circular RAM ring' },
              { stage: '3. Pattern Recognition Engine', status: 'ACTIVE', latency: '4.5ms', note: '30+ Candlestick & Wave patterns' },
              { stage: '4. Reasoning & Logic Engine', status: 'ACTIVE', latency: '3.2ms', note: 'Contextual market deduction' },
              { stage: '5. Decision Support & Risk', status: 'ACTIVE', latency: '1.9ms', note: 'ATR Stop Loss / Take Profit 1-3' },
              { stage: '6. Consciousness Metacognition', status: 'ACTIVE', latency: '3.8ms', note: 'Reflective feedback & learning loop' },
            ].map((p) => (
              <div
                key={p.stage}
                className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D] flex items-center justify-between"
              >
                <div>
                  <span className="font-bold text-white">{p.stage}</span>
                  <p className="text-[10px] text-[#8D9AAA] font-sans">{p.note}</p>
                </div>
                <div className="text-right">
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {p.status}
                  </span>
                  <div className="text-[10px] text-[#5F6B78] mt-0.5">{p.latency}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
