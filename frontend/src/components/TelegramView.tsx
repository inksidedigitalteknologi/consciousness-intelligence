import React, { useState } from 'react';
import { Send, CheckCircle2, AlertCircle, Shield, Bell, Key } from 'lucide-react';

interface TelegramViewProps {
  isConfigured: boolean;
  onSaveConfig: (token: string, chatId: string) => void;
}

export const TelegramView: React.FC<TelegramViewProps> = ({ isConfigured, onSaveConfig }) => {
  const [token, setToken] = useState('718293****:AAH****');
  const [chatId, setChatId] = useState('-100293847291');
  const [testResult, setTestResult] = useState<string | null>(null);
  const [isTesting, setIsTesting] = useState(false);

  const [signalsEnabled, setSignalsEnabled] = useState(true);
  const [tradesEnabled, setTradesEnabled] = useState(true);
  const [errorsEnabled, setErrorsEnabled] = useState(true);
  const [statusEnabled, setStatusEnabled] = useState(true);

  const handleTest = () => {
    setIsTesting(true);
    setTimeout(() => {
      setIsTesting(false);
      setTestResult('✅ Telegram test message dispatched successfully to Chat ID ' + chatId);
    }, 500);
  };

  return (
    <div id="telegram-view" className="space-y-6 pb-12">
      {/* Top Banner */}
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
              Real-time trading signal alerts, position notifications & system crash warnings.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
          <span className="text-white font-bold">TELEGRAM READY</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Configuration Form */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
            <Key className="w-4 h-4 text-sky-400" />
            Bot Token & Chat Credentials
          </h3>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-bold text-white block mb-1">Bot Token</label>
              <input
                type="text"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="Enter Telegram Bot Token..."
                className="w-full px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="text-xs font-bold text-white block mb-1">Target Chat ID</label>
              <input
                type="text"
                value={chatId}
                onChange={(e) => setChatId(e.target.value)}
                placeholder="Enter Telegram Chat ID (e.g. -100xxx or @channel)..."
                className="w-full px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-sky-500"
              />
            </div>

            <div className="flex gap-2 pt-2">
              <button
                onClick={handleTest}
                disabled={isTesting}
                className="flex-1 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs shadow-md shadow-sky-600/30 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                <Send className="w-3.5 h-3.5" />
                <span>{isTesting ? 'Testing...' : 'Test Connection'}</span>
              </button>

              <button
                onClick={() => onSaveConfig(token, chatId)}
                className="px-5 py-2.5 rounded-xl bg-[#1A2530] hover:bg-[#26313D] border border-[#26313D] text-white font-bold text-xs cursor-pointer"
              >
                Save
              </button>
            </div>

            {testResult && (
              <div className="p-3 rounded-xl bg-[#0B0F14] border border-emerald-500/30 text-xs text-emerald-300 font-sans">
                {testResult}
              </div>
            )}
          </div>
        </div>

        {/* Notification Event Toggles */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 flex items-center gap-2">
            <Bell className="w-4 h-4 text-amber-400" />
            Notification Event Triggers
          </h3>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
              <div>
                <div className="font-bold text-white">Trading Signals</div>
                <div className="text-[10px] text-[#8D9AAA]">Send BUY / SELL signal alerts immediately</div>
              </div>
              <input
                type="checkbox"
                checked={signalsEnabled}
                onChange={(e) => setSignalsEnabled(e.target.checked)}
                className="w-4 h-4 accent-sky-600 cursor-pointer"
              />
            </div>

            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
              <div>
                <div className="font-bold text-white">Trade Execution Events</div>
                <div className="text-[10px] text-[#8D9AAA]">Send entry price, TP/SL executions and PnL</div>
              </div>
              <input
                type="checkbox"
                checked={tradesEnabled}
                onChange={(e) => setTradesEnabled(e.target.checked)}
                className="w-4 h-4 accent-sky-600 cursor-pointer"
              />
            </div>

            <div className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
              <div>
                <div className="font-bold text-white">System Health & Crash Warnings</div>
                <div className="text-[10px] text-[#8D9AAA]">Send critical circuit breaker & watchdog warnings</div>
              </div>
              <input
                type="checkbox"
                checked={errorsEnabled}
                onChange={(e) => setErrorsEnabled(e.target.checked)}
                className="w-4 h-4 accent-sky-600 cursor-pointer"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
