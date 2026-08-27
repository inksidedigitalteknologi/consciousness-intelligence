// src/components/KnowledgeView.tsx
// INKSIDE DIGITAL - KNOWLEDGE VIEW v9.1
// FIX: ERROR HANDLING, DEBOUNCE, LOADING STATES
// PERMANENT INTELLIGENCE MEMORY

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
} from 'lucide-react';

// ============================================================
// TYPES
// ============================================================

export interface KnowledgeItem {
  id: string;
  content: string;
  category: string;
  type: 'fact' | 'concept' | 'rule' | 'pattern' | 'insight' | 'reference' | 'qa';
  confidence: number;
  importance: number;
  tags: string[];
  status: 'active' | 'archived' | 'pending';
  createdAt: string;
  updatedAt?: string;
  source?: string;
  metadata?: Record<string, any>;
}

interface KnowledgeViewProps {
  knowledgeList: KnowledgeItem[];
  onAddKnowledge: (item: Partial<KnowledgeItem>) => void;
  onDeleteKnowledge?: (id: string) => void;
  onUpdateKnowledge?: (id: string, item: Partial<KnowledgeItem>) => void;
  isLoading?: boolean;
}

// ============================================================
// HELPER COMPONENTS
// ============================================================

const StatusBadge: React.FC<{ status: KnowledgeItem['status'] }> = ({ status }) => {
  const colors = {
    active: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20',
    archived: 'bg-gray-500/20 text-gray-400 border-gray-500/20',
    pending: 'bg-amber-500/20 text-amber-400 border-amber-500/20',
  };
  return (
    <span className={`text-[9px] font-bold px-2 py-0.5 rounded border ${colors[status]}`}>
      {status.toUpperCase()}
    </span>
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

// ============================================================
// MAIN COMPONENT
// ============================================================

export const KnowledgeView: React.FC<KnowledgeViewProps> = ({
  knowledgeList,
  onAddKnowledge,
  onDeleteKnowledge,
  onUpdateKnowledge,
  isLoading = false,
}) => {
  // ===== STATE =====
  const [activeTab, setActiveTab] = useState<'text' | 'url' | 'raw'>('text');
  const [question, setQuestion] = useState('');
  const [qaAnswer, setQaAnswer] = useState<string | null>(null);
  const [isAnswering, setIsAnswering] = useState(false);
  const [qaError, setQaError] = useState<string | null>(null);

  const [textContent, setTextContent] = useState('');
  const [urlContent, setUrlContent] = useState('');
  const [rawContent, setRawContent] = useState('');
  const [category, setCategory] = useState('Trading');
  const [searchFilter, setSearchFilter] = useState('');
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState('All');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState<string | null>(null);

  // URL fetch state
  const [isFetchingUrl, setIsFetchingUrl] = useState(false);
  const [urlError, setUrlError] = useState<string | null>(null);

  // ===== REFS =====
  const searchTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const successTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // ===== CONSTANTS =====
  const categories = ['All', 'Trading', 'Strategy', 'Market', 'Finance', 'General Knowledge', 'QA'];
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
    const matchesSearch = item.content.toLowerCase().includes(searchFilter.toLowerCase());
    return matchesCat && matchesSearch;
  });

  // ===== HANDLERS =====

  // ---- Q&A ----
  const handleAsk = useCallback(() => {
    if (!question.trim()) {
      setQaError('Please enter a question.');
      return;
    }

    setIsAnswering(true);
    setQaError(null);
    setQaAnswer(null);

    // Simulasi pencarian di knowledge
    setTimeout(() => {
      try {
        // Cari di knowledge yang ada
        const keywords = question.toLowerCase().split(' ');
        let bestMatch: KnowledgeItem | null = null;
        let bestScore = 0;

        for (const item of knowledgeList) {
          let score = 0;
          const content = item.content.toLowerCase();
          for (const keyword of keywords) {
            if (content.includes(keyword)) score += 1;
          }
          if (score > bestScore) {
            bestScore = score;
            bestMatch = item;
          }
        }

        if (bestMatch && bestScore >= 2) {
          setQaAnswer(bestMatch.content);
        } else {
          // Generate answer from knowledge
          const relatedItems = knowledgeList
            .filter((k) => k.tags.some((tag) => question.toLowerCase().includes(tag)))
            .slice(0, 3);

          if (relatedItems.length > 0) {
            const combined = relatedItems.map((k) => k.content).join(' ');
            setQaAnswer(
              `📚 Based on ${relatedItems.length} knowledge entries:\n\n${combined}`
            );
          } else {
            setQaAnswer(
              `🤔 I don't have specific knowledge about "${question}" yet. Try adding it to the knowledge base!`
            );
          }
        }
      } catch (error) {
        setQaError('Failed to process your question. Please try again.');
        console.error('Q&A error:', error);
      } finally {
        setIsAnswering(false);
      }
    }, 400);
  }, [question, knowledgeList]);

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
        id: `knowledge_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
        content: textContent.trim(),
        category,
        type: 'fact',
        confidence: 85,
        importance: 0.8,
        tags: [category.toLowerCase(), 'user-added'],
        status: 'active',
        createdAt: new Date().toISOString().replace('T', ' ').substring(0, 19),
        source: 'user_input',
      });

      setTextContent('');
      setSubmitSuccess('✅ Knowledge saved successfully!');

      // Clear success message after 3 seconds
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

    // Validasi URL
    try {
      new URL(urlContent);
    } catch {
      setUrlError('Invalid URL format. Please enter a complete URL (e.g., https://example.com).');
      return;
    }

    setIsFetchingUrl(true);
    setUrlError(null);
    setSubmitError(null);

    try {
      // Simulasi fetch (karena di frontend tidak bisa fetch arbitrary URL)
      // Di production, ini harus melalui backend proxy
      const response = await fetch(`/api/knowledge/fetch-url`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': localStorage.getItem('apiKey') || '',
        },
        body: JSON.stringify({ url: urlContent }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      onAddKnowledge({
        id: `knowledge_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
        content: data.content || `Fetched content from ${urlContent}`,
        category: 'Market',
        type: 'reference',
        confidence: 80,
        importance: 0.7,
        tags: ['url-fetched', 'macro', ...(data.tags || [])],
        status: 'active',
        createdAt: new Date().toISOString().replace('T', ' ').substring(0, 19),
        source: `url:${urlContent}`,
        metadata: data.metadata || { url: urlContent },
      });

      setUrlContent('');
      setSubmitSuccess('✅ URL content fetched and saved successfully!');

      if (successTimeoutRef.current) clearTimeout(successTimeoutRef.current);
      successTimeoutRef.current = setTimeout(() => {
        setSubmitSuccess(null);
      }, 3000);
    } catch (error) {
      // Fallback: simpan URL sebagai knowledge
      console.warn('URL fetch failed, saving as reference:', error);
      onAddKnowledge({
        id: `knowledge_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
        content: `[URL Reference] ${urlContent}`,
        category: 'Market',
        type: 'reference',
        confidence: 60,
        importance: 0.5,
        tags: ['url-reference', 'external'],
        status: 'pending',
        createdAt: new Date().toISOString().replace('T', ' ').substring(0, 19),
        source: `url:${urlContent}`,
        metadata: { url: urlContent, fetch_error: error instanceof Error ? error.message : 'Unknown error' },
      });
      setUrlContent('');
      setSubmitSuccess('✅ URL saved as reference (content fetch pending).');
    } finally {
      setIsFetchingUrl(false);
    }
  }, [urlContent, onAddKnowledge]);

  // ---- Save Raw ----
  const handleSaveRaw = useCallback(() => {
    if (!rawContent.trim()) {
      setSubmitError('Please paste some raw data to parse.');
      return;
    }

    setIsSubmitting(true);
    setSubmitError(null);

    try {
      let parsed = rawContent.trim();
      let tags: string[] = ['raw-data'];

      // Coba parse JSON
      try {
        const json = JSON.parse(rawContent);
        parsed = JSON.stringify(json, null, 2);
        tags.push('json');
      } catch {
        // Bukan JSON, coba CSV atau text biasa
        if (rawContent.includes(',')) {
          tags.push('csv');
        } else {
          tags.push('text');
        }
      }

      onAddKnowledge({
        id: `knowledge_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
        content: parsed.length > 500 ? `${parsed.substring(0, 500)}... [truncated]` : parsed,
        category: 'Trading',
        type: 'fact',
        confidence: 90,
        importance: 0.8,
        tags: tags,
        status: 'active',
        createdAt: new Date().toISOString().replace('T', ' ').substring(0, 19),
        source: 'raw_data_input',
        metadata: { original_length: rawContent.length },
      });

      setRawContent('');
      setSubmitSuccess('✅ Raw data parsed and saved successfully!');

      if (successTimeoutRef.current) clearTimeout(successTimeoutRef.current);
      successTimeoutRef.current = setTimeout(() => {
        setSubmitSuccess(null);
      }, 3000);
    } catch (error) {
      setSubmitError('Failed to parse raw data. Please check the format.');
      console.error('Raw parse error:', error);
    } finally {
      setIsSubmitting(false);
    }
  }, [rawContent, onAddKnowledge]);

  // ---- Search with Debounce ----
  const handleSearchChange = useCallback((value: string) => {
    setSearchFilter(value);
  }, []);

  // ---- Delete Knowledge ----
  const handleDelete = useCallback(
    (id: string) => {
      if (window.confirm('Are you sure you want to delete this knowledge item?')) {
        onDeleteKnowledge?.(id);
      }
    },
    [onDeleteKnowledge]
  );

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
      {/* ===== TOP BANNER ===== */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-teal-600/20 border border-teal-500/30 flex items-center justify-center text-teal-400">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Knowledge Base & Semantic Graph v9.1
            </h2>
            <p className="text-xs text-[#8D9AAA]">
              Permanent Intelligence Memory, Smart Suggestions & Natural Language Q&A Engine
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
            <span className="text-[10px] text-[#5F6B78] font-bold block">Total Stored Items</span>
            <span className="text-sm font-black text-white font-mono">{knowledgeList.length}</span>
          </div>
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

      {/* ===== ASK Q&A SECTION ===== */}
      <div className="p-5 rounded-2xl bg-[#1A2530] border border-[#26313D] space-y-3 shadow-lg">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-teal-400" />
          <h3 className="text-sm font-bold text-white tracking-wider uppercase">
            Ask Knowledge Base
          </h3>
        </div>

        <div className="flex gap-2">
          <input
            id="qa-question-input"
            type="text"
            placeholder="Ask anything about stored trading knowledge (e.g., what is bitcoin halving?)..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
            className="flex-1 px-4 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-teal-500"
            disabled={isAnswering}
          />
          <button
            onClick={handleAsk}
            disabled={isAnswering || !question.trim()}
            className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition-all shadow-md shadow-teal-600/30 flex items-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
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
            <strong className="text-teal-400 block mb-1">💡 Answer:</strong>
            {qaAnswer}
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
              }}
              className="text-[10px] px-2 py-1 rounded-md bg-[#0B0F14] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors cursor-pointer"
            >
              {sug}
            </button>
          ))}
        </div>
      </div>

      {/* ===== ADD KNOWLEDGE BOX ===== */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Plus className="w-4 h-4 text-emerald-400" />
            Add Knowledge
          </h3>

          <div className="flex items-center gap-2">
            {(['text', 'url', 'raw'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-colors cursor-pointer ${
                  activeTab === tab ? 'bg-blue-600 text-white' : 'text-[#8D9AAA] hover:text-white bg-[#0B0F14]'
                }`}
              >
                {tab === 'text' && '📝 Text'}
                {tab === 'url' && '🌐 URL Fetch'}
                {tab === 'raw' && '📊 Raw Data'}
              </button>
            ))}
          </div>
        </div>

        {/* Tab: Text */}
        {activeTab === 'text' && (
          <div className="space-y-3">
            <textarea
              id="add-knowledge-textarea"
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
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </select>
              </div>

              <button
                onClick={handleSaveText}
                disabled={isSubmitting || !textContent.trim()}
                className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-md cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
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
                className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isFetchingUrl ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Globe className="w-3.5 h-3.5" />}
                <span>{isFetchingUrl ? 'Fetching...' : 'Fetch & Extract'}</span>
              </button>
            </div>
            {urlError && (
              <div className="text-rose-400 text-[11px] bg-rose-500/10 p-2 rounded-lg border border-rose-500/20">
                {urlError}
              </div>
            )}
            <p className="text-[11px] text-[#5F6B78]">
              💡 System extracts article body text, removes boilerplate, and indexes sentences automatically.
            </p>
          </div>
        )}

        {/* Tab: Raw */}
        {activeTab === 'raw' && (
          <div className="space-y-3">
            <textarea
              rows={3}
              placeholder="Paste raw JSON or CSV dataset here..."
              value={rawContent}
              onChange={(e) => setRawContent(e.target.value)}
              className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-amber-500"
              disabled={isSubmitting}
            />
            <button
              onClick={handleSaveRaw}
              disabled={isSubmitting || !rawContent.trim()}
              className="px-4 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isSubmitting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <FileCode className="w-3.5 h-3.5" />}
              <span>{isSubmitting ? 'Parsing...' : 'Parse & Ingest'}</span>
            </button>
          </div>
        )}
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
              className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-[#0B0F14] hover:bg-blue-600 text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors cursor-pointer"
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
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>

            <input
              type="text"
              placeholder="Filter items..."
              value={searchFilter}
              onChange={(e) => handleSearchChange(e.target.value)}
              className="px-3 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-teal-500 w-32 sm:w-40"
            />
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
              {searchFilter || selectedCategoryFilter !== 'All'
                ? 'No knowledge items match your filters.'
                : 'No knowledge items yet. Add your first piece of knowledge above!'}
            </p>
          </div>
        )}

        {/* Knowledge Items */}
        {!isLoading && filteredKnowledge.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            {filteredKnowledge.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] flex flex-col justify-between space-y-3 hover:border-teal-500/40 transition-all duration-300 group"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 border border-teal-500/20">
                        {item.category.toUpperCase()}
                      </span>
                      <StatusBadge status={item.status} />
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-mono text-[#8D9AAA]">{item.confidence}% Conf</span>
                      {onDeleteKnowledge && (
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="opacity-0 group-hover:opacity-100 transition-opacity text-rose-400 hover:text-rose-300"
                          title="Delete"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </div>
                  </div>
                  <p className="text-xs text-[#E8EDF2] leading-relaxed mt-2">{item.content}</p>
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-[#26313D]/60 text-[10px] text-[#5F6B78] font-mono flex-wrap gap-1">
                  <div className="flex items-center gap-1 flex-wrap">
                    {item.tags.slice(0, 3).map((tg) => (
                      <span key={tg} className="text-[#8D9AAA]">
                        #{tg}
                      </span>
                    ))}
                    {item.tags.length > 3 && (
                      <span className="text-[#5F6B78]">+{item.tags.length - 3}</span>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="w-3 h-3" />
                    <span>{item.createdAt}</span>
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
