
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# FEATURE EXTRACTOR
#
# Version: 2.0
#
# Comprehensive Feature Extraction Layer
#
# Responsibilities:
# - Extract structural features
# - Extract type information
# - Extract text features
# - Extract numeric features
# - Extract collection statistics
# - Extract dictionary metadata
# - Extract market-oriented features
# - Handle nested data
# - Handle lists / tuples / sets
# - Handle None safely
# - Preserve backward compatibility
#
# ============================================================

import logging
import math
import re
from collections import Counter

logger = logging.getLogger(__name__)


# ============================================================
#
# FEATURE EXTRACTOR
#
# ============================================================

class FeatureExtractor:

    VERSION = "2.0"

    def __init__(self):

        self.name = "feature_extractor"

        self.count = 0
        self.success_count = 0
        self.error_count = 0

        self.last_features = {}
        self.last_input_type = None

        logger.info(
            "Feature Extractor initialized."
        )

    # ========================================================
    # MAIN PROCESS
    # ========================================================

    def process(self, data):

        self.count += 1

        self.last_input_type = (
            type(data).__name__
        )

        try:

            features = self._extract_features(
                data
            )

            self.last_features = features
            self.success_count += 1

            return features

        except Exception as e:

            self.error_count += 1

            logger.exception(
                "Feature extractor error: %s",
                e
            )

            return {}

    # ========================================================
    # BACKWARD COMPATIBILITY
    # ========================================================

    def extract(self, data):

        return self.process(data)

    # ========================================================
    # FEATURE EXTRACTION ROUTER
    # ========================================================

    def _extract_features(self, data):

        features = {

            "extractor": self.name,

            "version": self.VERSION,

            "data_type":
                type(data).__name__,

        }

        # ----------------------------------------------------
        # NONE
        # ----------------------------------------------------

        if data is None:

            features.update({

                "is_empty": True,

                "is_none": True,

                "size": 0,

            })

            return features

        features["is_none"] = False

        # ----------------------------------------------------
        # DICTIONARY
        # ----------------------------------------------------

        if isinstance(data, dict):

            features.update(
                self._extract_dict_features(
                    data
                )
            )

            return features

        # ----------------------------------------------------
        # TEXT
        # ----------------------------------------------------

        if isinstance(data, str):

            features.update(
                self._extract_text_features(
                    data
                )
            )

            return features

        # ----------------------------------------------------
        # NUMERIC
        # ----------------------------------------------------

        if isinstance(
            data,
            (int, float)
        ) and not isinstance(
            data,
            bool
        ):

            features.update(
                self._extract_numeric_features(
                    data
                )
            )

            return features

        # ----------------------------------------------------
        # BOOLEAN
        # ----------------------------------------------------

        if isinstance(data, bool):

            features.update({

                "is_boolean": True,

                "boolean_value": data,

                "numeric_value":
                    int(data),

            })

            return features

        # ----------------------------------------------------
        # LIST / TUPLE / SET
        # ----------------------------------------------------

        if isinstance(
            data,
            (list, tuple, set)
        ):

            features.update(
                self._extract_collection_features(
                    data
                )
            )

            return features

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        features.update({

            "is_empty": False,

            "object_type":
                type(data).__name__,

            "string_length":
                len(str(data)),

        })

        return features

    # ========================================================
    # DICTIONARY FEATURES
    # ========================================================

    def _extract_dict_features(self, data):

        keys = list(data.keys())
        values = list(data.values())

        string_keys = [
            key for key in keys
            if isinstance(key, str)
        ]

        numeric_values = [
            value
            for value in values
            if isinstance(
                value,
                (int, float)
            )
            and not isinstance(
                value,
                bool
            )
        ]

        boolean_values = [
            value
            for value in values
            if isinstance(
                value,
                bool
            )
        ]

        string_values = [
            value
            for value in values
            if isinstance(
                value,
                str
            )
        ]

        nested_values = [
            value
            for value in values
            if isinstance(
                value,
                (dict, list, tuple, set)
            )
        ]

        none_values = [
            value
            for value in values
            if value is None
        ]

        features = {

            # Basic structure
            "is_empty":
                len(data) == 0,

            "size":
                len(data),

            "key_count":
                len(keys),

            "keys":
                keys,

            "string_keys":
                string_keys,

            # Value types
            "value_count":
                len(values),

            "string_value_count":
                len(string_values),

            "numeric_value_count":
                len(numeric_values),

            "boolean_value_count":
                len(boolean_values),

            "nested_value_count":
                len(nested_values),

            "none_value_count":
                len(none_values),

            # Structure
            "has_nested_data":
                len(nested_values) > 0,

            "has_none_values":
                len(none_values) > 0,

            "has_numeric_values":
                len(numeric_values) > 0,

            "has_text_values":
                len(string_values) > 0,

            "has_boolean_values":
                len(boolean_values) > 0,

        }

        # ----------------------------------------------------
        # Numeric summary
        # ----------------------------------------------------

        if numeric_values:

            features.update(
                self._numeric_summary(
                    numeric_values
                )
            )

        # ----------------------------------------------------
        # Text summary
        # ----------------------------------------------------

        if string_values:

            text_features = self._text_collection_summary(
                string_values
            )

            features.update(
                text_features
            )

        # ----------------------------------------------------
        # Market-oriented features
        # ----------------------------------------------------

        features.update(
            self._extract_market_features(
                data
            )
        )

        # ----------------------------------------------------
        # Common semantic keys
        # ----------------------------------------------------

        features.update(
            self._extract_semantic_keys(
                data
            )
        )

        return features

    # ========================================================
    # TEXT FEATURES
    # ========================================================

    def _extract_text_features(self, text):

        text = str(text)

        stripped = text.strip()

        words = re.findall(
            r"\b[\w'-]+\b",
            stripped
        )

        characters = len(text)

        letters = sum(
            char.isalpha()
            for char in text
        )

        digits = sum(
            char.isdigit()
            for char in text
        )

        spaces = sum(
            char.isspace()
            for char in text
        )

        uppercase = sum(
            char.isupper()
            for char in text
        )

        lowercase = sum(
            char.islower()
            for char in text
        )

        punctuation = sum(
            not char.isalnum()
            and not char.isspace()
            for char in text
        )

        return {

            "is_empty":
                stripped == "",

            "string_length":
                characters,

            "word_count":
                len(words),

            "unique_word_count":
                len(set(
                    word.lower()
                    for word in words
                )),

            "letter_count":
                letters,

            "digit_count":
                digits,

            "space_count":
                spaces,

            "uppercase_count":
                uppercase,

            "lowercase_count":
                lowercase,

            "punctuation_count":
                punctuation,

            "has_digits":
                digits > 0,

            "has_letters":
                letters > 0,

            "has_uppercase":
                uppercase > 0,

            "has_punctuation":
                punctuation > 0,

            "words":
                words[:50],

        }

    # ========================================================
    # NUMERIC FEATURES
    # ========================================================

    def _extract_numeric_features(self, value):

        try:

            numeric_value = float(value)

            finite = math.isfinite(
                numeric_value
            )

        except Exception:

            numeric_value = 0.0
            finite = False

        return {

            "is_empty": False,

            "is_numeric": True,

            "numeric_value":
                numeric_value,

            "is_integer":
                isinstance(value, int),

            "is_finite":
                finite,

            "is_positive":
                numeric_value > 0,

            "is_negative":
                numeric_value < 0,

            "is_zero":
                numeric_value == 0,

            "absolute_value":
                abs(numeric_value),

        }

    # ========================================================
    # COLLECTION FEATURES
    # ========================================================

    def _extract_collection_features(self, data):

        items = list(data)

        type_counts = Counter(
            type(item).__name__
            for item in items
        )

        features = {

            "is_empty":
                len(items) == 0,

            "size":
                len(items),

            "item_count":
                len(items),

            "unique_count":
                len(set(
                    repr(item)
                    for item in items
                )),

            "type_distribution":
                dict(type_counts),

            "has_duplicates":
                len(items)
                != len(set(
                    repr(item)
                    for item in items
                )),

        }

        numeric_values = [

            item

            for item in items

            if isinstance(
                item,
                (int, float)
            )

            and not isinstance(
                item,
                bool
            )
        ]

        if numeric_values:

            features.update(
                self._numeric_summary(
                    numeric_values
                )
            )

        string_values = [

            item

            for item in items

            if isinstance(
                item,
                str
            )
        ]

        if string_values:

            features.update(
                self._text_collection_summary(
                    string_values
                )
            )

        return features

    # ========================================================
    # NUMERIC COLLECTION SUMMARY
    # ========================================================

    def _numeric_summary(self, values):

        if not values:

            return {}

        try:

            values = [
                float(value)
                for value in values
                if math.isfinite(
                    float(value)
                )
            ]

            if not values:

                return {}

            total = sum(values)

            minimum = min(values)
            maximum = max(values)

            mean = total / len(values)

            variance = sum(
                (value - mean) ** 2
                for value in values
            ) / len(values)

            return {

                "numeric_min":
                    minimum,

                "numeric_max":
                    maximum,

                "numeric_sum":
                    total,

                "numeric_mean":
                    mean,

                "numeric_range":
                    maximum - minimum,

                "numeric_variance":
                    variance,

                "numeric_count":
                    len(values),

            }

        except Exception:

            return {}

    # ========================================================
    # TEXT COLLECTION SUMMARY
    # ========================================================

    def _text_collection_summary(self, values):

        if not values:

            return {}

        try:

            lengths = [
                len(str(value))
                for value in values
            ]

            words = []

            for value in values:

                words.extend(
                    re.findall(
                        r"\b[\w'-]+\b",
                        str(value)
                    )
                )

            return {

                "text_min_length":
                    min(lengths),

                "text_max_length":
                    max(lengths),

                "text_average_length":
                    sum(lengths)
                    / len(lengths),

                "text_total_words":
                    len(words),

                "text_unique_words":
                    len(set(
                        word.lower()
                        for word in words
                    )),

            }

        except Exception:

            return {}

    # ========================================================
    # MARKET FEATURE EXTRACTION
    # ========================================================

    def _extract_market_features(self, data):

        if not isinstance(data, dict):

            return {}

        features = {}

        market_keys = {

            "price",
            "close",
            "open",
            "high",
            "low",
            "volume",
            "rsi",
            "macd",
            "atr",
            "adx",
            "momentum",
            "roc",
            "vwap",
            "mfi",
            "cci",

        }

        available = []

        normalized_keys = {

            str(key).lower()

            for key in data.keys()

        }

        for key in market_keys:

            if key in normalized_keys:

                available.append(key)

        if available:

            features.update({

                "market_data_detected":
                    True,

                "market_features":
                    available,

                "market_feature_count":
                    len(available),

            })

        else:

            features.update({

                "market_data_detected":
                    False,

                "market_features":
                    [],

                "market_feature_count":
                    0,

            })

        # ----------------------------------------------------
        # OHLC detection
        # ----------------------------------------------------

        required_ohlc = {
            "open",
            "high",
            "low",
            "close",
        }

        if required_ohlc.issubset(
            normalized_keys
        ):

            features[
                "has_ohlc"
            ] = True

        else:

            features[
                "has_ohlc"
            ] = False

        # ----------------------------------------------------
        # Volume detection
        # ----------------------------------------------------

        features[
            "has_volume"
        ] = "volume" in normalized_keys

        return features

    # ========================================================
    # SEMANTIC KEY EXTRACTION
    # ========================================================

    def _extract_semantic_keys(self, data):

        if not isinstance(data, dict):

            return {}

        normalized = {

            str(key).lower():

            key

            for key in data.keys()

        }

        semantic = {

            "has_signal":
                "signal" in normalized,

            "has_pattern":
                "pattern" in normalized,

            "has_market":
                "market" in normalized,

            "has_domain":
                "domain" in normalized,

            "has_prediction":
                "prediction" in normalized,

            "has_reality":
                "reality" in normalized,

            "has_confidence":
                "confidence" in normalized,

            "has_timestamp":
                "timestamp" in normalized,

            "has_result":
                "result" in normalized,

        }

        return semantic

    # ========================================================
    # BATCH EXTRACTION
    # ========================================================

    def extract_many(self, datasets):

        if datasets is None:

            return []

        try:

            return [

                self.process(data)

                for data in datasets

            ]

        except Exception as e:

            logger.exception(
                "Batch feature extraction error: %s",
                e
            )

            return []

    # ========================================================
    # FEATURE NAMES
    # ========================================================

    def feature_names(self, data=None):

        if data is not None:

            features = self.process(
                data
            )

            return list(
                features.keys()
            )

        return list(
            self.last_features.keys()
        )

    # ========================================================
    # LAST FEATURES
    # ========================================================

    def get_last_features(self):

        return dict(
            self.last_features
        )

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.count = 0
        self.success_count = 0
        self.error_count = 0

        self.last_features = {}
        self.last_input_type = None

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        return {

            "name":
                self.name,

            "version":
                self.VERSION,

            "online":
                True,

            "count":
                self.count,

            "success":
                self.success_count,

            "errors":
                self.error_count,

            "last_input_type":
                self.last_input_type,

            "feature_count":
                len(
                    self.last_features
                ),

        }


# ============================================================
#
# BACKWARD COMPATIBILITY
#
# ============================================================

FeatureExtractorEngine = FeatureExtractor


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

extractor = FeatureExtractor()

