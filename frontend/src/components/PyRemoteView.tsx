import React, { useState } from 'react';
import { Smartphone, Monitor, Play, Square, Sliders, Terminal, MousePointer, RefreshCw, CheckCircle2, Trash2 } from 'lucide-react';
import { SystemLogEntry } from '../types';

interface PyRemoteViewProps {
  logs: SystemLogEntry[];
  onClearLogs: () => void;
}

export const PyRemoteView: React.FC<PyRemoteViewProps> = ({ logs, onClearLogs }) => {
  const [speed, setSpeed] = useState(50);
  const [autoExport, setAutoExport] = useState(true);
  const [taskStatus, setTaskStatus] = useState<'IDLE' | 'RUNNING' | 'STOPPED'>('RUNNING');
  const [logFilter, setLogFilter] = useState('');

  const filteredLogs = logs.filter(
    (l) =>
      l.message.toLowerCase().includes(logFilter.toLowerCase()) ||
      l.source.toLowerCase().includes(logFilter.toLowerCase())
  );

  return (
    <div id="pyremote-view" className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-600/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Smartphone className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              PyRemote GUI Bridge Server (Mobile Remote Control)
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Flask HTTP Bridge on port 5000 for remote Android / PC telemetry & control.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 font-mono text-xs">
          <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-emerald-500/30">
            <span className="text-[10px] text-[#5F6B78] block font-sans">Bridge Server URL</span>
            <span className="text-emerald-400 font-bold">http://127.0.0.1:5000</span>
          </div>
        </div>
      </div>

      {/* Screen Streaming & Virtual Control Widgets */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Screen Streaming Simulator */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <Monitor className="w-4 h-4 text-cyan-400" />
              Live Screen / GUI Stream (/api/screen)
            </h3>
            <span className="text-xs font-mono text-emerald-400 font-bold">30 FPS · JPEG 85%</span>
          </div>

          <div className="h-64 rounded-xl bg-[#0B0F14] border border-[#26313D] p-4 flex flex-col justify-between relative overflow-hidden">
            <div className="flex items-center justify-between text-xs text-[#8D9AAA] font-mono">
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                Inkside GUI Terminal (PC Active Window)
              </span>
              <span>1600x950</span>
            </div>

            {/* Simulated Terminal Interface Preview */}
            <div className="p-3.5 rounded-lg bg-[#1A2530]/80 border border-[#26313D] space-y-2 font-mono text-[11px]">
              <div className="flex items-center justify-between border-b border-[#26313D] pb-1.5 text-white">
                <span>INKSIDE TRADING BOT v4.4.1</span>
                <span className="text-emerald-400">[ONLINE]</span>
              </div>
              <div className="text-[#8D9AAA] text-[10px] space-y-1">
                <div>&gt; [Scanner] BTC/USD: $68,420.50 (+3.42%) | Trend: BULLISH</div>
                <div>&gt; [Brain] Decision: STRONG_BUY (Confidence: 88%)</div>
                <div>&gt; [Autonomous] 18 RSS Feeds Active | Cycle #1,420</div>
              </div>
            </div>

            <div className="flex items-center justify-between text-[10px] text-[#5F6B78] font-mono">
              <span>Touch / Virtual Click simulation ready</span>
              <span>Latency: 8ms</span>
            </div>
          </div>
        </div>

        {/* Remote Action Widgets */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <Sliders className="w-4 h-4 text-purple-400" />
              Remote Custom Widgets (/api/action)
            </h3>
            <span className="text-xs text-[#5F6B78] font-mono">REST API Handler</span>
          </div>

          <div className="space-y-3 font-mono text-xs">
            {/* Start Task Button */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
              <div>
                <span className="font-bold text-white font-sans block">Trigger Remote Start Task</span>
                <span className="text-[10px] text-[#8D9AAA]">Action: start_task</span>
              </div>
              <button
                onClick={() => setTaskStatus('RUNNING')}
                className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs cursor-pointer"
              >
                Trigger Start
              </button>
            </div>

            {/* Stop Task Button */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
              <div>
                <span className="font-bold text-white font-sans block">Trigger Remote Stop Task</span>
                <span className="text-[10px] text-[#8D9AAA]">Action: stop_task</span>
              </div>
              <button
                onClick={() => setTaskStatus('STOPPED')}
                className="px-4 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs cursor-pointer"
              >
                Trigger Stop
              </button>
            </div>

            {/* Set Speed Slider */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white font-sans">Remote Engine Speed</span>
                <span className="text-blue-400 font-bold">{speed} ms</span>
              </div>
              <input
                type="range"
                min="10"
                max="100"
                value={speed}
                onChange={(e) => setSpeed(parseInt(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Logs Buffer Console */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-3 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#26313D]/70">
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-bold text-white tracking-wider uppercase">
              Bridge Real-Time Logs Buffer (/api/logs)
            </h3>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="text"
              placeholder="Search logs..."
              value={logFilter}
              onChange={(e) => setLogFilter(e.target.value)}
              className="px-3 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none"
            />
            <button
              onClick={onClearLogs}
              className="flex items-center gap-1 px-3 py-1 rounded-lg bg-rose-600/20 hover:bg-rose-600 border border-rose-500/40 text-rose-300 hover:text-white text-xs font-bold transition-all cursor-pointer"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear</span>
            </button>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#0B0F14] border border-[#26313D] font-mono text-xs max-h-64 overflow-y-auto space-y-1.5">
          {filteredLogs.map((l) => (
            <div key={l.id} className="flex items-start gap-2.5 leading-relaxed">
              <span className="text-[#5F6B78] text-[10px] shrink-0">
                [{new Date(l.timestamp).toLocaleTimeString()}]
              </span>
              <span
                className={`text-[10px] font-bold px-1.5 py-0.2 rounded shrink-0 ${
                  l.level === 'SUCCESS'
                    ? 'bg-emerald-500/10 text-emerald-400'
                    : l.level === 'ERROR'
                    ? 'bg-rose-500/10 text-rose-400'
                    : l.level === 'WARNING'
                    ? 'bg-amber-500/10 text-amber-400'
                    : 'bg-blue-500/10 text-blue-400'
                }`}
              >
                {l.level}
              </span>
              <span className="text-[#8D9AAA] text-[11px] font-bold shrink-0">[{l.source}]</span>
              <span className="text-[#E8EDF2] text-[11px]">{l.message}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
