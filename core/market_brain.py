# core/market_brain.py
# ============================================================
# MARKET BRAIN — Comprehensive Analysis
# ============================================================
# Gabung technical indicators + Brain pipeline + prediction
# untuk analisis market paling lengkap.

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def _make_json_safe(obj, depth=0, max_depth=10, _seen=None):
    """
    Ubah objek jadi JSON-safe — hindari circular reference.
    
    Handle: dict, list, tuple, str, int, float, bool, None
    Selain itu → str(obj)
    """
    if _seen is None:
        _seen = set()
    
    if depth > max_depth:
        return f"<max_depth_exceeded: {type(obj).__name__}>"
    
    # Primitive
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    
    # Deteksi circular reference
    obj_id = id(obj)
    if obj_id in _seen:
        return f"<circular_ref: {type(obj).__name__}>"
    
    _seen = _seen | {obj_id}
    
    # Dict
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            try:
                key_str = str(k)
                result[key_str] = _make_json_safe(v, depth + 1, max_depth, _seen)
            except Exception:
                continue
        return result
    
    # List / tuple
    if isinstance(obj, (list, tuple)):
        return [_make_json_safe(item, depth + 1, max_depth, _seen) for item in obj[:200]]
    
    # Set
    if isinstance(obj, set):
        return list(obj)[:200]
    
    # Datetime
    if hasattr(obj, 'isoformat'):
        try:
            return obj.isoformat()
        except Exception:
            pass
    
    # Enum
    if hasattr(obj, 'value'):
        try:
            return _make_json_safe(obj.value, depth + 1, max_depth, _seen)
        except Exception:
            pass
    
    # Objek dengan to_dict
    if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
        try:
            return _make_json_safe(obj.to_dict(), depth + 1, max_depth, _seen)
        except Exception:
            pass
    
    # Fallback: string
    try:
        return str(obj)[:500]
    except Exception:
        return f"<unstringifiable: {type(obj).__name__}>"


def analyze_market_full(
    symbol: str,
    rows: List[Dict[str, Any]],
    market_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Analisis market dengan SELURUH kemampuan Brain.
    
    Input:
        symbol: 'MMM'
        rows: historical dari Nasdaq (descending)
        market_context: dari bulk market (optional)
    
    Output: dict lengkap dengan semua data Brain
    """
    result = {
        'symbol': symbol,
        'timestamp': datetime.now().isoformat(),
        'total_days': len(rows),
    }
    
    if not rows:
        return {**result, 'error': 'No data'}
    
    # ============================================================
    # 1. TECHNICAL INDICATORS
    # ============================================================
    try:
        from core.market_indicators import (
            calculate_indicators,
            analyze_multi_timeframe,
            parse_price,
        )
        
        result['indicators'] = calculate_indicators(rows)
        result['multi_timeframe'] = analyze_multi_timeframe(rows)
    except Exception as e:
        logger.error(f"Indicators error: {e}")
        result['indicators'] = {'error': str(e)}
        result['multi_timeframe'] = {'error': str(e)}
    
    # ============================================================
    # 2. PREDICTION (Monte Carlo)
    # ============================================================
    prediction = {}
    try:
        from core.market_indicators import parse_price
        import random
        import statistics

        # Ambil 252 hari (1 tahun) harga — ascending
        closes = []
        for r in rows[:252]:
            p = parse_price(r.get('close'))
            if p is not None:
                closes.append(p)
        closes = list(reversed(closes))

        if len(closes) >= 30:
            current_price = closes[-1]

            # Returns harian
            returns = []
            for i in range(1, len(closes)):
                ret = (closes[i] - closes[i - 1]) / closes[i - 1]
                returns.append(ret)

            if returns:
                mean_ret = statistics.mean(returns)
                std_ret = statistics.stdev(returns) if len(returns) > 1 else 0.0

                # Monte Carlo: 1000 iterasi, 30 hari
                outcomes = []
                for _ in range(1000):
                    price = current_price
                    for _ in range(30):
                        change = random.gauss(mean_ret, std_ret)
                        price *= (1 + change)
                    outcomes.append(price)
                outcomes.sort()

                prob_up = sum(1 for o in outcomes if o > current_price) / len(outcomes) * 100
                prob_down = sum(1 for o in outcomes if o < current_price) / len(outcomes) * 100

                prediction = {
                    'current_price': round(current_price, 2),
                    'days': 30,
                    'iterations': 1000,
                    'target_mean': round(statistics.mean(outcomes), 2),
                    'target_median': round(statistics.median(outcomes), 2),
                    'p5': round(outcomes[50], 2),
                    'p95': round(outcomes[950], 2),
                    'prob_up': round(prob_up, 1),
                    'prob_down': round(prob_down, 1),
                    'expected_return_pct': round(((statistics.mean(outcomes) - current_price) / current_price) * 100, 2),
                    'volatility_daily': round(std_ret * 100, 2),
                    'scenarios': {
                        'bullish': round(outcomes[850], 2),
                        'base': round(outcomes[500], 2),
                        'bearish': round(outcomes[150], 2),
                    },
                    'source': 'monte_carlo',
                }
            else:
                prediction = {'error': 'No returns'}
        else:
            prediction = {'error': f'Only {len(closes)} days'}
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        prediction = {'error': str(e)}

    result['prediction'] = prediction

    # ============================================================
    # 3. FEED KE BRAIN
    # ============================================================
    brain_output = {}
    try:
        from core.brain import brain as global_brain

        if global_brain is not None:
            # Baca state saja — JANGAN panggil brain.observe()
            last = getattr(global_brain, 'last_result', None) or {}
            
            # State — pastikan string
            state_str = 'UNKNOWN'
            try:
                if hasattr(global_brain, 'state') and hasattr(global_brain.state, 'value'):
                    state_str = str(global_brain.state.value)
            except Exception:
                pass
            
            # Metrics — pastikan dict primitif
            metrics_dict = {}
            try:
                m = getattr(global_brain, 'metrics', {}) or {}
                metrics_dict = {
                    'cycles': int(m.get('total_cycles', 0)),
                    'errors': int(getattr(global_brain, 'errors', 0) or 0),
                    'successful_cycles': int(m.get('successful_cycles', 0)),
                    'decision_count': int(m.get('decision_count', 0)),
                    'learning_count': int(m.get('learning_count', 0)),
                }
            except Exception:
                metrics_dict = {}
            
            brain_output = {
                'cycle': int(getattr(global_brain, 'cycles', 0) or 0),
                'state': state_str,
                'metrics': metrics_dict,
                'last_decision': last.get('decision') if isinstance(last.get('decision'), dict) else {},
                'note': 'Brain state, not market-specific',
            }
    except Exception as e:
        logger.error(f"Brain state error: {e}")
        brain_output = {'error': str(e)}

    result['brain'] = brain_output

    # ============================================================
    # 3b. MARKET DECISION
    # ============================================================
    market_decision = {}
    try:
        indicators = result.get('indicators', {}) or {}
        mtf = result.get('multi_timeframe', {}) or {}
        overall = mtf.get('overall', {}) or {}
        
        action = overall.get('action', 'HOLD')
        confidence = overall.get('confidence', 50)
        
        rsi = indicators.get('rsi')
        trend = indicators.get('trend_sma')
        support = indicators.get('support')
        resistance = indicators.get('resistance')
        current_price = indicators.get('current_price')
        
        reasons = []
        if rsi is not None:
            if rsi < 30:
                reasons.append(f"RSI {rsi} — oversold, potensi bounce")
            elif rsi > 70:
                reasons.append(f"RSI {rsi} — overbought, potensi koreksi")
            else:
                reasons.append(f"RSI {rsi} — netral")
        
        if trend == 'BULLISH':
            reasons.append("Tren jangka pendek bullish")
        elif trend == 'BEARISH':
            reasons.append("Tren jangka pendek bearish")
        
        if current_price and support and resistance:
            range_pos = (current_price - support) / (resistance - support) if (resistance - support) > 0 else 0.5
            if range_pos < 0.2:
                reasons.append(f"Dekat support ${support}")
            elif range_pos > 0.8:
                reasons.append(f"Dekat resistance ${resistance}")
        
        entry = stop = target = None
        if current_price:
            if action == 'BUY':
                entry = round(current_price * 1.005, 2)
                stop = round(support * 0.99, 2) if support else round(current_price * 0.95, 2)
                target = round(resistance * 0.99, 2) if resistance else round(current_price * 1.05, 2)
            elif action == 'SELL':
                entry = round(current_price * 0.995, 2)
                stop = round(resistance * 1.01, 2) if resistance else round(current_price * 1.05, 2)
                target = round(support * 1.01, 2) if support else round(current_price * 0.95, 2)
        
        market_decision = {
            'action': action,
            'confidence': confidence,
            'score': overall.get('score', 0),
            'reasons': reasons[:5],
            'insights': overall.get('insights', []),
            'levels': {
                'current': current_price,
                'support': support,
                'resistance': resistance,
                'entry': entry,
                'stop': stop,
                'target': target,
            },
        }
    except Exception as e:
        logger.debug(f"Market decision error: {e}")
        market_decision = {'error': str(e)}

    result['market_decision'] = market_decision

    
    # ============================================================
    # 4. REFLECTION
    # ============================================================
    reflection = {}
    try:
        from core.brain import brain as global_brain
        if global_brain is not None:
            refl = global_brain.reflection()
            reflection = {
                'awareness': refl.get('awareness'),
                'emotion': refl.get('emotion'),
                'curiosity': refl.get('curiosity'),
                'insight_depth': refl.get('insight_depth'),
                'resilience': refl.get('resilience'),
                'focus': refl.get('focus'),
                'confidence': refl.get('confidence'),
                'stability': refl.get('stability'),
                'reflection_quality': refl.get('reflection_quality'),
                'insights': refl.get('insights', [])[:5],
            }
    except Exception as e:
        logger.debug(f"Reflection error: {e}")
    
    result['reflection'] = reflection
    
    # ============================================================
    # 5. SELF-MODEL
    # ============================================================
    self_model = {}
    try:
        from core.brain import brain as global_brain
        if global_brain is not None and hasattr(global_brain, 'self_model') and global_brain.self_model:
            self_model = global_brain.self_model.summary()
    except Exception as e:
        logger.debug(f"Self model error: {e}")
    
    result['self_model'] = self_model
    
    # ============================================================
    # 6. KNOWLEDGE — Similar Cases
    # ============================================================
    knowledge_context = {}
    try:
        from core.knowledge import knowledge as global_knowledge
        
        if global_knowledge is not None:
            # Cari knowledge terkait symbol
            try:
                related = global_knowledge.search(symbol, max_results=5)
                knowledge_context['related_items'] = [
                    {'content': getattr(k, 'content', '')[:150], 'category': getattr(k, 'category', '')}
                    for k in (related or [])
                ]
            except Exception:
                knowledge_context['related_items'] = []
            
            # Stats
            try:
                stats = global_knowledge.stats()
                knowledge_context['total_items'] = stats.total
                knowledge_context['categories'] = len(stats.by_category) if hasattr(stats, 'by_category') else 0
            except Exception:
                pass
    except Exception as e:
        logger.debug(f"Knowledge error: {e}")
    
    result['knowledge_context'] = knowledge_context
    
    # ============================================================
    # 7. ADAPTIVE WEIGHTS
    # ============================================================
    adaptive = {}
    try:
        from core.learning import adaptive_engine
        if adaptive_engine is not None:
            all_data = adaptive_engine.get_all()
            if isinstance(all_data, dict):
                adaptive = {
                    'entries': [
                        {
                            'key': k,
                            'weight': getattr(v, 'weight', 0) if not isinstance(v, dict) else v.get('weight', 0),
                            'confidence': getattr(v, 'confidence', 0) if not isinstance(v, dict) else v.get('confidence', 0),
                        }
                        for k, v in list(all_data.items())[:10]
                    ],
                    'total': len(all_data),
                }
    except Exception as e:
        logger.debug(f"Adaptive error: {e}")
    
    result['adaptive'] = adaptive
    
    # ============================================================
    # 8. EXPERIENCE STATS
    # ============================================================
    experience = {}
    try:
        from core.learning import experience_engine
        if experience_engine is not None:
            experience = {
                'total': experience_engine.count() if hasattr(experience_engine, 'count') else 0,
            }
    except Exception as e:
        logger.debug(f"Experience error: {e}")
    
    result['experience'] = experience
    
    # Sanitasi — hindari circular reference
    return _make_json_safe(result)


__all__ = ['analyze_market_full', '_make_json_safe']
