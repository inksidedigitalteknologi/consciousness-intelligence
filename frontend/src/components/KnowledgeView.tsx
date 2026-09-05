// src/components/KnowledgeView.tsx
// INKSIDE DIGITAL - KNOWLEDGE VIEW v10.0
// FULL AI INTEGRATION - PERMANENT INTELLIGENCE MEMORY
// COMPREHENSIVE DISPLAY WITH AI ENHANCEMENT

import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  BookOpen,
  Search,
  Plus,
  Sparkles,
  Tag,
  Globe,
  FileCode,
  Check,
  Send,
  Loader2,
  AlertCircle,
  X,
  Trash2,
  Edit2,
  Download,
  Upload,
  Filter,
  Clock,
  Brain,
  Zap,
  Layers,
  BarChart3,
  Shield,
  Database,
  Cpu,
  Network,
  Hash,
  Calendar,
  User,
  Link,
  Star,
  TrendingUp,
  Info,
} from 'lucide-react';

// ============================================================
// TYPES (Extended with AI Fields)
// ============================================================

export interface KnowledgeItem {
  id: string;
  content: string;
  category: string;
  type: 'fact' | 'concept' | 'rule' | 'pattern' | 'insight' | 'reference' | 'qa' | 'strategy';
  confidence: number;
  importance: number;
  tags: string[];
  status: 'active' | 'archived' | 'pending' | 'learning';
  createdAt: string;
  updatedAt?: string;
  source?: string;
  metadata?: Record<string, any>;
  
  // AI Enhancement Fields
  ai_summary?: string;
  ai_insights?: string[];
  ai_tags?: string[];
  ai_enhanced: boolean;
  ai_enhanced_at?: string;
}

interface KnowledgeViewProps {
  knowledgeList: KnowledgeItem[];
  onAddKnowledge: (item: Partial<KnowledgeItem>) => void;
  onDeleteKnowledge?: (id: string) => void;
  onUpdateKnowledge?: (id: string, item: Partial<KnowledgeItem>) => void;
  onEnhanceWithAI?: (id: string) => void;
  onBatchEnhance?: () => void;
  isLoading?: boolean;
  aiStatus?: {
    available: boolean;
    enabled: boolean;
    enhanced_items: number;
    total_items: number;
    enhancement_percentage: number;
  };
  stats?: {
    total: number;
    active: number;
    archived: number;
    categories: Record<string, number>;
    avg_confidence: number;
    ai_enhanced_count: number;
  };
}

// ============================================================
// HELPER COMPONENTS
// ============================================================

const StatusBadge: React.FC<{ status: KnowledgeItem['status'] }> = ({ status }) => {
  const colors = {
    active: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
    archived: 'bg-gray-500/20 text-gray-400 border-gray-500/20',
    pending: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
    learning: 'bg-blue-500/20 text-blue-400 border-blue-500/20',
  };
  return (
    <span className={`text-[9px] font-bold px-2 py-0.5 rounded border ${colors[status]}`}>
      {status.toUpperCase()}
    </span>
  );
};

const ConfidenceBar: React.FC<{ value: number }> = ({ value }) => {
  const color = value >= 80 ? 'bg-emerald-500' : value >= 60 ? 'bg-amber-500' : 'bg-rose-500';
  return (
    <div className="flex items-center gap-2">
      <div className="w-16 h-1.5 rounded-full bg-[#26313D] overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
      <span className="text-[10px] font-mono text-[#8D9AAA]">{value}%</span>
    </div>
  );
};

const SkeletonItem: React.FC = () => (
  <div className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] animate-pulse">
    <div className="flex items-center justify-between">
      <div className="h-4 bg-[#26313D] rounded w-20"></div>
      <div className="h-3 bg-[#26313D] rounded w-12"></div>
    </div>
    <div className="mt-2 h-4 bg-[#26313D] rounded w-full"></div>
    <div className="mt-1 h-4 bg-[#26313D] rounded w-3/4"></div>
    <div className="mt-3 flex items-center justify-between">
      <div className="flex gap-1">
        <div className="h-3 bg-[#26313D] rounded w-12"></div>
        <div className="h-3 bg-[#26313D] rounded w-12"></div>
      </div>
      <div className="h-3 bg-[#26313D] rounded w-20"></div>
    </div>
  </div>
);

const AIBadge: React.FC<{ enhanced: boolean }> = ({ enhanced }) => {
  if (!enhanced) return null;
  return (
    <span className="flex items-center gap-1 text-[9px] font-bold px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/20">
      <Sparkles className="w-2.5 h-2.5" />
      AI
    </span>
  );
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export const KnowledgeView: React.FC<KnowledgeViewProps> = ({
  knowledgeList,
  onAddKnowledge,
  onDeleteKnowledge,
  onUpdateKnowledge,
  onEnhanceWithAI,
  onBatchEnhance,
  isLoading = false,
  aiStatus,
  stats,
}) => {
  // ===== STATE =====
  const [activeTab, setActiveTab] = useState<'text' | 'url' | 'raw' | 'ai'>('text');
  const [question, setQuestion] = useState('');
  const [qaAnswer, setQaAnswer] = useState<string | null>(null);
  const [qaSources, setQaSources] = useState<KnowledgeItem[]>([]);
  const [isAnswering, setIsAnswering] = useState(false);
  const [qaError, setQaError] = useState<string | null>(null);

  const [textContent, setTextContent] = useState('');
  const [urlContent, setUrlContent] = useState('');
  const [rawContent, setRawContent] = useState('');
  const [category, setCategory] = useState('Trading');
  const [searchFilter, setSearchFilter] = useState('');
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState('All');
  const [selectedTypeFilter, setSelectedTypeFilter] = useState('All');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState<string | null>(null);
  const [isEnhancing, setIsEnhancing] = useState(false);
  const [enhanceTargetId, setEnhanceTargetId] = useState<string | null>(null);

  // URL fetch state
  const [isFetchingUrl, setIsFetchingUrl] = useState(false);
  const [urlError, setUrlError] = useState<string | null>(null);

  // View mode
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // ===== REFS =====
  const searchTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const successTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // ===== CONSTANTS =====
  const categories = ['All', 'Trading', 'Strategy', 'Market', 'Finance', 'General Knowledge', 'QA', 'AI Generated'];
  const types = ['All', 'fact', 'concept', 'rule', 'pattern', 'insight', 'reference', 'qa', 'strategy'];
  const trendingTopics = ['bitcoin', 'halving', 'strategy', 'mtf-alignment', 'kraken', 'indonesia', 'bi-rate'];
  const smartSuggestions = [
    'What is the optimal RSI threshold for MTF momentum?',
    'Tell me about Bitcoin Halving cycles',
    'How does Kraken WebSocket stream work?',
    'Summarize recent macro economic insights',
  ];

  // ===== FILTERED KNOWLEDGE =====
  const filteredKnowledge = knowledgeList.filter((item) => {
    const matchesCat = selectedCategoryFilter === 'All' || item.category === selectedCategoryFilter;
    const matchesType = selectedTypeFilter === 'All' || item.type === selectedTypeFilter;
    const matchesSearch = item.content.toLowerCase().includes(searchFilter.toLowerCase());
    return matchesCat && matchesType && matchesSearch;
  });

  // ===== AI ENHANCED ITEMS =====
  const aiEnhancedItems = knowledgeList.filter((item) => item.ai_enhanced);
  const aiStats = {
    total: knowledgeList.length,
    enhanced: aiEnhancedItems.length,
    percentage: knowledgeList.length > 0 ? (aiEnhancedItems.length / knowledgeList.length * 100) : 0,
  };

  // ===== HANDLERS =====

  // ---- Q&A with AI ----
  const handleAsk = useCallback(async () => {
    if (!question.trim()) {
      setQaError('Please enter a question.');
      return;
    }

    setIsAnswering(true);
    setQaError(null);
    setQaAnswer(null);
    setQaSources([]);

    try {
      // 1. Search in local knowledge
      const keywords = question.toLowerCase().split(' ');
      let matches: { item: KnowledgeItem; score: number }[] = [];

      for (const item of knowledgeList) {
        let score = 0;
        const content = item.content.toLowerCase();
        const tags = item.tags.map(t => t.toLowerCase());
        
        for (const keyword of keywords) {
          if (content.includes(keyword)) score += 1;
          if (tags.some(t => t.includes(keyword))) score += 0.5;
        }
        
        // Boost AI-enhanced items
        if (item.ai_enhanced) score += 0.3;
        
        if (score > 0) {
          matches.push({ item, score });
        }
      }

      matches.sort((a, b) => b.score - a.score);
      const topMatches = matches.slice(0, 5);

      // 2. Try to call AI API
      try {
        const response = await fetch('/api/ai/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': localStorage.getItem('apiKey') || 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ',
          },
          body: JSON.stringify({ 
            question: question,
            context: topMatches.map(m => m.item.content).join('\n\n')
          }),
        });

        if (response.ok) {
          const data = await response.json();
          if (data.ai_enabled && data.answer) {
            setQaAnswer(data.answer);
            setQaSources(topMatches.map(m => m.item));
            setIsAnswering(false);
            return;
          }
        }
      } catch (apiError) {
        console.warn('AI API call failed, using local knowledge:', apiError);
      }

      // 3. Fallback: Use local knowledge
      if (topMatches.length > 0) {
        const bestMatch = topMatches[0];
        const answer = bestMatch.item.ai_summary || bestMatch.item.content;
        
        let response = `📚 **Best match from knowledge base** (confidence: ${bestMatch.score})\n\n${answer}`;
        
        if (topMatches.length > 1) {
          response += `\n\n📖 **Related entries:**\n`;
          topMatches.slice(1, 4).forEach((m, i) => {
            const preview = m.item.content.length > 80 
              ? m.item.content.substring(0, 80) + '...' 
              : m.item.content;
            response += `${i + 1}. ${preview}\n`;
          });
        }
        
        if (aiStats.enhanced > 0) {
          response += `\n\n🤖 **AI Enhanced Knowledge:** ${aiStats.enhanced} items available in database.`;
        }
        
        setQaAnswer(response);
        setQaSources(topMatches.map(m => m.item));
      } else {
        setQaAnswer(
          `🤔 I don't have specific knowledge about "${question}" yet. ` +
          `Try adding it to the knowledge base or enable AI enhancement for better answers!\n\n` +
          `💡 **Tip:** Click the "AI Enhance" button on any knowledge item to get AI-powered insights.`
        );
        setQaSources([]);
      }
    } catch (error) {
      setQaError('Failed to process your question. Please try again.');
      console.error('Q&A error:', error);
    } finally {
      setIsAnswering(false);
    }
  }, [question, knowledgeList, aiStats]);

  // ---- Save Text ----
  const handleSaveText = useCallback(() => {
    if (!textContent.trim()) {
      setSubmitError('Please enter some content to save.');
      return;
    }

    setIsSubmitting(true);
    setSubmitError(null);
    setSubmitSuccess(null);

    try {
      onAddKnowledge({
        content: textContent.trim(),
        category,
        type: 'fact',
        confidence: 85,
        importance: 0.8,
        tags: [category.toLowerCase(), 'user-added'],
        status: 'active',
        source: 'user_input',
        ai_enhanced: false,
      });

      setTextContent('');
      setSubmitSuccess('✅ Knowledge saved successfully!');

      if (successTimeoutRef.current) clearTimeout(successTimeoutRef.current);
      successTimeoutRef.current = setTimeout(() => {
        setSubmitSuccess(null);
      }, 3000);
    } catch (error) {
      setSubmitError('Failed to save knowledge. Please try again.');
      console.error('Save error:', error);
    } finally {
      setIsSubmitting(false);
    }
  }, [textContent, category, onAddKnowledge]);

  // ---- Fetch URL ----
  const handleFetchUrl = useCallback(async () => {
    if (!urlContent.trim()) {
      setUrlError('Please enter a valid URL.');
      return;
    }

    try {
      new URL(urlContent);
    } catch {
      setUrlError('Invalid URL format.');
      return;
    }

    setIsFetchingUrl(true);
    setUrlError(null);

    try {
      const response = await fetch(`/api/knowledge/fetch-url`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': localStorage.getItem('apiKey') || 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ',
        },
        body: JSON.stringify({ url: urlContent }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();

      onAddKnowledge({
        content: data.content || `Fetched content from ${urlContent}`,
        category: 'Market',
        type: 'reference',
        confidence: 80,
        importance: 0.7,
        tags: ['url-fetched', 'macro', ...(data.tags || [])],
        status: 'active',
        source: `url:${urlContent}`,
        metadata: { url: urlContent },
        ai_enhanced: false,
      });

      setUrlContent('');
      setSubmitSuccess('✅ URL content fetched and saved!');
    } catch (error) {
      console.warn('URL fetch failed:', error);
      onAddKnowledge({
        content: `[URL Reference] ${urlContent}`,
        category: 'Market',
        type: 'reference',
        confidence: 60,
        importance: 0.5,
        tags: ['url-reference'],
        status: 'pending',
        source: `url:${urlContent}`,
        metadata: { url: urlContent },
        ai_enhanced: false,
      });
      setUrlContent('');
      setSubmitSuccess('✅ URL saved as reference.');
    } finally {
      setIsFetchingUrl(false);
    }
  }, [urlContent, onAddKnowledge]);

  // ---- Save Raw ----
  const handleSaveRaw = useCallback(() => {
    if (!rawContent.trim()) {
      setSubmitError('Please paste some raw data.');
      return;
    }

    setIsSubmitting(true);
    setSubmitError(null);

    try {
      let parsed = rawContent.trim();
      let tags: string[] = ['raw-data'];

      try {
        const json = JSON.parse(rawContent);
        parsed = JSON.stringify(json, null, 2);
        tags.push('json');
      } catch {
        if (rawContent.includes(',')) tags.push('csv');
        else tags.push('text');
      }

      onAddKnowledge({
        content: parsed.length > 500 ? `${parsed.substring(0, 500)}... [truncated]` : parsed,
        category: 'Trading',
        type: 'fact',
        confidence: 90,
        importance: 0.8,
        tags: tags,
        status: 'active',
        source: 'raw_data_input',
        metadata: { original_length: rawContent.length },
        ai_enhanced: false,
      });

      setRawContent('');
      setSubmitSuccess('✅ Raw data parsed and saved!');
    } catch (error) {
      setSubmitError('Failed to parse raw data.');
      console.error('Raw parse error:', error);
    } finally {
      setIsSubmitting(false);
    }
  }, [rawContent, onAddKnowledge]);

  // ---- AI Enhance Single Item ----
  const handleEnhanceItem = useCallback((id: string) => {
    if (onEnhanceWithAI) {
      setEnhanceTargetId(id);
      onEnhanceWithAI(id);
      setTimeout(() => setEnhanceTargetId(null), 2000);
    }
  }, [onEnhanceWithAI]);

  // ---- AI Enhance All ----
  const handleEnhanceAll = useCallback(() => {
    if (onBatchEnhance && window.confirm('Enhance all knowledge items with AI? This may take a moment.')) {
      setIsEnhancing(true);
      onBatchEnhance();
      setTimeout(() => setIsEnhancing(false), 3000);
    }
  }, [onBatchEnhance]);

  // ---- Delete Knowledge ----
  const handleDelete = useCallback((id: string) => {
    if (window.confirm('Are you sure you want to delete this knowledge item?')) {
      onDeleteKnowledge?.(id);
    }
  }, [onDeleteKnowledge]);

  // ---- Search with Debounce ----
  const handleSearchChange = useCallback((value: string) => {
    setSearchFilter(value);
  }, []);

  // ===== CLEANUP =====
  useEffect(() => {
    return () => {
      if (searchTimeoutRef.current) clearTimeout(searchTimeoutRef.current);
      if (successTimeoutRef.current) clearTimeout(successTimeoutRef.current);
    };
  }, []);

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div id="knowledge-view" className="space-y-6 pb-12">
      
      {/* ===== TOP BANNER with AI Stats ===== */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] to-[#1A2530] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-teal-600/20 border border-teal-500/30 flex items-center justify-center text-teal-400">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Knowledge Base & AI Memory v10.0
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              {aiStats.enhanced > 0 
                ? `🧠 ${aiStats.enhanced} items AI-enhanced · ${aiStats.percentage.toFixed(0)}% of knowledge`
                : '💡 AI Enhancement ready - Add knowledge to get started'}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
            <span className="text-[10px] text-[#5F6B78] font-bold block">AI Status</span>
            <span className={`text-sm font-black font-mono ${aiStatus?.enabled ? 'text-emerald-400' : 'text-amber-400'}`}>
              {aiStatus?.enabled ? '🟢 ENABLED' : '🟡 DISABLED'}
            </span>
          </div>
          <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
            <span className="text-[10px] text-[#5F6B78] font-bold block">Total Items</span>
            <span className="text-sm font-black text-white font-mono">{knowledgeList.length}</span>
          </div>
          {aiStatus && (
            <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
              <span className="text-[10px] text-[#5F6B78] font-bold block">AI Enhanced</span>
              <span className="text-sm font-black text-purple-400 font-mono">{aiStatus.enhanced_items}</span>
            </div>
          )}
        </div>
      </div>

      {/* ===== SUCCESS / ERROR MESSAGES ===== */}
      {submitSuccess && (
        <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center gap-2 text-emerald-400 text-xs">
          <Check className="w-4 h-4" />
          <span>{submitSuccess}</span>
          <button
            onClick={() => setSubmitSuccess(null)}
            className="ml-auto text-emerald-400/70 hover:text-emerald-400"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {submitError && (
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center gap-2 text-rose-400 text-xs">
          <AlertCircle className="w-4 h-4" />
          <span>{submitError}</span>
          <button
            onClick={() => setSubmitError(null)}
            className="ml-auto text-rose-400/70 hover:text-rose-400"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* ===== ASK Q&A SECTION with AI ===== */}
      <div className="p-5 rounded-2xl bg-[#1A2530] border border-[#26313D] space-y-3 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-teal-400" />
            <h3 className="text-sm font-bold text-white tracking-wider uppercase">
              Ask AI Knowledge Base
            </h3>
            {aiStatus?.enabled && (
              <span className="text-[8px] font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/20">
                AI POWERED
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[9px] text-[#5F6B78]">
              {aiStats.enhanced > 0 ? `${aiStats.enhanced} AI-enhanced items` : 'No AI enhancements yet'}
            </span>
          </div>
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Ask anything about your knowledge base..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
            className="flex-1 px-4 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-teal-500"
            disabled={isAnswering}
          />
          <button
            onClick={handleAsk}
            disabled={isAnswering || !question.trim()}
            className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition-all shadow-md shadow-teal-600/30 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnswering ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Send className="w-3.5 h-3.5" />
            )}
            <span>{isAnswering ? 'Searching...' : 'Ask'}</span>
          </button>
        </div>

        {qaError && (
          <div className="p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs">
            {qaError}
          </div>
        )}

        {qaAnswer && (
          <div className="p-3.5 rounded-xl bg-[#0B0F14] border border-teal-500/30 text-xs text-teal-200 leading-relaxed font-sans whitespace-pre-line">
            <div className="flex items-center gap-2 mb-1">
              <Sparkles className="w-3 h-3 text-teal-400" />
              <strong className="text-teal-400">AI Answer</strong>
              {qaSources.length > 0 && (
                <span className="text-[9px] text-[#5F6B78]">
                  ({qaSources.length} sources)
                </span>
              )}
            </div>
            {qaAnswer}
            {qaSources.length > 0 && (
              <div className="mt-2 pt-2 border-t border-[#26313D]">
                <span className="text-[9px] text-[#5F6B78]">📚 Sources:</span>
                {qaSources.slice(0, 3).map((src) => (
                  <div key={src.id} className="text-[9px] text-[#8D9AAA] truncate">
                    • {src.content.substring(0, 60)}...
                    {src.ai_enhanced && ' ✨'}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Smart Suggestions */}
        <div className="pt-2 flex flex-wrap items-center gap-2">
          <span className="text-[10px] text-[#5F6B78] font-bold">Suggestions:</span>
          {smartSuggestions.map((sug, i) => (
            <button
              key={i}
              onClick={() => {
                setQuestion(sug);
                setQaAnswer(null);
                setQaError(null);
                setQaSources([]);
              }}
              className="text-[10px] px-2 py-1 rounded-md bg-[#0B0F14] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors"
            >
              {sug}
            </button>
          ))}
        </div>
      </div>

      {/* ===== ADD KNOWLEDGE BOX ===== */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70 flex-wrap gap-2">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Plus className="w-4 h-4 text-emerald-400" />
            Add Knowledge
          </h3>

          <div className="flex items-center gap-2 flex-wrap">
            {(['text', 'url', 'raw', 'ai'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-colors ${
                  activeTab === tab 
                    ? tab === 'ai' ? 'bg-purple-600 text-white' : 'bg-blue-600 text-white'
                    : 'text-[#8D9AAA] hover:text-white bg-[#0B0F14]'
                }`}
              >
                {tab === 'text' && '📝 Text'}
                {tab === 'url' && '🌐 URL'}
                {tab === 'raw' && '📊 Raw'}
                {tab === 'ai' && '🤖 AI Generate'}
              </button>
            ))}
          </div>
        </div>

        {/* Tab: Text */}
        {activeTab === 'text' && (
          <div className="space-y-3">
            <textarea
              rows={3}
              placeholder="Type or paste knowledge text here..."
              value={textContent}
              onChange={(e) => setTextContent(e.target.value)}
              className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-blue-500"
              disabled={isSubmitting}
            />
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div className="flex items-center gap-2">
                <span className="text-xs text-[#8D9AAA]">Category:</span>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="px-2.5 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white font-semibold"
                >
                  {categories.filter((c) => c !== 'All').map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
                <button
                  onClick={() => {
                    if (textContent.trim()) {
                      const tags = textContent.toLowerCase().split(' ').slice(0, 5);
                      const suggestedCategory = tags.find(t => 
                        ['trading', 'market', 'finance', 'strategy', 'bitcoin', 'crypto'].includes(t)
                      ) || 'Trading';
                      setCategory(suggestedCategory.charAt(0).toUpperCase() + suggestedCategory.slice(1));
                    }
                  }}
                  className="text-[10px] px-2 py-1 rounded bg-[#26313D] hover:bg-[#3A4A5A] text-[#8D9AAA] transition-colors"
                >
                  Suggest
                </button>
              </div>
              <button
                onClick={handleSaveText}
                disabled={isSubmitting || !textContent.trim()}
                className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-md flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Check className="w-3.5 h-3.5" />}
                <span>{isSubmitting ? 'Saving...' : 'Save Knowledge'}</span>
              </button>
            </div>
          </div>
        )}

        {/* Tab: URL */}
        {activeTab === 'url' && (
          <div className="space-y-3">
            <div className="flex gap-2">
              <input
                type="url"
                placeholder="https://example.com/article..."
                value={urlContent}
                onChange={(e) => setUrlContent(e.target.value)}
                className="flex-1 px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-purple-500"
                disabled={isFetchingUrl}
              />
              <button
                onClick={handleFetchUrl}
                disabled={isFetchingUrl || !urlContent.trim()}
                className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isFetchingUrl ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Globe className="w-3.5 h-3.5" />}
                <span>{isFetchingUrl ? 'Fetching...' : 'Fetch'}</span>
              </button>
            </div>
            {urlError && (
              <div className="text-rose-400 text-[11px] bg-rose-500/10 p-2 rounded-lg border border-rose-500/20">
                {urlError}
              </div>
            )}
          </div>
        )}

        {/* Tab: Raw */}
        {activeTab === 'raw' && (
          <div className="space-y-3">
            <textarea
              rows={3}
              placeholder="Paste raw JSON or CSV data..."
              value={rawContent}
              onChange={(e) => setRawContent(e.target.value)}
              className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-amber-500"
              disabled={isSubmitting}
            />
            <button
              onClick={handleSaveRaw}
              disabled={isSubmitting || !rawContent.trim()}
              className="px-4 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <FileCode className="w-3.5 h-3.5" />}
              <span>{isSubmitting ? 'Parsing...' : 'Parse & Ingest'}</span>
            </button>
          </div>
        )}

        {/* Tab: AI Generate */}
        {activeTab === 'ai' && (
          <div className="space-y-3">
            <div className="p-3 rounded-xl bg-[#0B0F14] border border-purple-500/20">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-4 h-4 text-purple-400" />
                <span className="text-xs font-bold text-white">AI Content Generator</span>
                {!aiStatus?.enabled && (
                  <span className="text-[8px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/20">
                    AI DISABLED
                  </span>
                )}
              </div>
              <p className="text-[10px] text-[#8D9AAA] mb-3">
                Generate knowledge using AI. Enter a topic and AI will create structured knowledge from it.
              </p>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Enter a topic (e.g., 'Bitcoin halving')..."
                  className="flex-1 px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-purple-500"
                  disabled={!aiStatus?.enabled}
                />
                <button
                  disabled={!aiStatus?.enabled}
                  className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Brain className="w-3.5 h-3.5" />
                  <span>Generate</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ===== AI ENHANCE CONTROLS ===== */}
      <div className="p-4 rounded-xl bg-gradient-to-r from-[#1A2530] to-[#131A22] border border-[#26313D] flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Brain className="w-4 h-4 text-purple-400" />
          <span className="text-xs font-bold text-white">AI Enhancement</span>
          <span className="text-[10px] text-[#8D9AAA]">
            {aiStats.enhanced} / {aiStats.total} items enhanced
          </span>
          {aiStats.total > 0 && (
            <div className="w-16 h-1.5 rounded-full bg-[#26313D] overflow-hidden">
              <div 
                className="h-full rounded-full bg-purple-500" 
                style={{ width: `${aiStats.percentage}%` }} 
              />
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleEnhanceAll}
            disabled={isEnhancing || knowledgeList.length === 0 || !aiStatus?.enabled}
            className="px-4 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isEnhancing ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Zap className="w-3.5 h-3.5" />
            )}
            <span>{isEnhancing ? 'Enhancing...' : 'Enhance All with AI'}</span>
          </button>
        </div>
      </div>

      {/* ===== TRENDING TOPICS ===== */}
      <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D] flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-1.5 text-xs font-bold text-white">
          <Tag className="w-3.5 h-3.5 text-amber-400" />
          <span>Trending Topics:</span>
        </div>
        <div className="flex flex-wrap items-center gap-1.5">
          {trendingTopics.map((t) => (
            <button
              key={t}
              onClick={() => setSearchFilter(t)}
              className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-[#0B0F14] hover:bg-blue-600 text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors"
            >
              #{t}
            </button>
          ))}
        </div>
      </div>

      {/* ===== KNOWLEDGE ITEMS GRID ===== */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#26313D]/70">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Filter className="w-4 h-4 text-teal-400" />
            Stored Knowledge ({filteredKnowledge.length})
          </h3>

          <div className="flex items-center gap-2 flex-wrap">
            <select
              value={selectedCategoryFilter}
              onChange={(e) => setSelectedCategoryFilter(e.target.value)}
              className="px-2.5 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white font-semibold"
            >
              {categories.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>

            <select
              value={selectedTypeFilter}
              onChange={(e) => setSelectedTypeFilter(e.target.value)}
              className="px-2.5 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white font-semibold"
            >
              {types.map((t) => (
                <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
              ))}
            </select>

            <input
              type="text"
              placeholder="Filter items..."
              value={searchFilter}
              onChange={(e) => handleSearchChange(e.target.value)}
              className="px-3 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-teal-500 w-32 sm:w-40"
            />

            <button
              onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
              className="px-2 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-[#8D9AAA] hover:text-white transition-colors"
            >
              {viewMode === 'grid' ? '⊞' : '≡'}
            </button>
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            {[1, 2, 3, 4].map((i) => (
              <SkeletonItem key={i} />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!isLoading && filteredKnowledge.length === 0 && (
          <div className="text-center py-12">
            <BookOpen className="w-12 h-12 text-[#26313D] mx-auto mb-3" />
            <p className="text-[#8D9AAA] text-sm">
              {searchFilter || selectedCategoryFilter !== 'All' || selectedTypeFilter !== 'All'
                ? 'No knowledge items match your filters.'
                : 'No knowledge items yet. Add your first piece of knowledge above!'}
            </p>
            {!aiStatus?.enabled && (
              <p className="text-[11px] text-[#5F6B78] mt-2">
                💡 Enable AI (set DEEPSEEK_API_KEY) to automatically enhance your knowledge.
              </p>
            )}
          </div>
        )}

        {/* Knowledge Items */}
        {!isLoading && filteredKnowledge.length > 0 && (
          <div className={viewMode === 'grid' 
            ? 'grid grid-cols-1 md:grid-cols-2 gap-3.5' 
            : 'space-y-2'
          }>
            {filteredKnowledge.map((item) => (
              <div
                key={item.id}
                className={`p-4 rounded-xl bg-[#1A2530] border border-[#26313D] flex flex-col justify-between space-y-3 hover:border-teal-500/40 transition-all duration-300 group ${
                  item.ai_enhanced ? 'border-purple-500/20' : ''
                }`}
              >
                <div>
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 border border-teal-500/20">
                        {item.category.toUpperCase()}
                      </span>
                      <StatusBadge status={item.status} />
                      <AIBadge enhanced={item.ai_enhanced} />
                    </div>
                    <div className="flex items-center gap-2">
                      <ConfidenceBar value={item.confidence} />
                      {onDeleteKnowledge && (
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="opacity-0 group-hover:opacity-100 transition-opacity text-rose-400 hover:text-rose-300"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </div>
                  </div>
                  
                  <p className="text-xs text-[#E8EDF2] leading-relaxed mt-2">
                    {item.content}
                  </p>
                  
                  {/* AI Summary - if available */}
                  {item.ai_summary && (
                    <div className="mt-2 p-2 rounded-lg bg-purple-500/5 border border-purple-500/10">
                      <div className="flex items-center gap-1">
                        <Sparkles className="w-3 h-3 text-purple-400" />
                        <span className="text-[9px] text-purple-400 font-bold">AI Summary</span>
                      </div>
                      <p className="text-[10px] text-[#8D9AAA] leading-relaxed">
                        {item.ai_summary}
                      </p>
                    </div>
                  )}
                  
                  {/* AI Insights */}
                  {item.ai_insights && item.ai_insights.length > 0 && (
                    <div className="mt-1 flex flex-wrap gap-1">
                      {item.ai_insights.slice(0, 2).map((insight, i) => (
                        <span key={i} className="text-[9px] px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400">
                          💡 {insight}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-[#26313D]/60 text-[10px] text-[#5F6B78] font-mono flex-wrap gap-1">
                  <div className="flex items-center gap-1 flex-wrap">
                    {item.ai_tags && item.ai_tags.length > 0 ? (
                      item.ai_tags.slice(0, 3).map((tg) => (
                        <span key={tg} className="text-purple-400/70">#{tg}</span>
                      ))
                    ) : (
                      item.tags.slice(0, 3).map((tg) => (
                        <span key={tg} className="text-[#8D9AAA]">#{tg}</span>
                      ))
                    )}
                    {(item.ai_tags?.length || 0) > 3 && (
                      <span className="text-[#5F6B78]">+{(item.ai_tags?.length || 0) - 3}</span>
                    )}
                  </div>
                  <div className="flex items-center gap-3">
                    {onEnhanceWithAI && !item.ai_enhanced && aiStatus?.enabled && (
                      <button
                        onClick={() => handleEnhanceItem(item.id)}
                        disabled={enhanceTargetId === item.id}
                        className="text-[9px] text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-1"
                      >
                        {enhanceTargetId === item.id ? (
                          <Loader2 className="w-3 h-3 animate-spin" />
                        ) : (
                          <Sparkles className="w-3 h-3" />
                        )}
                        AI
                      </button>
                    )}
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      <span>{item.createdAt}</span>
                    </div>
                    {item.source && (
                      <span className="text-[#5F6B78]">📎 {item.source}</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default KnowledgeView;
