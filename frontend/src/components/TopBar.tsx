import React, { useState, useEffect } from 'react';
import { Play, Square, RefreshCw, Radio, Send, Activity, Brain, Menu, Star } from 'lucide-react';
import { NavigationPage } from '../types';

interface TopBarProps {
  currentPage: NavigationPage;
  engineRunning: boolean;
  onToggleEngine: () => void;
  telegramConfigured: boolean;
  onRefreshData: () => void;
  isRefreshing: boolean;
  onOpenSidebar?: () => void;
  onNavigateWatchlist?: () => void;
  watchlistCount?: number;
}

export const TopBar: React.FC<TopBarProps> = ({
  currentPage,
  engineRunning,
  onToggleEngine,
  telegramConfigured,
  onRefreshData,
  isRefreshing,
  onOpenSidebar,
  onNavigateWatchlist,
  watchlistCount = 0,
}) => {
  const [timeStr, setTimeStr] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toTimeString().split(' ')[0]);
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const getPageTitle = (page: NavigationPage): string => {
    const titles: Record<NavigationPage, string> = {
      'Dashboard': 'Dashboard Overview',
      'Watchlist': 'Market Watchlist',
      'Brain': 'Cognitive Brain Core',
      'Reflection': 'Cognitive Mirror Reflection',
      'Market': 'Live Market Tickers',
      'Signals': 'Signals Radar',
      'Learning': 'Learning Engine',
      'Memory': 'Memory Database',
      'Pattern': 'Pattern Detector',
      'Prediction': 'Predictions',
      'Decision': 'Decision Engine',
      'Knowledge': 'Knowledge Base',
      'Health': 'System Health',
      'Trading': 'Trading Execution',
      'Telegram': 'Telegram Bridge',
      'Diagnostics': 'Diagnostics Test',
      'Settings': 'Configuration'
    };
    return titles[page] || page;
  };

  return (
    <header
      id="app-topbar"
      className="h-14 sm:h-16 bg-[#131A22] border-b border-[#26313D] px-3 sm:px-6 flex items-center justify-between shrink-0 select-none z-10 gap-2"
    >
      {/* Left: Mobile Menu Hamburger & Page Title */}
      <div className="flex items-center gap-2 sm:gap-3 min-w-0">
        {onOpenSidebar && (
          <button
            onClick={onOpenSidebar}
            id="mobile-sidebar-toggle"
            className="lg:hidden p-2 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors cursor-pointer shrink-0"
            title="Open Menu"
          >
            <Menu className="w-4 h-4" />
          </button>
        )}

        <div className="flex items-center gap-2 min-w-0">
          <h1 className="text-sm sm:text-base md:text-lg font-bold text-white tracking-wide truncate">
            {getPageTitle(currentPage)}
          </h1>
          <span className="hidden sm:inline-block text-[10px] sm:text-xs px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 font-semibold shrink-0">
            LIVE
          </span>
        </div>
      </div>

      {/* Action Badges & Status */}
      <div className="flex items-center gap-1.5 sm:gap-3 shrink-0">
        {/* Watchlist Quick Access Button */}
        {onNavigateWatchlist && (
          <button
            onClick={onNavigateWatchlist}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl border transition-all cursor-pointer ${
              currentPage === 'Watchlist'
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                : 'bg-[#0F141B] text-[#8D9AAA] hover:text-amber-400 border-[#26313D]'
            }`}
            title="Open Watchlist"
          >
            <Star className={`w-3.5 h-3.5 ${watchlistCount > 0 ? 'fill-amber-400 text-amber-400' : ''}`} />
            <span className="text-xs font-bold font-mono hidden md:inline">{watchlistCount} Watchlist</span>
            <span className="text-xs font-bold font-mono md:hidden">{watchlistCount}</span>
          </button>
        )}

        {/* Kraken Exchange Status */}
        <div className="hidden xl:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#0F141B] border border-[#26313D]">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs font-bold text-[#E8EDF2] tracking-wider">KRAKEN</span>
          <span className="text-[10px] text-emerald-400 font-semibold">ONLINE</span>
        </div>

        {/* Telegram Status */}
        <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#0F141B] border border-[#26313D]">
          <Send className="w-3.5 h-3.5 text-sky-400" />
          <span className="text-xs font-semibold text-[#8D9AAA]">TG</span>
          <span className={`text-[10px] font-bold ${telegramConfigured ? 'text-emerald-400' : 'text-amber-400'}`}>
            {telegramConfigured ? 'ACTIVE' : 'READY'}
          </span>
        </div>

        {/* Engine Toggle Buttons */}
        <div className="flex items-center gap-1.5 sm:gap-2">
          {engineRunning ? (
            <button
              id="stop-engine-btn"
              onClick={onToggleEngine}
              className="flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-xl bg-rose-600/20 hover:bg-rose-600 border border-rose-500/40 text-rose-300 hover:text-white text-xs font-bold transition-all shadow-sm cursor-pointer"
            >
              <Square className="w-3.5 h-3.5 fill-current shrink-0" />
              <span className="hidden sm:inline">STOP</span>
            </button>
          ) : (
            <button
              id="start-engine-btn"
              onClick={onToggleEngine}
              className="flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 border border-emerald-400/40 text-white text-xs font-bold transition-all shadow-md shadow-emerald-600/30 cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-current shrink-0" />
              <span className="hidden sm:inline">START</span>
            </button>
          )}

          {/* Refresh Action */}
          <button
            id="refresh-btn"
            onClick={onRefreshData}
            title="Refresh All Engine Data"
            disabled={isRefreshing}
            className="p-2 rounded-xl bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin text-blue-400' : ''}`} />
          </button>
        </div>

        {/* Live Clock */}
        <div className="hidden sm:block pl-2.5 border-l border-[#26313D] text-right font-mono">
          <div className="text-xs font-bold text-white tracking-wider">{timeStr || '00:00:00'}</div>
          <div className="text-[9px] text-[#5F6B78] font-sans hidden md:block">UTC+7 JAKARTA</div>
        </div>
      </div>
    </header>
  );
};

export default TopBar;
