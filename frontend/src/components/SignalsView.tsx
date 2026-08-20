import React, { useState } from 'react';
import { Radio, ShieldAlert, CheckCircle2, AlertCircle, ArrowUpRight, ArrowDownRight, Filter, ChevronRight } from 'lucide-react';
import { TradingSignal } from '../types';

interface SignalsViewProps {
  signals: TradingSignal[];
}

export const SignalsView: React.FC<SignalsViewProps> = ({ signals }) => {
  const [filter, setFilter] = useState<'ALL' | 'BUY' | 'SELL' | 'HOLD'>('ALL');
  const [selectedSignal, setSelectedSignal] = useState<TradingSignal>(signals[0]);

  const filtered = signals.filter((s) => {
    if (filter === 'BUY') return s.signal.includes('BUY');
    if (filter === 'SELL') return s.signal.includes('SELL');
    if (filter === 'HOLD') return s.signal === 'HOLD' || s.signal === 'MONITOR';
    return true;
  });

  return (
    <div id="signals-view" className="space-y-6 pb-12">
      {/* Header & Filter Controls */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div>
          <h2 className="text-lg font-bold text-white tracking-wide flex items-center gap-2">
            <Radio className="w-5 h-5 text-amber-400" />
            Signal Engine v4.0 (Multi-Timeframe Radar)
          </h2>
          <p className="text-xs text-[#8D9AAA]">
            Algorithmic signal generator with ATR dynamic stop-loss & 3-stage Take Profit targets.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 bg-[#0B0F14] p-1 rounded-xl border border-[#26313D]">
          {(['ALL', 'BUY', 'SELL', 'HOLD'] as const).map((mode) => (
            <button
              key={mode}
              onClick={() => setFilter(mode)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold font-mono transition-colors cursor-pointer ${
                filter === mode
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                  : 'text-[#8D9AAA] hover:text-white'
              }`}
            >
              {mode}
            </button>
          ))}
        </div>
      </div>

      {/* Spotlight Selected Signal Card */}
      {selectedSignal && (
        <div className="p-6 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#1A2530] to-[#131A22] border border-[#26313D] space-y-5 shadow-xl">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#26313D]">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center font-black text-white text-base">
                {selectedSignal.pair.split('/')[0]}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xl font-black text-white font-mono">{selectedSignal.pair}</span>
                  <span
                    className={`text-xs font-black px-2.5 py-0.5 rounded border ${
                      selectedSignal.signal.includes('BUY')
                        ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                        : selectedSignal.signal.includes('SELL')
                        ? 'bg-rose-500/20 text-rose-400 border-rose-500/30'
                        : 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                    }`}
                  >
                    {selectedSignal.signal.replace('_', ' ')}
                  </span>
                </div>
                <div className="text-xs text-[#8D9AAA] mt-0.5 font-mono">
                  Current Price: <strong className="text-white">${selectedSignal.price.toLocaleString()}</strong> · Confidence: <strong className="text-blue-400">{selectedSignal.confidence}%</strong>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
                <span className="text-[10px] text-[#5F6B78] font-bold block">Signal Quality</span>
                <span className="text-xs font-bold text-emerald-400">{selectedSignal.quality}</span>
              </div>
              <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
                <span className="text-[10px] text-[#5F6B78] font-bold block">Risk / Reward</span>
                <span className="text-xs font-bold text-blue-400">1:{selectedSignal.riskReward}</span>
              </div>
            </div>
          </div>

          {/* Trade Execution Targets Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono">
            <div className="p-3.5 rounded-xl bg-[#0B0F14] border border-[#26313D]">
              <span className="text-[10px] text-[#8D9AAA] font-bold uppercase block">Entry Price</span>
              <div className="text-base font-bold text-white mt-1">${selectedSignal.entry.toLocaleString()}</div>
              <span className="text-[10px] text-[#5F6B78]">Limit / Market</span>
            </div>
            <div className="p-3.5 rounded-xl bg-[#0B0F14] border border-rose-500/20">
              <span className="text-[10px] text-rose-400 font-bold uppercase block">Stop Loss (1.5x ATR)</span>
              <div className="text-base font-bold text-rose-300 mt-1">${selectedSignal.stopLoss.toLocaleString()}</div>
              <span className="text-[10px] text-rose-400/70">Hard Invalidation</span>
            </div>
            <div className="p-3.5 rounded-xl bg-[#0B0F14] border border-emerald-500/20">
              <span className="text-[10px] text-emerald-400 font-bold uppercase block">TP 1 (1.5x RR)</span>
              <div className="text-base font-bold text-emerald-300 mt-1">${selectedSignal.tp1.toLocaleString()}</div>
              <span className="text-[10px] text-emerald-400/70">Take 30% Off</span>
            </div>
            <div className="p-3.5 rounded-xl bg-[#0B0F14] border border-emerald-500/30">
              <span className="text-[10px] text-emerald-400 font-bold uppercase block">TP 2 (2.5x RR)</span>
              <div className="text-base font-bold text-emerald-400 mt-1">${selectedSignal.tp2.toLocaleString()}</div>
              <span className="text-[10px] text-emerald-400/70">Core Target (50%)</span>
            </div>
          </div>

          {/* MTF Timeframe Alignment Grid */}
          <div>
            <span className="text-xs font-bold text-[#8D9AAA] uppercase tracking-wider block mb-2 font-mono">
              Multi-Timeframe (MTF) Alignment Matrix
            </span>
            <div className="grid grid-cols-5 gap-2 font-mono text-center text-xs">
              {Object.entries(selectedSignal.mtfAlignment).map(([tf, status]) => {
                const isBull = status === 'BULLISH';
                const isBear = status === 'BEARISH';
                return (
                  <div
                    key={tf}
                    className={`p-2.5 rounded-xl border ${
                      isBull
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                        : isBear
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                        : 'bg-[#0B0F14] text-[#8D9AAA] border-[#26313D]'
                    }`}
                  >
                    <span className="text-[10px] text-[#5F6B78] block font-bold">{tf.toUpperCase()}</span>
                    <span className="font-extrabold mt-0.5 block">{status}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Analysis & Reasons */}
          <div className="space-y-2 pt-2 border-t border-[#26313D]/70">
            <span className="text-xs font-bold text-[#8D9AAA] uppercase tracking-wider block font-mono">
              Algorithmic Evidence & Confirmation Checklist
            </span>
            <div className="space-y-1.5 text-xs text-[#E8EDF2]">
              {selectedSignal.reasons.map((r, i) => (
                <div key={i} className="flex items-start gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{r}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Signals List Table */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
        <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 mb-3">
          All Generated Signals ({filtered.length})
        </h3>

        <div className="space-y-2.5">
          {filtered.map((sig) => {
            const isBuy = sig.signal.includes('BUY');
            const isSell = sig.signal.includes('SELL');
            const isSelected = selectedSignal?.id === sig.id;
            return (
              <div
                key={sig.id}
                onClick={() => setSelectedSignal(sig)}
                className={`p-4 rounded-xl border transition-all cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-3 ${
                  isSelected
                    ? 'bg-[#1A2530] border-blue-500/60 shadow-md'
                    : 'bg-[#131A22] hover:bg-[#1A2530]/60 border-[#26313D]'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="font-black text-white font-mono text-sm tracking-wide">{sig.pair}</span>
                  <span
                    className={`text-[10px] font-black px-2 py-0.5 rounded border ${
                      isBuy
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                        : isSell
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                    }`}
                  >
                    {sig.signal.replace('_', ' ')}
                  </span>
                  <span className="text-xs font-mono text-blue-400 font-bold">{sig.confidence}% Conf</span>
                </div>

                <div className="flex items-center gap-4 text-xs font-mono text-[#8D9AAA]">
                  <div>Entry: <strong className="text-white">${sig.entry.toLocaleString()}</strong></div>
                  <div>SL: <strong className="text-rose-400">${sig.stopLoss.toLocaleString()}</strong></div>
                  <div>TP2: <strong className="text-emerald-400">${sig.tp2.toLocaleString()}</strong></div>
                  <ChevronRight className="w-4 h-4 text-[#5F6B78]" />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
