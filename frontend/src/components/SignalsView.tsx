// src/components/SignalsView.tsx
// INKSIDE DIGITAL — Dividend Hunter (replaces SignalsView)
// Self-fetching: fetches dividend data if props empty

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  DollarSign, TrendingUp, Shield, AlertTriangle,
  Search, RefreshCw, Loader2, Download, ChevronDown, ChevronRight,
  Award, Crown, Medal, Clock, ArrowUpDown, Calendar,
  Activity, Check, X,
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface DividendRecord {
  symbol?: string;
  name?: string;
  sector?: string;
  dividend?: number;
  annual_dividend?: number;
  ex_date?: string;
  pay_date?: string;
  record_date?: string;
  announcement_date?: string;
  frequency?: string;
  source?: string;
  type?: string;
  trap_score?: number;
  category?: string;
  recommendation?: string;
  current_yield?: number;
  payout_ratio?: number;
  streak_years?: number;
  cut_count?: number;
  cagr_5y?: number;
  cagr_10y?: number;
  is_king?: boolean;
  is_aristocrat?: boolean;
  is_champion?: boolean;
  red_flags?: Array<{ code: string; severity?: string; message: string }>;
  green_flags?: Array<{ code: string; message: string }>;
  free_cash_flow?: number;
  debt_to_equity?: number;
  history_years?: number;
  [key: string]: any;
}

interface SignalsViewProps {
  signals?: DividendRecord[];
  apiKey?: string;
}

type FilterMode = 'ALL' | 'SAFE' | 'CAUTION' | 'RISKY' | 'TRAP' | 'KING' | 'ARISTOCRAT';
type SortMode = 'TRAP' | 'YIELD' | 'STREAK' | 'SYMBOL';

// ============================================================
// HELPERS
// ============================================================

const safeNum = (n: any, fallback = 0) => {
  const v = Number(n);
  return isNaN(v) ? fallback : v;
};

const getTrapColor = (score: number) => {
  if (score >= 70) return 'text-rose-400 bg-rose-500/20 border-rose-500/40';
  if (score >= 50) return 'text-orange-400 bg-orange-500/20 border-orange-500/40';
  if (score >= 30) return 'text-amber-400 bg-amber-500/20 border-amber-500/40';
  return 'text-emerald-400 bg-emerald-500/20 border-emerald-500/40';
};

const getTrapBarColor = (score: number) => {
  if (score >= 70) return 'bg-rose-500';
  if (score >= 50) return 'bg-orange-500';
  if (score >= 30) return 'bg-amber-500';
  return 'bg-emerald-500';
};

const getCategoryIcon = (cat?: string) => {
  const c = (cat || '').toUpperCase();
  if (c === 'TRAP') return '🚨';
  if (c === 'RISKY') return '⚠️';
  if (c === 'CAUTION') return '🟡';
  if (c === 'SAFE') return '✅';
  return '❓';
};

const getCategoryFromScore = (score: number): string => {
  if (score >= 70) return 'TRAP';
  if (score >= 50) return 'RISKY';
  if (score >= 30) return 'CAUTION';
  return 'SAFE';
};

const getBadge = (d: DividendRecord) => {
  if (d.is_king) return {
    label: 'KING',
    icon: <Crown className="w-3 h-3" />,
    cls: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
  };
  if (d.is_aristocrat) return {
    label: 'ARISTOCRAT',
    icon: <Award className="w-3 h-3" />,
    cls: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
  };
  if (d.is_champion) return {
    label: 'CHAMPION',
    icon: <Medal className="w-3 h-3" />,
    cls: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
  };
  return null;
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const SignalsView: React.FC<SignalsViewProps> = ({ signals = [], apiKey: propApiKey }) => {
  const apiKey = 'iks_612d40ce554b1670525355c85567f823';  // hardcoded to prevent 401

  const [filter, setFilter] = useState<FilterMode>('ALL');
  const [sortBy, setSortBy] = useState<SortMode>('TRAP');
  const [search, setSearch] = useState('');
  const [expandedSymbol, setExpandedSymbol] = useState<string | null>(null);
  const [trapCache, setTrapCache] = useState<Record<string, DividendRecord>>({});
  const [trapLoading, setTrapLoading] = useState<Record<string, boolean>>({});
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [page, setPage] = useState(0);
  const perPage = 10;

  const [selfFetched, setSelfFetched] = useState<DividendRecord[]>([]);
  const [selfLoading, setSelfLoading] = useState(false);
  const [selfError, setSelfError] = useState<string | null>(null);

  // ============================================================
  // SELF-FETCH
  // ============================================================

  const fetchDividends = useCallback(async (showRefresh = false) => {
    if (showRefresh) setIsRefreshing(true);
    setSelfLoading(true);
    setSelfError(null);
    try {
      const res = await fetch('/api/dividend/top?limit=50', {
        headers: { 'X-API-Key': apiKey },
      });
      if (res.ok) {
        const data = await res.json();
        const stocks = data.data || [];
        setSelfFetched(stocks);

        // Auto-fetch trap analysis untuk 10 saham pertama (paralel)
        const firstPage = stocks.slice(0, perPage);
        const results = await Promise.all(
          firstPage.map(async (s: DividendRecord) => {
            const sym = s.symbol;
            if (!sym) return null;
            try {
              const r = await fetch(`/api/dividend/trap-analysis/${sym}`, {
                headers: { 'X-API-Key': apiKey },
              });
              if (r.ok) {
                const d = await r.json();
                return { symbol: sym, data: d.data || {} };
              }
            } catch (e) {
              console.warn(`Trap fetch failed for ${sym}`);
            }
            return null;
          })
        );

        const newCache: Record<string, DividendRecord> = {};
        results.forEach((r) => {
          if (r && r.symbol) newCache[r.symbol] = r.data;
        });
        setTrapCache((prev) => ({ ...prev, ...newCache }));
      } else {
        setSelfError(`HTTP ${res.status}`);
      }
    } catch (err) {
      setSelfError(err instanceof Error ? err.message : 'Fetch failed');
    } finally {
      setSelfLoading(false);
      if (showRefresh) setTimeout(() => setIsRefreshing(false), 300);
    }
  }, [apiKey]);

  useEffect(() => {
    if (signals && signals.length > 0) return;
    if (selfFetched.length > 0) return;
    fetchDividends();
  }, [signals, selfFetched.length, fetchDividends]);

  // ============================================================
  // FETCH TRAP
  // ============================================================

  const fetchTrap = useCallback(async (symbol: string) => {
    if (trapCache[symbol] || trapLoading[symbol]) return;
    setTrapLoading(prev => ({ ...prev, [symbol]: true }));
    try {
      // Fetch BOTH: trap-analysis + opportunity
      const [trapRes, oppRes] = await Promise.all([
        fetch(`/api/dividend/trap-analysis/${symbol}`, {
          headers: { 'X-API-Key': apiKey },
        }),
        fetch(`/api/dividend/opportunity/${symbol}`, {
          headers: { 'X-API-Key': apiKey },
        }).catch(() => null),
      ]);

      let merged: DividendRecord = {};

      if (trapRes.ok) {
        const trapData = await trapRes.json();
        merged = { ...merged, ...(trapData.data || {}) };
      }

      if (oppRes && oppRes.ok) {
        const oppData = await oppRes.json();
        merged = { ...merged, ...(oppData.data || {}) };
      }

      setTrapCache(prev => ({ ...prev, [symbol]: merged }));
    } catch (err) {
      console.error(`Trap fetch failed for ${symbol}:`, err);
    } finally {
      setTrapLoading(prev => ({ ...prev, [symbol]: false }));
    }
  }, [apiKey, trapCache, trapLoading]);

  const toggleRow = (symbol: string) => {
    if (expandedSymbol === symbol) {
      setExpandedSymbol(null);
    } else {
      setExpandedSymbol(symbol);
      fetchTrap(symbol);
    }
  };

  // ============================================================
  // DATA
  // ============================================================

  const safeSignals = useMemo(() => {
    // Always use self-fetched dividend data (not props)
    return selfFetched;
  }, [selfFetched]);

  const merged = useMemo(() => {
    return safeSignals.map(s => {
      const symbol = (s.symbol || '').toUpperCase();
      const trap = trapCache[symbol];
      return trap ? { ...s, ...trap } : s;
    });
  }, [safeSignals, trapCache]);

  const filtered = useMemo(() => {
    let list = [...merged];

    if (filter !== 'ALL') {
      if (['SAFE', 'CAUTION', 'RISKY', 'TRAP'].includes(filter)) {
        list = list.filter(d => {
          const cat = (d.category || getCategoryFromScore(safeNum(d.trap_score, 0))).toUpperCase();
          return cat === filter;
        });
      } else if (filter === 'KING') {
        list = list.filter(d => d.is_king);
      } else if (filter === 'ARISTOCRAT') {
        list = list.filter(d => d.is_aristocrat);
      }
    }

    if (search.trim()) {
      const q = search.toLowerCase();
      list = list.filter(d =>
        (d.symbol || '').toLowerCase().includes(q) ||
        (d.name || '').toLowerCase().includes(q)
      );
    }

    list.sort((a, b) => {
      if (sortBy === 'TRAP') return safeNum(a.trap_score, 50) - safeNum(b.trap_score, 50);
      if (sortBy === 'YIELD') return safeNum(b.current_yield || b.annual_dividend) - safeNum(a.current_yield || a.annual_dividend);
      if (sortBy === 'STREAK') return safeNum(b.streak_years) - safeNum(a.streak_years);
      if (sortBy === 'SYMBOL') return (a.symbol || '').localeCompare(b.symbol || '');
      return 0;
    });

    return list;
  }, [merged, filter, search, sortBy]);

  // Pagination
  const totalPages = Math.ceil(filtered.length / perPage);
  const paginatedItems = useMemo(() => {
    return filtered.slice(page * perPage, (page + 1) * perPage);
  }, [filtered, page, perPage]);

  // Reset page saat filter/search berubah
  useEffect(() => {
    setPage(0);
  }, [filter, search, sortBy]);

  // Fetch trap untuk halaman aktif
  const fetchTrapForPage = useCallback(async (items: DividendRecord[]) => {
    const toFetch = items.filter((d) => {
      const sym = d.symbol;
      return sym && !trapCache[sym] && !trapLoading[sym];
    });
    if (toFetch.length === 0) return;

    const results = await Promise.all(
      toFetch.map(async (s) => {
        const sym = s.symbol;
        if (!sym) return null;
        try {
          const r = await fetch(`/api/dividend/trap-analysis/${sym}`, {
            headers: { 'X-API-Key': apiKey },
          });
          if (r.ok) {
            const d = await r.json();
            return { symbol: sym, data: d.data || {} };
          }
        } catch (e) {}
        return null;
      })
    );

    const newCache: Record<string, DividendRecord> = {};
    results.forEach((r) => {
      if (r && r.symbol) newCache[r.symbol] = r.data;
    });
    setTrapCache((prev) => ({ ...prev, ...newCache }));
  }, [apiKey, trapCache, trapLoading]);

  useEffect(() => {
    if (paginatedItems.length > 0) {
      fetchTrapForPage(paginatedItems);
    }
  }, [paginatedItems, fetchTrapForPage]);

  const stats = useMemo(() => {
    const total = merged.length;
    const safe = merged.filter(d => safeNum(d.trap_score, 100) < 30).length;
    const trap = merged.filter(d => safeNum(d.trap_score, 0) >= 50).length;
    const kings = merged.filter(d => d.is_king).length;
    const yields = merged.map(d => safeNum(d.current_yield)).filter(y => y > 0);
    const avgYield = yields.length > 0 ? yields.reduce((a, b) => a + b, 0) / yields.length : 0;
    return { total, safe, trap, kings, avgYield };
  }, [merged]);

  const handleExport = useCallback(() => {
    const headers = ['Symbol', 'Name', 'Sector', 'Trap Score', 'Category', 'Yield', 'Payout', 'Streak', 'Cuts', 'CAGR 5Y', 'CAGR 10Y', 'Badge'];
    const rows = filtered.map(d => [
      d.symbol || '', d.name || '', d.sector || '',
      safeNum(d.trap_score, ''), d.category || '',
      safeNum(d.current_yield, ''), safeNum(d.payout_ratio, ''),
      safeNum(d.streak_years, ''), safeNum(d.cut_count, ''),
      safeNum(d.cagr_5y, ''), safeNum(d.cagr_10y, ''),
      d.is_king ? 'KING' : d.is_aristocrat ? 'ARISTOCRAT' : d.is_champion ? 'CHAMPION' : '',
    ]);
    const csv = [headers, ...rows].map(r => r.map(v => `"${v}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dividend_hunter_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }, [filtered]);

  // ============================================================
  // LOADING
  // ============================================================

  if ((selfLoading || isRefreshing) && safeSignals.length === 0) {
    return (
      <div className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <DollarSign className="w-5 h-5 text-emerald-400" />
          <h2 className="text-lg font-bold text-white">Dividend Hunter</h2>
        </div>
        <div className="glass-card rounded-2xl py-16 text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-3 text-emerald-400" />
          <p className="text-[#8D9AAA]">Loading dividend data from Nasdaq...</p>
        </div>
      </div>
    );
  }

  if (safeSignals.length === 0) {
    return (
      <div className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <DollarSign className="w-5 h-5 text-emerald-400" />
          <h2 className="text-lg font-bold text-white">Dividend Hunter</h2>
        </div>
        <div className="text-center text-gray-400 py-12 glass-card rounded-xl">
          <DollarSign className="w-12 h-12 text-[#5F6B78] mx-auto mb-4" />
          <p className="text-lg">No dividend data available</p>
          <p className="text-sm mt-1">
            {selfError ? `Error: ${selfError}` : 'Waiting for data from Nasdaq API...'}
          </p>
          <button
            onClick={() => fetchDividends(true)}
            className="mt-6 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold transition cursor-pointer flex items-center gap-2 mx-auto"
          >
            <RefreshCw className="w-4 h-4" />
            Retry
          </button>
        </div>
      </div>
    );
  }

  // ============================================================
  // MAIN RENDER
  // ============================================================

  return (
    <div id="signals-view" className="space-y-6 pb-12 p-6">

      <div className="glass-card rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            Dividend Hunter
          </h2>
          <p className="text-xs text-[#8D9AAA] mt-0.5">
            {stats.total} stocks · Avg yield {stats.avgYield.toFixed(2)}% · {stats.safe} safe · {stats.trap} trap alert
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => fetchDividends(true)}
            disabled={isRefreshing}
            className="p-2 rounded-lg glass-panel hover:bg-white/5 text-[#8D9AAA] hover:text-white transition cursor-pointer disabled:opacity-50"
            title="Refresh"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          </button>
          <button
            onClick={handleExport}
            className="px-3 py-2 rounded-lg glass-panel hover:bg-white/5 text-[#8D9AAA] hover:text-white text-xs font-bold transition cursor-pointer flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            Export
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="glass-card rounded-xl p-4">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold tracking-wider">Total</div>
          <div className="text-xl font-black text-white font-mono mt-1">{stats.total}</div>
        </div>
        <div className="glass-card rounded-xl p-4">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold tracking-wider">Safe</div>
          <div className="text-xl font-black text-emerald-300 font-mono mt-1">{stats.safe}</div>
        </div>
        <div className="glass-card rounded-xl p-4">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold tracking-wider">Trap Alert</div>
          <div className="text-xl font-black text-rose-300 font-mono mt-1">{stats.trap}</div>
        </div>
        <div className="glass-card rounded-xl p-4">
          <div className="text-[10px] text-[#8D9AAA] uppercase font-bold tracking-wider">Kings</div>
          <div className="text-xl font-black text-amber-300 font-mono mt-1">{stats.kings}</div>
        </div>
      </div>

      <div className="glass-card rounded-2xl p-4 flex flex-col md:flex-row gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#5F6B78]" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search symbol or company..."
            className="w-full pl-10 pr-3 py-2 rounded-lg glass-panel text-sm text-white placeholder-[#5F6B78] focus:outline-none focus:border-emerald-500 transition"
          />
        </div>
        <div className="flex items-center gap-1.5 glass-panel p-1 rounded-xl flex-wrap">
          {(['ALL', 'SAFE', 'CAUTION', 'RISKY', 'TRAP', 'KING', 'ARISTOCRAT'] as const).map((mode) => (
            <button
              key={mode}
              onClick={() => setFilter(mode)}
              className={`px-2.5 py-1.5 rounded-lg text-[10px] font-bold font-mono transition-all cursor-pointer ${
                filter === mode
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'text-[#8D9AAA] hover:text-white'
              }`}
            >
              {mode}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-1.5 glass-panel p-1 rounded-xl">
          <ArrowUpDown className="w-3.5 h-3.5 text-[#5F6B78] ml-1" />
          {([
            { id: 'TRAP', label: 'TRAP' },
            { id: 'YIELD', label: 'YIELD' },
            { id: 'STREAK', label: 'STREAK' },
            { id: 'SYMBOL', label: 'A-Z' },
          ] as const).map((s) => (
            <button
              key={s.id}
              onClick={() => setSortBy(s.id)}
              className={`px-2.5 py-1.5 rounded-lg text-[10px] font-bold font-mono transition-all cursor-pointer ${
                sortBy === s.id ? 'bg-amber-600 text-white' : 'text-[#8D9AAA] hover:text-white'
              }`}
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 && (
        <div className="glass-card rounded-2xl py-12 text-center">
          <p className="text-[#8D9AAA]">No dividend stocks match the current filter</p>
        </div>
      )}

      {filtered.length > 0 && (
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between pb-4 border-b border-white/10 mb-4">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase">
              Dividend Stocks ({filtered.length})
            </h3>
            <span className="text-[10px] text-[#5F6B78]">Click to expand trap analysis</span>
          </div>

          <div className="space-y-3">
            {paginatedItems.map((d, index) => {
              const symbol = d.symbol || '?';
              const isExpanded = expandedSymbol === symbol;
              const trap = trapCache[symbol];
              const isLoading = trapLoading[symbol];
              const trapScore = safeNum(trap?.trap_score, safeNum(d.trap_score, 0));
              const category = trap?.category || d.category || getCategoryFromScore(trapScore);
              const badge = getBadge({ ...d, ...trap });

              return (
                <div key={`${symbol}-${index}`} className="rounded-xl border border-white/5 overflow-hidden transition-all duration-200">
                  <div
                    onClick={() => toggleRow(symbol)}
                    className="p-5 glass-panel hover:bg-white/5 transition cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-3"
                  >
                    <div className="flex items-center gap-3 min-w-0 flex-1">
                      {isExpanded ? (
                        <ChevronDown className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                      ) : (
                        <ChevronRight className="w-4 h-4 text-[#5F6B78] flex-shrink-0" />
                      )}
                      <span className="font-black text-white font-mono text-sm tracking-wide w-16 flex-shrink-0">
                        {symbol}
                      </span>
                      <span className="text-xs text-[#8D9AAA] truncate hidden md:block">{d.name || '—'}</span>
                      {badge && (
                        <span className={`text-[9px] font-black px-1.5 py-0.5 rounded border flex items-center gap-1 flex-shrink-0 ${badge.cls}`}>
                          {badge.icon}
                          {badge.label}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-4 text-xs font-mono flex-shrink-0">
                      <div className="text-emerald-400 font-bold">
                        {safeNum(trap?.current_yield || d.current_yield, 0).toFixed(2)}%
                      </div>
                      <div className="text-[#8D9AAA] hidden lg:block">
                        Div: <span className="text-white">${safeNum(d.dividend, 0).toFixed(4)}</span>
                      </div>
                      {safeNum(trap?.streak_years || d.streak_years) > 0 && (
                        <div className="text-[#8D9AAA] hidden lg:flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          <span className="text-white">{safeNum(trap?.streak_years || d.streak_years)}y</span>
                        </div>
                      )}
                      <div className={`px-2 py-1 rounded-lg border font-bold flex items-center gap-1 ${getTrapColor(trapScore)}`}>
                        {getCategoryIcon(category)}
                        {trapScore}
                      </div>
                    </div>
                  </div>

                  {isExpanded && (
                    <div className="p-5 bg-[#0B0F14]/60 border-t border-white/5 animate-fade-in space-y-4">
                      {isLoading && !trap && (
                        <div className="text-center py-8 text-[#8D9AAA] text-xs">
                          <Loader2 className="w-5 h-5 animate-spin mx-auto mb-2 text-emerald-400" />
                          Loading trap analysis for {symbol}...
                        </div>
                      )}
                      {!isLoading && !trap && (
                        <div className="text-center py-6 text-amber-400 text-xs">
                          ⚠️ Trap analysis not available for {symbol}
                        </div>
                      )}
                      {trap && (
                        <>
                          {/* ============================================================ */}
                          {/* DIVIDEND OPPORTUNITY — TIMING + BRAIN + STRATEGY */}
                          {/* ============================================================ */}
                          {(trap.ex_date || trap.strategy || trap.brain_decision) && (
                            <div className="glass-card rounded-xl p-5 border-l-4 border-l-emerald-500">
                              <div className="flex items-center gap-2 mb-4">
                                <Calendar className="w-4 h-4 text-emerald-400" />
                                <span className="text-xs font-bold text-emerald-300 uppercase tracking-wider">
                                  Dividend Opportunity
                                </span>
                              </div>

                              {/* Timing Grid */}
                              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
                                <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                  <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">Ex-Date</div>
                                  <div className="text-sm font-mono font-bold text-white mt-1">
                                    {trap.ex_date || '—'}
                                  </div>
                                  {trap.days_to_ex != null && (
                                    <div className={`text-[10px] mt-0.5 ${
                                      trap.days_to_ex <= 1 ? 'text-rose-400 font-bold' :
                                      trap.days_to_ex <= 7 ? 'text-amber-400' : 'text-[#8D9AAA]'
                                    }`}>
                                      {trap.days_to_ex > 0
                                        ? `${trap.days_to_ex} days`
                                        : trap.days_to_ex === 0
                                        ? 'TODAY'
                                        : `${-trap.days_to_ex} days ago`}
                                    </div>
                                  )}
                                </div>
                                <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                  <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">Pay-Date</div>
                                  <div className="text-sm font-mono font-bold text-white mt-1">
                                    {trap.pay_date || '—'}
                                  </div>
                                  {trap.days_to_pay != null && trap.days_to_pay > 0 && (
                                    <div className="text-[10px] text-[#8D9AAA] mt-0.5">
                                      in {trap.days_to_pay} days
                                    </div>
                                  )}
                                </div>
                                <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                  <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">Amount</div>
                                  <div className="text-sm font-mono font-bold text-emerald-300 mt-1">
                                    ${safeNum(trap.dividend_amount).toFixed(4)}
                                  </div>
                                </div>
                                <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                  <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">Frequency</div>
                                  <div className="text-sm font-mono font-bold text-white mt-1">
                                    {trap.frequency || '—'}
                                  </div>
                                </div>
                              </div>

                              {/* Brain Analysis */}
                              {trap.brain_decision && (
                                <div className="mb-4 p-4 rounded-lg bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/20">
                                  <div className="flex items-center justify-between mb-2">
                                    <div className="flex items-center gap-2">
                                      <span className="text-purple-400 text-sm">🧠</span>
                                      <span className="text-xs font-bold text-white uppercase tracking-wider">
                                        Brain Analysis
                                      </span>
                                    </div>
                                    <div className={`text-sm font-black ${
                                      trap.brain_decision?.includes('BUY') ? 'text-emerald-300' :
                                      trap.brain_decision?.includes('AVOID') ? 'text-rose-300' :
                                      'text-amber-300'
                                    }`}>
                                      {trap.brain_decision}
                                      {trap.brain_confidence != null && (
                                        <span className="text-[10px] text-[#8D9AAA] ml-1">
                                          ({safeNum(trap.brain_confidence).toFixed(0)}%)
                                        </span>
                                      )}
                                    </div>
                                  </div>
                                  {trap.brain_reasoning && trap.brain_reasoning.length > 0 && (
                                    <ul className="space-y-1 mt-2">
                                      {trap.brain_reasoning.map((r: string, i: number) => (
                                        <li key={i} className="text-[11px] text-[#E8EDF2] leading-snug flex items-start gap-1.5">
                                          <span className="text-purple-400 mt-0.5">•</span>
                                          <span>{r}</span>
                                        </li>
                                      ))}
                                    </ul>
                                  )}
                                </div>
                              )}

                              {/* Strategy */}
                              {trap.strategy && (
                                <div className={`mb-4 p-4 rounded-lg border ${
                                  trap.strategy === 'BUY_BEFORE_EX' ? 'bg-emerald-500/10 border-emerald-500/30' :
                                  trap.strategy === 'BUY_NOW' ? 'bg-blue-500/10 border-blue-500/30' :
                                  trap.strategy === 'SKIP' ? 'bg-rose-500/10 border-rose-500/30' :
                                  'bg-amber-500/10 border-amber-500/30'
                                }`}>
                                  <div className="flex items-center justify-between mb-1">
                                    <span className="text-[10px] uppercase tracking-wider text-[#8D9AAA] font-bold">
                                      Strategy
                                    </span>
                                    <span className={`text-sm font-black ${
                                      trap.strategy === 'BUY_BEFORE_EX' ? 'text-emerald-300' :
                                      trap.strategy === 'BUY_NOW' ? 'text-blue-300' :
                                      trap.strategy === 'SKIP' ? 'text-rose-300' :
                                      'text-amber-300'
                                    }`}>
                                      {trap.strategy}
                                    </span>
                                  </div>
                                  <div className="text-[11px] text-[#E8EDF2]">
                                    {trap.strategy_reason}
                                  </div>
                                </div>
                              )}

                              {/* Capture Calculator */}
                              {safeNum(trap.dividend_amount) > 0 && (
                                <div className="p-4 rounded-lg bg-black/30 border border-white/5">
                                  <div className="text-[10px] uppercase tracking-wider text-[#8D9AAA] font-bold mb-2">
                                    💹 Capture Calculator
                                  </div>
                                  <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
                                    <div className="flex justify-between">
                                      <span className="text-[#8D9AAA]">Dividend:</span>
                                      <span className="text-emerald-300">+${safeNum(trap.dividend_amount).toFixed(4)}</span>
                                    </div>
                                    <div className="flex justify-between">
                                      <span className="text-[#8D9AAA]">Tax (15%):</span>
                                      <span className="text-rose-300">-${(safeNum(trap.dividend_amount) * 0.15).toFixed(4)}</span>
                                    </div>
                                    <div className="flex justify-between">
                                      <span className="text-[#8D9AAA]">Expected drop:</span>
                                      <span className="text-rose-300">-${safeNum(trap.expected_drop).toFixed(4)}</span>
                                    </div>
                                    <div className="flex justify-between border-t border-white/10 pt-1 mt-1">
                                      <span className="text-[#8D9AAA]">Net:</span>
                                      <span className={`font-bold ${
                                        safeNum(trap.net_profit_pct) >= 0 ? 'text-emerald-300' : 'text-rose-300'
                                      }`}>
                                        {safeNum(trap.net_profit_pct).toFixed(3)}%
                                      </span>
                                    </div>
                                  </div>
                                  <div className={`text-[10px] text-center mt-2 pt-2 border-t border-white/10 font-bold uppercase tracking-wider ${
                                    trap.capture_verdict === 'WORTH_IT' ? 'text-emerald-400' :
                                    trap.capture_verdict === 'NOT_WORTH' ? 'text-rose-400' :
                                    'text-amber-400'
                                  }`}>
                                    Verdict: {trap.capture_verdict || 'UNKNOWN'}
                                  </div>
                                </div>
                              )}
                            </div>
                          )}

                          <div className="glass-card rounded-xl p-5">
                            <div className="flex items-center justify-between mb-3">
                              <div>
                                <div className="text-[10px] uppercase tracking-widest text-[#8D9AAA] font-bold">Trap Analysis</div>
                                <div className="text-sm font-bold text-white mt-0.5">{trap.name || d.name}</div>
                              </div>
                              <div className="text-right">
                                <div className="text-[10px] uppercase tracking-widest text-[#8D9AAA] font-bold">Category</div>
                                <div className={`text-lg font-black ${getTrapColor(trapScore).split(' ')[0]}`}>
                                  {getCategoryIcon(category)} {category}
                                </div>
                              </div>
                            </div>
                            <div className="mb-4">
                              <div className="flex justify-between text-[10px] text-[#8D9AAA] uppercase font-bold mb-1">
                                <span>Trap Score</span>
                                <span>{trapScore}/100</span>
                              </div>
                              <div className="w-full h-2 rounded-full bg-black/40 overflow-hidden">
                                <div
                                  className={`h-full rounded-full transition-all duration-1000 ${getTrapBarColor(trapScore)}`}
                                  style={{ width: `${trapScore}%` }}
                                />
                              </div>
                            </div>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                              <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">Yield</div>
                                <div className="text-sm font-mono font-bold text-emerald-300 mt-1">
                                  {safeNum(trap.current_yield).toFixed(2)}%
                                </div>
                              </div>
                              <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">Payout</div>
                                <div className={`text-sm font-mono font-bold mt-1 ${
                                  safeNum(trap.payout_ratio) > 80 ? 'text-rose-300' :
                                  safeNum(trap.payout_ratio) > 60 ? 'text-amber-300' : 'text-emerald-300'
                                }`}>
                                  {safeNum(trap.payout_ratio).toFixed(1)}%
                                </div>
                              </div>
                              <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">Streak</div>
                                <div className="text-sm font-mono font-bold text-white mt-1">
                                  {safeNum(trap.streak_years)} years
                                </div>
                              </div>
                              <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">Cuts</div>
                                <div className={`text-sm font-mono font-bold mt-1 ${
                                  safeNum(trap.cut_count) > 0 ? 'text-rose-300' : 'text-emerald-300'
                                }`}>
                                  {safeNum(trap.cut_count)}x
                                </div>
                              </div>
                              <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">CAGR 5Y</div>
                                <div className={`text-sm font-mono font-bold mt-1 ${
                                  safeNum(trap.cagr_5y) >= 0 ? 'text-emerald-300' : 'text-rose-300'
                                }`}>
                                  {safeNum(trap.cagr_5y).toFixed(2)}%
                                </div>
                              </div>
                              <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">CAGR 10Y</div>
                                <div className={`text-sm font-mono font-bold mt-1 ${
                                  safeNum(trap.cagr_10y) >= 0 ? 'text-emerald-300' : 'text-rose-300'
                                }`}>
                                  {safeNum(trap.cagr_10y).toFixed(2)}%
                                </div>
                              </div>
                              <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">Debt/Eq</div>
                                <div className={`text-sm font-mono font-bold mt-1 ${
                                  safeNum(trap.debt_to_equity) > 100 ? 'text-rose-300' :
                                  safeNum(trap.debt_to_equity) > 50 ? 'text-amber-300' : 'text-emerald-300'
                                }`}>
                                  {safeNum(trap.debt_to_equity).toFixed(1)}%
                                </div>
                              </div>
                              <div className="p-3 rounded-lg bg-black/30 border border-white/5">
                                <div className="text-[9px] text-[#8D9AAA] uppercase font-bold">FCF</div>
                                <div className={`text-sm font-mono font-bold mt-1 ${
                                  safeNum(trap.free_cash_flow) >= 0 ? 'text-emerald-300' : 'text-rose-300'
                                }`}>
                                  ${safeNum(trap.free_cash_flow).toFixed(2)}B
                                </div>
                              </div>
                            </div>
                          </div>

                          {trap.red_flags && trap.red_flags.length > 0 && (
                            <div className="glass-card rounded-xl p-4">
                              <div className="flex items-center gap-2 mb-3">
                                <AlertTriangle className="w-4 h-4 text-rose-400" />
                                <span className="text-xs font-bold text-rose-300 uppercase tracking-wider">
                                  Red Flags ({trap.red_flags.length})
                                </span>
                              </div>
                              <div className="space-y-2">
                                {trap.red_flags.map((f, i) => (
                                  <div key={i} className="flex items-start gap-2 p-2 rounded-lg bg-rose-500/5 border border-rose-500/20">
                                    <X className="w-3.5 h-3.5 text-rose-400 flex-shrink-0 mt-0.5" />
                                    <div className="text-xs text-[#E8EDF2] leading-snug">
                                      <span className="text-rose-400 font-bold">[{f.severity || 'INFO'}]</span>{' '}
                                      {f.message}
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {trap.green_flags && trap.green_flags.length > 0 && (
                            <div className="glass-card rounded-xl p-4">
                              <div className="flex items-center gap-2 mb-3">
                                <Check className="w-4 h-4 text-emerald-400" />
                                <span className="text-xs font-bold text-emerald-300 uppercase tracking-wider">
                                  Green Flags ({trap.green_flags.length})
                                </span>
                              </div>
                              <div className="space-y-2">
                                {trap.green_flags.map((f, i) => (
                                  <div key={i} className="flex items-start gap-2 p-2 rounded-lg bg-emerald-500/5 border border-emerald-500/20">
                                    <Check className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
                                    <div className="text-xs text-[#E8EDF2] leading-snug">{f.message}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          <div className={`glass-card rounded-xl p-4 text-center ${
                            trap.recommendation?.includes('BUY') ? 'border-emerald-500/30' :
                            trap.recommendation?.includes('AVOID') ? 'border-rose-500/30' :
                            'border-amber-500/30'
                          }`}>
                            <div className="text-[10px] text-[#8D9AAA] uppercase font-bold tracking-wider mb-1">
                              Recommendation
                            </div>
                            <div className={`text-lg font-black ${
                              trap.recommendation?.includes('BUY') ? 'text-emerald-300' :
                              trap.recommendation?.includes('AVOID') ? 'text-rose-300' :
                              'text-amber-300'
                            }`}>
                              {trap.recommendation || 'HOLD'}
                            </div>
                          </div>

                          <div className="text-[10px] text-[#5F6B78] text-center pt-2 border-t border-white/5 flex items-center justify-center gap-3">
                            <span>{safeNum(trap.history_years).toFixed(1)} years of history</span>
                            <span>·</span>
                            <span className="flex items-center gap-1">
                              <Activity className="w-3 h-3" />
                              Source: yfinance + Nasdaq
                            </span>
                          </div>
                        </>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* PAGINATION */}
      {totalPages > 1 && (
        <div className="glass-card rounded-2xl p-4 flex items-center justify-between">
          <button
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="px-4 py-2 rounded-lg glass-panel hover:bg-white/5 text-[#8D9AAA] hover:text-white text-xs font-bold transition cursor-pointer disabled:opacity-30"
          >
            ← Previous
          </button>
          <div className="flex items-center gap-2">
            {Array.from({ length: totalPages }).map((_, i) => {
              const show = i === 0 || i === totalPages - 1 || Math.abs(i - page) <= 1;
              const isEllipsis = !show && (i === 1 || i === totalPages - 2);
              if (isEllipsis) return <span key={i} className="text-[#5F6B78] text-xs">...</span>;
              if (!show) return null;
              return (
                <button
                  key={i}
                  onClick={() => setPage(i)}
                  className={`w-8 h-8 rounded-lg text-xs font-bold transition cursor-pointer ${
                    page === i
                      ? 'bg-emerald-600 text-white'
                      : 'glass-panel text-[#8D9AAA] hover:text-white'
                  }`}
                >
                  {i + 1}
                </button>
              );
            })}
          </div>
          <button
            onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1}
            className="px-4 py-2 rounded-lg glass-panel hover:bg-white/5 text-[#8D9AAA] hover:text-white text-xs font-bold transition cursor-pointer disabled:opacity-30"
          >
            Next →
          </button>
        </div>
      )}

      <div className="text-xs text-[#5F6B78] text-center">
        Showing {page * perPage + 1}-{Math.min((page + 1) * perPage, filtered.length)} of {filtered.length} stocks
      </div>
    </div>
  );
};

export default SignalsView;
