// ============================================================
// CANDLE DATA
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
  candles: CandleData[];
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

// ============================================================
// API RESPONSE TYPES
// ============================================================

export interface StatusResponse {
  status: string;
  bot: {
    state: string;
    consciousness: boolean;
    results: number;
    health: number;
  };
  server: {
    uptime: number;
    version: string;
  };
}

export interface BrainStateResponse {
  brain: {
    health: number;
    neurons: number;
    connections: number;
    learning_rate: number;
  };
  consciousness: {
    level: number;
    state: string;
  };
}

export interface PerformanceResponse {
  pnl: number;
  win_rate: number;
  total_trades: number;
  prediction_accuracy: number;
  open_positions: number;
  risk_level: string;
}

export interface Signal {
  pair: string;
  signal: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  price: number;
  strength: 'STRONG' | 'WEAK' | 'NEUTRAL';
  timestamp: string;
}

// ============================================================
// SYSTEM METRICS
// ============================================================

export interface SystemMetrics {
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
// WEBSOCKET MESSAGES
// ============================================================

export interface WebSocketMessage {
  type: string;
  payload: any;
  channel: string;
}

export interface WebSocketChannelData {
  channel: string;
  type: string;
  payload: any;
}

// ============================================================
// COMPONENT PROPS
// ============================================================

export interface BaseViewProps {
  wsConnected?: boolean;
  onRefresh?: () => void;
}

export interface DashboardViewProps extends BaseViewProps {
  tickers: TickerInfo[];
  signals: TradingSignal[];
  insights: CognitiveInsight[];
  engineRunning: boolean;
  learningActive: boolean;
  cycleCount: number;
  brainState: string;
  consciousnessLevel: number;
  systemMetrics: SystemMetrics;
  onNavigate: (page: NavigationPage) => void;
}

export interface SignalViewProps extends BaseViewProps {
  signals: TradingSignal[];
}

export interface KnowledgeViewProps extends BaseViewProps {
  knowledgeList: KnowledgeItem[];
  onAddKnowledge: (item: Partial<KnowledgeItem>) => void;
}

export interface TradingViewProps extends BaseViewProps {
  engineRunning: boolean;
  onToggleEngine: () => void;
  positions: TradingPosition[];
  onClosePosition: (id: string) => void;
}

export interface HealthViewProps extends BaseViewProps {
  components: ComponentHealthStatus[];
  healthScore: number;
}

export interface TelegramViewProps extends BaseViewProps {
  isConfigured: boolean;
  onSaveConfig: () => void;
}

export interface WatchlistViewProps extends BaseViewProps {
  tickers: TickerInfo[];
  signals: TradingSignal[];
  onNavigateToTrading: (pair: string) => void;
  onNavigateToSignals: (pair: string) => void;
}

// ============================================================
// HOOK TYPES
// ============================================================

export interface UseLocalStorageReturn<T> {
  value: T;
  setValue: (value: T) => void;
  removeValue: () => void;
}

export interface UseWebSocketReturn {
  isConnected: boolean;
  reconnectAttempts: number;
  subscribe: (channel: string, callback: (data: any) => void) => () => void;
  sendMessage: (message: WebSocketMessage) => void;
  getConnectionStatus: () => string;
  reconnect: () => void;
}

// ============================================================
// UTILITY TYPES
// ============================================================

export type SignalStrength = 'STRONG' | 'WEAK' | 'NEUTRAL';
export type SignalDirection = 'BUY' | 'SELL' | 'HOLD';
export type PositionStatus = 'OPEN' | 'CLOSED' | 'STOPPED' | 'TAKE_PROFIT';
export type LogLevel = 'INFO' | 'WARNING' | 'ERROR' | 'SUCCESS' | 'DEBUG';
export type ComponentStatus = 'healthy' | 'warning' | 'error' | 'unknown';
export type KnowledgeStatus = 'active' | 'archived' | 'learning';
export type KnowledgeType = 'fact' | 'rule' | 'pattern' | 'strategy';
export type TrendDirection = 'BULLISH' | 'BEARISH' | 'NEUTRAL';
export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH';
