// src/components/DashboardView.tsx
// INKSIDE DIGITAL - DASHBOARD VIEW v3.0
// Dividend Hunter integration + Error Boundary + Real Data

import React, { useState, useEffect, useMemo, useCallback, memo } from 'react';
import {
  Brain, Sparkles, GraduationCap, RefreshCw, TrendingUp, Search,
  BookOpen, Database, Activity, ChevronLeft, ChevronRight,
  ArrowUpRight, Shield, Zap, CheckCircle2, AlertCircle, Clock,
  BarChart3, Gauge, Cpu, HardDrive, Wifi, Target, Compass,
  Lightbulb, Rocket, Award, Loader2, X, DollarSign,
  TrendingDown, Crown, Medal, Calendar,
} from 'lucide-react';
import { TickerInfo, TradingSignal, CognitiveInsight, NavigationPage } from '../types';

// ============================================================
// CONSTANTS
// ============================================================

const API_KEY = 'iks_612d40ce554b1670525355c85567f823';
const LOG_PREFIX = '[DashboardView]';

// ============================================================
// TYPES
// ============================================================

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

interface DividendRecord {
  symbol: string;
  name: string;
  dividend: number;
  annual_dividend?: number;
  ex_date?: string;
  pay_date?: string;
  sector?: string;
  source?: string;
}

interface TrapRecord {
  symbol: string;
  name?: string;
  trap_score: number;
  category: string;
  recommendation: string;
  current_yield: number;
  streak_years?: number;
  cut_count?: number;
  is_king?: boolean;
  is_aristocrat?: boolean;
  is_champion?: boolean;
}

interface DashboardViewProps {
  tickers: TickerInfo[];
  signals: TradingSignal[];
  insights: CognitiveInsight[];
  engineRunning: boolean;
  learningActive: boolean;
  cycleCount: number;
  brainState: string;
  consciousnessLevel: number;
  systemMetrics: SystemMetrics;
  onNavigate: (page: NavigationPage) => void;
  wsConnected?: boolean;
  isLoading?: boolean;
  error?: string | null;
  onRefresh?: () => void;
}

// ============================================================
// LOGGER
// ============================================================

const log = {
  info: (m: string, d?: any) => console.info(`${LOG_PREFIX} ${m}`, d || ''),
  warn: (m: string, d?: any) => console.warn(`${LOG_PREFIX} ⚠️ ${m}`, d || ''),
  error: (m: string, e?: any) => console.error(`${LOG_PREFIX} ❌ ${m}`, e || ''),
  debug: (m: string, d?: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`${LOG_PREFIX} ${m}`, d || '');
    }
  },
};

// ============================================================
// FORMATTERS
// ============================================================

const formatUptime = (s: number): string => {
  if (!s || s <= 0) return '--';
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  return h > 0 ? `${h}h ${m}m` : `${m}m`;
};

const formatRam = (gb: number): string => {
  if (!gb || gb <= 0) return '--';
  return `${gb.toFixed(1)} GB`;
};

const formatPnl = (v: number): string => {
  if (!v && v !== 0) return '--';
  return v >= 0 ? `+$${v.toFixed(2)}` : `-$${Math.abs(v).toFixed(2)}`;
};

const formatPrice = (p: number): string => {
  if (!p && p !== 0) return '--';
  if (p >= 1000) return p.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  if (p >= 1) return p.toFixed(4);
  return p.toFixed(8);
};

const safeNum = (n: any, fallback = 0): number => {
  const v = Number(n);
  return isNaN(v) ? fallback : v;
};

// ============================================================
// ERROR BOUNDARY
// ============================================================

class DashboardErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error: Error | null }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    log.error('Error Boundary:', { error, info });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-6 rounded-2xl bg-[#131A22] border border-rose-500/30" role="alert">
          <div className="flex items-center gap-3 text-rose-400">
            <AlertCircle className="w-5 h-5" />
            <span className="font-bold">Dashboard Error</span>
          </div>
          <p className="text-xs text-[#8D9AAA] mt-2">
            {this.state.error?.message || 'Unknown error'}
          </p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="mt-3 px-4 py-2 rounded-lg bg-rose-500/20 text-rose-400 text-xs hover:bg-rose-500/30 transition-colors"
          >
            Retry
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// ============================================================
// SUB-COMPONENTS
// ============================================================

const MetricCard = memo(({ metric, categoryColors }: { metric: any; categoryColors: any }) => {
  const colors = categoryColors[metric.category] || categoryColors.system;
  return (
    <div
      onClick={metric.onClick}
      className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] hover:border-[#3B82F6]/50 transition-all cursor-pointer group"
      role={metric.onClick ? 'button' : undefined}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          {metric.icon}
          <span className="text-[10px] font-semibold text-[#8D9AAA] truncate max-w-[60px]">
            {metric.title}
          </span>
        </div>
        {metric.badge && (
          <span className={`text-[8px] font-black px-1.5 py-0.5 rounded ${colors.bg} ${colors.text} border ${colors.border}`}>
            {metric.badge}
          </span>
        )}
      </div>
      <div className="mt-1.5">
        <div className="text-sm font-black text-white font-mono truncate">{metric.value}</div>
        <div className="text-[9px] text-[#5F6B78] truncate">{metric.subtitle}</div>
      </div>
    </div>
  );
});
MetricCard.displayName = 'MetricCard';

const SignalCard = memo(({ signal }: { signal: TradingSignal }) => {
  const isBuy = signal.signal?.includes('BUY');
  const isSell = signal.signal?.includes('SELL');
  const colorClass = isBuy
    ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
    : isSell
    ? 'text-rose-400 bg-rose-500/10 border-rose-500/20'
    : 'text-amber-400 bg-amber-500/10 border-amber-500/20';

  return (
    <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] hover:border-[#3B82F6]/50 transition-all flex flex-col justify-between space-y-3">
      <div>
        <div className="flex items-center justify-between">
          <span className="font-extrabold text-white text-sm tracking-wide font-mono">
            {signal.pair}
          </span>
          <span className={`text-[10px] font-black px-2 py-0.5 rounded border ${colorClass}`}>
            {signal.signal?.replace('_', ' ') || 'HOLD'}
          </span>
        </div>
        <div className="mt-2 flex items-baseline justify-between">
          <span className="text-base font-bold text-white font-mono">
            ${formatPrice(signal.price)}
          </span>
          <span className="text-xs font-mono font-bold text-blue-400">
            {signal.confidence}% Conf
          </span>
        </div>
        <div className="w-full bg-[#0B0F14] h-1.5 rounded-full mt-2 overflow-hidden">
          <div
            className={`h-full ${signal.confidence >= 80 ? 'bg-emerald-400' : signal.confidence >= 60 ? 'bg-blue-400' : 'bg-amber-400'}`}
            style={{ width: `${signal.confidence}%` }}
          />
        </div>
      </div>
    </div>
  );
});
SignalCard.displayName = 'SignalCard';

const TickerRow = memo(({ ticker }: { ticker: TickerInfo }) => {
  const isPositive = ticker.change24h >= 0;
  return (
    <div className="py-3 flex items-center justify-between hover:bg-[#18212B]/40 px-2 rounded-lg transition-colors">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-[#1A2530] border border-[#26313D] flex items-center justify-center font-bold text-white text-xs">
          {ticker.pair?.split('/')[0] || '?'}
        </div>
        <div>
          <div className="font-bold text-white text-xs tracking-wide">{ticker.pair}</div>
          <div className="text-[10px] text-[#5F6B78]">{ticker.name || ticker.pair}</div>
        </div>
      </div>
      <div className="flex items-center gap-6">
        <div className="text-right">
          <div className="font-mono font-bold text-white text-xs">${formatPrice(ticker.price)}</div>
        </div>
        <div className={`flex items-center gap-1 font-mono font-bold text-xs px-2.5 py-1 rounded-lg ${
          isPositive ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
        }`}>
          {isPositive ? '+' : ''}{(ticker.change24h || 0).toFixed(2)}%
        </div>
      </div>
    </div>
  );
});
TickerRow.displayName = 'TickerRow';

const InsightCard = memo(({ insight }: { insight: CognitiveInsight }) => (
  <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-1 hover:border-purple-500/30 transition-all">
    <div className="flex items-center justify-between">
      <span className="text-xs font-bold text-white tracking-wide">{insight.title}</span>
      <span className="text-[9px] font-mono text-[#8D9AAA] px-1.5 py-0.5 rounded bg-[#0B0F14]">
        {insight.confidence || 0}% Conf
      </span>
    </div>
    <p className="text-[11px] text-[#8D9AAA] leading-relaxed">{insight.content}</p>
  </div>
));
InsightCard.displayName = 'InsightCard';

// ============================================================
// DIVIDEND HUNTER SECTION
// ============================================================

const DividendHunterSection: React.FC<{
  dividends: DividendRecord[];
  traps: TrapRecord[];
  loading: boolean;
  onNavigate: (page: NavigationPage) => void;
}> = ({ dividends, traps, loading, onNavigate }) => {
  const trapMap = useMemo(() => {
    const m: Record<string, TrapRecord> = {};
    traps.forEach(t => { m[t.symbol] = t; });
    return m;
  }, [traps]);

  const stats = useMemo(() => {
    const total = dividends.length;
    const safe = traps.filter(t => t.trap_score < 30).length;
    const trap = traps.filter(t => t.trap_score >= 50).length;
    const kings = traps.filter(t => t.is_king).length;
    const aristocrats = traps.filter(t => t.is_aristocrat).length;
    return { total, safe, trap, kings, aristocrats };
  }, [dividends, traps]);

  const getTrapColor = (score: number) => {
    if (score >= 70) return 'text-rose-400 bg-rose-500/20 border-rose-500/30';
    if (score >= 50) return 'text-orange-400 bg-orange-500/20 border-orange-500/30';
    if (score >= 30) return 'text-amber-400 bg-amber-500/20 border-amber-500/30';
    return 'text-emerald-400 bg-emerald-500/20 border-emerald-500/30';
  };

  const getTrapIcon = (score: number) => {
    if (score >= 70) return '🚨';
    if (score >= 50) return '⚠️';
    if (score >= 30) return '🟡';
    return '✅';
  };

  return (
    <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-[#26313D]/70">
        <div className="flex items-center gap-2.5">
          <DollarSign className="w-4 h-4 text-emerald-400" />
          <h3 className="text-sm font-bold text-white tracking-wider uppercase">
            Dividend Hunter
          </h3>
          <span className="text-xs text-[#8D9AAA] hidden sm:inline">
            {dividends.length > 0 ? `(${dividends.length} stocks)` : '(loading...)'}
          </span>
          {loading && <Loader2 className="w-4 h-4 text-emerald-400 animate-spin" />}
        </div>
        <button
          onClick={() => onNavigate('Signals')}
          className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1 cursor-pointer transition-colors"
        >
          View All <ArrowUpRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mt-4">
        <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold">Total</div>
          <div className="text-lg font-black text-white font-mono mt-1">{stats.total}</div>
        </div>
        <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold">Safe</div>
          <div className="text-lg font-black text-emerald-300 font-mono mt-1">{stats.safe}</div>
        </div>
        <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold">Trap Alert</div>
          <div className="text-lg font-black text-rose-300 font-mono mt-1">{stats.trap}</div>
        </div>
        <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold">Kings</div>
          <div className="text-lg font-black text-amber-300 font-mono mt-1">{stats.kings}</div>
        </div>
        <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold">Aristocrats</div>
          <div className="text-lg font-black text-purple-300 font-mono mt-1">{stats.aristocrats}</div>
        </div>
      </div>

      {/* Top Dividend Stocks */}
      {dividends.length > 0 && (
        <div className="mt-4 space-y-2">
          <div className="text-[10px] uppercase text-[#8D9AAA] font-bold tracking-wider">
            Top Dividend Stocks
          </div>
          {dividends.slice(0, 5).map((d, i) => {
            const trap = trapMap[d.symbol];
            const score = safeNum(trap?.trap_score, 0);
            return (
              <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-[#1A2530] border border-[#26313D] hover:border-emerald-500/30 transition-all">
                <div className="flex items-center gap-3 min-w-0 flex-1">
                  <span className="font-black text-white font-mono text-xs w-14 flex-shrink-0">{d.symbol}</span>
                  <span className="text-[10px] text-[#8D9AAA] truncate hidden md:block">{d.name}</span>
                </div>
                <div className="flex items-center gap-3 text-[10px] font-mono flex-shrink-0">
                  <span className="text-emerald-400 font-bold">${safeNum(d.dividend).toFixed(4)}</span>
                  <span className={`px-1.5 py-0.5 rounded border ${getTrapColor(score)}`}>
                    {getTrapIcon(score)} {score}
                  </span>
                  {trap?.is_king && <Crown className="w-3 h-3 text-amber-400" />}
                  {trap?.is_aristocrat && <Award className="w-3 h-3 text-purple-400" />}
                  {trap?.is_champion && <Medal className="w-3 h-3 text-cyan-400" />}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {dividends.length === 0 && !loading && (
        <div className="py-8 text-center text-[#5F6B78]">
          <DollarSign className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <p className="text-xs">No dividend data available</p>
        </div>
      )}
    </div>
  );
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const DashboardView: React.FC<DashboardViewProps> = ({
  tickers = [],
  signals = [],
  insights = [],
  engineRunning = true,
  learningActive = false,
  cycleCount = 0,
  brainState = 'IDLE',
  consciousnessLevel = 0,
  systemMetrics,
  onNavigate,
  wsConnected = false,
  isLoading = false,
  error = null,
  onRefresh,
}) => {
  const [signalPage, setSignalPage] = useState(0);
  const [metricPage, setMetricPage] = useState(0);
  const [localError, setLocalError] = useState<string | null>(null);

  // Dividend state
  const [dividends, setDividends] = useState<DividendRecord[]>([]);
  const [traps, setTraps] = useState<TrapRecord[]>([]);
  const [dividendLoading, setDividendLoading] = useState(false);

  const signalsPerPage = 4;
  const metricsPerPage = 12;

  const totalSignalPages = Math.max(1, Math.ceil(signals.length / signalsPerPage));
  const currentSignals = useMemo(
    () => signals.slice(signalPage * signalsPerPage, (signalPage + 1) * signalsPerPage),
    [signals, signalPage, signalsPerPage]
  );

  // ============================================================
  // FETCH DIVIDEND
  // ============================================================

  useEffect(() => {
    const fetchDividend = async () => {
      setDividendLoading(true);
      try {
        const [topRes, trapRes] = await Promise.all([
          fetch('/api/dividend/top?limit=10', { headers: { 'X-API-Key': API_KEY } }),
          fetch('/api/dividend/trap-screener/top', { headers: { 'X-API-Key': API_KEY } }).catch(() => null),
        ]);
        if (topRes.ok) {
          const d = await topRes.json();
          setDividends(d.data || []);
        }
        if (trapRes && trapRes.ok) {
          const t = await trapRes.json();
          setTraps(t.data || []);
        }
      } catch (e) {
        log.warn('Dividend fetch failed:', e);
      } finally {
        setDividendLoading(false);
      }
    };
    fetchDividend();
    const iv = setInterval(fetchDividend, 300000);
    return () => clearInterval(iv);
  }, []);

  // ============================================================
  // LOGGING
  // ============================================================

  useEffect(() => {
    log.info('DashboardView mounted', {
      tickers: tickers.length,
      signals: signals.length,
      insights: insights.length,
    });
  }, []);

  // ============================================================
  // METRICS
  // ============================================================

  const allMetrics = useMemo(() => [
    // System
    {
      id: 'brain', category: 'system',
      icon: <Brain className="w-4 h-4 text-blue-400" />,
      title: 'Cognitive Brain', value: brainState || 'IDLE',
      subtitle: `Cycles: ${cycleCount}`, badge: 'v4.2.3',
      onClick: () => onNavigate('Brain'),
    },
    {
      id: 'consciousness', category: 'system',
      icon: <Sparkles className="w-4 h-4 text-purple-400" />,
      title: 'Consciousness',
      value: consciousnessLevel > 0 ? `${(consciousnessLevel * 100).toFixed(0)}%` : '--',
      subtitle: 'Awareness', badge: 'CALM',
      onClick: () => onNavigate('Reflection'),
    },
    {
      id: 'learning', category: 'system',
      icon: <GraduationCap className="w-4 h-4 text-emerald-400" />,
      title: 'Learning', value: learningActive ? 'ACTIVE' : 'IDLE',
      subtitle: '32 Modules', badge: 'v3.0',
      onClick: () => onNavigate('Learning'),
    },
    {
      id: 'memory', category: 'system',
      icon: <Database className="w-4 h-4 text-indigo-400" />,
      title: 'Memory', value: systemMetrics?.memory_count ?? '--',
      subtitle: 'Records', badge: 'SQLITE',
      onClick: () => onNavigate('Memory'),
    },
    {
      id: 'knowledge', category: 'system',
      icon: <BookOpen className="w-4 h-4 text-teal-400" />,
      title: 'Knowledge', value: systemMetrics?.knowledge_count ?? '--',
      subtitle: 'Items', badge: 'GRAPH',
      onClick: () => onNavigate('Knowledge'),
    },
    {
      id: 'cpu', category: 'system',
      icon: <Cpu className="w-4 h-4 text-cyan-400" />,
      title: 'CPU', value: systemMetrics?.cpu ? `${systemMetrics.cpu.toFixed(0)}%` : '--',
      subtitle: 'Usage', badge: 'REAL',
    },
    {
      id: 'ram', category: 'system',
      icon: <HardDrive className="w-4 h-4 text-rose-400" />,
      title: 'RAM', value: formatRam(systemMetrics?.ram),
      subtitle: 'Usage', badge: 'REAL',
    },
    {
      id: 'uptime', category: 'system',
      icon: <Clock className="w-4 h-4 text-amber-400" />,
      title: 'Uptime', value: formatUptime(systemMetrics?.uptime),
      subtitle: 'Since start', badge: 'STABLE',
    },
    // Market
    {
      id: 'exchange', category: 'market',
      icon: <RefreshCw className="w-4 h-4 text-cyan-400" />,
      title: 'Exchange', value: tickers.length > 0 ? 'ONLINE' : 'OFFLINE',
      subtitle: `${tickers.length} Pairs`, badge: 'LIVE',
      onClick: () => onNavigate('Market'),
    },
    {
      id: 'signals_count', category: 'market',
      icon: <TrendingUp className="w-4 h-4 text-amber-400" />,
      title: 'Signals', value: signals.length,
      subtitle: 'Active', badge: 'MTF',
      onClick: () => onNavigate('Signals'),
    },
    {
      id: 'dividend_count', category: 'market',
      icon: <DollarSign className="w-4 h-4 text-emerald-400" />,
      title: 'Dividends', value: dividends.length,
      subtitle: 'Stocks', badge: 'NEW',
      onClick: () => onNavigate('Signals'),
    },
    {
      id: 'trap_count', category: 'market',
      icon: <AlertCircle className="w-4 h-4 text-rose-400" />,
      title: 'Trap Alert',
      value: traps.filter(t => t.trap_score >= 50).length,
      subtitle: 'High risk', badge: 'ALERT',
    },
    // Trading
    {
      id: 'trading_pnl', category: 'trading',
      icon: <Zap className="w-4 h-4 text-emerald-400" />,
      title: 'Total PnL', value: formatPnl(systemMetrics?.pnl),
      subtitle: `${systemMetrics?.win_rate ?? '--'}% Win`, badge: 'PAPER',
      onClick: () => onNavigate('Trading'),
    },
    {
      id: 'trades_count', category: 'trading',
      icon: <TrendingUp className="w-4 h-4 text-blue-400" />,
      title: 'Trades', value: systemMetrics?.total_trades ?? '--',
      subtitle: 'All time', badge: 'ACTIVE',
    },
    {
      id: 'positions_open', category: 'trading',
      icon: <Target className="w-4 h-4 text-amber-400" />,
      title: 'Positions', value: systemMetrics?.open_positions ?? '--',
      subtitle: 'Open', badge: 'HOLD',
    },
    {
      id: 'risk_level', category: 'trading',
      icon: <Shield className="w-4 h-4 text-rose-400" />,
      title: 'Risk', value: systemMetrics?.risk_level || '--',
      subtitle: 'Per trade', badge: 'LEVEL',
    },
    // Cognitive
    {
      id: 'insights_count', category: 'cognitive',
      icon: <Lightbulb className="w-4 h-4 text-yellow-400" />,
      title: 'Insights', value: insights.length,
      subtitle: 'Active', badge: 'LIVE',
    },
    {
      id: 'prediction_accuracy', category: 'cognitive',
      icon: <Compass className="w-4 h-4 text-cyan-400" />,
      title: 'Accuracy',
      value: systemMetrics?.prediction_accuracy ? `${systemMetrics.prediction_accuracy.toFixed(1)}%` : '--',
      subtitle: 'Last 100', badge: 'ML',
    },
  ], [brainState, cycleCount, consciousnessLevel, learningActive, engineRunning,
      systemMetrics, tickers.length, signals.length, insights.length, dividends.length, traps, onNavigate]);

  // ============================================================
  // PAGINATION
  // ============================================================

  const totalMetricPages = Math.ceil(allMetrics.length / metricsPerPage);
  const currentMetrics = useMemo(
    () => allMetrics.slice(metricPage * metricsPerPage, (metricPage + 1) * metricsPerPage),
    [allMetrics, metricPage, metricsPerPage]
  );

  const groupedMetrics = useMemo(() => {
    const groups: Record<string, typeof allMetrics> = { system: [], market: [], trading: [], cognitive: [] };
    currentMetrics.forEach(m => { if (groups[m.category]) groups[m.category].push(m); });
    return groups;
  }, [currentMetrics]);

  const categoryColors = {
    system: { bg: 'bg-blue-500/10', border: 'border-blue-500/20', text: 'text-blue-400' },
    market: { bg: 'bg-cyan-500/10', border: 'border-cyan-500/20', text: 'text-cyan-400' },
    trading: { bg: 'bg-emerald-500/10', border: 'border-emerald-500/20', text: 'text-emerald-400' },
    cognitive: { bg: 'bg-purple-500/10', border: 'border-purple-500/20', text: 'text-purple-400' },
  };

  const categoryLabels: Record<string, string> = {
    system: '⚙️ System',
    market: '📊 Market',
    trading: '💰 Trading',
    cognitive: '🧠 Cognitive',
  };

  const handleMetricPageChange = useCallback((dir: 'prev' | 'next') => {
    setMetricPage(p => dir === 'prev' ? Math.max(0, p - 1) : Math.min(totalMetricPages - 1, p + 1));
  }, [totalMetricPages]);

  const handleSignalPageChange = useCallback((dir: 'prev' | 'next') => {
    setSignalPage(p => dir === 'prev' ? Math.max(0, p - 1) : Math.min(totalSignalPages - 1, p + 1));
  }, [totalSignalPages]);

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <DashboardErrorBoundary>
      <div id="dashboard-view" className="space-y-6 pb-12">
        {/* ERROR */}
        {(error || localError) && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center gap-2 text-rose-400 text-xs">
            <AlertCircle className="w-4 h-4" />
            <span>{error || localError}</span>
            <button onClick={() => setLocalError(null)} className="ml-auto">
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* HEADER */}
        <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#18212B] to-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
          <div className="space-y-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className={`w-2.5 h-2.5 rounded-full ${engineRunning ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
              <h2 className="text-xl font-bold text-white tracking-wide">Cognitive Intelligence System</h2>
              <span className={`text-xs px-2.5 py-0.5 rounded-full ${
                engineRunning ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              } font-semibold`}>
                {engineRunning ? 'ACTIVE' : 'STANDBY'}
              </span>
              {wsConnected && (
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 animate-pulse">
                  LIVE
                </span>
              )}
            </div>
            <p className="text-xs text-[#8D9AAA]">
              {engineRunning
                ? 'Live streaming exchange bridge with autonomous cognitive reflection.'
                : 'System is running and ready.'}
            </p>
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            <div className="px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
              <div className="text-[10px] uppercase font-bold text-[#5F6B78]">Health</div>
              <div className="text-sm font-extrabold text-emerald-400 font-mono">
                {systemMetrics?.health_score ? `${systemMetrics.health_score.toFixed(1)}%` : '--'}
              </div>
            </div>
            <div className="px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
              <div className="text-[10px] uppercase font-bold text-[#5F6B78]">Cycles</div>
              <div className="text-sm font-extrabold text-blue-400 font-mono">#{cycleCount || 0}</div>
            </div>
            {onRefresh && (
              <button onClick={onRefresh} className="p-2 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors" aria-label="Refresh">
                <RefreshCw className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* DIVIDEND HUNTER */}
        <DividendHunterSection
          dividends={dividends}
          traps={traps}
          loading={dividendLoading}
          onNavigate={onNavigate}
        />

        {/* METRICS */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
          <div className="flex items-center justify-between pb-4 border-b border-[#26313D]/70">
            <div className="flex items-center gap-2.5">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Activity className="w-4 h-4 text-blue-400" />
                System Metrics
              </h3>
              <span className="text-xs text-[#8D9AAA] hidden sm:inline">
                ({allMetrics.length} metrics • Page {metricPage + 1}/{totalMetricPages})
              </span>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={() => handleMetricPageChange('prev')} disabled={metricPage === 0}
                className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 transition-colors">
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="text-xs text-[#5F6B78] font-mono px-2">{metricPage + 1}/{totalMetricPages}</span>
              <button onClick={() => handleMetricPageChange('next')} disabled={metricPage >= totalMetricPages - 1}
                className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 transition-colors">
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {Object.entries(groupedMetrics).map(([cat, metrics]) => (
            metrics.length > 0 && (
              <div key={cat} className="mt-4">
                <div className="flex items-center gap-2 mb-3">
                  <div className={`w-1 h-4 rounded-full ${categoryColors[cat as keyof typeof categoryColors]?.bg.replace('/10', '')}`} />
                  <span className={`text-[11px] font-bold uppercase tracking-wider ${categoryColors[cat as keyof typeof categoryColors]?.text}`}>
                    {categoryLabels[cat]}
                  </span>
                  <span className="text-[10px] text-[#5F6B78]">({metrics.length})</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-3">
                  {metrics.map(m => <MetricCard key={m.id} metric={m} categoryColors={categoryColors} />)}
                </div>
              </div>
            )
          ))}
        </div>

        {/* SIGNALS */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
          <div className="flex items-center justify-between pb-4 border-b border-[#26313D]/70">
            <div className="flex items-center gap-2.5">
              <div className={`w-2.5 h-2.5 rounded-full ${signals.length > 0 ? 'bg-emerald-400' : 'bg-amber-400'}`} />
              <h3 className="text-sm font-bold text-white tracking-wider uppercase">Live MTF Signals</h3>
              <span className="text-xs text-[#8D9AAA] hidden sm:inline">
                {signals.length > 0 ? `(${signals.length})` : '(waiting)'}
              </span>
            </div>
            {signals.length > 0 && (
              <div className="flex items-center gap-2">
                <span className="text-xs text-[#8D9AAA] font-mono mr-2">Page {signalPage + 1}/{totalSignalPages}</span>
                <button onClick={() => handleSignalPageChange('prev')} disabled={signalPage === 0}
                  className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] border border-[#26313D] disabled:opacity-30">
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <button onClick={() => handleSignalPageChange('next')} disabled={signalPage >= totalSignalPages - 1}
                  className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] border border-[#26313D] disabled:opacity-30">
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5 mt-4">
            {signals.length === 0 ? (
              <div className="col-span-full py-12 text-center text-[#5F6B78]">
                <div className="text-5xl mb-4">📡</div>
                <p className="text-base font-medium">No Signals Available</p>
                <p className="text-sm mt-1">Waiting for data from cognitive engine...</p>
              </div>
            ) : (
              currentSignals.map(sig => <SignalCard key={sig.id} signal={sig} />)
            )}
          </div>
        </div>

        {/* MARKET + INSIGHTS */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-blue-400" />
                Live Market Tickers
              </h3>
              <button onClick={() => onNavigate('Market')}
                className="text-xs font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1">
                View All <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>
            <div className="divide-y divide-[#26313D]/50 mt-2">
              {tickers.length === 0 ? (
                <div className="py-8 text-center text-[#5F6B78]">
                  <p className="text-sm font-medium">No market data available</p>
                </div>
              ) : (
                tickers.slice(0, 5).map(t => <TickerRow key={t.pair} ticker={t} />)
              )}
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
                <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-purple-400" />
                  Cognitive Insights
                </h3>
                <span className="text-[10px] font-mono text-[#5F6B78]">{insights.length || 0} active</span>
              </div>
              <div className="space-y-3 mt-3.5">
                {insights.length === 0 ? (
                  <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] text-center text-[#5F6B78]">
                    <div className="text-3xl mb-2">🧠</div>
                    <p className="text-sm font-medium">No insights yet</p>
                  </div>
                ) : (
                  insights.slice(0, 3).map(ins => <InsightCard key={ins.id} insight={ins} />)
                )}
              </div>
            </div>
            <button onClick={() => onNavigate('Reflection')}
              className="w-full mt-4 py-2 rounded-xl bg-purple-600/20 hover:bg-purple-600 border border-purple-500/40 text-purple-300 hover:text-white text-xs font-bold transition-all">
              Open Cognitive Mirror
            </button>
          </div>
        </div>
      </div>
    </DashboardErrorBoundary>
  );
};

DashboardView.displayName = 'DashboardView';

export default DashboardView;
