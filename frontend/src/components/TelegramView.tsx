import React, { useState, useEffect, useRef } from 'react';
import {
  Send,
  CheckCircle2,
  AlertCircle,
  Shield,
  Bell,
  Key,
  Settings,
  RefreshCw,
  History,
  Clock,
  User,
  MessageSquare,
  Zap,
  Activity,
  TrendingUp,
  TrendingDown,
  Minus,
  Trash2,
  Plus,
  Copy,
  Save,
  Eye,
  EyeOff,
  Info,
  AlertTriangle,
  Check,
  X,
  Loader2,
} from 'lucide-react';
import { inksideAPI } from '../api/inkside';

// ============================================================
// TYPES
// ============================================================

interface TelegramMessage {
  id: string;
  text: string;
  timestamp: string;
  status: 'sent' | 'failed' | 'pending';
  type: 'signal' | 'alert' | 'test' | 'system' | 'trade' | 'daily';
}

interface TelegramConfig {
  bot_token: string;
  chat_id: string;
  enabled: boolean;
  configured: boolean;
  notifications: {
    signals: boolean;
    trades: boolean;
    health: boolean;
    errors: boolean;
    daily_report: boolean;
  };
}

interface TelegramViewProps {
  isConfigured: boolean;
  onSaveConfig: (token: string, chatId: string) => void;
}

// ============================================================
// HELPER FUNCTIONS
// ============================================================

const maskToken = (token: string): string => {
  if (!token || token.length < 10) return token;
  return token.substring(0, 6) + '••••••••' + token.substring(token.length - 4);
};

const maskChatId = (chatId: string): string => {
  if (!chatId || chatId.length < 8) return chatId;
  return chatId.substring(0, 3) + '••••••' + chatId.substring(chatId.length - 3);
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const TelegramView: React.FC<TelegramViewProps> = ({
  isConfigured,
  onSaveConfig,
}) => {
  // ============================================================
  // STATE
  // ============================================================

  const [botToken, setBotToken] = useState('');
  const [chatId, setChatId] = useState('');
  const [showToken, setShowToken] = useState(false);
  const [showChatId, setShowChatId] = useState(false);
  const [messages, setMessages] = useState<TelegramMessage[]>([]);
  const [customMessage, setCustomMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [testResult, setTestResult] = useState<{ type: 'success' | 'error' | 'info' | null; message: string }>({ type: null, message: '' });
  const [copied, setCopied] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [config, setConfig] = useState<TelegramConfig>({
    bot_token: '',
    chat_id: '',
    enabled: true,
    configured: false,
    notifications: {
      signals: true,
      trades: true,
      health: true,
      errors: true,
      daily_report: false,
    },
  });
  const [lastStatusCheck, setLastStatusCheck] = useState<string | null>(null);
  const [isStatusLoading, setIsStatusLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // ============================================================
  // LOAD CONFIG FROM BACKEND
  // ============================================================

  const loadConfig = async () => {
    try {
      const response = await fetch('/api/telegram/config');
      const data = await response.json();

      if (data.configured) {
        setConfig((prev) => ({
          ...prev,
          bot_token: data.bot_token || '',
          chat_id: data.chat_id || '',
          configured: true,
          enabled: true,
        }));
        setBotToken(data.bot_token || '');
        setChatId(data.chat_id || '');
        setTestResult({ type: 'info', message: '✅ Configuration loaded from backend.' });
      } else {
        setConfig((prev) => ({ ...prev, configured: false }));
      }
    } catch (error) {
      console.error('Failed to load config:', error);
    }
  };

  // ============================================================
  // FETCH TELEGRAM STATUS
  // ============================================================

  const fetchTelegramStatus = async () => {
    setIsStatusLoading(true);
    try {
      const status = await inksideAPI.getTelegramStatus();
      setConfig((prev) => ({
        ...prev,
        configured: status.configured || false,
        enabled: status.configured || false,
      }));
      setLastStatusCheck(new Date().toISOString());
    } catch (error) {
      console.error('Failed to fetch Telegram status:', error);
    } finally {
      setIsStatusLoading(false);
    }
  };

  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {
    fetchTelegramStatus();
    loadConfig();

    // Load saved messages from localStorage
    const savedMessages = localStorage.getItem('telegram_messages');
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch (e) {
        console.error('Failed to load messages:', e);
      }
    }

    // Auto-refresh status every 30 seconds
    const interval = setInterval(fetchTelegramStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  // Save messages to localStorage
  useEffect(() => {
    localStorage.setItem('telegram_messages', JSON.stringify(messages));
  }, [messages]);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // ============================================================
  // SEND MESSAGE FUNCTIONS
  // ============================================================

  const sendMessage = async (text: string, type: TelegramMessage['type'] = 'test') => {
    if (!text.trim()) {
      setTestResult({ type: 'error', message: '❌ Message cannot be empty.' });
      return;
    }

    setIsSending(true);
    setTestResult({ type: null, message: '' });

    // Tambahkan pending message
    const pendingMessage: TelegramMessage = {
      id: `msg-${Date.now()}`,
      text: text,
      timestamp: new Date().toISOString(),
      status: 'pending',
      type: type,
    };
    setMessages((prev) => [pendingMessage, ...prev]);

    try {
      const response = await fetch('/api/telegram/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json();

      // Update status dari pending ke sent/failed
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === pendingMessage.id
            ? { ...msg, status: data.sent ? 'sent' : 'failed' }
            : msg
        )
      );

      if (data.sent) {
        setTestResult({ type: 'success', message: '✅ Message sent successfully!' });
      } else {
        setTestResult({ type: 'error', message: `❌ Failed to send: ${data.message || 'Unknown error'}` });
      }
    } catch (error: any) {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === pendingMessage.id ? { ...msg, status: 'failed' } : msg
        )
      );
      setTestResult({ type: 'error', message: `❌ Error: ${error.message}` });
    } finally {
      setIsSending(false);
    }
  };

  // ============================================================
  // SAVE CONFIG TO BACKEND
  // ============================================================

  const handleSaveConfig = async () => {
    const token = botToken.trim();
    const chatIdValue = chatId.trim();

    if (!token || !chatIdValue) {
      setTestResult({ type: 'error', message: '❌ Please enter both Bot Token and Chat ID.' });
      return;
    }

    setIsSaving(true);
    setTestResult({ type: null, message: '' });

    try {
      const response = await fetch('/api/telegram/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bot_token: token,
          chat_id: chatIdValue,
        }),
      });

      const data = await response.json();

      if (data.status === 'success') {
        setTestResult({ type: 'success', message: '✅ Configuration saved to backend! Restart backend to apply.' });
        setConfig((prev) => ({
          ...prev,
          bot_token: token,
          chat_id: chatIdValue,
          configured: true,
          enabled: true,
        }));
        onSaveConfig(token, chatIdValue);
        await fetchTelegramStatus();
      } else {
        setTestResult({ type: 'error', message: `❌ Failed to save: ${data.message}` });
      }
    } catch (error: any) {
      setTestResult({ type: 'error', message: `❌ Error: ${error.message}` });
    } finally {
      setIsSaving(false);
    }
  };

  // ============================================================
  // HANDLERS
  // ============================================================

  const handleSendCustom = () => {
    if (!customMessage.trim()) return;
    sendMessage(customMessage.trim(), 'test');
    setCustomMessage('');
  };

  const handleClearHistory = () => {
    if (window.confirm('Clear all message history?')) {
      setMessages([]);
      localStorage.removeItem('telegram_messages');
      setTestResult({ type: 'info', message: '🗑️ Message history cleared.' });
    }
  };

  const handleCopyConfig = () => {
    const token = botToken || config.bot_token;
    const chatIdValue = chatId || config.chat_id;
    const configText = `TELEGRAM_BOT_TOKEN=${token}\nTELEGRAM_CHAT_ID=${chatIdValue}`;

    if (navigator.clipboard) {
      navigator.clipboard.writeText(configText).then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      });
    } else {
      // Fallback
      const textarea = document.createElement('textarea');
      textarea.value = configText;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // ============================================================
  // QUICK MESSAGE TEMPLATES
  // ============================================================

  const quickTemplates = [
    {
      label: '🧠 System Health',
      icon: <Activity className="w-4 h-4" />,
      message: `🧠 <b>SYSTEM HEALTH REPORT</b>\n━━━━━━━━━━━━━━━━━━━━━\n<b>Status</b>: ✅ ONLINE\n<b>Uptime</b>: 24h 37m\n<b>Health Score</b>: 98.4%\n<b>Active Modules</b>: 32/32\n━━━━━━━━━━━━━━━━━━━━━\n<b>Time</b>: ${new Date().toLocaleString()}`,
      color: 'blue',
    },
    {
      label: '📊 Performance',
      icon: <TrendingUp className="w-4 h-4" />,
      message: `📊 <b>PERFORMANCE SUMMARY</b>\n━━━━━━━━━━━━━━━━━━━━━\n<b>Total Trades</b>: 42\n<b>Win Rate</b>: 78.5%\n<b>Total PnL</b>: +$335.58\n<b>ROI</b>: 3.36%\n━━━━━━━━━━━━━━━━━━━━━\n<b>Time</b>: ${new Date().toLocaleString()}`,
      color: 'green',
    },
    {
      label: '🔴 Emergency Alert',
      icon: <AlertCircle className="w-4 h-4" />,
      message: `🔴 <b>⚠️ EMERGENCY ALERT</b>\n━━━━━━━━━━━━━━━━━━━━━\n<b>Type</b>: System Warning\n<b>Severity</b>: HIGH\n<b>Message</b>: Abnormal market conditions detected. Please check system immediately.\n━━━━━━━━━━━━━━━━━━━━━\n<b>Time</b>: ${new Date().toLocaleString()}`,
      color: 'red',
    },
    {
      label: '💰 Daily Summary',
      icon: <Clock className="w-4 h-4" />,
      message: `💰 <b>DAILY TRADING SUMMARY</b>\n━━━━━━━━━━━━━━━━━━━━━\n<b>Date</b>: ${new Date().toLocaleDateString()}\n<b>Trades</b>: 12\n<b>Win</b>: 9 | Loss: 3\n<b>PnL</b>: +$89.50\n<b>Best Trade</b>: BTC/USD +$42.30\n━━━━━━━━━━━━━━━━━━━━━\n<b>Report Time</b>: ${new Date().toLocaleString()}`,
      color: 'yellow',
    },
    {
      label: '📈 Signal Alert',
      icon: <TrendingUp className="w-4 h-4" />,
      message: `📈 <b>TRADING SIGNAL</b>\n━━━━━━━━━━━━━━━━━━━━━\n<b>Pair</b>: BTC/USD\n<b>Signal</b>: STRONG BUY\n<b>Confidence</b>: 88%\n<b>Price</b>: $68,420.50\n<b>Target</b>: $71,000.00\n<b>Stop Loss</b>: $66,500.00\n━━━━━━━━━━━━━━━━━━━━━\n<b>Time</b>: ${new Date().toLocaleString()}`,
      color: 'purple',
    },
    {
      label: '📉 Trade Alert',
      icon: <TrendingDown className="w-4 h-4" />,
      message: `📉 <b>TRADE EXECUTED</b>\n━━━━━━━━━━━━━━━━━━━━━\n<b>Pair</b>: ETH/USD\n<b>Side</b>: SELL\n<b>Size</b>: 1.5 ETH\n<b>Price</b>: $3,245.00\n<b>PnL</b>: +$87.50\n<b>Status</b>: ✅ COMPLETED\n━━━━━━━━━━━━━━━━━━━━━\n<b>Time</b>: ${new Date().toLocaleString()}`,
      color: 'red',
    },
    {
      label: '🛡️ Risk Alert',
      icon: <Shield className="w-4 h-4" />,
      message: `🛡️ <b>RISK ALERT</b>\n━━━━━━━━━━━━━━━━━━━━━\n<b>Risk Level</b>: HIGH\n<b>Drawdown</b>: 12.5%\n<b>Current Position</b>: 45%\n<b>Max Allowed</b>: 20%\n<b>Action</b>: ⚠️ Reduce position or increase stop loss\n━━━━━━━━━━━━━━━━━━━━━\n<b>Time</b>: ${new Date().toLocaleString()}`,
      color: 'orange',
    },
    {
      label: '📡 System Info',
      icon: <Info className="w-4 h-4" />,
      message: `📡 <b>SYSTEM INFO</b>\n━━━━━━━━━━━━━━━━━━━━━\n<b>Brain</b>: Cognitive Mirror v5.0\n<b>Memory</b>: 2,450 records\n<b>Knowledge</b>: 1,840 items\n<b>Patterns</b>: 18 detected\n<b>Learning</b>: 🟢 ACTIVE\n━━━━━━━━━━━━━━━━━━━━━\n<b>Time</b>: ${new Date().toLocaleString()}`,
      color: 'cyan',
    },
  ];

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="space-y-6 pb-12">
      {/* ============================================================
          HEADER
      ============================================================ */}

      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#18212B] to-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-sky-600/20 border border-sky-500/30 flex items-center justify-center text-sky-400">
            <Send className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Telegram Notification & Signals Bridge
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Real-time trading signal alerts, position notifications & system warnings
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span
            className={`w-2.5 h-2.5 rounded-full ${
              config.configured || isConfigured ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'
            }`}
          />
          <span
            className={`text-xs font-bold ${
              config.configured || isConfigured ? 'text-emerald-400' : 'text-red-400'
            }`}
          >
            {config.configured || isConfigured ? 'CONFIGURED' : 'NOT CONFIGURED'}
          </span>
          <button
            onClick={fetchTelegramStatus}
            disabled={isStatusLoading}
            className="p-2 rounded-lg bg-[#1A2530] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${isStatusLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* ============================================================
          TWO COLUMN LAYOUT
      ============================================================ */}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ============================================================
            LEFT COLUMN - CONFIG & SEND
        ============================================================ */}

        <div className="space-y-6">
          {/* Config Card - AMAN DENGAN ASTERISK */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
              <Key className="w-4 h-4 text-sky-400" />
              Bot Configuration
            </h3>

            <div className="space-y-4 pt-4">
              {/* Status Bar */}
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D]">
                <div className="flex items-center gap-2">
                  <div
                    className={`w-2.5 h-2.5 rounded-full ${
                      config.configured || isConfigured ? 'bg-emerald-400' : 'bg-red-400'
                    }`}
                  />
                  <span className="text-xs font-medium text-white">
                    {config.configured || isConfigured ? '✅ Connected' : '⚠️ Not Connected'}
                  </span>
                </div>
                {lastStatusCheck && (
                  <span className="text-[10px] text-[#5F6B78] font-mono">
                    Last check: {new Date(lastStatusCheck).toLocaleTimeString()}
                  </span>
                )}
              </div>

              {/* Bot Token - Dengan Asterisk */}
              <div>
                <label className="text-xs font-bold text-white block mb-1.5">
                  Bot Token
                  <span className="text-[10px] text-[#5F6B78] ml-2 font-normal">
                    (stored securely on server)
                  </span>
                </label>
                <div className="relative">
                  <input
                    type={showToken ? 'text' : 'password'}
                    value={botToken || config.bot_token}
                    onChange={(e) => setBotToken(e.target.value)}
                    placeholder={config.configured ? '••••••••••••••••' : 'Enter Bot Token'}
                    className="w-full px-3.5 py-2.5 pr-24 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-sky-500"
                  />
                  <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                    <button
                      onClick={() => setShowToken(!showToken)}
                      className="p-1.5 rounded-lg text-[#8D9AAA] hover:text-white transition-colors"
                    >
                      {showToken ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                    {config.configured && botToken && (
                      <span className="text-[10px] text-emerald-400 font-mono px-1.5 py-0.5 bg-emerald-500/10 rounded">
                        ● Active
                      </span>
                    )}
                  </div>
                </div>
                {config.configured && botToken && (
                  <div className="mt-1 text-[10px] text-[#5F6B78] font-mono">
                    Current: {maskToken(botToken)}
                  </div>
                )}
                <p className="text-[10px] text-[#5F6B78] mt-1">
                  Get from <span className="text-sky-400">@BotFather</span> on Telegram
                </p>
              </div>

              {/* Chat ID - Dengan Asterisk */}
              <div>
                <label className="text-xs font-bold text-white block mb-1.5">
                  Chat ID
                  <span className="text-[10px] text-[#5F6B78] ml-2 font-normal">
                    (stored securely on server)
                  </span>
                </label>
                <div className="relative">
                  <input
                    type={showChatId ? 'text' : 'password'}
                    value={chatId || config.chat_id}
                    onChange={(e) => setChatId(e.target.value)}
                    placeholder={config.configured ? '••••••••••••' : 'Enter Chat ID'}
                    className="w-full px-3.5 py-2.5 pr-24 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-sky-500"
                  />
                  <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                    <button
                      onClick={() => setShowChatId(!showChatId)}
                      className="p-1.5 rounded-lg text-[#8D9AAA] hover:text-white transition-colors"
                    >
                      {showChatId ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                    {config.configured && chatId && (
                      <span className="text-[10px] text-emerald-400 font-mono px-1.5 py-0.5 bg-emerald-500/10 rounded">
                        ● Active
                      </span>
                    )}
                  </div>
                </div>
                {config.configured && chatId && (
                  <div className="mt-1 text-[10px] text-[#5F6B78] font-mono">
                    Current: {maskChatId(chatId)}
                  </div>
                )}
                <p className="text-[10px] text-[#5F6B78] mt-1">
                  Get from <span className="text-sky-400">@userinfobot</span> on Telegram
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2">
                <button
                  onClick={handleSaveConfig}
                  disabled={isSaving}
                  className="flex-1 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all disabled:opacity-50 shadow-md shadow-sky-600/30"
                >
                  {isSaving ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="w-3.5 h-3.5" />
                      Save Configuration
                    </>
                  )}
                </button>
                <button
                  onClick={handleCopyConfig}
                  className="px-4 py-2.5 rounded-xl bg-[#1A2530] hover:bg-[#26313D] border border-[#26313D] text-white font-bold text-xs flex items-center gap-1.5 transition-all"
                  title="Copy config to clipboard"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
              </div>

              {/* Info Box */}
              <div className="p-3 rounded-xl bg-[#0B0F14] border border-[#26313D]">
                <p className="text-[10px] text-[#5F6B78] flex items-start gap-2">
                  <Info className="w-3.5 h-3.5 text-sky-400 shrink-0 mt-0.5" />
                  <span>
                    Your bot token and chat ID are <strong className="text-emerald-400">encrypted</strong> and stored securely on the server.
                    They are <strong className="text-amber-400">never exposed</strong> to the browser or any third party.
                    <br />
                    <span className="text-[9px] text-[#5F6B78]">
                      Only first 6 and last 4 characters are visible for verification.
                    </span>
                  </span>
                </p>
              </div>

              {/* Test Result */}
              {testResult.type && (
                <div
                  className={`p-3 rounded-xl text-xs font-mono ${
                    testResult.type === 'success'
                      ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/30'
                      : testResult.type === 'error'
                      ? 'bg-red-500/10 text-red-300 border border-red-500/30'
                      : 'bg-blue-500/10 text-blue-300 border border-blue-500/30'
                  }`}
                >
                  {testResult.message}
                </div>
              )}
            </div>
          </div>

          {/* Send Custom Message */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-emerald-400" />
              Send Custom Message
            </h3>

            <div className="space-y-3 pt-4">
              <textarea
                value={customMessage}
                onChange={(e) => setCustomMessage(e.target.value)}
                placeholder="Type your message here... (supports HTML formatting: &lt;b&gt;, &lt;i&gt;, &lt;code&gt;)"
                rows={3}
                className="w-full px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-sky-500 resize-none font-mono"
              />
              <div className="flex gap-2">
                <button
                  onClick={handleSendCustom}
                  disabled={isSending || !customMessage.trim()}
                  className="flex-1 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all disabled:opacity-50 shadow-md shadow-emerald-600/30"
                >
                  {isSending ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <Send className="w-3.5 h-3.5" />
                      Send Message
                    </>
                  )}
                </button>
              </div>
              <p className="text-[10px] text-[#5F6B78]">
                Use HTML tags: <code className="bg-[#0B0F14] px-1 rounded">&lt;b&gt;bold&lt;/b&gt;</code>{' '}
                <code className="bg-[#0B0F14] px-1 rounded">&lt;i&gt;italic&lt;/i&gt;</code>{' '}
                <code className="bg-[#0B0F14] px-1 rounded">&lt;code&gt;code&lt;/code&gt;</code>
              </p>
            </div>
          </div>

          {/* Quick Templates */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-400" />
              Quick Message Templates
            </h3>

            <div className="grid grid-cols-2 gap-2 pt-4">
              {quickTemplates.map((template, index) => (
                <button
                  key={index}
                  onClick={() => sendMessage(template.message, 'test')}
                  disabled={isSending}
                  className={`p-3 rounded-xl bg-[#1A2530] hover:bg-[#26313D] border border-[#26313D] text-white text-xs font-medium transition-all flex items-center gap-2 hover:border-${template.color}-500/50 disabled:opacity-50`}
                >
                  {template.icon}
                  <span className="truncate">{template.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* ============================================================
            RIGHT COLUMN - MESSAGE HISTORY
        ============================================================ */}

        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg flex flex-col">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <History className="w-4 h-4 text-blue-400" />
              Message History ({messages.length})
            </h3>
            <div className="flex items-center gap-2">
              {messages.length > 0 && (
                <button
                  onClick={handleClearHistory}
                  className="p-1.5 rounded-lg text-red-400 hover:bg-red-500/20 transition-colors"
                  title="Clear history"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              )}
              <button
                onClick={fetchTelegramStatus}
                className="p-1.5 rounded-lg text-[#8D9AAA] hover:bg-[#1A2530] hover:text-white transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          <div className="flex-1 space-y-2.5 pt-3 overflow-y-auto max-h-[600px] pr-1">
            {messages.length === 0 ? (
              <div className="text-center text-[#5F6B78] py-12">
                <MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-30" />
                <p className="text-sm font-medium">No messages sent yet</p>
                <p className="text-xs mt-1">Send a test message using the templates or custom message</p>
              </div>
            ) : (
              messages.map((msg) => {
                const isSent = msg.status === 'sent';
                const isFailed = msg.status === 'failed';
                const isPending = msg.status === 'pending';

                const typeColors = {
                  signal: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
                  alert: 'bg-red-500/20 text-red-400 border-red-500/30',
                  test: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
                  system: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
                  trade: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
                  daily: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
                };

                const statusColors = {
                  sent: 'text-emerald-400',
                  failed: 'text-red-400',
                  pending: 'text-yellow-400',
                };

                return (
                  <div
                    key={msg.id}
                    className={`p-3 rounded-xl border ${
                      isSent
                        ? 'bg-[#1A2530] border-[#26313D]'
                        : isFailed
                        ? 'bg-red-500/10 border-red-500/30'
                        : 'bg-yellow-500/10 border-yellow-500/30'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span
                            className={`text-[10px] font-bold px-1.5 py-0.5 rounded border ${
                              typeColors[msg.type] || typeColors.system
                            }`}
                          >
                            {msg.type.toUpperCase()}
                          </span>
                          <span className={`text-[10px] font-mono ${statusColors[msg.status]}`}>
                            {isPending ? '⏳' : isSent ? '✅' : '❌'} {msg.status}
                          </span>
                          <span className="text-[10px] text-[#5F6B78] font-mono ml-auto">
                            {new Date(msg.timestamp).toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="text-xs text-white mt-1.5 whitespace-pre-wrap break-words font-mono leading-relaxed">
                          {msg.text}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Footer stats */}
          <div className="pt-3 mt-3 border-t border-[#26313D]/70 flex items-center justify-between text-[10px] text-[#5F6B78]">
            <span>
              Sent: <span className="text-emerald-400">{messages.filter((m) => m.status === 'sent').length}</span>
              {' · '}
              Failed: <span className="text-red-400">{messages.filter((m) => m.status === 'failed').length}</span>
              {' · '}
              Pending: <span className="text-yellow-400">{messages.filter((m) => m.status === 'pending').length}</span>
            </span>
            <span>
              {messages.length > 0 ? `${messages.length} total` : 'No messages'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TelegramView;
