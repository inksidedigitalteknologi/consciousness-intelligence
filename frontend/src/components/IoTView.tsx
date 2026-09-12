// src/components/IoTView.tsx
// INKSIDE DIGITAL — IoT View

import React, { useState, useEffect, useCallback } from 'react';
import { Radio, RefreshCw, Server, Loader2, Zap } from 'lucide-react';

interface IoTDevice {
  id: string;
  name: string;
  type: 'sensor' | 'actuator' | 'hybrid';
  status: 'online' | 'offline' | 'unknown';
  value?: number;
  unit?: string;
  last_seen?: string;
}

interface IoTViewProps {
  wsConnected?: boolean;
}

export const IoTView: React.FC<IoTViewProps> = ({ wsConnected }) => {
  const [devices, setDevices] = useState<IoTDevice[]>([]);
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const apiKey = localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823';

  const fetchDevices = useCallback(async () => {
    try {
      const r = await fetch('/api/iot/devices', {
        headers: { 'X-API-Key': apiKey },
      });
      if (r.ok) {
        const data = await r.json();
        setDevices(data.devices || []);
      }
    } catch {
      // silent
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  useEffect(() => {
    fetchDevices();
    const iv = setInterval(fetchDevices, 30000);
    return () => clearInterval(iv);
  }, [fetchDevices]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await fetchDevices();
    setTimeout(() => setIsRefreshing(false), 300);
  };

  return (
    <div className="space-y-6 pb-12">
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-600/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Radio className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">IoT Devices</h2>
            <p className="text-xs text-[#8D9AAA]">
              Device management · Sensor data · Command control
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span
            className={`text-xs px-2 py-0.5 rounded font-bold ${
              wsConnected
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20'
                : 'bg-rose-500/20 text-rose-400 border border-rose-500/20'
            }`}
          >
            {wsConnected ? '🟢 LIVE' : '🔴 OFFLINE'}
          </span>
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="p-1.5 rounded-lg bg-[#1A2530] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[10px] text-[#8D9AAA] uppercase">Total Devices</div>
          <div className="text-xl font-black text-white font-mono">{devices.length}</div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[10px] text-[#8D9AAA] uppercase">Online</div>
          <div className="text-xl font-black text-emerald-400 font-mono">
            {devices.filter((d) => d.status === 'online').length}
          </div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[10px] text-[#8D9AAA] uppercase">Sensors</div>
          <div className="text-xl font-black text-cyan-400 font-mono">
            {devices.filter((d) => d.type === 'sensor' || d.type === 'hybrid').length}
          </div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[10px] text-[#8D9AAA] uppercase">Actuators</div>
          <div className="text-xl font-black text-amber-400 font-mono">
            {devices.filter((d) => d.type === 'actuator' || d.type === 'hybrid').length}
          </div>
        </div>
      </div>

      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D]">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Server className="w-4 h-4 text-cyan-400" />
            Registered Devices
          </h3>
          <span className="text-xs text-[#5F6B78]">{devices.length} devices</span>
        </div>

        {loading ? (
          <div className="py-8 flex items-center justify-center text-[#5F6B78] text-xs">
            <Loader2 className="w-4 h-4 animate-spin mr-2" />
            Memuat device...
          </div>
        ) : devices.length === 0 ? (
          <div className="py-12 text-center space-y-3">
            <div className="w-12 h-12 mx-auto rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-center">
              <Radio className="w-6 h-6 text-[#5F6B78]" />
            </div>
            <div className="text-[#8D9AAA] text-sm font-semibold">
              Belum ada device terdaftar
            </div>
            <div className="text-[#5F6B78] text-xs max-w-md mx-auto">
              Device akan muncul saat Anda menghubungkan ESP32, Arduino, atau perangkat IoT lain.
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mt-4">
            {devices.map((d) => (
              <div key={d.id} className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D]">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span
                      className={`w-2 h-2 rounded-full ${
                        d.status === 'online' ? 'bg-emerald-400 animate-pulse' : 'bg-[#5F6B78]'
                      }`}
                    />
                    <span className="text-xs font-bold text-white">{d.name || d.id}</span>
                  </div>
                  <span className="text-[10px] text-[#5F6B78] font-mono">{d.type}</span>
                </div>
                {d.value !== undefined && (
                  <div className="text-lg font-black text-cyan-400 font-mono">
                    {d.value}
                    {d.unit || ''}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-3">
        <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
          <Zap className="w-4 h-4 text-amber-400" />
          Cara Menghubungkan Device
        </h3>
        <div className="space-y-2 text-xs text-[#8D9AAA]">
          <p>
            <strong className="text-white">1. HTTP REST:</strong> Device kirim ke{' '}
            <code className="px-1.5 py-0.5 bg-[#0B0F14] rounded text-cyan-400">
              POST /api/iot/sensor
            </code>
          </p>
          <pre className="p-3 bg-[#0B0F14] rounded-lg border border-[#26313D] text-[10px] text-cyan-300 overflow-x-auto">
{`{
  "device_id": "esp32_suhu_01",
  "type": "temperature",
  "value": 35.2,
  "unit": "°C"
}`}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default IoTView;
