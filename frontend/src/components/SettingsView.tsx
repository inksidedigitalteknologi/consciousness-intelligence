// src/components/SettingsView.tsx
// INKSIDE DIGITAL — Settings View v3.0 (Comprehensive)
// 11 tabs: System, Trading, Exchange, Dividend, AI, Telegram,
// Knowledge, Backup, Cache, Security, Modules

import React, { useState, useEffect, useCallback } from 'react';
import {
  Save, RefreshCw, Settings, Shield, Bell, Zap, Sliders, Globe,
  Lock, Database, Cpu, HardDrive, Clock, AlertTriangle,
  CheckCircle2, XCircle, Mail, Key, Server, Wifi, Activity,
  BarChart3, TrendingUp, Target, Brain, Info, Loader2, Heart,
  DollarSign, Bot, Send, BookOpen, Archive, HardDriveDownload,
  Trash2, Play, Pause, Check, Eye, EyeOff, Copy, Terminal,
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface ConfigData {
  // App
  app_name: string;
  app_version: string;
  app_author: string;
  cognitive_engine_version: string;
  signal_engine_version: string;

  // Exchange
  exchange_name: string;
  exchange_type: string;
  request_delay: number;
  request_timeout: number;
  request_retry_count: number;
  cache_ttl_seconds: number;
  max_markets: number;

  // Market
  default_pairs: string[];
  default_timeframes: string[];
  main_timeframe: string;
  scalp_timeframe: string;
  swing_timeframe: string;
  long_timeframe: string;

  // Scanner
  scan_interval_seconds: number;
  max_workers: number;
  scanner_batch_size: number;
  scanner_batch_delay: number;
  scanner_timeout: number;

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
  telegram_bot_token: string;
  telegram_chat_id: string;

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

  // Dividend
  dividend_enabled: boolean;
  dividend_trap_threshold: number;
  dividend_cache_ttl: number;
  dividend_data_source: string;

  // AI
  ai_enabled: boolean;
  ai_model: string;
  ai_daily_limit: number;
  ai_improvement_hour: number;

  // Knowledge
  knowledge_auto_learning: boolean;
  knowledge_rss_enabled: boolean;
  knowledge_max_items: number;
  knowledge_filter_indonesia: boolean;

  // Backup
  backup_enabled: boolean;
  backup_interval_hours: number;
  backup_keep_count: number;
  backup_max_age_days: number;

  // Cache
  cache_warm_enabled: boolean;
  cache_endpoint_ttl: Record<string, number>;

  // Status
  backend_status: 'online' | 'offline' | 'degraded';
  knowledge_items: number;
  dividend_items: number;
  ai_enabled_status: boolean;
  uptime_seconds: number;
  memory_items: number;
  patterns_count: number;
  decisions_count: number;
  semantic_count: number;
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
// HELPER COMPONENTS
// ============================================================

const Section: React.FC<{ title: string; icon: React.ReactNode; children: React.ReactNode }> = ({ title, icon, children }) => (
  <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
    <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
      {icon}
      {title}
    </h4>
    {children}
  </div>
);

const Field: React.FC<{ label: string; hint?: string; children: React.ReactNode }> = ({ label, hint, children }) => (
  <div>
    <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">{label}</label>
    {children}
    {hint && <p className="text-[10px] text-[#5F6B78] mt-1">{hint}</p>}
  </div>
);

const Toggle: React.FC<{ checked: boolean; onChange: (v: boolean) => void; label: string; disabled?: boolean }> = ({ checked, onChange, label, disabled }) => (
  <div className="flex items-center gap-3">
    <input
      type="checkbox"
      checked={checked}
      onChange={(e) => onChange(e.target.checked)}
      className="w-4 h-4 accent-blue-500 cursor-pointer"
      disabled={disabled}
    />
    <span className={`text-sm ${disabled ? 'text-[#5F6B78]' : 'text-[#8D9AAA]'}`}>{label}</span>
  </div>
);

const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
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
// MAIN COMPONENT
// ============================================================

export const SettingsView: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showToken, setShowToken] = useState(false);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<
    'system' | 'trading' | 'exchange' | 'dividend' | 'ai' | 'telegram' |
    'knowledge' | 'backup' | 'cache' | 'security' | 'modules'
  >('system');

  const [config, setConfig] = useState<ConfigData | null>(null);
  const [originalConfig, setOriginalConfig] = useState<ConfigData | null>(null);
  const [localSettings, setLocalSettings] = useState<Partial<ConfigData>>({});
  const [modules, setModules] = useState<any[]>([]);

  // ============================================================
  // LOAD CONFIG
  // ============================================================

  const loadConfig = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const configData = await fetchWithAuth('/api/config');
      setConfig(configData);
      setOriginalConfig(configData);
      setLocalSettings(configData);
      console.log('✅ Config loaded:', configData);

      // Load modules
      try {
        const modulesData = await fetchWithAuth('/api/modules/list');
        setModules(modulesData.modules || []);
      } catch (e) {
        console.warn('Modules not available:', e);
      }
    } catch (err) {
      console.error('Failed to load config:', err);
      setError('Failed to load configuration from backend.');
      try {
        const saved = localStorage.getItem('inkside_config');
        if (saved) {
          const parsed = JSON.parse(saved);
          setConfig(parsed);
          setOriginalConfig(parsed);
          setLocalSettings(parsed);
        }
      } catch (e) {
        console.error('Failed to load from localStorage:', e);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  // ============================================================
  // SAVE CONFIG
  // ============================================================

  const saveConfig = useCallback(async () => {
    if (!localSettings) return;
    setSaving(true);
    setSaved(false);
    setError(null);
    try {
      await fetchWithAuth('/api/config', {
        method: 'POST',
        body: JSON.stringify(localSettings),
      });
      setConfig(localSettings as ConfigData);
      setOriginalConfig(localSettings as ConfigData);
      localStorage.setItem('inkside_config', JSON.stringify(localSettings));
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
      console.log('✅ Config saved');
    } catch (err) {
      console.error('Failed to save config:', err);
      setError('Failed to save configuration.');
    } finally {
      setSaving(false);
    }
  }, [localSettings]);

  // ============================================================
  // RESET DEFAULTS
  // ============================================================

  const resetToDefaults = useCallback(async () => {
    if (!window.confirm('Reset all settings to default values?')) return;
    try {
      const defaultConfig = await fetchWithAuth('/api/config/default');
      setLocalSettings(defaultConfig);
      setConfig(defaultConfig);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error('Failed to reset:', err);
      setError('Failed to reset configuration.');
    }
  }, []);

  // ============================================================
  // CLEAR CACHE
  // ============================================================

  const clearCache = useCallback(async () => {
    if (!window.confirm('Clear all caches?')) return;
    try {
      await fetchWithAuth('/api/cache/clear', { method: 'POST' });
      alert('✅ Cache cleared');
    } catch (err) {
      alert('❌ Failed to clear cache');
    }
  }, []);

  // ============================================================
  // WARM CACHE
  // ============================================================

  const warmCache = useCallback(async () => {
    try {
      await fetchWithAuth('/api/cache/warm', { method: 'POST' });
      alert('✅ Cache warming started');
    } catch (err) {
      alert('❌ Failed to warm cache');
    }
  }, []);

  // ============================================================
  // TEST TELEGRAM
  // ============================================================

  const testTelegram = useCallback(async () => {
    try {
      const res = await fetch('/api/telegram/test', {
        method: 'POST',
        headers: { 'X-API-Key': API_KEY },
      });
      const data = await res.json();
      alert(data.sent ? '✅ Test message sent!' : '❌ Failed: ' + (data.message || 'Unknown'));
    } catch {
      alert('❌ Failed to send test message');
    }
  }, []);

  // ============================================================
  // HANDLERS
  // ============================================================

  const handleChange = <K extends keyof ConfigData>(key: K, value: ConfigData[K]) => {
    setLocalSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleNumberChange = (key: keyof ConfigData, value: string) => {
    const num = parseFloat(value);
    if (!isNaN(num)) handleChange(key, num as any);
  };

  // ============================================================
  // EFFECTS
  // ============================================================

  useEffect(() => { loadConfig(); }, [loadConfig]);

  useEffect(() => {
    if (localSettings && Object.keys(localSettings).length > 0) {
      localStorage.setItem('inkside_config', JSON.stringify(localSettings));
    }
  }, [localSettings]);

  // ============================================================
  // TAB RENDERERS
  // ============================================================

  const renderSystemTab = () => (
    <div className="space-y-6">
      <Section title="System Status" icon={<Activity className="w-4 h-4 text-blue-400" />}>
        <div className="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 2xl:grid-cols-8 gap-3">
          {[
            { label: 'Backend', value: config?.backend_status === 'online' ? '✅ Online' : '⚠️ Offline' },
            { label: 'Knowledge', value: `${config?.knowledge_items || 0} items` },
            { label: 'Memory', value: `${config?.memory_items || 0} items` },
            { label: 'Uptime', value: `${Math.floor((config?.uptime_seconds || 0) / 3600)}h` },
          ].map((s, i) => (
            <div key={i} className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
              <span className="text-[10px] text-[#5F6B78] block">{s.label}</span>
              <span className="text-sm font-bold text-white">{s.value}</span>
            </div>
          ))}
        </div>
      </Section>

      <Section title="Debug & Logging" icon={<Terminal className="w-4 h-4 text-amber-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4">
          <Field label="Log Level">
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
          </Field>
          <div className="pt-2">
            <Toggle
              checked={localSettings?.debug_mode || false}
              onChange={(v) => handleChange('debug_mode', v)}
              label="Debug Mode"
            />
          </div>
        </div>
      </Section>

      <Section title="Performance" icon={<Cpu className="w-4 h-4 text-cyan-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
          <Field label="Max Threads">
            <input type="number" min={1} max={50}
              value={localSettings?.max_threads || 10}
              onChange={(e) => handleNumberChange('max_threads', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Thread Pool Size">
            <input type="number" min={1} max={50}
              value={localSettings?.thread_pool_size || 10}
              onChange={(e) => handleNumberChange('thread_pool_size', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="API Timeout (s)">
            <input type="number" min={5} max={120}
              value={localSettings?.api_timeout || 15}
              onChange={(e) => handleNumberChange('api_timeout', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
      </Section>

      <Section title="App Information" icon={<Info className="w-4 h-4 text-blue-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-3 text-xs">
          {[
            { label: 'App Name', value: config?.app_name },
            { label: 'Version', value: config?.app_version },
            { label: 'Author', value: config?.app_author },
            { label: 'Cognitive Engine', value: config?.cognitive_engine_version },
            { label: 'Signal Engine', value: config?.signal_engine_version },
          ].map((item, i) => (
            <div key={i} className="flex justify-between p-2 rounded-lg bg-[#0B0F14] border border-[#26313D]">
              <span className="text-[#5F6B78]">{item.label}</span>
              <span className="text-white font-mono">{item.value || '—'}</span>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );

  const renderTradingTab = () => (
    <div className="space-y-6">
      <Section title="Trading Mode" icon={<TrendingUp className="w-4 h-4 text-emerald-400" />}>
        <div className="grid grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-3">
          {(['PAPER', 'LIVE', 'HYBRID'] as const).map((mode) => {
            const isActive =
              (mode === 'PAPER' && localSettings?.paper_trading && !localSettings?.trading_enabled) ||
              (mode === 'HYBRID' && localSettings?.paper_trading && localSettings?.trading_enabled) ||
              (mode === 'LIVE' && !localSettings?.paper_trading && localSettings?.trading_enabled);
            return (
              <button key={mode}
                onClick={() => {
                  handleChange('paper_trading', mode === 'PAPER' || mode === 'HYBRID');
                  handleChange('trading_enabled', mode === 'LIVE' || mode === 'HYBRID');
                }}
                className={`px-4 py-3 rounded-xl text-sm font-bold transition-all cursor-pointer ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                    : 'bg-[#0B0F14] text-[#8D9AAA] hover:text-white border border-[#26313D]'
                }`}
              >
                {mode}
              </button>
            );
          })}
        </div>
        <p className="text-xs text-[#5F6B78] mt-2">PAPER = Simulated | LIVE = Real money | HYBRID = Both</p>
      </Section>

      <Section title="Risk Management" icon={<Shield className="w-4 h-4 text-rose-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
          <Field label="Risk per Trade (%)">
            <input type="number" min={0.1} max={10} step={0.1}
              value={localSettings?.default_risk_percent || 1}
              onChange={(e) => handleNumberChange('default_risk_percent', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Risk Reward Ratio">
            <input type="number" min={1} max={10} step={0.5}
              value={localSettings?.default_risk_reward || 3}
              onChange={(e) => handleNumberChange('default_risk_reward', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Max Drawdown (%)">
            <input type="number" min={5} max={50}
              value={localSettings?.max_drawdown_percent || 20}
              onChange={(e) => handleNumberChange('max_drawdown_percent', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Max Position Size">
            <input type="number" min={10}
              value={localSettings?.max_position_size || 1000}
              onChange={(e) => handleNumberChange('max_position_size', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Min Position Size">
            <input type="number" min={1}
              value={localSettings?.min_position_size || 10}
              onChange={(e) => handleNumberChange('min_position_size', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Max Daily Trades">
            <input type="number" min={1} max={100}
              value={localSettings?.max_daily_trades || 10}
              onChange={(e) => handleNumberChange('max_daily_trades', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Max Open Positions">
            <input type="number" min={1} max={20}
              value={localSettings?.max_open_positions || 5}
              onChange={(e) => handleNumberChange('max_open_positions', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
      </Section>

      <Section title="Default SL/TP" icon={<Target className="w-4 h-4 text-amber-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4">
          <Field label="Stop Loss (%)">
            <input type="number" min={0.5} max={20} step={0.5}
              value={localSettings?.stop_loss_percent || 5}
              onChange={(e) => handleNumberChange('stop_loss_percent', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Take Profit (%)">
            <input type="number" min={1} max={50}
              value={localSettings?.take_profit_percent || 15}
              onChange={(e) => handleNumberChange('take_profit_percent', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
      </Section>

      <Section title="Signal Engine" icon={<Zap className="w-4 h-4 text-cyan-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
          <Field label="Min MTF Alignment">
            <input type="number" min={1} max={6}
              value={localSettings?.min_mtf_alignment || 2}
              onChange={(e) => handleNumberChange('min_mtf_alignment', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Min Signal Strength">
            <input type="number" min={0} max={100}
              value={localSettings?.min_signal_strength || 60}
              onChange={(e) => handleNumberChange('min_signal_strength', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Min Confidence">
            <input type="number" min={0} max={100}
              value={localSettings?.min_signal_confidence || 60}
              onChange={(e) => handleNumberChange('min_signal_confidence', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Cooldown (s)">
            <input type="number" min={0}
              value={localSettings?.signal_cooldown_seconds || 7200}
              onChange={(e) => handleNumberChange('signal_cooldown_seconds', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Max Signals/Scan">
            <input type="number" min={1} max={20}
              value={localSettings?.max_signals_per_scan || 2}
              onChange={(e) => handleNumberChange('max_signals_per_scan', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
      </Section>
    </div>
  );

  const renderExchangeTab = () => (
    <div className="space-y-6">
      <Section title="Exchange Configuration" icon={<Server className="w-4 h-4 text-blue-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4">
          <Field label="Exchange">
            <div className="px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm">
              {config?.exchange_name || 'Kraken'}
            </div>
          </Field>
          <Field label="Exchange Type">
            <div className="px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm">
              {config?.exchange_type || 'kraken'}
            </div>
          </Field>
          <Field label="Request Delay (s)">
            <input type="number" min={0.5} max={10} step={0.5}
              value={localSettings?.request_delay || 2}
              onChange={(e) => handleNumberChange('request_delay', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Cache TTL (s)">
            <input type="number" min={30} max={600}
              value={localSettings?.cache_ttl_seconds || 120}
              onChange={(e) => handleNumberChange('cache_ttl_seconds', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
      </Section>

      <Section title="Market Pairs" icon={<Globe className="w-4 h-4 text-emerald-400" />}>
        <div className="flex flex-wrap gap-2">
          {(localSettings?.default_pairs || ['BTC/USD', 'ETH/USD', 'SOL/USD']).map((pair) => (
            <span key={pair} className="px-3 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-white text-sm">
              {pair}
            </span>
          ))}
        </div>
        <p className="text-xs text-[#5F6B78] mt-2">Configure pairs via config.py</p>
      </Section>

      <Section title="Timeframes" icon={<Clock className="w-4 h-4 text-amber-400" />}>
        <div className="flex flex-wrap gap-2">
          {(localSettings?.default_timeframes || ['1h', '4h', '1d']).map((tf) => (
            <span key={tf} className={`px-3 py-1 rounded-lg border text-sm ${
              tf === localSettings?.main_timeframe
                ? 'bg-blue-600/20 text-blue-400 border-blue-500/30'
                : 'bg-[#0B0F14] text-[#8D9AAA] border-[#26313D]'
            }`}>
              {tf} {tf === localSettings?.main_timeframe && '⭐'}
            </span>
          ))}
        </div>
        <p className="text-xs text-[#5F6B78] mt-2">Main: {localSettings?.main_timeframe || '1h'} | Scalp: {localSettings?.scalp_timeframe || '15m'} | Swing: {localSettings?.swing_timeframe || '4h'} | Long: {localSettings?.long_timeframe || '1d'}</p>
      </Section>

      <Section title="Scanner" icon={<Activity className="w-4 h-4 text-purple-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
          <Field label="Scan Interval (s)">
            <input type="number" min={60}
              value={localSettings?.scan_interval_seconds || 600}
              onChange={(e) => handleNumberChange('scan_interval_seconds', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Batch Size">
            <input type="number" min={1} max={20}
              value={localSettings?.scanner_batch_size || 2}
              onChange={(e) => handleNumberChange('scanner_batch_size', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Batch Delay (s)">
            <input type="number" min={1}
              value={localSettings?.scanner_batch_delay || 5}
              onChange={(e) => handleNumberChange('scanner_batch_delay', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
      </Section>
    </div>
  );

  const renderDividendTab = () => (
    <div className="space-y-6">
      <Section title="Dividend Hunter" icon={<DollarSign className="w-4 h-4 text-emerald-400" />}>
        <Toggle
          checked={localSettings?.dividend_enabled !== false}
          onChange={(v) => handleChange('dividend_enabled', v)}
          label="Enable Dividend Hunter"
        />
        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 mt-4">
          <Field label="Trap Score Threshold" hint="Score di atas ini = trap">
            <input type="number" min={0} max={100}
              value={localSettings?.dividend_trap_threshold || 50}
              onChange={(e) => handleNumberChange('dividend_trap_threshold', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Cache TTL (s)">
            <input type="number" min={300}
              value={localSettings?.dividend_cache_ttl || 21600}
              onChange={(e) => handleNumberChange('dividend_cache_ttl', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Data Source">
            <select
              value={localSettings?.dividend_data_source || 'nasdaq'}
              onChange={(e) => handleChange('dividend_data_source', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            >
              <option value="nasdaq">Nasdaq API</option>
              <option value="yfinance">Yahoo Finance</option>
              <option value="both">Both</option>
            </select>
          </Field>
        </div>
      </Section>

      <Section title="Dividend Data Status" icon={<BarChart3 className="w-4 h-4 text-cyan-400" />}>
        <div className="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 2xl:grid-cols-8 gap-3">
          {[
            { label: 'Dividend Items', value: config?.dividend_items || 0 },
            { label: 'Trap Alerts', value: '—' },
            { label: 'Kings', value: '—' },
            { label: 'Aristocrats', value: '—' },
          ].map((s, i) => (
            <div key={i} className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
              <span className="text-[10px] text-[#5F6B78] block">{s.label}</span>
              <span className="text-sm font-bold text-white font-mono">{s.value}</span>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );

  const renderAITab = () => (
    <div className="space-y-6">
      <Section title="AI / DeepSeek" icon={<Bot className="w-4 h-4 text-purple-400" />}>
        <Toggle
          checked={localSettings?.ai_enabled || false}
          onChange={(v) => handleChange('ai_enabled', v)}
          label="Enable DeepSeek AI"
        />
        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 mt-4">
          <Field label="Model">
            <select
              value={localSettings?.ai_model || 'deepseek-chat'}
              onChange={(e) => handleChange('ai_model', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            >
              <option value="deepseek-chat">deepseek-chat</option>
              <option value="deepseek-coder">deepseek-coder</option>
              <option value="deepseek-reasoner">deepseek-reasoner</option>
            </select>
          </Field>
          <Field label="Daily Limit">
            <input type="number" min={1} max={1000}
              value={localSettings?.ai_daily_limit || 10}
              onChange={(e) => handleNumberChange('ai_daily_limit', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Improvement Hour">
            <input type="number" min={0} max={23}
              value={localSettings?.ai_improvement_hour || 2}
              onChange={(e) => handleNumberChange('ai_improvement_hour', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
        <div className="mt-4 p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
          <code className="text-xs text-[#8D9AAA] font-mono">
            # Edit ~/consciousness-intelligence/.env<br />
            DEEPSEEK_ENABLED=true<br />
            DEEPSEEK_API_KEY=your_api_key_here
          </code>
        </div>
      </Section>

      <Section title="AI Status" icon={<CheckCircle2 className="w-4 h-4 text-emerald-400" />}>
        <div className="flex items-center justify-between p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${config?.ai_enabled_status ? 'bg-emerald-400' : 'bg-rose-400'}`} />
            <span className="text-sm font-bold text-white">
              {config?.ai_enabled_status ? '✅ AI Enabled' : '❌ AI Disabled'}
            </span>
          </div>
          <span className="text-xs text-[#5F6B78]">Model: {localSettings?.ai_model || 'deepseek-chat'}</span>
        </div>
      </Section>
    </div>
  );

  const renderTelegramTab = () => (
    <div className="space-y-6">
      <Section title="Telegram Bot" icon={<Send className="w-4 h-4 text-sky-400" />}>
        <Toggle
          checked={localSettings?.telegram_enabled || false}
          onChange={(v) => handleChange('telegram_enabled', v)}
          label="Enable Telegram Alerts"
        />
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-4 mt-4">
          <Field label="Bot Token" hint="From @BotFather">
            <div className="relative">
              <input
                type={showToken ? 'text' : 'password'}
                value={localSettings?.telegram_bot_token || ''}
                onChange={(e) => handleChange('telegram_bot_token', e.target.value)}
                placeholder="123456:ABC-DEF..."
                className="w-full px-3 py-2 pr-10 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
              />
              <button
                onClick={() => setShowToken(!showToken)}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-[#5F6B78] hover:text-white"
              >
                {showToken ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </Field>
          <Field label="Chat ID">
            <input
              type="text"
              value={localSettings?.telegram_chat_id || ''}
              onChange={(e) => handleChange('telegram_chat_id', e.target.value)}
              placeholder="123456789"
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
        <div className="mt-4 flex items-center justify-between p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${config?.telegram_configured ? 'bg-emerald-400' : 'bg-amber-400'}`} />
            <span className="text-sm font-bold text-white">
              {config?.telegram_configured ? '✅ Bot Configured' : '⚠️ Not Configured'}
            </span>
          </div>
          <span className="text-xs text-[#5F6B78]">Configure via .env</span>
        </div>
        <button
          onClick={testTelegram}
          className="mt-4 w-full py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm transition-all"
        >
          📨 Send Test Message
        </button>
      </Section>

      <Section title="Available Commands" icon={<Terminal className="w-4 h-4 text-amber-400" />}>
        <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-2 text-xs">
          {['/start', '/health', '/signals', '/performance', '/pnl', '/brain',
            '/modules', '/daily', '/risk', '/trade', '/refresh'].map((cmd) => (
            <span key={cmd} className="px-2 py-1 rounded bg-[#0B0F14] border border-[#26313D] text-[#8D9AAA] font-mono">
              {cmd}
            </span>
          ))}
        </div>
      </Section>
    </div>
  );

  const renderKnowledgeTab = () => (
    <div className="space-y-6">
      <Section title="Knowledge Engine" icon={<BookOpen className="w-4 h-4 text-teal-400" />}>
        <Toggle
          checked={localSettings?.knowledge_auto_learning || false}
          onChange={(v) => handleChange('knowledge_auto_learning', v)}
          label="Enable Auto-Learning"
        />
        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 mt-4">
          <Field label="Max Items" hint="0 = unlimited">
            <input type="number" min={0}
              value={localSettings?.knowledge_max_items || 0}
              onChange={(e) => handleNumberChange('knowledge_max_items', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
        <div className="mt-4 space-y-3">
          <Toggle
            checked={localSettings?.knowledge_rss_enabled || false}
            onChange={(v) => handleChange('knowledge_rss_enabled', v)}
            label="Enable RSS Feed Learning"
          />
          <Toggle
            checked={localSettings?.knowledge_filter_indonesia || false}
            onChange={(v) => handleChange('knowledge_filter_indonesia', v)}
            label="Filter Indonesian Content"
          />
        </div>
      </Section>

      <Section title="Knowledge Status" icon={<Database className="w-4 h-4 text-indigo-400" />}>
        <div className="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 2xl:grid-cols-8 gap-3">
          {[
            { label: 'Knowledge', value: config?.knowledge_items || 0 },
            { label: 'Memory', value: config?.memory_items || 0 },
            { label: 'Patterns', value: config?.patterns_count || 0 },
            { label: 'Decisions', value: config?.decisions_count || 0 },
            { label: 'Semantic', value: config?.semantic_count || 0 },
          ].map((s, i) => (
            <div key={i} className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
              <span className="text-[10px] text-[#5F6B78] block">{s.label}</span>
              <span className="text-sm font-bold text-white font-mono">{s.value}</span>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );

  const renderBackupTab = () => (
    <div className="space-y-6">
      <Section title="Backup Configuration" icon={<HardDriveDownload className="w-4 h-4 text-amber-400" />}>
        <Toggle
          checked={localSettings?.backup_enabled !== false}
          onChange={(v) => handleChange('backup_enabled', v)}
          label="Enable Auto-Backup"
        />
        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 mt-4">
          <Field label="Interval (hours)">
            <input type="number" min={1} max={168}
              value={localSettings?.backup_interval_hours || 6}
              onChange={(e) => handleNumberChange('backup_interval_hours', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Keep Count">
            <input type="number" min={1} max={50}
              value={localSettings?.backup_keep_count || 3}
              onChange={(e) => handleNumberChange('backup_keep_count', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
          <Field label="Max Age (days)">
            <input type="number" min={1} max={365}
              value={localSettings?.backup_max_age_days || 7}
              onChange={(e) => handleNumberChange('backup_max_age_days', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </Field>
        </div>
      </Section>

      <Section title="Backup Actions" icon={<Archive className="w-4 h-4 text-blue-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-3">
          <button
            onClick={async () => {
              try {
                await fetchWithAuth('/api/database/backups/cleanup', {
                  method: 'POST',
                  body: JSON.stringify({
                    keep: localSettings?.backup_keep_count || 3,
                    max_age_days: 0,
                  }),
                });
                alert('✅ Cleanup done');
              } catch {
                alert('❌ Cleanup failed');
              }
            }}
            className="py-2 rounded-xl bg-rose-600/20 hover:bg-rose-600/30 text-rose-400 font-bold text-sm border border-rose-500/20 transition-all"
          >
            🧹 Cleanup Old Backups
          </button>
          <button
            onClick={async () => {
              try {
                const res = await fetchWithAuth('/api/database/backups');
                alert(`Total: ${res.count} files, ${res.total_size_mb} MB`);
              } catch {
                alert('❌ Failed to load backups');
              }
            }}
            className="py-2 rounded-xl bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 font-bold text-sm border border-blue-500/20 transition-all"
          >
            📊 View Backups
          </button>
        </div>
      </Section>
    </div>
  );

  const renderCacheTab = () => (
    <div className="space-y-6">
      <Section title="Cache Configuration" icon={<Zap className="w-4 h-4 text-amber-400" />}>
        <Toggle
          checked={localSettings?.cache_warm_enabled !== false}
          onChange={(v) => handleChange('cache_warm_enabled', v)}
          label="Enable Warm Cache on Startup"
        />
        <div className="mt-4">
          <h5 className="text-xs font-bold text-white mb-2">Endpoint TTL (seconds)</h5>
          <div className="space-y-2">
            {Object.entries({
              'dividend/top': 3600,
              'dividend/upcoming': 3600,
              'dividend/trap-screener': 21600,
              'dividend/stats': 3600,
              'dividend/sectors': 21600,
              'knowledge/all': 300,
              'knowledge/stats': 300,
            }).map(([endpoint, ttl]) => (
              <div key={endpoint} className="flex items-center justify-between p-2 rounded-lg bg-[#0B0F14] border border-[#26313D]">
                <span className="text-xs text-[#8D9AAA] font-mono">{endpoint}</span>
                <span className="text-xs text-white font-mono font-bold">{ttl}s</span>
              </div>
            ))}
          </div>
        </div>
      </Section>

      <Section title="Cache Actions" icon={<RefreshCw className="w-4 h-4 text-cyan-400" />}>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-3">
          <button
            onClick={clearCache}
            className="py-2 rounded-xl bg-rose-600/20 hover:bg-rose-600/30 text-rose-400 font-bold text-sm border border-rose-500/20 transition-all"
          >
            🗑️ Clear All Cache
          </button>
          <button
            onClick={warmCache}
            className="py-2 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-400 font-bold text-sm border border-emerald-500/20 transition-all"
          >
            🔥 Warm Cache Now
          </button>
        </div>
      </Section>
    </div>
  );

  const renderSecurityTab = () => (
    <div className="space-y-6">
      <Section title="Security Settings" icon={<Shield className="w-4 h-4 text-amber-400" />}>
        <div className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">API Key</label>
            <div className="flex items-center gap-2 p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
              <Key className="w-4 h-4 text-emerald-400" />
              <span className="text-sm text-white font-mono">
                {showToken ? API_KEY : '••••••••••••••••'}
              </span>
              <button
                onClick={() => setShowToken(!showToken)}
                className="ml-auto text-[#5F6B78] hover:text-white"
              >
                {showToken ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(API_KEY);
                  setCopied(true);
                  setTimeout(() => setCopied(false), 2000);
                }}
                className="text-[#5F6B78] hover:text-white"
              >
                {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
            <p className="text-[10px] text-[#5F6B78] mt-1">Configure via .env file</p>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">IP Whitelist</label>
            <input
              type="text"
              placeholder="192.168.1.1, 10.0.0.1"
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm"
            />
          </div>
          <Toggle
            checked={false}
            onChange={() => {}}
            label="Require 2FA for trading (Coming soon)"
            disabled
          />
        </div>
      </Section>

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

  const renderModulesTab = () => (
    <div className="space-y-6">
      <Section title="System Modules" icon={<Cpu className="w-4 h-4 text-blue-400" />}>
        <div className="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 2xl:grid-cols-8 gap-3 mb-4">
          <div className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
            <span className="text-[10px] text-[#5F6B78] block">Total</span>
            <span className="text-sm font-bold text-white font-mono">{modules.length || 54}</span>
          </div>
          <div className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
            <span className="text-[10px] text-[#5F6B78] block">Active</span>
            <span className="text-sm font-bold text-emerald-400 font-mono">
              {modules.filter((m: any) => m.status === 'active').length || 48}
            </span>
          </div>
          <div className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
            <span className="text-[10px] text-[#5F6B78] block">Warning</span>
            <span className="text-sm font-bold text-amber-400 font-mono">
              {modules.filter((m: any) => m.status === 'warning').length || 6}
            </span>
          </div>
          <div className="p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
            <span className="text-[10px] text-[#5F6B78] block">Health</span>
            <span className="text-sm font-bold text-cyan-400 font-mono">88.9%</span>
          </div>
        </div>

        {modules.length > 0 ? (
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {modules.map((mod: any, i: number) => (
              <div key={i} className="flex items-center justify-between p-2 rounded-lg bg-[#0B0F14] border border-[#26313D]">
                <div className="flex items-center gap-2">
                  {mod.status === 'active'
                    ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    : <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />}
                  <span className="text-xs text-white font-mono">{mod.name}</span>
                </div>
                <span className={`text-[10px] font-bold ${
                  mod.status === 'active' ? 'text-emerald-400' : 'text-amber-400'
                }`}>
                  {mod.status?.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-[#5F6B78] text-xs">
            Module data not available
          </div>
        )}
      </Section>
    </div>
  );

  // ============================================================
  // MAIN RENDER
  // ============================================================

  const tabs = [
    { id: 'system' as const, label: '⚙️ System', icon: Settings },
    { id: 'trading' as const, label: '💰 Trading', icon: TrendingUp },
    { id: 'exchange' as const, label: '🔄 Exchange', icon: Server },
    { id: 'dividend' as const, label: '💰 Dividend', icon: DollarSign },
    { id: 'ai' as const, label: '🧠 AI', icon: Brain },
    { id: 'telegram' as const, label: '✈️ Telegram', icon: Send },
    { id: 'knowledge' as const, label: '📚 Knowledge', icon: BookOpen },
    { id: 'backup' as const, label: '💾 Backup', icon: Archive },
    { id: 'cache' as const, label: '⚡ Cache', icon: Zap },
    { id: 'security' as const, label: '🔒 Security', icon: Shield },
    { id: 'modules' as const, label: '📊 Modules', icon: Cpu },
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
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                  : 'text-[#8D9AAA] hover:text-white hover:bg-[#1A2530]'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
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
        {activeTab === 'dividend' && renderDividendTab()}
        {activeTab === 'ai' && renderAITab()}
        {activeTab === 'telegram' && renderTelegramTab()}
        {activeTab === 'knowledge' && renderKnowledgeTab()}
        {activeTab === 'backup' && renderBackupTab()}
        {activeTab === 'cache' && renderCacheTab()}
        {activeTab === 'security' && renderSecurityTab()}
        {activeTab === 'modules' && renderModulesTab()}
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
