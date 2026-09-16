# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# DEPENDENCY MANAGER
# FOUNDATION v3.0
#
# Compatible Engine API: v1.0
#
# ============================================================

from __future__ import annotations

import logging
import threading

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

DEPENDENCY_VERSION = "3.0"
API_VERSION = "1.0"


# ============================================================
#
# ERRORS
#
# ============================================================

class DependencyError(Exception):
    """Base dependency manager error."""


class DependencyCycleError(DependencyError):
    """Raised when a dependency cycle is detected."""


class DependencyNotFoundError(DependencyError):
    """Raised when a required dependency is missing."""


# ============================================================
#
# DEPENDENCY SPECIFICATION
#
# ============================================================

@dataclass
class DependencySpec:

    name: str

    version: str = "1.0"

    required: List[str] = field(
        default_factory=list
    )

    optional: List[str] = field(
        default_factory=list
    )

    description: str = ""

    enabled: bool = True

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# ============================================================
#
# DEPENDENCY MANAGER
#
# ============================================================

class DependencyManager:
    """
    Central dependency graph manager.

    Responsibilities:

    - Register modules
    - Track required dependencies
    - Track optional dependencies
    - Detect missing dependencies
    - Detect dependency cycles
    - Resolve loading order
    - Validate graph
    - Enable / disable modules
    - Runtime inspection

    Engine does NOT need to know the internal dependency graph.
    """

    def __init__(self):

        self.lock = threading.RLock()

        self.dependencies: Dict[
            str,
            DependencySpec
        ] = {}

        self.registration_order: List[str] = []

        self.started_at = (
            self._utc_now()
        )

        self.register_count = 0

        self.error_count = 0

        logger.info(
            "Dependency Manager v%s initialized.",
            DEPENDENCY_VERSION
        )


    # ========================================================
    #
    # TIME
    #
    # ========================================================

    @staticmethod
    def _utc_now() -> str:

        from datetime import datetime

        return (
            datetime.utcnow()
            .isoformat()
            + "Z"
        )


    # ========================================================
    #
    # REGISTER
    #
    # ========================================================

    def register(
        self,
        name: str,
        *,
        version: str = "1.0",
        required: Optional[List[str]] = None,
        optional: Optional[List[str]] = None,
        description: str = "",
        enabled: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DependencySpec:

        if not name:

            raise DependencyError(
                "Module name cannot be empty."
            )

        required = list(
            required or []
        )

        optional = list(
            optional or []
        )

        if name in required:

            raise DependencyError(
                f"Module cannot depend on itself: {name}"
            )

        if name in optional:

            raise DependencyError(
                f"Module cannot optionally depend on itself: {name}"
            )

        with self.lock:

            if name in self.dependencies:

                spec = self.dependencies[name]

                spec.version = version

                spec.required = required

                spec.optional = optional

                spec.description = description

                spec.enabled = enabled

                if metadata is not None:

                    spec.metadata = dict(
                        metadata
                    )

                return spec

            spec = DependencySpec(

                name=name,

                version=version,

                required=required,

                optional=optional,

                description=description,

                enabled=enabled,

                metadata=dict(
                    metadata or {}
                )

            )

            self.dependencies[name] = spec

            self.registration_order.append(
                name
            )

            self.register_count += 1

        return spec


    # ========================================================
    #
    # UNREGISTER
    #
    # ========================================================

    def unregister(
        self,
        name: str
    ) -> bool:

        with self.lock:

            if name not in self.dependencies:

                return False

            del self.dependencies[name]

            self.registration_order = [
                item
                for item
                in self.registration_order
                if item != name
            ]

        return True


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

            return name in self.dependencies


    # ========================================================
    #
    # GET
    #
    # ========================================================

    def get(
        self,
        name: str
    ) -> Optional[DependencySpec]:

        with self.lock:

            return self.dependencies.get(
                name
            )


    # ========================================================
    #
    # ENABLE / DISABLE
    #
    # ========================================================

    def enable(
        self,
        name: str
    ) -> bool:

        with self.lock:

            spec = self.dependencies.get(
                name
            )

            if spec is None:

                return False

            spec.enabled = True

            return True


    def disable(
        self,
        name: str
    ) -> bool:

        with self.lock:

            spec = self.dependencies.get(
                name
            )

            if spec is None:

                return False

            spec.enabled = False

            return True


    # ========================================================
    #
    # REQUIRED DEPENDENCIES
    #
    # ========================================================

    def required_dependencies(
        self,
        name: str
    ) -> List[str]:

        with self.lock:

            spec = self.dependencies.get(
                name
            )

            if spec is None:

                return []

            return list(
                spec.required
            )


    # ========================================================
    #
    # OPTIONAL DEPENDENCIES
    #
    # ========================================================

    def optional_dependencies(
        self,
        name: str
    ) -> List[str]:

        with self.lock:

            spec = self.dependencies.get(
                name
            )

            if spec is None:

                return []

            return list(
                spec.optional
            )


    # ========================================================
    #
    # MISSING DEPENDENCIES
    #
    # ========================================================

    def missing(
        self,
        name: str
    ) -> List[str]:

        with self.lock:

            spec = self.dependencies.get(
                name
            )

            if spec is None:

                return []

            return [
                dependency

                for dependency
                in spec.required

                if (
                    dependency
                    not in self.dependencies
                )
            ]


    # ========================================================
    #
    # OPTIONAL MISSING
    #
    # ========================================================

    def missing_optional(
        self,
        name: str
    ) -> List[str]:

        with self.lock:

            spec = self.dependencies.get(
                name
            )

            if spec is None:

                return []

            return [
                dependency

                for dependency
                in spec.optional

                if (
                    dependency
                    not in self.dependencies
                )
            ]


    # ========================================================
    #
    # VALIDATE
    #
    # ========================================================

    def validate(
        self
    ) -> Dict[str, Any]:

        errors = []

        warnings = []

        with self.lock:

            names = set(
                self.dependencies.keys()
            )

            for name, spec in (
                self.dependencies.items()
            ):

                for dependency in (
                    spec.required
                ):

                    if dependency not in names:

                        errors.append(
                            {
                                "module": name,
                                "dependency": dependency,
                                "type": "required"
                            }
                        )

                for dependency in (
                    spec.optional
                ):

                    if dependency not in names:

                        warnings.append(
                            {
                                "module": name,
                                "dependency": dependency,
                                "type": "optional"
                            }
                        )

            try:

                self._resolve_order()

            except DependencyCycleError as exc:

                errors.append(
                    {
                        "type": "cycle",
                        "message": str(exc)
                    }
                )

        return {

            "valid":
                len(errors) == 0,

            "errors":
                errors,

            "warnings":
                warnings
        }


    # ========================================================
    #
    # RESOLVE LOAD ORDER
    #
    # ========================================================

    def resolve_order(
        self
    ) -> List[str]:

        with self.lock:

            return self._resolve_order()


    def _resolve_order(
        self
    ) -> List[str]:

        names = list(
            self.registration_order
        )

        state: Dict[
            str,
            int
        ] = {}

        result: List[str] = []

        visiting: List[str] = []

        def visit(
            name: str
        ):

            if name not in self.dependencies:

                raise DependencyNotFoundError(
                    f"Dependency not registered: {name}"
                )

            current_state = state.get(
                name,
                0
            )

            if current_state == 2:

                return

            if current_state == 1:

                cycle_start = (
                    visiting.index(name)
                    if name in visiting
                    else 0
                )

                cycle = (
                    visiting[cycle_start:]
                    + [name]
                )

                raise DependencyCycleError(
                    "Dependency cycle detected: "
                    + " -> ".join(cycle)
                )

            state[name] = 1

            visiting.append(
                name
            )

            spec = self.dependencies[
                name
            ]

            for dependency in (
                spec.required
            ):

                visit(
                    dependency
                )

            visiting.pop()

            state[name] = 2

            if name not in result:

                result.append(
                    name
                )

        for name in names:

            visit(
                name
            )

        return result


    # ========================================================
    #
    # ENABLED LOAD ORDER
    #
    # ========================================================

    def enabled_order(
        self
    ) -> List[str]:

        with self.lock:

            order = self._resolve_order()

            return [
                name
                for name in order
                if self.dependencies[
                    name
                ].enabled
            ]


    # ========================================================
    #
    # DEPENDENTS
    #
    # ========================================================

    def dependents(
        self,
        name: str
    ) -> List[str]:

        result = []

        with self.lock:

            for module, spec in (
                self.dependencies.items()
            ):

                if name in spec.required:

                    result.append(
                        module
                    )

        return result


    # ========================================================
    #
    # GRAPH
    #
    # ========================================================

    def graph(
        self
    ) -> Dict[str, Dict[str, List[str]]]:

        with self.lock:

            return {

                name: {

                    "required":
                        list(spec.required),

                    "optional":
                        list(spec.optional)

                }

                for name, spec
                in self.dependencies.items()
            }


    # ========================================================
    #
    # EXPORT
    #
    # ========================================================

    def snapshot(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            return {

                "version":
                    DEPENDENCY_VERSION,

                "api_version":
                    API_VERSION,

                "modules": {

                    name: {

                        "version":
                            spec.version,

                        "required":
                            list(spec.required),

                        "optional":
                            list(spec.optional),

                        "description":
                            spec.description,

                        "enabled":
                            spec.enabled,

                        "metadata":
                            dict(spec.metadata)

                    }

                    for name, spec
                    in self.dependencies.items()
                },

                "registration_order":
                    list(
                        self.registration_order
                    ),

                "resolved_order":
                    self._resolve_order()

            }


    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ) -> Dict[str, Any]:

        validation = self.validate()

        with self.lock:

            enabled = sum(
                1
                for spec
                in self.dependencies.values()
                if spec.enabled
            )

            return {

                "status":
                    "ONLINE"
                    if validation["valid"]
                    else
                    "WARNING",

                "version":
                    DEPENDENCY_VERSION,

                "api_version":
                    API_VERSION,

                "modules":
                    len(
                        self.dependencies
                    ),

                "enabled":
                    enabled,

                "registered":
                    self.register_count,

                "errors":
                    self.error_count,

                "validation":
                    validation,

                "resolved_order":
                    (
                        self._resolve_order()
                        if validation["valid"]
                        else []
                    ),

                "started_at":
                    self.started_at

            }


    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self
    ):

        with self.lock:

            self.dependencies.clear()

            self.registration_order.clear()

            self.register_count = 0

            self.error_count = 0

        logger.info(
            "Dependency Manager reset."
        )

        return True


# ============================================================
#
# GLOBAL DEPENDENCY MANAGER
#
# ============================================================

dependency_manager = DependencyManager()


# ============================================================
#
# COMPATIBILITY API
#
# ============================================================

def register(
    name: str,
    **kwargs
):

    return dependency_manager.register(
        name,
        **kwargs
    )


def unregister(
    name: str
):

    return dependency_manager.unregister(
        name
    )


def exists(
    name: str
):

    return dependency_manager.exists(
        name
    )


def get(
    name: str
):

    return dependency_manager.get(
        name
    )


def resolve_order():

    return dependency_manager.resolve_order()


def enabled_order():

    return dependency_manager.enabled_order()


def validate():

    return dependency_manager.validate()


def graph():

    return dependency_manager.graph()


def snapshot():

    return dependency_manager.snapshot()


def status():

    return dependency_manager.status()


# ============================================================
#
# STANDARD FOUNDATION MODULES
#
# ============================================================

register(
    "system_config",
    version="3.0",
    description="Central system configuration layer."
)

register(
    "serializer",
    version="1.0",
    description="Safe serialization layer.",
    required=[
        "system_config"
    ]
)

register(
    "contracts",
    version="1.0",
    description="Stable module contracts.",
    required=[
        "system_config"
    ]
)

register(
    "event_system",
    version="3.0",
    description="Central event bus.",
    required=[
        "contracts",
        "system_config"
    ]
)

register(
    "engine",
    version="1.0",
    description="Stable intelligence engine API.",
    required=[
        "contracts",
        "system_config",
        "event_system"
    ]
)


# ============================================================
#
# TEST
#
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO
    )

    print()
    print("=" * 60)
    print("INKSIDE INTELLIGENCE OS")
    print("DEPENDENCY MANAGER TEST")
    print("=" * 60)
    print()

    print("MODULE GRAPH:")
    print(
        graph()
    )

    print()
    print("RESOLVED ORDER:")
    print(
        resolve_order()
    )

    print()
    print("VALIDATION:")
    print(
        validate()
    )

    print()
    print("STATUS:")
    print(
        status()
    )

    print()
    print("=" * 60)
    print("DEPENDENCY MANAGER TEST COMPLETE")
    print("=" * 60)