// src/api/inkside.ts
import axios from 'axios';

// ============================================================
// CONFIG
// ============================================================

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://45.41.204.21';

// ============================================================
// TYPES
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
    modules?: {
      brain: string;
      scanner: string;
      learning: string;
      exchange: string;
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

// ============================================================
// API CLASS
// ============================================================

class InksideAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async get<T>(endpoint: string): Promise<T> {
    try {
      const response = await axios.get<T>(`${this.baseUrl}${endpoint}`, {
        timeout: 10000,
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.data;
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  private async post<T>(endpoint: string, data?: any): Promise<T> {
    try {
      const response = await axios.post<T>(`${this.baseUrl}${endpoint}`, data, {
        timeout: 10000,
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.data;
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  // ============================================================
  // API METHODS
  // ============================================================

  // Status
  async getStatus(): Promise<StatusResponse> {
    return this.get<StatusResponse>('/api/status');
  }

  // Health
  async getHealth(): Promise<{ status: string; uptime: number; timestamp: string }> {
    return this.get<{ status: string; uptime: number; timestamp: string }>('/api/health');
  }

  // Signals
  async getSignals(): Promise<SignalsResponse> {
    return this.get<SignalsResponse>('/api/signals');
  }

  // Market Data
  async getMarketData(pair: string = 'BTC/USD'): Promise<MarketDataResponse> {
    return this.get<MarketDataResponse>(`/api/market?pair=${encodeURIComponent(pair)}`);
  }

  // Analyze Pair
  async analyzePair(pair: string): Promise<any> {
    return this.get(`/api/analyze/${encodeURIComponent(pair)}`);
  }

  // Brain State
  async getBrainState(): Promise<BrainStateResponse> {
    return this.get<BrainStateResponse>('/api/brain/state');
  }

  // Brain Reflection
  async getBrainReflection(): Promise<ReflectionResponse> {
    return this.get<ReflectionResponse>('/api/brain/reflection');
  }

  // Performance
  async getPerformance(): Promise<PerformanceResponse> {
    return this.get<PerformanceResponse>('/api/performance');
  }

  // Positions
  async getPositions(): Promise<PositionsResponse> {
    return this.get<PositionsResponse>('/api/positions');
  }

  // Logs
  async getLogs(limit: number = 50): Promise<LogsResponse> {
    return this.get<LogsResponse>(`/api/logs?limit=${limit}`);
  }

  // Diagnostics
  async getDiagnostics(): Promise<DiagnosticsResponse> {
    return this.get<DiagnosticsResponse>('/api/diagnostics');
  }

  // Telegram Status
  async getTelegramStatus(): Promise<TelegramStatusResponse> {
    return this.get<TelegramStatusResponse>('/api/telegram/status');
  }

  // Engine Control
  async startEngine(): Promise<{ status: string; success: boolean; timestamp: string }> {
    return this.post<{ status: string; success: boolean; timestamp: string }>('/api/engine/start');
  }

  async stopEngine(): Promise<{ status: string; success: boolean; timestamp: string }> {
    return this.post<{ status: string; success: boolean; timestamp: string }>('/api/engine/stop');
  }

  // Learning Status
  async getLearningStatus(): Promise<{ learning: { active: boolean; cycles: number; status: string }; timestamp: string }> {
    return this.get<{ learning: { active: boolean; cycles: number; status: string }; timestamp: string }>('/api/learning/status');
  }
}

// ============================================================
// EXPORT
// ============================================================

export const inksideAPI = new InksideAPI();
export default inksideAPI;
