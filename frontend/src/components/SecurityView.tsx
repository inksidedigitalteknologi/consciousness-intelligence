// ============================================================
// INKSIDE DIGITAL — SECURITY VIEW
// Real-time Security Monitoring Dashboard
// ============================================================

import React, { useState, useEffect, useCallback } from 'react';
import {
  Shield, ShieldAlert, ShieldCheck, Activity, AlertTriangle,
  Users, Globe, Clock, TrendingUp, RefreshCw, Lock,
  Ban, Eye, Zap, Target, Server, Fingerprint, Wifi,
  ChevronRight, ChevronDown, Search, Filter, Download,
  BarChart3, PieChart, LineChart, Database, Cpu,
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface SecurityStats {
  period_hours: number;
  total_events: number;
  unique_ips: number;
  by_type: Record<string, number>;
  by_severity: Record<string, number>;
}

interface Attacker {
  ip: string;
  total_hits: number;
  ssh_failed: number;
  ssh_success: number;
  nginx_scans: number;
  exploits: number;
  threat_score: number;
  country: string | null;
  is_blocked: number;
}

interface UsernameAttempt {
  username: string;
  count: number;
  unique_ips: number;
  success_count: number;
  last_seen: string;
}

interface AttackPattern {
  pattern_type: string;
  count: number;
  unique_ips: number;
  last_seen: string;
}

interface SecurityEvent {
  timestamp: string;
  ip: string;
  event_type: string;
  severity: string;
  username: string | null;
  path: string | null;
  method: string | null;
  status_code: number | null;
  user_agent: string | null;
}

interface TimelineEntry {
  hour: string;
  total: number;
  ssh_failed: number;
  nginx_scans: number;
}

interface SecurityViewProps {
  wsConnected?: boolean;
}

// ============================================================
// HELPERS
// ============================================================

const API_KEY = (): string =>
  localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823';

const getSeverityColor = (severity: string): string => {
  switch (severity) {
    case 'critical': return 'text-red-500 bg-red-500/10 border-red-500/30';
    case 'high': return 'text-orange-500 bg-orange-500/10 border-orange-500/30';
    case 'medium': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/30';
    case 'low': return 'text-blue-500 bg-blue-500/10 border-blue-500/30';
    default: return 'text-gray-500 bg-gray-500/10 border-gray-500/30';
  }
};

const getThreatColor = (score: number): string => {
  if (score >= 80) return 'text-red-500';
  if (score >= 50) return 'text-orange-500';
  if (score >= 20) return 'text-yellow-500';
  return 'text-blue-500';
};

const getCountryFlag = (country: string | null): string => {
  if (!country) return '🌍';
  const flags: Record<string, string> = {
    'United Kingdom': '🇬🇧', 'Korea, Republic of': '🇰🇷', 'South Korea': '🇰🇷',
    'United States': '🇺🇸', 'Malaysia': '🇲🇾', 'Indonesia': '🇮🇩',
    'Iran, Islamic Republic of': '🇮🇷', 'Iran': '🇮🇷',
    'Russian Federation': '🇷🇺', 'Russia': '🇷🇺',
    'China': '🇨🇳', 'Brazil': '🇧🇷', 'Netherlands': '🇳🇱',
    'Germany': '🇩🇪', 'France': '🇫🇷', 'Vietnam': '🇻🇳',
    'India': '🇮🇳', 'Bulgaria': '🇧🇬', 'Sweden': '🇸🇪',
    'Singapore': '🇸🇬', 'Japan': '🇯🇵', 'Thailand': '🇹🇭',
    'Panama': '🇵🇦', 'Seychelles': '🇸🇨', 'Moldova': '🇲🇩',
    'Ukraine': '🇺🇦', 'Turkey': '🇹🇷', 'Poland': '🇵🇱',
  };
  return flags[country] || '🌍';
};

const formatTime = (ts: string): string => {
  if (!ts) return '-';
  try {
    const d = new Date(ts);
    return d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  } catch {
    return ts.slice(11, 19);
  }
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const SecurityView: React.FC<SecurityViewProps> = ({ wsConnected }) => {
  const [stats, setStats] = useState<SecurityStats | null>(null);
  const [attackers, setAttackers] = useState<Attacker[]>([]);
  const [usernames, setUsernames] = useState<UsernameAttempt[]>([]);
  const [patterns, setPatterns] = useState<AttackPattern[]>([]);
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [timeline, setTimeline] = useState<TimelineEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  // ── Tab state ──
  const [activeTab, setActiveTab] = useState<'security' | 'logs'>('security');

  // ── Logs state ──
  const [logsList, setLogsList] = useState<any[]>([]);
  const [logsStats, setLogsStats] = useState<any>({});
  const [selectedLog, setSelectedLog] = useState<string>('main.log');
  const [logLines, setLogLines] = useState<string[]>([]);
  const [logLevel, setLogLevel] = useState<string>('');
  const [logLoading, setLogLoading] = useState(false);

  // ── Fetch functions ───────────────────────────────────────
  const fetchAll = useCallback(async () => {
    try {
      const headers = { 'X-API-Key': API_KEY() };
      const base = '';

      const [
        statsRes, attackersRes, usernamesRes,
        patternsRes, eventsRes, timelineRes,
      ] = await Promise.all([
        fetch(`${base}/api/security/stats?hours=24`, { headers }),
        fetch(`${base}/api/security/top-attackers?limit=10&hours=24`, { headers }),
        fetch(`${base}/api/security/top-usernames?limit=10`, { headers }),
        fetch(`${base}/api/security/top-patterns?limit=10`, { headers }),
        fetch(`${base}/api/security/events?limit=30`, { headers }),
        fetch(`${base}/api/security/timeline?hours=24`, { headers }),
      ]);

      const statsData = await statsRes.json();
      const attackersData = await attackersRes.json();
      const usernamesData = await usernamesRes.json();
      const patternsData = await patternsRes.json();
      const eventsData = await eventsRes.json();
      const timelineData = await timelineRes.json();

      setStats(statsData);
      setAttackers(attackersData.attackers || []);
      setUsernames(usernamesData.usernames || []);
      setPatterns(patternsData.patterns || []);
      setEvents(eventsData.events || []);
      setTimeline(timelineData.timeline || []);
      setLastUpdate(new Date().toLocaleTimeString('en-GB'));
      setError(null);
    } catch (err) {
      console.error('Security fetch error:', err);
      setError('Failed to fetch security data');
    } finally {
      setLoading(false);
    }
  }, []);

  const triggerScan = useCallback(async () => {
    setScanning(true);
    try {
      const res = await fetch('/api/security/scan', {
        method: 'POST',
        headers: { 'X-API-Key': API_KEY() },
      });
      const data = await res.json();
      console.log('Scan result:', data);
      await fetchAll();
    } catch (err) {
      console.error('Scan error:', err);
    } finally {
      setScanning(false);
    }
  }, [fetchAll]);

  // ── Fetch logs ────────────────────────────────────────────
  const fetchLogsList = useCallback(async () => {
    try {
      const res = await fetch('/api/logs/list', { headers: { 'X-API-Key': API_KEY() } });
      const data = await res.json();
      setLogsList(data.logs || []);
    } catch (e) { console.error(e); }
  }, []);

  const fetchLogsStats = useCallback(async () => {
    try {
      const res = await fetch('/api/logs/stats', { headers: { 'X-API-Key': API_KEY() } });
      const data = await res.json();
      setLogsStats(data.stats || {});
    } catch (e) { console.error(e); }
  }, []);

  const fetchLogTail = useCallback(async (file: string, level: string = '') => {
    setLogLoading(true);
    try {
      const url = `/api/logs/tail?file=${file}&lines=100${level ? `&level=${level}` : ''}`;
      const res = await fetch(url, { headers: { 'X-API-Key': API_KEY() } });
      const data = await res.json();
      setLogLines(data.lines || []);
    } catch (e) { console.error(e); }
    finally { setLogLoading(false); }
  }, []);

  // ── Initial + interval ────────────────────────────────────
  useEffect(() => {
    fetchAll();
    fetchLogsList();
    fetchLogsStats();
    const interval = setInterval(fetchAll, 60000);
    return () => clearInterval(interval);
  }, [fetchAll, fetchLogsList, fetchLogsStats]);

  // Fetch tail saat tab logs aktif / file berubah
  useEffect(() => {
    if (activeTab === 'logs') {
      fetchLogTail(selectedLog, logLevel);
    }
  }, [activeTab, selectedLog, logLevel, fetchLogTail]);

  // ── Render ────────────────────────────────────────────────
  return (
    <div className="space-y-4 p-4">
      {/* HEADER */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Shield className="w-6 h-6 text-cyan-400" />
          <div>
            <h1 className="text-xl font-bold text-white">Security Monitor</h1>
            <p className="text-xs text-gray-400">
              Real-time threat detection · {lastUpdate && `Updated ${lastUpdate}`}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className={`flex items-center gap-1 px-2 py-1 rounded text-xs ${wsConnected ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
            <Wifi className="w-3 h-3" />
            {wsConnected ? 'Live' : 'Offline'}
          </div>
          <button
            onClick={triggerScan}
            disabled={scanning}
            className="flex items-center gap-1 px-3 py-1.5 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-400 rounded text-xs transition disabled:opacity-50"
          >
            <RefreshCw className={`w-3 h-3 ${scanning ? 'animate-spin' : ''}`} />
            {scanning ? 'Scanning...' : 'Scan Now'}
          </button>
        </div>

        {/* TAB SELECTOR */}
        <div className="flex items-center gap-1 bg-gray-900/50 border border-gray-800 rounded p-1">
          <button
            onClick={() => setActiveTab('security')}
            className={`px-3 py-1 rounded text-xs transition ${
              activeTab === 'security' ? 'bg-cyan-500/20 text-cyan-400' : 'text-gray-400 hover:text-white'
            }`}
          >
            🛡️ Security
          </button>
          <button
            onClick={() => setActiveTab('logs')}
            className={`px-3 py-1 rounded text-xs transition ${
              activeTab === 'logs' ? 'bg-cyan-500/20 text-cyan-400' : 'text-gray-400 hover:text-white'
            }`}
          >
            📄 Logs
          </button>
        </div>
      </div>

      {/* SECURITY TAB */}
      {activeTab === 'security' && (
        <>
      {/* ERROR */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-3 py-2 rounded text-sm">
          {error}
        </div>
      )}

      {/* SUMMARY CARDS */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3">
          <div className="flex items-center gap-2 mb-1">
            <Activity className="w-4 h-4 text-cyan-400" />
            <span className="text-xs text-gray-400">Total Events (24h)</span>
          </div>
          <div className="text-2xl font-bold text-white">
            {stats?.total_events?.toLocaleString() || 0}
          </div>
        </div>

        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3">
          <div className="flex items-center gap-2 mb-1">
            <Globe className="w-4 h-4 text-orange-400" />
            <span className="text-xs text-gray-400">Unique IPs</span>
          </div>
          <div className="text-2xl font-bold text-white">
            {stats?.unique_ips || 0}
          </div>
        </div>

        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3">
          <div className="flex items-center gap-2 mb-1">
            <Lock className="w-4 h-4 text-red-400" />
            <span className="text-xs text-gray-400">SSH Failed</span>
          </div>
          <div className="text-2xl font-bold text-red-400">
            {stats?.by_type?.ssh_failed?.toLocaleString() || 0}
          </div>
        </div>

        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3">
          <div className="flex items-center gap-2 mb-1">
            <ShieldAlert className="w-4 h-4 text-yellow-400" />
            <span className="text-xs text-gray-400">Bot Scans</span>
          </div>
          <div className="text-2xl font-bold text-yellow-400">
            {stats?.by_type?.nginx_scan || 0}
          </div>
        </div>
      </div>

      {/* TWO COLUMN LAYOUT */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
        {/* TOP ATTACKERS */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Target className="w-4 h-4 text-red-400" />
              Top Attackers
            </h2>
            <span className="text-xs text-gray-500">{attackers.length}</span>
          </div>
          <div className="space-y-1 max-h-64 overflow-y-auto">
            {attackers.map((a) => (
              <div key={a.ip} className="flex items-center justify-between p-2 bg-gray-800/50 rounded text-xs">
                <div className="flex items-center gap-2 flex-1">
                  <span className={`font-bold ${getThreatColor(a.threat_score)}`}>
                    {a.threat_score}
                  </span>
                  <span className="font-mono text-gray-300">{a.ip}</span>
                  {a.country && (
                    <span className="text-gray-500 text-xs" title={a.country}>
                      {getCountryFlag(a.country)} {a.country}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-3 text-gray-400">
                  <span title="SSH Failed">🔒 {a.ssh_failed}</span>
                  <span title="Total Hits">📊 {a.total_hits}</span>
                </div>
              </div>
            ))}
            {attackers.length === 0 && (
              <div className="text-center text-gray-500 py-4 text-xs">
                No attackers detected
              </div>
            )}
          </div>
        </div>

        {/* TOP USERNAMES */}
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Users className="w-4 h-4 text-orange-400" />
              Username Attempts
            </h2>
            <span className="text-xs text-gray-500">{usernames.length}</span>
          </div>
          <div className="space-y-1 max-h-64 overflow-y-auto">
            {usernames.map((u) => (
              <div key={u.username} className="flex items-center justify-between p-2 bg-gray-800/50 rounded text-xs">
                <div className="flex items-center gap-2 flex-1">
                  <Fingerprint className="w-3 h-3 text-gray-500" />
                  <span className="font-mono text-gray-300">{u.username}</span>
                </div>
                <div className="flex items-center gap-3 text-gray-400">
                  <span title="Attempts">📊 {u.count}</span>
                  {u.success_count > 0 && (
                    <span className="text-red-400" title="Success">✅ {u.success_count}</span>
                  )}
                </div>
              </div>
            ))}
            {usernames.length === 0 && (
              <div className="text-center text-gray-500 py-4 text-xs">
                No username attempts
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ATTACK PATTERNS */}
      {patterns.length > 0 && (
        <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2 mb-3">
            <Zap className="w-4 h-4 text-yellow-400" />
            Attack Patterns
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {patterns.map((p) => (
              <div key={p.pattern_type} className="p-2 bg-gray-800/50 rounded text-xs">
                <div className="text-yellow-400 font-semibold">{p.pattern_type}</div>
                <div className="text-gray-400">{p.count} hits</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* RECENT EVENTS */}
      <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Eye className="w-4 h-4 text-cyan-400" />
            Recent Events
          </h2>
          <span className="text-xs text-gray-500">{events.length} events</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="text-gray-500 border-b border-gray-800">
                <th className="text-left py-1 px-2">Time</th>
                <th className="text-left py-1 px-2">IP</th>
                <th className="text-left py-1 px-2">Type</th>
                <th className="text-left py-1 px-2">User/Path</th>
                <th className="text-left py-1 px-2">Severity</th>
              </tr>
            </thead>
            <tbody>
              {events.slice(0, 20).map((e, i) => (
                <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-800/30">
                  <td className="py-1 px-2 text-gray-400 font-mono">{formatTime(e.timestamp)}</td>
                  <td className="py-1 px-2 text-gray-300 font-mono">{e.ip}</td>
                  <td className="py-1 px-2 text-gray-400">{e.event_type}</td>
                  <td className="py-1 px-2 text-gray-400 font-mono truncate max-w-xs">
                    {e.username || e.path || '-'}
                  </td>
                  <td className="py-1 px-2">
                    <span className={`px-1.5 py-0.5 rounded text-xs border ${getSeverityColor(e.severity)}`}>
                      {e.severity}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {events.length === 0 && (
            <div className="text-center text-gray-500 py-4 text-xs">
              No events recorded
            </div>
          )}
        </div>
      </div>
        </>
      )}

      {/* LOGS TAB */}
      {activeTab === 'logs' && (
        <div className="space-y-3">
          <div className="flex items-center gap-2 flex-wrap">
            <select
              value={selectedLog}
              onChange={(e) => setSelectedLog(e.target.value)}
              className="bg-gray-900/50 border border-gray-800 text-white text-xs rounded px-3 py-1.5"
            >
              {logsList.map((log: any) => (
                <option key={log.name} value={log.name}>
                  {log.name} ({log.size_kb} KB)
                </option>
              ))}
            </select>
            <select
              value={logLevel}
              onChange={(e) => setLogLevel(e.target.value)}
              className="bg-gray-900/50 border border-gray-800 text-white text-xs rounded px-3 py-1.5"
            >
              <option value="">All Levels</option>
              <option value="INFO">INFO</option>
              <option value="WARNING">WARNING</option>
              <option value="ERROR">ERROR</option>
              <option value="CRITICAL">CRITICAL</option>
            </select>
            <button
              onClick={() => fetchLogTail(selectedLog, logLevel)}
              disabled={logLoading}
              className="flex items-center gap-1 px-3 py-1.5 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-400 rounded text-xs transition disabled:opacity-50"
            >
              <RefreshCw className={`w-3 h-3 ${logLoading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            <span className="text-xs text-gray-500">{logLines.length} lines</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {logsList.slice(0, 4).map((log: any) => {
              const s = logsStats[log.name] || {};
              return (
                <div key={log.name} className="bg-gray-900/50 border border-gray-800 rounded-lg p-2 text-xs">
                  <div className="text-gray-400 truncate">{log.name}</div>
                  <div className="flex gap-2 mt-1">
                    <span className="text-blue-400">I:{s.INFO || 0}</span>
                    <span className="text-yellow-400">W:{s.WARNING || 0}</span>
                    <span className="text-red-400">E:{s.ERROR || 0}</span>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-3">
            <div className="font-mono text-xs max-h-[600px] overflow-y-auto space-y-0.5">
              {logLines.length === 0 && (
                <div className="text-center text-gray-500 py-4">
                  {logLoading ? 'Loading...' : 'No log lines'}
                </div>
              )}
              {logLines.map((line, i) => {
                let color = 'text-gray-300';
                if (line.includes('| ERROR |')) color = 'text-red-400';
                else if (line.includes('| WARNING |')) color = 'text-yellow-400';
                else if (line.includes('| CRITICAL |')) color = 'text-red-500 font-bold';
                else if (line.includes('| DEBUG |')) color = 'text-gray-500';
                return (
                  <div key={i} className={`${color} whitespace-pre-wrap break-all`}>
                    {line}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SecurityView;
