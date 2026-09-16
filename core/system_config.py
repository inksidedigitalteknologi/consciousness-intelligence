# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# SYSTEM CONFIGURATION
# FOUNDATION v3.0
#
# Compatible Engine API: v1.0
#
# ============================================================
#
# PURPOSE
# ------------------------------------------------------------
# Central configuration layer for the entire Intelligence OS.
#
# Design goals:
# - Engine independent
# - Thread safe
# - Runtime configuration
# - Environment overrides
# - Typed access
# - Nested configuration
# - Safe defaults
# - Validation
# - Snapshot support
# - JSON persistence
# - Atomic file writes
# - Future plugin/module configuration
# - Backward compatible
#
# ============================================================

from __future__ import annotations

import copy
import json
import logging
import os
import threading

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


# ============================================================
#
# VERSION
#
# ============================================================

CONFIG_VERSION = "3.0"
API_VERSION = "1.0"


# ============================================================
#
# DEFAULT PATHS
#
# ============================================================

DEFAULT_CONFIG_DIR = Path("data")
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "system_config.json"


# ============================================================
#
# CONFIGURATION ERRORS
#
# ============================================================

class ConfigError(Exception):
    """Base configuration error."""


class ConfigValidationError(ConfigError):
    """Raised when configuration validation fails."""


# ============================================================
#
# CONFIG VALUE
#
# ============================================================

@dataclass
class ConfigValue:
    """
    Metadata container for a configuration value.
    """

    value: Any

    description: str = ""

    mutable: bool = True

    secret: bool = False

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# ============================================================
#
# SYSTEM CONFIG
#
# ============================================================

class SystemConfig:
    """
    Central configuration manager.

    Example:

        config = SystemConfig()

        config.set(
            "system.name",
            "INKSIDE Intelligence OS"
        )

        value = config.get(
            "system.name"
        )
    """

    def __init__(
        self,
        config_file: str | Path = DEFAULT_CONFIG_FILE,
        auto_load: bool = True
    ):

        self.lock = threading.RLock()

        self.config_file = Path(
            config_file
        )

        self.values: Dict[
            str,
            ConfigValue
        ] = {}

        self.started_at = (
            datetime.utcnow()
            .isoformat()
            + "Z"
        )

        self.version = CONFIG_VERSION

        self.api_version = API_VERSION

        self.change_count = 0

        self.load_count = 0

        self.save_count = 0

        self.error_count = 0

        self._register_defaults()

        if auto_load:

            self.load()


    # ========================================================
    #
    # DEFAULT CONFIGURATION
    #
    # ========================================================

    def _register_defaults(self):

        defaults = {

            # ------------------------------------------------
            # SYSTEM
            # ------------------------------------------------

            "system.name":
                "INKSIDE Intelligence OS",

            "system.version":
                CONFIG_VERSION,

            "system.environment":
                "production",

            "system.debug":
                False,

            "system.safe_mode":
                False,

            "system.auto_start":
                True,

            "system.max_workers":
                8,


            # ------------------------------------------------
            # ENGINE
            # ------------------------------------------------

            "engine.api_version":
                "1.0",

            "engine.enabled":
                True,

            "engine.max_execution_time":
                120,

            "engine.max_retries":
                3,

            "engine.parallel":
                True,


            # ------------------------------------------------
            # EVENTS
            # ------------------------------------------------

            "events.enabled":
                True,

            "events.max_history":
                1000,

            "events.async_enabled":
                True,


            # ------------------------------------------------
            # MODULES
            # ------------------------------------------------

            "modules.auto_load":
                True,

            "modules.strict_dependencies":
                True,

            "modules.allow_runtime_enable":
                True,

            "modules.allow_runtime_disable":
                True,


            # ------------------------------------------------
            # HEALTH
            # ------------------------------------------------

            "health.enabled":
                True,

            "health.interval":
                30,

            "health.failure_threshold":
                3,


            # ------------------------------------------------
            # MEMORY
            # ------------------------------------------------

            "memory.enabled":
                True,

            "memory.max_items":
                100000,

            "memory.persistence":
                True,


            # ------------------------------------------------
            # LEARNING
            # ------------------------------------------------

            "learning.enabled":
                True,

            "learning.auto_adapt":
                True,

            "learning.minimum_confidence":
                50.0,


            # ------------------------------------------------
            # LOGGING
            # ------------------------------------------------

            "logging.enabled":
                True,

            "logging.level":
                "INFO",

            "logging.file":
                "logs/inkside.log",


            # ------------------------------------------------
            # STORAGE
            # ------------------------------------------------

            "storage.data_dir":
                "data",

            "storage.cache_dir":
                "data/cache",

            "storage.history_dir":
                "data/history",

            "storage.backup_dir":
                "data/backups",


            # ------------------------------------------------
            # SECURITY
            # ------------------------------------------------

            "security.enabled":
                True,

            "security.validate_inputs":
                True,

            "security.max_payload_size":
                10_000_000,


            # ------------------------------------------------
            # FUTURE AI
            # ------------------------------------------------

            "ai.enabled":
                False,

            "ai.provider":
                "local",

            "ai.model":
                "",

            "ai.timeout":
                60,

            "ai.max_tokens":
                4096,


            # ------------------------------------------------
            # FUTURE API
            # ------------------------------------------------

            "api.enabled":
                False,

            "api.host":
                "127.0.0.1",

            "api.port":
                8080,

            "api.timeout":
                30

        }

        for key, value in defaults.items():

            self.values[key] = ConfigValue(
                value=value
            )


    # ========================================================
    #
    # GET
    #
    # ========================================================

    def get(
        self,
        key: str,
        default: Any = None
    ) -> Any:

        with self.lock:

            item = self.values.get(
                key
            )

            if item is None:

                return default

            return copy.deepcopy(
                item.value
            )


    # ========================================================
    #
    # SET
    #
    # ========================================================

    def set(
        self,
        key: str,
        value: Any,
        *,
        mutable: Optional[bool] = None,
        secret: Optional[bool] = None,
        description: Optional[str] = None
    ) -> bool:

        if not key:

            raise ConfigError(
                "Configuration key cannot be empty."
            )

        with self.lock:

            existing = self.values.get(
                key
            )

            if existing is not None:

                if not existing.mutable:

                    raise ConfigError(
                        f"Configuration is immutable: {key}"
                    )

                if mutable is None:

                    mutable = existing.mutable

                if secret is None:

                    secret = existing.secret

                if description is None:

                    description = (
                        existing.description
                    )

            else:

                if mutable is None:

                    mutable = True

                if secret is None:

                    secret = False

                if description is None:

                    description = ""

            self.values[key] = ConfigValue(

                value=copy.deepcopy(
                    value
                ),

                description=description,

                mutable=mutable,

                secret=secret,

                metadata=(
                    existing.metadata
                    if existing is not None
                    else {}
                )
            )

            self.change_count += 1

        return True


    # ========================================================
    #
    # DELETE
    #
    # ========================================================

    def delete(
        self,
        key: str
    ) -> bool:

        with self.lock:

            item = self.values.get(
                key
            )

            if item is None:

                return False

            if not item.mutable:

                raise ConfigError(
                    f"Configuration is immutable: {key}"
                )

            del self.values[key]

            self.change_count += 1

        return True


    # ========================================================
    #
    # EXISTS
    #
    # ========================================================

    def exists(
        self,
        key: str
    ) -> bool:

        with self.lock:

            return key in self.values


    # ========================================================
    #
    # GET PREFIX
    #
    # ========================================================

    def get_prefix(
        self,
        prefix: str
    ) -> Dict[str, Any]:

        with self.lock:

            return {
                key:
                    copy.deepcopy(
                        item.value
                    )

                for key, item
                in self.values.items()

                if key.startswith(prefix)
            }


    # ========================================================
    #
    # UPDATE MANY
    #
    # ========================================================

    def update(
        self,
        values: Dict[str, Any]
    ) -> int:

        if not isinstance(
            values,
            dict
        ):

            raise ConfigError(
                "Configuration update must be a dictionary."
            )

        changed = 0

        for key, value in values.items():

            if self.set(
                key,
                value
            ):

                changed += 1

        return changed


    # ========================================================
    #
    # TYPE HELPERS
    #
    # ========================================================

    def get_string(
        self,
        key: str,
        default: str = ""
    ) -> str:

        value = self.get(
            key,
            default
        )

        if value is None:

            return default

        return str(value)


    def get_int(
        self,
        key: str,
        default: int = 0
    ) -> int:

        value = self.get(
            key,
            default
        )

        try:

            return int(value)

        except Exception:

            return default


    def get_float(
        self,
        key: str,
        default: float = 0.0
    ) -> float:

        value = self.get(
            key,
            default
        )

        try:

            return float(value)

        except Exception:

            return default


    def get_bool(
        self,
        key: str,
        default: bool = False
    ) -> bool:

        value = self.get(
            key,
            default
        )

        if isinstance(
            value,
            bool
        ):

            return value

        if isinstance(
            value,
            str
        ):

            return value.lower() in {
                "1",
                "true",
                "yes",
                "on",
                "enabled"
            }

        return bool(value)


    # ========================================================
    #
    # ENVIRONMENT OVERRIDE
    #
    # ========================================================

    def load_environment(
        self,
        prefix: str = "INKSIDE_"
    ) -> int:
        """
        Load environment variables.

        Example:

            INKSIDE_ENGINE_MAX_RETRIES=5

        becomes:

            engine.max.retries

        Existing keys are preferred when converting
        underscores to dots.
        """

        changed = 0

        for env_key, env_value in os.environ.items():

            if not env_key.startswith(
                prefix
            ):

                continue

            raw_key = env_key[
                len(prefix):
            ].lower()

            candidate = raw_key.replace(
                "_",
                "."
            )

            if self.exists(
                candidate
            ):

                current = self.get(
                    candidate
                )

                converted = (
                    self._convert_type(
                        env_value,
                        current
                    )
                )

                self.set(
                    candidate,
                    converted
                )

                changed += 1

        return changed


    # ========================================================
    #
    # TYPE CONVERSION
    # ========================================================

    @staticmethod
    def _convert_type(
        value: str,
        reference: Any
    ) -> Any:

        try:

            if isinstance(
                reference,
                bool
            ):

                return value.lower() in {
                    "1",
                    "true",
                    "yes",
                    "on",
                    "enabled"
                }

            if isinstance(
                reference,
                int
            ):

                return int(value)

            if isinstance(
                reference,
                float
            ):

                return float(value)

            return value

        except Exception:

            return value


    # ========================================================
    #
    # VALIDATION
    #
    # ========================================================

    def validate(self) -> Dict[str, Any]:
        """
        Validate known configuration values.
        """

        errors = []

        max_workers = self.get_int(
            "system.max_workers"
        )

        if max_workers < 1:

            errors.append(
                "system.max_workers must be >= 1"
            )


        retries = self.get_int(
            "engine.max_retries"
        )

        if retries < 0:

            errors.append(
                "engine.max_retries must be >= 0"
            )


        history = self.get_int(
            "events.max_history"
        )

        if history < 1:

            errors.append(
                "events.max_history must be >= 1"
            )


        health_interval = self.get_int(
            "health.interval"
        )

        if health_interval < 1:

            errors.append(
                "health.interval must be >= 1"
            )


        confidence = self.get_float(
            "learning.minimum_confidence"
        )

        if not 0 <= confidence <= 100:

            errors.append(
                "learning.minimum_confidence "
                "must be between 0 and 100"
            )


        api_port = self.get_int(
            "api.port"
        )

        if not 1 <= api_port <= 65535:

            errors.append(
                "api.port must be between 1 and 65535"
            )


        return {

            "valid":
                len(errors) == 0,

            "errors":
                errors,

            "checked_at":
                datetime.utcnow()
                .isoformat()
                + "Z"
        }


    # ========================================================
    #
    # SNAPSHOT
    #
    # ========================================================

    def snapshot(
        self,
        include_secrets: bool = False
    ) -> Dict[str, Any]:

        with self.lock:

            result = {}

            for key, item in (
                self.values.items()
            ):

                if (
                    item.secret
                    and not include_secrets
                ):

                    result[key] = (
                        "[SECRET]"
                    )

                else:

                    result[key] = (
                        copy.deepcopy(
                            item.value
                        )
                    )

        return result


    # ========================================================
    #
    # METADATA
    #
    # ========================================================

    def metadata(self) -> Dict[str, Any]:

        with self.lock:

            return {

                key: {

                    "mutable":
                        item.mutable,

                    "secret":
                        item.secret,

                    "description":
                        item.description,

                    "metadata":
                        copy.deepcopy(
                            item.metadata
                        )

                }

                for key, item
                in self.values.items()
            }


    # ========================================================
    #
    # SAVE
    # ========================================================

    def save(
        self,
        file_path: Optional[str | Path] = None
    ) -> bool:

        path = Path(
            file_path
            if file_path is not None
            else self.config_file
        )

        try:

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            payload = {

                "version":
                    CONFIG_VERSION,

                "api_version":
                    API_VERSION,

                "saved_at":
                    datetime.utcnow()
                    .isoformat()
                    + "Z",

                "values":
                    self.snapshot(
                        include_secrets=True
                    )

            }

            temporary = path.with_suffix(
                path.suffix + ".tmp"
            )

            with temporary.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    payload,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

            temporary.replace(
                path
            )

            self.save_count += 1

            logger.info(
                "System configuration saved: %s",
                path
            )

            return True

        except Exception as exc:

            self.error_count += 1

            logger.error(
                "Configuration save failed: %s",
                exc
            )

            return False


    # ========================================================
    #
    # LOAD
    #
    # ========================================================

    def load(
        self,
        file_path: Optional[str | Path] = None
    ) -> bool:

        path = Path(
            file_path
            if file_path is not None
            else self.config_file
        )

        if not path.exists():

            return False

        try:

            with path.open(
                "r",
                encoding="utf-8"
            ) as file:

                payload = json.load(
                    file
                )

            values = payload.get(
                "values",
                {}
            )

            if not isinstance(
                values,
                dict
            ):

                raise ConfigValidationError(
                    "Invalid configuration values."
                )

            for key, value in (
                values.items()
            ):

                if key in self.values:

                    existing = (
                        self.values[key]
                    )

                    if not existing.mutable:

                        continue

                    existing.value = (
                        copy.deepcopy(
                            value
                        )
                    )

                else:

                    self.values[key] = (
                        ConfigValue(
                            value=copy.deepcopy(
                                value
                            )
                        )
                    )

            self.load_count += 1

            logger.info(
                "System configuration loaded: %s",
                path
            )

            return True

        except Exception as exc:

            self.error_count += 1

            logger.error(
                "Configuration load failed: %s",
                exc
            )

            return False


    # ========================================================
    #
    # RESET TO DEFAULTS
    #
    # ========================================================

    def reset_defaults(self):

        with self.lock:

            current = dict(
                self.values
            )

            self.values.clear()

            self._register_defaults()

            for key, item in current.items():

                if (
                    key not in self.values
                    and not item.mutable
                ):

                    self.values[key] = item

            self.change_count += 1

        logger.info(
            "System configuration reset."
        )


    # ========================================================
    #
    # STATUS
    #
    # ========================================================

    def status(self) -> Dict[str, Any]:

        with self.lock:

            validation = self.validate()

            return {

                "status":
                    "ONLINE"
                    if validation["valid"]
                    else "WARNING",

                "version":
                    CONFIG_VERSION,

                "api_version":
                    API_VERSION,

                "keys":
                    len(self.values),

                "changes":
                    self.change_count,

                "loads":
                    self.load_count,

                "saves":
                    self.save_count,

                "errors":
                    self.error_count,

                "config_file":
                    str(self.config_file),

                "validation":
                    validation

            }


# ============================================================
#
# GLOBAL CONFIGURATION
#
# ============================================================

system_config = SystemConfig(
    auto_load=True
)


# ============================================================
#
# COMPATIBILITY API
#
# ============================================================

def get(
    key: str,
    default: Any = None
) -> Any:

    return system_config.get(
        key,
        default
    )


def set(
    key: str,
    value: Any,
    **kwargs
) -> bool:

    return system_config.set(
        key,
        value,
        **kwargs
    )


def delete(
    key: str
) -> bool:

    return system_config.delete(
        key
    )


def exists(
    key: str
) -> bool:

    return system_config.exists(
        key
    )


def update(
    values: Dict[str, Any]
) -> int:

    return system_config.update(
        values
    )


def snapshot(
    include_secrets: bool = False
):

    return system_config.snapshot(
        include_secrets
    )


def validate():

    return system_config.validate()


def save(
    file_path: Optional[str | Path] = None
):

    return system_config.save(
        file_path
    )


def load(
    file_path: Optional[str | Path] = None
):

    return system_config.load(
        file_path
    )


def status():

    return system_config.status()


# ============================================================
#
# TEST
#
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO
    )

    print()
    print("=" * 60)
    print("INKSIDE INTELLIGENCE OS")
    print("SYSTEM CONFIGURATION TEST")
    print("=" * 60)
    print()

    print(
        "System:",
        get("system.name")
    )

    print(
        "Engine API:",
        get("engine.api_version")
    )

    print(
        "Max Workers:",
        get("system.max_workers")
    )

    set(
        "system.debug",
        True
    )

    print(
        "Debug:",
        get("system.debug")
    )

    print()
    print("VALIDATION:")
    print(
        validate()
    )

    print()
    print("STATUS:")
    print(
        status()
    )

    print()
    print("SNAPSHOT:")
    print(
        snapshot()
    )

    print()
    print("=" * 60)
    print("SYSTEM CONFIGURATION TEST COMPLETE")
    print("=" * 60)