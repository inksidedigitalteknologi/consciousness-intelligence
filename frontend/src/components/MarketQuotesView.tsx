// src/components/MarketQuotesView.tsx
// INKSIDE DIGITAL — Market Quotes with Comprehensive Brain Analysis

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  TrendingUp, Search, RefreshCw, Loader2,
  ChevronLeft, ChevronRight, ChevronDown, ChevronUp, Activity,
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

  const [expandedSymbol, setExpandedSymbol] = useState<string | null>(null);
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

  const toggleRow = (symbol: string) => {
    if (expandedSymbol === symbol) {
      setExpandedSymbol(null);
    } else {
      setExpandedSymbol(symbol);
      fetchAnalysis(symbol);
    }
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

  // ============================================================
  // RENDER HELPERS
  // ============================================================

  const getPriceColor = (indicator: string) =>
    indicator === 'up' ? 'text-emerald-400' : 'text-rose-400';

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
          <p className="text-lg">Memuat data S&P 500...</p>
        </div>
      </div>
    );
  }

  // ============================================================
  // MAIN RENDER
  // ============================================================

  return (
    <div id="market-quotes-view" className="space-y-6 pb-12 p-6">
      {/* HEADER */}
      <div className="glass-card rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-amber-400" />
            S&P 500 Market Quotes
          </h2>
          <p className="text-xs text-[#8D9AAA]">
            {data?.count || 0} tickers · {data?.date || '—'} ·{' '}
            {data?.cached ? `cached ${data.cache_age_sec?.toFixed(0)}s` : 'fresh'}
          </p>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          {status && (
            <span className={`text-xs px-2 py-1 rounded font-bold flex items-center gap-1.5 ${
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
          <span className={`text-xs px-2 py-0.5 rounded font-bold ${
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
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* STATS */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="glass-card rounded-xl p-4">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold">Total</div>
          <div className="text-xl font-black text-white font-mono mt-1">{data?.count || 0}</div>
        </div>
        <div className="glass-card rounded-xl p-4">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold">Up</div>
          <div className="text-xl font-black text-emerald-300 font-mono mt-1">{upCount}</div>
        </div>
        <div className="glass-card rounded-xl p-4">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold">Down</div>
          <div className="text-xl font-black text-rose-300 font-mono mt-1">{downCount}</div>
        </div>
        <div className="glass-card rounded-xl p-4">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold">Filter</div>
          <div className="text-sm font-black text-blue-300 font-mono mt-1">{filtered.length}</div>
        </div>
      </div>

      {/* FILTER + SEARCH */}
      <div className="glass-card rounded-2xl p-4 flex flex-col md:flex-row gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#5F6B78]" />
          <input
            type="text"
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(0); }}
            placeholder="Cari ticker atau nama perusahaan..."
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
          Gagal memuat: {error}
        </div>
      )}

      {/* TABLE */}
      <div className="glass-card rounded-2xl p-5">
        <div className="flex items-center justify-between pb-3 border-b border-white/10 mb-3">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase">
            Quotes ({filtered.length}) — Hal. {page + 1}/{totalPages}
          </h3>
          <span className="text-[10px] text-[#5F6B78]">Klik ticker untuk analisis Brain</span>
        </div>

        <div className="space-y-2">
          {pageRecords.map((rec, index) => {
            const symbol = rec.ticker?.[0] || '?';
            const isExpanded = expandedSymbol === symbol;
            const analysis = analysisCache[symbol];
            const isLoading = analysisLoading[symbol];

            return (
              <div key={`${symbol}-${index}`} className="rounded-xl border border-white/5 overflow-hidden transition-all duration-300">
                {/* ROW */}
                <div
                  onClick={() => toggleRow(symbol)}
                  className="p-4 glass-panel hover:bg-white/5 transition cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-3"
                >
                  <div className="flex items-center gap-3 min-w-0 flex-1">
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-amber-400 flex-shrink-0 transition-transform" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-[#5F6B78] flex-shrink-0 transition-transform" />
                    )}
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
                    <div>
                      <strong className="text-white">{rec.lastSale || '—'}</strong>
                    </div>
                    <div className={getPriceColor(rec.deltaIndicator)}>
                      {rec.change || '—'} ({rec.pctChange || '—'})
                    </div>
                    <div className="hidden lg:block">
                      Vol: <span className="text-[#8D9AAA]">{rec.volume || '—'}</span>
                    </div>
                  </div>
                </div>

                {/* EXPANDED — FULL BRAIN ANALYSIS */}
                {isExpanded && (
                  <div className="p-4 bg-[#0B0F14]/60 border-t border-white/5 animate-fade-in">
                    {isLoading && (
                      <div className="py-12 text-center text-[#8D9AAA] text-xs">
                        <Loader2 className="w-6 h-6 animate-spin mx-auto mb-3 text-amber-400" />
                        Menganalisis {symbol} dengan Brain...
                        <div className="text-[10px] text-[#5F6B78] mt-1">
                          Fetch historical + hitung indikator + prediksi + decision
                        </div>
                      </div>
                    )}

                    {!isLoading && analysis?.error && (
                      <div className="py-6 text-center text-rose-400 text-xs">
                        ❌ {analysis.error}
                      </div>
                    )}

                    {!isLoading && analysis && !analysis.error && (
                      <div className="space-y-4">
                        {/* DECISION — full width */}
                        {analysis.market_decision && (
                          <DecisionCard
                            decision={analysis.market_decision}
                            symbol={symbol}
                          />
                        )}

                        {/* PREDICTION + TIMEFRAME — grid 2 */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                          {analysis.prediction && (
                            <PredictionChart prediction={analysis.prediction} />
                          )}
                          {analysis.multi_timeframe && (
                            <TimeframeGrid
                              timeframes={analysis.multi_timeframe.timeframes || {}}
                              consensus={analysis.multi_timeframe.consensus}
                              overall={analysis.multi_timeframe.overall}
                            />
                          )}
                        </div>

                        {/* LEVELS + BRAIN STATE — grid 2 */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                          {analysis.market_decision?.levels && (
                            <LevelsLadder
                              current={analysis.market_decision.levels.current}
                              support={analysis.market_decision.levels.support}
                              resistance={analysis.market_decision.levels.resistance}
                              entry={analysis.market_decision.levels.entry}
                              stop={analysis.market_decision.levels.stop}
                              target={analysis.market_decision.levels.target}
                            />
                          )}
                          <BrainStateCard
                            brain={analysis.brain}
                            reflection={analysis.reflection}
                            selfModel={analysis.self_model}
                          />
                        </div>

                        {/* FOOTER */}
                        <div className="text-[10px] text-[#5F6B78] text-center pt-2 border-t border-white/5 flex items-center justify-center gap-3">
                          <span>{analysis.total_days} hari data</span>
                          <span>·</span>
                          <span className="flex items-center gap-1">
                            <Activity className="w-3 h-3" />
                            {analysis.cached ? 'cached' : 'fresh'}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>
                )}
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
              {page * perPage + 1} – {Math.min((page + 1) * perPage, filtered.length)} dari {filtered.length}
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
  );
};

export default MarketQuotesView;
