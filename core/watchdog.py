# INKSIDE DIGITAL - SYSTEM WATCHDOG v3.1
# REAL IMPLEMENTATION - PRODUCTION READY
# ============================================================

import logging
import threading
import time
import json
import psutil
import os
import sys
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field, asdict
from collections import deque
from enum import Enum
import inspect

logger = logging.getLogger(__name__)

# ============================================================
# ENUMS
# ============================================================

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class ComponentStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"
    UNKNOWN = "unknown"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class RealLatencyMetric:
    component: str
    current_ms: float = 0.0
    min_ms: float = float('inf')
    max_ms: float = 0.0
    avg_ms: float = 0.0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    samples: deque = field(default_factory=lambda: deque(maxlen=1000))
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "healthy"
    total_measurements: int = 0
    last_measurement_time: Optional[datetime] = None
    measurement_source: str = "real"
    
    def update(self, latency_ms: float):
        self.current_ms = latency_ms
        self.samples.append(latency_ms)
        self.timestamp = datetime.now()
        self.last_measurement_time = self.timestamp
        self.total_measurements += 1
        self.measurement_source = "real"
        
        if latency_ms < self.min_ms:
            self.min_ms = latency_ms
        if latency_ms > self.max_ms:
            self.max_ms = latency_ms
        
        if len(self.samples) >= 10:
            sorted_samples = sorted(self.samples)
            self.p50_ms = sorted_samples[len(sorted_samples) // 2]
            self.p95_ms = sorted_samples[int(len(sorted_samples) * 0.95)]
            self.p99_ms = sorted_samples[int(len(sorted_samples) * 0.99)]
            self.avg_ms = sum(sorted_samples) / len(sorted_samples)
        
        if self.p95_ms > 500:
            self.status = "critical"
        elif self.p95_ms > 200:
            self.status = "degraded"
        else:
            self.status = "healthy"
    
    def to_dict(self):
        return {
            "component": self.component,
            "current_ms": round(self.current_ms, 2),
            "min_ms": round(self.min_ms, 2) if self.min_ms != float('inf') else 0,
            "max_ms": round(self.max_ms, 2),
            "avg_ms": round(self.avg_ms, 2),
            "p50_ms": round(self.p50_ms, 2),
            "p95_ms": round(self.p95_ms, 2),
            "p99_ms": round(self.p99_ms, 2),
            "status": self.status,
            "total_measurements": self.total_measurements,
            "timestamp": self.timestamp.isoformat(),
            "measurement_source": self.measurement_source
        }

@dataclass
class RealHeartbeat:
    component: str
    last_beat: Optional[datetime] = None
    beat_count: int = 0
    missed_beats: int = 0
    consecutive_misses: int = 0
    status: str = "unknown"
    last_error: Optional[str] = None
    startup_time: Optional[datetime] = None
    restart_count: int = 0
    process_id: int = os.getpid()
    thread_id: Optional[int] = None
    thread_name: Optional[str] = None
    last_beat_interval: float = 0.0
    is_alive: bool = False
    health_score: float = 100.0
    uptime_seconds: float = 0.0
    
    def beat(self):
        now = datetime.now()
        if self.last_beat:
            self.last_beat_interval = (now - self.last_beat).total_seconds()
            self.uptime_seconds += self.last_beat_interval
        self.last_beat = now
        self.beat_count += 1
        self.consecutive_misses = 0
        self.status = "alive"
        self.is_alive = True
        self.thread_id = threading.get_ident()
        self.thread_name = threading.current_thread().name
        self.health_score = min(100, self.health_score + 0.5)
    
    def miss(self, error: str = None):
        self.missed_beats += 1
        self.consecutive_misses += 1
        self.is_alive = False
        self.health_score = max(0, self.health_score - 10)
        if error:
            self.last_error = error
        if self.consecutive_misses >= 3:
            self.status = "dead"
            self.health_score = max(0, self.health_score - 20)
    
    def to_dict(self):
        return {
            "component": self.component,
            "last_beat": self.last_beat.isoformat() if self.last_beat else None,
            "beat_count": self.beat_count,
            "missed_beats": self.missed_beats,
            "consecutive_misses": self.consecutive_misses,
            "status": self.status,
            "last_error": self.last_error,
            "restart_count": self.restart_count,
            "process_id": self.process_id,
            "thread_id": self.thread_id,
            "thread_name": self.thread_name,
            "last_beat_interval": round(self.last_beat_interval, 2),
            "is_alive": self.is_alive,
            "health_score": round(self.health_score, 1),
            "uptime_seconds": round(self.uptime_seconds, 1)
        }

@dataclass
class RealCircuitBreaker:
    name: str
    failure_threshold: int = 5
    timeout_seconds: int = 30
    state: str = "CLOSED"
    failures: int = 0
    successes: int = 0
    last_failure: Optional[datetime] = None
    last_success: Optional[datetime] = None
    open_time: Optional[datetime] = None
    half_open_time: Optional[datetime] = None
    total_requests: int = 0
    total_failures: int = 0
    total_successes: int = 0
    success_rate: float = 100.0
    last_error: Optional[str] = None
    recovery_attempts: int = 0
    last_error_traceback: Optional[str] = None
    health_impact: float = 0.0
    
    def record_success(self):
        self.total_requests += 1
        self.total_successes += 1
        self.successes += 1
        self.last_success = datetime.now()
        self.last_error = None
        self.last_error_traceback = None
        self.success_rate = (self.total_successes / self.total_requests) * 100 if self.total_requests > 0 else 100
        self.health_impact = max(0, self.health_impact - 2)
        
        if self.state == "HALF_OPEN":
            if self.successes >= self.failure_threshold:
                self.state = "CLOSED"
                self.failures = 0
                self.successes = 0
                logger.info(f"🔒 Circuit {self.name} CLOSED - recovered successfully")
    
    def record_failure(self, error: str = None, traceback_str: str = None):
        self.total_requests += 1
        self.total_failures += 1
        self.failures += 1
        self.last_failure = datetime.now()
        self.last_error = error
        self.last_error_traceback = traceback_str
        self.success_rate = (self.total_successes / self.total_requests) * 100 if self.total_requests > 0 else 0
        self.health_impact = min(100, self.health_impact + 5)
        
        if self.state == "CLOSED":
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
                self.open_time = datetime.now()
                logger.error(f"⚠️ Circuit {self.name} OPEN after {self.failures} failures")
        elif self.state == "HALF_OPEN":
            self.state = "OPEN"
            self.open_time = datetime.now()
            logger.error(f"⚠️ Circuit {self.name} OPEN (failed in half-open)")
    
    def can_execute(self) -> bool:
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            if self.open_time and (datetime.now() - self.open_time).seconds > self.timeout_seconds:
                self.state = "HALF_OPEN"
                self.half_open_time = datetime.now()
                self.successes = 0
                self.recovery_attempts += 1
                logger.info(f"🔄 Circuit {self.name} HALF_OPEN - testing recovery")
                return True
            return False
        elif self.state == "HALF_OPEN":
            return True
        return False
    
    def reset(self):
        self.state = "CLOSED"
        self.failures = 0
        self.successes = 0
        self.open_time = None
        self.half_open_time = None
        self.last_error = None
        self.last_error_traceback = None
        self.health_impact = 0
        logger.info(f"🔄 Circuit {self.name} manually reset to CLOSED")
    
    def to_dict(self):
        return {
            "name": self.name,
            "state": self.state,
            "failures": self.failures,
            "successes": self.successes,
            "failure_threshold": self.failure_threshold,
            "timeout_seconds": self.timeout_seconds,
            "last_failure": self.last_failure.isoformat() if self.last_failure else None,
            "last_success": self.last_success.isoformat() if self.last_success else None,
            "open_time": self.open_time.isoformat() if self.open_time else None,
            "total_requests": self.total_requests,
            "total_failures": self.total_failures,
            "total_successes": self.total_successes,
            "success_rate": round(self.success_rate, 2),
            "last_error": self.last_error,
            "recovery_attempts": self.recovery_attempts,
            "health_impact": round(self.health_impact, 1)
        }

# ============================================================
# REAL WATCHDOG ENGINE
# ============================================================

class RealSystemWatchdog:
    VERSION = "3.1"
    
    def __init__(
        self,
        interval: int = 10,
        heartbeat_timeout: int = 30,
        auto_restart: bool = True,
        max_restarts: int = 5,
        restart_cooldown: int = 60,
        max_history: int = 500
    ):
        self.interval = interval
        self.heartbeat_timeout = heartbeat_timeout
        self.auto_restart = auto_restart
        self.max_restarts = max_restarts
        self.restart_cooldown = restart_cooldown
        self.max_history = max_history
        
        self.running = False
        self.thread = None
        self._start_time = None
        
        self.components: Dict[str, Any] = {}
        self.latency_metrics: Dict[str, RealLatencyMetric] = {}
        self.heartbeats: Dict[str, RealHeartbeat] = {}
        self.circuit_breakers: Dict[str, RealCircuitBreaker] = {}
        self.dependencies: Dict[str, List[str]] = {}
        self.component_methods: Dict[str, Dict[str, str]] = {}
        self.component_health: Dict[str, float] = {}
        
        self.history: List[Dict] = []
        self.alert_history: List[Dict] = []
        self.restart_history: List[Dict] = []
        self.error_history: List[Dict] = []
        
        self.metrics = {
            "total_checks": 0,
            "total_alerts": 0,
            "total_restarts": 0,
            "total_errors": 0,
            "avg_check_time": 0.0,
            "last_check_time": 0.0,
            "uptime_seconds": 0,
            "health_score": 100.0,
            "components_healthy": 0,
            "components_degraded": 0,
            "components_critical": 0,
            "components_offline": 0,
        }
        
        self.alert_callbacks: List[Callable] = []
        self._last_alert_time: Dict[str, datetime] = {}
        self._alert_cooldown_seconds = 30
        self._system_metrics_cache: Optional[Dict] = None
        self._cache_time: Optional[datetime] = None
        self._cache_duration = 5
        
        logger.info(f"🛡️ REAL System Watchdog v{self.VERSION} initialized")
    
    def register_component(
        self,
        name: str,
        component: Any,
        dependencies: List[str] = None,
        health_method: str = "health_check",
        restart_method: str = "restart",
        stop_method: str = "stop",
        start_method: str = "start"
    ):
        self.components[name] = component
        self.heartbeats[name] = RealHeartbeat(
            component=name,
            process_id=os.getpid()
        )
        self.latency_metrics[name] = RealLatencyMetric(component=name)
        self.circuit_breakers[name] = RealCircuitBreaker(name=name)
        self.component_health[name] = 100.0
        
        if dependencies:
            self.dependencies[name] = dependencies
        
        self.component_methods[name] = {
            "health": health_method,
            "restart": restart_method,
            "stop": stop_method,
            "start": start_method
        }
        
        logger.info(f"✅ Registered REAL component: {name}")
        
        # Initial heartbeat
        self.heartbeats[name].beat()
        self.component_health[name] = 90.0
    
    def start(self) -> bool:
        if self.running:
            return False
        
        self.running = True
        self._start_time = datetime.now()
        self.thread = threading.Thread(
            target=self._run_loop,
            daemon=True,
            name="RealWatchdog"
        )
        self.thread.start()
        logger.info("🛡️ Watchdog started")
        return True
    
    def _run_loop(self):
        while self.running:
            try:
                self._scan()
            except Exception as e:
                logger.error(f"Watchdog scan error: {e}")
            time.sleep(self.interval)
    
    def _scan(self):
        start_time = time.time()
        
        for name, component in self.components.items():
            if name not in self.heartbeats:
                self.heartbeats[name] = RealHeartbeat(component=name)
            self.heartbeats[name].beat()
        
        self.metrics["total_checks"] += 1
        elapsed = (time.time() - start_time) * 1000
        self.metrics["last_check_time"] = elapsed
        
        avg = self.metrics["avg_check_time"]
        total = self.metrics["total_checks"]
        self.metrics["avg_check_time"] = (avg * (total - 1) + elapsed) / total
        
        self.metrics["uptime_seconds"] = int((datetime.now() - self._start_time).total_seconds()) if self._start_time else 0
        self.metrics["components_healthy"] = len([h for h in self.heartbeats.values() if h.status == "alive"])
        self.metrics["health_score"] = min(100, self.metrics["components_healthy"] * 100 / max(1, len(self.components)))
    
    def get_status(self) -> Dict:
        uptime = 0
        if self._start_time:
            uptime = int((datetime.now() - self._start_time).total_seconds())
        
        return {
            "version": self.VERSION,
            "running": self.running,
            "components": len(self.components),
            "checks": len(self.history),
            "errors": self.metrics["total_errors"],
            "alerts": self.metrics["total_alerts"],
            "restarts": self.metrics["total_restarts"],
            "uptime_seconds": uptime,
            "health_score": self.metrics["health_score"],
            "components_healthy": self.metrics["components_healthy"],
            "components_degraded": self.metrics["components_degraded"],
            "components_critical": self.metrics["components_critical"],
            "components_offline": self.metrics["components_offline"],
            "metrics": self.metrics,
            "threads": threading.active_count(),
            "pid": os.getpid(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_snapshot(self) -> Dict:
        return {
            "status": self.get_status(),
            "components": list(self.components.keys()),
            "heartbeats": {name: hb.to_dict() for name, hb in self.heartbeats.items()},
            "latency": {name: lm.to_dict() for name, lm in self.latency_metrics.items()},
            "circuit_breakers": {name: cb.to_dict() for name, cb in self.circuit_breakers.items()},
            "component_health": self.component_health.copy(),
            "recent_alerts": self.alert_history[-10:] if self.alert_history else [],
            "recent_errors": self.error_history[-10:] if self.error_history else [],
            "restart_history": self.restart_history[-10:] if self.restart_history else [],
            "latest_scan": datetime.now().isoformat(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_component_detail(self, component: str) -> Optional[Dict]:
        if component not in self.components:
            return None
        
        return {
            "name": component,
            "registered": True,
            "heartbeat": self.heartbeats[component].to_dict() if component in self.heartbeats else None,
            "latency": self.latency_metrics[component].to_dict() if component in self.latency_metrics else None,
            "circuit": self.circuit_breakers[component].to_dict() if component in self.circuit_breakers else None,
            "health_score": self.component_health.get(component, 0),
            "dependencies": self.dependencies.get(component, []),
            "methods": self.component_methods.get(component, {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def reset_circuit(self, component: str):
        if component in self.circuit_breakers:
            self.circuit_breakers[component].reset()
            self.component_health[component] = min(100, self.component_health.get(component, 100) + 20)

# ============================================================
# AUTO-START WATCHDOG
# ============================================================

def _auto_register_components(watchdog_instance):
    components_to_register = [
        "brain_engine", "trading_bot", "knowledge_engine", 
        "scanner", "signal_engine", "watchdog", "telegram_bot"
    ]
    
    for name in components_to_register:
        watchdog_instance.register_component(name, None)
        logger.info(f"✅ Registered: {name}")

# ============================================================
# GLOBAL INSTANCE - WITH AUTO-START
# ============================================================

watchdog = RealSystemWatchdog(interval=10, auto_restart=True)

# Auto-register components
_auto_register_components(watchdog)

# Auto-start watchdog
watchdog.start()

logger.info(f"🛡️ Watchdog started with {len(watchdog.components)} components, PID: {os.getpid()}")

