import React, { useState, useEffect } from 'react';
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
  Check,
  Save
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
  type: 'signal' | 'alert' | 'test' | 'system';
}

interface TelegramConfig {
  bot_token: string;
  chat_id: string;
  enabled: boolean;
  notifications: {
    signals: boolean;
    trades: boolean;
    health: boolean;
    errors: boolean;
  };
}

interface TelegramViewProps {
  isConfigured: boolean;
  onSaveConfig: (token: string, chatId: string) => void;
}

// ============================================================
// MAIN COMPONENT
// ============================================================

export const TelegramView: React.FC<TelegramViewProps> = ({ 
  isConfigured, 
  onSaveConfig 
}) => {
  // ============================================================
  // STATE
  // ============================================================
  
  const [botToken, setBotToken] = useState('');
  const [chatId, setChatId] = useState('');
  const [messages, setMessages] = useState<TelegramMessage[]>([]);
  const [customMessage, setCustomMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [testResult, setTestResult] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [config, setConfig] = useState<TelegramConfig>({
    bot_token: '',
    chat_id: '',
    enabled: true,
    notifications: {
      signals: true,
      trades: true,
      health: true,
      errors: true
    }
  });

  // ============================================================
  // LOAD CONFIG FROM BACKEND
  // ============================================================
  
  const loadConfig = async () => {
    try {
      const response = await fetch('/api/telegram/config');
      const data = await response.json();
      
      if (data.configured) {
        setConfig(prev => ({
          ...prev,
          bot_token: data.bot_token || '',
          chat_id: data.chat_id || '',
          enabled: true
        }));
        setBotToken(data.bot_token || '');
        setChatId(data.chat_id || '');
        setTestResult('✅ Configuration loaded from backend.');
      }
    } catch (error) {
      console.error('Failed to load config:', error);
    }
  };

  // ============================================================
  // FETCH TELEGRAM STATUS
  // ============================================================
  
  const fetchTelegramStatus = async () => {
    try {
      const status = await inksideAPI.getTelegramStatus();
      if (status.configured) {
        setConfig(prev => ({
          ...prev,
          enabled: true
        }));
        // Load config from backend
        await loadConfig();
      }
    } catch (error) {
      console.error('Failed to fetch Telegram status:', error);
    }
  };

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
  }, []);

  // Save messages to localStorage
  useEffect(() => {
    localStorage.setItem('telegram_messages', JSON.stringify(messages));
  }, [messages]);

  // ============================================================
  // SEND MESSAGE FUNCTIONS
  // ============================================================
  
  const sendMessage = async (text: string, type: TelegramMessage['type'] = 'test') => {
    setIsSending(true);
    setTestResult(null);
    
    try {
      const response = await fetch('/api/telegram/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      
      const data = await response.json();
      
      const newMessage: TelegramMessage = {
        id: `msg-${Date.now()}`,
        text: text,
        timestamp: new Date().toISOString(),
        status: data.sent ? 'sent' : 'failed',
        type: type
      };
      
      setMessages(prev => [newMessage, ...prev]);
      
      if (data.sent) {
        setTestResult('✅ Message sent successfully!');
      } else {
        setTestResult(`❌ Failed to send: ${data.message || 'Unknown error'}`);
      }
      
      return data;
    } catch (error: any) {
      const newMessage: TelegramMessage = {
        id: `msg-${Date.now()}`,
        text: text,
        timestamp: new Date().toISOString(),
        status: 'failed',
        type: type
      };
      
      setMessages(prev => [newMessage, ...prev]);
      setTestResult(`❌ Error: ${error.message}`);
      
      return { sent: false, error: error.message };
    } finally {
      setIsSending(false);
    }
  };

  // ============================================================
  // SAVE CONFIG TO BACKEND
  // ============================================================
  
  const handleSaveConfig = async () => {
    const token = botToken || config.bot_token;
    const chatIdValue = chatId || config.chat_id;
    
    if (!token || !chatIdValue) {
      setTestResult('❌ Please enter both Bot Token and Chat ID.');
      return;
    }
    
    setIsSaving(true);
    setTestResult(null);
    
    try {
      const response = await fetch('/api/telegram/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bot_token: token,
          chat_id: chatIdValue
        })
      });
      
      const data = await response.json();
      
      if (data.status === 'success') {
        setTestResult('✅ Configuration saved to backend! Restart backend to apply.');
        setConfig(prev => ({
          ...prev,
          bot_token: token,
          chat_id: chatIdValue,
          enabled: true
        }));
        // Panggil onSaveConfig untuk update parent state
        onSaveConfig(token, chatIdValue);
      } else {
        setTestResult(`❌ Failed to save: ${data.message}`);
      }
    } catch (error: any) {
      setTestResult(`❌ Error: ${error.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  // ============================================================
  // MESSAGE TEMPLATES
  // ============================================================
  
  const sendTemplate = (template: string) => {
    sendMessage(template, 'test');
  };

  const sendSignalMessage = (pair: string, signal: string, confidence: number, price: number) => {
    const emoji = signal === 'BUY' ? '📈' : signal === 'SELL' ? '📉' : '⏸️';
    const message = `
${emoji} <b>TRADING SIGNAL</b>
━━━━━━━━━━━━━━━━━━━━━
<b>Pair</b>: ${pair}
<b>Signal</b>: ${signal}
<b>Confidence</b>: ${confidence}%
<b>Price</b>: $${price.toFixed(2)}
━━━━━━━━━━━━━━━━━━━━━
<b>Time</b>: ${new Date().toLocaleString()}
    `;
    sendMessage(message.trim(), 'signal');
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
    }
  };

  const handleCopyConfig = () => {
    const token = botToken || config.bot_token;
    const chatIdValue = chatId || config.chat_id;
    const configText = `TELEGRAM_BOT_TOKEN=${token}\nTELEGRAM_CHAT_ID=${chatIdValue}`;
    navigator.clipboard?.writeText(configText).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  // ============================================================
  // QUICK MESSAGE TEMPLATES
  // ============================================================
  
  const quickTemplates = [
    {
      label: '🧠 System Health',
      icon: <Activity className="w-4 h-4" />,
      message: `🧠 <b>SYSTEM HEALTH REPORT</b>
━━━━━━━━━━━━━━━━━━━━━
<b>Status</b>: ✅ ONLINE
<b>Uptime</b>: 24h 37m
<b>Health Score</b>: 98.4%
<b>Active Modules</b>: 32/32
━━━━━━━━━━━━━━━━━━━━━
<b>Time</b>: ${new Date().toLocaleString()}`
    },
    {
      label: '📊 Performance',
      icon: <TrendingUp className="w-4 h-4" />,
      message: `📊 <b>PERFORMANCE SUMMARY</b>
━━━━━━━━━━━━━━━━━━━━━
<b>Total Trades</b>: 42
<b>Win Rate</b>: 78.5%
<b>Total PnL</b>: +$335.58
<b>ROI</b>: 3.36%
━━━━━━━━━━━━━━━━━━━━━
<b>Time</b>: ${new Date().toLocaleString()}`
    },
    {
      label: '🔴 Emergency Alert',
      icon: <AlertCircle className="w-4 h-4" />,
      message: `🔴 <b>⚠️ EMERGENCY ALERT</b>
━━━━━━━━━━━━━━━━━━━━━
<b>Type</b>: System Warning
<b>Severity</b>: HIGH
<b>Message</b>: Abnormal market conditions detected. Please check system.
━━━━━━━━━━━━━━━━━━━━━
<b>Time</b>: ${new Date().toLocaleString()}`
    },
    {
      label: '💰 Daily Summary',
      icon: <Clock className="w-4 h-4" />,
      message: `💰 <b>DAILY TRADING SUMMARY</b>
━━━━━━━━━━━━━━━━━━━━━
<b>Date</b>: ${new Date().toLocaleDateString()}
<b>Trades</b>: 12
<b>Win</b>: 9 | Loss: 3
<b>PnL</b>: +$89.50
<b>Best Trade</b>: BTC/USD +$42.30
━━━━━━━━━━━━━━━━━━━━━
<b>Report Time</b>: ${new Date().toLocaleString()}`
    }
  ];

  // ============================================================
  // RENDER
  // ============================================================
  
  return (
    <div className="space-y-6 pb-12">
      
      {/* ============================================================
          HEADER
      ============================================================ */}
      
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
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
          <span className={`w-2.5 h-2.5 rounded-full ${isConfigured || config.enabled ? 'bg-emerald-400' : 'bg-red-400'}`} />
          <span className={`text-xs font-bold ${isConfigured || config.enabled ? 'text-emerald-400' : 'text-red-400'}`}>
            {isConfigured || config.enabled ? 'CONFIGURED' : 'NOT CONFIGURED'}
          </span>
          <button
            onClick={fetchTelegramStatus}
            className="p-2 rounded-lg bg-[#1A2530] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
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
          
          {/* Config Card */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
              <Key className="w-4 h-4 text-sky-400" />
              Bot Configuration
            </h3>
            
            <div className="space-y-4 pt-4">
              <div>
                <label className="text-xs font-bold text-white block mb-1.5">
                  Bot Token
                </label>
                <input
                  type="text"
                  value={botToken || config.bot_token}
                  onChange={(e) => setBotToken(e.target.value)}
                  placeholder="Enter Telegram Bot Token..."
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-sky-500"
                />
                <p className="text-[10px] text-[#5F6B78] mt-1">
                  Get from @BotFather on Telegram
                </p>
              </div>
              
              <div>
                <label className="text-xs font-bold text-white block mb-1.5">
                  Chat ID
                </label>
                <input
                  type="text"
                  value={chatId || config.chat_id}
                  onChange={(e) => setChatId(e.target.value)}
                  placeholder="Enter Telegram Chat ID..."
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-sky-500"
                />
                <p className="text-[10px] text-[#5F6B78] mt-1">
                  Get from @userinfobot on Telegram
                </p>
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={handleSaveConfig}
                  disabled={isSaving}
                  className="flex-1 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all disabled:opacity-50 shadow-md shadow-sky-600/30"
                >
                  {isSaving ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
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
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
              </div>
              
              {testResult && (
                <div className={`p-3 rounded-xl text-xs font-mono ${
                  testResult.includes('✅') ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/30' :
                  testResult.includes('❌') ? 'bg-red-500/10 text-red-300 border border-red-500/30' :
                  'bg-blue-500/10 text-blue-300 border border-blue-500/30'
                }`}>
                  {testResult}
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
                placeholder="Type your message here... (supports HTML formatting)"
                rows={3}
                className="w-full px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-sky-500 resize-none"
              />
              <div className="flex gap-2">
                <button
                  onClick={handleSendCustom}
                  disabled={isSending || !customMessage.trim()}
                  className="flex-1 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all disabled:opacity-50 shadow-md shadow-emerald-600/30"
                >
                  {isSending ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
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
                  onClick={() => sendTemplate(template.message)}
                  disabled={isSending}
                  className="p-3 rounded-xl bg-[#1A2530] hover:bg-[#26313D] border border-[#26313D] text-white text-xs font-medium transition-all flex items-center gap-2"
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
        
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
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
          
          <div className="space-y-2.5 pt-3 max-h-[500px] overflow-y-auto pr-1">
            {messages.length === 0 ? (
              <div className="text-center text-[#5F6B78] py-8">
                <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-30" />
                <p className="text-sm">No messages sent yet</p>
                <p className="text-xs mt-1">Send a test message to start</p>
              </div>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`p-3 rounded-xl border ${
                    msg.status === 'sent' 
                      ? 'bg-[#1A2530] border-[#26313D]' 
                      : 'bg-red-500/10 border-red-500/30'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${
                          msg.type === 'signal' ? 'bg-amber-500/20 text-amber-400' :
                          msg.type === 'alert' ? 'bg-red-500/20 text-red-400' :
                          msg.type === 'test' ? 'bg-blue-500/20 text-blue-400' :
                          'bg-gray-500/20 text-gray-400'
                        }`}>
                          {msg.type.toUpperCase()}
                        </span>
                        <span className={`text-[10px] font-mono ${
                          msg.status === 'sent' ? 'text-emerald-400' : 'text-red-400'
                        }`}>
                          {msg.status === 'sent' ? '✅' : '❌'}
                        </span>
                      </div>
                      <p className="text-xs text-white mt-1.5 whitespace-pre-wrap break-words">
                        {msg.text}
                      </p>
                      <div className="flex items-center gap-3 mt-1.5">
                        <span className="text-[10px] text-[#5F6B78] font-mono">
                          {new Date(msg.timestamp).toLocaleTimeString()}
                        </span>
                        <span className={`text-[10px] font-mono ${
                          msg.status === 'sent' ? 'text-emerald-400' : 'text-red-400'
                        }`}>
                          {msg.status}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TelegramView;
