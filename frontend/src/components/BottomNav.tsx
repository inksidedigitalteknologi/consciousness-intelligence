import React from 'react';
import { LayoutDashboard, Star, TrendingUp, Radio, Menu, Zap } from 'lucide-react';
import { NavigationPage } from '../types';

interface BottomNavProps {
  currentPage: NavigationPage;
  onPageChange: (page: NavigationPage) => void;
  onOpenMenu: () => void;
  watchlistCount: number;
}

export const BottomNav: React.FC<BottomNavProps> = ({
  currentPage,
  onPageChange,
  onOpenMenu,
  watchlistCount,
}) => {
  const navItems = [
    { id: 'Dashboard' as NavigationPage, label: 'Home', icon: LayoutDashboard },
    { id: 'Watchlist' as NavigationPage, label: 'Watchlist', icon: Star, badge: watchlistCount },
    { id: 'Market' as NavigationPage, label: 'Market', icon: TrendingUp },
    { id: 'Signals' as NavigationPage, label: 'Signals', icon: Radio },
    { id: 'Trading' as NavigationPage, label: 'Trade', icon: Zap },
  ];

  return (
    <nav
      id="mobile-bottom-nav"
      className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#0F141B]/95 backdrop-blur-md border-t border-[#26313D] px-2 py-1.5 flex items-center justify-around select-none shadow-2xl safe-area-bottom"
    >
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = currentPage === item.id;
        return (
          <button
            key={item.id}
            onClick={() => onPageChange(item.id)}
            className={`flex flex-col items-center justify-center py-1 px-2 rounded-xl transition-all cursor-pointer relative min-w-[56px] min-h-[44px] ${
              isActive
                ? 'text-blue-400 font-bold'
                : 'text-[#8D9AAA] hover:text-white'
            }`}
          >
            <div className="relative">
              <Icon className={`w-5 h-5 ${isActive ? 'text-blue-400 scale-110' : item.id === 'Watchlist' ? 'text-amber-400/80' : 'text-[#8D9AAA]'}`} />
              {item.badge !== undefined && item.badge > 0 && (
                <span className="absolute -top-1.5 -right-2 w-4 h-4 rounded-full bg-amber-500 text-black text-[9px] font-black font-mono flex items-center justify-center shadow-sm">
                  {item.badge}
                </span>
              )}
            </div>
            <span className="text-[10px] mt-0.5 tracking-tight font-sans">
              {item.label}
            </span>
          </button>
        );
      })}

      {/* Menu / All Subsystems Trigger */}
      <button
        onClick={onOpenMenu}
        className="flex flex-col items-center justify-center py-1 px-2 rounded-xl text-[#8D9AAA] hover:text-white transition-all cursor-pointer min-w-[56px] min-h-[44px]"
      >
        <Menu className="w-5 h-5 text-[#8D9AAA]" />
        <span className="text-[10px] mt-0.5 tracking-tight font-sans">More</span>
      </button>
    </nav>
  );
};
