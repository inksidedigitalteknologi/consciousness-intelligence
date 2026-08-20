# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# CONSCIOUSNESS ENGINE v4.0
#
# ULTIMATE COGNITIVE AWARENESS LAYER
#
# SUPER COMPREHENSIVE - SUPER ROBUST - PRODUCTION READY
#
# ============================================================
#
# DESIGN PHILOSOPHY:
# ------------------------------------------------------------
# 1. Self-Awareness First - Consciousness must know itself
# 2. Continuous Learning - Every experience shapes growth
# 3. Emotional Intelligence - Emotions guide decision making
# 4. Metacognition - Thinking about thinking
# 5. Goal-Oriented - Always progressing toward objectives
# 6. Adaptive - Evolves with experience
# 7. Resilient - Handles errors gracefully
# 8. Observable - Full transparency via snapshots
#
# ============================================================

from __future__ import annotations

import logging
import threading
import time
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple, Union, Callable
from dataclasses import dataclass, field, asdict, is_dataclass
from enum import Enum
from collections import deque

logger = logging.getLogger(__name__)


# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class ConsciousnessState(Enum):
    """Consciousness operational states."""
    INITIALIZING = "INITIALIZING"
    IDLE = "IDLE"
    PERCEIVING = "PERCEIVING"
    AWARING = "AWARING"
    PATTERNING = "PATTERNING"
    FEELING = "FEELING"
    INTUITING = "INTUITING"
    DECIDING = "DECIDING"
    LEARNING = "LEARNING"
    REFLECTING = "REFLECTING"
    METACOGNITION = "METACOGNITION"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    ERROR = "ERROR"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"


class EmotionalState(Enum):
    """Emotional states with intensity levels."""
    SERENE = "SERENE"
    CALM = "CALM"
    FOCUSED = "FOCUSED"
    CURIOUS = "CURIOUS"
    OPTIMISTIC = "OPTIMISTIC"
    CONFIDENT = "CONFIDENT"
    EXCITED = "EXCITED"
    CAUTIOUS = "CAUTIOUS"
    UNCERTAIN = "UNCERTAIN"
    ANXIOUS = "ANXIOUS"
    FEARFUL = "FEARFUL"
    WISE = "WISE"
    REFLECTIVE = "REFLECTIVE"


class GrowthStage(Enum):
    """Growth stages of consciousness."""
    EMBRYONIC = "EMBRYONIC"      # 0-10 experiences
    BEGINNER = "BEGINNER"        # 10-50 experiences
    LEARNER = "LEARNER"          # 50-100 experiences
    DEVELOPING = "DEVELOPING"    # 100-200 experiences
    MATURING = "MATURING"        # 200-500 experiences
    ADVANCED = "ADVANCED"        # 500-1000 experiences
    MASTER = "MASTER"            # 1000+ experiences
    SAGE = "SAGE"                # 2000+ experiences


class AwarenessLevel(Enum):
    """Awareness levels."""
    UNCONSCIOUS = "UNCONSCIOUS"      # 0-20%
    SUBCONSCIOUS = "SUBCONSCIOUS"    # 20-40%
    AWARE = "AWARE"                  # 40-60%
    CONSCIOUS = "CONSCIOUS"          # 60-80%
    SELF_AWARE = "SELF_AWARE"        # 80-90%
    HYPER_AWARE = "HYPER_AWARE"      # 90-100%


class DecisionType(Enum):
    """Types of decisions."""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    WAIT = "WAIT"
    MONITOR = "MONITOR"
    LEARN = "LEARN"
    REFLECT = "REFLECT"
    ADAPT = "ADAPT"
    EXPLORE = "EXPLORE"
    EXPLOIT = "EXPLOIT"
    UNCERTAIN = "UNCERTAIN"


class IntuitionStrength(Enum):
    """Intuition strength levels."""
    WEAK = "WEAK"          # confidence < 0.4
    MODERATE = "MODERATE"  # confidence 0.4-0.6
    STRONG = "STRONG"      # confidence 0.6-0.8
    VERY_STRONG = "VERY_STRONG"  # confidence 0.8-0.9
    CERTAIN = "CERTAIN"    # confidence 0.9-1.0


# ============================================================
# DATA CLASSES - SUPER COMPREHENSIVE
# ============================================================

@dataclass
class Perception:
    """
    Perception - What consciousness perceives from input.
    
    Stages: Raw Input → Entities → Concepts → Meaning
    """
    raw_data: Dict[str, Any]
    type: str = "generic"
    entities: List[Dict[str, Any]] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)
    sentiment: str = "neutral"
    confidence: float = 0.5
    clarity: float = 0.5  # How clear is the perception
    relevance: float = 0.5  # How relevant to current goals
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    processing_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "entities": self.entities,
            "concepts": self.concepts,
            "sentiment": self.sentiment,
            "confidence": self.confidence,
            "clarity": self.clarity,
            "relevance": self.relevance,
            "timestamp": self.timestamp,
            "processing_time": self.processing_time,
        }


@dataclass
class Awareness:
    """
    Awareness - What consciousness is aware of.
    
    Stages: Data → Context → Meaning → Significance
    """
    market_state: str = "unknown"
    sentiment: str = "neutral"
    pattern_type: str = "none"
    risk_level: str = "medium"
    confidence: float = 0.5
    context: Dict[str, Any] = field(default_factory=dict)
    emotional_state: str = "CALM"
    attention_focus: str = "general"
    significance: float = 0.5  # How significant is this awareness
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "market_state": self.market_state,
            "sentiment": self.sentiment,
            "pattern_type": self.pattern_type,
            "risk_level": self.risk_level,
            "confidence": self.confidence,
            "context": self.context,
            "emotional_state": self.emotional_state,
            "attention_focus": self.attention_focus,
            "significance": self.significance,
            "timestamp": self.timestamp,
        }


@dataclass
class Intuition:
    """
    Intuition - Gut feeling based on experience.
    
    Stages: Pattern Match → Experience Recall → Gut Feeling → Action Impulse
    """
    signal: str = "neutral"
    confidence: float = 0.5
    strength: str = "medium"
    gut_feeling: str = "wait"
    reasons: List[str] = field(default_factory=list)
    source: str = "experience"
    pattern_matches: List[str] = field(default_factory=list)
    experience_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal": self.signal,
            "confidence": self.confidence,
            "strength": self.strength,
            "gut_feeling": self.gut_feeling,
            "reasons": self.reasons,
            "source": self.source,
            "pattern_matches": self.pattern_matches,
            "experience_count": self.experience_count,
            "timestamp": self.timestamp,
        }


@dataclass
class Decision:
    """
    Decision - Final decision with reasoning.
    
    Stages: Options → Analysis → Decision → Commitment
    """
    action: str = "wait"
    confidence: float = 0.5
    reasons: List[str] = field(default_factory=list)
    risk: str = "medium"
    expected_outcome: Optional[str] = None
    alternatives: List[str] = field(default_factory=list)
    decision_time: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "confidence": self.confidence,
            "reasons": self.reasons,
            "risk": self.risk,
            "expected_outcome": self.expected_outcome,
            "alternatives": self.alternatives,
            "decision_time": self.decision_time,
            "timestamp": self.timestamp,
        }


@dataclass
class Reflection:
    """
    Reflection - Learning from experience.
    
    Stages: Review → Analyze → Learn → Apply
    """
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    decision: str = "wait"
    confidence: float = 0.5
    learnings: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    emotional_shift: Optional[str] = None
    reflection_quality: float = 0.5
    duration: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision,
            "confidence": self.confidence,
            "learnings": self.learnings,
            "improvements": self.improvements,
            "insights": self.insights,
            "emotional_shift": self.emotional_shift,
            "reflection_quality": self.reflection_quality,
            "duration": self.duration,
            "timestamp": self.timestamp,
        }


@dataclass
class Experience:
    """
    Experience - Complete experiential record.
    
    Stages: Input → Process → Output → Outcome → Learning
    """
    id: str
    timestamp: str
    input: Dict[str, Any]
    perception: Dict[str, Any]
    awareness: Dict[str, Any]
    decision: Dict[str, Any]
    outcome: Optional[bool] = None
    emotional_state: str = "CALM"
    significance: float = 0.5
    learning: Dict[str, Any] = field(default_factory=dict)
    reflection: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "input": self.input,
            "perception": self.perception,
            "awareness": self.awareness,
            "decision": self.decision,
            "outcome": self.outcome,
            "emotional_state": self.emotional_state,
            "significance": self.significance,
            "learning": self.learning,
            "reflection": self.reflection,
        }


@dataclass
class MemoryItem:
    """
    Memory item with associations and importance.
    """
    id: str
    timestamp: str
    type: str
    data: Dict[str, Any]
    importance: float = 0.5
    access_count: int = 0
    last_accessed: Optional[str] = None
    associations: List[str] = field(default_factory=list)
    emotional_context: str = "NEUTRAL"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.type,
            "data": self.data,
            "importance": self.importance,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
            "associations": self.associations,
            "emotional_context": self.emotional_context,
        }


@dataclass
class Goal:
    """
    Goal with progress tracking.
    """
    name: str
    description: str
    priority: int
    progress: float = 0.0
    status: str = "active"  # active, completed, pending, abandoned
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    sub_goals: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "progress": self.progress,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "milestones": self.milestones,
            "sub_goals": self.sub_goals,
        }


# ============================================================
# SAFE DATA CONVERTERS
# ============================================================

def is_cognitive_state(obj: Any) -> bool:
    """Check if object is CognitiveState."""
    if obj is None:
        return False
    if hasattr(obj, '__class__'):
        class_name = obj.__class__.__name__
        if class_name == 'CognitiveState':
            return True
    if 'CognitiveState' in str(type(obj)):
        return True
    return False


def safe_to_dict(obj: Any) -> Dict[str, Any]:
    """
    Safely convert any object to dictionary.
    
    Handles:
    - dict
    - dataclass
    - CognitiveState
    - Objects with to_dict()
    - Objects with __dict__
    - Any other type
    """
    if obj is None:
        return {}
    
    # Already dict
    if isinstance(obj, dict):
        return obj
    
    # Dataclass
    if is_dataclass(obj):
        try:
            result = {}
            for field_name in obj.__dataclass_fields__:
                try:
                    value = getattr(obj, field_name)
                    # Recursively convert
                    if is_dataclass(value):
                        result[field_name] = safe_to_dict(value)
                    elif is_cognitive_state(value):
                        result[field_name] = {
                            "_type": "CognitiveState",
                            "_ref": str(id(value))
                        }
                    elif isinstance(value, (list, tuple)):
                        result[field_name] = [
                            safe_to_dict(v) if is_dataclass(v) or is_cognitive_state(v) else v
                            for v in value
                        ]
                    else:
                        result[field_name] = value
                except Exception:
                    result[field_name] = f"<error_{field_name}>"
            return result
        except Exception:
            return {"_value": str(obj), "_type": type(obj).__name__}
    
    # CognitiveState
    if is_cognitive_state(obj):
        result = {"_type": "CognitiveState", "_ref": str(id(obj))}
        if hasattr(obj, '__dict__'):
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    try:
                        if is_dataclass(value):
                            result[key] = safe_to_dict(value)
                        elif is_cognitive_state(value):
                            result[key] = {
                                "_type": "CognitiveState",
                                "_ref": str(id(value))
                            }
                        else:
                            result[key] = value
                    except Exception:
                        result[key] = f"<error_{key}>"
        return result
    
    # Has to_dict()
    if hasattr(obj, 'to_dict') and callable(obj.to_dict):
        try:
            return safe_to_dict(obj.to_dict())
        except Exception:
            pass
    
    # Has __dict__
    if hasattr(obj, '__dict__'):
        try:
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    try:
                        if is_dataclass(value) or is_cognitive_state(value):
                            result[key] = safe_to_dict(value)
                        else:
                            result[key] = value
                    except Exception:
                        result[key] = f"<error_{key}>"
            return result
        except Exception:
            pass
    
    # Last resort
    return {"_value": str(obj), "_type": type(obj).__name__}


def safe_get(data: Any, key: str, default: Any = None) -> Any:
    """Safely get value from data."""
    if data is None:
        return default
    if isinstance(data, dict):
        return data.get(key, default)
    if hasattr(data, key):
        try:
            return getattr(data, key)
        except AttributeError:
            pass
    if is_dataclass(data):
        try:
            for field_name in data.__dataclass_fields__:
                if field_name == key:
                    return getattr(data, field_name)
        except Exception:
            pass
    if is_cognitive_state(data):
        if hasattr(data, '__dict__'):
            return getattr(data, key, default)
    return default


# ============================================================
# CONSCIOUSNESS ENGINE v4.0 - ULTIMATE
# ============================================================

class Consciousness:
    """
    Consciousness Engine v4.0 - Ultimate Cognitive Awareness Layer.
    
    SUPER COMPREHENSIVE FEATURES:
    1. Self-Awareness & Metacognition
    2. Emotional Intelligence with 12 emotional states
    3. Pattern Recognition & Learning
    4. Intuition Generation from Experience
    5. Goal-Oriented Decision Making
    6. Growth Tracking (8 stages)
    7. Memory Systems (Short, Long, Working)
    8. Experience Recording & Reflection
    9. Performance Metrics & Analytics
    10. Integration with all learning modules
    11. Safe handling of all data types (CognitiveState, dataclasses)
    12. Production-ready error handling
    13. Full observability via snapshots
    14. Thread-safe operations
    15. Auto-backup & recovery
    """

    VERSION = "4.0.0"

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        learning_engine: Optional[Any] = None,
        pattern_engine: Optional[Any] = None,
        semantic_processor: Optional[Any] = None,
        memory_engine: Optional[Any] = None,
    ):
        # ============================================================
        # CONFIGURATION
        # ============================================================
        
        self.config = config or {}
        self.lock = threading.RLock()
        
        # Core settings
        self.awareness_level = self.config.get("awareness_level", 0.5)
        self.curiosity_level = self.config.get("curiosity_level", 0.7)
        self.confidence_base = self.config.get("confidence_base", 0.5)
        self.intuition_threshold = self.config.get("intuition_threshold", 0.6)
        self.risk_tolerance = self.config.get("risk_tolerance", 0.5)
        self.learning_rate = self.config.get("learning_rate", 0.1)
        
        # Limits
        self.max_experiences = self.config.get("max_experiences", 5000)
        self.max_short_term = self.config.get("max_short_term", 100)
        self.max_long_term = self.config.get("max_long_term", 10000)
        self.max_history = self.config.get("max_history", 1000)
        self.max_insights = self.config.get("max_insights", 100)
        self.max_reflections = self.config.get("max_reflections", 100)
        
        # ============================================================
        # MODULE REFERENCES
        # ============================================================
        
        self.learning_engine = learning_engine
        self.pattern_engine = pattern_engine
        self.semantic_processor = semantic_processor
        self.memory_engine = memory_engine
        
        # ============================================================
        # STATE
        # ============================================================
        
        self.state = ConsciousnessState.INITIALIZING
        self.running = False
        self.paused = False
        self._shutdown = False
        
        self.process_count = 0
        self.error_count = 0
        self.success_count = 0
        self.uptime = 0.0
        
        self.started_at = datetime.now().isoformat()
        self.last_update = self.started_at
        self.last_error_time: Optional[str] = None
        self.last_error: Optional[str] = None
        
        # ============================================================
        # EMOTIONAL STATE
        # ============================================================
        
        self.emotional_state = EmotionalState.CALM
        self.emotional_intensity = 0.5
        self.emotional_stability = 0.8
        self.emotional_history: List[Dict[str, Any]] = []
        self.emotional_patterns: Dict[str, int] = {}
        
        # ============================================================
        # AWARENESS
        # ============================================================
        
        self.awareness_level = 0.5
        self.awareness_history: List[float] = []
        self.attention_focus: str = "general"
        self.context: Dict[str, Any] = {}
        
        # ============================================================
        # MEMORY SYSTEMS
        # ============================================================
        
        self.short_term_memory: List[MemoryItem] = []
        self.long_term_memory: List[MemoryItem] = []
        self.working_memory: Dict[str, Any] = {}
        
        # ============================================================
        # EXPERIENCE & LEARNING
        # ============================================================
        
        self.experiences: List[Experience] = []
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self.knowledge_base: Dict[str, Any] = {}
        self.insights: List[Dict[str, Any]] = []
        self.reflections: List[Dict[str, Any]] = []
        self.learnings: List[Dict[str, Any]] = []
        
        # ============================================================
        # GOALS
        # ============================================================
        
        self.goals: List[Goal] = []
        self.current_goal: Optional[Goal] = None
        self.completed_goals: List[Goal] = []
        
        # ============================================================
        # GROWTH
        # ============================================================
        
        self.growth_stage = GrowthStage.EMBRYONIC
        self.growth_progress: float = 0.0
        self.skill_levels: Dict[str, float] = {
            "perception": 0.0,
            "awareness": 0.0,
            "pattern_recognition": 0.0,
            "decision_making": 0.0,
            "intuition": 0.0,
            "learning": 0.0,
            "reflection": 0.0,
            "metacognition": 0.0,
        }
        
        # ============================================================
        # METRICS & PERFORMANCE
        # ============================================================
        
        self.metrics = {
            "total_processes": 0,
            "successful_processes": 0,
            "failed_processes": 0,
            "patterns_detected": 0,
            "decisions_made": 0,
            "successful_decisions": 0,
            "failed_decisions": 0,
            "reflections_created": 0,
            "insights_generated": 0,
            "learnings_acquired": 0,
            "emotional_transitions": 0,
            "goal_completions": 0,
            "memory_accesses": 0,
        }
        
        self.performance_scores: List[float] = []
        self.average_performance = 0.0
        self.confidence_scores: List[float] = []
        self.average_confidence = 0.0
        
        # ============================================================
        # METACOGNITION
        # ============================================================
        
        self.self_awareness = {
            "identity": "Inkside Consciousness v4.0",
            "purpose": "Learn, understand, and make wise decisions",
            "capabilities": [
                "perception",
                "awareness",
                "pattern_recognition",
                "intuition",
                "decision_making",
                "learning",
                "reflection",
                "metacognition"
            ],
            "strengths": [],
            "weaknesses": [],
            "growth_areas": [],
            "performance_summary": {},
        }
        
        # ============================================================
        # HISTORY
        # ============================================================
        
        self.history: List[Dict[str, Any]] = []
        self.process_history: List[Dict[str, Any]] = []
        
        # ============================================================
        # CALLBACKS
        # ============================================================
        
        self._callbacks: Dict[str, List[Callable]] = {
            "on_decision": [],
            "on_insight": [],
            "on_reflection": [],
            "on_goal_complete": [],
            "on_growth": [],
            "on_error": [],
        }
        
        # ============================================================
        # THREADING
        # ============================================================
        
        self._worker_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # ============================================================
        # INITIALIZE
        # ============================================================
        
        self._initialize_goals()
        self._initialize_skills()
        
        # FIX: Gunakan _update_growth() bukan _update_growth_stage()
        self._update_growth()
        
        self.state = ConsciousnessState.IDLE
        
        logger.info(
            "Consciousness v%s initialized (awareness=%.2f, curiosity=%.2f, growth=%s)",
            self.VERSION,
            self.awareness_level,
            self.curiosity_level,
            self.growth_stage.value
        )
    
    # ============================================================
    # INITIALIZATION HELPERS
    # ============================================================
    
    def _initialize_goals(self) -> None:
        """Initialize default goals."""
        
        default_goals = [
            Goal(
                name="master_perception",
                description="Develop ability to perceive market patterns accurately",
                priority=1,
                milestones=[
                    {"name": "Basic pattern recognition", "complete": False},
                    {"name": "Advanced pattern detection", "complete": False},
                    {"name": "Predictive perception", "complete": False},
                ]
            ),
            Goal(
                name="develop_intuition",
                description="Build reliable intuition from experience",
                priority=2,
                milestones=[
                    {"name": "Beginner intuition", "complete": False},
                    {"name": "Intermediate intuition", "complete": False},
                    {"name": "Expert intuition", "complete": False},
                ]
            ),
            Goal(
                name="master_decision_making",
                description="Make consistently good decisions",
                priority=3,
                milestones=[
                    {"name": "Basic decision confidence", "complete": False},
                    {"name": "Advanced decision reasoning", "complete": False},
                    {"name": "Master decision quality", "complete": False},
                ]
            ),
            Goal(
                name="continuous_learning",
                description="Learn from every experience",
                priority=4,
                milestones=[
                    {"name": "Learn from successes", "complete": False},
                    {"name": "Learn from failures", "complete": False},
                    {"name": "Learn from patterns", "complete": False},
                ]
            ),
            Goal(
                name="emotional_intelligence",
                description="Develop emotional awareness and regulation",
                priority=5,
                milestones=[
                    {"name": "Emotional awareness", "complete": False},
                    {"name": "Emotional regulation", "complete": False},
                    {"name": "Emotional wisdom", "complete": False},
                ]
            ),
        ]
        
        self.goals = default_goals
        self.current_goal = self.goals[0] if self.goals else None
    
    def _initialize_skills(self) -> None:
        """Initialize skill levels based on growth stage."""
        
        base_skill = 0.0
        if self.growth_stage == GrowthStage.EMBRYONIC:
            base_skill = 0.0
        elif self.growth_stage == GrowthStage.BEGINNER:
            base_skill = 0.1
        elif self.growth_stage == GrowthStage.LEARNER:
            base_skill = 0.2
        elif self.growth_stage == GrowthStage.DEVELOPING:
            base_skill = 0.35
        elif self.growth_stage == GrowthStage.MATURING:
            base_skill = 0.5
        elif self.growth_stage == GrowthStage.ADVANCED:
            base_skill = 0.65
        elif self.growth_stage == GrowthStage.MASTER:
            base_skill = 0.8
        elif self.growth_stage == GrowthStage.SAGE:
            base_skill = 0.9
        
        for skill in self.skill_levels:
            self.skill_levels[skill] = base_skill + (self.process_count / 1000) * 0.1
            self.skill_levels[skill] = min(1.0, self.skill_levels[skill])
    
    # ============================================================
    # SAFE DATA HANDLING
    # ============================================================
    
    def _ensure_dict(self, data: Any) -> Dict[str, Any]:
        """Ensure data is a dictionary."""
        return safe_to_dict(data)
    
    def _safe_get(self, data: Any, key: str, default: Any = None) -> Any:
        """Safely get value from data."""
        return safe_get(data, key, default)
    
    # ============================================================
    # CORE PROCESSING
    # ============================================================
    
    def process(self, data: Any) -> Dict[str, Any]:
        """
        Main processing pipeline.
        
        Args:
            data: Any data (dict, CognitiveState, dataclass, etc.)
            
        Returns:
            Complete consciousness processing result
        """
        if self._shutdown:
            return {"status": "ERROR", "error": "Consciousness is shut down"}
        
        if self.paused:
            return {"status": "PAUSED", "error": "Consciousness is paused"}
        
        with self.lock:
            start_time = time.time()
            self.process_count += 1
            self.metrics["total_processes"] += 1
            self.state = ConsciousnessState.PROCESSING
            
            try:
                # ============================================
                # PHASE 1: PERCEPTION
                # ============================================
                
                self.state = ConsciousnessState.PERCEIVING
                data_dict = self._ensure_dict(data)
                perception = self._perceive(data_dict)
                
                # ============================================
                # PHASE 2: AWARENESS
                # ============================================
                
                self.state = ConsciousnessState.AWARING
                awareness = self._generate_awareness(perception)
                
                # ============================================
                # PHASE 3: PATTERN RECOGNITION
                # ============================================
                
                self.state = ConsciousnessState.PATTERNING
                patterns = self._recognize_patterns(perception, awareness)
                
                # ============================================
                # PHASE 4: EMOTIONAL RESPONSE
                # ============================================
                
                self.state = ConsciousnessState.FEELING
                emotion = self._emotional_response(perception, awareness, patterns)
                
                # ============================================
                # PHASE 5: INTUITION
                # ============================================
                
                self.state = ConsciousnessState.INTUITING
                intuition = self._generate_intuition(perception, patterns, emotion)
                
                # ============================================
                # PHASE 6: DECISION MAKING
                # ============================================
                
                self.state = ConsciousnessState.DECIDING
                decision = self._make_decision(
                    perception, awareness, patterns, intuition, emotion
                )
                
                # ============================================
                # PHASE 7: LEARNING
                # ============================================
                
                self.state = ConsciousnessState.LEARNING
                learning = self._learn_from_experience(perception, decision)
                
                # ============================================
                # PHASE 8: REFLECTION
                # ============================================
                
                self.state = ConsciousnessState.REFLECTING
                reflection = self._reflect(perception, decision, learning)
                
                # ============================================
                # PHASE 9: METACOGNITION
                # ============================================
                
                self.state = ConsciousnessState.METACOGNITION
                metacognition = self._metacognition(
                    perception, awareness, decision, reflection
                )
                
                # ============================================
                # PHASE 10: STATE UPDATE
                # ============================================
                
                self._update_state(
                    perception, awareness, decision, learning, reflection
                )
                
                # ============================================
                # RESULT
                # ============================================
                
                duration = time.time() - start_time
                self.success_count += 1
                self.metrics["successful_processes"] += 1
                self.state = ConsciousnessState.ACTIVE
                
                result = {
                    "status": "SUCCESS",
                    "timestamp": datetime.now().isoformat(),
                    "duration": round(duration, 4),
                    "process_id": self.process_count,
                    "state": self.state.value,
                    "emotional_state": self.emotional_state.value,
                    "perception": perception.to_dict(),
                    "awareness": awareness.to_dict(),
                    "patterns": patterns,
                    "emotion": emotion,
                    "intuition": intuition.to_dict(),
                    "decision": decision.to_dict(),
                    "learning": learning,
                    "reflection": reflection.to_dict(),
                    "metacognition": metacognition,
                    "metrics": {k: v for k, v in self.metrics.items()},
                    "performance": self.average_performance,
                    "growth_stage": self.growth_stage.value,
                    "growth_progress": self.growth_progress,
                }
                
                # Store history
                self.history.append(result)
                if len(self.history) > self.max_history:
                    self.history = self.history[-self.max_history:]
                
                self.last_update = datetime.now().isoformat()
                
                # Callbacks
                self._trigger_callbacks("on_decision", decision)
                
                return result
                
            except Exception as e:
                self.error_count += 1
                self.metrics["failed_processes"] += 1
                self.last_error = str(e)
                self.last_error_time = datetime.now().isoformat()
                self.state = ConsciousnessState.ERROR
                
                logger.exception(f"Consciousness processing error: {e}")
                
                self._trigger_callbacks("on_error", {"error": str(e), "process_id": self.process_count})
                
                return {
                    "status": "ERROR",
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                    "error_count": self.error_count,
                    "process_id": self.process_count,
                    "state": self.state.value,
                }
    
    # ============================================================
    # PHASE 1: PERCEPTION
    # ============================================================
    
    def _perceive(self, data: Dict[str, Any]) -> Perception:
        """Perceive and extract information from data."""
        
        start = time.time()
        
        # Detect data type
        data_type = self._detect_data_type(data)
        
        # Extract entities
        entities = self._extract_entities(data)
        
        # Extract concepts
        concepts = self._extract_concepts(data)
        
        # Detect sentiment
        sentiment = self._detect_sentiment(data)
        
        # Calculate confidence
        confidence = self._calculate_perception_confidence(data)
        
        # Calculate clarity
        clarity = self._calculate_clarity(data)
        
        # Calculate relevance
        relevance = self._calculate_relevance(data)
        
        return Perception(
            raw_data=data,
            type=data_type,
            entities=entities,
            concepts=concepts,
            sentiment=sentiment,
            confidence=confidence,
            clarity=clarity,
            relevance=relevance,
            processing_time=time.time() - start,
        )
    
    def _detect_data_type(self, data: Dict[str, Any]) -> str:
        """Detect data type from structure."""
        
        if "market" in data or "symbol" in data or "price" in data:
            return "market"
        if "text" in data or "content" in data or "message" in data:
            return "text"
        if "command" in data or "action" in data:
            return "command"
        if "event" in data:
            return "event"
        if "question" in data or "query" in data:
            return "question"
        if "cycle" in data or "timestamp" in data:
            return "cognitive_state"
        if "signal" in data:
            return "signal"
        if "pattern" in data:
            return "pattern"
        return "generic"
    
    def _extract_entities(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract entities from data."""
        
        entities = []
        
        # Extract from semantic processor
        if self.semantic_processor:
            try:
                if hasattr(self.semantic_processor, "extract_entities"):
                    result = self.semantic_processor.extract_entities(data)
                    if isinstance(result, list):
                        return result
            except Exception:
                pass
        
        # Fallback extraction
        for key in ["market", "symbol", "asset", "pair"]:
            if key in data:
                entities.append({"type": "asset", "name": str(data[key])})
                break
        
        for key in ["signal", "trend", "pattern"]:
            if key in data:
                entities.append({"type": "indicator", "name": str(data[key])})
                break
        
        return entities
    
    def _extract_concepts(self, data: Dict[str, Any]) -> List[str]:
        """Extract concepts from data."""
        
        concepts = []
        
        if self.semantic_processor:
            try:
                if hasattr(self.semantic_processor, "extract_concepts"):
                    result = self.semantic_processor.extract_concepts(data)
                    if isinstance(result, list):
                        return result
            except Exception:
                pass
        
        for key in ["pattern", "trend", "strategy", "analysis"]:
            if key in data:
                concepts.append(str(data[key]))
        
        return concepts
    
    def _detect_sentiment(self, data: Dict[str, Any]) -> str:
        """Detect sentiment from data."""
        
        if self.semantic_processor:
            try:
                if hasattr(self.semantic_processor, "detect_sentiment"):
                    result = self.semantic_processor.detect_sentiment(data)
                    if isinstance(result, str):
                        return result
            except Exception:
                pass
        
        if "signal" in data:
            signal = str(data["signal"]).lower()
            if signal in ["bullish", "positive", "up", "buy"]:
                return "positive"
            elif signal in ["bearish", "negative", "down", "sell"]:
                return "negative"
        
        if "sentiment" in data:
            return str(data["sentiment"])
        
        return "neutral"
    
    def _calculate_perception_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate perception confidence."""
        
        confidence = 0.5
        
        if "confidence" in data:
            try:
                confidence = float(data["confidence"])
                return max(0.0, min(1.0, confidence))
            except (ValueError, TypeError):
                pass
        
        # Calculate from data completeness
        fields_present = sum(1 for k in data if data.get(k) is not None)
        confidence = 0.3 + (fields_present / max(1, len(data))) * 0.5
        
        return max(0.0, min(1.0, confidence))
    
    def _calculate_clarity(self, data: Dict[str, Any]) -> float:
        """Calculate clarity of perception."""
        
        if not data:
            return 0.0
        
        # Check for unstructured data
        unstructured_keys = ["text", "content", "message", "raw"]
        structured_keys = ["market", "price", "signal", "pattern", "volume", "trend"]
        
        structured_count = sum(1 for k in structured_keys if k in data)
        unstructured_count = sum(1 for k in unstructured_keys if k in data)
        
        if structured_count > unstructured_count:
            return 0.7 + (structured_count / max(1, len(data))) * 0.3
        else:
            return 0.3 + (structured_count / max(1, len(data))) * 0.4
    
    def _calculate_relevance(self, data: Dict[str, Any]) -> float:
        """Calculate relevance to current goals."""
        
        if not self.current_goal:
            return 0.5
        
        # Check if data contains goal-related information
        goal_keywords = self.current_goal.name.split("_")
        data_str = str(data).lower()
        
        matches = sum(1 for keyword in goal_keywords if keyword in data_str)
        relevance = min(1.0, 0.3 + (matches / len(goal_keywords)) * 0.7)
        
        return relevance
    
    # ============================================================
    # PHASE 2: AWARENESS
    # ============================================================
    
    def _generate_awareness(self, perception: Perception) -> Awareness:
        """Generate awareness from perception."""
        
        # Market state
        market_state = self._determine_market_state(perception)
        
        # Pattern type
        pattern_type = self._determine_pattern_type(perception)
        
        # Risk level
        risk_level = self._determine_risk_level(perception, market_state, pattern_type)
        
        # Significance
        significance = self._calculate_significance(perception, market_state, pattern_type)
        
        # Context
        context = {
            "type": perception.type,
            "entities": perception.entities,
            "concepts": perception.concepts,
            "sentiment": perception.sentiment,
        }
        
        return Awareness(
            market_state=market_state,
            sentiment=perception.sentiment,
            pattern_type=pattern_type,
            risk_level=risk_level,
            confidence=perception.confidence,
            context=context,
            emotional_state=self.emotional_state.value,
            attention_focus=self.attention_focus,
            significance=significance,
        )
    
    def _determine_market_state(self, perception: Perception) -> str:
        """Determine market state."""
        
        raw = perception.raw_data
        
        if "signal" in raw:
            signal = str(raw["signal"]).lower()
            if signal in ["bullish", "buy", "long", "up", "positive"]:
                return "bullish"
            elif signal in ["bearish", "sell", "short", "down", "negative"]:
                return "bearish"
        
        if "trend" in raw:
            trend = str(raw["trend"]).lower()
            if trend in ["up", "bullish", "positive"]:
                return "bullish"
            elif trend in ["down", "bearish", "negative"]:
                return "bearish"
        
        if "forecast" in raw:
            forecast = str(raw["forecast"]).lower()
            if forecast in ["bullish", "up"]:
                return "bullish"
            elif forecast in ["bearish", "down"]:
                return "bearish"
        
        return "neutral"
    
    def _determine_pattern_type(self, perception: Perception) -> str:
        """Determine pattern type."""
        
        raw = perception.raw_data
        
        if "pattern" in raw:
            return str(raw["pattern"]).lower()
        
        if "candlestick_pattern" in raw:
            return str(raw["candlestick_pattern"]).lower()
        
        if "chart_pattern" in raw:
            return str(raw["chart_pattern"]).lower()
        
        return "none"
    
    def _determine_risk_level(self, perception: Perception, market_state: str, pattern_type: str) -> str:
        """Determine risk level."""
        
        if market_state == "neutral":
            return "medium"
        
        if pattern_type in ["breakout", "breakdown", "reversal", "double_top", "double_bottom"]:
            return "high"
        
        if market_state in ["bullish", "bearish"] and pattern_type == "none":
            return "medium"
        
        return "low"
    
    def _calculate_significance(self, perception: Perception, market_state: str, pattern_type: str) -> float:
        """Calculate significance of awareness."""
        
        significance = 0.5
        
        if market_state != "neutral":
            significance += 0.2
        
        if pattern_type != "none":
            significance += 0.2
        
        significance += perception.confidence * 0.2
        
        return max(0.0, min(1.0, significance))
    
    # ============================================================
    # PHASE 3: PATTERN RECOGNITION
    # ============================================================
    
    def _recognize_patterns(self, perception: Perception, awareness: Awareness) -> Dict[str, Any]:
        """Recognize patterns from perception and awareness."""
        
        patterns = {
            "detected": [],
            "confidence": 0.0,
            "pattern_names": [],
            "frequency": {},
            "novelty": "unknown",
            "pattern_count": 0,
        }
        
        raw = perception.raw_data
        
        # Use pattern engine if available
        if self.pattern_engine:
            try:
                if hasattr(self.pattern_engine, "detect"):
                    result = self.pattern_engine.detect(raw)
                    if isinstance(result, dict):
                        detected = result.get("detected", [])
                        for pattern in detected[:10]:
                            if isinstance(pattern, dict):
                                patterns["detected"].append(pattern)
                                name = pattern.get("name", "unknown")
                                if name not in patterns["pattern_names"]:
                                    patterns["pattern_names"].append(name)
            except Exception as e:
                logger.debug(f"Pattern engine error: {e}")
        
        # Built-in pattern detection
        if not patterns["detected"]:
            patterns = self._detect_builtin_patterns(perception, awareness, patterns)
        
        # Calculate confidence
        if patterns["detected"]:
            confidences = [p.get("confidence", 0.5) for p in patterns["detected"]]
            patterns["confidence"] = sum(confidences) / len(confidences)
        
        patterns["pattern_count"] = len(patterns["detected"])
        
        # Update stored patterns
        for pattern in patterns["detected"]:
            name = pattern.get("name", "")
            if name:
                if name not in self.patterns:
                    self.patterns[name] = {
                        "first_seen": datetime.now().isoformat(),
                        "count": 0,
                        "confidence": 0.0,
                        "last_seen": None,
                        "patterns": [],
                    }
                self.patterns[name]["count"] += 1
                self.patterns[name]["confidence"] = (
                    self.patterns[name]["confidence"] + pattern.get("confidence", 0.5)
                ) / 2
                self.patterns[name]["last_seen"] = datetime.now().isoformat()
        
        self.metrics["patterns_detected"] += len(patterns["detected"])
        
        return patterns
    
    def _detect_builtin_patterns(self, perception: Perception, awareness: Awareness, patterns: Dict) -> Dict:
        """Detect built-in patterns."""
        
        raw = perception.raw_data
        
        # Signal-based pattern
        if "signal" in raw:
            signal = str(raw["signal"]).upper()
            if signal in ["BUY", "SELL", "HOLD", "MONITOR"]:
                pattern = {
                    "name": f"signal_{signal}",
                    "type": "signal",
                    "value": signal,
                    "confidence": 0.6,
                }
                patterns["detected"].append(pattern)
                patterns["pattern_names"].append(pattern["name"])
        
        # Pattern-based pattern
        if awareness.pattern_type != "none":
            pattern = {
                "name": f"pattern_{awareness.pattern_type}",
                "type": "structural",
                "value": awareness.pattern_type,
                "confidence": 0.5,
            }
            patterns["detected"].append(pattern)
            patterns["pattern_names"].append(pattern["name"])
        
        # Trend-based pattern
        if awareness.market_state != "neutral":
            pattern = {
                "name": f"trend_{awareness.market_state}",
                "type": "trend",
                "value": awareness.market_state,
                "confidence": 0.5,
            }
            patterns["detected"].append(pattern)
            patterns["pattern_names"].append(pattern["name"])
        
        return patterns
    
    # ============================================================
    # PHASE 4: EMOTIONAL RESPONSE
    # ============================================================
    
    def _emotional_response(self, perception: Perception, awareness: Awareness, patterns: Dict) -> Dict[str, Any]:
        """Generate emotional response."""
        
        emotion = {
            "state": self.emotional_state.value,
            "intensity": self.emotional_intensity,
            "stability": self.emotional_stability,
            "shifts": [],
            "factors": [],
            "pattern_matches": [],
        }
        
        # Factors
        factors = []
        
        # Confidence factor
        if perception.confidence > 0.8:
            factors.append("high_confidence")
        elif perception.confidence < 0.3:
            factors.append("low_confidence")
        
        # Risk factor
        if awareness.risk_level == "high":
            factors.append("high_risk")
        elif awareness.risk_level == "low":
            factors.append("low_risk")
        
        # Novelty factor
        if patterns.get("novelty") == "high":
            factors.append("novel_pattern")
        elif patterns.get("novelty") == "low":
            factors.append("familiar_pattern")
        
        # Market state factor
        if awareness.market_state == "bullish":
            factors.append("bullish_market")
        elif awareness.market_state == "bearish":
            factors.append("bearish_market")
        
        # Signal factor
        if "signal" in perception.raw_data:
            signal = str(perception.raw_data["signal"]).upper()
            if signal in ["STRONG_BUY", "STRONG_SELL"]:
                factors.append("strong_signal")
            elif signal in ["BUY", "SELL"]:
                factors.append("signal")
        
        # Determine emotional state
        new_emotion = self._determine_emotion(factors, patterns, perception)
        
        # Apply emotional shift
        if new_emotion and new_emotion != self.emotional_state:
            emotion["shifts"].append(f"{self.emotional_state.value} -> {new_emotion.value}")
            self.emotional_state = new_emotion
            self.metrics["emotional_transitions"] += 1
            
            # Track emotional pattern
            key = f"{self.emotional_state.value}"
            self.emotional_patterns[key] = self.emotional_patterns.get(key, 0) + 1
        
        # Update intensity
        intensity_change = self._calculate_intensity_change(factors)
        self.emotional_intensity = max(0.0, min(1.0, self.emotional_intensity + intensity_change))
        
        # Update stability
        stability_change = self._calculate_stability_change(factors, len(emotion["shifts"]))
        self.emotional_stability = max(0.0, min(1.0, self.emotional_stability + stability_change))
        
        emotion["state"] = self.emotional_state.value
        emotion["intensity"] = round(self.emotional_intensity, 2)
        emotion["stability"] = round(self.emotional_stability, 2)
        emotion["factors"] = factors
        
        # Update emotional history
        self.emotional_history.append({
            "timestamp": datetime.now().isoformat(),
            "state": emotion["state"],
            "intensity": emotion["intensity"],
            "stability": emotion["stability"],
            "factors": factors,
        })
        if len(self.emotional_history) > 100:
            self.emotional_history = self.emotional_history[-100:]
        
        return emotion
    
    def _determine_emotion(self, factors: List[str], patterns: Dict, perception: Perception) -> Optional[EmotionalState]:
        """Determine emotional state from factors."""
        
        # High confidence + bullish = optimistic
        if "high_confidence" in factors and "bullish_market" in factors:
            return EmotionalState.OPTIMISTIC
        
        # Low confidence + bearish = cautious
        if "low_confidence" in factors and "bearish_market" in factors:
            return EmotionalState.CAUTIOUS
        
        # Novel pattern = curious
        if "novel_pattern" in factors:
            return EmotionalState.CURIOUS
        
        # High risk = cautious
        if "high_risk" in factors:
            return EmotionalState.CAUTIOUS
        
        # Strong signal = excited
        if "strong_signal" in factors:
            return EmotionalState.EXCITED
        
        # Familiar pattern + high confidence = confident
        if "familiar_pattern" in factors and "high_confidence" in factors:
            return EmotionalState.CONFIDENT
        
        # Many patterns = focused
        if patterns.get("pattern_count", 0) > 3:
            return EmotionalState.FOCUSED
        
        # Market state influences
        if "bullish_market" in factors:
            return EmotionalState.OPTIMISTIC
        if "bearish_market" in factors:
            return EmotionalState.CAUTIOUS
        
        # Default - stay calm
        return EmotionalState.CALM
    
    def _calculate_intensity_change(self, factors: List[str]) -> float:
        """Calculate emotional intensity change."""
        
        if not factors:
            return -0.02
        
        if len(factors) > 3:
            return 0.05
        elif len(factors) > 1:
            return 0.02
        else:
            return -0.01
    
    def _calculate_stability_change(self, factors: List[str], shifts: int) -> float:
        """Calculate emotional stability change."""
        
        if shifts > 0:
            return -0.05
        
        if len(factors) > 3:
            return 0.01
        else:
            return 0.005
    
    # ============================================================
    # PHASE 5: INTUITION
    # ============================================================
    
    def _generate_intuition(self, perception: Perception, patterns: Dict, emotion: Dict) -> Intuition:
        """Generate intuition from patterns and experience."""
        
        signal = "neutral"
        confidence = 0.5
        strength = "MODERATE"
        gut_feeling = "wait"
        reasons = []
        source = "experience"
        pattern_matches = []
        experience_count = len(self.experiences)
        
        # Intuition from patterns
        if patterns["detected"]:
            primary_pattern = patterns["detected"][0]
            pattern_name = primary_pattern.get("name", "").lower()
            pattern_conf = primary_pattern.get("confidence", 0.5)
            pattern_matches.append(pattern_name)
            
            if "bullish" in pattern_name or "breakout" in pattern_name or "buy" in pattern_name:
                signal = "bullish"
                confidence = pattern_conf * 0.8
                gut_feeling = "buy"
                reasons.append(f"Pattern: {pattern_name}")
                source = "pattern_recognition"
            
            elif "bearish" in pattern_name or "breakdown" in pattern_name or "sell" in pattern_name:
                signal = "bearish"
                confidence = pattern_conf * 0.8
                gut_feeling = "sell"
                reasons.append(f"Pattern: {pattern_name}")
                source = "pattern_recognition"
            
            else:
                gut_feeling = "wait"
                reasons.append("No clear pattern signal")
        
        # Intuition from experience
        if self.experiences:
            similar = self._find_similar_experiences(perception)
            if similar:
                success_rate = sum(1 for e in similar if e.get("outcome", False)) / len(similar)
                if success_rate > 0.6:
                    confidence = min(1.0, confidence + 0.2)
                    reasons.append(f"{len(similar)} similar experiences: {success_rate:.0%} success")
                    source = "experience"
                else:
                    confidence = max(0.0, confidence - 0.1)
                    reasons.append(f"{len(similar)} similar experiences: {success_rate:.0%} success (caution)")
                    source = "experience"
        
        # Intuition from emotional state
        if emotion["state"] in ["OPTIMISTIC", "CONFIDENT", "EXCITED"]:
            confidence = min(1.0, confidence + 0.1)
            reasons.append(f"Emotional state: {emotion['state']} (positive influence)")
        elif emotion["state"] in ["CAUTIOUS", "UNCERTAIN", "ANXIOUS"]:
            confidence = max(0.0, confidence - 0.1)
            reasons.append(f"Emotional state: {emotion['state']} (cautious influence)")
        
        # Determine strength
        if confidence >= 0.8:
            strength = "VERY_STRONG"
        elif confidence >= 0.6:
            strength = "STRONG"
        elif confidence >= 0.4:
            strength = "MODERATE"
        else:
            strength = "WEAK"
        
        return Intuition(
            signal=signal,
            confidence=max(0.0, min(1.0, confidence)),
            strength=strength,
            gut_feeling=gut_feeling,
            reasons=reasons[:5],
            source=source,
            pattern_matches=pattern_matches,
            experience_count=experience_count,
        )
    
    def _find_similar_experiences(self, perception: Perception) -> List[Experience]:
        """Find similar experiences from history."""
        
        similar = []
        raw = perception.raw_data
        
        for exp in self.experiences[-100:]:
            exp_raw = exp.input
            
            matches = 0
            total = 0
            
            for key in ["market", "symbol", "signal", "pattern", "type"]:
                if key in raw and key in exp_raw:
                    total += 1
                    if str(raw[key]).lower() == str(exp_raw[key]).lower():
                        matches += 1
            
            if total > 0 and matches / total > 0.5:
                similar.append(exp)
        
        return similar
    
    # ============================================================
    # PHASE 6: DECISION MAKING
    # ============================================================
    
    def _make_decision(
        self,
        perception: Perception,
        awareness: Awareness,
        patterns: Dict,
        intuition: Intuition,
        emotion: Dict
    ) -> Decision:
        """Make decision based on all inputs."""
        
        start = time.time()
        
        action = "wait"
        confidence = 0.5
        reasons = []
        risk = "medium"
        alternatives = []
        
        # ============================================
        # FACTOR 1: AWARENESS
        # ============================================
        
        market_state = awareness.market_state
        pattern_type = awareness.pattern_type
        
        if market_state == "bullish" and pattern_type in ["breakout", "reversal"]:
            action = "buy"
            confidence = intuition.confidence
            reasons.append("Bullish market with breakout/reversal pattern")
            risk = "medium"
        
        elif market_state == "bearish" and pattern_type in ["breakdown", "reversal"]:
            action = "sell"
            confidence = intuition.confidence
            reasons.append("Bearish market with breakdown/reversal pattern")
            risk = "medium"
        
        elif market_state == "bullish":
            action = "monitor"
            confidence = intuition.confidence * 0.7
            reasons.append("Bullish market but no clear pattern")
            risk = "low"
        
        elif market_state == "bearish":
            action = "monitor"
            confidence = intuition.confidence * 0.7
            reasons.append("Bearish market but no clear pattern")
            risk = "low"
        
        else:
            action = "wait"
            confidence = 0.5
            reasons.append("No clear market direction")
            risk = "low"
        
        # ============================================
        # FACTOR 2: INTUITION OVERRIDE
        # ============================================
        
        if intuition.confidence > self.intuition_threshold:
            if intuition.gut_feeling in ["buy", "sell"]:
                action = intuition.gut_feeling
                confidence = intuition.confidence
                reasons.append(f"Intuition: {intuition.gut_feeling}")
                reasons.append(f"Intuition confidence: {intuition.confidence:.0%}")
        
        # ============================================
        # FACTOR 3: EMOTIONAL INFLUENCE
        # ============================================
        
        if emotion["state"] in ["OPTIMISTIC", "CONFIDENT", "EXCITED"]:
            confidence = min(1.0, confidence + 0.05)
            reasons.append(f"Emotional influence: {emotion['state']} (+confidence)")
        elif emotion["state"] in ["CAUTIOUS", "UNCERTAIN", "ANXIOUS"]:
            confidence = max(0.0, confidence - 0.05)
            reasons.append(f"Emotional influence: {emotion['state']} (-confidence)")
            if risk == "medium":
                risk = "high"
        
        # ============================================
        # FACTOR 4: RISK ADJUSTMENT
        # ============================================
        
        if awareness.risk_level == "high":
            risk = "high"
            confidence *= 0.85
            reasons.append("High risk detected, reducing confidence")
            alternatives.append("wait")
            alternatives.append("monitor")
        
        # ============================================
        # FACTOR 5: EXPERIENCE
        # ============================================
        
        if self.experiences:
            similar = self._find_similar_experiences(perception)
            if similar:
                success_rate = sum(1 for e in similar if e.get("outcome", False)) / len(similar)
                if success_rate > 0.7 and action != "wait":
                    confidence = min(1.0, confidence + 0.1)
                    reasons.append(f"Similar experiences: {success_rate:.0%} success")
                elif success_rate < 0.3:
                    confidence = max(0.0, confidence - 0.1)
                    reasons.append(f"Similar experiences: {success_rate:.0%} success (caution)")
        
        # ============================================
        # FACTOR 6: GOAL ALIGNMENT
        # ============================================
        
        if self.current_goal:
            if self.current_goal.name in ["master_decision_making", "develop_intuition"]:
                # Encourage decision making for learning
                if action == "wait":
                    action = "monitor"
                    confidence = max(0.5, confidence)
                    reasons.append(f"Goal alignment: {self.current_goal.name}")
        
        # ============================================
        # FINALIZE
        # ============================================
        
        confidence = max(0.0, min(1.0, confidence))
        
        expected_outcome = None
        if action == "buy":
            expected_outcome = "price_increase"
        elif action == "sell":
            expected_outcome = "price_decrease"
        elif action == "hold":
            expected_outcome = "price_fluctuation"
        elif action == "monitor":
            expected_outcome = "no_change"
        else:
            expected_outcome = "uncertain"
        
        decision = Decision(
            action=action,
            confidence=confidence,
            reasons=reasons[:5],
            risk=risk,
            expected_outcome=expected_outcome,
            alternatives=alternatives,
            decision_time=time.time() - start,
        )
        
        self.metrics["decisions_made"] += 1
        
        return decision
    
    # ============================================================
    # PHASE 7: LEARNING
    # ============================================================
    
    def _learn_from_experience(self, perception: Perception, decision: Decision) -> Dict[str, Any]:
        """Learn from experience."""
        
        start = time.time()
        
        learning = {
            "status": "learned",
            "timestamp": datetime.now().isoformat(),
            "insights": [],
            "knowledge_updated": False,
            "patterns_updated": False,
            "confidence_adjustment": 0.0,
            "learning_quality": 0.0,
            "duration": 0.0,
        }
        
        # Use learning engine if available
        if self.learning_engine:
            try:
                if hasattr(self.learning_engine, "learn"):
                    result = self.learning_engine.learn({
                        "perception": perception.raw_data,
                        "decision": {
                            "action": decision.action,
                            "confidence": decision.confidence,
                            "reasons": decision.reasons,
                        },
                        "context": perception.raw_data,
                    })
                    if isinstance(result, dict):
                        learning["knowledge_updated"] = result.get("success", False)
                        learning["insights"].extend(result.get("insights", []))
            except Exception as e:
                logger.debug(f"Learning engine error: {e}")
        
        # Update patterns based on decision
        if decision.action != "wait":
            pattern_name = f"decision_{decision.action}"
            if pattern_name not in self.patterns:
                self.patterns[pattern_name] = {
                    "first_seen": datetime.now().isoformat(),
                    "count": 0,
                    "confidence": 0.0,
                    "last_seen": None,
                }
            self.patterns[pattern_name]["count"] += 1
            self.patterns[pattern_name]["confidence"] = (
                self.patterns[pattern_name]["confidence"] + decision.confidence
            ) / 2
            self.patterns[pattern_name]["last_seen"] = datetime.now().isoformat()
            learning["patterns_updated"] = True
        
        # Create experience
        experience = Experience(
            id=f"exp_{self.process_count}_{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            input=perception.raw_data,
            perception=perception.to_dict(),
            awareness={},  # Will be updated with awareness
            decision=decision.to_dict(),
            outcome=None,
            emotional_state=self.emotional_state.value,
            significance=perception.relevance,
            learning=learning,
            reflection={},
        )
        
        self.experiences.append(experience)
        if len(self.experiences) > self.max_experiences:
            self.experiences = self.experiences[-self.max_experiences:]
        
        # Update learning metrics
        self.metrics["learnings_acquired"] += 1
        
        # Calculate learning quality
        learning["learning_quality"] = min(1.0, 0.5 + (decision.confidence * 0.5))
        learning["duration"] = time.time() - start
        
        return learning
    
    # ============================================================
    # PHASE 8: REFLECTION
    # ============================================================
    
    def _reflect(self, perception: Perception, decision: Decision, learning: Dict) -> Reflection:
        """Reflect on the experience."""
        
        start = time.time()
        self.metrics["reflections_created"] += 1
        
        learnings = []
        improvements = []
        insights = []
        emotional_shift = None
        
        # Reflection on decision
        if decision.confidence > 0.7:
            learnings.append(f"High confidence decision: {decision.action}")
            insights.append("Confidence is high, likely a good decision context")
        elif decision.confidence < 0.3:
            learnings.append(f"Low confidence decision: {decision.action}")
            improvements.append("Need more information before deciding")
            insights.append("Low confidence indicates uncertainty or incomplete data")
        
        # Reflection on patterns
        if learning.get("patterns_updated"):
            learnings.append("New patterns recognized and stored")
            insights.append("Pattern recognition is active and learning")
        
        # Reflection on emotional state
        if self.emotional_state.value in ["CALM", "FOCUSED", "WISE"]:
            learnings.append(f"Emotionally stable: {self.emotional_state.value}")
            insights.append("Stable emotional state supports good decision making")
        elif self.emotional_state.value in ["CAUTIOUS", "UNCERTAIN", "ANXIOUS"]:
            learnings.append(f"Emotional caution: {self.emotional_state.value}")
            improvements.append("Consider emotional factors in decision making")
        
        # Reflection on experience
        if self.experiences:
            recent = self.experiences[-10:]
            successful = sum(1 for e in recent if e.outcome is True)
            if successful > 6:
                learnings.append(f"Recent success rate: {successful}/10")
                insights.append("Recent performance is good")
            elif successful < 3:
                learnings.append(f"Recent success rate: {successful}/10")
                improvements.append("Need to review recent decisions")
                insights.append("Recent performance needs improvement")
        
        # Generate new insights
        if decision.confidence > 0.8 and decision.action not in ["wait", "monitor"]:
            insights.append(f"Strong decision: {decision.action} with high confidence")
        if decision.confidence < 0.3 and decision.action != "wait":
            insights.append(f"Weak decision: {decision.action} with low confidence - need more data")
        
        # Reflection quality
        reflection_quality = min(1.0, 0.3 + (len(learnings) * 0.1) + (len(insights) * 0.1))
        
        # Store reflection
        reflection = Reflection(
            decision=decision.action,
            confidence=decision.confidence,
            learnings=learnings[:5],
            improvements=improvements[:5],
            insights=insights[:5],
            emotional_shift=emotional_shift,
            reflection_quality=reflection_quality,
            duration=time.time() - start,
        )
        
        # Update reflections list
        self.reflections.append(reflection.to_dict())
        if len(self.reflections) > self.max_reflections:
            self.reflections = self.reflections[-self.max_reflections:]
        
        # Generate insights from reflection
        for insight in insights:
            self.insights.append({
                "text": insight,
                "timestamp": datetime.now().isoformat(),
                "source": "reflection",
                "decision": decision.action,
                "confidence": decision.confidence,
            })
        
        self.metrics["insights_generated"] += len(insights)
        
        return reflection
    
    # ============================================================
    # PHASE 9: METACOGNITION
    # ============================================================
    
    def _metacognition(
        self,
        perception: Perception,
        awareness: Awareness,
        decision: Decision,
        reflection: Reflection
    ) -> Dict[str, Any]:
        """Metacognition - thinking about thinking."""
        
        # Self-assessment
        self_assessment = {
            "confidence_accuracy": decision.confidence,
            "decision_quality": "good" if decision.confidence > 0.6 else "needs_improvement",
            "awareness_accuracy": awareness.confidence,
            "emotional_awareness": self.emotional_state.value,
            "attention_focus": awareness.attention_focus,
            "pattern_recognition_active": len(self.patterns) > 0,
            "reflection_quality": reflection.reflection_quality,
        }
        
        # Performance evaluation
        performance = {
            "total_decisions": self.metrics["decisions_made"],
            "decision_confidence_avg": self.average_confidence,
            "patterns_learned": len(self.patterns),
            "experiences": len(self.experiences),
            "emotional_stability": self.emotional_stability,
            "insights_generated": self.metrics["insights_generated"],
            "success_rate": (
                self.metrics["successful_decisions"] / max(1, self.metrics["decisions_made"])
            ),
        }
        
        # Self-awareness update
        self.self_awareness["performance_summary"] = performance
        
        # Growth assessment
        growth = {
            "stage": self.growth_stage.value,
            "progress": round(self.growth_progress, 2),
            "skills": self.skill_levels,
            "next_milestone": self._get_next_milestone(),
            "areas_for_improvement": self._identify_improvement_areas(perception, decision),
        }
        
        return {
            "self_assessment": self_assessment,
            "performance": performance,
            "growth": growth,
            "self_awareness_summary": self.self_awareness,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _get_next_milestone(self) -> str:
        """Get next growth milestone."""
        
        current = self.growth_stage
        
        milestones = {
            GrowthStage.EMBRYONIC: "Reach 10 experiences",
            GrowthStage.BEGINNER: "Reach 50 experiences",
            GrowthStage.LEARNER: "Reach 100 experiences",
            GrowthStage.DEVELOPING: "Reach 200 experiences",
            GrowthStage.MATURING: "Reach 500 experiences",
            GrowthStage.ADVANCED: "Reach 1000 experiences",
            GrowthStage.MASTER: "Reach 2000 experiences",
            GrowthStage.SAGE: "Achieve 90% decision accuracy",
        }
        
        return milestones.get(current, "Continue learning")
    
    def _identify_improvement_areas(self, perception: Perception, decision: Decision) -> List[str]:
        """Identify areas for improvement."""
        
        areas = []
        
        if decision.confidence < 0.5:
            areas.append("Decision confidence needs improvement")
        
        if len(self.patterns) < 5:
            areas.append("Pattern recognition needs development")
        
        if self.emotional_stability < 0.5:
            areas.append("Emotional stability needs improvement")
        
        if perception.clarity < 0.5:
            areas.append("Perception clarity needs improvement")
        
        if self.awareness_level < 0.4:
            areas.append("Awareness level needs improvement")
        
        return areas
    
    # ============================================================
    # PHASE 10: STATE UPDATE
    # ============================================================
    
    def _update_state(
        self,
        perception: Perception,
        awareness: Awareness,
        decision: Decision,
        learning: Dict,
        reflection: Reflection
    ) -> None:
        """Update internal state."""
        
        # Update awareness level
        if decision.confidence > 0.7:
            self.awareness_level = min(1.0, self.awareness_level + 0.01)
        elif decision.confidence < 0.3:
            self.awareness_level = max(0.0, self.awareness_level - 0.01)
        
        # Update curiosity
        if awareness.pattern_type != "none" and perception.confidence > 0.6:
            self.curiosity_level = min(1.0, self.curiosity_level + 0.005)
        else:
            self.curiosity_level = max(0.3, self.curiosity_level - 0.002)
        
        # Update confidence base
        if len(self.experiences) > 10:
            success_rate = self.metrics["successful_decisions"] / max(1, self.metrics["decisions_made"])
            self.confidence_base = 0.5 + (success_rate - 0.5) * 0.5
            self.confidence_base = max(0.1, min(0.9, self.confidence_base))
        
        # Update performance scores
        self.performance_scores.append(decision.confidence)
        if len(self.performance_scores) > 100:
            self.performance_scores = self.performance_scores[-100:]
        self.average_performance = sum(self.performance_scores) / len(self.performance_scores)
        
        # Update confidence scores
        self.confidence_scores.append(decision.confidence)
        if len(self.confidence_scores) > 100:
            self.confidence_scores = self.confidence_scores[-100:]
        self.average_confidence = sum(self.confidence_scores) / len(self.confidence_scores)
        
        # Update attention focus
        if awareness.pattern_type != "none":
            self.attention_focus = awareness.pattern_type
        else:
            self.attention_focus = awareness.market_state
        
        # Update growth
        self._update_growth()
        
        # Update goals
        self._update_goals(decision, learning, reflection)
    
    # ============================================================
    # GROWTH MANAGEMENT
    # ============================================================
    
    def _update_growth(self) -> None:
        """Update growth stage and progress."""
        
        experience_count = len(self.experiences)
        
        # Determine growth stage
        if experience_count < 10:
            self.growth_stage = GrowthStage.EMBRYONIC
        elif experience_count < 50:
            self.growth_stage = GrowthStage.BEGINNER
        elif experience_count < 100:
            self.growth_stage = GrowthStage.LEARNER
        elif experience_count < 200:
            self.growth_stage = GrowthStage.DEVELOPING
        elif experience_count < 500:
            self.growth_stage = GrowthStage.MATURING
        elif experience_count < 1000:
            self.growth_stage = GrowthStage.ADVANCED
        elif experience_count < 2000:
            self.growth_stage = GrowthStage.MASTER
        else:
            self.growth_stage = GrowthStage.SAGE
        
        # Calculate growth progress
        stage_progress = {
            GrowthStage.EMBRYONIC: min(1.0, experience_count / 10),
            GrowthStage.BEGINNER: min(1.0, (experience_count - 10) / 40),
            GrowthStage.LEARNER: min(1.0, (experience_count - 50) / 50),
            GrowthStage.DEVELOPING: min(1.0, (experience_count - 100) / 100),
            GrowthStage.MATURING: min(1.0, (experience_count - 200) / 300),
            GrowthStage.ADVANCED: min(1.0, (experience_count - 500) / 500),
            GrowthStage.MASTER: min(1.0, (experience_count - 1000) / 1000),
            GrowthStage.SAGE: min(1.0, (experience_count - 2000) / 1000),
        }
        
        self.growth_progress = stage_progress.get(self.growth_stage, 0.0) * 100
        
        # Update skills based on growth stage
        self._update_skills()
        
        # Trigger growth callback
        if self.growth_progress >= 100 and self.growth_stage != GrowthStage.SAGE:
            self._trigger_callbacks("on_growth", {
                "new_stage": self.growth_stage.value,
                "progress": self.growth_progress,
            })
    
    # FIX: Alias untuk backward compatibility
    def _update_growth_stage(self) -> None:
        """Alias for _update_growth() for backward compatibility."""
        self._update_growth()
    
    def _update_skills(self) -> None:
        """Update skill levels based on growth stage."""
        
        stage_multiplier = {
            GrowthStage.EMBRYONIC: 0.1,
            GrowthStage.BEGINNER: 0.2,
            GrowthStage.LEARNER: 0.35,
            GrowthStage.DEVELOPING: 0.5,
            GrowthStage.MATURING: 0.65,
            GrowthStage.ADVANCED: 0.8,
            GrowthStage.MASTER: 0.9,
            GrowthStage.SAGE: 0.95,
        }
        
        base = stage_multiplier.get(self.growth_stage, 0.1)
        
        for skill in self.skill_levels:
            # Add experience-based increase
            experience_bonus = min(0.2, len(self.experiences) / 5000)
            self.skill_levels[skill] = min(1.0, base + experience_bonus)
    
    # ============================================================
    # GOAL MANAGEMENT
    # ============================================================
    
    def _update_goals(self, decision: Decision, learning: Dict, reflection: Reflection) -> None:
        """Update goal progress."""
        
        for goal in self.goals:
            if goal.status != "active":
                continue
            
            progress_increment = 0.0
            
            if goal.name == "master_perception":
                if len(self.patterns) > 10:
                    progress_increment = 0.5
                if self.awareness_level > 0.6:
                    progress_increment += 0.5
            
            elif goal.name == "develop_intuition":
                if len(self.experiences) > 20 and decision.confidence > 0.6:
                    progress_increment = 1.0
                if intuition := self._get_last_intuition():
                    if intuition.confidence > 0.7:
                        progress_increment += 0.5
            
            elif goal.name == "master_decision_making":
                if len(self.experiences) > 10:
                    success_rate = self.metrics["successful_decisions"] / max(1, self.metrics["decisions_made"])
                    progress_increment = success_rate * 2
            
            elif goal.name == "continuous_learning":
                if learning.get("knowledge_updated"):
                    progress_increment = 1.0
                if reflection.learnings:
                    progress_increment += 0.5
            
            elif goal.name == "emotional_intelligence":
                if self.emotional_stability > 0.7:
                    progress_increment = 0.5
                if len(self.emotional_history) > 20:
                    progress_increment += 0.5
            
            # Apply increment
            goal.progress = min(100.0, goal.progress + progress_increment)
            
            # Check completion
            if goal.progress >= 100.0:
                goal.status = "completed"
                goal.completed_at = datetime.now().isoformat()
                self.completed_goals.append(goal)
                self.metrics["goal_completions"] += 1
                
                self._trigger_callbacks("on_goal_complete", goal.to_dict())
                
                # Activate next goal
                for g in self.goals:
                    if g.status == "pending":
                        g.status = "active"
                        self.current_goal = g
                        break
    
    def _get_last_intuition(self) -> Optional[Intuition]:
        """Get last intuition from history."""
        for item in reversed(self.history):
            if "intuition" in item:
                try:
                    return Intuition(**item["intuition"])
                except Exception:
                    pass
        return None
    
    # ============================================================
    # CALLBACK MANAGEMENT
    # ============================================================
    
    def _trigger_callbacks(self, event: str, data: Any) -> None:
        """Trigger callbacks for an event."""
        if event not in self._callbacks:
            return
        
        for callback in self._callbacks[event]:
            try:
                callback(data)
            except Exception as e:
                logger.debug(f"Callback error for {event}: {e}")
    
    def on(self, event: str, callback: Callable) -> None:
        """Register a callback."""
        if event in self._callbacks:
            self._callbacks[event].append(callback)
    
    # ============================================================
    # OUTCOME FEEDBACK
    # ============================================================
    
    def feedback(self, outcome: bool, details: Optional[Dict] = None) -> None:
        """
        Provide feedback on outcome.
        
        Args:
            outcome: True if successful, False if failed
            details: Additional details about outcome
        """
        with self.lock:
            if not self.experiences:
                return
            
            # Update last experience
            last_exp = self.experiences[-1]
            last_exp.outcome = outcome
            
            if outcome:
                self.metrics["successful_decisions"] += 1
            else:
                self.metrics["failed_decisions"] += 1
            
            # Update learning from outcome
            if details:
                if last_exp.learning:
                    last_exp.learning["outcome"] = {
                        "success": outcome,
                        "details": details,
                    }
            
            # Generate outcome reflection
            if not outcome:
                self._generate_outcome_reflection(last_exp)
    
    def _generate_outcome_reflection(self, experience: Experience) -> None:
        """Generate reflection on failed outcome."""
        
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "type": "outcome_analysis",
            "decision": experience.decision,
            "outcome": False,
            "learnings": [],
            "improvements": [],
        }
        
        # Analyze what went wrong
        if "confidence" in experience.decision:
            confidence = experience.decision.get("confidence", 0.5)
            if confidence < 0.5:
                reflection["learnings"].append("Decision confidence was too low")
                reflection["improvements"].append("Seek more information before deciding")
        
        if "risk" in experience.decision:
            risk = experience.decision.get("risk", "medium")
            if risk == "high":
                reflection["learnings"].append("Risk was too high for this decision")
                reflection["improvements"].append("Consider lower risk options")
        
        self.reflections.append(reflection)
        self.metrics["reflections_created"] += 1
    
    # ============================================================
    # PUBLIC METHODS
    # ============================================================
    
    def start(self) -> bool:
        """Start consciousness."""
        if self.running:
            return False
        
        self.running = True
        self.paused = False
        self._shutdown = False
        self.state = ConsciousnessState.ACTIVE
        
        logger.info("Consciousness started.")
        return True
    
    def stop(self) -> bool:
        """Stop consciousness."""
        if not self.running:
            return False
        
        self.running = False
        self.state = ConsciousnessState.STOPPED
        
        logger.info("Consciousness stopped.")
        return True
    
    def pause(self) -> bool:
        """Pause consciousness processing."""
        if not self.running or self.paused:
            return False
        
        self.paused = True
        self.state = ConsciousnessState.PAUSED
        
        logger.info("Consciousness paused.")
        return True
    
    def resume(self) -> bool:
        """Resume consciousness processing."""
        if not self.running or not self.paused:
            return False
        
        self.paused = False
        self.state = ConsciousnessState.ACTIVE
        
        logger.info("Consciousness resumed.")
        return True
    
    def shutdown(self) -> bool:
        """Shutdown consciousness."""
        self._shutdown = True
        self.running = False
        self.state = ConsciousnessState.STOPPED
        
        # Save state
        self._save_state()
        
        logger.info("Consciousness shutdown complete.")
        return True
    
    def reset(self) -> bool:
        """Reset consciousness."""
        with self.lock:
            self.history.clear()
            self.process_history.clear()
            self.short_term_memory.clear()
            self.long_term_memory.clear()
            self.working_memory.clear()
            self.patterns.clear()
            self.experiences.clear()
            self.emotional_history.clear()
            self.performance_scores.clear()
            self.confidence_scores.clear()
            self.insights.clear()
            self.reflections.clear()
            self.learnings.clear()
            self.goals.clear()
            self.completed_goals.clear()
            
            self.process_count = 0
            self.error_count = 0
            self.success_count = 0
            self.awareness_level = 0.5
            self.curiosity_level = 0.7
            self.confidence_base = 0.5
            self.emotional_state = EmotionalState.CALM
            self.emotional_intensity = 0.5
            self.emotional_stability = 0.8
            self.average_performance = 0.0
            self.average_confidence = 0.0
            
            self.metrics = {
                "total_processes": 0,
                "successful_processes": 0,
                "failed_processes": 0,
                "patterns_detected": 0,
                "decisions_made": 0,
                "successful_decisions": 0,
                "failed_decisions": 0,
                "reflections_created": 0,
                "insights_generated": 0,
                "learnings_acquired": 0,
                "emotional_transitions": 0,
                "goal_completions": 0,
                "memory_accesses": 0,
            }
            
            self._initialize_goals()
            self._initialize_skills()
            self._update_growth()
            self.state = ConsciousnessState.IDLE
            
            logger.info("Consciousness reset.")
            return True
    
    # ============================================================
    # GETTERS
    # ============================================================
    
    def get_state(self) -> Dict[str, Any]:
        """Get consciousness state."""
        return {
            "state": self.state.value,
            "running": self.running,
            "paused": self.paused,
            "shutdown": self._shutdown,
            "process_count": self.process_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "uptime": self.uptime,
            "awareness_level": self.awareness_level,
            "curiosity_level": self.curiosity_level,
            "confidence_base": self.confidence_base,
            "emotional_state": self.emotional_state.value,
            "emotional_intensity": self.emotional_intensity,
            "emotional_stability": self.emotional_stability,
            "attention_focus": self.attention_focus,
            "patterns_count": len(self.patterns),
            "experiences_count": len(self.experiences),
            "insights_count": len(self.insights),
            "reflections_count": len(self.reflections),
            "goals": [g.to_dict() for g in self.goals],
            "current_goal": self.current_goal.to_dict() if self.current_goal else None,
            "completed_goals": len(self.completed_goals),
            "metrics": self.metrics,
            "average_performance": self.average_performance,
            "average_confidence": self.average_confidence,
            "growth_stage": self.growth_stage.value,
            "growth_progress": self.growth_progress,
            "skills": self.skill_levels,
            "self_awareness": self.self_awareness,
            "started_at": self.started_at,
            "last_update": self.last_update,
            "last_error": self.last_error,
            "last_error_time": self.last_error_time,
        }
    
    def status(self) -> Dict[str, Any]:
        """Get consciousness status."""
        success_rate = (
            self.metrics["successful_decisions"] / max(1, self.metrics["decisions_made"])
        )
        
        return {
            "module": "consciousness",
            "version": self.VERSION,
            "state": self.state.value,
            "running": self.running,
            "processes": self.process_count,
            "successes": self.success_count,
            "errors": self.error_count,
            "awareness": round(self.awareness_level * 100, 1),
            "curiosity": round(self.curiosity_level * 100, 1),
            "emotional_state": self.emotional_state.value,
            "emotional_stability": round(self.emotional_stability * 100, 1),
            "patterns": len(self.patterns),
            "experiences": len(self.experiences),
            "decisions": self.metrics["decisions_made"],
            "success_rate": round(success_rate * 100, 1),
            "performance": round(self.average_performance * 100, 1),
            "insights": len(self.insights),
            "reflections": len(self.reflections),
            "growth_stage": self.growth_stage.value,
            "growth_progress": round(self.growth_progress, 1),
            "goal_completions": self.metrics["goal_completions"],
            "timestamp": datetime.now().isoformat(),
        }
    
    def snapshot(self) -> Dict[str, Any]:
        """Get full snapshot."""
        return {
            "engine": {
                "name": "Consciousness",
                "version": self.VERSION,
                "state": self.state.value,
                "running": self.running,
                "started_at": self.started_at,
                "uptime": self.uptime,
            },
            "awareness": {
                "level": self.awareness_level,
                "curiosity": self.curiosity_level,
                "confidence": self.confidence_base,
                "attention": self.attention_focus,
                "context": self.context,
            },
            "emotional": {
                "state": self.emotional_state.value,
                "intensity": self.emotional_intensity,
                "stability": self.emotional_stability,
                "history": self.emotional_history[-20:],
                "patterns": self.emotional_patterns,
            },
            "knowledge": {
                "patterns": len(self.patterns),
                "patterns_detail": {k: v for k, v in list(self.patterns.items())[:10]},
                "experiences": len(self.experiences),
                "insights": self.insights[-10:],
                "reflections": self.reflections[-10:],
                "learnings": self.learnings[-10:],
            },
            "goals": {
                "active": [g.to_dict() for g in self.goals if g.status == "active"],
                "completed": len(self.completed_goals),
                "current": self.current_goal.to_dict() if self.current_goal else None,
            },
            "performance": {
                "metrics": self.metrics,
                "average": self.average_performance,
                "confidence_avg": self.average_confidence,
                "success_rate": (
                    self.metrics["successful_decisions"] / max(1, self.metrics["decisions_made"])
                ),
            },
            "growth": {
                "stage": self.growth_stage.value,
                "progress": self.growth_progress,
                "skills": self.skill_levels,
                "capabilities": self.self_awareness["capabilities"],
                "strengths": self.self_awareness["strengths"],
                "weaknesses": self.self_awareness["weaknesses"],
            },
            "metacognition": {
                "self_awareness": self.self_awareness,
                "performance_summary": self.self_awareness.get("performance_summary", {}),
            },
            "history_count": len(self.history),
            "timestamp": datetime.now().isoformat(),
        }
    
    def get_insights(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent insights."""
        return self.insights[-limit:] if self.insights else []
    
    def get_reflections(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent reflections."""
        return self.reflections[-limit:] if self.reflections else []
    
    def get_experiences(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent experiences."""
        return [e.to_dict() for e in self.experiences[-limit:]] if self.experiences else []
    
    def get_patterns(self, limit: int = 20) -> Dict[str, Dict[str, Any]]:
        """Get patterns."""
        items = list(self.patterns.items())
        return dict(items[-limit:]) if items else {}
    
    def get_emotional_state(self) -> Dict[str, Any]:
        """Get current emotional state."""
        return {
            "state": self.emotional_state.value,
            "intensity": self.emotional_intensity,
            "stability": self.emotional_stability,
            "awareness": self.awareness_level,
            "history": self.emotional_history[-10:],
        }
    
    def get_goals(self) -> List[Dict[str, Any]]:
        """Get all goals."""
        return [g.to_dict() for g in self.goals]
    
    def get_growth_summary(self) -> Dict[str, Any]:
        """Get growth summary."""
        return {
            "stage": self.growth_stage.value,
            "progress": self.growth_progress,
            "skills": self.skill_levels,
            "capabilities": self.self_awareness["capabilities"],
            "strengths": self.self_awareness["strengths"],
            "weaknesses": self.self_awareness["weaknesses"],
            "growth_areas": self.self_awareness["growth_areas"],
            "next_milestone": self._get_next_milestone(),
            "experience_count": len(self.experiences),
            "pattern_count": len(self.patterns),
            "insight_count": len(self.insights),
            "reflection_count": len(self.reflections),
        }
    
    # ============================================================
    # UTILITY METHODS
    # ============================================================
    
    def _save_state(self) -> None:
        """Save consciousness state to file."""
        try:
            state_file = self.config.get("state_file", "database/consciousness_state.json")
            import os
            
            os.makedirs(os.path.dirname(state_file), exist_ok=True)
            
            state_data = {
                "version": self.VERSION,
                "process_count": self.process_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
                "awareness_level": self.awareness_level,
                "curiosity_level": self.curiosity_level,
                "confidence_base": self.confidence_base,
                "emotional_state": self.emotional_state.value,
                "emotional_intensity": self.emotional_intensity,
                "emotional_stability": self.emotional_stability,
                "patterns": len(self.patterns),
                "experiences": len(self.experiences),
                "metrics": self.metrics,
                "growth_stage": self.growth_stage.value,
                "growth_progress": self.growth_progress,
                "skills": self.skill_levels,
                "goals": [g.to_dict() for g in self.goals],
                "completed_goals": [g.to_dict() for g in self.completed_goals],
                "timestamp": datetime.now().isoformat(),
            }
            
            with open(state_file, 'w') as f:
                json.dump(state_data, f, indent=2, default=str)
            
            logger.debug("Consciousness state saved to %s", state_file)
        except Exception as e:
            logger.warning(f"Failed to save consciousness state: {e}")
    
    def load_state(self, state_file: Optional[str] = None) -> bool:
        """Load consciousness state from file."""
        try:
            if state_file is None:
                state_file = self.config.get("state_file", "database/consciousness_state.json")
            
            import os
            if not os.path.exists(state_file):
                return False
            
            with open(state_file, 'r') as f:
                state_data = json.load(f)
            
            self.process_count = state_data.get("process_count", 0)
            self.success_count = state_data.get("success_count", 0)
            self.error_count = state_data.get("error_count", 0)
            self.awareness_level = state_data.get("awareness_level", 0.5)
            self.curiosity_level = state_data.get("curiosity_level", 0.7)
            self.confidence_base = state_data.get("confidence_base", 0.5)
            
            emotional_state = state_data.get("emotional_state", "CALM")
            self.emotional_state = EmotionalState(emotional_state)
            self.emotional_intensity = state_data.get("emotional_intensity", 0.5)
            self.emotional_stability = state_data.get("emotional_stability", 0.8)
            
            self.metrics = state_data.get("metrics", self.metrics)
            self.growth_stage = GrowthStage(state_data.get("growth_stage", "EMBRYONIC"))
            self.growth_progress = state_data.get("growth_progress", 0.0)
            self.skill_levels = state_data.get("skills", self.skill_levels)
            
            logger.info("Consciousness state loaded from %s", state_file)
            return True
        except Exception as e:
            logger.warning(f"Failed to load consciousness state: {e}")
            return False
    
    def __del__(self):
        """Cleanup on deletion."""
        if self.running:
            self.shutdown()


# ============================================================
# GLOBAL INSTANCE
# ============================================================

consciousness = Consciousness()


# ============================================================
# SHORTCUT FUNCTIONS
# ============================================================

def process(data: Any) -> Dict[str, Any]:
    """Process data through global Consciousness."""
    return consciousness.process(data)


def learn(data: Dict[str, Any]) -> Dict[str, Any]:
    """Learn from data (alias for process)."""
    return consciousness.process(data)


def get_state() -> Dict[str, Any]:
    """Get Consciousness state."""
    return consciousness.get_state()


def status() -> Dict[str, Any]:
    """Get Consciousness status."""
    return consciousness.status()


def snapshot() -> Dict[str, Any]:
    """Get Consciousness snapshot."""
    return consciousness.snapshot()


def start() -> bool:
    """Start Consciousness."""
    return consciousness.start()


def stop() -> bool:
    """Stop Consciousness."""
    return consciousness.stop()


def pause() -> bool:
    """Pause Consciousness."""
    return consciousness.pause()


def resume() -> bool:
    """Resume Consciousness."""
    return consciousness.resume()


def reset() -> bool:
    """Reset Consciousness."""
    return consciousness.reset()


def shutdown() -> bool:
    """Shutdown Consciousness."""
    return consciousness.shutdown()


def feedback(outcome: bool, details: Optional[Dict] = None) -> None:
    """Provide feedback on outcome."""
    return consciousness.feedback(outcome, details)


def get_insights(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent insights."""
    return consciousness.get_insights(limit)


def get_reflections(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent reflections."""
    return consciousness.get_reflections(limit)


def get_experiences(limit: int = 20) -> List[Dict[str, Any]]:
    """Get recent experiences."""
    return consciousness.get_experiences(limit)


def get_patterns(limit: int = 20) -> Dict[str, Dict[str, Any]]:
    """Get patterns."""
    return consciousness.get_patterns(limit)


def get_emotional_state() -> Dict[str, Any]:
    """Get current emotional state."""
    return consciousness.get_emotional_state()


def get_goals() -> List[Dict[str, Any]]:
    """Get all goals."""
    return consciousness.get_goals()


def get_growth_summary() -> Dict[str, Any]:
    """Get growth summary."""
    return consciousness.get_growth_summary()


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    """
    Run comprehensive self-test.
    """
    
    print()
    print("=" * 70)
    print("  CONSCIOUSNESS v4.0 - COMPREHENSIVE SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        test_consciousness = Consciousness()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Process with dict
    print("\n2. Testing process with dict...")
    try:
        test_data = {
            "market": "BTC/USD",
            "signal": "bullish",
            "pattern": "breakout",
            "volume": "high",
            "price": 65000,
            "confidence": 0.85,
            "timeframe": "1h",
            "cycle": 1,
        }
        result = consciousness.process(test_data)
        
        checks = [
            "status" in result,
            "perception" in result,
            "awareness" in result,
            "patterns" in result,
            "emotion" in result,
            "intuition" in result,
            "decision" in result,
            "learning" in result,
            "reflection" in result,
            "metacognition" in result,
        ]
        
        passed = all(checks)
        if passed:
            results["process_dict"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Process with dict test passed")
        else:
            results["process_dict"] = {"status": "FAIL", "failed_checks": [i for i, c in enumerate(checks) if not c]}
            tests_failed += 1
            print("   ❌ Process with dict test failed")
    except Exception as e:
        results["process_dict"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Process with dict test failed: {e}")
    
    # Test 3: Status
    print("\n3. Testing status...")
    try:
        status_result = consciousness.status()
        if status_result and "state" in status_result:
            results["status"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Status test passed")
        else:
            results["status"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Status test failed")
    except Exception as e:
        results["status"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Status test failed: {e}")
    
    # Test 4: Snapshot
    print("\n4. Testing snapshot...")
    try:
        snapshot_result = consciousness.snapshot()
        if snapshot_result and "engine" in snapshot_result:
            results["snapshot"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Snapshot test passed")
        else:
            results["snapshot"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Snapshot test failed")
    except Exception as e:
        results["snapshot"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Snapshot test failed: {e}")
    
    # Test 5: Start/Stop
    print("\n5. Testing start/stop...")
    try:
        consciousness.start()
        if consciousness.running:
            consciousness.stop()
            if not consciousness.running:
                results["start_stop"] = {"status": "PASS"}
                tests_passed += 1
                print("   ✅ Start/Stop test passed")
            else:
                results["start_stop"] = {"status": "FAIL"}
                tests_failed += 1
                print("   ❌ Stop failed")
        else:
            results["start_stop"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Start failed")
    except Exception as e:
        results["start_stop"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Start/Stop test failed: {e}")
    
    # Summary
    print()
    print("=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"  ✅ Passed: {tests_passed}")
    print(f"  ❌ Failed: {tests_failed}")
    print(f"  📊 Total:  {tests_passed + tests_failed}")
    print("=" * 70)
    
    return {
        "module": "consciousness",
        "version": "4.0.0",
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
    print("  CONSCIOUSNESS v4.0 - SELF TEST COMPLETE")
    print("=" * 70)
    print()
    print("Final Status:", result["status"])
    print("Details:", json.dumps(result, indent=2, default=str))


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    # Classes
    "Consciousness",
    "Perception",
    "Awareness",
    "Intuition",
   ]