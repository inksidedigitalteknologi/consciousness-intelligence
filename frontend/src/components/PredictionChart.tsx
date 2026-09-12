// src/components/PredictionChart.tsx
// SVG histogram — Monte Carlo outcomes

import React, { useMemo } from 'react';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';

interface Prediction {
  current_price?: number;
  days?: number;
  iterations?: number;
  target_mean?: number;
  target_median?: number;
  p5?: number;
  p95?: number;
  prob_up?: number;
  prob_down?: number;
  expected_return_pct?: number;
  volatility_daily?: number;
  scenarios?: {
    bullish?: number;
    base?: number;
    bearish?: number;
  };
  source?: string;
}

interface PredictionChartProps {
  prediction: Prediction;
}

export const PredictionChart: React.FC<PredictionChartProps> = ({ prediction }) => {
  const p = prediction || {};

  const hasData = p.current_price && p.p5 && p.p95;

  // Generate histogram bars dari range
  const bars = useMemo(() => {
    if (!hasData) return [];

    const min = p.p5!;
    const max = p.p95!;
    const range = max - min;
    const mid = p.current_price!;

    const BAR_COUNT = 24;
    const barWidth = range / BAR_COUNT;

    // Distribusi normal-ish
    const result: { x: number; height: number; isBull: boolean }[] = [];
    const mean = p.target_mean || mid;
    const std = (max - min) / 4; // rough estimate

    for (let i = 0; i < BAR_COUNT; i++) {
      const x = min + (i + 0.5) * barWidth;
      const normalized = Math.exp(-Math.pow((x - mean) / std, 2) / 2);
      const height = normalized * 100;
      result.push({
        x,
        height: Math.max(5, height),
        isBull: x > mid,
      });
    }

    return result;
  }, [p.current_price, p.p5, p.p95, p.target_mean, hasData]);

  if (!hasData) {
    return (
      <div className="glass-card rounded-2xl p-5">
        <div className="flex items-center gap-2 mb-3">
          <Activity className="w-4 h-4 text-cyan-400" />
          <span className="text-sm font-bold text-white uppercase tracking-wider">Prediction</span>
        </div>
        <div className="py-8 text-center text-[#8D9AAA] text-xs">
          {p.source === 'error' ? '❌ Prediction error' : 'Memuat prediksi...'}
        </div>
      </div>
    );
  }

  const probUp = p.prob_up || 0;
  const probDown = p.prob_down || 0;
  const expReturn = p.expected_return_pct || 0;
  const isPositive = expReturn > 0;

  // Chart dimensions
  const W = 320;
  const H = 100;
  const minX = p.p5!;
  const maxX = p.p95!;
  const range = maxX - minX;
  const currentX = ((p.current_price! - minX) / range) * W;
  const targetX = ((p.target_mean! - minX) / range) * W;

  return (
    <div className="glass-card rounded-2xl p-5 animate-fade-in">
      {/* HEADER */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-cyan-400" />
          <span className="text-sm font-bold text-white uppercase tracking-wider">
            Prediction {p.days}D
          </span>
        </div>
        <span className={`text-[10px] px-2 py-0.5 rounded font-bold border ${
          isPositive
            ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
            : 'bg-rose-500/20 text-rose-300 border-rose-500/30'
        }`}>
          {isPositive ? <TrendingUp className="w-3 h-3 inline mr-1" /> : <TrendingDown className="w-3 h-3 inline mr-1" />}
          {isPositive ? '+' : ''}{expReturn.toFixed(2)}%
        </span>
      </div>

      {/* TARGET */}
      <div className="mb-4">
        <div className="text-[10px] uppercase text-[#8D9AAA] tracking-wider font-bold mb-1">Target {p.days} hari</div>
        <div className="flex items-end gap-3">
          <span className="text-2xl font-black text-white font-mono">${p.target_mean?.toFixed(2)}</span>
          <span className="text-xs text-[#5F6B78] font-mono mb-1">
            dari ${p.current_price?.toFixed(2)}
          </span>
        </div>
      </div>

      {/* HISTOGRAM */}
      <div className="relative mb-4">
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full" style={{ height: '100px' }}>
          {/* Grid lines */}
          <line x1="0" y1={H * 0.5} x2={W} y2={H * 0.5} stroke="rgba(255,255,255,0.03)" strokeWidth="1" />
          <line x1="0" y1={H * 0.75} x2={W} y2={H * 0.75} stroke="rgba(255,255,255,0.03)" strokeWidth="1" />

          {/* Bars */}
          {bars.map((bar, i) => {
            const barX = ((bar.x - minX) / range) * W - 5;
            const barH = (bar.height / 100) * (H * 0.85);
            const barY = H - barH;
            return (
              <rect
                key={i}
                x={barX}
                y={barY}
                width={8}
                height={barH}
                rx={2}
                fill={bar.isBull ? 'rgba(16, 185, 129, 0.5)' : 'rgba(239, 68, 68, 0.5)'}
                stroke={bar.isBull ? 'rgba(16, 185, 129, 0.8)' : 'rgba(239, 68, 68, 0.8)'}
                strokeWidth="0.5"
              />
            );
          })}

          {/* Current price line */}
          <line
            x1={currentX} y1={0} x2={currentX} y2={H}
            stroke="white" strokeWidth="1.5" strokeDasharray="3 3"
            opacity="0.7"
          />
          <text
            x={currentX} y={10}
            fill="white" fontSize="8" textAnchor="middle"
            fontFamily="monospace"
          >
            NOW
          </text>

          {/* Target line */}
          <line
            x1={targetX} y1={0} x2={targetX} y2={H}
            stroke="#22D3EE" strokeWidth="1" strokeDasharray="2 2"
            opacity="0.6"
          />
        </svg>
      </div>

      {/* STATS ROW */}
      <div className="grid grid-cols-2 gap-2 mb-3">
        <div className="p-2 rounded-lg bg-black/30 border border-white/5">
          <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Prob Up</div>
          <div className="text-sm font-bold text-emerald-300 font-mono">{probUp.toFixed(1)}%</div>
        </div>
        <div className="p-2 rounded-lg bg-black/30 border border-white/5">
          <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Prob Down</div>
          <div className="text-sm font-bold text-rose-300 font-mono">{probDown.toFixed(1)}%</div>
        </div>
      </div>

      {/* PROB BAR */}
      <div className="flex h-1.5 rounded-full overflow-hidden bg-black/40 mb-4">
        <div className="h-full bg-gradient-to-r from-emerald-500 to-emerald-400" style={{ width: `${probUp}%` }} />
        <div className="h-full bg-gradient-to-r from-rose-400 to-rose-500" style={{ width: `${probDown}%` }} />
      </div>

      {/* SCENARIOS */}
      {p.scenarios && (
        <div className="space-y-1.5 pt-3 border-t border-white/10">
          <div className="text-[10px] uppercase text-[#8D9AAA] tracking-wider font-bold mb-2">Skenario</div>
          {[
            { label: 'Bullish', value: p.scenarios.bullish, icon: '🐂', color: 'text-emerald-300' },
            { label: 'Base', value: p.scenarios.base, icon: '➡', color: 'text-cyan-300' },
            { label: 'Bearish', value: p.scenarios.bearish, icon: '🐻', color: 'text-rose-300' },
          ].map((s, i) => (
            <div key={i} className="flex items-center justify-between text-[11px] py-1 px-2 rounded bg-black/20">
              <span className="text-[#8D9AAA]">{s.icon} {s.label}</span>
              <span className={`font-mono font-bold ${s.color}`}>${s.value?.toFixed(2) || '—'}</span>
            </div>
          ))}
        </div>
      )}

      {/* FOOTER */}
      <div className="mt-3 pt-3 border-t border-white/10 flex items-center justify-between text-[9px] text-[#5F6B78]">
        <span>{p.iterations?.toLocaleString()} iterasi</span>
        <span className="font-mono">Vol {p.volatility_daily?.toFixed(2)}%/hari</span>
      </div>
    </div>
  );
};

export default PredictionChart;
