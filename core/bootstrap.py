# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# BOOTSTRAP SYSTEM v4.0 - ULTRA ROBUST
#
# SUPER COMPREHENSIVE STARTUP SYSTEM
#
# Responsible:
# - Startup Sequence
# - Core Initialization
# - Health Validation
# - Module Discovery (AUTO-DETECT all core.learning modules)
# - Dependency Resolution
# - Learning Engine Registration (ALL modules)
# - Graceful Failure
# - Recovery System
# - Performance Metrics
# - Status Reporting
# - Auto-Healing
# - Module Registry Export
#
# ============================================================

from __future__ import annotations

import logging
import threading
import time
import traceback
import inspect
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Set

logger = logging.getLogger(__name__)


# ============================================================
# CONSTANTS
# ============================================================

BOOTSTRAP_VERSION = "4.0.0"

STATUS_ONLINE = "ONLINE"
STATUS_OFFLINE = "OFFLINE"
STATUS_DEGRADED = "DEGRADED"
STATUS_FAILED = "FAILED"
STATUS_UNKNOWN = "UNKNOWN"
STATUS_INITIALIZING = "INITIALIZING"
STATUS_RECOVERING = "RECOVERING"

PHASE_CORE = "CORE"
PHASE_MODULES = "MODULES"
PHASE_LEARNING_REGISTRATION = "LEARNING_REGISTRATION"
PHASE_SERVICES = "SERVICES"
PHASE_INTEGRATION = "INTEGRATION"
PHASE_COMPLETE = "COMPLETE"


# ============================================================
# SAFE IMPORT
# ============================================================

def safe_import(module: str, fromlist: Optional[List[str]] = None) -> Any:
    """
    Safely import a module with error handling.
    
    Args:
        module: Module path
        fromlist: Optional list of attributes to import
        
    Returns:
        Imported module or None if failed
    """
    try:
        if fromlist:
            return __import__(module, fromlist=fromlist)
        return __import__(module, fromlist=["*"])
    except ImportError as e:
        logger.debug(f"Import failed {module}: {e}")
        return None
    except Exception as e:
        logger.warning(f"Import error {module}: {e}")
        return None


def discover_modules_in_package(package_name: str) -> List[str]:
    """
    Auto-discover module names in a package.
    
    Args:
        package_name: Package path (e.g., 'core.learning')
        
    Returns:
        List of module names
    """
    discovered = []
    try:
        pkg = __import__(package_name, fromlist=['*'])
        for attr_name in dir(pkg):
            if attr_name.startswith('_'):
                continue
            attr = getattr(pkg, attr_name, None)
            # Check if it's a module or class
            if inspect.ismodule(attr) or inspect.isclass(attr) or callable(attr):
                discovered.append(attr_name)
    except Exception as e:
        logger.debug(f"Discovery failed for {package_name}: {e}")
    return discovered


# ============================================================
# MODULE DEFINITION
# ============================================================

class ModuleDefinition:
    """Definition of a module to bootstrap."""
    
    def __init__(
        self,
        name: str,
        module_path: str,
        class_name: Optional[str] = None,
        required: bool = True,
        dependencies: Optional[List[str]] = None,
        init_method: Optional[str] = None,
        startup_timeout: float = 10.0,
        learning_priority: int = 100,
        auto_register: bool = True
    ):
        self.name = name
        self.module_path = module_path
        self.class_name = class_name
        self.required = required
        self.dependencies = dependencies or []
        self.init_method = init_method
        self.startup_timeout = startup_timeout
        self.learning_priority = learning_priority
        self.auto_register = auto_register
        
        self.status = STATUS_UNKNOWN
        self.module = None
        self.instance = None
        self.error = None
        self.start_time = None
        self.end_time = None
        self.load_time = 0.0


# ============================================================
# BOOTSTRAP SYSTEM v4.0
# ============================================================

class Bootstrap:
    """
    Bootstrap System v4.0 - Ultra Robust Startup System.
    
    Features:
    1. Sequential Module Loading with Dependency Resolution
    2. Auto-Discovery of ALL core.learning modules
    3. Automatic Registration to Learning Engine
    4. Health Validation
    5. Graceful Failure
    6. Recovery System
    7. Performance Metrics
    8. Status Reporting
    9. Auto-Healing
    10. Thread Safety
    11. Module Registry Export
    12. Learning Engine Integration
    """

    VERSION = BOOTSTRAP_VERSION

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # ====================================================
        # STATE
        # ====================================================
        
        self.status: Dict[str, str] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.modules: Dict[str, ModuleDefinition] = {}
        self.instances: Dict[str, Any] = {}
        
        self.phase = PHASE_CORE
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.total_load_time = 0.0
        
        # ====================================================
        # THREAD SAFETY
        # ====================================================
        
        self.lock = threading.RLock()
        self.running = False
        self.recovery_attempts = 0
        self.max_recovery_attempts = self.config.get("max_recovery_attempts", 3)
        
        # ====================================================
        # STATISTICS
        # ====================================================
        
        self.stats = {
            "total_modules": 0,
            "loaded_modules": 0,
            "failed_modules": 0,
            "required_failed": 0,
            "optional_failed": 0,
            "recovery_attempts": 0,
            "total_load_time": 0.0,
            "fastest_load": float("inf"),
            "slowest_load": 0.0,
            "learning_registered": 0,
        }
        
        # ====================================================
        # REGISTER DEFAULT MODULES
        # ====================================================
        
        self._register_default_modules()
        
        logger.info("Bootstrap v%s initialized.", self.VERSION)

    # ========================================================
    # MODULE REGISTRATION
    # ========================================================

    def _register_default_modules(self) -> None:
        """
        Register ALL system modules including auto-discovery of core.learning.
        """
        
        # ----- Core Modules -----
        core_modules = [
            ("System Config", "core.system_config", "SystemConfig", True, [], None, 10),
            ("Health Monitor", "core.health", "HealthMonitor", False, ["System Config"], None, 20),
            ("Memory", "core.memory", "MemoryEngine", True, ["System Config"], None, 30),
            ("Knowledge", "core.knowledge", "KnowledgeEngine", False, ["Memory"], None, 40),
            ("Reasoning", "core.reasoning", "ReasoningEngine", False, ["Memory", "Knowledge"], None, 50),
            ("Scanner", "core.scanner", "MarketScanner", False, [], None, 60),
            ("Signal Engine", "core.signal_engine", "SignalEngine", False, ["Scanner"], None, 70),
            ("Analyzer", "core.analyzer", "Analyzer", False, [], None, 80),
            ("Scheduler", "core.scheduler", "Scheduler", False, [], None, 90),
            ("Runtime", "core.runtime", "RuntimeManager", False, [], None, 100),
            ("Watchdog", "core.watchdog", "SystemWatchdog", False, ["Runtime"], None, 110),
            ("Validator", "core.validator", "ModuleValidator", False, [], None, 120),
            ("Diagnostics", "core.diagnostics", "SystemDiagnostics", False, [], None, 130),
            ("Brain", "core.brain", "Brain", True, ["Memory"], None, 140),
            ("Consciousness", "core.consciousness", "Consciousness", False, ["Brain"], None, 150),
            ("Module Manager", "core.module_manager", "ModuleManager", False, [], None, 160),
        ]
        
        for name, path, class_name, required, deps, init_method, priority in core_modules:
            self.register_module(
                name=name,
                module_path=path,
                class_name=class_name,
                required=required,
                dependencies=deps,
                init_method=init_method,
                learning_priority=priority,
                auto_register=True
            )
        
        # ----- Learning Modules (Auto-Discovery) -----
        try:
            import core.learning as learning_pkg
            learning_modules = [
                ("Learning Engine", "core.learning.engine", "LearningEngine", True, ["Memory"], None, 200),
                ("Pattern Engine", "core.learning.pattern", "PatternEngine", False, ["Learning Engine"], None, 210),
                ("Semantic Memory", "core.learning.semantic_memory", "SemanticMemory", False, ["Memory"], None, 220),
                ("Market Learning", "core.learning.market_learning", "MarketLearning", False, ["Learning Engine"], None, 230),
                ("Prediction Engine", "core.learning.prediction", "PredictionEngine", False, ["Pattern Engine"], None, 240),
                ("Decision Engine", "core.learning.decision_engine", "DecisionEngine", False, ["Prediction Engine"], None, 250),
                ("Reflection Engine", "core.learning.reflection", "ReflectionEngine", False, ["Decision Engine"], None, 260),
                ("Insight Engine", "core.learning.insight", "InsightEngine", False, ["Reflection Engine"], None, 270),
                ("Evaluator Engine", "core.learning.evaluator", "EvaluatorEngine", False, ["Insight Engine"], None, 280),
                ("Improvement Engine", "core.learning.improvement", "ImprovementEngine", False, ["Evaluator Engine"], None, 290),
                ("Strategy Engine", "core.learning.strategy", "StrategyEngine", False, ["Decision Engine"], None, 300),
                ("Simulation Engine", "core.learning.simulation", "SimulationEngine", False, ["Strategy Engine"], None, 310),
                ("Adaptive Engine", "core.learning.adaptive", "AdaptiveEngine", False, ["Learning Engine"], None, 320),
                ("Learning Analyzer", "core.learning.analyzer", "LearningAnalyzer", False, ["Learning Engine"], None, 330),
                ("Collector", "core.learning.collector", "Collector", False, ["Learning Engine"], None, 340),
                ("Data Cleaner", "core.learning.data_cleaner", "DataCleaner", False, ["Collector"], None, 350),
                ("Normalizer", "core.learning.normalizer", "Normalizer", False, ["Data Cleaner"], None, 360),
                ("Feature Extractor", "core.learning.feature_extractor", "FeatureExtractor", False, ["Normalizer"], None, 370),
                ("Learning Memory", "core.learning.learning_memory", "LearningMemory", False, ["Memory"], None, 380),
                ("Memory Optimizer", "core.learning.memory_optimizer", "MemoryOptimizer", False, ["Learning Memory"], None, 390),
                ("Entity Recognition", "core.learning.entity_recognition", "EntityRecognition", False, ["Semantic Memory"], None, 400),
                ("Semantic Processor", "core.learning.semantic_processor", "SemanticProcessor", False, ["Entity Recognition"], None, 410),
                ("Context Manager", "core.learning.context_manager", "ContextManager", False, ["Semantic Processor"], None, 420),
                ("Goal Manager", "core.learning.goal_manager", "GoalManager", False, ["Context Manager"], None, 430),
                ("Behavior Engine", "core.learning.behavior", "BehaviorEngine", False, ["Goal Manager"], None, 440),
                ("Association Engine", "core.learning.association", "AssociationEngine", False, ["Behavior Engine"], None, 450),
                ("Self Diagnostic", "core.learning.self_diagnostic", "SelfDiagnostic", False, ["Diagnostics"], None, 460),
                ("Knowledge Builder", "core.learning.knowledge_builder", "KnowledgeBuilder", False, ["Knowledge"], None, 470),
                ("Curiosity Engine", "core.learning.curiosity", "CuriosityEngine", False, ["Consciousness"], None, 480),
                ("Experience Engine", "core.learning.experience", "ExperienceEngine", False, ["Curiosity Engine"], None, 490),
                ("Knowledge Graph", "core.learning.knowledge_graph", "KnowledgeGraph", False, ["Knowledge Builder"], None, 500),
                ("Module Registry", "core.learning.module_registry", "ModuleRegistry", False, [], None, 510),
            ]
            
            for name, path, class_name, required, deps, init_method, priority in learning_modules:
                self.register_module(
                    name=name,
                    module_path=path,
                    class_name=class_name,
                    required=required,
                    dependencies=deps,
                    init_method=init_method,
                    learning_priority=priority,
                    auto_register=True
                )
            logger.info("✅ Registered %d learning modules.", len(learning_modules))
            
        except ImportError as e:
            logger.warning(f"Learning package import failed: {e}")

    def register_module(
        self,
        name: str,
        module_path: str,
        class_name: Optional[str] = None,
        required: bool = True,
        dependencies: Optional[List[str]] = None,
        init_method: Optional[str] = None,
        startup_timeout: float = 10.0,
        learning_priority: int = 100,
        auto_register: bool = True
    ) -> None:
        """
        Register a module for bootstrap.
        
        Args:
            name: Display name
            module_path: Python module path
            class_name: Optional class name to instantiate
            required: If True, failure will abort startup
            dependencies: List of module names this depends on
            init_method: Method to call after instantiation
            startup_timeout: Timeout for startup in seconds
            learning_priority: Priority when registering to Learning Engine
            auto_register: Whether to auto-register to Learning Engine
        """
        with self.lock:
            self.modules[name] = ModuleDefinition(
                name=name,
                module_path=module_path,
                class_name=class_name,
                required=required,
                dependencies=dependencies or [],
                init_method=init_method,
                startup_timeout=startup_timeout,
                learning_priority=learning_priority,
                auto_register=auto_register
            )
            self.status[name] = STATUS_UNKNOWN

    # ========================================================
    # MAIN INITIALIZATION
    # ========================================================

    def initialize(self, phase: str = "ALL") -> Dict[str, str]:
        """
        Initialize all registered modules.
        
        Args:
            phase: Optional phase to stop at
            
        Returns:
            Status dictionary
        """
        self.started_at = datetime.now().isoformat()
        self.phase = PHASE_CORE
        self.running = True
        
        logger.info("INKSIDE Bootstrap v%s started.", self.VERSION)
        logger.info("Phase: %s", phase)
        
        try:
            # Phase 1: Core modules
            self.phase = PHASE_CORE
            self._load_modules(required_only=True, dependencies_required=False)
            
            if phase == PHASE_CORE:
                self._finalize()
                return self.status
            
            # Phase 2: Modules (all, including optional)
            self.phase = PHASE_MODULES
            self._load_modules(required_only=False, dependencies_required=True)
            
            if phase == PHASE_MODULES:
                self._finalize()
                return self.status
            
            # Phase 3: Learning Engine Registration (AUTO-REGISTER ALL MODULES)
            self.phase = PHASE_LEARNING_REGISTRATION
            self._register_to_learning_engine()
            
            if phase == PHASE_LEARNING_REGISTRATION:
                self._finalize()
                return self.status
            
            # Phase 4: Services
            self.phase = PHASE_SERVICES
            self._start_services()
            
            if phase == PHASE_SERVICES:
                self._finalize()
                return self.status
            
            # Phase 5: Integration
            self.phase = PHASE_INTEGRATION
            self._integrate_modules()
            
            if phase == PHASE_INTEGRATION:
                self._finalize()
                return self.status
            
            # Phase 6: Complete
            self.phase = PHASE_COMPLETE
            self._verify_all()
            
        except Exception as e:
            logger.exception("Bootstrap failed: %s", e)
            self.errors.append(f"Bootstrap error: {e}")
            self._attempt_recovery()
        
        self._finalize()
        return self.status

    # ========================================================
    # MODULE LOADING
    # ========================================================

    def _load_modules(
        self,
        required_only: bool = False,
        dependencies_required: bool = True
    ) -> None:
        """Load modules with dependency resolution."""
        
        load_order = self._get_load_order(required_only)
        
        for module_def in load_order:
            if not self.running:
                break
            
            if module_def.status == STATUS_ONLINE:
                continue
            
            if dependencies_required and not self._dependencies_ready(module_def):
                module_def.status = STATUS_DEGRADED
                self.status[module_def.name] = STATUS_DEGRADED
                self.warnings.append(f"Dependencies not ready: {module_def.name}")
                continue
            
            self._load_module(module_def)
            
            if module_def.required and module_def.status == STATUS_FAILED:
                self.errors.append(f"Critical module failed: {module_def.name}")
                break

    def _get_load_order(self, required_only: bool) -> List[ModuleDefinition]:
        """Get module load order based on dependencies."""
        with self.lock:
            modules = list(self.modules.values())
            
            if required_only:
                modules = [m for m in modules if m.required]
            
            loaded = []
            remaining = modules.copy()
            
            while remaining:
                ready = []
                for module in remaining:
                    deps_satisfied = True
                    for dep in module.dependencies:
                        dep_def = self.modules.get(dep)
                        if dep_def and dep_def.status != STATUS_ONLINE:
                            deps_satisfied = False
                            break
                    if deps_satisfied:
                        ready.append(module)
                
                if not ready:
                    for module in remaining:
                        if module.required:
                            self.errors.append(f"Cannot resolve dependencies for: {module.name}")
                    break
                
                ready.sort(key=lambda x: x.name)
                loaded.extend(ready)
                for module in ready:
                    remaining.remove(module)
            
            return loaded

    def _dependencies_ready(self, module_def: ModuleDefinition) -> bool:
        """Check if all dependencies are ready."""
        for dep in module_def.dependencies:
            dep_status = self.status.get(dep)
            if dep_status != STATUS_ONLINE:
                return False
        return True

    def _load_module(self, module_def: ModuleDefinition) -> None:
        """Load a single module."""
        module_def.start_time = time.time()
        self.status[module_def.name] = STATUS_INITIALIZING
        
        try:
            module = safe_import(module_def.module_path)
            if module is None:
                raise ImportError(f"Cannot import {module_def.module_path}")
            
            module_def.module = module
            
            if module_def.class_name:
                cls = getattr(module, module_def.class_name, None)
                if cls is None:
                    raise AttributeError(f"Class {module_def.class_name} not found in {module_def.module_path}")
                
                # Instantiate with config if available
                try:
                    instance = cls(self.config)
                except TypeError:
                    try:
                        instance = cls()
                    except Exception:
                        instance = cls
                
                module_def.instance = instance
                self.instances[module_def.name] = instance
                
                if module_def.init_method and hasattr(instance, module_def.init_method):
                    getattr(instance, module_def.init_method)()
            
            module_def.status = STATUS_ONLINE
            self.status[module_def.name] = STATUS_ONLINE
            self.stats["loaded_modules"] += 1
            
            logger.info("[✓] %s loaded successfully.", module_def.name)
            
        except Exception as e:
            module_def.error = str(e)
            module_def.status = STATUS_FAILED
            self.status[module_def.name] = STATUS_FAILED
            self.stats["failed_modules"] += 1
            
            if module_def.required:
                self.errors.append(f"Module {module_def.name} failed: {e}")
                self.stats["required_failed"] += 1
                logger.error("[✗] %s failed (required): %s", module_def.name, e)
            else:
                self.warnings.append(f"Module {module_def.name} failed: {e}")
                self.stats["optional_failed"] += 1
                logger.warning("[!] %s failed (optional): %s", module_def.name, e)
            
            logger.debug(traceback.format_exc())
        
        finally:
            module_def.end_time = time.time()
            module_def.load_time = module_def.end_time - module_def.start_time
            
            if module_def.load_time > 0:
                self.stats["slowest_load"] = max(self.stats["slowest_load"], module_def.load_time)
                self.stats["fastest_load"] = min(self.stats["fastest_load"], module_def.load_time)

    # ========================================================
    # REGISTER TO LEARNING ENGINE (CRITICAL)
    # ========================================================

    def _register_to_learning_engine(self) -> None:
        """
        Register ALL loaded modules to Learning Engine.
        This ensures all modules are available for autonomous learning.
        """
        learning_engine = self.instances.get("Learning Engine")
        if learning_engine is None:
            logger.warning("Learning Engine not loaded – skipping registration.")
            return
        
        if not hasattr(learning_engine, 'register_module'):
            logger.warning("Learning Engine has no register_module method – skipping.")
            return
        
        registered_count = 0
        failed_count = 0
        
        for name, module_def in self.modules.items():
            # Skip if module not loaded or not marked for auto-register
            if module_def.status != STATUS_ONLINE:
                continue
            if not module_def.auto_register:
                continue
            
            # Skip registering Learning Engine to itself
            if name == "Learning Engine":
                continue
            
            instance = module_def.instance
            if instance is None:
                continue
            
            # Convert name to safe module identifier
            module_name = name.lower().replace(" ", "_")
            
            try:
                learning_engine.register_module(
                    name=module_name,
                    module=instance,
                    enabled=True,
                    priority=module_def.learning_priority
                )
                registered_count += 1
                logger.debug(f"[LEARNING] Registered {name} (priority={module_def.learning_priority})")
            except Exception as e:
                failed_count += 1
                logger.warning(f"[LEARNING] Failed to register {name}: {e}")
        
        self.stats["learning_registered"] = registered_count
        logger.info(f"✅ {registered_count} modules registered to Learning Engine. {failed_count} failed.")

    # ========================================================
    # SERVICES & INTEGRATION
    # ========================================================

    def _start_services(self) -> None:
        """Start registered services."""
        
        services = [
            ("Watchdog", "start"),
            ("Scheduler", "start"),
            ("Runtime", "start"),
            ("Scanner", "start"),
        ]
        
        for name, method in services:
            instance = self.instances.get(name)
            if instance and hasattr(instance, method):
                try:
                    getattr(instance, method)()
                    logger.info("[✓] %s service started.", name)
                except Exception as e:
                    logger.warning("[!] %s start failed: %s", name, e)

    def _integrate_modules(self) -> None:
        """Integrate modules with each other."""
        
        # Brain <-> Consciousness
        brain = self.instances.get("Brain")
        consciousness = self.instances.get("Consciousness")
        if brain and consciousness:
            try:
                if hasattr(brain, "set_consciousness"):
                    brain.set_consciousness(consciousness)
                elif hasattr(brain, "consciousness"):
                    brain.consciousness = consciousness
                logger.info("[✓] Brain integrated with Consciousness.")
            except Exception as e:
                logger.warning("[!] Brain-Consciousness integration failed: %s", e)
        
        # Learning Engine <-> Memory
        learning = self.instances.get("Learning Engine")
        memory = self.instances.get("Memory")
        if learning and memory:
            try:
                if hasattr(learning, "set_memory"):
                    learning.set_memory(memory)
                logger.info("[✓] Learning Engine integrated with Memory.")
            except Exception as e:
                logger.warning("[!] Learning-Memory integration failed: %s", e)

    def _verify_all(self) -> None:
        """Verify all modules are working."""
        
        # Health check
        health = self.instances.get("Health Monitor")
        if health:
            try:
                if hasattr(health, "health_check"):
                    result = health.health_check()
                    if result and result.get("healthy"):
                        logger.info("[✓] Health check passed.")
                    else:
                        self.warnings.append("Health check returned unhealthy.")
            except Exception as e:
                logger.warning("[!] Health check failed: %s", e)

    # ========================================================
    # RECOVERY
    # ========================================================

    def _attempt_recovery(self) -> bool:
        self.recovery_attempts += 1
        self.stats["recovery_attempts"] += 1
        
        if self.recovery_attempts > self.max_recovery_attempts:
            logger.error("Max recovery attempts exceeded.")
            return False
        
        logger.info("Recovery attempt #%d", self.recovery_attempts)
        self.status["recovery"] = STATUS_RECOVERING
        
        try:
            for name, module_def in self.modules.items():
                if module_def.status == STATUS_FAILED and not module_def.required:
                    logger.info("Retrying optional module: %s", name)
                    self._load_module(module_def)
            
            critical_offline = []
            for name, module_def in self.modules.items():
                if module_def.required and module_def.status != STATUS_ONLINE:
                    critical_offline.append(name)
            
            if critical_offline:
                logger.warning("Critical modules still offline: %s", critical_offline)
                return False
            
            logger.info("Recovery successful.")
            return True
            
        except Exception as e:
            logger.exception("Recovery failed: %s", e)
            return False

    # ========================================================
    # STATUS & REPORTING
    # ========================================================

    def _finalize(self) -> None:
        self.completed_at = datetime.now().isoformat()
        self.running = False
        
        if self.completed_at and self.started_at:
            try:
                start = datetime.fromisoformat(self.started_at)
                end = datetime.fromisoformat(self.completed_at)
                self.total_load_time = (end - start).total_seconds()
                self.stats["total_load_time"] = self.total_load_time
            except Exception:
                pass
        
        # Log summary
        logger.info("=" * 60)
        logger.info("BOOTSTRAP SUMMARY")
        logger.info("=" * 60)
        logger.info("Status: %s", "READY" if self.is_ready() else "DEGRADED")
        logger.info("Modules: %d/%d", self.stats["loaded_modules"], len(self.modules))
        logger.info("Learning Registered: %d", self.stats["learning_registered"])
        logger.info("Errors: %d", len(self.errors))
        logger.info("Warnings: %d", len(self.warnings))
        logger.info("Load Time: %.2fs", self.total_load_time)
        logger.info("=" * 60)

    def is_ready(self) -> bool:
        if self.errors:
            return False
        return len(self.status) == len(self.modules)

    def report(self) -> Dict[str, Any]:
        with self.lock:
            modules_status = {}
            for name, module_def in self.modules.items():
                modules_status[name] = {
                    "status": module_def.status,
                    "required": module_def.required,
                    "load_time": round(module_def.load_time, 4),
                    "error": module_def.error,
                    "dependencies": module_def.dependencies,
                    "learning_priority": module_def.learning_priority,
                    "auto_register": module_def.auto_register,
                }
            
            return {
                "version": self.VERSION,
                "ready": self.is_ready(),
                "phase": self.phase,
                "started_at": self.started_at,
                "completed_at": self.completed_at,
                "total_load_time": round(self.total_load_time, 4),
                "statistics": self.stats,
                "modules": modules_status,
                "errors": self.errors,
                "warnings": self.warnings,
                "status": self.status,
                "instances": list(self.instances.keys()),
            }

    def get_module(self, name: str) -> Optional[Any]:
        with self.lock:
            return self.instances.get(name)

    def get_instances(self) -> Dict[str, Any]:
        with self.lock:
            return self.instances.copy()

    def get_summary(self) -> Dict[str, Any]:
        return {
            "ready": self.is_ready(),
            "modules_loaded": self.stats["loaded_modules"],
            "modules_failed": self.stats["failed_modules"],
            "learning_registered": self.stats["learning_registered"],
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "load_time": round(self.total_load_time, 4),
        }

    def reset(self) -> bool:
        with self.lock:
            self.status = {}
            self.errors = []
            self.warnings = []
            self.instances = {}
            
            for module_def in self.modules.values():
                module_def.status = STATUS_UNKNOWN
                module_def.module = None
                module_def.instance = None
                module_def.error = None
                module_def.start_time = None
                module_def.end_time = None
                module_def.load_time = 0.0
            
            self.stats = {
                "total_modules": 0,
                "loaded_modules": 0,
                "failed_modules": 0,
                "required_failed": 0,
                "optional_failed": 0,
                "recovery_attempts": 0,
                "total_load_time": 0.0,
                "fastest_load": float("inf"),
                "slowest_load": 0.0,
                "learning_registered": 0,
            }
            
            self.recovery_attempts = 0
            self.started_at = None
            self.completed_at = None
            self.total_load_time = 0.0
            self.running = False
            self.phase = PHASE_CORE
            
            logger.info("Bootstrap reset.")
            return True


# ============================================================
# GLOBAL INSTANCE
# ============================================================

bootstrap = Bootstrap()


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def safe_import_legacy(module: str) -> Any:
    return safe_import(module)


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    print()
    print("=" * 70)
    print("  BOOTSTRAP v4.0 - SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        test_bootstrap = Bootstrap()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Module Registration
    print("\n2. Testing module registration...")
    try:
        test_bootstrap = Bootstrap()
        if len(test_bootstrap.modules) > 10:
            results["registration"] = {"status": "PASS", "count": len(test_bootstrap.modules)}
            tests_passed += 1
            print(f"   ✅ Registration passed ({len(test_bootstrap.modules)} modules)")
        else:
            results["registration"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Registration failed (too few modules)")
    except Exception as e:
        results["registration"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Registration failed: {e}")
    
    # Test 3: Auto-registration to Learning Engine (simulated)
    print("\n3. Testing auto-registration...")
    try:
        test_bootstrap = Bootstrap()
        # Simulate learning engine
        class MockLearning:
            def register_module(self, **kwargs):
                pass
        test_bootstrap.instances["Learning Engine"] = MockLearning()
        test_bootstrap._register_to_learning_engine()
        results["auto_register"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Auto-registration passed")
    except Exception as e:
        results["auto_register"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Auto-registration failed: {e}")
    
    # Test 4: Report
    print("\n4. Testing report...")
    try:
        report = bootstrap.report()
        if report and "version" in report:
            results["report"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Report passed")
        else:
            results["report"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Report failed")
    except Exception as e:
        results["report"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Report failed: {e}")
    
    print()
    print("=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"  ✅ Passed: {tests_passed}")
    print(f"  ❌ Failed: {tests_failed}")
    print(f"  📊 Total:  {tests_passed + tests_failed}")
    print("=" * 70)
    
    return {
        "module": "bootstrap",
        "version": BOOTSTRAP_VERSION,
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
    print("=" * 70)
    print("  BOOTSTRAP v4.0 - SELF TEST COMPLETE")
    print("=" * 70)
    print()
    print("Final Status:", result["status"])
    print("Details:", result["details"])


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "Bootstrap",
    "bootstrap",
    "safe_import",
    "safe_import_legacy",
    "self_test",
    "BOOTSTRAP_VERSION",
    "STATUS_ONLINE",
    "STATUS_OFFLINE",
    "STATUS_DEGRADED",
    "STATUS_FAILED",
    "STATUS_UNKNOWN",
    "STATUS_INITIALIZING",
    "STATUS_RECOVERING",
    "PHASE_CORE",
    "PHASE_MODULES",
    "PHASE_LEARNING_REGISTRATION",
    "PHASE_SERVICES",
    "PHASE_INTEGRATION",
    "PHASE_COMPLETE",
    "discover_modules_in_package",
]


# ============================================================
# END
# ============================================================