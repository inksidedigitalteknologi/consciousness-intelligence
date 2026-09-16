import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { 
  RefreshCw, Radio, Send, Activity, Brain, Menu, Star, 
  Wifi, WifiOff, AlertTriangle, Clock, Zap, Shield, Server, 
  ChevronDown, ChevronUp, Cpu, HardDrive, Database, TrendingUp,
  Power, PowerOff, Signal, Bell, Loader2, CheckCircle2, XCircle
} from 'lucide-react';
import { NavigationPage } from '../types';
import { useWebSocketStatus, useWebSocketChannel } from '../contexts/WebSocketContext';

// ============================================================
// TYPES
// ============================================================

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
  wsConnected?: boolean;
  wsStatus?: string;
  healthScore?: number;
  uptime?: number;
  systemMode?: 'PAPER' | 'LIVE' | 'SIMULATION';
  riskLevel?: string;
  engineState?: 'IDLE' | 'RUNNING' | 'PAUSED' | 'ERROR';
  isToggling?: boolean;
}

// ============================================================
// HELPER FUNCTIONS
// ============================================================

const formatUptime = (seconds: number): string => {
  if (!seconds || seconds < 0) return '--:--:--';
  const hrs = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
};

const getRiskColor = (risk: string): string => {
  const map: Record<string, string> = {
    'LOW': 'text-emerald-400',
    'MODERATE': 'text-amber-400',
    'HIGH': 'text-rose-400',
    'CRITICAL': 'text-red-500',
  };
  return map[risk] || 'text-gray-400';
};

const getRiskBadge = (risk: string): string => {
  const map: Record<string, string> = {
    'LOW': 'bg-emerald-500/20 border-emerald-500/30',
    'MODERATE': 'bg-amber-500/20 border-amber-500/30',
    'HIGH': 'bg-rose-500/20 border-rose-500/30',
    'CRITICAL': 'bg-red-500/20 border-red-500/30',
  };
  return map[risk] || 'bg-gray-500/20 border-gray-500/30';
};

// ============================================================
// TOPBAR COMPONENT
// ============================================================

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
  wsConnected = false,
  wsStatus = 'disconnected',
  healthScore = 100,
  uptime = 0,
  systemMode = 'PAPER',
  riskLevel = 'LOW',
  engineState = 'RUNNING',
  isToggling = false,
}) => {
  // ============================================================
  // STATE
  // ============================================================
  
  const [timeStr, setTimeStr] = useState('');
  const [dateStr, setDateStr] = useState('');
  const [showSystemMenu, setShowSystemMenu] = useState(false);
  const [isHovering, setIsHovering] = useState(false);

  // ============================================================
  // WEBSOCKET
  // ============================================================
  
  const { isConnected, status } = useWebSocketStatus();

  useWebSocketChannel('engine', (data) => {
    if (data?.type === 'engine_status') {
      // Status akan update otomatis via props dari parent
    }
  });

  // ============================================================
  // CLOCK UPDATES
  // ============================================================
  
  useEffect(() => {
    const updateDateTime = () => {
      const now = new Date();
      setTimeStr(now.toTimeString().split(' ')[0]);
      setDateStr(now.toLocaleDateString('id-ID', { 
        day: '2-digit', 
        month: 'short', 
        year: 'numeric' 
      }));
    };
    
    updateDateTime();
    const interval = setInterval(updateDateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // ============================================================
  // MEMOIZED VALUES
  // ============================================================
  
  const healthColor = useMemo(() => {
    if (healthScore >= 80) return 'text-emerald-400';
    if (healthScore >= 60) return 'text-amber-400';
    if (healthScore >= 40) return 'text-orange-400';
    return 'text-red-400';
  }, [healthScore]);

  const healthBarColor = useMemo(() => {
    if (healthScore >= 80) return 'bg-emerald-400';
    if (healthScore >= 60) return 'bg-amber-400';
    if (healthScore >= 40) return 'bg-orange-400';
    return 'bg-red-400';
  }, [healthScore]);

  const pageTitle = useMemo(() => {
    const titles: Record<NavigationPage, string> = {
      'Dashboard': '📊 Dashboard',
      'Watchlist': '👁️ Watchlist',
      'Brain': '🧠 Brain Core',
      'Reflection': '🪞 Reflection',
      'Market': '📈 Market',
      'Signals': '📡 Signals',
      'Learning': '🧬 Learning',
      'Memory': '💾 Memory',
      'Pattern': '🔍 Patterns',
      'Prediction': '🔮 Predictions',
      'Decision': '⚡ Decisions',
      'Knowledge': '📚 Knowledge',
      'Health': '🩺 Health',
      'Trading': '💹 Trading',
      'Telegram': '✈️ Telegram',
      'Diagnostics': '🔬 Diagnostics',
      'Settings': '⚙️ Settings'
    };
    return titles[currentPage] || currentPage;
  }, [currentPage]);

  // ============================================================
  // RENDER FUNCTIONS
  // ============================================================

  // ✅ TANPA TOMBOL START/STOP - ENGINE ALWAYS RUNNING
  const renderEngineButton = () => {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-600/20 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
        <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
        <span className="hidden sm:inline">ENGINE RUNNING</span>
        <span className="sm:hidden">RUN</span>
      </div>
    );
  };

  // ============================================================
  // RENDER
  // ============================================================
  
  return (
    <header
      id="app-topbar"
      className="h-14 sm:h-16 bg-gradient-to-r from-[#131A22] to-[#1A2530] border-b border-[#26313D] px-3 sm:px-6 flex items-center justify-between shrink-0 select-none z-10 gap-2 backdrop-blur-sm"
    >
      {/* LEFT: Mobile Menu & Page Title */}
      <div className="flex items-center gap-2 sm:gap-3 min-w-0">
        {onOpenSidebar && (
          <button
            onClick={onOpenSidebar}
            id="mobile-sidebar-toggle"
            className="lg:hidden p-2 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-all duration-200 cursor-pointer shrink-0 hover:scale-105"
            title="Open Menu"
          >
            <Menu className="w-4 h-4" />
          </button>
        )}

        <div className="flex items-center gap-2 min-w-0">
          <h1 className="text-sm sm:text-base md:text-lg font-bold text-white tracking-wide truncate">
            {pageTitle}
          </h1>
          
          <span className={`hidden sm:inline-block text-[10px] sm:text-xs px-2 py-0.5 rounded-full font-semibold shrink-0 transition-all duration-300 ${
            wsConnected 
              ? 'bg-emerald-500/20 border border-emerald-500/30 text-emerald-400 animate-pulse' 
              : 'bg-amber-500/20 border border-amber-500/30 text-amber-400'
          }`}>
            {wsConnected ? '● LIVE' : '○ RECONNECTING'}
          </span>

          <span className={`hidden md:inline-block text-[9px] px-1.5 py-0.5 rounded-full font-bold ${
            engineState === 'RUNNING' 
              ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 animate-pulse'
              : engineState === 'PAUSED'
              ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
              : engineState === 'ERROR'
              ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
              : 'bg-[#26313D] text-[#5F6B78]'
          }`}>
            {engineState}
          </span>
        </div>
      </div>

      {/* RIGHT: Controls & Status */}
      <div className="flex items-center gap-1.5 sm:gap-3 shrink-0">
        
        {/* HEALTH SCORE */}
        <div 
          className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] cursor-help"
          title={`Health Score: ${healthScore}%`}
        >
          <Shield className="w-3.5 h-3.5 text-blue-400" />
          <div className="w-16 h-1.5 bg-[#1A2530] rounded-full overflow-hidden">
            <div 
              className={`h-full rounded-full transition-all duration-500 ${healthBarColor}`}
              style={{ width: `${Math.min(100, Math.max(0, healthScore))}%` }}
            />
          </div>
          <span className={`text-xs font-bold ${healthColor}`}>
            {Math.round(healthScore)}%
          </span>
        </div>

        {/* UPTIME */}
        <div 
          className="hidden xl:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D]"
          title="System Uptime"
        >
          <Clock className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-xs font-mono text-white font-bold tracking-wider">
            {formatUptime(uptime)}
          </span>
        </div>

        {/* MODE INDICATOR */}
        <div 
          className={`hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border ${
            systemMode === 'LIVE' 
              ? 'bg-rose-500/10 border-rose-500/30 text-rose-400' 
              : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
          }`}
        >
          {systemMode === 'LIVE' ? (
            <Power className="w-3 h-3" />
          ) : (
            <PowerOff className="w-3 h-3" />
          )}
          <span className="text-[10px] font-bold uppercase tracking-wider">
            {systemMode}
          </span>
        </div>

        {/* RISK LEVEL */}
        <div className={`hidden 2xl:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border ${getRiskBadge(riskLevel)}`}>
          <AlertTriangle className={`w-3.5 h-3.5 ${getRiskColor(riskLevel)}`} />
          <span className={`text-[10px] font-bold uppercase tracking-wider ${getRiskColor(riskLevel)}`}>
            {riskLevel}
          </span>
        </div>

        {/* TELEGRAM STATUS */}
        <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D]">
          <Send className="w-3.5 h-3.5 text-sky-400" />
          <span className={`text-[10px] font-bold ${
            telegramConfigured ? 'text-emerald-400' : 'text-amber-400'
          }`}>
            {telegramConfigured ? 'TG ●' : 'TG ○'}
          </span>
        </div>

        {/* WEBSOCKET STATUS */}
        <div 
          className="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] cursor-help"
          title={`WebSocket: ${wsStatus}`}
        >
          {wsConnected ? (
            <Wifi className="w-3.5 h-3.5 text-emerald-400" />
          ) : (
            <WifiOff className="w-3.5 h-3.5 text-rose-400" />
          )}
          <span className={`text-[10px] font-bold ${
            wsConnected ? 'text-emerald-400' : 'text-rose-400'
          }`}>
            {wsConnected ? 'WS' : 'WS↓'}
          </span>
        </div>

        {/* WATCHLIST BUTTON */}
        {onNavigateWatchlist && (
          <button
            onClick={onNavigateWatchlist}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl border transition-all duration-200 cursor-pointer ${
              currentPage === 'Watchlist'
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                : 'bg-[#0B0F14] text-[#8D9AAA] hover:text-amber-400 border-[#26313D] hover:border-amber-500/30'
            }`}
            title="Open Watchlist"
          >
            <Star className={`w-3.5 h-3.5 ${watchlistCount > 0 ? 'fill-amber-400 text-amber-400' : ''}`} />
            <span className="text-xs font-bold font-mono hidden md:inline">
              {watchlistCount > 0 ? watchlistCount : ''}
            </span>
          </button>
        )}

        {/* ENGINE CONTROL - TANPA TOMBOL START/STOP */}
        <div className="flex items-center gap-1.5 sm:gap-2">
          {renderEngineButton()}

          {/* REFRESH BUTTON */}
          <button
            id="refresh-btn"
            onClick={onRefreshData}
            title="Refresh All Engine Data"
            disabled={isRefreshing}
            className="p-2 rounded-xl bg-[#18212B] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-all duration-200 cursor-pointer disabled:opacity-50 hover:scale-105"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin text-blue-400' : ''}`} />
          </button>
        </div>

        {/* CLOCK */}
        <div className="hidden sm:block pl-2.5 border-l border-[#26313D] text-right font-mono">
          <div className="text-xs font-bold text-white tracking-wider tabular-nums">
            {timeStr || '--:--:--'}
          </div>
          <div className="text-[9px] text-[#5F6B78] font-sans hidden xl:block">
            {dateStr || '--'}
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopBar;
