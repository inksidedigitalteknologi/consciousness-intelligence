
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# MODULE BASE v2.0
#
# Universal Production Foundation for Intelligence Modules
#
# ============================================================
#
# PURPOSE
#
# - Standardize all intelligence modules
# - Stable lifecycle management
# - Standard input/output contract
# - Error isolation
# - Health monitoring
# - Runtime metrics
# - Execution timing
# - Configuration management
# - Capability management
# - Dependency declaration
# - Lifecycle hooks
# - Execution hooks
# - Event tracking
# - Failure tracking
# - Reset support
# - Safe snapshots
# - Runtime statistics
# - Backward compatibility
# - Future-proof extension
#
# ============================================================

from __future__ import annotations

import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    Optional,
    Iterable,
)

from .contracts import (
    ModuleStatus,
    ModuleInput,
    ModuleOutput,
    create_input,
    normalize_output,
    safe_copy,
    safe_json,
    utc_now,
    validate_output,
    generate_id,
)

logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

MODULE_BASE_VERSION = "2.0"
MODULE_BASE_API_VERSION = "1.0"


# ============================================================
#
# EXECUTION STATES
#
# ============================================================

MODULE_STATE_CREATED = "created"
MODULE_STATE_INITIALIZING = "initializing"
MODULE_STATE_READY = "ready"
MODULE_STATE_RUNNING = "running"
MODULE_STATE_STOPPING = "stopping"
MODULE_STATE_STOPPED = "stopped"
MODULE_STATE_ERROR = "error"
MODULE_STATE_DISABLED = "disabled"


# ============================================================
#
# EXECUTION RESULT TYPES
#
# ============================================================

EXECUTION_SUCCESS = "success"
EXECUTION_FAILURE = "failure"
EXECUTION_SKIPPED = "skipped"


# ============================================================
#
# MODULE BASE
#
# ============================================================

class IntelligenceModule(ABC):
    """
    Universal production foundation for INKSIDE Intelligence OS.

    Every intelligence module should inherit from this class.

    Example:

        class PatternEngine(IntelligenceModule):

            NAME = "pattern"
            VERSION = "2.0"

            DESCRIPTION = (
                "Detects market patterns."
            )

            CAPABILITIES = {
                "pattern_detection",
                "technical_analysis",
            }

            DEPENDENCIES = {
                "market_data",
            }

            def process(self, data):
                return {
                    "patterns": []
                }

    Child modules should normally implement only:

        process()

    Optional lifecycle hooks can also be overridden:

        on_initialize()
        on_start()
        on_stop()
        on_error()
        before_process()
        after_process()

    The public execution interface is:

        module.execute(...)

    Direct calls to process() remain supported for compatibility,
    but production engine code should preferably use execute().
    """

    # ========================================================
    #
    # MODULE IDENTITY
    #
    # ========================================================

    NAME = "unnamed"

    VERSION = "1.0"

    DESCRIPTION = ""

    AUTHOR = "INKSIDE DIGITAL"

    CATEGORY = "intelligence"

    # ========================================================
    #
    # CAPABILITIES
    #
    # ========================================================

    CAPABILITIES = set()

    # ========================================================
    #
    # DEPENDENCIES
    #
    # ========================================================

    DEPENDENCIES = set()

    # ========================================================
    #
    # OPERATIONS
    #
    # ========================================================

    OPERATIONS = [
        "process",
    ]

    # ========================================================
    #
    # PRIORITY
    #
    # ========================================================

    PRIORITY = 100

    # ========================================================
    #
    # CRITICAL MODULE
    #
    # ========================================================

    CRITICAL = False

    # ========================================================
    #
    # AUTO INITIALIZATION
    #
    # ========================================================

    AUTO_INITIALIZE = False

    # ========================================================
    #
    # ALLOW CONCURRENT EXECUTION
    #
    # ========================================================

    ALLOW_CONCURRENT_EXECUTION = True

    # ========================================================
    #
    # DEFAULT CONFIGURATION
    #
    # ========================================================

    DEFAULT_CONFIG: Dict[str, Any] = {}

    # ========================================================
    #
    # CONFIGURATION KEYS
    #
    # ========================================================

    CONFIG_SCHEMA: Dict[str, Any] = {}

    # ========================================================
    #
    # INITIALIZATION
    #
    # ========================================================

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:

        # ----------------------------------------------------
        # Runtime lock
        # ----------------------------------------------------

        self._lock = threading.RLock()

        # ----------------------------------------------------
        # Execution lock
        # ----------------------------------------------------

        self._execution_lock = threading.Lock()

        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------

        self.config = safe_copy(
            self.DEFAULT_CONFIG
        )

        if config:

            self.config.update(
                safe_copy(config)
            )

        # ----------------------------------------------------
        # Module status
        # ----------------------------------------------------

        self.status = ModuleStatus(
            name=self.NAME,
            version=self.VERSION,
        )

        # ----------------------------------------------------
        # Runtime identity
        # ----------------------------------------------------

        self.instance_id = generate_id(
            "module"
        )

        self.created_at = utc_now()

        self.started_at: Optional[str] = None

        self.stopped_at: Optional[str] = None

        self.last_execution_at: Optional[str] = None

        self.last_success_at: Optional[str] = None

        self.last_failure_at: Optional[str] = None

        # ----------------------------------------------------
        # Runtime state
        # ----------------------------------------------------

        self.state = MODULE_STATE_CREATED

        self.enabled = True

        self.initialized = False

        self.running = False

        # ----------------------------------------------------
        # Execution statistics
        # ----------------------------------------------------

        self.execution_count = 0

        self.success_count = 0

        self.failure_count = 0

        self.skipped_count = 0

        self.error_count = 0

        self.warning_count = 0

        # ----------------------------------------------------
        # Timing statistics
        # ----------------------------------------------------

        self.last_duration = 0.0

        self.total_duration = 0.0

        self.min_duration = 0.0

        self.max_duration = 0.0

        self.average_duration = 0.0

        # ----------------------------------------------------
        # Runtime objects
        # ----------------------------------------------------

        self.last_output: Optional[
            ModuleOutput
        ] = None

        self.last_input: Optional[
            ModuleInput
        ] = None

        self.last_error: Optional[str] = None

        self.metadata: Dict[str, Any] = {}

        # ----------------------------------------------------
        # Failure history
        # ----------------------------------------------------

        self.failure_history = []

        self.max_failure_history = 100

        # ----------------------------------------------------
        # Execution history
        # ----------------------------------------------------

        self.execution_history = []

        self.max_execution_history = 100

        # ----------------------------------------------------
        # Lifecycle
        # ----------------------------------------------------

        logger.info(
            "Module created: %s v%s [%s]",
            self.NAME,
            self.VERSION,
            self.instance_id,
        )

        if self.AUTO_INITIALIZE:

            try:

                self.initialize()

            except Exception:

                logger.exception(
                    "Automatic initialization failed: %s",
                    self.NAME,
                )

    # ========================================================
    #
    # PRIMARY PROCESS
    #
    # ========================================================

    @abstractmethod
    def process(
        self,
        data: Any = None,
    ) -> Any:
        """
        Main module operation.

        Child modules should implement this method.

        The return value may be:

        - ModuleOutput
        - dict
        - list
        - primitive
        - arbitrary Python object

        execute() will normalize the result into ModuleOutput.
        """

        raise NotImplementedError(
            f"{self.NAME}.process() "
            "must be implemented."
        )

    # ========================================================
    #
    # INITIALIZE
    #
    # ========================================================

    def initialize(self) -> bool:
        """
        Initialize the module.

        Safe to call multiple times.
        """

        with self._lock:

            if self.initialized:

                return True

            self.state = (
                MODULE_STATE_INITIALIZING
            )

            try:

                self.on_initialize()

                self.initialized = True

                self.state = (
                    MODULE_STATE_READY
                )

                self.status.mark_healthy()

                logger.info(
                    "Module initialized: %s",
                    self.NAME,
                )

                return True

            except Exception as exc:

                self.initialized = False

                self.state = (
                    MODULE_STATE_ERROR
                )

                self.status.mark_error(
                    exc
                )

                self.last_error = str(exc)

                logger.exception(
                    "Module initialization failed: %s",
                    self.NAME,
                )

                return False

    # ========================================================
    #
    # START
    #
    # ========================================================

    def start(self) -> bool:
        """
        Start the module.
        """

        with self._lock:

            if not self.enabled:

                self.state = (
                    MODULE_STATE_DISABLED
                )

                return False

            if not self.initialized:

                if not self.initialize():

                    return False

            try:

                self.on_start()

                self.running = True

                self.started_at = utc_now()

                self.state = (
                    MODULE_STATE_READY
                )

                self.status.enable()

                logger.info(
                    "Module started: %s",
                    self.NAME,
                )

                return True

            except Exception as exc:

                self.running = False

                self.state = (
                    MODULE_STATE_ERROR
                )

                self.status.mark_error(
                    exc
                )

                self.last_error = str(exc)

                logger.exception(
                    "Module start failed: %s",
                    self.NAME,
                )

                return False

    # ========================================================
    #
    # STOP
    #
    # ========================================================

    def stop(self) -> bool:
        """
        Stop the module without destroying configuration.
        """

        with self._lock:

            self.state = (
                MODULE_STATE_STOPPING
            )

            try:

                self.on_stop()

                self.running = False

                self.stopped_at = utc_now()

                self.state = (
                    MODULE_STATE_STOPPED
                )

                self.status.online = False

                logger.info(
                    "Module stopped: %s",
                    self.NAME,
                )

                return True

            except Exception as exc:

                self.state = (
                    MODULE_STATE_ERROR
                )

                self.status.mark_error(
                    exc
                )

                self.last_error = str(exc)

                logger.exception(
                    "Module stop failed: %s",
                    self.NAME,
                )

                return False

    # ========================================================
    #
    # EXECUTE
    #
    # ========================================================

    def execute(
        self,
        data: Any = None,
        *,
        source: str = "engine",
        context: Optional[
            Dict[str, Any]
        ] = None,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
        request_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        stage: Optional[str] = None,
    ) -> ModuleOutput:
        """
        Safe production execution interface.

        Responsibilities:

        - Input normalization
        - Request identity
        - Execution tracking
        - Timing
        - Error isolation
        - Result normalization
        - Contract validation
        - Metrics
        - Hooks
        - Failure history
        """

        # ----------------------------------------------------
        # Disabled
        # ----------------------------------------------------

        if not self.enabled:

            self.skipped_count += 1

            output = ModuleOutput(
                data=None,
                success=True,
                module=self.NAME,
                version=self.VERSION,
                request_id=request_id,
                skipped=True,
                state="skipped",
            )

            output.add_warning(
                "Module is disabled."
            )

            return output

        # ----------------------------------------------------
        # Initialize if required
        # ----------------------------------------------------

        if not self.initialized:

            if not self.initialize():

                return self._build_failure_output(
                    request_id=request_id,
                    error=(
                        "Module initialization failed."
                    ),
                )

        # ----------------------------------------------------
        # Build input
        # ----------------------------------------------------

        module_input = create_input(
            data=data,
            source=source,
            context=context,
            metadata=metadata,
            request_id=request_id,
            trace_id=trace_id,
            stage=stage,
        )

        self.last_input = module_input

        # ----------------------------------------------------
        # Concurrent execution guard
        # ----------------------------------------------------

        execution_lock_acquired = False

        if not self.ALLOW_CONCURRENT_EXECUTION:

            execution_lock_acquired = (
                self._execution_lock.acquire(
                    blocking=False
                )
            )

            if not execution_lock_acquired:

                self.skipped_count += 1

                output = ModuleOutput(
                    data=None,
                    success=True,
                    module=self.NAME,
                    version=self.VERSION,
                    request_id=(
                        module_input.request_id
                    ),
                    skipped=True,
                    state="skipped",
                )

                output.add_warning(
                    "Module execution already in progress."
                )

                return output

        # ----------------------------------------------------
        # Execution
        # ----------------------------------------------------

        start = time.perf_counter()

        self.execution_count += 1

        self.status.mark_execution()

        self.running = True

        self.state = MODULE_STATE_RUNNING

        self.last_execution_at = utc_now()

        try:

            # ------------------------------------------------
            # Before hook
            # ------------------------------------------------

            self.before_process(
                module_input
            )

            # ------------------------------------------------
            # Process
            # ------------------------------------------------

            raw_output = self.process(
                module_input.data
            )

            # ------------------------------------------------
            # Normalize
            # ------------------------------------------------

            output = normalize_output(
                raw_output,
                module_name=self.NAME,
                request_id=module_input.request_id,
            )

            # ------------------------------------------------
            # Propagate execution context
            # ------------------------------------------------

            output.trace_id = (
                module_input.trace_id
            )

            output.stage = (
                module_input.stage
            )

            # ------------------------------------------------
            # Validate
            # ------------------------------------------------

            if not validate_output(output):

                logger.warning(
                    "Non-standard output from %s. "
                    "Automatically normalizing.",
                    self.NAME,
                )

                output = ModuleOutput(
                    data=safe_copy(
                        raw_output
                    ),
                    success=True,
                    module=self.NAME,
                    version=self.VERSION,
                    request_id=(
                        module_input.request_id
                    ),
                    trace_id=(
                        module_input.trace_id
                    ),
                    stage=(
                        module_input.stage
                    ),
                )

                output.add_warning(
                    "Module returned non-standard "
                    "output; automatically normalized."
                )

            # ------------------------------------------------
            # After hook
            # ------------------------------------------------

            self.after_process(
                module_input,
                output,
            )

            # ------------------------------------------------
            # Metrics
            # ------------------------------------------------

            if output.skipped:

                self.skipped_count += 1

            elif output.success:

                self.success_count += 1

                self.last_success_at = (
                    utc_now()
                )

                self.status.mark_healthy()

            else:

                self.failure_count += 1

                self.last_failure_at = (
                    utc_now()
                )

            self.warning_count += len(
                output.warnings
            )

            self.last_output = output

            self._record_execution(
                output
            )

            return output

        except Exception as exc:

            self.failure_count += 1

            self.error_count += 1

            self.last_failure_at = utc_now()

            self.last_error = str(exc)

            self.state = (
                MODULE_STATE_ERROR
            )

            self.status.mark_error(
                exc
            )

            self._record_failure(
                exc,
                module_input,
            )

            # ------------------------------------------------
            # Error hook
            # ------------------------------------------------

            try:

                self.on_error(
                    exc
                )

            except Exception:

                logger.exception(
                    "Module error hook failed: %s",
                    self.NAME,
                )

            logger.exception(
                "Module execution failed: %s",
                self.NAME,
            )

            output = self._build_failure_output(
                request_id=(
                    module_input.request_id
                ),
                trace_id=(
                    module_input.trace_id
                ),
                stage=(
                    module_input.stage
                ),
                error=str(exc),
            )

            self.last_output = output

            self._record_execution(
                output
            )

            return output

        finally:

            duration = (
                time.perf_counter()
                - start
            )

            self._update_timing(
                duration
            )

            self.running = False

            if self.state != MODULE_STATE_ERROR:

                self.state = (
                    MODULE_STATE_READY
                )

            if execution_lock_acquired:

                self._execution_lock.release()

    # ========================================================
    #
    # FAILURE OUTPUT
    #
    # ========================================================

    def _build_failure_output(
        self,
        *,
        request_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        stage: Optional[str] = None,
        error: str = "Unknown module error.",
    ) -> ModuleOutput:

        output = ModuleOutput(
            data=None,
            success=False,
            module=self.NAME,
            version=self.VERSION,
            request_id=request_id,
            trace_id=trace_id,
            stage=stage,
        )

        output.add_error(
            error
        )

        return output

    # ========================================================
    #
    # TIMING
    #
    # ========================================================

    def _update_timing(
        self,
        duration: float,
    ) -> None:

        self.last_duration = duration

        self.total_duration += duration

        if self.execution_count <= 1:

            self.min_duration = duration

            self.max_duration = duration

        else:

            self.min_duration = min(
                self.min_duration,
                duration,
            )

            self.max_duration = max(
                self.max_duration,
                duration,
            )

        if self.execution_count > 0:

            self.average_duration = (
                self.total_duration
                / self.execution_count
            )

    # ========================================================
    #
    # EXECUTION HISTORY
    #
    # ========================================================

    def _record_execution(
        self,
        output: ModuleOutput,
    ) -> None:

        record = {
            "timestamp": utc_now(),
            "module": self.NAME,
            "instance_id": self.instance_id,
            "request_id": output.request_id,
            "trace_id": output.trace_id,
            "stage": output.stage,
            "success": output.success,
            "state": output.state,
            "confidence": output.confidence,
            "duration": self.last_duration,
        }

        self.execution_history.append(
            record
        )

        if len(
            self.execution_history
        ) > self.max_execution_history:

            del self.execution_history[
                :-self.max_execution_history
            ]

    # ========================================================
    #
    # FAILURE HISTORY
    #
    # ========================================================

    def _record_failure(
        self,
        error: Exception,
        module_input: ModuleInput,
    ) -> None:

        record = {
            "timestamp": utc_now(),
            "module": self.NAME,
            "instance_id": self.instance_id,
            "request_id": module_input.request_id,
            "trace_id": module_input.trace_id,
            "error_type": type(error).__name__,
            "error": str(error),
        }

        self.failure_history.append(
            record
        )

        if len(
            self.failure_history
        ) > self.max_failure_history:

            del self.failure_history[
                :-self.max_failure_history
            ]

    # ========================================================
    #
    # HEALTH
    #
    # ========================================================

    def health(self) -> Dict[str, Any]:
        """
        Return comprehensive runtime health.
        """

        status = self.status.to_dict()

        success_rate = 0.0

        if self.execution_count:

            success_rate = (
                self.success_count
                / self.execution_count
                * 100.0
            )

        error_rate = 0.0

        if self.execution_count:

            error_rate = (
                self.failure_count
                / self.execution_count
                * 100.0
            )

        status.update({

            "module_base_version":
                MODULE_BASE_VERSION,

            "instance_id":
                self.instance_id,

            "name":
                self.NAME,

            "version":
                self.VERSION,

            "description":
                self.DESCRIPTION,

            "author":
                self.AUTHOR,

            "category":
                self.CATEGORY,

            "state":
                self.state,

            "enabled":
                self.enabled,

            "initialized":
                self.initialized,

            "running":
                self.running,

            "critical":
                self.CRITICAL,

            "priority":
                self.PRIORITY,

            "capabilities":
                self.capabilities(),

            "dependencies":
                self.dependencies(),

            "operations":
                list(self.OPERATIONS),

            "execution_count":
                self.execution_count,

            "success_count":
                self.success_count,

            "failure_count":
                self.failure_count,

            "skipped_count":
                self.skipped_count,

            "error_count":
                self.error_count,

            "warning_count":
                self.warning_count,

            "success_rate":
                round(
                    success_rate,
                    4,
                ),

            "error_rate":
                round(
                    error_rate,
                    4,
                ),

            "last_duration":
                self.last_duration,

            "average_duration":
                self.average_duration,

            "min_duration":
                self.min_duration,

            "max_duration":
                self.max_duration,

            "total_duration":
                self.total_duration,

            "created_at":
                self.created_at,

            "started_at":
                self.started_at,

            "stopped_at":
                self.stopped_at,

            "last_execution_at":
                self.last_execution_at,

            "last_success_at":
                self.last_success_at,

            "last_failure_at":
                self.last_failure_at,

            "last_error":
                self.last_error,

        })

        return safe_json(
            status
        )

    # ========================================================
    #
    # ENABLE
    #
    # ========================================================

    def enable(self) -> bool:

        with self._lock:

            self.enabled = True

            self.status.enable()

            if self.state == MODULE_STATE_DISABLED:

                self.state = (
                    MODULE_STATE_READY
                    if self.initialized
                    else MODULE_STATE_CREATED
                )

            logger.info(
                "Module enabled: %s",
                self.NAME,
            )

            return True

    # ========================================================
    #
    # DISABLE
    #
    # ========================================================

    def disable(self) -> bool:

        with self._lock:

            self.enabled = False

            self.running = False

            self.status.disable()

            self.state = (
                MODULE_STATE_DISABLED
            )

            logger.info(
                "Module disabled: %s",
                self.NAME,
            )

            return True

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self,
        *,
        preserve_metadata: bool = False,
    ) -> bool:
        """
        Reset runtime state while preserving configuration.
        """

        try:

            with self._lock:

                preserved_metadata = (
                    safe_copy(
                        self.metadata
                    )
                    if preserve_metadata
                    else {}
                )

                self.status = ModuleStatus(
                    name=self.NAME,
                    version=self.VERSION,
                )

                self.execution_count = 0

                self.success_count = 0

                self.failure_count = 0

                self.skipped_count = 0

                self.error_count = 0

                self.warning_count = 0

                self.last_duration = 0.0

                self.total_duration = 0.0

                self.min_duration = 0.0

                self.max_duration = 0.0

                self.average_duration = 0.0

                self.last_output = None

                self.last_input = None

                self.last_error = None

                self.last_execution_at = None

                self.last_success_at = None

                self.last_failure_at = None

                self.started_at = None

                self.stopped_at = None

                self.failure_history = []

                self.execution_history = []

                self.metadata = (
                    preserved_metadata
                )

                self.enabled = True

                self.running = False

                self.state = (
                    MODULE_STATE_READY
                    if self.initialized
                    else MODULE_STATE_CREATED
                )

                logger.info(
                    "Module reset: %s",
                    self.NAME,
                )

                return True

        except Exception as exc:

            logger.exception(
                "Module reset failed: %s",
                self.NAME,
            )

            self.last_error = str(exc)

            return False

    # ========================================================
    #
    # CONFIGURATION
    #
    # ========================================================

    def configure(
        self,
        config: Optional[
            Dict[str, Any]
        ] = None,
        *,
        replace: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Update module configuration.

        replace=False:
            Merge into existing configuration.

        replace=True:
            Replace configuration completely.
        """

        incoming = {}

        if config:

            incoming.update(
                safe_copy(config)
            )

        if kwargs:

            incoming.update(
                safe_copy(kwargs)
            )

        if replace:

            self.config = incoming

        else:

            self.config.update(
                incoming
            )

        return safe_copy(
            self.config
        )

    # ========================================================
    #
    # GET CONFIG
    #
    # ========================================================

    def get_config(
        self,
        key: Optional[str] = None,
        default: Any = None,
    ) -> Any:

        if key is None:

            return safe_copy(
                self.config
            )

        return safe_copy(
            self.config.get(
                key,
                default,
            )
        )

    # ========================================================
    #
    # SET CONFIG
    #
    # ========================================================

    def set_config(
        self,
        key: str,
        value: Any,
    ) -> bool:

        if not key:

            return False

        self.config[
            str(key)
        ] = safe_copy(value)

        return True

    # ========================================================
    #
    # CAPABILITIES
    #
    # ========================================================

    def capabilities(self) -> list:

        return sorted(
            str(item)
            for item in self.CAPABILITIES
        )

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

    # ========================================================
    #
    # DEPENDENCIES
    #
    # ========================================================

    def dependencies(self) -> list:

        return sorted(
            str(item)
            for item in self.DEPENDENCIES
        )

    def requires(
        self,
        dependency: str,
    ) -> bool:

        if not dependency:

            return False

        return (
            dependency
            in self.DEPENDENCIES
        )

    # ========================================================
    #
    # OPERATION SUPPORT
    #
    # ========================================================

    def supports_operation(
        self,
        operation: str,
    ) -> bool:

        if not operation:

            return False

        return (
            operation
            in self.OPERATIONS
        )

    # ========================================================
    #
    # INFO
    #
    # ========================================================

    def info(self) -> Dict[str, Any]:

        return safe_json({

            "module_base_version":
                MODULE_BASE_VERSION,

            "api_version":
                MODULE_BASE_API_VERSION,

            "instance_id":
                self.instance_id,

            "name":
                self.NAME,

            "version":
                self.VERSION,

            "description":
                self.DESCRIPTION,

            "author":
                self.AUTHOR,

            "category":
                self.CATEGORY,

            "capabilities":
                self.capabilities(),

            "dependencies":
                self.dependencies(),

            "operations":
                list(
                    self.OPERATIONS
                ),

            "priority":
                self.PRIORITY,

            "critical":
                self.CRITICAL,

            "auto_initialize":
                self.AUTO_INITIALIZE,

            "allow_concurrent_execution":
                self.ALLOW_CONCURRENT_EXECUTION,

        })

    # ========================================================
    #
    # SNAPSHOT
    #
    # ========================================================

    def snapshot(
        self,
        *,
        include_history: bool = False,
        include_last_data: bool = False,
    ) -> Dict[str, Any]:
        """
        Return a JSON-safe complete module snapshot.
        """

        result = {

            "info":
                self.info(),

            "health":
                self.health(),

            "config":
                safe_json(
                    self.config
                ),

            "metadata":
                safe_json(
                    self.metadata
                ),

        }

        if include_history:

            result[
                "execution_history"
            ] = safe_json(
                self.execution_history
            )

            result[
                "failure_history"
            ] = safe_json(
                self.failure_history
            )

        if include_last_data:

            result[
                "last_input"
            ] = (
                safe_json(
                    self.last_input.to_dict()
                )
                if self.last_input
                else None
            )

            result[
                "last_output"
            ] = (
                safe_json(
                    self.last_output.to_dict()
                )
                if self.last_output
                else None
            )

        return safe_json(
            result
        )

    # ========================================================
    #
    # METRICS
    #
    # ========================================================

    def metrics(self) -> Dict[str, Any]:

        success_rate = 0.0

        if self.execution_count:

            success_rate = (
                self.success_count
                / self.execution_count
                * 100
            )

        return {

            "execution_count":
                self.execution_count,

            "success_count":
                self.success_count,

            "failure_count":
                self.failure_count,

            "skipped_count":
                self.skipped_count,

            "error_count":
                self.error_count,

            "warning_count":
                self.warning_count,

            "success_rate":
                round(
                    success_rate,
                    4,
                ),

            "last_duration":
                self.last_duration,

            "average_duration":
                self.average_duration,

            "min_duration":
                self.min_duration,

            "max_duration":
                self.max_duration,

            "total_duration":
                self.total_duration,

        }

    # ========================================================
    #
    # PING
    #
    # ========================================================

    def ping(self) -> bool:

        return (
            self.enabled
            and self.initialized
            and self.status.online
            and self.state
            not in {
                MODULE_STATE_ERROR,
                MODULE_STATE_DISABLED,
                MODULE_STATE_STOPPED,
            }
        )

    # ========================================================
    #
    # READY CHECK
    #
    # ========================================================

    def is_ready(self) -> bool:

        return (
            self.enabled
            and self.initialized
            and self.state
            in {
                MODULE_STATE_READY,
                MODULE_STATE_RUNNING,
            }
        )

    # ========================================================
    #
    # EVENT HOOKS
    #
    # ========================================================

    def on_initialize(self) -> None:
        """
        Called during initialization.
        """

        return None

    def on_start(self) -> None:
        """
        Called when module starts.
        """

        return None

    def on_stop(self) -> None:
        """
        Called when module stops.
        """

        return None

    def before_process(
        self,
        module_input: ModuleInput,
    ) -> None:
        """
        Called immediately before process().
        """

        return None

    def after_process(
        self,
        module_input: ModuleInput,
        output: ModuleOutput,
    ) -> None:
        """
        Called immediately after process().
        """

        return None

    def on_error(
        self,
        error: Exception,
    ) -> None:
        """
        Called when execution fails.
        """

        return None

    # ========================================================
    #
    # METADATA
    #
    # ========================================================

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> bool:

        if not key:

            return False

        self.metadata[
            str(key)
        ] = safe_copy(value)

        return True

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return safe_copy(
            self.metadata.get(
                key,
                default,
            )
        )

    # ========================================================
    #
    # FACTORY RESET
    #
    # ========================================================

    def clear_runtime_history(self) -> None:

        self.execution_history.clear()

        self.failure_history.clear()

    # ========================================================
    #
    # STRING REPRESENTATION
    #
    # ========================================================

    def __repr__(self) -> str:

        return (
            f"<{self.__class__.__name__} "
            f"name={self.NAME!r} "
            f"version={self.VERSION!r} "
            f"state={self.state!r} "
            f"enabled={self.enabled!r}>"
        )


# ============================================================
#
# MODULE FACTORY
#
# ============================================================

def create_module(
    module_class,
    config: Optional[
        Dict[str, Any]
    ] = None,
):
    """
    Generic module factory.

    Compatible with future ModuleRegistry.
    """

    if not isinstance(
        module_class,
        type,
    ):

        raise TypeError(
            "module_class must be a class."
        )

    module = module_class(
        config=config
    )

    if not isinstance(
        module,
        IntelligenceModule,
    ):

        raise TypeError(
            f"{module_class.__name__} "
            "must inherit IntelligenceModule."
        )

    return module


# ============================================================
#
# MODULE VALIDATION
#
# ============================================================

def validate_module(
    module: Any,
) -> bool:
    """
    Validate whether an object follows
    the INKSIDE Intelligence Module foundation.
    """

    if not isinstance(
        module,
        IntelligenceModule,
    ):

        return False

    required_attributes = [

        "NAME",
        "VERSION",
        "process",
        "execute",
        "initialize",
        "start",
        "stop",
        "health",
        "reset",
        "configure",
        "info",
        "snapshot",
        "ping",
    ]

    for attribute in required_attributes:

        if not hasattr(
            module,
            attribute,
        ):

            return False

    return True


# ============================================================
#
# MODULE CLASS VALIDATION
#
# ============================================================

def validate_module_class(
    module_class: Any,
) -> bool:
    """
    Validate a module class before registration.
    """

    try:

        return (
            isinstance(
                module_class,
                type,
            )
            and issubclass(
                module_class,
                IntelligenceModule,
            )
        )

    except Exception:

        return False


# ============================================================
#
# MODULE DESCRIPTION
#
# ============================================================

def describe_module(
    module: Any,
) -> Dict[str, Any]:
    """
    Return safe descriptive information.
    """

    if not validate_module(
        module
    ):

        return {
            "valid": False,
            "error": (
                "Object is not a valid "
                "IntelligenceModule."
            ),
        }

    return {
        "valid": True,
        "info": module.info(),
        "health": module.health(),
    }


# ============================================================
#
# MODULE SELF TEST
#
# ============================================================

def self_test(
    module: IntelligenceModule,
) -> Dict[str, Any]:
    """
    Basic module runtime self-test.

    Does not invoke process() automatically because
    arbitrary modules may require structured input.
    """

    result = {

        "module":
            getattr(
                module,
                "NAME",
                "unknown",
            ),

        "valid":
            False,

        "initialized":
            False,

        "enabled":
            False,

        "ping":
            False,

        "healthy":
            False,

        "timestamp":
            utc_now(),

        "errors":
            [],
    }

    try:

        result["valid"] = (
            validate_module(
                module
            )
        )

        result["enabled"] = (
            module.enabled
        )

        result["initialized"] = (
            module.initialized
        )

        result["ping"] = (
            module.ping()
        )

        result["healthy"] = (
            module.status.healthy
        )

        return safe_json(
            result
        )

    except Exception as exc:

        result[
            "errors"
        ].append(
            str(exc)
        )

        return safe_json(
            result
        )


# ============================================================
#
# PUBLIC API
#
# ============================================================

__all__ = [

    # Version
    "MODULE_BASE_VERSION",
    "MODULE_BASE_API_VERSION",

    # States
    "MODULE_STATE_CREATED",
    "MODULE_STATE_INITIALIZING",
    "MODULE_STATE_READY",
    "MODULE_STATE_RUNNING",
    "MODULE_STATE_STOPPING",
    "MODULE_STATE_STOPPED",
    "MODULE_STATE_ERROR",
    "MODULE_STATE_DISABLED",

    # Results
    "EXECUTION_SUCCESS",
    "EXECUTION_FAILURE",
    "EXECUTION_SKIPPED",

    # Main class
    "IntelligenceModule",

    # Factory
    "create_module",

    # Validation
    "validate_module",
    "validate_module_class",

    # Utilities
    "describe_module",
    "self_test",
]

