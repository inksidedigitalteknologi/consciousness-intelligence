// src/components/BrainView.tsx
// INKSIDE DIGITAL - COGNITIVE BRAIN ENGINE v8.0
// Pipeline + Reflection + Developer/Trader tabs

import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Brain, Cpu, Eye, Compass, Feather, Shield, Globe,
  Database, Code, Atom, Dna, Droplets, Leaf, Flame,
  Telescope, Microscope, Palette, Music, Film, Coffee, Heart,
  Network, Server, Loader2, ChevronLeft, ChevronRight,
  CheckCircle2, XCircle, Clock, AlertTriangle, Sparkles,
  Wrench, TrendingUp, Activity, Zap, BookOpen,
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface PipelineStage {
  name: string;
  key: string;
  module: string;
  status: string;
  note: string;
  reason_source?: string;
  reason_preview?: string;
}

interface PipelineData {
  stages: PipelineStage[];
  modules: { available: string[]; unavailable: string[]; total: number; loaded: number };
  meta: {
    cycles: number; errors: number; state: string;
    success_rate: number; error_rate: number; avg_processing_ms: number;
    learning_count: number; prediction_count: number; decision_count: number;
    health_score: number;
  };
}

interface Reflection {
  awareness: number;
  emotion: string;
  curiosity: number;
  insight_depth: number;
  resilience: number;
  focus: number;
  confidence: number;
  stability: string;
  reflection_quality: string;
  insights: string[];
}

interface SystemMetrics {
  cpu: number;
  ram: number;
  ram_percent: number;
  disk_percent: number;
  uptime: number;
  health_score: number;
}

interface AIStatus {
  enabled: boolean;
  model: string;
  reason_stats: { hits: number; misses: number; errors: number; cache_size: number };
}

interface Performance {
  total_dividend?: number;
  avg_dividend?: number;
  total_companies?: number;
  roi?: number;
  trades?: number;
  win_rate?: number;
  total_pnl?: number;
}

interface KnowledgeItem {
  id: string;
  content: string;
  category: string;
  tags: string[];
  created_at?: string;
}

interface SelfData {
  self: {
    name: string;
    birth: string | null;
    age_cycles: number;
    age_days: number;
    emotion: string;
    narrative: string;
    experiences_count: number;
    milestones_count: number;
  };
  metrics: {
    cycles: number;
    success_rate: number;
    error_rate: number;
    decision_count: number;
    learning_count: number;
    prediction_count: number;
    health_score: number;
  };
  performance: {
    total_decisions_logged: number;
    decision_mix: { BUY: number; SELL: number; HOLD: number; OTHER: number };
    avg_confidence: number;
    ai_reason_stats: { hits: number; misses: number; errors: number; cache_size: number };
    ai_usage_pct: number;
  };
  knowledge: {
    total: number;
    categories: number;
    ai_enhanced: number;
  };
}

interface BrainViewProps {
  brainState: string;
  cycleCount: number;
  healthScore: number;
  wsConnected?: boolean;
}

// ============================================================
// CONSTANTS
// ============================================================

const STATUS_STYLE: Record<string, { bg: string; text: string; icon: React.ReactNode }> = {
  ACTIVE:   { bg: 'bg-emerald-500/10 border-emerald-500/20', text: 'text-emerald-400', icon: <CheckCircle2 className="w-3 h-3" /> },
  IDLE:     { bg: 'bg-slate-500/10 border-slate-500/20',     text: 'text-slate-400',   icon: <Clock className="w-3 h-3" /> },
  FALLBACK: { bg: 'bg-amber-500/10 border-amber-500/20',     text: 'text-amber-400',   icon: <AlertTriangle className="w-3 h-3" /> },
  OFFLINE:  { bg: 'bg-rose-500/10 border-rose-500/20',       text: 'text-rose-400',    icon: <XCircle className="w-3 h-3" /> },
  ERROR:    { bg: 'bg-rose-500/10 border-rose-500/20',       text: 'text-rose-400',    icon: <XCircle className="w-3 h-3" /> },
};

const EMOTION_MAP: Record<string, string> = {
  CALM: '😌', FOCUSED: '🎯', CURIOUS: '🤔', ALERT: '⚡',
  CONTEMPLATIVE: '🧘', EXCITED: '🔥', OPTIMISTIC: '🌟',
  CAUTIOUS: '⚠️', ANXIOUS: '😰', CONFIDENT: '💪',
};

const KNOWLEDGE_DOMAINS = [
  { icon: <Database className="w-4 h-4" />, label: 'Data Science', color: 'text-cyan-400' },
  { icon: <Code className="w-4 h-4" />, label: 'Programming', color: 'text-blue-400' },
  { icon: <Atom className="w-4 h-4" />, label: 'Physics', color: 'text-indigo-400' },
  { icon: <Dna className="w-4 h-4" />, label: 'Biology', color: 'text-emerald-400' },
  { icon: <Droplets className="w-4 h-4" />, label: 'Chemistry', color: 'text-cyan-400' },
  { icon: <Leaf className="w-4 h-4" />, label: 'Environment', color: 'text-green-400' },
  { icon: <Flame className="w-4 h-4" />, label: 'Energy', color: 'text-orange-400' },
  { icon: <Globe className="w-4 h-4" />, label: 'Geography', color: 'text-emerald-400' },
  { icon: <Telescope className="w-4 h-4" />, label: 'Astronomy', color: 'text-purple-400' },
  { icon: <Microscope className="w-4 h-4" />, label: 'Science', color: 'text-blue-400' },
  { icon: <Palette className="w-4 h-4" />, label: 'Art', color: 'text-pink-400' },
  { icon: <Music className="w-4 h-4" />, label: 'Music', color: 'text-rose-400' },
  { icon: <Film className="w-4 h-4" />, label: 'Film', color: 'text-indigo-400' },
  { icon: <Coffee className="w-4 h-4" />, label: 'Culture', color: 'text-amber-400' },
  { icon: <Heart className="w-4 h-4" />, label: 'Health', color: 'text-rose-400' },
  { icon: <Brain className="w-4 h-4" />, label: 'Neuroscience', color: 'text-purple-400' },
  { icon: <Network className="w-4 h-4" />, label: 'Networking', color: 'text-cyan-400' },
  { icon: <Server className="w-4 h-4" />, label: 'Infrastructure', color: 'text-gray-400' },
];

// ============================================================
// METER
// ============================================================

const Meter: React.FC<{ label: string; value: number; color: string; icon: React.ReactNode }> = ({
  label, value, color, icon,
}) => {
  const pct = Math.min(Math.max(value * 100, 0), 100);
  const bg = color.replace('text-', 'bg-').replace('-400', '-500');
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-[10px]">
        <div className="flex items-center gap-1.5">
          <span className={color}>{icon}</span>
          <span className="text-[#8D9AAA]">{label}</span>
        </div>
        <span className="text-white font-mono">{Math.round(pct)}%</span>
      </div>
      <div className="w-full h-1 rounded-full bg-[#26313D] overflow-hidden">
        <div className={`h-full rounded-full ${bg} transition-all duration-700`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
};

// ============================================================
// MAIN
// ============================================================

export const BrainView: React.FC<BrainViewProps> = ({
  brainState, cycleCount, healthScore, wsConnected,
}) => {
  const [pipeline, setPipeline] = useState<PipelineData | null>(null);
  const [reflection, setReflection] = useState<Reflection | null>(null);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [aiStatus, setAiStatus] = useState<AIStatus | null>(null);
  const [selfData, setSelfData] = useState<SelfData | null>(null);
  const [knowledge, setKnowledge] = useState<KnowledgeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [activeTab, setActiveTab] = useState<'developer' | 'trader'>(() => {
    return (localStorage.getItem('brain_tab') as 'developer' | 'trader') || 'developer';
  });

  const touchStartX = useRef<number | null>(null);
  const touchEndX = useRef<number | null>(null);

  const apiKey = localStorage.getItem('apiKey') || 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ';

  // ============================================================
  // FETCH
  // ============================================================

  const fetchAll = useCallback(async () => {
    try {
      const [pRes, rRes, mRes, aRes, sRes, kRes] = await Promise.all([
        fetch('/api/brain/pipeline', { headers: { 'X-API-Key': apiKey } }),
        fetch('/api/brain/reflection', { headers: { 'X-API-Key': apiKey } }),
        fetch('/api/system/metrics', { headers: { 'X-API-Key': apiKey } }),
        fetch('/api/brain/ai/status', { headers: { 'X-API-Key': apiKey } }),
        fetch('/api/brain/self', { headers: { 'X-API-Key': apiKey } }),
        fetch('/api/knowledge/all', { headers: { 'X-API-Key': apiKey } }),
      ]);
      if (pRes.ok) setPipeline(await pRes.json());
      if (rRes.ok) setReflection(await rRes.json());
      if (mRes.ok) setMetrics(await mRes.json());
      if (aRes.ok) setAiStatus(await aRes.json());
      if (sRes.ok) setSelfData(await sRes.json());
      if (kRes.ok) {
        const d = await kRes.json();
        setKnowledge(d.items || []);
      }
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'fetch failed');
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  useEffect(() => {
    fetchAll();
    const iv = setInterval(fetchAll, 30000);
    return () => clearInterval(iv);
  }, [fetchAll]);

  useEffect(() => {
    localStorage.setItem('brain_tab', activeTab);
  }, [activeTab]);

  // ============================================================
  // PAGES (pipeline)
  // ============================================================

  const stages = pipeline?.stages || [];
  const modules = pipeline?.modules;

  const pages = [
    {
      title: 'Cognitive Pipeline',
      subtitle: `${stages.length} stages — real from brain.observe()`,
      items: stages.map((s) => ({ kind: 'stage' as const, data: s })),
    },
    {
      title: 'Available Modules',
      subtitle: `${modules?.loaded || 0}/${modules?.total || 0} loaded`,
      items: (modules?.available || []).map((m) => ({ kind: 'module' as const, name: m, ok: true })),
    },
  ];

  const totalPages = pages.length;

  const goToPage = (p: number) => {
    if (p < 0) p = totalPages - 1;
    if (p >= totalPages) p = 0;
    setPage(p);
  };

  const onTouchStart = (e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX;
    touchEndX.current = null;
  };
  const onTouchMove = (e: React.TouchEvent) => {
    touchEndX.current = e.touches[0].clientX;
  };
  const onTouchEnd = () => {
    if (touchStartX.current === null || touchEndX.current === null) return;
    const delta = touchStartX.current - touchEndX.current;
    if (delta > 50) goToPage(page + 1);
    else if (delta < -50) goToPage(page - 1);
    touchStartX.current = null;
    touchEndX.current = null;
  };

  const meta = pipeline?.meta;

  // Recent decisions — extract dari knowledge items
  const recentDecisions = knowledge
    .filter((k) => k.tags?.includes('auto-observe') || k.tags?.includes('brain'))
    .slice(0, 5)
    .map((k) => {
      const m = k.content.match(/Decision:\s*(\w+)\s*\(conf\s*([\d.]+)%\)/);
      if (!m) return null;
      return { action: m[1], confidence: parseFloat(m[2]), preview: k.content };
    })
    .filter(Boolean) as { action: string; confidence: number; preview: string }[];

  const latestDecision = stages.find((s) => s.key === 'decision');

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div id="brain-view" className="space-y-5 pb-12">
      {/* HEADER */}
      <div className="p-4 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white tracking-wide">
              Cognitive Brain Engine v8.0
            </h2>
            <p className="text-[11px] text-[#8D9AAA]">
              Real pipeline · Cognitive reflection · Developer + Trader views
            </p>
          </div>
        </div>
        <span className={`text-xs px-2 py-0.5 rounded font-bold ${wsConnected
          ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20'
          : 'bg-rose-500/20 text-rose-400 border border-rose-500/20'}`}>
          {wsConnected ? '🟢 LIVE' : '🔴 OFFLINE'}
        </span>
      </div>

      {/* META PANEL */}
      {meta && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-2.5">
          <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
            <div className="text-[10px] text-[#8D9AAA] uppercase">Cycles</div>
            <div className="text-lg font-black text-white font-mono">{meta.cycles}</div>
            <div className="text-[9px] text-[#5F6B78]">brain runs</div>
          </div>
          <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
            <div className="text-[10px] text-[#8D9AAA] uppercase">Success</div>
            <div className="text-lg font-black text-emerald-400 font-mono">{meta.success_rate}%</div>
            <div className="text-[9px] text-[#5F6B78]">dari {meta.cycles} cycle</div>
          </div>
          <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
            <div className="text-[10px] text-[#8D9AAA] uppercase">Decisions</div>
            <div className="text-lg font-black text-blue-400 font-mono">{meta.decision_count}</div>
            <div className="text-[9px] text-[#5F6B78]">output</div>
          </div>
          <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
            <div className="text-[10px] text-[#8D9AAA] uppercase">Avg Latency</div>
            <div className="text-lg font-black text-amber-400 font-mono">{meta.avg_processing_ms}ms</div>
            <div className="text-[9px] text-[#5F6B78]">per cycle</div>
          </div>
          <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D] col-span-2 md:col-span-1">
            <div className="text-[10px] text-[#8D9AAA] uppercase">Health</div>
            <div className="text-lg font-black text-emerald-400 font-mono">{meta.health_score}%</div>
            <div className="text-[9px] text-[#5F6B78]">sistem</div>
          </div>
        </div>
      )}

      {/* PIPELINE + REFLECTION */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* PIPELINE */}
        <div className="lg:col-span-2 p-4 rounded-2xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <div>
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Cpu className="w-4 h-4 text-blue-400" />
                {pages[page]?.title || 'Pipeline'}
              </h3>
              <p className="text-[10px] text-[#5F6B78] mt-0.5">{pages[page]?.subtitle}</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] text-[#5F6B78] font-mono">{page + 1}/{totalPages}</span>
              <button onClick={() => goToPage(page - 1)}
                className="p-1 rounded-md bg-[#1A2530] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white">
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button onClick={() => goToPage(page + 1)}
                className="p-1 rounded-md bg-[#1A2530] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white">
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {loading ? (
            <div className="py-8 flex items-center justify-center text-[#5F6B78] text-xs">
              <Loader2 className="w-4 h-4 animate-spin mr-2" /> Memuat pipeline...
            </div>
          ) : (
            <div className="mt-3 overflow-hidden" onTouchStart={onTouchStart}
              onTouchMove={onTouchMove} onTouchEnd={onTouchEnd}>
              <div className="flex transition-transform duration-500 ease-out"
                style={{ transform: `translateX(-${page * 100}%)` }}>
                {pages.map((pg, pIdx) => (
                  <div key={pIdx} className="w-full flex-shrink-0 space-y-1.5 max-h-[460px] overflow-y-auto pr-1">
                    {pg.items.map((item, i) => {
                      if (item.kind === 'stage') {
                        const s = item.data;
                        const st = STATUS_STYLE[s.status] || STATUS_STYLE.IDLE;
                        const isDecision = s.key === 'decision';
                        return (
                          <div key={i} className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                            <div className="flex items-center justify-between gap-3">
                              <div className="min-w-0 flex-1">
                                <div className="flex items-center gap-2">
                                  <span className="font-bold text-white text-xs">{s.name}</span>

                                </div>
                                <p className="text-[10px] text-[#8D9AAA] truncate">{s.note}</p>
                              </div>
                              <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded border flex items-center gap-1 flex-shrink-0 ${st.bg} ${st.text}`}>
                                {st.icon} {s.status}
                              </span>
                            </div>
                          </div>
                        );
                      } else {
                        return (
                          <div key={i}
                            className="p-2 rounded-lg bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
                            <span className="text-xs font-mono text-[#E8EDF2]">{item.name}</span>
                            {item.ok ? (
                              <span className="text-[10px] text-emerald-400">✓</span>
                            ) : (
                              <span className="text-[10px] text-rose-400">✗</span>
                            )}
                          </div>
                        );
                      }
                    })}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex items-center justify-center gap-2 pt-3">
            {pages.map((_, idx) => (
              <button key={idx} onClick={() => goToPage(idx)}
                className={`h-1.5 rounded-full transition-all duration-300 ${
                  idx === page ? 'w-6 bg-blue-500' : 'w-1.5 bg-[#26313D] hover:bg-[#3A4A5A]'
                }`} />
            ))}
          </div>
        </div>

        {/* REFLECTION */}
        <div className="p-4 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-3">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400" />
              Cognitive Reflection
            </h3>
          </div>

          {!reflection ? (
            <div className="py-8 text-center text-xs text-[#5F6B78]">
              <Loader2 className="w-4 h-4 animate-spin mx-auto mb-2" />
              Memuat refleksi...
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{EMOTION_MAP[reflection.emotion] || '🧠'}</span>
                  <div>
                    <div className="text-[10px] text-[#8D9AAA]">Emotion</div>
                    <div className="text-xs font-bold text-white">{reflection.emotion}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-[10px] text-[#8D9AAA]">Stability</div>
                  <div className={`text-xs font-bold ${
                    reflection.stability === 'STABLE' ? 'text-emerald-400' :
                    reflection.stability === 'ADAPTING' ? 'text-amber-400' : 'text-rose-400'
                  }`}>{reflection.stability}</div>
                </div>
              </div>

              <div className="space-y-2.5">
                <Meter label="Awareness" value={reflection.awareness} color="text-purple-400" icon={<Eye className="w-3 h-3" />} />
                <Meter label="Curiosity" value={reflection.curiosity} color="text-blue-400" icon={<Compass className="w-3 h-3" />} />
                <Meter label="Insight Depth" value={reflection.insight_depth} color="text-teal-400" icon={<Feather className="w-3 h-3" />} />
                <Meter label="Resilience" value={reflection.resilience} color="text-emerald-400" icon={<Shield className="w-3 h-3" />} />
                <Meter label="Focus" value={reflection.focus} color="text-amber-400" icon={<Sparkles className="w-3 h-3" />} />
              </div>

              <div className="grid grid-cols-2 gap-2 text-[10px]">
                <div className="p-2 rounded bg-[#1A2530] border border-[#26313D]">
                  <div className="text-[#8D9AAA]">Quality</div>
                  <div className={`font-bold ${
                    reflection.reflection_quality === 'EXCELLENT' ? 'text-emerald-400' :
                    reflection.reflection_quality === 'GOOD' ? 'text-blue-400' :
                    reflection.reflection_quality === 'FAIR' ? 'text-amber-400' : 'text-rose-400'
                  }`}>{reflection.reflection_quality}</div>
                </div>
                <div className="p-2 rounded bg-[#1A2530] border border-[#26313D]">
                  <div className="text-[#8D9AAA]">Confidence</div>
                  <div className="font-bold text-white">{Math.round(reflection.confidence * 100)}%</div>
                </div>
              </div>

              {reflection.insights && reflection.insights.length > 0 && (
                <div className="pt-2 border-t border-[#26313D] space-y-1.5">
                  <div className="text-[10px] text-[#8D9AAA] uppercase">Insights</div>
                  {reflection.insights.slice(0, 3).map((ins, idx) => (
                    <div key={idx} className="text-[10px] text-[#E8EDF2] leading-snug">{ins}</div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* ==================== TAB: Developer / Trader ==================== */}
      <div className="rounded-2xl bg-[#131A22] border border-[#26313D] overflow-hidden">
        {/* Tab header */}
        <div className="flex border-b border-[#26313D]">
          <button
            onClick={() => setActiveTab('developer')}
            className={`flex items-center gap-2 px-5 py-3 text-xs font-bold uppercase tracking-wider transition-colors ${
              activeTab === 'developer'
                ? 'text-white bg-[#1A2530] border-b-2 border-blue-500'
                : 'text-[#8D9AAA] hover:text-white hover:bg-[#1A2530]/50'
            }`}>
            <Wrench className="w-3.5 h-3.5" />
            Developer
          </button>
          <button
            onClick={() => setActiveTab('trader')}
            className={`flex items-center gap-2 px-5 py-3 text-xs font-bold uppercase tracking-wider transition-colors ${
              activeTab === 'trader'
                ? 'text-white bg-[#1A2530] border-b-2 border-emerald-500'
                : 'text-[#8D9AAA] hover:text-white hover:bg-[#1A2530]/50'
            }`}>
            <TrendingUp className="w-3.5 h-3.5" />
            Trader
          </button>
        </div>

        {/* Tab content */}
        <div className="p-5">
          {/* ============ DEVELOPER TAB ============ */}
          {activeTab === 'developer' && (
            <div className="space-y-4">
              {/* System Resources */}
              <div>
                <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2.5 flex items-center gap-2">
                  <Activity className="w-3.5 h-3.5 text-blue-400" />
                  System Resources
                </h4>
                {metrics ? (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5">
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">CPU</div>
                      <div className="text-sm font-bold text-white font-mono">{metrics.cpu.toFixed(1)}%</div>
                    </div>
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">RAM</div>
                      <div className="text-sm font-bold text-white font-mono">{metrics.ram_percent.toFixed(1)}%</div>
                    </div>
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">Disk</div>
                      <div className="text-sm font-bold text-white font-mono">{metrics.disk_percent.toFixed(1)}%</div>
                    </div>
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">Uptime</div>
                      <div className="text-sm font-bold text-white font-mono">
                        {Math.floor(metrics.uptime / 3600)}h {Math.floor((metrics.uptime % 3600) / 60)}m
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-xs text-[#5F6B78]">Loading...</div>
                )}
              </div>

              {/* AI Status */}
              <div>
                <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2.5 flex items-center gap-2">
                  <Zap className="w-3.5 h-3.5 text-purple-400" />
                  AI Status
                </h4>
                {aiStatus ? (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5">
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">DeepSeek</div>
                      <div className={`text-sm font-bold ${aiStatus.enabled ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {aiStatus.enabled ? 'ENABLED' : 'DISABLED'}
                      </div>
                    </div>
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">Model</div>
                      <div className="text-sm font-bold text-white font-mono text-[11px]">{aiStatus.model || '—'}</div>
                    </div>
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">Cache Hits</div>
                      <div className="text-sm font-bold text-white font-mono">
                        {aiStatus.reason_stats?.hits || 0}
                      </div>
                    </div>
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">AI Errors</div>
                      <div className={`text-sm font-bold font-mono ${(aiStatus.reason_stats?.errors || 0) > 0 ? 'text-rose-400' : 'text-white'}`}>
                        {aiStatus.reason_stats?.errors || 0}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-xs text-[#5F6B78]">Loading...</div>
                )}
              </div>

              {/* Module Health */}
              {modules && (
                <div>
                  <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2.5 flex items-center gap-2">
                    <Server className="w-3.5 h-3.5 text-emerald-400" />
                    Module Health — {modules.loaded}/{modules.total} loaded
                  </h4>
                  <div className="flex flex-wrap gap-1.5">
                    {modules.available.map((m) => (
                      <span key={m} className="text-[10px] px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                        ✓ {m}
                      </span>
                    ))}
                    {modules.unavailable.map((m) => (
                      <span key={m} className="text-[10px] px-2 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 font-mono">
                        ✗ {m}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* ============ TRADER TAB ============ */}
          {activeTab === 'trader' && (
            <div className="space-y-4">
              {/* Latest Decision — HERO */}
              {latestDecision && latestDecision.reason_preview && (
                <div className="p-4 rounded-xl bg-gradient-to-br from-purple-500/10 to-blue-500/10 border border-purple-500/30">
                  <div className="flex items-center gap-2 mb-2">
                    <Sparkles className="w-4 h-4 text-purple-400" />
                    <span className="text-xs font-bold text-white uppercase tracking-wider">Latest Decision</span>
                  </div>
                  <div className="text-[11px] text-[#E8EDF2] leading-relaxed whitespace-pre-line">
                    {latestDecision.reason_preview}
                  </div>
                </div>
              )}

              {/* Inkside Performance — real dari self_model */}
              {selfData && (
                <div>
                  <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2.5 flex items-center gap-2">
                    <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                    Inkside Performance
                  </h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5">
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">Umur</div>
                      <div className="text-sm font-bold text-white font-mono">
                        {selfData.self.age_cycles} cycles
                      </div>
                      <div className="text-[9px] text-[#5F6B78]">{selfData.self.age_days} hari</div>
                    </div>
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">Decisions</div>
                      <div className="text-sm font-bold text-blue-400 font-mono">
                        {selfData.performance.total_decisions_logged}
                      </div>
                      <div className="text-[9px] text-[#5F6B78]">tersimpan</div>
                    </div>
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">Avg Confidence</div>
                      <div className="text-sm font-bold text-amber-400 font-mono">
                        {selfData.performance.avg_confidence.toFixed(1)}%
                      </div>
                      <div className="text-[9px] text-[#5F6B78]">dari log</div>
                    </div>
                    <div className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D]">
                      <div className="text-[10px] text-[#8D9AAA]">Reason Mode</div>
                      <div className="text-sm font-bold text-cyan-400 font-mono">
                        TEMPLATE
                      </div>
                      <div className="text-[9px] text-[#5F6B78]">
                        deterministic
                      </div>
                    </div>
                  </div>

                  {/* Decision Mix */}
                  <div className="mt-3 p-3 rounded-lg bg-[#1A2530] border border-[#26313D]">
                    <div className="text-[10px] text-[#8D9AAA] mb-2">Decision Mix</div>
                    <div className="flex gap-3 text-[11px] font-mono">
                      <span className="text-emerald-400">
                        BUY: {selfData.performance.decision_mix.BUY}
                      </span>
                      <span className="text-rose-400">
                        SELL: {selfData.performance.decision_mix.SELL}
                      </span>
                      <span className="text-slate-400">
                        HOLD: {selfData.performance.decision_mix.HOLD}
                      </span>
                    </div>
                  </div>

                  {/* Knowledge Growth */}
                  <div className="mt-3 p-3 rounded-lg bg-[#1A2530] border border-[#26313D] flex justify-between items-center">
                    <div className="text-[10px] text-[#8D9AAA]">Knowledge Base</div>
                    <div className="text-sm font-bold text-cyan-400 font-mono">
                      {selfData.knowledge.total} items · {selfData.knowledge.categories} kategori
                    </div>
                  </div>

                  {/* Self Info */}
                  <div className="mt-3 p-3 rounded-lg bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/20">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] text-[#8D9AAA]">Self</span>
                      <span className="text-[10px] font-bold text-white">
                        {selfData.self.name}
                      </span>
                      <span className="text-[9px] text-purple-400">
                        {selfData.self.emotion}
                      </span>
                    </div>
                    <div className="text-[10px] text-[#E8EDF2] italic leading-snug">
                      "{selfData.self.narrative}"
                    </div>
                  </div>
                </div>
              )}

              {/* Recent Decisions */}
              {recentDecisions.length > 0 && (
                <div>
                  <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2.5 flex items-center gap-2">
                    <BookOpen className="w-3.5 h-3.5 text-blue-400" />
                    Recent Decisions ({recentDecisions.length})
                  </h4>
                  <div className="space-y-1.5">
                    {recentDecisions.map((d, i) => (
                      <div key={i} className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center gap-2">
                            <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                              d.action === 'BUY' ? 'bg-emerald-500/20 text-emerald-400' :
                              d.action === 'SELL' ? 'bg-rose-500/20 text-rose-400' :
                              'bg-slate-500/20 text-slate-400'
                            }`}>{d.action}</span>
                            <span className="text-[10px] text-[#8D9AAA] font-mono">conf {d.confidence}%</span>
                          </div>
                          <p className="text-[10px] text-[#5F6B78] truncate mt-0.5">{d.preview}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {recentDecisions.length === 0 && (
                <div className="text-xs text-[#5F6B78] py-2">
                  Belum ada decision tersimpan. Tunggu scheduler beberapa cycle.
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* KNOWLEDGE DOMAINS */}
      <div className="p-4 rounded-2xl bg-[#131A22] border border-[#26313D]">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Globe className="w-4 h-4 text-cyan-400" />
            Universal Knowledge Domains
          </h3>
          <span className="text-[11px] text-[#5F6B78]">AI-powered · Multi-domain</span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-2 mt-3">
          {KNOWLEDGE_DOMAINS.map((d, i) => (
            <div key={i}
              className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D] flex items-center gap-2 hover:border-purple-500/30 transition-all">
              <span className={d.color}>{d.icon}</span>
              <span className="text-[10px] text-[#8D9AAA]">{d.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BrainView;
