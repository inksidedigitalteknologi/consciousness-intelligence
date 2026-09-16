from __future__ import annotations

import logging
import statistics
import json
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
from collections import deque, Counter
import math

# ============================================================
# HEALTH IMPORT
# ============================================================

try:
    from core.health import set_status
except ImportError:
    def set_status(*args, **kwargs):
        pass

# ============================================================
# AI INTEGRATION
# ============================================================

try:
    from core.deepseek import deepseek_ai
    DEEPSEEK_AVAILABLE = True
    DEEPSEEK_ENABLED = deepseek_ai.enabled if hasattr(deepseek_ai, 'enabled') else False
except ImportError:
    DEEPSEEK_AVAILABLE = False
    DEEPSEEK_ENABLED = False
    deepseek_ai = None

logger = logging.getLogger(__name__)

if DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED:
    logger.info("🤖 DeepSeek AI Integration: ENABLED for Signal Engine")
else:
    logger.info("🤖 DeepSeek AI Integration: DISABLED for Signal Engine")

# ============================================================
# CONSTANTS
# ============================================================

SIGNAL_BUY = "BUY"
SIGNAL_STRONG_BUY = "STRONG_BUY"
SIGNAL_SELL = "SELL"
SIGNAL_STRONG_SELL = "STRONG_SELL"
SIGNAL_HOLD = "HOLD"
SIGNAL_MONITOR = "MONITOR"
SIGNAL_WAIT = "WAIT"
SIGNAL_EXIT = "EXIT"

SIGNAL_QUALITY_EXCELLENT = "EXCELLENT"
SIGNAL_QUALITY_GOOD = "GOOD"
SIGNAL_QUALITY_FAIR = "FAIR"
SIGNAL_QUALITY_WEAK = "WEAK"
SIGNAL_QUALITY_NEUTRAL = "NEUTRAL"
SIGNAL_QUALITY_AI_VALIDATED = "AI_VALIDATED"

MARKET_TRENDING_BULLISH = "TRENDING_BULLISH"
MARKET_TRENDING_BEARISH = "TRENDING_BEARISH"
MARKET_RANGING = "RANGING"
MARKET_NEUTRAL = "NEUTRAL"
MARKET_VOLATILE = "VOLATILE"
MARKET_BREAKOUT = "BREAKOUT"
MARKET_BREAKDOWN = "BREAKDOWN"
MARKET_ACCUMULATION = "ACCUMULATION"
MARKET_DISTRIBUTION = "DISTRIBUTION"

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_EXTREME = "EXTREME"

# ============================================================
# SIGNAL ENGINE v5.0
# ============================================================

class SignalEngine:
    """
    Signal Engine v5.0 - Super Comprehensive Signal Generator with AI.
    
    Menggunakan weighted multi-factor analysis + AI validation untuk
    menghasilkan sinyal trading yang akurat dengan confidence scoring.
    """

    VERSION = "5.0.0"

    # ============================================================
    # WEIGHT CONFIGURATION - OPTIMIZED
    # ============================================================

    WEIGHTS = {
        "mtf": 25,
        "trend": 20,
        "ema": 15,
        "adx": 12,
        "macd": 10,
        "volume": 10,
        "breakout": 10,
        "rsi": 8,
        "bollinger": 5,
        "momentum": 5,
        "candle": 5,
        "divergence": 5,
        "support_resistance": 5,
        "volatility": 3,
        "seasonality": 2,
        "sentiment": 3,
        "correlation": 2,
    }

    MAX_SCORE = sum(WEIGHTS.values())

    # ============================================================
    # SIGNAL THRESHOLDS - DYNAMIC
    # ============================================================

    THRESHOLDS = {
        "strong_buy": 80,
        "buy": 65,
        "weak_buy": 50,
        "weak_sell": 50,
        "sell": 65,
        "strong_sell": 80,
        "hold_max": 45,
        "monitor_min": 40,
        "exit_min": 70,
    }

    # ============================================================
    # CONFIDENCE THRESHOLDS
    # ============================================================

    CONFIDENCE = {
        "very_high": 85,
        "high": 75,
        "medium": 55,
        "low": 35,
        "very_low": 20,
    }

    # ============================================================
    # RISK SETTINGS - OPTIMIZED
    # ============================================================

    RISK = {
        "atr_sl": 1.5,
        "tp1_rr": 1.5,
        "tp2_rr": 2.5,
        "tp3_rr": 4.0,
        "max_risk_percent": 2.0,
        "min_risk_reward": 1.0,
        "optimal_risk_reward": 2.5,
        "dynamic_sizing": True,
        "risk_adj_factor": 1.0,
        "max_position_size": 100.0,
        "min_position_size": 1.0,
    }

    # ============================================================
    # TIMEFRAME WEIGHTS
    # ============================================================

    TIMEFRAME_WEIGHTS = {
        "1m": 0.5,
        "5m": 1.0,
        "15m": 1.5,
        "30m": 2.0,
        "1h": 2.5,
        "2h": 3.0,
        "4h": 3.5,
        "6h": 4.0,
        "8h": 4.5,
        "12h": 5.0,
        "1d": 6.0,
        "1w": 7.0,
        "1M": 8.0,
    }

    # ============================================================
    # INIT
    # ============================================================

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        self.weights = self.config.get("weights", self.WEIGHTS.copy())
        self.thresholds = self.config.get("thresholds", self.THRESHOLDS.copy())
        self.confidence_thresholds = self.config.get("confidence", self.CONFIDENCE.copy())
        self.risk_settings = self.config.get("risk", self.RISK.copy())
        self.timeframe_weights = self.config.get("timeframe_weights", self.TIMEFRAME_WEIGHTS.copy())
        
        self.total_signals = 0
        self.buy_signals = 0
        self.sell_signals = 0
        self.hold_signals = 0
        self.ai_validated = 0
        self.history: List[Dict[str, Any]] = []
        self.max_history = self.config.get("max_history", 2000)
        self.performance: Dict[str, Any] = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "accuracy": 0.0,
            "win_rate": 0.0,
            "avg_win": 0.0,
            "avg_loss": 0.0,
            "profit_factor": 0.0,
            "sharpe_ratio": 0.0,
        }
        self._signal_cache: Dict[str, Any] = {}
        self._cache_ttl = 60
        
        # AI Status
        self.ai_enabled = DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED
        
        logger.info("Signal Engine v%s initialized.", self.VERSION)
        logger.info("🤖 AI Integration: %s", "ENABLED" if self.ai_enabled else "DISABLED")
        set_status("signal_engine", "INITIALIZED")

    # ============================================================
    # NORMALIZE ANALYSIS
    # ============================================================

    def _normalize_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize analysis data for consistent processing."""
        if not analysis:
            return {}
        if isinstance(analysis, dict):
            return analysis
        if hasattr(analysis, 'to_dict'):
            return analysis.to_dict()
        if hasattr(analysis, '__dict__'):
            return analysis.__dict__
        return {"raw": str(analysis)}

    # ============================================================
    # MAIN SIGNAL GENERATOR
    # ============================================================

    def generate_signal(self, analysis: Dict[str, Any], use_ai: bool = True) -> Dict[str, Any]:
        """
        Generate trading signal from market analysis with AI enhancement.
        
        Args:
            analysis: Market analysis data
            use_ai: Enable AI validation
            
        Returns:
            Complete signal with entry, SL, TP, confidence, and AI insights
        """
        if not analysis:
            return self._empty_signal("No analysis data")

        try:
            start_time = time.time()
            pair = analysis.get("pair", analysis.get("symbol", "UNKNOWN"))
            
            # Check cache
            cache_key = f"{pair}_{hash(str(analysis))}"
            if cache_key in self._signal_cache:
                cached = self._signal_cache[cache_key]
                if (time.time() - cached.get('_cache_time', 0)) < self._cache_ttl:
                    logger.debug(f"Cache hit for {pair}")
                    return cached
            
            data = self._normalize_analysis(analysis)
            
            # Market context
            market_regime = self._detect_market_regime(data)
            trend = self._detect_trend(data)
            volatility = self._detect_volatility(data)
            sentiment = self._detect_sentiment(data)
            
            # Evaluate all factors
            buy_score, sell_score, reasons, warnings, evidence = self._evaluate_all_factors(data)
            
            # Normalize scores
            buy_score = self._normalize_score(buy_score)
            sell_score = self._normalize_score(sell_score)
            
            # Determine signal
            signal = self._determine_signal(buy_score, sell_score, market_regime, data)
            
            # Calculate confidence
            confidence = self._calculate_confidence(buy_score, sell_score, signal, market_regime, data)
            
            # Get entry price
            entry = self._get_entry_price(data)
            
            # Calculate risk levels
            risk = self._calculate_risk_levels(entry, data, signal)
            
            # Calculate signal quality
            quality = self._calculate_signal_quality(signal, confidence, risk["risk_reward"], warnings, data)
            
            # Generate recommendation
            recommendation = self._generate_recommendation(signal, confidence, market_regime, quality, data)
            
            # Build result
            result = {
                "engine_version": self.VERSION,
                "pair": pair,
                "symbol": pair,
                "signal": signal,
                "trend": trend,
                "market_regime": market_regime,
                "volatility": volatility,
                "sentiment": sentiment,
                "confidence": confidence,
                "strength": max(buy_score, sell_score),
                "buy_score": buy_score,
                "sell_score": sell_score,
                "entry": risk["entry"],
                "stop_loss": risk["stop_loss"],
                "take_profit_1": risk["take_profit_1"],
                "take_profit_2": risk["take_profit_2"],
                "take_profit_3": risk["take_profit_3"],
                "risk_reward": risk["risk_reward"],
                "risk_level": risk["risk_level"],
                "position_size": risk["position_size"],
                "signal_quality": quality,
                "recommendation": recommendation,
                "reasons": self._unique(reasons[:10]),
                "warnings": self._unique(warnings[:5]),
                "evidence": self._unique(evidence[:5]),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "processing_time": round((time.time() - start_time) * 1000, 2),
            }
            
            # AI Enhancement
            if use_ai and self.ai_enabled:
                try:
                    ai_result = self._enhance_with_ai(result, data)
                    result = {**result, **ai_result}
                except Exception as e:
                    logger.warning(f"AI enhancement failed: {e}")
                    result['ai_status'] = 'error'
                    result['ai_error'] = str(e)
            
            # Cache result
            result['_cache_time'] = time.time()
            self._signal_cache[cache_key] = result
            
            # Record history
            self._record_history(result)
            
            # Update statistics
            self._update_statistics(signal)
            
            set_status("signal_engine", "ONLINE")
            
            logger.info(
                "%s | BUY %.2f | SELL %.2f | SIGNAL %s | QUALITY %s | CONF %.2f%% | AI %s",
                pair, buy_score, sell_score, signal, quality, confidence,
                "✅" if result.get('ai_validated', False) else "❌"
            )
            
            return result

        except Exception as e:
            logger.exception("Signal Engine Error: %s", e)
            set_status("signal_engine", "ERROR")
            return self._empty_signal(str(e), analysis.get("pair", "UNKNOWN"))

    # ============================================================
    # AI ENHANCEMENT
    # ============================================================

    def _enhance_with_ai(self, signal: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance signal with AI insights."""
        if not self.ai_enabled:
            return {'ai_validated': False, 'ai_status': 'disabled'}
        
        try:
            context = f"""
Signal Analysis:
- Pair: {signal.get('pair')}
- Signal: {signal.get('signal')}
- Confidence: {signal.get('confidence')}%
- Quality: {signal.get('signal_quality')}
- Buy Score: {signal.get('buy_score')}
- Sell Score: {signal.get('sell_score')}
- Market Regime: {signal.get('market_regime')}
- Risk Level: {signal.get('risk_level')}
- Risk/Reward: {signal.get('risk_reward')}

Top Reasons:
{chr(10).join(['- ' + r for r in signal.get('reasons', [])[:5]])}
"""
            
            prompt = f"""Validasi sinyal trading ini dengan sangat teliti:

1. APAKAH SINYAL INI VALID? Berikan alasan kuat (Ya/Tidak)
2. SKOR VALIDASI: 1-100
3. KEKUATAN: Skor 1-10
4. RISIKO UTAMA: Apa risiko terbesar?
5. REKOMENDASI: Apakah Anda setuju? Mengapa?
6. INSIGHT: Insight tambahan yang berharga

Berikan analisis kritis dan objektif.
"""
            
            ai_response = deepseek_ai.ask(
                question=prompt,
                context=context,
                system_prompt="analyst",
                temperature=0.4,
                max_tokens=512
            )
            
            # Parse AI response
            validation_score = self._parse_ai_validation(ai_response)
            is_valid = validation_score >= 60
            
            # Store in knowledge
            from core.knowledge import knowledge
            knowledge.add(
                content=f"AI Signal Validation for {signal.get('pair')}: {ai_response[:300]}...",
                category="signal",
                type="ai_validation",
                tags=["ai", "signal", signal.get('pair', '').replace('/', '_')],
                confidence=validation_score,
                importance=0.7,
                metadata={
                    'pair': signal.get('pair'),
                    'signal': signal.get('signal'),
                    'confidence': signal.get('confidence'),
                    'validation_score': validation_score,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            self.ai_validated += 1
            
            return {
                'ai_validated': True,
                'ai_status': 'success',
                'ai_validation': ai_response,
                'ai_validation_score': validation_score,
                'ai_is_valid': is_valid,
                'ai_confidence_boost': 5 if is_valid and validation_score > 75 else 0,
                'ai_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AI enhancement error: {e}")
            return {
                'ai_validated': False,
                'ai_status': 'error',
                'ai_error': str(e)
            }

    def _parse_ai_validation(self, response: str) -> int:
        """Parse validation score from AI response."""
        score = 70
        try:
            response_lower = response.lower()
            
            # Look for score patterns
            import re
            score_patterns = [
                r'(?:score|skor|validasi)\s*[:=]\s*(\d+)',
                r'(\d+)\s*(?:%|percent)',
                r'skor\s+(\d+)',
            ]
            
            for pattern in score_patterns:
                match = re.search(pattern, response_lower)
                if match:
                    score = int(match.group(1))
                    break
            
            # Quality indicators
            if 'sangat valid' in response_lower or 'excellent' in response_lower:
                score = min(100, score + 15)
            if 'valid' in response_lower and 'tidak' not in response_lower:
                score = max(score, 70)
            if 'weak' in response_lower or 'lemah' in response_lower:
                score = min(score, 50)
            if 'high risk' in response_lower or 'risiko tinggi' in response_lower:
                score = max(0, score - 20)
            
            return max(0, min(100, score))
            
        except Exception as e:
            logger.debug(f"AI score parsing error: {e}")
            return 70

    # ============================================================
    # EVALUATE ALL FACTORS
    # ============================================================

    def _evaluate_all_factors(self, data: Dict[str, Any]) -> Tuple[float, float, List[str], List[str], List[str]]:
        """Evaluate all factors and return scores."""
        buy_score = 0
        sell_score = 0
        reasons = []
        warnings = []
        evidence = []
        
        evaluators = [
            ("mtf", self._evaluate_mtf),
            ("trend", self._evaluate_trend),
            ("ema", self._evaluate_ema),
            ("adx", self._evaluate_adx),
            ("macd", self._evaluate_macd),
            ("volume", self._evaluate_volume),
            ("breakout", self._evaluate_breakout),
            ("rsi", self._evaluate_rsi),
            ("bollinger", self._evaluate_bollinger),
            ("momentum", self._evaluate_momentum),
            ("candle", self._evaluate_candle_pattern),
            ("divergence", self._evaluate_divergence),
            ("sr", self._evaluate_support_resistance),
            ("volatility", self._evaluate_volatility_factor),
            ("sentiment", self._evaluate_sentiment),
            ("correlation", self._evaluate_correlation),
        ]
        
        for name, evaluator in evaluators:
            try:
                result = evaluator(data)
                buy_score += result.get("buy", 0)
                sell_score += result.get("sell", 0)
                reasons.extend(result.get("reasons", []))
                warnings.extend(result.get("warnings", []))
                evidence.extend(result.get("evidence", []))
            except Exception as e:
                logger.debug(f"Evaluator {name} failed: {e}")
                warnings.append(f"{name} analysis unavailable")
        
        return buy_score, sell_score, reasons, warnings, evidence

    # ============================================================
    # ENHANCED EVALUATORS
    # ============================================================

    def _evaluate_mtf(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": [], "warnings": []}
        
        timeframes = data.get("timeframes")
        if not isinstance(timeframes, dict):
            return result
        
        bullish = 0
        bearish = 0
        total = 0
        
        for tf, direction in timeframes.items():
            weight = self.timeframe_weights.get(str(tf).lower(), 1)
            direction = str(direction).upper()
            total += weight
            if direction == "BULLISH":
                bullish += weight
                result["reasons"].append(f"{tf} bullish")
            elif direction == "BEARISH":
                bearish += weight
                result["reasons"].append(f"{tf} bearish")
        
        if total > 0:
            buy = (bullish / total) * self.weights["mtf"]
            sell = (bearish / total) * self.weights["mtf"]
            
            if buy >= 8:
                result["buy"] = round(buy, 2)
                result["reasons"].append("Weighted MTF bullish alignment")
            if sell >= 8:
                result["sell"] = round(sell, 2)
                result["reasons"].append("Weighted MTF bearish alignment")
            
            # Check alignment strength
            if abs(bullish - bearish) / total > 0.6:
                result["reasons"].append("Strong MTF alignment")
        
        return result

    def _evaluate_trend(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        trend = self._detect_trend(data)
        if trend == "BULLISH":
            result["buy"] = self.weights["trend"]
            result["reasons"].append("Overall bullish market trend")
        elif trend == "BEARISH":
            result["sell"] = self.weights["trend"]
            result["reasons"].append("Overall bearish market trend")
        
        return result

    def _evaluate_ema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        price = self._get_entry_price(data)
        ema9 = data.get("ema9")
        ema21 = data.get("ema21")
        ema50 = data.get("ema50")
        ema200 = data.get("ema200")
        
        buy = 0
        sell = 0
        
        if price and ema9:
            if price > ema9:
                buy += 3
                result["reasons"].append("Price above EMA9")
            else:
                sell += 3
                result["reasons"].append("Price below EMA9")
        
        if ema9 and ema21:
            if ema9 > ema21:
                buy += 4
                result["reasons"].append("EMA9 above EMA21 (bullish)")
            else:
                sell += 4
                result["reasons"].append("EMA9 below EMA21 (bearish)")
        
        if ema50 and ema200:
            if ema50 > ema200:
                buy += 8
                result["reasons"].append("EMA50 above EMA200 (golden cross)")
            else:
                sell += 8
                result["reasons"].append("EMA50 below EMA200 (death cross)")
        
        result["buy"] = min(buy, self.weights["ema"])
        result["sell"] = min(sell, self.weights["ema"])
        
        return result

    def _evaluate_adx(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        adx = data.get("adx")
        if adx is None:
            return result
        
        trend = self._detect_trend(data)
        
        if adx >= 25:
            if trend == "BULLISH":
                result["buy"] = self.weights["adx"]
                result["reasons"].append(f"ADX {adx:.1f} confirms strong bullish trend")
            elif trend == "BEARISH":
                result["sell"] = self.weights["adx"]
                result["reasons"].append(f"ADX {adx:.1f} confirms strong bearish trend")
            else:
                result["reasons"].append(f"ADX {adx:.1f} strong trend, direction unclear")
        elif adx >= 20:
            result["reasons"].append(f"ADX {adx:.1f} moderate trend")
            result["buy"] = self.weights["adx"] * 0.3
            result["sell"] = self.weights["adx"] * 0.3
        else:
            result["reasons"].append(f"ADX {adx:.1f} weak trend - ranging market")
        
        return result

    def _evaluate_macd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        macd = data.get("macd")
        signal = data.get("macd_signal")
        histogram = data.get("macd_histogram")
        
        if macd is None or signal is None:
            return result
        
        if macd > signal:
            result["buy"] += 7
            result["reasons"].append("MACD bullish crossover")
        else:
            result["sell"] += 7
            result["reasons"].append("MACD bearish crossover")
        
        if histogram is not None:
            if histogram > 0:
                result["buy"] += 3
                if abs(histogram) > 0.1:
                    result["reasons"].append("MACD histogram positive & growing")
                else:
                    result["reasons"].append("MACD histogram positive")
            else:
                result["sell"] += 3
                if abs(histogram) > 0.1:
                    result["reasons"].append("MACD histogram negative & falling")
                else:
                    result["reasons"].append("MACD histogram negative")
        
        result["buy"] = min(result["buy"], self.weights["macd"])
        result["sell"] = min(result["sell"], self.weights["macd"])
        
        return result

    def _evaluate_volume(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": [], "warnings": []}
        
        volume = data.get("volume")
        average = data.get("average_volume")
        
        if not volume or not average:
            result["warnings"].append("Volume data insufficient")
            return result
        
        ratio = volume / average
        trend = self._detect_trend(data)
        
        if ratio >= 1.5:
            if trend == "BULLISH":
                result["buy"] = self.weights["volume"]
                result["reasons"].append(f"High volume {ratio:.1f}x confirms bullish movement")
            elif trend == "BEARISH":
                result["sell"] = self.weights["volume"]
                result["reasons"].append(f"High volume {ratio:.1f}x confirms bearish movement")
            else:
                result["reasons"].append(f"High volume {ratio:.1f}x with neutral trend")
        elif ratio < 0.7:
            result["warnings"].append(f"Low volume {ratio:.1f}x - weak confirmation")
            result["buy"] = self.weights["volume"] * 0.3
            result["sell"] = self.weights["volume"] * 0.3
        else:
            result["reasons"].append(f"Volume {ratio:.1f}x at normal levels")
            result["buy"] = self.weights["volume"] * 0.5
            result["sell"] = self.weights["volume"] * 0.5
        
        return result

    def _evaluate_breakout(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        price = self._get_entry_price(data)
        resistance = data.get("resistance")
        support = data.get("support")
        volume_ratio = data.get("volume_ratio", 0)
        
        if not price:
            return result
        
        # Breakout with volume confirmation
        if resistance and price > resistance:
            if volume_ratio > 1.5:
                result["buy"] = self.weights["breakout"]
                result["reasons"].append(f"Bullish breakout with volume {volume_ratio:.1f}x")
            else:
                result["buy"] = self.weights["breakout"] * 0.6
                result["reasons"].append("Bullish breakout (low volume confirmation)")
        
        # Breakdown with volume confirmation
        elif support and price < support:
            if volume_ratio > 1.5:
                result["sell"] = self.weights["breakout"]
                result["reasons"].append(f"Bearish breakdown with volume {volume_ratio:.1f}x")
            else:
                result["sell"] = self.weights["breakout"] * 0.6
                result["reasons"].append("Bearish breakdown (low volume confirmation)")
        
        return result

    def _evaluate_rsi(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": [], "warnings": []}
        
        rsi = data.get("rsi")
        if rsi is None:
            return result
        
        if rsi < 25:
            result["buy"] = self.weights["rsi"]
            result["reasons"].append(f"RSI {rsi:.1f} severely oversold")
        elif rsi < 30:
            result["buy"] = self.weights["rsi"] * 0.9
            result["reasons"].append(f"RSI {rsi:.1f} oversold - recovery potential")
        elif 30 <= rsi < 40:
            result["buy"] = self.weights["rsi"] * 0.6
            result["reasons"].append(f"RSI {rsi:.1f} near oversold")
        elif 40 <= rsi < 50:
            result["buy"] = self.weights["rsi"] * 0.3
            result["sell"] = self.weights["rsi"] * 0.3
            result["reasons"].append(f"RSI {rsi:.1f} neutral zone")
        elif 50 <= rsi < 60:
            result["buy"] = self.weights["rsi"] * 0.5
            result["reasons"].append(f"RSI {rsi:.1f} bullish momentum")
        elif 60 <= rsi < 70:
            result["buy"] = self.weights["rsi"] * 0.7
            result["reasons"].append(f"RSI {rsi:.1f} strong bullish momentum")
        elif 70 <= rsi < 75:
            result["sell"] = self.weights["rsi"] * 0.7
            result["reasons"].append(f"RSI {rsi:.1f} approaching overbought")
        elif 75 <= rsi < 80:
            result["sell"] = self.weights["rsi"] * 0.9
            result["warnings"].append(f"RSI {rsi:.1f} overbought")
        else:
            result["sell"] = self.weights["rsi"]
            result["warnings"].append(f"RSI {rsi:.1f} severely overbought")
        
        return result

    def _evaluate_bollinger(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        price = self._get_entry_price(data)
        upper = data.get("bb_upper")
        lower = data.get("bb_lower")
        middle = data.get("bb_middle")
        bb_width = data.get("bb_width")
        
        if not price:
            return result
        
        if lower and price <= lower:
            result["buy"] = self.weights["bollinger"]
            result["reasons"].append("Price at lower Bollinger Band (oversold)")
        elif upper and price >= upper:
            result["sell"] = self.weights["bollinger"]
            result["reasons"].append("Price at upper Bollinger Band (overbought)")
        elif middle and price > middle * 1.02:
            result["buy"] = self.weights["bollinger"] * 0.5
            result["reasons"].append("Price above middle Bollinger Band")
        elif middle and price < middle * 0.98:
            result["sell"] = self.weights["bollinger"] * 0.5
            result["reasons"].append("Price below middle Bollinger Band")
        
        # Bollinger Squeeze
        if bb_width and bb_width < 0.5:
            result["reasons"].append("Bollinger squeeze detected - potential breakout")
        
        return result

    def _evaluate_momentum(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        momentum = data.get("momentum")
        roc = data.get("roc")
        price = self._get_entry_price(data)
        
        if momentum is not None:
            if momentum > 0:
                result["buy"] = self.weights["momentum"]
                result["reasons"].append(f"Positive momentum {momentum:.2f}")
            elif momentum < 0:
                result["sell"] = self.weights["momentum"]
                result["reasons"].append(f"Negative momentum {momentum:.2f}")
        
        if roc is not None:
            if roc > 0:
                result["buy"] += 2
                if momentum is not None:
                    result["reasons"].append(f"ROC {roc:.2f}% positive")
            else:
                result["sell"] += 2
                result["reasons"].append(f"ROC {roc:.2f}% negative")
        
        result["buy"] = min(result["buy"], self.weights["momentum"])
        result["sell"] = min(result["sell"], self.weights["momentum"])
        
        return result

    def _evaluate_candle_pattern(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        patterns = data.get("patterns")
        if isinstance(patterns, str):
            patterns = [patterns]
        elif not isinstance(patterns, list):
            return result
        
        bullish_patterns = [
            "HAMMER", "BULLISH_ENGULFING", "MORNING_STAR",
            "THREE_WHITE_SOLDIERS", "BULLISH_HARAMI", "PIERCING_LINE",
            "DOJI", "SPINNING_TOP", "BULLISH_MARUBOZU"
        ]
        
        bearish_patterns = [
            "SHOOTING_STAR", "BEARISH_ENGULFING", "EVENING_STAR",
            "THREE_BLACK_CROWS", "BEARISH_HARAMI", "DARK_CLOUD_COVER",
            "BEARISH_MARUBOZU", "HANGING_MAN"
        ]
        
        for pattern in patterns:
            p = str(pattern).upper()
            if p in bullish_patterns:
                result["buy"] += 2
                result["reasons"].append(f"Bullish candle pattern: {p}")
            elif p in bearish_patterns:
                result["sell"] += 2
                result["reasons"].append(f"Bearish candle pattern: {p}")
        
        result["buy"] = min(result["buy"], self.weights["candle"])
        result["sell"] = min(result["sell"], self.weights["candle"])
        
        return result

    def _evaluate_divergence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        price_history = data.get("price_history", [])
        macd_history = data.get("macd_history", [])
        rsi_history = data.get("rsi_history", [])
        
        # MACD Divergence
        if len(price_history) >= 3 and len(macd_history) >= 3:
            # Bullish divergence (price lower low, MACD higher low)
            if (price_history[-1] < price_history[-2] and 
                macd_history[-1] > macd_history[-2]):
                result["buy"] = self.weights["divergence"]
                result["reasons"].append("Bullish MACD divergence detected")
            
            # Bearish divergence (price higher high, MACD lower high)
            if (price_history[-1] > price_history[-2] and 
                macd_history[-1] < macd_history[-2]):
                result["sell"] = self.weights["divergence"]
                result["reasons"].append("Bearish MACD divergence detected")
        
        # RSI Divergence
        if len(price_history) >= 3 and len(rsi_history) >= 3:
            if (price_history[-1] < price_history[-2] and 
                rsi_history[-1] > rsi_history[-2]):
                result["buy"] += self.weights["divergence"] * 0.5
                result["reasons"].append("Bullish RSI divergence detected")
            
            if (price_history[-1] > price_history[-2] and 
                rsi_history[-1] < rsi_history[-2]):
                result["sell"] += self.weights["divergence"] * 0.5
                result["reasons"].append("Bearish RSI divergence detected")
        
        result["buy"] = min(result["buy"], self.weights["divergence"])
        result["sell"] = min(result["sell"], self.weights["divergence"])
        
        return result

    def _evaluate_support_resistance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        price = self._get_entry_price(data)
        support = data.get("support")
        resistance = data.get("resistance")
        
        if not price:
            return result
        
        if support and resistance:
            range_width = resistance - support
            if range_width > 0:
                position = (price - support) / range_width
                
                if position < 0.15:
                    result["buy"] = self.weights["support_resistance"]
                    result["reasons"].append("Price at strong support")
                elif position < 0.3:
                    result["buy"] = self.weights["support_resistance"] * 0.6
                    result["reasons"].append("Price near support zone")
                elif position > 0.85:
                    result["sell"] = self.weights["support_resistance"]
                    result["reasons"].append("Price at strong resistance")
                elif position > 0.7:
                    result["sell"] = self.weights["support_resistance"] * 0.6
                    result["reasons"].append("Price near resistance zone")
                elif 0.4 <= position <= 0.6:
                    result["reasons"].append("Price in middle of range")
        
        return result

    def _evaluate_volatility_factor(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"buy": 0, "sell": 0, "reasons": [], "warnings": []}
        
        atr = data.get("atr")
        price = self._get_entry_price(data)
        
        if atr and price and price > 0:
            atr_percent = (atr / price) * 100
            
            if atr_percent > 5:
                result["warnings"].append(f"Very high volatility {atr_percent:.1f}% - increased risk")
                result["sell"] = self.weights["volatility"] * 0.5
            elif atr_percent > 3:
                result["warnings"].append(f"High volatility {atr_percent:.1f}%")
                result["buy"] = self.weights["volatility"] * 0.3
            elif atr_percent > 1:
                result["buy"] = self.weights["volatility"] * 0.5
                result["reasons"].append(f"Normal volatility {atr_percent:.1f}%")
            else:
                result["buy"] = self.weights["volatility"]
                result["reasons"].append(f"Low volatility {atr_percent:.1f}% - stable environment")
        
        return result

    def _evaluate_sentiment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate market sentiment."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        sentiment = data.get("sentiment")
        if sentiment is None:
            return result
        
        sentiment_score = float(sentiment) if isinstance(sentiment, (int, float)) else 0
        
        if sentiment_score > 60:
            result["buy"] = self.weights["sentiment"] * (sentiment_score / 100)
            result["reasons"].append(f"Sentiment score {sentiment_score:.1f} (bullish)")
        elif sentiment_score < 40:
            result["sell"] = self.weights["sentiment"] * ((100 - sentiment_score) / 100)
            result["reasons"].append(f"Sentiment score {sentiment_score:.1f} (bearish)")
        else:
            result["reasons"].append(f"Sentiment score {sentiment_score:.1f} (neutral)")
        
        return result

    def _evaluate_correlation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate correlation with market."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        correlation = data.get("correlation")
        if correlation is None:
            return result
        
        if abs(correlation) > 0.7:
            direction = "bullish" if correlation > 0 else "bearish"
            result["buy" if correlation > 0 else "sell"] = self.weights["correlation"]
            result["reasons"].append(f"High correlation {correlation:.2f} with market ({direction})")
        else:
            result["reasons"].append(f"Low correlation {correlation:.2f} - independent movement")
        
        return result

    # ============================================================
    # MARKET CONTEXT DETECTION
    # ============================================================

    def _detect_market_regime(self, data: Dict[str, Any]) -> str:
        """Detect current market regime."""
        adx = data.get("adx")
        trend = self._detect_trend(data)
        atr_percent = data.get("atr_percent", 0)
        price = self._get_entry_price(data)
        
        # Breakout detection
        resistance = data.get("resistance")
        if resistance and price and price > resistance * 1.01:
            return MARKET_BREAKOUT
        
        support = data.get("support")
        if support and price and price < support * 0.99:
            return MARKET_BREAKDOWN
        
        # Trending
        if adx is not None:
            if adx >= 25:
                if trend == "BULLISH":
                    return MARKET_TRENDING_BULLISH
                if trend == "BEARISH":
                    return MARKET_TRENDING_BEARISH
            elif adx < 20:
                return MARKET_RANGING
        
        # Volatility
        if atr_percent > 3:
            return MARKET_VOLATILE
        
        return MARKET_NEUTRAL

    def _detect_trend(self, data: Dict[str, Any]) -> str:
        """Detect market trend from multiple sources."""
        custom = data.get("trend")
        if custom:
            return str(custom).upper()
        
        price = self._get_entry_price(data)
        ema50 = data.get("ema50")
        ema200 = data.get("ema200")
        sma20 = data.get("sma20")
        adx = data.get("adx")
        
        bullish_score = 0
        bearish_score = 0
        
        if price and ema50 and ema200:
            if price > ema50 > ema200:
                bullish_score += 4
            elif price < ema50 < ema200:
                bearish_score += 4
        
        if price and sma20:
            if price > sma20:
                bullish_score += 1
            else:
                bearish_score += 1
        
        if adx and adx >= 25:
            if price and ema50:
                if price > ema50:
                    bullish_score += 2
                else:
                    bearish_score += 2
        
        if bullish_score > bearish_score:
            return "BULLISH"
        elif bearish_score > bullish_score:
            return "BEARISH"
        return "NEUTRAL"

    def _detect_volatility(self, data: Dict[str, Any]) -> str:
        """Detect volatility level."""
        atr = data.get("atr")
        price = self._get_entry_price(data)
        
        if atr and price and price > 0:
            atr_percent = (atr / price) * 100
            if atr_percent > 5:
                return "HIGH"
            elif atr_percent > 2:
                return "MEDIUM"
            else:
                return "LOW"
        
        volatility = data.get("volatility")
        if volatility:
            if volatility > 3:
                return "HIGH"
            elif volatility > 1:
                return "MEDIUM"
            else:
                return "LOW"
        
        return "MEDIUM"

    def _detect_sentiment(self, data: Dict[str, Any]) -> float:
        """Detect market sentiment score 0-100."""
        sentiment = data.get("sentiment")
        if sentiment is not None:
            try:
                return float(sentiment)
            except (ValueError, TypeError):
                pass
        
        # Calculate from price action
        price = self._get_entry_price(data)
        ema21 = data.get("ema21")
        ema50 = data.get("ema50")
        
        if price and ema21 and ema50:
            if price > ema21 > ema50:
                return 70
            elif price < ema21 < ema50:
                return 30
        
        return 50

    # ============================================================
    # SCORE NORMALIZATION
    # ============================================================

    def _normalize_score(self, score: float) -> float:
        """Normalize score to percentage (0-100)."""
        if score <= 0:
            return 0
        return round(min((score / self.MAX_SCORE) * 100, 100), 2)

    # ============================================================
    # SIGNAL DETERMINATION
    # ============================================================

    def _determine_signal(self, buy_score: float, sell_score: float, market_regime: str, data: Dict[str, Any]) -> str:
        """Determine final signal from scores."""
        diff = buy_score - sell_score
        
        # In ranging market, require higher confidence
        if market_regime in [MARKET_RANGING, MARKET_NEUTRAL]:
            if abs(diff) < 15:
                return SIGNAL_HOLD
            threshold_multiplier = 1.2
        else:
            threshold_multiplier = 1.0
        
        # Exit signal detection
        if abs(diff) > self.thresholds["exit_min"]:
            if sell_score > buy_score and sell_score > 70:
                return SIGNAL_EXIT
        
        # Buy signals
        if buy_score >= self.thresholds["strong_buy"] * threshold_multiplier and buy_score > sell_score:
            return SIGNAL_STRONG_BUY
        if buy_score >= self.thresholds["buy"] * threshold_multiplier and buy_score > sell_score:
            return SIGNAL_BUY
        if buy_score >= self.thresholds["weak_buy"] and buy_score > sell_score * 1.2:
            return SIGNAL_MONITOR
        
        # Sell signals
        if sell_score >= self.thresholds["strong_sell"] * threshold_multiplier and sell_score > buy_score:
            return SIGNAL_STRONG_SELL
        if sell_score >= self.thresholds["sell"] * threshold_multiplier and sell_score > buy_score:
            return SIGNAL_SELL
        if sell_score >= self.thresholds["weak_sell"] and sell_score > buy_score * 1.2:
            return SIGNAL_MONITOR
        
        return SIGNAL_HOLD

    # ============================================================
    # CONFIDENCE CALCULATION
    # ============================================================

    def _calculate_confidence(self, buy_score: float, sell_score: float, signal: str, market_regime: str, data: Dict[str, Any]) -> float:
        """Calculate confidence level with multiple factors."""
        if signal in [SIGNAL_HOLD, SIGNAL_WAIT]:
            return 0
        
        strength = max(buy_score, sell_score)
        difference = abs(buy_score - sell_score)
        consensus = difference / (strength + 1) * 100
        
        # Base confidence
        confidence = (
            strength * 0.35 +
            consensus * 0.25 +
            self._get_quality_boost(signal) * 0.20 +
            self._get_regime_confidence(market_regime) * 0.10 +
            self._get_volatility_adjustment(data) * 0.10
        )
        
        # AI confidence boost
        if self.ai_enabled and signal not in [SIGNAL_HOLD, SIGNAL_WAIT]:
            confidence += 3
        
        return round(min(confidence, 100), 2)

    def _get_quality_boost(self, signal: str) -> float:
        """Get quality boost based on signal strength."""
        if signal in [SIGNAL_STRONG_BUY, SIGNAL_STRONG_SELL]:
            return 15
        elif signal in [SIGNAL_BUY, SIGNAL_SELL]:
            return 10
        elif signal == SIGNAL_MONITOR:
            return 5
        return 0

    def _get_regime_confidence(self, market_regime: str) -> float:
        """Get confidence based on market regime."""
        if market_regime in [MARKET_TRENDING_BULLISH, MARKET_TRENDING_BEARISH]:
            return 15
        elif market_regime in [MARKET_BREAKOUT, MARKET_BREAKDOWN]:
            return 20
        elif market_regime == MARKET_RANGING:
            return 5
        return 10

    def _get_volatility_adjustment(self, data: Dict[str, Any]) -> float:
        """Get volatility adjustment for confidence."""
        volatility = self._detect_volatility(data)
        if volatility == "LOW":
            return 10
        elif volatility == "MEDIUM":
            return 5
        return 0

    # ============================================================
    # ENTRY PRICE
    # ============================================================

    def _get_entry_price(self, data: Dict[str, Any]) -> float:
        """Get entry price from data."""
        price_fields = [
            "price", "close", "last", "last_price",
            "current_price", "ticker_price", "mark_price"
        ]
        
        for field in price_fields:
            value = data.get(field)
            if value is not None:
                try:
                    value = float(value)
                    if value > 0:
                        return value
                except (ValueError, TypeError):
                    continue
        
        return 0.0

    # ============================================================
    # RISK MANAGEMENT
    # ============================================================

    def _calculate_risk_levels(self, entry: float, data: Dict[str, Any], signal: str) -> Dict[str, Any]:
        """Calculate risk levels with ATR-based SL/TP and dynamic sizing."""
        result = {
            "entry": round(entry, 8),
            "stop_loss": None,
            "take_profit_1": None,
            "take_profit_2": None,
            "take_profit_3": None,
            "risk_reward": 0,
            "risk_level": "UNKNOWN",
            "position_size": 0,
        }
        
        if entry <= 0:
            return result
        
        atr = data.get("atr") or data.get("ATR") or data.get("average_true_range")
        try:
            atr = float(atr) if atr is not None else 0
        except (ValueError, TypeError):
            atr = 0
        
        if atr <= 0:
            atr = entry * 0.015
        
        # Dynamic ATR adjustment based on volatility
        atr_percent = (atr / entry) * 100
        sl_multiplier = self.risk_settings["atr_sl"]
        
        if atr_percent > 5:
            sl_multiplier = self.risk_settings["atr_sl"] * 0.8
        elif atr_percent < 1:
            sl_multiplier = self.risk_settings["atr_sl"] * 1.2
        
        if signal in [SIGNAL_BUY, SIGNAL_STRONG_BUY, SIGNAL_MONITOR]:
            stop_loss = entry - (atr * sl_multiplier)
            risk = entry - stop_loss
            tp1 = entry + (risk * self.risk_settings["tp1_rr"])
            tp2 = entry + (risk * self.risk_settings["tp2_rr"])
            tp3 = entry + (risk * self.risk_settings["tp3_rr"])
            
        elif signal in [SIGNAL_SELL, SIGNAL_STRONG_SELL, SIGNAL_EXIT]:
            stop_loss = entry + (atr * sl_multiplier)
            risk = stop_loss - entry
            tp1 = entry - (risk * self.risk_settings["tp1_rr"])
            tp2 = entry - (risk * self.risk_settings["tp2_rr"])
            tp3 = entry - (risk * self.risk_settings["tp3_rr"])
            
        else:
            return result
        
        rr = self.risk_settings["tp2_rr"]
        
        # Dynamic position sizing
        position_size = 1.0
        if self.risk_settings.get("dynamic_sizing", True):
            base_size = 1.0
            volatility_adjustment = max(0.5, min(2.0, 1.5 / (atr_percent / 2)))
            confidence_adjustment = 1.0
            risk_adjustment = 1.0
            
            # Adjust for risk level
            if atr_percent > 5:
                risk_adjustment = 0.5
            elif atr_percent > 3:
                risk_adjustment = 0.75
            
            # Adjust for signal strength
            if signal in [SIGNAL_STRONG_BUY, SIGNAL_STRONG_SELL]:
                confidence_adjustment = 1.5
            elif signal in [SIGNAL_BUY, SIGNAL_SELL]:
                confidence_adjustment = 1.25
            
            position_size = base_size * volatility_adjustment * confidence_adjustment * risk_adjustment
            position_size = max(
                self.risk_settings.get("min_position_size", 1.0),
                min(self.risk_settings.get("max_position_size", 100.0), position_size)
            )
        
        result.update({
            "stop_loss": round(stop_loss, 8),
            "take_profit_1": round(tp1, 8),
            "take_profit_2": round(tp2, 8),
            "take_profit_3": round(tp3, 8),
            "risk_reward": rr,
            "position_size": round(position_size, 2),
        })
        
        # Risk level
        if atr_percent < 1:
            result["risk_level"] = RISK_LOW
        elif atr_percent < 2:
            result["risk_level"] = RISK_MEDIUM
        elif atr_percent < 4:
            result["risk_level"] = RISK_HIGH
        else:
            result["risk_level"] = RISK_EXTREME
        
        return result

    # ============================================================
    # SIGNAL QUALITY
    # ============================================================

    def _calculate_signal_quality(self, signal: str, confidence: float, risk_reward: float, warnings: List[str], data: Dict[str, Any]) -> str:
        """Calculate signal quality rating."""
        if signal in [SIGNAL_HOLD, SIGNAL_WAIT]:
            return SIGNAL_QUALITY_NEUTRAL
        
        score = 0
        
        # Confidence scoring
        if confidence >= 80:
            score += 40
        elif confidence >= 65:
            score += 30
        elif confidence >= 50:
            score += 20
        elif confidence >= 35:
            score += 10
        
        # Risk reward scoring
        if risk_reward >= 3:
            score += 30
        elif risk_reward >= 2:
            score += 20
        elif risk_reward >= 1.5:
            score += 10
        
        # Warning penalty
        if not warnings:
            score += 30
        elif len(warnings) <= 2:
            score += 15
        elif len(warnings) <= 5:
            score += 5
        
        # Signal strength bonus
        if signal in [SIGNAL_STRONG_BUY, SIGNAL_STRONG_SELL]:
            score += 10
        elif signal in [SIGNAL_BUY, SIGNAL_SELL]:
            score += 5
        
        # AI validation bonus
        if self.ai_enabled and signal not in [SIGNAL_HOLD, SIGNAL_WAIT]:
            score += 5
        
        # Market regime bonus
        regime = data.get("market_regime", "")
        if regime in [MARKET_TRENDING_BULLISH, MARKET_TRENDING_BEARISH]:
            score += 5
        
        if score >= 85:
            return SIGNAL_QUALITY_EXCELLENT
        elif score >= 65:
            return SIGNAL_QUALITY_GOOD
        elif score >= 40:
            return SIGNAL_QUALITY_FAIR
        return SIGNAL_QUALITY_WEAK

    # ============================================================
    # RECOMMENDATION
    # ============================================================

    def _generate_recommendation(self, signal: str, confidence: float, market_regime: str, quality: str, data: Dict[str, Any]) -> str:
        """Generate human-readable recommendation."""
        if signal in [SIGNAL_HOLD, SIGNAL_WAIT]:
            return "Wait for confirmation"
        
        recommendations = {
            SIGNAL_STRONG_BUY: "Strong Buy - Consider entering position with conviction",
            SIGNAL_BUY: "Buy - Good opportunity with confirmation",
            SIGNAL_SELL: "Sell - Good opportunity to exit",
            SIGNAL_STRONG_SELL: "Strong Sell - Consider exiting position",
            SIGNAL_MONITOR: "Monitor - Prepare for entry",
            SIGNAL_EXIT: "Exit - Close position to protect capital",
        }
        
        base = recommendations.get(signal, "Hold position")
        
        if confidence >= 85:
            base += " (very high confidence)"
        elif confidence >= 75:
            base += " (high confidence)"
        elif confidence >= 55:
            base += " (moderate confidence)"
        else:
            base += " (low confidence - proceed with caution)"
        
        if quality == SIGNAL_QUALITY_EXCELLENT:
            base += " - Excellent quality signal"
        elif quality == SIGNAL_QUALITY_WEAK:
            base += " - Weak signal, consider skipping"
        
        if market_regime in [MARKET_RANGING, MARKET_NEUTRAL]:
            base += " - Ranging market, manage expectations"
        elif market_regime == MARKET_VOLATILE:
            base += " - High volatility, use wider stops"
        elif market_regime in [MARKET_BREAKOUT, MARKET_BREAKDOWN]:
            base += " - Breakout detected, momentum may follow"
        
        if self.ai_enabled:
            base += " (AI validated)"
        
        return base

    # ============================================================
    # HISTORY & STATISTICS
    # ============================================================

    def _record_history(self, entry: Dict[str, Any]) -> None:
        """Record signal in history."""
        self.history.append(entry)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get signal history."""
        return self.history[-limit:] if self.history else []

    def get_statistics(self) -> Dict[str, Any]:
        """Get signal statistics."""
        total = self.total_signals
        if total == 0:
            return {
                "total": 0,
                "buy": 0,
                "sell": 0,
                "hold": 0,
                "buy_ratio": 0,
                "sell_ratio": 0,
                "accuracy": 0,
                "ai_validated": 0,
                "ai_ratio": 0,
            }
        
        return {
            "total": total,
            "buy": self.buy_signals,
            "sell": self.sell_signals,
            "hold": self.hold_signals,
            "buy_ratio": round((self.buy_signals / total) * 100, 2),
            "sell_ratio": round((self.sell_signals / total) * 100, 2),
            "accuracy": round(self.performance["accuracy"], 2),
            "ai_validated": self.ai_validated,
            "ai_ratio": round((self.ai_validated / total) * 100, 2) if total > 0 else 0,
            "win_rate": round(self.performance.get("win_rate", 0), 2),
            "profit_factor": round(self.performance.get("profit_factor", 0), 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _update_statistics(self, signal: str) -> None:
        """Update signal statistics."""
        self.total_signals += 1
        if signal in [SIGNAL_BUY, SIGNAL_STRONG_BUY]:
            self.buy_signals += 1
        elif signal in [SIGNAL_SELL, SIGNAL_STRONG_SELL]:
            self.sell_signals += 1
        else:
            self.hold_signals += 1

    def record_outcome(self, signal_id: str, success: bool, pnl: float = 0) -> None:
        """Record signal outcome for accuracy tracking."""
        self.performance["total"] += 1
        if success:
            self.performance["successful"] += 1
            if pnl > 0:
                self.performance["avg_win"] = ((self.performance["avg_win"] * (self.performance["successful"] - 1)) + pnl) / self.performance["successful"]
        else:
            self.performance["failed"] += 1
            if pnl < 0:
                self.performance["avg_loss"] = ((self.performance["avg_loss"] * (self.performance["failed"] - 1)) + abs(pnl)) / self.performance["failed"]
        
        total = self.performance["total"]
        self.performance["accuracy"] = (self.performance["successful"] / total * 100) if total > 0 else 0
        self.performance["win_rate"] = self.performance["accuracy"]
        
        if self.performance["avg_loss"] > 0:
            self.performance["profit_factor"] = self.performance["avg_win"] / self.performance["avg_loss"]
        else:
            self.performance["profit_factor"] = 0

    # ============================================================
    # AI METHODS - PUBLIC
    # ============================================================

    def validate_with_ai(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Validate existing signal with AI."""
        if not self.ai_enabled:
            return {
                **signal,
                'ai_validated': False,
                'ai_status': 'disabled'
            }
        
        result = self._enhance_with_ai(signal, {})
        return {**signal, **result}

    def get_ai_status(self) -> Dict[str, Any]:
        """Get AI integration status."""
        return {
            'ai_enabled': self.ai_enabled,
            'ai_available': DEEPSEEK_AVAILABLE,
            'ai_validated_signals': self.ai_validated,
            'total_signals': self.total_signals,
            'validation_ratio': round(self.ai_validated / max(1, self.total_signals) * 100, 2),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

    # ============================================================
    # UTILITY
    # ============================================================

    def _unique(self, items: List[str]) -> List[str]:
        """Remove duplicates while preserving order."""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                result.append(item)
                seen.add(item)
        return result

    def _empty_signal(self, error: str, pair: str = "UNKNOWN") -> Dict[str, Any]:
        """Return empty signal on error."""
        return {
            "engine_version": self.VERSION,
            "pair": pair,
            "symbol": pair,
            "signal": SIGNAL_HOLD,
            "trend": "UNKNOWN",
            "market_regime": MARKET_NEUTRAL,
            "volatility": "UNKNOWN",
            "sentiment": 50,
            "confidence": 0,
            "strength": 0,
            "buy_score": 0,
            "sell_score": 0,
            "entry": 0,
            "stop_loss": None,
            "take_profit_1": None,
            "take_profit_2": None,
            "take_profit_3": None,
            "risk_reward": 0,
            "risk_level": "UNKNOWN",
            "position_size": 0,
            "signal_quality": "ERROR",
            "recommendation": f"Signal unavailable: {error}",
            "reasons": [],
            "warnings": [error],
            "evidence": [],
            "ai_validated": False,
            "ai_status": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def clear_cache(self) -> None:
        """Clear signal cache."""
        self._signal_cache.clear()
        logger.info("Signal cache cleared")

    def set_weights(self, weights: Dict[str, float]) -> None:
        """Update weights configuration."""
        self.weights.update(weights)
        self.MAX_SCORE = sum(self.weights.values())
        logger.info("Weights updated: %s", weights)


# ============================================================
# GLOBAL INSTANCE
# ============================================================

signal_engine = SignalEngine()


# ============================================================
# COMPATIBILITY
# ============================================================

SignalEngineV4 = SignalEngine
SignalEngineV3 = SignalEngine


# ============================================================
# SHORTCUT FUNCTIONS
# ============================================================

def generate_signal(analysis: Dict[str, Any], use_ai: bool = True) -> Dict[str, Any]:
    return signal_engine.generate_signal(analysis, use_ai)


def get_history(limit: int = 50) -> List[Dict[str, Any]]:
    return signal_engine.get_history(limit)


def get_statistics() -> Dict[str, Any]:
    return signal_engine.get_statistics()


def validate_with_ai(signal: Dict[str, Any]) -> Dict[str, Any]:
    return signal_engine.validate_with_ai(signal)


def get_ai_status() -> Dict[str, Any]:
    return signal_engine.get_ai_status()


def clear_cache() -> None:
    signal_engine.clear_cache()


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "SignalEngine",
    "signal_engine",
    "generate_signal",
    "get_history",
    "get_statistics",
    "validate_with_ai",
    "get_ai_status",
    "clear_cache",
    "SIGNAL_BUY",
    "SIGNAL_STRONG_BUY",
    "SIGNAL_SELL",
    "SIGNAL_STRONG_SELL",
    "SIGNAL_HOLD",
    "SIGNAL_MONITOR",
    "SIGNAL_WAIT",
    "SIGNAL_EXIT",
    "SIGNAL_QUALITY_EXCELLENT",
    "SIGNAL_QUALITY_GOOD",
    "SIGNAL_QUALITY_FAIR",
    "SIGNAL_QUALITY_WEAK",
    "SIGNAL_QUALITY_NEUTRAL",
    "SIGNAL_QUALITY_AI_VALIDATED",
    "MARKET_TRENDING_BULLISH",
    "MARKET_TRENDING_BEARISH",
    "MARKET_RANGING",
    "MARKET_NEUTRAL",
    "MARKET_VOLATILE",
    "MARKET_BREAKOUT",
    "MARKET_BREAKDOWN",
    "RISK_LOW",
    "RISK_MEDIUM",
    "RISK_HIGH",
    "RISK_EXTREME",
]
