// src/components/LearningView.tsx
// INKSIDE DIGITAL - LEARNING VIEW v4.2
// FIX: AUTO-REFRESH SILENT DI BACKGROUND
// MANUAL REFRESH SMOOTH DENGAN INDIKATOR
// TANPA TOMBOL ON/OFF

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Brain,
  RefreshCw,
  Layers,
  CheckCircle2,
  Sparkles,
  Target,
  Sliders,
  Database,
  ShieldCheck,
  Compass,
  Share2,
  Wifi,
  WifiOff,
  Loader2,
  AlertCircle,
  Plus,
  Search,
  Download,
  Zap,
  X,
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface Module {
  name: string;
  title: string;
  version: string;
  priority: number;
  status: 'ONLINE' | 'OFFLINE' | 'DEGRADED' | 'STARTING' | 'STOPPING';
  role: string;
  online: boolean;
  uptime?: number;
  health_score?: number;
}

interface AdaptiveEntry {
  key: string;
  domain: string;
  weight: number;
  confidence: number;
  reliability: number;
  successRate: number;
  attempts: number;
  trend?: 'up' | 'down' | 'stable';
}

interface CuriosityQuestion {
  id: string;
  question: string;
  domain: string;
  area: string;
  priority: number;
  status: 'UNRESOLVED' | 'INVESTIGATING' | 'RESOLVED' | 'ARCHIVED';
  answer?: string;
  created_at?: string;
}

interface Goal {
  id: string;
  title: string;
  priority: 'CRITICAL' | 'HIGH' | 'NORMAL' | 'LOW';
  progress: number;
  status: 'ACTIVE' | 'COMPLETED' | 'PAUSED' | 'ARCHIVED';
  objective: string;
  created_at?: string;
  deadline?: string;
  milestones?: Array<{ title: string; completed: boolean }>;
  blockers?: string[];
}

interface ExperienceStats {
  sensory_buffer: number;
  short_term: number;
  working_memory: number;
  permanent: number;
  total: number;
  memory_growth_rate?: number;
  consolidation_rate?: number;
  last_consolidation?: string;
}

interface KnowledgeGraph {
  concepts: Array<{ id: string; name: string; weight: number; frequency?: number }>;
  relations: Array<{ source: string; target: string; type: string; weight: number }>;
  clustering?: Array<{ name: string; members: string[] }>;
}

interface EvaluatorStats {
  total_evaluations: number;
  successful_changes: number;
  active_plans: number;
  accuracy: number;
  precision?: number;
  recall?: number;
  f1_score?: number;
  last_evaluation?: string;
}

interface LearningStats {
  cycleCount: number;
  learningActive: boolean;
  learningRate: number;
  decayRate: number;
  circuitBreakers: number;
  modulesCount: number;
  active_learning_sessions: number;
}

// ============================================================
// SKELETON LOADING COMPONENTS
// ============================================================

const SkeletonMetric: React.FC = () => (
  <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] animate-pulse">
    <div className="h-3 bg-[#26313D] rounded w-1/2"></div>
    <div className="mt-2 h-7 bg-[#26313D] rounded w-1/3"></div>
    <div className="mt-1 h-3 bg-[#26313D] rounded w-1/4"></div>
  </div>
);

const SkeletonModule: React.FC = () => (
  <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] animate-pulse">
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="w-3.5 h-3.5 bg-[#26313D] rounded-full"></div>
        <div className="h-4 bg-[#26313D] rounded w-24"></div>
      </div>
      <div className="h-5 bg-[#26313D] rounded w-12"></div>
    </div>
    <div className="mt-2 h-3 bg-[#26313D] rounded w-32"></div>
    <div className="mt-2 h-1.5 bg-[#26313D] rounded w-full"></div>
  </div>
);

// ============================================================
// MAIN COMPONENT
// ============================================================

export const LearningView: React.FC = () => {
  // ===== STATE =====
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [wsConnected, setWsConnected] = useState(false);
  
  // Data states - retain old data during refresh
  const [stats, setStats] = useState<LearningStats | null>(null);
  const [modules, setModules] = useState<Module[]>([]);
  const [adaptiveEntries, setAdaptiveEntries] = useState<AdaptiveEntry[]>([]);
  const [questions, setQuestions] = useState<CuriosityQuestion[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [experienceStats, setExperienceStats] = useState<ExperienceStats | null>(null);
  const [knowledgeGraph, setKnowledgeGraph] = useState<KnowledgeGraph | null>(null);
  const [evaluatorStats, setEvaluatorStats] = useState<EvaluatorStats | null>(null);
  
  // UI states
  const [activeTab, setActiveTab] = useState('overview');
  const [searchFilter, setSearchFilter] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('All');
  const [selectedPriority, setSelectedPriority] = useState('All');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [newQuestion, setNewQuestion] = useState('');
  const [scenarioInput, setScenarioInput] = useState(
    'BTC price spikes +5% on breakout with high volume expansion'
  );
  const [simulationResult, setSimulationResult] = useState<any>(null);
  const [isSimulating, setIsSimulating] = useState(false);
  
  // ===== REFS =====
  const refreshTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const apiKey = localStorage.getItem('apiKey') || '';
  const API_BASE = import.meta.env.VITE_API_URL || 'http://45.41.204.21';

  // ===== API HELPER =====
  const fetchWithAuth = useCallback(async (endpoint: string) => {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'X-API-Key': apiKey }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }, [API_BASE, apiKey]);

  // ===== FETCH ALL DATA (HANYA UNTUK FIRST LOAD) =====
  const initialLoad = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [
        statsData,
        modulesData,
        adaptiveData,
        questionsData,
        goalsData,
        expData,
        graphData,
        evalData
      ] = await Promise.all([
        fetchWithAuth('/api/learning/stats'),
        fetchWithAuth('/api/modules/list'),
        fetchWithAuth('/api/learning/adaptive'),
        fetchWithAuth('/api/learning/curiosity'),
        fetchWithAuth('/api/learning/goals'),
        fetchWithAuth('/api/learning/experience'),
        fetchWithAuth('/api/learning/graph'),
        fetchWithAuth('/api/learning/evaluator'),
      ]);

      if (statsData) setStats(statsData);
      if (modulesData?.modules) setModules(modulesData.modules);
      if (adaptiveData?.entries) setAdaptiveEntries(adaptiveData.entries);
      if (questionsData?.questions) setQuestions(questionsData.questions);
      if (goalsData?.goals) setGoals(goalsData.goals);
      if (expData) setExperienceStats(expData);
      if (graphData) setKnowledgeGraph(graphData);
      if (evalData) setEvaluatorStats(evalData);
      
      setLastUpdate(new Date());

    } catch (err) {
      console.error('Failed to load learning data:', err);
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  }, [fetchWithAuth]);

  // ===== MANUAL REFRESH (SMOOTH, DENGAN INDIKATOR) =====
  const manualRefresh = useCallback(async () => {
    try {
      setIsRefreshing(true);
      setError(null);

      const [
        statsData,
        modulesData,
        adaptiveData,
        questionsData,
        goalsData,
        expData,
        graphData,
        evalData
      ] = await Promise.all([
        fetchWithAuth('/api/learning/stats'),
        fetchWithAuth('/api/modules/list'),
        fetchWithAuth('/api/learning/adaptive'),
        fetchWithAuth('/api/learning/curiosity'),
        fetchWithAuth('/api/learning/goals'),
        fetchWithAuth('/api/learning/experience'),
        fetchWithAuth('/api/learning/graph'),
        fetchWithAuth('/api/learning/evaluator'),
      ]);

      if (statsData) setStats(statsData);
      if (modulesData?.modules) setModules(modulesData.modules);
      if (adaptiveData?.entries) setAdaptiveEntries(adaptiveData.entries);
      if (questionsData?.questions) setQuestions(questionsData.questions);
      if (goalsData?.goals) setGoals(goalsData.goals);
      if (expData) setExperienceStats(expData);
      if (graphData) setKnowledgeGraph(graphData);
      if (evalData) setEvaluatorStats(evalData);
      
      setLastUpdate(new Date());

    } catch (err) {
      console.error('Manual refresh failed:', err);
      setError(err instanceof Error ? err.message : 'Refresh failed');
    } finally {
      setTimeout(() => setIsRefreshing(false), 300);
    }
  }, [fetchWithAuth]);

  // ===== SILENT REFRESH (BACKGROUND, TANPA INDIKATOR) =====
  const silentRefresh = useCallback(async () => {
    try {
      // ✅ Tidak ada isRefreshing, tidak ada loading
      const [
        statsData,
        modulesData,
        adaptiveData,
        questionsData,
        goalsData,
        expData,
        graphData,
        evalData
      ] = await Promise.all([
        fetchWithAuth('/api/learning/stats'),
        fetchWithAuth('/api/modules/list'),
        fetchWithAuth('/api/learning/adaptive'),
        fetchWithAuth('/api/learning/curiosity'),
        fetchWithAuth('/api/learning/goals'),
        fetchWithAuth('/api/learning/experience'),
        fetchWithAuth('/api/learning/graph'),
        fetchWithAuth('/api/learning/evaluator'),
      ]);

      if (statsData) setStats(statsData);
      if (modulesData?.modules) setModules(modulesData.modules);
      if (adaptiveData?.entries) setAdaptiveEntries(adaptiveData.entries);
      if (questionsData?.questions) setQuestions(questionsData.questions);
      if (goalsData?.goals) setGoals(goalsData.goals);
      if (expData) setExperienceStats(expData);
      if (graphData) setKnowledgeGraph(graphData);
      if (evalData) setEvaluatorStats(evalData);
      
      setLastUpdate(new Date());

    } catch (err) {
      // Silent fail - tidak tampilkan error ke user
      console.debug('Background refresh failed:', err);
    }
  }, [fetchWithAuth]);

  // ===== HANDLE MANUAL REFRESH WITH DEBOUNCE =====
  const handleRefresh = useCallback(() => {
    if (refreshTimeoutRef.current) {
      clearTimeout(refreshTimeoutRef.current);
    }
    refreshTimeoutRef.current = setTimeout(() => {
      manualRefresh();
    }, 300);
  }, [manualRefresh]);

  // ===== WEBSOCKET =====
  useEffect(() => {
    try {
      const socket = new WebSocket(`${API_BASE.replace('http', 'ws')}/socket.io/?EIO=4&transport=websocket`);
      socket.onopen = () => setWsConnected(true);
      socket.onclose = () => setWsConnected(false);
      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data?.payload?.type === 'learning_update') {
            const payload = data.payload;
            if (payload.stats) setStats(prev => ({ ...prev, ...payload.stats }));
            if (payload.modules) setModules(payload.modules);
            if (payload.adaptive) setAdaptiveEntries(payload.adaptive);
            setLastUpdate(new Date());
          }
        } catch (e) {}
      };
      return () => { if (socket.readyState === WebSocket.OPEN) socket.close(); };
    } catch (e) {}
  }, [API_BASE]);

  // ===== INITIAL LOAD + AUTO-REFRESH SILENT =====
  useEffect(() => {
    // ✅ First load
    initialLoad();
    
    // ✅ Auto-refresh di background setiap 30 detik
    const interval = setInterval(() => {
      silentRefresh(); // ✅ Silent, tanpa indicator
    }, 30000);
    
    return () => {
      clearInterval(interval);
      if (refreshTimeoutRef.current) clearTimeout(refreshTimeoutRef.current);
    };
  }, []); // ✅ Kosongkan dependency

  // ============================================================
  // RENDER HELPERS
  // ============================================================

  const StatusBadge = ({ status }: { status: string }) => {
    const colors: Record<string, string> = {
      ONLINE: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
      OFFLINE: 'bg-rose-500/20 text-rose-400 border-rose-500/20',
      DEGRADED: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
      ACTIVE: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
      COMPLETED: 'bg-blue-500/20 text-blue-400 border-blue-500/20',
      PAUSED: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
      ARCHIVED: 'bg-gray-500/20 text-gray-400 border-gray-500/20',
      UNRESOLVED: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
      INVESTIGATING: 'bg-blue-500/20 text-blue-400 border-blue-500/20',
      RESOLVED: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
      CRITICAL: 'bg-rose-500/20 text-rose-400 border-rose-500/20',
      HIGH: 'bg-orange-500/20 text-orange-400 border-orange-500/20',
      NORMAL: 'bg-blue-500/20 text-blue-400 border-blue-500/20',
      LOW: 'bg-gray-500/20 text-gray-400 border-gray-500/20',
    };
    return (
      <span className={`text-[9px] font-bold px-2 py-0.5 rounded border ${colors[status] || 'bg-gray-500/20 text-gray-400'}`}>
        {status}
      </span>
    );
  };

  const ProgressBar = ({ value, color = 'emerald' }: { value: number; color?: string }) => {
    const colors: Record<string, string> = {
      emerald: 'bg-emerald-500',
      blue: 'bg-blue-500',
      purple: 'bg-purple-500',
      amber: 'bg-amber-500',
      rose: 'bg-rose-500',
      cyan: 'bg-cyan-500',
    };
    const percent = Math.min(100, Math.max(0, value));
    return (
      <div className="w-full bg-[#0B0F14] h-1.5 rounded-full overflow-hidden">
        <div className={`${colors[color] || colors.emerald} h-full transition-all duration-700 ease-in-out`} style={{ width: `${percent}%` }} />
      </div>
    );
  };

  const MetricCard = ({ label, value, icon: Icon, color = 'emerald', sub, progress }: any) => {
    const colors: Record<string, string> = {
      emerald: 'text-emerald-400 bg-emerald-600/20 border-emerald-500/30',
      blue: 'text-blue-400 bg-blue-600/20 border-blue-500/30',
      purple: 'text-purple-400 bg-purple-600/20 border-purple-500/30',
      cyan: 'text-cyan-400 bg-cyan-600/20 border-cyan-500/30',
      amber: 'text-amber-400 bg-amber-600/20 border-amber-500/30',
      rose: 'text-rose-400 bg-rose-600/20 border-rose-500/30',
    };
    return (
      <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-emerald-500/30 transition-all duration-300">
        <div className="flex items-center justify-between">
          <div className="text-[10px] uppercase font-bold text-[#8D9AAA]">{label}</div>
          <div className={`w-6 h-6 rounded-lg ${colors[color] || colors.emerald} flex items-center justify-center`}>
            <Icon className="w-3.5 h-3.5" />
          </div>
        </div>
        <div className="text-xl font-black text-white font-mono mt-1 transition-all duration-300">
          {value}
        </div>
        {sub && <div className="text-[10px] text-[#5F6B78] mt-0.5">{sub}</div>}
        {progress !== undefined && (
          <div className="mt-2">
            <ProgressBar value={progress} color={color} />
          </div>
        )}
      </div>
    );
  };

  // ============================================================
  // LOADING STATE (First Load Only)
  // ============================================================

  if (loading && !stats && modules.length === 0) {
    return (
      <div className="space-y-6 pb-12">
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] animate-pulse">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#26313D]"></div>
            <div>
              <div className="h-6 bg-[#26313D] rounded w-48"></div>
              <div className="mt-1 h-4 bg-[#26313D] rounded w-72"></div>
            </div>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5">
          {[1, 2, 3, 4].map(i => <SkeletonMetric key={i} />)}
        </div>
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <div className="h-5 bg-[#26313D] rounded w-32"></div>
            <div className="h-4 bg-[#26313D] rounded w-20"></div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5 mt-4">
            {[1, 2, 3, 4, 5, 6].map(i => <SkeletonModule key={i} />)}
          </div>
        </div>
      </div>
    );
  }

  // ============================================================
  // MAIN RENDER
  // ============================================================

  return (
    <div className="space-y-6 pb-12">
      {/* ============================================================
      TOP BANNER - SMOOTH MANUAL REFRESH
      ============================================================ */}
      <div className={`p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg transition-all duration-300 ${
        isRefreshing ? 'opacity-70 scale-[0.99]' : 'opacity-100 scale-100'
      }`}>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide flex items-center gap-2">
              Autonomous Intelligence Learning Suite v4.2
              {wsConnected ? (
                <Wifi className="w-4 h-4 text-emerald-400 animate-pulse" />
              ) : (
                <WifiOff className="w-4 h-4 text-amber-400" />
              )}
            </h2>
            <p className="text-xs text-[#8D9AAA] flex items-center gap-2 flex-wrap">
              Real-time Learning Analytics · {modules.length} Modules · 
              Last updated: {lastUpdate.toLocaleTimeString()}
              {isRefreshing && (
                <span className="text-emerald-400 flex items-center gap-1">
                  <Loader2 className="w-3 h-3 animate-spin" />
                  refreshing...
                </span>
              )}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-[#8D9AAA]">Learning:</span>
            <span className={`text-xs font-mono font-bold px-3 py-1 rounded-lg transition-all duration-500 ${
              stats?.learningActive || stats?.cycleCount > 0
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 animate-pulse'
                : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
            }`}>
              {stats?.learningActive || stats?.cycleCount > 0 ? 'AUTONOMOUS ACTIVE' : 'IDLE'}
            </span>
          </div>

          <div className="flex items-center gap-1">
            {/* ✅ TOMBOL REFRESH - MANUAL SAJA */}
            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className={`p-1.5 rounded-lg transition-all duration-300 ${
                isRefreshing 
                  ? 'bg-[#26313D] text-emerald-400 cursor-not-allowed' 
                  : 'bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white'
              }`}
              title="Refresh data"
            >
              <RefreshCw className={`w-4 h-4 transition-all duration-500 ${
                isRefreshing ? 'animate-spin text-emerald-400' : ''
              }`} />
            </button>
            <button
              onClick={() => {/* Export logic */}}
              className="p-1.5 rounded-lg bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white transition-colors"
              title="Export data"
            >
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* ============================================================
      ERROR DISPLAY
      ============================================================ */}
      {error && (
        <div className={`p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center gap-2 text-rose-400 text-xs transition-all duration-300 ${
          isRefreshing ? 'opacity-50' : 'opacity-100'
        }`}>
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
          <button 
            onClick={() => setError(null)}
            className="ml-auto text-rose-400/70 hover:text-rose-400"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* ============================================================
      METRICS ROW
      ============================================================ */}
      <div className={`grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3.5 transition-all duration-500 ${
        isRefreshing ? 'opacity-60' : 'opacity-100'
      }`}>
        <MetricCard
          label="Learning Cycles"
          value={stats?.cycleCount ?? '...'}
          icon={ActivityIcon}
          color="emerald"
          progress={stats?.cycleCount ? stats.cycleCount % 100 : 0}
        />
        <MetricCard
          label="Modules"
          value={modules.length}
          icon={Layers}
          color="blue"
          sub={`${modules.filter(m => m.status === 'ONLINE').length} online`}
        />
        <MetricCard
          label="Adaptive Weights"
          value={adaptiveEntries.length}
          icon={Sliders}
          color="purple"
        />
        <MetricCard
          label="Questions"
          value={questions.length}
          icon={Compass}
          color="cyan"
          sub={`${questions.filter(q => q.status === 'RESOLVED').length} resolved`}
        />
        <MetricCard
          label="Active Goals"
          value={goals.filter(g => g.status === 'ACTIVE').length}
          icon={Target}
          color="amber"
          sub={`${goals.filter(g => g.status === 'COMPLETED').length} completed`}
        />
        <MetricCard
          label="Accuracy"
          value={evaluatorStats?.accuracy ? `${evaluatorStats.accuracy}%` : '...'}
          icon={ShieldCheck}
          color="emerald"
          progress={evaluatorStats?.accuracy || 0}
        />
      </div>

      {/* ============================================================
      TABS
      ============================================================ */}
      <div className={`flex flex-wrap items-center gap-2 p-1.5 rounded-xl bg-[#131A22] border border-[#26313D] transition-all duration-300 ${
        isRefreshing ? 'opacity-60' : 'opacity-100'
      }`}>
        {[
          { id: 'overview', label: 'Overview', icon: Layers },
          { id: 'adaptive', label: 'Adaptive Weights', icon: Sliders },
          { id: 'curiosity', label: 'Curiosity', icon: Compass },
          { id: 'goals', label: 'Goals', icon: Target },
          { id: 'simulation', label: 'Simulation', icon: Sparkles },
          { id: 'experience', label: 'Experience', icon: Database },
          { id: 'knowledge_graph', label: 'Knowledge Graph', icon: Share2 },
          { id: 'evaluator', label: 'Evaluator', icon: ShieldCheck },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-bold font-mono transition-all duration-300 cursor-pointer ${
                isActive
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30 scale-105'
                  : 'text-[#8D9AAA] hover:bg-[#1A2530] hover:text-white'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* ============================================================
      SEARCH & FILTER
      ============================================================ */}
      <div className={`flex flex-wrap items-center gap-3 p-3 rounded-xl bg-[#131A22] border border-[#26313D] transition-all duration-300 ${
        isRefreshing ? 'opacity-60' : 'opacity-100'
      }`}>
        <div className="flex-1 min-w-[150px] relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#5F6B78]" />
          <input
            type="text"
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            placeholder="Search modules, questions, goals..."
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-emerald-500 transition-all"
          />
        </div>

        <select
          value={selectedStatus}
          onChange={(e) => setSelectedStatus(e.target.value)}
          className="px-2.5 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white focus:outline-none focus:border-emerald-500"
        >
          <option value="All">All Status</option>
          <option value="ONLINE">Online</option>
          <option value="OFFLINE">Offline</option>
          <option value="DEGRADED">Degraded</option>
          <option value="ACTIVE">Active</option>
          <option value="COMPLETED">Completed</option>
          <option value="UNRESOLVED">Unresolved</option>
          <option value="RESOLVED">Resolved</option>
        </select>

        <select
          value={selectedPriority}
          onChange={(e) => setSelectedPriority(e.target.value)}
          className="px-2.5 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white focus:outline-none focus:border-emerald-500"
        >
          <option value="All">All Priority</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="NORMAL">Normal</option>
          <option value="LOW">Low</option>
        </select>

        <button
          onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
          className="p-1.5 rounded-lg bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white transition-colors"
        >
          {viewMode === 'grid' ? <Layers className="w-4 h-4" /> : <ListIcon className="w-4 h-4" />}
        </button>
      </div>

      {/* ============================================================
      TAB CONTENT - OVERVIEW
      ============================================================ */}
      {activeTab === 'overview' && (
        <div className={`transition-all duration-500 ${isRefreshing ? 'opacity-60' : 'opacity-100'}`}>
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg space-y-3">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <ServerIcon className="w-4 h-4 text-emerald-400" />
                Module Status Overview
              </h3>
              <span className="text-xs text-[#5F6B78]">
                {modules.filter(m => m.status === 'ONLINE').length}/{modules.length} Online
              </span>
            </div>

            <div className={`grid ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'} gap-2.5 max-h-[400px] overflow-y-auto pr-1 transition-all duration-300`}>
              {modules.length === 0 ? (
                <div className="col-span-full text-center py-8 text-[#5F6B78] text-sm">
                  {isRefreshing ? 'Loading modules...' : 'No modules found'}
                </div>
              ) : (
                modules.map((m) => (
                  <div
                    key={m.name}
                    className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] hover:border-emerald-500/40 transition-all duration-300"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-1.5">
                          <CheckCircle2 className={`w-3.5 h-3.5 ${
                            m.status === 'ONLINE' ? 'text-emerald-400' : 
                            m.status === 'DEGRADED' ? 'text-amber-400' : 'text-rose-400'
                          }`} />
                          <span className="font-bold text-white text-xs truncate">{m.title}</span>
                        </div>
                        <div className="text-[9px] text-[#8D9AAA] mt-0.5 font-mono">
                          <code>{m.name}.py</code> · v{m.version}
                        </div>
                        <div className="text-[9px] text-[#5F6B78] mt-0.5 truncate">{m.role}</div>
                      </div>
                      <div className="text-right shrink-0 ml-2">
                        <StatusBadge status={m.status} />
                        <div className="text-[8px] text-[#5F6B78] mt-1 font-mono">Prio {m.priority}</div>
                      </div>
                    </div>
                    {m.health_score !== undefined && (
                      <div className="mt-2">
                        <div className="flex justify-between text-[8px] text-[#5F6B78]">
                          <span>Health</span>
                          <span className="text-white">{m.health_score}%</span>
                        </div>
                        <ProgressBar 
                          value={m.health_score} 
                          color={m.health_score > 80 ? 'emerald' : m.health_score > 60 ? 'amber' : 'rose'} 
                        />
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - ADAPTIVE
      ============================================================ */}
      {activeTab === 'adaptive' && (
        <div className={`transition-all duration-500 ${isRefreshing ? 'opacity-60' : 'opacity-100'}`}>
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Sliders className="w-4 h-4 text-purple-400" />
                Adaptive Weights & Confidence Calibration
              </h3>
              <span className="text-xs text-purple-400 font-mono">Dynamic Reinforcement</span>
            </div>

            {adaptiveEntries.length === 0 ? (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                {isRefreshing ? 'Loading adaptive weights...' : 'No adaptive weight data available.'}
              </div>
            ) : (
              <div className="divide-y divide-[#26313D]/40 font-mono text-xs">
                {adaptiveEntries.map((entry) => (
                  <div key={entry.key} className="py-3 flex flex-col lg:flex-row lg:items-center justify-between gap-2 transition-all duration-300 hover:bg-[#1A2530]/30 px-2 rounded-lg">
                    <div className="min-w-[200px]">
                      <div className="font-bold text-white text-sm">{entry.key.replace('_', ' ').toUpperCase()}</div>
                      <div className="text-[10px] text-[#8D9AAA] font-sans">
                        Domain: <span className="text-cyan-400">{entry.domain}</span> · {entry.attempts} attempts
                      </div>
                    </div>

                    <div className="flex flex-wrap items-center gap-4">
                      <div>
                        <div className="text-[10px] text-[#5F6B78]">Weight</div>
                        <div className="flex items-center gap-1">
                          <div className="w-20 bg-[#0B0F14] h-1.5 rounded-full overflow-hidden">
                            <div className="bg-purple-400 h-full transition-all duration-700" style={{ width: `${entry.weight}%` }} />
                          </div>
                          <span className="text-purple-400 font-bold text-sm">{entry.weight}</span>
                        </div>
                      </div>
                      <div>
                        <div className="text-[10px] text-[#5F6B78]">Confidence</div>
                        <span className="text-emerald-400 font-bold text-sm">{entry.confidence}%</span>
                      </div>
                      <div>
                        <div className="text-[10px] text-[#5F6B78]">Success Rate</div>
                        <span className="text-white font-bold text-sm">{entry.successRate}%</span>
                      </div>
                      <div className="flex items-center gap-1">
                        {entry.trend === 'up' && <TrendingUpIcon className="w-3.5 h-3.5 text-emerald-400" />}
                        {entry.trend === 'down' && <TrendingDownIcon className="w-3.5 h-3.5 text-rose-400" />}
                        {entry.trend === 'stable' && <MinusIcon className="w-3.5 h-3.5 text-[#5F6B78]" />}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - CURIOSITY
      ============================================================ */}
      {activeTab === 'curiosity' && (
        <div className={`transition-all duration-500 ${isRefreshing ? 'opacity-60' : 'opacity-100'}`}>
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Compass className="w-4 h-4 text-cyan-400" />
                Knowledge Gap Discovery & Automated Questioning
              </h3>
              <span className="text-xs text-cyan-400 font-mono">{questions.length} Questions</span>
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                value={newQuestion}
                onChange={(e) => setNewQuestion(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && console.log('Add question')}
                placeholder="Ask or inject an autonomous learning research question..."
                className="flex-1 px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-cyan-500 transition-all"
              />
              <button className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-1.5 cursor-pointer shadow-md shadow-cyan-600/20 transition-all hover:scale-105">
                <Plus className="w-3.5 h-3.5" />
                <span>Ask</span>
              </button>
            </div>

            {questions.length === 0 ? (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                {isRefreshing ? 'Loading questions...' : 'No questions found.'}
              </div>
            ) : (
              <div className="space-y-3 font-mono text-xs">
                {questions.map((q) => (
                  <div
                    key={q.id}
                    className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2 hover:border-cyan-500/30 transition-all duration-300"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <span className="font-bold text-white text-sm font-sans">{q.question}</span>
                        <div className="text-[10px] text-[#8D9AAA] mt-1">
                          Area: <code className="text-cyan-400">{q.area}</code> · Domain: {q.domain}
                          {q.created_at && ` · Created: ${new Date(q.created_at).toLocaleDateString()}`}
                        </div>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        <StatusBadge status={q.status} />
                        <span className="text-[10px] text-[#8D9AAA]">Prio {q.priority}</span>
                      </div>
                    </div>
                    {q.answer && (
                      <div className="p-2.5 rounded-lg bg-[#0B0F14] border border-emerald-500/20 text-emerald-300 text-[11px] font-sans">
                        {q.answer}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - GOALS
      ============================================================ */}
      {activeTab === 'goals' && (
        <div className={`transition-all duration-500 ${isRefreshing ? 'opacity-60' : 'opacity-100'}`}>
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Target className="w-4 h-4 text-emerald-400" />
                Autonomous Goal Manager & Milestones
              </h3>
              <span className="text-xs text-emerald-400 font-mono">
                {goals.filter(g => g.status === 'ACTIVE').length} Active · {goals.filter(g => g.status === 'COMPLETED').length} Completed
              </span>
            </div>

            {goals.length === 0 ? (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                {isRefreshing ? 'Loading goals...' : 'No goals found.'}
              </div>
            ) : (
              <div className={`grid ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-1'} gap-4`}>
                {goals.map((g) => (
                  <div key={g.id} className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-3 hover:border-emerald-500/30 transition-all duration-300">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-white text-sm font-sans">{g.title}</span>
                      <StatusBadge status={g.status} />
                    </div>

                    <div className="space-y-1">
                      <div className="flex justify-between text-[10px] font-mono text-[#8D9AAA]">
                        <span>Progress</span>
                        <span className="text-white font-bold">{g.progress}%</span>
                      </div>
                      <ProgressBar 
                        value={g.progress} 
                        color={g.progress >= 90 ? 'emerald' : g.progress >= 60 ? 'blue' : 'amber'} 
                      />
                    </div>

                    <div className="text-[10px] text-[#8D9AAA] font-sans">
                      Objective: <strong className="text-white">{g.objective}</strong>
                    </div>

                    {g.milestones && g.milestones.length > 0 && (
                      <div className="pt-2 border-t border-[#26313D]/40">
                        <div className="text-[9px] text-[#5F6B78] font-mono">Milestones:</div>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {g.milestones.map((m, i) => (
                            <span key={i} className={`text-[8px] px-1.5 py-0.5 rounded transition-all ${
                              m.completed ? 'bg-emerald-500/20 text-emerald-400' : 'bg-[#0B0F14] text-[#5F6B78]'
                            }`}>
                              {m.completed ? '✅' : '⬜'} {m.title}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {g.blockers && g.blockers.length > 0 && (
                      <div className="text-[9px] text-rose-400 font-mono">
                        ⚠️ Blockers: {g.blockers.join(', ')}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - SIMULATION
      ============================================================ */}
      {activeTab === 'simulation' && (
        <div className={`transition-all duration-500 ${isRefreshing ? 'opacity-60' : 'opacity-100'}`}>
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                Scenario Simulation & Monte Carlo Engine
              </h3>
              <span className="text-xs text-cyan-400 font-mono">Stochastic Gaussian Modeling</span>
            </div>

            <div className="space-y-3">
              <label className="text-xs text-white font-bold block">Input Market Scenario</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={scenarioInput}
                  onChange={(e) => setScenarioInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && console.log('Simulate')}
                  placeholder="Enter hypothetical market scenario..."
                  className="flex-1 px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-cyan-500 transition-all"
                />
                <button
                  onClick={() => setIsSimulating(true)}
                  disabled={isSimulating}
                  className="px-5 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs shadow-md shadow-cyan-600/30 flex items-center gap-2 cursor-pointer transition-all hover:scale-105 disabled:opacity-50"
                >
                  {isSimulating ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <Zap className="w-3.5 h-3.5" />
                  )}
                  <span>{isSimulating ? 'Simulating...' : 'Simulate'}</span>
                </button>
              </div>

              {simulationResult && (
                <div className="p-4 rounded-xl bg-[#0B0F14] border border-cyan-500/30 space-y-3 font-mono text-xs">
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                    <div className="p-2.5 bg-[#131A22] rounded-lg text-center">
                      <div className="text-[9px] text-[#5F6B78]">Direction</div>
                      <span className={`font-bold text-sm ${
                        simulationResult.direction === 'positive' ? 'text-emerald-400' : 
                        simulationResult.direction === 'negative' ? 'text-rose-400' : 'text-amber-400'
                      }`}>
                        {simulationResult.direction?.toUpperCase() || 'NEUTRAL'}
                      </span>
                    </div>
                    <div className="p-2.5 bg-[#131A22] rounded-lg text-center">
                      <div className="text-[9px] text-[#5F6B78]">Confidence</div>
                      <span className="text-white font-bold text-sm">{simulationResult.confidence || 0}%</span>
                    </div>
                    <div className="p-2.5 bg-[#131A22] rounded-lg text-center">
                      <div className="text-[9px] text-[#5F6B78]">Risk</div>
                      <span className={`font-bold text-sm ${
                        simulationResult.risk === 'LOW' ? 'text-emerald-400' : 
                        simulationResult.risk === 'HIGH' ? 'text-amber-400' : 'text-rose-400'
                      }`}>
                        {simulationResult.risk || 'UNKNOWN'}
                      </span>
                    </div>
                    <div className="p-2.5 bg-[#131A22] rounded-lg text-center">
                      <div className="text-[9px] text-[#5F6B78]">Impact</div>
                      <span className={`font-bold text-sm ${
                        simulationResult.impact === 'high' ? 'text-amber-400' : 'text-blue-400'
                      }`}>
                        {simulationResult.impact?.toUpperCase() || 'MEDIUM'}
                      </span>
                    </div>
                  </div>
                  <div className="text-[11px] text-[#8D9AAA] font-sans bg-[#131A22] p-2.5 rounded-lg border border-[#26313D]/40">
                    {simulationResult.summary || 'Simulation complete.'}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - EXPERIENCE
      ============================================================ */}
      {activeTab === 'experience' && (
        <div className={`transition-all duration-500 ${isRefreshing ? 'opacity-60' : 'opacity-100'}`}>
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Database className="w-4 h-4 text-emerald-400" />
                Experience Engine & Memory Consolidation
              </h3>
              <span className="text-xs text-emerald-400 font-mono">
                {experienceStats?.total || 0} Stored Experiences
              </span>
            </div>

            {experienceStats ? (
              <>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center transition-all hover:border-emerald-500/30">
                    <div className="text-[10px] text-[#5F6B78]">Sensory Buffer</div>
                    <div className="text-base font-bold text-white">{experienceStats.sensory_buffer}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center transition-all hover:border-emerald-500/30">
                    <div className="text-[10px] text-[#5F6B78]">Short-Term</div>
                    <div className="text-base font-bold text-white">{experienceStats.short_term}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center transition-all hover:border-emerald-500/30">
                    <div className="text-[10px] text-[#5F6B78]">Working Memory</div>
                    <div className="text-base font-bold text-emerald-400">{experienceStats.working_memory}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center transition-all hover:border-emerald-500/30">
                    <div className="text-[10px] text-[#5F6B78]">Permanent</div>
                    <div className="text-base font-bold text-purple-400">{experienceStats.permanent}</div>
                  </div>
                </div>

                {experienceStats.memory_growth_rate !== undefined && (
                  <div className="flex flex-wrap items-center gap-4 text-xs text-[#8D9AAA] font-mono">
                    <span>Growth Rate: <strong className="text-white">{experienceStats.memory_growth_rate}%</strong></span>
                    <span>Consolidation: <strong className="text-white">{experienceStats.consolidation_rate || 0}%</strong></span>
                    {experienceStats.last_consolidation && (
                      <span>Last: <strong className="text-white">{new Date(experienceStats.last_consolidation).toLocaleString()}</strong></span>
                    )}
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                {isRefreshing ? 'Loading experience data...' : 'No experience data available.'}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - KNOWLEDGE GRAPH
      ============================================================ */}
      {activeTab === 'knowledge_graph' && (
        <div className={`transition-all duration-500 ${isRefreshing ? 'opacity-60' : 'opacity-100'}`}>
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Share2 className="w-4 h-4 text-purple-400" />
                Knowledge Graph & Concept Builder
              </h3>
              <span className="text-xs text-purple-400 font-mono">
                {knowledgeGraph?.concepts?.length || 0} Concepts · {knowledgeGraph?.relations?.length || 0} Relations
              </span>
            </div>

            {knowledgeGraph && knowledgeGraph.concepts.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 font-mono text-xs">
                <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                  <div className="text-sm font-bold text-white mb-2">Key Concepts</div>
                  <div className="space-y-1">
                    {knowledgeGraph.concepts.slice(0, 10).map((c) => (
                      <div key={c.id} className="flex justify-between text-[11px] transition-all hover:bg-[#0B0F14] px-1 py-0.5 rounded">
                        <span className="text-[#8D9AAA]">{c.name}</span>
                        <span className="text-purple-400 font-bold">weight: {c.weight}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                  <div className="text-sm font-bold text-white mb-2">Relations</div>
                  <div className="space-y-1">
                    {knowledgeGraph.relations.slice(0, 10).map((r, i) => (
                      <div key={i} className="text-[11px] text-[#8D9AAA] transition-all hover:bg-[#0B0F14] px-1 py-0.5 rounded">
                        <code className="text-cyan-400">{r.source}</code>
                        <span className="text-[#5F6B78]"> --[{r.type}]--&gt; </span>
                        <code className="text-cyan-400">{r.target}</code>
                        <span className="text-purple-400"> ({r.weight})</span>
                      </div>
                    ))}
                  </div>
                </div>

                {knowledgeGraph.clustering && knowledgeGraph.clustering.length > 0 && (
                  <div className="col-span-full p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                    <div className="text-sm font-bold text-white mb-2">Clusters</div>
                    <div className="flex flex-wrap gap-2">
                      {knowledgeGraph.clustering.map((c, i) => (
                        <div key={i} className="text-[10px] px-2 py-1 rounded bg-[#0B0F14] border border-[#26313D] transition-all hover:border-purple-500/30">
                          <span className="text-amber-400 font-bold">{c.name}</span>
                          <span className="text-[#5F6B78] ml-1">({c.members.length} members)</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                {isRefreshing ? 'Loading knowledge graph...' : 'No knowledge graph data available.'}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - EVALUATOR
      ============================================================ */}
      {activeTab === 'evaluator' && (
        <div className={`transition-all duration-500 ${isRefreshing ? 'opacity-60' : 'opacity-100'}`}>
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                General Evaluator & Improvement Engine
              </h3>
              <span className="text-xs text-emerald-400 font-mono">
                Accuracy: {evaluatorStats?.accuracy || 0}%
              </span>
            </div>

            {evaluatorStats ? (
              <>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-3 font-mono text-xs">
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center transition-all hover:border-emerald-500/30">
                    <div className="text-[10px] text-[#5F6B78]">Total Evaluations</div>
                    <div className="text-base font-bold text-white">{evaluatorStats.total_evaluations}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center transition-all hover:border-emerald-500/30">
                    <div className="text-[10px] text-[#5F6B78]">Successful Changes</div>
                    <div className="text-base font-bold text-emerald-400">{evaluatorStats.successful_changes}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center transition-all hover:border-emerald-500/30">
                    <div className="text-[10px] text-[#5F6B78]">Active Plans</div>
                    <div className="text-base font-bold text-cyan-400">{evaluatorStats.active_plans}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center transition-all hover:border-emerald-500/30">
                    <div className="text-[10px] text-[#5F6B78]">Accuracy</div>
                    <div className="text-base font-bold text-emerald-400">{evaluatorStats.accuracy}%</div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-4 text-xs text-[#8D9AAA] font-mono">
                  {evaluatorStats.precision !== undefined && (
                    <span>Precision: <strong className="text-white">{evaluatorStats.precision}%</strong></span>
                  )}
                  {evaluatorStats.recall !== undefined && (
                    <span>Recall: <strong className="text-white">{evaluatorStats.recall}%</strong></span>
                  )}
                  {evaluatorStats.f1_score !== undefined && (
                    <span>F1 Score: <strong className="text-white">{evaluatorStats.f1_score}%</strong></span>
                  )}
                  {evaluatorStats.last_evaluation && (
                    <span>Last: <strong className="text-white">{new Date(evaluatorStats.last_evaluation).toLocaleString()}</strong></span>
                  )}
                </div>
              </>
            ) : (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                {isRefreshing ? 'Loading evaluator data...' : 'No evaluator data available.'}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================
      FOOTER
      ============================================================ */}
      <div className="flex items-center justify-between text-[10px] text-[#5F6B78] border-t border-[#26313D]/40 pt-4">
        <span>Last update: {lastUpdate.toLocaleString()}</span>
        <div className="flex items-center gap-2">
          {wsConnected ? (
            <Wifi className="w-3 h-3 text-emerald-400" />
          ) : (
            <WifiOff className="w-3 h-3 text-amber-400" />
          )}
          <span>Data source: REAL API · v4.2</span>
        </div>
      </div>
    </div>
  );
};

// ============================================================
// ICON COMPONENTS
// ============================================================

const ActivityIcon = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
  </svg>
);

const ServerIcon = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="4" width="18" height="6" rx="2" />
    <rect x="3" y="14" width="18" height="6" rx="2" />
    <circle cx="7" cy="7" r="1" />
    <circle cx="7" cy="17" r="1" />
  </svg>
);

const ListIcon = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="8" y1="6" x2="21" y2="6" />
    <line x1="8" y1="12" x2="21" y2="12" />
    <line x1="8" y1="18" x2="21" y2="18" />
    <line x1="3" y1="6" x2="3.01" y2="6" />
    <line x1="3" y1="12" x2="3.01" y2="12" />
    <line x1="3" y1="18" x2="3.01" y2="18" />
  </svg>
);

const MinusIcon = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const TrendingUpIcon = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
    <polyline points="17 6 23 6 23 12" />
  </svg>
);

const TrendingDownIcon = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <polyline points="23 18 13.5 8.5 8.5 13.5 1 6" />
    <polyline points="17 18 23 18 23 12" />
  </svg>
);

export default LearningView;
