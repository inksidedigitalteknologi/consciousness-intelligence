// src/components/BrainStateCard.tsx
// Brain metrics + self-model + reflection

import React from 'react';
import { Brain, Eye, Compass, Feather, Shield, Focus, Activity, Sparkles } from 'lucide-react';

interface BrainState {
  cycle?: number;
  state?: string;
  metrics?: {
    cycles?: number;
    errors?: number;
    successful_cycles?: number;
    decision_count?: number;
    learning_count?: number;
  };
  last_decision?: any;
  note?: string;
}

interface Reflection {
  awareness?: number;
  emotion?: string;
  curiosity?: number;
  insight_depth?: number;
  resilience?: number;
  focus?: number;
  confidence?: number;
  stability?: string;
  reflection_quality?: string;
  insights?: string[];
}

interface SelfModel {
  name?: string;
  age_cycles?: number;
  age_days?: number;
  emotion?: string;
  narrative?: string;
}

interface BrainStateCardProps {
  brain?: BrainState;
  reflection?: Reflection;
  selfModel?: SelfModel;
}

const EMOTION_EMOJI: Record<string, string> = {
  CALM: '😌', FOCUSED: '🎯', CURIOUS: '🤔', ALERT: '⚡',
  CONTEMPLATIVE: '🧘', EXCITED: '🚀', OPTIMISTIC: '🌟',
  CAUTIOUS: '⚠️', ANXIOUS: '😰', CONFIDENT: '💪',
};

const Meter: React.FC<{ label: string; value?: number; icon: React.ReactNode; color: string }> = ({
  label, value, icon, color,
}) => {
  const pct = Math.min(Math.max((value || 0) * 100, 0), 100);
  const colorMap: Record<string, string> = {
    'text-purple-400': 'bg-purple-500',
    'text-blue-400': 'bg-blue-500',
    'text-emerald-400': 'bg-emerald-500',
    'text-teal-400': 'bg-teal-500',
    'text-amber-400': 'bg-amber-500',
  };
  const bg = colorMap[color] || 'bg-purple-500';

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-[9px]">
        <div className="flex items-center gap-1">
          <span className={color}>{icon}</span>
          <span className="text-[#8D9AAA]">{label}</span>
        </div>
        <span className="text-white font-mono">{Math.round(pct)}%</span>
      </div>
      <div className="w-full h-1 rounded-full bg-black/40 overflow-hidden">
        <div className={`h-full rounded-full ${bg} transition-all duration-1000`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
};

export const BrainStateCard: React.FC<BrainStateCardProps> = ({ brain, reflection, selfModel }) => {
  const b = brain || {};
  const r = reflection || {};
  const s = selfModel || {};
  const m = b.metrics || {};

  return (
    <div className="glass-card rounded-2xl p-5 animate-fade-in">
      {/* HEADER */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Brain className="w-4 h-4 text-purple-400" />
          <span className="text-sm font-bold text-white uppercase tracking-wider">Brain State</span>
        </div>
        <span className={`text-[10px] px-2 py-0.5 rounded font-bold border ${
          b.state === 'ACTIVE'
            ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
            : 'bg-slate-500/20 text-slate-300 border-slate-500/30'
        }`}>
          {b.state || 'UNKNOWN'}
        </span>
      </div>

      {/* SELF-MODEL */}
      {s.name && (
        <div className="mb-4 p-3 rounded-lg bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/20">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-bold text-white">{s.name}</span>
            <span className="text-[10px] font-mono text-purple-300">
              {s.age_cycles || 0} cycles · {s.age_days || 0} hari
            </span>
          </div>
          {s.emotion && (
            <div className="text-[10px] text-[#8D9AAA]">
              {EMOTION_EMOJI[s.emotion] || '🧠'} {s.emotion}
            </div>
          )}
        </div>
      )}

      {/* METRICS GRID */}
      <div className="grid grid-cols-3 gap-2 mb-4">
        <div className="p-2 rounded-lg bg-black/30 border border-white/5 text-center">
          <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Cycles</div>
          <div className="text-sm font-black text-white font-mono">{(m.cycles || 0).toLocaleString()}</div>
        </div>
        <div className="p-2 rounded-lg bg-black/30 border border-white/5 text-center">
          <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Decisions</div>
          <div className="text-sm font-black text-cyan-300 font-mono">{(m.decision_count || 0).toLocaleString()}</div>
        </div>
        <div className="p-2 rounded-lg bg-black/30 border border-white/5 text-center">
          <div className="text-[9px] uppercase text-[#8D9AAA] tracking-wider">Learning</div>
          <div className="text-sm font-black text-emerald-300 font-mono">{(m.learning_count || 0).toLocaleString()}</div>
        </div>
      </div>

      {/* ERRORS */}
      {m.errors !== undefined && (
        <div className="flex items-center justify-between text-[10px] mb-4 px-2 py-1.5 rounded bg-black/30 border border-white/5">
          <span className="text-[#8D9AAA]">Errors</span>
          <span className={`font-mono font-bold ${m.errors > 0 ? 'text-rose-300' : 'text-emerald-300'}`}>
            {m.errors}
          </span>
        </div>
      )}

      {/* REFLECTION METERS */}
      {reflection && (r.awareness !== undefined || r.focus !== undefined) && (
        <div className="pt-4 border-t border-white/10 space-y-2.5">
          <div className="flex items-center gap-2 mb-1">
            <Sparkles className="w-3.5 h-3.5 text-purple-400" />
            <span className="text-[10px] uppercase text-[#8D9AAA] tracking-wider font-bold">Cognitive Reflection</span>
          </div>

          <Meter label="Awareness" value={r.awareness} icon={<Eye className="w-3 h-3" />} color="text-purple-400" />
          <Meter label="Curiosity" value={r.curiosity} icon={<Compass className="w-3 h-3" />} color="text-blue-400" />
          <Meter label="Insight" value={r.insight_depth} icon={<Feather className="w-3 h-3" />} color="text-teal-400" />
          <Meter label="Resilience" value={r.resilience} icon={<Shield className="w-3 h-3" />} color="text-emerald-400" />
          <Meter label="Focus" value={r.focus} icon={<Focus className="w-3 h-3" />} color="text-amber-400" />

          {/* Emotion + stability */}
          <div className="grid grid-cols-2 gap-2 pt-2">
            <div className="p-2 rounded bg-black/30 border border-white/5">
              <div className="text-[9px] text-[#8D9AAA] uppercase">Emotion</div>
              <div className="text-[11px] font-bold text-white">
                {EMOTION_EMOJI[r.emotion || ''] || '🧠'} {r.emotion || '—'}
              </div>
            </div>
            <div className="p-2 rounded bg-black/30 border border-white/5">
              <div className="text-[9px] text-[#8D9AAA] uppercase">Stability</div>
              <div className={`text-[11px] font-bold ${
                r.stability === 'STABLE' ? 'text-emerald-300' :
                r.stability === 'ADAPTING' ? 'text-amber-300' : 'text-rose-300'
              }`}>
                {r.stability || '—'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* INSIGHTS */}
      {r.insights && r.insights.length > 0 && (
        <div className="mt-3 pt-3 border-t border-white/10 space-y-1">
          {r.insights.slice(0, 2).map((ins, i) => (
            <div key={i} className="text-[10px] text-[#8D9AAA] leading-snug">
              {ins}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BrainStateCard;
