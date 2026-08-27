// src/api/inkside.ts
// INKSIDE DIGITAL - API SERVICE v2.0
// FIX: Base URL sekarang tanpa /api di akhir

import axios from 'axios';

// ============================================================
// ✅ FIX: BASE URL TANPA /api di akhir
// ============================================================

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://45.41.204.21';
const API_KEY = import.meta.env.VITE_API_KEY || '';

// ============================================================
// TYPES & INTERFACES
// ============================================================

export interface StatusResponse {
  status: string;
  bot: {
    state: string;
    mode: string;
    cycles: number;
    uptime: number;
    version: string;
    consciousness: boolean;
    learning_engine: boolean;
    scanner: boolean;
    exchange: boolean;
    risk_level: string;
    portfolio: {
      cash: number;
      total_value: number;
      pnl: number;
      pnl_percentage: number;
    };
    performance: {
      total_trades: number;
      winning_trades: number;
      losing_trades: number;
      win_rate: number;
      total_pnl: number;
      total_pnl_percentage: number;
    };
  };
  version: string;
  mode: string;
  timestamp: string;
}

export interface Signal {
  pair: string;
  signal: 'BUY' | 'SELL' | 'HOLD' | 'MONITOR';
  confidence: number;
  price: number;
  strength?: string;
  timestamp: string;
}

export interface SignalsResponse {
  signals: Signal[];
  timestamp: string;
}

export interface MarketDataResponse {
  pair: string;
  data: {
    price: number;
    change: number;
    volume: number;
    high: number;
    low: number;
    trend: string;
    timestamp: string;
  };
  timestamp: string;
}

export interface BrainStateResponse {
  brain: {
    state: string;
    cycles: number;
    goals: Array<{
      name: string;
      priority: number;
      progress: number;
      status: string;
    }>;
    modules_available: number;
    total_modules: number;
    health: number;
    timestamp: string;
  };
  timestamp: string;
}

export interface ReflectionResponse {
  reflection: {
    awareness: number;
    emotion: string;
    curiosity: number;
    insights: string[];
    timestamp: string;
  };
  timestamp: string;
}

export interface PerformanceResponse {
  performance: {
    roi: number;
    trades: number;
    win_rate: number;
    total_pnl: number;
  };
  timestamp: string;
}

export interface Position {
  id: string;
  pair: string;
  type: 'LONG' | 'SHORT';
  entry_price: number;
  current_price: number;
  quantity: number;
  pnl: number;
  timestamp: number;
}

export interface PositionsResponse {
  positions: Position[];
  timestamp: string;
}

export interface LogEntry {
  id: number;
  timestamp: string;
  level: 'INFO' | 'SUCCESS' | 'WARNING' | 'ERROR';
  message: string;
  source: string;
}

export interface LogsResponse {
  logs: LogEntry[];
  count: number;
  timestamp: string;
}

export interface DiagnosticsResponse {
  diagnostics: {
    system: {
      cpu_usage: number;
      memory_usage: number;
      disk_usage: number;
      uptime: number;
    };
    application: {
      status: string;
      version: string;
      mode: string;
      uptime: number;
    };
  };
  timestamp: string;
}

export interface TelegramStatusResponse {
  configured: boolean;
  bot_name: string;
  status: 'online' | 'offline';
  last_message: string | null;
  timestamp: string;
}

export interface Prediction {
  pair: string;
  current_price: number;
  direction: 'UP' | 'DOWN' | 'SIDEWAYS';
  target_price: number;
  change_percent: number;
  confidence: number;
  regime: string;
  method: string;
  timeframe: string;
  rsi: number;
  macd: string;
  fib_level: string;
  sr_range: string;
  volatility: number;
  timestamp: string;
}

export interface PredictionMetricsResponse {
  overall_accuracy: number;
  sharpe_ratio: number;
  active_forecasts: number;
  market_regime: string;
  regime_confidence: number;
  last_update: string;
}

export interface MonteCarloRequest {
  pair: string;
  iterations: number;
  periods: number;
  method: string;
}

export interface MonteCarloResponse {
  bullish: {
    price: number;
    change_percent: number;
    probability: number;
    description: string;
  };
  base: {
    price: number;
    change_percent: number;
    probability: number;
    description: string;
  };
  bearish: {
    price: number;
    change_percent: number;
    probability: number;
    description: string;
  };
  confidence_interval: {
    lower: number;
    upper: number;
    median: number;
  };
  iterations: number;
  periods: number;
}

export interface SystemMetricsResponse {
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
}

export interface WatchdogStatusResponse {
  status: string;
  components: Record<string, any>;
  alerts: any[];
  timestamp: string;
}

// ============================================================
// API CLASS
// ============================================================

class InksideAPI {
  private baseUrl: string;
  private apiKey: string;

  constructor(baseUrl: string = API_BASE_URL, apiKey: string = API_KEY) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  // ============================================================
  // PRIVATE METHODS
  // ============================================================

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }
    return headers;
  }

  private async get<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    try {
      // ✅ PASTIKAN endpoint dimulai dengan /api/
      const url = endpoint.startsWith('/api/') ? endpoint : `/api${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
      const response = await axios.get<T>(`${this.baseUrl}${url}`, {
        params,
        timeout: 30000,
        headers: this.getHeaders(),
      });
      return response.data;
    } catch (error) {
      console.error(`❌ API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  private async post<T>(endpoint: string, data?: any): Promise<T> {
    try {
      const url = endpoint.startsWith('/api/') ? endpoint : `/api${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
      const response = await axios.post<T>(`${this.baseUrl}${url}`, data, {
        timeout: 30000,
        headers: this.getHeaders(),
      });
      return response.data;
    } catch (error) {
      console.error(`❌ API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  private async put<T>(endpoint: string, data?: any): Promise<T> {
    try {
      const url = endpoint.startsWith('/api/') ? endpoint : `/api${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
      const response = await axios.put<T>(`${this.baseUrl}${url}`, data, {
        timeout: 30000,
        headers: this.getHeaders(),
      });
      return response.data;
    } catch (error) {
      console.error(`❌ API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  private async delete<T>(endpoint: string): Promise<T> {
    try {
      const url = endpoint.startsWith('/api/') ? endpoint : `/api${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
      const response = await axios.delete<T>(`${this.baseUrl}${url}`, {
        timeout: 30000,
        headers: this.getHeaders(),
      });
      return response.data;
    } catch (error) {
      console.error(`❌ API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  // ============================================================
  // CORE API
  // ============================================================

  async getStatus(): Promise<StatusResponse> {
    return this.get<StatusResponse>('/status');
  }

  async getHealth(): Promise<{ status: string; uptime: number; version: string; timestamp: string }> {
    return this.get<{ status: string; uptime: number; version: string; timestamp: string }>('/health');
  }

  async getSignals(): Promise<SignalsResponse> {
    return this.get<SignalsResponse>('/signals');
  }

  async getMarketData(pair: string = 'BTC/USDT'): Promise<MarketDataResponse> {
    return this.get<MarketDataResponse>(`/market?pair=${encodeURIComponent(pair)}`);
  }

  async analyzePair(pair: string): Promise<any> {
    return this.get(`/analyze/${encodeURIComponent(pair)}`);
  }

  async getBrainState(): Promise<BrainStateResponse> {
    return this.get<BrainStateResponse>('/brain/state');
  }

  async getBrainReflection(): Promise<ReflectionResponse> {
    return this.get<ReflectionResponse>('/brain/reflection');
  }

  async getPerformance(): Promise<PerformanceResponse> {
    return this.get<PerformanceResponse>('/performance');
  }

  async getPositions(): Promise<PositionsResponse> {
    return this.get<PositionsResponse>('/positions');
  }

  async getLogs(limit: number = 50): Promise<LogsResponse> {
    return this.get<LogsResponse>(`/logs?limit=${limit}`);
  }

  async getDiagnostics(): Promise<DiagnosticsResponse> {
    return this.get<DiagnosticsResponse>('/diagnostics');
  }

  async getTelegramStatus(): Promise<TelegramStatusResponse> {
    return this.get<TelegramStatusResponse>('/telegram/status');
  }

  async startEngine(): Promise<{ status: string; success: boolean; timestamp: string }> {
    return this.post<{ status: string; success: boolean; timestamp: string }>('/engine/start');
  }

  async stopEngine(): Promise<{ status: string; success: boolean; timestamp: string }> {
    return this.post<{ status: string; success: boolean; timestamp: string }>('/engine/stop');
  }

  async getLearningStatus(): Promise<{ learning: { active: boolean; cycles: number; status: string }; timestamp: string }> {
    return this.get<{ learning: { active: boolean; cycles: number; status: string }; timestamp: string }>('/learning/status');
  }

  // ============================================================
  // PREDICTION API
  // ============================================================

  async getPredictions(params?: { pair?: string; horizon?: string; method?: string }): Promise<Prediction[]> {
    return this.get<Prediction[]>('/predictions', params);
  }

  async getPredictionMetrics(): Promise<PredictionMetricsResponse> {
    return this.get<PredictionMetricsResponse>('/predictions/metrics');
  }

  async runMonteCarlo(data: MonteCarloRequest): Promise<MonteCarloResponse> {
    return this.post<MonteCarloResponse>('/predictions/monte_carlo', data);
  }

  async getMonteCarlo(pair: string): Promise<MonteCarloResponse> {
    return this.get<MonteCarloResponse>(`/predictions/monte_carlo?pair=${encodeURIComponent(pair)}`);
  }

  // ============================================================
  // SYSTEM METRICS
  // ============================================================

  async getSystemMetrics(): Promise<SystemMetricsResponse> {
    return this.get<SystemMetricsResponse>('/system/metrics');
  }

  // ============================================================
  // WATCHDOG API
  // ============================================================

  async getWatchdogStatus(): Promise<WatchdogStatusResponse> {
    return this.get<WatchdogStatusResponse>('/watchdog/status');
  }

  async getWatchdogSnapshot(): Promise<any> {
    return this.get<any>('/watchdog/snapshot');
  }

  async getWatchdogData(): Promise<any> {
    return this.get<any>('/watchdog/data');
  }

  async getWatchdogComponent(name: string): Promise<any> {
    return this.get<any>(`/watchdog/component/${name}`);
  }

  async resetCircuitBreaker(component: string): Promise<{ status: string; message: string }> {
    return this.post<{ status: string; message: string }>(`/watchdog/circuit/${component}/reset`);
  }

  // ============================================================
  // PATTERN API
  // ============================================================

  async getPatterns(params?: { pair?: string; bias?: string; type?: string }): Promise<any> {
    return this.get<any>('/patterns', params);
  }

  async getPatternStats(): Promise<any> {
    return this.get<any>('/patterns/stats');
  }

  async detectPatterns(text: string): Promise<any> {
    return this.post<any>('/patterns/detect', { text });
  }

  // ============================================================
  // TELEGRAM API
  // ============================================================

  async setTelegramWebhook(url: string): Promise<{ status: string; message: string }> {
    return this.post<{ status: string; message: string }>('/telegram/set_webhook', { webhook_url: url });
  }

  async getTelegramWebhook(): Promise<any> {
    return this.get<any>('/telegram/get_webhook');
  }

  async sendTelegramMessage(chatId: string, text: string): Promise<{ success: boolean; message: string }> {
    return this.post<{ success: boolean; message: string }>('/telegram/send', { chat_id: chatId, text });
  }

  async testTelegram(): Promise<{ success: boolean; message: string }> {
    return this.post<{ success: boolean; message: string }>('/telegram/test');
  }

  // ============================================================
  // WATCHLIST API
  // ============================================================

  async getWatchlist(userId?: string): Promise<any> {
    const url = userId ? `/watchlist?user_id=${userId}` : '/watchlist';
    return this.get(url);
  }

  async addToWatchlist(pair: string, userId?: string): Promise<any> {
    return this.post('/watchlist', { pair, user_id: userId });
  }

  async removeFromWatchlist(pair: string, userId?: string): Promise<any> {
    const url = userId ? `/watchlist/${pair}?user_id=${userId}` : `/watchlist/${pair}`;
    return this.delete(url);
  }

  // ============================================================
  // KNOWLEDGE API
  // ============================================================

  async getKnowledgeStats(): Promise<any> {
    return this.get('/knowledge/stats');
  }

  async searchKnowledge(query: string): Promise<any> {
    return this.get(`/knowledge/search?q=${encodeURIComponent(query)}`);
  }

  async addKnowledge(data: any): Promise<any> {
    return this.post('/knowledge/add', data);
  }

  async askQuestion(question: string): Promise<any> {
    return this.post('/knowledge/ask', { question });
  }

  async fetchUrl(url: string): Promise<any> {
    return this.post('/knowledge/fetch-url', { url });
  }

  // ============================================================
  // LEARNING API
  // ============================================================

  async getLearningStats(): Promise<any> {
    return this.get('/learning/stats');
  }

  async getAdaptiveWeights(): Promise<any> {
    return this.get('/learning/adaptive');
  }

  async getCuriosityQuestions(): Promise<any> {
    return this.get('/learning/curiosity');
  }

  async addCuriosityQuestion(question: string, domain?: string, area?: string): Promise<any> {
    return this.post('/learning/curiosity', { question, domain, area });
  }

  async getGoals(): Promise<any> {
    return this.get('/learning/goals');
  }

  async getExperienceStats(): Promise<any> {
    return this.get('/learning/experience');
  }

  async getKnowledgeGraph(): Promise<any> {
    return this.get('/learning/graph');
  }

  async getEvaluatorStats(): Promise<any> {
    return this.get('/learning/evaluator');
  }

  // ============================================================
  // MODULES API
  // ============================================================

  async getModules(): Promise<any> {
    return this.get('/modules/list');
  }

  // ============================================================
  // SIMULATION API
  // ============================================================

  async runSimulation(params: any): Promise<any> {
    return this.post('/learning/simulate', params);
  }

  async stressTest(params: any): Promise<any> {
    return this.post('/learning/stress_test', params);
  }
}

// ============================================================
// EXPORT SINGLETON INSTANCE
// ============================================================

export const inksideAPI = new InksideAPI();
export default inksideAPI;
