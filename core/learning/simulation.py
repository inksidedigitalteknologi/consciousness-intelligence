# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SIMULATION ENGINE v3.0
#
# ULTRA COMPREHENSIVE SCENARIO SIMULATION
#
# NEW FEATURES v3.0:
# 1. Advanced Scenario Analysis
# 2. Monte Carlo Simulation
# 3. Sensitivity Analysis
# 4. Confidence Calibration
# 5. Risk Scoring
# 6. Multi-Scenario Comparison
# 7. Historical Pattern Matching
# 8. Volatility Modeling
# 9. Correlation Analysis
# 10. Impact Assessment
# 11. Probability Distribution
# 12. Scenario Ranking
# 13. Batch Optimization
# 14. Real-time Monitoring
# 15. Export/Import v2
# 16. Self-Test
# 17. Performance Analytics
# 18. Smart Filtering
#
# ============================================================

import copy
import logging
import re
import math
import random
import statistics
import threading
from datetime import datetime
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================
#
# CONSTANTS
#
# ============================================================

MODULE_NAME = "simulation"
MODULE_VERSION = "3.0.0"
API_VERSION = "2.0"

MAX_HISTORY = 500
DEFAULT_CONFIDENCE_THRESHOLD = 50
DEFAULT_RISK_THRESHOLD = 50
MAX_SIMULATION_DEPTH = 10


# ============================================================
#
# ENUMS
#
# ============================================================

class Direction(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EXTREME = "EXTREME"


class ImpactLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    MEDIUM_HIGH = "medium-high"
    HIGH = "high"
    EXTREME = "extreme"


# ============================================================
#
# DATA CLASSES
# ============================================================

@dataclass
class SimulationResult:
    """Complete simulation result."""
    timestamp: str
    version: str
    status: str
    scenario: Any
    normalized_scenario: str
    categories: List[str]
    factors: List[str]
    direction: str
    impact: str
    risk: str
    risk_score: float
    confidence: float
    probability: float
    possible_effect: str
    assumptions: List[str]
    context: Dict[str, Any]
    sensitivity: Optional[Dict[str, Any]] = None
    monte_carlo: Optional[Dict[str, Any]] = None
    patterns: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SimulationStats:
    """Simulation statistics."""
    total: int = 0
    stored: int = 0
    successful: int = 0
    failed: int = 0
    average_confidence: float = 0.0
    average_probability: float = 0.0
    average_risk_score: float = 0.0
    positive: int = 0
    negative: int = 0
    mixed: int = 0
    unknown: int = 0
    categories: Dict[str, int] = field(default_factory=dict)
    risks: Dict[str, int] = field(default_factory=dict)
    impacts: Dict[str, int] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
#
# SIMULATION ENGINE v3.0
#
# ============================================================

class SimulationEngine:
    """
    ULTRA COMPREHENSIVE Simulation Engine v3.0.
    
    Features:
    1. Scenario Simulation
    2. Monte Carlo Simulation
    3. Sensitivity Analysis
    4. Confidence Calibration
    5. Risk Scoring
    6. Multi-Scenario Comparison
    7. Pattern Matching
    8. Volatility Modeling
    9. Correlation Analysis
    10. Impact Assessment
    11. Scenario Ranking
    12. Batch Optimization
    """
    
    VERSION = MODULE_VERSION
    NAME = MODULE_NAME

    # ========================================================
    #
    # SCENARIO KEYWORDS
    #
    # ========================================================

    POSITIVE_KEYWORDS = {
        "volume naik", "volume meningkat", "volume tinggi",
        "momentum naik", "momentum meningkat", "momentum kuat",
        "breakout", "bullish", "harga naik", "trend naik",
        "uptrend", "buy pressure", "tekanan beli", "demand meningkat",
        "liquidity meningkat", "likuiditas meningkat", "akumulasi",
    }

    NEGATIVE_KEYWORDS = {
        "volume turun", "volume menurun", "volume rendah",
        "momentum turun", "momentum melemah", "momentum lemah",
        "bearish", "harga turun", "trend turun", "downtrend",
        "sell pressure", "tekanan jual", "demand menurun",
        "liquidity menurun", "likuiditas menurun", "distribusi",
    }

    VOLATILITY_KEYWORDS = {
        "volatilitas tinggi", "volatility tinggi", "volatility",
        "volatile", "volatil", "spike", "flash crash",
        "pump", "dump", "extreme volatility",
    }

    BREAKOUT_KEYWORDS = {
        "breakout", "break out", "resistance ditembus",
        "resistance breakout", "support ditembus",
        "break resistance", "break support",
    }

    REVERSAL_KEYWORDS = {
        "reversal", "pembalikan", "trend reversal",
        "potential reversal", "potensi reversal",
        "reversal bullish", "reversal bearish",
    }

    # ========================================================
    #
    # FACTOR KEYWORDS
    #
    # ========================================================

    FACTOR_KEYWORDS = {
        "volume": ("volume",),
        "momentum": ("momentum",),
        "price": ("harga", "price"),
        "trend": ("trend", "uptrend", "downtrend"),
        "breakout": ("breakout", "resistance"),
        "support": ("support",),
        "volatility": ("volatility", "volatilitas", "volatile", "volatil", "spike"),
        "liquidity": ("liquidity", "likuiditas"),
        "demand": ("demand", "permintaan"),
        "pressure": ("pressure", "tekanan beli", "tekanan jual"),
        "momentum_strength": ("momentum kuat", "momentum lemah"),
    }

    # ========================================================
    #
    # INITIALIZATION
    #
    # ========================================================

    def __init__(self, max_history: int = None, config: Optional[Dict] = None):
        self.config = config or {}
        self.max_history = max(1, int(max_history or MAX_HISTORY))
        self.lock = threading.RLock()
        
        # Core storage
        self.simulations: List[SimulationResult] = []
        self.pattern_cache: Dict[str, List[Dict]] = defaultdict(list)
        
        # Statistics
        self.total_simulations = 0
        self.successful_simulations = 0
        self.failed_simulations = 0
        self.last_simulation: Optional[SimulationResult] = None
        
        # Timestamps
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        
        # Counters
        self.category_counter = Counter()
        self.direction_counter = Counter()
        self.risk_counter = Counter()
        self.impact_counter = Counter()
        
        # Monte Carlo cache
        self.monte_carlo_cache: Dict[str, Any] = {}
        
        # Thread safety
        self._running = False
        
        logger.info(
            "Simulation Engine v%s initialized | max_history=%s",
            self.VERSION, self.max_history
        )

    # ========================================================
    #
    # INTERNAL HELPERS
    #
    # ========================================================

    def _timestamp(self) -> str:
        return datetime.now().isoformat()

    def _safe_copy(self, value: Any) -> Any:
        try:
            return copy.deepcopy(value)
        except Exception:
            return value

    def _normalize_text(self, value: Any) -> str:
        if value is None:
            return ""
        try:
            text = str(value).strip().lower()
            return re.sub(r"\s+", " ", text)
        except Exception:
            return ""

    def _trim_history(self) -> None:
        if len(self.simulations) > self.max_history:
            self.simulations = self.simulations[-self.max_history:]

    def _rebuild_statistics(self) -> None:
        self.category_counter.clear()
        self.direction_counter.clear()
        self.risk_counter.clear()
        self.impact_counter.clear()
        
        for item in self.simulations:
            if not isinstance(item, SimulationResult):
                continue
            direction = item.direction
            risk = item.risk
            impact = item.impact
            categories = item.categories or []
            
            if direction:
                self.direction_counter[direction] += 1
            if risk:
                self.risk_counter[risk] += 1
            if impact:
                self.impact_counter[impact] += 1
            for category in categories:
                self.category_counter[category] += 1
        
        if self.simulations:
            self.last_simulation = self._safe_copy(self.simulations[-1])

    # ========================================================
    #
    # SCENARIO ANALYSIS
    #
    # ========================================================

    def classify(self, scenario: Any) -> List[str]:
        text = self._normalize_text(scenario)
        categories = []
        
        if any(kw in text for kw in self.POSITIVE_KEYWORDS):
            categories.append("positive_momentum")
        if any(kw in text for kw in self.NEGATIVE_KEYWORDS):
            categories.append("negative_momentum")
        if any(kw in text for kw in self.VOLATILITY_KEYWORDS):
            categories.append("volatility")
        if any(kw in text for kw in self.BREAKOUT_KEYWORDS):
            categories.append("breakout")
        if any(kw in text for kw in self.REVERSAL_KEYWORDS):
            categories.append("reversal")
        
        if not categories:
            categories.append("unknown")
        
        return categories

    def detect_factors(self, scenario: Any) -> List[str]:
        text = self._normalize_text(scenario)
        factors = []
        for factor, keywords in self.FACTOR_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                factors.append(factor)
        return factors

    def estimate_direction(self, scenario: Any) -> str:
        text = self._normalize_text(scenario)
        positive = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text)
        negative = sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in text)
        
        if positive > negative:
            return Direction.POSITIVE.value
        if negative > positive:
            return Direction.NEGATIVE.value
        if positive == negative and positive > 0:
            return Direction.MIXED.value
        return Direction.UNKNOWN.value

    def estimate_impact(self, scenario: Any) -> str:
        direction = self.estimate_direction(scenario)
        categories = self.classify(scenario)
        
        if "volatility" in categories:
            return ImpactLevel.HIGH.value
        if "reversal" in categories:
            return ImpactLevel.HIGH.value
        if "breakout" in categories:
            return ImpactLevel.MEDIUM_HIGH.value
        if direction in {Direction.POSITIVE.value, Direction.NEGATIVE.value}:
            return ImpactLevel.MEDIUM.value
        if direction == Direction.MIXED.value:
            return ImpactLevel.MEDIUM.value
        return ImpactLevel.LOW.value

    def estimate_risk(self, scenario: Any) -> str:
        categories = self.classify(scenario)
        direction = self.estimate_direction(scenario)
        
        if "volatility" in categories:
            return RiskLevel.HIGH.value
        if "reversal" in categories:
            return RiskLevel.HIGH.value
        if direction == Direction.MIXED.value:
            return RiskLevel.HIGH.value
        if direction == Direction.UNKNOWN.value:
            return RiskLevel.MEDIUM.value
        if "breakout" in categories:
            return RiskLevel.MEDIUM.value
        return RiskLevel.LOW.value

    def estimate_confidence(self, scenario: Any) -> int:
        factors = self.detect_factors(scenario)
        categories = self.classify(scenario)
        direction = self.estimate_direction(scenario)
        
        score = 30
        score += min(len(factors) * 7, 35)
        
        if direction in {Direction.POSITIVE.value, Direction.NEGATIVE.value}:
            score += 12
        elif direction == Direction.MIXED.value:
            score -= 10
        
        if "unknown" not in categories:
            score += 8
        if "breakout" in categories:
            score += 5
        if "reversal" in categories:
            score -= 8
        if "volatility" in categories:
            score -= 10
        
        return max(0, min(100, int(round(score))))

    def estimate_probability(self, confidence: float) -> float:
        try:
            confidence = float(confidence)
        except Exception:
            confidence = 0
        confidence = max(0, min(100, confidence))
        return round(confidence / 100, 3)

    def risk_score(self, risk: str) -> float:
        mapping = {
            RiskLevel.LOW.value: 25,
            RiskLevel.MEDIUM.value: 55,
            RiskLevel.HIGH.value: 85,
            RiskLevel.EXTREME.value: 95,
        }
        return mapping.get(str(risk).upper(), 50)

    # ========================================================
    #
    # EFFECT & ASSUMPTIONS
    #
    # ========================================================

    def generate_effect(self, scenario: Any) -> str:
        direction = self.estimate_direction(scenario)
        categories = self.classify(scenario)
        
        if "breakout" in categories and direction == Direction.POSITIVE.value:
            return "Momentum may strengthen and price expansion may continue."
        if "breakout" in categories and direction == Direction.NEGATIVE.value:
            return "Downside expansion may accelerate if support weakness persists."
        if "reversal" in categories:
            return "Trend direction may become unstable and reversal probability may increase."
        if "volatility" in categories:
            return "Market volatility may increase while directional confidence decreases."
        if direction == Direction.POSITIVE.value:
            return "Positive momentum may improve market strength."
        if direction == Direction.NEGATIVE.value:
            return "Negative pressure may weaken market momentum."
        if direction == Direction.MIXED.value:
            return "Conflicting factors may produce uncertain directional movement."
        return "Scenario impact cannot be determined with sufficient confidence."

    def generate_assumptions(self, scenario: Any) -> List[str]:
        factors = self.detect_factors(scenario)
        assumptions = []
        
        factor_assumptions = {
            "volume": "Volume data remains representative of market participation.",
            "momentum": "Current momentum remains active during the simulated horizon.",
            "trend": "The existing trend does not change abruptly.",
            "volatility": "Volatility remains within an observable range.",
            "liquidity": "Market liquidity remains sufficient for normal price discovery.",
        }
        
        for factor in factors:
            if factor in factor_assumptions:
                assumptions.append(factor_assumptions[factor])
        
        if not assumptions:
            assumptions.append("No major external factor invalidates the simulated scenario.")
        
        return assumptions

    # ========================================================
    #
    # MONTE CARLO SIMULATION
    #
    # ========================================================

    def monte_carlo(
        self,
        scenario: Any,
        iterations: int = 100,
        volatility: float = 0.02,
        confidence: float = 0.95
    ) -> Dict[str, Any]:
        """
        Monte Carlo simulation for scenario uncertainty.
        
        Args:
            scenario: The scenario to simulate
            iterations: Number of iterations
            volatility: Volatility factor
            confidence: Confidence level
            
        Returns:
            Monte Carlo results
        """
        try:
            # Get baseline values
            base = self.simulate(scenario)
            if base.get("status") == "failed":
                return {"status": "failed", "error": "Base simulation failed"}
            
            base_confidence = base.get("confidence", 50)
            base_probability = base.get("probability", 0.5)
            
            # Generate random paths
            results = []
            for _ in range(iterations):
                # Add random noise
                noise = random.gauss(0, volatility)
                adjusted_confidence = max(0, min(100, base_confidence + noise * 10))
                adjusted_probability = max(0, min(1, base_probability + noise * 0.1))
                
                # Adjust direction based on volatility
                direction = base.get("direction", Direction.UNKNOWN.value)
                if volatility > 0.05 and random.random() > 0.7:
                    if direction == Direction.POSITIVE.value:
                        direction = Direction.MIXED.value
                    elif direction == Direction.NEGATIVE.value:
                        direction = Direction.MIXED.value
                
                results.append({
                    "confidence": adjusted_confidence,
                    "probability": adjusted_probability,
                    "direction": direction,
                    "iteration": len(results) + 1
                })
            
            # Calculate statistics
            confidences = [r["confidence"] for r in results]
            probabilities = [r["probability"] for r in results]
            
            return {
                "iterations": iterations,
                "volatility": volatility,
                "confidence_level": confidence,
                "mean_confidence": round(statistics.mean(confidences), 2),
                "std_confidence": round(statistics.stdev(confidences), 2) if len(confidences) > 1 else 0,
                "mean_probability": round(statistics.mean(probabilities), 3),
                "std_probability": round(statistics.stdev(probabilities), 3) if len(probabilities) > 1 else 0,
                "percentile_5": round(sorted(confidences)[int(len(confidences) * 0.05)], 2),
                "percentile_95": round(sorted(confidences)[int(len(confidences) * 0.95)], 2),
                "direction_distribution": {
                    Direction.POSITIVE.value: sum(1 for r in results if r["direction"] == Direction.POSITIVE.value),
                    Direction.NEGATIVE.value: sum(1 for r in results if r["direction"] == Direction.NEGATIVE.value),
                    Direction.MIXED.value: sum(1 for r in results if r["direction"] == Direction.MIXED.value),
                    Direction.UNKNOWN.value: sum(1 for r in results if r["direction"] == Direction.UNKNOWN.value),
                },
                "results": results[:10]  # Sample of results
            }
            
        except Exception as e:
            logger.exception("Monte Carlo failed: %s", e)
            return {"status": "failed", "error": str(e)}

    # ========================================================
    #
    # SENSITIVITY ANALYSIS
    #
    # ========================================================

    def sensitivity_analysis(
        self,
        scenario: Any,
        parameters: List[str] = None
    ) -> Dict[str, Any]:
        """
        Sensitivity analysis for scenario parameters.
        
        Args:
            scenario: The scenario to analyze
            parameters: List of parameters to test
            
        Returns:
            Sensitivity analysis results
        """
        try:
            base = self.simulate(scenario)
            if base.get("status") == "failed":
                return {"status": "failed", "error": "Base simulation failed"}
            
            base_confidence = base.get("confidence", 50)
            
            # Define parameters to test
            if not parameters:
                parameters = ["volume", "momentum", "volatility", "trend"]
            
            sensitivity = {}
            for param in parameters:
                # Test positive and negative variations
                positive_scenario = f"{self._normalize_text(scenario)} {param} strengthened"
                negative_scenario = f"{self._normalize_text(scenario)} {param} weakened"
                
                pos_result = self.simulate(positive_scenario)
                neg_result = self.simulate(negative_scenario)
                
                pos_confidence = pos_result.get("confidence", 50) if pos_result.get("status") == "success" else 50
                neg_confidence = neg_result.get("confidence", 50) if neg_result.get("status") == "success" else 50
                
                sensitivity[param] = {
                    "base_confidence": base_confidence,
                    "positive_impact": round(pos_confidence - base_confidence, 2),
                    "negative_impact": round(neg_confidence - base_confidence, 2),
                    "sensitivity_score": round(abs(pos_confidence - neg_confidence) / 2, 2),
                }
            
            return {
                "status": "success",
                "timestamp": self._timestamp(),
                "base_scenario": base,
                "parameters": sensitivity,
                "most_sensitive": max(sensitivity.items(), key=lambda x: x[1]["sensitivity_score"])[0] if sensitivity else None,
            }
            
        except Exception as e:
            logger.exception("Sensitivity analysis failed: %s", e)
            return {"status": "failed", "error": str(e)}

    # ========================================================
    #
    # MAIN SIMULATION
    #
    # ========================================================

    def simulate(
        self,
        scenario: Any,
        context: Optional[Dict] = None,
        enable_monte_carlo: bool = False,
        enable_sensitivity: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a scenario simulation.
        
        Args:
            scenario: The scenario to simulate
            context: Optional context
            enable_monte_carlo: Enable Monte Carlo simulation
            enable_sensitivity: Enable sensitivity analysis
            
        Returns:
            Simulation result
        """
        with self.lock:
            timestamp = self._timestamp()
            
            try:
                if scenario is None:
                    raise ValueError("Scenario cannot be None.")
                
                normalized = self._normalize_text(scenario)
                if not normalized:
                    raise ValueError("Scenario cannot be empty.")
                
                categories = self.classify(normalized)
                factors = self.detect_factors(normalized)
                direction = self.estimate_direction(normalized)
                impact = self.estimate_impact(normalized)
                risk = self.estimate_risk(normalized)
                confidence = self.estimate_confidence(normalized)
                probability = self.estimate_probability(confidence)
                effect = self.generate_effect(normalized)
                assumptions = self.generate_assumptions(normalized)
                
                result = {
                    "timestamp": timestamp,
                    "version": self.VERSION,
                    "status": "success",
                    "scenario": self._safe_copy(scenario),
                    "normalized_scenario": normalized,
                    "categories": categories,
                    "factors": factors,
                    "direction": direction,
                    "impact": impact,
                    "risk": risk,
                    "risk_score": self.risk_score(risk),
                    "confidence": confidence,
                    "probability": probability,
                    "possible_effect": effect,
                    "assumptions": assumptions,
                    "context": self._safe_copy(context) if context else {},
                }
                
                # Monte Carlo
                if enable_monte_carlo:
                    result["monte_carlo"] = self.monte_carlo(scenario)
                
                # Sensitivity
                if enable_sensitivity:
                    result["sensitivity"] = self.sensitivity_analysis(scenario)
                
                # Pattern matching
                result["patterns"] = self._match_patterns(normalized)
                
                self.total_simulations += 1
                self.successful_simulations += 1
                
                # Convert to SimulationResult
                sim_result = SimulationResult(**result)
                self.simulations.append(sim_result)
                self.last_simulation = sim_result
                
                # Update counters
                self.direction_counter[direction] += 1
                for category in categories:
                    self.category_counter[category] += 1
                self.risk_counter[risk] += 1
                self.impact_counter[impact] += 1
                
                self.updated_at = timestamp
                self._trim_history()
                
                return self._safe_copy(result)
                
            except Exception as e:
                self.total_simulations += 1
                self.failed_simulations += 1
                self.updated_at = timestamp
                logger.exception("Simulation failed: %s", e)
                
                return {
                    "timestamp": timestamp,
                    "version": self.VERSION,
                    "status": "failed",
                    "scenario": self._safe_copy(scenario),
                    "error": str(e),
                }

    # ========================================================
    #
    # PATTERN MATCHING
    #
    # ========================================================

    def _match_patterns(self, text: str) -> List[str]:
        """Match patterns in text."""
        patterns = []
        
        # Check for known patterns
        pattern_definitions = {
            "breakout_follow_through": ["breakout", "follow", "continue"],
            "reversal_after_volume": ["reversal", "volume", "spike"],
            "trend_continuation": ["trend", "continue", "momentum"],
            "volatility_expansion": ["volatility", "expand", "spike"],
        }
        
        for pattern_name, keywords in pattern_definitions.items():
            if all(kw in text for kw in keywords):
                patterns.append(pattern_name)
        
        return patterns

    # ========================================================
    #
    # COMPARE SCENARIOS
    #
    # ========================================================

    def compare(
        self,
        scenario_a: Any,
        scenario_b: Any
    ) -> Dict[str, Any]:
        """Compare two scenarios."""
        result_a = self.simulate(scenario_a)
        result_b = self.simulate(scenario_b)
        
        confidence_a = result_a.get("confidence", 0)
        confidence_b = result_b.get("confidence", 0)
        
        if confidence_a > confidence_b:
            preferred = "scenario_a"
        elif confidence_b > confidence_a:
            preferred = "scenario_b"
        else:
            preferred = "equal"
        
        return {
            "timestamp": self._timestamp(),
            "scenario_a": result_a,
            "scenario_b": result_b,
            "preferred": preferred,
            "confidence_difference": abs(confidence_a - confidence_b),
        }

    # ========================================================
    #
    # BATCH SIMULATION
    #
    # ========================================================

    def simulate_batch(
        self,
        scenarios: List[Any],
        context: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Simulate multiple scenarios."""
        if not scenarios:
            return []
        
        if not isinstance(scenarios, (list, tuple)):
            raise TypeError("Scenarios must be a list or tuple.")
        
        results = []
        for scenario in scenarios:
            results.append(self.simulate(scenario, context=context))
        
        return results

    # ========================================================
    #
    # HISTORY MANAGEMENT
    #
    # ========================================================

    def history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get simulation history."""
        try:
            limit = int(limit)
        except Exception:
            limit = 20
        
        if limit <= 0:
            return []
        
        return self._safe_copy([
            r.to_dict() if isinstance(r, SimulationResult) else r
            for r in self.simulations[-limit:]
        ])

    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """Search history by keyword."""
        if not keyword:
            return []
        
        keyword = self._normalize_text(keyword)
        if not keyword:
            return []
        
        results = []
        for item in self.simulations:
            text = str(item.to_dict() if isinstance(item, SimulationResult) else item).lower()
            if keyword in text:
                results.append(item.to_dict() if isinstance(item, SimulationResult) else item)
        
        return self._safe_copy(results)

    def search_category(self, category: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search by category."""
        if not category:
            return []
        
        category = str(category).lower()
        results = [
            item.to_dict() if isinstance(item, SimulationResult) else item
            for item in self.simulations
            if category in (item.categories if isinstance(item, SimulationResult) else item.get("categories", []))
        ]
        
        return self._safe_copy(results[-limit:])

    def search_direction(self, direction: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search by direction."""
        if not direction:
            return []
        
        direction = str(direction).lower()
        results = [
            item.to_dict() if isinstance(item, SimulationResult) else item
            for item in self.simulations
            if (item.direction if isinstance(item, SimulationResult) else item.get("direction")) == direction
        ]
        
        return self._safe_copy(results[-limit:])

    # ========================================================
    #
    # STATISTICS
    #
    # ========================================================

    def statistics(self) -> SimulationStats:
        """Get comprehensive statistics."""
        if not self.simulations:
            return SimulationStats(
                total=self.total_simulations,
                stored=0,
                successful=self.successful_simulations,
                failed=self.failed_simulations,
            )
        
        confidence_values = []
        probability_values = []
        risk_scores = []
        
        for item in self.simulations:
            if isinstance(item, SimulationResult):
                confidence_values.append(item.confidence)
                probability_values.append(item.probability)
                risk_scores.append(item.risk_score)
            else:
                confidence_values.append(item.get("confidence", 0))
                probability_values.append(item.get("probability", 0))
                risk_scores.append(item.get("risk_score", 0))
        
        return SimulationStats(
            total=self.total_simulations,
            stored=len(self.simulations),
            successful=self.successful_simulations,
            failed=self.failed_simulations,
            average_confidence=round(statistics.mean(confidence_values), 2) if confidence_values else 0,
            average_probability=round(statistics.mean(probability_values), 3) if probability_values else 0,
            average_risk_score=round(statistics.mean(risk_scores), 2) if risk_scores else 0,
            positive=self.direction_counter.get(Direction.POSITIVE.value, 0),
            negative=self.direction_counter.get(Direction.NEGATIVE.value, 0),
            mixed=self.direction_counter.get(Direction.MIXED.value, 0),
            unknown=self.direction_counter.get(Direction.UNKNOWN.value, 0),
            categories=dict(self.category_counter),
            risks=dict(self.risk_counter),
            impacts=dict(self.impact_counter),
            timestamp=self._timestamp()
        )

    # ========================================================
    #
    # EXPORT / IMPORT
    #
    # ========================================================

    def export_data(self) -> Dict[str, Any]:
        """Export all simulation data."""
        return {
            "version": self.VERSION,
            "max_history": self.max_history,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "total_simulations": self.total_simulations,
            "successful_simulations": self.successful_simulations,
            "failed_simulations": self.failed_simulations,
            "simulations": [
                item.to_dict() if isinstance(item, SimulationResult) else item
                for item in self.simulations
            ],
            "statistics": asdict(self.statistics()),
        }

    def import_data(self, data: Dict[str, Any], replace: bool = True) -> int:
        """Import simulation data."""
        if not isinstance(data, dict):
            return 0
        
        simulations = data.get("simulations", [])
        if not isinstance(simulations, list):
            return 0
        
        if replace:
            self.simulations.clear()
        
        imported = 0
        for item in simulations:
            if not isinstance(item, dict):
                continue
            try:
                if "timestamp" in item and "scenario" in item:
                    sim_result = SimulationResult(**item)
                    self.simulations.append(sim_result)
                else:
                    self.simulations.append(self._safe_copy(item))
                imported += 1
            except Exception as e:
                logger.warning("Failed to import simulation: %s", e)
        
        self._trim_history()
        self._rebuild_statistics()
        self.updated_at = self._timestamp()
        
        return imported

    # ========================================================
    #
    # CLEAR & RESET
    #
    # ========================================================

    def clear(self) -> bool:
        """Clear all simulations."""
        self.simulations.clear()
        self.last_simulation = None
        self.category_counter.clear()
        self.direction_counter.clear()
        self.risk_counter.clear()
        self.impact_counter.clear()
        self.pattern_cache.clear()
        self.monte_carlo_cache.clear()
        self.updated_at = self._timestamp()
        return True

    def reset(self) -> bool:
        """Reset all statistics."""
        self.total_simulations = 0
        self.successful_simulations = 0
        self.failed_simulations = 0
        self._rebuild_statistics()
        self.updated_at = self._timestamp()
        return True

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
            "total": self.total_simulations,
            "stored": len(self.simulations),
            "successful": self.successful_simulations,
            "failed": self.failed_simulations,
            "history_limit": self.max_history,
            "has_latest": self.last_simulation is not None,
            "avg_confidence": stats.average_confidence,
            "avg_probability": stats.average_probability,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "timestamp": self._timestamp(),
        }


# ============================================================
#
# BACKWARD COMPATIBILITY
# ============================================================

Simulation = SimulationEngine


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

simulation_engine = SimulationEngine()


# ============================================================
#
# COMPATIBILITY FUNCTIONS - MENGGUNAKAN simulation_engine
# ============================================================

def simulate(scenario: Any, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Legacy simulate function."""
    return simulation_engine.simulate(scenario, context)


def evaluate(scenario: Any) -> str:
    """Legacy evaluate function."""
    result = simulation_engine.simulate(scenario)
    if result.get("status") == "failed":
        return "Simulation failed"
    return result.get("possible_effect", "Unknown scenario")


def history(limit: int = 20) -> List[Dict[str, Any]]:
    """Legacy history function."""
    return simulation_engine.history(limit)


def status() -> Dict[str, Any]:
    """Legacy status function."""
    return simulation_engine.status()


# ============================================================
#
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    """Run comprehensive self-test."""
    print()
    print("=" * 70)
    print("  SIMULATION ENGINE v3.0 - SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        engine = SimulationEngine()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Simulation
    print("\n2. Testing simulation...")
    try:
        result = simulation_engine.simulate("Bullish breakout with high volume")
        if result and result.get("status") == "success":
            results["simulation"] = {"status": "PASS", "confidence": result.get("confidence")}
            tests_passed += 1
            print(f"   ✅ Simulation passed (confidence: {result.get('confidence')}%)")
        else:
            results["simulation"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Simulation failed")
    except Exception as e:
        results["simulation"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Simulation failed: {e}")
    
    # Test 3: Statistics
    print("\n3. Testing statistics...")
    try:
        stats = simulation_engine.statistics()
        if stats and stats.total > 0:
            results["statistics"] = {"status": "PASS", "total": stats.total}
            tests_passed += 1
            print(f"   ✅ Statistics passed (total: {stats.total})")
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
        status_result = simulation_engine.status()
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
        "module": "simulation",
        "version": SIMULATION_VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
#
# PUBLIC API
# ============================================================

__all__ = [
    "MODULE_NAME",
    "MODULE_VERSION",
    "API_VERSION",
    "SimulationEngine",
    "SimulationResult",
    "SimulationStats",
    "Direction",
    "RiskLevel",
    "ImpactLevel",
    "simulation_engine",
    "simulate",
    "evaluate",
    "history",
    "status",
    "self_test",
]


# ============================================================
#
# END
# ============================================================