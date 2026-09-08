import React, { useState, useEffect, useCallback } from 'react';
import { 
  LineChart, 
  Sparkles, 
  TrendingUp, 
  TrendingDown, 
  Target, 
  Play, 
  BarChart2, 
  Activity, 
  Layers, 
  ShieldAlert, 
  AlertCircle, 
  RefreshCw,
  Zap,
  Clock,
  DollarSign,
  Percent,
  ArrowUpRight,
  ArrowDownRight,
  Minus,
  Loader2,
  Wifi,
  WifiOff
} from 'lucide-react';
import { predictionService } from '../services/predictionService';
import { useWebSocketChannel, useWebSocketStatus } from '../contexts/WebSocketContext';

// ============================================================
// TYPES / INTERFACES
// ============================================================

interface Prediction {
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

interface MonteCarloResult {
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

interface SystemMetrics {
  overall_accuracy: number;
  sharpe_ratio: number;
  active_forecasts: number;
  market_regime: string;
  regime_confidence: number;
  last_update: string;
}

// ============================================================
// API SERVICE - PAKAI NGINX PROXY
// ============================================================

const API_BASE = '';

// ============================================================
// MAIN COMPONENT
// ============================================================

export const PredictionView: React.FC = () => {
  const [selectedPair, setSelectedPair] = useState('BTC/USDT');
  const [selectedHorizon, setSelectedHorizon] = useState('1h');
  const [selectedMethod, setSelectedMethod] = useState('ensemble_all');
  
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationRan, setSimulationRan] = useState(false);
  
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [monteCarlo, setMonteCarlo] = useState<MonteCarloResult | null>(null);
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  // ============================================================
  // WEBSOCKET - SOCKET.IO
  // ============================================================
  
  const { isConnected, status } = useWebSocketStatus();

  useWebSocketChannel('predictions', (data) => {
    if (data?.type === 'prediction_update') {
      const payload = data.payload || data.data;
      if (Array.isArray(payload)) {
        setPredictions(payload);
      } else if (payload?.pair) {
        setPredictions(prev => 
          prev.map(p => 
            p.pair === payload.pair ? { ...p, ...payload } : p
          )
        );
      }
      setLastUpdated(new Date());
    }
  });

  useWebSocketChannel('metrics', (data) => {
    if (data?.type === 'system_metrics' || data?.type === 'metrics_update') {
      const payload = data.payload || data.data;
      if (payload) {
        setMetrics(prev => ({
          ...prev,
          ...payload,
          last_update: new Date().toISOString()
        }));
      }
    }
  });

  useWebSocketChannel('monte_carlo', (data) => {
    if (data?.type === 'monte_carlo_update') {
      const payload = data.payload || data.data;
      if (payload) {
        setMonteCarlo(payload);
        setSimulationRan(true);
        setLastUpdated(new Date());
      }
    }
  });

  // ============================================================
  // FETCH DATA - TANPA new URL()
  // ============================================================
  
  const fetchData = useCallback(async () => {
    try {
      setRefreshing(true);
      setError(null);
      
      // 1. Fetch predictions - langsung pakai path relatif
      const predResponse = await predictionService.getPredictions({
        pair: selectedPair,
        horizon: selectedHorizon,
        method: selectedMethod
      });
      
      if (predResponse.success && predResponse.data) {
        setPredictions(predResponse.data);
        setLastUpdated(new Date());
      } else {
        throw new Error(predResponse.error || 'Failed to fetch predictions');
      }

      // 2. Fetch system metrics
      const metricsResponse = await predictionService.getMetrics();
      if (metricsResponse.success && metricsResponse.data) {
        setMetrics(metricsResponse.data);
      }

      // 3. Fetch Monte Carlo if already ran
      if (simulationRan) {
        const mcResponse = await predictionService.getMonteCarlo(selectedPair);
        if (mcResponse.success && mcResponse.data) {
          setMonteCarlo(mcResponse.data);
        }
      }

      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load prediction data');
      setLoading(false);
    } finally {
      setRefreshing(false);
    }
  }, [selectedPair, selectedHorizon, selectedMethod, simulationRan]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // ============================================================
  // HANDLERS
  // ============================================================
  
  const handleRunMonteCarlo = async () => {
    setIsSimulating(true);
    setError(null);
    try {
      const response = await predictionService.runMonteCarlo({
        pair: selectedPair,
        iterations: 1000,
        periods: 30,
        method: selectedMethod
      });
      
      if (response.success && response.data) {
        setMonteCarlo(response.data);
        setSimulationRan(true);
        setLastUpdated(new Date());
      } else {
        setError(response.error || 'Monte Carlo simulation failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Simulation failed');
    } finally {
      setIsSimulating(false);
    }
  };

  const handleRefresh = useCallback(() => {
    fetchData();
  }, [fetchData]);

  const handlePairChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedPair(e.target.value);
  };

  const handleHorizonChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedHorizon(e.target.value);
  };

  // ============================================================
  // RENDER HELPERS
  // ============================================================
  
  const getDirectionIcon = (direction: string) => {
    if (direction === 'UP') {
      return <ArrowUpRight className="w-4 h-4 text-emerald-400" />;
    } else if (direction === 'DOWN') {
      return <ArrowDownRight className="w-4 h-4 text-rose-400" />;
    }
    return <Minus className="w-4 h-4 text-amber-400" />;
  };

  const getDirectionColor = (direction: string) => {
    if (direction === 'UP') return 'text-emerald-400';
    if (direction === 'DOWN') return 'text-rose-400';
    return 'text-amber-400';
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 85) return 'text-emerald-400';
    if (confidence >= 70) return 'text-blue-400';
    if (confidence >= 50) return 'text-amber-400';
    return 'text-rose-400';
  };

  const getRegimeColor = (regime: string) => {
    if (!regime) return 'text-cyan-400';
    const r = regime.toUpperCase();
    if (r.includes('BULL') || r.includes('HIGH_MOMENTUM')) return 'text-emerald-400';
    if (r.includes('BEAR')) return 'text-rose-400';
    if (r.includes('RANGE') || r.includes('CONSOLIDATION')) return 'text-amber-400';
    return 'text-cyan-400';
  };

  // ============================================================
  // LOADING STATE
  // ============================================================
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-500 animate-spin mx-auto" />
          <p className="text-[#8D9AAA] mt-4 font-mono text-sm">Loading prediction data...</p>
          <p className="text-[#5F6B78] text-xs mt-1">Fetching real-time market intelligence</p>
        </div>
      </div>
    );
  }

  // ============================================================
  // ERROR STATE
  // ============================================================
  
  if (error) {
    return (
      <div className="p-6 rounded-2xl bg-red-500/10 border border-red-500/30">
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 rounded-xl bg-red-500/20 flex items-center justify-center flex-shrink-0">
            <AlertCircle className="w-5 h-5 text-red-400" />
          </div>
          <div className="flex-1">
            <h3 className="font-bold text-red-400 text-sm">Error Loading Data</h3>
            <p className="text-sm text-[#8D9AAA] mt-1">{error}</p>
            <div className="flex gap-3 mt-3">
              <button 
                onClick={handleRefresh}
                className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg text-sm text-red-400 transition-colors flex items-center gap-2"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? 'animate-spin' : ''}`} />
                Retry
              </button>
              <button 
                onClick={() => {
                  setError(null);
                  setLoading(true);
                  fetchData();
                }}
                className="px-4 py-2 bg-[#1A2530] hover:bg-[#26313D] rounded-lg text-sm text-white transition-colors"
              >
                Reset View
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ============================================================
  // MAIN RENDER
  // ============================================================
  
  return (
    <div id="prediction-view" className="space-y-6 pb-12">
      
      {/* HEADER BAR */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#131A22] border border-[#26313D]">
            {isConnected ? (
              <Wifi className="w-3.5 h-3.5 text-emerald-400" />
            ) : (
              <WifiOff className="w-3.5 h-3.5 text-amber-400" />
            )}
            <span className={`text-[10px] font-mono font-bold ${isConnected ? 'text-emerald-400' : 'text-amber-400'}`}>
              {isConnected ? 'LIVE' : 'RECONNECTING...'}
            </span>
            <span className="text-[8px] text-[#5F6B78]">({status})</span>
          </div>
          
          {lastUpdated && (
            <span className="text-[10px] text-[#5F6B78] font-mono">
              Updated: {lastUpdated.toLocaleTimeString()}
            </span>
          )}
        </div>
        
        <div className="flex items-center gap-2">
          <button 
            onClick={handleRefresh}
            disabled={refreshing}
            className="p-2 hover:bg-[#1A2530] rounded-lg transition-colors disabled:opacity-50"
            title="Refresh data"
          >
            <RefreshCw className={`w-4 h-4 text-[#8D9AAA] ${refreshing ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* BANNER */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] to-[#1A2530] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <LineChart className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Prediction & Forecasting Engine v4.0
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              {metrics?.last_update 
                ? `Last update: ${new Date(metrics.last_update).toLocaleString()}` 
                : 'Real-time market intelligence'}
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <select
            value={selectedPair}
            onChange={handlePairChange}
            className="px-3 py-2 rounded-xl bg-[#1A2530] border border-[#26313D] text-white text-xs font-mono focus:outline-none focus:border-blue-500/50"
          >
            {predictions.length > 0 ? (
              predictions.map(p => (
                <option key={p.pair} value={p.pair}>{p.pair}</option>
              ))
            ) : (
              <option value="BTC/USDT">BTC/USDT</option>
            )}
          </select>

          <select
            value={selectedHorizon}
            onChange={handleHorizonChange}
            className="px-3 py-2 rounded-xl bg-[#1A2530] border border-[#26313D] text-white text-xs font-mono focus:outline-none focus:border-blue-500/50"
          >
            <option value="5m">5m</option>
            <option value="15m">15m</option>
            <option value="1h">1h</option>
            <option value="4h">4h</option>
            <option value="1d">1d</option>
            <option value="1w">1w</option>
          </select>

          <button
            onClick={handleRunMonteCarlo}
            disabled={isSimulating}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-md shadow-blue-600/30 cursor-pointer disabled:opacity-50 transition-all duration-200"
          >
            {isSimulating ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Play className="w-3.5 h-3.5 fill-current" />
            )}
            <span>{isSimulating ? 'Simulating 1,000 Paths...' : 'Run Monte Carlo'}</span>
          </button>
        </div>
      </div>

      {/* METRICS GRID */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-[#3A4A5A] transition-colors">
          <div className="flex items-center gap-2">
            <Target className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-[10px] uppercase font-bold text-[#8D9AAA]">Accuracy</span>
          </div>
          <span className="text-xl font-bold font-mono text-emerald-400 mt-1 block">
            {metrics?.overall_accuracy ? `${metrics.overall_accuracy}%` : '—'}
          </span>
          <span className="text-[9px] text-[#5F6B78] mt-0.5 block font-mono">
            {predictions.length} active forecasts
          </span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-[#3A4A5A] transition-colors">
          <div className="flex items-center gap-2">
            <Activity className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-[10px] uppercase font-bold text-[#8D9AAA]">Sharpe Ratio</span>
          </div>
          <span className="text-xl font-bold font-mono text-cyan-400 mt-1 block">
            {metrics?.sharpe_ratio ? metrics.sharpe_ratio.toFixed(2) : '—'}
          </span>
          <span className="text-[9px] text-[#5F6B78] mt-0.5 block font-mono">Risk-Adjusted Alpha</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-[#3A4A5A] transition-colors">
          <div className="flex items-center gap-2">
            <Layers className="w-3.5 h-3.5 text-purple-400" />
            <span className="text-[10px] uppercase font-bold text-[#8D9AAA]">Active Forecasts</span>
          </div>
          <span className="text-xl font-bold font-mono text-purple-400 mt-1 block">
            {metrics?.active_forecasts ?? predictions.length}
          </span>
          <span className="text-[9px] text-[#5F6B78] mt-0.5 block font-mono">Multi-timeframe pairs</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] hover:border-[#3A4A5A] transition-colors">
          <div className="flex items-center gap-2">
            <Zap className="w-3.5 h-3.5 text-amber-400" />
            <span className="text-[10px] uppercase font-bold text-[#8D9AAA]">Market Regime</span>
          </div>
          <span className={`text-xl font-bold font-mono mt-1 block ${getRegimeColor(metrics?.market_regime || '')}`}>
            {metrics?.market_regime ?? 'DETECTING...'}
          </span>
          <span className="text-[9px] text-[#5F6B78] mt-0.5 block font-mono">
            Conf: {metrics?.regime_confidence ?? 0}%
          </span>
        </div>
      </div>

      {/* MONTE CARLO RESULTS */}
      {monteCarlo && (
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg animate-in fade-in duration-300">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-white tracking-wider uppercase">
                Monte Carlo Probability Distribution
              </h3>
            </div>
            <span className="text-[10px] text-cyan-400 font-mono font-bold">
              {monteCarlo.iterations} Iterations · {monteCarlo.periods} Periods
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 font-mono text-xs">
            <div className="p-4 rounded-xl bg-[#1A2530] border border-emerald-500/30 space-y-1">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-[10px] uppercase font-bold text-emerald-400">
                  Bullish ({monteCarlo.bullish.probability}% Prob)
                </span>
              </div>
              <div className="text-lg font-bold text-white">
                ${monteCarlo.bullish.price.toLocaleString()}
              </div>
              <div className="text-xs text-emerald-400">
                +{monteCarlo.bullish.change_percent}%
              </div>
              <div className="text-[10px] text-[#8D9AAA] font-sans mt-1">
                {monteCarlo.bullish.description}
              </div>
            </div>

            <div className="p-4 rounded-xl bg-[#1A2530] border border-blue-500/30 space-y-1">
              <div className="flex items-center gap-2">
                <Minus className="w-3.5 h-3.5 text-blue-400" />
                <span className="text-[10px] uppercase font-bold text-blue-400">
                  Base ({monteCarlo.base.probability}% Prob)
                </span>
              </div>
              <div className="text-lg font-bold text-white">
                ${monteCarlo.base.price.toLocaleString()}
              </div>
              <div className="text-xs text-blue-400">
                {monteCarlo.base.change_percent >= 0 ? '+' : ''}{monteCarlo.base.change_percent}%
              </div>
              <div className="text-[10px] text-[#8D9AAA] font-sans mt-1">
                {monteCarlo.base.description}
              </div>
            </div>

            <div className="p-4 rounded-xl bg-[#1A2530] border border-rose-500/30 space-y-1">
              <div className="flex items-center gap-2">
                <TrendingDown className="w-3.5 h-3.5 text-rose-400" />
                <span className="text-[10px] uppercase font-bold text-rose-400">
                  Bearish ({monteCarlo.bearish.probability}% Prob)
                </span>
              </div>
              <div className="text-lg font-bold text-white">
                ${monteCarlo.bearish.price.toLocaleString()}
              </div>
              <div className="text-xs text-rose-400">
                {monteCarlo.bearish.change_percent}%
              </div>
              <div className="text-[10px] text-[#8D9AAA] font-sans mt-1">
                {monteCarlo.bearish.description}
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-[#0B0F14] border border-[#26313D] space-y-2">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-[#8D9AAA]">95% Prediction Interval:</span>
              <span className="text-white font-bold">
                ${monteCarlo.confidence_interval.lower.toLocaleString()} — ${monteCarlo.confidence_interval.upper.toLocaleString()}
                <span className="text-[#5F6B78] font-normal ml-2">
                  (Median: ${monteCarlo.confidence_interval.median.toLocaleString()})
                </span>
              </span>
            </div>
            <div className="w-full h-2 bg-[#1A2530] rounded-full overflow-hidden flex">
              <div className="bg-rose-500/70 h-full w-[25%]" title="Bearish 25%" />
              <div className="bg-blue-500 h-full w-[45%]" title="Base 45%" />
              <div className="bg-emerald-500 h-full w-[30%]" title="Bullish 30%" />
            </div>
            <div className="flex justify-between text-[9px] text-[#5F6B78] font-mono">
              <span>Bearish 25%</span>
              <span>Base 45%</span>
              <span>Bullish 30%</span>
            </div>
          </div>
        </div>
      )}

      {/* PREDICTIONS GRID */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Target className="w-4 h-4 text-blue-400" />
            Real-Time Pair Forecast Matrix
          </h3>
          <span className="text-[10px] text-[#5F6B78] font-mono">
            {predictions.filter(p => p.confidence > 70).length} high-confidence signals
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {predictions.length > 0 ? (
            predictions.map((f) => (
              <div
                key={f.pair}
                className={`p-5 rounded-2xl bg-[#131A22] border ${
                  f.confidence >= 85 
                    ? 'border-emerald-500/40 hover:border-emerald-500/60' 
                    : f.confidence >= 70
                    ? 'border-blue-500/40 hover:border-blue-500/60'
                    : f.confidence >= 50
                    ? 'border-amber-500/40 hover:border-amber-500/60'
                    : 'border-[#26313D] hover:border-[#3A4A5A]'
                } space-y-3 shadow-lg transition-all duration-300 hover:shadow-xl`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="font-mono font-bold text-base text-white">
                      {f.pair}
                    </div>
                    <span className="text-xs font-mono text-[#8D9AAA]">
                      ${f.current_price.toLocaleString()}
                    </span>
                    <span className="text-[9px] text-[#5F6B78] font-mono">
                      {new Date(f.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getDirectionIcon(f.direction)}
                    <span className={`text-xs font-mono font-bold ${getDirectionColor(f.direction)}`}>
                      {f.direction} {f.change_percent}%
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 font-mono text-xs pt-1">
                  <div className="p-2 bg-[#1A2530] rounded-lg">
                    <span className="text-[9px] text-[#5F6B78] block">Confidence</span>
                    <span className={`font-bold ${getConfidenceColor(f.confidence)}`}>
                      {f.confidence}%
                    </span>
                  </div>
                  <div className="p-2 bg-[#1A2530] rounded-lg">
                    <span className="text-[9px] text-[#5F6B78] block">RSI / MACD</span>
                    <span className="font-bold text-white text-[11px]">{f.rsi} · {f.macd}</span>
                  </div>
                  <div className="p-2 bg-[#1A2530] rounded-lg">
                    <span className="text-[9px] text-[#5F6B78] block">Timeframe</span>
                    <span className="font-bold text-cyan-400">{f.timeframe}</span>
                  </div>
                </div>

                <div className="p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D]/60 space-y-1 font-mono text-[11px]">
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">Fibonacci:</span>
                    <span className="text-white">{f.fib_level}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#8D9AAA]">S/R Channel:</span>
                    <span className="text-white">{f.sr_range}</span>
                  </div>
                  <div className="flex justify-between items-center pt-1 border-t border-[#26313D]/40">
                    <span className="text-[#5F6B78] text-[10px] font-sans">
                      Method: {f.method}
                    </span>
                    <span className={`text-[10px] font-bold ${getRegimeColor(f.regime)}`}>
                      {f.regime}
                    </span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-2 p-8 text-center text-[#5F6B78]">
              <p className="text-sm">No predictions available for the selected filters</p>
              <button 
                onClick={handleRefresh}
                className="mt-3 text-blue-400 text-xs hover:underline"
              >
                Refresh data
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PredictionView;
