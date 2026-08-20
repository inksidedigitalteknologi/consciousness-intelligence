# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SEMANTIC PROCESSOR ENGINE
#
# Version: 2.0
#
# PURPOSE:
# - Understand Meaning
# - Extract Concepts
# - Detect Sentiment
# - Detect Intent
# - Detect Topics
# - Extract Keywords
# - Detect Risk
# - Build Semantic Representation
# - Compare Semantic Context
# - Maintain Semantic Memory
#
# ============================================================

import logging
import re
from collections import Counter, deque
from datetime import datetime


logger = logging.getLogger(__name__)


class SemanticProcessor:

    # ========================================================
    # CONFIGURATION
    # ========================================================

    MAX_HISTORY = 1000

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self, max_history=None):

        self.name = "semantic_processor"

        self.max_history = (
            max_history
            if max_history is not None
            else self.MAX_HISTORY
        )

        self.processed_count = 0
        self.error_count = 0

        self.history = deque(
            maxlen=self.max_history
        )

        self.concept_frequency = Counter()
        self.topic_frequency = Counter()
        self.keyword_frequency = Counter()
        self.sentiment_frequency = Counter()
        self.intent_frequency = Counter()

        logger.info(
            "Semantic Processor v2.0 initialized."
        )

    # ========================================================
    # MAIN PROCESS
    # ========================================================

    def process(
        self,
        text,
        entities=None,
        context=None
    ):

        try:

            timestamp = datetime.now().isoformat()

            original_text = (
                ""
                if text is None
                else str(text)
            )

            normalized_text = (
                self.normalize_text(
                    original_text
                )
            )

            tokens = self.tokenize(
                normalized_text
            )

            concepts = self.extract_concepts(
                normalized_text
            )

            sentiment = self.detect_sentiment(
                normalized_text
            )

            intent = self.detect_intent(
                normalized_text
            )

            topics = self.detect_topics(
                normalized_text
            )

            keywords = self.extract_keywords(
                normalized_text
            )

            risk = self.detect_risk(
                normalized_text
            )

            temporal = self.detect_temporal_context(
                normalized_text
            )

            market = self.detect_market_semantics(
                normalized_text
            )

            text_stats = self.text_statistics(
                original_text,
                tokens
            )

            meaning = self.create_meaning(
                normalized_text,
                concepts=concepts,
                sentiment=sentiment,
                topics=topics,
                intent=intent,
            )

            confidence = self.calculate_confidence(
                concepts=concepts,
                topics=topics,
                sentiment=sentiment,
                intent=intent,
                keywords=keywords,
            )

            semantic_tags = (
                self.build_semantic_tags(
                    concepts=concepts,
                    topics=topics,
                    sentiment=sentiment,
                    intent=intent,
                    risk=risk,
                    market=market,
                )
            )

            result = {

                "timestamp":
                    timestamp,

                "original":
                    original_text,

                "normalized":
                    normalized_text,

                "entities":
                    entities or [],

                "tokens":
                    tokens,

                "concepts":
                    concepts,

                "keywords":
                    keywords,

                "topics":
                    topics,

                "sentiment":
                    sentiment,

                "intent":
                    intent,

                "risk":
                    risk,

                "temporal":
                    temporal,

                "market":
                    market,

                "meaning":
                    meaning,

                "semantic_tags":
                    semantic_tags,

                "confidence":
                    confidence,

                "statistics":
                    text_stats,

                "context":
                    context or {},

            }

            # ------------------------------------------------
            # MEMORY
            # ------------------------------------------------

            self.history.append(
                result
            )

            # ------------------------------------------------
            # FREQUENCY TRACKING
            # ------------------------------------------------

            self.concept_frequency.update(
                concepts
            )

            self.topic_frequency.update(
                topics
            )

            self.keyword_frequency.update(
                keywords
            )

            self.sentiment_frequency.update(
                [sentiment["label"]]
            )

            self.intent_frequency.update(
                [intent["label"]]
            )

            self.processed_count += 1

            return result

        except Exception as e:

            self.error_count += 1

            logger.exception(
                "Semantic processing failed: %s",
                e
            )

            return {
                "timestamp":
                    datetime.now().isoformat(),

                "original":
                    text,

                "error":
                    str(e),

                "error_type":
                    type(e).__name__,

                "semantic_tags":
                    [],

                "concepts":
                    [],

                "keywords":
                    [],

                "topics":
                    [],

            }

    # ========================================================
    # NORMALIZATION
    # ========================================================

    def normalize_text(self, text):

        text = str(text)

        text = text.strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.lower()

    # ========================================================
    # TOKENIZER
    # ========================================================

    def tokenize(self, text):

        if not text:

            return []

        return re.findall(
            r"[a-zA-Z0-9_%$./-]+",
            text
        )

    # ========================================================
    # CONCEPT EXTRACTION
    # ========================================================

    def extract_concepts(self, text):

        text = self.normalize_text(
            text
        )

        concepts = set()

        mapping = {

            # ----------------------------------------------
            # MARKET
            # ----------------------------------------------

            "naik":
                "bullish",

            "meningkat":
                "bullish",

            "menguat":
                "bullish",

            "bullish":
                "bullish",

            "turun":
                "bearish",

            "menurun":
                "bearish",

            "melemah":
                "bearish",

            "bearish":
                "bearish",

            "breakout":
                "breakout",

            "breakdown":
                "breakdown",

            "volume":
                "market_activity",

            "momentum":
                "momentum",

            "trend":
                "trend",

            "tren":
                "trend",

            "support":
                "support",

            "resistance":
                "resistance",

            "konsolidasi":
                "consolidation",

            "consolidation":
                "consolidation",

            "sideways":
                "consolidation",

            # ----------------------------------------------
            # RISK
            # ----------------------------------------------

            "risiko":
                "risk",

            "risk":
                "risk",

            "volatilitas":
                "volatility",

            "volatile":
                "volatility",

            "drawdown":
                "drawdown",

            "kerugian":
                "loss",

            "rugi":
                "loss",

            # ----------------------------------------------
            # ECONOMY
            # ----------------------------------------------

            "inflasi":
                "inflation",

            "inflation":
                "inflation",

            "suku bunga":
                "interest_rate",

            "interest rate":
                "interest_rate",

            "fed":
                "central_bank",

            "federal reserve":
                "central_bank",

            "ekonomi":
                "economy",

            "economy":
                "economy",

            # ----------------------------------------------
            # FINANCE
            # ----------------------------------------------

            "profit":
                "profit",

            "keuntungan":
                "profit",

            "loss":
                "loss",

            "trading":
                "trading",

            "investasi":
                "investment",

            "investment":
                "investment",

            # ----------------------------------------------
            # TECHNOLOGY
            # ----------------------------------------------

            "ai":
                "artificial_intelligence",

            "artificial intelligence":
                "artificial_intelligence",

            "machine learning":
                "machine_learning",

            "neural network":
                "neural_network",

        }

        for phrase, concept in mapping.items():

            if phrase in text:

                concepts.add(
                    concept
                )

        return sorted(
            concepts
        )

    # ========================================================
    # SENTIMENT ANALYSIS
    # ========================================================

    def detect_sentiment(self, text):

        text = self.normalize_text(
            text
        )

        positive_words = [

            "naik",
            "meningkat",
            "menguat",
            "bullish",
            "profit",
            "untung",
            "keuntungan",
            "kuat",
            "breakout",
            "positif",
            "bagus",
            "baik",
            "sukses",
            "success",
            "strong",

        ]

        negative_words = [

            "turun",
            "menurun",
            "melemah",
            "bearish",
            "rugi",
            "kerugian",
            "jatuh",
            "tekanan",
            "negatif",
            "buruk",
            "lemah",
            "loss",
            "failure",
            "weak",

        ]

        positive_hits = 0
        negative_hits = 0

        for word in positive_words:

            positive_hits += (
                text.count(word)
            )

        for word in negative_words:

            negative_hits += (
                text.count(word)
            )

        raw_score = (
            positive_hits
            -
            negative_hits
        )

        total_hits = (
            positive_hits
            +
            negative_hits
        )

        if raw_score > 0:

            label = "positive"

        elif raw_score < 0:

            label = "negative"

        else:

            label = "neutral"

        if total_hits:

            score = round(
                raw_score / total_hits,
                2
            )

        else:

            score = 0.0

        confidence = round(
            min(
                1.0,
                total_hits / 5
            ),
            2
        )

        return {

            "label":
                label,

            "score":
                score,

            "confidence":
                confidence,

            "positive_hits":
                positive_hits,

            "negative_hits":
                negative_hits,

        }

    # ========================================================
    # INTENT DETECTION
    # ========================================================

    def detect_intent(self, text):

        text = self.normalize_text(
            text
        )

        intent_rules = {

            "question": [
                "apa",
                "apakah",
                "mengapa",
                "kenapa",
                "bagaimana",
                "what",
                "why",
                "how",
                "?",
            ],

            "prediction": [
                "prediksi",
                "prediction",
                "akan naik",
                "akan turun",
                "forecast",
                "forecasting",
                "kemungkinan",
            ],

            "analysis": [
                "analisis",
                "analysis",
                "evaluate",
                "evaluasi",
                "periksa",
                "check",
                "review",
            ],

            "decision": [
                "beli",
                "buy",
                "jual",
                "sell",
                "hold",
                "keputusan",
                "decision",
            ],

            "learning": [
                "belajar",
                "learning",
                "pelajari",
                "learn",
                "lesson",
            ],

            "information": [
                "informasi",
                "information",
                "jelaskan",
                "explain",
                "detail",
            ],

            "command": [
                "jalankan",
                "run",
                "mulai",
                "start",
                "stop",
                "hapus",
                "delete",
            ],

        }

        scores = {}

        for intent, words in intent_rules.items():

            score = 0

            for word in words:

                if word in text:

                    score += 1

            scores[intent] = score

        best_intent = max(
            scores,
            key=scores.get
        )

        best_score = scores[
            best_intent
        ]

        if best_score == 0:

            best_intent = "statement"

        confidence = round(
            min(
                1.0,
                best_score / 3
            ),
            2
        )

        return {

            "label":
                best_intent,

            "confidence":
                confidence,

            "scores":
                scores,

        }

    # ========================================================
    # TOPIC DETECTION
    # ========================================================

    def detect_topics(self, text):

        text = self.normalize_text(
            text
        )

        topic_rules = {

            "trading": [
                "trading",
                "buy",
                "sell",
                "hold",
                "entry",
                "stop loss",
                "take profit",
            ],

            "crypto": [
                "btc",
                "bitcoin",
                "eth",
                "ethereum",
                "crypto",
                "kripto",
            ],

            "finance": [
                "profit",
                "loss",
                "investment",
                "investasi",
                "portfolio",
                "asset",
            ],

            "economics": [
                "inflasi",
                "inflation",
                "fed",
                "interest rate",
                "suku bunga",
                "economy",
                "ekonomi",
            ],

            "technology": [
                "ai",
                "artificial intelligence",
                "machine learning",
                "software",
                "technology",
                "teknologi",
            ],

            "science": [
                "science",
                "earth",
                "planet",
                "physics",
                "biology",
                "chemistry",
            ],

            "general_knowledge": [
                "capital",
                "negara",
                "country",
                "kota",
                "sejarah",
                "history",
                "knowledge",
            ],

        }

        topics = []

        for topic, words in topic_rules.items():

            for word in words:

                if word in text:

                    topics.append(
                        topic
                    )

                    break

        return sorted(
            set(topics)
        )

    # ========================================================
    # KEYWORD EXTRACTION
    # ========================================================

    def extract_keywords(
        self,
        text,
        limit=15
    ):

        tokens = self.tokenize(
            text
        )

        stopwords = {

            "yang",
            "dan",
            "atau",
            "dengan",
            "untuk",
            "dari",
            "ini",
            "itu",
            "adalah",
            "akan",
            "the",
            "and",
            "or",
            "with",
            "for",
            "from",
            "this",
            "that",
            "is",
            "are",

        }

        filtered = []

        for token in tokens:

            clean = token.lower()

            if len(clean) < 3:

                continue

            if clean in stopwords:

                continue

            filtered.append(
                clean
            )

        frequency = Counter(
            filtered
        )

        return [
            word
            for word, count
            in frequency.most_common(
                limit
            )
        ]

    # ========================================================
    # RISK DETECTION
    # ========================================================

    def detect_risk(self, text):

        text = self.normalize_text(
            text
        )

        high_risk = [

            "crash",
            "collapse",
            "market crash",
            "extreme volatility",
            "likuidasi",
            "liquidation",
            "panic",
            "krisis",
            "crisis",

        ]

        medium_risk = [

            "risk",
            "risiko",
            "volatile",
            "volatilitas",
            "drawdown",
            "uncertainty",
            "ketidakpastian",

        ]

        high_hits = sum(
            text.count(word)
            for word in high_risk
        )

        medium_hits = sum(
            text.count(word)
            for word in medium_risk
        )

        if high_hits:

            level = "high"

        elif medium_hits:

            level = "medium"

        else:

            level = "low"

        return {

            "level":
                level,

            "high_hits":
                high_hits,

            "medium_hits":
                medium_hits,

            "risk_detected":
                bool(
                    high_hits
                    or
                    medium_hits
                ),

        }

    # ========================================================
    # TEMPORAL CONTEXT
    # ========================================================

    def detect_temporal_context(self, text):

        text = self.normalize_text(
            text
        )

        temporal_map = {

            "past": [
                "kemarin",
                "dulu",
                "sebelumnya",
                "yesterday",
                "previous",
                "historical",
            ],

            "present": [
                "sekarang",
                "saat ini",
                "today",
                "now",
                "current",
            ],

            "future": [
                "besok",
                "nanti",
                "akan",
                "tomorrow",
                "future",
                "forecast",
            ],

        }

        detected = []

        for period, words in temporal_map.items():

            for word in words:

                if word in text:

                    detected.append(
                        period
                    )

                    break

        if not detected:

            detected.append(
                "unspecified"
            )

        return sorted(
            set(detected)
        )

    # ========================================================
    # MARKET SEMANTICS
    # ========================================================

    def detect_market_semantics(self, text):

        text = self.normalize_text(
            text
        )

        direction = "neutral"

        if any(
            word in text
            for word in [
                "bullish",
                "naik",
                "menguat",
                "breakout",
            ]
        ):

            direction = "bullish"

        elif any(
            word in text
            for word in [
                "bearish",
                "turun",
                "melemah",
                "breakdown",
            ]
        ):

            direction = "bearish"

        volatility = "normal"

        if any(
            word in text
            for word in [
                "volatile",
                "volatilitas",
                "extreme volatility",
            ]
        ):

            volatility = "high"

        elif any(
            word in text
            for word in [
                "low volatility",
                "tenang",
                "calm",
            ]
        ):

            volatility = "low"

        structure = []

        if "breakout" in text:

            structure.append(
                "breakout"
            )

        if "breakdown" in text:

            structure.append(
                "breakdown"
            )

        if (
            "support" in text
        ):

            structure.append(
                "support"
            )

        if (
            "resistance" in text
        ):

            structure.append(
                "resistance"
            )

        if not structure:

            structure.append(
                "undefined"
            )

        return {

            "direction":
                direction,

            "volatility":
                volatility,

            "structure":
                structure,

        }

    # ========================================================
    # TEXT STATISTICS
    # ========================================================

    def text_statistics(
        self,
        original,
        tokens
    ):

        text = str(
            original
        )

        words = len(
            tokens
        )

        characters = len(
            text
        )

        sentences = len(
            re.findall(
                r"[.!?]+",
                text
            )
        )

        if sentences == 0 and words:

            sentences = 1

        return {

            "characters":
                characters,

            "words":
                words,

            "sentences":
                sentences,

            "unique_words":
                len(
                    set(tokens)
                ),

        }

    # ========================================================
    # MEANING CREATION
    # ========================================================

    def create_meaning(
        self,
        text,
        concepts=None,
        sentiment=None,
        topics=None,
        intent=None,
    ):

        concepts = concepts or []

        topics = topics or []

        sentiment = (
            sentiment
            or
            self.detect_sentiment(text)
        )

        intent = (
            intent
            or
            self.detect_intent(text)
        )

        if concepts:

            concept_text = (
                ", ".join(
                    concepts
                )
            )

        else:

            concept_text = (
                "no specific concepts"
            )

        return {

            "summary":
                (
                    "Detected "
                    +
                    sentiment["label"]
                    +
                    " semantic condition"
                ),

            "concepts":
                concepts,

            "topics":
                topics,

            "sentiment":
                sentiment["label"],

            "intent":
                intent["label"],

            "concept_summary":
                concept_text,

        }

    # ========================================================
    # CONFIDENCE
    # ========================================================

    def calculate_confidence(
        self,
        concepts,
        topics,
        sentiment,
        intent,
        keywords,
    ):

        score = 0.0

        if concepts:

            score += 0.20

        if topics:

            score += 0.20

        if keywords:

            score += 0.20

        score += (
            sentiment.get(
                "confidence",
                0
            )
            * 0.20
        )

        score += (
            intent.get(
                "confidence",
                0
            )
            * 0.20
        )

        return round(
            min(
                1.0,
                score
            ),
            2
        )

    # ========================================================
    # SEMANTIC TAGS
    # ========================================================

    def build_semantic_tags(
        self,
        concepts=None,
        topics=None,
        sentiment=None,
        intent=None,
        risk=None,
        market=None,
    ):

        tags = set()

        for item in concepts or []:

            tags.add(item)

        for item in topics or []:

            tags.add(
                "topic:" + item
            )

        if sentiment:

            tags.add(
                "sentiment:"
                +
                sentiment["label"]
            )

        if intent:

            tags.add(
                "intent:"
                +
                intent["label"]
            )

        if risk:

            tags.add(
                "risk:"
                +
                risk["level"]
            )

        if market:

            tags.add(
                "market:"
                +
                market["direction"]
            )

            tags.add(
                "volatility:"
                +
                market["volatility"]
            )

        return sorted(
            tags
        )

    # ========================================================
    # SEMANTIC COMPARISON
    # ========================================================

    def compare(
        self,
        first,
        second
    ):

        if not isinstance(
            first,
            dict
        ):

            return 0.0

        if not isinstance(
            second,
            dict
        ):

            return 0.0

        first_items = set(
            first.get(
                "concepts",
                []
            )
        )

        second_items = set(
            second.get(
                "concepts",
                []
            )
        )

        first_topics = set(
            first.get(
                "topics",
                []
            )
        )

        second_topics = set(
            second.get(
                "topics",
                []
            )
        )

        first_keywords = set(
            first.get(
                "keywords",
                []
            )
        )

        second_keywords = set(
            second.get(
                "keywords",
                []
            )
        )

        scores = []

        # ------------------------------------------------
        # CONCEPT SIMILARITY
        # ------------------------------------------------

        if (
            first_items
            or
            second_items
        ):

            union = (
                first_items
                |
                second_items
            )

            common = (
                first_items
                &
                second_items
            )

            if union:

                scores.append(
                    len(common)
                    /
                    len(union)
                )

        # ------------------------------------------------
        # TOPIC SIMILARITY
        # ------------------------------------------------

        if (
            first_topics
            or
            second_topics
        ):

            union = (
                first_topics
                |
                second_topics
            )

            common = (
                first_topics
                &
                second_topics
            )

            if union:

                scores.append(
                    len(common)
                    /
                    len(union)
                )

        # ------------------------------------------------
        # KEYWORD SIMILARITY
        # ------------------------------------------------

        if (
            first_keywords
            or
            second_keywords
        ):

            union = (
                first_keywords
                |
                second_keywords
            )

            common = (
                first_keywords
                &
                second_keywords
            )

            if union:

                scores.append(
                    len(common)
                    /
                    len(union)
                )

        # ------------------------------------------------
        # SENTIMENT
        # ------------------------------------------------

        first_sentiment = (
            first.get(
                "sentiment",
                {}
            )
            .get(
                "label"
            )
        )

        second_sentiment = (
            second.get(
                "sentiment",
                {}
            )
            .get(
                "label"
            )
        )

        if (
            first_sentiment
            and
            second_sentiment
        ):

            scores.append(
                1.0
                if
                first_sentiment
                ==
                second_sentiment
                else
                0.0
            )

        if not scores:

            return 0.0

        return round(
            sum(scores)
            /
            len(scores),
            2
        )

    # ========================================================
    # SEARCH SEMANTIC MEMORY
    # ========================================================

    def search(
        self,
        query,
        limit=10
    ):

        query = self.normalize_text(
            query
        )

        query_tokens = set(
            self.tokenize(
                query
            )
        )

        results = []

        for item in reversed(
            self.history
        ):

            item_text = (
                item.get(
                    "normalized",
                    ""
                )
            )

            item_tokens = set(
                self.tokenize(
                    item_text
                )
            )

            if (
                query_tokens
                &
                item_tokens
            ):

                results.append(
                    item
                )

            if len(results) >= limit:

                break

        return results

    # ========================================================
    # GET RECENT
    # ========================================================

    def get_recent(
        self,
        limit=10
    ):

        if limit <= 0:

            return []

        return list(
            self.history
        )[-limit:]

    # ========================================================
    # TOP CONCEPTS
    # ========================================================

    def top_concepts(
        self,
        limit=10
    ):

        return (
            self.concept_frequency
            .most_common(limit)
        )

    # ========================================================
    # TOP TOPICS
    # ========================================================

    def top_topics(
        self,
        limit=10
    ):

        return (
            self.topic_frequency
            .most_common(limit)
        )

    # ========================================================
    # TOP KEYWORDS
    # ========================================================

    def top_keywords(
        self,
        limit=10
    ):

        return (
            self.keyword_frequency
            .most_common(limit)
        )

    # ========================================================
    # CLEAR MEMORY
    # ========================================================

    def clear(self):

        self.history.clear()

        self.concept_frequency.clear()

        self.topic_frequency.clear()

        self.keyword_frequency.clear()

        self.sentiment_frequency.clear()

        self.intent_frequency.clear()

        logger.info(
            "Semantic memory cleared."
        )

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        return {

            "name":
                self.name,

            "version":
                "2.0",

            "online":
                True,

            "processed":
                self.processed_count,

            "errors":
                self.error_count,

            "memory":
                len(
                    self.history
                ),

            "memory_limit":
                self.max_history,

            "concepts_tracked":
                len(
                    self.concept_frequency
                ),

            "topics_tracked":
                len(
                    self.topic_frequency
                ),

            "keywords_tracked":
                len(
                    self.keyword_frequency
                ),

            "sentiments_tracked":
                len(
                    self.sentiment_frequency
                ),

            "intents_tracked":
                len(
                    self.intent_frequency
                ),

        }


# ============================================================
#
# BACKWARD COMPATIBILITY
#
# ============================================================

SemanticEngine = SemanticProcessor


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

semantic_processor = SemanticProcessor()