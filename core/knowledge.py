# ============================================================
# INKSIDE DIGITAL - KNOWLEDGE ENGINE v2.0.0
# UNLIMITED MEMORY ARCHITECTURE
# SELF-MANAGING WITH AUTO-CLEANUP
# ============================================================

from __future__ import annotations

import json
import logging
import threading
import hashlib
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
from dataclasses import dataclass, field, is_dataclass
from enum import Enum

logger = logging.getLogger(__name__)

# ============================================================
# VERSION
# ============================================================

KNOWLEDGE_VERSION = "2.0.0"

# ============================================================
# PATHS
# ============================================================

DATA_DIR = Path("database")
DATA_DIR.mkdir(exist_ok=True)

KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"
KNOWLEDGE_INDEX_FILE = DATA_DIR / "knowledge_index.json"
KNOWLEDGE_BACKUP_DIR = DATA_DIR / "knowledge_backups"
KNOWLEDGE_BACKUP_DIR.mkdir(exist_ok=True)
STATE_CACHE_FILE = DATA_DIR / "state_cache.json"

# ============================================================
# DEFAULTS
# ============================================================

# ❌ TIDAK ADA LIMIT ITEMS - UNLIMITED!
DEFAULT_MAX_ITEMS = None  # Unlimited

# Config untuk auto-cleanup
DEFAULT_CONFIDENCE_DECAY = 0.01
DEFAULT_CONFIDENCE_MIN = 0.0
DEFAULT_CONFIDENCE_MAX = 100.0
DEFAULT_SIMILARITY_THRESHOLD = 0.7
DEFAULT_EXPIRATION_DAYS = 365
DEFAULT_AUTO_BACKUP_INTERVAL = 86400  # 24 jam

# Threshold untuk aggressive cleanup
CLEANUP_CONFIDENCE_THRESHOLD = 30.0  # Hapus jika confidence < 30%
CLEANUP_ACCESS_DAYS = 90  # Hapus jika tidak diakses > 90 hari
CLEANUP_IMPORTANCE_THRESHOLD = 0.3  # Hapus jika importance < 0.3
MAX_BACKUP_FILES = 5  # Simpan 5 backup terakhir
MAX_DATABASE_SIZE_MB = 5000  # 5GB max

# ============================================================
# ENUMS
# ============================================================

class KnowledgeCategory(Enum):
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
    COGNITIVE = "cognitive"
    FOOD = "food"
    SCIENCE = "science"
    HEALTH = "health"
    TECHNOLOGY = "technology"
    GENERAL_KNOWLEDGE = "general_knowledge"

class KnowledgeStatus(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"
    EXPIRED = "expired"
    PENDING = "pending"
    REVIEW = "review"

class KnowledgeType(Enum):
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
    COGNITIVE = "cognitive"
    RECIPE = "recipe"
    QA = "qa"

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class KnowledgeItem:
    """Single knowledge item - UNLIMITED."""
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
    database_size_mb: float = 0.0

# ============================================================
# SAFE SERIALIZATION HELPERS
# ============================================================

def safe_key(obj: Any) -> str:
    """Convert any object to safe string key."""
    if obj is None:
        return "none"
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (int, float, bool)):
        return str(obj)
    if isinstance(obj, Enum):
        return f"{obj.__class__.__name__}_{obj.value}"
    if is_dataclass(obj):
        try:
            return f"dataclass_{type(obj).__name__}_{id(obj)}"
        except:
            return f"dataclass_{type(obj).__name__}_{id(obj)}"
    if hasattr(obj, '__dict__'):
        return f"{type(obj).__name__}_{id(obj)}"
    return str(obj)

def safe_serialize(obj: Any) -> Any:
    """Safely serialize any object for JSON."""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {safe_key(k): safe_serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [safe_serialize(item) for item in obj]
    if isinstance(obj, Enum):
        return obj.value
    if is_dataclass(obj):
        return safe_serialize(obj.__dict__ if hasattr(obj, '__dict__') else str(obj))
    if hasattr(obj, '__dict__'):
        return safe_serialize(obj.__dict__)
    return str(obj)

# ============================================================
# MAIN KNOWLEDGE ENGINE - UNLIMITED
# ============================================================

class KnowledgeEngine:
    """
    Knowledge Engine v4.0.0 - UNLIMITED MEMORY.
    Self-managing with aggressive auto-cleanup.
    No limits - only smart cleanup.
    """

    VERSION = KNOWLEDGE_VERSION

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.lock = threading.RLock()
        
        # ❌ NO LIMITS - UNLIMITED
        self.max_items = None  # Unlimited!
        
        # Configuration
        self.confidence_decay = self.config.get("confidence_decay", DEFAULT_CONFIDENCE_DECAY)
        self.similarity_threshold = self.config.get("similarity_threshold", DEFAULT_SIMILARITY_THRESHOLD)
        self.expiration_days = self.config.get("expiration_days", DEFAULT_EXPIRATION_DAYS)
        self.auto_backup_interval = self.config.get("auto_backup_interval", DEFAULT_AUTO_BACKUP_INTERVAL)
        
        # Storage
        self._knowledge: Dict[str, KnowledgeItem] = {}
        self._categories: Dict[str, List[str]] = {}
        self._tags: Dict[str, List[str]] = {}
        self._index: Dict[str, Set[str]] = {}
        self._state_cache: Dict[str, Dict] = {}
        
        # Stats
        self._stats = KnowledgeStats()
        self._last_backup: Optional[str] = None
        self._initialized = False
        
        # Load data
        self.load()
        self._build_index()
        
        # Start auto-backup
        if self.config.get("auto_backup", True):
            self._start_auto_backup()
        
        self._initialized = True
        self._update_stats()
        self._log_status()
        
        logger.info(f"🧠 Knowledge Engine v{self.VERSION} initialized")
        logger.info(f"   📚 Items: {len(self._knowledge)} (UNLIMITED)")
        logger.info(f"   💾 States: {len(self._state_cache)}")
        logger.info(f"   📦 Size: {self._get_database_size_mb():.2f} MB")

    # ============================================================
    # DATABASE SIZE MANAGEMENT
    # ============================================================

    def _get_database_size_mb(self) -> float:
        """Get current database size in MB."""
        total_size = 0
        if KNOWLEDGE_FILE.exists():
            total_size += KNOWLEDGE_FILE.stat().st_size
        if STATE_CACHE_FILE.exists():
            total_size += STATE_CACHE_FILE.stat().st_size
        return total_size / (1024 * 1024)

    def auto_manage_size(self, max_size_mb: float = MAX_DATABASE_SIZE_MB) -> Dict[str, Any]:
        """Auto-manage database size. Run aggressive cleanup if exceeded."""
        current_size = self._get_database_size_mb()
        
        result = {
            "size_mb": current_size,
            "max_size_mb": max_size_mb,
            "exceeded": current_size > max_size_mb,
            "items_removed": 0,
            "action": "none"
        }
        
        if current_size > max_size_mb:
            logger.warning(f"⚠️ Database exceeds {max_size_mb} MB ({current_size:.2f} MB)")
            logger.info("🧹 Running aggressive cleanup...")
            
            removed = self.aggressive_cleanup()
            result["items_removed"] = removed
            result["action"] = "aggressive_cleanup"
            
            # Save after cleanup
            self.save()
            
            # Check new size
            new_size = self._get_database_size_mb()
            result["new_size_mb"] = new_size
            logger.info(f"✅ Database reduced to {new_size:.2f} MB ({removed} items removed)")
        
        return result

    # ============================================================
    # AGGRESSIVE CLEANUP - CORE FEATURE
    # ============================================================

    def aggressive_cleanup(self) -> int:
        """
        Aggressive cleanup - removes low-quality items.
        - Confidence < 30%
        - Not accessed > 90 days
        - Importance < 0.3
        - Expired items
        """
        count = 0
        try:
            with self.lock:
                to_delete = []
                now = datetime.now()
                
                for item_id, item in self._knowledge.items():
                    should_delete = False
                    reasons = []
                    
                    # 1. Confidence terlalu rendah
                    if item.confidence < CLEANUP_CONFIDENCE_THRESHOLD:
                        should_delete = True
                        reasons.append(f"confidence={item.confidence:.1f}%")
                    
                    # 2. Tidak diakses > 90 hari
                    if item.accessed_at:
                        try:
                            accessed = datetime.fromisoformat(item.accessed_at)
                            if (now - accessed).days > CLEANUP_ACCESS_DAYS:
                                should_delete = True
                                reasons.append(f"not_accessed_{CLEANUP_ACCESS_DAYS}d")
                        except:
                            pass
                    
                    # 3. Importance rendah
                    if item.importance < CLEANUP_IMPORTANCE_THRESHOLD:
                        should_delete = True
                        reasons.append(f"importance={item.importance:.2f}")
                    
                    # 4. Sudah expired
                    if item.expires_at:
                        try:
                            expires = datetime.fromisoformat(item.expires_at)
                            if now > expires:
                                should_delete = True
                                reasons.append("expired")
                        except:
                            pass
                    
                    if should_delete:
                        to_delete.append((item_id, reasons))
                
                for item_id, reasons in to_delete:
                    self._delete_internal(item_id, permanent=True)
                    count += 1
                    logger.debug(f"🧹 Removed: {item_id[:8]} ({', '.join(reasons)})")
            
            if count > 0:
                self.save()
                self._build_index()
                self._update_stats()
                logger.info(f"🧹 Aggressive cleanup: {count} items removed")
            else:
                logger.debug("🧹 Aggressive cleanup: no items to remove")
            
            return count
            
        except Exception as e:
            logger.error(f"❌ Aggressive cleanup failed: {e}")
            return 0

    def _delete_internal(self, item_id: str, permanent: bool = True) -> bool:
        """Internal delete without extra save."""
        try:
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
                
                # Remove from index
                for word in self._extract_keywords(item.content):
                    if word in self._index and item_id in self._index[word]:
                        self._index[word].remove(item_id)
                
                del self._knowledge[item_id]
            else:
                item.status = KnowledgeStatus.ARCHIVED.value
                item.updated_at = datetime.now().isoformat()
            
            return True
            
        except Exception as e:
            logger.error(f"Delete internal error: {e}")
            return False

    # ============================================================
    # LOAD / SAVE
    # ============================================================

    def load(self) -> bool:
        """Load knowledge from storage."""
        try:
            if KNOWLEDGE_FILE.exists():
                with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    for item_id, item_data in data.items():
                        if isinstance(item_data, dict):
                            try:
                                self._knowledge[item_id] = KnowledgeItem(**item_data)
                            except Exception as e:
                                logger.warning(f"Failed to load item {item_id}: {e}")
            
            if STATE_CACHE_FILE.exists():
                with open(STATE_CACHE_FILE, "r", encoding="utf-8") as f:
                    try:
                        self._state_cache = json.load(f)
                    except Exception as e:
                        logger.warning(f"Failed to load state cache: {e}")
                        self._state_cache = {}
            
            self._build_index()
            self._update_stats()
            
            logger.info(f"✅ Knowledge loaded: {len(self._knowledge)} items, {len(self._state_cache)} states")
            return True
            
        except Exception as e:
            logger.error(f"❌ Knowledge load failed: {e}")
            return False

    def save(self) -> bool:
        """Save knowledge to storage with safe serialization."""
        try:
            with self.lock:
                # Save knowledge
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
                
                # Save state cache
                safe_state_cache = {}
                for key, value in self._state_cache.items():
                    try:
                        safe_state_cache[key] = safe_serialize(value)
                    except Exception as e:
                        logger.warning(f"Failed to serialize state {key}: {e}")
                        safe_state_cache[key] = {"error": str(e), "key": str(key)}
                
                with open(STATE_CACHE_FILE, "w", encoding="utf-8") as f:
                    json.dump(safe_state_cache, f, indent=2, ensure_ascii=False, default=safe_serialize)
                
                self._save_index()
            
            logger.debug(f"💾 Saved: {len(self._knowledge)} items, {len(self._state_cache)} states")
            return True
            
        except Exception as e:
            logger.error(f"❌ Save failed: {e}")
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
            logger.warning(f"Index save failed: {e}")

    def _build_index(self) -> None:
        """Build search index."""
        with self.lock:
            self._categories = {}
            self._tags = {}
            self._index = {}
            
            for item_id, item in self._knowledge.items():
                if item.category not in self._categories:
                    self._categories[item.category] = []
                self._categories[item.category].append(item_id)
                
                for tag in item.tags:
                    if tag not in self._tags:
                        self._tags[tag] = []
                    self._tags[tag].append(item_id)
                
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
    # KNOWLEDGE MANAGEMENT - UNLIMITED
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
        expires_in_days: Optional[int] = None
    ) -> Optional[str]:
        """
        Add new knowledge item. UNLIMITED - no max limit!
        """
        if not content:
            logger.warning("Empty knowledge content")
            return None
        
        try:
            with self.lock:
                item_id = self._generate_id(content)
                
                # Check if exists
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
                    if expires_in_days:
                        item.expires_at = (datetime.now() + timedelta(days=expires_in_days)).isoformat()
                    return item_id
                
                # New item
                expires_at = None
                if expires_in_days:
                    expires_at = (datetime.now() + timedelta(days=expires_in_days)).isoformat()
                
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
                    expires_at=expires_at,
                )
                
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
            
            logger.debug(f"📚 Added: {item_id[:8]} ({category})")
            return item_id
            
        except Exception as e:
            logger.error(f"❌ Add failed: {e}")
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
            logger.error(f"❌ Update failed: {e}")
            return False

    def delete(self, item_id: str, permanent: bool = False) -> bool:
        try:
            with self.lock:
                success = self._delete_internal(item_id, permanent)
            
            if success and permanent:
                self.save()
                self._build_index()
                self._update_stats()
            elif success:
                self.save()
                self._update_stats()
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Delete failed: {e}")
            return False

    def all(self) -> List[KnowledgeItem]:
        with self.lock:
            return list(self._knowledge.values())

    # ============================================================
    # STATE MANAGEMENT
    # ============================================================

    def store_state(self, state: Any, metadata: Optional[Dict] = None) -> str:
        """Store any state object."""
        try:
            state_key = safe_key(state)
            state_data = self._extract_state_data(state)
            
            if metadata is None:
                metadata = {}
            elif not isinstance(metadata, dict):
                metadata = {"value": str(metadata)}
            
            if not isinstance(state_data, dict):
                state_data = {"__value__": str(state_data)}
            
            with self.lock:
                self._state_cache[state_key] = {
                    'state_key': state_key,
                    'state_type': type(state).__name__,
                    'data': state_data,
                    'metadata': metadata,
                    'timestamp': datetime.now().isoformat(),
                    'access_count': 0,
                }
                
                content = self._format_state_content(state, state_data)
                safe_metadata = {
                    'state_key': state_key,
                    'state_type': type(state).__name__,
                    'timestamp': datetime.now().isoformat(),
                }
                
                self.add(
                    content=content,
                    category=KnowledgeCategory.STATE.value,
                    type=KnowledgeType.STATE.value,
                    tags=['state', type(state).__name__.lower()],
                    confidence=50.0,
                    importance=0.5,
                    metadata=safe_metadata,
                )
                
                self._stats.state_count = len(self._state_cache)
            
            self.save()
            logger.debug(f"💾 State stored: {state_key[:8]} ({type(state).__name__})")
            return state_key
            
        except Exception as e:
            logger.error(f"❌ Store state failed: {e}")
            fallback_key = f"state_{id(state)}_{int(time.time())}"
            self._state_cache[fallback_key] = {
                'state_key': fallback_key,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
            }
            return fallback_key

    def get_state(self, state_key: str) -> Optional[Dict]:
        with self.lock:
            result = self._state_cache.get(state_key)
            if result:
                result['access_count'] = result.get('access_count', 0) + 1
            return result

    def get_all_states(self) -> List[Dict]:
        with self.lock:
            return list(self._state_cache.values())

    def _extract_state_data(self, state: Any) -> Dict[str, Any]:
        if is_dataclass(state):
            return {k: safe_serialize(v) for k, v in state.__dict__.items() if not k.startswith('_')}
        if hasattr(state, '__dict__'):
            return {k: safe_serialize(v) for k, v in state.__dict__.items() if not k.startswith('_')}
        return {"__value__": safe_serialize(state)}

    def _format_state_content(self, state: Any, data: Dict) -> str:
        try:
            state_type = type(state).__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = f"[{timestamp}] Cognitive State: {state_type}\n"
            content += f"Type: {state_type}\n"
            
            important_keys = ['state', 'status', 'mode', 'phase', 'confidence', 
                            'level', 'active', 'running', 'current', 'cycle']
            
            for key in important_keys:
                if key in data:
                    value = data[key]
                    if isinstance(value, (str, int, float, bool)):
                        content += f"{key}: {value}\n"
            
            return content
            
        except Exception as e:
            return f"Cognitive State at {datetime.now().isoformat()}"

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.0,
        max_results: Optional[int] = None,  # ✅ Unlimited
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
                final_results = [{
                    'item': item,
                    'score': score,
                    'state': state_data
                } for item, score, state_data in results]
            else:
                results.sort(key=lambda x: (x[1], x[0].confidence), reverse=True)
                final_results = [item for item, _ in results]
            
            # ✅ UNLIMITED - no max_results limit
            return final_results
        
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
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
        except:
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
            logger.error(f"❌ Reinforce failed: {e}")
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
            logger.error(f"❌ Decay failed: {e}")
            return False

    # ============================================================
    # BACKUP
    # ============================================================

    def backup(self) -> Optional[Path]:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = KNOWLEDGE_BACKUP_DIR / f"knowledge_backup_{timestamp}.json"
            
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
            
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=safe_serialize)
            
            self._last_backup = datetime.now().isoformat()
            self._clean_backups(keep=MAX_BACKUP_FILES)
            
            logger.debug(f"💾 Backup created: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return None

    def _clean_backups(self, keep: int = MAX_BACKUP_FILES) -> None:
        """Keep only latest N backups."""
        try:
            backups = sorted(KNOWLEDGE_BACKUP_DIR.glob("knowledge_backup_*.json"))
            for backup in backups[:-keep]:
                backup.unlink()
                logger.debug(f"🧹 Removed old backup: {backup}")
                
        except Exception as e:
            logger.warning(f"Backup cleanup failed: {e}")

    def _start_auto_backup(self) -> None:
        def backup_loop():
            while True:
                time.sleep(self.auto_backup_interval)
                try:
                    self.backup()
                except Exception as e:
                    logger.debug(f"Auto-backup failed: {e}")
        
        thread = threading.Thread(target=backup_loop, daemon=True)
        thread.start()

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
            stats.database_size_mb = self._get_database_size_mb()
            
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
            except:
                stats.recently_added = 0
            
            self._stats = stats

    def _log_status(self) -> None:
        """Log current status."""
        stats = self._stats
        logger.info(f"📊 Knowledge Status:")
        logger.info(f"   Total: {stats.total} (UNLIMITED)")
        logger.info(f"   States: {stats.state_count}")
        logger.info(f"   Active: {stats.active}")
        logger.info(f"   Archived: {stats.archived}")
        logger.info(f"   Avg Confidence: {stats.avg_confidence}%")
        logger.info(f"   Database Size: {stats.database_size_mb:.2f} MB")

    # ============================================================
    # UTILITY
    # ============================================================

    def get_categories(self) -> List[str]:
        with self.lock:
            return list(self._categories.keys())

    def get_tags(self) -> List[str]:
        with self.lock:
            return list(self._tags.keys())

    def deduplicate(self) -> int:
        """Remove duplicate items."""
        count = 0
        try:
            seen = {}
            with self.lock:
                for item_id, item in list(self._knowledge.items()):
                    content_hash = hashlib.md5(item.content.encode()).hexdigest()
                    if content_hash in seen:
                        existing = seen[content_hash]
                        if item.confidence > existing.confidence:
                            self._delete_internal(existing.id, permanent=True)
                            seen[content_hash] = item
                        else:
                            self._delete_internal(item_id, permanent=True)
                        count += 1
                    else:
                        seen[content_hash] = item
            
            if count > 0:
                self.save()
                self._build_index()
                self._update_stats()
            
            return count
            
        except Exception as e:
            logger.error(f"❌ Deduplicate failed: {e}")
            return 0

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
            logger.info("🧹 Knowledge cleared")
            return True
            
        except Exception as e:
            logger.error(f"❌ Clear failed: {e}")
            return False

# ============================================================
# GLOBAL INSTANCE
# ============================================================

knowledge = KnowledgeEngine()

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
    "knowledge",
    "KNOWLEDGE_VERSION",
    "DATA_DIR",
    "KNOWLEDGE_FILE",
]
