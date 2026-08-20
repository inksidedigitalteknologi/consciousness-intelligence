
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# ENTITY RECOGNITION ENGINE
#
# Version: 2.0
#
# Comprehensive Entity Intelligence Layer
#
# Functions:
# - Entity Detection
# - Entity Classification
# - Entity Normalization
# - Entity Importance
# - Entity Confidence
# - Context Detection
# - Crypto / Market Entity Detection
# - Indicator Detection
# - Signal Detection
# - Pattern Detection
# - Timeframe Detection
# - Numeric Detection
# - Percentage Detection
# - Price Detection
# - URL / Email Detection
# - Entity Memory
# - Entity Frequency
# - Entity Search
# - Batch Recognition
# - Statistics
#
# Backward Compatible:
# - extract()
# - detect_numbers()
# - calculate_importance()
# - store()
# - search()
# - summary()
# - status()
# - entity_recognition
#
# ============================================================

import logging
import re
from collections import Counter, defaultdict
from datetime import datetime


logger = logging.getLogger(__name__)


# ============================================================
#
# ENTITY RECOGNITION ENGINE
#
# ============================================================

class EntityRecognition:

    VERSION = "2.0"

    MAX_MEMORY = 5000

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        self.name = "entity_recognition"

        self.entities = []

        self.entity_count = 0

        self.extraction_count = 0

        self.success_count = 0

        self.error_count = 0

        self.type_counter = Counter()

        self.name_counter = Counter()

        self.last_text = ""

        self.last_entities = []

        self.last_extraction = None

        # ====================================================
        # ENTITY DATABASE
        # ====================================================

        self.dictionary = {

            # ------------------------------------------------
            # CRYPTO
            # ------------------------------------------------

            "BTC": "CRYPTO",

            "BITCOIN": "CRYPTO",

            "ETH": "CRYPTO",

            "ETHEREUM": "CRYPTO",

            "SOL": "CRYPTO",

            "SOLANA": "CRYPTO",

            "XRP": "CRYPTO",

            "RIPPLE": "CRYPTO",

            "LTC": "CRYPTO",

            "LITECOIN": "CRYPTO",

            "DOGE": "CRYPTO",

            "DOGECOIN": "CRYPTO",

            "ADA": "CRYPTO",

            "CARDANO": "CRYPTO",

            "BNB": "CRYPTO",

            "DOT": "CRYPTO",

            "AVAX": "CRYPTO",

            "LINK": "CRYPTO",

            # ------------------------------------------------
            # EXCHANGES
            # ------------------------------------------------

            "KRAKEN": "EXCHANGE",

            "BINANCE": "EXCHANGE",

            "COINBASE": "EXCHANGE",

            "BYBIT": "EXCHANGE",

            "OKX": "EXCHANGE",

            "KUCOIN": "EXCHANGE",

            # ------------------------------------------------
            # ECONOMY
            # ------------------------------------------------

            "FED": "ORGANIZATION",

            "FEDERAL RESERVE": "ORGANIZATION",

            "ECB": "ORGANIZATION",

            "EUROPEAN CENTRAL BANK": "ORGANIZATION",

            "INFLATION": "ECONOMIC_FACTOR",

            "INTEREST RATE": "ECONOMIC_FACTOR",

            "GDP": "ECONOMIC_INDICATOR",

            "CPI": "ECONOMIC_INDICATOR",

            "PPI": "ECONOMIC_INDICATOR",

            "UNEMPLOYMENT": "ECONOMIC_FACTOR",

            "RECESSION": "ECONOMIC_FACTOR",

            "LIQUIDITY": "ECONOMIC_FACTOR",

            # ------------------------------------------------
            # TECHNOLOGY
            # ------------------------------------------------

            "AI": "TECHNOLOGY",

            "ARTIFICIAL INTELLIGENCE": "TECHNOLOGY",

            "MACHINE LEARNING": "TECHNOLOGY",

            "DEEP LEARNING": "TECHNOLOGY",

            "NEURAL NETWORK": "TECHNOLOGY",

            # ------------------------------------------------
            # TRADING CONCEPTS
            # ------------------------------------------------

            "BREAKOUT": "MARKET_PATTERN",

            "BREAKDOWN": "MARKET_PATTERN",

            "REVERSAL": "MARKET_PATTERN",

            "CONSOLIDATION": "MARKET_PATTERN",

            "TREND": "MARKET_CONCEPT",

            "MOMENTUM": "MARKET_CONCEPT",

            "VOLATILITY": "MARKET_CONCEPT",

            "SUPPORT": "PRICE_LEVEL",

            "RESISTANCE": "PRICE_LEVEL",

            "LIQUIDITY": "MARKET_CONCEPT",

            # ------------------------------------------------
            # SIGNALS
            # ------------------------------------------------

            "BUY": "SIGNAL",

            "SELL": "SIGNAL",

            "HOLD": "SIGNAL",

            "BULLISH": "SIGNAL",

            "BEARISH": "SIGNAL",

            "LONG": "SIGNAL",

            "SHORT": "SIGNAL",

            # ------------------------------------------------
            # TECHNICAL INDICATORS
            # ------------------------------------------------

            "RSI": "INDICATOR",

            "MACD": "INDICATOR",

            "SMA": "INDICATOR",

            "EMA": "INDICATOR",

            "ATR": "INDICATOR",

            "ADX": "INDICATOR",

            "CCI": "INDICATOR",

            "VWAP": "INDICATOR",

            "MFI": "INDICATOR",

            "OBV": "INDICATOR",

            "ROC": "INDICATOR",

            "STOCHASTIC": "INDICATOR",

            "STOCH RSI": "INDICATOR",

            "BOLLINGER BANDS": "INDICATOR",

            "ICHIMOKU": "INDICATOR",

            "SUPERTREND": "INDICATOR",

            "WILLIAMS %R": "INDICATOR",

            # ------------------------------------------------
            # CANDLE PATTERNS
            # ------------------------------------------------

            "DOJI": "CANDLE_PATTERN",

            "HAMMER": "CANDLE_PATTERN",

            "SHOOTING STAR": "CANDLE_PATTERN",

            "ENGULFING": "CANDLE_PATTERN",

            "BULLISH ENGULFING": "CANDLE_PATTERN",

            "BEARISH ENGULFING": "CANDLE_PATTERN",

            "MORNING STAR": "CANDLE_PATTERN",

            "EVENING STAR": "CANDLE_PATTERN",

            "HARAMI": "CANDLE_PATTERN",

            "SPINNING TOP": "CANDLE_PATTERN",

            "MARUBOZU": "CANDLE_PATTERN",

        }

        # ====================================================
        # TIMEFRAME MAP
        # ====================================================

        self.timeframe_patterns = {

            "1m": r"\b1m\b",

            "3m": r"\b3m\b",

            "5m": r"\b5m\b",

            "15m": r"\b15m\b",

            "30m": r"\b30m\b",

            "1h": r"\b1h\b",

            "4h": r"\b4h\b",

            "12h": r"\b12h\b",

            "1d": r"\b1d\b",

            "1w": r"\b1w\b",

            "1M": r"\b1M\b",

        }

        logger.info(
            "Entity Recognition Engine v%s initialized.",
            self.VERSION
        )

    # ========================================================
    # MAIN EXTRACTION
    # ========================================================

    def extract(self, text):

        self.extraction_count += 1

        self.last_text = str(
            text or ""
        )

        self.last_extraction = (
            datetime.now().isoformat()
        )

        try:

            if text is None:

                self.last_entities = []

                return []

            text_string = str(text)

            if not text_string.strip():

                self.last_entities = []

                return []

            text_upper = text_string.upper()

            found = []

            # ------------------------------------------------
            # Dictionary entities
            # ------------------------------------------------

            found.extend(
                self._detect_dictionary_entities(
                    text_string,
                    text_upper
                )
            )

            # ------------------------------------------------
            # Market pairs
            # ------------------------------------------------

            found.extend(
                self._detect_market_pairs(
                    text_string
                )
            )

            # ------------------------------------------------
            # Timeframes
            # ------------------------------------------------

            found.extend(
                self._detect_timeframes(
                    text_string
                )
            )

            # ------------------------------------------------
            # Numbers
            # ------------------------------------------------

            found.extend(
                self.detect_numbers(
                    text_string
                )
            )

            # ------------------------------------------------
            # Prices
            # ------------------------------------------------

            found.extend(
                self._detect_prices(
                    text_string
                )
            )

            # ------------------------------------------------
            # Percentages
            # ------------------------------------------------

            found.extend(
                self._detect_percentages(
                    text_string
                )
            )

            # ------------------------------------------------
            # Emails
            # ------------------------------------------------

            found.extend(
                self._detect_emails(
                    text_string
                )
            )

            # ------------------------------------------------
            # URLs
            # ------------------------------------------------

            found.extend(
                self._detect_urls(
                    text_string
                )
            )

            # ------------------------------------------------
            # Deduplicate
            # ------------------------------------------------

            found = self._deduplicate(
                found
            )

            # ------------------------------------------------
            # Context enrichment
            # ------------------------------------------------

            for entity in found:

                self._enrich_entity(
                    entity,
                    text_string
                )

            # ------------------------------------------------
            # Store
            # ------------------------------------------------

            for entity in found:

                self.store(
                    entity
                )

            self.last_entities = list(
                found
            )

            self.success_count += 1

            return found

        except Exception as e:

            self.error_count += 1

            logger.exception(
                "Entity extraction failed: %s",
                e
            )

            self.last_entities = []

            return []

    # ========================================================
    # DICTIONARY DETECTION
    # ========================================================

    def _detect_dictionary_entities(
        self,
        text,
        text_upper
    ):

        results = []

        # Longest first prevents partial matches
        names = sorted(
            self.dictionary.keys(),
            key=len,
            reverse=True
        )

        for name in names:

            pattern = (
                r"(?<![A-Z0-9])"
                + re.escape(name)
                + r"(?![A-Z0-9])"
            )

            if re.search(
                pattern,
                text_upper
            ):

                entity = self._create_entity(

                    name=name,

                    entity_type=self.dictionary[
                        name
                    ],

                    source="dictionary",

                    text=text_upper

                )

                results.append(
                    entity
                )

        return results

    # ========================================================
    # MARKET PAIR DETECTION
    # ========================================================

    def _detect_market_pairs(self, text):

        results = []

        patterns = [

            r"\b[A-Z]{2,10}/[A-Z]{2,6}\b",

            r"\b[A-Z]{2,10}-[A-Z]{2,6}\b",

        ]

        found_pairs = set()

        for pattern in patterns:

            for match in re.findall(
                pattern,
                text.upper()
            ):

                if match in found_pairs:
                    continue

                found_pairs.add(match)

                results.append({

                    "name": match,

                    "type": "MARKET_PAIR",

                    "importance": 0.8,

                    "confidence": 0.95,

                    "source": "market_pair",

                    "timestamp":
                        datetime.now().isoformat(),

                })

        return results

    # ========================================================
    # TIMEFRAME DETECTION
    # ========================================================

    def _detect_timeframes(self, text):

        results = []

        for timeframe, pattern in (
            self.timeframe_patterns.items()
        ):

            if re.search(
                pattern,
                text
            ):

                results.append({

                    "name": timeframe,

                    "type": "TIMEFRAME",

                    "importance": 0.65,

                    "confidence": 0.95,

                    "source": "timeframe",

                    "timestamp":
                        datetime.now().isoformat(),

                })

        return results

    # ========================================================
    # NUMBER DETECTION
    # ========================================================

    def detect_numbers(self, text):

        results = []

        pattern = (
            r"(?<![\w])"
            r"-?\d+(?:\.\d+)?"
            r"(?:[eE][+-]?\d+)?"
            r"%?"
        )

        for number in re.findall(
            pattern,
            str(text)
        ):

            entity_type = (
                "PERCENTAGE"
                if number.endswith("%")
                else "NUMERIC_VALUE"
            )

            results.append({

                "name": number,

                "type": entity_type,

                "importance":
                    0.5,

                "confidence":
                    0.98,

                "source": "numeric",

                "timestamp":
                    datetime.now().isoformat(),

            })

        return results

    # ========================================================
    # PRICE DETECTION
    # ========================================================

    def _detect_prices(self, text):

        results = []

        patterns = [

            r"(?:USD|USDT|\$)\s*\d+(?:,\d{3})*(?:\.\d+)?",

            r"\d+(?:,\d{3})*(?:\.\d+)?\s*(?:USD|USDT)",

        ]

        for pattern in patterns:

            for value in re.findall(
                pattern,
                str(text).upper()
            ):

                results.append({

                    "name": value,

                    "type": "PRICE",

                    "importance": 0.75,

                    "confidence": 0.98,

                    "source": "price",

                    "timestamp":
                        datetime.now().isoformat(),

                })

        return results

    # ========================================================
    # PERCENTAGE DETECTION
    # ========================================================

    def _detect_percentages(self, text):

        results = []

        for value in re.findall(
            r"-?\d+(?:\.\d+)?\s*%",
            str(text)
        ):

            results.append({

                "name":
                    value.strip(),

                "type":
                    "PERCENTAGE",

                "importance":
                    0.6,

                "confidence":
                    0.99,

                "source":
                    "percentage",

                "timestamp":
                    datetime.now().isoformat(),

            })

        return results

    # ========================================================
    # EMAIL DETECTION
    # ========================================================

    def _detect_emails(self, text):

        results = []

        pattern = (
            r"\b[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+\."
            r"[A-Za-z]{2,}\b"
        )

        for email in re.findall(
            pattern,
            str(text)
        ):

            results.append({

                "name": email,

                "type": "EMAIL",

                "importance": 0.5,

                "confidence": 0.99,

                "source": "email",

                "timestamp":
                    datetime.now().isoformat(),

            })

        return results

    # ========================================================
    # URL DETECTION
    # ========================================================

    def _detect_urls(self, text):

        results = []

        pattern = (
            r"\bhttps?://"
            r"[^\s]+"
        )

        for url in re.findall(
            pattern,
            str(text)
        ):

            results.append({

                "name": url,

                "type": "URL",

                "importance": 0.4,

                "confidence": 0.99,

                "source": "url",

                "timestamp":
                    datetime.now().isoformat(),

            })

        return results

    # ========================================================
    # ENTITY CREATION
    # ========================================================

    def _create_entity(
        self,
        name,
        entity_type,
        source,
        text
    ):

        importance = (
            self.calculate_importance(
                name,
                text
            )
        )

        return {

            "name": name,

            "type": entity_type,

            "importance": importance,

            "confidence": 0.95,

            "source": source,

            "timestamp":
                datetime.now().isoformat(),

        }

    # ========================================================
    # IMPORTANCE
    # ========================================================

    def calculate_importance(
        self,
        entity,
        text
    ):

        score = 0.5

        frequency = str(
            text
        ).count(
            str(entity).upper()
        )

        if frequency > 1:

            score += min(
                0.2,
                frequency * 0.05
            )

        # Important market entities
        if entity.upper() in {

            "BTC",
            "BITCOIN",
            "ETH",
            "ETHEREUM",

        }:

            score += 0.2

        # Important signals
        if entity.upper() in {

            "BUY",
            "SELL",
            "BULLISH",
            "BEARISH",

        }:

            score += 0.15

        # Indicators
        if entity.upper() in {

            "RSI",
            "MACD",
            "ATR",
            "ADX",

        }:

            score += 0.10

        return min(
            round(score, 2),
            1.0
        )

    # ========================================================
    # ENTITY ENRICHMENT
    # ========================================================

    def _enrich_entity(
        self,
        entity,
        text
    ):

        entity_name = str(
            entity.get(
                "name",
                ""
            )
        )

        context = self._get_context(
            entity_name,
            text
        )

        entity["context"] = context

        entity["frequency"] = (
            text.upper().count(
                entity_name.upper()
            )
        )

        entity["normalized"] = (
            entity_name.strip().upper()
        )

        # Adjust confidence based on source
        source = entity.get(
            "source"
        )

        if source == "dictionary":

            entity["confidence"] = max(
                entity.get(
                    "confidence",
                    0.8
                ),
                0.95
            )

        return entity

    # ========================================================
    # CONTEXT
    # ========================================================

    def _get_context(
        self,
        entity,
        text,
        window=50
    ):

        position = text.upper().find(
            str(entity).upper()
        )

        if position < 0:

            return ""

        start = max(
            0,
            position - window
        )

        end = min(
            len(text),
            position
            + len(entity)
            + window
        )

        return text[start:end].strip()

    # ========================================================
    # DEDUPLICATION
    # ========================================================

    def _deduplicate(
        self,
        entities
    ):

        unique = {}

        priority = {

            "MARKET_PAIR": 10,

            "PRICE": 9,

            "PERCENTAGE": 8,

            "INDICATOR": 7,

            "SIGNAL": 7,

            "CRYPTO": 7,

            "CANDLE_PATTERN": 6,

            "TIMEFRAME": 6,

            "ECONOMIC_FACTOR": 5,

            "TECHNOLOGY": 5,

            "NUMERIC_VALUE": 3,

        }

        for entity in entities:

            key = (

                str(
                    entity.get(
                        "name",
                        ""
                    )
                ).upper(),

                entity.get(
                    "type"
                )

            )

            if key not in unique:

                unique[key] = entity

                continue

            old = unique[key]

            old_priority = priority.get(
                old.get("type"),
                1
            )

            new_priority = priority.get(
                entity.get("type"),
                1
            )

            if new_priority > old_priority:

                unique[key] = entity

        return list(
            unique.values()
        )

    # ========================================================
    # STORE
    # ========================================================

    def store(self, entity):

        if not isinstance(
            entity,
            dict
        ):

            return False

        self.entities.append(
            dict(entity)
        )

        self.entity_count += 1

        entity_name = str(
            entity.get(
                "name",
                ""
            )
        ).upper()

        entity_type = entity.get(
            "type",
            "UNKNOWN"
        )

        self.name_counter[
            entity_name
        ] += 1

        self.type_counter[
            entity_type
        ] += 1

        # Memory protection
        if len(self.entities) > self.MAX_MEMORY:

            excess = (
                len(self.entities)
                - self.MAX_MEMORY
            )

            del self.entities[
                :excess
            ]

        return True

    # ========================================================
    # SEARCH
    # ========================================================

    def search(self, name):

        if not name:

            return []

        query = str(
            name
        ).lower()

        return [

            entity

            for entity in self.entities

            if query in str(
                entity.get(
                    "name",
                    ""
                )
            ).lower()

        ]

    # ========================================================
    # SEARCH BY TYPE
    # ========================================================

    def search_type(
        self,
        entity_type
    ):

        if not entity_type:

            return []

        entity_type = str(
            entity_type
        ).upper()

        return [

            entity

            for entity in self.entities

            if str(
                entity.get(
                    "type",
                    ""
                )
            ).upper()
            == entity_type

        ]

    # ========================================================
    # MOST COMMON ENTITIES
    # ========================================================

    def most_common(
        self,
        limit=10
    ):

        return self.name_counter.most_common(
            limit
        )

    # ========================================================
    # MOST COMMON TYPES
    # ========================================================

    def most_common_types(
        self,
        limit=10
    ):

        return self.type_counter.most_common(
            limit
        )

    # ========================================================
    # BATCH EXTRACTION
    # ========================================================

    def extract_many(
        self,
        texts
    ):

        if texts is None:

            return []

        results = []

        for text in texts:

            try:

                results.append(
                    self.extract(
                        text
                    )
                )

            except Exception:

                logger.exception(
                    "Batch entity extraction error."
                )

                results.append([])

        return results

    # ========================================================
    # CLEAR MEMORY
    # ========================================================

    def clear(self):

        self.entities.clear()

        self.entity_count = 0

        self.type_counter.clear()

        self.name_counter.clear()

        self.last_entities = []

        return True

    # ========================================================
    # ENTITY SUMMARY
    # ========================================================

    def summary(self):

        return {

            "total":
                self.entity_count,

            "stored":
                len(self.entities),

            "categories":
                dict(
                    self.type_counter
                ),

            "unique_entities":
                len(
                    self.name_counter
                ),

            "top_entities":
                self.most_common(
                    10
                ),

        }

    # ========================================================
    # LAST EXTRACTION
    # ========================================================

    def last(self):

        return list(
            self.last_entities
        )

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        return {

            "name":
                self.name,

            "version":
                self.VERSION,

            "online":
                True,

            "entities":
                self.entity_count,

            "stored":
                len(self.entities),

            "extractions":
                self.extraction_count,

            "success":
                self.success_count,

            "errors":
                self.error_count,

            "unique_entities":
                len(
                    self.name_counter
                ),

            "entity_types":
                len(
                    self.type_counter
                ),

            "last_extraction":
                self.last_extraction,

        }


# ============================================================
#
# BACKWARD COMPATIBILITY
#
# ============================================================

EntityRecognitionEngine = EntityRecognition


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

entity_recognition = EntityRecognition()

