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
} from 'lucide-react';
import { TickerInfo, TradingSignal, CognitiveInsight } from '../types';

interface DashboardViewProps {
  tickers: TickerInfo[];
  signals: TradingSignal[];
  insights: CognitiveInsight[];
  engineRunning: boolean;
  learningActive: boolean;
  cycleCount: number;
  brainState: string;
  consciousnessLevel: number;
  onNavigate: (page: any) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  tickers,
  signals,
  insights,
  engineRunning,
  learningActive,
  cycleCount,
  brainState,
  consciousnessLevel,
  onNavigate,
}) => {
  const [signalPage, setSignalPage] = useState(0);
  const signalsPerPage = 4;
  const totalPages = Math.ceil(signals.length / signalsPerPage) || 1;
  const currentSignals = signals.slice(
    signalPage * signalsPerPage,
    (signalPage + 1) * signalsPerPage
  );

  return (
    <div id="dashboard-view" className="space-y-6 pb-12">
      {/* Banner / System Header */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#18212B] to-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <h2 className="text-xl font-bold text-white tracking-wide">
              Cognitive Intelligence System
            </h2>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 font-semibold border border-blue-500/30">
              REAL-TIME MTF SCANNER
            </span>
          </div>
          <p className="text-xs text-[#8D9AAA]">
            Kraken live streaming exchange bridge with autonomous cognitive reflection and risk management.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
            <div className="text-[10px] uppercase font-bold text-[#5F6B78]">Health Score</div>
            <div className="text-sm font-extrabold text-emerald-400 font-mono">98.4%</div>
          </div>
          <div className="px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
            <div className="text-[10px] uppercase font-bold text-[#5F6B78]">Total Cycles</div>
            <div className="text-sm font-extrabold text-blue-400 font-mono">#{cycleCount}</div>
          </div>
        </div>
      </div>

      {/* Row 1: Primary System Status Metrics (3x3 Grid) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Brain Card */}
        <div
          id="metric-card-brain"
          onClick={() => onNavigate('Brain')}
          className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-blue-500/50 transition-all cursor-pointer group shadow-sm"
        >
          <div className="flex items-center justify-between text-[#8D9AAA]">
            <span className="text-xs font-semibold flex items-center gap-2">
              <Brain className="w-4 h-4 text-blue-400 group-hover:scale-110 transition-transform" />
              Cognitive Brain
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
              v4.2.3
            </span>
          </div>
          <div className="mt-2.5 flex items-baseline justify-between">
            <span className="text-2xl font-black text-white font-mono">{brainState}</span>
            <span className="text-xs text-emerald-400 font-bold">98.5% Success</span>
          </div>
          <div className="mt-1 text-[11px] text-[#5F6B78]">
            Cycles: <strong className="text-[#8D9AAA]">{cycleCount}</strong> | Errors: <strong className="text-emerald-400">0</strong>
          </div>
        </div>

        {/* Consciousness Card */}
        <div
          id="metric-card-consciousness"
          onClick={() => onNavigate('Reflection')}
          className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-purple-500/50 transition-all cursor-pointer group shadow-sm"
        >
          <div className="flex items-center justify-between text-[#8D9AAA]">
            <span className="text-xs font-semibold flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400 group-hover:scale-110 transition-transform" />
              Consciousness Awareness
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">
              v4.0
            </span>
          </div>
          <div className="mt-2.5 flex items-baseline justify-between">
            <span className="text-2xl font-black text-white font-mono">
              {(consciousnessLevel * 100).toFixed(0)}%
            </span>
            <span className="text-xs text-purple-300 font-bold">😌 CALM</span>
          </div>
          <div className="mt-1 text-[11px] text-[#5F6B78]">
            Curiosity: <strong className="text-[#8D9AAA]">68%</strong> | Insight Depth: <strong className="text-[#8D9AAA]">74%</strong>
          </div>
        </div>

        {/* Learning Engine Card */}
        <div
          id="metric-card-learning"
          onClick={() => onNavigate('Learning')}
          className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-emerald-500/50 transition-all cursor-pointer group shadow-sm"
        >
          <div className="flex items-center justify-between text-[#8D9AAA]">
            <span className="text-xs font-semibold flex items-center gap-2">
              <GraduationCap className="w-4 h-4 text-emerald-400 group-hover:scale-110 transition-transform" />
              Learning Engine
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              v3.0
            </span>
          </div>
          <div className="mt-2.5 flex items-baseline justify-between">
            <span className="text-2xl font-black text-white font-mono">
              {learningActive ? 'ACTIVE' : 'IDLE'}
            </span>
            <span className="text-xs text-emerald-400 font-bold">32 Modules</span>
          </div>
          <div className="mt-1 text-[11px] text-[#5F6B78]">
            Autonomous RSS: <strong className="text-emerald-400">18 Feeds</strong> | Rate: <strong className="text-[#8D9AAA]">0.10</strong>
          </div>
        </div>

        {/* Exchange Card */}
        <div
          id="metric-card-exchange"
          onClick={() => onNavigate('Market')}
          className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-cyan-500/50 transition-all cursor-pointer group shadow-sm"
        >
          <div className="flex items-center justify-between text-[#8D9AAA]">
            <span className="text-xs font-semibold flex items-center gap-2">
              <RefreshCw className="w-4 h-4 text-cyan-400 group-hover:rotate-180 transition-transform duration-500" />
              Kraken Exchange
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              LIVE
            </span>
          </div>
          <div className="mt-2.5 flex items-baseline justify-between">
            <span className="text-2xl font-black text-emerald-400 font-mono">ONLINE</span>
            <span className="text-xs text-[#8D9AAA]">20 Pairs</span>
          </div>
          <div className="mt-1 text-[11px] text-[#5F6B78]">
            Latency: <strong className="text-emerald-400">42ms</strong> | Rate Limit: <strong className="text-[#8D9AAA]">15 req/s</strong>
          </div>
        </div>

        {/* Signal Radar Card */}
        <div
          id="metric-card-signal"
          onClick={() => onNavigate('Signals')}
          className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-amber-500/50 transition-all cursor-pointer group shadow-sm"
        >
          <div className="flex items-center justify-between text-[#8D9AAA]">
            <span className="text-xs font-semibold flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-amber-400 group-hover:scale-110 transition-transform" />
              Signal Radar
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
              MTF
            </span>
          </div>
          <div className="mt-2.5 flex items-baseline justify-between">
            <span className="text-2xl font-black text-emerald-400 font-mono">
              {signals[0]?.signal || 'BUY'}
            </span>
            <span className="text-xs text-emerald-400 font-bold font-mono">
              {signals[0]?.confidence || 88}% Conf
            </span>
          </div>
          <div className="mt-1 text-[11px] text-[#5F6B78]">
            Active: <strong className="text-[#8D9AAA]">{signals.length} Signals</strong> | Quality: <strong className="text-emerald-400">EXCELLENT</strong>
          </div>
        </div>

        {/* Scanner Card */}
        <div
          id="metric-card-scanner"
          onClick={() => onNavigate('Signals')}
          className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-blue-500/50 transition-all cursor-pointer group shadow-sm"
        >
          <div className="flex items-center justify-between text-[#8D9AAA]">
            <span className="text-xs font-semibold flex items-center gap-2">
              <Search className="w-4 h-4 text-blue-400 group-hover:scale-110 transition-transform" />
              Scanner Engine
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
              AUTO
            </span>
          </div>
          <div className="mt-2.5 flex items-baseline justify-between">
            <span className="text-2xl font-black text-white font-mono">SCANNING</span>
            <span className="text-xs text-blue-400 font-bold">1h / 4h / 1d</span>
          </div>
          <div className="mt-1 text-[11px] text-[#5F6B78]">
            Interval: <strong className="text-[#8D9AAA]">60s</strong> | Worker Pool: <strong className="text-[#8D9AAA]">8 threads</strong>
          </div>
        </div>

        {/* Knowledge Base Card */}
        <div
          id="metric-card-knowledge"
          onClick={() => onNavigate('Knowledge')}
          className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-teal-500/50 transition-all cursor-pointer group shadow-sm"
        >
          <div className="flex items-center justify-between text-[#8D9AAA]">
            <span className="text-xs font-semibold flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-teal-400 group-hover:scale-110 transition-transform" />
              Knowledge Base
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-teal-500/10 text-teal-400 border border-teal-500/20">
              GRAPH
            </span>
          </div>
          <div className="mt-2.5 flex items-baseline justify-between">
            <span className="text-2xl font-black text-white font-mono">1,840</span>
            <span className="text-xs text-teal-300 font-bold">89.2% Conf</span>
          </div>
          <div className="mt-1 text-[11px] text-[#5F6B78]">
            Categories: <strong className="text-[#8D9AAA]">14</strong> | Facts: <strong className="text-[#8D9AAA]">1,280</strong>
          </div>
        </div>

        {/* Memory System Card */}
        <div
          id="metric-card-memory"
          onClick={() => onNavigate('Memory')}
          className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-indigo-500/50 transition-all cursor-pointer group shadow-sm"
        >
          <div className="flex items-center justify-between text-[#8D9AAA]">
            <span className="text-xs font-semibold flex items-center gap-2">
              <Database className="w-4 h-4 text-indigo-400 group-hover:scale-110 transition-transform" />
              Long-Term Memory
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              SQLITE
            </span>
          </div>
          <div className="mt-2.5 flex items-baseline justify-between">
            <span className="text-2xl font-black text-white font-mono">2,450</span>
            <span className="text-xs text-indigo-300 font-bold">12.4 MB</span>
          </div>
          <div className="mt-1 text-[11px] text-[#5F6B78]">
            Short: <strong className="text-[#8D9AAA]">50</strong> | Long: <strong className="text-[#8D9AAA]">2,400</strong> | Semantic: <strong className="text-[#8D9AAA]">420</strong>
          </div>
        </div>

        {/* Performance Card */}
        <div
          id="metric-card-performance"
          onClick={() => onNavigate('Trading')}
          className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-emerald-500/50 transition-all cursor-pointer group shadow-sm"
        >
          <div className="flex items-center justify-between text-[#8D9AAA]">
            <span className="text-xs font-semibold flex items-center gap-2">
              <Zap className="w-4 h-4 text-emerald-400 group-hover:scale-110 transition-transform" />
              Trading PnL & Win Rate
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              PAPER
            </span>
          </div>
          <div className="mt-2.5 flex items-baseline justify-between">
            <span className="text-2xl font-black text-emerald-400 font-mono">+$335.58</span>
            <span className="text-xs text-emerald-400 font-bold font-mono">78.5% Win</span>
          </div>
          <div className="mt-1 text-[11px] text-[#5F6B78]">
            Total Trades: <strong className="text-[#8D9AAA]">42</strong> | Open: <strong className="text-blue-400">2 Positions</strong>
          </div>
        </div>
      </div>

      {/* Row 2: Live Signals Grid with Pagination */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
        <div className="flex items-center justify-between pb-4 border-b border-[#26313D]/70">
          <div className="flex items-center gap-2.5">
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
            <h3 className="text-sm font-bold text-white tracking-wider uppercase">
              Live MTF Signal Matrix
            </h3>
            <span className="text-xs text-[#8D9AAA] hidden sm:inline">
              (Multi-Timeframe 5m / 15m / 1h / 4h / 1d)
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-[#8D9AAA] font-mono mr-2">
              Page {signalPage + 1} of {totalPages}
            </span>
            <button
              onClick={() => setSignalPage((p) => Math.max(0, p - 1))}
              disabled={signalPage === 0}
              className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => setSignalPage((p) => Math.min(totalPages - 1, p + 1))}
              disabled={signalPage >= totalPages - 1}
              className="p-1.5 rounded-lg bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] disabled:opacity-30 cursor-pointer"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5 mt-4">
          {currentSignals.map((sig) => {
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

                  {/* Confidence Bar */}
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
          })}
        </div>
      </div>

      {/* Row 3: Live Crypto Market Overview & Cognitive Insights */}
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
            {tickers.slice(0, 5).map((t) => {
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
            })}
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
              <span className="text-[10px] font-mono text-[#5F6B78]">{insights.length} active</span>
            </div>

            <div className="space-y-3 mt-3.5">
              {insights.slice(0, 3).map((ins) => (
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
              ))}
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
