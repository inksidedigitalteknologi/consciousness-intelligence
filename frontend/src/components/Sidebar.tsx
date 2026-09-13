// src/components/Sidebar.tsx
// INKSIDE DIGITAL — Collapsible Sidebar (preserves original API)

import React, { useMemo, useState, useCallback, useEffect } from 'react';
import {
  LayoutDashboard,
  Brain,
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
  ShieldCheck,
  Zap,
  Star,
  X,
  Wifi,
  WifiOff,
  ChevronDown,
  ChevronRight,
  PanelLeftClose,
  PanelLeftOpen,
} from 'lucide-react';
import { NavigationPage } from '../types';

// ============================================================
// TYPES
// ============================================================

interface SidebarProps {
  currentPage: NavigationPage;
  onPageChange: (page: NavigationPage) => void;
  engineRunning: boolean;
  learningActive: boolean;
  cycleCount: number;
  isOpen?: boolean;
  onClose?: () => void;
  watchlistCount?: number;
  wsConnected?: boolean;
  wsStatus?: string;
  healthScore?: number;
  version?: string;
}

interface NavItem {
  id: NavigationPage;
  label: string;
  icon: React.ElementType;
  badge?: number | string;
  isNew?: boolean;
  isBeta?: boolean;
}

interface NavGroup {
  title: string;
  icon?: React.ElementType;
  items: NavItem[];
  collapsible?: boolean;
}

// ============================================================
// HELPERS
// ============================================================

const getHealthColor = (score: number): string => {
  if (score >= 80) return 'text-emerald-400';
  if (score >= 60) return 'text-amber-400';
  if (score >= 40) return 'text-orange-400';
  return 'text-red-400';
};

const getHealthBg = (score: number): string => {
  if (score >= 80) return 'bg-emerald-400';
  if (score >= 60) return 'bg-amber-400';
  if (score >= 40) return 'bg-orange-400';
  return 'bg-red-400';
};

const LS_KEY = 'inkside.sidebar.collapsed';

// ============================================================
// SIDEBAR COMPONENT
// ============================================================

export const Sidebar: React.FC<SidebarProps> = ({
  currentPage,
  onPageChange,
  engineRunning,
  learningActive,
  cycleCount,
  isOpen = false,
  onClose,
  watchlistCount = 0,
  wsConnected = false,
  wsStatus = 'disconnected',
  healthScore = 100,
  version = '4.4.1',
}) => {
  // ============================================================
  // STATE
  // ============================================================

  const [collapsed, setCollapsed] = useState<boolean>(() => {
    try {
      return localStorage.getItem(LS_KEY) === 'true';
    } catch {
      return false;
    }
  });

  const [collapsedGroups, setCollapsedGroups] = useState<Record<string, boolean>>({
    '📊 OVERVIEW': false,
    '🧠 INTELLIGENCE': false,
    '📈 MARKET & SIGNALS': false,
    '📚 KNOWLEDGE & HEALTH': false,
    '⚙️ CONTROL & BRIDGE': false,
  });

  useEffect(() => {
    try {
      localStorage.setItem(LS_KEY, String(collapsed));
    } catch {
      /* ignore */
    }
  }, [collapsed]);

  const toggleCollapsed = useCallback(() => {
    setCollapsed((c) => !c);
  }, []);

  // ============================================================
  // NAVIGATION GROUPS
  // ============================================================

  const groups: NavGroup[] = useMemo(() => [
    {
      title: '📊 OVERVIEW',
      icon: LayoutDashboard,
      items: [
        { id: 'Dashboard' as NavigationPage, label: 'Dashboard', icon: LayoutDashboard },
        { id: 'Watchlist' as NavigationPage, label: 'Watchlist', icon: Star, badge: watchlistCount > 0 ? watchlistCount : undefined },
      ],
    },
    {
      title: '🧠 INTELLIGENCE',
      icon: Brain,
      collapsible: true,
      items: [
        { id: 'Brain' as NavigationPage, label: 'Brain Engine', icon: Brain },
        { id: 'Reflection' as NavigationPage, label: 'Cognitive Mirror', icon: Sparkle },
        { id: 'Learning' as NavigationPage, label: 'Learning Engine', icon: GraduationCap, isBeta: true },
        { id: 'Memory' as NavigationPage, label: 'Memory Storage', icon: Database },
        { id: 'Pattern' as NavigationPage, label: 'Pattern Detector', icon: Search, isNew: true },
      ],
    },
    {
      title: '📈 MARKET & SIGNALS',
      icon: TrendingUp,
      collapsible: true,
      items: [
        { id: 'Market' as NavigationPage, label: 'Live Tickers', icon: TrendingUp },
        { id: 'MarketQuotes' as NavigationPage, label: 'S&P 500 Quotes', icon: TrendingUp, isNew: true },
        { id: 'Signals' as NavigationPage, label: 'Signals Radar', icon: Radio, isNew: true },
        { id: 'Prediction' as NavigationPage, label: 'Predictions', icon: LineChart, isBeta: true },
        { id: 'Decision' as NavigationPage, label: 'Decision Engine', icon: Target },
      ],
    },
    {
      title: '📚 KNOWLEDGE & HEALTH',
      icon: BookOpen,
      collapsible: true,
      items: [
        { id: 'Knowledge' as NavigationPage, label: 'Knowledge Base', icon: BookOpen },
        { id: 'Health' as NavigationPage, label: 'System Health', icon: Activity },
        { id: 'Diagnostics' as NavigationPage, label: 'Diagnostics', icon: ShieldCheck },
      ],
    },
    {
      title: '🌐 IOT & DEVICES',
      icon: Radio,
      collapsible: true,
      items: [
        { id: 'IoT' as NavigationPage, label: 'IoT Devices', icon: Radio, isNew: true },
      ],
    },
    {
      title: '⚙️ CONTROL & BRIDGE',
      icon: Sliders,
      collapsible: true,
      items: [
        { id: 'Trading' as NavigationPage, label: 'Trading Engine', icon: Zap },
        { id: 'Telegram' as NavigationPage, label: 'Telegram Alerts', icon: Send },
        { id: 'Settings' as NavigationPage, label: 'Settings', icon: Sliders },
      ],
    },
  ], [watchlistCount]);

  // ============================================================
  // HANDLERS
  // ============================================================

  const handleItemClick = useCallback((pageId: NavigationPage) => {
    onPageChange(pageId);
    if (onClose) onClose();
  }, [onPageChange, onClose]);

  const toggleGroup = useCallback((title: string) => {
    setCollapsedGroups((prev) => ({
      ...prev,
      [title]: !prev[title],
    }));
  }, []);

  // ============================================================
  // RENDER HELPERS
  // ============================================================

  const renderNavItem = (item: NavItem, isActive: boolean) => {
    const Icon = item.icon;
    return (
      <button
        key={item.id}
        id={`nav-btn-${item.id.toLowerCase()}`}
        onClick={() => handleItemClick(item.id)}
        title={collapsed ? item.label : undefined}
        className={`w-full flex items-center rounded-lg text-xs font-semibold transition-all duration-200 cursor-pointer group relative ${
          collapsed ? 'justify-center px-0 py-2.5' : 'justify-between px-3 py-2'
        } ${
          isActive
            ? 'bg-gradient-to-r from-blue-600/80 to-blue-600/40 text-white shadow-lg shadow-blue-600/20'
            : 'text-[#8D9AAA] hover:bg-[#18212B] hover:text-white'
        }`}
      >
        <div className={`flex items-center gap-3 min-w-0 ${collapsed ? '' : 'flex-1'}`}>
          <Icon className={`w-4 h-4 shrink-0 transition-colors ${
            isActive ? 'text-white' : 'text-[#8D9AAA] group-hover:text-white'
          }`} />

          {!collapsed && (
            <>
              <span className="truncate text-[11px]">{item.label}</span>

              {item.isNew && (
                <span className="text-[8px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/30 text-emerald-300 border border-emerald-500/20">
                  NEW
                </span>
              )}
              {item.isBeta && (
                <span className="text-[8px] font-bold px-1.5 py-0.5 rounded bg-amber-500/30 text-amber-300 border border-amber-500/20">
                  BETA
                </span>
              )}
            </>
          )}
        </div>

        {!collapsed && item.badge !== undefined && (
          <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded-full ${
            isActive
              ? 'bg-white/20 text-white'
              : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
          }`}>
            {item.badge}
          </span>
        )}

        {/* Active indicator (collapsed mode) */}
        {collapsed && isActive && (
          <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-blue-400 rounded-r-full" />
        )}
      </button>
    );
  };

  // ============================================================
  // SIDEBAR CONTENT
  // ============================================================

  const sidebarContent = (
    <div className="flex flex-col justify-between h-full overflow-y-auto select-none">
      {/* HEADER */}
      <div>
        <div className={`border-b border-[#26313D]/60 bg-gradient-to-b from-[#0B0F14] to-transparent ${collapsed ? 'p-3' : 'p-4 sm:p-5'}`}>
          <div className="flex items-center justify-between gap-2">
            {!collapsed ? (
              <div className="flex items-center gap-2.5 min-w-0">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/20 font-black text-white text-base shrink-0">
                  IN
                </div>
                <div className="min-w-0">
                  <div className="flex items-center gap-1.5">
                    <span className="text-white font-extrabold text-base tracking-wider">INKSIDE</span>
                    <span className="text-blue-400 font-bold text-[10px] px-1.5 py-0.5 rounded bg-blue-500/10 border border-blue-500/20">
                      DIGITAL
                    </span>
                  </div>
                  <p className="text-[10px] text-[#8D9AAA] tracking-tight font-medium truncate">
                    COGNITIVE MIRROR ENGINE
                  </p>
                </div>
              </div>
            ) : (
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/20 font-black text-white text-base mx-auto">
                IN
              </div>
            )}

            {onClose && !collapsed && (
              <button
                onClick={onClose}
                className="lg:hidden p-1.5 rounded-lg text-[#8D9AAA] hover:text-white hover:bg-[#1A2530] transition-colors cursor-pointer"
                title="Close Sidebar"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>

          {/* COLLAPSE TOGGLE (desktop only) */}
          <button
            onClick={toggleCollapsed}
            className={`hidden lg:flex mt-3 w-full items-center justify-center gap-1.5 py-1.5 rounded-lg bg-[#131A22] hover:bg-[#1A2530] text-[#8D9AAA] hover:text-white border border-[#26313D]/80 transition-all cursor-pointer ${
              collapsed ? 'px-0' : 'px-2.5'
            }`}
            title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {collapsed ? (
              <PanelLeftOpen className="w-3.5 h-3.5" />
            ) : (
              <>
                <PanelLeftClose className="w-3.5 h-3.5" />
                <span className="text-[10px] font-semibold">Collapse</span>
              </>
            )}
          </button>

          {/* STATUS PILLS */}
          {!collapsed && (
            <div className="mt-3.5 grid grid-cols-2 gap-1.5">
              <div className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-[#131A22] border border-[#26313D]/80">
                <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${learningActive ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
                  <span className="text-[10px] font-semibold text-[#8D9AAA]">
                    {learningActive ? 'LEARNING' : 'IDLE'}
                  </span>
                </div>
                <span className="text-[9px] font-mono font-bold text-[#5F6B78] bg-[#0B0F14] px-1.5 py-0.5 rounded">
                  #{cycleCount}
                </span>
              </div>

              <div className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-[#131A22] border border-[#26313D]/80">
                <div className="flex items-center gap-2">
                  {wsConnected ? (
                    <Wifi className="w-3 h-3 text-emerald-400" />
                  ) : (
                    <WifiOff className="w-3 h-3 text-rose-400" />
                  )}
                  <span className="text-[10px] font-semibold text-[#8D9AAA]">
                    {wsConnected ? 'LIVE' : 'OFFLINE'}
                  </span>
                </div>
                <span className="text-[9px] font-mono font-bold text-[#5F6B78] bg-[#0B0F14] px-1.5 py-0.5 rounded">
                  WS
                </span>
              </div>
            </div>
          )}

          {/* COLLAPSED STATUS DOTS */}
          {collapsed && (
            <div className="mt-3 flex flex-col items-center gap-1.5">
              <span
                className={`w-2.5 h-2.5 rounded-full ${learningActive ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}
                title={learningActive ? 'Learning active' : 'Idle'}
              />
              {wsConnected ? (
                <Wifi className="w-3 h-3 text-emerald-400" title="WebSocket connected" />
              ) : (
                <WifiOff className="w-3 h-3 text-rose-400" title="WebSocket offline" />
              )}
            </div>
          )}
        </div>

        {/* NAVIGATION */}
        <nav className={`${collapsed ? 'p-2' : 'p-3'} space-y-3`}>
          {groups.map((group) => {
            const isCollapsed = collapsedGroups[group.title] || false;
            const isActiveGroup = group.items.some((item) => item.id === currentPage);

            return (
              <div key={group.title}>
                {/* Group Header */}
                {!collapsed ? (
                  <div
                    className={`flex items-center justify-between px-3 py-1.5 rounded-lg cursor-pointer transition-colors ${
                      isActiveGroup ? 'bg-blue-600/10' : 'hover:bg-[#131A22]'
                    }`}
                    onClick={() => group.collapsible && toggleGroup(group.title)}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-bold tracking-wider text-[#5F6B78] uppercase">
                        {group.title}
                      </span>
                    </div>
                    {group.collapsible && (
                      <button className="text-[#5F6B78] hover:text-white">
                        {isCollapsed ? (
                          <ChevronRight className="w-3.5 h-3.5" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5" />
                        )}
                      </button>
                    )}
                  </div>
                ) : (
                  <div className="h-px bg-[#26313D]/60 my-2 mx-1" />
                )}

                {/* Group Items */}
                {(!isCollapsed || collapsed) && (
                  <div className={`mt-1 space-y-0.5 ${collapsed ? '' : 'pl-1'}`}>
                    {group.items.map((item) => {
                      const isActive = currentPage === item.id;
                      return renderNavItem(item, isActive);
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
      </div>

      {/* FOOTER */}
      <div className={`border-t border-[#26313D] bg-[#131A22]/70 ${collapsed ? 'p-2' : 'p-3.5'} space-y-2`}>
        {!collapsed ? (
          <>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className={`w-2.5 h-2.5 rounded-full ${engineRunning ? 'bg-emerald-400 animate-pulse' : 'bg-blue-400'}`} />
                <span className="font-bold text-[11px] text-[#E8EDF2]">
                  {engineRunning ? 'ENGINE RUNNING' : 'SYSTEM ONLINE'}
                </span>
              </div>
              <span className="text-[9px] text-[#5F6B78] font-mono">v{version}</span>
            </div>

            <div className="flex items-center gap-2">
              <div className="flex-1 h-1.5 bg-[#1A2530] rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${getHealthBg(healthScore)}`}
                  style={{ width: `${Math.min(100, Math.max(0, healthScore))}%` }}
                />
              </div>
              <span className={`text-[9px] font-bold ${getHealthColor(healthScore)}`}>
                {Math.round(healthScore)}%
              </span>
            </div>
          </>
        ) : (
          <div className="flex flex-col items-center gap-1.5" title={`Health: ${Math.round(healthScore)}% · Engine: ${engineRunning ? 'Running' : 'Online'}`}>
            <span className={`w-2.5 h-2.5 rounded-full ${engineRunning ? 'bg-emerald-400 animate-pulse' : 'bg-blue-400'}`} />
            <span className={`text-[9px] font-bold ${getHealthColor(healthScore)}`}>
              {Math.round(healthScore)}%
            </span>
          </div>
        )}
      </div>
    </div>
  );

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <>
      {/* Desktop Sidebar */}
      <aside
        id="app-sidebar-desktop"
        className={`hidden lg:flex bg-[#131A22] border-r border-[#26313D] flex-col justify-between h-screen shrink-0 overflow-y-auto transition-all duration-300 ease-in-out ${
          collapsed ? 'w-16' : 'w-64'
        }`}
      >
        {sidebarContent}
      </aside>

      {/* Mobile Drawer (always expanded) */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 lg:hidden flex transition-opacity animate-in fade-in duration-200"
          onClick={onClose}
        >
          <aside
            id="app-sidebar-mobile"
            className="w-72 sm:w-80 bg-[#131A22] border-r border-[#26313D] h-full shadow-2xl overflow-y-auto animate-in slide-in-from-left duration-300"
            onClick={(e) => e.stopPropagation()}
          >
            {sidebarContent}
          </aside>
        </div>
      )}
    </>
  );
};

export default Sidebar;
