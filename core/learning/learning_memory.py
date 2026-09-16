# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# LEARNING MEMORY CORE
# VERSION 2.0
#
# GENERAL-PURPOSE INTELLIGENCE MEMORY
#
# ============================================================
#
# DESIGN GOALS
# ------------------------------------------------------------
# 1. General-purpose memory
# 2. Trading-compatible
# 3. Knowledge-compatible
# 4. Experience-compatible
# 5. Observation-compatible
# 6. Insight-compatible
# 7. Thread-safe
# 8. Deduplication
# 9. Searchable
# 10. Confidence-aware
# 11. Importance-aware
# 12. Source-aware
# 13. Tag-aware
# 14. Serializable
# 15. Future database/vector-store ready
#
# ============================================================

import logging
import threading
import hashlib
import copy

from datetime import datetime
from collections import deque
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


# ============================================================
# METADATA
# ============================================================

MEMORY_NAME = "Learning Memory"
MEMORY_VERSION = "2.0"


# ============================================================
# LEARNING MEMORY
# ============================================================

class LearningMemory:

    # ========================================================
    # INIT
    # ========================================================

    def __init__(
        self,
        max_size: int = 10000,
        deduplicate: bool = True,
    ):

        self.max_size = max(100, int(max_size))

        self.deduplicate = deduplicate

        # ----------------------------------------------------
        # Memory stores
        # ----------------------------------------------------

        self.observations = deque(
            maxlen=self.max_size
        )

        self.experiences = deque(
            maxlen=self.max_size
        )

        self.insights = deque(
            maxlen=self.max_size
        )

        self.knowledge = deque(
            maxlen=self.max_size
        )

        self.feedback = deque(
            maxlen=self.max_size
        )

        self.decisions = deque(
            maxlen=self.max_size
        )

        # ----------------------------------------------------
        # Global memory index
        # ----------------------------------------------------

        self.index = {}

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        self.total_writes = 0
        self.duplicate_writes = 0
        self.total_reads = 0

        # ----------------------------------------------------
        # Thread safety
        # ----------------------------------------------------

        self.lock = threading.RLock()

        logger.info(
            "%s v%s initialized.",
            MEMORY_NAME,
            MEMORY_VERSION,
        )

    # ========================================================
    # INTERNAL HELPERS
    # ========================================================

    def _timestamp(self) -> str:

        return datetime.now().isoformat()

    # --------------------------------------------------------

    def _safe_copy(self, value: Any) -> Any:

        try:
            return copy.deepcopy(value)

        except Exception:

            return value

    # --------------------------------------------------------

    def _fingerprint(self, value: Any) -> str:

        try:

            normalized = repr(
                value
            )

            return hashlib.sha256(
                normalized.encode(
                    "utf-8",
                    errors="ignore",
                )
            ).hexdigest()[:20]

        except Exception:

            return hashlib.sha256(
                str(id(value)).encode()
            ).hexdigest()[:20]

    # --------------------------------------------------------

    def _create_item(
        self,
        memory_type: str,
        value: Any,
        category: str = "general",
        source: str = "unknown",
        confidence: float = 0.0,
        importance: float = 0.0,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        safe_value = self._safe_copy(
            value
        )

        fingerprint = self._fingerprint(
            {
                "type": memory_type,
                "category": category,
                "value": safe_value,
            }
        )

        return {

            "id": fingerprint,

            "time":
                self._timestamp(),

            "type":
                memory_type,

            "category":
                category,

            "source":
                source,

            "confidence":
                self._normalize_score(
                    confidence
                ),

            "importance":
                self._normalize_score(
                    importance
                ),

            "tags":
                list(tags or []),

            "data":
                safe_value,

            "metadata":
                self._safe_copy(
                    metadata or {}
                ),

        }

    # --------------------------------------------------------

    def _normalize_score(
        self,
        value: Any,
    ) -> float:

        try:

            value = float(value)

        except Exception:

            return 0.0

        return round(
            max(
                0.0,
                min(
                    100.0,
                    value,
                ),
            ),
            2,
        )

    # --------------------------------------------------------

    def _store(
        self,
        collection,
        item: Dict[str, Any],
    ) -> Dict[str, Any]:

        with self.lock:

            memory_id = item["id"]

            if (
                self.deduplicate
                and memory_id in self.index
            ):

                self.duplicate_writes += 1

                return self._safe_copy(
                    self.index[memory_id]
                )

            collection.append(
                item
            )

            self.index[memory_id] = (
                self._safe_copy(item)
            )

            self.total_writes += 1

            return self._safe_copy(
                item
            )

    # ========================================================
    # OBSERVATION
    # ========================================================

    def store_observation(
        self,
        data: Any,
        category: str = "general",
        source: str = "unknown",
        confidence: float = 0,
        importance: float = 0,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        item = self._create_item(
            memory_type="observation",
            value=data,
            category=category,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata,
        )

        return self._store(
            self.observations,
            item,
        )

    # ========================================================
    # EXPERIENCE
    # ========================================================

    def store_experience(
        self,
        experience: Any,
        category: str = "general",
        source: str = "system",
        confidence: float = 0,
        importance: float = 0,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        item = self._create_item(
            memory_type="experience",
            value=experience,
            category=category,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata,
        )

        return self._store(
            self.experiences,
            item,
        )

    # ========================================================
    # KNOWLEDGE
    # ========================================================

    def store_knowledge(
        self,
        knowledge: Any,
        category: str = "general",
        source: str = "unknown",
        confidence: float = 0,
        importance: float = 0,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        item = self._create_item(
            memory_type="knowledge",
            value=knowledge,
            category=category,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata,
        )

        return self._store(
            self.knowledge,
            item,
        )

    # ========================================================
    # INSIGHT
    # ========================================================

    def store_insight(
        self,
        insight: Any,
        category: str = "general",
        source: str = "system",
        confidence: float = 0,
        importance: float = 0,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        item = self._create_item(
            memory_type="insight",
            value=insight,
            category=category,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata,
        )

        return self._store(
            self.insights,
            item,
        )

    # ========================================================
    # FEEDBACK
    # ========================================================

    def store_feedback(
        self,
        feedback: Any,
        category: str = "general",
        source: str = "user",
        confidence: float = 0,
        importance: float = 0,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        item = self._create_item(
            memory_type="feedback",
            value=feedback,
            category=category,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata,
        )

        return self._store(
            self.feedback,
            item,
        )

    # ========================================================
    # DECISION
    # ========================================================

    def store_decision(
        self,
        decision: Any,
        category: str = "general",
        source: str = "system",
        confidence: float = 0,
        importance: float = 0,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        item = self._create_item(
            memory_type="decision",
            value=decision,
            category=category,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata,
        )

        return self._store(
            self.decisions,
            item,
        )

    # ========================================================
    # GENERIC STORE
    # ========================================================

    def store(
        self,
        memory_type: str,
        data: Any,
        **kwargs,
    ) -> Dict[str, Any]:

        memory_type = str(
            memory_type
        ).lower().strip()

        mapping = {

            "observation":
                self.store_observation,

            "experience":
                self.store_experience,

            "knowledge":
                self.store_knowledge,

            "insight":
                self.store_insight,

            "feedback":
                self.store_feedback,

            "decision":
                self.store_decision,

        }

        handler = mapping.get(
            memory_type
        )

        if handler is None:

            raise ValueError(
                f"Unsupported memory type: "
                f"{memory_type}"
            )

        return handler(
            data,
            **kwargs,
        )

    # ========================================================
    # INTERNAL COLLECTION READ
    # ========================================================

    def _read(
        self,
        collection,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:

        with self.lock:

            self.total_reads += 1

            try:
                limit = max(
                    1,
                    int(limit),
                )
            except Exception:
                limit = 100

            return self._safe_copy(
                list(collection)[-limit:]
            )

    # ========================================================
    # READ METHODS
    # ========================================================

    def get_observations(
        self,
        limit: int = 100,
    ):

        return self._read(
            self.observations,
            limit,
        )

    # --------------------------------------------------------

    def get_experiences(
        self,
        limit: int = 100,
    ):

        return self._read(
            self.experiences,
            limit,
        )

    # --------------------------------------------------------

    def get_knowledge(
        self,
        limit: int = 100,
    ):

        return self._read(
            self.knowledge,
            limit,
        )

    # --------------------------------------------------------

    def get_insights(
        self,
        limit: int = 100,
    ):

        return self._read(
            self.insights,
            limit,
        )

    # --------------------------------------------------------

    def get_feedback(
        self,
        limit: int = 100,
    ):

        return self._read(
            self.feedback,
            limit,
        )

    # --------------------------------------------------------

    def get_decisions(
        self,
        limit: int = 100,
    ):

        return self._read(
            self.decisions,
            limit,
        )

    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query: Any,
        memory_type: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:

        query_text = str(
            query
        ).lower()

        with self.lock:

            collections = {

                "observation":
                    self.observations,

                "experience":
                    self.experiences,

                "knowledge":
                    self.knowledge,

                "insight":
                    self.insights,

                "feedback":
                    self.feedback,

                "decision":
                    self.decisions,

            }

            if memory_type:

                selected = collections.get(
                    memory_type.lower()
                )

                if selected is None:
                    return []

                sources = [selected]

            else:

                sources = list(
                    collections.values()
                )

            results = []

            for collection in sources:

                for item in reversed(
                    list(collection)
                ):

                    if category:

                        if (
                            str(
                                item.get(
                                    "category",
                                    "",
                                )
                            ).lower()
                            !=
                            str(
                                category
                            ).lower()
                        ):
                            continue

                    try:

                        searchable = repr(
                            item
                        ).lower()

                        if query_text in searchable:

                            results.append(
                                self._safe_copy(
                                    item
                                )
                            )

                    except Exception:

                        continue

                    if len(results) >= limit:

                        return results

            self.total_reads += 1

            return results

    # ========================================================
    # RECENT
    # ========================================================

    def recent(
        self,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:

        all_items = []

        with self.lock:

            for collection in (
                self.observations,
                self.experiences,
                self.knowledge,
                self.insights,
                self.feedback,
                self.decisions,
            ):

                all_items.extend(
                    list(collection)
                )

        all_items.sort(
            key=lambda x:
                x.get(
                    "time",
                    "",
                ),
            reverse=True,
        )

        return self._safe_copy(
            all_items[:limit]
        )

    # ========================================================
    # STATS
    # ========================================================

    def stats(self) -> Dict[str, Any]:

        with self.lock:

            return {

                "observations":
                    len(
                        self.observations
                    ),

                "experiences":
                    len(
                        self.experiences
                    ),

                "knowledge":
                    len(
                        self.knowledge
                    ),

                "insights":
                    len(
                        self.insights
                    ),

                "feedback":
                    len(
                        self.feedback
                    ),

                "decisions":
                    len(
                        self.decisions
                    ),

                "total":
                    self.total_memory(),

                "writes":
                    self.total_writes,

                "duplicates":
                    self.duplicate_writes,

                "reads":
                    self.total_reads,

            }

    # ========================================================
    # TOTAL
    # ========================================================

    def total_memory(self) -> int:

        return (

            len(self.observations)
            + len(self.experiences)
            + len(self.knowledge)
            + len(self.insights)
            + len(self.feedback)
            + len(self.decisions)

        )

    # ========================================================
    # GET BY ID
    # ========================================================

    def get_by_id(
        self,
        memory_id: str,
    ) -> Optional[Dict[str, Any]]:

        with self.lock:

            item = self.index.get(
                memory_id
            )

            if item is None:
                return None

            self.total_reads += 1

            return self._safe_copy(
                item
            )

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(
        self,
        memory_type: Optional[str] = None,
    ) -> bool:

        with self.lock:

            collections = {

                "observation":
                    self.observations,

                "experience":
                    self.experiences,

                "knowledge":
                    self.knowledge,

                "insight":
                    self.insights,

                "feedback":
                    self.feedback,

                "decision":
                    self.decisions,

            }

            if memory_type:

                collection = collections.get(
                    memory_type.lower()
                )

                if collection is None:
                    return False

                collection.clear()

            else:

                for collection in (
                    self.observations,
                    self.experiences,
                    self.knowledge,
                    self.insights,
                    self.feedback,
                    self.decisions,
                ):

                    collection.clear()

                self.index.clear()

            return True

    # ========================================================
    # SNAPSHOT
    # ========================================================

    def snapshot(
        self,
        limit: int = 100,
    ) -> Dict[str, Any]:

        return {

            "module":
                MEMORY_NAME,

            "version":
                MEMORY_VERSION,

            "stats":
                self.stats(),

            "recent":
                self.recent(limit),

        }

    # ========================================================
    # STATUS
    # ========================================================

    def status(self) -> Dict[str, Any]:

        data = self.stats()

        return {

            "module":
                "learning_memory",

            "name":
                MEMORY_NAME,

            "version":
                MEMORY_VERSION,

            "online":
                True,

            "total":
                data["total"],

            "stats":
                data,

            "deduplicate":
                self.deduplicate,

            "max_size":
                self.max_size,

        }


# ============================================================
# GLOBAL INSTANCE
# ============================================================

learning_memory = LearningMemory()


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [

    "MEMORY_NAME",
    "MEMORY_VERSION",
    "LearningMemory",
    "learning_memory",

]

