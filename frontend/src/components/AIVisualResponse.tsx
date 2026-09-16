/**
 * AIVisualResponse — render AI response sebagai kartu visual
 */
import React from 'react';
import {
  Sparkles, TrendingUp, Lightbulb,
  Target, MapPin, Clock, ExternalLink, ChevronRight
} from 'lucide-react';

export interface AIMetric {
  label: string;
  value: string;
  color?: 'green' | 'red' | 'yellow' | 'blue' | 'purple';
}

export interface AISection {
  heading: string;
  type: 'list' | 'text' | 'steps' | 'quote';
  items?: string[];
  content?: string;
}

export interface AIResponse {
  title: string;
  summary: string;
  sections: AISection[];
  metrics: AIMetric[];
  actions: string[];
  follow_up_questions: string[];
  confidence: number;
  question_type?: string;
  sources_used?: boolean;
  kb_items_count?: number;
}

interface Props {
  response: AIResponse;
  onFollowUp?: (q: string) => void;
}

const colorMap: Record<string, string> = {
  green: 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10',
  red: 'text-rose-400 border-rose-500/30 bg-rose-500/10',
  yellow: 'text-amber-400 border-amber-500/30 bg-amber-500/10',
  blue: 'text-blue-400 border-blue-500/30 bg-blue-500/10',
  purple: 'text-purple-400 border-purple-500/30 bg-purple-500/10',
};

const typeIcon: Record<string, React.ReactNode> = {
  definition: <Lightbulb className="w-3.5 h-3.5" />,
  general: <Sparkles className="w-3.5 h-3.5" />,
  recipe: <Target className="w-3.5 h-3.5" />,
  location: <MapPin className="w-3.5 h-3.5" />,
  how_to: <Target className="w-3.5 h-3.5" />,
  comparison: <TrendingUp className="w-3.5 h-3.5" />,
  analysis: <TrendingUp className="w-3.5 h-3.5" />,
  realtime: <Clock className="w-3.5 h-3.5" />,
  knowledge_base: <Sparkles className="w-3.5 h-3.5" />,
  creative: <Sparkles className="w-3.5 h-3.5" />,
};

export const AIVisualResponse: React.FC<Props> = ({ response, onFollowUp }) => {
  const confidence = Math.round((response.confidence || 0.7) * 100);

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex items-start justify-between gap-3 pb-3 border-b border-teal-500/20">
        <div className="flex items-start gap-2 flex-1">
          <div className="p-2 rounded-lg bg-teal-500/10 border border-teal-500/30 text-teal-400">
            {typeIcon[response.question_type || 'general'] || <Sparkles className="w-3.5 h-3.5" />}
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">{response.title || 'Jawaban AI'}</h3>
            {response.question_type && (
              <span className="text-[9px] text-[#5F6B78] uppercase tracking-wider font-bold">
                {response.question_type.replace('_', ' ')}
              </span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2 text-[10px] text-[#8D9AAA]">
          {response.sources_used && (
            <span className="px-2 py-0.5 rounded bg-purple-500/10 border border-purple-500/20 text-purple-300">
              KB {response.kb_items_count || 0}
            </span>
          )}
          <span className={`px-2 py-0.5 rounded border font-bold ${
            confidence > 80 ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20' :
            confidence > 60 ? 'bg-amber-500/10 text-amber-300 border-amber-500/20' :
            'bg-rose-500/10 text-rose-300 border-rose-500/20'
          }`}>
            {confidence}%
          </span>
        </div>
      </div>

      {response.summary && (
        <div className="text-sm text-[#E8EDF2] leading-relaxed font-sans">
          {response.summary}
        </div>
      )}

      {response.metrics && response.metrics.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
          {response.metrics.map((m, i) => {
            const color = colorMap[m.color || 'blue'] || colorMap.blue;
            return (
              <div key={i} className={`p-2.5 rounded-lg border ${color}`}>
                <div className="text-[9px] uppercase font-bold opacity-80 tracking-wider">
                  {m.label}
                </div>
                <div className="text-sm font-bold font-mono mt-0.5">
                  {m.value}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {response.sections && response.sections.map((sec, i) => (
        <div key={i} className="space-y-2">
          <h4 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span className="w-1 h-3 bg-teal-400 rounded-full"></span>
            {sec.heading}
          </h4>

          {sec.type === 'text' && sec.content && (
            <p className="text-xs text-[#8D9AAA] leading-relaxed pl-3">
              {sec.content}
            </p>
          )}

          {(sec.type === 'list' || sec.type === 'steps') && sec.items && (
            <ul className="space-y-1.5 pl-3">
              {sec.items.map((item, j) => (
                <li key={j} className="text-xs text-[#8D9AAA] leading-relaxed flex items-start gap-2">
                  {sec.type === 'steps' ? (
                    <span className="flex-shrink-0 w-4 h-4 rounded-full bg-teal-500/20 text-teal-300 text-[9px] font-bold flex items-center justify-center mt-0.5">
                      {j + 1}
                    </span>
                  ) : (
                    <span className="flex-shrink-0 text-teal-400 mt-1">▸</span>
                  )}
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          )}

          {sec.type === 'quote' && sec.content && (
            <blockquote className="border-l-2 border-teal-400 pl-3 italic text-xs text-[#8D9AAA]">
              {sec.content}
            </blockquote>
          )}
        </div>
      ))}

      {response.actions && response.actions.length > 0 && (
        <div className="p-3 rounded-lg bg-amber-500/5 border border-amber-500/20">
          <div className="flex items-center gap-1.5 mb-2">
            <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
            <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider">
              Saran / Action
            </span>
          </div>
          <ul className="space-y-1">
            {response.actions.map((a, i) => (
              <li key={i} className="text-xs text-amber-100/90 flex items-start gap-2">
                <ChevronRight className="w-3 h-3 flex-shrink-0 mt-0.5 text-amber-400" />
                <span>{a}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {response.follow_up_questions && response.follow_up_questions.length > 0 && onFollowUp && (
        <div className="pt-2 border-t border-[#26313D]/60">
          <div className="text-[9px] text-[#5F6B78] uppercase font-bold mb-2 tracking-wider">
            Tanya lanjutan
          </div>
          <div className="flex flex-wrap gap-1.5">
            {response.follow_up_questions.map((q, i) => (
              <button
                key={i}
                onClick={() => onFollowUp(q)}
                className="text-[10px] px-2.5 py-1 rounded-full bg-[#0B0F14] hover:bg-teal-500/10 border border-[#26313D] hover:border-teal-500/40 text-[#8D9AAA] hover:text-teal-300 transition-colors flex items-center gap-1"
              >
                <ExternalLink className="w-2.5 h-2.5" />
                {q}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AIVisualResponse;
