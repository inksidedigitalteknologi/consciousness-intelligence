export type NavigationPage =
  | 'Dashboard'
  | 'Watchlist'
  | 'Brain'
  | 'Consciousness'
  | 'Market'
  | 'Signals'
  | 'Learning'
  | 'Memory'
  | 'Pattern'
  | 'Prediction'
  | 'Decision'
  | 'Reflection'
  | 'Health'
  | 'Knowledge'
  | 'Telegram'
  | 'Trading'
  | 'PyRemote'
  | 'Diagnostics'
  | 'Settings';

export interface TickerInfo {
  pair: string;
  name: string;
  price: number;
  change24h: number;
  high24h: number;
  low24h: number;
  volume24h: number;
  trend: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
  rsi: number;
  macd: number;
  atr: number;
  history: number[];
}

export interface TradingSignal {
  id: string;
  pair: string;
  signal: 'BUY' | 'STRONG_BUY' | 'SELL' | 'STRONG_SELL' | 'HOLD' | 'MONITOR';
  confidence: number;
  quality: 'EXCELLENT' | 'GOOD' | 'FAIR' | 'WEAK' | 'NEUTRAL';
  price: number;
  entry: number;
  stopLoss: number;
  tp1: number;
  tp2: number;
  tp3: number;
  riskReward: number;
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'EXTREME';
  trend: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
  timeframe: string;
  mtfAlignment: {
    '5m': string;
    '15m': string;
    '1h': string;
    '4h': string;
    '1d': string;
  };
  reasons: string[];
  warnings: string[];
  timestamp: string;
}

export interface CognitiveInsight {
  id: string;
  title: string;
  content: string;
  category: 'brain' | 'consciousness' | 'market' | 'learning' | 'exchange' | 'system' | 'general';
  confidence: number;
  importance: number;
  timestamp: string;
}

export interface KnowledgeItem {
  id: string;
  content: string;
  category: string;
  type: string;
  confidence: number;
  importance: number;
  tags: string[];
  status: 'active' | 'archived' | 'expired';
  createdAt: string;
}

export interface SystemLogEntry {
  id: number;
  timestamp: number;
  level: 'INFO' | 'WARNING' | 'ERROR' | 'SUCCESS' | 'STDOUT';
  message: string;
  source: string;
}

export interface ComponentHealthStatus {
  name: string;
  status: 'ONLINE' | 'DEGRADED' | 'OFFLINE' | 'INITIALIZING';
  score: number;
  checks: number;
  errors: number;
  latencyMs: number;
  lastCheck: string;
}

export interface TradingPosition {
  id: string;
  pair: string;
  side: 'BUY' | 'SELL';
  entryPrice: number;
  currentPrice: number;
  amount: number;
  pnlUsd: number;
  pnlPercent: number;
  stopLoss: number;
  takeProfit: number;
  openTime: string;
}

export interface WatchlistEntry {
  pair: string;
  addedAt: string;
  alertHigh?: number;
  alertLow?: number;
  notes?: string;
  pinned?: boolean;
}
