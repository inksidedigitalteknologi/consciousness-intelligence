import {
  TradingSignal,
  TickerInfo,
  SystemMetrics,
  KnowledgeItem,
  ComponentHealthStatus,
} from '../types';

// ============================================================
// SIGNAL VALIDATORS
// ============================================================

export const isValidSignal = (signal: any): signal is TradingSignal => {
  return (
    signal &&
    typeof signal.id === 'string' &&
    typeof signal.pair === 'string' &&
    ['BUY', 'SELL', 'HOLD'].includes(signal.signal) &&
    typeof signal.confidence === 'number' &&
    signal.confidence >= 0 &&
    signal.confidence <= 100 &&
    typeof signal.price === 'number' &&
    signal.price > 0
  );
};

export const isValidTicker = (ticker: any): ticker is TickerInfo => {
  return (
    ticker &&
    typeof ticker.pair === 'string' &&
    typeof ticker.name === 'string' &&
    typeof ticker.price === 'number' &&
    ticker.price > 0 &&
    typeof ticker.change24h === 'number' &&
    typeof ticker.volume24h === 'number'
  );
};

// ============================================================
// METRICS VALIDATORS
// ============================================================

export const isValidMetrics = (metrics: any): metrics is SystemMetrics => {
  return (
    metrics &&
    typeof metrics.cpu === 'number' &&
    typeof metrics.ram === 'number' &&
    typeof metrics.ram_percent === 'number' &&
    typeof metrics.uptime === 'number' &&
    typeof metrics.health_score === 'number'
  );
};

// ============================================================
// KNOWLEDGE VALIDATORS
// ============================================================

export const isValidKnowledge = (item: any): item is KnowledgeItem => {
  return (
    item &&
    typeof item.id === 'string' &&
    typeof item.content === 'string' &&
    typeof item.category === 'string' &&
    ['fact', 'rule', 'pattern', 'strategy'].includes(item.type) &&
    typeof item.confidence === 'number' &&
    typeof item.importance === 'number'
  );
};

// ============================================================
// HEALTH VALIDATORS
// ============================================================

export const isValidHealthStatus = (status: any): status is ComponentHealthStatus => {
  return (
    status &&
    typeof status.name === 'string' &&
    ['healthy', 'warning', 'error', 'unknown'].includes(status.status) &&
    typeof status.lastCheck === 'string'
  );
};

// ============================================================
// POSITION VALIDATORS
// ============================================================

export const isValidPosition = (position: any): boolean => {
  return (
    position &&
    typeof position.id === 'string' &&
    typeof position.pair === 'string' &&
    ['LONG', 'SHORT'].includes(position.type) &&
    typeof position.entryPrice === 'number' &&
    typeof position.currentPrice === 'number' &&
    typeof position.size === 'number' &&
    ['OPEN', 'CLOSED', 'STOPPED', 'TAKE_PROFIT'].includes(position.status)
  );
};

// ============================================================
// UTILITY VALIDATORS
// ============================================================

export const isString = (value: any): value is string => {
  return typeof value === 'string';
};

export const isNumber = (value: any): value is number => {
  return typeof value === 'number' && !isNaN(value);
};

export const isBoolean = (value: any): value is boolean => {
  return typeof value === 'boolean';
};

export const isObject = (value: any): value is Record<string, any> => {
  return value && typeof value === 'object' && !Array.isArray(value);
};

export const isArray = <T>(value: any): value is T[] => {
  return Array.isArray(value);
};

export const hasKeys = (obj: any, keys: string[]): boolean => {
  return keys.every(key => key in obj);
};

export const isNotEmpty = (value: any): boolean => {
  if (value === null || value === undefined) return false;
  if (typeof value === 'string') return value.trim().length > 0;
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === 'object') return Object.keys(value).length > 0;
  return true;
