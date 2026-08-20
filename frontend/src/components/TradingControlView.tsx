import React, { useState } from 'react';
import { Zap, Play, Square, ShieldCheck, DollarSign, ArrowUpRight, TrendingUp, AlertCircle } from 'lucide-react';
import { TradingPosition } from '../types';

interface TradingControlViewProps {
  engineRunning: boolean;
  onToggleEngine: () => void;
  positions: TradingPosition[];
  onClosePosition: (id: string) => void;
}

export const TradingControlView: React.FC<TradingControlViewProps> = ({
  engineRunning,
  onToggleEngine,
  positions,
  onClosePosition,
}) => {
  const [autoTrading, setAutoTrading] = useState(false);
  const [paperTrading, setPaperTrading] = useState(true);
  const [riskPercent, setRiskPercent] = useState(1.5);

  const totalPnlUsd = positions.reduce((acc, p) => acc + p.pnlUsd, 0);

  return (
    <div id="trading-control-view" className="space-y-6 pb-12">
      {/* Top Header */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-600/20 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Trading Control & Execution Engine
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Automated vs. Paper Trading Execution with Dynamic Position Sizing
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onToggleEngine}
            className={`flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-bold transition-all shadow-md cursor-pointer ${
              engineRunning
                ? 'bg-rose-600 hover:bg-rose-500 text-white shadow-rose-600/30'
                : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-600/30'
            }`}
          >
            {engineRunning ? (
              <>
                <Square className="w-3.5 h-3.5 fill-current" />
                <span>STOP TRADING ENGINE</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>START TRADING ENGINE</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Control Cards & Configuration */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Controls Left (1 Col) */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70">
            Execution Mode Toggles
          </h3>

          <div className="space-y-3.5">
            {/* Auto Trading Switch */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
              <div>
                <div className="text-xs font-bold text-white">Automated Trading</div>
                <div className="text-[10px] text-[#8D9AAA]">Execute orders without manual confirmation</div>
              </div>
              <input
                type="checkbox"
                checked={autoTrading}
                onChange={(e) => setAutoTrading(e.target.checked)}
                className="w-4 h-4 accent-blue-600 cursor-pointer"
              />
            </div>

            {/* Paper Trading Switch */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between">
              <div>
                <div className="text-xs font-bold text-white">Paper Trading (Safe Mode)</div>
                <div className="text-[10px] text-emerald-400">Zero capital risk simulation</div>
              </div>
              <input
                type="checkbox"
                checked={paperTrading}
                onChange={(e) => setPaperTrading(e.target.checked)}
                className="w-4 h-4 accent-emerald-600 cursor-pointer"
              />
            </div>

            {/* Risk Per Trade Slider */}
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-white">Risk Per Trade:</span>
                <span className="font-mono font-bold text-blue-400">{riskPercent}%</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="5.0"
                step="0.5"
                value={riskPercent}
                onChange={(e) => setRiskPercent(parseFloat(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
              <span className="text-[10px] text-[#5F6B78] block">Caps max position loss at {riskPercent}% of equity</span>
            </div>
          </div>
        </div>

        {/* Live Positions Right (2 Cols) */}
        <div className="lg:col-span-2 p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              Active Open Positions ({positions.length})
            </h3>
            <div className="text-xs font-mono font-bold text-emerald-400">
              Total Unrealized PnL: +${totalPnlUsd.toFixed(2)}
            </div>
          </div>

          <div className="space-y-3">
            {positions.map((pos) => (
              <div
                key={pos.id}
                className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xs font-black px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-mono">
                    {pos.side}
                  </span>
                  <div>
                    <div className="text-sm font-bold text-white font-mono">{pos.pair}</div>
                    <div className="text-[10px] text-[#8D9AAA] font-mono">
                      Entry: ${pos.entryPrice.toLocaleString()} · Amount: {pos.amount}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-5">
                  <div className="text-right font-mono">
                    <div className="text-xs font-bold text-white">
                      Current: ${pos.currentPrice.toLocaleString()}
                    </div>
                    <div className="text-xs font-bold text-emerald-400">
                      +${pos.pnlUsd.toFixed(2)} (+{pos.pnlPercent.toFixed(2)}%)
                    </div>
                  </div>

                  <button
                    onClick={() => onClosePosition(pos.id)}
                    className="px-3 py-1.5 rounded-lg bg-rose-600/20 hover:bg-rose-600 border border-rose-500/40 text-rose-300 hover:text-white text-xs font-bold transition-all cursor-pointer"
                  >
                    Close
                  </button>
                </div>
              </div>
            ))}

            {positions.length === 0 && (
              <div className="py-8 text-center text-xs text-[#5F6B78]">
                No open positions. Scanner is searching for high-probability setups.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
