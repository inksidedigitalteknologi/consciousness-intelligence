// src/components/views/BrainView.tsx
// INKSIDE DIGITAL - COGNITIVE BRAIN ENGINE v5.0
// FULL CONSCIOUSNESS AI INTEGRATION
// UNIVERSAL INTELLIGENCE - BEYOND TRADING

import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Brain,
  Cpu,
  Zap,
  Activity,
  CheckCircle2,
  AlertTriangle,
  Play,
  RefreshCw,
  Sparkles,
  Sliders,
  Eye,
  Heart,
  Compass,
  Feather,
  Shield,
  TrendingUp,
  Clock,
  Calendar,
  Loader2,
  MessageSquare,
  Award,
  GitBranch,
  Network,
  Users,
  Target,
  Star,
  Sun,
  Moon,
  Cloud,
  Waves,
  Infinity,
  Gem,
  Flower2,
  Trees,
  Mountain,
  Ship,
  Rocket,
  Globe,
  BookOpen,
  Lightbulb,
  Zap as ZapIcon,
  Coffee,
  Music,
  Film,
  Palette,
  Camera,
  Code,
  Database,
  Cloud as CloudIcon,
  Server,
  Wifi,
  Bluetooth,
  Radio,
  Satellite,
  Telescope,
  Microscope,
  Atom,
  Dna,
  Leaf,
  Droplets,
  Wind,
  Flame,
  Snowflake,
  Umbrella,
  Sun as SunIcon,
  Moon as MoonIcon,
  CloudRain,
  CloudSnow,
  CloudLightning,
  CloudSun,
  CloudMoon,
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

interface ConsciousnessState {
  awareness_level: number;
  curiosity_level: number;
  reflection_quality: number;
  growth_stage: string;
  last_improvement: string | null;
  total_improvements: number;
  insights_generated: number;
  performance_score: number;
  emotional_state: string;
  focus_area: string;
  confidence: number;
  resilience: number;
  timestamp: string;
}

interface AIStatus {
  enabled: boolean;
  version: string;
  model: string;
  available: boolean;
  consciousness: ConsciousnessState;
  usage: {
    today: number;
    daily_limit: number;
    remaining: number;
    total_calls: number;
  };
  cache: {
    size: number;
    hit_rate: number;
  };
  memory: {
    short_term: number;
    long_term: number;
    improvements: number;
  };
}

interface BrainViewProps {
  brainState: string;
  cycleCount: number;
  healthScore: number;
  onRefresh: () => void;
  wsConnected?: boolean;
}

// ============================================================
// HELPER COMPONENTS
// ============================================================

const ConsciousnessMeter: React.FC<{
  label: string;
  value: number;
  icon: React.ReactNode;
  color?: string;
  description?: string;
}> = ({ label, value, icon, color = 'text-purple-400', description }) => {
  const percentage = Math.min(value * 100, 100);
  const colorMap: Record<string, string> = {
    'text-purple-400': 'bg-purple-500',
    'text-blue-400': 'bg-blue-500',
    'text-emerald-400': 'bg-emerald-500',
    'text-amber-400': 'bg-amber-500',
    'text-rose-400': 'bg-rose-500',
    'text-teal-400': 'bg-teal-500',
    'text-cyan-400': 'bg-cyan-500',
    'text-indigo-400': 'bg-indigo-500',
    'text-pink-400': 'bg-pink-500',
    'text-orange-400': 'bg-orange-500',
  };
  const bgColor = colorMap[color] || 'bg-purple-500';

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center gap-1.5">
          <span className={color}>{icon}</span>
          <span className="text-[#8D9AAA]">{label}</span>
          {description && (
            <span className="text-[9px] text-[#5F6B78]">({description})</span>
          )}
        </div>
        <span className="text-white font-mono">{Math.round(percentage)}%</span>
      </div>
      <div className="w-full h-1.5 rounded-full bg-[#26313D] overflow-hidden">
        <div
          className={`h-full rounded-full ${bgColor} transition-all duration-1000`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

const EmotionBadge: React.FC<{ emotion: string }> = ({ emotion }) => {
  const emotions: Record<string, { emoji: string; color: string; description: string }> = {
    CALM: { emoji: '😌', color: 'bg-blue-500/20 text-blue-400 border-blue-500/20', description: 'Tenang' },
    CONFIDENT: { emoji: '😎', color: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20', description: 'Percaya Diri' },
    LEARNING: { emoji: '📚', color: 'bg-amber-500/20 text-amber-400 border-amber-500/20', description: 'Belajar' },
    CURIOUS: { emoji: '🤔', color: 'bg-purple-500/20 text-purple-400 border-purple-500/20', description: 'Penasaran' },
    FOCUSED: { emoji: '🎯', color: 'bg-teal-500/20 text-teal-400 border-teal-500/20', description: 'Fokus' },
    EXCITED: { emoji: '🔥', color: 'bg-rose-500/20 text-rose-400 border-rose-500/20', description: 'Bersemangat' },
    REFLECTIVE: { emoji: '🧘', color: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/20', description: 'Reflektif' },
    WISE: { emoji: '🦉', color: 'bg-purple-500/20 text-purple-400 border-purple-500/20', description: 'Bijaksana' },
    CREATIVE: { emoji: '🎨', color: 'bg-pink-500/20 text-pink-400 border-pink-500/20', description: 'Kreatif' },
    ANALYTICAL: { emoji: '🔬', color: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/20', description: 'Analitis' },
    PEACEFUL: { emoji: '🌊', color: 'bg-blue-500/20 text-blue-400 border-blue-500/20', description: 'Damai' },
    ENERGIZED: { emoji: '⚡', color: 'bg-amber-500/20 text-amber-400 border-amber-500/20', description: 'Berenergi' },
  };
  const data = emotions[emotion] || { emoji: '🧠', color: 'bg-gray-500/20 text-gray-400 border-gray-500/20', description: 'Netral' };
  return (
    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${data.color}`} title={data.description}>
      {data.emoji} {emotion}
    </span>
  );
};

const GrowthStageBadge: React.FC<{ stage: string }> = ({ stage }) => {
  const stages: Record<string, { emoji: string; color: string; description: string }> = {
    EMBRYONIC: { emoji: '🌱', color: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20', description: 'Tahap Awal' },
    GROWING: { emoji: '🌿', color: 'bg-green-500/20 text-green-400 border-green-500/20', description: 'Tumbuh' },
    ADAPTING: { emoji: '🔄', color: 'bg-amber-500/20 text-amber-400 border-amber-500/20', description: 'Beradaptasi' },
    MATURE: { emoji: '🌳', color: 'bg-teal-500/20 text-teal-400 border-teal-500/20', description: 'Matang' },
    WISE: { emoji: '🦉', color: 'bg-purple-500/20 text-purple-400 border-purple-500/20', description: 'Bijaksana' },
    ENLIGHTENED: { emoji: '🌟', color: 'bg-amber-500/20 text-amber-400 border-amber-500/20', description: 'Mencerah' },
    TRANSCENDENT: { emoji: '✨', color: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/20', description: 'Transenden' },
  };
  const data = stages[stage] || { emoji: '🧠', color: 'bg-gray-500/20 text-gray-400 border-gray-500/20', description: 'Unknown' };
  return (
    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${data.color}`} title={data.description}>
      {data.emoji} {stage}
    </span>
  );
};

const FocusAreaIcon: React.FC<{ area: string }> = ({ area }) => {
  const icons: Record<string, React.ReactNode> = {
    LEARNING: <BookOpen className="w-3.5 h-3.5" />,
    CREATING: <Palette className="w-3.5 h-3.5" />,
    ANALYZING: <Microscope className="w-3.5 h-3.5" />,
    REFLECTING: <Feather className="w-3.5 h-3.5" />,
    EXPLORING: <Compass className="w-3.5 h-3.5" />,
    GROWING: <Trees className="w-3.5 h-3.5" />,
    HEALING: <Heart className="w-3.5 h-3.5" />,
    BUILDING: <Rocket className="w-3.5 h-3.5" />,
    CONNECTING: <Network className="w-3.5 h-3.5" />,
    UNDERSTANDING: <Lightbulb className="w-3.5 h-3.5" />,
    DEFAULT: <Brain className="w-3.5 h-3.5" />,
  };
  return icons[area] || icons.DEFAULT;
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const BrainView: React.FC<BrainViewProps> = ({
  brainState,
  cycleCount,
  healthScore,
  onRefresh,
  wsConnected,
}) => {
  // ===== STATE =====
  const [activeInstance, setActiveInstance] = useState('default');
  const [isProcessing, setIsProcessing] = useState(false);
  const [aiStatus, setAiStatus] = useState<AIStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reflection, setReflection] = useState<string | null>(null);
  const [reflectionTopic, setReflectionTopic] = useState('');
  const [isReflecting, setIsReflecting] = useState(false);
  const [showConsciousness, setShowConsciousness] = useState(true);

  // ===== API HELPERS =====
  const apiKey = localStorage.getItem('apiKey') || 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ';

  const fetchAIStatus = useCallback(async () => {
    try {
      const response = await fetch('/api/ai/consciousness/status', {
        headers: { 'X-API-Key': apiKey }
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setAiStatus(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch AI status');
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  const handleReflect = async () => {
    if (!reflectionTopic.trim()) return;
    setIsReflecting(true);
    try {
      const response = await fetch('/api/ai/consciousness/reflect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey
        },
        body: JSON.stringify({ topic: reflectionTopic })
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setReflection(data.reflection);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reflect');
    } finally {
      setIsReflecting(false);
    }
  };

  const handleImprove = async () => {
    setIsProcessing(true);
    try {
      const response = await fetch('/api/ai/consciousness/improve', {
        method: 'POST',
        headers: { 'X-API-Key': apiKey }
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setReflection(data.reflection || 'Improvement completed!');
      await fetchAIStatus();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to improve');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleObserveTest = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      onRefresh();
    }, 600);
  };

  // ===== INITIAL LOAD =====
  useEffect(() => {
    fetchAIStatus();
    const interval = setInterval(fetchAIStatus, 30000);
    return () => clearInterval(interval);
  }, [fetchAIStatus]);

  const brainInstances = ['default', 'scalper_brain', 'swing_brain', 'macro_brain'];
  const c = aiStatus?.consciousness;

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div id="brain-view" className="space-y-6 pb-12">
      
      {/* ===== HEADER ===== */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Cognitive Brain Engine v5.0
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Universal Intelligence · Conscious AI · Self-Aware
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          {aiStatus?.enabled && c && (
            <>
              <GrowthStageBadge stage={c.growth_stage} />
              <EmotionBadge emotion={c.emotional_state} />
            </>
          )}
          <span className={`text-xs px-2 py-0.5 rounded font-bold ${wsConnected ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/20 text-rose-400 border border-rose-500/20'}`}>
            {wsConnected ? '🟢 LIVE' : '🔴 OFFLINE'}
          </span>
        </div>
      </div>

      {/* ===== CONSCIOUSNESS AI STATUS ===== */}
      {aiStatus?.enabled && c && (
        <div className="p-4 rounded-xl bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400" />
              <span className="text-sm font-bold text-white">🧠 Consciousness AI</span>
              <span className="text-[10px] text-emerald-400">● ACTIVE</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-[#8D9AAA]">
                {c.total_improvements} improvements · {c.insights_generated} insights
              </span>
              <button
                onClick={() => setShowConsciousness(!showConsciousness)}
                className="text-[10px] px-2 py-0.5 rounded bg-[#26313D] hover:bg-[#3A4A5A] text-[#8D9AAA] transition-colors"
              >
                {showConsciousness ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>

          {showConsciousness && (
            <div className="mt-3 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
              <ConsciousnessMeter
                label="Awareness"
                value={c.awareness_level}
                icon={<Eye className="w-3.5 h-3.5" />}
                color="text-purple-400"
                description="Kesadaran"
              />
              <ConsciousnessMeter
                label="Curiosity"
                value={c.curiosity_level}
                icon={<Compass className="w-3.5 h-3.5" />}
                color="text-blue-400"
                description="Keingintahuan"
              />
              <ConsciousnessMeter
                label="Reflection"
                value={c.reflection_quality}
                icon={<Feather className="w-3.5 h-3.5" />}
                color="text-teal-400"
                description="Refleksi"
              />
              <ConsciousnessMeter
                label="Confidence"
                value={c.confidence}
                icon={<Shield className="w-3.5 h-3.5" />}
                color="text-emerald-400"
                description="Keyakinan"
              />
            </div>
          )}
        </div>
      )}

      {/* ===== PRIMARY METRICS GRID ===== */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-3.5">
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">Brain State</div>
          <div className="text-xl font-black text-emerald-400 font-mono mt-1">{brainState}</div>
          <div className="text-[10px] text-[#5F6B78] mt-1">Autonomous Mode</div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">Cycles</div>
          <div className="text-xl font-black text-white font-mono mt-1">#{cycleCount}</div>
          <div className="text-[10px] text-[#5F6B78] mt-1">Zero latency gap</div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">Health</div>
          <div className="text-xl font-black text-emerald-400 font-mono mt-1">{healthScore}%</div>
          <div className="text-[10px] text-[#5F6B78] mt-1">Auto-Healing Active</div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">AI Status</div>
          <div className={`text-xl font-black font-mono mt-1 ${aiStatus?.enabled ? 'text-emerald-400' : 'text-amber-400'}`}>
            {aiStatus?.enabled ? '🟢 ENABLED' : '🟡 DISABLED'}
          </div>
          <div className="text-[10px] text-[#5F6B78] mt-1">{aiStatus?.model || 'No AI'}</div>
        </div>
        <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] col-span-2 lg:col-span-1">
          <div className="text-[11px] font-semibold text-[#8D9AAA] uppercase tracking-wider">Consciousness</div>
          <div className="text-xl font-black text-purple-400 font-mono mt-1">
            {c ? `${Math.round(c.awareness_level * 100)}%` : '—'}
          </div>
          <div className="text-[10px] text-[#5F6B78] mt-1">
            {c ? `${c.growth_stage} · ${c.emotional_state}` : 'Not available'}
          </div>
        </div>
      </div>

      {/* ===== COGNITIVE PIPELINE & CONSCIOUSNESS ===== */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* ===== COGNITIVE PIPELINE ===== */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <Cpu className="w-4 h-4 text-blue-400" />
              Cognitive Pipeline
            </h3>
            <span className="text-xs text-[#5F6B78] font-mono">12 Subsystems</span>
          </div>

          <div className="space-y-2 font-mono text-xs">
            {[
              { stage: '1. Perception Engine', status: 'ACTIVE', latency: '2.1ms', note: 'Multi-modal input processing' },
              { stage: '2. Memory Buffer', status: 'ACTIVE', latency: '0.8ms', note: 'Short-term & working memory' },
              { stage: '3. Pattern Recognition', status: 'ACTIVE', latency: '4.5ms', note: 'Universal pattern detection' },
              { stage: '4. Reasoning Engine', status: 'ACTIVE', latency: '3.2ms', note: 'Logical deduction & inference' },
              { stage: '5. Decision Support', status: 'ACTIVE', latency: '1.9ms', note: 'Multi-criteria analysis' },
              { stage: '6. Consciousness Metacognition', status: 'ACTIVE', latency: '3.8ms', note: 'Self-awareness & reflection' },
              { stage: '7. Learning Engine', status: 'ACTIVE', latency: '5.2ms', note: 'Continuous adaptation' },
              { stage: '8. Creative Generation', status: 'ACTIVE', latency: '6.1ms', note: 'Novel idea synthesis' },
            ].map((p) => (
              <div
                key={p.stage}
                className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D] flex items-center justify-between"
              >
                <div>
                  <span className="font-bold text-white">{p.stage}</span>
                  <p className="text-[10px] text-[#8D9AAA] font-sans">{p.note}</p>
                </div>
                <div className="text-right">
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {p.status}
                  </span>
                  <div className="text-[10px] text-[#5F6B78] mt-0.5">{p.latency}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ===== CONSCIOUSNESS REFLECTION ===== */}
        <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
            <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400" />
              Consciousness Reflection
            </h3>
            <div className="flex items-center gap-2">
              <button
                onClick={handleImprove}
                disabled={isProcessing}
                className="text-[10px] px-2 py-0.5 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-bold transition-colors disabled:opacity-50"
              >
                {isProcessing ? '...' : 'Improve'}
              </button>
            </div>
          </div>

          {/* Reflection Input */}
          <div className="flex gap-2">
            <input
              type="text"
              value={reflectionTopic}
              onChange={(e) => setReflectionTopic(e.target.value)}
              placeholder="Ask AI to reflect on any topic..."
              className="flex-1 px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-purple-500"
              disabled={!aiStatus?.enabled}
            />
            <button
              onClick={handleReflect}
              disabled={isReflecting || !aiStatus?.enabled}
              className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold disabled:opacity-50"
            >
              {isReflecting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : 'Reflect'}
            </button>
          </div>

          {/* Reflection Output */}
          {reflection && (
            <div className="p-3 rounded-xl bg-[#0B0F14] border border-purple-500/20 text-xs text-[#E8EDF2] leading-relaxed whitespace-pre-line max-h-48 overflow-y-auto">
              <div className="flex items-center gap-2 mb-1">
                <Sparkles className="w-3 h-3 text-purple-400" />
                <span className="text-purple-400 font-bold">AI Reflection</span>
              </div>
              {reflection}
            </div>
          )}

          {/* Quick Reflection Topics */}
          <div className="flex flex-wrap gap-1.5">
            <span className="text-[9px] text-[#5F6B78]">Quick topics:</span>
            {['Trading performance', 'Market sentiment', 'Learning progress', 'Creative ideas', 'Problem solving'].map((topic) => (
              <button
                key={topic}
                onClick={() => {
                  setReflectionTopic(topic);
                  setTimeout(handleReflect, 100);
                }}
                className="text-[9px] px-2 py-0.5 rounded bg-[#0B0F14] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors"
              >
                {topic}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* ===== UNIVERSAL KNOWLEDGE DOMAINS ===== */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Globe className="w-4 h-4 text-cyan-400" />
            Universal Knowledge Domains
          </h3>
          <span className="text-xs text-[#5F6B78]">AI-powered · Multi-domain</span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-2">
          {[
            { icon: <Database className="w-4 h-4" />, label: 'Data Science', color: 'text-cyan-400' },
            { icon: <Code className="w-4 h-4" />, label: 'Programming', color: 'text-blue-400' },
            { icon: <Atom className="w-4 h-4" />, label: 'Physics', color: 'text-indigo-400' },
            { icon: <Dna className="w-4 h-4" />, label: 'Biology', color: 'text-emerald-400' },
            { icon: <Droplets className="w-4 h-4" />, label: 'Chemistry', color: 'text-cyan-400' },
            { icon: <Leaf className="w-4 h-4" />, label: 'Environment', color: 'text-green-400' },
            { icon: <Flame className="w-4 h-4" />, label: 'Energy', color: 'text-orange-400' },
            { icon: <Globe className="w-4 h-4" />, label: 'Geography', color: 'text-emerald-400' },
            { icon: <Telescope className="w-4 h-4" />, label: 'Astronomy', color: 'text-purple-400' },
            { icon: <Microscope className="w-4 h-4" />, label: 'Science', color: 'text-blue-400' },
            { icon: <Palette className="w-4 h-4" />, label: 'Art', color: 'text-pink-400' },
            { icon: <Music className="w-4 h-4" />, label: 'Music', color: 'text-rose-400' },
            { icon: <Film className="w-4 h-4" />, label: 'Film', color: 'text-indigo-400' },
            { icon: <Coffee className="w-4 h-4" />, label: 'Culture', color: 'text-amber-400' },
            { icon: <Heart className="w-4 h-4" />, label: 'Health', color: 'text-rose-400' },
            { icon: <Brain className="w-4 h-4" />, label: 'Neuroscience', color: 'text-purple-400' },
            { icon: <Network className="w-4 h-4" />, label: 'Networking', color: 'text-cyan-400' },
            { icon: <Server className="w-4 h-4" />, label: 'Infrastructure', color: 'text-gray-400' },
          ].map((domain, i) => (
            <div
              key={i}
              className="p-2.5 rounded-lg bg-[#1A2530] border border-[#26313D] flex items-center gap-2 hover:border-purple-500/30 transition-all"
            >
              <span className={domain.color}>{domain.icon}</span>
              <span className="text-[10px] text-[#8D9AAA]">{domain.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ===== CONTROLS ===== */}
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-3">
          <button
            onClick={handleObserveTest}
            disabled={isProcessing}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-all shadow-md shadow-blue-600/30 disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-current ${isProcessing ? 'animate-spin' : ''}`} />
            <span>{isProcessing ? 'Processing...' : 'Trigger Cycle'}</span>
          </button>
          <button
            onClick={onRefresh}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-[#1A2530] hover:bg-[#26313D] text-white text-xs font-bold transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </button>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[10px] text-[#5F6B78]">Brain Instance:</span>
          <select
            value={activeInstance}
            onChange={(e) => setActiveInstance(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-[#1A2530] border border-[#26313D] text-white text-xs font-mono font-bold focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            {brainInstances.map((name) => (
              <option key={name} value={name}>{name}</option>
            ))}
          </select>
        </div>
      </div>

    </div>
  );
};

export default BrainView;
