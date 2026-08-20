import React, { useState } from 'react';
import {
  Star,
  Plus,
  Trash2,
  TrendingUp,
  ArrowUpRight,
  ArrowDownRight,
  Bell,
  BellRing,
  Edit3,
  Search,
  SlidersHorizontal,
  Zap,
  Radio,
  ExternalLink,
  CheckCircle2,
  AlertTriangle,
  Pin,
  Sparkles,
  LayoutGrid,
  List as ListIcon
} from 'lucide-react';
import { TickerInfo, WatchlistEntry, TradingSignal } from '../types';

interface WatchlistViewProps {
  tickers: TickerInfo[];
  signals: TradingSignal[];
  watchlist: WatchlistEntry[];
  onToggleWatchlist: (pair: string) => void;
  onUpdateAlerts: (pair: string, alertHigh?: number, alertLow?: number) => void;
  onUpdateNotes: (pair: string, notes: string) => void;
  onTogglePin: (pair: string) => void;
  onNavigateToTrading: (pair: string) => void;
  onNavigateToSignals: (pair: string) => void;
}

export const WatchlistView: React.FC<WatchlistViewProps> = ({
  tickers,
  signals,
  watchlist,
  onToggleWatchlist,
  onUpdateAlerts,
  onUpdateNotes,
  onTogglePin,
  onNavigateToTrading,
  onNavigateToSignals,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterMode, setFilterMode] = useState<'all' | 'bullish' | 'bearish' | 'alerts' | 'pinned'>('all');
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [selectedPairToAdd, setSelectedPairToAdd] = useState('');
  const [editingNotesPair, setEditingNotesPair] = useState<string | null>(null);
  const [noteDraft, setNoteDraft] = useState('');
  const [editingAlertPair, setEditingAlertPair] = useState<string | null>(null);
  const [alertHighDraft, setAlertHighDraft] = useState<string>('');
  const [alertLowDraft, setAlertLowDraft] = useState<string>('');

  // Map watchlist entries with live ticker data
  const watchlistedTickers = watchlist.map((entry) => {
    const ticker = tickers.find((t) => t.pair === entry.pair) || {
      pair: entry.pair,
      name: entry.pair.split('/')[0],
      price: 0,
      change24h: 0,
      high24h: 0,
      low24h: 0,
      volume24h: 0,
      trend: 'NEUTRAL' as const,
      rsi: 50,
      macd: 0,
      atr: 0,
      history: [0, 0, 0, 0, 0, 0, 0, 0],
    };
    const signal = signals.find((s) => s.pair === entry.pair);
    return {
      entry,
      ticker,
      signal,
    };
  });

  // Sort pinned items first
  const sortedItems = [...watchlistedTickers].sort((a, b) => {
    if (a.entry.pinned && !b.entry.pinned) return -1;
    if (!a.entry.pinned && b.entry.pinned) return 1;
    return b.ticker.volume24h - a.ticker.volume24h;
  });

  // Filter
  const filteredItems = sortedItems.filter((item) => {
    const matchSearch =
      item.ticker.pair.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.ticker.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.entry.notes && item.entry.notes.toLowerCase().includes(searchTerm.toLowerCase()));

    if (!matchSearch) return false;

    if (filterMode === 'bullish') return item.ticker.trend === 'BULLISH';
    if (filterMode === 'bearish') return item.ticker.trend === 'BEARISH';
    if (filterMode === 'alerts') return item.entry.alertHigh || item.entry.alertLow;
    if (filterMode === 'pinned') return item.entry.pinned;

    return true;
  });

  // Unwatched tickers available to add
  const availableTickersToAdd = tickers.filter(
    (t) => !watchlist.some((w) => w.pair === t.pair)
  );

  const handleAddSelectedPair = () => {
    if (selectedPairToAdd) {
      onToggleWatchlist(selectedPairToAdd);
      setSelectedPairToAdd('');
    }
  };

  const handleOpenNotes = (pair: string, currentNotes?: string) => {
    setEditingNotesPair(pair);
    setNoteDraft(currentNotes || '');
  };

  const handleSaveNotes = (pair: string) => {
    onUpdateNotes(pair, noteDraft);
    setEditingNotesPair(null);
  };

  const handleOpenAlerts = (pair: string, high?: number, low?: number) => {
    setEditingAlertPair(pair);
    setAlertHighDraft(high ? high.toString() : '');
    setAlertLowDraft(low ? low.toString() : '');
  };

  const handleSaveAlerts = (pair: string) => {
    const high = alertHighDraft ? parseFloat(alertHighDraft) : undefined;
    const low = alertLowDraft ? parseFloat(alertLowDraft) : undefined;
    onUpdateAlerts(pair, high, low);
    setEditingAlertPair(null);
  };

  const handleAddBundle = (pairs: string[]) => {
    pairs.forEach((p) => {
      if (!watchlist.some((w) => w.pair === p)) {
        onToggleWatchlist(p);
      }
    });
  };

  // Stats calculation
  const totalWatchlist = watchlist.length;
  const topGainer = [...watchlistedTickers].sort((a, b) => b.ticker.change24h - a.ticker.change24h)[0];
  const bullishCount = watchlistedTickers.filter((w) => w.ticker.trend === 'BULLISH').length;
  const totalAlerts = watchlistedTickers.filter((w) => w.entry.alertHigh || w.entry.alertLow).length;

  return (
    <div id="watchlist-view" className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#16202B] to-[#131A22] border border-[#26313D] shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0">
              <Star className="w-5 h-5 fill-amber-400" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-lg sm:text-xl font-bold text-white tracking-wide">
                  Market Watchlist & Custom Radar
                </h2>
                <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 font-bold border border-amber-500/20 font-mono">
                  {totalWatchlist} PAIRS TRACKED
                </span>
              </div>
              <p className="text-xs text-[#8D9AAA] mt-0.5">
                Pin target assets, set automated price breakout alerts, attach trade thesis notes, and execute rapid orders.
              </p>
            </div>
          </div>

          {/* Quick Add Bar */}
          <div className="flex items-center gap-2 w-full md:w-auto">
            <div className="relative flex-1 md:w-56">
              <select
                value={selectedPairToAdd}
                onChange={(e) => setSelectedPairToAdd(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white focus:outline-none focus:border-amber-500 cursor-pointer"
              >
                <option value="">+ Select pair to add...</option>
                {availableTickersToAdd.map((t) => (
                  <option key={t.pair} value={t.pair}>
                    {t.pair} ({t.name}) - ${t.price.toLocaleString()}
                  </option>
                ))}
              </select>
            </div>
            <button
              onClick={handleAddSelectedPair}
              disabled={!selectedPairToAdd}
              className="px-3.5 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 disabled:opacity-40 disabled:hover:bg-amber-500 text-black font-bold text-xs flex items-center gap-1.5 transition-all shadow-md shadow-amber-500/20 cursor-pointer shrink-0"
            >
              <Plus className="w-4 h-4" />
              <span>Add</span>
            </button>
          </div>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <div className="p-3.5 sm:p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Tracked Assets</span>
          <div className="text-lg sm:text-xl font-bold font-mono text-white mt-1">
            {totalWatchlist} <span className="text-xs font-normal text-[#5F6B78]">Pairs</span>
          </div>
          <span className="text-[10px] text-amber-400 mt-1 block font-mono">Live Kraken Synced</span>
        </div>

        <div className="p-3.5 sm:p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Top Gainer</span>
          <div className="text-lg sm:text-xl font-bold font-mono text-emerald-400 mt-1 truncate">
            {topGainer ? `${topGainer.ticker.pair.split('/')[0]} (+${topGainer.ticker.change24h.toFixed(1)}%)` : 'None'}
          </div>
          <span className="text-[10px] text-[#5F6B78] mt-1 block font-mono">24h Leader</span>
        </div>

        <div className="p-3.5 sm:p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Bullish Bias</span>
          <div className="text-lg sm:text-xl font-bold font-mono text-cyan-400 mt-1">
            {totalWatchlist > 0 ? `${Math.round((bullishCount / totalWatchlist) * 100)}%` : '0%'}
          </div>
          <span className="text-[10px] text-cyan-400/80 mt-1 block font-mono">{bullishCount} Bullish Trends</span>
        </div>

        <div className="p-3.5 sm:p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Active Alerts</span>
          <div className="text-lg sm:text-xl font-bold font-mono text-purple-400 mt-1">
            {totalAlerts} <span className="text-xs font-normal text-[#5F6B78]">Triggers</span>
          </div>
          <span className="text-[10px] text-purple-400/80 mt-1 block font-mono">Telegram Ready</span>
        </div>
      </div>

      {/* Controls & Filter Bar */}
      <div className="p-3.5 sm:p-4 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-lg">
        {/* Search */}
        <div className="relative flex-1 max-w-xs">
          <Search className="w-4 h-4 text-[#5F6B78] absolute left-3 top-2.5" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Filter watchlist or notes..."
            className="w-full pl-9 pr-3 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-amber-500"
          />
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
          {[
            { id: 'all', label: 'All' },
            { id: 'pinned', label: '📌 Pinned' },
            { id: 'bullish', label: '🟢 Bullish' },
            { id: 'bearish', label: '🔴 Bearish' },
            { id: 'alerts', label: '🔔 With Alerts' },
          ].map((pill) => (
            <button
              key={pill.id}
              onClick={() => setFilterMode(pill.id as any)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                filterMode === pill.id
                  ? 'bg-amber-500 text-black font-bold shadow-sm'
                  : 'bg-[#0B0F14] text-[#8D9AAA] hover:bg-[#18212B] hover:text-white border border-[#26313D]'
              }`}
            >
              {pill.label}
            </button>
          ))}
        </div>

        {/* View Mode Toggle */}
        <div className="flex items-center gap-1 bg-[#0B0F14] p-1 rounded-xl border border-[#26313D] self-end sm:self-auto">
          <button
            onClick={() => setViewMode('grid')}
            title="Grid View"
            className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
              viewMode === 'grid' ? 'bg-amber-500 text-black' : 'text-[#8D9AAA] hover:text-white'
            }`}
          >
            <LayoutGrid className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setViewMode('table')}
            title="Table View"
            className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
              viewMode === 'table' ? 'bg-amber-500 text-black' : 'text-[#8D9AAA] hover:text-white'
            }`}
          >
            <ListIcon className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      {filteredItems.length === 0 ? (
        <div className="p-8 sm:p-12 rounded-2xl bg-[#131A22] border border-[#26313D] text-center space-y-4">
          <div className="w-14 h-14 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 mx-auto">
            <Star className="w-7 h-7" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">No Pairs in Watchlist</h3>
            <p className="text-xs text-[#8D9AAA] max-w-md mx-auto mt-1">
              Add your favorite cryptocurrency pairs from the selector above or click a starter preset below to quickly populate your trading radar.
            </p>
          </div>

          {/* Starter presets */}
          <div className="pt-2 flex flex-wrap items-center justify-center gap-2 max-w-lg mx-auto">
            <button
              onClick={() => handleAddBundle(['BTC/USD', 'ETH/USD', 'SOL/USD'])}
              className="px-3 py-1.5 rounded-xl bg-[#1A2530] hover:bg-amber-500 hover:text-black border border-[#26313D] text-xs font-semibold text-white transition-colors cursor-pointer flex items-center gap-1.5"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>Add Top 3 Bluechips</span>
            </button>
            <button
              onClick={() => handleAddBundle(['AVAX/USD', 'LINK/USD', 'DOT/USD'])}
              className="px-3 py-1.5 rounded-xl bg-[#1A2530] hover:bg-amber-500 hover:text-black border border-[#26313D] text-xs font-semibold text-white transition-colors cursor-pointer flex items-center gap-1.5"
            >
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
              <span>Add Layer 1 & Infra</span>
            </button>
            <button
              onClick={() => handleAddBundle(['XRP/USD', 'ADA/USD', 'LTC/USD', 'BCH/USD'])}
              className="px-3 py-1.5 rounded-xl bg-[#1A2530] hover:bg-amber-500 hover:text-black border border-[#26313D] text-xs font-semibold text-white transition-colors cursor-pointer flex items-center gap-1.5"
            >
              <Sparkles className="w-3.5 h-3.5 text-purple-400" />
              <span>Add Major Altcoins</span>
            </button>
          </div>
        </div>
      ) : viewMode === 'grid' ? (
        /* Grid View Cards */
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredItems.map(({ entry, ticker, signal }) => {
            const isPositive = ticker.change24h >= 0;
            const minPrice = Math.min(...ticker.history) * 0.998;
            const maxPrice = Math.max(...ticker.history) * 1.002;
            const priceSpread = maxPrice - minPrice || 1;

            const isHighAlertTriggered = entry.alertHigh && ticker.price >= entry.alertHigh;
            const isLowAlertTriggered = entry.alertLow && ticker.price <= entry.alertLow;

            return (
              <div
                key={ticker.pair}
                className={`p-4 sm:p-5 rounded-2xl bg-[#131A22] border transition-all duration-200 shadow-lg space-y-4 flex flex-col justify-between ${
                  entry.pinned ? 'border-amber-500/40 bg-gradient-to-b from-[#16202B] to-[#131A22]' : 'border-[#26313D] hover:border-[#384759]'
                }`}
              >
                <div>
                  {/* Card Header */}
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2.5">
                      <div className="w-9 h-9 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-center font-bold text-white text-xs">
                        {ticker.pair.split('/')[0]}
                      </div>
                      <div>
                        <div className="flex items-center gap-1.5">
                          <span className="font-mono font-bold text-white text-base">{ticker.pair}</span>
                          {entry.pinned && (
                            <span title="Pinned Asset" className="text-amber-400">
                              <Pin className="w-3.5 h-3.5 fill-amber-400" />
                            </span>
                          )}
                        </div>
                        <span className="text-[11px] text-[#8D9AAA] block">{ticker.name}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-1">
                      {/* Pin Button */}
                      <button
                        onClick={() => onTogglePin(ticker.pair)}
                        title={entry.pinned ? 'Unpin' : 'Pin to top'}
                        className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                          entry.pinned ? 'text-amber-400 bg-amber-500/10' : 'text-[#5F6B78] hover:text-white'
                        }`}
                      >
                        <Pin className={`w-3.5 h-3.5 ${entry.pinned ? 'fill-current' : ''}`} />
                      </button>

                      {/* Remove Button */}
                      <button
                        onClick={() => onToggleWatchlist(ticker.pair)}
                        title="Remove from Watchlist"
                        className="p-1.5 rounded-lg text-[#5F6B78] hover:text-rose-400 hover:bg-rose-500/10 transition-colors cursor-pointer"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  {/* Price & Change Row */}
                  <div className="mt-3 flex items-baseline justify-between">
                    <div>
                      <span className="text-xl sm:text-2xl font-black font-mono text-white">
                        ${ticker.price >= 1 ? ticker.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : ticker.price.toFixed(4)}
                      </span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <span
                        className={`px-2 py-0.5 rounded-lg text-xs font-mono font-bold flex items-center gap-0.5 ${
                          isPositive
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        }`}
                      >
                        {isPositive ? <ArrowUpRight className="w-3.5 h-3.5" /> : <ArrowDownRight className="w-3.5 h-3.5" />}
                        {isPositive ? '+' : ''}
                        {ticker.change24h.toFixed(2)}%
                      </span>
                    </div>
                  </div>

                  {/* Mini Sparkline Chart */}
                  <div className="mt-3 h-14 w-full bg-[#0B0F14] rounded-xl border border-[#26313D]/70 p-2 flex items-end gap-1.5 relative overflow-hidden">
                    {ticker.history.map((val, idx) => {
                      const heightPct = Math.max(15, Math.min(95, ((val - minPrice) / priceSpread) * 100));
                      const isBarGreen = idx > 0 && val >= ticker.history[idx - 1];
                      return (
                        <div
                          key={idx}
                          className="flex-1 flex flex-col justify-end h-full"
                          title={`$${val.toLocaleString()}`}
                        >
                          <div
                            className={`w-full rounded-t transition-all duration-300 ${
                              isBarGreen ? 'bg-emerald-500/70' : 'bg-blue-500/70'
                            }`}
                            style={{ height: `${heightPct}%` }}
                          />
                        </div>
                      );
                    })}
                  </div>

                  {/* Technical Indicators Pill Row */}
                  <div className="mt-3 grid grid-cols-3 gap-2 text-center font-mono text-[10px]">
                    <div className="p-2 rounded-lg bg-[#0B0F14] border border-[#26313D]/60">
                      <span className="text-[#5F6B78] block">RSI (14)</span>
                      <span className={`font-bold ${ticker.rsi > 70 ? 'text-amber-400' : ticker.rsi < 30 ? 'text-blue-400' : 'text-white'}`}>
                        {ticker.rsi.toFixed(1)}
                      </span>
                    </div>
                    <div className="p-2 rounded-lg bg-[#0B0F14] border border-[#26313D]/60">
                      <span className="text-[#5F6B78] block">TREND</span>
                      <span className={`font-bold ${ticker.trend === 'BULLISH' ? 'text-emerald-400' : ticker.trend === 'BEARISH' ? 'text-rose-400' : 'text-slate-400'}`}>
                        {ticker.trend}
                      </span>
                    </div>
                    <div className="p-2 rounded-lg bg-[#0B0F14] border border-[#26313D]/60">
                      <span className="text-[#5F6B78] block">ATR</span>
                      <span className="font-bold text-cyan-400">
                        ${ticker.atr >= 1 ? ticker.atr.toFixed(2) : ticker.atr.toFixed(3)}
                      </span>
                    </div>
                  </div>

                  {/* Price Alerts Status */}
                  {(entry.alertHigh || entry.alertLow) && (
                    <div className="mt-3 p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-[11px] font-mono flex items-center justify-between">
                      <div className="flex items-center gap-1.5">
                        <BellRing className={`w-3.5 h-3.5 ${isHighAlertTriggered || isLowAlertTriggered ? 'text-amber-400 animate-bounce' : 'text-purple-400'}`} />
                        <span className="text-[#8D9AAA]">Alerts:</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {entry.alertHigh && (
                          <span className={`px-1.5 py-0.5 rounded ${isHighAlertTriggered ? 'bg-emerald-500/20 text-emerald-300 font-bold' : 'text-[#8D9AAA]'}`}>
                            ▲ ${entry.alertHigh.toLocaleString()}
                          </span>
                        )}
                        {entry.alertLow && (
                          <span className={`px-1.5 py-0.5 rounded ${isLowAlertTriggered ? 'bg-rose-500/20 text-rose-300 font-bold' : 'text-[#8D9AAA]'}`}>
                            ▼ ${entry.alertLow.toLocaleString()}
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Notes / Thesis Section */}
                  {entry.notes && (
                    <div className="mt-3 p-2.5 rounded-xl bg-[#0B0F14]/70 border border-[#26313D]/60 text-xs text-[#8D9AAA] italic flex items-start gap-2">
                      <Edit3 className="w-3 h-3 text-amber-400 shrink-0 mt-0.5" />
                      <span className="line-clamp-2">{entry.notes}</span>
                    </div>
                  )}

                  {/* Signal Radar Hint if any */}
                  {signal && (
                    <div className="mt-3 px-3 py-1.5 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-between text-xs">
                      <div className="flex items-center gap-1.5">
                        <Radio className="w-3.5 h-3.5 text-blue-400" />
                        <span className="font-bold text-blue-300">{signal.signal} Signal</span>
                      </div>
                      <span className="font-mono text-emerald-400 font-bold">{signal.confidence}% Conf.</span>
                    </div>
                  )}
                </div>

                {/* Card Action Footer */}
                <div className="pt-2 border-t border-[#26313D]/60 flex items-center justify-between gap-2">
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => handleOpenAlerts(ticker.pair, entry.alertHigh, entry.alertLow)}
                      title="Set Price Alerts"
                      className="p-2 rounded-lg bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-purple-400 border border-[#26313D] transition-colors cursor-pointer"
                    >
                      <Bell className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => handleOpenNotes(ticker.pair, entry.notes)}
                      title="Edit Thesis Note"
                      className="p-2 rounded-lg bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-amber-400 border border-[#26313D] transition-colors cursor-pointer"
                    >
                      <Edit3 className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => onNavigateToSignals(ticker.pair)}
                      title="View Signals Radar"
                      className="p-2 rounded-lg bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-blue-400 border border-[#26313D] transition-colors cursor-pointer"
                    >
                      <Radio className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  <button
                    onClick={() => onNavigateToTrading(ticker.pair)}
                    className="flex-1 max-w-[130px] py-1.5 px-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 transition-all shadow-md shadow-blue-600/20 cursor-pointer"
                  >
                    <Zap className="w-3.5 h-3.5 fill-current" />
                    <span>Trade</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* Table View */
        <div className="p-4 sm:p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="text-[#5F6B78] border-b border-[#26313D] text-[11px]">
                  <th className="pb-3 pl-2">PAIR</th>
                  <th className="pb-3 text-right">PRICE (USD)</th>
                  <th className="pb-3 text-right">24H CHANGE</th>
                  <th className="pb-3 text-center hidden sm:table-cell">RSI</th>
                  <th className="pb-3 text-center hidden md:table-cell">TREND</th>
                  <th className="pb-3 text-center hidden lg:table-cell">ALERTS</th>
                  <th className="pb-3 text-right pr-2">ACTIONS</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#26313D]/40">
                {filteredItems.map(({ entry, ticker, signal }) => {
                  const isPositive = ticker.change24h >= 0;
                  return (
                    <tr key={ticker.pair} className="hover:bg-[#1A2530]/60 transition-colors">
                      <td className="py-3 pl-2 font-bold text-white font-sans flex items-center gap-2">
                        <button
                          onClick={() => onTogglePin(ticker.pair)}
                          className={`p-1 rounded cursor-pointer ${
                            entry.pinned ? 'text-amber-400' : 'text-[#5F6B78] hover:text-white'
                          }`}
                        >
                          <Pin className={`w-3.5 h-3.5 ${entry.pinned ? 'fill-current' : ''}`} />
                        </button>
                        <span className="w-6 h-6 rounded-md bg-[#0B0F14] border border-[#26313D] flex items-center justify-center text-[10px] font-bold font-mono">
                          {ticker.pair.split('/')[0]}
                        </span>
                        <div>
                          <span>{ticker.pair}</span>
                          <span className="text-[10px] text-[#5F6B78] block sm:hidden">{ticker.name}</span>
                        </div>
                      </td>
                      <td className="py-3 text-right font-bold text-white">
                        ${ticker.price >= 1 ? ticker.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : ticker.price.toFixed(4)}
                      </td>
                      <td className="py-3 text-right">
                        <span
                          className={`inline-block px-2 py-0.5 rounded font-bold ${
                            isPositive
                              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                              : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                          }`}
                        >
                          {isPositive ? '+' : ''}
                          {ticker.change24h.toFixed(2)}%
                        </span>
                      </td>
                      <td className="py-3 text-center text-white hidden sm:table-cell">
                        {ticker.rsi.toFixed(1)}
                      </td>
                      <td className="py-3 text-center hidden md:table-cell">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          ticker.trend === 'BULLISH' ? 'text-emerald-400 bg-emerald-500/10' : ticker.trend === 'BEARISH' ? 'text-rose-400 bg-rose-500/10' : 'text-slate-400 bg-slate-500/10'
                        }`}>
                          {ticker.trend}
                        </span>
                      </td>
                      <td className="py-3 text-center text-[#8D9AAA] hidden lg:table-cell">
                        {entry.alertHigh || entry.alertLow ? (
                          <span className="text-purple-400 font-bold flex items-center justify-center gap-1">
                            <Bell className="w-3 h-3" /> Active
                          </span>
                        ) : (
                          <span className="text-[#5F6B78]">None</span>
                        )}
                      </td>
                      <td className="py-3 text-right pr-2">
                        <div className="flex items-center justify-end gap-1.5 font-sans">
                          <button
                            onClick={() => handleOpenAlerts(ticker.pair, entry.alertHigh, entry.alertLow)}
                            title="Set Price Alert"
                            className="p-1.5 rounded-md bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-purple-400 border border-[#26313D] cursor-pointer"
                          >
                            <Bell className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => onNavigateToTrading(ticker.pair)}
                            className="px-2.5 py-1 rounded-md bg-blue-600 hover:bg-blue-500 text-white font-bold text-[11px] cursor-pointer flex items-center gap-1"
                          >
                            <Zap className="w-3 h-3" />
                            <span>Trade</span>
                          </button>
                          <button
                            onClick={() => onToggleWatchlist(ticker.pair)}
                            title="Remove"
                            className="p-1.5 rounded-md bg-[#0B0F14] hover:bg-rose-500/20 text-[#5F6B78] hover:text-rose-400 border border-[#26313D] cursor-pointer"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Price Alert Modal */}
      {editingAlertPair && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="w-full max-w-md p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]">
              <div className="flex items-center gap-2">
                <BellRing className="w-5 h-5 text-purple-400" />
                <h3 className="text-base font-bold text-white">Price Alert: {editingAlertPair}</h3>
              </div>
              <button
                onClick={() => setEditingAlertPair(null)}
                className="text-[#8D9AAA] hover:text-white text-sm cursor-pointer"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-[#8D9AAA]">
              Receive instant in-app and Telegram push alerts when {editingAlertPair} crosses your target levels.
            </p>

            <div className="space-y-3 font-mono text-xs">
              <div>
                <label className="block text-[11px] font-bold text-emerald-400 mb-1">
                  ▲ Alert High (Breakout Target USD)
                </label>
                <input
                  type="number"
                  step="any"
                  value={alertHighDraft}
                  onChange={(e) => setAlertHighDraft(e.target.value)}
                  placeholder="e.g. 72000"
                  className="w-full px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white focus:outline-none focus:border-emerald-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold text-rose-400 mb-1">
                  ▼ Alert Low (Support / Stop Trigger USD)
                </label>
                <input
                  type="number"
                  step="any"
                  value={alertLowDraft}
                  onChange={(e) => setAlertLowDraft(e.target.value)}
                  placeholder="e.g. 64000"
                  className="w-full px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white focus:outline-none focus:border-rose-500 font-mono"
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-3 border-t border-[#26313D]">
              <button
                onClick={() => setEditingAlertPair(null)}
                className="px-4 py-2 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] text-xs font-semibold text-[#8D9AAA] border border-[#26313D] cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={() => handleSaveAlerts(editingAlertPair)}
                className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-xs font-bold text-white shadow-md shadow-purple-600/30 cursor-pointer"
              >
                Save Alerts
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Notes / Trade Thesis Modal */}
      {editingNotesPair && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="w-full max-w-md p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]">
              <div className="flex items-center gap-2">
                <Edit3 className="w-5 h-5 text-amber-400" />
                <h3 className="text-base font-bold text-white">Trade Thesis: {editingNotesPair}</h3>
              </div>
              <button
                onClick={() => setEditingNotesPair(null)}
                className="text-[#8D9AAA] hover:text-white text-sm cursor-pointer"
              >
                ✕
              </button>
            </div>

            <div>
              <label className="block text-[11px] font-bold text-[#8D9AAA] mb-1.5">
                Trading Notes, Entry Plan & Strategy Reminders
              </label>
              <textarea
                value={noteDraft}
                onChange={(e) => setNoteDraft(e.target.value)}
                rows={4}
                placeholder="e.g. Wait for daily candle close above $69K with volume expansion before scaling in..."
                className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-amber-500 font-sans"
              />
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-[#26313D]">
              <button
                onClick={() => setEditingNotesPair(null)}
                className="px-4 py-2 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] text-xs font-semibold text-[#8D9AAA] border border-[#26313D] cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={() => handleSaveNotes(editingNotesPair)}
                className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-xs font-bold text-black shadow-md shadow-amber-500/20 cursor-pointer"
              >
                Save Notes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
