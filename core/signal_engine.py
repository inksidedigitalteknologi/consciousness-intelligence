# ============================================================
# INKSIDE DIGITAL TRADING BOT
# SIGNAL ENGINE v4.0
#
# SUPER COMPREHENSIVE SIGNAL ENGINE
#
# Fitur:
# 1. Multi-Timeframe Analysis (MTF)
# 2. Trend Detection (EMA, SMA, ADX)
# 3. Momentum Analysis (RSI, MACD, ROC)
# 4. Volume Intelligence
# 5. Pattern Recognition (Candlestick)
# 6. Breakout / Breakdown Detection
# 7. Bollinger Bands
# 8. MACD Divergence
# 9. Risk Management (ATR-based SL/TP)
# 10. Signal Quality Scoring
# 11. Confidence Calculation
# 12. Market Regime Detection
# 13. Divergence Detection
# 14. Support / Resistance
# 15. Volatility Analysis
# 16. Signal Strength
# 17. Multi-Factor Weighted Scoring
# 18. Dynamic Threshold Adjustment
# 19. Signal History
# 20. Performance Tracking
# ============================================================

from __future__ import annotations

import logging
import statistics
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# HEALTH IMPORT - FIXED
# ============================================================

try:
    from core.health import set_status
except ImportError:
    def set_status(*args, **kwargs):
        pass

logger = logging.getLogger(__name__)


# ============================================================
# CONSTANTS
# ============================================================

SIGNAL_BUY = "BUY"
SIGNAL_STRONG_BUY = "STRONG BUY"
SIGNAL_SELL = "SELL"
SIGNAL_STRONG_SELL = "STRONG SELL"
SIGNAL_HOLD = "HOLD"
SIGNAL_MONITOR = "MONITOR"
SIGNAL_WAIT = "WAIT"

SIGNAL_QUALITY_EXCELLENT = "EXCELLENT"
SIGNAL_QUALITY_GOOD = "GOOD"
SIGNAL_QUALITY_FAIR = "FAIR"
SIGNAL_QUALITY_WEAK = "WEAK"
SIGNAL_QUALITY_NEUTRAL = "NEUTRAL"

MARKET_TRENDING_BULLISH = "TRENDING_BULLISH"
MARKET_TRENDING_BEARISH = "TRENDING_BEARISH"
MARKET_RANGING = "RANGING"
MARKET_NEUTRAL = "NEUTRAL"
MARKET_VOLATILE = "VOLATILE"

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_EXTREME = "EXTREME"


# ============================================================
# SIGNAL ENGINE v4.0
# ============================================================

class SignalEngine:
    """
    Signal Engine v4.0 - Super Comprehensive Signal Generator.
    
    Menggunakan weighted multi-factor analysis untuk menghasilkan
    sinyal trading yang akurat dengan confidence scoring.
    """

    VERSION = "4.0.0"

    # ========================================================
    # WEIGHT CONFIGURATION
    # ========================================================

    WEIGHTS = {
        "mtf": 25,          # Multi-timeframe alignment
        "trend": 20,        # Overall trend
        "ema": 15,          # EMA structure
        "adx": 12,          # Trend strength
        "macd": 10,         # Momentum
        "volume": 10,       # Volume confirmation
        "breakout": 10,     # Breakout/breakdown
        "rsi": 8,           # RSI
        "bollinger": 5,     # Bollinger Bands
        "momentum": 5,      # Price momentum
        "candle": 5,        # Candlestick patterns
        "divergence": 5,    # MACD divergence
        "support_resistance": 5,  # S/R levels
        "volatility": 3,    # Volatility
        "seasonality": 2,   # Time-based patterns
    }

    MAX_SCORE = sum(WEIGHTS.values())  # ~140

    # ========================================================
    # SIGNAL THRESHOLDS
    # ========================================================

    THRESHOLDS = {
        "strong_buy": 80,
        "buy": 65,
        "weak_buy": 50,
        "weak_sell": 50,
        "sell": 65,
        "strong_sell": 80,
        "hold_max": 45,
    }

    # ========================================================
    # CONFIDENCE THRESHOLDS
    # ========================================================

    CONFIDENCE = {
        "high": 75,
        "medium": 55,
        "low": 35,
    }

    # ========================================================
    # RISK SETTINGS
    # ========================================================

    RISK = {
        "atr_sl": 1.5,
        "tp1_rr": 1.5,
        "tp2_rr": 2.5,
        "tp3_rr": 4.0,
        "max_risk_percent": 2.0,
        "min_risk_reward": 1.0,
    }

    # ========================================================
    # TIMEFRAME WEIGHTS
    # ========================================================

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

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Override defaults from config
        self.weights = self.config.get("weights", self.WEIGHTS.copy())
        self.thresholds = self.config.get("thresholds", self.THRESHOLDS.copy())
        self.confidence_thresholds = self.config.get("confidence", self.CONFIDENCE.copy())
        self.risk_settings = self.config.get("risk", self.RISK.copy())
        self.timeframe_weights = self.config.get("timeframe_weights", self.TIMEFRAME_WEIGHTS.copy())
        
        # Statistics
        self.total_signals = 0
        self.buy_signals = 0
        self.sell_signals = 0
        self.hold_signals = 0
        self.history: List[Dict[str, Any]] = []
        self.max_history = self.config.get("max_history", 1000)
        self.performance: Dict[str, Any] = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "accuracy": 0.0,
        }
        
        logger.info("Signal Engine v%s initialized.", self.VERSION)
        set_status("signal_engine", "INITIALIZED")

    # ========================================================
    # MAIN SIGNAL GENERATOR
    # ========================================================

    def generate_signal(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate trading signal from market analysis.
        
        Args:
            analysis: Market analysis data
            
        Returns:
            Complete signal with entry, SL, TP, and confidence
        """
        if not analysis:
            return self._empty_signal("No analysis data")

        try:
            pair = analysis.get("pair", analysis.get("symbol", "UNKNOWN"))
            
            # Normalize analysis data
            data = self._normalize_analysis(analysis)
            
            # Get market context
            market_regime = self._detect_market_regime(data)
            trend = self._detect_trend(data)
            volatility = self._detect_volatility(data)
            
            # Evaluate all factors
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
            
            # Normalize scores
            buy_score = self._normalize_score(buy_score)
            sell_score = self._normalize_score(sell_score)
            
            # Determine signal
            signal = self._determine_signal(buy_score, sell_score, market_regime)
            
            # Calculate confidence
            confidence = self._calculate_confidence(buy_score, sell_score, signal, market_regime)
            
            # Get entry price
            entry = self._get_entry_price(data)
            
            # Calculate risk levels
            risk = self._calculate_risk_levels(entry, data, signal)
            
            # Calculate signal quality
            quality = self._calculate_signal_quality(signal, confidence, risk["risk_reward"], warnings)
            
            # Generate recommendation
            recommendation = self._generate_recommendation(signal, confidence, market_regime, quality)
            
            # Record history
            self._record_history({
                "pair": pair,
                "signal": signal,
                "confidence": confidence,
                "quality": quality,
                "buy_score": buy_score,
                "sell_score": sell_score,
                "market_regime": market_regime,
                "trend": trend,
                "reasons": reasons[:5],
                "warnings": warnings[:3],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            
            # Build result
            result = {
                "engine_version": self.VERSION,
                "pair": pair,
                "symbol": pair,
                "signal": signal,
                "trend": trend,
                "market_regime": market_regime,
                "volatility": volatility,
                "confidence": confidence,
                "strength": max(buy_score, sell_score),
                "buy_score": buy_score,
                "sell_score": sell_score,
                "entry": risk["entry"],
                "stop_loss": risk["stop_loss"],
                "take_profit_1": risk["take_profit_1"],
                "take_profit_2": risk["take_profit_2"],
                "take_profit_3": risk["take_profit_3"],
                "tp1": risk["take_profit_1"],
                "tp2": risk["take_profit_2"],
                "tp3": risk["take_profit_3"],
                "risk_reward": risk["risk_reward"],
                "risk_level": risk["risk_level"],
                "signal_quality": quality,
                "recommendation": recommendation,
                "reasons": self._unique(reasons[:10]),
                "warnings": self._unique(warnings[:5]),
                "evidence": self._unique(evidence[:5]),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            
            # Update statistics
            self.total_signals += 1
            if signal in [SIGNAL_BUY, SIGNAL_STRONG_BUY]:
                self.buy_signals += 1
            elif signal in [SIGNAL_SELL, SIGNAL_STRONG_SELL]:
                self.sell_signals += 1
            else:
                self.hold_signals += 1
            
            logger.info(
                "%s | BUY %.2f | SELL %.2f | SIGNAL %s | QUALITY %s | CONF %.2f%%",
                pair, buy_score, sell_score, signal, quality, confidence
            )
            
            set_status("signal_engine", "ONLINE")
            
            return result

        except Exception as e:
            logger.exception("Signal Engine Error: %s", e)
            set_status("signal_engine", "ERROR")
            return self._empty_signal(str(e), analysis.get("pair", "UNKNOWN"))

    # ========================================================
    # NORMALIZATION
    # ========================================================

    def _normalize_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize analysis data with proper types."""
        data = dict(analysis)
        
        numeric_fields = [
            "price", "close", "last", "last_price", "current_price", "ticker_price",
            "rsi", "adx", "atr", "ATR", "average_true_range",
            "volume", "average_volume",
            "macd", "macd_signal", "macd_histogram",
            "ema9", "ema21", "ema50", "ema200",
            "sma20", "sma50", "sma200",
            "bb_upper", "bb_middle", "bb_lower",
            "support", "resistance", "pivot",
            "momentum", "roc",
            "high", "low", "open",
            "change_24h", "change_7d",
        ]
        
        for field in numeric_fields:
            if data.get(field) is not None:
                try:
                    data[field] = float(data[field])
                except (ValueError, TypeError):
                    data[field] = None
        
        # Ensure price exists
        if data.get("price") is None and data.get("close") is not None:
            data["price"] = data["close"]
        
        return data

    # ========================================================
    # MARKET REGIME
    # ========================================================

    def _detect_market_regime(self, data: Dict[str, Any]) -> str:
        """Detect current market regime."""
        adx = data.get("adx")
        trend = self._detect_trend(data)
        
        if adx is not None:
            if adx >= 25:
                if trend == "BULLISH":
                    return MARKET_TRENDING_BULLISH
                if trend == "BEARISH":
                    return MARKET_TRENDING_BEARISH
            elif adx < 20:
                return MARKET_RANGING
        
        # Check volatility
        volatility = data.get("volatility")
        if volatility and volatility > 3.0:
            return MARKET_VOLATILE
        
        return MARKET_NEUTRAL

    # ========================================================
    # TREND DETECTION
    # ========================================================

    def _detect_trend(self, data: Dict[str, Any]) -> str:
        """Detect market trend from multiple sources."""
        # Custom trend from analysis
        custom = data.get("trend")
        if custom:
            return str(custom).upper()
        
        price = self._get_entry_price(data)
        ema50 = data.get("ema50")
        ema200 = data.get("ema200")
        sma20 = data.get("sma20")
        
        bullish_score = 0
        bearish_score = 0
        
        # EMA structure
        if price and ema50 and ema200:
            if price > ema50 > ema200:
                bullish_score += 3
            elif price < ema50 < ema200:
                bearish_score += 3
        
        # Price vs SMA
        if price and sma20:
            if price > sma20:
                bullish_score += 1
            else:
                bearish_score += 1
        
        # ADX alignment
        adx = data.get("adx")
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

    # ========================================================
    # VOLATILITY DETECTION
    # ========================================================

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

    # ========================================================
    # EVALUATORS
    # ========================================================

    def _evaluate_mtf(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Multi-timeframe alignment."""
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
            elif direction == "BEARISH":
                bearish += weight
        
        if total > 0:
            buy = (bullish / total) * self.weights["mtf"]
            sell = (bearish / total) * self.weights["mtf"]
            
            if buy >= 8:
                result["buy"] = round(buy, 2)
                result["reasons"].append("Weighted MTF bullish alignment")
            if sell >= 8:
                result["sell"] = round(sell, 2)
                result["reasons"].append("Weighted MTF bearish alignment")
        
        return result

    def _evaluate_trend(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trend evaluation."""
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
        """EMA structure evaluation."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        ema9 = data.get("ema9")
        ema21 = data.get("ema21")
        ema50 = data.get("ema50")
        ema200 = data.get("ema200")
        
        buy = 0
        sell = 0
        
        if ema9 and ema21:
            if ema9 > ema21:
                buy += 7
                result["reasons"].append("EMA9 above EMA21 (bullish)")
            else:
                sell += 7
                result["reasons"].append("EMA9 below EMA21 (bearish)")
        
        if ema50 and ema200:
            if ema50 > ema200:
                buy += 8
                result["reasons"].append("EMA50 above EMA200 (bullish structure)")
            else:
                sell += 8
                result["reasons"].append("EMA50 below EMA200 (bearish structure)")
        
        result["buy"] = min(buy, self.weights["ema"])
        result["sell"] = min(sell, self.weights["ema"])
        
        return result

    def _evaluate_adx(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """ADX trend strength."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        adx = data.get("adx")
        if adx is None:
            return result
        
        trend = self._detect_trend(data)
        
        if adx >= 25:
            if trend == "BULLISH":
                result["buy"] = self.weights["adx"]
                result["reasons"].append("ADX confirms strong bullish trend")
            elif trend == "BEARISH":
                result["sell"] = self.weights["adx"]
                result["reasons"].append("ADX confirms strong bearish trend")
        elif adx >= 20:
            result["reasons"].append("ADX: moderate trend strength")
        else:
            result["reasons"].append("ADX: weak trend (possible ranging)")
        
        return result

    def _evaluate_macd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """MACD momentum."""
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
                result["reasons"].append("MACD histogram positive")
            else:
                result["sell"] += 3
                result["reasons"].append("MACD histogram negative")
        
        result["buy"] = min(result["buy"], self.weights["macd"])
        result["sell"] = min(result["sell"], self.weights["macd"])
        
        return result

    def _evaluate_volume(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Volume analysis."""
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
                result["reasons"].append("High volume confirms bullish movement")
            elif trend == "BEARISH":
                result["sell"] = self.weights["volume"]
                result["reasons"].append("High volume confirms bearish movement")
            else:
                result["reasons"].append("High volume with neutral trend")
        elif ratio < 0.7:
            result["warnings"].append("Volume below average (weak confirmation)")
        else:
            result["reasons"].append("Volume at normal levels")
        
        return result

    def _evaluate_breakout(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Breakout/breakdown detection."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        price = self._get_entry_price(data)
        resistance = data.get("resistance")
        support = data.get("support")
        
        if not price:
            return result
        
        if resistance and price > resistance:
            result["buy"] = self.weights["breakout"]
            result["reasons"].append("Bullish breakout detected")
        elif support and price < support:
            result["sell"] = self.weights["breakout"]
            result["reasons"].append("Bearish breakdown detected")
        
        return result

    def _evaluate_rsi(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """RSI analysis."""
        result = {"buy": 0, "sell": 0, "reasons": [], "warnings": []}
        
        rsi = data.get("rsi")
        if rsi is None:
            return result
        
        if rsi < 30:
            result["buy"] = self.weights["rsi"]
            result["reasons"].append("RSI oversold (recovery potential)")
        elif 50 <= rsi <= 70:
            result["buy"] = self.weights["rsi"] * 0.7
            result["reasons"].append("RSI in bullish momentum zone")
        elif 70 < rsi <= 80:
            result["sell"] = self.weights["rsi"] * 0.7
            result["reasons"].append("RSI approaching overbought")
        elif rsi > 80:
            result["sell"] = self.weights["rsi"]
            result["warnings"].append("RSI severely overbought")
        elif 30 <= rsi < 50:
            result["sell"] = self.weights["rsi"] * 0.5
            result["reasons"].append("RSI in bearish momentum zone")
        
        return result

    def _evaluate_bollinger(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Bollinger Bands analysis."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        price = self._get_entry_price(data)
        upper = data.get("bb_upper")
        lower = data.get("bb_lower")
        middle = data.get("bb_middle")
        
        if not price:
            return result
        
        if lower and price <= lower:
            result["buy"] = self.weights["bollinger"]
            result["reasons"].append("Price near lower Bollinger Band")
        elif upper and price >= upper:
            result["sell"] = self.weights["bollinger"]
            result["reasons"].append("Price near upper Bollinger Band")
        elif middle and price > middle:
            result["buy"] = self.weights["bollinger"] * 0.5
            result["reasons"].append("Price above middle Bollinger Band")
        elif middle and price < middle:
            result["sell"] = self.weights["bollinger"] * 0.5
            result["reasons"].append("Price below middle Bollinger Band")
        
        return result

    def _evaluate_momentum(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Price momentum analysis."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        momentum = data.get("momentum")
        roc = data.get("roc")
        
        if momentum is not None:
            if momentum > 0:
                result["buy"] = self.weights["momentum"]
                result["reasons"].append("Positive price momentum")
            elif momentum < 0:
                result["sell"] = self.weights["momentum"]
                result["reasons"].append("Negative price momentum")
        
        if roc is not None:
            if roc > 0:
                result["buy"] += 2
                if momentum is not None:
                    result["reasons"].append("ROC positive (strength)")
            else:
                result["sell"] += 2
                if momentum is not None:
                    result["reasons"].append("ROC negative (weakness)")
        
        result["buy"] = min(result["buy"], self.weights["momentum"])
        result["sell"] = min(result["sell"], self.weights["momentum"])
        
        return result

    def _evaluate_candle_pattern(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Candlestick pattern detection."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        patterns = data.get("patterns")
        if isinstance(patterns, str):
            patterns = [patterns]
        elif not isinstance(patterns, list):
            return result
        
        bullish_patterns = [
            "HAMMER", "BULLISH_ENGULFING", "MORNING_STAR",
            "THREE_WHITE_SOLDIERS", "BULLISH_HARAMI", "PIERCING_LINE"
        ]
        
        bearish_patterns = [
            "SHOOTING_STAR", "BEARISH_ENGULFING", "EVENING_STAR",
            "THREE_BLACK_CROWS", "BEARISH_HARAMI", "DARK_CLOUD_COVER"
        ]
        
        for pattern in patterns:
            p = str(pattern).upper()
            if p in bullish_patterns:
                result["buy"] += 1
                result["reasons"].append(f"Bullish candle pattern: {p}")
            elif p in bearish_patterns:
                result["sell"] += 1
                result["reasons"].append(f"Bearish candle pattern: {p}")
        
        result["buy"] = min(result["buy"], self.weights["candle"])
        result["sell"] = min(result["sell"], self.weights["candle"])
        
        return result

    def _evaluate_divergence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """MACD divergence detection."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        price_history = data.get("price_history")
        macd_history = data.get("macd_history")
        
        if not isinstance(price_history, list) or len(price_history) < 3:
            return result
        if not isinstance(macd_history, list) or len(macd_history) < 3:
            return result
        
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
        
        return result

    def _evaluate_support_resistance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Support/Resistance levels."""
        result = {"buy": 0, "sell": 0, "reasons": []}
        
        price = self._get_entry_price(data)
        support = data.get("support")
        resistance = data.get("resistance")
        
        if not price:
            return result
        
        if support and resistance:
            range_width = resistance - support
            position = (price - support) / range_width if range_width > 0 else 0.5
            
            if position < 0.2:
                result["buy"] = self.weights["support_resistance"]
                result["reasons"].append("Price near support level")
            elif position > 0.8:
                result["sell"] = self.weights["support_resistance"]
                result["reasons"].append("Price near resistance level")
            elif 0.4 <= position <= 0.6:
                result["reasons"].append("Price in middle of range")
        
        return result

    def _evaluate_volatility_factor(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Volatility factor."""
        result = {"buy": 0, "sell": 0, "reasons": [], "warnings": []}
        
        atr = data.get("atr")
        price = self._get_entry_price(data)
        
        if atr and price and price > 0:
            atr_percent = (atr / price) * 100
            
            if atr_percent > 5:
                result["warnings"].append("Very high volatility (risk)")
                result["sell"] = self.weights["volatility"] * 0.5
            elif atr_percent > 3:
                result["warnings"].append("High volatility")
                result["buy"] = self.weights["volatility"] * 0.3
            elif atr_percent > 1:
                result["buy"] = self.weights["volatility"] * 0.5
                result["reasons"].append("Normal volatility environment")
            else:
                result["buy"] = self.weights["volatility"]
                result["reasons"].append("Low volatility (stable environment)")
        
        return result

    # ========================================================
    # SCORE NORMALIZATION
    # ========================================================

    def _normalize_score(self, score: float) -> float:
        """Normalize score to percentage (0-100)."""
        if score <= 0:
            return 0
        return round(min((score / self.MAX_SCORE) * 100, 100), 2)

    # ========================================================
    # SIGNAL DETERMINATION
    # ========================================================

    def _determine_signal(self, buy_score: float, sell_score: float, market_regime: str) -> str:
        """Determine final signal from scores."""
        
        # In ranging market, require higher confidence
        if market_regime == MARKET_RANGING:
            if max(buy_score, sell_score) < 70:
                return SIGNAL_HOLD
        
        # Check buy signals
        if buy_score >= self.thresholds["strong_buy"] and buy_score > sell_score:
            return SIGNAL_STRONG_BUY
        if buy_score >= self.thresholds["buy"] and buy_score > sell_score:
            return SIGNAL_BUY
        if buy_score >= self.thresholds["weak_buy"] and buy_score > sell_score * 1.2:
            return SIGNAL_MONITOR
        
        # Check sell signals
        if sell_score >= self.thresholds["strong_sell"] and sell_score > buy_score:
            return SIGNAL_STRONG_SELL
        if sell_score >= self.thresholds["sell"] and sell_score > buy_score:
            return SIGNAL_SELL
        if sell_score >= self.thresholds["weak_sell"] and sell_score > buy_score * 1.2:
            return SIGNAL_MONITOR
        
        return SIGNAL_HOLD

    # ========================================================
    # CONFIDENCE CALCULATION
    # ========================================================

    def _calculate_confidence(self, buy_score: float, sell_score: float, signal: str, market_regime: str) -> float:
        """Calculate confidence level."""
        if signal in [SIGNAL_HOLD, SIGNAL_WAIT]:
            return 0
        
        strength = max(buy_score, sell_score)
        difference = abs(buy_score - sell_score)
        
        # Base confidence from strength
        confidence = strength * 0.6 + difference * 0.3
        
        # Market regime adjustment
        if market_regime in [MARKET_TRENDING_BULLISH, MARKET_TRENDING_BEARISH]:
            confidence += 5
        elif market_regime == MARKET_RANGING:
            confidence -= 5
        
        # Signal quality adjustment
        if signal in [SIGNAL_STRONG_BUY, SIGNAL_STRONG_SELL]:
            confidence += 10
        
        return round(min(confidence, 100), 2)

    # ========================================================
    # ENTRY PRICE
    # ========================================================

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

    # ========================================================
    # RISK MANAGEMENT
    # ========================================================

    def _calculate_risk_levels(self, entry: float, data: Dict[str, Any], signal: str) -> Dict[str, Any]:
        """Calculate risk levels with ATR-based SL/TP."""
        result = {
            "entry": round(entry, 8),
            "stop_loss": None,
            "take_profit_1": None,
            "take_profit_2": None,
            "take_profit_3": None,
            "risk_reward": 0,
            "risk_level": "UNKNOWN",
        }
        
        if entry <= 0:
            return result
        
        # Get ATR
        atr = data.get("atr") or data.get("ATR") or data.get("average_true_range")
        try:
            atr = float(atr) if atr is not None else 0
        except (ValueError, TypeError):
            atr = 0
        
        # Fallback ATR
        if atr <= 0:
            atr = entry * 0.015
        
        if signal in [SIGNAL_BUY, SIGNAL_STRONG_BUY]:
            stop_loss = entry - (atr * self.risk_settings["atr_sl"])
            risk = entry - stop_loss
            tp1 = entry + (risk * self.risk_settings["tp1_rr"])
            tp2 = entry + (risk * self.risk_settings["tp2_rr"])
            tp3 = entry + (risk * self.risk_settings["tp3_rr"])
            
        elif signal in [SIGNAL_SELL, SIGNAL_STRONG_SELL]:
            stop_loss = entry + (atr * self.risk_settings["atr_sl"])
            risk = stop_loss - entry
            tp1 = entry - (risk * self.risk_settings["tp1_rr"])
            tp2 = entry - (risk * self.risk_settings["tp2_rr"])
            tp3 = entry - (risk * self.risk_settings["tp3_rr"])
            
        else:
            return result
        
        rr = self.risk_settings["tp2_rr"]  # Use TP2 for main RR
        
        result.update({
            "stop_loss": round(stop_loss, 8),
            "take_profit_1": round(tp1, 8),
            "take_profit_2": round(tp2, 8),
            "take_profit_3": round(tp3, 8),
            "risk_reward": rr,
        })
        
        # Risk level
        atr_percent = (atr / entry) * 100
        if atr_percent < 1:
            result["risk_level"] = RISK_LOW
        elif atr_percent < 2:
            result["risk_level"] = RISK_MEDIUM
        elif atr_percent < 4:
            result["risk_level"] = RISK_HIGH
        else:
            result["risk_level"] = RISK_EXTREME
        
        return result

    # ========================================================
    # SIGNAL QUALITY
    # ========================================================

    def _calculate_signal_quality(self, signal: str, confidence: float, risk_reward: float, warnings: List[str]) -> str:
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
        
        if score >= 85:
            return SIGNAL_QUALITY_EXCELLENT
        elif score >= 65:
            return SIGNAL_QUALITY_GOOD
        elif score >= 40:
            return SIGNAL_QUALITY_FAIR
        return SIGNAL_QUALITY_WEAK

    # ========================================================
    # RECOMMENDATION
    # ========================================================

    def _generate_recommendation(self, signal: str, confidence: float, market_regime: str, quality: str) -> str:
        """Generate human-readable recommendation."""
        if signal in [SIGNAL_HOLD, SIGNAL_WAIT]:
            return "Wait for confirmation"
        
        recommendations = {
            SIGNAL_STRONG_BUY: "Strong Buy - Consider entering position",
            SIGNAL_BUY: "Buy - Good opportunity with confirmation",
            SIGNAL_SELL: "Sell - Good opportunity to exit",
            SIGNAL_STRONG_SELL: "Strong Sell - Consider exiting position",
            SIGNAL_MONITOR: "Monitor - Prepare for entry",
        }
        
        base = recommendations.get(signal, "Hold position")
        
        # Add confidence note
        if confidence >= 75:
            base += " (high confidence)"
        elif confidence >= 55:
            base += " (moderate confidence)"
        else:
            base += " (low confidence - proceed with caution)"
        
        # Add market regime note
        if market_regime == MARKET_RANGING:
            base += " - Ranging market"
        elif market_regime == MARKET_VOLATILE:
            base += " - High volatility expected"
        
        return base

    # ========================================================
    # HISTORY & STATISTICS
    # ========================================================

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
            }
        
        return {
            "total": total,
            "buy": self.buy_signals,
            "sell": self.sell_signals,
            "hold": self.hold_signals,
            "buy_ratio": round((self.buy_signals / total) * 100, 2),
            "sell_ratio": round((self.sell_signals / total) * 100, 2),
            "accuracy": round(self.performance["accuracy"], 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def record_outcome(self, signal_id: str, success: bool) -> None:
        """Record signal outcome for accuracy tracking."""
        self.performance["total"] += 1
        if success:
            self.performance["successful"] += 1
        else:
            self.performance["failed"] += 1
        self.performance["accuracy"] = (
            self.performance["successful"] / self.performance["total"] * 100
            if self.performance["total"] > 0 else 0
        )

    # ========================================================
    # UTILITY
    # ========================================================

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
            "confidence": 0,
            "strength": 0,
            "buy_score": 0,
            "sell_score": 0,
            "entry": 0,
            "stop_loss": None,
            "take_profit_1": None,
            "take_profit_2": None,
            "take_profit_3": None,
            "tp1": None,
            "tp2": None,
            "tp3": None,
            "risk_reward": 0,
            "risk_level": "UNKNOWN",
            "signal_quality": "ERROR",
            "recommendation": f"Signal unavailable: {error}",
            "reasons": [],
            "warnings": [error],
            "evidence": [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================
# GLOBAL INSTANCE
# ============================================================

signal_engine = SignalEngine()


# ============================================================
# COMPATIBILITY
# ============================================================

SignalEngineV3 = SignalEngine


# ============================================================
# END
# ============================================================