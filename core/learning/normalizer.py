
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# NORMALIZER ENGINE
#
# Version: 2.0 Professional
#
# PURPOSE:
# Standardize data before entering the Intelligence Pipeline.
#
# PIPELINE:
#
# Collector
#     ↓
# DataCleaner
#     ↓
# Normalizer
#     ↓
# FeatureExtractor
#     ↓
# EntityRecognition
#     ↓
# SemanticProcessor
#     ↓
# Analyzer
#     ↓
# Reasoning
#     ↓
# Learning
#
# ============================================================

import logging
import math
import re

from datetime import datetime, date
from decimal import Decimal


logger = logging.getLogger(__name__)


# ============================================================
# NORMALIZER
# ============================================================

class Normalizer:

    VERSION = "2.0"

    def __init__(self):

        self.name = "normalizer"

        # Statistics
        self.process_count = 0
        self.success_count = 0
        self.error_count = 0

        self.dict_count = 0
        self.list_count = 0
        self.string_count = 0
        self.numeric_count = 0

        self.last_process = None
        self.last_error = None

        logger.info(
            "Normalizer v%s initialized.",
            self.VERSION
        )

    # ========================================================
    # MAIN PROCESS
    # ========================================================

    def process(self, data):

        self.process_count += 1

        self.last_process = datetime.now().isoformat()

        try:

            if data is None:

                self.success_count += 1

                return {}

            result = self._normalize_value(data)

            self.success_count += 1

            return result

        except Exception as e:

            self.error_count += 1

            self.last_error = str(e)

            logger.exception(
                "Normalizer error: %s",
                e
            )

            # Never destroy the original data
            return data

    # ========================================================
    # PUBLIC ALIAS
    # ========================================================

    def normalize(self, data):

        return self.process(data)

    # ========================================================
    # VALUE NORMALIZATION
    # ========================================================

    def _normalize_value(self, value):

        # ----------------------------------------------------
        # None
        # ----------------------------------------------------

        if value is None:

            return None

        # ----------------------------------------------------
        # Dictionary
        # ----------------------------------------------------

        if isinstance(value, dict):

            self.dict_count += 1

            return self._normalize_dict(value)

        # ----------------------------------------------------
        # List
        # ----------------------------------------------------

        if isinstance(value, list):

            self.list_count += 1

            return [
                self._normalize_value(item)
                for item in value
            ]

        # ----------------------------------------------------
        # Tuple
        # ----------------------------------------------------

        if isinstance(value, tuple):

            self.list_count += 1

            return tuple(
                self._normalize_value(item)
                for item in value
            )

        # ----------------------------------------------------
        # Set
        # ----------------------------------------------------

        if isinstance(value, set):

            return {
                self._normalize_value(item)
                for item in value
            }

        # ----------------------------------------------------
        # String
        # ----------------------------------------------------

        if isinstance(value, str):

            self.string_count += 1

            return self._normalize_string(value)

        # ----------------------------------------------------
        # Boolean
        # ----------------------------------------------------

        if isinstance(value, bool):

            return value

        # ----------------------------------------------------
        # Numeric
        # ----------------------------------------------------

        if isinstance(
            value,
            (int, float, Decimal)
        ):

            self.numeric_count += 1

            return self._normalize_numeric(value)

        # ----------------------------------------------------
        # Datetime
        # ----------------------------------------------------

        if isinstance(value, datetime):

            return value.isoformat()

        # ----------------------------------------------------
        # Date
        # ----------------------------------------------------

        if isinstance(value, date):

            return value.isoformat()

        # ----------------------------------------------------
        # Unknown object
        # ----------------------------------------------------

        return value

    # ========================================================
    # DICTIONARY NORMALIZATION
    # ========================================================

    def _normalize_dict(self, data):

        result = {}

        for key, value in data.items():

            normalized_key = self._normalize_key(key)

            normalized_value = self._normalize_value(value)

            result[normalized_key] = normalized_value

        return result

    # ========================================================
    # KEY NORMALIZATION
    # ========================================================

    def _normalize_key(self, key):

        if key is None:

            return ""

        key = str(key).strip()

        # Convert spaces to underscores
        key = re.sub(
            r"\s+",
            "_",
            key
        )

        # Remove dangerous control characters
        key = re.sub(
            r"[\x00-\x1f\x7f]",
            "",
            key
        )

        return key

    # ========================================================
    # STRING NORMALIZATION
    # ========================================================

    def _normalize_string(self, value):

        if value is None:

            return ""

        # Remove leading/trailing spaces
        value = value.strip()

        # Normalize repeated whitespace
        value = re.sub(
            r"\s+",
            " ",
            value
        )

        # Remove control characters
        value = re.sub(
            r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]",
            "",
            value
        )

        # Empty string
        if value == "":

            return ""

        return value

    # ========================================================
    # NUMERIC NORMALIZATION
    # ========================================================

    def _normalize_numeric(self, value):

        try:

            # Preserve booleans
            if isinstance(value, bool):

                return value

            # Decimal → float
            if isinstance(value, Decimal):

                value = float(value)

            # Handle NaN / Infinity
            if isinstance(value, float):

                if math.isnan(value):

                    return None

                if math.isinf(value):

                    return None

            return value

        except Exception:

            return value

    # ========================================================
    # MARKET DATA NORMALIZATION
    # ========================================================

    def normalize_market(self, data):

        """
        Normalize common trading / market fields.

        Does NOT calculate indicators.
        Does NOT modify trading logic.
        """

        if not isinstance(data, dict):

            return self.process(data)

        result = self.process(data)

        # ----------------------------------------------------
        # SYMBOL / PAIR
        # ----------------------------------------------------

        for field in (
            "pair",
            "symbol",
            "market"
        ):

            if field in result:

                result[field] = self._normalize_symbol(
                    result[field]
                )

        # ----------------------------------------------------
        # SIGNAL
        # ----------------------------------------------------

        if "signal" in result:

            result["signal"] = self._normalize_signal(
                result["signal"]
            )

        # ----------------------------------------------------
        # TIMEFRAME
        # ----------------------------------------------------

        if "timeframe" in result:

            result["timeframe"] = self._normalize_timeframe(
                result["timeframe"]
            )

        return result

    # ========================================================
    # SYMBOL NORMALIZATION
    # ========================================================

    def _normalize_symbol(self, value):

        if value is None:

            return value

        value = str(value).strip().upper()

        # Common separator normalization
        value = value.replace(
            "-",
            "/"
        )

        value = value.replace(
            "_",
            "/"
        )

        return value

    # ========================================================
    # SIGNAL NORMALIZATION
    # ========================================================

    def _normalize_signal(self, value):

        if value is None:

            return value

        value = str(value).strip().upper()

        aliases = {

            "LONG": "BUY",

            "SHORT": "SELL",

            "BULL": "BUY",

            "BULLISH": "BUY",

            "BEAR": "SELL",

            "BEARISH": "SELL",

            "NEUTRAL": "HOLD",

            "WAIT": "HOLD",

            "NONE": "HOLD",

        }

        return aliases.get(
            value,
            value
        )

    # ========================================================
    # TIMEFRAME NORMALIZATION
    # ========================================================

    def _normalize_timeframe(self, value):

        if value is None:

            return value

        value = str(value).strip().lower()

        aliases = {

            "1min": "1m",

            "1minute": "1m",

            "5min": "5m",

            "5minute": "5m",

            "15min": "15m",

            "15minute": "15m",

            "30min": "30m",

            "30minute": "30m",

            "1hour": "1h",

            "1hr": "1h",

            "60m": "1h",

            "4hour": "4h",

            "4hr": "4h",

            "240m": "4h",

            "1day": "1d",

            "1daily": "1d",

            "24h": "1d",

        }

        return aliases.get(
            value,
            value
        )

    # ========================================================
    # TEXT NORMALIZATION
    # ========================================================

    def normalize_text(self, text):

        if text is None:

            return ""

        return self._normalize_string(
            str(text)
        )

    # ========================================================
    # LIST NORMALIZATION
    # ========================================================

    def normalize_list(self, data):

        if data is None:

            return []

        if not isinstance(
            data,
            (list, tuple, set)
        ):

            data = [data]

        return [
            self._normalize_value(item)
            for item in data
        ]

    # ========================================================
    # BATCH NORMALIZATION
    # ========================================================

    def normalize_batch(self, items):

        if items is None:

            return []

        return [
            self.process(item)
            for item in items
        ]

    # ========================================================
    # REMOVE EMPTY VALUES
    # ========================================================

    def remove_empty(self, data):

        """
        Remove empty values without modifying
        the original object.
        """

        if isinstance(data, dict):

            result = {}

            for key, value in data.items():

                cleaned = self.remove_empty(value)

                if cleaned in (
                    None,
                    "",
                    [],
                    {},
                    ()
                ):

                    continue

                result[key] = cleaned

            return result

        if isinstance(data, list):

            result = []

            for item in data:

                cleaned = self.remove_empty(item)

                if cleaned in (
                    None,
                    "",
                    [],
                    {},
                    ()
                ):

                    continue

                result.append(cleaned)

            return result

        if isinstance(data, tuple):

            return tuple(
                self.remove_empty(item)
                for item in data
            )

        return data

    # ========================================================
    # FLATTEN DATA
    # ========================================================

    def flatten(self, data, prefix=""):

        """
        Convert nested dictionary into flat dictionary.

        Example:

        {
            "market": {
                "price": 100
            }
        }

        becomes:

        {
            "market.price": 100
        }
        """

        result = {}

        if not isinstance(data, dict):

            return result

        for key, value in data.items():

            full_key = (
                f"{prefix}.{key}"
                if prefix
                else str(key)
            )

            if isinstance(value, dict):

                result.update(
                    self.flatten(
                        value,
                        full_key
                    )
                )

            else:

                result[full_key] = value

        return result

    # ========================================================
    # TIMESTAMP NORMALIZATION
    # ========================================================

    def normalize_timestamp(self, value):

        if value is None:

            return None

        if isinstance(
            value,
            datetime
        ):

            return value.isoformat()

        if isinstance(
            value,
            date
        ):

            return value.isoformat()

        if isinstance(value, str):

            value = value.strip()

            if not value:

                return None

            return value

        return value

    # ========================================================
    # CREATE STANDARD RECORD
    # ========================================================

    def standard_record(
        self,
        data,
        source="unknown",
        domain="general"
    ):

        normalized = self.process(
            data
        )

        return {

            "source":
                self.normalize_text(
                    source
                ),

            "domain":
                self.normalize_text(
                    domain
                ),

            "data":
                normalized,

            "timestamp":
                datetime.now().isoformat(),

        }

    # ========================================================
    # VALIDATE NORMALIZED DATA
    # ========================================================

    def validate(self, data):

        result = {

            "valid": True,

            "type":
                type(data).__name__,

            "errors": [],

        }

        if data is None:

            result["valid"] = False

            result["errors"].append(
                "data_is_none"
            )

            return result

        if isinstance(data, dict):

            for key in data.keys():

                if key is None:

                    result["valid"] = False

                    result["errors"].append(
                        "null_key"
                    )

        return result

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

            "process_count":
                self.process_count,

            "success_count":
                self.success_count,

            "error_count":
                self.error_count,

            "dict_count":
                self.dict_count,

            "list_count":
                self.list_count,

            "string_count":
                self.string_count,

            "numeric_count":
                self.numeric_count,

            "last_process":
                self.last_process,

            "last_error":
                self.last_error,

        }

    # ========================================================
    # RESET STATISTICS
    # ========================================================

    def reset_statistics(self):

        self.process_count = 0
        self.success_count = 0
        self.error_count = 0

        self.dict_count = 0
        self.list_count = 0
        self.string_count = 0
        self.numeric_count = 0

        self.last_process = None
        self.last_error = None

        logger.info(
            "Normalizer statistics reset."
        )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

DataNormalizer = Normalizer


# ============================================================
# GLOBAL INSTANCE
# ============================================================

normalizer = Normalizer()


# ============================================================
# OPTIONAL MODULE FUNCTIONS
# ============================================================

def normalize(data):

    return normalizer.normalize(data)


def normalize_market(data):

    return normalizer.normalize_market(data)


def normalize_text(text):

    return normalizer.normalize_text(text)


def normalize_batch(items):

    return normalizer.normalize_batch(items)

