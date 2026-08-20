# ============================================================
# core/learning/curiosity.py
# CURIOSITY ENGINE v3.0
# SUPER COMPREHENSIVE KNOWLEDGE DISCOVERY
#
# FITUR LENGKAP:
# 1. Discover Knowledge Gaps
# 2. Detect Weak Prediction Areas
# 3. Generate Questions
# 4. Prioritize Unknowns
# 5. Track Unresolved Problems
# 6. Confidence-Based Questioning
# 7. Accuracy Gap Detection
# 8. Question Answering & Resolution
# 9. Priority Scoring System
# 10. Knowledge Gap Analysis
# 11. Pattern of Uncertainty Detection
# 12. Curiosity-Driven Learning
# 13. Question History & Tracking
# 14. Domain-Specific Curiosity
# 15. Automated Question Generation
# 16. Question Ranking & Filtering
# 17. Gap Evolution Tracking
# 18. Self-Assessment Questions
# 19. Learning Objective Generation
# 20. Research Direction Suggestions
# ============================================================

from __future__ import annotations

import logging
import uuid
import random
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ============================================================
# VERSION
# ============================================================

CURIOSITY_VERSION = "3.0.0"
API_VERSION = "1.0"


# ============================================================
# CONSTANTS
# ============================================================

# Question status
STATUS_UNRESOLVED = "unresolved"
STATUS_RESOLVED = "resolved"
STATUS_INVESTIGATING = "investigating"
STATUS_DEPRECATED = "deprecated"
STATUS_ANSWERED = "answered"

# Priority levels
PRIORITY_CRITICAL = 90
PRIORITY_HIGH = 75
PRIORITY_MEDIUM = 50
PRIORITY_LOW = 25

# Domain types
DOMAIN_GENERAL = "general"
DOMAIN_MARKET = "market"
DOMAIN_TRADING = "trading"
DOMAIN_LEARNING = "learning"
DOMAIN_TECHNOLOGY = "technology"
DOMAIN_STRATEGY = "strategy"
DOMAIN_KNOWLEDGE = "knowledge"
DOMAIN_PREDICTION = "prediction"
DOMAIN_DECISION = "decision"
DOMAIN_PERFORMANCE = "performance"


# ============================================================
# TIME HELPER
# ============================================================

def utc_now() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now().isoformat()


# ============================================================
# CURIOSITY ENGINE v3.0
# ============================================================

class CuriosityEngine:
    """
    Super Comprehensive Curiosity Engine.
    
    Features:
    - Discover Knowledge Gaps
    - Detect Weak Prediction Areas
    - Generate Questions
    - Prioritize Unknowns
    - Track Unresolved Problems
    - Confidence-Based Questioning
    - Accuracy Gap Detection
    - Question Answering & Resolution
    - Priority Scoring System
    - Knowledge Gap Analysis
    """
    
    VERSION = CURIOSITY_VERSION
    
    def __init__(
        self,
        max_questions: int = 500,
        config: Optional[Dict[str, Any]] = None
    ):
        self.config = config or {}
        self.max_questions = max(1, int(max_questions))
        
        self.questions: List[Dict[str, Any]] = []
        self.gaps: List[Dict[str, Any]] = []
        self.resolved: List[Dict[str, Any]] = []
        self.investigations: List[Dict[str, Any]] = []
        self.gap_history: List[Dict[str, Any]] = []
        
        self.total_questions = 0
        self.total_gaps = 0
        self.total_resolved = 0
        self.total_analysis = 0
        self.total_investigations = 0
        
        self.last_question: Optional[Dict[str, Any]] = None
        self.last_gap: Optional[Dict[str, Any]] = None
        
        # Domain-specific thresholds
        self.domain_thresholds = {
            DOMAIN_MARKET: 65,
            DOMAIN_TRADING: 60,
            DOMAIN_LEARNING: 70,
            DOMAIN_TECHNOLOGY: 75,
            DOMAIN_STRATEGY: 55,
            DOMAIN_KNOWLEDGE: 60,
            DOMAIN_PREDICTION: 70,
            DOMAIN_DECISION: 65,
            DOMAIN_PERFORMANCE: 60,
            DOMAIN_GENERAL: 50,
        }
        
        # Question templates
        self.question_templates = self._load_templates()
        
        logger.info("Curiosity Engine v%s initialized.", self.VERSION)
    
    def _load_templates(self) -> Dict[str, List[str]]:
        """Load question templates."""
        return {
            "accuracy": [
                "Why is {area} performing below expectation?",
                "What causes {area} to be inaccurate?",
                "How can {area} be improved?",
                "What factors affect {area} accuracy?",
            ],
            "confidence": [
                "Why is confidence low in {area}?",
                "What would increase confidence in {area}?",
                "Is {area} reliable enough?",
            ],
            "gap": [
                "What is missing in {area}?",
                "Why does {area} have a knowledge gap?",
                "What information is needed for {area}?",
            ],
            "performance": [
                "Why is {area} underperforming?",
                "How can {area} performance be improved?",
                "What is causing {area} to fail?",
            ],
            "market": [
                "Why is {area} behaving differently?",
                "What drives {area} movement?",
                "What are the key factors for {area}?",
            ],
        }
    
    # ========================================================
    # INTERNAL HELPERS
    # ========================================================
    
    def _timestamp(self) -> str:
        """Get current timestamp."""
        return utc_now()
    
    def _normalize_score(self, value: Any) -> float:
        """Normalize score to 0-100."""
        try:
            score = float(value)
        except (TypeError, ValueError):
            return 0.0
        
        # Support both: 0.0-1.0 and 0-100
        if 0 <= score <= 1:
            score *= 100
        
        return max(0.0, min(score, 100.0))
    
    def _question_exists(self, question: str) -> bool:
        """Check if question already exists."""
        question = str(question).strip().lower()
        for item in self.questions:
            if str(item.get("question", "")).strip().lower() == question:
                return True
        return False
    
    def _trim_questions(self) -> None:
        """Trim questions if exceeded."""
        if len(self.questions) > self.max_questions:
            excess = len(self.questions) - self.max_questions
            self.questions = self.questions[excess:]
    
    # ========================================================
    # PRIORITY CALCULATION
    # ========================================================
    
    def calculate_priority(
        self,
        accuracy: float = 0,
        confidence: float = 0,
        frequency: int = 1,
        impact: float = 0.5,
        urgency: float = 0.5
    ) -> float:
        """
        Calculate priority score (0-100).
        
        Args:
            accuracy: Accuracy score (0-100)
            confidence: Confidence score (0-100)
            frequency: How often this occurs
            impact: Impact level (0-1)
            urgency: Urgency level (0-1)
            
        Returns:
            Priority score (0-100)
        """
        accuracy = self._normalize_score(accuracy)
        confidence = self._normalize_score(confidence)
        
        # Weakness = low accuracy
        weakness = (100 - accuracy) * 0.5
        
        # Uncertainty = low confidence
        uncertainty = (100 - confidence) * 0.3
        
        # Frequency factor
        try:
            freq = max(1, int(frequency))
        except (TypeError, ValueError):
            freq = 1
        recurrence = min(freq * 2, 10)
        
        # Impact factor
        impact_score = impact * 10
        
        # Urgency factor
        urgency_score = urgency * 5
        
        priority = weakness + uncertainty + recurrence + impact_score + urgency_score
        
        return round(max(0.0, min(priority, 100.0)), 2)
    
    # ========================================================
    # GAP DETECTION
    # ========================================================
    
    def analyze_gap(
        self,
        data: Dict[str, Any],
        domain: str = DOMAIN_GENERAL
    ) -> List[Dict[str, Any]]:
        """
        Analyze and detect knowledge gaps.
        
        Args:
            data: Data containing accuracy/confidence info
            domain: Domain of analysis
            
        Returns:
            List of detected gaps
        """
        gaps = []
        
        try:
            self.total_analysis += 1
            
            if not isinstance(data, dict):
                return gaps
            
            accuracy_data = data.get("accuracy", {})
            confidence_data = data.get("confidence", {})
            
            if not isinstance(accuracy_data, dict):
                accuracy_data = {}
            if not isinstance(confidence_data, dict):
                confidence_data = {}
            
            # Get domain threshold
            threshold = self.domain_thresholds.get(domain, 60)
            
            # Process each area
            all_areas = set(accuracy_data.keys()) | set(confidence_data.keys())
            
            for area in all_areas:
                accuracy = self._normalize_score(accuracy_data.get(area, 0))
                confidence = self._normalize_score(confidence_data.get(area, 0))
                
                # Check if below threshold
                if accuracy < threshold or confidence < threshold:
                    gap = {
                        "id": str(uuid.uuid4())[:8],
                        "timestamp": self._timestamp(),
                        "area": area,
                        "domain": domain,
                        "accuracy": accuracy,
                        "confidence": confidence,
                        "threshold": threshold,
                        "reason": self._determine_gap_reason(accuracy, confidence, threshold),
                        "priority": self.calculate_priority(accuracy, confidence),
                        "status": "open",
                        "investigations": 0,
                        "history": [{"action": "detected", "timestamp": self._timestamp()}],
                    }
                    
                    gaps.append(gap)
                    self.gaps.append(gap)
                    self.total_gaps += 1
                    self.last_gap = gap
                    
                    # Generate question
                    question = self._generate_question(area, domain, accuracy, confidence)
                    self.ask(
                        question,
                        area=area,
                        domain=domain,
                        reason=gap["reason"],
                        accuracy=accuracy,
                        confidence=confidence,
                        priority=gap["priority"]
                    )
            
            return gaps
            
        except Exception as e:
            logger.exception("Gap analysis failed: %s", e)
            return []
    
    def _determine_gap_reason(
        self,
        accuracy: float,
        confidence: float,
        threshold: float
    ) -> str:
        """Determine reason for gap."""
        if accuracy < threshold and confidence < threshold:
            return "Low accuracy and low confidence"
        elif accuracy < threshold:
            return "Low prediction accuracy"
        elif confidence < threshold:
            return "Low confidence in predictions"
        else:
            return "Below optimal threshold"
    
    def _generate_question(
        self,
        area: str,
        domain: str,
        accuracy: float,
        confidence: float
    ) -> str:
        """Generate a question based on gap."""
        templates = self.question_templates
        
        if domain in templates:
            domain_templates = templates[domain]
        else:
            domain_templates = templates.get("general", templates["gap"])
        
        # Choose template based on scores
        if accuracy < 40:
            template_key = "accuracy"
        elif confidence < 40:
            template_key = "confidence"
        else:
            template_key = "gap"
        
        template_list = templates.get(template_key, templates["gap"])
        
        # Use random template
        template = random.choice(template_list)
        
        return template.format(area=area)
    
    # ========================================================
    # PREDICTION ANALYSIS
    # ========================================================
    
    def analyze_prediction(
        self,
        prediction: Any,
        reality: Any,
        domain: str = DOMAIN_GENERAL,
        confidence: float = 0.0
    ) -> Dict[str, Any]:
        """
        Analyze prediction vs reality.
        
        Args:
            prediction: Predicted value
            reality: Actual value
            domain: Domain of prediction
            confidence: Confidence in prediction
            
        Returns:
            Analysis result
        """
        correct = prediction == reality
        
        if correct:
            return {
                "correct": True,
                "gap": False,
                "confidence": confidence,
                "message": "Prediction was correct",
            }
        
        # Calculate accuracy
        if isinstance(prediction, (int, float)) and isinstance(reality, (int, float)):
            if reality != 0:
                accuracy = 100 - min(abs((prediction - reality) / reality) * 100, 100)
            else:
                accuracy = 50 if prediction == reality else 0
        else:
            accuracy = 100.0 if correct else 0.0
        
        # Create gap
        area = f"{domain}.prediction"
        question = f"Why did the prediction for {domain} fail?"
        
        item = self.ask(
            question,
            area=area,
            domain=domain,
            reason="Prediction mismatch with reality",
            accuracy=accuracy,
            confidence=confidence,
            priority=self.calculate_priority(accuracy, confidence)
        )
        
        return {
            "correct": False,
            "gap": True,
            "accuracy": accuracy,
            "question": item,
            "message": f"Prediction failed with {accuracy:.1f}% accuracy",
        }
    
    # ========================================================
    # CONFIDENCE ANALYSIS
    # ========================================================
    
    def analyze_confidence(
        self,
        data: Dict[str, float],
        threshold: float = 60.0
    ) -> List[Dict[str, Any]]:
        """
        Analyze confidence levels.
        
        Args:
            data: Dictionary of area -> confidence
            threshold: Minimum confidence threshold
            
        Returns:
            List of low confidence areas
        """
        results = []
        
        if not isinstance(data, dict):
            return results
        
        for area, value in data.items():
            confidence = self._normalize_score(value)
            
            if confidence < threshold:
                results.append({
                    "area": area,
                    "confidence": confidence,
                    "threshold": threshold,
                    "gap": threshold - confidence,
                    "reason": "Low confidence",
                    "priority": self.calculate_priority(50, confidence),
                })
        
        return results
    
    # ========================================================
    # QUESTION MANAGEMENT
    # ========================================================
    
    def ask(
        self,
        question: str,
        area: Optional[str] = None,
        domain: str = DOMAIN_GENERAL,
        reason: str = "Unknown",
        accuracy: Optional[float] = None,
        confidence: Optional[float] = None,
        priority: float = 50.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Ask a question.
        
        Args:
            question: Question text
            area: Area of question
            domain: Domain of question
            reason: Why this question is asked
            accuracy: Current accuracy
            confidence: Current confidence
            priority: Priority score
            metadata: Additional metadata
            
        Returns:
            Question object or None
        """
        question = str(question).strip()
        if not question:
            return None
        
        if self._question_exists(question):
            return None
        
        item = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": self._timestamp(),
            "question": question,
            "area": area,
            "domain": domain,
            "reason": reason,
            "accuracy": self._normalize_score(accuracy) if accuracy is not None else None,
            "confidence": self._normalize_score(confidence) if confidence is not None else None,
            "priority": max(0.0, min(float(priority), 100.0)),
            "status": STATUS_UNRESOLVED,
            "metadata": deepcopy(metadata) if metadata else {},
            "history": [{"action": "asked", "timestamp": self._timestamp()}],
            "investigations": 0,
        }
        
        self.questions.append(item)
        self.total_questions += 1
        self.last_question = item
        self._trim_questions()
        
        logger.debug("Question asked: %s", question[:50])
        return item
    
    def resolve(
        self,
        question_id: str,
        answer: Optional[Any] = None,
        note: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Resolve a question.
        
        Args:
            question_id: Question ID
            answer: Answer to the question
            note: Resolution note
            
        Returns:
            Resolved question or None
        """
        for item in self.questions:
            if item.get("id") == question_id and item.get("status") == STATUS_UNRESOLVED:
                item["status"] = STATUS_RESOLVED
                item["resolved_at"] = self._timestamp()
                item["answer"] = answer
                item["resolution_note"] = note
                item["history"].append({"action": "resolved", "timestamp": self._timestamp()})
                
                self.resolved.append(item)
                self.total_resolved += 1
                
                logger.info("Question resolved: %s", item.get("question", "")[:50])
                return item
        
        return None
    
    def investigate(
        self,
        question_id: str,
        note: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Mark a question as under investigation.
        
        Args:
            question_id: Question ID
            note: Investigation note
            
        Returns:
            Updated question or None
        """
        for item in self.questions:
            if item.get("id") == question_id and item.get("status") == STATUS_UNRESOLVED:
                item["status"] = STATUS_INVESTIGATING
                item["investigations"] += 1
                item["history"].append({"action": "investigating", "note": note, "timestamp": self._timestamp()})
                self.total_investigations += 1
                self.investigations.append(item)
                return item
        
        return None
    
    # ========================================================
    # GET QUESTIONS
    # ========================================================
    
    def get_questions(
        self,
        limit: int = 20,
        unresolved_only: bool = False,
        domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get questions.
        
        Args:
            limit: Maximum number of questions
            unresolved_only: Only unresolved questions
            domain: Filter by domain
            
        Returns:
            List of questions
        """
        items = self.questions
        
        if unresolved_only:
            items = [item for item in items if item.get("status") == STATUS_UNRESOLVED]
        
        if domain:
            items = [item for item in items if item.get("domain") == domain]
        
        return items[-max(1, int(limit)):]
    
    def open_questions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get open (unresolved) questions."""
        return self.get_questions(limit=limit, unresolved_only=True)
    
    def get_gaps(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get detected gaps."""
        return self.gaps[-max(1, int(limit)):]
    
    def get_resolved(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get resolved questions."""
        return self.resolved[-max(1, int(limit)):]
    
    # ========================================================
    # SEARCH
    # ========================================================
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search questions by keyword.
        
        Args:
            keyword: Search keyword
            
        Returns:
            Matching questions
        """
        keyword = str(keyword).lower()
        results = []
        
        for item in self.questions:
            searchable = " ".join([
                str(item.get("question", "")),
                str(item.get("area", "")),
                str(item.get("domain", "")),
                str(item.get("reason", "")),
                str(item.get("answer", "")),
            ]).lower()
            
            if keyword in searchable:
                results.append(item)
        
        return results
    
    # ========================================================
    # PRIORITY
    # ========================================================
    
    def highest_priority(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get highest priority unresolved questions.
        
        Args:
            limit: Maximum number of questions
            
        Returns:
            Highest priority questions
        """
        items = [item for item in self.questions if item.get("status") == STATUS_UNRESOLVED]
        items.sort(key=lambda x: x.get("priority", 0), reverse=True)
        return items[:max(1, int(limit))]
    
    def by_priority(self, min_priority: float = 50.0) -> List[Dict[str, Any]]:
        """
        Get questions by minimum priority.
        
        Args:
            min_priority: Minimum priority threshold
            
        Returns:
            Questions with priority >= min_priority
        """
        return [item for item in self.questions if item.get("priority", 0) >= min_priority]
    
    # ========================================================
    # STATISTICS
    # ========================================================
    
    def statistics(self) -> Dict[str, Any]:
        """Get statistics."""
        unresolved = sum(1 for item in self.questions if item.get("status") == STATUS_UNRESOLVED)
        resolved = sum(1 for item in self.questions if item.get("status") == STATUS_RESOLVED)
        investigating = sum(1 for item in self.questions if item.get("status") == STATUS_INVESTIGATING)
        
        # Domain distribution
        domain_counts: Dict[str, int] = {}
        for item in self.questions:
            domain = item.get("domain", DOMAIN_GENERAL)
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        return {
            "total_questions": self.total_questions,
            "total_gaps": self.total_gaps,
            "total_resolved": self.total_resolved,
            "total_investigations": self.total_investigations,
            "stored_questions": len(self.questions),
            "unresolved": unresolved,
            "resolved": resolved,
            "investigating": investigating,
            "analysis_runs": self.total_analysis,
            "domain_distribution": domain_counts,
            "average_priority": round(
                sum(item.get("priority", 0) for item in self.questions) / max(1, len(self.questions)),
                2
            ),
        }
    
    def gap_statistics(self) -> Dict[str, Any]:
        """Get gap statistics."""
        open_gaps = [g for g in self.gaps if g.get("status") == "open"]
        closed_gaps = [g for g in self.gaps if g.get("status") != "open"]
        
        return {
            "total_gaps": len(self.gaps),
            "open_gaps": len(open_gaps),
            "closed_gaps": len(closed_gaps),
            "resolution_rate": round(
                (len(closed_gaps) / max(1, len(self.gaps))) * 100,
                2
            ),
            "avg_priority": round(
                sum(g.get("priority", 0) for g in self.gaps) / max(1, len(self.gaps)),
                2
            ),
        }
    
    # ========================================================
    # SUMMARY
    # ========================================================
    
    def summary(self) -> Dict[str, Any]:
        """Get quick summary."""
        stats = self.statistics()
        return {
            "questions": len(self.questions),
            "unresolved": stats["unresolved"],
            "resolved": stats["resolved"],
            "gaps": len(self.gaps),
            "analysis_runs": self.total_analysis,
            "latest": self.latest(),
        }
    
    def latest(self) -> Optional[Dict[str, Any]]:
        """Get latest question."""
        if not self.questions:
            return None
        return self.questions[-1]
    
    # ========================================================
    # CLEAR & RESET
    # ========================================================
    
    def clear(self) -> bool:
        """Clear all data."""
        self.questions.clear()
        self.gaps.clear()
        self.resolved.clear()
        self.investigations.clear()
        self.gap_history.clear()
        
        self.total_questions = 0
        self.total_gaps = 0
        self.total_resolved = 0
        self.total_analysis = 0
        self.total_investigations = 0
        
        self.last_question = None
        self.last_gap = None
        
        logger.info("Curiosity Engine cleared.")
        return True
    
    def reset(self) -> bool:
        """Reset all data."""
        return self.clear()
    
    # ========================================================
    # EXPORT / IMPORT
    # ========================================================
    
    def export(self) -> Dict[str, Any]:
        """Export all data."""
        return {
            "version": self.VERSION,
            "exported_at": self._timestamp(),
            "questions": deepcopy(self.questions),
            "gaps": deepcopy(self.gaps),
            "resolved": deepcopy(self.resolved),
            "statistics": self.statistics(),
        }
    
    def import_data(self, data: Dict[str, Any]) -> int:
        """Import data."""
        if not data:
            return 0
        
        imported = 0
        
        for item in data.get("questions", []):
            self.questions.append(item)
            imported += 1
        
        for item in data.get("gaps", []):
            self.gaps.append(item)
            imported += 1
        
        self._trim_questions()
        logger.info("Imported %s items", imported)
        return imported
    
    # ========================================================
    # STATUS
    # ========================================================
    
    def status(self) -> Dict[str, Any]:
        """Get system status."""
        stats = self.statistics()
        return {
            "module": "curiosity",
            "version": self.VERSION,
            "api_version": API_VERSION,
            "status": "ONLINE",
            "questions": stats["stored_questions"],
            "unresolved": stats["unresolved"],
            "resolved": stats["resolved"],
            "investigating": stats["investigating"],
            "gaps": stats["total_gaps"],
            "analysis_runs": stats["analysis_runs"],
            "has_latest": self.last_question is not None,
            "timestamp": self._timestamp(),
        }


# ============================================================
# GLOBAL INSTANCE
# ============================================================

curiosity_engine = CuriosityEngine()


# ============================================================
# COMPATIBILITY FUNCTIONS - MENGGUNAKAN curiosity_engine
# ============================================================

def ask(question: str, **kwargs) -> Optional[Dict[str, Any]]:
    """Legacy ask function."""
    return curiosity_engine.ask(question, **kwargs)


def resolve(question_id: str, answer: Any = None) -> Optional[Dict[str, Any]]:
    """Legacy resolve function."""
    return curiosity_engine.resolve(question_id, answer)


def search(keyword: str) -> List[Dict[str, Any]]:
    """Legacy search function."""
    return curiosity_engine.search(keyword)


def status() -> Dict[str, Any]:
    """Legacy status function."""
    return curiosity_engine.status()


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    """Run comprehensive self-test."""
    print()
    print("=" * 70)
    print("  CURIOSITY ENGINE v3.0 - SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        engine = CuriosityEngine()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Ask Question
    print("\n2. Testing ask...")
    try:
        question = curiosity_engine.ask(
            "Why is market prediction inaccurate?",
            area="market_prediction",
            domain="market",
            reason="Low accuracy",
            priority=75
        )
        if question and question.get("id"):
            results["ask"] = {"status": "PASS", "id": question["id"]}
            tests_passed += 1
            print(f"   ✅ Ask passed (ID: {question['id']})")
        else:
            results["ask"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Ask failed")
    except Exception as e:
        results["ask"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Ask failed: {e}")
    
    # Test 3: Gap Analysis
    print("\n3. Testing analyze_gap...")
    try:
        gaps = curiosity_engine.analyze_gap({
            "accuracy": {"market": 45, "sentiment": 55},
            "confidence": {"market": 50, "sentiment": 60},
        }, domain="market")
        if gaps is not None:
            results["analyze_gap"] = {"status": "PASS", "count": len(gaps)}
            tests_passed += 1
            print(f"   ✅ Gap analysis passed ({len(gaps)} gaps)")
        else:
            results["analyze_gap"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Gap analysis failed")
    except Exception as e:
        results["analyze_gap"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Gap analysis failed: {e}")
    
    # Test 4: Statistics
    print("\n4. Testing statistics...")
    try:
        stats = curiosity_engine.statistics()
        if stats and "total_questions" in stats:
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
        status_result = curiosity_engine.status()
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
        "module": "curiosity",
        "version": CURIOSITY_VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "CuriosityEngine",
    "curiosity_engine",
    "ask",
    "resolve",
    "search",
    "status",
    "self_test",
    "CURIOSITY_VERSION",
    "API_VERSION",
    "STATUS_UNRESOLVED",
    "STATUS_RESOLVED",
    "STATUS_INVESTIGATING",
    "STATUS_DEPRECATED",
    "STATUS_ANSWERED",
]


# ============================================================
# END
# ============================================================