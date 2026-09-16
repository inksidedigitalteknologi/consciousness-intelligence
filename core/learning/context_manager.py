
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# CONTEXT MANAGER
#
# VERSION 5.0 FINAL
#
# ============================================================
#
# PURPOSE
#
# Context Manager is the SHORT-TERM WORKING CONTEXT layer.
#
# It answers:
#
#   "What is happening now?"
#   "What happened recently?"
#   "What did the system observe?"
#   "What signal was generated?"
#   "What was predicted?"
#   "What decision was made?"
#   "What happened afterward?"
#   "Is the reasoning pipeline complete?"
#
# Context Manager is NOT permanent memory.
#
# Permanent memory belongs to:
#
#   LearningMemory
#   SemanticMemory
#   KnowledgeGraph
#   ArchiveManager
#
# PIPELINE:
#
# OBSERVATION
#      ↓
# MARKET STATE
#      ↓
# SIGNAL
#      ↓
# PREDICTION
#      ↓
# DECISION
#      ↓
# OUTCOME
#      ↓
# LEARNING
#
# VERSION 5.0 adds:
#
#   - Thread safety
#   - Temporal awareness
#   - Context relevance scoring
#   - Pipeline state tracking
#   - Pipeline consistency checking
#   - Confidence analysis
#   - Activity analysis
#   - Context summary
#   - Event age calculation
#   - Time-window queries
#   - Pair/timeframe contextual matching
#   - Current context synchronization
#   - Better import/export reconstruction
#   - Backward compatibility
#
# ============================================================

import copy
import logging
import threading

from collections import Counter, deque
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


# ============================================================
#
# CONTEXT MANAGER
#
# ============================================================

class ContextManager:
    """
    Comprehensive temporal and situational context manager.

    This module provides short-term working memory for the
    Intelligence OS.

    It does not make decisions and does not replace permanent
    learning memory.
    """

    VERSION = "5.0"

    DEFAULT_MAX_SIZE = 1000

    # ========================================================
    #
    # INITIALIZATION
    #
    # ========================================================

    def __init__(
        self,
        max_size=DEFAULT_MAX_SIZE
    ):

        try:
            max_size = int(max_size)

        except Exception:
            max_size = self.DEFAULT_MAX_SIZE

        if max_size <= 0:
            max_size = self.DEFAULT_MAX_SIZE

        self.max_size = max_size

        # ----------------------------------------------------
        # THREAD SAFETY
        # ----------------------------------------------------

        self._lock = threading.RLock()

        # ----------------------------------------------------
        # MAIN EVENT HISTORY
        # ----------------------------------------------------

        self.history = deque(
            maxlen=self.max_size
        )

        # ----------------------------------------------------
        # CURRENT CONTEXT
        # ----------------------------------------------------

        self.current_context = {}

        self.current_market_context = {}

        self.current_signal_context = {}

        self.current_prediction_context = {}

        self.current_decision_context = {}

        self.current_outcome_context = {}

        self.current_learning_context = {}

        # ----------------------------------------------------
        # COUNTERS
        # ----------------------------------------------------

        self.total_events = 0

        self.sequence = 0

        self.total_observations = 0

        self.total_signals = 0

        self.total_predictions = 0

        self.total_decisions = 0

        self.total_outcomes = 0

        self.total_learning_events = 0

        # ----------------------------------------------------
        # LAST EVENT REFERENCES
        # ----------------------------------------------------

        self.last_event = None

        self.last_observation = None

        self.last_signal = None

        self.last_prediction = None

        self.last_decision = None

        self.last_outcome = None

        self.last_learning_event = None

        # ----------------------------------------------------
        # DOMAIN TRACKING
        # ----------------------------------------------------

        self.domain_counter = Counter()

        self.event_counter = Counter()

        self.source_counter = Counter()

        self.pair_counter = Counter()

        self.timeframe_counter = Counter()

        self.tag_counter = Counter()

        # ----------------------------------------------------
        # LIFETIME
        # ----------------------------------------------------

        self.created_at = (
            datetime.now().isoformat()
        )

        self.updated_at = self.created_at

        logger.info(
            "Context Manager v%s initialized | max_size=%s",
            self.VERSION,
            self.max_size
        )

    # ========================================================
    #
    # INTERNAL HELPERS
    #
    # ========================================================

    def _timestamp(self):

        return datetime.now().isoformat()

    # --------------------------------------------------------

    def _next_sequence(self):

        self.sequence += 1

        return self.sequence

    # --------------------------------------------------------

    def _safe_copy(
        self,
        value
    ):

        try:

            return copy.deepcopy(
                value
            )

        except Exception:

            return value

    # --------------------------------------------------------

    def _normalize_string(
        self,
        value
    ):

        if value is None:
            return None

        try:

            value = str(
                value
            ).strip()

            return (
                value
                if value
                else None
            )

        except Exception:

            return None

    # --------------------------------------------------------

    def _safe_limit(
        self,
        limit,
        default=10
    ):

        try:

            limit = int(
                limit
            )

        except Exception:

            limit = default

        if limit <= 0:
            return 0

        return limit

    # ========================================================
    #
    # EVENT NORMALIZATION
    #
    # ========================================================

    def _normalize_event(
        self,
        data,
        domain=None,
        event_type=None,
        source=None,
        pair=None,
        timeframe=None,
        confidence=None,
        tags=None,
        metadata=None
    ):
        """
        Normalize incoming context into a common event schema.
        """

        timestamp = self._timestamp()

        sequence = self._next_sequence()

        # ----------------------------------------------------
        # PAYLOAD
        # ----------------------------------------------------

        if isinstance(
            data,
            dict
        ):

            payload = self._safe_copy(
                data
            )

        else:

            payload = {
                "value":
                    self._safe_copy(
                        data
                    )
            }

        # ----------------------------------------------------
        # INFERENCE
        # ----------------------------------------------------

        if domain is None:

            domain = payload.get(
                "domain"
            )

        if event_type is None:

            event_type = payload.get(
                "event_type",
                payload.get(
                    "type"
                )
            )

        if source is None:

            source = payload.get(
                "source"
            )

        if pair is None:

            pair = payload.get(
                "pair",
                payload.get(
                    "symbol"
                )
            )

        if timeframe is None:

            timeframe = payload.get(
                "timeframe",
                payload.get(
                    "tf"
                )
            )

        if confidence is None:

            confidence = payload.get(
                "confidence"
            )

        if tags is None:

            tags = payload.get(
                "tags",
                []
            )

        if metadata is None:

            metadata = payload.get(
                "metadata",
                {}
            )

        # ----------------------------------------------------
        # NORMALIZE CONFIDENCE
        # ----------------------------------------------------

        normalized_confidence = (
            self._normalize_confidence(
                confidence
            )
        )

        # ----------------------------------------------------
        # NORMALIZE TAGS
        # ----------------------------------------------------

        if tags is None:

            tags = []

        elif isinstance(
            tags,
            str
        ):

            tags = [tags]

        elif not isinstance(
            tags,
            (list, tuple, set)
        ):

            tags = [str(tags)]

        tags = [

            str(tag).strip()

            for tag in tags

            if tag is not None
            and str(tag).strip()

        ]

        # ----------------------------------------------------
        # NORMALIZE METADATA
        # ----------------------------------------------------

        if not isinstance(
            metadata,
            dict
        ):

            metadata = {
                "value":
                    self._safe_copy(
                        metadata
                    )
            }

        # ----------------------------------------------------
        # EVENT
        # ----------------------------------------------------

        event = {

            "sequence":
                sequence,

            "timestamp":
                timestamp,

            "domain":
                self._normalize_string(
                    domain
                ),

            "event_type":
                self._normalize_string(
                    event_type
                ),

            "source":
                self._normalize_string(
                    source
                ),

            "pair":
                self._normalize_string(
                    pair
                ),

            "timeframe":
                self._normalize_string(
                    timeframe
                ),

            "confidence":
                normalized_confidence,

            "tags":
                tags,

            "metadata":
                self._safe_copy(
                    metadata
                ),

            "data":
                payload

        }

        return event

    # ========================================================
    #
    # CONFIDENCE NORMALIZATION
    #
    # ========================================================

    def _normalize_confidence(
        self,
        value
    ):

        if value is None:
            return None

        try:

            value = float(
                value
            )

        except Exception:

            return None

        # Accept both:
        #
        # 0.0 - 1.0
        # 0 - 100

        if 0 <= value <= 1:

            value *= 100

        return max(
            0.0,
            min(
                100.0,
                value
            )
        )

    # ========================================================
    #
    # ADD EVENT
    #
    # ========================================================

    def add(
        self,
        data,
        domain=None,
        event_type=None,
        source=None,
        pair=None,
        timeframe=None,
        confidence=None,
        tags=None,
        metadata=None
    ):
        """
        Add an event to working context.

        Backward compatible:

            context_manager.add(data)

        Extended:

            context_manager.add(
                data,
                domain="trading",
                event_type="signal",
                source="scanner",
                pair="BTC/USD",
                timeframe="1h",
                confidence=82
            )
        """

        with self._lock:

            try:

                event = self._normalize_event(
                    data=data,
                    domain=domain,
                    event_type=event_type,
                    source=source,
                    pair=pair,
                    timeframe=timeframe,
                    confidence=confidence,
                    tags=tags,
                    metadata=metadata
                )

                self.history.append(
                    event
                )

                self.total_events += 1

                self.updated_at = (
                    event["timestamp"]
                )

                self.last_event = event

                # ------------------------------------------------
                # COUNTERS
                # ------------------------------------------------

                if event["domain"]:

                    self.domain_counter[
                        event["domain"]
                    ] += 1

                if event["event_type"]:

                    self.event_counter[
                        event["event_type"]
                    ] += 1

                if event["source"]:

                    self.source_counter[
                        event["source"]
                    ] += 1

                if event["pair"]:

                    self.pair_counter[
                        event["pair"]
                    ] += 1

                if event["timeframe"]:

                    self.timeframe_counter[
                        event["timeframe"]
                    ] += 1

                for tag in event["tags"]:

                    self.tag_counter[
                        tag
                    ] += 1

                # ------------------------------------------------
                # CATEGORIZATION
                # ------------------------------------------------

                self._categorize_event(
                    event
                )

                # ------------------------------------------------
                # CURRENT CONTEXT
                # ------------------------------------------------

                self._sync_current_context()

                return self._safe_copy(
                    event
                )

            except Exception as e:

                logger.exception(
                    "Context event add failed: %s",
                    e
                )

                return None

    # ========================================================
    #
    # EVENT CATEGORIZATION
    #
    # ========================================================

    def _categorize_event(
        self,
        event
    ):

        event_type = (
            event.get(
                "event_type"
            )
            or ""
        ).lower()

        data = event.get(
            "data",
            {}
        )

        if not isinstance(
            data,
            dict
        ):

            data = {}

        # ----------------------------------------------------
        # OBSERVATION
        # ----------------------------------------------------

        if event_type in (
            "observation",
            "market_observation",
            "observe"
        ):

            self.total_observations += 1

            self.last_observation = event

        # ----------------------------------------------------
        # MARKET
        # ----------------------------------------------------

        if event_type in (
            "market",
            "market_state",
            "market_observation"
        ):

            self.current_market_context = (
                self._safe_copy(
                    data
                )
            )

        # ----------------------------------------------------
        # SIGNAL
        # ----------------------------------------------------

        if event_type in (
            "signal",
            "trading_signal",
            "signal_generated"
        ):

            self.total_signals += 1

            self.last_signal = event

            self.current_signal_context = (
                self._safe_copy(
                    data
                )
            )

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        if event_type in (
            "prediction",
            "forecast"
        ):

            self.total_predictions += 1

            self.last_prediction = event

            self.current_prediction_context = (
                self._safe_copy(
                    data
                )
            )

        # ----------------------------------------------------
        # DECISION
        # ----------------------------------------------------

        if event_type in (
            "decision",
            "action"
        ):

            self.total_decisions += 1

            self.last_decision = event

            self.current_decision_context = (
                self._safe_copy(
                    data
                )
            )

        # ----------------------------------------------------
        # OUTCOME
        # ----------------------------------------------------

        if event_type in (
            "outcome",
            "result",
            "trade_result"
        ):

            self.total_outcomes += 1

            self.last_outcome = event

            self.current_outcome_context = (
                self._safe_copy(
                    data
                )
            )

        # ----------------------------------------------------
        # LEARNING
        # ----------------------------------------------------

        if event_type in (
            "learning",
            "learning_result",
            "experience",
            "evaluation",
            "feedback"
        ):

            self.total_learning_events += 1

            self.last_learning_event = event

            self.current_learning_context = (
                self._safe_copy(
                    data
                )
            )

        # ----------------------------------------------------
        # TRADING DOMAIN
        # ----------------------------------------------------

        if event.get(
            "domain"
        ) == "trading":

            self.current_market_context = (
                self._safe_copy(
                    data
                )
                if event_type in (
                    "market",
                    "market_state",
                    "market_observation"
                )
                else self.current_market_context
            )

    # ========================================================
    #
    # CURRENT CONTEXT SYNCHRONIZATION
    #
    # ========================================================

    def _sync_current_context(
        self
    ):

        self.current_context = {

            "market":
                self._safe_copy(
                    self.current_market_context
                ),

            "signal":
                self._safe_copy(
                    self.current_signal_context
                ),

            "prediction":
                self._safe_copy(
                    self.current_prediction_context
                ),

            "decision":
                self._safe_copy(
                    self.current_decision_context
                ),

            "outcome":
                self._safe_copy(
                    self.current_outcome_context
                ),

            "learning":
                self._safe_copy(
                    self.current_learning_context
                ),

            "latest":
                self._safe_copy(
                    self.last_event
                )

        }

    # ========================================================
    #
    # SPECIALIZED ADD METHODS
    #
    # ========================================================

    def add_observation(
        self,
        data,
        **kwargs
    ):

        kwargs.setdefault(
            "domain",
            "trading"
        )

        kwargs.setdefault(
            "event_type",
            "observation"
        )

        return self.add(
            data,
            **kwargs
        )

    # --------------------------------------------------------

    def add_market_state(
        self,
        data,
        pair=None,
        timeframe=None,
        **kwargs
    ):

        kwargs.setdefault(
            "domain",
            "trading"
        )

        kwargs.setdefault(
            "event_type",
            "market_state"
        )

        return self.add(
            data,
            pair=pair,
            timeframe=timeframe,
            **kwargs
        )

    # --------------------------------------------------------

    def add_signal(
        self,
        data,
        pair=None,
        timeframe=None,
        confidence=None,
        **kwargs
    ):

        kwargs.setdefault(
            "domain",
            "trading"
        )

        kwargs.setdefault(
            "event_type",
            "signal"
        )

        return self.add(
            data,
            pair=pair,
            timeframe=timeframe,
            confidence=confidence,
            **kwargs
        )

    # --------------------------------------------------------

    def add_prediction(
        self,
        data,
        pair=None,
        timeframe=None,
        confidence=None,
        **kwargs
    ):

        kwargs.setdefault(
            "domain",
            "trading"
        )

        kwargs.setdefault(
            "event_type",
            "prediction"
        )

        return self.add(
            data,
            pair=pair,
            timeframe=timeframe,
            confidence=confidence,
            **kwargs
        )

    # --------------------------------------------------------

    def add_decision(
        self,
        data,
        pair=None,
        timeframe=None,
        **kwargs
    ):

        kwargs.setdefault(
            "domain",
            "trading"
        )

        kwargs.setdefault(
            "event_type",
            "decision"
        )

        return self.add(
            data,
            pair=pair,
            timeframe=timeframe,
            **kwargs
        )

    # --------------------------------------------------------

    def add_outcome(
        self,
        data,
        pair=None,
        timeframe=None,
        **kwargs
    ):

        kwargs.setdefault(
            "domain",
            "trading"
        )

        kwargs.setdefault(
            "event_type",
            "outcome"
        )

        return self.add(
            data,
            pair=pair,
            timeframe=timeframe,
            **kwargs
        )

    # --------------------------------------------------------

    def add_learning(
        self,
        data,
        domain=None,
        **kwargs
    ):

        kwargs.setdefault(
            "event_type",
            "learning"
        )

        return self.add(
            data,
            domain=domain,
            **kwargs
        )

    # ========================================================
    #
    # RECENT EVENTS
    #
    # ========================================================

    def get_recent(
        self,
        limit=10
    ):

        limit = self._safe_limit(
            limit
        )

        if limit <= 0:
            return []

        with self._lock:

            return self._safe_copy(
                list(
                    self.history
                )[-limit:]
            )

    # ========================================================
    #
    # LATEST
    #
    # ========================================================

    def latest(
        self
    ):

        with self._lock:

            if not self.history:
                return None

            return self._safe_copy(
                self.history[-1]
            )

    # ========================================================
    #
    # CONTEXT WINDOW
    #
    # ========================================================

    def context_window(
        self,
        limit=20
    ):

        return self.get_recent(
            limit
        )

    # ========================================================
    #
    # DOMAIN CONTEXT
    #
    # ========================================================

    def get_domain_context(
        self,
        domain,
        limit=10
    ):

        if not domain:
            return []

        limit = self._safe_limit(
            limit
        )

        with self._lock:

            events = [

                event

                for event in self.history

                if event.get(
                    "domain"
                ) == domain

            ]

            return self._safe_copy(
                events[-limit:]
            )

    # ========================================================
    #
    # EVENT TYPE CONTEXT
    #
    # ========================================================

    def get_event_context(
        self,
        event_type,
        limit=10
    ):

        if not event_type:
            return []

        limit = self._safe_limit(
            limit
        )

        with self._lock:

            events = [

                event

                for event in self.history

                if event.get(
                    "event_type"
                ) == event_type

            ]

            return self._safe_copy(
                events[-limit:]
            )

    # ========================================================
    #
    # PAIR CONTEXT
    #
    # ========================================================

    def get_pair_context(
        self,
        pair,
        limit=10
    ):

        if not pair:
            return []

        limit = self._safe_limit(
            limit
        )

        with self._lock:

            events = [

                event

                for event in self.history

                if event.get(
                    "pair"
                ) == pair

            ]

            return self._safe_copy(
                events[-limit:]
            )

    # ========================================================
    #
    # TIMEFRAME CONTEXT
    #
    # ========================================================

    def get_timeframe_context(
        self,
        timeframe,
        limit=10
    ):

        if not timeframe:
            return []

        limit = self._safe_limit(
            limit
        )

        with self._lock:

            events = [

                event

                for event in self.history

                if event.get(
                    "timeframe"
                ) == timeframe

            ]

            return self._safe_copy(
                events[-limit:]
            )

    # ========================================================
    #
    # TRADING CONTEXT
    #
    # ========================================================

    def get_trading_context(
        self,
        pair=None,
        timeframe=None,
        limit=20
    ):

        limit = self._safe_limit(
            limit
        )

        with self._lock:

            events = []

            for event in self.history:

                if event.get(
                    "domain"
                ) != "trading":

                    continue

                if (
                    pair is not None
                    and
                    event.get(
                        "pair"
                    ) != pair
                ):

                    continue

                if (
                    timeframe is not None
                    and
                    event.get(
                        "timeframe"
                    ) != timeframe
                ):

                    continue

                events.append(
                    event
                )

            return self._safe_copy(
                events[-limit:]
            )

    # ========================================================
    #
    # SIGNAL CONTEXT
    #
    # ========================================================

    def get_signal_context(
        self,
        pair=None,
        timeframe=None,
        limit=20
    ):

        return self._filtered_event_context(
            "signal",
            pair,
            timeframe,
            limit
        )

    # ========================================================
    #
    # PREDICTION CONTEXT
    #
    # ========================================================

    def get_prediction_context(
        self,
        pair=None,
        timeframe=None,
        limit=20
    ):

        return self._filtered_event_context(
            "prediction",
            pair,
            timeframe,
            limit
        )

    # ========================================================
    #
    # OUTCOME CONTEXT
    #
    # ========================================================

    def get_outcome_context(
        self,
        pair=None,
        timeframe=None,
        limit=20
    ):

        return self._filtered_event_context(
            "outcome",
            pair,
            timeframe,
            limit
        )

    # ========================================================
    #
    # INTERNAL FILTER
    #
    # ========================================================

    def _filtered_event_context(
        self,
        event_type,
        pair=None,
        timeframe=None,
        limit=20
    ):

        limit = self._safe_limit(
            limit
        )

        with self._lock:

            events = [

                event

                for event in self.history

                if event.get(
                    "event_type"
                ) == event_type

                and (
                    pair is None
                    or
                    event.get(
                        "pair"
                    ) == pair
                )

                and (
                    timeframe is None
                    or
                    event.get(
                        "timeframe"
                    ) == timeframe
                )

            ]

            return self._safe_copy(
                events[-limit:]
            )

    # ========================================================
    #
    # TAG SEARCH
    #
    # ========================================================

    def find_by_tag(
        self,
        tag,
        limit=20
    ):

        if not tag:
            return []

        limit = self._safe_limit(
            limit
        )

        tag = str(
            tag
        )

        with self._lock:

            events = [

                event

                for event in self.history

                if tag in event.get(
                    "tags",
                    []
                )

            ]

            return self._safe_copy(
                events[-limit:]
            )

    # ========================================================
    #
    # SOURCE SEARCH
    #
    # ========================================================

    def find_by_source(
        self,
        source,
        limit=20
    ):

        if not source:
            return []

        limit = self._safe_limit(
            limit
        )

        with self._lock:

            events = [

                event

                for event in self.history

                if event.get(
                    "source"
                ) == source

            ]

            return self._safe_copy(
                events[-limit:]
            )

    # ========================================================
    #
    # TIME WINDOW
    #
    # ========================================================

    def get_recent_by_seconds(
        self,
        seconds=300,
        limit=None
    ):
        """
        Return events created within the last N seconds.
        """

        try:

            seconds = float(
                seconds
            )

        except Exception:

            seconds = 300

        if seconds <= 0:
            return []

        cutoff = (
            datetime.now()
            - timedelta(
                seconds=seconds
            )
        )

        with self._lock:

            result = []

            for event in self.history:

                try:

                    event_time = datetime.fromisoformat(
                        event.get(
                            "timestamp"
                        )
                    )

                except Exception:

                    continue

                if event_time >= cutoff:

                    result.append(
                        event
                    )

            if limit is not None:

                limit = self._safe_limit(
                    limit
                )

                result = result[-limit:]

            return self._safe_copy(
                result
            )

    # ========================================================
    #
    # EVENT AGE
    #
    # ========================================================

    def event_age_seconds(
        self,
        event
    ):

        if not isinstance(
            event,
            dict
        ):

            return None

        timestamp = event.get(
            "timestamp"
        )

        if not timestamp:
            return None

        try:

            created = datetime.fromisoformat(
                timestamp
            )

            age = (
                datetime.now()
                - created
            ).total_seconds()

            return max(
                0.0,
                age
            )

        except Exception:

            return None

    # ========================================================
    #
    # PIPELINE STATE
    #
    # ========================================================

    def pipeline_state(
        self,
        pair=None,
        timeframe=None
    ):
        """
        Describe the current intelligence pipeline.

        OBSERVATION
        MARKET
        SIGNAL
        PREDICTION
        DECISION
        OUTCOME
        LEARNING
        """

        with self._lock:

            def latest_matching(
                event_types
            ):

                for event in reversed(
                    self.history
                ):

                    if event.get(
                        "event_type"
                    ) not in event_types:

                        continue

                    if (
                        pair is not None
                        and
                        event.get(
                            "pair"
                        ) != pair
                    ):

                        continue

                    if (
                        timeframe is not None
                        and
                        event.get(
                            "timeframe"
                        ) != timeframe
                    ):

                        continue

                    return event

                return None

            observation = latest_matching(
                {
                    "observation",
                    "market_observation"
                }
            )

            market = latest_matching(
                {
                    "market",
                    "market_state"
                }
            )

            signal = latest_matching(
                {
                    "signal",
                    "trading_signal",
                    "signal_generated"
                }
            )

            prediction = latest_matching(
                {
                    "prediction",
                    "forecast"
                }
            )

            decision = latest_matching(
                {
                    "decision",
                    "action"
                }
            )

            outcome = latest_matching(
                {
                    "outcome",
                    "result",
                    "trade_result"
                }
            )

            learning = latest_matching(
                {
                    "learning",
                    "learning_result",
                    "experience",
                    "evaluation",
                    "feedback"
                }
            )

            stages = {

                "observation":
                    observation is not None,

                "market":
                    market is not None,

                "signal":
                    signal is not None,

                "prediction":
                    prediction is not None,

                "decision":
                    decision is not None,

                "outcome":
                    outcome is not None,

                "learning":
                    learning is not None

            }

            completed = sum(
                1
                for value in stages.values()
                if value
            )

            return {

                "stages":
                    stages,

                "completed":
                    completed,

                "total_stages":
                    len(stages),

                "completion_percent":
                    round(
                        (
                            completed
                            / len(stages)
                        ) * 100,
                        2
                    ),

                "next_stage":
                    self._next_pipeline_stage(
                        stages
                    ),

                "latest": {

                    "observation":
                        self._safe_copy(
                            observation
                        ),

                    "market":
                        self._safe_copy(
                            market
                        ),

                    "signal":
                        self._safe_copy(
                            signal
                        ),

                    "prediction":
                        self._safe_copy(
                            prediction
                        ),

                    "decision":
                        self._safe_copy(
                            decision
                        ),

                    "outcome":
                        self._safe_copy(
                            outcome
                        ),

                    "learning":
                        self._safe_copy(
                            learning
                        )

                }

            }

    # ========================================================
    #
    # NEXT PIPELINE STAGE
    #
    # ========================================================

    def _next_pipeline_stage(
        self,
        stages
    ):

        order = [

            "observation",
            "market",
            "signal",
            "prediction",
            "decision",
            "outcome",
            "learning"

        ]

        for stage in order:

            if not stages.get(
                stage,
                False
            ):

                return stage

        return "complete"

    # ========================================================
    #
    # PIPELINE CONSISTENCY
    #
    # ========================================================

    def validate_pipeline(
        self,
        pair=None,
        timeframe=None
    ):
        """
        Check whether the intelligence pipeline has logical
        continuity.
        """

        state = self.pipeline_state(
            pair=pair,
            timeframe=timeframe
        )

        stages = state[
            "stages"
        ]

        warnings = []

        if stages["prediction"] and not stages["signal"]:

            warnings.append(
                "Prediction exists without signal context"
            )

        if stages["decision"] and not stages["prediction"]:

            warnings.append(
                "Decision exists without prediction context"
            )

        if stages["outcome"] and not stages["decision"]:

            warnings.append(
                "Outcome exists without decision context"
            )

        if stages["learning"] and not stages["outcome"]:

            warnings.append(
                "Learning exists without outcome context"
            )

        return {

            "valid":
                len(warnings) == 0,

            "warnings":
                warnings,

            "pipeline":
                state

        }

    # ========================================================
    #
    # CONFIDENCE ANALYSIS
    #
    # ========================================================

    def confidence_analysis(
        self,
        limit=100
    ):
        """
        Analyze confidence distribution across recent events.
        """

        limit = self._safe_limit(
            limit,
            default=100
        )

        with self._lock:

            events = list(
                self.history
            )[-limit:]

            values = [

                event.get(
                    "confidence"
                )

                for event in events

                if event.get(
                    "confidence"
                ) is not None

            ]

            if not values:

                return {

                    "count": 0,

                    "average": 0,

                    "minimum": 0,

                    "maximum": 0,

                    "high": 0,

                    "medium": 0,

                    "low": 0

                }

            high = sum(
                1
                for value in values
                if value >= 70
            )

            medium = sum(
                1
                for value in values
                if 50 <= value < 70
            )

            low = sum(
                1
                for value in values
                if value < 50
            )

            return {

                "count":
                    len(values),

                "average":
                    round(
                        sum(values)
                        / len(values),
                        2
                    ),

                "minimum":
                    min(values),

                "maximum":
                    max(values),

                "high":
                    high,

                "medium":
                    medium,

                "low":
                    low

            }

    # ========================================================
    #
    # ACTIVITY ANALYSIS
    #
    # ========================================================

    def activity_analysis(
        self
    ):

        with self._lock:

            if not self.history:

                return {

                    "active":
                        False,

                    "events_last_60s":
                        0,

                    "events_last_5m":
                        0,

                    "events_last_1h":
                        0

                }

        return {

            "active":
                bool(
                    self.get_recent_by_seconds(
                        60
                    )
                ),

            "events_last_60s":
                len(
                    self.get_recent_by_seconds(
                        60
                    )
                ),

            "events_last_5m":
                len(
                    self.get_recent_by_seconds(
                        300
                    )
                ),

            "events_last_1h":
                len(
                    self.get_recent_by_seconds(
                        3600
                    )
                )

        }

    # ========================================================
    #
    # CONTEXT RELEVANCE
    #
    # ========================================================

    def relevance_score(
        self,
        event,
        pair=None,
        timeframe=None,
        event_type=None,
        domain=None
    ):
        """
        Calculate contextual relevance from 0-100.

        Relevance factors:

            pair match       +30
            timeframe match  +20
            event type       +20
            domain match     +15
            recency           +15
        """

        if not isinstance(
            event,
            dict
        ):

            return 0

        score = 0

        if (
            pair is not None
            and
            event.get(
                "pair"
            ) == pair
        ):

            score += 30

        if (
            timeframe is not None
            and
            event.get(
                "timeframe"
            ) == timeframe
        ):

            score += 20

        if (
            event_type is not None
            and
            event.get(
                "event_type"
            ) == event_type
        ):

            score += 20

        if (
            domain is not None
            and
            event.get(
                "domain"
            ) == domain
        ):

            score += 15

        age = self.event_age_seconds(
            event
        )

        if age is not None:

            if age <= 60:
                score += 15

            elif age <= 300:
                score += 12

            elif age <= 1800:
                score += 9

            elif age <= 3600:
                score += 6

            elif age <= 21600:
                score += 3

        return min(
            100,
            score
        )

    # ========================================================
    #
    # MOST RELEVANT CONTEXT
    #
    # ========================================================

    def get_relevant_context(
        self,
        pair=None,
        timeframe=None,
        event_type=None,
        domain=None,
        limit=20
    ):

        limit = self._safe_limit(
            limit
        )

        with self._lock:

            ranked = []

            for event in self.history:

                score = self.relevance_score(
                    event,
                    pair=pair,
                    timeframe=timeframe,
                    event_type=event_type,
                    domain=domain
                )

                if score > 0:

                    ranked.append(
                        (
                            score,
                            event
                        )
                    )

            ranked.sort(
                key=lambda item: (
                    item[0],
                    item[1].get(
                        "sequence",
                        0
                    )
                ),
                reverse=True
            )

            result = []

            for score, event in ranked[:limit]:

                item = self._safe_copy(
                    event
                )

                item[
                    "relevance_score"
                ] = score

                result.append(
                    item
                )

            return result

    # ========================================================
    #
    # CURRENT STATE
    #
    # ========================================================

    def current_state(
        self
    ):

        with self._lock:

            return {

                "market":
                    self._safe_copy(
                        self.current_market_context
                    ),

                "signal":
                    self._safe_copy(
                        self.current_signal_context
                    ),

                "prediction":
                    self._safe_copy(
                        self.current_prediction_context
                    ),

                "decision":
                    self._safe_copy(
                        self.current_decision_context
                    ),

                "outcome":
                    self._safe_copy(
                        self.current_outcome_context
                    ),

                "learning":
                    self._safe_copy(
                        self.current_learning_context
                    ),

                "latest":
                    self._safe_copy(
                        self.last_event
                    )

            }

    # ========================================================
    #
    # BUILD CONTEXT
    #
    # ========================================================

    def build_context(
        self,
        limit=10
    ):
        """
        Build comprehensive situational context.
        """

        return {

            "version":
                self.VERSION,

            "timestamp":
                self._timestamp(),

            "sequence":
                self.sequence,

            "total_events":
                self.total_events,

            "recent_events":
                len(self.history),

            "recent":
                self.get_recent(
                    limit
                ),

            "latest":
                self.latest(),

            "market":
                self._safe_copy(
                    self.current_market_context
                ),

            "signal":
                self._safe_copy(
                    self.current_signal_context
                ),

            "prediction":
                self._safe_copy(
                    self.current_prediction_context
                ),

            "decision":
                self._safe_copy(
                    self.current_decision_context
                ),

            "outcome":
                self._safe_copy(
                    self.current_outcome_context
                ),

            "learning":
                self._safe_copy(
                    self.current_learning_context
                ),

            "statistics":
                self.statistics(),

            "pipeline":
                self.pipeline_state(),

            "confidence":
                self.confidence_analysis(),

            "activity":
                self.activity_analysis(),

            "awareness":
                self._build_awareness()

        }

    # ========================================================
    #
    # AWARENESS
    #
    # ========================================================

    def _build_awareness(
        self
    ):

        return {

            "has_market":
                bool(
                    self.current_market_context
                ),

            "has_signal":
                bool(
                    self.current_signal_context
                ),

            "has_prediction":
                bool(
                    self.current_prediction_context
                ),

            "has_decision":
                bool(
                    self.current_decision_context
                ),

            "has_outcome":
                bool(
                    self.current_outcome_context
                ),

            "has_learning":
                bool(
                    self.current_learning_context
                ),

            "history_available":
                bool(
                    self.history
                ),

            "pipeline_complete":
                self.pipeline_state()[
                    "next_stage"
                ] == "complete"

        }

    # ========================================================
    #
    # STATISTICS
    #
    # ========================================================

    def statistics(
        self
    ):

        with self._lock:

            return {

                "total_events":
                    self.total_events,

                "retained_events":
                    len(self.history),

                "total_observations":
                    self.total_observations,

                "total_signals":
                    self.total_signals,

                "total_predictions":
                    self.total_predictions,

                "total_decisions":
                    self.total_decisions,

                "total_outcomes":
                    self.total_outcomes,

                "total_learning_events":
                    self.total_learning_events,

                "domains":
                    dict(
                        self.domain_counter
                    ),

                "event_types":
                    dict(
                        self.event_counter
                    ),

                "sources":
                    dict(
                        self.source_counter
                    ),

                "pairs":
                    dict(
                        self.pair_counter
                    ),

                "timeframes":
                    dict(
                        self.timeframe_counter
                    ),

                "tags":
                    dict(
                        self.tag_counter
                    )

            }

    # ========================================================
    #
    # DOMAIN STATISTICS
    #
    # ========================================================

    def domain_statistics(
        self,
        domain
    ):

        if not domain:
            return {}

        events = self.get_domain_context(
            domain,
            limit=self.max_size
        )

        event_types = Counter(

            event.get(
                "event_type"
            )

            for event in events

            if event.get(
                "event_type"
            )

        )

        pairs = Counter(

            event.get(
                "pair"
            )

            for event in events

            if event.get(
                "pair"
            )

        )

        return {

            "domain":
                domain,

            "events":
                len(events),

            "event_types":
                dict(event_types),

            "pairs":
                dict(pairs)

        }

    # ========================================================
    #
    # PAIR STATISTICS
    #
    # ========================================================

    def pair_statistics(
        self,
        pair
    ):

        if not pair:
            return {}

        events = self.get_pair_context(
            pair,
            limit=self.max_size
        )

        types = Counter(

            event.get(
                "event_type"
            )

            for event in events

            if event.get(
                "event_type"
            )

        )

        return {

            "pair":
                pair,

            "events":
                len(events),

            "event_types":
                dict(types)

        }

    # ========================================================
    #
    # BUILD SNAPSHOT
    #
    # ========================================================

    def snapshot(
        self,
        limit=20
    ):
        """
        Create a portable context snapshot.
        """

        return {

            "version":
                self.VERSION,

            "created_at":
                self.created_at,

            "snapshot_at":
                self._timestamp(),

            "context":
                self.build_context(
                    limit=limit
                )

        }

    # ========================================================
    #
    # EXPORT
    #
    # ========================================================

    def export_data(
        self,
        limit=None
    ):
        """
        Export context into a serializable dictionary.
        """

        with self._lock:

            if limit is None:

                events = list(
                    self.history
                )

            else:

                events = self.get_recent(
                    limit
                )

            return {

                "version":
                    self.VERSION,

                "max_size":
                    self.max_size,

                "created_at":
                    self.created_at,

                "updated_at":
                    self.updated_at,

                "total_events":
                    self.total_events,

                "sequence":
                    self.sequence,

                "events":
                    self._safe_copy(
                        events
                    ),

                "current_state":
                    self.current_state()

            }

    # ========================================================
    #
    # IMPORT
    #
    # ========================================================

    def import_data(
        self,
        data,
        replace=True
    ):
        """
        Import previously exported context.

        Returns number of imported events.
        """

        if not isinstance(
            data,
            dict
        ):

            return 0

        events = data.get(
            "events",
            []
        )

        if not isinstance(
            events,
            list
        ):

            return 0

        with self._lock:

            if replace:

                self.history.clear()

            imported = 0

            for event in events:

                if not isinstance(
                    event,
                    dict
                ):

                    continue

                self.history.append(
                    self._safe_copy(
                        event
                    )
                )

                imported += 1

            # ------------------------------------------------
            # RESTORE COUNTERS
            # ------------------------------------------------

            stored_total = data.get(
                "total_events"
            )

            if stored_total is not None:

                try:

                    self.total_events = int(
                        stored_total
                    )

                except Exception:

                    self.total_events = len(
                        self.history
                    )

            elif replace:

                self.total_events = len(
                    self.history
                )

            stored_sequence = data.get(
                "sequence"
            )

            if stored_sequence is not None:

                try:

                    self.sequence = int(
                        stored_sequence
                    )

                except Exception:

                    pass

            elif self.history:

                self.sequence = max(

                    int(
                        event.get(
                            "sequence",
                            0
                        )
                    )

                    for event in self.history

                    if isinstance(
                        event,
                        dict
                    )

                )

            # ------------------------------------------------
            # RESTORE CREATED TIME
            # ------------------------------------------------

            if data.get(
                "created_at"
            ):

                self.created_at = data[
                    "created_at"
                ]

            # ------------------------------------------------
            # REBUILD
            # ------------------------------------------------

            self._rebuild_indexes()

            self.updated_at = (
                self._timestamp()
            )

            self._sync_current_context()

            return imported

    # ========================================================
    #
    # REBUILD INDEXES
    #
    # ========================================================

    def _rebuild_indexes(
        self
    ):

        self.domain_counter.clear()

        self.event_counter.clear()

        self.source_counter.clear()

        self.pair_counter.clear()

        self.timeframe_counter.clear()

        self.tag_counter.clear()

        self.total_observations = 0

        self.total_signals = 0

        self.total_predictions = 0

        self.total_decisions = 0

        self.total_outcomes = 0

        self.total_learning_events = 0

        self.last_event = None

        self.last_observation = None

        self.last_signal = None

        self.last_prediction = None

        self.last_decision = None

        self.last_outcome = None

        self.last_learning_event = None

        self.current_market_context = {}

        self.current_signal_context = {}

        self.current_prediction_context = {}

        self.current_decision_context = {}

        self.current_outcome_context = {}

        self.current_learning_context = {}

        for event in self.history:

            if not isinstance(
                event,
                dict
            ):

                continue

            domain = event.get(
                "domain"
            )

            event_type = event.get(
                "event_type"
            )

            source = event.get(
                "source"
            )

            pair = event.get(
                "pair"
            )

            timeframe = event.get(
                "timeframe"
            )

            tags = event.get(
                "tags",
                []
            )

            if domain:

                self.domain_counter[
                    domain
                ] += 1

            if event_type:

                self.event_counter[
                    event_type
                ] += 1

            if source:

                self.source_counter[
                    source
                ] += 1

            if pair:

                self.pair_counter[
                    pair
                ] += 1

            if timeframe:

                self.timeframe_counter[
                    timeframe
                ] += 1

            for tag in tags:

                self.tag_counter[
                    str(tag)
                ] += 1

            self._categorize_event(
                event
            )

            self.last_event = event

        self._sync_current_context()

    # ========================================================
    #
    # SIZE
    #
    # ========================================================

    def size(
        self
    ):

        with self._lock:

            return len(
                self.history
            )

    # ========================================================
    #
    # TOTAL
    #
    # ========================================================

    def total(
        self
    ):

        return self.total_events

    # ========================================================
    #
    # HAS CONTEXT
    #
    # ========================================================

    def has_context(
        self
    ):

        with self._lock:

            return bool(
                self.history
            )

    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ):

        with self._lock:

            pipeline = self.pipeline_state()

            return {

                "module":
                    "context_manager",

                "version":
                    self.VERSION,

                "max_size":
                    self.max_size,

                "current_size":
                    len(
                        self.history
                    ),

                "total_events":
                    self.total_events,

                "sequence":
                    self.sequence,

                "observations":
                    self.total_observations,

                "signals":
                    self.total_signals,

                "predictions":
                    self.total_predictions,

                "decisions":
                    self.total_decisions,

                "outcomes":
                    self.total_outcomes,

                "learning_events":
                    self.total_learning_events,

                "domains":
                    len(
                        self.domain_counter
                    ),

                "pairs":
                    len(
                        self.pair_counter
                    ),

                "timeframes":
                    len(
                        self.timeframe_counter
                    ),

                "tags":
                    len(
                        self.tag_counter
                    ),

                "pipeline_completion":
                    pipeline[
                        "completion_percent"
                    ],

                "next_stage":
                    pipeline[
                        "next_stage"
                    ],

                "active":
                    self.activity_analysis()[
                        "active"
                    ],

                "has_context":
                    bool(
                        self.history
                    ),

                "created_at":
                    self.created_at,

                "updated_at":
                    self.updated_at

            }

    # ========================================================
    #
    # CLEAR
    #
    # ========================================================

    def clear(
        self
    ):
        """
        Clear active context while preserving lifetime
        total event count and sequence.
        """

        with self._lock:

            self.history.clear()

            self.current_context = {}

            self.current_market_context = {}

            self.current_signal_context = {}

            self.current_prediction_context = {}

            self.current_decision_context = {}

            self.current_outcome_context = {}

            self.current_learning_context = {}

            self.last_event = None

            self.last_observation = None

            self.last_signal = None

            self.last_prediction = None

            self.last_decision = None

            self.last_outcome = None

            self.last_learning_event = None

            self.domain_counter.clear()

            self.event_counter.clear()

            self.source_counter.clear()

            self.pair_counter.clear()

            self.timeframe_counter.clear()

            self.tag_counter.clear()

            self.total_observations = 0

            self.total_signals = 0

            self.total_predictions = 0

            self.total_decisions = 0

            self.total_outcomes = 0

            self.total_learning_events = 0

            self.updated_at = (
                self._timestamp()
            )

            return True

    # ========================================================
    #
    # RESET
    #
    # ========================================================

    def reset(
        self
    ):
        """
        Complete reset including lifetime counters.
        """

        with self._lock:

            self.clear()

            self.total_events = 0

            self.sequence = 0

            self.created_at = (
                self._timestamp()
            )

            self.updated_at = (
                self.created_at
            )

            return True


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

context_manager = ContextManager()


# ============================================================
#
# BACKWARD COMPATIBILITY
#
# ============================================================

Context = ContextManager

