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
    # RSI Balanced: rata-rata 3 period (3, 7, 14)
    rsi_3 = calculate_rsi(closes, period=3)
    rsi_7 = calculate_rsi(closes, period=7)
    rsi_14 = calculate_rsi(closes, period=14)
    _valid_rsi = [r for r in [rsi_3, rsi_7, rsi_14] if r is not None]
    rsi = round(sum(_valid_rsi) / len(_valid_rsi), 2) if _valid_rsi else None
    rsi_period = 'balanced(3,7,14)'

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
    
    # Cross detection (dengan threshold minimum 0.5%)
    sma_cross = None
    if sma20 and sma50:
        diff_pct = abs(sma20 - sma50) / sma50 * 100
        if diff_pct < 0.5:
            sma_cross = None  # terlalu tipis, tidak valid
        elif sma20 > sma50:
            sma_cross = "GOLDEN"  # bullish
        else:
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
        'rsi_period': rsi_period,
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

        # === OHLCV untuk analisis lanjutan (Fase 2) ===
        '_closes': closes,
        '_highs': highs,
        '_lows': lows,
        '_opens': opens,
        '_volumes': volumes,
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

            # === RSI BALANCED PER TIMEFRAME (3, 7, 14 rata-rata) ===
            # Scaling period berdasarkan timeframe
            period_scale = {'1m': 1, '3m': 2, '6m': 3, '1y': 4}
            scale = period_scale.get(label, 1)
            p3 = 3 * scale
            p7 = 7 * scale
            p14 = 14 * scale

            rsi_vals = []
            for period in [p3, p7, p14]:
                if len(closes) >= period + 1:
                    gains, losses = [], []
                    for i in range(1, len(closes)):
                        diff = closes[i] - closes[i-1]
                        gains.append(max(diff, 0))
                        losses.append(max(-diff, 0))
                    avg_gain = sum(gains[-period:]) / period
                    avg_loss = sum(losses[-period:]) / period
                    if avg_loss == 0:
                        rsi_vals.append(100.0)
                    else:
                        rs = avg_gain / avg_loss
                        rsi_vals.append(round(100 - (100 / (1 + rs)), 2))

            rsi_tf = round(sum(rsi_vals) / len(rsi_vals), 2) if rsi_vals else None
            rsi_period = f'balanced({p3},{p7},{p14})'

            indicators['rsi'] = rsi_tf
            indicators['rsi_period'] = rsi_period

            if rsi_tf is None:
                indicators['rsi_signal'] = "UNKNOWN"
            elif rsi_tf >= 70:
                indicators['rsi_signal'] = "OVERBOUGHT"
            elif rsi_tf <= 30:
                indicators['rsi_signal'] = "OVERSOLD"
            elif rsi_tf >= 60:
                indicators['rsi_signal'] = "STRONG"
            elif rsi_tf <= 40:
                indicators['rsi_signal'] = "WEAK"
            else:
                indicators['rsi_signal'] = "NEUTRAL"
            # === END RSI PER TIMEFRAME ===
            
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
                'rsi_period': indicators.get('rsi_period'),
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


def analyze_unified(
    indicators: Dict[str, Any],
    multi_timeframe: Optional[Dict[str, Any]] = None,
    prediction: Optional[Dict[str, Any]] = None,
    market_context: Optional[Dict[str, Any]] = None,
    fundamental: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Analisis TERPADU — 14 aspek, Equal Weight.

    Aspek:
    1. RSI
    2. Trend SMA
    3. SMA Cross
    4. Volume Signal
    5. Volume Ratio
    6. Momentum 5d
    7. Volatilitas
    8. Support/Resistance
    9. Distance to S/R
    10. Low/High 20d
    11. EMA 12/26
    12. Multi-Timeframe
    13. Monte Carlo
    14. Market Regime

    Threshold: BUY >= 50, SELL <= -50, else HOLD.
    Confidence: 50 + abs(score), max 95, min 30.
    """
    scores = {}

    # === 1. RSI ===
    rsi = indicators.get('rsi')
    if rsi is not None:
        if rsi < 30:
            scores['rsi'] = +100
        elif rsi < 45:
            scores['rsi'] = +50
        elif rsi < 55:
            scores['rsi'] = 0
        elif rsi < 70:
            scores['rsi'] = -25
        else:
            scores['rsi'] = -100

    # === 2. Trend SMA ===
    trend = indicators.get('trend_sma')
    if trend == 'BULLISH':
        scores['trend'] = +100
    elif trend == 'BEARISH':
        scores['trend'] = -100
    else:
        scores['trend'] = 0

    # === 3. SMA Cross ===
    cross = indicators.get('sma_cross')
    if cross == 'GOLDEN':
        scores['cross'] = +100
    elif cross == 'DEATH':
        scores['cross'] = -100
    else:
        scores['cross'] = 0

    # === 4. Volume Signal (digabung dengan ratio) ===
    vol_signal = indicators.get('volume_signal')
    vol_ratio = indicators.get('volume_ratio', 0)
    vol_score = 0
    if vol_signal == 'HIGH':
        if trend == 'BULLISH':
            vol_score = +75  # volume tinggi + trend naik = kuat
        elif trend == 'BEARISH':
            vol_score = -75  # volume tinggi + trend turun = kuat
    elif vol_signal == 'LOW':
        vol_score = -25  # volume rendah = lemah
    else:
        # NORMAL — pakai volume_ratio
        if vol_ratio > 1.5:
            vol_score = +30 if trend == 'BULLISH' else -30
        elif vol_ratio > 1.0:
            vol_score = +15 if trend == 'BULLISH' else -15
        elif vol_ratio < 0.7:
            vol_score = -15
    scores['volume_signal'] = vol_score

    # === 5. Volume Ratio — DIHAPUS (digabung ke volume_signal) ===
    # volume_ratio sekarang digabung ke scores['volume_signal']

    # === 6. Momentum 5d ===
    mom = indicators.get('momentum_5d')
    if mom is not None:
        if mom > 5:
            scores['momentum'] = +100
        elif mom > 2:
            scores['momentum'] = +50
        elif mom > 0:
            scores['momentum'] = +20
        elif mom > -2:
            scores['momentum'] = -20
        elif mom > -5:
            scores['momentum'] = -50
        else:
            scores['momentum'] = -100
    else:
        scores['momentum'] = 0

    # === 7. Volatilitas ===
    risk = indicators.get('risk_level')
    if risk == 'LOW':
        scores['volatilitas'] = +30
    elif risk == 'HIGH':
        scores['volatilitas'] = -30
    else:
        scores['volatilitas'] = 0

    # === 8. Support/Resistance ===
    current = indicators.get('current_price')
    support = indicators.get('support')
    resistance = indicators.get('resistance')
    if current and support and resistance and resistance > support:
        pos = (current - support) / (resistance - support)
        scores['sr'] = round((0.5 - pos) * 200, 2)
    else:
        scores['sr'] = 0

    # === 9. Distance to S/R ===
    dist_sup = indicators.get('distance_to_support')
    dist_res = indicators.get('distance_to_resistance')
    if dist_sup is not None and dist_res is not None:
        if dist_sup < 2:
            scores['distance'] = +50
        elif dist_res < 2:
            scores['distance'] = -50
        else:
            scores['distance'] = 0
    else:
        scores['distance'] = 0

    # === 10. Low/High 20d ===
    low_20d = indicators.get('low_20d')
    high_20d = indicators.get('high_20d')
    if current and low_20d and high_20d and high_20d > low_20d:
        pos = (current - low_20d) / (high_20d - low_20d)
        scores['range_20d'] = round((0.5 - pos) * 200, 2)
    else:
        scores['range_20d'] = 0

    # === 11. EMA 12/26 ===
    ema12 = indicators.get('ema12')
    ema26 = indicators.get('ema26')
    if ema12 and ema26:
        if ema12 > ema26:
            scores['ema'] = +50
        elif ema12 < ema26:
            scores['ema'] = -50
        else:
            scores['ema'] = 0
    else:
        scores['ema'] = 0

    # === 12. Multi-Timeframe ===
    if multi_timeframe and isinstance(multi_timeframe, dict):
        mtf_overall = multi_timeframe.get('overall', {}) or {}
        scores['mtf'] = mtf_overall.get('score', 0)
    else:
        scores['mtf'] = 0

    # === 13. Monte Carlo ===
    if prediction and isinstance(prediction, dict):
        prob_up = prediction.get('prob_up', 50)
        scores['mc'] = round((prob_up - 50) * 2, 2)
    else:
        scores['mc'] = 0

    # === 14. Market Regime ===
    if market_context and isinstance(market_context, dict):
        regime = market_context.get('regime', 'NEUTRAL')
        if regime == 'BULLISH':
            scores['regime'] = +50
        elif regime == 'BEARISH':
            scores['regime'] = -50
        else:
            scores['regime'] = 0
    else:
        scores['regime'] = 0

    # === AMBIL OHLCV DARI INDICATORS ===
    closes = indicators.get('_closes', [])
    highs = indicators.get('_highs', [])
    lows = indicators.get('_lows', [])
    opens = indicators.get('_opens', [])
    volumes = indicators.get('_volumes', [])

    # === SIMPAN FUNDAMENTAL ===
    if fundamental:
        indicators['_fundamental'] = fundamental

    # === 15. MACD ===
    try:
        macd_data = calculate_macd(closes)
        if macd_data.get('trend') == 'BULLISH':
            scores['macd'] = +50
        elif macd_data.get('trend') == 'BEARISH':
            scores['macd'] = -50
        else:
            scores['macd'] = 0
    except Exception:
        scores['macd'] = 0

    # === 16. BOLLINGER ===
    try:
        bb = calculate_bollinger(closes)
        if bb.get('signal') == 'OVERSOLD':
            scores['bollinger'] = +75
        elif bb.get('signal') == 'OVERBOUGHT':
            scores['bollinger'] = -75
        else:
            scores['bollinger'] = 0
    except Exception:
        scores['bollinger'] = 0

    # === 17. ATR ===
    try:
        atr = calculate_atr(highs, lows, closes)
        if atr and current:
            atr_pct = (atr / current) * 100
            if atr_pct < 2:
                scores['atr'] = +25
            elif atr_pct > 5:
                scores['atr'] = -25
            else:
                scores['atr'] = 0
        else:
            scores['atr'] = 0
    except Exception:
        scores['atr'] = 0

    # === 18. STOCHASTIC ===
    try:
        stoch = calculate_stochastic(highs, lows, closes)
        if stoch.get('signal') == 'OVERSOLD':
            scores['stochastic'] = +75
        elif stoch.get('signal') == 'OVERBOUGHT':
            scores['stochastic'] = -75
        else:
            scores['stochastic'] = 0
    except Exception:
        scores['stochastic'] = 0

    # === 19. OBV ===
    try:
        obv = calculate_obv(closes, volumes)
        if obv.get('trend') == 'BULLISH':
            scores['obv'] = +50
        elif obv.get('trend') == 'BEARISH':
            scores['obv'] = -50
        else:
            scores['obv'] = 0
    except Exception:
        scores['obv'] = 0

    # === 20. VWAP ===
    try:
        vwap = calculate_vwap(highs, lows, closes, volumes)
        if vwap and current:
            if current > vwap * 1.02:
                scores['vwap'] = -25
            elif current < vwap * 0.98:
                scores['vwap'] = +25
            else:
                scores['vwap'] = 0
        else:
            scores['vwap'] = 0
    except Exception:
        scores['vwap'] = 0

    # === 21. FIBONACCI ===
    try:
        fib = calculate_fibonacci(highs, lows)
        if fib.get('nearest') in ('0.382', '0.500', '0.618'):
            scores['fibonacci'] = +25
        else:
            scores['fibonacci'] = 0
    except Exception:
        scores['fibonacci'] = 0

    # === 22. VOLUME PROFILE ===
    try:
        vp = calculate_volume_profile(closes, volumes)
        if vp.get('poc') and current:
            if current < vp['poc'] * 0.98:
                scores['volume_profile'] = +25
            elif current > vp['poc'] * 1.02:
                scores['volume_profile'] = -25
            else:
                scores['volume_profile'] = 0
        else:
            scores['volume_profile'] = 0
    except Exception:
        scores['volume_profile'] = 0

    # === 27-29. CORRELATION (Fase 3b) ===
    try:
        corr_data = indicators.get('_correlation', {}) or {}
        corr_scores = score_correlation(corr_data)
        scores['corr_sp500'] = corr_scores.get('corr_sp500', 0)
        scores['beta'] = corr_scores.get('beta', 0)
    except Exception:
        scores['corr_sp500'] = 0
        scores['beta'] = 0

    # === 30-31. SENTIMEN (Fase 4a) ===
    try:
        sent_data = indicators.get('_sentiment', {}) or {}
        sent_scores = score_sentiment(sent_data)
        scores['sentiment'] = sent_scores.get('sentiment', 0)
    except Exception:
        scores['sentiment'] = 0

    # === 32-35. ADVANCED (Fase 4b) ===
    try:
        # Candlestick
        if len(opens) >= 3 and len(highs) >= 3 and len(lows) >= 3:
            cs = detect_candlestick(opens, highs, lows, closes)
            scores['candlestick'] = cs.get('score', 0)
        else:
            scores['candlestick'] = 0
        
        # Seasonality
        seas = calculate_seasonality(closes)
        scores['seasonality'] = seas.get('score', 0)
        
        # Analyst rating (dari _analyst)
        analyst = indicators.get('_analyst', {}) or {}
        scores['analyst_rating'] = analyst.get('score', 0)
        
        # Elliott Wave
        ew = detect_elliott_wave(closes)
        scores['elliott_wave'] = ew.get('score', 0)
    except Exception:
        scores['candlestick'] = 0
        scores['seasonality'] = 0
        scores['analyst_rating'] = 0
        scores['elliott_wave'] = 0

    # === 23-26. FUNDAMENTAL ===
    fund = indicators.get('_fundamental', {}) or {}
    current_price_f = indicators.get('current_price')

    # 23. Market Cap
    mc = fund.get('market_cap')
    if mc:
        if mc > 10_000_000_000:
            scores['market_cap'] = +50
        elif mc > 2_000_000_000:
            scores['market_cap'] = +25
        elif mc > 300_000_000:
            scores['market_cap'] = 0
        else:
            scores['market_cap'] = -25
    else:
        scores['market_cap'] = 0

    # 24. 1Y Target Upside
    target = fund.get('one_year_target')
    if target and current_price_f:
        upside = ((target - current_price_f) / current_price_f) * 100
        if upside > 20:
            scores['target_upside'] = +75
        elif upside > 10:
            scores['target_upside'] = +50
        elif upside > 0:
            scores['target_upside'] = +25
        elif upside > -10:
            scores['target_upside'] = -25
        else:
            scores['target_upside'] = -75
    else:
        scores['target_upside'] = 0

    # 25. 52W Position
    w52_high = fund.get('week52_high')
    w52_low = fund.get('week52_low')
    if w52_high and w52_low and current_price_f and w52_high > w52_low:
        pos = (current_price_f - w52_low) / (w52_high - w52_low)
        scores['week52_position'] = round((0.5 - pos) * 200, 2)
    else:
        scores['week52_position'] = 0

    # 26. Dividend Yield
    dy = fund.get('dividend_yield')
    if dy is not None:
        if dy > 5:
            scores['dividend_yield'] = +50
        elif dy > 3:
            scores['dividend_yield'] = +25
        elif dy > 1:
            scores['dividend_yield'] = 0
        else:
            scores['dividend_yield'] = -25
    else:
        scores['dividend_yield'] = 0

    # === FINAL SCORE — Equal Weight ===
    valid_scores = [v for v in scores.values() if v is not None]
    aspek_count = len(valid_scores)
    final_score = sum(valid_scores) / aspek_count if aspek_count > 0 else 0
    final_score = round(final_score, 1)

    # === ACTION — Threshold 50 ===
    if final_score >= 50:
        action = 'BUY'
    elif final_score <= -50:
        action = 'SELL'
    else:
        action = 'HOLD'

    # === CONFIDENCE ===
    confidence = min(95, max(30, 50 + abs(final_score)))
    confidence = round(confidence, 1)

    return {
        'score': final_score,
        'action': action,
        'confidence': confidence,
        'breakdown': scores,
        'aspek_count': aspek_count,
        'aspek_aktif': list(scores.keys()),
        'weights': 'equal',
        'threshold': 50,
        'fase': 1,
    }


def calculate_macd(closes: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, Any]:
    """MACD — Moving Average Convergence Divergence."""
    if len(closes) < slow + signal:
        return {'macd': None, 'signal': None, 'histogram': None, 'trend': None}

    def ema(data, period):
        k = 2 / (period + 1)
        result = [data[0]]
        for i in range(1, len(data)):
            result.append(data[i] * k + result[-1] * (1 - k))
        return result

    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    macd_line = [ema_fast[i] - ema_slow[i] for i in range(len(closes))]
    signal_line = ema(macd_line, signal)
    histogram = macd_line[-1] - signal_line[-1]

    if histogram > 0:
        trend = 'BULLISH'
    elif histogram < 0:
        trend = 'BEARISH'
    else:
        trend = 'NEUTRAL'

    return {
        'macd': round(macd_line[-1], 4),
        'signal': round(signal_line[-1], 4),
        'histogram': round(histogram, 4),
        'trend': trend,
    }


def calculate_bollinger(closes: List[float], period: int = 20, std_mult: float = 2.0) -> Dict[str, Any]:
    """Bollinger Bands."""
    if len(closes) < period:
        return {'upper': None, 'middle': None, 'lower': None, 'position': None, 'signal': None}

    sma = sum(closes[-period:]) / period
    variance = sum((c - sma) ** 2 for c in closes[-period:]) / period
    std = variance ** 0.5

    upper = sma + std_mult * std
    lower = sma - std_mult * std
    current = closes[-1]

    if upper == lower:
        position = 0.5
    else:
        position = (current - lower) / (upper - lower)

    if position > 0.95:
        signal = 'OVERBOUGHT'
    elif position < 0.05:
        signal = 'OVERSOLD'
    else:
        signal = 'NEUTRAL'

    return {
        'upper': round(upper, 2),
        'middle': round(sma, 2),
        'lower': round(lower, 2),
        'position': round(position, 3),
        'signal': signal,
    }


def calculate_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Optional[float]:
    """Average True Range."""
    if len(closes) < period + 1:
        return None

    trs = []
    for i in range(1, len(closes)):
        hl = highs[i] - lows[i]
        hc = abs(highs[i] - closes[i-1])
        lc = abs(lows[i] - closes[i-1])
        trs.append(max(hl, hc, lc))

    return round(sum(trs[-period:]) / period, 4)


def calculate_stochastic(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Dict[str, Any]:
    """Stochastic Oscillator."""
    if len(closes) < period:
        return {'k': None, 'd': None, 'signal': None}

    highest = max(highs[-period:])
    lowest = min(lows[-period:])

    if highest == lowest:
        k = 50.0
    else:
        k = ((closes[-1] - lowest) / (highest - lowest)) * 100

    if k > 80:
        signal = 'OVERBOUGHT'
    elif k < 20:
        signal = 'OVERSOLD'
    else:
        signal = 'NEUTRAL'

    return {'k': round(k, 2), 'd': round(k, 2), 'signal': signal}


def calculate_obv(closes: List[float], volumes: List[float]) -> Dict[str, Any]:
    """On-Balance Volume."""
    if len(closes) < 2 or len(volumes) < 2:
        return {'obv': None, 'trend': None}

    obv = [0]
    for i in range(1, len(closes)):
        if closes[i] > closes[i-1]:
            obv.append(obv[-1] + volumes[i])
        elif closes[i] < closes[i-1]:
            obv.append(obv[-1] - volumes[i])
        else:
            obv.append(obv[-1])

    # Trend: bandingkan OBV sekarang vs 10 hari lalu
    if len(obv) >= 10:
        if obv[-1] > obv[-10]:
            trend = 'BULLISH'
        elif obv[-1] < obv[-10]:
            trend = 'BEARISH'
        else:
            trend = 'NEUTRAL'
    else:
        trend = 'NEUTRAL'

    return {'obv': obv[-1], 'trend': trend}


def calculate_vwap(highs: List[float], lows: List[float], closes: List[float], volumes: List[float], period: int = 20) -> Optional[float]:
    """Volume Weighted Average Price."""
    if len(closes) < period or len(volumes) < period:
        return None

    typical = [(highs[i] + lows[i] + closes[i]) / 3 for i in range(-period, 0)]
    vols = volumes[-period:]
    total_vol = sum(vols)
    if total_vol == 0:
        return None

    return round(sum(typical[i] * vols[i] for i in range(period)) / total_vol, 2)


def calculate_fibonacci(highs: List[float], lows: List[float], period: int = 20) -> Dict[str, Any]:
    """Fibonacci Retracement levels."""
    if len(highs) < period or len(lows) < period:
        return {'levels': {}, 'nearest': None}

    high = max(highs[-period:])
    low = min(lows[-period:])
    diff = high - low

    if diff == 0:
        return {'levels': {}, 'nearest': None}

    levels = {
        '0.236': round(high - diff * 0.236, 2),
        '0.382': round(high - diff * 0.382, 2),
        '0.500': round(high - diff * 0.500, 2),
        '0.618': round(high - diff * 0.618, 2),
        '0.786': round(high - diff * 0.786, 2),
    }

    current = closes_ref = None
    # nearest level
    nearest = None
    min_dist = float('inf')
    for level_name, level_price in levels.items():
        dist = abs(level_price - (high + low) / 2)
        if dist < min_dist:
            min_dist = dist
            nearest = level_name

    return {'levels': levels, 'nearest': nearest}


def calculate_volume_profile(closes: List[float], volumes: List[float], bins: int = 10) -> Dict[str, Any]:
    """Volume Profile — POC (Point of Control)."""
    if len(closes) < bins or len(volumes) < bins:
        return {'poc': None, 'value_area_high': None, 'value_area_low': None}

    min_price = min(closes)
    max_price = max(closes)
    if max_price == min_price:
        return {'poc': round(min_price, 2), 'value_area_high': round(max_price, 2), 'value_area_low': round(min_price, 2)}

    bin_size = (max_price - min_price) / bins
    bin_volumes = [0] * bins

    for i, c in enumerate(closes):
        idx = min(int((c - min_price) / bin_size), bins - 1)
        bin_volumes[idx] += volumes[i]

    poc_idx = bin_volumes.index(max(bin_volumes))
    poc = min_price + (poc_idx + 0.5) * bin_size

    return {
        'poc': round(poc, 2),
        'value_area_high': round(max_price, 2),
        'value_area_low': round(min_price, 2),
    }


def fetch_fundamental(symbol: str) -> Dict[str, Any]:
    """
    Fetch fundamental data dari Nasdaq /summary endpoint.

    Return:
    {
        'market_cap': int or None,
        'dividend_yield': float or None,
        'annualized_dividend': float or None,
        'one_year_target': float or None,
        'sector': str or None,
        'industry': str or None,
        'avg_volume': int or None,
        'week52_high': float or None,
        'week52_low': float or None,
        'previous_close': float or None,
        'source': 'nasdaq_summary',
    }
    """
    import requests

    result = {
        'market_cap': None,
        'dividend_yield': None,
        'annualized_dividend': None,
        'one_year_target': None,
        'sector': None,
        'industry': None,
        'avg_volume': None,
        'week52_high': None,
        'week52_low': None,
        'previous_close': None,
        'source': 'nasdaq_summary',
    }

    try:
        url = f'https://api.nasdaq.com/api/quote/{symbol}/summary?assetclass=stocks'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://www.nasdaq.com',
            'referer': 'https://www.nasdaq.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        summary = data.get('data', {}).get('summaryData', {}) or {}

        # Helper: ambil value
        def get_val(key):
            item = summary.get(key, {})
            return item.get('value') if isinstance(item, dict) else None

        # Market Cap
        mc = get_val('MarketCap')
        if mc and mc not in ('N/A', ''):
            try:
                result['market_cap'] = int(str(mc).replace(',', ''))
            except (ValueError, TypeError):
                pass

        # Dividend Yield
        dy = get_val('Yield')
        if dy and dy not in ('N/A', ''):
            try:
                result['dividend_yield'] = float(str(dy).replace('%', ''))
            except (ValueError, TypeError):
                pass

        # Annualized Dividend
        ad = get_val('AnnualizedDividend')
        if ad and ad not in ('N/A', ''):
            try:
                result['annualized_dividend'] = float(str(ad).replace('$', '').replace(',', ''))
            except (ValueError, TypeError):
                pass

        # 1 Year Target
        t = get_val('OneYrTarget')
        if t and t not in ('N/A', ''):
            try:
                result['one_year_target'] = float(str(t).replace('$', '').replace(',', ''))
            except (ValueError, TypeError):
                pass

        # Sector
        result['sector'] = get_val('Sector')

        # Industry
        result['industry'] = get_val('Industry')

        # Average Volume
        av = get_val('AverageVolume')
        if av and av not in ('N/A', ''):
            try:
                result['avg_volume'] = int(str(av).replace(',', ''))
            except (ValueError, TypeError):
                pass

        # 52 Week High/Low
        w52 = get_val('FiftTwoWeekHighLow')
        if w52 and w52 not in ('N/A', ''):
            try:
                parts = str(w52).split('/')
                if len(parts) == 2:
                    result['week52_high'] = float(parts[0].replace('$', '').replace(',', ''))
                    result['week52_low'] = float(parts[1].replace('$', '').replace(',', ''))
            except (ValueError, TypeError):
                pass

        # Previous Close
        pc = get_val('PreviousClose')
        if pc and pc not in ('N/A', ''):
            try:
                result['previous_close'] = float(str(pc).replace('$', '').replace(',', ''))
            except (ValueError, TypeError):
                pass

    except Exception as e:
        result['error'] = str(e)

    return result


def score_fundamental(data: Dict[str, Any]) -> Dict[str, float]:
    """
    Score fundamental — P/E, P/B, EPS, Market Cap, Dividend.

    Return dict dengan skor -100..100 per aspek.
    """
    scores = {}

    # === P/E Ratio ===
    pe = data.get('pe_ratio')
    if pe is not None:
        if pe < 0:
            scores['pe'] = -50  # laba negatif
        elif pe < 10:
            scores['pe'] = +75  # sangat murah
        elif pe < 20:
            scores['pe'] = +50  # murah
        elif pe < 30:
            scores['pe'] = 0    # wajar
        elif pe < 50:
            scores['pe'] = -25  # mahal
        else:
            scores['pe'] = -50  # sangat mahal
    else:
        scores['pe'] = 0

    # === P/B Ratio (estimasi dari P/E) ===
    # Kalau tidak ada data P/B, skip
    pb = data.get('pb_ratio')
    if pb is not None:
        if pb < 1:
            scores['pb'] = +75  # di bawah book value
        elif pb < 3:
            scores['pb'] = +25
        elif pb < 5:
            scores['pb'] = 0
        else:
            scores['pb'] = -50
    else:
        scores['pb'] = 0

    # === EPS ===
    eps = data.get('eps')
    if eps is not None:
        if eps > 0:
            scores['eps'] = +50  # laba positif
        else:
            scores['eps'] = -75  # laba negatif
    else:
        scores['eps'] = 0

    # === Market Cap ===
    mc = data.get('market_cap')
    if mc is not None:
        if mc > 10_000_000_000:      # > $10B = large cap
            scores['market_cap'] = +50
        elif mc > 2_000_000_000:     # $2B-$10B = mid cap
            scores['market_cap'] = +25
        elif mc > 300_000_000:       # $300M-$2B = small cap
            scores['market_cap'] = 0
        else:                        # < $300M = micro cap
            scores['market_cap'] = -25
    else:
        scores['market_cap'] = 0

    # === Dividend Yield ===
    dy = data.get('dividend_yield')
    if dy is not None:
        if dy > 5:
            scores['dividend'] = +50  # yield tinggi
        elif dy > 2:
            scores['dividend'] = +25  # yield bagus
        elif dy > 0:
            scores['dividend'] = 0
        else:
            scores['dividend'] = -25  # tidak ada dividend
    else:
        scores['dividend'] = 0

    return scores


def calculate_correlation(symbol: str, benchmark: str = 'SPY', days: int = 90) -> Dict[str, Any]:
    """Hitung korelasi saham dengan benchmark (S&P 500) — align by date object."""
    import requests
    import statistics

    result = {'correlation_90d': None, 'correlation_30d': None, 'beta': None, 'benchmark': benchmark}

    try:
        from datetime import datetime as _dt, timedelta as _td
        fromdate = (_dt.now() - _td(days=730)).strftime('%Y-%m-%d')
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'accept': 'application/json'}

        ETF_LIST = {'SPY', 'QQQ', 'IWM', 'DIA', 'VTI', 'VOO', 'IVV', 'XLK', 'XLF', 'XLE', 'XLV', 'XLI', 'XLP', 'XLY', 'XLU', 'XLB', 'XLRE', 'XLC'}

        def _parse_date(date_str):
            """Parse MM/DD/YYYY → datetime.date."""
            if not date_str:
                return None
            s = str(date_str).strip()
            for fmt in ('%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y'):
                try:
                    return _dt.strptime(s, fmt).date()
                except (ValueError, TypeError):
                    continue
            return None

        def _fetch(sym):
            """Fetch dan return dict {date_obj: close}."""
            assetclass = 'etf' if sym.upper() in ETF_LIST else 'stocks'
            url = f'https://api.nasdaq.com/api/quote/{sym}/historical?assetclass={assetclass}&fromdate={fromdate}&limit=9999'
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code != 200:
                return {}
            try:
                data = r.json()
            except Exception:
                return {}
            if not data or not isinstance(data, dict):
                return {}
            rows = data.get('data', {}).get('tradesTable', {}).get('rows', []) if data.get('data') else []
            out = {}
            for row in rows:
                d = _parse_date(row.get('date'))
                c = row.get('close', '').replace('$', '').replace(',', '').strip()
                if d and c and c != 'N/A':
                    try:
                        out[d] = float(c)
                    except (ValueError, TypeError):
                        pass
            return out

        sym_data = _fetch(symbol)
        bench_data = _fetch(benchmark)

        # Align by date object (sorted)
        common_dates = sorted(set(sym_data.keys()) & set(bench_data.keys()))
        result['sym_closes'] = len(sym_data)
        result['bench_closes'] = len(bench_data)
        result['common_dates'] = len(common_dates)

        if len(common_dates) >= 30:
            sym_closes = [sym_data[d] for d in common_dates]
            bench_closes = [bench_data[d] for d in common_dates]

            sym_rets = [(sym_closes[i] - sym_closes[i-1]) / sym_closes[i-1] for i in range(1, len(sym_closes))]
            bench_rets = [(bench_closes[i] - bench_closes[i-1]) / bench_closes[i-1] for i in range(1, len(bench_closes))]

            # 90 hari
            s90, b90 = sym_rets[-90:], bench_rets[-90:]
            if len(s90) >= 20:
                mean_s, mean_b = statistics.mean(s90), statistics.mean(b90)
                cov = sum((s90[i]-mean_s)*(b90[i]-mean_b) for i in range(len(s90))) / len(s90)
                std_s = statistics.stdev(s90) if len(s90) > 1 else 1
                std_b = statistics.stdev(b90) if len(b90) > 1 else 1
                if std_s > 0 and std_b > 0:
                    result['correlation_90d'] = round(cov / (std_s * std_b), 3)
                    result['beta'] = round(cov / (std_b ** 2), 3)

            # 30 hari
            s30, b30 = sym_rets[-30:], bench_rets[-30:]
            if len(s30) >= 15:
                mean_s, mean_b = statistics.mean(s30), statistics.mean(b30)
                cov = sum((s30[i]-mean_s)*(b30[i]-mean_b) for i in range(len(s30))) / len(s30)
                std_s = statistics.stdev(s30) if len(s30) > 1 else 1
                std_b = statistics.stdev(b30) if len(b30) > 1 else 1
                if std_s > 0 and std_b > 0:
                    result['correlation_30d'] = round(cov / (std_s * std_b), 3)
    except Exception as e:
        result['error'] = str(e)

    return result

def score_correlation(data: Dict[str, Any]) -> Dict[str, float]:
    """Score correlation & beta."""
    scores = {}
    
    # Correlation S&P 500
    corr = data.get('correlation_90d')
    if corr is not None:
        if corr > 0.8:
            scores['corr_sp500'] = -25  # terlalu terikat market
        elif corr > 0.5:
            scores['corr_sp500'] = 0
        elif corr > 0:
            scores['corr_sp500'] = +25  # diversifikasi
        else:
            scores['corr_sp500'] = +50  # negatif = hedge
    else:
        scores['corr_sp500'] = 0
    
    # Beta
    beta = data.get('beta')
    if beta is not None:
        if beta > 1.5:
            scores['beta'] = -50  # sangat volatil
        elif beta > 1.0:
            scores['beta'] = -25  # lebih volatil dari market
        elif beta > 0.5:
            scores['beta'] = +25  # kurang volatil
        elif beta > 0:
            scores['beta'] = +50  # defensif
        else:
            scores['beta'] = +75  # inverse
    else:
        scores['beta'] = 0
    
    # Correlation Sektor (placeholder — sama dengan S&P untuk sekarang)
    scores['corr_sector'] = scores.get('corr_sp500', 0)
    
    return scores


def fetch_sentiment(symbol: str) -> Dict[str, Any]:
    """Fetch sentimen berita dari RSS feed (Yahoo Finance)."""
    import requests
    import re
    
    result = {'sentiment_score': 0, 'headline_count': 0, 'sources': [], 'source': 'rss'}
    
    try:
        url = f'https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US'
        headers = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            items = re.findall(r'<title>(.*?)</title>', r.text)
            items = [i for i in items if i and i.lower() != f'{symbol.lower()} - yahoo finance']
            
            # Simple sentiment: keyword-based
            positive_words = ['up', 'rise', 'gain', 'surge', 'bull', 'strong', 'beat', 'record', 'high', 'growth']
            negative_words = ['down', 'fall', 'drop', 'plunge', 'bear', 'weak', 'miss', 'low', 'loss', 'cut']
            
            pos_count = 0
            neg_count = 0
            for item in items:
                lower = item.lower()
                pos_count += sum(1 for w in positive_words if w in lower)
                neg_count += sum(1 for w in negative_words if w in lower)
            
            total = pos_count + neg_count
            if total > 0:
                result['sentiment_score'] = round((pos_count - neg_count) / total * 100, 1)
            result['headline_count'] = len(items)
            result['sources'] = items[:5]
    except Exception as e:
        result['error'] = str(e)
    
    return result


def score_sentiment(data: Dict[str, Any]) -> Dict[str, float]:
    """Score sentimen."""
    scores = {}
    
    sent = data.get('sentiment_score', 0)
    count = data.get('headline_count', 0)
    
    if count > 0:
        if sent > 50:
            scores['sentiment'] = +75
        elif sent > 20:
            scores['sentiment'] = +50
        elif sent > -20:
            scores['sentiment'] = 0
        elif sent > -50:
            scores['sentiment'] = -50
        else:
            scores['sentiment'] = -75
    else:
        scores['sentiment'] = 0
    
    # Social sentiment (placeholder = sama)
    scores['social_sentiment'] = scores['sentiment']
    
    return scores


def detect_candlestick(opens: List[float], highs: List[float], lows: List[float], closes: List[float]) -> Dict[str, Any]:
    """Deteksi pola candlestick sederhana."""
    if len(closes) < 3:
        return {'patterns': [], 'score': 0}
    
    patterns = []
    
    # Engulfing Bullish
    if len(closes) >= 2:
        prev_body = closes[-2] - opens[-2]
        curr_body = closes[-1] - opens[-1]
        if prev_body < 0 and curr_body > 0 and curr_body > abs(prev_body) * 1.2:
            patterns.append('bullish_engulfing')
    
    # Hammer
    body = abs(closes[-1] - opens[-1])
    lower_shadow = min(opens[-1], closes[-1]) - lows[-1]
    upper_shadow = highs[-1] - max(opens[-1], closes[-1])
    if body > 0 and lower_shadow > body * 2 and upper_shadow < body:
        patterns.append('hammer')
    
    # Doji
    if body < (highs[-1] - lows[-1]) * 0.1:
        patterns.append('doji')
    
    score = 0
    if 'bullish_engulfing' in patterns or 'hammer' in patterns:
        score = +50
    elif 'doji' in patterns:
        score = 0
    
    return {'patterns': patterns, 'score': score}


def calculate_seasonality(closes: List[float]) -> Dict[str, Any]:
    """Hitung seasonality sederhana (monthly performance)."""
    if len(closes) < 60:
        return {'score': 0, 'month_avg': None}
    
    # Rata-rata return bulanan (proxy)
    monthly_returns = []
    for i in range(20, min(len(closes), 240), 20):
        ret = (closes[i] - closes[i-20]) / closes[i-20] * 100
        monthly_returns.append(ret)
    
    if monthly_returns:
        avg = sum(monthly_returns) / len(monthly_returns)
        if avg > 3:
            score = +50
        elif avg > 1:
            score = +25
        elif avg > -1:
            score = 0
        elif avg > -3:
            score = -25
        else:
            score = -50
        return {'score': score, 'month_avg': round(avg, 2)}
    
    return {'score': 0, 'month_avg': None}


def fetch_insider(symbol: str) -> Dict[str, Any]:
    """Fetch insider trading (placeholder)."""
    return {'net_buying': 0, 'score': 0}


def fetch_short_interest(symbol: str) -> Dict[str, Any]:
    """Fetch short interest (placeholder)."""
    return {'short_pct': None, 'score': 0}


def fetch_options_flow(symbol: str) -> Dict[str, Any]:
    """Fetch options flow (placeholder)."""
    return {'put_call_ratio': None, 'score': 0}


def fetch_analyst_rating(symbol: str) -> Dict[str, Any]:
    """Fetch analyst rating dari Nasdaq summary."""
    import requests
    result = {'rating': None, 'target': None, 'score': 0}
    
    try:
        url = f'https://api.nasdaq.com/api/quote/{symbol}/summary?assetclass=stocks'
        headers = {'user-agent': 'Mozilla/5.0', 'accept': 'application/json'}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        summary = data.get('data', {}).get('summaryData', {}) or {}
        
        target_item = summary.get('OneYrTarget', {})
        target_str = target_item.get('value', '') if isinstance(target_item, dict) else ''
        
        if target_str and target_str != 'N/A':
            try:
                target = float(target_str.replace('$', '').replace(',', ''))
                result['target'] = target
                result['score'] = +25  # ada target = analis follow
            except (ValueError, TypeError):
                pass
    except Exception as e:
        result['error'] = str(e)
    
    return result


def detect_elliott_wave(closes: List[float]) -> Dict[str, Any]:
    """Deteksi Elliott Wave (placeholder sederhana)."""
    if len(closes) < 30:
        return {'wave': None, 'score': 0}
    
    # Simple: cek apakah ada 5 wave naik atau turun
    recent = closes[-30:]
    if recent[-1] > recent[0]:
        return {'wave': 'impulse_up', 'score': +25}
    else:
        return {'wave': 'impulse_down', 'score': -25}


__all__ = [
    'calculate_indicators',
    'score_indicators',
    'analyze_multi_timeframe',
    'analyze_unified',
    'detect_elliott_wave',
    'fetch_analyst_rating',
    'fetch_options_flow',
    'fetch_short_interest',
    'fetch_insider',
    'calculate_seasonality',
    'detect_candlestick',
    'score_sentiment',
    'fetch_sentiment',
    'score_correlation',
    'calculate_correlation',
    'score_fundamental',
    'fetch_fundamental',
    'calculate_rsi',
    'calculate_sma',
    'calculate_ema',
    'calculate_volatility',
    'calculate_volume_profile',
    'calculate_fibonacci',
    'calculate_vwap',
    'calculate_obv',
    'calculate_stochastic',
    'calculate_atr',
    'calculate_bollinger',
    'calculate_macd',
]
