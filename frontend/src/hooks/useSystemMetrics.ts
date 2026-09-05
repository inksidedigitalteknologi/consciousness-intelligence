import { useState, useEffect, useCallback } from 'react';
import { SystemMetrics } from '../types';
import { DEFAULT_METRICS } from '../utils/constants';
import { metricsService } from '../services/metricService';

// ============================================================
// USE SYSTEM METRICS HOOK
// ============================================================

export function useSystemMetrics(initialMetrics?: Partial<SystemMetrics>) {
  const [metrics, setMetrics] = useState<SystemMetrics>({
    ...DEFAULT_METRICS,
    ...initialMetrics,
  });
  const [history, setHistory] = useState<SystemMetrics[]>([]);
  const [trends, setTrends] = useState<Record<string, number>>({});

  // Update metrics
  const updateMetrics = useCallback((newMetrics: Partial<SystemMetrics>) => {
    setMetrics(prev => {
      const updated = { ...prev, ...newMetrics };
      
      // Calculate health score
      updated.health_score = metricsService.calculateHealthScore(updated);
      updated.risk_level = metricsService.getRiskLevel(updated);
      updated.last_update = new Date().toISOString();
      
      // Add to history
      setHistory(prevHistory => {
        const newHistory = [...prevHistory, updated];
        if (newHistory.length > 100) {
          return newHistory.slice(-100);
        }
        return newHistory;
      });
      
      return updated;
    });
  }, []);

  // Calculate trends
  useEffect(() => {
    if (history.length < 2) return;
    
    const newTrends: Record<string, number> = {};
    const keys: (keyof SystemMetrics)[] = [
      'cpu', 'ram', 'ram_percent', 'disk_percent',
      'win_rate', 'prediction_accuracy', 'health_score'
    ];
    
    for (const key of keys) {
      newTrends[key] = metricsService.getTrend(history, key);
    }
    
    setTrends(newTrends);
  }, [history]);

  // Reset metrics
  const resetMetrics = useCallback(() => {
    setMetrics(DEFAULT_METRICS);
    setHistory([]);
    setTrends({});
  }, []);

  return {
    metrics,
    history,
    trends,
    updateMetrics,
    resetMetrics,
    healthScore: metrics.health_score,
    riskLevel: metrics.risk_level,
    isHealthy: metrics.health_score >= 70,
    isWarning: metrics.health_score >= 40 && metrics.health_score < 70,
    isCritical: metrics.health_score < 40,
  };
}

export default useSystemMetrics;
