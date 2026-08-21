import React from 'react';
import {
  LayoutDashboard,
  Brain,
  Sparkles,
  TrendingUp,
  Radio,
  GraduationCap,
  Database,
  Search,
  LineChart,
  Target,
  Sparkle,
  Activity,
  BookOpen,
  Send,
  Sliders,
  Terminal,
  Smartphone,
  ShieldCheck,
  Zap,
  Star,
  X,
} from 'lucide-react';
import { NavigationPage } from '../types';

interface SidebarProps {
  currentPage: NavigationPage;
  onPageChange: (page: NavigationPage) => void;
  engineRunning: boolean;
  learningActive: boolean;
  cycleCount: number;
  isOpen?: boolean;
  onClose?: () => void;
  watchlistCount?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentPage,
  onPageChange,
  engineRunning,
  learningActive,
  cycleCount,
  isOpen = false,
  onClose,
  watchlistCount = 0,
}) => {
  const groups = [
    {
      title: '📊 OVERVIEW',
      items: [
        { id: 'Dashboard' as NavigationPage, label: 'Dashboard', icon: LayoutDashboard },
        { id: 'Watchlist' as NavigationPage, label: 'Watchlist', icon: Star, badge: watchlistCount > 0 ? watchlistCount : undefined },
      ],
    },
    {
      title: '🧠 INTELLIGENCE',
      items: [
        { id: 'Brain' as NavigationPage, label: 'Brain Engine', icon: Brain },
        { id: 'Reflection' as NavigationPage, label: 'Cognitive Mirror', icon: Sparkle },
        { id: 'Learning' as NavigationPage, label: 'Learning Engine', icon: GraduationCap },
        { id: 'Memory' as NavigationPage, label: 'Memory Storage', icon: Database },
        { id: 'Pattern' as NavigationPage, label: 'Pattern Detector', icon: Search },
      ],
    },
    {
      title: '📈 MARKET & SIGNALS',
      items: [
        { id: 'Market' as NavigationPage, label: 'Live Tickers', icon: TrendingUp },
        { id: 'Signals' as NavigationPage, label: 'Signals Radar', icon: Radio },
        { id: 'Prediction' as NavigationPage, label: 'Predictions', icon: LineChart },
        { id: 'Decision' as NavigationPage, label: 'Decision Engine', icon: Target },
      ],
    },
    {
      title: '📚 KNOWLEDGE & HEALTH',
      items: [
        { id: 'Knowledge' as NavigationPage, label: 'Knowledge Base', icon: BookOpen },
        { id: 'Health' as NavigationPage, label: 'System Health', icon: Activity },
        { id: 'Diagnostics' as NavigationPage, label: 'Diagnostics Test', icon: ShieldCheck },
      ],
    },
    {
      title: '⚙️ CONTROL & BRIDGE',
      items: [
        { id: 'Trading' as NavigationPage, label: 'Trading Engine', icon: Zap },
        { id: 'Telegram' as NavigationPage, label: 'Telegram Alerts', icon: Send },
        { id: 'Settings' as NavigationPage, label: 'Bot Settings', icon: Sliders },
      ],
    },
  ];

  const handleItemClick = (pageId: NavigationPage) => {
    onPageChange(pageId);
    if (onClose) {
      onClose();
    }
  };

  const sidebarContent = (
    <div className="flex flex-col justify-between h-full overflow-y-auto select-none">
      <div>
        {/* Logo Section */}
        <div className="p-4 sm:p-5 border-b border-[#26313D]/60 bg-[#0B0F14]/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/20 font-black text-white text-base">
                IN
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <span className="text-white font-extrabold text-base tracking-wider">INKSIDE</span>
                  <span className="text-blue-400 font-bold text-xs px-1.5 py-0.5 rounded bg-blue-500/10 border border-blue-500/20">
                    DIGITAL
                  </span>
                </div>
                <p className="text-[10px] text-[#8D9AAA] tracking-tight font-medium">
                  COGNITIVE MIRROR ENGINE v4.4
                </p>
              </div>
            </div>

            {/* Mobile Close Button */}
            {onClose && (
              <button
                onClick={onClose}
                className="lg:hidden p-1.5 rounded-lg text-[#8D9AAA] hover:text-white hover:bg-[#1A2530] transition-colors cursor-pointer"
                title="Close Sidebar"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>

          {/* Quick Learning Status Pill */}
          <div className="mt-3.5 flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-[#131A22] border border-[#26313D]/80">
            <div className="flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full ${learningActive ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
              <span className="text-[11px] font-semibold text-[#8D9AAA]">
                LEARNING: <strong className={learningActive ? 'text-emerald-400' : 'text-amber-400'}>{learningActive ? 'ACTIVE' : 'IDLE'}</strong>
              </span>
            </div>
            <span className="text-[10px] font-mono font-bold text-[#5F6B78] bg-[#0B0F14] px-1.5 py-0.5 rounded">
              #{cycleCount}
            </span>
          </div>
        </div>

        {/* Nav Groups */}
        <nav className="p-3 space-y-4">
          {groups.map((group) => (
            <div key={group.title}>
              <div className="px-3 mb-1.5 text-[10px] font-bold tracking-wider text-[#5F6B78]">
                {group.title}
              </div>
              <div className="space-y-1">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = currentPage === item.id;
                  return (
                    <button
                      key={item.id}
                      id={`nav-btn-${item.id.toLowerCase()}`}
                      onClick={() => handleItemClick(item.id)}
                      className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-all duration-150 cursor-pointer ${
                        isActive
                          ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                          : 'text-[#8D9AAA] hover:bg-[#18212B] hover:text-white'
                      }`}
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : item.id === 'Watchlist' ? 'text-amber-400' : 'text-[#8D9AAA]'}`} />
                        <span className="truncate">{item.label}</span>
                      </div>
                      {item.badge !== undefined && (
                        <span className={`text-[10px] font-mono font-bold px-1.5 py-0.2 rounded-full ${
                          isActive ? 'bg-white text-blue-600' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        }`}>
                          {item.badge}
                        </span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </nav>
      </div>

      {/* Footer System Status */}
      <div className="p-3.5 border-t border-[#26313D] bg-[#131A22]/70">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${engineRunning ? 'bg-emerald-400' : 'bg-blue-400'}`} />
            <span className="font-bold text-[#E8EDF2] text-[11px]">
              {engineRunning ? 'ENGINE RUNNING' : 'SYSTEM ONLINE'}
            </span>
          </div>
          <span className="text-[10px] text-[#5F6B78] font-mono">v4.4.1</span>
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Persistent Sidebar */}
      <aside
        id="app-sidebar-desktop"
        className="hidden lg:flex w-64 bg-[#0F141B] border-r border-[#26313D] flex-col justify-between h-screen shrink-0 overflow-y-auto"
      >
        {sidebarContent}
      </aside>

      {/* Mobile / Tablet Drawer Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/70 backdrop-blur-xs z-50 lg:hidden flex transition-opacity animate-in fade-in"
          onClick={onClose}
        >
          <aside
            id="app-sidebar-mobile"
            className="w-72 sm:w-80 bg-[#0F141B] border-r border-[#26313D] h-full shadow-2xl overflow-y-auto animate-in slide-in-from-left duration-200"
            onClick={(e) => e.stopPropagation()}
          >
            {sidebarContent}
          </aside>
        </div>
      )}
    </>
  );
};
