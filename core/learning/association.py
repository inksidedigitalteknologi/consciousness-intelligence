# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# ASSOCIATION ENGINE
#
# VERSION 2.0
#
# DOMAIN-AGNOSTIC RELATIONSHIP INTELLIGENCE
#
# ============================================================

import logging
import math
import re

from collections import defaultdict, Counter
from datetime import datetime


logger = logging.getLogger(__name__)


# ============================================================
#
# ASSOCIATION ENGINE
#
# ============================================================

class AssociationEngine:

    VERSION = "2.0"

    MAX_ASSOCIATIONS_PER_ITEM = 100
    MIN_STRENGTH = 0.01

    def __init__(self):

        # ----------------------------------------------------
        # Core association storage
        # ----------------------------------------------------

        self.rules = defaultdict(dict)

        # ----------------------------------------------------
        # Relationship metadata
        # ----------------------------------------------------

        self.relationships = {}

        # ----------------------------------------------------
        # Frequency tracking
        # ----------------------------------------------------

        self.item_frequency = Counter()

        # ----------------------------------------------------
        # Co-occurrence tracking
        # ----------------------------------------------------

        self.cooccurrence = Counter()

        # ----------------------------------------------------
        # Domain tracking
        # ----------------------------------------------------

        self.domain_items = defaultdict(Counter)

        # ----------------------------------------------------
        # Confidence tracking
        # ----------------------------------------------------

        self.confidence = {}

        # ----------------------------------------------------
        # Learning statistics
        # ----------------------------------------------------

        self.learn_count = 0
        self.prediction_count = 0
        self.success_count = 0

        # ----------------------------------------------------
        # History
        # ----------------------------------------------------

        self.history = []

        # ----------------------------------------------------
        # Last operation
        # ----------------------------------------------------

        self.last_learning = None
        self.last_prediction = None

        logger.info(
            "Association Engine v%s initialized.",
            self.VERSION
        )

    # ========================================================
    #
    # NORMALIZE ITEM
    #
    # ========================================================

    def _normalize(self, item):

        if item is None:
            return None

        if isinstance(item, str):

            item = item.strip().lower()

            item = re.sub(
                r"\s+",
                " ",
                item
            )

            return item

        if isinstance(item, (int, float, bool)):

            return str(item).lower()

        return str(item).strip().lower()

    # ========================================================
    #
    # VALIDATE ITEMS
    #
    # ========================================================

    def _prepare_items(self, items):

        if items is None:
            return []

        if isinstance(items, dict):

            items = list(
                items.keys()
            )

        elif isinstance(items, str):

            items = [items]

        else:

            try:

                items = list(items)

            except Exception:

                items = [items]

        result = []

        seen = set()

        for item in items:

            normalized = self._normalize(
                item
            )

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(
                normalized
            )

            result.append(
                normalized
            )

        return result

    # ========================================================
    #
    # ASSOCIATION STRENGTH
    #
    # ========================================================

    def _calculate_strength(
        self,
        source,
        target
    ):

        pair = (
            source,
            target
        )

        frequency = self.cooccurrence.get(
            pair,
            0
        )

        source_frequency = self.item_frequency.get(
            source,
            0
        )

        if source_frequency <= 0:
            return 0.0

        strength = (
            frequency /
            source_frequency
        )

        return min(
            max(
                strength,
                0.0
            ),
            1.0
        )

    # ========================================================
    #
    # LEARN
    #
    # ========================================================

    def learn(
        self,
        items,
        domain="general",
        context=None,
        weight=1.0
    ):

        try:

            prepared = self._prepare_items(
                items
            )

            if len(prepared) < 2:

                return {
                    "status": "INSUFFICIENT_DATA",
                    "items": prepared,
                    "domain": domain
                }

            weight = max(
                float(weight),
                0.0
            )

            # ------------------------------------------------
            # Frequency
            # ------------------------------------------------

            for item in prepared:

                self.item_frequency[item] += weight

                self.domain_items[
                    domain
                ][item] += weight

            # ------------------------------------------------
            # Pair associations
            # ------------------------------------------------

            created = 0

            for source in prepared:

                for target in prepared:

                    if source == target:
                        continue

                    pair = (
                        source,
                        target
                    )

                    self.cooccurrence[
                        pair
                    ] += weight

                    strength = (
                        self._calculate_strength(
                            source,
                            target
                        )
                    )

                    self.rules[
                        source
                    ][target] = strength

                    self.relationships[
                        f"{source}::{target}"
                    ] = {

                        "source": source,

                        "target": target,

                        "domain": domain,

                        "strength": round(
                            strength,
                            6
                        ),

                        "frequency": self.cooccurrence[
                            pair
                        ],

                        "updated": datetime.now().isoformat()

                    }

                    created += 1

            # ------------------------------------------------
            # Limit associations
            # ------------------------------------------------

            self._prune()

            self.learn_count += 1

            self.last_learning = {

                "time":
                    datetime.now().isoformat(),

                "domain":
                    domain,

                "items":
                    prepared,

                "created":
                    created

            }

            self.history.append(
                self.last_learning
            )

            # Keep history bounded

            if len(self.history) > 1000:

                self.history = (
                    self.history[-1000:]
                )

            return {

                "status": "OK",

                "engine":
                    "Association Engine",

                "version":
                    self.VERSION,

                "domain":
                    domain,

                "items":
                    prepared,

                "associations_created":
                    created,

                "unique_items":
                    len(
                        prepared
                    ),

                "total_items":
                    len(
                        self.item_frequency
                    )

            }

        except Exception as e:

            logger.exception(
                "Association learning failed: %s",
                e
            )

            return {

                "status": "ERROR",

                "error":
                    str(e)

            }

    # ========================================================
    #
    # PRUNE
    #
    # ========================================================

    def _prune(self):

        for source in list(
            self.rules.keys()
        ):

            associations = self.rules[
                source
            ]

            if len(associations) <= self.MAX_ASSOCIATIONS_PER_ITEM:
                continue

            sorted_items = sorted(
                associations.items(),
                key=lambda x: x[1],
                reverse=True
            )

            self.rules[
                source
            ] = dict(
                sorted_items[
                    :self.MAX_ASSOCIATIONS_PER_ITEM
                ]
            )

    # ========================================================
    #
    # PREDICT
    #
    # ========================================================

    def predict(
        self,
        item,
        limit=10,
        min_strength=None
    ):

        try:

            normalized = self._normalize(
                item
            )

            if min_strength is None:

                min_strength = (
                    self.MIN_STRENGTH
                )

            associations = self.rules.get(
                normalized,
                {}
            )

            results = []

            for target, strength in associations.items():

                if strength < min_strength:
                    continue

                results.append({

                    "item":
                        target,

                    "strength":
                        round(
                            strength,
                            6
                        ),

                    "frequency":
                        self.cooccurrence.get(
                            (
                                normalized,
                                target
                            ),
                            0
                        )

                })

            results.sort(
                key=lambda x: x["strength"],
                reverse=True
            )

            results = results[
                :limit
            ]

            self.prediction_count += 1

            self.last_prediction = {

                "time":
                    datetime.now().isoformat(),

                "item":
                    normalized,

                "results":
                    results

            }

            return results

        except Exception as e:

            logger.exception(
                "Association prediction failed: %s",
                e
            )

            return []

    # ========================================================
    #
    # RELATED
    #
    # ========================================================

    def related(
        self,
        item,
        limit=10
    ):

        return self.predict(
            item,
            limit=limit
        )

    # ========================================================
    #
    # STRENGTH
    #
    # ========================================================

    def strength(
        self,
        source,
        target
    ):

        source = self._normalize(
            source
        )

        target = self._normalize(
            target
        )

        return self.rules.get(
            source,
            {}
        ).get(
            target,
            0.0
        )

    # ========================================================
    #
    # FIND PATH
    #
    # ========================================================

    def find_path(
        self,
        source,
        target,
        max_depth=3
    ):

        source = self._normalize(
            source
        )

        target = self._normalize(
            target
        )

        if source == target:

            return [source]

        queue = [
            (
                source,
                [source]
            )
        ]

        visited = {
            source
        }

        while queue:

            current, path = queue.pop(
                0
            )

            if len(path) > max_depth:
                continue

            neighbors = self.rules.get(
                current,
                {}
            )

            for neighbor in neighbors:

                if neighbor in visited:
                    continue

                new_path = (
                    path +
                    [neighbor]
                )

                if neighbor == target:

                    return new_path

                visited.add(
                    neighbor
                )

                queue.append(
                    (
                        neighbor,
                        new_path
                    )
                )

        return []

    # ========================================================
    #
    # COMMON ASSOCIATIONS
    #
    # ========================================================

    def common(
        self,
        items
    ):

        prepared = self._prepare_items(
            items
        )

        if not prepared:
            return []

        sets = []

        for item in prepared:

            related = set(
                self.rules.get(
                    item,
                    {}
                ).keys()
            )

            sets.append(
                related
            )

        if not sets:
            return []

        common_items = set.intersection(
            *sets
        )

        results = []

        for item in common_items:

            strengths = [

                self.strength(
                    source,
                    item
                )

                for source in prepared

            ]

            results.append({

                "item":
                    item,

                "strength":
                    round(
                        sum(
                            strengths
                        ) /
                        len(
                            strengths
                        ),
                        6
                    )

            })

        results.sort(
            key=lambda x: x["strength"],
            reverse=True
        )

        return results

    # ========================================================
    #
    # DOMAIN ASSOCIATIONS
    #
    # ========================================================

    def domain(
        self,
        domain
    ):

        return dict(
            self.domain_items.get(
                domain,
                {}
            )
        )

    # ========================================================
    #
    # ALL ASSOCIATIONS
    #
    # ========================================================

    def all(self):

        result = {}

        for source, targets in self.rules.items():

            result[source] = dict(
                targets
            )

        return result

    # ========================================================
    #
    # TOP ITEMS
    #
    # ========================================================

    def top_items(
        self,
        limit=20
    ):

        return [

            {

                "item":
                    item,

                "frequency":
                    frequency

            }

            for item, frequency
            in self.item_frequency.most_common(
                limit
            )

        ]

    # ========================================================
    #
    # FEEDBACK
    #
    # ========================================================

    def feedback(
        self,
        source,
        target,
        success=True
    ):

        source = self._normalize(
            source
        )

        target = self._normalize(
            target
        )

        key = (
            source,
            target
        )

        if key not in self.cooccurrence:

            return {

                "status":
                    "UNKNOWN_ASSOCIATION",

                "source":
                    source,

                "target":
                    target

            }

        old_strength = self.rules[
            source
        ].get(
            target,
            0.0
        )

        if success:

            self.success_count += 1

            new_strength = min(
                old_strength + 0.05,
                1.0
            )

        else:

            new_strength = max(
                old_strength - 0.05,
                0.0
            )

        self.rules[
            source
        ][target] = new_strength

        relationship_key = (
            f"{source}::{target}"
        )

        if relationship_key in self.relationships:

            self.relationships[
                relationship_key
            ][
                "strength"
            ] = round(
                new_strength,
                6
            )

        return {

            "status":
                "UPDATED",

            "source":
                source,

            "target":
                target,

            "success":
                success,

            "previous":
                round(
                    old_strength,
                    6
                ),

            "new":
                round(
                    new_strength,
                    6
                )

        }

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def clear(self):

        self.rules.clear()

        self.relationships.clear()

        self.item_frequency.clear()

        self.cooccurrence.clear()

        self.domain_items.clear()

        self.confidence.clear()

        self.history.clear()

        self.learn_count = 0

        self.prediction_count = 0

        self.success_count = 0

        self.last_learning = None

        self.last_prediction = None

        logger.warning(
            "Association Engine memory cleared."
        )

        return True

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(self):

        connection_count = sum(

            len(
                targets
            )

            for targets
            in self.rules.values()

        )

        return {

            "module":
                "association",

            "version":
                self.VERSION,

            "online":
                True,

            "items":
                len(
                    self.item_frequency
                ),

            "connections":
                connection_count,

            "relationships":
                len(
                    self.relationships
                ),

            "domains":
                len(
                    self.domain_items
                ),

            "learning_cycles":
                self.learn_count,

            "predictions":
                self.prediction_count,

            "successful_feedback":
                self.success_count,

            "history":
                len(
                    self.history
                ),

            "last_learning":
                self.last_learning,

            "last_prediction":
                self.last_prediction

        }


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

association_engine = AssociationEngine()


# ============================================================
#
# PUBLIC API
#
# ============================================================

__all__ = [
    "AssociationEngine",
    "association_engine",
]


# ============================================================
#
# END
#
# ============================================================