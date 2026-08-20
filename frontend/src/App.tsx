import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
import { DashboardView } from './components/DashboardView';
import { BrainView } from './components/BrainView';
import { ReflectionView } from './components/ReflectionView';
import { MarketView } from './components/MarketView';
import { SignalsView } from './components/SignalsView';
import { LearningView } from './components/LearningView';
import { KnowledgeView } from './components/KnowledgeView';
import { HealthView } from './components/HealthView';
import { TradingControlView } from './components/TradingControlView';
import { TelegramView } from './components/TelegramView';
import { PyRemoteView } from './components/PyRemoteView';
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

export default function App() {
  const [currentPage, setCurrentPage] = useState<NavigationPage>('Dashboard');
  const [engineRunning, setEngineRunning] = useState(true);
  const [learningActive, setLearningActive] = useState(true);
  const [cycleCount, setCycleCount] = useState(1420);
  const [brainState, setBrainState] = useState('ACTIVE');
  const [consciousnessLevel, setConsciousnessLevel] = useState(0.78);
  const [emotionalState, setEmotionalState] = useState('CALM');

  const [tickers, setTickers] = useState<TickerInfo[]>(INITIAL_TICKERS);
  const [signals, setSignals] = useState<TradingSignal[]>(INITIAL_SIGNALS);
  const [insights, setInsights] = useState<CognitiveInsight[]>(INITIAL_INSIGHTS);
  const [knowledgeList, setKnowledgeList] = useState<KnowledgeItem[]>(INITIAL_KNOWLEDGE);
  const [components, setComponents] = useState<ComponentHealthStatus[]>(INITIAL_COMPONENTS);
  const [positions, setPositions] = useState<TradingPosition[]>(INITIAL_POSITIONS);
  const [logs, setLogs] = useState<SystemLogEntry[]>(INITIAL_LOGS);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [telegramConfigured, setTelegramConfigured] = useState(true);

  // Live simulation tick
  useEffect(() => {
    if (!engineRunning) return;

    const interval = setInterval(() => {
      setCycleCount((c) => c + 1);

      // Random micro-fluctuation for price feed to mimic live WebSocket
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

  const handleToggleEngine = () => {
    setEngineRunning((prev) => {
      const next = !prev;
      setBrainState(next ? 'ACTIVE' : 'IDLE');
      setLearningActive(next);

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
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
      setCycleCount((c) => c + 10);
      setLogs((prevLogs) => [
        {
          id: Date.now(),
          timestamp: Date.now(),
          level: 'INFO',
          message: 'All 20+ subsystems refreshed. Synchronized with memory DB.',
          source: 'System',
        },
        ...prevLogs,
      ]);
    }, 400);
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
              signals={signals}
              insights={insights}
              engineRunning={engineRunning}
              learningActive={learningActive}
              cycleCount={cycleCount}
              brainState={brainState}
              consciousnessLevel={consciousnessLevel}
              onNavigate={setCurrentPage}
            />
          )}

          {currentPage === 'Brain' && (
            <BrainView
              brainState={brainState}
              cycleCount={cycleCount}
              healthScore={98}
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

          {currentPage === 'Signals' && <SignalsView signals={signals} />}

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
            <HealthView components={components} healthScore={98} />
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

          {currentPage === 'PyRemote' && (
            <PyRemoteView logs={logs} onClearLogs={() => setLogs([])} />
          )}

          {currentPage === 'Diagnostics' && <DiagnosticsView />}

          {currentPage === 'Settings' && <SettingsView />}
        </main>
      </div>
    </div>
  );
}
