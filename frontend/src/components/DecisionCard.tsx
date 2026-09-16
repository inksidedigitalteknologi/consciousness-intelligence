// src/components/DecisionCard.tsx
// Glassmorphism decision hero panel

import React from 'react';
import { TrendingUp, TrendingDown, Minus, Target, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface DirectionData {
  direction?: string;
  confidence?: number;
  actionable?: boolean;
  reasoning?: string;
  entry_zone?: number[];
  target?: number;
  stop?: number;
  expected_return?: number;
  risk_reward?: number;
  experience?: {
    similar_decisions?: number;
    win_rate?: number;
    recommendation?: string;
  };
}

interface UnifiedData {
  score?: number;
  action?: string;
  confidence?: number;
  aspek_count?: number;
  breakdown?: Record<string, number>;
  weights?: string;
  threshold?: number;
  fase?: number;
}

interface MarketDecision {
  action?: string;
  confidence?: number;
  score?: number;
  reasons?: string[];
  insights?: string[];
  unified?: UnifiedData;
  direction?: DirectionData;
  levels?: {
    current?: number;
    support?: number;
    resistance?: number;
    entry?: number;
    stop?: number;
    target?: number;
  };
}

interface DecisionCardProps {
  decision: MarketDecision;
  symbol?: string;
}

export const DecisionCard: React.FC<DecisionCardProps> = ({ decision, symbol }) => {
  const action = (decision?.action || 'HOLD').toUpperCase();
  const confidence = decision?.confidence || 0;
  const score = decision?.score || 0;
  const reasons = decision?.reasons || [];
  const levels = decision?.levels || {};
  const unified = decision?.unified;
  const breakdown = unified?.breakdown || {};
  const aspekCount = unified?.aspek_count || 0;
  const direction = decision?.direction;

  // Style per action
  const actionStyle = {
    BUY: {
      card: 'glass-card-green',
      badge: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
      bar: 'from-emerald-500 to-emerald-400',
      glow: 'shadow-emerald-500/20',
      icon: <TrendingUp className="w-6 h-6" />,
      emoji: '🚀',
    },
    SELL: {
      card: 'glass-card-red',
      badge: 'bg-rose-500/20 text-rose-300 border-rose-500/40',
      bar: 'from-rose-500 to-rose-400',
      glow: 'shadow-rose-500/20',
      icon: <TrendingDown className="w-6 h-6" />,
      emoji: '🔻',
    },
    HOLD: {
      card: 'glass-card-amber',
      badge: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
      bar: 'from-amber-500 to-amber-400',
      glow: 'shadow-amber-500/20',
      icon: <Minus className="w-6 h-6" />,
      emoji: '⏸',
    },
  }[action] || {
    card: 'glass-card',
    badge: 'bg-gray-500/20 text-gray-300 border-gray-500/40',
    bar: 'from-gray-500 to-gray-400',
    glow: 'shadow-gray-500/20',
    icon: <Minus className="w-6 h-6" />,
    emoji: '⏸',
  };

  return (
    <div className={`rounded-2xl ${actionStyle.card} p-6 animate-fade-in transition-all duration-500`}>
      {/* HEADER */}
      <div className="flex items-start justify-between mb-5">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center border ${actionStyle.badge} ${actionStyle.glow} shadow-lg`}>
            {actionStyle.icon}
          </div>
          <div>
            <div className="text-[10px] uppercase tracking-widest text-[#8D9AAA] font-bold">
              Market Decision
            </div>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="text-sm font-bold text-white">{symbol || '—'}</span>
              <span className="text-[10px] text-[#5F6B78]">·</span>
              <span className={`text-2xl font-black tracking-wide ${
                action === 'BUY' ? 'text-emerald-300' :
                action === 'SELL' ? 'text-rose-300' :
                'text-amber-300'
              }`}>
                {actionStyle.emoji} {action}
              </span>
            </div>
          </div>
        </div>

        {/* Score */}
        <div className="text-right">
          <div className="text-[10px] uppercase tracking-widest text-[#8D9AAA] font-bold">Score</div>
          <div className={`text-2xl font-black font-mono ${
            score > 0 ? 'text-emerald-300' : score < 0 ? 'text-rose-300' : 'text-white'
          }`}>
            {score > 0 ? '+' : ''}{typeof score === 'number' ? score.toFixed(1) : score}
          </div>
          <div className="text-[10px] text-[#5F6B78]">/ 100</div>
        </div>
      </div>

      {/* CONFIDENCE BAR */}
      <div className="mb-5">
        <div className="flex items-center justify-between text-[10px] mb-2">
          <span className="uppercase tracking-widest text-[#8D9AAA] font-bold">Confidence</span>
          <span className="text-white font-mono font-bold text-sm">{confidence.toFixed(0)}%</span>
        </div>
        <div className="w-full h-2 rounded-full bg-black/40 overflow-hidden border border-white/5">
          <div
            className={`h-full rounded-full bg-gradient-to-r ${actionStyle.bar} transition-all duration-1000 ease-out`}
            style={{
              width: `${confidence}%`,
              boxShadow: '0 0 12px currentColor',
            }}
          />
        </div>
      </div>

      {/* REASONS */}
      {reasons.length > 0 && (
        <div className="space-y-2 mb-4">
          <div className="text-[10px] uppercase tracking-widest text-[#8D9AAA] font-bold mb-2">
            Analysis Reasons
          </div>
          {reasons.slice(0, 4).map((r, i) => {
            const isPositive = /oversold|bounce|support|bullish|naik|up/i.test(r);
            const isNegative = /overbought|resistance|bearish|turun|down/i.test(r);
            return (
              <div
                key={i}
                className="flex items-start gap-2 text-[11px] leading-snug p-2 rounded-lg bg-black/20 border border-white/5"
              >
                <span className="mt-0.5 flex-shrink-0">
                  {isPositive ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  ) : isNegative ? (
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                  ) : (
                    <Minus className="w-3.5 h-3.5 text-[#5F6B78]" />
                  )}
                </span>
                <span className="text-[#E8EDF2]">{r}</span>
              </div>
            );
          })}
        </div>
      )}

      {/* LEVELS — hanya kalau ada action BUY/SELL */}
      {(action === 'BUY' || action === 'SELL') && (levels.entry || levels.target) && (
        <div className="grid grid-cols-3 gap-2 pt-4 border-t border-white/10">
          {levels.entry && (
            <div className="p-2 rounded-lg bg-black/30 border border-white/5 text-center">
              <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Entry</div>
              <div className="text-sm font-bold text-blue-300 font-mono">${levels.entry}</div>
            </div>
          )}
          {levels.stop && (
            <div className="p-2 rounded-lg bg-black/30 border border-white/5 text-center">
              <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Stop</div>
              <div className="text-sm font-bold text-rose-300 font-mono">${levels.stop}</div>
            </div>
          )}
          {levels.target && (
            <div className="p-2 rounded-lg bg-black/30 border border-white/5 text-center">
              <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Target</div>
              <div className="text-sm font-bold text-emerald-300 font-mono">${levels.target}</div>
            </div>
          )}
        </div>
      )}

      {/* BRAIN DIRECTION */}
      {direction && direction.direction && (
        <div className="mt-4 pt-4 border-t border-white/10">
          <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <span className="text-[10px] uppercase tracking-widest text-[#8D9AAA] font-bold">
                🎯 Brain Direction
              </span>
              <span className={`text-lg font-black tracking-wide ${
                direction.direction?.includes('BUY') ? 'text-emerald-300' :
                direction.direction?.includes('SELL') ? 'text-rose-300' :
                'text-amber-300'
              }`}>
                {direction.direction}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-[#8D9AAA]">
                Confidence: <span className="text-white font-bold">{direction.confidence?.toFixed(0)}%</span>
              </span>
              {direction.actionable && (
                <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[9px] font-bold">
                  ✅ Actionable
                </span>
              )}
            </div>
          </div>
          
          {direction.reasoning && (
            <div className="text-[10px] text-[#8D9AAA] leading-relaxed p-2 rounded bg-black/20 border border-white/5 mb-3">
              {direction.reasoning}
            </div>
          )}
          
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-3">
            {direction.entry_zone && direction.entry_zone.length >= 2 && (
              <div className="p-2 rounded bg-black/30 border border-white/5 text-center">
                <div className="text-[9px] uppercase text-[#8D9AAA]">Entry Zone</div>
                <div className="text-xs font-bold text-blue-300 font-mono">
                  ${direction.entry_zone[0]?.toFixed(2)}
                  {direction.entry_zone.length >= 2 && ` - $${direction.entry_zone[direction.entry_zone.length-1]?.toFixed(2)}`}
                </div>
              </div>
            )}
            {direction.target && (
              <div className="p-2 rounded bg-black/30 border border-white/5 text-center">
                <div className="text-[9px] uppercase text-[#8D9AAA]">Target</div>
                <div className="text-xs font-bold text-emerald-300 font-mono">
                  ${direction.target.toFixed(2)}
                  {direction.expected_return !== 0 && (
                    <span className="text-[9px] ml-1">
                      ({direction.expected_return > 0 ? '+' : ''}{direction.expected_return?.toFixed(2)}%)
                    </span>
                  )}
                </div>
              </div>
            )}
            {direction.stop && (
              <div className="p-2 rounded bg-black/30 border border-white/5 text-center">
                <div className="text-[9px] uppercase text-[#8D9AAA]">Stop</div>
                <div className="text-xs font-bold text-rose-300 font-mono">${direction.stop.toFixed(2)}</div>
              </div>
            )}
            {direction.risk_reward !== undefined && direction.risk_reward > 0 && (
              <div className="p-2 rounded bg-black/30 border border-white/5 text-center">
                <div className="text-[9px] uppercase text-[#8D9AAA]">R:R</div>
                <div className="text-xs font-bold text-white font-mono">1:{direction.risk_reward?.toFixed(1)}</div>
              </div>
            )}
          </div>
          
          {direction.experience && direction.experience.similar_decisions && direction.experience.similar_decisions > 0 && (
            <div className="p-2 rounded bg-purple-500/5 border border-purple-500/20 flex items-center justify-between flex-wrap gap-2">
              <div className="text-[10px] text-[#8D9AAA]">
                📊 <span className="text-purple-300 font-bold">{direction.experience.similar_decisions}</span> decision serupa
              </div>
              <div className="text-[10px] text-[#8D9AAA]">
                Win rate: <span className={`font-bold ${
                  (direction.experience.win_rate || 0) > 60 ? 'text-emerald-300' :
                  (direction.experience.win_rate || 0) > 40 ? 'text-amber-300' :
                  'text-rose-300'
                }`}>{direction.experience.win_rate?.toFixed(1)}%</span>
              </div>
              <div className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                direction.experience.recommendation === 'AKTIF' ? 'bg-emerald-500/20 text-emerald-300' :
                direction.experience.recommendation === 'NORMAL' ? 'bg-blue-500/20 text-blue-300' :
                direction.experience.recommendation === 'HATI-HATI' ? 'bg-amber-500/20 text-amber-300' :
                'bg-rose-500/20 text-rose-300'
              }`}>
                {direction.experience.recommendation}
              </div>
            </div>
          )}
        </div>
      )}

      {/* UNIFIED — 32 Aspek */}
      {unified && aspekCount > 0 && (
        <div className="mt-4 pt-4 border-t border-white/10">
          <div className="flex items-center justify-between mb-3">
            <div className="text-[10px] uppercase tracking-widest text-[#8D9AAA] font-bold">
              🧠 Unified Analysis
            </div>
            <div className="flex items-center gap-2 text-[10px]">
              <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 font-bold">
                {aspekCount} aspek
              </span>
              <span className={`px-2 py-0.5 rounded border font-bold ${
                unified.action === 'BUY' ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' :
                unified.action === 'SELL' ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' :
                'bg-amber-500/20 text-amber-300 border-amber-500/30'
              }`}>
                {unified.action} {unified.confidence?.toFixed(1)}%
              </span>
              <span className={`font-mono font-bold ${
                (unified.score || 0) > 0 ? 'text-emerald-300' :
                (unified.score || 0) < 0 ? 'text-rose-300' : 'text-white'
              }`}>
                {(unified.score || 0) > 0 ? '+' : ''}{unified.score?.toFixed(1)}
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-1.5">
            {Object.entries(breakdown).map(([key, value]) => {
              const v = typeof value === 'number' ? value : 0;
              const color = v > 30 ? 'text-emerald-300 bg-emerald-500/10 border-emerald-500/20' :
                            v < -30 ? 'text-rose-300 bg-rose-500/10 border-rose-500/20' :
                            v !== 0 ? 'text-amber-300 bg-amber-500/10 border-amber-500/20' :
                            'text-[#5F6B78] bg-black/20 border-white/5';
              return (
                <div
                  key={key}
                  className={`px-2 py-1 rounded border text-[9px] flex items-center justify-between gap-1 ${color}`}
                  title={`${key}: ${v}`}
                >
                  <span className="truncate font-bold uppercase tracking-wide">{key.replace(/_/g, ' ')}</span>
                  <span className="font-mono font-black flex-shrink-0">{v > 0 ? '+' : ''}{v.toFixed(0)}</span>
                </div>
              );
            })}
          </div>

          {unified.weights && (
            <div className="mt-2 text-[9px] text-[#5F6B78] text-center">
              Weights: {unified.weights} · Threshold: {unified.threshold}
            </div>
          )}
        </div>
      )}

      {/* INSIGHTS */}
      {decision?.insights && decision.insights.length > 0 && (
        <div className="mt-4 pt-4 border-t border-white/10 space-y-1">
          {decision.insights.slice(0, 2).map((ins, i) => (
            <div key={i} className="text-[10px] text-[#8D9AAA] leading-snug">
              {ins}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DecisionCard;
