# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# REASONING ENGINE v3.0
#
# Advanced Cognitive Reasoning Layer
#
# Compatible:
# - Brain v3.0
# - Learning Engine v2.1
# - Long Term Memory
# - Trading Intelligence
#
# Functions:
# - Context Reasoning
# - Market Understanding
# - Historical Memory Analysis
# - Pattern Interpretation
# - Risk Awareness
# - Confidence Evaluation
# - General Knowledge Reasoning
# - Logical Deduction
# - Explainable Reasoning
#
# ============================================================

import logging
import threading
import json
from datetime import datetime
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple

# ============================================================
# SAFE IMPORTS
# ============================================================

try:
    from core.memory import memory
    MEMORY_AVAILABLE = True
except ImportError:
    memory = None
    MEMORY_AVAILABLE = False

try:
    from core.learning.engine import learning_engine
    LEARNING_ENGINE_AVAILABLE = True
except ImportError:
    learning_engine = None
    LEARNING_ENGINE_AVAILABLE = False

logger = logging.getLogger(__name__)


# ============================================================
# CONSTANTS
# ============================================================

MODULE_NAME = "reasoning"
MODULE_VERSION = "3.0.0"
API_VERSION = "1.0"

MAX_HISTORY = 500

POSITIVE_KEYWORDS = {
    "bullish", "breakout", "momentum", "growth", "strong",
    "buy", "accumulation", "uptrend", "support", "recovery",
    "high_volume", "positive", "gain", "profit", "success",
    "opportunity", "upgrade", "breakthrough", "innovation",
}

NEGATIVE_KEYWORDS = {
    "bearish", "breakdown", "weak", "sell", "distribution",
    "downtrend", "resistance", "decline", "crash", "low_volume",
    "negative", "loss", "failure", "risk", "danger",
    "downgrade", "recession", "inflation", "crisis",
}

CONFIRMATION_KEYWORDS = {
    "volume", "high_volume", "breakout", "momentum",
    "trend", "support", "resistance", "confirmation",
    "consensus", "approval", "validation",
}


# ============================================================
# REASONING ENGINE v3.0
# ============================================================

class ReasoningEngine:
    """
    Super Comprehensive Reasoning Engine v3.0.
    
    Supports:
    - Market Reasoning (trading intelligence)
    - General Knowledge Reasoning
    - Sentiment Analysis
    - Logical Deduction
    - Probabilistic Reasoning
    - Evidence-Based Reasoning
    - Multi-Domain Support
    - Brain Compatibility
    - Learning Engine Integration
    - Memory Context
    """

    VERSION = MODULE_VERSION
    NAME = MODULE_NAME

    def __init__(self):
        self.lock = threading.RLock()
        self.reason_count = 0
        self.last_reasoning = None
        self.history = []
        self.errors = 0
        self.success_count = 0
        self.failure_count = 0
        
        # General knowledge facts
        self.knowledge_base = self._load_knowledge_base()
        
        # Logical rules
        self.logical_rules = self._load_logical_rules()
        
        logger.info("Reasoning Engine v%s initialized.", self.VERSION)

    # ============================================================
    # KNOWLEDGE BASE
    # ============================================================

    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load general knowledge base."""
        return {
            "geography": {
                "capital": {
                    "france": "Paris",
                    "indonesia": "Jakarta",
                    "germany": "Berlin",
                    "japan": "Tokyo",
                    "usa": "Washington D.C.",
                    "uk": "London",
                    "italy": "Rome",
                    "spain": "Madrid",
                },
                "population": {
                    "indonesia": "278 million",
                    "usa": "332 million",
                    "japan": "125 million",
                },
            },
            "science": {
                "physics": {
                    "speed_of_light": "299,792,458 m/s",
                    "gravity": "9.8 m/s²",
                },
                "chemistry": {
                    "water_boiling": "100°C at sea level",
                },
            },
            "history": {
                "indonesia": {
                    "independence": "August 17, 1945",
                },
                "world": {
                    "ww2_start": "September 1, 1939",
                },
            },
            "technology": {
                "ai": {
                    "definition": "Artificial Intelligence simulates human intelligence in machines.",
                },
                "blockchain": {
                    "definition": "Blockchain is a distributed ledger technology.",
                },
            },
        }

    def _load_logical_rules(self) -> List[Dict[str, Any]]:
        """Load logical deduction rules."""
        return [
            {
                "name": "bullish_market",
                "conditions": [
                    {"type": "sentiment", "value": "positive"},
                    {"type": "signal", "value": "buy"},
                ],
                "conclusion": "The market is in a bullish state.",
                "confidence": 0.85,
            },
            {
                "name": "bearish_market",
                "conditions": [
                    {"type": "sentiment", "value": "negative"},
                    {"type": "signal", "value": "sell"},
                ],
                "conclusion": "The market is in a bearish state.",
                "confidence": 0.85,
            },
            {
                "name": "high_volume_confirmation",
                "conditions": [
                    {"type": "keyword", "value": "high_volume"},
                    {"type": "keyword", "value": "breakout"},
                ],
                "conclusion": "High volume breakout indicates strong conviction.",
                "confidence": 0.75,
            },
        ]

    # ============================================================
    # BRAIN COMPATIBILITY BRIDGE
    # ============================================================

    def analyze(self, data: Any) -> Dict[str, Any]:
        """Brain compatibility bridge."""
        return self.think(data, context="market")

    # ============================================================
    # MAIN THINK PROCESS
    # ============================================================

    def think(self, data: Any, context: str = "general") -> Dict[str, Any]:
        """
        Main reasoning process.
        
        Args:
            data: Input data (dict, list, string, etc.)
            context: Reasoning context (market, general, research)
            
        Returns:
            Complete reasoning result
        """
        with self.lock:
            try:
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "context": context,
                    "input": data,
                    "analysis": {},
                    "memory": {},
                    "learning": {},
                    "risk": {},
                    "decision": None,
                    "confidence": 0,
                }

                # 1. Memory Context
                if MEMORY_AVAILABLE:
                    result["memory"] = self.read_memory()

                # 2. Learning Insight
                if LEARNING_ENGINE_AVAILABLE and learning_engine:
                    try:
                        if hasattr(learning_engine, 'get_insight'):
                            insight = learning_engine.get_insight()
                            result["learning"] = insight if insight else {}
                        else:
                            result["learning"] = {"status": "available"}
                    except Exception:
                        result["learning"] = {}

                # 3. Context Routing
                if context == "market":
                    analysis = self.market_reasoning(data)
                elif context == "research":
                    analysis = self.information_reasoning(data)
                else:
                    analysis = self.general_reasoning(data)

                result["analysis"] = analysis

                # 4. Risk Analysis
                result["risk"] = self.risk_analysis(result)

                # 5. Conclusion
                result["decision"] = self.generate_conclusion(result)

                # 6. Confidence
                result["confidence"] = self.calculate_confidence(result)

                # Save state
                self.reason_count += 1
                self.last_reasoning = result
                self.history.append(result)

                if len(self.history) > MAX_HISTORY:
                    self.history.pop(0)

                # Save to memory
                if MEMORY_AVAILABLE and hasattr(memory, 'save_knowledge'):
                    try:
                        memory.save_knowledge(result, "reasoning")
                    except Exception:
                        pass

                return result

            except Exception as e:
                self.errors += 1
                logger.exception("Reasoning failed: %s", e)
                return {"error": str(e), "timestamp": datetime.now().isoformat()}

    # ============================================================
    # MEMORY READING
    # ============================================================

    def read_memory(self) -> Dict[str, Any]:
        """Read memory context."""
        if not MEMORY_AVAILABLE or memory is None:
            return {}
        
        try:
            observations = memory.get_observations(50) if hasattr(memory, 'get_observations') else []
            patterns = memory.get_patterns(50) if hasattr(memory, 'get_patterns') else []
            decisions = memory.get_decisions(20) if hasattr(memory, 'get_decisions') else []

            return {
                "observations": len(observations),
                "patterns": len(patterns),
                "decisions": len(decisions),
            }
        except Exception as e:
            logger.warning("Memory read failed: %s", e)
            return {}

    # ============================================================
    # MARKET REASONING
    # ============================================================

    def market_reasoning(self, data: Any) -> Dict[str, Any]:
        """
        Market-specific reasoning for trading intelligence.
        
        Reads:
        - Signal
        - Confidence
        - Strength
        - MTF Alignment
        - Pattern
        """
        try:
            analysis = {
                "trend": "NEUTRAL",
                "buy_score": 0,
                "sell_score": 0,
                "signals": 0,
                "mtf_alignment": 0,
                "patterns": [],
                "average_confidence": 0,
                "positive_factors": [],
                "negative_factors": [],
                "confirmation_factors": [],
                "conflicts": [],
            }

            confidence_values = []
            buy_score = 0
            sell_score = 0

            # Process data if it's a list of signals
            if isinstance(data, list):
                analysis["signals"] = len(data)

                for item in data:
                    if not isinstance(item, dict):
                        continue

                    signal = item.get("signal", {})
                    if not isinstance(signal, dict):
                        continue

                    action = str(signal.get("signal", "HOLD")).upper()
                    confidence = float(signal.get("confidence", 0))
                    strength = float(signal.get("strength", 0))

                    confidence_values.append(confidence)

                    # Weighted signal
                    weight = (confidence * 0.6) + (strength * 0.4)

                    if action == "BUY":
                        buy_score += weight
                        analysis["positive_factors"].append("buy_signal")
                    elif action == "SELL":
                        sell_score += weight
                        analysis["negative_factors"].append("sell_signal")

                    # MTF
                    mtf = signal.get("mtf_alignment", 0)
                    try:
                        analysis["mtf_alignment"] += int(mtf)
                    except Exception:
                        pass

                    # Pattern
                    pattern = signal.get("pattern")
                    if pattern:
                        analysis["patterns"].append(pattern)

            # If data is a dict with features
            elif isinstance(data, dict):
                features = data.get("features", {})
                analysis_data = data.get("analysis", {})
                
                keywords = features.get("keywords", [])
                sentiment = analysis_data.get("sentiment", "neutral")

                # Process keywords
                keyword_set = set(str(k).strip().lower() for k in keywords if k)
                positive_matches = keyword_set & POSITIVE_KEYWORDS
                negative_matches = keyword_set & NEGATIVE_KEYWORDS
                confirmation_matches = keyword_set & CONFIRMATION_KEYWORDS

                analysis["positive_factors"] = list(positive_matches)
                analysis["negative_factors"] = list(negative_matches)
                analysis["confirmation_factors"] = list(confirmation_matches)

                # Sentiment
                if sentiment == "positive":
                    buy_score = 60
                    analysis["positive_factors"].append("positive_sentiment")
                elif sentiment == "negative":
                    sell_score = 60
                    analysis["negative_factors"].append("negative_sentiment")

                # Conflicts
                if positive_matches and negative_matches:
                    analysis["conflicts"].append({
                        "type": "directional_conflict",
                        "positive": list(positive_matches),
                        "negative": list(negative_matches),
                    })

            # Final score
            analysis["buy_score"] = round(buy_score, 2)
            analysis["sell_score"] = round(sell_score, 2)

            if buy_score > sell_score:
                analysis["trend"] = "BULLISH"
            elif sell_score > buy_score:
                analysis["trend"] = "BEARISH"
            else:
                analysis["trend"] = "NEUTRAL"

            if confidence_values:
                analysis["average_confidence"] = round(
                    sum(confidence_values) / len(confidence_values), 2
                )

            return analysis

        except Exception as e:
            logger.exception("Market reasoning error: %s", e)
            return {}

    # ============================================================
    # INFORMATION REASONING
    # ============================================================

    def information_reasoning(self, data: Any) -> Dict[str, Any]:
        """Reasoning for text/research data."""
        text = str(data)
        keywords = self.extract_keywords(text)

        # Try knowledge base lookup
        knowledge_result = self._query_knowledge_base(text)
        if knowledge_result:
            return {
                "type": "knowledge",
                "response": knowledge_result,
                "length": len(text),
                "keywords": keywords,
                "summary": text[:500],
                "source": "knowledge_base",
                "confidence": 0.9,
            }

        return {
            "type": "information",
            "length": len(text),
            "keywords": keywords,
            "summary": text[:500],
            "confidence": 0.5,
        }

    # ============================================================
    # GENERAL REASONING
    # ============================================================

    def general_reasoning(self, data: Any) -> Dict[str, Any]:
        """General purpose reasoning."""
        text = str(data)
        text_lower = text.lower()

        # Check for greetings
        greeting_responses = {
            "hello": "Hello! How can I assist you?",
            "hi": "Hi there! What can I help with?",
            "help": "I'm here to help! Ask me anything.",
            "thanks": "You're welcome!",
            "thank you": "You're welcome!",
        }
        
        for key, response in greeting_responses.items():
            if key in text_lower:
                return {
                    "type": "greeting",
                    "response": response,
                    "confidence": 1.0,
                }

        # Try knowledge base
        knowledge_result = self._query_knowledge_base(text)
        if knowledge_result:
            return {
                "type": "knowledge",
                "response": knowledge_result,
                "confidence": 0.9,
                "source": "knowledge_base",
            }

        # Try logical deduction
        deduction = self._apply_logical_rules(text)
        if deduction:
            return {
                "type": "deduction",
                "response": deduction["conclusion"],
                "confidence": deduction["confidence"],
                "rules_applied": deduction["rules_applied"],
            }

        # Try question answering
        answer = self._answer_question(text)
        if answer:
            return {
                "type": "answer",
                "response": answer,
                "confidence": 0.7,
            }

        return {
            "type": "general",
            "content": text[:500],
            "confidence": 0.3,
        }

    def _answer_question(self, text: str) -> Optional[str]:
        """Answer common questions."""
        text_lower = text.lower()
        
        if "how are you" in text_lower:
            return "I'm functioning optimally! How can I assist?"
        
        if "what is your name" in text_lower:
            return "I am Inkside Intelligence OS, a Cognitive Mirror Engine."
        
        if "what can you do" in text_lower:
            return "I can help with market analysis, general knowledge, reasoning, and decision support."
        
        if "tell me about yourself" in text_lower:
            return "I am an AI system designed for market intelligence and cognitive reasoning."
        
        if "what is the meaning of life" in text_lower:
            return "The meaning of life is subjective. For me, it's helping you make better decisions!"
        
        return None

    # ============================================================
    # KNOWLEDGE BASE QUERY
    # ============================================================

    def _query_knowledge_base(self, query: str) -> Optional[str]:
        """Query general knowledge base."""
        query_lower = query.lower()

        # Geography: capital
        if "capital of" in query_lower:
            for country, capital in self.knowledge_base.get("geography", {}).get("capital", {}).items():
                if country in query_lower:
                    return f"The capital of {country.title()} is {capital}."

        # Geography: population
        if "population of" in query_lower:
            for country, population in self.knowledge_base.get("geography", {}).get("population", {}).items():
                if country in query_lower:
                    return f"The population of {country.title()} is approximately {population}."

        # Science: speed of light
        if "speed of light" in query_lower:
            return self.knowledge_base.get("science", {}).get("physics", {}).get("speed_of_light", "")

        # Science: gravity
        if "gravity" in query_lower:
            return self.knowledge_base.get("science", {}).get("physics", {}).get("gravity", "")

        # History: Indonesia independence
        if "indonesia independence" in query_lower or "indonesia merdeka" in query_lower:
            return self.knowledge_base.get("history", {}).get("indonesia", {}).get("independence", "")

        # History: WW2
        if "world war" in query_lower or "ww2" in query_lower:
            return self.knowledge_base.get("history", {}).get("world", {}).get("ww2_start", "")

        # Technology: AI
        if "what is ai" in query_lower or "artificial intelligence" in query_lower:
            return self.knowledge_base.get("technology", {}).get("ai", {}).get("definition", "")

        # Technology: Blockchain
        if "what is blockchain" in query_lower:
            return self.knowledge_base.get("technology", {}).get("blockchain", {}).get("definition", "")

        return None

    # ============================================================
    # LOGICAL DEDUCTION
    # ============================================================

    def _apply_logical_rules(self, text: str) -> Optional[Dict[str, Any]]:
        """Apply logical rules to text."""
        text_lower = text.lower()
        applied_rules = []
        conclusion = None
        confidence = 0.0

        for rule in self.logical_rules:
            conditions_met = 0
            total_conditions = len(rule["conditions"])

            for condition in rule["conditions"]:
                if condition["type"] == "sentiment":
                    if "positive" in text_lower and condition["value"] == "positive":
                        conditions_met += 1
                    elif "negative" in text_lower and condition["value"] == "negative":
                        conditions_met += 1
                elif condition["type"] == "keyword":
                    if condition["value"] in text_lower:
                        conditions_met += 1

            if total_conditions > 0 and conditions_met >= total_conditions * 0.7:
                applied_rules.append(rule["name"])
                if rule.get("conclusion"):
                    conclusion = rule["conclusion"]
                    confidence = rule.get("confidence", 0.5)

        if applied_rules and conclusion:
            return {
                "conclusion": conclusion,
                "confidence": confidence,
                "rules_applied": applied_rules,
            }

        return None

    # ============================================================
    # RISK ANALYSIS
    # ============================================================

    def risk_analysis(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk from reasoning result."""
        risk = {
            "level": "LOW",
            "reason": [],
            "recommendation": "NORMAL",
        }

        analysis = result.get("analysis", {})
        confidence = analysis.get("average_confidence", 0)
        mtf = analysis.get("mtf_alignment", 0)

        # Low confidence
        if confidence < 40:
            risk["level"] = "HIGH"
            risk["reason"].append("Low confidence")
        elif confidence < 60:
            risk["level"] = "MEDIUM"
            risk["reason"].append("Moderate confidence")

        # MTF check
        if mtf < 2:
            risk["reason"].append("Weak timeframe alignment")
            if risk["level"] == "LOW":
                risk["level"] = "MEDIUM"

        # Conflict check
        conflicts = analysis.get("conflicts", [])
        if conflicts:
            risk["level"] = "HIGH"
            risk["reason"].append(f"{len(conflicts)} conflicts detected")

        # Recommendation
        if risk["level"] == "HIGH":
            risk["recommendation"] = "Avoid aggressive position. Wait confirmation."
        elif risk["level"] == "MEDIUM":
            risk["recommendation"] = "Reduce position size."
        else:
            risk["recommendation"] = "Normal execution allowed."

        return risk

    # ============================================================
    # CONCLUSION GENERATOR
    # ============================================================

    def generate_conclusion(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate conclusion from reasoning result."""
        analysis = result.get("analysis", {})
        trend = analysis.get("trend", "NEUTRAL")
        risk = result.get("risk", {})
        risk_level = risk.get("level", "LOW")

        if trend == "BULLISH":
            return {
                "action": "BUY_BIAS",
                "message": "Market shows bullish probability.",
                "risk": risk_level,
            }
        elif trend == "BEARISH":
            return {
                "action": "SELL_BIAS",
                "message": "Market shows bearish probability.",
                "risk": risk_level,
            }
        else:
            return {
                "action": "WAIT",
                "message": "Market condition unclear.",
                "risk": risk_level,
            }

    # ============================================================
    # CONFIDENCE CALCULATION
    # ============================================================

    def calculate_confidence(self, result: Dict[str, Any]) -> int:
        """Calculate confidence score (0-100)."""
        try:
            score = 0
            analysis = result.get("analysis", {})
            memory_data = result.get("memory", {})
            learning_data = result.get("learning", {})

            # Analysis quality
            if analysis:
                score += 20

            # Trend confirmation
            trend = analysis.get("trend", "NEUTRAL")
            if trend != "NEUTRAL":
                score += 20

            # Signal confidence
            avg_conf = analysis.get("average_confidence", 0)
            score += avg_conf * 0.35

            # Memory experience
            if memory_data:
                if memory_data.get("observations", 0) > 10:
                    score += 10

            # Learning support
            if learning_data:
                score += 15

            return min(int(score), 100)

        except Exception as e:
            logger.exception("Confidence calculation failed: %s", e)
            return 0

    # ============================================================
    # KEYWORD EXTRACTION
    # ============================================================

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        try:
            words = str(text).lower().split()
            result = []
            for word in words:
                clean = word.replace(".", "").replace(",", "").replace(":", "").replace(";", "")
                if len(clean) > 5 and clean.isalpha():
                    result.append(clean)
            return list(set(result))[:30]
        except Exception:
            return []

    # ============================================================
    # PREDICTION BRIDGE
    # ============================================================

    def prediction_input(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Bridge to prediction engine."""
        analysis = result.get("analysis", {})
        return {
            "trend": analysis.get("trend", "NEUTRAL"),
            "confidence": result.get("confidence", 0),
            "risk": result.get("risk", {}),
        }

    # ============================================================
    # INSIGHT GENERATOR
    # ============================================================

    def insight(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate natural language insight."""
        try:
            analysis = result.get("analysis", {})
            trend = analysis.get("trend", "NEUTRAL")
            confidence = result.get("confidence", 0)
            risk = result.get("risk", {}).get("level", "LOW")

            return {
                "summary": f"Market condition {trend} with confidence {confidence}%.",
                "risk": risk,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception:
            return {}

    # ============================================================
    # STATUS & PUBLIC API
    # ============================================================

    def status(self) -> Dict[str, Any]:
        """Get engine status."""
        return {
            "module": self.NAME,
            "version": self.VERSION,
            "status": "ONLINE",
            "reason_count": self.reason_count,
            "errors": self.errors,
            "history": len(self.history),
            "active": True,
            "timestamp": datetime.now().isoformat(),
        }

    def snapshot(self) -> Dict[str, Any]:
        """Get snapshot for GUI dashboard."""
        return {
            "status": self.status(),
            "last_reasoning": self.last_reasoning,
        }

    def get_history(self, limit: int = 20) -> List[Dict]:
        """Get reasoning history."""
        return deepcopy(self.history[-limit:]) if self.history else []

    def latest(self) -> Optional[Dict]:
        """Get latest reasoning result."""
        return deepcopy(self.last_reasoning) if self.last_reasoning else None

    def reset(self) -> bool:
        """Reset engine."""
        self.reason_count = 0
        self.history.clear()
        self.errors = 0
        self.last_reasoning = None
        return True

    def answer(self, question: str) -> str:
        """Answer a question using general reasoning."""
        result = self.think({"text": question, "type": "question"}, context="general")
        return result.get("analysis", {}).get("response", "I don't have an answer for that.")


# ============================================================
# GLOBAL INSTANCE
# ============================================================

reasoning = ReasoningEngine()


# ============================================================
# SHORTCUT FUNCTIONS - MENGGUNAKAN reasoning
# ============================================================

def think(data: Any, context: str = "general") -> Dict[str, Any]:
    """Quick think shortcut."""
    return reasoning.think(data, context)


def analyze(data: Any) -> Dict[str, Any]:
    """Brain compatibility shortcut."""
    return reasoning.analyze(data)


def answer(question: str) -> str:
    """Quick answer shortcut."""
    return reasoning.answer(question)


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    """Run self-test."""
    print()
    print("=" * 70)
    print("  REASONING ENGINE v3.0 - SELF TEST")
    print("=" * 70)
    print()

    tests_passed = 0
    tests_failed = 0
    results = {}

    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        engine = ReasoningEngine()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")

    # Test 2: Market Reasoning
    print("\n2. Testing market reasoning...")
    try:
        test_data = {
            "features": {
                "keywords": ["bullish", "breakout", "volume"],
            },
            "analysis": {
                "sentiment": "positive",
            }
        }
        result = reasoning.think(test_data, context="market")
        if result and result.get("analysis", {}).get("trend") == "BULLISH":
            results["market_reasoning"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Market reasoning passed")
        else:
            results["market_reasoning"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Market reasoning failed")
    except Exception as e:
        results["market_reasoning"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Market reasoning failed: {e}")

    # Test 3: General Knowledge
    print("\n3. Testing general knowledge...")
    try:
        result = reasoning.answer("What is the capital of France?")
        if result and "Paris" in result:
            results["general_knowledge"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ General knowledge passed")
        else:
            results["general_knowledge"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ General knowledge failed")
    except Exception as e:
        results["general_knowledge"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ General knowledge failed: {e}")

    # Test 4: Status
    print("\n4. Testing status...")
    try:
        status = reasoning.status()
        if status and "module" in status:
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
        "module": "reasoning",
        "version": reasoning.VERSION,
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
    "ReasoningEngine",
    "reasoning",
    "think",
    "analyze",
    "answer",
    "self_test",
]


# ============================================================
# END
# ============================================================