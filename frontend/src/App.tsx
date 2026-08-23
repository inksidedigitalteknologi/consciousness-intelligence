import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
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
    if (saved && saved !== 'undefined') {
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
}

// ============================================================
// LOADING SCREEN COMPONENT
// ============================================================

const LoadingScreen: React.FC = () => (
  <div className="flex h-screen w-screen bg-[#0B0F14] items-center justify-center">
    <div className="text-center">
      <div className="text-4xl mb-4">🧠</div>
      <div className="text-white text-xl">Loading Inkside Digital...</div>
      <div className="text-gray-500 text-sm mt-2">Menghubungkan ke backend...</div>
    </div>
  </div>
);

// ============================================================
// DEFAULT SYSTEM METRICS
// ============================================================

const defaultSystemMetrics: SystemMetrics = {
  cpu: 0,
  ram: 0,
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
};

// ============================================================
// MAIN APP
// ============================================================

export default function App() {
  // ============================================================
  // NAVIGATION STATE - LOAD FROM LOCALSTORAGE
  // ============================================================
  
  const [currentPage, setCurrentPage] = useState<NavigationPage>(loadCurrentPage);
  
  // Auto-save page ke localStorage
  useEffect(() => {
    saveCurrentPage(currentPage);
  }, [currentPage]);

  // ============================================================
  // STATE FOR BACKEND REAL DATA
  // ============================================================
  
  const [apiStatus, setApiStatus] = useState<StatusResponse | null>(null);
  const [realSignals, setRealSignals] = useState<APISignal[]>([]);
  const [brainState, setBrainState] = useState<BrainStateResponse | null>(null);
  const [performance, setPerformance] = useState<PerformanceResponse | null>(null);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // ============================================================
  // STATE FOR UI CONTROLS (REAL DATA)
  // ============================================================
  
  const [engineRunning, setEngineRunning] = useState(false);
  const [learningActive, setLearningActive] = useState(false);
  const [cycleCount, setCycleCount] = useState(0);
  const [consciousnessLevel, setConsciousnessLevel] = useState(0.5);
  const [emotionalState, setEmotionalState] = useState('CALM');
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics>(defaultSystemMetrics);

  // ============================================================
  // STATE FOR UI DATA (DARI BACKEND ATAU KOSONG)
  // ============================================================
  
  const [tickers, setTickers] = useState<TickerInfo[]>([]);
  const [signals, setSignals] = useState<TradingSignal[]>([]);
  const [insights, setInsights] = useState<CognitiveInsight[]>([]);
  const [knowledgeList, setKnowledgeList] = useState<KnowledgeItem[]>([]);
  const [components, setComponents] = useState<ComponentHealthStatus[]>([]);
  const [positions, setPositions] = useState<TradingPosition[]>([]);
  const [logs, setLogs] = useState<SystemLogEntry[]>([]);
  const [telegramConfigured, setTelegramConfigured] = useState(false);

  // ============================================================
  // MAP DATA API KE FORMAT KOMPATIBEL
  // ============================================================
  
  const mapSignalData = (apiSignals: any[]): any[] => {
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
  };

  // ============================================================
  // FETCH SYSTEM METRICS
  // ============================================================
  
  const fetchSystemMetrics = async () => {
    try {
      const response = await fetch('/api/system/metrics');
      if (response.ok) {
        const data = await response.json();
        setSystemMetrics({
          cpu: data.cpu || 0,
          ram: data.ram || 0,
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
        });
      }
    } catch (error) {
      console.error('Failed to fetch system metrics:', error);
    }
  };

  // ============================================================
  // FETCH REAL DATA
  // ============================================================
  
  const fetchRealData = async (showRefresh: boolean = false) => {
    try {
      if (showRefresh) {
        setIsRefreshing(true);
      }
      
      setError(null);
      
      const [statusData, signalsData, brainData, perfData] = await Promise.all([
        inksideAPI.getStatus(),
        inksideAPI.getSignals(),
        inksideAPI.getBrainState(),
        inksideAPI.getPerformance(),
      ]);
      
      setApiStatus(statusData);
      
      const mappedSignals = mapSignalData(signalsData.signals || []);
      setRealSignals(mappedSignals);
      
      setBrainState(brainData);
      setPerformance(perfData);
      
      if (statusData?.bot) {
        setEngineRunning(statusData.bot.state === 'RUNNING' || statusData.bot.state === 'ACTIVE');
        setLearningActive(statusData.bot.consciousness || false);
        setCycleCount(statusData.bot.results || 0);
      }
      
      // Fetch system metrics
      await fetchSystemMetrics();
      
    } catch (err) {
      console.error('Failed to fetch real data:', err);
      setError('Gagal mengambil data dari backend. Pastikan backend berjalan di port 5001.');
    } finally {
      if (showRefresh) {
        setIsRefreshing(false);
      }
    }
  };

  // ============================================================
  // INITIAL LOAD & AUTO UPDATE
  // ============================================================
  
  useEffect(() => {
    const init = async () => {
      setIsInitialLoading(true);
      await fetchRealData(false);
      setIsInitialLoading(false);
    };
    init();
    
    const interval = setInterval(() => {
      fetchRealData(false);
    }, 30000);
    
    return () => clearInterval(interval);
  }, []);

  // ============================================================
  // HANDLERS
  // ============================================================
  
  const handleToggleEngine = () => {
    setEngineRunning((prev) => {
      const next = !prev;
      setLogs((prevLogs) => [
        {
          id: Date.now(),
          timestamp: Date.now(),
          level: next ? 'SUCCESS' : 'WARNING',
          message: next
            ? 'Trading Engine & MTF Scanner started by user command.'
            : 'Trading Engine stopped gracefully.',
          source: 'Engine',
        },
        ...prevLogs,
      ]);
      return next;
    });
  };

  const handleRefreshData = () => {
    fetchRealData(true);
    setLogs((prevLogs) => [
      {
        id: Date.now(),
        timestamp: Date.now(),
        level: 'INFO',
        message: 'All subsystems refreshed with real data from backend API.',
        source: 'System',
      },
      ...prevLogs,
    ]);
  };

  const handleAddKnowledge = (item: Partial<KnowledgeItem>) => {
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
    setKnowledgeList((prev) => [newItem, ...prev]);

    setLogs((prevLogs) => [
      {
        id: Date.now(),
        timestamp: Date.now(),
        level: 'SUCCESS',
        message: `Added new knowledge item: "${newItem.content.substring(0, 50)}..."`,
        source: 'Knowledge',
      },
      ...prevLogs,
    ]);
  };

  const handleClosePosition = (id: string) => {
    setPositions((prev) => prev.filter((p) => p.id !== id));
    setLogs((prevLogs) => [
      {
        id: Date.now(),
        timestamp: Date.now(),
        level: 'INFO',
        message: `Position ${id} closed with profit.`,
        source: 'TradingBot',
      },
      ...prevLogs,
    ]);
  };

  // ============================================================
  // RENDER - Loading
  // ============================================================
  
  if (isInitialLoading) {
    return <LoadingScreen />;
  }

  if (error) {
    return (
      <div className="flex h-screen w-screen bg-[#0B0F14] items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-4xl mb-4">❌</div>
          <div className="text-red-400 text-xl">{error}</div>
          <button
            onClick={() => fetchRealData(true)}
            className="mt-4 px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // ============================================================
  // RENDER - Main App
  // ============================================================
  
  return (
    <div className="flex h-screen w-screen bg-[#0B0F14] text-[#E8EDF2] overflow-hidden font-sans">
      {/* Left Sidebar */}
      <Sidebar
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        engineRunning={engineRunning}
        learningActive={learningActive}
        cycleCount={cycleCount}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        <TopBar
          currentPage={currentPage}
          engineRunning={engineRunning}
          onToggleEngine={handleToggleEngine}
          telegramConfigured={telegramConfigured}
          onRefreshData={handleRefreshData}
          isRefreshing={isRefreshing}
        />

        {/* Scrollable View Container */}
        <main className="flex-1 overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-[#26313D] scrollbar-track-transparent">
          
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
            />
          )}

          {currentPage === 'Brain' && (
            <BrainView
              brainState={apiStatus?.bot?.state || 'IDLE'}
              cycleCount={cycleCount}
              healthScore={systemMetrics.health_score || 95}
              onRefresh={handleRefreshData}
            />
          )}

          {currentPage === 'Reflection' && (
            <ReflectionView
              consciousnessLevel={consciousnessLevel}
              emotionalState={emotionalState}
            />
          )}

          {currentPage === 'Market' && <MarketView tickers={tickers} />}

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
            />
          )}

          {currentPage === 'Signals' && (
            <SignalsView signals={realSignals.length > 0 ? realSignals as any : signals} />
          )}

          {currentPage === 'Learning' && (
            <LearningView learningActive={learningActive} cycleCount={cycleCount} />
          )}

          {currentPage === 'Memory' && <MemoryView />}
          {currentPage === 'Pattern' && <PatternView />}
          {currentPage === 'Prediction' && <PredictionView />}
          {currentPage === 'Decision' && <DecisionView />}

          {currentPage === 'Knowledge' && (
            <KnowledgeView knowledgeList={knowledgeList} onAddKnowledge={handleAddKnowledge} />
          )}

          {currentPage === 'Health' && (
            <HealthView components={components} healthScore={systemMetrics.health_score || 95} />
          )}

          {currentPage === 'Trading' && (
            <TradingControlView
              engineRunning={engineRunning}
              onToggleEngine={handleToggleEngine}
              positions={positions}
              onClosePosition={handleClosePosition}
            />
          )}

          {currentPage === 'Telegram' && (
            <TelegramView
              isConfigured={telegramConfigured}
              onSaveConfig={() => setTelegramConfigured(true)}
            />
          )}

          {currentPage === 'Diagnostics' && <DiagnosticsView />}
          {currentPage === 'Settings' && <SettingsView />}
          
        </main>
      </div>
    </div>
  );
}
