// frontend/src/components/DiagnosticsView.tsx
// INKSIDE DIGITAL - DIAGNOSTICS VIEW v6.0
// REAL DATA - TANPA DUMMY
// FIX: API_BASE_URL, Error Handling, Auto-Refresh

import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';

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

// ✅ GUNakan PATH RELATIF - Nginx akan proxy ke backend
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
  const [autoRefresh, setAutoRefresh] = useState<boolean>(true);
  const [watchdogError, setWatchdogError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState<number>(0);

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
      setWatchdogError(null);
      
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
      setWatchdogError(err.message || 'Watchdog API not available');
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

  const handleRefreshAll = useCallback(async () => {
    setRefreshKey(prev => prev + 1);
    await fetchAllData();
  }, [fetchAllData]);

  const toggleAutoRefresh = useCallback(() => {
    setAutoRefresh(prev => !prev);
  }, []);

  // ============================================================
  // EFFECTS
  // ============================================================

  // Initial load
  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  // Auto-refresh
  useEffect(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    if (autoRefresh) {
      intervalRef.current = setInterval(() => {
        fetchDiagnostics();
        fetchWatchdogData();
      }, 5000);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [autoRefresh, fetchDiagnostics, fetchWatchdogData]);

  // ============================================================
  // LOADING STATE
  // ============================================================

  if (loading && !diagnostics && !watchdogStatus) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading diagnostics...</p>
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

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-white">
      <div className="max-w-7xl mx-auto">
        {/* ============================================================
        HEADER
        ============================================================ */}
        <div className="flex flex-wrap justify-between items-center mb-6 gap-4">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3">
              🧠 System Diagnostics
              <span className="text-xs font-normal text-gray-400 bg-gray-800 px-3 py-1 rounded-full">
                v6.0
              </span>
              {watchdogStatus?.running && (
                <span className="text-xs bg-green-500/20 text-green-500 px-3 py-1 rounded-full border border-green-500/30 animate-pulse">
                  ● LIVE
                </span>
              )}
            </h1>
            <p className="text-gray-400 text-sm mt-1">
              Complete system health, performance & watchdog monitoring • Last update: {lastUpdate || '--'}
            </p>
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            <button
              onClick={toggleAutoRefresh}
              className={`px-4 py-2 rounded-lg text-sm transition ${
                autoRefresh
                  ? 'bg-blue-600 hover:bg-blue-700'
                  : 'bg-gray-700 hover:bg-gray-600'
              }`}
            >
              {autoRefresh ? '⏸️ Auto Refresh' : '▶️ Manual'}
            </button>
            <button
              onClick={handleRefreshAll}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition text-sm"
            >
              🔄 Refresh All
            </button>
          </div>
        </div>

        {/* ============================================================
        ERROR DISPLAY
        ============================================================ */}
        {error && (
          <div className="bg-red-900/30 border border-red-500 rounded-lg p-4 mb-6">
            <p className="text-red-400">⚠️ {error}</p>
          </div>
        )}

        {/* ============================================================
        SECTION 1: SYSTEM METRICS
        ============================================================ */}
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          📊 System Metrics
          <span className="text-xs font-normal text-gray-400">
            Real-time performance data
          </span>
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">CPU Usage</div>
            <div className="text-2xl font-bold">
              {metrics?.cpu?.toFixed(1) || '0'}%
            </div>
            <div className="w-full bg-gray-700 rounded-full h-1.5 mt-2">
              <div
                className={`h-1.5 rounded-full transition-all ${
                  (metrics?.cpu || 0) > 80 ? 'bg-red-500' :
                  (metrics?.cpu || 0) > 60 ? 'bg-yellow-500' : 'bg-green-500'
                }`}
                style={{ width: `${Math.min(metrics?.cpu || 0, 100)}%` }}
              />
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">RAM Usage</div>
            <div className="text-2xl font-bold">
              {metrics?.ram?.toFixed(1) || '0'} GB
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {metrics?.ram_percent?.toFixed(0) || '0'}% used
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">Disk Usage</div>
            <div className="text-2xl font-bold">
              {metrics?.disk_percent?.toFixed(1) || '0'}%
            </div>
            <div className="w-full bg-gray-700 rounded-full h-1.5 mt-2">
              <div
                className={`h-1.5 rounded-full transition-all ${
                  (metrics?.disk_percent || 0) > 80 ? 'bg-red-500' :
                  (metrics?.disk_percent || 0) > 60 ? 'bg-yellow-500' : 'bg-green-500'
                }`}
                style={{ width: `${Math.min(metrics?.disk_percent || 0, 100)}%` }}
              />
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">Uptime</div>
            <div className="text-2xl font-bold text-green-500">
              {formatUptime(metrics?.uptime || 0)}
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">Health Score</div>
            <div className={`text-2xl font-bold ${getHealthScoreColor(metrics?.health_score || 0)}`}>
              {metrics?.health_score || 0}%
            </div>
            <div className="w-full bg-gray-700 rounded-full h-1.5 mt-2">
              <div
                className={`h-1.5 rounded-full transition-all ${getHealthBarColor(metrics?.health_score || 0)}`}
                style={{ width: `${Math.min(metrics?.health_score || 0, 100)}%` }}
              />
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">Knowledge</div>
            <div className="text-2xl font-bold">
              {metrics?.knowledge_count || 0}
            </div>
            <div className="text-xs text-gray-500 mt-1">items stored</div>
          </div>
        </div>

        {/* ============================================================
        SECTION 2: TRADING PERFORMANCE
        ============================================================ */}
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          📈 Trading Performance
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">Total PnL</div>
            <div className={`text-2xl font-bold ${(metrics?.pnl || 0) >= 0 ? 'text-green-500' : 'text-red-500'}`}>
              ${metrics?.pnl?.toFixed(2) || '0.00'}
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">Win Rate</div>
            <div className="text-2xl font-bold text-blue-500">
              {metrics?.win_rate?.toFixed(1) || '0'}%
            </div>
            <div className="w-full bg-gray-700 rounded-full h-1.5 mt-2">
              <div
                className="h-1.5 rounded-full bg-blue-500 transition-all"
                style={{ width: `${Math.min(metrics?.win_rate || 0, 100)}%` }}
              />
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">Total Trades</div>
            <div className="text-2xl font-bold">
              {metrics?.total_trades || 0}
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400 uppercase">Prediction Accuracy</div>
            <div className="text-2xl font-bold text-purple-500">
              {metrics?.prediction_accuracy?.toFixed(1) || '0'}%
            </div>
          </div>
        </div>

        {/* ============================================================
        SECTION 3: WATCHDOG DIAGNOSTICS
        ============================================================ */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            🛡️ Watchdog Diagnostics
            <span className="text-xs font-normal text-gray-400">
              Real-time component health monitoring
            </span>
          </h2>
          {watchdogStatus && (
            <span className={`px-3 py-1 rounded-lg text-sm ${
              watchdogStatus.running
                ? 'bg-green-500/20 text-green-500 border border-green-500/30'
                : 'bg-red-500/20 text-red-500 border border-red-500/30'
            }`}>
              {watchdogStatus.running ? '🟢 Active' : '🔴 Inactive'}
            </span>
          )}
        </div>

        {watchdogError ? (
          <div className="bg-yellow-900/30 border border-yellow-500 rounded-lg p-4 mb-6">
            <p className="text-yellow-400">⚠️ Watchdog: {watchdogError}</p>
            <p className="text-gray-400 text-sm mt-1">
              Make sure backend is running and components are registered.
            </p>
          </div>
        ) : (
          <>
            {/* Watchdog Summary Cards */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
              <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
                <div className="text-xs text-gray-400 uppercase">Components</div>
                <div className="text-2xl font-bold text-blue-500">{watchdogStatus?.components || 0}</div>
                <div className="text-xs text-gray-500 mt-1">
                  {watchdogStatus?.components_healthy || 0} healthy
                </div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
                <div className="text-xs text-gray-400 uppercase">Health Score</div>
                <div className={`text-2xl font-bold ${getHealthScoreColor(watchdogStatus?.health_score || 0)}`}>
                  {watchdogStatus?.health_score || 0}%
                </div>
                <div className="w-full bg-gray-700 rounded-full h-1.5 mt-2">
                  <div
                    className={`h-1.5 rounded-full transition-all ${getHealthBarColor(watchdogStatus?.health_score || 0)}`}
                    style={{ width: `${Math.min(watchdogStatus?.health_score || 0, 100)}%` }}
                  />
                </div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
                <div className="text-xs text-gray-400 uppercase">Checks</div>
                <div className="text-2xl font-bold text-yellow-500">{watchdogStatus?.checks || 0}</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
                <div className="text-xs text-gray-400 uppercase">Alerts</div>
                <div className={`text-2xl font-bold ${(watchdogStatus?.alerts || 0) > 0 ? 'text-red-500' : 'text-green-500'}`}>
                  {watchdogStatus?.alerts || 0}
                </div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
                <div className="text-xs text-gray-400 uppercase">Uptime</div>
                <div className="text-2xl font-bold text-green-500">
                  {formatUptime(watchdogStatus?.uptime_seconds || 0)}
                </div>
              </div>
            </div>

            {/* Component Selector & Detail */}
            {components.length > 0 && (
              <>
                <div className="flex flex-wrap gap-4 mb-6">
                  <div className="flex-1 min-w-[200px]">
                    <select
                      className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none transition"
                      value={selectedComponent}
                      onChange={(e) => handleComponentSelect(e.target.value)}
                    >
                      <option value="">Select Component</option>
                      {components.map((name) => {
                        const hb = heartbeats[name];
                        const status = hb?.status || 'unknown';
                        const health = componentHealth[name] || 0;
                        return (
                          <option key={name} value={name}>
                            {getStatusIcon(status)} {name} - {status} ({health}%)
                          </option>
                        );
                      })}
                    </select>
                  </div>
                  {componentDetail && (
                    <button
                      onClick={() => handleResetCircuit(selectedComponent)}
                      className="px-4 py-3 bg-red-600 hover:bg-red-700 rounded-lg transition text-sm font-medium"
                    >
                      🔄 Reset Circuit Breaker
                    </button>
                  )}
                </div>

                {/* Component Detail Cards */}
                {componentDetail && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <div className="bg-gray-800 p-5 rounded-lg border border-gray-700">
                      <h4 className="text-xs font-semibold text-gray-400 uppercase mb-3 flex items-center gap-2">
                        💓 Heartbeat
                        <span className={`px-2 py-0.5 rounded text-xs ${getStatusColor(componentDetail.heartbeat?.status)}`}>
                          {componentDetail.heartbeat?.status?.toUpperCase() || 'UNKNOWN'}
                        </span>
                      </h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Beats</span>
                          <span className="font-mono">{componentDetail.heartbeat?.beat_count || 0}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Missed</span>
                          <span className={`font-mono ${componentDetail.heartbeat?.missed_beats > 0 ? 'text-red-500' : ''}`}>
                            {componentDetail.heartbeat?.missed_beats || 0}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Restarts</span>
                          <span className={`font-mono ${componentDetail.heartbeat?.restart_count > 0 ? 'text-orange-500' : ''}`}>
                            {componentDetail.heartbeat?.restart_count || 0}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Health Score</span>
                          <span className={`font-mono ${getHealthScoreColor(componentDetail.heartbeat?.health_score || 0)}`}>
                            {componentDetail.heartbeat?.health_score || 0}%
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Last Beat</span>
                          <span className="font-mono text-xs">
                            {componentDetail.heartbeat?.last_beat
                              ? new Date(componentDetail.heartbeat.last_beat).toLocaleTimeString()
                              : 'Never'}
                          </span>
                        </div>
                        {componentDetail.heartbeat?.last_error && (
                          <div className="bg-red-900/20 p-2 rounded text-xs text-red-400 truncate">
                            Error: {componentDetail.heartbeat.last_error}
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="bg-gray-800 p-5 rounded-lg border border-gray-700">
                      <h4 className="text-xs font-semibold text-gray-400 uppercase mb-3 flex items-center gap-2">
                        📦 Component Info
                      </h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Name</span>
                          <span className="font-mono">{componentDetail.name}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Registered</span>
                          <span className={componentDetail.registered ? 'text-green-500' : 'text-red-500'}>
                            {componentDetail.registered ? '✅ Yes' : '❌ No'}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Health Score</span>
                          <span className={`font-mono ${getHealthScoreColor(componentDetail.health_score || 0)}`}>
                            {componentDetail.health_score || 0}%
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Dependencies</span>
                          <span className="font-mono text-xs">
                            {componentDetail.dependencies?.length > 0
                              ? componentDetail.dependencies.join(', ')
                              : 'None'}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="bg-gray-800 p-5 rounded-lg border border-gray-700">
                      <h4 className="text-xs font-semibold text-gray-400 uppercase mb-3 flex items-center gap-2">
                        ⚡ Actions
                      </h4>
                      <div className="space-y-3">
                        <button
                          onClick={() => handleResetCircuit(selectedComponent)}
                          className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition text-sm"
                        >
                          🔄 Reset Circuit Breaker
                        </button>
                        <button
                          onClick={() => {
                            fetchWatchdogData();
                            fetchComponentDetail(selectedComponent);
                          }}
                          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition text-sm"
                        >
                          🔍 Refresh Component
                        </button>
                      </div>
                    </div>
                  </div>
                )}

                {/* Components Table */}
                <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
                  <div className="px-5 py-4 border-b border-gray-700 flex justify-between items-center">
                    <h4 className="text-sm font-semibold text-gray-400 uppercase">
                      📊 All Components
                    </h4>
                    <span className="text-xs text-gray-500">{components.length} total</span>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-gray-900/50">
                        <tr>
                          <th className="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase">Component</th>
                          <th className="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase">Status</th>
                          <th className="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase">Health</th>
                          <th className="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase">Beats</th>
                          <th className="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase">Missed</th>
                          <th className="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase">Restarts</th>
                          <th className="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase">Last Beat</th>
                          <th className="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase">Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {components.map((name) => {
                          const hb = heartbeats[name] || { 
                            status: 'unknown', 
                            beat_count: 0, 
                            missed_beats: 0, 
                            restart_count: 0, 
                            last_beat: null 
                          };
                          const health = componentHealth[name] || 0;
                          const isSelected = name === selectedComponent;
                          return (
                            <tr
                              key={name}
                              className={`border-t border-gray-700/50 cursor-pointer transition hover:bg-gray-700/30 ${
                                isSelected ? 'bg-blue-900/20' : ''
                              }`}
                              onClick={() => handleComponentSelect(name)}
                            >
                              <td className="px-5 py-3 font-medium flex items-center gap-2">
                                {getStatusIcon(hb.status)}
                                {name}
                              </td>
                              <td className="px-5 py-3">
                                <span className={`px-2 py-1 rounded text-xs ${getStatusColor(hb.status)}`}>
                                  {hb.status?.toUpperCase() || 'UNKNOWN'}
                                </span>
                              </td>
                              <td className="px-5 py-3">
                                <span className={`font-mono ${getHealthScoreColor(health)}`}>
                                  {health}%
                                </span>
                                <div className="w-16 bg-gray-700 rounded-full h-1 mt-1">
                                  <div
                                    className={`h-1 rounded-full transition-all ${getHealthBarColor(health)}`}
                                    style={{ width: `${Math.min(health, 100)}%` }}
                                  />
                                </div>
                              </td>
                              <td className="px-5 py-3 font-mono">{hb.beat_count}</td>
                              <td className={`px-5 py-3 font-mono ${hb.missed_beats > 0 ? 'text-red-500' : ''}`}>
                                {hb.missed_beats}
                              </td>
                              <td className={`px-5 py-3 font-mono ${hb.restart_count > 0 ? 'text-orange-500' : ''}`}>
                                {hb.restart_count}
                              </td>
                              <td className="px-5 py-3 font-mono text-xs text-gray-400">
                                {hb.last_beat ? new Date(hb.last_beat).toLocaleTimeString() : 'Never'}
                              </td>
                              <td className="px-5 py-3">
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleResetCircuit(name);
                                  }}
                                  className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-xs transition"
                                >
                                  Reset
                                </button>
                              </td>
                            </tr>
                          );
                        })}
                        {components.length === 0 && (
                          <tr>
                            <td colSpan={8} className="px-5 py-8 text-center text-gray-500">
                              No components registered yet. Watchdog may be initializing.
                            </td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            )}
          </>
        )}

        {/* ============================================================
        FOOTER
        ============================================================ */}
        <div className="mt-8 text-center text-xs text-gray-600 border-t border-gray-800 pt-4">
          <p>
            Inkside Digital v6.0 • Diagnostics & Watchdog v3.1 REAL • 
            {watchdogStatus?.running ? ' 🟢 All systems operational' : ' 🔴 Monitoring inactive'}
          </p>
          <p className="mt-1">
            PID: {watchdogStatus?.pid || 'N/A'} • 
            Components: {watchdogStatus?.components || 0} • 
            Uptime: {formatUptime(watchdogStatus?.uptime_seconds || 0)} •
            Version: {watchdogStatus?.version || '--'}
          </p>
        </div>
      </div>
    </div>
  );
};


export { DiagnosticsView };
