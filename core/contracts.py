# core/contracts.py
# INKSIDE DIGITAL - CONTRACTS (standalone)
# ============================================================

CONTRACT_VERSION = "2.0"
INTERNAL_CONTRACT_REVISION = "2.0"
CONTRACT_SCHEMA = ""
DEFAULT_MAX_DEPTH = 20
DEFAULT_MAX_ITEMS = 10000
DEFAULT_MAX_STRING_LENGTH = 100000
CIRCULAR_REFERENCE_MARKER = "[CIRCULAR_REFERENCE]"
MAX_DEPTH_MARKER = "[MAX_DEPTH]"
UNSERIALIZABLE_MARKER = "[UNSERIALIZABLE]"
TRUNCATED_MARKER = "[TRUNCATED]"

OUTPUT_SUCCESS = "success"
OUTPUT_PARTIAL = "partial"
OUTPUT_SKIPPED = "skipped"
OUTPUT_FAILED = "failed"
VALID_OUTPUT_STATES = {"success", "partial", "skipped", "failed"}

MODULE_CREATED = "created"
MODULE_INITIALIZING = "initializing"
MODULE_ONLINE = "online"
MODULE_DEGRADED = "degraded"
MODULE_OFFLINE = "offline"

ModuleContract = None
ModuleOutput = None
ModuleInput = None

__all__ = [
    "CONTRACT_VERSION", "OUTPUT_SUCCESS", "OUTPUT_PARTIAL",
    "OUTPUT_SKIPPED", "OUTPUT_FAILED", "MODULE_ONLINE",
    "MODULE_DEGRADED", "MODULE_OFFLINE", "ModuleContract",
    "ModuleOutput", "ModuleInput",
]
