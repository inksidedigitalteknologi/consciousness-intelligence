# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# UNIVERSAL LEARNING ANALYZER
#
# Version: 2.0
#
# Purpose:
# Domain-agnostic intelligence analysis layer.
#
# Supported domains:
# - trading
# - knowledge
# - science
# - mathematics
# - reasoning
# - text
# - general
# - custom
#
# Responsibilities:
# - Input normalization
# - Domain detection
# - Entity extraction
# - Keyword extraction
# - Sentiment analysis
# - Numerical analysis
# - Pattern detection
# - Relationship detection
# - Anomaly detection
# - Novelty estimation
# - Temporal information detection
# - Semantic classification
# - Evidence aggregation
# - Confidence estimation
# - Conclusion generation
# - Analysis history
#
# ============================================================

import logging
import math
import re
import statistics

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


# ============================================================
#
# LEARNING ANALYZER
#
# ============================================================

class LearningAnalyzer:
    """
    Universal domain-agnostic analyzer.

    The analyzer does NOT assume that the incoming information
    belongs to trading.

    It attempts to understand the structure and characteristics
    of arbitrary information before producing an analysis result.
    """

    VERSION = "2.0"

    MAX_HISTORY = 500

    # ========================================================
    #
    # BASIC VOCABULARY
    #
    # ========================================================

    POSITIVE_WORDS = {
        "positive",
        "good",
        "great",
        "excellent",
        "strong",
        "success",
        "successful",
        "correct",
        "accurate",
        "profit",
        "profitable",
        "gain",
        "growth",
        "improved",
        "improvement",
        "stable",
        "healthy",
        "confirmed",
        "bullish",
        "winning",
        "win",
        "safe",
        "effective",
        "valid",
        "true",
    }

    NEGATIVE_WORDS = {
        "negative",
        "bad",
        "poor",
        "weak",
        "failure",
        "failed",
        "incorrect",
        "inaccurate",
        "loss",
        "lost",
        "decline",
        "decrease",
        "worse",
        "unstable",
        "danger",
        "dangerous",
        "invalid",
        "false",
        "bearish",
        "wrong",
        "error",
        "risk",
        "critical",
    }

    UNCERTAINTY_WORDS = {
        "maybe",
        "possibly",
        "possible",
        "perhaps",
        "likely",
        "unlikely",
        "uncertain",
        "unclear",
        "unknown",
        "might",
        "could",
        "potential",
        "probable",
        "probability",
        "estimate",
        "estimated",
        "assume",
        "assumption",
    }

    ACTION_WORDS = {
        "buy",
        "sell",
        "hold",
        "learn",
        "analyze",
        "predict",
        "evaluate",
        "compare",
        "calculate",
        "test",
        "verify",
        "check",
        "monitor",
        "update",
        "store",
        "remember",
        "observe",
        "detect",
        "classify",
        "decide",
    }

    # ========================================================
    #
    # DOMAIN KEYWORDS
    #
    # ========================================================

    DOMAIN_KEYWORDS = {
        "trading": {
            "market",
            "price",
            "volume",
            "candlestick",
            "breakout",
            "support",
            "resistance",
            "rsi",
            "macd",
            "ema",
            "sma",
            "atr",
            "crypto",
            "bitcoin",
            "btc",
            "ethereum",
            "eth",
            "bullish",
            "bearish",
            "buy",
            "sell",
            "stop",
            "profit",
            "trade",
            "trading",
        },

        "science": {
            "experiment",
            "hypothesis",
            "observation",
            "laboratory",
            "research",
            "theory",
            "measurement",
            "result",
            "chemical",
            "physics",
            "biology",
            "scientific",
            "variable",
            "control",
        },

        "mathematics": {
            "equation",
            "number",
            "calculate",
            "calculation",
            "formula",
            "algebra",
            "geometry",
            "integral",
            "derivative",
            "probability",
            "percentage",
            "ratio",
            "sum",
            "average",
            "mean",
            "median",
            "variance",
        },

        "knowledge": {
            "question",
            "answer",
            "fact",
            "history",
            "geography",
            "capital",
            "country",
            "definition",
            "information",
            "knowledge",
        },

        "reasoning": {
            "logic",
            "reason",
            "reasoning",
            "because",
            "therefore",
            "if",
            "then",
            "condition",
            "premise",
            "conclusion",
            "true",
            "false",
            "cause",
            "effect",
        },

        "text": {
            "text",
            "sentence",
            "paragraph",
            "document",
            "article",
            "message",
            "language",
            "word",
            "phrase",
            "statement",
        },
    }

    # ========================================================
    #
    # INITIALIZATION
    #
    # ========================================================

    def __init__(self):

        self.analysis_count = 0
        self.success_count = 0
        self.error_count = 0

        self.history: List[Dict[str, Any]] = []

        self.domain_counts: Counter = Counter()
        self.sentiment_counts: Counter = Counter()
        self.pattern_counts: Counter = Counter()

        self.total_entities = 0
        self.total_keywords = 0
        self.total_anomalies = 0
        self.total_novel = 0

        self.last_analysis: Optional[Dict[str, Any]] = None
        self.last_error: Optional[str] = None

        self.total_analysis_time_ms = 0.0

        logger.info(
            "Universal Learning Analyzer v%s initialized.",
            self.VERSION,
        )

    # ========================================================
    #
    # PUBLIC API
    #
    # ========================================================

    def analyze(
        self,
        data: Any,
    ) -> Dict[str, Any]:

        """
        Analyze arbitrary information.

        The method accepts dictionaries, lists, strings,
        numbers, booleans and generic Python objects.
        """

        started = datetime.now()

        try:

            normalized = self._normalize_input(data)

            domain = self._detect_domain(normalized)

            text = self._extract_text(normalized)

            features = self._extract_features(
                normalized,
                text,
            )

            analysis = self._build_analysis(
                normalized,
                domain,
                features,
            )

            result = {
                "timestamp": datetime.now().isoformat(),

                "analyzer":
                    "Universal Learning Analyzer",

                "version":
                    self.VERSION,

                "status":
                    "OK",

                "domain":
                    domain,

                "input_type":
                    self._detect_input_type(
                        normalized
                    ),

                "features":
                    features,

                "analysis":
                    analysis,
            }

            duration = (
                datetime.now() - started
            ).total_seconds() * 1000

            result["duration_ms"] = round(
                duration,
                3,
            )

            self._register_success(
                result
            )

            return result

        except Exception as exc:

            self.error_count += 1

            self.last_error = str(exc)

            logger.exception(
                "Universal analysis failed: %s",
                exc,
            )

            return {
                "timestamp":
                    datetime.now().isoformat(),

                "analyzer":
                    "Universal Learning Analyzer",

                "version":
                    self.VERSION,

                "domain":
                    "unknown",

                "status":
                    "ERROR",

                "error":
                    str(exc),

                "features":
                    {},

                "analysis":
                    {
                        "confidence":
                            0.0,

                        "summary":
                            "Analysis failed.",
                    },
            }

    # ========================================================
    #
    # NORMALIZATION
    #
    # ========================================================

    def _normalize_input(
        self,
        data: Any,
    ) -> Any:

        if data is None:
            return {}

        if isinstance(
            data,
            (
                dict,
                list,
                tuple,
                str,
                int,
                float,
                bool,
            ),
        ):
            return data

        try:
            return vars(data)

        except Exception:
            return str(data)

    # ========================================================
    #
    # INPUT TYPE
    #
    # ========================================================

    def _detect_input_type(
        self,
        data: Any,
    ) -> str:

        if isinstance(data, dict):
            return "dictionary"

        if isinstance(data, list):
            return "list"

        if isinstance(data, tuple):
            return "tuple"

        if isinstance(data, str):
            return "text"

        if isinstance(data, bool):
            return "boolean"

        if isinstance(data, (int, float)):
            return "numeric"

        return "object"

    # ========================================================
    #
    # DOMAIN DETECTION
    #
    # ========================================================

    def _detect_domain(
        self,
        data: Any,
    ) -> str:

        if isinstance(data, dict):

            explicit = (
                data.get("domain")
                or data.get("category")
                or data.get("context")
            )

            if isinstance(
                explicit,
                str,
            ):

                explicit_lower = (
                    explicit.lower().strip()
                )

                if explicit_lower in (
                    "trading",
                    "science",
                    "mathematics",
                    "knowledge",
                    "reasoning",
                    "text",
                    "general",
                    "custom",
                ):
                    return explicit_lower

        text = self._extract_text(
            data
        ).lower()

        scores: Dict[str, int] = {}

        for domain, words in (
            self.DOMAIN_KEYWORDS.items()
        ):

            score = 0

            for word in words:

                if re.search(
                    r"\b"
                    + re.escape(word)
                    + r"\b",
                    text,
                ):
                    score += 1

            scores[domain] = score

        if not scores:
            return "general"

        best_domain = max(
            scores,
            key=scores.get,
        )

        if scores[best_domain] <= 0:
            return "general"

        return best_domain

    # ========================================================
    #
    # TEXT EXTRACTION
    #
    # ========================================================

    def _extract_text(
        self,
        data: Any,
    ) -> str:

        parts: List[str] = []

        def walk(value: Any):

            if isinstance(
                value,
                dict,
            ):

                for key, item in (
                    value.items()
                ):

                    parts.append(
                        str(key)
                    )

                    walk(item)

            elif isinstance(
                value,
                (list, tuple, set),
            ):

                for item in value:
                    walk(item)

            else:

                if value is not None:

                    parts.append(
                        str(value)
                    )

        walk(data)

        return " ".join(parts)

    # ========================================================
    #
    # FEATURE EXTRACTION
    #
    # ========================================================

    def _extract_features(
        self,
        data: Any,
        text: str,
    ) -> Dict[str, Any]:

        tokens = self._tokenize(
            text
        )

        keywords = self._extract_keywords(
            tokens
        )

        entities = self._extract_entities(
            text
        )

        sentiment = self._analyze_sentiment(
            tokens
        )

        numbers = self._extract_numbers(
            text
        )

        temporal = self._extract_temporal(
            text
        )

        patterns = self._detect_patterns(
            data,
            text,
            tokens,
            numbers,
        )

        relationships = (
            self._detect_relationships(
                data
            )
        )

        anomalies = (
            self._detect_anomalies(
                numbers
            )
        )

        novelty = (
            self._estimate_novelty(
                text,
                keywords,
            )
        )

        semantic = (
            self._semantic_analysis(
                tokens
            )
        )

        return {

            "text": {
                "characters":
                    len(text),

                "tokens":
                    len(tokens),

                "unique_tokens":
                    len(set(tokens)),

                "documents":
                    self._estimate_documents(
                        data
                    ),
            },

            "keywords":
                keywords,

            "entities":
                entities,

            "sentiment":
                sentiment,

            "numerical":
                numbers,

            "temporal":
                temporal,

            "patterns":
                patterns,

            "relationships":
                relationships,

            "anomalies":
                anomalies,

            "novelty":
                novelty,

            "semantic":
                semantic,
        }

    # ========================================================
    #
    # TOKENIZATION
    #
    # ========================================================

    def _tokenize(
        self,
        text: str,
    ) -> List[str]:

        return re.findall(
            r"[A-Za-z0-9_./%-]+",
            text.lower(),
        )

    # ========================================================
    #
    # KEYWORDS
    #
    # ========================================================

    def _extract_keywords(
        self,
        tokens: List[str],
    ) -> List[Dict[str, Any]]:

        if not tokens:
            return []

        stopwords = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "is",
            "are",
            "was",
            "were",
            "to",
            "of",
            "in",
            "on",
            "for",
            "with",
            "this",
            "that",
            "it",
            "as",
            "by",
            "from",
            "be",
            "has",
            "have",
            "had",
        }

        counter = Counter(
            token
            for token in tokens
            if token not in stopwords
            and len(token) > 2
        )

        return [
            {
                "token": token,
                "frequency": count,
            }

            for token, count
            in counter.most_common(30)
        ]

    # ========================================================
    #
    # ENTITY EXTRACTION
    #
    # ========================================================

    def _extract_entities(
        self,
        text: str,
    ) -> List[Dict[str, Any]]:

        entities = []

        # Market symbols

        symbols = re.findall(
            r"\b[A-Z]{2,10}/[A-Z]{2,10}\b",
            text,
        )

        for symbol in symbols:

            entities.append(
                {
                    "type":
                        "market_symbol",

                    "value":
                        symbol,
                }
            )

        # URLs

        urls = re.findall(
            r"https?://[^\s]+",
            text,
        )

        for url in urls:

            entities.append(
                {
                    "type":
                        "url",

                    "value":
                        url,
                }
            )

        # Dates

        dates = re.findall(
            r"\b\d{4}-\d{2}-\d{2}\b",
            text,
        )

        for date in dates:

            entities.append(
                {
                    "type":
                        "date",

                    "value":
                        date,
                }
            )

        # Percentages

        percentages = re.findall(
            r"\b\d+(?:\.\d+)?%",
            text,
        )

        for value in percentages:

            entities.append(
                {
                    "type":
                        "percentage",

                    "value":
                        value,
                }
            )

        return entities

    # ========================================================
    #
    # SENTIMENT
    #
    # ========================================================

    def _analyze_sentiment(
        self,
        tokens: List[str],
    ) -> Dict[str, Any]:

        positive = sum(
            1
            for token in tokens
            if token in self.POSITIVE_WORDS
        )

        negative = sum(
            1
            for token in tokens
            if token in self.NEGATIVE_WORDS
        )

        uncertainty = sum(
            1
            for token in tokens
            if token in self.UNCERTAINTY_WORDS
        )

        if positive > negative:

            dominant = "positive"

        elif negative > positive:

            dominant = "negative"

        else:

            dominant = "neutral"

        total = positive + negative

        if total:

            polarity = (
                positive - negative
            ) / total

        else:

            polarity = 0.0

        return {

            "dominant":
                dominant,

            "positive":
                positive,

            "negative":
                negative,

            "uncertainty":
                uncertainty,

            "polarity":
                round(
                    polarity,
                    4,
                ),
        }

    # ========================================================
    #
    # NUMERICAL ANALYSIS
    #
    # ========================================================

    def _extract_numbers(
        self,
        text: str,
    ) -> Dict[str, Any]:

        raw = re.findall(
            r"(?<![A-Za-z])"
            r"-?\d+(?:\.\d+)?"
            r"(?![A-Za-z])",
            text,
        )

        values = []

        for value in raw:

            try:

                values.append(
                    float(value)
                )

            except Exception:
                pass

        if not values:

            return {
                "count": 0,
                "values": [],
                "mean": None,
                "minimum": None,
                "maximum": None,
                "range": None,
                "variance": None,
                "standard_deviation": None,
            }

        mean = statistics.mean(
            values
        )

        variance = (
            statistics.pvariance(
                values
            )
            if len(values) > 1
            else 0.0
        )

        return {

            "count":
                len(values),

            "values":
                values[:100],

            "mean":
                round(
                    mean,
                    6,
                ),

            "minimum":
                min(values),

            "maximum":
                max(values),

            "range":
                max(values)
                - min(values),

            "variance":
                round(
                    variance,
                    6,
                ),

            "standard_deviation":
                round(
                    math.sqrt(
                        variance
                    ),
                    6,
                ),
        }

    # ========================================================
    #
    # TEMPORAL INFORMATION
    #
    # ========================================================

    def _extract_temporal(
        self,
        text: str,
    ) -> Dict[str, Any]:

        timestamps = re.findall(
            r"\b\d{4}-\d{2}-\d{2}"
            r"(?:[T\s]\d{2}:\d{2}"
            r"(?::\d{2}(?:\.\d+)?)?)?",
            text,
        )

        temporal_words = []

        for word in (
            "today",
            "yesterday",
            "tomorrow",
            "daily",
            "weekly",
            "monthly",
            "yearly",
            "recent",
            "previous",
            "next",
            "before",
            "after",
            "during",
        ):

            if re.search(
                r"\b"
                + word
                + r"\b",
                text.lower(),
            ):

                temporal_words.append(
                    word
                )

        return {

            "count":
                len(timestamps),

            "timestamps":
                timestamps[:50],

            "temporal_terms":
                temporal_words,
        }

    # ========================================================
    #
    # PATTERN DETECTION
    #
    # ========================================================

    def _detect_patterns(
        self,
        data: Any,
        text: str,
        tokens: List[str],
        numbers: Dict[str, Any],
    ) -> Dict[str, Any]:

        patterns = []

        lower_text = text.lower()

        # Repetition

        counter = Counter(
            tokens
        )

        repeated = [
            {
                "value":
                    token,

                "count":
                    count,
            }

            for token, count
            in counter.items()

            if count >= 2
        ]

        if repeated:
            patterns.append(
                "repetition"
            )

        # Sequence

        values = numbers.get(
            "values",
            []
        )

        if len(values) >= 3:

            diffs = [
                round(
                    values[i + 1]
                    - values[i],
                    8,
                )

                for i in range(
                    len(values) - 1
                )
            ]

            if len(set(diffs)) == 1:

                patterns.append(
                    "arithmetic_sequence"
                )

        # Trading patterns

        trading_patterns = {

            "breakout":
                "breakout",

            "bullish":
                "bullish_bias",

            "bearish":
                "bearish_bias",

            "volume":
                "volume_activity",

            "support":
                "support_reference",

            "resistance":
                "resistance_reference",
        }

        for keyword, pattern_name in (
            trading_patterns.items()
        ):

            if re.search(
                r"\b"
                + keyword
                + r"\b",
                lower_text,
            ):

                patterns.append(
                    pattern_name
                )

        # Logical patterns

        if (
            "if" in tokens
            and "then" in tokens
        ):

            patterns.append(
                "conditional_reasoning"
            )

        if (
            "because" in tokens
            or "therefore" in tokens
        ):

            patterns.append(
                "causal_reasoning"
            )

        detected = list(
            dict.fromkeys(
                patterns
            )
        )

        return {

            "detected":
                detected,

            "count":
                len(detected),

            "repeated_values":
                repeated[:30],

            "sequence":
                self._sequence_summary(
                    values
                ),
        }

    # ========================================================
    #
    # SEQUENCE ANALYSIS
    #
    # ========================================================

    def _sequence_summary(
        self,
        values: List[float],
    ) -> Dict[str, Any]:

        if len(values) < 2:

            return {
                "detected": False
            }

        diffs = [
            values[i + 1]
            - values[i]

            for i in range(
                len(values) - 1
            )
        ]

        increasing = all(
            diffs[i] >= 0
            for i in range(
                len(diffs)
            )
        )

        decreasing = all(
            diffs[i] <= 0
            for i in range(
                len(diffs)
            )
        )

        return {

            "detected":
                True,

            "direction":
                (
                    "increasing"
                    if increasing
                    else
                    "decreasing"
                    if decreasing
                    else
                    "mixed"
                ),

            "differences":
                diffs[:50],
        }

    # ========================================================
    #
    # RELATIONSHIPS
    #
    # ========================================================

    def _detect_relationships(
        self,
        data: Any,
    ) -> Dict[str, Any]:

        relationships = []

        if isinstance(
            data,
            dict,
        ):

            keys = list(
                data.keys()
            )

            for i in range(
                len(keys)
            ):

                for j in range(
                    i + 1,
                    len(keys)
                ):

                    relationships.append(
                        {
                            "fields": [
                                keys[i],
                                keys[j],
                            ]
                        }
                    )

        return {

            "relationships":
                relationships[:100],

            "count":
                len(relationships),
        }

    # ========================================================
    #
    # ANOMALY DETECTION
    #
    # ========================================================

    def _detect_anomalies(
        self,
        numbers: Dict[str, Any],
    ) -> Dict[str, Any]:

        values = numbers.get(
            "values",
            []
        )

        if len(values) < 4:

            return {
                "detected": False,
                "count": 0,
                "values": [],
            }

        mean = statistics.mean(
            values
        )

        stdev = statistics.pstdev(
            values
        )

        if stdev == 0:

            return {
                "detected": False,
                "count": 0,
                "values": [],
            }

        anomalies = []

        for value in values:

            z = abs(
                (
                    value - mean
                ) / stdev
            )

            if z >= 3:

                anomalies.append(
                    {
                        "value":
                            value,

                        "z_score":
                            round(
                                z,
                                4,
                            ),
                    }
                )

        return {

            "detected":
                bool(anomalies),

            "count":
                len(anomalies),

            "values":
                anomalies,
        }

    # ========================================================
    #
    # NOVELTY
    #
    # ========================================================

    def _estimate_novelty(
        self,
        text: str,
        keywords: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        if not text.strip():

            return {
                "score": 0.0,
                "classification": "empty",
            }

        known_tokens = (
            set(self.POSITIVE_WORDS)
            | set(self.NEGATIVE_WORDS)
            | set(self.UNCERTAINTY_WORDS)
        )

        tokens = self._tokenize(
            text
        )

        if not tokens:

            return {
                "score": 0.0,
                "classification": "empty",
            }

        unknown = sum(
            1
            for token in tokens
            if token not in known_tokens
        )

        score = min(
            unknown
            / max(
                len(tokens),
                1,
            ),
            1.0,
        )

        if score >= 0.75:

            classification = (
                "high_novelty"
            )

        elif score >= 0.40:

            classification = (
                "medium_novelty"
            )

        else:

            classification = (
                "low_novelty"
            )

        return {

            "score":
                round(
                    score,
                    4,
                ),

            "classification":
                classification,

            "unknown_token_count":
                unknown,
        }

    # ========================================================
    #
    # SEMANTIC ANALYSIS
    #
    # ========================================================

    def _semantic_analysis(
        self,
        tokens: List[str],
    ) -> Dict[str, Any]:

        actions = Counter()

        for token in tokens:

            if token in self.ACTION_WORDS:
                actions[token] += 1

        states = Counter()

        for token in (
            self.POSITIVE_WORDS
            | self.NEGATIVE_WORDS
        ):

            if token in tokens:
                states[token] += 1

        return {

            "actions":
                dict(actions),

            "states":
                dict(states),

            "intent":
                self._infer_intent(
                    tokens
                ),
        }

    # ========================================================
    #
    # INTENT
    #
    # ========================================================

    def _infer_intent(
        self,
        tokens: List[str],
    ) -> Dict[str, int]:

        intent = Counter()

        mapping = {

            "learn": {
                "learn",
                "remember",
                "study",
            },

            "analyze": {
                "analyze",
                "analysis",
                "check",
                "inspect",
            },

            "predict": {
                "predict",
                "forecast",
                "estimate",
            },

            "evaluate": {
                "evaluate",
                "test",
                "verify",
            },

            "decision": {
                "buy",
                "sell",
                "hold",
                "decide",
            },
        }

        token_set = set(
            tokens
        )

        for intent_name, words in (
            mapping.items()
        ):

            count = len(
                token_set & words
            )

            if count:

                intent[
                    intent_name
                ] = count

        return dict(
            intent
        )

    # ========================================================
    #
    # DOCUMENT ESTIMATION
    #
    # ========================================================

    def _estimate_documents(
        self,
        data: Any,
    ) -> int:

        if isinstance(
            data,
            list,
        ):

            return len(data)

        return 1

    # ========================================================
    #
    # ANALYSIS CONSTRUCTION
    #
    # ========================================================

    def _build_analysis(
        self,
        data: Any,
        domain: str,
        features: Dict[str, Any],
    ) -> Dict[str, Any]:

        sentiment = features[
            "sentiment"
        ]

        patterns = features[
            "patterns"
        ]

        anomalies = features[
            "anomalies"
        ]

        novelty = features[
            "novelty"
        ]

        semantic = features[
            "semantic"
        ]

        evidence = 0

        evidence += min(
            len(
                features[
                    "entities"
                ]
            ),
            10,
        )

        evidence += min(
            len(
                features[
                    "keywords"
                ]
            ),
            10,
        )

        evidence += min(
            patterns[
                "count"
            ],
            10,
        )

        evidence += min(
            features[
                "numerical"
            ][
                "count"
            ],
            10,
        )

        confidence = (
            self._calculate_confidence(
                evidence,
                anomalies,
                novelty,
                sentiment,
            )
        )

        conclusions = []

        # Sentiment

        if (
            sentiment["dominant"]
            == "positive"
        ):

            conclusions.append(
                "Positive semantic signals detected."
            )

        elif (
            sentiment["dominant"]
            == "negative"
        ):

            conclusions.append(
                "Negative semantic signals detected."
            )

        else:

            conclusions.append(
                "No dominant positive or negative semantic bias detected."
            )

        # Patterns

        if patterns["count"]:

            conclusions.append(
                "One or more structural patterns were detected."
            )

        # Anomalies

        if anomalies["detected"]:

            conclusions.append(
                "Potential numerical anomalies were detected."
            )

        # Novelty

        if (
            novelty["classification"]
            == "high_novelty"
        ):

            conclusions.append(
                "The input contains relatively novel information."
            )

        # Intent

        if semantic["intent"]:

            conclusions.append(
                "Action-oriented or analytical intent was detected."
            )

        # Domain

        domain_conclusion = (
            self._domain_interpretation(
                domain,
                features,
            )
        )

        if domain_conclusion:

            conclusions.append(
                domain_conclusion
            )

        summary = " ".join(
            conclusions
        )

        return {

            "domain":
                domain,

            "confidence":
                confidence,

            "evidence_score":
                evidence,

            "sentiment":
                sentiment[
                    "dominant"
                ],

            "pattern_count":
                patterns[
                    "count"
                ],

            "anomaly_detected":
                anomalies[
                    "detected"
                ],

            "novelty":
                novelty[
                    "classification"
                ],

            "intent":
                semantic[
                    "intent"
                ],

            "conclusions":
                conclusions,

            "summary":
                summary,
        }

    # ========================================================
    #
    # CONFIDENCE
    #
    # ========================================================

    def _calculate_confidence(
        self,
        evidence: int,
        anomalies: Dict[str, Any],
        novelty: Dict[str, Any],
        sentiment: Dict[str, Any],
    ) -> float:

        score = 40.0

        score += min(
            evidence * 2.0,
            30.0,
        )

        if (
            sentiment["dominant"]
            != "neutral"
        ):

            score += 5.0

        if anomalies["detected"]:

            score -= 5.0

        if (
            novelty["classification"]
            == "high_novelty"
        ):

            score -= 5.0

        return round(
            max(
                0.0,
                min(
                    score,
                    100.0,
                ),
            ),
            2,
        )

    # ========================================================
    #
    # DOMAIN INTERPRETATION
    #
    # ========================================================

    def _domain_interpretation(
        self,
        domain: str,
        features: Dict[str, Any],
    ) -> str:

        if domain == "trading":

            patterns = features[
                "patterns"
            ][
                "detected"
            ]

            if "breakout" in patterns:

                return (
                    "Trading context contains breakout-related evidence."
                )

            if "bullish_bias" in patterns:

                return (
                    "Trading context contains bullish directional evidence."
                )

            if "bearish_bias" in patterns:

                return (
                    "Trading context contains bearish directional evidence."
                )

            return (
                "Trading-related information detected."
            )

        if domain == "science":

            return (
                "Scientific context detected; observations and evidence should be evaluated against measurable outcomes."
            )

        if domain == "mathematics":

            return (
                "Mathematical context detected; numerical relationships and structural consistency are relevant."
            )

        if domain == "knowledge":

            return (
                "Knowledge-oriented context detected; factual verification can be applied."
            )

        if domain == "reasoning":

            return (
                "Reasoning context detected; logical relationships and premises should be evaluated."
            )

        if domain == "text":

            return (
                "Text-oriented context detected; semantic structure and language features are relevant."
            )

        return (
            "General information detected and analyzed using domain-independent features."
        )

    # ========================================================
    #
    # SUCCESS REGISTRATION
    #
    # ========================================================

    def _register_success(
        self,
        result: Dict[str, Any],
    ) -> None:

        self.analysis_count += 1
        self.success_count += 1

        self.last_analysis = result

        domain = result.get(
            "domain",
            "unknown",
        )

        self.domain_counts[
            domain
        ] += 1

        features = result.get(
            "features",
            {},
        )

        sentiment = features.get(
            "sentiment",
            {},
        )

        self.sentiment_counts[
            sentiment.get(
                "dominant",
                "neutral",
            )
        ] += 1

        patterns = (
            features.get(
                "patterns",
                {},
            ).get(
                "detected",
                [],
            )
        )

        for pattern in patterns:

            self.pattern_counts[
                pattern
            ] += 1

        self.total_entities += len(
            features.get(
                "entities",
                [],
            )
        )

        self.total_keywords += len(
            features.get(
                "keywords",
                [],
            )
        )

        anomalies = features.get(
            "anomalies",
            {},
        )

        self.total_anomalies += (
            anomalies.get(
                "count",
                0,
            )
        )

        novelty = features.get(
            "novelty",
            {},
        )

        if (
            novelty.get(
                "classification"
            )
            == "high_novelty"
        ):

            self.total_novel += 1

        duration = result.get(
            "duration_ms",
            0.0,
        )

        self.total_analysis_time_ms += (
            duration
        )

        self.history.append(
            result
        )

        if (
            len(self.history)
            > self.MAX_HISTORY
        ):

            self.history = self.history[
                -self.MAX_HISTORY:
            ]

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self,
    ) -> Dict[str, Any]:

        average_duration = (

            self.total_analysis_time_ms
            / self.analysis_count

            if self.analysis_count
            else 0.0
        )

        return {

            "module":
                "learning_analyzer",

            "name":
                "Universal Learning Analyzer",

            "version":
                self.VERSION,

            "online":
                True,

            "analysis_count":
                self.analysis_count,

            "success_count":
                self.success_count,

            "error_count":
                self.error_count,

            "success_rate":
                round(
                    (
                        self.success_count
                        / self.analysis_count
                        * 100
                    )
                    if self.analysis_count
                    else 0.0,
                    2,
                ),

            "average_duration_ms":
                round(
                    average_duration,
                    3,
                ),

            "domains":
                dict(
                    self.domain_counts
                ),

            "sentiment":
                dict(
                    self.sentiment_counts
                ),

            "patterns":
                dict(
                    self.pattern_counts
                ),

            "total_entities":
                self.total_entities,

            "total_keywords":
                self.total_keywords,

            "total_anomalies":
                self.total_anomalies,

            "high_novelty":
                self.total_novel,

            "history_size":
                len(
                    self.history
                ),

            "last_error":
                self.last_error,

            "last_analysis":
                self.last_analysis,
        }

    # ========================================================
    #
    # HISTORY
    #
    # ========================================================

    def get_history(
        self,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:

        try:

            limit = max(
                1,
                min(
                    int(limit),
                    self.MAX_HISTORY,
                ),
            )

        except Exception:

            limit = 20

        return self.history[
            -limit:
        ]

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset_statistics(
        self,
    ) -> None:

        self.analysis_count = 0
        self.success_count = 0
        self.error_count = 0

        self.history.clear()

        self.domain_counts.clear()
        self.sentiment_counts.clear()
        self.pattern_counts.clear()

        self.total_entities = 0
        self.total_keywords = 0
        self.total_anomalies = 0
        self.total_novel = 0

        self.last_analysis = None
        self.last_error = None

        self.total_analysis_time_ms = 0.0

        logger.info(
            "Learning Analyzer statistics reset."
        )


# ============================================================
#
# GLOBAL INSTANCE - KONSISTEN DENGAN STANDAR
#
# ============================================================

learning_analyzer = LearningAnalyzer()


# ============================================================
#
# COMPATIBILITY FUNCTIONS
#
# ============================================================

def analyze(data: Any) -> Dict[str, Any]:
    """Legacy analyze function."""
    return learning_analyzer.analyze(data)


def status() -> Dict[str, Any]:
    """Legacy status function."""
    return learning_analyzer.status()


# ============================================================
#
# PUBLIC API
# ============================================================

__all__ = [
    "LearningAnalyzer",
    "learning_analyzer",
    "analyze",
    "status",
]


# ============================================================
#
# END
#
# ============================================================