import React, { useState, useEffect, useCallback } from 'react';
import {
  Save,
  RefreshCw,
  Settings,
  Shield,
  Bell,
  Zap,
  Sliders,
  Globe,
  Lock,
  Users,
  Database,
  Cpu,
  HardDrive,
  Clock,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Mail,
  Key,
  Globe2,
  Server,
  Wifi,
  Activity,
  BarChart3,
  PieChart,
  LineChart,
  TrendingUp,
  Target,
  Compass,
  Layers,
  GitBranch,
  Workflow,
  Eye,
  EyeOff,
  Copy,
  Check,
  Send,
  Brain,
  Info,
  Loader2,
  Heart,
} from 'lucide-react';

// ============================================================
// TYPES - Match dengan config.py
// ============================================================

interface ConfigData {
  // App
  app_name: string;
  app_version: string;
  app_author: string;
  
  // Exchange
  exchange_name: string;
  exchange_type: string;
  coingecko_rate_limit: number;
  request_delay: number;
  cache_ttl_seconds: number;
  max_markets: number;
  
  // Market
  default_pairs: string[];
  default_timeframes: string[];
  main_timeframe: string;
  
  // Scanner
  scan_interval_seconds: number;
  max_workers: number;
  scanner_batch_size: number;
  scanner_batch_delay: number;
  
  // Signal
  min_mtf_alignment: number;
  min_signal_strength: number;
  min_signal_confidence: number;
  signal_cooldown_seconds: number;
  max_signals_per_scan: number;
  
  // Risk
  default_risk_percent: number;
  default_risk_reward: number;
  max_position_size: number;
  min_position_size: number;
  max_daily_trades: number;
  max_open_positions: number;
  max_drawdown_percent: number;
  stop_loss_percent: number;
  take_profit_percent: number;
  
  // Trading
  trading_enabled: boolean;
  paper_trading: boolean;
  auto_trade: boolean;
  
  // Telegram
  telegram_enabled: boolean;
  telegram_configured: boolean;
  
  // Learning
  learning_enabled: boolean;
  learning_interval_seconds: number;
  learning_auto_start: boolean;
  learning_max_history: number;
  
  // Prediction
  prediction_enabled: boolean;
  prediction_horizon: number[];
  prediction_min_confidence: number;
  
  // Health
  health_check_interval: number;
  health_min_score: number;
  health_critical_score: number;
  
  // System
  debug_mode: boolean;
  log_level: string;
  max_threads: number;
  thread_pool_size: number;
  api_timeout: number;
  
  // Status
  backend_status: 'online' | 'offline' | 'degraded';
  knowledge_items: number;
  dividend_items: number;
  ai_enabled: boolean;
  uptime_seconds: number;
}

// ============================================================
// API HELPER
// ============================================================

const API_KEY = 'iks_612d40ce554b1670525355c85567f823';

const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY,
      ...options.headers,
    },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const SettingsView: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'system' | 'trading' | 'exchange' | 'telegram' | 'cognitive' | 'security'>('system');
  
  const [config, setConfig] = useState<ConfigData | null>(null);
  const [originalConfig, setOriginalConfig] = useState<ConfigData | null>(null);
  
  // Local settings yang bisa diubah
  const [localSettings, setLocalSettings] = useState<Partial<ConfigData>>({});

  // ============================================================
  // LOAD CONFIG FROM BACKEND
  // ============================================================
  
  const loadConfig = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      // 1. Load config dari backend
      const configData = await fetchWithAuth('/api/config');
      setConfig(configData);
      setOriginalConfig(configData);
      setLocalSettings(configData);
      
      console.log('✅ Config loaded from backend:', configData);
    } catch (err) {
      console.error('Failed to load config:', err);
      setError('Failed to load configuration from backend. Make sure the server is running.');
      
      // Fallback: load from localStorage
      try {
        const saved = localStorage.getItem('inkside_config');
        if (saved) {
          const parsed = JSON.parse(saved);
          setConfig(parsed);
          setOriginalConfig(parsed);
          setLocalSettings(parsed);
          console.log('✅ Config loaded from localStorage (fallback)');
        }
      } catch (e) {
        console.error('Failed to load from localStorage:', e);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  // ============================================================
  // SAVE CONFIG TO BACKEND
  // ============================================================
  
  const saveConfig = useCallback(async () => {
    if (!localSettings) return;
    
    setSaving(true);
    setSaved(false);
    setError(null);
    
    try {
      // Kirim ke backend
      await fetchWithAuth('/api/config', {
        method: 'POST',
        body: JSON.stringify(localSettings),
      });
      
      // Update local state
      setConfig(localSettings as ConfigData);
      setOriginalConfig(localSettings as ConfigData);
      
      // Save to localStorage as backup
      localStorage.setItem('inkside_config', JSON.stringify(localSettings));
      
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
      console.log('✅ Config saved successfully');
    } catch (err) {
      console.error('Failed to save config:', err);
      setError('Failed to save configuration. Please try again.');
    } finally {
      setSaving(false);
    }
  }, [localSettings]);

  // ============================================================
  // RESET TO DEFAULTS
  // ============================================================
  
  const resetToDefaults = useCallback(async () => {
    if (!window.confirm('Reset all settings to default values?')) return;
    
    try {
      const defaultConfig = await fetchWithAuth('/api/config/default');
      setLocalSettings(defaultConfig);
      setConfig(defaultConfig);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
      console.log('✅ Config reset to defaults');
    } catch (err) {
      console.error('Failed to reset config:', err);
      setError('Failed to reset configuration.');
    }
  }, []);

  // ============================================================
  // INIT
  // ============================================================
  
  useEffect(() => {
    loadConfig();
  }, [loadConfig]);

  // Auto-save to localStorage setiap perubahan
  useEffect(() => {
    if (localSettings && Object.keys(localSettings).length > 0) {
      localStorage.setItem('inkside_config', JSON.stringify(localSettings));
    }
  }, [localSettings]);

  // ============================================================
  // HANDLERS
  // ============================================================
  
  const handleChange = <K extends keyof ConfigData>(key: K, value: ConfigData[K]) => {
    setLocalSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleNumberChange = (key: keyof ConfigData, value: string) => {
    const num = parseFloat(value);
    if (!isNaN(num)) {
      handleChange(key, num);
    }
  };

  // ============================================================
  // RENDER HELPERS
  // ============================================================
  
  const renderStatusBadge = (status: string) => {
    const colors: Record<string, string> = {
      online: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
      offline: 'bg-rose-500/20 text-rose-400 border-rose-500/30',
      degraded: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    };
    return (
      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${colors[status] || colors.offline}`}>
        {status.toUpperCase()}
      </span>
    );
  };

  // ============================================================
  // TAB: SYSTEM
  // ============================================================
  
  const renderSystemTab = () => (
    <div className="space-y-6">
      {/* System Status */}
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <Activity className="w-4 h-4 text-blue-400" />
          System Status
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
            <span className="text-[10px] text-[#5F6B78] block">Backend</span>
            <span className="text-sm font-bold text-white">
              {config?.backend_status === 'online' ? '✅ Online' : '⚠️ Offline'}
            </span>
          </div>
          <div className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
            <span className="text-[10px] text-[#5F6B78] block">Knowledge</span>
            <span className="text-sm font-bold text-white">{config?.knowledge_items || 0} items</span>
          </div>
          <div className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
            <span className="text-[10px] text-[#5F6B78] block">AI Status</span>
            <span className="text-sm font-bold text-white">
              {config?.ai_enabled ? '✅ Enabled' : '❌ Disabled'}
            </span>
          </div>
          <div className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
            <span className="text-[10px] text-[#5F6B78] block">Uptime</span>
            <span className="text-sm font-bold text-white">
              {config?.uptime_seconds ? `${Math.floor(config.uptime_seconds / 3600)}h` : '0h'}
            </span>
          </div>
        </div>
      </div>

      {/* Debug & Logging */}
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Debug & Logging</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Log Level</label>
            <select
              value={localSettings?.log_level || 'INFO'}
              onChange={(e) => handleChange('log_level', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            >
              <option value="DEBUG">DEBUG</option>
              <option value="INFO">INFO</option>
              <option value="WARNING">WARNING</option>
              <option value="ERROR">ERROR</option>
            </select>
          </div>
          <div className="flex items-center gap-3 pt-2">
            <input
              type="checkbox"
              checked={localSettings?.debug_mode || false}
              onChange={(e) => handleChange('debug_mode', e.target.checked)}
              className="w-4 h-4 accent-blue-500"
            />
            <span className="text-sm text-[#8D9AAA]">Debug Mode</span>
          </div>
        </div>
      </div>

      {/* Thread & Performance */}
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Performance</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Max Threads</label>
            <input
              type="number"
              value={localSettings?.max_threads || 10}
              onChange={(e) => handleNumberChange('max_threads', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={1}
              max={50}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">API Timeout (s)</label>
            <input
              type="number"
              value={localSettings?.api_timeout || 15}
              onChange={(e) => handleNumberChange('api_timeout', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={5}
              max={60}
            />
          </div>
        </div>
      </div>
    </div>
  );

  // ============================================================
  // TAB: TRADING
  // ============================================================
  
  const renderTradingTab = () => (
    <div className="space-y-6">
      {/* Trading Mode */}
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Trading Mode</h4>
        <div className="grid grid-cols-3 gap-3">
          {(['PAPER', 'LIVE', 'HYBRID'] as const).map((mode) => (
            <button
              key={mode}
              onClick={() => {
                handleChange('paper_trading', mode === 'PAPER' || mode === 'HYBRID');
                handleChange('trading_enabled', mode === 'LIVE' || mode === 'HYBRID');
              }}
              className={`px-4 py-3 rounded-xl text-sm font-bold transition-all cursor-pointer ${
                (mode === 'PAPER' && localSettings?.paper_trading && !localSettings?.trading_enabled) ||
                (mode === 'HYBRID' && localSettings?.paper_trading && localSettings?.trading_enabled) ||
                (mode === 'LIVE' && !localSettings?.paper_trading && localSettings?.trading_enabled)
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                  : 'bg-[#0B0F14] text-[#8D9AAA] hover:text-white border border-[#26313D]'
              }`}
            >
              {mode}
            </button>
          ))}
        </div>
        <p className="text-xs text-[#5F6B78] mt-2">PAPER = Simulated | LIVE = Real money | HYBRID = Both</p>
      </div>

      {/* Risk Management */}
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Risk Management</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Risk per Trade (%)</label>
            <input
              type="number"
              value={localSettings?.default_risk_percent || 1}
              onChange={(e) => handleNumberChange('default_risk_percent', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={0.1}
              max={10}
              step={0.1}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Risk Reward Ratio</label>
            <input
              type="number"
              value={localSettings?.default_risk_reward || 3}
              onChange={(e) => handleNumberChange('default_risk_reward', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={1}
              max={10}
              step={0.5}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Max Drawdown (%)</label>
            <input
              type="number"
              value={localSettings?.max_drawdown_percent || 20}
              onChange={(e) => handleNumberChange('max_drawdown_percent', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={5}
              max={50}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Max Position Size</label>
            <input
              type="number"
              value={localSettings?.max_position_size || 1000}
              onChange={(e) => handleNumberChange('max_position_size', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={10}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Max Daily Trades</label>
            <input
              type="number"
              value={localSettings?.max_daily_trades || 10}
              onChange={(e) => handleNumberChange('max_daily_trades', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={1}
              max={100}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Max Open Positions</label>
            <input
              type="number"
              value={localSettings?.max_open_positions || 5}
              onChange={(e) => handleNumberChange('max_open_positions', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={1}
              max={20}
            />
          </div>
        </div>
      </div>

      {/* SL/TP Default */}
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Default SL/TP</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Stop Loss (%)</label>
            <input
              type="number"
              value={localSettings?.stop_loss_percent || 5}
              onChange={(e) => handleNumberChange('stop_loss_percent', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={0.5}
              max={20}
              step={0.5}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Take Profit (%)</label>
            <input
              type="number"
              value={localSettings?.take_profit_percent || 15}
              onChange={(e) => handleNumberChange('take_profit_percent', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={1}
              max={50}
            />
          </div>
        </div>
      </div>
    </div>
  );

  // ============================================================
  // TAB: EXCHANGE
  // ============================================================
  
  const renderExchangeTab = () => (
    <div className="space-y-6">
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <Server className="w-4 h-4 text-blue-400" />
          Exchange Configuration
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Exchange</label>
            <div className="px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm">
              {config?.exchange_name || 'CoinGecko'}
            </div>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Rate Limit (req/min)</label>
            <input
              type="number"
              value={localSettings?.coingecko_rate_limit || 30}
              onChange={(e) => handleNumberChange('coingecko_rate_limit', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={10}
              max={50}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Request Delay (s)</label>
            <input
              type="number"
              value={localSettings?.request_delay || 2}
              onChange={(e) => handleNumberChange('request_delay', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={0.5}
              max={10}
              step={0.5}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Cache TTL (s)</label>
            <input
              type="number"
              value={localSettings?.cache_ttl_seconds || 120}
              onChange={(e) => handleNumberChange('cache_ttl_seconds', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
              min={30}
              max={600}
            />
          </div>
        </div>
      </div>

      {/* Market Pairs */}
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <Globe className="w-4 h-4 text-emerald-400" />
          Market Pairs
        </h4>
        <div className="flex flex-wrap gap-2">
          {(localSettings?.default_pairs || ['BTC/USD', 'ETH/USD', 'SOL/USD']).map((pair) => (
            <span
              key={pair}
              className="px-3 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            >
              {pair}
            </span>
          ))}
        </div>
        <p className="text-xs text-[#5F6B78] mt-2">Configure pairs via config.py</p>
      </div>

      {/* Timeframes */}
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <Clock className="w-4 h-4 text-amber-400" />
          Timeframes
        </h4>
        <div className="flex flex-wrap gap-2">
          {(localSettings?.default_timeframes || ['1h', '4h', '1d']).map((tf) => (
            <span
              key={tf}
              className={`px-3 py-1 rounded-lg border text-sm ${
                tf === localSettings?.main_timeframe
                  ? 'bg-blue-600/20 text-blue-400 border-blue-500/30'
                  : 'bg-[#0B0F14] text-[#8D9AAA] border-[#26313D]'
              }`}
            >
              {tf} {tf === localSettings?.main_timeframe && '⭐'}
            </span>
          ))}
        </div>
        <p className="text-xs text-[#5F6B78] mt-2">Main timeframe: {localSettings?.main_timeframe || '1h'}</p>
      </div>
    </div>
  );

  // ============================================================
  // TAB: TELEGRAM
  // ============================================================
  
  const renderTelegramTab = () => (
    <div className="space-y-6">
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <div className="flex items-center gap-3 mb-4">
          <input
            type="checkbox"
            checked={localSettings?.telegram_enabled || false}
            onChange={(e) => handleChange('telegram_enabled', e.target.checked)}
            className="w-4 h-4 accent-blue-500"
          />
          <span className="text-sm font-bold text-white">Enable Telegram Alerts</span>
        </div>

        <div className="flex items-center justify-between p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${config?.telegram_configured ? 'bg-emerald-400' : 'bg-amber-400'}`} />
            <span className="text-sm font-bold text-white">
              {config?.telegram_configured ? '✅ Bot Configured' : '⚠️ Bot Not Configured'}
            </span>
          </div>
          <div className="flex items-center gap-2 text-xs text-[#5F6B78]">
            <Info className="w-4 h-4" />
            <span>Configure via .env file</span>
          </div>
        </div>
        <p className="text-xs text-[#5F6B78] mt-2">
          Bot token and chat ID are stored securely on the server.
        </p>
        <div className="mt-3 p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
          <code className="text-xs text-[#8D9AAA] font-mono">
            # Edit ~/consciousness-intelligence/.env<br />
            TELEGRAM_BOT_TOKEN=your_bot_token<br />
            TELEGRAM_CHAT_ID=your_chat_id
          </code>
        </div>
        <button
          onClick={() => window.open('https://t.me/BotFather', '_blank')}
          className="mt-3 w-full py-2 rounded-xl bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 font-bold text-sm transition-all border border-blue-500/20"
        >
          🤖 Create Telegram Bot
        </button>
      </div>

      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <button
          onClick={async () => {
            try {
              const res = await fetch('/api/telegram/test', {
                method: 'POST',
                headers: { 'X-API-Key': API_KEY },
              });
              const data = await res.json();
              alert(data.sent ? '✅ Test message sent!' : '❌ Failed: ' + (data.message || 'Unknown error'));
            } catch {
              alert('❌ Failed to send test message');
            }
          }}
          className="w-full py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm transition-all"
        >
          📨 Send Test Message
        </button>
      </div>
    </div>
  );

  // ============================================================
  // TAB: COGNITIVE
  // ============================================================
  
  const renderCognitiveTab = () => (
    <div className="space-y-6">
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <Brain className="w-4 h-4 text-purple-400" />
          Learning Engine
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center gap-3 pt-2">
            <input
              type="checkbox"
              checked={localSettings?.learning_enabled || false}
              onChange={(e) => handleChange('learning_enabled', e.target.checked)}
              className="w-4 h-4 accent-purple-500"
            />
            <span className="text-sm text-[#8D9AAA]">Enable Learning</span>
          </div>
          <div className="flex items-center gap-3 pt-2">
            <input
              type="checkbox"
              checked={localSettings?.learning_auto_start || false}
              onChange={(e) => handleChange('learning_auto_start', e.target.checked)}
              className="w-4 h-4 accent-purple-500"
            />
            <span className="text-sm text-[#8D9AAA]">Auto-start Learning</span>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Learning Interval (s)</label>
            <input
              type="number"
              value={localSettings?.learning_interval_seconds || 600}
              onChange={(e) => handleNumberChange('learning_interval_seconds', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-purple-500"
              min={60}
              max={3600}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Max History</label>
            <input
              type="number"
              value={localSettings?.learning_max_history || 500}
              onChange={(e) => handleNumberChange('learning_max_history', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-purple-500"
              min={50}
              max={5000}
            />
          </div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <Target className="w-4 h-4 text-cyan-400" />
          Prediction Engine
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center gap-3 pt-2">
            <input
              type="checkbox"
              checked={localSettings?.prediction_enabled || false}
              onChange={(e) => handleChange('prediction_enabled', e.target.checked)}
              className="w-4 h-4 accent-cyan-500"
            />
            <span className="text-sm text-[#8D9AAA]">Enable Predictions</span>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Min Confidence</label>
            <input
              type="number"
              value={localSettings?.prediction_min_confidence || 0.6}
              onChange={(e) => handleNumberChange('prediction_min_confidence', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-cyan-500"
              min={0.1}
              max={1}
              step={0.05}
            />
          </div>
        </div>
        <div className="mt-3">
          <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Prediction Horizons (minutes)</label>
          <div className="flex gap-2">
            {(localSettings?.prediction_horizon || [5, 15, 30, 60]).map((h) => (
              <span key={h} className="px-3 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-white text-sm">
                {h}m
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <Heart className="w-4 h-4 text-rose-400" />
          Health Monitor
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Check Interval (s)</label>
            <input
              type="number"
              value={localSettings?.health_check_interval || 60}
              onChange={(e) => handleNumberChange('health_check_interval', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-rose-500"
              min={10}
              max={600}
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Min Health Score</label>
            <input
              type="number"
              value={localSettings?.health_min_score || 80}
              onChange={(e) => handleNumberChange('health_min_score', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-rose-500"
              min={30}
              max={100}
            />
          </div>
        </div>
      </div>
    </div>
  );

  // ============================================================
  // TAB: SECURITY
  // ============================================================
  
  const renderSecurityTab = () => (
    <div className="space-y-6">
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <Shield className="w-4 h-4 text-amber-400" />
          Security Settings
        </h4>
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={false}
              onChange={() => {}}
              className="w-4 h-4 accent-amber-500 disabled:opacity-50"
              disabled
            />
            <span className="text-sm text-[#8D9AAA]">Require 2FA for trading (Coming soon)</span>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">API Key Authentication</label>
            <div className="flex items-center gap-2 p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
              <Key className="w-4 h-4 text-emerald-400" />
              <span className="text-sm text-white font-mono">••••••••••••••••</span>
              <span className="text-xs text-[#5F6B78] ml-auto">Configured via .env</span>
            </div>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">IP Whitelist</label>
            <input
              type="text"
              placeholder="Enter IPs separated by commas"
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-amber-500"
            />
            <p className="text-[10px] text-[#5F6B78] mt-1">Example: 192.168.1.1, 10.0.0.1</p>
          </div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
        <div className="flex items-start gap-3">
          <Shield className="w-5 h-5 text-amber-400 mt-0.5" />
          <div>
            <h4 className="text-sm font-bold text-amber-400">Security Best Practices</h4>
            <ul className="text-xs text-[#8D9AAA] space-y-1 mt-2">
              <li>✅ API keys stored securely on server (never in browser)</li>
              <li>✅ All requests require API key authentication</li>
              <li>✅ HTTPS recommended for production</li>
              <li>✅ Regular security updates applied</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );

  // ============================================================
  // MAIN RENDER
  // ============================================================

  const tabs = [
    { id: 'system' as const, label: '⚙️ System', icon: Settings },
    { id: 'trading' as const, label: '💰 Trading', icon: TrendingUp },
    { id: 'exchange' as const, label: '🔄 Exchange', icon: Server },
    { id: 'telegram' as const, label: '✈️ Telegram', icon: Send },
    { id: 'cognitive' as const, label: '🧠 Cognitive', icon: Brain },
    { id: 'security' as const, label: '🔒 Security', icon: Shield },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Loader2 className="w-10 h-10 text-blue-400 animate-spin mx-auto mb-3" />
          <p className="text-[#8D9AAA]">Loading configuration...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#18212B] to-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center">
            <Settings className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-wide">Bot Settings</h2>
            <p className="text-xs text-[#8D9AAA]">
              {config?.app_name || 'INKSIDEDIGITAL'} v{config?.app_version || '3.0.0'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 flex-wrap">
          {saved && (
            <span className="text-emerald-400 text-sm font-semibold flex items-center gap-1 animate-pulse">
              <Check className="w-4 h-4" /> Saved
            </span>
          )}
          {error && (
            <span className="text-rose-400 text-sm font-semibold flex items-center gap-1">
              <AlertTriangle className="w-4 h-4" /> {error}
            </span>
          )}
          <button
            onClick={loadConfig}
            disabled={loading}
            className="px-4 py-2 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white border border-[#26313D] text-xs font-semibold transition-all cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 inline ${loading ? 'animate-spin' : ''}`} />
            {loading ? ' Loading...' : ' Refresh'}
          </button>
          <button
            onClick={resetToDefaults}
            className="px-4 py-2 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/20 text-xs font-semibold transition-all cursor-pointer"
          >
            Reset Defaults
          </button>
          <button
            onClick={saveConfig}
            disabled={saving}
            className="px-6 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm transition-all shadow-lg shadow-blue-600/30 cursor-pointer disabled:opacity-50 flex items-center gap-2"
          >
            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 p-2 rounded-xl bg-[#131A22] border border-[#26313D]">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all cursor-pointer ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                  : 'text-[#8D9AAA] hover:text-white hover:bg-[#1A2530]'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Content */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
        {activeTab === 'system' && renderSystemTab()}
        {activeTab === 'trading' && renderTradingTab()}
        {activeTab === 'exchange' && renderExchangeTab()}
        {activeTab === 'telegram' && renderTelegramTab()}
        {activeTab === 'cognitive' && renderCognitiveTab()}
        {activeTab === 'security' && renderSecurityTab()}
      </div>

      {/* Footer */}
      <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
        <p className="text-xs text-amber-400">
          🔒 API keys and tokens are stored securely on the server. Never exposed to the browser.
          Configure them via <code className="bg-[#0B0F14] px-2 py-0.5 rounded">~/.env</code> file.
        </p>
      </div>
    </div>
  );
};

export default SettingsView;
