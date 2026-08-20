# ============================================================
# core/reasoning.py
# REASONING ENGINE v3.0
# SUPER COMPREHENSIVE COGNITIVE REASONING
#
# FITUR:
# 1. Market Reasoning (trading signals)
# 2. General Knowledge Reasoning (facts, logic)
# 3. Sentiment Analysis (positive/negative/neutral)
# 4. Keyword & Entity Extraction
# 5. Logical Deduction (if-then rules)
# 6. Probabilistic Reasoning (confidence scoring)
# 7. Evidence-Based Reasoning
# 8. Conflict Detection
# 9. Multi-Domain Support
# 10. Reasoning History & Tracking
# 11. Accuracy Measurement
# 12. Explainable Reasoning (human-readable)
# ============================================================

import logging
import json
from datetime import datetime
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ============================================================
# CONSTANTS
# ============================================================

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

GENERAL_KNOWLEDGE_PATTERNS = {
    "geography": {
        "capital": "The capital of {country} is {capital}.",
        "population": "The population of {country} is approximately {population}.",
    },
    "science": {
        "speed_of_light": "The speed of light is approximately 299,792,458 m/s.",
        "gravity": "Earth's gravity is 9.8 m/s².",
        "water": "Water boils at 100°C (212°F) at sea level.",
    },
    "history": {
        "indonesia_independence": "Indonesia declared independence on August 17, 1945.",
        "ww2": "World War II lasted from 1939 to 1945.",
    },
    "technology": {
        "ai": "Artificial Intelligence (AI) simulates human intelligence in machines.",
        "machine_learning": "Machine Learning is a subset of AI that learns from data.",
    },
}


# ============================================================
# REASONING ENGINE v3.0
# ============================================================

class ReasoningEngine:
    """
    Super Comprehensive Reasoning Engine v3.0.
    
    Supports:
    - Market Reasoning (trading)
    - General Knowledge Reasoning
    - Sentiment Analysis
    - Logical Deduction
    - Probabilistic Reasoning
    - Evidence-Based Reasoning
    - Multi-Domain Support
    """
    
    VERSION = "3.0.0"
    NAME = "reasoning"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.reasoning_count = 0
        self.history: List[Dict] = []
        self.success_count = 0
        self.failure_count = 0
        self.last_reasoning = None
        
        # General knowledge facts
        self.knowledge_base = self._load_knowledge_base()
        
        # Logical rules
        self.logical_rules = self._load_logical_rules()
        
        # Domain-specific patterns
        self.patterns = self._load_patterns()
        
        logger.info("Reasoning Engine v%s initialized.", self.VERSION)
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load general knowledge base."""
        return {
            # Geography
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
                    "germany": "83 million",
                },
                "area": {
                    "indonesia": "1,904,569 km²",
                    "usa": "9,833,517 km²",
                    "japan": "377,975 km²",
                },
            },
            "science": {
                "physics": {
                    "speed_of_light": "299,792,458 m/s",
                    "gravity": "9.8 m/s²",
                    "plank_constant": "6.626 × 10⁻³⁴ J⋅s",
                },
                "chemistry": {
                    "water_boiling": "100°C at sea level",
                    "water_freezing": "0°C at sea level",
                    "ph_neutral": "7.0",
                },
            },
            "history": {
                "indonesia": {
                    "independence": "August 17, 1945",
                    "proclamation": "Soekarno-Hatta proclaimed independence",
                },
                "world": {
                    "ww2_start": "September 1, 1939",
                    "ww2_end": "September 2, 1945",
                },
            },
            "technology": {
                "ai": {
                    "definition": "Artificial Intelligence simulates human intelligence in machines.",
                    "types": "Narrow AI, General AI, Super AI",
                },
                "blockchain": {
                    "definition": "Blockchain is a distributed ledger technology.",
                    "consensus": "Proof of Work, Proof of Stake, etc.",
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
                    {"type": "trend", "value": "uptrend"},
                ],
                "conclusion": "The market is in a bullish state.",
                "confidence": 0.85,
            },
            {
                "name": "bearish_market",
                "conditions": [
                    {"type": "sentiment", "value": "negative"},
                    {"type": "signal", "value": "sell"},
                    {"type": "trend", "value": "downtrend"},
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
            {
                "name": "knowledge_general",
                "conditions": [
                    {"type": "domain", "value": "general"},
                ],
                "conclusion": "Using general knowledge reasoning.",
                "confidence": 0.6,
            },
        ]
    
    def _load_patterns(self) -> Dict[str, Any]:
        """Load reasoning patterns."""
        return {
            "question_patterns": [
                {"patterns": ["what is", "who is", "where is", "when is", "why is", "how is", "tell me about"], "domain": "general"},
                {"patterns": ["what is the capital", "capital of"], "domain": "geography"},
                {"patterns": ["how many", "population"], "domain": "geography"},
                {"patterns": ["what is the speed", "how fast"], "domain": "science"},
                {"patterns": ["when did", "history of"], "domain": "history"},
                {"patterns": ["what is ai", "artificial intelligence"], "domain": "technology"},
                {"patterns": ["what is blockchain"], "domain": "technology"},
                {"patterns": ["bullish", "bearish", "market", "trading", "signal"], "domain": "market"},
            ],
            "general_knowledge": {
                "responses": {
                    "hello": "Hello! How can I assist you?",
                    "hi": "Hi there! What can I help with?",
                    "help": "I'm here to help! Ask me anything.",
                    "thanks": "You're welcome!",
                    "thank you": "You're welcome!",
                }
            }
        }
    
    # ========================================================
    # MAIN REASONING
    # ========================================================
    
    def reason(self, data: Any, domain: str = "auto") -> Dict[str, Any]:
        """
        Main reasoning method - detects domain automatically.
        
        Args:
            data: Input data (dict, list, string, etc.)
            domain: Optional domain override (market, general, auto)
            
        Returns:
            Reasoning result with full analysis
        """
        try:
            # Normalize input
            normalized_data = self._normalize_input(data)
            
            # Auto-detect domain
            detected_domain = self._detect_domain(normalized_data)
            domain = detected_domain if domain == "auto" else domain
            
            # Domain-specific reasoning
            if domain == "market":
                result = self._market_reasoning(normalized_data)
            elif domain == "general":
                result = self._general_reasoning(normalized_data)
            else:
                result = self._general_reasoning(normalized_data)
            
            # Add domain info
            result["domain"] = domain
            result["detected_domain"] = detected_domain
            result["timestamp"] = datetime.now().isoformat()
            result["reasoning_cycle"] = self.reasoning_count + 1
            
            # Store history
            self.reasoning_count += 1
            self.last_reasoning = result
            self.history.append(deepcopy(result))
            
            if len(self.history) > MAX_HISTORY:
                self.history.pop(0)
            
            return result
            
        except Exception as e:
            logger.exception(f"Reasoning failed: {e}")
            return {
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
    
    # ========================================================
    # INPUT NORMALIZATION
    # ========================================================
    
    def _normalize_input(self, data: Any) -> Dict[str, Any]:
        """Normalize input to dictionary format."""
        if data is None:
            return {}
        
        if isinstance(data, dict):
            return data
        
        if isinstance(data, str):
            # Try to parse as JSON
            try:
                parsed = json.loads(data)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass
            
            # Treat as text/query
            return {"text": data, "type": "question"}
        
        if isinstance(data, list):
            return {"items": data, "type": "list"}
        
        return {"raw": data, "type": "generic"}
    
    # ========================================================
    # DOMAIN DETECTION
    # ========================================================
    
    def _detect_domain(self, data: Dict[str, Any]) -> str:
        """Auto-detect domain from input."""
        text = str(data).lower()
        
        # Market keywords
        if any(kw in text for kw in ["btc", "eth", "sol", "price", "market", "trading", "bullish", "bearish", "signal", "volume"]):
            return "market"
        
        # Question patterns
        question_starters = ["what", "who", "where", "when", "why", "how", "tell me", "explain", "define"]
        if any(text.startswith(q) for q in question_starters):
            # Check for specific domains
            if "capital" in text or "country" in text or "population" in text:
                return "general"
            if "speed" in text or "light" in text or "gravity" in text:
                return "general"
            if "history" in text or "when" in text:
                return "general"
            if "ai" in text or "blockchain" in text or "technology" in text:
                return "general"
            return "general"
        
        # Default
        return "general"
    
    # ========================================================
    # MARKET REASONING
    # ========================================================
    
    def _market_reasoning(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Market-specific reasoning."""
        features = data.get("features", {})
        analysis = data.get("analysis", {})
        prediction = data.get("prediction", {})
        
        sentiment = self._normalize_sentiment(analysis.get("sentiment", "neutral"))
        keywords = self._normalize_list(features.get("keywords", []))
        entities = self._normalize_list(features.get("entities", []))
        
        # Process keywords
        keyword_set = set(str(k).strip().lower() for k in keywords if k is not None)
        positive_matches = keyword_set & POSITIVE_KEYWORDS
        negative_matches = keyword_set & NEGATIVE_KEYWORDS
        confirmation_matches = keyword_set & CONFIRMATION_KEYWORDS
        
        # Build reasoning
        reasons = []
        evidence = []
        positive_factors = []
        negative_factors = []
        confirmation_factors = []
        conflicts = []
        
        # Sentiment reasoning
        if sentiment == "positive":
            reasons.append("Positive market pressure detected.")
            evidence.append({"type": "sentiment", "value": sentiment, "impact": "positive"})
            positive_factors.append("positive_sentiment")
        elif sentiment == "negative":
            reasons.append("Negative market pressure detected.")
            evidence.append({"type": "sentiment", "value": sentiment, "impact": "negative"})
            negative_factors.append("negative_sentiment")
        else:
            reasons.append("Market sentiment remains neutral.")
            evidence.append({"type": "sentiment", "value": sentiment, "impact": "neutral"})
        
        # Keyword reasoning
        for kw in sorted(positive_matches):
            positive_factors.append(kw)
            evidence.append({"type": "keyword", "value": kw, "impact": "positive"})
        
        for kw in sorted(negative_matches):
            negative_factors.append(kw)
            evidence.append({"type": "keyword", "value": kw, "impact": "negative"})
        
        for kw in sorted(confirmation_matches):
            confirmation_factors.append(kw)
            evidence.append({"type": "confirmation", "value": kw, "impact": "confirmation"})
        
        # Conflict detection
        if positive_matches and negative_matches:
            conflicts.append({
                "type": "directional_conflict",
                "positive": sorted(positive_matches),
                "negative": sorted(negative_matches),
            })
        
        if sentiment == "positive" and negative_matches and not positive_matches:
            conflicts.append({
                "type": "sentiment_conflict",
                "sentiment": sentiment,
                "negative_factors": sorted(negative_matches),
            })
        
        if sentiment == "negative" and positive_matches and not negative_matches:
            conflicts.append({
                "type": "sentiment_conflict",
                "sentiment": sentiment,
                "positive_factors": sorted(positive_matches),
            })
        
        # Calculate scores
        score = self._calculate_score(
            sentiment=sentiment,
            positive_factors=positive_factors,
            negative_factors=negative_factors,
            confirmation_factors=confirmation_factors,
            conflicts=conflicts,
        )
        
        direction = self._determine_direction(
            sentiment=sentiment,
            positive_factors=positive_factors,
            negative_factors=negative_factors,
            conflicts=conflicts,
        )
        
        confidence = self._calculate_confidence(
            score=score,
            evidence=evidence,
            conflicts=conflicts,
        )
        
        return {
            "direction": direction,
            "sentiment": sentiment,
            "score": score,
            "confidence": confidence,
            "strength": self._strength_label(score),
            "entities": entities,
            "keywords": keywords,
            "reasons": reasons,
            "evidence": evidence,
            "positive_factors": positive_factors,
            "negative_factors": negative_factors,
            "confirmation_factors": confirmation_factors,
            "conflicts": conflicts,
            "summary": self._build_summary(direction, score, positive_factors, negative_factors, conflicts),
        }
    
    # ========================================================
    # GENERAL KNOWLEDGE REASONING
    # ========================================================
    
    def _general_reasoning(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """General knowledge reasoning."""
        text = data.get("text", data.get("query", ""))
        domain = data.get("domain", "general")
        
        # Check for basic greetings
        greeting_responses = self.patterns.get("general_knowledge", {}).get("responses", {})
        for key, response in greeting_responses.items():
            if key in text.lower():
                return {
                    "response": response,
                    "domain": "general",
                    "type": "greeting",
                    "confidence": 1.0,
                }
        
        # Try knowledge base lookup
        knowledge_result = self._query_knowledge_base(text)
        if knowledge_result:
            return {
                "response": knowledge_result,
                "domain": "general",
                "type": "knowledge",
                "confidence": 0.9,
                "source": "knowledge_base",
            }
        
        # Try logical deduction
        deduction = self._apply_logical_rules(text)
        if deduction:
            return {
                "response": deduction["conclusion"],
                "domain": "general",
                "type": "deduction",
                "confidence": deduction["confidence"],
                "rules_applied": deduction["rules_applied"],
            }
        
        # Try question answering
        answer = self._answer_question(text)
        if answer:
            return {
                "response": answer,
                "domain": "general",
                "type": "answer",
                "confidence": 0.7,
            }
        
        # Fallback response
        return {
            "response": "I'm not sure about that. Could you rephrase your question?",
            "domain": "general",
            "type": "fallback",
            "confidence": 0.2,
        }
    
    # ========================================================
    # KNOWLEDGE BASE QUERY
    # ========================================================
    
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
        
        # Geography: area
        if "area of" in query_lower:
            for country, area in self.knowledge_base.get("geography", {}).get("area", {}).items():
                if country in query_lower:
                    return f"The area of {country.title()} is {area}."
        
        # Science: speed of light
        if "speed of light" in query_lower:
            return self.knowledge_base.get("science", {}).get("physics", {}).get("speed_of_light", "")
        
        # Science: gravity
        if "gravity" in query_lower:
            return self.knowledge_base.get("science", {}).get("physics", {}).get("gravity", "")
        
        # Science: water boiling
        if "water boil" in query_lower or "boiling point" in query_lower:
            return self.knowledge_base.get("science", {}).get("chemistry", {}).get("water_boiling", "")
        
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
    
    # ========================================================
    # LOGICAL DEDUCTION
    # ========================================================
    
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
                elif condition["type"] == "domain":
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
    
    # ========================================================
    # QUESTION ANSWERING
    # ========================================================
    
    def _answer_question(self, text: str) -> Optional[str]:
        """Answer general questions."""
        text_lower = text.lower()
        
        # Simple pattern matching
        if "hello" in text_lower or "hi" in text_lower:
            return "Hello! How can I help you?"
        
        if "how are you" in text_lower:
            return "I'm functioning optimally! How can I assist?"
        
        if "what is your name" in text_lower:
            return "I am Inkside Intelligence OS, a Cognitive Mirror Engine."
        
        if "what can you do" in text_lower:
            return "I can help with market analysis, general knowledge, reasoning, and decision support."
        
        if "tell me about yourself" in text_lower:
            return "I am an AI system designed for market intelligence and cognitive reasoning."
        
        return None
    
    # ========================================================
    # UTILITY METHODS
    # ========================================================
    
    def _normalize_sentiment(self, sentiment: Any) -> str:
        """Normalize sentiment value."""
        if sentiment is None:
            return "neutral"
        
        value = str(sentiment).strip().lower()
        
        if value in {"positive", "bullish", "bull", "buy", "optimistic"}:
            return "positive"
        
        if value in {"negative", "bearish", "bear", "sell", "pessimistic"}:
            return "negative"
        
        return "neutral"
    
    def _normalize_list(self, value: Any) -> List[str]:
        """Normalize to list."""
        if value is None:
            return []
        
        if isinstance(value, (list, tuple, set)):
            return list(value)
        
        return [str(value)]
    
    def _calculate_score(
        self,
        sentiment: str,
        positive_factors: List[str],
        negative_factors: List[str],
        confirmation_factors: List[str],
        conflicts: List[Dict],
    ) -> float:
        """Calculate reasoning score."""
        score = 50.0
        
        # Sentiment
        if sentiment == "positive":
            score += 15
        elif sentiment == "negative":
            score -= 15
        
        # Factors
        score += min(len(positive_factors) * 5, 20)
        score -= min(len(negative_factors) * 5, 20)
        score += min(len(confirmation_factors) * 3, 12)
        
        # Conflicts
        score -= min(len(conflicts) * 10, 25)
        
        return round(max(0, min(100, score)), 2)
    
    def _calculate_confidence(self, score: float, evidence: List[Dict], conflicts: List[Dict]) -> float:
        """Calculate confidence."""
        confidence = float(score)
        
        if len(evidence) >= 5:
            confidence += 5
        elif len(evidence) >= 3:
            confidence += 3
        
        confidence -= len(conflicts) * 8
        
        return round(max(0, min(100, confidence)), 2)
    
    def _determine_direction(
        self,
        sentiment: str,
        positive_factors: List[str],
        negative_factors: List[str],
        conflicts: List[Dict],
    ) -> str:
        """Determine direction."""
        pos = len(positive_factors)
        neg = len(negative_factors)
        
        if conflicts and abs(pos - neg) <= 1:
            return "uncertain"
        
        if pos > neg:
            return "bullish"
        
        if neg > pos:
            return "bearish"
        
        if sentiment == "positive":
            return "bullish"
        if sentiment == "negative":
            return "bearish"
        
        return "neutral"
    
    def _strength_label(self, score: float) -> str:
        """Get strength label."""
        if score >= 80:
            return "very_strong"
        if score >= 65:
            return "strong"
        if score >= 50:
            return "moderate"
        if score >= 35:
            return "weak"
        return "very_weak"
    
    def _build_summary(
        self,
        direction: str,
        score: float,
        positive_factors: List[str],
        negative_factors: List[str],
        conflicts: List[Dict],
    ) -> str:
        """Build human-readable summary."""
        if direction == "bullish":
            base = "Reasoning indicates bullish conditions."
        elif direction == "bearish":
            base = "Reasoning indicates bearish conditions."
        elif direction == "uncertain":
            base = "Reasoning indicates conflicting market conditions."
        else:
            base = "Reasoning indicates neutral market conditions."
        
        details = f" Score: {score}%."
        
        if positive_factors:
            details += f" Positive factors: {', '.join(positive_factors[:5])}."
        
        if negative_factors:
            details += f" Negative factors: {', '.join(negative_factors[:5])}."
        
        if conflicts:
            details += " Conflicting signals detected, proceed with caution."
        
        return base + details
    
    # ========================================================
    # PUBLIC API
    # ========================================================
    
    def analyze(self, data: Any, domain: str = "auto") -> Dict[str, Any]:
        """Analyze data with reasoning."""
        return self.reason(data, domain)
    
    def answer(self, question: str) -> str:
        """Answer a question."""
        result = self.reason({"text": question, "type": "question"}, domain="general")
        return result.get("response", "I don't have an answer for that.")
    
    def get_history(self, limit: int = 20) -> List[Dict]:
        """Get reasoning history."""
        return deepcopy(self.history[-limit:]) if self.history else []
    
    def latest(self) -> Optional[Dict]:
        """Get latest reasoning result."""
        return deepcopy(self.last_reasoning) if self.last_reasoning else None
    
    def status(self) -> Dict[str, Any]:
        """Get status."""
        return {
            "module": "reasoning",
            "version": self.VERSION,
            "reasoning_count": self.reasoning_count,
            "history_size": len(self.history),
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "accuracy": self._calculate_accuracy(),
            "last_direction": self.last_reasoning.get("direction") if self.last_reasoning else None,
        }
    
    def _calculate_accuracy(self) -> float:
        """Calculate accuracy."""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return round((self.success_count / total) * 100, 2)
    
    def reset(self) -> bool:
        """Reset engine."""
        self.reasoning_count = 0
        self.history.clear()
        self.success_count = 0
        self.failure_count = 0
        self.last_reasoning = None
        return True


# ============================================================
# GLOBAL INSTANCE
# ============================================================

reasoning_engine = ReasoningEngine()


# ============================================================
# SHORTCUT FUNCTIONS - MENGGUNAKAN reasoning_engine
# ============================================================

def think(data: Any, domain: str = "auto") -> Dict[str, Any]:
    """Quick reasoning shortcut."""
    return reasoning_engine.reason(data, domain)


def answer(question: str) -> str:
    """Quick answer shortcut."""
    return reasoning_engine.answer(question)


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
    
    # Test 1: Market Reasoning
    print("1. Testing market reasoning...")
    try:
        test_data = {
            "features": {
                "keywords": ["bullish", "breakout", "volume"],
                "entities": ["BTC/USD"],
            },
            "analysis": {
                "sentiment": "positive",
            }
        }
        result = reasoning_engine.reason(test_data, domain="market")
        if result and result.get("direction") == "bullish":
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
    
    # Test 2: General Knowledge
    print("\n2. Testing general knowledge...")
    try:
        result = reasoning_engine.answer("What is the capital of France?")
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
    
    # Test 3: Question Answering
    print("\n3. Testing question answering...")
    try:
        result = reasoning_engine.answer("What is AI?")
        if result and "Artificial Intelligence" in result:
            results["question_answering"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Question answering passed")
        else:
            results["question_answering"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Question answering failed")
    except Exception as e:
        results["question_answering"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Question answering failed: {e}")
    
    # Test 4: Status
    print("\n4. Testing status...")
    try:
        status = reasoning_engine.status()
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
        "version": reasoning_engine.VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "ReasoningEngine",
    "reasoning_engine",
    "think",
    "answer",
    "self_test",
]


# ============================================================
# END
# ============================================================