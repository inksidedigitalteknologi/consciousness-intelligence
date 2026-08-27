import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  TrendingUp,
  Search,
  Star,
  RefreshCw,
  Wifi,
  WifiOff,
  Loader2,
  AlertCircle,
  Clock,
  BarChart3,
  Gauge,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  Zap,
  Shield,
  Eye,
  Filter
} from 'lucide-react';
import { TickerInfo } from '../types';
import { useWebSocketStatus, useWebSocketChannel } from '../contexts/WebSocketContext';

// ============================================================
// CONSTANTS
// ============================================================

const WATCHLIST_KEY = 'inkside_watchlist_data';
const AUTO_REFRESH_INTERVAL = 30000; // 30 detik

// ============================================================
// HELPERS
// ============================================================

const loadWatchlist = (): string[] => {
  try {
    const data = localStorage.getItem(WATCHLIST_KEY);
    if (data) {
      const parsed = JSON.parse(data);
      return parsed.map((item: any) => item.pair);
    }
    return [];
  } catch {
    return [];
  }
};

const saveWatchlist = (watchlist: string[]) => {
  try {
    const existing = localStorage.getItem(WATCHLIST_KEY);
    const parsed = existing ? JSON.parse(existing) : [];
    const updated = watchlist.map(pair => {
      const found = parsed.find((item: any) => item.pair === pair);
      return found || { pair, pinned: false, notes: '', alertHigh: undefined, alertLow: undefined };
    });
    localStorage.setItem(WATCHLIST_KEY, JSON.stringify(updated));
  } catch (e) {
    console.error('Failed to save watchlist:', e);
  }
};

// ============================================================
// TYPES
// ============================================================

interface MarketViewProps {
  tickers: TickerInfo[];
  watchlist?: string[];
  onToggleWatchlist?: (pair: string) => void;
  onSelectPair?: (pair: string) => void;
  wsConnected?: boolean;
  lastUpdate?: Date;
}

// ============================================================
// MAIN COMPONENT
// ============================================================

export const MarketView: React.FC<MarketViewProps> = ({
  tickers,
  watchlist = [],
  onToggleWatchlist,
  onSelectPair,
  wsConnected = false,
  lastUpdate,
}) => {
  // ============================================================
  // WEBSOCKET
  // ============================================================
  
  const { isConnected, status } = useWebSocketStatus();

  useWebSocketChannel('market', (data) => {
    if (data?.type === 'ticker_update') {
      // Ticker akan diupdate via props dari parent
      setLastUpdateTime(new Date().toLocaleTimeString());
    }
  });

  // ============================================================
  // STATE
  // ============================================================
  
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTicker, setSelectedTicker] = useState<TickerInfo | null>(
    tickers.length > 0 ? tickers[0] : null
  );
  const [activeTab, setActiveTab] = useState<'1h' | '4h' | '1d'>('1h');
  const [onlyWatchlist, setOnlyWatchlist] = useState(false);
  const [localWatchlist, setLocalWatchlist] = useState<string[]>(loadWatchlist);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [lastUpdateTime, setLastUpdateTime] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  // ============================================================
  // EFFECTS
  // ============================================================

  useEffect(() => {
    if (watchlist.length > 0) {
      setLocalWatchlist(watchlist);
    }
  }, [watchlist]);

  // Auto-select first ticker jika belum ada
  useEffect(() => {
    if (tickers.length > 0 && !selectedTicker) {
      setSelectedTicker(tickers[0]);
    }
  }, [tickers, selectedTicker]);

  // ============================================================
  // HANDLERS
  // ============================================================

  const toggleWatchlist = useCallback((pair: string) => {
    setLocalWatchlist(prev => {
      const exists = prev.includes(pair);
      const newList = exists ? prev.filter(p => p !== pair) : [...prev, pair];
      saveWatchlist(newList);
      if (onToggleWatchlist) {
        onToggleWatchlist(pair);
      }
      return newList;
    });
  }, [onToggleWatchlist]);

  const handleSelectPair = useCallback((ticker: TickerInfo) => {
    setSelectedTicker(ticker);
    if (onSelectPair) {
      onSelectPair(ticker.pair);
    }
    setTimeout(() => {
      document.getElementById('market-spotlight')?.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      });
    }, 100);
  }, [onSelectPair]);

  const handleRefresh = useCallback(() => {
    setIsRefreshing(true);
    // Refresh akan di-trigger dari parent via props
    setTimeout(() => setIsRefreshing(false), 1000);
  }, []);

  // ============================================================
  // MEMOIZED VALUES
  // ============================================================

  const isInWatchlist = useCallback((pair: string) => {
    return localWatchlist.includes(pair);
  }, [localWatchlist]);

  const filteredTickers = useMemo(() => {
    return tickers.filter((t) => {
      const matchSearch =
        t.pair.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.name.toLowerCase().includes(searchTerm.toLowerCase());
      if (!matchSearch) return false;
      if (onlyWatchlist) return localWatchlist.includes(t.pair);
      return true;
    });
  }, [tickers, searchTerm, onlyWatchlist, localWatchlist]);

  const currentTicker = useMemo(() => {
    return selectedTicker || tickers[0] || null;
  }, [selectedTicker, tickers]);

  // ============================================================
  // RENDER HELPERS
  // ============================================================

  const renderMiniChart = (ticker: TickerInfo) => {
    if (!ticker.history || ticker.history.length === 0) {
      return <div className="w-full text-center text-[#5F6B78] text-sm">No chart data</div>;
    }

    const min = Math.min(...ticker.history) * 0.998;
    const max = Math.max(...ticker.history) * 1.002;
    const range = max - min || 1;

    return ticker.history.map((val, idx) => {
      const heightPct = Math.max(15, Math.min(95, ((val - min) / range) * 100));
      const isGreen = idx > 0 && val >= ticker.history[idx - 1];

      return (
        <div key={idx} className="flex-1 flex flex-col items-center gap-1 group relative">
          <div className="absolute -top-8 bg-[#1A2530] border border-[#26313D] text-white text-[10px] font-mono px-1.5 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-20">
            ${val.toLocaleString()}
          </div>
          <div
            className={`w-full rounded-t-md transition-all duration-300 ${
              isGreen ? 'bg-emerald-500/80 hover:bg-emerald-400' : 'bg-blue-500/80 hover:bg-blue-400'
            }`}
            style={{ height: `${heightPct}%` }}
          />
          <span className="text-[8px] sm:text-[9px] text-[#5F6B78] font-mono">
            T-{ticker.history.length - idx}
          </span>
        </div>
      );
    });
  };

  // ============================================================
  // LOADING STATE
  // ============================================================

  if (tickers.length === 0) {
    return (
      <div className="p-12 text-center text-[#5F6B78]">
        <div className="text-4xl mb-3">📊</div>
        <p className="text-sm font-medium">No market data available</p>
        <p className="text-xs mt-1">Connect to exchange to see live prices</p>
        {isConnected && (
          <div className="mt-3 flex items-center justify-center gap-2">
            <Loader2 className="w-4 h-4 animate-spin text-cyan-400" />
            <span className="text-xs text-cyan-400">Waiting for data...</span>
          </div>
        )}
      </div>
    );
  }

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div id="market-view" className="space-y-4 sm:space-y-6 pb-12">

      {/* ============================================================
          HEADER
          ============================================================ */}
      <div className="p-4 sm:p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-white tracking-wide flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-400" />
            Live Market Tickers
            {isConnected ? (
              <Wifi className="w-3.5 h-3.5 text-emerald-400" />
            ) : (
              <WifiOff className="w-3.5 h-3.5 text-amber-400" />
            )}
            <span className="text-[10px] font-normal text-[#5F6B78]">
              {isConnected ? '● LIVE' : '○ OFFLINE'}
            </span>
          </h2>
          <p className="text-xs text-[#8D9AAA] flex items-center gap-2">
            Direct feed from Kraken Exchange
            {lastUpdateTime && (
              <>
                <span className="text-[#5F6B78]">•</span>
                <span className="text-[#5F6B78]">Updated: {lastUpdateTime}</span>
              </>
            )}
            {isRefreshing && (
              <>
                <span className="text-[#5F6B78]">•</span>
                <span className="text-cyan-400 animate-pulse flex items-center gap-1">
                  <Loader2 className="w-3 h-3 animate-spin" />
                  Refreshing...
                </span>
              </>
            )}
          </p>
        </div>

        <div className="flex items-center gap-2 w-full md:w-auto">
          <button
            onClick={() => setOnlyWatchlist(!onlyWatchlist)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer shrink-0 ${
              onlyWatchlist
                ? 'bg-amber-500 text-black font-bold shadow-md shadow-amber-500/20'
                : 'bg-[#0B0F14] text-[#8D9AAA] hover:text-white border border-[#26313D]'
            }`}
          >
            <Star className={`w-3.5 h-3.5 ${onlyWatchlist ? 'fill-black' : ''}`} />
            <span>Watchlist ({localWatchlist.length})</span>
          </button>

          <button
            onClick={handleRefresh}
            className="p-1.5 rounded-lg bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors"
            title="Refresh"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          </button>

          <div className="relative flex-1 md:w-60">
            <Search className="w-4 h-4 text-[#5F6B78] absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search pair..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>
      </div>

      {/* ============================================================
          SPOTLIGHT - Selected Ticker
          ============================================================ */}
      {currentTicker && (
        <div id="market-spotlight" className="p-4 sm:p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-xl">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#26313D]/70">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-center font-bold text-white text-sm shrink-0">
                {currentTicker.pair.split('/')[0]}
              </div>
              <div>
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-lg sm:text-xl font-black text-white font-mono">
                    {currentTicker.pair}
                  </span>
                  <span
                    className={`text-xs font-mono font-bold px-2 py-0.5 rounded ${
                      (currentTicker.change24h ?? 0) >= 0
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                    }`}
                  >
                    {(currentTicker.change24h ?? 0) >= 0 ? '+' : ''}
                    {currentTicker.change24h?.toFixed(2) ?? '0.00'}%
                  </span>

                  <button
                    onClick={() => toggleWatchlist(currentTicker.pair)}
                    title={isInWatchlist(currentTicker.pair) ? 'Remove from Watchlist' : 'Add to Watchlist'}
                    className={`p-1.5 rounded-lg border transition-all cursor-pointer ${
                      isInWatchlist(currentTicker.pair)
                        ? 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                        : 'bg-[#0B0F14] text-[#8D9AAA] hover:text-white border-[#26313D]'
                    }`}
                  >
                    <Star className={`w-3.5 h-3.5 ${isInWatchlist(currentTicker.pair) ? 'fill-amber-400' : ''}`} />
                  </button>
                </div>
                <span className="text-xs text-[#8D9AAA]">
                  {currentTicker.name} · {isConnected ? '🟢 Live' : '🔴 Offline'}
                </span>
              </div>
            </div>

            <div className="flex items-center gap-1.5 bg-[#0B0F14] p-1 rounded-xl border border-[#26313D] self-start sm:self-auto">
              {(['1h', '4h', '1d'] as const).map((tf) => (
                <button
                  key={tf}
                  onClick={() => setActiveTab(tf)}
                  className={`px-3 py-1 rounded-lg text-xs font-mono font-bold transition-colors cursor-pointer ${
                    activeTab === tf ? 'bg-blue-600 text-white' : 'text-[#8D9AAA] hover:text-white'
                  }`}
                >
                  {tf.toUpperCase()}
                </button>
              ))}
            </div>
          </div>

          {/* Chart */}
          <div className="h-48 sm:h-56 w-full bg-[#0B0F14] rounded-xl border border-[#26313D]/80 p-3 sm:p-4 flex flex-col justify-between relative overflow-hidden">
            <div className="absolute inset-0 grid grid-rows-4 grid-cols-6 pointer-events-none opacity-10">
              {Array.from({ length: 24 }).map((_, i) => (
                <div key={i} className="border-b border-r border-white/20" />
              ))}
            </div>

            <div className="flex items-center justify-between text-xs text-[#8D9AAA] font-mono z-10">
              <span>High: ${currentTicker.high24h?.toLocaleString() ?? '0'}</span>
              <span>Low: ${currentTicker.low24h?.toLocaleString() ?? '0'}</span>
            </div>

            <div className="h-28 sm:h-32 w-full flex items-end gap-2 sm:gap-3 px-1 sm:px-2 z-10">
              {currentTicker.history && currentTicker.history.length > 0 ? (
                renderMiniChart(currentTicker)
              ) : (
                <div className="w-full text-center text-[#5F6B78] text-sm">No chart data</div>
              )}
            </div>

            <div className="flex items-center justify-between text-[10px] sm:text-[11px] text-[#5F6B78] font-mono z-10 pt-2 border-t border-[#26313D]/40">
              <span>Price: <strong className="text-white">${currentTicker.price?.toLocaleString() ?? '0'}</strong></span>
              <span className="hidden sm:inline">
                Volume: <strong className="text-white">${((currentTicker.volume24h ?? 0) * (currentTicker.price ?? 0) / 1000000).toFixed(2)}M</strong>
              </span>
            </div>
          </div>

          {/* Indicators */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-3 pt-1">
            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <span className="text-[10px] text-[#8D9AAA] font-semibold uppercase">RSI (14)</span>
              <div className="text-sm sm:text-base font-bold text-white font-mono mt-0.5">
                {currentTicker.rsi?.toFixed(1) ?? '--'}
              </div>
              <span className="text-[10px] text-emerald-400 font-bold">
                {(currentTicker.rsi ?? 0) > 70 ? 'Overbought' : (currentTicker.rsi ?? 0) < 30 ? 'Oversold' : 'Momentum'}
              </span>
            </div>
            
            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <span className="text-[10px] text-[#8D9AAA] font-semibold uppercase">MACD Histogram</span>
              <div className="text-sm sm:text-base font-bold text-white font-mono mt-0.5">
                {currentTicker.macd !== undefined ? `+${currentTicker.macd.toFixed(2)}` : '--'}
              </div>
              <span className="text-[10px] text-emerald-400 font-bold">Positive Expansion</span>
            </div>
            
            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <span className="text-[10px] text-[#8D9AAA] font-semibold uppercase">ATR (14)</span>
              <div className="text-sm sm:text-base font-bold text-white font-mono mt-0.5">
                ${(currentTicker.atr ?? 0) >= 1 
                  ? currentTicker.atr?.toFixed(2) ?? '0.00' 
                  : currentTicker.atr?.toFixed(4) ?? '0.0000'}
              </div>
              <span className="text-[10px] text-blue-400 font-bold">Volatility</span>
            </div>
            
            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <span className="text-[10px] text-[#8D9AAA] font-semibold uppercase">Bid/Ask Spread</span>
              <div className="text-sm sm:text-base font-bold text-white font-mono mt-0.5">
                {currentTicker.bid && currentTicker.ask 
                  ? (currentTicker.ask - currentTicker.bid).toFixed(2) 
                  : '--'}
              </div>
              <span className="text-[10px] text-blue-400 font-bold">
                Depth: {currentTicker.depth?.toFixed(0) ?? '--'}%
              </span>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================
          TICKER LIST
          ============================================================ */}
      <div className="p-4 sm:p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70 mb-3">
          <h3 className="text-xs sm:text-sm font-bold text-white tracking-wider uppercase">
            Available Markets ({filteredTickers.length})
          </h3>
          {onlyWatchlist && (
            <span className="text-[11px] text-amber-400 font-mono font-bold">📌 Filtered to Watchlist</span>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="text-[#5F6B78] border-b border-[#26313D] text-[11px]">
                <th className="pb-3 pl-2">PAIR</th>
                <th className="pb-3 text-right">PRICE</th>
                <th className="pb-3 text-right">24H CHANGE</th>
                <th className="pb-3 text-right hidden sm:table-cell">HIGH</th>
                <th className="pb-3 text-right hidden sm:table-cell">LOW</th>
                <th className="pb-3 text-right hidden md:table-cell">VOLUME</th>
                <th className="pb-3 text-right pr-2">ACTION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#26313D]/40">
              {filteredTickers.map((t) => {
                const isPositive = (t.change24h ?? 0) >= 0;
                const isSelected = selectedTicker?.pair === t.pair;
                const inWatchlist = localWatchlist.includes(t.pair);

                return (
                  <tr
                    key={t.pair}
                    onClick={() => handleSelectPair(t)}
                    className={`hover:bg-[#1A2530] transition-colors cursor-pointer ${
                      isSelected ? 'bg-[#1A2530]/80' : ''
                    }`}
                  >
                    <td className="py-3 pl-2 font-bold text-white font-sans flex items-center gap-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleWatchlist(t.pair);
                        }}
                        className={`p-1 rounded cursor-pointer ${
                          inWatchlist ? 'text-amber-400' : 'text-[#5F6B78] hover:text-white'
                        }`}
                      >
                        <Star className={`w-3.5 h-3.5 ${inWatchlist ? 'fill-amber-400' : ''}`} />
                      </button>
                      <span className="w-6 h-6 rounded-md bg-[#0B0F14] border border-[#26313D] flex items-center justify-center text-[10px] font-bold">
                        {t.pair.split('/')[0]}
                      </span>
                      <span>{t.pair}</span>
                    </td>
                    <td className="py-3 text-right font-bold text-white">
                      ${t.price >= 1 ? t.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : t.price.toFixed(4)}
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
                        {t.change24h?.toFixed(2) ?? '0.00'}%
                      </span>
                    </td>
                    <td className="py-3 text-right text-[#8D9AAA] hidden sm:table-cell">
                      ${t.high24h?.toLocaleString() ?? '0'}
                    </td>
                    <td className="py-3 text-right text-[#8D9AAA] hidden sm:table-cell">
                      ${t.low24h?.toLocaleString() ?? '0'}
                    </td>
                    <td className="py-3 text-right text-[#8D9AAA] hidden md:table-cell">
                      ${((t.volume24h ?? 0) * (t.price ?? 0) / 1000000).toFixed(1)}M
                    </td>
                    <td className="py-3 text-right pr-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleSelectPair(t);
                        }}
                        className="px-2.5 py-1 rounded-md bg-[#0B0F14] hover:bg-blue-600 hover:text-white border border-[#26313D] text-[#8D9AAA] text-[10px] font-bold font-sans transition-colors cursor-pointer"
                      >
                        Select
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {filteredTickers.length === 0 && (
          <div className="text-center py-8 text-[#8D9AAA] text-sm">
            {onlyWatchlist ? 'No pairs in your watchlist.' : 'No pairs found matching your search.'}
          </div>
        )}
      </div>
    </div>
  );
};

export default MarketView;
