# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# EVENT SYSTEM
# FOUNDATION v3.1
#
# Compatible Engine API: v1.0
#
# ============================================================
#
# PURPOSE
# ------------------------------------------------------------
# Central Event Bus for the entire Intelligence OS.
#
# DESIGN GOALS
# ------------------------------------------------------------
# - Stable API
# - Thread safe
# - Event driven architecture
# - Loose coupling between modules
# - Future proof
# - Safe handler execution
# - Event history
# - Priority support
# - Wildcard subscriptions
# - Runtime subscribe / unsubscribe
# - Async publishing
# - Handler metrics
# - UUID event identity
# - UTC timestamps
# - Event filtering
# - Handler lifecycle control
# - Handler object unsubscribe
# - Once-only handlers
# - Event history search
# - Diagnostics
# - Self test
#
# IMPORTANT
# ------------------------------------------------------------
# API_VERSION MUST REMAIN "1.0"
#
# EVENT_VERSION may evolve internally without forcing
# engine.py or other modules to change.
#
# ============================================================

from __future__ import annotations

import inspect
import logging
import threading
import time
import uuid

from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
)


logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

EVENT_VERSION = "3.1"

# Stable public compatibility contract.
API_VERSION = "1.0"


# ============================================================
#
# EVENT PRIORITY
#
# ============================================================

PRIORITY_LOW = 10
PRIORITY_NORMAL = 50
PRIORITY_HIGH = 75
PRIORITY_CRITICAL = 100


# ============================================================
#
# TIME HELPERS
#
# ============================================================

def utc_now() -> str:
    """
    Return current UTC timestamp in ISO-8601 format.
    """

    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


# ============================================================
#
# EVENT RESULT
#
# ============================================================

@dataclass
class EventResult:
    """
    Result returned by an event handler.
    """

    handler: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    duration: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary.
        """

        return {
            "handler": self.handler,
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "duration": self.duration,
        }


# ============================================================
#
# EVENT
#
# ============================================================

@dataclass
class Event:
    """
    Event container.

    Events should contain data rather than references to
    large engine/module objects.
    """

    name: str
    data: Any = None

    source: str = "system"

    priority: int = PRIORITY_NORMAL

    timestamp: str = field(
        default_factory=utc_now
    )

    event_id: str = field(
        default_factory=lambda: uuid.uuid4().hex
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert event to dictionary.
        """

        return {
            "name": self.name,
            "data": self.data,
            "source": self.source,
            "priority": self.priority,
            "timestamp": self.timestamp,
            "event_id": self.event_id,
            "metadata": dict(self.metadata),
        }


# ============================================================
#
# EVENT HANDLER
#
# ============================================================

@dataclass
class EventHandler:
    """
    Registered event handler.
    """

    callback: Callable

    event_name: str

    priority: int = PRIORITY_NORMAL

    name: str = ""

    enabled: bool = True

    once: bool = False

    calls: int = 0

    successes: int = 0

    errors: int = 0

    last_call: Optional[str] = None

    last_success: Optional[str] = None

    last_error: Optional[str] = None

    total_duration: float = 0.0

    registered_at: str = field(
        default_factory=utc_now
    )

    handler_id: str = field(
        default_factory=lambda: uuid.uuid4().hex
    )

    def __post_init__(self):
        """
        Generate a readable handler name when none is provided.
        """

        if not self.name:

            self.name = getattr(
                self.callback,
                "__name__",
                "anonymous_handler"
            )

    @property
    def average_duration(self) -> float:
        """
        Return average execution duration.
        """

        if self.calls <= 0:
            return 0.0

        return (
            self.total_duration
            /
            self.calls
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert handler information to dictionary.
        """

        return {
            "handler_id": self.handler_id,
            "name": self.name,
            "event_name": self.event_name,
            "priority": self.priority,
            "enabled": self.enabled,
            "once": self.once,
            "calls": self.calls,
            "successes": self.successes,
            "errors": self.errors,
            "last_call": self.last_call,
            "last_success": self.last_success,
            "last_error": self.last_error,
            "total_duration": self.total_duration,
            "average_duration": self.average_duration,
            "registered_at": self.registered_at,
        }


# ============================================================
#
# EVENT BUS
#
# ============================================================

class EventBus:
    """
    Central event dispatcher.

    Stable public API.

    Example:

        event_system.subscribe(
            "market.signal",
            handler
        )

        event_system.publish(
            "market.signal",
            {
                "market": "BTC/USD",
                "signal": "bullish"
            }
        )
    """

    def __init__(
        self,
        max_history: int = 1000
    ):

        self.lock = threading.RLock()

        self.handlers: Dict[
            str,
            List[EventHandler]
        ] = defaultdict(list)

        self.history = deque(
            maxlen=max(
                1,
                int(max_history)
            )
        )

        self.max_history = max(
            1,
            int(max_history)
        )

        self.events_published = 0

        self.events_processed = 0

        self.events_with_errors = 0

        self.handler_errors = 0

        self.started_at = utc_now()

        self.last_event_at: Optional[str] = None

        self.last_event_id: Optional[str] = None

        self.enabled = True

        self._shutdown = False

        logger.info(
            "Event Bus v%s initialized.",
            EVENT_VERSION
        )

    # ========================================================
    #
    # SUBSCRIBE
    #
    # ========================================================

    def subscribe(
        self,
        event_name: str,
        callback: Callable,
        priority: int = PRIORITY_NORMAL,
        name: Optional[str] = None,
        once: bool = False
    ) -> EventHandler:
        """
        Register an event handler.
        """

        if not event_name:

            raise ValueError(
                "event_name cannot be empty"
            )

        if not callable(callback):

            raise TypeError(
                "callback must be callable"
            )

        event_name = str(
            event_name
        ).strip()

        if not event_name:

            raise ValueError(
                "event_name cannot be empty"
            )

        handler = EventHandler(
            callback=callback,
            event_name=event_name,
            priority=int(priority),
            name=name or "",
            once=bool(once)
        )

        with self.lock:

            self.handlers[
                event_name
            ].append(
                handler
            )

            self.handlers[
                event_name
            ].sort(
                key=lambda item: item.priority,
                reverse=True
            )

        logger.debug(
            "Event handler registered: %s -> %s",
            event_name,
            handler.name
        )

        return handler

    # ========================================================
    #
    # SUBSCRIBE ONCE
    #
    # ========================================================

    def subscribe_once(
        self,
        event_name: str,
        callback: Callable,
        priority: int = PRIORITY_NORMAL,
        name: Optional[str] = None
    ) -> EventHandler:
        """
        Register a handler that automatically disables itself
        after its first execution.
        """

        return self.subscribe(
            event_name=event_name,
            callback=callback,
            priority=priority,
            name=name,
            once=True
        )

    # ========================================================
    #
    # UNSUBSCRIBE
    #
    # ========================================================

    def unsubscribe(
        self,
        event_name: str,
        callback: Optional[Callable] = None,
        name: Optional[str] = None
    ) -> int:
        """
        Remove registered handlers.

        Returns number of removed handlers.
        """

        removed = 0

        with self.lock:

            handlers = self.handlers.get(
                event_name,
                []
            )

            remaining = []

            for handler in handlers:

                remove = False

                if callback is not None:

                    if handler.callback is callback:

                        remove = True

                elif name is not None:

                    if handler.name == name:

                        remove = True

                if remove:

                    removed += 1

                else:

                    remaining.append(
                        handler
                    )

            if remaining:

                self.handlers[
                    event_name
                ] = remaining

            else:

                self.handlers.pop(
                    event_name,
                    None
                )

        return removed

    # ========================================================
    #
    # UNSUBSCRIBE HANDLER
    #
    # ========================================================

    def unsubscribe_handler(
        self,
        handler: EventHandler
    ) -> bool:
        """
        Remove a specific EventHandler object.
        """

        if not isinstance(
            handler,
            EventHandler
        ):

            return False

        with self.lock:

            handlers = self.handlers.get(
                handler.event_name,
                []
            )

            for index, item in enumerate(
                handlers
            ):

                if item is handler:

                    handlers.pop(
                        index
                    )

                    if not handlers:

                        self.handlers.pop(
                            handler.event_name,
                            None
                        )

                    return True

        return False

    # ========================================================
    #
    # CLEAR
    #
    # ========================================================

    def clear(
        self,
        event_name: Optional[str] = None
    ) -> None:
        """
        Remove event handlers.
        """

        with self.lock:

            if event_name is None:

                self.handlers.clear()

            else:

                self.handlers.pop(
                    event_name,
                    None
                )

    # ========================================================
    #
    # ENABLE / DISABLE HANDLER
    #
    # ========================================================

    def set_handler_enabled(
        self,
        event_name: str,
        handler_name: str,
        enabled: bool
    ) -> bool:

        with self.lock:

            for handler in self.handlers.get(
                event_name,
                []
            ):

                if handler.name == handler_name:

                    handler.enabled = bool(
                        enabled
                    )

                    return True

        return False

    # ========================================================
    #
    # ENABLE / DISABLE BY ID
    #
    # ========================================================

    def set_handler_enabled_by_id(
        self,
        handler_id: str,
        enabled: bool
    ) -> bool:

        with self.lock:

            for handlers in self.handlers.values():

                for handler in handlers:

                    if handler.handler_id == handler_id:

                        handler.enabled = bool(
                            enabled
                        )

                        return True

        return False

    # ========================================================
    #
    # GET HANDLERS
    #
    # ========================================================

    def get_handlers(
        self,
        event_name: Optional[str] = None
    ) -> List[EventHandler]:
        """
        Return registered handlers.
        """

        with self.lock:

            if event_name is not None:

                return list(
                    self.handlers.get(
                        event_name,
                        []
                    )
                )

            result = []

            for handlers in self.handlers.values():

                result.extend(
                    handlers
                )

            return list(
                result
            )

    # ========================================================
    #
    # MATCH EVENTS
    #
    # ========================================================

    def _matching_handlers(
        self,
        event_name: str
    ) -> List[EventHandler]:

        matched = []

        with self.lock:

            # Exact event
            matched.extend(
                self.handlers.get(
                    event_name,
                    []
                )
            )

            # Global wildcard
            matched.extend(
                self.handlers.get(
                    "*",
                    []
                )
            )

            # Prefix wildcards
            parts = event_name.split(".")

            for index in range(
                1,
                len(parts)
            ):

                wildcard_name = (
                    ".".join(
                        parts[:index]
                    )
                    + ".*"
                )

                matched.extend(
                    self.handlers.get(
                        wildcard_name,
                        []
                    )
                )

        matched = [
            handler
            for handler in matched
            if handler.enabled
        ]

        matched.sort(
            key=lambda handler: handler.priority,
            reverse=True
        )

        return matched

    # ========================================================
    #
    # NORMALIZE EVENT
    #
    # ========================================================

    def _normalize_event(
        self,
        event_or_name: Any,
        data: Any = None,
        source: str = "system",
        priority: int = PRIORITY_NORMAL,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Event:

        if isinstance(
            event_or_name,
            Event
        ):

            return event_or_name

        if event_or_name is None:

            raise ValueError(
                "event name cannot be None"
            )

        event_name = str(
            event_or_name
        ).strip()

        if not event_name:

            raise ValueError(
                "event name cannot be empty"
            )

        return Event(
            name=event_name,
            data=data,
            source=str(
                source
            ),
            priority=int(
                priority
            ),
            metadata=dict(
                metadata or {}
            )
        )

    # ========================================================
    #
    # PUBLISH
    #
    # ========================================================

    def publish(
        self,
        event_or_name: Any,
        data: Any = None,
        source: str = "system",
        priority: int = PRIORITY_NORMAL,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[EventResult]:
        """
        Publish and immediately dispatch an event.
        """

        with self.lock:

            if not self.enabled:

                return []

            if self._shutdown:

                logger.warning(
                    "Event Bus is shut down."
                )

                return []

        event = self._normalize_event(
            event_or_name,
            data=data,
            source=source,
            priority=priority,
            metadata=metadata
        )

        with self.lock:

            self.events_published += 1

            self.last_event_at = (
                event.timestamp
            )

            self.last_event_id = (
                event.event_id
            )

            self.history.append(
                event
            )

        handlers = self._matching_handlers(
            event.name
        )

        results = []

        for handler in handlers:

            result = self._execute_handler(
                handler,
                event
            )

            results.append(
                result
            )

        with self.lock:

            self.events_processed += 1

            if any(
                not result.success
                for result in results
            ):

                self.events_with_errors += 1

        return results

    # ========================================================
    #
    # EMIT
    #
    # ========================================================

    def emit(
        self,
        *args,
        **kwargs
    ):

        return self.publish(
            *args,
            **kwargs
        )

    # ========================================================
    #
    # DISPATCH
    #
    # ========================================================

    def dispatch(
        self,
        *args,
        **kwargs
    ):

        return self.publish(
            *args,
            **kwargs
        )

    # ========================================================
    #
    # EXECUTE HANDLER
    #
    # ========================================================

    def _execute_handler(
        self,
        handler: EventHandler,
        event: Event
    ) -> EventResult:

        start = time.perf_counter()

        with self.lock:

            handler.calls += 1

            handler.last_call = utc_now()

        try:

            callback = handler.callback

            accepts_argument = True

            try:

                signature = inspect.signature(
                    callback
                )

                parameters = list(
                    signature.parameters.values()
                )

                positional_parameters = [
                    parameter
                    for parameter in parameters
                    if parameter.kind
                    in (
                        parameter.POSITIONAL_ONLY,
                        parameter.POSITIONAL_OR_KEYWORD
                    )
                ]

                accepts_argument = (
                    len(
                        positional_parameters
                    ) > 0
                )

            except (
                TypeError,
                ValueError
            ):

                accepts_argument = True

            if accepts_argument:

                result = callback(
                    event
                )

            else:

                result = callback()

            duration = (
                time.perf_counter()
                - start
            )

            with self.lock:

                handler.successes += 1

                handler.last_success = utc_now()

                handler.total_duration += (
                    duration
                )

                if handler.once:

                    handler.enabled = False

            return EventResult(
                handler=handler.name,
                success=True,
                result=result,
                duration=duration
            )

        except Exception as exc:

            duration = (
                time.perf_counter()
                - start
            )

            with self.lock:

                handler.errors += 1

                handler.last_error = str(
                    exc
                )

                handler.total_duration += (
                    duration
                )

                self.handler_errors += 1

                if handler.once:

                    handler.enabled = False

            logger.exception(
                "Event handler failed: "
                "%s | %s",
                event.name,
                handler.name
            )

            return EventResult(
                handler=handler.name,
                success=False,
                result=None,
                error=str(exc),
                duration=duration
            )

    # ========================================================
    #
    # ASYNC PUBLISH
    #
    # ========================================================

    def publish_async(
        self,
        event_or_name: Any,
        data: Any = None,
        source: str = "system",
        priority: int = PRIORITY_NORMAL,
        metadata: Optional[Dict[str, Any]] = None
    ) -> threading.Thread:
        """
        Publish event asynchronously.

        Returns the worker thread.
        """

        thread = threading.Thread(
            target=self.publish,
            args=(event_or_name,),
            kwargs={
                "data": data,
                "source": source,
                "priority": priority,
                "metadata": metadata
            },
            daemon=True,
            name="InksideEventWorker"
        )

        thread.start()

        return thread

    # ========================================================
    #
    # WAIT FOR ASYNC THREAD
    #
    # ========================================================

    def wait(
        self,
        thread: Optional[threading.Thread],
        timeout: Optional[float] = None
    ) -> bool:
        """
        Wait for an asynchronous event worker.
        """

        if thread is None:

            return False

        if not isinstance(
            thread,
            threading.Thread
        ):

            return False

        thread.join(
            timeout=timeout
        )

        return not thread.is_alive()

    # ========================================================
    #
    # RECENT EVENTS
    #
    # ========================================================

    def recent(
        self,
        limit: int = 50
    ) -> List[Event]:
        """
        Return most recent events.
        """

        try:

            limit = int(
                limit
            )

        except (
            TypeError,
            ValueError
        ):

            limit = 50

        limit = max(
            0,
            limit
        )

        if limit == 0:

            return []

        with self.lock:

            events = list(
                self.history
            )

        return events[-limit:]

    # ========================================================
    #
    # SEARCH HISTORY
    #
    # ========================================================

    def search(
        self,
        keyword: Optional[str] = None,
        event_name: Optional[str] = None,
        source: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Event]:
        """
        Search event history.
        """

        keyword_text = (
            str(keyword).lower()
            if keyword is not None
            else None
        )

        event_text = (
            str(event_name).lower()
            if event_name is not None
            else None
        )

        source_text = (
            str(source).lower()
            if source is not None
            else None
        )

        with self.lock:

            events = list(
                self.history
            )

        results = []

        for event in reversed(events):

            if (
                event_text is not None
                and
                event.name.lower()
                != event_text
            ):

                continue

            if (
                source_text is not None
                and
                event.source.lower()
                != source_text
            ):

                continue

            if keyword_text is not None:

                searchable = (
                    f"{event.name} "
                    f"{event.source} "
                    f"{event.data} "
                    f"{event.metadata}"
                ).lower()

                if keyword_text not in searchable:

                    continue

            results.append(
                event
            )

            if (
                limit is not None
                and
                len(results)
                >= max(
                    0,
                    int(limit)
                )
            ):

                break

        return results

    # ========================================================
    #
    # EVENT COUNT
    #
    # ========================================================

    def count(
        self,
        event_name: Optional[str] = None
    ) -> int:

        with self.lock:

            if event_name is None:

                return len(
                    self.history
                )

            return sum(
                1
                for event in self.history
                if event.name == event_name
            )

    # ========================================================
    #
    # CLEAR HISTORY
    #
    # ========================================================

    def clear_history(self) -> bool:
        """
        Clear event history without removing handlers.
        """

        with self.lock:

            self.history.clear()

        return True

    # ========================================================
    #
    # HANDLER STATUS
    #
    # ========================================================

    def handler_status(
        self
    ) -> List[Dict[str, Any]]:
        """
        Return detailed handler metrics.
        """

        with self.lock:

            return [
                handler.to_dict()
                for handlers
                in self.handlers.values()
                for handler in handlers
            ]

    # ========================================================
    #
    # EVENT TYPES
    #
    # ========================================================

    def event_types(
        self
    ) -> Dict[str, int]:
        """
        Return event counts grouped by event name.
        """

        result: Dict[str, int] = {}

        with self.lock:

            for event in self.history:

                result[event.name] = (
                    result.get(
                        event.name,
                        0
                    )
                    + 1
                )

        return result

    # ========================================================
    #
    # SOURCES
    #
    # ========================================================

    def event_sources(
        self
    ) -> Dict[str, int]:
        """
        Return event counts grouped by source.
        """

        result: Dict[str, int] = {}

        with self.lock:

            for event in self.history:

                result[event.source] = (
                    result.get(
                        event.source,
                        0
                    )
                    + 1
                )

        return result

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            total_handlers = sum(
                len(items)
                for items
                in self.handlers.values()
            )

            enabled_handlers = sum(
                1
                for items
                in self.handlers.values()
                for handler in items
                if handler.enabled
            )

            disabled_handlers = (
                total_handlers
                - enabled_handlers
            )

            return {
                "status": (
                    "ONLINE"
                    if self.enabled
                    and not self._shutdown
                    else "DISABLED"
                ),
                "version": EVENT_VERSION,
                "api_version": API_VERSION,
                "events_published":
                    self.events_published,
                "events_processed":
                    self.events_processed,
                "events_with_errors":
                    self.events_with_errors,
                "handler_errors":
                    self.handler_errors,
                "handlers":
                    total_handlers,
                "handlers_enabled":
                    enabled_handlers,
                "handlers_disabled":
                    disabled_handlers,
                "event_types":
                    len(
                        self.event_types()
                    ),
                "history":
                    len(
                        self.history
                    ),
                "max_history":
                    self.max_history,
                "started_at":
                    self.started_at,
                "last_event_at":
                    self.last_event_at,
                "last_event_id":
                    self.last_event_id,
                "shutdown":
                    self._shutdown,
            }

    # ========================================================
    #
    # ENABLE
    #
    # ========================================================

    def enable(
        self
    ) -> bool:

        with self.lock:

            if self._shutdown:

                logger.warning(
                    "Cannot enable a shut down Event Bus."
                )

                return False

            self.enabled = True

        logger.info(
            "Event Bus enabled."
        )

        return True

    # ========================================================
    #
    # DISABLE
    #
    # ========================================================

    def disable(
        self
    ) -> bool:

        with self.lock:

            self.enabled = False

        logger.info(
            "Event Bus disabled."
        )

        return True

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self,
        clear_handlers: bool = False
    ) -> bool:
        """
        Reset metrics and history.

        By default handlers remain registered.
        """

        with self.lock:

            self.history.clear()

            self.events_published = 0

            self.events_processed = 0

            self.events_with_errors = 0

            self.handler_errors = 0

            self.last_event_at = None

            self.last_event_id = None

            if clear_handlers:

                self.handlers.clear()

            self.enabled = True

            self._shutdown = False

        logger.info(
            "Event Bus reset."
        )

        return True

    # ========================================================
    #
    # SHUTDOWN
    #
    # ========================================================

    def shutdown(
        self,
        clear_handlers: bool = False
    ) -> bool:
        """
        Permanently disable the current bus instance until
        reset() is called.
        """

        with self.lock:

            self.enabled = False

            self._shutdown = True

            if clear_handlers:

                self.handlers.clear()

        logger.info(
            "Event Bus shutdown."
        )

        return True


# ============================================================
#
# GLOBAL EVENT BUS
#
# ============================================================

event_system = EventBus()


# ============================================================
#
# COMPATIBILITY API - MENGGUNAKAN event_system
# ============================================================

def subscribe(
    event_name: str,
    callback: Callable,
    priority: int = PRIORITY_NORMAL,
    name: Optional[str] = None,
    once: bool = False
) -> EventHandler:

    return event_system.subscribe(
        event_name,
        callback,
        priority,
        name,
        once
    )


def unsubscribe(
    event_name: str,
    callback: Optional[Callable] = None,
    name: Optional[str] = None
) -> int:

    return event_system.unsubscribe(
        event_name,
        callback,
        name
    )


def publish(
    event_or_name: Any,
    data: Any = None,
    source: str = "system",
    priority: int = PRIORITY_NORMAL,
    metadata: Optional[Dict[str, Any]] = None
) -> List[EventResult]:

    return event_system.publish(
        event_or_name,
        data=data,
        source=source,
        priority=priority,
        metadata=metadata
    )


def emit(
    *args,
    **kwargs
):

    return event_system.publish(
        *args,
        **kwargs
    )


def dispatch(
    *args,
    **kwargs
):

    return event_system.publish(
        *args,
        **kwargs
    )


def publish_async(
    event_or_name: Any,
    data: Any = None,
    source: str = "system",
    priority: int = PRIORITY_NORMAL,
    metadata: Optional[Dict[str, Any]] = None
):

    return event_system.publish_async(
        event_or_name,
        data=data,
        source=source,
        priority=priority,
        metadata=metadata
    )


def status() -> Dict[str, Any]:

    return event_system.status()


# ============================================================
#
# STANDARD INKSIDE EVENT NAMES
#
# ============================================================

# ENGINE
EVENT_ENGINE_STARTED = "engine.started"
EVENT_ENGINE_STOPPED = "engine.stopped"
EVENT_ENGINE_ERROR = "engine.error"

# LEARNING
EVENT_LEARNING_STARTED = "learning.started"
EVENT_LEARNING_COMPLETED = "learning.completed"
EVENT_LEARNING_ERROR = "learning.error"

# MARKET
EVENT_MARKET_UPDATE = "market.update"
EVENT_MARKET_SIGNAL = "market.signal"
EVENT_MARKET_ANALYSIS = "market.analysis"

# INTELLIGENCE
EVENT_PATTERN_DETECTED = "pattern.detected"
EVENT_DECISION_CREATED = "decision.created"
EVENT_PREDICTION_CREATED = "prediction.created"
EVENT_STRATEGY_CREATED = "strategy.created"

# KNOWLEDGE / MEMORY
EVENT_KNOWLEDGE_UPDATED = "knowledge.updated"
EVENT_MEMORY_UPDATED = "memory.updated"

# SYSTEM HEALTH
EVENT_HEALTH_CHANGED = "health.changed"
EVENT_DIAGNOSTIC_WARNING = "diagnostic.warning"

# SYSTEM
EVENT_SYSTEM_WARNING = "system.warning"
EVENT_SYSTEM_ERROR = "system.error"
EVENT_SYSTEM_SHUTDOWN = "system.shutdown"


# ============================================================
#
# ADDITIONAL STANDARD EVENTS
#
# ============================================================

# DATA
EVENT_DATA_COLLECTED = "data.collected"
EVENT_DATA_CLEANED = "data.cleaned"
EVENT_DATA_NORMALIZED = "data.normalized"
EVENT_FEATURES_EXTRACTED = "features.extracted"

# ENTITY / SEMANTIC
EVENT_ENTITY_DETECTED = "entity.detected"
EVENT_SEMANTIC_PROCESSED = "semantic.processed"

# EXPERIENCE
EVENT_EXPERIENCE_RECORDED = "experience.recorded"

# INSIGHT
EVENT_INSIGHT_CREATED = "insight.created"

# REFLECTION
EVENT_REFLECTION_CREATED = "reflection.created"
EVENT_LESSON_CREATED = "lesson.created"

# ADAPTIVE LEARNING
EVENT_ADAPTATION_UPDATED = "adaptation.updated"

# SIMULATION
EVENT_SIMULATION_STARTED = "simulation.started"
EVENT_SIMULATION_COMPLETED = "simulation.completed"
EVENT_SIMULATION_ERROR = "simulation.error"

# ARCHIVE
EVENT_ARCHIVE_CREATED = "archive.created"
EVENT_ARCHIVE_LOADED = "archive.loaded"

# CONTEXT
EVENT_CONTEXT_UPDATED = "context.updated"
EVENT_CONTEXT_RESET = "context.reset"


# ============================================================
#
# SELF TEST
#
# ============================================================

def test_event_system() -> Dict[str, Any]:
    """
    Internal event system validation.
    """

    received = []

    def handler(event):

        received.append(
            event.name
        )

        return {
            "received": True,
            "event_id": event.event_id
        }

    test_bus = EventBus(
        max_history=100
    )

    test_bus.subscribe(
        "test.event",
        handler,
        priority=PRIORITY_HIGH
    )

    results = test_bus.publish(
        "test.event",
        {
            "value": 123
        },
        source="self_test"
    )

    status_data = test_bus.status()

    success = (
        len(results) == 1
        and results[0].success
        and received == ["test.event"]
        and status_data[
            "events_published"
        ] == 1
        and status_data[
            "events_processed"
        ] == 1
        and status_data[
            "handler_errors"
        ] == 0
        and test_bus.count(
            "test.event"
        ) == 1
    )

    return {
        "status": (
            "PASS"
            if success
            else "FAIL"
        ),
        "event_version":
            EVENT_VERSION,
        "api_version":
            API_VERSION,
        "events":
            received,
        "results":
            [
                result.to_dict()
                for result in results
            ],
        "bus_status":
            status_data
    }


# ============================================================
#
# ADVANCED SELF TEST
#
# ============================================================

def test_event_system_advanced() -> Dict[str, Any]:
    """
    Extended validation for:
    - wildcard events
    - priority
    - once handlers
    - handler failure isolation
    - async publishing
    - event history
    """

    calls = []

    test_bus = EventBus(
        max_history=50
    )

    def high_priority(event):

        calls.append(
            "high"
        )

        return "high_ok"

    def wildcard_handler(event):

        calls.append(
            "wildcard"
        )

        return "wildcard_ok"

    def once_handler(event):

        calls.append(
            "once"
        )

        return "once_ok"

    def failing_handler(event):

        calls.append(
            "failing"
        )

        raise RuntimeError(
            "intentional test error"
        )

    test_bus.subscribe(
        "market.signal",
        high_priority,
        priority=PRIORITY_HIGH,
        name="high_priority"
    )

    test_bus.subscribe(
        "market.*",
        wildcard_handler,
        priority=PRIORITY_NORMAL,
        name="market_wildcard"
    )

    test_bus.subscribe_once(
        "market.signal",
        once_handler,
        priority=PRIORITY_LOW,
        name="once_handler"
    )

    test_bus.subscribe(
        "market.signal",
        failing_handler,
        priority=PRIORITY_LOW,
        name="failing_handler"
    )

    results_1 = test_bus.publish(
        "market.signal",
        {
            "symbol": "BTC/USD"
        },
        source="advanced_test"
    )

    results_2 = test_bus.publish(
        "market.signal",
        {
            "symbol": "ETH/USD"
        },
        source="advanced_test"
    )

    async_thread = test_bus.publish_async(
        "market.update",
        {
            "symbol": "SOL/USD"
        },
        source="async_test"
    )

    async_completed = test_bus.wait(
        async_thread,
        timeout=5.0
    )

    status_data = test_bus.status()

    once_count = calls.count(
        "once"
    )

    failure_detected = any(
        not result.success
        for result in results_1
    )

    success = (
        len(results_1) == 4
        and len(results_2) == 3
        and async_completed
        and once_count == 1
        and failure_detected
        and test_bus.count(
            "market.signal"
        ) == 2
        and test_bus.count(
            "market.update"
        ) == 1
        and status_data[
            "handler_errors"
        ] == 2
    )

    return {
        "status": (
            "PASS"
            if success
            else "FAIL"
        ),
        "calls": calls,
        "results_first_publish": [
            result.to_dict()
            for result in results_1
        ],
        "results_second_publish": [
            result.to_dict()
            for result in results_2
        ],
        "async_completed":
            async_completed,
        "bus_status":
            status_data
    }


# ============================================================
#
# PUBLIC API
# ============================================================

__all__ = [
    # Version
    "EVENT_VERSION",
    "API_VERSION",
    
    # Priority
    "PRIORITY_LOW",
    "PRIORITY_NORMAL",
    "PRIORITY_HIGH",
    "PRIORITY_CRITICAL",
    
    # Core
    "EventBus",
    "Event",
    "EventHandler",
    "EventResult",
    
    # Global instance
    "event_system",
    
    # Compatibility functions
    "subscribe",
    "unsubscribe",
    "publish",
    "emit",
    "dispatch",
    "publish_async",
    "status",
    
    # Standard event names
    "EVENT_ENGINE_STARTED",
    "EVENT_ENGINE_STOPPED",
    "EVENT_ENGINE_ERROR",
    "EVENT_LEARNING_STARTED",
    "EVENT_LEARNING_COMPLETED",
    "EVENT_LEARNING_ERROR",
    "EVENT_MARKET_UPDATE",
    "EVENT_MARKET_SIGNAL",
    "EVENT_MARKET_ANALYSIS",
    "EVENT_PATTERN_DETECTED",
    "EVENT_DECISION_CREATED",
    "EVENT_PREDICTION_CREATED",
    "EVENT_STRATEGY_CREATED",
    "EVENT_KNOWLEDGE_UPDATED",
    "EVENT_MEMORY_UPDATED",
    "EVENT_HEALTH_CHANGED",
    "EVENT_DIAGNOSTIC_WARNING",
    "EVENT_SYSTEM_WARNING",
    "EVENT_SYSTEM_ERROR",
    "EVENT_SYSTEM_SHUTDOWN",
    "EVENT_DATA_COLLECTED",
    "EVENT_DATA_CLEANED",
    "EVENT_DATA_NORMALIZED",
    "EVENT_FEATURES_EXTRACTED",
    "EVENT_ENTITY_DETECTED",
    "EVENT_SEMANTIC_PROCESSED",
    "EVENT_EXPERIENCE_RECORDED",
    "EVENT_INSIGHT_CREATED",
    "EVENT_REFLECTION_CREATED",
    "EVENT_LESSON_CREATED",
    "EVENT_ADAPTATION_UPDATED",
    "EVENT_SIMULATION_STARTED",
    "EVENT_SIMULATION_COMPLETED",
    "EVENT_SIMULATION_ERROR",
    "EVENT_ARCHIVE_CREATED",
    "EVENT_ARCHIVE_LOADED",
    "EVENT_CONTEXT_UPDATED",
    "EVENT_CONTEXT_RESET",
    
    # Tests
    "test_event_system",
    "test_event_system_advanced",
]


# ============================================================
# END
# ============================================================