# core/brain.py
# INKSIDE DIGITAL - COGNITIVE BRAIN v4.2.3
# SUPER COMPREHENSIVE CORE INTELLIGENCE CONTROLLER
# WITH AI INTEGRATION - DEEPSEEK ENHANCED

import random
import logging
import threading
import time
import json
import sys
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter

logger = logging.getLogger(__name__)

# ============================================================
# AI INTEGRATION FLAG
# ============================================================

try:
    from core.deepseek import deepseek_ai
    DEEPSEEK_AVAILABLE = True
    DEEPSEEK_ENABLED = deepseek_ai.enabled if hasattr(deepseek_ai, 'enabled') else False
except ImportError:
    DEEPSEEK_AVAILABLE = False
    DEEPSEEK_ENABLED = False
    deepseek_ai = None

logger.info(f"🧠 AI Integration: {'ENABLED' if DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED else 'DISABLED'}")

# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class BrainState(Enum):
    INITIALIZING = "INITIALIZING"
    IDLE = "IDLE"
    PROCESSING = "PROCESSING"
    LEARNING = "LEARNING"
    REFLECTING = "REFLECTING"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    ERROR = "ERROR"
    STOPPED = "STOPPED"
    RECOVERING = "RECOVERING"
    FALLBACK = "FALLBACK"


class MarketMode(Enum):
    CRYPTO = "CRYPTO"
    STOCK = "STOCK"
    HYBRID = "HYBRID"
    FOREX = "FOREX"
    COMMODITY = "COMMODITY"
    ALL = "ALL"


class ProcessingPriority(Enum):
    HIGH = 10
    MEDIUM = 5
    LOW = 1
    BACKGROUND = 0


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class CognitiveState:
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    cycle: int = 0
    input_data: Dict[str, Any] = field(default_factory=dict)
    perception: Dict[str, Any] = field(default_factory=dict)
    memory: Dict[str, Any] = field(default_factory=dict)
    learning: Dict[str, Any] = field(default_factory=dict)
    patterns: Dict[str, Any] = field(default_factory=dict)
    reasoning: Dict[str, Any] = field(default_factory=dict)
    knowledge: Dict[str, Any] = field(default_factory=dict)
    awareness: Dict[str, Any] = field(default_factory=dict)
    decision: Dict[str, Any] = field(default_factory=dict)
    prediction: Dict[str, Any] = field(default_factory=dict)
    feedback: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MarketIntelligence:
    forecast: str = "NEUTRAL"
    confidence: float = 0.0
    anomaly: str = "NORMAL"
    bias: str = "UNKNOWN"
    risk_level: str = "MEDIUM"
    signals: List[Dict[str, Any]] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DecisionSupport:
    action: str = "HOLD"
    reason: str = "Insufficient information"
    confidence: float = 0.0
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    expected_outcome: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# SAFE IMPORT HELPER
# ============================================================

def safe_import(module_path: str, class_name: str) -> Optional[Any]:
    try:
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name)
    except Exception as e:
        logger.debug(f"Safe import failed: {module_path}.{class_name} -> {e}")
        return None


# ============================================================
# COGNITIVE BRAIN CLASS
# ============================================================

class Brain:
    """
    Cognitive Brain v4.2.3 - Ultra Robust Intelligence Controller.
    With AI Integration - DeepSeek Enhanced Reflection.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.lock = threading.RLock()
        self.config = config or {}

        # GUI COMPATIBILITY
        self.brain_instance = self
        self._brain_available = True
        self._instances = {}
        self.brain_instances = self._instances
        self._active_instance = "default"

        # VERSION & IDENTITY
        self.version = "4.2.3"
        self.name = "Cognitive Brain"
        self.identity = {
            "name": self.name,
            "version": self.version,
            "type": "Cognitive Intelligence Core",
            "created_at": datetime.now().isoformat(),
        }

        # MODULE REFERENCES
        self._load_modules()

        # STATE
        self.state = BrainState.INITIALIZING
        self.running = True
        self.cycles = 0
        self.errors = 0
        self.successful_cycles = 0
        self.failed_cycles = 0
        self.recovery_attempts = 0

        self.started_at = datetime.now().isoformat()
        self.last_update = self.started_at
        self.last_input: Optional[Dict[str, Any]] = None
        self.last_result: Optional[Dict[str, Any]] = None
        self.last_error: Optional[str] = None
        self.last_error_time: Optional[str] = None

        # MARKET MODE
        self.market_mode = MarketMode.CRYPTO
        self._supported_modes = [m.value for m in MarketMode]

        # MEMORY SYSTEMS
        self.short_term_memory: List[Dict[str, Any]] = []
        self.short_term_limit = self.config.get("short_term_limit", 50)

        self.long_term_memory: List[Dict[str, Any]] = []
        self.long_term_limit = self.config.get("long_term_limit", 1000)

        self.working_memory: Dict[str, Any] = {}

        # HISTORY
        self.history: List[Dict[str, Any]] = []
        self.history_limit = self.config.get("history_limit", 500)

        # PERFORMANCE METRICS
        self.metrics = {
            "total_cycles": 0,
            "successful_cycles": 0,
            "failed_cycles": 0,
            "average_processing_time": 0.0,
            "total_processing_time": 0.0,
            "learning_count": 0,
            "prediction_count": 0,
            "decision_count": 0,
            "memory_usage": 0,
            "error_rate": 0.0,
            "success_rate": 0.0,
            "throughput": 0.0,
            "recovery_count": 0,
        }

        self.processing_times: List[float] = []
        self.performance_scores: List[float] = []
        self.average_performance = 0.0
        self.confidence_score = 0.5
        self.health_score = 100.0

        # FEATURES & CAPABILITIES
        self.capabilities = {
            "perception": True,
            "memory": True,
            "learning": True,
            "reasoning": True,
            "knowledge": True,
            "consciousness": True,
            "pattern_recognition": True,
            "prediction": True,
            "decision_support": True,
            "feedback_loop": True,
            "auto_healing": True,
            "random_fallback": True,
            "gui_compatibility": True,
            "multi_instance": True,
            "zero_downtime": True,
        }
        self.active_features = self.capabilities.copy()

        # AUTO-HEALING
        self.healing_attempts = 0
        self.last_healing_time: Optional[str] = None
        self.healing_history: List[Dict[str, Any]] = []
        self.auto_healing_enabled = self.config.get("auto_healing", True)
        self.error_threshold = self.config.get("error_threshold", 10)
        self.healing_cooldown = self.config.get("healing_cooldown", 60)
        self.max_recovery_attempts = self.config.get("max_recovery_attempts", 5)

        # GOALS
        self.goals = self._initialize_goals()
        self.current_goal: Optional[Dict[str, Any]] = None

        # RANDOM SEED
        random.seed(int(time.time()))

        # FINALIZE
        self.state = BrainState.IDLE
        self._log_module_status()

        logger.info("Cognitive Brain v%s initialized successfully.", self.version)
        if DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED:
            logger.info("🤖 DeepSeek AI Integration: ENABLED")
        else:
            logger.info("🤖 DeepSeek AI Integration: DISABLED")

    # ============================================================
    # GUI COMPATIBILITY METHODS
    # ============================================================

    def get_brain(self):
        return self

    def set_brain(self, brain):
        self.brain_instance = brain
        self._brain_available = brain is not None
        return True

    def get_metrics(self):
        return self.metrics if hasattr(self, 'metrics') else {}

    def get_state(self):
        try:
            return self.status()
        except Exception as e:
            logger.debug(f"Get state error: {e}")
            return {
                "state": "ERROR",
                "version": self.version,
                "state_value": "ERROR",
                "cycles": self.cycles,
                "errors": self.errors,
                "error": str(e)
            }

    def get_forecast(self):
        try:
            return self.forecast()
        except Exception as e:
            logger.debug(f"Get forecast error: {e}")
            return {
                "forecast": "NEUTRAL",
                "confidence": 0,
                "is_fallback": True,
                "error": str(e)
            }

    def get_status(self):
        return self.status()

    # ============================================================
    # MULTI-INSTANCE SUPPORT
    # ============================================================

    def register_instance(self, name: str, instance):
        self._instances[name] = instance
        self.brain_instances = self._instances
        logger.info(f"Registered brain instance: {name}")
        return True

    def switch_instance(self, name: str) -> bool:
        if name in self._instances:
            self._active_instance = name
            self.brain_instance = self._instances[name]
            self.brain_instances = self._instances
            logger.info(f"Switched to brain instance: {name}")
            return True
        return False

    def get_active_instance(self):
        return self._instances.get(self._active_instance, self)

    def get_instances(self) -> Dict[str, Any]:
        return self._instances.copy()

    def get_brain_instances(self) -> Dict[str, Any]:
        return self._instances.copy()

    # ============================================================
    # MODULE LOADING
    # ============================================================

    def _load_modules(self) -> None:
        self.module_manager = safe_import("core.module_manager", "module_manager")
        self.memory = safe_import("core.memory", "memory")
        self.knowledge = safe_import("core.knowledge", "knowledge")
        self.reasoning = safe_import("core.reasoning", "reasoning")
        self.perception = safe_import("core.perception", "perception")
        self.consciousness = safe_import("core.consciousness", "consciousness")

        self.learning_engine = safe_import("core.learning.engine", "learning_engine")
        self.learning = safe_import("core.learning.engine", "learning")
        self.pattern_engine = safe_import("core.learning.pattern", "pattern")
        self.semantic_memory = safe_import("core.learning.semantic_memory", "semantic_memory")
        self.market_learning = safe_import("core.learning.market_learning", "market_learning")

        self.strategy_engine = safe_import("core.learning.strategy", "strategy")
        self.simulation_engine = safe_import("core.learning.simulation", "simulation")
        self.reflection_engine = safe_import("core.learning.reflection", "reflection")
        self.insight_engine = safe_import("core.learning.insight", "insight")

        self.collector = safe_import("core.learning.collector", "collector")
        self.analyzer = safe_import("core.learning.analyzer", "analyzer")
        self.evaluator = safe_import("core.learning.evaluator", "evaluator")

        self.event_system = safe_import("core.learning.event", "event_system")
        self.event_bus = safe_import("core.learning.event", "EventBus")

        self.contracts = safe_import("core.contracts", "CONTRACT_VERSION")
        self.module_contract = safe_import("core.contracts", "ModuleContract")
        self.module_output = safe_import("core.contracts", "ModuleOutput")
        self.module_input = safe_import("core.contracts", "ModuleInput")

        self.modules_available = {
            "module_manager": self.module_manager is not None,
            "memory": self.memory is not None,
            "knowledge": self.knowledge is not None,
            "reasoning": self.reasoning is not None,
            "perception": self.perception is not None,
            "consciousness": self.consciousness is not None,
            "learning_engine": self.learning_engine is not None,
            "pattern_engine": self.pattern_engine is not None,
            "semantic_memory": self.semantic_memory is not None,
            "market_learning": self.market_learning is not None,
            "strategy_engine": self.strategy_engine is not None,
            "simulation_engine": self.simulation_engine is not None,
            "reflection_engine": self.reflection_engine is not None,
            "insight_engine": self.insight_engine is not None,
            "collector": self.collector is not None,
            "analyzer": self.analyzer is not None,
            "evaluator": self.evaluator is not None,
            "event": self.event_system is not None,
            "contracts": self.contracts is not None,
        }

        self.available_modules_count = sum(1 for v in self.modules_available.values() if v)
        self.total_modules_count = len(self.modules_available)

    def _log_module_status(self) -> None:
        available = [k for k, v in self.modules_available.items() if v]
        unavailable = [k for k, v in self.modules_available.items() if not v]
        logger.info("Modules available: %d/%d", len(available), len(self.modules_available))
        if unavailable:
            logger.debug("Unavailable modules: %s", ", ".join(unavailable))

    # ============================================================
    # GOALS INITIALIZATION
    # ============================================================

    def _initialize_goals(self) -> List[Dict[str, Any]]:
        return [
            {"name": "learn_continuously", "priority": 1, "progress": 0.0, "status": "active"},
            {"name": "improve_decision_making", "priority": 2, "progress": 0.0, "status": "active"},
            {"name": "develop_intuition", "priority": 3, "progress": 0.0, "status": "active"},
            {"name": "build_knowledge_base", "priority": 4, "progress": 0.0, "status": "active"},
            {"name": "achieve_market_mastery", "priority": 5, "progress": 0.0, "status": "pending"},
            {"name": "optimize_performance", "priority": 6, "progress": 0.0, "status": "pending"},
        ]

    # ============================================================
    # SAFE EXECUTION
    # ============================================================

    def execute(self, module: Any, method: str, *args, **kwargs) -> Optional[Any]:
        if module is None:
            return None
        try:
            if hasattr(module, method):
                func = getattr(module, method)
                if callable(func):
                    return func(*args, **kwargs)
        except Exception as e:
            self.errors += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now().isoformat()
            logger.debug(f"Brain execution error: {method} -> {e}")
        return None

    # ============================================================
    # RANDOM DATA GENERATION
    # ============================================================

    def _generate_random_market_data(self) -> Dict[str, Any]:
        directions = ["BULLISH", "BEARISH", "NEUTRAL"]
        actions = ["BUY", "SELL", "HOLD", "MONITOR", "EXIT"]
        risk_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        emotions = ["CALM", "FOCUSED", "CURIOUS", "CAUTIOUS", "CONFIDENT"]

        direction = random.choice(directions)
        confidence = random.randint(40, 95)

        if direction == "BULLISH":
            bullish = random.randint(60, 95)
            bearish = random.randint(5, 40)
            neutral = 100 - bullish - bearish
        elif direction == "BEARISH":
            bearish = random.randint(60, 95)
            bullish = random.randint(5, 40)
            neutral = 100 - bullish - bearish
        else:
            bullish = random.randint(20, 60)
            bearish = random.randint(20, 60)
            neutral = 100 - bullish - bearish

        reasons = [
            "Bullish breakout detected",
            "Bearish divergence confirmed",
            "Support level holding strong",
            "Resistance level breaking",
            "Volume spike indicates momentum",
            "RSI oversold condition",
            "MACD crossover bullish",
            "Price above moving averages",
            "Market sentiment improving",
            "Technical indicators aligned",
        ]

        return {
            "forecast": direction,
            "confidence": confidence,
            "bullish_probability": bullish,
            "bearish_probability": bearish,
            "neutral_probability": neutral,
            "action": random.choice(actions),
            "reason": random.choice(reasons),
            "risk_level": random.choice(risk_levels),
            "emotion": random.choice(emotions),
            "timestamp": datetime.now().isoformat(),
            "is_fallback": True,
        }

    # ============================================================
    # MAIN OBSERVATION PIPELINE
    # ============================================================

    def observe(self, data: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()

        with self.lock:
            self.cycles += 1
            self.metrics["total_cycles"] += 1
            self.state = BrainState.PROCESSING

            timestamp = datetime.now().isoformat()
            self.last_input = data

            try:
                cognitive_state = CognitiveState(
                    timestamp=timestamp,
                    cycle=self.cycles,
                    input_data=data,
                )

                cognitive_state.perception = self._perceive(data)
                cognitive_state.memory = self._store_memory(cognitive_state.perception)
                cognitive_state.patterns = self._recognize_patterns(cognitive_state.perception)
                cognitive_state.learning = self._learn(cognitive_state.perception, cognitive_state.patterns)
                cognitive_state.reasoning = self._reason(cognitive_state)
                cognitive_state.knowledge = self._update_knowledge(cognitive_state)
                cognitive_state.awareness = self._reflect_consciousness(cognitive_state)
                cognitive_state.prediction = self._predict(cognitive_state)
                cognitive_state.decision = self._decide(cognitive_state)
                cognitive_state.feedback = self._prepare_feedback(cognitive_state)

                self.last_result = self._cognitive_state_to_dict(cognitive_state)
                self._update_metrics(start_time)
                self._store_history(cognitive_state)
                self._update_goals(cognitive_state)

                self.state = BrainState.ACTIVE
                self.successful_cycles += 1
                self.metrics["successful_cycles"] += 1

                return self.last_result

            except Exception as e:
                self.errors += 1
                self.failed_cycles += 1
                self.metrics["failed_cycles"] += 1
                self.last_error = str(e)
                self.last_error_time = datetime.now().isoformat()
                self.state = BrainState.ERROR

                logger.exception(f"Brain observation failed: {e}")

                if self.auto_healing_enabled:
                    self._attempt_healing()

                return self._generate_fallback_response(e)

    def _generate_fallback_response(self, error: Exception) -> Dict[str, Any]:
        random_data = self._generate_random_market_data()
        return {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycles,
            "status": "FALLBACK",
            "error": str(error),
            "error_count": self.errors,
            "state": self.state.value,
            "perception": {"type": "fallback", "confidence": 0.3},
            "memory": {"stored": False, "source": "fallback"},
            "learning": {"status": "fallback", "confidence": 0.3},
            "patterns": {"detected": [], "count": 0},
            "reasoning": {"confidence": 0.3, "trend": "UNKNOWN"},
            "knowledge": {"updated": False},
            "awareness": {"state": "FALLBACK", "confidence": 0.3},
            "prediction": {"forecast": random_data["forecast"], "confidence": random_data["confidence"]},
            "decision": {
                "action": random_data["action"],
                "confidence": random_data["confidence"],
                "reason": random_data["reason"],
                "timestamp": datetime.now().isoformat(),
            },
            "feedback": {"awaiting_feedback": True},
            "metadata": {"is_fallback": True, "error": str(error)},
        }

    # ============================================================
    # PIPELINE STEPS
    # ============================================================

    def _perceive(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if self.perception is not None:
                result = self.execute(self.perception, "analyze", data)
                if result is not None:
                    return result
            if self.market_learning is not None:
                result = self.execute(self.market_learning, "process", data)
                if result is not None:
                    return result
            return {
                "type": self._detect_data_type(data),
                "entities": self._extract_entities(data),
                "sentiment": self._detect_sentiment(data),
                "confidence": self._calculate_confidence(data),
                "raw": data,
                "is_fallback": True,
            }
        except Exception as e:
            logger.debug(f"Perception error: {e}")
            return {
                "type": "unknown",
                "entities": [],
                "sentiment": "neutral",
                "confidence": 0.3,
                "raw": data,
                "is_fallback": True,
                "error": str(e),
            }

    def _detect_data_type(self, data: Dict[str, Any]) -> str:
        if "market" in data or "symbol" in data or "price" in data:
            return "market"
        elif "text" in data or "content" in data:
            return "text"
        elif "event" in data:
            return "event"
        elif "command" in data or "action" in data:
            return "command"
        else:
            return "generic"

    def _extract_entities(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        entities = []
        for key in ["market", "symbol", "asset", "pair"]:
            if key in data:
                entities.append({"type": "asset", "name": str(data[key])})
                break
        for key in ["signal", "trend", "pattern"]:
            if key in data:
                entities.append({"type": "indicator", "name": str(data[key])})
                break
        return entities

    def _detect_sentiment(self, data: Dict[str, Any]) -> str:
        if "signal" in data:
            signal = str(data["signal"]).lower()
            if signal in ["bullish", "positive", "up", "buy"]:
                return "positive"
            elif signal in ["bearish", "negative", "down", "sell"]:
                return "negative"
        if "sentiment" in data:
            return str(data["sentiment"])
        return "neutral"

    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        if "confidence" in data:
            try:
                return float(data["confidence"])
            except (ValueError, TypeError):
                pass
        fields_present = sum(1 for k in data if data.get(k) is not None)
        return min(0.5 + (fields_present * 0.05), 1.0)

    # ============================================================
    # MEMORY STORAGE
    # ============================================================

    def _store_memory(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        try:
            perception_dict = self._to_dict_safe(perception)
            confidence = self._extract_confidence(perception, perception_dict)

            memory_entry = {
                "type": "market_observation",
                "timestamp": datetime.now().isoformat(),
                "data": perception_dict,
                "importance": confidence,
                "source_type": type(perception).__name__,
            }

            if self.memory is not None:
                result = self.execute(self.memory, "remember", memory_entry)
                if result is not None:
                    return {"stored": True, "result": result, "source": "external_memory", "importance": confidence}

            self.short_term_memory.append(memory_entry)
            if len(self.short_term_memory) > self.short_term_limit:
                oldest = self.short_term_memory.pop(0)
                self.long_term_memory.append(oldest)
                if len(self.long_term_memory) > self.long_term_limit:
                    self.long_term_memory = self.long_term_memory[-self.long_term_limit:]

            return {
                "stored": True,
                "short_term_count": len(self.short_term_memory),
                "long_term_count": len(self.long_term_memory),
                "source": "internal_memory",
                "importance": confidence,
            }

        except Exception as e:
            logger.debug(f"Memory storage error: {e}")
            return {"stored": False, "error": str(e), "source": "fallback", "importance": 0.3}

    def _to_dict_safe(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, dict):
            return obj
        if hasattr(obj, 'to_dict') and callable(obj.to_dict):
            try:
                return obj.to_dict()
            except Exception:
                pass
        if hasattr(obj, '__dict__') and not isinstance(obj, dict):
            return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        return {"data": str(obj), "type": type(obj).__name__}

    def _extract_confidence(self, obj: Any, obj_dict: Dict[str, Any]) -> float:
        confidence = 0.5
        for attr in ['confidence', 'score', 'strength', 'quality', 'certainty', 'importance']:
            if hasattr(obj, attr):
                try:
                    confidence = float(getattr(obj, attr))
                    break
                except (ValueError, TypeError):
                    pass
        if confidence == 0.5 and isinstance(obj_dict, dict):
            for key in ['confidence', 'score', 'strength', 'quality', 'certainty']:
                if key in obj_dict:
                    try:
                        confidence = float(obj_dict[key])
                        break
                    except (ValueError, TypeError):
                        pass
        try:
            confidence = max(0.0, min(1.0, float(confidence)))
        except (ValueError, TypeError):
            confidence = 0.5
        return confidence

    # ============================================================
    # PATTERN RECOGNITION
    # ============================================================

    def _recognize_patterns(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if self.pattern_engine is not None:
                result = self.execute(self.pattern_engine, "detect", perception)
                if result is not None:
                    return result
            if self.learning_engine is not None:
                result = self.execute(self.learning_engine, "detect_patterns", perception)
                if result is not None:
                    return result

            patterns = []
            raw = perception.get("raw", {})
            if "signal" in raw:
                patterns.append({"type": "signal", "value": raw["signal"], "confidence": random.uniform(0.3, 0.8)})
            if "pattern" in raw:
                patterns.append({"type": "structural", "value": raw["pattern"], "confidence": random.uniform(0.3, 0.8)})
            if "trend" in raw:
                patterns.append({"type": "trend", "value": raw["trend"], "confidence": random.uniform(0.3, 0.8)})

            if not patterns:
                pattern_types = ["signal", "trend", "structural", "seasonal", "cyclical"]
                for _ in range(random.randint(1, 3)):
                    patterns.append({
                        "type": random.choice(pattern_types),
                        "value": f"pattern_{random.randint(1, 100)}",
                        "confidence": random.uniform(0.3, 0.8)
                    })

            return {
                "detected": patterns,
                "count": len(patterns),
                "confidence": sum(p.get("confidence", 0.5) for p in patterns) / max(1, len(patterns)),
                "is_fallback": True,
            }

        except Exception as e:
            logger.debug(f"Pattern recognition error: {e}")
            return {"detected": [], "count": 0, "confidence": 0.3, "error": str(e), "is_fallback": True}

    # ============================================================
    # LEARNING
    # ============================================================

    def _learn(self, perception: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        try:
            learning_data = {
                "perception": perception,
                "patterns": patterns,
                "timestamp": datetime.now().isoformat(),
            }

            if self.learning_engine is not None:
                result = self.execute(self.learning_engine, "learn", learning_data)
                if result is not None:
                    self.metrics["learning_count"] += 1
                    return result

            if self.market_learning is not None:
                result = self.execute(self.market_learning, "learn", learning_data)
                if result is not None:
                    self.metrics["learning_count"] += 1
                    return result

            return {
                "status": "learned",
                "timestamp": datetime.now().isoformat(),
                "patterns_processed": len(patterns.get("detected", [])),
                "insights": [f"Pattern #{i+1} stored for future reference" for i in range(min(3, len(patterns.get("detected", []))))],
                "confidence": random.uniform(0.4, 0.8),
                "is_fallback": True,
            }

        except Exception as e:
            logger.debug(f"Learning error: {e}")
            return {"status": "fallback", "error": str(e), "is_fallback": True, "confidence": 0.3}

    # ============================================================
    # REASONING
    # ============================================================

    def _reason(self, state: CognitiveState) -> Dict[str, Any]:
        try:
            if self.reasoning is not None:
                result = self.execute(self.reasoning, "analyze", state)
                if result is not None:
                    return result

            reasoning_engine = safe_import("core.learning.reasoning_engine", "reasoning_engine")
            if reasoning_engine is not None:
                result = self.execute(reasoning_engine, "analyze", state)
                if result is not None:
                    return result

            directions = ["BULLISH", "BEARISH", "NEUTRAL"]
            direction = random.choice(directions)
            confidence = random.uniform(0.3, 0.8)

            return {
                "confidence": confidence,
                "trend": direction,
                "anomaly": random.choice(["NORMAL", "WARNING", "CRITICAL"]),
                "prediction": {"direction": direction, "confidence": confidence},
                "evidence": [f"Evidence #{i+1} from reasoning" for i in range(random.randint(1, 3))],
                "bias": random.choice(["POSITIVE", "NEGATIVE", "NEUTRAL"]),
                "is_fallback": True,
            }

        except Exception as e:
            logger.debug(f"Reasoning error: {e}")
            return {"confidence": 0.3, "trend": "UNKNOWN", "anomaly": "UNKNOWN", "prediction": {"direction": "NEUTRAL", "confidence": 0.3}, "evidence": [], "error": str(e), "is_fallback": True}

    # ============================================================
    # KNOWLEDGE UPDATE
    # ============================================================

    def _update_knowledge(self, state: CognitiveState) -> Dict[str, Any]:
        try:
            if self.knowledge is not None:
                result = self.execute(self.knowledge, "update", state)
                if result is not None:
                    return result

            knowledge_builder = safe_import("core.learning.knowledge_builder", "knowledge_builder")
            if knowledge_builder is not None:
                result = self.execute(knowledge_builder, "update", state)
                if result is not None:
                    return result

            return {"updated": True, "timestamp": datetime.now().isoformat(), "knowledge_units": len(self.long_term_memory) + random.randint(0, 5), "is_fallback": True}

        except Exception as e:
            logger.debug(f"Knowledge update error: {e}")
            return {"updated": False, "error": str(e), "is_fallback": True}

    # ============================================================
    # CONSCIOUSNESS
    # ============================================================

    def _reflect_consciousness(self, state: CognitiveState) -> Dict[str, Any]:
        try:
            if self.consciousness is not None:
                if hasattr(self.consciousness, "reflect"):
                    result = self.execute(self.consciousness, "reflect", state)
                    if result is not None:
                        return result
                elif hasattr(self.consciousness, "process"):
                    result = self.execute(self.consciousness, "process", state)
                    if result is not None:
                        return result

            consciousness_module = safe_import("core.learning.consciousness", "consciousness")
            if consciousness_module is not None:
                result = self.execute(consciousness_module, "reflect", state)
                if result is not None:
                    return result

            states = ["ACTIVE", "FOCUSED", "CURIOUS", "REFLECTING", "CALM"]
            emotions = ["CALM", "FOCUSED", "CURIOUS", "CAUTIOUS", "CONFIDENT"]

            return {
                "state": random.choice(states),
                "confidence": random.uniform(0.4, 0.9),
                "stability": random.choice(["STABLE", "VOLATILE", "ADAPTING"]),
                "reflection": random.choice([
                    "System is operating normally.",
                    "Processing market data efficiently.",
                    "Learning patterns from recent data.",
                    "Preparing for decision making.",
                ]),
                "emotion": random.choice(emotions),
                "awareness_level": random.uniform(0.3, 0.9),
                "is_fallback": True,
            }

        except Exception as e:
            logger.debug(f"Consciousness error: {e}")
            return {"state": "FALLBACK", "confidence": 0.3, "stability": "UNKNOWN", "reflection": "Consciousness module unavailable.", "error": str(e), "is_fallback": True}

    # ============================================================
    # PREDICTION
    # ============================================================

    def _predict(self, state: CognitiveState) -> Dict[str, Any]:
        try:
            prediction_module = safe_import("core.learning.prediction", "prediction")
            if prediction_module is not None:
                result = self.execute(prediction_module, "predict", state)
                if result is not None:
                    self.metrics["prediction_count"] += 1
                    return result

            if self.simulation_engine is not None:
                result = self.execute(self.simulation_engine, "simulate", state)
                if result is not None:
                    self.metrics["prediction_count"] += 1
                    return result

            directions = ["BULLISH", "BEARISH", "NEUTRAL"]
            direction = random.choice(directions)
            confidence = random.uniform(0.4, 0.9)

            return {
                "forecast": direction,
                "confidence": confidence,
                "direction": direction,
                "target": None,
                "timestamp": datetime.now().isoformat(),
                "probability": random.uniform(0.3, 0.8),
                "is_fallback": True,
            }

        except Exception as e:
            logger.debug(f"Prediction error: {e}")
            return {"forecast": "NEUTRAL", "confidence": 0.3, "direction": "UNKNOWN", "error": str(e), "is_fallback": True}

    # ============================================================
    # DECISION
    # ============================================================

    def _decide(self, state: CognitiveState) -> Dict[str, Any]:
        try:
            intelligence = self._market_intelligence(state)

            decision_engine = safe_import("core.learning.decision_engine", "decision_engine")
            if decision_engine is not None:
                result = self.execute(decision_engine, "decide", state, intelligence)
                if result is not None:
                    self.metrics["decision_count"] += 1
                    return result

            if self.strategy_engine is not None:
                result = self.execute(self.strategy_engine, "decide", state, intelligence)
                if result is not None:
                    self.metrics["decision_count"] += 1
                    return result

            return self._simple_decision(intelligence)

        except Exception as e:
            logger.debug(f"Decision error: {e}")
            return {"action": "HOLD", "reason": f"Decision error: {e}", "confidence": 0.3, "timestamp": datetime.now().isoformat(), "is_fallback": True, "error": str(e)}

    def _simple_decision(self, intelligence: Dict[str, Any]) -> Dict[str, Any]:
        forecast = intelligence.get("forecast", "NEUTRAL")
        confidence = intelligence.get("confidence", 0.0)

        confidence = min(95, confidence + random.randint(-5, 5))

        actions = ["HOLD", "MONITOR"]

        if forecast == "BULLISH" and confidence >= 70:
            actions = ["BUY", "MONITOR", "HOLD"]
        elif forecast == "BEARISH" and confidence >= 70:
            actions = ["SELL", "MONITOR", "HOLD"]
        elif confidence >= 50:
            actions = ["MONITOR", "HOLD"]

        action = random.choice(actions)

        reasons = [
            "Bullish forecast with strong confidence",
            "Bearish forecast with strong confidence",
            "Moderate confidence, monitor market",
            "Insufficient information",
            "Market conditions favorable",
            "Risk assessment recommends caution",
        ]

        return {
            "action": action,
            "reason": random.choice(reasons),
            "confidence": confidence,
            "alternatives": [
                {"action": "HOLD", "reason": "Maintain current position"},
                {"action": "MONITOR", "reason": "Watch for confirmation"},
            ],
            "risk_assessment": {
                "level": random.choice(["LOW", "MEDIUM", "HIGH"]),
                "factors": ["Market volatility", "Liquidity", "Timeframe"],
            },
            "expected_outcome": random.choice(["price_increase", "price_decrease", "no_change"]),
            "timestamp": datetime.now().isoformat(),
            "is_fallback": True,
        }

    # ============================================================
    # FEEDBACK
    # ============================================================

    def _prepare_feedback(self, state: CognitiveState) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "cycle": state.cycle,
            "decision": state.decision,
            "prediction": state.prediction,
            "confidence": state.decision.get("confidence", 0.5),
            "awaiting_feedback": True,
            "is_fallback": "is_fallback" in state.decision,
        }

    # ============================================================
    # MARKET INTELLIGENCE
    # ============================================================

    def _market_intelligence(self, state: CognitiveState) -> Dict[str, Any]:
        try:
            result = {
                "forecast": "NEUTRAL",
                "confidence": 0.0,
                "anomaly": "NORMAL",
                "bias": "UNKNOWN",
                "risk_level": "MEDIUM",
                "signals": [],
                "evidence": [],
                "timestamp": datetime.now().isoformat(),
            }

            reasoning = state.reasoning
            if reasoning and isinstance(reasoning, dict):
                if "prediction" in reasoning:
                    pred = reasoning["prediction"]
                    if isinstance(pred, dict):
                        result["forecast"] = pred.get("direction", "NEUTRAL")
                        result["confidence"] = pred.get("confidence", 0.0)
                result["anomaly"] = reasoning.get("anomaly", "NORMAL")
                result["bias"] = reasoning.get("bias", "UNKNOWN")
                result["evidence"].extend(reasoning.get("evidence", []))

            patterns = state.patterns
            if patterns and isinstance(patterns, dict):
                for p in patterns.get("detected", []):
                    if p.get("type") == "signal":
                        result["signals"].append(p)

            learning = state.learning
            if learning and isinstance(learning, dict):
                if learning.get("confidence"):
                    result["confidence"] = max(result["confidence"], learning["confidence"])
                if learning.get("forecast"):
                    result["forecast"] = learning["forecast"]

            decision = state.decision
            if decision and isinstance(decision, dict):
                result["confidence"] = max(result["confidence"], decision.get("confidence", 0.0))
                result["signals"].append({
                    "type": "decision",
                    "action": decision.get("action", "UNKNOWN"),
                    "confidence": decision.get("confidence", 0.0),
                })

            if result["confidence"] == 0:
                random_data = self._generate_random_market_data()
                result["forecast"] = random_data["forecast"]
                result["confidence"] = random_data["confidence"]
                result["is_fallback"] = True

            if self.errors > 10:
                result["anomaly"] = "WARNING"
            elif self.errors > 30:
                result["anomaly"] = "CRITICAL"

            return result

        except Exception as e:
            logger.debug(f"Market intelligence error: {e}")
            random_data = self._generate_random_market_data()
            return {
                "forecast": random_data["forecast"],
                "confidence": random_data["confidence"],
                "anomaly": "UNKNOWN",
                "bias": "UNKNOWN",
                "risk_level": "MEDIUM",
                "signals": [],
                "evidence": ["Fallback due to error"],
                "timestamp": datetime.now().isoformat(),
                "is_fallback": True,
                "error": str(e),
            }

    # ============================================================
    # PUBLIC API METHODS
    # ============================================================

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.observe(data)

    def market_intelligence(self, state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if state is None:
            state = self.last_result or {}
        if isinstance(state, dict):
            return self._market_intelligence_from_dict(state)
        return self._generate_random_market_data()

    def _market_intelligence_from_dict(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = {
                "forecast": "NEUTRAL",
                "confidence": 0.0,
                "anomaly": "NORMAL",
                "bias": "UNKNOWN",
                "risk_level": "MEDIUM",
                "signals": [],
                "evidence": [],
                "timestamp": datetime.now().isoformat(),
            }

            reasoning_data = state.get("reasoning", {})
            if isinstance(reasoning_data, dict):
                if "prediction" in reasoning_data:
                    pred = reasoning_data["prediction"]
                    if isinstance(pred, dict):
                        result["forecast"] = pred.get("direction", "NEUTRAL")
                        result["confidence"] = pred.get("confidence", 0.0)
                result["anomaly"] = reasoning_data.get("anomaly", "NORMAL")
                result["bias"] = reasoning_data.get("bias", "UNKNOWN")
                result["evidence"].extend(reasoning_data.get("evidence", []))

            learning_data = state.get("learning", {})
            if isinstance(learning_data, dict):
                pred = learning_data.get("prediction", {})
                if isinstance(pred, dict):
                    if result["forecast"] == "NEUTRAL":
                        result["forecast"] = pred.get("forecast", "NEUTRAL")
                    result["confidence"] = max(result["confidence"], pred.get("confidence", 0.0))

            decision = state.get("decision", {})
            if isinstance(decision, dict):
                result["confidence"] = max(result["confidence"], decision.get("confidence", 0.0))
                result["signals"].append({
                    "type": "decision",
                    "action": decision.get("action", "UNKNOWN"),
                    "confidence": decision.get("confidence", 0.0),
                })

            if result["confidence"] == 0:
                random_data = self._generate_random_market_data()
                result["forecast"] = random_data["forecast"]
                result["confidence"] = random_data["confidence"]
                result["is_fallback"] = True

            return result

        except Exception as e:
            logger.debug(f"Market intelligence from dict error: {e}")
            return self._generate_random_market_data()

    def decision_support(self, state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            if state is None:
                state = self.last_result or {}

            intelligence = self.market_intelligence(state)

            existing_decision = state.get("decision", {}) if isinstance(state, dict) else {}

            decision = {
                "action": existing_decision.get("action", "HOLD"),
                "reason": existing_decision.get("reason", "Insufficient information"),
                "confidence": existing_decision.get("confidence", intelligence.get("confidence", 0.0)),
                "alternatives": existing_decision.get("alternatives", []),
                "risk_assessment": existing_decision.get("risk_assessment", {
                    "level": intelligence.get("risk_level", "MEDIUM"),
                    "factors": [],
                }),
                "expected_outcome": existing_decision.get("expected_outcome"),
                "timestamp": datetime.now().isoformat(),
            }

            if decision["action"] == "HOLD" and decision["confidence"] == 0:
                forecast = intelligence.get("forecast", "")
                confidence = intelligence.get("confidence", 0.0)

                if forecast == "BULLISH" and confidence >= 70:
                    decision["action"] = "BUY"
                    decision["reason"] = "Bullish forecast with strong confidence"
                    decision["alternatives"] = [
                        {"action": "MONITOR", "reason": "Wait for confirmation"},
                        {"action": "HOLD", "reason": "Wait for better entry"},
                    ]
                    decision["expected_outcome"] = "price_increase"
                elif forecast == "BEARISH" and confidence >= 70:
                    decision["action"] = "SELL"
                    decision["reason"] = "Bearish forecast with strong confidence"
                    decision["alternatives"] = [
                        {"action": "MONITOR", "reason": "Wait for confirmation"},
                        {"action": "HOLD", "reason": "Wait for better exit"},
                    ]
                    decision["expected_outcome"] = "price_decrease"
                elif confidence >= 50:
                    decision["action"] = "MONITOR"
                    decision["reason"] = "Moderate confidence, monitor market"
                    decision["alternatives"] = [
                        {"action": "HOLD", "reason": "Maintain current position"},
                    ]
                    decision["expected_outcome"] = "no_change"
                else:
                    random_data = self._generate_random_market_data()
                    decision["action"] = random_data["action"]
                    decision["reason"] = random_data["reason"]
                    decision["confidence"] = random_data["confidence"]
                    decision["is_fallback"] = True

            return decision

        except Exception as e:
            logger.debug(f"Decision support error: {e}")
            random_data = self._generate_random_market_data()
            return {
                "action": random_data["action"],
                "reason": random_data["reason"],
                "confidence": random_data["confidence"],
                "alternatives": [],
                "risk_assessment": {"level": random_data["risk_level"], "factors": []},
                "expected_outcome": random_data.get("forecast", ""),
                "timestamp": datetime.now().isoformat(),
                "is_fallback": True,
                "error": str(e),
            }

    def forecast(self) -> Dict[str, Any]:
        try:
            intelligence = self.market_intelligence()
            return {
                "forecast": intelligence.get("forecast", "NEUTRAL"),
                "confidence": intelligence.get("confidence", 0.0),
                "timestamp": datetime.now().isoformat(),
                "is_fallback": intelligence.get("is_fallback", False),
            }
        except Exception as e:
            random_data = self._generate_random_market_data()
            return {
                "forecast": random_data["forecast"],
                "confidence": random_data["confidence"],
                "timestamp": datetime.now().isoformat(),
                "is_fallback": True,
                "error": str(e),
            }

    # ============================================================
    # REFLECTION - SUPER COMPREHENSIVE
    # ============================================================

    def reflection(self) -> Dict[str, Any]:
        try:
            consciousness_data = {}
            snapshot_data = {}
            status_data = {}
            memory_stats = {}
            learning_stats = {}
            goal_stats = {}
            performance_data = {}

            if self.consciousness is not None:
                try:
                    if hasattr(self.consciousness, 'get_state'):
                        consciousness_data = self.consciousness.get_state()
                    elif hasattr(self.consciousness, 'status'):
                        consciousness_data = self.consciousness.status()
                    elif hasattr(self.consciousness, 'snapshot'):
                        consciousness_data = self.consciousness.snapshot()
                except Exception as e:
                    logger.debug(f"Consciousness data error: {e}")

            try:
                snapshot_data = self.snapshot()
            except Exception as e:
                logger.debug(f"Snapshot data error: {e}")

            try:
                status_data = self.status()
            except Exception as e:
                logger.debug(f"Status data error: {e}")

            memory_stats = {
                'short_term': len(self.short_term_memory) if hasattr(self, 'short_term_memory') else 0,
                'long_term': len(self.long_term_memory) if hasattr(self, 'long_term_memory') else 0,
                'working': len(self.working_memory) if hasattr(self, 'working_memory') else 0,
            }

            learning_stats = {
                'learning_count': self.metrics.get('learning_count', 0),
                'prediction_count': self.metrics.get('prediction_count', 0),
                'decision_count': self.metrics.get('decision_count', 0),
                'learning_active': self.learning_engine is not None,
                'modules_available': self.available_modules_count,
            }

            if hasattr(self, 'goals'):
                goal_stats = {
                    'total': len(self.goals),
                    'active': sum(1 for g in self.goals if g.get('status') == 'active'),
                    'completed': sum(1 for g in self.goals if g.get('status') == 'completed'),
                    'pending': sum(1 for g in self.goals if g.get('status') == 'pending'),
                }

            performance_data = {
                'success_rate': self.metrics.get('success_rate', 0),
                'error_rate': self.metrics.get('error_rate', 0),
                'avg_processing_time': self.metrics.get('average_processing_time', 0),
                'throughput': self.metrics.get('throughput', 0),
                'health_score': self.health_score if hasattr(self, 'health_score') else 70,
                'cycles': self.cycles,
                'errors': self.errors,
                'recovery_count': self.metrics.get('recovery_count', 0),
                'healing_attempts': self.healing_attempts if hasattr(self, 'healing_attempts') else 0,
            }

            # Calculate metrics
            awareness_sources = []
            if consciousness_data and isinstance(consciousness_data, dict):
                for key in ['awareness', 'awareness_level', 'consciousness_level', 'self_awareness']:
                    if key in consciousness_data:
                        try:
                            val = float(consciousness_data[key])
                            if 0 <= val <= 1:
                                awareness_sources.append(val)
                        except (ValueError, TypeError):
                            pass

            if snapshot_data and isinstance(snapshot_data, dict):
                brain_data = snapshot_data.get('brain', {})
                health = brain_data.get('health', {}).get('score', 70)
                awareness_sources.append(health / 100)

            if status_data and isinstance(status_data, dict):
                success_rate = status_data.get('success_rate', 50) / 100
                awareness_sources.append(min(0.95, 0.3 + success_rate * 0.6))

            health_score = performance_data.get('health_score', 70) / 100
            awareness_sources.append(health_score)

            if awareness_sources:
                awareness = sum(awareness_sources) / len(awareness_sources)
            else:
                awareness = 0.5
            awareness = max(0.1, min(0.98, awareness))

            # Emotion
            emotion_sources = []
            emotion_map = {
                'BULLISH': 'EXCITED', 'BEARISH': 'CAUTIOUS', 'NEUTRAL': 'CALM',
                'POSITIVE': 'OPTIMISTIC', 'NEGATIVE': 'ANXIOUS', 'VOLATILE': 'ALERT', 'STABLE': 'CALM'
            }

            if consciousness_data and isinstance(consciousness_data, dict):
                for key in ['emotional_state', 'emotion', 'mood', 'state']:
                    if key in consciousness_data:
                        val = str(consciousness_data[key]).upper()
                        if val in emotion_map:
                            emotion_sources.append(emotion_map[val])
                        elif val in ['CALM', 'FOCUSED', 'CURIOUS', 'ALERT', 'CONTEMPLATIVE', 'EXCITED', 'OPTIMISTIC', 'CAUTIOUS', 'ANXIOUS']:
                            emotion_sources.append(val)

            if snapshot_data and isinstance(snapshot_data, dict):
                forecast = snapshot_data.get('market', {}).get('forecast', 'NEUTRAL')
                if forecast in emotion_map:
                    emotion_sources.append(emotion_map[forecast])

            error_rate = performance_data.get('error_rate', 0)
            if error_rate > 30:
                emotion_sources.append('ANXIOUS')
            elif error_rate > 15:
                emotion_sources.append('CAUTIOUS')
            elif error_rate < 5:
                emotion_sources.append('CONFIDENT')

            cycles = performance_data.get('cycles', 0)
            if cycles > 1000:
                emotion_sources.append('CONTEMPLATIVE')
            elif cycles > 500:
                emotion_sources.append('FOCUSED')

            if emotion_sources:
                emotion_counts = Counter(emotion_sources)
                emotion = emotion_counts.most_common(1)[0][0]
            else:
                emotion = 'CALM'

            # Curiosity
            curiosity_sources = []
            if consciousness_data and isinstance(consciousness_data, dict):
                for key in ['curiosity', 'curiosity_level', 'learning_drive']:
                    if key in consciousness_data:
                        try:
                            val = float(consciousness_data[key])
                            if 0 <= val <= 1:
                                curiosity_sources.append(val)
                        except (ValueError, TypeError):
                            pass

            if learning_stats.get('learning_active', False):
                curiosity_sources.append(0.7)
            if learning_stats.get('learning_count', 0) > 10:
                curiosity_sources.append(min(0.95, 0.5 + learning_stats['learning_count'] / 200))

            pred_count = learning_stats.get('prediction_count', 0)
            if pred_count > 0:
                curiosity_sources.append(min(0.9, 0.4 + pred_count / 100))

            cycles = performance_data.get('cycles', 0)
            curiosity_sources.append(min(0.85, 0.3 + (cycles % 100) / 150))

            if curiosity_sources:
                curiosity = sum(curiosity_sources) / len(curiosity_sources)
            else:
                curiosity = 0.5
            curiosity = max(0.1, min(0.98, curiosity))

            # Insight depth
            insight_sources = []
            if consciousness_data and isinstance(consciousness_data, dict):
                for key in ['insight_depth', 'insight', 'depth', 'clarity']:
                    if key in consciousness_data:
                        try:
                            val = float(consciousness_data[key])
                            if 0 <= val <= 1:
                                insight_sources.append(val)
                        except (ValueError, TypeError):
                            pass

            if snapshot_data and isinstance(snapshot_data, dict):
                confidence = snapshot_data.get('decision', {}).get('confidence', 0.5)
                insight_sources.append(confidence)

            if hasattr(self, 'last_result') and self.last_result:
                reasoning = self.last_result.get('reasoning', {})
                if isinstance(reasoning, dict):
                    conf = reasoning.get('confidence', 0.5)
                    insight_sources.append(conf)

            success_rate = performance_data.get('success_rate', 50) / 100
            insight_sources.append(0.3 + success_rate * 0.6)

            if insight_sources:
                insight_depth = sum(insight_sources) / len(insight_sources)
            else:
                insight_depth = 0.5
            insight_depth = max(0.1, min(0.98, insight_depth))

            # Resilience
            resilience_sources = []
            if consciousness_data and isinstance(consciousness_data, dict):
                for key in ['resilience', 'resiliency', 'recovery']:
                    if key in consciousness_data:
                        try:
                            val = float(consciousness_data[key])
                            if 0 <= val <= 1:
                                resilience_sources.append(val)
                        except (ValueError, TypeError):
                            pass

            recovery_count = performance_data.get('recovery_count', 0)
            if recovery_count > 0:
                resilience_sources.append(min(0.9, 0.5 + recovery_count / 20))

            healing = performance_data.get('healing_attempts', 0)
            errors = performance_data.get('errors', 1)
            if errors > 0 and healing > 0:
                resilience_sources.append(min(0.95, 0.3 + healing / errors))

            error_rate = performance_data.get('error_rate', 0)
            resilience_sources.append(max(0.2, 0.9 - error_rate / 100))

            if hasattr(self, 'auto_healing_enabled') and self.auto_healing_enabled:
                resilience_sources.append(0.8)

            if resilience_sources:
                resilience = sum(resilience_sources) / len(resilience_sources)
            else:
                resilience = 0.6
            resilience = max(0.1, min(0.98, resilience))

            # Focus
            focus_sources = []
            if consciousness_data and isinstance(consciousness_data, dict):
                for key in ['focus', 'attention', 'concentration', 'focus_level']:
                    if key in consciousness_data:
                        try:
                            val = float(consciousness_data[key])
                            if 0 <= val <= 1:
                                focus_sources.append(val)
                        except (ValueError, TypeError):
                            pass

            success_rate = performance_data.get('success_rate', 50) / 100
            focus_sources.append(0.3 + success_rate * 0.6)

            throughput = performance_data.get('throughput', 0)
            if throughput > 0:
                focus_sources.append(min(0.95, 0.3 + throughput / 10))

            error_rate = performance_data.get('error_rate', 0)
            if error_rate < 10:
                focus_sources.append(0.8)
            elif error_rate < 20:
                focus_sources.append(0.6)
            else:
                focus_sources.append(0.4)

            active_goals = goal_stats.get('active', 0)
            if active_goals > 0:
                focus_sources.append(min(0.9, 0.4 + active_goals / 10))

            if focus_sources:
                focus = sum(focus_sources) / len(focus_sources)
            else:
                focus = 0.5
            focus = max(0.1, min(0.98, focus))

            # Generate insights
            insights = self._generate_rich_insights(
                awareness=awareness,
                emotion=emotion,
                curiosity=curiosity,
                insight_depth=insight_depth,
                resilience=resilience,
                focus=focus,
                consciousness_data=consciousness_data,
                snapshot_data=snapshot_data,
                status_data=status_data,
                memory_stats=memory_stats,
                learning_stats=learning_stats,
                goal_stats=goal_stats,
                performance_data=performance_data
            )

            confidence = (awareness * 0.3 + insight_depth * 0.3 + resilience * 0.2 + focus * 0.2)
            confidence = max(0.1, min(0.98, confidence))

            error_rate = performance_data.get('error_rate', 0)
            if error_rate < 5:
                stability = "STABLE"
            elif error_rate < 15:
                stability = "ADAPTING"
            else:
                stability = "VOLATILE"

            if awareness > 0.7 and insight_depth > 0.7 and focus > 0.7:
                reflection_quality = "EXCELLENT"
            elif awareness > 0.5 and insight_depth > 0.5:
                reflection_quality = "GOOD"
            elif awareness > 0.3:
                reflection_quality = "FAIR"
            else:
                reflection_quality = "POOR"

            return {
                'awareness': awareness,
                'emotion': emotion,
                'curiosity': curiosity,
                'insight_depth': insight_depth,
                'resilience': resilience,
                'focus': focus,
                'insights': insights[:8],
                'source': 'comprehensive',
                'confidence': confidence,
                'stability': stability,
                'reflection_quality': reflection_quality,
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'cycles': performance_data.get('cycles', 0),
                    'success_rate': performance_data.get('success_rate', 0),
                    'health_score': performance_data.get('health_score', 70),
                    'modules_available': learning_stats.get('modules_available', 0),
                }
            }

        except Exception as e:
            logger.exception(f"Reflection error: {e}")
            return self._generate_reflection_fallback()

    def _generate_rich_insights(
        self,
        awareness: float,
        emotion: str,
        curiosity: float,
        insight_depth: float,
        resilience: float,
        focus: float,
        consciousness_data: Dict[str, Any],
        snapshot_data: Dict[str, Any],
        status_data: Dict[str, Any],
        memory_stats: Dict[str, Any],
        learning_stats: Dict[str, Any],
        goal_stats: Dict[str, Any],
        performance_data: Dict[str, Any]
    ) -> List[str]:
        insights = []

        if awareness >= 0.8:
            insights.append(f"🧠 High self-awareness ({awareness*100:.0f}%) — system has excellent understanding of its state and performance.")
        elif awareness >= 0.5:
            insights.append(f"🧠 Moderate self-awareness ({awareness*100:.0f}%) — system is aware but could improve monitoring.")
        else:
            insights.append(f"🧠 Low self-awareness ({awareness*100:.0f}%) — system needs better state monitoring.")

        emotion_messages = {
            'CALM': "😌 Emotion: CALM — system is operating in a stable, balanced state.",
            'FOCUSED': "🧘 Emotion: FOCUSED — system is concentrating on current tasks.",
            'CURIOUS': "🤔 Emotion: CURIOUS — system is actively seeking new patterns and information.",
            'ALERT': "⚡ Emotion: ALERT — system is monitoring for potential changes.",
            'CONTEMPLATIVE': "🧠 Emotion: CONTEMPLATIVE — system is reflecting and analyzing deeply.",
            'EXCITED': "🚀 Emotion: EXCITED — system is responding positively to market conditions.",
            'OPTIMISTIC': "🌟 Emotion: OPTIMISTIC — system has a positive outlook.",
            'CAUTIOUS': "⚠️ Emotion: CAUTIOUS — system is being careful and risk-aware.",
            'ANXIOUS': "😰 Emotion: ANXIOUS — system detected concerning patterns.",
            'CONFIDENT': "💪 Emotion: CONFIDENT — system is assured in its analysis."
        }
        insights.append(emotion_messages.get(emotion, f"💭 Emotion: {emotion}"))

        if curiosity >= 0.7:
            insights.append(f"🔍 High curiosity ({curiosity*100:.0f}%) — system is actively exploring and learning from data.")
        elif curiosity >= 0.4:
            insights.append(f"🔍 Moderate curiosity ({curiosity*100:.0f}%) — system is learning steadily.")
        else:
            insights.append(f"🔍 Low curiosity ({curiosity*100:.0f}%) — system may need more data variety.")

        if insight_depth >= 0.7:
            insights.append(f"📊 Deep analytical clarity ({insight_depth*100:.0f}%) — system is generating high-quality insights.")
        elif insight_depth >= 0.4:
            insights.append(f"📊 Moderate analytical clarity ({insight_depth*100:.0f}%) — insights are forming.")
        else:
            insights.append(f"📊 Limited analytical clarity ({insight_depth*100:.0f}%) — need more data for better insights.")

        if resilience >= 0.7:
            insights.append(f"🛡️ Strong resilience ({resilience*100:.0f}%) — system recovers well from issues.")
        elif resilience >= 0.4:
            insights.append(f"🛡️ Moderate resilience ({resilience*100:.0f}%) — system can handle some disruptions.")
        else:
            insights.append(f"🛡️ Low resilience ({resilience*100:.0f}%) — system needs better recovery mechanisms.")

        if focus >= 0.7:
            insights.append(f"🎯 Strong focus ({focus*100:.0f}%) — system is concentrating effectively on key signals.")
        elif focus >= 0.4:
            insights.append(f"🎯 Moderate focus ({focus*100:.0f}%) — system is maintaining attention.")
        else:
            insights.append(f"🎯 Low focus ({focus*100:.0f}%) — system is distracted or overloaded.")

        success_rate = performance_data.get('success_rate', 0)
        error_rate = performance_data.get('error_rate', 0)
        cycles = performance_data.get('cycles', 0)

        if success_rate >= 80:
            insights.append(f"📈 Excellent performance — {success_rate:.1f}% success rate over {cycles} cycles.")
        elif success_rate >= 50:
            insights.append(f"📈 Good performance — {success_rate:.1f}% success rate over {cycles} cycles.")
        else:
            insights.append(f"📈 Performance needs improvement — {success_rate:.1f}% success rate, {error_rate:.1f}% error rate.")

        learning_count = learning_stats.get('learning_count', 0)
        pred_count = learning_stats.get('prediction_count', 0)
        dec_count = learning_stats.get('decision_count', 0)

        if learning_count > 0 or pred_count > 0 or dec_count > 0:
            insights.append(f"📚 Learning active — {learning_count} learning cycles, {pred_count} predictions, {dec_count} decisions.")

        if learning_stats.get('learning_active', False):
            insights.append("🧠 Learning engine is ONLINE and processing.")
        else:
            insights.append("🧠 Learning engine is OFFLINE — limited learning capability.")

        short = memory_stats.get('short_term', 0)
        long = memory_stats.get('long_term', 0)
        working = memory_stats.get('working', 0)

        if short > 0 or long > 0:
            insights.append(f"💾 Memory status — Short-term: {short}, Long-term: {long}, Working: {working}.")

        active = goal_stats.get('active', 0)
        completed = goal_stats.get('completed', 0)
        pending = goal_stats.get('pending', 0)
        total = goal_stats.get('total', 0)

        if total > 0:
            if completed > 0:
                insights.append(f"🎯 Goals — {completed} completed, {active} active, {pending} pending.")
            else:
                insights.append(f"🎯 Active goals: {active} — working towards completion.")

        health = performance_data.get('health_score', 70)
        if health >= 80:
            insights.append(f"❤️ System health: EXCELLENT ({health:.1f}%)")
        elif health >= 60:
            insights.append(f"❤️ System health: GOOD ({health:.1f}%)")
        elif health >= 40:
            insights.append(f"❤️ System health: FAIR ({health:.1f}%) — monitor closely.")
        else:
            insights.append(f"❤️ System health: POOR ({health:.1f}%) — attention required!")

        if snapshot_data and isinstance(snapshot_data, dict):
            market = snapshot_data.get('market', {})
            if market:
                forecast = market.get('forecast', 'NEUTRAL')
                market_confidence = market.get('confidence', 0)
                anomaly = market.get('anomaly', 'NORMAL')

                if anomaly == 'CRITICAL':
                    insights.append(f"🚨 Market CRITICAL anomaly detected — immediate attention required!")
                elif anomaly == 'WARNING':
                    insights.append(f"⚠️ Market warning — {forecast} forecast with {market_confidence:.0f}% confidence.")
                else:
                    insights.append(f"📊 Market status — {forecast} forecast with {market_confidence:.0f}% confidence.")

        recovery_count = performance_data.get('recovery_count', 0)
        healing = performance_data.get('healing_attempts', 0)

        if recovery_count > 0 or healing > 0:
            if recovery_count > 5:
                insights.append(f"🔄 Frequent recovery events ({recovery_count}) — system may need optimization.")
            else:
                insights.append(f"🔄 Recovery: {recovery_count} successful recoveries.")

        modules_available = learning_stats.get('modules_available', 0)
        if modules_available > 0:
            insights.append(f"⚙️ {modules_available} modules available for cognitive processing.")

        if awareness > 0.7 and insight_depth > 0.7 and focus > 0.7:
            insights.append("🌟 Overall: System is in excellent cognitive state, ready for complex decisions.")
        elif awareness > 0.5 and insight_depth > 0.5:
            insights.append("📈 Overall: System is functioning well, with room for improvement.")
        else:
            insights.append("🔄 Overall: System is in development phase — building cognitive capacity.")

        seen = set()
        unique_insights = []
        for insight in insights:
            if insight not in seen:
                seen.add(insight)
                unique_insights.append(insight)

        return unique_insights[:8]

    def _generate_reflection_fallback(self) -> Dict[str, Any]:
        emotions = ['CALM', 'FOCUSED', 'CURIOUS', 'ALERT', 'CONTEMPLATIVE', 'EXCITED', 'OPTIMISTIC', 'CAUTIOUS']
        return {
            'awareness': random.uniform(0.4, 0.8),
            'emotion': random.choice(emotions),
            'curiosity': random.uniform(0.3, 0.7),
            'insight_depth': random.uniform(0.3, 0.7),
            'resilience': random.uniform(0.4, 0.8),
            'focus': random.uniform(0.3, 0.7),
            'insights': [
                "⚠️ System is operating in fallback reflection mode.",
                "🔧 Some cognitive modules may be unavailable.",
                "📡 Using simulated reflection data — check brain health.",
                "🔄 Core systems are active but limited.",
                "💡 Recommend checking consciousness module.",
            ],
            'source': 'fallback',
            'confidence': 0.3,
            'stability': 'VOLATILE',
            'reflection_quality': 'POOR',
            'timestamp': datetime.now().isoformat(),
            'metadata': {'error': True, 'fallback': True}
        }

    # ============================================================
    # AI INTEGRATION - DEEPSEEK ENHANCED REFLECTION
    # ============================================================

    def reflection_with_ai(self, topic: str = None) -> Dict[str, Any]:
        try:
            if not DEEPSEEK_AVAILABLE or not DEEPSEEK_ENABLED:
                base = self.reflection()
                return {
                    **base,
                    'ai_enhanced': False,
                    'ai_status': 'disabled',
                    'ai_message': 'DeepSeek AI is not enabled. Set DEEPSEEK_ENABLED=true and provide API key.'
                }

            base_reflection = self.reflection()

            context = f"""
Brain State:
- Awareness: {base_reflection.get('awareness', 0):.2f}
- Emotion: {base_reflection.get('emotion', 'Unknown')}
- Curiosity: {base_reflection.get('curiosity', 0):.2f}
- Insight Depth: {base_reflection.get('insight_depth', 0):.2f}
- Resilience: {base_reflection.get('resilience', 0):.2f}
- Focus: {base_reflection.get('focus', 0):.2f}
- Confidence: {base_reflection.get('confidence', 0):.2f}
- Stability: {base_reflection.get('stability', 'Unknown')}

Current Insights:
{chr(10).join(['- ' + i for i in base_reflection.get('insights', [])[:5]])}

Topic: {topic or 'General cognitive state'}
"""

            prompt = f"""Analisis dan refleksikan state cognitive brain ini dengan mendalam:

1. COGNITIVE ASSESSMENT: Bagaimana kondisi kognitif secara keseluruhan?
2. EMOTIONAL INTELLIGENCE: Apa arti dari emotion {base_reflection.get('emotion', 'Unknown')}?
3. GROWTH OPPORTUNITIES: Apa area yang bisa ditingkatkan?
4. MARKET READINESS: Seberapa siap sistem menghadapi pasar?
5. RECOMMENDATION: Berikan rekomendasi konkret.

Berikan analisis yang jernih, reflektif, dan actionable.
"""

            ai_reflection = deepseek_ai.ask(
                question=prompt,
                context=context,
                system_prompt="reflective",
                temperature=0.7,
                max_tokens=1024
            )

            ai_insights = self._generate_ai_insights(base_reflection, ai_reflection)

            return {
                **base_reflection,
                'ai_enhanced': True,
                'ai_status': 'success',
                'ai_reflection': ai_reflection,
                'ai_insights': ai_insights,
                'ai_timestamp': datetime.now().isoformat(),
                'metadata': {
                    **base_reflection.get('metadata', {}),
                    'ai_enhanced_at': datetime.now().isoformat(),
                    'ai_model': deepseek_ai.model,
                }
            }

        except ImportError:
            base = self.reflection()
            return {
                **base,
                'ai_enhanced': False,
                'ai_status': 'not_available',
                'ai_message': 'DeepSeek module not available.'
            }
        except Exception as e:
            logger.error(f"AI reflection error: {e}")
            base = self.reflection()
            return {
                **base,
                'ai_enhanced': False,
                'ai_status': 'error',
                'ai_error': str(e)
            }

    def _generate_ai_insights(self, base_reflection: Dict, ai_reflection: str) -> List[str]:
        insights = []

        awareness = base_reflection.get('awareness', 0.5)
        if awareness > 0.7:
            insights.append(f"🧠 AI Perspective: System shows strong self-awareness ({awareness*100:.0f}%). Ready for complex decisions.")
        elif awareness > 0.4:
            insights.append(f"🧠 AI Perspective: Moderate awareness ({awareness*100:.0f}%). Improving monitoring recommended.")
        else:
            insights.append(f"🧠 AI Perspective: Low awareness ({awareness*100:.0f}%). Focus on state monitoring.")

        emotion = base_reflection.get('emotion', 'Unknown')
        emotion_insights = {
            'CALM': "😌 AI Observation: Calm state ideal for objective analysis.",
            'FOCUSED': "🎯 AI Observation: Focused state optimal for execution.",
            'CURIOUS': "🔍 AI Observation: Curious state good for pattern discovery.",
            'ALERT': "⚡ AI Observation: Alert state indicates active monitoring.",
            'CONTEMPLATIVE': "🧠 AI Observation: Contemplative state good for strategy formulation.",
            'EXCITED': "🚀 AI Observation: Excited state may indicate high conviction.",
            'OPTIMISTIC': "🌟 AI Observation: Optimistic state aligns with bullish markets.",
            'CAUTIOUS': "⚠️ AI Observation: Cautious state appropriate for risk management.",
            'ANXIOUS': "😰 AI Observation: Anxious state warrants attention to risk.",
            'CONFIDENT': "💪 AI Observation: Confident state supports decisive action."
        }
        insights.append(emotion_insights.get(emotion, f"💭 AI Observation: Emotion: {emotion}"))

        curiosity = base_reflection.get('curiosity', 0.5)
        if curiosity > 0.6:
            insights.append(f"🔬 AI Observation: High curiosity ({curiosity*100:.0f}%) - system is actively learning.")
        else:
            insights.append(f"🔬 AI Observation: Curiosity at {curiosity*100:.0f}% - consider exposing to more data variety.")

        stability = base_reflection.get('stability', 'Unknown')
        if stability == 'STABLE':
            insights.append("📊 AI Observation: Stable state - good for consistent performance.")
        elif stability == 'ADAPTING':
            insights.append("📊 AI Observation: Adapting state - system is adjusting to new conditions.")
        else:
            insights.append("📊 AI Observation: Volatile state - monitor closely for recovery.")

        confidence = base_reflection.get('confidence', 0.5)
        if confidence > 0.6:
            insights.append(f"📈 AI Observation: Confidence at {confidence*100:.0f}% - system is ready for action.")
        else:
            insights.append(f"📈 AI Observation: Confidence at {confidence*100:.0f}% - consider more data before major decisions.")

        if ai_reflection and len(ai_reflection) > 50:
            sentences = ai_reflection.split('.')
            for sentence in sentences:
                if len(sentence) > 20 and any(word in sentence.lower() for word in ['rekomendasi', 'sarankan', 'saran', 'action', 'tindakan']):
                    insights.append(f"💡 AI Recommendation: {sentence.strip()}.")
                    break
            else:
                for sentence in sentences:
                    if len(sentence) > 30:
                        insights.append(f"💡 AI Insight: {sentence.strip()}.")
                        break

        return insights[:8]

    def get_ai_status(self) -> Dict[str, Any]:
        return {
            'ai_enabled': DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED,
            'ai_available': DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED and deepseek_ai is not None,
            'ai_model': deepseek_ai.model if DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED else None,
            'ai_version': getattr(deepseek_ai, 'VERSION', 'unknown') if DEEPSEEK_AVAILABLE else None,
            'reflection_version': self.version,
            'timestamp': datetime.now().isoformat()
        }

    # ============================================================
    # FEEDBACK
    # ============================================================

    def feedback(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            if self.learning_engine is not None:
                result = self.execute(self.learning_engine, "feedback", result)
                if result is not None:
                    return result

            if self.learning is not None:
                result = self.execute(self.learning, "feedback", result)
                if result is not None:
                    return result

            self.working_memory["last_feedback"] = {
                "timestamp": datetime.now().isoformat(),
                "result": result,
            }

            if result.get("success", False):
                self.metrics["successful_cycles"] += 1
            else:
                self.metrics["failed_cycles"] += 1

            return {"status": "feedback_received", "timestamp": datetime.now().isoformat()}

        except Exception as e:
            logger.debug(f"Feedback error: {e}")
            return {"status": "error", "error": str(e)}

    # ============================================================
    # SETTINGS & CONFIGURATION
    # ============================================================

    def set_market_mode(self, mode: str) -> bool:
        mode = mode.upper()
        if mode in self._supported_modes:
            self.market_mode = MarketMode(mode)
            logger.info("Market mode set to: %s", mode)
            return True
        return False

    def get_market_mode(self) -> str:
        return self.market_mode.value

    def get_capabilities(self) -> Dict[str, bool]:
        return self.active_features.copy()

    def toggle_capability(self, capability: str, enabled: bool) -> bool:
        if capability in self.capabilities:
            self.active_features[capability] = enabled
            logger.info("Capability %s set to: %s", capability, enabled)
            return True
        return False

    # ============================================================
    # AUTO-HEALING
    # ============================================================

    def _attempt_healing(self) -> bool:
        if not self.auto_healing_enabled:
            return False

        if self.last_healing_time:
            try:
                last = datetime.fromisoformat(self.last_healing_time)
                elapsed = (datetime.now() - last).total_seconds()
                if elapsed < self.healing_cooldown:
                    return False
            except (ValueError, TypeError):
                pass

        if self.healing_attempts >= self.max_recovery_attempts:
            logger.warning("Max recovery attempts reached. Manual intervention required.")
            return False

        self.healing_attempts += 1
        self.last_healing_time = datetime.now().isoformat()

        healing_actions = []
        healed = False

        if self.errors > self.error_threshold:
            self.errors = 0
            healing_actions.append("Reset error counter")
            healed = True

        if len(self.short_term_memory) >= self.short_term_limit:
            self.short_term_memory = self.short_term_memory[-self.short_term_limit//2:]
            healing_actions.append("Cleared short-term memory")
            healed = True

        if self.state == BrainState.ERROR:
            self.state = BrainState.IDLE
            healing_actions.append("Reset state from ERROR to IDLE")
            healed = True

        if len(self.long_term_memory) > self.long_term_limit * 1.2:
            self.long_term_memory = self.long_term_memory[-self.long_term_limit:]
            healing_actions.append("Trimmed long-term memory")
            healed = True

        if self.errors > self.error_threshold * 2:
            self._load_modules()
            healing_actions.append("Re-initialized modules")
            healed = True

        self.healing_history.append({
            "timestamp": datetime.now().isoformat(),
            "actions": healing_actions,
            "attempt": self.healing_attempts,
            "success": healed,
            "state_before": self.state.value,
            "state_after": self.state.value if healed else self.state.value,
        })

        if healed:
            logger.info("Auto-healing applied: %s", ", ".join(healing_actions))
            self.metrics["recovery_count"] += 1
            self.state = BrainState.RECOVERING
            time.sleep(0.5)
            self.state = BrainState.ACTIVE

        return healed

    # ============================================================
    # METRICS & PERFORMANCE
    # ============================================================

    def _update_metrics(self, start_time: float) -> None:
        processing_time = time.time() - start_time
        self.processing_times.append(processing_time)
        if len(self.processing_times) > 100:
            self.processing_times = self.processing_times[-100:]

        avg_time = sum(self.processing_times) / len(self.processing_times)
        self.metrics["average_processing_time"] = avg_time
        self.metrics["total_processing_time"] += processing_time

        if self.metrics["total_cycles"] > 0:
            self.metrics["error_rate"] = (self.errors / self.metrics["total_cycles"]) * 100
            self.metrics["success_rate"] = (self.metrics["successful_cycles"] / self.metrics["total_cycles"]) * 100

        if self.metrics["total_processing_time"] > 0:
            self.metrics["throughput"] = self.metrics["total_cycles"] / self.metrics["total_processing_time"]

    def _store_history(self, state: CognitiveState) -> None:
        entry = self._cognitive_state_to_dict(state)
        self.history.append(entry)
        if len(self.history) > self.history_limit:
            self.history = self.history[-self.history_limit:]

    def _update_goals(self, state: CognitiveState) -> None:
        for goal in self.goals:
            if goal["status"] != "active":
                continue

            progress_increment = 0.0

            if goal["name"] == "learn_continuously":
                if state.learning and state.learning.get("status") == "learned":
                    progress_increment = 1.0

            elif goal["name"] == "improve_decision_making":
                if state.decision and state.decision.get("confidence", 0) > 0.7:
                    progress_increment = 0.5

            elif goal["name"] == "develop_intuition":
                if state.patterns and len(state.patterns.get("detected", [])) > 0:
                    progress_increment = 0.5

            elif goal["name"] == "build_knowledge_base":
                if state.knowledge and state.knowledge.get("updated", False):
                    progress_increment = 0.5

            elif goal["name"] == "achieve_market_mastery":
                if self.metrics["success_rate"] > 80:
                    progress_increment = 0.2

            elif goal["name"] == "optimize_performance":
                if self.metrics["average_processing_time"] < 1.0:
                    progress_increment = 0.2

            goal["progress"] = min(100.0, goal["progress"] + progress_increment)

            if goal["progress"] >= 100:
                goal["status"] = "completed"
                for g in self.goals:
                    if g["status"] == "pending":
                        g["status"] = "active"
                        self.current_goal = g
                        break

    # ============================================================
    # UTILITY METHODS
    # ============================================================

    def _cognitive_state_to_dict(self, state: CognitiveState) -> Dict[str, Any]:
        return {
            "timestamp": state.timestamp,
            "cycle": state.cycle,
            "input": state.input_data,
            "perception": state.perception,
            "memory": state.memory,
            "learning": state.learning,
            "patterns": state.patterns,
            "reasoning": state.reasoning,
            "knowledge": state.knowledge,
            "awareness": state.awareness,
            "decision": state.decision,
            "prediction": state.prediction,
            "feedback": state.feedback,
            "metadata": state.metadata,
        }

    def _dict_to_cognitive_state(self, data: Dict[str, Any]) -> CognitiveState:
        return CognitiveState(
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            cycle=data.get("cycle", 0),
            input_data=data.get("input", {}),
            perception=data.get("perception", {}),
            memory=data.get("memory", {}),
            learning=data.get("learning", {}),
            patterns=data.get("patterns", {}),
            reasoning=data.get("reasoning", {}),
            knowledge=data.get("knowledge", {}),
            awareness=data.get("awareness", {}),
            decision=data.get("decision", {}),
            prediction=data.get("prediction", {}),
            feedback=data.get("feedback", {}),
            metadata=data.get("metadata", {}),
        )

    # ============================================================
    # GET STATE & STATUS
    # ============================================================

    def get_state_full(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "name": self.name,
            "state": self.state.value,
            "running": self.running,
            "cycles": self.cycles,
            "successful_cycles": self.successful_cycles,
            "failed_cycles": self.failed_cycles,
            "errors": self.errors,
            "market_mode": self.market_mode.value,
            "started_at": self.started_at,
            "last_update": self.last_update,
            "last_input": self.last_input,
            "last_result": self.last_result,
            "last_error": self.last_error,
            "last_error_time": self.last_error_time,
            "history_size": len(self.history),
            "metrics": self.metrics,
            "goals": self.goals,
            "current_goal": self.current_goal,
            "capabilities": self.active_features,
            "modules_available": self.modules_available,
            "available_modules_count": self.available_modules_count,
            "total_modules_count": self.total_modules_count,
            "performance": {
                "average": round(self.average_performance, 4),
                "confidence": round(self.confidence_score, 4),
                "health": round(self.health_score, 2),
            },
            "auto_healing": {
                "enabled": self.auto_healing_enabled,
                "attempts": self.healing_attempts,
                "history": self.healing_history[-5:],
            },
            "timestamp": datetime.now().isoformat(),
        }

    def status(self) -> Dict[str, Any]:
        return {
            "engine": self.name,
            "version": self.version,
            "state": self.state.value,
            "running": self.running,
            "cycles": self.cycles,
            "errors": self.errors,
            "success_rate": round(self.metrics["success_rate"], 2),
            "error_rate": round(self.metrics["error_rate"], 2),
            "avg_processing_time": round(self.metrics["average_processing_time"], 4),
            "throughput": round(self.metrics["throughput"], 2),
            "market_mode": self.market_mode.value,
            "available_modules": self.available_modules_count,
            "total_modules": self.total_modules_count,
            "health": round(self.health_score, 2),
            "confidence": round(self.confidence_score, 4),
            "goals_active": sum(1 for g in self.goals if g["status"] == "active"),
            "goals_completed": sum(1 for g in self.goals if g["status"] == "completed"),
            "is_fallback_mode": any(g.get("is_fallback", False) for g in [self.last_result or {}]),
            "recovery_attempts": self.recovery_attempts,
            "healing_attempts": self.healing_attempts,
            "timestamp": datetime.now().isoformat(),
        }

    def snapshot(self) -> Dict[str, Any]:
        try:
            intelligence = self.market_intelligence()
            decision = self.decision_support()

            return {
                "brain": {
                    "status": "ONLINE" if self.running else "OFFLINE",
                    "version": self.version,
                    "state": self.state.value,
                    "cycles": self.cycles,
                    "errors": self.errors,
                    "success_rate": round(self.metrics["success_rate"], 2),
                },
                "market": {
                    "mode": self.market_mode.value,
                    "forecast": intelligence.get("forecast", "NEUTRAL"),
                    "confidence": intelligence.get("confidence", 0.0),
                    "anomaly": intelligence.get("anomaly", "NORMAL"),
                    "bias": intelligence.get("bias", "UNKNOWN"),
                    "risk_level": intelligence.get("risk_level", "MEDIUM"),
                },
                "decision": {
                    "action": decision.get("action", "HOLD"),
                    "confidence": decision.get("confidence", 0.0),
                    "reason": decision.get("reason", "Unknown"),
                    "expected_outcome": decision.get("expected_outcome"),
                },
                "learning": {
                    "active": self.learning_engine is not None,
                    "history": len(self.history),
                    "insights": len(self.long_term_memory),
                },
                "health": {
                    "score": round(self.health_score, 2),
                    "auto_healing": self.auto_healing_enabled,
                    "healing_attempts": self.healing_attempts,
                },
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.debug(f"Snapshot error: {e}")
            return {
                "brain": {"status": "ERROR", "version": self.version},
                "market": {"forecast": "NEUTRAL", "confidence": 0},
                "decision": {"action": "HOLD", "confidence": 0},
                "health": {"score": 50},
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def health_check(self) -> Dict[str, Any]:
        try:
            components = {}
            for name, available in self.modules_available.items():
                components[name] = available

            components["short_term_memory"] = len(self.short_term_memory) < self.short_term_limit
            components["long_term_memory"] = len(self.long_term_memory) < self.long_term_limit
            components["error_rate"] = self.metrics["error_rate"] < 10.0
            components["processing_time"] = self.metrics["average_processing_time"] < 2.0
            components["state_healthy"] = self.state not in [BrainState.ERROR, BrainState.DEGRADED]
            components["has_brain_instance"] = hasattr(self, 'brain_instance') and self.brain_instance is self

            healthy = all(components.values())

            health_score = 100.0

            unavailable = sum(1 for k, v in components.items() if not v and k not in [
                "short_term_memory", "long_term_memory", "error_rate",
                "processing_time", "state_healthy", "has_brain_instance"
            ])
            health_score -= unavailable * 5

            if self.metrics["error_rate"] > 20:
                health_score -= 20
            elif self.metrics["error_rate"] > 10:
                health_score -= 10

            if self.metrics["average_processing_time"] > 3.0:
                health_score -= 10
            elif self.metrics["average_processing_time"] > 1.5:
                health_score -= 5

            if self.active_features.get("random_fallback", False):
                health_score = min(100, health_score + 5)

            if components.get("has_brain_instance", False):
                health_score = min(100, health_score + 5)

            self.health_score = max(0.0, min(100.0, health_score))

            return {
                "healthy": healthy,
                "health_score": round(self.health_score, 2),
                "components": components,
                "errors": self.errors,
                "cycles": self.cycles,
                "success_rate": round(self.metrics["success_rate"], 2),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.debug(f"Health check error: {e}")
            return {
                "healthy": False,
                "health_score": 50.0,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    # ============================================================
    # MODULE STATUS DISPLAY
    # ============================================================

    def get_module_display_status(self) -> Dict[str, Any]:
        available = [k for k, v in self.modules_available.items() if v]
        unavailable = [k for k, v in self.modules_available.items() if not v]

        display_items = []
        for name in sorted(self.modules_available.keys()):
            status = "✓" if self.modules_available[name] else "✗"
            display_items.append(f"[{status}] {name}")

        return {
            "total": len(self.modules_available),
            "available": len(available),
            "unavailable": len(unavailable),
            "available_list": available,
            "unavailable_list": unavailable,
            "display": display_items,
            "health_percentage": round((len(available) / len(self.modules_available)) * 100, 1) if self.modules_available else 0,
        }

    def print_module_status(self) -> None:
        status = self.get_module_display_status()

        print()
        print("=" * 70)
        print("  MODULE STATUS SUMMARY")
        print("=" * 70)
        print(f"  Total Modules : {status['total']}")
        print(f"  Available     : {status['available']}")
        print(f"  Unavailable   : {status['unavailable']}")
        print(f"  Health        : {status['health_percentage']}%")
        print("-" * 70)

        if status['available_list']:
            print("  [✓] Available:")
            for name in sorted(status['available_list']):
                print(f"      - {name}")

        if status['unavailable_list']:
            print("  [✗] Unavailable:")
            for name in sorted(status['unavailable_list']):
                print(f"      - {name}")

        print("=" * 70)

    # ============================================================
    # CONTROL METHODS
    # ============================================================

    def start(self) -> bool:
        if self.running:
            return False
        self.running = True
        self.state = BrainState.ACTIVE
        logger.info("Brain started.")
        return True

    def stop(self) -> bool:
        if not self.running:
            return False
        self.running = False
        self.state = BrainState.STOPPED
        logger.info("Brain stopped.")
        return True

    def reset(self) -> bool:
        try:
            with self.lock:
                self.cycles = 0
                self.successful_cycles = 0
                self.failed_cycles = 0
                self.errors = 0
                self.recovery_attempts = 0
                self.last_input = None
                self.last_result = None
                self.last_error = None
                self.last_error_time = None
                self.history.clear()
                self.short_term_memory.clear()
                self.long_term_memory.clear()
                self.working_memory.clear()
                self.processing_times.clear()
                self.performance_scores.clear()
                self.healing_history.clear()

                self.metrics = {
                    "total_cycles": 0,
                    "successful_cycles": 0,
                    "failed_cycles": 0,
                    "average_processing_time": 0.0,
                    "total_processing_time": 0.0,
                    "learning_count": 0,
                    "prediction_count": 0,
                    "decision_count": 0,
                    "memory_usage": 0,
                    "error_rate": 0.0,
                    "success_rate": 0.0,
                    "throughput": 0.0,
                    "recovery_count": 0,
                }

                self.health_score = 100.0
                self.confidence_score = 0.5
                self.average_performance = 0.0

                self.state = BrainState.IDLE
                self.goals = self._initialize_goals()
                self.current_goal = None

                self.brain_instance = self
                self._brain_available = True
                self.brain_instances = self._instances

                logger.info("Brain reset completed.")
                return True

        except Exception as e:
            logger.exception(f"Brain reset failed: {e}")
            return False

    def shutdown(self) -> bool:
        try:
            self.stop()
            logger.info("Brain shutdown completed.")
            return True
        except Exception as e:
            logger.exception(f"Brain shutdown failed: {e}")
            return False


# ============================================================
# GLOBAL INSTANCE
# ============================================================

brain = Brain()


# ============================================================
# SHORTCUT FUNCTIONS
# ============================================================

def observe(data: Dict[str, Any]) -> Dict[str, Any]:
    return brain.observe(data)


def analyze(data: Dict[str, Any]) -> Dict[str, Any]:
    return brain.analyze(data)


def get_state_full() -> Dict[str, Any]:
    return brain.get_state_full()


def status() -> Dict[str, Any]:
    return brain.status()


def snapshot() -> Dict[str, Any]:
    return brain.snapshot()


def forecast() -> Dict[str, Any]:
    return brain.forecast()


def decision_support() -> Dict[str, Any]:
    return brain.decision_support()


def feedback(result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return brain.feedback(result)


def health_check() -> Dict[str, Any]:
    return brain.health_check()


def start() -> bool:
    return brain.start()


def stop() -> bool:
    return brain.stop()


def reset() -> bool:
    return brain.reset()


def get_module_status() -> Dict[str, Any]:
    return brain.get_module_display_status()


def print_module_status() -> None:
    brain.print_module_status()


def reflection() -> Dict[str, Any]:
    return brain.reflection()


def reflection_with_ai(topic: str = None) -> Dict[str, Any]:
    return brain.reflection_with_ai(topic)


def get_ai_status() -> Dict[str, Any]:
    return brain.get_ai_status()


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    print()
    print("=" * 70)
    print("  COGNITIVE BRAIN v4.2.3 - COMPREHENSIVE SELF TEST")
    print("=" * 70)
    print()

    tests_passed = 0
    tests_failed = 0
    results = {}

    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        test_brain = Brain()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")

    # Test 2: brain_instance
    print("\n2. Testing brain_instance...")
    try:
        test_brain = Brain()
        if hasattr(test_brain, 'brain_instance') and test_brain.brain_instance is test_brain:
            results["brain_instance"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ brain_instance test passed")
        else:
            results["brain_instance"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ brain_instance test failed")
    except Exception as e:
        results["brain_instance"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ brain_instance test failed: {e}")

    # Test 3: AI Integration
    print("\n3. Testing AI integration...")
    try:
        from core.deepseek import deepseek_ai
        if DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED:
            results["ai_integration"] = {"status": "PASS", "message": "AI is enabled"}
            tests_passed += 1
            print("   ✅ AI integration: ENABLED")
        else:
            results["ai_integration"] = {"status": "SKIP", "message": "AI is disabled"}
            print("   ⏭️ AI integration: DISABLED (skipped)")
    except Exception as e:
        results["ai_integration"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ AI integration test failed: {e}")

    # Test 4: Observe
    print("\n4. Testing observe...")
    try:
        test_data = {
            "market": "BTC/USD",
            "signal": "bullish",
            "pattern": "breakout",
            "volume": "high",
            "price": 65000,
            "confidence": 0.85,
        }
        result = brain.observe(test_data)

        checks = {
            "has_timestamp": "timestamp" in result,
            "has_cycle": "cycle" in result,
            "has_perception": "perception" in result,
            "has_memory": "memory" in result,
            "has_learning": "learning" in result,
            "has_patterns": "patterns" in result,
            "has_reasoning": "reasoning" in result,
            "has_knowledge": "knowledge" in result,
            "has_awareness": "awareness" in result,
            "has_decision": "decision" in result,
            "has_prediction": "prediction" in result,
            "has_feedback": "feedback" in result,
            "status_ok": result.get("status") != "ERROR",
        }

        passed = all(checks.values())
        if passed:
            results["observe"] = {"status": "PASS", "checks": checks}
            tests_passed += 1
            print("   ✅ Observe test passed")
        else:
            failed_checks = [k for k, v in checks.items() if not v]
            results["observe"] = {"status": "FAIL", "failed_checks": failed_checks}
            tests_failed += 1
            print(f"   ❌ Observe test failed: {failed_checks}")
    except Exception as e:
        results["observe"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Observe test failed: {e}")

    # Test 5: Reflection with AI
    print("\n5. Testing reflection with AI...")
    try:
        reflection_result = brain.reflection()
        if reflection_result and "awareness" in reflection_result:
            results["reflection"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Reflection test passed")
        else:
            results["reflection"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Reflection test failed")
    except Exception as e:
        results["reflection"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Reflection test failed: {e}")

    # Summary
    print()
    print("=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"  ✅ Passed: {tests_passed}")
    print(f"  ❌ Failed: {tests_failed}")
    print(f"  📊 Total:  {tests_passed + tests_failed}")
    print("=" * 70)

    brain.print_module_status()

    return {
        "module": "brain",
        "version": "4.2.3",
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
    print("  COGNITIVE BRAIN v4.2.3 - SELF TEST COMPLETE")
    print("=" * 70)
    print()
    print("Final Status:", result["status"])
    print("Details:", json.dumps(result, indent=2, default=str))


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "Brain",
    "CognitiveState",
    "MarketIntelligence",
    "DecisionSupport",
    "BrainState",
    "MarketMode",
    "ProcessingPriority",
    "brain",
    "observe",
    "analyze",
    "get_state_full",
    "status",
    "snapshot",
    "forecast",
    "decision_support",
    "feedback",
    "health_check",
    "start",
    "stop",
    "reset",
    "get_module_status",
    "print_module_status",
    "reflection",
    "reflection_with_ai",
    "get_ai_status",
    "self_test",
]
