import React, { useState } from 'react';
import { Radio, ChevronRight } from 'lucide-react';

interface Signal {
  pair?: string;
  signal?: string;
  confidence?: number;
  price?: number;
  strength?: string;
  timestamp?: string;
  [key: string]: any;
}

interface SignalsViewProps {
  signals: Signal[];
}

export const SignalsView: React.FC<SignalsViewProps> = ({ signals = [] }) => {
  const [filter, setFilter] = useState<'ALL' | 'BUY' | 'SELL' | 'HOLD'>('ALL');

  const safeSignals = Array.isArray(signals) ? signals : [];

  const filtered = safeSignals.filter((s) => {
    const sig = (s?.signal || '').toUpperCase();
    if (filter === 'BUY') return sig === 'BUY';
    if (filter === 'SELL') return sig === 'SELL';
    if (filter === 'HOLD') return sig === 'HOLD' || sig === 'MONITOR';
    return true;
  });

  const getSignalColor = (signal: string) => {
    const s = (signal || '').toUpperCase();
    if (s === 'BUY') return 'text-green-400 bg-green-500/20 border-green-500/30';
    if (s === 'SELL') return 'text-red-400 bg-red-500/20 border-red-500/30';
    if (s === 'MONITOR') return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30';
    return 'text-gray-400 bg-gray-500/20 border-gray-500/30';
  };

  const getStrengthColor = (strength?: string) => {
    const s = (strength || '').toUpperCase();
    if (s === 'STRONG') return 'text-green-400';
    if (s === 'WEAK') return 'text-yellow-400';
    return 'text-gray-400';
  };

  const getSignalIcon = (signal: string) => {
    const s = (signal || '').toUpperCase();
    if (s === 'BUY') return '📈';
    if (s === 'SELL') return '📉';
    if (s === 'MONITOR') return '👀';
    return '⏸️';
  };

  const safePrice = (price: any) => {
    const num = Number(price);
    return isNaN(num) ? 0 : num;
  };

  if (!safeSignals || safeSignals.length === 0) {
    return (
      <div className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <Radio className="w-5 h-5 text-amber-400" />
          <h2 className="text-lg font-bold text-white">Signal Engine</h2>
        </div>
        <div className="text-center text-gray-400 py-12 bg-gray-900/50 rounded-xl">
          <p className="text-lg">No signals available</p>
          <p className="text-sm mt-1">Waiting for signals from the engine...</p>
        </div>
      </div>
    );
  }

  return (
    <div id="signals-view" className="space-y-6 pb-12 p-6">
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Radio className="w-5 h-5 text-amber-400" />
            Signal Engine v4.0
          </h2>
          <p className="text-xs text-[#8D9AAA]">
            {safeSignals.length} signals • Real-time from cognitive engine
          </p>
        </div>
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

      {filtered.length === 0 ? (
        <div className="text-center text-gray-400 py-8 bg-gray-800/30 rounded-xl">
          <p>No signals match the current filter</p>
        </div>
      ) : (
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 mb-3">
            All Signals ({filtered.length})
          </h3>
          <div className="space-y-2">
            {filtered.map((sig, index) => (
              <div
                key={index}
                className="p-4 rounded-xl border border-[#26313D] bg-[#131A22] hover:bg-[#1A2530]/60 transition flex flex-col md:flex-row md:items-center justify-between gap-3"
              >
                <div className="flex items-center gap-3">
                  <span className="text-lg">{getSignalIcon(sig.signal)}</span>
                  <span className="font-black text-white font-mono text-sm tracking-wide">
                    {sig.pair || 'UNKNOWN'}
                  </span>
                  <span className={`text-[10px] font-black px-2 py-0.5 rounded border ${getSignalColor(sig.signal)}`}>
                    {sig.signal || 'HOLD'}
                  </span>
                  <span className="text-xs font-mono text-blue-400 font-bold">{sig.confidence || 0}%</span>
                </div>
                <div className="flex items-center gap-4 text-xs font-mono text-[#8D9AAA]">
                  <div>Price: <strong className="text-white">${safePrice(sig.price).toFixed(2)}</strong></div>
                  <div>Strength: <span className={getStrengthColor(sig.strength)}>{sig.strength || 'NEUTRAL'}</span></div>
                  <ChevronRight className="w-4 h-4 text-[#5F6B78]" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="text-xs text-gray-500 text-center">
        {filtered.length} signals • Updated: {new Date().toLocaleTimeString()}
      </div>
    </div>
  );
};

export default SignalsView;
