// frontend/src/components/DiagnosticsView.tsx
// INKSIDE DIGITAL - DIAGNOSTICS VIEW v2.0
// FULL VERSION DENGAN SEMUA FITUR FASE 1 & 2
// Search, Filter, Sort, Mini Health Bar, Dependencies, View Logs, Export Report, dll

import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import {
  Activity,
  AlertCircle,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Cpu,
  Database,
  HardDrive,
  Heart,
  LayoutGrid,
  Loader2,
  RefreshCw,
  Server,
  Shield,
  TrendingUp,
  Wifi,
  WifiOff,
  Zap,
  Clock,
  DollarSign,
  Target,
  Layers,
  GitBranch,
  Workflow,
  Eye,
  EyeOff,
  Copy,
  Check,
  Info,
  Search,
  Filter,
  ArrowUpDown,
  FileText,
  Download,
  Link,
  ChevronUp,
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface DiagnosticsStatus {
  status: string;
  version: string;
  mode: string;
  uptime: number;
  timestamp: string;
}

interface SystemMetrics {
  cpu: number;
  ram: number;
  ram_percent?: number;
  disk_percent?: number;
  disk_used?: number;
  disk_total?: number;
  uptime: number;
  memory_count: number;
  knowledge_count: number;
  pnl: number;
  win_rate: number;
  total_trades: number;
  prediction_accuracy: number;
  open_positions: number;
  risk_level: string;
  health_score: number;
  last_update?: string;
  swap_used?: number;
  swap_total?: number;
  swap_percent?: number;
}

interface WatchdogStatus {
  running: boolean;
  components: number;
  checks: number;
  alerts: number;
  restarts: number;
  uptime_seconds: number;
  health_score: number;
  components_healthy: number;
  components_degraded: number;
  components_critical: number;
  components_offline: number;
  pid?: number;
  version?: string;
  timestamp?: string;
  last_alert?: string | null;
  auto_restarts?: number;
  health_trend?: 'up' | 'down' | 'stable';
}

interface HeartbeatData {
  status: string;
  beat_count: number;
  missed_beats: number;
  last_beat: string | null;
  restart_count: number;
  last_error?: string | null;
  is_alive?: boolean;
  health_score?: number;
  last_error_time?: string | null;
}

interface WatchdogSnapshot {
  status: WatchdogStatus;
  components: string[];
  heartbeats: Record<string, HeartbeatData>;
  component_health?: Record<string, number>;
  timestamp: string;
}

interface ComponentDetail {
  name: string;
  registered: boolean;
  heartbeat: HeartbeatData;
  dependencies: string[];
  health_score?: number;
  methods?: Record<string, string>;
  logs?: string[];
  last_scan?: string;
}

// ============================================================
// API CONFIG
// ============================================================

const API_BASE = '';

// ============================================================
// HELPER FUNCTIONS
// ============================================================

const formatUptime = (seconds: number): string => {
  if (!seconds || seconds < 0) return '0s';
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  const parts = [];
  if (days > 0) parts.push(`${days}d`);
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  if (secs > 0 && days === 0) parts.push(`${secs}s`);

  return parts.join(' ') || '0s';
};

const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
};

const getStatusColor = (status: string): string => {
  const s = status?.toLowerCase() || '';
  if (['alive', 'healthy', 'online', 'ok', 'running'].includes(s)) {
    return 'text-green-500 bg-green-500/10 border-green-500/20';
  }
  if (['error', 'dead', 'offline', 'critical', 'stopped'].includes(s)) {
    return 'text-red-500 bg-red-500/10 border-red-500/20';
  }
  if (['warning', 'degraded', 'idle', 'unknown'].includes(s)) {
    return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20';
  }
  return 'text-gray-500 bg-gray-500/10 border-gray-500/20';
};

const getStatusIcon = (status: string): string => {
  const s = status?.toLowerCase() || '';
  if (['alive', 'healthy', 'online', 'ok', 'running'].includes(s)) return '🟢';
  if (['error', 'dead', 'offline', 'critical', 'stopped'].includes(s)) return '🔴';
  if (['warning', 'degraded', 'idle', 'unknown'].includes(s)) return '🟡';
  return '⚪';
};

const getHealthScoreColor = (score: number): string => {
  if (score >= 80) return 'text-green-500';
  if (score >= 60) return 'text-yellow-500';
  if (score >= 40) return 'text-orange-500';
  return 'text-red-500';
};

const getHealthBarColor = (score: number): string => {
  if (score >= 80) return 'bg-green-500';
  if (score >= 60) return 'bg-yellow-500';
  if (score >= 40) return 'bg-orange-500';
  return 'bg-red-500';
};

const getRiskColor = (risk: string): string => {
  const r = risk?.toUpperCase() || '';
  if (r === 'LOW') return 'text-green-500';
  if (r === 'MODERATE') return 'text-yellow-500';
  if (r === 'HIGH') return 'text-orange-500';
  if (r === 'CRITICAL') return 'text-red-500';
  return 'text-gray-500';
};

const getRiskEmoji = (risk: string): string => {
  const r = risk?.toUpperCase() || '';
  if (r === 'LOW') return '🟢';
  if (r === 'MODERATE') return '🟡';
  if (r === 'HIGH') return '🟠';
  if (r === 'CRITICAL') return '🔴';
  return '⚪';
};

const getTrendIcon = (trend?: string) => {
  if (trend === 'up') return <TrendingUp className="w-3 h-3 text-green-400" />;
  if (trend === 'down') return <TrendingUp className="w-3 h-3 text-red-400 transform rotate-180" />;
  return <div className="w-3 h-3 rounded-full bg-gray-500" />;
};

// ============================================================
// SUB-COMPONENTS
// ============================================================

const MetricCard = ({ icon, label, value, subtitle, color = 'blue' }: any) => {
  const colorMap: any = {
    blue: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
    green: 'text-green-400 bg-green-500/10 border-green-500/20',
    yellow: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20',
    red: 'text-red-400 bg-red-500/10 border-red-500/20',
    purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
    cyan: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20',
    emerald: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
    amber: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  };

  return (
    <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-[#3A4A5A] transition-all duration-300 group">
      <div className="flex items-center gap-2.5 mb-2">
        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${colorMap[color]}`}>
          {icon}
        </div>
        <span className="text-[10px] uppercase font-bold text-[#8D9AAA] tracking-wider">{label}</span>
      </div>
      <div className="text-2xl font-bold font-mono text-white">{value}</div>
      {subtitle && <div className="text-[10px] text-[#5F6B78] mt-0.5">{subtitle}</div>}
    </div>
  );
};

const HealthBar = ({ score }: { score: number }) => (
  <div className="w-full bg-[#1A2530] rounded-full h-2 overflow-hidden">
    <div
      className={`h-full rounded-full transition-all duration-700 ease-out ${getHealthBarColor(score)}`}
      style={{ width: `${Math.min(Math.max(score, 0), 100)}%` }}
    />
  </div>
);

const StatusBadge = ({ status }: { status: string }) => (
  <span className={`px-2.5 py-1 rounded-lg text-[10px] font-bold ${getStatusColor(status)}`}>
    {status?.toUpperCase() || 'UNKNOWN'}
  </span>
);

const MiniHealthBar = ({ score, className = '' }: { score: number; className?: string }) => (
  <div className={`w-12 h-1.5 rounded-full bg-[#1A2530] overflow-hidden ${className}`}>
    <div
      className={`h-full rounded-full transition-all duration-500 ${getHealthBarColor(score)}`}
      style={{ width: `${Math.min(Math.max(score, 0), 100)}%` }}
    />
  </div>
);

// ============================================================
// MAIN COMPONENT
// ============================================================

const DiagnosticsView: React.FC = () => {
  // ============================================================
  // STATE
  // ============================================================
  
  const [diagnostics, setDiagnostics] = useState<DiagnosticsStatus | null>(null);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string>('');

  const [watchdogStatus, setWatchdogStatus] = useState<WatchdogStatus | null>(null);
  const [watchdogSnapshot, setWatchdogSnapshot] = useState<WatchdogSnapshot | null>(null);
  const [selectedComponent, setSelectedComponent] = useState<string>('');
  const [componentDetail, setComponentDetail] = useState<ComponentDetail | null>(null);
  const [expandedComponents, setExpandedComponents] = useState<Set<string>>(new Set());

  // Filter & Search State
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'healthy' | 'degraded' | 'critical' | 'offline'>('all');
  const [sortBy, setSortBy] = useState<'name' | 'health' | 'status'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // View Logs State
  const [showLogs, setShowLogs] = useState<boolean>(false);

  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // ============================================================
  // FETCH FUNCTIONS
  // ============================================================

  const fetchDiagnostics = useCallback(async () => {
    try {
      const [diagRes, metricsRes] = await Promise.all([
        axios.get(`${API_BASE}/api/diagnostics`),
        axios.get(`${API_BASE}/api/system/metrics`)
      ]);
      setDiagnostics(diagRes.data);
      setMetrics(metricsRes.data);
      setLastUpdate(new Date().toLocaleTimeString());
      setError(null);
    } catch (err: any) {
      console.error('Failed to fetch diagnostics:', err);
      setError(err.message || 'Failed to connect to API');
    }
  }, []);

  const fetchWatchdogData = useCallback(async () => {
    try {
      const [statusRes, snapshotRes] = await Promise.all([
        axios.get(`${API_BASE}/api/watchdog/status`),
        axios.get(`${API_BASE}/api/watchdog/snapshot`)
      ]);

      setWatchdogStatus(statusRes.data);
      setWatchdogSnapshot(snapshotRes.data);

      const components = snapshotRes.data?.components || [];
      if (components.length > 0 && !selectedComponent) {
        const firstComp = components[0];
        setSelectedComponent(firstComp);
        await fetchComponentDetail(firstComp);
      }
    } catch (err: any) {
      console.error('Failed to fetch watchdog data:', err);
    }
  }, [selectedComponent]);

  const fetchComponentDetail = useCallback(async (name: string) => {
    try {
      const res = await axios.get(`${API_BASE}/api/watchdog/component/${name}`);
      setComponentDetail(res.data);
    } catch (err: any) {
      console.error('Failed to fetch component detail:', err);
    }
  }, []);

  const fetchAllData = useCallback(async () => {
    setLoading(true);
    await Promise.all([fetchDiagnostics(), fetchWatchdogData()]);
    setLoading(false);
  }, [fetchDiagnostics, fetchWatchdogData]);

  // ============================================================
  // HANDLERS
  // ============================================================

  const handleComponentSelect = useCallback(async (name: string) => {
    setSelectedComponent(name);
    await fetchComponentDetail(name);
    setExpandedComponents(prev => new Set(prev).add(name));
  }, [fetchComponentDetail]);

  const handleResetCircuit = useCallback(async (name: string) => {
    try {
      await axios.post(`${API_BASE}/api/watchdog/circuit/${name}/reset`);
      await fetchWatchdogData();
      await fetchComponentDetail(name);
    } catch (err) {
      console.error('Failed to reset circuit:', err);
    }
  }, [fetchWatchdogData, fetchComponentDetail]);

  const handleViewLogs = useCallback(async (name: string) => {
    try {
      const res = await axios.get(`${API_BASE}/api/watchdog/component/${name}/logs`);
      setComponentDetail(prev => prev ? { ...prev, logs: res.data.logs || [] } : null);
      setShowLogs(true);
    } catch (err) {
      console.error('Failed to fetch logs:', err);
    }
  }, []);

  const handleExportReport = useCallback(async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/watchdog/report`);
      const blob = new Blob([JSON.stringify(res.data, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `watchdog-report-${new Date().toISOString().slice(0,10)}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to export report:', err);
    }
  }, []);

  const toggleComponentExpand = (name: string) => {
    setExpandedComponents(prev => {
      const newSet = new Set(prev);
      if (newSet.has(name)) {
        newSet.delete(name);
      } else {
        newSet.add(name);
      }
      return newSet;
    });
  };

  // Filter & Sort Functions
  const getFilteredComponents = useCallback(() => {
    const components = watchdogSnapshot?.components || [];
    const heartbeats = watchdogSnapshot?.heartbeats || {};
    const componentHealth = watchdogSnapshot?.component_health || {};

    let filtered = components.filter(name => {
      // Search filter
      if (searchQuery && !name.toLowerCase().includes(searchQuery.toLowerCase())) {
        return false;
      }

      // Status filter
      const hb = heartbeats[name] || { status: 'unknown' };
      const status = hb.status?.toLowerCase() || 'unknown';
      
      if (statusFilter === 'healthy' && !['alive', 'healthy', 'online', 'ok', 'running'].includes(status)) {
        return false;
      }
      if (statusFilter === 'degraded' && status !== 'degraded' && status !== 'warning') {
        return false;
      }
      if (statusFilter === 'critical' && status !== 'critical' && status !== 'error') {
        return false;
      }
      if (statusFilter === 'offline' && status !== 'offline' && status !== 'dead' && status !== 'stopped') {
        return false;
      }

      return true;
    });

    // Sort
    filtered.sort((a, b) => {
      const healthA = componentHealth[a] || 0;
      const healthB = componentHealth[b] || 0;
      const statusA = (heartbeats[a]?.status?.toLowerCase() || 'unknown');
      const statusB = (heartbeats[b]?.status?.toLowerCase() || 'unknown');

      let comparison = 0;
      if (sortBy === 'name') {
        comparison = a.localeCompare(b);
      } else if (sortBy === 'health') {
        comparison = healthA - healthB;
      } else if (sortBy === 'status') {
        comparison = statusA.localeCompare(statusB);
      }

      return sortOrder === 'asc' ? comparison : -comparison;
    });

    return filtered;
  }, [watchdogSnapshot, searchQuery, statusFilter, sortBy, sortOrder]);

  // ============================================================
  // EFFECTS
  // ============================================================

  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  useEffect(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    intervalRef.current = setInterval(() => {
      fetchDiagnostics();
      fetchWatchdogData();
    }, 5000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [fetchDiagnostics, fetchWatchdogData]);

  // ============================================================
  // LOADING STATE
  // ============================================================

  if (loading && !diagnostics && !watchdogStatus) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4" />
          <p className="text-gray-400 text-sm">Loading diagnostics...</p>
        </div>
      </div>
    );
  }

  // ============================================================
  // RENDER
  // ============================================================

  const components = watchdogSnapshot?.components || [];
  const heartbeats = watchdogSnapshot?.heartbeats || {};
  const componentHealth = watchdogSnapshot?.component_health || {};
  const health = metrics?.health_score || 0;
  const filteredComponents = getFilteredComponents();

  const statusCounts = {
    total: components.length,
    healthy: components.filter(name => {
      const status = heartbeats[name]?.status?.toLowerCase() || '';
      return ['alive', 'healthy', 'online', 'ok', 'running'].includes(status);
    }).length,
    degraded: components.filter(name => {
      const status = heartbeats[name]?.status?.toLowerCase() || '';
      return status === 'degraded' || status === 'warning';
    }).length,
    critical: components.filter(name => {
      const status = heartbeats[name]?.status?.toLowerCase() || '';
      return status === 'critical' || status === 'error';
    }).length,
    offline: components.filter(name => {
      const status = heartbeats[name]?.status?.toLowerCase() || '';
      return status === 'offline' || status === 'dead' || status === 'stopped';
    }).length,
  };

  return (
    <div className="p-4 md:p-6 bg-gray-900 min-h-screen text-white">
      <div className="max-w-7xl mx-auto">
        {/* HEADER */}
        <div className="mb-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-600/20 to-purple-600/20 border border-blue-500/30 flex items-center justify-center">
                <Shield className="w-6 h-6 text-blue-400" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white tracking-tight">
                  System Diagnostics
                  <span className="ml-2 text-xs font-normal text-gray-400 bg-gray-800 px-2.5 py-1 rounded-full">
                    v2.0
                  </span>
                </h1>
                <p className="text-sm text-gray-400">
                  Real-time system health & component monitoring • Last update: {lastUpdate || '--'}
                  {watchdogStatus?.running && (
                    <span className="ml-2 text-xs text-green-500 animate-pulse">● LIVE</span>
                  )}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              {watchdogStatus && (
                <div className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-2 ${
                  watchdogStatus.running
                    ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                    : 'bg-red-500/20 text-red-400 border border-red-500/30'
                }`}>
                  <div className={`w-2 h-2 rounded-full ${watchdogStatus.running ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
                  {watchdogStatus.running ? 'ACTIVE' : 'INACTIVE'}
                </div>
              )}
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <Clock className="w-4 h-4" />
                <span>{formatUptime(metrics?.uptime || 0)}</span>
              </div>
            </div>
          </div>

          {/* Quick Stats Bar - DENGAN DISK & SWAP */}
          {metrics && (
            <div className="mt-4 grid grid-cols-2 md:grid-cols-5 lg:grid-cols-7 gap-3">
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase tracking-wider">Health</div>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`text-xl font-bold font-mono ${getHealthScoreColor(metrics.health_score)}`}>
                    {metrics.health_score}%
                  </span>
                </div>
                <HealthBar score={metrics.health_score} />
              </div>
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase tracking-wider">CPU</div>
                <div className="text-xl font-bold font-mono text-white">{metrics.cpu?.toFixed(1) || 0}%</div>
                <div className="w-full bg-[#1A2530] rounded-full h-1.5 mt-1">
                  <div className={`h-1.5 rounded-full transition-all ${metrics.cpu > 80 ? 'bg-red-500' : metrics.cpu > 60 ? 'bg-yellow-500' : 'bg-green-500'}`} style={{ width: `${Math.min(metrics.cpu || 0, 100)}%` }} />
                </div>
              </div>
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase tracking-wider">RAM</div>
                <div className="text-xl font-bold font-mono text-white">{metrics.ram?.toFixed(1) || 0} GB</div>
                <div className="text-[10px] text-gray-500">{metrics.ram_percent?.toFixed(0) || 0}% used</div>
              </div>
              {/* Disk Usage */}
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase tracking-wider">Disk</div>
                <div className="text-xl font-bold font-mono text-white">
                  {metrics.disk_used ? formatBytes(metrics.disk_used) : '--'}
                </div>
                <div className="text-[10px] text-gray-500">
                  {metrics.disk_total ? `of ${formatBytes(metrics.disk_total)}` : '--'}
                </div>
                {metrics.disk_percent !== undefined && (
                  <div className="w-full bg-[#1A2530] rounded-full h-1.5 mt-1">
                    <div className={`h-1.5 rounded-full transition-all ${metrics.disk_percent > 80 ? 'bg-red-500' : metrics.disk_percent > 60 ? 'bg-yellow-500' : 'bg-green-500'}`} style={{ width: `${Math.min(metrics.disk_percent, 100)}%` }} />
                  </div>
                )}
              </div>
              {/* Swap Usage */}
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase tracking-wider">Swap</div>
                <div className="text-xl font-bold font-mono text-white">
                  {metrics.swap_used ? formatBytes(metrics.swap_used) : '0 B'}
                </div>
                <div className="text-[10px] text-gray-500">
                  {metrics.swap_total ? `of ${formatBytes(metrics.swap_total)}` : 'N/A'}
                </div>
                {metrics.swap_percent !== undefined && metrics.swap_total && metrics.swap_total > 0 && (
                  <div className="w-full bg-[#1A2530] rounded-full h-1.5 mt-1">
                    <div className={`h-1.5 rounded-full transition-all ${metrics.swap_percent > 50 ? 'bg-red-500' : metrics.swap_percent > 25 ? 'bg-yellow-500' : 'bg-green-500'}`} style={{ width: `${Math.min(metrics.swap_percent, 100)}%` }} />
                  </div>
                )}
              </div>
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase tracking-wider">Risk</div>
                <div className="text-xl font-bold font-mono flex items-center gap-1.5">
                  <span>{getRiskEmoji(metrics.risk_level)}</span>
                  <span className={getRiskColor(metrics.risk_level)}>{metrics.risk_level || '--'}</span>
                </div>
              </div>
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase tracking-wider">Knowledge</div>
                <div className="text-xl font-bold font-mono text-white">{metrics.knowledge_count || 0}</div>
                <div className="text-[10px] text-gray-500">items stored</div>
              </div>
            </div>
          )}
        </div>

        {/* ERROR DISPLAY */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
            <p className="text-red-400 text-sm">{error}</p>
            <button
              onClick={() => { setError(null); fetchAllData(); }}
              className="ml-auto px-3 py-1 bg-red-500/20 hover:bg-red-500/30 rounded-lg text-xs text-red-400 transition-colors"
            >
              Retry
            </button>
          </div>
        )}

        {/* TWO COLUMN LAYOUT */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* LEFT COLUMN - Watchdog Status & Components List */}
          <div className="lg:col-span-1 space-y-4">
            {/* Watchdog Status Card - DENGAN FITUR BARU */}
            <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2 mb-4">
                <Heart className="w-4 h-4 text-rose-400" />
                Watchdog Status
              </h3>
              
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400">Status</span>
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${watchdogStatus?.running ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
                    <span className={`text-xs font-bold ${watchdogStatus?.running ? 'text-green-400' : 'text-red-400'}`}>
                      {watchdogStatus?.running ? 'RUNNING' : 'STOPPED'}
                    </span>
                  </div>
                </div>
                
                <div className="flex justify-between items-center p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400">Health Score</span>
                  <div className="flex items-center gap-2">
                    <span className={`text-sm font-bold font-mono ${getHealthScoreColor(watchdogStatus?.health_score || 0)}`}>
                      {watchdogStatus?.health_score || 0}%
                    </span>
                    {watchdogStatus?.health_trend && (
                      <span className="text-xs">
                        {getTrendIcon(watchdogStatus.health_trend)}
                      </span>
                    )}
                  </div>
                </div>

                {/* Component Health Summary - BARU */}
                <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400 block mb-2">Component Health</span>
                  <div className="flex items-center gap-3 text-xs">
                    <span className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-green-500" />
                      <span className="text-green-400 font-bold">{watchdogStatus?.components_healthy || 0}</span>
                      <span className="text-gray-500">healthy</span>
                    </span>
                    <span className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-yellow-500" />
                      <span className="text-yellow-400 font-bold">{watchdogStatus?.components_degraded || 0}</span>
                      <span className="text-gray-500">degraded</span>
                    </span>
                    <span className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-red-500" />
                      <span className="text-red-400 font-bold">{watchdogStatus?.components_critical || 0}</span>
                      <span className="text-gray-500">critical</span>
                    </span>
                    <span className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-gray-500" />
                      <span className="text-gray-400 font-bold">{watchdogStatus?.components_offline || 0}</span>
                      <span className="text-gray-500">offline</span>
                    </span>
                  </div>
                </div>
                
                <div className="flex justify-between items-center p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400">Components</span>
                  <span className="text-sm font-bold font-mono text-white">
                    {watchdogStatus?.components || 0}
                    <span className="text-xs text-gray-500 ml-1">total</span>
                  </span>
                </div>
                
                <div className="flex justify-between items-center p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400">Uptime</span>
                  <span className="text-sm font-bold font-mono text-green-400">
                    {formatUptime(watchdogStatus?.uptime_seconds || 0)}
                  </span>
                </div>
                
                <div className="flex justify-between items-center p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400">Checks</span>
                  <span className="text-sm font-bold font-mono text-yellow-400">
                    {watchdogStatus?.checks || 0}
                  </span>
                </div>
                
                <div className="flex justify-between items-center p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400">Alerts</span>
                  <span className={`text-sm font-bold font-mono ${(watchdogStatus?.alerts || 0) > 0 ? 'text-red-400' : 'text-green-400'}`}>
                    {watchdogStatus?.alerts || 0}
                  </span>
                </div>

                {/* Auto-Restart Count - BARU */}
                <div className="flex justify-between items-center p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400">Auto-Restarts</span>
                  <span className={`text-sm font-bold font-mono ${(watchdogStatus?.auto_restarts || 0) > 0 ? 'text-orange-400' : 'text-green-400'}`}>
                    {watchdogStatus?.auto_restarts || 0}
                  </span>
                </div>

                {/* Last Alert Time - BARU */}
                <div className="flex justify-between items-center p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400">Last Alert</span>
                  <span className="text-xs font-mono text-gray-400">
                    {watchdogStatus?.last_alert
                      ? new Date(watchdogStatus.last_alert).toLocaleTimeString()
                      : 'Never'}
                  </span>
                </div>
              </div>
            </div>

            {/* Components List - DENGAN SEARCH, FILTER, SORT */}
            <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                  <LayoutGrid className="w-4 h-4 text-blue-400" />
                  Components ({filteredComponents.length}/{components.length})
                </h3>
                {/* Export Report Button - BARU */}
                <button
                  onClick={handleExportReport}
                  className="p-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 transition-colors"
                  title="Export Report"
                >
                  <Download className="w-4 h-4" />
                </button>
              </div>

              {/* Search Bar - BARU */}
              <div className="relative mb-3">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                  type="text"
                  placeholder="Search components..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 rounded-xl bg-[#1A2530] border border-[#26313D] text-white text-sm placeholder-gray-500 focus:outline-none focus:border-blue-500/50 transition-colors"
                />
              </div>

              {/* Filter & Sort Controls - BARU */}
              <div className="flex flex-wrap items-center gap-2 mb-3">
                <div className="flex items-center gap-1 bg-[#1A2530] rounded-lg p-1">
                  <button
                    onClick={() => setStatusFilter('all')}
                    className={`px-2 py-1 rounded-md text-xs transition-colors ${
                      statusFilter === 'all' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    All ({statusCounts.total})
                  </button>
                  <button
                    onClick={() => setStatusFilter('healthy')}
                    className={`px-2 py-1 rounded-md text-xs transition-colors ${
                      statusFilter === 'healthy' ? 'bg-green-600 text-white' : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    🟢 ({statusCounts.healthy})
                  </button>
                  <button
                    onClick={() => setStatusFilter('degraded')}
                    className={`px-2 py-1 rounded-md text-xs transition-colors ${
                      statusFilter === 'degraded' ? 'bg-yellow-600 text-white' : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    🟡 ({statusCounts.degraded})
                  </button>
                  <button
                    onClick={() => setStatusFilter('critical')}
                    className={`px-2 py-1 rounded-md text-xs transition-colors ${
                      statusFilter === 'critical' ? 'bg-red-600 text-white' : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    🔴 ({statusCounts.critical})
                  </button>
                  <button
                    onClick={() => setStatusFilter('offline')}
                    className={`px-2 py-1 rounded-md text-xs transition-colors ${
                      statusFilter === 'offline' ? 'bg-gray-600 text-white' : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    ⚫ ({statusCounts.offline})
                  </button>
                </div>

                <div className="flex items-center gap-1 ml-auto">
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as any)}
                    className="px-2 py-1 rounded-lg bg-[#1A2530] border border-[#26313D] text-xs text-gray-400 focus:outline-none focus:border-blue-500/50"
                  >
                    <option value="name">Name</option>
                    <option value="health">Health</option>
                    <option value="status">Status</option>
                  </select>
                  <button
                    onClick={() => setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc')}
                    className="p-1.5 rounded-lg bg-[#1A2530] border border-[#26313D] text-gray-400 hover:text-white transition-colors"
                  >
                    <ArrowUpDown className={`w-3.5 h-3.5 ${sortOrder === 'desc' ? 'transform rotate-180' : ''}`} />
                  </button>
                </div>
              </div>
              
              <div className="space-y-2 max-h-[400px] overflow-y-auto pr-1">
                {filteredComponents.map((name) => {
                  const hb = heartbeats[name] || { status: 'unknown', beat_count: 0, missed_beats: 0, restart_count: 0, last_beat: null };
                  const health = componentHealth[name] || 0;
                  const isSelected = name === selectedComponent;
                  const isExpanded = expandedComponents.has(name);
                  
                  return (
                    <div
                      key={name}
                      className={`rounded-xl border transition-all duration-300 cursor-pointer ${
                        isSelected
                          ? 'bg-blue-900/20 border-blue-500/40'
                          : 'bg-[#1A2530] border-[#26313D] hover:border-[#3A4A5A]'
                      }`}
                    >
                      <div
                        className="p-3 flex items-center justify-between"
                        onClick={() => {
                          handleComponentSelect(name);
                          toggleComponentExpand(name);
                        }}
                      >
                        <div className="flex items-center gap-2.5 min-w-0">
                          <span className="flex-shrink-0">{getStatusIcon(hb.status)}</span>
                          <span className="text-sm font-medium text-white truncate">{name}</span>
                          <StatusBadge status={hb.status || 'unknown'} />
                          {/* Dependency Indicator - BARU */}
                          {componentDetail?.dependencies?.length && componentDetail.name === name && (
                            <span className="flex items-center gap-0.5 text-[8px] text-gray-500">
                              <Link className="w-3 h-3" />
                              {componentDetail.dependencies.length}
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-3 flex-shrink-0">
                          {/* Mini Health Bar - BARU */}
                          <MiniHealthBar score={health} className="w-10" />
                          <span className={`text-xs font-mono font-bold ${getHealthScoreColor(health)}`}>
                            {health}%
                          </span>
                          {isExpanded ? (
                            <ChevronDown className="w-4 h-4 text-gray-500" />
                          ) : (
                            <ChevronRight className="w-4 h-4 text-gray-500" />
                          )}
                        </div>
                      </div>
                      
                      {/* Expanded Detail - DENGAN DEPENDENCIES & VIEW LOGS */}
                      {isExpanded && isSelected && componentDetail && componentDetail.name === name && (
                        <div className="px-3 pb-3 pt-1 border-t border-[#26313D]/50 space-y-2">
                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-gray-400">Beats</span>
                              <div className="font-mono text-white">{componentDetail.heartbeat?.beat_count || 0}</div>
                            </div>
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-gray-400">Missed</span>
                              <div className={`font-mono ${componentDetail.heartbeat?.missed_beats > 0 ? 'text-red-400' : 'text-white'}`}>
                                {componentDetail.heartbeat?.missed_beats || 0}
                              </div>
                            </div>
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-gray-400">Restarts</span>
                              <div className={`font-mono ${componentDetail.heartbeat?.restart_count > 0 ? 'text-orange-400' : 'text-white'}`}>
                                {componentDetail.heartbeat?.restart_count || 0}
                              </div>
                            </div>
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-gray-400">Health</span>
                              <div className={`font-mono font-bold ${getHealthScoreColor(componentDetail.health_score || 0)}`}>
                                {componentDetail.health_score || 0}%
                              </div>
                            </div>
                          </div>

                          {/* Dependencies List - BARU */}
                          {componentDetail.dependencies?.length > 0 && (
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-xs text-gray-400">Dependencies</span>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {componentDetail.dependencies.map((dep) => (
                                  <span key={dep} className="px-2 py-0.5 rounded-md bg-blue-600/20 text-blue-400 text-[10px] font-mono">
                                    {dep}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          <div className="flex gap-2">
                            <button
                              onClick={(e) => { e.stopPropagation(); handleResetCircuit(name); }}
                              className="flex-1 py-1.5 rounded-lg bg-red-600/20 hover:bg-red-600/30 text-red-400 text-xs font-medium transition-colors"
                            >
                              🔄 Reset Circuit
                            </button>
                            {/* View Logs Button - BARU */}
                            <button
                              onClick={(e) => { e.stopPropagation(); handleViewLogs(name); }}
                              className="flex-1 py-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 text-xs font-medium transition-colors flex items-center justify-center gap-1"
                            >
                              <FileText className="w-3 h-3" />
                              View Logs
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}

                {filteredComponents.length === 0 && (
                  <div className="text-center py-8 text-gray-500 text-sm">
                    <Search className="w-8 h-8 mx-auto mb-2 opacity-30" />
                    No components found matching your filters
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN - Component Detail - DENGAN FITUR BARU */}
          <div className="lg:col-span-2 space-y-4">
            {componentDetail ? (
              <>
                {/* Component Header */}
                <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] to-[#1A2530] border border-[#26313D]">
                  <div className="flex items-center justify-between flex-wrap gap-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center">
                        <Server className="w-5 h-5 text-blue-400" />
                      </div>
                      <div>
                        <h2 className="text-lg font-bold text-white">{componentDetail.name}</h2>
                        <p className="text-xs text-gray-400">
                          {componentDetail.registered ? '✅ Registered' : '❌ Not Registered'}
                          {componentDetail.dependencies?.length > 0 && ` • ${componentDetail.dependencies.length} dependencies`}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <StatusBadge status={componentDetail.heartbeat?.status || 'unknown'} />
                      <span className={`text-sm font-bold font-mono ${getHealthScoreColor(componentDetail.health_score || 0)}`}>
                        {componentDetail.health_score || 0}% Health
                      </span>
                    </div>
                  </div>
                </div>

                {/* Component Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                    <div className="text-[10px] text-gray-400 uppercase tracking-wider">Beats</div>
                    <div className="text-xl font-bold font-mono text-white mt-1">{componentDetail.heartbeat?.beat_count || 0}</div>
                  </div>
                  <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                    <div className="text-[10px] text-gray-400 uppercase tracking-wider">Missed</div>
                    <div className={`text-xl font-bold font-mono mt-1 ${componentDetail.heartbeat?.missed_beats > 0 ? 'text-red-400' : 'text-white'}`}>
                      {componentDetail.heartbeat?.missed_beats || 0}
                    </div>
                  </div>
                  <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                    <div className="text-[10px] text-gray-400 uppercase tracking-wider">Restarts</div>
                    <div className={`text-xl font-bold font-mono mt-1 ${componentDetail.heartbeat?.restart_count > 0 ? 'text-orange-400' : 'text-white'}`}>
                      {componentDetail.heartbeat?.restart_count || 0}
                    </div>
                  </div>
                  <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                    <div className="text-[10px] text-gray-400 uppercase tracking-wider">Health</div>
                    <div className={`text-xl font-bold font-mono mt-1 ${getHealthScoreColor(componentDetail.health_score || 0)}`}>
                      {componentDetail.health_score || 0}%
                    </div>
                  </div>
                </div>

                {/* Dependencies Section - BARU */}
                {componentDetail.dependencies?.length > 0 && (
                  <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
                    <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2 mb-4">
                      <Link className="w-4 h-4 text-purple-400" />
                      Dependencies
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {componentDetail.dependencies.map((dep) => (
                        <span
                          key={dep}
                          className="px-3 py-1.5 rounded-xl bg-purple-600/10 border border-purple-500/30 text-purple-400 text-sm font-mono"
                        >
                          {dep}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Methods Section - BARU */}
                {componentDetail.methods && Object.keys(componentDetail.methods).length > 0 && (
                  <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
                    <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2 mb-4">
                      <Workflow className="w-4 h-4 text-cyan-400" />
                      Available Methods
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                      {Object.entries(componentDetail.methods).map(([name, type]) => (
                        <div key={name} className="p-2 rounded-lg bg-[#1A2530] border border-[#26313D]/50">
                          <span className="text-xs font-mono text-white">{name}</span>
                          <span className="text-[9px] text-gray-500 block">{type}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Heartbeat Detail - DENGAN LAST ERROR TIME */}
                <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
                  <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2 mb-4">
                    <Heart className="w-4 h-4 text-rose-400" />
                    Heartbeat Details
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                    <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                      <span className="text-xs text-gray-400 block">Status</span>
                      <span className="font-bold text-white">{componentDetail.heartbeat?.status?.toUpperCase() || 'UNKNOWN'}</span>
                    </div>
                    <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                      <span className="text-xs text-gray-400 block">Last Beat</span>
                      <span className="font-mono text-white text-xs">
                        {componentDetail.heartbeat?.last_beat
                          ? new Date(componentDetail.heartbeat.last_beat).toLocaleTimeString()
                          : 'Never'}
                      </span>
                    </div>
                    <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                      <span className="text-xs text-gray-400 block">Is Alive</span>
                      <span className={`font-bold ${componentDetail.heartbeat?.is_alive ? 'text-green-400' : 'text-red-400'}`}>
                        {componentDetail.heartbeat?.is_alive ? '✅ Yes' : '❌ No'}
                      </span>
                    </div>
                    {/* Last Error Time - BARU */}
                    {componentDetail.heartbeat?.last_error_time && (
                      <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                        <span className="text-xs text-gray-400 block">Last Error Time</span>
                        <span className="font-mono text-red-400 text-xs">
                          {new Date(componentDetail.heartbeat.last_error_time).toLocaleTimeString()}
                        </span>
                      </div>
                    )}
                    {componentDetail.heartbeat?.last_error && (
                      <div className="col-span-full p-3 rounded-xl bg-red-500/10 border border-red-500/30">
                        <span className="text-xs text-gray-400 block">Last Error</span>
                        <span className="text-xs text-red-400 font-mono">{componentDetail.heartbeat.last_error}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Logs Section - BARU */}
                {showLogs && componentDetail.logs && componentDetail.logs.length > 0 && (
                  <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                        <FileText className="w-4 h-4 text-yellow-400" />
                        Logs
                      </h3>
                      <button
                        onClick={() => setShowLogs(false)}
                        className="text-xs text-gray-400 hover:text-white transition-colors"
                      >
                        Close
                      </button>
                    </div>
                    <div className="max-h-60 overflow-y-auto space-y-1 font-mono text-xs">
                      {componentDetail.logs.map((log, index) => (
                        <div key={index} className="p-1.5 rounded bg-[#0B0F14] text-gray-300 border border-[#26313D]/30">
                          {log}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Actions - DENGAN TOMBOL BARU */}
                <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
                  <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2 mb-4">
                    <Zap className="w-4 h-4 text-yellow-400" />
                    Actions
                  </h3>
                  <div className="flex flex-wrap gap-3">
                    <button
                      onClick={() => handleResetCircuit(selectedComponent)}
                      className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-sm font-medium transition-all shadow-md shadow-red-600/30"
                    >
                      🔄 Reset Circuit Breaker
                    </button>
                    <button
                      onClick={() => {
                        fetchWatchdogData();
                        fetchComponentDetail(selectedComponent);
                      }}
                      className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium transition-all shadow-md shadow-blue-600/30"
                    >
                      🔍 Refresh Component
                    </button>
                    {/* View Logs Button - BARU */}
                    <button
                      onClick={() => handleViewLogs(selectedComponent)}
                      className="px-4 py-2 rounded-xl bg-yellow-600 hover:bg-yellow-700 text-white text-sm font-medium transition-all shadow-md shadow-yellow-600/30"
                    >
                      📝 View Logs
                    </button>
                    {/* Export Report Button - BARU */}
                    <button
                      onClick={handleExportReport}
                      className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium transition-all shadow-md shadow-purple-600/30"
                    >
                      📊 Export Report
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <div className="p-12 text-center text-gray-500 bg-[#131A22] rounded-2xl border border-[#26313D]">
                <Server className="w-12 h-12 mx-auto mb-3 opacity-30" />
                <p className="text-sm font-medium">Select a component from the list</p>
                <p className="text-xs mt-1">Click any component to view its details</p>
              </div>
            )}
          </div>
        </div>

        {/* FOOTER - DENGAN LAST SCAN */}
        <div className="mt-8 pt-4 border-t border-[#26313D]/40 flex flex-wrap items-center justify-between text-[10px] text-gray-600 gap-2">
          <span>
            Inkside Digital v2.0 • Diagnostics & Watchdog v3.1
            {watchdogStatus?.running ? ' 🟢 All systems operational' : ' 🔴 Monitoring inactive'}
          </span>
          <div className="flex items-center gap-4">
            <span>
              PID: {watchdogStatus?.pid || 'N/A'} • 
              Components: {watchdogStatus?.components || 0} • 
              Uptime: {formatUptime(watchdogStatus?.uptime_seconds || 0)}
            </span>
            {/* Last Scan - BARU */}
            <span className="text-gray-500">
              Last scan: {lastUpdate || '--'}
            </span>
            <span className="text-gray-500">
              v{diagnostics?.version || 'N/A'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export { DiagnosticsView };
