import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { 
  Zap, 
  ShieldCheck, 
  DollarSign, 
  TrendingUp, 
  AlertCircle,
  Wifi,
  WifiOff,
  Loader2,
  CheckCircle2,
  XCircle,
  Clock,
  BarChart3,
  RefreshCw,
  Activity,
  Cpu,
  HardDrive,
  Server,
  Radio,
  Signal,
  Gauge,
  Brain,
  Sparkles,
  Target,
  Compass,
  Sliders,
  Power
} from 'lucide-react';
import { TradingPosition } from '../types';
import { useWebSocketStatus, useWebSocketChannel } from '../contexts/WebSocketContext';
import { inksideAPI } from '../api/inkside';

// ============================================================
// TYPES
// ============================================================

interface TradingControlViewProps {
  engineRunning: boolean;
  onToggleEngine: () => void;
  positions: TradingPosition[];
  onClosePosition: (id: string) => void;
  wsConnected?: boolean;
  lastUpdate?: Date;
}

interface EngineStatus {
  running: boolean;
  mode: 'PAPER' | 'LIVE' | 'SIMULATION';
  state: 'IDLE' | 'RUNNING' | 'PAUSED' | 'ERROR';
  uptime: number;
  active_signals: number;
  open_positions: number;
  total_trades: number;
  win_rate: number;
  total_pnl: number;
  risk_level: string;
  health_score: number;
  last_heartbeat: string;
}

interface ExecutionMode {
  autoTrading: boolean;
  paperTrading: boolean;
  riskPercent: number;
  maxPositions: number;
  stopLossPercent: number;
  takeProfitPercent: number;
}

// ============================================================
// LOCALSTORAGE KEYS
// ============================================================

const ENGINE_STATE_KEY = 'inkside_engine_state';
const EXECUTION_MODE_KEY = 'inkside_execution_mode';

// ============================================================
// MAIN COMPONENT
// ============================================================

export const TradingControlView: React.FC<TradingControlViewProps> = ({
  engineRunning: propEngineRunning,
  onToggleEngine,
  positions,
  onClosePosition,
  wsConnected = false,
  lastUpdate,
}) => {
  // ============================================================
  // STATE - Engine Status (Load from localStorage)
  // ============================================================

  const [engineStatus, setEngineStatus] = useState<EngineStatus>(() => {
    const saved = localStorage.getItem(ENGINE_STATE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        return {
          running: parsed.running || false,
          mode: parsed.mode || 'PAPER',
          state: parsed.running ? 'RUNNING' : 'IDLE',
          uptime: parsed.uptime || 0,
          active_signals: parsed.active_signals || 0,
          open_positions: parsed.open_positions || 0,
          total_trades: parsed.total_trades || 0,
          win_rate: parsed.win_rate || 0,
          total_pnl: parsed.total_pnl || 0,
          risk_level: parsed.risk_level || 'LOW',
          health_score: parsed.health_score || 100,
          last_heartbeat: parsed.last_heartbeat || new Date().toISOString(),
        };
      } catch (e) {
        console.error('Failed to load engine state:', e);
      }
    }
    return {
      running: true, // ✅ ALWAYS TRUE
      mode: 'PAPER',
      state: 'RUNNING',
      uptime: 0,
      active_signals: 0,
      open_positions: 0,
      total_trades: 0,
      win_rate: 0,
      total_pnl: 0,
      risk_level: 'LOW',
      health_score: 100,
      last_heartbeat: new Date().toISOString(),
    };
  });

  const [executionMode, setExecutionMode] = useState<ExecutionMode>(() => {
    const saved = localStorage.getItem(EXECUTION_MODE_KEY);
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.error('Failed to load execution mode:', e);
      }
    }
    return {
      autoTrading: false,
      paperTrading: true,
      riskPercent: 1.5,
      maxPositions: 5,
      stopLossPercent: 2.0,
      takeProfitPercent: 4.0,
    };
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [tradeHistory, setTradeHistory] = useState<any[]>([]);
  const [engineLogs, setEngineLogs] = useState<string[]>(() => {
    // Initial log
    return [`[${new Date().toLocaleTimeString()}] 🚀 Engine is running and ready`];
  });

  // ============================================================
  // WEBSOCKET - REAL-TIME ENGINE STATUS
  // ============================================================

  const { isConnected, status } = useWebSocketStatus();

  useWebSocketChannel('engine', (data) => {
    if (data?.type === 'engine_status') {
      const newStatus = {
        ...engineStatus,
        ...data.payload,
        running: true, // ✅ ALWAYS TRUE
        state: 'RUNNING',
        last_heartbeat: new Date().toISOString(),
      };
      setEngineStatus(newStatus);
      
      localStorage.setItem(ENGINE_STATE_KEY, JSON.stringify({
        running: true,
        mode: newStatus.mode || 'PAPER',
        uptime: newStatus.uptime || 0,
        active_signals: newStatus.active_signals || 0,
        open_positions: newStatus.open_positions || 0,
        total_trades: newStatus.total_trades || 0,
        win_rate: newStatus.win_rate || 0,
        total_pnl: newStatus.total_pnl || 0,
        risk_level: newStatus.risk_level || 'LOW',
        health_score: newStatus.health_score || 100,
        last_heartbeat: newStatus.last_heartbeat,
      }));
    }
    if (data?.type === 'engine_log') {
      setEngineLogs(prev => [data.payload, ...prev].slice(0, 50));
    }
    if (data?.type === 'trade_executed') {
      setTradeHistory(prev => [data.payload, ...prev].slice(0, 50));
    }
  });

  useWebSocketChannel('positions', (data) => {
    if (data?.type === 'position_update') {
      // Positions will be updated via props
    }
  });

  // ============================================================
  // FETCH ENGINE STATUS
  // ============================================================

  const fetchEngineStatus = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const statusData = await inksideAPI.getStatus();
      const perfData = await inksideAPI.getPerformance();
      
      if (statusData?.bot) {
        const newStatus = {
          running: true, // ✅ ALWAYS TRUE
          mode: statusData.bot.trading_mode === 'LIVE' ? 'LIVE' : 'PAPER',
          state: 'RUNNING',
          uptime: statusData.bot.uptime || 0,
          open_positions: positions.length || 0,
          total_trades: statusData.bot.performance?.total_trades || 0,
          win_rate: statusData.bot.performance?.win_rate || 0,
          total_pnl: statusData.bot.performance?.total_pnl || 0,
          risk_level: statusData.bot.risk_level || 'LOW',
          health_score: 95,
          active_signals: 0,
          last_heartbeat: new Date().toISOString(),
        };
        setEngineStatus(newStatus);
        
        localStorage.setItem(ENGINE_STATE_KEY, JSON.stringify({
          running: true,
          mode: newStatus.mode || 'PAPER',
          uptime: newStatus.uptime || 0,
          active_signals: newStatus.active_signals || 0,
          open_positions: newStatus.open_positions || 0,
          total_trades: newStatus.total_trades || 0,
          win_rate: newStatus.win_rate || 0,
          total_pnl: newStatus.total_pnl || 0,
          risk_level: newStatus.risk_level || 'LOW',
          health_score: newStatus.health_score || 100,
          last_heartbeat: newStatus.last_heartbeat,
        }));
      }
      
      if (perfData?.performance) {
        setEngineStatus(prev => ({
          ...prev,
          total_trades: perfData.performance.trades || 0,
          win_rate: perfData.performance.win_rate || 0,
          total_pnl: perfData.performance.total_pnl || 0,
        }));
      }
      
    } catch (err) {
      console.error('Failed to fetch engine status:', err);
      setError('Failed to fetch engine status');
    } finally {
      setIsLoading(false);
    }
  }, [positions]);

  // ============================================================
  // AUTO-LOAD ENGINE STATUS ON MOUNT
  // ============================================================

  useEffect(() => {
    // ✅ ALWAYS RUNNING
    setEngineStatus(prev => ({
      ...prev,
      running: true,
      state: 'RUNNING',
    }));
    
    // Load saved state dari localStorage
    const savedState = localStorage.getItem(ENGINE_STATE_KEY);
    if (savedState) {
      try {
        const parsed = JSON.parse(savedState);
        setEngineStatus(prev => ({
          ...prev,
          running: true,
          state: 'RUNNING',
          mode: parsed.mode || 'PAPER',
          uptime: parsed.uptime || 0,
          active_signals: parsed.active_signals || 0,
          open_positions: parsed.open_positions || 0,
          total_trades: parsed.total_trades || 0,
          win_rate: parsed.win_rate || 0,
          total_pnl: parsed.total_pnl || 0,
          risk_level: parsed.risk_level || 'LOW',
          health_score: parsed.health_score || 100,
          last_heartbeat: parsed.last_heartbeat || new Date().toISOString(),
        }));
      } catch (e) {
        console.error('Failed to load engine state:', e);
      }
    }
    
    fetchEngineStatus();
    
    // Auto-refresh every 5 seconds
    const interval = setInterval(fetchEngineStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  // ============================================================
  // HANDLERS - ❌ TOMBOL START/STOP DIHAPUS
  // ============================================================

  // ❌ handleToggleEngine DIHAPUS - engine selalu running
  // Fungsi ini TIDAK ADA lagi

  // ============================================================
  // HANDLERS - Execution Mode
  // ============================================================

  const handleAutoTradingToggle = useCallback(() => {
    const newValue = !executionMode.autoTrading;
    const updated = { ...executionMode, autoTrading: newValue };
    setExecutionMode(updated);
    localStorage.setItem(EXECUTION_MODE_KEY, JSON.stringify(updated));
    setEngineLogs(prev => [
      `[${new Date().toLocaleTimeString()}] ${newValue ? '🔄' : '⏸️'} Auto-trading ${newValue ? 'enabled' : 'disabled'}`,
      ...prev
    ]);
  }, [executionMode]);

  const handlePaperTradingToggle = useCallback(() => {
    const newValue = !executionMode.paperTrading;
    const updated = { ...executionMode, paperTrading: newValue };
    setExecutionMode(updated);
    localStorage.setItem(EXECUTION_MODE_KEY, JSON.stringify(updated));
    setEngineStatus(prev => ({
      ...prev,
      mode: newValue ? 'PAPER' : 'LIVE',
    }));
    setEngineLogs(prev => [
      `[${new Date().toLocaleTimeString()}] 📝 Paper trading ${newValue ? 'enabled' : 'disabled'}`,
      ...prev
    ]);
  }, [executionMode]);

  const handleRiskChange = useCallback((value: number) => {
    const updated = { ...executionMode, riskPercent: value };
    setExecutionMode(updated);
    localStorage.setItem(EXECUTION_MODE_KEY, JSON.stringify(updated));
    setEngineLogs(prev => [
      `[${new Date().toLocaleTimeString()}] 📊 Risk per trade set to ${value}%`,
      ...prev
    ]);
  }, [executionMode]);

  // ============================================================
  // COMPUTED VALUES
  // ============================================================

  const totalPnlUsd = useMemo(() => {
    return positions.reduce((acc, p) => acc + (p.pnlUsd || 0), 0);
  }, [positions]);

  const winningPositions = useMemo(() => {
    return positions.filter(p => (p.pnlUsd || 0) > 0);
  }, [positions]);

  const winningRate = useMemo(() => {
    if (positions.length === 0) return engineStatus.win_rate || 0;
    return (winningPositions.length / positions.length) * 100;
  }, [positions, winningPositions, engineStatus.win_rate]);

  // ============================================================
  // RENDER HELPERS
  // ============================================================

  const StatusBadge = ({ status }: { status: string }) => {
    const colors: Record<string, string> = {
      RUNNING: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30 animate-pulse',
      IDLE: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
      PAUSED: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
      ERROR: 'bg-rose-500/20 text-rose-400 border-rose-500/30',
    };
    return (
      <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${colors[status] || colors.IDLE}`}>
        {status}
      </span>
    );
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div id="trading-control-view" className="space-y-6 pb-12">
      {/* Top Header - Engine Status */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-xl flex items-center justify-center bg-emerald-600/20 border border-emerald-500/30 text-emerald-400`}>
              <Activity className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-lg font-bold text-white tracking-wide">
                  Trading Control & Execution Engine
                </h2>
                <StatusBadge status="RUNNING" />
              </div>
              <p className="text-xs text-[#8D9AAA] flex items-center gap-2">
                Mode: <span className={`font-bold text-emerald-400`}>
                  {engineStatus.mode}
                </span>
                {isConnected && <span className="text-emerald-400">● LIVE</span>}
                {engineStatus.uptime > 0 && (
                  <span className="text-[#5F6B78]">Uptime: {Math.floor(engineStatus.uptime / 60)}m {engineStatus.uptime % 60}s</span>
                )}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* ✅ STATUS INDICATOR - TANPA TOMBOL START/STOP */}
            <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-600/20 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
              ENGINE RUNNING
            </div>
            
            <button
              onClick={fetchEngineStatus}
              className="p-2 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors cursor-pointer"
              title="Refresh status"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
        
        {/* Status Messages */}
        {error && (
          <div className="mt-3 p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            {error}
          </div>
        )}
        {successMessage && (
          <div className="mt-3 p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" />
            {successMessage}
          </div>
        )}
      </div>

      {/* Quick Stats - REAL DATA */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <div className="p-3.5 sm:p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center gap-1.5">
            <Activity className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-[10px] uppercase font-bold text-[#8D9AAA]">Status</span>
          </div>
          <div className="text-lg sm:text-xl font-bold font-mono text-emerald-400 mt-1">
            RUNNING
          </div>
          <span className="text-[10px] text-[#5F6B78] mt-1 block font-mono">
            ACTIVE
          </span>
        </div>

        <div className="p-3.5 sm:p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center gap-1.5">
            <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-[10px] uppercase font-bold text-[#8D9AAA]">Win Rate</span>
          </div>
          <div className="text-lg sm:text-xl font-bold font-mono text-cyan-400 mt-1">
            {winningRate.toFixed(0)}%
          </div>
          <span className="text-[10px] text-[#5F6B78] mt-1 block font-mono">
            {engineStatus.total_trades} trades
          </span>
        </div>

        <div className="p-3.5 sm:p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center gap-1.5">
            <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-[10px] uppercase font-bold text-[#8D9AAA]">Total PnL</span>
          </div>
          <div className={`text-lg sm:text-xl font-bold font-mono mt-1 ${engineStatus.total_pnl >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            {engineStatus.total_pnl >= 0 ? '+' : ''}{engineStatus.total_pnl.toFixed(2)}
          </div>
          <span className="text-[10px] text-[#5F6B78] mt-1 block font-mono">
            {engineStatus.open_positions} open
          </span>
        </div>

        <div className="p-3.5 sm:p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
            <span className="text-[10px] uppercase font-bold text-[#8D9AAA]">Health</span>
          </div>
          <div className="text-lg sm:text-xl font-bold font-mono text-amber-400 mt-1">
            {engineStatus.health_score}%
          </div>
          <span className="text-[10px] text-[#5F6B78] mt-1 block font-mono">
            Risk: {engineStatus.risk_level}
          </span>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Controls Left (1 Col) */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
            <Sliders className="w-4 h-4" />
            Execution Mode Toggles
          </h3>

          <div className="space-y-3.5">
            {/* Auto Trading Switch */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
              <div>
                <div className="text-xs font-bold text-white flex items-center gap-1.5">
                  {executionMode.autoTrading ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <XCircle className="w-3.5 h-3.5 text-[#5F6B78]" />
                  )}
                  Automated Trading
                </div>
                <div className="text-[10px] text-[#8D9AAA]">
                  {executionMode.autoTrading ? '✅ Auto-execution enabled' : '⏸️ Manual execution only'}
                </div>
              </div>
              <button
                onClick={handleAutoTradingToggle}
                className={`relative w-10 h-5 rounded-full transition-colors cursor-pointer ${
                  executionMode.autoTrading ? 'bg-blue-600' : 'bg-[#26313D]'
                }`}
              >
                <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all ${
                  executionMode.autoTrading ? 'left-5' : 'left-0.5'
                }`} />
              </button>
            </div>

            {/* Paper Trading Switch */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
              <div>
                <div className="text-xs font-bold text-white flex items-center gap-1.5">
                  {executionMode.paperTrading ? (
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
                  )}
                  Paper Trading (Safe Mode)
                </div>
                <div className="text-[10px] text-[#8D9AAA]">
                  {executionMode.paperTrading 
                    ? '✅ Zero capital risk simulation' 
                    : '⚠️ REAL capital at risk'}
                </div>
                {executionMode.paperTrading && (
                  <div className="text-[9px] text-emerald-400 mt-0.5">
                    Current balance: $10,000.00 (simulated)
                  </div>
                )}
              </div>
              <button
                onClick={handlePaperTradingToggle}
                className={`relative w-10 h-5 rounded-full transition-colors cursor-pointer ${
                  executionMode.paperTrading ? 'bg-emerald-600' : 'bg-[#26313D]'
                }`}
              >
                <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all ${
                  executionMode.paperTrading ? 'left-5' : 'left-0.5'
                }`} />
              </button>
            </div>

            {/* Risk Slider */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5">
                  <Gauge className="w-3.5 h-3.5 text-blue-400" />
                  <span className="font-bold text-white">Risk Per Trade:</span>
                </div>
                <span className="font-mono font-bold text-blue-400">{executionMode.riskPercent}%</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="5.0"
                step="0.5"
                value={executionMode.riskPercent}
                onChange={(e) => handleRiskChange(parseFloat(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-[#5F6B78]">
                <span>0.5% Conservative</span>
                <span>5.0% Aggressive</span>
              </div>
              <span className="text-[10px] text-[#5F6B78] block">
                Caps max position loss at {executionMode.riskPercent}% of equity
              </span>
            </div>

            {/* Additional Settings */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D]">
              <div className="flex items-center justify-between text-xs">
                <span className="text-[#8D9AAA]">Max Positions</span>
                <span className="font-bold text-white">{executionMode.maxPositions}</span>
              </div>
              <div className="flex items-center justify-between text-xs mt-1.5">
                <span className="text-[#8D9AAA]">Stop Loss</span>
                <span className="font-bold text-rose-400">{executionMode.stopLossPercent}%</span>
              </div>
              <div className="flex items-center justify-between text-xs mt-1.5">
                <span className="text-[#8D9AAA]">Take Profit</span>
                <span className="font-bold text-emerald-400">{executionMode.takeProfitPercent}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Positions & Logs Right (2 Cols) */}
        <div className="lg:col-span-2 space-y-4">
          {/* Positions */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                Active Open Positions ({positions.length})
              </h3>
              <div className={`text-xs font-mono font-bold ${totalPnlUsd >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                Total PnL: {totalPnlUsd >= 0 ? '+' : ''}{totalPnlUsd.toFixed(2)}
              </div>
            </div>

            <div className="space-y-3 mt-3 max-h-[300px] overflow-y-auto pr-1">
              {positions.length === 0 ? (
                <div className="py-8 text-center text-xs text-[#5F6B78]">
                  <div className="text-4xl mb-3">📭</div>
                  <p className="text-sm font-medium">No Open Positions</p>
                  <p className="text-xs">Scanner is searching for high-probability setups.</p>
                  <div className="flex justify-center gap-2 mt-3">
                    <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                    <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" style={{ animationDelay: '0.3s' }} />
                    <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" style={{ animationDelay: '0.6s' }} />
                  </div>
                </div>
              ) : (
                positions.map((pos) => {
                  const isProfitable = (pos.pnlUsd || 0) >= 0;
                  return (
                    <div
                      key={pos.id}
                      className={`p-4 rounded-xl bg-[#1A2530] border transition-all hover:border-blue-500/30 ${
                        isProfitable ? 'border-emerald-500/30' : 'border-rose-500/30'
                      } flex flex-col sm:flex-row sm:items-center justify-between gap-3`}
                    >
                      <div className="flex items-center gap-3">
                        <span className={`text-xs font-black px-2 py-1 rounded font-mono ${
                          pos.side === 'LONG' 
                            ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' 
                            : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                        }`}>
                          {pos.side}
                        </span>
                        <div>
                          <div className="text-sm font-bold text-white font-mono">{pos.pair}</div>
                          <div className="text-[10px] text-[#8D9AAA] font-mono">
                            Entry: ${pos.entryPrice?.toLocaleString() || '0'} · Amount: {pos.amount || 0}
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-5">
                        <div className="text-right font-mono">
                          <div className="text-xs font-bold text-white">
                            ${pos.currentPrice?.toLocaleString() || '0'}
                          </div>
                          <div className={`text-xs font-bold ${isProfitable ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {isProfitable ? '+' : ''}{pos.pnlUsd?.toFixed(2)} ({isProfitable ? '+' : ''}{pos.pnlPercent?.toFixed(2)}%)
                          </div>
                        </div>

                        <button
                          onClick={() => onClosePosition(pos.id)}
                          className="px-3 py-1.5 rounded-lg bg-rose-600/20 hover:bg-rose-600 border border-rose-500/40 text-rose-300 hover:text-white text-xs font-bold transition-all cursor-pointer"
                        >
                          Close
                        </button>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          {/* Engine Logs */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Server className="w-4 h-4 text-blue-400" />
                Engine Logs
              </h3>
              <span className="text-[10px] text-[#5F6B78] font-mono">
                {engineLogs.length} entries
              </span>
            </div>

            <div className="mt-3 max-h-[150px] overflow-y-auto pr-1 space-y-1 font-mono text-[10px]">
              {engineLogs.map((log, idx) => (
                <div key={idx} className="text-[#8D9AAA] border-b border-[#26313D]/20 pb-1">
                  {log}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TradingControlView;
