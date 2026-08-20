
# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# ARCHIVE MANAGER ENGINE
#
# Version: 2.0
#
# PURPOSE:
# Universal long-term archive/storage layer for the
# Inkside Intelligence OS.
#
# This module is DOMAIN-AGNOSTIC.
#
# It can store:
#   - trading observations
#   - knowledge
#   - reasoning results
#   - experiences
#   - insights
#   - evaluator results
#   - adaptive learning events
#   - pattern discoveries
#   - analyzer results
#   - feedback
#   - decisions
#   - system events
#   - future intelligence modules
#
# ============================================================

import json
import logging
import shutil
import threading
import uuid

from pathlib import Path
from datetime import datetime, timezone


logger = logging.getLogger(__name__)


# ============================================================
#
# CONSTANTS
#
# ============================================================

ARCHIVE_VERSION = "2.0"

DEFAULT_PATH = "database/archive.json"

DEFAULT_MAX_RECORDS = 10000

DEFAULT_BACKUP_COUNT = 3


# ============================================================
#
# ARCHIVE MANAGER
#
# ============================================================

class ArchiveManager:

    def __init__(
        self,
        path=DEFAULT_PATH,
        max_records=DEFAULT_MAX_RECORDS,
        backup_count=DEFAULT_BACKUP_COUNT
    ):

        self.path = Path(path)

        self.max_records = max(
            int(max_records),
            100
        )

        self.backup_count = max(
            int(backup_count),
            1
        )

        self.lock = threading.RLock()

        self.write_count = 0
        self.read_count = 0
        self.error_count = 0
        self.archive_count = 0
        self.delete_count = 0
        self.search_count = 0
        self.recovery_count = 0
        self.duplicate_count = 0

        self.initialized_at = self._now()

        self._prepare_storage()

        logger.info(
            "Archive Manager initialized. "
            "Path=%s MaxRecords=%s",
            self.path,
            self.max_records
        )


    # ========================================================
    #
    # TIME
    #
    # ========================================================

    @staticmethod
    def _now():

        return datetime.now(
            timezone.utc
        ).isoformat()


    # ========================================================
    #
    # STORAGE INITIALIZATION
    #
    # ========================================================

    def _prepare_storage(self):

        try:

            self.path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            if not self.path.exists():

                self._atomic_write(
                    []
                )

            else:

                # Validate existing archive.
                records = self.load()

                if not isinstance(
                    records,
                    list
                ):

                    logger.warning(
                        "Archive format invalid. "
                        "Creating new archive."
                    )

                    self._atomic_write(
                        []
                    )

        except Exception as e:

            self.error_count += 1

            logger.exception(
                "Archive initialization failed: %s",
                e
            )


    # ========================================================
    #
    # ATOMIC WRITE
    #
    # ========================================================

    def _atomic_write(
        self,
        records
    ):

        temp_path = self.path.with_suffix(
            self.path.suffix + ".tmp"
        )

        payload = json.dumps(
            records,
            indent=4,
            ensure_ascii=False,
            default=str
        )

        temp_path.write_text(
            payload,
            encoding="utf-8"
        )

        temp_path.replace(
            self.path
        )


    # ========================================================
    #
    # BACKUP
    #
    # ========================================================

    def _create_backup(self):

        try:

            if not self.path.exists():
                return False

            timestamp = datetime.now(
                timezone.utc
            ).strftime(
                "%Y%m%d_%H%M%S"
            )

            backup = self.path.with_name(
                f"{self.path.stem}_{timestamp}.bak"
            )

            shutil.copy2(
                self.path,
                backup
            )

            self._cleanup_backups()

            return True

        except Exception as e:

            logger.warning(
                "Archive backup failed: %s",
                e
            )

            return False


    # ========================================================
    #
    # CLEAN OLD BACKUPS
    #
    # ========================================================

    def _cleanup_backups(self):

        try:

            backups = sorted(
                self.path.parent.glob(
                    f"{self.path.stem}_*.bak"
                ),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            for old_backup in backups[
                self.backup_count:
            ]:

                try:

                    old_backup.unlink()

                except Exception:

                    pass

        except Exception as e:

            logger.debug(
                "Backup cleanup failed: %s",
                e
            )


    # ========================================================
    #
    # NORMALIZE RECORD
    #
    # ========================================================

    def _normalize_record(
        self,
        data,
        record_type="observation",
        domain="general",
        category="general",
        source="unknown",
        confidence=0.0,
        importance=0.0,
        tags=None,
        metadata=None,
        record_id=None
    ):

        if tags is None:
            tags = []

        if metadata is None:
            metadata = {}

        if not isinstance(
            tags,
            list
        ):

            tags = [
                str(tags)
            ]

        if not isinstance(
            metadata,
            dict
        ):

            metadata = {
                "value": metadata
            }

        record = {

            "id":
                record_id
                or uuid.uuid4().hex[:20],

            "time":
                self._now(),

            "archive_version":
                ARCHIVE_VERSION,

            "type":
                str(record_type),

            "domain":
                str(domain),

            "category":
                str(category),

            "source":
                str(source),

            "confidence":
                self._safe_float(
                    confidence
                ),

            "importance":
                self._safe_float(
                    importance
                ),

            "tags":
                list(
                    dict.fromkeys(
                        str(tag)
                        for tag in tags
                    )
                ),

            "data":
                data,

            "metadata":
                metadata

        }

        return record


    # ========================================================
    #
    # SAFE FLOAT
    #
    # ========================================================

    @staticmethod
    def _safe_float(
        value
    ):

        try:

            return float(
                value
            )

        except Exception:

            return 0.0


    # ========================================================
    #
    # DUPLICATE DETECTION
    #
    # ========================================================

    @staticmethod
    def _fingerprint(
        data
    ):

        try:

            payload = json.dumps(
                data,
                sort_keys=True,
                ensure_ascii=False,
                default=str
            )

            return payload

        except Exception:

            return str(data)


    def _is_duplicate(
        self,
        records,
        record
    ):

        fingerprint = self._fingerprint(
            record.get(
                "data"
            )
        )

        for existing in records:

            if self._fingerprint(
                existing.get(
                    "data"
                )
            ) == fingerprint:

                if (
                    existing.get("domain")
                    == record.get("domain")
                    and
                    existing.get("type")
                    == record.get("type")
                ):

                    return True

        return False


    # ========================================================
    #
    # ARCHIVE
    #
    # ========================================================

    def archive(
        self,
        data,
        record_type="observation",
        domain="general",
        category="general",
        source="unknown",
        confidence=0.0,
        importance=0.0,
        tags=None,
        metadata=None,
        record_id=None,
        allow_duplicate=False
    ):

        with self.lock:

            try:

                records = self.load()

                record = self._normalize_record(
                    data=data,
                    record_type=record_type,
                    domain=domain,
                    category=category,
                    source=source,
                    confidence=confidence,
                    importance=importance,
                    tags=tags,
                    metadata=metadata,
                    record_id=record_id
                )

                if not allow_duplicate:

                    if self._is_duplicate(
                        records,
                        record
                    ):

                        self.duplicate_count += 1

                        logger.debug(
                            "Duplicate archive ignored."
                        )

                        return None


                records.append(
                    record
                )

                # Enforce maximum archive size.
                if len(records) > self.max_records:

                    overflow = (
                        len(records)
                        - self.max_records
                    )

                    records = records[
                        overflow:
                    ]


                self._create_backup()

                self._atomic_write(
                    records
                )

                self.write_count += 1
                self.archive_count += 1

                return record

            except Exception as e:

                self.error_count += 1

                logger.exception(
                    "Archive failed: %s",
                    e
                )

                return None


    # ========================================================
    #
    # SHORTCUT METHODS
    #
    # ========================================================

    def observation(
        self,
        data,
        domain="general",
        source="unknown",
        confidence=0.0,
        importance=0.0,
        tags=None,
        metadata=None
    ):

        return self.archive(
            data=data,
            record_type="observation",
            domain=domain,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata
        )


    def knowledge(
        self,
        data,
        domain="general_knowledge",
        category="general",
        source="unknown",
        confidence=0.0,
        importance=0.0,
        tags=None,
        metadata=None
    ):

        return self.archive(
            data=data,
            record_type="knowledge",
            domain=domain,
            category=category,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata
        )


    def experience(
        self,
        data,
        domain="general",
        source="system",
        confidence=0.0,
        importance=0.0,
        tags=None,
        metadata=None
    ):

        return self.archive(
            data=data,
            record_type="experience",
            domain=domain,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata
        )


    def insight(
        self,
        data,
        domain="general",
        source="system",
        confidence=0.0,
        importance=0.0,
        tags=None,
        metadata=None
    ):

        return self.archive(
            data=data,
            record_type="insight",
            domain=domain,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata
        )


    def feedback(
        self,
        data,
        domain="general",
        source="unknown",
        confidence=0.0,
        importance=0.0,
        tags=None,
        metadata=None
    ):

        return self.archive(
            data=data,
            record_type="feedback",
            domain=domain,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata
        )


    def decision(
        self,
        data,
        domain="general",
        source="system",
        confidence=0.0,
        importance=0.0,
        tags=None,
        metadata=None
    ):

        return self.archive(
            data=data,
            record_type="decision",
            domain=domain,
            source=source,
            confidence=confidence,
            importance=importance,
            tags=tags,
            metadata=metadata
        )


    # ========================================================
    #
    # LOAD
    #
    # ========================================================

    def load(
        self
    ):

        with self.lock:

            self.read_count += 1

            try:

                if not self.path.exists():

                    return []

                raw = self.path.read_text(
                    encoding="utf-8"
                )

                if not raw.strip():

                    return []

                records = json.loads(
                    raw
                )

                if not isinstance(
                    records,
                    list
                ):

                    raise ValueError(
                        "Archive root must be a list."
                    )

                return records

            except Exception as e:

                self.error_count += 1

                logger.error(
                    "Archive load failed: %s",
                    e
                )

                return self._recover_archive()


    # ========================================================
    #
    # RECOVERY
    #
    # ========================================================

    def _recover_archive(
        self
    ):

        self.recovery_count += 1

        try:

            backups = sorted(
                self.path.parent.glob(
                    f"{self.path.stem}_*.bak"
                ),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            for backup in backups:

                try:

                    records = json.loads(
                        backup.read_text(
                            encoding="utf-8"
                        )
                    )

                    if isinstance(
                        records,
                        list
                    ):

                        logger.warning(
                            "Archive recovered from backup: %s",
                            backup
                        )

                        return records

                except Exception:

                    continue

        except Exception as e:

            logger.error(
                "Archive recovery failed: %s",
                e
            )

        return []


    # ========================================================
    #
    # GET BY ID
    #
    # ========================================================

    def get(
        self,
        record_id
    ):

        for record in self.load():

            if record.get(
                "id"
            ) == record_id:

                return record

        return None


    # ========================================================
    #
    # SEARCH
    #
    # ========================================================

    def search(
        self,
        keyword=None,
        domain=None,
        record_type=None,
        category=None,
        source=None,
        tags=None,
        limit=None
    ):

        self.search_count += 1

        records = self.load()

        if tags is None:

            tags = []

        if isinstance(
            tags,
            str
        ):

            tags = [
                tags
            ]

        keyword_lower = (
            str(keyword).lower()
            if keyword is not None
            else None
        )

        results = []

        for record in records:

            if domain is not None:

                if record.get(
                    "domain"
                ) != domain:

                    continue


            if record_type is not None:

                if record.get(
                    "type"
                ) != record_type:

                    continue


            if category is not None:

                if record.get(
                    "category"
                ) != category:

                    continue


            if source is not None:

                if record.get(
                    "source"
                ) != source:

                    continue


            if tags:

                record_tags = set(
                    str(tag).lower()
                    for tag in record.get(
                        "tags",
                        []
                    )
                )

                required_tags = set(
                    str(tag).lower()
                    for tag in tags
                )

                if not required_tags.issubset(
                    record_tags
                ):

                    continue


            if keyword_lower is not None:

                searchable = (
                    str(record)
                    .lower()
                )

                if keyword_lower not in searchable:

                    continue


            results.append(
                record
            )

        if limit is not None:

            try:

                limit = int(
                    limit
                )

                if limit >= 0:

                    results = results[
                        -limit:
                    ]

            except Exception:

                pass

        return results


    # ========================================================
    #
    # LATEST
    #
    # ========================================================

    def latest(
        self,
        limit=10,
        domain=None,
        record_type=None
    ):

        results = self.search(
            domain=domain,
            record_type=record_type
        )

        return results[
            -int(limit):
        ]


    # ========================================================
    #
    # DELETE BY ID
    #
    # ========================================================

    def delete(
        self,
        record_id
    ):

        with self.lock:

            records = self.load()

            original_count = len(
                records
            )

            records = [
                record
                for record in records
                if record.get(
                    "id"
                ) != record_id
            ]

            if len(records) == original_count:

                return False

            self._create_backup()

            self._atomic_write(
                records
            )

            self.delete_count += 1

            return True


    # ========================================================
    #
    # DELETE OLDEST
    #
    # ========================================================

    def delete_oldest(
        self,
        count=1
    ):

        with self.lock:

            records = self.load()

            count = max(
                int(count),
                0
            )

            if count == 0:

                return 0

            removed = min(
                count,
                len(records)
            )

            remaining = records[
                removed:
            ]

            if removed:

                self._create_backup()

                self._atomic_write(
                    remaining
                )

                self.delete_count += removed

            return removed


    # ========================================================
    #
    # CLEAR
    #
    # ========================================================

    def clear(
        self
    ):

        with self.lock:

            try:

                self._create_backup()

                self._atomic_write(
                    []
                )

                self.delete_count += 1

                return True

            except Exception as e:

                self.error_count += 1

                logger.exception(
                    "Archive clear failed: %s",
                    e
                )

                return False


    # ========================================================
    #
    # COUNT
    #
    # ========================================================

    def count(
        self,
        domain=None,
        record_type=None
    ):

        if (
            domain is None
            and
            record_type is None
        ):

            return len(
                self.load()
            )

        return len(
            self.search(
                domain=domain,
                record_type=record_type
            )
        )


    # ========================================================
    #
    # STATISTICS
    #
    # ========================================================

    def statistics(
        self
    ):

        records = self.load()

        domains = {}
        types = {}
        categories = {}
        sources = {}

        confidence_values = []
        importance_values = []

        for record in records:

            domain = record.get(
                "domain",
                "unknown"
            )

            record_type = record.get(
                "type",
                "unknown"
            )

            category = record.get(
                "category",
                "unknown"
            )

            source = record.get(
                "source",
                "unknown"
            )

            domains[domain] = (
                domains.get(
                    domain,
                    0
                ) + 1
            )

            types[record_type] = (
                types.get(
                    record_type,
                    0
                ) + 1
            )

            categories[category] = (
                categories.get(
                    category,
                    0
                ) + 1
            )

            sources[source] = (
                sources.get(
                    source,
                    0
                ) + 1
            )

            try:

                confidence_values.append(
                    float(
                        record.get(
                            "confidence",
                            0
                        )
                    )
                )

            except Exception:

                pass

            try:

                importance_values.append(
                    float(
                        record.get(
                            "importance",
                            0
                        )
                    )
                )

            except Exception:

                pass


        total = len(
            records
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


        average_importance = (
            sum(
                importance_values
            )
            /
            len(
                importance_values
            )
            if importance_values
            else 0.0
        )


        return {

            "total":
                total,

            "max_records":
                self.max_records,

            "remaining_capacity":
                max(
                    self.max_records
                    - total,
                    0
                ),

            "domains":
                domains,

            "types":
                types,

            "categories":
                categories,

            "sources":
                sources,

            "average_confidence":
                round(
                    average_confidence,
                    2
                ),

            "average_importance":
                round(
                    average_importance,
                    2
                )

        }


    # ========================================================
    #
    # EXPORT
    #
    # ========================================================

    def export(
        self,
        output_path,
        domain=None,
        record_type=None,
        keyword=None
    ):

        try:

            output = Path(
                output_path
            )

            output.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            records = self.search(
                keyword=keyword,
                domain=domain,
                record_type=record_type
            )

            output.write_text(
                json.dumps(
                    records,
                    indent=4,
                    ensure_ascii=False,
                    default=str
                ),
                encoding="utf-8"
            )

            return True

        except Exception as e:

            self.error_count += 1

            logger.exception(
                "Archive export failed: %s",
                e
            )

            return False


    # ========================================================
    #
    # RETENTION
    #
    # ========================================================

    def enforce_retention(
        self,
        max_records=None
    ):

        with self.lock:

            records = self.load()

            limit = (
                int(max_records)
                if max_records is not None
                else self.max_records
            )

            if len(records) <= limit:

                return 0

            remove_count = (
                len(records)
                - limit
            )

            self._create_backup()

            self._atomic_write(
                records[
                    remove_count:
                ]
            )

            self.delete_count += (
                remove_count
            )

            return remove_count


    # ========================================================
    #
    # BACKUP PUBLIC METHOD
    #
    # ========================================================

    def backup(
        self
    ):

        with self.lock:

            return self._create_backup()


    # ========================================================
    #
    # HEALTH CHECK
    #
    # ========================================================

    def health(
        self
    ):

        try:

            records = self.load()

            valid = isinstance(
                records,
                list
            )

            return {

                "online":
                    True,

                "healthy":
                    valid,

                "path":
                    str(
                        self.path
                    ),

                "exists":
                    self.path.exists(),

                "records":
                    len(records)
                    if valid
                    else 0,

                "writable":
                    self.path.parent.exists(),

                "errors":
                    self.error_count,

                "recoveries":
                    self.recovery_count

            }

        except Exception as e:

            return {

                "online":
                    False,

                "healthy":
                    False,

                "path":
                    str(
                        self.path
                    ),

                "error":
                    str(e)

            }


    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(
        self
    ):

        statistics = self.statistics()

        return {

            "module":
                "archive_manager",

            "name":
                "Archive Manager",

            "version":
                ARCHIVE_VERSION,

            "online":
                True,

            "path":
                str(
                    self.path
                ),

            "records":
                statistics[
                    "total"
                ],

            "max_records":
                self.max_records,

            "remaining_capacity":
                statistics[
                    "remaining_capacity"
                ],

            "domains":
                statistics[
                    "domains"
                ],

            "types":
                statistics[
                    "types"
                ],

            "writes":
                self.write_count,

            "reads":
                self.read_count,

            "archives":
                self.archive_count,

            "deletes":
                self.delete_count,

            "searches":
                self.search_count,

            "duplicates":
                self.duplicate_count,

            "errors":
                self.error_count,

            "recoveries":
                self.recovery_count,

            "initialized_at":
                self.initialized_at

        }


# ============================================================
#
# GLOBAL INSTANCE
#
# ============================================================

archive_manager = ArchiveManager()


# ============================================================
#
# MODULE TEST
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

    print(
        "=========================================="
    )

    print(
        "INKSIDE INTELLIGENCE OS"
    )

    print(
        "ARCHIVE MANAGER TEST"
    )

    print(
        "=========================================="
    )


    # --------------------------------------------------------
    # Test observation
    # --------------------------------------------------------

    observation = archive_manager.observation(

        data={

            "market":
                "BTC/USD",

            "signal":
                "bullish",

            "pattern":
                "breakout",

            "volume":
                "high"

        },

        domain="trading",

        source="market_learning",

        confidence=82,

        importance=75,

        tags=[
            "btc",
            "bullish",
            "breakout"
        ]

    )

    print(
        "\nObservation:"
    )

    print(
        observation
    )


    # --------------------------------------------------------
    # Test knowledge
    # --------------------------------------------------------

    knowledge = archive_manager.knowledge(

        data={

            "question":
                "What is the capital of France?",

            "answer":
                "Paris"

        },

        domain="general_knowledge",

        category="geography",

        source="test",

        confidence=95,

        importance=60,

        tags=[
            "geography",
            "capital"
        ]

    )

    print(
        "\nKnowledge:"
    )

    print(
        knowledge
    )


    # --------------------------------------------------------
    # Test experience
    # --------------------------------------------------------

    experience = archive_manager.experience(

        data={

            "event":
                "multi_domain_evaluation",

            "result":
                "successful"

        },

        domain="multi_domain",

        source="system",

        confidence=90,

        importance=80,

        tags=[
            "learning",
            "evaluation"
        ]

    )

    print(
        "\nExperience:"
    )

    print(
        experience
    )


    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    print(
        "\nSearch BTC:"
    )

    print(
        archive_manager.search(
            keyword="BTC"
        )
    )


    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    print(
        "\nStatistics:"
    )

    print(
        json.dumps(
            archive_manager.statistics(),
            indent=4,
            ensure_ascii=False
        )
    )


    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    print(
        "\nHealth:"
    )

    print(
        json.dumps(
            archive_manager.health(),
            indent=4,
            ensure_ascii=False
        )
    )


    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    print(
        "\nStatus:"
    )

    print(
        json.dumps(
            archive_manager.status(),
            indent=4,
            ensure_ascii=False
        )
    )


    print(
        "\n=========================================="
    )

    print(
        "ARCHIVE MANAGER TEST FINISHED"
    )

    print(
        "=========================================="
    )

