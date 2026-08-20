# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# DECISION ENGINE
#
# Version: 2.0
#
# Responsibilities:
#
# - Analyze Decision Context
# - Combine Analysis Signals
# - Evaluate Confidence
# - Detect Signal Conflicts
# - Calculate Decision Score
# - Determine BUY / SELL / HOLD
# - Determine Risk Level
# - Generate Decision Reasoning
# - Track Decision History
# - Provide Decision Statistics
# - Support Backward Compatibility
#
# ============================================================

import logging
from datetime import datetime
from statistics import mean

logger = logging.getLogger(__name__)


# ============================================================
#
# DECISION ENGINE
#
# ============================================================

class DecisionEngine:

    # ========================================================
    # CONFIGURATION
    # ========================================================

    DEFAULT_BUY_THRESHOLD = 70
    DEFAULT_SELL_THRESHOLD = 70

    DEFAULT_MIN_CONFIDENCE = 55

    MAX_HISTORY = 500

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        buy_threshold=None,
        sell_threshold=None,
        min_confidence=None,
        max_history=None
    ):

        self.buy_threshold = (
            buy_threshold
            if buy_threshold is not None
            else self.DEFAULT_BUY_THRESHOLD
        )

        self.sell_threshold = (
            sell_threshold
            if sell_threshold is not None
            else self.DEFAULT_SELL_THRESHOLD
        )

        self.min_confidence = (
            min_confidence
            if min_confidence is not None
            else self.DEFAULT_MIN_CONFIDENCE
        )

        self.max_history = (
            max_history
            if max_history is not None
            else self.MAX_HISTORY
        )

        self.decisions = 0

        self.history = []

        self.action_counts = {
            "BUY": 0,
            "SELL": 0,
            "HOLD": 0
        }

        self.confidence_history = []

        self.score_history = []

        logger.info(
            "Decision Engine initialized."
        )

    # ========================================================
    #
    # MAIN DECISION
    #
    # ========================================================

    def decide(
        self,
        data
    ):

        try:

            if not isinstance(data, dict):

                data = {
                    "input": data
                }

            analysis = self._get_dict(
                data.get(
                    "analysis"
                )
            )

            prediction = self._get_dict(
                data.get(
                    "prediction"
                )
            )

            semantic = self._get_dict(
                data.get(
                    "semantic"
                )
            )

            insight = self._get_dict(
                data.get(
                    "insight"
                )
            )

            reasoning = self._get_dict(
                data.get(
                    "reasoning"
                )
            )

            context = self._get_dict(
                data.get(
                    "context"
                )
            )

            # ------------------------------------------------
            # Extract signals
            # ------------------------------------------------

            sentiment = self.normalize_sentiment(
                analysis.get(
                    "sentiment",
                    semantic.get(
                        "sentiment",
                        "neutral"
                    )
                )
            )

            confidence = self.extract_confidence(
                analysis,
                prediction,
                insight,
                reasoning
            )

            score = self.calculate_score(
                sentiment=sentiment,
                confidence=confidence,
                analysis=analysis,
                prediction=prediction,
                semantic=semantic,
                insight=insight,
                reasoning=reasoning
            )

            # ------------------------------------------------
            # Conflict detection
            # ------------------------------------------------

            conflicts = self.detect_conflicts(
                analysis=analysis,
                prediction=prediction,
                semantic=semantic,
                reasoning=reasoning
            )

            # ------------------------------------------------
            # Risk assessment
            # ------------------------------------------------

            risk = self.calculate_risk(
                confidence=confidence,
                score=score,
                sentiment=sentiment,
                conflicts=conflicts
            )

            # ------------------------------------------------
            # Determine action
            # ------------------------------------------------

            action = self.determine_action(
                score=score,
                confidence=confidence,
                sentiment=sentiment,
                conflicts=conflicts
            )

            # ------------------------------------------------
            # Generate reasoning
            # ------------------------------------------------

            reason = self.generate_reason(
                action=action,
                sentiment=sentiment,
                confidence=confidence,
                score=score,
                risk=risk,
                conflicts=conflicts
            )

            # ------------------------------------------------
            # Evidence
            # ------------------------------------------------

            evidence = self.collect_evidence(
                data=data,
                analysis=analysis,
                prediction=prediction,
                semantic=semantic,
                insight=insight,
                reasoning=reasoning
            )

            # ------------------------------------------------
            # Decision object
            # ------------------------------------------------

            timestamp = datetime.now().isoformat()

            decision_id = (
                f"DEC-{self.decisions + 1:06d}"
            )

            result = {

                "id":
                    decision_id,

                "timestamp":
                    timestamp,

                "action":
                    action,

                "confidence":
                    round(
                        confidence,
                        2
                    ),

                "score":
                    round(
                        score,
                        2
                    ),

                "sentiment":
                    sentiment,

                "risk":
                    risk,

                "conflicts":
                    conflicts,

                "evidence":
                    evidence,

                "reason":
                    reason,

                "thresholds": {

                    "buy":
                        self.buy_threshold,

                    "sell":
                        self.sell_threshold,

                    "minimum_confidence":
                        self.min_confidence

                },

                "context":
                    context

            }

            # ------------------------------------------------
            # Store decision
            # ------------------------------------------------

            self.decisions += 1

            self.action_counts[action] = (
                self.action_counts.get(
                    action,
                    0
                ) + 1
            )

            self.confidence_history.append(
                confidence
            )

            self.score_history.append(
                score
            )

            self.history.append(
                result
            )

            self._trim_history()

            # ------------------------------------------------
            # Backward-compatible output
            # ------------------------------------------------

            data["decision"] = result

            return data

        except Exception as e:

            logger.exception(
                "Decision failed: %s",
                e
            )

            return data

    # ========================================================
    #
    # CONFIDENCE EXTRACTION
    #
    # ========================================================

    def extract_confidence(
        self,
        analysis=None,
        prediction=None,
        insight=None,
        reasoning=None
    ):

        values = []

        sources = [
            analysis,
            prediction,
            insight,
            reasoning
        ]

        for source in sources:

            if not isinstance(
                source,
                dict
            ):
                continue

            value = source.get(
                "confidence"
            )

            if value is None:

                value = source.get(
                    "score"
                )

            if isinstance(
                value,
                (int, float)
            ):

                values.append(
                    self.normalize_confidence(
                        value
                    )
                )

        if not values:

            return 0.0

        return round(
            mean(values),
            2
        )

    # ========================================================
    #
    # NORMALIZE CONFIDENCE
    #
    # ========================================================

    def normalize_confidence(
        self,
        value
    ):

        try:

            value = float(
                value
            )

            # Support 0.0 - 1.0
            if 0 <= value <= 1:

                value *= 100

            return max(
                0.0,
                min(
                    value,
                    100.0
                )
            )

        except (
            TypeError,
            ValueError
        ):

            return 0.0

    # ========================================================
    #
    # NORMALIZE SENTIMENT
    #
    # ========================================================

    def normalize_sentiment(
        self,
        sentiment
    ):

        if sentiment is None:

            return "neutral"

        sentiment = str(
            sentiment
        ).strip().lower()

        mapping = {

            "bullish":
                "positive",

            "buy":
                "positive",

            "positive":
                "positive",

            "bearish":
                "negative",

            "sell":
                "negative",

            "negative":
                "negative",

            "neutral":
                "neutral",

            "hold":
                "neutral"

        }

        return mapping.get(
            sentiment,
            "neutral"
        )

    # ========================================================
    #
    # SCORE CALCULATION
    #
    # ========================================================

    def calculate_score(
        self,
        sentiment,
        confidence,
        analysis=None,
        prediction=None,
        semantic=None,
        insight=None,
        reasoning=None
    ):

        score = 50.0

        # ------------------------------------------------
        # Sentiment contribution
        # ------------------------------------------------

        if sentiment == "positive":

            score += 25

        elif sentiment == "negative":

            score -= 25

        # ------------------------------------------------
        # Confidence contribution
        # ------------------------------------------------

        confidence_factor = (
            confidence - 50
        ) * 0.5

        if sentiment == "positive":

            score += confidence_factor

        elif sentiment == "negative":

            score -= confidence_factor

        # ------------------------------------------------
        # Prediction contribution
        # ------------------------------------------------

        prediction_value = ""

        if isinstance(
            prediction,
            dict
        ):

            prediction_value = str(
                prediction.get(
                    "prediction",
                    prediction.get(
                        "signal",
                        ""
                    )
                )
            ).lower()

        if prediction_value in (
            "bullish",
            "buy",
            "positive"
        ):

            score += 10

        elif prediction_value in (
            "bearish",
            "sell",
            "negative"
        ):

            score -= 10

        # ------------------------------------------------
        # Analysis signal
        # ------------------------------------------------

        if isinstance(
            analysis,
            dict
        ):

            signal = str(
                analysis.get(
                    "signal",
                    ""
                )
            ).lower()

            if signal in (
                "bullish",
                "buy",
                "positive"
            ):

                score += 10

            elif signal in (
                "bearish",
                "sell",
                "negative"
            ):

                score -= 10

        return max(
            0.0,
            min(
                score,
                100.0
            )
        )

    # ========================================================
    #
    # CONFLICT DETECTION
    #
    # ========================================================

    def detect_conflicts(
        self,
        analysis=None,
        prediction=None,
        semantic=None,
        reasoning=None
    ):

        signals = []

        sources = [
            analysis,
            prediction,
            semantic,
            reasoning
        ]

        for source in sources:

            if not isinstance(
                source,
                dict
            ):
                continue

            values = [

                source.get(
                    "sentiment"
                ),

                source.get(
                    "signal"
                ),

                source.get(
                    "prediction"
                ),

                source.get(
                    "direction"
                )

            ]

            for value in values:

                if value is None:
                    continue

                normalized = self.normalize_sentiment(
                    value
                )

                if normalized in (
                    "positive",
                    "negative"
                ):

                    signals.append(
                        normalized
                    )

        unique = set(
            signals
        )

        return {
            "detected":
                len(unique) > 1,

            "count":
                len(signals),

            "types":
                list(unique)
        }

    # ========================================================
    #
    # RISK CALCULATION
    #
    # ========================================================

    def calculate_risk(
        self,
        confidence,
        score,
        sentiment,
        conflicts
    ):

        risk_score = 0.0

        # Low confidence = higher risk

        risk_score += (
            100 - confidence
        ) * 0.5

        # Weak score = higher risk

        distance = abs(
            score - 50
        )

        risk_score += (
            50 - min(
                distance,
                50
            )
        ) * 0.5

        # Neutral decisions are less decisive

        if sentiment == "neutral":

            risk_score += 10

        # Conflicting intelligence

        if conflicts.get(
            "detected",
            False
        ):

            risk_score += 20

        if risk_score >= 70:

            return "HIGH"

        if risk_score >= 40:

            return "MEDIUM"

        return "LOW"

    # ========================================================
    #
    # DETERMINE ACTION
    #
    # ========================================================

    def determine_action(
        self,
        score,
        confidence,
        sentiment,
        conflicts
    ):

        # Never act when confidence is too low.

        if confidence < self.min_confidence:

            return "HOLD"

        # Conflicting signals require caution.

        if conflicts.get(
            "detected",
            False
        ):

            if confidence < 80:

                return "HOLD"

        if (
            sentiment == "positive"
            and
            score >= self.buy_threshold
        ):

            return "BUY"

        if (
            sentiment == "negative"
            and
            (
                100 - score
            ) >= self.sell_threshold
        ):

            return "SELL"

        return "HOLD"

    # ========================================================
    #
    # REASON GENERATOR
    #
    # ========================================================

    def generate_reason(
        self,
        action,
        sentiment,
        confidence,
        score,
        risk,
        conflicts
    ):

        reasons = []

        if sentiment == "positive":

            reasons.append(
                "Positive market sentiment detected."
            )

        elif sentiment == "negative":

            reasons.append(
                "Negative market sentiment detected."
            )

        else:

            reasons.append(
                "Market sentiment is neutral."
            )

        reasons.append(
            f"Decision confidence is {confidence:.1f}%."
        )

        reasons.append(
            f"Decision score is {score:.1f}/100."
        )

        reasons.append(
            f"Risk level is {risk}."
        )

        if conflicts.get(
            "detected",
            False
        ):

            reasons.append(
                "Conflicting signals detected."
            )

        if action == "BUY":

            reasons.append(
                "Conditions meet the BUY threshold."
            )

        elif action == "SELL":

            reasons.append(
                "Conditions meet the SELL threshold."
            )

        else:

            reasons.append(
                "Conditions do not provide sufficient "
                "evidence for an active decision."
            )

        return " ".join(
            reasons
        )

    # ========================================================
    #
    # EVIDENCE COLLECTION
    #
    # ========================================================

    def collect_evidence(
        self,
        data,
        analysis,
        prediction,
        semantic,
        insight,
        reasoning
    ):

        evidence = []

        if isinstance(
            analysis,
            dict
        ):

            evidence.append({
                "source":
                    "analysis",

                "data":
                    analysis
            })

        if isinstance(
            prediction,
            dict
        ):

            evidence.append({
                "source":
                    "prediction",

                "data":
                    prediction
            })

        if isinstance(
            semantic,
            dict
        ):

            evidence.append({
                "source":
                    "semantic",

                "data":
                    semantic
            })

        if isinstance(
            insight,
            dict
        ):

            evidence.append({
                "source":
                    "insight",

                "data":
                    insight
            })

        if isinstance(
            reasoning,
            dict
        ):

            evidence.append({
                "source":
                    "reasoning",

                "data":
                    reasoning
            })

        return evidence

    # ========================================================
    #
    # HISTORY MANAGEMENT
    #
    # ========================================================

    def _trim_history(
        self
    ):

        if len(
            self.history
        ) > self.max_history:

            excess = (
                len(
                    self.history
                )
                -
                self.max_history
            )

            del self.history[
                :excess
            ]

    # ========================================================
    #
    # LATEST DECISION
    #
    # ========================================================

    def latest(
        self
    ):

        if not self.history:

            return None

        return self.history[-1]

    # ========================================================
    #
    # RECALL
    #
    # ========================================================

    def recall(
        self,
        limit=20
    ):

        if limit <= 0:

            return []

        return self.history[
            -limit:
        ]

    # ========================================================
    #
    # SEARCH
    #
    # ========================================================

    def search(
        self,
        action=None,
        sentiment=None,
        risk=None
    ):

        results = []

        for item in self.history:

            if (
                action is not None
                and
                item.get(
                    "action"
                ) != action
            ):

                continue

            if (
                sentiment is not None
                and
                item.get(
                    "sentiment"
                ) != sentiment
            ):

                continue

            if (
                risk is not None
                and
                item.get(
                    "risk"
                ) != risk
            ):

                continue

            results.append(
                item
            )

        return results

    # ========================================================
    #
    # STATISTICS
    #
    # ========================================================

    def statistics(
        self
    ):

        average_confidence = 0

        average_score = 0

        if self.confidence_history:

            average_confidence = round(
                mean(
                    self.confidence_history
                ),
                2
            )

        if self.score_history:

            average_score = round(
                mean(
                    self.score_history
                ),
                2
            )

        return {

            "decisions":
                self.decisions,

            "actions":
                dict(
                    self.action_counts
                ),

            "average_confidence":
                average_confidence,

            "average_score":
                average_score,

            "history":
                len(
                    self.history
                )

        }

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self
    ):

        self.decisions = 0

        self.history.clear()

        self.confidence_history.clear()

        self.score_history.clear()

        self.action_counts = {

            "BUY":
                0,

            "SELL":
                0,

            "HOLD":
                0

        }

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
                "decision",

            "online":
                True,

            "decisions":
                self.decisions,

            "history":
                len(
                    self.history
                ),

            "max_history":
                self.max_history,

            "buy_threshold":
                self.buy_threshold,

            "sell_threshold":
                self.sell_threshold,

            "minimum_confidence":
                self.min_confidence,

            "actions":
                dict(
                    self.action_counts
                ),

            "average_confidence":
                (
                    round(
                        mean(
                            self.confidence_history
                        ),
                        2
                    )
                    if self.confidence_history
                    else 0
                ),

            "average_score":
                (
                    round(
                        mean(
                            self.score_history
                        ),
                        2
                    )
                    if self.score_history
                    else 0
                )

        }

    # ========================================================
    #
    # UTILITY
    #
    # ========================================================

    @staticmethod
    def _get_dict(
        value
    ):

        if isinstance(
            value,
            dict
        ):

            return value

        return {}


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

decision_engine = DecisionEngine()


# ============================================================
#
# PUBLIC API
#
# ============================================================

__all__ = [
    "DecisionEngine",
    "decision_engine",
]


# ============================================================
#
# END
#
# ============================================================