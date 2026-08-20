// src/api/inkside.ts
import axios from 'axios';

// ============================================================
// CONFIG
// ============================================================

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://45.41.204.21:5001';

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
        timeout: 5000,
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

  // === STATUS ===
  async getStatus(): Promise<StatusResponse> {
    return this.get<StatusResponse>('/api/status');
  }

  // === SIGNALS ===
  async getSignals(): Promise<SignalsResponse> {
    return this.get<SignalsResponse>('/api/signals');
  }

  // === MARKET DATA ===
  async getMarketData(pair: string = 'BTC/USD'): Promise<MarketDataResponse> {
    return this.get<MarketDataResponse>(`/api/market?pair=${pair}`);
  }

  // === BRAIN STATE ===
  async getBrainState(): Promise<BrainStateResponse> {
    return this.get<BrainStateResponse>('/api/brain/state');
  }

  // === PERFORMANCE ===
  async getPerformance(): Promise<PerformanceResponse> {
    return this.get<PerformanceResponse>('/api/performance');
  }

  // === ANALYZE PAIR ===
  async analyzePair(pair: string): Promise<any> {
    return this.get(`/api/analyze/${pair}`);
  }
}

export const inksideAPI = new InksideAPI();
export default inksideAPI;
