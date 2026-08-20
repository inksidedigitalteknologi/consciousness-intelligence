# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# GENERAL EVALUATOR ENGINE
# VERSION 2.1
#
# MULTI-DOMAIN EVALUATION + FEEDBACK LAYER
#
# ============================================================
#
# DESIGN GOALS
# ------------------------------------------------------------
# 1. General-purpose evaluation
# 2. Trading compatible
# 3. General knowledge compatible
# 4. Prediction evaluation
# 5. Classification evaluation
# 6. Boolean evaluation
# 7. Numeric evaluation
# 8. Text evaluation
# 9. Structured evaluation
# 10. Confidence-aware evaluation
# 11. Feedback-aware evaluation
# 12. Domain statistics
# 13. Historical evaluation
# 14. Numeric tolerance
# 15. Confidence calibration
# 16. Adaptive-learning ready
# 17. Serializable output
# 18. Thread-safe
# 19. Safe execution
# 20. Domain agnostic
#
# IMPORTANT
# ------------------------------------------------------------
# This module MUST NOT contain:
#
# - trading strategy
# - buy/sell logic
# - market logic
# - pattern logic
# - prediction generation
# - knowledge generation
#
# This module ONLY evaluates:
#
# prediction/result
# against
# reality/expected answer
#
# ============================================================

import logging
import math
import re
import threading

from datetime import datetime
from typing import Any, Dict, Optional


logger = logging.getLogger(__name__)


# ============================================================
# METADATA
# ============================================================

MODULE_NAME = "evaluator"
MODULE_VERSION = "2.1"
API_VERSION = "1.0"

EVALUATOR_NAME = "General Evaluation Engine"
EVALUATOR_VERSION = MODULE_VERSION


# ============================================================
# EVALUATOR ENGINE
# ============================================================

class EvaluatorEngine:

    """
    General-purpose evaluation engine.

    Works across multiple intelligence domains.

    Examples
    --------

    Trading:

        evaluator.evaluate(
            "bullish",
            "bullish",
            domain="trading"
        )

    Knowledge:

        evaluator.evaluate(
            "Paris",
            "Paris",
            domain="knowledge"
        )

    Numeric:

        evaluator.evaluate(
            102,
            100,
            domain="numeric"
        )

    Boolean:

        evaluator.evaluate(
            True,
            False,
            domain="reasoning"
        )

    Confidence:

        evaluator.evaluate(
            {
                "value": "bullish",
                "confidence": 85
            },
            "bullish",
            domain="trading"
        )

    The evaluator does NOT generate predictions.
    It only evaluates an existing result.
    """

    # ========================================================
    # INIT
    # ========================================================

    def __init__(
        self,
        max_history: int = 1000,
    ):

        self.correct = 0
        self.wrong = 0
        self.partial = 0

        self.total = 0

        self.total_score = 0.0

        self.total_confidence = 0.0
        self.confidence_samples = 0

        self.domains: Dict[str, Dict[str, Any]] = {}

        self.types: Dict[str, Dict[str, Any]] = {}

        self.history = []

        self.max_history = max(
            1,
            int(max_history)
        )

        self.last_evaluation = None

        self._lock = threading.RLock()

        logger.info(
            "%s %s initialized.",
            EVALUATOR_NAME,
            EVALUATOR_VERSION,
        )

    # ========================================================
    # NORMALIZE VALUE
    # ========================================================

    def _normalize(
        self,
        value: Any,
    ) -> Any:

        """
        Normalize values for safe comparison.
        """

        if isinstance(value, str):

            return value.strip().lower()

        if isinstance(value, bool):

            return value

        if isinstance(value, (int, float)):

            return value

        if isinstance(value, dict):

            normalized = {}

            for key, item in value.items():

                normalized[
                    str(key).strip().lower()
                ] = self._normalize(item)

            return normalized

        if isinstance(value, (list, tuple, set)):

            return [
                self._normalize(item)
                for item in value
            ]

        return value

    # ========================================================
    # DOMAIN DETECTION
    # ========================================================

    def _detect_domain(
        self,
        domain: Optional[str],
        context: Optional[Dict[str, Any]],
    ) -> str:

        if domain:

            return str(
                domain
            ).strip().lower()

        if isinstance(context, dict):

            detected = context.get(
                "domain"
            )

            if detected:

                return str(
                    detected
                ).strip().lower()

        return "general"

    # ========================================================
    # TYPE DETECTION
    # ========================================================

    def _detect_type(
        self,
        prediction: Any,
        reality: Any,
    ) -> str:

        if (
            isinstance(prediction, bool)
            and
            isinstance(reality, bool)
        ):

            return "boolean"

        if (
            isinstance(prediction, (int, float))
            and
            not isinstance(prediction, bool)
            and
            isinstance(reality, (int, float))
            and
            not isinstance(reality, bool)
        ):

            return "numeric"

        if (
            isinstance(prediction, str)
            and
            isinstance(reality, str)
        ):

            return "text"

        if (
            isinstance(prediction, dict)
            or
            isinstance(reality, dict)
        ):

            return "structured"

        if (
            isinstance(prediction, (list, tuple, set))
            or
            isinstance(reality, (list, tuple, set))
        ):

            return "collection"

        return "general"

    # ========================================================
    # TEXT TOKENIZATION
    # ========================================================

    def _tokens(
        self,
        value: str,
    ):

        return set(
            re.findall(
                r"\b\w+\b",
                value.lower(),
            )
        )

    # ========================================================
    # TEXT COMPARISON
    # ========================================================

    def _compare_text(
        self,
        prediction: str,
        reality: str,
    ) -> Dict[str, Any]:

        p = self._normalize(
            prediction
        )

        r = self._normalize(
            reality
        )

        exact = p == r

        p_tokens = self._tokens(p)
        r_tokens = self._tokens(r)

        if not p_tokens and not r_tokens:

            similarity = 100.0

        elif not p_tokens or not r_tokens:

            similarity = 0.0

        else:

            intersection = (
                p_tokens
                &
                r_tokens
            )

            union = (
                p_tokens
                |
                r_tokens
            )

            similarity = (
                len(intersection)
                /
                len(union)
                *
                100
            )

        return {

            "exact": exact,

            "similarity": round(
                similarity,
                2
            ),

            "prediction_length": len(p),

            "reality_length": len(r),

        }

    # ========================================================
    # NUMERIC COMPARISON
    # ========================================================

    def _compare_numeric(
        self,
        prediction: float,
        reality: float,
        tolerance: Optional[float] = None,
        relative_tolerance: Optional[float] = None,
    ) -> Dict[str, Any]:

        prediction = float(
            prediction
        )

        reality = float(
            reality
        )

        if not (
            math.isfinite(prediction)
            and
            math.isfinite(reality)
        ):

            return {

                "exact": False,

                "valid": False,

                "score": 0.0,

            }

        error = (
            prediction
            -
            reality
        )

        absolute_error = abs(
            error
        )

        if reality != 0:

            percentage_error = (
                absolute_error
                /
                abs(reality)
                *
                100
            )

        else:

            percentage_error = (
                0.0
                if absolute_error == 0
                else 100.0
            )

        exact = (
            prediction == reality
        )

        tolerance_match = False

        if tolerance is not None:

            try:

                tolerance_value = abs(
                    float(tolerance)
                )

                tolerance_match = (
                    absolute_error
                    <=
                    tolerance_value
                )

            except Exception:

                tolerance_match = False

        relative_match = False

        if relative_tolerance is not None:

            try:

                relative_value = abs(
                    float(relative_tolerance)
                )

                relative_match = (
                    absolute_error
                    <=
                    abs(reality)
                    *
                    relative_value
                )

            except Exception:

                relative_match = False

        if exact or tolerance_match or relative_match:

            score = 100.0

        else:

            score = max(
                0.0,
                100.0
                -
                percentage_error
            )

        return {

            "valid": True,

            "prediction": prediction,

            "reality": reality,

            "error": round(
                error,
                6
            ),

            "absolute_error": round(
                absolute_error,
                6
            ),

            "percentage_error": round(
                percentage_error,
                4
            ),

            "tolerance": tolerance,

            "relative_tolerance": relative_tolerance,

            "tolerance_match": tolerance_match,

            "relative_tolerance_match": relative_match,

            "exact": exact,

            "score": round(
                score,
                2
            ),

        }

    # ========================================================
    # STRUCTURED COMPARISON
    # ========================================================

    def _compare_structured(
        self,
        prediction: Any,
        reality: Any,
    ) -> Dict[str, Any]:

        p = self._normalize(
            prediction
        )

        r = self._normalize(
            reality
        )

        if p == r:

            return {

                "exact": True,

                "score": 100.0,

                "matched_fields": 1,

                "total_fields": 1,

            }

        if (
            isinstance(p, dict)
            and
            isinstance(r, dict)
        ):

            keys = (
                set(p.keys())
                |
                set(r.keys())
            )

            if not keys:

                return {

                    "exact": True,

                    "score": 100.0,

                    "matched_fields": 0,

                    "total_fields": 0,

                }

            matched = 0

            details = {}

            for key in keys:

                exists_p = key in p
                exists_r = key in r

                if exists_p and exists_r:

                    nested = self._compare_values(
                        p[key],
                        r[key],
                    )

                    field_score = nested.get(
                        "score",
                        0.0
                    )

                    if field_score >= 99.999:

                        matched += 1

                    details[key] = {

                        "score":
                            round(
                                field_score,
                                2
                            ),

                        "exact":
                            bool(
                                nested.get(
                                    "exact",
                                    False
                                )
                            ),

                    }

                else:

                    details[key] = {

                        "score": 0.0,

                        "exact": False,

                    }

            score = (
                matched
                /
                len(keys)
                *
                100
            )

            return {

                "exact": False,

                "matched_fields": matched,

                "total_fields": len(keys),

                "score": round(
                    score,
                    2
                ),

                "fields": details,

            }

        if (
            isinstance(p, (list, tuple))
            and
            isinstance(r, (list, tuple))
        ):

            if not p and not r:

                return {

                    "exact": True,

                    "score": 100.0,

                }

            if not p or not r:

                return {

                    "exact": False,

                    "score": 0.0,

                }

            max_length = max(
                len(p),
                len(r)
            )

            matches = 0

            comparisons = []

            for index in range(
                max_length
            ):

                if (
                    index < len(p)
                    and
                    index < len(r)
                ):

                    comparison = (
                        self._compare_values(
                            p[index],
                            r[index],
                        )
                    )

                    field_score = comparison.get(
                        "score",
                        0.0
                    )

                    if field_score >= 99.999:

                        matches += 1

                    comparisons.append(
                        round(
                            field_score,
                            2
                        )
                    )

                else:

                    comparisons.append(
                        0.0
                    )

            score = (
                matches
                /
                max_length
                *
                100
            )

            return {

                "exact": False,

                "matched_items": matches,

                "total_items": max_length,

                "score": round(
                    score,
                    2
                ),

                "items": comparisons,

            }

        return {

            "exact": False,

            "score": 0.0,

        }

    # ========================================================
    # GENERIC VALUE COMPARISON
    # ========================================================

    def _compare_values(
        self,
        prediction: Any,
        reality: Any,
        tolerance: Optional[float] = None,
        relative_tolerance: Optional[float] = None,
    ) -> Dict[str, Any]:

        evaluation_type = self._detect_type(
            prediction,
            reality,
        )

        if evaluation_type == "numeric":

            return self._compare_numeric(
                prediction,
                reality,
                tolerance=tolerance,
                relative_tolerance=relative_tolerance,
            )

        if evaluation_type == "text":

            result = self._compare_text(
                prediction,
                reality,
            )

            return {

                **result,

                "score":
                    100.0
                    if result["exact"]
                    else result["similarity"],

            }

        if evaluation_type == "boolean":

            exact = (
                prediction
                ==
                reality
            )

            return {

                "exact": exact,

                "score":
                    100.0
                    if exact
                    else 0.0,

            }

        if evaluation_type in (
            "structured",
            "collection",
        ):

            return self._compare_structured(
                prediction,
                reality,
            )

        exact = (
            self._normalize(prediction)
            ==
            self._normalize(reality)
        )

        return {

            "exact": exact,

            "score":
                100.0
                if exact
                else 0.0,

        }

    # ========================================================
    # CONFIDENCE EXTRACTION
    # ========================================================

    def _extract_confidence(
        self,
        prediction: Any,
    ) -> Optional[float]:

        if not isinstance(
            prediction,
            dict
        ):

            return None

        confidence = prediction.get(
            "confidence"
        )

        if confidence is None:

            confidence = prediction.get(
                "score"
            )

        if confidence is None:

            return None

        try:

            confidence = float(
                confidence
            )

        except Exception:

            return None

        if not math.isfinite(
            confidence
        ):

            return None

        if 0 <= confidence <= 1:

            confidence *= 100

        return max(
            0.0,
            min(
                100.0,
                confidence
            )
        )

    # ========================================================
    # EXTRACT PREDICTION VALUE
    # ========================================================

    def _extract_prediction_value(
        self,
        prediction: Any,
    ) -> Any:

        if not isinstance(
            prediction,
            dict
        ):

            return prediction

        for key in (
            "value",
            "prediction",
            "answer",
            "result",
            "output",
        ):

            if key in prediction:

                return prediction[key]

        return prediction

    # ========================================================
    # RESULT CLASSIFICATION
    # ========================================================

    def _classify_score(
        self,
        score: float,
    ) -> str:

        if score >= 99.999:

            return "correct"

        if score <= 0:

            return "wrong"

        return "partial"

    # ========================================================
    # UPDATE DOMAIN STATISTICS
    # ========================================================

    def _update_domain_stats(
        self,
        domain: str,
        result_status: str,
        score: float,
    ):

        if domain not in self.domains:

            self.domains[domain] = {

                "total": 0,

                "correct": 0,

                "wrong": 0,

                "partial": 0,

                "score_total": 0.0,

            }

        stats = self.domains[
            domain
        ]

        stats["total"] += 1

        stats[
            result_status
        ] += 1

        stats[
            "score_total"
        ] += score

    # ========================================================
    # UPDATE TYPE STATISTICS
    # ========================================================

    def _update_type_stats(
        self,
        evaluation_type: str,
        result_status: str,
        score: float,
    ):

        if evaluation_type not in self.types:

            self.types[
                evaluation_type
            ] = {

                "total": 0,

                "correct": 0,

                "wrong": 0,

                "partial": 0,

                "score_total": 0.0,

            }

        stats = self.types[
            evaluation_type
        ]

        stats["total"] += 1

        stats[
            result_status
        ] += 1

        stats[
            "score_total"
        ] += score

    # ========================================================
    # MAIN EVALUATE
    # ========================================================

    def evaluate(
        self,
        prediction: Any,
        reality: Any,
        domain: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        tolerance: Optional[float] = None,
        relative_tolerance: Optional[float] = None,
    ) -> Dict[str, Any]:

        """
        Evaluate a result against reality.

        This method is domain agnostic.

        Returns a serializable dictionary.
        """

        start = datetime.now()

        try:

            domain_name = self._detect_domain(
                domain,
                context,
            )

            prediction_value = (
                self._extract_prediction_value(
                    prediction
                )
            )

            normalized_prediction = (
                self._normalize(
                    prediction_value
                )
            )

            normalized_reality = (
                self._normalize(
                    reality
                )
            )

            evaluation_type = (
                self._detect_type(
                    normalized_prediction,
                    normalized_reality,
                )
            )

            comparison = self._compare_values(
                normalized_prediction,
                normalized_reality,
                tolerance=tolerance,
                relative_tolerance=relative_tolerance,
            )

            score = float(
                comparison.get(
                    "score",
                    0.0
                )
            )

            score = max(
                0.0,
                min(
                    100.0,
                    score
                )
            )

            result_status = (
                self._classify_score(
                    score
                )
            )

            confidence = (
                self._extract_confidence(
                    prediction
                )
            )

            with self._lock:

                self.total += 1

                self.total_score += score

                if result_status == "correct":

                    self.correct += 1

                elif result_status == "wrong":

                    self.wrong += 1

                else:

                    self.partial += 1

                if confidence is not None:

                    self.total_confidence += (
                        confidence
                    )

                    self.confidence_samples += 1

                self._update_domain_stats(
                    domain_name,
                    result_status,
                    score,
                )

                self._update_type_stats(
                    evaluation_type,
                    result_status,
                    score,
                )

                result = {

                    "timestamp":
                        start.isoformat(),

                    "engine":
                        EVALUATOR_NAME,

                    "version":
                        EVALUATOR_VERSION,

                    "domain":
                        domain_name,

                    "type":
                        evaluation_type,

                    "result":
                        result_status,

                    "score":
                        round(
                            score,
                            2
                        ),

                    "prediction":
                        prediction_value,

                    "reality":
                        reality,

                    "comparison":
                        comparison,

                    "confidence":
                        confidence,

                    "confidence_correct":
                        (
                            confidence is not None
                            and
                            result_status == "correct"
                        ),

                    "accuracy":
                        self.accuracy(),

                    "average_score":
                        self.average_score(),

                    "duration_ms":
                        round(
                            (
                                datetime.now()
                                -
                                start
                            ).total_seconds()
                            * 1000,
                            3,
                        ),

                }

                if context is not None:

                    result[
                        "context"
                    ] = context

                self.history.append(
                    result
                )

                if len(
                    self.history
                ) > self.max_history:

                    self.history = (
                        self.history[
                            -self.max_history:
                        ]
                    )

                self.last_evaluation = result

            return result

        except Exception as exc:

            logger.exception(
                "Evaluation failed: %s",
                exc,
            )

            return {

                "timestamp":
                    start.isoformat(),

                "engine":
                    EVALUATOR_NAME,

                "version":
                    EVALUATOR_VERSION,

                "domain":
                    self._detect_domain(
                        domain,
                        context,
                    ),

                "type":
                    "error",

                "result":
                    "error",

                "score":
                    0.0,

                "prediction":
                    prediction,

                "reality":
                    reality,

                "error":
                    str(exc),

            }

    # ========================================================
    # ACCURACY
    # ========================================================

    def accuracy(
        self,
    ) -> float:

        with self._lock:

            if self.total == 0:

                return 0.0

            return round(
                self.correct
                /
                self.total
                *
                100,
                2
            )

    # ========================================================
    # AVERAGE SCORE
    # ========================================================

    def average_score(
        self,
    ) -> float:

        with self._lock:

            if self.total == 0:

                return 0.0

            return round(
                self.total_score
                /
                self.total,
                2
            )

    # ========================================================
    # SUCCESS RATE
    # ========================================================

    def success_rate(
        self,
    ) -> float:

        with self._lock:

            if self.total == 0:

                return 0.0

            weighted = (
                self.correct
                +
                self.partial
                * 0.5
            )

            return round(
                weighted
                /
                self.total
                *
                100,
                2
            )

    # ========================================================
    # AVERAGE CONFIDENCE
    # ========================================================

    def average_confidence(
        self,
    ) -> float:

        with self._lock:

            if self.confidence_samples == 0:

                return 0.0

            return round(
                self.total_confidence
                /
                self.confidence_samples,
                2
            )

    # ========================================================
    # CONFIDENCE CALIBRATION
    # ========================================================

    def confidence_calibration(
        self,
    ) -> Dict[str, Any]:

        with self._lock:

            samples = [
                item
                for item in self.history
                if item.get(
                    "confidence"
                ) is not None
            ]

            if not samples:

                return {

                    "samples": 0,

                    "average_confidence": 0.0,

                    "accuracy": 0.0,

                    "calibration_error": 0.0,

                }

            average_confidence = (
                sum(
                    item[
                        "confidence"
                    ]
                    for item in samples
                )
                /
                len(samples)
            )

            successful = sum(
                1
                for item in samples
                if item.get(
                    "result"
                ) == "correct"
            )

            actual_accuracy = (
                successful
                /
                len(samples)
                *
                100
            )

            calibration_error = abs(
                average_confidence
                -
                actual_accuracy
            )

            return {

                "samples":
                    len(samples),

                "average_confidence":
                    round(
                        average_confidence,
                        2
                    ),

                "accuracy":
                    round(
                        actual_accuracy,
                        2
                    ),

                "calibration_error":
                    round(
                        calibration_error,
                        2
                    ),

            }

    # ========================================================
    # DOMAIN ACCURACY
    # ========================================================

    def domain_accuracy(
        self,
        domain: str,
    ) -> float:

        domain_name = (
            str(domain)
            .strip()
            .lower()
        )

        with self._lock:

            stats = self.domains.get(
                domain_name
            )

            if not stats:

                return 0.0

            total = stats[
                "total"
            ]

            if total == 0:

                return 0.0

            return round(
                stats["correct"]
                /
                total
                *
                100,
                2
            )

    # ========================================================
    # DOMAIN SCORE
    # ========================================================

    def domain_score(
        self,
        domain: str,
    ) -> float:

        domain_name = (
            str(domain)
            .strip()
            .lower()
        )

        with self._lock:

            stats = self.domains.get(
                domain_name
            )

            if not stats:

                return 0.0

            total = stats[
                "total"
            ]

            if total == 0:

                return 0.0

            return round(
                stats["score_total"]
                /
                total,
                2
            )

    # ========================================================
    # TYPE SCORE
    # ========================================================

    def type_score(
        self,
        evaluation_type: str,
    ) -> float:

        type_name = (
            str(evaluation_type)
            .strip()
            .lower()
        )

        with self._lock:

            stats = self.types.get(
                type_name
            )

            if not stats:

                return 0.0

            total = stats[
                "total"
            ]

            if total == 0:

                return 0.0

            return round(
                stats["score_total"]
                /
                total,
                2
            )

    # ========================================================
    # LAST RESULT
    # ========================================================

    def last(
        self,
    ):

        with self._lock:

            return self.last_evaluation

    # ========================================================
    # HISTORY
    # ========================================================

    def get_history(
        self,
        limit: Optional[int] = None,
    ):

        with self._lock:

            if limit is None:

                return list(
                    self.history
                )

            try:

                limit = int(
                    limit
                )

            except Exception:

                return list(
                    self.history
                )

            if limit <= 0:

                return []

            return list(
                self.history[
                    -limit:
                ]
            )

    # ========================================================
    # STATUS
    # ========================================================

    def status(
        self,
    ) -> Dict[str, Any]:

        with self._lock:

            domains = {}

            for name, stats in (
                self.domains.items()
            ):

                total = stats[
                    "total"
                ]

                domains[name] = {

                    **stats,

                    "accuracy":
                        (
                            round(
                                stats["correct"]
                                /
                                total
                                *
                                100,
                                2
                            )
                            if total
                            else 0.0
                        ),

                    "average_score":
                        (
                            round(
                                stats["score_total"]
                                /
                                total,
                                2
                            )
                            if total
                            else 0.0
                        ),

                }

            types = {}

            for name, stats in (
                self.types.items()
            ):

                total = stats[
                    "total"
                ]

                types[name] = {

                    **stats,

                    "accuracy":
                        (
                            round(
                                stats["correct"]
                                /
                                total
                                *
                                100,
                                2
                            )
                            if total
                            else 0.0
                        ),

                    "average_score":
                        (
                            round(
                                stats["score_total"]
                                /
                                total,
                                2
                            )
                            if total
                            else 0.0
                        ),

                }

            return {

                "engine":
                    EVALUATOR_NAME,

                "version":
                    EVALUATOR_VERSION,

                "online":
                    True,

                "total":
                    self.total,

                "correct":
                    self.correct,

                "wrong":
                    self.wrong,

                "partial":
                    self.partial,

                "accuracy":
                    self.accuracy(),

                "average_score":
                    self.average_score(),

                "success_rate":
                    self.success_rate(),

                "average_confidence":
                    self.average_confidence(),

                "confidence_calibration":
                    self.confidence_calibration(),

                "domains":
                    domains,

                "types":
                    types,

                "history":
                    len(
                        self.history
                    ),

                "last_evaluation":
                    self.last_evaluation,

            }

    # ========================================================
    # RESET
    # ========================================================

    def reset(
        self,
    ) -> bool:

        with self._lock:

            self.correct = 0

            self.wrong = 0

            self.partial = 0

            self.total = 0

            self.total_score = 0.0

            self.total_confidence = 0.0

            self.confidence_samples = 0

            self.domains.clear()

            self.types.clear()

            self.history.clear()

            self.last_evaluation = None

        logger.info(
            "Evaluator statistics reset."
        )

        return True


# ============================================================
# GLOBAL INSTANCE
# ============================================================

evaluator_engine = EvaluatorEngine()


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "MODULE_NAME",
    "MODULE_VERSION",
    "API_VERSION",
    "EVALUATOR_NAME",
    "EVALUATOR_VERSION",
    "EvaluatorEngine",
    "evaluator_engine",
]


# ============================================================
# END
# ============================================================