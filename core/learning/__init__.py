# ============================================================
# core/learning/__init__.py
# LEARNING PACKAGE - ALL LEARNING MODULES
# ============================================================

"""
LEARNING PACKAGE

Cara import:
    from core.learning import (
        LearningEngine, learning_engine,
        PatternEngine, pattern,
        PredictionEngine, prediction_engine,
        ...
    )
"""

__version__ = "2.1.2"
__all__ = []


# ============================================================
# ENGINE & CORE
# ============================================================

try:
    from .engine import (
        LearningEngine,
        learning_engine,
        SafeSerializer,
        LearningContext,
        ModuleSpec,
        ModuleExecutor,
        KERNEL_VERSION,
        ENGINE_VERSION,
        STATE_IDLE,
        STATE_RUNNING,
        STATE_SUCCESS,
        STATE_PARTIAL,
        STATE_ERROR,
        STATE_TIMEOUT,
        STATE_DISABLED,
        STATE_DEPENDENCY_ERROR,
        STATE_NO_OUTPUT,
        STATE_CIRCUIT_OPEN,
        STATE_SHUTDOWN,
    )
    LEARNING_ENGINE_AVAILABLE = True
    __all__ += [
        "LearningEngine", "learning_engine",
        "SafeSerializer", "LearningContext",
        "ModuleSpec", "ModuleExecutor",
        "KERNEL_VERSION", "ENGINE_VERSION",
        "STATE_IDLE", "STATE_RUNNING", "STATE_SUCCESS",
        "STATE_PARTIAL", "STATE_ERROR", "STATE_TIMEOUT",
        "STATE_DISABLED", "STATE_DEPENDENCY_ERROR",
        "STATE_NO_OUTPUT", "STATE_CIRCUIT_OPEN",
        "STATE_SHUTDOWN",
        "LEARNING_ENGINE_AVAILABLE",
    ]
except ImportError:
    LEARNING_ENGINE_AVAILABLE = False
    LearningEngine = None
    learning_engine = None
    SafeSerializer = None
    LearningContext = None
    ModuleSpec = None
    ModuleExecutor = None
    KERNEL_VERSION = "N/A"
    ENGINE_VERSION = "N/A"
    STATE_IDLE = "IDLE"
    STATE_RUNNING = "RUNNING"
    STATE_SUCCESS = "SUCCESS"
    STATE_PARTIAL = "PARTIAL"
    STATE_ERROR = "ERROR"
    STATE_TIMEOUT = "TIMEOUT"
    STATE_DISABLED = "DISABLED"
    STATE_DEPENDENCY_ERROR = "DEPENDENCY_ERROR"
    STATE_NO_OUTPUT = "NO_OUTPUT"
    STATE_CIRCUIT_OPEN = "CIRCUIT_OPEN"
    STATE_SHUTDOWN = "SHUTDOWN"


# ============================================================
# PATTERN
# ============================================================

try:
    from .pattern import PatternEngine, pattern
    PATTERN_AVAILABLE = True
    __all__ += ["PatternEngine", "pattern", "PATTERN_AVAILABLE"]
except ImportError:
    PATTERN_AVAILABLE = False
    PatternEngine = None
    pattern = None


# ============================================================
# PREDICTION
# ============================================================

try:
    from .prediction import PredictionEngine, prediction_engine
    PREDICTION_AVAILABLE = True
    __all__ += ["PredictionEngine", "prediction_engine", "PREDICTION_AVAILABLE"]
except ImportError:
    PREDICTION_AVAILABLE = False
    PredictionEngine = None
    prediction_engine = None


# ============================================================
# REASONING ENGINE - DISABLED (pakai core/reasoning.py)
# ============================================================

# ReasoningEngine telah dipindahkan ke core/reasoning.py
# Gunakan import dari core.reasoning untuk fungsionalitas reasoning
REASONING_ENGINE_AVAILABLE = False
ReasoningEngine = None
reasoning_engine = None


# ============================================================
# DECISION ENGINE
# ============================================================

try:
    from .decision_engine import DecisionEngine, decision_engine
    DECISION_ENGINE_AVAILABLE = True
    __all__ += ["DecisionEngine", "decision_engine", "DECISION_ENGINE_AVAILABLE"]
except ImportError:
    DECISION_ENGINE_AVAILABLE = False
    DecisionEngine = None
    decision_engine = None


# ============================================================
# SEMANTIC MEMORY
# ============================================================

try:
    from .semantic_memory import SemanticMemory, semantic_memory
    SEMANTIC_MEMORY_AVAILABLE = True
    __all__ += ["SemanticMemory", "semantic_memory", "SEMANTIC_MEMORY_AVAILABLE"]
except ImportError:
    SEMANTIC_MEMORY_AVAILABLE = False
    SemanticMemory = None
    semantic_memory = None


# ============================================================
# LEARNING MEMORY
# ============================================================

try:
    from .learning_memory import LearningMemory, learning_memory
    LEARNING_MEMORY_AVAILABLE = True
    __all__ += ["LearningMemory", "learning_memory", "LEARNING_MEMORY_AVAILABLE"]
except ImportError:
    LEARNING_MEMORY_AVAILABLE = False
    LearningMemory = None
    learning_memory = None


# ============================================================
# MEMORY OPTIMIZER
# ============================================================

try:
    from .memory_optimizer import MemoryOptimizer, memory_optimizer
    MEMORY_OPTIMIZER_AVAILABLE = True
    __all__ += ["MemoryOptimizer", "memory_optimizer", "MEMORY_OPTIMIZER_AVAILABLE"]
except ImportError:
    MEMORY_OPTIMIZER_AVAILABLE = False
    MemoryOptimizer = None
    memory_optimizer = None


# ============================================================
# ENTITY RECOGNITION
# ============================================================

try:
    from .entity_recognition import EntityRecognition, entity_recognition
    ENTITY_RECOGNITION_AVAILABLE = True
    __all__ += ["EntityRecognition", "entity_recognition", "ENTITY_RECOGNITION_AVAILABLE"]
except ImportError:
    ENTITY_RECOGNITION_AVAILABLE = False
    EntityRecognition = None
    entity_recognition = None


# ============================================================
# SEMANTIC PROCESSOR
# ============================================================

try:
    from .semantic_processor import SemanticProcessor, semantic_processor
    SEMANTIC_PROCESSOR_AVAILABLE = True
    __all__ += ["SemanticProcessor", "semantic_processor", "SEMANTIC_PROCESSOR_AVAILABLE"]
except ImportError:
    SEMANTIC_PROCESSOR_AVAILABLE = False
    SemanticProcessor = None
    semantic_processor = None


# ============================================================
# CONTEXT MANAGER
# ============================================================

try:
    from .context_manager import ContextManager, context_manager
    CONTEXT_MANAGER_AVAILABLE = True
    __all__ += ["ContextManager", "context_manager", "CONTEXT_MANAGER_AVAILABLE"]
except ImportError:
    CONTEXT_MANAGER_AVAILABLE = False
    ContextManager = None
    context_manager = None


# ============================================================
# GOAL MANAGER
# ============================================================

try:
    from .goal_manager import GoalManager, goal_manager
    GOAL_MANAGER_AVAILABLE = True
    __all__ += ["GoalManager", "goal_manager", "GOAL_MANAGER_AVAILABLE"]
except ImportError:
    GOAL_MANAGER_AVAILABLE = False
    GoalManager = None
    goal_manager = None


# ============================================================
# REFLECTION
# ============================================================

try:
    from .reflection import ReflectionEngine, reflection_engine
    REFLECTION_AVAILABLE = True
    __all__ += ["ReflectionEngine", "reflection_engine", "REFLECTION_AVAILABLE"]
except ImportError:
    REFLECTION_AVAILABLE = False
    ReflectionEngine = None
    reflection_engine = None


# ============================================================
# INSIGHT
# ============================================================

try:
    from .insight import InsightEngine, insight_engine
    INSIGHT_AVAILABLE = True
    __all__ += ["InsightEngine", "insight_engine", "INSIGHT_AVAILABLE"]
except ImportError:
    INSIGHT_AVAILABLE = False
    InsightEngine = None
    insight_engine = None


# ============================================================
# BEHAVIOR
# ============================================================

try:
    from .behavior import BehaviorEngine, behavior_engine
    BEHAVIOR_AVAILABLE = True
    __all__ += ["BehaviorEngine", "behavior_engine", "BEHAVIOR_AVAILABLE"]
except ImportError:
    BEHAVIOR_AVAILABLE = False
    BehaviorEngine = None
    behavior_engine = None


# ============================================================
# ASSOCIATION
# ============================================================

try:
    from .association import AssociationEngine, association_engine
    ASSOCIATION_AVAILABLE = True
    __all__ += ["AssociationEngine", "association_engine", "ASSOCIATION_AVAILABLE"]
except ImportError:
    ASSOCIATION_AVAILABLE = False
    AssociationEngine = None
    association_engine = None


# ============================================================
# SELF DIAGNOSTIC
# ============================================================

try:
    from .self_diagnostic import SelfDiagnostic, self_diagnostic
    SELF_DIAGNOSTIC_AVAILABLE = True
    __all__ += ["SelfDiagnostic", "self_diagnostic", "SELF_DIAGNOSTIC_AVAILABLE"]
except ImportError:
    SELF_DIAGNOSTIC_AVAILABLE = False
    SelfDiagnostic = None
    self_diagnostic = None


# ============================================================
# IMPROVEMENT
# ============================================================

try:
    from .improvement import ImprovementEngine, improvement_engine
    IMPROVEMENT_AVAILABLE = True
    __all__ += ["ImprovementEngine", "improvement_engine", "IMPROVEMENT_AVAILABLE"]
except ImportError:
    IMPROVEMENT_AVAILABLE = False
    ImprovementEngine = None
    improvement_engine = None


# ============================================================
# EVENT SYSTEM
# ============================================================

try:
    from .event import (
        EventBus,
        Event,
        EventHandler,
        EventResult,
        event_system,
        subscribe,
        unsubscribe,
        publish,
        emit,
        dispatch,
        publish_async,
        status,
        PRIORITY_LOW,
        PRIORITY_NORMAL,
        PRIORITY_HIGH,
        PRIORITY_CRITICAL,
        EVENT_VERSION,
        API_VERSION,
        EVENT_ENGINE_STARTED,
        EVENT_ENGINE_STOPPED,
        EVENT_ENGINE_ERROR,
        EVENT_LEARNING_STARTED,
        EVENT_LEARNING_COMPLETED,
        EVENT_LEARNING_ERROR,
        EVENT_MARKET_UPDATE,
        EVENT_MARKET_SIGNAL,
        EVENT_MARKET_ANALYSIS,
        EVENT_PATTERN_DETECTED,
        EVENT_DECISION_CREATED,
        EVENT_PREDICTION_CREATED,
        EVENT_STRATEGY_CREATED,
        EVENT_KNOWLEDGE_UPDATED,
        EVENT_MEMORY_UPDATED,
        EVENT_HEALTH_CHANGED,
        EVENT_DIAGNOSTIC_WARNING,
        EVENT_SYSTEM_WARNING,
        EVENT_SYSTEM_ERROR,
        EVENT_SYSTEM_SHUTDOWN,
        EVENT_DATA_COLLECTED,
        EVENT_DATA_CLEANED,
        EVENT_DATA_NORMALIZED,
        EVENT_FEATURES_EXTRACTED,
        EVENT_ENTITY_DETECTED,
        EVENT_SEMANTIC_PROCESSED,
        EVENT_EXPERIENCE_RECORDED,
        EVENT_INSIGHT_CREATED,
        EVENT_REFLECTION_CREATED,
        EVENT_LESSON_CREATED,
        EVENT_ADAPTATION_UPDATED,
        EVENT_SIMULATION_STARTED,
        EVENT_SIMULATION_COMPLETED,
        EVENT_SIMULATION_ERROR,
        EVENT_ARCHIVE_CREATED,
        EVENT_ARCHIVE_LOADED,
        EVENT_CONTEXT_UPDATED,
        EVENT_CONTEXT_RESET,
        test_event_system,
        test_event_system_advanced,
    )
    EVENT_AVAILABLE = True
    __all__ += [
        "EventBus", "Event", "EventHandler", "EventResult",
        "event_system",
        "subscribe", "unsubscribe", "publish", "emit", "dispatch",
        "publish_async", "status",
        "PRIORITY_LOW", "PRIORITY_NORMAL", "PRIORITY_HIGH", "PRIORITY_CRITICAL",
        "EVENT_VERSION", "API_VERSION",
        "EVENT_AVAILABLE",
        "EVENT_ENGINE_STARTED", "EVENT_ENGINE_STOPPED", "EVENT_ENGINE_ERROR",
        "EVENT_LEARNING_STARTED", "EVENT_LEARNING_COMPLETED", "EVENT_LEARNING_ERROR",
        "EVENT_MARKET_UPDATE", "EVENT_MARKET_SIGNAL", "EVENT_MARKET_ANALYSIS",
        "EVENT_PATTERN_DETECTED", "EVENT_DECISION_CREATED",
        "EVENT_PREDICTION_CREATED", "EVENT_STRATEGY_CREATED",
        "EVENT_KNOWLEDGE_UPDATED", "EVENT_MEMORY_UPDATED",
        "EVENT_HEALTH_CHANGED", "EVENT_DIAGNOSTIC_WARNING",
        "EVENT_SYSTEM_WARNING", "EVENT_SYSTEM_ERROR", "EVENT_SYSTEM_SHUTDOWN",
        "EVENT_DATA_COLLECTED", "EVENT_DATA_CLEANED",
        "EVENT_DATA_NORMALIZED", "EVENT_FEATURES_EXTRACTED",
        "EVENT_ENTITY_DETECTED", "EVENT_SEMANTIC_PROCESSED",
        "EVENT_EXPERIENCE_RECORDED", "EVENT_INSIGHT_CREATED",
        "EVENT_REFLECTION_CREATED", "EVENT_LESSON_CREATED",
        "EVENT_ADAPTATION_UPDATED",
        "EVENT_SIMULATION_STARTED", "EVENT_SIMULATION_COMPLETED",
        "EVENT_SIMULATION_ERROR",
        "EVENT_ARCHIVE_CREATED", "EVENT_ARCHIVE_LOADED",
        "EVENT_CONTEXT_UPDATED", "EVENT_CONTEXT_RESET",
        "test_event_system", "test_event_system_advanced",
    ]
except ImportError:
    EVENT_AVAILABLE = False
    EventBus = None
    Event = None
    EventHandler = None
    EventResult = None
    event_system = None
    subscribe = None
    unsubscribe = None
    publish = None
    emit = None
    dispatch = None
    publish_async = None
    status = None
    PRIORITY_LOW = 10
    PRIORITY_NORMAL = 50
    PRIORITY_HIGH = 75
    PRIORITY_CRITICAL = 100
    EVENT_VERSION = "N/A"
    API_VERSION = "N/A"
    EVENT_ENGINE_STARTED = "engine.started"
    EVENT_ENGINE_STOPPED = "engine.stopped"
    EVENT_ENGINE_ERROR = "engine.error"
    EVENT_LEARNING_STARTED = "learning.started"
    EVENT_LEARNING_COMPLETED = "learning.completed"
    EVENT_LEARNING_ERROR = "learning.error"
    EVENT_MARKET_UPDATE = "market.update"
    EVENT_MARKET_SIGNAL = "market.signal"
    EVENT_MARKET_ANALYSIS = "market.analysis"
    EVENT_PATTERN_DETECTED = "pattern.detected"
    EVENT_DECISION_CREATED = "decision.created"
    EVENT_PREDICTION_CREATED = "prediction.created"
    EVENT_STRATEGY_CREATED = "strategy.created"
    EVENT_KNOWLEDGE_UPDATED = "knowledge.updated"
    EVENT_MEMORY_UPDATED = "memory.updated"
    EVENT_HEALTH_CHANGED = "health.changed"
    EVENT_DIAGNOSTIC_WARNING = "diagnostic.warning"
    EVENT_SYSTEM_WARNING = "system.warning"
    EVENT_SYSTEM_ERROR = "system.error"
    EVENT_SYSTEM_SHUTDOWN = "system.shutdown"
    EVENT_DATA_COLLECTED = "data.collected"
    EVENT_DATA_CLEANED = "data.cleaned"
    EVENT_DATA_NORMALIZED = "data.normalized"
    EVENT_FEATURES_EXTRACTED = "features.extracted"
    EVENT_ENTITY_DETECTED = "entity.detected"
    EVENT_SEMANTIC_PROCESSED = "semantic.processed"
    EVENT_EXPERIENCE_RECORDED = "experience.recorded"
    EVENT_INSIGHT_CREATED = "insight.created"
    EVENT_REFLECTION_CREATED = "reflection.created"
    EVENT_LESSON_CREATED = "lesson.created"
    EVENT_ADAPTATION_UPDATED = "adaptation.updated"
    EVENT_SIMULATION_STARTED = "simulation.started"
    EVENT_SIMULATION_COMPLETED = "simulation.completed"
    EVENT_SIMULATION_ERROR = "simulation.error"
    EVENT_ARCHIVE_CREATED = "archive.created"
    EVENT_ARCHIVE_LOADED = "archive.loaded"
    EVENT_CONTEXT_UPDATED = "context.updated"
    EVENT_CONTEXT_RESET = "context.reset"
    test_event_system = None
    test_event_system_advanced = None


# ============================================================
# MARKET LEARNING
# ============================================================

try:
    from .market_learning import MarketLearning, market_learning
    MARKET_LEARNING_AVAILABLE = True
    __all__ += ["MarketLearning", "market_learning", "MARKET_LEARNING_AVAILABLE"]
except ImportError:
    MARKET_LEARNING_AVAILABLE = False
    MarketLearning = None
    market_learning = None


# ============================================================
# STRATEGY
# ============================================================

try:
    from .strategy import StrategyEngine, strategy_engine
    STRATEGY_AVAILABLE = True
    __all__ += ["StrategyEngine", "strategy_engine", "STRATEGY_AVAILABLE"]
except ImportError:
    STRATEGY_AVAILABLE = False
    StrategyEngine = None
    strategy_engine = None


# ============================================================
# SIMULATION
# ============================================================

try:
    from .simulation import SimulationEngine, simulation_engine
    SIMULATION_AVAILABLE = True
    __all__ += ["SimulationEngine", "simulation_engine", "SIMULATION_AVAILABLE"]
except ImportError:
    SIMULATION_AVAILABLE = False
    SimulationEngine = None
    simulation_engine = None


# ============================================================
# EVALUATOR
# ============================================================

try:
    from .evaluator import EvaluatorEngine, evaluator_engine
    EVALUATOR_AVAILABLE = True
    __all__ += ["EvaluatorEngine", "evaluator_engine", "EVALUATOR_AVAILABLE"]
except ImportError:
    EVALUATOR_AVAILABLE = False
    EvaluatorEngine = None
    evaluator_engine = None


# ============================================================
# ADAPTIVE
# ============================================================

try:
    from .adaptive import AdaptiveEngine, adaptive_engine
    ADAPTIVE_AVAILABLE = True
    __all__ += ["AdaptiveEngine", "adaptive_engine", "ADAPTIVE_AVAILABLE"]
except ImportError:
    ADAPTIVE_AVAILABLE = False
    AdaptiveEngine = None
    adaptive_engine = None


# ============================================================
# LEARNING ANALYZER
# ============================================================

try:
    from .analyzer import LearningAnalyzer, learning_analyzer
    LEARNING_ANALYZER_AVAILABLE = True
    __all__ += ["LearningAnalyzer", "learning_analyzer", "LEARNING_ANALYZER_AVAILABLE"]
except ImportError:
    LEARNING_ANALYZER_AVAILABLE = False
    LearningAnalyzer = None
    learning_analyzer = None


# ============================================================
# DATA PIPELINE
# ============================================================

try:
    from .collector import Collector
    from .data_cleaner import DataCleaner
    from .normalizer import Normalizer
    from .feature_extractor import FeatureExtractor
    DATA_PIPELINE_AVAILABLE = True
    __all__ += [
        "Collector", "DataCleaner",
        "Normalizer", "FeatureExtractor",
        "DATA_PIPELINE_AVAILABLE",
    ]
except ImportError:
    DATA_PIPELINE_AVAILABLE = False
    Collector = None
    DataCleaner = None
    Normalizer = None
    FeatureExtractor = None


# ============================================================
# ARCHIVE MANAGER
# ============================================================

try:
    from .archive_manager import ArchiveManager, archive_manager
    ARCHIVE_AVAILABLE = True
    __all__ += ["ArchiveManager", "archive_manager", "ARCHIVE_AVAILABLE"]
except ImportError:
    ARCHIVE_AVAILABLE = False
    ArchiveManager = None
    archive_manager = None


# ============================================================
# MODULE REGISTRY
# ============================================================

try:
    from .module_registry import ModuleRegistry, module_registry
    MODULE_REGISTRY_AVAILABLE = True
    __all__ += ["ModuleRegistry", "module_registry", "MODULE_REGISTRY_AVAILABLE"]
except ImportError:
    MODULE_REGISTRY_AVAILABLE = False
    ModuleRegistry = None
    module_registry = None


# ============================================================
# MODULE BASE
# ============================================================

try:
    from .module_base import ModuleBase
    __all__ += ["ModuleBase"]
except ImportError:
    ModuleBase = None


# ============================================================
# KNOWLEDGE BUILDER
# ============================================================

try:
    from .knowledge_builder import KnowledgeBuilder, knowledge_builder
    KNOWLEDGE_BUILDER_AVAILABLE = True
    __all__ += ["KnowledgeBuilder", "knowledge_builder", "KNOWLEDGE_BUILDER_AVAILABLE"]
except ImportError:
    KNOWLEDGE_BUILDER_AVAILABLE = False
    KnowledgeBuilder = None
    knowledge_builder = None


# ============================================================
# CURIOSITY
# ============================================================

try:
    from .curiosity import CuriosityEngine, curiosity_engine
    CURIOSITY_AVAILABLE = True
    __all__ += ["CuriosityEngine", "curiosity_engine", "CURIOSITY_AVAILABLE"]
except ImportError:
    CURIOSITY_AVAILABLE = False
    CuriosityEngine = None
    curiosity_engine = None


# ============================================================
# EXPERIENCE
# ============================================================

try:
    from .experience import ExperienceEngine, experience_engine
    EXPERIENCE_AVAILABLE = True
    __all__ += ["ExperienceEngine", "experience_engine", "EXPERIENCE_AVAILABLE"]
except ImportError:
    EXPERIENCE_AVAILABLE = False
    ExperienceEngine = None
    experience_engine = None


# ============================================================
# KNOWLEDGE GRAPH
# ============================================================

try:
    from .knowledge_graph import KnowledgeGraph, knowledge_graph
    KNOWLEDGE_GRAPH_AVAILABLE = True
    __all__ += ["KnowledgeGraph", "knowledge_graph", "KNOWLEDGE_GRAPH_AVAILABLE"]
except ImportError:
    KNOWLEDGE_GRAPH_AVAILABLE = False
    KnowledgeGraph = None
    knowledge_graph = None


# ============================================================
# EXTERNAL MODULES (dari core level)
# ============================================================

# HEALTH
try:
    from core.health import HealthMonitor, health_monitor
    HEALTH_AVAILABLE = True
    __all__ += ["HealthMonitor", "health_monitor", "HEALTH_AVAILABLE"]
except ImportError:
    HEALTH_AVAILABLE = False
    HealthMonitor = None
    health_monitor = None

# BOOTSTRAP
try:
    from core.bootstrap import Bootstrap, bootstrap
    BOOTSTRAP_AVAILABLE = True
    __all__ += ["Bootstrap", "bootstrap", "BOOTSTRAP_AVAILABLE"]
except ImportError:
    BOOTSTRAP_AVAILABLE = False
    Bootstrap = None
    bootstrap = None

# BRAIN
try:
    from core.brain import Brain, brain
    BRAIN_AVAILABLE = True
    __all__ += ["Brain", "brain", "BRAIN_AVAILABLE"]
except ImportError:
    BRAIN_AVAILABLE = False
    Brain = None
    brain = None

# CONSCIOUSNESS
try:
    from core.consciousness import Consciousness, consciousness
    CONSCIOUSNESS_AVAILABLE = True
    __all__ += ["Consciousness", "consciousness", "CONSCIOUSNESS_AVAILABLE"]
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False
    Consciousness = None
    consciousness = None

# DIAGNOSTICS
try:
    from core.diagnostics import Diagnostics, diagnostics
    DIAGNOSTICS_AVAILABLE = True
    __all__ += ["Diagnostics", "diagnostics", "DIAGNOSTICS_AVAILABLE"]
except ImportError:
    DIAGNOSTICS_AVAILABLE = False
    Diagnostics = None
    diagnostics = None

# KNOWLEDGE
try:
    from core.knowledge import KnowledgeEngine, knowledge_engine
    KNOWLEDGE_AVAILABLE = True
    __all__ += ["KnowledgeEngine", "knowledge_engine", "KNOWLEDGE_AVAILABLE"]
except ImportError:
    KNOWLEDGE_AVAILABLE = False
    KnowledgeEngine = None
    knowledge_engine = None

# MARKET DATA
try:
    from core.market_data import MarketData, market_data
    MARKET_DATA_AVAILABLE = True
    __all__ += ["MarketData", "market_data", "MARKET_DATA_AVAILABLE"]
except ImportError:
    MARKET_DATA_AVAILABLE = False
    MarketData = None
    market_data = None

# MEMORY
try:
    from core.memory import MemoryEngine, memory_engine
    MEMORY_AVAILABLE = True
    __all__ += ["MemoryEngine", "memory_engine", "MEMORY_AVAILABLE"]
except ImportError:
    MEMORY_AVAILABLE = False
    MemoryEngine = None
    memory_engine = None

# MODULE MANAGER
try:
    from core.module_manager import ModuleManager, module_manager
    MODULE_MANAGER_AVAILABLE = True
    __all__ += ["ModuleManager", "module_manager", "MODULE_MANAGER_AVAILABLE"]
except ImportError:
    MODULE_MANAGER_AVAILABLE = False
    ModuleManager = None
    module_manager = None

# REASONING
try:
    from core.reasoning import ReasoningEngine, reasoning_engine
    REASONING_AVAILABLE = True
    __all__ += ["ReasoningEngine", "reasoning_engine", "REASONING_AVAILABLE"]
except ImportError:
    REASONING_AVAILABLE = False
    ReasoningEngine = None
    reasoning_engine = None

# RUNTIME
try:
    from core.runtime import RuntimeManager, runtime_manager
    RUNTIME_AVAILABLE = True
    __all__ += ["RuntimeManager", "runtime_manager", "RUNTIME_AVAILABLE"]
except ImportError:
    RUNTIME_AVAILABLE = False
    RuntimeManager = None
    runtime_manager = None

# SCANNER
try:
    from core.scanner import ScannerEngine, scanner_engine
    SCANNER_AVAILABLE = True
    __all__ += ["ScannerEngine", "scanner_engine", "SCANNER_AVAILABLE"]
except ImportError:
    SCANNER_AVAILABLE = False
    ScannerEngine = None
    scanner_engine = None

# SCHEDULER
try:
    from core.scheduler import Scheduler, scheduler
    SCHEDULER_AVAILABLE = True
    __all__ += ["Scheduler", "scheduler", "SCHEDULER_AVAILABLE"]
except ImportError:
    SCHEDULER_AVAILABLE = False
    Scheduler = None
    scheduler = None

# SIGNAL
try:
    from core.signal import SignalEngine, signal_engine
    SIGNAL_AVAILABLE = True
    __all__ += ["SignalEngine", "signal_engine", "SIGNAL_AVAILABLE"]
except ImportError:
    SIGNAL_AVAILABLE = False
    SignalEngine = None
    signal_engine = None

# SYSTEM CONFIG
try:
    from core.system_config import SystemConfig, system_config
    SYSTEM_CONFIG_AVAILABLE = True
    __all__ += ["SystemConfig", "system_config", "SYSTEM_CONFIG_AVAILABLE"]
except ImportError:
    SYSTEM_CONFIG_AVAILABLE = False
    SystemConfig = None
    system_config = None

# VALIDATOR
try:
    from core.validator import Validator, validator
    VALIDATOR_AVAILABLE = True
    __all__ += ["Validator", "validator", "VALIDATOR_AVAILABLE"]
except ImportError:
    VALIDATOR_AVAILABLE = False
    Validator = None
    validator = None

# WATCHDOG
try:
    from core.watchdog import Watchdog, watchdog
    WATCHDOG_AVAILABLE = True
    __all__ += ["Watchdog", "watchdog", "WATCHDOG_AVAILABLE"]
except ImportError:
    WATCHDOG_AVAILABLE = False
    Watchdog = None
    watchdog = None


# ============================================================
# CONTRACTS - Dari core/contracts.py
# ============================================================

try:
    from core.contracts import (
        CONTRACT_VERSION,
        INTERNAL_CONTRACT_REVISION,
        CONTRACT_SCHEMA,
        ModuleStatus,
        ModuleInput,
        ModuleOutput,
        LearningEvent,
        LearningResult,
        ModuleContract,
        safe_json,
        safe_copy,
        normalize_confidence,
        normalize_execution_time,
        utc_now,
        utc_timestamp,
        generate_id,
        create_input,
        create_event,
        normalize_output,
        exception_to_output,
        validate_input,
        validate_output,
        is_contract_compatible,
        output_is_success,
        output_is_failure,
        output_is_skipped,
        dumps,
        dump,
        load,
        ExecutionTimer,
        ContractContext,
        ModuleExecution,
        test_contracts,
        OUTPUT_SUCCESS,
        OUTPUT_PARTIAL,
        OUTPUT_SKIPPED,
        OUTPUT_FAILED,
        VALID_OUTPUT_STATES,
        MODULE_CREATED,
        MODULE_INITIALIZING,
        MODULE_ONLINE,
        MODULE_DEGRADED,
        MODULE_OFFLINE,
        MODULE_DISABLED,
        MODULE_SHUTTING_DOWN,
        MODULE_STOPPED,
        MODULE_ERROR,
        VALID_MODULE_STATES,
        CIRCULAR_REFERENCE_MARKER,
        MAX_DEPTH_MARKER,
        UNSERIALIZABLE_MARKER,
        TRUNCATED_MARKER,
        DEFAULT_MAX_DEPTH,
        DEFAULT_MAX_ITEMS,
        DEFAULT_MAX_STRING_LENGTH,
    )
    CONTRACTS_AVAILABLE = True
    __all__ += [
        "CONTRACT_VERSION",
        "INTERNAL_CONTRACT_REVISION",
        "CONTRACT_SCHEMA",
        "ModuleStatus",
        "ModuleInput",
        "ModuleOutput",
        "LearningEvent",
        "LearningResult",
        "ModuleContract",
        "safe_json",
        "safe_copy",
        "normalize_confidence",
        "normalize_execution_time",
        "utc_now",
        "utc_timestamp",
        "generate_id",
        "create_input",
        "create_event",
        "normalize_output",
        "exception_to_output",
        "validate_input",
        "validate_output",
        "is_contract_compatible",
        "output_is_success",
        "output_is_failure",
        "output_is_skipped",
        "dumps",
        "dump",
        "load",
        "ExecutionTimer",
        "ContractContext",
        "ModuleExecution",
        "test_contracts",
        "OUTPUT_SUCCESS",
        "OUTPUT_PARTIAL",
        "OUTPUT_SKIPPED",
        "OUTPUT_FAILED",
        "VALID_OUTPUT_STATES",
        "MODULE_CREATED",
        "MODULE_INITIALIZING",
        "MODULE_ONLINE",
        "MODULE_DEGRADED",
        "MODULE_OFFLINE",
        "MODULE_DISABLED",
        "MODULE_SHUTTING_DOWN",
        "MODULE_STOPPED",
        "MODULE_ERROR",
        "VALID_MODULE_STATES",
        "CIRCULAR_REFERENCE_MARKER",
        "MAX_DEPTH_MARKER",
        "UNSERIALIZABLE_MARKER",
        "TRUNCATED_MARKER",
        "DEFAULT_MAX_DEPTH",
        "DEFAULT_MAX_ITEMS",
        "DEFAULT_MAX_STRING_LENGTH",
        "CONTRACTS_AVAILABLE",
    ]
except ImportError:
    CONTRACTS_AVAILABLE = False
    CONTRACT_VERSION = "2.0"
    INTERNAL_CONTRACT_REVISION = "2.0"
    CONTRACT_SCHEMA = "inkside-intelligence-learning-contract"
    ModuleStatus = None
    ModuleInput = None
    ModuleOutput = None
    LearningEvent = None
    LearningResult = None
    ModuleContract = None
    safe_json = None
    safe_copy = None
    normalize_confidence = None
    normalize_execution_time = None
    utc_now = None
    utc_timestamp = None
    generate_id = None
    create_input = None
    create_event = None
    normalize_output = None
    exception_to_output = None
    validate_input = None
    validate_output = None
    is_contract_compatible = None
    output_is_success = None
    output_is_failure = None
    output_is_skipped = None
    dumps = None
    dump = None
    load = None
    ExecutionTimer = None
    ContractContext = None
    ModuleExecution = None
    test_contracts = None
    OUTPUT_SUCCESS = "success"
    OUTPUT_PARTIAL = "partial"
    OUTPUT_SKIPPED = "skipped"
    OUTPUT_FAILED = "failed"
    VALID_OUTPUT_STATES = {"success", "partial", "skipped", "failed"}
    MODULE_CREATED = "created"
    MODULE_INITIALIZING = "initializing"
    MODULE_ONLINE = "online"
    MODULE_DEGRADED = "degraded"
    MODULE_OFFLINE = "offline"
    MODULE_DISABLED = "disabled"
    MODULE_SHUTTING_DOWN = "shutting_down"
    MODULE_STOPPED = "stopped"
    MODULE_ERROR = "error"
    VALID_MODULE_STATES = {
        "created", "initializing", "online", "degraded",
        "offline", "disabled", "shutting_down", "stopped", "error"
    }
    CIRCULAR_REFERENCE_MARKER = "[CIRCULAR_REFERENCE]"
    MAX_DEPTH_MARKER = "[MAX_DEPTH]"
    UNSERIALIZABLE_MARKER = "[UNSERIALIZABLE]"
    TRUNCATED_MARKER = "[TRUNCATED]"
    DEFAULT_MAX_DEPTH = 20
    DEFAULT_MAX_ITEMS = 10000
    DEFAULT_MAX_STRING_LENGTH = 100000


# ============================================================
# GET MODULE STATUS
# ============================================================

def get_module_status() -> dict:
    """
    Return status of all available modules.
    
    Returns:
        Dictionary with module names as keys and availability as values
    """
    return {
        "adaptive": ADAPTIVE_AVAILABLE,
        "analyzer": LEARNING_ANALYZER_AVAILABLE,
        "archive": ARCHIVE_AVAILABLE,
        "association": ASSOCIATION_AVAILABLE,
        "behavior": BEHAVIOR_AVAILABLE,
        "bootstrap": BOOTSTRAP_AVAILABLE,
        "brain": BRAIN_AVAILABLE,
        "consciousness": CONSCIOUSNESS_AVAILABLE,
        "context_manager": CONTEXT_MANAGER_AVAILABLE,
        "contracts": CONTRACTS_AVAILABLE,
        "curiosity": CURIOSITY_AVAILABLE,
        "data_pipeline": DATA_PIPELINE_AVAILABLE,
        "decision_engine": DECISION_ENGINE_AVAILABLE,
        "diagnostics": DIAGNOSTICS_AVAILABLE,
        "entity_recognition": ENTITY_RECOGNITION_AVAILABLE,
        "evaluator": EVALUATOR_AVAILABLE,
        "event": EVENT_AVAILABLE,
        "experience": EXPERIENCE_AVAILABLE,
        "goal_manager": GOAL_MANAGER_AVAILABLE,
        "health": HEALTH_AVAILABLE,
        "improvement": IMPROVEMENT_AVAILABLE,
        "insight": INSIGHT_AVAILABLE,
        "knowledge": KNOWLEDGE_AVAILABLE,
        "knowledge_builder": KNOWLEDGE_BUILDER_AVAILABLE,
        "knowledge_graph": KNOWLEDGE_GRAPH_AVAILABLE,
        "learning_analyzer": LEARNING_ANALYZER_AVAILABLE,
        "learning_engine": LEARNING_ENGINE_AVAILABLE,
        "learning_memory": LEARNING_MEMORY_AVAILABLE,
        "market_data": MARKET_DATA_AVAILABLE,
        "market_learning": MARKET_LEARNING_AVAILABLE,
        "memory": MEMORY_AVAILABLE,
        "memory_optimizer": MEMORY_OPTIMIZER_AVAILABLE,
        "module_manager": MODULE_MANAGER_AVAILABLE,
        "module_registry": MODULE_REGISTRY_AVAILABLE,
        "pattern": PATTERN_AVAILABLE,
        "prediction": PREDICTION_AVAILABLE,
        "reasoning": REASONING_AVAILABLE,
        "reflection": REFLECTION_AVAILABLE,
        "runtime": RUNTIME_AVAILABLE,
        "scanner": SCANNER_AVAILABLE,
        "scheduler": SCHEDULER_AVAILABLE,
        "self_diagnostic": SELF_DIAGNOSTIC_AVAILABLE,
        "semantic_memory": SEMANTIC_MEMORY_AVAILABLE,
        "semantic_processor": SEMANTIC_PROCESSOR_AVAILABLE,
        "signal": SIGNAL_AVAILABLE,
        "simulation": SIMULATION_AVAILABLE,
        "strategy": STRATEGY_AVAILABLE,
        "system_config": SYSTEM_CONFIG_AVAILABLE,
        "validator": VALIDATOR_AVAILABLE,
        "watchdog": WATCHDOG_AVAILABLE,
    }


def get_available_modules() -> list:
    """
    Return list of available module names.
    
    Returns:
        List of module names that are available
    """
    return [
        name for name, available in get_module_status().items()
        if available
    ]


def get_unavailable_modules() -> list:
    """
    Return list of unavailable module names.
    
    Returns:
        List of module names that are not available
    """
    return [
        name for name, available in get_module_status().items()
        if not available
    ]


def get_module_health() -> dict:
    """
    Get module health summary.
    
    Returns:
        Dictionary with health metrics
    """
    status = get_module_status()
    total = len(status)
    available = sum(1 for v in status.values() if v)
    unavailable = total - available
    
    return {
        "total_modules": total,
        "available": available,
        "unavailable": unavailable,
        "health_percentage": round((available / total) * 100, 1) if total > 0 else 0,
        "available_modules": get_available_modules(),
        "unavailable_modules": get_unavailable_modules(),
    }


# ============================================================
# VERSION INFO
# ============================================================

def get_version_info() -> dict:
    """
    Get version information for all modules.
    
    Returns:
        Dictionary with version information
    """
    return {
        "package_version": __version__,
        "contract_version": CONTRACT_VERSION,
        "event_version": EVENT_VERSION,
        "engine_version": ENGINE_VERSION,
        "kernel_version": KERNEL_VERSION,
    }


# ============================================================
# END
# ============================================================

# ============================================================
# DEBUG FUNCTIONS
# ============================================================

def print_module_status():
    """Print module status in a formatted table."""
    status = get_module_status()
    
    # Group modules
    available = [name for name, avail in status.items() if avail]
    unavailable = [name for name, avail in status.items() if not avail]
    
    print("=" * 70)
    print("  MODULE STATUS SUMMARY")
    print("=" * 70)
    print(f"  Total Modules : {len(status)}")
    print(f"  Available     : {len(available)}")
    print(f"  Unavailable   : {len(unavailable)}")
    print("-" * 70)
    
    if available:
        print("  [✓] Available:")
        for name in sorted(available):
            print(f"      - {name}")
    
    if unavailable:
        print("  [✗] Unavailable:")
        for name in sorted(unavailable):
            print(f"      - {name}")
    
    print("=" * 70)


def debug_module_status():
    """Debug function to check module availability."""
    status = get_module_status()
    
    # Check specific modules
    critical_modules = [
        "event", "contracts", "learning_engine", 
        "prediction", "pattern", "market_learning"
    ]
    
    print("\n[DEBUG] Critical Modules Status:")
    for module in critical_modules:
        available = status.get(module, False)
        status_icon = "✓" if available else "✗"
        print(f"  [{status_icon}] {module}: {available}")
    
    return status
