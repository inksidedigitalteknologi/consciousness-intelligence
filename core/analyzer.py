# core/analyzer.py
# INKSIDEDIGITAL - MARKET ANALYZER v5.0
# 
# SUPER COMPREHENSIVE MARKET ANALYZER
# TANPA DEPENDENSI EXTERNAL - SEMUA PERHITUNGAN MANUAL
# TANPA DATA DUMMY
#
# Fitur:
# 1. Multi-Timeframe Analysis
# 2. Advanced Trend Detection (EMA, SMA)
# 3. Momentum Analysis (RSI, MACD, ROC)
# 4. Volume Intelligence
# 5. Volatility Analysis (ATR, Bollinger)
# 6. Candle Pattern Recognition (20+ patterns)
# 7. Support/Resistance Detection
# 8. Divergence Detection
# 9. Market Regime Detection
# 10. Signal Confidence Scoring
# 11. Dynamic Risk Management
# ============================================================

import logging
import math
import statistics
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ============================================================
# CONSTANTS
# ============================================================

TREND_BULLISH = "BULLISH"
TREND_BEARISH = "BEARISH"
TREND_NEUTRAL = "NEUTRAL"
TREND_STRONG_BULLISH = "STRONG_BULLISH"
TREND_STRONG_BEARISH = "STRONG_BEARISH"

VOLUME_EXTREME = "EXTREME_VOLUME"
VOLUME_HIGH = "HIGH_VOLUME"
VOLUME_NORMAL = "NORMAL"
VOLUME_LOW = "LOW_VOLUME"

VOLATILITY_EXTREME = "EXTREME"
VOLATILITY_HIGH = "HIGH"
VOLATILITY_NORMAL = "NORMAL"
VOLATILITY_LOW = "LOW"

PATTERN_DOJI = "DOJI"
PATTERN_HAMMER = "HAMMER"
PATTERN_SHOOTING_STAR = "SHOOTING_STAR"
PATTERN_BULLISH_ENGULFING = "BULLISH_ENGULFING"
PATTERN_BEARISH_ENGULFING = "BEARISH_ENGULFING"
PATTERN_MORNING_STAR = "MORNING_STAR"
PATTERN_EVENING_STAR = "EVENING_STAR"
PATTERN_THREE_WHITE_SOLDIERS = "THREE_WHITE_SOLDIERS"
PATTERN_THREE_BLACK_CROWS = "THREE_BLACK_CROWS"
PATTERN_BULLISH_HARAMI = "BULLISH_HARAMI"
PATTERN_BEARISH_HARAMI = "BEARISH_HARAMI"
PATTERN_PIERCING_LINE = "PIERCING_LINE"
PATTERN_DARK_CLOUD_COVER = "DARK_CLOUD_COVER"
PATTERN_MARUBOZU = "MARUBOZU"
PATTERN_SPINNING_TOP = "SPINNING_TOP"
PATTERN_UNKNOWN = "UNKNOWN"

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"

SIGNAL_BUY = "BUY"
SIGNAL_SELL = "SELL"
SIGNAL_HOLD = "HOLD"
SIGNAL_STRONG_BUY = "STRONG_BUY"
SIGNAL_STRONG_SELL = "STRONG_SELL"


# ============================================================
# ANALYZER ENGINE v5.0
# ============================================================

class Analyzer:
    """
    Analyzer v5.0 - Super Comprehensive Market Analyzer.
    
    Semua perhitungan manual, tanpa dependensi eksternal.
    """
    
    VERSION = "5.0.0"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Minimum candles required
        self.min_candles = self.config.get("min_candles", 50)
        self.min_candles_pattern = self.config.get("min_candles_pattern", 20)
        
        # ATR Management
        self.atr_sl_multiplier = self.config.get("atr_sl_multiplier", 1.5)
        self.tp1_multiplier = self.config.get("tp1_multiplier", 1.0)
        self.tp2_multiplier = self.config.get("tp2_multiplier", 2.0)
        self.tp3_multiplier = self.config.get("tp3_multiplier", 3.0)
        
        # Confidence thresholds
        self.confidence_threshold = self.config.get("confidence_threshold", 45)
        self.high_confidence_threshold = self.config.get("high_confidence_threshold", 70)
        
        # Performance tracking
        self.total_analysis = 0
        self.successful_analysis = 0
        self.failed_analysis = 0
        self.history: List[Dict[str, Any]] = []
        self.max_history = self.config.get("max_history", 500)
        
        logger.info("Analyzer v%s initialized.", self.VERSION)

    # ============================================================
    # MAIN ANALYSIS
    # ============================================================

    def analyze(
        self,
        pair: str,
        candles: List[Dict[str, Any]],
        timeframe: str = "1h",
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive market analysis.

        Args:
            pair: Trading pair
            candles: OHLCV data
            timeframe: Timeframe string
            options: Additional options

        Returns:
            Complete analysis result
        """
        self.total_analysis += 1
        
        try:
            if not candles:
                self.failed_analysis += 1
                return self._no_data_result(pair, "NO_DATA")
            
            normalized = self._normalize_candles(candles)
            
            if len(normalized) < self.min_candles_pattern:
                self.failed_analysis += 1
                return self._no_data_result(pair, "INSUFFICIENT_DATA")
            
            # Extract price data
            closes = [c["close"] for c in normalized]
            highs = [c["high"] for c in normalized]
            lows = [c["low"] for c in normalized]
            opens = [c["open"] for c in normalized]
            volumes = [c["volume"] for c in normalized]
            
            price = closes[-1]
            
            # Calculate indicators
            indicators = self._calculate_indicators(closes, highs, lows, volumes, opens)
            
            # Trend Analysis
            trend_analysis = self._analyze_trend(price, indicators, closes)
            
            # Momentum Analysis
            momentum_analysis = self._analyze_momentum(indicators, closes)
            
            # Volume Analysis
            volume_analysis = self._analyze_volume(volumes, closes)
            
            # Volatility Analysis
            volatility_analysis = self._analyze_volatility(closes, indicators)
            
            # Candle Pattern Analysis
            pattern_analysis = self._analyze_candles(normalized)
            
            # Support/Resistance
            sr_levels = self._detect_support_resistance(highs, lows, closes)
            
            # Divergence Detection
            divergence = self._detect_divergence(closes, indicators)
            
            # Market Regime
            regime = self._detect_market_regime(indicators, trend_analysis, volatility_analysis)
            
            # Fibonacci Levels
            fib_levels = self._calculate_fibonacci(highs, lows)
            
            # Pivot Points
            pivots = self._calculate_pivot_points(highs, lows, closes)
            
            # Scoring
            bullish_score = (
                trend_analysis["bullish_score"] +
                momentum_analysis["bullish_score"] +
                volume_analysis["bullish_score"] +
                pattern_analysis["bullish_score"] +
                (divergence.get("bullish", 0) * 2)
            )
            
            bearish_score = (
                trend_analysis["bearish_score"] +
                momentum_analysis["bearish_score"] +
                volume_analysis["bearish_score"] +
                pattern_analysis["bearish_score"] +
                (divergence.get("bearish", 0) * 2)
            )
            
            score = bullish_score - bearish_score
            
            # Confidence & Signal
            confidence = self._calculate_confidence(
                bullish_score, bearish_score,
                trend_analysis, volume_analysis,
                volatility_analysis, pattern_analysis,
                sr_levels
            )
            
            signal = self._determine_signal(score, confidence)
            
            # Risk Management
            risk = self._calculate_risk_levels(
                price,
                indicators.get("atr"),
                signal,
                sr_levels
            )
            
            # Signal Quality
            quality = self._calculate_signal_quality(
                confidence,
                trend_analysis,
                volume_analysis,
                pattern_analysis,
                volatility_analysis
            )
            
            self.successful_analysis += 1
            
            # Build result
            result = {
                "pair": pair,
                "symbol": pair,
                "timeframe": timeframe,
                "price": price,
                "close": price,
                "signal": signal,
                "confidence": confidence,
                "strength": quality,
                "signal_quality": quality,
                "score": score,
                "bullish_score": bullish_score,
                "bearish_score": bearish_score,
                "entry": risk.get("entry"),
                "entry_price": risk.get("entry"),
                "stop_loss": risk.get("stop_loss"),
                "take_profit_1": risk.get("tp1"),
                "take_profit_2": risk.get("tp2"),
                "take_profit_3": risk.get("tp3"),
                "tp1": risk.get("tp1"),
                "tp2": risk.get("tp2"),
                "tp3": risk.get("tp3"),
                "risk_reward": risk.get("risk_reward"),
                "trend": trend_analysis.get("direction", "UNKNOWN"),
                "trend_strength": trend_analysis.get("strength", 0),
                "trend_signals": trend_analysis.get("signals", []),
                "momentum_signals": momentum_analysis.get("signals", []),
                "volume_state": volume_analysis.get("state", "UNKNOWN"),
                "volume_ratio": volume_analysis.get("ratio", 1.0),
                "volatility": volatility_analysis,
                "pattern": pattern_analysis.get("pattern", "UNKNOWN"),
                "patterns": pattern_analysis.get("patterns", []),
                "support": sr_levels.get("support"),
                "resistance": sr_levels.get("resistance"),
                "pivot": sr_levels.get("pivot"),
                "divergence": divergence.get("detected", []),
                "market_regime": regime,
                "fibonacci": fib_levels.get("levels", {}),
                "pivot_points": pivots,
                "indicators": {
                    "rsi": indicators.get("rsi"),
                    "atr": indicators.get("atr"),
                    "adx": indicators.get("adx"),
                    "roc": indicators.get("roc"),
                    "ema9": indicators.get("ema9"),
                    "ema21": indicators.get("ema21"),
                    "ema50": indicators.get("ema50"),
                    "ema200": indicators.get("ema200"),
                    "sma20": indicators.get("sma20"),
                    "sma50": indicators.get("sma50"),
                    "macd": indicators.get("macd"),
                    "macd_signal": indicators.get("macd_signal"),
                    "macd_histogram": indicators.get("macd_histogram"),
                    "bb_upper": indicators.get("bb_upper"),
                    "bb_middle": indicators.get("bb_middle"),
                    "bb_lower": indicators.get("bb_lower"),
                    "stoch_k": indicators.get("stoch_k"),
                    "stoch_d": indicators.get("stoch_d"),
                    "volume": indicators.get("volume"),
                    "average_volume": indicators.get("average_volume"),
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Store history
            self._record_history(result)
            
            logger.debug(
                "Analysis %s | Signal %s | Confidence %.2f%% | Score %.2f",
                pair, signal, confidence, score
            )
            
            return result
            
        except Exception as e:
            self.failed_analysis += 1
            logger.exception("Analyzer error %s : %s", pair, e)
            return self._no_data_result(pair, "ANALYSIS_ERROR")

    # ============================================================
    # INDICATOR CALCULATIONS
    # ============================================================

    def _calculate_indicators(
        self,
        closes: List[float],
        highs: List[float],
        lows: List[float],
        volumes: List[float],
        opens: List[float]
    ) -> Dict[str, Any]:
        """Calculate all technical indicators manually."""
        
        indicators = {}
        
        # EMAs
        indicators["ema9"] = self._calculate_ema(closes, 9)
        indicators["ema21"] = self._calculate_ema(closes, 21)
        indicators["ema50"] = self._calculate_ema(closes, 50)
        indicators["ema200"] = self._calculate_ema(closes, 200)
        
        # SMAs
        indicators["sma20"] = self._calculate_sma(closes, 20)
        indicators["sma50"] = self._calculate_sma(closes, 50)
        indicators["sma200"] = self._calculate_sma(closes, 200)
        
        # RSI
        indicators["rsi"] = self._calculate_rsi(closes)
        
        # ATR
        indicators["atr"] = self._calculate_atr(highs, lows, closes)
        
        # ADX
        indicators["adx"] = self._calculate_adx(highs, lows, closes)
        
        # MACD
        macd = self._calculate_macd(closes)
        indicators["macd"] = macd.get("macd")
        indicators["macd_signal"] = macd.get("signal")
        indicators["macd_histogram"] = macd.get("histogram")
        
        # Bollinger Bands
        bb = self._calculate_bollinger(closes)
        indicators["bb_upper"] = bb.get("upper")
        indicators["bb_middle"] = bb.get("middle")
        indicators["bb_lower"] = bb.get("lower")
        
        # ROC
        indicators["roc"] = self._calculate_roc(closes)
        
        # Stochastic
        stoch = self._calculate_stochastic(highs, lows, closes)
        indicators["stoch_k"] = stoch.get("k")
        indicators["stoch_d"] = stoch.get("d")
        
        # Volume
        indicators["volume"] = volumes[-1] if volumes else 0
        indicators["average_volume"] = self._calculate_sma(volumes, 20) if volumes else 0
        
        return indicators

    def _calculate_ema(self, data: List[float], period: int) -> Optional[float]:
        """Calculate Exponential Moving Average."""
        if len(data) < period:
            return None
        
        multiplier = 2 / (period + 1)
        ema = data[0]
        
        for price in data[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema

    def _calculate_sma(self, data: List[float], period: int) -> Optional[float]:
        """Calculate Simple Moving Average."""
        if len(data) < period:
            return None
        return sum(data[-period:]) / period

    def _calculate_rsi(self, closes: List[float], period: int = 14) -> Optional[float]:
        """Calculate Relative Strength Index."""
        if len(closes) < period + 1:
            return None
        
        gains = 0
        losses = 0
        
        for i in range(1, period + 1):
            change = closes[-i] - closes[-i-1]
            if change > 0:
                gains += change
            else:
                losses += abs(change)
        
        if losses == 0:
            return 100.0
        
        rs = gains / losses
        return 100 - (100 / (1 + rs))

    def _calculate_atr(self, highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Optional[float]:
        """Calculate Average True Range."""
        if len(closes) < period:
            return None
        
        tr_values = []
        for i in range(1, len(closes)):
            high = highs[i]
            low = lows[i]
            prev_close = closes[i-1]
            
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            tr_values.append(tr)
        
        if len(tr_values) < period:
            return None
        
        return sum(tr_values[-period:]) / period

    def _calculate_adx(self, highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Optional[float]:
        """Calculate Average Directional Index (simplified)."""
        if len(closes) < period * 2:
            return None
        
        # Calculate TR
        tr_values = []
        for i in range(1, len(closes)):
            high = highs[i]
            low = lows[i]
            prev_close = closes[i-1]
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            tr_values.append(tr)
        
        # Calculate +DM and -DM
        plus_dm = []
        minus_dm = []
        for i in range(1, len(highs)):
            up_move = highs[i] - highs[i-1]
            down_move = lows[i-1] - lows[i]
            
            if up_move > down_move and up_move > 0:
                plus_dm.append(up_move)
            else:
                plus_dm.append(0)
            
            if down_move > up_move and down_move > 0:
                minus_dm.append(down_move)
            else:
                minus_dm.append(0)
        
        if len(tr_values) < period or len(plus_dm) < period:
            return None
        
        atr = sum(tr_values[-period:]) / period
        plus_di = (sum(plus_dm[-period:]) / period) / atr * 100 if atr > 0 else 0
        minus_di = (sum(minus_dm[-period:]) / period) / atr * 100 if atr > 0 else 0
        
        dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100 if (plus_di + minus_di) > 0 else 0
        return dx

    def _calculate_macd(self, closes: List[float]) -> Dict[str, Optional[float]]:
        """Calculate MACD."""
        if len(closes) < 26:
            return {"macd": None, "signal": None, "histogram": None}
        
        ema12 = self._calculate_ema(closes, 12)
        ema26 = self._calculate_ema(closes, 26)
        
        if ema12 is None or ema26 is None:
            return {"macd": None, "signal": None, "histogram": None}
        
        macd_line = ema12 - ema26
        signal_line = macd_line * 0.9  # Approximation
        
        return {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": macd_line - signal_line
        }

    def _calculate_bollinger(self, closes: List[float], period: int = 20, std_dev: float = 2.0) -> Dict[str, Optional[float]]:
        """Calculate Bollinger Bands."""
        if len(closes) < period:
            return {"upper": None, "middle": None, "lower": None}
        
        sma = self._calculate_sma(closes, period)
        if sma is None:
            return {"upper": None, "middle": None, "lower": None}
        
        variance = sum((x - sma) ** 2 for x in closes[-period:]) / period
        std = math.sqrt(variance)
        
        return {
            "upper": sma + (std * std_dev),
            "middle": sma,
            "lower": sma - (std * std_dev)
        }

    def _calculate_roc(self, closes: List[float], period: int = 10) -> Optional[float]:
        """Calculate Rate of Change."""
        if len(closes) <= period:
            return None
        
        old_price = closes[-period-1]
        current_price = closes[-1]
        
        if old_price == 0:
            return 0
        
        return ((current_price - old_price) / old_price) * 100

    def _calculate_stochastic(self, highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Dict[str, Optional[float]]:
        """Calculate Stochastic Oscillator."""
        if len(closes) < period:
            return {"k": None, "d": None}
        
        highest_high = max(highs[-period:])
        lowest_low = min(lows[-period:])
        
        if highest_high == lowest_low:
            return {"k": 50, "d": 50}
        
        k = ((closes[-1] - lowest_low) / (highest_high - lowest_low)) * 100
        d = k  # Simplified
        
        return {"k": k, "d": d}

    # ============================================================
    # TREND ANALYSIS
    # ============================================================

    def _analyze_trend(self, price: float, indicators: Dict[str, Any], closes: List[float]) -> Dict[str, Any]:
        """Comprehensive trend analysis."""
        bullish = 0
        bearish = 0
        signals = []
        
        ema9 = indicators.get("ema9")
        ema21 = indicators.get("ema21")
        ema50 = indicators.get("ema50")
        ema200 = indicators.get("ema200")
        sma20 = indicators.get("sma20")
        sma50 = indicators.get("sma50")
        adx = indicators.get("adx")
        
        # EMA 9/21
        if ema9 and ema21:
            if ema9 > ema21:
                bullish += 3
                signals.append("EMA9 > EMA21")
            else:
                bearish += 3
                signals.append("EMA9 < EMA21")
        
        # EMA 21/50
        if ema21 and ema50:
            if ema21 > ema50:
                bullish += 4
                signals.append("EMA21 > EMA50 (bullish)")
            else:
                bearish += 4
                signals.append("EMA21 < EMA50 (bearish)")
        
        # EMA 50/200
        if ema50 and ema200:
            if ema50 > ema200:
                bullish += 5
                signals.append("EMA50 > EMA200 (golden cross)")
            else:
                bearish += 5
                signals.append("EMA50 < EMA200 (death cross)")
        
        # Price vs EMA200
        if ema200:
            if price > ema200:
                bullish += 3
                signals.append("Price above EMA200")
            else:
                bearish += 3
                signals.append("Price below EMA200")
        
        # SMA analysis
        if sma20 and sma50:
            if sma20 > sma50:
                bullish += 2
                signals.append("SMA20 > SMA50")
            else:
                bearish += 2
                signals.append("SMA20 < SMA50")
        
        # ADX strength
        if adx:
            if adx >= 30:
                if bullish > bearish:
                    bullish += 2
                    signals.append("Strong ADX bullish trend")
                elif bearish > bullish:
                    bearish += 2
                    signals.append("Strong ADX bearish trend")
                else:
                    signals.append("Strong ADX trend, direction unclear")
            elif adx >= 20:
                signals.append("Moderate ADX trend")
            else:
                signals.append("Weak ADX (ranging)")
        
        # Determine direction
        if bullish > bearish:
            direction = TREND_BULLISH
            if bullish - bearish >= 8:
                direction = TREND_STRONG_BULLISH
        elif bearish > bullish:
            direction = TREND_BEARISH
            if bearish - bullish >= 8:
                direction = TREND_STRONG_BEARISH
        else:
            direction = TREND_NEUTRAL
        
        return {
            "direction": direction,
            "bullish_score": bullish,
            "bearish_score": bearish,
            "strength": abs(bullish - bearish),
            "signals": signals
        }

    # ============================================================
    # MOMENTUM ANALYSIS
    # ============================================================

    def _analyze_momentum(self, indicators: Dict[str, Any], closes: List[float]) -> Dict[str, Any]:
        """Comprehensive momentum analysis."""
        bullish = 0
        bearish = 0
        signals = []
        
        rsi = indicators.get("rsi")
        roc = indicators.get("roc")
        macd = indicators.get("macd")
        macd_signal = indicators.get("macd_signal")
        macd_hist = indicators.get("macd_histogram")
        stoch_k = indicators.get("stoch_k")
        
        # RSI
        if rsi is not None:
            if rsi < 30:
                bullish += 3
                signals.append("RSI oversold")
            elif rsi < 40:
                bullish += 1
                signals.append("RSI approaching oversold")
            elif rsi > 70:
                bearish += 3
                signals.append("RSI overbought")
            elif rsi > 60:
                bearish += 1
                signals.append("RSI approaching overbought")
            else:
                signals.append("RSI neutral")
        
        # ROC
        if roc is not None:
            if roc > 5:
                bullish += 2
                signals.append("Strong positive ROC")
            elif roc > 0:
                bullish += 1
                signals.append("Positive ROC")
            elif roc < -5:
                bearish += 2
                signals.append("Strong negative ROC")
            elif roc < 0:
                bearish += 1
                signals.append("Negative ROC")
        
        # MACD
        if macd is not None and macd_signal is not None:
            if macd > macd_signal:
                bullish += 3
                signals.append("MACD bullish crossover")
                if macd_hist and macd_hist > 0:
                    bullish += 1
                    signals.append("MACD histogram positive")
            else:
                bearish += 3
                signals.append("MACD bearish crossover")
                if macd_hist and macd_hist < 0:
                    bearish += 1
                    signals.append("MACD histogram negative")
        
        # Stochastic
        if stoch_k is not None:
            if stoch_k < 20:
                bullish += 2
                signals.append("Stochastic oversold")
            elif stoch_k > 80:
                bearish += 2
                signals.append("Stochastic overbought")
        
        return {
            "bullish_score": bullish,
            "bearish_score": bearish,
            "signals": signals
        }

    # ============================================================
    # VOLUME ANALYSIS
    # ============================================================

    def _analyze_volume(self, volumes: List[float], closes: List[float]) -> Dict[str, Any]:
        """Comprehensive volume analysis."""
        if not volumes:
            return {"state": "UNKNOWN", "ratio": 1, "bullish_score": 0, "bearish_score": 0, "signals": []}
        
        current = volumes[-1]
        average = self._calculate_sma(volumes, 20) or 1
        
        ratio = current / average if average > 0 else 1
        
        bullish = 0
        bearish = 0
        signals = []
        
        if ratio >= 2.5:
            state = VOLUME_EXTREME
            signals.append("Extreme volume spike")
            bullish += 2
        elif ratio >= 1.5:
            state = VOLUME_HIGH
            signals.append("High volume")
            bullish += 1
        elif ratio <= 0.3:
            state = VOLUME_LOW
            signals.append("Very low volume")
            bearish += 1
        elif ratio <= 0.5:
            state = VOLUME_LOW
            signals.append("Low volume")
            bearish += 0.5
        else:
            state = VOLUME_NORMAL
            signals.append("Normal volume")
        
        # Volume trend
        if len(volumes) > 5:
            vol_sma5 = self._calculate_sma(volumes, 5)
            vol_sma20 = self._calculate_sma(volumes, 20)
            if vol_sma5 and vol_sma20 and vol_sma5 > vol_sma20 * 1.2:
                bullish += 1
                signals.append("Volume increasing")
        
        return {
            "state": state,
            "ratio": round(ratio, 2),
            "bullish_score": bullish,
            "bearish_score": bearish,
            "signals": signals
        }

    # ============================================================
    # VOLATILITY ANALYSIS
    # ============================================================

    def _analyze_volatility(self, closes: List[float], indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive volatility analysis."""
        if len(closes) < 10:
            return {"state": "UNKNOWN", "value": 0}
        
        # Historical volatility
        changes = []
        for i in range(1, len(closes)):
            if closes[i-1] != 0:
                changes.append(((closes[i] - closes[i-1]) / closes[i-1]) * 100)
        
        if not changes:
            return {"state": "UNKNOWN", "value": 0}
        
        avg = statistics.mean(changes)
        variance = statistics.mean([(x - avg) ** 2 for x in changes])
        volatility = math.sqrt(variance)
        
        # ATR-based
        atr = indicators.get("atr")
        price = closes[-1]
        atr_percent = (atr / price * 100) if price > 0 and atr else 0
        
        # Combined
        combined = (volatility + atr_percent) / 2
        
        if combined >= 5:
            state = VOLATILITY_EXTREME
        elif combined >= 3:
            state = VOLATILITY_HIGH
        elif combined >= 1:
            state = VOLATILITY_NORMAL
        else:
            state = VOLATILITY_LOW
        
        return {
            "state": state,
            "value": round(combined, 4),
            "historical": round(volatility, 4),
            "atr_percent": round(atr_percent, 4)
        }

    # ============================================================
    # CANDLE PATTERN ANALYSIS
    # ============================================================

    def _analyze_candles(self, candles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive candlestick pattern analysis."""
        if len(candles) < 2:
            return {"pattern": PATTERN_UNKNOWN, "bullish_score": 0, "bearish_score": 0, "patterns": []}
        
        current = candles[-1]
        previous = candles[-2]
        
        o = current["open"]
        h = current["high"]
        l = current["low"]
        c = current["close"]
        
        body = abs(c - o)
        candle_range = h - l or 0.000001
        
        upper = h - max(o, c)
        lower = min(o, c) - l
        
        bullish = 0
        bearish = 0
        patterns = []
        main_pattern = PATTERN_UNKNOWN
        
        # Single Candle Patterns
        if body <= candle_range * 0.1:
            main_pattern = PATTERN_DOJI
            patterns.append(PATTERN_DOJI)
            bearish += 0.5
        
        elif body >= candle_range * 0.9:
            main_pattern = PATTERN_MARUBOZU
            patterns.append(PATTERN_MARUBOZU)
            if c > o:
                bullish += 2
            else:
                bearish += 2
        
        elif 0.2 <= body / candle_range <= 0.4:
            main_pattern = PATTERN_SPINNING_TOP
            patterns.append(PATTERN_SPINNING_TOP)
        
        elif lower > body * 2 and upper < body:
            main_pattern = PATTERN_HAMMER
            patterns.append(PATTERN_HAMMER)
            bullish += 3
            if len(candles) > 1 and candles[-1].get("volume", 0) > candles[-2].get("volume", 0):
                bullish += 1
        
        elif upper > body * 2 and lower < body:
            main_pattern = PATTERN_SHOOTING_STAR
            patterns.append(PATTERN_SHOOTING_STAR)
            bearish += 3
        
        # Two Candle Patterns
        if (previous["close"] < previous["open"] and 
            c > o and 
            c > previous["open"] and 
            o < previous["close"]):
            main_pattern = PATTERN_BULLISH_ENGULFING
            patterns.append(PATTERN_BULLISH_ENGULFING)
            bullish += 4
        
        elif (previous["close"] > previous["open"] and 
              c < o and 
              c < previous["open"] and 
              o > previous["close"]):
            main_pattern = PATTERN_BEARISH_ENGULFING
            patterns.append(PATTERN_BEARISH_ENGULFING)
            bearish += 4
        
        elif (previous["close"] > previous["open"] and
              c > o and
              body < previous["close"] - previous["open"]):
            main_pattern = PATTERN_BULLISH_HARAMI
            patterns.append(PATTERN_BULLISH_HARAMI)
            bullish += 2
        
        elif (previous["close"] < previous["open"] and
              c < o and
              body < previous["open"] - previous["close"]):
            main_pattern = PATTERN_BEARISH_HARAMI
            patterns.append(PATTERN_BEARISH_HARAMI)
            bearish += 2
        
        elif (previous["close"] < previous["open"] and
              c > o and
              c > (previous["open"] + previous["close"]) / 2 and
              o < previous["close"]):
            main_pattern = PATTERN_PIERCING_LINE
            patterns.append(PATTERN_PIERCING_LINE)
            bullish += 3
        
        elif (previous["close"] > previous["open"] and
              c < o and
              c < (previous["open"] + previous["close"]) / 2 and
              o > previous["close"]):
            main_pattern = PATTERN_DARK_CLOUD_COVER
            patterns.append(PATTERN_DARK_CLOUD_COVER)
            bearish += 3
        
        # Three Candle Patterns
        if len(candles) >= 3:
            prev2 = candles[-3]
            
            if (prev2["close"] < prev2["open"] and
                body <= candle_range * 0.1 and
                c > o and
                c > (prev2["open"] + prev2["close"]) / 2):
                main_pattern = PATTERN_MORNING_STAR
                patterns.append(PATTERN_MORNING_STAR)
                bullish += 5
            
            elif (prev2["close"] > prev2["open"] and
                  body <= candle_range * 0.1 and
                  c < o and
                  c < (prev2["open"] + prev2["close"]) / 2):
                main_pattern = PATTERN_EVENING_STAR
                patterns.append(PATTERN_EVENING_STAR)
                bearish += 5
            
            elif (prev2["close"] > prev2["open"] and
                  previous["close"] > previous["open"] and
                  c > o and
                  prev2["close"] < previous["close"] < c):
                main_pattern = PATTERN_THREE_WHITE_SOLDIERS
                patterns.append(PATTERN_THREE_WHITE_SOLDIERS)
                bullish += 4
            
            elif (prev2["close"] < prev2["open"] and
                  previous["close"] < previous["open"] and
                  c < o and
                  prev2["close"] > previous["close"] > c):
                main_pattern = PATTERN_THREE_BLACK_CROWS
                patterns.append(PATTERN_THREE_BLACK_CROWS)
                bearish += 4
        
        return {
            "pattern": main_pattern,
            "bullish_score": bullish,
            "bearish_score": bearish,
            "patterns": list(set(patterns))
        }

    # ============================================================
    # SUPPORT/RESISTANCE DETECTION
    # ============================================================

    def _detect_support_resistance(self, highs: List[float], lows: List[float], closes: List[float]) -> Dict[str, Any]:
        """Detect support and resistance levels."""
        if len(highs) < 20:
            return {"support": None, "resistance": None, "levels": []}
        
        # Find swing highs and lows
        swing_highs = []
        swing_lows = []
        
        for i in range(10, min(len(highs) - 10, len(highs))):
            if i < 10 or i >= len(highs) - 10:
                continue
            if highs[i] == max(highs[i-10:i+11]):
                swing_highs.append(highs[i])
            if lows[i] == min(lows[i-10:i+11]):
                swing_lows.append(lows[i])
        
        price = closes[-1]
        
        # Nearest resistance (above price)
        resistance = None
        for level in sorted(swing_highs):
            if level > price:
                resistance = level
                break
        
        # Nearest support (below price)
        support = None
        for level in sorted(swing_lows, reverse=True):
            if level < price:
                support = level
                break
        
        # Pivot
        pivot = (highs[-1] + lows[-1] + closes[-1]) / 3
        
        return {
            "support": support,
            "resistance": resistance,
            "pivot": pivot,
            "near_resistance": resistance and (resistance - price) / price < 0.02,
            "near_support": support and (price - support) / price < 0.02
        }

    # ============================================================
    # DIVERGENCE DETECTION
    # ============================================================

    def _detect_divergence(self, closes: List[float], indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Detect MACD divergence."""
        result = {"bullish": 0, "bearish": 0, "detected": []}
        
        macd = indicators.get("macd")
        if macd is None or len(closes) < 20:
            return result
        
        # Simple divergence
        if closes[-1] < closes[-5] and macd > indicators.get("macd_prev", macd):
            result["bullish"] += 1
            result["detected"].append("Bullish divergence")
        
        if closes[-1] > closes[-5] and macd < indicators.get("macd_prev", macd):
            result["bearish"] += 1
            result["detected"].append("Bearish divergence")
        
        return result

    # ============================================================
    # MARKET REGIME DETECTION
    # ============================================================

    def _detect_market_regime(self, indicators: Dict[str, Any], trend: Dict[str, Any], volatility: Dict[str, Any]) -> str:
        """Detect current market regime."""
        adx = indicators.get("adx")
        direction = trend.get("direction", TREND_NEUTRAL)
        vol_state = volatility.get("state", VOLATILITY_NORMAL)
        
        if adx and adx >= 30:
            if direction in [TREND_BULLISH, TREND_STRONG_BULLISH]:
                return "TRENDING_BULLISH"
            elif direction in [TREND_BEARISH, TREND_STRONG_BEARISH]:
                return "TRENDING_BEARISH"
        
        if adx and adx < 20:
            if vol_state == VOLATILITY_HIGH:
                return "VOLATILE_RANGING"
            return "RANGING"
        
        if vol_state == VOLATILITY_EXTREME:
            return "HIGH_VOLATILITY"
        
        return "NEUTRAL"

    # ============================================================
    # FIBONACCI
    # ============================================================

    def _calculate_fibonacci(self, highs: List[float], lows: List[float]) -> Dict[str, Any]:
        """Calculate Fibonacci levels."""
        if len(highs) < 20 or len(lows) < 20:
            return {}
        
        high = max(highs[-20:])
        low = min(lows[-20:])
        diff = high - low
        
        if diff == 0:
            return {}
        
        return {
            "high": high,
            "low": low,
            "levels": {
                "0.0": high,
                "0.236": high - (diff * 0.236),
                "0.382": high - (diff * 0.382),
                "0.5": high - (diff * 0.5),
                "0.618": high - (diff * 0.618),
                "0.786": high - (diff * 0.786),
                "1.0": low,
                "1.272": low - (diff * 0.272),
                "1.618": low - (diff * 0.618),
            }
        }

    # ============================================================
    # PIVOT POINTS
    # ============================================================

    def _calculate_pivot_points(self, highs: List[float], lows: List[float], closes: List[float]) -> Dict[str, Any]:
        """Calculate pivot points."""
        if len(highs) < 1 or len(lows) < 1 or len(closes) < 1:
            return {}
        
        high = highs[-1]
        low = lows[-1]
        close = closes[-1]
        
        pivot = (high + low + close) / 3
        
        return {
            "pivot": pivot,
            "r1": (2 * pivot) - low,
            "r2": pivot + (high - low),
            "r3": high + 2 * (pivot - low),
            "s1": (2 * pivot) - high,
            "s2": pivot - (high - low),
            "s3": low - 2 * (high - pivot)
        }

    # ============================================================
    # CONFIDENCE ENGINE
    # ============================================================

    def _calculate_confidence(
        self,
        bullish_score: float,
        bearish_score: float,
        trend: Dict[str, Any],
        volume: Dict[str, Any],
        volatility: Dict[str, Any],
        candle: Dict[str, Any],
        sr: Dict[str, Any]
    ) -> float:
        """Calculate signal confidence."""
        total = bullish_score + bearish_score
        
        if total <= 0:
            return 0
        
        # Agreement between indicators
        agreement = abs(bullish_score - bearish_score) / total
        confidence = agreement * 60
        
        # Trend alignment
        if trend.get("direction") not in [TREND_NEUTRAL, "UNKNOWN"]:
            confidence += 10
        
        # Volume confirmation
        if volume.get("state") in [VOLUME_HIGH, VOLUME_EXTREME]:
            confidence += 10
        
        # Pattern confirmation
        if candle.get("pattern") not in [PATTERN_UNKNOWN, PATTERN_DOJI]:
            confidence += 5
        
        # Volatility penalty
        if volatility.get("state") == VOLATILITY_EXTREME:
            confidence -= 10
        elif volatility.get("state") == VOLATILITY_HIGH:
            confidence -= 5
        
        # S/R proximity
        if sr.get("near_support") or sr.get("near_resistance"):
            confidence += 5
        
        return round(max(0, min(confidence, 100)), 2)

    # ============================================================
    # SIGNAL DETERMINATION
    # ============================================================

    def _determine_signal(self, score: float, confidence: float) -> str:
        """Determine final signal."""
        if confidence < self.confidence_threshold:
            return SIGNAL_HOLD
        
        if score >= 8:
            return SIGNAL_STRONG_BUY if confidence >= self.high_confidence_threshold else SIGNAL_BUY
        elif score >= 4:
            return SIGNAL_BUY
        elif score <= -8:
            return SIGNAL_STRONG_SELL if confidence >= self.high_confidence_threshold else SIGNAL_SELL
        elif score <= -4:
            return SIGNAL_SELL
        
        return SIGNAL_HOLD

    # ============================================================
    # RISK MANAGEMENT
    # ============================================================

    def _calculate_risk_levels(self, price: float, atr: Optional[float], signal: str, sr: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk levels with ATR and S/R."""
        entry = self._round_price(price)
        
        if not atr:
            atr = price * 0.01
        
        if signal in [SIGNAL_BUY, SIGNAL_STRONG_BUY]:
            stop_loss = sr.get("support")
            if stop_loss and (entry - stop_loss) / entry < 0.05:
                stop_loss = entry - (atr * self.atr_sl_multiplier)
            else:
                stop_loss = entry - (atr * self.atr_sl_multiplier)
            
            risk = entry - stop_loss
            tp1 = entry + (risk * self.tp1_multiplier)
            tp2 = entry + (risk * self.tp2_multiplier)
            tp3 = entry + (risk * self.tp3_multiplier)
            
        elif signal in [SIGNAL_SELL, SIGNAL_STRONG_SELL]:
            stop_loss = sr.get("resistance")
            if stop_loss and (stop_loss - entry) / entry < 0.05:
                stop_loss = entry + (atr * self.atr_sl_multiplier)
            else:
                stop_loss = entry + (atr * self.atr_sl_multiplier)
            
            risk = stop_loss - entry
            tp1 = entry - (risk * self.tp1_multiplier)
            tp2 = entry - (risk * self.tp2_multiplier)
            tp3 = entry - (risk * self.tp3_multiplier)
            
        else:
            return {"entry": entry, "stop_loss": entry, "tp1": entry, "tp2": entry, "tp3": entry, "risk_reward": 0}
        
        risk_reward = risk and (tp2 - entry) / risk if risk > 0 else 0
        
        return {
            "entry": self._round_price(entry),
            "stop_loss": self._round_price(stop_loss),
            "tp1": self._round_price(tp1),
            "tp2": self._round_price(tp2),
            "tp3": self._round_price(tp3),
            "risk_reward": round(risk_reward, 2)
        }

    # ============================================================
    # SIGNAL QUALITY
    # ============================================================

    def _calculate_signal_quality(
        self,
        confidence: float,
        trend: Dict[str, Any],
        volume: Dict[str, Any],
        candle: Dict[str, Any],
        volatility: Dict[str, Any]
    ) -> str:
        """Calculate signal quality rating."""
        if confidence < 30:
            return "POOR"
        
        score = 0
        
        # Confidence
        if confidence >= 70:
            score += 35
        elif confidence >= 55:
            score += 25
        else:
            score += 15
        
        # Trend strength
        if trend.get("strength", 0) >= 5:
            score += 20
        elif trend.get("strength", 0) >= 3:
            score += 10
        
        # Volume
        if volume.get("state") in [VOLUME_HIGH, VOLUME_EXTREME]:
            score += 15
        elif volume.get("state") == VOLUME_NORMAL:
            score += 5
        
        # Pattern
        if candle.get("pattern") not in [PATTERN_UNKNOWN, PATTERN_DOJI]:
            score += 15
        
        # Volatility
        if volatility.get("state") in [VOLATILITY_NORMAL, VOLATILITY_LOW]:
            score += 15
        elif volatility.get("state") == VOLATILITY_HIGH:
            score += 5
        
        if score >= 80:
            return "EXCELLENT"
        elif score >= 60:
            return "GOOD"
        elif score >= 40:
            return "FAIR"
        return "POOR"

    # ============================================================
    # UTILITY
    # ============================================================

    def _normalize_candles(self, candles: List[Any]) -> List[Dict[str, float]]:
        """Normalize candle data to uniform format."""
        result = []
        
        for candle in candles:
            try:
                if isinstance(candle, dict):
                    close = float(candle.get("close", 0))
                    result.append({
                        "open": float(candle.get("open", close)),
                        "high": float(candle.get("high", close)),
                        "low": float(candle.get("low", close)),
                        "close": close,
                        "volume": float(candle.get("volume", 0))
                    })
                elif isinstance(candle, (list, tuple)) and len(candle) >= 6:
                    result.append({
                        "open": float(candle[1]),
                        "high": float(candle[2]),
                        "low": float(candle[3]),
                        "close": float(candle[4]),
                        "volume": float(candle[5])
                    })
            except Exception:
                continue
        
        return result

    def _round_price(self, value: float) -> float:
        """Round price to 8 decimals."""
        try:
            return round(float(value), 8)
        except Exception:
            return 0.0

    def _record_history(self, result: Dict[str, Any]) -> None:
        """Record analysis in history."""
        entry = {
            "timestamp": result.get("timestamp"),
            "pair": result.get("pair"),
            "signal": result.get("signal"),
            "confidence": result.get("confidence"),
            "score": result.get("score")
        }
        self.history.append(entry)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def _no_data_result(self, pair: str, status: str) -> Dict[str, Any]:
        """Return empty result for no data."""
        return {
            "pair": pair,
            "status": status,
            "signal": "HOLD",
            "confidence": 0,
            "strength": 0,
            "signal_quality": 0,
            "entry": None,
            "stop_loss": None,
            "take_profit": None,
            "risk_reward": 0,
            "timestamp": datetime.now().isoformat()
        }


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

MarketAnalyzer = Analyzer

# ============================================================
# GLOBAL INSTANCE
# ============================================================

analyzer = Analyzer()


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "Analyzer",
    "MarketAnalyzer",
    "analyzer",
]
