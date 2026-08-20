import React from 'react';
import { Activity, ShieldCheck, Cpu, HardDrive, CheckCircle2, AlertTriangle, RefreshCw } from 'lucide-react';
import { ComponentHealthStatus } from '../types';

interface HealthViewProps {
  components: ComponentHealthStatus[];
  healthScore: number;
}

export const HealthView: React.FC<HealthViewProps> = ({ components, healthScore }) => {
  return (
    <div id="health-view" className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-rose-600/20 border border-rose-500/30 flex items-center justify-center text-rose-400">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              System Health & Watchdog Diagnostics
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Real-time Subsystem Latency, Process Heartbeat & Circuit Breaker Monitoring
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-4 py-2 rounded-xl bg-[#0B0F14] border border-emerald-500/30 text-right">
            <span className="text-[10px] text-[#5F6B78] font-bold block uppercase">Overall Health</span>
            <span className="text-base font-black text-emerald-400 font-mono">{healthScore}% (EXCELLENT)</span>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5 font-mono">
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] text-[#8D9AAA] font-bold uppercase block font-sans">Active Services</span>
          <div className="text-xl font-black text-white mt-1">{components.length} / {components.length}</div>
          <span className="text-[10px] text-emerald-400 font-bold">100% Online</span>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] text-[#8D9AAA] font-bold uppercase block font-sans">Circuit Breaker</span>
          <div className="text-xl font-black text-emerald-400 mt-1">CLOSED</div>
          <span className="text-[10px] text-[#5F6B78]">0 Tripped</span>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] text-[#8D9AAA] font-bold uppercase block font-sans">Avg RPC Latency</span>
          <div className="text-xl font-black text-cyan-400 mt-1">14.2 ms</div>
          <span className="text-[10px] text-emerald-400">Optimal</span>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] text-[#8D9AAA] font-bold uppercase block font-sans">System Uptime</span>
          <div className="text-xl font-black text-purple-400 mt-1">99.98%</div>
          <span className="text-[10px] text-[#5F6B78]">Zero Fatal Errors</span>
        </div>
      </div>

      {/* Components Health Matrix */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg">
        <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70 mb-4">
          Core Subsystems Health Status ({components.length})
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {components.map((c) => (
            <div
              key={c.name}
              className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between"
            >
              <div>
                <div className="text-xs font-bold text-white flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400" />
                  <span>{c.name}</span>
                </div>
                <div className="text-[10px] text-[#8D9AAA] font-mono mt-0.5">
                  Checks: {c.checks} · Errors: <strong className="text-emerald-400">{c.errors}</strong> · {c.latencyMs}ms
                </div>
              </div>

              <div className="text-right">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {c.status}
                </span>
                <span className="text-[10px] text-emerald-400 font-bold block font-mono mt-0.5">
                  {c.score}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
