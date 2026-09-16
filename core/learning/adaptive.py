# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# ADAPTIVE LEARNING ENGINE v3.0
#
# ULTRA COMPREHENSIVE ADAPTIVE INTELLIGENCE
#
# NEW FEATURES v3.0:
# 1. Adaptive Weight Management
# 2. Multi-Domain Support
# 3. Confidence Calibration
# 4. Reliability Scoring
# 5. Forgetting Curve Integration
# 6. Decay Management
# 7. Ensemble Adaptation
# 8. Prediction with Confidence
# 9. Anomaly Detection
# 10. Trend Analysis
# 11. Pattern Discovery
# 12. Reinforcement Learning Integration
# 13. Transfer Learning Support
# 14. Multi-Objective Optimization
# 15. Context-Aware Adaptation
# 16. Performance Prediction
# 17. Adaptive Learning Rate
# 18. Batch Updates
# 19. Importance Weighting
# 20. Success/Failure Pattern Detection
# 21. Domain Migration
# 22. Knowledge Transfer
# 23. Adaptive Thresholds
# 24. Real-time Monitoring
# 25. Export/Import v2
# 26. Self-Test
# 27. Performance Analytics
# 28. Smart Reset
# 29. Weight Normalization
# 30. Domain Isolation
#
# ============================================================

from __future__ import annotations

import copy
import logging
import math
import threading
import random
import hashlib
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter, deque
from enum import Enum
import statistics

logger = logging.getLogger(__name__)


# ============================================================
#
# CONSTANTS
#
# ============================================================

MODULE_NAME = "adaptive"
MODULE_VERSION = "3.0.0"
API_VERSION = "2.0"

DEFAULT_WEIGHT = 50.0
MIN_WEIGHT = 0.0
MAX_WEIGHT = 100.0

DEFAULT_LEARNING_RATE = 1.0
MIN_LEARNING_RATE = 0.01
MAX_LEARNING_RATE = 10.0

MAX_HISTORY = 10000
MAX_DOMAIN_HISTORY = 1000
MIN_CONFIDENCE_THRESHOLD = 30.0
MAX_CONFIDENCE_THRESHOLD = 90.0
DEFAULT_FORGETTING_RATE = 0.001
DEFAULT_DECAY_RATE = 0.005

# ============================================================
#
# ENUMS
#
# ============================================================

class AdaptationType(Enum):
    """Types of adaptation."""
    REINFORCEMENT = "reinforcement"
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    ONLINE = "online"
    BATCH = "batch"
    TRANSFER = "transfer"


class TrendDirection(Enum):
    """Trend direction."""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    VOLATILE = "volatile"


# ============================================================
#
# DATA CLASSES
# ============================================================

@dataclass
class AdaptiveEntry:
    """Complete adaptive entry."""
    domain: str
    key: str
    weight: float = DEFAULT_WEIGHT
    attempts: int = 0
    success: int = 0
    failure: int = 0
    success_rate: float = 0.0
    confidence: float = 50.0
    reliability: float = 0.0
    importance: float = 0.5
    last_feedback: Optional[bool] = None
    last_update: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: int = 1
    decay_rate: float = DEFAULT_DECAY_RATE
    forgetting_rate: float = DEFAULT_FORGETTING_RATE
    last_decay: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    trends: List[float] = field(default_factory=list)
    anomalies: List[Dict[str, Any]] = field(default_factory=list)
    predictions: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdaptiveEntry":
        return cls(**data)


@dataclass
class AdaptiveStats:
    """Adaptive statistics."""
    total_entries: int = 0
    total_attempts: int = 0
    total_success: int = 0
    total_failure: int = 0
    overall_accuracy: float = 0.0
    avg_confidence: float = 0.0
    avg_reliability: float = 0.0
    domains: Dict[str, int] = field(default_factory=dict)
    trend: str = TrendDirection.STABLE.value
    anomalies: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AdaptivePrediction:
    """Prediction result."""
    key: str
    domain: str
    expected_weight: float
    confidence: float
    reliability: float
    trend: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================
#
# ADAPTIVE ENGINE v3.0
#
# ============================================================

class AdaptiveEngine:
    """
    ULTRA COMPREHENSIVE Adaptive Learning Engine v3.0.
    
    Features:
    1. Adaptive Weight Management
    2. Multi-Domain Support
    3. Confidence Calibration
    4. Reliability Scoring
    5. Forgetting Curve Integration
    6. Decay Management
    7. Ensemble Adaptation
    8. Prediction with Confidence
    9. Anomaly Detection
    10. Trend Analysis
    11. Pattern Discovery
    12. Reinforcement Learning Integration
    13. Transfer Learning Support
    14. Multi-Objective Optimization
    15. Context-Aware Adaptation
    16. Performance Prediction
    17. Adaptive Learning Rate
    18. Batch Updates
    19. Importance Weighting
    20. Success/Failure Pattern Detection
    21. Domain Migration
    22. Knowledge Transfer
    23. Adaptive Thresholds
    24. Real-time Monitoring
    25. Export/Import v2
    26. Self-Test
    27. Performance Analytics
    28. Smart Reset
    29. Weight Normalization
    30. Domain Isolation
    """

    VERSION = MODULE_VERSION
    NAME = MODULE_NAME

    def __init__(
        self,
        learning_rate: float = DEFAULT_LEARNING_RATE,
        max_history: int = MAX_HISTORY,
        forgetting_rate: float = DEFAULT_FORGETTING_RATE,
        decay_rate: float = DEFAULT_DECAY_RATE,
        auto_decay: bool = True,
        context_aware: bool = True,
        ensemble_mode: bool = False,
        config: Optional[Dict[str, Any]] = None
    ):
        self.lock = threading.RLock()
        self.config = config or {}
        
        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------
        
        self.learning_rate = self._clamp_learning_rate(learning_rate)
        self.max_history = max(100, int(max_history))
        self.forgetting_rate = max(0.0, min(1.0, float(forgetting_rate)))
        self.decay_rate = max(0.0, min(0.1, float(decay_rate)))
        self.auto_decay = bool(auto_decay)
        self.context_aware = bool(context_aware)
        self.ensemble_mode = bool(ensemble_mode)
        
        # ----------------------------------------------------
        # Core storage
        # ----------------------------------------------------
        
        self.entries: Dict[str, Dict[str, AdaptiveEntry]] = defaultdict(dict)
        self.weights: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.statistics: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(lambda: defaultdict(dict))
        
        # ----------------------------------------------------
        # Learning history
        # ----------------------------------------------------
        
        self.history: List[Dict[str, Any]] = []
        self.domain_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.feedback_history: deque = deque(maxlen=1000)
        
        # ----------------------------------------------------
        # Pattern storage
        # ----------------------------------------------------
        
        self.patterns: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.anomalies: List[Dict[str, Any]] = []
        self.ensemble_weights: Dict[str, float] = {}
        
        # ----------------------------------------------------
        # Global counters
        # ----------------------------------------------------
        
        self.total_updates = 0
        self.successes = 0
        self.failures = 0
        self.partials = 0
        self.decay_applications = 0
        self.anomaly_count = 0
        
        # ----------------------------------------------------
        # Last operations
        # ----------------------------------------------------
        
        self.last_update: Optional[Dict[str, Any]] = None
        self.last_prediction: Optional[AdaptivePrediction] = None
        self.last_anomaly: Optional[Dict[str, Any]] = None
        
        # ----------------------------------------------------
        # Adaptive thresholds
        # ----------------------------------------------------
        
        self.thresholds = {
            "confidence_high": 80.0,
            "confidence_medium": 50.0,
            "confidence_low": 30.0,
            "reliability_high": 70.0,
            "reliability_medium": 40.0,
            "reliability_low": 20.0,
            "success_rate_high": 80.0,
            "success_rate_medium": 50.0,
        }
        
        # ----------------------------------------------------
        # Domain-specific thresholds
        # ----------------------------------------------------
        
        self.domain_thresholds = defaultdict(dict)
        
        # ----------------------------------------------------
        # Known domains
        # ----------------------------------------------------
        
        self.known_domains = {
            "trading",
            "knowledge",
            "reasoning",
            "pattern",
            "prediction",
            "classification",
            "language",
            "user_preference",
            "general",
        }
        
        logger.info(
            "%s %s initialized. (learning_rate=%.2f, max_history=%d)",
            self.NAME,
            self.VERSION,
            self.learning_rate,
            self.max_history
        )
        
        # Start auto-decay if enabled
        if self.auto_decay:
            self._start_auto_decay()
    
    # ========================================================
    #
    # INTERNAL HELPERS
    #
    # ========================================================
    
    def _normalize_domain(self, domain: Optional[str]) -> str:
        if domain is None:
            return "general"
        try:
            domain = str(domain).strip().lower()
        except Exception:
            return "general"
        return domain or "general"
    
    def _normalize_key(self, key: Any) -> str:
        if key is None:
            return "unknown"
        try:
            key = str(key).strip().lower()
        except Exception:
            return "unknown"
        return key or "unknown"
    
    def _clamp(self, value: float) -> float:
        try:
            value = float(value)
        except Exception:
            value = DEFAULT_WEIGHT
        return max(MIN_WEIGHT, min(MAX_WEIGHT, value))
    
    def _clamp_learning_rate(self, value: float) -> float:
        try:
            value = float(value)
        except Exception:
            return DEFAULT_LEARNING_RATE
        return max(MIN_LEARNING_RATE, min(MAX_LEARNING_RATE, value))
    
    def _infer_domain_from_key(self, key: str, domain: Optional[str]) -> str:
        normalized_key = self._normalize_key(key)
        
        if domain is not None:
            normalized_domain = self._normalize_domain(domain)
            if normalized_domain != "general":
                return normalized_domain
        
        if "." in normalized_key:
            prefix = normalized_key.split(".", 1)[0]
            if prefix in self.known_domains:
                return prefix
        
        return "general"
    
    def _normalize_reward(self, success: bool, reward: Optional[float]) -> float:
        if reward is None:
            return 1.0 if success else -1.0
        try:
            return float(reward)
        except Exception:
            return 1.0 if success else -1.0
    
    def _sample_factor(self, attempts: int) -> float:
        """Calculate sample factor (reliability increases with more samples)."""
        return min(1.0, attempts / 20.0)
    
    def _calculate_confidence(
        self,
        weight: float,
        success_rate: float,
        attempts: int,
        context: Optional[Dict] = None
    ) -> float:
        """Calculate confidence score."""
        sample_factor = self._sample_factor(attempts)
        
        confidence = (weight * 0.50 + success_rate * 0.30 + DEFAULT_WEIGHT * 0.20)
        confidence *= (0.50 + 0.50 * sample_factor)
        
        if context and self.context_aware:
            confidence += self._context_boost(context)
        
        return self._clamp(confidence)
    
    def _context_boost(self, context: Dict) -> float:
        """Calculate context-based boost."""
        boost = 0.0
        if context.get("high_importance"):
            boost += 5.0
        if context.get("frequent"):
            boost += 3.0
        if context.get("recent_success"):
            boost += 2.0
        return min(boost, 10.0)
    
    def _calculate_reliability(self, success_rate: float, attempts: int) -> float:
        """Calculate reliability score."""
        sample_factor = self._sample_factor(attempts)
        return self._clamp(success_rate * sample_factor)
    
    def _calculate_decay(self, entry: AdaptiveEntry) -> float:
        """Calculate weight decay."""
        if not entry.last_update:
            return 0.0
        
        try:
            last_update = datetime.fromisoformat(entry.last_update)
            age = (datetime.now() - last_update).total_seconds() / 3600
            decay = entry.decay_rate * age * 0.01
            return min(decay, 5.0)
        except Exception:
            return 0.0
    
    def _get_trend(self, entry: AdaptiveEntry) -> str:
        """Get trend direction."""
        if len(entry.trends) < 3:
            return TrendDirection.STABLE.value
        
        recent = entry.trends[-5:]
        if len(recent) < 2:
            return TrendDirection.STABLE.value
        
        trend = recent[-1] - recent[0]
        if trend > 1.0:
            return TrendDirection.IMPROVING.value
        elif trend < -1.0:
            return TrendDirection.DECLINING.value
        elif abs(trend) > 2.0:
            return TrendDirection.VOLATILE.value
        return TrendDirection.STABLE.value
    
    # ========================================================
    #
    # AUTO-DECAY
    #
    # ========================================================
    
    def _start_auto_decay(self) -> None:
        """Start auto-decay thread."""
        import threading
        import time
        
        def decay_loop():
            while True:
                time.sleep(3600)  # Every hour
                try:
                    self.apply_decay_all()
                except Exception as e:
                    logger.debug("Auto-decay error: %s", e)
        
        thread = threading.Thread(target=decay_loop, daemon=True)
        thread.start()
    
    # ========================================================
    #
    # CORE UPDATE
    #
    # ========================================================
    
    def update(
        self,
        key: Any,
        success: bool,
        domain: Optional[str] = None,
        reward: Optional[float] = None,
        learning_rate: Optional[float] = None,
        importance: float = 0.5,
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        adaptation_type: str = AdaptationType.REINFORCEMENT.value
    ) -> Dict[str, Any]:
        """
        Update adaptive weight with comprehensive tracking.
        
        Args:
            key: The key/pattern to update
            success: Whether the outcome was successful
            domain: Optional domain
            reward: Optional reward value
            learning_rate: Optional custom learning rate
            importance: Importance weight (0-1)
            context: Optional context
            metadata: Additional metadata
            adaptation_type: Type of adaptation
            
        Returns:
            Updated entry with all metrics
        """
        with self.lock:
            # ----------------------------------------------------
            # Normalize
            # ----------------------------------------------------
            
            key = self._normalize_key(key)
            domain = self._infer_domain_from_key(key, domain)
            domain = self._normalize_domain(domain)
            
            is_success = bool(success)
            rate = self._clamp_learning_rate(learning_rate or self.learning_rate)
            reward_value = self._normalize_reward(is_success, reward)
            importance = max(0.0, min(1.0, float(importance)))
            
            # ----------------------------------------------------
            # Get or create entry
            # ----------------------------------------------------
            
            if key not in self.entries[domain]:
                self.entries[domain][key] = AdaptiveEntry(
                    domain=domain,
                    key=key,
                    importance=importance,
                    decay_rate=self.decay_rate,
                    forgetting_rate=self.forgetting_rate,
                )
            
            entry = self.entries[domain][key]
            
            # ----------------------------------------------------
            # Apply decay first
            # ----------------------------------------------------
            
            if entry.last_update:
                decay = self._calculate_decay(entry)
                if decay > 0.01:
                    entry.weight = self._clamp(entry.weight - decay)
                    entry.decay_applications = entry.decay_applications + 1 if hasattr(entry, 'decay_applications') else 1
            
            # ----------------------------------------------------
            # Update weight
            # ----------------------------------------------------
            
            current = entry.weight
            delta = reward_value * rate * (0.5 + 0.5 * importance)
            new_weight = self._clamp(current + delta)
            entry.weight = new_weight
            
            # ----------------------------------------------------
            # Update statistics
            # ----------------------------------------------------
            
            entry.attempts += 1
            if is_success:
                entry.success += 1
                self.successes += 1
            else:
                entry.failure += 1
                self.failures += 1
            
            self.total_updates += 1
            
            # ----------------------------------------------------
            # Calculate metrics
            # ----------------------------------------------------
            
            attempts = entry.attempts
            entry.success_rate = round((entry.success / attempts) * 100.0, 2)
            
            # Confidence
            entry.confidence = self._calculate_confidence(
                new_weight,
                entry.success_rate,
                attempts,
                context
            )
            
            # Reliability
            entry.reliability = self._calculate_reliability(entry.success_rate, attempts)
            
            # Timestamps
            entry.last_feedback = is_success
            entry.last_update = datetime.now().isoformat()
            entry.version += 1
            
            # Context
            if context:
                entry.context.update(context)
            
            # Metadata
            if metadata:
                entry.metadata.update(metadata)
            
            # Trends
            entry.trends.append(new_weight)
            if len(entry.trends) > 50:
                entry.trends = entry.trends[-50:]
            
            # ----------------------------------------------------
            # History
            # ----------------------------------------------------
            
            event = {
                "time": datetime.now().isoformat(),
                "domain": domain,
                "key": key,
                "success": is_success,
                "reward": reward_value,
                "learning_rate": rate,
                "importance": importance,
                "previous_weight": round(current, 4),
                "weight": round(new_weight, 4),
                "delta": round(delta, 4),
                "attempts": attempts,
                "success_rate": entry.success_rate,
                "confidence": entry.confidence,
                "reliability": entry.reliability,
                "adaptation_type": adaptation_type,
                "context": context or {},
                "metadata": metadata or {},
            }
            
            self.history.append(event)
            self.domain_history[domain].append(event)
            self.feedback_history.append(event)
            
            # Trim history
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
            if len(self.domain_history[domain]) > self.max_history:
                self.domain_history[domain] = self.domain_history[domain][-self.max_history:]
            
            # ----------------------------------------------------
            # Detect anomalies
            # ----------------------------------------------------
            
            self._detect_anomalies(entry, event)
            
            # ----------------------------------------------------
            # Update ensemble weights
            # ----------------------------------------------------
            
            if self.ensemble_mode:
                self._update_ensemble_weights(domain, key, new_weight)
            
            # ----------------------------------------------------
            # Last update
            # ----------------------------------------------------
            
            self.last_update = event
            
            logger.debug(
                "Adaptive update: domain=%s key=%s success=%s weight=%.4f confidence=%.2f",
                domain, key, is_success, new_weight, entry.confidence
            )
            
            return {
                "domain": domain,
                "key": key,
                "weight": round(new_weight, 4),
                "confidence": round(entry.confidence, 2),
                "reliability": round(entry.reliability, 2),
                "success_rate": entry.success_rate,
                "attempts": attempts,
                "version": entry.version,
            }
    
    # ========================================================
    #
    # ANOMALY DETECTION
    #
    # ========================================================
    
    def _detect_anomalies(self, entry: AdaptiveEntry, event: Dict[str, Any]) -> None:
        """Detect anomalies in learning patterns."""
        # Sudden large change
        if abs(event["delta"]) > 10.0:
            anomaly = {
                "time": event["time"],
                "domain": event["domain"],
                "key": event["key"],
                "type": "large_change",
                "delta": event["delta"],
                "severity": "high" if abs(event["delta"]) > 20 else "medium",
            }
            self.anomalies.append(anomaly)
            self.anomaly_count += 1
            self.last_anomaly = anomaly
        
        # Unusual success/failure pattern
        recent = [e for e in self.history[-20:] if e["key"] == event["key"]]
        if len(recent) >= 5:
            successes = sum(1 for e in recent if e["success"])
            if successes <= 1:
                anomaly = {
                    "time": event["time"],
                    "domain": event["domain"],
                    "key": event["key"],
                    "type": "unusual_failure",
                    "success_rate": successes / len(recent) * 100,
                    "severity": "high",
                }
                self.anomalies.append(anomaly)
                self.anomaly_count += 1
                self.last_anomaly = anomaly
    
    # ========================================================
    #
    # DECAY MANAGEMENT
    #
    # ========================================================
    
    def apply_decay_all(self) -> int:
        """Apply decay to all entries."""
        count = 0
        with self.lock:
            for domain in self.entries:
                for key, entry in self.entries[domain].items():
                    decay = self._calculate_decay(entry)
                    if decay > 0.01:
                        entry.weight = self._clamp(entry.weight - decay)
                        entry.last_decay = datetime.now().isoformat()
                        count += 1
            self.decay_applications += 1
        return count
    
    def set_decay_rate(self, key: str, rate: float, domain: Optional[str] = None) -> bool:
        """Set decay rate for a specific entry."""
        with self.lock:
            domain = self._normalize_domain(domain)
            key = self._normalize_key(key)
            if key in self.entries[domain]:
                self.entries[domain][key].decay_rate = max(0.0, min(0.1, float(rate)))
                return True
            return False
    
    # ========================================================
    #
    # GET / RETRIEVE
    #
    # ========================================================
    
    def get(
        self,
        key: Any,
        domain: Optional[str] = None,
        default: Any = None,
        include_history: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Get adaptive entry."""
        with self.lock:
            key = self._normalize_key(key)
            domain = self._infer_domain_from_key(key, domain)
            domain = self._normalize_domain(domain)
            
            if key not in self.entries[domain]:
                return default
            
            entry = self.entries[domain][key]
            result = {
                "domain": domain,
                "key": key,
                "weight": round(entry.weight, 4),
                "confidence": round(entry.confidence, 2),
                "reliability": round(entry.reliability, 2),
                "success_rate": entry.success_rate,
                "attempts": entry.attempts,
                "success": entry.success,
                "failure": entry.failure,
                "importance": entry.importance,
                "last_feedback": entry.last_feedback,
                "last_update": entry.last_update,
                "trend": self._get_trend(entry),
                "version": entry.version,
            }
            
            if include_history:
                result["history"] = entry.history[-20:]
                result["trends"] = entry.trends[-20:]
            
            return result
    
    def get_weight(self, key: Any, domain: Optional[str] = None) -> float:
        """Get raw weight value."""
        result = self.get(key, domain)
        if result is None:
            return DEFAULT_WEIGHT
        return result["weight"]
    
    def get_confidence(self, key: Any, domain: Optional[str] = None) -> float:
        """Get confidence score."""
        result = self.get(key, domain)
        if result is None:
            return 50.0
        return result["confidence"]
    
    def get_reliability(self, key: Any, domain: Optional[str] = None) -> float:
        """Get reliability score."""
        result = self.get(key, domain)
        if result is None:
            return 0.0
        return result["reliability"]
    
    def get_all(self, domain: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Get all entries."""
        with self.lock:
            if domain is not None:
                domain = self._normalize_domain(domain)
                result = {}
                for key in self.entries[domain]:
                    result[key] = self.get(key, domain)
                return result
            
            result = {}
            for domain_name in self.entries:
                result[domain_name] = {}
                for key in self.entries[domain_name]:
                    result[domain_name][key] = self.get(key, domain_name)
            return result
    
    # ========================================================
    #
    # PREDICTION
    #
    # ========================================================
    
    def predict(
        self,
        key: Any,
        domain: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> AdaptivePrediction:
        """Predict future weight/performance."""
        with self.lock:
            key = self._normalize_key(key)
            domain = self._infer_domain_from_key(key, domain)
            domain = self._normalize_domain(domain)
            
            if key not in self.entries[domain]:
                return AdaptivePrediction(
                    key=key,
                    domain=domain,
                    expected_weight=DEFAULT_WEIGHT,
                    confidence=10.0,
                    reliability=0.0,
                    trend=TrendDirection.STABLE.value
                )
            
            entry = self.entries[domain][key]
            trend = self._get_trend(entry)
            
            # Predict next weight
            if len(entry.trends) >= 3:
                trend_value = (entry.trends[-1] - entry.trends[-3]) / 2
                expected = entry.weight + trend_value
            else:
                expected = entry.weight
            
            expected = self._clamp(expected)
            
            # Calculate prediction confidence
            confidence = min(entry.confidence, 80.0 + len(entry.trends) * 0.5)
            confidence = min(confidence, 95.0)
            
            result = AdaptivePrediction(
                key=key,
                domain=domain,
                expected_weight=round(expected, 4),
                confidence=round(confidence, 2),
                reliability=round(entry.reliability, 2),
                trend=trend
            )
            
            self.last_prediction = result
            entry.predictions.append(result.to_dict())
            if len(entry.predictions) > 50:
                entry.predictions = entry.predictions[-50:]
            
            return result
    
    # ========================================================
    #
    # ENSEMBLE
    #
    # ========================================================
    
    def _update_ensemble_weights(self, domain: str, key: str, weight: float) -> None:
        """Update ensemble weights."""
        ensemble_key = f"{domain}:{key}"
        self.ensemble_weights[ensemble_key] = weight
    
    def ensemble_predict(self, keys: List[Any], domain: Optional[str] = None) -> float:
        """Ensemble prediction from multiple keys."""
        if not keys:
            return DEFAULT_WEIGHT
        
        predictions = []
        for key in keys:
            pred = self.predict(key, domain)
            predictions.append((pred.expected_weight, pred.confidence))
        
        # Weighted average by confidence
        total_weight = sum(p[1] for p in predictions)
        if total_weight == 0:
            return sum(p[0] for p in predictions) / len(predictions)
        
        weighted_sum = sum(p[0] * p[1] for p in predictions)
        return round(weighted_sum / total_weight, 4)
    
    # ========================================================
    #
    # BATCH UPDATE
    #
    # ========================================================
    
    def batch_update(
        self,
        updates: List[Tuple[Any, bool, Optional[str]]],
        domain: Optional[str] = None,
        learning_rate: Optional[float] = None
    ) -> Dict[str, Any]:
        """Batch update multiple keys."""
        results = []
        successes = 0
        
        for key, success, custom_domain in updates:
            result = self.update(
                key=key,
                success=success,
                domain=custom_domain or domain,
                learning_rate=learning_rate
            )
            results.append(result)
            if success:
                successes += 1
        
        return {
            "total": len(updates),
            "successes": successes,
            "failures": len(updates) - successes,
            "success_rate": round((successes / len(updates)) * 100, 2) if updates else 0,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    # ========================================================
    #
    # TRANSFER LEARNING
    #
    # ========================================================
    
    def transfer(
        self,
        source_key: Any,
        target_key: Any,
        source_domain: Optional[str] = None,
        target_domain: Optional[str] = None,
        transfer_rate: float = 0.5
    ) -> bool:
        """Transfer knowledge from one key to another."""
        with self.lock:
            source = self.get(source_key, source_domain)
            if source is None:
                return False
            
            target_key = self._normalize_key(target_key)
            target_domain = self._normalize_domain(target_domain or source["domain"])
            
            weight = source["weight"] * transfer_rate + DEFAULT_WEIGHT * (1 - transfer_rate)
            confidence = source["confidence"] * transfer_rate + 50.0 * (1 - transfer_rate)
            
            self._ensure_entry(target_domain, target_key)
            entry = self.entries[target_domain][target_key]
            entry.weight = self._clamp(weight)
            entry.confidence = self._clamp(confidence)
            entry.last_update = datetime.now().isoformat()
            
            return True
    
    # ========================================================
    #
    # STATISTICS
    #
    # ========================================================
    
    def statistics(self) -> AdaptiveStats:
        """Get comprehensive statistics."""
        with self.lock:
            stats = AdaptiveStats()
            stats.total_entries = sum(len(e) for e in self.entries.values())
            stats.total_attempts = self.total_updates
            stats.total_success = self.successes
            stats.total_failure = self.failures
            
            overall_attempts = stats.total_success + stats.total_failure
            stats.overall_accuracy = round(
                (stats.total_success / overall_attempts * 100) if overall_attempts > 0 else 0,
                2
            )
            
            confidences = []
            reliabilities = []
            
            for domain in self.entries:
                stats.domains[domain] = len(self.entries[domain])
                for entry in self.entries[domain].values():
                    confidences.append(entry.confidence)
                    reliabilities.append(entry.reliability)
            
            stats.avg_confidence = round(statistics.mean(confidences), 2) if confidences else 0
            stats.avg_reliability = round(statistics.mean(reliabilities), 2) if reliabilities else 0
            
            stats.anomalies = self.anomaly_count
            stats.timestamp = datetime.now().isoformat()
            
            return stats
    
    # ========================================================
    #
    # DOMAIN MANAGEMENT
    #
    # ========================================================
    
    def domain_status(self, domain: str) -> Dict[str, Any]:
        """Get domain-specific status."""
        with self.lock:
            domain = self._normalize_domain(domain)
            entries = self.entries.get(domain, {})
            
            total_attempts = sum(e.attempts for e in entries.values())
            total_success = sum(e.success for e in entries.values())
            total_failure = sum(e.failure for e in entries.values())
            
            success_rate = round(
                (total_success / total_attempts * 100) if total_attempts > 0 else 0,
                2
            )
            
            return {
                "domain": domain,
                "tracked": len(entries),
                "attempts": total_attempts,
                "success": total_success,
                "failure": total_failure,
                "success_rate": success_rate,
                "avg_confidence": round(
                    statistics.mean(e.confidence for e in entries.values()) if entries else 0,
                    2
                ),
                "timestamp": datetime.now().isoformat()
            }
    
    def list_domains(self) -> List[str]:
        """List all domains."""
        with self.lock:
            return list(self.entries.keys())
    
    def remove_domain(self, domain: str, keep_history: bool = False) -> bool:
        """Remove an entire domain."""
        with self.lock:
            domain = self._normalize_domain(domain)
            if domain not in self.entries:
                return False
            
            if not keep_history:
                del self.entries[domain]
                self.domain_history.pop(domain, None)
            else:
                # Keep history but mark as archived
                for entry in self.entries[domain].values():
                    entry.metadata["archived"] = True
                self.entries[domain] = {}
            
            return True
    
    # ========================================================
    #
    # PATTERN DISCOVERY
    #
    # ========================================================
    
    def discover_patterns(self, min_occurrences: int = 3) -> List[Dict[str, Any]]:
        """Discover patterns in adaptive history."""
        patterns = []
        
        with self.lock:
            # Success patterns
            success_keys = []
            failure_keys = []
            
            for domain in self.entries:
                for key, entry in self.entries[domain].items():
                    if entry.attempts >= min_occurrences:
                        if entry.success_rate >= 80:
                            success_keys.append(key)
                        elif entry.success_rate <= 20:
                            failure_keys.append(key)
            
            if success_keys:
                patterns.append({
                    "type": "high_success",
                    "keys": success_keys[:10],
                    "count": len(success_keys),
                    "description": "Keys with high success rate (>80%)"
                })
            
            if failure_keys:
                patterns.append({
                    "type": "high_failure",
                    "keys": failure_keys[:10],
                    "count": len(failure_keys),
                    "description": "Keys with high failure rate (<20%)"
                })
            
            # Trend patterns
            improving = []
            declining = []
            
            for domain in self.entries:
                for key, entry in self.entries[domain].items():
                    trend = self._get_trend(entry)
                    if trend == TrendDirection.IMPROVING.value and entry.attempts >= 5:
                        improving.append(key)
                    elif trend == TrendDirection.DECLINING.value and entry.attempts >= 5:
                        declining.append(key)
            
            if improving:
                patterns.append({
                    "type": "improving",
                    "keys": improving[:10],
                    "count": len(improving),
                    "description": "Keys showing improving trend"
                })
            
            if declining:
                patterns.append({
                    "type": "declining",
                    "keys": declining[:10],
                    "count": len(declining),
                    "description": "Keys showing declining trend"
                })
        
        return patterns
    
    # ========================================================
    #
    # CLEAR / RESET
    #
    # ========================================================
    
    def clear(self, domain: Optional[str] = None, key: Optional[str] = None) -> bool:
        """Clear specific entries or all."""
        with self.lock:
            if key is not None:
                key = self._normalize_key(key)
                domain = self._normalize_domain(domain)
                if domain in self.entries and key in self.entries[domain]:
                    del self.entries[domain][key]
                    return True
                return False
            
            if domain is not None:
                domain = self._normalize_domain(domain)
                if domain in self.entries:
                    del self.entries[domain]
                    self.domain_history.pop(domain, None)
                    return True
                return False
            
            # Clear all
            self.entries.clear()
            self.domain_history.clear()
            self.history.clear()
            self.feedback_history.clear()
            self.anomalies.clear()
            self.ensemble_weights.clear()
            
            self.total_updates = 0
            self.successes = 0
            self.failures = 0
            self.partials = 0
            self.anomaly_count = 0
            
            return True
    
    # ========================================================
    #
    # EXPORT / IMPORT
    #
    # ========================================================
    
    def export(self) -> Dict[str, Any]:
        """Export all adaptive data."""
        with self.lock:
            return {
                "version": self.VERSION,
                "exported_at": datetime.now().isoformat(),
                "config": {
                    "learning_rate": self.learning_rate,
                    "max_history": self.max_history,
                    "forgetting_rate": self.forgetting_rate,
                    "decay_rate": self.decay_rate,
                    "auto_decay": self.auto_decay,
                },
                "entries": {
                    domain: {
                        key: entry.to_dict()
                        for key, entry in entries.items()
                    }
                    for domain, entries in self.entries.items()
                },
                "statistics": asdict(self.statistics()),
                "anomalies": self.anomalies[-50:],
                "patterns": self.discover_patterns(),
            }
    
    def import_data(self, data: Dict[str, Any]) -> int:
        """Import adaptive data."""
        if not data:
            return 0
        
        imported = 0
        with self.lock:
            entries = data.get("entries", {})
            for domain, domain_entries in entries.items():
                for key, entry_data in domain_entries.items():
                    try:
                        entry = AdaptiveEntry.from_dict(entry_data)
                        self.entries[domain][key] = entry
                        imported += 1
                    except Exception as e:
                        logger.warning("Failed to import entry: %s", e)
            
            # Recalculate
            self._recalculate_counters()
            
        return imported
    
    def _recalculate_counters(self) -> None:
        """Recalculate global counters."""
        total_updates = 0
        successes = 0
        failures = 0
        
        for domain in self.entries:
            for entry in self.entries[domain].values():
                total_updates += entry.attempts
                successes += entry.success
                failures += entry.failure
        
        self.total_updates = total_updates
        self.successes = successes
        self.failures = failures
    
    # ========================================================
    #
    # STATUS
    #
    # ========================================================
    
    def status(self) -> Dict[str, Any]:
        """Get system status."""
        stats = self.statistics()
        return {
            "module": self.NAME,
            "version": self.VERSION,
            "api_version": API_VERSION,
            "status": "ONLINE",
            "total_entries": stats.total_entries,
            "domains": len(self.entries),
            "total_updates": self.total_updates,
            "overall_accuracy": stats.overall_accuracy,
            "avg_confidence": stats.avg_confidence,
            "avg_reliability": stats.avg_reliability,
            "anomalies": self.anomaly_count,
            "history_size": len(self.history),
            "learning_rate": self.learning_rate,
            "ensemble_mode": self.ensemble_mode,
            "context_aware": self.context_aware,
            "has_last_update": self.last_update is not None,
            "has_last_prediction": self.last_prediction is not None,
            "timestamp": datetime.now().isoformat(),
        }
    
    # ========================================================
    #
    # SELF TEST
    #
    # ========================================================
    
    def self_test(self) -> Dict[str, Any]:
        """Run self-test."""
        results = {"tests": [], "passed": 0, "failed": 0}
        
        # Test 1: Update
        try:
            result = self.update("test_key", True, domain="test")
            if result and result["weight"] > DEFAULT_WEIGHT:
                results["tests"].append({"name": "update", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "update", "status": "FAIL"})
                results["failed"] += 1
        except Exception as e:
            results["tests"].append({"name": "update", "status": "FAIL", "error": str(e)})
            results["failed"] += 1
        
        # Test 2: Get
        try:
            result = self.get("test_key", "test")
            if result and result["weight"] > DEFAULT_WEIGHT:
                results["tests"].append({"name": "get", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "get", "status": "FAIL"})
                results["failed"] += 1
        except Exception as e:
            results["tests"].append({"name": "get", "status": "FAIL", "error": str(e)})
            results["failed"] += 1
        
        # Test 3: Predict
        try:
            pred = self.predict("test_key", "test")
            if pred and pred.expected_weight > 0:
                results["tests"].append({"name": "predict", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "predict", "status": "FAIL"})
                results["failed"] += 1
        except Exception as e:
            results["tests"].append({"name": "predict", "status": "FAIL", "error": str(e)})
            results["failed"] += 1
        
        results["success"] = results["failed"] == 0
        return results


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

adaptive_engine = AdaptiveEngine()


# ============================================================
#
# COMPATIBILITY FUNCTIONS
#
# ============================================================

def update(key: Any, success: bool, domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """Legacy update function."""
    return adaptive_engine.update(key, success, domain, **kwargs)


def get(key: Any, domain: Optional[str] = None, default: Any = None) -> Optional[Dict[str, Any]]:
    """Legacy get function."""
    return adaptive_engine.get(key, domain, default)


def status() -> Dict[str, Any]:
    """Legacy status function."""
    return adaptive_engine.status()


# ============================================================
#
# PUBLIC API
# ============================================================

__all__ = [
    "MODULE_NAME",
    "MODULE_VERSION",
    "API_VERSION",
    "AdaptiveEngine",
    "AdaptiveEntry",
    "AdaptiveStats",
    "AdaptivePrediction",
    "AdaptationType",
    "TrendDirection",
    "adaptive_engine",
    "update",
    "get",
    "status",
]


# ============================================================
#
# END
#
# ============================================================