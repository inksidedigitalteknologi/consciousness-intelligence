# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# MARKET LEARNING MODULE
#
# MODULE VERSION 2.1
#
# Production Intelligence Module
#
# Compatible with:
#   - contracts.py
#   - module_base.py
#   - registry.py
#
# ============================================================

from __future__ import annotations

import logging
import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .module_base import IntelligenceModule
from .contracts import (
    ModuleInput,
    ModuleOutput,
    safe_copy,
    safe_json,
    utc_now,
)

logger = logging.getLogger(__name__)


# ============================================================
#
# MODULE IDENTITY
#
# ============================================================

MODULE_NAME = "market_learning"
MODULE_VERSION = "2.1"

DESCRIPTION = (
    "Market intelligence learning module that evaluates "
    "signal, trend, pattern, volume, momentum, volatility "
    "and market context into a structured learning result."
)


# ============================================================
#
# NORMALIZED STATES
#
# ============================================================

BIAS_BULLISH = "bullish"
BIAS_BEARISH = "bearish"
BIAS_NEUTRAL = "neutral"

STRENGTH_HIGH = "HIGH"
STRENGTH_MEDIUM = "MEDIUM"
STRENGTH_LOW = "LOW"

STATUS_OK = "OK"
STATUS_PARTIAL = "PARTIAL"
STATUS_ERROR = "ERROR"


# ============================================================
#
# HELPER FUNCTIONS
#
# ============================================================

def _normalize_text(value: Any) -> Optional[str]:
    """
    Normalize arbitrary input into lowercase text.

    Empty values become None.
    """

    if value is None:
        return None

    try:
        text = str(value).strip().lower()
    except Exception:
        return None

    return text or None


def _safe_float(value: Any) -> Optional[float]:
    """
    Convert a value to finite float.

    Invalid / non-finite values return None.
    """

    if value is None:
        return None

    try:
        number = float(value)

        if not math.isfinite(number):
            return None

        return number

    except Exception:
        return None


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    """
    Clamp numeric value into a safe range.
    """

    try:
        value = float(value)
    except Exception:
        return minimum

    return max(
        minimum,
        min(maximum, value),
    )


def _normalize_bias(value: Any) -> str:
    """
    Normalize market direction.
    """

    text = _normalize_text(value)

    if text in {
        "bullish",
        "buy",
        "long",
        "up",
        "positive",
        "strong bullish",
    }:
        return BIAS_BULLISH

    if text in {
        "bearish",
        "sell",
        "short",
        "down",
        "negative",
        "strong bearish",
    }:
        return BIAS_BEARISH

    return BIAS_NEUTRAL


def _normalize_strength(value: Any) -> Optional[str]:
    """
    Normalize qualitative strength.
    """

    text = _normalize_text(value)

    if not text:
        return None

    if text in {
        "high",
        "strong",
        "very strong",
        "extreme",
    }:
        return STRENGTH_HIGH

    if text in {
        "medium",
        "moderate",
        "normal",
    }:
        return STRENGTH_MEDIUM

    if text in {
        "low",
        "weak",
        "very weak",
    }:
        return STRENGTH_LOW

    return str(value).upper()


def _timestamp() -> str:
    """
    UTC timestamp helper.
    """

    return utc_now()


# ============================================================
#
# MARKET LEARNING MODULE
#
# ============================================================

class MarketLearning(IntelligenceModule):
    """
    Universal market learning module.

    The module intentionally does not perform exchange/API
    operations. It analyzes structured market information
    supplied by another layer.

    Expected payload examples:

        {
            "input": {
                "market": "BTC/USD",
                "signal": "bullish",
                "pattern": "breakout",
                "volume": "high",
                "trend": "bullish",
                "momentum": "strong",
                "volatility": "normal"
            },
            "cycle": 10
        }

    Numeric values are also accepted where available.
    """

    # ========================================================
    #
    # IDENTITY
    #
    # ========================================================

    NAME = MODULE_NAME
    VERSION = MODULE_VERSION
    DESCRIPTION = DESCRIPTION

    # ========================================================
    #
    # CAPABILITIES
    #
    # ========================================================

    CAPABILITIES = [
        "market_learning",
        "market_analysis",
        "signal_analysis",
        "pattern_analysis",
        "volume_analysis",
        "trend_analysis",
        "momentum_analysis",
        "volatility_analysis",
        "market_context",
        "confidence_scoring",
        "evidence_generation",
        "structured_assessment",
    ]

    # ========================================================
    #
    # OPERATIONS
    #
    # ========================================================

    OPERATIONS = [
        "process",
        "analyze",
        "learn",
    ]

    # ========================================================
    #
    # PRIORITY
    #
    # ========================================================

    PRIORITY = 50

    # Market learning should normally not stop the engine.
    CRITICAL = False

    # ========================================================
    #
    # DEFAULT CONFIGURATION
    #
    # ========================================================

    DEFAULT_CONFIG = {

        # Minimum confidence required to call
        # an assessment meaningful.
        "minimum_confidence": 35.0,

        # Confidence required for strong assessment.
        "strong_confidence": 75.0,

        # Confidence required for medium assessment.
        "medium_confidence": 55.0,

        # Whether neutral observations should be
        # included in the result.
        "include_neutral_observations": True,

        # Whether detailed scoring should be returned.
        "include_scoring": True,

        # Whether evidence should be returned.
        "include_evidence": True,

        # Whether learning features should be returned.
        "include_learning_features": True,

        # Whether recommendation should be generated.
        "generate_recommendation": True,

    }

    # ========================================================
    #
    # INIT
    #
    # ========================================================

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            config=config
        )

        self.calls = 0

        self.learning_cycles = 0

        self.bullish_count = 0

        self.bearish_count = 0

        self.neutral_count = 0

        self.high_confidence_count = 0

        self.last_assessment: Optional[str] = None

        self.last_bias: Optional[str] = None

        self.last_market: Optional[str] = None

        self.total_confidence = 0.0

        logger.info(
            "MarketLearning initialized: %s v%s",
            self.NAME,
            self.VERSION,
        )

    # ========================================================
    #
    # PRIMARY PROCESS
    #
    # ========================================================

    def process(
        self,
        payload: Any,
    ) -> ModuleOutput:
        """
        Analyze market payload.

        This method follows the IntelligenceModule contract.
        """

        self.calls += 1
        self.learning_cycles += 1

        # ----------------------------------------------------
        # PAYLOAD VALIDATION
        # ----------------------------------------------------

        if not isinstance(payload, dict):

            output = ModuleOutput(
                data=None,
                success=False,
                module=self.NAME,
                version=self.VERSION,
            )

            output.mark_failed(
                "Payload must be a dictionary."
            )

            return output

        # ----------------------------------------------------
        # EXTRACT INPUT
        # ----------------------------------------------------

        input_data = payload.get(
            "input",
            payload,
        )

        if not isinstance(input_data, dict):

            input_data = {}

        # Safe copy prevents mutation of caller data.
        input_data = safe_copy(
            input_data
        )

        # ----------------------------------------------------
        # BASIC MARKET DATA
        # ----------------------------------------------------

        market = input_data.get(
            "market"
        )

        symbol = input_data.get(
            "symbol"
        )

        timeframe = input_data.get(
            "timeframe"
        )

        signal = input_data.get(
            "signal"
        )

        pattern = input_data.get(
            "pattern"
        )

        volume = input_data.get(
            "volume"
        )

        trend = input_data.get(
            "trend"
        )

        momentum = input_data.get(
            "momentum"
        )

        volatility = input_data.get(
            "volatility"
        )

        # ----------------------------------------------------
        # NUMERIC DATA
        # ----------------------------------------------------

        signal_score = _safe_float(
            input_data.get(
                "signal_score"
            )
        )

        volume_score = _safe_float(
            input_data.get(
                "volume_score"
            )
        )

        momentum_score = _safe_float(
            input_data.get(
                "momentum_score"
            )
        )

        trend_score = _safe_float(
            input_data.get(
                "trend_score"
            )
        )

        pattern_score = _safe_float(
            input_data.get(
                "pattern_score"
            )
        )

        volatility_score = _safe_float(
            input_data.get(
                "volatility_score"
            )
        )

        confidence_input = _safe_float(
            input_data.get(
                "confidence"
            )
        )

        # ----------------------------------------------------
        # NORMALIZE STATES
        # ----------------------------------------------------

        normalized_signal = _normalize_bias(
            signal
        )

        normalized_trend = _normalize_bias(
            trend
        )

        normalized_pattern = _normalize_text(
            pattern
        )

        normalized_volume = _normalize_text(
            volume
        )

        normalized_momentum = _normalize_text(
            momentum
        )

        normalized_volatility = _normalize_text(
            volatility
        )

        # ----------------------------------------------------
        # TRACK LAST CONTEXT
        # ----------------------------------------------------

        self.last_market = (
            str(market)
            if market is not None
            else None
        )

        self.last_bias = normalized_signal

        # ====================================================
        #
        # OBSERVATIONS
        #
        # ====================================================

        observations: List[str] = []

        evidence: List[str] = []

        warnings: List[str] = []

        # ----------------------------------------------------
        # SIGNAL
        # ----------------------------------------------------

        if normalized_signal == BIAS_BULLISH:

            observations.append(
                "Market signal indicates bullish bias."
            )

            evidence.append(
                "Bullish signal detected."
            )

        elif normalized_signal == BIAS_BEARISH:

            observations.append(
                "Market signal indicates bearish bias."
            )

            evidence.append(
                "Bearish signal detected."
            )

        elif signal:

            observations.append(
                f"Market signal detected: {signal}."
            )

        elif self.config.get(
            "include_neutral_observations",
            True,
        ):

            observations.append(
                "No directional market signal was provided."
            )

        # ----------------------------------------------------
        # TREND
        # ----------------------------------------------------

        if normalized_trend == BIAS_BULLISH:

            observations.append(
                "Trend structure currently favors the upside."
            )

            evidence.append(
                "Bullish trend context."
            )

        elif normalized_trend == BIAS_BEARISH:

            observations.append(
                "Trend structure currently favors the downside."
            )

            evidence.append(
                "Bearish trend context."
            )

        elif trend:

            observations.append(
                f"Trend condition: {trend}."
            )

        # ----------------------------------------------------
        # PATTERN
        # ----------------------------------------------------

        if normalized_pattern == "breakout":

            observations.append(
                "Breakout pattern detected."
            )

            evidence.append(
                "Breakout structure detected."
            )

        elif normalized_pattern in {
            "breakdown",
            "bearish_breakdown",
        }:

            observations.append(
                "Breakdown pattern detected."
            )

            evidence.append(
                "Bearish breakdown structure detected."
            )

        elif normalized_pattern in {
            "reversal",
            "bullish_reversal",
        }:

            observations.append(
                "Potential reversal pattern detected."
            )

            evidence.append(
                "Reversal structure detected."
            )

        elif normalized_pattern:

            observations.append(
                f"Pattern detected: {pattern}."
            )

        # ----------------------------------------------------
        # VOLUME
        # ----------------------------------------------------

        if normalized_volume == "high":

            observations.append(
                "High volume indicates stronger market participation."
            )

            evidence.append(
                "High-volume confirmation."
            )

        elif normalized_volume == "low":

            observations.append(
                "Low volume indicates weaker market participation."
            )

            warnings.append(
                "Volume confirmation is weak."
            )

        elif normalized_volume:

            observations.append(
                f"Volume condition: {volume}."
            )

        # ----------------------------------------------------
        # MOMENTUM
        # ----------------------------------------------------

        if normalized_momentum in {
            "strong",
            "high",
            "positive",
            "bullish",
        }:

            observations.append(
                "Momentum supports continued directional movement."
            )

            evidence.append(
                "Positive momentum detected."
            )

        elif normalized_momentum in {
            "weak",
            "low",
            "negative",
            "bearish",
        }:

            observations.append(
                "Momentum is weak or unfavorable."
            )

            warnings.append(
                "Momentum confirmation is weak."
            )

        elif normalized_momentum:

            observations.append(
                f"Momentum condition: {momentum}."
            )

        # ----------------------------------------------------
        # VOLATILITY
        # ----------------------------------------------------

        if normalized_volatility in {
            "high",
            "extreme",
        }:

            observations.append(
                "Volatility is elevated and may increase market risk."
            )

            warnings.append(
                "Elevated volatility detected."
            )

        elif normalized_volatility in {
            "low",
            "very low",
        }:

            observations.append(
                "Low volatility suggests a quieter market environment."
            )

        elif normalized_volatility:

            observations.append(
                f"Volatility condition: {volatility}."
            )

        # ====================================================
        #
        # SCORING ENGINE
        #
        # ====================================================

        bullish_points = 0.0

        bearish_points = 0.0

        score_reasons: List[str] = []

        # ----------------------------------------------------
        # SIGNAL SCORE
        # ----------------------------------------------------

        if normalized_signal == BIAS_BULLISH:

            bullish_points += 30.0

            score_reasons.append(
                "Bullish signal +30"
            )

        elif normalized_signal == BIAS_BEARISH:

            bearish_points += 30.0

            score_reasons.append(
                "Bearish signal +30"
            )

        # ----------------------------------------------------
        # TREND SCORE
        # ----------------------------------------------------

        if normalized_trend == BIAS_BULLISH:

            bullish_points += 20.0

            score_reasons.append(
                "Bullish trend +20"
            )

        elif normalized_trend == BIAS_BEARISH:

            bearish_points += 20.0

            score_reasons.append(
                "Bearish trend +20"
            )

        # ----------------------------------------------------
        # BREAKOUT / BREAKDOWN
        # ----------------------------------------------------

        if normalized_pattern == "breakout":

            bullish_points += 20.0

            score_reasons.append(
                "Breakout pattern +20"
            )

        elif normalized_pattern in {
            "breakdown",
            "bearish_breakdown",
        }:

            bearish_points += 20.0

            score_reasons.append(
                "Breakdown pattern +20"
            )

        # ----------------------------------------------------
        # VOLUME
        # ----------------------------------------------------

        if normalized_volume == "high":

            if (
                normalized_signal
                == BIAS_BULLISH
            ):

                bullish_points += 15.0

                score_reasons.append(
                    "High volume bullish confirmation +15"
                )

            elif (
                normalized_signal
                == BIAS_BEARISH
            ):

                bearish_points += 15.0

                score_reasons.append(
                    "High volume bearish confirmation +15"
                )

            else:

                bullish_points += 5.0

                score_reasons.append(
                    "High volume activity +5"
                )

        elif normalized_volume == "low":

            score_reasons.append(
                "Low volume provides weak confirmation"
            )

        # ----------------------------------------------------
        # MOMENTUM
        # ----------------------------------------------------

        if normalized_momentum in {
            "strong",
            "high",
            "positive",
            "bullish",
        }:

            if normalized_signal == BIAS_BEARISH:

                bearish_points += 10.0

            else:

                bullish_points += 10.0

            score_reasons.append(
                "Positive momentum +10"
            )

        elif normalized_momentum in {
            "weak",
            "low",
            "negative",
            "bearish",
        }:

            if normalized_signal == BIAS_BULLISH:

                bullish_points -= 5.0

            elif normalized_signal == BIAS_BEARISH:

                bearish_points -= 5.0

            score_reasons.append(
                "Weak momentum -5"
            )

        # ----------------------------------------------------
        # EXTERNAL NUMERIC SCORES
        # ----------------------------------------------------

        numeric_scores = {
            "signal": signal_score,
            "volume": volume_score,
            "momentum": momentum_score,
            "trend": trend_score,
            "pattern": pattern_score,
            "volatility": volatility_score,
        }

        numeric_scores = {
            key: _clamp(value)
            for key, value in numeric_scores.items()
            if value is not None
        }

        # ====================================================
        #
        # DIRECTION
        #
        # ====================================================

        if bullish_points > bearish_points:

            bias = BIAS_BULLISH

        elif bearish_points > bullish_points:

            bias = BIAS_BEARISH

        else:

            bias = BIAS_NEUTRAL

        # ====================================================
        #
        # RAW STRENGTH
        #
        # ====================================================

        directional_score = max(
            bullish_points,
            bearish_points,
        )

        opposing_score = min(
            bullish_points,
            bearish_points,
        )

        separation = max(
            0.0,
            directional_score
            - opposing_score,
        )

        confidence = (
            directional_score
            + separation * 0.35
        )

        # ----------------------------------------------------
        # External confidence can contribute.
        # ----------------------------------------------------

        if confidence_input is not None:

            confidence = (
                confidence * 0.70
                + confidence_input * 0.30
            )

        # ----------------------------------------------------
        # Numeric component scores
        # ----------------------------------------------------

        if numeric_scores:

            numeric_average = (
                sum(
                    numeric_scores.values()
                )
                / len(
                    numeric_scores
                )
            )

            confidence = (
                confidence * 0.75
                + numeric_average * 0.25
            )

        confidence = _clamp(
            confidence
        )

        # ====================================================
        #
        # CONFIDENCE ADJUSTMENTS
        #
        # ====================================================

        if normalized_volume == "low":

            confidence -= 8.0

        if normalized_volatility in {
            "high",
            "extreme",
        }:

            confidence -= 5.0

        if normalized_pattern == "breakout" and (
            normalized_volume == "high"
        ):

            confidence += 8.0

        if normalized_signal == normalized_trend and (
            normalized_signal
            in {
                BIAS_BULLISH,
                BIAS_BEARISH,
            }
        ):

            confidence += 7.0

        confidence = _clamp(
            confidence
        )

        # ====================================================
        #
        # STRENGTH
        #
        # ====================================================

        strong_threshold = float(
            self.config.get(
                "strong_confidence",
                75.0,
            )
        )

        medium_threshold = float(
            self.config.get(
                "medium_confidence",
                55.0,
            )
        )

        if confidence >= strong_threshold:

            strength = STRENGTH_HIGH

        elif confidence >= medium_threshold:

            strength = STRENGTH_MEDIUM

        else:

            strength = STRENGTH_LOW

        # ====================================================
        #
        # ASSESSMENT
        #
        # ====================================================

        if (
            bias == BIAS_BULLISH
            and normalized_pattern == "breakout"
            and normalized_volume == "high"
        ):

            assessment = (
                "Strong bullish breakout context "
                "with volume confirmation."
            )

        elif (
            bias == BIAS_BULLISH
            and strength == STRENGTH_HIGH
        ):

            assessment = (
                "Strong bullish market context "
                "with multiple supporting factors."
            )

        elif bias == BIAS_BULLISH:

            assessment = (
                "Bullish market context detected, "
                "but confirmation is incomplete."
            )

        elif (
            bias == BIAS_BEARISH
            and normalized_pattern
            in {
                "breakdown",
                "bearish_breakdown",
            }
            and normalized_volume == "high"
        ):

            assessment = (
                "Strong bearish breakdown context "
                "with volume confirmation."
            )

        elif (
            bias == BIAS_BEARISH
            and strength == STRENGTH_HIGH
        ):

            assessment = (
                "Strong bearish market context "
                "with multiple supporting factors."
            )

        elif bias == BIAS_BEARISH:

            assessment = (
                "Bearish market context detected."
            )

        else:

            assessment = (
                "Insufficient directional evidence "
                "for a strong market assessment."
            )

        # ====================================================
        #
        # RECOMMENDATION
        #
        # ====================================================

        recommendation = (
            "WAIT_FOR_CONFIRMATION"
        )

        if (
            bias == BIAS_BULLISH
            and confidence >= strong_threshold
        ):

            recommendation = "BULLISH_BIAS"

        elif (
            bias == BIAS_BEARISH
            and confidence >= strong_threshold
        ):

            recommendation = "BEARISH_BIAS"

        elif (
            bias == BIAS_BULLISH
            and confidence >= medium_threshold
        ):

            recommendation = "MONITOR_BULLISH"

        elif (
            bias == BIAS_BEARISH
            and confidence >= medium_threshold
        ):

            recommendation = "MONITOR_BEARISH"

        # ====================================================
        #
        # LEARNING FEATURES
        #
        # ====================================================

        learning_features = {

            "directional_bias":
                bias,

            "signal_direction":
                normalized_signal,

            "trend_direction":
                normalized_trend,

            "pattern":
                normalized_pattern,

            "volume":
                normalized_volume,

            "momentum":
                normalized_momentum,

            "volatility":
                normalized_volatility,

            "signal_score":
                signal_score,

            "trend_score":
                trend_score,

            "pattern_score":
                pattern_score,

            "volume_score":
                volume_score,

            "momentum_score":
                momentum_score,

            "volatility_score":
                volatility_score,

            "confidence":
                round(
                    confidence,
                    2,
                ),

        }

        # ====================================================
        #
        # MARKET CONTEXT
        #
        # ====================================================

        context = {

            "market":
                market,

            "symbol":
                symbol,

            "timeframe":
                timeframe,

            "cycle":
                payload.get(
                    "cycle"
                ),

            "source":
                payload.get(
                    "source"
                ),

            "timestamp":
                _timestamp(),

        }

        # ====================================================
        #
        # DATA QUALITY
        #
        # ====================================================

        supplied_fields = [

            signal,
            pattern,
            volume,
            trend,
            momentum,
            volatility,

        ]

        available_fields = sum(
            1
            for value in supplied_fields
            if value is not None
        )

        data_completeness = (
            available_fields
            / len(
                supplied_fields
            )
            * 100.0
        )

        if data_completeness < 30:

            warnings.append(
                "Market input contains limited "
                "directional information."
            )

        elif data_completeness < 60:

            warnings.append(
                "Market context is partially populated."
            )

        # ====================================================
        #
        # FINAL STATUS
        #
        # ====================================================

        minimum_confidence = float(
            self.config.get(
                "minimum_confidence",
                35.0,
            )
        )

        if confidence < minimum_confidence:

            status = STATUS_PARTIAL

        else:

            status = STATUS_OK

        # ====================================================
        #
        # RESULT
        #
        # ====================================================

        result: Dict[str, Any] = {

            "status":
                status,

            "module":
                self.NAME,

            "version":
                self.VERSION,

            "timestamp":
                _timestamp(),

            "market":
                market,

            "symbol":
                symbol,

            "timeframe":
                timeframe,

            "signal":
                signal,

            "pattern":
                pattern,

            "volume":
                volume,

            "trend":
                trend,

            "momentum":
                momentum,

            "volatility":
                volatility,

            "bias":
                bias,

            "assessment":
                assessment,

            "strength":
                strength,

            "confidence":
                round(
                    confidence,
                    2,
                ),

            "recommendation":
                recommendation,

            "data_completeness":
                round(
                    data_completeness,
                    2,
                ),

            "observations":
                observations,

            "warnings":
                warnings,

            "cycle":
                payload.get(
                    "cycle"
                ),

        }

        # ----------------------------------------------------
        # SCORING
        # ----------------------------------------------------

        if self.config.get(
            "include_scoring",
            True,
        ):

            result["scoring"] = {

                "bullish_points":
                    round(
                        bullish_points,
                        2,
                    ),

                "bearish_points":
                    round(
                        bearish_points,
                        2,
                    ),

                "directional_score":
                    round(
                        directional_score,
                        2,
                    ),

                "separation":
                    round(
                        separation,
                        2,
                    ),

                "reasons":
                    score_reasons,

            }

        # ----------------------------------------------------
        # EVIDENCE
        # ----------------------------------------------------

        if self.config.get(
            "include_evidence",
            True,
        ):

            result["evidence"] = evidence

        # ----------------------------------------------------
        # LEARNING FEATURES
        # ----------------------------------------------------

        if self.config.get(
            "include_learning_features",
            True,
        ):

            result["learning_features"] = (
                learning_features
            )

        # ----------------------------------------------------
        # CONTEXT
        # ----------------------------------------------------

        result["context"] = context

        # ====================================================
        #
        # UPDATE INTERNAL LEARNING STATE
        #
        # ====================================================

        if bias == BIAS_BULLISH:

            self.bullish_count += 1

        elif bias == BIAS_BEARISH:

            self.bearish_count += 1

        else:

            self.neutral_count += 1

        if confidence >= strong_threshold:

            self.high_confidence_count += 1

        self.total_confidence += confidence

        self.last_assessment = assessment

        # ====================================================
        #
        # OUTPUT
        #
        # ====================================================

        output = ModuleOutput(

            data=safe_json(
                result
            ),

            success=True,

            module=self.NAME,

            version=self.VERSION,

            confidence=confidence,

            stage="market_learning",

            metadata={

                "bias":
                    bias,

                "strength":
                    strength,

                "recommendation":
                    recommendation,

                "data_completeness":
                    round(
                        data_completeness,
                        2,
                    ),

                "cycle":
                    payload.get(
                        "cycle"
                    ),

            },

        )

        if status == STATUS_PARTIAL:

            output.mark_partial()

        for warning in warnings:

            output.add_warning(
                warning
            )

        return output

    # ========================================================
    #
    # ANALYZE
    #
    # ========================================================

    def analyze(
        self,
        payload: Any,
    ) -> ModuleOutput:
        """
        Explicit alias for process().
        """

        return self.process(
            payload
        )

    # ========================================================
    #
    # LEARN
    #
    # ========================================================

    def learn(
        self,
        payload: Any,
    ) -> ModuleOutput:
        """
        Explicit learning operation.

        Currently delegates to process() so the public
        contract remains stable while the learning system
        evolves.
        """

        return self.process(
            payload
        )

    # ========================================================
    #
    # LEARNING SUMMARY
    #
    # ========================================================

    def learning_summary(
        self,
    ) -> Dict[str, Any]:
        """
        Return accumulated learning statistics.
        """

        total_directional = (
            self.bullish_count
            + self.bearish_count
            + self.neutral_count
        )

        average_confidence = 0.0

        if self.calls > 0:

            average_confidence = (
                self.total_confidence
                / self.calls
            )

        return {

            "module":
                self.NAME,

            "version":
                self.VERSION,

            "calls":
                self.calls,

            "learning_cycles":
                self.learning_cycles,

            "bullish":
                self.bullish_count,

            "bearish":
                self.bearish_count,

            "neutral":
                self.neutral_count,

            "high_confidence":
                self.high_confidence_count,

            "average_confidence":
                round(
                    average_confidence,
                    2,
                ),

            "directional_observations":
                total_directional,

            "last_market":
                self.last_market,

            "last_bias":
                self.last_bias,

            "last_assessment":
                self.last_assessment,

        }

    # ========================================================
    #
    # HEALTH
    #
    # ========================================================

    def health(
        self,
    ) -> Dict[str, Any]:
        """
        Extend base health information with
        market-learning metrics.
        """

        result = super().health()

        result.update({

            "learning":

                self.learning_summary(),

        })

        return safe_json(
            result
        )

    # ========================================================
    #
    # GET_STATUS - ADDED FOR COMPATIBILITY
    #
    # ========================================================

    def get_status(
        self,
    ) -> Dict[str, Any]:
        """
        Return module status for integration test compatibility.

        This method is used by the integration test suite
        to display module status in the system status report.
        """

        total_directional = (
            self.bullish_count
            + self.bearish_count
            + self.neutral_count
        )

        average_confidence = 0.0

        if self.calls > 0:
            average_confidence = (
                self.total_confidence
                / self.calls
            )

        return {

            "module":
                self.NAME,

            "name":
                "Market Learning",

            "version":
                self.VERSION,

            "online":
                True,

            "status":
                "ONLINE",

            "calls":
                self.calls,

            "learning_cycles":
                self.learning_cycles,

            "bullish":
                self.bullish_count,

            "bearish":
                self.bearish_count,

            "neutral":
                self.neutral_count,

            "high_confidence":
                self.high_confidence_count,

            "average_confidence":
                round(
                    average_confidence,
                    2,
                ),

            "directional_observations":
                total_directional,

            "last_market":
                self.last_market,

            "last_bias":
                self.last_bias,

            "last_assessment":
                self.last_assessment,

            "timestamp":
                _timestamp(),
        }

    # ========================================================
    #
    # STATUS - ALIAS FOR COMPATIBILITY
    #
    # ========================================================

    # Method status() sebagai alias untuk get_status()
    # Ini memastikan kompatibilitas dengan test
    def status(
        self,
    ) -> Dict[str, Any]:
        """
        Alias for get_status() for integration test compatibility.
        """
        return self.get_status()

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self,
    ) -> bool:
        """
        Reset runtime learning statistics while
        preserving configuration.
        """

        try:

            super().reset()

            self.calls = 0

            self.learning_cycles = 0

            self.bullish_count = 0

            self.bearish_count = 0

            self.neutral_count = 0

            self.high_confidence_count = 0

            self.last_assessment = None

            self.last_bias = None

            self.last_market = None

            self.total_confidence = 0.0

            return True

        except Exception as exc:

            logger.exception(
                "MarketLearning reset failed: %s",
                exc,
            )

            return False


# ============================================================
#
# MODULE FACTORY
#
# ============================================================

def create_market_learning(
    config: Optional[
        Dict[str, Any]
    ] = None,
) -> MarketLearning:
    """
    Factory for creating MarketLearning instances.
    """

    return MarketLearning(
        config=config
    )


# ============================================================
#
# MODULE INSTANCE
#
# ============================================================

market_learning = MarketLearning()


# ============================================================
#
# BACKWARD COMPATIBILITY FUNCTION
#
# ============================================================

def process(
    payload: Any,
) -> ModuleOutput:
    """
    Legacy-compatible module-level process function.
    """

    return market_learning.process(
        payload
    )


# ============================================================
#
# HEALTH
#
# ============================================================

def health() -> Dict[str, Any]:
    """
    Module-level health access.
    """

    return market_learning.health()


# ============================================================
#
# LEARNING SUMMARY
#
# ============================================================

def learning_summary() -> Dict[str, Any]:
    """
    Module-level learning summary.
    """

    return market_learning.learning_summary()


# ============================================================
#
# GET_STATUS - ADDED FOR COMPATIBILITY
#
# ============================================================

def get_status() -> Dict[str, Any]:
    """
    Module-level status access.
    """

    return market_learning.get_status()


# ============================================================
#
# STATUS - ALIAS FOR COMPATIBILITY
#
# ============================================================

def status() -> Dict[str, Any]:
    """
    Alias for get_status() for integration test compatibility.
    """

    return get_status()


# ============================================================
#
# SELF TEST
#
# ============================================================

def self_test() -> Dict[str, Any]:
    """
    Run a local module test without requiring engine.py.
    """

    test_payload = {

        "input": {

            "market":
                "BTC/USD",

            "symbol":
                "BTC/USD",

            "timeframe":
                "1h",

            "signal":
                "bullish",

            "pattern":
                "breakout",

            "volume":
                "high",

            "trend":
                "bullish",

            "momentum":
                "strong",

            "volatility":
                "normal",

        },

        "cycle":
            1,

        "source":
            "self_test",

    }

    result = market_learning.process(
        test_payload
    )

    valid = (
        isinstance(
            result,
            ModuleOutput,
        )
        and result.module
        == MODULE_NAME
        and result.success
    )

    return {

        "module":
            MODULE_NAME,

        "version":
            MODULE_VERSION,

        "success":
            valid,

        "result":
            result.to_dict(),

        "health":
            market_learning.health(),

        "get_status":
            market_learning.get_status(),

        "status":
            market_learning.status(),

    }


# ============================================================
#
# PUBLIC API
#
# ============================================================

__all__ = [

    "MODULE_NAME"]