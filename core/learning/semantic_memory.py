
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SEMANTIC MEMORY ENGINE
#
# Version 3.0
#
# ============================================================
#
# RESPONSIBILITIES
#
# - Store semantic meaning
# - Categorize semantic memories
# - Importance scoring
# - Confidence scoring
# - Concept extraction
# - Keyword search
# - Category search
# - Semantic filtering
# - Memory recall
# - Related memory discovery
# - Memory reinforcement
# - Memory statistics
# - Memory cleanup
# - Memory history
# - Latest memory
# - Memory update
# - Memory deletion
# - System status
#
# ============================================================

import logging
import re
from copy import deepcopy
from datetime import datetime


logger = logging.getLogger(__name__)


class SemanticMemory:

    # ========================================================
    # CONFIGURATION
    # ========================================================

    MAX_MEMORY = 2000
    DEFAULT_IMPORTANCE = 0.5
    DEFAULT_CONFIDENCE = 0.5
    DEFAULT_STRENGTH = 1.0

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self, max_memory=MAX_MEMORY):

        try:
            max_memory = int(max_memory)
        except (TypeError, ValueError):
            max_memory = self.MAX_MEMORY

        self.memory = []

        self.max_memory = max(
            1,
            max_memory
        )

        self.total_stored = 0
        self.total_searches = 0
        self.total_recalls = 0
        self.total_reinforced = 0

        self.last_memory = None

        logger.info(
            "Semantic Memory initialized."
        )

    # ========================================================
    # NORMALIZE TEXT
    # ========================================================

    def normalize_text(self, value):

        if value is None:
            return ""

        text = str(value).strip().lower()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    # ========================================================
    # EXTRACT KEYWORDS
    # ========================================================

    def extract_keywords(self, meaning):

        text = self.normalize_text(
            meaning
        )

        if not text:
            return []

        words = re.findall(
            r"[a-zA-Z0-9_\-/]+",
            text
        )

        stopwords = {
            "yang",
            "dan",
            "atau",
            "dengan",
            "untuk",
            "dari",
            "pada",
            "adalah",
            "ini",
            "itu",
            "the",
            "and",
            "or",
            "with",
            "for",
            "from",
            "is",
            "are",
            "of",
            "to",
        }

        keywords = []

        for word in words:

            if len(word) < 3:
                continue

            if word in stopwords:
                continue

            if word not in keywords:
                keywords.append(word)

        return keywords[:30]

    # ========================================================
    # EXTRACT CONCEPTS
    # ========================================================

    def extract_concepts(self, meaning):

        text = self.normalize_text(
            meaning
        )

        if not text:
            return []

        concepts = []

        concept_map = {
            "bullish": "positive_market",
            "bearish": "negative_market",
            "breakout": "breakout",
            "reversal": "reversal",
            "momentum": "momentum",
            "volume": "volume",
            "trend": "trend",
            "risk": "risk",
            "confidence": "confidence",
            "prediction": "prediction",
            "learning": "learning",
            "pattern": "pattern",
            "market": "market",
            "ai": "artificial_intelligence",
            "bitcoin": "bitcoin",
            "btc": "bitcoin",
            "ethereum": "ethereum",
            "eth": "ethereum",
            "price": "price",
            "support": "support",
            "resistance": "resistance",
            "liquidity": "liquidity",
            "volatility": "volatility",
        }

        for keyword, concept in concept_map.items():

            if keyword in text:

                if concept not in concepts:
                    concepts.append(concept)

        return concepts

    # ========================================================
    # NORMALIZE SCORE
    # ========================================================

    def normalize_score(
        self,
        value,
        default=0.5
    ):

        try:
            value = float(value)

        except (
            TypeError,
            ValueError
        ):
            value = default

        if value > 1:
            value = value / 100.0

        return max(
            0.0,
            min(
                1.0,
                value
            )
        )

    # ========================================================
    # STORE MEMORY
    # ========================================================

    def store(
        self,
        meaning,
        category="general",
        importance=DEFAULT_IMPORTANCE,
        confidence=DEFAULT_CONFIDENCE,
        source=None,
        metadata=None,
        concepts=None,
        keywords=None
    ):

        timestamp = datetime.now().isoformat()

        if concepts is None:
            concepts = self.extract_concepts(
                meaning
            )

        if keywords is None:
            keywords = self.extract_keywords(
                meaning
            )

        if not isinstance(
            concepts,
            (list, tuple, set)
        ):
            concepts = []

        if not isinstance(
            keywords,
            (list, tuple, set)
        ):
            keywords = []

        item = {
            "id": self.total_stored + 1,

            "time": timestamp,

            "timestamp": timestamp,

            "category": str(
                category
            ),

            "meaning": meaning,

            "importance": self.normalize_score(
                importance,
                default=self.DEFAULT_IMPORTANCE
            ),

            "confidence": self.normalize_score(
                confidence,
                default=self.DEFAULT_CONFIDENCE
            ),

            "strength": self.DEFAULT_STRENGTH,

            "recall_count": 0,

            "reinforcement_count": 0,

            "source": source,

            "concepts": list(
                concepts
            ),

            "keywords": list(
                keywords
            ),

            "metadata": (
                deepcopy(metadata)
                if isinstance(
                    metadata,
                    dict
                )
                else {}
            ),
        }

        self.memory.append(
            item
        )

        self.total_stored += 1

        self.last_memory = item

        self._trim_memory()

        return item

    # ========================================================
    # STORE STRUCTURED MEMORY
    # ========================================================

    def store_memory(self, memory):

        if not isinstance(
            memory,
            dict
        ):

            return self.store(
                memory
            )

        meaning = memory.get(
            "meaning",
            memory
        )

        return self.store(
            meaning=meaning,

            category=memory.get(
                "category",
                "general"
            ),

            importance=memory.get(
                "importance",
                self.DEFAULT_IMPORTANCE
            ),

            confidence=memory.get(
                "confidence",
                self.DEFAULT_CONFIDENCE
            ),

            source=memory.get(
                "source"
            ),

            metadata=memory.get(
                "metadata"
            ),

            concepts=memory.get(
                "concepts"
            ),

            keywords=memory.get(
                "keywords"
            ),
        )

    # ========================================================
    # SEARCH MEMORY
    # ========================================================

    def search(
        self,
        keyword,
        limit=None
    ):

        self.total_searches += 1

        keyword = self.normalize_text(
            keyword
        )

        if not keyword:
            return []

        result = []

        for item in reversed(
            self.memory
        ):

            searchable = " ".join(
                [
                    str(
                        item.get(
                            "meaning",
                            ""
                        )
                    ),

                    str(
                        item.get(
                            "category",
                            ""
                        )
                    ),

                    " ".join(
                        str(value)
                        for value in item.get(
                            "keywords",
                            []
                        )
                    ),

                    " ".join(
                        str(value)
                        for value in item.get(
                            "concepts",
                            []
                        )
                    ),
                ]
            ).lower()

            if keyword in searchable:

                item["recall_count"] = (
                    item.get(
                        "recall_count",
                        0
                    )
                    + 1
                )

                self.total_recalls += 1

                result.append(
                    item
                )

                if (
                    limit is not None
                    and
                    len(result) >= int(limit)
                ):
                    break

        return result

    # ========================================================
    # SEARCH BY CATEGORY
    # ========================================================

    def search_category(
        self,
        category,
        limit=None
    ):

        category = self.normalize_text(
            category
        )

        if not category:
            return []

        result = [

            item

            for item in reversed(
                self.memory
            )

            if self.normalize_text(
                item.get(
                    "category",
                    ""
                )
            ) == category
        ]

        if limit is not None:

            try:
                limit = int(limit)
            except (
                TypeError,
                ValueError
            ):
                limit = 20

            result = result[
                :max(
                    0,
                    limit
                )
            ]

        return result

    # ========================================================
    # SEARCH BY CONCEPT
    # ========================================================

    def search_concept(
        self,
        concept,
        limit=None
    ):

        concept = self.normalize_text(
            concept
        )

        if not concept:
            return []

        result = []

        for item in reversed(
            self.memory
        ):

            concepts = [

                self.normalize_text(
                    value
                )

                for value in item.get(
                    "concepts",
                    []
                )
            ]

            if concept in concepts:

                result.append(
                    item
                )

                if (
                    limit is not None
                    and
                    len(result) >= int(limit)
                ):
                    break

        return result

    # ========================================================
    # SEMANTIC FILTER
    # ========================================================

    def filter(
        self,
        category=None,
        concept=None,
        min_importance=None,
        min_confidence=None
    ):

        results = []

        normalized_category = (
            self.normalize_text(category)
            if category is not None
            else None
        )

        normalized_concept = (
            self.normalize_text(concept)
            if concept is not None
            else None
        )

        if min_importance is not None:
            min_importance = self.normalize_score(
                min_importance
            )

        if min_confidence is not None:
            min_confidence = self.normalize_score(
                min_confidence
            )

        for item in reversed(
            self.memory
        ):

            if (
                normalized_category is not None
                and
                self.normalize_text(
                    item.get(
                        "category",
                        ""
                    )
                )
                != normalized_category
            ):
                continue

            if (
                normalized_concept is not None
                and
                normalized_concept not in [
                    self.normalize_text(value)
                    for value in item.get(
                        "concepts",
                        []
                    )
                ]
            ):
                continue

            if (
                min_importance is not None
                and
                item.get(
                    "importance",
                    0
                ) < min_importance
            ):
                continue

            if (
                min_confidence is not None
                and
                item.get(
                    "confidence",
                    0
                ) < min_confidence
            ):
                continue

            results.append(
                item
            )

        return results

    # ========================================================
    # GET RECENT
    # ========================================================

    def get_recent(
        self,
        limit=20
    ):

        try:
            limit = int(limit)

        except (
            TypeError,
            ValueError
        ):
            limit = 20

        if limit <= 0:
            return []

        return self.memory[
            -limit:
        ]

    # ========================================================
    # RECALL
    # ========================================================

    def recall(
        self,
        limit=20
    ):

        results = self.get_recent(
            limit
        )

        for item in results:

            item["recall_count"] = (
                item.get(
                    "recall_count",
                    0
                )
                + 1
            )

            self.total_recalls += 1

        return results

    # ========================================================
    # GET LATEST
    # ========================================================

    def latest(self):

        return self.last_memory

    # ========================================================
    # GET IMPORTANT MEMORIES
    # ========================================================

    def important(
        self,
        limit=20,
        threshold=0.7
    ):

        try:
            limit = int(limit)
        except (
            TypeError,
            ValueError
        ):
            limit = 20

        threshold = self.normalize_score(
            threshold
        )

        result = [

            item

            for item in self.memory

            if item.get(
                "importance",
                0
            ) >= threshold
        ]

        result.sort(

            key=lambda item: (

                item.get(
                    "importance",
                    0
                )

                *

                item.get(
                    "confidence",
                    0
                )

                *

                item.get(
                    "strength",
                    1
                )
            ),

            reverse=True
        )

        return result[
            :max(
                0,
                limit
            )
        ]

    # ========================================================
    # RELATED MEMORIES
    # ========================================================

    def related(
        self,
        memory,
        limit=10
    ):

        if not isinstance(
            memory,
            dict
        ):
            return []

        try:
            limit = int(limit)
        except (
            TypeError,
            ValueError
        ):
            limit = 10

        target_concepts = {
            self.normalize_text(value)
            for value in memory.get(
                "concepts",
                []
            )
        }

        target_keywords = {
            self.normalize_text(value)
            for value in memory.get(
                "keywords",
                []
            )
        }

        target_category = self.normalize_text(
            memory.get(
                "category",
                ""
            )
        )

        scored = []

        for item in self.memory:

            if item is memory:
                continue

            concepts = {
                self.normalize_text(value)
                for value in item.get(
                    "concepts",
                    []
                )
            }

            keywords = {
                self.normalize_text(value)
                for value in item.get(
                    "keywords",
                    []
                )
            }

            category = self.normalize_text(
                item.get(
                    "category",
                    ""
                )
            )

            concept_score = len(
                target_concepts
                &
                concepts
            )

            keyword_score = len(
                target_keywords
                &
                keywords
            )

            category_score = (
                2
                if (
                    target_category
                    and
                    target_category == category
                )
                else 0
            )

            score = (
                concept_score * 3
                +
                keyword_score
                +
                category_score
            )

            if score > 0:

                scored.append(
                    (
                        score,
                        item
                    )
                )

        scored.sort(
            key=lambda pair: pair[0],
            reverse=True
        )

        return [
            item
            for _, item in scored[
                :max(
                    0,
                    limit
                )
            ]
        ]

    # ========================================================
    # REINFORCE MEMORY
    # ========================================================

    def reinforce(
        self,
        memory_id,
        amount=0.1
    ):

        try:
            memory_id = int(
                memory_id
            )

        except (
            TypeError,
            ValueError
        ):
            return None

        amount = self.normalize_score(
            amount,
            default=0.1
        )

        for item in self.memory:

            if item.get(
                "id"
            ) != memory_id:
                continue

            item["strength"] = min(
                1.0,

                item.get(
                    "strength",
                    self.DEFAULT_STRENGTH
                )
                +
                amount
            )

            item["reinforcement_count"] = (
                item.get(
                    "reinforcement_count",
                    0
                )
                +
                1
            )

            self.total_reinforced += 1

            item["updated"] = (
                datetime.now()
                .isoformat()
            )

            return item

        return None

    # ========================================================
    # UPDATE MEMORY
    # ========================================================

    def update(
        self,
        memory_id,
        **changes
    ):

        try:
            memory_id = int(
                memory_id
            )

        except (
            TypeError,
            ValueError
        ):
            return None

        allowed = {
            "category",
            "meaning",
            "importance",
            "confidence",
            "source",
            "metadata",
            "concepts",
            "keywords",
        }

        for item in self.memory:

            if item.get(
                "id"
            ) != memory_id:
                continue

            for key, value in changes.items():

                if key not in allowed:
                    continue

                if key in {
                    "importance",
                    "confidence"
                }:

                    value = self.normalize_score(
                        value
                    )

                elif key == "metadata":

                    value = (
                        deepcopy(value)
                        if isinstance(
                            value,
                            dict
                        )
                        else {}
                    )

                elif key in {
                    "concepts",
                    "keywords"
                }:

                    value = (
                        list(value)
                        if isinstance(
                            value,
                            (list, tuple, set)
                        )
                        else []
                    )

                item[key] = value

            # Rebuild semantic indexes when meaning changes.
            if "meaning" in changes:

                item["keywords"] = (
                    self.extract_keywords(
                        item.get(
                            "meaning",
                            ""
                        )
                    )
                )

                item["concepts"] = (
                    self.extract_concepts(
                        item.get(
                            "meaning",
                            ""
                        )
                    )

                )

            item["updated"] = (
                datetime.now()
                .isoformat()
            )

            self.last_memory = item

            return item

        return None

    # ========================================================
    # DELETE MEMORY
    # ========================================================

    def delete(
        self,
        memory_id
    ):

        try:
            memory_id = int(
                memory_id
            )

        except (
            TypeError,
            ValueError
        ):
            return False

        for index, item in enumerate(
            self.memory
        ):

            if item.get(
                "id"
            ) == memory_id:

                removed = self.memory.pop(
                    index
                )

                if (
                    self.last_memory
                    is removed
                ):

                    self.last_memory = (
                        self.memory[-1]
                        if self.memory
                        else None
                    )

                return True

        return False

    # ========================================================
    # CLEAR MEMORY
    # ========================================================

    def clear(self):

        self.memory.clear()

        self.last_memory = None

        return True

    # ========================================================
    # COUNT
    # ========================================================

    def count(self):

        return len(
            self.memory
        )

    # ========================================================
    # CATEGORIES
    # ========================================================

    def categories(self):

        result = {}

        for item in self.memory:

            category = item.get(
                "category",
                "general"
            )

            result[category] = (
                result.get(
                    category,
                    0
                )
                +
                1
            )

        return result

    # ========================================================
    # CONCEPTS
    # ========================================================

    def concepts(self):

        result = {}

        for item in self.memory:

            for concept in item.get(
                "concepts",
                []
            ):

                result[concept] = (
                    result.get(
                        concept,
                        0
                    )
                    +
                    1
                )

        return result

    # ========================================================
    # STATISTICS
    # ========================================================

    def statistics(self):

        if not self.memory:

            return {
                "total": 0,

                "categories": 0,

                "concepts": 0,

                "average_importance": 0,

                "average_confidence": 0,

                "average_strength": 0,

                "searches":
                    self.total_searches,

                "recalls":
                    self.total_recalls,

                "reinforced":
                    self.total_reinforced,
            }

        importance = [

            self.normalize_score(
                item.get(
                    "importance",
                    0
                )
            )

            for item in self.memory
        ]

        confidence = [

            self.normalize_score(
                item.get(
                    "confidence",
                    0
                )
            )

            for item in self.memory
        ]

        strength = [

            self.normalize_score(
                item.get(
                    "strength",
                    0
                )
            )

            for item in self.memory
        ]

        return {

            "total":
                len(
                    self.memory
                ),

            "categories":
                len(
                    self.categories()
                ),

            "concepts":
                len(
                    self.concepts()
                ),

            "average_importance":
                round(
                    sum(importance)
                    /
                    len(importance),
                    3
                ),

            "average_confidence":
                round(
                    sum(confidence)
                    /
                    len(confidence),
                    3
                ),

            "average_strength":
                round(
                    sum(strength)
                    /
                    len(strength),
                    3
                ),

            "searches":
                self.total_searches,

            "recalls":
                self.total_recalls,

            "reinforced":
                self.total_reinforced,
        }

    # ========================================================
    # MEMORY LIMIT
    # ========================================================

    def _trim_memory(self):

        if len(
            self.memory
        ) <= self.max_memory:

            return

        del self.memory[
            :-self.max_memory
        ]

    # ========================================================
    # CLEANUP
    # ========================================================

    def cleanup(self):

        self._trim_memory()

        return {
            "status": "ok",
            "items": len(
                self.memory
            ),
            "max_memory": self.max_memory,
        }

    # ========================================================
    # HISTORY
    # ========================================================

    def history(
        self,
        limit=20
    ):

        return self.get_recent(
            limit
        )

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        stats = self.statistics()

        return {

            "module":
                "semantic_memory",

            "items":
                len(
                    self.memory
                ),

            "max_memory":
                self.max_memory,

            "total_stored":
                self.total_stored,

            "categories":
                stats.get(
                    "categories",
                    0
                ),

            "concepts":
                stats.get(
                    "concepts",
                    0
                ),

            "searches":
                self.total_searches,

            "recalls":
                self.total_recalls,

            "reinforced":
                self.total_reinforced,

            "has_latest":
                self.last_memory is not None,

        }


# ============================================================
# GLOBAL INSTANCE
# ============================================================

semantic_memory = SemanticMemory()


# ============================================================
# BACKWARD-COMPATIBILITY ALIAS
# ============================================================

SemanticMemoryEngine = SemanticMemory

