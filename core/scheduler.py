# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SCHEDULER SYSTEM
# FOUNDATION v3.0
#
# Compatible Engine API: v1.0
#
# ============================================================
#
# PURPOSE
# ------------------------------------------------------------
# Central task scheduling system for the Intelligence OS.
#
# Design goals:
# - Stable API
# - Thread safe
# - Engine independent
# - Background task execution
# - One-time tasks
# - Repeating tasks
# - Delayed tasks
# - Runtime add/remove
# - Task enable / disable
# - Priority support
# - Retry support
# - Failure isolation
# - Execution statistics
# - Graceful shutdown
# - Future plugin compatibility
#
# IMPORTANT
# ------------------------------------------------------------
# Engine.py should NOT contain scheduling logic.
#
# Future modules can create scheduled jobs through this layer
# without modifying engine.py.
#
# ============================================================

from __future__ import annotations

import logging
import threading
import time
import uuid

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

SCHEDULER_VERSION = "3.0"

API_VERSION = "1.0"


# ============================================================
#
# TASK STATES
#
# ============================================================

TASK_PENDING = "pending"
TASK_RUNNING = "running"
TASK_COMPLETED = "completed"
TASK_FAILED = "failed"
TASK_CANCELLED = "cancelled"
TASK_DISABLED = "disabled"


# ============================================================
#
# TASK TYPES
#
# ============================================================

TASK_ONCE = "once"
TASK_INTERVAL = "interval"
TASK_DELAY = "delay"


# ============================================================
#
# PRIORITY
#
# ============================================================

PRIORITY_LOW = 10
PRIORITY_NORMAL = 50
PRIORITY_HIGH = 75
PRIORITY_CRITICAL = 100


# ============================================================
#
# SCHEDULED TASK
#
# ============================================================

@dataclass
class ScheduledTask:
    """
    Metadata and runtime state for a scheduled task.
    """

    task_id: str

    name: str

    callback: Callable

    task_type: str = TASK_ONCE

    interval: float = 0.0

    delay: float = 0.0

    priority: int = PRIORITY_NORMAL

    enabled: bool = True

    state: str = TASK_PENDING

    max_retries: int = 0

    retry_count: int = 0

    executions: int = 0

    failures: int = 0

    created_at: str = field(
        default_factory=lambda:
            datetime.now().isoformat()
    )

    next_run: Optional[float] = None

    last_run: Optional[str] = None

    last_success: Optional[str] = None

    last_error: Optional[str] = None

    last_duration: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    thread: Optional[threading.Thread] = None

    cancel_event: threading.Event = field(
        default_factory=threading.Event
    )

    def to_dict(self) -> Dict[str, Any]:
        """
        Return serializable task information.
        """

        return {
            "task_id": self.task_id,
            "name": self.name,
            "task_type": self.task_type,
            "interval": self.interval,
            "delay": self.delay,
            "priority": self.priority,
            "enabled": self.enabled,
            "state": self.state,
            "max_retries": self.max_retries,
            "retry_count": self.retry_count,
            "executions": self.executions,
            "failures": self.failures,
            "created_at": self.created_at,
            "next_run": self.next_run,
            "last_run": self.last_run,
            "last_success": self.last_success,
            "last_error": self.last_error,
            "last_duration": self.last_duration,
            "metadata": dict(self.metadata),
        }


# ============================================================
#
# SCHEDULER
#
# ============================================================

class Scheduler:
    """
    Central background scheduler.

    The scheduler owns timing and task lifecycle.
    """

    def __init__(
        self,
        max_workers: int = 10
    ):

        self.lock = threading.RLock()

        self.tasks: Dict[
            str,
            ScheduledTask
        ] = {}

        self.max_workers = max(
            1,
            int(max_workers)
        )

        self.active_workers = 0

        self.enabled = True

        self.running = False

        self.started_at: Optional[str] = None

        self.stopped_at: Optional[str] = None

        self.total_executions = 0

        self.total_failures = 0

        self.total_tasks_created = 0

        self.total_tasks_cancelled = 0

        self._stop_event = threading.Event()

        self._scheduler_thread: Optional[
            threading.Thread
        ] = None

        logger.info(
            "Scheduler v%s initialized.",
            SCHEDULER_VERSION
        )


    # ========================================================
    #
    # START
    #
    # ========================================================

    def start(self) -> bool:
        """
        Start scheduler loop.
        """

        with self.lock:

            if self.running:

                return True

            self.enabled = True

            self.running = True

            self.started_at = (
                datetime.now().isoformat()
            )

            self.stopped_at = None

            self._stop_event.clear()

            self._scheduler_thread = (
                threading.Thread(
                    target=self._run_loop,
                    name="InksideScheduler",
                    daemon=True
                )
            )

            self._scheduler_thread.start()

        logger.info(
            "Scheduler started."
        )

        return True


    # ========================================================
    #
    # STOP
    #
    # ========================================================

    def stop(
        self,
        wait: bool = True
    ) -> bool:
        """
        Gracefully stop scheduler.
        """

        with self.lock:

            if not self.running:

                return True

            self.running = False

            self.enabled = False

            self._stop_event.set()

            for task in self.tasks.values():

                task.cancel_event.set()

                if task.state == TASK_RUNNING:

                    task.state = TASK_CANCELLED

            thread = self._scheduler_thread

            self.stopped_at = (
                datetime.now().isoformat()
            )

        if (
            wait
            and thread is not None
            and thread.is_alive()
        ):

            thread.join(
                timeout=5.0
            )

        logger.info(
            "Scheduler stopped."
        )

        return True


    # ========================================================
    #
    # ADD ONCE
    #
    # ========================================================

    def add_once(
        self,
        callback: Callable,
        *,
        name: Optional[str] = None,
        delay: float = 0.0,
        priority: int = PRIORITY_NORMAL,
        max_retries: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Schedule a task that runs once.
        """

        return self._add_task(
            callback=callback,
            task_type=TASK_ONCE,
            name=name,
            delay=delay,
            priority=priority,
            max_retries=max_retries,
            metadata=metadata
        )


    # ========================================================
    #
    # ADD DELAY
    #
    # ========================================================

    def add_delay(
        self,
        callback: Callable,
        delay: float,
        *,
        name: Optional[str] = None,
        priority: int = PRIORITY_NORMAL,
        max_retries: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Schedule a delayed task.
        """

        return self._add_task(
            callback=callback,
            task_type=TASK_DELAY,
            name=name,
            delay=delay,
            priority=priority,
            max_retries=max_retries,
            metadata=metadata
        )


    # ========================================================
    #
    # ADD INTERVAL
    #
    # ========================================================

    def add_interval(
        self,
        callback: Callable,
        interval: float,
        *,
        name: Optional[str] = None,
        delay: Optional[float] = None,
        priority: int = PRIORITY_NORMAL,
        max_retries: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Schedule a repeating task.
        """

        interval = max(
            0.01,
            float(interval)
        )

        if delay is None:

            delay = interval

        return self._add_task(
            callback=callback,
            task_type=TASK_INTERVAL,
            name=name,
            interval=interval,
            delay=delay,
            priority=priority,
            max_retries=max_retries,
            metadata=metadata
        )


    # ========================================================
    #
    # INTERNAL ADD
    #
    # ========================================================

    def _add_task(
        self,
        callback: Callable,
        task_type: str,
        name: Optional[str],
        interval: float = 0.0,
        delay: float = 0.0,
        priority: int = PRIORITY_NORMAL,
        max_retries: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:

        if not callable(callback):

            raise TypeError(
                "callback must be callable."
            )

        task_id = uuid.uuid4().hex

        task_name = (
            name
            or getattr(
                callback,
                "__name__",
                "anonymous_task"
            )
        )

        now = time.time()

        task = ScheduledTask(

            task_id=task_id,

            name=str(
                task_name
            ),

            callback=callback,

            task_type=task_type,

            interval=max(
                0.0,
                float(interval)
            ),

            delay=max(
                0.0,
                float(delay)
            ),

            priority=int(
                priority
            ),

            max_retries=max(
                0,
                int(max_retries)
            ),

            metadata=dict(
                metadata or {}
            ),

            next_run=(
                now
                + max(
                    0.0,
                    float(delay)
                )
            )
        )

        with self.lock:

            self.tasks[
                task_id
            ] = task

            self.total_tasks_created += 1

        logger.debug(
            "Task added: %s [%s]",
            task.name,
            task_id
        )

        if not self.running:

            self.start()

        return task_id


    # ========================================================
    #
    # REMOVE TASK
    #
    # ========================================================

    def remove(
        self,
        task_id: str
    ) -> bool:
        """
        Cancel and remove a task.
        """

        with self.lock:

            task = self.tasks.get(
                task_id
            )

            if task is None:

                return False

            task.enabled = False

            task.state = TASK_CANCELLED

            task.cancel_event.set()

            del self.tasks[
                task_id
            ]

            self.total_tasks_cancelled += 1

        logger.debug(
            "Task removed: %s",
            task_id
        )

        return True


    # ========================================================
    #
    # CANCEL
    #
    # ========================================================

    def cancel(
        self,
        task_id: str
    ) -> bool:

        with self.lock:

            task = self.tasks.get(
                task_id
            )

            if task is None:

                return False

            task.enabled = False

            task.state = TASK_CANCELLED

            task.cancel_event.set()

            self.total_tasks_cancelled += 1

        return True


    # ========================================================
    #
    # ENABLE TASK
    #
    # ========================================================

    def enable_task(
        self,
        task_id: str
    ) -> bool:

        with self.lock:

            task = self.tasks.get(
                task_id
            )

            if task is None:

                return False

            task.enabled = True

            if task.state in (
                TASK_DISABLED,
                TASK_CANCELLED
            ):

                task.state = TASK_PENDING

            task.cancel_event.clear()

            return True


    # ========================================================
    #
    # DISABLE TASK
    #
    # ========================================================

    def disable_task(
        self,
        task_id: str
    ) -> bool:

        with self.lock:

            task = self.tasks.get(
                task_id
            )

            if task is None:

                return False

            task.enabled = False

            task.state = TASK_DISABLED

            task.cancel_event.set()

            return True


    # ========================================================
    #
    # GET TASK
    #
    # ========================================================

    def get(
        self,
        task_id: str
    ) -> Optional[ScheduledTask]:

        with self.lock:

            return self.tasks.get(
                task_id
            )


    # ========================================================
    #
    # LIST TASKS
    #
    # ========================================================

    def list_tasks(
        self,
        enabled_only: bool = False
    ) -> List[ScheduledTask]:

        with self.lock:

            tasks = list(
                self.tasks.values()
            )

            if enabled_only:

                tasks = [
                    task
                    for task in tasks
                    if task.enabled
                ]

            return tasks


    # ========================================================
    #
    # FIND BY NAME
    #
    # ========================================================

    def find(
        self,
        name: str
    ) -> List[ScheduledTask]:

        with self.lock:

            return [
                task
                for task
                in self.tasks.values()
                if task.name == name
            ]


    # ========================================================
    #
    # SCHEDULER LOOP
    #
    # ========================================================

    def _run_loop(self):

        while not self._stop_event.is_set():

            if not self.enabled:

                time.sleep(
                    0.1
                )

                continue

            now = time.time()

            due_tasks = []

            with self.lock:

                for task in self.tasks.values():

                    if not task.enabled:

                        continue

                    if task.state == TASK_RUNNING:

                        continue

                    if (
                        task.next_run is not None
                        and now >= task.next_run
                    ):

                        due_tasks.append(
                            task
                        )

                due_tasks.sort(
                    key=lambda item:
                    item.priority,
                    reverse=True
                )

            for task in due_tasks:

                if (
                    self.active_workers
                    >= self.max_workers
                ):

                    break

                self._dispatch(
                    task
                )

            time.sleep(
                0.05
            )


    # ========================================================
    #
    # DISPATCH
    #
    # ========================================================

    def _dispatch(
        self,
        task: ScheduledTask
    ) -> None:

        with self.lock:

            if not task.enabled:

                return

            if task.state == TASK_RUNNING:

                return

            task.state = TASK_RUNNING

            self.active_workers += 1

        thread = threading.Thread(

            target=self._execute_task,

            args=(task,),

            name=(
                f"InksideTask-{task.name}"
            ),

            daemon=True

        )

        task.thread = thread

        thread.start()


    # ========================================================
    #
    # EXECUTE
    #
    # ========================================================

    def _execute_task(
        self,
        task: ScheduledTask
    ) -> None:

        start = time.time()

        success = False

        error = None

        try:

            if task.cancel_event.is_set():

                task.state = TASK_CANCELLED

                return

            task.last_run = (
                datetime.now().isoformat()
            )

            task.callback()

            success = True

            task.executions += 1

            task.last_success = (
                datetime.now().isoformat()
            )

            task.retry_count = 0

        except Exception as exc:

            error = str(
                exc
            )

            task.failures += 1

            task.retry_count += 1

            self.total_failures += 1

            task.last_error = error

            logger.exception(
                "Scheduled task failed: %s",
                task.name
            )

        finally:

            duration = (
                time.time() - start
            )

            task.last_duration = duration

            self.total_executions += 1

            with self.lock:

                self.active_workers = max(
                    0,
                    self.active_workers - 1
                )

                if not success:

                    if (
                        task.retry_count
                        <= task.max_retries
                        and task.enabled
                    ):

                        task.state = (
                            TASK_PENDING
                        )

                        task.next_run = (
                            time.time()
                            + min(
                                60.0,
                                max(
                                    1.0,
                                    2 ** (
                                        task.retry_count - 1
                                    )
                                )
                            )
                        )

                    elif (
                        task.task_type
                        == TASK_INTERVAL
                        and task.enabled
                    ):

                        task.state = (
                            TASK_PENDING
                        )

                        task.next_run = (
                            time.time()
                            + task.interval
                        )

                    else:

                        task.state = (
                            TASK_FAILED
                        )

                else:

                    if (
                        task.task_type
                        == TASK_INTERVAL
                        and task.enabled
                        and not task.cancel_event.is_set()
                    ):

                        task.state = (
                            TASK_PENDING
                        )

                        task.next_run = (
                            time.time()
                            + task.interval
                        )

                    else:

                        task.state = (
                            TASK_COMPLETED
                        )

                        task.enabled = False

        if error:

            logger.debug(
                "Task error: %s | %s",
                task.name,
                error
            )


    # ========================================================
    #
    # RUN NOW
    #
    # ========================================================

    def run_now(
        self,
        task_id: str
    ) -> bool:
        """
        Execute a registered task immediately.
        """

        task = self.get(
            task_id
        )

        if task is None:

            return False

        if not task.enabled:

            return False

        self._dispatch(
            task
        )

        return True


    # ========================================================
    #
    # WAIT
    #
    # ========================================================

    def wait(
        self,
        task_id: str,
        timeout: Optional[float] = None
    ) -> bool:
        """
        Wait for a task's current worker to finish.
        """

        task = self.get(
            task_id
        )

        if task is None:

            return False

        thread = task.thread

        if (
            thread is not None
            and thread.is_alive()
        ):

            thread.join(
                timeout=timeout
            )

        return True


    # ========================================================
    #
    # CLEAR COMPLETED
    #
    # ========================================================

    def clear_completed(self) -> int:

        removed = 0

        with self.lock:

            task_ids = [

                task_id

                for task_id, task

                in self.tasks.items()

                if task.state
                in (
                    TASK_COMPLETED,
                    TASK_CANCELLED,
                    TASK_FAILED
                )
            ]

            for task_id in task_ids:

                del self.tasks[
                    task_id
                ]

                removed += 1

        return removed


    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            tasks = list(
                self.tasks.values()
            )

            return {

                "status":
                    "ONLINE"
                    if (
                        self.enabled
                        and self.running
                    )
                    else
                    "OFFLINE",

                "version":
                    SCHEDULER_VERSION,

                "api_version":
                    API_VERSION,

                "running":
                    self.running,

                "enabled":
                    self.enabled,

                "tasks":
                    len(tasks),

                "active_tasks":
                    sum(
                        1
                        for task
                        in tasks
                        if task.state
                        == TASK_RUNNING
                    ),

                "pending_tasks":
                    sum(
                        1
                        for task
                        in tasks
                        if task.state
                        == TASK_PENDING
                    ),

                "completed_tasks":
                    sum(
                        1
                        for task
                        in tasks
                        if task.state
                        == TASK_COMPLETED
                    ),

                "failed_tasks":
                    sum(
                        1
                        for task
                        in tasks
                        if task.state
                        == TASK_FAILED
                    ),

                "active_workers":
                    self.active_workers,

                "max_workers":
                    self.max_workers,

                "total_executions":
                    self.total_executions,

                "total_failures":
                    self.total_failures,

                "total_tasks_created":
                    self.total_tasks_created,

                "total_tasks_cancelled":
                    self.total_tasks_cancelled,

                "started_at":
                    self.started_at,

                "stopped_at":
                    self.stopped_at

            }


    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self,
        remove_tasks: bool = True
    ) -> bool:

        with self.lock:

            if remove_tasks:

                for task in self.tasks.values():

                    task.cancel_event.set()

                self.tasks.clear()

            self.total_executions = 0

            self.total_failures = 0

            self.total_tasks_created = 0

            self.total_tasks_cancelled = 0

        return True


# ============================================================
#
# GLOBAL SCHEDULER
#
# ============================================================

scheduler = Scheduler()


# ============================================================
#
# COMPATIBILITY API
#
# ============================================================

def start() -> bool:

    return scheduler.start()


def stop(
    wait: bool = True
) -> bool:

    return scheduler.stop(
        wait=wait
    )


def add_once(
    callback: Callable,
    *,
    name: Optional[str] = None,
    delay: float = 0.0,
    priority: int = PRIORITY_NORMAL,
    max_retries: int = 0,
    metadata: Optional[Dict[str, Any]] = None
) -> str:

    return scheduler.add_once(
        callback,
        name=name,
        delay=delay,
        priority=priority,
        max_retries=max_retries,
        metadata=metadata
    )


def add_interval(
    callback: Callable,
    interval: float,
    *,
    name: Optional[str] = None,
    delay: Optional[float] = None,
    priority: int = PRIORITY_NORMAL,
    max_retries: int = 0,
    metadata: Optional[Dict[str, Any]] = None
) -> str:

    return scheduler.add_interval(
        callback,
        interval,
        name=name,
        delay=delay,
        priority=priority,
        max_retries=max_retries,
        metadata=metadata
    )


def add_delay(
    callback: Callable,
    delay: float,
    *,
    name: Optional[str] = None,
    priority: int = PRIORITY_NORMAL,
    max_retries: int = 0,
    metadata: Optional[Dict[str, Any]] = None
) -> str:

    return scheduler.add_delay(
        callback,
        delay,
        name=name,
        priority=priority,
        max_retries=max_retries,
        metadata=metadata
    )


def cancel(
    task_id: str
) -> bool:

    return scheduler.cancel(
        task_id
    )


def remove(
    task_id: str
) -> bool:

    return scheduler.remove(
        task_id
    )


def run_now(
    task_id: str
) -> bool:

    return scheduler.run_now(
        task_id
    )


def status() -> Dict[str, Any]:

    return scheduler.status()


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
    print("SCHEDULER TEST")
    print("=" * 60)
    print()

    counter = {
        "value": 0
    }

    def test_task():

        counter["value"] += 1

        print(
            "TASK EXECUTED:",
            counter["value"]
        )

    scheduler.start()

    task_id = scheduler.add_interval(
        test_task,
        interval=1.0,
        name="test_interval"
    )

    print(
        "TASK ID:",
        task_id
    )

    time.sleep(
        3.5
    )

    scheduler.cancel(
        task_id
    )

    print()

    print(
        "STATUS:"
    )

    print(
        scheduler.status()
    )

    scheduler.stop()

    print()
    print("=" * 60)
    print("SCHEDULER TEST COMPLETE")
    print("=" * 60)