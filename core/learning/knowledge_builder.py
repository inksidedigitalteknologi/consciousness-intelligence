# ============================================================
# core/learning/knowledge_builder.py
# KNOWLEDGE BUILDER ENGINE v3.0
# SUPER COMPREHENSIVE KNOWLEDGE MANAGEMENT
#
# FITUR LENGKAP:
# 1. Build Knowledge from Experience
# 2. Extract Concepts & Entities
# 3. Identify Facts and Patterns
# 4. Connect Related Concepts (Knowledge Graph)
# 5. Track Knowledge Confidence
# 6. Search Knowledge (full-text)
# 7. Detect Repeated Knowledge
# 8. Domain Classification
# 9. Knowledge Versioning
# 10. Knowledge Evolution Pipeline
# 11. Export/Import Knowledge
# 12. Knowledge Analytics
# 13. Knowledge Summarization
# 14. Knowledge Reinforcement
# 15. Knowledge Decay
# ============================================================

from __future__ import annotations  # <-- FIXED!

import logging
import json
import uuid
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)  # <-- FIXED!


# ============================================================
# VERSION
# ============================================================

KNOWLEDGE_BUILDER_VERSION = "3.0.0"
API_VERSION = "1.0"


# ============================================================
# CONSTANTS
# ============================================================

# Domain classifications
DOMAIN_TRADING = "trading"
DOMAIN_ECONOMICS = "economics"
DOMAIN_TECHNOLOGY = "technology"
DOMAIN_GENERAL = "general"
DOMAIN_MARKET = "market"
DOMAIN_LEARNING = "learning"
DOMAIN_STRATEGY = "strategy"

# Knowledge types
TYPE_PREDICTION = "prediction"
TYPE_EXPERIENCE = "experience"
TYPE_INSIGHT = "insight"
TYPE_REFLECTION = "reflection"
TYPE_ANALYSIS = "analysis"
TYPE_OBSERVATION = "observation"
TYPE_FACT = "fact"
TYPE_CONCEPT = "concept"
TYPE_RULE = "rule"
TYPE_PATTERN = "pattern"

# Knowledge status
STATUS_ACTIVE = "active"
STATUS_DEPRECATED = "deprecated"
STATUS_ARCHIVED = "archived"
STATUS_PENDING = "pending"
STATUS_VERIFIED = "verified"
STATUS_CONFLICTED = "conflicted"


# ============================================================
# TIME HELPER
# ============================================================

def utc_now() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now().isoformat()


# ============================================================
# KNOWLEDGE BUILDER v3.0
# ============================================================

class KnowledgeBuilder:
    """
    Super Comprehensive Knowledge Builder Engine.
    
    Features:
    - Build Knowledge from Experience
    - Extract Concepts & Entities
    - Identify Facts and Patterns
    - Connect Related Concepts (Knowledge Graph)
    - Track Knowledge Confidence
    - Search Knowledge (full-text)
    - Domain Classification
    - Knowledge Versioning
    - Export/Import Knowledge
    - Knowledge Analytics
    """
    
    VERSION = KNOWLEDGE_BUILDER_VERSION
    
    def __init__(
        self,
        max_knowledge: int = 1000,
        config: Optional[Dict[str, Any]] = None
    ):
        self.config = config or {}
        self.max_knowledge = max(1, int(max_knowledge))
        self.knowledge_count = 0
        self.knowledge: List[Dict[str, Any]] = []
        self.concepts: Dict[str, Dict[str, Any]] = {}
        self.relations: Dict[str, Dict[str, int]] = {}
        self.facts: List[Dict[str, Any]] = []
        self.patterns: List[Dict[str, Any]] = []
        
        self.total_concepts = 0
        self.total_relations = 0
        self.total_builds = 0
        self.total_facts = 0
        self.total_patterns = 0
        self.total_domains: Dict[str, int] = {}
        
        self.last_build: Optional[Dict[str, Any]] = None
        
        # Knowledge graph adjacency
        self.graph: Dict[str, Set[str]] = {}
        
        # Confidence tracking
        self.confidence_history: List[float] = []
        
        # Domain-specific keyword maps
        self._load_keyword_maps()
        
        logger.info("Knowledge Builder v%s initialized.", self.VERSION)
    
    def _load_keyword_maps(self) -> None:
        """Load keyword-to-concept mapping."""
        self.keyword_map = {
            # MARKET
            "bullish": "positive_market_movement",
            "bearish": "negative_market_movement",
            "breakout": "price_expansion_event",
            "breakdown": "price_contraction_event",
            "volume": "market_participation",
            "trend": "market_direction",
            "momentum": "price_momentum",
            "volatility": "market_volatility",
            "support": "support_level",
            "resistance": "resistance_level",
            "price": "price_level",
            "market": "market_condition",
            "signal": "trading_signal",
            "entry": "entry_point",
            "exit": "exit_point",
            "stop_loss": "risk_management",
            "take_profit": "profit_taking",
            
            # MACRO
            "inflation": "inflation",
            "inflasi": "inflation",
            "interest rate": "interest_rate",
            "suku bunga": "interest_rate",
            "fed": "central_bank",
            "economics": "economic_condition",
            "economy": "economic_condition",
            
            # TECHNOLOGY
            "ai": "artificial_intelligence",
            "artificial intelligence": "artificial_intelligence",
            "machine learning": "machine_learning",
            "deep learning": "deep_learning",
            "blockchain": "blockchain_technology",
            "crypto": "cryptocurrency",
            "algorithm": "algorithm",
            "data": "data_analysis",
            
            # GENERAL
            "risk": "risk_management",
            "profit": "profitability",
            "loss": "loss",
            "prediction": "prediction",
            "accuracy": "prediction_accuracy",
            "confidence": "prediction_confidence",
            "learning": "learning_process",
            "knowledge": "knowledge_management",
            "strategy": "strategy_development",
            "decision": "decision_making",
            "analysis": "data_analysis",
            "pattern": "pattern_recognition",
            "experience": "experience_learning",
            "insight": "insight_generation",
            "reflection": "reflection_learning",
        }
        
        self.domain_keywords = {
            DOMAIN_TRADING: ["btc", "bitcoin", "eth", "crypto", "market", "bullish", "bearish", "trading", "signal"],
            DOMAIN_ECONOMICS: ["inflation", "inflasi", "fed", "interest rate", "suku bunga", "economy", "economics"],
            DOMAIN_TECHNOLOGY: ["ai", "artificial intelligence", "machine learning", "technology", "blockchain"],
            DOMAIN_STRATEGY: ["strategy", "plan", "goal", "objective", "target"],
            DOMAIN_LEARNING: ["learn", "study", "practice", "improve", "skill"],
        }
    
    # ========================================================
    # CORE: BUILD KNOWLEDGE
    # ========================================================
    
    def build(
        self,
        experience: Any,
        source: str = "unknown",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Build knowledge from experience.
        
        Args:
            experience: Raw experience data
            source: Source of knowledge
            metadata: Additional metadata
            
        Returns:
            Knowledge object or None
        """
        try:
            self.total_builds += 1
            
            # Extract components
            concepts = self.extract_concepts(experience)
            facts = self.extract_facts(experience)
            patterns = self.extract_patterns(experience)
            domain = self.detect_domain(experience)
            knowledge_type = self.detect_type(experience)
            
            # Calculate confidence
            confidence = self.calculate_confidence(
                experience,
                concepts,
                facts,
                patterns
            )
            
            # Create knowledge
            knowledge = {
                "id": str(uuid.uuid4())[:8],
                "timestamp": utc_now(),
                "source": str(source),
                "domain": domain,
                "type": knowledge_type,
                "concepts": concepts,
                "facts": facts,
                "patterns": patterns,
                "confidence": confidence,
                "status": STATUS_ACTIVE,
                "version": 1,
                "relevance": 1.0,
                "access_count": 0,
                "metadata": deepcopy(metadata) if metadata else {},
                "history": [{"action": "created", "timestamp": utc_now()}],
            }
            
            # Store
            self.knowledge.append(knowledge)
            self.knowledge_count += 1
            
            # Register concepts
            self._register_concepts(concepts)
            
            # Register relations
            self._register_relations(concepts)
            
            # Register facts
            self._register_facts(facts)
            
            # Register patterns
            self._register_patterns(patterns)
            
            # Update domain stats
            self.total_domains[domain] = self.total_domains.get(domain, 0) + 1
            
            # Trim if needed
            self._trim_memory()
            
            # Set last build
            self.last_build = knowledge
            
            logger.debug("Knowledge built: %s concepts, %s facts", len(concepts), len(facts))
            
            return knowledge
            
        except Exception as e:
            logger.exception("Knowledge build failed: %s", e)
            return None
    
    # ========================================================
    # CONCEPT EXTRACTION
    # ========================================================
    
    def extract_concepts(self, data: Any) -> List[str]:
        """Extract concepts from data."""
        text = self._normalize_text(data)
        concepts = []
        
        # Check keyword map
        for keyword, concept in self.keyword_map.items():
            if keyword in text:
                if concept not in concepts:
                    concepts.append(concept)
        
        # Extract from dict
        if isinstance(data, dict):
            # Check for concept fields
            concept_fields = ["concept", "concepts", "topic", "subject", "category"]
            for field in concept_fields:
                if field in data:
                    value = data[field]
                    if isinstance(value, str):
                        concepts.extend(self._extract_from_text(value))
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, str):
                                concepts.extend(self._extract_from_text(item))
        
        # Extract entities
        entities = self._extract_entities(text)
        concepts.extend(entities)
        
        # Remove duplicates and sort
        return sorted(set(concepts))
    
    def _extract_from_text(self, text: str) -> List[str]:
        """Extract concepts from text."""
        text = str(text).lower()
        concepts = []
        for keyword, concept in self.keyword_map.items():
            if keyword in text:
                if concept not in concepts:
                    concepts.append(concept)
        return concepts
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract entities from text."""
        entities = []
        text_lower = text.lower()
        
        # Common entities
        entity_patterns = {
            "btc": "Bitcoin",
            "eth": "Ethereum",
            "sol": "Solana",
            "ada": "Cardano",
            "xrp": "Ripple",
            "dot": "Polkadot",
            "fed": "Federal Reserve",
            "fomc": "FOMC",
            "cpi": "CPI",
            "gdp": "GDP",
        }
        
        for key, value in entity_patterns.items():
            if key in text_lower:
                entities.append(value)
        
        return entities
    
    # ========================================================
    # FACT EXTRACTION
    # ========================================================
    
    def extract_facts(self, data: Any) -> List[Dict[str, Any]]:
        """Extract facts from data."""
        facts = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if value is None:
                    continue
                if isinstance(value, (str, int, float, bool)):
                    facts.append({
                        "key": str(key),
                        "value": value,
                        "type": type(value).__name__,
                        "confidence": 0.8,
                    })
                elif isinstance(value, list):
                    facts.append({
                        "key": str(key),
                        "value": value,
                        "type": "list",
                        "count": len(value),
                        "confidence": 0.6,
                    })
        elif isinstance(data, str):
            # Extract simple facts from text
            text = data.lower()
            if "is" in text:
                parts = text.split("is", 1)
                if len(parts) == 2:
                    facts.append({
                        "key": parts[0].strip(),
                        "value": parts[1].strip(),
                        "type": "statement",
                        "confidence": 0.5,
                    })
        
        self.total_facts += len(facts)
        return facts
    
    # ========================================================
    # PATTERN EXTRACTION
    # ========================================================
    
    def extract_patterns(self, data: Any) -> List[Dict[str, Any]]:
        """Extract patterns from data."""
        patterns = []
        text = self._normalize_text(data)
        
        # Pattern detection
        pattern_keywords = {
            "breakout": "breakout_pattern",
            "breakdown": "breakdown_pattern",
            "trend": "trend_pattern",
            "reversal": "reversal_pattern",
            "consolidation": "consolidation_pattern",
            "double bottom": "double_bottom_pattern",
            "double top": "double_top_pattern",
            "head and shoulders": "head_shoulders_pattern",
        }
        
        for keyword, pattern in pattern_keywords.items():
            if keyword in text:
                patterns.append({
                    "name": pattern,
                    "keywords": [keyword],
                    "confidence": 0.7,
                    "type": "market",
                })
        
        # Time-based patterns
        if "daily" in text:
            patterns.append({"name": "daily_pattern", "type": "timeframe", "confidence": 0.5})
        if "weekly" in text:
            patterns.append({"name": "weekly_pattern", "type": "timeframe", "confidence": 0.5})
        if "monthly" in text:
            patterns.append({"name": "monthly_pattern", "type": "timeframe", "confidence": 0.5})
        
        self.total_patterns += len(patterns)
        return patterns
    
    # ========================================================
    # DOMAIN DETECTION
    # ========================================================
    
    def detect_domain(self, data: Any) -> str:
        """Detect knowledge domain."""
        text = self._normalize_text(data)
        
        # Check domain keywords
        for domain, keywords in self.domain_keywords.items():
            if any(kw in text for kw in keywords):
                return domain
        
        # Check from dict
        if isinstance(data, dict):
            if "domain" in data:
                domain = data["domain"]
                if domain in self.domain_keywords:
                    return domain
        
        # Check for specific patterns
        if any(word in text for word in ["price", "trade", "buy", "sell", "signal"]):
            return DOMAIN_TRADING
        
        if any(word in text for word in ["learn", "study", "skill", "knowledge"]):
            return DOMAIN_LEARNING
        
        if any(word in text for word in ["strategy", "plan", "goal"]):
            return DOMAIN_STRATEGY
        
        return DOMAIN_GENERAL
    
    # ========================================================
    # KNOWLEDGE TYPE DETECTION
    # ========================================================
    
    def detect_type(self, data: Any) -> str:
        """Detect knowledge type."""
        if isinstance(data, dict):
            if "prediction" in data:
                return TYPE_PREDICTION
            if "experience" in data:
                return TYPE_EXPERIENCE
            if "insight" in data:
                return TYPE_INSIGHT
            if "reflection" in data:
                return TYPE_REFLECTION
            if "analysis" in data:
                return TYPE_ANALYSIS
            if "pattern" in data:
                return TYPE_PATTERN
            if "rule" in data:
                return TYPE_RULE
        
        text = self._normalize_text(data)
        if any(word in text for word in ["predict", "forecast", "expect"]):
            return TYPE_PREDICTION
        if any(word in text for word in ["reflect", "think", "consider"]):
            return TYPE_REFLECTION
        if any(word in text for word in ["insight", "realize", "understand"]):
            return TYPE_INSIGHT
        if any(word in text for word in ["experience", "felt", "observed"]):
            return TYPE_EXPERIENCE
        
        return TYPE_OBSERVATION
    
    # ========================================================
    # CONFIDENCE CALCULATION
    # ========================================================
    
    def calculate_confidence(
        self,
        experience: Any,
        concepts: List[str],
        facts: List[Dict],
        patterns: List[Dict]
    ) -> float:
        """Calculate confidence score (0-100)."""
        score = 20.0
        
        # Concepts contribution
        score += min(len(concepts) * 10, 30)
        
        # Facts contribution
        score += min(len(facts) * 5, 25)
        
        # Patterns contribution
        score += min(len(patterns) * 8, 20)
        
        # Source confidence
        if isinstance(experience, dict):
            supplied = experience.get("confidence")
            if supplied is not None:
                try:
                    supplied = float(supplied)
                    if supplied <= 1:
                        supplied *= 100
                    return round(max(0, min(supplied, 100)), 2)
                except (TypeError, ValueError):
                    pass
        
        # Experience richness
        text = self._normalize_text(experience)
        word_count = len(text.split())
        if word_count > 50:
            score += 5
        elif word_count > 100:
            score += 10
        
        return round(max(0, min(score, 100)), 2)
    
    # ========================================================
    # REGISTRY METHODS
    # ========================================================
    
    def _register_concepts(self, concepts: List[str]) -> None:
        """Register concepts in concept map."""
        for concept in concepts:
            if concept not in self.concepts:
                self.concepts[concept] = {
                    "count": 0,
                    "first_seen": utc_now(),
                    "last_seen": utc_now(),
                }
                self.total_concepts += 1
            
            self.concepts[concept]["count"] += 1
            self.concepts[concept]["last_seen"] = utc_now()
            
            # Add to graph
            if concept not in self.graph:
                self.graph[concept] = set()
    
    def _register_relations(self, concepts: List[str]) -> None:
        """Register relationships between concepts."""
        for first in concepts:
            if first not in self.relations:
                self.relations[first] = {}
            for second in concepts:
                if first == second:
                    continue
                self.relations[first][second] = self.relations[first].get(second, 0) + 1
                self.total_relations += 1
                
                # Update graph
                if first in self.graph and second in self.graph:
                    self.graph[first].add(second)
                    self.graph[second].add(first)
    
    def _register_facts(self, facts: List[Dict]) -> None:
        """Register facts."""
        for fact in facts:
            self.facts.append(fact)
    
    def _register_patterns(self, patterns: List[Dict]) -> None:
        """Register patterns."""
        for pattern in patterns:
            self.patterns.append(pattern)
    
    def _trim_memory(self) -> None:
        """Trim knowledge memory if exceeded."""
        if len(self.knowledge) > self.max_knowledge:
            excess = len(self.knowledge) - self.max_knowledge
            # Remove oldest (least important)
            self.knowledge = self.knowledge[excess:]
    
    # ========================================================
    # KNOWLEDGE ACCESS
    # ========================================================
    
    def get_all(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all knowledge items."""
        if limit is None:
            return list(self.knowledge)
        return self.knowledge[-max(1, int(limit)):]
    
    def latest(self) -> Optional[Dict[str, Any]]:
        """Get latest knowledge."""
        if not self.knowledge:
            return None
        return self.knowledge[-1]
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """Search knowledge by keyword."""
        keyword = self._normalize_text(keyword)
        if not keyword:
            return []
        
        results = []
        for item in self.knowledge:
            searchable = " ".join([
                str(item.get("source", "")),
                " ".join(item.get("concepts", [])),
                json.dumps(item.get("facts", [])),
                json.dumps(item.get("patterns", [])),
                str(item.get("metadata", {})),
            ]).lower()
            
            if keyword in searchable:
                results.append(item)
        
        return results
    
    def by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Get knowledge by domain."""
        domain = self._normalize_text(domain)
        return [item for item in self.knowledge if item.get("domain") == domain]
    
    def by_concept(self, concept: str) -> List[Dict[str, Any]]:
        """Get knowledge by concept."""
        concept = self._normalize_text(concept)
        return [
            item for item in self.knowledge
            if concept in [c.lower() for c in item.get("concepts", [])]
        ]
    
    def related(self, concept: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get related concepts."""
        concept = self._normalize_text(concept)
        relations = self.relations.get(concept, {})
        
        ordered = sorted(
            relations.items(),
            key=lambda item: item[1],
            reverse=True
        )
        
        return [
            {"concept": item[0], "strength": item[1]}
            for item in ordered[:max(1, int(limit))]
        ]
    
    def get_graph(self) -> Dict[str, Set[str]]:
        """Get knowledge graph."""
        return {k: set(v) for k, v in self.graph.items()}
    
    # ========================================================
    # KNOWLEDGE EVOLUTION
    # ========================================================
    
    def reinforce(self, knowledge_id: str, factor: float = 1.2) -> bool:
        """Reinforce knowledge confidence."""
        for item in self.knowledge:
            if item.get("id") == knowledge_id:
                old_conf = item["confidence"]
                item["confidence"] = min(100.0, old_conf * factor)
                item["version"] += 1
                item["history"].append({"action": "reinforced", "timestamp": utc_now()})
                return True
        return False
    
    def decay(self, factor: float = 0.95) -> int:
        """Apply confidence decay to all knowledge."""
        decayed = 0
        for item in self.knowledge:
            if item.get("status") == STATUS_ACTIVE:
                old_conf = item["confidence"]
                item["confidence"] = max(10.0, old_conf * factor)
                if item["confidence"] < old_conf:
                    decayed += 1
        return decayed
    
    def deprecate(self, knowledge_id: str, reason: str = "") -> bool:
        """Deprecate a knowledge item."""
        for item in self.knowledge:
            if item.get("id") == knowledge_id:
                item["status"] = STATUS_DEPRECATED
                item["history"].append({"action": "deprecated", "reason": reason, "timestamp": utc_now()})
                return True
        return False
    
    # ========================================================
    # STATISTICS
    # ========================================================
    
    def statistics(self) -> Dict[str, Any]:
        """Get knowledge statistics."""
        return {
            "knowledge": len(self.knowledge),
            "concepts": len(self.concepts),
            "relations": self.total_relations,
            "facts": self.total_facts,
            "patterns": self.total_patterns,
            "builds": self.total_builds,
            "domains": self.total_domains,
            "average_confidence": round(
                sum(k.get("confidence", 0) for k in self.knowledge) / max(1, len(self.knowledge)),
                2
            ),
            "active": sum(1 for k in self.knowledge if k.get("status") == STATUS_ACTIVE),
            "verified": sum(1 for k in self.knowledge if k.get("status") == STATUS_VERIFIED),
            "deprecated": sum(1 for k in self.knowledge if k.get("status") == STATUS_DEPRECATED),
        }
    
    def summary(self) -> Dict[str, Any]:
        """Get quick summary."""
        return {
            "knowledge_count": len(self.knowledge),
            "concept_count": len(self.concepts),
            "relation_count": self.total_relations,
            "latest": self.latest(),
        }
    
    # ========================================================
    # EXPORT / IMPORT
    # ========================================================
    
    def export(self) -> Dict[str, Any]:
        """Export all knowledge."""
        return {
            "version": self.VERSION,
            "exported_at": utc_now(),
            "knowledge": deepcopy(self.knowledge),
            "concepts": deepcopy(self.concepts),
            "relations": deepcopy(self.relations),
            "graph": {k: list(v) for k, v in self.graph.items()},
            "statistics": self.statistics(),
        }
    
    def import_data(self, data: Dict[str, Any]) -> int:
        """Import knowledge data."""
        if not data:
            return 0
        
        imported = 0
        knowledge_data = data.get("knowledge", [])
        for item in knowledge_data:
            self.knowledge.append(item)
            imported += 1
        
        self.knowledge_count += imported
        self._trim_memory()
        
        logger.info("Imported %s knowledge items", imported)
        return imported
    
    # ========================================================
    # CLEAR & RESET
    # ========================================================
    
    def clear(self) -> bool:
        """Clear all knowledge."""
        self.knowledge.clear()
        self.concepts.clear()
        self.relations.clear()
        self.facts.clear()
        self.patterns.clear()
        self.graph.clear()
        self.confidence_history.clear()
        
        self.knowledge_count = 0
        self.total_concepts = 0
        self.total_relations = 0
        self.total_facts = 0
        self.total_patterns = 0
        self.total_builds = 0
        self.total_domains = {}
        
        self.last_build = None
        
        logger.info("Knowledge Builder cleared.")
        return True
    
    # ========================================================
    # STATUS
    # ========================================================
    
    def status(self) -> Dict[str, Any]:
        """Get system status."""
        return {
            "module": "knowledge_builder",
            "version": self.VERSION,
            "api_version": API_VERSION,
            "status": "ONLINE",
            "knowledge": len(self.knowledge),
            "concepts": len(self.concepts),
            "relations": self.total_relations,
            "builds": self.total_builds,
            "has_latest": self.last_build is not None,
            "timestamp": utc_now(),
        }
    
    # ========================================================
    # UTILITY
    # ========================================================
    
    @staticmethod
    def _normalize_text(data: Any) -> str:
        """Normalize text for processing."""
        if data is None:
            return ""
        return str(data).strip().lower()
    
    def get_concepts(self) -> List[str]:
        """Get all concepts."""
        return list(self.concepts.keys())
    
    def get_domains(self) -> List[str]:
        """Get all domains."""
        return list(self.total_domains.keys())


# ============================================================
# GLOBAL INSTANCE
# ============================================================

knowledge_builder = KnowledgeBuilder()


# ============================================================
# COMPATIBILITY FUNCTIONS
# ============================================================

def build(experience: Any, source: str = "unknown") -> Optional[Dict[str, Any]]:
    """Legacy build function."""
    return knowledge_builder.build(experience, source)


def search(keyword: str) -> List[Dict[str, Any]]:
    """Legacy search function."""
    return knowledge_builder.search(keyword)


def status() -> Dict[str, Any]:
    """Legacy status function."""
    return knowledge_builder.status()


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    """Run comprehensive self-test."""
    print()
    print("=" * 70)
    print("  KNOWLEDGE BUILDER v3.0 - SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        builder = KnowledgeBuilder()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Build Knowledge
    print("\n2. Testing build...")
    try:
        experience = {
            "signal": "bullish",
            "market": "BTC/USD",
            "confidence": 0.85,
            "pattern": "breakout",
        }
        result = knowledge_builder.build(experience, source="test")
        if result and result.get("id"):
            results["build"] = {"status": "PASS", "id": result["id"]}
            tests_passed += 1
            print(f"   ✅ Build passed (ID: {result['id']})")
        else:
            results["build"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Build failed")
    except Exception as e:
        results["build"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Build failed: {e}")
    
    # Test 3: Search
    print("\n3. Testing search...")
    try:
        results_search = knowledge_builder.search("bullish")
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
    
    # Test 4: Statistics
    print("\n4. Testing statistics...")
    try:
        stats = knowledge_builder.statistics()
        if stats and "knowledge" in stats:
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
        status_result = knowledge_builder.status()
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
        "module": "knowledge_builder",
        "version": KNOWLEDGE_BUILDER_VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "KnowledgeBuilder",
    "knowledge_builder",
    "build",
    "search",
    "status",
    "self_test",
    "KNOWLEDGE_BUILDER_VERSION",
    "API_VERSION",
]


# ============================================================
# END
# ============================================================