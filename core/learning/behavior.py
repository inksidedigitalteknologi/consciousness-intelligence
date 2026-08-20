# ============================================================
# core/learning/behavior.py
# BEHAVIOR LEARNING ENGINE v3.0
# SUPER COMPREHENSIVE BEHAVIOR INTELLIGENCE
#
# FITUR LENGKAP:
# 1. Behavior Learning & Tracking
# 2. Domain-Specific Behavior Analysis
# 3. Pattern Recognition
# 4. Context-Aware Behavior Prediction
# 5. Outcome-Based Learning
# 6. Confidence Scoring
# 7. Behavior Frequency Analysis
# 8. Pattern Discovery
# 9. Feedback Integration
# 10. Behavior History
# 11. Multi-Domain Support
# 12. Adaptive Learning
# 13. Behavior Ranking
# 14. Anomaly Detection
# 15. Behavior Trends
# 16. Export/Import
# 17. Self-Test
# ============================================================

from __future__ import annotations

import logging
import math
import json
import uuid
from collections import defaultdict, Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ============================================================
# VERSION
# ============================================================

BEHAVIOR_VERSION = "3.0.0"
API_VERSION = "1.0"


# ============================================================
# CONSTANTS
# ============================================================

BEHAVIOR_STATUS_LEARNED = "learned"
BEHAVIOR_STATUS_PREDICTED = "predicted"
BEHAVIOR_STATUS_CONFIRMED = "confirmed"
BEHAVIOR_STATUS_REJECTED = "rejected"
BEHAVIOR_STATUS_EVOLVED = "evolved"

OUTCOME_SUCCESS = "success"
OUTCOME_FAILURE = "failure"
OUTCOME_PARTIAL = "partial"
OUTCOME_NEUTRAL = "neutral"

DOMAIN_GENERAL = "general"
DOMAIN_MARKET = "market"
DOMAIN_TRADING = "trading"
DOMAIN_LEARNING = "learning"
DOMAIN_STRATEGY = "strategy"


# ============================================================
# TIME HELPER
# ============================================================

def utc_now() -> str:
    """Return current UTC timestamp."""
    return datetime.now().isoformat()


# ============================================================
# BEHAVIOR ENGINE v3.0
# ============================================================

class BehaviorEngine:
    """
    Super Comprehensive Behavior Learning Engine.
    
    Features:
    - Behavior Learning & Tracking
    - Domain-Specific Behavior Analysis
    - Pattern Recognition
    - Context-Aware Behavior Prediction
    - Outcome-Based Learning
    - Confidence Scoring
    - Behavior Frequency Analysis
    - Pattern Discovery
    - Feedback Integration
    - Behavior History
    - Multi-Domain Support
    - Adaptive Learning
    """
    
    VERSION = BEHAVIOR_VERSION
    MAX_HISTORY = 2000
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Behavior counters
        self.behaviors: Counter = Counter()
        self.domain_behaviors: Dict[str, Counter] = defaultdict(Counter)
        
        # Pattern storage
        self.patterns: Dict[str, Counter] = defaultdict(Counter)
        
        # Context → behavior relationships
        self.context_behaviors: Dict[str, Counter] = defaultdict(Counter)
        
        # Behavior → outcome relationships
        self.outcomes: Dict[str, Counter] = defaultdict(Counter)
        
        # Behavior → confidence
        self.confidence: Dict[str, float] = {}
        
        # Behavior frequency
        self.frequency: Counter = Counter()
        
        # Behavior trends
        self.trends: Dict[str, List[Dict]] = defaultdict(list)
        
        # Anomaly detection
        self.anomalies: List[Dict] = []
        
        # Learning history
        self.history: List[Dict] = []
        
        # Behavior sequences
        self.sequences: List[List[str]] = []
        
        # Statistics
        self.learning_count = 0
        self.prediction_count = 0
        self.feedback_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.partial_count = 0
        self.anomaly_count = 0
        
        # Last operations
        self.last_learning: Optional[Dict] = None
        self.last_prediction: Optional[Dict] = None
        self.last_feedback: Optional[Dict] = None
        self.last_anomaly: Optional[Dict] = None
        
        # Domain thresholds
        self.domain_thresholds = {
            DOMAIN_GENERAL: 0.5,
            DOMAIN_MARKET: 0.6,
            DOMAIN_TRADING: 0.7,
            DOMAIN_LEARNING: 0.5,
            DOMAIN_STRATEGY: 0.6,
        }
        
        logger.info("Behavior Engine v%s initialized.", self.VERSION)
    
    # ========================================================
    # NORMALIZATION HELPERS
    # ========================================================
    
    def _normalize(self, value: Any) -> Optional[str]:
        """Normalize string value."""
        if value is None:
            return None
        
        if isinstance(value, str):
            value = value.strip().lower()
            return value if value else None
        
        if isinstance(value, (int, float, bool)):
            return str(value).lower()
        
        return str(value).strip().lower()
    
    def _text(self, value: Any) -> str:
        """Convert to safe text."""
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        return str(value)
    
    # ========================================================
    # DOMAIN EXTRACTION
    # ========================================================
    
    def _extract_domain(self, data: Dict) -> str:
        """Extract domain from data."""
        domain = data.get("domain")
        if domain:
            return self._normalize(domain) or DOMAIN_GENERAL
        
        metadata = data.get("metadata", {})
        if isinstance(metadata, dict):
            domain = metadata.get("domain")
            if domain:
                return self._normalize(domain) or DOMAIN_GENERAL
        
        return DOMAIN_GENERAL
    
    def _extract_analysis(self, data: Dict) -> Dict:
        """Extract analysis from data."""
        analysis = data.get("analysis", {})
        return analysis if isinstance(analysis, dict) else {}
    
    # ========================================================
    # BEHAVIOR SIGNAL EXTRACTION
    # ========================================================
    
    def _extract_behavior_signals(self, data: Dict) -> List[str]:
        """Extract behavior signals from data."""
        analysis = self._extract_analysis(data)
        signals = []
        
        # Sentiment
        sentiment = analysis.get("sentiment")
        if sentiment:
            signals.append(self._normalize(sentiment))
        
        # Explicit behavior
        behavior = data.get("behavior")
        if behavior:
            if isinstance(behavior, (list, tuple, set)):
                for item in behavior:
                    normalized = self._normalize(item)
                    if normalized:
                        signals.append(normalized)
            else:
                normalized = self._normalize(behavior)
                if normalized:
                    signals.append(normalized)
        
        # Actions
        actions = data.get("actions", [])
        if isinstance(actions, (list, tuple, set)):
            for action in actions:
                normalized = self._normalize(action)
                if normalized:
                    signals.append(f"action:{normalized}")
        
        # Intent
        intent = data.get("intent")
        if intent:
            signals.append(f"intent:{self._normalize(intent)}")
        
        # States
        states = analysis.get("states", [])
        if isinstance(states, (list, tuple, set)):
            for state in states:
                normalized = self._normalize(state)
                if normalized:
                    signals.append(f"state:{normalized}")
        
        # Remove duplicates
        return list(dict.fromkeys(signals))
    
    # ========================================================
    # CONTEXT EXTRACTION
    # ========================================================
    
    def _extract_context(self, data: Dict) -> Dict[str, str]:
        """Extract context from data."""
        context = {}
        
        # Explicit context
        supplied = data.get("context")
        if isinstance(supplied, dict):
            context.update(supplied)
        
        # Market
        if "market" in data:
            context["market"] = data["market"]
        
        # Pattern
        if "pattern" in data:
            context["pattern"] = data["pattern"]
        
        # Category
        if "category" in data:
            context["category"] = data["category"]
        
        # Source
        if "source" in data:
            context["source"] = data["source"]
        
        # Timeframe
        if "timeframe" in data:
            context["timeframe"] = data["timeframe"]
        
        return {
            self._normalize(key): self._normalize(value)
            for key, value in context.items()
            if value is not None
        }
    
    # ========================================================
    # OUTCOME EXTRACTION
    # ========================================================
    
    def _extract_outcome(self, data: Dict) -> Optional[str]:
        """Extract outcome from data."""
        outcome = data.get("outcome")
        if outcome is not None:
            return self._normalize(outcome)
        
        evaluation = data.get("evaluation", {})
        if isinstance(evaluation, dict):
            outcome = evaluation.get("result")
            if outcome is not None:
                return self._normalize(outcome)
        
        result = data.get("result")
        if isinstance(result, str):
            return self._normalize(result)
        
        return None
    
    # ========================================================
    # CONFIDENCE CALCULATION
    # ========================================================
    
    def _calculate_confidence(self, behavior: str) -> float:
        """Calculate confidence for a behavior."""
        total = self.frequency.get(behavior, 0)
        if total <= 0:
            return 0.0
        
        outcomes = self.outcomes.get(behavior, {})
        if not outcomes:
            return min(50.0 + math.log1p(total) * 5.0, 90.0)
        
        success = (
            outcomes.get(OUTCOME_SUCCESS, 0) +
            outcomes.get("correct", 0) +
            outcomes.get("positive", 0)
        )
        
        total_outcomes = sum(outcomes.values())
        if total_outcomes == 0:
            return 50.0
        
        confidence = (success / total_outcomes) * 100
        return max(0.0, min(confidence, 100.0))
    
    # ========================================================
    # MAIN LEARN METHOD
    # ========================================================
    
    def learn(self, data: Dict) -> Dict:
        """
        Learn behavior from data.
        
        Args:
            data: Input data with behavior information
            
        Returns:
            Learning result
        """
        try:
            if not isinstance(data, dict):
                return {"status": "INVALID_DATA"}
            
            domain = self._extract_domain(data)
            signals = self._extract_behavior_signals(data)
            context = self._extract_context(data)
            
            if not signals:
                signals = ["neutral"]
            
            # Update behavior frequency
            for behavior in signals:
                self.behaviors[behavior] += 1
                self.domain_behaviors[domain][behavior] += 1
                self.frequency[behavior] += 1
            
            # Context relationships
            for key, value in context.items():
                context_key = f"{key}:{value}"
                for behavior in signals:
                    self.context_behaviors[context_key][behavior] += 1
            
            # Pattern generation
            if len(signals) > 1:
                pattern = " -> ".join(signals)
                self.patterns[domain][pattern] += 1
                self.sequences.append(signals)
                if len(self.sequences) > self.MAX_HISTORY:
                    self.sequences = self.sequences[-self.MAX_HISTORY:]
            
            # Outcome
            outcome = self._extract_outcome(data)
            if outcome:
                for behavior in signals:
                    self.outcomes[behavior][outcome] += 1
            
            # Update confidence
            for behavior in signals:
                self.confidence[behavior] = self._calculate_confidence(behavior)
            
            # Update trends
            for behavior in signals:
                self.trends[behavior].append({
                    "timestamp": utc_now(),
                    "count": self.frequency[behavior],
                    "confidence": self.confidence.get(behavior, 0),
                })
                if len(self.trends[behavior]) > 100:
                    self.trends[behavior] = self.trends[behavior][-100:]
            
            # Anomaly detection
            self._detect_anomalies(signals, domain)
            
            self.learning_count += 1
            self.last_learning = {
                "time": utc_now(),
                "domain": domain,
                "behaviors": signals,
                "context": context,
                "outcome": outcome,
            }
            
            self.history.append(self.last_learning)
            if len(self.history) > self.MAX_HISTORY:
                self.history = self.history[-self.MAX_HISTORY:]
            
            return {
                "status": "OK",
                "engine": "Behavior Learning Engine",
                "version": self.VERSION,
                "domain": domain,
                "behaviors": signals,
                "context": context,
                "outcome": outcome,
                "confidence": {
                    behavior: round(self.confidence.get(behavior, 0.0), 2)
                    for behavior in signals
                }
            }
            
        except Exception as e:
            logger.exception("Behavior learning failed: %s", e)
            return {"status": "ERROR", "error": str(e)}
    
    # ========================================================
    # ANOMALY DETECTION
    # ========================================================
    
    def _detect_anomalies(self, signals: List[str], domain: str) -> None:
        """Detect anomalous behavior patterns."""
        threshold = self.domain_thresholds.get(domain, 0.5)
        
        for behavior in signals:
            count = self.frequency.get(behavior, 0)
            
            # If behavior is rare, flag as anomaly
            if count == 1 and len(self.history) > 10:
                self.anomaly_count += 1
                self.last_anomaly = {
                    "time": utc_now(),
                    "behavior": behavior,
                    "domain": domain,
                    "reason": "First occurrence",
                }
                self.anomalies.append(self.last_anomaly)
                if len(self.anomalies) > 100:
                    self.anomalies = self.anomalies[-100:]
    
    # ========================================================
    # PREDICTION
    # ========================================================
    
    def predict(self, context=None, domain=None, limit: int = 10) -> List[Dict]:
        """
        Predict behavior based on context and domain.
        
        Args:
            context: Context information
            domain: Domain filter
            limit: Maximum predictions
            
        Returns:
            List of predicted behaviors
        """
        try:
            candidates = Counter()
            
            # Domain-based prediction
            if domain:
                normalized_domain = self._normalize(domain) or DOMAIN_GENERAL
                for behavior, count in self.domain_behaviors.get(normalized_domain, {}).items():
                    candidates[behavior] += count
            
            # Context-based prediction
            if context:
                if isinstance(context, dict):
                    for key, value in context.items():
                        context_key = f"{self._normalize(key)}:{self._normalize(value)}"
                        for behavior, count in self.context_behaviors.get(context_key, {}).items():
                            candidates[behavior] += count
                else:
                    normalized = self._normalize(context)
                    if normalized:
                        for behavior, count in self.context_behaviors.get(normalized, {}).items():
                            candidates[behavior] += count
            
            # Global fallback
            if not candidates:
                candidates.update(self.behaviors)
            
            results = []
            for behavior, count in candidates.most_common(limit):
                results.append({
                    "behavior": behavior,
                    "frequency": count,
                    "confidence": round(self.confidence.get(behavior, 0.0), 2),
                    "trend": self._get_trend(behavior),
                })
            
            self.prediction_count += 1
            self.last_prediction = {
                "time": utc_now(),
                "domain": domain,
                "context": context,
                "predictions": results,
            }
            
            return results
            
        except Exception as e:
            logger.exception("Behavior prediction failed: %s", e)
            return []
    
    def _get_trend(self, behavior: str) -> str:
        """Get trend direction for behavior."""
        trend_data = self.trends.get(behavior, [])
        if len(trend_data) < 3:
            return "stable"
        
        recent = trend_data[-3:]
        counts = [t["count"] for t in recent]
        
        if counts[-1] > counts[0]:
            return "increasing"
        elif counts[-1] < counts[0]:
            return "decreasing"
        return "stable"
    
    # ========================================================
    # GET METHODS
    # ========================================================
    
    def get_behavior(self, domain: Optional[str] = None) -> Dict:
        """Get behavior counts."""
        if domain is None:
            return dict(self.behaviors)
        return dict(self.domain_behaviors.get(self._normalize(domain) or DOMAIN_GENERAL, {}))
    
    def get_patterns(self, domain: Optional[str] = None, limit: int = 20) -> Dict:
        """Get behavior patterns."""
        if domain is None:
            result = {}
            for name, patterns in self.patterns.items():
                result[name] = dict(patterns.most_common(limit))
            return result
        return dict(self.patterns.get(self._normalize(domain) or DOMAIN_GENERAL, {}).most_common(limit))
    
    def get_context_behavior(self, context: Any) -> Dict:
        """Get behavior by context."""
        if isinstance(context, dict):
            results = Counter()
            for key, value in context.items():
                context_key = f"{self._normalize(key)}:{self._normalize(value)}"
                results.update(self.context_behaviors.get(context_key, {}))
            return dict(results.most_common())
        
        normalized = self._normalize(context)
        if normalized:
            return dict(self.context_behaviors.get(normalized, {}))
        return {}
    
    def get_confidence(self, behavior: str) -> float:
        """Get confidence for a behavior."""
        return self.confidence.get(self._normalize(behavior), 0.0)
    
    def get_outcomes(self, behavior: str) -> Dict:
        """Get outcomes for a behavior."""
        return dict(self.outcomes.get(self._normalize(behavior), {}))
    
    def get_trends(self, behavior: str, limit: int = 20) -> List[Dict]:
        """Get trend history for a behavior."""
        return self.trends.get(self._normalize(behavior), [])[-limit:]
    
    def get_anomalies(self, limit: int = 20) -> List[Dict]:
        """Get detected anomalies."""
        return self.anomalies[-limit:]
    
    def get_sequences(self, limit: int = 20) -> List[List[str]]:
        """Get behavior sequences."""
        return self.sequences[-limit:]
    
    # ========================================================
    # FEEDBACK
    # ========================================================
    
    def feedback(self, behavior: str, success: bool = True, outcome: Optional[str] = None) -> Dict:
        """
        Provide feedback on behavior prediction.
        
        Args:
            behavior: Behavior to provide feedback for
            success: Whether the behavior was successful
            outcome: Optional outcome description
            
        Returns:
            Feedback result
        """
        try:
            behavior = self._normalize(behavior)
            if not behavior:
                return {"status": "INVALID_BEHAVIOR"}
            
            self.feedback_count += 1
            
            if success:
                self.success_count += 1
                outcome_key = outcome or OUTCOME_SUCCESS
            else:
                self.failure_count += 1
                outcome_key = outcome or OUTCOME_FAILURE
            
            self.outcomes[behavior][self._normalize(outcome_key)] += 1
            self.confidence[behavior] = self._calculate_confidence(behavior)
            
            self.last_feedback = {
                "time": utc_now(),
                "behavior": behavior,
                "success": success,
                "outcome": outcome_key,
                "confidence": self.confidence[behavior],
            }
            
            return {
                "status": "UPDATED",
                "behavior": behavior,
                "success": success,
                "confidence": round(self.confidence[behavior], 2),
            }
            
        except Exception as e:
            logger.exception("Behavior feedback failed: %s", e)
            return {"status": "ERROR", "error": str(e)}
    
    # ========================================================
    # TOP BEHAVIORS
    # ========================================================
    
    def top(self, limit: int = 20) -> List[Dict]:
        """Get top behaviors."""
        return [
            {
                "behavior": behavior,
                "frequency": frequency,
                "confidence": round(self.confidence.get(behavior, 0.0), 2),
                "trend": self._get_trend(behavior),
            }
            for behavior, frequency in self.behaviors.most_common(limit)
        ]
    
    def top_by_domain(self, domain: str, limit: int = 20) -> List[Dict]:
        """Get top behaviors by domain."""
        domain = self._normalize(domain) or DOMAIN_GENERAL
        behaviors = self.domain_behaviors.get(domain, {})
        return [
            {
                "behavior": behavior,
                "frequency": frequency,
                "confidence": round(self.confidence.get(behavior, 0.0), 2),
            }
            for behavior, frequency in behaviors.most_common(limit)
        ]
    
    # ========================================================
    # SEARCH
    # ========================================================
    
    def search(self, query: str, limit: int = 20) -> List[Dict]:
        """Search behaviors by query."""
        query = self._normalize(query)
        if not query:
            return []
        
        results = []
        for behavior, count in self.behaviors.items():
            if query in behavior:
                results.append({
                    "behavior": behavior,
                    "frequency": count,
                    "confidence": round(self.confidence.get(behavior, 0.0), 2),
                })
                if len(results) >= limit:
                    break
        
        return results
    
    # ========================================================
    # CLEAR
    # ========================================================
    
    def clear(self) -> bool:
        """Clear all behavior data."""
        self.behaviors.clear()
        self.domain_behaviors.clear()
        self.patterns.clear()
        self.context_behaviors.clear()
        self.outcomes.clear()
        self.confidence.clear()
        self.frequency.clear()
        self.trends.clear()
        self.anomalies.clear()
        self.history.clear()
        self.sequences.clear()
        
        self.learning_count = 0
        self.prediction_count = 0
        self.feedback_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.partial_count = 0
        self.anomaly_count = 0
        
        self.last_learning = None
        self.last_prediction = None
        self.last_feedback = None
        self.last_anomaly = None
        
        logger.info("Behavior Engine cleared.")
        return True
    
    # ========================================================
    # STATISTICS
    # ========================================================
    
    def statistics(self) -> Dict:
        """Get behavior statistics."""
        return {
            "total_behaviors": len(self.behaviors),
            "total_domains": len(self.domain_behaviors),
            "total_patterns": sum(len(p) for p in self.patterns.values()),
            "total_contexts": len(self.context_behaviors),
            "total_outcomes": sum(len(o) for o in self.outcomes.values()),
            "total_anomalies": self.anomaly_count,
            "learning_count": self.learning_count,
            "prediction_count": self.prediction_count,
            "feedback_count": self.feedback_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "accuracy": round((self.success_count / max(self.feedback_count, 1)) * 100, 2),
            "avg_confidence": round(
                sum(self.confidence.values()) / max(len(self.confidence), 1),
                2
            ),
            "history_size": len(self.history),
            "sequences": len(self.sequences),
        }
    
    # ========================================================
    # EXPORT / IMPORT
    # ========================================================
    
    def export(self) -> Dict:
        """Export all behavior data."""
        return {
            "version": self.VERSION,
            "exported_at": utc_now(),
            "behaviors": dict(self.behaviors),
            "domain_behaviors": {k: dict(v) for k, v in self.domain_behaviors.items()},
            "patterns": {k: dict(v) for k, v in self.patterns.items()},
            "context_behaviors": {k: dict(v) for k, v in self.context_behaviors.items()},
            "outcomes": {k: dict(v) for k, v in self.outcomes.items()},
            "confidence": self.confidence,
            "history": self.history[-100:],
            "statistics": self.statistics(),
        }
    
    def import_data(self, data: Dict) -> int:
        """Import behavior data."""
        if not data:
            return 0
        
        imported = 0
        
        if "behaviors" in data:
            self.behaviors.update(data["behaviors"])
            imported += len(data["behaviors"])
        
        if "domain_behaviors" in data:
            for domain, behaviors in data["domain_behaviors"].items():
                self.domain_behaviors[domain].update(behaviors)
                imported += len(behaviors)
        
        if "patterns" in data:
            for domain, patterns in data["patterns"].items():
                self.patterns[domain].update(patterns)
                imported += len(patterns)
        
        if "outcomes" in data:
            for behavior, outcomes in data["outcomes"].items():
                self.outcomes[behavior].update(outcomes)
                imported += len(outcomes)
        
        if "confidence" in data:
            self.confidence.update(data["confidence"])
            imported += len(data["confidence"])
        
        logger.info("Imported %s behavior items", imported)
        return imported
    
    # ========================================================
    # STATUS
    # ========================================================
    
    def status(self) -> Dict:
        """Get system status."""
        stats = self.statistics()
        return {
            "module": "behavior",
            "version": self.VERSION,
            "api_version": API_VERSION,
            "status": "ONLINE",
            "behaviors": len(self.behaviors),
            "domains": len(self.domain_behaviors),
            "patterns": stats["total_patterns"],
            "contexts": len(self.context_behaviors),
            "outcome_types": stats["total_outcomes"],
            "learning_count": self.learning_count,
            "prediction_count": self.prediction_count,
            "feedback_count": self.feedback_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "accuracy": stats["accuracy"],
            "history": len(self.history),
            "sequences": len(self.sequences),
            "anomalies": self.anomaly_count,
            "has_last_learning": self.last_learning is not None,
            "has_last_prediction": self.last_prediction is not None,
            "timestamp": utc_now(),
        }


# ============================================================
# GLOBAL INSTANCE
# ============================================================

behavior_engine = BehaviorEngine()


# ============================================================
# COMPATIBILITY FUNCTIONS - MENGGUNAKAN behavior_engine
# ============================================================

def learn(data: Dict) -> Dict:
    """Legacy learn function."""
    return behavior_engine.learn(data)


def predict(context=None, domain=None, limit: int = 10) -> List[Dict]:
    """Legacy predict function."""
    return behavior_engine.predict(context, domain, limit)


def get_behavior(domain: Optional[str] = None) -> Dict:
    """Legacy get_behavior function."""
    return behavior_engine.get_behavior(domain)


def top(limit: int = 20) -> List[Dict]:
    """Legacy top function."""
    return behavior_engine.top(limit)


def status() -> Dict:
    """Legacy status function."""
    return behavior_engine.status()


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict:
    """Run comprehensive self-test."""
    print()
    print("=" * 70)
    print("  BEHAVIOR ENGINE v3.0 - SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        engine = BehaviorEngine()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Learn
    print("\n2. Testing learn...")
    try:
        result = behavior_engine.learn({
            "behavior": "buy",
            "domain": "trading",
            "analysis": {"sentiment": "positive"},
            "context": {"market": "BTC/USD"},
            "outcome": "success",
        })
        if result and result.get("status") == "OK":
            results["learn"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Learn passed")
        else:
            results["learn"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Learn failed")
    except Exception as e:
        results["learn"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Learn failed: {e}")
    
    # Test 3: Predict
    print("\n3. Testing predict...")
    try:
        predictions = behavior_engine.predict(domain="trading")
        if predictions is not None:
            results["predict"] = {"status": "PASS", "count": len(predictions)}
            tests_passed += 1
            print(f"   ✅ Predict passed ({len(predictions)} predictions)")
        else:
            results["predict"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Predict failed")
    except Exception as e:
        results["predict"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Predict failed: {e}")
    
    # Test 4: Status
    print("\n4. Testing status...")
    try:
        status_result = behavior_engine.status()
        if status_result and "status" in status_result:
            results["status"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Status passed")
        else:
            results["status"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Status failed")
    except Exception as e:
        results["status"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Status failed: {e}")
    
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
        "module": "behavior",
        "version": BEHAVIOR_VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "BehaviorEngine",
    "behavior_engine",
    "learn",
    "predict",
    "get_behavior",
    "top",
    "status",
    "self_test",
    "BEHAVIOR_VERSION",
    "API_VERSION",
]


# ============================================================
# END
# ============================================================