// src/components/TelegramView.tsx
// TELEGRAM VIEW v3.1 - LAYOUT DIPERBAIKI

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Send,
  Shield,
  Key,
  RefreshCw,
  History,
  Clock,
  MessageSquare,
  Zap,
  Activity,
  TrendingUp,
  TrendingDown,
  Trash2,
  Copy,
  Save,
  Eye,
  EyeOff,
  Info,
  AlertTriangle,
  Check,
  Loader2,
  Brain,
  BarChart3,
  Signal,
  Target,
  Rocket,
  Layers,
  Database,
  Server,
  Cpu,
  HardDrive,
  Gauge,
  Play,
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface TelegramMessage {
  id: string;
  text: string;
  timestamp: string;
  status: 'sent' | 'failed' | 'pending';
  type: 'start' | 'performance' | 'health' | 'signal' | 'pnl' | 'brain' | 'modules' | 'daily' | 'risk' | 'trade' | 'refresh' | 'custom';
}

interface SystemMetrics {
  cpu: number;
  ram: number;
  uptime: number;
  health_score: number;
  risk_level: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  memory_count: number;
  knowledge_count: number;
  pnl: number;
  win_rate: number;
  total_trades: number;
  prediction_accuracy: number;
  open_positions: number;
}

interface ModuleStatus {
  name: string;
  title: string;
  version: string;
  status: 'ONLINE' | 'OFFLINE' | 'DEGRADED';
  priority: number;
  role: string;
  online: boolean;
}

interface LearningStats {
  cycle_count: number;
  learning_active: boolean;
  learning_rate: number;
  decay_rate: number;
  circuit_breakers: number;
  modules_count: number;
}

interface AdaptiveWeight {
  key: string;
  domain: string;
  weight: number;
  confidence: number;
  reliability: number;
  successRate: number;
  attempts: number;
  trend?: 'up' | 'down' | 'stable';
}

interface TelegramViewProps {
  isConfigured?: boolean;
  onSaveConfig?: (token: string, chatId: string) => void;
}

// ============================================================
// API SERVICE
// ============================================================

const API_BASE = '/api';

const api = {
  async getStatus(): Promise<{ configured: boolean; status: string; bot_name: string }> {
    const response = await fetch(`${API_BASE}/telegram/status`);
    if (!response.ok) throw new Error('Failed to get status');
    return response.json();
  },

  async getConfig(): Promise<{ bot_token: string; chat_id: string; configured: boolean }> {
    const response = await fetch(`${API_BASE}/telegram/config`);
    if (!response.ok) throw new Error('Failed to get config');
    return response.json();
  },

  async saveConfig(botToken: string, chatId: string): Promise<{ status: string; message: string }> {
    const response = await fetch(`${API_BASE}/telegram/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bot_token: botToken, chat_id: chatId }),
    });
    if (!response.ok) throw new Error('Failed to save config');
    return response.json();
  },

  async sendMessage(message: string): Promise<{ sent: boolean; status: string; message: string }> {
    const response = await fetch(`${API_BASE}/telegram/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
  },

  async testConnection(): Promise<{ status: string; message: string; sent: boolean }> {
    const response = await fetch(`${API_BASE}/telegram/test`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Test failed');
    return response.json();
  },

  async getSystemMetrics(): Promise<SystemMetrics> {
    const response = await fetch(`${API_BASE}/system/metrics`);
    if (!response.ok) throw new Error('Failed to get system metrics');
    return response.json();
  },

  async getModules(): Promise<ModuleStatus[]> {
    const response = await fetch(`${API_BASE}/modules/list`);
    if (!response.ok) throw new Error('Failed to get modules');
    const data = await response.json();
    return data.modules || [];
  },

  async getLearningStats(): Promise<LearningStats> {
    const response = await fetch(`${API_BASE}/learning/stats`);
    if (!response.ok) throw new Error('Failed to get learning stats');
    return response.json();
  },

  async getAdaptiveWeights(): Promise<AdaptiveWeight[]> {
    const response = await fetch(`${API_BASE}/learning/adaptive`);
    if (!response.ok) throw new Error('Failed to get adaptive weights');
    const data = await response.json();
    return data.entries || [];
  },

  async getEvaluatorStats(): Promise<any> {
    const response = await fetch(`${API_BASE}/learning/evaluator`);
    if (!response.ok) throw new Error('Failed to get evaluator stats');
    return response.json();
  },

  async getBrainState(): Promise<any> {
    const response = await fetch(`${API_BASE}/brain/state`);
    if (!response.ok) throw new Error('Failed to get brain state');
    return response.json();
  },
};

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

const formatUptime = (seconds: number): string => {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  if (days > 0) return `${days}d ${hours}h ${minutes}m`;
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
};

const getRiskEmoji = (risk: string): string => {
  switch (risk) {
    case 'LOW': return '🟢';
    case 'MODERATE': return '🟡';
    case 'HIGH': return '🟠';
    case 'CRITICAL': return '🔴';
    default: return '⚪';
  }
};

// ============================================================
// COMPONENT
// ============================================================

export function TelegramView({ isConfigured: propConfigured, onSaveConfig: propOnSaveConfig }: TelegramViewProps) {
  // ============================================================
  // STATE
  // ============================================================

  const [botToken, setBotToken] = useState('');
  const [chatId, setChatId] = useState('');
  const [showToken, setShowToken] = useState(false);
  const [showChatId, setShowChatId] = useState(false);
  const [isConfigured, setIsConfigured] = useState(propConfigured || false);
  const [isSaving, setIsSaving] = useState(false);
  const [isTestRunning, setIsTestRunning] = useState(false);

  const [messages, setMessages] = useState<TelegramMessage[]>([]);
  const [customMessage, setCustomMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [result, setResult] = useState<{ type: 'success' | 'error' | 'info' | null; message: string }>({
    type: null,
    message: '',
  });

  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [modules, setModules] = useState<ModuleStatus[]>([]);
  const [learningStats, setLearningStats] = useState<LearningStats | null>(null);
  const [adaptiveWeights, setAdaptiveWeights] = useState<AdaptiveWeight[]>([]);
  const [evaluatorStats, setEvaluatorStats] = useState<any>(null);
  const [brainState, setBrainState] = useState<any>(null);
  const [isLoadingData, setIsLoadingData] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const autoRefreshInterval = useRef<NodeJS.Timeout | null>(null);

  // ============================================================
  // LOAD DATA
  // ============================================================

  const loadAllData = useCallback(async () => {
    try {
      setIsLoadingData(true);
      const [metricsData, modulesData, learningData, weightsData, evalData, brainData] = await Promise.all([
        api.getSystemMetrics(),
        api.getModules(),
        api.getLearningStats(),
        api.getAdaptiveWeights(),
        api.getEvaluatorStats(),
        api.getBrainState(),
      ]);
      setMetrics(metricsData);
      setModules(modulesData);
      setLearningStats(learningData);
      setAdaptiveWeights(weightsData);
      setEvaluatorStats(evalData);
      setBrainState(brainData);
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setIsLoadingData(false);
    }
  }, []);

  const loadConfig = useCallback(async () => {
    try {
      const config = await api.getConfig();
      setIsConfigured(config.configured || false);
      if (config.configured) {
        setBotToken(config.bot_token || '');
        setChatId(config.chat_id || '');
      }
    } catch (error) {
      console.error('Failed to load config:', error);
    }
  }, []);

  const loadStatus = useCallback(async () => {
    try {
      const status = await api.getStatus();
      setIsConfigured(status.configured || false);
    } catch (error) {
      console.error('Failed to load status:', error);
    }
  }, []);

  // ============================================================
  // INITIALIZATION
  // ============================================================

  useEffect(() => {
    loadConfig();
    loadAllData();
    loadStatus();

    const savedMessages = localStorage.getItem('telegram_messages_real');
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch (e) {
        console.error('Failed to load messages:', e);
      }
    }

    autoRefreshInterval.current = setInterval(() => {
      loadAllData();
      loadStatus();
    }, 30000);

    return () => {
      if (autoRefreshInterval.current) {
        clearInterval(autoRefreshInterval.current);
      }
    };
  }, [loadConfig, loadAllData, loadStatus]);

  useEffect(() => {
    localStorage.setItem('telegram_messages_real', JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // ============================================================
  // SEND MESSAGE
  // ============================================================

  const sendMessage = async (text: string, type: TelegramMessage['type'] = 'custom') => {
    if (!text.trim()) {
      setResult({ type: 'error', message: '❌ Message cannot be empty.' });
      return;
    }

    if (!isConfigured) {
      setResult({ type: 'error', message: '❌ Telegram is not configured.' });
      return;
    }

    setIsSending(true);
    setResult({ type: null, message: '' });

    const pendingMessage: TelegramMessage = {
      id: `msg-${Date.now()}`,
      text: text,
      timestamp: new Date().toISOString(),
      status: 'pending',
      type: type,
    };
    setMessages((prev) => [pendingMessage, ...prev]);

    try {
      const response = await api.sendMessage(text);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === pendingMessage.id
            ? { ...msg, status: response.sent ? 'sent' : 'failed' }
            : msg
        )
      );
      if (response.sent) {
        setResult({ type: 'success', message: '✅ Message sent successfully!' });
      } else {
        setResult({ type: 'error', message: `❌ Failed to send: ${response.message || 'Unknown error'}` });
      }
    } catch (error: any) {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === pendingMessage.id ? { ...msg, status: 'failed' } : msg
        )
      );
      setResult({ type: 'error', message: `❌ Error: ${error.message}` });
    } finally {
      setIsSending(false);
    }
  };

  // ============================================================
  // HANDLERS
  // ============================================================

  const handleSaveConfig = async () => {
    const token = botToken.trim();
    const chatIdValue = chatId.trim();

    if (!token || !chatIdValue) {
      setResult({ type: 'error', message: '❌ Please enter both Bot Token and Chat ID.' });
      return;
    }

    setIsSaving(true);
    setResult({ type: null, message: '' });

    try {
      const response = await api.saveConfig(token, chatIdValue);
      if (response.status === 'success') {
        setIsConfigured(true);
        setResult({ type: 'success', message: '✅ Configuration saved! Restart backend to apply.' });
        if (propOnSaveConfig) propOnSaveConfig(token, chatIdValue);
        await loadStatus();
      } else {
        setResult({ type: 'error', message: `❌ Failed to save: ${response.message}` });
      }
    } catch (error: any) {
      setResult({ type: 'error', message: `❌ Error: ${error.message}` });
    } finally {
      setIsSaving(false);
    }
  };

  const handleTestConnection = async () => {
    setIsTestRunning(true);
    setResult({ type: null, message: '' });
    try {
      const response = await api.testConnection();
      if (response.status === 'success') {
        setResult({ type: 'success', message: `✅ ${response.message}` });
      } else {
        setResult({ type: 'error', message: `❌ ${response.message}` });
      }
    } catch (error: any) {
      setResult({ type: 'error', message: `❌ Error: ${error.message}` });
    } finally {
      setIsTestRunning(false);
    }
  };

  const handleSendCustom = () => {
    if (!customMessage.trim()) return;
    sendMessage(customMessage.trim(), 'custom');
    setCustomMessage('');
  };

  const handleClearHistory = () => {
    if (window.confirm('Clear all message history?')) {
      setMessages([]);
      localStorage.removeItem('telegram_messages_real');
      setResult({ type: 'info', message: '🗑️ Message history cleared.' });
    }
  };

  const handleCopyConfig = () => {
    const configText = `TELEGRAM_BOT_TOKEN=${botToken || 'your_token_here'}\nTELEGRAM_CHAT_ID=${chatId || 'your_chat_id_here'}`;
    navigator.clipboard?.writeText(configText).then(() => {
      setResult({ type: 'info', message: '✅ Config copied to clipboard!' });
      setTimeout(() => setResult({ type: null, message: '' }), 3000);
    });
  };

  // ============================================================
  // TEMPLATES
  // ============================================================

  const getTemplates = () => {
    const m = metrics;
    const l = learningStats;
    const e = evaluatorStats;
    const mods = modules;
    const brain = brainState;
    const weights = adaptiveWeights;

    return [
      {
        id: 'start',
        label: '🚀 Start',
        icon: <Play className="w-4 h-4" />,
        color: 'emerald',
        message: () => {
          const onlineModules = mods.filter(mod => mod.online).length;
          const totalModules = mods.length;
          const topSignal = weights.length > 0 ? weights[0] : null;
          return `🚀 <b>INKSIDE DIGITAL - SYSTEM OVERVIEW</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n<b>🖥️ SYSTEM STATUS</b>\nHealth: ${m?.health_score || 0}% ${getRiskEmoji(m?.risk_level || 'UNKNOWN')}\nRisk: ${m?.risk_level || 'UNKNOWN'}\nUptime: ${formatUptime(m?.uptime || 0)}\n\n<b>📊 PERFORMANCE</b>\nTrades: ${m?.total_trades || 0}\nWin Rate: ${m?.win_rate || 0}%\nPnL: ${m?.pnl ? (m.pnl > 0 ? '+' : '') + m.pnl.toFixed(2) : '0.00'}\n\n<b>🧠 BRAIN & MEMORY</b>\nMemory: ${m?.memory_count || 0} items\nKnowledge: ${m?.knowledge_count || 0} items\nLearning: ${l?.learning_active ? '🟢 ACTIVE' : '🔴 IDLE'}\n\n<b>🔌 MODULES</b>\nOnline: ${onlineModules}/${totalModules}\nCircuit Breakers: ${l?.circuit_breakers || 0}\n\n<b>🎯 TOP SIGNAL</b>\n${topSignal ? `${topSignal.key}\nConfidence: ${topSignal.confidence}% | Success: ${topSignal.successRate}%` : 'No signals available'}\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`;
        },
      },
      {
        id: 'performance',
        label: '📊 Perf',
        icon: <BarChart3 className="w-4 h-4" />,
        color: 'blue',
        message: () => `📊 <b>PERFORMANCE REPORT</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n<b>📈 TRADING STATS</b>\nTotal Trades: ${m?.total_trades || 0}\nWin Rate: ${m?.win_rate || 0}%\nTotal PnL: ${m?.pnl ? (m.pnl > 0 ? '+' : '') + m.pnl.toFixed(2) : '0.00'}\nOpen Positions: ${m?.open_positions || 0}\n\n<b>🎯 PREDICTION</b>\nAccuracy: ${m?.prediction_accuracy || 0}%\nEvaluations: ${e?.total_evaluations || 0}\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`,
      },
      {
        id: 'health',
        label: '🩺 Health',
        icon: <Activity className="w-4 h-4" />,
        color: 'green',
        message: () => {
          const onlineModules = mods.filter(mod => mod.online).length;
          const totalModules = mods.length;
          const health = m?.health_score || 0;
          const status = health >= 80 ? '🟢 EXCELLENT' : health >= 60 ? '🟡 GOOD' : health >= 40 ? '🟠 WARNING' : '🔴 CRITICAL';
          return `🩺 <b>SYSTEM HEALTH CHECK</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n<b>📊 OVERALL HEALTH</b>\nScore: ${health}%\nStatus: ${status}\nRisk Level: ${getRiskEmoji(m?.risk_level || 'UNKNOWN')} ${m?.risk_level || 'UNKNOWN'}\nUptime: ${formatUptime(m?.uptime || 0)}\n\n<b>💻 RESOURCES</b>\nCPU: ${m?.cpu || 0}%\nRAM: ${m?.ram || 0} GB\n\n<b>🔌 MODULES</b>\nOnline: ${onlineModules}/${totalModules}\nLearning: ${l?.learning_active ? '🟢 ACTIVE' : '🔴 IDLE'}\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`;
        },
      },
      {
        id: 'signal',
        label: '🎯 Signals',
        icon: <Signal className="w-4 h-4" />,
        color: 'purple',
        message: () => {
          const topWeights = weights.slice(0, 5);
          if (topWeights.length === 0) {
            return `🎯 <b>TRADING SIGNALS</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n⚠️ No signals available.\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`;
          }
          let signalText = `🎯 <b>LIVE TRADING SIGNALS</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n`;
          topWeights.forEach((w, i) => {
            const trend = w.trend === 'up' ? '📈' : w.trend === 'down' ? '📉' : '➡️';
            signalText += `<b>${i+1}. ${w.key}</b>\n   Confidence: ${w.confidence}% ${trend}\n   Success Rate: ${w.successRate}%\n   Attempts: ${w.attempts}\n\n`;
          });
          signalText += `━━━━━━━━━━━━━━━━━━━━━\nTotal Signals: ${weights.length}\n🕐 ${new Date().toLocaleString()}`;
          return signalText;
        },
      },
      {
        id: 'pnl',
        label: '📈 PnL',
        icon: <TrendingUp className="w-4 h-4" />,
        color: 'emerald',
        message: () => {
          const pnl = m?.pnl || 0;
          return `📈 <b>PROFIT / LOSS REPORT</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n<b>💰 PNL SUMMARY</b>\nTotal PnL: ${pnl > 0 ? '+' : ''}${pnl.toFixed(2)}\nWin Rate: ${m?.win_rate || 0}%\nTotal Trades: ${m?.total_trades || 0}\nOpen Positions: ${m?.open_positions || 0}\n\n<b>📊 STATUS</b>\n${pnl > 0 ? '✅ PROFITABLE' : '❌ LOSING'}\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`;
        },
      },
      {
        id: 'brain',
        label: '🧠 Brain',
        icon: <Brain className="w-4 h-4" />,
        color: 'purple',
        message: () => `🧠 <b>COGNITIVE BRAIN STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n<b>🧠 BRAIN STATE</b>\nState: ${brain?.brain?.state || 'UNKNOWN'}\nLearning: ${l?.learning_active ? '🟢 ACTIVE' : '🔴 IDLE'}\nCycles: ${l?.cycle_count || 0}\n\n<b>📊 METRICS</b>\nMemory: ${m?.memory_count || 0} items\nKnowledge: ${m?.knowledge_count || 0} items\nAccuracy: ${e?.accuracy || 0}%\n\n<b>📋 MODULES</b>\nTotal: ${modules.length}\nOnline: ${modules.filter(m => m.online).length}\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`,
      },
      {
        id: 'modules',
        label: '🔌 Mods',
        icon: <Layers className="w-4 h-4" />,
        color: 'cyan',
        message: () => {
          const online = mods.filter(mod => mod.online);
          const offline = mods.filter(mod => !mod.online);
          let msg = `🔌 <b>MODULE STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━\n\nTotal: ${mods.length}\nOnline: ${online.length} 🟢\nOffline: ${offline.length} 🔴\n\n<b>✅ ONLINE MODULES</b>\n`;
          online.slice(0, 8).forEach(mod => {
            msg += `🟢 ${mod.title} v${mod.version}\n`;
          });
          if (online.length > 8) msg += `... and ${online.length - 8} more\n`;
          if (offline.length > 0) {
            msg += `\n<b>❌ OFFLINE MODULES</b>\n`;
            offline.slice(0, 5).forEach(mod => {
              msg += `🔴 ${mod.title}\n`;
            });
            if (offline.length > 5) msg += `... and ${offline.length - 5} more\n`;
          }
          msg += `\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`;
          return msg;
        },
      },
      {
        id: 'daily',
        label: '📅 Daily',
        icon: <Clock className="w-4 h-4" />,
        color: 'yellow',
        message: () => `📅 <b>DAILY REPORT</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n<b>📊 TODAY'S SUMMARY</b>\nDate: ${new Date().toLocaleDateString()}\nTrades: ${m?.total_trades || 0}\nWin Rate: ${m?.win_rate || 0}%\nPnL: ${m?.pnl ? (m.pnl > 0 ? '+' : '') + m.pnl.toFixed(2) : '0.00'}\n\n<b>🖥️ SYSTEM</b>\nHealth: ${m?.health_score || 0}%\nRisk: ${m?.risk_level || 'UNKNOWN'}\nModules Online: ${modules.filter(m => m.online).length}/${modules.length}\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`,
      },
      {
        id: 'risk',
        label: '🛡️ Risk',
        icon: <Shield className="w-4 h-4" />,
        color: 'orange',
        message: () => `🛡️ <b>RISK ASSESSMENT</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n<b>📊 RISK METRICS</b>\nRisk Level: ${getRiskEmoji(m?.risk_level || 'UNKNOWN')} ${m?.risk_level || 'UNKNOWN'}\nHealth Score: ${m?.health_score || 0}%\nCircuit Breakers: ${l?.circuit_breakers || 0}\nOpen Positions: ${m?.open_positions || 0}\n\n<b>💻 RESOURCES</b>\nCPU: ${m?.cpu || 0}%\nRAM: ${m?.ram || 0} GB\n\n<b>⚠️ STATUS</b>\n${m?.risk_level === 'LOW' ? '✅ System is safe' :
  m?.risk_level === 'MODERATE' ? '⚠️ Monitor closely' :
  m?.risk_level === 'HIGH' ? '🔴 High risk - Take action!' :
  '🚨 CRITICAL - Immediate action required!'}\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`,
      },
      {
        id: 'trade',
        label: '⚡ Trade',
        icon: <Rocket className="w-4 h-4" />,
        color: 'amber',
        message: () => {
          const topSignal = weights.length > 0 ? weights[0] : null;
          return `⚡ <b>QUICK TRADE ACTION</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n<b>🎯 SIGNAL</b>\n${topSignal ? `${topSignal.key}\nConfidence: ${topSignal.confidence}%\nSuccess Rate: ${topSignal.successRate}%` : 'No signal available'}\n\n<b>📊 RECOMMENDATION</b>\n${topSignal ? (topSignal.confidence > 70 ? '🟢 BUY / LONG' : '🔴 SELL / SHORT') : '⚠️ Wait for signal'}\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`;
        },
      },
      {
        id: 'refresh',
        label: '🔄 Refresh',
        icon: <RefreshCw className="w-4 h-4" />,
        color: 'blue',
        message: () => `🔄 <b>DATA REFRESHED</b>\n━━━━━━━━━━━━━━━━━━━━━\n\n✅ All data has been refreshed.\n\n<b>📊 LATEST METRICS</b>\nHealth: ${m?.health_score || 0}%\nRisk: ${m?.risk_level || 'UNKNOWN'}\nTrades: ${m?.total_trades || 0}\nWin Rate: ${m?.win_rate || 0}%\nPnL: ${m?.pnl ? (m.pnl > 0 ? '+' : '') + m.pnl.toFixed(2) : '0.00'}\n\n<b>🔌 MODULES</b>\nOnline: ${modules.filter(m => m.online).length}/${modules.length}\n━━━━━━━━━━━━━━━━━━━━━\n🕐 ${new Date().toLocaleString()}`,
      },
    ];
  };

  const templates = getTemplates();

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="space-y-6 pb-12">
      {/* HEADER */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] via-[#18212B] to-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-sky-600/20 border border-sky-500/30 flex items-center justify-center text-sky-400">
            <Send className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Telegram Bridge v3.1
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              {templates.length} Commands • Real-time data • {isConfigured ? '✅ Connected' : '⚠️ Not Configured'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 flex-wrap">
          <span className={`w-2.5 h-2.5 rounded-full ${isConfigured ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'}`} />
          <span className={`text-xs font-bold ${isConfigured ? 'text-emerald-400' : 'text-red-400'}`}>
            {isConfigured ? 'CONFIGURED' : 'NOT CONFIGURED'}
          </span>
          <button
            onClick={() => { loadAllData(); loadStatus(); }}
            disabled={isLoadingData}
            className="p-2 rounded-lg bg-[#1A2530] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${isLoadingData ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* SYSTEM STATUS BAR - DIPERBAIKI */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[10px] text-[#5F6B78]">Health</div>
          <div className="text-lg font-bold text-white">{metrics?.health_score || 0}%</div>
          <div className="text-[10px] text-[#8D9AAA]">{metrics?.risk_level || '--'}</div>
        </div>
        <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[10px] text-[#5F6B78]">Trades</div>
          <div className="text-lg font-bold text-white">{metrics?.total_trades || 0}</div>
          <div className="text-[10px] text-[#8D9AAA]">Win: {metrics?.win_rate || 0}%</div>
        </div>
        <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[10px] text-[#5F6B78]">PnL</div>
          <div className={`text-lg font-bold ${(metrics?.pnl || 0) > 0 ? 'text-emerald-400' : (metrics?.pnl || 0) < 0 ? 'text-red-400' : 'text-white'}`}>
            {(metrics?.pnl || 0) > 0 ? '+' : ''}{(metrics?.pnl || 0).toFixed(2)}
          </div>
          <div className="text-[10px] text-[#8D9AAA]">Positions: {metrics?.open_positions || 0}</div>
        </div>
        <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[10px] text-[#5F6B78]">Modules</div>
          <div className="text-lg font-bold text-emerald-400">{modules.filter(m => m.online).length}/{modules.length}</div>
          <div className="text-[10px] text-[#8D9AAA]">Online / Total</div>
        </div>
        <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[10px] text-[#5F6B78]">Uptime</div>
          <div className="text-lg font-bold text-white">{formatUptime(metrics?.uptime || 0)}</div>
          <div className="text-[10px] text-[#8D9AAA]">{learningStats?.learning_active ? '🟢 Learning Active' : '🔴 Idle'}</div>
        </div>
      </div>

      {/* TWO COLUMN LAYOUT */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* LEFT COLUMN */}
        <div className="space-y-6">
          {/* Config Card - DIPERBAIKI (Engine Status dihapus dari sini) */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
              <Key className="w-4 h-4 text-sky-400" />
              Bot Configuration
            </h3>

            <div className="space-y-4 pt-4">
              <div className="p-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] flex items-center justify-between">
                <span className="text-xs text-[#8D9AAA]">Status:</span>
                <span className={`text-xs font-bold ${isConfigured ? 'text-emerald-400' : 'text-red-400'}`}>
                  {isConfigured ? '✅ Connected' : '⚠️ Not Connected'}
                </span>
              </div>

              <div>
                <label className="text-xs font-bold text-white block mb-1.5">Bot Token</label>
                <div className="relative">
                  <input
                    type={showToken ? 'text' : 'password'}
                    value={botToken}
                    onChange={(e) => setBotToken(e.target.value)}
                    placeholder="Enter Bot Token from @BotFather"
                    className="w-full px-3.5 py-2.5 pr-20 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-sky-500"
                  />
                  <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                    <button onClick={() => setShowToken(!showToken)} className="p-1.5 rounded-lg text-[#8D9AAA] hover:text-white">
                      {showToken ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
                {isConfigured && (
                  <div className="mt-1 text-[10px] text-[#5F6B78] font-mono">Current: {maskToken(botToken)}</div>
                )}
              </div>

              <div>
                <label className="text-xs font-bold text-white block mb-1.5">Chat ID</label>
                <div className="relative">
                  <input
                    type={showChatId ? 'text' : 'password'}
                    value={chatId}
                    onChange={(e) => setChatId(e.target.value)}
                    placeholder="Enter Chat ID from @userinfobot"
                    className="w-full px-3.5 py-2.5 pr-20 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-sky-500"
                  />
                  <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                    <button onClick={() => setShowChatId(!showChatId)} className="p-1.5 rounded-lg text-[#8D9AAA] hover:text-white">
                      {showChatId ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
                {isConfigured && (
                  <div className="mt-1 text-[10px] text-[#5F6B78] font-mono">Current: {maskChatId(chatId)}</div>
                )}
              </div>

              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={handleSaveConfig}
                  disabled={isSaving}
                  className="flex-1 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all disabled:opacity-50 shadow-md shadow-sky-600/30"
                >
                  {isSaving ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Save className="w-3.5 h-3.5" />}
                  {isSaving ? 'Saving...' : 'Save Config'}
                </button>
                <button
                  onClick={handleTestConnection}
                  disabled={isTestRunning}
                  className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-2 transition-all disabled:opacity-50 shadow-md shadow-emerald-600/30"
                >
                  {isTestRunning ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Zap className="w-3.5 h-3.5" />}
                  {isTestRunning ? 'Testing...' : 'Test'}
                </button>
                <button
                  onClick={handleCopyConfig}
                  className="px-4 py-2.5 rounded-xl bg-[#1A2530] hover:bg-[#26313D] border border-[#26313D] text-white font-bold text-xs flex items-center gap-1.5 transition-all"
                >
                  <Copy className="w-3.5 h-3.5" />
                </button>
              </div>

              {result.type && (
                <div className={`p-3 rounded-xl text-xs font-mono ${
                  result.type === 'success'
                    ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/30'
                    : result.type === 'error'
                    ? 'bg-red-500/10 text-red-300 border border-red-500/30'
                    : 'bg-blue-500/10 text-blue-300 border border-blue-500/30'
                }`}>
                  {result.message}
                </div>
              )}
            </div>
          </div>

          {/* Quick Commands */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-400" />
              Quick Commands ({templates.length})
            </h3>
            <div className="grid grid-cols-2 gap-2 pt-4">
              {templates.map((template) => (
                <button
                  key={template.id}
                  onClick={() => {
                    const msg = typeof template.message === 'function' ? template.message() : template.message;
                    sendMessage(msg, template.id as TelegramMessage['type']);
                  }}
                  disabled={isSending || !isConfigured}
                  className={`p-2.5 rounded-xl bg-[#1A2530] hover:bg-[#26313D] border border-[#26313D] text-white text-xs font-medium transition-all flex items-center gap-2 hover:border-${template.color}-500/50 disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  <span className={`text-${template.color}-400`}>{template.icon}</span>
                  <span className="truncate text-[10px]">{template.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Custom Message */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-emerald-400" />
              Custom Message
            </h3>
            <div className="space-y-3 pt-4">
              <textarea
                value={customMessage}
                onChange={(e) => setCustomMessage(e.target.value)}
                placeholder="Type your message here... (HTML supported)"
                rows={3}
                className="w-full px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-sky-500 resize-none font-mono"
              />
              <button
                onClick={handleSendCustom}
                disabled={isSending || !customMessage.trim() || !isConfigured}
                className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all disabled:opacity-50 shadow-md shadow-emerald-600/30"
              >
                {isSending ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
                {isSending ? 'Sending...' : 'Send Message'}
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN - MESSAGE HISTORY - DIPERBAIKI */}
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
                  className="p-1.5 rounded-lg bg-red-500/20 hover:bg-red-500/30 text-red-400 transition-colors flex items-center gap-1"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span className="text-[10px]">Clear</span>
                </button>
              )}
              <button
                onClick={() => { loadAllData(); loadStatus(); }}
                className="p-1.5 rounded-lg text-[#8D9AAA] hover:bg-[#1A2530] hover:text-white transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          <div className="flex-1 space-y-2.5 pt-3 overflow-y-auto max-h-[450px] pr-1">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16 text-[#5F6B78]">
                <MessageSquare className="w-12 h-12 mb-4 opacity-30" />
                <p className="text-sm font-medium">No messages sent yet</p>
                <p className="text-xs mt-1">Use the command buttons above</p>
              </div>
            ) : (
              messages.map((msg) => {
                const isSent = msg.status === 'sent';
                const isFailed = msg.status === 'failed';
                const isPending = msg.status === 'pending';

                const typeColors: Record<string, string> = {
                  start: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
                  performance: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
                  health: 'bg-green-500/20 text-green-400 border-green-500/30',
                  signal: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
                  pnl: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
                  brain: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
                  modules: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
                  daily: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
                  risk: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
                  trade: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
                  refresh: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
                  custom: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
                };

                return (
                  <div
                    key={msg.id}
                    className={`p-3 rounded-xl border ${
                      isSent ? 'bg-[#1A2530] border-[#26313D]' :
                      isFailed ? 'bg-red-500/10 border-red-500/30' :
                      'bg-yellow-500/10 border-yellow-500/30'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded border ${typeColors[msg.type] || typeColors.custom}`}>
                            {msg.type.toUpperCase()}
                          </span>
                          <span className={`text-[10px] font-mono ${isSent ? 'text-emerald-400' : isFailed ? 'text-red-400' : 'text-yellow-400'}`}>
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

          {/* FOOTER STATS - DIPERBAIKI (tetap di bawah) */}
          <div className="pt-3 mt-3 border-t border-[#26313D]/70 flex items-center justify-between text-[10px] text-[#5F6B78]">
            <span>
              Sent: <span className="text-emerald-400">{messages.filter((m) => m.status === 'sent').length}</span>
              {' · '}
              Failed: <span className="text-red-400">{messages.filter((m) => m.status === 'failed').length}</span>
              {' · '}
              Pending: <span className="text-yellow-400">{messages.filter((m) => m.status === 'pending').length}</span>
            </span>
            <span>{messages.length > 0 ? `${messages.length} total` : 'No messages'}</span>
          </div>

          {/* EXTRA SPACE & USEFUL FEATURE - BOTTOM */}
          <div className="mt-4 pt-4 border-t border-[#26313D]/40">
            <div className="flex items-center justify-between text-[10px] text-[#5F6B78]">
              <div className="flex items-center gap-2">
                <span>💡 Quick Tips:</span>
                <span className="text-[9px]">• Use commands for instant reports</span>
              </div>
              <span className="text-[9px]">
                {learningStats?.learning_active ? '🟢 Learning active' : '🔴 Idle'}
              </span>
            </div>
            <div className="flex items-center gap-4 mt-1 text-[9px] text-[#5F6B78]">
              <span>🔄 Auto-refresh: 30s</span>
              <span>📊 {modules.filter(m => m.online).length}/{modules.length} modules</span>
              <span className="text-[#3B82F6] cursor-pointer hover:underline" onClick={() => { loadAllData(); loadStatus(); }}>
                ↻ Refresh now
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* FOOTER */}
      <div className="flex items-center justify-between text-[10px] text-[#5F6B78] border-t border-[#26313D]/40 pt-4 flex-wrap gap-2">
        <span>Data source: REAL API · Last update: {lastUpdate.toLocaleString()}</span>
        <span>
          {isConfigured ? '✅ Connected' : '⚠️ Not Configured'}
          {' · '}
          {modules.filter(m => m.online).length}/{modules.length} modules online
          {' · '}
          {templates.length} commands
        </span>
      </div>
    </div>
  );
}

export default TelegramView;
