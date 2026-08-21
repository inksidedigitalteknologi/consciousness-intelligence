// ============================================================
// CANDLE DATA - TAMBAHKAN INI
// ============================================================

export interface CandleData {
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  timestamp: number;
}

// ============================================================
// TICKER & MARKET DATA
// ============================================================

export interface TickerInfo {
  pair: string;
  name: string;
  price: number;
  change24h: number;
  high24h: number;
  low24h: number;
  volume24h: number;
  history: number[];
  rsi: number;
  macd: number;
  atr: number;
  trend: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
  bid: number;
  ask: number;
  depth: number;
  candles: CandleData[]; // TAMBAHKAN INI
}

// ============================================================
// WATCHLIST
// ============================================================

export interface WatchlistEntry {
  pair: string;
  pinned: boolean;
  notes: string;
  alertHigh?: number;
  alertLow?: number;
}

// ============================================================
// TRADING SIGNALS
// ============================================================

export interface TradingSignal {
  id: string;
  pair: string;
  signal: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  price: number;
  strength: 'STRONG' | 'WEAK' | 'NEUTRAL';
  timestamp: string;
  entry: number;
  stopLoss: number;
  tp1: number;
  tp2: number;
  quality: 'EXCELLENT' | 'GOOD' | 'NEUTRAL';
  riskReward: number;
  mtfAlignment: {
    '5m': string;
    '15m': string;
    '1h': string;
    '4h': string;
    '1d': string;
  };
  reasons: string[];
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  trend: string;
  timeframe: string;
}

// ============================================================
// COGNITIVE INSIGHTS
// ============================================================

export interface CognitiveInsight {
  id: string;
  type: 'PATTERN' | 'SENTIMENT' | 'PREDICTION' | 'ANOMALY';
  title: string;
  description: string;
  confidence: number;
  timestamp: string;
  pair?: string;
  data?: any;
}

// ============================================================
// KNOWLEDGE
// ============================================================

export interface KnowledgeItem {
  id: string;
  content: string;
  category: string;
  type: 'fact' | 'rule' | 'pattern' | 'strategy';
  confidence: number;
  importance: number;
  tags: string[];
  status: 'active' | 'archived' | 'learning';
  createdAt: string;
  updatedAt?: string;
}

// ============================================================
// COMPONENT HEALTH
// ============================================================

export interface ComponentHealthStatus {
  name: string;
  status: 'healthy' | 'warning' | 'error' | 'unknown';
  lastCheck: string;
  metrics: {
    cpu?: number;
    memory?: number;
    latency?: number;
    uptime?: number;
  };
  message?: string;
}

// ============================================================
// TRADING POSITIONS
// ============================================================

export interface TradingPosition {
  id: string;
  pair: string;
  type: 'LONG' | 'SHORT';
  entryPrice: number;
  currentPrice: number;
  size: number;
  leverage: number;
  pnl: number;
  pnlPercent: number;
  status: 'OPEN' | 'CLOSED' | 'STOPPED' | 'TAKE_PROFIT';
  entryTime: string;
  exitTime?: string;
  stopLoss?: number;
  takeProfit?: number;
}

// ============================================================
// SYSTEM LOGS
// ============================================================

export interface SystemLogEntry {
  id: number;
  timestamp: number;
  level: 'INFO' | 'WARNING' | 'ERROR' | 'SUCCESS' | 'DEBUG';
  message: string;
  source: string;
  details?: any;
}

// ============================================================
// NAVIGATION
// ============================================================

export type NavigationPage = 
  | 'Dashboard'
  | 'Brain'
  | 'Reflection'
  | 'Market'
  | 'Watchlist'
  | 'Signals'
  | 'Learning'
  | 'Memory'
  | 'Pattern'
  | 'Prediction'
  | 'Decision'
  | 'Knowledge'
  | 'Health'
  | 'Trading'
  | 'Telegram'
  | 'Diagnostics'
  | 'Settings';
