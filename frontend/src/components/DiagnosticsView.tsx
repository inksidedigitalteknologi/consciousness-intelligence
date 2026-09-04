// frontend/src/components/DiagnosticsView.tsx
// INKSIDE DIGITAL - DIAGNOSTICS VIEW v7.0
// REAL DATA - SMOOTH UI - NO DUMMY

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

  return (
    <div className="p-4 md:p-6 bg-gray-900 min-h-screen text-white">
      <div className="max-w-7xl mx-auto">
        {/* ============================================================
        HEADER - SMOOTH
        ============================================================ */}
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
                    v7.0
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

          {/* Quick Stats Bar */}
          {metrics && (
            <div className="mt-4 grid grid-cols-2 md:grid-cols-5 gap-3">
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

        {/* ============================================================
        ERROR DISPLAY
        ============================================================ */}
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

        {/* ============================================================
        TWO COLUMN LAYOUT
        ============================================================ */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* LEFT COLUMN - Watchdog Status & Components List */}
          <div className="lg:col-span-1 space-y-4">
            {/* Watchdog Status Card */}
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
                  <span className={`text-sm font-bold font-mono ${getHealthScoreColor(watchdogStatus?.health_score || 0)}`}>
                    {watchdogStatus?.health_score || 0}%
                  </span>
                </div>
                
                <div className="flex justify-between items-center p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                  <span className="text-xs text-gray-400">Components</span>
                  <span className="text-sm font-bold font-mono text-white">
                    {watchdogStatus?.components_healthy || 0}/{watchdogStatus?.components || 0}
                    <span className="text-xs text-gray-500 ml-1">healthy</span>
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
              </div>
            </div>

            {/* Components List */}
            <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2 mb-4">
                <LayoutGrid className="w-4 h-4 text-blue-400" />
                Components ({components.length})
              </h3>
              
              <div className="space-y-2 max-h-[400px] overflow-y-auto pr-1">
                {components.map((name) => {
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
                        </div>
                        <div className="flex items-center gap-3 flex-shrink-0">
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
                      
                      {/* Expanded Detail */}
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
                          <button
                            onClick={(e) => { e.stopPropagation(); handleResetCircuit(name); }}
                            className="w-full py-1.5 rounded-lg bg-red-600/20 hover:bg-red-600/30 text-red-400 text-xs font-medium transition-colors"
                          >
                            🔄 Reset Circuit
                          </button>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN - Component Detail */}
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

                {/* Heartbeat Detail */}
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
                    {componentDetail.heartbeat?.last_error && (
                      <div className="col-span-full p-3 rounded-xl bg-red-500/10 border border-red-500/30">
                        <span className="text-xs text-gray-400 block">Last Error</span>
                        <span className="text-xs text-red-400 font-mono">{componentDetail.heartbeat.last_error}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Actions */}
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

        {/* ============================================================
        FOOTER
        ============================================================ */}
        <div className="mt-8 pt-4 border-t border-[#26313D]/40 flex flex-wrap items-center justify-between text-[10px] text-gray-600 gap-2">
          <span>
            Inkside Digital v7.0 • Diagnostics & Watchdog v3.1 REAL
            {watchdogStatus?.running ? ' 🟢 All systems operational' : ' 🔴 Monitoring inactive'}
          </span>
          <span>
            PID: {watchdogStatus?.pid || 'N/A'} • 
            Components: {watchdogStatus?.components || 0} • 
            Uptime: {formatUptime(watchdogStatus?.uptime_seconds || 0)}
          </span>
        </div>
      </div>
    </div>
  );
};

export { DiagnosticsView };
