# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# RUNTIME SYSTEM
# FOUNDATION v3.0
#
# Compatible Engine API: v1.0
#
# ============================================================
#
# PURPOSE
# ------------------------------------------------------------
# Runtime lifecycle manager for the entire Intelligence OS.
#
# Responsibilities:
#
# - Application lifecycle
# - Start / stop / restart
# - Runtime state
# - Module registration
# - Module lifecycle
# - Runtime heartbeat
# - Shutdown coordination
# - Safe execution
# - Runtime statistics
# - Event integration
# - Future module compatibility
#
# IMPORTANT:
# ------------------------------------------------------------
# runtime.py MUST NOT contain intelligence logic.
#
# Intelligence belongs to engine.py and future modules.
#
# runtime.py only manages:
#
#     START
#       ↓
#     RUNTIME
#       ↓
#     MODULES
#       ↓
#     EVENTS
#       ↓
#     SHUTDOWN
#
# ============================================================

from __future__ import annotations

import logging
import threading
import time

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

RUNTIME_VERSION = "3.0"

# Stable compatibility API.
API_VERSION = "1.0"


# ============================================================
#
# RUNTIME STATES
#
# ============================================================

STATE_CREATED = "CREATED"
STATE_STARTING = "STARTING"
STATE_RUNNING = "RUNNING"
STATE_STOPPING = "STOPPING"
STATE_STOPPED = "STOPPED"
STATE_ERROR = "ERROR"


# ============================================================
#
# RUNTIME EVENTS
#
# ============================================================

EVENT_RUNTIME_CREATED = "runtime.created"
EVENT_RUNTIME_STARTING = "runtime.starting"
EVENT_RUNTIME_STARTED = "runtime.started"
EVENT_RUNTIME_STOPPING = "runtime.stopping"
EVENT_RUNTIME_STOPPED = "runtime.stopped"
EVENT_RUNTIME_RESTARTED = "runtime.restarted"
EVENT_RUNTIME_ERROR = "runtime.error"
EVENT_RUNTIME_HEARTBEAT = "runtime.heartbeat"
EVENT_MODULE_REGISTERED = "runtime.module.registered"
EVENT_MODULE_STARTED = "runtime.module.started"
EVENT_MODULE_STOPPED = "runtime.module.stopped"
EVENT_MODULE_ERROR = "runtime.module.error"


# ============================================================
#
# RUNTIME CONFIGURATION
#
# ============================================================

DEFAULT_HEARTBEAT_INTERVAL = 10.0


# ============================================================
#
# RUNTIME STATISTICS
#
# ============================================================

@dataclass
class RuntimeStats:

    starts: int = 0

    stops: int = 0

    restarts: int = 0

    heartbeat_count: int = 0

    module_starts: int = 0

    module_stops: int = 0

    module_errors: int = 0

    runtime_errors: int = 0

    last_start: Optional[str] = None

    last_stop: Optional[str] = None

    last_restart: Optional[str] = None

    last_heartbeat: Optional[str] = None

    last_error: Optional[str] = None

    started_at: Optional[str] = None

    uptime_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:

        return {
            "starts": self.starts,
            "stops": self.stops,
            "restarts": self.restarts,
            "heartbeat_count": self.heartbeat_count,
            "module_starts": self.module_starts,
            "module_stops": self.module_stops,
            "module_errors": self.module_errors,
            "runtime_errors": self.runtime_errors,
            "last_start": self.last_start,
            "last_stop": self.last_stop,
            "last_restart": self.last_restart,
            "last_heartbeat": self.last_heartbeat,
            "last_error": self.last_error,
            "started_at": self.started_at,
            "uptime_seconds": self.uptime_seconds,
        }


# ============================================================
#
# RUNTIME MODULE
#
# ============================================================

@dataclass
class RuntimeModule:

    name: str

    instance: Any

    version: str = "1.0"

    enabled: bool = True

    started: bool = False

    healthy: bool = True

    registered_at: str = field(
        default_factory=lambda:
            datetime.utcnow().isoformat() + "Z"
    )

    started_at: Optional[str] = None

    stopped_at: Optional[str] = None

    errors: int = 0

    last_error: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:

        return {

            "name": self.name,

            "version": self.version,

            "enabled": self.enabled,

            "started": self.started,

            "healthy": self.healthy,

            "registered_at": self.registered_at,

            "started_at": self.started_at,

            "stopped_at": self.stopped_at,

            "errors": self.errors,

            "last_error": self.last_error,

            "metadata": dict(self.metadata)

        }


# ============================================================
#
# RUNTIME MANAGER
#
# ============================================================

class RuntimeManager:
    """
    Central lifecycle manager.

    RuntimeManager deliberately does not contain intelligence
    processing logic.

    It manages application lifecycle and modules only.
    """

    NAME = "runtime"

    VERSION = RUNTIME_VERSION

    API_VERSION = API_VERSION

    def __init__(
        self,
        heartbeat_interval: float =
        DEFAULT_HEARTBEAT_INTERVAL
    ):

        self.lock = threading.RLock()

        self.state = STATE_CREATED

        self.enabled = True

        self.heartbeat_interval = max(
            0.5,
            float(heartbeat_interval)
        )

        self.modules: Dict[
            str,
            RuntimeModule
        ] = {}

        self.stats = RuntimeStats()

        self.created_at = (
            datetime.utcnow()
            .isoformat()
            + "Z"
        )

        self._runtime_thread: Optional[
            threading.Thread
        ] = None

        self._stop_event = threading.Event()

        self._heartbeat_callbacks = []

        self._event_callback: Optional[
            Callable
        ] = None

        logger.info(
            "Runtime Manager v%s initialized.",
            RUNTIME_VERSION
        )


    # ========================================================
    #
    # EVENT CONNECTOR
    #
    # ========================================================

    def set_event_callback(
        self,
        callback: Optional[Callable]
    ) -> None:
        """
        Connect runtime to event.py.

        callback(event_name, data)
        """

        if callback is not None:

            if not callable(callback):

                raise TypeError(
                    "event callback must be callable"
                )

        with self.lock:

            self._event_callback = callback


    # ========================================================
    #
    # INTERNAL EVENT EMITTER
    #
    # ========================================================

    def _emit(
        self,
        event_name: str,
        data: Any = None
    ) -> None:

        callback = None

        with self.lock:

            callback = self._event_callback

        if callback is None:

            return

        try:

            callback(
                event_name,
                data
            )

        except Exception as exc:

            logger.debug(
                "Runtime event emission failed: %s",
                exc
            )


    # ========================================================
    #
    # REGISTER MODULE
    #
    # ========================================================

    def register(
        self,
        name: str,
        module: Any,
        *,
        version: str = "1.0",
        enabled: bool = True,
        metadata: Optional[
            Dict[str, Any]
        ] = None
    ) -> RuntimeModule:
        """
        Register a module with the runtime.
        """

        if not name:

            raise ValueError(
                "module name cannot be empty"
            )

        if module is None:

            raise ValueError(
                "module cannot be None"
            )

        with self.lock:

            if name in self.modules:

                raise ValueError(
                    f"Module already registered: {name}"
                )

            runtime_module = RuntimeModule(

                name=name,

                instance=module,

                version=version,

                enabled=enabled,

                metadata=dict(
                    metadata or {}
                )

            )

            self.modules[name] = (
                runtime_module
            )

        logger.info(
            "Runtime module registered: %s",
            name
        )

        self._emit(
            EVENT_MODULE_REGISTERED,
            {
                "name": name,
                "version": version
            }
        )

        return runtime_module


    # ========================================================
    #
    # UNREGISTER MODULE
    #
    # ========================================================

    def unregister(
        self,
        name: str
    ) -> bool:

        with self.lock:

            module = self.modules.get(
                name
            )

        if module is None:

            return False

        if module.started:

            self._stop_module(
                module
            )

        with self.lock:

            self.modules.pop(
                name,
                None
            )

        return True


    # ========================================================
    #
    # GET MODULE
    #
    # ========================================================

    def get_module(
        self,
        name: str
    ) -> Any:

        with self.lock:

            module = self.modules.get(
                name
            )

            if module is None:

                return None

            return module.instance


    # ========================================================
    #
    # GET RUNTIME MODULE
    #
    # ========================================================

    def get_runtime_module(
        self,
        name: str
    ) -> Optional[RuntimeModule]:

        with self.lock:

            return self.modules.get(
                name
            )


    # ========================================================
    #
    # START MODULE
    #
    # ========================================================

    def _start_module(
        self,
        runtime_module: RuntimeModule
    ) -> bool:

        if not runtime_module.enabled:

            return False

        if runtime_module.started:

            return True

        module = runtime_module.instance

        try:

            start_method = getattr(
                module,
                "start",
                None
            )

            if callable(start_method):

                result = start_method()

                if result is False:

                    raise RuntimeError(
                        "module start() returned False"
                    )

            runtime_module.started = True

            runtime_module.healthy = True

            runtime_module.started_at = (
                datetime.utcnow()
                .isoformat()
                + "Z"
            )

            self.stats.module_starts += 1

            logger.info(
                "Runtime module started: %s",
                runtime_module.name
            )

            self._emit(
                EVENT_MODULE_STARTED,
                {
                    "name":
                        runtime_module.name
                }
            )

            return True

        except Exception as exc:

            runtime_module.errors += 1

            runtime_module.healthy = False

            runtime_module.last_error = str(
                exc
            )

            self.stats.module_errors += 1

            logger.exception(
                "Failed to start module: %s",
                runtime_module.name
            )

            self._emit(
                EVENT_MODULE_ERROR,
                {
                    "name":
                        runtime_module.name,

                    "error":
                        str(exc)
                }
            )

            return False


    # ========================================================
    #
    # STOP MODULE
    #
    # ========================================================

    def _stop_module(
        self,
        runtime_module: RuntimeModule
    ) -> bool:

        if not runtime_module.started:

            return True

        module = runtime_module.instance

        try:

            stop_method = getattr(
                module,
                "stop",
                None
            )

            if callable(stop_method):

                result = stop_method()

                if result is False:

                    logger.warning(
                        "Module stop returned False: %s",
                        runtime_module.name
                    )

            runtime_module.started = False

            runtime_module.stopped_at = (
                datetime.utcnow()
                .isoformat()
                + "Z"
            )

            self.stats.module_stops += 1

            logger.info(
                "Runtime module stopped: %s",
                runtime_module.name
            )

            self._emit(
                EVENT_MODULE_STOPPED,
                {
                    "name":
                        runtime_module.name
                }
            )

            return True

        except Exception as exc:

            runtime_module.errors += 1

            runtime_module.healthy = False

            runtime_module.last_error = str(
                exc
            )

            self.stats.module_errors += 1

            logger.exception(
                "Failed to stop module: %s",
                runtime_module.name
            )

            return False


    # ========================================================
    #
    # START RUNTIME
    #
    # ========================================================

    def start(self) -> bool:

        with self.lock:

            if self.state == STATE_RUNNING:

                return True

            if self.state == STATE_STARTING:

                return False

            self.state = STATE_STARTING

            self._stop_event.clear()

        logger.info(
            "Runtime starting..."
        )

        self._emit(
            EVENT_RUNTIME_STARTING
        )

        try:

            with self.lock:

                modules = list(
                    self.modules.values()
                )

            for runtime_module in modules:

                self._start_module(
                    runtime_module
                )

            with self.lock:

                self.state = STATE_RUNNING

                self.stats.starts += 1

                self.stats.last_start = (
                    datetime.utcnow()
                    .isoformat()
                    + "Z"
                )

                self.stats.started_at = (
                    self.stats.last_start
                )

            self._start_heartbeat()

            self._emit(
                EVENT_RUNTIME_STARTED
            )

            logger.info(
                "Runtime started successfully."
            )

            return True

        except Exception as exc:

            with self.lock:

                self.state = STATE_ERROR

                self.stats.runtime_errors += 1

                self.stats.last_error = str(
                    exc
                )

            logger.exception(
                "Runtime start failed."
            )

            self._emit(
                EVENT_RUNTIME_ERROR,
                {
                    "error": str(exc)
                }
            )

            return False


    # ========================================================
    #
    # STOP RUNTIME
    #
    # ========================================================

    def stop(self) -> bool:

        with self.lock:

            if self.state == STATE_STOPPED:

                return True

            if self.state == STATE_STOPPING:

                return False

            self.state = STATE_STOPPING

            self._stop_event.set()

        logger.info(
            "Runtime stopping..."
        )

        self._emit(
            EVENT_RUNTIME_STOPPING
        )

        with self.lock:

            modules = list(
                self.modules.values()
            )

        # Stop in reverse registration order.
        for runtime_module in reversed(
            modules
        ):

            self._stop_module(
                runtime_module
            )

        with self.lock:

            self.state = STATE_STOPPED

            self.stats.stops += 1

            self.stats.last_stop = (
                datetime.utcnow()
                .isoformat()
                + "Z"
            )

            self._update_uptime_locked()

        self._emit(
            EVENT_RUNTIME_STOPPED
        )

        logger.info(
            "Runtime stopped."
        )

        return True


    # ========================================================
    #
    # RESTART
    #
    # ========================================================

    def restart(self) -> bool:

        logger.info(
            "Runtime restart requested."
        )

        if not self.stop():

            return False

        with self.lock:

            self.stats.restarts += 1

            self.stats.last_restart = (
                datetime.utcnow()
                .isoformat()
                + "Z"
            )

        result = self.start()

        if result:

            self._emit(
                EVENT_RUNTIME_RESTARTED
            )

        return result


    # ========================================================
    #
    # HEARTBEAT
    #
    # ========================================================

    def _start_heartbeat(self) -> None:

        with self.lock:

            if (
                self._runtime_thread is not None
                and self._runtime_thread.is_alive()
            ):

                return

            self._runtime_thread = (
                threading.Thread(
                    target=self._heartbeat_loop,
                    name="InksideRuntimeHeartbeat",
                    daemon=True
                )
            )

            self._runtime_thread.start()


    def _heartbeat_loop(self) -> None:

        while not self._stop_event.wait(
            self.heartbeat_interval
        ):

            with self.lock:

                if self.state != STATE_RUNNING:

                    continue

                self.stats.heartbeat_count += 1

                self.stats.last_heartbeat = (
                    datetime.utcnow()
                    .isoformat()
                    + "Z"
                )

                self._update_uptime_locked()

            self._run_heartbeat_callbacks()

            self._emit(
                EVENT_RUNTIME_HEARTBEAT,
                self.status()
            )


    # ========================================================
    #
    # HEARTBEAT CALLBACK
    #
    # ========================================================

    def add_heartbeat_callback(
        self,
        callback: Callable
    ) -> bool:

        if not callable(callback):

            raise TypeError(
                "callback must be callable"
            )

        with self.lock:

            if callback not in (
                self._heartbeat_callbacks
            ):

                self._heartbeat_callbacks.append(
                    callback
                )

        return True


    def remove_heartbeat_callback(
        self,
        callback: Callable
    ) -> bool:

        with self.lock:

            if callback in (
                self._heartbeat_callbacks
            ):

                self._heartbeat_callbacks.remove(
                    callback
                )

                return True

        return False


    def _run_heartbeat_callbacks(
        self
    ) -> None:

        with self.lock:

            callbacks = list(
                self._heartbeat_callbacks
            )

        for callback in callbacks:

            try:

                callback(
                    self.status()
                )

            except Exception as exc:

                logger.debug(
                    "Heartbeat callback failed: %s",
                    exc
                )


    # ========================================================
    #
    # UPTIME
    #
    # ========================================================

    def _update_uptime_locked(
        self
    ) -> None:

        if not self.stats.started_at:

            self.stats.uptime_seconds = 0.0

            return

        try:

            started = datetime.fromisoformat(
                self.stats.started_at
                .replace("Z", "")
            )

            now = datetime.utcnow()

            self.stats.uptime_seconds = max(
                0.0,
                (
                    now - started
                ).total_seconds()
            )

        except Exception:

            self.stats.uptime_seconds = 0.0


    # ========================================================
    #
    # HEALTH
    #
    # ========================================================

    def health(self) -> Dict[str, Any]:

        with self.lock:

            modules = {
                name:
                    module.to_dict()
                for name, module
                in self.modules.items()
            }

            healthy = (
                self.state
                == STATE_RUNNING
            )

            for module in self.modules.values():

                if module.enabled and not module.healthy:

                    healthy = False

                    break

            return {

                "status":
                    "HEALTHY"
                    if healthy
                    else
                    "UNHEALTHY",

                "state":
                    self.state,

                "version":
                    RUNTIME_VERSION,

                "api_version":
                    API_VERSION,

                "modules":
                    modules,

                "stats":
                    self.stats.to_dict()

            }


    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(self) -> Dict[str, Any]:

        with self.lock:

            self._update_uptime_locked()

            modules = {}

            for name, module in (
                self.modules.items()
            ):

                modules[name] = {

                    "version":
                        module.version,

                    "enabled":
                        module.enabled,

                    "started":
                        module.started,

                    "healthy":
                        module.healthy,

                    "errors":
                        module.errors,

                    "last_error":
                        module.last_error

                }

            return {

                "runtime":
                    self.NAME,

                "version":
                    RUNTIME_VERSION,

                "api_version":
                    API_VERSION,

                "state":
                    self.state,

                "enabled":
                    self.enabled,

                "created_at":
                    self.created_at,

                "uptime_seconds":
                    self.stats.uptime_seconds,

                "modules":
                    modules,

                "statistics":
                    self.stats.to_dict()

            }


    # ========================================================
    #
    # ENABLE
    #
    # ========================================================

    def enable(self) -> bool:

        with self.lock:

            self.enabled = True

        return True


    # ========================================================
    #
    # DISABLE
    #
    # ========================================================

    def disable(self) -> bool:

        with self.lock:

            self.enabled = False

        return True


    # ========================================================
    #
    # IS RUNNING
    #
    # ========================================================

    def is_running(self) -> bool:

        with self.lock:

            return (
                self.state
                == STATE_RUNNING
            )


    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self,
        clear_modules: bool = False
    ) -> bool:

        if self.is_running():

            self.stop()

        with self.lock:

            self.state = STATE_CREATED

            self.stats = RuntimeStats()

            self._stop_event.clear()

            if clear_modules:

                self.modules.clear()

        logger.info(
            "Runtime reset."
        )

        return True


# ============================================================
#
# GLOBAL RUNTIME
#
# ============================================================

runtime = RuntimeManager()


# ============================================================
#
# COMPATIBILITY FUNCTIONS
#
# ============================================================

def start() -> bool:

    return runtime.start()


def stop() -> bool:

    return runtime.stop()


def restart() -> bool:

    return runtime.restart()


def register(
    name: str,
    module: Any,
    *,
    version: str = "1.0",
    enabled: bool = True,
    metadata: Optional[
        Dict[str, Any]
    ] = None
):

    return runtime.register(
        name,
        module,
        version=version,
        enabled=enabled,
        metadata=metadata
    )


def unregister(
    name: str
) -> bool:

    return runtime.unregister(
        name
    )


def get_module(
    name: str
) -> Any:

    return runtime.get_module(
        name
    )


def status() -> Dict[str, Any]:

    return runtime.status()


def health() -> Dict[str, Any]:

    return runtime.health()


def is_running() -> bool:

    return runtime.is_running()


# ============================================================
#
# TEST MODULE
#
# ============================================================

class _TestModule:

    NAME = "test_module"

    VERSION = "1.0"

    def __init__(self):

        self.started = False

    def start(self):

        self.started = True

        return True

    def stop(self):

        self.started = False

        return True


# ============================================================
#
# TEST
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
    print("RUNTIME SYSTEM TEST")
    print("=" * 70)
    print()

    test_module = _TestModule()

    register(
        "test_module",
        test_module,
        version="1.0"
    )

    print("REGISTERED:")
    print(status())

    print()
    print("STARTING RUNTIME...")

    start()

    print()
    print("RUNTIME STATUS:")
    print(status())

    print()
    print("RUNTIME HEALTH:")
    print(health())

    time.sleep(1)

    print()
    print("STOPPING RUNTIME...")

    stop()

    print()
    print("FINAL STATUS:")
    print(status())

    print()
    print("=" * 70)
    print("RUNTIME TEST COMPLETE")
    print("=" * 70)