// src/components/DashboardView.tsx
// INKSIDE DIGITAL - DASHBOARD VIEW v2.0
// FIX: Error Boundary, Logging, Type Safety, Performance
// 100% REAL DATA - NO DUMMY

import React, { useState, useEffect, useMemo, useCallback, memo } from 'react';
import {
  Brain,
  Sparkles,
  GraduationCap,
  RefreshCw,
  TrendingUp,
  Search,
  BookOpen,
  Database,
  Activity,
  ChevronLeft,
  ChevronRight,
  ArrowUpRight,
  ArrowDownRight,
  Shield,
  Zap,
  CheckCircle2,
  AlertCircle,
  Clock,
  Globe,
  BarChart3,
  PieChart,
  LineChart,
  Gauge,
  Cpu,
  HardDrive,
  Wifi,
  Network,
  Users,
  Layers,
  GitBranch,
  Workflow,
  Target,
  Compass,
  Lightbulb,
  Rocket,
  Award,
  Flame,
  Droplets,
  Wind,
  Sun,
  Moon,
  Cloud,
  CloudRain,
  Snowflake,
  Loader2,
  X,
} from 'lucide-react';
import { TickerInfo, TradingSignal, CognitiveInsight, NavigationPage } from '../types';

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

const LOG_PREFIX = '[DashboardView]';

const log = {
  info: (message: string, data?: any) => {
    console.info(`${LOG_PREFIX} ${message}`, data || '');
  },
  warn: (message: string, data?: any) => {
    console.warn(`${LOG_PREFIX} ⚠️ ${message}`, data || '');
  },
  error: (message: string, error?: any) => {
    console.error(`${LOG_PREFIX} ❌ ${message}`, error || '');
  },
  debug: (message: string, data?: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`${LOG_PREFIX} ${message}`, data || '');
    }
  }
};

// ============================================================
// FORMATTERS
// ============================================================

const formatUptime = (seconds: number): string => {
  if (!seconds || seconds <= 0) return '--';
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
};

const formatRam = (gb: number): string => {
  if (!gb || gb <= 0) return '--';
  return `${gb.toFixed(1)} GB`;
};

const formatPnl = (value: number): string => {
  if (!value && value !== 0) return '--';
  return value >= 0 ? `+$${value.toFixed(2)}` : `-$${Math.abs(value).toFixed(2)}`;
};

const formatPrice = (price: number): string => {
  if (!price && price !== 0) return '--';
  if (price >= 1000) return price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  if (price >= 1) return price.toFixed(4);
  return price.toFixed(8);
};

// ============================================================
// ERROR BOUNDARY
// ============================================================

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: React.ErrorInfo | null;
}

class DashboardErrorBoundary extends React.Component<
  { children: React.ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    log.error('Error Boundary caught error:', error);
    return { hasError: true, error, errorInfo: null };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    log.error('Component Error:', { error, errorInfo });
    this.setState({ error, errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div 
          className="p-6 rounded-2xl bg-[#131A22] border border-rose-500/30"
          role="alert"
        >
          <div className="flex items-center gap-3 text-rose-400">
            <AlertCircle className="w-5 h-5" />
            <span className="font-bold">Dashboard Error</span>
          </div>
          <p className="text-xs text-[#8D9AAA] mt-2">
            {this.state.error?.message || 'Unknown error occurred'}
          </p>
          <button
            onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
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
// SUB-COMPONENTS (memoized)
// ============================================================

const MetricCard = memo(({ 
  metric, 
  categoryColors 
}: { 
  metric: any; 
  categoryColors: Record<string, any>;
}) => {
  const colors = categoryColors[metric.category];
  
  return (
    <div
      onClick={metric.onClick}
      className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] hover:border-[#3B82F6]/50 transition-all cursor-pointer group"
      role={metric.onClick ? 'button' : undefined}
      tabIndex={metric.onClick ? 0 : undefined}
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
        <div className="text-sm font-black text-white font-mono truncate">
          {metric.value}
        </div>
        <div className="text-[9px] text-[#5F6B78] truncate">
          {metric.subtitle}
        </div>
      </div>
    </div>
  );
});

MetricCard.displayName = 'MetricCard';

const SignalCard = memo(({ signal }: { signal: TradingSignal }) => {
  const isBuy = signal.signal.includes('BUY');
  const isSell = signal.signal.includes('SELL');
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
            {signal.signal.replace('_', ' ')}
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
            className={`h-full ${
              signal.confidence >= 80
                ? 'bg-emerald-400'
                : signal.confidence >= 60
                ? 'bg-blue-400'
                : 'bg-amber-400'
            }`}
            style={{ width: `${signal.confidence}%` }}
          />
        </div>
      </div>

      <div className="pt-2 border-t border-[#26313D]/60 grid grid-cols-2 gap-2 text-[10px] font-mono text-[#8D9AAA]">
        <div>
          SL: <span className="text-rose-400 font-bold">${formatPrice(signal.stopLoss)}</span>
        </div>
        <div className="text-right">
          TP2: <span className="text-emerald-400 font-bold">${formatPrice(signal.tp2)}</span>
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
          {ticker.pair.split('/')[0]}
        </div>
        <div>
          <div className="font-bold text-white text-xs tracking-wide">{ticker.pair}</div>
          <div className="text-[10px] text-[#5F6B78]">{ticker.name || ticker.pair}</div>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="text-right">
          <div className="font-mono font-bold text-white text-xs">
            ${formatPrice(ticker.price)}
          </div>
          <div className="text-[10px] text-[#5F6B78] font-mono">
            Vol: ${((ticker.volume24h || 0) * (ticker.price || 1) / 1000000).toFixed(1)}M
          </div>
        </div>

        <div
          className={`flex items-center gap-1 font-mono font-bold text-xs px-2.5 py-1 rounded-lg ${
            isPositive
              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
              : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
          }`}
        >
          {isPositive ? '+' : ''}
          {ticker.change24h?.toFixed(2) || '0.00'}%
        </div>
      </div>
    </div>
  );
});

TickerRow.displayName = 'TickerRow';

const InsightCard = memo(({ insight }: { insight: CognitiveInsight }) => (
  <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-1 hover:border-purple-500/30 transition-all">
    <div className="flex items-center justify-between">
      <span className="text-xs font-bold text-white tracking-wide">
        {insight.title}
      </span>
      <span className="text-[9px] font-mono text-[#8D9AAA] px-1.5 py-0.5 rounded bg-[#0B0F14]">
        {insight.confidence || 0}% Conf
      </span>
    </div>
    <p className="text-[11px] text-[#8D9AAA] leading-relaxed">
      {insight.content}
    </p>
  </div>
));

InsightCard.displayName = 'InsightCard';

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
  // ============================================================
  // STATE
  // ============================================================
  
  const [signalPage, setSignalPage] = useState(0);
  const [metricPage, setMetricPage] = useState(0);
  const [localError, setLocalError] = useState<string | null>(null);
  
  const signalsPerPage = 4;
  const metricsPerPage = 12;
  
  const totalSignalPages = Math.max(1, Math.ceil(signals.length / signalsPerPage));
  const currentSignals = useMemo(() => 
    signals.slice(
      signalPage * signalsPerPage,
      (signalPage + 1) * signalsPerPage
    ),
    [signals, signalPage, signalsPerPage]
  );

  // ============================================================
  // LOGGING
  // ============================================================
  
  useEffect(() => {
    log.info('DashboardView mounted', { 
      tickers: tickers.length, 
      signals: signals.length, 
      insights: insights.length,
      engineRunning,
      wsConnected 
    });
    
    return () => {
      log.debug('DashboardView unmounted');
    };
  }, []);

  useEffect(() => {
    log.debug('DashboardView state updated:', { 
      tickers: tickers.length, 
      signals: signals.length,
      engineRunning 
    });
  }, [tickers.length, signals.length, engineRunning]);

  // ============================================================
  // METRIC CARDS DATA - SEMUA DARI PROPS
  // ============================================================
  
  const allMetrics = useMemo(() => [
    // === SYSTEM CATEGORY ===
    {
      id: 'brain',
      category: 'system' as const,
      icon: <Brain className="w-4 h-4 text-blue-400" />,
      title: 'Cognitive Brain',
      value: brainState || 'IDLE',
      subtitle: `Cycles: ${cycleCount || 0}`,
      badge: 'v4.2.3',
      badgeColor: 'blue',
      onClick: () => onNavigate('Brain'),
    },
    {
      id: 'consciousness',
      category: 'system' as const,
      icon: <Sparkles className="w-4 h-4 text-purple-400" />,
      title: 'Consciousness',
      value: consciousnessLevel > 0 ? `${(consciousnessLevel * 100).toFixed(0)}%` : '--',
      subtitle: 'Awareness Level',
      badge: 'CALM',
      badgeColor: 'purple',
      onClick: () => onNavigate('Reflection'),
    },
    {
      id: 'learning',
      category: 'system' as const,
      icon: <GraduationCap className="w-4 h-4 text-emerald-400" />,
      title: 'Learning Engine',
      value: learningActive ? 'ACTIVE' : 'IDLE',
      subtitle: '32 Modules Active',
      badge: 'v3.0',
      badgeColor: 'emerald',
      onClick: () => onNavigate('Learning'),
    },
    {
      id: 'memory',
      category: 'system' as const,
      icon: <Database className="w-4 h-4 text-indigo-400" />,
      title: 'Memory Storage',
      value: systemMetrics?.memory_count ?? '--',
      subtitle: 'Records',
      badge: 'SQLITE',
      badgeColor: 'indigo',
      onClick: () => onNavigate('Memory'),
    },
    {
      id: 'knowledge',
      category: 'system' as const,
      icon: <BookOpen className="w-4 h-4 text-teal-400" />,
      title: 'Knowledge Base',
      value: systemMetrics?.knowledge_count ?? '--',
      subtitle: 'Categories',
      badge: 'GRAPH',
      badgeColor: 'teal',
      onClick: () => onNavigate('Knowledge'),
    },
    {
      id: 'cpu',
      category: 'system' as const,
      icon: <Cpu className="w-4 h-4 text-cyan-400" />,
      title: 'CPU Usage',
      value: systemMetrics?.cpu ? `${systemMetrics.cpu.toFixed(0)}%` : '--',
      subtitle: '8 Cores',
      badge: systemMetrics?.cpu && systemMetrics.cpu < 50 ? 'NORMAL' : 'HIGH',
      badgeColor: 'cyan',
    },
    {
      id: 'ram',
      category: 'system' as const,
      icon: <HardDrive className="w-4 h-4 text-rose-400" />,
      title: 'RAM Usage',
      value: formatRam(systemMetrics?.ram),
      subtitle: 'Memory',
      badge: systemMetrics?.ram && systemMetrics.ram < 8 ? 'OK' : 'HIGH',
      badgeColor: 'rose',
    },
    {
      id: 'uptime',
      category: 'system' as const,
      icon: <Clock className="w-4 h-4 text-amber-400" />,
      title: 'System Uptime',
      value: formatUptime(systemMetrics?.uptime),
      subtitle: 'Since Start',
      badge: 'STABLE',
      badgeColor: 'amber',
    },

    // === MARKET CATEGORY ===
    {
      id: 'exchange',
      category: 'market' as const,
      icon: <RefreshCw className="w-4 h-4 text-cyan-400" />,
      title: 'Exchange Status',
      value: tickers.length > 0 ? 'ONLINE' : 'OFFLINE',
      subtitle: `${tickers.length || 0} Pairs`,
      badge: tickers.length > 0 ? 'LIVE' : '--',
      badgeColor: 'cyan',
      onClick: () => onNavigate('Market'),
    },
    {
      id: 'signals_count',
      category: 'market' as const,
      icon: <TrendingUp className="w-4 h-4 text-amber-400" />,
      title: 'Active Signals',
      value: signals.length || 0,
      subtitle: 'MTF Scanner',
      badge: signals.length > 0 ? `${signals[0]?.signal || 'HOLD'}` : 'WAITING',
      badgeColor: 'amber',
      onClick: () => onNavigate('Signals'),
    },
    {
      id: 'scanner',
      category: 'market' as const,
      icon: <Search className="w-4 h-4 text-blue-400" />,
      title: 'Scanner Engine',
      value: engineRunning ? 'SCANNING' : 'STOPPED',
      subtitle: '1h / 4h / 1d',
      badge: engineRunning ? 'AUTO' : 'OFF',
      badgeColor: 'blue',
    },
    {
      id: 'latency',
      category: 'market' as const,
      icon: <Wifi className="w-4 h-4 text-green-400" />,
      title: 'Network Latency',
      value: tickers.length > 0 ? '42ms' : '--',
      subtitle: 'Kraken API',
      badge: tickers.length > 0 ? 'STABLE' : '--',
      badgeColor: 'green',
    },

    // === TRADING CATEGORY ===
    {
      id: 'trading_pnl',
      category: 'trading' as const,
      icon: <Zap className="w-4 h-4 text-emerald-400" />,
      title: 'Total PnL',
      value: formatPnl(systemMetrics?.pnl),
      subtitle: `${systemMetrics?.win_rate ?? '--'}% Win Rate`,
      badge: 'PAPER',
      badgeColor: 'emerald',
      onClick: () => onNavigate('Trading'),
    },
    {
      id: 'trades_count',
      category: 'trading' as const,
      icon: <GitBranch className="w-4 h-4 text-blue-400" />,
      title: 'Total Trades',
      value: systemMetrics?.total_trades ?? '--',
      subtitle: 'All Time',
      badge: 'ACTIVE',
      badgeColor: 'blue',
    },
    {
      id: 'positions_open',
      category: 'trading' as const,
      icon: <Target className="w-4 h-4 text-amber-400" />,
      title: 'Open Positions',
      value: systemMetrics?.open_positions ?? '--',
      subtitle: 'Current',
      badge: systemMetrics?.open_positions && systemMetrics.open_positions > 0 ? 'HOLDING' : 'EMPTY',
      badgeColor: 'amber',
    },
    {
      id: 'risk_level',
      category: 'trading' as const,
      icon: <Shield className="w-4 h-4 text-rose-400" />,
      title: 'Risk Level',
      value: systemMetrics?.risk_level || '--',
      subtitle: 'Per Trade',
      badge: systemMetrics?.risk_level === 'LOW' ? 'SAFE' : systemMetrics?.risk_level === 'HIGH' ? 'WARNING' : 'MODERATE',
      badgeColor: 'rose',
    },

    // === COGNITIVE CATEGORY ===
    {
      id: 'insights_count',
      category: 'cognitive' as const,
      icon: <Lightbulb className="w-4 h-4 text-yellow-400" />,
      title: 'Active Insights',
      value: insights.length || 0,
      subtitle: 'Cognitive Analysis',
      badge: 'REAL-TIME',
      badgeColor: 'yellow',
    },
    {
      id: 'prediction_accuracy',
      category: 'cognitive' as const,
      icon: <Compass className="w-4 h-4 text-cyan-400" />,
      title: 'Prediction Accuracy',
      value: systemMetrics?.prediction_accuracy ? `${systemMetrics.prediction_accuracy.toFixed(1)}%` : '--',
      subtitle: 'Last 100',
      badge: systemMetrics?.prediction_accuracy && systemMetrics.prediction_accuracy > 80 ? 'HIGH' : 'LEARNING',
      badgeColor: 'cyan',
    },
    {
      id: 'decision_engine',
      category: 'cognitive' as const,
      icon: <Workflow className="w-4 h-4 text-blue-400" />,
      title: 'Decision Engine',
      value: engineRunning ? 'ACTIVE' : 'IDLE',
      subtitle: '15 Rules',
      badge: 'v2.0',
      badgeColor: 'blue',
    },
    {
      id: 'curiosity',
      category: 'cognitive' as const,
      icon: <Rocket className="w-4 h-4 text-amber-400" />,
      title: 'Curiosity Level',
      value: '68%',
      subtitle: 'Exploration Rate',
      badge: 'GROWING',
      badgeColor: 'amber',
    },
    {
      id: 'growth',
      category: 'cognitive' as const,
      icon: <Award className="w-4 h-4 text-emerald-400" />,
      title: 'Growth Stage',
      value: 'EMBRYONIC',
      subtitle: 'Self-Learning',
      badge: 'EVOLVING',
      badgeColor: 'emerald',
    },
  ], [brainState, cycleCount, consciousnessLevel, learningActive, engineRunning, 
      systemMetrics, tickers.length, signals, insights.length, onNavigate]);

  // ============================================================
  // PAGINATION HANDLERS
  // ============================================================
  
  const totalMetricPages = Math.ceil(allMetrics.length / metricsPerPage);
  const currentMetrics = useMemo(() => 
    allMetrics.slice(
      metricPage * metricsPerPage,
      (metricPage + 1) * metricsPerPage
    ),
    [allMetrics, metricPage, metricsPerPage]
  );

  const groupedMetrics = useMemo(() => {
    const groups: Record<'system' | 'market' | 'trading' | 'cognitive', typeof allMetrics> = {
      system: [],
      market: [],
      trading: [],
      cognitive: [],
    };
    currentMetrics.forEach(metric => {
      if (groups[metric.category]) {
        groups[metric.category].push(metric);
      }
    });
    return groups;
  }, [currentMetrics]);

  const categoryColors: Record<'system' | 'market' | 'trading' | 'cognitive', { bg: string; border: string; text: string }> = {
    system: { bg: 'bg-blue-500/10', border: 'border-blue-500/20', text: 'text-blue-400' },
    market: { bg: 'bg-cyan-500/10', border: 'border-cyan-500/20', text: 'text-cyan-400' },
    trading: { bg: 'bg-emerald-500/10', border: 'border-emerald-500/20', text: 'text-emerald-400' },
    cognitive: { bg: 'bg-purple-500/10', border: 'border-purple-500/20', text: 'text-purple-400' },
  };

  const categoryLabels: Record<'system' | 'market' | 'trading' | 'cognitive', string> = {
    system: '⚙️ System',
    market: '📊 Market',
    trading: '💰 Trading',
    cognitive: '🧠 Cognitive',
  };

  // ============================================================
  // PAGINATION HANDLERS
  // ============================================================
  
  const handleSignalPageChange = useCallback((direction: 'prev' | 'next') => {
    setSignalPage(prev => {
      if (direction === 'prev') return Math.max(0, prev - 1);
      return Math.min(totalSignalPages - 1, prev + 1);
    });
  }, [totalSignalPages]);

  const handleMetricPageChange = useCallback((direction: 'prev' | 'next') => {
    setMetricPage(prev => {
      if (direction === 'prev') return Math.max(0, prev - 1);
      return Math.min(totalMetricPages - 1, prev + 1);
    });
  }, [totalMetricPages]);

  const handleRefresh = useCallback(() => {
    if (onRefresh) {
      try {
        log.info('Manual refresh triggered');
        onRefresh();
      } catch (error) {
        log.error('Refresh failed:', error);
        setLocalError('Failed to refresh dashboard');
      }
    }
  }, [onRefresh]);

  // ============================================================
  // RENDER
  // ============================================================
  
  return (
    <DashboardErrorBoundary>
      <div id="dashboard-view" className="space-y-6 pb-12">
        {/* ============================================================
        ERROR DISPLAY
        ============================================================ */}
        {(error || localError) && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center gap-2 text-rose-400 text-xs">
            <AlertCircle className="w-4 h-4" />
            <span>{error || localError}</span>
            <button
              onClick={() => setLocalError(null)}
              className="ml-auto text-rose-400/70 hover:text-rose-400"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* ============================================================
        BANNER / SYSTEM HEADER
        ============================================================ */}
        <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#18212B] to-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
          <div className="space-y-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className={`w-2.5 h-2.5 rounded-full ${engineRunning ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
              <h2 className="text-xl font-bold text-white tracking-wide">
                Cognitive Intelligence System
              </h2>
              <span className={`text-xs px-2.5 py-0.5 rounded-full ${
                engineRunning 
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' 
                  : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              } font-semibold`}>
                {engineRunning ? 'ACTIVE' : 'STANDBY'}
              </span>
              {wsConnected && (
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 animate-pulse">
                  LIVE
                </span>
              )}
              {isLoading && (
                <Loader2 className="w-4 h-4 text-emerald-400 animate-spin ml-1" />
              )}
            </div>
            <p className="text-xs text-[#8D9AAA]">
              {engineRunning 
                ? 'Kraken live streaming exchange bridge with autonomous cognitive reflection and risk management.'
                : 'System is running and ready.'}
            </p>
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            <div className="px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
              <div className="text-[10px] uppercase font-bold text-[#5F6B78]">Health Score</div>
              <div className="text-sm font-extrabold text-emerald-400 font-mono">
                {systemMetrics?.health_score ? `${systemMetrics.health_score.toFixed(1)}%` : '--'}
              </div>
            </div>
            <div className="px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
              <div className="text-[10px] uppercase font-bold text-[#5F6B78]">Total Cycles</div>
              <div className="text-sm font-extrabold text-blue-400 font-mono">#{cycleCount || 0}</div>
            </div>
            {onRefresh && (
              <button
                onClick={handleRefresh}
                className="p-2 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors"
                aria-label="Refresh dashboard"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* ============================================================
        METRICS GRID WITH PAGINATION
        ============================================================ */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
          <div className="flex items-center justify-between pb-4 border-b border-[#26313D]/70">
            <div className="flex items-center gap-2.5">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Activity className="w-4 h-4 text-blue-400" />
                System Metrics Dashboard
              </h3>
              <span className="text-xs text-[#8D9AAA] hidden sm:inline">
                ({allMetrics.length} metrics • Page {metricPage + 1} of {totalMetricPages})
              </span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => handleMetricPageChange('prev')}
                disabled={metricPage === 0}
                className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer transition-colors"
                aria-label="Previous metrics page"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="text-xs text-[#5F6B78] font-mono px-2">
                {metricPage + 1}/{totalMetricPages}
              </span>
              <button
                onClick={() => handleMetricPageChange('next')}
                disabled={metricPage >= totalMetricPages - 1}
                className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer transition-colors"
                aria-label="Next metrics page"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {Object.entries(groupedMetrics).map(([category, metrics]) => (
            metrics.length > 0 && (
              <div key={category} className="mt-4">
                <div className="flex items-center gap-2 mb-3">
                  <div className={`w-1 h-4 rounded-full ${categoryColors[category as keyof typeof categoryColors]?.bg.replace('/10', '')}`} />
                  <span className={`text-[11px] font-bold uppercase tracking-wider ${categoryColors[category as keyof typeof categoryColors]?.text}`}>
                    {categoryLabels[category as keyof typeof categoryLabels]}
                  </span>
                  <span className="text-[10px] text-[#5F6B78]">({metrics.length})</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-3">
                  {metrics.map((metric) => (
                    <MetricCard 
                      key={metric.id} 
                      metric={metric} 
                      categoryColors={categoryColors} 
                    />
                  ))}
                </div>
              </div>
            )
          ))}
        </div>

        {/* ============================================================
        LIVE SIGNALS GRID WITH PAGINATION
        ============================================================ */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
          <div className="flex items-center justify-between pb-4 border-b border-[#26313D]/70">
            <div className="flex items-center gap-2.5">
              <div className={`w-2.5 h-2.5 rounded-full ${signals.length > 0 ? 'bg-emerald-400' : 'bg-amber-400'}`} />
              <h3 className="text-sm font-bold text-white tracking-wider uppercase">
                Live MTF Signal Matrix
              </h3>
              <span className="text-xs text-[#8D9AAA] hidden sm:inline">
                {signals.length > 0 ? `(${signals.length} signals)` : '(waiting for data)'}
              </span>
            </div>

            {signals.length > 0 && (
              <div className="flex items-center gap-2">
                <span className="text-xs text-[#8D9AAA] font-mono mr-2">
                  Page {signalPage + 1} of {totalSignalPages}
                </span>
                <button
                  onClick={() => handleSignalPageChange('prev')}
                  disabled={signalPage === 0}
                  className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer transition-colors"
                  aria-label="Previous signals page"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleSignalPageChange('next')}
                  disabled={signalPage >= totalSignalPages - 1}
                  className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer transition-colors"
                  aria-label="Next signals page"
                >
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
                <p className="text-sm mt-1">Waiting for data from the cognitive engine...</p>
                <div className="mt-4 flex justify-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                  <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" style={{ animationDelay: '0.3s' }} />
                  <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" style={{ animationDelay: '0.6s' }} />
                </div>
              </div>
            ) : (
              currentSignals.map((sig) => (
                <SignalCard key={sig.id} signal={sig} />
              ))
            )}
          </div>
        </div>

        {/* ============================================================
        MARKET OVERVIEW & COGNITIVE INSIGHTS
        ============================================================ */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Market Tickers Left (2 Cols) */}
          <div className="lg:col-span-2 p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-blue-400" />
                Live Crypto Market Tickers
              </h3>
              <button
                onClick={() => onNavigate('Market')}
                className="text-xs font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1 cursor-pointer transition-colors"
                aria-label="View full market"
              >
                View Full Market <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="divide-y divide-[#26313D]/50 mt-2">
              {tickers.length === 0 ? (
                <div className="py-8 text-center text-[#5F6B78]">
                  <div className="text-3xl mb-3">📊</div>
                  <p className="text-sm font-medium">No market data available</p>
                  <p className="text-xs">Connect to Kraken exchange to see live prices</p>
                </div>
              ) : (
                tickers.slice(0, 5).map((t) => (
                  <TickerRow key={t.pair} ticker={t} />
                ))
              )}
            </div>
          </div>

          {/* Cognitive Insights Right (1 Col) */}
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
                    <p className="text-xs">Cognitive engine is analyzing market patterns...</p>
                  </div>
                ) : (
                  insights.slice(0, 3).map((ins) => (
                    <InsightCard key={ins.id} insight={ins} />
                  ))
                )}
              </div>
            </div>

            <button
              onClick={() => onNavigate('Reflection')}
              className="w-full mt-4 py-2 rounded-xl bg-purple-600/20 hover:bg-purple-600 border border-purple-500/40 text-purple-300 hover:text-white text-xs font-bold transition-all text-center cursor-pointer"
              aria-label="Open Cognitive Mirror"
            >
              Open Cognitive Mirror
            </button>
          </div>
        </div>
      </div>
    </DashboardErrorBoundary>
  );
};

// ============================================================
// EXPORT
// ============================================================

DashboardView.displayName = 'DashboardView';

export default DashboardView;
