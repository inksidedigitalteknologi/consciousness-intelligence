import { SystemMetrics } from '../types';
import { DEFAULT_METRICS } from '../utils/constants';

// ============================================================
// METRICS SERVICE
// ============================================================

export class MetricsService {
  /**
   * Calculate health score from metrics
   */
  calculateHealthScore(metrics: Partial<SystemMetrics>): number {
    const scores: number[] = [];
    
    // CPU usage (lower is better)
    if (metrics.cpu !== undefined) {
      scores.push(Math.max(0, 100 - (metrics.cpu * 0.8)));
    }
    
    // RAM usage (lower is better)
    if (metrics.ram_percent !== undefined) {
      scores.push(Math.max(0, 100 - (metrics.ram_percent * 0.7)));
    }
    
    // Win rate (higher is better)
    if (metrics.win_rate !== undefined) {
      scores.push(metrics.win_rate);
    }
    
    // Prediction accuracy (higher is better)
    if (metrics.prediction_accuracy !== undefined) {
      scores.push(metrics.prediction_accuracy);
    }
    
    // PnL (higher is better, cap at 100)
    if (metrics.pnl !== undefined) {
      const normalized = Math.min(Math.max(0, (metrics.pnl + 100) / 2), 100);
      scores.push(normalized);
    }
    
    return scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 50;
  }

  /**
   * Get risk level from metrics
   */
  getRiskLevel(metrics: Partial<SystemMetrics>): 'LOW' | 'MEDIUM' | 'HIGH' {
    const riskFactors: number[] = [];
    
    if (metrics.ram_percent !== undefined && metrics.ram_percent > 80) {
      riskFactors.push(1);
    }
    
    if (metrics.cpu !== undefined && metrics.cpu > 80) {
      riskFactors.push(1);
    }
    
    if (metrics.win_rate !== undefined && metrics.win_rate < 50) {
      riskFactors.push(1);
    }
    
    if (metrics.open_positions !== undefined && metrics.open_positions > 5) {
      riskFactors.push(1);
    }
    
    const totalRisk = riskFactors.reduce((a, b) => a + b, 0);
    
    if (totalRisk >= 3) return 'HIGH';
    if (totalRisk >= 1) return 'MEDIUM';
    return 'LOW';
  }

  /**
   * Format metrics for display
   */
  formatMetrics(metrics: SystemMetrics): Record<string, string> {
    return {
      cpu: `${metrics.cpu.toFixed(1)}%`,
      ram: `${metrics.ram.toFixed(1)}MB / ${metrics.ram_percent.toFixed(1)}%`,
      disk: `${metrics.disk_percent.toFixed(1)}%`,
      uptime: this.formatUptime(metrics.uptime),
      pnl: `$${metrics.pnl.toFixed(2)}`,
      winRate: `${metrics.win_rate.toFixed(1)}%`,
      health: `${metrics.health_score}/100`,
      risk: metrics.risk_level,
    };
  }

  /**
   * Format uptime seconds to readable string
   */
  formatUptime(seconds: number): string {
    if (!seconds) return '0s';
    
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    const parts: string[] = [];
    if (days > 0) parts.push(`${days}d`);
    if (hours > 0) parts.push(`${hours}h`);
    if (minutes > 0) parts.push(`${minutes}m`);
    if (secs > 0 && parts.length === 0) parts.push(`${secs}s`);
    
    return parts.join(' ') || '0s';
  }

  /**
   * Get metrics trend over time
   */
  getTrend(history: SystemMetrics[], key: keyof SystemMetrics): number {
    if (!history || history.length < 2) return 0;
    const latest = history[history.length - 1][key];
    const previous = history[history.length - 2][key];
    if (typeof latest !== 'number' || typeof previous !== 'number') return 0;
    return latest - previous;
  }

  /**
   * Calculate moving average
   */
  movingAverage(history: number[], window: number = 5): number[] {
    const result: number[] = [];
    for (let i = 0; i < history.length; i++) {
      const start = Math.max(0, i - window + 1);
      const slice = history.slice(start, i + 1);
      const avg = slice.reduce((a, b) => a + b, 0) / slice.length;
      result.push(avg);
    }
    return result;
  }

  /**
   * Normalize metrics to 0-100 scale
   */
  normalize(value: number, min: number = 0, max: number = 100): number {
    return Math.max(0, Math.min(100, ((value - min) / (max - min)) * 100));
  }
}

export const metricsService = new MetricsService();
export default metricsService;
