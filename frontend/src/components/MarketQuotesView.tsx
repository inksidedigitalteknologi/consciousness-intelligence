// src/components/MarketQuotesView.tsx
// INKSIDE DIGITAL — Market Quotes (Master-Detail Split View)

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  TrendingUp, Search, RefreshCw, Loader2,
  ChevronLeft, ChevronRight, Activity, X,
  ArrowUpRight, ArrowDownRight, BarChart3,
} from 'lucide-react';

import { DecisionCard } from './DecisionCard';
import { PredictionChart } from './PredictionChart';
import { TimeframeGrid } from './TimeframeGrid';
import { LevelsLadder } from './LevelsLadder';
import { BrainStateCard } from './BrainStateCard';

// ============================================================
// TYPES
// ============================================================

interface QuoteRecord {
  key: string;
  ticker: [string, string];
  lastSale: string;
  change: string;
  pctChange: string;
  deltaIndicator: 'up' | 'down';
  volume: string;
  assetclass: string;
}

interface QuotesData {
  date: string;
  records: QuoteRecord[];
  count: number;
  cached: boolean;
  cache_age_sec?: number;
  timestamp: string;
}

interface MarketStatus {
  status: string;
  is_open: boolean;
  is_weekday: boolean;
  time_et: string;
}

interface FullAnalysis {
  symbol: string;
  total_days: number;
  indicators?: any;
  multi_timeframe?: any;
  prediction?: any;
  brain?: any;
  market_decision?: any;
  reflection?: any;
  self_model?: any;
  knowledge_context?: any;
  adaptive?: any;
  experience?: any;
  cached?: boolean;
  error?: string;
}

interface MarketQuotesViewProps {
  wsConnected?: boolean;
}

// ============================================================
// MAIN
// ============================================================

export const MarketQuotesView: React.FC<MarketQuotesViewProps> = ({ wsConnected }) => {
  const [data, setData] = useState<QuotesData | null>(null);
  const [status, setStatus] = useState<MarketStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState<'ALL' | 'UP' | 'DOWN'>('ALL');
  const [page, setPage] = useState(0);
  const perPage = 50;

  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
  const [analysisCache, setAnalysisCache] = useState<Record<string, FullAnalysis>>({});
  const [analysisLoading, setAnalysisLoading] = useState<Record<string, boolean>>({});

  const apiKey = localStorage.getItem('apiKey') || 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ';

  // ============================================================
  // FETCH QUOTES
  // ============================================================

  const fetchAll = useCallback(async (showRefresh = false) => {
    if (showRefresh) setIsRefreshing(true);
    try {
      const [quotesRes, statusRes] = await Promise.all([
        fetch('/api/market/quotes', { headers: { 'X-API-Key': apiKey } }),
        fetch('/api/market/status', { headers: { 'X-API-Key': apiKey } }),
      ]);
      if (quotesRes.ok) setData(await quotesRes.json());
      if (statusRes.ok) setStatus(await statusRes.json());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Fetch failed');
    } finally {
      setLoading(false);
      if (showRefresh) setTimeout(() => setIsRefreshing(false), 300);
    }
  }, [apiKey]);

  // ============================================================
  // FETCH ANALYSIS
  // ============================================================

  const fetchAnalysis = useCallback(async (symbol: string) => {
    if (analysisCache[symbol] || analysisLoading[symbol]) return;

    setAnalysisLoading((prev) => ({ ...prev, [symbol]: true }));

    try {
      const r = await fetch(`/api/market/analyze/${symbol}`, {
        headers: { 'X-API-Key': apiKey },
      });
      if (r.ok) {
        const result = await r.json();
        setAnalysisCache((prev) => ({ ...prev, [symbol]: result }));
      } else {
        setAnalysisCache((prev) => ({
          ...prev,
          [symbol]: { symbol, error: `HTTP ${r.status}` } as any,
        }));
      }
    } catch (err) {
      setAnalysisCache((prev) => ({
        ...prev,
        [symbol]: { symbol, error: String(err) } as any,
      }));
    } finally {
      setAnalysisLoading((prev) => ({ ...prev, [symbol]: false }));
    }
  }, [apiKey, analysisCache, analysisLoading]);

  const selectSymbol = (symbol: string) => {
    setSelectedSymbol(symbol);
    fetchAnalysis(symbol);
  };

  // ============================================================
  // EFFECTS
  // ============================================================

  useEffect(() => {
    fetchAll();
    const interval = status?.is_open ? 60000 : 300000;
    const iv = setInterval(() => fetchAll(), interval);
    return () => clearInterval(iv);
  }, [fetchAll, status?.is_open]);

  // ============================================================
  // FILTER
  // ============================================================

  const safeRecords = Array.isArray(data?.records) ? data.records : [];

  const filtered = useMemo(() => {
    let records = safeRecords;
    if (filter === 'UP') records = records.filter((r) => r.deltaIndicator === 'up');
    else if (filter === 'DOWN') records = records.filter((r) => r.deltaIndicator === 'down');
    if (search.trim()) {
      const q = search.toLowerCase();
      records = records.filter((r) => {
        const symbol = (r.ticker?.[0] || '').toLowerCase();
        const name = (r.ticker?.[1] || '').toLowerCase();
        return symbol.includes(q) || name.includes(q);
      });
    }
    return records;
  }, [safeRecords, filter, search]);

  const totalPages = Math.ceil(filtered.length / perPage);
  const pageRecords = filtered.slice(page * perPage, (page + 1) * perPage);

  const upCount = safeRecords.filter((r) => r.deltaIndicator === 'up').length;
  const downCount = safeRecords.filter((r) => r.deltaIndicator === 'down').length;

  const selectedAnalysis = selectedSymbol ? analysisCache[selectedSymbol] : null;
  const selectedLoading = selectedSymbol ? analysisLoading[selectedSymbol] : false;

  // ============================================================
  // LOADING
  // ============================================================

  if (loading && !data) {
    return (
      <div className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <TrendingUp className="w-5 h-5 text-amber-400" />
          <h2 className="text-lg font-bold text-white">Market Quotes</h2>
        </div>
        <div className="text-center text-gray-400 py-12 glass-card rounded-xl">
          <Loader2 className="w-6 h-6 animate-spin mx-auto mb-3 text-amber-400" />
          <p className="text-lg">Loading S&P 500 data...</p>
        </div>
      </div>
    );
  }

  // ============================================================
  // MAIN RENDER — MASTER-DETAIL SPLIT
  // ============================================================

  return (
    <div id="market-quotes-view" className="flex flex-col lg:flex-row gap-6 p-6 pb-12 min-h-0">

      {/* LEFT PANEL — MASTER (LIST) */}
      <div className={`flex flex-col gap-4 min-w-0 ${selectedSymbol ? 'lg:w-1/2' : 'w-full'} transition-all duration-300`}>

        {/* HEADER */}
        <div className="glass-card rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-amber-400" />
              S&P 500 Market Quotes
            </h2>
            <p className="text-xs text-[#8D9AAA] mt-0.5">
              {data?.count || 0} tickers · {data?.date || '—'} ·{' '}
              {data?.cached ? `cached ${data.cache_age_sec?.toFixed(0)}s` : 'fresh'}
            </p>
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            {status && (
              <span className={`text-xs px-2.5 py-1 rounded-lg font-bold flex items-center gap-1.5 ${
                status.is_open
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : 'bg-slate-500/20 text-slate-300 border border-slate-500/30'
              }`}>
                <span className={`w-2 h-2 rounded-full ${
                  status.is_open ? 'bg-emerald-400 animate-pulse' : 'bg-slate-400'
                }`} />
                {status.status}
              </span>
            )}
            <span className={`text-xs px-2.5 py-1 rounded-lg font-bold ${
              wsConnected
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
            }`}>
              {wsConnected ? '🟢 LIVE' : '🔴 OFFLINE'}
            </span>
            <button
              onClick={() => fetchAll(true)}
              disabled={isRefreshing}
              className="p-2 rounded-lg glass-panel hover:bg-white/5 text-[#8D9AAA] hover:text-white transition cursor-pointer disabled:opacity-50"
              title="Refresh"
            >
              <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>

        {/* STATS */}
        <div className="grid grid-cols-4 gap-3">
          <div className="glass-card rounded-xl p-4">
            <div className="text-[10px] text-[#8D9AAA] uppercase font-bold tracking-wider">Total</div>
            <div className="text-xl font-black text-white font-mono mt-1">{data?.count || 0}</div>
          </div>
          <div className="glass-card rounded-xl p-4">
            <div className="text-[10px] text-[#8D9AAA] uppercase font-bold tracking-wider">Up</div>
            <div className="text-xl font-black text-emerald-300 font-mono mt-1">{upCount}</div>
          </div>
          <div className="glass-card rounded-xl p-4">
            <div className="text-[10px] text-[#8D9AAA] uppercase font-bold tracking-wider">Down</div>
            <div className="text-xl font-black text-rose-300 font-mono mt-1">{downCount}</div>
          </div>
          <div className="glass-card rounded-xl p-4">
            <div className="text-[10px] text-[#8D9AAA] uppercase font-bold tracking-wider">Shown</div>
            <div className="text-xl font-black text-blue-300 font-mono mt-1">{filtered.length}</div>
          </div>
        </div>

        {/* SEARCH + FILTER */}
        <div className="glass-card rounded-2xl p-4 flex flex-col md:flex-row gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#5F6B78]" />
            <input
              type="text"
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(0); }}
              placeholder="Search ticker or company name..."
              className="w-full pl-10 pr-3 py-2 rounded-lg glass-panel text-sm text-white placeholder-[#5F6B78] focus:outline-none focus:border-amber-500 transition"
            />
          </div>
          <div className="flex items-center gap-1.5 glass-panel p-1 rounded-xl">
            {(['ALL', 'UP', 'DOWN'] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => { setFilter(mode); setPage(0); }}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold font-mono transition-all cursor-pointer ${
                  filter === mode
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                    : 'text-[#8D9AAA] hover:text-white'
                }`}
              >
                {mode}
              </button>
            ))}
          </div>
        </div>

        {/* ERROR */}
        {error && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm">
            Failed to load: {error}
          </div>
        )}

        {/* LIST */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between pb-4 border-b border-white/10 mb-4">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase">
              Quotes ({filtered.length}) — Page {page + 1}/{totalPages}
            </h3>
            <span className="text-[10px] text-[#5F6B78]">
              {selectedSymbol ? 'Select another ticker to analyze' : 'Select a ticker for Brain analysis'}
            </span>
          </div>

          <div className="space-y-3">
            {pageRecords.map((rec, index) => {
              const symbol = rec.ticker?.[0] || '?';
              const isSelected = selectedSymbol === symbol;
              const isUp = rec.deltaIndicator === 'up';

              return (
                <div
                  key={`${symbol}-${index}`}
                  onClick={() => selectSymbol(symbol)}
                  className={`p-5 rounded-xl border transition-all duration-200 cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-3 ${
                    isSelected
                      ? 'bg-blue-600/15 border-blue-500/40 shadow-lg shadow-blue-600/10'
                      : 'bg-transparent border-white/5 hover:bg-white/5 hover:border-white/10'
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0 flex-1">
                    <span className="font-black text-white font-mono text-sm tracking-wide w-16 flex-shrink-0">
                      {symbol}
                    </span>
                    <span className="text-xs text-[#8D9AAA] truncate">
                      {rec.ticker?.[1] || '—'}
                    </span>
                    <span className="text-[10px] font-black px-2 py-0.5 rounded border text-gray-400 bg-gray-500/20 border-gray-500/30 flex-shrink-0">
                      {rec.assetclass || 'STOCKS'}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-xs font-mono text-[#8D9AAA] flex-shrink-0">
                    <div className="flex items-center gap-1.5">
                      {isUp ? (
                        <ArrowUpRight className="w-3.5 h-3.5 text-emerald-400" />
                      ) : (
                        <ArrowDownRight className="w-3.5 h-3.5 text-rose-400" />
                      )}
                      <strong className="text-white">{rec.lastSale || '—'}</strong>
                    </div>
                    <div className={isUp ? 'text-emerald-400' : 'text-rose-400'}>
                      {rec.change || '—'} ({rec.pctChange || '—'})
                    </div>
                    <div className="hidden lg:block">
                      Vol: <span className="text-[#8D9AAA]">{rec.volume || '—'}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* PAGINATION */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between pt-4 mt-4 border-t border-white/10">
              <button
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                disabled={page === 0}
                className="p-2 rounded-lg glass-panel hover:bg-white/5 text-[#8D9AAA] hover:text-white disabled:opacity-30 cursor-pointer"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="text-xs text-[#8D9AAA] font-mono">
                {page * perPage + 1} – {Math.min((page + 1) * perPage, filtered.length)} of {filtered.length}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                disabled={page >= totalPages - 1}
                className="p-2 rounded-lg glass-panel hover:bg-white/5 text-[#8D9AAA] hover:text-white disabled:opacity-30 cursor-pointer"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>

        {/* FOOTER */}
        <div className="text-xs text-[#5F6B78] text-center">
          {filtered.length} quotes · Updated: {data?.timestamp ? new Date(data.timestamp).toLocaleString() : new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* RIGHT PANEL — DETAIL */}
      {selectedSymbol && (
        <div className="lg:w-1/2 flex flex-col gap-4 min-w-0">

          {/* DETAIL HEADER */}
          <div className="glass-card rounded-2xl p-6 flex items-center justify-between gap-4 sticky top-0 z-10 backdrop-blur-md">
            <div className="flex items-center gap-3 min-w-0">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div className="min-w-0">
                <div className="text-[10px] uppercase tracking-widest text-[#8D9AAA] font-bold">
                  Brain Analysis
                </div>
                <div className="text-xl font-black text-white tracking-wide truncate">
                  {selectedSymbol}
                </div>
              </div>
            </div>
            <button
              onClick={() => setSelectedSymbol(null)}
              className="p-2 rounded-lg glass-panel hover:bg-white/5 text-[#8D9AAA] hover:text-white transition cursor-pointer"
              title="Close detail"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* DETAIL BODY */}
          <div className="overflow-y-auto space-y-4 pr-1">
            {selectedLoading && (
              <div className="glass-card rounded-2xl py-16 text-center text-[#8D9AAA] text-xs">
                <Loader2 className="w-6 h-6 animate-spin mx-auto mb-3 text-amber-400" />
                Analyzing {selectedSymbol} with Brain...
                <div className="text-[10px] text-[#5F6B78] mt-1">
                  Fetching historical data + computing indicators + prediction + decision
                </div>
              </div>
            )}

            {!selectedLoading && selectedAnalysis?.error && (
              <div className="glass-card rounded-2xl py-12 text-center text-rose-400 text-sm">
                ❌ {selectedAnalysis.error}
              </div>
            )}

            {!selectedLoading && selectedAnalysis && !selectedAnalysis.error && (
              <>
                {selectedAnalysis.market_decision && (
                  <DecisionCard
                    decision={selectedAnalysis.market_decision}
                    symbol={selectedSymbol}
                  />
                )}

                <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                  {selectedAnalysis.prediction && (
                    <PredictionChart prediction={selectedAnalysis.prediction} />
                  )}
                  {selectedAnalysis.multi_timeframe && (
                    <TimeframeGrid
                      timeframes={selectedAnalysis.multi_timeframe.timeframes || {}}
                      consensus={selectedAnalysis.multi_timeframe.consensus}
                      overall={selectedAnalysis.multi_timeframe.overall}
                    />
                  )}
                </div>

                <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                  {selectedAnalysis.market_decision?.levels && (
                    <LevelsLadder
                      current={selectedAnalysis.market_decision.levels.current}
                      support={selectedAnalysis.market_decision.levels.support}
                      resistance={selectedAnalysis.market_decision.levels.resistance}
                      entry={selectedAnalysis.market_decision.levels.entry}
                      stop={selectedAnalysis.market_decision.levels.stop}
                      target={selectedAnalysis.market_decision.levels.target}
                    />
                  )}
                  <BrainStateCard
                    brain={selectedAnalysis.brain}
                    reflection={selectedAnalysis.reflection}
                    selfModel={selectedAnalysis.self_model}
                  />
                </div>

                <div className="text-[10px] text-[#5F6B78] text-center pt-2 border-t border-white/5 flex items-center justify-center gap-3">
                  <span>{selectedAnalysis.total_days} days of data</span>
                  <span>·</span>
                  <span className="flex items-center gap-1">
                    <Activity className="w-3 h-3" />
                    {selectedAnalysis.cached ? 'cached' : 'fresh'}
                  </span>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MarketQuotesView;
