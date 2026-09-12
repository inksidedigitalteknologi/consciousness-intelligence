# core/market_indicators.py
# Technical Indicator Engine — hitung dari historical data
# Bukan Brain — murni matematika

import logging
import statistics
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def parse_price(value: str) -> Optional[float]:
    """Parse '$164.97' → 164.97"""
    if value is None:
        return None
    try:
        return float(str(value).replace('$', '').replace(',', '').strip())
    except (ValueError, TypeError):
        return None


def parse_volume(value: str) -> Optional[int]:
    """Parse '3,286,005' → 3286005"""
    if value is None:
        return None
    try:
        return int(str(value).replace(',', '').strip())
    except (ValueError, TypeError):
        return None


def calculate_rsi(closes: List[float], period: int = 14) -> Optional[float]:
    """Relative Strength Index."""
    if len(closes) < period + 1:
        return None
    
    gains = []
    losses = []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def calculate_sma(closes: List[float], period: int) -> Optional[float]:
    """Simple Moving Average."""
    if len(closes) < period:
        return None
    return round(sum(closes[-period:]) / period, 2)


def calculate_ema(closes: List[float], period: int) -> Optional[float]:
    """Exponential Moving Average."""
    if len(closes) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = sum(closes[:period]) / period
    
    for price in closes[period:]:
        ema = (price - ema) * multiplier + ema
    
    return round(ema, 2)


def calculate_volatility(closes: List[float]) -> Optional[float]:
    """Volatilitas — std dev returns × 100."""
    if len(closes) < 2:
        return None
    try:
        returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
        return round(statistics.stdev(returns) * 100, 2)
    except statistics.StatisticsError:
        return None


def calculate_indicators(historical: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Hitung semua indikator dari historical data Nasdaq.
    
    Input format:
        [{'date': '09/11/2026', 'close': '$164.97', 'volume': '3,286,005', 
          'open': '$164.36', 'high': '$165.37', 'low': '$163.50'}, ...]
    
    PENTING: Nasdaq return data DESCENDING (terbaru dulu).
    Kita reverse supaya ASCENDING (terlama dulu) untuk kalkulasi RSI/SMA.
    """
    if not historical:
        return {"error": "No historical data"}
    
    # Reverse: Nasdaq descending → kita butuh ascending
    historical = list(reversed(historical))
    
    closes = []
    volumes = []
    highs = []
    lows = []
    opens = []
    
    for row in historical:
        c = parse_price(row.get('close'))
        v = parse_volume(row.get('volume'))
        h = parse_price(row.get('high'))
        l = parse_price(row.get('low'))
        o = parse_price(row.get('open'))
        
        if c is not None:
            closes.append(c)
            volumes.append(v if v is not None else 0)
            highs.append(h if h is not None else c)
            lows.append(l if l is not None else c)
            opens.append(o if o is not None else c)
    
    if not closes:
        return {"error": "No valid closes"}
    
    current_price = closes[-1]
    
    # Basic indicators
    rsi = calculate_rsi(closes)
    sma20 = calculate_sma(closes, 20)
    sma50 = calculate_sma(closes, 50)
    ema12 = calculate_ema(closes, min(12, len(closes)))
    ema26 = calculate_ema(closes, min(26, len(closes)))
    
    # Volume
    volume_today = volumes[-1] if volumes else 0
    volume_avg_20 = sum(volumes[-20:]) / min(20, len(volumes)) if volumes else 0
    volume_ratio = round(volume_today / volume_avg_20, 2) if volume_avg_20 > 0 else 0
    
    # Support/Resistance (20 hari)
    lookback = min(20, len(lows))
    support = round(min(lows[-lookback:]), 2)
    resistance = round(max(highs[-lookback:]), 2)
    
    # Trend from SMA
    if sma20 and current_price > sma20:
        trend_sma = "BULLISH"
    elif sma20 and current_price < sma20:
        trend_sma = "BEARISH"
    else:
        trend_sma = "NEUTRAL"
    
    # Cross detection
    sma_cross = None
    if sma20 and sma50:
        if sma20 > sma50:
            sma_cross = "GOLDEN"  # bullish
        elif sma20 < sma50:
            sma_cross = "DEATH"  # bearish
    
    # Momentum (5 hari)
    momentum_5d = None
    if len(closes) >= 5:
        momentum_5d = round(((closes[-1] - closes[-5]) / closes[-5]) * 100, 2)
    
    # Volatility
    volatility = calculate_volatility(closes)
    
    # RSI interpretation
    if rsi is None:
        rsi_signal = "UNKNOWN"
    elif rsi >= 70:
        rsi_signal = "OVERBOUGHT"
    elif rsi <= 30:
        rsi_signal = "OVERSOLD"
    elif rsi >= 60:
        rsi_signal = "STRONG"
    elif rsi <= 40:
        rsi_signal = "WEAK"
    else:
        rsi_signal = "NEUTRAL"
    
    return {
        'current_price': current_price,
        'days_available': len(closes),
        
        # Momentum
        'rsi': rsi,
        'rsi_signal': rsi_signal,
        'momentum_5d': momentum_5d,
        
        # Moving Averages
        'sma20': sma20,
        'sma50': sma50,
        'ema12': ema12,
        'ema26': ema26,
        'trend_sma': trend_sma,
        'sma_cross': sma_cross,
        
        # Volume
        'volume_today': volume_today,
        'volume_avg_20': int(volume_avg_20),
        'volume_ratio': volume_ratio,
        'volume_signal': 'HIGH' if volume_ratio > 1.5 else 'LOW' if volume_ratio < 0.7 else 'NORMAL',
        
        # Level
        'support': support,
        'resistance': resistance,
        'distance_to_support': round(((current_price - support) / support) * 100, 2),
        'distance_to_resistance': round(((resistance - current_price) / current_price) * 100, 2),
        
        # Risk
        'volatility': volatility,
        'risk_level': 'HIGH' if volatility and volatility > 3 else 'LOW' if volatility and volatility < 1 else 'MEDIUM',
        
        # Price range
        'low_20d': round(min(lows[-lookback:]), 2),
        'high_20d': round(max(highs[-lookback:]), 2),
    }


def score_indicators(indicators: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scoring dari indikator — weighted score untuk rekomendasi.
    
    Return:
        {'score': -100..100, 'action': 'BUY'/'SELL'/'HOLD', 'confidence': 0-100, 'reasons': [...]}
    """
    score = 0
    reasons = []
    
    # 1. RSI (weight 25)
    rsi = indicators.get('rsi')
    if rsi is not None:
        if rsi < 30:
            score += 25
            reasons.append(f"RSI {rsi} — oversold, potensi bounce")
        elif rsi < 45:
            score += 10
            reasons.append(f"RSI {rsi} — weak, potensi reversal naik")
        elif rsi < 55:
            reasons.append(f"RSI {rsi} — netral")
        elif rsi < 70:
            score -= 5
            reasons.append(f"RSI {rsi} — strong, hati-hati overbought")
        else:
            score -= 25
            reasons.append(f"RSI {rsi} — overbought, potensi koreksi")
    
    # 2. Trend SMA20 (weight 20)
    trend = indicators.get('trend_sma')
    if trend == 'BULLISH':
        score += 20
        reasons.append(f"Harga di atas SMA20 — trend bullish")
    elif trend == 'BEARISH':
        score -= 20
        reasons.append(f"Harga di bawah SMA20 — trend bearish")
    
    # 3. SMA Cross (weight 15)
    cross = indicators.get('sma_cross')
    if cross == 'GOLDEN':
        score += 15
        reasons.append("Golden cross — SMA20 di atas SMA50")
    elif cross == 'DEATH':
        score -= 15
        reasons.append("Death cross — SMA20 di bawah SMA50")
    
    # 4. Volume (weight 15)
    vol_signal = indicators.get('volume_signal')
    vol_ratio = indicators.get('volume_ratio', 1)
    if vol_signal == 'HIGH':
        # Volume tinggi — konfirmasi arah
        if trend == 'BULLISH':
            score += 15
            reasons.append(f"Volume {vol_ratio}× avg — konfirmasi bullish")
        elif trend == 'BEARISH':
            score -= 15
            reasons.append(f"Volume {vol_ratio}× avg — konfirmasi bearish")
    elif vol_signal == 'LOW':
        score -= 5
        reasons.append(f"Volume {vol_ratio}× avg — lemah, kurang konfirmasi")
    
    # 5. Momentum 5d (weight 15)
    mom = indicators.get('momentum_5d')
    if mom is not None:
        if mom > 5:
            score += 15
            reasons.append(f"Momentum 5d: +{mom}% — kuat")
        elif mom > 2:
            score += 8
            reasons.append(f"Momentum 5d: +{mom}% — positif")
        elif mom < -5:
            score -= 15
            reasons.append(f"Momentum 5d: {mom}% — turun kuat")
        elif mom < -2:
            score -= 8
            reasons.append(f"Momentum 5d: {mom}% — negatif")
    
    # 6. Volatility (weight 10)
    risk = indicators.get('risk_level')
    if risk == 'LOW':
        score += 5
        reasons.append("Volatilitas rendah — stabil")
    elif risk == 'HIGH':
        score -= 10
        reasons.append("Volatilitas tinggi — risk tinggi")
    
    # Final action
    if score >= 40:
        action = "BUY"
        confidence = min(95, 50 + score)
    elif score <= -40:
        action = "SELL"
        confidence = min(95, 50 + abs(score))
    else:
        action = "HOLD"
        confidence = max(40, 60 - abs(score))
    
    return {
        'score': score,
        'action': action,
        'confidence': round(confidence, 1),
        'reasons': reasons,
    }


def analyze_multi_timeframe(historical_full: list) -> dict:
    """
    Analisis dari 4 timeframe dengan slicing.
    
    Input: historical penuh dari Nasdaq (2 tahun = 501 rows)
    Output: {'timeframes': {...}, 'consensus': {...}, 'overall': {...}}
    """
    if not historical_full:
        return {"error": "No historical data"}
    
    total = len(historical_full)
    
    # Slicing per timeframe — dengan SMA berbeda
    # 1M → SMA20, 3M → SMA50, 6M → SMA100, 1Y → SMA200
    timeframes = {
        '1m': {'days': 21,  'sma_period': 20},
        '3m': {'days': 62,  'sma_period': 50},
        '6m': {'days': 125, 'sma_period': 100},
        '1y': {'days': 251, 'sma_period': 200},
    }
    
    results = {}
    
    for label, cfg in timeframes.items():
        days = min(cfg['days'], total)
        sma_period = cfg['sma_period']
        
        slice_data = historical_full[:days]
        
        if len(slice_data) < 15:
            results[label] = {
                'days': len(slice_data),
                'error': f'Only {len(slice_data)} days available',
            }
            continue
        
        indicators = calculate_indicators(slice_data)
        
        # Tambah SMA sesuai timeframe
        try:
            # Reverse slice — ascending
            asc = list(reversed(slice_data))
            closes = [float(r['close'].replace('$', '').replace(',', '')) for r in asc]
            
            if len(closes) >= sma_period:
                sma_tf = round(sum(closes[-sma_period:]) / sma_period, 2)
            else:
                sma_tf = None
            
            indicators['sma_timeframe'] = sma_tf
            indicators['sma_timeframe_period'] = sma_period
            
            # Trend berdasarkan SMA timeframe (bukan SMA20)
            current_price = indicators.get('current_price')
            if sma_tf and current_price:
                if current_price > sma_tf:
                    indicators['trend_sma'] = "BULLISH"
                elif current_price < sma_tf:
                    indicators['trend_sma'] = "BEARISH"
                else:
                    indicators['trend_sma'] = "NEUTRAL"
        except Exception:
            indicators['sma_timeframe'] = None
            indicators['sma_timeframe_period'] = sma_period
        
        score = score_indicators(indicators)
        
        results[label] = {
            'days': len(slice_data),
            'indicators': {
                'current_price': indicators.get('current_price'),
                'rsi': indicators.get('rsi'),
                'rsi_signal': indicators.get('rsi_signal'),
                'sma20': indicators.get('sma20'),
                'sma50': indicators.get('sma50'),
                'sma_timeframe': indicators.get('sma_timeframe'),
                'sma_timeframe_period': indicators.get('sma_timeframe_period'),
                'trend_sma': indicators.get('trend_sma'),
                'momentum_5d': indicators.get('momentum_5d'),
                'volume_ratio': indicators.get('volume_ratio'),
                'volatility': indicators.get('volatility'),
                'support': indicators.get('support'),
                'resistance': indicators.get('resistance'),
            },
            'score': {
                'action': score.get('action'),
                'score': score.get('score'),
                'confidence': score.get('confidence'),
                'reasons': score.get('reasons', [])[:3],
            },
        }
    
    # Consensus
    actions = [r['score']['action'] for r in results.values() if 'score' in r]
    action_counts = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
    for a in actions:
        action_counts[a] = action_counts.get(a, 0) + 1
    
    if actions:
        consensus_action = max(action_counts, key=action_counts.get)
        agreement = round((action_counts[consensus_action] / len(actions)) * 100, 1)
    else:
        consensus_action = 'HOLD'
        agreement = 0
    
    # Trend consistency — apakah semua timeframe searah?
    trends = [r['indicators']['trend_sma'] for r in results.values() if 'indicators' in r]
    bullish_count = trends.count('BULLISH')
    bearish_count = trends.count('BEARISH')
    
    # Overall score
    total_score = sum(r['score']['score'] for r in results.values() if 'score' in r)
    avg_score = round(total_score / len(actions), 1) if actions else 0
    
    # Overall action
    if avg_score >= 30:
        overall = 'BUY'
    elif avg_score <= -30:
        overall = 'SELL'
    else:
        overall = 'HOLD'
    
    # Confidence
    overall_confidence = min(95, max(30, 50 + abs(avg_score) // 2))
    
    # Multi-timeframe insight
    insights = []
    if bullish_count == len(trends):
        insights.append(f"✅ Semua timeframe BULLISH ({bullish_count}/{len(trends)}) — trend kuat")
    elif bearish_count == len(trends):
        insights.append(f"🔴 Semua timeframe BEARISH ({bearish_count}/{len(trends)}) — trend turun")
    elif bullish_count > bearish_count:
        insights.append(f"📊 Mayoritas BULLISH ({bullish_count}/{len(trends)}) — trend naik")
    elif bearish_count > bullish_count:
        insights.append(f"📊 Mayoritas BEARISH ({bearish_count}/{len(trends)}) — trend turun")
    else:
        insights.append(f"⚠️ Konflik timeframe ({bullish_count} bullish / {bearish_count} bearish) — volatilitas")
    
    if agreement >= 75:
        insights.append(f"✅ Konsensus tinggi ({agreement}%) — sinyal jelas")
    elif agreement >= 50:
        insights.append(f"📊 Konsensus moderat ({agreement}%)")
    else:
        insights.append(f"⚠️ Konsensus rendah ({agreement}%) — tidak ada sinyal jelas")
    
    return {
        'timeframes': results,
        'consensus': {
            'action': consensus_action,
            'agreement': agreement,
            'breakdown': action_counts,
        },
        'overall': {
            'action': overall,
            'confidence': round(overall_confidence, 1),
            'score': avg_score,
            'insights': insights,
            'trend_consistency': {
                'bullish': bullish_count,
                'bearish': bearish_count,
                'total': len(trends),
            },
        },
    }


__all__ = [
    'calculate_indicators',
    'score_indicators',
    'analyze_multi_timeframe',
    'calculate_rsi',
    'calculate_sma',
    'calculate_ema',
    'calculate_volatility',
]
