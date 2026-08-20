# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# REFLECTION ENGINE v2.0
#
# Functions:
# - Reflect On Experience
# - Evaluate Outcome
# - Detect Success / Failure
# - Compare Prediction vs Reality
# - Calculate Error
# - Generate Learning Lesson
# - Generate Recommendations
# - Track Reflection History
# - Search Reflections
# - Reflection Statistics
# - Latest Reflection
# - Status Monitoring
# - Backward Compatibility
#
# ============================================================

import logging
from datetime import datetime
from collections import Counter
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ============================================================
# CONSTANTS
# ============================================================

MODULE_NAME = "reflection"
MODULE_VERSION = "2.0.0"
API_VERSION = "1.0"


# ============================================================
# REFLECTION ENGINE
# ============================================================

class ReflectionEngine:
    """
    Reflection Engine for learning from outcomes.
    
    Features:
    - Reflect on experiences
    - Evaluate outcomes (success/failure/neutral)
    - Calculate prediction errors
    - Generate learning lessons
    - Generate recommendations
    - Track reflection history
    - Search reflections
    - Reflection statistics
    """

    VERSION = MODULE_VERSION
    NAME = MODULE_NAME

    def __init__(self, max_history: int = 1000):
        self.name = self.NAME
        self.max_history = max(1, int(max_history))
        self.reflections: List[Dict[str, Any]] = []
        self.total_reflections = 0
        self.success_count = 0
        self.failure_count = 0
        self.neutral_count = 0
        
        logger.info("Reflection Engine v%s initialized.", self.VERSION)

    # ========================================================
    # MAIN REFLECTION
    # ========================================================

    def reflect(
        self,
        event: Any,
        outcome: Any = None,
        prediction: Any = None,
        reality: Any = None,
        confidence: Optional[float] = None,
        context: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a reflection from an event and its outcome.
        
        Args:
            event: The event/action being reflected upon
            outcome: The outcome (success/failure/etc)
            prediction: What was predicted
            reality: What actually happened
            confidence: Confidence level (0-100)
            context: Additional context
            metadata: Additional metadata
            
        Returns:
            Reflection dictionary or None
        """
        try:
            timestamp = datetime.now().isoformat()
            
            evaluation = self.evaluate_outcome(
                outcome=outcome,
                prediction=prediction,
                reality=reality
            )
            
            error = self.calculate_error(
                prediction=prediction,
                reality=reality
            )
            
            lesson = self.generate_lesson(
                outcome=outcome,
                prediction=prediction,
                reality=reality,
                evaluation=evaluation,
                error=error
            )
            
            recommendation = self.generate_recommendation(
                evaluation=evaluation,
                error=error,
                confidence=confidence
            )
            
            reflection = {
                "id": self._generate_id(),
                "time": timestamp,
                "timestamp": timestamp,
                "event": event,
                "outcome": outcome,
                "prediction": prediction,
                "reality": reality,
                "evaluation": evaluation,
                "error": error,
                "confidence": self.normalize_confidence(confidence),
                "lesson": lesson,
                "recommendation": recommendation,
                "context": context if isinstance(context, dict) else {},
                "metadata": metadata if isinstance(metadata, dict) else {}
            }
            
            self._store(reflection)
            return reflection
            
        except Exception as e:
            logger.exception("Reflection failed: %s", e)
            return None

    # ========================================================
    # INTERNAL HELPERS
    # ========================================================

    def _generate_id(self) -> str:
        """Generate a unique ID for reflection."""
        import uuid
        return f"ref_{uuid.uuid4().hex[:8]}"

    def _store(self, reflection: Dict[str, Any]) -> None:
        """Store a reflection."""
        self.reflections.append(reflection)
        
        if len(self.reflections) > self.max_history:
            self.reflections = self.reflections[-self.max_history:]
        
        self.total_reflections += 1
        
        evaluation = reflection.get("evaluation")
        if evaluation == "success":
            self.success_count += 1
        elif evaluation == "failure":
            self.failure_count += 1
        else:
            self.neutral_count += 1

    # ========================================================
    # OUTCOME EVALUATION
    # ========================================================

    def evaluate_outcome(
        self,
        outcome: Any = None,
        prediction: Any = None,
        reality: Any = None
    ) -> str:
        """
        Evaluate the outcome of an event.
        
        Returns:
            "success", "failure", or "neutral"
        """
        if outcome is not None:
            normalized = self.normalize_outcome(outcome)
            if normalized in ("success", "correct", "right", "confirmed", "profit", "win"):
                return "success"
            if normalized in ("wrong", "failure", "failed", "incorrect", "loss", "lost"):
                return "failure"
        
        if prediction is not None and reality is not None:
            try:
                if prediction == reality:
                    return "success"
                return "failure"
            except Exception:
                pass
        
        return "neutral"

    def normalize_outcome(self, outcome: Any) -> str:
        """Normalize outcome to string."""
        if outcome is None:
            return ""
        return str(outcome).strip().lower()

    # ========================================================
    # CONFIDENCE NORMALIZATION
    # ========================================================

    def normalize_confidence(self, confidence: Any) -> Optional[float]:
        """Normalize confidence to 0-100."""
        if confidence is None:
            return None
        
        try:
            value = float(confidence)
            if 0 <= value <= 1:
                value *= 100
            return round(max(0, min(value, 100)), 2)
        except (TypeError, ValueError):
            return None

    # ========================================================
    # ERROR CALCULATION
    # ========================================================

    def calculate_error(
        self,
        prediction: Any = None,
        reality: Any = None
    ) -> Dict[str, Any]:
        """Calculate error between prediction and reality."""
        if prediction is None or reality is None:
            return {
                "available": False,
                "type": None,
                "value": None
            }
        
        # Numeric error
        if isinstance(prediction, (int, float)) and isinstance(reality, (int, float)):
            difference = prediction - reality
            absolute = abs(difference)
            percentage = (absolute / abs(reality)) * 100 if reality != 0 else None
            
            return {
                "available": True,
                "type": "numeric",
                "value": round(difference, 6),
                "absolute": round(absolute, 6),
                "percentage": round(percentage, 2) if percentage is not None else None
            }
        
        # Categorical / exact match
        matched = prediction == reality
        return {
            "available": True,
            "type": "categorical",
            "value": 0 if matched else 1,
            "absolute": 0 if matched else 1,
            "percentage": 0 if matched else 100
        }

    # ========================================================
    # LESSON GENERATOR
    # ========================================================

    def generate_lesson(
        self,
        outcome: Any = None,
        prediction: Any = None,
        reality: Any = None,
        evaluation: Optional[str] = None,
        error: Optional[Dict] = None
    ) -> str:
        """Generate a learning lesson."""
        if evaluation is None:
            evaluation = self.evaluate_outcome(outcome, prediction, reality)
        
        if evaluation == "failure":
            if isinstance(error, dict) and error.get("type") == "numeric":
                percentage = error.get("percentage")
                if percentage is not None:
                    return (
                        f"Prediction did not match reality. "
                        f"Numeric deviation was {percentage}%. "
                        "Future predictions should consider stronger validation."
                    )
            return (
                "Prediction failed. "
                "The underlying assumptions should be reviewed "
                "before repeating the pattern."
            )
        
        if evaluation == "success":
            return (
                "Prediction was confirmed. "
                "The associated pattern and reasoning "
                "are reinforced by the observed outcome."
            )
        
        return (
            "Outcome was inconclusive. "
            "More observations are required before "
            "reinforcing or rejecting the pattern."
        )

    # ========================================================
    # RECOMMENDATION GENERATOR
    # ========================================================

    def generate_recommendation(
        self,
        evaluation: str,
        error: Optional[Dict] = None,
        confidence: Optional[float] = None
    ) -> str:
        """Generate a recommendation based on reflection."""
        normalized_confidence = self.normalize_confidence(confidence)
        
        if evaluation == "failure":
            if normalized_confidence is not None and normalized_confidence >= 80:
                return (
                    "Review high-confidence assumptions. "
                    "Confidence may be overestimated."
                )
            return (
                "Reduce confidence and collect "
                "additional evidence before repeating "
                "the decision pattern."
            )
        
        if evaluation == "success":
            return (
                "Retain the successful pattern while "
                "continuing to validate it with new data."
            )
        
        return (
            "Continue observation and avoid "
            "overfitting to the current result."
        )

    # ========================================================
    # ANALYZE REFLECTION
    # ========================================================

    def analyze(self, reflection: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a reflection."""
        if not isinstance(reflection, dict):
            return {"valid": False, "reason": "Reflection must be a dictionary."}
        
        return {
            "valid": True,
            "evaluation": reflection.get("evaluation", "neutral"),
            "has_prediction": reflection.get("prediction") is not None,
            "has_reality": reflection.get("reality") is not None,
            "has_error": bool(reflection.get("error", {})),
            "confidence": reflection.get("confidence"),
            "lesson": reflection.get("lesson"),
            "recommendation": reflection.get("recommendation")
        }

    # ========================================================
    # GET METHODS
    # ========================================================

    def latest(self) -> Optional[Dict[str, Any]]:
        """Get the latest reflection."""
        return self.reflections[-1] if self.reflections else None

    def get_reflections(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent reflections."""
        limit = max(1, int(limit))
        return self.reflections[-limit:]

    def history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Alias for get_reflections."""
        return self.get_reflections(limit)

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search reflections by keyword."""
        if not query:
            return []
        
        query = str(query).strip().lower()
        if not query:
            return []
        
        results = []
        for reflection in self.reflections:
            searchable = " ".join([
                str(reflection.get("event", "")),
                str(reflection.get("outcome", "")),
                str(reflection.get("lesson", "")),
                str(reflection.get("evaluation", "")),
                str(reflection.get("recommendation", ""))
            ]).lower()
            
            if query in searchable:
                results.append(reflection)
        
        return results

    def filter_by_evaluation(self, evaluation: str) -> List[Dict[str, Any]]:
        """Filter reflections by evaluation."""
        target = str(evaluation).strip().lower()
        return [
            r for r in self.reflections
            if str(r.get("evaluation", "")).lower() == target
        ]

    def filter_by_success(self) -> List[Dict[str, Any]]:
        """Get successful reflections."""
        return self.filter_by_evaluation("success")

    def filter_by_failure(self) -> List[Dict[str, Any]]:
        """Get failed reflections."""
        return self.filter_by_evaluation("failure")

    # ========================================================
    # STATISTICS
    # ========================================================

    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_reflections == 0:
            return 0.0
        return round((self.success_count / self.total_reflections) * 100, 2)

    def statistics(self) -> Dict[str, Any]:
        """Get reflection statistics."""
        evaluations = Counter(
            r.get("evaluation", "neutral") for r in self.reflections
        )
        
        return {
            "total": self.total_reflections,
            "stored": len(self.reflections),
            "success": self.success_count,
            "failure": self.failure_count,
            "neutral": self.neutral_count,
            "success_rate": self.success_rate(),
            "evaluations": dict(evaluations),
            "timestamp": datetime.now().isoformat()
        }

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self) -> bool:
        """Clear all reflections."""
        self.reflections.clear()
        self.total_reflections = 0
        self.success_count = 0
        self.failure_count = 0
        self.neutral_count = 0
        return True

    # ========================================================
    # STATUS
    # ========================================================

    def status(self) -> Dict[str, Any]:
        """Get engine status."""
        stats = self.statistics()
        return {
            "module": self.NAME,
            "version": self.VERSION,
            "api_version": API_VERSION,
            "status": "ONLINE",
            "stored": stats["stored"],
            "total": stats["total"],
            "success": stats["success"],
            "failure": stats["failure"],
            "neutral": stats["neutral"],
            "success_rate": stats["success_rate"],
            "max_history": self.max_history,
            "has_latest": self.latest() is not None,
            "timestamp": datetime.now().isoformat()
        }


# ============================================================
# GLOBAL INSTANCE
# ============================================================

reflection_engine = ReflectionEngine()


# ============================================================
# COMPATIBILITY FUNCTIONS
# ============================================================

def reflect(event: Any, **kwargs) -> Optional[Dict[str, Any]]:
    """Legacy reflect function."""
    return reflection_engine.reflect(event, **kwargs)


def latest() -> Optional[Dict[str, Any]]:
    """Legacy latest function."""
    return reflection_engine.latest()


def history(limit: int = 50) -> List[Dict[str, Any]]:
    """Legacy history function."""
    return reflection_engine.history(limit)


def status() -> Dict[str, Any]:
    """Legacy status function."""
    return reflection_engine.status()


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    """Run comprehensive self-test."""
    print()
    print("=" * 70)
    print("  REFLECTION ENGINE v2.0 - SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        engine = ReflectionEngine()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Reflect - Success
    print("\n2. Testing reflect (success)...")
    try:
        reflection = reflection_engine.reflect(
            event="Test event",
            prediction="up",
            reality="up",
            confidence=85
        )
        if reflection and reflection.get("evaluation") == "success":
            results["reflect_success"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Reflect success passed")
        else:
            results["reflect_success"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Reflect success failed")
    except Exception as e:
        results["reflect_success"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Reflect success failed: {e}")
    
    # Test 3: Reflect - Failure
    print("\n3. Testing reflect (failure)...")
    try:
        reflection = reflection_engine.reflect(
            event="Test event",
            prediction="up",
            reality="down",
            confidence=90
        )
        if reflection and reflection.get("evaluation") == "failure":
            results["reflect_failure"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Reflect failure passed")
        else:
            results["reflect_failure"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Reflect failure failed")
    except Exception as e:
        results["reflect_failure"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Reflect failure failed: {e}")
    
    # Test 4: Statistics
    print("\n4. Testing statistics...")
    try:
        stats = reflection_engine.statistics()
        if stats and stats["total"] >= 2:
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
    
    # Test 5: Status
    print("\n5. Testing status...")
    try:
        status_result = reflection_engine.status()
        if status_result and "module" in status_result:
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
        "module": "reflection",
        "version": reflection_engine.VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "MODULE_NAME",
    "MODULE_VERSION",
    "API_VERSION",
    "ReflectionEngine",
    "reflection_engine",
    "reflect",
    "latest",
    "history",
    "status",
    "self_test",
]


# ============================================================
# END
# ============================================================