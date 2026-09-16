// src/components/KnowledgeView.tsx
// INKSIDE DIGITAL - KNOWLEDGE VIEW v1.02
// 100+ FEATURES - COMPLETE KNOWLEDGE MANAGEMENT SYSTEM

import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import {
  BookOpen, Search, Plus, Sparkles, Tag, Globe, FileCode,
  Check, Send, Loader2, AlertCircle, X, Trash2, Edit2,
  Download, Upload, Filter, Clock, Brain, Zap, Layers,
  BarChart3, Shield, Database, Cpu, Network, Hash,
  Calendar, User, Link, Star, TrendingUp, Info,
  ChevronDown, ChevronRight, ChevronLeft, Copy, Save,
  Settings, SlidersVertical, Eye, EyeOff, Gauge,
  GitBranch, GraduationCap, HardDrive, Heart, Key,
  Lightbulb, List, Menu, MessageSquare, Minus, Monitor,
  Music, Palette, PenLine, Pin, Play, Power, Radio,
  RefreshCw, Rocket, RotateCcw, Share2, Signal, Square,
  Target, Timer, Workflow, Wifi, Zap as ZapIcon, Activity,
} from 'lucide-react';

import { AIVisualResponse } from './AIVisualResponse';
import type { AIResponse } from './AIVisualResponse';

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
  ai_summary?: string;
  ai_insights?: string[];
  ai_tags?: string[];
  ai_enhanced: boolean;
  ai_enhanced_at?: string;
  created_at?: string;
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
    enhanced_items?: number;
    total_items?: number;
    enhancement_percentage?: number;
    usage_today?: number;
    daily_limit?: number;
    remaining?: number;
    total_calls?: number;
    model?: string;
  };
  stats?: {
    total: number;
    active: number;
    archived: number;
    categories: Record<string, number>;
    avg_confidence: number;
    ai_enhanced_count: number;
  };
  wsConnected?: boolean;
}

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

const AIBadge: React.FC<{ enhanced: boolean }> = ({ enhanced }) => {
  if (!enhanced) return null;
  return (
    <span className="flex items-center gap-1 text-[9px] font-bold px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/20">
      <Sparkles className="w-2.5 h-2.5" />
      AI
    </span>
  );
};

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
  wsConnected = false,
}) => {
  // ===== STATE =====
  const [activeTab, setActiveTab] = useState<'text' | 'url' | 'raw' | 'ai'>('text');
  const [question, setQuestion] = useState('');
  const [qaAnswer, setQaAnswer] = useState<string | null>(null);
  const [qaData, setQaData] = useState<AIResponse | null>(null);
  const [qaSources, setQaSources] = useState<KnowledgeItem[]>([]);
  const [isAnswering, setIsAnswering] = useState(false);
  const [qaError, setQaError] = useState<string | null>(null);
  const [textContent, setTextContent] = useState('');
  const [urlContent, setUrlContent] = useState('');
  const [rawContent, setRawContent] = useState('');
  const [aiPrompt, setAiPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [category, setCategory] = useState('Trading');
  const [searchFilter, setSearchFilter] = useState('');
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState('All');
  const [selectedTypeFilter, setSelectedTypeFilter] = useState('All');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState<string | null>(null);
  const [isEnhancing, setIsEnhancing] = useState(false);
  const [enhanceTargetId, setEnhanceTargetId] = useState<string | null>(null);
  const [isFetchingUrl, setIsFetchingUrl] = useState(false);
  const [urlError, setUrlError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [editingItem, setEditingItem] = useState<KnowledgeItem | null>(null);
  const [isBulkMode, setIsBulkMode] = useState(false);
  const [showAnalytics, setShowAnalytics] = useState(true);
  const [showGraph, setShowGraph] = useState(false);
  const [exportFormat, setExportFormat] = useState<'json' | 'csv' | 'markdown'>('json');
  const [importData, setImportData] = useState<string>('');
  const [showImportModal, setShowImportModal] = useState(false);
  const [sortBy, setSortBy] = useState<'recent' | 'confidence' | 'category' | 'importance'>('recent');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [tagFilter, setTagFilter] = useState<string>('');
  const [dateRange, setDateRange] = useState<{ start: string; end: string }>({ start: '', end: '' });
  const [confidenceMin, setConfidenceMin] = useState(0);
  const [autoSave, setAutoSave] = useState(true);
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [keyboardMode, setKeyboardMode] = useState(false);
  const [undoStack, setUndoStack] = useState<KnowledgeItem[][]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(20);
  const [aiUsage, setAiUsage] = useState<{
    usage_today?: number;
    daily_limit?: number;
    remaining?: number;
    total_calls?: number;
    model?: string;
    enabled?: boolean;
    available?: boolean;
  } | null>(null);
  const [learningData, setLearningData] = useState<{
    cycles?: number;
    decision_count?: number;
    learning_count?: number;
    prediction_count?: number;
    success_rate?: number;
    health_score?: number;
    avg_confidence?: number;
    total_decisions_logged?: number;
    decision_mix?: { BUY?: number; HOLD?: number; SELL?: number };
  } | null>(null);
  const [redoStack, setRedoStack] = useState<KnowledgeItem[][]>([]);
  const [notification, setNotification] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null);
  const [bulkTagInput, setBulkTagInput] = useState('');
  const [bulkAction, setBulkAction] = useState<'add' | 'remove'>('add');
  const [showArchived, setShowArchived] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());
  const [tagCloud, setTagCloud] = useState<Record<string, number>>({});
  const [categoryStats, setCategoryStats] = useState<Record<string, number>>({});

  const searchTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const successTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // ===== CONSTANTS =====
  const categories = ['All', 'Trading', 'Strategy', 'Market', 'Finance', 'General Knowledge', 'QA', 'AI Generated', 'Cryptocurrency', 'Economy', 'Business', 'Technology'];
  const types = ['All', 'fact', 'concept', 'rule', 'pattern', 'insight', 'reference', 'qa', 'strategy'];
  const trendingTopics = ['bitcoin', 'halving', 'strategy', 'mtf-alignment', 'kraken', 'indonesia', 'bi-rate', 'ethereum', 'solana', 'defi'];
  const smartSuggestions = [
    'What is the optimal RSI threshold for MTF momentum?',
    'Tell me about Bitcoin Halving cycles',
    'How does Kraken WebSocket stream work?',
    'Summarize recent macro economic insights',
    'Explain DeFi yield farming strategies',
    'What is the difference between PoW and PoS?',
  ];

  // ===== COMPUTED VALUES =====
  const filteredKnowledge = useMemo(() => {
    let items = knowledgeList.filter((item) => {
      const matchesCat = selectedCategoryFilter === 'All' || item.category === selectedCategoryFilter;
      const matchesType = selectedTypeFilter === 'All' || item.type === selectedTypeFilter;
      const matchesSearch = item.content.toLowerCase().includes(searchFilter.toLowerCase()) ||
        item.tags.some(t => t.toLowerCase().includes(searchFilter.toLowerCase()));
      const matchesTag = tagFilter === '' || item.tags.some(t => t.toLowerCase() === tagFilter.toLowerCase());
      const matchesConfidence = item.confidence >= confidenceMin;
      const matchesDate = dateRange.start === '' || (item.createdAt >= dateRange.start && item.createdAt <= (dateRange.end || new Date().toISOString()));
      const matchesStatus = showArchived ? true : item.status !== 'archived';
      return matchesCat && matchesType && matchesSearch && matchesTag && matchesConfidence && matchesDate && matchesStatus;
    });

    items.sort((a, b) => {
      let comparison = 0;
      switch (sortBy) {
        case 'recent': comparison = new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime(); break;
        case 'confidence': comparison = a.confidence - b.confidence; break;
        case 'category': comparison = a.category.localeCompare(b.category); break;
        case 'importance': comparison = a.importance - b.importance; break;
        default: comparison = 0;
      }
      return sortOrder === 'asc' ? comparison : -comparison;
    });

    return items;
  }, [knowledgeList, selectedCategoryFilter, selectedTypeFilter, searchFilter, tagFilter, confidenceMin, dateRange, showArchived, sortBy, sortOrder]);

  // === PAGINASI ===
  const totalPages = Math.max(1, Math.ceil(filteredKnowledge.length / pageSize));
  const pageRecords = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredKnowledge.slice(start, start + pageSize);
  }, [filteredKnowledge, currentPage, pageSize]);

  // === FETCH LEARNING DATA ===
  useEffect(() => {
    const fetchLearning = async () => {
      try {
        const apiKey = localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823';
        const res = await fetch('/api/brain/self', {
          headers: { 'X-API-Key': apiKey },
        });
        if (res.ok) {
          const data = await res.json();
          const m = data?.metrics || {};
          const p = data?.performance || {};
          setLearningData({
            cycles: m.cycles ?? 0,
            decision_count: m.decision_count ?? 0,
            learning_count: m.learning_count ?? 0,
            prediction_count: m.prediction_count ?? 0,
            success_rate: m.success_rate ?? 0,
            health_score: m.health_score ?? 0,
            avg_confidence: p.avg_confidence ?? 0,
            total_decisions_logged: p.total_decisions_logged ?? 0,
            decision_mix: p.decision_mix ?? {},
          });
        }
      } catch (err) {
        console.warn('Failed to fetch learning data:', err);
      }
    };
    fetchLearning();
    const interval = setInterval(fetchLearning, 60000);
    return () => clearInterval(interval);
  }, []);

  // === FETCH AI USAGE ===
  useEffect(() => {
    const fetchAiUsage = async () => {
      try {
        const apiKey = localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823';
        const res = await fetch('/api/ai/status', {
          headers: { 'X-API-Key': apiKey },
        });
        if (res.ok) {
          const data = await res.json();
          setAiUsage(data);
        }
      } catch (err) {
        console.warn('Failed to fetch AI usage:', err);
      }
    };
    fetchAiUsage();
    const interval = setInterval(fetchAiUsage, 60000);
    return () => clearInterval(interval);
  }, []);

  // Reset page ke 1 saat filter berubah
  useEffect(() => {
    setCurrentPage(1);
  }, [searchFilter, selectedCategoryFilter, selectedTypeFilter, tagFilter, confidenceMin, showArchived]);

  // === QUALITY STATS ===
  const qualityStats = useMemo(() => {
    const total = filteredKnowledge.length || 1;
    const high = filteredKnowledge.filter((i) => (i.confidence || 0) >= 70).length;
    const medium = filteredKnowledge.filter((i) => (i.confidence || 0) >= 40 && (i.confidence || 0) < 70).length;
    const low = filteredKnowledge.filter((i) => (i.confidence || 0) < 40).length;
    const enhanced = filteredKnowledge.filter((i) => i.ai_enhanced).length;
    const avg = filteredKnowledge.length > 0
      ? Math.round(filteredKnowledge.reduce((s, i) => s + (i.confidence || 0), 0) / filteredKnowledge.length)
      : 0;
    return {
      high, medium, low, enhanced,
      highPct: Math.round((high / total) * 100),
      mediumPct: Math.round((medium / total) * 100),
      lowPct: Math.round((low / total) * 100),
      enhancedPct: Math.round((enhanced / total) * 100),
      avg,
    };
  }, [filteredKnowledge]);

  // === GROWTH 7 HARI ===
  const growthData = useMemo(() => {
    const days = 7;
    const now = new Date();
    const buckets: { label: string; count: number; date: string }[] = [];
    for (let i = days - 1; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const label = d.toLocaleDateString('id-ID', { day: '2-digit', month: 'short' });
      const dateKey = d.toISOString().slice(0, 10);
      buckets.push({ label, count: 0, date: dateKey });
    }
    knowledgeList.forEach((item) => {
      const ts = item.createdAt || (item as any).created_at;
      if (!ts) return;
      const dateKey = String(ts).slice(0, 10);
      const bucket = buckets.find((b) => b.date === dateKey);
      if (bucket) bucket.count += 1;
    });
    const max = Math.max(1, ...buckets.map((b) => b.count));
    const total = buckets.reduce((s, b) => s + b.count, 0);
    return { buckets, max, total };
  }, [knowledgeList]);

  // === RECENT ACTIVITY (10 terbaru) ===
  const recentActivity = useMemo(() => {
    const timeAgo = (ts: string | undefined): string => {
      if (!ts) return '—';
      try {
        const diff = Date.now() - new Date(ts).getTime();
        const mins = Math.floor(diff / 60000);
        if (mins < 1) return 'baru saja';
        if (mins < 60) return `${mins}m lalu`;
        const hours = Math.floor(mins / 60);
        if (hours < 24) return `${hours}j lalu`;
        const days = Math.floor(hours / 24);
        if (days < 7) return `${days}h lalu`;
        return new Date(ts).toLocaleDateString('id-ID', { day: '2-digit', month: 'short' });
      } catch {
        return '—';
      }
    };

    return [...knowledgeList]
      .sort((a, b) => {
        const ta = String(a.createdAt || (a as any).created_at || '');
        const tb = String(b.createdAt || (b as any).created_at || '');
        return tb.localeCompare(ta);
      })
      .slice(0, 20)
      .map((item) => {
        const ts = item.createdAt || (item as any).created_at;
        const raw = (item.content || '')
          .replace(/^Observation type:\s*/i, '')
          .replace(/^Q:\s*/i, '')
          .replace(/\n+/g, ' ')
          .trim();
        const isTruncated = raw.length > 150;
        const preview = raw.substring(0, 150) + (isTruncated ? '…' : '');
        const isQA = item.category === 'Q&A';
        const isEnhanced = item.ai_enhanced;
        // Icon per kategori
        const icon = isQA ? '💬' : item.category === 'Cognitive Observation' ? '🧠' : isEnhanced ? '✨' : '📄';
        return {
          text: preview || '(kosong)',
          time: timeAgo(ts),
          color: isQA ? 'bg-purple-400' : isEnhanced ? 'bg-teal-400' : 'bg-cyan-400',
          category: item.category || 'General',
          icon,
        };
      });
  }, [knowledgeList]);

  // === PAGINATION NUMBERS ===
  const pageNumbers = useMemo(() => {
    const pages: number[] = [];
    const maxVisible = 5;
    let start = Math.max(1, currentPage - Math.floor(maxVisible / 2));
    let end = Math.min(totalPages, start + maxVisible - 1);
    if (end - start + 1 < maxVisible) {
      start = Math.max(1, end - maxVisible + 1);
    }
    for (let i = start; i <= end; i++) pages.push(i);
    return pages;
  }, [currentPage, totalPages]);

  const aiEnhancedItems = knowledgeList.filter((item) => item.ai_enhanced);
  const aiStats = {
    total: knowledgeList.length,
    enhanced: aiEnhancedItems.length,
    percentage: knowledgeList.length > 0 ? (aiEnhancedItems.length / knowledgeList.length * 100) : 0,
  };

  useEffect(() => {
    const tags: Record<string, number> = {};
    const cats: Record<string, number> = {};
    knowledgeList.forEach(item => {
      item.tags.forEach(tag => {
        tags[tag] = (tags[tag] || 0) + 1;
      });
      cats[item.category] = (cats[item.category] || 0) + 1;
    });
    setTagCloud(tags);
    setCategoryStats(cats);
  }, [knowledgeList]);

  // ============================================================
  // HANDLERS
  // ============================================================

  const handleAsk = useCallback(async () => {
    if (!question.trim()) {
      setQaError('Please enter a question.');
      return;
    }
    setIsAnswering(true);
    setQaError(null);
    setQaAnswer(null);
    setQaData(null);
    setQaSources([]);

    try {
      const keywords = question.toLowerCase().split(' ');
      // Filter stop words (kata umum yang tidak informatif)
      const STOP_WORDS = new Set([
        'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dengan', 'adalah',
        'ini', 'itu', 'hal', 'baru', 'saya', 'kamu', 'anda', 'apa', 'bagaimana',
        'cara', 'adalah', 'akan', 'bisa', 'dapat', 'juga', 'atau', 'tidak',
        'the', 'and', 'is', 'are', 'was', 'were', 'a', 'an', 'of', 'to',
        'in', 'on', 'for', 'with', 'this', 'that', 'it', 'i', 'you', 'we',
      ]);

      const meaningfulKeywords = keywords.filter(
        (k) => k.length >= 3 && !STOP_WORDS.has(k)
      );

      let matches: { item: KnowledgeItem; score: number }[] = [];

      for (const item of knowledgeList) {
        let score = 0;
        const content = item.content.toLowerCase();
        const tags = item.tags.map(t => t.toLowerCase());

        for (const keyword of meaningfulKeywords) {
          if (content.includes(keyword)) score += 1;
          if (tags.some(t => t.includes(keyword))) score += 1.5;
        }
        if (item.ai_enhanced && score > 0) score += 0.3;
        if (score >= 1.0) matches.push({ item, score });
      }

      matches.sort((a, b) => b.score - a.score);
      // Hanya ambil 5 teratas + minimal score 1.0
      const topMatches = matches.filter((m) => m.score >= 1.0).slice(0, 5);

      try {
        const response = await fetch('/api/ai/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823',
          },
          body: JSON.stringify({
            question: question,
            context: topMatches.map(m => m.item.content).join('\n\n')
          }),
        });

        if (response.ok) {
          const data = await response.json();
          
          // Cek apakah response baru (JSON terstruktur)
          if (data.ai_enabled && (data.title || data.sections)) {
            setQaData(data);
            setQaAnswer(null);
            setQaSources(topMatches.map(m => m.item));

            // === AUTO-SAVE JSON RESPONSE KE KB ===
            if (autoSave) {
              try {
                // Convert JSON response ke markdown text
                const parts: string[] = [];
                if (data.summary) parts.push(data.summary);
                
                if (data.sections && Array.isArray(data.sections)) {
                  for (const sec of data.sections) {
                    if (sec.heading) parts.push(`\n## ${sec.heading}`);
                    if (sec.items && Array.isArray(sec.items)) {
                      for (const item of sec.items) {
                        parts.push(`- ${item}`);
                      }
                    } else if (sec.content) {
                      parts.push(sec.content);
                    }
                  }
                }
                
                if (data.metrics && Array.isArray(data.metrics)) {
                  parts.push('\n## Data');
                  for (const m of data.metrics) {
                    parts.push(`- ${m.label}: ${m.value}`);
                  }
                }
                
                if (data.actions && Array.isArray(data.actions)) {
                  parts.push('\n## Saran');
                  for (const a of data.actions) {
                    parts.push(`- ${a}`);
                  }
                }
                
                const answerText = parts.join('\n').trim();
                
                if (answerText) {
                  const newItem = {
                    content: `Q: ${question}\n\nA: ${answerText}`,
                    category: 'Q&A',
                    type: 'qa' as const,
                    confidence: Math.round((data.confidence || 0.7) * 100),
                    importance: 0.7,
                    tags: [
                      'qa',
                      'ai-generated',
                      data.question_type || 'general',
                      ...question.toLowerCase().split(' ').filter((w: string) => w.length > 3).slice(0, 5),
                    ],
                    status: 'active' as const,
                    source: 'ai_chat',
                    ai_enhanced: true,
                  };

                  const apiKey = localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823';
                  const saveResponse = await fetch('/api/knowledge/add', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                      'X-API-Key': apiKey,
                    },
                    body: JSON.stringify(newItem),
                  });

                  if (saveResponse.ok) {
                    const savedData = await saveResponse.json();
                    onAddKnowledge(savedData.item || newItem);
                    setNotification({ type: 'success', message: '✅ Q&A saved to knowledge base!' });
                  } else {
                    onAddKnowledge(newItem);
                  }
                }
              } catch (saveError) {
                console.warn('Auto-save JSON failed:', saveError);
              }
            }
          } else if (data.ai_enabled && data.answer) {
            // Fallback ke string lama
            setQaAnswer(data.answer);
            setQaData(null);
            setQaSources(topMatches.map(m => m.item));
            
            if (autoSave) {
              try {
                const newItem = {
                  content: `Q: ${question}\nA: ${data.answer}`,
                  category: 'QA',
                  type: 'qa' as const,
                  confidence: 85,
                  importance: 0.7,
                  tags: ['qa', 'ai-generated', ...question.toLowerCase().split(' ').slice(0, 3)],
                  status: 'active' as const,
                  source: 'ai_chat',
                  ai_enhanced: true,
                };
                
                const apiKey = localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823';
                const saveResponse = await fetch('/api/knowledge/add', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': apiKey,
                  },
                  body: JSON.stringify(newItem),
                });
                
                if (saveResponse.ok) {
                  const savedData = await saveResponse.json();
                  if (savedData.item) {
                    onAddKnowledge(savedData.item);
                  } else {
                    onAddKnowledge(newItem);
                  }
                  setNotification({ type: 'success', message: '✅ AI answer saved to knowledge base!' });
                } else {
                  onAddKnowledge(newItem);
                }
              } catch (saveError) {
                console.warn('Auto-save failed:', saveError);
                const fallbackItem = {
                  content: `Q: ${question}\nA: ${data.answer}`,
                  category: 'QA',
                  type: 'qa' as const,
                  confidence: 85,
                  importance: 0.7,
                  tags: ['qa', 'ai-generated'],
                  status: 'active' as const,
                  source: 'ai_chat',
                  ai_enhanced: true,
                };
                onAddKnowledge(fallbackItem);
              }
            }
            
            setIsAnswering(false);
            return;
          }
        }
      } catch (apiError) {
        console.warn('AI API call failed:', apiError);
      }

      if (topMatches.length > 0) {
        const bestMatch = topMatches[0];
        const answer = bestMatch.item.ai_summary || bestMatch.item.content;
        let response = `📚 **Best match** (confidence: ${bestMatch.score})\n\n${answer}`;
        if (topMatches.length > 1) {
          response += `\n\n📖 **Related entries:**\n`;
          topMatches.slice(1, 3).forEach((m, i) => {
            const preview = m.item.content.substring(0, 60) + '...';
            response += `${i + 1}. ${preview}\n`;
          });
        }
        setQaAnswer(response);
        setQaSources(topMatches.map(m => m.item));
        
        if (autoSave) {
          const fallbackItem = {
            content: `Q: ${question}\nA: ${response}`,
            category: 'QA',
            type: 'qa' as const,
            confidence: 80,
            importance: 0.6,
            tags: ['qa', 'local-match'],
            status: 'active' as const,
            source: 'local_knowledge',
            ai_enhanced: false,
          };
          onAddKnowledge(fallbackItem);
          setNotification({ type: 'success', message: '✅ Q&A saved from local knowledge!' });
        }
      } else {
        setQaAnswer(`🤔 I don't have knowledge about "${question}" yet. Add it to the knowledge base!`);
        setQaSources([]);
      }
    } catch (error) {
      setQaError('Failed to process your question.');
      console.error('Q&A error:', error);
    } finally {
      setIsAnswering(false);
    }
  }, [question, knowledgeList, autoSave, onAddKnowledge]);

  const handleSaveText = useCallback(async () => {
    if (!textContent.trim()) {
      setNotification({ type: 'error', message: 'Please enter some content.' });
      return;
    }
    setIsSubmitting(true);
    setSubmitError(null);
    setSubmitSuccess(null);

    try {
      const newItem = {
        content: textContent.trim(),
        category: 'Auto',   // Backend akan auto-classify pakai AI
        type: 'fact' as const,
        confidence: 85,
        importance: 0.8,
        tags: ['user-added'],
        status: 'active' as const,
        source: 'user_input',
        ai_enhanced: false,
      };

      // POST ke API — backend akan auto-classify category pakai AI
      const apiKey = localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823';
      const res = await fetch('/api/knowledge/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey,
        },
        body: JSON.stringify({
          content: newItem.content,
          category: newItem.category,
          type: newItem.type,
          tags: newItem.tags,
          confidence: newItem.confidence,
          importance: newItem.importance,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        onAddKnowledge(data.item || newItem);
        setTextContent('');
        setNotification({
          type: 'success',
          message: `✅ Saved! Auto-classified sebagai ${data.item?.category || 'General'}`,
        });
      } else {
        // Fallback ke state lokal kalau API gagal
        onAddKnowledge(newItem);
        setTextContent('');
        setNotification({ type: 'success', message: '✅ Knowledge saved (offline mode)' });
      }
    } catch (error) {
      setNotification({ type: 'error', message: 'Failed to save knowledge.' });
      console.error('Save error:', error);
    } finally {
      setIsSubmitting(false);
    }
  }, [textContent, category, onAddKnowledge]);

  const handleSaveRaw = useCallback(() => {
    if (!rawContent.trim()) {
      setNotification({ type: 'error', message: 'Please paste some raw data.' });
      return;
    }
    setIsSubmitting(true);

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
        type: 'fact' as const,
        confidence: 90,
        importance: 0.8,
        tags: tags,
        status: 'active' as const,
        source: 'raw_data_input',
        metadata: { original_length: rawContent.length },
        ai_enhanced: false,
      });

      setRawContent('');
      setNotification({ type: 'success', message: '✅ Raw data parsed and saved!' });
    } catch (error) {
      setNotification({ type: 'error', message: 'Failed to parse raw data.' });
      console.error('Raw parse error:', error);
    } finally {
      setIsSubmitting(false);
    }
  }, [rawContent, onAddKnowledge]);

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
          'X-API-Key': localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823',
        },
        body: JSON.stringify({ url: urlContent }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();

      onAddKnowledge({
        content: data.content || `Fetched content from ${urlContent}`,
        category: 'Market',
        type: 'reference' as const,
        confidence: 80,
        importance: 0.7,
        tags: ['url-fetched', 'macro', ...(data.tags || [])],
        status: 'active' as const,
        source: `url:${urlContent}`,
        metadata: { url: urlContent },
        ai_enhanced: false,
      });

      setUrlContent('');
      setNotification({ type: 'success', message: '✅ URL content fetched and saved!' });
    } catch (error) {
      console.warn('URL fetch failed:', error);
      onAddKnowledge({
        content: `[URL Reference] ${urlContent}`,
        category: 'Market',
        type: 'reference' as const,
        confidence: 60,
        importance: 0.5,
        tags: ['url-reference'],
        status: 'pending' as const,
        source: `url:${urlContent}`,
        metadata: { url: urlContent },
        ai_enhanced: false,
      });
      setUrlContent('');
      setNotification({ type: 'success', message: '✅ URL saved as reference.' });
    } finally {
      setIsFetchingUrl(false);
    }
  }, [urlContent, onAddKnowledge]);

  const handleGenerateAI = useCallback(async () => {
    if (!aiPrompt.trim()) {
      setNotification({ type: 'error', message: 'Please enter a topic or prompt.' });
      return;
    }
    if (!aiUsage?.enabled) {
      setNotification({ type: 'error', message: 'AI is disabled. Set DEEPSEEK_API_KEY.' });
      return;
    }

    setIsGenerating(true);
    try {
      const apiKey = localStorage.getItem('apiKey') || 'iks_612d40ce554b1670525355c85567f823';
      const res = await fetch('/api/ai/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey,
        },
        body: JSON.stringify({
          question: 'Buatkan knowledge terstruktur tentang: ' + aiPrompt + '. Sertakan definisi, konsep kunci, contoh konkret, dan insight penting. Format dalam paragraf yang informatif.',
        }),
      });

      if (!res.ok) throw new Error('HTTP ' + res.status);

      const data = await res.json();

      const NL = String.fromCharCode(10);
      const parts: string[] = [];
      if (data.summary) parts.push(data.summary);
      if (data.sections && Array.isArray(data.sections)) {
        for (const s of data.sections) {
          if (s.heading) parts.push('## ' + s.heading);
          if (s.content) parts.push(s.content);
          if (s.items && Array.isArray(s.items)) parts.push(s.items.join(NL));
        }
      }
      let generated = parts.join(NL + NL);
      if (!generated.trim()) generated = data.answer || JSON.stringify(data);

      onAddKnowledge({
        content: generated.substring(0, 2000),
        category: 'AI Generated',
        type: 'insight' as const,
        confidence: Math.round((data.confidence || 0.85) * 100),
        importance: 0.8,
        tags: ['ai-generated', data.question_type || 'general', aiPrompt.toLowerCase().substring(0, 20)],
        status: 'active' as const,
        source: 'ai_prompt:' + aiPrompt,
        metadata: { prompt: aiPrompt, question_type: data.question_type },
        ai_enhanced: false,
      });

      setAiPrompt('');
      setNotification({ type: 'success', message: 'AI generated knowledge tentang "' + aiPrompt + '"' });
    } catch (error) {
      console.error('AI generate error:', error);
      setNotification({ type: 'error', message: 'Gagal generate konten AI.' });
    } finally {
      setIsGenerating(false);
    }
  }, [aiPrompt, aiUsage, onAddKnowledge]);

  const handleEdit = useCallback((item: KnowledgeItem) => {
    setEditingItem(item);
  }, []);

  const handleSaveEdit = useCallback((id: string, updates: Partial<KnowledgeItem>) => {
    onUpdateKnowledge?.(id, updates);
    setEditingItem(null);
    setNotification({ type: 'success', message: '✅ Knowledge updated successfully!' });
  }, [onUpdateKnowledge]);

  const handleDelete = useCallback((id: string) => {
    if (window.confirm('Are you sure you want to delete this knowledge item?')) {
      onDeleteKnowledge?.(id);
      setNotification({ type: 'info', message: '🗑️ Knowledge deleted.' });
    }
  }, [onDeleteKnowledge]);

  const handleBulkDelete = useCallback(() => {
    if (selectedIds.length === 0) return;
    if (window.confirm(`Delete ${selectedIds.length} items?`)) {
      selectedIds.forEach(id => onDeleteKnowledge?.(id));
      setSelectedIds([]);
      setNotification({ type: 'info', message: `🗑️ Deleted ${selectedIds.length} items.` });
    }
  }, [selectedIds, onDeleteKnowledge]);

  const handleBulkTag = useCallback((action: 'add' | 'remove') => {
    if (selectedIds.length === 0 || !bulkTagInput.trim()) return;
    selectedIds.forEach(id => {
      const item = knowledgeList.find(k => k.id === id);
      if (item) {
        const newTags = action === 'add'
          ? [...new Set([...item.tags, bulkTagInput.trim()])]
          : item.tags.filter(t => t !== bulkTagInput.trim());
        onUpdateKnowledge?.(id, { tags: newTags });
      }
    });
    setBulkTagInput('');
    setNotification({ type: 'success', message: `${action === 'add' ? 'Added' : 'Removed'} tag "${bulkTagInput}" from ${selectedIds.length} items.` });
  }, [selectedIds, bulkTagInput, knowledgeList, onUpdateKnowledge]);

  const handleExport = useCallback(() => {
    let data: any = filteredKnowledge;
    let mimeType = 'application/json';
    let filename = `knowledge_export_${new Date().toISOString().split('T')[0]}`;
    let content = '';

    switch (exportFormat) {
      case 'json':
        content = JSON.stringify(data, null, 2);
        mimeType = 'application/json';
        filename += '.json';
        break;
      case 'csv':
        const headers = ['id', 'content', 'category', 'type', 'confidence', 'importance', 'tags', 'status', 'createdAt'];
        const rows = data.map((item: KnowledgeItem) =>
          headers.map(h => JSON.stringify((item as any)[h] || '')).join(',')
        );
        content = headers.join(',') + '\n' + rows.join('\n');
        mimeType = 'text/csv';
        filename += '.csv';
        break;
      case 'markdown':
        content = data.map((item: KnowledgeItem) =>
          `## ${item.category} - ${item.type}\n\n${item.content}\n\n**Confidence:** ${item.confidence}%\n**Tags:** ${item.tags.join(', ')}\n**Created:** ${item.createdAt}\n\n---\n`
        ).join('\n');
        mimeType = 'text/markdown';
        filename += '.md';
        break;
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
    setNotification({ type: 'success', message: `📦 Exported ${filteredKnowledge.length} items as ${exportFormat.toUpperCase()}` });
  }, [filteredKnowledge, exportFormat]);

  const handleImport = useCallback(() => {
    if (!importData.trim()) {
      setNotification({ type: 'error', message: 'Please paste data to import.' });
      return;
    }
    try {
      const data = JSON.parse(importData);
      const items = Array.isArray(data) ? data : [data];
      items.forEach((item: any) => {
        onAddKnowledge({
          content: item.content || item.text || JSON.stringify(item),
          category: item.category || 'General',
          type: item.type || 'fact',
          confidence: item.confidence || 80,
          importance: item.importance || 0.7,
          tags: item.tags || [],
          status: 'active',
          source: 'import',
          ai_enhanced: false,
        });
      });
      setImportData('');
      setShowImportModal(false);
      setNotification({ type: 'success', message: `📥 Imported ${items.length} items successfully!` });
    } catch (error) {
      setNotification({ type: 'error', message: 'Invalid JSON data. Please check format.' });
    }
  }, [importData, onAddKnowledge]);

  const toggleSelectAll = useCallback(() => {
    if (selectedIds.length === filteredKnowledge.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(filteredKnowledge.map(item => item.id));
    }
  }, [selectedIds, filteredKnowledge]);

  const toggleExpand = useCallback((id: string) => {
    setExpandedItems(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }, []);

  const toggleSelect = useCallback((id: string) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!keyboardMode) return;

      switch (e.key) {
        case 'k':
        case 'K':
          if ((e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            inputRef.current?.focus();
          }
          break;
        case 'Escape':
          setSelectedIds([]);
          setEditingItem(null);
          break;
        case 'b':
        case 'B':
          if ((e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            setIsBulkMode(!isBulkMode);
          }
          break;
        case 's':
        case 'S':
          if ((e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            setShowShortcuts(!showShortcuts);
          }
          break;
        default:
          break;
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [keyboardMode, isBulkMode, showShortcuts]);

  const handleEnhanceItem = useCallback((id: string) => {
    if (onEnhanceWithAI) {
      setEnhanceTargetId(id);
      onEnhanceWithAI(id);
      setTimeout(() => setEnhanceTargetId(null), 2000);
    }
  }, [onEnhanceWithAI]);

  const handleEnhanceAll = useCallback(() => {
    if (onBatchEnhance && window.confirm('Enhance all knowledge items with AI? This may take a moment.')) {
      setIsEnhancing(true);
      onBatchEnhance();
      setTimeout(() => setIsEnhancing(false), 3000);
    }
  }, [onBatchEnhance]);

  const clearFilters = useCallback(() => {
    setSearchFilter('');
    setSelectedCategoryFilter('All');
    setSelectedTypeFilter('All');
    setTagFilter('');
    setConfidenceMin(0);
    setDateRange({ start: '', end: '' });
    setShowArchived(false);
  }, []);

  useEffect(() => {
    if (notification) {
      const timer = setTimeout(() => setNotification(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [notification]);

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div id="knowledge-view" className="space-y-6 pb-12">
      {notification && (
        <div className={`p-3 rounded-xl flex items-center gap-2 text-xs ${notification.type === 'success' ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-400' : notification.type === 'error' ? 'bg-rose-500/10 border border-rose-500/30 text-rose-400' : 'bg-blue-500/10 border border-blue-500/30 text-blue-400'}`}>
          <span>{notification.message}</span>
          <button onClick={() => setNotification(null)} className="ml-auto opacity-70 hover:opacity-100">
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#131A22] to-[#1A2530] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-teal-600/20 border border-teal-500/30 flex items-center justify-center text-teal-400">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">Knowledge Base & AI Memory v1.02</h2>
            <p className="text-xs text-[#8D9AAA]">
              {aiStats.enhanced > 0 ? `🧠 ${aiStats.enhanced} items AI-enhanced · ${aiStats.percentage.toFixed(0)}% of knowledge` : '💡 AI Enhancement ready - Add knowledge to get started'}
              {wsConnected && <span className="ml-2 text-emerald-400">● LIVE</span>}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
            <span className="text-[10px] text-[#5F6B78] font-bold block">Total Items</span>
            <span className="text-sm font-black text-white font-mono">{knowledgeList.length}</span>
          </div>
          <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
            <span className="text-[10px] text-[#5F6B78] font-bold block">AI Enhanced</span>
            <span className="text-sm font-black text-purple-400 font-mono">{aiEnhancedItems.length}</span>
          </div>
          <div className="px-3.5 py-1.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-right">
            <span className="text-[10px] text-[#5F6B78] font-bold block">Categories</span>
            <span className="text-sm font-black text-white font-mono">{Object.keys(categoryStats).length}</span>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        <button onClick={() => setShowAnalytics(!showAnalytics)} className="text-xs font-bold text-[#8D9AAA] hover:text-white flex items-center gap-1">
          {showAnalytics ? '▼' : '▶'} Analytics Dashboard
        </button>

        {showAnalytics && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* === KIRI: KPI + Top Tags === */}
            <div className="space-y-3">
              {/* KPI GRID 2x3 */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-center">
                  <div className="text-2xl font-bold text-white font-mono">{knowledgeList.length.toLocaleString()}</div>
                  <div className="text-[10px] text-[#8D9AAA] font-bold uppercase tracking-wider">Total Items</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-teal-400 font-mono">{Object.keys(categoryStats).length}</div>
                  <div className="text-[10px] text-[#8D9AAA] font-bold uppercase tracking-wider">Categories</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-400 font-mono">{aiEnhancedItems.length}</div>
                  <div className="text-[10px] text-[#8D9AAA] font-bold uppercase tracking-wider">AI Enhanced</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-amber-400 font-mono">
                    {knowledgeList.length > 0 ? Math.round(knowledgeList.reduce((sum, i) => sum + i.confidence, 0) / knowledgeList.length) : 0}%
                  </div>
                  <div className="text-[10px] text-[#8D9AAA] font-bold uppercase tracking-wider">Avg Confidence</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-emerald-400 font-mono">{growthData.total}</div>
                  <div className="text-[10px] text-[#8D9AAA] font-bold uppercase tracking-wider">Last 7 Days</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-rose-400 font-mono">
                    {knowledgeList.filter((i) => !i.ai_enhanced).length}
                  </div>
                  <div className="text-[10px] text-[#8D9AAA] font-bold uppercase tracking-wider">Pending AI</div>
                </div>
              </div>

              {/* TOP TAGS */}
              <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="text-[10px] text-[#8D9AAA] font-bold uppercase tracking-wider mb-2 flex items-center gap-2">
                  <Tag className="w-3.5 h-3.5 text-teal-400" />
                  Top Tags
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {Object.entries(tagCloud).sort((a, b) => b[1] - a[1]).filter(([, count]) => count >= 2).slice(0, 8).map(([tag, count]) => (
                    <span key={tag} className="text-[10px] px-2 py-0.5 rounded-full bg-[#1A2530] text-[#8D9AAA] hover:text-white cursor-pointer transition-colors border border-[#26313D]" onClick={() => setTagFilter(tag)}>
                      #{tag} <span className="text-[#5F6B78]">({count})</span>
                    </span>
                  ))}
                </div>
              </div>

              {/* ============================================================ */}
              {/* KOMPONEN: LEARNING PROGRESS PANEL (kolom kanan)             */}
              {/* ============================================================ */}
              <div className="p-4 rounded-xl bg-gradient-to-br from-[#131A22] to-[#0F1620] border border-[#26313D]">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                    <Brain className="w-4 h-4 text-cyan-400" />
                    Learning Progress
                  </h3>
                  <span className="text-[9px] text-cyan-400 font-mono px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20 flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
                    LIVE
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                  {/* Cycles */}
                  <div className="p-2.5 rounded-lg bg-[#0B0F14]/60 border border-cyan-500/10">
                    <div className="flex items-center gap-1.5 mb-1">
                      <RefreshCw className="w-3 h-3 text-cyan-400" />
                      <span className="text-[9px] uppercase text-[#8D9AAA] font-bold">Cycles</span>
                    </div>
                    <div className="text-lg font-bold text-cyan-300 font-mono">
                      {(learningData?.cycles ?? 0).toLocaleString()}
                    </div>
                  </div>

                  {/* Decisions */}
                  <div className="p-2.5 rounded-lg bg-[#0B0F14]/60 border border-teal-500/10">
                    <div className="flex items-center gap-1.5 mb-1">
                      <Target className="w-3 h-3 text-teal-400" />
                      <span className="text-[9px] uppercase text-[#8D9AAA] font-bold">Decisions</span>
                    </div>
                    <div className="text-lg font-bold text-teal-300 font-mono">
                      {(learningData?.decision_count ?? 0).toLocaleString()}
                    </div>
                  </div>

                  {/* Predictions */}
                  <div className="p-2.5 rounded-lg bg-[#0B0F14]/60 border border-purple-500/10">
                    <div className="flex items-center gap-1.5 mb-1">
                      <Sparkles className="w-3 h-3 text-purple-400" />
                      <span className="text-[9px] uppercase text-[#8D9AAA] font-bold">Predictions</span>
                    </div>
                    <div className="text-lg font-bold text-purple-300 font-mono">
                      {(learningData?.prediction_count ?? 0).toLocaleString()}
                    </div>
                  </div>

                  {/* Learning */}
                  <div className="p-2.5 rounded-lg bg-[#0B0F14]/60 border border-emerald-500/10">
                    <div className="flex items-center gap-1.5 mb-1">
                      <GraduationCap className="w-3 h-3 text-emerald-400" />
                      <span className="text-[9px] uppercase text-[#8D9AAA] font-bold">Learning</span>
                    </div>
                    <div className="text-lg font-bold text-emerald-300 font-mono">
                      {(learningData?.learning_count ?? 0).toLocaleString()}
                    </div>
                  </div>

                  {/* Success Rate */}
                  <div className="p-2.5 rounded-lg bg-[#0B0F14]/60 border border-blue-500/10">
                    <div className="flex items-center gap-1.5 mb-1">
                      <TrendingUp className="w-3 h-3 text-blue-400" />
                      <span className="text-[9px] uppercase text-[#8D9AAA] font-bold">Success</span>
                    </div>
                    <div className="text-lg font-bold text-blue-300 font-mono">
                      {(learningData?.success_rate ?? 0).toFixed(1)}%
                    </div>
                    <div className="mt-1 h-1 rounded-full bg-[#131A22] overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 to-cyan-400 transition-all duration-500"
                        style={{ width: `${Math.min(100, learningData?.success_rate ?? 0)}%` }}
                      />
                    </div>
                  </div>

                  {/* Health Score */}
                  <div className="p-2.5 rounded-lg bg-[#0B0F14]/60 border border-rose-500/10">
                    <div className="flex items-center gap-1.5 mb-1">
                      <Heart className="w-3 h-3 text-rose-400" />
                      <span className="text-[9px] uppercase text-[#8D9AAA] font-bold">Health</span>
                    </div>
                    <div className="text-lg font-bold text-rose-300 font-mono">
                      {(learningData?.health_score ?? 0).toFixed(0)}%
                    </div>
                    <div className="mt-1 h-1 rounded-full bg-[#131A22] overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-rose-500 to-pink-400 transition-all duration-500"
                        style={{ width: `${Math.min(100, learningData?.health_score ?? 0)}%` }}
                      />
                    </div>
                  </div>
                </div>

                {/* Decision Mix */}
                {learningData?.decision_mix && (
                  <div className="mt-3 pt-3 border-t border-[#26313D]">
                    <div className="flex items-center justify-between text-[9px] text-[#5F6B78] font-bold uppercase mb-2">
                      <span>Decision Mix</span>
                      <span className="text-[#8D9AAA] font-mono">
                        {(learningData?.total_decisions_logged ?? 0).toLocaleString()} logged
                      </span>
                    </div>
                    <div className="flex items-center gap-2 h-2 rounded-full overflow-hidden bg-[#0B0F14]">
                      {(() => {
                        const mix = learningData?.decision_mix || {};
                        const total = (mix.BUY ?? 0) + (mix.HOLD ?? 0) + (mix.SELL ?? 0) || 1;
                        const buyPct = ((mix.BUY ?? 0) / total) * 100;
                        const holdPct = ((mix.HOLD ?? 0) / total) * 100;
                        const sellPct = ((mix.SELL ?? 0) / total) * 100;
                        return (
                          <>
                            <div className="h-full bg-emerald-500 transition-all" style={{ width: `${buyPct}%` }} title={`BUY: ${mix.BUY ?? 0}`} />
                            <div className="h-full bg-amber-500 transition-all" style={{ width: `${holdPct}%` }} title={`HOLD: ${mix.HOLD ?? 0}`} />
                            <div className="h-full bg-rose-500 transition-all" style={{ width: `${sellPct}%` }} title={`SELL: ${mix.SELL ?? 0}`} />
                          </>
                        );
                      })()}
                    </div>
                    <div className="flex items-center justify-between text-[9px] font-mono mt-1.5">
                      <span className="text-emerald-400">● BUY {learningData?.decision_mix?.BUY ?? 0}</span>
                      <span className="text-amber-400">● HOLD {learningData?.decision_mix?.HOLD ?? 0}</span>
                      <span className="text-rose-400">● SELL {learningData?.decision_mix?.SELL ?? 0}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* === KANAN: Growth Chart + Recent Activity === */}
            <div className="space-y-3">
              {/* GROWTH CHART 7 HARI */}
              <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-emerald-400" />
                    Growth (7 Days)
                  </h3>
                  <span className="text-[10px] text-emerald-400 font-mono font-bold">
                    +{growthData.total} items
                  </span>
                </div>
                <div className="flex items-end gap-1.5 h-28 pt-4">
                  {growthData.buckets.map((b, i) => {
                    const barHeight = Math.max(6, Math.round((b.count / growthData.max) * 80));
                    return (
                      <div key={i} className="flex-1 flex flex-col items-center justify-end gap-1 group h-full">
                        <span className="text-[9px] text-teal-400 font-mono font-bold opacity-70 group-hover:opacity-100 transition-opacity">
                          {b.count}
                        </span>
                        <div
                          className="w-full bg-gradient-to-t from-teal-600 to-teal-400 rounded-t transition-all hover:from-teal-500 hover:to-teal-300 shadow-lg shadow-teal-500/20"
                          style={{ height: `${barHeight}px`, minHeight: '6px' }}
                          title={`${b.label}: ${b.count} items`}
                        />
                        <span className="text-[8px] text-[#5F6B78] font-mono whitespace-nowrap">{b.label}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* RECENT ACTIVITY */}
              <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
                  <Clock className="w-4 h-4 text-cyan-400" />
                  Recent Activity
                </h3>
                <div className="space-y-2 max-h-[320px] overflow-y-auto pr-1 scrollbar-thin scrollbar-thumb-[#26313D]">
                  {recentActivity.length === 0 ? (
                    <div className="text-[10px] text-[#5F6B78] text-center py-4">Belum ada aktivitas</div>
                  ) : (
                    recentActivity.map((item, i) => (
                      <div key={i} className="flex items-start gap-2 text-[10px] py-0.5">
                        <span className="text-xs flex-shrink-0 leading-none mt-0.5">{item.icon}</span>
                        <div className="flex-1 min-w-0">
                          <div className="text-[#E8EDF2] line-clamp-2 leading-relaxed">{item.text}</div>
                          <div className="flex items-center gap-2 mt-0.5">
                            <span className="text-[#5F6B78] font-mono text-[9px]">{item.time}</span>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

            </div>
          </div>
        )}
      </div>

      {/* ============================================================ */}
      {/* KOMPONEN 1: AI USAGE PANEL                                   */}
      {/* ============================================================ */}
      <div className="p-4 rounded-xl bg-gradient-to-r from-purple-500/10 to-transparent border border-purple-500/20">
        <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
          <div className="flex items-center gap-2">
            <ZapIcon className="w-4 h-4 text-purple-400" />
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">AI Usage Today</h3>
          </div>
          <span className="text-[10px] text-purple-400 font-mono px-2 py-0.5 rounded bg-purple-500/10 border border-purple-500/20">
            {aiUsage?.model || 'deepseek-chat'}
          </span>
        </div>
        <div className="grid grid-cols-3 gap-3">
          <div>
            <div className="text-[9px] uppercase text-[#8D9AAA] font-bold">Calls Used</div>
            <div className="text-lg font-bold text-purple-300 font-mono mt-0.5">
              {aiUsage?.usage_today ?? 0}
            </div>
          </div>
          <div>
            <div className="text-[9px] uppercase text-[#8D9AAA] font-bold">Remaining</div>
            <div className="text-lg font-bold text-emerald-300 font-mono mt-0.5">
              {(aiUsage?.remaining ?? (aiUsage?.daily_limit ?? 0) - (aiUsage?.usage_today ?? 0)).toLocaleString()}
            </div>
          </div>
          <div>
            <div className="text-[9px] uppercase text-[#8D9AAA] font-bold">Daily Limit</div>
            <div className="text-lg font-bold text-white font-mono mt-0.5">
              {(aiUsage?.daily_limit ?? 0).toLocaleString()}
            </div>
          </div>
        </div>
        {/* Progress bar */}
        <div className="mt-3">
          <div className="h-1.5 rounded-full bg-[#0B0F14] overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-purple-500 to-teal-400 transition-all duration-500"
              style={{
                width: `${Math.min(100, ((aiUsage?.usage_today ?? 0) / (aiUsage?.daily_limit ?? 1)) * 100)}%`,
              }}
            />
          </div>
          <div className="flex items-center justify-between mt-1 text-[9px] text-[#5F6B78] font-mono">
            <span>{(((aiUsage?.usage_today ?? 0) / (aiUsage?.daily_limit ?? 1)) * 100).toFixed(2)}% used</span>
            <span>{aiUsage?.enabled ? '🟢 ONLINE' : '🔴 OFFLINE'}</span>
          </div>
        </div>
      </div>

      {/* ============================================================ */}
      {/* KOMPONEN 2: KNOWLEDGE QUALITY PANEL                          */}
      {/* ============================================================ */}
      <div className="p-4 rounded-xl bg-[#131A22] border border-[#26313D]">
        <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
          <Activity className="w-4 h-4 text-teal-400" />
          Knowledge Quality
        </h3>
        <div className="space-y-2.5">
          {/* High */}
          <div>
            <div className="flex items-center justify-between text-[10px] mb-1">
              <span className="text-emerald-400 font-bold">High (≥70%)</span>
              <span className="text-[#8D9AAA] font-mono">{qualityStats.high} items · {qualityStats.highPct}%</span>
            </div>
            <div className="h-1.5 rounded-full bg-[#0B0F14] overflow-hidden">
              <div className="h-full bg-emerald-500 transition-all duration-500" style={{ width: `${qualityStats.highPct}%` }} />
            </div>
          </div>
          {/* Medium */}
          <div>
            <div className="flex items-center justify-between text-[10px] mb-1">
              <span className="text-amber-400 font-bold">Medium (40-70%)</span>
              <span className="text-[#8D9AAA] font-mono">{qualityStats.medium} items · {qualityStats.mediumPct}%</span>
            </div>
            <div className="h-1.5 rounded-full bg-[#0B0F14] overflow-hidden">
              <div className="h-full bg-amber-500 transition-all duration-500" style={{ width: `${qualityStats.mediumPct}%` }} />
            </div>
          </div>
          {/* Low */}
          <div>
            <div className="flex items-center justify-between text-[10px] mb-1">
              <span className="text-rose-400 font-bold">Low (&lt;40%)</span>
              <span className="text-[#8D9AAA] font-mono">{qualityStats.low} items · {qualityStats.lowPct}%</span>
            </div>
            <div className="h-1.5 rounded-full bg-[#0B0F14] overflow-hidden">
              <div className="h-full bg-rose-500 transition-all duration-500" style={{ width: `${qualityStats.lowPct}%` }} />
            </div>
          </div>
        </div>
        <div className="mt-3 pt-3 border-t border-[#26313D] grid grid-cols-2 gap-3">
          <div>
            <div className="text-[9px] uppercase text-[#5F6B78] font-bold">Avg Confidence</div>
            <div className="text-lg font-bold text-teal-300 font-mono mt-0.5">{qualityStats.avg}%</div>
          </div>
          <div>
            <div className="text-[9px] uppercase text-[#5F6B78] font-bold">AI Enhanced</div>
            <div className="text-lg font-bold text-purple-300 font-mono mt-0.5">{qualityStats.enhancedPct}%</div>
          </div>
        </div>
      </div>

      {/* === ASK AI + ADD KNOWLEDGE (2 columns) === */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="p-5 rounded-2xl bg-[#1A2530] border border-[#26313D] space-y-3 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-teal-400" />
            <h3 className="text-sm font-bold text-white tracking-wider uppercase">Ask AI Knowledge Base</h3>
            {aiUsage?.enabled && <span className="text-[8px] font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/20">AI POWERED</span>}
            <span className="text-[8px] px-2 py-0.5 rounded bg-[#26313D] text-[#8D9AAA]">{autoSave ? 'Auto-save ON' : 'Auto-save OFF'}</span>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={() => setAutoSave(!autoSave)} className="text-[9px] px-2 py-0.5 rounded bg-[#0B0F14] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white transition-colors">
              {autoSave ? 'Auto-save' : 'Manual'}
            </button>
            <span className="text-[9px] text-[#5F6B78]">{aiStats.enhanced > 0 ? `${aiStats.enhanced} AI-enhanced items` : 'No AI enhancements yet'}</span>
          </div>
        </div>

        <div className="flex gap-2">
          <input ref={inputRef} type="text" placeholder="Ask anything about your knowledge base..." value={question} onChange={(e) => setQuestion(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleAsk()} className="flex-1 px-4 py-2.5 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-teal-500" disabled={isAnswering} />
          <button onClick={handleAsk} disabled={isAnswering || !question.trim()} className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition-all shadow-md shadow-teal-600/30 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
            {isAnswering ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
            <span>{isAnswering ? 'Searching...' : 'Ask'}</span>
          </button>
        </div>

        {qaError && <div className="p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs">{qaError}</div>}

        {/* Render AI Response — pakai AIVisualResponse kalau qaData ada (JSON baru) */}
        {qaData ? (
          <div className="p-4 rounded-xl bg-[#0B0F14] border border-teal-500/30">
            <AIVisualResponse
              response={qaData}
              onFollowUp={(q) => {
                setQuestion(q);
                setQaData(null);
                setQaError(null);
                setQaSources([]);
                setTimeout(() => handleAsk(), 50);
              }}
            />
            {qaSources.length > 0 && (
              <div className="mt-3 pt-3 border-t border-[#26313D]">
                <span className="text-[9px] text-[#5F6B78]">📚 Sources ({qaSources.length}):</span>
                {qaSources.slice(0, 3).map((src) => (
                  <div key={src.id} className="text-[9px] text-[#8D9AAA] truncate">
                    • {src.content.substring(0, 80)}...
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : qaAnswer ? (
          <div className="p-3.5 rounded-xl bg-[#0B0F14] border border-teal-500/30 text-xs text-teal-200 leading-relaxed font-sans whitespace-pre-line">
            <div className="flex items-center gap-2 mb-1">
              <Sparkles className="w-3 h-3 text-teal-400" />
              <strong className="text-teal-400">AI Answer</strong>
              {qaSources.length > 0 && <span className="text-[9px] text-[#5F6B78]">({qaSources.length} sources)</span>}
            </div>
            {qaAnswer}
          </div>
        ) : null}

        <div className="pt-2 flex flex-wrap items-center gap-2">
          <span className="text-[10px] text-[#5F6B78] font-bold">Suggestions:</span>
          {smartSuggestions.map((sug, i) => (
            <button key={i} onClick={() => { setQuestion(sug); setQaAnswer(null); setQaData(null); setQaError(null); setQaSources([]); }} className="text-[10px] px-2 py-1 rounded-md bg-[#0B0F14] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors">
              {sug}
            </button>
          ))}
        </div>
      </div>

      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70 flex-wrap gap-2">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Plus className="w-4 h-4 text-emerald-400" />
            Add Knowledge
          </h3>

          <div className="flex items-center gap-2 flex-wrap">
            {(['text', 'url', 'raw', 'ai'] as const).map((tab) => (
              <button key={tab} onClick={() => setActiveTab(tab)} className={`px-3 py-1 rounded-lg text-xs font-bold transition-colors ${activeTab === tab ? tab === 'ai' ? 'bg-purple-600 text-white' : 'bg-blue-600 text-white' : 'text-[#8D9AAA] hover:text-white bg-[#0B0F14]'}`}>
                {tab === 'text' && '📝 Text'}
                {tab === 'url' && '🌐 URL'}
                {tab === 'raw' && '📊 Raw'}
                {tab === 'ai' && '🤖 AI Generate'}
              </button>
            ))}
          </div>
        </div>

        {activeTab === 'text' && (
          <div className="space-y-3">
            <textarea rows={3} placeholder="Type or paste knowledge text here..." value={textContent} onChange={(e) => setTextContent(e.target.value)} className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-blue-500" disabled={isSubmitting} />
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div className="flex items-center gap-2">
                <span className="text-[10px] text-[#5F6B78] flex items-center gap-1 px-2 py-1 rounded bg-purple-500/5 border border-purple-500/10">
                  <Sparkles className="w-3 h-3 text-purple-400" />
                  AI akan auto-classify saat save
                </span>
              </div>
              <button onClick={handleSaveText} disabled={isSubmitting || !textContent.trim()} className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-md flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
                {isSubmitting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Check className="w-3.5 h-3.5" />}
                <span>{isSubmitting ? 'Analyzing...' : 'Analyze & Save'}</span>
              </button>
            </div>
          </div>
        )}

        {activeTab === 'url' && (
          <div className="space-y-3">
            <div className="flex gap-2">
              <input type="url" placeholder="https://example.com/article..." value={urlContent} onChange={(e) => setUrlContent(e.target.value)} className="flex-1 px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-purple-500" disabled={isFetchingUrl} />
              <button onClick={handleFetchUrl} disabled={isFetchingUrl || !urlContent.trim()} className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
                {isFetchingUrl ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Globe className="w-3.5 h-3.5" />}
                <span>{isFetchingUrl ? 'Fetching...' : 'Fetch & Analyze'}</span>
              </button>
            </div>
            {urlError && <div className="text-rose-400 text-[11px] bg-rose-500/10 p-2 rounded-lg border border-rose-500/20">{urlError}</div>}
          </div>
        )}

        {activeTab === 'raw' && (
          <div className="space-y-3">
            <textarea rows={3} placeholder="Paste raw JSON or CSV data..." value={rawContent} onChange={(e) => setRawContent(e.target.value)} className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none focus:border-amber-500" disabled={isSubmitting} />
            <button onClick={handleSaveRaw} disabled={isSubmitting || !rawContent.trim()} className="px-4 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
              {isSubmitting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <FileCode className="w-3.5 h-3.5" />}
              <span>{isSubmitting ? 'Parsing...' : 'Parse & Analyze'}</span>
            </button>
          </div>
        )}

        {activeTab === 'ai' && (
          <div className="space-y-3">
            <div className="p-3 rounded-xl bg-[#0B0F14] border border-purple-500/20">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-4 h-4 text-purple-400" />
                <span className="text-xs font-bold text-white">AI Content Generator</span>
                {!aiUsage?.enabled && <span className="text-[8px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/20">AI DISABLED</span>}
              </div>
              <p className="text-[10px] text-[#8D9AAA] mb-3">Generate knowledge using AI. Enter a topic and AI will create structured knowledge from it.</p>
              <div className="flex gap-2">
                <input type="text" placeholder="Enter a topic (e.g., 'Bitcoin halving')..." value={aiPrompt} onChange={(e) => setAiPrompt(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter' && !isGenerating) handleGenerateAI(); }} className="flex-1 px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-purple-500" disabled={!aiUsage?.enabled || isGenerating} />
                <button onClick={handleGenerateAI} disabled={!aiUsage?.enabled || isGenerating || !aiPrompt.trim()} className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
                  {isGenerating ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Brain className="w-3.5 h-3.5" />}
                  <span>{isGenerating ? 'Generating...' : 'Generate & Save'}</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      
      </div>
      {/* === END ASK AI + ADD KNOWLEDGE === */}

      {/* === UNIFIED KNOWLEDGE TOOLBAR === */}
      <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D] flex flex-wrap items-center gap-2">
        <div className="relative flex-1 min-w-[180px]">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#5F6B78]" />
          <input type="text" placeholder="Search knowledge..." value={searchFilter} onChange={(e) => setSearchFilter(e.target.value)} className="w-full pl-8 pr-8 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-teal-500 transition-colors" />
          {searchFilter && (
            <button onClick={() => setSearchFilter('')} className="absolute right-2 top-1/2 -translate-y-1/2 text-[#5F6B78] hover:text-white">
              <X className="w-3 h-3" />
            </button>
          )}
        </div>

        <button onClick={() => setShowFilters(!showFilters)} className={`px-2.5 py-1.5 rounded-lg border text-xs flex items-center gap-1.5 transition-colors ${showFilters ? 'bg-teal-600/20 text-teal-300 border-teal-500/40' : 'bg-[#0B0F14] text-[#8D9AAA] border-[#26313D] hover:text-white'}`}>
          <Filter className="w-3.5 h-3.5" />
          <span>Filters</span>
        </button>

        <select value={sortBy} onChange={(e) => setSortBy(e.target.value as any)} className="px-2 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white focus:outline-none focus:border-teal-500">
          <option value="recent">Recent</option>
          <option value="confidence">Confidence</option>
          <option value="category">Category</option>
          <option value="importance">Importance</option>
        </select>

        <button onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')} className="px-2 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-[#8D9AAA] hover:text-white transition-colors" title={sortOrder === 'asc' ? 'Ascending' : 'Descending'}>
          {sortOrder === 'asc' ? '↑' : '↓'}
        </button>

        <button onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')} className="px-2 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-[#8D9AAA] hover:text-white transition-colors" title={viewMode === 'grid' ? 'Switch to list' : 'Switch to grid'}>
          {viewMode === 'grid' ? '≡' : '⊞'}
        </button>

        <button onClick={() => setIsBulkMode(!isBulkMode)} className={`px-2.5 py-1.5 rounded-lg border text-xs flex items-center gap-1.5 transition-colors ${isBulkMode ? 'bg-teal-600 text-white border-teal-500' : 'bg-[#0B0F14] text-[#8D9AAA] border-[#26313D] hover:text-white'}`}>
          ☑ <span className="hidden sm:inline">Bulk</span>
        </button>

        <select value={exportFormat} onChange={(e) => setExportFormat(e.target.value as any)} className="px-2 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white">
          <option value="json">JSON</option>
          <option value="csv">CSV</option>
          <option value="markdown">Markdown</option>
        </select>
        <button onClick={handleExport} className="px-2.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-colors">⬇️ Export</button>

        <button onClick={() => setShowImportModal(true)} className="px-2.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-colors">⬆️ Import</button>

        <button onClick={() => setShowArchived(!showArchived)} className={`px-2.5 py-1.5 rounded-lg border text-xs transition-colors ${showArchived ? 'bg-amber-600 text-white border-amber-500' : 'bg-[#0B0F14] text-[#8D9AAA] border-[#26313D] hover:text-white'}`}>🗂️ Archived</button>

        <button onClick={() => setKeyboardMode(!keyboardMode)} className={`px-2.5 py-1.5 rounded-lg border text-xs transition-colors ${keyboardMode ? 'bg-blue-600 text-white border-blue-500' : 'bg-[#0B0F14] text-[#8D9AAA] border-[#26313D] hover:text-white'}`}>⌨️ {keyboardMode ? 'ON' : 'OFF'}</button>

        <button onClick={clearFilters} className="px-2.5 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-[#8D9AAA] hover:text-rose-300 text-xs transition-colors">✕ Clear</button>
      </div>

      {showFilters && (
        <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D] flex flex-wrap items-center gap-2">
          <select value={selectedCategoryFilter} onChange={(e) => setSelectedCategoryFilter(e.target.value)} className="px-2 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white">
            {categories.map((c) => (<option key={c} value={c}>{c}</option>))}
          </select>
          <select value={selectedTypeFilter} onChange={(e) => setSelectedTypeFilter(e.target.value)} className="px-2 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white">
            {types.map((t) => (<option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>))}
          </select>
          <input type="number" placeholder="Min Conf" value={confidenceMin} onChange={(e) => setConfidenceMin(Number(e.target.value))} className="w-20 px-2 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78]" />
          <input type="date" value={dateRange.start} onChange={(e) => setDateRange(prev => ({ ...prev, start: e.target.value }))} className="px-2 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white" />
          <input type="date" value={dateRange.end} onChange={(e) => setDateRange(prev => ({ ...prev, end: e.target.value }))} className="px-2 py-1.5 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white" />
        </div>
      )}

      <div className="p-3 rounded-xl bg-gradient-to-r from-[#1A2530] to-[#131A22] border border-[#26313D] flex flex-col sm:flex-row items-center justify-between gap-2">
        <div className="flex items-center gap-2 flex-wrap">
          <Brain className="w-4 h-4 text-purple-400" />
          <span className="text-xs font-bold text-white">AI Enhancement</span>
          <span className="text-[10px] text-[#8D9AAA]">{aiStats.enhanced} / {aiStats.total} items enhanced</span>
          {aiStats.total > 0 && (
            <div className="w-16 h-1.5 rounded-full bg-[#26313D] overflow-hidden">
              <div className="h-full rounded-full bg-purple-500" style={{ width: `${aiStats.percentage}%` }} />
            </div>
          )}
        </div>
        <button onClick={handleEnhanceAll} disabled={isEnhancing || knowledgeList.length === 0 || !aiUsage?.enabled} className="px-3 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
          {isEnhancing ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Zap className="w-3.5 h-3.5" />}
          <span>{isEnhancing ? 'Enhancing...' : 'Enhance All'}</span>
        </button>
      </div>

      {isBulkMode && selectedIds.length > 0 && (
        <div className="p-3 rounded-xl bg-[#1A2530] border border-teal-500/30 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span className="text-xs text-white font-bold">
            {selectedIds.length} item{selectedIds.length > 1 ? 's' : ''} selected
            <button onClick={toggleSelectAll} className="ml-2 text-[#8D9AAA] hover:text-white text-[10px]">{selectedIds.length === filteredKnowledge.length ? 'Deselect All' : 'Select All'}</button>
            <button onClick={() => setSelectedIds([])} className="ml-2 text-[#8D9AAA] hover:text-white">✕</button>
          </span>
          <div className="flex flex-wrap items-center gap-2">
            <div className="flex items-center gap-1">
              <input className="px-2 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] w-24" placeholder="Tag" value={bulkTagInput} onChange={(e) => setBulkTagInput(e.target.value)} />
              <button onClick={() => handleBulkTag('add')} className="px-2 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs">Add</button>
              <button onClick={() => handleBulkTag('remove')} className="px-2 py-1 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs">Remove</button>
            </div>
            <button onClick={handleBulkDelete} className="px-3 py-1 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs">🗑️ Delete</button>
          </div>
        </div>
      )}

      <div className="p-3 rounded-xl bg-[#131A22] border border-[#26313D] flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-1.5 text-xs font-bold text-white">
          <Tag className="w-3.5 h-3.5 text-amber-400" />
          <span>Trending:</span>
        </div>
        <div className="flex flex-wrap items-center gap-1.5">
          {trendingTopics.slice(0, 10).map((t) => (<button key={t} onClick={() => setSearchFilter(t)} className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-[#0B0F14] hover:bg-blue-600 text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors">#{t}</button>))}
        </div>
        <span className="text-[10px] text-[#5F6B78] ml-auto">{filteredKnowledge.length} items</span>
      </div>

      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
        <div className="flex items-center justify-between pb-3 border-b border-[#26313D]/70">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase flex items-center gap-2">
            <Filter className="w-4 h-4 text-teal-400" />
            Knowledge ({filteredKnowledge.length})
          </h3>
        </div>

        {isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-3.5">
            {[1, 2, 3, 4].map((i) => (<div key={i} className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] animate-pulse h-24" />))}
          </div>
        )}

        {!isLoading && filteredKnowledge.length === 0 && (
          <div className="text-center py-12">
            <BookOpen className="w-12 h-12 text-[#26313D] mx-auto mb-3" />
            <p className="text-[#8D9AAA] text-sm">
              {searchFilter || selectedCategoryFilter !== 'All' || selectedTypeFilter !== 'All' || tagFilter ? 'No items match your filters.' : 'No knowledge items yet. Add your first piece of knowledge above!'}
            </p>
            {!aiUsage?.enabled && <p className="text-[11px] text-[#5F6B78] mt-2">💡 Enable AI (set DEEPSEEK_API_KEY) to automatically enhance your knowledge.</p>}
            <button onClick={clearFilters} className="mt-3 text-xs text-teal-400 hover:text-teal-300">Clear all filters</button>
          </div>
        )}

        {!isLoading && filteredKnowledge.length > 0 && (
          <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-3.5' : 'space-y-2'}>
            {pageRecords.map((item) => (
              <div key={item.id} className={`h-[340px] flex flex-col p-4 rounded-xl bg-[#1A2530] border border-[#26313D] hover:border-teal-500/40 transition-all duration-300 group ${item.ai_enhanced ? 'border-purple-500/20' : ''} ${selectedIds.includes(item.id) ? 'border-teal-500 bg-teal-500/10' : ''}`}>
                <div className="flex items-start gap-2 flex-1 min-h-0">
                  {isBulkMode && <input type="checkbox" checked={selectedIds.includes(item.id)} onChange={() => toggleSelect(item.id)} className="mt-1 w-3.5 h-3.5 accent-teal-500 cursor-pointer shrink-0" />}
                  <div className="flex-1 min-w-0 flex flex-col h-full">
                    <div className="flex items-center justify-between gap-2 flex-wrap shrink-0">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 border border-teal-500/20">{item.category.toUpperCase()}</span>
                        <StatusBadge status={item.status} />
                        <AIBadge enhanced={item.ai_enhanced} />
                      </div>
                      <div className="flex items-center gap-2">
                        <ConfidenceBar value={item.confidence} />
                        <button onClick={() => handleEdit(item)} className="text-[#8D9AAA] hover:text-white transition-colors" title="Edit"><Edit2 className="w-3.5 h-3.5" /></button>
                        <button onClick={() => handleDelete(item.id)} className="text-rose-400 hover:text-rose-300 transition-colors" title="Delete"><Trash2 className="w-3.5 h-3.5" /></button>
                      </div>
                    </div>

                    <div className="mt-2 flex-1 min-h-0 overflow-hidden">
                      <p className={`text-xs text-[#E8EDF2] leading-relaxed ${expandedItems.has(item.id) ? '' : 'line-clamp-5'}`}>{item.content}</p>
                      {item.content && item.content.length > 200 && (
                        <button
                          onClick={() => toggleExpand(item.id)}
                          className="mt-1 text-[10px] text-teal-400 hover:text-teal-300 font-bold"
                        >
                          {expandedItems.has(item.id) ? '↑ Show less' : '↓ Read more'}
                        </button>
                      )}
                    </div>

                    {item.ai_summary && (
                      <div className="mt-2 p-2 rounded-lg bg-purple-500/5 border border-purple-500/10 shrink-0">
                        <div className="flex items-center gap-1"><Sparkles className="w-3 h-3 text-purple-400" /><span className="text-[9px] text-purple-400 font-bold">AI Summary</span></div>
                        <p className="text-[10px] text-[#8D9AAA] leading-relaxed line-clamp-2">{item.ai_summary}</p>
                      </div>
                    )}

                    {item.ai_insights && item.ai_insights.length > 0 && (
                      <div className="mt-1 flex flex-wrap gap-1 shrink-0">
                        {item.ai_insights.slice(0, 2).map((insight, i) => (<span key={i} className="text-[9px] px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400 truncate max-w-full">💡 {insight}</span>))}
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-2 mt-2 border-t border-[#26313D]/60 text-[10px] text-[#5F6B78] font-mono flex-wrap gap-1 shrink-0">
                  <div className="flex items-center gap-1 flex-wrap">
                    {item.ai_tags && item.ai_tags.length > 0 ? item.ai_tags.slice(0, 3).map((tg) => (<span key={tg} className="text-purple-400/70 cursor-pointer hover:text-purple-400" onClick={() => setTagFilter(tg)}>#{tg}</span>)) : item.tags.slice(0, 3).map((tg) => (<span key={tg} className="text-[#8D9AAA] cursor-pointer hover:text-white" onClick={() => setTagFilter(tg)}>#{tg}</span>))}
                    {(item.ai_tags?.length || 0) > 3 && <span className="text-[#5F6B78]">+{(item.ai_tags?.length || 0) - 3}</span>}
                  </div>
                  <div className="flex items-center gap-3">
                    {onEnhanceWithAI && !item.ai_enhanced && aiUsage?.enabled && (
                      <button onClick={() => handleEnhanceItem(item.id)} disabled={enhanceTargetId === item.id} className="text-[9px] text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-1">
                        {enhanceTargetId === item.id ? <Loader2 className="w-3 h-3 animate-spin" /> : <Sparkles className="w-3 h-3" />}
                        AI
                      </button>
                    )}
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      <span>{item.created_at || item.createdAt ? new Date(item.created_at || item.createdAt).toLocaleDateString("id-ID", { year: "numeric", month: "short", day: "numeric" }) : "No date"}</span>
                    </div>
                    {item.source && <span className="text-[#5F6B78]">📎 {item.source}</span>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ============================================================ */}
        {/* PAGINASI                                                     */}
        {/* ============================================================ */}
        {!isLoading && filteredKnowledge.length > 0 && totalPages > 1 && (
          <div className="mt-3 p-3 rounded-xl bg-[#131A22] border border-[#26313D] flex items-center justify-between flex-wrap gap-3">
            <div className="text-[10px] text-[#8D9AAA] font-mono">
              Showing <span className="text-white font-bold">{(currentPage - 1) * pageSize + 1}</span>–<span className="text-white font-bold">{Math.min(currentPage * pageSize, filteredKnowledge.length)}</span> of <span className="text-white font-bold">{filteredKnowledge.length}</span> items
            </div>
            <div className="flex items-center gap-1">
              <button
                onClick={() => setCurrentPage(1)}
                disabled={currentPage === 1}
                className="px-2 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-[10px] text-[#8D9AAA] hover:text-white hover:border-teal-500/40 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                « First
              </button>
              <button
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="px-2 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-[10px] text-[#8D9AAA] hover:text-white hover:border-teal-500/40 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                ‹ Prev
              </button>
              {pageNumbers.map(n => (
                <button
                  key={n}
                  onClick={() => setCurrentPage(n)}
                  className={`min-w-[28px] px-2 py-1 rounded-lg border text-[10px] font-bold transition-colors ${
                    n === currentPage
                      ? 'bg-teal-600 border-teal-500 text-white'
                      : 'bg-[#0B0F14] border-[#26313D] text-[#8D9AAA] hover:text-white hover:border-teal-500/40'
                  }`}
                >
                  {n}
                </button>
              ))}
              <button
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className="px-2 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-[10px] text-[#8D9AAA] hover:text-white hover:border-teal-500/40 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                Next ›
              </button>
              <button
                onClick={() => setCurrentPage(totalPages)}
                disabled={currentPage === totalPages}
                className="px-2 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-[10px] text-[#8D9AAA] hover:text-white hover:border-teal-500/40 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                Last »
              </button>
            </div>
          </div>
        )}
      </div>

      {editingItem && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={() => setEditingItem(null)}>
          <div className="bg-[#1A2530] border border-[#26313D] rounded-2xl p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-white">✏️ Edit Knowledge</h3>
              <button onClick={() => setEditingItem(null)} className="text-[#8D9AAA] hover:text-white"><X className="w-5 h-5" /></button>
            </div>
            <div className="space-y-3">
              <div>
                <label className="text-xs text-[#8D9AAA] block mb-1">Content</label>
                <textarea rows={4} className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white focus:outline-none focus:border-teal-500" value={editingItem.content} onChange={(e) => setEditingItem({ ...editingItem, content: e.target.value })} />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-[#8D9AAA] block mb-1">Category</label>
                  <input className="w-full p-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white focus:outline-none focus:border-teal-500" value={editingItem.category} onChange={(e) => setEditingItem({ ...editingItem, category: e.target.value })} />
                </div>
                <div>
                  <label className="text-xs text-[#8D9AAA] block mb-1">Confidence (%)</label>
                  <input type="number" className="w-full p-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white focus:outline-none focus:border-teal-500" value={editingItem.confidence} onChange={(e) => setEditingItem({ ...editingItem, confidence: Number(e.target.value) })} min="0" max="100" />
                </div>
              </div>
              <div>
                <label className="text-xs text-[#8D9AAA] block mb-1">Tags (comma separated)</label>
                <input className="w-full p-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white focus:outline-none focus:border-teal-500" value={editingItem.tags.join(', ')} onChange={(e) => setEditingItem({ ...editingItem, tags: e.target.value.split(',').map(t => t.trim()).filter(Boolean) })} />
              </div>
              <button onClick={() => handleSaveEdit(editingItem.id, { content: editingItem.content, category: editingItem.category, tags: editingItem.tags, confidence: editingItem.confidence })} className="w-full py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition-colors">💾 Save Changes</button>
            </div>
          </div>
        </div>
      )}

      {showImportModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={() => setShowImportModal(false)}>
          <div className="bg-[#1A2530] border border-[#26313D] rounded-2xl p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-white">⬆️ Import Knowledge</h3>
              <button onClick={() => setShowImportModal(false)} className="text-[#8D9AAA] hover:text-white"><X className="w-5 h-5" /></button>
            </div>
            <div className="space-y-3">
              <div>
                <label className="text-xs text-[#8D9AAA] block mb-1">Paste JSON data</label>
                <textarea rows={6} className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono focus:outline-none focus:border-teal-500" placeholder='[{"content": "Your knowledge", "category": "Trading", "tags": ["tag1"]}]' value={importData} onChange={(e) => setImportData(e.target.value)} />
              </div>
              <button onClick={handleImport} className="w-full py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-colors">📥 Import</button>
            </div>
          </div>
        </div>
      )}

      {showShortcuts && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={() => setShowShortcuts(false)}>
          <div className="bg-[#1A2530] border border-[#26313D] rounded-2xl p-6 max-w-md w-full" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-white">⌨️ Keyboard Shortcuts</h3>
              <button onClick={() => setShowShortcuts(false)} className="text-[#8D9AAA] hover:text-white"><X className="w-5 h-5" /></button>
            </div>
            <div className="space-y-2 text-xs text-[#8D9AAA]">
              <div className="flex justify-between py-1 border-b border-[#26313D]/40"><span>Ctrl+K</span><span>Focus search</span></div>
              <div className="flex justify-between py-1 border-b border-[#26313D]/40"><span>Ctrl+B</span><span>Toggle bulk mode</span></div>
              <div className="flex justify-between py-1 border-b border-[#26313D]/40"><span>Ctrl+S</span><span>Show shortcuts</span></div>
              <div className="flex justify-between py-1 border-b border-[#26313D]/40"><span>ESC</span><span>Clear selection / Close modals</span></div>
              <div className="flex justify-between py-1"><span>Enter</span><span>Submit Q&A</span></div>
            </div>
          </div>
        </div>
      )}

      <div className="text-[9px] text-[#5F6B78] text-center py-2 border-t border-[#26313D]/50 flex flex-wrap items-center justify-center gap-2">
        <span>🧠 Knowledge View v1.02</span>
        <span className="w-1 h-1 rounded-full bg-[#26313D]"></span>
        <span>{knowledgeList.length} items</span>
        <span className="w-1 h-1 rounded-full bg-[#26313D]"></span>
        <span>AI {aiEnhancedItems.length > 0 ? '🟢 ENABLED' : '🟡 DISABLED'}</span>
        <span className="w-1 h-1 rounded-full bg-[#26313D]"></span>
        <button onClick={() => setShowShortcuts(true)} className="hover:text-white transition-colors">⌨️ Shortcuts</button>
        <span className="w-1 h-1 rounded-full bg-[#26313D]"></span>
        <span>{wsConnected ? '● LIVE' : '○ OFFLINE'}</span>
      </div>
    </div>
  );
};

export default KnowledgeView;
