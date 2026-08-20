# ============================================================
#
# INKSIDE INTELLIGENCE OS
# LEARNING ENGINE
#
# KERNEL VERSION 2.1.2
#
# PRODUCTION-GRADE INTELLIGENCE KERNEL
#
# FIXED:
# - Added is_running() method for status checks
# - Added start() and stop() aliases for GUI compatibility
# - Improved start_learning() to handle stale running state
# - Enhanced thread cleanup in stop_learning()
# - Fixed potential race conditions in learning_loop
# - Added safety checks in shutdown()
#
# ============================================================

from __future__ import annotations

import copy
import json
import logging
import math
import threading
import time
import uuid

from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError as FutureTimeoutError,
)

from datetime import (
    date,
    datetime,
    timezone,
)

from enum import Enum
from pathlib import Path

from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
)


logger = logging.getLogger(__name__)


# ============================================================
#
# KERNEL METADATA
#
# ============================================================

KERNEL_NAME = "INKSIDE INTELLIGENCE OS"
KERNEL_VERSION = "2.1.2"

ENGINE_NAME = "Learning Engine"
ENGINE_VERSION = "2.1.2"

MAX_HISTORY = 100

DEFAULT_LEARNING_INTERVAL = 300

DEFAULT_MAX_DEPTH = 16

DEFAULT_MODULE_TIMEOUT = 60

DEFAULT_RETRY_COUNT = 2

DEFAULT_RETRY_BACKOFF = 1.0

DEFAULT_CIRCUIT_THRESHOLD = 5

DEFAULT_CIRCUIT_RESET = 60

DEFAULT_MAX_WORKERS = 8


# ============================================================
#
# EXECUTION STATES
#
# ============================================================

STATE_IDLE = "IDLE"
STATE_RUNNING = "RUNNING"
STATE_SUCCESS = "SUCCESS"
STATE_PARTIAL = "PARTIAL"
STATE_ERROR = "ERROR"
STATE_TIMEOUT = "TIMEOUT"
STATE_DISABLED = "DISABLED"
STATE_DEPENDENCY_ERROR = "DEPENDENCY_ERROR"
STATE_NO_OUTPUT = "NO_OUTPUT"
STATE_CIRCUIT_OPEN = "CIRCUIT_OPEN"
STATE_SHUTDOWN = "SHUTDOWN"


# ============================================================
#
# OPTIONAL FOUNDATION IMPORTS
#
# ============================================================

try:

    from .module_registry import (
        module_registry,
        ModuleInfo,
        STATE_ERROR as FOUNDATION_STATE_ERROR,
        STATE_DISABLED as FOUNDATION_STATE_DISABLED,
    )

    FOUNDATION_REGISTRY_AVAILABLE = True

except Exception:

    FOUNDATION_REGISTRY_AVAILABLE = False

    module_registry = None
    ModuleInfo = None

    FOUNDATION_STATE_ERROR = STATE_ERROR
    FOUNDATION_STATE_DISABLED = STATE_DISABLED


try:

    from .contracts import (
        ModuleStatus,
        ModuleInput,
        ModuleOutput,
        create_input,
        normalize_output,
        safe_copy,
        utc_now,
        validate_output,
    )

    FOUNDATION_CONTRACTS_AVAILABLE = True

except Exception:

    FOUNDATION_CONTRACTS_AVAILABLE = False

    ModuleStatus = None
    ModuleInput = None
    ModuleOutput = None

    def safe_copy(value: Any) -> Any:

        try:
            return copy.deepcopy(value)

        except Exception:
            return value


    def utc_now() -> str:

        return datetime.now(
            timezone.utc
        ).isoformat()


    def create_input(
        data: Any = None,
        source: str = "engine",
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        return {

            "data": data,

            "source": source,

            "context": context or {},

            "metadata": metadata or {},

        }


    def normalize_output(
        output: Any,
        module_name: str = "unknown",
        request_id: Optional[str] = None,
    ) -> Any:

        return output


    def validate_output(
        output: Any,
    ) -> bool:

        return True


# ============================================================
#
# UTILITY
#
# ============================================================

def generate_id(prefix: str = "") -> str:

    value = uuid.uuid4().hex

    if prefix:
        return f"{prefix}_{value}"

    return value


def utc_timestamp() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()


# ============================================================
#
# SAFE SERIALIZER
#
# ============================================================

class SafeSerializer:
    """
    Converts arbitrary Python objects into safe serializable
    structures.

    Protects against:

    - circular references
    - excessive nesting
    - datetime
    - date
    - Path
    - Enum
    - bytes
    - sets
    - tuples
    - exceptions
    - NaN
    - infinity
    - unsupported objects
    """

    def __init__(
        self,
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> None:

        self.max_depth = max(
            1,
            int(max_depth),
        )

    def sanitize(
        self,
        value: Any,
        depth: int = 0,
        seen: Optional[Set[int]] = None,
    ) -> Any:

        if seen is None:
            seen = set()

        if depth > self.max_depth:
            return "<MAX_DEPTH>"

        if value is None:
            return None

        if isinstance(
            value,
            (str, int, bool),
        ):
            return value

        if isinstance(
            value,
            float,
        ):

            if math.isnan(value):
                return None

            if math.isinf(value):

                return (
                    "Infinity"
                    if value > 0
                    else "-Infinity"
                )

            return value

        if isinstance(
            value,
            datetime,
        ):

            if value.tzinfo is None:
                return value.isoformat()

            return value.astimezone(
                timezone.utc
            ).isoformat()

        if isinstance(
            value,
            date,
        ):

            return value.isoformat()

        if isinstance(
            value,
            Enum,
        ):

            return self.sanitize(
                value.value,
                depth + 1,
                seen,
            )

        if isinstance(
            value,
            Path,
        ):

            return str(value)

        if isinstance(
            value,
            bytes,
        ):

            try:

                return value.decode(
                    "utf-8",
                    errors="replace",
                )

            except Exception:

                return repr(value)

        if isinstance(
            value,
            (
                dict,
                list,
                tuple,
                set,
            ),
        ):

            object_id = id(value)

            if object_id in seen:

                return "<CIRCULAR_REFERENCE>"

            seen.add(object_id)

        if isinstance(
            value,
            dict,
        ):

            result = {}

            for key, item in value.items():

                try:

                    result[str(key)] = (
                        self.sanitize(
                            item,
                            depth + 1,
                            seen,
                        )
                    )

                except Exception:

                    result[str(key)] = (
                        "<UNSERIALIZABLE>"
                    )

            seen.discard(id(value))

            return result

        if isinstance(
            value,
            list,
        ):

            result = []

            for item in value:

                try:

                    result.append(
                        self.sanitize(
                            item,
                            depth + 1,
                            seen,
                        )
                    )

                except Exception:

                    result.append(
                        "<UNSERIALIZABLE>"
                    )

            seen.discard(id(value))

            return result

        if isinstance(
            value,
            tuple,
        ):

            result = [

                self.sanitize(
                    item,
                    depth + 1,
                    seen,
                )

                for item in value

            ]

            seen.discard(id(value))

            return result

        if isinstance(
            value,
            set,
        ):

            result = [

                self.sanitize(
                    item,
                    depth + 1,
                    seen,
                )

                for item in value

            ]

            seen.discard(id(value))

            return result

        if isinstance(
            value,
            BaseException,
        ):

            return {

                "type":
                    type(value).__name__,

                "message":
                    str(value),

            }

        if hasattr(
            value,
            "__dict__",
        ):

            try:

                return self.sanitize(
                    vars(value),
                    depth + 1,
                    seen,
                )

            except Exception:

                return repr(value)

        try:

            json.dumps(value)

            return value

        except Exception:
            pass

        try:

            return str(value)

        except Exception:

            return "<UNSERIALIZABLE>"

    def json_safe(
        self,
        value: Any,
    ) -> Any:

        return self.sanitize(value)


# ============================================================
#
# EXECUTION CONTEXT
#
# ============================================================

class LearningContext:

    def __init__(
        self,
        input_data: Any = None,
        cycle: int = 0,
        request_id: Optional[str] = None,
        execution_id: Optional[str] = None,
        source: str = "engine",
        parent_id: Optional[str] = None,
    ) -> None:

        self.created_at = utc_timestamp()

        self.cycle = cycle

        self.request_id = (
            request_id
            or generate_id("req")
        )

        self.execution_id = (
            execution_id
            or generate_id("exec")
        )

        self.parent_id = parent_id

        self.source = source

        self.input = input_data

        self.data: Dict[str, Any] = {}

        self.results: Dict[str, Any] = {}

        self.errors: List[
            Dict[str, Any]
        ] = []

        self.metadata: Dict[str, Any] = {

            "kernel":
                KERNEL_VERSION,

            "engine":
                ENGINE_VERSION,

            "created_at":
                self.created_at,

            "source":
                source,

        }

    def set(
        self,
        name: str,
        value: Any,
    ) -> None:

        self.results[
            str(name)
        ] = value

    def get(
        self,
        name: str,
        default: Any = None,
    ) -> Any:

        return self.results.get(
            name,
            default,
        )

    def set_data(
        self,
        name: str,
        value: Any,
    ) -> None:

        self.data[
            str(name)
        ] = value

    def add_error(
        self,
        module: str,
        error: Any,
    ) -> None:

        self.errors.append({

            "module":
                module,

            "error":
                str(error),

            "timestamp":
                utc_timestamp(),

        })

    def snapshot(
        self,
        serializer: SafeSerializer,
    ) -> Dict[str, Any]:

        payload = {

            "cycle":
                self.cycle,

            "request_id":
                self.request_id,

            "execution_id":
                self.execution_id,

            "parent_id":
                self.parent_id,

            "source":
                self.source,

            "input":
                self.input,

            "data":
                self.data,

            "results":
                self.results,

            "errors":
                self.errors,

            "metadata":
                self.metadata,

        }

        return serializer.sanitize(
            payload
        )


# ============================================================
#
# CIRCUIT BREAKER
#
# ============================================================

class CircuitBreaker:

    def __init__(
        self,
        threshold: int = DEFAULT_CIRCUIT_THRESHOLD,
        reset_seconds: int = DEFAULT_CIRCUIT_RESET,
    ) -> None:

        self.threshold = max(
            1,
            int(threshold),
        )

        self.reset_seconds = max(
            1,
            int(reset_seconds),
        )

        self.failures = 0

        self.opened_at = None

        self.lock = threading.RLock()

    def allow(self) -> bool:

        with self.lock:

            if self.opened_at is None:
                return True

            elapsed = (
                time.time()
                - self.opened_at
            )

            if elapsed >= self.reset_seconds:

                self.opened_at = None

                self.failures = 0

                return True

            return False

    def success(self) -> None:

        with self.lock:

            self.failures = 0
            self.opened_at = None

    def failure(self) -> None:

        with self.lock:

            self.failures += 1

            if (
                self.failures
                >= self.threshold
            ):

                self.opened_at = time.time()

    def state(self) -> str:

        with self.lock:

            if self.opened_at is None:
                return "CLOSED"

            if (
                time.time()
                - self.opened_at
                >= self.reset_seconds
            ):

                return "HALF_OPEN"

            return "OPEN"

    def reset(self) -> None:

        with self.lock:

            self.failures = 0
            self.opened_at = None


# ============================================================
#
# LOCAL MODULE SPEC
#
# ============================================================

class ModuleSpec:

    def __init__(
        self,
        name: str,
        module: Any,
        enabled: bool = True,
        priority: int = 100,
        dependencies: Optional[
            Iterable[str]
        ] = None,
        timeout: int = DEFAULT_MODULE_TIMEOUT,
        retries: int = DEFAULT_RETRY_COUNT,
        retry_backoff: float = DEFAULT_RETRY_BACKOFF,
        circuit_threshold: int = DEFAULT_CIRCUIT_THRESHOLD,
        circuit_reset: int = DEFAULT_CIRCUIT_RESET,
        version: Optional[str] = None,
        tags: Optional[
            Iterable[str]
        ] = None,
    ) -> None:

        self.name = name

        self.module = module  # <-- Ini yang penting!

        self.enabled = enabled

        self.priority = int(priority)

        self.dependencies = list(
            dependencies or []
        )

        self.timeout = max(
            1,
            int(timeout),
        )

        self.retries = max(
            0,
            int(retries),
        )

        self.retry_backoff = max(
            0.0,
            float(retry_backoff),
        )

        self.version = (
            version
            or getattr(
                module,
                "VERSION",
                "1.0",
            )
        )

        self.tags = list(
            tags or []
        )

        self.calls = 0

        self.executions = 0

        self.errors = 0

        self.timeouts = 0

        self.retries_used = 0

        self.last_error = None

        self.last_duration = 0.0

        self.last_execution = None

        self.registered_at = utc_timestamp()

        self.circuit = CircuitBreaker(

            threshold=
                circuit_threshold,

            reset_seconds=
                circuit_reset,

        )

        self.lock = threading.RLock()

    @property
    def available(self) -> bool:

        return self.module is not None

    def record_success(
        self,
        duration: float,
    ) -> None:

        with self.lock:

            self.calls += 1

            self.executions += 1

            self.last_duration = duration

            self.last_execution = (
                utc_timestamp()
            )

            self.last_error = None

            self.circuit.success()

    def record_error(
        self,
        error: Exception,
        duration: float,
        timeout: bool = False,
    ) -> None:

        with self.lock:

            self.calls += 1

            self.executions += 1

            self.errors += 1

            if timeout:
                self.timeouts += 1

            self.last_duration = duration

            self.last_execution = (
                utc_timestamp()
            )

            self.last_error = str(
                error
            )

            self.circuit.failure()

    def record_retry(self) -> None:

        with self.lock:
            self.retries_used += 1

    def reset_statistics(self) -> None:

        with self.lock:

            self.calls = 0
            self.executions = 0
            self.errors = 0
            self.timeouts = 0
            self.retries_used = 0
            self.last_error = None
            self.last_duration = 0.0
            self.last_execution = None
            self.circuit.reset()

    def status(self) -> Dict[str, Any]:

        with self.lock:

            return {

                "name":
                    self.name,

                "version":
                    self.version,

                "enabled":
                    self.enabled,

                "available":
                    self.available,

                "priority":
                    self.priority,

                "dependencies":
                    list(self.dependencies),

                "tags":
                    list(self.tags),

                "calls":
                    self.calls,

                "executions":
                    self.executions,

                "errors":
                    self.errors,

                "timeouts":
                    self.timeouts,

                "retries_used":
                    self.retries_used,

                "last_error":
                    self.last_error,

                "last_duration":
                    self.last_duration,

                "last_execution":
                    self.last_execution,

                "circuit":
                    self.circuit.state(),

                "registered_at":
                    self.registered_at,

            }


# ============================================================
#
# LOCAL MODULE REGISTRY
#
# ============================================================

class LocalModuleRegistry:

    def __init__(self) -> None:

        self._modules: Dict[
            str,
            ModuleSpec
        ] = {}

        self._lock = threading.RLock()

    def register(
        self,
        name: str,
        module: Any,
        enabled: bool = True,
        priority: int = 100,
        dependencies: Optional[
            Iterable[str]
        ] = None,
        **kwargs,
    ) -> ModuleSpec:

        if not name:

            raise ValueError(
                "Module name cannot be empty."
            )

        spec = ModuleSpec(

            name=name,

            module=module,  # <-- module disimpan di sini

            enabled=enabled,

            priority=priority,

            dependencies=dependencies,

            **kwargs,

        )

        with self._lock:

            self._modules[
                name
            ] = spec

        return spec

    def unregister(
        self,
        name: str,
    ) -> bool:

        with self._lock:

            return (
                self._modules.pop(
                    name,
                    None,
                )
                is not None
            )

    def get(
        self,
        name: str,
    ) -> Optional[ModuleSpec]:
        """
        Returns ModuleSpec, NOT the module directly.
        This is the key contract!
        """

        with self._lock:

            return self._modules.get(
                name
            )

    def descriptor(
        self,
        name: str,
    ) -> Optional[ModuleSpec]:

        return self.get(name)

    def get_info(
        self,
        name: str,
    ) -> Optional[ModuleSpec]:

        return self.get(name)

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.get(name) is not None

    def enable(
        self,
        name: str,
    ) -> bool:

        spec = self.get(name)

        if spec is None:
            return False

        with spec.lock:
            spec.enabled = True

        return True

    def disable(
        self,
        name: str,
    ) -> bool:

        spec = self.get(name)

        if spec is None:
            return False

        with spec.lock:
            spec.enabled = False

        return True

    def all(
        self,
    ) -> List[ModuleSpec]:

        with self._lock:

            return sorted(

                list(
                    self._modules.values()
                ),

                key=lambda item: (
                    item.priority,
                    item.name,
                ),

            )

    def list(
        self,
    ) -> List[ModuleSpec]:

        return self.all()

    def descriptors(
        self,
    ) -> List[ModuleSpec]:

        return self.all()

    def dependencies_available(
        self,
        name: str,
    ) -> bool:

        spec = self.get(name)

        if spec is None:
            return False

        for dependency in (
            spec.dependencies
        ):

            dep = self.get(
                dependency
            )

            if dep is None:
                return False

            if not dep.enabled:
                return False

            if not dep.available:
                return False

        return True

    def check_dependencies(
        self,
        name: str,
    ) -> Dict[str, Any]:

        spec = self.get(name)

        if spec is None:

            return {

                "ready":
                    False,

                "missing":
                    [name],

            }

        missing = []

        disabled = []

        unavailable = []

        for dependency in (
            spec.dependencies
        ):

            dep = self.get(
                dependency
            )

            if dep is None:

                missing.append(
                    dependency
                )

            elif not dep.enabled:

                disabled.append(
                    dependency
                )

            elif not dep.available:

                unavailable.append(
                    dependency
                )

        return {

            "ready":
                not (
                    missing
                    or disabled
                    or unavailable
                ),

            "missing":
                missing,

            "disabled":
                disabled,

            "unavailable":
                unavailable,

        }

    def status(
        self,
    ) -> Dict[str, Any]:

        with self._lock:

            return {

                name:
                    spec.status()

                for name, spec
                in self._modules.items()

            }


# ============================================================
#
# EVENT BUS
#
# ============================================================

class EventBus:

    def __init__(self) -> None:

        self._listeners: Dict[
            str,
            List[Callable]
        ] = {}

        self._lock = threading.RLock()

    def subscribe(
        self,
        event: str,
        callback: Callable,
    ) -> None:

        if not callable(callback):
            raise ValueError(
                "Event callback must be callable."
            )

        with self._lock:

            self._listeners.setdefault(
                event,
                [],
            ).append(
                callback
            )

    def unsubscribe(
        self,
        event: str,
        callback: Callable,
    ) -> None:

        with self._lock:

            listeners = (
                self._listeners.get(
                    event,
                    [],
                )
            )

            if callback in listeners:
                listeners.remove(
                    callback
                )

    def emit(
        self,
        event: str,
        payload: Any = None,
    ) -> None:

        with self._lock:

            listeners = list(
                self._listeners.get(
                    event,
                    [],
                )
            )

            listeners += list(
                self._listeners.get(
                    "*",
                    [],
                )
            )

        for callback in listeners:

            try:

                callback(
                    payload
                )

            except Exception:

                logger.exception(
                    "Event listener failed: %s",
                    event,
                )


# ============================================================
#
# MODULE EXECUTOR
#
# ============================================================

class ModuleExecutor:

    METHODS = (

        "execute",

        "process",

        "run",

        "analyze",

        "detect",

        "extract",

        "predict",

        "decide",

        "generate",

        "simulate",

        "store",

        "archive",

        "build",

    )

    def __init__(
        self,
        serializer: SafeSerializer,
        max_workers: int = DEFAULT_MAX_WORKERS,
    ) -> None:

        self.serializer = serializer

        self.max_workers = max(
            1,
            int(max_workers),
        )

        self.executor = (
            ThreadPoolExecutor(
                max_workers=
                    self.max_workers,

                thread_name_prefix=
                    "InksideModule",
            )
        )

    def resolve(
        self,
        module: Any,
    ) -> Optional[Callable]:

        if module is None:
            return None

        for method_name in self.METHODS:

            method = getattr(
                module,
                method_name,
                None,
            )

            if callable(method):

                return method

        if callable(module):

            return module

        return None

    def execute(
        self,
        spec: ModuleSpec,
        payload: Any,
    ) -> Dict[str, Any]:
        """
        Execute a module spec.

        Returns:
            {
                "status": "SUCCESS" | "ERROR" | "TIMEOUT" | "DISABLED" | "CIRCUIT_OPEN",
                "output": <module output>,  # only on SUCCESS
                "error": <error message>,   # only on ERROR/TIMEOUT
                "duration": <float>,
                "attempts": <int>
            }
        """

        if spec is None:

            return {

                "status":
                    STATE_ERROR,

                "error":
                    "Missing module specification.",

            }

        if not spec.enabled:

            return {

                "status":
                    STATE_DISABLED,

            }

        if not spec.available:

            return {

                "status":
                    STATE_ERROR,

                "error":
                    "Module unavailable.",

            }

        if not spec.circuit.allow():

            return {

                "status":
                    STATE_CIRCUIT_OPEN,

                "error":
                    "Module circuit breaker is open.",

            }

        method = self.resolve(
            spec.module  # <-- spec.module is the actual module
        )

        if method is None:

            return {

                "status":
                    STATE_ERROR,

                "error":
                    "Module has no supported interface.",

            }

        attempts = (
            spec.retries + 1
        )

        last_error = None

        for attempt in range(
            attempts
        ):

            start = time.perf_counter()

            try:

                try:

                    safe_payload = (
                        copy.deepcopy(
                            payload
                        )
                    )

                except Exception:

                    safe_payload = payload

                future = (
                    self.executor.submit(
                        method,
                        safe_payload,
                    )
                )

                try:

                    output = future.result(
                        timeout=
                            spec.timeout
                    )

                except FutureTimeoutError:

                    duration = (
                        time.perf_counter()
                        - start
                    )

                    error = TimeoutError(
                        f"Module '{spec.name}' "
                        f"timed out after "
                        f"{spec.timeout}s."
                    )

                    spec.record_error(
                        error,
                        duration,
                        timeout=True,
                    )

                    last_error = error

                    if attempt + 1 < attempts:

                        spec.record_retry()

                        self._backoff(
                            spec,
                            attempt,
                        )

                        continue

                    return {

                        "status":
                            STATE_TIMEOUT,

                        "error":
                            str(error),

                        "duration":
                            round(
                                duration,
                                6,
                            ),

                        "attempts":
                            attempt + 1,

                    }

                duration = (
                    time.perf_counter()
                    - start
                )

                spec.record_success(
                    duration
                )

                safe_output = (
                    self.serializer.sanitize(
                        output
                    )
                )

                return {

                    "status":
                        STATE_SUCCESS,

                    "output":
                        safe_output,  # <-- output ada di sini!

                    "duration":
                        round(
                            duration,
                            6,
                        ),

                    "attempts":
                        attempt + 1,

                }

            except Exception as exc:

                duration = (
                    time.perf_counter()
                    - start
                )

                spec.record_error(
                    exc,
                    duration,
                )

                last_error = exc

                if attempt + 1 < attempts:

                    spec.record_retry()

                    self._backoff(
                        spec,
                        attempt,
                    )

                    continue

                return {

                    "status":
                        STATE_ERROR,

                    "error":
                        str(exc),

                    "duration":
                        round(
                            duration,
                            6,
                        ),

                    "attempts":
                        attempt + 1,

                }

        return {

            "status":
                STATE_ERROR,

            "error":
                str(last_error)
                if last_error
                else "Unknown module error.",

        }

    def _backoff(
        self,
        spec: ModuleSpec,
        attempt: int,
    ) -> None:

        delay = (
            spec.retry_backoff
            * (
                2 ** attempt
            )
        )

        if delay > 0:
            time.sleep(delay)

    def shutdown(
        self,
    ) -> None:

        try:

            self.executor.shutdown(
                wait=False,
                cancel_futures=True,
            )

        except Exception:

            logger.exception(
                "Module executor shutdown failed."
            )


# ============================================================
#
# LEARNING ENGINE
#
# ============================================================

class LearningEngine:

    def __init__(
        self,
        registry: Any = None,
        config: Optional[
            Dict[str, Any]
        ] = None,
    ) -> None:

        # ----------------------------------------------------
        # Runtime
        # ----------------------------------------------------

        self.running = False

        self.thread: Optional[
            threading.Thread
        ] = None

        self.lock = threading.RLock()

        self.shutdown_event = (
            threading.Event()
        )

        # ----------------------------------------------------
        # Counters
        # ----------------------------------------------------

        self.cycles = 0

        self.errors = 0

        self.successful_cycles = 0

        self.failed_cycles = 0

        self.partial_cycles = 0

        self.total_execution_time = 0.0

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        self.last_result = None

        self.last_learning = None

        self.last_error = None

        self.history: List[
            Dict[str, Any]
        ] = []

        # ----------------------------------------------------
        # Infrastructure
        # ----------------------------------------------------

        self.serializer = (
            SafeSerializer()
        )

        self.events = EventBus()

        # ----------------------------------------------------
        # Registry - CRITICAL: Use LocalModuleRegistry
        # ----------------------------------------------------

        # ALWAYS use LocalModuleRegistry for consistency
        self.registry = LocalModuleRegistry()

        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------

        self.config = {

            "kernel":
                KERNEL_VERSION,

            "engine":
                ENGINE_VERSION,

            "max_history":
                MAX_HISTORY,

            "safe_mode":
                True,

            "copy_module_input":
                True,

            "continue_on_module_error":
                True,

            "learning_interval":
                DEFAULT_LEARNING_INTERVAL,

            "module_timeout":
                DEFAULT_MODULE_TIMEOUT,

            "retry_count":
                DEFAULT_RETRY_COUNT,

            "retry_backoff":
                DEFAULT_RETRY_BACKOFF,

            "max_workers":
                DEFAULT_MAX_WORKERS,

            "state_file":
                None,

        }

        if config:

            self.config.update(
                safe_copy(config)
            )

        self.executor = (
            ModuleExecutor(

                self.serializer,

                self.config.get(
                    "max_workers",
                    DEFAULT_MAX_WORKERS,
                ),

            )
        )

        logger.info(
            "%s v%s initialized.",
            ENGINE_NAME,
            ENGINE_VERSION,
        )

    # ========================================================
    #
    # EVENTS
    #
    # ========================================================

    def subscribe(
        self,
        event: str,
        callback: Callable,
    ) -> None:

        self.events.subscribe(
            event,
            callback,
        )

    def unsubscribe(
        self,
        event: str,
        callback: Callable,
    ) -> None:

        self.events.unsubscribe(
            event,
            callback,
        )

    # ========================================================
    #
    # MODULE MANAGEMENT
    #
    # ========================================================

    def register_module(
        self,
        name: str,
        module: Any,
        enabled: bool = True,
        priority: int = 100,
        dependencies: Optional[
            Iterable[str]
        ] = None,
        **kwargs,
    ):

        if not name:

            raise ValueError(
                "Module name cannot be empty."
            )

        # Use registry.register which returns ModuleSpec
        result = self.registry.register(

            name=name,

            module=module,

            enabled=enabled,

            priority=priority,

            dependencies=dependencies,

            **kwargs,

        )

        logger.info(
            "Learning module registered: %s",
            name,
        )

        self.events.emit(
            "module.registered",
            {
                "module":
                    name,
            },
        )

        return result

    def register_instance(
        self,
        module: Any,
        name: Optional[str] = None,
        **kwargs,
    ):

        module_name = (

            name

            or getattr(
                module,
                "NAME",
                None,
            )

            or getattr(
                module,
                "name",
                None,
            )

        )

        if not module_name:

            raise ValueError(
                "Unable to determine module name."
            )

        return self.register_module(
            module_name,
            module,
            **kwargs,
        )

    def unregister_module(
        self,
        name: str,
    ) -> bool:

        try:

            result = (
                self.registry.unregister(
                    name
                )
            )

            success = bool(
                result
                if result is not None
                else True
            )

            if success:

                self.events.emit(
                    "module.unregistered",
                    {
                        "module":
                            name,
                    },
                )

            return success

        except Exception as exc:

            logger.exception(
                "Unable to unregister module %s: %s",
                name,
                exc,
            )

            return False

    def enable_module(
        self,
        name: str,
    ) -> bool:

        try:

            result = (
                self.registry.enable(
                    name
                )
            )

            return bool(
                result
                if result is not None
                else True
            )

        except Exception as exc:

            logger.exception(
                "Unable to enable module %s: %s",
                name,
                exc,
            )

            return False

    def disable_module(
        self,
        name: str,
    ) -> bool:

        try:

            result = (
                self.registry.disable(
                    name
                )
            )

            return bool(
                result
                if result is not None
                else True
            )

        except Exception as exc:

            logger.exception(
                "Unable to disable module %s: %s",
                name,
                exc,
            )

            return False

    def get_module(
        self,
        name: str,
    ) -> Any:

        try:

            spec = self.registry.get(
                name
            )

            if spec is None:
                return None

            return spec.module  # <-- Get module from spec

        except Exception:

            return None

    def module_exists(
        self,
        name: str,
    ) -> bool:

        try:

            return self.registry.exists(
                name
            )

        except Exception:

            return False

    # ========================================================
    #
    # MODULE SPECS
    #
    # ========================================================

    def _get_specs(
        self,
    ) -> List[Any]:

        return self.registry.all()

    # ========================================================
    #
    # DEPENDENCY CHECK
    #
    # ========================================================

    def _dependencies_ready(
        self,
        name: str,
    ) -> bool:

        return self.registry.dependencies_available(
            name
        )

    # ========================================================
    #
    # TOPOLOGICAL EXECUTION ORDER
    #
    # ========================================================

    def _execution_order(
        self,
        specs: List[Any],
    ) -> List[Any]:

        # Simple priority-based order
        return sorted(
            specs,
            key=lambda spec: (
                spec.priority,
                spec.name,
            )
        )

    # ========================================================
    #
    # EXECUTE MODULE
    #
    # ========================================================

    def execute_module(
        self,
        name: str,
        payload: Any = None,
    ) -> Any:

        spec = None

        try:

            spec = self.registry.get(
                name
            )

            if spec is None:

                logger.debug(
                    "Unknown learning module: %s",
                    name,
                )

                return None

            if not self._dependencies_ready(
                name
            ):

                logger.warning(
                    "Module dependencies unavailable: %s",
                    name,
                )

                return None

            # Execute using ModuleExecutor
            execution = (
                self.executor.execute(
                    spec,
                    payload,
                )
            )

            status = execution.get(
                "status"
            )

            if status != STATE_SUCCESS:

                self.errors += 1

                self.last_error = (
                    execution.get(
                        "error"
                    )
                )

                self.events.emit(
                    "module.error",
                    {
                        "module":
                            name,

                        "execution":
                            execution,

                    },
                )

                return None

            self.events.emit(
                "module.executed",
                {
                    "module":
                        name,

                    "execution":
                        execution,

                },
            )

            return execution.get(
                "output"
            )

        except Exception as exc:

            self.errors += 1

            self.last_error = str(
                exc
            )

            logger.exception(
                "Module execution failed [%s]: %s",
                name,
                exc,
            )

            self.events.emit(
                "module.error",
                {
                    "module":
                        name,

                    "error":
                        str(exc),

                },
            )

            return None

    # ========================================================
    #
    # BUILD CONTEXT
    #
    # ========================================================

    def create_context(
        self,
        data: Any,
        request_id: Optional[str] = None,
        source: str = "engine",
        parent_id: Optional[str] = None,
    ) -> LearningContext:

        return LearningContext(

            input_data=data,

            cycle=self.cycles + 1,

            request_id=request_id,

            source=source,

            parent_id=parent_id,

        )

    # ========================================================
    #
    # BUILD MODULE PAYLOAD
    #
    # ========================================================

    def _build_payload(
        self,
        context: LearningContext,
    ) -> Dict[str, Any]:

        return {

            "input":
                safe_copy(
                    context.input
                ),

            "cycle":
                context.cycle,

            "request_id":
                context.request_id,

            "execution_id":
                context.execution_id,

            "parent_id":
                context.parent_id,

            "source":
                context.source,

            "data":
                safe_copy(
                    context.data
                ),

            "results":
                safe_copy(
                    context.results
                ),

            "metadata":
                safe_copy(
                    context.metadata
                ),

        }

    # ========================================================
    #
    # LEARNING PIPELINE
    #
    # ========================================================

    def learn(
        self,
        data: Any,
        request_id: Optional[str] = None,
        source: str = "engine",
        parent_id: Optional[str] = None,
    ) -> Dict[str, Any]:

        with self.lock:

            start = time.perf_counter()

            next_cycle = (
                self.cycles + 1
            )

            context = (
                self.create_context(
                    data,
                    request_id=
                        request_id,
                    source=
                        source,
                    parent_id=
                        parent_id,
                )
            )

            result = {

                "status":
                    STATE_RUNNING,

                "timestamp":
                    utc_timestamp(),

                "request_id":
                    context.request_id,

                "execution_id":
                    context.execution_id,

                "cycle":
                    next_cycle,

                "source":
                    source,

                "input":
                    self.serializer.sanitize(
                        data
                    ),

                "modules":
                    {},

                "errors":
                    [],

            }

            self.events.emit(
                "learning.started",
                result,
            )

            module_specs = (
                self._execution_order(
                    self._get_specs()
                )
            )

            for spec in module_specs:

                name = spec.name

                if not spec.enabled:

                    result[
                        "modules"
                    ][name] = {

                        "status":
                            STATE_DISABLED,

                    }

                    continue

                if not self._dependencies_ready(
                    name
                ):

                    result[
                        "modules"
                    ][name] = {

                        "status":
                            STATE_DEPENDENCY_ERROR,

                    }

                    result[
                        "errors"
                    ].append({

                        "module":
                            name,

                        "error":
                            "Dependencies unavailable.",

                    })

                    context.add_error(
                        name,
                        "Dependencies unavailable.",
                    )

                    continue

                payload = (
                    self._build_payload(
                        context
                    )
                )

                try:

                    output = (
                        self.execute_module(
                            name,
                            payload,
                        )
                    )

                    if output is None:

                        result[
                            "modules"
                        ][name] = {

                            "status":
                                STATE_NO_OUTPUT,

                        }

                        continue

                    safe_output = (
                        self.serializer.sanitize(
                            output
                        )
                    )

                    context.set(
                        name,
                        safe_output,
                    )

                    result[
                        "modules"
                    ][name] = {

                        "status":
                            STATE_SUCCESS,

                        "output":
                            safe_output,

                    }

                except Exception as exc:

                    self.errors += 1

                    error_info = {

                        "module":
                            name,

                        "error":
                            str(exc),

                        "timestamp":
                            utc_timestamp(),

                    }

                    result[
                        "errors"
                    ].append(
                        error_info
                    )

                    context.add_error(
                        name,
                        exc,
                    )

                    result[
                        "modules"
                    ][name] = {

                        "status":
                            STATE_ERROR,

                        "error":
                            str(exc),

                    }

                    if not self.config.get(
                        "continue_on_module_error",
                        True,
                    ):

                        break

            result[
                "results"
            ] = self.serializer.sanitize(
                context.results
            )

            result[
                "context"
            ] = {

                "request_id":
                    context.request_id,

                "execution_id":
                    context.execution_id,

                "parent_id":
                    context.parent_id,

                "source":
                    context.source,

            }

            duration = (
                time.perf_counter()
                - start
            )

            self.total_execution_time += (
                duration
            )

            result[
                "engine"
            ] = {

                "name":
                    ENGINE_NAME,

                "version":
                    ENGINE_VERSION,

                "kernel":
                    KERNEL_VERSION,

                "cycle":
                    next_cycle,

                "duration":
                    round(
                        duration,
                        6,
                    ),

                "registered_modules":
                    len(
                        module_specs
                    ),

            }

            errors = result[
                "errors"
            ]

            if errors:

                result[
                    "status"
                ] = STATE_PARTIAL

                self.failed_cycles += 1

                self.partial_cycles += 1

            else:

                result[
                    "status"
                ] = STATE_SUCCESS

                self.successful_cycles += 1

            result = (
                self.serializer.sanitize(
                    result
                )
            )

            self.cycles += 1

            self.last_learning = (
                utc_timestamp()
            )

            self.last_result = result

            self.history.append(
                result
            )

            max_history = int(
                self.config.get(
                    "max_history",
                    MAX_HISTORY,
                )
            )

            if (
                max_history > 0
                and
                len(self.history)
                > max_history
            ):

                self.history = (
                    self.history[
                        -max_history:
                    ]
                )

            self.events.emit(
                "learning.completed",
                result,
            )

            self._persist_state_safe()

            return result

    # ========================================================
    #
    # BATCH LEARNING
    #
    # ========================================================

    def learn_batch(
        self,
        dataset: Iterable[Any],
    ) -> List[
        Dict[str, Any]
    ]:

        results = []

        if dataset is None:
            return results

        for item in dataset:

            if not self.running and (
                self.shutdown_event.is_set()
            ):

                break

            try:

                results.append(
                    self.learn(item)
                )

            except Exception as exc:

                self.errors += 1

                logger.exception(
                    "Batch learning error: %s",
                    exc,
                )

                results.append({

                    "status":
                        STATE_ERROR,

                    "error":
                        str(exc),

                })

        return results

    # ========================================================
    #
    # OBSERVE
    #
    # ========================================================

    def observe(
        self,
        data: Any,
    ) -> Dict[str, Any]:

        return self.learn(
            data,
            source="observe",
        )

    # ========================================================
    #
    # FEEDBACK
    #
    # ========================================================

    def feedback(
        self,
        result: Any,
    ) -> Dict[str, Any]:

        feedback_data = {

            "timestamp":
                utc_timestamp(),

            "type":
                "feedback",

            "request_id":
                generate_id("feedback"),

            "data":
                self.serializer.sanitize(
                    result
                ),

        }

        self.events.emit(
            "feedback.received",
            feedback_data,
        )

        evaluation = (
            self.execute_module(
                "evaluator",
                feedback_data,
            )
        )

        reflection = (
            self.execute_module(
                "reflection",
                {

                    "feedback":
                        feedback_data,

                    "evaluation":
                        evaluation,

                },
            )
        )

        improvement = (
            self.execute_module(
                "improvement",
                {

                    "feedback":
                        feedback_data,

                    "evaluation":
                        evaluation,

                    "reflection":
                        reflection,

                },
            )
        )

        response = {

            "status":
                "OK",

            "evaluation":
                evaluation,

            "reflection":
                reflection,

            "improvement":
                improvement,

        }

        response = (
            self.serializer.sanitize(
                response
            )
        )

        self.events.emit(
            "feedback.completed",
            response,
        )

        return response

    # ========================================================
    #
    # INSIGHT
    #
    # ========================================================

    def get_insight(
        self,
    ) -> Any:

        if not self.last_result:
            return None

        modules = (
            self.last_result.get(
                "modules",
                {},
            )
        )

        insight = modules.get(
            "insight"
        )

        if isinstance(
            insight,
            dict,
        ):

            return insight.get(
                "output"
            )

        return insight

    # ========================================================
    #
    # HISTORY
    #
    # ========================================================

    def get_history(
        self,
        limit: Optional[int] = None,
    ) -> List[
        Dict[str, Any]
    ]:

        with self.lock:

            history = list(
                self.history
            )

            if limit is None:
                return history

            try:

                limit = int(
                    limit
                )

            except Exception:

                return history

            if limit <= 0:
                return []

            return history[
                -limit:
            ]

    # ========================================================
    #
    # STATE
    #
    # ========================================================

    def get_state(
        self,
    ) -> Dict[str, Any]:

        average = 0.0

        if self.cycles > 0:

            average = (
                self.total_execution_time
                / self.cycles
            )

        return {

            "kernel":
                KERNEL_VERSION,

            "engine":
                ENGINE_VERSION,

            "cycles":
                self.cycles,

            "successful_cycles":
                self.successful_cycles,

            "failed_cycles":
                self.failed_cycles,

            "partial_cycles":
                self.partial_cycles,

            "errors":
                self.errors,

            "average_cycle_duration":
                round(
                    average,
                    6,
                ),

            "total_execution_time":
                round(
                    self.total_execution_time,
                    6,
                ),

            "learning":
                self.running,

            "last_learning":
                self.last_learning,

            "last_error":
                self.last_error,

            "history":
                len(
                    self.history
                ),

        }

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self,
    ) -> Dict[str, Any]:

        try:

            modules = (
                self.registry.status()
            )

        except Exception:

            modules = {}

        online = []

        offline = []

        disabled = []

        errors = []

        circuit_open = []

        for name, info in (
            modules.items()
        ):

            enabled = info.get(
                "enabled",
                True,
            )

            state = info.get(
                "state"
            )

            available = info.get(
                "available",
                True,
            )

            circuit = info.get(
                "circuit",
                "CLOSED",
            )

            if not enabled:

                disabled.append(
                    name
                )

            elif circuit == "OPEN":

                circuit_open.append(
                    name
                )

            elif state == STATE_ERROR:

                errors.append(
                    name
                )

            elif not available:

                offline.append(
                    name
                )

            else:

                online.append(
                    name
                )

        return {

            "engine":
                "ONLINE",

            "kernel_version":
                KERNEL_VERSION,

            "engine_version":
                ENGINE_VERSION,

            "running":
                self.running,

            "cycles":
                self.cycles,

            "errors":
                self.errors,

            "successful_cycles":
                self.successful_cycles,

            "failed_cycles":
                self.failed_cycles,

            "partial_cycles":
                self.partial_cycles,

            "modules_online":
                online,

            "modules_offline":
                offline,

            "modules_disabled":
                disabled,

            "modules_error":
                errors,

            "modules_circuit_open":
                circuit_open,

            "module_count":
                len(modules),

            "history":
                len(
                    self.history
                ),

        }

    # ========================================================
    #
    # HEALTH
    #
    # ========================================================

    def health(
        self,
    ) -> Dict[str, Any]:

        status = self.status()

        healthy = (
            status["engine"]
            == "ONLINE"
        )

        if status[
            "modules_error"
        ]:

            healthy = False

        if status[
            "modules_circuit_open"
        ]:

            healthy = False

        return {

            "healthy":
                healthy,

            "engine":
                ENGINE_NAME,

            "version":
                ENGINE_VERSION,

            "running":
                self.running,

            "cycles":
                self.cycles,

            "errors":
                self.errors,

            "modules":
                status[
                    "module_count"
                ],

            "module_errors":
                len(
                    status[
                        "modules_error"
                    ]
                ),

            "circuits_open":
                len(
                    status[
                        "modules_circuit_open"
                    ]
                ),

        }

    # ========================================================
    #
    # DIAGNOSTICS
    #
    # ========================================================

    def diagnostics(
        self,
    ) -> Dict[str, Any]:

        return {

            "kernel": {

                "name":
                    KERNEL_NAME,

                "version":
                    KERNEL_VERSION,

            },

            "engine":
                self.get_state(),

            "health":
                self.health(),

            "registry":
                self.status(),

            "foundation": {

                "registry":
                    FOUNDATION_REGISTRY_AVAILABLE,

                "contracts":
                    FOUNDATION_CONTRACTS_AVAILABLE,

            },

            "configuration":
                self.serializer.sanitize(
                    self.config
                ),

        }

    # ========================================================
    #
    # SNAPSHOT
    #
    # ========================================================

    def snapshot(
        self,
    ) -> Dict[str, Any]:

        snapshot = {

            "kernel": {

                "name":
                    KERNEL_NAME,

                "version":
                    KERNEL_VERSION,

            },

            "engine": {

                "name":
                    ENGINE_NAME,

                "version":
                    ENGINE_VERSION,

                "status":
                    (
                        STATE_RUNNING
                        if self.running
                        else STATE_IDLE
                    ),

                "cycles":
                    self.cycles,

                "errors":
                    self.errors,

                "successful_cycles":
                    self.successful_cycles,

                "failed_cycles":
                    self.failed_cycles,

                "partial_cycles":
                    self.partial_cycles,

            },

            "learning": {

                "last":
                    self.last_learning,

                "history":
                    len(
                        self.history
                    ),

            },

            "insight":
                self.get_insight(),

            "modules":
                self.status(),

        }

        return (
            self.serializer.sanitize(
                snapshot
            )
        )

    # ========================================================
    #
    # AUTONOMOUS LEARNING LOOP
    #
    # ========================================================

    def learning_loop(
        self,
        interval: int = DEFAULT_LEARNING_INTERVAL,
    ) -> None:

        try:

            interval = max(
                1,
                int(interval),
            )

        except Exception:

            interval = (
                DEFAULT_LEARNING_INTERVAL
            )

        logger.info(
            "Autonomous learning loop started."
        )

        self.events.emit(
            "engine.started",
            {
                "interval":
                    interval,
            },
        )

        while (
            self.running
            and not self.shutdown_event.is_set()
        ):

            try:

                collector = (
                    self.get_module(
                        "collector"
                    )
                )

                if collector:

                    data = (
                        self.execute_module(
                            "collector",
                            None,
                        )
                    )

                    if data is not None:

                        self.learn(
                            data,
                            source="autonomous",
                        )

                else:

                    logger.debug(
                        "Collector module not registered."
                    )

            except Exception as exc:

                self.errors += 1

                self.last_error = str(
                    exc
                )

                logger.exception(
                    "Learning loop error: %s",
                    exc,
                )

                self.events.emit(
                    "engine.error",
                    {
                        "error":
                            str(exc),
                    },
                )

            # ------------------------------------------------
            # Interruptible sleep
            # ------------------------------------------------

            self.shutdown_event.wait(
                timeout=interval
            )

        logger.info(
            "Autonomous learning loop stopped."
        )

        self.events.emit(
            "engine.stopped",
            {},
        )

    # ========================================================
    #
    # START
    #
    # ========================================================

    def start_learning(
        self,
        interval: int = DEFAULT_LEARNING_INTERVAL,
    ) -> bool:

        try:

            interval = max(
                1,
                int(interval),
            )

        except Exception:

            interval = (
                DEFAULT_LEARNING_INTERVAL
            )

        with self.lock:

            # FIX: If thread died but running flag is True, reset it
            if self.running:
                # Check if the thread is actually alive
                if self.thread and not self.thread.is_alive():
                    logger.warning(
                        "Learning thread is dead but running flag is True. Resetting."
                    )
                    self.running = False
                    self.thread = None
                else:
                    logger.warning(
                        "Learning already running."
                    )
                    return False

            self.running = True

            self.shutdown_event.clear()

            self.config[
                "learning_interval"
            ] = interval

            self.thread = (
                threading.Thread(

                    target=
                        self.learning_loop,

                    args=(
                        interval,
                    ),

                    daemon=True,

                    name=
                        "InksideLearningEngine",

                )
            )

            self.thread.start()

            logger.info(
                "Autonomous Learning enabled."
            )

            return True

    # ========================================================
    #
    # STOP
    #
    # ========================================================

    def stop_learning(
        self,
    ) -> bool:

        with self.lock:

            self.running = False

            self.shutdown_event.set()

            thread = self.thread

            self.thread = None

        if thread:

            try:

                if (
                    thread.is_alive()
                    and
                    thread
                    is not threading.current_thread()
                ):

                    thread.join(
                        timeout=5
                    )

            except Exception:

                logger.exception(
                    "Learning thread shutdown error."
                )

        logger.info(
            "Learning stopped."
        )

        return True

    # ========================================================
    #
    # ALIASES FOR GUI COMPATIBILITY
    #
    # ========================================================

    def start(
        self,
        interval: int = DEFAULT_LEARNING_INTERVAL,
    ) -> bool:
        """Alias for start_learning() for GUI compatibility."""
        return self.start_learning(interval)

    def stop(
        self,
    ) -> bool:
        """Alias for stop_learning() for GUI compatibility."""
        return self.stop_learning()

    def is_running(
        self,
    ) -> bool:
        """Check if the learning engine is running."""
        with self.lock:
            if not self.running:
                return False
            if self.thread and not self.thread.is_alive():
                # Thread died but flag is True - correct it
                self.running = False
                self.thread = None
                return False
            return True

    # ========================================================
    #
    # PERSISTENCE
    #
    # ========================================================

    def _persist_state_safe(
        self,
    ) -> None:

        path = self.config.get(
            "state_file"
        )

        if not path:
            return

        try:

            self.save_state(
                path
            )

        except Exception:

            logger.exception(
                "Unable to persist engine state."
            )

    def save_state(
        self,
        path: Optional[
            str | Path
        ] = None,
    ) -> bool:

        path = (
            path
            or self.config.get(
                "state_file"
            )
        )

        if not path:

            return False

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {

            "kernel":
                KERNEL_NAME,

            "kernel_version":
                KERNEL_VERSION,

            "engine":
                ENGINE_NAME,

            "engine_version":
                ENGINE_VERSION,

            "saved_at":
                utc_timestamp(),

            "state":
                self.get_state(),

            "history":
                self.get_history(),

        }

        safe_payload = (
            self.serializer.sanitize(
                payload
            )
        )

        temp_path = (
            path.with_suffix(
                path.suffix
                + ".tmp"
            )
        )

        with open(
            temp_path,
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                safe_payload,
                handle,
                ensure_ascii=False,
                indent=2,
            )

        temp_path.replace(
            path
        )

        return True

    def load_state(
        self,
        path: Optional[
            str | Path
        ] = None,
    ) -> bool:

        path = (
            path
            or self.config.get(
                "state_file"
            )
        )

        if not path:
            return False

        path = Path(path)

        if not path.exists():
            return False

        try:

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as handle:

                payload = json.load(
                    handle
                )

            state = payload.get(
                "state",
                {}
            )

            history = payload.get(
                "history",
                []
            )

            with self.lock:

                self.cycles = int(
                    state.get(
                        "cycles",
                        0,
                    )
                )

                self.errors = int(
                    state.get(
                        "errors",
                        0,
                    )
                )

                self.successful_cycles = int(
                    state.get(
                        "successful_cycles",
                        0,
                    )
                )

                self.failed_cycles = int(
                    state.get(
                        "failed_cycles",
                        0,
                    )
                )

                self.partial_cycles = int(
                    state.get(
                        "partial_cycles",
                        0,
                    )
                )

                self.last_learning = (
                    state.get(
                        "last_learning"
                    )
                )

                self.last_error = (
                    state.get(
                        "last_error"
                    )
                )

                if isinstance(
                    history,
                    list,
                ):

                    max_history = int(
                        self.config.get(
                            "max_history",
                            MAX_HISTORY,
                        )
                    )

                    self.history = (
                        history[
                            -max_history:
                        ]
                        if max_history > 0
                        else []
                    )

            logger.info(
                "Learning Engine state restored."
            )

            return True

        except Exception as exc:

            logger.exception(
                "Learning Engine state restore failed: %s",
                exc,
            )

            return False

    # ========================================================
    #
    # SHUTDOWN
    #
    # ========================================================

    def shutdown(
        self,
    ) -> bool:

        try:

            self.stop_learning()

            self._persist_state_safe()

            self.executor.shutdown()

            logger.info(
                "Learning Engine shutdown complete."
            )

            return True

        except Exception as exc:

            logger.exception(
                "Learning Engine shutdown failed: %s",
                exc,
            )

            return False

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self,
        clear_module_statistics: bool = False,
        clear_history: bool = True,
    ) -> bool:

        try:

            self.stop_learning()

            with self.lock:

                if clear_history:

                    self.history.clear()

                self.cycles = 0

                self.errors = 0

                self.successful_cycles = 0

                self.failed_cycles = 0

                self.partial_cycles = 0

                self.total_execution_time = 0.0

                self.last_result = None

                self.last_learning = None

                self.last_error = None

                if clear_module_statistics:

                    for spec in (
                        self._get_specs()
                    ):

                        if hasattr(
                            spec,
                            "reset_statistics",
                        ):

                            try:

                                spec.reset_statistics()

                            except Exception:

                                logger.exception(
                                    "Unable to reset module statistics."
                                )

                        else:

                            for attribute in (

                                "calls",

                                "executions",

                                "errors",

                                "timeouts",

                                "retries_used",

                            ):

                                if hasattr(
                                    spec,
                                    attribute,
                                ):

                                    setattr(
                                        spec,
                                        attribute,
                                        0,
                                    )

                            for attribute in (

                                "last_error",

                                "last_execution",

                            ):

                                if hasattr(
                                    spec,
                                    attribute,
                                ):

                                    setattr(
                                        spec,
                                        attribute,
                                        None,
                                    )

                            if hasattr(
                                spec,
                                "last_duration",
                            ):

                                spec.last_duration = 0.0

                logger.info(
                    "Learning Engine reset."
                )

                self.events.emit(
                    "engine.reset",
                    {},
                )

                return True

        except Exception as exc:

            logger.exception(
                "Learning Engine reset failed: %s",
                exc,
            )

            return False


# ============================================================
#
# GLOBAL ENGINE INSTANCE
#
# ============================================================

learning_engine = LearningEngine()


# ============================================================
#
# PUBLIC API
#
# ============================================================

__all__ = [

    "KERNEL_NAME",

    "KERNEL_VERSION",

    "ENGINE_NAME",

    "ENGINE_VERSION",

    "MAX_HISTORY",

    "STATE_IDLE",

    "STATE_RUNNING",

    "STATE_SUCCESS",

    "STATE_PARTIAL",

    "STATE_ERROR",

    "STATE_TIMEOUT",

    "STATE_DISABLED",

    "STATE_DEPENDENCY_ERROR",

    "STATE_NO_OUTPUT",

    "STATE_CIRCUIT_OPEN",

    "STATE_SHUTDOWN",

    "SafeSerializer",

    "LearningContext",

    "CircuitBreaker",

    "ModuleSpec",

    "LocalModuleRegistry",

    "EventBus",

    "ModuleExecutor",

    "LearningEngine",

    "learning_engine",

]