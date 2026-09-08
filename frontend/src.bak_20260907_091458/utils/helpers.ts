import { NavigationPage, TradingSignal, Signal } from '../types';
import { STORAGE_KEYS, DEFAULT_PAGE } from './constants';

// ============================================================
// STORAGE HELPERS
// ============================================================

export const loadCurrentPage = (): NavigationPage => {
  try {
    const saved = localStorage.getItem(STORAGE_KEYS.CURRENT_PAGE);
    if (saved && saved !== 'undefined' && saved !== 'null') {
      return saved as NavigationPage;
    }
  } catch (error) {
    console.warn('Failed to load current page from localStorage:', error);
  }
  return DEFAULT_PAGE;
};

export const saveCurrentPage = (page: NavigationPage): void => {
  try {
    localStorage.setItem(STORAGE_KEYS.CURRENT_PAGE, page);
  } catch (error) {
    console.warn('Failed to save current page to localStorage:', error);
  }
};

export const loadSelectedPair = (): string | null => {
  try {
    return localStorage.getItem(STORAGE_KEYS.SELECTED_PAIR);
  } catch (error) {
    console.warn('Failed to load selected pair:', error);
    return null;
  }
};

export const saveSelectedPair = (pair: string): void => {
  try {
    localStorage.setItem(STORAGE_KEYS.SELECTED_PAIR, pair);
  } catch (error) {
    console.warn('Failed to save selected pair:', error);
  }
};

// ============================================================
// FORMATTING HELPERS
// ============================================================

export const formatPrice = (price: number): string => {
  if (!price || isNaN(price)) return '0.00';
  return price.toFixed(2);
};

export const formatPercent = (value: number): string => {
  if (!value || isNaN(value)) return '0.00%';
  return `${value.toFixed(2)}%`;
};

export const formatCurrency = (value: number): string => {
  if (!value || isNaN(value)) return '$0.00';
  return `$${value.toFixed(2)}`;
};

export const formatNumber = (value: number): string => {
  if (!value || isNaN(value)) return '0';
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`;
  return value.toString();
};

export const formatTime = (timestamp: number): string => {
  if (!timestamp) return '--:--:--';
  const date = new Date(timestamp);
  return date.toLocaleTimeString('id-ID', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
};

export const formatDate = (timestamp: number): string => {
  if (!timestamp) return '--/--/----';
  const date = new Date(timestamp);
  return date.toLocaleDateString('id-ID', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
};

export const formatRelativeTime = (timestamp: number): string => {
  const now = Date.now();
  const diff = now - timestamp;
  
  if (diff < 60000) return 'Just now';
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}d ago`;
  return formatDate(timestamp);
};

// ============================================================
// SIGNAL HELPERS
// ============================================================

export const getSignalColor = (signal: string): string => {
  switch (signal) {
    case 'BUY': return 'text-green-400 bg-green-500/20';
    case 'SELL': return 'text-red-400 bg-red-500/20';
    default: return 'text-gray-400 bg-gray-500/20';
  }
};

export const getSignalBadgeColor = (signal: string): string => {
  switch (signal) {
    case 'BUY': return 'bg-green-500';
    case 'SELL': return 'bg-red-500';
    default: return 'bg-gray-500';
  }
};

export const getStrengthColor = (strength: string): string => {
  switch (strength) {
    case 'STRONG': return 'text-green-400';
    case 'WEAK': return 'text-red-400';
    default: return 'text-yellow-400';
  }
};

export const getRiskColor = (risk: string): string => {
  switch (risk) {
    case 'LOW': return 'text-green-400';
    case 'MEDIUM': return 'text-yellow-400';
    case 'HIGH': return 'text-red-400';
    default: return 'text-gray-400';
  }
};

export const getQualityScore = (confidence: number): 'EXCELLENT' | 'GOOD' | 'NEUTRAL' => {
  if (confidence >= 80) return 'EXCELLENT';
  if (confidence >= 60) return 'GOOD';
  return 'NEUTRAL';
};

// ============================================================
// TRADING HELPERS
// ============================================================

export const calculatePnL = (entry: number, current: number, type: 'LONG' | 'SHORT'): number => {
  if (!entry || !current) return 0;
  const diff = current - entry;
  return type === 'LONG' ? diff : -diff;
};

export const calculatePnLPercent = (entry: number, current: number, type: 'LONG' | 'SHORT'): number => {
  if (!entry || !current) return 0;
  const pnl = calculatePnL(entry, current, type);
  return (pnl / entry) * 100;
};

export const calculateRiskReward = (entry: number, stopLoss: number, takeProfit: number): number => {
  if (!entry || !stopLoss || !takeProfit) return 0;
  const risk = Math.abs(entry - stopLoss);
  const reward = Math.abs(takeProfit - entry);
  return risk > 0 ? reward / risk : 0;
};

// ============================================================
// ARRAY HELPERS
// ============================================================

export const generateId = (): string => {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

export const sortBy = <T>(array: T[], key: keyof T, ascending: boolean = true): T[] => {
  return [...array].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return ascending ? aVal - bVal : bVal - aVal;
    }
    if (typeof aVal === 'string' && typeof bVal === 'string') {
      return ascending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }
    return 0;
  });
};

export const groupBy = <T, K extends keyof T>(array: T[], key: K): Map<T[K], T[]> => {
  const map = new Map<T[K], T[]>();
  for (const item of array) {
    const keyValue = item[key];
    if (!map.has(keyValue)) {
      map.set(keyValue, []);
    }
    map.get(keyValue)!.push(item);
  }
  return map;
};

// ============================================================
// VALIDATION HELPERS
// ============================================================

export const isValidPair = (pair: string): boolean => {
  return /^[A-Z]{2,6}\/[A-Z]{2,6}$/.test(pair);
};

export const isValidPrice = (price: number): boolean => {
  return !isNaN(price) && price > 0;
};

export const isValidPercentage = (value: number): boolean => {
  return !isNaN(value) && value >= 0 && value <= 100;
};

// ============================================================
// CLIPBOARD HELPERS
// ============================================================

export const copyToClipboard = async (text: string): Promise<boolean> => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.warn('Failed to copy to clipboard:', error);
    return false;
  }
};

// ============================================================
// ENVIRONMENT HELPERS
// ============================================================

export const isDev = (): boolean => {
  return process.env.NODE_ENV === 'development';
};

export const isProd = (): boolean => {
  return process.env.NODE_ENV === 'production';
};

export const getApiUrl = (): string => {
  return process.env.REACT_APP_API_URL || 'http://localhost:5001';
};

export const getWsUrl = (): string => {
  return process.env.REACT_APP_WS_URL || 'ws://localhost:5001/ws';
};
