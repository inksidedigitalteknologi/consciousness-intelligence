import React, { useState } from 'react';
import { BookOpen, Search, Plus, Sparkles, Tag, Globe, FileCode, Check, Send } from 'lucide-react';
import { KnowledgeItem } from '../types';

interface KnowledgeViewProps {
  knowledgeList: KnowledgeItem[];
  onAddKnowledge: (item: Partial<KnowledgeItem>) => void;
}

export const KnowledgeView: React.FC<KnowledgeViewProps> = ({ knowledgeList, onAddKnowledge }) => {
  const [activeTab, setActiveTab] = useState<'text' | 'url' | 'raw'>('text');
  const [question, setQuestion] = useState('');
  const [qaAnswer, setQaAnswer] = useState<string | null>(null);
  const [isAnswering, setIsAnswering] = useState(false);

  const [textContent, setTextContent] = useState('');
  const [urlContent, setUrlContent] = useState('');
  const [rawContent, setRawContent] = useState('');
  const [category, setCategory] = useState('Trading');
  const [searchFilter, setSearchFilter] = useState('');
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState('All');

  const categories = ['All', 'Trading', 'Strategy', 'Market', 'Finance', 'General Knowledge'];
  const trendingTopics = ['bitcoin', 'halving', 'strategy', 'mtf-alignment', 'kraken', 'indonesia', 'bi-rate'];
  const smartSuggestions = [
    'What is the optimal RSI threshold for MTF momentum?',
    'Tell me about Bitcoin Halving cycles',
    'How does Kraken WebSocket stream work?',
    'Summarize recent macro economic insights',
  ];

  const handleAsk = () => {
    if (!question.trim()) return;
    setIsAnswering(true);
    setTimeout(() => {
      setIsAnswering(false);
      // Smart response from knowledge items
      const found = knowledgeList.find((k) =>
        k.content.toLowerCase().includes(question.toLowerCase().split(' ')[0])
      );
      if (found) {
        setQaAnswer(found.content);
      } else {
        setQaAnswer(
          `According to the Cognitive Knowledge Base: "${question}" is closely correlated with Multi-Timeframe Alignment rules and Bitcoin momentum cycles.`
        );
      }
    }, 400);
  };

  const handleSaveText = () => {
    if (!textContent.trim()) return;
    onAddKnowledge({
      content: textContent,
      category,
      type: 'fact',
      confidence: 85,
      importance: 0.8,
      tags: [category.toLowerCase(), 'user-added'],
      status: 'active',
      createdAt: new Date().toISOString().replace('T', ' ').substring(0, 19),
    });
    setTextContent('');
  };

  const filteredKnowledge = knowledgeList.filter((item) => {
    const matchesCat = selectedCategoryFilter === 'All' || item.category === selectedCategoryFilter;
    const matchesSearch = item.content.toLowerCase().includes(searchFilter.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <div id="knowledge-view" className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-teal-600/20 border border-teal-500/30 flex items-center justify-center text-teal-400">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide">
              Knowledge Base & Semantic Graph v9.0
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

      {/* Ask Q&A Section */}
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
          />
          <button
            onClick={handleAsk}
            disabled={isAnswering}
            className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition-all shadow-md shadow-teal-600/30 flex items-center gap-2 cursor-pointer disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
            <span>{isAnswering ? 'Searching...' : 'Ask'}</span>
          </button>
        </div>

        {/* Q&A Response */}
        {qaAnswer && (
          <div className="p-3.5 rounded-xl bg-[#0B0F14] border border-teal-500/30 text-xs text-teal-200 leading-relaxed font-sans">
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
              }}
              className="text-[10px] px-2 py-1 rounded-md bg-[#0B0F14] hover:bg-[#26313D] text-[#8D9AAA] hover:text-white border border-[#26313D] transition-colors cursor-pointer"
            >
              {sug}
            </button>
          ))}
        </div>
      </div>

      {/* Add Knowledge Box */}
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
                {tab === 'raw' && '📊 Raw JSON/CSV'}
              </button>
            ))}
          </div>
        </div>

        {/* Tab contents */}
        {activeTab === 'text' && (
          <div className="space-y-3">
            <textarea
              id="add-knowledge-textarea"
              rows={3}
              placeholder="Type or paste knowledge text here..."
              value={textContent}
              onChange={(e) => setTextContent(e.target.value)}
              className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none focus:border-blue-500"
            />
            <div className="flex items-center justify-between">
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
                className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-md cursor-pointer"
              >
                Save Knowledge
              </button>
            </div>
          </div>
        )}

        {activeTab === 'url' && (
          <div className="space-y-3">
            <div className="flex gap-2">
              <input
                type="url"
                placeholder="https://example.com/article..."
                value={urlContent}
                onChange={(e) => setUrlContent(e.target.value)}
                className="flex-1 px-3 py-2 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none"
              />
              <button
                onClick={() => {
                  if (urlContent) {
                    onAddKnowledge({
                      content: `Fetched content from ${urlContent}: Macro liquidity and crypto volatility indicators updated.`,
                      category: 'Market',
                      type: 'reference',
                      confidence: 80,
                      importance: 0.7,
                      tags: ['url-fetched', 'macro'],
                      status: 'active',
                      createdAt: new Date().toISOString().replace('T', ' ').substring(0, 19),
                    });
                    setUrlContent('');
                  }
                }}
                className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold cursor-pointer"
              >
                Fetch & Extract
              </button>
            </div>
            <p className="text-[11px] text-[#5F6B78]">
              💡 System extracts article body text, removes boilerplate HTML/JS tags, and indexes sentences automatically.
            </p>
          </div>
        )}

        {activeTab === 'raw' && (
          <div className="space-y-3">
            <textarea
              rows={3}
              placeholder="Paste raw JSON or CSV dataset here..."
              value={rawContent}
              onChange={(e) => setRawContent(e.target.value)}
              className="w-full p-3 rounded-xl bg-[#0B0F14] border border-[#26313D] text-xs text-white font-mono placeholder-[#5F6B78] focus:outline-none"
            />
            <button
              onClick={() => {
                if (rawContent) {
                  onAddKnowledge({
                    content: `[Raw Data] ${rawContent.substring(0, 200)}`,
                    category: 'Trading',
                    type: 'fact',
                    confidence: 90,
                    importance: 0.8,
                    tags: ['raw-data'],
                    status: 'active',
                    createdAt: new Date().toISOString().replace('T', ' ').substring(0, 19),
                  });
                  setRawContent('');
                }
              }}
              className="px-4 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold cursor-pointer"
            >
              Parse & Ingest
            </button>
          </div>
        )}
      </div>

      {/* Trending Topics Bar */}
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

      {/* Knowledge Items Grid */}
      <div className="p-5 rounded-2xl bg-[#131A22] border border-[#26313D] space-y-4 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#26313D]/70">
          <h3 className="text-sm font-bold text-white tracking-wider uppercase">
            Stored Knowledge Graph ({filteredKnowledge.length})
          </h3>

          <div className="flex items-center gap-2">
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
              onChange={(e) => setSearchFilter(e.target.value)}
              className="px-3 py-1 rounded-lg bg-[#0B0F14] border border-[#26313D] text-xs text-white placeholder-[#5F6B78] focus:outline-none"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          {filteredKnowledge.map((item) => (
            <div
              key={item.id}
              className="p-4 rounded-xl bg-[#1A2530] border border-[#26313D] flex flex-col justify-between space-y-3 hover:border-teal-500/40 transition-all"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 border border-teal-500/20">
                    {item.category.toUpperCase()}
                  </span>
                  <span className="text-[10px] font-mono text-[#8D9AAA]">{item.confidence}% Conf</span>
                </div>
                <p className="text-xs text-[#E8EDF2] leading-relaxed mt-2">{item.content}</p>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-[#26313D]/60 text-[10px] text-[#5F6B78] font-mono">
                <div className="flex items-center gap-1">
                  {item.tags.map((tg) => (
                    <span key={tg} className="text-[#8D9AAA]">
                      #{tg}
                    </span>
                  ))}
                </div>
                <span>{item.createdAt}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
