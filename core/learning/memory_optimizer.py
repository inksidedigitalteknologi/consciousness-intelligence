# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# MEMORY OPTIMIZER ENGINE
#
# Version: 2.0
#
# Responsibilities:
# - Memory importance scoring
# - Recency scoring
# - Confidence scoring
# - Learning value detection
# - Success / failure detection
# - Domain weighting
# - Duplicate detection
# - Memory ranking
# - Memory optimization
# - Memory compression
# - Memory statistics
# - Memory filtering
# - Memory retention
#
# ============================================================

import logging
import hashlib
import math

from datetime import datetime, timezone


logger = logging.getLogger(__name__)


# ============================================================
#
# CONFIGURATION
#
# ============================================================

DEFAULT_KEEP = 1000

MAX_HISTORY = 100

RECENCY_DECAY_DAYS = 30

DUPLICATE_THRESHOLD = 0.95


# ============================================================
#
# MEMORY OPTIMIZER
#
# ============================================================

class MemoryOptimizer:

    def __init__(
        self,
        default_keep=DEFAULT_KEEP,
        recency_decay_days=RECENCY_DECAY_DAYS
    ):

        self.default_keep = max(
            1,
            int(default_keep)
        )

        self.recency_decay_days = max(
            1,
            int(recency_decay_days)
        )

        self.optimizations = 0

        self.items_processed = 0

        self.items_removed = 0

        self.duplicates_removed = 0

        self.compressions = 0

        self.history = []

        self.last_result = None

        logger.info(
            "Memory Optimizer initialized."
        )


    # ========================================================
    #
    # BASIC TEXT EXTRACTION
    #
    # ========================================================

    def _text(self, item):

        if item is None:
            return ""

        if isinstance(item, str):
            return item.lower()

        try:
            return str(item).lower()

        except Exception:

            return ""


    # ========================================================
    #
    # NUMERIC NORMALIZATION
    #
    # ========================================================

    def _number(
        self,
        value,
        default=0.0
    ):

        try:

            if isinstance(
                value,
                bool
            ):

                return (
                    1.0
                    if value
                    else 0.0
                )

            return float(value)

        except (
            TypeError,
            ValueError
        ):

            return default


    # ========================================================
    #
    # CONFIDENCE EXTRACTION
    #
    # ========================================================

    def _confidence(
        self,
        item
    ):

        if not isinstance(
            item,
            dict
        ):

            return 0.0

        candidates = [

            item.get(
                "confidence"
            ),

            item.get(
                "score"
            ),

            item.get(
                "importance"
            ),

            item.get(
                "analysis",
                {}
            ).get(
                "confidence"
            )
            if isinstance(
                item.get(
                    "analysis",
                    {}
                ),
                dict
            )
            else None

        ]

        for value in candidates:

            if value is None:
                continue

            value = self._number(
                value
            )

            if value > 1:

                value /= 100.0

            return max(
                0.0,
                min(
                    1.0,
                    value
                )
            )

        return 0.0


    # ========================================================
    #
    # RECENCY SCORE
    #
    # ========================================================

    def recency_score(
        self,
        item
    ):

        if not isinstance(
            item,
            dict
        ):

            return 0.0

        timestamp = (

            item.get(
                "timestamp"
            )

            or

            item.get(
                "time"
            )

            or

            item.get(
                "created_at"
            )

        )

        if not timestamp:

            return 0.5

        try:

            timestamp = str(
                timestamp
            ).replace(
                "Z",
                "+00:00"
            )

            dt = datetime.fromisoformat(
                timestamp
            )

            if dt.tzinfo is None:

                dt = dt.replace(
                    tzinfo=timezone.utc
                )

            now = datetime.now(
                timezone.utc
            )

            age = (
                now - dt
            ).total_seconds()

            if age < 0:
                age = 0

            days = (
                age / 86400.0
            )

            score = math.exp(
                -days
                /
                self.recency_decay_days
            )

            return max(
                0.0,
                min(
                    1.0,
                    score
                )
            )

        except Exception:

            return 0.5


    # ========================================================
    #
    # IMPORTANCE SCORE
    #
    # ========================================================

    def importance_score(
        self,
        item
    ):

        if not isinstance(
            item,
            dict
        ):

            return 0.0

        importance = self._number(
            item.get(
                "importance"
            )
        )

        if importance > 1:

            importance /= 100.0

        return max(
            0.0,
            min(
                1.0,
                importance
            )
        )


    # ========================================================
    #
    # KEYWORD SCORE
    #
    # ========================================================

    def keyword_score(
        self,
        item
    ):

        text = self._text(
            item
        )

        important = {

            "success": 2.0,

            "successful": 2.0,

            "pattern": 1.5,

            "prediction": 1.5,

            "knowledge": 1.5,

            "insight": 2.0,

            "learning": 2.0,

            "lesson": 2.0,

            "important": 2.0,

            "confirmed": 1.5,

            "correct": 1.5,

            "breakthrough": 3.0,

            "discovery": 2.5,

            "association": 1.5,

            "behavior": 1.5,

            "strategy": 1.5,

            "experience": 1.5,

            "reflection": 1.5,

            "adaptation": 1.5,

            "evolution": 2.0,

            "failure": 1.0,

            "wrong": 1.0,

        }

        score = 0.0

        for word, weight in important.items():

            if word in text:

                score += weight

        return score


    # ========================================================
    #
    # LEARNING VALUE
    #
    # ========================================================

    def learning_score(
        self,
        item
    ):

        text = self._text(
            item
        )

        score = 0.0

        learning_terms = [

            "learning",
            "lesson",
            "insight",
            "knowledge",
            "experience",
            "reflection",
            "pattern",
            "adaptation",
            "prediction",
            "evaluation"

        ]

        for term in learning_terms:

            if term in text:

                score += 1.0

        return min(
            score / 5.0,
            1.0
        )


    # ========================================================
    #
    # SUCCESS SCORE
    #
    # ========================================================

    def success_score(
        self,
        item
    ):

        text = self._text(
            item
        )

        positive = [

            "success",
            "successful",
            "correct",
            "confirmed",
            "profit",
            "profitable",
            "validated",
            "improved",
            "positive"

        ]

        negative = [

            "failure",
            "failed",
            "wrong",
            "incorrect",
            "loss",
            "negative"

        ]

        positive_hits = sum(
            1
            for word in positive
            if word in text
        )

        negative_hits = sum(
            1
            for word in negative
            if word in text
        )

        total = (
            positive_hits
            +
            negative_hits
        )

        if total == 0:

            return 0.5

        return (
            positive_hits
            /
            total
        )


    # ========================================================
    #
    # DOMAIN VALUE
    #
    # ========================================================

    def domain_score(
        self,
        item
    ):

        text = self._text(
            item
        )

        domains = {

            "trading": 1.0,

            "market": 1.0,

            "knowledge": 0.9,

            "reasoning": 0.9,

            "science": 0.9,

            "semantic": 0.8,

            "entity": 0.8,

            "behavior": 0.8,

            "association": 0.8,

            "evolution": 1.0,

        }

        score = 0.5

        for domain, value in domains.items():

            if domain in text:

                score = max(
                    score,
                    value
                )

        return score


    # ========================================================
    #
    # FREQUENCY SCORE
    #
    # ========================================================

    def frequency_score(
        self,
        item
    ):

        if not isinstance(
            item,
            dict
        ):

            return 0.0

        frequency = (

            item.get(
                "frequency"
            )

            or

            item.get(
                "count"
            )

            or

            item.get(
                "occurrences"
            )

        )

        frequency = self._number(
            frequency
        )

        if frequency <= 0:

            return 0.0

        return min(
            math.log1p(
                frequency
            )
            /
            math.log1p(
                100
            ),
            1.0
        )


    # ========================================================
    #
    # COMPOSITE SCORE
    #
    # ========================================================

    def score(
        self,
        item
    ):

        """
        Calculate overall memory value.

        Higher score means the memory
        is more valuable to retain.
        """

        keyword = self.keyword_score(
            item
        )

        keyword_normalized = min(
            keyword / 10.0,
            1.0
        )

        importance = self.importance_score(
            item
        )

        recency = self.recency_score(
            item
        )

        confidence = self._confidence(
            item
        )

        learning = self.learning_score(
            item
        )

        success = self.success_score(
            item
        )

        domain = self.domain_score(
            item
        )

        frequency = self.frequency_score(
            item
        )

        composite = (

            keyword_normalized * 0.15

            +

            importance * 0.15

            +

            recency * 0.15

            +

            confidence * 0.15

            +

            learning * 0.15

            +

            success * 0.10

            +

            domain * 0.10

            +

            frequency * 0.05

        )

        return round(
            composite * 100,
            4
        )


    # ========================================================
    #
    # MEMORY FINGERPRINT
    #
    # ========================================================

    def fingerprint(
        self,
        item
    ):

        try:

            if isinstance(
                item,
                dict
            ):

                normalized = {

                    key: value

                    for key, value
                    in sorted(
                        item.items()
                    )

                    if key not in {

                        "time",
                        "timestamp",
                        "created_at"

                    }

                }

                text = repr(
                    normalized
                )

            else:

                text = repr(
                    item
                )

            return hashlib.sha256(
                text.encode(
                    "utf-8",
                    errors="ignore"
                )
            ).hexdigest()

        except Exception:

            return hashlib.sha256(
                str(item).encode(
                    "utf-8",
                    errors="ignore"
                )
            ).hexdigest()


    # ========================================================
    #
    # DUPLICATE REMOVAL
    #
    # ========================================================

    def remove_duplicates(
        self,
        memory_list
    ):

        unique = []

        fingerprints = set()

        duplicates = 0

        for item in memory_list:

            fingerprint = self.fingerprint(
                item
            )

            if fingerprint in fingerprints:

                duplicates += 1

                continue

            fingerprints.add(
                fingerprint
            )

            unique.append(
                item
            )

        self.duplicates_removed += (
            duplicates
        )

        return unique


    # ========================================================
    #
    # RANK MEMORY
    #
    # ========================================================

    def rank(
        self,
        memory_list
    ):

        if not memory_list:

            return []

        try:

            ranked = sorted(

                memory_list,

                key=self.score,

                reverse=True

            )

            return ranked

        except Exception as e:

            logger.exception(
                "Memory ranking failed: %s",
                e
            )

            return []


    # ========================================================
    #
    # OPTIMIZE MEMORY
    #
    # ========================================================

    def optimize(
        self,
        memory_list,
        keep=None
    ):

        try:

            if memory_list is None:

                return []

            if keep is None:

                keep = self.default_keep

            keep = max(
                1,
                int(keep)
            )

            original_count = len(
                memory_list
            )

            self.items_processed += (
                original_count
            )

            cleaned = self.remove_duplicates(
                memory_list
            )

            ranked = self.rank(
                cleaned
            )

            optimized = ranked[
                :keep
            ]

            removed = (
                original_count
                -
                len(optimized)
            )

            self.items_removed += (
                max(
                    0,
                    removed
                )
            )

            self.optimizations += 1

            result = {

                "timestamp":
                    datetime.now().isoformat(),

                "original":
                    original_count,

                "unique":
                    len(cleaned),

                "kept":
                    len(optimized),

                "removed":
                    max(
                        0,
                        removed
                    ),

                "duplicates_removed":
                    original_count
                    -
                    len(cleaned),

                "optimization":
                    self.optimizations

            }

            self.last_result = result

            self.history.append(
                result
            )

            if len(
                self.history
            ) > MAX_HISTORY:

                self.history.pop(0)

            return optimized

        except Exception as e:

            logger.exception(
                "Memory optimization failed: %s",
                e
            )

            return []


    # ========================================================
    #
    # COMPRESS MEMORY
    #
    # ========================================================

    def compress(
        self,
        memory_list,
        keep=None
    ):

        """
        Optimize memory while retaining
        high-value information.

        This does not destroy the original
        input list.
        """

        result = self.optimize(
            memory_list,
            keep=keep
        )

        self.compressions += 1

        return result


    # ========================================================
    #
    # FILTER BY SCORE
    #
    # ========================================================

    def filter_by_score(
        self,
        memory_list,
        minimum_score=25
    ):

        result = []

        threshold = self._number(
            minimum_score,
            25
        )

        for item in memory_list or []:

            if self.score(
                item
            ) >= threshold:

                result.append(
                    item
                )

        return result


    # ========================================================
    #
    # TOP MEMORY
    # ========================================================

    def top(
        self,
        memory_list,
        limit=10
    ):

        limit = max(
            1,
            int(limit)
        )

        return self.rank(
            memory_list
        )[:limit]


    # ========================================================
    #
    # MEMORY ANALYSIS
    # ========================================================

    def analyze(
        self,
        memory_list
    ):

        memories = (
            memory_list
            or []
        )

        if not memories:

            return {

                "total":
                    0,

                "average_score":
                    0,

                "highest_score":
                    0,

                "lowest_score":
                    0

            }

        scores = [

            self.score(
                item
            )

            for item in memories

        ]

        return {

            "total":
                len(memories),

            "average_score":
                round(
                    sum(scores)
                    /
                    len(scores),
                    4
                ),

            "highest_score":
                max(scores),

            "lowest_score":
                min(scores),

            "high_value":
                sum(
                    1
                    for value in scores
                    if value >= 70
                ),

            "medium_value":
                sum(
                    1
                    for value in scores
                    if 40 <= value < 70
                ),

            "low_value":
                sum(
                    1
                    for value in scores
                    if value < 40
                )

        }


    # ========================================================
    #
    # MEMORY RETENTION DECISION
    #
    # ========================================================

    def should_retain(
        self,
        item,
        threshold=40
    ):

        return (
            self.score(
                item
            )
            >=
            float(threshold)
        )


    # ========================================================
    #
    # OPTIMIZATION HISTORY
    #
    # ========================================================

    def get_history(
        self,
        limit=20
    ):

        limit = max(
            1,
            int(limit)
        )

        return self.history[
            -limit:
        ]


    # ========================================================
    #
    # LAST OPTIMIZATION
    #
    # ========================================================

    def last_optimization(
        self
    ):

        return self.last_result


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
                "memory_optimizer",

            "optimizations":
                self.optimizations,

            "optimization_count":
                self.optimizations,

            "items_processed":
                self.items_processed,

            "items_removed":
                self.items_removed,

            "duplicates_removed":
                self.duplicates_removed,

            "compressions":
                self.compressions,

            "history":
                len(
                    self.history
                ),

            "default_keep":
                self.default_keep,

            "recency_decay_days":
                self.recency_decay_days

        }


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

memory_optimizer = MemoryOptimizer()