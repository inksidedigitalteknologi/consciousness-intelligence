import React, { useState } from 'react';
import { Sliders, Save, CheckCircle2, Shield } from 'lucide-react';

export const SettingsView: React.FC = () => {
  const [scanInterval, setScanInterval] = useState(60);
  const [minMtf, setMinMtf] = useState(4);
  const [minConfidence, setMinConfidence] = useState(70);
  const [minStrength, setMinStrength] = useState(70);
  const [atrSlMultiplier, setAtrSlMultiplier] = useState(1.5);
  const [tp2Multiplier, setTp2Multiplier] = useState(2.0);
  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleSave = () => {
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  return (
    <div id="settings-view" className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <Sliders className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              System Configuration & Risk Parameters
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Production parameters for Signal Engine v4.0, MTF Scanner & Risk Controls
            </p>
          </div>
        </div>

        <button
          onClick={handleSave}
          className="flex items-center gap-2 px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-all shadow-md shadow-blue-600/30 cursor-pointer"
        >
          <Save className="w-4 h-4" />
          <span>{savedSuccess ? 'Settings Saved!' : 'Save Settings'}</span>
        </button>
      </div>

      {/* Settings Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Scanner & MTF Parameters */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70">
            Scanner & Alignment Parameters
          </h3>

          <div className="space-y-3 font-mono text-xs">
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2">
              <div className="flex items-center justify-between font-sans">
                <span className="font-bold text-white">Scan Interval (Seconds)</span>
                <span className="text-blue-400 font-bold font-mono">{scanInterval}s</span>
              </div>
              <input
                type="number"
                value={scanInterval}
                onChange={(e) => setScanInterval(parseInt(e.target.value) || 60)}
                className="w-full px-3 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-white focus:outline-none"
              />
            </div>

            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2">
              <div className="flex items-center justify-between font-sans">
                <span className="font-bold text-white">Min MTF Timeframe Alignment</span>
                <span className="text-blue-400 font-bold font-mono">{minMtf} / 5</span>
              </div>
              <input
                type="range"
                min="2"
                max="5"
                value={minMtf}
                onChange={(e) => setMinMtf(parseInt(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
            </div>

            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2">
              <div className="flex items-center justify-between font-sans">
                <span className="font-bold text-white">Min Signal Confidence</span>
                <span className="text-emerald-400 font-bold font-mono">{minConfidence}%</span>
              </div>
              <input
                type="range"
                min="50"
                max="90"
                value={minConfidence}
                onChange={(e) => setMinConfidence(parseInt(e.target.value))}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>
          </div>
        </div>

        {/* Risk & Stop-Loss Multipliers */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase pb-3 border-b border-[#26313D]/70">
            ATR Risk & Profit Multipliers
          </h3>

          <div className="space-y-3 font-mono text-xs">
            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2">
              <div className="flex items-center justify-between font-sans">
                <span className="font-bold text-white">Stop Loss ATR Multiplier</span>
                <span className="text-rose-400 font-bold font-mono">{atrSlMultiplier}x ATR</span>
              </div>
              <input
                type="number"
                step="0.1"
                value={atrSlMultiplier}
                onChange={(e) => setAtrSlMultiplier(parseFloat(e.target.value) || 1.5)}
                className="w-full px-3 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-white focus:outline-none"
              />
            </div>

            <div className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2">
              <div className="flex items-center justify-between font-sans">
                <span className="font-bold text-white">TP 2 (Core Target) Risk/Reward</span>
                <span className="text-emerald-400 font-bold font-mono">1 : {tp2Multiplier}</span>
              </div>
              <input
                type="number"
                step="0.5"
                value={tp2Multiplier}
                onChange={(e) => setTp2Multiplier(parseFloat(e.target.value) || 2.0)}
                className="w-full px-3 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-white focus:outline-none"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
