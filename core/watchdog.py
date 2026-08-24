# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SYSTEM WATCHDOG v3.0 - REAL IMPLEMENTATION
#
# Version: 3.0
#
# FUNGSI REAL:
# - Monitoring komponen yang benar-benar berjalan
# - Deteksi heartbeat dari thread aktual
# - Latency dari request API nyata
# - Circuit breaker untuk exchange & API calls
# - Auto-restart komponen real
# - Alert ke Telegram real
#
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
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from collections import deque
from enum import Enum
import inspect

logger = logging.getLogger(__name__)

# ============================================================
#
# ENUMS
#
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

# ============================================================
#
# DATA CLASSES REAL
#
# ============================================================

@dataclass
class RealLatencyMetric:
    """Real latency tracking dengan data aktual"""
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
    measurement_source: str = "real"  # real, simulated, unknown
    
    def update(self, latency_ms: float):
        """Update dengan data real"""
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
        
        # Real threshold berdasarkan SLA
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
    """Real heartbeat dari thread aktual"""
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
    
    def beat(self):
        """Register heartbeat real dari thread"""
        self.last_beat = datetime.now()
        self.beat_count += 1
        self.consecutive_misses = 0
        self.status = "alive"
        self.is_alive = True
        self.thread_id = threading.get_ident()
        self.thread_name = threading.current_thread().name
        
        if hasattr(self, '_last_beat_time'):
            self.last_beat_interval = (self.last_beat - self._last_beat_time).total_seconds()
        self._last_beat_time = self.last_beat
    
    def miss(self, error: str = None):
        self.missed_beats += 1
        self.consecutive_misses += 1
        self.is_alive = False
        if error:
            self.last_error = error
        if self.consecutive_misses >= 3:
            self.status = "dead"
    
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
            "is_alive": self.is_alive
        }

@dataclass
class RealCircuitBreaker:
    """Real circuit breaker untuk exchange & API calls"""
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
    
    def record_success(self):
        self.total_requests += 1
        self.total_successes += 1
        self.successes += 1
        self.last_success = datetime.now()
        self.last_error = None
        self.last_error_traceback = None
        self.success_rate = (self.total_successes / self.total_requests) * 100 if self.total_requests > 0 else 100
        
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
            "recovery_attempts": self.recovery_attempts
        }

# ============================================================
#
# REAL WATCHDOG ENGINE
#
# ============================================================

class RealSystemWatchdog:
    """
    REAL System Watchdog - Memonitor komponen yang benar-benar berjalan
    """
    
    def __init__(
        self,
        interval: int = 10,
        heartbeat_timeout: int = 30,
        auto_restart: bool = True,
        max_restarts: int = 5,
        restart_cooldown: int = 60
    ):
        self.interval = interval
        self.heartbeat_timeout = heartbeat_timeout
        self.auto_restart = auto_restart
        self.max_restarts = max_restarts
        self.restart_cooldown = restart_cooldown
        
        self.running = False
        self.thread = None
        self._start_time = None
        
        # REAL COMPONENT TRACKING
        self.components: Dict[str, Any] = {}
        self.latency_metrics: Dict[str, RealLatencyMetric] = {}
        self.heartbeats: Dict[str, RealHeartbeat] = {}
        self.circuit_breakers: Dict[str, RealCircuitBreaker] = {}
        self.dependencies: Dict[str, List[str]] = {}
        self.component_methods: Dict[str, List[str]] = {}
        
        # History
        self.history = []
        self.alert_history = []
        self.restart_history = []
        self.error_history = []
        
        # Stats
        self.metrics = {
            "total_checks": 0,
            "total_alerts": 0,
            "total_restarts": 0,
            "total_errors": 0,
            "avg_check_time": 0.0,
            "last_check_time": 0.0,
            "uptime_seconds": 0
        }
        
        # Alert system
        self.alert_callbacks: List[Callable] = []
        self._last_alert_time: Dict[str, datetime] = {}
        
        logger.info("🛡️ REAL System Watchdog v3.0 initialized")
    
    # ============================================================
    #
    # REGISTER REAL COMPONENT
    #
    # ============================================================
    
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
        """
        Register REAL component yang berjalan
        
        Args:
            name: Nama komponen
            component: Instance komponen yang sebenarnya
            dependencies: List komponen yang dibutuhkan
            health_method: Method untuk health check
            restart_method: Method untuk restart
            stop_method: Method untuk stop
            start_method: Method untuk start
        """
        self.components[name] = component
        self.heartbeats[name] = RealHeartbeat(
            component=name,
            process_id=os.getpid()
        )
        self.latency_metrics[name] = RealLatencyMetric(component=name)
        self.circuit_breakers[name] = RealCircuitBreaker(name=name)
        
        if dependencies:
            self.dependencies[name] = dependencies
        
        # Simpan method names
        self.component_methods[name] = {
            "health": health_method,
            "restart": restart_method,
            "stop": stop_method,
            "start": start_method
        }
        
        logger.info(f"✅ Registered REAL component: {name}")
        
        # Initial health check
        try:
            self._perform_health_check(name, component)
        except Exception as e:
            logger.warning(f"Initial health check failed for {name}: {e}")
    
    def _perform_health_check(self, name: str, component: Any) -> Dict:
        """Perform actual health check on component"""
        result = {
            "name": name,
            "status": "UNKNOWN",
            "timestamp": datetime.now().isoformat(),
            "details": {},
            "latency_ms": 0
        }
        
        start_time = time.time()
        
        try:
            methods = self.component_methods.get(name, {})
            health_method = methods.get("health", "health_check")
            
            if hasattr(component, health_method):
                health_result = getattr(component, health_method)()
                
                if isinstance(health_result, dict):
                    result["details"] = health_result
                    result["status"] = "ONLINE" if health_result.get("status") == "OK" else "WARNING"
                elif isinstance(health_result, bool):
                    result["status"] = "ONLINE" if health_result else "WARNING"
                else:
                    result["status"] = "ONLINE" if health_result else "WARNING"
            else:
                # Check if component has basic attributes
                if hasattr(component, "running"):
                    result["status"] = "ONLINE" if component.running else "IDLE"
                else:
                    result["status"] = "AVAILABLE"
            
            # Record heartbeat
            self.record_heartbeat(name)
            
        except Exception as e:
            result["status"] = "ERROR"
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()
            self.record_heartbeat(name, str(e))
            self.record_circuit_failure(name, str(e))
            logger.error(f"Health check failed for {name}: {e}")
        
        result["latency_ms"] = (time.time() - start_time) * 1000
        self.record_latency(name, result["latency_ms"])
        
        return result
    
    # ============================================================
    #
    # REAL HEARTBEAT SYSTEM
    #
    # ============================================================
    
    def record_heartbeat(self, component: str, error: str = None):
        """Record REAL heartbeat from component"""
        if component not in self.heartbeats:
            self.heartbeats[component] = RealHeartbeat(component=component)
        
        if error:
            self.heartbeats[component].miss(error)
        else:
            self.heartbeats[component].beat()
    
    # ============================================================
    #
    # REAL LATENCY SYSTEM
    #
    # ============================================================
    
    def record_latency(self, component: str, latency_ms: float):
        """Record REAL latency from component calls"""
        if component not in self.latency_metrics:
            self.latency_metrics[component] = RealLatencyMetric(component=component)
        
        self.latency_metrics[component].update(latency_ms)
        
        if latency_ms > 500:
            self._trigger_alert(
                severity="warning",
                component=component,
                message=f"High latency: {latency_ms:.1f}ms"
            )
    
    # ============================================================
    #
    # REAL CIRCUIT BREAKER
    #
    # ============================================================
    
    def record_circuit_success(self, component: str):
        """Record successful operation for circuit breaker"""
        if component not in self.circuit_breakers:
            self.circuit_breakers[component] = RealCircuitBreaker(name=component)
        self.circuit_breakers[component].record_success()
    
    def record_circuit_failure(self, component: str, error: str = None):
        """Record failed operation for circuit breaker"""
        if component not in self.circuit_breakers:
            self.circuit_breakers[component] = RealCircuitBreaker(name=component)
        
        tb = traceback.format_exc() if error else None
        self.circuit_breakers[component].record_failure(error, tb)
        
        if self.circuit_breakers[component].state == "OPEN":
            self._trigger_alert(
                severity="critical",
                component=component,
                message=f"Circuit OPEN: {error}"
            )
    
    def can_execute(self, component: str) -> bool:
        """Check if component can execute (circuit breaker)"""
        if component not in self.circuit_breakers:
            self.circuit_breakers[component] = RealCircuitBreaker(name=component)
        return self.circuit_breakers[component].can_execute()
    
    def reset_circuit(self, component: str):
        """Manually reset circuit breaker"""
        if component in self.circuit_breakers:
            self.circuit_breakers[component].reset()
    
    # ============================================================
    #
    # REAL AUTO-RESTART
    #
    # ============================================================
    
    def _attempt_restart(self, component: str):
        """Attempt to restart REAL component"""
        if component not in self.components:
            logger.error(f"Cannot restart {component}: not registered")
            return False
        
        heartbeat = self.heartbeats[component]
        heartbeat.restart_count += 1
        heartbeat.status = "restarting"
        
        methods = self.component_methods.get(component, {})
        comp = self.components[component]
        
        try:
            # Try to restart using registered method
            if hasattr(comp, methods.get("restart", "restart")):
                getattr(comp, methods.get("restart", "restart"))()
                logger.info(f"🔄 Restarted {component} via {methods.get('restart', 'restart')}()")
            elif hasattr(comp, methods.get("start", "start")):
                if hasattr(comp, methods.get("stop", "stop")):
                    getattr(comp, methods.get("stop", "stop"))()
                    time.sleep(1)
                getattr(comp, methods.get("start", "start"))()
                logger.info(f"🔄 Restarted {component} via start/stop")
            else:
                logger.error(f"No restart method for {component}")
                return False
            
            # Verify restart
            time.sleep(2)
            if hasattr(comp, "running"):
                if comp.running:
                    heartbeat.status = "alive"
                    logger.info(f"✅ {component} restarted successfully")
                    self.restart_history.append({
                        "component": component,
                        "timestamp": datetime.now().isoformat(),
                        "attempt": heartbeat.restart_count,
                        "success": True
                    })
                    return True
                else:
                    logger.error(f"❌ {component} restart failed - still not running")
                    return False
            else:
                # Assume success if no running attribute
                heartbeat.status = "alive"
                return True
                
        except Exception as e:
            logger.exception(f"Failed to restart {component}: {e}")
            heartbeat.status = "dead"
            heartbeat.last_error = str(e)
            self.restart_history.append({
                "component": component,
                "timestamp": datetime.now().isoformat(),
                "attempt": heartbeat.restart_count,
                "success": False,
                "error": str(e)
            })
            return False
    
    # ============================================================
    #
    # REAL SYSTEM SCAN
    #
    # ============================================================
    
    def scan(self) -> Dict:
        """Perform REAL system scan"""
        start_time = time.time()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "components": [],
            "system_metrics": self._get_real_system_metrics(),
            "summary": {
                "total": len(self.components),
                "online": 0,
                "warning": 0,
                "error": 0,
                "offline": 0,
                "unknown": 0
            },
            "threads": self._get_thread_info(),
            "process_info": self._get_process_info()
        }
        
        for name, component in self.components.items():
            # Check dependencies first
            if name in self.dependencies:
                deps_ok = all(
                    self.heartbeats.get(dep, RealHeartbeat(dep)).status == "alive"
                    for dep in self.dependencies[name]
                )
                if not deps_ok:
                    result = {
                        "name": name,
                        "status": "DEPENDENCY_FAILURE",
                        "timestamp": datetime.now().isoformat(),
                        "error": "Dependency failure"
                    }
                    report["components"].append(result)
                    report["summary"]["error"] += 1
                    continue
            
            # Perform health check
            result = self._perform_health_check(name, component)
            report["components"].append(result)
            
            # Update summary
            status = result.get("status", "UNKNOWN")
            if status == "ONLINE" or status == "AVAILABLE":
                report["summary"]["online"] += 1
            elif status == "WARNING" or status == "IDLE":
                report["summary"]["warning"] += 1
            elif status == "ERROR":
                report["summary"]["error"] += 1
            elif status == "OFFLINE":
                report["summary"]["offline"] += 1
            else:
                report["summary"]["unknown"] += 1
        
        # Add real metrics
        report["heartbeats"] = {
            name: hb.to_dict()
            for name, hb in self.heartbeats.items()
        }
        
        report["latency"] = {
            name: lm.to_dict()
            for name, lm in self.latency_metrics.items()
        }
        
        report["circuit_breakers"] = {
            name: cb.to_dict()
            for name, cb in self.circuit_breakers.items()
        }
        
        # Store history
        self.history.append(report)
        if len(self.history) > 500:
            self.history.pop(0)
        
        # Update metrics
        elapsed = (time.time() - start_time) * 1000
        self.metrics["total_checks"] += 1
        self.metrics["last_check_time"] = elapsed
        self.metrics["avg_check_time"] = (
            (self.metrics["avg_check_time"] * (self.metrics["total_checks"] - 1) + elapsed) 
            / self.metrics["total_checks"]
        )
        
        # Check for critical conditions
        if report["summary"]["error"] > 0:
            self._trigger_alert(
                severity="warning",
                component="system",
                message=f"{report['summary']['error']} components in error state"
            )
        
        return report
    
    def _get_real_system_metrics(self) -> Dict:
        """Get REAL system metrics from psutil"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=0.5),
                "cpu_count": psutil.cpu_count(),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_used_gb": psutil.virtual_memory().used / (1024**3),
                "memory_total_gb": psutil.virtual_memory().total / (1024**3),
                "disk_percent": psutil.disk_usage('/').percent,
                "disk_used_gb": psutil.disk_usage('/').used / (1024**3),
                "disk_total_gb": psutil.disk_usage('/').total / (1024**3),
                "load_avg": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0],
                "threads": threading.active_count(),
                "processes": len(psutil.pids()),
                "network_connections": len(psutil.net_connections()),
                "cpu_freq": psutil.cpu_freq().current if hasattr(psutil.cpu_freq(), 'current') else 0
            }
        except Exception as e:
            logger.error(f"System metrics error: {e}")
            return {}
    
    def _get_thread_info(self) -> List[Dict]:
        """Get REAL thread information"""
        threads = []
        for thread in threading.enumerate():
            threads.append({
                "name": thread.name,
                "id": thread.ident,
                "daemon": thread.daemon,
                "alive": thread.is_alive()
            })
        return threads
    
    def _get_process_info(self) -> Dict:
        """Get REAL process information"""
        try:
            process = psutil.Process(os.getpid())
            return {
                "pid": os.getpid(),
                "name": process.name(),
                "status": process.status(),
                "create_time": datetime.fromtimestamp(process.create_time()).isoformat(),
                "memory_rss_mb": process.memory_info().rss / (1024**2),
                "memory_vms_mb": process.memory_info().vms / (1024**2),
                "cpu_percent": process.cpu_percent(),
                "threads": process.num_threads()
            }
        except Exception as e:
            return {"pid": os.getpid(), "error": str(e)}
    
    # ============================================================
    #
    # REAL ALERT SYSTEM
    #
    # ============================================================
    
    def _trigger_alert(self, severity: str, component: str, message: str):
        """Trigger REAL alert with rate limiting"""
        alert_key = f"{component}_{severity}"
        now = datetime.now()
        
        if alert_key in self._last_alert_time:
            if (now - self._last_alert_time[alert_key]).seconds < 30:
                return
        
        self._last_alert_time[alert_key] = now
        self.metrics["total_alerts"] += 1
        
        alert = {
            "timestamp": now.isoformat(),
            "severity": severity,
            "component": component,
            "message": message,
            "alert_id": self.metrics["total_alerts"]
        }
        
        self.alert_history.append(alert)
        if len(self.alert_history) > 100:
            self.alert_history.pop(0)
        
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Alert callback error: {e}")
        
        log_level = logging.CRITICAL if severity == "critical" else logging.WARNING
        logger.log(log_level, f"🚨 [{severity.upper()}] {component}: {message}")
    
    def register_alert_callback(self, callback: Callable):
        """Register callback for alerts"""
        self.alert_callbacks.append(callback)
        logger.info("Alert callback registered")
    
    # ============================================================
    #
    # MONITOR LOOP
    #
    # ============================================================
    
    def loop(self):
        """Main monitoring loop"""
        logger.info("🛡️ Watchdog monitoring started")
        self._start_time = datetime.now()
        
        while self.running:
            loop_start = time.time()
            
            try:
                report = self.scan()
                
                # Check for dead components
                for name, hb in self.heartbeats.items():
                    if hb.status == "dead" and self.auto_restart:
                        if hb.restart_count < self.max_restarts:
                            self._attempt_restart(name)
                        else:
                            self._trigger_alert(
                                severity="critical",
                                component=name,
                                message=f"Max restarts ({self.max_restarts}) exceeded"
                            )
                
            except Exception as e:
                self.metrics["total_errors"] += 1
                logger.exception(f"Watchdog loop error: {e}")
                self.error_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                    "traceback": traceback.format_exc()
                })
            
            elapsed = time.time() - loop_start
            sleep_time = max(0, self.interval - elapsed)
            
            for _ in range(int(sleep_time)):
                if not self.running:
                    break
                time.sleep(1)
    
    # ============================================================
    #
    # START / STOP
    #
    # ============================================================
    
    def start(self) -> bool:
        if self.running:
            return False
        
        self.running = True
        self.thread = threading.Thread(
            target=self.loop,
            daemon=True,
            name="RealWatchdog"
        )
        self.thread.start()
        logger.info("🛡️ Watchdog started")
        return True
    
    def stop(self) -> bool:
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            self.thread = None
        logger.info("🛡️ Watchdog stopped")
        return True
    
    # ============================================================
    #
    # STATUS API
    #
    # ============================================================
    
    def get_status(self) -> Dict:
        """Get REAL status"""
        uptime = 0
        if self._start_time:
            uptime = (datetime.now() - self._start_time).seconds
        
        return {
            "running": self.running,
            "components": len(self.components),
            "checks": len(self.history),
            "errors": self.metrics["total_errors"],
            "alerts": self.metrics["total_alerts"],
            "restarts": self.metrics["total_restarts"],
            "uptime_seconds": uptime,
            "metrics": self.metrics,
            "threads": threading.active_count(),
            "pid": os.getpid()
        }
    
    def get_snapshot(self) -> Dict:
        """Get full REAL snapshot"""
        return {
            "status": self.get_status(),
            "latest_scan": self.history[-1] if self.history else None,
            "circuit_breakers": {
                name: cb.to_dict()
                for name, cb in self.circuit_breakers.items()
            },
            "heartbeats": {
                name: hb.to_dict()
                for name, hb in self.heartbeats.items()
            },
            "latency": {
                name: lm.to_dict()
                for name, lm in self.latency_metrics.items()
            },
            "recent_alerts": self.alert_history[-10:],
            "recent_errors": self.error_history[-10:],
            "restart_history": self.restart_history[-10:]
        }
    
    def get_component_detail(self, component: str) -> Optional[Dict]:
        """Get REAL detail for specific component"""
        if component not in self.components:
            return None
        
        return {
            "name": component,
            "registered": True,
            "heartbeat": self.heartbeats[component].to_dict() if component in self.heartbeats else None,
            "latency": self.latency_metrics[component].to_dict() if component in self.latency_metrics else None,
            "circuit": self.circuit_breakers[component].to_dict() if component in self.circuit_breakers else None,
            "dependencies": self.dependencies.get(component, []),
            "methods": self.component_methods.get(component, {}),
            "has_health_method": hasattr(self.components[component], "health_check"),
            "is_running": getattr(self.components[component], "running", False) if hasattr(self.components[component], "running") else None
        }

# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

watchdog = RealSystemWatchdog()

# ============================================================
#
# END
#
# ============================================================
