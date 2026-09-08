// src/components/DiagnosticsView.tsx
// INKSIDE DIGITAL - DIAGNOSTICS VIEW v3.0
// FULLY INTEGRATED WITH BACKEND ENDPOINTS

import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Activity, AlertCircle, CheckCircle2, ChevronDown, ChevronRight,
  Cpu, Database, HardDrive, Heart, LayoutGrid, Loader2, RefreshCw,
  Server, Shield, TrendingUp, Wifi, WifiOff, Zap, Clock,
  Search, Filter, ArrowUpDown, Download, Link, FileText,
  Eye, EyeOff, Copy, Check, Info, GitBranch, Workflow
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
  ram_percent: number;
  disk_percent: number;
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
  last_alert?: string;
  auto_restarts?: number;
  health_trend?: 'up' | 'down' | 'stable';
}

interface HeartbeatData {
  status: string;
  beat_count: number;
  missed_beats: number;
  last_beat: string | null;
  restart_count: number;
  last_error?: string;
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
  logs?: string[];
}

// ============================================================
// API CONFIG
// ============================================================

const API_KEY = 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ';
const API_BASE = '';

// ============================================================
// HELPERS
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
    return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
  }
  if (['error', 'dead', 'offline', 'critical', 'stopped'].includes(s)) {
    return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
  }
  if (['warning', 'degraded', 'idle', 'unknown'].includes(s)) {
    return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
  }
  return 'text-gray-400 bg-gray-500/10 border-gray-500/20';
};

const getStatusIcon = (status: string): string => {
  const s = status?.toLowerCase() || '';
  if (['alive', 'healthy', 'online', 'ok', 'running'].includes(s)) return '🟢';
  if (['error', 'dead', 'offline', 'critical', 'stopped'].includes(s)) return '🔴';
  if (['warning', 'degraded', 'idle', 'unknown'].includes(s)) return '🟡';
  return '⚪';
};

const getHealthScoreColor = (score: number): string => {
  if (score >= 80) return 'text-emerald-400';
  if (score >= 60) return 'text-amber-400';
  if (score >= 40) return 'text-orange-400';
  return 'text-rose-400';
};

const getHealthBarColor = (score: number): string => {
  if (score >= 80) return 'bg-emerald-500';
  if (score >= 60) return 'bg-amber-500';
  if (score >= 40) return 'bg-orange-500';
  return 'bg-rose-500';
};

const getRiskColor = (risk: string): string => {
  const r = risk?.toUpperCase() || '';
  if (r === 'LOW') return 'text-emerald-400';
  if (r === 'MODERATE') return 'text-amber-400';
  if (r === 'HIGH') return 'text-orange-400';
  if (r === 'CRITICAL') return 'text-rose-400';
  return 'text-gray-400';
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const DiagnosticsView: React.FC = () => {
  // ===== STATE =====
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [diagnostics, setDiagnostics] = useState<DiagnosticsStatus | null>(null);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [watchdogStatus, setWatchdogStatus] = useState<WatchdogStatus | null>(null);
  const [watchdogSnapshot, setWatchdogSnapshot] = useState<WatchdogSnapshot | null>(null);
  const [selectedComponent, setSelectedComponent] = useState<string>('');
  const [componentDetail, setComponentDetail] = useState<ComponentDetail | null>(null);
  const [expandedComponents, setExpandedComponents] = useState<Set<string>>(new Set());
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'healthy' | 'degraded' | 'critical' | 'offline'>('all');
  const [sortBy, setSortBy] = useState<'name' | 'health' | 'status'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // ===== FETCH FUNCTIONS =====
  const fetchWithAuth = useCallback(async (endpoint: string) => {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'X-API-Key': localStorage.getItem('apiKey') || API_KEY
      }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }, []);

  const fetchDiagnosticsData = useCallback(async () => {
    try {
      const [diagRes, metricsRes, statusRes, snapshotRes] = await Promise.all([
        fetchWithAuth('/api/diagnostics'),
        fetchWithAuth('/api/system/metrics'),
        fetchWithAuth('/api/watchdog/status'),
        fetchWithAuth('/api/watchdog/snapshot')
      ]);

      setDiagnostics(diagRes);
      setMetrics(metricsRes);
      setWatchdogStatus(statusRes);
      setWatchdogSnapshot(snapshotRes);
      setLastUpdate(new Date().toLocaleTimeString());
      setError(null);

      const components = snapshotRes?.components || [];
      if (components.length > 0 && !selectedComponent) {
        setSelectedComponent(components[0]);
        await fetchComponentDetail(components[0]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch diagnostics');
    } finally {
      setLoading(false);
    }
  }, [fetchWithAuth, selectedComponent]);

  const fetchComponentDetail = useCallback(async (name: string) => {
    try {
      const res = await fetchWithAuth(`/api/watchdog/component/${name}`);
      setComponentDetail(res);
    } catch (err) {
      console.error('Failed to fetch component detail:', err);
    }
  }, [fetchWithAuth]);

  const handleComponentSelect = useCallback(async (name: string) => {
    setSelectedComponent(name);
    await fetchComponentDetail(name);
    setExpandedComponents(prev => new Set(prev).add(name));
  }, [fetchComponentDetail]);

  const handleResetCircuit = useCallback(async (name: string) => {
    try {
      await fetchWithAuth(`/api/watchdog/circuit/${name}/reset`);
      await fetchDiagnosticsData();
      await fetchComponentDetail(name);
    } catch (err) {
      console.error('Failed to reset circuit:', err);
    }
  }, [fetchWithAuth, fetchDiagnosticsData, fetchComponentDetail]);

  const handleExportReport = useCallback(async () => {
    try {
      const res = await fetchWithAuth('/api/watchdog/report');
      const blob = new Blob([JSON.stringify(res, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `watchdog-report-${new Date().toISOString().slice(0,10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to export report:', err);
    }
  }, [fetchWithAuth]);

  // ===== FILTER & SORT =====
  const getFilteredComponents = useCallback(() => {
    const components = watchdogSnapshot?.components || [];
    const heartbeats = watchdogSnapshot?.heartbeats || {};
    const componentHealth = watchdogSnapshot?.component_health || {};

    let filtered = components.filter(name => {
      if (searchQuery && !name.toLowerCase().includes(searchQuery.toLowerCase())) return false;
      const status = heartbeats[name]?.status?.toLowerCase() || 'unknown';
      if (statusFilter === 'healthy' && !['alive', 'healthy', 'online', 'ok', 'running'].includes(status)) return false;
      if (statusFilter === 'degraded' && status !== 'degraded' && status !== 'warning') return false;
      if (statusFilter === 'critical' && status !== 'critical' && status !== 'error') return false;
      if (statusFilter === 'offline' && !['offline', 'dead', 'stopped'].includes(status)) return false;
      return true;
    });

    filtered.sort((a, b) => {
      const healthA = componentHealth[a] || 0;
      const healthB = componentHealth[b] || 0;
      const statusA = heartbeats[a]?.status?.toLowerCase() || 'unknown';
      const statusB = heartbeats[b]?.status?.toLowerCase() || 'unknown';
      let comparison = 0;
      if (sortBy === 'name') comparison = a.localeCompare(b);
      else if (sortBy === 'health') comparison = healthA - healthB;
      else if (sortBy === 'status') comparison = statusA.localeCompare(statusB);
      return sortOrder === 'asc' ? comparison : -comparison;
    });

    return filtered;
  }, [watchdogSnapshot, searchQuery, statusFilter, sortBy, sortOrder]);

  // ===== EFFECTS =====
  useEffect(() => {
    fetchDiagnosticsData();
    const interval = setInterval(fetchDiagnosticsData, 10000);
    return () => clearInterval(interval);
  }, [fetchDiagnosticsData]);

  // ===== LOADING =====
  if (loading) {
    return (
      <div className="flex items-center justify-center h-96 bg-[#0B0F14]">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-400 animate-spin mx-auto" />
          <p className="text-[#8D9AAA] mt-4">Loading diagnostics...</p>
        </div>
      </div>
    );
  }

  // ===== RENDER =====
  const components = watchdogSnapshot?.components || [];
  const heartbeats = watchdogSnapshot?.heartbeats || {};
  const componentHealth = watchdogSnapshot?.component_health || {};
  const filteredComponents = getFilteredComponents();

  const statusCounts = {
    total: components.length,
    healthy: components.filter(n => ['alive', 'healthy', 'online', 'ok', 'running'].includes(heartbeats[n]?.status?.toLowerCase() || '')).length,
    degraded: components.filter(n => (heartbeats[n]?.status?.toLowerCase() || '') === 'degraded' || (heartbeats[n]?.status?.toLowerCase() || '') === 'warning').length,
    critical: components.filter(n => (heartbeats[n]?.status?.toLowerCase() || '') === 'critical' || (heartbeats[n]?.status?.toLowerCase() || '') === 'error').length,
    offline: components.filter(n => ['offline', 'dead', 'stopped'].includes(heartbeats[n]?.status?.toLowerCase() || '')).length,
  };

  return (
    <div className="p-4 md:p-6 bg-[#0B0F14] min-h-screen text-white">
      <div className="max-w-7xl mx-auto">
        {/* HEADER */}
        <div className="mb-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-600/20 to-purple-600/20 border border-blue-500/30 flex items-center justify-center">
                <Shield className="w-6 h-6 text-blue-400" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">System Diagnostics</h1>
                <p className="text-sm text-gray-400">
                  Real-time system health • Last update: {lastUpdate || '--'}
                  {watchdogStatus?.running && <span className="ml-2 text-emerald-400 animate-pulse">● LIVE</span>}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-2 ${watchdogStatus?.running ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'}`}>
                <div className={`w-2 h-2 rounded-full ${watchdogStatus?.running ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'}`} />
                {watchdogStatus?.running ? 'ACTIVE' : 'INACTIVE'}
              </div>
              <button onClick={fetchDiagnosticsData} className="p-2 rounded-lg bg-[#1A2530] hover:bg-[#26313D] transition-colors">
                <RefreshCw className="w-4 h-4 text-[#8D9AAA]" />
              </button>
            </div>
          </div>

          {/* QUICK STATS */}
          {metrics && (
            <div className="mt-4 grid grid-cols-2 md:grid-cols-5 gap-3">
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase">Health</div>
                <div className={`text-xl font-bold font-mono ${getHealthScoreColor(metrics.health_score)}`}>
                  {metrics.health_score}%
                </div>
                <div className="w-full bg-[#1A2530] rounded-full h-1.5 mt-1">
                  <div className={`h-1.5 rounded-full ${getHealthBarColor(metrics.health_score)}`} style={{ width: `${Math.min(metrics.health_score, 100)}%` }} />
                </div>
              </div>
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase">CPU</div>
                <div className="text-xl font-bold font-mono text-white">{metrics.cpu?.toFixed(1) || 0}%</div>
              </div>
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase">RAM</div>
                <div className="text-xl font-bold font-mono text-white">{metrics.ram_percent?.toFixed(0) || 0}%</div>
              </div>
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase">Disk</div>
                <div className="text-xl font-bold font-mono text-white">{metrics.disk_percent?.toFixed(0) || 0}%</div>
              </div>
              <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-gray-400 uppercase">Risk</div>
                <div className={`text-xl font-bold font-mono ${getRiskColor(metrics.risk_level)}`}>
                  {metrics.risk_level || '--'}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* ERROR */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-rose-400" />
            <p className="text-rose-400 text-sm">{error}</p>
            <button onClick={fetchDiagnosticsData} className="ml-auto px-3 py-1 bg-rose-500/20 hover:bg-rose-500/30 rounded-lg text-xs text-rose-400">
              Retry
            </button>
          </div>
        )}

        {/* TWO COLUMN LAYOUT */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* LEFT COLUMN - Components */}
          <div className="lg:col-span-1 space-y-4">
            <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <LayoutGrid className="w-4 h-4 text-blue-400" />
                  Components ({filteredComponents.length}/{components.length})
                </h3>
                <button onClick={handleExportReport} className="p-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 text-blue-400" title="Export Report">
                  <Download className="w-4 h-4" />
                </button>
              </div>

              {/* Search */}
              <div className="relative mb-3">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                  type="text"
                  placeholder="Search components..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 rounded-xl bg-[#1A2530] border border-[#26313D] text-white text-sm placeholder-gray-500 focus:outline-none focus:border-blue-500/50"
                />
              </div>

              {/* Filters */}
              <div className="flex flex-wrap items-center gap-2 mb-3">
                <div className="flex items-center gap-1 bg-[#1A2530] rounded-lg p-1">
                  {[
                    { key: 'all', label: `All (${statusCounts.total})` },
                    { key: 'healthy', label: `🟢 (${statusCounts.healthy})` },
                    { key: 'degraded', label: `🟡 (${statusCounts.degraded})` },
                    { key: 'critical', label: `🔴 (${statusCounts.critical})` },
                    { key: 'offline', label: `⚫ (${statusCounts.offline})` }
                  ].map(({ key, label }) => (
                    <button
                      key={key}
                      onClick={() => setStatusFilter(key as any)}
                      className={`px-2 py-1 rounded-md text-xs transition-colors ${statusFilter === key ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'}`}
                    >
                      {label}
                    </button>
                  ))}
                </div>
                <div className="flex items-center gap-1 ml-auto">
                  <select value={sortBy} onChange={(e) => setSortBy(e.target.value as any)} className="px-2 py-1 rounded-lg bg-[#1A2530] border border-[#26313D] text-xs text-gray-400 focus:outline-none focus:border-blue-500/50">
                    <option value="name">Name</option>
                    <option value="health">Health</option>
                    <option value="status">Status</option>
                  </select>
                  <button onClick={() => setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc')} className="p-1.5 rounded-lg bg-[#1A2530] border border-[#26313D] text-gray-400 hover:text-white">
                    <ArrowUpDown className={`w-3.5 h-3.5 ${sortOrder === 'desc' ? 'transform rotate-180' : ''}`} />
                  </button>
                </div>
              </div>

              {/* Component List */}
              <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
                {filteredComponents.map((name) => {
                  const hb = heartbeats[name] || { status: 'unknown', beat_count: 0, missed_beats: 0, restart_count: 0, last_beat: null };
                  const health = componentHealth[name] || 0;
                  const isSelected = name === selectedComponent;
                  const isExpanded = expandedComponents.has(name);

                  return (
                    <div key={name} className={`rounded-xl border transition-all cursor-pointer ${isSelected ? 'bg-blue-900/20 border-blue-500/40' : 'bg-[#1A2530] border-[#26313D] hover:border-[#3A4A5A]'}`}>
                      <div className="p-3 flex items-center justify-between" onClick={() => handleComponentSelect(name)}>
                        <div className="flex items-center gap-2.5 min-w-0">
                          <span>{getStatusIcon(hb.status)}</span>
                          <span className="text-sm font-medium text-white truncate">{name}</span>
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${getStatusColor(hb.status)}`}>
                            {hb.status?.toUpperCase() || 'UNKNOWN'}
                          </span>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className={`text-xs font-mono font-bold ${getHealthScoreColor(health)}`}>{health}%</span>
                          {isExpanded ? <ChevronDown className="w-4 h-4 text-gray-500" /> : <ChevronRight className="w-4 h-4 text-gray-500" />}
                        </div>
                      </div>

                      {isExpanded && isSelected && componentDetail && componentDetail.name === name && (
                        <div className="px-3 pb-3 pt-1 border-t border-[#26313D]/50 space-y-2">
                          <div className="grid grid-cols-2 gap-2 text-xs">
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-gray-400">Beats</span>
                              <div className="font-mono text-white">{hb.beat_count}</div>
                            </div>
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-gray-400">Missed</span>
                              <div className={`font-mono ${hb.missed_beats > 0 ? 'text-rose-400' : 'text-white'}`}>{hb.missed_beats}</div>
                            </div>
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-gray-400">Restarts</span>
                              <div className={`font-mono ${hb.restart_count > 0 ? 'text-orange-400' : 'text-white'}`}>{hb.restart_count}</div>
                            </div>
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-gray-400">Health</span>
                              <div className={`font-mono font-bold ${getHealthScoreColor(componentDetail.health_score || 0)}`}>{componentDetail.health_score || 0}%</div>
                            </div>
                          </div>

                          {componentDetail.dependencies?.length > 0 && (
                            <div className="p-2 rounded-lg bg-[#0B0F14]">
                              <span className="text-xs text-gray-400">Dependencies</span>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {componentDetail.dependencies.map((dep) => (
                                  <span key={dep} className="px-2 py-0.5 rounded-md bg-blue-600/20 text-blue-400 text-[10px] font-mono">{dep}</span>
                                ))}
                              </div>
                            </div>
                          )}

                          <div className="flex gap-2">
                            <button onClick={(e) => { e.stopPropagation(); handleResetCircuit(name); }} className="flex-1 py-1.5 rounded-lg bg-rose-600/20 hover:bg-rose-600/30 text-rose-400 text-xs font-medium">
                              🔄 Reset Circuit
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
                    No components found
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN - Detail */}
          <div className="lg:col-span-2 space-y-4">
            {componentDetail ? (
              <>
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
                    <StatusBadge status={componentDetail.heartbeat?.status || 'unknown'} />
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                    <div className="text-[10px] text-gray-400 uppercase">Beats</div>
                    <div className="text-xl font-bold font-mono text-white">{componentDetail.heartbeat?.beat_count || 0}</div>
                  </div>
                  <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                    <div className="text-[10px] text-gray-400 uppercase">Missed</div>
                    <div className={`text-xl font-bold font-mono ${componentDetail.heartbeat?.missed_beats > 0 ? 'text-rose-400' : 'text-white'}`}>{componentDetail.heartbeat?.missed_beats || 0}</div>
                  </div>
                  <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                    <div className="text-[10px] text-gray-400 uppercase">Restarts</div>
                    <div className={`text-xl font-bold font-mono ${componentDetail.heartbeat?.restart_count > 0 ? 'text-orange-400' : 'text-white'}`}>{componentDetail.heartbeat?.restart_count || 0}</div>
                  </div>
                  <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                    <div className="text-[10px] text-gray-400 uppercase">Health</div>
                    <div className={`text-xl font-bold font-mono ${getHealthScoreColor(componentDetail.health_score || 0)}`}>{componentDetail.health_score || 0}%</div>
                  </div>
                </div>

                <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
                    <Heart className="w-4 h-4 text-rose-400" />
                    Heartbeat Details
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                      <span className="text-xs text-gray-400 block">Status</span>
                      <span className="font-bold text-white">{componentDetail.heartbeat?.status?.toUpperCase() || 'UNKNOWN'}</span>
                    </div>
                    <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                      <span className="text-xs text-gray-400 block">Last Beat</span>
                      <span className="font-mono text-white text-xs">{componentDetail.heartbeat?.last_beat ? new Date(componentDetail.heartbeat.last_beat).toLocaleTimeString() : 'Never'}</span>
                    </div>
                    <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]/50">
                      <span className="text-xs text-gray-400 block">Is Alive</span>
                      <span className={`font-bold ${componentDetail.heartbeat?.is_alive ? 'text-emerald-400' : 'text-rose-400'}`}>{componentDetail.heartbeat?.is_alive ? '✅ Yes' : '❌ No'}</span>
                    </div>
                  </div>
                </div>

                <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
                    <Zap className="w-4 h-4 text-yellow-400" />
                    Actions
                  </h3>
                  <div className="flex flex-wrap gap-3">
                    <button onClick={() => handleResetCircuit(selectedComponent)} className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-sm font-medium shadow-md shadow-rose-600/30">
                      🔄 Reset Circuit Breaker
                    </button>
                    <button onClick={() => { fetchDiagnosticsData(); fetchComponentDetail(selectedComponent); }} className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium shadow-md shadow-blue-600/30">
                      🔍 Refresh
                    </button>
                    <button onClick={handleExportReport} className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium shadow-md shadow-purple-600/30">
                      📊 Export Report
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <div className="p-12 text-center text-gray-500 bg-[#131A22] rounded-2xl border border-[#26313D]">
                <Server className="w-12 h-12 mx-auto mb-3 opacity-30" />
                <p className="text-sm font-medium">Select a component from the list</p>
              </div>
            )}
          </div>
        </div>

        {/* FOOTER */}
        <div className="mt-8 pt-4 border-t border-[#26313D]/40 flex flex-wrap items-center justify-between text-[10px] text-gray-600 gap-2">
          <span>Inkside Digital v{diagnostics?.version || 'N/A'} • Diagnostics v3.0</span>
          <div className="flex items-center gap-4">
            <span>PID: {watchdogStatus?.pid || 'N/A'} • Components: {watchdogStatus?.components || 0}</span>
            <span className="text-gray-500">Last scan: {lastUpdate}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================================
// HELPER COMPONENT
// ============================================================

const StatusBadge: React.FC<{ status: string }> = ({ status }) => (
  <span className={`px-2.5 py-1 rounded-lg text-[10px] font-bold ${getStatusColor(status)}`}>
    {status?.toUpperCase() || 'UNKNOWN'}
  </span>
);

export default DiagnosticsView;
