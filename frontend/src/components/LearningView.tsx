// src/components/LearningView.tsx
// INKSIDE DIGITAL - LEARNING VIEW v4.0
// 100% REAL DATA - NO DUMMY

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  GraduationCap,
  Play,
  RefreshCw,
  Layers,
  CheckCircle2,
  Sparkles,
  Target,
  Search,
  Sliders,
  Database,
  ShieldCheck,
  AlertTriangle,
  Lightbulb,
  Compass,
  Share2,
  Zap,
  Send,
  Plus,
  X,
  Download,
  Filter,
  Clock,
  TrendingUp,
  TrendingDown,
  Minimize2,
  Maximize2,
  Info,
  Settings,
  BarChart3,
  Activity,
  Cpu,
  HardDrive,
  Globe,
  Server,
  Terminal,
  Code2,
  GitBranch,
  Calendar,
  Users,
  Bell,
  ChevronDown,
  ChevronRight,
  Pause,
  RotateCcw,
  Trash2,
  Edit2,
  Check,
  AlertCircle,
  Loader2,
  GripVertical,
  MoreVertical,
  Eye,
  EyeOff,
  BookOpen,
  Brain,
  Network,
  LineChart,
  PieChart,
  BarChart2,
} from 'lucide-react';

// ============================================================
// TYPES - REAL DATA STRUCTURES
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
  memory_usage?: number;
  cpu_usage?: number;
  last_heartbeat?: string;
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
  last_updated?: string;
  trend?: 'up' | 'down' | 'stable';
  historical_weights?: number[];
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
  resolved_at?: string;
  confidence?: number;
  tags?: string[];
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

interface SimulationResult {
  direction: 'positive' | 'negative' | 'neutral';
  impact: 'high' | 'medium' | 'low';
  risk: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  risk_score: number;
  confidence: number;
  probability: number;
  possible_effect: string;
  assumptions: string[];
  monte_carlo: {
    iterations: number;
    mean_confidence: number;
    percentile_5: number;
    percentile_95: number;
    distribution?: Array<{ value: number; frequency: number }>;
  };
  recommended_action?: string;
  alternative_scenarios?: Array<{ name: string; probability: number }>;
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
  total_learnings?: number;
  success_rate?: number;
  avg_confidence?: number;
  active_learning_sessions?: number;
}

// ============================================================
// API SERVICE
// ============================================================

const API_BASE = '/api';

class LearningAPI {
  private static instance: LearningAPI;
  private eventSource: EventSource | null = null;
  private listeners: Map<string, Set<Function>> = new Map();

  static getInstance(): LearningAPI {
    if (!LearningAPI.instance) {
      LearningAPI.instance = new LearningAPI();
    }
    return LearningAPI.instance;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(error.error || `HTTP ${response.status}`);
    }
    return response.json();
  }

  // ============================================================
  // LEARNING APIs
  // ============================================================

  async getStats(): Promise<LearningStats> {
    return this.request<LearningStats>('/learning/stats');
  }

  async getModules(): Promise<Module[]> {
    const data = await this.request<{ modules: Module[] }>('/modules/list');
    return data.modules;
  }

  async getAdaptiveWeights(): Promise<AdaptiveEntry[]> {
    const data = await this.request<{ entries: AdaptiveEntry[] }>('/learning/adaptive');
    return data.entries;
  }

  async getCuriosityQuestions(): Promise<CuriosityQuestion[]> {
    const data = await this.request<{ questions: CuriosityQuestion[] }>('/learning/curiosity');
    return data.questions;
  }

  async addCuriosityQuestion(question: string, domain?: string, area?: string): Promise<string> {
    const data = await this.request<{ id: string }>('/learning/curiosity', {
      method: 'POST',
      body: JSON.stringify({ question, domain, area }),
    });
    return data.id;
  }

  async getGoals(): Promise<Goal[]> {
    const data = await this.request<{ goals: Goal[] }>('/learning/goals');
    return data.goals;
  }

  async simulateScenario(scenario: string): Promise<SimulationResult> {
    return this.request<SimulationResult>('/learning/simulate', {
      method: 'POST',
      body: JSON.stringify({ scenario }),
    });
  }

  async getExperienceStats(): Promise<ExperienceStats> {
    return this.request<ExperienceStats>('/learning/experience');
  }

  async getKnowledgeGraph(): Promise<KnowledgeGraph> {
    return this.request<KnowledgeGraph>('/learning/graph');
  }

  async getEvaluatorStats(): Promise<EvaluatorStats> {
    return this.request<EvaluatorStats>('/learning/evaluator');
  }

  // ============================================================
  // WEBSOCKET / SSE
  // ============================================================

  connectSSE(onMessage: (data: any) => void): void {
    if (this.eventSource) {
      this.eventSource.close();
    }

    this.eventSource = new EventSource(`${API_BASE}/learning/stream`);
    this.eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (e) {
        console.error('SSE parse error:', e);
      }
    };
    this.eventSource.onerror = () => {
      console.warn('SSE connection error, reconnecting in 5s...');
      setTimeout(() => this.connectSSE(onMessage), 5000);
    };
  }

  disconnectSSE(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}

const api = LearningAPI.getInstance();

// ============================================================
// COMPONENT
// ============================================================

type TabType =
  | 'overview'
  | 'adaptive'
  | 'curiosity'
  | 'goals'
  | 'simulation'
  | 'experience'
  | 'knowledge_graph'
  | 'evaluator'
  | 'settings';

interface LearningViewProps {
  learningActive?: boolean;
  cycleCount?: number;
}

export const LearningView: React.FC<LearningViewProps> = () => {
  // ============================================================
  // STATE - REAL DATA
  // ============================================================
  
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set());
  
  // Data states
  const [stats, setStats] = useState<LearningStats | null>(null);
  const [modules, setModules] = useState<Module[]>([]);
  const [adaptiveEntries, setAdaptiveEntries] = useState<AdaptiveEntry[]>([]);
  const [questions, setQuestions] = useState<CuriosityQuestion[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [experienceStats, setExperienceStats] = useState<ExperienceStats | null>(null);
  const [knowledgeGraph, setKnowledgeGraph] = useState<KnowledgeGraph | null>(null);
  const [evaluatorStats, setEvaluatorStats] = useState<EvaluatorStats | null>(null);
  const [simulationResult, setSimulationResult] = useState<SimulationResult | null>(null);
  
  // UI states
  const [scenarioInput, setScenarioInput] = useState('BTC price spikes +5% on breakout with high volume expansion');
  const [isSimulating, setIsSimulating] = useState(false);
  const [newQuestionInput, setNewQuestionInput] = useState('');
  const [searchFilter, setSearchFilter] = useState('');
  const [selectedDomain, setSelectedDomain] = useState<string>('All');
  const [selectedPriority, setSelectedPriority] = useState<string>('All');
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  // Refs
  const refreshTimeoutRef = useRef<number>();
  const sseCallbackRef = useRef<(data: any) => void>();

  // ============================================================
  // DATA FETCHING
  // ============================================================

  const fetchAllData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [
        statsData,
        modulesData,
        weightsData,
        questionsData,
        goalsData,
        expData,
        graphData,
        evalData
      ] = await Promise.all([
        api.getStats(),
        api.getModules(),
        api.getAdaptiveWeights(),
        api.getCuriosityQuestions(),
        api.getGoals(),
        api.getExperienceStats(),
        api.getKnowledgeGraph(),
        api.getEvaluatorStats(),
      ]);

      setStats(statsData);
      setModules(modulesData);
      setAdaptiveEntries(weightsData);
      setQuestions(questionsData);
      setGoals(goalsData);
      setExperienceStats(expData);
      setKnowledgeGraph(graphData);
      setEvaluatorStats(evalData);
      setLastUpdate(new Date());

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch learning data');
      console.error('Learning fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // ============================================================
  // EFFECTS
  // ============================================================

  useEffect(() => {
    fetchAllData();

    // Auto-refresh every 5 seconds
    if (autoRefresh) {
      const interval = setInterval(fetchAllData, 5000);
      return () => clearInterval(interval);
    }
  }, [fetchAllData, autoRefresh]);

  // SSE Connection for real-time updates
  useEffect(() => {
    sseCallbackRef.current = (data: any) => {
      console.log('SSE Data:', data);
      // Update relevant states based on data type
      if (data.type === 'stats') setStats(data.data);
      if (data.type === 'modules') setModules(data.data);
      if (data.type === 'adaptive') setAdaptiveEntries(data.data);
      if (data.type === 'questions') setQuestions(data.data);
      if (data.type === 'goals') setGoals(data.data);
      if (data.type === 'simulation') setSimulationResult(data.data);
      setLastUpdate(new Date());
    };

    api.connectSSE((data) => {
      if (sseCallbackRef.current) {
        sseCallbackRef.current(data);
      }
    });

    return () => {
      api.disconnectSSE();
    };
  }, []);

  // ============================================================
  // HANDLERS
  // ============================================================

  const handleSimulateScenario = async () => {
    if (!scenarioInput.trim()) return;
    setIsSimulating(true);
    try {
      const result = await api.simulateScenario(scenarioInput);
      setSimulationResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Simulation failed');
    } finally {
      setIsSimulating(false);
    }
  };

  const handleAddQuestion = async () => {
    if (!newQuestionInput.trim()) return;
    try {
      const id = await api.addCuriosityQuestion(
        newQuestionInput.trim(),
        'trading',
        'custom_discovery'
      );
      // Refresh questions
      const updated = await api.getCuriosityQuestions();
      setQuestions(updated);
      setNewQuestionInput('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add question');
    }
  };

  const handleExportData = (format: 'json' | 'csv') => {
    const data = {
      stats,
      modules,
      adaptiveEntries,
      questions,
      goals,
      experienceStats,
      knowledgeGraph,
      evaluatorStats,
      timestamp: new Date().toISOString(),
    };

    if (format === 'json') {
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `learning_data_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } else {
      // CSV export
      const headers = ['Type', 'Name', 'Value', 'Confidence', 'Status', 'Updated'];
      const rows = [
        headers,
        ...modules.map(m => ['Module', m.title, m.version, '', m.status, '']),
        ...adaptiveEntries.map(e => ['Adaptive', e.key, e.weight, e.confidence, '', '']),
        ...questions.map(q => ['Question', q.question, '', '', q.status, '']),
        ...goals.map(g => ['Goal', g.title, g.progress, '', g.status, '']),
      ];
      const csv = rows.map(r => r.join(',')).join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `learning_data_${new Date().toISOString().slice(0, 10)}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const toggleCard = (id: string) => {
    const newSet = new Set(expandedCards);
    if (newSet.has(id)) newSet.delete(id);
    else newSet.add(id);
    setExpandedCards(newSet);
  };

  // ============================================================
  // FILTERING
  // ============================================================

  const filteredModules = modules.filter(m => {
    if (searchFilter && !m.title.toLowerCase().includes(searchFilter.toLowerCase())) return false;
    if (selectedStatus !== 'All' && m.status !== selectedStatus) return false;
    return true;
  });

  const filteredQuestions = questions.filter(q => {
    if (searchFilter && !q.question.toLowerCase().includes(searchFilter.toLowerCase())) return false;
    if (selectedDomain !== 'All' && q.domain !== selectedDomain) return false;
    if (selectedPriority !== 'All' && q.priority !== parseInt(selectedPriority)) return false;
    if (selectedStatus !== 'All' && q.status !== selectedStatus) return false;
    return true;
  });

  const filteredGoals = goals.filter(g => {
    if (searchFilter && !g.title.toLowerCase().includes(searchFilter.toLowerCase())) return false;
    if (selectedStatus !== 'All' && g.status !== selectedStatus) return false;
    if (selectedPriority !== 'All' && g.priority !== selectedPriority) return false;
    return true;
  });

  // ============================================================
  // RENDER HELPERS
  // ============================================================

  const StatusBadge = ({ status }: { status: string }) => {
    const colors: Record<string, string> = {
      ONLINE: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
      OFFLINE: 'bg-rose-500/20 text-rose-400 border-rose-500/20',
      DEGRADED: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
      STARTING: 'bg-blue-500/20 text-blue-400 border-blue-500/20',
      STOPPING: 'bg-orange-500/20 text-orange-400 border-orange-500/20',
      ACTIVE: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
      COMPLETED: 'bg-blue-500/20 text-blue-400 border-blue-500/20',
      PAUSED: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
      ARCHIVED: 'bg-gray-500/20 text-gray-400 border-gray-500/20',
      UNRESOLVED: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
      INVESTIGATING: 'bg-blue-500/20 text-blue-400 border-blue-500/20',
      RESOLVED: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
      LOW: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
      MODERATE: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
      HIGH: 'bg-orange-500/20 text-orange-400 border-orange-500/20',
      CRITICAL: 'bg-rose-500/20 text-rose-400 border-rose-500/20',
    };
    return (
      <span className={`text-[9px] font-bold px-2 py-0.5 rounded border ${colors[status] || 'bg-gray-500/20 text-gray-400'}`}>
        {status}
      </span>
    );
  };

  const ProgressBar = ({ value, max = 100, color = 'emerald' }: { value: number; max?: number; color?: string }) => {
    const percent = Math.min(100, (value / max) * 100);
    const colors: Record<string, string> = {
      emerald: 'bg-emerald-500',
      blue: 'bg-blue-500',
      purple: 'bg-purple-500',
      cyan: 'bg-cyan-500',
      amber: 'bg-amber-500',
      rose: 'bg-rose-500',
    };
    return (
      <div className="w-full bg-[#0B0F14] h-2 rounded-full overflow-hidden">
        <div className={`${colors[color] || colors.emerald} h-full transition-all duration-500`} style={{ width: `${percent}%` }} />
      </div>
    );
  };

  // ============================================================
  // LOADING STATE
  // ============================================================

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-emerald-400 animate-spin mx-auto" />
          <p className="text-[#8D9AAA] mt-4 text-sm">Loading learning data...</p>
        </div>
      </div>
    );
  }

  // ============================================================
  // ERROR STATE
  // ============================================================

  if (error) {
    return (
      <div className="p-6 rounded-2xl bg-[#131A22] border border-rose-500/30">
        <div className="flex items-center gap-3 text-rose-400">
          <AlertCircle className="w-5 h-5" />
          <span className="font-bold">Error loading learning data:</span>
          <span className="text-sm">{error}</span>
        </div>
        <button
          onClick={fetchAllData}
          className="mt-4 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-white text-sm flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Retry
        </button>
      </div>
    );
  }

  // ============================================================
  // MAIN RENDER
  // ============================================================

  return (
    <div id="learning-view" className="space-y-6 pb-12">
      {/* ============================================================
      TOP BANNER
      ============================================================ */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Autonomous Intelligence Learning Suite v4.0
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Real-time Learning Analytics · {modules.length} Modules · Last updated: {lastUpdate.toLocaleTimeString()}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-[#8D9AAA]">Learning:</span>
            <span
              className={`text-xs font-mono font-bold px-3 py-1 rounded-lg ${
                stats?.learningActive
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 animate-pulse'
                  : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
              }`}
            >
              {stats?.learningActive ? 'AUTONOMOUS ACTIVE' : 'IDLE'}
            </span>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`p-1.5 rounded-lg transition-colors ${
                autoRefresh ? 'bg-emerald-500/20 text-emerald-400' : 'bg-[#0B0F14] text-[#5F6B78]'
              }`}
              title={autoRefresh ? 'Auto-refresh on' : 'Auto-refresh off'}
            >
              <RefreshCw className={`w-4 h-4 ${autoRefresh ? 'animate-spin-slow' : ''}`} />
            </button>
            <button
              onClick={() => fetchAllData()}
              className="p-1.5 rounded-lg bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white transition-colors"
              title="Refresh now"
            >
              <Zap className="w-4 h-4" />
            </button>
            <button
              onClick={() => handleExportData('json')}
              className="p-1.5 rounded-lg bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white transition-colors"
              title="Export data"
            >
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* ============================================================
      NAVIGATION TABS
      ============================================================ */}
      <div className="flex flex-wrap items-center gap-2 p-1.5 rounded-xl bg-[#131A22] border border-[#26313D]">
        {[
          { id: 'overview', label: 'Overview', icon: BarChart3 },
          { id: 'adaptive', label: 'Adaptive Weights', icon: Sliders },
          { id: 'curiosity', label: 'Curiosity', icon: Compass },
          { id: 'goals', label: 'Goals', icon: Target },
          { id: 'simulation', label: 'Simulation', icon: Sparkles },
          { id: 'experience', label: 'Experience', icon: Database },
          { id: 'knowledge_graph', label: 'Knowledge Graph', icon: Share2 },
          { id: 'evaluator', label: 'Evaluator', icon: ShieldCheck },
          { id: 'settings', label: 'Settings', icon: Settings },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as TabType)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-bold font-mono transition-all cursor-pointer ${
                isActive
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'text-[#8D9AAA] hover:bg-[#1A2530] hover:text-white'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
              {isActive && (
                <span className="text-[10px] opacity-70 ml-1">
                  {tab.id === 'overview' && modules.length}
                  {tab.id === 'adaptive' && adaptiveEntries.length}
                  {tab.id === 'curiosity' && questions.length}
                  {tab.id === 'goals' && goals.length}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* ============================================================
      SEARCH & FILTER BAR
      ============================================================ */}
      <div className="flex flex-wrap items-center gap-3 p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
        <div className="flex-1 min-w-[150px] relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#5F6B78]" />
          <input
            type="text"
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            placeholder="Search modules, questions, goals..."
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-emerald-500"
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
          {viewMode === 'grid' ? <Layers className="w-4 h-4" /> : <List className="w-4 h-4" />}
        </button>
      </div>

      {/* ============================================================
      TAB CONTENT - OVERVIEW
      ============================================================ */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Quick Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3.5">
            <MetricCard
              label="Learning Cycles"
              value={`#${stats?.cycleCount || 0}`}
              icon={Activity}
              color="emerald"
              progress={(stats?.cycleCount || 0) % 100}
            />
            <MetricCard
              label="Modules"
              value={modules.length}
              icon={Layers}
              color="blue"
              sub={modules.filter(m => m.status === 'ONLINE').length + ' online'}
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
              sub={questions.filter(q => q.status === 'RESOLVED').length + ' resolved'}
            />
            <MetricCard
              label="Active Goals"
              value={goals.filter(g => g.status === 'ACTIVE').length}
              icon={Target}
              color="amber"
              sub={goals.filter(g => g.status === 'COMPLETED').length + ' completed'}
            />
            <MetricCard
              label="Accuracy"
              value={`${evaluatorStats?.accuracy || 0}%`}
              icon={ShieldCheck}
              color="emerald"
              trend={evaluatorStats?.accuracy > 80 ? 'up' : 'down'}
            />
          </div>

          {/* Module Status */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg space-y-3">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Server className="w-4 h-4 text-emerald-400" />
                Module Status Overview
              </h3>
              <span className="text-xs text-[#5F6B78]">
                {modules.filter(m => m.status === 'ONLINE').length}/{modules.length} Online
              </span>
            </div>

            <div className={`grid ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'} gap-2.5 max-h-[400px] overflow-y-auto pr-1`}>
              {filteredModules.length === 0 ? (
                <div className="col-span-full text-center py-8 text-[#5F6B78] text-sm">
                  No modules found matching filters
                </div>
              ) : (
                filteredModules.map((m) => (
                  <div
                    key={m.name}
                    className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] hover:border-emerald-500/40 transition-all"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-1.5">
                          <CheckCircle2 className={`w-3.5 h-3.5 ${m.status === 'ONLINE' ? 'text-emerald-400' : m.status === 'DEGRADED' ? 'text-amber-400' : 'text-rose-400'}`} />
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
                        <ProgressBar value={m.health_score} color={m.health_score > 80 ? 'emerald' : m.health_score > 60 ? 'amber' : 'rose'} />
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
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Sliders className="w-4 h-4 text-purple-400" />
                Adaptive Weights & Confidence Calibration
              </h3>
              <span className="text-xs text-purple-400 font-mono">Dynamic Reinforcement</span>
            </div>

            <p className="text-xs text-[#8D9AAA]">
              Weights adapt dynamically based on actual trade outcomes, reward-to-risk performance, and time-decay curves.
              {adaptiveEntries.length === 0 && ' No adaptive entries available.'}
            </p>

            {adaptiveEntries.length === 0 ? (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                No adaptive weight data available. Run some trades to generate data.
              </div>
            ) : (
              <div className="divide-y divide-[#26313D]/40 font-mono text-xs">
                {adaptiveEntries.map((entry) => (
                  <div key={entry.key} className="py-3 flex flex-col lg:flex-row lg:items-center justify-between gap-2">
                    <div className="min-w-[200px]">
                      <div className="font-bold text-white text-sm">{entry.key}</div>
                      <div className="text-[10px] text-[#8D9AAA] font-sans">
                        Domain: <span className="text-cyan-400">{entry.domain}</span> · {entry.attempts} attempts
                      </div>
                    </div>

                    <div className="flex flex-wrap items-center gap-4">
                      <div>
                        <div className="text-[10px] text-[#5F6B78]">Weight</div>
                        <div className="flex items-center gap-1">
                          <div className="w-20 bg-[#0B0F14] h-1.5 rounded-full overflow-hidden">
                            <div className="bg-purple-400 h-full" style={{ width: `${entry.weight}%` }} />
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
                        {entry.trend === 'up' && <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />}
                        {entry.trend === 'down' && <TrendingDown className="w-3.5 h-3.5 text-rose-400" />}
                        {entry.trend === 'stable' && <Minus className="w-3.5 h-3.5 text-[#5F6B78]" />}
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
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Compass className="w-4 h-4 text-cyan-400" />
                Knowledge Gap Discovery & Automated Questioning
              </h3>
              <span className="text-xs text-cyan-400 font-mono">{questions.length} Questions</span>
            </div>

            {/* Add Question */}
            <div className="flex gap-2">
              <input
                type="text"
                value={newQuestionInput}
                onChange={(e) => setNewQuestionInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddQuestion()}
                placeholder="Ask or inject an autonomous learning research question..."
                className="flex-1 px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-cyan-500"
              />
              <button
                onClick={handleAddQuestion}
                className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-1.5 cursor-pointer shadow-md shadow-cyan-600/20 disabled:opacity-50"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Ask</span>
              </button>
            </div>

            {/* Questions List */}
            {filteredQuestions.length === 0 ? (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                No questions match your filters. Add a question to get started.
              </div>
            ) : (
              <div className="space-y-3 font-mono text-xs">
                {filteredQuestions.map((q) => (
                  <div
                    key={q.id}
                    className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2 hover:border-cyan-500/30 transition-colors"
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
        <div className="space-y-6">
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

            {filteredGoals.length === 0 ? (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                No goals match your filters.
              </div>
            ) : (
              <div className={`grid ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-1'} gap-4`}>
                {filteredGoals.map((g) => (
                  <div key={g.id} className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-3 hover:border-emerald-500/30 transition-colors">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-white text-sm font-sans">{g.title}</span>
                      <StatusBadge status={g.status} />
                    </div>

                    <div className="space-y-1">
                      <div className="flex justify-between text-[10px] font-mono text-[#8D9AAA]">
                        <span>Progress</span>
                        <span className="text-white font-bold">{g.progress}%</span>
                      </div>
                      <ProgressBar value={g.progress} color={g.progress >= 90 ? 'emerald' : g.progress >= 60 ? 'blue' : 'amber'} />
                    </div>

                    <div className="text-[10px] text-[#8D9AAA] font-sans">
                      Objective: <strong className="text-white">{g.objective}</strong>
                    </div>

                    {g.milestones && g.milestones.length > 0 && (
                      <div className="pt-2 border-t border-[#26313D]/40">
                        <div className="text-[9px] text-[#5F6B78] font-mono">Milestones:</div>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {g.milestones.map((m, i) => (
                            <span key={i} className={`text-[8px] px-1.5 py-0.5 rounded ${m.completed ? 'bg-emerald-500/20 text-emerald-400' : 'bg-[#0B0F14] text-[#5F6B78]'}`}>
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
        <div className="space-y-6">
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
                  onKeyDown={(e) => e.key === 'Enter' && handleSimulateScenario()}
                  placeholder="Enter hypothetical market scenario..."
                  className="flex-1 px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-cyan-500"
                />
                <button
                  onClick={handleSimulateScenario}
                  disabled={isSimulating}
                  className="px-5 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs shadow-md shadow-cyan-600/30 flex items-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  {isSimulating ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
                  <span>{isSimulating ? 'Simulating...' : 'Simulate'}</span>
                </button>
              </div>

              {simulationResult && (
                <div className="p-4 rounded-xl bg-[#0B0F14] border border-cyan-500/30 space-y-3 font-mono text-xs">
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                    <div className="p-2.5 bg-[#131A22] rounded-lg text-center">
                      <div className="text-[9px] text-[#5F6B78]">Direction</div>
                      <span className={`font-bold text-sm ${simulationResult.direction === 'positive' ? 'text-emerald-400' : simulationResult.direction === 'negative' ? 'text-rose-400' : 'text-amber-400'}`}>
                        {simulationResult.direction.toUpperCase()}
                      </span>
                    </div>
                    <div className="p-2.5 bg-[#131A22] rounded-lg text-center">
                      <div className="text-[9px] text-[#5F6B78]">Impact</div>
                      <span className={`font-bold text-sm ${simulationResult.impact === 'high' ? 'text-amber-400' : 'text-blue-400'}`}>
                        {simulationResult.impact.toUpperCase()}
                      </span>
                    </div>
                    <div className="p-2.5 bg-[#131A22] rounded-lg text-center">
                      <div className="text-[9px] text-[#5F6B78]">Risk</div>
                      <span className={`font-bold text-sm ${simulationResult.risk === 'LOW' ? 'text-emerald-400' : simulationResult.risk === 'HIGH' ? 'text-amber-400' : 'text-rose-400'}`}>
                        {simulationResult.risk} ({simulationResult.risk_score}%)
                      </span>
                    </div>
                    <div className="p-2.5 bg-[#131A22] rounded-lg text-center">
                      <div className="text-[9px] text-[#5F6B78]">Confidence</div>
                      <span className="text-white font-bold text-sm">{simulationResult.confidence}%</span>
                    </div>
                  </div>

                  <div className="p-3 bg-[#131A22] rounded-lg border border-[#26313D]/60 space-y-1 font-sans text-xs">
                    <div className="font-bold text-white">Possible Effect:</div>
                    <div className="text-[#8D9AAA]">{simulationResult.possible_effect}</div>
                  </div>

                  {simulationResult.recommended_action && (
                    <div className="p-3 bg-[#131A22] rounded-lg border border-emerald-500/30 space-y-1 font-sans text-xs">
                      <div className="font-bold text-emerald-400">Recommended Action:</div>
                      <div className="text-[#8D9AAA]">{simulationResult.recommended_action}</div>
                    </div>
                  )}

                  <div className="p-3 bg-[#131A22] rounded-lg border border-[#26313D]/60 space-y-1 font-mono text-[11px]">
                    <div className="font-bold text-cyan-400">Monte Carlo Confidence Interval:</div>
                    <div className="text-[#8D9AAA]">
                      Mean: <strong className="text-white">{simulationResult.monte_carlo.mean_confidence}%</strong> ·
                      5th: {simulationResult.monte_carlo.percentile_5}% ·
                      95th: {simulationResult.monte_carlo.percentile_95}%
                      <span className="ml-2 text-[#5F6B78]">({simulationResult.monte_carlo.iterations} iterations)</span>
                    </div>
                  </div>

                  {simulationResult.assumptions && simulationResult.assumptions.length > 0 && (
                    <div className="p-2.5 bg-[#0B0F14]/50 rounded-lg border border-[#26313D]/40">
                      <div className="text-[9px] text-[#5F6B78] mb-1">Assumptions:</div>
                      <ul className="text-[10px] text-[#8D9AAA] space-y-0.5">
                        {simulationResult.assumptions.map((a, i) => (
                          <li key={i}>• {a}</li>
                        ))}
                      </ul>
                    </div>
                  )}
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
        <div className="space-y-6">
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
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center">
                    <div className="text-[10px] text-[#5F6B78]">Sensory Buffer</div>
                    <div className="text-base font-bold text-white">{experienceStats.sensory_buffer}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center">
                    <div className="text-[10px] text-[#5F6B78]">Short-Term</div>
                    <div className="text-base font-bold text-white">{experienceStats.short_term}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center">
                    <div className="text-[10px] text-[#5F6B78]">Working Memory</div>
                    <div className="text-base font-bold text-emerald-400">{experienceStats.working_memory}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center">
                    <div className="text-[10px] text-[#5F6B78]">Permanent</div>
                    <div className="text-base font-bold text-purple-400">{experienceStats.permanent}</div>
                  </div>
                </div>

                {experienceStats.memory_growth_rate !== undefined && (
                  <div className="flex items-center gap-4 text-xs text-[#8D9AAA] font-mono">
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
                No experience data available.
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - KNOWLEDGE GRAPH
      ============================================================ */}
      {activeTab === 'knowledge_graph' && (
        <div className="space-y-6">
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
                      <div key={c.id} className="flex justify-between text-[11px]">
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
                      <div key={i} className="text-[11px] text-[#8D9AAA]">
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
                        <div key={i} className="text-[10px] px-2 py-1 rounded bg-[#0B0F14] border border-[#26313D]">
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
                No knowledge graph data available.
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - EVALUATOR
      ============================================================ */}
      {activeTab === 'evaluator' && (
        <div className="space-y-6">
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
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center">
                    <div className="text-[10px] text-[#5F6B78]">Total Evaluations</div>
                    <div className="text-base font-bold text-white">{evaluatorStats.total_evaluations}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center">
                    <div className="text-[10px] text-[#5F6B78]">Successful Changes</div>
                    <div className="text-base font-bold text-emerald-400">{evaluatorStats.successful_changes}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center">
                    <div className="text-[10px] text-[#5F6B78]">Active Plans</div>
                    <div className="text-base font-bold text-cyan-400">{evaluatorStats.active_plans}</div>
                  </div>
                  <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] text-center">
                    <div className="text-[10px] text-[#5F6B78]">Accuracy</div>
                    <div className="text-base font-bold text-emerald-400">{evaluatorStats.accuracy}%</div>
                  </div>
                </div>

                {(evaluatorStats.precision !== undefined || evaluatorStats.recall !== undefined || evaluatorStats.f1_score !== undefined) && (
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
                )}
              </>
            ) : (
              <div className="text-center py-8 text-[#5F6B78] text-sm">
                No evaluator data available.
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================
      TAB CONTENT - SETTINGS
      ============================================================ */}
      {activeTab === 'settings' && (
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <Settings className="w-4 h-4 text-emerald-400" />
              Learning Engine Settings
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <div className="text-[#8D9AAA]">Learning Rate</div>
                <div className="text-white font-bold text-sm">{stats?.learningRate || 0.01}</div>
              </div>
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <div className="text-[#8D9AAA]">Decay Rate</div>
                <div className="text-white font-bold text-sm">{stats?.decayRate || 0.005}</div>
              </div>
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <div className="text-[#8D9AAA]">Circuit Breakers</div>
                <div className="text-white font-bold text-sm">{stats?.circuitBreakers || 0}</div>
              </div>
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <div className="text-[#8D9AAA]">Active Sessions</div>
                <div className="text-white font-bold text-sm">{stats?.active_learning_sessions || 0}</div>
              </div>
            </div>

            <div className="flex gap-3 pt-2">
              <button className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-white text-xs font-bold flex items-center gap-2">
                <Play className="w-3.5 h-3.5" />
                Start Learning
              </button>
              <button className="px-4 py-2 bg-amber-600 hover:bg-amber-500 rounded-lg text-white text-xs font-bold flex items-center gap-2">
                <Pause className="w-3.5 h-3.5" />
                Pause
              </button>
              <button className="px-4 py-2 bg-[#0B0F14] hover:bg-[#1A2530] rounded-lg text-[#8D9AAA] text-xs font-bold border border-[#26313D] flex items-center gap-2">
                <RotateCcw className="w-3.5 h-3.5" />
                Reset Weights
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================
      FOOTER
      ============================================================ */}
      <div className="flex items-center justify-between text-[10px] text-[#5F6B78] border-t border-[#26313D]/40 pt-4">
        <span>Last update: {lastUpdate.toLocaleString()}</span>
        <span>Data source: REAL API · v4.0</span>
      </div>
    </div>
  );
};

// ============================================================
// METRIC CARD COMPONENT
// ============================================================

interface MetricCardProps {
  label: string;
  value: string | number;
  icon: React.ElementType;
  color?: 'emerald' | 'blue' | 'purple' | 'cyan' | 'amber' | 'rose';
  sub?: string;
  progress?: number;
  trend?: 'up' | 'down' | 'stable';
}

const MetricCard: React.FC<MetricCardProps> = ({ label, value, icon: Icon, color = 'emerald', sub, progress, trend }) => {
  const colors: Record<string, string> = {
    emerald: 'text-emerald-400 bg-emerald-600/20 border-emerald-500/30',
    blue: 'text-blue-400 bg-blue-600/20 border-blue-500/30',
    purple: 'text-purple-400 bg-purple-600/20 border-purple-500/30',
    cyan: 'text-cyan-400 bg-cyan-600/20 border-cyan-500/30',
    amber: 'text-amber-400 bg-amber-600/20 border-amber-500/30',
    rose: 'text-rose-400 bg-rose-600/20 border-rose-500/30',
  };

  return (
    <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-emerald-500/30 transition-all">
      <div className="flex items-center justify-between">
        <div className="text-[10px] uppercase font-bold text-[#8D9AAA]">{label}</div>
        <div className={`w-6 h-6 rounded-lg ${colors[color]} flex items-center justify-center`}>
          <Icon className="w-3.5 h-3.5" />
        </div>
      </div>
      <div className="text-xl font-black text-white font-mono mt-1">{value}</div>
      {sub && <div className="text-[10px] text-[#5F6B78] mt-0.5">{sub}</div>}
      {progress !== undefined && (
        <div className="w-full bg-[#0B0F14] h-1 rounded-full mt-2 overflow-hidden">
          <div className={`bg-${color}-500 h-full`} style={{ width: `${Math.min(100, progress)}%` }} />
        </div>
      )}
      {trend && (
        <div className="mt-1">
          {trend === 'up' && <TrendingUp className="w-3 h-3 text-emerald-400" />}
          {trend === 'down' && <TrendingDown className="w-3 h-3 text-rose-400" />}
          {trend === 'stable' && <Minus className="w-3 h-3 text-[#5F6B78]" />}
        </div>
      )}
    </div>
  );
};

// ============================================================
// HELPER COMPONENT
// ============================================================

const Minus: React.FC<{ className?: string }> = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const List: React.FC<{ className?: string }> = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="8" y1="6" x2="21" y2="6" />
    <line x1="8" y1="12" x2="21" y2="12" />
    <line x1="8" y1="18" x2="21" y2="18" />
    <line x1="3" y1="6" x2="3.01" y2="6" />
    <line x1="3" y1="12" x2="3.01" y2="12" />
    <line x1="3" y1="18" x2="3.01" y2="18" />
  </svg>
);
