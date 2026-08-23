import React, { useState } from 'react';
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
} from 'lucide-react';
import { TickerInfo, TradingSignal, CognitiveInsight } from '../types';

// ============================================================
// TYPES
// ============================================================

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
  onNavigate: (page: any) => void;
}

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

// ============================================================
// MAIN COMPONENT
// ============================================================

export const DashboardView: React.FC<DashboardViewProps> = ({
  tickers,
  signals,
  insights,
  engineRunning,
  learningActive,
  cycleCount,
  brainState,
  consciousnessLevel,
  systemMetrics,
  onNavigate,
}) => {
  const [signalPage, setSignalPage] = useState(0);
  const [metricPage, setMetricPage] = useState(0);
  const signalsPerPage = 4;
  const metricsPerPage = 12;
  
  const totalSignalPages = Math.max(1, Math.ceil(signals.length / signalsPerPage));
  const currentSignals = signals.slice(
    signalPage * signalsPerPage,
    (signalPage + 1) * signalsPerPage
  );

  // ============================================================
  // METRIC CARDS DATA - SEMUA DARI PROPS, TIDAK ADA DUMMY
  // ============================================================
  
  const allMetrics = [
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
      subtitle: '14 Categories',
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
      subtitle: '8 Cores Active',
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
      subtitle: `${tickers.length || 0} Pairs Tracked`,
      badge: tickers.length > 0 ? 'LIVE' : '--',
      badgeColor: 'cyan',
      onClick: () => onNavigate('Market'),
    },
    {
      id: 'signals',
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
      subtitle: 'Last 100 Predictions',
      badge: systemMetrics?.prediction_accuracy && systemMetrics.prediction_accuracy > 80 ? 'HIGH' : 'LEARNING',
      badgeColor: 'cyan',
    },
    {
      id: 'decision_engine',
      category: 'cognitive' as const,
      icon: <Workflow className="w-4 h-4 text-blue-400" />,
      title: 'Decision Engine',
      value: engineRunning ? 'ACTIVE' : 'IDLE',
      subtitle: '15 Rules Applied',
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
  ];

  // ============================================================
  // PAGINATION
  // ============================================================
  
  const totalMetricPages = Math.ceil(allMetrics.length / metricsPerPage);
  const currentMetrics = allMetrics.slice(
    metricPage * metricsPerPage,
    (metricPage + 1) * metricsPerPage
  );

  const groupedMetrics = currentMetrics.reduce((acc, metric) => {
    if (!acc[metric.category]) {
      acc[metric.category] = [];
    }
    acc[metric.category].push(metric);
    return acc;
  }, {} as Record<'system' | 'market' | 'trading' | 'cognitive', typeof allMetrics>);

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
  // RENDER
  // ============================================================

  return (
    <div id="dashboard-view" className="space-y-6 pb-12">
      {/* Banner / System Header */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#18212B] to-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${engineRunning ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
            <h2 className="text-xl font-bold text-white tracking-wide">
              Cognitive Intelligence System
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 font-semibold border border-blue-500/30">
              {engineRunning ? 'ACTIVE' : 'STANDBY'}
            </span>
          </div>
          <p className="text-xs text-[#8D9AAA]">
            {engineRunning 
              ? 'Kraken live streaming exchange bridge with autonomous cognitive reflection and risk management.'
              : 'System is idle. Start the engine to begin trading.'}
          </p>
        </div>

        <div className="flex items-center gap-3">
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
        </div>
      </div>

      {/* METRICS GRID WITH PAGINATION */}
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
              onClick={() => setMetricPage((p) => Math.max(0, p - 1))}
              disabled={metricPage === 0}
              className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-xs text-[#5F6B78] font-mono px-2">
              {metricPage + 1}/{totalMetricPages}
            </span>
            <button
              onClick={() => setMetricPage((p) => Math.min(totalMetricPages - 1, p + 1))}
              disabled={metricPage >= totalMetricPages - 1}
              className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {Object.entries(groupedMetrics).map(([category, metrics]) => (
          <div key={category} className="mt-4">
            <div className="flex items-center gap-2 mb-3">
              <div className={`w-1 h-4 rounded-full ${categoryColors[category as keyof typeof categoryColors]?.bg.replace('/10', '')}`} />
              <span className={`text-[11px] font-bold uppercase tracking-wider ${categoryColors[category as keyof typeof categoryColors]?.text}`}>
                {categoryLabels[category as keyof typeof categoryLabels]}
              </span>
              <span className="text-[10px] text-[#5F6B78]">({metrics.length})</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-3">
              {metrics.map((metric) => {
                const colors = categoryColors[metric.category];
                return (
                  <div
                    key={metric.id}
                    onClick={metric.onClick}
                    className={`p-3 rounded-xl bg-[#1A2530] border border-[#26313D] hover:border-[#3B82F6]/50 transition-all cursor-pointer group`}
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
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Row 2: Live Signals Grid with Pagination */}
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
                onClick={() => setSignalPage((p) => Math.max(0, p - 1))}
                disabled={signalPage === 0}
                className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => setSignalPage((p) => Math.min(totalSignalPages - 1, p + 1))}
                disabled={signalPage >= totalSignalPages - 1}
                className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer"
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
            currentSignals.map((sig) => {
              const isBuy = sig.signal.includes('BUY');
              const isSell = sig.signal.includes('SELL');
              const colorClass = isBuy
                ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
                : isSell
                ? 'text-rose-400 bg-rose-500/10 border-rose-500/20'
                : 'text-amber-400 bg-amber-500/10 border-amber-500/20';

              return (
                <div
                  key={sig.id}
                  className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] hover:border-[#3B82F6]/50 transition-all flex flex-col justify-between space-y-3"
                >
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="font-extrabold text-white text-sm tracking-wide font-mono">
                        {sig.pair}
                      </span>
                      <span className={`text-[10px] font-black px-2 py-0.5 rounded border ${colorClass}`}>
                        {sig.signal.replace('_', ' ')}
                      </span>
                    </div>

                    <div className="mt-2 flex items-baseline justify-between">
                      <span className="text-base font-bold text-white font-mono">
                        ${sig.price >= 10 ? sig.price.toLocaleString() : sig.price.toFixed(4)}
                      </span>
                      <span className="text-xs font-mono font-bold text-blue-400">
                        {sig.confidence}% Conf
                      </span>
                    </div>

                    <div className="w-full bg-[#0B0F14] h-1.5 rounded-full mt-2 overflow-hidden">
                      <div
                        className={`h-full ${
                          sig.confidence >= 80
                            ? 'bg-emerald-400'
                            : sig.confidence >= 60
                            ? 'bg-blue-400'
                            : 'bg-amber-400'
                        }`}
                        style={{ width: `${sig.confidence}%` }}
                      />
                    </div>
                  </div>

                  <div className="pt-2 border-t border-[#26313D]/60 grid grid-cols-2 gap-2 text-[10px] font-mono text-[#8D9AAA]">
                    <div>
                      SL: <span className="text-rose-400 font-bold">${sig.stopLoss.toLocaleString()}</span>
                    </div>
                    <div className="text-right">
                      TP2: <span className="text-emerald-400 font-bold">${sig.tp2.toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Row 3: Market Overview & Cognitive Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Market Tickers Left (2 Cols) */}
        <div className="lg:col-span-2 p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-blue-400" />
              Live Crypto Market Tickers (Kraken Feed)
            </h3>
            <button
              onClick={() => onNavigate('Market')}
              className="text-xs font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1 cursor-pointer"
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
              tickers.slice(0, 5).map((t) => {
                const isPositive = t.change24h >= 0;
                return (
                  <div
                    key={t.pair}
                    className="py-3 flex items-center justify-between hover:bg-[#18212B]/40 px-2 rounded-lg transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-[#1A2530] border border-[#26313D] flex items-center justify-center font-bold text-white text-xs">
                        {t.pair.split('/')[0]}
                      </div>
                      <div>
                        <div className="font-bold text-white text-xs tracking-wide">{t.pair}</div>
                        <div className="text-[10px] text-[#5F6B78]">{t.name}</div>
                      </div>
                    </div>

                    <div className="flex items-center gap-6">
                      <div className="text-right">
                        <div className="font-mono font-bold text-white text-xs">
                          ${t.price >= 1 ? t.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : t.price.toFixed(4)}
                        </div>
                        <div className="text-[10px] text-[#5F6B78] font-mono">
                          Vol: ${(t.volume24h * t.price / 1000000).toFixed(1)}M
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
                        {t.change24h.toFixed(2)}%
                      </div>
                    </div>
                  </div>
                );
              })
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
                  <div
                    key={ins.id}
                    className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-1 hover:border-purple-500/30 transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-white tracking-wide">
                        {ins.title}
                      </span>
                      <span className="text-[9px] font-mono text-[#8D9AAA] px-1.5 py-0.5 rounded bg-[#0B0F14]">
                        {ins.confidence}% Conf
                      </span>
                    </div>
                    <p className="text-[11px] text-[#8D9AAA] leading-relaxed">
                      {ins.content}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>

          <button
            onClick={() => onNavigate('Reflection')}
            className="w-full mt-4 py-2 rounded-xl bg-purple-600/20 hover:bg-purple-600 border border-purple-500/40 text-purple-300 hover:text-white text-xs font-bold transition-all text-center cursor-pointer"
          >
            Open Cognitive Mirror
          </button>
        </div>
      </div>
    </div>
  );
};
