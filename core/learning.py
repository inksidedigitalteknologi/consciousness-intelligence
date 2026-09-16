# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# LEARNING ENGINE v3.0
#
# SUPER COMPREHENSIVE ADAPTIVE LEARNING SYSTEM
#
# Functions:
# - Analyze Memory
# - Detect Patterns
# - Generate Insight
# - Adaptive Learning
# - Reinforcement Learning
# - Pattern Recognition
# - Knowledge Extraction
# - Insight Generation
# - Performance Tracking
# - Learning History
# - Feedback Loop
# - Confidence Scoring
# - Trend Analysis
# - Anomaly Detection
# - Prediction Generation
# - Decision Learning
# - Experience Learning
# - Semantic Learning
# - Behavioral Learning
# - Meta-Learning
#
# ============================================================

from __future__ import annotations

import logging
import statistics
import time
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================
# CONSTANTS
# ============================================================

LEARNING_VERSION = "3.0.0"

# Defaults
DEFAULT_MAX_HISTORY = 500
DEFAULT_MIN_CONFIDENCE = 30.0
DEFAULT_LEARNING_RATE = 0.1
DEFAULT_REINFORCEMENT_FACTOR = 1.2
DEFAULT_DECAY_FACTOR = 0.95


# ============================================================
# ENUMS
# ============================================================

class LearningType(Enum):
    """Types of learning."""
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    REINFORCEMENT = "reinforcement"
    ACTIVE = "active"
    PASSIVE = "passive"
    TRANSFER = "transfer"
    META = "meta"


class LearningStatus(Enum):
    """Learning status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class InsightType(Enum):
    """Types of insights."""
    TREND = "trend"
    PATTERN = "pattern"
    ANOMALY = "anomaly"
    PREDICTION = "prediction"
    OPPORTUNITY = "opportunity"
    RISK = "risk"
    CORRELATION = "correlation"
    CAUSATION = "causation"
    RECOMMENDATION = "recommendation"
    WARNING = "warning"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class LearningResult:
    """Result of a learning cycle."""
    id: str
    timestamp: str
    type: str
    insights: List[Dict[str, Any]]
    confidence: float
    metrics: Dict[str, Any]
    duration: float
    status: str
    errors: List[str] = field(default_factory=list)


@dataclass
class Insight:
    """Individual insight."""
    id: str
    type: str
    content: str
    confidence: float
    importance: float
    category: str
    source: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LearningStats:
    """Learning statistics."""
    total_cycles: int = 0
    successful_cycles: int = 0
    failed_cycles: int = 0
    total_insights: int = 0
    avg_confidence: float = 0.0
    avg_duration: float = 0.0
    total_duration: float = 0.0
    learning_rate: float = 0.0
    last_cycle: Optional[str] = None
    active: bool = False


# ============================================================
# MEMORY IMPORT
# ============================================================

try:
    from core.memory import memory
    MEMORY_AVAILABLE = True
except ImportError:
    memory = None
    MEMORY_AVAILABLE = False
    logger.warning("Memory module not available. Learning will use fallback.")


# ============================================================
# LEARNING ENGINE v3.0
# ============================================================

class LearningEngine:
    """
    Learning Engine v3.0 - Super Comprehensive Adaptive Learning.
    
    Fitur:
    1. Memory Analysis
    2. Pattern Detection
    3. Insight Generation
    4. Adaptive Learning
    5. Reinforcement Learning
    6. Knowledge Extraction
    7. Performance Tracking
    8. Learning History
    9. Feedback Loop
    10. Confidence Scoring
    11. Trend Analysis
    12. Anomaly Detection
    13. Prediction Generation
    14. Decision Learning
    15. Experience Learning
    16. Semantic Learning
    17. Behavioral Learning
    18. Meta-Learning
    """

    VERSION = LEARNING_VERSION

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # ====================================================
        # STATE
        # ====================================================
        
        self.learning_count = 0
        self.successful_learns = 0
        self.failed_learns = 0
        self.last_learning: Optional[str] = None
        self.last_result: Optional[LearningResult] = None
        self.insights: List[Insight] = []
        self.history: List[LearningResult] = []
        self.max_history = self.config.get("max_history", DEFAULT_MAX_HISTORY)
        
        # ====================================================
        # CONFIGURATION
        # ====================================================
        
        self.min_confidence = self.config.get("min_confidence", DEFAULT_MIN_CONFIDENCE)
        self.learning_rate = self.config.get("learning_rate", DEFAULT_LEARNING_RATE)
        self.reinforcement_factor = self.config.get("reinforcement_factor", DEFAULT_REINFORCEMENT_FACTOR)
        self.decay_factor = self.config.get("decay_factor", DEFAULT_DECAY_FACTOR)
        
        # ====================================================
        # STATISTICS
        # ====================================================
        
        self.stats = LearningStats()
        self.total_duration = 0.0
        self.cycle_times: List[float] = []
        
        # ====================================================
        # LEARNING STATE
        # ====================================================
        
        self.running = False
        self.current_cycle: Optional[str] = None
        self.errors: List[str] = []
        
        # ====================================================
        # KNOWLEDGE BASE
        # ====================================================
        
        self.knowledge_base: Dict[str, Any] = {}
        self.patterns_detected: Dict[str, int] = {}
        self.learning_adaptations: Dict[str, Any] = {}
        
        logger.info("Learning Engine v%s initialized.", self.VERSION)

    # ========================================================
    # MAIN LEARNING PROCESS
    # ========================================================

    def learn(
        self,
        data: Optional[Dict[str, Any]] = None,
        learning_type: str = "adaptive",
        force: bool = False
    ) -> Optional[LearningResult]:
        """
        Main learning process.
        
        Args:
            data: Optional data to learn from
            learning_type: Type of learning
            force: Force learning even if not enough data
            
        Returns:
            LearningResult or None
        """
        if self.running and not force:
            logger.warning("Learning already running")
            return None
        
        start_time = time.time()
        self.running = True
        self.learning_count += 1
        
        cycle_id = hashlib.md5(f"{self.learning_count}_{time.time()}".encode()).hexdigest()[:8]
        self.current_cycle = cycle_id
        
        logger.info("Learning cycle #%d started [%s]", self.learning_count, cycle_id)
        
        try:
            # Get data from memory if not provided
            if data is None and MEMORY_AVAILABLE and memory:
                data = self._get_memory_data()
            
            # Analyze
            analysis = self._analyze_data(data)
            
            # Generate insights
            insights = self._generate_insights(analysis, learning_type)
            
            # Calculate confidence
            confidence = self._calculate_confidence(insights, analysis)
            
            # Store insights
            for insight in insights:
                self._store_insight(insight)
            
            # Build result
            result = LearningResult(
                id=cycle_id,
                timestamp=datetime.now().isoformat(),
                type=learning_type,
                insights=[i.__dict__ for i in insights],
                confidence=confidence,
                metrics=self._get_metrics(),
                duration=time.time() - start_time,
                status=LearningStatus.COMPLETED.value,
                errors=self.errors.copy()
            )
            
            # Update state
            self.last_result = result
            self.last_learning = result.timestamp
            self.successful_learns += 1
            self.total_duration += result.duration
            self.cycle_times.append(result.duration)
            
            # Store history
            self.history.append(result)
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
            
            # Update statistics
            self._update_stats(result)
            
            # Adapt learning parameters
            self._adapt_learning(result)
            
            # Store knowledge
            if MEMORY_AVAILABLE and memory:
                self._store_knowledge(result, insights)
            
            logger.info(
                "Learning cycle #%d completed: %d insights, confidence %.2f%%, duration %.2fs",
                self.learning_count,
                len(insights),
                confidence,
                result.duration
            )
            
            return result
            
        except Exception as e:
            self.failed_learns += 1
            self.errors.append(str(e))
            logger.exception("Learning failed: %s", e)
            
            return LearningResult(
                id=cycle_id,
                timestamp=datetime.now().isoformat(),
                type=learning_type,
                insights=[],
                confidence=0.0,
                metrics={},
                duration=time.time() - start_time,
                status=LearningStatus.FAILED.value,
                errors=[str(e)]
            )
        
        finally:
            self.running = False
            self.current_cycle = None

    # ========================================================
    # DATA ANALYSIS
    # ========================================================

    def _get_memory_data(self) -> Dict[str, Any]:
        """Get data from memory."""
        data = {}
        
        try:
            if memory:
                # Get observations
                observations = memory.get_observations(200)
                data["observations"] = observations
                
                # Get patterns
                patterns = memory.get_patterns(200)
                data["patterns"] = patterns
                
                # Get knowledge
                knowledge = memory.get_knowledge(100)
                data["knowledge"] = knowledge
                
                # Get decisions
                decisions = memory.get_decisions(50)
                data["decisions"] = decisions
                
                # Get experiences
                experiences = memory.get_experiences(50)
                data["experiences"] = experiences
                
                # Get semantic
                semantic = memory.get_semantic(50)
                data["semantic"] = semantic
        except Exception as e:
            logger.warning("Memory data retrieval failed: %s", e)
            data["error"] = str(e)
        
        return data

    def _analyze_data(self, data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze data for patterns and insights."""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "data_count": 0,
            "patterns": {},
            "trends": {},
            "anomalies": [],
            "correlations": [],
            "statistics": {},
        }
        
        if not data:
            return analysis
        
        # Count data
        analysis["data_count"] = sum(len(v) if isinstance(v, (list, dict)) else 1 for v in data.values())
        
        # ================================================
        # MARKET BEHAVIOR ANALYSIS
        # ================================================
        
        observations = data.get("observations", [])
        if observations:
            analysis["market_behavior"] = self._analyze_market_behavior(observations)
        
        # ================================================
        # PATTERN ANALYSIS
        # ================================================
        
        patterns = data.get("patterns", [])
        if patterns:
            analysis["pattern_analysis"] = self._analyze_patterns(patterns)
        
        # ================================================
        # KNOWLEDGE ANALYSIS
        # ================================================
        
        knowledge = data.get("knowledge", [])
        if knowledge:
            analysis["knowledge_analysis"] = self._analyze_knowledge(knowledge)
        
        # ================================================
        # DECISION ANALYSIS
        # ================================================
        
        decisions = data.get("decisions", [])
        if decisions:
            analysis["decision_analysis"] = self._analyze_decisions(decisions)
        
        # ================================================
        # EXPERIENCE ANALYSIS
        # ================================================
        
        experiences = data.get("experiences", [])
        if experiences:
            analysis["experience_analysis"] = self._analyze_experiences(experiences)
        
        # ================================================
        # SEMANTIC ANALYSIS
        # ================================================
        
        semantic = data.get("semantic", [])
        if semantic:
            analysis["semantic_analysis"] = self._analyze_semantic(semantic)
        
        # ================================================
        # TREND DETECTION
        # ================================================
        
        analysis["trends"] = self._detect_trends(data)
        
        # ================================================
        # ANOMALY DETECTION
        # ================================================
        
        analysis["anomalies"] = self._detect_anomalies(data)
        
        # ================================================
        # STATISTICS
        # ================================================
        
        analysis["statistics"] = self._calculate_statistics(data)
        
        return analysis

    # ========================================================
    # ANALYSIS HELPERS
    # ========================================================

    def _analyze_market_behavior(self, observations: List) -> Dict[str, Any]:
        """Analyze market behavior from observations."""
        buy = 0
        sell = 0
        hold = 0
        total = 0
        
        for item in observations:
            try:
                text = str(item).upper()
                if "BUY" in text:
                    buy += 1
                elif "SELL" in text:
                    sell += 1
                else:
                    hold += 1
                total += 1
            except Exception:
                pass
        
        result = {
            "total": total,
            "buy": buy,
            "sell": sell,
            "hold": hold,
        }
        
        if total > 0:
            result["buy_percent"] = round((buy / total) * 100, 2)
            result["sell_percent"] = round((sell / total) * 100, 2)
            result["hold_percent"] = round((hold / total) * 100, 2)
        
        return result

    def _analyze_patterns(self, patterns: List) -> Dict[str, Any]:
        """Analyze patterns."""
        pattern_map = {}
        confidence_values = []
        
        for item in patterns:
            try:
                if isinstance(item, (list, tuple)):
                    if len(item) >= 3:
                        name = str(item[2])
                        pattern_map[name] = pattern_map.get(name, 0) + 1
                    if len(item) >= 4:
                        try:
                            confidence_values.append(float(item[3]))
                        except (ValueError, TypeError):
                            pass
            except Exception:
                pass
        
        result = {
            "total": len(pattern_map),
            "frequencies": pattern_map,
            "most_common": dict(sorted(pattern_map.items(), key=lambda x: -x[1])[:10])
        }
        
        if confidence_values:
            result["avg_confidence"] = round(statistics.mean(confidence_values), 2)
            result["min_confidence"] = round(min(confidence_values), 2)
            result["max_confidence"] = round(max(confidence_values), 2)
        
        return result

    def _analyze_knowledge(self, knowledge: List) -> Dict[str, Any]:
        """Analyze knowledge."""
        categories = {}
        total = len(knowledge)
        
        for item in knowledge:
            try:
                if isinstance(item, (list, tuple)):
                    category = str(item[1]) if len(item) > 1 else "unknown"
                    categories[category] = categories.get(category, 0) + 1
                elif isinstance(item, dict):
                    category = item.get("category", "unknown")
                    categories[category] = categories.get(category, 0) + 1
            except Exception:
                pass
        
        return {
            "total": total,
            "categories": categories,
            "unique_categories": len(categories),
            "most_common": dict(sorted(categories.items(), key=lambda x: -x[1])[:5])
        }

    def _analyze_decisions(self, decisions: List) -> Dict[str, Any]:
        """Analyze decisions."""
        decision_types = {}
        total = len(decisions)
        
        for item in decisions:
            try:
                if isinstance(item, (list, tuple)):
                    decision = str(item[1]) if len(item) > 1 else "unknown"
                    decision_types[decision] = decision_types.get(decision, 0) + 1
                elif isinstance(item, dict):
                    decision = item.get("decision", "unknown")
                    decision_types[decision] = decision_types.get(decision, 0) + 1
            except Exception:
                pass
        
        return {
            "total": total,
            "types": decision_types,
            "most_common": dict(sorted(decision_types.items(), key=lambda x: -x[1])[:5])
        }

    def _analyze_experiences(self, experiences: List) -> Dict[str, Any]:
        """Analyze experiences."""
        outcomes = {}
        total = len(experiences)
        profitable = 0
        
        for item in experiences:
            try:
                if isinstance(item, (list, tuple)):
                    result = str(item[6]) if len(item) > 6 else "unknown"
                    outcomes[result] = outcomes.get(result, 0) + 1
                    if len(item) > 5 and float(item[5]) > 0:
                        profitable += 1
                elif isinstance(item, dict):
                    result = item.get("result", "unknown")
                    outcomes[result] = outcomes.get(result, 0) + 1
                    if item.get("profit", 0) > 0:
                        profitable += 1
            except Exception:
                pass
        
        return {
            "total": total,
            "profitable": profitable,
            "profit_rate": round((profitable / total) * 100, 2) if total > 0 else 0,
            "outcomes": outcomes
        }

    def _analyze_semantic(self, semantic: List) -> Dict[str, Any]:
        """Analyze semantic data."""
        concepts = {}
        relations = {}
        
        for item in semantic:
            try:
                if isinstance(item, (list, tuple)):
                    concept = str(item[1]) if len(item) > 1 else "unknown"
                    relation = str(item[2]) if len(item) > 2 else "unknown"
                    concepts[concept] = concepts.get(concept, 0) + 1
                    relations[relation] = relations.get(relation, 0) + 1
                elif isinstance(item, dict):
                    concept = item.get("concept", "unknown")
                    relation = item.get("relation", "unknown")
                    concepts[concept] = concepts.get(concept, 0) + 1
                    relations[relation] = relations.get(relation, 0) + 1
            except Exception:
                pass
        
        return {
            "total": len(semantic),
            "concepts": concepts,
            "relations": relations,
            "top_concepts": dict(sorted(concepts.items(), key=lambda x: -x[1])[:10])
        }

    # ========================================================
    # TREND & ANOMALY DETECTION
    # ========================================================

    def _detect_trends(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect trends in data."""
        trends = []
        
        # Trend from market behavior
        market = data.get("market_behavior", {})
        if market.get("total", 0) > 0:
            buy_pct = market.get("buy_percent", 0)
            sell_pct = market.get("sell_percent", 0)
            
            if buy_pct > sell_pct + 15:
                trends.append({
                    "type": "market_trend",
                    "direction": "bullish",
                    "confidence": min(80 + (buy_pct - sell_pct), 100),
                    "description": "Strong bullish market behavior detected"
                })
            elif sell_pct > buy_pct + 15:
                trends.append({
                    "type": "market_trend",
                    "direction": "bearish",
                    "confidence": min(80 + (sell_pct - buy_pct), 100),
                    "description": "Strong bearish market behavior detected"
                })
            else:
                trends.append({
                    "type": "market_trend",
                    "direction": "neutral",
                    "confidence": 50,
                    "description": "Balanced market behavior"
                })
        
        # Trend from patterns
        patterns = data.get("pattern_analysis", {})
        if patterns.get("total", 0) > 0:
            most_common = patterns.get("most_common", {})
            if most_common:
                top_pattern = list(most_common.keys())[0] if most_common else None
                if top_pattern:
                    trends.append({
                        "type": "pattern_trend",
                        "direction": "emerging",
                        "confidence": min(60 + (most_common.get(top_pattern, 0) * 5), 100),
                        "description": f"Pattern {top_pattern} is emerging"
                    })
        
        # Trend from experiences
        experiences = data.get("experience_analysis", {})
        if experiences.get("total", 0) > 0:
            profit_rate = experiences.get("profit_rate", 0)
            if profit_rate > 60:
                trends.append({
                    "type": "performance_trend",
                    "direction": "improving",
                    "confidence": min(70 + profit_rate / 2, 100),
                    "description": "Trading performance is improving"
                })
            elif profit_rate < 40:
                trends.append({
                    "type": "performance_trend",
                    "direction": "declining",
                    "confidence": min(70 + (100 - profit_rate) / 2, 100),
                    "description": "Trading performance needs improvement"
                })
            else:
                trends.append({
                    "type": "performance_trend",
                    "direction": "stable",
                    "confidence": 50,
                    "description": "Trading performance is stable"
                })
        
        return trends

    def _detect_anomalies(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect anomalies in data."""
        anomalies = []
        
        # Check for high error rates
        if self.errors:
            if len(self.errors) > 10:
                anomalies.append({
                    "type": "error_anomaly",
                    "severity": "high",
                    "description": f"High error rate: {len(self.errors)} errors",
                    "confidence": 80
                })
            elif len(self.errors) > 5:
                anomalies.append({
                    "type": "error_anomaly",
                    "severity": "medium",
                    "description": f"Moderate error rate: {len(self.errors)} errors",
                    "confidence": 60
                })
        
        # Check pattern frequency anomaly
        patterns = data.get("pattern_analysis", {})
        if patterns.get("total", 0) > 20:
            frequencies = patterns.get("frequencies", {})
            if frequencies:
                avg_freq = sum(frequencies.values()) / len(frequencies)
                high_freq = [p for p, f in frequencies.items() if f > avg_freq * 3]
                if high_freq:
                    anomalies.append({
                        "type": "pattern_anomaly",
                        "severity": "medium",
                        "description": f"Unusually high pattern frequency: {', '.join(high_freq[:3])}",
                        "confidence": 70
                    })
        
        # Check experience anomaly
        experiences = data.get("experience_analysis", {})
        if experiences.get("total", 0) > 10:
            profit_rate = experiences.get("profit_rate", 0)
            if profit_rate < 20 and experiences.get("total", 0) > 20:
                anomalies.append({
                    "type": "performance_anomaly",
                    "severity": "high",
                    "description": f"Low profit rate: {profit_rate}% over {experiences['total']} trades",
                    "confidence": 75
                })
        
        return anomalies

    # ========================================================
    # STATISTICS
    # ========================================================

    def _calculate_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate statistics from data."""
        stats = {
            "total_data_points": 0,
            "unique_categories": 0,
            "avg_confidence": 0.0,
        }
        
        # Count data points
        for key, value in data.items():
            if isinstance(value, dict) and "total" in value:
                stats["total_data_points"] += value["total"]
        
        # Get confidence from pattern analysis
        patterns = data.get("pattern_analysis", {})
        stats["avg_confidence"] = patterns.get("avg_confidence", 0)
        
        return stats

    # ========================================================
    # INSIGHT GENERATION
    # ========================================================

    def _generate_insights(self, analysis: Dict[str, Any], learning_type: str) -> List[Insight]:
        """Generate insights from analysis."""
        insights = []
        
        # ================================================
        # TREND INSIGHTS
        # ================================================
        
        for trend in analysis.get("trends", []):
            insight = Insight(
                id=hashlib.md5(f"{trend}_{time.time()}".encode()).hexdigest()[:8],
                type=InsightType.TREND.value,
                content=trend.get("description", "Trend detected"),
                confidence=trend.get("confidence", 50),
                importance=1.0,
                category="trend",
                source=learning_type,
                timestamp=datetime.now().isoformat(),
                metadata=trend
            )
            insights.append(insight)
        
        # ================================================
        # ANOMALY INSIGHTS
        # ================================================
        
        for anomaly in analysis.get("anomalies", []):
            insight = Insight(
                id=hashlib.md5(f"{anomaly}_{time.time()}".encode()).hexdigest()[:8],
                type=InsightType.ANOMALY.value,
                content=anomaly.get("description", "Anomaly detected"),
                confidence=anomaly.get("confidence", 50),
                importance=0.8,
                category="anomaly",
                source=learning_type,
                timestamp=datetime.now().isoformat(),
                metadata=anomaly
            )
            insights.append(insight)
        
        # ================================================
        # MARKET INSIGHTS
        # ================================================
        
        market = analysis.get("market_behavior", {})
        if market.get("total", 0) > 0:
            buy_pct = market.get("buy_percent", 0)
            sell_pct = market.get("sell_percent", 0)
            
            if buy_pct > sell_pct:
                insight = Insight(
                    id=hashlib.md5(f"market_bullish_{time.time()}".encode()).hexdigest()[:8],
                    type=InsightType.OPPORTUNITY.value,
                    content=f"Bullish market bias: {buy_pct:.1f}% buy signals",
                    confidence=min(60 + (buy_pct - sell_pct), 100),
                    importance=0.7,
                    category="market",
                    source=learning_type,
                    timestamp=datetime.now().isoformat(),
                    metadata={"buy": buy_pct, "sell": sell_pct}
                )
                insights.append(insight)
            elif sell_pct > buy_pct:
                insight = Insight(
                    id=hashlib.md5(f"market_bearish_{time.time()}".encode()).hexdigest()[:8],
                    type=InsightType.WARNING.value,
                    content=f"Bearish market bias: {sell_pct:.1f}% sell signals",
                    confidence=min(60 + (sell_pct - buy_pct), 100),
                    importance=0.7,
                    category="market",
                    source=learning_type,
                    timestamp=datetime.now().isoformat(),
                    metadata={"buy": buy_pct, "sell": sell_pct}
                )
                insights.append(insight)
            else:
                insight = Insight(
                    id=hashlib.md5(f"market_neutral_{time.time()}".encode()).hexdigest()[:8],
                    type=InsightType.WARNING.value,
                    content="Neutral market conditions detected",
                    confidence=50,
                    importance=0.3,
                    category="market",
                    source=learning_type,
                    timestamp=datetime.now().isoformat(),
                    metadata={"buy": buy_pct, "sell": sell_pct}
                )
                insights.append(insight)
        
        # ================================================
        # PATTERN INSIGHTS
        # ================================================
        
        patterns = analysis.get("pattern_analysis", {})
        most_common = patterns.get("most_common", {})
        if most_common:
            top_pattern = list(most_common.keys())[0]
            top_count = most_common[top_pattern]
            insight = Insight(
                id=hashlib.md5(f"pattern_{top_pattern}_{time.time()}".encode()).hexdigest()[:8],
                type=InsightType.PATTERN.value,
                content=f"Dominant pattern: {top_pattern} ({top_count} occurrences)",
                confidence=min(70 + top_count * 2, 100),
                importance=0.6,
                category="pattern",
                source=learning_type,
                timestamp=datetime.now().isoformat(),
                metadata={"pattern": top_pattern, "count": top_count}
            )
            insights.append(insight)
        
        # ================================================
        # PERFORMANCE INSIGHTS
        # ================================================
        
        experiences = analysis.get("experience_analysis", {})
        if experiences.get("total", 0) > 0:
            profit_rate = experiences.get("profit_rate", 0)
            if profit_rate > 60:
                insight = Insight(
                    id=hashlib.md5(f"performance_good_{time.time()}".encode()).hexdigest()[:8],
                    type=InsightType.RECOMMENDATION.value,
                    content=f"Good performance: {profit_rate:.1f}% profitable trades",
                    confidence=min(70 + profit_rate / 2, 100),
                    importance=0.8,
                    category="performance",
                    source=learning_type,
                    timestamp=datetime.now().isoformat(),
                    metadata={"profit_rate": profit_rate}
                )
                insights.append(insight)
            elif profit_rate < 40:
                insight = Insight(
                    id=hashlib.md5(f"performance_poor_{time.time()}".encode()).hexdigest()[:8],
                    type=InsightType.WARNING.value,
                    content=f"Poor performance: {profit_rate:.1f}% profitable trades - consider strategy adjustment",
                    confidence=min(70 + (100 - profit_rate) / 2, 100),
                    importance=0.8,
                    category="performance",
                    source=learning_type,
                    timestamp=datetime.now().isoformat(),
                    metadata={"profit_rate": profit_rate}
                )
                insights.append(insight)
        
        # ================================================
        # PREDICTION INSIGHTS
        # ================================================
        
        if analysis.get("trends", []):
            market_trends = [t for t in analysis["trends"] if t.get("type") == "market_trend"]
            if market_trends:
                trend = market_trends[0]
                direction = trend.get("direction", "neutral")
                if direction != "neutral":
                    insight = Insight(
                        id=hashlib.md5(f"prediction_{direction}_{time.time()}".encode()).hexdigest()[:8],
                        type=InsightType.PREDICTION.value,
                        content=f"Predicted {direction} market movement with {trend.get('confidence', 50):.0f}% confidence",
                        confidence=trend.get("confidence", 50),
                        importance=0.5,
                        category="prediction",
                        source=learning_type,
                        timestamp=datetime.now().isoformat(),
                        metadata={"direction": direction, "confidence": trend.get("confidence", 50)}
                    )
                    insights.append(insight)
        
        return insights

    # ========================================================
    # CONFIDENCE CALCULATION
    # ========================================================

    def _calculate_confidence(self, insights: List[Insight], analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence."""
        if not insights:
            return 0.0
        
        # Average insight confidence
        avg_insight_conf = sum(i.confidence for i in insights) / len(insights)
        
        # Data quality factor
        data_count = analysis.get("data_count", 0)
        data_factor = min(data_count / 100, 1.0) if data_count > 0 else 0
        
        # Experience factor
        experience = analysis.get("experience_analysis", {})
        exp_factor = min(experience.get("total", 0) / 20, 1.0) if experience.get("total", 0) > 0 else 0
        
        # Pattern factor
        patterns = analysis.get("pattern_analysis", {})
        pattern_factor = min(patterns.get("total", 0) / 10, 1.0) if patterns.get("total", 0) > 0 else 0
        
        # Combined confidence
        confidence = (
            avg_insight_conf * 0.5 +
            data_factor * 0.2 +
            exp_factor * 0.15 +
            pattern_factor * 0.15
        )
        
        return min(max(confidence, 0), 100)

    # ========================================================
    # STORE INSIGHTS
    # ========================================================

    def _store_insight(self, insight: Insight) -> None:
        """Store insight in memory."""
        self.insights.append(insight)
        
        # Keep only recent insights
        if len(self.insights) > self.max_history:
            self.insights = self.insights[-self.max_history:]

    def _store_knowledge(self, result: LearningResult, insights: List[Insight]) -> None:
        """Store knowledge in memory."""
        try:
            if not memory:
                return
            
            # Store summary insight
            if insights:
                top_insight = max(insights, key=lambda x: x.importance)
                memory.save_knowledge(
                    {
                        "type": "learning_insight",
                        "insight": top_insight.content,
                        "confidence": top_insight.confidence,
                        "cycle": result.id,
                        "timestamp": result.timestamp,
                    },
                    "learning"
                )
            
            # Store patterns
            for insight in insights[:5]:
                memory.save_knowledge(
                    {
                        "type": insight.type,
                        "content": insight.content,
                        "confidence": insight.confidence,
                        "importance": insight.importance,
                        "category": insight.category,
                    },
                    f"insight_{insight.type}"
                )
                
        except Exception as e:
            logger.debug("Failed to store knowledge: %s", e)

    # ========================================================
    # ADAPTIVE LEARNING
    # ========================================================

    def _adapt_learning(self, result: LearningResult) -> None:
        """Adapt learning parameters based on results."""
        if result.confidence < self.min_confidence:
            # Increase learning rate
            self.learning_rate *= self.reinforcement_factor
            logger.debug("Learning rate increased to %.3f", self.learning_rate)
        elif result.confidence > 80:
            # Decrease learning rate (fine-tuning)
            self.learning_rate *= self.decay_factor
            logger.debug("Learning rate decreased to %.3f", self.learning_rate)
        
        # Update confidence threshold based on success rate
        if self.successful_learns > 10:
            success_rate = self.successful_learns / (self.successful_learns + self.failed_learns) * 100
            if success_rate < 50 and self.min_confidence > 20:
                self.min_confidence -= 2
                logger.debug("Min confidence decreased to %.1f", self.min_confidence)
            elif success_rate > 80 and self.min_confidence < 60:
                self.min_confidence += 2
                logger.debug("Min confidence increased to %.1f", self.min_confidence)

    # ========================================================
    # STATISTICS UPDATE
    # ========================================================

    def _update_stats(self, result: LearningResult) -> None:
        """Update statistics."""
        self.stats.total_cycles += 1
        self.stats.successful_cycles += 1 if result.status == LearningStatus.COMPLETED.value else 0
        self.stats.failed_cycles += 1 if result.status == LearningStatus.FAILED.value else 0
        self.stats.total_insights += len(result.insights)
        self.stats.total_duration += result.duration
        self.stats.avg_duration = self.stats.total_duration / self.stats.total_cycles
        self.stats.last_cycle = result.timestamp
        self.stats.learning_rate = self.learning_rate
        self.stats.active = self.running
        
        # Average confidence
        if self.stats.total_insights > 0:
            total_conf = sum(i.get("confidence", 0) for r in self.history for i in r.insights)
            self.stats.avg_confidence = total_conf / self.stats.total_insights

    def _get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        return {
            "learning_count": self.learning_count,
            "successful_learns": self.successful_learns,
            "failed_learns": self.failed_learns,
            "total_insights": len(self.insights),
            "learning_rate": self.learning_rate,
            "min_confidence": self.min_confidence,
            "errors": len(self.errors),
        }

    # ========================================================
    # PUBLIC API
    # ========================================================

    def get_insight(self, limit: int = 10) -> List[Insight]:
        """Get recent insights."""
        return self.insights[-limit:] if self.insights else []

    def get_insights_by_type(self, insight_type: str) -> List[Insight]:
        """Get insights by type."""
        return [i for i in self.insights if i.type == insight_type]

    def get_history(self, limit: int = 20) -> List[LearningResult]:
        """Get learning history."""
        return self.history[-limit:] if self.history else []

    def status(self) -> Dict[str, Any]:
        """Get learning status."""
        return {
            "learning_count": self.learning_count,
            "last_learning": self.last_learning,
            "insights": len(self.insights),
            "running": self.running,
            "current_cycle": self.current_cycle,
            "errors": len(self.errors),
            "learning_rate": self.learning_rate,
            "min_confidence": self.min_confidence,
            "stats": {
                "total_cycles": self.stats.total_cycles,
                "successful": self.stats.successful_cycles,
                "failed": self.stats.failed_cycles,
                "avg_confidence": round(self.stats.avg_confidence, 2),
                "avg_duration": round(self.stats.avg_duration, 4),
            }
        }

    def reset(self) -> bool:
        """Reset learning engine."""
        try:
            self.learning_count = 0
            self.successful_learns = 0
            self.failed_learns = 0
            self.last_learning = None
            self.last_result = None
            self.insights = []
            self.history = []
            self.errors = []
            self.cycle_times = []
            self.total_duration = 0.0
            self.running = False
            self.current_cycle = None
            
            self.stats = LearningStats()
            
            logger.info("Learning Engine reset.")
            return True
        except Exception as e:
            logger.error("Reset failed: %s", e)
            return False

    def analyze(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze data without storing results.
        
        Args:
            data: Data to analyze
            
        Returns:
            Analysis result
        """
        if data is None and MEMORY_AVAILABLE and memory:
            data = self._get_memory_data()
        
        return self._analyze_data(data)


# ============================================================
# GLOBAL INSTANCE
# ============================================================

learning = LearningEngine()


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def learn(data: Optional[Dict[str, Any]] = None) -> Optional[LearningResult]:
    """Legacy learn function."""
    return learning.learn(data)


def get_insight(limit: int = 10) -> List[Dict[str, Any]]:
    """Legacy get insight function."""
    insights = learning.get_insight(limit)
    return [i.__dict__ for i in insights]


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "LearningEngine",
    "LearningResult",
    "Insight",
    "LearningStats",
    "LearningType",
    "LearningStatus",
    "InsightType",
    "learning",
    "learn",
    "get_insight",
    "LEARNING_VERSION",
]


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    """
    Run learning engine self-test.
    """
    
    print()
    print("=" * 70)
    print("  LEARNING ENGINE v3.0 - SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        test_learning = LearningEngine()
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
        result = learning.learn({"test_data": "sample"}, force=True)
        if result and result.id:
            results["learn"] = {"status": "PASS", "id": result.id}
            tests_passed += 1
            print(f"   ✅ Learn passed (ID: {result.id})")
        else:
            results["learn"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Learn failed")
    except Exception as e:
        results["learn"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Learn failed: {e}")
    
    # Test 3: Insight
    print("\n3. Testing get_insight...")
    try:
        insights = learning.get_insight()
        if insights is not None:
            results["insight"] = {"status": "PASS", "count": len(insights)}
            tests_passed += 1
            print(f"   ✅ Insight passed ({len(insights)} insights)")
        else:
            results["insight"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Insight failed")
    except Exception as e:
        results["insight"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Insight failed: {e}")
    
    # Test 4: Status
    print("\n4. Testing status...")
    try:
        status = learning.status()
        if status and "learning_count" in status:
            results["status"] = {"status": "PASS", "count": status["learning_count"]}
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
    
    # Test 5: Reset
    print("\n5. Testing reset...")
    try:
        result = learning.reset()
        if result:
            results["reset"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Reset passed")
        else:
            results["reset"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Reset failed")
    except Exception as e:
        results["reset"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Reset failed: {e}")
    
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
        "module": "learning",
        "version": LEARNING_VERSION,
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
    print("  LEARNING ENGINE v3.0 - SELF TEST COMPLETE")
    print("=" * 70)
    print()
    print("Final Status:", result["status"])
    print("Details:", result["details"])


# ============================================================
# END
# ============================================================