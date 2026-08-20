# ============================================================
# core/__init__.py
# INKSIDE INTELLIGENCE OS - CORE PACKAGE
# SINGLE ENTRY POINT - SEMUA MODULE DARI SINI
# 
# COGNITIVE MIRROR ENGINE v5.0 - ULTIMATE
# ============================================================

"""
INKSIDE INTELLIGENCE OS - Ultimate Core Package

SINGLE ENTRY POINT:
    from core import (
        # Core Modules
        Brain, brain,
        Consciousness, consciousness,
        TradingBot,
        HealthMonitor, health_monitor,
        Memory, memory,
        Knowledge, knowledge,
        ReasoningEngine, reasoning,
        Scanner, scanner,
        SignalEngine, signal_engine,
        
        # Autonomous Learning
        AutonomousEngine, autonomous,
        autonomous_start, autonomous_stop,
        autonomous_status, autonomous_process_historical,
        
        # Exchange & Market Data
        KrakenMarketData, kraken_market,
        Exchange, exchange,
        get_exchange, get_market_data,
        get_ticker, get_ohlc, get_latest_prices, test_connection,
        
        # Learning Modules
        LearningEngine, learning_engine,
        PatternEngine, pattern,
        PredictionEngine, prediction_engine,
        ...
    )

JANGAN import langsung dari core.learning!
    ❌ from core.learning.engine import LearningEngine
    ✅ from core import LearningEngine
"""

__version__ = "5.0.0"
__author__ = "Inkside Intelligence OS"
__description__ = "Cognitive Mirror Engine - Ultimate Core Package"
__all__ = []

import time  # <-- FIX: tambahkan import time untuk get_exchange_status()


# ============================================================
# 1. CORE MODULES (dari core/)
# ============================================================

# 1.1 BRAIN
try:
    from .brain import (
        Brain,
        brain,
        observe,
        analyze,
        get_state,
        status as brain_status,
        snapshot as brain_snapshot,
        forecast,
        decision_support,
        feedback,
        health_check,
        start as brain_start,
        stop as brain_stop,
        reset as brain_reset,
        self_test as brain_self_test,
        get_module_status,
        print_module_status,
    )
    BRAIN_AVAILABLE = True
    __all__ += [
        "Brain", "brain",
        "observe", "analyze",
        "get_state",
        "brain_status", "brain_snapshot",
        "forecast", "decision_support",
        "feedback", "health_check",
        "brain_start", "brain_stop", "brain_reset",
        "brain_self_test",
        "get_module_status", "print_module_status",
        "BRAIN_AVAILABLE",
    ]
except ImportError:
    BRAIN_AVAILABLE = False
    Brain = None
    brain = None
    observe = None
    analyze = None
    get_state = None
    brain_status = None
    brain_snapshot = None
    forecast = None
    decision_support = None
    feedback = None
    health_check = None
    brain_start = None
    brain_stop = None
    brain_reset = None
    brain_self_test = None
    get_module_status = None
    print_module_status = None

# 1.2 CONSCIOUSNESS
try:
    from .consciousness import (
        Consciousness,
        consciousness,
        process as conscious_process,
        learn as conscious_learn,
        get_state as conscious_state,
        status as conscious_status,
        snapshot as conscious_snapshot,
        start as conscious_start,
        stop as conscious_stop,
        reset as conscious_reset,
        self_test as conscious_self_test,
    )
    CONSCIOUSNESS_AVAILABLE = True
    __all__ += [
        "Consciousness", "consciousness",
        "conscious_process", "conscious_learn",
        "conscious_state", "conscious_status",
        "conscious_snapshot",
        "conscious_start", "conscious_stop", "conscious_reset",
        "conscious_self_test",
        "CONSCIOUSNESS_AVAILABLE",
    ]
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False
    Consciousness = None
    consciousness = None
    conscious_process = None
    conscious_learn = None
    conscious_state = None
    conscious_status = None
    conscious_snapshot = None
    conscious_start = None
    conscious_stop = None
    conscious_reset = None
    conscious_self_test = None

# 1.3 TRADING BOT
try:
    from .bot import (
        TradingBot,
        BotEngine,
        TradingEngine,
        BotState,
        TradingMode,
        RiskLevel,
        SignalType,
        TradeResult,
        PerformanceMetrics,
    )
    BOT_AVAILABLE = True
    __all__ += [
        "TradingBot", "BotEngine", "TradingEngine",
        "BotState", "TradingMode", "RiskLevel",
        "SignalType", "TradeResult", "PerformanceMetrics",
        "BOT_AVAILABLE",
    ]
except ImportError:
    BOT_AVAILABLE = False
    TradingBot = None
    BotEngine = None
    TradingEngine = None
    BotState = None
    TradingMode = None
    RiskLevel = None
    SignalType = None
    TradeResult = None
    PerformanceMetrics = None

# 1.4 HEALTH MONITOR
try:
    from .health import (
        HealthMonitor,
        health_monitor,
        set_status,
        get_status,
        register_health,
        record_health,
        get_health,
        get_health_status,
        heartbeat,
        health_status,
        health_score,
        system_health,
        health_alerts,
        test_health,
        print_health,
    )
    HEALTH_AVAILABLE = True
    __all__ += [
        "HealthMonitor", "health_monitor",
        "set_status", "get_status",
        "register_health", "record_health",
        "get_health", "get_health_status",
        "heartbeat", "health_status",
        "health_score", "system_health",
        "health_alerts", "test_health", "print_health",
        "HEALTH_AVAILABLE",
    ]
except ImportError:
    HEALTH_AVAILABLE = False
    HealthMonitor = None
    health_monitor = None
    set_status = None
    get_status = None
    register_health = None
    record_health = None
    get_health = None
    get_health_status = None
    heartbeat = None
    health_status = None
    health_score = None
    system_health = None
    health_alerts = None
    test_health = None
    print_health = None

# 1.5 MEMORY
try:
    from .memory import memory
    MEMORY_AVAILABLE = True
    __all__ += ["memory", "MEMORY_AVAILABLE"]
except ImportError:
    MEMORY_AVAILABLE = False
    memory = None

# 1.6 KNOWLEDGE
try:
    from .knowledge import knowledge
    KNOWLEDGE_AVAILABLE = True
    __all__ += ["knowledge", "KNOWLEDGE_AVAILABLE"]
except ImportError:
    KNOWLEDGE_AVAILABLE = False
    knowledge = None

# 1.7 REASONING
try:
    from .reasoning import ReasoningEngine, reasoning
    REASONING_AVAILABLE = True
    __all__ += ["ReasoningEngine", "reasoning", "REASONING_AVAILABLE"]
except ImportError:
    REASONING_AVAILABLE = False
    ReasoningEngine = None
    reasoning = None

# 1.8 SCANNER
try:
    from .scanner import MarketScanner, CognitiveMarketScanner
    SCANNER_AVAILABLE = True
    __all__ += ["MarketScanner", "CognitiveMarketScanner", "SCANNER_AVAILABLE"]
except ImportError:
    SCANNER_AVAILABLE = False
    MarketScanner = None
    CognitiveMarketScanner = None

# 1.9 SIGNAL ENGINE
try:
    from .signal_engine import SignalEngine, signal_engine
    SIGNAL_AVAILABLE = True
    __all__ += ["SignalEngine", "signal_engine", "SIGNAL_AVAILABLE"]
except ImportError:
    SIGNAL_AVAILABLE = False
    SignalEngine = None
    signal_engine = None

# ============================================================
# 1.10 MARKET DATA & EXCHANGE (FULL INTEGRATION)
# ============================================================

try:
    from .market_data import (
        KrakenMarketData,
        kraken_market,
        TickerData,
        Candle,
        OrderBook,
        OrderBookLevel,
        Trade,
        MarketMetrics,
        Interval,
        DataSource,
        self_test as market_self_test,
        KRAKEN_VERSION,
    )
    MARKET_DATA_AVAILABLE = True
    
    # ============================================================
    # EXCHANGE ALIAS (for compatibility with bot.py and others)
    # ============================================================
    
    # Alias class
    Exchange = KrakenMarketData
    
    # Alias instance
    exchange = kraken_market
    
    # Convenience functions
    def get_exchange():
        """
        Get exchange instance.
        
        Returns:
            KrakenMarketData instance
        """
        return kraken_market
    
    def get_market_data():
        """
        Get market data instance.
        
        Returns:
            KrakenMarketData instance
        """
        return kraken_market
    
    def get_ticker(pair: str):
        """
        Get ticker for a pair.
        
        Args:
            pair: Trading pair (e.g., 'BTC/USD')
            
        Returns:
            TickerData or None
        """
        return kraken_market.get_ticker(pair)
    
    def get_ohlc(pair: str, interval: str = '1h', limit: int = 250):
        """
        Get OHLC data for a pair.
        
        Args:
            pair: Trading pair
            interval: Timeframe ('1m', '5m', '15m', '1h', '4h', '1d')
            limit: Number of candles
            
        Returns:
            List of Candle objects
        """
        return kraken_market.get_ohlc(pair, interval, limit)
    
    def get_latest_prices(pairs: list = None):
        """
        Get latest prices for multiple pairs.
        
        Args:
            pairs: List of trading pairs
            
        Returns:
            Dictionary of pair -> price
        """
        return kraken_market.get_latest_prices(pairs)
    
    def test_connection():
        """
        Test connection to Kraken.
        
        Returns:
            True if connected, False otherwise
        """
        return kraken_market.health_check().get('status') == 'ONLINE'
    
    __all__ += [
        "KrakenMarketData",
        "kraken_market",
        "Exchange",
        "exchange",
        "get_exchange",
        "get_market_data",
        "get_ticker",
        "get_ohlc",
        "get_latest_prices",
        "test_connection",
        "TickerData",
        "Candle",
        "OrderBook",
        "OrderBookLevel",
        "Trade",
        "MarketMetrics",
        "Interval",
        "DataSource",
        "market_self_test",
        "KRAKEN_VERSION",
        "MARKET_DATA_AVAILABLE",
    ]
    
except ImportError:
    MARKET_DATA_AVAILABLE = False
    KrakenMarketData = None
    kraken_market = None
    Exchange = None
    exchange = None
    get_exchange = None
    get_market_data = None
    get_ticker = None
    get_ohlc = None
    get_latest_prices = None
    test_connection = None
    TickerData = None
    Candle = None
    OrderBook = None
    OrderBookLevel = None
    Trade = None
    MarketMetrics = None
    Interval = None
    DataSource = None
    market_self_test = None
    KRAKEN_VERSION = "N/A"

# 1.11 ANALYZER
try:
    from .analyzer import Analyzer, MarketAnalyzer
    ANALYZER_AVAILABLE = True
    __all__ += ["Analyzer", "MarketAnalyzer", "ANALYZER_AVAILABLE"]
except ImportError:
    ANALYZER_AVAILABLE = False
    Analyzer = None
    MarketAnalyzer = None

# 1.12 MODULE MANAGER
try:
    from .module_manager import module_manager
    MODULE_MANAGER_AVAILABLE = True
    __all__ += ["module_manager", "MODULE_MANAGER_AVAILABLE"]
except ImportError:
    MODULE_MANAGER_AVAILABLE = False
    module_manager = None

# 1.13 SCHEDULER
try:
    from .scheduler import (
        Scheduler,
        scheduler,
        start as scheduler_start,
        stop as scheduler_stop,
        add_once,
        add_interval,
        add_delay,
        cancel,
        remove,
        run_now,
        status as scheduler_status,
    )
    SCHEDULER_AVAILABLE = True
    __all__ += [
        "Scheduler", "scheduler",
        "scheduler_start", "scheduler_stop",
        "add_once", "add_interval", "add_delay",
        "cancel", "remove", "run_now",
        "scheduler_status",
        "SCHEDULER_AVAILABLE",
    ]
except ImportError:
    SCHEDULER_AVAILABLE = False
    Scheduler = None
    scheduler = None
    scheduler_start = None
    scheduler_stop = None
    add_once = None
    add_interval = None
    add_delay = None
    cancel = None
    remove = None
    run_now = None
    scheduler_status = None

# 1.14 RUNTIME
try:
    from .runtime import (
        RuntimeManager,
        runtime,
        start as runtime_start,
        stop as runtime_stop,
        restart,
        register as runtime_register,
        unregister as runtime_unregister,
        get_module,
        status as runtime_status,
        health as runtime_health,
    )
    RUNTIME_AVAILABLE = True
    __all__ += [
        "RuntimeManager", "runtime",
        "runtime_start", "runtime_stop",
        "restart",
        "runtime_register", "runtime_unregister",
        "get_module",
        "runtime_status", "runtime_health",
        "RUNTIME_AVAILABLE",
    ]
except ImportError:
    RUNTIME_AVAILABLE = False
    RuntimeManager = None
    runtime = None
    runtime_start = None
    runtime_stop = None
    restart = None
    runtime_register = None
    runtime_unregister = None
    get_module = None
    runtime_status = None
    runtime_health = None

# 1.15 SYSTEM CONFIG
try:
    from .system_config import (
        SystemConfig,
        system_config,
        get as config_get,
        set as config_set,
        delete as config_delete,
        exists as config_exists,
        update as config_update,
        snapshot as config_snapshot,
        validate as config_validate,
        save as config_save,
        load as config_load,
        status as config_status,
    )
    SYSTEM_CONFIG_AVAILABLE = True
    __all__ += [
        "SystemConfig", "system_config",
        "config_get", "config_set",
        "config_delete", "config_exists",
        "config_update", "config_snapshot",
        "config_validate", "config_save",
        "config_load", "config_status",
        "SYSTEM_CONFIG_AVAILABLE",
    ]
except ImportError:
    SYSTEM_CONFIG_AVAILABLE = False
    SystemConfig = None
    system_config = None
    config_get = None
    config_set = None
    config_delete = None
    config_exists = None
    config_update = None
    config_snapshot = None
    config_validate = None
    config_save = None
    config_load = None
    config_status = None

# 1.16 WATCHDOG
try:
    from .watchdog import SystemWatchdog, watchdog
    WATCHDOG_AVAILABLE = True
    __all__ += ["SystemWatchdog", "watchdog", "WATCHDOG_AVAILABLE"]
except ImportError:
    WATCHDOG_AVAILABLE = False
    SystemWatchdog = None
    watchdog = None

# 1.17 AUTONOMOUS LEARNING ENGINE (BARU!)
try:
    from .autonomous import (
        AutonomousEngine,
        autonomous,
        start as autonomous_start,
        stop as autonomous_stop,
        status as autonomous_status,
        process_historical as autonomous_process_historical,
        self_test as autonomous_self_test,
    )
    AUTONOMOUS_AVAILABLE = True
    __all__ += [
        "AutonomousEngine", "autonomous",
        "autonomous_start", "autonomous_stop",
        "autonomous_status", "autonomous_process_historical",
        "autonomous_self_test",
        "AUTONOMOUS_AVAILABLE",
    ]
except ImportError:
    AUTONOMOUS_AVAILABLE = False
    AutonomousEngine = None
    autonomous = None
    autonomous_start = None
    autonomous_stop = None
    autonomous_status = None
    autonomous_process_historical = None
    autonomous_self_test = None

# 1.18 DIAGNOSTICS
try:
    from .diagnostics import SystemDiagnostics, diagnostics
    DIAGNOSTICS_AVAILABLE = True
    __all__ += ["SystemDiagnostics", "diagnostics", "DIAGNOSTICS_AVAILABLE"]
except ImportError:
    DIAGNOSTICS_AVAILABLE = False
    SystemDiagnostics = None
    diagnostics = None

# 1.19 VALIDATOR
try:
    from .validator import ModuleValidator, validator
    VALIDATOR_AVAILABLE = True
    __all__ += ["ModuleValidator", "validator", "VALIDATOR_AVAILABLE"]
except ImportError:
    VALIDATOR_AVAILABLE = False
    ModuleValidator = None
    validator = None

# 1.20 BOOTSTRAP
try:
    from .bootstrap import Bootstrap, bootstrap
    BOOTSTRAP_AVAILABLE = True
    __all__ += ["Bootstrap", "bootstrap", "BOOTSTRAP_AVAILABLE"]
except ImportError:
    BOOTSTRAP_AVAILABLE = False
    Bootstrap = None
    bootstrap = None


# ============================================================
# 2. LEARNING MODULES (dari core/learning/)
# ============================================================

# 2.1 ENGINE
try:
    from .learning.engine import (
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

# 2.2 PATTERN
try:
    from .learning.pattern import PatternEngine, pattern
    PATTERN_ENGINE_AVAILABLE = True
    __all__ += ["PatternEngine", "pattern", "PATTERN_ENGINE_AVAILABLE"]
except ImportError:
    PATTERN_ENGINE_AVAILABLE = False
    PatternEngine = None
    pattern = None

# 2.3 PREDICTION
try:
    from .learning.prediction import PredictionEngine, prediction_engine
    PREDICTION_AVAILABLE = True
    __all__ += ["PredictionEngine", "prediction_engine", "PREDICTION_AVAILABLE"]
except ImportError:
    PREDICTION_AVAILABLE = False
    PredictionEngine = None
    prediction_engine = None

# 2.4 REASONING ENGINE - DINONAKTIFKAN (diganti core/reasoning.py)
REASONING_ENGINE_AVAILABLE = False
ReasoningEngine = None
reasoning_engine = None

# 2.5 DECISION ENGINE
try:
    from .learning.decision_engine import DecisionEngine, decision_engine
    DECISION_ENGINE_AVAILABLE = True
    __all__ += ["DecisionEngine", "decision_engine", "DECISION_ENGINE_AVAILABLE"]
except ImportError:
    DECISION_ENGINE_AVAILABLE = False
    DecisionEngine = None
    decision_engine = None

# 2.6 SEMANTIC MEMORY
try:
    from .learning.semantic_memory import SemanticMemory, semantic_memory
    SEMANTIC_MEMORY_AVAILABLE = True
    __all__ += ["SemanticMemory", "semantic_memory", "SEMANTIC_MEMORY_AVAILABLE"]
except ImportError:
    SEMANTIC_MEMORY_AVAILABLE = False
    SemanticMemory = None
    semantic_memory = None

# 2.7 LEARNING MEMORY
try:
    from .learning.learning_memory import LearningMemory, learning_memory
    LEARNING_MEMORY_AVAILABLE = True
    __all__ += ["LearningMemory", "learning_memory", "LEARNING_MEMORY_AVAILABLE"]
except ImportError:
    LEARNING_MEMORY_AVAILABLE = False
    LearningMemory = None
    learning_memory = None

# 2.8 MEMORY OPTIMIZER
try:
    from .learning.memory_optimizer import MemoryOptimizer, memory_optimizer
    MEMORY_OPTIMIZER_AVAILABLE = True
    __all__ += ["MemoryOptimizer", "memory_optimizer", "MEMORY_OPTIMIZER_AVAILABLE"]
except ImportError:
    MEMORY_OPTIMIZER_AVAILABLE = False
    MemoryOptimizer = None
    memory_optimizer = None

# 2.9 ENTITY RECOGNITION
try:
    from .learning.entity_recognition import EntityRecognition, entity_recognition
    ENTITY_RECOGNITION_AVAILABLE = True
    __all__ += ["EntityRecognition", "entity_recognition", "ENTITY_RECOGNITION_AVAILABLE"]
except ImportError:
    ENTITY_RECOGNITION_AVAILABLE = False
    EntityRecognition = None
    entity_recognition = None

# 2.10 SEMANTIC PROCESSOR
try:
    from .learning.semantic_processor import SemanticProcessor, semantic_processor
    SEMANTIC_PROCESSOR_AVAILABLE = True
    __all__ += ["SemanticProcessor", "semantic_processor", "SEMANTIC_PROCESSOR_AVAILABLE"]
except ImportError:
    SEMANTIC_PROCESSOR_AVAILABLE = False
    SemanticProcessor = None
    semantic_processor = None

# 2.11 CONTEXT MANAGER
try:
    from .learning.context_manager import ContextManager, context_manager
    CONTEXT_MANAGER_AVAILABLE = True
    __all__ += ["ContextManager", "context_manager", "CONTEXT_MANAGER_AVAILABLE"]
except ImportError:
    CONTEXT_MANAGER_AVAILABLE = False
    ContextManager = None
    context_manager = None

# 2.12 GOAL MANAGER
try:
    from .learning.goal_manager import GoalManager, goal_manager
    GOAL_MANAGER_AVAILABLE = True
    __all__ += ["GoalManager", "goal_manager", "GOAL_MANAGER_AVAILABLE"]
except ImportError:
    GOAL_MANAGER_AVAILABLE = False
    GoalManager = None
    goal_manager = None

# 2.13 REFLECTION
try:
    from .learning.reflection import ReflectionEngine, reflection_engine
    REFLECTION_AVAILABLE = True
    __all__ += ["ReflectionEngine", "reflection_engine", "REFLECTION_AVAILABLE"]
except ImportError:
    REFLECTION_AVAILABLE = False
    ReflectionEngine = None
    reflection_engine = None

# 2.14 INSIGHT
try:
    from .learning.insight import InsightEngine, insight_engine
    INSIGHT_AVAILABLE = True
    __all__ += ["InsightEngine", "insight_engine", "INSIGHT_AVAILABLE"]
except ImportError:
    INSIGHT_AVAILABLE = False
    InsightEngine = None
    insight_engine = None

# 2.15 BEHAVIOR
try:
    from .learning.behavior import BehaviorEngine, behavior_engine
    BEHAVIOR_AVAILABLE = True
    __all__ += ["BehaviorEngine", "behavior_engine", "BEHAVIOR_AVAILABLE"]
except ImportError:
    BEHAVIOR_AVAILABLE = False
    BehaviorEngine = None
    behavior_engine = None

# 2.16 ASSOCIATION
try:
    from .learning.association import AssociationEngine, association_engine
    ASSOCIATION_AVAILABLE = True
    __all__ += ["AssociationEngine", "association_engine", "ASSOCIATION_AVAILABLE"]
except ImportError:
    ASSOCIATION_AVAILABLE = False
    AssociationEngine = None
    association_engine = None

# 2.17 SELF DIAGNOSTIC
try:
    from .learning.self_diagnostic import SelfDiagnostic, self_diagnostic
    SELF_DIAGNOSTIC_AVAILABLE = True
    __all__ += ["SelfDiagnostic", "self_diagnostic", "SELF_DIAGNOSTIC_AVAILABLE"]
except ImportError:
    SELF_DIAGNOSTIC_AVAILABLE = False
    SelfDiagnostic = None
    self_diagnostic = None

# 2.18 IMPROVEMENT
try:
    from .learning.improvement import ImprovementEngine, improvement_engine
    IMPROVEMENT_AVAILABLE = True
    __all__ += ["ImprovementEngine", "improvement_engine", "IMPROVEMENT_AVAILABLE"]
except ImportError:
    IMPROVEMENT_AVAILABLE = False
    ImprovementEngine = None
    improvement_engine = None

# ============================================================
# 2.19 EVENT
# ============================================================

try:
    from .learning.event import (
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
        status as event_status,
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
        test_event_system,
        test_event_system_advanced,
    )
    
    # Alias untuk backward compatibility
    EventSystem = EventBus
    
    EVENT_AVAILABLE = True
    __all__ += [
        "EventBus", "EventSystem", "Event", "EventHandler", "EventResult",
        "event_system",
        "subscribe", "unsubscribe", "publish", "emit", "dispatch",
        "publish_async", "event_status",
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
        "test_event_system", "test_event_system_advanced",
    ]
except ImportError:
    EVENT_AVAILABLE = False
    EventBus = None
    EventSystem = None
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
    event_status = None
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
    test_event_system = None
    test_event_system_advanced = None

# 2.20 MARKET LEARNING
try:
    from .learning.market_learning import MarketLearning, market_learning
    MARKET_LEARNING_AVAILABLE = True
    __all__ += ["MarketLearning", "market_learning", "MARKET_LEARNING_AVAILABLE"]
except ImportError:
    MARKET_LEARNING_AVAILABLE = False
    MarketLearning = None
    market_learning = None

# 2.21 STRATEGY
try:
    from .learning.strategy import StrategyEngine, strategy_engine
    STRATEGY_AVAILABLE = True
    __all__ += ["StrategyEngine", "strategy_engine", "STRATEGY_AVAILABLE"]
except ImportError:
    STRATEGY_AVAILABLE = False
    StrategyEngine = None
    strategy_engine = None

# 2.22 SIMULATION
try:
    from .learning.simulation import SimulationEngine, simulation_engine
    SIMULATION_AVAILABLE = True
    __all__ += ["SimulationEngine", "simulation_engine", "SIMULATION_AVAILABLE"]
except ImportError:
    SIMULATION_AVAILABLE = False
    SimulationEngine = None
    simulation_engine = None

# 2.23 EVALUATOR
try:
    from .learning.evaluator import EvaluatorEngine, evaluator_engine
    EVALUATOR_AVAILABLE = True
    __all__ += ["EvaluatorEngine", "evaluator_engine", "EVALUATOR_AVAILABLE"]
except ImportError:
    EVALUATOR_AVAILABLE = False
    EvaluatorEngine = None
    evaluator_engine = None

# 2.24 ADAPTIVE
try:
    from .learning.adaptive import AdaptiveEngine, adaptive_engine
    ADAPTIVE_AVAILABLE = True
    __all__ += ["AdaptiveEngine", "adaptive_engine", "ADAPTIVE_AVAILABLE"]
except ImportError:
    ADAPTIVE_AVAILABLE = False
    AdaptiveEngine = None
    adaptive_engine = None

# 2.25 LEARNING ANALYZER
try:
    from .learning.analyzer import LearningAnalyzer, learning_analyzer
    LEARNING_ANALYZER_AVAILABLE = True
    __all__ += ["LearningAnalyzer", "learning_analyzer", "LEARNING_ANALYZER_AVAILABLE"]
except ImportError:
    LEARNING_ANALYZER_AVAILABLE = False
    LearningAnalyzer = None
    learning_analyzer = None

# 2.26 DATA PIPELINE
try:
    from .learning.collector import Collector
    from .learning.data_cleaner import DataCleaner
    from .learning.normalizer import Normalizer
    from .learning.feature_extractor import FeatureExtractor
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

# 2.27 ARCHIVE MANAGER
try:
    from .learning.archive_manager import ArchiveManager, archive_manager
    ARCHIVE_AVAILABLE = True
    __all__ += ["ArchiveManager", "archive_manager", "ARCHIVE_AVAILABLE"]
except ImportError:
    ARCHIVE_AVAILABLE = False
    ArchiveManager = None
    archive_manager = None

# 2.28 MODULE REGISTRY
try:
    from .learning.module_registry import ModuleRegistry, module_registry
    MODULE_REGISTRY_AVAILABLE = True
    __all__ += ["ModuleRegistry", "module_registry", "MODULE_REGISTRY_AVAILABLE"]
except ImportError:
    MODULE_REGISTRY_AVAILABLE = False
    ModuleRegistry = None
    module_registry = None

# 2.29 MODULE BASE
try:
    from .learning.module_base import ModuleBase
    __all__ += ["ModuleBase"]
except ImportError:
    ModuleBase = None

# 2.30 SERIALIZER
try:
    from .learning.serializer import SafeSerializer
    __all__ += ["SafeSerializer"]
except ImportError:
    SafeSerializer = None

# ============================================================
# 2.31 CONTRACTS
# ============================================================

try:
    from .learning.contracts import (
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

# 2.32 KNOWLEDGE BUILDER
try:
    from .learning.knowledge_builder import KnowledgeBuilder, knowledge_builder
    KNOWLEDGE_BUILDER_AVAILABLE = True
    __all__ += ["KnowledgeBuilder", "knowledge_builder", "KNOWLEDGE_BUILDER_AVAILABLE"]
except ImportError:
    KNOWLEDGE_BUILDER_AVAILABLE = False
    KnowledgeBuilder = None
    knowledge_builder = None

# 2.33 CURIOSITY
try:
    from .learning.curiosity import CuriosityEngine, curiosity_engine
    CURIOSITY_AVAILABLE = True
    __all__ += ["CuriosityEngine", "curiosity_engine", "CURIOSITY_AVAILABLE"]
except ImportError:
    CURIOSITY_AVAILABLE = False
    CuriosityEngine = None
    curiosity_engine = None

# 2.34 EXPERIENCE
try:
    from .learning.experience import ExperienceEngine, experience_engine
    EXPERIENCE_AVAILABLE = True
    __all__ += ["ExperienceEngine", "experience_engine", "EXPERIENCE_AVAILABLE"]
except ImportError:
    EXPERIENCE_AVAILABLE = False
    ExperienceEngine = None
    experience_engine = None

# 2.35 KNOWLEDGE GRAPH
try:
    from .learning.knowledge_graph import KnowledgeGraph, knowledge_graph
    KNOWLEDGE_GRAPH_AVAILABLE = True
    __all__ += ["KnowledgeGraph", "knowledge_graph", "KNOWLEDGE_GRAPH_AVAILABLE"]
except ImportError:
    KNOWLEDGE_GRAPH_AVAILABLE = False
    KnowledgeGraph = None
    knowledge_graph = None


# ============================================================
# 3. PACKAGE INFO
# ============================================================

def get_package_info() -> dict:
    """Get comprehensive package information."""
    return {
        "name": "core",
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "modules": {
            "adaptive": ADAPTIVE_AVAILABLE,
            "analyzer": ANALYZER_AVAILABLE,
            "archive": ARCHIVE_AVAILABLE,
            "association": ASSOCIATION_AVAILABLE,
            "autonomous": AUTONOMOUS_AVAILABLE,  # <-- BARU!
            "behavior": BEHAVIOR_AVAILABLE,
            "bootstrap": BOOTSTRAP_AVAILABLE,
            "bot": BOT_AVAILABLE,
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
            "pattern": PATTERN_ENGINE_AVAILABLE,
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
        },
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }


def health_summary() -> dict:
    """Get health summary of all modules."""
    info = get_package_info()
    modules = info["modules"]
    
    online = sum(1 for v in modules.values() if v)
    total = len(modules)
    
    return {
        "status": "HEALTHY" if online == total else "DEGRADED",
        "online": online,
        "total": total,
        "health_score": round((online / total) * 100, 2),
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }


def get_exchange_status() -> dict:
    """Get exchange connection status."""
    if not MARKET_DATA_AVAILABLE or kraken_market is None:
        return {
            "available": False,
            "status": "UNAVAILABLE",
            "message": "Market data module not available"
        }
    
    try:
        health = kraken_market.health_check()
        return {
            "available": True,
            "status": health.get("status", "UNKNOWN"),
            "pairs": len(kraken_market.pairs) if hasattr(kraken_market, 'pairs') else 0,
            "cache_size": len(kraken_market.cache) if hasattr(kraken_market, 'cache') else 0,
            "timestamp": health.get("timestamp", time.time()),
        }
    except Exception as e:
        return {
            "available": True,
            "status": "ERROR",
            "error": str(e),
        }


# ============================================================
# 4. INITIALIZATION - TAMPILAN RAPI 3 KOLOM
# ============================================================

print()
print("=" * 70)
print("  INKSIDE INTELLIGENCE OS v5.0 - ULTIMATE CORE")
print("  COGNITIVE MIRROR ENGINE")
print("=" * 70)
print()

info = get_package_info()
modules = info["modules"]

# Tampilan 3 kolom
module_list = sorted(modules.items())
cols = 3
rows = (len(module_list) + cols - 1) // cols

for row in range(rows):
    line = ""
    for col in range(cols):
        idx = row + col * rows
        if idx < len(module_list):
            name, available = module_list[idx]
            icon = "✓" if available else "✗"
            display = name[:20] + ".." if len(name) > 20 else name
            line += f"  [{icon}] {display:<22}"
    print(line)

print()
print("=" * 70)
health = health_summary()
print(f"  HEALTH: {health['health_score']:.1f}%  ({health['online']}/{health['total']})")
print("=" * 70)

# Exchange status
exchange_status = get_exchange_status()
if exchange_status.get("available"):
    print(f"  EXCHANGE: {exchange_status.get('status', 'UNKNOWN')}  (Pairs: {exchange_status.get('pairs', 0)})")
else:
    print(f"  EXCHANGE: UNAVAILABLE")
print("=" * 70)
print()


# ============================================================
# 5. END
# ============================================================
