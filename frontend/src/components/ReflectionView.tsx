import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Sparkle, Shield, Compass, Eye, Heart, Zap,
  Brain, Database, Cpu, BookOpen, TrendingUp,
  RefreshCw, AlertCircle, CheckCircle2, Loader2,
  Activity, BarChart3, Gauge, Network, Layers,
  Target, Clock, GitBranch, Radio, Signal,
  Globe, Lock, Unlock, ChevronUp, ChevronDown,
  PieChart, LineChart, Radar, Map, Satellite,
  Cpu as CpuIcon, HardDrive, Cloud, Server
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface CognitiveMetrics {
  knowledge: {
    total_items: number;
    categories: number;
    avg_confidence: number;
    ai_enhanced: number;
    active: number;
    archived: number;
  };
  brain: {
    health: number;
    consciousness: number;
    emotional_state: string;
    learning_rate: number;
    curiosity_level: number;
  };
  system: {
    cpu: number;
    ram_percent: number;
    disk_percent: number;
    uptime_seconds: number;
    uptime_hours: number;
    uptime_days: number;
    health_score: number;
  };
  learning: {
    active_modules: number;
    total_modules: number;
    learning_cycles: number;
    accuracy: number;
    curiosity_level: number;
  };
  memory: {
    total_items: number;
    semantic_relationships: number;
  };
  pattern: {
    detected: number;
    accuracy: number;
    by_type: Record<string, number>;
  };
  trading: {
    pnl: number;
    win_rate: number;
    total_trades: number;
    open_positions: number;
  };
  websocket: {
    connected: boolean;
    active_channels: number;
  };
  timestamp: string;
}

interface Reflection {
  type: string;
  icon: string;
  content: string;
  importance: 'high' | 'medium' | 'low';
}

// ============================================================
// SUB-COMPONENTS
// ============================================================

const AnimatedCircularProgress: React.FC<{
  value: number;
  label: string;
  icon: React.ReactNode;
  color: string;
  sublabel?: string;
  size?: 'sm' | 'md' | 'lg';
}> = ({ value, label, icon, color, sublabel, size = 'md' }) => {
  const radius = size === 'sm' ? 28 : size === 'lg' ? 40 : 34;
  const strokeWidth = size === 'sm' ? 6 : size === 'lg' ? 8 : 7;
  const circumference = 2 * Math.PI * radius;
  const clampedValue = Math.min(Math.max(value, 0), 100);
  const offset = circumference - (clampedValue / 100) * circumference;

  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-20 h-20',
    lg: 'w-28 h-28'
  };

  const textSizes = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-2xl'
  };

  return (
    <div className="flex flex-col items-center group">
      <div className={`relative ${sizeClasses[size]} flex items-center justify-center`}>
        <svg className="w-full h-full -rotate-90 transform transition-all duration-700">
          <circle
            cx="50%"
            cy="50%"
            r={radius}
            className="stroke-[#1A2530]"
            strokeWidth={strokeWidth}
            fill="none"
          />
          <circle
            cx="50%"
            cy="50%"
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            fill="none"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center">
          <span className={`${textSizes[size]} font-black text-white font-mono tracking-tight`}>
            {Math.round(clampedValue)}%
          </span>
        </div>
      </div>
      <div className="mt-2 text-center">
        <div className="flex items-center justify-center gap-1.5">
          <span className="text-[10px] font-semibold text-white tracking-wide">{label}</span>
        </div>
        {sublabel && (
          <p className="text-[8px] text-[#5F6B78] mt-0.5">{sublabel}</p>
        )}
      </div>
    </div>
  );
};

const GlowCard: React.FC<{
  children: React.ReactNode;
  className?: string;
  glowColor?: string;
}> = ({ children, className = '', glowColor = 'purple-500/20' }) => (
  <div className={`relative group ${className}`}>
    <div className={`absolute -inset-0.5 bg-gradient-to-r from-${glowColor} to-transparent rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />
    <div className="relative bg-[#131A22] border border-[#26313D] rounded-2xl p-5 hover:border-purple-500/40 transition-all duration-300 shadow-xl">
      {children}
    </div>
  </div>
);

// ============================================================
// MAIN COMPONENT
// ============================================================

export const ReflectionView: React.FC = () => {
  const [metrics, setMetrics] = useState<CognitiveMetrics | null>(null);
  const [reflections, setReflections] = useState<Reflection[]>([]);
  const [narrative, setNarrative] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    details: true,
    system: true,
    learning: true
  });
  const [apiKey] = useState<string>(localStorage.getItem('apiKey') || 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ');
  const [animating, setAnimating] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // ============================================================
  // FETCH REAL DATA
  // ============================================================

  const fetchMetrics = useCallback(async () => {
    try {
      const response = await fetch('/api/cognitive-mirror/metrics', {
        headers: { 'X-API-Key': apiKey }
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setMetrics(data);
      setLastUpdate(data.timestamp);
    } catch (error) {
      console.error('Failed to fetch cognitive metrics:', error);
      setError('Failed to load cognitive metrics');
    }
  }, [apiKey]);

  const fetchReflections = useCallback(async () => {
    try {
      const response = await fetch('/api/cognitive-mirror/reflections', {
        headers: { 'X-API-Key': apiKey }
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setReflections(data.reflections || []);
    } catch (error) {
      console.error('Failed to fetch reflections:', error);
    }
  }, [apiKey]);

  const fetchNarrative = useCallback(async () => {
    try {
      const response = await fetch('/api/cognitive-mirror/narrative', {
        headers: { 'X-API-Key': apiKey }
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setNarrative(data.summary || 'System is initializing...');
    } catch (error) {
      console.error('Failed to fetch narrative:', error);
    }
  }, [apiKey]);

  const fetchAllData = useCallback(async () => {
    if (animating) return;
    setAnimating(true);
    await Promise.all([fetchMetrics(), fetchReflections(), fetchNarrative()]);
    setAnimating(false);
    setIsLoading(false);
  }, [fetchMetrics, fetchReflections, fetchNarrative, animating]);

  // ============================================================
  // INIT
  // ============================================================

  useEffect(() => {
    fetchAllData();

    intervalRef.current = setInterval(fetchAllData, 30000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [fetchAllData]);

  // ============================================================
  // COMPUTED VALUES
  // ============================================================

  const getMetricValue = (path: string): number => {
    if (!metrics) return 0;
    const parts = path.split('.');
    let value: any = metrics;
    for (const part of parts) {
      if (value && typeof value === 'object' && part in value) {
        value = value[part];
      } else {
        return 0;
      }
    }
    return typeof value === 'number' ? value : 0;
  };

  const cognitiveMetrics = [
    { label: 'Awareness', value: getMetricValue('brain.consciousness') * 100 || getMetricValue('system.health_score'), color: '#3B82F6', icon: <Eye className="w-3.5 h-3.5" />, sublabel: 'Self-awareness & health' },
    { label: 'Curiosity', value: getMetricValue('brain.curiosity_level') * 100 || getMetricValue('learning.curiosity_level') * 100, color: '#8B5CF6', icon: <Compass className="w-3.5 h-3.5" />, sublabel: 'Active learning' },
    { label: 'Insight Depth', value: Math.min(getMetricValue('knowledge.avg_confidence') || 70, 100), color: '#06B6D4', icon: <Sparkle className="w-3.5 h-3.5" />, sublabel: 'Knowledge quality' },
    { label: 'Resilience', value: Math.max(0, 100 - getMetricValue('system.cpu') - (getMetricValue('system.ram_percent') || 0) / 4), color: '#22C55E', icon: <Shield className="w-3.5 h-3.5" />, sublabel: 'System stability' },
    { label: 'Focus', value: Math.min(100, (getMetricValue('learning.active_modules') / Math.max(getMetricValue('learning.total_modules'), 1)) * 100), color: '#F59E0B', icon: <Zap className="w-3.5 h-3.5" />, sublabel: 'Active processing' },
  ];

  const healthStatus = metrics?.system?.health_score || 0;
  const healthColor = healthStatus > 85 ? '#22C55E' : healthStatus > 70 ? '#F59E0B' : '#EF4444';
  const healthEmoji = healthStatus > 85 ? '🌟' : healthStatus > 70 ? '🟢' : '⚠️';

  // ============================================================
  // RENDER
  // ============================================================

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[500px]">
        <div className="relative">
          <div className="w-20 h-20 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin" />
          <div className="absolute inset-0 flex items-center justify-center">
            <Brain className="w-8 h-8 text-purple-400 animate-pulse" />
          </div>
        </div>
        <p className="mt-4 text-[#8D9AAA] text-sm font-medium animate-pulse">🧠 Reflecting on cognitive state...</p>
        <p className="text-[10px] text-[#5F6B78] mt-1">Loading neural metrics from system</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] p-8">
        <div className="w-16 h-16 rounded-2xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center mb-4">
          <AlertCircle className="w-8 h-8 text-rose-400" />
        </div>
        <p className="text-rose-400 text-sm font-medium">{error}</p>
        <button
          onClick={fetchAllData}
          className="mt-4 px-6 py-2.5 bg-purple-600 hover:bg-purple-500 rounded-xl text-white text-sm font-bold transition-all shadow-lg shadow-purple-600/30 flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-12 max-w-7xl mx-auto">

      {/* ===== TOP BANNER ===== */}
      <GlowCard glowColor="purple-500/20" className="overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
        <div className="relative flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-600/20 to-purple-400/10 border border-purple-500/30 flex items-center justify-center">
                <Brain className="w-6 h-6 text-purple-400" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white tracking-wide flex items-center gap-2">
                  Cognitive Mirror & Metacognitive Reflection
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 animate-pulse flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                    LIVE
                  </span>
                </h2>
                <p className="text-xs text-[#8D9AAA]">Real-time cognitive state based on actual system data</p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            <div className="px-4 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-center min-w-[80px]">
              <span className="text-[9px] uppercase font-bold text-[#5F6B78] block">Knowledge</span>
              <span className="text-lg font-black text-purple-300">{metrics?.knowledge?.total_items || 0}</span>
            </div>
            <div className="px-4 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-center min-w-[80px]">
              <span className="text-[9px] uppercase font-bold text-[#5F6B78] block">Health</span>
              <span className="text-lg font-black" style={{ color: healthColor }}>
                {metrics?.system?.health_score || 0}%
              </span>
            </div>
            <button
              onClick={fetchAllData}
              disabled={animating}
              className="p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] hover:border-purple-500 text-[#8D9AAA] hover:text-white transition-all disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${animating ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>

        {/* Mini Status Bar */}
        <div className="mt-4 pt-4 border-t border-[#26313D]/50 flex flex-wrap items-center gap-4 text-[10px] text-[#5F6B78]">
          <span className="flex items-center gap-1.5">
            <Signal className="w-3 h-3 text-emerald-400" />
            <span className="text-emerald-400">Live</span>
          </span>
          <span className="w-px h-4 bg-[#26313D]" />
          <span className="flex items-center gap-1.5">
            <Clock className="w-3 h-3" />
            {lastUpdate ? new Date(lastUpdate).toLocaleTimeString() : '--:--:--'}
          </span>
          <span className="w-px h-4 bg-[#26313D]" />
          <span className="flex items-center gap-1.5">
            <Server className="w-3 h-3" />
            {metrics?.websocket?.active_channels || 0} channels
          </span>
          <span className="w-px h-4 bg-[#26313D]" />
          <span className={`flex items-center gap-1.5 ${metrics?.websocket?.connected ? 'text-emerald-400' : 'text-rose-400'}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${metrics?.websocket?.connected ? 'bg-emerald-400' : 'bg-rose-400'} animate-pulse`} />
            {metrics?.websocket?.connected ? 'Connected' : 'Offline'}
          </span>
        </div>
      </GlowCard>

      {/* ===== 5 METRICS GRID ===== */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {cognitiveMetrics.map((m) => (
          <GlowCard key={m.label} glowColor="purple-500/10" className="p-4">
            <div className="flex flex-col items-center">
              <AnimatedCircularProgress
                value={m.value}
                label={m.label}
                icon={m.icon}
                color={m.color}
                sublabel={m.sublabel}
                size="md"
              />
            </div>
          </GlowCard>
        ))}
      </div>

      {/* ===== COGNITIVE NARRATIVE + QUICK STATS ===== */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Narrative */}
        <GlowCard glowColor="purple-500/10" className="lg:col-span-2">
          <div className="flex items-center gap-2 pb-3 border-b border-[#26313D]/50">
            <Brain className="w-4 h-4 text-purple-400" />
            <h3 className="text-sm font-bold text-white tracking-wide">Cognitive Narrative</h3>
            <span className="text-[9px] text-[#5F6B78] ml-auto">
              {lastUpdate ? new Date(lastUpdate).toLocaleTimeString() : ''}
            </span>
          </div>

          <div className="mt-3 space-y-2">
            <div className="flex items-start gap-2 p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <span className="text-lg">{healthEmoji}</span>
              <div>
                <p className="text-xs text-[#E8EDF2] leading-relaxed">{narrative || 'System is initializing...'}</p>
                <div className="flex flex-wrap gap-4 mt-2 pt-2 border-t border-[#26313D]/30">
                  <span className="text-[10px] text-[#8D9AAA]">📊 <span className="text-white font-semibold">{metrics?.knowledge?.total_items || 0}</span> items</span>
                  <span className="text-[10px] text-[#8D9AAA]">📁 <span className="text-white font-semibold">{metrics?.knowledge?.categories || 0}</span> categories</span>
                  <span className="text-[10px] text-[#8D9AAA]">🤖 <span className="text-white font-semibold">{metrics?.knowledge?.ai_enhanced || 0}</span> AI</span>
                  <span className="text-[10px] text-[#8D9AAA]">⏰ <span className="text-white font-semibold">{metrics?.system?.uptime_hours || 0}h</span> uptime</span>
                  <span className="text-[10px] text-[#8D9AAA]">🎯 <span className="text-white font-semibold">{metrics?.knowledge?.avg_confidence || 0}%</span> confidence</span>
                </div>
              </div>
            </div>
          </div>
        </GlowCard>

        {/* Quick Stats Cards */}
        <div className="space-y-3">
          <GlowCard glowColor="emerald-500/10" className="p-4">
            <div className="flex items-center justify-between">
              <span className="text-xs text-[#8D9AAA]">Knowledge Items</span>
              <span className="text-2xl font-black text-white">{metrics?.knowledge?.total_items || 0}</span>
            </div>
            <div className="flex items-center justify-between mt-1">
              <span className="text-[10px] text-[#5F6B78]">Categories</span>
              <span className="text-sm font-bold text-purple-400">{metrics?.knowledge?.categories || 0}</span>
            </div>
            <div className="flex items-center justify-between mt-1">
              <span className="text-[10px] text-[#5F6B78]">AI Enhanced</span>
              <span className="text-sm font-bold text-blue-400">{metrics?.knowledge?.ai_enhanced || 0}</span>
            </div>
          </GlowCard>

          <GlowCard glowColor="amber-500/10" className="p-4">
            <div className="flex items-center justify-between">
              <span className="text-xs text-[#8D9AAA]">Health Score</span>
              <span className="text-2xl font-black" style={{ color: healthColor }}>
                {metrics?.system?.health_score || 0}%
              </span>
            </div>
            <div className="w-full h-1.5 rounded-full bg-[#1A2530] mt-2 overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-1000"
                style={{ width: `${Math.min(metrics?.system?.health_score || 0, 100)}%`, backgroundColor: healthColor }}
              />
            </div>
            <div className="flex items-center justify-between mt-1.5 text-[10px] text-[#5F6B78]">
              <span>CPU: {metrics?.system?.cpu || 0}%</span>
              <span>RAM: {metrics?.system?.ram_percent || 0}%</span>
              <span>Uptime: {metrics?.system?.uptime_hours || 0}h</span>
            </div>
          </GlowCard>
        </div>
      </div>

      {/* ===== NEURAL REFLECTIONS ===== */}
      <GlowCard glowColor="purple-500/10">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/50">
          <div className="flex items-center gap-2">
            <Heart className="w-4 h-4 text-rose-400" />
            <h3 className="text-sm font-bold text-white tracking-wide">Neural Reflections</h3>
            <span className="text-[9px] px-2 py-0.5 rounded-full bg-[#1A2530] text-[#5F6B78] border border-[#26313D]">
              {reflections.length}
            </span>
          </div>
          <span className="text-[9px] text-[#5F6B78]">Real-time system insights</span>
        </div>

        <div className="mt-3 space-y-2 max-h-[300px] overflow-y-auto scrollbar-thin scrollbar-thumb-[#26313D] scrollbar-track-transparent">
          {reflections.length === 0 ? (
            <div className="p-6 text-center text-[#5F6B78] text-xs border border-dashed border-[#26313D] rounded-xl">
              <span className="text-2xl block mb-2">🔮</span>
              No reflections yet. System is still observing...
            </div>
          ) : (
            reflections.map((ref, idx) => (
              <div
                key={idx}
                className={`p-3.5 rounded-xl bg-[#1A2530] border transition-all duration-300 hover:border-purple-500/50 hover:bg-[#1F2A38] group ${
                  ref.importance === 'high'
                    ? 'border-purple-500/30'
                    : ref.importance === 'medium'
                    ? 'border-blue-500/20'
                    : 'border-[#26313D]'
                }`}
              >
                <div className="flex items-start gap-3">
                  <span className="text-base shrink-0">{ref.icon}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-[#E8EDF2] leading-relaxed">{ref.content}</p>
                  </div>
                  {ref.importance === 'high' && (
                    <span className="text-[8px] px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-400 border border-purple-500/20 shrink-0 font-semibold">
                      IMPORTANT
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </GlowCard>

      {/* ===== SYSTEM DETAILS ===== */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <GlowCard glowColor="cyan-500/10">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/50">
            <h4 className="text-xs font-bold text-[#8D9AAA] uppercase tracking-wider flex items-center gap-2">
              <CpuIcon className="w-4 h-4" /> System Resources
            </h4>
            <button
              onClick={() => setExpandedSections(prev => ({ ...prev, system: !prev.system }))}
              className="text-[#5F6B78] hover:text-white transition-colors"
            >
              {expandedSections.system ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
          </div>

          {expandedSections.system && (
            <div className="mt-3 space-y-3">
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D]">
                <span className="text-xs text-[#8D9AAA]">CPU Usage</span>
                <div className="flex items-center gap-3">
                  <div className="w-24 h-1.5 rounded-full bg-[#1A2530] overflow-hidden">
                    <div className="h-full rounded-full bg-blue-500 transition-all duration-500" style={{ width: `${metrics?.system?.cpu || 0}%` }} />
                  </div>
                  <span className="text-xs font-mono text-white">{metrics?.system?.cpu || 0}%</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D]">
                <span className="text-xs text-[#8D9AAA]">RAM Usage</span>
                <div className="flex items-center gap-3">
                  <div className="w-24 h-1.5 rounded-full bg-[#1A2530] overflow-hidden">
                    <div className="h-full rounded-full bg-purple-500 transition-all duration-500" style={{ width: `${metrics?.system?.ram_percent || 0}%` }} />
                  </div>
                  <span className="text-xs font-mono text-white">{metrics?.system?.ram_percent || 0}%</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D]">
                <span className="text-xs text-[#8D9AAA]">Disk Usage</span>
                <div className="flex items-center gap-3">
                  <div className="w-24 h-1.5 rounded-full bg-[#1A2530] overflow-hidden">
                    <div className="h-full rounded-full bg-amber-500 transition-all duration-500" style={{ width: `${metrics?.system?.disk_percent || 0}%` }} />
                  </div>
                  <span className="text-xs font-mono text-white">{metrics?.system?.disk_percent || 0}%</span>
                </div>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D]">
                <span className="text-xs text-[#8D9AAA]">Uptime</span>
                <span className="text-xs font-mono text-white">
                  {metrics?.system?.uptime_days || 0}d {metrics?.system?.uptime_hours || 0}h
                </span>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D]">
                <span className="text-xs text-[#8D9AAA]">Health Score</span>
                <span className="text-xs font-mono font-bold" style={{ color: healthColor }}>
                  {metrics?.system?.health_score || 0}%
                </span>
              </div>
            </div>
          )}
        </GlowCard>

        <GlowCard glowColor="amber-500/10">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/50">
            <h4 className="text-xs font-bold text-[#8D9AAA] uppercase tracking-wider flex items-center gap-2">
              <Layers className="w-4 h-4" /> Learning Status
            </h4>
            <button
              onClick={() => setExpandedSections(prev => ({ ...prev, learning: !prev.learning }))}
              className="text-[#5F6B78] hover:text-white transition-colors"
            >
              {expandedSections.learning ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
          </div>

          {expandedSections.learning && (
            <div className="mt-3 space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-center">
                  <span className="text-[10px] text-[#5F6B78] block">Active Modules</span>
                  <span className="text-xl font-black text-white">{metrics?.learning?.active_modules || 0}</span>
                  <span className="text-[10px] text-[#5F6B78] block">/ {metrics?.learning?.total_modules || 0}</span>
                </div>
                <div className="p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-center">
                  <span className="text-[10px] text-[#5F6B78] block">Learning Cycles</span>
                  <span className="text-xl font-black text-purple-400">{metrics?.learning?.learning_cycles || 0}</span>
                </div>
                <div className="p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-center">
                  <span className="text-[10px] text-[#5F6B78] block">Accuracy</span>
                  <span className="text-xl font-black text-blue-400">{metrics?.learning?.accuracy || 0}%</span>
                </div>
                <div className="p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-center">
                  <span className="text-[10px] text-[#5F6B78] block">Curiosity</span>
                  <span className="text-xl font-black text-amber-400">{(metrics?.learning?.curiosity_level || 0) * 100}%</span>
                </div>
              </div>
            </div>
          )}
        </GlowCard>
      </div>

      {/* ===== ADVANCED METRICS (Hidden by default) ===== */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <GlowCard glowColor="purple-500/5" className="p-3">
          <div className="flex items-center gap-2 text-[10px] text-[#5F6B78]">
            <Database className="w-3 h-3" />
            <span>Memory Items</span>
            <span className="ml-auto text-white font-bold">{metrics?.memory?.total_items || 0}</span>
          </div>
        </GlowCard>
        <GlowCard glowColor="purple-500/5" className="p-3">
          <div className="flex items-center gap-2 text-[10px] text-[#5F6B78]">
            <Target className="w-3 h-3" />
            <span>Patterns Detected</span>
            <span className="ml-auto text-white font-bold">{metrics?.pattern?.detected || 0}</span>
          </div>
        </GlowCard>
        <GlowCard glowColor="purple-500/5" className="p-3">
          <div className="flex items-center gap-2 text-[10px] text-[#5F6B78]">
            <TrendingUp className="w-3 h-3" />
            <span>Win Rate</span>
            <span className="ml-auto text-white font-bold">{metrics?.trading?.win_rate || 0}%</span>
          </div>
        </GlowCard>
      </div>

      {/* ===== FOOTER ===== */}
      <div className="text-[9px] text-[#5F6B78] text-center py-3 border-t border-[#26313D]/30 flex flex-wrap items-center justify-center gap-3">
        <span className="flex items-center gap-1">🧠 Cognitive Mirror v3.0</span>
        <span className="w-px h-3 bg-[#26313D]" />
        <span className="flex items-center gap-1">📊 Real data from {metrics?.websocket?.active_channels || 0} channels</span>
        <span className="w-px h-3 bg-[#26313D]" />
        <span className={`flex items-center gap-1 ${metrics?.websocket?.connected ? 'text-emerald-400' : 'text-rose-400'}`}>
          <span className={`w-1.5 h-1.5 rounded-full ${metrics?.websocket?.connected ? 'bg-emerald-400' : 'bg-rose-400'} animate-pulse`} />
          {metrics?.websocket?.connected ? 'LIVE' : 'OFFLINE'}
        </span>
        <span className="w-px h-3 bg-[#26313D]" />
        <span className="flex items-center gap-1">🔄 Auto-refresh every 30s</span>
      </div>
    </div>
  );
};

export default ReflectionView;
