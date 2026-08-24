// frontend/src/components/HealthView.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Activity, 
  ShieldCheck, 
  Cpu, 
  HardDrive, 
  CheckCircle2, 
  AlertTriangle, 
  RefreshCw,
  Heart,
  Zap,
  Clock,
  AlertCircle,
  Power,
  Server,
  Database,
  Network,
  Globe,
  MessageCircle,
  Brain,
  TrendingUp,
  BarChart3,
  Gauge,
  Timer,
  Shield,
  ShieldAlert,
  ShieldCheck as ShieldCheckIcon
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface HeartbeatData {
  status: string;
  beat_count: number;
  missed_beats: number;
  last_beat: string | null;
  restart_count: number;
  last_error?: string | null;
}

interface ComponentDetail {
  name: string;
  registered: boolean;
  heartbeat: HeartbeatData;
  dependencies: string[];
}

interface WatchdogStatus {
  running: boolean;
  components: number;
  checks: number;
  alerts: number;
  restarts: number;
  uptime_seconds: number;
  timestamp: string;
  pid?: number;
}

interface WatchdogSnapshot {
  status: WatchdogStatus;
  components: string[];
  heartbeats: Record<string, HeartbeatData>;
  timestamp: string;
}

interface SystemMetrics {
  cpu: number;
  ram: number;
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

// ============================================================
// MAIN COMPONENT
// ============================================================

export const HealthView: React.FC = () => {
  // ============================================================
  // STATE
  // ============================================================
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [autoRefresh, setAutoRefresh] = useState<boolean>(true);
  
  const [watchdogStatus, setWatchdogStatus] = useState<WatchdogStatus | null>(null);
  const [watchdogSnapshot, setWatchdogSnapshot] = useState<WatchdogSnapshot | null>(null);
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics | null>(null);
  const [selectedComponent, setSelectedComponent] = useState<string>('');
  const [componentDetail, setComponentDetail] = useState<ComponentDetail | null>(null);

  const API_BASE = import.meta.env.VITE_API_URL || 'http://45.41.204.21:5001';

  // ============================================================
  // FETCH DATA
  // ============================================================

  const fetchData = async () => {
    try {
      setError(null);
      
      const [watchdogStatusRes, watchdogSnapshotRes, metricsRes] = await Promise.all([
        axios.get(`${API_BASE}/api/watchdog/status`),
        axios.get(`${API_BASE}/api/watchdog/snapshot`),
        axios.get(`${API_BASE}/api/system/metrics`)
      ]);

      setWatchdogStatus(watchdogStatusRes.data);
      setWatchdogSnapshot(watchdogSnapshotRes.data);
      setSystemMetrics(metricsRes.data);
      setLastUpdate(new Date().toLocaleTimeString());

      const components = watchdogSnapshotRes.data?.components || [];
      if (components.length > 0 && !selectedComponent) {
        const firstComp = components[0];
        setSelectedComponent(firstComp);
        await fetchComponentDetail(firstComp);
      }

      setLoading(false);
    } catch (err: any) {
      console.error('Failed to fetch health data:', err);
      setError(err.message || 'Failed to connect to API');
      setLoading(false);
    }
  };

  const fetchComponentDetail = async (name: string) => {
    try {
      const res = await axios.get(`${API_BASE}/api/watchdog/component/${name}`);
      setComponentDetail(res.data);
    } catch (err: any) {
      console.error('Failed to fetch component detail:', err);
    }
  };

  // ============================================================
  // EFFECTS
  // ============================================================

  useEffect(() => {
    fetchData();
    
    let interval: NodeJS.Timeout;
    if (autoRefresh) {
      interval = setInterval(fetchData, 5000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  // ============================================================
  // HANDLERS
  // ============================================================

  const handleComponentSelect = async (name: string) => {
    setSelectedComponent(name);
    await fetchComponentDetail(name);
  };

  const handleResetCircuit = async (name: string) => {
    try {
      await axios.post(`${API_BASE}/api/watchdog/circuit/${name}/reset`);
      await fetchData();
      await fetchComponentDetail(name);
    } catch (err) {
      console.error('Failed to reset circuit:', err);
    }
  };

  // ============================================================
  // UTILITY FUNCTIONS
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
    if (['alive', 'healthy', 'online', 'ok'].includes(s)) {
      return 'text-green-500 bg-green-500/10 border-green-500/20';
    }
    if (['error', 'dead', 'offline', 'critical'].includes(s)) {
      return 'text-red-500 bg-red-500/10 border-red-500/20';
    }
    if (['warning', 'degraded', 'idle'].includes(s)) {
      return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20';
    }
    return 'text-gray-500 bg-gray-500/10 border-gray-500/20';
  };

  const getStatusIcon = (status: string): React.ReactNode => {
    const s = status?.toLowerCase() || '';
    if (['alive', 'healthy', 'online', 'ok'].includes(s)) {
      return <CheckCircle2 className="w-4 h-4 text-green-500" />;
    }
    if (['error', 'dead', 'offline', 'critical'].includes(s)) {
      return <AlertTriangle className="w-4 h-4 text-red-500" />;
    }
    if (['warning', 'degraded', 'idle'].includes(s)) {
      return <AlertCircle className="w-4 h-4 text-yellow-500" />;
    }
    return <Activity className="w-4 h-4 text-gray-500" />;
  };

  const getHealthScoreColor = (score: number): string => {
    if (score >= 80) return 'text-green-500';
    if (score >= 60) return 'text-yellow-500';
    if (score >= 40) return 'text-orange-500';
    return 'text-red-500';
  };

  const getHealthScoreLabel = (score: number): string => {
    if (score >= 80) return 'EXCELLENT';
    if (score >= 60) return 'GOOD';
    if (score >= 40) return 'FAIR';
    return 'CRITICAL';
  };

  const getRiskLevelColor = (level: string): string => {
    const l = level?.toUpperCase() || '';
    if (l === 'LOW') return 'text-green-500 bg-green-500/10 border-green-500/20';
    if (l === 'MODERATE') return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20';
    if (l === 'HIGH') return 'text-orange-500 bg-orange-500/10 border-orange-500/20';
    if (l === 'CRITICAL') return 'text-red-500 bg-red-500/10 border-red-500/20';
    return 'text-gray-500 bg-gray-500/10 border-gray-500/20';
  };

  // ============================================================
  // LOADING STATE
  // ============================================================

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 bg-[#0B0F14]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-[#8D9AAA]">Loading health diagnostics...</p>
        </div>
      </div>
    );
  }

  // ============================================================
  // RENDER
  // ============================================================

  const components = watchdogSnapshot?.components || [];
  const heartbeats = watchdogSnapshot?.heartbeats || {};
  const metrics = systemMetrics;

  return (
    <div id="health-view" className="space-y-6 pb-12">
      {/* ============================================================
          HEADER BANNER
          ============================================================ */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-rose-600/20 border border-rose-500/30 flex items-center justify-center text-rose-400">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              🛡️ System Health & Watchdog Diagnostics
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Real-time Subsystem Latency, Process Heartbeat & Circuit Breaker Monitoring • 
              <span className="text-emerald-400 ml-1">
                {watchdogStatus?.running ? '🟢 Active' : '🔴 Inactive'}
              </span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`px-3 py-1.5 rounded-lg text-xs transition ${
              autoRefresh
                ? 'bg-blue-600 hover:bg-blue-700'
                : 'bg-[#1A2530] hover:bg-[#26313D]'
            }`}
          >
            {autoRefresh ? '⏸️ Auto' : '▶️ Manual'}
          </button>
          <button
            onClick={fetchData}
            className="px-3 py-1.5 bg-[#1A2530] hover:bg-[#26313D] rounded-lg transition text-xs flex items-center gap-1"
          >
            <RefreshCw className="w-3 h-3" />
            Refresh
          </button>
          <div className="px-4 py-2 rounded-xl bg-[#0B0F14] border border-emerald-500/30 text-right">
            <span className="text-[10px] text-[#5F6B78] font-bold block uppercase">Health Score</span>
            <span className={`text-base font-black font-mono ${getHealthScoreColor(metrics?.health_score || 0)}`}>
              {metrics?.health_score || 0}% ({getHealthScoreLabel(metrics?.health_score || 0)})
            </span>
          </div>
          <div className="px-4 py-2 rounded-xl bg-[#0B0F14] border border-emerald-500/30 text-right">
            <span className="text-[10px] text-[#5F6B78] font-bold block uppercase">Risk Level</span>
            <span className={`text-base font-black font-mono ${getRiskLevelColor(metrics?.risk_level || '--')}`}>
              {metrics?.risk_level || '--'}
            </span>
          </div>
        </div>
      </div>

      {/* ============================================================
          ERROR DISPLAY
          ============================================================ */}
      {error && (
        <div className="bg-red-900/30 border border-red-500 rounded-lg p-4">
          <p className="text-red-400">⚠️ {error}</p>
        </div>
      )}

      {/* ============================================================
          METRICS ROW - REAL DATA
          ============================================================ */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5 font-mono">
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] text-[#8D9AAA] font-bold uppercase block font-sans flex items-center gap-1">
            <Server className="w-3 h-3" />
            Active Services
          </span>
          <div className="text-xl font-black text-white mt-1">
            {watchdogStatus?.components || 0}
          </div>
          <span className="text-[10px] text-emerald-400 font-bold">
            {watchdogStatus?.running ? '🟢 Online' : '🔴 Offline'}
          </span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] text-[#8D9AAA] font-bold uppercase block font-sans flex items-center gap-1">
            <Shield className="w-3 h-3" />
            Circuit Breaker
          </span>
          <div className="text-xl font-black text-emerald-400 mt-1">
            {watchdogStatus?.alerts && watchdogStatus.alerts > 0 ? (
              <span className="text-yellow-500">{watchdogStatus.alerts} Alerts</span>
            ) : (
              'CLOSED'
            )}
          </div>
          <span className="text-[10px] text-[#5F6B78]">
            {watchdogStatus?.alerts || 0} Tripped
          </span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] text-[#8D9AAA] font-bold uppercase block font-sans flex items-center gap-1">
            <Timer className="w-3 h-3" />
            Watchdog Uptime
          </span>
          <div className="text-xl font-black text-cyan-400 mt-1">
            {formatUptime(watchdogStatus?.uptime_seconds || 0)}
          </div>
          <span className="text-[10px] text-emerald-400">Monitoring Active</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] text-[#8D9AAA] font-bold uppercase block font-sans flex items-center gap-1">
            <Gauge className="w-3 h-3" />
            System Health
          </span>
          <div className={`text-xl font-black mt-1 ${getHealthScoreColor(metrics?.health_score || 0)}`}>
            {metrics?.health_score || 0}%
          </div>
          <span className="text-[10px] text-[#5F6B78]">
            {getHealthScoreLabel(metrics?.health_score || 0)}
          </span>
        </div>
      </div>

      {/* ============================================================
          SYSTEM METRICS - REAL DATA
          ============================================================ */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5">
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-[#8D9AAA] font-bold uppercase font-sans">CPU</span>
            <Cpu className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-black text-white mt-1">{metrics?.cpu?.toFixed(1) || 0}%</div>
          <div className="w-full bg-[#1A2530] rounded-full h-1.5 mt-2">
            <div
              className={`h-1.5 rounded-full transition-all ${
                (metrics?.cpu || 0) > 80 ? 'bg-red-500' :
                (metrics?.cpu || 0) > 60 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${Math.min(metrics?.cpu || 0, 100)}%` }}
            />
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-[#8D9AAA] font-bold uppercase font-sans">RAM</span>
            <HardDrive className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-xl font-black text-white mt-1">{metrics?.ram?.toFixed(1) || 0} GB</div>
          <span className="text-[10px] text-[#5F6B78]">Total: {((metrics?.ram || 0) * 2).toFixed(1)} GB</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-[#8D9AAA] font-bold uppercase font-sans">System Uptime</span>
            <Clock className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-xl font-black text-emerald-400 mt-1">
            {formatUptime(metrics?.uptime || 0)}
          </div>
          <span className="text-[10px] text-[#5F6B78]">Since startup</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-[#8D9AAA] font-bold uppercase font-sans">Open Positions</span>
            <BarChart3 className="w-4 h-4 text-orange-400" />
          </div>
          <div className="text-xl font-black text-white mt-1">{metrics?.open_positions || 0}</div>
          <span className="text-[10px] text-[#5F6B78]">
            Win Rate: {metrics?.win_rate?.toFixed(1) || 0}%
          </span>
        </div>
      </div>

      {/* ============================================================
          COMPONENT SELECTOR
          ============================================================ */}
      {components.length > 0 && (
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
          <div className="flex flex-wrap items-center gap-4 mb-4">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <Heart className="w-4 h-4 text-rose-400" />
              Core Subsystems Health Status ({components.length})
            </h3>
            <div className="flex-1 min-w-[200px]">
              <select
                className="w-full bg-[#1A2530] text-white px-4 py-2 rounded-xl border border-[#26313D] focus:border-blue-500 focus:outline-none transition text-sm"
                value={selectedComponent}
                onChange={(e) => handleComponentSelect(e.target.value)}
              >
                <option value="">Select Component</option>
                {components.map((name) => {
                  const hb = heartbeats[name];
                  const status = hb?.status || 'unknown';
                  return (
                    <option key={name} value={name}>
                      {status === 'alive' ? '🟢' : '🔴'} {name} - {status}
                    </option>
                  );
                })}
              </select>
            </div>
            {componentDetail && (
              <button
                onClick={() => handleResetCircuit(selectedComponent)}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-xl transition text-sm font-medium flex items-center gap-2"
              >
                <ShieldAlert className="w-4 h-4" />
                Reset Circuit
              </button>
            )}
          </div>

          {/* Component Detail Cards */}
          {componentDetail && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
                <h4 className="text-xs font-semibold text-[#8D9AAA] uppercase mb-3 flex items-center gap-2">
                  <Heart className="w-4 h-4 text-rose-400" />
                  Heartbeat
                  <span className={`px-2 py-0.5 rounded text-xs ${getStatusColor(componentDetail.heartbeat?.status)}`}>
                    {componentDetail.heartbeat?.status || 'UNKNOWN'}
                  </span>
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">Beats</span>
                    <span className="font-mono text-white">{componentDetail.heartbeat?.beat_count || 0}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">Missed</span>
                    <span className={`font-mono ${componentDetail.heartbeat?.missed_beats > 0 ? 'text-red-500' : 'text-white'}`}>
                      {componentDetail.heartbeat?.missed_beats || 0}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">Restarts</span>
                    <span className={`font-mono ${componentDetail.heartbeat?.restart_count > 0 ? 'text-orange-500' : 'text-white'}`}>
                      {componentDetail.heartbeat?.restart_count || 0}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">Last Beat</span>
                    <span className="font-mono text-xs text-[#8D9AAA]">
                      {componentDetail.heartbeat?.last_beat
                        ? new Date(componentDetail.heartbeat.last_beat).toLocaleTimeString()
                        : 'Never'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
                <h4 className="text-xs font-semibold text-[#8D9AAA] uppercase mb-3 flex items-center gap-2">
                  <Server className="w-4 h-4 text-blue-400" />
                  Component Info
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">Name</span>
                    <span className="font-mono text-white">{componentDetail.name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">Registered</span>
                    <span className={componentDetail.registered ? 'text-green-500' : 'text-red-500'}>
                      {componentDetail.registered ? '✅ Yes' : '❌ No'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">Dependencies</span>
                    <span className="font-mono text-xs text-[#8D9AAA]">
                      {componentDetail.dependencies?.length > 0
                        ? componentDetail.dependencies.join(', ')
                        : 'None'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
                <h4 className="text-xs font-semibold text-[#8D9AAA] uppercase mb-3 flex items-center gap-2">
                  <Zap className="w-4 h-4 text-yellow-400" />
                  Quick Actions
                </h4>
                <div className="space-y-2">
                  <button
                    onClick={() => handleResetCircuit(selectedComponent)}
                    className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition text-sm flex items-center justify-center gap-2"
                  >
                    <ShieldAlert className="w-4 h-4" />
                    Reset Circuit Breaker
                  </button>
                  <button
                    onClick={() => {
                      fetchData();
                      fetchComponentDetail(selectedComponent);
                    }}
                    className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition text-sm flex items-center justify-center gap-2"
                  >
                    <RefreshCw className="w-4 h-4" />
                    Refresh Component
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Components Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-[#0B0F14]">
                <tr>
                  <th className="px-4 py-3 text-left text-[10px] font-bold text-[#8D9AAA] uppercase">Component</th>
                  <th className="px-4 py-3 text-left text-[10px] font-bold text-[#8D9AAA] uppercase">Status</th>
                  <th className="px-4 py-3 text-left text-[10px] font-bold text-[#8D9AAA] uppercase">Beats</th>
                  <th className="px-4 py-3 text-left text-[10px] font-bold text-[#8D9AAA] uppercase">Missed</th>
                  <th className="px-4 py-3 text-left text-[10px] font-bold text-[#8D9AAA] uppercase">Restarts</th>
                  <th className="px-4 py-3 text-left text-[10px] font-bold text-[#8D9AAA] uppercase">Last Beat</th>
                  <th className="px-4 py-3 text-left text-[10px] font-bold text-[#8D9AAA] uppercase">Action</th>
                </tr>
              </thead>
              <tbody>
                {components.map((name) => {
                  const hb = heartbeats[name] || { status: 'unknown', beat_count: 0, missed_beats: 0, restart_count: 0, last_beat: null };
                  const isSelected = name === selectedComponent;
                  return (
                    <tr
                      key={name}
                      className={`border-t border-[#26313D] cursor-pointer transition hover:bg-[#1A2530] ${
                        isSelected ? 'bg-[#1A2530]' : ''
                      }`}
                      onClick={() => handleComponentSelect(name)}
                    >
                      <td className="px-4 py-3 font-medium text-white flex items-center gap-2">
                        {getStatusIcon(hb.status)}
                        {name}
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded text-[10px] font-bold ${getStatusColor(hb.status)}`}>
                          {hb.status?.toUpperCase() || 'UNKNOWN'}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-mono text-white">{hb.beat_count}</td>
                      <td className={`px-4 py-3 font-mono ${hb.missed_beats > 0 ? 'text-red-500' : 'text-white'}`}>
                        {hb.missed_beats}
                      </td>
                      <td className={`px-4 py-3 font-mono ${hb.restart_count > 0 ? 'text-orange-500' : 'text-white'}`}>
                        {hb.restart_count}
                      </td>
                      <td className="px-4 py-3 font-mono text-xs text-[#8D9AAA]">
                        {hb.last_beat ? new Date(hb.last_beat).toLocaleTimeString() : 'Never'}
                      </td>
                      <td className="px-4 py-3">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleResetCircuit(name);
                          }}
                          className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded-lg text-xs transition"
                        >
                          Reset
                        </button>
                      </td>
                    </tr>
                  );
                })}
                {components.length === 0 && (
                  <tr>
                    <td colSpan={7} className="px-4 py-8 text-center text-[#5F6B78]">
                      No components registered yet. Start the bot to register components.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ============================================================
          FOOTER
          ============================================================ */}
      <div className="text-center text-[10px] text-[#5F6B78] border-t border-[#1A2530] pt-4">
        <p>
          Health & Watchdog v3.0 REAL • 
          {watchdogStatus?.running ? ' 🟢 Monitoring Active' : ' 🔴 Monitoring Inactive'} • 
          Last update: {lastUpdate} • 
          PID: {watchdogStatus?.pid || 'N/A'}
        </p>
      </div>
    </div>
  );
};
