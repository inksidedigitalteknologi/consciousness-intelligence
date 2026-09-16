# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# DATA CLEANER
#
# Version: 2.0 Professional
#
# ============================================================
#
# PURPOSE
# ------------------------------------------------------------
# Central data-quality layer for the Intelligence OS.
#
# Responsibilities:
#
# - Remove invalid / empty values
# - Normalize dictionary keys
# - Clean nested dictionaries
# - Clean lists / tuples / sets
# - Normalize strings
# - Normalize numeric values
# - Remove NaN / Infinity
# - Preserve valid False / 0 values
# - Optional duplicate removal
# - Recursive cleaning
# - Data quality statistics
# - Validation
# - Safe processing
# - Backward compatibility
#
# Compatible with:
#
#   collector.py
#   context_manager.py
#   feature_extractor.py
#   normalizer.py
#   learning_memory.py
#   analyzer.py
#   evaluator.py
#   engine.py
#   knowledge_builder.py
#   semantic_memory.py
#   registry.py
#
# ============================================================

import logging
import math
from datetime import datetime
from collections import Counter

logger = logging.getLogger(__name__)


# ============================================================
# DATA CLEANER
# ============================================================

class DataCleaner:

    VERSION = "2.0"

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        remove_none=True,
        remove_empty=True,
        normalize_strings=True,
        normalize_keys=True,
        remove_nan=True,
        remove_infinity=True,
        recursive=True,
        remove_duplicates=False,
        max_depth=20,
    ):

        self.name = "cleaner"

        self.remove_none = remove_none
        self.remove_empty = remove_empty
        self.normalize_strings = normalize_strings
        self.normalize_keys = normalize_keys
        self.remove_nan = remove_nan
        self.remove_infinity = remove_infinity
        self.recursive = recursive
        self.remove_duplicates = remove_duplicates
        self.max_depth = max_depth

        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        self.process_count = 0
        self.success_count = 0
        self.error_count = 0

        self.values_processed = 0
        self.values_removed = 0
        self.values_normalized = 0
        self.duplicates_removed = 0

        self.dict_count = 0
        self.list_count = 0
        self.string_count = 0
        self.numeric_count = 0

        self.last_process = None
        self.last_error = None

        logger.info(
            "Data Cleaner v%s initialized.",
            self.VERSION
        )

    # ========================================================
    # MAIN PROCESS
    # ========================================================

    def process(self, data):

        self.process_count += 1

        self.last_process = datetime.now().isoformat()
        self.last_error = None

        try:

            cleaned = self._clean_value(
                data,
                depth=0
            )

            self.success_count += 1

            return cleaned

        except Exception as e:

            self.error_count += 1

            self.last_error = str(e)

            logger.exception(
                "Data Cleaner error: %s",
                e
            )

            # ------------------------------------------------
            # SAFETY
            # ------------------------------------------------
            #
            # Do not destroy original data if cleaning fails.
            #

            return data

    # ========================================================
    # BACKWARD COMPATIBILITY
    # ========================================================

    def clean(self, data):

        return self.process(data)

    # ========================================================
    # CORE CLEANING ENGINE
    # ========================================================

    def _clean_value(
        self,
        value,
        depth=0
    ):

        self.values_processed += 1

        # ----------------------------------------------------
        # DEPTH PROTECTION
        # ----------------------------------------------------

        if depth > self.max_depth:

            logger.warning(
                "Maximum cleaner depth reached."
            )

            return value

        # ----------------------------------------------------
        # NONE
        # ----------------------------------------------------

        if value is None:

            if self.remove_none:

                self.values_removed += 1

                return None

            return value

        # ----------------------------------------------------
        # BOOLEAN
        # ----------------------------------------------------

        if isinstance(value, bool):

            return value

        # ----------------------------------------------------
        # NUMBERS
        # ----------------------------------------------------

        if isinstance(
            value,
            (int, float)
        ):

            self.numeric_count += 1

            return self._clean_number(
                value
            )

        # ----------------------------------------------------
        # STRING
        # ----------------------------------------------------

        if isinstance(value, str):

            self.string_count += 1

            return self._clean_string(
                value
            )

        # ----------------------------------------------------
        # DICTIONARY
        # ----------------------------------------------------

        if isinstance(value, dict):

            self.dict_count += 1

            return self._clean_dict(
                value,
                depth
            )

        # ----------------------------------------------------
        # LIST
        # ----------------------------------------------------

        if isinstance(value, list):

            self.list_count += 1

            return self._clean_list(
                value,
                depth
            )

        # ----------------------------------------------------
        # TUPLE
        # ----------------------------------------------------

        if isinstance(value, tuple):

            cleaned = self._clean_list(
                list(value),
                depth
            )

            if cleaned is None:

                return ()

            return tuple(cleaned)

        # ----------------------------------------------------
        # SET
        # ----------------------------------------------------

        if isinstance(value, set):

            cleaned = self._clean_list(
                list(value),
                depth
            )

            if cleaned is None:

                return set()

            try:

                return set(cleaned)

            except Exception:

                return cleaned

        # ----------------------------------------------------
        # DATETIME
        # ----------------------------------------------------

        if isinstance(
            value,
            datetime
        ):

            return value.isoformat()

        # ----------------------------------------------------
        # UNKNOWN OBJECT
        # ----------------------------------------------------

        return value

    # ========================================================
    # NUMBER CLEANING
    # ========================================================

    def _clean_number(
        self,
        value
    ):

        try:

            # ------------------------------------------------
            # NAN
            # ------------------------------------------------

            if isinstance(
                value,
                float
            ):

                if math.isnan(value):

                    if self.remove_nan:

                        self.values_removed += 1

                        return None

                # --------------------------------------------
                # INFINITY
                # --------------------------------------------

                if math.isinf(value):

                    if self.remove_infinity:

                        self.values_removed += 1

                        return None

            return value

        except Exception:

            return value

    # ========================================================
    # STRING CLEANING
    # ========================================================

    def _clean_string(
        self,
        value
    ):

        if not isinstance(
            value,
            str
        ):

            return value

        original = value

        if self.normalize_strings:

            value = value.strip()

            # ----------------------------------------------
            # NORMALIZE WHITESPACE
            # ----------------------------------------------

            value = " ".join(
                value.split()
            )

        # ----------------------------------------------------
        # EMPTY STRING
        # ----------------------------------------------------

        if self.remove_empty:

            if value == "":

                self.values_removed += 1

                return None

        if value != original:

            self.values_normalized += 1

        return value

    # ========================================================
    # KEY CLEANING
    # ========================================================

    def _clean_key(
        self,
        key
    ):

        if not self.normalize_keys:

            return key

        if isinstance(
            key,
            str
        ):

            original = key

            key = key.strip()

            key = " ".join(
                key.split()
            )

            if key != original:

                self.values_normalized += 1

        return key

    # ========================================================
    # DICTIONARY CLEANING
    # ========================================================

    def _clean_dict(
        self,
        data,
        depth
    ):

        cleaned = {}

        for key, value in data.items():

            try:

                clean_key = self._clean_key(
                    key
                )

                clean_value = self._clean_value(
                    value,
                    depth + 1
                )

                # --------------------------------------------
                # REMOVE INVALID VALUE
                # --------------------------------------------

                if clean_value is None:

                    if self.remove_none:

                        continue

                # --------------------------------------------
                # REMOVE EMPTY CONTAINERS
                # --------------------------------------------

                if self.remove_empty:

                    if self._is_empty_container(
                        clean_value
                    ):

                        self.values_removed += 1

                        continue

                cleaned[clean_key] = clean_value

            except Exception as e:

                logger.debug(
                    "Dictionary value cleaning failed: %s",
                    e
                )

                # --------------------------------------------
                # PRESERVE ORIGINAL VALUE
                # --------------------------------------------

                cleaned[key] = value

        return cleaned

    # ========================================================
    # LIST CLEANING
    # ========================================================

    def _clean_list(
        self,
        data,
        depth
    ):

        cleaned = []

        for item in data:

            try:

                clean_item = self._clean_value(
                    item,
                    depth + 1
                )

                # --------------------------------------------
                # REMOVE NONE
                # --------------------------------------------

                if clean_item is None:

                    if self.remove_none:

                        continue

                # --------------------------------------------
                # REMOVE EMPTY
                # --------------------------------------------

                if self.remove_empty:

                    if self._is_empty_container(
                        clean_item
                    ):

                        self.values_removed += 1

                        continue

                cleaned.append(
                    clean_item
                )

            except Exception as e:

                logger.debug(
                    "List item cleaning failed: %s",
                    e
                )

                cleaned.append(
                    item
                )

        # ----------------------------------------------------
        # DUPLICATE REMOVAL
        # ----------------------------------------------------

        if self.remove_duplicates:

            cleaned = self._remove_duplicates(
                cleaned
            )

        return cleaned

    # ========================================================
    # EMPTY DETECTION
    # ========================================================

    def _is_empty_container(
        self,
        value
    ):

        if value is None:

            return True

        if isinstance(
            value,
            str
        ):

            return value == ""

        if isinstance(
            value,
            (list, tuple, set, dict)
        ):

            return len(value) == 0

        return False

    # ========================================================
    # DUPLICATE REMOVAL
    # ========================================================

    def _remove_duplicates(
        self,
        values
    ):

        result = []

        seen = set()

        for value in values:

            try:

                marker = self._make_hashable(
                    value
                )

                if marker in seen:

                    self.duplicates_removed += 1

                    continue

                seen.add(
                    marker
                )

                result.append(
                    value
                )

            except Exception:

                result.append(
                    value
                )

        return result

    # ========================================================
    # HASHABLE REPRESENTATION
    # ========================================================

    def _make_hashable(
        self,
        value
    ):

        if isinstance(
            value,
            dict
        ):

            return tuple(
                sorted(
                    (
                        str(k),
                        self._make_hashable(v)
                    )
                    for k, v in value.items()
                )
            )

        if isinstance(
            value,
            list
        ):

            return tuple(
                self._make_hashable(v)
                for v in value
            )

        if isinstance(
            value,
            tuple
        ):

            return tuple(
                self._make_hashable(v)
                for v in value
            )

        if isinstance(
            value,
            set
        ):

            return tuple(
                sorted(
                    self._make_hashable(v)
                    for v in value
                )
            )

        try:

            hash(value)

            return value

        except Exception:

            return repr(value)

    # ========================================================
    # VALIDATION
    # ========================================================

    def validate(
        self,
        data
    ):

        issues = []

        self._validate_value(
            data,
            issues,
            path="root",
            depth=0
        )

        return {

            "valid":
                len(issues) == 0,

            "issues":
                issues,

            "issue_count":
                len(issues),

        }

    # ========================================================
    # VALIDATION ENGINE
    # ========================================================

    def _validate_value(
        self,
        value,
        issues,
        path,
        depth
    ):

        if depth > self.max_depth:

            issues.append(
                f"Maximum depth exceeded at {path}"
            )

            return

        # ----------------------------------------------------
        # NONE
        # ----------------------------------------------------

        if value is None:

            issues.append(
                f"None value at {path}"
            )

            return

        # ----------------------------------------------------
        # NUMBER
        # ----------------------------------------------------

        if isinstance(
            value,
            float
        ):

            if math.isnan(value):

                issues.append(
                    f"NaN value at {path}"
                )

            elif math.isinf(value):

                issues.append(
                    f"Infinity value at {path}"
                )

            return

        # ----------------------------------------------------
        # DICT
        # ----------------------------------------------------

        if isinstance(
            value,
            dict
        ):

            for key, item in value.items():

                key_path = (
                    f"{path}.{key}"
                )

                self._validate_value(
                    item,
                    issues,
                    key_path,
                    depth + 1
                )

            return

        # ----------------------------------------------------
        # LIST
        # ----------------------------------------------------

        if isinstance(
            value,
            (list, tuple, set)
        ):

            for index, item in enumerate(
                value
            ):

                self._validate_value(
                    item,
                    issues,
                    f"{path}[{index}]",
                    depth + 1
                )

    # ========================================================
    # CLEAN + VALIDATE
    # ========================================================

    def clean_and_validate(
        self,
        data
    ):

        cleaned = self.process(
            data
        )

        validation = self.validate(
            cleaned
        )

        return {

            "data":
                cleaned,

            "valid":
                validation["valid"],

            "issues":
                validation["issues"],

        }

    # ========================================================
    # DATA QUALITY SCORE
    # ========================================================

    def quality_score(
        self,
        data
    ):

        validation = self.validate(
            data
        )

        issues = validation["issue_count"]

        if issues == 0:

            return 100.0

        # ----------------------------------------------------
        # Score decreases gradually.
        # ----------------------------------------------------

        score = max(
            0.0,
            100.0 - (
                issues * 10
            )
        )

        return round(
            score,
            2
        )

    # ========================================================
    # BATCH CLEANING
    # ========================================================

    def clean_batch(
        self,
        items
    ):

        if items is None:

            return []

        if not isinstance(
            items,
            (list, tuple)
        ):

            return [
                self.process(items)
            ]

        return [

            self.process(item)

            for item in items

        ]

    # ========================================================
    # DATA SUMMARY
    # ========================================================

    def summarize(
        self,
        data
    ):

        summary = {

            "type":
                type(data).__name__,

            "size":
                self._get_size(data),

            "quality":
                self.quality_score(data),

        }

        if isinstance(
            data,
            dict
        ):

            summary["keys"] = len(
                data
            )

        elif isinstance(
            data,
            (list, tuple, set)
        ):

            summary["items"] = len(
                data
            )

        return summary

    # ========================================================
    # SIZE
    # ========================================================

    def _get_size(
        self,
        data
    ):

        try:

            if isinstance(
                data,
                (dict, list, tuple, set, str)
            ):

                return len(data)

        except Exception:

            pass

        return 1

    # ========================================================
    # RESET STATISTICS
    # ========================================================

    def reset_stats(
        self
    ):

        self.process_count = 0
        self.success_count = 0
        self.error_count = 0

        self.values_processed = 0
        self.values_removed = 0
        self.values_normalized = 0
        self.duplicates_removed = 0

        self.dict_count = 0
        self.list_count = 0
        self.string_count = 0
        self.numeric_count = 0

        self.last_process = None
        self.last_error = None

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        success_rate = 0.0

        if self.process_count > 0:

            success_rate = (
                self.success_count
                /
                self.process_count
            ) * 100

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

            "success_rate":
                round(
                    success_rate,
                    2
                ),

            "values_processed":
                self.values_processed,

            "values_removed":
                self.values_removed,

            "values_normalized":
                self.values_normalized,

            "duplicates_removed":
                self.duplicates_removed,

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

            "configuration": {

                "remove_none":
                    self.remove_none,

                "remove_empty":
                    self.remove_empty,

                "normalize_strings":
                    self.normalize_strings,

                "normalize_keys":
                    self.normalize_keys,

                "remove_nan":
                    self.remove_nan,

                "remove_infinity":
                    self.remove_infinity,

                "recursive":
                    self.recursive,

                "remove_duplicates":
                    self.remove_duplicates,

                "max_depth":
                    self.max_depth,

            }

        }


# ============================================================
# GLOBAL INSTANCE
# ============================================================

cleaner = DataCleaner()


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

DataCleanerEngine = DataCleaner