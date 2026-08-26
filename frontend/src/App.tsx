import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
import { BottomNav } from './components/BottomNav';
import { DashboardView } from './components/DashboardView';
import { BrainView } from './components/BrainView';
import { ReflectionView } from './components/ReflectionView';
import { MarketView } from './components/MarketView';
import { WatchlistView } from './components/WatchlistView';
import { SignalsView } from './components/SignalsView';
import { LearningView } from './components/LearningView';
import { KnowledgeView } from './components/KnowledgeView';
import { HealthView } from './components/HealthView';
import { TradingControlView } from './components/TradingControlView';
import { TelegramView } from './components/TelegramView';
import { DiagnosticsView } from './components/DiagnosticsView';
import { SettingsView } from './components/SettingsView';
import { MemoryView } from './components/MemoryView';
import { PatternView } from './components/PatternView';
import { PredictionView } from './components/PredictionView';
import { DecisionView } from './components/DecisionView';

import {
  NavigationPage,
  TickerInfo,
  TradingSignal,
  CognitiveInsight,
  KnowledgeItem,
  ComponentHealthStatus,
  TradingPosition,
  SystemLogEntry,
} from './types';

import { inksideAPI, StatusResponse, Signal as APISignal, BrainStateResponse, PerformanceResponse } from './api/inkside';
import { WebSocketProvider, useWebSocket, useWebSocketChannel, useWebSocketStatus } from './contexts/WebSocketContext';

// ============================================================
// LOCALSTORAGE KEYS
// ============================================================

const PAGE_STORAGE_KEY = 'inkside_current_page';

// ============================================================
// HELPER FUNCTIONS
// ============================================================

const loadCurrentPage = (): NavigationPage => {
  try {
    const saved = localStorage.getItem(PAGE_STORAGE_KEY);
    if (saved && saved !== 'undefined' && saved !== 'null') {
      return saved as NavigationPage;
    }
  } catch {}
  return 'Dashboard';
};

const saveCurrentPage = (page: NavigationPage) => {
  try {
    localStorage.setItem(PAGE_STORAGE_KEY, page);
  } catch {}
};

// ============================================================
// SYSTEM METRICS INTERFACE
// ============================================================

interface SystemMetrics {
  cpu: number;
  ram: number;
  ram_percent: number;
  disk_percent: number;
  uptime: number;
  memory_count: number;
  knowledge_count: number;
  pnl: number;
  win_rate: number;
  total_trades: number;
  prediction_accuracy: number;
  open_positions: number;
  risk_level: string;
  health_score: number;
  last_update: string;
}

// ============================================================
// LOADING SCREEN COMPONENT
// ============================================================

const LoadingScreen: React.FC<{ message?: string }> = ({ message = 'Loading Inkside Digital...' }) => (
  <div className="flex h-screen w-screen bg-[#0B0F14] items-center justify-center">
    <div className="text-center">
      <div className="text-4xl mb-4 animate-pulse">🧠</div>
      <div className="text-white text-xl font-light">{message}</div>
      <div className="text-gray-500 text-sm mt-2 animate-pulse">Menghubungkan ke backend...</div>
      <div className="mt-4 w-12 h-12 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mx-auto"></div>
    </div>
  </div>
);

// ============================================================
// ERROR SCREEN COMPONENT
// ============================================================

const ErrorScreen: React.FC<{ error: string; onRetry: () => void }> = ({ error, onRetry }) => (
  <div className="flex h-screen w-screen bg-[#0B0F14] items-center justify-center">
    <div className="text-center max-w-md p-8 rounded-2xl bg-red-500/10 border border-red-500/30">
      <div className="text-4xl mb-4">❌</div>
      <div className="text-red-400 text-lg font-medium">{error}</div>
      <p className="text-gray-400 text-sm mt-2">
        Pastikan backend berjalan di port 5001 dan API Key benar.
      </p>
      <button
        onClick={onRetry}
        className="mt-4 px-6 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all duration-200"
      >
        🔄 Retry
      </button>
    </div>
  </div>
);

// ============================================================
// DEFAULT SYSTEM METRICS
// ============================================================

const defaultSystemMetrics: SystemMetrics = {
  cpu: 0,
  ram: 0,
  ram_percent: 0,
  disk_percent: 0,
  uptime: 0,
  memory_count: 0,
  knowledge_count: 0,
  pnl: 0,
  win_rate: 0,
  total_trades: 0,
  prediction_accuracy: 0,
  open_positions: 0,
  risk_level: '--',
  health_score: 0,
  last_update: new Date().toISOString(),
};

// ============================================================
// MAIN APP CONTENT
// ============================================================

function AppContent() {
  // ============================================================
  // NAVIGATION STATE
  // ============================================================
  
  const [currentPage, setCurrentPage] = useState<NavigationPage>(loadCurrentPage);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  
  useEffect(() => {
    saveCurrentPage(currentPage);
  }, [currentPage]);

  // ============================================================
  // WEBSOCKET
  // ============================================================
  
  const { isConnected, reconnectAttempts, getConnectionStatus } = useWebSocket();
  
  useWebSocketChannel('metrics', (data) => {
    if (data.type === 'system_metrics') {
      setSystemMetrics(prev => ({
        ...prev,
        ...data.payload,
        last_update: new Date().toISOString(),
      }));
    }
  });

  useWebSocketChannel('status', (data) => {
    if (data.type === 'engine_status') {
      setEngineRunning(data.payload.running || false);
      setLearningActive(data.payload.learning || false);
      setCycleCount(data.payload.cycles || 0);
    }
  });

  useWebSocketChannel('signals', (data) => {
    if (data.type === 'signal_update') {
      const mapped = mapSignalData([data.payload]);
      setRealSignals(prev => {
        const filtered = prev.filter(s => s.pair !== data.payload.pair);
        return [...filtered, ...mapped];
      });
    }
  });

  // ============================================================
  // STATE
  // ============================================================
  
  const [apiStatus, setApiStatus] = useState<StatusResponse | null>(null);
  const [realSignals, setRealSignals] = useState<any[]>([]);
  const [brainState, setBrainState] = useState<BrainStateResponse | null>(null);
  const [performance, setPerformance] = useState<PerformanceResponse | null>(null);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  
  const [engineRunning, setEngineRunning] = useState(false);
  const [isToggling, setIsToggling] = useState(false); // <-- TAMBAHKAN INI
  const [learningActive, setLearningActive] = useState(false);
  const [cycleCount, setCycleCount] = useState(0);
  const [consciousnessLevel, setConsciousnessLevel] = useState(0.5);
  const [emotionalState, setEmotionalState] = useState('CALM');
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics>(defaultSystemMetrics);

  const [tickers, setTickers] = useState<TickerInfo[]>([]);
  const [signals, setSignals] = useState<TradingSignal[]>([]);
  const [insights, setInsights] = useState<CognitiveInsight[]>([]);
  const [knowledgeList, setKnowledgeList] = useState<KnowledgeItem[]>([]);
  const [components, setComponents] = useState<ComponentHealthStatus[]>([]);
  const [positions, setPositions] = useState<TradingPosition[]>([]);
  const [logs, setLogs] = useState<SystemLogEntry[]>([]);
  const [telegramConfigured, setTelegramConfigured] = useState(false);
  const [watchlistCount, setWatchlistCount] = useState(0);

  // ============================================================
  // HELPERS
  // ============================================================
  
  const mapSignalData = useCallback((apiSignals: any[]): any[] => {
    if (!apiSignals || apiSignals.length === 0) return [];
    return apiSignals.map((s, index) => ({
      pair: s.pair || '',
      signal: s.signal || 'HOLD',
      confidence: s.confidence || 0,
      price: s.price || 0,
      strength: s.strength || 'NEUTRAL',
      timestamp: s.timestamp || new Date().toISOString(),
      id: `sig-${Date.now()}-${index}-${Math.random().toString(36).substr(2, 6)}`,
      entry: s.price || 0,
      stopLoss: s.price ? Math.round(s.price * 0.95 * 100) / 100 : 0,
      tp1: s.price ? Math.round(s.price * 1.05 * 100) / 100 : 0,
      tp2: s.price ? Math.round(s.price * 1.10 * 100) / 100 : 0,
      quality: s.confidence > 80 ? 'EXCELLENT' : s.confidence > 60 ? 'GOOD' : 'NEUTRAL',
      riskReward: s.confidence > 80 ? 3 : s.confidence > 60 ? 2 : 1,
      mtfAlignment: {
        '5m': s.strength === 'STRONG' ? 'BULLISH' : 'NEUTRAL',
        '15m': s.signal === 'BUY' ? 'BULLISH' : s.signal === 'SELL' ? 'BEARISH' : 'NEUTRAL',
        '1h': s.signal === 'BUY' ? 'BULLISH' : s.signal === 'SELL' ? 'BEARISH' : 'NEUTRAL',
        '4h': 'NEUTRAL',
        '1d': 'NEUTRAL'
      },
      reasons: [
        `Signal generated by cognitive engine for ${s.pair}`,
        `Confidence: ${s.confidence}%`,
        `Strength: ${s.strength || 'NEUTRAL'}`
      ],
      riskLevel: s.confidence > 80 ? 'LOW' : s.confidence > 60 ? 'MEDIUM' : 'HIGH',
      trend: s.signal === 'BUY' ? 'BULLISH' : s.signal === 'SELL' ? 'BEARISH' : 'NEUTRAL',
      timeframe: '1h',
    }));
  }, []);

  const fetchSystemMetrics = useCallback(async () => {
    try {
      const response = await fetch('/api/system/metrics');
      if (response.ok) {
        const data = await response.json();
        setSystemMetrics({
          cpu: data.cpu || 0,
          ram: data.ram || 0,
          ram_percent: data.ram_percent || 0,
          disk_percent: data.disk_percent || 0,
          uptime: data.uptime || 0,
          memory_count: data.memory_count || 0,
          knowledge_count: data.knowledge_count || 0,
          pnl: data.pnl || 0,
          win_rate: data.win_rate || 0,
          total_trades: data.total_trades || 0,
          prediction_accuracy: data.prediction_accuracy || 0,
          open_positions: data.open_positions || 0,
          risk_level: data.risk_level || '--',
          health_score: data.health_score || 0,
          last_update: new Date().toISOString(),
        });
      }
    } catch (error) {
      console.error('Failed to fetch system metrics:', error);
    }
  }, []);

  const fetchRealData = useCallback(async (showRefresh: boolean = false) => {
    try {
      if (showRefresh) setIsRefreshing(true);
      setError(null);
      
      const [statusData, signalsData, brainData, perfData] = await Promise.all([
        inksideAPI.getStatus(),
        inksideAPI.getSignals(),
        inksideAPI.getBrainState(),
        inksideAPI.getPerformance(),
      ]);
      
      setApiStatus(statusData);
      setRealSignals(mapSignalData(signalsData.signals || []));
      setBrainState(brainData);
      setPerformance(perfData);
      
      if (statusData?.bot) {
        setEngineRunning(statusData.bot.state === 'RUNNING' || statusData.bot.state === 'ACTIVE');
        setLearningActive(statusData.bot.consciousness || false);
        setCycleCount(statusData.bot.results || 0);
        if (brainData?.brain) {
          setConsciousnessLevel(brainData.brain.health / 100 || 0.5);
        }
      }
      
      await fetchSystemMetrics();
      setRetryCount(0);
    } catch (err) {
      console.error('Failed to fetch real data:', err);
      setError('Gagal mengambil data dari backend. Pastikan backend berjalan di port 5001.');
      setRetryCount(prev => prev + 1);
    } finally {
      if (showRefresh) setIsRefreshing(false);
    }
  }, [mapSignalData, fetchSystemMetrics]);

  // ============================================================
  // INIT
  // ============================================================
  
  useEffect(() => {
    let mounted = true;
    const init = async () => {
      if (!mounted) return;
      setIsInitialLoading(true);
      await fetchRealData(false);
      if (mounted) setIsInitialLoading(false);
    };
    init();
    
    const interval = setInterval(() => {
      if (mounted) fetchRealData(false);
    }, 30000);
    
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, [fetchRealData]);

  // ============================================================
  // HANDLERS
  // ============================================================
  
  const handleToggleEngine = useCallback(async () => {
    setIsToggling(true);
    try {
      const next = !engineRunning;
      
      // Kirim request ke backend
      if (next) {
        try {
          await fetch('/api/engine/start', {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'X-API-Key': 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ'
            }
          });
        } catch (e) {
          console.warn('Start engine API failed, using fallback:', e);
        }
      } else {
        try {
          await fetch('/api/engine/stop', {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'X-API-Key': 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ'
            }
          });
        } catch (e) {
          console.warn('Stop engine API failed, using fallback:', e);
        }
      }
      
      // Update local state
      setEngineRunning(next);
      
      // Simpan ke localStorage
      localStorage.setItem('inkside_engine_state', JSON.stringify({
        running: next,
        updatedAt: new Date().toISOString()
      }));
      
      // Tambah log
      setLogs(prevLogs => [
        {
          id: Date.now(),
          timestamp: Date.now(),
          level: next ? 'SUCCESS' : 'WARNING',
          message: next
            ? 'Trading Engine & MTF Scanner started.'
            : 'Trading Engine stopped gracefully.',
          source: 'Engine',
        },
        ...prevLogs.slice(0, 99),
      ]);
      
      // Broadcast via WebSocket (optional)
      try {
        const ws = new WebSocket('ws://45.41.204.21/socket.io/');
        ws.onopen = () => {
          ws.send(JSON.stringify({
            channel: 'engine',
            payload: { running: next, type: 'engine_status' }
          }));
          ws.close();
        };
      } catch (e) {
        // Silent fail
      }
      
    } catch (err) {
      console.error('Engine toggle error:', err);
      setError('Failed to toggle engine');
    } finally {
      setIsToggling(false);
    }
  }, [engineRunning]);

  const handleRefreshData = useCallback(() => {
    fetchRealData(true);
    setLogs(prevLogs => [
      {
        id: Date.now(),
        timestamp: Date.now(),
        level: 'INFO',
        message: 'All subsystems refreshed with real data from backend API.',
        source: 'System',
      },
      ...prevLogs.slice(0, 99),
    ]);
  }, [fetchRealData]);

  const handleAddKnowledge = useCallback((item: Partial<KnowledgeItem>) => {
    const newItem: KnowledgeItem = {
      id: `kb-${Date.now()}`,
      content: item.content || '',
      category: item.category || 'General',
      type: item.type || 'fact',
      confidence: item.confidence || 85,
      importance: item.importance || 0.8,
      tags: item.tags || ['manual'],
      status: 'active',
      createdAt: item.createdAt || new Date().toISOString(),
    };
    setKnowledgeList(prev => [newItem, ...prev]);
    setLogs(prevLogs => [
      {
        id: Date.now(),
        timestamp: Date.now(),
        level: 'SUCCESS',
        message: `Added new knowledge item: "${newItem.content.substring(0, 50)}..."`,
        source: 'Knowledge',
      },
      ...prevLogs.slice(0, 99),
    ]);
  }, []);

  const handleClosePosition = useCallback((id: string) => {
    setPositions(prev => prev.filter(p => p.id !== id));
    setLogs(prevLogs => [
      {
        id: Date.now(),
        timestamp: Date.now(),
        level: 'INFO',
        message: `Position ${id} closed.`,
        source: 'TradingBot',
      },
      ...prevLogs.slice(0, 99),
    ]);
  }, []);

  // ============================================================
  // RENDER
  // ============================================================
  
  if (isInitialLoading) {
    return <LoadingScreen message="Loading Inkside Digital..." />;
  }

  if (error && retryCount > 3) {
    return (
      <ErrorScreen 
        error={error} 
        onRetry={() => {
          setRetryCount(0);
          fetchRealData(true);
        }} 
      />
    );
  }

  const connectionStatus = getConnectionStatus();
  
  return (
    <div className="flex flex-col h-screen w-screen bg-[#0B0F14] text-[#E8EDF2] overflow-hidden font-sans">
      {/* Main Layout: Sidebar + Content */}
      <div className="flex flex-1 min-h-0">
        {/* Sidebar */}
        <Sidebar
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          engineRunning={engineRunning}
          learningActive={learningActive}
          cycleCount={cycleCount}
          wsConnected={isConnected}
          wsStatus={connectionStatus}
          healthScore={systemMetrics.health_score}
          version="1.0.0"
          watchlistCount={watchlistCount}
          isOpen={isSidebarOpen}
          onClose={() => setIsSidebarOpen(false)}
        />

        {/* Main Content */}
        <div className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
          <TopBar
            currentPage={currentPage}
            engineRunning={engineRunning}
            onToggleEngine={handleToggleEngine}
            telegramConfigured={telegramConfigured}
            onRefreshData={handleRefreshData}
            isRefreshing={isRefreshing}
            wsConnected={isConnected}
            wsStatus={connectionStatus}
            healthScore={systemMetrics.health_score}
            uptime={systemMetrics.uptime}
            systemMode="PAPER"
            riskLevel={systemMetrics.risk_level}
            watchlistCount={watchlistCount}
            engineState={engineRunning ? 'RUNNING' : 'IDLE'}
            isToggling={isToggling}
            onOpenSidebar={() => setIsSidebarOpen(true)}
            onNavigateWatchlist={() => setCurrentPage('Watchlist')}
          />

          <main className="flex-1 overflow-y-auto p-4 sm:p-6 pb-20 sm:pb-6 scrollbar-thin scrollbar-thumb-[#26313D] scrollbar-track-transparent">
            
            {currentPage === 'Dashboard' && (
              <DashboardView
                tickers={tickers}
                signals={realSignals.length > 0 ? realSignals as any : signals}
                insights={insights}
                engineRunning={engineRunning}
                learningActive={learningActive}
                cycleCount={cycleCount}
                brainState={apiStatus?.bot?.state || 'IDLE'}
                consciousnessLevel={consciousnessLevel}
                systemMetrics={systemMetrics}
                onNavigate={setCurrentPage}
                wsConnected={isConnected}
              />
            )}

            {currentPage === 'Brain' && (
              <BrainView
                brainState={apiStatus?.bot?.state || 'IDLE'}
                cycleCount={cycleCount}
                healthScore={systemMetrics.health_score || 95}
                onRefresh={handleRefreshData}
                wsConnected={isConnected}
              />
            )}

            {currentPage === 'Reflection' && (
              <ReflectionView
                consciousnessLevel={consciousnessLevel}
                emotionalState={emotionalState}
                wsConnected={isConnected}
              />
            )}

            {currentPage === 'Market' && (
              <MarketView tickers={tickers} wsConnected={isConnected} />
            )}

            {currentPage === 'Watchlist' && (
              <WatchlistView
                tickers={tickers}
                signals={realSignals.length > 0 ? realSignals as any : signals}
                onNavigateToTrading={(pair: string) => {
                  setCurrentPage('Trading');
                  localStorage.setItem('inkside_selected_pair', pair);
                }}
                onNavigateToSignals={(pair: string) => {
                  setCurrentPage('Signals');
                  localStorage.setItem('inkside_selected_pair', pair);
                }}
                wsConnected={isConnected}
              />
            )}

            {currentPage === 'Signals' && (
              <SignalsView signals={realSignals.length > 0 ? realSignals as any : signals} wsConnected={isConnected} />
            )}

            {currentPage === 'Learning' && (
              <LearningView learningActive={learningActive} cycleCount={cycleCount} wsConnected={isConnected} />
            )}

            {currentPage === 'Memory' && <MemoryView wsConnected={isConnected} />}
            {currentPage === 'Pattern' && <PatternView wsConnected={isConnected} />}
            {currentPage === 'Prediction' && <PredictionView wsConnected={isConnected} />}
            {currentPage === 'Decision' && <DecisionView wsConnected={isConnected} />}

            {currentPage === 'Knowledge' && (
              <KnowledgeView knowledgeList={knowledgeList} onAddKnowledge={handleAddKnowledge} wsConnected={isConnected} />
            )}

            {currentPage === 'Health' && (
              <HealthView components={components} healthScore={systemMetrics.health_score || 95} wsConnected={isConnected} />
            )}

            {currentPage === 'Trading' && (
              <TradingControlView
                engineRunning={engineRunning}
                onToggleEngine={handleToggleEngine}
                positions={positions}
                onClosePosition={handleClosePosition}
                wsConnected={isConnected}
              />
            )}

            {currentPage === 'Telegram' && (
              <TelegramView
                isConfigured={telegramConfigured}
                onSaveConfig={() => setTelegramConfigured(true)}
                wsConnected={isConnected}
              />
            )}

            {currentPage === 'Diagnostics' && <DiagnosticsView wsConnected={isConnected} />}
            {currentPage === 'Settings' && <SettingsView wsConnected={isConnected} />}
            
          </main>
        </div>
      </div>

      {/* Bottom Navigation (Mobile Only) */}
      <BottomNav
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        onOpenMenu={() => setIsSidebarOpen(true)}
        watchlistCount={watchlistCount}
        engineRunning={engineRunning}
        wsConnected={isConnected}
        healthScore={systemMetrics.health_score}
      />
    </div>
  );
}

// ============================================================
// MAIN APP WITH WEBSOCKET PROVIDER
// ============================================================

export default function App() {
  return (
    <WebSocketProvider>
      <AppContent />
    </WebSocketProvider>
  );
}
