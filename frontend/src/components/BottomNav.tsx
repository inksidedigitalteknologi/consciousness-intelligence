// src/components/BottomNav.tsx
// INKSIDE DIGITAL - BOTTOM NAVIGATION v2.0
// FIX: Error Boundary, Logging, Type Safety, Performance

import React, { useMemo, useCallback, memo } from 'react';
import { 
  LayoutDashboard, 
  Star, 
  TrendingUp, 
  Radio, 
  Menu, 
  Zap,
  AlertCircle,
  Wifi,
  WifiOff,
  Activity
} from 'lucide-react';
import { NavigationPage } from '../types';

// ============================================================
// TYPES
// ============================================================

interface BottomNavProps {
  currentPage: NavigationPage;
  onPageChange: (page: NavigationPage) => void;
  onOpenMenu: () => void;
  watchlistCount: number;
  engineRunning?: boolean;
  wsConnected?: boolean;
  healthScore?: number;
}

interface NavItem {
  id: NavigationPage;
  label: string;
  icon: React.ElementType;
  badge?: number;
}

// ============================================================
// LOGGER
// ============================================================

const LOG_PREFIX = '[BottomNav]';

const log = {
  info: (message: string, data?: any) => {
    console.info(`${LOG_PREFIX} ${message}`, data || '');
  },
  warn: (message: string, data?: any) => {
    console.warn(`${LOG_PREFIX} ⚠️ ${message}`, data || '');
  },
  error: (message: string, error?: any) => {
    console.error(`${LOG_PREFIX} ❌ ${message}`, error || '');
  },
  debug: (message: string, data?: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`${LOG_PREFIX} ${message}`, data || '');
    }
  }
};

// ============================================================
// ERROR BOUNDARY
// ============================================================

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: React.ErrorInfo | null;
}

class BottomNavErrorBoundary extends React.Component<
  { children: React.ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    log.error('Error Boundary caught error:', error);
    return { hasError: true, error, errorInfo: null };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    log.error('Component Error:', { error, errorInfo });
    this.setState({ error, errorInfo });
    
    // Optional: Send to error tracking service
    if (window.errorTracker) {
      window.errorTracker.captureError(error, { component: 'BottomNav', errorInfo });
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div 
          className="fixed bottom-0 left-0 right-0 z-40 bg-[#0F141B]/95 backdrop-blur-md border-t border-rose-500/30 px-4 py-3 flex items-center gap-3"
          role="alert"
        >
          <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-rose-400 font-medium">Navigation Error</p>
            <p className="text-[10px] text-[#8D9AAA] truncate">
              {this.state.error?.message || 'Unknown error occurred'}
            </p>
          </div>
          <button
            onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
            className="px-3 py-1 rounded-lg bg-rose-500/20 text-rose-400 text-xs hover:bg-rose-500/30 transition-colors"
          >
            Retry
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// ============================================================
// NAV ITEM COMPONENT (memoized)
// ============================================================

interface NavItemProps {
  item: NavItem;
  isActive: boolean;
  onClick: () => void;
  engineRunning?: boolean;
}

const NavItemComponent = memo(({ item, isActive, onClick, engineRunning }: NavItemProps) => {
  const Icon = item.icon;
  
  const handleClick = useCallback(() => {
    try {
      log.debug(`Navigating to: ${item.id}`);
      onClick();
    } catch (error) {
      log.error(`Failed to navigate to ${item.id}:`, error);
    }
  }, [onClick, item.id]);

  return (
    <button
      onClick={handleClick}
      className={`
        flex flex-col items-center justify-center py-1 px-2 rounded-xl 
        transition-all duration-200 cursor-pointer relative min-w-[56px] min-h-[44px]
        ${isActive 
          ? 'text-blue-400 font-bold scale-105' 
          : 'text-[#8D9AAA] hover:text-white hover:bg-[#1A2530]'
        }
        focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:ring-offset-2 focus:ring-offset-[#0F141B]
        active:scale-95
      `}
      aria-label={`${item.label}${isActive ? ' (active)' : ''}`}
      aria-current={isActive ? 'page' : undefined}
    >
      <div className="relative">
        <Icon className={`w-5 h-5 transition-transform duration-200 ${isActive ? 'scale-110' : ''}`} />
        {item.badge !== undefined && item.badge > 0 && (
          <span 
            className="absolute -top-1.5 -right-2 w-4 h-4 rounded-full bg-amber-500 text-black text-[9px] font-black font-mono flex items-center justify-center animate-pulse"
            aria-label={`${item.badge} items`}
          >
            {item.badge > 99 ? '99+' : item.badge}
          </span>
        )}
      </div>
      <span className="text-[10px] mt-0.5 tracking-tight font-sans">{item.label}</span>
    </button>
  );
});

NavItemComponent.displayName = 'NavItem';

// ============================================================
// MAIN COMPONENT
// ============================================================

export const BottomNav: React.FC<BottomNavProps> = ({
  currentPage,
  onPageChange,
  onOpenMenu,
  watchlistCount,
  engineRunning = false,
  wsConnected = false,
  healthScore = 100,
}) => {
  // ============================================================
  // LOGGING
  // ============================================================
  
  React.useEffect(() => {
    log.info('BottomNav mounted', { 
      currentPage, 
      engineRunning, 
      wsConnected, 
      healthScore,
      watchlistCount 
    });
    
    return () => {
      log.debug('BottomNav unmounted');
    };
  }, []);

  React.useEffect(() => {
    log.debug('State updated:', { currentPage, engineRunning, wsConnected });
  }, [currentPage, engineRunning, wsConnected]);

  // ============================================================
  // MEMOIZED VALUES
  // ============================================================
  
  const navItems = useMemo<NavItem[]>(() => [
    { id: 'Dashboard' as NavigationPage, label: 'Home', icon: LayoutDashboard },
    { id: 'Watchlist' as NavigationPage, label: 'Watchlist', icon: Star, badge: watchlistCount },
    { id: 'Market' as NavigationPage, label: 'Market', icon: TrendingUp },
    { id: 'Signals' as NavigationPage, label: 'Signals', icon: Radio },
    { id: 'Trading' as NavigationPage, label: 'Trade', icon: Zap },
  ], [watchlistCount]);

  // ============================================================
  // HANDLERS
  // ============================================================
  
  const handlePageChange = useCallback((page: NavigationPage) => {
    try {
      log.info(`Page change requested: ${page}`);
      
      // Validasi page
      const validPages: NavigationPage[] = ['Dashboard', 'Watchlist', 'Market', 'Signals', 'Trading'];
      if (!validPages.includes(page)) {
        log.warn(`Invalid page requested: ${page}`);
        return;
      }
      
      onPageChange(page);
    } catch (error) {
      log.error(`Page change to ${page} failed:`, error);
      // Fallback: jangan crash, tetap di halaman saat ini
    }
  }, [onPageChange]);

  const handleMenuOpen = useCallback(() => {
    try {
      log.info('Menu opened');
      onOpenMenu();
    } catch (error) {
      log.error('Menu open failed:', error);
    }
  }, [onOpenMenu]);

  // ============================================================
  // RENDER
  // ============================================================
  
  return (
    <BottomNavErrorBoundary>
      <nav 
        className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#0F141B]/95 backdrop-blur-md border-t border-[#26313D] px-2 py-1.5 flex items-center justify-around select-none shadow-2xl safe-area-bottom"
        role="navigation"
        aria-label="Bottom Navigation"
      >
        {/* Status Indicators */}
        <div className="absolute -top-7 right-2 flex items-center gap-1.5 text-[8px] font-mono">
          {engineRunning && (
            <span className="flex items-center gap-0.5 text-emerald-400">
              <Activity className="w-2.5 h-2.5 animate-pulse" />
            </span>
          )}
          {wsConnected ? (
            <Wifi className="w-2.5 h-2.5 text-emerald-400" />
          ) : (
            <WifiOff className="w-2.5 h-2.5 text-amber-400" />
          )}
          {healthScore < 70 && (
            <AlertCircle className="w-2.5 h-2.5 text-amber-400 animate-pulse" />
          )}
        </div>

        {/* Navigation Items */}
        {navItems.map((item) => (
          <NavItemComponent
            key={item.id}
            item={item}
            isActive={currentPage === item.id}
            onClick={() => handlePageChange(item.id)}
            engineRunning={engineRunning}
          />
        ))}

        {/* More Button */}
        <button
          onClick={handleMenuOpen}
          className={`
            flex flex-col items-center justify-center py-1 px-2 rounded-xl 
            transition-all duration-200 cursor-pointer min-w-[56px] min-h-[44px]
            text-[#8D9AAA] hover:text-white hover:bg-[#1A2530]
            focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:ring-offset-2 focus:ring-offset-[#0F141B]
            active:scale-95
          `}
          aria-label="Open menu"
        >
          <Menu className="w-5 h-5" />
          <span className="text-[10px] mt-0.5 tracking-tight font-sans">More</span>
        </button>
      </nav>
    </BottomNavErrorBoundary>
  );
};

// ============================================================
// EXPORT WITH DISPLAY NAME
// ============================================================

BottomNav.displayName = 'BottomNav';

export default BottomNav;
