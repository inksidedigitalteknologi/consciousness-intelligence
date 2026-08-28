// src/components/PatternView.tsx
// INKSIDE DIGITAL - PATTERN VIEW v3.2
// FIX: Error Boundary, Logging, Theme Support, Performance

import React, { useState, useEffect, useCallback, useMemo, memo } from 'react';
import { 
  Search, 
  Sparkles, 
  TrendingUp, 
  TrendingDown, 
  Eye, 
  AlertTriangle, 
  Layers, 
  Filter,
  Wifi,
  WifiOff,
  Loader2,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Clock,
  Zap,
  Shield,
  Brain,
  Activity,
  BarChart3,
  Target,
  Compass,
  Gauge,
  Timer,
  X
} from 'lucide-react';
import { useWebSocketStatus, useWebSocketChannel } from '../contexts/WebSocketContext';
import { inksideAPI } from '../api/inkside';

// ============================================================
// TYPES
// ============================================================

interface PatternItem {
  id: string;
  name: string;
  type: 'CANDLESTICK' | 'HARMONIC' | 'BREAKOUT' | 'CHART' | 'VOLUME' | 'MOMENTUM';
  bias: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
  confidence: number;
  timeframe: string;
  pair: string;
  description: string;
  reliability: number;
  occurrence: number;
  detected_at: string;
  strength: 'STRONG' | 'MODERATE' | 'WEAK';
  volume_confirmation: boolean;
  price: number;
}

interface PatternStats {
  total: number;
  bullish: number;
  bearish: number;
  neutral: number;
  avg_confidence: number;
  top_pair: string;
  last_update: string;
}

interface PatternDetectionResult {
  timestamp: string;
  entities: string[];
  patterns_detected: Array<{
    name: string;
    confidence: number;
    type: string;
  }>;
  dominant_bias: string;
  composite_confidence: number;
  summary: string;
  structure_depth: number;
  novelty_score: string;
}

interface PatternViewProps {
  className?: string;
}

// ============================================================
// LOGGER
// ============================================================

const LOG_PREFIX = '[PatternView]';

const log = {
  info: (message: string, data?: any) => {
    console.info(`${LOG_PREFIX} ${message}`, data || '');
  },
  warn: (message: string, data?: any) => {
    console.warn(`${LOG_PREFIX} ⚠️ ${message}`, data || '');
  },
  error: (message: string, error?: any) => {
    console.error(`${LOG_PREFIX} ❌ ${message}`, error || '');
  },
  debug: (message: string, data?: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`${LOG_PREFIX} ${message}`, data || '');
    }
  }
};

// ============================================================
// ERROR BOUNDARY
// ============================================================

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: React.ErrorInfo | null;
}

class PatternErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: React.ReactNode; fallback?: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    log.error('Error Boundary caught error:', error);
    return { hasError: true, error, errorInfo: null };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    log.error('Component Error:', { error, errorInfo });
    this.setState({ error, errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-6 rounded-2xl bg-rose-500/10 border border-rose-500/30">
          <div className="flex items-center gap-3 text-rose-400">
            <AlertTriangle className="w-5 h-5" />
            <span className="font-bold">PatternView Error</span>
          </div>
          <p className="text-xs text-[#8D9AAA] mt-2">
            {this.state.error?.message || 'Unknown error occurred'}
          </p>
          <button
            onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
            className="mt-3 px-4 py-2 rounded-lg bg-rose-500/20 text-rose-400 text-xs hover:bg-rose-500/30 transition-colors"
          >
            Retry
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// ============================================================
// PATTERN SERVICE
// ============================================================

const API_BASE = import.meta.env.VITE_API_URL || 'http://45.41.204.21';

class PatternService {
  private static instance: PatternService;

  static getInstance(): PatternService {
    if (!PatternService.instance) {
      PatternService.instance = new PatternService();
    }
    return PatternService.instance;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const apiKey = localStorage.getItem('apiKey') || import.meta.env.VITE_API_KEY || '';
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 
        'Content-Type': 'application/json',
        'X-API-Key': apiKey,
      },
      ...options,
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}`);
    }
    return response.json();
  }

  async getPatterns(params?: { pair?: string; bias?: string; type?: string }): Promise<PatternItem[]> {
    const query = new URLSearchParams();
    if (params?.pair && params.pair !== 'ALL') query.append('pair', params.pair);
    if (params?.bias && params.bias !== 'ALL') query.append('bias', params.bias);
    if (params?.type && params.type !== 'ALL') query.append('type', params.type);
    
    try {
      const data = await this.request<{ patterns: PatternItem[] }>(`/api/patterns?${query.toString()}`);
      return data.patterns || [];
    } catch (error) {
      log.error('Failed to fetch patterns:', error);
      return [];
    }
  }

  async getPatternStats(): Promise<PatternStats | null> {
    try {
      return await this.request<PatternStats>('/api/patterns/stats');
    } catch (error) {
      log.error('Failed to fetch pattern stats:', error);
      return null;
    }
  }

  async detectPatterns(text: string): Promise<PatternDetectionResult | null> {
    try {
      return await this.request<PatternDetectionResult>('/api/patterns/detect', {
        method: 'POST',
        body: JSON.stringify({ text }),
      });
    } catch (error) {
      log.error('Pattern detection failed:', error);
      return null;
    }
  }
}

const patternService = PatternService.getInstance();

// ============================================================
// HELPERS
// ============================================================

const getBiasColor = (bias: string): string => {
  if (bias === 'BULLISH') return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20';
  if (bias === 'BEARISH') return 'bg-rose-500/20 text-rose-400 border-rose-500/20';
  return 'bg-amber-500/20 text-amber-400 border-amber-500/20';
};

const getBiasIcon = (bias: string) => {
  if (bias === 'BULLISH') return <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />;
  if (bias === 'BEARISH') return <TrendingDown className="w-3.5 h-3.5 text-rose-400" />;
  return <MinusIcon className="w-3.5 h-3.5 text-amber-400" />;
};

const getConfidenceColor = (confidence: number): string => {
  if (confidence >= 80) return 'text-emerald-400';
  if (confidence >= 60) return 'text-blue-400';
  if (confidence >= 40) return 'text-amber-400';
  return 'text-rose-400';
};

const getStrengthBadge = (strength: string): string => {
  if (strength === 'STRONG') return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
  if (strength === 'MODERATE') return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
  return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
};

// ============================================================
// SUB-COMPONENTS
// ============================================================

const MinusIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const MetricCard = memo(({ 
  label, 
  value, 
  sub, 
  color = 'text-white',
  icon: Icon 
}: { 
  label: string; 
  value: React.ReactNode; 
  sub?: string; 
  color?: string;
  icon?: React.ElementType;
}) => (
  <div className="p-4 rounded-xl bg-[var(--bg-card)] border border-[var(--border-primary)] hover:border-[#3A4A5A] transition-all duration-300">
    <span className="text-[10px] uppercase font-bold text-[var(--text-muted)] block">{label}</span>
    <span className={`text-xl font-bold font-mono mt-1 block ${color}`}>{value}</span>
    {sub && <span className="text-[10px] text-[var(--text-muted)] mt-1 block font-mono">{sub}</span>}
  </div>
));

MetricCard.displayName = 'MetricCard';

// ============================================================
// MAIN COMPONENT
// ============================================================

export const PatternView: React.FC<PatternViewProps> = ({ className = '' }) => {
  // ============================================================
  // WEBSOCKET
  // ============================================================
  
  const { isConnected, status } = useWebSocketStatus();

  useWebSocketChannel('patterns', (data) => {
    if (data?.type === 'pattern_update') {
      setPatterns(prev => {
        const existing = prev.findIndex(p => p.id === data.payload.id);
        if (existing >= 0) {
          const newPatterns = [...prev];
          newPatterns[existing] = data.payload;
          return newPatterns;
        }
        return [data.payload, ...prev].slice(0, 50);
      });
      setLastUpdate(new Date().toLocaleTimeString());
      log.debug('Pattern update received');
    }
    if (data?.type === 'pattern_stats') {
      setStats(data.payload);
    }
  });

  // ============================================================
  // STATE
  // ============================================================
  
  const [patterns, setPatterns] = useState<PatternItem[]>([]);
  const [stats, setStats] = useState<PatternStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [isRefreshing, setIsRefreshing] = useState(false);
  
  const [selectedPair, setSelectedPair] = useState('ALL');
  const [selectedBias, setSelectedBias] = useState('ALL');
  const [selectedType, setSelectedType] = useState('ALL');
  
  const [testInput, setTestInput] = useState('');
  const [testResults, setTestResults] = useState<PatternDetectionResult | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [localError, setLocalError] = useState<string | null>(null);

  // ============================================================
  // LOGGING
  // ============================================================
  
  useEffect(() => {
    log.info('PatternView mounted', { 
      patterns: patterns.length, 
      isConnected,
      autoRefresh 
    });
    return () => {
      log.debug('PatternView unmounted');
    };
  }, []);

  // ============================================================
  // FETCH DATA
  // ============================================================

  const fetchPatterns = useCallback(async (showRefresh: boolean = false) => {
    try {
      if (showRefresh) {
        setIsRefreshing(true);
      } else {
        setLoading(true);
      }
      setError(null);
      setLocalError(null);

      log.debug('Fetching patterns...', { selectedPair, selectedBias, selectedType });

      const [patternsData, statsData] = await Promise.all([
        patternService.getPatterns({
          pair: selectedPair,
          bias: selectedBias,
          type: selectedType,
        }),
        patternService.getPatternStats(),
      ]);

      setPatterns(patternsData);
      setStats(statsData);
      setLastUpdate(new Date().toLocaleTimeString());
      log.debug('Patterns fetched successfully', { count: patternsData.length });

    } catch (err) {
      log.error('Failed to fetch patterns:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch pattern data');
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  }, [selectedPair, selectedBias, selectedType]);

  // ============================================================
  // EFFECTS
  // ============================================================

  useEffect(() => {
    fetchPatterns(false);
    
    if (autoRefresh) {
      const interval = setInterval(() => {
        fetchPatterns(true);
      }, 60000);
      return () => clearInterval(interval);
    }
  }, [fetchPatterns, autoRefresh]);

  // ============================================================
  // HANDLERS
  // ============================================================

  const handleDetectPattern = useCallback(async () => {
    if (!testInput.trim()) {
      setLocalError('Please enter a market observation.');
      return;
    }
    
    setIsScanning(true);
    setLocalError(null);
    
    try {
      log.info('Detecting patterns from input:', testInput);
      const result = await patternService.detectPatterns(testInput);
      if (result) {
        setTestResults(result);
        log.debug('Pattern detection successful', { patterns: result.patterns_detected.length });
      } else {
        setLocalError('No patterns detected. Try a different description.');
      }
    } catch (err) {
      log.error('Pattern detection failed:', err);
      setLocalError('Pattern detection failed. Please try again.');
    } finally {
      setIsScanning(false);
    }
  }, [testInput]);

  const handleRefresh = useCallback(() => {
    log.info('Manual refresh triggered');
    fetchPatterns(true);
  }, [fetchPatterns]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleDetectPattern();
    }
  }, [handleDetectPattern]);

  const toggleAutoRefresh = useCallback(() => {
    setAutoRefresh(prev => !prev);
    log.info(`Auto-refresh ${autoRefresh ? 'disabled' : 'enabled'}`);
  }, [autoRefresh]);

  // ============================================================
  // MEMOIZED VALUES
  // ============================================================

  const filteredPatterns = useMemo(() => {
    return patterns.filter(p => {
      if (selectedPair !== 'ALL' && p.pair !== selectedPair) return false;
      if (selectedBias !== 'ALL' && p.bias !== selectedBias) return false;
      if (selectedType !== 'ALL' && p.type !== selectedType) return false;
      return true;
    });
  }, [patterns, selectedPair, selectedBias, selectedType]);

  const bullishRatio = useMemo(() => {
    if (!patterns.length) return '0%';
    const bullish = patterns.filter(p => p.bias === 'BULLISH').length;
    return `${Math.round((bullish / patterns.length) * 100)}%`;
  }, [patterns]);

  const avgConfidence = useMemo(() => {
    if (!patterns.length) return 0;
    return Math.round(patterns.reduce((acc, p) => acc + p.confidence, 0) / patterns.length);
  }, [patterns]);

  const uniquePairs = useMemo(() => {
    return ['ALL', ...new Set(patterns.map(p => p.pair))];
  }, [patterns]);

  // ============================================================
  // LOADING STATE
  // ============================================================

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 bg-[var(--bg-primary)]">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-purple-500 animate-spin mx-auto" />
          <p className="text-[var(--text-tertiary)] mt-4 text-sm">Loading pattern data...</p>
          <p className="text-[var(--text-muted)] text-xs mt-1">Fetching real-time patterns</p>
        </div>
      </div>
    );
  }

  // ============================================================
  // ERROR STATE
  // ============================================================

  if (error) {
    return (
      <div className="p-6 rounded-2xl bg-rose-500/10 border border-rose-500/30">
        <div className="flex items-center gap-3 text-rose-400">
          <AlertTriangle className="w-5 h-5" />
          <span className="font-bold">Error:</span>
          <span className="text-sm">{error}</span>
        </div>
        <button
          onClick={handleRefresh}
          className="mt-4 px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded-lg text-white text-sm flex items-center gap-2 transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Retry
        </button>
      </div>
    );
  }

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <PatternErrorBoundary>
      <div id="pattern-view" className={`space-y-6 pb-12 ${className}`}>
        {/* ============================================================
        TOP BANNER
        ============================================================ */}
        <div className="p-5 rounded-2xl bg-gradient-to-r from-[var(--bg-secondary)] to-[var(--bg-tertiary)] border border-[var(--border-primary)] shadow-lg">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
                <Search className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-[var(--text-primary)] tracking-wide flex items-center gap-2 flex-wrap">
                  Pattern Recognition Engine v3.2
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/30">
                    {patterns.length} ACTIVE
                  </span>
                </h2>
                <p className="text-xs text-[var(--text-tertiary)] flex items-center gap-2 flex-wrap">
                  30+ Candlestick, Harmonic Wave & Structural Pattern Detectors
                  {isConnected ? (
                    <Wifi className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <WifiOff className="w-3.5 h-3.5 text-amber-400" />
                  )}
                  <span className="text-[var(--text-muted)]">•</span>
                  <span className="text-[var(--text-muted)]">Last update: {lastUpdate}</span>
                  {isRefreshing && (
                    <>
                      <span className="text-[var(--text-muted)]">•</span>
                      <span className="text-cyan-400 animate-pulse flex items-center gap-1">
                        <Loader2 className="w-3 h-3 animate-spin" />
                        Updating...
                      </span>
                    </>
                  )}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 flex-wrap">
              <button
                onClick={toggleAutoRefresh}
                className={`px-3 py-1.5 rounded-lg text-xs transition flex items-center gap-1 ${
                  autoRefresh
                    ? 'bg-blue-600 hover:bg-blue-700 text-white'
                    : 'bg-[var(--bg-tertiary)] hover:bg-[var(--border-primary)] text-[var(--text-tertiary)]'
                }`}
                aria-label={autoRefresh ? 'Disable auto-refresh' : 'Enable auto-refresh'}
              >
                {autoRefresh ? '⏸️ 60s' : '▶️ Manual'}
              </button>
              <button
                onClick={handleRefresh}
                disabled={isRefreshing}
                className="px-3 py-1.5 bg-[var(--bg-tertiary)] hover:bg-[var(--border-primary)] rounded-lg transition text-xs flex items-center gap-1 text-[var(--text-primary)] disabled:opacity-50"
                aria-label="Refresh patterns"
              >
                <RefreshCw className={`w-3 h-3 ${isRefreshing ? 'animate-spin' : ''}`} />
                Refresh
              </button>
            </div>
          </div>

          {/* Error Display */}
          {(localError) && (
            <div className="mt-3 p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" />
              {localError}
              <button
                onClick={() => setLocalError(null)}
                className="ml-auto text-rose-400/70 hover:text-rose-400"
                aria-label="Dismiss error"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>

        {/* ============================================================
        METRICS ROW
        ============================================================ */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
          <MetricCard
            label="Active Patterns"
            value={`${patterns.length} Formations`}
            sub="Real-time Feed"
            color="text-white"
          />
          <MetricCard
            label="Avg Confidence"
            value={`${avgConfidence}%`}
            sub="Calibrated via Evaluator"
            color={getConfidenceColor(avgConfidence)}
          />
          <MetricCard
            label="Bullish / Bearish"
            value={`${bullishRatio} / ${100 - parseInt(bullishRatio)}%`}
            sub={`${patterns.filter(p => p.bias === 'BULLISH').length} Bullish`}
            color="text-blue-400"
          />
          <MetricCard
            label="Top Pair"
            value={stats?.top_pair || 'N/A'}
            sub="Highest Activity"
            color="text-purple-400"
          />
        </div>

        {/* ============================================================
        PATTERN DETECTION SANDBOX
        ============================================================ */}
        <div className="p-5 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-primary)] shadow-lg">
          <div className="flex items-center justify-between pb-3 border-b border-[var(--border-secondary)]">
            <h3 className="text-sm font-bold text-[var(--text-primary)] tracking-wider uppercase flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400" />
              Pattern Detection Sandbox
            </h3>
            <span className="text-xs text-[var(--text-muted)] font-mono">Real-time Detection</span>
          </div>

          <div className="space-y-3 mt-3">
            <label className="text-xs text-[var(--text-primary)] font-bold block">Market Observation / Pattern Description</label>
            <div className="flex gap-2">
              <input
                type="text"
                value={testInput}
                onChange={(e) => setTestInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="e.g. BTC/USD broke above resistance with high volume and bullish engulfing candle..."
                className="flex-1 px-3.5 py-2.5 rounded-xl bg-[var(--bg-input)] border border-[var(--border-primary)] text-xs text-[var(--text-primary)] font-mono placeholder-[var(--text-muted)] focus:outline-none focus:border-purple-500 transition-colors"
                aria-label="Market observation input"
              />
              <button
                onClick={handleDetectPattern}
                disabled={isScanning || !testInput.trim()}
                className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-md shadow-purple-600/30 flex items-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:scale-105"
                aria-label="Detect patterns"
              >
                {isScanning ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <Search className="w-3.5 h-3.5" />
                )}
                <span>{isScanning ? 'Detecting...' : 'Detect Patterns'}</span>
              </button>
            </div>

            {testResults && (
              <div className="p-4 rounded-xl bg-[var(--bg-input)] border border-purple-500/30 space-y-3 font-mono text-xs animate-in fade-in duration-300">
                <div className="flex items-center justify-between">
                  <span className="text-purple-400 font-bold">DETECTION RESULTS:</span>
                  <span className="text-[10px] text-[var(--text-muted)]">{testResults.timestamp}</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  <div className="p-2.5 rounded-lg bg-[var(--bg-card)] border border-[var(--border-primary)]">
                    <div className="text-[10px] text-[var(--text-tertiary)]">Dominant Bias</div>
                    <div className={`font-bold mt-0.5 ${testResults.dominant_bias === 'BULLISH' ? 'text-emerald-400' : testResults.dominant_bias === 'BEARISH' ? 'text-rose-400' : 'text-amber-400'}`}>
                      {testResults.dominant_bias}
                    </div>
                  </div>
                  <div className="p-2.5 rounded-lg bg-[var(--bg-card)] border border-[var(--border-primary)]">
                    <div className="text-[10px] text-[var(--text-tertiary)]">Composite Confidence</div>
                    <div className="text-[var(--text-primary)] font-bold mt-0.5">{testResults.composite_confidence}%</div>
                  </div>
                  <div className="p-2.5 rounded-lg bg-[var(--bg-card)] border border-[var(--border-primary)]">
                    <div className="text-[10px] text-[var(--text-tertiary)]">Novelty Score</div>
                    <div className="text-blue-400 font-bold mt-0.5 text-[10px]">{testResults.novelty_score}</div>
                  </div>
                </div>

                <div>
                  <div className="text-[11px] font-bold text-[var(--text-primary)] mb-1.5">Detected Patterns:</div>
                  <div className="space-y-1.5">
                    {testResults.patterns_detected.map((p, idx) => (
                      <div key={idx} className="flex items-center justify-between p-2 rounded-lg bg-[var(--bg-card)] border border-[var(--border-secondary)] text-xs">
                        <span className="text-[var(--text-primary)]">{p.name} ({p.type})</span>
                        <span className="text-emerald-400 font-bold">{p.confidence}%</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="text-[11px] text-[var(--text-tertiary)] font-sans bg-[var(--bg-card)] p-2.5 rounded-lg border border-[var(--border-secondary)]">
                  {testResults.summary}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* ============================================================
        PATTERNS LIST
        ============================================================ */}
        <div className="p-5 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-primary)] shadow-lg">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[var(--border-secondary)]">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-purple-400" />
              <h3 className="text-sm font-bold text-[var(--text-primary)] tracking-wider uppercase">
                Active Patterns ({filteredPatterns.length})
              </h3>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <select
                value={selectedPair}
                onChange={(e) => setSelectedPair(e.target.value)}
                className="px-2.5 py-1 rounded-lg bg-[var(--bg-input)] border border-[var(--border-primary)] text-xs text-[var(--text-primary)] focus:outline-none focus:border-purple-500 transition-colors"
                aria-label="Filter by pair"
              >
                <option value="ALL">All Pairs</option>
                {uniquePairs.filter(p => p !== 'ALL').map(pair => (
                  <option key={pair} value={pair}>{pair}</option>
                ))}
              </select>

              <select
                value={selectedBias}
                onChange={(e) => setSelectedBias(e.target.value)}
                className="px-2.5 py-1 rounded-lg bg-[var(--bg-input)] border border-[var(--border-primary)] text-xs text-[var(--text-primary)] focus:outline-none focus:border-purple-500 transition-colors"
                aria-label="Filter by bias"
              >
                <option value="ALL">All Biases</option>
                <option value="BULLISH">🟢 Bullish</option>
                <option value="BEARISH">🔴 Bearish</option>
                <option value="NEUTRAL">🟡 Neutral</option>
              </select>

              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="px-2.5 py-1 rounded-lg bg-[var(--bg-input)] border border-[var(--border-primary)] text-xs text-[var(--text-primary)] focus:outline-none focus:border-purple-500 transition-colors"
                aria-label="Filter by type"
              >
                <option value="ALL">All Types</option>
                <option value="CANDLESTICK">Candlestick</option>
                <option value="BREAKOUT">Breakout</option>
                <option value="CHART">Chart Pattern</option>
                <option value="MOMENTUM">Momentum</option>
                <option value="VOLUME">Volume</option>
              </select>
            </div>
          </div>

          {filteredPatterns.length === 0 ? (
            <div className="text-center py-12 text-[var(--text-muted)]">
              <div className="text-4xl mb-3">🔍</div>
              <p className="text-sm font-medium">No patterns match your filters</p>
              <p className="text-xs mt-1">Try adjusting your filter settings</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 mt-3">
              {filteredPatterns.map((pattern) => (
                <div
                  key={pattern.id}
                  className="p-4 rounded-xl bg-[var(--bg-tertiary)] border border-[var(--border-primary)] space-y-2.5 hover:border-purple-500/40 transition-all duration-300"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-[var(--text-primary)] text-xs bg-[var(--bg-input)] px-2 py-0.5 rounded border border-[var(--border-primary)]">
                        {pattern.pair}
                      </span>
                      <span className="font-bold text-[var(--text-primary)] text-sm">{pattern.name}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      {getBiasIcon(pattern.bias)}
                      <span className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded border ${getBiasColor(pattern.bias)}`}>
                        {pattern.bias} · {pattern.timeframe}
                      </span>
                    </div>
                  </div>

                  <p className="text-xs text-[var(--text-tertiary)] leading-relaxed">{pattern.description}</p>

                  <div className="pt-2 border-t border-[var(--border-secondary)] flex items-center justify-between font-mono text-[11px] flex-wrap gap-2">
                    <span className="text-[var(--text-muted)] flex items-center gap-1">
                      <span className={`px-1.5 py-0.5 rounded text-[9px] ${getStrengthBadge(pattern.strength)}`}>
                        {pattern.strength}
                      </span>
                    </span>
                    <div className="flex items-center gap-3">
                      <span className="text-[var(--text-tertiary)] flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {new Date(pattern.detected_at).toLocaleTimeString()}
                      </span>
                      <span className="text-emerald-400 font-bold">
                        {pattern.confidence}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ============================================================
        FOOTER
        ============================================================ */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-[9px] text-[var(--text-muted)] border-t border-[var(--border-secondary)] pt-4">
          <div className="flex items-center gap-3">
            <span>Pattern View v3.2</span>
            <span className="text-[var(--border-primary)]">|</span>
            <span>Data: 100% REAL</span>
            <span className="text-[var(--border-primary)]">|</span>
            {isConnected ? (
              <span className="text-emerald-400">🟢 Live</span>
            ) : (
              <span className="text-amber-400">🟡 Cached</span>
            )}
          </div>
          <div className="flex items-center gap-3">
            {autoRefresh && <span className="text-cyan-400">Auto-refresh: 60s</span>}
            <span>Last update: {lastUpdate}</span>
            {isConnected ? (
              <Wifi className="w-3 h-3 text-emerald-400" />
            ) : (
              <WifiOff className="w-3 h-3 text-amber-400" />
            )}
          </div>
        </div>
      </div>
    </PatternErrorBoundary>
  );
};

// ============================================================
// EXPORT
// ============================================================

PatternView.displayName = 'PatternView';

export default PatternView;
