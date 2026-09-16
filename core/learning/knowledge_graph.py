# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# KNOWLEDGE GRAPH ENGINE
#
# FOUNDATION VERSION 3.0
#
# ============================================================
#
# PURPOSE
# ------------------------------------------------------------
#
# Central knowledge representation engine for INKSIDE
# Intelligence OS.
#
# Features:
#
# - Knowledge Nodes
# - Concept Relationships
# - Typed Relationships
# - Weighted Connections
# - Confidence Tracking
# - Evidence Tracking
# - Observation Tracking
# - Learning Events
# - Experience Learning
# - Confidence Decay
# - Relationship Reinforcement
# - Bidirectional Relationships
# - Directed Relationships
# - Related Concept Discovery
# - Keyword Search
# - Ranked Search
# - Graph Traversal
# - Multi-depth Neighbors
# - Shortest Path Discovery
# - Weighted Path Discovery
# - Node Removal
# - Connection Removal
# - Graph Merge
# - Graph Snapshot
# - Export
# - Import
# - Statistics
# - Health Monitoring
# - Thread Safety
# - Reset Support
# - Backward Compatibility
#
# ============================================================

from __future__ import annotations

import copy
import logging
import math
import threading

from collections import deque
from datetime import datetime, timezone
from heapq import heappop, heappush
from typing import Any, Dict, List, Optional, Tuple


logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

KNOWLEDGE_GRAPH_VERSION = "3.0"
API_VERSION = "1.0"


# ============================================================
#
# DEFAULT VALUES
#
# ============================================================

DEFAULT_WEIGHT = 1.0
DEFAULT_CONFIDENCE = 1.0

MIN_WEIGHT = 0.0
MAX_CONFIDENCE = 1.0

DEFAULT_RELATION = "related_to"

DEFAULT_SEARCH_LIMIT = 50

DEFAULT_MAX_DEPTH = 5


# ============================================================
#
# RELATION TYPES
#
# ============================================================

RELATION_RELATED = "related_to"
RELATION_CAUSES = "causes"
RELATION_SUPPORTS = "supports"
RELATION_CONTRADICTS = "contradicts"
RELATION_PRECEDES = "precedes"
RELATION_FOLLOWS = "follows"
RELATION_CONTAINS = "contains"
RELATION_PART_OF = "part_of"
RELATION_SIMILAR = "similar_to"
RELATION_DEPENDS = "depends_on"
RELATION_INFLUENCES = "influences"
RELATION_ASSOCIATED = "associated_with"


# ============================================================
#
# INTERNAL TIME HELPERS
#
# ============================================================

def _utc_now() -> str:
    """
    Return timezone-aware UTC timestamp.
    """

    return (
        datetime.now(
            timezone.utc
        )
        .isoformat()
        .replace(
            "+00:00",
            "Z"
        )
    )


# ============================================================
#
# KNOWLEDGE GRAPH
#
# ============================================================

class KnowledgeGraph:
    """
    Universal knowledge graph engine for INKSIDE
    Intelligence OS.

    The graph stores:

        node
            metadata
            connections

    Example:

        {
            "breakout": {
                "metadata": {
                    "observations": 10
                },

                "connections": {
                    "volume": {
                        "relation": "supports",
                        "weight": 4.5,
                        "confidence": 0.91,
                        "count": 8
                    }
                }
            }
        }

    The class is thread-safe and can be shared between
    scanner, learning, intelligence and analysis modules.
    """

    # ========================================================
    #
    # INIT
    #
    # ========================================================

    def __init__(
        self,
        *,
        confidence_decay: float = 0.995,
        max_nodes: Optional[int] = None,
        max_connections_per_node: Optional[int] = None,
    ):

        self.lock = threading.RLock()

        # ----------------------------------------------------
        # GRAPH
        # ----------------------------------------------------

        self.graph: Dict[
            str,
            Dict[str, Any]
        ] = {}

        # ----------------------------------------------------
        # CONFIG
        # ----------------------------------------------------

        self.confidence_decay = float(
            confidence_decay
        )

        self.max_nodes = max_nodes

        self.max_connections_per_node = (
            max_connections_per_node
        )

        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        self.nodes_created = 0
        self.nodes_removed = 0

        self.connections_created = 0
        self.connections_removed = 0

        self.learning_events = 0
        self.experience_events = 0

        self.searches = 0
        self.traversals = 0

        self.path_searches = 0

        self.updates = 0

        self.errors = 0

        self.started_at = _utc_now()

        self.last_learning = None
        self.last_search = None
        self.last_error = None

        logger.info(
            "Knowledge Graph v%s initialized.",
            KNOWLEDGE_GRAPH_VERSION
        )

    # ========================================================
    #
    # INTERNAL HELPERS
    #
    # ========================================================

    def _normalize_concept(
        self,
        concept: Any
    ) -> Optional[str]:

        if concept is None:
            return None

        concept = str(
            concept
        ).strip()

        if not concept:
            return None

        return concept

    # --------------------------------------------------------

    def _normalize_relation(
        self,
        relation: Any
    ) -> str:

        if relation is None:
            return DEFAULT_RELATION

        relation = str(
            relation
        ).strip().lower()

        if not relation:
            return DEFAULT_RELATION

        return relation

    # --------------------------------------------------------

    def _safe_float(
        self,
        value: Any,
        default: float
    ) -> float:

        try:

            result = float(value)

            if not math.isfinite(
                result
            ):
                return default

            return result

        except (
            TypeError,
            ValueError
        ):

            return default

    # --------------------------------------------------------

    def _clamp_confidence(
        self,
        value: Any
    ) -> float:

        value = self._safe_float(
            value,
            DEFAULT_CONFIDENCE
        )

        return max(
            0.0,
            min(
                MAX_CONFIDENCE,
                value
            )
        )

    # --------------------------------------------------------

    def _ensure_node(
        self,
        concept: Any
    ) -> Optional[str]:

        concept = self._normalize_concept(
            concept
        )

        if concept is None:
            return None

        if concept not in self.graph:

            if (
                self.max_nodes is not None
                and
                len(self.graph)
                >= self.max_nodes
            ):

                logger.warning(
                    "Knowledge graph max_nodes reached: %s",
                    self.max_nodes
                )

                return None

            now = _utc_now()

            self.graph[concept] = {

                "metadata": {

                    "created":
                        now,

                    "updated":
                        now,

                    "observations":
                        0,

                    "learning_events":
                        0,

                    "confidence":
                        DEFAULT_CONFIDENCE,

                    "tags":
                        [],

                    "source":
                        None,

                },

                "connections": {}

            }

            self.nodes_created += 1

        return concept

    # ========================================================
    #
    # NODE
    #
    # ========================================================

    def add_node(
        self,
        concept: Any,
        metadata: Optional[
            Dict[str, Any]
        ] = None
    ) -> bool:

        with self.lock:

            concept = self._ensure_node(
                concept
            )

            if concept is None:
                return False

            node = self.graph[
                concept
            ]

            if isinstance(
                metadata,
                dict
            ):

                metadata_copy = copy.deepcopy(
                    metadata
                )

                node[
                    "metadata"
                ].update(
                    metadata_copy
                )

            node[
                "metadata"
            ][
                "updated"
            ] = _utc_now()

            self.updates += 1

            return True

    # ========================================================
    #
    # UPDATE NODE
    #
    # ========================================================

    def update_node(
        self,
        concept: Any,
        **metadata: Any
    ) -> bool:

        return self.add_node(
            concept,
            metadata
        )

    # ========================================================
    #
    # GET NODE
    #
    # ========================================================

    def get(
        self,
        concept: Any
    ) -> Optional[
        Dict[str, Any]
    ]:

        concept = self._normalize_concept(
            concept
        )

        if concept is None:
            return None

        with self.lock:

            data = self.graph.get(
                concept
            )

            if data is None:
                return None

            return copy.deepcopy(
                data
            )

    # ========================================================
    #
    # HAS NODE
    #
    # ========================================================

    def has_node(
        self,
        concept: Any
    ) -> bool:

        concept = self._normalize_concept(
            concept
        )

        if concept is None:
            return False

        with self.lock:

            return concept in self.graph

    # ========================================================
    #
    # CONNECT
    #
    # ========================================================

    def connect(
        self,
        concept_a: Any,
        concept_b: Any,
        weight: float = DEFAULT_WEIGHT,
        confidence: float = DEFAULT_CONFIDENCE,
        bidirectional: bool = True,
        relation: str = DEFAULT_RELATION,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> bool:

        with self.lock:

            concept_a = self._ensure_node(
                concept_a
            )

            concept_b = self._ensure_node(
                concept_b
            )

            if (
                concept_a is None
                or
                concept_b is None
            ):

                return False

            if concept_a == concept_b:
                return False

            relation = self._normalize_relation(
                relation
            )

            weight = max(
                MIN_WEIGHT,
                self._safe_float(
                    weight,
                    DEFAULT_WEIGHT
                )
            )

            confidence = self._clamp_confidence(
                confidence
            )

            now = _utc_now()

            success = self._connect_one_way(
                concept_a,
                concept_b,
                weight,
                confidence,
                relation,
                now,
                metadata
            )

            if not success:
                return False

            if bidirectional:

                self._connect_one_way(
                    concept_b,
                    concept_a,
                    weight,
                    confidence,
                    relation,
                    now,
                    metadata
                )

            return True

    # ========================================================
    #
    # INTERNAL ONE-WAY CONNECTION
    #
    # ========================================================

    def _connect_one_way(
        self,
        source: str,
        target: str,
        weight: float,
        confidence: float,
        relation: str,
        timestamp: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> bool:

        connections = self.graph[
            source
        ][
            "connections"
        ]

        existing = connections.get(
            target
        )

        if existing:

            old_weight = self._safe_float(
                existing.get(
                    "weight"
                ),
                DEFAULT_WEIGHT
            )

            old_confidence = self._clamp_confidence(
                existing.get(
                    "confidence"
                )
            )

            old_count = int(
                existing.get(
                    "count",
                    1
                )
            )

            existing[
                "weight"
            ] = (
                old_weight
                +
                weight
            )

            existing[
                "confidence"
            ] = (
                (
                    old_confidence
                    * old_count
                )
                +
                confidence
            ) / (
                old_count + 1
            )

            existing[
                "count"
            ] = old_count + 1

            existing[
                "last_seen"
            ] = timestamp

            existing[
                "relation"
            ] = relation

            if isinstance(
                metadata,
                dict
            ):

                existing.setdefault(
                    "metadata",
                    {}
                ).update(
                    copy.deepcopy(
                        metadata
                    )
                )

            self.updates += 1

            return True

        # ----------------------------------------------------
        # Connection limit
        # ----------------------------------------------------

        if (
            self.max_connections_per_node
            is not None
            and
            len(connections)
            >= self.max_connections_per_node
        ):

            self._prune_weakest_connection(
                source
            )

        connections[
            target
        ] = {

            "relation":
                relation,

            "weight":
                weight,

            "confidence":
                confidence,

            "count":
                1,

            "created":
                timestamp,

            "last_seen":
                timestamp,

            "metadata":
                copy.deepcopy(
                    metadata or {}
                ),

        }

        self.connections_created += 1

        return True

    # ========================================================
    #
    # PRUNE WEAKEST CONNECTION
    #
    # ========================================================

    def _prune_weakest_connection(
        self,
        concept: str
    ) -> None:

        connections = self.graph[
            concept
        ][
            "connections"
        ]

        if not connections:
            return

        weakest = min(
            connections.items(),
            key=lambda item: (
                self._safe_float(
                    item[1].get(
                        "weight"
                    ),
                    0.0
                )
                *
                self._clamp_confidence(
                    item[1].get(
                        "confidence"
                    )
                )
            )
        )

        del connections[
            weakest[0]
        ]

        self.connections_removed += 1

    # ========================================================
    #
    # DISCONNECT
    #
    # ========================================================

    def disconnect(
        self,
        concept_a: Any,
        concept_b: Any,
        bidirectional: bool = True
    ) -> bool:

        concept_a = self._normalize_concept(
            concept_a
        )

        concept_b = self._normalize_concept(
            concept_b
        )

        if (
            concept_a is None
            or
            concept_b is None
        ):
            return False

        with self.lock:

            if concept_a not in self.graph:
                return False

            removed = (
                concept_b
                in self.graph[
                    concept_a
                ][
                    "connections"
                ]
            )

            if removed:

                del self.graph[
                    concept_a
                ][
                    "connections"
                ][
                    concept_b
                ]

                self.connections_removed += 1

            if (
                bidirectional
                and
                concept_b in self.graph
            ):

                reverse_removed = (
                    concept_a
                    in self.graph[
                        concept_b
                    ][
                        "connections"
                    ]
                )

                if reverse_removed:

                    del self.graph[
                        concept_b
                    ][
                        "connections"
                    ][
                        concept_a
                    ]

                    self.connections_removed += 1

            return removed

    # ========================================================
    #
    # REMOVE NODE
    #
    # ========================================================

    def remove(
        self,
        concept: Any
    ) -> bool:

        concept = self._normalize_concept(
            concept
        )

        if concept is None:
            return False

        with self.lock:

            if concept not in self.graph:
                return False

            # Remove incoming edges
            for node in self.graph.values():

                if concept in node[
                    "connections"
                ]:

                    del node[
                        "connections"
                    ][
                        concept
                    ]

                    self.connections_removed += 1

            del self.graph[
                concept
            ]

            self.nodes_removed += 1

            return True

    # ========================================================
    #
    # LEARN
    #
    # ========================================================

    def learn(
        self,
        knowledge: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(
            knowledge,
            dict
        ):

            return self.all()

        with self.lock:

            concepts = knowledge.get(
                "concept",
                knowledge.get(
                    "concepts",
                    []
                )
            )

            if isinstance(
                concepts,
                str
            ):

                concepts = [
                    concepts
                ]

            if not isinstance(
                concepts,
                list
            ):

                return self.all()

            normalized = []

            for concept in concepts:

                normalized_concept = (
                    self._normalize_concept(
                        concept
                    )
                )

                if normalized_concept:

                    normalized.append(
                        normalized_concept
                    )

            normalized = list(
                dict.fromkeys(
                    normalized
                )
            )

            if not normalized:

                return self.all()

            self.learning_events += 1

            self.last_learning = _utc_now()

            # ------------------------------------------------
            # Metadata
            # ------------------------------------------------

            source = knowledge.get(
                "source"
            )

            confidence = self._clamp_confidence(
                knowledge.get(
                    "confidence",
                    DEFAULT_CONFIDENCE
                )
            )

            tags = knowledge.get(
                "tags",
                []
            )

            if isinstance(
                tags,
                str
            ):

                tags = [tags]

            # ------------------------------------------------
            # Create nodes
            # ------------------------------------------------

            for concept in normalized:

                node = self._ensure_node(
                    concept
                )

                if node is None:
                    continue

                metadata = self.graph[
                    node
                ][
                    "metadata"
                ]

                metadata[
                    "observations"
                ] = int(
                    metadata.get(
                        "observations",
                        0
                    )
                ) + 1

                metadata[
                    "learning_events"
                ] = int(
                    metadata.get(
                        "learning_events",
                        0
                    )
                ) + 1

                metadata[
                    "confidence"
                ] = (
                    metadata.get(
                        "confidence",
                        DEFAULT_CONFIDENCE
                    )
                    +
                    confidence
                ) / 2

                if source is not None:

                    metadata[
                        "source"
                    ] = source

                if tags:

                    existing_tags = set(
                        metadata.get(
                            "tags",
                            []
                        )
                    )

                    existing_tags.update(
                        str(tag)
                        for tag in tags
                    )

                    metadata[
                        "tags"
                    ] = sorted(
                        existing_tags
                    )

                metadata[
                    "updated"
                ] = _utc_now()

            # ------------------------------------------------
            # Relationship metadata
            # ------------------------------------------------

            relation = self._normalize_relation(
                knowledge.get(
                    "relation",
                    DEFAULT_RELATION
                )
            )

            weight = self._safe_float(
                knowledge.get(
                    "weight",
                    DEFAULT_WEIGHT
                ),
                DEFAULT_WEIGHT
            )

            bidirectional = bool(
                knowledge.get(
                    "bidirectional",
                    True
                )
            )

            # ------------------------------------------------
            # Create relationships
            # ------------------------------------------------

            for i in range(
                len(normalized)
            ):

                for j in range(
                    i + 1,
                    len(normalized)
                ):

                    self.connect(
                        normalized[i],
                        normalized[j],
                        weight=weight,
                        confidence=confidence,
                        bidirectional=bidirectional,
                        relation=relation,
                        metadata={
                            "source":
                                source
                        }
                    )

            return self.all()

    # ========================================================
    #
    # LEARN EXPERIENCE
    #
    # ========================================================

    def learn_experience(
        self,
        experience: Dict[str, Any]
    ) -> bool:

        if not isinstance(
            experience,
            dict
        ):

            return False

        with self.lock:

            concepts = experience.get(
                "concepts",
                experience.get(
                    "concept",
                    []
                )
            )

            if isinstance(
                concepts,
                str
            ):

                concepts = [
                    concepts
                ]

            if not isinstance(
                concepts,
                list
            ):

                return False

            knowledge = {

                "concept":
                    concepts,

                "confidence":
                    experience.get(
                        "confidence",
                        DEFAULT_CONFIDENCE
                    ),

                "source":
                    experience.get(
                        "source",
                        "experience"
                    ),

                "tags":
                    experience.get(
                        "tags",
                        []
                    ),

                "relation":
                    experience.get(
                        "relation",
                        DEFAULT_RELATION
                    ),

                "weight":
                    experience.get(
                        "weight",
                        DEFAULT_WEIGHT
                    ),

                "bidirectional":
                    experience.get(
                        "bidirectional",
                        True
                    ),

            }

            result = self.learn(
                knowledge
            )

            if result is None:
                return False

            self.experience_events += 1

            return True

    # ========================================================
    #
    # REINFORCE CONNECTION
    #
    # ========================================================

    def reinforce(
        self,
        concept_a: Any,
        concept_b: Any,
        amount: float = 1.0,
        confidence: Optional[
            float
        ] = None,
        relation: Optional[
            str
        ] = None,
        bidirectional: bool = True
    ) -> bool:

        return self.connect(
            concept_a,
            concept_b,
            weight=amount,
            confidence=(
                DEFAULT_CONFIDENCE
                if confidence is None
                else confidence
            ),
            relation=(
                DEFAULT_RELATION
                if relation is None
                else relation
            ),
            bidirectional=bidirectional
        )

    # ========================================================
    #
    # DECAY CONFIDENCE
    #
    # ========================================================

    def decay_confidence(
        self,
        factor: Optional[
            float
        ] = None
    ) -> int:
        """
        Apply confidence decay to all relationships.

        Example:

            factor=0.99

        means every confidence value is reduced by 1%.
        """

        factor = (
            self.confidence_decay
            if factor is None
            else self._safe_float(
                factor,
                self.confidence_decay
            )
        )

        factor = max(
            0.0,
            min(
                1.0,
                factor
            )
        )

        changed = 0

        with self.lock:

            for node in self.graph.values():

                for connection in node[
                    "connections"
                ].values():

                    old = self._clamp_confidence(
                        connection.get(
                            "confidence"
                        )
                    )

                    new = old * factor

                    connection[
                        "confidence"
                    ] = new

                    changed += 1

        return changed

    # ========================================================
    #
    # RELATED
    #
    # ========================================================

    def related(
        self,
        concept: Any,
        limit: Optional[int] = None,
        relation: Optional[str] = None
    ) -> List[
        Dict[str, Any]
    ]:

        concept = self._normalize_concept(
            concept
        )

        if concept is None:
            return []

        with self.lock:

            node = self.graph.get(
                concept
            )

            if node is None:
                return []

            self.searches += 1
            self.last_search = _utc_now()

            relation = (
                self._normalize_relation(
                    relation
                )
                if relation is not None
                else None
            )

            ranked = []

            for name, metadata in (
                node[
                    "connections"
                ].items()
            ):

                if (
                    relation is not None
                    and
                    metadata.get(
                        "relation"
                    ) != relation
                ):

                    continue

                weight = self._safe_float(
                    metadata.get(
                        "weight"
                    ),
                    0.0
                )

                confidence = (
                    self._clamp_confidence(
                        metadata.get(
                            "confidence"
                        )
                    )
                )

                score = (
                    weight
                    *
                    confidence
                )

                ranked.append(
                    (
                        score,
                        name,
                        metadata
                    )
                )

            ranked.sort(
                key=lambda item: item[0],
                reverse=True
            )

            result = []

            for score, name, metadata in ranked:

                item = copy.deepcopy(
                    metadata
                )

                item[
                    "concept"
                ] = name

                item[
                    "score"
                ] = score

                result.append(
                    item
                )

            if limit is not None:

                return result[
                    :max(
                        0,
                        int(limit)
                    )
                ]

            return result

    # ========================================================
    #
    # NEIGHBORS
    #
    # ========================================================

    def neighbors(
        self,
        concept: Any,
        depth: int = 1
    ) -> List[str]:

        concept = self._normalize_concept(
            concept
        )

        if concept is None:
            return []

        try:
            depth = int(depth)
        except (
            TypeError,
            ValueError
        ):
            return []

        if depth < 1:
            return []

        depth = min(
            depth,
            DEFAULT_MAX_DEPTH
        )

        with self.lock:

            if concept not in self.graph:
                return []

            visited = {
                concept
            }

            queue = deque(
                [
                    (
                        concept,
                        0
                    )
                ]
            )

            result = []

            self.traversals += 1

            while queue:

                current, current_depth = (
                    queue.popleft()
                )

                if current_depth >= depth:
                    continue

                for neighbor in self.graph[
                    current
                ][
                    "connections"
                ]:

                    if neighbor in visited:
                        continue

                    visited.add(
                        neighbor
                    )

                    result.append(
                        neighbor
                    )

                    queue.append(
                        (
                            neighbor,
                            current_depth + 1
                        )
                    )

            return result

    # ========================================================
    #
    # FIND PATH
    #
    # ========================================================

    def find_path(
        self,
        start: Any,
        target: Any
    ) -> List[str]:

        start = self._normalize_concept(
            start
        )

        target = self._normalize_concept(
            target
        )

        if (
            start is None
            or
            target is None
        ):
            return []

        with self.lock:

            if (
                start not in self.graph
                or
                target not in self.graph
            ):

                return []

            if start == target:
                return [start]

            queue = deque(
                [
                    [start]
                ]
            )

            visited = {
                start
            }

            self.traversals += 1
            self.path_searches += 1

            while queue:

                path = queue.popleft()

                current = path[-1]

                for neighbor in self.graph[
                    current
                ][
                    "connections"
                ]:

                    if neighbor in visited:
                        continue

                    new_path = (
                        path
                        +
                        [neighbor]
                    )

                    if neighbor == target:
                        return new_path

                    visited.add(
                        neighbor
                    )

                    queue.append(
                        new_path
                    )

            return []

    # ========================================================
    #
    # WEIGHTED PATH
    #
    # ========================================================

    def find_weighted_path(
        self,
        start: Any,
        target: Any
    ) -> List[str]:

        start = self._normalize_concept(
            start
        )

        target = self._normalize_concept(
            target
        )

        if (
            start is None
            or
            target is None
        ):
            return []

        with self.lock:

            if (
                start not in self.graph
                or
                target not in self.graph
            ):

                return []

            self.path_searches += 1

            queue = [
                (
                    0.0,
                    start,
                    [start]
                )
            ]

            best = {
                start: 0.0
            }

            while queue:

                cost, current, path = (
                    heappop(queue)
                )

                if current == target:
                    return path

                if cost > best.get(
                    current,
                    float("inf")
                ):
                    continue

                for neighbor, metadata in (
                    self.graph[
                        current
                    ][
                        "connections"
                    ].items()
                ):

                    weight = max(
                        0.000001,
                        self._safe_float(
                            metadata.get(
                                "weight"
                            ),
                            1.0
                        )
                    )

                    confidence = max(
                        0.000001,
                        self._clamp_confidence(
                            metadata.get(
                                "confidence"
                            )
                        )
                    )

                    effective = (
                        weight
                        *
                        confidence
                    )

                    edge_cost = (
                        1.0
                        /
                        effective
                    )

                    new_cost = (
                        cost
                        +
                        edge_cost
                    )

                    if new_cost < best.get(
                        neighbor,
                        float("inf")
                    ):

                        best[
                            neighbor
                        ] = new_cost

                        heappush(
                            queue,
                            (
                                new_cost,
                                neighbor,
                                path
                                +
                                [neighbor]
                            )
                        )

            return []

    # ========================================================
    #
    # SEARCH
    #
    # ========================================================

    def search(
        self,
        keyword: Any,
        limit: int = DEFAULT_SEARCH_LIMIT
    ) -> List[
        Dict[str, Any]
    ]:

        if keyword is None:
            return []

        keyword = str(
            keyword
        ).strip().lower()

        if not keyword:
            return []

        with self.lock:

            self.searches += 1
            self.last_search = _utc_now()

            results = []

            for concept, data in (
                self.graph.items()
            ):

                metadata = data.get(
                    "metadata",
                    {}
                )

                score = 0.0

                concept_lower = (
                    concept.lower()
                )

                # Exact match
                if concept_lower == keyword:

                    score += 100.0

                # Prefix
                elif concept_lower.startswith(
                    keyword
                ):

                    score += 75.0

                # Contains
                elif keyword in concept_lower:

                    score += 50.0

                # Metadata search
                metadata_text = " ".join(
                    str(value)
                    for value
                    in metadata.values()
                ).lower()

                if keyword in metadata_text:

                    score += 20.0

                if score <= 0:
                    continue

                observations = int(
                    metadata.get(
                        "observations",
                        0
                    )
                )

                confidence = (
                    self._clamp_confidence(
                        metadata.get(
                            "confidence",
                            1.0
                        )
                    )
                )

                score += min(
                    observations,
                    100
                ) * 0.1

                score += confidence * 10

                results.append(
                    {
                        "concept":
                            concept,

                        "score":
                            score,

                        "metadata":
                            copy.deepcopy(
                                metadata
                            ),

                        "connections":
                            len(
                                data.get(
                                    "connections",
                                    {}
                                )
                            )
                    }
                )

            results.sort(
                key=lambda item:
                    item["score"],
                reverse=True
            )

            return results[
                :max(
                    0,
                    int(limit)
                )
            ]

    # ========================================================
    #
    # FIND BY TAG
    #
    # ========================================================

    def find_by_tag(
        self,
        tag: str
    ) -> List[str]:

        tag = str(
            tag
        ).strip().lower()

        if not tag:
            return []

        with self.lock:

            result = []

            for concept, node in (
                self.graph.items()
            ):

                tags = node[
                    "metadata"
                ].get(
                    "tags",
                    []
                )

                if any(
                    str(item).lower()
                    == tag
                    for item in tags
                ):

                    result.append(
                        concept
                    )

            return result

    # ========================================================
    #
    # FIND BY RELATION
    #
    # ========================================================

    def find_by_relation(
        self,
        relation: str
    ) -> List[
        Dict[str, Any]
    ]:

        relation = self._normalize_relation(
            relation
        )

        with self.lock:

            results = []

            for source, node in (
                self.graph.items()
            ):

                for target, metadata in (
                    node[
                        "connections"
                    ].items()
                ):

                    if metadata.get(
                        "relation"
                    ) != relation:

                        continue

                    results.append(
                        {
                            "source":
                                source,

                            "target":
                                target,

                            "metadata":
                                copy.deepcopy(
                                    metadata
                                )
                        }
                    )

            return results

    # ========================================================
    #
    # LEARNING FROM PAIR
    #
    # ========================================================

    def learn_pair(
        self,
        concept_a: Any,
        concept_b: Any,
        *,
        weight: float = 1.0,
        confidence: float = 1.0,
        relation: str = DEFAULT_RELATION,
        bidirectional: bool = True,
        source: Optional[str] = None
    ) -> bool:

        return self.connect(
            concept_a,
            concept_b,
            weight=weight,
            confidence=confidence,
            relation=relation,
            bidirectional=bidirectional,
            metadata={
                "source":
                    source
            }
        )

    # ========================================================
    #
    # MERGE
    #
    # ========================================================

    def merge(
        self,
        other: Any
    ) -> bool:
        """
        Merge another KnowledgeGraph or exported graph
        into this graph.
        """

        if isinstance(
            other,
            KnowledgeGraph
        ):

            data = other.export()

        elif isinstance(
            other,
            dict
        ):

            data = other

        else:

            return False

        graph_data = data.get(
            "graph",
            {}
        )

        if not isinstance(
            graph_data,
            dict
        ):

            return False

        with self.lock:

            for concept, node in (
                graph_data.items()
            ):

                self.add_node(
                    concept,
                    node.get(
                        "metadata",
                        {}
                    )
                )

                for target, metadata in (
                    node.get(
                        "connections",
                        {}
                    ).items()
                ):

                    self.connect(
                        concept,
                        target,
                        weight=metadata.get(
                            "weight",
                            1.0
                        ),
                        confidence=metadata.get(
                            "confidence",
                            1.0
                        ),
                        bidirectional=False,
                        relation=metadata.get(
                            "relation",
                            DEFAULT_RELATION
                        ),
                        metadata=metadata.get(
                            "metadata",
                            {}
                        )
                    )

            return True

    # ========================================================
    #
    # ALL
    #
    # ========================================================

    def all(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            return copy.deepcopy(
                self.graph
            )

    # ========================================================
    #
    # EXPORT
    #
    # ========================================================

    def export(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            return {

                "version":
                    KNOWLEDGE_GRAPH_VERSION,

                "api_version":
                    API_VERSION,

                "graph":
                    copy.deepcopy(
                        self.graph
                    ),

                "statistics":
                    self.statistics(),

                "timestamp":
                    _utc_now(),

            }

    # ========================================================
    #
    # IMPORT
    #
    # ========================================================

    def import_data(
        self,
        data: Dict[str, Any],
        *,
        merge: bool = True
    ) -> bool:

        if not isinstance(
            data,
            dict
        ):

            return False

        graph_data = data.get(
            "graph",
            {}
        )

        if not isinstance(
            graph_data,
            dict
        ):

            return False

        with self.lock:

            if not merge:

                self.graph.clear()

            for concept, node in (
                graph_data.items()
            ):

                self.add_node(
                    concept,
                    node.get(
                        "metadata",
                        {}
                    )
                )

                for target, metadata in (
                    node.get(
                        "connections",
                        {}
                    ).items()
                ):

                    self.connect(
                        concept,
                        target,
                        weight=metadata.get(
                            "weight",
                            1.0
                        ),
                        confidence=metadata.get(
                            "confidence",
                            1.0
                        ),
                        bidirectional=False,
                        relation=metadata.get(
                            "relation",
                            DEFAULT_RELATION
                        ),
                        metadata=metadata.get(
                            "metadata",
                            {}
                        )
                    )

            return True

    # ========================================================
    #
    # SNAPSHOT
    #
    # ========================================================

    def snapshot(
        self
    ) -> Dict[str, Any]:

        return self.export()

    # ========================================================
    #
    # STATISTICS
    #
    # ========================================================

    def statistics(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            connections = sum(
                len(
                    node.get(
                        "connections",
                        {}
                    )
                )
                for node
                in self.graph.values()
            )

            weighted_connections = []

            confidence_values = []

            for node in self.graph.values():

                for metadata in node[
                    "connections"
                ].values():

                    weighted_connections.append(
                        self._safe_float(
                            metadata.get(
                                "weight"
                            ),
                            0.0
                        )
                    )

                    confidence_values.append(
                        self._clamp_confidence(
                            metadata.get(
                                "confidence"
                            )
                        )
                    )

            average_weight = (
                sum(
                    weighted_connections
                )
                /
                len(
                    weighted_connections
                )
                if weighted_connections
                else 0.0
            )

            average_confidence = (
                sum(
                    confidence_values
                )
                /
                len(
                    confidence_values
                )
                if confidence_values
                else 0.0
            )

            return {

                "nodes":
                    len(
                        self.graph
                    ),

                "connections":
                    connections,

                "nodes_created":
                    self.nodes_created,

                "nodes_removed":
                    self.nodes_removed,

                "connections_created":
                    self.connections_created,

                "connections_removed":
                    self.connections_removed,

                "learning_events":
                    self.learning_events,

                "experience_events":
                    self.experience_events,

                "searches":
                    self.searches,

                "traversals":
                    self.traversals,

                "path_searches":
                    self.path_searches,

                "updates":
                    self.updates,

                "errors":
                    self.errors,

                "average_weight":
                    average_weight,

                "average_confidence":
                    average_confidence,

            }

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ) -> Dict[str, Any]:

        stats = self.statistics()

        return {

            "module":
                "knowledge_graph",

            "status":
                "ONLINE",

            "version":
                KNOWLEDGE_GRAPH_VERSION,

            "api_version":
                API_VERSION,

            "started_at":
                self.started_at,

            "last_learning":
                self.last_learning,

            "last_search":
                self.last_search,

            "last_error":
                self.last_error,

            **stats,

        }

    # ========================================================
    #
    # HEALTH
    #
    # ========================================================

    def health(
        self
    ) -> Dict[str, Any]:

        with self.lock:

            node_count = len(
                self.graph
            )

            connection_count = sum(
                len(
                    node.get(
                        "connections",
                        {}
                    )
                )
                for node
                in self.graph.values()
            )

            return {

                "healthy":
                    True,

                "module":
                    "knowledge_graph",

                "version":
                    KNOWLEDGE_GRAPH_VERSION,

                "nodes":
                    node_count,

                "connections":
                    connection_count,

                "thread_safe":
                    True,

                "confidence_decay":
                    self.confidence_decay,

                "max_nodes":
                    self.max_nodes,

                "max_connections_per_node":
                    self.max_connections_per_node,

            }

    # ========================================================
    #
    # CLEAR
    #
    # ========================================================

    def clear(
        self
    ) -> bool:

        with self.lock:

            self.graph.clear()

            self.nodes_created = 0
            self.nodes_removed = 0

            self.connections_created = 0
            self.connections_removed = 0

            self.learning_events = 0
            self.experience_events = 0

            self.searches = 0
            self.traversals = 0

            self.path_searches = 0
            self.updates = 0

            self.errors = 0

            self.last_learning = None
            self.last_search = None
            self.last_error = None

            return True

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self,
        clear_graph: bool = False
    ) -> bool:

        with self.lock:

            if clear_graph:

                return self.clear()

            for node in self.graph.values():

                metadata = node.get(
                    "metadata",
                    {}
                )

                metadata[
                    "observations"
                ] = 0

                metadata[
                    "learning_events"
                ] = 0

                for connection in node[
                    "connections"
                ].values():

                    connection[
                        "count"
                    ] = 1

            self.learning_events = 0
            self.experience_events = 0

            self.searches = 0
            self.traversals = 0

            self.path_searches = 0
            self.updates = 0

            self.errors = 0

            self.last_learning = None
            self.last_search = None
            self.last_error = None

            return True


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

knowledge_graph = KnowledgeGraph()


# ============================================================
#
# BACKWARD COMPATIBILITY API
#
# ============================================================

def add_node(
    concept: Any,
    metadata: Optional[
        Dict[str, Any]
    ] = None
) -> bool:

    return knowledge_graph.add_node(
        concept,
        metadata
    )


def connect(
    concept_a: Any,
    concept_b: Any,
    weight: float = DEFAULT_WEIGHT,
    confidence: float = DEFAULT_CONFIDENCE,
    bidirectional: bool = True,
    relation: str = DEFAULT_RELATION,
    metadata: Optional[
        Dict[str, Any]
    ] = None,
) -> bool:

    return knowledge_graph.connect(
        concept_a,
        concept_b,
        weight=weight,
        confidence=confidence,
        bidirectional=bidirectional,
        relation=relation,
        metadata=metadata
    )


def learn(
    knowledge: Dict[str, Any]
):

    return knowledge_graph.learn(
        knowledge
    )


def learn_experience(
    experience: Dict[str, Any]
) -> bool:

    return knowledge_graph.learn_experience(
        experience
    )


def related(
    concept: Any,
    limit: Optional[int] = None
):

    return knowledge_graph.related(
        concept,
        limit=limit
    )


def neighbors(
    concept: Any,
    depth: int = 1
):

    return knowledge_graph.neighbors(
        concept,
        depth
    )


def find_path(
    start: Any,
    target: Any
):

    return knowledge_graph.find_path(
        start,
        target
    )


def search(
    keyword: Any,
    limit: int = DEFAULT_SEARCH_LIMIT
):

    return knowledge_graph.search(
        keyword,
        limit
    )


def get(
    concept: Any
):

    return knowledge_graph.get(
        concept
    )


def disconnect(
    concept_a: Any,
    concept_b: Any,
    bidirectional: bool = True
):

    return knowledge_graph.disconnect(
        concept_a,
        concept_b,
        bidirectional
    )


def remove(
    concept: Any
):

    return knowledge_graph.remove(
        concept
    )


def all():

    return knowledge_graph.all()


def export():

    return knowledge_graph.export()


def statistics():

    return knowledge_graph.statistics()


def status():

    return knowledge_graph.status()


def health():

    return knowledge_graph.health()


def clear():

    return knowledge_graph.clear()


# ============================================================
#
# SELF TEST
#
# ============================================================

def test_knowledge_graph() -> Dict[str, Any]:
    """
    Internal validation test.

    Does not modify the global knowledge_graph.
    """

    graph = KnowledgeGraph()

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    assert graph.add_node(
        "market"
    )

    assert graph.add_node(
        "breakout"
    )

    assert graph.add_node(
        "volume"
    )

    # --------------------------------------------------------
    # Connections
    # --------------------------------------------------------

    assert graph.connect(
        "market",
        "breakout",
        weight=2.0,
        confidence=0.9,
        relation=RELATION_SUPPORTS
    )

    assert graph.connect(
        "breakout",
        "volume",
        weight=3.0,
        confidence=0.95,
        relation=RELATION_ASSOCIATED
    )

    # --------------------------------------------------------
    # Learning
    # --------------------------------------------------------

    graph.learn(
        {
            "concept": [
                "market",
                "breakout",
                "volume"
            ],
            "confidence": 0.9,
            "source": "test",
            "tags": [
                "market",
                "technical"
            ]
        }
    )

    # --------------------------------------------------------
    # Related
    # --------------------------------------------------------

    related_result = graph.related(
        "market"
    )

    assert related_result

    # --------------------------------------------------------
    # Neighbors
    # --------------------------------------------------------

    neighbor_result = graph.neighbors(
        "market",
        depth=2
    )

    assert "breakout" in neighbor_result

    # --------------------------------------------------------
    # Path
    # --------------------------------------------------------

    path = graph.find_path(
        "market",
        "volume"
    )

    assert path

    # --------------------------------------------------------
    # Weighted Path
    # --------------------------------------------------------

    weighted_path = graph.find_weighted_path(
        "market",
        "volume"
    )

    assert weighted_path

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    search_result = graph.search(
        "market"
    )

    assert search_result

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    stats = graph.statistics()

    assert stats[
        "nodes"
    ] >= 3

    assert stats[
        "connections"
    ] >= 2

    # --------------------------------------------------------
    # Export
    # --------------------------------------------------------

    exported = graph.export()

    assert "graph" in exported

    # --------------------------------------------------------
    # Import
    # --------------------------------------------------------

    imported = KnowledgeGraph()

    assert imported.import_data(
        exported,
        merge=False
    )

    assert imported.has_node(
        "market"
    )

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    health_data = graph.health()

    assert health_data[
        "healthy"
    ] is True

    # --------------------------------------------------------
    # Disconnect
    # --------------------------------------------------------

    assert graph.disconnect(
        "market",
        "breakout"
    )

    # --------------------------------------------------------
    # Remove
    # --------------------------------------------------------

    assert graph.remove(
        "volume"
    )

    return {

        "success":
            True,

        "nodes":
            stats[
                "nodes"
            ],

        "connections":
            stats[
                "connections"
            ],

        "path":
            path,

        "weighted_path":
            weighted_path,

        "search_results":
            len(
                search_result
            ),

        "status":
            graph.status(),

        "message":
            "Knowledge Graph self-test passed."

    }


# ============================================================
#
# MAIN
#
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )
    )

    print()
    print("=" * 70)
    print("INKSIDE INTELLIGENCE OS")
    print("KNOWLEDGE GRAPH ENGINE")
    print("=" * 70)
    print()

    try:

        result = test_knowledge_graph()

        print(
            "========== TEST RESULT =========="
        )

        print(
            result
        )

        print()

        print(
            "========== GLOBAL STATUS =========="
        )

        print(
            knowledge_graph.status()
        )

        print()

        print("=" * 70)
        print(
            "KNOWLEDGE GRAPH TEST COMPLETE"
        )
        print("=" * 70)

    except Exception as exc:

        logger.exception(
            "Knowledge Graph test failed."
        )

        print()
        print(
            "KNOWLEDGE GRAPH TEST FAILED"
        )
        print(
            str(exc)
        )
        print()