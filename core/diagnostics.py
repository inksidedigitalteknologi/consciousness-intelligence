# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SYSTEM DIAGNOSTICS ENGINE v4.0
#
# ULTRA COMPREHENSIVE DIAGNOSTIC SYSTEM
#
# ============================================================

from __future__ import annotations

import logging
import sys
import platform
import time
import json
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import threading
import statistics

logger = logging.getLogger(__name__)


# ============================================================
# CONSTANTS
# ============================================================

DIAGNOSTICS_VERSION = "4.0.0"

# Status
STATUS_ONLINE = "ONLINE"
STATUS_OFFLINE = "OFFLINE"
STATUS_DEGRADED = "DEGRADED"
STATUS_FAILED = "FAILED"
STATUS_WARNING = "WARNING"
STATUS_READY = "READY"
STATUS_UNKNOWN = "UNKNOWN"
STATUS_RECOVERING = "RECOVERING"
STATUS_MAINTENANCE = "MAINTENANCE"
STATUS_OVERLOADED = "OVERLOADED"

# Severity
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_LOW = "LOW"
SEVERITY_INFO = "INFO"

# Risk Levels
RISK_CRITICAL = "CRITICAL"
RISK_HIGH = "HIGH"
RISK_MODERATE = "MODERATE"
RISK_LOW = "LOW"
RISK_NEGLIGIBLE = "NEGLIGIBLE"

# Alert Types
ALERT_SYSTEM = "SYSTEM"
ALERT_COMPONENT = "COMPONENT"
ALERT_PERFORMANCE = "PERFORMANCE"
ALERT_SECURITY = "SECURITY"
ALERT_CAPACITY = "CAPACITY"
ALERT_COMPLIANCE = "COMPLIANCE"


# ============================================================
# ENUMS
# ============================================================

class DiagnosticLevel(Enum):
    """Diagnostic detail level."""
    MINIMAL = "minimal"
    STANDARD = "standard"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"


class HealthStatus(Enum):
    """Health status levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class Trend(Enum):
    """Trend direction."""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    VOLATILE = "volatile"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class ComponentHealth:
    """Health information for a component."""
    name: str
    status: str = STATUS_UNKNOWN
    details: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    load_time: float = 0.0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    health_score: float = 100.0
    uptime: float = 0.0
    last_check: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """System alert."""
    id: str
    type: str
    severity: str
    message: str
    timestamp: str
    source: str
    details: Dict[str, Any] = field(default_factory=dict)
    acknowledged: bool = False
    resolved: bool = False
    resolution: Optional[str] = None
    resolved_at: Optional[str] = None


@dataclass
class RiskAssessment:
    """Risk assessment for a component."""
    component: str
    risk_level: str = RISK_LOW
    score: float = 0.0
    factors: List[str] = field(default_factory=list)
    mitigation: List[str] = field(default_factory=list)
    impact: str = "LOW"
    probability: str = "LOW"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class PerformanceBenchmark:
    """Performance benchmark result."""
    name: str
    value: float
    unit: str
    threshold: float
    status: str
    percentile: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DiagnosticReport:
    """Complete diagnostic report."""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = DIAGNOSTICS_VERSION
    system: Dict[str, Any] = field(default_factory=dict)
    components: Dict[str, ComponentHealth] = field(default_factory=dict)
    modules: Dict[str, Any] = field(default_factory=dict)
    performance: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    health_score: float = 100.0
    summary: Dict[str, Any] = field(default_factory=dict)
    alerts: List[Alert] = field(default_factory=list)
    risks: List[RiskAssessment] = field(default_factory=list)
    benchmarks: List[PerformanceBenchmark] = field(default_factory=list)
    trends: Dict[str, Any] = field(default_factory=dict)
    compliance: Dict[str, Any] = field(default_factory=dict)
    security: Dict[str, Any] = field(default_factory=dict)
    capacity: Dict[str, Any] = field(default_factory=dict)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    health_status: str = HealthStatus.GOOD.value
    trend: str = Trend.STABLE.value


# ============================================================
# SAFE IMPORTS
# ============================================================

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

try:
    from core.module_manager import module_manager
    MODULE_MANAGER_AVAILABLE = True
except Exception:
    module_manager = None
    MODULE_MANAGER_AVAILABLE = False

try:
    from core.validator import validator
    VALIDATOR_AVAILABLE = True
except Exception:
    validator = None
    VALIDATOR_AVAILABLE = False

try:
    from core.health import get_status, health_monitor
    HEALTH_AVAILABLE = True
except ImportError:
    get_status = None
    health_monitor = None
    HEALTH_AVAILABLE = False

try:
    from core.memory import memory
    MEMORY_AVAILABLE = True
except Exception:
    memory = None
    MEMORY_AVAILABLE = False

try:
    from core.brain import brain as brain_instance
    BRAIN_AVAILABLE = True
except Exception:
    brain_instance = None
    BRAIN_AVAILABLE = False

try:
    from core.consciousness import consciousness
    CONSCIOUSNESS_AVAILABLE = True
except Exception:
    consciousness = None
    CONSCIOUSNESS_AVAILABLE = False

try:
    from core.learning.engine import learning_engine
    LEARNING_AVAILABLE = True
except Exception:
    learning_engine = None
    LEARNING_AVAILABLE = False

try:
    from core.learning.pattern import pattern
    PATTERN_AVAILABLE = True
except Exception:
    pattern = None
    PATTERN_AVAILABLE = False

try:
    from core.runtime import runtime
    RUNTIME_AVAILABLE = True
except Exception:
    runtime = None
    RUNTIME_AVAILABLE = False

try:
    from core.scheduler import scheduler
    SCHEDULER_AVAILABLE = True
except Exception:
    scheduler = None
    SCHEDULER_AVAILABLE = False

try:
    from core.watchdog import watchdog
    WATCHDOG_AVAILABLE = True
except Exception:
    watchdog = None
    WATCHDOG_AVAILABLE = False

try:
    from core.scanner import scanner
    SCANNER_AVAILABLE = True
except Exception:
    scanner = None
    SCANNER_AVAILABLE = False

try:
    from core.signal_engine import signal_engine
    SIGNAL_AVAILABLE = True
except Exception:
    signal_engine = None
    SIGNAL_AVAILABLE = False


# ============================================================
# SYSTEM DIAGNOSTICS ENGINE v4.0
# ============================================================

class SystemDiagnostics:
    """
    System Diagnostics v4.0 - Ultra Comprehensive Diagnostic System.
    """

    VERSION = DIAGNOSTICS_VERSION
    MAX_HISTORY = 500
    ALERT_WINDOW = 3600  # 1 hour
    HEALTH_THRESHOLDS = {
        HealthStatus.EXCELLENT: 95,
        HealthStatus.GOOD: 80,
        HealthStatus.FAIR: 65,
        HealthStatus.POOR: 50,
        HealthStatus.CRITICAL: 0,
    }

    def __init__(self):
        self.report = DiagnosticReport()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.recommendations: List[str] = []
        self.history: List[DiagnosticReport] = []
        self.max_history = self.MAX_HISTORY
        self.alert_history: List[Alert] = []
        self.risk_history: List[RiskAssessment] = []
        self.benchmark_history: List[PerformanceBenchmark] = []
        
        self.diagnostic_count = 0
        self.last_run_time: Optional[str] = None
        self.average_run_time = 0.0
        self.run_times: List[float] = []
        self.score_history: deque = deque(maxlen=100)
        self.trend_cache: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._component_dependencies = self._init_dependencies()
        
        self.thresholds = {
            "cpu_warning": 80,
            "cpu_critical": 95,
            "memory_warning": 80,
            "memory_critical": 95,
            "disk_warning": 85,
            "disk_critical": 95,
            "error_threshold": 10,
            "warning_threshold": 20,
        }
        
        logger.info("System Diagnostics v%s initialized.", self.VERSION)

    def _init_dependencies(self) -> Dict[str, List[str]]:
        """Initialize component dependencies."""
        return {
            "Brain": ["Memory", "Consciousness"],
            "Consciousness": ["Memory", "Learning Engine"],
            "Learning Engine": ["Memory", "Pattern Engine"],
            "Pattern Engine": ["Memory"],
            "Runtime": ["Scheduler", "Module Manager"],
            "Scheduler": ["Runtime"],
            "Watchdog": ["Runtime", "Health Monitor"],
            "Health Monitor": ["Runtime"],
            "Module Manager": ["Runtime"],
            "Scanner": ["Signal Engine", "Market Data"],
            "Signal Engine": ["Scanner"],
        }

    # ============================================================
    # MAIN DIAGNOSTIC RUN
    # ============================================================

    def run(
        self,
        level: DiagnosticLevel = DiagnosticLevel.STANDARD,
        full_scan: bool = True,
        include_forecast: bool = True
    ) -> DiagnosticReport:
        with self._lock:
            start_time = time.time()
            self.diagnostic_count += 1
            logger.info("Starting system diagnostics (level: %s)...", level.value)
            
            self.report = DiagnosticReport()
            self.errors = []
            self.warnings = []
            self.recommendations = []
            
            try:
                self._check_system()
                self._check_components()
                if full_scan or level != DiagnosticLevel.MINIMAL:
                    self._check_modules()
                if full_scan or level != DiagnosticLevel.MINIMAL:
                    self._check_learning()
                self._check_performance()
                if full_scan or level != DiagnosticLevel.MINIMAL:
                    self._check_resources()
                if full_scan and level == DiagnosticLevel.COMPREHENSIVE:
                    self._analyze_dependencies()
                if full_scan and level in [DiagnosticLevel.DETAILED, DiagnosticLevel.COMPREHENSIVE]:
                    self._assess_risks()
                if full_scan and level == DiagnosticLevel.COMPREHENSIVE:
                    self._run_benchmarks()
                if full_scan and level == DiagnosticLevel.COMPREHENSIVE:
                    self._assess_security()
                if full_scan and level == DiagnosticLevel.COMPREHENSIVE:
                    self._check_compliance()
                if full_scan and level in [DiagnosticLevel.DETAILED, DiagnosticLevel.COMPREHENSIVE]:
                    self._check_capacity()
                if include_forecast:
                    self._analyze_trends()
                if full_scan and level in [DiagnosticLevel.DETAILED, DiagnosticLevel.COMPREHENSIVE]:
                    self._detect_anomalies()
                if self.errors and level in [DiagnosticLevel.DETAILED, DiagnosticLevel.COMPREHENSIVE]:
                    self._root_cause_analysis()
                self._generate_recommendations()
                self._generate_alerts()
            except Exception as e:
                self.errors.append(f"Diagnostics failed: {e}")
                logger.exception("Diagnostics failed: %s", e)
            
            self._calculate_health_score()
            self._determine_health_status()
            self._build_summary()
            
            self.report.errors = self.errors
            self.report.warnings = self.warnings
            self.report.recommendations = self.recommendations
            self.report.health_score = self._calculate_health_score()
            self.report.health_status = self._determine_health_status()
            self.report.trend = self._determine_trend()
            
            self._record_history()
            
            elapsed = time.time() - start_time
            self.run_times.append(elapsed)
            if len(self.run_times) > 100:
                self.run_times = self.run_times[-100:]
            self.average_run_time = sum(self.run_times) / len(self.run_times)
            self.last_run_time = datetime.now().isoformat()
            
            logger.info("Diagnostics completed in %.2fs (score: %.1f%%)", 
                       elapsed, self.report.health_score)
            return self.report

    # ============================================================
    # SYSTEM CHECK
    # ============================================================

    def _check_system(self) -> None:
        try:
            self.report.system = {
                "python": sys.version,
                "platform": platform.platform(),
                "processor": platform.processor(),
                "architecture": platform.architecture(),
                "hostname": platform.node(),
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "timestamp": datetime.now().isoformat(),
                "status": STATUS_READY,
                "python_implementation": platform.python_implementation(),
                "python_compiler": platform.python_compiler(),
                "python_build": platform.python_build(),
            }
        except Exception as e:
            self.errors.append(f"System check failed: {e}")

    # ============================================================
    # COMPONENT CHECKS
    # ============================================================

    def _check_components(self) -> None:
        components = []
        component_checks = [
            ("Brain", BRAIN_AVAILABLE, brain_instance, None),
            ("Consciousness", CONSCIOUSNESS_AVAILABLE, consciousness, "status"),
            ("Memory", MEMORY_AVAILABLE, memory, "stats"),
            ("Learning Engine", LEARNING_AVAILABLE, learning_engine, "status"),
            ("Pattern Engine", PATTERN_AVAILABLE, pattern, "get_state"),
            ("Runtime", RUNTIME_AVAILABLE, runtime, "status"),
            ("Scheduler", SCHEDULER_AVAILABLE, scheduler, "status"),
            ("Watchdog", WATCHDOG_AVAILABLE, watchdog, "status"),
            ("Health Monitor", HEALTH_AVAILABLE, health_monitor, "status"),
            ("Module Manager", MODULE_MANAGER_AVAILABLE, module_manager, "snapshot"),
            ("Scanner", SCANNER_AVAILABLE, scanner, "status"),
            ("Signal Engine", SIGNAL_AVAILABLE, signal_engine, "status"),
        ]
        
        for name, available, module, attr in component_checks:
            comp = ComponentHealth(name)
            if available and module:
                try:
                    comp.status = STATUS_ONLINE
                    comp.health_score = 100.0
                    comp.last_check = datetime.now().isoformat()
                    if attr:
                        try:
                            if hasattr(module, attr):
                                data = getattr(module, attr)
                                if callable(data):
                                    data = data()
                                if isinstance(data, dict):
                                    comp.details.update(data)
                        except Exception as e:
                            comp.warnings.append(f"Could not get {attr}: {e}")
                    comp.dependencies = self._component_dependencies.get(name, [])
                    comp.dependents = [
                        dep for dep, deps in self._component_dependencies.items()
                        if name in deps
                    ]
                except Exception as e:
                    comp.status = STATUS_DEGRADED
                    comp.warnings.append(str(e))
                    comp.health_score = 50.0
            else:
                comp.status = STATUS_OFFLINE
                comp.health_score = 0.0
                comp.errors.append("Component not available")
            components.append(comp)
        
        for comp in components:
            self.report.components[comp.name] = comp

    # ============================================================
    # MODULE CHECK
    # ============================================================

    def _check_modules(self) -> None:
        try:
            if not MODULE_MANAGER_AVAILABLE or not module_manager:
                self.report.modules = {"status": STATUS_OFFLINE}
                self.warnings.append("Module Manager not available")
                return
            
            if hasattr(module_manager, "snapshot"):
                self.report.modules = module_manager.snapshot()
            elif hasattr(module_manager, "system_report"):
                self.report.modules = module_manager.system_report()
            else:
                self.report.modules = {"status": STATUS_UNKNOWN}
                self.warnings.append("Module Manager snapshot not available")
            
            if VALIDATOR_AVAILABLE and validator:
                try:
                    if hasattr(validator, "validate_all"):
                        # Assume validator has modules attribute or similar
                        if hasattr(module_manager, "modules"):
                            validator.validate_all(module_manager.modules)
                            self.report.modules["validation"] = validator.snapshot()
                except Exception as e:
                    self.warnings.append(f"Module validation failed: {e}")
            
            modules = self.report.modules.get("modules", {})
            if isinstance(modules, dict):
                total = len(modules)
                loaded = sum(1 for m in modules.values() if m == "LOADED")
                self.report.modules["summary"] = {
                    "total": total,
                    "loaded": loaded,
                    "loading_rate": (loaded / total * 100) if total > 0 else 0,
                }
        except Exception as e:
            self.errors.append(f"Module check failed: {e}")

    # ============================================================
    # LEARNING CHECK
    # ============================================================

    def _check_learning(self) -> None:
        try:
            if not LEARNING_AVAILABLE or not learning_engine:
                self.report.summary["learning"] = {"status": STATUS_OFFLINE}
                return
            
            state = {}
            if hasattr(learning_engine, "get_state"):
                state = learning_engine.get_state()
            elif hasattr(learning_engine, "status"):
                state = learning_engine.status()
            
            self.report.summary["learning"] = {
                "status": STATUS_ONLINE,
                "state": state,
                "version": getattr(learning_engine, "VERSION", "N/A"),
            }
        except Exception as e:
            self.report.summary["learning"] = {"status": STATUS_FAILED, "error": str(e)}
            self.errors.append(f"Learning Engine error: {e}")

    # ============================================================
    # PERFORMANCE CHECK
    # ============================================================

    def _check_performance(self) -> None:
        try:
            self.report.performance = {
                "diagnostic_count": self.diagnostic_count,
                "average_run_time": round(self.average_run_time, 4),
                "last_run_time": self.last_run_time,
                "history_size": len(self.history),
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "recommendations": len(self.recommendations),
                "total_runs": len(self.run_times),
                "min_run_time": round(min(self.run_times), 4) if self.run_times else 0,
                "max_run_time": round(max(self.run_times), 4) if self.run_times else 0,
            }
        except Exception as e:
            self.warnings.append(f"Performance check failed: {e}")

    # ============================================================
    # RESOURCE CHECK
    # ============================================================

    def _check_resources(self) -> None:
        if not PSUTIL_AVAILABLE:
            self.warnings.append("psutil not available for resource monitoring")
            return
        
        try:
            cpu_percent = psutil.cpu_percent(interval=0.5)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            net_io = psutil.net_io_counters()
            processes = len(psutil.pids())
            
            self.report.system["resources"] = {
                "cpu": {
                    "percent": cpu_percent,
                    "count": cpu_count,
                    "frequency": cpu_freq._asdict() if cpu_freq else None,
                    "status": self._get_resource_status(cpu_percent, "cpu"),
                },
                "memory": {
                    "total": mem.total,
                    "available": mem.available,
                    "used": mem.used,
                    "percent": mem.percent,
                    "status": self._get_resource_status(mem.percent, "memory"),
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": disk.percent,
                    "status": self._get_resource_status(disk.percent, "disk"),
                },
                "network": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv,
                },
                "processes": processes,
                "timestamp": datetime.now().isoformat(),
            }
            
            if cpu_percent > self.thresholds["cpu_warning"]:
                self.warnings.append(f"High CPU usage: {cpu_percent}%")
            if cpu_percent > self.thresholds["cpu_critical"]:
                self.errors.append(f"Critical CPU usage: {cpu_percent}%")
            
            if mem.percent > self.thresholds["memory_warning"]:
                self.warnings.append(f"High memory usage: {mem.percent}%")
            if mem.percent > self.thresholds["memory_critical"]:
                self.errors.append(f"Critical memory usage: {mem.percent}%")
            
            if disk.percent > self.thresholds["disk_warning"]:
                self.warnings.append(f"High disk usage: {disk.percent}%")
            if disk.percent > self.thresholds["disk_critical"]:
                self.errors.append(f"Critical disk usage: {disk.percent}%")
        except Exception as e:
            self.warnings.append(f"Resource check failed: {e}")

    def _get_resource_status(self, value: float, resource_type: str) -> str:
        if resource_type == "cpu":
            if value > self.thresholds["cpu_critical"]:
                return STATUS_CRITICAL
            elif value > self.thresholds["cpu_warning"]:
                return STATUS_WARNING
        elif resource_type == "memory":
            if value > self.thresholds["memory_critical"]:
                return STATUS_CRITICAL
            elif value > self.thresholds["memory_warning"]:
                return STATUS_WARNING
        elif resource_type == "disk":
            if value > self.thresholds["disk_critical"]:
                return STATUS_CRITICAL
            elif value > self.thresholds["disk_warning"]:
                return STATUS_WARNING
        return STATUS_ONLINE

    # ============================================================
    # DEPENDENCY ANALYSIS
    # ============================================================

    def _analyze_dependencies(self) -> None:
        try:
            deps = {}
            for comp_name, comp in self.report.components.items():
                deps[comp_name] = {
                    "dependencies": comp.dependencies,
                    "dependents": comp.dependents,
                    "status": comp.status,
                    "health": comp.health_score,
                }
            self.report.dependencies = deps
            
            for comp_name, comp in self.report.components.items():
                for dep in comp.dependencies:
                    if dep in self.report.components:
                        dep_status = self.report.components[dep].status
                        if dep_status in [STATUS_OFFLINE, STATUS_FAILED]:
                            self.warnings.append(
                                f"Component '{comp_name}' depends on '{dep}' which is {dep_status}"
                            )
                            comp.health_score -= 20
                    else:
                        self.warnings.append(
                            f"Component '{comp_name}' depends on unknown component '{dep}'"
                        )
        except Exception as e:
            self.warnings.append(f"Dependency analysis failed: {e}")

    # ============================================================
    # RISK ASSESSMENT
    # ============================================================

    def _assess_risks(self) -> None:
        try:
            risks = []
            for comp_name, comp in self.report.components.items():
                risk = RiskAssessment(component=comp_name)
                score = 0.0
                factors = []
                
                if comp.status == STATUS_FAILED:
                    score += 40
                    factors.append("Component failed")
                elif comp.status == STATUS_OFFLINE:
                    score += 30
                    factors.append("Component offline")
                elif comp.status == STATUS_DEGRADED:
                    score += 20
                    factors.append("Component degraded")
                
                if comp.errors:
                    score += len(comp.errors) * 5
                    factors.append(f"{len(comp.errors)} errors")
                if comp.warnings:
                    score += len(comp.warnings) * 2
                    factors.append(f"{len(comp.warnings)} warnings")
                if comp.health_score < 50:
                    score += 20
                    factors.append("Low health score")
                
                risk.score = min(score, 100)
                risk.factors = factors
                
                if risk.score >= 70:
                    risk.risk_level = RISK_HIGH
                    risk.impact = "HIGH"
                    risk.probability = "HIGH"
                elif risk.score >= 50:
                    risk.risk_level = RISK_MODERATE
                    risk.impact = "MODERATE"
                    risk.probability = "MODERATE"
                elif risk.score >= 30:
                    risk.risk_level = RISK_LOW
                    risk.impact = "LOW"
                    risk.probability = "LOW"
                else:
                    risk.risk_level = RISK_NEGLIGIBLE
                    risk.impact = "NEGLIGIBLE"
                    risk.probability = "NEGLIGIBLE"
                
                risk.mitigation = self._generate_mitigation(comp_name, risk)
                risks.append(risk)
            
            self.report.risks = risks
            
            high_risks = sum(1 for r in risks if r.risk_level in [RISK_HIGH, RISK_CRITICAL])
            moderate_risks = sum(1 for r in risks if r.risk_level == RISK_MODERATE)
            self.report.summary["risks"] = {
                "high": high_risks,
                "moderate": moderate_risks,
                "low": len(risks) - high_risks - moderate_risks,
                "total": len(risks),
            }
        except Exception as e:
            self.warnings.append(f"Risk assessment failed: {e}")

    def _generate_mitigation(self, component: str, risk: RiskAssessment) -> List[str]:
        mitigations = []
        if risk.risk_level in [RISK_HIGH, RISK_CRITICAL]:
            mitigations.append(f"Immediate action required for {component}")
            if "failed" in str(risk.factors).lower():
                mitigations.append(f"Restart {component} service")
            if "offline" in str(risk.factors).lower():
                mitigations.append(f"Check {component} connectivity and configuration")
            if "errors" in str(risk.factors).lower():
                mitigations.append(f"Review {component} error logs")
        if risk.risk_level == RISK_MODERATE:
            mitigations.append(f"Monitor {component} closely")
            if "degraded" in str(risk.factors).lower():
                mitigations.append(f"Check {component} performance")
        if risk.risk_level == RISK_LOW:
            mitigations.append(f"Review {component} configuration")
            mitigations.append(f"Schedule maintenance for {component}")
        return mitigations

    # ============================================================
    # PERFORMANCE BENCHMARKING
    # ============================================================

    def _run_benchmarks(self) -> None:
        try:
            benchmarks = []
            if PSUTIL_AVAILABLE:
                cpu_percent = psutil.cpu_percent(interval=0.5)
                benchmarks.append(PerformanceBenchmark(
                    name="CPU Usage",
                    value=cpu_percent,
                    unit="%",
                    threshold=self.thresholds["cpu_warning"],
                    status=self._get_resource_status(cpu_percent, "cpu"),
                    percentile=100 - cpu_percent,
                ))
                mem = psutil.virtual_memory()
                benchmarks.append(PerformanceBenchmark(
                    name="Memory Usage",
                    value=mem.percent,
                    unit="%",
                    threshold=self.thresholds["memory_warning"],
                    status=self._get_resource_status(mem.percent, "memory"),
                    percentile=100 - mem.percent,
                ))
            else:
                benchmarks.append(PerformanceBenchmark(
                    name="CPU Usage",
                    value=0,
                    unit="%",
                    threshold=80,
                    status=STATUS_UNKNOWN,
                    percentile=0,
                ))
                benchmarks.append(PerformanceBenchmark(
                    name="Memory Usage",
                    value=0,
                    unit="%",
                    threshold=80,
                    status=STATUS_UNKNOWN,
                    percentile=0,
                ))
            
            for comp_name, comp in self.report.components.items():
                if comp.status == STATUS_ONLINE:
                    benchmarks.append(PerformanceBenchmark(
                        name=f"{comp_name} Health",
                        value=comp.health_score,
                        unit="%",
                        threshold=80,
                        status=STATUS_ONLINE if comp.health_score >= 80 else STATUS_WARNING,
                        percentile=comp.health_score,
                    ))
            
            self.report.benchmarks = benchmarks
        except Exception as e:
            self.warnings.append(f"Benchmark failed: {e}")

    # ============================================================
    # SECURITY ASSESSMENT
    # ============================================================

    def _assess_security(self) -> None:
        try:
            security = {
                "timestamp": datetime.now().isoformat(),
                "status": "SECURE",
                "checks": [],
            }
            py_version = sys.version_info
            if py_version.major == 3 and py_version.minor >= 8:
                security["checks"].append({
                    "name": "Python Version",
                    "status": "PASS",
                    "details": f"{py_version.major}.{py_version.minor}.{py_version.micro}",
                })
            else:
                security["checks"].append({
                    "name": "Python Version",
                    "status": "WARNING",
                    "details": f"Version {py_version.major}.{py_version.minor} may have security issues",
                })
            
            if platform.system() in ["Linux", "Darwin"]:
                security["checks"].append({
                    "name": "Platform Security",
                    "status": "PASS",
                    "details": f"{platform.system()} is secure",
                })
            else:
                security["checks"].append({
                    "name": "Platform Security",
                    "status": "WARNING",
                    "details": f"{platform.system()} may have security concerns",
                })
            
            offline_components = [
                name for name, comp in self.report.components.items()
                if comp.status in [STATUS_OFFLINE, STATUS_FAILED]
            ]
            if offline_components:
                security["checks"].append({
                    "name": "Component Status",
                    "status": "WARNING",
                    "details": f"Offline components: {', '.join(offline_components)}",
                })
                security["status"] = "DEGRADED"
            
            if self.errors:
                security["checks"].append({
                    "name": "Error Analysis",
                    "status": "WARNING",
                    "details": f"{len(self.errors)} errors detected",
                })
                security["status"] = "DEGRADED"
            
            self.report.security = security
        except Exception as e:
            self.warnings.append(f"Security assessment failed: {e}")

    # ============================================================
    # COMPLIANCE CHECK
    # ============================================================

    def _check_compliance(self) -> None:
        try:
            compliance = {
                "timestamp": datetime.now().isoformat(),
                "status": "COMPLIANT",
                "checks": [],
                "requirements": [],
            }
            requirements = [
                {
                    "id": "REQ-001",
                    "name": "System Health",
                    "requirement": "Health score >= 80%",
                    "status": "PASS" if self.report.health_score >= 80 else "FAIL",
                    "actual": f"{self.report.health_score:.1f}%",
                },
                {
                    "id": "REQ-002",
                    "name": "Component Availability",
                    "requirement": "All critical components online",
                    "status": "PASS" if all(
                        comp.status == STATUS_ONLINE 
                        for comp in self.report.components.values()
                    ) else "FAIL",
                    "actual": f"{sum(1 for c in self.report.components.values() if c.status == STATUS_ONLINE)}/{len(self.report.components)}",
                },
                {
                    "id": "REQ-003",
                    "name": "Error Rate",
                    "requirement": "Errors < 5",
                    "status": "PASS" if len(self.errors) < 5 else "FAIL",
                    "actual": str(len(self.errors)),
                },
                {
                    "id": "REQ-004",
                    "name": "Resource Usage",
                    "requirement": "CPU < 80%, Memory < 80%, Disk < 85%",
                    "status": "PASS",
                    "actual": "Monitoring",
                },
            ]
            compliance["requirements"] = requirements
            compliance["checks"] = [
                {
                    "name": req["name"],
                    "status": req["status"],
                    "details": req["requirement"],
                    "actual": req["actual"],
                }
                for req in requirements
            ]
            failed = sum(1 for req in requirements if req["status"] == "FAIL")
            if failed > 0:
                compliance["status"] = "NON_COMPLIANT"
                self.warnings.append(f"{failed} compliance requirements failed")
            self.report.compliance = compliance
        except Exception as e:
            self.warnings.append(f"Compliance check failed: {e}")

    # ============================================================
    # CAPACITY PLANNING
    # ============================================================

    def _check_capacity(self) -> None:
        try:
            capacity = {
                "timestamp": datetime.now().isoformat(),
                "status": "ADEQUATE",
                "resources": {},
                "forecast": {},
            }
            if PSUTIL_AVAILABLE:
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                capacity["resources"] = {
                    "memory": {
                        "total": mem.total,
                        "used": mem.used,
                        "available": mem.available,
                        "percent": mem.percent,
                        "status": "OK" if mem.percent < 80 else "WARNING",
                    },
                    "disk": {
                        "total": disk.total,
                        "used": disk.used,
                        "free": disk.free,
                        "percent": disk.percent,
                        "status": "OK" if disk.percent < 85 else "WARNING",
                    },
                }
                if len(self.history) > 5:
                    avg_memory = []
                    for report in self.history[-10:]:
                        resources = report.system.get("resources", {})
                        if resources:
                            mem_data = resources.get("memory", {})
                            if mem_data:
                                avg_memory.append(mem_data.get("percent", 0))
                    if avg_memory:
                        avg = statistics.mean(avg_memory)
                        if avg > 70:
                            capacity["forecast"]["memory"] = {
                                "warning": "Memory usage trend increasing",
                                "projection": f"~{min(avg + 10, 100):.1f}% in 30 days",
                            }
                            capacity["status"] = "MONITOR"
            self.report.capacity = capacity
        except Exception as e:
            self.warnings.append(f"Capacity check failed: {e}")

    # ============================================================
    # TREND ANALYSIS
    # ============================================================

    def _analyze_trends(self) -> None:
        try:
            if len(self.history) < 2:
                self.report.trends = {
                    "trend": Trend.STABLE.value,
                    "message": "Insufficient data for trend analysis",
                    "confidence": 0,
                }
                return
            scores = [report.health_score for report in self.history[-20:]]
            if len(scores) < 2:
                self.report.trends = {"trend": Trend.STABLE.value, "confidence": 50}
                return
            trend_value = 0
            for i in range(1, len(scores)):
                trend_value += scores[i] - scores[i-1]
            trend_value /= len(scores) - 1
            
            if trend_value > 1:
                trend = Trend.IMPROVING
                message = "System health is improving"
            elif trend_value < -1:
                trend = Trend.DECLINING
                message = "System health is declining"
            elif trend_value > 0.5:
                trend = Trend.VOLATILE
                message = "System health is volatile with positive trend"
            elif trend_value < -0.5:
                trend = Trend.VOLATILE
                message = "System health is volatile with negative trend"
            else:
                trend = Trend.STABLE
                message = "System health is stable"
            
            variance = statistics.variance(scores) if len(scores) > 1 else 0
            confidence = max(50, min(100, 100 - variance))
            
            self.report.trends = {
                "trend": trend.value,
                "message": message,
                "confidence": round(confidence, 2),
                "trend_value": round(trend_value, 2),
                "scores": scores,
                "current": scores[-1],
                "previous": scores[-2],
                "change": round(scores[-1] - scores[-2], 2),
            }
        except Exception as e:
            self.warnings.append(f"Trend analysis failed: {e}")

    # ============================================================
    # ANOMALY DETECTION
    # ============================================================

    def _detect_anomalies(self) -> None:
        try:
            anomalies = []
            if len(self.history) > 5:
                scores = [report.health_score for report in self.history[-10:]]
                if len(scores) > 1:
                    try:
                        mean = statistics.mean(scores)
                        std = statistics.stdev(scores) if len(scores) > 1 else 0
                    except Exception:
                        mean = scores[-1]
                        std = 0
                    for i, score in enumerate(scores):
                        if std > 0 and abs(score - mean) > 2 * std:
                            anomalies.append({
                                "type": "SCORE_DROP",
                                "value": score,
                                "mean": mean,
                                "std": std,
                                "timestamp": self.history[-(10 - i)].timestamp if i < 10 else "unknown",
                            })
            for comp in self.report.components.values():
                if comp.status == STATUS_FAILED and comp.health_score < 30:
                    anomalies.append({
                        "type": "COMPONENT_FAILURE",
                        "component": comp.name,
                        "status": comp.status,
                        "score": comp.health_score,
                    })
            if anomalies:
                self.report.summary["anomalies"] = {
                    "count": len(anomalies),
                    "details": anomalies,
                }
                self.warnings.append(f"{len(anomalies)} anomalies detected")
        except Exception as e:
            self.warnings.append(f"Anomaly detection failed: {e}")

    # ============================================================
    # ROOT CAUSE ANALYSIS
    # ============================================================

    def _root_cause_analysis(self) -> None:
        try:
            if not self.errors:
                return
            root_causes = []
            for error in self.errors:
                cause = self._analyze_error(error)
                root_causes.append({
                    "error": error,
                    "cause": cause,
                    "timestamp": datetime.now().isoformat(),
                })
            self.report.summary["root_causes"] = root_causes
        except Exception as e:
            self.warnings.append(f"Root cause analysis failed: {e}")

    def _analyze_error(self, error: str) -> str:
        error_lower = error.lower()
        if "memory" in error_lower:
            return "Memory resource issue - check memory usage and limits"
        elif "cpu" in error_lower:
            return "CPU resource issue - check CPU usage and processes"
        elif "disk" in error_lower:
            return "Disk resource issue - check disk space and I/O"
        elif "import" in error_lower or "module" in error_lower:
            return "Module import error - check module availability and dependencies"
        elif "timeout" in error_lower:
            return "Timeout error - check network latency and component responsiveness"
        elif "connection" in error_lower or "connect" in error_lower:
            return "Connection error - check network and service availability"
        else:
            return "Unknown error - check logs for details"

    # ============================================================
    # ALERT GENERATION
    # ============================================================

    def _generate_alerts(self) -> None:
        alerts = []
        if self.report.health_score < 50:
            alerts.append(Alert(
                id=self._generate_alert_id(),
                type=ALERT_SYSTEM,
                severity=SEVERITY_CRITICAL,
                message=f"System health critical: {self.report.health_score}%",
                source="diagnostics",
                timestamp=datetime.now().isoformat(),
                details={"health_score": self.report.health_score},
            ))
        for comp in self.report.components.values():
            if comp.status == STATUS_FAILED:
                alerts.append(Alert(
                    id=self._generate_alert_id(),
                    type=ALERT_COMPONENT,
                    severity=SEVERITY_HIGH,
                    message=f"Component '{comp.name}' failed",
                    source="diagnostics",
                    timestamp=datetime.now().isoformat(),
                    details={"component": comp.name, "errors": comp.errors},
                ))
        if PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            if mem.percent > self.thresholds["memory_critical"]:
                alerts.append(Alert(
                    id=self._generate_alert_id(),
                    type=ALERT_PERFORMANCE,
                    severity=SEVERITY_HIGH,
                    message=f"Critical memory usage: {mem.percent}%",
                    source="diagnostics",
                    timestamp=datetime.now().isoformat(),
                    details={"memory_percent": mem.percent},
                ))
        for risk in self.report.risks:
            if risk.risk_level in [RISK_HIGH, RISK_CRITICAL]:
                alerts.append(Alert(
                    id=self._generate_alert_id(),
                    type=ALERT_SYSTEM,
                    severity=SEVERITY_MEDIUM,
                    message=f"High risk detected in '{risk.component}': {risk.score:.1f}%",
                    source="diagnostics",
                    timestamp=datetime.now().isoformat(),
                    details={"component": risk.component, "score": risk.score},
                ))
        self.report.alerts = alerts
        self.alert_history.extend(alerts)
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]

    def _generate_alert_id(self) -> str:
        timestamp = datetime.now().timestamp()
        return hashlib.md5(f"{timestamp}{len(self.alert_history)}".encode()).hexdigest()[:12]

    # ============================================================
    # RECOMMENDATIONS
    # ============================================================

    def _generate_recommendations(self) -> None:
        self.recommendations = []
        if self.errors:
            self.recommendations.append("🔴 Address critical errors immediately")
            for error in self.errors[:3]:
                self.recommendations.append(f"  - {error}")
        offline = [name for name, comp in self.report.components.items() 
                  if comp.status in [STATUS_OFFLINE, STATUS_FAILED]]
        if offline:
            self.recommendations.append(f"🟠 Restart offline components: {', '.join(offline)}")
        degraded = [name for name, comp in self.report.components.items() 
                   if comp.status == STATUS_DEGRADED]
        if degraded:
            self.recommendations.append(f"🟡 Investigate degraded components: {', '.join(degraded)}")
        if PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            if mem.percent > 80:
                self.recommendations.append(f"🟠 High memory usage ({mem.percent}%) - consider cleanup")
            cpu = psutil.cpu_percent()
            if cpu > 80:
                self.recommendations.append(f"🟠 High CPU usage ({cpu}%) - check processes")
        if self.report.health_score < 70:
            self.recommendations.append("🟠 System health below 70% - investigate issues")
        elif self.report.health_score < 90:
            self.recommendations.append("🟡 System health moderate - monitor closely")
        if self.report.security.get("status") == "DEGRADED":
            self.recommendations.append("🔴 Security posture degraded - investigate")
        if self.report.compliance.get("status") == "NON_COMPLIANT":
            self.recommendations.append("🔴 Compliance check failed - review requirements")
        high_risks = [r for r in self.report.risks if r.risk_level in [RISK_HIGH, RISK_CRITICAL]]
        for risk in high_risks[:3]:
            self.recommendations.append(f"🔴 Mitigate high risk in '{risk.component}'")
        if self.report.capacity.get("status") == "MONITOR":
            self.recommendations.append("🟡 Monitor capacity - resources trending toward limits")
        if not self.recommendations:
            self.recommendations.append("✅ All systems healthy. No action required.")

    # ============================================================
    # HEALTH SCORE
    # ============================================================

    def _calculate_health_score(self) -> float:
        score = 100.0
        if self.errors:
            score -= min(len(self.errors) * 5, 30)
        if self.warnings:
            score -= min(len(self.warnings) * 2, 15)
        offline = sum(1 for comp in self.report.components.values() 
                     if comp.status == STATUS_OFFLINE)
        if offline:
            score -= min(offline * 10, 50)
        failed = sum(1 for comp in self.report.components.values() 
                    if comp.status == STATUS_FAILED)
        if failed:
            score -= min(failed * 15, 60)
        degraded = sum(1 for comp in self.report.components.values() 
                      if comp.status == STATUS_DEGRADED)
        if degraded:
            score -= min(degraded * 5, 25)
        if PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            if mem.percent > 80:
                score -= (mem.percent - 80) * 0.5
            cpu = psutil.cpu_percent()
            if cpu > 80:
                score -= (cpu - 80) * 0.5
        if not MODULE_MANAGER_AVAILABLE:
            score -= 10
        if not LEARNING_AVAILABLE:
            score -= 10
        high_risks = sum(1 for r in self.report.risks 
                        if r.risk_level in [RISK_HIGH, RISK_CRITICAL])
        if high_risks:
            score -= min(high_risks * 5, 25)
        self.report.health_score = max(0, min(100, round(score, 2)))
        return self.report.health_score

    def _determine_health_status(self) -> str:
        score = self.report.health_score
        if score >= self.HEALTH_THRESHOLDS[HealthStatus.EXCELLENT]:
            return HealthStatus.EXCELLENT.value
        elif score >= self.HEALTH_THRESHOLDS[HealthStatus.GOOD]:
            return HealthStatus.GOOD.value
        elif score >= self.HEALTH_THRESHOLDS[HealthStatus.FAIR]:
            return HealthStatus.FAIR.value
        elif score >= self.HEALTH_THRESHOLDS[HealthStatus.POOR]:
            return HealthStatus.POOR.value
        else:
            return HealthStatus.CRITICAL.value

    def _determine_trend(self) -> str:
        if "trends" in self.report and self.report.trends:
            return self.report.trends.get("trend", Trend.STABLE.value)
        if len(self.history) < 2:
            return Trend.STABLE.value
        scores = [report.health_score for report in self.history[-5:]]
        if len(scores) < 2:
            return Trend.STABLE.value
        avg_change = (scores[-1] - scores[0]) / len(scores)
        if avg_change > 1:
            return Trend.IMPROVING.value
        elif avg_change < -1:
            return Trend.DECLINING.value
        else:
            return Trend.STABLE.value

    # ============================================================
    # SUMMARY
    # ============================================================

    def _build_summary(self) -> None:
        try:
            total_components = len(self.report.components)
            online = sum(1 for comp in self.report.components.values() 
                        if comp.status == STATUS_ONLINE)
            degraded = sum(1 for comp in self.report.components.values() 
                          if comp.status == STATUS_DEGRADED)
            offline = sum(1 for comp in self.report.components.values() 
                         if comp.status == STATUS_OFFLINE)
            failed = sum(1 for comp in self.report.components.values() 
                        if comp.status == STATUS_FAILED)
            self.report.summary.update({
                "status": STATUS_READY if not self.errors else STATUS_WARNING,
                "components": {
                    "total": total_components,
                    "online": online,
                    "degraded": degraded,
                    "offline": offline,
                    "failed": failed,
                },
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "recommendations": len(self.recommendations),
                "alerts": len(self.report.alerts),
                "risks": len(self.report.risks),
                "health_score": self.report.health_score,
                "health_status": self.report.health_status,
                "trend": self.report.trend,
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            self.warnings.append(f"Summary build failed: {e}")

    # ============================================================
    # HISTORY
    # ============================================================

    def _record_history(self) -> None:
        try:
            self.history.append(self.report)
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
            self.score_history.append(self.report.health_score)
        except Exception as e:
            logger.warning(f"History record failed: {e}")

    def get_history(self, limit: int = 10) -> List[DiagnosticReport]:
        return self.history[-limit:] if self.history else []

    def get_score_history(self, limit: int = 50) -> List[float]:
        return list(self.score_history)[-limit:] if self.score_history else []

    def get_health_trend(self) -> Dict[str, Any]:
        if not self.history:
            return {"trend": "NO_DATA", "scores": []}
        scores = [report.health_score for report in self.history[-20:]]
        trend = self._determine_trend()
        return {
            "trend": trend,
            "current": scores[-1] if scores else 0,
            "min": min(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "average": sum(scores) / len(scores) if scores else 0,
            "scores": scores,
        }

    def get_alerts(
        self,
        severity: Optional[str] = None,
        resolved: Optional[bool] = None,
        limit: int = 50
    ) -> List[Alert]:
        alerts = self.alert_history
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        if resolved is not None:
            alerts = [a for a in alerts if a.resolved == resolved]
        return alerts[-limit:] if alerts else []

    def get_risks(self, risk_level: Optional[str] = None) -> List[RiskAssessment]:
        risks = self.report.risks
        if risk_level:
            risks = [r for r in risks if r.risk_level == risk_level]
        return risks

    # ============================================================
    # SNAPSHOT & REPORT
    # ============================================================

    def snapshot(self) -> Dict[str, Any]:
        # Use the most recent report if available, otherwise run minimal
        if self.history:
            latest = self.history[-1]
            return {
                "timestamp": datetime.now().isoformat(),
                "health_score": latest.health_score,
                "health_status": latest.health_status,
                "status": latest.summary.get("status", STATUS_UNKNOWN),
                "errors": len(latest.errors),
                "warnings": len(latest.warnings),
                "online_components": latest.summary.get("components", {}).get("online", 0),
                "total_components": latest.summary.get("components", {}).get("total", 0),
                "alerts": len(latest.alerts),
                "trend": latest.trend,
            }
        else:
            # Run a minimal scan
            report = self.run(level=DiagnosticLevel.MINIMAL)
            return {
                "timestamp": datetime.now().isoformat(),
                "health_score": report.health_score,
                "health_status": report.health_status,
                "status": report.summary.get("status", STATUS_UNKNOWN),
                "errors": len(report.errors),
                "warnings": len(report.warnings),
                "online_components": report.summary.get("components", {}).get("online", 0),
                "total_components": report.summary.get("components", {}).get("total", 0),
                "alerts": len(report.alerts),
                "trend": report.trend,
            }

    def report(self, level: DiagnosticLevel = DiagnosticLevel.COMPREHENSIVE) -> Dict[str, Any]:
        result = self.run(level=level)
        return self._to_dict(result)

    def export_json(self, level: DiagnosticLevel = DiagnosticLevel.COMPREHENSIVE) -> str:
        report = self.run(level=level)
        return json.dumps(self._to_dict(report), indent=2, default=str)

    def _to_dict(self, obj: Any) -> Dict[str, Any]:
        if hasattr(obj, "__dataclass_fields__"):
            result = {}
            for field_name in obj.__dataclass_fields__:
                value = getattr(obj, field_name)
                result[field_name] = self._to_dict(value)
            return result
        elif isinstance(obj, dict):
            return {k: self._to_dict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._to_dict(item) for item in obj]
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return obj

    # ============================================================
    # CONTINUOUS MONITORING
    # ============================================================

    def start_monitoring(self, interval: int = 60):
        if hasattr(self, "_monitoring_thread") and self._monitoring_thread.is_alive():
            logger.warning("Monitoring already running")
            return
        
        def monitor_loop():
            while True:
                try:
                    self.run(level=DiagnosticLevel.STANDARD, full_scan=True)
                    logger.debug("Monitoring scan completed")
                except Exception as e:
                    logger.error(f"Monitoring scan failed: {e}")
                time.sleep(interval)
        
        self._monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self._monitoring_thread.start()
        logger.info("Continuous monitoring started (interval: %ds)", interval)

    def stop_monitoring(self):
        if hasattr(self, "_monitoring_thread"):
            self._monitoring_thread = None
            logger.info("Continuous monitoring stopped")

    # ============================================================
    # INCIDENT REPORTING
    # ============================================================

    def generate_incident_report(self, incident_id: str, description: str) -> Dict[str, Any]:
        report = self.run(level=DiagnosticLevel.COMPREHENSIVE)
        incident = {
            "incident_id": incident_id,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "system_state": {
                "health_score": report.health_score,
                "health_status": report.health_status,
                "status": report.summary.get("status", STATUS_UNKNOWN),
            },
            "components": {
                name: {
                    "status": comp.status,
                    "health": comp.health_score,
                    "errors": comp.errors,
                    "warnings": comp.warnings,
                }
                for name, comp in report.components.items()
                if comp.errors or comp.warnings or comp.status != STATUS_ONLINE
            },
            "errors": report.errors,
            "warnings": report.warnings,
            "recommendations": report.recommendations,
            "alerts": [
                {
                    "severity": alert.severity,
                    "message": alert.message,
                    "source": alert.source,
                    "timestamp": alert.timestamp,
                }
                for alert in report.alerts
            ],
            "risks": [
                {
                    "component": risk.component,
                    "level": risk.risk_level,
                    "score": risk.score,
                    "factors": risk.factors,
                }
                for risk in report.risks
            ],
        }
        return incident


# ============================================================
# GLOBAL INSTANCE
# ============================================================

diagnostics = SystemDiagnostics()


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def get_diagnostics():
    return diagnostics


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    print()
    print("=" * 80)
    print("  SYSTEM DIAGNOSTICS v4.0 - ULTRA SELF TEST")
    print("=" * 80)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        test_diag = SystemDiagnostics()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Run diagnostics
    print("\n2. Testing diagnostic run...")
    try:
        report = diagnostics.run()
        if report and report.health_score is not None:
            results["run"] = {"status": "PASS", "score": report.health_score}
            tests_passed += 1
            print(f"   ✅ Run passed (score: {report.health_score:.1f}%)")
        else:
            results["run"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Run failed")
    except Exception as e:
        results["run"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Run failed: {e}")
    
    # Test 3: Snapshot
    print("\n3. Testing snapshot...")
    try:
        snapshot = diagnostics.snapshot()
        if snapshot and "health_score" in snapshot:
            results["snapshot"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Snapshot passed")
        else:
            results["snapshot"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Snapshot failed")
    except Exception as e:
        results["snapshot"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Snapshot failed: {e}")
    
    # Test 4: Alerts
    print("\n4. Testing alerts...")
    try:
        alerts = diagnostics.get_alerts()
        if alerts is not None:
            results["alerts"] = {"status": "PASS", "count": len(alerts)}
            tests_passed += 1
            print(f"   ✅ Alerts passed ({len(alerts)} alerts)")
        else:
            results["alerts"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Alerts failed")
    except Exception as e:
        results["alerts"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Alerts failed: {e}")
    
    # Test 5: Trend Analysis
    print("\n5. Testing trend analysis...")
    try:
        trend = diagnostics.get_health_trend()
        if trend and "trend" in trend:
            results["trend"] = {"status": "PASS", "trend": trend["trend"]}
            tests_passed += 1
            print(f"   ✅ Trend analysis passed (trend: {trend['trend']})")
        else:
            results["trend"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Trend analysis failed")
    except Exception as e:
        results["trend"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Trend analysis failed: {e}")
    
    # Test 6: Export
    print("\n6. Testing export...")
    try:
        json_data = diagnostics.export_json()
        if json_data and len(json_data) > 100:
            results["export"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Export passed")
        else:
            results["export"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Export failed")
    except Exception as e:
        results["export"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Export failed: {e}")
    
    # Summary
    print()
    print("=" * 80)
    print("  TEST SUMMARY")
    print("=" * 80)
    print(f"  ✅ Passed: {tests_passed}")
    print(f"  ❌ Failed: {tests_failed}")
    print(f"  📊 Total:  {tests_passed + tests_failed}")
    print("=" * 80)
    
    return {
        "module": "diagnostics",
        "version": DIAGNOSTICS_VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    
    result = self_test()
    
    print()
    print("=" * 80)
    print("  SYSTEM DIAGNOSTICS v4.0 - ULTRA SELF TEST COMPLETE")
    print("=" * 80)
    print()
    print("Final Status:", result["status"])
    print("Tests Passed:", result["tests_passed"])
    print("Tests Failed:", result["tests_failed"])


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "SystemDiagnostics",
    "ComponentHealth",
    "DiagnosticReport",
    "Alert",
    "RiskAssessment",
    "PerformanceBenchmark",
    "DiagnosticLevel",
    "HealthStatus",
    "Trend",
    "DIAGNOSTICS_VERSION",
    "STATUS_ONLINE",
    "STATUS_OFFLINE",
    "STATUS_DEGRADED",
    "STATUS_FAILED",
    "STATUS_WARNING",
    "STATUS_READY",
    "STATUS_UNKNOWN",
    "STATUS_RECOVERING",
    "STATUS_MAINTENANCE",
    "STATUS_OVERLOADED",
    "SEVERITY_CRITICAL",
    "SEVERITY_HIGH",
    "SEVERITY_MEDIUM",
    "SEVERITY_LOW",
    "SEVERITY_INFO",
    "RISK_CRITICAL",
    "RISK_HIGH",
    "RISK_MODERATE",
    "RISK_LOW",
    "RISK_NEGLIGIBLE",
    "diagnostics",
    "get_diagnostics",
    "self_test",
]


# ============================================================
# END
# ============================================================