# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# MODULE REGISTRY
# FOUNDATION v4.3
#
# Compatible Engine API: v1.1
#
# ============================================================
#
# PURPOSE
# ------------------------------------------------------------
#
# Central registry and orchestration layer for all
# INKSIDE Intelligence OS modules.
#
# Design goals:
#
# - Stable public API
# - Backward compatibility
# - Thread safety
# - Dynamic registration
# - Runtime enable / disable
# - Module lifecycle management
# - Version tracking
# - Dependency management
# - Dependency ordering
# - Circular dependency detection
# - Module health monitoring
# - Runtime metrics
# - Execution timing
# - Batch execution
# - Capability / tag discovery
# - Alias support
# - Safe error isolation
# - Critical module tracking
# - Registry snapshots
# - Deterministic behavior
# - Future-proof extension
# - No dependency on engine.py
#
# IMPORTANT
# ------------------------------------------------------------
#
# engine.py must NOT contain module-specific registry logic.
#
# New intelligence modules should register themselves here.
#
# Supported execution interfaces:
#
#   1. process()
#   2. execute()
#   3. run()
#   4. callable object
#
# Optional lifecycle hooks:
#
#   initialize()
#   shutdown()
#   reset()
#   health()
#   on_error()
#
# ============================================================

from __future__ import annotations

import logging
import threading
import time
import traceback

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
)


logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

REGISTRY_VERSION = "4.3"
API_VERSION = "1.1"

REGISTRY_NAME = "INKSIDE_MODULE_REGISTRY"


# ============================================================
#
# MODULE STATES
#
# ============================================================

MODULE_REGISTERED = "REGISTERED"
MODULE_INITIALIZING = "INITIALIZING"
MODULE_ONLINE = "ONLINE"
MODULE_OFFLINE = "OFFLINE"
MODULE_DISABLED = "DISABLED"
MODULE_ERROR = "ERROR"
MODULE_SHUTTING_DOWN = "SHUTTING_DOWN"
MODULE_UNKNOWN = "UNKNOWN"


VALID_MODULE_STATES = {
    MODULE_REGISTERED,
    MODULE_INITIALIZING,
    MODULE_ONLINE,
    MODULE_OFFLINE,
    MODULE_DISABLED,
    MODULE_ERROR,
    MODULE_SHUTTING_DOWN,
    MODULE_UNKNOWN,
}


# ============================================================
#
# EXECUTION INTERFACES
#
# ============================================================

EXECUTION_PROCESS = "process"
EXECUTION_EXECUTE = "execute"
EXECUTION_RUN = "run"
EXECUTION_CALLABLE = "callable"

VALID_EXECUTION_INTERFACES = {
    EXECUTION_PROCESS,
    EXECUTION_EXECUTE,
    EXECUTION_RUN,
    EXECUTION_CALLABLE,
}


# ============================================================
#
# TIME
#
# ============================================================

def utc_now() -> str:
    """
    Return current UTC time as ISO-8601 string.
    """

    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


# ============================================================
#
# SAFE HELPERS
#
# ============================================================

def _safe_str(value: Any) -> str:
    """
    Safely convert arbitrary value to string.
    """

    try:
        return str(value)

    except Exception:
        return "<UNSERIALIZABLE>"


def _normalize_name(value: Any) -> str:
    """
    Normalize module names and aliases.
    """

    if value is None:
        return ""

    try:
        return str(value).strip()

    except Exception:
        return ""


def _safe_list(value: Any) -> List[Any]:
    """
    Safely convert iterable values into a list.
    """

    if value is None:
        return []

    if isinstance(value, str):
        return [value]

    try:
        return list(value)

    except Exception:
        return []


def _normalize_names(value: Any) -> List[str]:
    """
    Normalize a collection of names.

    Empty values are removed.
    Duplicates are removed while preserving order.
    """

    result: List[str] = []
    seen: Set[str] = set()

    for item in _safe_list(value):

        normalized = _normalize_name(item)

        if not normalized:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)
        result.append(normalized)

    return result


def _safe_metadata(
    value: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Safely copy metadata.
    """

    if not isinstance(value, dict):
        return {}

    try:
        return dict(value)

    except Exception:
        return {}


# ============================================================
#
# MODULE DESCRIPTOR
#
# ============================================================

@dataclass
class ModuleDescriptor:
    """
    Registry metadata and runtime state for one module.
    """

    name: str
    module: Any

    version: str = "1.0"

    enabled: bool = True
    state: str = MODULE_REGISTERED

    priority: int = 50
    critical: bool = False

    dependencies: List[str] = field(
        default_factory=list
    )

    tags: List[str] = field(
        default_factory=list
    )

    capabilities: List[str] = field(
        default_factory=list
    )

    aliases: List[str] = field(
        default_factory=list
    )

    description: str = ""

    execution_interface: str = (
        EXECUTION_PROCESS
    )

    registered_at: str = field(
        default_factory=utc_now
    )

    initialized_at: Optional[str] = None
    shutdown_at: Optional[str] = None

    last_execution: Optional[str] = None
    last_success: Optional[str] = None
    last_failure: Optional[str] = None

    executions: int = 0
    successes: int = 0
    failures: int = 0

    total_duration: float = 0.0
    last_duration: float = 0.0

    min_duration: Optional[float] = None
    max_duration: Optional[float] = None

    errors: int = 0

    last_error: Optional[str] = None
    last_result: Any = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    lock: Any = field(
        default=None,
        repr=False,
        compare=False
    )

    # ========================================================
    #
    # POST INIT
    #
    # ========================================================

    def __post_init__(self) -> None:

        if self.lock is None:
            self.lock = threading.RLock()

    # ========================================================
    #
    # SUCCESS RATE
    #
    # ========================================================

    def success_rate(self) -> float:

        with self.lock:

            if self.executions <= 0:
                return 0.0

            return (
                self.successes
                / self.executions
            ) * 100.0

    # ========================================================
    #
    # AVERAGE DURATION
    #
    # ========================================================

    def average_duration(self) -> float:

        with self.lock:

            if self.executions <= 0:
                return 0.0

            return (
                self.total_duration
                / self.executions
            )

    # ========================================================
    #
    # EXECUTION MARK
    #
    # ========================================================

    def mark_execution(
        self,
        duration: float
    ) -> None:

        with self.lock:

            try:
                duration_value = float(
                    duration
                )
            except Exception:
                duration_value = 0.0

            duration_value = max(
                0.0,
                duration_value
            )

            self.executions += 1

            self.last_execution = utc_now()

            self.last_duration = (
                duration_value
            )

            self.total_duration += (
                duration_value
            )

            if (
                self.min_duration is None
                or duration_value
                < self.min_duration
            ):
                self.min_duration = (
                    duration_value
                )

            if (
                self.max_duration is None
                or duration_value
                > self.max_duration
            ):
                self.max_duration = (
                    duration_value
                )

    # ========================================================
    #
    # SUCCESS
    #
    # ========================================================

    def mark_success(
        self,
        result: Any = None
    ) -> None:

        with self.lock:

            self.successes += 1

            self.last_success = utc_now()

            self.last_result = result

            self.state = MODULE_ONLINE

            self.last_error = None

    # ========================================================
    #
    # ERROR
    #
    # ========================================================

    def mark_error(
        self,
        error: Exception | str
    ) -> None:

        with self.lock:

            self.errors += 1
            self.failures += 1

            self.last_failure = utc_now()

            self.last_error = _safe_str(
                error
            )

            self.state = MODULE_ERROR

    # ========================================================
    #
    # ONLINE
    #
    # ========================================================

    def mark_online(self) -> None:

        with self.lock:

            if self.enabled:
                self.state = MODULE_ONLINE

    # ========================================================
    #
    # OFFLINE
    #
    # ========================================================

    def mark_offline(self) -> None:

        with self.lock:
            self.state = MODULE_OFFLINE

    # ========================================================
    #
    # DISABLED
    #
    # ========================================================

    def mark_disabled(self) -> None:

        with self.lock:

            self.enabled = False
            self.state = MODULE_DISABLED

    # ========================================================
    #
    # ENABLED
    #
    # ========================================================

    def mark_enabled(self) -> None:

        with self.lock:

            self.enabled = True

            if self.state == MODULE_DISABLED:
                self.state = MODULE_REGISTERED

    # ========================================================
    #
    # RESET METRICS
    #
    # ========================================================

    def reset_metrics(self) -> None:

        with self.lock:

            self.executions = 0
            self.successes = 0
            self.failures = 0
            self.errors = 0

            self.total_duration = 0.0
            self.last_duration = 0.0

            self.min_duration = None
            self.max_duration = None

            self.last_execution = None
            self.last_success = None
            self.last_failure = None

            self.last_error = None
            self.last_result = None

    # ========================================================
    #
    # DICT
    #
    # ========================================================

    def to_dict(
        self,
        include_module: bool = False
    ) -> Dict[str, Any]:

        with self.lock:

            result = {

                "name":
                    self.name,

                "version":
                    self.version,

                "enabled":
                    self.enabled,

                "state":
                    self.state,

                "priority":
                    self.priority,

                "critical":
                    self.critical,

                "dependencies":
                    list(self.dependencies),

                "tags":
                    list(self.tags),

                "capabilities":
                    list(self.capabilities),

                "aliases":
                    list(self.aliases),

                "description":
                    self.description,

                "execution_interface":
                    self.execution_interface,

                "registered_at":
                    self.registered_at,

                "initialized_at":
                    self.initialized_at,

                "shutdown_at":
                    self.shutdown_at,

                "last_execution":
                    self.last_execution,

                "last_success":
                    self.last_success,

                "last_failure":
                    self.last_failure,

                "executions":
                    self.executions,

                "successes":
                    self.successes,

                "failures":
                    self.failures,

                "errors":
                    self.errors,

                "success_rate":
                    self.success_rate(),

                "total_duration":
                    self.total_duration,

                "last_duration":
                    self.last_duration,

                "average_duration":
                    self.average_duration(),

                "min_duration":
                    self.min_duration,

                "max_duration":
                    self.max_duration,

                "last_error":
                    self.last_error,

                "metadata":
                    dict(self.metadata),
            }

            if include_module:
                result["module"] = self.module

            return result


# ============================================================
#
# MODULE REGISTRY
#
# ============================================================

class ModuleRegistry:
    """
    Central registry for INKSIDE Intelligence OS modules.
    """

    # ========================================================
    #
    # INIT
    #
    # ========================================================

    def __init__(self):

        self.lock = threading.RLock()

        self._modules: Dict[
            str,
            ModuleDescriptor
        ] = {}

        self._aliases: Dict[
            str,
            str
        ] = {}

        self._started_at = utc_now()

        self._registrations = 0
        self._unregistrations = 0

        self._executions = 0
        self._successes = 0
        self._failures = 0
        self._errors = 0

        self._initialized = False

        logger.info(
            "Module Registry v%s initialized.",
            REGISTRY_VERSION
        )

    # ========================================================
    #
    # INTERNAL RESOLUTION
    #
    # ========================================================

    def _resolve_name(
        self,
        name: str
    ) -> Optional[str]:

        normalized = _normalize_name(
            name
        )

        if not normalized:
            return None

        if normalized in self._modules:
            return normalized

        return self._aliases.get(
            normalized
        )

    # ========================================================
    #
    # INTERNAL DEPENDENCY RESOLUTION
    #
    # ========================================================

    def _resolve_dependency(
        self,
        dependency: str
    ) -> Optional[str]:

        return self._resolve_name(
            dependency
        )

    # ========================================================
    #
    # DETECT INTERFACE
    #
    # ========================================================

    def _detect_interface(
        self,
        module: Any
    ) -> str:

        process = getattr(
            module,
            "process",
            None
        )

        if callable(process):
            return EXECUTION_PROCESS

        execute = getattr(
            module,
            "execute",
            None
        )

        if callable(execute):
            return EXECUTION_EXECUTE

        run = getattr(
            module,
            "run",
            None
        )

        if callable(run):
            return EXECUTION_RUN

        if callable(module):
            return EXECUTION_CALLABLE

        return "unsupported"

    # ========================================================
    #
    # REGISTER
    #
    # ========================================================

    def register(
        self,
        name: str,
        module: Any,
        version: str = "1.0",
        *,
        enabled: bool = True,
        priority: int = 50,
        critical: bool = False,
        dependencies: Optional[
            Iterable[str]
        ] = None,
        tags: Optional[
            Iterable[str]
        ] = None,
        capabilities: Optional[
            Iterable[str]
        ] = None,
        aliases: Optional[
            Iterable[str]
        ] = None,
        description: str = "",
        metadata: Optional[
            Dict[str, Any]
        ] = None,
        replace: bool = False,
    ) -> ModuleDescriptor:
        """
        Register an Intelligence OS module.
        """

        normalized_name = _normalize_name(
            name
        )

        if not normalized_name:
            raise ValueError(
                "Module name cannot be empty."
            )

        if module is None:
            raise ValueError(
                f"Module '{normalized_name}' "
                "cannot be None."
            )

        interface = (
            self._detect_interface(
                module
            )
        )

        if interface == "unsupported":
            raise TypeError(
                f"Module '{normalized_name}' "
                "has no supported execution "
                "interface."
            )

        normalized_dependencies = (
            _normalize_names(
                dependencies
            )
        )

        normalized_tags = (
            _normalize_names(
                tags
            )
        )

        normalized_capabilities = (
            _normalize_names(
                capabilities
            )
        )

        normalized_aliases = (
            _normalize_names(
                aliases
            )
        )

        if normalized_name in normalized_aliases:

            normalized_aliases = [
                alias
                for alias in normalized_aliases
                if alias != normalized_name
            ]

        with self.lock:

            existing_module = (
                self._modules.get(
                    normalized_name
                )
            )

            if (
                existing_module is not None
                and not replace
            ):
                raise ValueError(
                    "Module already registered: "
                    f"{normalized_name}"
                )

            # ------------------------------------------------
            # Validate aliases BEFORE changing registry state.
            # ------------------------------------------------

            for alias in normalized_aliases:

                if alias == normalized_name:
                    continue

                alias_owner = (
                    self._aliases.get(
                        alias
                    )
                )

                if (
                    alias_owner is not None
                    and alias_owner
                    != normalized_name
                ):
                    raise ValueError(
                        "Alias already used: "
                        f"{alias}"
                    )

                if (
                    alias in self._modules
                    and alias
                    != normalized_name
                ):
                    raise ValueError(
                        "Alias conflicts with "
                        f"module name: {alias}"
                    )

            # ------------------------------------------------
            # Module name cannot collide with another alias.
            # ------------------------------------------------

            alias_owner = (
                self._aliases.get(
                    normalized_name
                )
            )

            if (
                alias_owner is not None
                and alias_owner
                != normalized_name
            ):
                raise ValueError(
                    "Module name conflicts with "
                    f"alias: {normalized_name}"
                )

            # ------------------------------------------------
            # Validate dependency self-reference.
            # ------------------------------------------------

            for dependency in normalized_dependencies:

                if dependency == normalized_name:

                    raise ValueError(
                        "Module cannot depend on itself: "
                        f"{normalized_name}"
                    )

            # ------------------------------------------------
            # Remove old module aliases only after all
            # validation has succeeded.
            # ------------------------------------------------

            if existing_module is not None:

                for alias in existing_module.aliases:

                    if (
                        self._aliases.get(alias)
                        == normalized_name
                    ):
                        self._aliases.pop(
                            alias,
                            None
                        )

            descriptor = ModuleDescriptor(

                name=normalized_name,

                module=module,

                version=_safe_str(
                    version
                ),

                enabled=bool(
                    enabled
                ),

                state=(
                    MODULE_REGISTERED
                    if enabled
                    else MODULE_DISABLED
                ),

                priority=int(
                    priority
                ),

                critical=bool(
                    critical
                ),

                dependencies=(
                    normalized_dependencies
                ),

                tags=(
                    normalized_tags
                ),

                capabilities=(
                    normalized_capabilities
                ),

                aliases=(
                    normalized_aliases
                ),

                description=_safe_str(
                    description
                ),

                execution_interface=(
                    interface
                ),

                metadata=_safe_metadata(
                    metadata
                ),
            )

            self._modules[
                normalized_name
            ] = descriptor

            for alias in normalized_aliases:

                self._aliases[
                    alias
                ] = normalized_name

            self._registrations += 1

        logger.info(
            "Module registered: %s v%s | interface=%s",
            normalized_name,
            version,
            interface,
        )

        return descriptor

    # ========================================================
    #
    # UNREGISTER
    #
    # ========================================================

    def unregister(
        self,
        name: str,
        *,
        force: bool = False
    ) -> bool:

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:
                return False

            dependents = self.dependents(
                resolved
            )

            if dependents and not force:

                raise RuntimeError(
                    "Cannot unregister module "
                    f"'{resolved}'. Dependents: "
                    + ", ".join(
                        dependents
                    )
                )

            descriptor = self._modules.pop(
                resolved
            )

            for alias in descriptor.aliases:

                if (
                    self._aliases.get(alias)
                    == resolved
                ):
                    self._aliases.pop(
                        alias,
                        None
                    )

            self._unregistrations += 1

        logger.info(
            "Module unregistered: %s",
            resolved
        )

        return True

    # ========================================================
    #
    # GET - RETURNS ModuleDescriptor (CRITICAL FOR ENGINE)
    #
    # ========================================================

    def get(
        self,
        name: str,
        default: Any = None
    ) -> Any:
        """
        Get module descriptor by name.

        CRITICAL: Returns ModuleDescriptor, NOT the module directly.
        This is required for engine compatibility.

        Engine expects: registry.get("name") -> ModuleSpec/ModuleDescriptor
        Then: spec.module -> actual module
        """

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:
                return default

            descriptor = self._modules.get(
                resolved
            )

            if descriptor is None:
                return default

            return descriptor

    # ========================================================
    #
    # GET_MODULE - Returns module directly (convenience)
    #
    # ========================================================

    def get_module(
        self,
        name: str,
        default: Any = None
    ) -> Any:
        """
        Get actual module directly.

        This is a convenience method for when you only need
        the module, not the descriptor.
        """

        descriptor = self.get(
            name
        )

        if descriptor is None:
            return default

        return descriptor.module

    # ========================================================
    #
    # GET_INFO (COMPATIBILITY)
    #
    # ========================================================

    def get_info(
        self,
        name: str
    ) -> Optional[ModuleDescriptor]:
        """
        Get module descriptor by name.
        Alias for get() for engine compatibility.
        """

        return self.get(name)

    # ========================================================
    #
    # DESCRIPTOR
    #
    # ========================================================

    def descriptor(
        self,
        name: str
    ) -> Optional[ModuleDescriptor]:

        return self.get(name)

    # ========================================================
    #
    # EXISTS
    #
    # ========================================================

    def exists(
        self,
        name: str
    ) -> bool:

        with self.lock:

            return (
                self._resolve_name(
                    name
                )
                is not None
            )

    # ========================================================
    #
    # ENABLE
    #
    # ========================================================

    def enable(
        self,
        name: str
    ) -> bool:

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:
                return False

            descriptor = self._modules[
                resolved
            ]

            descriptor.mark_enabled()

        logger.info(
            "Module enabled: %s",
            resolved
        )

        return True

    # ========================================================
    #
    # DISABLE
    #
    # ========================================================

    def disable(
        self,
        name: str,
        *,
        force: bool = False
    ) -> bool:

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:
                return False

            dependents = self.dependents(
                resolved
            )

            active_dependents = [
                item
                for item in dependents
                if self._modules[item].enabled
            ]

            if (
                active_dependents
                and not force
            ):

                raise RuntimeError(
                    "Cannot disable module "
                    f"'{resolved}'. Active "
                    "dependents: "
                    + ", ".join(
                        active_dependents
                    )
                )

            descriptor = self._modules[
                resolved
            ]

            descriptor.mark_disabled()

        logger.info(
            "Module disabled: %s",
            resolved
        )

        return True

    # ========================================================
    #
    # ENABLED
    #
    # ========================================================

    def is_enabled(
        self,
        name: str
    ) -> bool:

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:
                return False

            descriptor = self._modules[
                resolved
            ]

            return bool(
                descriptor.enabled
            )

    # ========================================================
    #
    # ALL
    #
    # ========================================================

    def all(
        self
    ) -> List[ModuleDescriptor]:
        """
        Return all module descriptors (for engine compatibility).
        """

        with self.lock:
            return list(self._modules.values())

    # ========================================================
    #
    # LIST
    #
    # ========================================================

    def list(
        self,
        *,
        enabled_only: bool = False,
        state: Optional[str] = None,
        tag: Optional[str] = None,
        capability: Optional[str] = None,
    ) -> List[str]:

        with self.lock:

            descriptors = list(
                self._modules.values()
            )

            if enabled_only:

                descriptors = [
                    item
                    for item in descriptors
                    if item.enabled
                ]

            if state:

                descriptors = [
                    item
                    for item in descriptors
                    if item.state == state
                ]

            if tag:

                descriptors = [
                    item
                    for item in descriptors
                    if tag in item.tags
                ]

            if capability:

                descriptors = [
                    item
                    for item in descriptors
                    if capability
                    in item.capabilities
                ]

            descriptors.sort(
                key=lambda item: (
                    -item.priority,
                    item.name
                )
            )

            return [
                item.name
                for item in descriptors
            ]

    # ========================================================
    #
    # DESCRIPTORS
    #
    # ========================================================

    def descriptors(
        self,
        *,
        enabled_only: bool = False
    ) -> List[ModuleDescriptor]:

        with self.lock:

            result = list(
                self._modules.values()
            )

            if enabled_only:

                result = [
                    item
                    for item in result
                    if item.enabled
                ]

            result.sort(
                key=lambda item: (
                    -item.priority,
                    item.name
                )
            )

            return result

    # ========================================================
    #
    # FIND BY TAG
    #
    # ========================================================

    def find_by_tag(
        self,
        tag: str,
        *,
        enabled_only: bool = False
    ) -> List[Any]:

        names = self.list(
            enabled_only=enabled_only,
            tag=tag
        )

        with self.lock:

            return [
                self._modules[name].module
                for name in names
                if name in self._modules
            ]

    # ========================================================
    #
    # FIND BY CAPABILITY
    #
    # ========================================================

    def find_by_capability(
        self,
        capability: str,
        *,
        enabled_only: bool = False
    ) -> List[Any]:

        names = self.list(
            enabled_only=enabled_only,
            capability=capability
        )

        with self.lock:

            return [
                self._modules[name].module
                for name in names
                if name in self._modules
            ]

    # ========================================================
    #
    # DEPENDENTS
    #
    # ========================================================

    def dependents(
        self,
        module_name: str
    ) -> List[str]:

        with self.lock:

            resolved = self._resolve_name(
                module_name
            )

            if resolved is None:
                return []

            result: List[str] = []

            for descriptor in (
                self._modules.values()
            ):

                for dependency in (
                    descriptor.dependencies
                ):

                    dependency_resolved = (
                        self._resolve_dependency(
                            dependency
                        )
                    )

                    if (
                        dependency_resolved
                        == resolved
                    ):

                        result.append(
                            descriptor.name
                        )

                        break

            result.sort()

            return result

    # ========================================================
    #
    # CHECK DEPENDENCIES
    #
    # ========================================================

    def check_dependencies(
        self,
        name: str,
        *,
        require_online: bool = False
    ) -> Dict[str, Any]:

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:

                return {
                    "module": name,
                    "exists": False,
                    "ready": False,
                    "missing": [],
                    "disabled": [],
                    "offline": [],
                    "errors": [],
                }

            descriptor = self._modules[
                resolved
            ]

            missing: List[str] = []
            disabled: List[str] = []
            offline: List[str] = []
            errors: List[str] = []

            resolved_dependencies: List[str] = []

            for dependency in (
                descriptor.dependencies
            ):

                dependency_name = (
                    self._resolve_dependency(
                        dependency
                    )
                )

                if dependency_name is None:

                    missing.append(
                        dependency
                    )

                    continue

                resolved_dependencies.append(
                    dependency_name
                )

                dependency_descriptor = (
                    self._modules[
                        dependency_name
                    ]
                )

                if not (
                    dependency_descriptor.enabled
                ):

                    disabled.append(
                        dependency_name
                    )

                if (
                    dependency_descriptor.state
                    == MODULE_ERROR
                ):

                    errors.append(
                        dependency_name
                    )

                if (
                    require_online
                    and dependency_descriptor.state
                    != MODULE_ONLINE
                ):

                    offline.append(
                        dependency_name
                    )

            ready = (
                len(missing) == 0
                and len(disabled) == 0
                and len(errors) == 0
                and len(offline) == 0
            )

            return {

                "module":
                    resolved,

                "exists":
                    True,

                "ready":
                    ready,

                "missing":
                    missing,

                "disabled":
                    disabled,

                "offline":
                    offline,

                "errors":
                    errors,

                "dependencies":
                    list(
                        descriptor.dependencies
                    ),

                "resolved_dependencies":
                    resolved_dependencies,

            }

    # ========================================================
    #
    # VALIDATE
    #
    # ========================================================

    def validate(
        self,
        name: str,
        *,
        require_online: bool = False
    ) -> bool:

        result = self.check_dependencies(
            name,
            require_online=require_online
        )

        return bool(
            result.get("ready")
        )

    # ========================================================
    #
    # DEPENDENCY GRAPH
    #
    # ========================================================

    def dependency_graph(
        self
    ) -> Dict[str, List[str]]:

        with self.lock:

            graph: Dict[
                str,
                List[str]
            ] = {}

            for descriptor in (
                self._modules.values()
            ):

                resolved_dependencies = []

                for dependency in (
                    descriptor.dependencies
                ):

                    resolved = (
                        self._resolve_dependency(
                            dependency
                        )
                    )

                    if resolved is not None:

                        resolved_dependencies.append(
                            resolved
                        )

                graph[
                    descriptor.name
                ] = resolved_dependencies

            return graph

    # ========================================================
    #
    # CIRCULAR DEPENDENCY DETECTION
    #
    # ========================================================

    def find_cycles(
        self
    ) -> List[List[str]]:

        with self.lock:

            graph = (
                self.dependency_graph()
            )

            cycles: List[List[str]] = []

            visiting: Set[str] = set()
            visited: Set[str] = set()

            def visit(
                node: str,
                path: List[str]
            ) -> None:

                if node in visiting:

                    try:

                        index = path.index(
                            node
                        )

                        cycle = (
                            path[index:]
                            + [node]
                        )

                        if cycle not in cycles:
                            cycles.append(
                                cycle
                            )

                    except ValueError:
                        pass

                    return

                if node in visited:
                    return

                visiting.add(node)

                for dependency in (
                    graph.get(
                        node,
                        []
                    )
                ):

                    visit(
                        dependency,
                        path + [dependency]
                    )

                visiting.discard(node)
                visited.add(node)

            for node in sorted(graph):

                visit(
                    node,
                    [node]
                )

            return cycles

    # ========================================================
    #
    # EXECUTION ORDER
    #
    # ========================================================

    def execution_order(
        self,
        names: Optional[
            Iterable[str]
        ] = None
    ) -> List[str]:
        """
        Return deterministic dependency-safe order.

        Dependencies are always placed before dependents.
        """

        with self.lock:

            if names is None:

                selected: Set[str] = set(
                    self._modules.keys()
                )

            else:

                selected = set()

                for name in names:

                    resolved = (
                        self._resolve_name(
                            name
                        )
                    )

                    if resolved is not None:
                        selected.add(
                            resolved
                        )

            graph = (
                self.dependency_graph()
            )

            # ------------------------------------------------
            # Recursively include known dependencies.
            # ------------------------------------------------

            changed = True

            while changed:

                changed = False

                for node in list(
                    selected
                ):

                    for dependency in (
                        graph.get(
                            node,
                            []
                        )
                    ):

                        if dependency not in selected:

                            selected.add(
                                dependency
                            )

                            changed = True

            cycles = self.find_cycles()

            if cycles:

                raise RuntimeError(
                    "Circular module dependencies "
                    "detected: "
                    + repr(cycles)
                )

            result: List[str] = []

            temporary: Set[str] = set()
            permanent: Set[str] = set()

            def sort_key(
                module_name: str
            ):
                descriptor = self._modules[
                    module_name
                ]

                return (
                    -descriptor.priority,
                    descriptor.name
                )

            def visit(
                node: str
            ) -> None:

                if node in permanent:
                    return

                if node in temporary:

                    raise RuntimeError(
                        "Circular dependency detected "
                        f"at module: {node}"
                    )

                temporary.add(node)

                dependencies = sorted(
                    graph.get(
                        node,
                        []
                    ),
                    key=sort_key
                )

                for dependency in dependencies:

                    if dependency in selected:

                        visit(
                            dependency
                        )

                temporary.remove(node)

                permanent.add(node)

                result.append(node)

            for node in sorted(
                selected,
                key=sort_key
            ):

                visit(node)

            return result

    # ========================================================
    #
    # INITIALIZE ONE
    #
    # ========================================================

    def initialize(
        self,
        name: str,
        *,
        require_dependencies: bool = True
    ) -> bool:

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:
                return False

            descriptor = self._modules[
                resolved
            ]

            if not descriptor.enabled:
                return False

            if (
                descriptor.state
                == MODULE_ONLINE
            ):
                return True

            if require_dependencies:

                dependency_check = (
                    self.check_dependencies(
                        resolved,
                        require_online=True
                    )
                )

                if not dependency_check[
                    "ready"
                ]:

                    logger.warning(
                        "Module '%s' cannot "
                        "initialize. Dependencies "
                        "not ready: %s",
                        resolved,
                        dependency_check
                    )

                    return False

            module = descriptor.module

            descriptor.state = (
                MODULE_INITIALIZING
            )

        try:

            initializer = getattr(
                module,
                "initialize",
                None
            )

            if callable(initializer):

                result = initializer()

                if result is False:

                    raise RuntimeError(
                        "Module initialization "
                        "returned False."
                    )

            with self.lock:

                descriptor.initialized_at = (
                    utc_now()
                )

                descriptor.shutdown_at = None

                descriptor.mark_online()

            logger.info(
                "Module initialized: %s",
                resolved
            )

            return True

        except Exception as exc:

            with self.lock:

                descriptor.mark_error(
                    exc
                )

                self._errors += 1

            logger.exception(
                "Module initialization failed: %s",
                resolved
            )

            return False

    # ========================================================
    #
    # INITIALIZE ALL
    #
    # ========================================================

    def initialize_all(
        self,
        *,
        enabled_only: bool = True
    ) -> Dict[str, bool]:

        names = self.execution_order()

        result: Dict[str, bool] = {}

        for name in names:

            descriptor = self.descriptor(
                name
            )

            if descriptor is None:
                continue

            if (
                enabled_only
                and not descriptor.enabled
            ):
                continue

            # ------------------------------------------------
            # Dependencies must be ONLINE before initialization.
            # ------------------------------------------------

            dependency_check = (
                self.check_dependencies(
                    name,
                    require_online=True
                )
            )

            if not dependency_check[
                "ready"
            ]:

                result[name] = False

                logger.warning(
                    "Skipping initialization of "
                    "%s because dependencies "
                    "are not ready.",
                    name
                )

                continue

            result[name] = (
                self.initialize(
                    name,
                    require_dependencies=True
                )
            )

        self._initialized = (
            bool(result)
            and all(
                result.values()
            )
        )

        if not result:
            self._initialized = True

        return result

    # ========================================================
    #
    # SHUTDOWN ONE
    #
    # ========================================================

    def shutdown(
        self,
        name: str
    ) -> bool:

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:
                return False

            descriptor = self._modules[
                resolved
            ]

            if descriptor.state in {
                MODULE_REGISTERED,
                MODULE_DISABLED,
                MODULE_OFFLINE,
            }:

                return True

            module = descriptor.module

            descriptor.state = (
                MODULE_SHUTTING_DOWN
            )

        try:

            shutdowner = getattr(
                module,
                "shutdown",
                None
            )

            if callable(shutdowner):

                result = shutdowner()

                if result is False:

                    raise RuntimeError(
                        "Module shutdown "
                        "returned False."
                    )

            with self.lock:

                descriptor.shutdown_at = (
                    utc_now()
                )

                descriptor.mark_offline()

            logger.info(
                "Module shutdown: %s",
                resolved
            )

            return True

        except Exception as exc:

            with self.lock:

                descriptor.mark_error(
                    exc
                )

                self._errors += 1

            logger.exception(
                "Module shutdown failed: %s",
                resolved
            )

            return False

    # ========================================================
    #
    # SHUTDOWN ALL
    #
    # ========================================================

    def shutdown_all(
        self
    ) -> Dict[str, bool]:

        names = self.execution_order()

        names.reverse()

        result: Dict[str, bool] = {}

        for name in names:

            result[name] = (
                self.shutdown(name)
            )

        with self.lock:

            self._initialized = False

        return result

    # ========================================================
    #
    # EXECUTE ONE
    #
    # ========================================================

    def execute(
        self,
        name: str,
        *args,
        require_dependencies: bool = True,
        require_online: bool = False,
        **kwargs
    ) -> Any:
        """
        Execute one registered module safely.

        Registry lock is released before module execution.
        """

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:

                raise KeyError(
                    f"Module not registered: {name}"
                )

            descriptor = self._modules[
                resolved
            ]

            if not descriptor.enabled:

                raise RuntimeError(
                    f"Module disabled: {resolved}"
                )

            if require_dependencies:

                dependency_check = (
                    self.check_dependencies(
                        resolved,
                        require_online=True
                    )
                )

                if not dependency_check[
                    "ready"
                ]:

                    dependency_names = (
                        dependency_check[
                            "missing"
                        ]
                        + dependency_check[
                            "disabled"
                        ]
                        + dependency_check[
                            "offline"
                        ]
                        + dependency_check[
                            "errors"
                        ]
                    )

                    raise RuntimeError(
                        "Module dependencies "
                        "not ready: "
                        + ", ".join(
                            dependency_names
                        )
                    )

            if (
                require_online
                and descriptor.state
                != MODULE_ONLINE
            ):

                raise RuntimeError(
                    f"Module is not online: "
                    f"{resolved}"
                )

            module = descriptor.module

            interface = (
                descriptor.execution_interface
            )

        start = time.perf_counter()

        try:

            if interface == EXECUTION_PROCESS:

                result = module.process(
                    *args,
                    **kwargs
                )

            elif interface == EXECUTION_EXECUTE:

                result = module.execute(
                    *args,
                    **kwargs
                )

            elif interface == EXECUTION_RUN:

                result = module.run(
                    *args,
                    **kwargs
                )

            elif interface == EXECUTION_CALLABLE:

                result = module(
                    *args,
                    **kwargs
                )

            else:

                raise TypeError(
                    "Unsupported module interface: "
                    f"{interface}"
                )

            duration = (
                time.perf_counter()
                - start
            )

            with self.lock:

                descriptor.mark_execution(
                    duration
                )

                descriptor.mark_success(
                    result
                )

                self._executions += 1
                self._successes += 1

            return result

        except Exception as exc:

            duration = (
                time.perf_counter()
                - start
            )

            with self.lock:

                descriptor.mark_execution(
                    duration
                )

                descriptor.mark_error(
                    exc
                )

                self._executions += 1
                self._failures += 1
                self._errors += 1

            logger.error(
                "Module execution failed: "
                "%s | %s",
                resolved,
                exc
            )

            logger.debug(
                traceback.format_exc()
            )

            # ------------------------------------------------
            # Optional error hook.
            # ------------------------------------------------

            try:

                on_error = getattr(
                    module,
                    "on_error",
                    None
                )

                if callable(on_error):

                    on_error(exc)

            except Exception:

                logger.debug(
                    "Module on_error hook failed.",
                    exc_info=True
                )

            raise

    # ========================================================
    #
    # SAFE EXECUTE
    #
    # ========================================================

    def safe_execute(
        self,
        name: str,
        *args,
        default: Any = None,
        **kwargs
    ) -> Any:

        try:

            return self.execute(
                name,
                *args,
                **kwargs
            )

        except Exception as exc:

            logger.error(
                "Safe module execution failed: "
                "%s | %s",
                name,
                exc
            )

            return default

    # ========================================================
    #
    # EXECUTE ALL
    #
    # ========================================================

    def execute_all(
        self,
        data: Any = None,
        *,
        names: Optional[
            Iterable[str]
        ] = None,
        stop_on_error: bool = False,
        include_disabled: bool = False,
        safe: bool = True,
    ) -> Dict[str, Any]:
        """
        Execute multiple modules in dependency order.
        """

        order = self.execution_order(
            names
        )

        results: Dict[
            str,
            Any
        ] = {}

        for name in order:

            descriptor = self.descriptor(
                name
            )

            if descriptor is None:
                continue

            if (
                not include_disabled
                and not descriptor.enabled
            ):
                continue

            try:

                results[name] = (
                    self.execute(
                        name,
                        data
                    )
                )

            except Exception as exc:

                if not safe:
                    raise

                results[name] = {

                    "error":
                        _safe_str(exc),

                    "module":
                        name,

                    "state":
                        MODULE_ERROR,
                }

                if stop_on_error:
                    break

        return results

    # ========================================================
    #
    # HEALTH ONE
    #
    # ========================================================

    def health(
        self,
        name: str
    ) -> Dict[str, Any]:

        descriptor = self.descriptor(
            name
        )

        if descriptor is None:

            return {

                "module":
                    name,

                "exists":
                    False,

                "healthy":
                    False,
            }

        result = descriptor.to_dict()

        module = descriptor.module

        try:

            health_method = getattr(
                module,
                "health",
                None
            )

            if callable(health_method):

                result[
                    "module_health"
                ] = health_method()

        except Exception as exc:

            result[
                "module_health_error"
            ] = _safe_str(exc)

        result["healthy"] = (
            descriptor.enabled
            and descriptor.state
            == MODULE_ONLINE
        )

        return result

    # ========================================================
    #
    # HEALTH ALL
    #
    # ========================================================

    def health_all(
        self
    ) -> Dict[
        str,
        Dict[str, Any]
    ]:

        with self.lock:

            names = sorted(
                self._modules.keys()
            )

        return {
            name:
                self.health(name)
            for name in names
        }

    # ========================================================
    #
    # RESET ONE
    #
    # ========================================================

    def reset_module(
        self,
        name: str,
        *,
        reset_internal: bool = True
    ) -> bool:

        with self.lock:

            resolved = self._resolve_name(
                name
            )

            if resolved is None:
                return False

            descriptor = self._modules[
                resolved
            ]

            module = descriptor.module

        try:

            if reset_internal:

                resetter = getattr(
                    module,
                    "reset",
                    None
                )

                if callable(resetter):

                    result = resetter()

                    if result is False:
                        return False

            with self.lock:

                descriptor.reset_metrics()

                descriptor.state = (
                    MODULE_REGISTERED
                    if descriptor.enabled
                    else MODULE_DISABLED
                )

            logger.info(
                "Module reset: %s",
                resolved
            )

            return True

        except Exception as exc:

            with self.lock:

                descriptor.mark_error(
                    exc
                )

                self._errors += 1

            logger.exception(
                "Module reset failed: %s",
                resolved
            )

            return False

    # ========================================================
    #
    # RESET REGISTRY
    #
    # ========================================================

    def reset(
        self,
        clear_modules: bool = False
    ) -> bool:

        if clear_modules:

            with self.lock:

                self._modules.clear()
                self._aliases.clear()

                self._registrations = 0
                self._unregistrations = 0

                self._executions = 0
                self._successes = 0
                self._failures = 0
                self._errors = 0

                self._initialized = False

            logger.info(
                "Module Registry completely cleared."
            )

            return True

        with self.lock:

            names = list(
                self._modules.keys()
            )

            self._executions = 0
            self._successes = 0
            self._failures = 0
            self._errors = 0

        result = True

        for name in names:

            if not self.reset_module(
                name
            ):
                result = False

        logger.info(
            "Module Registry reset."
        )

        return result

    # ========================================================
    #
    # SNAPSHOT
    #
    # ========================================================

    def snapshot(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            modules = {
                name:
                    descriptor.to_dict()
                for name, descriptor
                in self._modules.items()
            }

            aliases = dict(
                self._aliases
            )

            registry_metrics = (
                self.metrics()
            )

            return {

                "registry":
                    REGISTRY_NAME,

                "version":
                    REGISTRY_VERSION,

                "api_version":
                    API_VERSION,

                "started_at":
                    self._started_at,

                "initialized":
                    self._initialized,

                "modules":
                    modules,

                "aliases":
                    aliases,

                "metrics":
                    registry_metrics,
            }

    # ========================================================
    #
    # METRICS
    #
    # ========================================================

    def metrics(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            total_duration = sum(
                descriptor.total_duration
                for descriptor
                in self._modules.values()
            )

            average_duration = 0.0

            if self._executions > 0:

                average_duration = (
                    total_duration
                    / self._executions
                )

            success_rate = 0.0

            if self._executions > 0:

                success_rate = (
                    self._successes
                    / self._executions
                ) * 100.0

            return {

                "registrations":
                    self._registrations,

                "unregistrations":
                    self._unregistrations,

                "executions":
                    self._executions,

                "successes":
                    self._successes,

                "failures":
                    self._failures,

                "errors":
                    self._errors,

                "success_rate":
                    success_rate,

                "average_duration":
                    average_duration,
            }

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            descriptors = list(
                self._modules.values()
            )

            online = [
                item.name
                for item in descriptors
                if item.state
                == MODULE_ONLINE
            ]

            offline = [
                item.name
                for item in descriptors
                if item.state
                == MODULE_OFFLINE
            ]

            disabled = [
                item.name
                for item in descriptors
                if not item.enabled
            ]

            errors = [
                item.name
                for item in descriptors
                if item.state
                == MODULE_ERROR
            ]

            critical_errors = [
                item.name
                for item in descriptors
                if (
                    item.critical
                    and item.state
                    == MODULE_ERROR
                )
            ]

            dependency_cycles = (
                self.find_cycles()
            )

            return {

                "registry":
                    REGISTRY_NAME,

                "online":
                    True,

                "version":
                    REGISTRY_VERSION,

                "api_version":
                    API_VERSION,

                "module_count":
                    len(descriptors),

                "modules":
                    sorted(
                        item.name
                        for item in descriptors
                    ),

                "modules_online":
                    sorted(
                        online
                    ),

                "modules_offline":
                    sorted(
                        offline
                    ),

                "modules_disabled":
                    sorted(
                        disabled
                    ),

                "modules_error":
                    sorted(
                        errors
                    ),

                "critical_errors":
                    sorted(
                        critical_errors
                    ),

                "dependency_cycles":
                    dependency_cycles,

                "aliases":
                    dict(
                        self._aliases
                    ),

                "registrations":
                    self._registrations,

                "unregistrations":
                    self._unregistrations,

                "errors":
                    self._errors,

                "executions":
                    self._executions,

                "successes":
                    self._successes,

                "failures":
                    self._failures,

                "initialized":
                    self._initialized,

                "started_at":
                    self._started_at,
            }

    # ========================================================
    #
    # FIND
    #
    # ========================================================

    def find(
        self,
        *,
        tag: Optional[str] = None,
        capability: Optional[str] = None,
        enabled_only: bool = False,
        critical_only: bool = False,
    ) -> List[ModuleDescriptor]:

        with self.lock:

            result = list(
                self._modules.values()
            )

            if tag:

                result = [
                    item
                    for item in result
                    if tag in item.tags
                ]

            if capability:

                result = [
                    item
                    for item in result
                    if capability
                    in item.capabilities
                ]

            if enabled_only:

                result = [
                    item
                    for item in result
                    if item.enabled
                ]

            if critical_only:

                result = [
                    item
                    for item in result
                    if item.critical
                ]

            result.sort(
                key=lambda item: (
                    -item.priority,
                    item.name
                )
            )

            return result

    # ========================================================
    #
    # DEPENDENCIES_AVAILABLE (ENGINE COMPATIBILITY)
    #
    # ========================================================

    def dependencies_available(
        self,
        name: str
    ) -> bool:
        """
        Check if all dependencies are available.
        For engine compatibility.
        """

        result = self.check_dependencies(
            name,
            require_online=False
        )

        return bool(
            result.get("ready", False)
        )

    # ========================================================
    #
    # MODULE_INFO (ENGINE COMPATIBILITY)
    #
    # ========================================================

    def module_info(
        self,
        name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get module info as dict.
        For engine compatibility.
        """

        descriptor = self.descriptor(
            name
        )

        if descriptor is None:
            return None

        return descriptor.to_dict(
            include_module=True
        )


# ============================================================
#
# GLOBAL REGISTRY
#
# ============================================================

module_registry = ModuleRegistry()


# ============================================================
#
# COMPATIBILITY API
#
# ============================================================

def register(
    name: str,
    module: Any,
    version: str = "1.0",
    **kwargs
) -> ModuleDescriptor:

    return module_registry.register(
        name,
        module,
        version,
        **kwargs
    )


def unregister(
    name: str,
    **kwargs
) -> bool:

    return module_registry.unregister(
        name,
        **kwargs
    )


def get(
    name: str,
    default: Any = None
) -> Any:
    """
    Get module descriptor (compatibility wrapper).
    
    Returns ModuleDescriptor, NOT the module directly.
    """

    return module_registry.get(
        name,
        default
    )


def get_module(
    name: str,
    default: Any = None
) -> Any:
    """
    Get actual module directly.
    """

    return module_registry.get_module(
        name,
        default
    )


def exists(
    name: str
) -> bool:

    return module_registry.exists(
        name
    )


def enable(
    name: str
) -> bool:

    return module_registry.enable(
        name
    )


def disable(
    name: str,
    **kwargs
) -> bool:

    return module_registry.disable(
        name,
        **kwargs
    )


def execute(
    name: str,
    *args,
    **kwargs
) -> Any:

    return module_registry.execute(
        name,
        *args,
        **kwargs
    )


def safe_execute(
    name: str,
    *args,
    **kwargs
) -> Any:

    return module_registry.safe_execute(
        name,
        *args,
        **kwargs
    )


def status() -> Dict[str, Any]:

    return module_registry.status()


def metrics() -> Dict[str, Any]:

    return module_registry.metrics()


def snapshot() -> Dict[str, Any]:

    return module_registry.snapshot()


def health(
    name: str
) -> Dict[str, Any]:

    return module_registry.health(
        name
    )


def health_all() -> Dict[
    str,
    Dict[str, Any]
]:

    return module_registry.health_all()


def initialize(
    name: str,
    **kwargs
) -> bool:

    return module_registry.initialize(
        name,
        **kwargs
    )


def initialize_all() -> Dict[str, bool]:

    return module_registry.initialize_all()


def shutdown(
    name: str
) -> bool:

    return module_registry.shutdown(
        name
    )


def shutdown_all() -> Dict[str, bool]:

    return module_registry.shutdown_all()


# ============================================================
#
# PUBLIC API
#
# ============================================================

__all__ = [

    # --------------------------------------------------------
    # Versions
    # --------------------------------------------------------

    "REGISTRY_VERSION",
    "API_VERSION",
    "REGISTRY_NAME",

    # --------------------------------------------------------
    # States
    # --------------------------------------------------------

    "MODULE_REGISTERED",
    "MODULE_INITIALIZING",
    "MODULE_ONLINE",
    "MODULE_OFFLINE",
    "MODULE_DISABLED",
    "MODULE_ERROR",
    "MODULE_SHUTTING_DOWN",
    "MODULE_UNKNOWN",
    "VALID_MODULE_STATES",

    # --------------------------------------------------------
    # Interfaces
    # --------------------------------------------------------

    "EXECUTION_PROCESS",
    "EXECUTION_EXECUTE",
    "EXECUTION_RUN",
    "EXECUTION_CALLABLE",
    "VALID_EXECUTION_INTERFACES",

    # --------------------------------------------------------
    # Classes
    # --------------------------------------------------------

    "ModuleDescriptor",
    "ModuleRegistry",

    # --------------------------------------------------------
    # Global registry
    # --------------------------------------------------------

    "module_registry",

    # --------------------------------------------------------
    # Compatibility API
    # --------------------------------------------------------

    "register",
    "unregister",
    "get",
    "get_module",
    "exists",
    "enable",
    "disable",
    "execute",
    "safe_execute",

    # --------------------------------------------------------
    # Lifecycle
    # --------------------------------------------------------

    "initialize",
    "initialize_all",
    "shutdown",
    "shutdown_all",

    # --------------------------------------------------------
    # Monitoring
    # --------------------------------------------------------

    "health",
    "health_all",
    "metrics",
    "status",
    "snapshot",
]