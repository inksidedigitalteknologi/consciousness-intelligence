// src/components/HealthView.tsx
// INKSIDE DIGITAL - HEALTH VIEW v4.0
// SUPER ADVANCED - REAL-TIME DASHBOARD

import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import {
  Activity, ShieldCheck, Cpu, HardDrive, CheckCircle2, AlertTriangle,
  RefreshCw, Heart, Zap, Clock, AlertCircle, Server, Database,
  Network, Wifi, WifiOff, Loader2, ChevronDown, ChevronRight,
  Search, Filter, X, Gauge, Timer, Shield, TrendingUp, Eye, EyeOff,
  Bell, BellRing, TrendingDown, ArrowUp, ArrowDown, Minus,
  BarChart3, LineChart, PieChart, Sparkles, Award, Target, Compass
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface HealthMetric {
  name: string;
  status: 'healthy' | 'warning' | 'error' | 'unknown';
  message?: string;
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'stable';
  value?: string | number;
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
  last_update?: string;
}

interface HealthHistory {
  timestamp: string;
  health_score: number;
  cpu: number;
  ram: number;
}

interface Alert {
  id: string;
  type: 'info' | 'warning' | 'error' | 'success';
  message: string;
  timestamp: string;
  read: boolean;
}

interface HealthViewProps {
  wsConnected?: boolean;
}

// ============================================================
// API CONFIG
// ============================================================

const API_KEY = 'iks_612d40ce554b1670525355c85567f823';
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
  if (['healthy', 'online', 'ok', 'running'].includes(s)) return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
  if (['warning', 'degraded', 'idle'].includes(s)) return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
  if (['error', 'offline', 'critical', 'stopped'].includes(s)) return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
  return 'text-gray-400 bg-gray-500/10 border-gray-500/20';
};

const getStatusIcon = (status: string) => {
  const s = status?.toLowerCase() || '';
  if (['healthy', 'online', 'ok', 'running'].includes(s)) return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
  if (['warning', 'degraded', 'idle'].includes(s)) return <AlertTriangle className="w-4 h-4 text-amber-400" />;
  if (['error', 'offline', 'critical', 'stopped'].includes(s)) return <AlertCircle className="w-4 h-4 text-rose-400" />;
  return <Activity className="w-4 h-4 text-gray-400" />;
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

const getHealthLabel = (score: number): { label: string; emoji: string } => {
  if (score >= 90) return { label: 'Excellent', emoji: '🌟' };
  if (score >= 80) return { label: 'Great', emoji: '💪' };
  if (score >= 70) return { label: 'Good', emoji: '👍' };
  if (score >= 60) return { label: 'Fair', emoji: '🤔' };
  if (score >= 40) return { label: 'Poor', emoji: '😟' };
  return { label: 'Critical', emoji: '🚨' };
};

// ============================================================
// ANIMATED COUNTER
// ============================================================

const AnimatedCounter: React.FC<{ value: number; duration?: number; suffix?: string; prefix?: string }> = ({
  value,
  duration = 1000,
  suffix = '',
  prefix = ''
}) => {
  const [count, setCount] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    setIsAnimating(true);
    const startTime = Date.now();
    const startValue = count;
    const endValue = value;
    const diff = endValue - startValue;

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = startValue + diff * eased;
      setCount(current);

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        setCount(endValue);
        setIsAnimating(false);
      }
    };

    requestAnimationFrame(animate);
  }, [value, duration]);

  return (
    <span className={isAnimating ? 'text-emerald-400 transition-colors' : ''}>
      {prefix}{Math.round(count)}{suffix}
    </span>
  );
};

// ============================================================
// MINI CHART
// ============================================================

const MiniChart: React.FC<{ data: number[]; color?: string; height?: number }> = ({
  data,
  color = '#10B981',
  height = 40
}) => {
  if (!data || data.length < 2) return null;
  
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const points = data.map((v, i) => ({
    x: (i / (data.length - 1)) * 100,
    y: 100 - ((v - min) / range) * 100
  }));

  const path = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');

  return (
    <svg width="100%" height={height} className="overflow-visible">
      <path
        d={path}
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="opacity-80"
      />
      <path
        d={`${path} L ${points[points.length - 1].x} 100 L ${points[0].x} 100 Z`}
        fill={color}
        opacity="0.1"
      />
    </svg>
  );
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const HealthView: React.FC<HealthViewProps> = ({ wsConnected = false }) => {
  // ===== STATE =====
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [healthData, setHealthData] = useState<HealthMetric[]>([]);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [showAlerts, setShowAlerts] = useState(false);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [history, setHistory] = useState<HealthHistory[]>([]);
  const [expanded, setExpanded] = useState(true);

  // ===== FETCH FUNCTIONS =====
  const fetchWithAuth = useCallback(async (endpoint: string) => {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'X-API-Key': localStorage.getItem('apiKey') || API_KEY }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }, []);

  const fetchHealthData = useCallback(async () => {
    try {
      const [healthRes, metricsRes] = await Promise.all([
        fetchWithAuth('/api/health'),
        fetchWithAuth('/api/system/metrics')
      ]);

      setMetrics(metricsRes);

      const metricsList: HealthMetric[] = [
        { 
          name: 'API Server', 
          status: healthRes.status === 'healthy' ? 'healthy' : 'warning',
          icon: <Server className="w-4 h-4" />,
          value: 'v' + (healthRes.version || '1.0')
        },
        { 
          name: 'Knowledge Engine', 
          status: healthRes.knowledge_items > 0 ? 'healthy' : 'warning',
          message: `${healthRes.knowledge_items} items`,
          icon: <Database className="w-4 h-4" />
        },
        { 
          name: 'Dividend Module', 
          status: healthRes.dividend_available ? 'healthy' : 'warning',
          icon: <Activity className="w-4 h-4" />
        },
        { 
          name: 'AI Engine', 
          status: healthRes.ai_enabled ? 'healthy' : 'warning',
          icon: <Sparkles className="w-4 h-4" />,
          value: healthRes.ai_enabled ? 'ON' : 'OFF'
        },
        { 
          name: 'Database', 
          status: 'healthy',
          icon: <HardDrive className="w-4 h-4" />
        },
        { 
          name: 'Memory', 
          status: 'healthy',
          icon: <Cpu className="w-4 h-4" />,
          value: `${metricsRes.ram_percent?.toFixed(0) || 0}%`
        },
        { 
          name: 'Cache', 
          status: 'healthy',
          icon: <Zap className="w-4 h-4" />
        },
        { 
          name: 'WebSocket', 
          status: wsConnected ? 'healthy' : 'warning',
          icon: wsConnected ? <Wifi className="w-4 h-4" /> : <WifiOff className="w-4 h-4" />
        },
      ];

      setHealthData(metricsList);
      setLastUpdate(new Date().toLocaleTimeString());

      // Add to history
      setHistory(prev => {
        const newEntry = {
          timestamp: new Date().toLocaleTimeString(),
          health_score: metricsRes.health_score || 0,
          cpu: metricsRes.cpu || 0,
          ram: metricsRes.ram_percent || 0
        };
        const newHistory = [...prev, newEntry];
        return newHistory.slice(-20);
      });

      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch health data');
      
      // Add alert
      setAlerts(prev => [{
        id: Date.now().toString(),
        type: 'error',
        message: err instanceof Error ? err.message : 'Failed to fetch health data',
        timestamp: new Date().toLocaleTimeString(),
        read: false
      }, ...prev].slice(0, 20));
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  }, [fetchWithAuth, wsConnected]);

  const handleRefresh = useCallback(async () => {
    setIsRefreshing(true);
    await fetchHealthData();
  }, [fetchHealthData]);

  // ===== EFFECTS =====
  useEffect(() => {
    fetchHealthData();
    const interval = setInterval(fetchHealthData, 15000);
    return () => clearInterval(interval);
  }, [fetchHealthData]);

  // ===== MEMOIZED =====
  const healthScore = metrics?.health_score || 0;
  const healthLabel = getHealthLabel(healthScore);
  const healthHistory = useMemo(() => history.map(h => h.health_score), [history]);
  const cpuHistory = useMemo(() => history.map(h => h.cpu), [history]);
  const ramHistory = useMemo(() => history.map(h => h.ram), [history]);

  const unreadAlerts = alerts.filter(a => !a.read).length;

  // ===== LOADING =====
  if (loading) {
    return (
      <div className="flex items-center justify-center h-96 bg-[#0B0F14]">
        <div className="text-center">
          <div className="relative">
            <div className="w-20 h-20 border-4 border-emerald-500/20 border-t-emerald-500 rounded-full animate-spin" />
            <Heart className="w-8 h-8 text-emerald-400 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse" />
          </div>
          <p className="text-[#8D9AAA] mt-4 text-sm font-medium">Loading Health Dashboard...</p>
          <p className="text-[#5F6B78] text-xs mt-1">Fetching real-time system status</p>
        </div>
      </div>
    );
  }

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="p-4 md:p-6 bg-[#0B0F14] min-h-screen">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* ===== HEADER ===== */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#131A22] via-[#1A2530] to-[#131A22] border border-[#26313D] p-6">
          {/* Background Decor */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/4" />
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-blue-500/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/4" />
          
          <div className="relative flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-600/30 to-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
                  <Heart className="w-7 h-7 text-emerald-400" />
                </div>
                <div className={`absolute -top-1 -right-1 w-4 h-4 rounded-full ${metrics?.health_score >= 70 ? 'bg-emerald-500' : 'bg-amber-500'} animate-pulse border-2 border-[#0B0F14]`} />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                  🛡️ System Health
                  <span className={`text-xs font-bold px-3 py-1 rounded-full ${error ? 'bg-rose-500/20 text-rose-400' : 'bg-emerald-500/20 text-emerald-400'} border ${error ? 'border-rose-500/30' : 'border-emerald-500/30'}`}>
                    {error ? '⚠️ Error' : '🟢 Live'}
                  </span>
                </h1>
                <p className="text-sm text-[#8D9AAA] flex items-center gap-3">
                  <span>Real-time monitoring & component status</span>
                  <span className="w-1 h-1 rounded-full bg-[#26313D]" />
                  <span className="flex items-center gap-1">
                    {wsConnected ? <Wifi className="w-3.5 h-3.5 text-emerald-400" /> : <WifiOff className="w-3.5 h-3.5 text-amber-400" />}
                    {wsConnected ? 'Connected' : 'Disconnected'}
                  </span>
                  <span className="w-1 h-1 rounded-full bg-[#26313D]" />
                  <span className="text-[#5F6B78]">v4.0</span>
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {/* Alert Bell */}
              <button
                onClick={() => setShowAlerts(!showAlerts)}
                className="relative p-2.5 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] border border-[#26313D] transition-all hover:border-emerald-500/30"
              >
                {unreadAlerts > 0 ? (
                  <BellRing className="w-4 h-4 text-amber-400" />
                ) : (
                  <Bell className="w-4 h-4 text-[#8D9AAA]" />
                )}
                {unreadAlerts > 0 && (
                  <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-rose-500 text-[9px] font-bold text-white flex items-center justify-center border-2 border-[#0B0F14]">
                    {unreadAlerts}
                  </span>
                )}
              </button>

              <button
                onClick={handleRefresh}
                disabled={isRefreshing}
                className="p-2.5 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] border border-[#26313D] transition-all hover:border-emerald-500/30 disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 text-[#8D9AAA] ${isRefreshing ? 'animate-spin' : ''}`} />
              </button>

              <button
                onClick={() => setExpanded(!expanded)}
                className="p-2.5 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] border border-[#26313D] transition-all hover:border-emerald-500/30"
              >
                {expanded ? <EyeOff className="w-4 h-4 text-[#8D9AAA]" /> : <Eye className="w-4 h-4 text-[#8D9AAA]" />}
              </button>
            </div>
          </div>

          {/* Error Banner */}
          {error && (
            <div className="relative mt-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm flex items-center gap-3">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <span>{error}</span>
              <button onClick={handleRefresh} className="ml-auto px-3 py-1 bg-rose-500/20 hover:bg-rose-500/30 rounded-lg text-xs transition-colors">
                Retry
              </button>
            </div>
          )}

          {/* Alerts Panel */}
          {showAlerts && alerts.length > 0 && (
            <div className="relative mt-4 p-4 rounded-xl bg-[#0B0F14] border border-[#26313D] max-h-48 overflow-y-auto space-y-2">
              <div className="flex items-center justify-between sticky top-0 bg-[#0B0F14] pb-2 border-b border-[#26313D]/50">
                <span className="text-xs font-bold text-white">🔔 Alerts</span>
                <button onClick={() => setAlerts([])} className="text-[10px] text-[#5F6B78] hover:text-white transition-colors">
                  Clear All
                </button>
              </div>
              {alerts.map(alert => (
                <div key={alert.id} className={`p-2 rounded-lg flex items-start gap-2 text-xs ${alert.type === 'error' ? 'bg-rose-500/10 border border-rose-500/20' : alert.type === 'warning' ? 'bg-amber-500/10 border border-amber-500/20' : 'bg-emerald-500/10 border border-emerald-500/20'}`}>
                  {alert.type === 'error' ? <AlertCircle className="w-3.5 h-3.5 text-rose-400 flex-shrink-0 mt-0.5" /> : alert.type === 'warning' ? <AlertTriangle className="w-3.5 h-3.5 text-amber-400 flex-shrink-0 mt-0.5" /> : <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />}
                  <span className="flex-1 text-[#E8EDF2]">{alert.message}</span>
                  <span className="text-[#5F6B78] flex-shrink-0">{alert.timestamp}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ===== MAIN METRICS GRID ===== */}
        {metrics && (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3.5">
            {/* Health Score */}
            <div className="relative overflow-hidden p-4 rounded-2xl bg-gradient-to-br from-[#131A22] to-[#1A2530] border border-[#26313D] group hover:border-emerald-500/30 transition-all duration-300">
              <div className="absolute top-0 right-0 w-20 h-20 bg-emerald-500/5 rounded-full blur-2xl -translate-y-1/2 translate-x-1/4" />
              <div className="relative">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] uppercase font-bold text-[#8D9AAA] tracking-wider">Health</span>
                  <span className="text-lg">{healthLabel.emoji}</span>
                </div>
                <div className="mt-1 flex items-end gap-2">
                  <span className={`text-3xl font-black font-mono ${getHealthScoreColor(healthScore)}`}>
                    <AnimatedCounter value={healthScore} suffix="%" />
                  </span>
                  <span className="text-xs text-[#5F6B78] font-medium pb-1">{healthLabel.label}</span>
                </div>
                <div className="mt-2 w-full h-1.5 rounded-full bg-[#1A2530] overflow-hidden">
                  <div className={`h-full rounded-full transition-all duration-1000 ${getHealthBarColor(healthScore)}`} style={{ width: `${Math.min(healthScore, 100)}%` }} />
                </div>
                <div className="mt-1.5 flex items-center gap-2 text-[9px] text-[#5F6B78]">
                  <span>▲ {history.length > 1 && healthScore > (history[history.length-2]?.health_score || 0) ? `${((healthScore - (history[history.length-2]?.health_score || 0))).toFixed(1)}%` : 'stable'}</span>
                  <span className="w-1 h-1 rounded-full bg-[#26313D]" />
                  <span>{formatUptime(metrics.uptime)}</span>
                </div>
              </div>
            </div>

            {/* CPU */}
            <div className="relative overflow-hidden p-4 rounded-2xl bg-[#131A22] border border-[#26313D] group hover:border-blue-500/30 transition-all duration-300">
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-[#8D9AAA] tracking-wider">CPU</span>
                <Cpu className="w-4 h-4 text-blue-400" />
              </div>
              <div className="mt-1">
                <span className="text-3xl font-black font-mono text-white">{metrics.cpu?.toFixed(1) || 0}<span className="text-lg">%</span></span>
              </div>
              <div className="mt-2 w-full h-1.5 rounded-full bg-[#1A2530] overflow-hidden">
                <div className={`h-full rounded-full transition-all duration-1000 ${metrics.cpu > 80 ? 'bg-rose-500' : metrics.cpu > 60 ? 'bg-amber-500' : 'bg-blue-500'}`} style={{ width: `${Math.min(metrics.cpu || 0, 100)}%` }} />
              </div>
              {cpuHistory.length > 1 && <MiniChart data={cpuHistory} color={metrics.cpu > 80 ? '#EF4444' : metrics.cpu > 60 ? '#F59E0B' : '#3B82F6'} height={30} />}
            </div>

            {/* Memory */}
            <div className="relative overflow-hidden p-4 rounded-2xl bg-[#131A22] border border-[#26313D] group hover:border-purple-500/30 transition-all duration-300">
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-[#8D9AAA] tracking-wider">Memory</span>
                <Activity className="w-4 h-4 text-purple-400" />
              </div>
              <div className="mt-1">
                <span className="text-3xl font-black font-mono text-white">{metrics.ram_percent?.toFixed(0) || 0}<span className="text-lg">%</span></span>
              </div>
              <div className="mt-2 w-full h-1.5 rounded-full bg-[#1A2530] overflow-hidden">
                <div className={`h-full rounded-full transition-all duration-1000 ${metrics.ram_percent > 80 ? 'bg-rose-500' : metrics.ram_percent > 60 ? 'bg-amber-500' : 'bg-purple-500'}`} style={{ width: `${Math.min(metrics.ram_percent || 0, 100)}%` }} />
              </div>
              <div className="mt-1 text-[9px] text-[#5F6B78]">{metrics.ram?.toFixed(1) || 0} GB used</div>
            </div>

            {/* Uptime */}
            <div className="relative overflow-hidden p-4 rounded-2xl bg-[#131A22] border border-[#26313D] group hover:border-cyan-500/30 transition-all duration-300">
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-[#8D9AAA] tracking-wider">Uptime</span>
                <Clock className="w-4 h-4 text-cyan-400" />
              </div>
              <div className="mt-1">
                <span className="text-2xl font-black font-mono text-cyan-400">{formatUptime(metrics.uptime || 0)}</span>
              </div>
              <div className="mt-1 text-[9px] text-[#5F6B78]">System running</div>
              <div className="mt-1 flex items-center gap-1 text-[9px] text-[#5F6B78]">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                <span>Active</span>
              </div>
            </div>

            {/* Disk */}
            <div className="relative overflow-hidden p-4 rounded-2xl bg-[#131A22] border border-[#26313D] group hover:border-orange-500/30 transition-all duration-300">
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-[#8D9AAA] tracking-wider">Disk</span>
                <HardDrive className="w-4 h-4 text-orange-400" />
              </div>
              <div className="mt-1">
                <span className="text-3xl font-black font-mono text-white">{metrics.disk_percent?.toFixed(0) || 0}<span className="text-lg">%</span></span>
              </div>
              <div className="mt-2 w-full h-1.5 rounded-full bg-[#1A2530] overflow-hidden">
                <div className={`h-full rounded-full transition-all duration-1000 ${metrics.disk_percent > 80 ? 'bg-rose-500' : metrics.disk_percent > 60 ? 'bg-amber-500' : 'bg-orange-500'}`} style={{ width: `${Math.min(metrics.disk_percent || 0, 100)}%` }} />
              </div>
            </div>

            {/* Risk */}
            <div className="relative overflow-hidden p-4 rounded-2xl bg-[#131A22] border border-[#26313D] group hover:border-emerald-500/30 transition-all duration-300">
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-[#8D9AAA] tracking-wider">Risk</span>
                <Shield className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="mt-1 flex items-center gap-2">
                <span className={`text-2xl font-black font-mono ${metrics.risk_level === 'LOW' ? 'text-emerald-400' : metrics.risk_level === 'MODERATE' ? 'text-amber-400' : metrics.risk_level === 'HIGH' ? 'text-orange-400' : 'text-rose-400'}`}>
                  {metrics.risk_level || '--'}
                </span>
                <span className="text-sm">
                  {metrics.risk_level === 'LOW' ? '🟢' : metrics.risk_level === 'MODERATE' ? '🟡' : metrics.risk_level === 'HIGH' ? '🟠' : '🔴'}
                </span>
              </div>
              <div className="mt-1 text-[9px] text-[#5F6B78]">Open positions: {metrics.open_positions || 0}</div>
            </div>
          </div>
        )}

        {/* ===== HEALTH METRICS ===== */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5">
          {healthData.map((metric) => (
            <div
              key={metric.name}
              className={`p-4 rounded-2xl bg-[#131A22] border transition-all duration-300 group hover:scale-[1.02] hover:shadow-lg ${getStatusColor(metric.status)}`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-[#8D9AAA]">{metric.icon || <Activity className="w-4 h-4" />}</span>
                  <span className="text-xs font-bold text-[#8D9AAA]">{metric.name}</span>
                </div>
                {getStatusIcon(metric.status)}
              </div>
              <div className="mt-2 flex items-end justify-between">
                <span className="text-2xl font-bold text-white">
                  {metric.status === 'healthy' ? '🟢' : metric.status === 'warning' ? '🟡' : '🔴'}
                </span>
                {metric.value && (
                  <span className="text-sm font-mono text-[#8D9AAA]">{metric.value}</span>
                )}
              </div>
              {metric.message && (
                <div className="mt-1 text-[10px] text-[#5F6B78]">{metric.message}</div>
              )}
            </div>
          ))}
        </div>

        {/* ===== HEALTH HISTORY CHART ===== */}
        {healthHistory.length > 1 && (
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <LineChart className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-bold text-white">Health History</h3>
              </div>
              <span className="text-[10px] text-[#5F6B78]">Last {healthHistory.length} updates</span>
            </div>
            <div className="h-16">
              <MiniChart data={healthHistory} color="#10B981" height={60} />
            </div>
            <div className="flex items-center justify-between mt-1 text-[9px] text-[#5F6B78]">
              <span>{history[0]?.timestamp || '--'}</span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                {healthHistory[healthHistory.length - 1] || 0}%
              </span>
              <span>{history[history.length - 1]?.timestamp || '--'}</span>
            </div>
          </div>
        )}

        {/* ===== FOOTER ===== */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-[10px] text-[#5F6B78] border-t border-[#1A2530] pt-4">
          <div className="flex items-center gap-3 flex-wrap">
            <span className="flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Health View v4.0
            </span>
            <span className="text-[#26313D]">|</span>
            <span className="text-[#26313D]">|</span>
            <span className="flex items-center gap-1">
              {metrics?.health_score >= 70 ? '🟢' : metrics?.health_score >= 40 ? '🟡' : '🔴'}
              {healthLabel.label}
            </span>
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            <span>Last update: {lastUpdate || '--'}</span>
            {wsConnected ? <Wifi className="w-3 h-3 text-emerald-400" /> : <WifiOff className="w-3 h-3 text-amber-400" />}
            <button
              onClick={() => {
                localStorage.setItem('apiKey', API_KEY);
                fetchHealthData();
              }}
              className="px-2 py-0.5 rounded bg-[#1A2530] hover:bg-[#26313D] transition-colors text-[#8D9AAA] hover:text-white"
            >
              Refresh Key
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HealthView;
