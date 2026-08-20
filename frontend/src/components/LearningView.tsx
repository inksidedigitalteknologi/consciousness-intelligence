import React, { useState } from 'react';
import {
  GraduationCap,
  Play,
  RefreshCw,
  Rss,
  Layers,
  CheckCircle2,
  Cpu,
  BarChart2,
  Sparkles,
  Target,
  Search,
  Sliders,
  Database,
  ShieldCheck,
  AlertTriangle,
  Lightbulb,
  Compass,
  ArrowRight,
  TrendingUp,
  Share2,
  Workflow,
  Zap,
  BookOpen,
  Send,
  Plus,
} from 'lucide-react';

interface LearningViewProps {
  learningActive: boolean;
  cycleCount: number;
}

type TabType =
  | 'overview'
  | 'adaptive'
  | 'curiosity'
  | 'goals'
  | 'experience'
  | 'simulation'
  | 'knowledge_graph'
  | 'evaluator';

export const LearningView: React.FC<LearningViewProps> = ({ learningActive, cycleCount }) => {
  const [activeTab, setActiveTab] = useState<TabType>('overview');

  // Registered Modules Matrix (25+ Modules from INKSIDE Intelligence OS)
  const allModules = [
    { name: 'learning_engine', title: 'Learning Engine Kernel', version: '2.1.2', prio: 10, status: 'ONLINE', role: 'Kernel Coordinator' },
    { name: 'market_learning', title: 'Market Learning Engine', version: '2.1', prio: 30, status: 'ONLINE', role: 'MTF & Signal Learning' },
    { name: 'pattern_engine', title: 'Pattern Recognition Engine', version: '3.1', prio: 40, status: 'ONLINE', role: 'Candlestick & Wave Scanner' },
    { name: 'prediction', title: 'Prediction & Forecasting Engine', version: '4.0', prio: 50, status: 'ONLINE', role: 'Monte Carlo & ML Forecast' },
    { name: 'reasoning', title: 'Cognitive Reasoning Engine', version: '3.0', prio: 60, status: 'ONLINE', role: 'Multi-Domain Logic' },
    { name: 'decision_engine', title: 'Decision Support Engine', version: '2.0', prio: 70, status: 'ONLINE', role: 'Action & Execution Bias' },
    { name: 'strategy', title: 'Strategy Generation Engine', version: '2.0', prio: 75, status: 'ONLINE', role: 'Entry/Exit & Position Sizing' },
    { name: 'simulation', title: 'Scenario Simulation Engine', version: '3.0', prio: 80, status: 'ONLINE', role: 'Monte Carlo Stochastic Drift' },
    { name: 'reflection', title: 'Reflection & Cognitive Mirror', version: '2.0', prio: 85, status: 'ONLINE', role: 'Outcome Learning & Lessons' },
    { name: 'evaluator', title: 'General Evaluation Engine', version: '2.1', prio: 90, status: 'ONLINE', role: 'Accuracy & Calibration' },
    { name: 'adaptive', title: 'Adaptive Weight Engine', version: '3.0', prio: 95, status: 'ONLINE', role: 'Forgetting & Dynamic Weights' },
    { name: 'curiosity', title: 'Curiosity & Discovery Engine', version: '3.0', prio: 100, status: 'ONLINE', role: 'Knowledge Gap Questioning' },
    { name: 'goal_manager', title: 'Goal Management Engine', version: '3.0', prio: 105, status: 'ONLINE', role: 'Milestones & Objectives' },
    { name: 'experience', title: 'Experience Engine', version: '3.0', prio: 110, status: 'ONLINE', role: 'Experience Replay & Clustering' },
    { name: 'knowledge_builder', title: 'Knowledge Builder Engine', version: '3.0', prio: 115, status: 'ONLINE', role: 'Concept Extraction' },
    { name: 'knowledge_graph', title: 'Knowledge Graph Engine', version: '3.0', prio: 120, status: 'ONLINE', role: 'Weighted Graph Discovery' },
    { name: 'semantic_memory', title: 'Semantic Vector Memory', version: '3.0', prio: 125, status: 'ONLINE', role: 'Semantic Retrieval & Concepts' },
    { name: 'semantic_processor', title: 'Semantic Processor Engine', version: '2.0', prio: 130, status: 'ONLINE', role: 'Intent & Topic Analysis' },
    { name: 'entity_recognition', title: 'Entity Recognition Engine', version: '2.0', prio: 135, status: 'ONLINE', role: 'Crypto & Indicator NER' },
    { name: 'feature_extractor', title: 'Feature Extractor Engine', version: '2.0', prio: 140, status: 'ONLINE', role: 'OHLC & Text Features' },
    { name: 'normalizer', title: 'Data Normalizer Engine', version: '2.0', prio: 145, status: 'ONLINE', role: 'Standardized Payload Format' },
    { name: 'data_cleaner', title: 'Data Cleaner Engine', version: '2.0', prio: 150, status: 'ONLINE', role: 'NaN / Inf / Duplicate Purge' },
    { name: 'collector', title: 'Data Collector Layer', version: '2.0', prio: 155, status: 'ONLINE', role: 'Ingestion Envelopes' },
    { name: 'self_diagnostic', title: 'Self Diagnostic Engine', version: '2.0', prio: 160, status: 'ONLINE', role: 'Subsystem Health Verifier' },
    { name: 'improvement', title: 'Improvement Engine', version: '2.0', prio: 165, status: 'ONLINE', role: 'Weakness Rectification' },
    { name: 'behavior', title: 'Behavior Learning Engine', version: '3.0', prio: 170, status: 'ONLINE', role: 'Behavioral Pattern Trends' },
    { name: 'association', title: 'Association Engine', version: '2.0', prio: 175, status: 'ONLINE', role: 'Co-occurrence Graph' },
    { name: 'memory_optimizer', title: 'Memory Optimizer Engine', version: '2.0', prio: 180, status: 'ONLINE', role: 'Deduplication & Ranking' },
    { name: 'archive_manager', title: 'Archive Storage Manager', version: '2.0', prio: 185, status: 'ONLINE', role: 'Backup & Permanent Store' },
    { name: 'event_system', title: 'Event Bus Subsystem', version: '3.1', prio: 190, status: 'ONLINE', role: 'Async Priority Event Dispatch' },
  ];

  // --- STATE FOR ADAPTIVE TAB ---
  const [adaptiveEntries, setAdaptiveEntries] = useState([
    { key: 'btc.breakout_confirmation', domain: 'trading', weight: 74.5, confidence: 88.2, reliability: 82.0, successRate: 84.5, attempts: 142 },
    { key: 'rsi.oversold_reversal', domain: 'trading', weight: 68.2, confidence: 79.4, reliability: 75.0, successRate: 78.0, attempts: 98 },
    { key: 'eth.fibonacci_0618_bounce', domain: 'trading', weight: 81.0, confidence: 91.5, reliability: 86.5, successRate: 89.2, attempts: 65 },
    { key: 'volume.spike_expansion', domain: 'market', weight: 77.0, confidence: 85.0, reliability: 80.0, successRate: 82.5, attempts: 110 },
    { key: 'knowledge.geography_capitals', domain: 'knowledge', weight: 95.0, confidence: 98.0, reliability: 96.0, successRate: 98.5, attempts: 210 },
    { key: 'reasoning.causal_deduction', domain: 'reasoning', weight: 84.0, confidence: 89.0, reliability: 84.0, successRate: 88.0, attempts: 155 },
  ]);

  // --- STATE FOR CURIOSITY TAB ---
  const [questions, setQuestions] = useState([
    { id: 'q-101', question: 'Why does ADA/USD 4h timeframe show repeated false breakouts at 50 EMA?', domain: 'trading', area: 'ada.false_breakout', priority: 88, status: 'UNRESOLVED' },
    { id: 'q-102', question: 'What causes prediction divergence between MACD and RSI on 15m XRP/USD?', domain: 'trading', area: 'xrp.indicator_divergence', priority: 79, status: 'INVESTIGATING' },
    { id: 'q-103', question: 'How can volatility decay rate be calibrated dynamically during FOMC rate announcements?', domain: 'market', area: 'market.fomc_volatility', priority: 92, status: 'UNRESOLVED' },
    { id: 'q-104', question: 'Why is confidence score below 60% in low-liquidity overnight sessions?', domain: 'performance', area: 'engine.overnight_confidence', priority: 72, status: 'RESOLVED', answer: 'Resolved: Applied 0.7x weight penalty on volume during Asian session low-liquidity hours.' },
  ]);
  const [newQuestionInput, setNewQuestionInput] = useState('');

  // --- STATE FOR GOALS TAB ---
  const [goals, setGoals] = useState([
    { id: 'g-1', title: 'Achieve 90%+ MTF Signal Accuracy on BTC/USD', priority: 'CRITICAL', progress: 84.5, status: 'ACTIVE', objective: 'Calibrate 5m to 1d alignment filters' },
    { id: 'g-2', title: 'Reduce False Reversal Signals on 15m timeframe', priority: 'HIGH', progress: 72.0, status: 'ACTIVE', objective: 'Integrate ATR volatility filter' },
    { id: 'g-3', title: 'Consolidate 3,000 Memory Vectors into Long-Term Store', priority: 'NORMAL', progress: 95.0, status: 'ACTIVE', objective: 'SQLite batch migration' },
    { id: 'g-4', title: 'Zero Circuit-Breaker Faults in Kraken Bridge', priority: 'CRITICAL', progress: 100.0, status: 'COMPLETED', objective: 'Exponential backoff implementation' },
  ]);

  // --- STATE FOR SIMULATION TAB ---
  const [scenarioInput, setScenarioInput] = useState('BTC price spikes +5% on breakout with high volume expansion');
  const [simulationResult, setSimulationResult] = useState<any>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const handleSimulateScenario = () => {
    setIsSimulating(true);
    setTimeout(() => {
      setIsSimulating(false);
      setSimulationResult({
        direction: 'positive',
        impact: 'high',
        risk: 'LOW',
        risk_score: 25.0,
        confidence: 89,
        probability: 0.89,
        possible_effect: 'Momentum may strengthen and price expansion may continue past key resistance.',
        assumptions: [
          'Volume data remains representative of institutional market participation.',
          'Current momentum remains active across 1h and 4h horizons.',
          'No unexpected macro circuit-breaker event occurs.'
        ],
        monte_carlo: {
          iterations: 1000,
          mean_confidence: 88.4,
          percentile_5: 82.1,
          percentile_95: 94.8,
        },
      });
    }, 450);
  };

  const handleAddQuestion = () => {
    if (!newQuestionInput.trim()) return;
    const newQ = {
      id: `q-${Date.now().toString().slice(-4)}`,
      question: newQuestionInput.trim(),
      domain: 'trading',
      area: 'custom_discovery',
      priority: 80,
      status: 'UNRESOLVED',
    };
    setQuestions([newQ, ...questions]);
    setNewQuestionInput('');
  };

  return (
    <div id="learning-view" className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <GraduationCap className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Autonomous Intelligence Learning Suite v3.0
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Kernel v2.1.2 · 30 Subsystems: Adaptive Weights, Curiosity Gap Finder, Goal Manager & Monte Carlo Simulation
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-semibold text-[#8D9AAA]">Learning Kernel:</span>
          <span
            className={`text-xs font-mono font-bold px-3 py-1 rounded-lg ${
              learningActive
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 animate-pulse'
                : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
            }`}
          >
            {learningActive ? 'AUTONOMOUS ACTIVE' : 'IDLE'}
          </span>
        </div>
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex flex-wrap items-center gap-2 p-1.5 rounded-xl bg-[#131A22] border border-[#26313D]">
        {[
          { id: 'overview', label: 'Kernel Overview & Registry', icon: Layers },
          { id: 'adaptive', label: 'Adaptive Weights v3.0', icon: Sliders },
          { id: 'curiosity', label: 'Curiosity & Gaps v3.0', icon: Compass },
          { id: 'goals', label: 'Goal Manager v3.0', icon: Target },
          { id: 'simulation', label: 'Scenario & Monte Carlo', icon: Sparkles },
          { id: 'experience', label: 'Experience Engine v3.0', icon: Database },
          { id: 'knowledge_graph', label: 'Knowledge Graph v3.0', icon: Share2 },
          { id: 'evaluator', label: 'Evaluator & Improvements', icon: ShieldCheck },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as TabType)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-bold font-mono transition-all cursor-pointer ${
                isActive
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'text-[#8D9AAA] hover:bg-[#1A2530] hover:text-white'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* TAB 1: KERNEL OVERVIEW & REGISTRY */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Quick Metrics */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
            <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
              <div className="text-[10px] uppercase font-bold text-[#8D9AAA]">Learning Cycles</div>
              <div className="text-xl font-black text-white font-mono mt-1">#{cycleCount}</div>
              <div className="w-full bg-[#0B0F14] h-1.5 rounded-full mt-2 overflow-hidden">
                <div className="bg-emerald-500 h-full" style={{ width: `${Math.min(100, cycleCount % 100)}%` }} />
              </div>
            </div>

            <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
              <div className="text-[10px] uppercase font-bold text-[#8D9AAA]">Registered Subsystems</div>
              <div className="text-xl font-black text-emerald-400 font-mono mt-1">
                {allModules.length} Modules
              </div>
              <div className="text-[10px] text-[#5F6B78] mt-1">100% Contract v2.0 Compliant</div>
            </div>

            <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
              <div className="text-[10px] uppercase font-bold text-[#8D9AAA]">Adaptive Learning Rate</div>
              <div className="text-xl font-black text-purple-400 font-mono mt-1">1.00x</div>
              <div className="text-[10px] text-[#5F6B78] mt-1">With 0.005h Decay Rate</div>
            </div>

            <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
              <div className="text-[10px] uppercase font-bold text-[#8D9AAA]">Circuit Breakers</div>
              <div className="text-xl font-black text-cyan-400 font-mono mt-1">0 Open (CLOSED)</div>
              <div className="text-[10px] text-emerald-400 mt-1">All Safe & Operational</div>
            </div>
          </div>

          {/* Module Registry Table */}
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] shadow-lg space-y-3">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Layers className="w-4 h-4 text-emerald-400" />
                All 30 Intelligence OS Modules Matrix (Registry v4.3)
              </h3>
              <span className="text-xs text-[#5F6B78] font-mono">Kernel v2.1.2</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5 max-h-[500px] overflow-y-auto pr-1">
              {allModules.map((m) => (
                <div
                  key={m.name}
                  className="p-3 rounded-xl bg-[#1A2530] border border-[#26313D] flex items-center justify-between hover:border-emerald-500/40 transition-colors"
                >
                  <div>
                    <div className="font-bold text-white text-xs flex items-center gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span>{m.title}</span>
                    </div>
                    <div className="text-[10px] text-[#8D9AAA] mt-0.5 font-mono">
                      <code>{m.name}.py</code> · v{m.version}
                    </div>
                    <div className="text-[10px] text-[#5F6B78] mt-0.5">{m.role}</div>
                  </div>
                  <div className="text-right">
                    <span className="text-[9px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      {m.status}
                    </span>
                    <div className="text-[9px] text-[#5F6B78] mt-1 font-mono">Prio {m.prio}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: ADAPTIVE LEARNING V3.0 */}
      {activeTab === 'adaptive' && (
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Sliders className="w-4 h-4 text-purple-400" />
                Adaptive Weights & Confidence Calibration (adaptive.py v3.0)
              </h3>
              <span className="text-xs text-purple-400 font-mono font-bold">Dynamic Reinforcement</span>
            </div>

            <p className="text-xs text-[#8D9AAA]">
              Weights adapt dynamically based on actual trade outcomes, reward-to-risk performance, and time-decay curves.
            </p>

            <div className="divide-y divide-[#26313D]/40 font-mono text-xs">
              {adaptiveEntries.map((entry) => (
                <div key={entry.key} className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div>
                    <div className="font-bold text-white text-sm">{entry.key}</div>
                    <div className="text-[10px] text-[#8D9AAA] font-sans">
                      Domain: <span className="text-cyan-400">{entry.domain}</span> · {entry.attempts} total attempts
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-right">
                    <div>
                      <div className="text-[10px] text-[#5F6B78]">Weight Score</div>
                      <div className="text-purple-400 font-bold text-sm">{entry.weight} / 100</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-[#5F6B78]">Confidence</div>
                      <div className="text-emerald-400 font-bold text-sm">{entry.confidence}%</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-[#5F6B78]">Success Rate</div>
                      <div className="text-white font-bold text-sm">{entry.successRate}%</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: CURIOSITY & GAPS V3.0 */}
      {activeTab === 'curiosity' && (
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Compass className="w-4 h-4 text-cyan-400" />
                Knowledge Gap Discovery & Automated Questioning (curiosity.py v3.0)
              </h3>
              <span className="text-xs text-cyan-400 font-mono font-bold">{questions.length} Questions</span>
            </div>

            {/* Input to Ask Question */}
            <div className="flex gap-2">
              <input
                type="text"
                value={newQuestionInput}
                onChange={(e) => setNewQuestionInput(e.target.value)}
                placeholder="Ask or inject an autonomous learning research question..."
                className="flex-1 px-3.5 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-cyan-500"
              />
              <button
                onClick={handleAddQuestion}
                className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-1.5 cursor-pointer shadow-md shadow-cyan-600/20"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Inject Question</span>
              </button>
            </div>

            {/* Questions List */}
            <div className="space-y-3 font-mono text-xs">
              {questions.map((q) => (
                <div
                  key={q.id}
                  className="p-3.5 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white text-sm font-sans">{q.question}</span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                        q.status === 'RESOLVED'
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                          : q.status === 'INVESTIGATING'
                          ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                          : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                      }`}
                    >
                      {q.status} · Prio {q.priority}
                    </span>
                  </div>
                  <div className="text-[10px] text-[#8D9AAA]">
                    Area: <code className="text-cyan-400">{q.area}</code> · Domain: {q.domain}
                  </div>
                  {q.answer && (
                    <div className="p-2.5 rounded-lg bg-[#0B0F14] border border-emerald-500/20 text-emerald-300 text-[11px] font-sans">
                      {q.answer}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: GOAL MANAGER V3.0 */}
      {activeTab === 'goals' && (
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Target className="w-4 h-4 text-emerald-400" />
                Autonomous Goal Manager & Milestones (goal_manager.py v3.0)
              </h3>
              <span className="text-xs text-emerald-400 font-mono font-bold">4 Active Objectives</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {goals.map((g) => (
                <div key={g.id} className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white text-sm font-sans">{g.title}</span>
                    <span
                      className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded border ${
                        g.priority === 'CRITICAL'
                          ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                          : 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                      }`}
                    >
                      {g.priority}
                    </span>
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between text-[10px] font-mono text-[#8D9AAA]">
                      <span>Progress</span>
                      <span className="text-white font-bold">{g.progress}%</span>
                    </div>
                    <div className="w-full bg-[#0B0F14] h-2 rounded-full overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-emerald-400 h-full"
                        style={{ width: `${g.progress}%` }}
                      />
                    </div>
                  </div>

                  <div className="text-[10px] text-[#8D9AAA] font-sans">
                    Objective: <strong className="text-white">{g.objective}</strong>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 5: SCENARIO & MONTE CARLO */}
      {activeTab === 'simulation' && (
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                Scenario Simulation & Monte Carlo Engine (simulation.py v3.0)
              </h3>
              <span className="text-xs text-cyan-400 font-mono font-bold">Stochastic Gaussian Modeling</span>
            </div>

            <div className="space-y-3">
              <label className="text-xs text-white font-bold block">Input Market Scenario</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={scenarioInput}
                  onChange={(e) => setScenarioInput(e.target.value)}
                  placeholder="Enter hypothetical market scenario..."
                  className="flex-1 px-3.5 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-cyan-500"
                />
                <button
                  onClick={handleSimulateScenario}
                  disabled={isSimulating}
                  className="px-5 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs shadow-md shadow-cyan-600/30 flex items-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>{isSimulating ? 'Simulating...' : 'Simulate Scenario'}</span>
                </button>
              </div>

              {simulationResult && (
                <div className="p-4 rounded-xl bg-[#0B0F14] border border-cyan-500/30 space-y-3 font-mono text-xs">
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                    <div className="p-2.5 bg-[#131A22] rounded-lg">
                      <span className="text-[10px] text-[#5F6B78] block">Estimated Direction</span>
                      <span className="text-emerald-400 font-bold text-sm">{simulationResult.direction.toUpperCase()}</span>
                    </div>
                    <div className="p-2.5 bg-[#131A22] rounded-lg">
                      <span className="text-[10px] text-[#5F6B78] block">Impact Level</span>
                      <span className="text-purple-400 font-bold text-sm">{simulationResult.impact.toUpperCase()}</span>
                    </div>
                    <div className="p-2.5 bg-[#131A22] rounded-lg">
                      <span className="text-[10px] text-[#5F6B78] block">Risk Rating</span>
                      <span className="text-emerald-400 font-bold text-sm">{simulationResult.risk} ({simulationResult.risk_score}%)</span>
                    </div>
                    <div className="p-2.5 bg-[#131A22] rounded-lg">
                      <span className="text-[10px] text-[#5F6B78] block">Confidence</span>
                      <span className="text-white font-bold text-sm">{simulationResult.confidence}%</span>
                    </div>
                  </div>

                  <div className="p-3 bg-[#131A22] rounded-lg border border-[#26313D]/60 space-y-1 font-sans text-xs">
                    <div className="font-bold text-white">Possible Effect:</div>
                    <div className="text-[#8D9AAA]">{simulationResult.possible_effect}</div>
                  </div>

                  <div className="p-3 bg-[#131A22] rounded-lg border border-[#26313D]/60 space-y-1 font-mono text-[11px]">
                    <div className="font-bold text-cyan-400">Monte Carlo Confidence Interval:</div>
                    <div className="text-[#8D9AAA]">
                      Mean: <strong className="text-white">{simulationResult.monte_carlo.mean_confidence}%</strong> · 5th Percentile: {simulationResult.monte_carlo.percentile_5}% · 95th Percentile: {simulationResult.monte_carlo.percentile_95}%
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* TAB 6: EXPERIENCE ENGINE */}
      {activeTab === 'experience' && (
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Database className="w-4 h-4 text-emerald-400" />
                Experience Engine & Memory Consolidation (experience.py v3.0)
              </h3>
              <span className="text-xs text-emerald-400 font-mono font-bold">2,450 Stored Experiences</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <div className="text-[10px] text-[#5F6B78]">Sensory Buffer</div>
                <div className="text-base font-bold text-white">12 Items</div>
              </div>
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <div className="text-[10px] text-[#5F6B78]">Short-Term Memory</div>
                <div className="text-base font-bold text-white">48 Items</div>
              </div>
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <div className="text-[10px] text-[#5F6B78]">Working Memory</div>
                <div className="text-base font-bold text-emerald-400">320 Items</div>
              </div>
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <div className="text-[10px] text-[#5F6B78]">Permanent Consolidated</div>
                <div className="text-base font-bold text-purple-400">2,070 Items</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 7: KNOWLEDGE GRAPH & BUILDER */}
      {activeTab === 'knowledge_graph' && (
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <Share2 className="w-4 h-4 text-purple-400" />
                Knowledge Graph & Concept Builder (knowledge_graph.py v3.0)
              </h3>
              <span className="text-xs text-purple-400 font-mono font-bold">120 Concepts · 480 Relations</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 font-mono text-xs">
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] space-y-2">
                <div className="text-sm font-bold text-white">Breakout Concept Graph</div>
                <div className="text-[11px] text-[#8D9AAA]">
                  <code>breakout</code> --[supports]--&gt; <code>volume_expansion</code> (weight: 4.8)
                </div>
                <div className="text-[11px] text-[#8D9AAA]">
                  <code>breakout</code> --[associated]--&gt; <code>resistance_level</code> (weight: 3.9)
                </div>
              </div>

              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D] space-y-2">
                <div className="text-sm font-bold text-white">Macro Indicator Graph</div>
                <div className="text-[11px] text-[#8D9AAA]">
                  <code>interest_rate_cut</code> --[influences]--&gt; <code>crypto_liquidity</code> (weight: 4.2)
                </div>
                <div className="text-[11px] text-[#8D9AAA]">
                  <code>cpi_inflation</code> --[precedes]--&gt; <code>market_volatility</code> (weight: 3.7)
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 8: EVALUATOR & IMPROVEMENTS */}
      {activeTab === 'evaluator' && (
        <div className="space-y-6">
          <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
              <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                General Evaluator & Improvement Engine (evaluator.py & improvement.py v2.0)
              </h3>
              <span className="text-xs text-emerald-400 font-mono font-bold">Accuracy: 88.4%</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 font-mono text-xs">
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <span className="text-[10px] text-[#5F6B78] block">Total Evaluations</span>
                <span className="text-base font-bold text-white">1,420 Completed</span>
              </div>
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <span className="text-[10px] text-[#5F6B78] block">Successful Changes</span>
                <span className="text-base font-bold text-emerald-400">128 Applied</span>
              </div>
              <div className="p-3 bg-[#1A2530] rounded-xl border border-[#26313D]">
                <span className="text-[10px] text-[#5F6B78] block">Active Improvement Plans</span>
                <span className="text-base font-bold text-cyan-400">3 In Progress</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
