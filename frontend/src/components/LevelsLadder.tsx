// src/components/LevelsLadder.tsx
// Price ladder — support/resistance visual

import React from 'react';
import { ArrowUp, ArrowDown, Target } from 'lucide-react';

interface LevelsLadderProps {
  current?: number;
  support?: number;
  resistance?: number;
  entry?: number;
  stop?: number;
  target?: number;
}

export const LevelsLadder: React.FC<LevelsLadderProps> = ({
  current, support, resistance, entry, stop, target,
}) => {
  if (!current || !support || !resistance) {
    return (
      <div className="glass-card rounded-2xl p-5">
        <div className="text-sm font-bold text-white uppercase tracking-wider mb-3">Price Levels</div>
        <div className="py-6 text-center text-[#8D9AAA] text-xs">Data tidak tersedia</div>
      </div>
    );
  }

  const range = resistance - support;
  const positionPct = ((current - support) / range) * 100;

  const resistancePct = 0;
  const supportPct = 100;

  // Level marker
  const markerTop = Math.max(0, Math.min(100, (1 - positionPct / 100) * 100));

  // Determine zone
  const zone =
    positionPct > 80 ? { label: 'DEKAT RESISTANCE', color: 'text-rose-300', hint: 'Potensi koreksi' } :
    positionPct < 20 ? { label: 'DEKAT SUPPORT', color: 'text-emerald-300', hint: 'Potensi bounce' } :
    { label: 'ZONA NETRAL', color: 'text-amber-300', hint: 'Tidak ada sinyal jelas' };

  const distToSupport = ((current - support) / current) * 100;
  const distToResistance = ((resistance - current) / current) * 100;

  return (
    <div className="glass-card rounded-2xl p-5 animate-fade-in">
      {/* HEADER */}
      <div className="flex items-center justify-between mb-5">
        <div className="text-sm font-bold text-white uppercase tracking-wider">Price Levels</div>
        <span className={`text-[10px] px-2 py-0.5 rounded font-bold border ${
          positionPct > 80 ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' :
          positionPct < 20 ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' :
          'bg-amber-500/20 text-amber-300 border-amber-500/30'
        }`}>
          {zone.label}
        </span>
      </div>

      {/* LADDER */}
      <div className="relative flex gap-4">
        {/* Scale */}
        <div className="relative flex-1" style={{ height: '220px' }}>
          {/* Grid lines */}
          <div className="absolute inset-0 flex flex-col justify-between">
            <div className="border-t border-dashed border-white/5" />
            <div className="border-t border-dashed border-white/5" />
            <div className="border-t border-dashed border-white/5" />
            <div className="border-t border-dashed border-white/5" />
          </div>

          {/* Resistance level — top */}
          <div className="absolute left-0 right-0 flex items-center gap-2" style={{ top: '0%' }}>
            <div className="flex-1 h-0.5 bg-gradient-to-r from-rose-500 to-transparent" />
            <div className="px-2 py-1 rounded bg-rose-500/20 border border-rose-500/40 text-rose-300 text-[10px] font-bold font-mono">
              <ArrowUp className="w-3 h-3 inline mr-1" />
              R ${resistance.toFixed(2)}
            </div>
          </div>

          {/* Current price marker */}
          <div
            className="absolute left-0 right-0 flex items-center gap-2 transition-all duration-1000"
            style={{ top: `${markerTop}%` }}
          >
            <div className="w-2 h-2 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/50 animate-pulse" />
            <div className="flex-1 h-0.5 bg-cyan-400/50" />
            <div className="px-2 py-1 rounded bg-cyan-500/30 border border-cyan-400/50 text-cyan-100 text-[10px] font-bold font-mono shadow-lg shadow-cyan-500/20">
              <Target className="w-3 h-3 inline mr-1" />
              NOW ${current.toFixed(2)}
            </div>
          </div>

          {/* Support level — bottom */}
          <div className="absolute left-0 right-0 flex items-center gap-2" style={{ bottom: '0%' }}>
            <div className="flex-1 h-0.5 bg-gradient-to-r from-emerald-500 to-transparent" />
            <div className="px-2 py-1 rounded bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-[10px] font-bold font-mono">
              <ArrowDown className="w-3 h-3 inline mr-1" />
              S ${support.toFixed(2)}
            </div>
          </div>
        </div>
      </div>

      {/* DISTANCES */}
      <div className="grid grid-cols-2 gap-2 mt-4">
        <div className="p-2.5 rounded-lg bg-black/30 border border-white/5">
          <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Ke Support</div>
          <div className="text-sm font-bold text-emerald-300 font-mono">
            {distToSupport > 0 ? '-' : '+'}{Math.abs(distToSupport).toFixed(2)}%
          </div>
        </div>
        <div className="p-2.5 rounded-lg bg-black/30 border border-white/5">
          <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Ke Resistance</div>
          <div className="text-sm font-bold text-rose-300 font-mono">
            +{distToResistance.toFixed(2)}%
          </div>
        </div>
      </div>

      {/* ZONE HINT */}
      <div className={`mt-3 p-2.5 rounded-lg bg-black/30 border border-white/5 text-center`}>
        <div className={`text-xs font-bold ${zone.color}`}>{zone.hint}</div>
      </div>

      {/* ENTRY/STOP/TARGET — kalau ada */}
      {(entry || stop || target) && (
        <div className="grid grid-cols-3 gap-2 mt-3 pt-3 border-t border-white/10">
          {entry && (
            <div className="p-2 rounded bg-blue-500/10 border border-blue-500/30 text-center">
              <div className="text-[9px] uppercase text-blue-300 tracking-wider font-bold">Entry</div>
              <div className="text-xs font-bold text-blue-200 font-mono">${entry}</div>
            </div>
          )}
          {stop && (
            <div className="p-2 rounded bg-rose-500/10 border border-rose-500/30 text-center">
              <div className="text-[9px] uppercase text-rose-300 tracking-wider font-bold">Stop</div>
              <div className="text-xs font-bold text-rose-200 font-mono">${stop}</div>
            </div>
          )}
          {target && (
            <div className="p-2 rounded bg-emerald-500/10 border border-emerald-500/30 text-center">
              <div className="text-[9px] uppercase text-emerald-300 tracking-wider font-bold">Target</div>
              <div className="text-xs font-bold text-emerald-200 font-mono">${target}</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LevelsLadder;
