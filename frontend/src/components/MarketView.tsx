import React, { useState } from 'react';
import { TrendingUp, ArrowUpRight, ArrowDownRight, Search, BarChart3, SlidersHorizontal, Activity, Star } from 'lucide-react';
import { TickerInfo } from '../types';

interface MarketViewProps {
  tickers: TickerInfo[];
  watchlist?: string[];
  onToggleWatchlist?: (pair: string) => void;
  onSelectPair?: (pair: string) => void;
}

export const MarketView: React.FC<MarketViewProps> = ({
  tickers,
  watchlist = [],
  onToggleWatchlist,
  onSelectPair,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTicker, setSelectedTicker] = useState<TickerInfo>(tickers[0]);
  const [activeTab, setActiveTab] = useState<'1h' | '4h' | '1d'>('1h');
  const [onlyWatchlist, setOnlyWatchlist] = useState(false);

  const filteredTickers = tickers.filter((t) => {
    const matchSearch =
      t.pair.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.name.toLowerCase().includes(searchTerm.toLowerCase());
    if (!matchSearch) return false;
    if (onlyWatchlist) return watchlist.includes(t.pair);
    return true;
  });

  const isSelectedWatchlisted = watchlist.includes(selectedTicker?.pair || '');

  return (
    <div id="market-view" className="space-y-4 sm:space-y-6 pb-12">
      {/* Top Header */}
      <div className="p-4 sm:p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-white tracking-wide flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-400" />
            Live Market Tickers & Technical Indicators
          </h2>
          <p className="text-xs text-[#8D9AAA]">
            Direct public feed from Kraken Exchange with sub-second order book depth analysis.
          </p>
        </div>

        {/* Search & Watchlist Filter */}
        <div className="flex items-center gap-2 w-full md:w-auto">
          {/* Watchlist toggle filter pill */}
          <button
            onClick={() => setOnlyWatchlist(!onlyWatchlist)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer shrink-0 ${
              onlyWatchlist
                ? 'bg-amber-500 text-black font-bold shadow-md shadow-amber-500/20'
                : 'bg-[#0B0F14] text-[#8D9AAA] hover:text-white border border-[#26313D]'
            }`}
          >
            <Star className={`w-3.5 h-3.5 ${onlyWatchlist ? 'fill-black' : ''}`} />
            <span>Watchlist ({watchlist.length})</span>
          </button>

          {/* Search Field */}
          <div className="relative flex-1 md:w-60">
            <Search className="w-4 h-4 text-[#5F6B78] absolute left-3 top-2.5" />
            <input
              id="market-search-input"
              type="text"
              placeholder="Search pair..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Selected Pair Chart & Indicator Spotlight */}
      {selectedTicker && (
        <div className="p-4 sm:p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-xl">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#26313D]/70">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-center font-bold text-white text-sm shrink-0">
                {selectedTicker.pair.split('/')[0]}
              </div>
              <div>
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-lg sm:text-xl font-black text-white font-mono">{selectedTicker.pair}</span>
                  <span
                    className={`text-xs font-mono font-bold px-2 py-0.5 rounded ${
                      selectedTicker.change24h >= 0
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                    }`}
                  >
                    {selectedTicker.change24h >= 0 ? '+' : ''}
                    {selectedTicker.change24h.toFixed(2)}%
                  </span>

                  {/* Watchlist toggle in spotlight */}
                  {onToggleWatchlist && (
                    <button
                      onClick={() => onToggleWatchlist(selectedTicker.pair)}
                      title={isSelectedWatchlisted ? 'Remove from Watchlist' : 'Add to Watchlist'}
                      className={`p-1.5 rounded-lg border transition-all cursor-pointer ${
                        isSelectedWatchlisted
                          ? 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                          : 'bg-[#0B0F14] text-[#8D9AAA] hover:text-white border-[#26313D]'
                      }`}
                    >
                      <Star className={`w-3.5 h-3.5 ${isSelectedWatchlisted ? 'fill-amber-400' : ''}`} />
                    </button>
                  )}
                </div>
                <span className="text-xs text-[#8D9AAA]">{selectedTicker.name} · Kraken Live Stream</span>
              </div>
            </div>

            {/* Timeframe selector */}
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

          {/* Simulated Candlestick / Area Chart */}
          <div className="h-48 sm:h-56 w-full bg-[#0B0F14] rounded-xl border border-[#26313D]/80 p-3 sm:p-4 flex flex-col justify-between relative overflow-hidden">
            {/* Background Grid Lines */}
            <div className="absolute inset-0 grid grid-rows-4 grid-cols-6 pointer-events-none opacity-10">
              {Array.from({ length: 24 }).map((_, i) => (
                <div key={i} className="border-b border-r border-white/20" />
              ))}
            </div>

            <div className="flex items-center justify-between text-xs text-[#8D9AAA] font-mono z-10">
              <span>High: ${selectedTicker.high24h.toLocaleString()}</span>
              <span>Low: ${selectedTicker.low24h.toLocaleString()}</span>
            </div>

            {/* Simulated Line / Bar SVG Visualization */}
            <div className="h-28 sm:h-32 w-full flex items-end gap-2 sm:gap-3 px-1 sm:px-2 z-10">
              {selectedTicker.history.map((val, idx) => {
                const min = Math.min(...selectedTicker.history) * 0.998;
                const max = Math.max(...selectedTicker.history) * 1.002;
                const heightPct = Math.max(15, Math.min(95, ((val - min) / (max - min)) * 100));
                const isGreen = idx > 0 && val >= selectedTicker.history[idx - 1];

                return (
                  <div key={idx} className="flex-1 flex flex-col items-center gap-1 group relative">
                    {/* Tooltip */}
                    <div className="absolute -top-8 bg-[#1A2530] border border-[#26313D] text-white text-[10px] font-mono px-1.5 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-20">
                      ${val.toLocaleString()}
                    </div>
                    <div
                      className={`w-full rounded-t-md transition-all duration-300 ${
                        isGreen ? 'bg-emerald-500/80 hover:bg-emerald-400' : 'bg-blue-500/80 hover:bg-blue-400'
                      }`}
                      style={{ height: `${heightPct}%` }}
                    />
                    <span className="text-[8px] sm:text-[9px] text-[#5F6B78] font-mono">T-{selectedTicker.history.length - idx}</span>
                  </div>
                );
              })}
            </div>

            <div className="flex items-center justify-between text-[10px] sm:text-[11px] text-[#5F6B78] font-mono z-10 pt-2 border-t border-[#26313D]/40">
              <span>Current Price: <strong className="text-white">${selectedTicker.price.toLocaleString()}</strong></span>
              <span className="hidden sm:inline">24h Volume: <strong className="text-white">${(selectedTicker.volume24h * selectedTicker.price / 1000000).toFixed(2)}M</strong></span>
            </div>
          </div>

          {/* Indicators Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-3 pt-1">
            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <span className="text-[10px] text-[#8D9AAA] font-semibold uppercase">RSI (14)</span>
              <div className="text-sm sm:text-base font-bold text-white font-mono mt-0.5">{selectedTicker.rsi.toFixed(1)}</div>
              <span className="text-[10px] text-emerald-400 font-bold">
                {selectedTicker.rsi > 70 ? 'Overbought' : selectedTicker.rsi < 30 ? 'Oversold' : 'Momentum Bullish'}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <span className="text-[10px] text-[#8D9AAA] font-semibold uppercase">MACD Histogram</span>
              <div className="text-sm sm:text-base font-bold text-white font-mono mt-0.5">+{selectedTicker.macd.toFixed(2)}</div>
              <span className="text-[10px] text-emerald-400 font-bold">Positive Expansion</span>
            </div>
            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <span className="text-[10px] text-[#8D9AAA] font-semibold uppercase">ATR Volatility (14)</span>
              <div className="text-sm sm:text-base font-bold text-white font-mono mt-0.5">
                ${selectedTicker.atr >= 1 ? selectedTicker.atr.toFixed(2) : selectedTicker.atr.toFixed(4)}
              </div>
              <span className="text-[10px] text-blue-400 font-bold">SL Buffer ±1.5x</span>
            </div>
            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <span className="text-[10px] text-[#8D9AAA] font-semibold uppercase">Overall Trend</span>
              <div className="text-sm sm:text-base font-bold text-emerald-400 font-mono mt-0.5">{selectedTicker.trend}</div>
              <span className="text-[10px] text-[#8D9AAA] font-bold">5/5 MTF Aligned</span>
            </div>
          </div>
        </div>
      )}

      {/* Full Pairs Table Grid */}
      <div className="p-4 sm:p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70 mb-3">
          <h3 className="text-xs sm:text-sm font-bold text-white tracking-wider uppercase">
            Available Markets ({filteredTickers.length})
          </h3>
          {onlyWatchlist && (
            <span className="text-[11px] text-amber-400 font-mono font-bold">Filtered to Watchlist</span>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="text-[#5F6B78] border-b border-[#26313D] text-[11px]">
                <th className="pb-3 pl-2">PAIR</th>
                <th className="pb-3 text-right">PRICE (USD)</th>
                <th className="pb-3 text-right">24H CHANGE</th>
                <th className="pb-3 text-right hidden sm:table-cell">24H HIGH</th>
                <th className="pb-3 text-right hidden sm:table-cell">24H LOW</th>
                <th className="pb-3 text-right hidden md:table-cell">24H VOLUME</th>
                <th className="pb-3 text-right pr-2">ACTION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#26313D]/40">
              {filteredTickers.map((t) => {
                const isPositive = t.change24h >= 0;
                const isSelected = selectedTicker?.pair === t.pair;
                const inWatchlist = watchlist.includes(t.pair);

                return (
                  <tr
                    key={t.pair}
                    onClick={() => setSelectedTicker(t)}
                    className={`hover:bg-[#1A2530] transition-colors cursor-pointer ${
                      isSelected ? 'bg-[#1A2530]/80' : ''
                    }`}
                  >
                    <td className="py-3 pl-2 font-bold text-white font-sans flex items-center gap-2">
                      {onToggleWatchlist && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onToggleWatchlist(t.pair);
                          }}
                          className={`p-1 rounded cursor-pointer ${
                            inWatchlist ? 'text-amber-400' : 'text-[#5F6B78] hover:text-white'
                          }`}
                        >
                          <Star className={`w-3.5 h-3.5 ${inWatchlist ? 'fill-amber-400' : ''}`} />
                        </button>
                      )}
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
                        {t.change24h.toFixed(2)}%
                      </span>
                    </td>
                    <td className="py-3 text-right text-[#8D9AAA] hidden sm:table-cell">
                      ${t.high24h.toLocaleString()}
                    </td>
                    <td className="py-3 text-right text-[#8D9AAA] hidden sm:table-cell">
                      ${t.low24h.toLocaleString()}
                    </td>
                    <td className="py-3 text-right text-[#8D9AAA] hidden md:table-cell">
                      ${(t.volume24h * t.price / 1000000).toFixed(1)}M
                    </td>
                    <td className="py-3 text-right pr-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedTicker(t);
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
      </div>
    </div>
  );
};
