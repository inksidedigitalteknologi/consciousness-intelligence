// src/components/TimeframeGrid.tsx
// Multi-timeframe heatmap grid

import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface TimeframeData {
  days?: number;
  indicators?: {
    rsi?: number;
    rsi_signal?: string;
    sma_timeframe?: number;
    sma_timeframe_period?: number;
    trend_sma?: string;
    momentum_5d?: number;
    volume_ratio?: number;
  };
  score?: {
    action?: string;
    score?: number;
    confidence?: number;
    reasons?: string[];
  };
  error?: string;
}

interface TimeframeGridProps {
  timeframes: Record<string, TimeframeData>;
  consensus?: {
    action?: string;
    agreement?: number;
    breakdown?: Record<string, number>;
  };
  overall?: {
    action?: string;
    confidence?: number;
    score?: number;
    insights?: string[];
  };
}

export const TimeframeGrid: React.FC<TimeframeGridProps> = ({ timeframes, consensus, overall }) => {
  const tfs = ['1m', '3m', '6m', '1y'];
  const labels: Record<string, string> = { '1m': '1 Bulan', '3m': '3 Bulan', '6m': '6 Bulan', '1y': '1 Tahun' };

  const getActionStyle = (action?: string) => {
    if (action === 'BUY') return {
      bg: 'bg-emerald-500/15',
      border: 'border-emerald-500/40',
      text: 'text-emerald-300',
      glow: 'shadow-emerald-500/10',
      icon: <TrendingUp className="w-3.5 h-3.5" />,
      gradient: 'from-emerald-500 to-emerald-400',
    };
    if (action === 'SELL') return {
      bg: 'bg-rose-500/15',
      border: 'border-rose-500/40',
      text: 'text-rose-300',
      glow: 'shadow-rose-500/10',
      icon: <TrendingDown className="w-3.5 h-3.5" />,
      gradient: 'from-rose-500 to-rose-400',
    };
    return {
      bg: 'bg-amber-500/15',
      border: 'border-amber-500/40',
      text: 'text-amber-300',
      glow: 'shadow-amber-500/10',
      icon: <Minus className="w-3.5 h-3.5" />,
      gradient: 'from-amber-500 to-amber-400',
    };
  };

  const getRsiColor = (rsi?: number) => {
    if (!rsi) return 'text-gray-400';
    if (rsi >= 70) return 'text-rose-300';
    if (rsi <= 30) return 'text-emerald-300';
    return 'text-white';
  };

  const totalTfs = tfs.filter((tf) => timeframes?.[tf] && !timeframes[tf].error).length;

  return (
    <div className="glass-card rounded-2xl p-5 animate-fade-in">
      {/* HEADER */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <div className="text-sm font-bold text-white uppercase tracking-wider">Multi-Timeframe</div>
          <div className="text-[10px] text-[#8D9AAA] mt-0.5">
            {totalTfs} timeframe analisis
          </div>
        </div>
        {overall?.action && (
          <span className={`text-xs px-2.5 py-1 rounded-lg font-bold border ${getActionStyle(overall.action).bg} ${getActionStyle(overall.action).border} ${getActionStyle(overall.action).text}`}>
            {overall.action} · {overall.confidence?.toFixed(0)}%
          </span>
        )}
      </div>

      {/* GRID 2x2 */}
      <div className="grid grid-cols-2 gap-2.5 mb-4">
        {tfs.map((tf) => {
          const t = timeframes?.[tf];
          if (!t) return null;

          if (t.error) {
            return (
              <div key={tf} className="p-3 rounded-xl bg-black/30 border border-white/5">
                <div className="text-[10px] uppercase text-[#8D9AAA] tracking-wider font-bold">{labels[tf]}</div>
                <div className="text-[10px] text-rose-400 mt-2">Error</div>
              </div>
            );
          }

          const style = getActionStyle(t.score?.action);
          const ind = t.indicators || {};
          const sc = t.score || {};
          const smaPeriod = ind.sma_timeframe_period;
          const smaVal = ind.sma_timeframe;

          return (
            <div
              key={tf}
              className={`relative p-3 rounded-xl ${style.bg} border ${style.border} ${style.glow} shadow-lg transition-all duration-300 hover:scale-[1.02]`}
            >
              {/* Header */}
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] uppercase text-white tracking-wider font-bold">{labels[tf]}</span>
                <span className={`text-[10px] font-black px-1.5 py-0.5 rounded border ${style.bg} ${style.border} ${style.text} flex items-center gap-0.5`}>
                  {style.icon}
                  {sc.action}
                </span>
              </div>

              {/* Days */}
              <div className="text-[9px] text-[#5F6B78] font-mono mb-2">
                {t.days} hari
              </div>

              {/* Stats */}
              <div className="space-y-1 text-[10px]">
                {smaVal !== undefined && (
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">SMA{smaPeriod}</span>
                    <span className="font-mono text-white">${smaVal}</span>
                  </div>
                )}
                {ind.rsi !== undefined && (
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">RSI</span>
                    <span className={`font-mono font-bold ${getRsiColor(ind.rsi)}`}>
                      {ind.rsi}
                    </span>
                  </div>
                )}
                {ind.trend_sma && (
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">Trend</span>
                    <span className={`font-bold ${
                      ind.trend_sma === 'BULLISH' ? 'text-emerald-300' :
                      ind.trend_sma === 'BEARISH' ? 'text-rose-300' : 'text-amber-300'
                    }`}>
                      {ind.trend_sma}
                    </span>
                  </div>
                )}
              </div>

              {/* Confidence bar */}
              <div className="mt-2 pt-2 border-t border-white/10">
                <div className="flex justify-between text-[9px] mb-1">
                  <span className="text-[#8D9AAA]">Conf</span>
                  <span className="text-white font-mono">{sc.confidence}%</span>
                </div>
                <div className="w-full h-1 rounded-full bg-black/40 overflow-hidden">
                  <div
                    className={`h-full rounded-full bg-gradient-to-r ${style.gradient} transition-all duration-1000`}
                    style={{ width: `${sc.confidence}%` }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* CONSENSUS */}
      {consensus && consensus.action && (
        <div className="pt-3 border-t border-white/10">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] uppercase text-[#8D9AAA] tracking-wider font-bold">Konsensus</span>
            <span className={`text-xs font-black ${getActionStyle(consensus.action).text}`}>
              {consensus.action} · {consensus.agreement?.toFixed(0)}%
            </span>
          </div>
          <div className="flex h-1.5 rounded-full overflow-hidden bg-black/40">
            {(['BUY', 'HOLD', 'SELL'] as const).map((action) => {
              const count = consensus.breakdown?.[action] || 0;
              const total = totalTfs || 1;
              const pct = (count / total) * 100;
              if (pct === 0) return null;
              const color =
                action === 'BUY' ? 'bg-emerald-500' :
                action === 'SELL' ? 'bg-rose-500' : 'bg-amber-500';
              return (
                <div
                  key={action}
                  className={`h-full ${color} transition-all duration-1000`}
                  style={{ width: `${pct}%` }}
                  title={`${action}: ${count}/${total}`}
                />
              );
            })}
          </div>
          <div className="flex justify-between text-[9px] text-[#5F6B78] mt-1.5">
            {(['BUY', 'HOLD', 'SELL'] as const).map((action) => (
              <span key={action} className="flex items-center gap-1">
                <span className={`w-1.5 h-1.5 rounded-full ${
                  action === 'BUY' ? 'bg-emerald-500' :
                  action === 'SELL' ? 'bg-rose-500' : 'bg-amber-500'
                }`} />
                {action} {consensus.breakdown?.[action] || 0}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* INSIGHTS */}
      {overall?.insights && overall.insights.length > 0 && (
        <div className="mt-3 pt-3 border-t border-white/10 space-y-1">
          {overall.insights.slice(0, 2).map((ins, i) => (
            <div key={i} className="text-[10px] text-[#8D9AAA] leading-snug">
              {ins}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TimeframeGrid;
