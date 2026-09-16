# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# LEARNING CONTRACTS v2.0
#
# Production-Grade Stable Module Interface
#
# ============================================================
#
# PURPOSE
# ------------------------------------------------------------
#
# This module is the stable contract layer between:
#
#   - Learning Engine
#   - Intelligence Modules
#   - Scanner / Analyzer
#   - Memory
#   - Reasoning
#   - Prediction
#   - Strategy
#   - Decision
#   - Simulation
#   - Knowledge
#   - Graph
#   - Adaptive systems
#   - Future modules
#
# DESIGN PRINCIPLES
# ------------------------------------------------------------
#
# 1. Stable public contract
# 2. Backward compatibility
# 3. Defensive programming
# 4. JSON-safe transport
# 5. Circular-reference protection
# 6. Bounded serialization
# 7. Traceable execution
# 8. Structured errors
# 9. Module health monitoring
# 10. Extension-friendly architecture
# 11. No dependency on engine.py
# 12. Safe for production
#
# ============================================================

from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
    field,
    fields,
    is_dataclass,
)

from datetime import (
    date,
    datetime,
    time,
    timezone,
)

from enum import Enum
from pathlib import Path

from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
)

import copy
import json
import logging
import math
import time as time_module
import uuid


logger = logging.getLogger(__name__)


# ============================================================
#
# CONTRACT VERSION
#
# ============================================================

#
# CONTRACT_VERSION
# ------------------------------------------------------------
# Public compatibility version.
#
# Modules should depend on this value only when absolutely
# necessary.
#

CONTRACT_VERSION = "2.0"


#
# INTERNAL_CONTRACT_REVISION
# ------------------------------------------------------------
# Internal implementation revision.
#
# Can change without forcing every module to migrate.
#

INTERNAL_CONTRACT_REVISION = "2.0"


#
# CONTRACT_SCHEMA
# ------------------------------------------------------------
# Human-readable schema identifier.
#

CONTRACT_SCHEMA = (
    "inkside-intelligence-learning-contract"
)


# ============================================================
#
# SERIALIZATION LIMITS
#
# ============================================================

DEFAULT_MAX_DEPTH = 20
DEFAULT_MAX_ITEMS = 10000
DEFAULT_MAX_STRING_LENGTH = 100000


CIRCULAR_REFERENCE_MARKER = "[CIRCULAR_REFERENCE]"
MAX_DEPTH_MARKER = "[MAX_DEPTH]"
UNSERIALIZABLE_MARKER = "[UNSERIALIZABLE]"
TRUNCATED_MARKER = "[TRUNCATED]"


# ============================================================
#
# OUTPUT STATES
#
# ============================================================

OUTPUT_SUCCESS = "success"
OUTPUT_PARTIAL = "partial"
OUTPUT_SKIPPED = "skipped"
OUTPUT_FAILED = "failed"


VALID_OUTPUT_STATES = {
    OUTPUT_SUCCESS,
    OUTPUT_PARTIAL,
    OUTPUT_SKIPPED,
    OUTPUT_FAILED,
}


# ============================================================
#
# MODULE LIFECYCLE STATES
#
# ============================================================

MODULE_CREATED = "created"
MODULE_INITIALIZING = "initializing"
MODULE_ONLINE = "online"
MODULE_DEGRADED = "degraded"
MODULE_OFFLINE = "offline"
MODULE_DISABLED = "disabled"
MODULE_SHUTTING_DOWN = "shutting_down"
MODULE_STOPPED = "stopped"
MODULE_ERROR = "error"


VALID_MODULE_STATES = {
    MODULE_CREATED,
    MODULE_INITIALIZING,
    MODULE_ONLINE,
    MODULE_DEGRADED,
    MODULE_OFFLINE,
    MODULE_DISABLED,
    MODULE_SHUTTING_DOWN,
    MODULE_STOPPED,
    MODULE_ERROR,
}


# ============================================================
#
# TIME
#
# ============================================================

def utc_now() -> str:
    """
    Return the current timezone-aware UTC timestamp.

    Format:
        2026-01-01T12:00:00.000000Z
    """

    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def utc_timestamp() -> float:
    """
    Return Unix timestamp in UTC.
    """

    return time_module.time()


# ============================================================
#
# ID GENERATION
#
# ============================================================

def generate_id(prefix: str = "") -> str:
    """
    Generate a globally unique identifier.

    Examples:
        req_aabbcc...
        evt_aabbcc...
        trace_aabbcc...
    """

    value = uuid.uuid4().hex

    if prefix:
        return f"{prefix}_{value}"

    return value


# ============================================================
#
# SAFE NUMBER NORMALIZATION
#
# ============================================================

def normalize_confidence(
    value: Any,
    default: float = 0.0,
) -> float:
    """
    Normalize confidence to a safe 0-100 float.
    """

    try:
        value = float(value)

    except Exception:
        value = default

    if not math.isfinite(value):
        value = default

    return max(
        0.0,
        min(
            100.0,
            value,
        ),
    )


def normalize_execution_time(
    value: Any,
) -> float:
    """
    Normalize execution time to a non-negative finite float.
    """

    try:
        value = float(value)

    except Exception:
        return 0.0

    if not math.isfinite(value):
        return 0.0

    return max(
        0.0,
        value,
    )


# ============================================================
#
# SAFE COPY
#
# ============================================================

def safe_copy(
    value: Any,
) -> Any:
    """
    Defensive deepcopy.

    If deepcopy fails, return the original object instead of
    crashing the pipeline.
    """

    try:
        return copy.deepcopy(value)

    except Exception:
        return value


# ============================================================
#
# SAFE JSON SERIALIZER
#
# ============================================================

def safe_json(
    value: Any,
    *,
    max_depth: int = DEFAULT_MAX_DEPTH,
    max_items: int = DEFAULT_MAX_ITEMS,
    max_string_length: int = DEFAULT_MAX_STRING_LENGTH,
) -> Any:
    """
    Convert arbitrary Python objects into JSON-safe structures.

    Features:
        - circular-reference protection
        - recursion-depth protection
        - collection-size protection
        - string-length protection
        - datetime support
        - date/time support
        - Path support
        - Enum support
        - dataclass support
        - bytes support
        - tuple/set/frozenset support
        - custom object support
        - NaN / Infinity protection
    """

    max_depth = max(
        1,
        int(max_depth),
    )

    max_items = max(
        1,
        int(max_items),
    )

    max_string_length = max(
        100,
        int(max_string_length),
    )

    seen: Set[int] = set()

    def _sanitize(
        current: Any,
        depth: int,
    ) -> Any:

        # ----------------------------------------------------
        # DEPTH PROTECTION
        # ----------------------------------------------------

        if depth > max_depth:
            return MAX_DEPTH_MARKER


        # ----------------------------------------------------
        # NONE
        # ----------------------------------------------------

        if current is None:
            return None


        # ----------------------------------------------------
        # BOOLEAN
        # ----------------------------------------------------

        if isinstance(
            current,
            bool,
        ):
            return current


        # ----------------------------------------------------
        # INTEGER
        # ----------------------------------------------------

        if isinstance(
            current,
            int,
        ):

            return current


        # ----------------------------------------------------
        # FLOAT
        # ----------------------------------------------------

        if isinstance(
            current,
            float,
        ):

            if math.isfinite(current):
                return current

            if math.isnan(current):
                return None

            if current > 0:
                return "Infinity"

            return "-Infinity"


        # ----------------------------------------------------
        # STRING
        # ----------------------------------------------------

        if isinstance(
            current,
            str,
        ):

            if len(current) > max_string_length:

                return (
                    current[:max_string_length]
                    + TRUNCATED_MARKER
                )

            return current


        # ----------------------------------------------------
        # BYTES
        # ----------------------------------------------------

        if isinstance(
            current,
            bytes,
        ):

            try:
                return current.decode(
                    "utf-8",
                    errors="replace",
                )

            except Exception:
                return str(current)


        # ----------------------------------------------------
        # BYTEARRAY
        # ----------------------------------------------------

        if isinstance(
            current,
            bytearray,
        ):

            try:
                return bytes(
                    current
                ).decode(
                    "utf-8",
                    errors="replace",
                )

            except Exception:
                return str(current)


        # ----------------------------------------------------
        # DATETIME / DATE / TIME
        # ----------------------------------------------------

        if isinstance(
            current,
            (
                datetime,
                date,
                time,
            ),
        ):

            return current.isoformat()


        # ----------------------------------------------------
        # PATH
        # ----------------------------------------------------

        if isinstance(
            current,
            Path,
        ):

            return str(current)


        # ----------------------------------------------------
        # ENUM
        # ----------------------------------------------------

        if isinstance(
            current,
            Enum,
        ):

            try:
                return _sanitize(
                    current.value,
                    depth + 1,
                )

            except Exception:
                return str(current)


        # ----------------------------------------------------
        # DATACLASS
        # ----------------------------------------------------

        if is_dataclass(current):

            object_id = id(current)

            if object_id in seen:
                return CIRCULAR_REFERENCE_MARKER

            seen.add(object_id)

            try:

                try:
                    raw = asdict(current)

                except Exception:

                    raw = {}

                    for item in fields(current):

                        try:
                            raw[item.name] = getattr(
                                current,
                                item.name,
                            )

                        except Exception:
                            raw[item.name] = (
                                UNSERIALIZABLE_MARKER
                            )

                return _sanitize(
                    raw,
                    depth + 1,
                )

            finally:

                seen.discard(object_id)


        # ----------------------------------------------------
        # DICTIONARY
        # ----------------------------------------------------

        if isinstance(
            current,
            Mapping,
        ):

            object_id = id(current)

            if object_id in seen:
                return CIRCULAR_REFERENCE_MARKER

            seen.add(object_id)

            result: Dict[str, Any] = {}

            try:

                count = 0

                for key, item in current.items():

                    if count >= max_items:

                        result[
                            "__truncated__"
                        ] = True

                        break

                    safe_key = _sanitize_key(
                        key
                    )

                    result[
                        safe_key
                    ] = _sanitize(
                        item,
                        depth + 1,
                    )

                    count += 1

                return result

            finally:

                seen.discard(object_id)


        # ----------------------------------------------------
        # LIST / TUPLE / SET
        # ----------------------------------------------------

        if isinstance(
            current,
            (
                list,
                tuple,
                set,
                frozenset,
            ),
        ):

            object_id = id(current)

            if object_id in seen:
                return CIRCULAR_REFERENCE_MARKER

            seen.add(object_id)

            result: List[Any] = []

            try:

                for index, item in enumerate(
                    current
                ):

                    if index >= max_items:

                        result.append(
                            TRUNCATED_MARKER
                        )

                        break

                    result.append(
                        _sanitize(
                            item,
                            depth + 1,
                        )
                    )

                return result

            finally:

                seen.discard(object_id)


        # ----------------------------------------------------
        # CUSTOM OBJECT
        # ----------------------------------------------------

        object_id = id(current)

        if object_id in seen:
            return CIRCULAR_REFERENCE_MARKER

        seen.add(object_id)

        try:

            # -----------------------------------------------
            # to_dict()
            # -----------------------------------------------

            if hasattr(
                current,
                "to_dict",
            ):

                try:

                    converted = current.to_dict()

                    return _sanitize(
                        converted,
                        depth + 1,
                    )

                except Exception:
                    pass


            # -----------------------------------------------
            # __dict__
            # -----------------------------------------------

            if hasattr(
                current,
                "__dict__",
            ):

                try:

                    raw = vars(
                        current
                    )

                    return {
                        "__type__":
                            type(current).__name__,

                        "__module__":
                            type(current).__module__,

                        "data":
                            _sanitize(
                                raw,
                                depth + 1,
                            ),
                    }

                except Exception:
                    pass


            # -----------------------------------------------
            # FALLBACK
            # -----------------------------------------------

            try:

                text = str(
                    current
                )

            except Exception:

                text = UNSERIALIZABLE_MARKER

            return {
                "__type__":
                    type(current).__name__,

                "__module__":
                    type(current).__module__,

                "__value__":
                    text,
            }

        finally:

            seen.discard(object_id)


    def _sanitize_key(
        key: Any,
    ) -> str:

        if isinstance(
            key,
            str,
        ):

            if len(key) > max_string_length:

                return (
                    key[:max_string_length]
                    + TRUNCATED_MARKER
                )

            return key


        if key is None:
            return "null"


        if isinstance(
            key,
            bool,
        ):

            return str(
                key
            ).lower()


        try:

            return str(
                key
            )

        except Exception:

            return "[INVALID_KEY]"


    return _sanitize(
        value,
        0,
    )


# ============================================================
#
# JSON SAFE CHECK
#
# ============================================================

def is_json_safe(
    value: Any,
) -> bool:
    """
    Check whether a value can be represented as valid JSON
    after sanitization.
    """

    try:

        json.dumps(
            safe_json(value),
            ensure_ascii=False,
        )

        return True

    except Exception:

        return False


# ============================================================
#
# MODULE STATUS
#
# ============================================================

@dataclass
class ModuleStatus:
    """
    Runtime health information for a module.
    """

    name: str

    version: str = "1.0"

    enabled: bool = True

    online: bool = False

    healthy: bool = True

    state: str = MODULE_CREATED

    errors: int = 0

    warnings: int = 0

    executions: int = 0

    successful_executions: int = 0

    failed_executions: int = 0

    skipped_executions: int = 0

    total_execution_time: float = 0.0

    average_execution_time: float = 0.0

    last_execution: Optional[str] = None

    last_success: Optional[str] = None

    last_error_time: Optional[str] = None

    last_error: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def mark_execution(
        self,
        execution_time: float = 0.0,
        success: bool = True,
        skipped: bool = False,
    ) -> None:

        self.executions += 1

        self.last_execution = utc_now()

        execution_time = normalize_execution_time(
            execution_time
        )

        self.total_execution_time += (
            execution_time
        )

        if self.executions > 0:

            self.average_execution_time = (
                self.total_execution_time
                / self.executions
            )

        if skipped:

            self.skipped_executions += 1

            return

        if success:

            self.successful_executions += 1

            self.last_success = (
                self.last_execution
            )

        else:

            self.failed_executions += 1


    def mark_error(
        self,
        error: Exception | str,
    ) -> None:

        self.errors += 1

        self.healthy = False

        self.state = MODULE_ERROR

        self.last_error = str(
            error
        )

        self.last_error_time = utc_now()


    def mark_warning(
        self,
        message: Exception | str,
    ) -> None:

        self.warnings += 1


    def mark_healthy(self) -> None:

        self.healthy = True

        self.online = True

        self.state = MODULE_ONLINE

        self.last_error = None


    def disable(self) -> None:

        self.enabled = False

        self.online = False

        self.state = MODULE_DISABLED


    def enable(self) -> None:

        self.enabled = True

        self.online = True

        self.state = MODULE_ONLINE


    def set_state(
        self,
        state: str,
    ) -> None:

        if state not in VALID_MODULE_STATES:

            raise ValueError(
                f"Invalid module state: {state}"
            )

        self.state = state

        self.online = (
            state
            in {
                MODULE_ONLINE,
                MODULE_DEGRADED,
            }
        )


    def to_dict(self) -> Dict[str, Any]:

        return safe_json(
            asdict(self)
        )


# ============================================================
#
# MODULE INPUT
#
# ============================================================

@dataclass
class ModuleInput:
    """
    Standardized input envelope for modules.
    """

    data: Any

    source: str = "unknown"

    timestamp: str = field(
        default_factory=utc_now
    )

    request_id: str = field(
        default_factory=lambda:
        generate_id("req")
    )

    trace_id: Optional[str] = None

    parent_id: Optional[str] = None

    stage: Optional[str] = None

    context: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    priority: int = 0

    attempt: int = 1

    max_attempts: int = 1

    timeout: Optional[float] = None

    tags: List[str] = field(
        default_factory=list
    )

    def __post_init__(self):

        if not self.trace_id:

            self.trace_id = generate_id(
                "trace"
            )

        try:
            self.priority = int(
                self.priority
            )

        except Exception:
            self.priority = 0

        try:
            self.attempt = max(
                1,
                int(self.attempt),
            )

        except Exception:
            self.attempt = 1

        try:
            self.max_attempts = max(
                1,
                int(self.max_attempts),
            )

        except Exception:
            self.max_attempts = 1

        if (
            self.timeout is not None
        ):

            try:

                self.timeout = max(
                    0.0,
                    float(self.timeout),
                )

            except Exception:

                self.timeout = None


    def clone(
        self,
        *,
        new_request_id: bool = False,
        preserve_trace: bool = True,
    ) -> "ModuleInput":

        return ModuleInput(

            data=safe_copy(
                self.data
            ),

            source=self.source,

            timestamp=self.timestamp,

            request_id=(
                generate_id("req")
                if new_request_id
                else self.request_id
            ),

            trace_id=(
                self.trace_id
                if preserve_trace
                else generate_id("trace")
            ),

            parent_id=self.parent_id,

            stage=self.stage,

            context=safe_copy(
                self.context
            ),

            metadata=safe_copy(
                self.metadata
            ),

            priority=self.priority,

            attempt=self.attempt,

            max_attempts=self.max_attempts,

            timeout=self.timeout,

            tags=list(
                self.tags
            ),
        )


    def next_attempt(
        self,
    ) -> "ModuleInput":

        cloned = self.clone()

        cloned.attempt += 1

        cloned.parent_id = (
            self.request_id
        )

        return cloned


    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return safe_json(
            asdict(self)
        )


# ============================================================
#
# MODULE OUTPUT
#
# ============================================================

@dataclass
class ModuleOutput:
    """
    Standardized output envelope for modules.
    """

    data: Any = None

    success: bool = True

    module: str = "unknown"

    version: str = CONTRACT_VERSION

    timestamp: str = field(
        default_factory=utc_now
    )

    request_id: Optional[str] = None

    trace_id: Optional[str] = None

    parent_id: Optional[str] = None

    confidence: float = 0.0

    warnings: List[str] = field(
        default_factory=list
    )

    errors: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    state: str = OUTPUT_SUCCESS

    stage: Optional[str] = None

    execution_time: float = 0.0

    skipped: bool = False

    retryable: bool = False

    attempt: int = 1

    max_attempts: int = 1

    cache_hit: bool = False

    degraded: bool = False

    extensions: Dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self):

        self.confidence = normalize_confidence(
            self.confidence
        )

        self.execution_time = (
            normalize_execution_time(
                self.execution_time
            )
        )

        if self.state not in VALID_OUTPUT_STATES:

            self.state = (
                OUTPUT_SUCCESS
                if self.success
                else OUTPUT_FAILED
            )

        self.success = (
            self.state
            != OUTPUT_FAILED
        )

        if self.state == OUTPUT_SKIPPED:

            self.skipped = True


    def add_warning(
        self,
        message: Any,
    ) -> None:

        if message is None:
            return

        text = str(
            message
        )

        if text:

            self.warnings.append(
                text
            )


    def add_error(
        self,
        message: Any,
    ) -> None:

        if message is None:
            return

        text = str(
            message
        )

        if text:

            self.errors.append(
                text
            )

            self.success = False

            self.state = OUTPUT_FAILED


    def set_confidence(
        self,
        value: Any,
    ) -> None:

        self.confidence = normalize_confidence(
            value
        )


    def set_execution_time(
        self,
        value: Any,
    ) -> None:

        self.execution_time = (
            normalize_execution_time(
                value
            )
        )


    def mark_success(
        self,
    ) -> None:

        self.success = True

        self.skipped = False

        self.state = OUTPUT_SUCCESS


    def mark_partial(
        self,
    ) -> None:

        self.success = True

        self.skipped = False

        self.state = OUTPUT_PARTIAL


    def mark_skipped(
        self,
        reason: Optional[str] = None,
    ) -> None:

        self.success = True

        self.skipped = True

        self.state = OUTPUT_SKIPPED

        if reason:

            self.add_warning(
                reason
            )


    def mark_failed(
        self,
        error: Optional[str] = None,
        *,
        retryable: bool = False,
    ) -> None:

        self.success = False

        self.skipped = False

        self.state = OUTPUT_FAILED

        self.retryable = retryable

        if error:

            self.add_error(
                error
            )


    def set_extension(
        self,
        name: str,
        value: Any,
    ) -> None:

        if not name:
            return

        self.extensions[
            str(name)
        ] = safe_copy(
            value
        )


    def get_extension(
        self,
        name: str,
        default: Any = None,
    ) -> Any:

        return self.extensions.get(
            name,
            default,
        )


    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return safe_json(
            asdict(self)
        )


    def clone(
        self,
    ) -> "ModuleOutput":

        return ModuleOutput(
            data=safe_copy(
                self.data
            ),

            success=self.success,

            module=self.module,

            version=self.version,

            timestamp=self.timestamp,

            request_id=self.request_id,

            trace_id=self.trace_id,

            parent_id=self.parent_id,

            confidence=self.confidence,

            warnings=list(
                self.warnings
            ),

            errors=list(
                self.errors
            ),

            metadata=safe_copy(
                self.metadata
            ),

            state=self.state,

            stage=self.stage,

            execution_time=self.execution_time,

            skipped=self.skipped,

            retryable=self.retryable,

            attempt=self.attempt,

            max_attempts=self.max_attempts,

            cache_hit=self.cache_hit,

            degraded=self.degraded,

            extensions=safe_copy(
                self.extensions
            ),
        )


# ============================================================
#
# LEARNING EVENT
#
# ============================================================

@dataclass
class LearningEvent:
    """
    Standard event envelope used between learning modules.
    """

    event_type: str

    source: str

    data: Any = None

    timestamp: str = field(
        default_factory=utc_now
    )

    event_id: str = field(
        default_factory=lambda:
        generate_id("evt")
    )

    request_id: Optional[str] = None

    trace_id: Optional[str] = None

    parent_id: Optional[str] = None

    stage: Optional[str] = None

    severity: str = "info"

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    tags: List[str] = field(
        default_factory=list
    )


    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return safe_json(
            asdict(self)
        )


    def child_event(
        self,
        event_type: str,
        data: Any = None,
        source: Optional[str] = None,
    ) -> "LearningEvent":

        return LearningEvent(

            event_type=event_type,

            source=(
                source
                or self.source
            ),

            data=data,

            request_id=self.request_id,

            trace_id=self.trace_id,

            parent_id=self.event_id,

            stage=self.stage,

            metadata=safe_copy(
                self.metadata
            ),

            tags=list(
                self.tags
            ),
        )


# ============================================================
#
# LEARNING RESULT
#
# ============================================================

@dataclass
class LearningResult:
    """
    Central result container for the Intelligence OS.

    The architecture intentionally exposes many cognitive
    stages while keeping `extensions` available for future
    modules.
    """

    input_data: Any = None

    timestamp: str = field(
        default_factory=utc_now
    )

    request_id: str = field(
        default_factory=lambda:
        generate_id("req")
    )

    trace_id: Optional[str] = None

    features: Any = None

    entities: Any = None

    semantic: Any = None

    context: Any = None

    analysis: Any = None

    patterns: Any = None

    behavior: Any = None

    experience: Any = None

    evaluation: Any = None

    reflection: Any = None

    improvement: Any = None

    adaptive: Any = None

    reasoning: Any = None

    prediction: Any = None

    simulation: Any = None

    strategy: Any = None

    decision: Any = None

    knowledge: Any = None

    graph: Any = None

    memory: Any = None

    association: Any = None

    curiosity: Any = None

    goals: Any = None

    diagnostic: Any = None

    evolution: Any = None

    insight: Any = None

    engine: Dict[str, Any] = field(
        default_factory=dict
    )

    warnings: List[str] = field(
        default_factory=list
    )

    errors: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    extensions: Dict[str, Any] = field(
        default_factory=dict
    )


    def __post_init__(self):

        if not self.trace_id:

            self.trace_id = generate_id(
                "trace"
            )


    def add_warning(
        self,
        message: Any,
    ) -> None:

        if message:

            self.warnings.append(
                str(message)
            )


    def add_error(
        self,
        message: Any,
    ) -> None:

        if message:

            self.errors.append(
                str(message)
            )


    def set_extension(
        self,
        name: str,
        value: Any,
    ) -> None:

        if not name:
            return

        self.extensions[
            str(name)
        ] = safe_copy(
            value
        )


    def get_extension(
        self,
        name: str,
        default: Any = None,
    ) -> Any:

        return self.extensions.get(
            name,
            default,
        )


    def has_errors(
        self,
    ) -> bool:

        return bool(
            self.errors
        )


    def has_warnings(
        self,
    ) -> bool:

        return bool(
            self.warnings
        )


    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return safe_json(
            asdict(self)
        )


    def clone(
        self,
    ) -> "LearningResult":

        return LearningResult(

            input_data=safe_copy(
                self.input_data
            ),

            timestamp=self.timestamp,

            request_id=self.request_id,

            trace_id=self.trace_id,

            features=safe_copy(
                self.features
            ),

            entities=safe_copy(
                self.entities
            ),

            semantic=safe_copy(
                self.semantic
            ),

            context=safe_copy(
                self.context
            ),

            analysis=safe_copy(
                self.analysis
            ),

            patterns=safe_copy(
                self.patterns
            ),

            behavior=safe_copy(
                self.behavior
            ),

            experience=safe_copy(
                self.experience
            ),

            evaluation=safe_copy(
                self.evaluation
            ),

            reflection=safe_copy(
                self.reflection
            ),

            improvement=safe_copy(
                self.improvement
            ),

            adaptive=safe_copy(
                self.adaptive
            ),

            reasoning=safe_copy(
                self.reasoning
            ),

            prediction=safe_copy(
                self.prediction
            ),

            simulation=safe_copy(
                self.simulation
            ),

            strategy=safe_copy(
                self.strategy
            ),

            decision=safe_copy(
                self.decision
            ),

            knowledge=safe_copy(
                self.knowledge
            ),

            graph=safe_copy(
                self.graph
            ),

            memory=safe_copy(
                self.memory
            ),

            association=safe_copy(
                self.association
            ),

            curiosity=safe_copy(
                self.curiosity
            ),

            goals=safe_copy(
                self.goals
            ),

            diagnostic=safe_copy(
                self.diagnostic
            ),

            evolution=safe_copy(
                self.evolution
            ),

            insight=safe_copy(
                self.insight
            ),

            engine=safe_copy(
                self.engine
            ),

            warnings=list(
                self.warnings
            ),

            errors=list(
                self.errors
            ),

            metadata=safe_copy(
                self.metadata
            ),

            extensions=safe_copy(
                self.extensions
            ),
        )


# ============================================================
#
# MODULE CONTRACT
#
# ============================================================

class ModuleContract:
    """
    Base interface for all Intelligence OS modules.

    Legacy modules may continue to operate outside this
    interface while migration happens gradually.
    """

    NAME = "unnamed"

    VERSION = "1.0"

    DESCRIPTION = ""

    CAPABILITIES: Set[str] = set()

    DEPENDENCIES: List[str] = []

    OPTIONAL_DEPENDENCIES: List[str] = []

    CONTRACT_VERSION = CONTRACT_VERSION

    ENABLED_BY_DEFAULT = True

    MAX_EXECUTION_TIME: Optional[float] = None


    def __init__(
        self,
    ):

        self.status = ModuleStatus(

            name=self.NAME,

            version=self.VERSION,

            enabled=self.ENABLED_BY_DEFAULT,
        )

        self._initialized = False

        self._shutdown = False


    # ========================================================
    #
    # PRIMARY PROCESS
    #
    # ========================================================

    def process(
        self,
        data: Any = None,
    ) -> ModuleOutput:

        raise NotImplementedError(
            f"{self.NAME}.process() "
            "must be implemented."
        )


    # ========================================================
    #
    # INPUT NORMALIZATION
    #
    # ========================================================

    def process_input(
        self,
        module_input: ModuleInput,
    ) -> ModuleOutput:

        return self.process(
            module_input.data
        )


    # ========================================================
    #
    # LIFECYCLE
    #
    # ========================================================

    def initialize(
        self,
    ) -> bool:

        self.status.set_state(
            MODULE_INITIALIZING
        )

        try:

            self._initialized = True

            self._shutdown = False

            self.status.mark_healthy()

            return True

        except Exception as exc:

            self.status.mark_error(
                exc
            )

            return False


    def shutdown(
        self,
    ) -> bool:

        self.status.set_state(
            MODULE_SHUTTING_DOWN
        )

        try:

            self._shutdown = True

            self._initialized = False

            self.status.set_state(
                MODULE_STOPPED
            )

            return True

        except Exception as exc:

            self.status.mark_error(
                exc
            )

            return False


    def reset(
        self,
    ) -> None:

        self.status = ModuleStatus(

            name=self.NAME,

            version=self.VERSION,

            enabled=self.ENABLED_BY_DEFAULT,
        )

        self._initialized = False

        self._shutdown = False


    # ========================================================
    #
    # HEALTH
    #
    # ========================================================

    def health(
        self,
    ) -> Dict[str, Any]:

        return self.status.to_dict()


    def is_healthy(
        self,
    ) -> bool:

        return (
            self.status.enabled
            and self.status.healthy
        )


    def is_online(
        self,
    ) -> bool:

        return (
            self.status.online
            and self.status.enabled
        )


    # ========================================================
    #
    # CAPABILITIES
    #
    # ========================================================

    def supports(
        self,
        capability: str,
    ) -> bool:

        if not capability:
            return False

        return (
            capability
            in self.CAPABILITIES
        )


    def capabilities(
        self,
    ) -> List[str]:

        return sorted(
            self.CAPABILITIES
        )


    # ========================================================
    #
    # DEPENDENCIES
    #
    # ========================================================

    def dependencies(
        self,
    ) -> List[str]:

        return list(
            self.DEPENDENCIES
        )


    def optional_dependencies(
        self,
    ) -> List[str]:

        return list(
            self.OPTIONAL_DEPENDENCIES
        )


    # ========================================================
    #
    # METADATA
    #
    # ========================================================

    def metadata(
        self,
    ) -> Dict[str, Any]:

        return {

            "name":
                self.NAME,

            "version":
                self.VERSION,

            "description":
                self.DESCRIPTION,

            "contract_version":
                self.CONTRACT_VERSION,

            "capabilities":
                self.capabilities(),

            "dependencies":
                self.dependencies(),

            "optional_dependencies":
                self.optional_dependencies(),

            "status":
                self.status.to_dict(),
        }


    # ========================================================
    #
    # ENABLE / DISABLE
    #
    # ========================================================

    def enable(
        self,
    ) -> None:

        self.status.enable()


    def disable(
        self,
    ) -> None:

        self.status.disable()


# ============================================================
#
# NORMALIZE MODULE RESULT
#
# ============================================================

def normalize_output(
    value: Any,
    module_name: str = "unknown",
    request_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    stage: Optional[str] = None,
) -> ModuleOutput:
    """
    Convert arbitrary module return values into ModuleOutput.
    """

    if isinstance(
        value,
        ModuleOutput,
    ):

        if not value.request_id:
            value.request_id = request_id

        if not value.trace_id:
            value.trace_id = trace_id

        if not value.stage:
            value.stage = stage

        if not value.module:
            value.module = module_name

        return value


    return ModuleOutput(

        data=safe_copy(
            value
        ),

        success=True,

        module=module_name,

        version=CONTRACT_VERSION,

        request_id=request_id,

        trace_id=trace_id,

        stage=stage,
    )


# ============================================================
#
# CREATE INPUT
#
# ============================================================

def create_input(
    data: Any,
    source: str = "unknown",
    context: Optional[
        Dict[str, Any]
    ] = None,
    metadata: Optional[
        Dict[str, Any]
    ] = None,
    request_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    stage: Optional[str] = None,
    parent_id: Optional[str] = None,
    priority: int = 0,
    attempt: int = 1,
    max_attempts: int = 1,
    timeout: Optional[float] = None,
    tags: Optional[
        Iterable[str]
    ] = None,
) -> ModuleInput:
    """
    Create a standardized ModuleInput.
    """

    return ModuleInput(

        data=safe_copy(
            data
        ),

        source=source,

        context=safe_copy(
            context or {}
        ),

        metadata=safe_copy(
            metadata or {}
        ),

        request_id=(
            request_id
            or generate_id("req")
        ),

        trace_id=(
            trace_id
            or generate_id("trace")
        ),

        stage=stage,

        parent_id=parent_id,

        priority=priority,

        attempt=attempt,

        max_attempts=max_attempts,

        timeout=timeout,

        tags=list(
            tags or []
        ),
    )


# ============================================================
#
# CREATE EVENT
#
# ============================================================

def create_event(
    event_type: str,
    source: str,
    data: Any = None,
    *,
    request_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    stage: Optional[str] = None,
    severity: str = "info",
    metadata: Optional[
        Dict[str, Any]
    ] = None,
    tags: Optional[
        Iterable[str]
    ] = None,
) -> LearningEvent:
    """
    Create a standardized LearningEvent.
    """

    return LearningEvent(

        event_type=event_type,

        source=source,

        data=safe_copy(
            data
        ),

        request_id=request_id,

        trace_id=(
            trace_id
            or generate_id("trace")
        ),

        parent_id=parent_id,

        stage=stage,

        severity=severity,

        metadata=safe_copy(
            metadata or {}
        ),

        tags=list(
            tags or []
        ),
    )


# ============================================================
#
# EXCEPTION -> MODULE OUTPUT
#
# ============================================================

def exception_to_output(
    error: Exception | str,
    *,
    module_name: str = "unknown",
    request_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    stage: Optional[str] = None,
    retryable: bool = False,
    metadata: Optional[
        Dict[str, Any]
    ] = None,
) -> ModuleOutput:
    """
    Convert an exception into a safe ModuleOutput.
    """

    output = ModuleOutput(

        data=None,

        success=False,

        module=module_name,

        version=CONTRACT_VERSION,

        request_id=request_id,

        trace_id=trace_id,

        stage=stage,

        metadata=safe_copy(
            metadata or {}
        ),

        retryable=retryable,
    )

    output.mark_failed(
        str(error),
        retryable=retryable,
    )

    return output


# ============================================================
#
# CONTRACT VALIDATION
#
# ============================================================

def validate_output(
    output: Any,
) -> bool:
    """
    Validate ModuleOutput against the public contract.
    """

    if not isinstance(
        output,
        ModuleOutput,
    ):
        return False


    if not output.module:
        return False


    if not isinstance(
        output.warnings,
        list,
    ):
        return False


    if not isinstance(
        output.errors,
        list,
    ):
        return False


    if not isinstance(
        output.success,
        bool,
    ):
        return False


    if not isinstance(
        output.skipped,
        bool,
    ):
        return False


    if output.state not in VALID_OUTPUT_STATES:
        return False


    try:

        confidence = float(
            output.confidence
        )

        if not math.isfinite(
            confidence
        ):
            return False

        if confidence < 0:
            return False

        if confidence > 100:
            return False

    except Exception:

        return False


    try:

        execution_time = float(
            output.execution_time
        )

        if not math.isfinite(
            execution_time
        ):
            return False

        if execution_time < 0:
            return False

    except Exception:

        return False


    if output.state == OUTPUT_FAILED:

        if output.success:
            return False


    if output.state == OUTPUT_SKIPPED:

        if not output.skipped:
            return False


    return True


# ============================================================
#
# VALIDATE INPUT
#
# ============================================================

def validate_input(
    module_input: Any,
) -> bool:
    """
    Validate ModuleInput.
    """

    if not isinstance(
        module_input,
        ModuleInput,
    ):
        return False


    if not module_input.source:
        return False


    if not module_input.request_id:
        return False


    if not module_input.trace_id:
        return False


    if not isinstance(
        module_input.context,
        dict,
    ):
        return False


    if not isinstance(
        module_input.metadata,
        dict,
    ):
        return False


    try:

        if module_input.attempt < 1:
            return False

        if module_input.max_attempts < 1:
            return False

    except Exception:

        return False


    return True


# ============================================================
#
# CONTRACT COMPATIBILITY
#
# ============================================================

def is_contract_compatible(
    version: str,
    expected: str = CONTRACT_VERSION,
) -> bool:
    """
    Basic contract compatibility check.

    Major version mismatch = incompatible.

    Example:
        2.1 compatible with 2.0
        3.0 incompatible with 2.0
    """

    try:

        version_major = str(
            version
        ).split(".")[0]

        expected_major = str(
            expected
        ).split(".")[0]

        return (
            version_major
            == expected_major
        )

    except Exception:

        return False


# ============================================================
#
# RESULT STATUS HELPERS
#
# ============================================================

def output_is_success(
    output: Any,
) -> bool:

    return (
        isinstance(
            output,
            ModuleOutput,
        )
        and output.success
        and output.state
        in {
            OUTPUT_SUCCESS,
            OUTPUT_PARTIAL,
        }
    )


def output_is_failure(
    output: Any,
) -> bool:

    return (
        isinstance(
            output,
            ModuleOutput,
        )
        and output.state
        == OUTPUT_FAILED
    )


def output_is_skipped(
    output: Any,
) -> bool:

    return (
        isinstance(
            output,
            ModuleOutput,
        )
        and output.state
        == OUTPUT_SKIPPED
    )


# ============================================================
#
# SERIALIZATION HELPERS
#
# ============================================================

def dumps(
    value: Any,
    *,
    indent: Optional[int] = None,
    sort_keys: bool = False,
) -> str:
    """
    Convert arbitrary contract data to JSON.
    """

    return json.dumps(

        safe_json(
            value
        ),

        ensure_ascii=False,

        indent=indent,

        sort_keys=sort_keys,
    )


def dump(
    value: Any,
    file_path: str | Path,
    *,
    indent: int = 2,
) -> bool:
    """
    Atomically write contract data to JSON.
    """

    try:

        path = Path(
            file_path
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary = path.with_suffix(
            path.suffix + ".tmp"
        )

        with temporary.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(

                safe_json(
                    value
                ),

                file,

                ensure_ascii=False,

                indent=indent,
            )


        temporary.replace(
            path
        )

        return True

    except Exception as exc:

        logger.exception(
            "Failed to write contract data: %s",
            exc,
        )

        return False


def load(
    file_path: str | Path,
    default: Any = None,
) -> Any:
    """
    Load JSON contract data safely.
    """

    try:

        path = Path(
            file_path
        )

        if not path.exists():
            return default


        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(
                file
            )

    except Exception as exc:

        logger.exception(
            "Failed to load contract data: %s",
            exc,
        )

        return default


# ============================================================
#
# EXECUTION TIMER
#
# ============================================================

class ExecutionTimer:
    """
    Lightweight monotonic execution timer.
    """

    def __init__(self):

        self.started_at = (
            time_module.perf_counter()
        )

        self.finished_at: Optional[
            float
        ] = None


    def stop(
        self,
    ) -> float:

        if self.finished_at is None:

            self.finished_at = (
                time_module.perf_counter()
            )

        return max(

            0.0,

            self.finished_at
            - self.started_at,
        )


    @property
    def elapsed(
        self,
    ) -> float:

        if self.finished_at is not None:

            return max(

                0.0,

                self.finished_at
                - self.started_at,
            )

        return max(

            0.0,

            time_module.perf_counter()
            - self.started_at,
        )


# ============================================================
#
# CONTRACT CONTEXT
#
# ============================================================

@dataclass
class ContractContext:
    """
    Shared execution context.

    Allows modules to communicate through a stable context
    without coupling directly to engine.py.
    """

    request_id: str = field(
        default_factory=lambda:
        generate_id("req")
    )

    trace_id: str = field(
        default_factory=lambda:
        generate_id("trace")
    )

    parent_id: Optional[str] = None

    source: str = "unknown"

    stage: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    variables: Dict[str, Any] = field(
        default_factory=dict
    )

    tags: List[str] = field(
        default_factory=list
    )


    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        if not key:
            return

        self.variables[
            str(key)
        ] = safe_copy(
            value
        )


    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.variables.get(
            key,
            default,
        )


    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return safe_json(
            asdict(self)
        )


# ============================================================
#
# MODULE EXECUTION RESULT
#
# ============================================================

@dataclass
class ModuleExecution:
    """
    Detailed execution record.

    Useful for diagnostics, telemetry, debugging and future
    observability systems.
    """

    execution_id: str = field(
        default_factory=lambda:
        generate_id("exec")
    )

    request_id: Optional[str] = None

    trace_id: Optional[str] = None

    module: str = "unknown"

    version: str = "1.0"

    stage: Optional[str] = None

    started_at: str = field(
        default_factory=utc_now
    )

    finished_at: Optional[str] = None

    duration: float = 0.0

    success: bool = False

    state: str = OUTPUT_SUCCESS

    attempt: int = 1

    error: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


    def finish(
        self,
        *,
        success: bool,
        state: str = OUTPUT_SUCCESS,
        error: Optional[str] = None,
        duration: Optional[float] = None,
    ) -> None:

        self.finished_at = utc_now()

        self.success = bool(
            success
        )

        self.state = state

        self.error = (
            str(error)
            if error
            else None
        )

        if duration is not None:

            self.duration = (
                normalize_execution_time(
                    duration
                )
            )


    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return safe_json(
            asdict(self)
        )


# ============================================================
#
# DEEP CONTRACT TEST
#
# ============================================================

def test_contracts() -> Dict[str, Any]:
    """
    Internal contract self-test.

    Returns a diagnostic dictionary instead of raising.
    """

    results: Dict[str, Any] = {}

    try:

        module_input = create_input(

            data={
                "market": "BTC/USD",

                "price": 100000,

                "nested": {
                    "active": True
                },
            },

            source="test",
        )

        results[
            "input_created"
        ] = validate_input(
            module_input
        )


        output = ModuleOutput(

            data={
                "signal": "bullish"
            },

            module="TestModule",

            request_id=(
                module_input.request_id
            ),

            trace_id=(
                module_input.trace_id
            ),
        )

        output.set_confidence(
            87.5
        )

        results[
            "output_valid"
        ] = validate_output(
            output
        )


        circular: Dict[str, Any] = {}

        circular[
            "self"
        ] = circular

        safe = safe_json(
            circular
        )

        results[
            "circular_protected"
        ] = (
            safe.get("self")
            == CIRCULAR_REFERENCE_MARKER
        )


        complex_data = {

            "datetime":
                datetime.now(
                    timezone.utc
                ),

            "date":
                date.today(),

            "time":
                datetime.now().time(),

            "path":
                Path("data/test.json"),

            "set":
                {"a", "b", "c"},

            "bytes":
                b"hello",

            "nan":
                float("nan"),

            "inf":
                float("inf"),
        }

        serialized = safe_json(
            complex_data
        )

        results[
            "complex_serialization"
        ] = is_json_safe(
            serialized
        )


        results[
            "json_serialization"
        ] = is_json_safe(
            output
        )


        results[
            "contract_compatible"
        ] = is_contract_compatible(
            CONTRACT_VERSION
        )


        results[
            "status"
        ] = "ONLINE"


        results[
            "success"
        ] = all(
            bool(value)
            for key, value in results.items()
            if key != "status"
        )

        return results

    except Exception as exc:

        logger.exception(
            "Contract self-test failed: %s",
            exc,
        )

        return {

            "status":
                "ERROR",

            "success":
                False,

            "error":
                str(exc),
        }


# ============================================================
#
# PUBLIC API
#
# ============================================================

__all__ = [

    # --------------------------------------------------------
    # VERSION
    # --------------------------------------------------------

    "CONTRACT_VERSION",
    "INTERNAL_CONTRACT_REVISION",
    "CONTRACT_SCHEMA",

    # --------------------------------------------------------
    # OUTPUT STATES
    # --------------------------------------------------------

    "OUTPUT_SUCCESS",
    "OUTPUT_PARTIAL",
    "OUTPUT_SKIPPED",
    "OUTPUT_FAILED",
    "VALID_OUTPUT_STATES",

    # --------------------------------------------------------
    # MODULE STATES
    # --------------------------------------------------------

    "MODULE_CREATED",
    "MODULE_INITIALIZING",
    "MODULE_ONLINE",
    "MODULE_DEGRADED",
    "MODULE_OFFLINE",
    "MODULE_DISABLED",
    "MODULE_SHUTTING_DOWN",
    "MODULE_STOPPED",
    "MODULE_ERROR",
    "VALID_MODULE_STATES",

    # --------------------------------------------------------
    # SERIALIZATION MARKERS
    # --------------------------------------------------------

    "CIRCULAR_REFERENCE_MARKER",
    "MAX_DEPTH_MARKER",
    "UNSERIALIZABLE_MARKER",
    "TRUNCATED_MARKER",

    # --------------------------------------------------------
    # TIME / ID
    # --------------------------------------------------------

    "utc_now",
    "utc_timestamp",
    "generate_id",

    # --------------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------------

    "normalize_confidence",
    "normalize_execution_time",

    # --------------------------------------------------------
    # COPY / JSON
    # --------------------------------------------------------

    "safe_copy",
    "safe_json",
    "is_json_safe",
    "dumps",
    "dump",
    "load",

    # --------------------------------------------------------
    # CORE CONTRACTS
    # --------------------------------------------------------

    "ModuleStatus",
    "ModuleInput",
    "ModuleOutput",
    "LearningEvent",
    "LearningResult",

    # --------------------------------------------------------
    # EXECUTION
    # --------------------------------------------------------

    "ExecutionTimer",
    "ContractContext",
    "ModuleExecution",

    # --------------------------------------------------------
    # MODULE
    # --------------------------------------------------------

    "ModuleContract",

    # --------------------------------------------------------
    # HELPERS
    # --------------------------------------------------------

    "normalize_output",
    "create_input",
    "create_event",
    "exception_to_output",

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    "validate_input",
    "validate_output",
    "is_contract_compatible",

    # --------------------------------------------------------
    # OUTPUT HELPERS
    # --------------------------------------------------------

    "output_is_success",
    "output_is_failure",
    "output_is_skipped",

    # --------------------------------------------------------
    # TEST
    # --------------------------------------------------------

    "test_contracts",
]


# ============================================================
#
# END
#
# ============================================================