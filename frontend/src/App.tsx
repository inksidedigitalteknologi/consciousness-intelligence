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

import {
  INITIAL_TICKERS,
  INITIAL_SIGNALS,
  INITIAL_INSIGHTS,
  INITIAL_KNOWLEDGE,
  INITIAL_COMPONENTS,
  INITIAL_POSITIONS,
  INITIAL_LOGS,
} from './data/mockData';

import { inksideAPI, StatusResponse, Signal as APISignal, BrainStateResponse, PerformanceResponse } from './api/inkside';

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
// MAIN APP
// ============================================================

export default function App() {
  const [currentPage, setCurrentPage] = useState<NavigationPage>('Dashboard');
  
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
  // STATE FOR UI CONTROLS
  // ============================================================
  
  const [engineRunning, setEngineRunning] = useState(true);
  const [learningActive, setLearningActive] = useState(true);
  const [cycleCount, setCycleCount] = useState(1420);
  const [consciousnessLevel, setConsciousnessLevel] = useState(0.78);
  const [emotionalState, setEmotionalState] = useState('CALM');

  const [tickers, setTickers] = useState<TickerInfo[]>(INITIAL_TICKERS);
  const [signals, setSignals] = useState<TradingSignal[]>(INITIAL_SIGNALS);
  const [insights, setInsights] = useState<CognitiveInsight[]>(INITIAL_INSIGHTS);
  const [knowledgeList, setKnowledgeList] = useState<KnowledgeItem[]>(INITIAL_KNOWLEDGE);
  const [components, setComponents] = useState<ComponentHealthStatus[]>(INITIAL_COMPONENTS);
  const [positions, setPositions] = useState<TradingPosition[]>(INITIAL_POSITIONS);
  const [logs, setLogs] = useState<SystemLogEntry[]>(INITIAL_LOGS);
  const [telegramConfigured, setTelegramConfigured] = useState(true);

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
  // FETCH REAL DATA (TANPA LOADING BERKEDIP)
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
  // INITIAL LOAD & AUTO UPDATE (TANPA BERKEDIP)
  // ============================================================
  
  useEffect(() => {
    const init = async () => {
      setIsInitialLoading(true);
      await fetchRealData(false);
      setIsInitialLoading(false);
    };
    init();
    
    // Update setiap 15 detik TANPA loading indicator
    const interval = setInterval(() => {
      fetchRealData(false);
    }, 15000);
    
    return () => clearInterval(interval);
  }, []);

  // ============================================================
  // LIVE SIMULATION (untuk data dummy)
  // ============================================================
  
  useEffect(() => {
    if (!engineRunning) return;

    const interval = setInterval(() => {
      setCycleCount((c) => c + 1);

      setTickers((prevTickers) =>
        prevTickers.map((t) => {
          const delta = (Math.random() - 0.49) * (t.price * 0.0008);
          const newPrice = Math.max(0.001, t.price + delta);
          const updatedHistory = [...t.history.slice(1), newPrice];
          return {
            ...t,
            price: newPrice,
            change24h: t.change24h + (delta > 0 ? 0.01 : -0.01),
            history: updatedHistory,
          };
        })
      );
    }, 2500);

    return () => clearInterval(interval);
  }, [engineRunning]);

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
              onNavigate={setCurrentPage}
            />
          )}

          {currentPage === 'Brain' && (
            <BrainView
              brainState={apiStatus?.bot?.state || 'IDLE'}
              cycleCount={cycleCount}
              healthScore={95}
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

          {/* ⬇️ WATCHLIST VIEW - TAMBAHKAN INI ⬇️ */}
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
            <HealthView components={components} healthScore={95} />
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
