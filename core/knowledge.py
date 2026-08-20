# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# KNOWLEDGE ENGINE v3.1
#
# SUPER COMPREHENSIVE PERMANENT UNDERSTANDING LAYER - FIXED
#
# FIXES:
# - Safe handling of CognitiveState objects as keys
# - Fixed is_dataclass import issue
# - Proper dict conversion for dataclasses
# - Better error handling for unhashable types
# - State cache management
# - JSON serialization safety
# - Fixed CognitiveState in dictionary keys
# - Improved safe_key for complex objects
#
# ============================================================

from __future__ import annotations

import logging
import json
import threading
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set, Union
from dataclasses import dataclass, field, is_dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================
# CONSTANTS
# ============================================================

KNOWLEDGE_VERSION = "3.1.1"

# Storage
DATA_DIR = Path("database")
DATA_DIR.mkdir(exist_ok=True)

KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"
KNOWLEDGE_INDEX_FILE = DATA_DIR / "knowledge_index.json"
KNOWLEDGE_BACKUP_DIR = DATA_DIR / "knowledge_backups"
KNOWLEDGE_BACKUP_DIR.mkdir(exist_ok=True)

# Defaults
DEFAULT_MAX_ITEMS = 10000
DEFAULT_CONFIDENCE_DECAY = 0.01
DEFAULT_CONFIDENCE_MIN = 0.0
DEFAULT_CONFIDENCE_MAX = 100.0
DEFAULT_SIMILARITY_THRESHOLD = 0.7
DEFAULT_EXPIRATION_DAYS = 365
DEFAULT_AUTO_BACKUP_INTERVAL = 3600 * 24  # 24 hours


# ============================================================
# ENUMS
# ============================================================

class KnowledgeCategory(Enum):
    """Knowledge categories."""
    GENERAL = "general"
    MARKET = "market"
    TRADING = "trading"
    PATTERN = "pattern"
    STRATEGY = "strategy"
    ANALYSIS = "analysis"
    REFLECTION = "reflection"
    INSIGHT = "insight"
    LEARNING = "learning"
    EXPERIENCE = "experience"
    KNOWLEDGE = "knowledge"
    CONCEPT = "concept"
    FACT = "fact"
    RULE = "rule"
    PROCEDURE = "procedure"
    REFERENCE = "reference"
    STATE = "state"


class KnowledgeStatus(Enum):
    """Knowledge status."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"
    EXPIRED = "expired"
    PENDING = "pending"
    REVIEW = "review"


class KnowledgeType(Enum):
    """Knowledge types."""
    FACT = "fact"
    CONCEPT = "concept"
    RULE = "rule"
    PROCEDURE = "procedure"
    REFERENCE = "reference"
    INSIGHT = "insight"
    PATTERN = "pattern"
    STRATEGY = "strategy"
    EXPERIENCE = "experience"
    REFLECTION = "reflection"
    ANALYSIS = "analysis"
    PREDICTION = "prediction"
    DECISION = "decision"
    LEARNING = "learning"
    STATE = "state"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class KnowledgeItem:
    """Single knowledge item."""
    id: str
    content: str
    category: str = KnowledgeCategory.GENERAL.value
    type: str = KnowledgeType.FACT.value
    status: str = KnowledgeStatus.ACTIVE.value
    confidence: float = 0.0
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)
    source: str = "unknown"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    accessed_at: Optional[str] = None
    expires_at: Optional[str] = None
    access_count: int = 0
    version: int = 1
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "category": self.category,
            "type": self.type,
            "status": self.status,
            "confidence": self.confidence,
            "importance": self.importance,
            "tags": self.tags,
            "source": self.source,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "accessed_at": self.accessed_at,
            "expires_at": self.expires_at,
            "access_count": self.access_count,
            "version": self.version,
            "parent_id": self.parent_id,
            "children": self.children,
            "relationships": self.relationships,
            "metadata": self.metadata,
        }


@dataclass
class KnowledgeStats:
    """Knowledge statistics."""
    total: int = 0
    by_category: Dict[str, int] = field(default_factory=dict)
    by_type: Dict[str, int] = field(default_factory=dict)
    by_status: Dict[str, int] = field(default_factory=dict)
    avg_confidence: float = 0.0
    total_access: int = 0
    recently_added: int = 0
    active: int = 0
    archived: int = 0
    expired: int = 0
    deprecated: int = 0
    state_count: int = 0


# ============================================================
# FIX: SAFE KEY HELPER FUNCTIONS - IMPROVED
# ============================================================

def safe_key(obj: Any) -> str:
    """
    Convert any object to a safe string key.
    
    FIX: Handles CognitiveState and other unhashable types.
    """
    if obj is None:
        return "none"
    
    # Already string
    if isinstance(obj, str):
        return obj
    
    # Integer, float, boolean
    if isinstance(obj, (int, float, bool)):
        return str(obj)
    
    # Enum
    if isinstance(obj, Enum):
        return f"{obj.__class__.__name__}_{obj.value}"
    
    # ============================================================
    # FIX: Handle dataclass (including CognitiveState) FIRST
    # ============================================================
    
    if is_dataclass(obj):
        try:
            data = {}
            # Get all fields from dataclass
            if hasattr(obj, '__dataclass_fields__'):
                for field_name in obj.__dataclass_fields__:
                    try:
                        value = getattr(obj, field_name, None)
                        data[field_name] = safe_key(value)
                    except Exception:
                        data[field_name] = f"<error_{field_name}>"
            else:
                # Fallback: use asdict
                try:
                    data = asdict(obj)
                    for key, value in data.items():
                        data[key] = safe_key(value)
                except Exception:
                    data = {"__value__": str(obj)}
            return f"dataclass_{type(obj).__name__}_{hash(json.dumps(data, sort_keys=True, default=str))}"
        except Exception:
            return f"dataclass_{type(obj).__name__}_{id(obj)}"
    
    # Has to_dict method
    if hasattr(obj, 'to_dict') and callable(obj.to_dict):
        try:
            data = obj.to_dict()
            if isinstance(data, dict):
                return json.dumps(data, sort_keys=True, default=str)
            return str(data)
        except Exception:
            return str(obj)
    
    # Dict
    if isinstance(obj, dict):
        try:
            sorted_dict = {}
            for key in sorted(obj.keys()):
                try:
                    sorted_dict[safe_key(key)] = safe_key(obj[key])
                except Exception:
                    sorted_dict[safe_key(key)] = str(obj[key])
            return json.dumps(sorted_dict, sort_keys=True, default=str)
        except Exception:
            return str(obj)
    
    # List or tuple
    if isinstance(obj, (list, tuple)):
        try:
            safe_list = [safe_key(item) for item in obj]
            return json.dumps(safe_list, sort_keys=True)
        except Exception:
            return str(obj)
    
    # Has __dict__
    if hasattr(obj, '__dict__'):
        try:
            data = {}
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    try:
                        data[key] = safe_key(value)
                    except Exception:
                        data[key] = f"<error_{key}>"
            return json.dumps(data, sort_keys=True)
        except Exception:
            return str(obj)
    
    # Last resort - use id
    try:
        return f"{type(obj).__name__}_{id(obj)}"
    except Exception:
        return f"<{type(obj).__name__}>"


def safe_hash(obj: Any) -> str:
    """Generate safe hash from any object."""
    key = safe_key(obj)
    return hashlib.md5(key.encode()).hexdigest()[:16]


def safe_dict(obj: Any) -> Dict[str, Any]:
    """
    Convert any object to a safe dictionary.
    """
    if obj is None:
        return {}
    
    # ============================================================
    # FIX: Handle dataclass first
    # ============================================================
    
    if is_dataclass(obj):
        result = {"__dataclass__": type(obj).__name__}
        try:
            if hasattr(obj, '__dataclass_fields__'):
                for field_name in obj.__dataclass_fields__:
                    try:
                        value = getattr(obj, field_name, None)
                        result[field_name] = safe_dict(value)
                    except Exception:
                        result[field_name] = f"<error_{field_name}>"
            else:
                try:
                    data = asdict(obj)
                    for key, value in data.items():
                        result[key] = safe_dict(value)
                except Exception:
                    result["__value__"] = str(obj)
        except Exception:
            result["__value__"] = str(obj)
        return result
    
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            result[safe_key(key)] = safe_dict(value)
        return result
    
    if isinstance(obj, (list, tuple)):
        return {"__list__": [safe_dict(item) for item in obj]}
    
    if isinstance(obj, Enum):
        return {"__enum__": obj.value, "__class__": obj.__class__.__name__}
    
    if hasattr(obj, 'to_dict') and callable(obj.to_dict):
        try:
            data = obj.to_dict()
            return safe_dict(data)
        except Exception:
            return {"__value__": str(obj)}
    
    if hasattr(obj, '__dict__'):
        result = {"__object__": type(obj).__name__}
        for key, value in obj.__dict__.items():
            if not key.startswith('_'):
                try:
                    result[key] = safe_dict(value)
                except Exception:
                    result[key] = f"<error_{key}>"
        return result
    
    return {"__value__": str(obj)}


def safe_serialize(obj: Any) -> Any:
    """
    Safely serialize any object for JSON.
    """
    if obj is None:
        return None
    
    if isinstance(obj, (str, int, float, bool)):
        return obj
    
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            result[safe_key(key)] = safe_serialize(value)
        return result
    
    if isinstance(obj, (list, tuple)):
        return [safe_serialize(item) for item in obj]
    
    if isinstance(obj, Enum):
        return obj.value
    
    if is_dataclass(obj):
        return safe_serialize(safe_dict(obj))
    
    if hasattr(obj, 'to_dict') and callable(obj.to_dict):
        try:
            return safe_serialize(obj.to_dict())
        except Exception:
            return str(obj)
    
    if hasattr(obj, '__dict__'):
        return safe_serialize(safe_dict(obj))
    
    return str(obj)


# ============================================================
# KNOWLEDGE ENGINE v3.1 - FIXED
# ============================================================

class KnowledgeEngine:
    """
    Knowledge Engine v3.1 - Super Comprehensive Knowledge Management - FIXED.
    """

    VERSION = KNOWLEDGE_VERSION

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.lock = threading.RLock()
        
        # Configuration
        self.max_items = self.config.get("max_items", DEFAULT_MAX_ITEMS)
        self.confidence_decay = self.config.get("confidence_decay", DEFAULT_CONFIDENCE_DECAY)
        self.similarity_threshold = self.config.get("similarity_threshold", DEFAULT_SIMILARITY_THRESHOLD)
        self.expiration_days = self.config.get("expiration_days", DEFAULT_EXPIRATION_DAYS)
        self.auto_backup_interval = self.config.get("auto_backup_interval", DEFAULT_AUTO_BACKUP_INTERVAL)
        
        # Knowledge storage
        self._knowledge: Dict[str, KnowledgeItem] = {}
        self._categories: Dict[str, List[str]] = {}
        self._tags: Dict[str, List[str]] = {}
        self._index: Dict[str, Set[str]] = {}
        
        # FIX: State cache with safe keys (string keys, not objects)
        self._state_cache: Dict[str, Dict] = {}
        
        # Stats
        self._stats = KnowledgeStats()
        self._last_backup: Optional[str] = None
        self._initialized = False
        
        # Load data
        self.load()
        self._build_index()
        
        # Start auto-backup if enabled
        if self.config.get("auto_backup", True):
            self._start_auto_backup()
        
        self._initialized = True
        logger.info("Knowledge Engine v%s initialized. Items: %d, States: %d", 
                   self.VERSION, len(self._knowledge), len(self._state_cache))

    # ============================================================
    # FIXED: STATE MANAGEMENT
    # ============================================================

    def store_state(self, state: Any, metadata: Optional[Dict] = None) -> str:
        """
        Store any state object safely.
        """
        try:
            # Generate safe key
            state_key = safe_key(state)
            
            # Extract state data safely (pastikan dict)
            state_data = self._extract_state_data(state)
            
            # Pastikan metadata adalah dict
            if metadata is None:
                metadata = {}
            elif not isinstance(metadata, dict):
                metadata = {"value": str(metadata)}
            
            # Pastikan state_data adalah dict
            if not isinstance(state_data, dict):
                state_data = {"__value__": str(state_data)}
            
            with self.lock:
                # Store in cache dengan data yang sudah safe
                self._state_cache[state_key] = {
                    'state_key': state_key,
                    'state_type': type(state).__name__,
                    'data': state_data,
                    'metadata': metadata,
                    'timestamp': datetime.now().isoformat(),
                    'access_count': 0,
                }
                
                # FIX: Hanya simpan metadata yang safe
                content = self._format_state_content(state, state_data)
                
                safe_metadata = {
                    'state_key': state_key,
                    'state_type': type(state).__name__,
                    'timestamp': datetime.now().isoformat(),
                    'state_summary': self._get_state_summary(state_data),
                }
                
                item_id = self.add(
                    content=content,
                    category=KnowledgeCategory.STATE.value,
                    type=KnowledgeType.STATE.value,
                    tags=['state', type(state).__name__.lower(), 'cognitive'],
                    confidence=50.0,
                    importance=0.5,
                    metadata=safe_metadata,
                )
                
                self._stats.state_count = len(self._state_cache)
            
            self.save()
            logger.debug("State stored: %s (%s)", state_key[:8], type(state).__name__)
            return state_key
            
        except Exception as e:
            logger.error(f"Store state failed: {e}")
            fallback_key = f"state_{id(state)}_{int(time.time())}"
            self._state_cache[fallback_key] = {
                'state_key': fallback_key,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
            }
            return fallback_key

    def _get_state_summary(self, state_data: Dict) -> str:
        """Get summary of state data."""
        try:
            important_keys = ['state', 'status', 'mode', 'phase', 'confidence', 
                            'level', 'active', 'running', 'current', 'cycle']
            parts = []
            for key in important_keys:
                if key in state_data:
                    value = state_data[key]
                    if isinstance(value, (str, int, float, bool)):
                        parts.append(f"{key}={value}")
            return ", ".join(parts[:5]) if parts else "no_summary"
        except Exception:
            return "error_summary"

    def get_state(self, state_key: str) -> Optional[Dict]:
        """Get stored state by key."""
        with self.lock:
            result = self._state_cache.get(state_key)
            if result:
                result['access_count'] = result.get('access_count', 0) + 1
            return result

    def get_all_states(self) -> List[Dict]:
        """Get all stored states."""
        with self.lock:
            return list(self._state_cache.values())

    def get_states_by_type(self, state_type: str) -> List[Dict]:
        """Get states by type."""
        results = []
        with self.lock:
            for cached in self._state_cache.values():
                if cached.get('state_type') == state_type:
                    results.append(cached)
        return results

    def delete_state(self, state_key: str) -> bool:
        """Delete a stored state."""
        try:
            with self.lock:
                if state_key in self._state_cache:
                    del self._state_cache[state_key]
                    self._stats.state_count = len(self._state_cache)
                    self.save()
                    return True
            return False
        except Exception as e:
            logger.error(f"Delete state failed: {e}")
            return False

    def clear_states(self) -> int:
        """Clear all stored states."""
        with self.lock:
            count = len(self._state_cache)
            self._state_cache.clear()
            self._stats.state_count = 0
            self.save()
            logger.info(f"Cleared {count} states")
            return count

    def _extract_state_data(self, state: Any) -> Dict[str, Any]:
        """Extract data from state object safely."""
        return safe_dict(state)

    def _format_state_content(self, state: Any, data: Dict) -> str:
        """Format state content for storage."""
        try:
            state_type = type(state).__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            content = f"[{timestamp}] Cognitive State: {state_type}\n"
            content += f"Type: {state_type}\n"
            
            # Add important fields
            important_keys = ['state', 'status', 'mode', 'phase', 'confidence', 
                            'level', 'active', 'running', 'current', 'cycle']
            
            found = False
            for key in important_keys:
                if key in data:
                    value = data[key]
                    if isinstance(value, (str, int, float, bool)):
                        content += f"{key}: {value}\n"
                        found = True
            
            if not found:
                keys = list(data.keys())[:5]
                for key in keys:
                    if not key.startswith('__'):
                        value = data[key]
                        if isinstance(value, (str, int, float, bool)):
                            content += f"{key}: {value}\n"
            
            content += f"\nData points: {len(data)}"
            
            return content
            
        except Exception as e:
            return f"Cognitive State update at {datetime.now().isoformat()} (error: {e})"

    # ============================================================
    # LOAD / SAVE (FIXED)
    # ============================================================

    def load(self) -> bool:
        """Load knowledge from storage."""
        try:
            # Load knowledge
            if KNOWLEDGE_FILE.exists():
                with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    for item_id, item_data in data.items():
                        if isinstance(item_data, dict):
                            self._knowledge[item_id] = KnowledgeItem(**item_data)
                elif isinstance(data, list):
                    for item_data in data:
                        if isinstance(item_data, dict):
                            item_id = item_data.get("id", str(len(self._knowledge)))
                            self._knowledge[item_id] = KnowledgeItem(**item_data)
            
            # Load state cache
            state_file = DATA_DIR / "state_cache.json"
            if state_file.exists():
                with open(state_file, "r", encoding="utf-8") as f:
                    # FIX: Safe load state cache
                    try:
                        self._state_cache = json.load(f)
                    except Exception as e:
                        logger.warning(f"Failed to load state cache: {e}")
                        self._state_cache = {}
            
            self._build_index()
            self._update_stats()
            
            logger.info("Knowledge loaded: %d items, %d states", 
                       len(self._knowledge), len(self._state_cache))
            return True
            
        except Exception as e:
            logger.error("Knowledge load failed: %s", e)
            return False

    def save(self) -> bool:
        """
        Save knowledge to storage.
        """
        try:
            with self.lock:
                # Save knowledge - convert to safe dict
                data = {}
                for item_id, item in self._knowledge.items():
                    try:
                        data[item_id] = item.to_dict()
                    except Exception as e:
                        logger.warning(f"Failed to serialize item {item_id}: {e}")
                        data[item_id] = {"id": item_id, "error": str(e)}
                
                temp_file = KNOWLEDGE_FILE.with_suffix(".tmp")
                with open(temp_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=safe_serialize)
                temp_file.replace(KNOWLEDGE_FILE)
                
                # FIX: Save state cache dengan safe_serialize
                state_file = DATA_DIR / "state_cache.json"
                
                # FIX: Ensure all state data is serializable
                safe_state_cache = {}
                for key, value in self._state_cache.items():
                    try:
                        safe_state_cache[key] = safe_serialize(value)
                    except Exception as e:
                        logger.warning(f"Failed to serialize state {key}: {e}")
                        safe_state_cache[key] = {"error": str(e), "key": str(key)}
                
                with open(state_file, "w", encoding="utf-8") as f:
                    json.dump(safe_state_cache, f, indent=2, ensure_ascii=False, default=safe_serialize)
                
                # Save index
                self._save_index()
            
            logger.debug("Knowledge saved: %d items, %d states", 
                        len(self._knowledge), len(self._state_cache))
            return True
            
        except Exception as e:
            logger.error("Knowledge save failed: %s", e)
            try:
                self._emergency_save()
            except Exception:
                pass
            return False

    def _emergency_save(self) -> bool:
        """Emergency save with minimal data."""
        try:
            emergency_file = DATA_DIR / "knowledge_emergency.json"
            data = {}
            for item_id, item in self._knowledge.items():
                try:
                    data[item_id] = {
                        "id": item.id,
                        "content": item.content[:1000],
                        "category": item.category,
                        "type": item.type,
                        "status": item.status,
                        "confidence": item.confidence,
                    }
                except Exception:
                    data[item_id] = {"id": item_id, "error": "emergency_serialization_failed"}
            
            with open(emergency_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=safe_serialize)
            logger.warning("Emergency save completed")
            return True
        except Exception:
            return False

    def _save_index(self) -> None:
        """Save search index."""
        try:
            with self.lock:
                index_data = {
                    "categories": self._categories,
                    "tags": self._tags,
                    "state_count": len(self._state_cache),
                    "last_updated": datetime.now().isoformat(),
                }
            
            with open(KNOWLEDGE_INDEX_FILE, "w", encoding="utf-8") as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.warning("Index save failed: %s", e)

    def _build_index(self) -> None:
        """Build search index."""
        with self.lock:
            self._categories = {}
            self._tags = {}
            self._index = {}
            
            for item_id, item in self._knowledge.items():
                # Category index
                if item.category not in self._categories:
                    self._categories[item.category] = []
                self._categories[item.category].append(item_id)
                
                # Tag index
                for tag in item.tags:
                    if tag not in self._tags:
                        self._tags[tag] = []
                    self._tags[tag].append(item_id)
                
                # Content index
                words = self._extract_keywords(item.content)
                for word in words:
                    if word not in self._index:
                        self._index[word] = set()
                    self._index[word].add(item_id)

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text."""
        stopwords = {
            "the", "a", "an", "and", "or", "of", "to", "in", "on", "for",
            "with", "is", "are", "was", "were", "this", "that", "it", "as",
            "at", "by", "from", "has", "have", "had", "will", "would", "could"
        }
        words = set()
        for word in text.lower().split():
            word = word.strip(".,!?;:()\"'")
            if len(word) > 2 and word not in stopwords:
                words.add(word)
        return words

    # ============================================================
    # KNOWLEDGE MANAGEMENT
    # ============================================================

    def add(
        self,
        content: str,
        category: str = KnowledgeCategory.GENERAL.value,
        type: str = KnowledgeType.FACT.value,
        tags: Optional[List[str]] = None,
        source: str = "unknown",
        confidence: float = 0.0,
        importance: float = 0.5,
        parent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        state_data: Optional[Any] = None
    ) -> Optional[str]:
        """
        Add new knowledge item.
        """
        if not content:
            logger.warning("Empty knowledge content")
            return None
        
        try:
            existing = self._find_similar(content)
            if existing:
                logger.debug("Similar knowledge exists: %s", existing[0].id)
            
            with self.lock:
                item_id = self._generate_id(content)
                
                if item_id in self._knowledge:
                    item = self._knowledge[item_id]
                    item.content = content
                    item.category = category
                    item.type = type
                    item.tags = tags or []
                    item.source = source
                    item.confidence = confidence
                    item.importance = importance
                    item.updated_at = datetime.now().isoformat()
                    item.version += 1
                    if parent_id:
                        item.parent_id = parent_id
                    if metadata:
                        item.metadata.update(metadata)
                    if state_data:
                        item.metadata['state_key'] = safe_key(state_data)
                    return item_id
                
                item = KnowledgeItem(
                    id=item_id,
                    content=content,
                    category=category,
                    type=type,
                    tags=tags or [],
                    source=source,
                    confidence=confidence,
                    importance=importance,
                    parent_id=parent_id,
                    metadata=metadata or {},
                )
                
                if state_data:
                    item.metadata['state_key'] = safe_key(state_data)
                
                self._knowledge[item_id] = item
                
                if category not in self._categories:
                    self._categories[category] = []
                self._categories[category].append(item_id)
                
                for tag in item.tags:
                    if tag not in self._tags:
                        self._tags[tag] = []
                    self._tags[tag].append(item_id)
                
                if parent_id and parent_id in self._knowledge:
                    self._knowledge[parent_id].children.append(item_id)
            
            self.save()
            self._update_stats()
            
            logger.info("Knowledge added: %s (%s)", item_id[:8], category)
            return item_id
            
        except Exception as e:
            logger.error("Add knowledge failed: %s", e)
            return None

    def _generate_id(self, content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def get(self, item_id: str, return_state: bool = False) -> Optional[Union[KnowledgeItem, Dict]]:
        with self.lock:
            item = self._knowledge.get(item_id)
            if not item:
                return None
            
            item.access_count += 1
            item.accessed_at = datetime.now().isoformat()
            self._update_stats()
            
            if return_state:
                state_key = item.metadata.get('state_key')
                if state_key:
                    return self._state_cache.get(state_key)
            
            return item

    def update(self, item_id: str, **kwargs) -> bool:
        try:
            with self.lock:
                item = self._knowledge.get(item_id)
                if not item:
                    return False
                
                for key, value in kwargs.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                
                item.updated_at = datetime.now().isoformat()
                item.version += 1
            
            self.save()
            self._build_index()
            self._update_stats()
            return True
            
        except Exception as e:
            logger.error("Update failed: %s", e)
            return False

    def delete(self, item_id: str, permanent: bool = False) -> bool:
        try:
            with self.lock:
                item = self._knowledge.get(item_id)
                if not item:
                    return False
                
                if permanent:
                    if item.parent_id and item.parent_id in self._knowledge:
                        parent = self._knowledge[item.parent_id]
                        if item_id in parent.children:
                            parent.children.remove(item_id)
                    
                    if item.category in self._categories:
                        if item_id in self._categories[item.category]:
                            self._categories[item.category].remove(item_id)
                    
                    for tag in item.tags:
                        if tag in self._tags and item_id in self._tags[tag]:
                            self._tags[tag].remove(item_id)
                    
                    del self._knowledge[item_id]
                else:
                    item.status = KnowledgeStatus.ARCHIVED.value
                    item.updated_at = datetime.now().isoformat()
            
            self.save()
            self._build_index()
            self._update_stats()
            return True
            
        except Exception as e:
            logger.error("Delete failed: %s", e)
            return False

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.0,
        max_results: int = 20,
        include_archived: bool = False,
        include_state_data: bool = False
    ) -> List[Union[KnowledgeItem, Dict]]:
        try:
            results = []
            
            with self.lock:
                candidates = set()
                keywords = self._extract_keywords(query)
                
                for keyword in keywords:
                    if keyword in self._index:
                        candidates.update(self._index[keyword])
                
                for item_id in candidates:
                    item = self._knowledge.get(item_id)
                    if not item:
                        continue
                    
                    if not include_archived and item.status == KnowledgeStatus.ARCHIVED.value:
                        continue
                    
                    if category and item.category != category:
                        continue
                    
                    if tags and not all(tag in item.tags for tag in tags):
                        continue
                    
                    if item.confidence < min_confidence:
                        continue
                    
                    score = self._calculate_relevance(query, item)
                    if score > 0:
                        if include_state_data:
                            state_key = item.metadata.get('state_key')
                            state_data = None
                            if state_key:
                                state_data = self._state_cache.get(state_key)
                            results.append((item, score, state_data))
                        else:
                            results.append((item, score))
            
            if include_state_data:
                results.sort(key=lambda x: (x[1], x[0].confidence), reverse=True)
                return [{
                    'item': item,
                    'score': score,
                    'state': state_data
                } for item, score, state_data in results[:max_results]]
            else:
                results.sort(key=lambda x: (x[1], x[0].confidence), reverse=True)
                return [item for item, _ in results[:max_results]]
        
        except Exception as e:
            logger.error("Search failed: %s", e)
            return []

    def _calculate_relevance(self, query: str, item: KnowledgeItem) -> float:
        score = 0.0
        query_lower = query.lower()
        content_lower = item.content.lower()
        
        if query_lower in content_lower:
            score += 0.5
        
        keywords = self._extract_keywords(query)
        for keyword in keywords:
            if keyword in content_lower:
                score += 0.2
        
        for tag in item.tags:
            if tag.lower() in query_lower:
                score += 0.3
        
        if item.category.lower() in query_lower:
            score += 0.2
        
        score += (item.confidence / 100) * 0.3
        
        try:
            created = datetime.fromisoformat(item.created_at)
            days_old = (datetime.now() - created).days
            score += max(0, (1 - days_old / 365)) * 0.1
        except Exception:
            pass
        
        return min(score, 1.0)

    def find_by_category(self, category: str) -> List[KnowledgeItem]:
        with self.lock:
            item_ids = self._categories.get(category, [])
            return [self._knowledge[i] for i in item_ids if i in self._knowledge]

    def find_by_tag(self, tag: str) -> List[KnowledgeItem]:
        with self.lock:
            item_ids = self._tags.get(tag, [])
            return [self._knowledge[i] for i in item_ids if i in self._knowledge]

    def find_similar(self, content: str, threshold: float = None) -> List[KnowledgeItem]:
        threshold = threshold or self.similarity_threshold
        
        try:
            results = []
            keywords = self._extract_keywords(content)
            
            for item in self._knowledge.values():
                similarity = self._calculate_similarity(keywords, item)
                if similarity >= threshold:
                    results.append((item, similarity))
            
            results.sort(key=lambda x: x[1], reverse=True)
            return [item for item, _ in results[:10]]
            
        except Exception as e:
            logger.debug("Similarity search failed: %s", e)
            return []

    def _calculate_similarity(self, keywords: Set[str], item: KnowledgeItem) -> float:
        if not keywords:
            return 0.0
        
        item_keywords = self._extract_keywords(item.content)
        intersection = keywords.intersection(item_keywords)
        
        if not intersection:
            return 0.0
        
        return len(intersection) / len(keywords)

    def _find_similar(self, content: str) -> List[KnowledgeItem]:
        return self.find_similar(content, threshold=0.8)

    # ============================================================
    # CONFIDENCE MANAGEMENT
    # ============================================================

    def reinforce(self, item_id: str, value: float) -> bool:
        try:
            with self.lock:
                item = self._knowledge.get(item_id)
                if not item:
                    return False
                
                item.confidence = min(DEFAULT_CONFIDENCE_MAX, item.confidence + value)
                item.updated_at = datetime.now().isoformat()
            
            self.save()
            self._update_stats()
            return True
            
        except Exception as e:
            logger.error("Reinforce failed: %s", e)
            return False

    def decay_confidence(self, item_id: str, value: float = None) -> bool:
        value = value or self.confidence_decay
        try:
            with self.lock:
                item = self._knowledge.get(item_id)
                if not item:
                    return False
                
                item.confidence = max(DEFAULT_CONFIDENCE_MIN, item.confidence - value)
                item.updated_at = datetime.now().isoformat()
            
            self.save()
            self._update_stats()
            return True
            
        except Exception as e:
            logger.error("Decay failed: %s", e)
            return False

    def apply_decay_all(self) -> int:
        count = 0
        try:
            with self.lock:
                for item in self._knowledge.values():
                    if item.confidence > 0:
                        item.confidence = max(DEFAULT_CONFIDENCE_MIN, item.confidence - self.confidence_decay)
                        count += 1
            
            self.save()
            self._update_stats()
            return count
            
        except Exception as e:
            logger.error("Decay all failed: %s", e)
            return 0

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    def add_relationship(self, item_id: str, relation_type: str, target_id: str) -> bool:
        try:
            with self.lock:
                item = self._knowledge.get(item_id)
                target = self._knowledge.get(target_id)
                
                if not item or not target:
                    return False
                
                if relation_type not in item.relationships:
                    item.relationships[relation_type] = []
                
                if target_id not in item.relationships[relation_type]:
                    item.relationships[relation_type].append(target_id)
                    item.updated_at = datetime.now().isoformat()
            
            self.save()
            return True
            
        except Exception as e:
            logger.error("Add relationship failed: %s", e)
            return False

    def get_relationships(self, item_id: str, relation_type: Optional[str] = None) -> Dict[str, List[KnowledgeItem]]:
        result = {}
        try:
            with self.lock:
                item = self._knowledge.get(item_id)
                if not item:
                    return result
                
                relations = item.relationships
                if relation_type:
                    relations = {relation_type: relations.get(relation_type, [])}
                
                for rel_type, targets in relations.items():
                    result[rel_type] = [
                        self._knowledge[t] for t in targets
                        if t in self._knowledge
                    ]
            
            return result
            
        except Exception as e:
            logger.error("Get relationships failed: %s", e)
            return {}

    # ============================================================
    # STATISTICS
    # ============================================================

    def stats(self) -> KnowledgeStats:
        with self.lock:
            return self._stats

    def _update_stats(self) -> None:
        with self.lock:
            stats = KnowledgeStats()
            stats.total = len(self._knowledge)
            stats.state_count = len(self._state_cache)
            
            for item in self._knowledge.values():
                stats.by_category[item.category] = stats.by_category.get(item.category, 0) + 1
                stats.by_type[item.type] = stats.by_type.get(item.type, 0) + 1
                stats.by_status[item.status] = stats.by_status.get(item.status, 0) + 1
                stats.total_access += item.access_count
                
                if item.status == KnowledgeStatus.ACTIVE.value:
                    stats.active += 1
                elif item.status == KnowledgeStatus.ARCHIVED.value:
                    stats.archived += 1
                elif item.status == KnowledgeStatus.EXPIRED.value:
                    stats.expired += 1
                elif item.status == KnowledgeStatus.DEPRECATED.value:
                    stats.deprecated += 1
            
            if stats.total > 0:
                total_conf = sum(item.confidence for item in self._knowledge.values())
                stats.avg_confidence = round(total_conf / stats.total, 2)
            
            try:
                week_ago = datetime.now() - timedelta(days=7)
                stats.recently_added = sum(
                    1 for item in self._knowledge.values()
                    if datetime.fromisoformat(item.created_at) > week_ago
                )
            except Exception:
                stats.recently_added = 0
            
            self._stats = stats

    # ============================================================
    # EXPORT / IMPORT
    # ============================================================

    def export(self, file_path: Optional[Path] = None) -> bool:
        try:
            file_path = file_path or DATA_DIR / f"knowledge_export_{datetime.now().strftime('%Y%m%d')}.json"
            
            with self.lock:
                data = {
                    "version": self.VERSION,
                    "exported_at": datetime.now().isoformat(),
                    "items": {
                        item_id: item.to_dict()
                        for item_id, item in self._knowledge.items()
                    },
                    "states": self._state_cache,
                }
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=safe_serialize)
            
            logger.info("Knowledge exported: %s", file_path)
            return True
            
        except Exception as e:
            logger.error("Export failed: %s", e)
            return False

    def import_from_file(self, file_path: Path) -> int:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            items = data.get("items", {})
            states = data.get("states", {})
            count = 0
            
            for item_id, item_data in items.items():
                if item_id not in self._knowledge:
                    item = KnowledgeItem(**item_data)
                    self._knowledge[item_id] = item
                    count += 1
            
            self._state_cache.update(states)
            
            self._build_index()
            self.save()
            self._update_stats()
            
            logger.info("Imported %d items and %d states from %s", count, len(states), file_path)
            return count
            
        except Exception as e:
            logger.error("Import failed: %s", e)
            return 0

    # ============================================================
    # BACKUP
    # ============================================================

    def backup(self) -> Optional[Path]:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = KNOWLEDGE_BACKUP_DIR / f"knowledge_backup_{timestamp}.json"
            
            if self.export(backup_file):
                self._last_backup = datetime.now().isoformat()
                self._clean_backups()
                return backup_file
            
            return None
            
        except Exception as e:
            logger.error("Backup failed: %s", e)
            return None

    def _clean_backups(self, keep: int = 10) -> None:
        try:
            backups = sorted(KNOWLEDGE_BACKUP_DIR.glob("knowledge_backup_*.json"))
            for backup in backups[:-keep]:
                backup.unlink()
                logger.debug("Removed old backup: %s", backup)
                
        except Exception as e:
            logger.warning("Backup cleanup failed: %s", e)

    def _start_auto_backup(self) -> None:
        def backup_loop():
            while True:
                time.sleep(self.auto_backup_interval)
                try:
                    self.backup()
                except Exception as e:
                    logger.debug("Auto-backup failed: %s", e)
        
        thread = threading.Thread(target=backup_loop, daemon=True)
        thread.start()

    # ============================================================
    # MAINTENANCE
    # ============================================================

    def cleanup(self, days: int = 30) -> int:
        count = 0
        try:
            with self.lock:
                to_delete = []
                
                for item_id, item in self._knowledge.items():
                    if item.expires_at:
                        try:
                            expires = datetime.fromisoformat(item.expires_at)
                            if datetime.now() > expires:
                                to_delete.append(item_id)
                                continue
                        except Exception:
                            pass
                    
                    if item.accessed_at:
                        try:
                            accessed = datetime.fromisoformat(item.accessed_at)
                            if (datetime.now() - accessed).days > days:
                                item.status = KnowledgeStatus.ARCHIVED.value
                                count += 1
                        except Exception:
                            pass
                
                for item_id in to_delete:
                    self.delete(item_id, permanent=True)
                    count += 1
            
            self.save()
            self._update_stats()
            
            logger.info("Cleanup completed: %d items affected", count)
            return count
            
        except Exception as e:
            logger.error("Cleanup failed: %s", e)
            return 0

    def deduplicate(self) -> int:
        count = 0
        try:
            seen = {}
            
            with self.lock:
                for item_id, item in list(self._knowledge.items()):
                    content_hash = hashlib.md5(item.content.encode()).hexdigest()
                    
                    if content_hash in seen:
                        existing = seen[content_hash]
                        if item.confidence > existing.confidence:
                            self.delete(existing.id, permanent=True)
                            seen[content_hash] = item
                        else:
                            self.delete(item_id, permanent=True)
                        count += 1
                    else:
                        seen[content_hash] = item
            
            self.save()
            self._update_stats()
            
            logger.info("Deduplication: %d items removed", count)
            return count
            
        except Exception as e:
            logger.error("Deduplication failed: %s", e)
            return 0

    # ============================================================
    # ANALYTICS
    # ============================================================

    def get_analytics(self) -> Dict[str, Any]:
        try:
            with self.lock:
                category_dist = {
                    cat: len(items)
                    for cat, items in self._categories.items()
                }
                
                tag_dist = {
                    tag: len(items)
                    for tag, items in self._tags.items()
                }
                
                confidence_levels = {
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                }
                
                for item in self._knowledge.values():
                    if item.confidence >= 80:
                        confidence_levels["high"] += 1
                    elif item.confidence >= 50:
                        confidence_levels["medium"] += 1
                    else:
                        confidence_levels["low"] += 1
                
                return {
                    "total": len(self._knowledge),
                    "states": len(self._state_cache),
                    "categories": category_dist,
                    "tags": tag_dist,
                    "confidence": confidence_levels,
                    "avg_confidence": self._stats.avg_confidence,
                    "access_count": self._stats.total_access,
                    "active": self._stats.active,
                    "archived": self._stats.archived,
                    "expired": self._stats.expired,
                    "deprecated": self._stats.deprecated,
                    "recently_added": self._stats.recently_added,
                    "last_backup": self._last_backup,
                    "timestamp": datetime.now().isoformat(),
                }
                
        except Exception as e:
            logger.error("Analytics failed: %s", e)
            return {"error": str(e)}

    # ============================================================
    # UTILITY
    # ============================================================

    def all(self) -> List[KnowledgeItem]:
        with self.lock:
            return list(self._knowledge.values())

    def get_categories(self) -> List[str]:
        with self.lock:
            return list(self._categories.keys())

    def get_tags(self) -> List[str]:
        with self.lock:
            return list(self._tags.keys())

    def clear(self, clear_states: bool = True) -> bool:
        try:
            with self.lock:
                self._knowledge.clear()
                self._categories.clear()
                self._tags.clear()
                self._index.clear()
                if clear_states:
                    self._state_cache.clear()
            
            self.save()
            self._update_stats()
            logger.info("Knowledge cleared")
            return True
            
        except Exception as e:
            logger.error("Clear failed: %s", e)
            return False


# ============================================================
# GLOBAL INSTANCE
# ============================================================

knowledge = KnowledgeEngine()


# ============================================================
# COMPATIBILITY FUNCTIONS
# ============================================================

def add_knowledge(content: str, category: str = "general") -> bool:
    return knowledge.add(content, category) is not None


def search_knowledge(keyword: str) -> List[Dict]:
    results = knowledge.search(keyword)
    return [item.to_dict() for item in results]


def get_knowledge_stats() -> Dict:
    stats = knowledge.stats()
    return {
        "total": stats.total,
        "states": stats.state_count,
        "file": str(KNOWLEDGE_FILE),
    }


def store_state(state: Any, metadata: Optional[Dict] = None) -> str:
    return knowledge.store_state(state, metadata)


def get_state(state_key: str) -> Optional[Dict]:
    return knowledge.get_state(state_key)


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "KnowledgeEngine",
    "KnowledgeItem",
    "KnowledgeStats",
    "KnowledgeCategory",
    "KnowledgeStatus",
    "KnowledgeType",
    "safe_key",
    "safe_hash",
    "safe_dict",
    "safe_serialize",
    "knowledge",
    "add_knowledge",
    "search_knowledge",
    "get_knowledge_stats",
    "store_state",
    "get_state",
    "KNOWLEDGE_VERSION",
    "DATA_DIR",
    "KNOWLEDGE_FILE",
]


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    print()
    print("=" * 70)
    print("  KNOWLEDGE ENGINE v3.1 - SELF TEST (FIXED)")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        test_knowledge = KnowledgeEngine()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Add
    print("\n2. Testing add...")
    try:
        item_id = knowledge.add("Test knowledge content", "test", "fact", ["test", "example"])
        if item_id:
            results["add"] = {"status": "PASS", "id": item_id}
            tests_passed += 1
            print(f"   ✅ Add passed (ID: {item_id})")
        else:
            results["add"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Add failed")
    except Exception as e:
        results["add"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Add failed: {e}")
    
    # Test 3: State Storage
    print("\n3. Testing state storage...")
    try:
        class MockState:
            def __init__(self):
                self.id = "test_123"
                self.status = "ACTIVE"
                self.confidence = 75.5
                self.data = {"key": "value"}
        
        state = MockState()
        state_key = knowledge.store_state(state, {"test": "metadata"})
        
        if state_key:
            results["state_storage"] = {"status": "PASS", "key": state_key}
            tests_passed += 1
            print(f"   ✅ State storage passed (Key: {state_key[:8]})")
        else:
            results["state_storage"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ State storage failed")
    except Exception as e:
        results["state_storage"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ State storage failed: {e}")
    
    # Summary
    print()
    print("=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"  ✅ Passed: {tests_passed}")
    print(f"  ❌ Failed: {tests_failed}")
    print(f"  📊 Total:  {tests_passed + tests_failed}")
    print("=" * 70)
    
    return {
        "module": "knowledge",
        "version": KNOWLEDGE_VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    
    result = self_test()
    
    print()
    print("=" * 70)
    print("  KNOWLEDGE ENGINE v3.1 - SELF TEST COMPLETE")
    print("=" * 70)
    print()
    print("Final Status:", result["status"])
    print("Tests Passed:", result["tests_passed"])
    print("Tests Failed:", result["tests_failed"])


# ============================================================
# END
# ============================================================