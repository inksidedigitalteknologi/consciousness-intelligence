# core/perception.py
# ============================================================
# INKSIDE DIGITAL - PERCEPTION ENGINE
# Comprehensive input analysis: type, entities, sentiment, concepts
# Deterministic — NO RANDOM
# ============================================================

import re
import logging
from datetime import datetime
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


# ============================================================
# KEYWORD MAPS
# ============================================================

POSITIVE_KEYWORDS = {
    "bullish", "buy", "up", "profit", "gain", "strong", "positive",
    "rise", "surge", "rally", "breakout", "support", "growth",
    "success", "win", "bull", "long", "higher", "boost", "improve",
    "optimistic", "confident", "recovery", "expand", "accelerate",
}

NEGATIVE_KEYWORDS = {
    "bearish", "sell", "down", "loss", "weak", "negative",
    "drop", "crash", "dump", "breakdown", "resistance", "fear",
    "fail", "lose", "bear", "short", "lower", "decline", "fall",
    "pessimistic", "uncertain", "recession", "contract", "slowdown",
}

CONCEPT_MAP = {
    "volatility": {"volatile", "volatility", "swing", "fluctuation", "unstable"},
    "momentum": {"momentum", "trend", "direction", "velocity", "impulse"},
    "liquidity": {"liquidity", "volume", "flow", "depth", "spread"},
    "risk": {"risk", "danger", "exposure", "drawdown", "loss"},
    "trend": {"trend", "uptrend", "downtrend", "sideways", "range"},
    "reversal": {"reversal", "inversion", "turn", "flip", "rotate"},
    "breakout": {"breakout", "break", "escape", "clearing"},
    "consolidation": {"consolidation", "range", "flat", "sideways", "accumulation"},
    "learning": {"learn", "learning", "study", "train", "adapt"},
    "prediction": {"predict", "prediction", "forecast", "project", "anticipate"},
    "decision": {"decide", "decision", "choose", "select", "opt"},
    "reflection": {"reflect", "reflection", "review", "examine", "consider"},
    "reasoning": {"reason", "reasoning", "logic", "deduce", "infer"},
    "confidence": {"confidence", "sure", "certain", "assured", "determined"},
    "uncertainty": {"uncertain", "unknown", "ambiguous", "unclear", "doubt"},
    "signal": {"signal", "indicator", "sign", "alert", "cue"},
    "noise": {"noise", "chaos", "random", "distraction", "clutter"},
}

ASSET_PATTERN = re.compile(r'\b([A-Z]{2,6})(?:[/-]([A-Z]{2,6}))?\b')
NUMERIC_KEYS = {"price", "volume", "amount", "confidence", "value", "quantity", "size"}
TEMPORAL_KEYS = {"timestamp", "date", "time", "datetime", "when", "expiry"}
INDICATOR_KEYS = {"signal", "trend", "pattern", "indicator", "direction"}
ACTION_KEYS = {"action", "command", "operation", "task", "method"}
MARKET_KEYS = {"market", "symbol", "price", "pair", "ticker", "asset", "exchange"}
TEXT_KEYS = {"text", "content", "message", "body", "note", "comment"}
EVENT_KEYS = {"event", "trigger", "alert", "notification", "occurrence"}
QUERY_KEYS = {"question", "query", "ask", "prompt", "request"}


# ============================================================
# PERCEPTION ENGINE
# ============================================================

class PerceptionEngine:
    """
    Comprehensive perception engine.

    Pipeline:
        1. detect_type       → klasifikasi tipe input
        2. extract_entities  → NER deterministik
        3. detect_sentiment  → analisis sentimen keyword-based
        4. extract_concepts  → konsep abstrak
        5. compute_scores    → confidence, clarity, relevance
    """

    VERSION = "1.0.0"

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.name = "Perception Engine"
        self.stats = {
            "total_analyses": 0,
            "by_type": {},
            "by_sentiment": {},
        }
        logger.info(f"PerceptionEngine v{self.VERSION} initialized")

    # ------------------------------------------------------------
    # MAIN ENTRY
    # ------------------------------------------------------------

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze input data. Deterministic. No random.

        Returns dict compatible with brain.py _perceive().
        """
        start = datetime.now()

        if not isinstance(data, dict):
            data = {"raw": data}

        data_type = self.detect_type(data)
        entities = self.extract_entities(data)
        sentiment, sentiment_score = self.detect_sentiment(data)
        concepts = self.extract_concepts(data)
        confidence, clarity, relevance = self.compute_scores(
            data, entities, concepts, data_type
        )

        elapsed = (datetime.now() - start).total_seconds() * 1000

        # Update stats
        self.stats["total_analyses"] += 1
        self.stats["by_type"][data_type] = self.stats["by_type"].get(data_type, 0) + 1
        self.stats["by_sentiment"][sentiment] = self.stats["by_sentiment"].get(sentiment, 0) + 1

        result = {
            "type": data_type,
            "entities": entities,
            "sentiment": sentiment,
            "sentiment_score": round(sentiment_score, 3),
            "concepts": concepts,
            "confidence": round(confidence, 3),
            "clarity": round(clarity, 3),
            "relevance": round(relevance, 3),
            "processing_time": round(elapsed, 2),
            "raw": data,
            "is_fallback": False,  # engine ini asli, bukan fallback
            "engine_version": self.VERSION,
        }

        return result

    # ------------------------------------------------------------
    # 1. TYPE DETECTION
    # ------------------------------------------------------------

    def detect_type(self, data: Dict[str, Any]) -> str:
        keys = {str(k).lower() for k in data.keys()}

        if keys & MARKET_KEYS:
            return "market"
        if keys & QUERY_KEYS:
            return "query"
        if keys & INDICATOR_KEYS:
            return "signal"
        if keys & EVENT_KEYS:
            return "event"
        if keys & ACTION_KEYS:
            return "command"
        if keys & TEXT_KEYS:
            return "text"
        return "generic"

    # ------------------------------------------------------------
    # 2. ENTITY EXTRACTION
    # ------------------------------------------------------------

    def extract_entities(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        entities: List[Dict[str, Any]] = []
        seen = set()

        def add(etype: str, name: str, value: Any = None):
            key = (etype, str(name).lower())
            if key in seen:
                return
            seen.add(key)
            entry = {"type": etype, "name": str(name)}
            if value is not None:
                entry["value"] = value
            entities.append(entry)

        for raw_key, value in data.items():
            key = str(raw_key).lower()

            # Asset-like keys
            if key in {"symbol", "pair", "asset", "market", "ticker"}:
                add("asset", str(value), value)
                continue

            # Numeric
            if key in NUMERIC_KEYS:
                add("numeric", key, value)
                continue

            # Temporal
            if key in TEMPORAL_KEYS:
                add("temporal", key, value)
                continue

            # Indicator
            if key in INDICATOR_KEYS:
                add("indicator", str(value), value)
                continue

            # Action
            if key in ACTION_KEYS:
                add("action", str(value), value)
                continue

            # Free-text: scan for asset symbols
            if isinstance(value, str):
                for m in ASSET_PATTERN.finditer(value):
                    sym = m.group(1)
                    if sym not in {"THE", "AND", "FOR", "YOU", "ARE", "NOT", "ALL"}:
                        add("asset", sym, None)

        return entities

    # ------------------------------------------------------------
    # 3. SENTIMENT DETECTION
    # ------------------------------------------------------------

    def detect_sentiment(self, data: Dict[str, Any]) -> Tuple[str, float]:
        text_parts: List[str] = []

        for key in ("text", "content", "message", "sentiment", "signal", "trend", "note"):
            val = data.get(key)
            if isinstance(val, str):
                text_parts.append(val.lower())

        # Serialize small values
        for k, v in data.items():
            if isinstance(v, str) and len(v) < 200:
                text_parts.append(v.lower())

        text = " ".join(text_parts)
        if not text.strip():
            return "neutral", 0.0

        tokens = re.findall(r"[a-z]+", text)
        if not tokens:
            return "neutral", 0.0

        pos = sum(1 for t in tokens if t in POSITIVE_KEYWORDS)
        neg = sum(1 for t in tokens if t in NEGATIVE_KEYWORDS)
        total = pos + neg

        if total == 0:
            return "neutral", 0.0

        score = (pos - neg) / total  # -1 .. +1
        if score > 0.15:
            return "positive", score
        if score < -0.15:
            return "negative", score
        return "neutral", score

    # ------------------------------------------------------------
    # 4. CONCEPT EXTRACTION
    # ------------------------------------------------------------

    def extract_concepts(self, data: Dict[str, Any]) -> List[str]:
        # Collect tokens from all string values
        tokens = set()
        for v in data.values():
            if isinstance(v, str):
                tokens.update(re.findall(r"[a-z]+", v.lower()))
            elif isinstance(v, (list, tuple)):
                for item in v:
                    if isinstance(item, str):
                        tokens.update(re.findall(r"[a-z]+", item.lower()))

        # Also include keys
        for k in data.keys():
            tokens.update(re.findall(r"[a-z]+", str(k).lower()))

        concepts = []
        for concept, kws in CONCEPT_MAP.items():
            if tokens & kws:
                concepts.append(concept)

        return concepts

    # ------------------------------------------------------------
    # 5. SCORE COMPUTATION
    # ------------------------------------------------------------

    def compute_scores(
        self,
        data: Dict[str, Any],
        entities: List[Dict[str, Any]],
        concepts: List[str],
        data_type: str,
    ) -> Tuple[float, float, float]:
        # Confidence: explicit field wins, else from evidence
        explicit = data.get("confidence")
        if isinstance(explicit, (int, float)):
            confidence = max(0.0, min(1.0, float(explicit)))
        else:
            evidence = len(entities) * 0.1 + len(concepts) * 0.05
            confidence = min(0.95, 0.4 + evidence)

        # Clarity: ratio of non-null fields
        total_fields = max(1, len(data))
        filled = sum(1 for v in data.values() if v not in (None, "", [], {}))
        clarity = filled / total_fields

        # Relevance: apakah tipe data relevan dengan field yang ada
        relevance_bonus = {
            "market": 0.2,
            "signal": 0.2,
            "query": 0.1,
            "event": 0.1,
            "command": 0.1,
            "text": 0.05,
            "generic": 0.0,
        }.get(data_type, 0.0)

        concept_bonus = min(0.3, len(concepts) * 0.05)
        relevance = min(1.0, 0.4 + relevance_bonus + concept_bonus)

        return confidence, clarity, relevance

    # ------------------------------------------------------------
    # UTILITY
    # ------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        return {
            "version": self.VERSION,
            "name": self.name,
            **self.stats,
        }

    def status(self) -> Dict[str, Any]:
        return {
            "engine": self.name,
            "version": self.VERSION,
            "status": "ONLINE",
            "total_analyses": self.stats["total_analyses"],
        }


# ============================================================
# SINGLETON INSTANCE
# ============================================================

perception = PerceptionEngine()


# ============================================================
# MODULE EXPORTS
# ============================================================

__all__ = [
    "PerceptionEngine",
    "perception",
]
