
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SERIALIZER
#
# Version: 2.0
#
# Production Safe Data Serialization Infrastructure
#
# ============================================================
#
# RESPONSIBILITIES
#
# - Convert arbitrary Python objects to JSON-safe structures
# - Prevent circular reference crashes
# - Handle dataclass safely
# - Handle datetime / date / time / timedelta
# - Handle Decimal
# - Handle Enum
# - Handle UUID
# - Handle Path
# - Handle bytes / bytearray / memoryview
# - Handle set / frozenset / tuple
# - Handle Mapping / iterable objects
# - Handle custom objects
# - Handle __dict__ / __slots__
# - Respect custom to_dict()
# - Respect custom to_json()
# - Limit recursion depth
# - Limit collection size
# - Limit string size
# - Limit dictionary key size
# - Protect against malformed objects
# - Protect against circular structures
# - Protect against NaN / Infinity
# - Support deterministic serialization
# - Support JSON string serialization
# - Support atomic JSON file writing
# - Support safe JSON loading
# - Support optional backup
# - Maintain runtime statistics
# - Never crash the Learning Engine
#
# ============================================================

from __future__ import annotations

import base64
import json
import logging
import math
import os
import threading

from collections.abc import Iterable, Mapping
from dataclasses import fields, is_dataclass
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID


logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

SERIALIZER_VERSION = "2.0"
API_VERSION = "2.0"


# ============================================================
#
# CONFIGURATION
#
# ============================================================

DEFAULT_MAX_DEPTH = 20
DEFAULT_MAX_ITEMS = 10000
DEFAULT_MAX_STRING_LENGTH = 100000
DEFAULT_MAX_KEY_LENGTH = 10000
DEFAULT_MAX_FILE_SIZE = 50 * 1024 * 1024

DEFAULT_INDENT = 2

# When bytes cannot reasonably be represented as UTF-8,
# base64 is used instead of exposing Python's b'...' repr.
BYTES_ENCODING = "base64"

# ============================================================
#
# MARKERS
#
# ============================================================

CIRCULAR_REFERENCE_MARKER = "[CIRCULAR_REFERENCE]"
MAX_DEPTH_MARKER = "[MAX_DEPTH]"
MAX_ITEMS_MARKER = "[MAX_ITEMS]"
UNSERIALIZABLE_MARKER = "[UNSERIALIZABLE]"
INVALID_OBJECT_MARKER = "[INVALID_OBJECT]"
INVALID_KEY_MARKER = "[INVALID_KEY]"
TRUNCATED_MARKER = "[TRUNCATED]"
FILE_TOO_LARGE_MARKER = "[FILE_TOO_LARGE]"


# ============================================================
#
# SERIALIZATION RESULT TYPES
#
# ============================================================

TYPE_MARKER = "__type__"
MODULE_MARKER = "__module__"
VALUE_MARKER = "__value__"
DATA_MARKER = "data"


# ============================================================
#
# SAFE SERIALIZER
#
# ============================================================

class SafeSerializer:
    """
    Production-safe serializer for the INKSIDE Intelligence OS.

    The serializer is deliberately independent from the Learning
    Engine. Any module can use it without introducing a dependency
    on the engine itself.

    Design principles:

    1. Never allow serialization failures to crash the caller.
    2. Preserve as much useful information as possible.
    3. Detect circular references.
    4. Prevent unbounded recursion.
    5. Prevent enormous collections.
    6. Normalize non-JSON Python types.
    7. Keep file writes atomic.
    8. Remain deterministic when requested.
    """

    def __init__(
        self,
        max_depth: int = DEFAULT_MAX_DEPTH,
        max_items: int = DEFAULT_MAX_ITEMS,
        max_string_length: int = DEFAULT_MAX_STRING_LENGTH,
        max_key_length: int = DEFAULT_MAX_KEY_LENGTH,
        max_file_size: int = DEFAULT_MAX_FILE_SIZE,
    ) -> None:

        self.max_depth = max(
            1,
            int(max_depth)
        )

        self.max_items = max(
            1,
            int(max_items)
        )

        self.max_string_length = max(
            100,
            int(max_string_length)
        )

        self.max_key_length = max(
            10,
            int(max_key_length)
        )

        self.max_file_size = max(
            1024,
            int(max_file_size)
        )

        self._lock = threading.RLock()

        self._stats = {
            "sanitize_calls": 0,
            "sanitize_success": 0,
            "sanitize_errors": 0,
            "objects_processed": 0,
            "circular_references": 0,
            "max_depth_hits": 0,
            "max_items_hits": 0,
            "strings_truncated": 0,
            "objects_with_to_dict": 0,
            "objects_with_to_json": 0,
            "dataclasses_processed": 0,
            "bytes_processed": 0,
            "fallback_objects": 0,
            "file_writes": 0,
            "file_write_errors": 0,
            "file_loads": 0,
            "file_load_errors": 0,
        }

        logger.info(
            "SafeSerializer v%s initialized.",
            SERIALIZER_VERSION
        )

    # ========================================================
    #
    # PUBLIC SANITIZE
    #
    # ========================================================

    def sanitize(
        self,
        value: Any
    ) -> Any:
        """
        Convert arbitrary Python data into a JSON-safe structure.

        This method is deliberately defensive. Any unexpected
        internal error results in a safe fallback object instead
        of propagating the exception to the Learning Engine.
        """

        with self._lock:
            self._stats["sanitize_calls"] += 1

        try:

            result = self._sanitize(
                value=value,
                depth=0,
                seen=set()
            )

            with self._lock:
                self._stats["sanitize_success"] += 1

            return result

        except Exception as exc:

            with self._lock:
                self._stats["sanitize_errors"] += 1

            logger.exception(
                "Serialization failed: %s",
                exc
            )

            return {
                TYPE_MARKER: type(value).__name__,
                VALUE_MARKER: UNSERIALIZABLE_MARKER,
                "error": str(exc),
            }

    # ========================================================
    #
    # INTERNAL SANITIZER
    #
    # ========================================================

    def _sanitize(
        self,
        value: Any,
        depth: int,
        seen: set[int]
    ) -> Any:

        # ----------------------------------------------------
        # DEPTH PROTECTION
        # ----------------------------------------------------

        if depth > self.max_depth:

            with self._lock:
                self._stats["max_depth_hits"] += 1

            return MAX_DEPTH_MARKER

        # ----------------------------------------------------
        # NONE
        # ----------------------------------------------------

        if value is None:
            return None

        # ----------------------------------------------------
        # BOOL
        # ----------------------------------------------------

        if isinstance(value, bool):
            return value

        # ----------------------------------------------------
        # INTEGER
        # ----------------------------------------------------

        if isinstance(value, int):
            return value

        # ----------------------------------------------------
        # FLOAT
        # ----------------------------------------------------

        if isinstance(value, float):

            if math.isnan(value):
                return None

            if math.isinf(value):

                if value > 0:
                    return "Infinity"

                return "-Infinity"

            return value

        # ----------------------------------------------------
        # DECIMAL
        # ----------------------------------------------------

        if isinstance(value, Decimal):

            if not value.is_finite():
                return str(value)

            return float(value)

        # ----------------------------------------------------
        # STRING
        # ----------------------------------------------------

        if isinstance(value, str):

            return self._sanitize_string(
                value
            )

        # ----------------------------------------------------
        # BYTES
        # ----------------------------------------------------

        if isinstance(
            value,
            (
                bytes,
                bytearray,
                memoryview
            )
        ):

            return self._sanitize_bytes(
                value
            )

        # ----------------------------------------------------
        # DATETIME / DATE / TIME
        # ----------------------------------------------------

        if isinstance(
            value,
            (
                datetime,
                date,
                time
            )
        ):

            return value.isoformat()

        # ----------------------------------------------------
        # TIMEDELTA
        # ----------------------------------------------------

        if isinstance(
            value,
            timedelta
        ):

            return {
                TYPE_MARKER: "timedelta",
                "total_seconds": value.total_seconds(),
            }

        # ----------------------------------------------------
        # UUID
        # ----------------------------------------------------

        if isinstance(value, UUID):

            return str(value)

        # ----------------------------------------------------
        # PATH
        # ----------------------------------------------------

        if isinstance(value, Path):

            return str(value)

        # ----------------------------------------------------
        # ENUM
        # ----------------------------------------------------

        if isinstance(value, Enum):

            return self._sanitize_enum(
                value,
                depth,
                seen
            )

        # ----------------------------------------------------
        # DATACLASS
        # ----------------------------------------------------

        if is_dataclass(value) and not isinstance(
            value,
            type
        ):

            return self._sanitize_dataclass(
                value,
                depth,
                seen
            )

        # ----------------------------------------------------
        # DICT / MAPPING
        # ----------------------------------------------------

        if isinstance(
            value,
            Mapping
        ):

            return self._sanitize_mapping(
                value,
                depth,
                seen
            )

        # ----------------------------------------------------
        # LIST
        # ----------------------------------------------------

        if isinstance(value, list):

            return self._sanitize_sequence(
                value,
                depth,
                seen,
                sequence_type="list"
            )

        # ----------------------------------------------------
        # TUPLE
        # ----------------------------------------------------

        if isinstance(value, tuple):

            return self._sanitize_sequence(
                value,
                depth,
                seen,
                sequence_type="tuple"
            )

        # ----------------------------------------------------
        # SET
        # ----------------------------------------------------

        if isinstance(value, set):

            return self._sanitize_sequence(
                value,
                depth,
                seen,
                sequence_type="set"
            )

        # ----------------------------------------------------
        # FROZENSET
        # ----------------------------------------------------

        if isinstance(value, frozenset):

            return self._sanitize_sequence(
                value,
                depth,
                seen,
                sequence_type="frozenset"
            )

        # ----------------------------------------------------
        # GENERIC ITERABLE
        #
        # Strings and known collections have already been
        # handled above.
        # ----------------------------------------------------

        if self._is_safe_iterable(value):

            return self._sanitize_iterable(
                value,
                depth,
                seen
            )

        # ----------------------------------------------------
        # CUSTOM OBJECT
        # ----------------------------------------------------

        return self._sanitize_object(
            value=value,
            depth=depth,
            seen=seen
        )

    # ========================================================
    #
    # STRING
    #
    # ========================================================

    def _sanitize_string(
        self,
        value: str
    ) -> str:

        if len(value) <= self.max_string_length:
            return value

        with self._lock:
            self._stats["strings_truncated"] += 1

        return (
            value[:self.max_string_length]
            + TRUNCATED_MARKER
        )

    # ========================================================
    #
    # BYTES
    #
    # ========================================================

    def _sanitize_bytes(
        self,
        value: bytes | bytearray | memoryview
    ) -> Any:

        with self._lock:
            self._stats["bytes_processed"] += 1

        try:

            raw = bytes(value)

            try:

                decoded = raw.decode(
                    "utf-8"
                )

                return decoded

            except UnicodeDecodeError:

                encoded = base64.b64encode(
                    raw
                ).decode("ascii")

                return {
                    TYPE_MARKER: "bytes",
                    "encoding": BYTES_ENCODING,
                    "value": encoded,
                }

        except Exception as exc:

            return {
                TYPE_MARKER: "bytes",
                VALUE_MARKER: UNSERIALIZABLE_MARKER,
                "error": str(exc),
            }

    # ========================================================
    #
    # ENUM
    #
    # ========================================================

    def _sanitize_enum(
        self,
        value: Enum,
        depth: int,
        seen: set[int]
    ) -> dict[str, Any]:

        try:

            return {
                TYPE_MARKER:
                    type(value).__name__,

                MODULE_MARKER:
                    type(value).__module__,

                "name":
                    value.name,

                "value":
                    self._sanitize(
                        value.value,
                        depth + 1,
                        seen
                    ),
            }

        except Exception:

            return {
                TYPE_MARKER:
                    type(value).__name__,

                VALUE_MARKER:
                    str(value),
            }

    # ========================================================
    #
    # DATACLASS
    # ========================================================

    def _sanitize_dataclass(
        self,
        value: Any,
        depth: int,
        seen: set[int]
    ) -> Any:

        object_id = id(value)

        if object_id in seen:

            with self._lock:
                self._stats["circular_references"] += 1

            return CIRCULAR_REFERENCE_MARKER

        seen.add(object_id)

        with self._lock:
            self._stats["dataclasses_processed"] += 1

        try:

            result = {
                TYPE_MARKER:
                    type(value).__name__,

                MODULE_MARKER:
                    type(value).__module__,

                DATA_MARKER: {}
            }

            for field_info in fields(value):

                try:

                    raw_value = getattr(
                        value,
                        field_info.name
                    )

                    result[DATA_MARKER][
                        field_info.name
                    ] = self._sanitize(
                        raw_value,
                        depth + 1,
                        seen
                    )

                except Exception as exc:

                    result[DATA_MARKER][
                        field_info.name
                    ] = {
                        VALUE_MARKER:
                            UNSERIALIZABLE_MARKER,
                        "error":
                            str(exc),
                    }

            return result

        finally:

            seen.discard(object_id)

    # ========================================================
    #
    # MAPPING
    #
    # ========================================================

    def _sanitize_mapping(
        self,
        value: Mapping,
        depth: int,
        seen: set[int]
    ) -> dict[str, Any]:

        object_id = id(value)

        if object_id in seen:

            with self._lock:
                self._stats["circular_references"] += 1

            return CIRCULAR_REFERENCE_MARKER

        seen.add(object_id)

        try:

            result: dict[str, Any] = {}

            count = 0

            for key, item in value.items():

                if count >= self.max_items:

                    with self._lock:
                        self._stats["max_items_hits"] += 1

                    result[
                        "__truncated__"
                    ] = True

                    result[
                        "__reason__"
                    ] = MAX_ITEMS_MARKER

                    break

                safe_key = self._sanitize_key(
                    key
                )

                # Avoid accidental collision caused by
                # converting non-string dictionary keys.
                safe_key = self._unique_key(
                    result,
                    safe_key
                )

                result[safe_key] = self._sanitize(
                    item,
                    depth + 1,
                    seen
                )

                count += 1

            return result

        except Exception as exc:

            return {
                TYPE_MARKER:
                    type(value).__name__,

                VALUE_MARKER:
                    UNSERIALIZABLE_MARKER,

                "error":
                    str(exc),
            }

        finally:

            seen.discard(object_id)

    # ========================================================
    #
    # SEQUENCE
    #
    # ========================================================

    def _sanitize_sequence(
        self,
        value: Any,
        depth: int,
        seen: set[int],
        sequence_type: str
    ) -> list[Any]:

        object_id = id(value)

        if object_id in seen:

            with self._lock:
                self._stats["circular_references"] += 1

            return [CIRCULAR_REFERENCE_MARKER]

        seen.add(object_id)

        try:

            result = []

            for index, item in enumerate(value):

                if index >= self.max_items:

                    with self._lock:
                        self._stats["max_items_hits"] += 1

                    result.append(
                        MAX_ITEMS_MARKER
                    )

                    break

                result.append(
                    self._sanitize(
                        item,
                        depth + 1,
                        seen
                    )
                )

            # Sets are unordered. Sorting their serialized
            # representation makes output deterministic.
            if sequence_type in (
                "set",
                "frozenset"
            ):

                try:

                    result.sort(
                        key=lambda item:
                            json.dumps(
                                item,
                                ensure_ascii=False,
                                sort_keys=True,
                                default=str
                            )
                    )

                except Exception:
                    pass

            return result

        finally:

            seen.discard(object_id)

    # ========================================================
    #
    # GENERIC ITERABLE
    #
    # ========================================================

    def _sanitize_iterable(
        self,
        value: Any,
        depth: int,
        seen: set[int]
    ) -> list[Any]:

        object_id = id(value)

        if object_id in seen:

            with self._lock:
                self._stats["circular_references"] += 1

            return [CIRCULAR_REFERENCE_MARKER]

        seen.add(object_id)

        try:

            result = []

            iterator = iter(value)

            for index, item in enumerate(iterator):

                if index >= self.max_items:

                    with self._lock:
                        self._stats["max_items_hits"] += 1

                    result.append(
                        MAX_ITEMS_MARKER
                    )

                    break

                result.append(
                    self._sanitize(
                        item,
                        depth + 1,
                        seen
                    )
                )

            return result

        except Exception as exc:

            return {
                TYPE_MARKER:
                    type(value).__name__,

                VALUE_MARKER:
                    UNSERIALIZABLE_MARKER,

                "error":
                    str(exc),
            }

        finally:

            seen.discard(object_id)

    # ========================================================
    #
    # ITERABLE DETECTION
    #
    # ========================================================

    def _is_safe_iterable(
        self,
        value: Any
    ) -> bool:

        if isinstance(
            value,
            (
                str,
                bytes,
                bytearray,
                memoryview,
                dict,
                list,
                tuple,
                set,
                frozenset
            )
        ):
            return False

        try:

            return isinstance(
                value,
                Iterable
            )

        except Exception:

            return False

    # ========================================================
    #
    # SAFE KEY
    #
    # ========================================================

    def _sanitize_key(
        self,
        key: Any
    ) -> str:

        if isinstance(key, str):

            if len(key) > self.max_key_length:

                return (
                    key[:self.max_key_length]
                    + TRUNCATED_MARKER
                )

            return key

        if key is None:
            return "null"

        if isinstance(key, bool):
            return str(key).lower()

        if isinstance(
            key,
            (
                int,
                float
            )
        ):

            if isinstance(key, float):

                if math.isnan(key):
                    return "NaN"

                if math.isinf(key):
                    return (
                        "Infinity"
                        if key > 0
                        else
                        "-Infinity"
                    )

            return str(key)

        if isinstance(key, Enum):

            return (
                f"{type(key).__name__}.{key.name}"
            )

        if isinstance(key, UUID):

            return str(key)

        try:

            text = str(key)

            if len(text) > self.max_key_length:

                return (
                    text[:self.max_key_length]
                    + TRUNCATED_MARKER
                )

            return text

        except Exception:

            return INVALID_KEY_MARKER

    # ========================================================
    #
    # UNIQUE DICT KEY
    #
    # ========================================================

    def _unique_key(
        self,
        result: dict[str, Any],
        key: str
    ) -> str:

        if key not in result:
            return key

        index = 2

        while f"{key}#{index}" in result:
            index += 1

        return f"{key}#{index}"

    # ========================================================
    #
    # CUSTOM OBJECT
    #
    # ========================================================

    def _sanitize_object(
        self,
        value: Any,
        depth: int,
        seen: set[int]
    ) -> Any:

        object_id = id(value)

        if object_id in seen:

            with self._lock:
                self._stats["circular_references"] += 1

            return CIRCULAR_REFERENCE_MARKER

        seen.add(object_id)

        with self._lock:
            self._stats["objects_processed"] += 1

        try:

            # ------------------------------------------------
            # to_json()
            # ------------------------------------------------

            if hasattr(
                value,
                "to_json"
            ):

                try:

                    raw = value.to_json()

                    with self._lock:
                        self._stats[
                            "objects_with_to_json"
                        ] += 1

                    if isinstance(raw, str):

                        try:

                            raw = json.loads(raw)

                        except Exception:

                            return {
                                TYPE_MARKER:
                                    type(value).__name__,

                                VALUE_MARKER:
                                    self._sanitize_string(
                                        raw
                                    )
                            }

                    return self._sanitize(
                        raw,
                        depth + 1,
                        seen
                    )

                except Exception as exc:

                    logger.debug(
                        "to_json failed for %s: %s",
                        type(value).__name__,
                        exc
                    )

            # ------------------------------------------------
            # to_dict()
            # ------------------------------------------------

            if hasattr(
                value,
                "to_dict"
            ):

                try:

                    raw = value.to_dict()

                    with self._lock:
                        self._stats[
                            "objects_with_to_dict"
                        ] += 1

                    return self._sanitize(
                        raw,
                        depth + 1,
                        seen
                    )

                except Exception as exc:

                    logger.debug(
                        "to_dict failed for %s: %s",
                        type(value).__name__,
                        exc
                    )

            # ------------------------------------------------
            # __dict__
            # ------------------------------------------------

            if hasattr(
                value,
                "__dict__"
            ):

                try:

                    raw = vars(value)

                    return {
                        TYPE_MARKER:
                            type(value).__name__,

                        MODULE_MARKER:
                            type(value).__module__,

                        DATA_MARKER:
                            self._sanitize(
                                raw,
                                depth + 1,
                                seen
                            )
                    }

                except Exception as exc:

                    logger.debug(
                        "__dict__ serialization failed "
                        "for %s: %s",
                        type(value).__name__,
                        exc
                    )

            # ------------------------------------------------
            # __slots__
            # ------------------------------------------------

            slots = getattr(
                type(value),
                "__slots__",
                None
            )

            if slots:

                if isinstance(
                    slots,
                    str
                ):

                    slots = [slots]

                data = {}

                for slot in slots:

                    try:

                        if hasattr(
                            value,
                            slot
                        ):

                            data[slot] = self._sanitize(
                                getattr(
                                    value,
                                    slot
                                ),
                                depth + 1,
                                seen
                            )

                    except Exception as exc:

                        data[slot] = {
                            VALUE_MARKER:
                                UNSERIALIZABLE_MARKER,
                            "error":
                                str(exc),
                        }

                return {
                    TYPE_MARKER:
                        type(value).__name__,

                    MODULE_MARKER:
                        type(value).__module__,

                    DATA_MARKER:
                        data
                }

            # ------------------------------------------------
            # FALLBACK
            # ------------------------------------------------

            with self._lock:
                self._stats["fallback_objects"] += 1

            try:

                return {
                    TYPE_MARKER:
                        type(value).__name__,

                    MODULE_MARKER:
                        type(value).__module__,

                    VALUE_MARKER:
                        self._sanitize_string(
                            str(value)
                        )
                }

            except Exception:

                return {
                    TYPE_MARKER:
                        type(value).__name__,

                    VALUE_MARKER:
                        UNSERIALIZABLE_MARKER
                }

        finally:

            seen.discard(object_id)

    # ========================================================
    #
    # JSON STRING
    #
    # ========================================================

    def dumps(
        self,
        value: Any,
        *,
        indent: int | None = None,
        sort_keys: bool = False,
        ensure_ascii: bool = False,
        allow_nan: bool = False
    ) -> str:
        """
        Convert arbitrary Python data into a JSON string.
        """

        safe_value = self.sanitize(
            value
        )

        try:

            return json.dumps(
                safe_value,
                ensure_ascii=ensure_ascii,
                indent=indent,
                sort_keys=sort_keys,
                allow_nan=allow_nan
            )

        except Exception as exc:

            logger.exception(
                "JSON dumps failed: %s",
                exc
            )

            fallback = {
                TYPE_MARKER:
                    "serialization_error",

                VALUE_MARKER:
                    UNSERIALIZABLE_MARKER,

                "error":
                    str(exc)
            }

            return json.dumps(
                fallback,
                ensure_ascii=False
            )

    # ========================================================
    #
    # JSON FILE WRITE
    #
    # ========================================================

    def dump(
        self,
        value: Any,
        file_path: str | Path,
        *,
        indent: int = DEFAULT_INDENT,
        sort_keys: bool = False,
        backup: bool = False
    ) -> bool:
        """
        Safely write serialized data to a JSON file.

        Uses a temporary file followed by os.replace() so
        readers do not normally observe a half-written file.
        """

        try:

            path = Path(
                file_path
            )

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            safe_value = self.sanitize(
                value
            )

            temporary = path.with_suffix(
                path.suffix + ".tmp"
            )

            with temporary.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    safe_value,
                    file,
                    ensure_ascii=False,
                    indent=indent,
                    sort_keys=sort_keys,
                    allow_nan=False
                )

                file.flush()

                try:
                    os.fsync(
                        file.fileno()
                    )
                except Exception:
                    pass

            # ------------------------------------------------
            # OPTIONAL BACKUP
            # ------------------------------------------------

            if backup and path.exists():

                backup_path = path.with_suffix(
                    path.suffix + ".bak"
                )

                try:

                    if backup_path.exists():
                        backup_path.unlink()

                    path.replace(
                        backup_path
                    )

                except Exception as exc:

                    logger.warning(
                        "Backup creation failed for %s: %s",
                        path,
                        exc
                    )

            os.replace(
                temporary,
                path
            )

            with self._lock:
                self._stats["file_writes"] += 1

            return True

        except Exception as exc:

            with self._lock:
                self._stats["file_write_errors"] += 1

            logger.exception(
                "Failed to write serialized data: %s",
                exc
            )

            try:

                if "temporary" in locals():
                    if temporary.exists():
                        temporary.unlink()

            except Exception:
                pass

            return False

    # ========================================================
    #
    # JSON LOAD
    #
    # ========================================================

    def load(
        self,
        file_path: str | Path,
        default: Any = None,
        *,
        max_file_size: int | None = None
    ) -> Any:
        """
        Safely load JSON data from disk.
        """

        try:

            path = Path(
                file_path
            )

            if not path.exists():
                return default

            limit = (
                self.max_file_size
                if max_file_size is None
                else max(
                    1024,
                    int(max_file_size)
                )
            )

            try:

                size = path.stat().st_size

                if size > limit:

                    logger.warning(
                        "JSON file exceeds maximum size: %s",
                        path
                    )

                    return {
                        VALUE_MARKER:
                            FILE_TOO_LARGE_MARKER,

                        "path":
                            str(path),

                        "size":
                            size,

                        "max_size":
                            limit
                    }

            except Exception:
                pass

            with path.open(
                "r",
                encoding="utf-8-sig"
            ) as file:

                data = json.load(
                    file
                )

            with self._lock:
                self._stats["file_loads"] += 1

            return data

        except Exception as exc:

            with self._lock:
                self._stats["file_load_errors"] += 1

            logger.exception(
                "Failed to load serialized data: %s",
                exc
            )

            return default

    # ========================================================
    #
    # JSON SAFETY CHECK
    #
    # ========================================================

    def is_json_safe(
        self,
        value: Any
    ) -> bool:
        """
        Check whether a value can be serialized directly by
        Python's JSON encoder without sanitization.
        """

        try:

            json.dumps(
                value,
                ensure_ascii=False,
                allow_nan=False
            )

            return True

        except Exception:

            return False

    # ========================================================
    #
    # VALIDATE SERIALIZED DATA
    #
    # ========================================================

    def validate(
        self,
        value: Any
    ) -> dict[str, Any]:
        """
        Sanitize and validate a value.

        Returns a structured validation result.
        """

        try:

            safe_value = self.sanitize(
                value
            )

            json.dumps(
                safe_value,
                ensure_ascii=False,
                allow_nan=False
            )

            return {
                "valid": True,
                "json_safe": True,
                "value": safe_value,
                "error": None
            }

        except Exception as exc:

            return {
                "valid": False,
                "json_safe": False,
                "value": None,
                "error": str(exc)
            }

    # ========================================================
    #
    # STATS
    #
    # ========================================================

    def stats(
        self
    ) -> dict[str, Any]:

        with self._lock:

            result = dict(
                self._stats
            )

            calls = result[
                "sanitize_calls"
            ]

            if calls > 0:

                result[
                    "sanitize_success_rate"
                ] = round(
                    (
                        result[
                            "sanitize_success"
                        ]
                        / calls
                    ) * 100.0,
                    2
                )

            else:

                result[
                    "sanitize_success_rate"
                ] = 100.0

            result[
                "version"
            ] = SERIALIZER_VERSION

            result[
                "api_version"
            ] = API_VERSION

            return result

    # ========================================================
    #
    # RESET STATS
    #
    # ========================================================

    def reset_stats(
        self
    ) -> None:

        with self._lock:

            for key in self._stats:

                self._stats[key] = 0

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ) -> dict[str, Any]:

        stats = self.stats()

        return {
            "module":
                "serializer",

            "name":
                "Safe Serializer",

            "version":
                SERIALIZER_VERSION,

            "api_version":
                API_VERSION,

            "online":
                True,

            "max_depth":
                self.max_depth,

            "max_items":
                self.max_items,

            "max_string_length":
                self.max_string_length,

            "max_key_length":
                self.max_key_length,

            "max_file_size":
                self.max_file_size,

            "stats":
                stats
        }


# ============================================================
#
# GLOBAL SERIALIZER
#
# ============================================================

serializer = SafeSerializer()


# ============================================================
#
# SHORTCUT FUNCTIONS
#
# ============================================================

def sanitize(
    value: Any
) -> Any:

    return serializer.sanitize(
        value
    )


def dumps(
    value: Any,
    *,
    indent: int | None = None,
    sort_keys: bool = False,
    ensure_ascii: bool = False,
    allow_nan: bool = False
) -> str:

    return serializer.dumps(
        value,
        indent=indent,
        sort_keys=sort_keys,
        ensure_ascii=ensure_ascii,
        allow_nan=allow_nan
    )


def dump(
    value: Any,
    file_path: str | Path,
    *,
    indent: int = DEFAULT_INDENT,
    sort_keys: bool = False,
    backup: bool = False
) -> bool:

    return serializer.dump(
        value,
        file_path,
        indent=indent,
        sort_keys=sort_keys,
        backup=backup
    )


def load(
    file_path: str | Path,
    default: Any = None,
    *,
    max_file_size: int | None = None
) -> Any:

    return serializer.load(
        file_path,
        default,
        max_file_size=max_file_size
    )


def is_json_safe(
    value: Any
) -> bool:

    return serializer.is_json_safe(
        value
    )


def validate(
    value: Any
) -> dict[str, Any]:

    return serializer.validate(
        value
    )


def serializer_stats() -> dict[str, Any]:

    return serializer.stats()


def serializer_status() -> dict[str, Any]:

    return serializer.status()


# ============================================================
#
# SERIALIZABILITY TEST
#
# ============================================================

def test_serializer() -> dict[str, Any]:
    """
    Comprehensive serializer validation.
    """

    checks: dict[str, bool] = {}

    # --------------------------------------------------------
    # BASIC DATA
    # --------------------------------------------------------

    data = {
        "market": "BTC/USD",
        "signal": "bullish",
        "price": 100000.50,
        "active": True,
        "none": None
    }

    safe_data = sanitize(
        data
    )

    checks["basic_dict"] = (
        isinstance(
            safe_data,
            dict
        )
        and
        safe_data["market"]
        == "BTC/USD"
    )

    # --------------------------------------------------------
    # DATETIME
    # --------------------------------------------------------

    timestamp = datetime.now(
        timezone.utc
    )

    result = sanitize(
        {
            "timestamp": timestamp
        }
    )

    checks["datetime"] = (
        isinstance(
            result["timestamp"],
            str
        )
    )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    result = sanitize(
        {
            "date": date.today()
        }
    )

    checks["date"] = (
        isinstance(
            result["date"],
            str
        )
    )

    # --------------------------------------------------------
    # TIMEDELTA
    # --------------------------------------------------------

    result = sanitize(
        {
            "duration":
                timedelta(
                    seconds=10
                )
        }
    )

    checks["timedelta"] = (
        isinstance(
            result["duration"],
            dict
        )
        and
        result["duration"][
            TYPE_MARKER
        ]
        == "timedelta"
    )

    # --------------------------------------------------------
    # DECIMAL
    # --------------------------------------------------------

    result = sanitize(
        {
            "value":
                Decimal("123.45")
        }
    )

    checks["decimal"] = (
        result["value"]
        == 123.45
    )

    # --------------------------------------------------------
    # UUID
    # --------------------------------------------------------

    from uuid import uuid4

    generated_uuid = uuid4()

    result = sanitize(
        {
            "id":
                generated_uuid
        }
    )

    checks["uuid"] = (
        result["id"]
        == str(generated_uuid)
    )

    # --------------------------------------------------------
    # PATH
    # --------------------------------------------------------

    result = sanitize(
        {
            "path":
                Path("database/test.json")
        }
    )

    checks["path"] = (
        result["path"]
        == "database/test.json"
    )

    # --------------------------------------------------------
    # SET
    # --------------------------------------------------------

    result = sanitize(
        {
            "tags": {
                "breakout",
                "momentum",
                "volume"
            }
        }
    )

    checks["set"] = (
        isinstance(
            result["tags"],
            list
        )
        and
        len(result["tags"]) == 3
    )

    # --------------------------------------------------------
    # TUPLE
    # --------------------------------------------------------

    result = sanitize(
        {
            "values": (
                1,
                2,
                3
            )
        }
    )

    checks["tuple"] = (
        result["values"]
        == [1, 2, 3]
    )

    # --------------------------------------------------------
    # BYTES
    # --------------------------------------------------------

    result = sanitize(
        {
            "bytes":
                b"hello"
        }
    )

    checks["bytes"] = (
        result["bytes"]
        == "hello"
    )

    # --------------------------------------------------------
    # CIRCULAR REFERENCE
    # --------------------------------------------------------

    circular = {}

    circular["self"] = circular

    safe_circular = sanitize(
        circular
    )

    checks["circular_protected"] = (
        safe_circular.get("self")
        == CIRCULAR_REFERENCE_MARKER
    )

    # --------------------------------------------------------
    # DEEP STRUCTURE
    # --------------------------------------------------------

    deep = {
        "level": 0
    }

    current = deep

    for index in range(50):

        current["next"] = {
            "level":
                index + 1
        }

        current = current[
            "next"
        ]

    serializer_local = SafeSerializer(
        max_depth=5
    )

    deep_result = serializer_local.sanitize(
        deep
    )

    deep_json = json.dumps(
        deep_result
    )

    checks["depth_protected"] = (
        MAX_DEPTH_MARKER
        in deep_json
    )

    # --------------------------------------------------------
    # LARGE LIST
    # --------------------------------------------------------

    serializer_local = SafeSerializer(
        max_items=5
    )

    large_result = serializer_local.sanitize(
        list(
            range(100)
        )
    )

    checks["items_protected"] = (
        len(large_result) == 6
        and
        large_result[-1]
        == MAX_ITEMS_MARKER
    )

    # --------------------------------------------------------
    # LONG STRING
    # --------------------------------------------------------

    serializer_local = SafeSerializer(
        max_string_length=10
    )

    long_string = serializer_local.sanitize(
        "A" * 100
    )

    checks["string_protected"] = (
        isinstance(
            long_string,
            str
        )
        and
        TRUNCATED_MARKER
        in long_string
    )

    # --------------------------------------------------------
    # NAN
    # --------------------------------------------------------

    result = sanitize(
        {
            "value":
                float("nan")
        }
    )

    checks["nan_protected"] = (
        result["value"] is None
    )

    # --------------------------------------------------------
    # POSITIVE INFINITY
    # --------------------------------------------------------

    result = sanitize(
        {
            "value":
                float("inf")
        }
    )

    checks["positive_infinity"] = (
        result["value"]
        == "Infinity"
    )

    # --------------------------------------------------------
    # NEGATIVE INFINITY
    # --------------------------------------------------------

    result = sanitize(
        {
            "value":
                float("-inf")
        }
    )

    checks["negative_infinity"] = (
        result["value"]
        == "-Infinity"
    )

    # --------------------------------------------------------
    # CUSTOM to_dict
    # --------------------------------------------------------

    class TestObject:

        def __init__(
            self
        ):

            self.name = "test"

        def to_dict(
            self
        ):

            return {
                "name":
                    self.name,

                "source":
                    "to_dict"
            }

    result = sanitize(
        TestObject()
    )

    checks["custom_to_dict"] = (
        result.get("name")
        == "test"
        and
        result.get("source")
        == "to_dict"
    )

    # --------------------------------------------------------
    # __dict__
    # --------------------------------------------------------

    class DictObject:

        def __init__(
            self
        ):

            self.value = 123

    result = sanitize(
        DictObject()
    )

    checks["custom_object"] = (
        result.get(
            TYPE_MARKER
        )
        == "DictObject"
        and
        result.get(
            DATA_MARKER
        )["value"]
        == 123
    )

    # --------------------------------------------------------
    # JSON STRING
    # --------------------------------------------------------

    json_string = dumps(
        data,
        indent=2
    )

    try:

        decoded = json.loads(
            json_string
        )

        checks["json_dumps"] = (
            isinstance(
                decoded,
                dict
            )
        )

    except Exception:

        checks["json_dumps"] = False

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    validation = validate(
        data
    )

    checks["validation"] = (
        validation.get(
            "valid"
        )
        is True
        and
        validation.get(
            "json_safe"
        )
        is True
    )

    # --------------------------------------------------------
    # JSON SAFE
    # --------------------------------------------------------

    checks["json_safe"] = (
        is_json_safe(
            {
                "a": 1,
                "b": "test"
            }
        )
        is True
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status_result = serializer_status()

    checks["status"] = (
        isinstance(
            status_result,
            dict
        )
        and
        status_result.get(
            "online"
        )
        is True
    )

    # --------------------------------------------------------
    # STATS
    # --------------------------------------------------------

    stats = serializer_stats()

    checks["stats"] = (
        isinstance(
            stats,
            dict
        )
        and
        stats.get(
            "sanitize_calls",
            0
        ) > 0
    )

    # --------------------------------------------------------
    # FINAL JSON VALIDATION
    # --------------------------------------------------------

    try:

        json.dumps(
            safe_data,
            ensure_ascii=False,
            allow_nan=False
        )

        checks["final_json_validation"] = True

    except Exception:

        checks["final_json_validation"] = False

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    passed = sum(
        1
        for value in checks.values()
        if value
    )

    failed = (
        len(checks)
        - passed
    )

    score = (
        round(
            (
                passed
                /
                len(checks)
            ) * 100.0,
            2
        )
        if checks
        else 100.0
    )

    return {
        "status":
            (
                "PASS"
                if failed == 0
                else
                "FAIL"
            ),

        "version":
            SERIALIZER_VERSION,

        "api_version":
            API_VERSION,

        "checks":
            checks,

        "passed":
            passed,

        "failed":
            failed,

        "score":
            score,

        "stats":
            serializer_stats(),

        "serializer_status":
            serializer_status()
    }


# ============================================================
#
# MANUAL TEST
#
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )
    )

    print()
    print("=" * 70)
    print("INKSIDE INTELLIGENCE OS")
    print("SAFE SERIALIZER v2.0")
    print("=" * 70)
    print()

    result = test_serializer()

    print(
        "TEST STATUS:",
        result["status"]
    )

    print(
        "VERSION:",
        result["version"]
    )

    print(
        "API VERSION:",
        result["api_version"]
    )

    print(
        "PASSED:",
        result["passed"]
    )

    print(
        "FAILED:",
        result["failed"]
    )

    print(
        "SCORE:",
        result["score"]
    )

    print()
    print("CHECKS:")

    for name, value in result[
        "checks"
    ].items():

        print(
            f"  [{'PASS' if value else 'FAIL'}] "
            f"{name}"
        )

    print()
    print("STATUS:")
    print(
        json.dumps(
            result[
                "serializer_status"
            ],
            indent=2,
            ensure_ascii=False
        )
    )

    print()
    print("=" * 70)
    print("SERIALIZER TEST COMPLETE")
    print("=" * 70)


# ============================================================
#
# PUBLIC API
#
# ============================================================

__all__ = [

    "SafeSerializer",

    "serializer",

    "sanitize",
    "dumps",
    "dump",
    "load",

    "is_json_safe",
    "validate",

    "serializer_stats",
    "serializer_status",

    "test_serializer",

    "SERIALIZER_VERSION",
    "API_VERSION",

    "CIRCULAR_REFERENCE_MARKER",
    "MAX_DEPTH_MARKER",
    "MAX_ITEMS_MARKER",
    "UNSERIALIZABLE_MARKER",
    "INVALID_OBJECT_MARKER",
    "INVALID_KEY_MARKER",
    "TRUNCATED_MARKER",
    "FILE_TOO_LARGE_MARKER",
]

