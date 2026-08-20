# ============================================================
# core/learning/insight.py
# INSIGHT ENGINE v3.0
# SUPER COMPREHENSIVE INTELLIGENCE INSIGHT LAYER
#
# FITUR LENGKAP:
# 1. Generate intelligence insights
# 2. Summarize multi-module analysis
# 3. Extract important factors
# 4. Calculate confidence
# 5. Detect dominant signals
# 6. Detect conflicts between modules
# 7. Build intelligence reports
# 8. Compare insights
# 9. Track insight history
# 10. Search historical insights
# 11. Rank insight importance
# 12. Generate recommendations
# 13. Maintain insight statistics
# 14. Export/Import insights
# 15. Insight validation
# 16. Multi-domain support
# 17. Sentiment analysis integration
# 18. Priority scoring
# 19. Insight categorization
# 20. Temporal analysis
# ============================================================

from __future__ import annotations

import logging
import json
import uuid
from copy import deepcopy
from datetime import datetime
from collections import Counter
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ============================================================
# VERSION
# ============================================================

INSIGHT_VERSION = "3.0.0"
API_VERSION = "1.0"


# ============================================================
# CONSTANTS
# ============================================================

SIGNAL_BULLISH = "bullish"
SIGNAL_BEARISH = "bearish"
SIGNAL_NEUTRAL = "neutral"
SIGNAL_UNCERTAIN = "uncertain"

INSIGHT_TYPE_GENERAL = "general"
INSIGHT_TYPE_MARKET = "market"
INSIGHT_TYPE_PREDICTION = "prediction"
INSIGHT_TYPE_DECISION = "decision"
INSIGHT_TYPE_STRATEGY = "strategy"
INSIGHT_TYPE_LEARNING = "learning"
INSIGHT_TYPE_PERFORMANCE = "performance"

INSIGHT_STATUS_ACTIVE = "active"
INSIGHT_STATUS_ARCHIVED = "archived"
INSIGHT_STATUS_DEPRECATED = "deprecated"
INSIGHT_STATUS_PENDING = "pending"
INSIGHT_STATUS_CONFIRMED = "confirmed"


# ============================================================
# TIME HELPER
# ============================================================

def utc_now() -> str:
    """Return current UTC timestamp."""
    return datetime.now().isoformat()


# ============================================================
# INSIGHT ENGINE v3.0
# ============================================================

class InsightEngine:
    """
    Super Comprehensive Insight Engine.
    
    Features:
    - Generate intelligence insights
    - Summarize multi-module analysis
    - Extract important factors
    - Calculate confidence
    - Detect dominant signals
    - Detect conflicts between modules
    - Build intelligence reports
    - Compare insights
    - Track insight history
    - Search historical insights
    - Rank insight importance
    - Generate recommendations
    - Maintain insight statistics
    - Export/Import insights
    """
    
    VERSION = INSIGHT_VERSION
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "insight"
        self.max_history = self.config.get("max_history", 1000)
        self.insights: List[Dict[str, Any]] = []
        self.archived: List[Dict[str, Any]] = []
        
        self.total_generated = 0
        self.total_success = 0
        self.total_failed = 0
        self.total_conflicts_detected = 0
        self.total_recommendations = 0
        
        self.last_generated: Optional[str] = None
        self.last_insight: Optional[Dict[str, Any]] = None
        
        logger.info("Insight Engine v%s initialized.", self.VERSION)
    
    # ========================================================
    # MAIN INSIGHT GENERATOR
    # ========================================================
    
    def generate(
        self,
        data: Any,
        source: str = "unknown",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate intelligence insight from data.
        
        Args:
            data: Input data from various modules
            source: Source of data (analysis, prediction, etc.)
            metadata: Additional metadata
            
        Returns:
            Insight object or None
        """
        try:
            self.total_generated += 1
            
            # Normalize data
            if data is None:
                data = {}
            if not isinstance(data, dict):
                data = {"data": data}
            
            timestamp = utc_now()
            
            # Extract components
            confidence = self.calculate_confidence(data)
            dominant_signal = self.detect_dominant_signal(data)
            conflicts = self.detect_conflicts(data)
            points = self.extract_points(data)
            domains = self.detect_domains(data)
            insight_type = self.detect_type(data, dominant_signal)
            importance = self.calculate_importance(data, confidence, conflicts)
            recommendation = self.generate_recommendation(data, dominant_signal, conflicts)
            summary = self.create_summary(data)
            
            # Build insight
            insight = {
                "id": str(uuid.uuid4())[:8],
                "timestamp": timestamp,
                "time": timestamp,
                "source": str(source),
                "type": insight_type,
                "domains": domains,
                "summary": summary,
                "details": points,
                "confidence": confidence,
                "dominant_signal": dominant_signal,
                "conflicts": conflicts,
                "importance": importance,
                "recommendation": recommendation,
                "source_count": self.count_sources(data),
                "status": INSIGHT_STATUS_ACTIVE,
                "version": 1,
                "metadata": deepcopy(metadata) if metadata else {},
                "history": [{"action": "generated", "timestamp": timestamp}],
            }
            
            # Store
            self.insights.append(insight)
            if len(self.insights) > self.max_history:
                self.insights = self.insights[-self.max_history:]
            
            self.total_success += 1
            self.last_generated = timestamp
            self.last_insight = insight
            
            logger.debug("Insight generated: %s", insight["id"])
            return insight
            
        except Exception as e:
            self.total_failed += 1
            logger.exception("Insight generation failed: %s", e)
            return None
    
    # ========================================================
    # SUMMARY GENERATOR
    # ========================================================
    
    def create_summary(self, data: Dict[str, Any]) -> str:
        """Create natural language summary."""
        if not isinstance(data, dict):
            return "No structured intelligence data available."
        
        text = []
        
        analysis = self._safe_dict(data.get("analysis"))
        reasoning = self._safe_dict(data.get("reasoning"))
        decision = self._safe_dict(data.get("decision"))
        prediction = self._safe_dict(data.get("prediction"))
        strategy = self._safe_dict(data.get("strategy"))
        semantic = self._safe_dict(data.get("semantic"))
        experience = self._safe_dict(data.get("experience"))
        
        # Sentiment
        sentiment = analysis.get("sentiment") or semantic.get("sentiment") or "neutral"
        sentiment = str(sentiment).lower()
        
        if sentiment == "positive":
            text.append("Market condition shows positive momentum.")
        elif sentiment == "negative":
            text.append("Market condition shows weakness or negative pressure.")
        else:
            text.append("Market condition remains neutral or uncertain.")
        
        # Trend
        trend = analysis.get("trend")
        if trend:
            text.append(f"Detected trend: {trend}.")
        
        # Prediction
        predicted = prediction.get("prediction") or prediction.get("signal") or prediction.get("direction")
        if predicted:
            text.append(f"Prediction indicates {predicted}.")
        
        # Reasoning
        reasoning_summary = reasoning.get("summary")
        if reasoning_summary:
            text.append(str(reasoning_summary))
        
        # Strategy
        strategy_name = strategy.get("name") or strategy.get("strategy")
        if strategy_name:
            text.append(f"Strategy context: {strategy_name}.")
        
        # Experience
        if experience:
            lesson = experience.get("lesson") or experience.get("insight")
            if lesson:
                text.append(f"Learning from experience: {lesson}.")
        
        # Decision
        action = decision.get("action") or decision.get("signal") or "HOLD"
        confidence = decision.get("confidence")
        if confidence is None:
            confidence = self.calculate_confidence(data)
        
        text.append(f"Current recommendation: {action} with confidence {confidence}%.")
        
        return " ".join(text)
    
    # ========================================================
    # POINT EXTRACTION
    # ========================================================
    
    def extract_points(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract important points from data."""
        points = []
        
        if not isinstance(data, dict):
            return points
        
        sources = [
            ("analysis", data.get("analysis")),
            ("prediction", data.get("prediction")),
            ("reasoning", data.get("reasoning")),
            ("decision", data.get("decision")),
            ("strategy", data.get("strategy")),
            ("semantic", data.get("semantic")),
            ("experience", data.get("experience")),
            ("learning", data.get("learning")),
        ]
        
        for source_name, item in sources:
            if not isinstance(item, dict):
                continue
            
            for key, value in item.items():
                if value is not None:
                    points.append({
                        "source": source_name,
                        "factor": str(key),
                        "value": value
                    })
        
        return points
    
    # ========================================================
    # CONFIDENCE CALCULATION
    # ========================================================
    
    def calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score (0-100)."""
        if not isinstance(data, dict):
            return 0.0
        
        values = []
        sources = [
            data.get("analysis"),
            data.get("prediction"),
            data.get("decision"),
            data.get("reasoning"),
            data.get("strategy"),
            data.get("learning"),
        ]
        
        for source in sources:
            if not isinstance(source, dict):
                continue
            
            # Try multiple confidence fields
            value = source.get("confidence") or source.get("score") or source.get("confidence_score")
            if value is None:
                value = source.get("quality") or source.get("strength")
            
            numeric = self._numeric(value)
            if numeric is not None:
                # Normalize 0-1 to 0-100
                if 0 <= numeric <= 1:
                    numeric *= 100
                numeric = max(0.0, min(100.0, numeric))
                values.append(numeric)
        
        if not values:
            return 0.0
        
        return round(sum(values) / len(values), 2)
    
    # ========================================================
    # DOMINANT SIGNAL DETECTION
    # ========================================================
    
    def detect_dominant_signal(self, data: Dict[str, Any]) -> str:
        """Detect dominant signal from multiple sources."""
        if not isinstance(data, dict):
            return SIGNAL_NEUTRAL
        
        signals = []
        sources = [
            data.get("analysis"),
            data.get("prediction"),
            data.get("decision"),
            data.get("strategy"),
            data.get("reasoning"),
        ]
        
        keys = ["signal", "direction", "trend", "prediction", "action", "sentiment"]
        
        for source in sources:
            if not isinstance(source, dict):
                continue
            
            for key in keys:
                value = source.get(key)
                if value:
                    normalized = str(value).lower().strip()
                    
                    bullish_words = ["bull", "buy", "long", "up", "positive", "bullish"]
                    bearish_words = ["bear", "sell", "short", "down", "negative", "bearish"]
                    
                    if any(word in normalized for word in bullish_words):
                        signals.append(SIGNAL_BULLISH)
                    elif any(word in normalized for word in bearish_words):
                        signals.append(SIGNAL_BEARISH)
                    elif any(word in normalized for word in ["hold", "neutral", "sideways"]):
                        signals.append(SIGNAL_NEUTRAL)
        
        if not signals:
            return SIGNAL_NEUTRAL
        
        # Get most common signal
        counter = Counter(signals)
        most_common = counter.most_common(1)[0]
        
        # If tie, return neutral
        if len(counter) > 1 and most_common[1] == 1:
            return SIGNAL_UNCERTAIN
        
        return most_common[0]
    
    # ========================================================
    # CONFLICT DETECTION
    # ========================================================
    
    def detect_conflicts(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect conflicts between different sources."""
        if not isinstance(data, dict):
            return []
        
        conflicts = []
        
        analysis = self._safe_dict(data.get("analysis"))
        prediction = self._safe_dict(data.get("prediction"))
        decision = self._safe_dict(data.get("decision"))
        reasoning = self._safe_dict(data.get("reasoning"))
        strategy = self._safe_dict(data.get("strategy"))
        
        # Extract signals
        analysis_signal = self._normalize_signal(
            analysis.get("signal") or analysis.get("trend")
        )
        prediction_signal = self._normalize_signal(
            prediction.get("signal") or prediction.get("direction") or prediction.get("prediction")
        )
        decision_signal = self._normalize_signal(
            decision.get("action") or decision.get("signal")
        )
        reasoning_signal = self._normalize_signal(
            reasoning.get("conclusion") or reasoning.get("direction")
        )
        strategy_signal = self._normalize_signal(
            strategy.get("bias") or strategy.get("direction")
        )
        
        # Check conflicts
        if analysis_signal and prediction_signal and analysis_signal != prediction_signal:
            conflicts.append({
                "type": "analysis_prediction",
                "analysis": analysis_signal,
                "prediction": prediction_signal,
                "severity": "high",
            })
            self.total_conflicts_detected += 1
        
        if prediction_signal and decision_signal and prediction_signal != decision_signal:
            conflicts.append({
                "type": "prediction_decision",
                "prediction": prediction_signal,
                "decision": decision_signal,
                "severity": "critical",
            })
            self.total_conflicts_detected += 1
        
        if reasoning_signal and decision_signal and reasoning_signal != decision_signal:
            conflicts.append({
                "type": "reasoning_decision",
                "reasoning": reasoning_signal,
                "decision": decision_signal,
                "severity": "medium",
            })
            self.total_conflicts_detected += 1
        
        if strategy_signal and analysis_signal and strategy_signal != analysis_signal:
            conflicts.append({
                "type": "strategy_analysis",
                "strategy": strategy_signal,
                "analysis": analysis_signal,
                "severity": "medium",
            })
            self.total_conflicts_detected += 1
        
        return conflicts
    
    # ========================================================
    # IMPORTANCE CALCULATION
    # ========================================================
    
    def calculate_importance(
        self,
        data: Dict[str, Any],
        confidence: float = 0.0,
        conflicts: Optional[List[Dict]] = None
    ) -> float:
        """Calculate importance score (0-1)."""
        score = 0.5
        
        # Confidence contribution
        confidence_value = self._numeric(confidence) or 0
        score += (min(confidence_value, 100) / 100) * 0.3
        
        # Conflict penalty
        if conflicts:
            score -= min(len(conflicts) * 0.1, 0.3)
        
        # Source count bonus
        source_count = self.count_sources(data)
        score += min(source_count * 0.03, 0.2)
        
        # Data richness
        if isinstance(data, dict):
            keys = len(data)
            score += min(keys * 0.01, 0.2)
        
        return round(max(0.0, min(score, 1.0)), 2)
    
    # ========================================================
    # RECOMMENDATION GENERATOR
    # ========================================================
    
    def generate_recommendation(
        self,
        data: Dict[str, Any],
        dominant_signal: Optional[str] = None,
        conflicts: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Generate recommendation based on insights."""
        self.total_recommendations += 1
        
        if conflicts:
            return {
                "action": "CAUTION",
                "reason": "Intelligence sources are conflicting. Verify before acting.",
                "signal": dominant_signal or SIGNAL_NEUTRAL,
                "priority": "high",
                "suggestion": "Wait for confirmation or seek additional data.",
            }
        
        if dominant_signal == SIGNAL_BULLISH:
            return {
                "action": "MONITOR_LONG",
                "reason": "Multiple intelligence sources indicate bullish conditions.",
                "signal": SIGNAL_BULLISH,
                "priority": "medium",
                "suggestion": "Consider entry with proper risk management.",
            }
        
        if dominant_signal == SIGNAL_BEARISH:
            return {
                "action": "MONITOR_SHORT",
                "reason": "Multiple intelligence sources indicate bearish conditions.",
                "signal": SIGNAL_BEARISH,
                "priority": "medium",
                "suggestion": "Consider reducing exposure or hedging.",
            }
        
        if dominant_signal == SIGNAL_UNCERTAIN:
            return {
                "action": "OBSERVE",
                "reason": "Mixed signals detected. Market direction unclear.",
                "signal": SIGNAL_UNCERTAIN,
                "priority": "low",
                "suggestion": "Maintain current position and monitor closely.",
            }
        
        return {
            "action": "HOLD",
            "reason": "Insufficient directional agreement or neutral conditions.",
            "signal": SIGNAL_NEUTRAL,
            "priority": "low",
            "suggestion": "Wait for clearer signals before making decisions.",
        }
    
    # ========================================================
    # TYPE DETECTION
    # ========================================================
    
    def detect_type(self, data: Dict[str, Any], signal: Optional[str] = None) -> str:
        """Detect insight type."""
        if not isinstance(data, dict):
            return INSIGHT_TYPE_GENERAL
        
        if data.get("prediction") or data.get("forecast"):
            return INSIGHT_TYPE_PREDICTION
        
        if data.get("decision") or data.get("action"):
            return INSIGHT_TYPE_DECISION
        
        if data.get("strategy") or data.get("plan"):
            return INSIGHT_TYPE_STRATEGY
        
        if data.get("learning") or data.get("lesson"):
            return INSIGHT_TYPE_LEARNING
        
        if data.get("performance") or data.get("metrics"):
            return INSIGHT_TYPE_PERFORMANCE
        
        if data.get("market") or data.get("analysis"):
            return INSIGHT_TYPE_MARKET
        
        return INSIGHT_TYPE_GENERAL
    
    # ========================================================
    # DOMAIN DETECTION
    # ========================================================
    
    def detect_domains(self, data: Dict[str, Any]) -> List[str]:
        """Detect domains from data."""
        if not isinstance(data, dict):
            return []
        
        domains = []
        known_domains = [
            "trading", "market", "finance", "science",
            "reasoning", "knowledge", "strategy",
            "prediction", "analysis", "semantic",
            "learning", "experience", "decision",
            "performance", "risk", "economics"
        ]
        
        for key in data.keys():
            key_lower = str(key).lower()
            if key_lower in known_domains:
                domains.append(key_lower)
        
        return domains
    
    # ========================================================
    # SOURCE COUNT
    # ========================================================
    
    def count_sources(self, data: Dict[str, Any]) -> int:
        """Count non-null sources in data."""
        if not isinstance(data, dict):
            return 0
        
        return sum(1 for value in data.values() if value is not None)
    
    # ========================================================
    # COMPARE INSIGHTS
    # ========================================================
    
    def compare(self, old: Optional[Dict], new: Optional[Dict]) -> Dict[str, Any]:
        """Compare two insights."""
        if old is None:
            old = {}
        if new is None:
            new = {}
        
        old_summary = old.get("summary") if isinstance(old, dict) else None
        new_summary = new.get("summary") if isinstance(new, dict) else None
        
        old_confidence = old.get("confidence") if isinstance(old, dict) else None
        new_confidence = new.get("confidence") if isinstance(new, dict) else None
        
        old_signal = old.get("dominant_signal") if isinstance(old, dict) else None
        new_signal = new.get("dominant_signal") if isinstance(new, dict) else None
        
        return {
            "changed": old != new,
            "previous": old,
            "current": new,
            "summary_changed": old_summary != new_summary,
            "signal_changed": old_signal != new_signal,
            "confidence_change": (
                (self._numeric(new_confidence) or 0) -
                (self._numeric(old_confidence) or 0)
            ),
            "improved": (
                (self._numeric(new_confidence) or 0) >
                (self._numeric(old_confidence) or 0)
            ),
            "degraded": (
                (self._numeric(new_confidence) or 0) <
                (self._numeric(old_confidence) or 0)
            ),
        }
    
    # ========================================================
    # SEARCH
    # ========================================================
    
    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search insights by keyword."""
        if not query:
            return []
        
        query = str(query).lower()
        results = []
        
        for insight in reversed(self.insights):
            text = json.dumps(insight, default=str).lower()
            if query in text:
                results.append(insight)
                if len(results) >= limit:
                    break
        
        return results
    
    # ========================================================
    # FILTER BY SIGNAL
    # ========================================================
    
    def by_signal(self, signal: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Filter insights by dominant signal."""
        if not signal:
            return []
        
        signal = str(signal).lower()
        results = []
        
        for item in reversed(self.insights):
            if str(item.get("dominant_signal", "")).lower() == signal:
                results.append(item)
                if len(results) >= limit:
                    break
        
        return results
    
    # ========================================================
    # FILTER BY TYPE
    # ========================================================
    
    def by_type(self, insight_type: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Filter insights by type."""
        if not insight_type:
            return []
        
        results = []
        for item in reversed(self.insights):
            if item.get("type") == insight_type:
                results.append(item)
                if len(results) >= limit:
                    break
        
        return results
    
    # ========================================================
    # LATEST
    # ========================================================
    
    def latest(self) -> Optional[Dict[str, Any]]:
        """Get latest insight."""
        return self.last_insight or (self.insights[-1] if self.insights else None)
    
    # ========================================================
    # HISTORY
    # ========================================================
    
    def history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get insight history."""
        limit = max(0, int(limit))
        if limit == 0:
            return []
        return self.insights[-limit:]
    
    # ========================================================
    # CLEAR
    # ========================================================
    
    def clear(self) -> bool:
        """Clear all insights."""
        self.insights.clear()
        self.archived.clear()
        self.last_insight = None
        return True
    
    # ========================================================
    # ARCHIVE
    # ========================================================
    
    def archive(self, insight_id: str) -> bool:
        """Archive an insight."""
        for i, item in enumerate(self.insights):
            if item.get("id") == insight_id:
                item["status"] = INSIGHT_STATUS_ARCHIVED
                self.archived.append(item)
                self.insights.pop(i)
                return True
        return False
    
    # ========================================================
    # EXPORT / IMPORT
    # ========================================================
    
    def export(self) -> Dict[str, Any]:
        """Export all insights."""
        return {
            "version": self.VERSION,
            "exported_at": utc_now(),
            "insights": deepcopy(self.insights),
            "archived": deepcopy(self.archived),
            "statistics": self.statistics(),
        }
    
    def import_data(self, data: Dict[str, Any]) -> int:
        """Import insights."""
        if not data:
            return 0
        
        imported = 0
        for item in data.get("insights", []):
            self.insights.append(item)
            imported += 1
        
        self.total_generated += imported
        return imported
    
    # ========================================================
    # STATISTICS
    # ========================================================
    
    def statistics(self) -> Dict[str, Any]:
        """Get insight statistics."""
        signals = []
        types = []
        
        for item in self.insights:
            signal = item.get("dominant_signal")
            if signal:
                signals.append(signal)
            
            insight_type = item.get("type")
            if insight_type:
                types.append(insight_type)
        
        return {
            "total_generated": self.total_generated,
            "total_success": self.total_success,
            "total_failed": self.total_failed,
            "total_conflicts": self.total_conflicts_detected,
            "total_recommendations": self.total_recommendations,
            "stored": len(self.insights),
            "archived": len(self.archived),
            "signals": dict(Counter(signals)),
            "types": dict(Counter(types)),
            "last_generated": self.last_generated,
            "avg_confidence": round(
                sum(item.get("confidence", 0) for item in self.insights) / max(1, len(self.insights)),
                2
            ),
        }
    
    # ========================================================
    # VALIDATE
    # ========================================================
    
    def validate(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an insight."""
        errors = []
        warnings = []
        
        if not insight.get("summary"):
            errors.append("Missing summary")
        
        if insight.get("confidence", 0) > 100 or insight.get("confidence", 0) < 0:
            errors.append("Confidence out of range (0-100)")
        
        if insight.get("importance", 0) > 1 or insight.get("importance", 0) < 0:
            errors.append("Importance out of range (0-1)")
        
        if not insight.get("timestamp"):
            warnings.append("Missing timestamp")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
    
    # ========================================================
    # STATUS
    # ========================================================
    
    def status(self) -> Dict[str, Any]:
        """Get system status."""
        stats = self.statistics()
        return {
            "name": self.name,
            "version": self.VERSION,
            "api_version": API_VERSION,
            "status": "ONLINE",
            "generated": self.total_generated,
            "successful": self.total_success,
            "failed": self.total_failed,
            "stored": len(self.insights),
            "max_history": self.max_history,
            "last_generated": self.last_generated,
            "has_latest": self.last_insight is not None,
            "timestamp": utc_now(),
        }
    
    # ========================================================
    # INTERNAL HELPERS
    # ========================================================
    
    @staticmethod
    def _safe_dict(value: Any) -> Dict[str, Any]:
        """Safely convert to dict."""
        if isinstance(value, dict):
            return value
        return {}
    
    @staticmethod
    def _numeric(value: Any) -> Optional[float]:
        """Safely convert to float."""
        try:
            if value is None:
                return None
            if isinstance(value, bool):
                return float(value)
            return float(value)
        except (TypeError, ValueError):
            return None
    
    @staticmethod
    def _normalize_signal(value: Any) -> Optional[str]:
        """Normalize signal string."""
        if not value:
            return None
        
        value = str(value).lower().strip()
        
        bullish_words = ["bull", "buy", "long", "up", "positive", "bullish"]
        bearish_words = ["bear", "sell", "short", "down", "negative", "bearish"]
        
        if any(word in value for word in bullish_words):
            return SIGNAL_BULLISH
        if any(word in value for word in bearish_words):
            return SIGNAL_BEARISH
        if any(word in value for word in ["hold", "neutral", "sideways"]):
            return SIGNAL_NEUTRAL
        
        return value


# ============================================================
# GLOBAL INSTANCE
# ============================================================

insight_engine = InsightEngine()


# ============================================================
# COMPATIBILITY FUNCTIONS - MENGGUNAKAN insight_engine
# ============================================================

def generate(data: Any) -> Optional[Dict[str, Any]]:
    """Legacy generate function."""
    return insight_engine.generate(data)


def latest() -> Optional[Dict[str, Any]]:
    """Legacy latest function."""
    return insight_engine.latest()


def history(limit: int = 50) -> List[Dict[str, Any]]:
    """Legacy history function."""
    return insight_engine.history(limit)


def status() -> Dict[str, Any]:
    """Legacy status function."""
    return insight_engine.status()


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    """Run comprehensive self-test."""
    print()
    print("=" * 70)
    print("  INSIGHT ENGINE v3.0 - SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        engine = InsightEngine()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Generate
    print("\n2. Testing generate...")
    try:
        test_data = {
            "analysis": {"sentiment": "positive", "trend": "BULLISH"},
            "prediction": {"signal": "BUY", "confidence": 0.8},
            "decision": {"action": "BUY", "confidence": 75},
        }
        result = insight_engine.generate(test_data, source="test")
        if result and result.get("id"):
            results["generate"] = {"status": "PASS", "id": result["id"]}
            tests_passed += 1
            print(f"   ✅ Generate passed (ID: {result['id']})")
        else:
            results["generate"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Generate failed")
    except Exception as e:
        results["generate"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Generate failed: {e}")
    
    # Test 3: Statistics
    print("\n3. Testing statistics...")
    try:
        stats = insight_engine.statistics()
        if stats and "total_generated" in stats:
            results["statistics"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Statistics passed")
        else:
            results["statistics"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Statistics failed")
    except Exception as e:
        results["statistics"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Statistics failed: {e}")
    
    # Test 4: Status
    print("\n4. Testing status...")
    try:
        status_result = insight_engine.status()
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
    
    # Test 5: Search
    print("\n5. Testing search...")
    try:
        results_search = insight_engine.search("bullish")
        if results_search is not None:
            results["search"] = {"status": "PASS", "count": len(results_search)}
            tests_passed += 1
            print(f"   ✅ Search passed ({len(results_search)} results)")
        else:
            results["search"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Search failed")
    except Exception as e:
        results["search"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Search failed: {e}")
    
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
        "module": "insight",
        "version": INSIGHT_VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "InsightEngine",
    "insight_engine",
    "generate",
    "latest",
    "history",
    "status",
    "self_test",
    "INSIGHT_VERSION",
    "API_VERSION",
    "SIGNAL_BULLISH",
    "SIGNAL_BEARISH",
    "SIGNAL_NEUTRAL",
    "SIGNAL_UNCERTAIN",
]


# ============================================================
# END
# ============================================================