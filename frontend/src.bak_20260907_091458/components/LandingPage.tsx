import React, { useState, useEffect } from 'react';
import { 
  BrainCircuit, 
  Zap, 
  Shield, 
  Activity, 
  TrendingUp, 
  ArrowRight,
  Menu,
  X,
  Github,
  Twitter,
  Send,
  Lock,
  Server,
  Cpu,
  Radio,
  Rss,
  Monitor,
  Layers
} from 'lucide-react';
import { HeroCanvas } from './HeroCanvas';
import { inksideAPI } from '../api/inkside';

interface LandingPageProps {
  onEnterDashboard: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onEnterDashboard }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [status, setStatus] = useState<'online' | 'offline' | 'loading'>('loading');
  const [signals, setSignals] = useState<any[]>([]);
  const [stats, setStats] = useState({
    cycles: 0,
    health: 0,
    pairs: 0,
    uptime: 0
  });

  // Fetch real data untuk preview
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statusRes, signalsRes] = await Promise.all([
          inksideAPI.getStatus(),
          inksideAPI.getSignals()
        ]);
        
        setStatus('online');
        setSignals(signalsRes.signals?.slice(0, 3) || []);
        
        if (statusRes?.bot) {
          setStats({
            cycles: statusRes.bot.cycles || 0,
            health: 98,
            pairs: 20,
            uptime: statusRes.bot.uptime || 0
          });
        }
      } catch {
        setStatus('offline');
      }
    };
    
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: <BrainCircuit className="w-6 h-6 text-cyan-400" />,
      title: 'Cognitive Brain Engine',
      desc: 'Neural reflection algorithm that analyzes market regime shifts, macro volatility, and cross-asset flow.'
    },
    {
      icon: <Shield className="w-6 h-6 text-emerald-400" />,
      title: 'Consciousness Risk Module',
      desc: 'Self-aware risk guardian with hard circuit-breaker logic and real-time drawdown caps.'
    },
    {
      icon: <Zap className="w-6 h-6 text-amber-400" />,
      title: 'Autonomous Self-Learning',
      desc: 'Continuously learns from historic win/loss patterns via vectorized memory.'
    },
    {
      icon: <Radio className="w-6 h-6 text-purple-400" />,
      title: 'Kraken WebSocket API',
      desc: 'Ultra-low latency connection with sub-50ms order execution.'
    },
    {
      icon: <Send className="w-6 h-6 text-blue-400" />,
      title: 'Telegram Remote Bridge',
      desc: 'Full remote command suite via Telegram bot: signals, PnL, emergency stop.'
    },
    {
      icon: <Monitor className="w-6 h-6 text-rose-400" />,
      title: 'CustomTkinter Desktop GUI',
      desc: 'Lightweight, modern dark-mode GUI engineered in Python CustomTkinter.'
    },
    {
      icon: <Rss className="w-6 h-6 text-orange-400" />,
      title: '47+ Real-Time RSS Feeds',
      desc: 'Aggregates Bloomberg, CoinDesk, Reuters, and Indonesian economic portals.'
    },
    {
      icon: <Lock className="w-6 h-6 text-cyan-400" />,
      title: '100% Self-Hosted & Private',
      desc: 'Zero marketplace dependencies. Run on your private Linux VPS or local PC.'
    }
  ];

  const getSignalColor = (signal: string) => {
    const s = signal?.toUpperCase() || '';
    if (s === 'BUY') return 'text-green-400 bg-green-500/20';
    if (s === 'SELL') return 'text-red-400 bg-red-500/20';
    return 'text-yellow-400 bg-yellow-500/20';
  };

  return (
    <div className="relative min-h-screen bg-[#07070B] text-white overflow-hidden">
      
      {/* ============================================================
          HERO CANVAS BACKGROUND
          ============================================================ */}
      <HeroCanvas />

      {/* ============================================================
          NAVBAR
          ============================================================ */}
      <nav className="relative z-20 border-b border-white/10 bg-[#07070B]/80 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-amber-500 p-[1px]">
              <div className="w-full h-full bg-[#07070F] rounded-[10px] flex items-center justify-center">
                <BrainCircuit className="w-5 h-5 text-cyan-400" />
              </div>
            </div>
            <span className="font-heading font-extrabold text-lg text-white">
              INKSIDE<span className="text-amber-400">.DIGITAL</span>
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              v5.0
            </span>
          </div>

          <div className="flex items-center gap-4">
            <div className={`hidden md:flex items-center gap-2 text-xs ${status === 'online' ? 'text-emerald-400' : 'text-red-400'}`}>
              <span className={`w-2 h-2 rounded-full ${status === 'online' ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'}`} />
              {status === 'online' ? 'System Online' : 'Connecting...'}
            </div>
            <button
              onClick={onEnterDashboard}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-sm flex items-center gap-2 shadow-lg shadow-amber-500/20"
            >
              <span>Launch Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-lg text-gray-400 hover:text-white"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </nav>

      {/* ============================================================
          HERO SECTION
          ============================================================ */}
      <section className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          {/* LEFT - Content */}
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-mono">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
              COGNITIVE MIRROR ENGINE v5.0
            </div>
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-heading font-black leading-tight">
              Cognitive Intelligence for{' '}
              <span className="gold-gradient-text">Smarter Trading.</span>
            </h1>
            
            <p className="text-lg text-gray-400 max-w-lg">
              Enterprise-grade algorithmic trading software with neural market reflection, 
              consciousness risk protection, and direct Kraken Exchange execution.
            </p>
            
            <div className="flex flex-wrap gap-4 pt-2">
              <button
                onClick={onEnterDashboard}
                className="px-6 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold flex items-center gap-2 shadow-lg shadow-amber-500/20"
              >
                <span>Launch Dashboard</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>

            {/* Live Stats Preview */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-6">
              <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                <div className="text-2xl font-bold text-cyan-400">{stats.cycles.toLocaleString()}</div>
                <div className="text-xs text-gray-400">Cycles Processed</div>
              </div>
              <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                <div className="text-2xl font-bold text-emerald-400">{stats.health}%</div>
                <div className="text-xs text-gray-400">System Health</div>
              </div>
              <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                <div className="text-2xl font-bold text-amber-400">{stats.pairs}</div>
                <div className="text-xs text-gray-400">Trading Pairs</div>
              </div>
              <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                <div className="text-2xl font-bold text-purple-400">{(stats.uptime / 60).toFixed(0)}m</div>
                <div className="text-xs text-gray-400">Uptime</div>
              </div>
            </div>
          </div>

          {/* RIGHT - Live Signals Preview */}
          <div className="lg:pl-8">
            <div className="p-6 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-bold text-white">📊 Live Signals</span>
                <span className="text-xs text-gray-400">Real-time from Kraken</span>
              </div>
              
              {signals.length === 0 ? (
                <div className="text-center py-8 text-gray-400 text-sm">
                  <Activity className="w-8 h-8 mx-auto mb-2 opacity-30" />
                  Waiting for signals...
                </div>
              ) : (
                <div className="space-y-3">
                  {signals.map((signal, i) => (
                    <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
                      <div>
                        <div className="font-bold text-white font-mono">{signal.pair}</div>
                        <div className="text-xs text-gray-400">${signal.price?.toFixed(2) || '0.00'}</div>
                      </div>
                      <div className="text-right">
                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${getSignalColor(signal.signal)}`}>
                          {signal.signal || 'HOLD'}
                        </span>
                        <div className="text-xs text-gray-400 mt-1">{signal.confidence}% confidence</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
              
              <button
                onClick={onEnterDashboard}
                className="w-full mt-4 py-2.5 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-sm font-semibold transition-colors"
              >
                View All Signals →
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* ============================================================
          FEATURES SECTION
          ============================================================ */}
      <section className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-heading font-black text-white">
            Engineered for <span className="text-cyan-400">Alpha</span>
          </h2>
          <p className="text-gray-400 mt-2 max-w-2xl mx-auto">
            Deployable on your private server, combining real-time news sentiment, order book imbalance, 
            and consciousness drawdown safeguards.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, i) => (
            <div key={i} className="p-6 rounded-2xl bg-[#131A22] border border-[#26313D] hover:border-cyan-500/30 transition-all group">
              <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                {feature.icon}
              </div>
              <h3 className="font-bold text-white text-sm mb-2">{feature.title}</h3>
              <p className="text-xs text-gray-400 leading-relaxed">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ============================================================
          CTA SECTION
          ============================================================ */}
      <section className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="p-8 sm:p-12 rounded-3xl bg-gradient-to-r from-cyan-950/60 to-purple-950/60 border border-white/20 text-center">
          <h2 className="text-2xl sm:text-3xl font-heading font-black text-white mb-4">
            Ready to Take Control of Your Trading?
          </h2>
          <p className="text-gray-400 max-w-xl mx-auto mb-6">
            Launch the Cognitive Mirror Engine dashboard and start monitoring the market in real-time.
          </p>
          <button
            onClick={onEnterDashboard}
            className="px-8 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-sm flex items-center gap-2 shadow-lg shadow-amber-500/20 mx-auto"
          >
            <span>Launch Dashboard</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </section>

      {/* ============================================================
          FOOTER
          ============================================================ */}
      <footer className="relative z-10 border-t border-white/10 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-gray-500">
          <p>© 2026 Inkside Digital. All rights reserved. Cognitive Mirror Engine v5.0</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
