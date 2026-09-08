import React, { useState } from 'react';
import { Database, Search, Sparkles, Filter, Trash2, RefreshCw, HardDrive, Cpu, Layers } from 'lucide-react';

export const MemoryView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'sqlite' | 'semantic' | 'optimizer' | 'archive'>('sqlite');
  const [searchQuery, setSearchQuery] = useState('');

  const memoryRecords = [
    { id: 'mem-101', type: 'Observation', domain: 'trading', content: 'BTC/USD breakout with volume expansion above $94,200', confidence: 91, importance: 0.9, timestamp: '2026-08-18 08:30:00' },
    { id: 'mem-102', type: 'Experience', domain: 'trading', content: 'Entry at $192.00 on SOL/USD hit Take Profit 2 at $215.00 (+12% PnL)', confidence: 95, importance: 0.95, timestamp: '2026-08-18 08:15:22' },
    { id: 'mem-103', type: 'Insight', domain: 'market', content: 'Macro interest rate announcement caused 15m spike in crypto liquidity', confidence: 85, importance: 0.8, timestamp: '2026-08-18 07:45:10' },
    { id: 'mem-104', type: 'Knowledge', domain: 'knowledge', content: 'Federal Reserve rate cut cycles correlate with Bitcoin bull expansions', confidence: 88, importance: 0.85, timestamp: '2026-08-18 06:20:00' },
    { id: 'mem-105', type: 'Decision', domain: 'trading', content: 'Executed BUY order on ETH/USD at $3,100 with ATR Stop Loss at $3,040', confidence: 83, importance: 0.8, timestamp: '2026-08-18 05:10:15' },
    { id: 'mem-106', type: 'Reflection', domain: 'learning', content: 'Trailing stop protected capital from sudden Asian session flash pullback', confidence: 90, importance: 0.85, timestamp: '2026-08-18 04:30:00' },
  ];

  const filteredRecords = memoryRecords.filter((r) => {
    if (!searchQuery) return true;
    return (
      r.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.domain.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.type.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  return (
    <div id="memory-view" className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Long-Term & Semantic Memory System v3.0
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              SQLite Long-Term Store, Semantic Vector Space (semantic_memory.py) & Memory Optimizer (memory_optimizer.py)
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
          <span className="text-white font-bold">2,450 VECTORS PERSISTED</span>
        </div>
      </div>

      {/* Memory Sub-Tabs */}
      <div className="flex flex-wrap items-center gap-2 p-1.5 rounded-xl bg-[#131A22] border border-[#26313D]">
        {[
          { id: 'sqlite', label: 'SQLite Store (memory.db)', icon: HardDrive },
          { id: 'semantic', label: 'Semantic Vectors (3.0)', icon: Cpu },
          { id: 'optimizer', label: 'Memory Optimizer (2.0)', icon: Sparkles },
          { id: 'archive', label: 'Archive Storage Manager', icon: Layers },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-bold font-mono transition-all cursor-pointer ${
                isActive
                  ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30'
                  : 'text-[#8D9AAA] hover:bg-[#1A2530] hover:text-white'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Memory Stats Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Total Records</span>
          <span className="text-xl font-bold font-mono text-white mt-1 block">2,450 Vectors</span>
          <span className="text-[10px] text-emerald-400 mt-1 block font-mono">SQLite WAL Mode Active</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Semantic Categories</span>
          <span className="text-xl font-bold font-mono text-cyan-400 mt-1 block">18 Clusters</span>
          <span className="text-[10px] text-[#5F6B78] mt-1 block font-mono">High Concept Density</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Optimizer Deduplications</span>
          <span className="text-xl font-bold font-mono text-purple-400 mt-1 block">340 Purged</span>
          <span className="text-[10px] text-purple-400/80 mt-1 block font-mono">SHA-256 Fingerprint Index</span>
        </div>

        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <span className="text-[10px] uppercase font-bold text-[#8D9AAA] block">Retention Rate</span>
          <span className="text-xl font-bold font-mono text-emerald-400 mt-1 block">99.4%</span>
          <span className="text-[10px] text-[#5F6B78] mt-1 block font-mono">Ebbinghaus Curve</span>
        </div>
      </div>

      {/* Search & Records Explorer */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#26313D]/70">
          <div className="flex items-center gap-2">
            <Search className="w-4 h-4 text-purple-400" />
            <h3 className="text-sm font-bold text-white tracking-wider uppercase">
              Memory Vectors Explorer ({filteredRecords.length})
            </h3>
          </div>

          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search memory records by keyword or domain..."
            className="px-3.5 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-purple-500 w-full sm:w-72"
          />
        </div>

        <div className="divide-y divide-[#26313D]/40 font-mono text-xs">
          {filteredRecords.map((item) => (
            <div key={item.id} className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-purple-400 text-xs bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">
                    {item.type}
                  </span>
                  <span className="text-[10px] text-[#8D9AAA]">Domain: {item.domain}</span>
                </div>
                <p className="text-xs text-white font-sans">{item.content}</p>
                <div className="text-[10px] text-[#5F6B78]">{item.timestamp}</div>
              </div>

              <div className="flex items-center gap-3 text-right">
                <div>
                  <div className="text-[10px] text-[#5F6B78]">Confidence</div>
                  <div className="text-emerald-400 font-bold">{item.confidence}%</div>
                </div>
                <div>
                  <div className="text-[10px] text-[#5F6B78]">Importance</div>
                  <div className="text-cyan-400 font-bold">{item.importance}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
