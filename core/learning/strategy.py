# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# STRATEGY ENGINE
#
# Version: 2.0
#
# Purpose:
# - Convert decision into actionable strategy
# - Evaluate confidence and risk
# - Generate trading strategy context
# - Maintain strategy history
# - Provide strategy statistics
# - Support downstream Insight / Evolution engines
#
# Pipeline:
#
# Analysis
#    ↓
# Prediction
#    ↓
# Decision
#    ↓
# Strategy
#    ↓
# Insight / Reflection
#    ↓
# Evolution
#
# ============================================================

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


# ============================================================
#
# STRATEGY ENGINE
#
# ============================================================

class StrategyEngine:

    MAX_HISTORY = 500

    VALID_ACTIONS = {
        "BUY",
        "SELL",
        "HOLD",
    }

    VALID_RISK_LEVELS = {
        "LOW",
        "MEDIUM",
        "HIGH",
    }

    # ========================================================
    #
    # INITIALIZATION
    #
    # ========================================================

    def __init__(self):

        self.strategies: List[Dict[str, Any]] = []

        self.strategy_count = 0

        self.buy_count = 0
        self.sell_count = 0
        self.hold_count = 0

        self.low_risk_count = 0
        self.medium_risk_count = 0
        self.high_risk_count = 0

        self.last_strategy: Optional[Dict[str, Any]] = None

        logger.info(
            "Strategy Engine initialized."
        )

    # ========================================================
    #
    # MAIN STRATEGY GENERATOR
    #
    # ========================================================

    def generate(
        self,
        data
    ):

        if not isinstance(data, dict):

            logger.warning(
                "Strategy generation received invalid data."
            )

            return data

        try:

            decision = data.get(
                "decision",
                {}
            )

            if not isinstance(
                decision,
                dict
            ):

                decision = {}

            analysis = data.get(
                "analysis",
                {}
            )

            if not isinstance(
                analysis,
                dict
            ):

                analysis = {}

            prediction = data.get(
                "prediction",
                {}
            )

            if not isinstance(
                prediction,
                dict
            ):

                prediction = {}

            # ------------------------------------------------
            # BASIC DECISION DATA
            # ------------------------------------------------

            action = self.normalize_action(
                decision.get(
                    "action",
                    "HOLD"
                )
            )

            confidence = self.normalize_confidence(
                decision.get(
                    "confidence",
                    analysis.get(
                        "confidence",
                        prediction.get(
                            "confidence",
                            0
                        )
                    )
                )
            )

            sentiment = str(
                decision.get(
                    "sentiment",
                    analysis.get(
                        "sentiment",
                        "neutral"
                    )
                )
            ).lower()

            # ------------------------------------------------
            # RISK
            # ------------------------------------------------

            risk_score = self.calculate_risk_score(
                confidence=confidence,
                action=action,
                sentiment=sentiment
            )

            risk = self.risk_level(
                decision={
                    "confidence": confidence,
                    "action": action,
                    "sentiment": sentiment,
                }
            )

            # ------------------------------------------------
            # STRATEGY BIAS
            # ------------------------------------------------

            bias = self.generate_bias(
                action=action,
                sentiment=sentiment,
                confidence=confidence
            )

            # ------------------------------------------------
            # ENTRY / EXIT
            # ------------------------------------------------

            entry = self.generate_entry_condition(
                action=action,
                confidence=confidence,
                sentiment=sentiment
            )

            exit_condition = self.generate_exit_condition(
                action=action,
                confidence=confidence
            )

            # ------------------------------------------------
            # POSITION GUIDANCE
            # ------------------------------------------------

            position = self.position_guidance(
                action=action,
                confidence=confidence,
                risk=risk
            )

            # ------------------------------------------------
            # REWARD / RISK
            # ------------------------------------------------

            reward_risk = self.estimate_reward_risk(
                confidence=confidence,
                risk=risk
            )

            # ------------------------------------------------
            # RATIONALE
            # ------------------------------------------------

            rationale = self.build_rationale(
                action=action,
                confidence=confidence,
                sentiment=sentiment,
                risk=risk
            )

            # ------------------------------------------------
            # STRATEGY ID
            # ------------------------------------------------

            strategy_id = self.create_strategy_id()

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            strategy = {

                "id":
                    strategy_id,

                "timestamp":
                    datetime.now().isoformat(),

                "action":
                    action,

                "confidence":
                    confidence,

                "sentiment":
                    sentiment,

                "bias":
                    bias,

                "risk":
                    risk,

                "risk_score":
                    risk_score,

                "position":
                    position,

                "entry":
                    entry,

                "exit":
                    exit_condition,

                "reward_risk":
                    reward_risk,

                "rationale":
                    rationale,

                "source": {

                    "analysis":
                        bool(analysis),

                    "prediction":
                        bool(prediction),

                    "decision":
                        bool(decision),

                },

            }

            # ------------------------------------------------
            # STORE
            # ------------------------------------------------

            self.strategies.append(
                strategy
            )

            self.strategy_count += 1

            self.last_strategy = strategy

            self.update_counters(
                action=action,
                risk=risk
            )

            self.trim_history()

            # ------------------------------------------------
            # ATTACH TO PIPELINE
            # ------------------------------------------------

            data["strategy"] = strategy

            return data

        except Exception as e:

            logger.exception(
                "Strategy generation failed: %s",
                e
            )

            return data

    # ========================================================
    #
    # ACTION NORMALIZATION
    #
    # ========================================================

    def normalize_action(
        self,
        action
    ):

        if action is None:

            return "HOLD"

        action = str(
            action
        ).upper().strip()

        if action not in self.VALID_ACTIONS:

            return "HOLD"

        return action

    # ========================================================
    #
    # CONFIDENCE NORMALIZATION
    #
    # ========================================================

    def normalize_confidence(
        self,
        confidence
    ):

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            return 0.0

        return round(
            max(
                0.0,
                min(
                    100.0,
                    confidence
                )
            ),
            2
        )

    # ========================================================
    #
    # RISK LEVEL
    #
    # ========================================================

    def risk_level(
        self,
        decision
    ):

        if not isinstance(
            decision,
            dict
        ):

            return "HIGH"

        confidence = self.normalize_confidence(
            decision.get(
                "confidence",
                0
            )
        )

        action = self.normalize_action(
            decision.get(
                "action",
                "HOLD"
            )
        )

        # HOLD does not automatically mean low risk.
        # Low confidence means uncertainty remains high.

        if action == "HOLD":

            if confidence >= 80:

                return "LOW"

            elif confidence >= 55:

                return "MEDIUM"

            return "HIGH"

        if confidence >= 80:

            return "LOW"

        if confidence >= 55:

            return "MEDIUM"

        return "HIGH"

    # ========================================================
    #
    # RISK SCORE
    #
    # ========================================================

    def calculate_risk_score(
        self,
        confidence,
        action,
        sentiment
    ):

        confidence = self.normalize_confidence(
            confidence
        )

        # Base risk is inverse of confidence.

        risk_score = 100 - confidence

        # HOLD with uncertain sentiment remains cautious.

        if action == "HOLD":

            risk_score += 5

        # Sentiment/action disagreement increases risk.

        if (
            action == "BUY"
            and sentiment == "negative"
        ):

            risk_score += 15

        if (
            action == "SELL"
            and sentiment == "positive"
        ):

            risk_score += 15

        return round(
            max(
                0.0,
                min(
                    100.0,
                    risk_score
                )
            ),
            2
        )

    # ========================================================
    #
    # STRATEGY BIAS
    #
    # ========================================================

    def generate_bias(
        self,
        action,
        sentiment,
        confidence
    ):

        if action == "BUY":

            if confidence >= 80:

                return "STRONG_BULLISH"

            return "BULLISH"

        if action == "SELL":

            if confidence >= 80:

                return "STRONG_BEARISH"

            return "BEARISH"

        if sentiment == "positive":

            return "NEUTRAL_BULLISH"

        if sentiment == "negative":

            return "NEUTRAL_BEARISH"

        return "NEUTRAL"

    # ========================================================
    #
    # ENTRY CONDITION
    #
    # ========================================================

    def generate_entry_condition(
        self,
        action,
        confidence,
        sentiment
    ):

        if action == "BUY":

            return {

                "direction":
                    "LONG",

                "condition":
                    "Bullish confirmation",

                "minimum_confidence":
                    55,

                "confirmation_required":
                    confidence < 80,

            }

        if action == "SELL":

            return {

                "direction":
                    "SHORT",

                "condition":
                    "Bearish confirmation",

                "minimum_confidence":
                    55,

                "confirmation_required":
                    confidence < 80,

            }

        return {

            "direction":
                "NONE",

            "condition":
                "Wait for directional confirmation",

            "minimum_confidence":
                0,

            "confirmation_required":
                True,

        }

    # ========================================================
    #
    # EXIT CONDITION
    #
    # ========================================================

    def generate_exit_condition(
        self,
        action,
        confidence
    ):

        if action == "BUY":

            return {

                "direction":
                    "LONG",

                "trigger":
                    "Bullish thesis invalidation",

                "confidence_threshold":
                    max(
                        0,
                        confidence - 20
                    ),

            }

        if action == "SELL":

            return {

                "direction":
                    "SHORT",

                "trigger":
                    "Bearish thesis invalidation",

                "confidence_threshold":
                    max(
                        0,
                        confidence - 20
                    ),

            }

        return {

            "direction":
                "NONE",

            "trigger":
                "Directional signal appears",

            "confidence_threshold":
                50,

        }

    # ========================================================
    #
    # POSITION GUIDANCE
    #
    # ========================================================

    def position_guidance(
        self,
        action,
        confidence,
        risk
    ):

        if action == "HOLD":

            return "NO_POSITION"

        if risk == "HIGH":

            return "SMALL"

        if risk == "MEDIUM":

            return "NORMAL"

        if confidence >= 85:

            return "FULL"

        return "NORMAL"

    # ========================================================
    #
    # REWARD / RISK ESTIMATION
    #
    # ========================================================

    def estimate_reward_risk(
        self,
        confidence,
        risk
    ):

        if risk == "LOW":

            ratio = 3.0

        elif risk == "MEDIUM":

            ratio = 2.0

        else:

            ratio = 1.0

        return {

            "estimated_ratio":
                ratio,

            "minimum_acceptable":
                1.5,

            "favorable":
                ratio >= 1.5,

            "confidence":
                confidence,

        }

    # ========================================================
    #
    # RATIONALE
    #
    # ========================================================

    def build_rationale(
        self,
        action,
        confidence,
        sentiment,
        risk
    ):

        if action == "BUY":

            base = (
                "Bullish strategy generated "
                "from positive directional evidence."
            )

        elif action == "SELL":

            base = (
                "Bearish strategy generated "
                "from negative directional evidence."
            )

        else:

            base = (
                "No directional strategy activated. "
                "System recommends waiting for confirmation."
            )

        return (
            f"{base} "
            f"Sentiment={sentiment}, "
            f"confidence={confidence}%, "
            f"risk={risk}."
        )

    # ========================================================
    #
    # STRATEGY ID
    #
    # ========================================================

    def create_strategy_id(
        self
    ):

        return (
            f"STR-{self.strategy_count + 1:06d}"
        )

    # ========================================================
    #
    # COUNTERS
    #
    # ========================================================

    def update_counters(
        self,
        action,
        risk
    ):

        if action == "BUY":

            self.buy_count += 1

        elif action == "SELL":

            self.sell_count += 1

        else:

            self.hold_count += 1

        if risk == "LOW":

            self.low_risk_count += 1

        elif risk == "MEDIUM":

            self.medium_risk_count += 1

        else:

            self.high_risk_count += 1

    # ========================================================
    #
    # HISTORY TRIM
    #
    # ========================================================

    def trim_history(
        self
    ):

        if len(
            self.strategies
        ) > self.MAX_HISTORY:

            excess = (
                len(self.strategies)
                - self.MAX_HISTORY
            )

            del self.strategies[
                :excess
            ]

    # ========================================================
    #
    # LATEST STRATEGY
    #
    # ========================================================

    def latest(
        self
    ):

        return self.last_strategy

    # ========================================================
    #
    # HISTORY
    #
    # ========================================================

    def history(
        self,
        limit=20
    ):

        try:

            limit = int(
                limit
            )

        except (
            TypeError,
            ValueError
        ):

            limit = 20

        if limit <= 0:

            return []

        return self.strategies[
            -limit:
        ]

    # ========================================================
    #
    # SEARCH
    #
    # ========================================================

    def search(
        self,
        keyword
    ):

        if keyword is None:

            return []

        keyword = str(
            keyword
        ).lower()

        return [

            item

            for item in self.strategies

            if keyword in str(
                item
            ).lower()

        ]

    # ========================================================
    #
    # FILTER BY ACTION
    #
    # ========================================================

    def by_action(
        self,
        action
    ):

        action = self.normalize_action(
            action
        )

        return [

            item

            for item in self.strategies

            if item.get(
                "action"
            ) == action

        ]

    # ========================================================
    #
    # FILTER BY RISK
    #
    # ========================================================

    def by_risk(
        self,
        risk
    ):

        risk = str(
            risk
        ).upper().strip()

        if risk not in self.VALID_RISK_LEVELS:

            return []

        return [

            item

            for item in self.strategies

            if item.get(
                "risk"
            ) == risk

        ]

    # ========================================================
    #
    # STATISTICS
    #
    # ========================================================

    def statistics(
        self
    ):

        total = len(
            self.strategies
        )

        if total == 0:

            return {

                "total":
                    0,

                "buy":
                    0,

                "sell":
                    0,

                "hold":
                    0,

                "low_risk":
                    0,

                "medium_risk":
                    0,

                "high_risk":
                    0,

            }

        return {

            "total":
                total,

            "buy":
                self.buy_count,

            "sell":
                self.sell_count,

            "hold":
                self.hold_count,

            "low_risk":
                self.low_risk_count,

            "medium_risk":
                self.medium_risk_count,

            "high_risk":
                self.high_risk_count,

        }

    # ========================================================
    #
    # CLEAR HISTORY
    #
    # ========================================================

    def clear(
        self
    ):

        self.strategies.clear()

        self.last_strategy = None

        return True

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ):

        return {

            "module":
                "strategy",

            "version":
                "2.0",

            "total":
                self.strategy_count,

            "stored":
                len(
                    self.strategies
                ),

            "buy":
                self.buy_count,

            "sell":
                self.sell_count,

            "hold":
                self.hold_count,

            "low_risk":
                self.low_risk_count,

            "medium_risk":
                self.medium_risk_count,

            "high_risk":
                self.high_risk_count,

            "has_latest":
                self.last_strategy is not None,

        }


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

strategy_engine = StrategyEngine()


# ============================================================
#
# PUBLIC API
#
# ============================================================

__all__ = [
    "StrategyEngine",
    "strategy_engine",
]


# ============================================================
#
# END
#
# ============================================================