import React, { useState, useEffect } from 'react';
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
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface SettingsData {
  // Trading (AMAN - Bisa di frontend)
  trading_mode: 'PAPER' | 'LIVE' | 'HYBRID';
  risk_level: 'LOW' | 'MODERATE' | 'HIGH' | 'AGGRESSIVE';
  max_position_size: number;
  max_drawdown: number;
  stop_loss_default: number;
  take_profit_default: number;
  
  // Exchange (HANYA STATUS, BUKAN API KEY)
  exchange: 'KRAKEN' | 'BINANCE' | 'BYBIT';
  exchange_configured: boolean;
  enable_websocket: boolean;
  
  // Telegram (HANYA STATUS, BUKAN TOKEN)
  telegram_enabled: boolean;
  telegram_configured: boolean;
  telegram_alerts: {
    signals: boolean;
    trades: boolean;
    errors: boolean;
    daily_report: boolean;
  };
  
  // System
  auto_start: boolean;
  auto_update: boolean;
  debug_mode: boolean;
  log_level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR';
  max_log_entries: number;
  
  // Cognitive
  learning_rate: number;
  curiosity_level: number;
  pattern_detection: boolean;
  auto_optimize: boolean;
  reflection_interval: number;
  
  // Security
  require_2fa: boolean;
  session_timeout: number;
  ip_whitelist: string[];
}

// ============================================================
// LOCALSTORAGE KEYS
// ============================================================

const SETTINGS_STORAGE_KEY = 'inkside_settings';

const loadSettingsFromStorage = (): SettingsData | null => {
  try {
    const data = localStorage.getItem(SETTINGS_STORAGE_KEY);
    if (data) {
      return JSON.parse(data);
    }
    return null;
  } catch {
    return null;
  }
};

const saveSettingsToStorage = (settings: SettingsData) => {
  try {
    localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(settings));
  } catch (e) {
    console.error('Failed to save settings to localStorage:', e);
  }
};

// ============================================================
// DEFAULT SETTINGS
// ============================================================

const defaultSettings: SettingsData = {
  trading_mode: 'PAPER',
  risk_level: 'MODERATE',
  max_position_size: 1000,
  max_drawdown: 20,
  stop_loss_default: 2,
  take_profit_default: 5,
  exchange: 'KRAKEN',
  exchange_configured: false,
  enable_websocket: true,
  telegram_enabled: false,
  telegram_configured: false,
  telegram_alerts: {
    signals: true,
    trades: true,
    errors: true,
    daily_report: false,
  },
  auto_start: false,
  auto_update: true,
  debug_mode: false,
  log_level: 'INFO',
  max_log_entries: 10000,
  learning_rate: 0.01,
  curiosity_level: 0.7,
  pattern_detection: true,
  auto_optimize: true,
  reflection_interval: 300,
  require_2fa: false,
  session_timeout: 3600,
  ip_whitelist: [],
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const SettingsView: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [activeTab, setActiveTab] = useState<'trading' | 'exchange' | 'telegram' | 'system' | 'cognitive' | 'security'>('trading');
  
  const [settings, setSettings] = useState<SettingsData>(() => {
    const saved = loadSettingsFromStorage();
    return saved || defaultSettings;
  });

  // ============================================================
  // LOAD SETTINGS
  // ============================================================
  
  useEffect(() => {
    loadSettings();
  }, []);

  // Auto-save ke localStorage setiap perubahan
  useEffect(() => {
    saveSettingsToStorage(settings);
  }, [settings]);

  const loadSettings = async () => {
    setLoading(true);
    try {
      // Load status dari backend (tanpa API key)
      const response = await fetch('/api/settings/status', {
        headers: { 'Accept': 'application/json' }
      });
      if (response.ok) {
        const data = await response.json();
        setSettings(prev => ({
          ...prev,
          exchange_configured: data.kraken_configured || false,
          telegram_configured: data.telegram_configured || false,
          trading_mode: data.trading_mode || prev.trading_mode,
          risk_level: data.risk_level || prev.risk_level,
        }));
        console.log('✅ Settings status loaded from backend');
      }
    } catch (error) {
      console.error('Failed to load settings status:', error);
    } finally {
      setLoading(false);
    }
  };

  const saveSettings = async () => {
    setSaving(true);
    setSaved(false);
    try {
      // Simpan ke localStorage
      saveSettingsToStorage(settings);
      
      // Kirim ke backend (tanpa API key)
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          trading_mode: settings.trading_mode,
          risk_level: settings.risk_level,
          max_position_size: settings.max_position_size,
          max_drawdown: settings.max_drawdown,
          stop_loss_default: settings.stop_loss_default,
          take_profit_default: settings.take_profit_default,
          exchange: settings.exchange,
          enable_websocket: settings.enable_websocket,
          telegram_enabled: settings.telegram_enabled,
          telegram_alerts: settings.telegram_alerts,
          auto_start: settings.auto_start,
          auto_update: settings.auto_update,
          debug_mode: settings.debug_mode,
          log_level: settings.log_level,
          max_log_entries: settings.max_log_entries,
          learning_rate: settings.learning_rate,
          curiosity_level: settings.curiosity_level,
          pattern_detection: settings.pattern_detection,
          auto_optimize: settings.auto_optimize,
          reflection_interval: settings.reflection_interval,
          require_2fa: settings.require_2fa,
          session_timeout: settings.session_timeout,
          ip_whitelist: settings.ip_whitelist,
        })
      });
      
      if (response.ok) {
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
        console.log('✅ Settings saved to backend');
      } else {
        console.error('Failed to save to backend');
      }
    } catch (error) {
      console.error('Failed to save settings:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (key: keyof SettingsData, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleTelegramAlert = (key: keyof typeof settings.telegram_alerts, value: boolean) => {
    setSettings(prev => ({
      ...prev,
      telegram_alerts: { ...prev.telegram_alerts, [key]: value }
    }));
  };

  const tabs = [
    { id: 'trading' as const, label: '💰 Trading', icon: TrendingUp },
    { id: 'exchange' as const, label: '🔄 Exchange', icon: Server },
    { id: 'telegram' as const, label: '✈️ Telegram', icon: Send },
    { id: 'system' as const, label: '⚙️ System', icon: Settings },
    { id: 'cognitive' as const, label: '🧠 Cognitive', icon: Brain },
    { id: 'security' as const, label: '🔒 Security', icon: Shield },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'trading':
        return renderTradingTab();
      case 'exchange':
        return renderExchangeTab();
      case 'telegram':
        return renderTelegramTab();
      case 'system':
        return renderSystemTab();
      case 'cognitive':
        return renderCognitiveTab();
      case 'security':
        return renderSecurityTab();
      default:
        return null;
    }
  };

  // ============================================================
  // TAB: TRADING
  // ============================================================
  
  const renderTradingTab = () => (
    <div className="space-y-6">
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Trading Mode</h4>
        <div className="grid grid-cols-3 gap-3">
          {(['PAPER', 'LIVE', 'HYBRID'] as const).map((mode) => (
            <button
              key={mode}
              onClick={() => handleChange('trading_mode', mode)}
              className={`px-4 py-3 rounded-xl text-sm font-bold transition-all cursor-pointer ${
                settings.trading_mode === mode
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                  : 'bg-[#0B0F14] text-[#8D9AAA] hover:text-white border border-[#26313D]'
              }`}
            >
              {mode}
            </button>
          ))}
        </div>
        <p className="text-xs text-[#5F6B78] mt-2">PAPER = Simulated | LIVE = Real money | HYBRID = Paper + Live monitoring</p>
      </div>

      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Risk Management</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Risk Level</label>
            <select
              value={settings.risk_level}
              onChange={(e) => handleChange('risk_level', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            >
              <option value="LOW">Low</option>
              <option value="MODERATE">Moderate</option>
              <option value="HIGH">High</option>
              <option value="AGGRESSIVE">Aggressive</option>
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Max Position Size ($)</label>
            <input
              type="number"
              value={settings.max_position_size}
              onChange={(e) => handleChange('max_position_size', parseFloat(e.target.value))}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Max Drawdown (%)</label>
            <input
              type="number"
              value={settings.max_drawdown}
              onChange={(e) => handleChange('max_drawdown', parseFloat(e.target.value))}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Default Stop Loss (%)</label>
            <input
              type="number"
              value={settings.stop_loss_default}
              onChange={(e) => handleChange('stop_loss_default', parseFloat(e.target.value))}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Default Take Profit (%)</label>
            <input
              type="number"
              value={settings.take_profit_default}
              onChange={(e) => handleChange('take_profit_default', parseFloat(e.target.value))}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>
      </div>
    </div>
  );

  // ============================================================
  // TAB: EXCHANGE (AMAN - TANPA INPUT API KEY)
  // ============================================================
  
  const renderExchangeTab = () => (
    <div className="space-y-6">
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Exchange Selection</h4>
        <div className="grid grid-cols-3 gap-3">
          {(['KRAKEN', 'BINANCE', 'BYBIT'] as const).map((ex) => (
            <button
              key={ex}
              onClick={() => handleChange('exchange', ex)}
              className={`px-4 py-3 rounded-xl text-sm font-bold transition-all cursor-pointer ${
                settings.exchange === ex
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                  : 'bg-[#0B0F14] text-[#8D9AAA] hover:text-white border border-[#26313D]'
              }`}
            >
              {ex}
            </button>
          ))}
        </div>
      </div>

      {/* STATUS API KEY - AMAN (TIDAK MENAMPILKAN API KEY) */}
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${settings.exchange_configured ? 'bg-emerald-400' : 'bg-amber-400'}`} />
            <span className="text-sm font-bold text-white">
              {settings.exchange_configured ? '✅ API Key Configured' : '⚠️ API Key Not Configured'}
            </span>
          </div>
          <div className="flex items-center gap-2 text-xs text-[#5F6B78]">
            <Info className="w-4 h-4" />
            <span>Configure via .env file</span>
          </div>
        </div>
        <p className="text-xs text-[#5F6B78] mt-2">
          API keys are stored securely on the server. Never exposed to the browser.
        </p>
        <div className="mt-3 p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
          <code className="text-xs text-[#8D9AAA] font-mono">
            # Edit ~/consciousness-intelligence/.env<br />
            KRAKEN_API_KEY=your_api_key<br />
            KRAKEN_API_SECRET=your_api_secret<br />
            KRAKEN_API_PASSPHRASE=your_passphrase
          </code>
        </div>
        <button
          onClick={() => window.open('https://www.kraken.com/settings/api', '_blank')}
          className="mt-3 w-full py-2 rounded-xl bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 font-bold text-sm transition-all border border-blue-500/20"
        >
          🔑 Get Kraken API Keys
        </button>
      </div>

      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <div className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={settings.enable_websocket}
            onChange={(e) => handleChange('enable_websocket', e.target.checked)}
            className="w-4 h-4 accent-blue-500"
          />
          <span className="text-sm text-[#8D9AAA]">Enable WebSocket (Real-time data)</span>
        </div>
      </div>
      
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <button
          onClick={async () => {
            try {
              const res = await fetch('/api/exchange/test', { method: 'POST' });
              const data = await res.json();
              alert(data.status === 'ok' ? '✅ Connection successful!' : '❌ Connection failed: ' + data.message);
            } catch {
              alert('❌ Failed to test connection');
            }
          }}
          className="w-full py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm transition-all"
        >
          🔌 Test Connection
        </button>
      </div>
    </div>
  );

  // ============================================================
  // TAB: TELEGRAM (AMAN - TANPA INPUT TOKEN)
  // ============================================================
  
  const renderTelegramTab = () => (
    <div className="space-y-6">
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <div className="flex items-center gap-3 mb-4">
          <input
            type="checkbox"
            checked={settings.telegram_enabled}
            onChange={(e) => handleChange('telegram_enabled', e.target.checked)}
            className="w-4 h-4 accent-blue-500"
          />
          <span className="text-sm font-bold text-white">Enable Telegram Alerts</span>
        </div>

        {/* STATUS TELEGRAM - AMAN */}
        <div className="flex items-center justify-between p-3 rounded-lg bg-[#0B0F14] border border-[#26313D]">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${settings.telegram_configured ? 'bg-emerald-400' : 'bg-amber-400'}`} />
            <span className="text-sm font-bold text-white">
              {settings.telegram_configured ? '✅ Bot Configured' : '⚠️ Bot Not Configured'}
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
        <h4 className="text-sm font-bold text-white mb-3">Alert Types</h4>
        {[
          { key: 'signals', label: '📡 Signal Alerts' },
          { key: 'trades', label: '💰 Trade Execution' },
          { key: 'errors', label: '⚠️ Error Alerts' },
          { key: 'daily_report', label: '📊 Daily Report' },
        ].map(({ key, label }) => (
          <div key={key} className="flex items-center gap-3 py-1">
            <input
              type="checkbox"
              checked={settings.telegram_alerts[key as keyof typeof settings.telegram_alerts]}
              onChange={(e) => handleTelegramAlert(key as keyof typeof settings.telegram_alerts, e.target.checked)}
              className="w-4 h-4 accent-blue-500"
            />
            <span className="text-sm text-[#8D9AAA]">{label}</span>
          </div>
        ))}
      </div>
      
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <button
          onClick={async () => {
            try {
              const res = await fetch('/api/telegram/test', { method: 'POST' });
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
  // TAB: SYSTEM
  // ============================================================
  
  const renderSystemTab = () => (
    <div className="space-y-6">
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">System Behavior</h4>
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.auto_start}
              onChange={(e) => handleChange('auto_start', e.target.checked)}
              className="w-4 h-4 accent-blue-500"
            />
            <span className="text-sm text-[#8D9AAA]">Auto-start engine on boot</span>
          </div>
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.auto_update}
              onChange={(e) => handleChange('auto_update', e.target.checked)}
              className="w-4 h-4 accent-blue-500"
            />
            <span className="text-sm text-[#8D9AAA]">Auto-update system</span>
          </div>
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.debug_mode}
              onChange={(e) => handleChange('debug_mode', e.target.checked)}
              className="w-4 h-4 accent-blue-500"
            />
            <span className="text-sm text-[#8D9AAA]">Debug mode (verbose logging)</span>
          </div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Logging</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Log Level</label>
            <select
              value={settings.log_level}
              onChange={(e) => handleChange('log_level', e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            >
              <option value="DEBUG">DEBUG</option>
              <option value="INFO">INFO</option>
              <option value="WARNING">WARNING</option>
              <option value="ERROR">ERROR</option>
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Max Log Entries</label>
            <input
              type="number"
              value={settings.max_log_entries}
              onChange={(e) => handleChange('max_log_entries', parseInt(e.target.value))}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>
      </div>
    </div>
  );

  // ============================================================
  // TAB: COGNITIVE
  // ============================================================
  
  const renderCognitiveTab = () => (
    <div className="space-y-6">
      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Learning Parameters</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Learning Rate</label>
            <input
              type="range"
              min="0.001"
              max="0.1"
              step="0.001"
              value={settings.learning_rate}
              onChange={(e) => handleChange('learning_rate', parseFloat(e.target.value))}
              className="w-full"
            />
            <span className="text-xs text-[#8D9AAA]">{settings.learning_rate}</span>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Curiosity Level</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={settings.curiosity_level}
              onChange={(e) => handleChange('curiosity_level', parseFloat(e.target.value))}
              className="w-full"
            />
            <span className="text-xs text-[#8D9AAA]">{settings.curiosity_level}</span>
          </div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D]">
        <h4 className="text-sm font-bold text-white mb-3">Cognitive Features</h4>
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.pattern_detection}
              onChange={(e) => handleChange('pattern_detection', e.target.checked)}
              className="w-4 h-4 accent-blue-500"
            />
            <span className="text-sm text-[#8D9AAA]">Pattern Detection</span>
          </div>
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.auto_optimize}
              onChange={(e) => handleChange('auto_optimize', e.target.checked)}
              className="w-4 h-4 accent-blue-500"
            />
            <span className="text-sm text-[#8D9AAA]">Auto-optimize learning</span>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Reflection Interval (seconds)</label>
            <input
              type="number"
              value={settings.reflection_interval}
              onChange={(e) => handleChange('reflection_interval', parseInt(e.target.value))}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
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
        <h4 className="text-sm font-bold text-white mb-3">Security Settings</h4>
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.require_2fa}
              onChange={(e) => handleChange('require_2fa', e.target.checked)}
              className="w-4 h-4 accent-blue-500"
            />
            <span className="text-sm text-[#8D9AAA]">Require 2FA for trading</span>
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">Session Timeout (seconds)</label>
            <input
              type="number"
              value={settings.session_timeout}
              onChange={(e) => handleChange('session_timeout', parseInt(e.target.value))}
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-[#8D9AAA] block mb-1">IP Whitelist</label>
            <input
              type="text"
              value={settings.ip_whitelist.join(', ')}
              onChange={(e) => handleChange('ip_whitelist', e.target.value.split(',').map(s => s.trim()).filter(Boolean))}
              placeholder="Enter IPs separated by commas"
              className="w-full px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-white text-sm focus:outline-none focus:border-blue-500"
            />
            <p className="text-[10px] text-[#5F6B78] mt-1">Example: 192.168.1.1, 10.0.0.1</p>
          </div>
        </div>
      </div>
    </div>
  );

  // ============================================================
  // MAIN RENDER
  // ============================================================

  return (
    <div className="space-y-6 pb-12">
      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#18212B] to-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center">
            <Settings className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-wide">Bot Settings</h2>
            <p className="text-xs text-[#8D9AAA]">Configure trading, exchange, and system preferences</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {saved && (
            <span className="text-emerald-400 text-sm font-semibold flex items-center gap-1">
              <Check className="w-4 h-4" /> Saved
            </span>
          )}
          <button
            onClick={loadSettings}
            disabled={loading}
            className="px-4 py-2 rounded-xl bg-[#0B0F14] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white border border-[#26313D] text-xs font-semibold transition-all cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 inline ${loading ? 'animate-spin' : ''}`} />
            {loading ? ' Loading...' : ' Refresh'}
          </button>
          <button
            onClick={saveSettings}
            disabled={saving}
            className="px-6 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm transition-all shadow-lg shadow-blue-600/30 cursor-pointer disabled:opacity-50 flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </div>

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

      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="text-center text-[#8D9AAA]">
              <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-3" />
              <p>Loading settings...</p>
            </div>
          </div>
        ) : (
          renderTabContent()
        )}
      </div>

      {/* SECURITY FOOTER */}
      <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
        <p className="text-xs text-amber-400">
          🔒 API keys and tokens are stored securely on the server. Never exposed to the browser.
          Configure them via <code className="bg-[#0B0F14] px-2 py-0.5 rounded">~/.env</code> file.
        </p>
      </div>
    </div>
  );
};
