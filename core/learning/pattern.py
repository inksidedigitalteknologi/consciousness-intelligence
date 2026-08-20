# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# PATTERN ENGINE v3.1
#
# COMPREHENSIVE GENERAL-PURPOSE PATTERN INTELLIGENCE
#
# ============================================================
#
# Supports:
#
# - Trading data
# - General knowledge
# - Text
# - Dictionaries
# - Lists
# - Nested structures
# - Numerical data
# - Entities
# - Concepts
# - Sentiment
# - Behavior
# - Temporal patterns
# - Sequence patterns
# - Co-occurrence
# - Relationships
# - Frequency analysis
# - Novelty detection
# - Anomaly detection
# - Trend detection
# - Pattern confidence
# - Pattern stability
# - Pattern history
# - Pattern fingerprint
# - Pattern consolidation
#
# Safe for LearningEngine.execute()
#
# ============================================================

import hashlib
import logging
import math
import re
from collections import Counter, defaultdict, deque
from datetime import datetime

logger = logging.getLogger(__name__)


# ============================================================
# CONFIGURATION
# ============================================================

MAX_HISTORY = 500
MAX_PATTERN_HISTORY = 200
MAX_TEXT_TOKENS = 5000
MAX_NESTED_DEPTH = 8
MAX_SEQUENCE_LENGTH = 1000
MIN_PATTERN_FREQUENCY = 2


# ============================================================
# PATTERN ENGINE
# ============================================================

class PatternEngine:

    def __init__(self):

        self.patterns = deque(
            maxlen=MAX_PATTERN_HISTORY
        )

        self.observation_history = deque(
            maxlen=MAX_HISTORY
        )

        self.frequency = Counter()

        self.key_frequency = Counter()

        self.value_frequency = Counter()

        self.entity_frequency = Counter()

        self.concept_frequency = Counter()

        self.token_frequency = Counter()

        self.relationship_frequency = Counter()

        self.sequence_frequency = Counter()

        self.type_frequency = Counter()

        self.sentiment_frequency = Counter()

        self.pattern_fingerprints = Counter()

        self.scan_count = 0

        self.total_observations = 0

        self.total_patterns = 0

        self.last_result = None

        self._initialized_at = datetime.now().isoformat()

        logger.info(
            "Pattern Engine v3.1 initialized."
        )

    # ========================================================
    # PUBLIC API
    # ========================================================

    def detect(self, observations):

        """
        Analyze one observation or a collection of observations.

        Accepted:

            dict
            list
            tuple
            set
            string
            number
            bool
            None

        Returns JSON-safe dictionary.
        """

        try:

            normalized = self._normalize_observations(
                observations
            )

            if not normalized:

                return self._empty_result()

            self.scan_count += 1

            self.total_observations += len(
                normalized
            )

            for observation in normalized:

                self._remember_observation(
                    observation
                )

            structure = self._analyze_structure(
                normalized
            )

            fields = self._analyze_fields(
                normalized
            )

            values = self._analyze_values(
                normalized
            )

            text = self._analyze_text(
                normalized
            )

            entities = self._analyze_entities(
                normalized
            )

            concepts = self._analyze_concepts(
                normalized
            )

            sentiment = self._analyze_sentiment(
                normalized
            )

            behavior = self._analyze_behavior(
                normalized
            )

            numerical = self._analyze_numerical(
                normalized
            )

            temporal = self._analyze_temporal(
                normalized
            )

            sequences = self._analyze_sequences(
                normalized
            )

            relationships = self._analyze_relationships(
                normalized
            )

            cooccurrence = self._analyze_cooccurrence(
                normalized
            )

            recurrence = self._analyze_recurrence(
                normalized
            )

            trends = self._analyze_trends(
                normalized
            )

            anomalies = self._analyze_anomalies(
                normalized,
                numerical
            )

            novelty = self._analyze_novelty(
                normalized
            )

            semantic = self._analyze_semantic_patterns(
                normalized
            )

            fingerprint = self._create_fingerprint(
                normalized
            )

            confidence = self._calculate_confidence(
                structure,
                fields,
                values,
                text,
                entities,
                concepts,
                relationships
            )

            result = {

                "timestamp":
                    datetime.now().isoformat(),

                "engine":
                    "Pattern Engine",

                "version":
                    "3.1",

                "scan":
                    self.scan_count,

                "observation_count":
                    len(normalized),

                "structure":
                    structure,

                "fields":
                    fields,

                "values":
                    values,

                "text":
                    text,

                "entities":
                    entities,

                "concepts":
                    concepts,

                "sentiment":
                    sentiment,

                "behavior":
                    behavior,

                "numerical":
                    numerical,

                "temporal":
                    temporal,

                "sequences":
                    sequences,

                "relationships":
                    relationships,

                "cooccurrence":
                    cooccurrence,

                "recurrence":
                    recurrence,

                "trends":
                    trends,

                "anomalies":
                    anomalies,

                "novelty":
                    novelty,

                "semantic":
                    semantic,

                "fingerprint":
                    fingerprint,

                "confidence":
                    confidence,

                "summary":
                    self._build_summary(
                        structure,
                        fields,
                        text,
                        entities,
                        concepts,
                        trends,
                        anomalies,
                        novelty
                    )
            }

            self._register_patterns(
                result
            )

            self.last_result = result

            return result

        except Exception as e:

            logger.exception(
                "Pattern detection failed: %s",
                e
            )

            return {
                "timestamp":
                    datetime.now().isoformat(),

                "engine":
                    "Pattern Engine",

                "version":
                    "3.1",

                "error":
                    str(e),

                "patterns":
                    {},

                "confidence":
                    0
            }

    # ========================================================
    # NORMALIZATION
    # ========================================================

    def _normalize_observations(self, data):

        if data is None:

            return []

        if isinstance(data, dict):

            return [self._safe_copy(data)]

        if isinstance(data, str):

            return [
                {
                    "text": data
                }
            ]

        if isinstance(data, (int, float, bool)):

            return [
                {
                    "value": data
                }
            ]

        if isinstance(data, (list, tuple, set)):

            result = []

            for item in list(data):

                if isinstance(item, dict):

                    result.append(
                        self._safe_copy(item)
                    )

                elif isinstance(
                    item,
                    (str, int, float, bool)
                ):

                    result.append(
                        {
                            "value": item
                        }
                    )

                else:

                    result.append(
                        {
                            "value":
                                self._safe_string(item)
                        }
                    )

            return result

        return [
            {
                "value":
                    self._safe_string(data)
            }
        ]

    # ========================================================
    # SAFE COPY
    # ========================================================

    def _safe_copy(
        self,
        data,
        depth=0,
        seen=None
    ):

        if seen is None:

            seen = set()

        if depth > MAX_NESTED_DEPTH:

            return "<MAX_DEPTH>"

        if isinstance(data, dict):

            object_id = id(data)

            if object_id in seen:

                return "<CIRCULAR_REFERENCE>"

            seen.add(object_id)

            result = {}

            for key, value in data.items():

                safe_key = self._safe_string(
                    key
                )

                result[safe_key] = self._safe_copy(
                    value,
                    depth + 1,
                    seen
                )

            seen.discard(object_id)

            return result

        if isinstance(data, (list, tuple, set)):

            object_id = id(data)

            if object_id in seen:

                return "<CIRCULAR_REFERENCE>"

            seen.add(object_id)

            result = []

            for value in list(data)[:MAX_SEQUENCE_LENGTH]:

                result.append(
                    self._safe_copy(
                        value,
                        depth + 1,
                        seen
                    )
                )

            seen.discard(object_id)

            return result

        if isinstance(
            data,
            (str, int, float, bool)
        ):

            if isinstance(data, float):

                if math.isnan(data):

                    return "NaN"

                if math.isinf(data):

                    return "Infinity"

            return data

        if data is None:

            return None

        return self._safe_string(data)

    # ========================================================
    # SAFE STRING
    # ========================================================

    def _safe_string(self, value):

        try:

            return str(value)[:1000]

        except Exception:

            return "<UNSERIALIZABLE>"

    # ========================================================
    # REMEMBER
    # ========================================================

    def _remember_observation(
        self,
        observation
    ):

        self.observation_history.append(
            self._safe_copy(observation)
        )

    # ========================================================
    # STRUCTURE ANALYSIS
    # ========================================================

    def _analyze_structure(
        self,
        observations
    ):

        type_counter = Counter()

        depth_counter = Counter()

        key_count = Counter()

        for item in observations:

            type_counter[
                type(item).__name__
            ] += 1

            depth = self._depth(item)

            depth_counter[
                depth
            ] += 1

            if isinstance(item, dict):

                for key in item.keys():

                    key_count[
                        str(key)
                    ] += 1

        self.type_frequency.update(
            type_counter
        )

        return {

            "types":
                dict(type_counter),

            "depth":
                dict(depth_counter),

            "keys":
                dict(key_count),

            "count":
                len(observations)
        }

    # ========================================================
    # DEPTH
    # ========================================================

    def _depth(
        self,
        value,
        level=0
    ):

        if level >= MAX_NESTED_DEPTH:

            return level

        if isinstance(value, dict):

            if not value:

                return level

            return max(
                self._depth(
                    item,
                    level + 1
                )
                for item in value.values()
            )

        if isinstance(value, list):

            if not value:

                return level

            return max(
                self._depth(
                    item,
                    level + 1
                )
                for item in value
            )

        return level

    # ========================================================
    # FIELD ANALYSIS
    # ========================================================

    def _analyze_fields(
        self,
        observations
    ):

        fields = Counter()

        field_types = defaultdict(
            Counter
        )

        for item in observations:

            if not isinstance(item, dict):

                continue

            for key, value in item.items():

                key = str(key)

                fields[key] += 1

                field_types[key][
                    type(value).__name__
                ] += 1

        self.key_frequency.update(
            fields
        )

        return {

            "frequency":
                dict(fields),

            "types":
                {
                    key:
                        dict(counter)

                    for key, counter
                    in field_types.items()
                },

            "unique_fields":
                len(fields)
        }

    # ========================================================
    # VALUE ANALYSIS
    # ========================================================

    def _analyze_values(
        self,
        observations
    ):

        values = Counter()

        for item in observations:

            self._collect_values(
                item,
                values
            )

        self.value_frequency.update(
            values
        )

        return {

            "frequent":
                [
                    {
                        "value":
                            key,

                        "count":
                            count
                    }

                    for key, count
                    in values.most_common(20)
                ],

            "unique":
                len(values)
        }

    def _collect_values(
        self,
        value,
        counter,
        depth=0
    ):

        if depth > MAX_NESTED_DEPTH:

            return

        if isinstance(value, dict):

            for key, item in value.items():

                counter[
                    self._value_signature(key)
                ] += 1

                self._collect_values(
                    item,
                    counter,
                    depth + 1
                )

        elif isinstance(value, list):

            for item in value[:MAX_SEQUENCE_LENGTH]:

                self._collect_values(
                    item,
                    counter,
                    depth + 1
                )

        else:

            counter[
                self._value_signature(value)
            ] += 1

    # ========================================================
    # VALUE SIGNATURE
    # ========================================================

    def _value_signature(
        self,
        value
    ):

        if isinstance(value, str):

            text = value.strip()

            if len(text) > 100:

                return text[:100]

            return text.lower()

        return self._safe_string(value)

    # ========================================================
    # TEXT ANALYSIS
    # ========================================================

    def _analyze_text(
        self,
        observations
    ):

        tokens = []

        text_sources = []

        for item in observations:

            self._extract_text(
                item,
                text_sources
            )

        for text in text_sources:

            found = re.findall(
                r"[A-Za-z0-9_./%+-]+",
                text.lower()
            )

            tokens.extend(
                found[:MAX_TEXT_TOKENS]
            )

        self.token_frequency.update(
            tokens
        )

        stopwords = {

            "the",
            "a",
            "an",
            "and",
            "or",
            "of",
            "to",
            "in",
            "on",
            "for",
            "with",
            "is",
            "are",
            "was",
            "were",
            "this",
            "that",
            "it",
            "as",
            "at",
            "by"
        }

        meaningful = [
            token
            for token in tokens
            if token not in stopwords
            and len(token) > 1
        ]

        counter = Counter(
            meaningful
        )

        return {

            "documents":
                len(text_sources),

            "characters":
                sum(
                    len(text)
                    for text in text_sources
                ),

            "tokens":
                len(tokens),

            "unique_tokens":
                len(set(tokens)),

            "keywords":
                [
                    {
                        "token":
                            token,

                        "frequency":
                            count
                    }

                    for token, count
                    in counter.most_common(30)
                ]
        }

    def _extract_text(
        self,
        value,
        output,
        depth=0
    ):

        if depth > MAX_NESTED_DEPTH:

            return

        if isinstance(value, str):

            if value.strip():

                output.append(
                    value[:10000]
                )

            return

        if isinstance(value, dict):

            for key, item in value.items():

                if isinstance(key, str):

                    output.append(key)

                self._extract_text(
                    item,
                    output,
                    depth + 1
                )

            return

        if isinstance(value, list):

            for item in value[:MAX_SEQUENCE_LENGTH]:

                self._extract_text(
                    item,
                    output,
                    depth + 1
                )

    # ========================================================
    # ENTITY ANALYSIS
    # ========================================================

    def _analyze_entities(
        self,
        observations
    ):

        entities = Counter()

        for item in observations:

            if not isinstance(item, dict):

                continue

            source = item.get(
                "entities",
                []
            )

            if isinstance(source, dict):

                source = [source]

            if not isinstance(
                source,
                list
            ):

                continue

            for entity in source:

                if isinstance(entity, dict):

                    name = entity.get(
                        "name"
                    )

                    entity_type = entity.get(
                        "type",
                        "UNKNOWN"
                    )

                    if name:

                        signature = (
                            f"{name}:{entity_type}"
                        )

                        entities[
                            signature
                        ] += 1

        self.entity_frequency.update(
            entities
        )

        return {

            "detected":
                dict(entities),

            "unique":
                len(entities)
        }

    # ========================================================
    # CONCEPT ANALYSIS
    # ========================================================

    def _analyze_concepts(
        self,
        observations
    ):

        concepts = Counter()

        concept_fields = {

            "concepts",
            "keywords",
            "topics",
            "themes",
            "categories",
            "tags"
        }

        for item in observations:

            self._extract_named_values(
                item,
                concept_fields,
                concepts
            )

        self.concept_frequency.update(
            concepts
        )

        return {

            "concepts":
                dict(concepts),

            "top":
                [
                    concept
                    for concept, _
                    in concepts.most_common(20)
                ]
        }

    def _extract_named_values(
        self,
        value,
        field_names,
        counter,
        depth=0
    ):

        if depth > MAX_NESTED_DEPTH:

            return

        if isinstance(value, dict):

            for key, item in value.items():

                key_lower = str(
                    key
                ).lower()

                if key_lower in field_names:

                    if isinstance(
                        item,
                        str
                    ):

                        counter[
                            item.lower()
                        ] += 1

                    elif isinstance(
                        item,
                        list
                    ):

                        for entry in item:

                            if isinstance(
                                entry,
                                str
                            ):

                                counter[
                                    entry.lower()
                                ] += 1

                self._extract_named_values(
                    item,
                    field_names,
                    counter,
                    depth + 1
                )

        elif isinstance(value, list):

            for item in value:

                self._extract_named_values(
                    item,
                    field_names,
                    counter,
                    depth + 1
                )

    # ========================================================
    # SENTIMENT
    # ========================================================

    def _analyze_sentiment(
        self,
        observations
    ):

        counter = Counter()

        positive_words = {

            "positive",
            "bullish",
            "strong",
            "growth",
            "success",
            "successful",
            "gain",
            "good",
            "improving",
            "increase",
            "up",
            "profit",
            "win",
            "healthy"
        }

        negative_words = {

            "negative",
            "bearish",
            "weak",
            "loss",
            "failed",
            "failure",
            "bad",
            "decline",
            "decrease",
            "down",
            "risk",
            "problem",
            "error"
        }

        neutral_words = {

            "neutral",
            "stable",
            "hold",
            "unknown",
            "normal"
        }

        for item in observations:

            text = self._flatten_text(
                item
            ).lower()

            positive = sum(
                text.count(word)
                for word in positive_words
            )

            negative = sum(
                text.count(word)
                for word in negative_words
            )

            neutral = sum(
                text.count(word)
                for word in neutral_words
            )

            if positive > negative:

                counter["positive"] += 1

            elif negative > positive:

                counter["negative"] += 1

            elif neutral:

                counter["neutral"] += 1

            else:

                counter["unknown"] += 1

        self.sentiment_frequency.update(
            counter
        )

        return {

            "distribution":
                dict(counter),

            "dominant":
                counter.most_common(1)[0][0]
                if counter
                else "unknown"
        }

    # ========================================================
    # BEHAVIOR
    # ========================================================

    def _analyze_behavior(
        self,
        observations
    ):

        behavior = Counter()

        positive = {

            "buy",
            "bullish",
            "increase",
            "growth",
            "expand",
            "up",
            "gain",
            "win",
            "success"
        }

        negative = {

            "sell",
            "bearish",
            "decrease",
            "decline",
            "down",
            "loss",
            "fail",
            "failure"
        }

        for item in observations:

            text = self._flatten_text(
                item
            ).lower()

            if any(
                word in text
                for word in positive
            ):

                behavior["positive"] += 1

            if any(
                word in text
                for word in negative
            ):

                behavior["negative"] += 1

            if (
                not any(
                    word in text
                    for word in positive
                )
                and
                not any(
                    word in text
                    for word in negative
                )
            ):

                behavior["neutral"] += 1

        return dict(
            behavior
        )

    # ========================================================
    # NUMERICAL ANALYSIS
    # ========================================================

    def _analyze_numerical(
        self,
        observations
    ):

        numbers = []

        self._collect_numbers(
            observations,
            numbers
        )

        if not numbers:

            return {

                "count":
                    0,

                "mean":
                    None,

                "minimum":
                    None,

                "maximum":
                    None,

                "range":
                    None
            }

        mean = sum(
            numbers
        ) / len(numbers)

        minimum = min(
            numbers
        )

        maximum = max(
            numbers
        )

        variance = sum(
            (
                value - mean
            ) ** 2
            for value in numbers
        ) / len(numbers)

        return {

            "count":
                len(numbers),

            "mean":
                round(
                    mean,
                    8
                ),

            "minimum":
                minimum,

            "maximum":
                maximum,

            "range":
                maximum - minimum,

            "variance":
                round(
                    variance,
                    8
                ),

            "standard_deviation":
                round(
                    math.sqrt(
                        variance
                    ),
                    8
                )
        }

    def _collect_numbers(
        self,
        value,
        output
    ):

        if isinstance(
            value,
            bool
        ):

            return

        if isinstance(
            value,
            (int, float)
        ):

            if isinstance(value, float):

                if (
                    math.isnan(value)
                    or
                    math.isinf(value)
                ):

                    return

            output.append(
                float(value)
            )

            return

        if isinstance(value, dict):

            for item in value.values():

                self._collect_numbers(
                    item,
                    output
                )

            return

        if isinstance(value, list):

            for item in value:

                self._collect_numbers(
                    item,
                    output
                )

    # ========================================================
    # TEMPORAL ANALYSIS
    # ========================================================

    def _analyze_temporal(
        self,
        observations
    ):

        timestamps = []

        for item in observations:

            if not isinstance(
                item,
                dict
            ):

                continue

            for key in (
                "timestamp",
                "time",
                "datetime",
                "date"
            ):

                value = item.get(
                    key
                )

                if value:

                    timestamps.append(
                        self._safe_string(
                            value
                        )
                    )

                    break

        return {

            "count":
                len(timestamps),

            "timestamps":
                timestamps[-20:]
        }

    # ========================================================
    # SEQUENCE ANALYSIS
    # ========================================================

    def _analyze_sequences(
        self,
        observations
    ):

        sequences = []

        for item in observations:

            if isinstance(
                item,
                dict
            ):

                for key, value in item.items():

                    if isinstance(
                        value,
                        list
                    ):

                        if 2 <= len(value) <= MAX_SEQUENCE_LENGTH:

                            signatures = [
                                self._value_signature(
                                    entry
                                )
                                for entry in value
                            ]

                            sequences.append({

                                "field":
                                    str(key),

                                "length":
                                    len(signatures),

                                "sequence":
                                    signatures[:100]
                            })

        return {

            "detected":
                sequences[:20],

            "count":
                len(sequences)
        }

    # ========================================================
    # RELATIONSHIP ANALYSIS
    # ========================================================

    def _analyze_relationships(
        self,
        observations
    ):

        relationships = Counter()

        for item in observations:

            if not isinstance(
                item,
                dict
            ):

                continue

            keys = [
                str(key)
                for key in item.keys()
            ]

            for index, first in enumerate(keys):

                for second in keys[index + 1:]:

                    pair = (
                        first,
                        second
                    )

                    relationships[
                        pair
                    ] += 1

        self.relationship_frequency.update(
            relationships
        )

        return {

            "relationships":
                [
                    {
                        "fields":
                            list(pair),

                        "frequency":
                            count
                    }

                    for pair, count
                    in relationships.most_common(30)
                ]
        }

    # ========================================================
    # COOCCURRENCE
    # ========================================================

    def _analyze_cooccurrence(
        self,
        observations
    ):

        cooccurrence = Counter()

        for item in observations:

            tokens = set(
                re.findall(
                    r"[A-Za-z0-9_./%+-]+",
                    self._flatten_text(
                        item
                    ).lower()
                )
            )

            tokens = list(
                tokens
            )[:100]

            for index, first in enumerate(tokens):

                for second in tokens[index + 1:]:

                    pair = tuple(
                        sorted(
                            (
                                first,
                                second
                            )
                        )
                    )

                    cooccurrence[
                        pair
                    ] += 1

        return {

            "pairs":
                [
                    {
                        "terms":
                            list(pair),

                        "frequency":
                            count
                    }

                    for pair, count
                    in cooccurrence.most_common(30)
                ]
        }

    # ========================================================
    # RECURRENCE
    # ========================================================

    def _analyze_recurrence(
        self,
        observations
    ):

        fingerprints = Counter()

        for item in observations:

            fingerprint = self._fingerprint(
                item
            )

            fingerprints[
                fingerprint
            ] += 1

        recurring = [
            {
                "fingerprint":
                    fingerprint,

                "count":
                    count
            }

            for fingerprint, count
            in fingerprints.items()
            if count > 1
        ]

        return {

            "recurring":
                recurring[:30],

            "count":
                len(recurring)
        }

    # ========================================================
    # TREND ANALYSIS
    # ========================================================

    def _analyze_trends(
        self,
        observations
    ):

        numbers = []

        self._collect_numbers(
            observations,
            numbers
        )

        if len(numbers) < 2:

            return {

                "direction":
                    "unknown",

                "strength":
                    0
            }

        increases = 0

        decreases = 0

        for index in range(
            1,
            len(numbers)
        ):

            if numbers[index] > numbers[index - 1]:

                increases += 1

            elif numbers[index] < numbers[index - 1]:

                decreases += 1

        total = (
            increases
            +
            decreases
        )

        if total == 0:

            return {

                "direction":
                    "stable",

                "strength":
                    0
            }

        if increases > decreases:

            direction = "increasing"

        elif decreases > increases:

            direction = "decreasing"

        else:

            direction = "mixed"

        strength = (
            abs(
                increases
                -
                decreases
            )
            /
            total
        )

        return {

            "direction":
                direction,

            "increases":
                increases,

            "decreases":
                decreases,

            "strength":
                round(
                    strength,
                    4
                )
        }

    # ========================================================
    # ANOMALY DETECTION
    # ========================================================

    def _analyze_anomalies(
        self,
        observations,
        numerical
    ):

        standard_deviation = numerical.get(
            "standard_deviation"
        )

        mean = numerical.get(
            "mean"
        )

        if (
            standard_deviation is None
            or
            mean is None
            or
            standard_deviation == 0
        ):

            return {

                "detected":
                    False,

                "count":
                    0
            }

        numbers = []

        self._collect_numbers(
            observations,
            numbers
        )

        anomalies = []

        threshold = (
            standard_deviation * 2
        )

        for value in numbers:

            distance = abs(
                value - mean
            )

            if distance > threshold:

                anomalies.append({

                    "value":
                        value,

                    "distance":
                        round(
                            distance,
                            8
                        )
                })

        return {

            "detected":
                bool(anomalies),

            "count":
                len(anomalies),

            "values":
                anomalies[:30]
        }

    # ========================================================
    # NOVELTY
    # ========================================================

    def _analyze_novelty(
        self,
        observations
    ):

        new_count = 0

        known_count = 0

        for item in observations:

            fingerprint = self._fingerprint(
                item
            )

            if (
                self.pattern_fingerprints.get(
                    fingerprint,
                    0
                )
                > 0
            ):

                known_count += 1

            else:

                new_count += 1

        total = (
            new_count
            +
            known_count
        )

        score = (
            new_count / total
            if total
            else 0
        )

        return {

            "new":
                new_count,

            "known":
                known_count,

            "score":
                round(
                    score,
                    4
                ),

            "classification":
                (
                    "high_novelty"
                    if score >= 0.7
                    else
                    "moderate_novelty"
                    if score >= 0.3
                    else
                    "familiar"
                )
        }

    # ========================================================
    # SEMANTIC PATTERN ANALYSIS
    # ========================================================

    def _analyze_semantic_patterns(
        self,
        observations
    ):

        semantic = {

            "topics":
                Counter(),

            "intent":
                Counter(),

            "actions":
                Counter(),

            "states":
                Counter()
        }

        intent_words = {

            "question":
                [
                    "why",
                    "what",
                    "how",
                    "when",
                    "where"
                ],

            "request":
                [
                    "need",
                    "want",
                    "request",
                    "please"
                ],

            "prediction":
                [
                    "predict",
                    "forecast",
                    "likely",
                    "future"
                ],

            "decision":
                [
                    "buy",
                    "sell",
                    "hold",
                    "decide"
                ]
        }

        action_words = {

            "increase",
            "decrease",
            "buy",
            "sell",
            "hold",
            "learn",
            "analyze",
            "predict",
            "build",
            "update",
            "create",
            "remove",
            "store"
        }

        state_words = {

            "active",
            "inactive",
            "stable",
            "unstable",
            "strong",
            "weak",
            "healthy",
            "error",
            "online",
            "offline"
        }

        for item in observations:

            text = self._flatten_text(
                item
            ).lower()

            for intent, words in intent_words.items():

                if any(
                    word in text
                    for word in words
                ):

                    semantic[
                        "intent"
                    ][intent] += 1

            for word in action_words:

                if word in text:

                    semantic[
                        "actions"
                    ][word] += 1

            for word in state_words:

                if word in text:

                    semantic[
                        "states"
                    ][word] += 1

        return {

            "intent":
                dict(
                    semantic["intent"]
                ),

            "actions":
                dict(
                    semantic["actions"]
                ),

            "states":
                dict(
                    semantic["states"]
                )
        }

    # ========================================================
    # FINGERPRINT
    # ========================================================

    def _fingerprint(
        self,
        value
    ):

        safe = self._safe_copy(
            value
        )

        text = repr(
            safe
        )

        return hashlib.sha256(
            text.encode(
                "utf-8",
                errors="ignore"
            )
        ).hexdigest()[:16]

    def _create_fingerprint(
        self,
        observations
    ):

        signatures = [
            self._fingerprint(
                item
            )
            for item in observations
        ]

        combined = "|".join(
            signatures
        )

        return hashlib.sha256(
            combined.encode(
                "utf-8",
                errors="ignore"
            )
        ).hexdigest()[:20]

    # ========================================================
    # REGISTER PATTERNS
    # ========================================================

    def _register_patterns(
        self,
        result
    ):

        fingerprint = result.get(
            "fingerprint"
        )

        if fingerprint:

            self.pattern_fingerprints[
                fingerprint
            ] += 1

        for item in result.get(
            "text",
            {}
        ).get(
            "keywords",
            []
        ):

            token = item.get(
                "token"
            )

            if token:

                self.frequency[
                    token
                ] += item.get(
                    "frequency",
                    0
                )

        self.total_patterns += 1

        self.patterns.append(
            self._safe_copy(
                result
            )
        )

    # ========================================================
    # CONFIDENCE
    # ========================================================

    def _calculate_confidence(
        self,
        structure,
        fields,
        values,
        text,
        entities,
        concepts,
        relationships
    ):

        score = 0

        if structure.get(
            "count",
            0
        ):

            score += 15

        if fields.get(
            "unique_fields",
            0
        ):

            score += 15

        if values.get(
            "unique",
            0
        ):

            score += 15

        if text.get(
            "tokens",
            0
        ):

            score += 15

        if entities.get(
            "unique",
            0
        ):

            score += 10

        if concepts.get(
            "top"
        ):

            score += 10

        if relationships.get(
            "relationships"
        ):

            score += 10

        score = min(
            score,
            100
        )

        return score

    # ========================================================
    # SUMMARY
    # ========================================================

    def _build_summary(
        self,
        structure,
        fields,
        text,
        entities,
        concepts,
        trends,
        anomalies,
        novelty
    ):

        parts = []

        count = structure.get(
            "count",
            0
        )

        parts.append(
            f"Analyzed {count} observation(s)."
        )

        unique_fields = fields.get(
            "unique_fields",
            0
        )

        if unique_fields:

            parts.append(
                f"{unique_fields} unique field(s) detected."
            )

        tokens = text.get(
            "unique_tokens",
            0
        )

        if tokens:

            parts.append(
                f"{tokens} unique text token(s) identified."
            )

        entity_count = entities.get(
            "unique",
            0
        )

        if entity_count:

            parts.append(
                f"{entity_count} entity pattern(s) detected."
            )

        concept_count = len(
            concepts.get(
                "top",
                []
            )
        )

        if concept_count:

            parts.append(
                f"{concept_count} concept(s) identified."
            )

        direction = trends.get(
            "direction"
        )

        if direction != "unknown":

            parts.append(
                f"Numerical trend: {direction}."
            )

        if anomalies.get(
            "detected"
        ):

            parts.append(
                f"{anomalies.get('count', 0)} numerical anomaly/anomalies detected."
            )

        parts.append(
            f"Novelty: {novelty.get('classification', 'unknown')}."
        )

        return " ".join(
            parts
        )

    # ========================================================
    # FLATTEN TEXT
    # ========================================================

    def _flatten_text(
        self,
        value,
        depth=0
    ):

        if depth > MAX_NESTED_DEPTH:

            return ""

        if isinstance(
            value,
            str
        ):

            return value

        if isinstance(
            value,
            (int, float, bool)
        ):

            return self._safe_string(
                value
            )

        if isinstance(
            value,
            dict
        ):

            parts = []

            for key, item in value.items():

                parts.append(
                    self._safe_string(
                        key
                    )
                )

                parts.append(
                    self._flatten_text(
                        item,
                        depth + 1
                    )
                )

            return " ".join(
                parts
            )

        if isinstance(
            value,
            list
        ):

            return " ".join(
                self._flatten_text(
                    item,
                    depth + 1
                )
                for item in value
            )

        return self._safe_string(
            value
        )

    # ========================================================
    # EMPTY RESULT
    # ========================================================

    def _empty_result(self):

        return {

            "timestamp":
                datetime.now().isoformat(),

            "engine":
                "Pattern Engine",

            "version":
                "3.1",

            "scan":
                self.scan_count,

            "observation_count":
                0,

            "structure":
                {},

            "fields":
                {},

            "values":
                {},

            "text":
                {},

            "entities":
                {},

            "concepts":
                {},

            "sentiment":
                {},

            "behavior":
                {},

            "numerical":
                {},

            "temporal":
                {},

            "sequences":
                {},

            "relationships":
                {},

            "cooccurrence":
                {},

            "recurrence":
                {},

            "trends":
                {},

            "anomalies":
                {},

            "novelty":
                {},

            "semantic":
                {},

            "fingerprint":
                None,

            "confidence":
                0,

            "summary":
                "No observations available."
        }

    # ========================================================
    # GET PATTERNS
    # ========================================================

    def get_patterns(
        self,
        limit=10
    ):

        try:

            limit = max(
                1,
                min(
                    int(limit),
                    MAX_PATTERN_HISTORY
                )
            )

        except Exception:

            limit = 10

        return list(
            self.patterns
        )[-limit:]

    # ========================================================
    # GET FREQUENT PATTERNS
    # ========================================================

    def get_frequent_patterns(
        self,
        limit=20
    ):

        try:

            limit = max(
                1,
                int(limit)
            )

        except Exception:

            limit = 20

        return [

            {
                "pattern":
                    key,

                "frequency":
                    count
            }

            for key, count
            in self.frequency.most_common(
                limit
            )
        ]

    # ========================================================
    # GET STATE
    # ========================================================

    def get_state(self):

        return {

            "engine":
                "Pattern Engine",

            "version":
                "3.1",

            "scans":
                self.scan_count,

            "observations":
                self.total_observations,

            "patterns":
                self.total_patterns,

            "history":
                len(
                    self.patterns
                ),

            "unique_fingerprints":
                len(
                    self.pattern_fingerprints
                ),

            "top_tokens":
                dict(
                    self.token_frequency.most_common(
                        20
                    )
                ),

            "top_entities":
                dict(
                    self.entity_frequency.most_common(
                        20
                    )
                ),

            "top_concepts":
                dict(
                    self.concept_frequency.most_common(
                        20
                    )
                )
        }

    # ========================================================
    # STATUS - ADDED FOR COMPATIBILITY
    # ========================================================

    def status(
        self,
    ) -> dict:
        """
        Return module status for integration test compatibility.

        This method is used by the integration test suite
        to display module status in the system status report.
        """

        return {

            "module":
                "pattern_engine",

            "name":
                "Pattern Engine",

            "version":
                "3.1",

            "online":
                True,

            "status":
                "ONLINE",

            "scans":
                self.scan_count,

            "observations":
                self.total_observations,

            "patterns":
                self.total_patterns,

            "history":
                len(
                    self.patterns
                ),

            "unique_fingerprints":
                len(
                    self.pattern_fingerprints
                ),

            "initialized_at":
                self._initialized_at,

            "timestamp":
                datetime.now().isoformat(),
        }

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        try:

            self.patterns.clear()

            self.observation_history.clear()

            self.frequency.clear()

            self.key_frequency.clear()

            self.value_frequency.clear()

            self.entity_frequency.clear()

            self.concept_frequency.clear()

            self.token_frequency.clear()

            self.relationship_frequency.clear()

            self.sequence_frequency.clear()

            self.type_frequency.clear()

            self.sentiment_frequency.clear()

            self.pattern_fingerprints.clear()

            self.scan_count = 0

            self.total_observations = 0

            self.total_patterns = 0

            self.last_result = None

            logger.info(
                "Pattern Engine reset."
            )

            return True

        except Exception as e:

            logger.exception(
                "Pattern Engine reset failed: %s",
                e
            )

            return False


# ============================================================
# GLOBAL INSTANCE
# ============================================================

pattern = PatternEngine()


# ============================================================
# COMPATIBILITY STATUS FUNCTION
# ============================================================

def status() -> dict:
    """
    Module-level status access for integration test compatibility.
    """

    return pattern.status()


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [

    "PatternEngine",

    "pattern",

    "status",

    "MAX_HISTORY",

    "MAX_PATTERN_HISTORY",

    "MAX_TEXT_TOKENS",

    "MAX_NESTED_DEPTH",

    "MAX_SEQUENCE_LENGTH",

    "MIN_PATTERN_FREQUENCY",
]