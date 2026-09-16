
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# DATA COLLECTOR
#
# Version: 2.0 Professional Intelligence Data Collector
#
# PURPOSE:
# - Collect raw intelligence data
# - Normalize collection envelope
# - Generate unique collection IDs
# - Track collection statistics
# - Maintain recent collection history
# - Support single + batch collection
# - Support external source metadata
# - Validate incoming data
# - Provide context-compatible output
# - Provide diagnostics and status
# - Backward compatible with DataCollector
#
# ============================================================

import logging
import uuid

from collections import deque
from datetime import datetime, timezone


logger = logging.getLogger(__name__)


class Collector:
    """
    Professional data ingestion layer for INKSIDE INTELLIGENCE OS.

    Collector is intentionally domain-agnostic.

    It does NOT attempt to:
        - analyze data
        - make predictions
        - modify data
        - learn from data
        - make decisions

    Its responsibility is to safely receive raw data and convert it
    into a consistent intelligence collection envelope.
    """

    VERSION = "2.0"

    DEFAULT_HISTORY_SIZE = 500

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        history_size=DEFAULT_HISTORY_SIZE
    ):
        self.name = "collector"

        self.history_size = max(
            1,
            int(history_size)
        )

        self.history = deque(
            maxlen=self.history_size
        )

        # ----------------------------------------------------
        # Counters
        # ----------------------------------------------------

        self.count = 0

        self.success_count = 0
        self.error_count = 0

        self.single_count = 0
        self.batch_count = 0

        self.item_count = 0

        # ----------------------------------------------------
        # Runtime state
        # ----------------------------------------------------

        self.last_collection = None
        self.last_collection_id = None
        self.last_source = None
        self.last_error = None

        self.started_at = self._now()

        logger.info(
            "Collector v%s initialized.",
            self.VERSION
        )

    # ========================================================
    # TIME
    # ========================================================

    @staticmethod
    def _now():
        """
        Return timezone-aware UTC timestamp.
        """

        return datetime.now(
            timezone.utc
        ).isoformat()

    # ========================================================
    # ID GENERATION
    # ========================================================

    @staticmethod
    def _generate_id():
        """
        Generate unique collection identifier.
        """

        return (
            "COL-"
            + uuid.uuid4().hex.upper()
        )

    # ========================================================
    # DATA VALIDATION
    # ========================================================

    def _validate_data(self, data):
        """
        Validate incoming data.

        None is considered valid because the collector can be
        used for event/control signals where the actual payload
        is optional.
        """

        if data is None:
            return True

        if isinstance(
            data,
            (
                dict,
                list,
                tuple,
                str,
                int,
                float,
                bool
            )
        ):
            return True

        # Allow arbitrary objects while keeping diagnostics.
        return True

    # ========================================================
    # SOURCE NORMALIZATION
    # ========================================================

    @staticmethod
    def _normalize_source(source):
        """
        Normalize source metadata.
        """

        if source is None:
            return "unknown"

        source = str(source).strip()

        if not source:
            return "unknown"

        return source

    # ========================================================
    # TYPE DETECTION
    # ========================================================

    @staticmethod
    def _detect_data_type(data):
        """
        Return a stable human-readable data type.
        """

        if data is None:
            return "none"

        if isinstance(data, dict):
            return "dict"

        if isinstance(data, list):
            return "list"

        if isinstance(data, tuple):
            return "tuple"

        if isinstance(data, str):
            return "string"

        if isinstance(data, bool):
            return "boolean"

        if isinstance(data, int):
            return "integer"

        if isinstance(data, float):
            return "float"

        return type(data).__name__

    # ========================================================
    # SIZE ESTIMATION
    # ========================================================

    @staticmethod
    def _estimate_size(data):
        """
        Estimate logical payload size.

        This is intentionally lightweight and does not serialize
        the payload.
        """

        if data is None:
            return 0

        if isinstance(
            data,
            (dict, list, tuple, str)
        ):
            try:
                return len(data)
            except Exception:
                return 1

        return 1

    # ========================================================
    # BUILD ENVELOPE
    # ========================================================

    def _build_envelope(
        self,
        data,
        source="unknown",
        metadata=None,
        event_type=None,
        domain=None
    ):
        """
        Build the standard collector envelope.
        """

        timestamp = self._now()

        collection_id = (
            self._generate_id()
        )

        source = self._normalize_source(
            source
        )

        if metadata is None:
            metadata = {}

        if not isinstance(
            metadata,
            dict
        ):
            metadata = {
                "value": metadata
            }

        envelope = {

            # ------------------------------------------------
            # Identity
            # ------------------------------------------------

            "collection_id":
                collection_id,

            "timestamp":
                timestamp,

            "source":
                source,

            # ------------------------------------------------
            # Classification
            # ------------------------------------------------

            "event_type":
                event_type,

            "domain":
                domain,

            "data_type":
                self._detect_data_type(
                    data
                ),

            # ------------------------------------------------
            # Payload
            # ------------------------------------------------

            "data":
                data,

            # ------------------------------------------------
            # Metadata
            # ------------------------------------------------

            "metadata":
                metadata,

            # ------------------------------------------------
            # Collector information
            # ------------------------------------------------

            "collector":
                self.name,

            "collector_version":
                self.VERSION,

            "sequence":
                self.count + 1,

            "size":
                self._estimate_size(
                    data
                )

        }

        return envelope

    # ========================================================
    # MAIN PROCESS
    # ========================================================

    def process(
        self,
        data=None,
        source="unknown",
        metadata=None,
        event_type=None,
        domain=None
    ):
        """
        Collect one data item.

        Returns:
            dict
                Standard intelligence collection envelope.
        """

        try:

            if not self._validate_data(
                data
            ):
                raise ValueError(
                    "Invalid collector data."
                )

            # ------------------------------------------------
            # Counters
            # ------------------------------------------------

            self.count += 1
            self.single_count += 1
            self.item_count += 1

            # ------------------------------------------------
            # Build envelope
            # ------------------------------------------------

            result = self._build_envelope(
                data=data,
                source=source,
                metadata=metadata,
                event_type=event_type,
                domain=domain
            )

            # ------------------------------------------------
            # Runtime state
            # ------------------------------------------------

            self.success_count += 1

            self.last_collection = (
                result["timestamp"]
            )

            self.last_collection_id = (
                result["collection_id"]
            )

            self.last_source = (
                result["source"]
            )

            self.last_error = None

            # ------------------------------------------------
            # History
            # ------------------------------------------------

            self.history.append(
                result
            )

            logger.debug(
                "Data collected: %s",
                result["collection_id"]
            )

            return result

        except Exception as e:

            self.error_count += 1
            self.last_error = str(e)

            logger.exception(
                "Collector error: %s",
                e
            )

            return {
                "success": False,
                "error": str(e),
                "timestamp": self._now(),
                "source": "collector",
                "data": data
            }

    # ========================================================
    # COLLECT ALIAS
    # ========================================================

    def collect(
        self,
        data=None,
        source="unknown",
        metadata=None,
        event_type=None,
        domain=None
    ):
        """
        Backward-compatible alias for process().
        """

        return self.process(
            data=data,
            source=source,
            metadata=metadata,
            event_type=event_type,
            domain=domain
        )

    # ========================================================
    # BATCH PROCESSING
    # ========================================================

    def process_batch(
        self,
        items,
        source="unknown",
        metadata=None,
        event_type=None,
        domain=None
    ):
        """
        Collect multiple data items.

        Each item receives its own collection envelope.
        """

        try:

            if items is None:
                items = []

            if isinstance(
                items,
                (str, bytes, dict)
            ):
                items = [items]

            items = list(items)

            self.batch_count += 1

            results = []

            for item in items:

                result = self.process(
                    data=item,
                    source=source,
                    metadata=metadata,
                    event_type=event_type,
                    domain=domain
                )

                results.append(
                    result
                )

            return {

                "success": True,

                "timestamp":
                    self._now(),

                "source":
                    self._normalize_source(
                        source
                    ),

                "count":
                    len(results),

                "items":
                    results

            }

        except Exception as e:

            self.error_count += 1
            self.last_error = str(e)

            logger.exception(
                "Collector batch error: %s",
                e
            )

            return {

                "success": False,

                "error":
                    str(e),

                "timestamp":
                    self._now(),

                "source":
                    "collector",

                "count":
                    0,

                "items":
                    []

            }

    # ========================================================
    # BATCH ALIAS
    # ========================================================

    def collect_batch(
        self,
        items,
        source="unknown",
        metadata=None,
        event_type=None,
        domain=None
    ):
        """
        Backward/semantic alias for process_batch().
        """

        return self.process_batch(
            items=items,
            source=source,
            metadata=metadata,
            event_type=event_type,
            domain=domain
        )

    # ========================================================
    # HISTORY
    # ========================================================

    def get_history(
        self,
        limit=10
    ):
        """
        Return most recent collected records.
        """

        try:

            limit = int(limit)

        except Exception:

            limit = 10

        if limit <= 0:
            return []

        return list(
            self.history
        )[-limit:]

    # ========================================================
    # LAST COLLECTION
    # ========================================================

    def get_last(self):
        """
        Return the most recently collected record.
        """

        if not self.history:
            return None

        return self.history[-1]

    # ========================================================
    # FIND BY SOURCE
    # ========================================================

    def get_by_source(
        self,
        source,
        limit=50
    ):
        """
        Return recent records belonging to a source.
        """

        source = self._normalize_source(
            source
        )

        records = [

            item

            for item in self.history

            if item.get("source")
            == source

        ]

        return records[-limit:]

    # ========================================================
    # FIND BY DOMAIN
    # ========================================================

    def get_by_domain(
        self,
        domain,
        limit=50
    ):
        """
        Return recent records belonging to a domain.
        """

        records = [

            item

            for item in self.history

            if item.get("domain")
            == domain

        ]

        return records[-limit:]

    # ========================================================
    # FIND BY EVENT TYPE
    # ========================================================

    def get_by_event_type(
        self,
        event_type,
        limit=50
    ):
        """
        Return recent records matching an event type.
        """

        records = [

            item

            for item in self.history

            if item.get("event_type")
            == event_type

        ]

        return records[-limit:]

    # ========================================================
    # CONTEXT
    # ========================================================

    def build_context(
        self,
        limit=5
    ):
        """
        Produce context information that can be passed to
        ContextManager or downstream intelligence modules.
        """

        recent = self.get_history(
            limit
        )

        return {

            "collector":
                self.name,

            "version":
                self.VERSION,

            "total_collected":
                self.success_count,

            "recent_count":
                len(recent),

            "latest":
                recent[-1]
                if recent
                else None,

            "recent":
                recent

        }

    # ========================================================
    # STATISTICS
    # ========================================================

    def statistics(self):
        """
        Return collection statistics.
        """

        success_rate = 0

        if self.count > 0:

            success_rate = (
                self.success_count
                / self.count
            ) * 100

        return {

            "total":
                self.count,

            "successful":
                self.success_count,

            "errors":
                self.error_count,

            "single_collections":
                self.single_count,

            "batch_collections":
                self.batch_count,

            "items":
                self.item_count,

            "success_rate":
                round(
                    success_rate,
                    2
                ),

            "history_size":
                len(
                    self.history
                )

        }

    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    def clear_history(self):
        """
        Clear recent collection history.

        Statistics are intentionally preserved.
        """

        self.history.clear()

        logger.info(
            "Collector history cleared."
        )

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):
        """
        Completely reset collector runtime state.
        """

        self.history.clear()

        self.count = 0
        self.success_count = 0
        self.error_count = 0

        self.single_count = 0
        self.batch_count = 0
        self.item_count = 0

        self.last_collection = None
        self.last_collection_id = None
        self.last_source = None
        self.last_error = None

        self.started_at = self._now()

        logger.info(
            "Collector reset."
        )

    # ========================================================
    # HEALTH
    # ========================================================

    def health(self):
        """
        Return simple collector health information.
        """

        if self.error_count == 0:

            state = "HEALTHY"

        elif (
            self.success_count
            >
            self.error_count
        ):

            state = "DEGRADED"

        else:

            state = "UNHEALTHY"

        return {

            "module":
                self.name,

            "version":
                self.VERSION,

            "state":
                state,

            "total":
                self.count,

            "success":
                self.success_count,

            "errors":
                self.error_count,

            "last_error":
                self.last_error,

            "last_collection":
                self.last_collection

        }

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):
        """
        Return complete collector status.

        Kept compatible with the original status() API.
        """

        statistics = self.statistics()

        return {

            "name":
                self.name,

            "version":
                self.VERSION,

            "count":
                self.count,

            "last":
                self.last_collection,

            "last_collection_id":
                self.last_collection_id,

            "last_source":
                self.last_source,

            "last_error":
                self.last_error,

            "history":
                len(
                    self.history
                ),

            "history_limit":
                self.history_size,

            "success":
                self.success_count,

            "errors":
                self.error_count,

            "success_rate":
                statistics[
                    "success_rate"
                ],

            "health":
                self.health()[
                    "state"
                ]

        }


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

DataCollector = Collector


# ============================================================
# GLOBAL INSTANCE
# ============================================================

collector = Collector()

