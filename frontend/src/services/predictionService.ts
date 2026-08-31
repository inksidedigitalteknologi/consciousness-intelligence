/**
 * Prediction Service - v1.0.0
 * Real-time data integration for PredictionView
 */

const API_BASE = "";
const API_KEY = import.meta.env.VITE_API_KEY || '';

// ============================================================
// TYPES / INTERFACES
// ============================================================

export interface PredictionRequest {
  pair: string;
  horizon: string;
  method: string;
}

export interface MonteCarloRequest {
  pair: string;
  iterations: number;
  periods: number;
  method: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp?: string;
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

export interface SystemMetrics {
  overall_accuracy: number;
  sharpe_ratio: number;
  active_forecasts: number;
  market_regime: string;
  regime_confidence: number;
  last_update: string;
}

export interface MonteCarloResult {
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

// ============================================================
// HELPER FUNCTIONS
// ============================================================

const getHeaders = () => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  // API Key dari localStorage atau env
  const apiKey = localStorage.getItem('apiKey') || API_KEY;
  if (apiKey) {
    headers['X-API-Key'] = apiKey;
  }
  
  return headers;
};

const handleResponse = async <T>(response: Response): Promise<ApiResponse<T>> => {
  try {
    if (!response.ok) {
      const errorText = await response.text();
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      
      try {
        const errorJson = JSON.parse(errorText);
        if (errorJson.error) {
          errorMessage = errorJson.error;
        }
      } catch {
        // Jika response bukan JSON, gunakan text
        if (errorText) {
          errorMessage = errorText;
        }
      }
      
      return {
        success: false,
        error: errorMessage,
        timestamp: new Date().toISOString(),
      };
    }
    
    const data = await response.json();
    return {
      success: true,
      data: data as T,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred',
      timestamp: new Date().toISOString(),
    };
  }
};

// ============================================================
// PREDICTION SERVICE
// ============================================================

export const predictionService = {
  /**
   * Get predictions for a specific pair
   */
  async getPredictions(params: PredictionRequest): Promise<ApiResponse<Prediction[]>> {
    try {
      const url = new URL(`${API_BASE}/predictions`);
      url.searchParams.append('pair', params.pair);
      url.searchParams.append('horizon', params.horizon);
      url.searchParams.append('method', params.method);
      
      const response = await fetch(url.toString(), {
        method: 'GET',
        headers: getHeaders(),
      });
      
      return handleResponse<Prediction[]>(response);
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  },

  /**
   * Get system prediction metrics
   */
  async getMetrics(): Promise<ApiResponse<SystemMetrics>> {
    try {
      const response = await fetch(`${API_BASE}/predictions/metrics`, {
        method: 'GET',
        headers: getHeaders(),
      });
      
      return handleResponse<SystemMetrics>(response);
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  },

  /**
   * Run Monte Carlo simulation
   */
  async runMonteCarlo(params: MonteCarloRequest): Promise<ApiResponse<MonteCarloResult>> {
    try {
      const response = await fetch(`${API_BASE}/predictions/monte_carlo`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({
          pair: params.pair,
          iterations: params.iterations || 1000,
          periods: params.periods || 30,
          method: params.method || 'ensemble_all',
        }),
      });
      
      return handleResponse<MonteCarloResult>(response);
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  },

  /**
   * Get cached Monte Carlo results
   */
  async getMonteCarlo(pair: string): Promise<ApiResponse<MonteCarloResult>> {
    try {
      const url = new URL(`${API_BASE}/predictions/monte_carlo`);
      url.searchParams.append('pair', pair);
      
      const response = await fetch(url.toString(), {
        method: 'GET',
        headers: getHeaders(),
      });
      
      return handleResponse<MonteCarloResult>(response);
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  },

  /**
   * Set API Key for authentication
   */
  setApiKey(apiKey: string): void {
    localStorage.setItem('apiKey', apiKey);
  },

  /**
   * Clear API Key
   */
  clearApiKey(): void {
    localStorage.removeItem('apiKey');
  },

  /**
   * Check if API is healthy
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE}/health`, {
        method: 'GET',
        headers: getHeaders(),
      });
      return response.ok;
    } catch {
      return false;
    }
  },
};

export default predictionService;
