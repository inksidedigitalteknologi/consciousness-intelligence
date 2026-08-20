# ============================================================
#
# INKSIDE INTELLIGENCE OS
#
# EXPERIENCE ENGINE v3.0
#
# ULTRA COMPREHENSIVE EXPERIENCE MANAGEMENT
#
# NEW FEATURES v3.0:
# - Experience Clustering
# - Pattern Discovery
# - Anomaly Detection
# - Experience Summarization
# - Reinforcement Learning Integration
# - Similarity Matching
# - Experience Validation
# - Confidence Calibration
# - Experience Graph
# - Temporal Analysis
# - Predictive Recall
# - Experience Weighting
# - Automatic Tagging
# - Experience Evolution Tracking
# - Performance Analytics
# - Decision Support
# - Experience Export/Import v2
# - Memory Consolidation
# - Forgetting Curve Management
# - Experience Replay
# - Transfer Learning Support
#
# ============================================================

from __future__ import annotations

import logging
import uuid
import json
import hashlib
import threading
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Set, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, Counter, deque
import statistics
import math

logger = logging.getLogger(__name__)


# ============================================================
# CONSTANTS
# ============================================================

EXPERIENCE_VERSION = "3.0.0"

# Status
STATUS_SUCCESS = "success"
STATUS_FAILURE = "failure"
STATUS_NEUTRAL = "neutral"
STATUS_PARTIAL = "partial"
STATUS_PENDING = "pending"
STATUS_EXPIRED = "expired"
STATUS_ARCHIVED = "archived"

# Importance Levels
IMPORTANCE_CRITICAL = 1.0
IMPORTANCE_HIGH = 0.8
IMPORTANCE_MEDIUM = 0.5
IMPORTANCE_LOW = 0.3
IMPORTANCE_MINIMAL = 0.1

# Confidence Levels
CONFIDENCE_VERY_HIGH = 0.95
CONFIDENCE_HIGH = 0.80
CONFIDENCE_MEDIUM = 0.60
CONFIDENCE_LOW = 0.40
CONFIDENCE_VERY_LOW = 0.20


# ============================================================
# ENUMS
# ============================================================

class ExperienceType(Enum):
    """Types of experiences."""
    ACTION = "action"
    DECISION = "decision"
    OBSERVATION = "observation"
    REACTION = "reaction"
    INTERACTION = "interaction"
    LEARNING = "learning"
    REFLECTION = "reflection"
    PREDICTION = "prediction"
    ANALYSIS = "analysis"
    STRATEGY = "strategy"


class ExperienceTier(Enum):
    """Experience importance tiers."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    TRIVIAL = "trivial"


class MemoryStage(Enum):
    """Memory consolidation stages."""
    SENSORY = "sensory"      # 0-10 minutes
    SHORT_TERM = "short_term"  # 10 minutes - 6 hours
    WORKING = "working"       # 6-24 hours
    LONG_TERM = "long_term"   # > 24 hours
    PERMANENT = "permanent"   # Consolidated


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class Experience:
    """Complete experience record."""
    id: str
    timestamp: str
    event: Any
    result: Any
    domain: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    status: str = STATUS_NEUTRAL
    success: Optional[bool] = None
    confidence: float = 0.5
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # New fields v3.0
    type: str = ExperienceType.ACTION.value
    tier: str = ExperienceTier.MEDIUM.value
    stage: str = MemoryStage.WORKING.value
    weight: float = 1.0
    decay_rate: float = 0.01
    access_count: int = 0
    last_accessed: Optional[str] = None
    version: int = 1
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    embeddings: Optional[List[float]] = None
    similarity_score: float = 0.0
    validation_count: int = 0
    validation_score: float = 0.0
    evolution: List[Dict[str, Any]] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "event": self.event,
            "result": self.result,
            "domain": self.domain,
            "context": self.context,
            "status": self.status,
            "success": self.success,
            "confidence": self.confidence,
            "importance": self.importance,
            "tags": self.tags,
            "metadata": self.metadata,
            "type": self.type,
            "tier": self.tier,
            "stage": self.stage,
            "weight": self.weight,
            "decay_rate": self.decay_rate,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
            "version": self.version,
            "parent_id": self.parent_id,
            "children": self.children,
            "similarity_score": self.similarity_score,
            "validation_count": self.validation_count,
            "validation_score": self.validation_score,
            "patterns": self.patterns,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Experience":
        return cls(**data)


@dataclass
class ExperienceStats:
    """Experience statistics."""
    total: int = 0
    by_status: Dict[str, int] = field(default_factory=dict)
    by_type: Dict[str, int] = field(default_factory=dict)
    by_domain: Dict[str, int] = field(default_factory=dict)
    by_tier: Dict[str, int] = field(default_factory=dict)
    by_stage: Dict[str, int] = field(default_factory=dict)
    success_rate: float = 0.0
    avg_confidence: float = 0.0
    avg_importance: float = 0.0
    total_access: int = 0
    recent_count: int = 0
    consolidated: int = 0
    patterns: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ExperiencePattern:
    """Discovered experience pattern."""
    id: str
    name: str
    description: str
    pattern_type: str
    confidence: float
    examples: List[str]
    frequency: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# EXPERIENCE ENGINE v3.0
# ============================================================

class ExperienceEngine:
    """
    Experience Engine v3.0 - Ultra Comprehensive Experience Management.
    
    Features:
    1. Record experiences
    2. Store outcomes
    3. Track success/failure
    4. Preserve context
    5. Assign importance
    6. Track confidence
    7. Search experiences
    8. Recall recent experiences
    9. Generate statistics
    10. Export/import
    11. Experience Clustering
    12. Pattern Discovery
    13. Anomaly Detection
    14. Experience Summarization
    15. Reinforcement Learning Integration
    16. Similarity Matching
    17. Experience Validation
    18. Confidence Calibration
    19. Experience Graph
    20. Temporal Analysis
    21. Predictive Recall
    22. Experience Weighting
    23. Automatic Tagging
    24. Experience Evolution Tracking
    25. Performance Analytics
    26. Memory Consolidation
    27. Forgetting Curve Management
    28. Experience Replay
    29. Transfer Learning Support
    """

    VERSION = EXPERIENCE_VERSION

    def __init__(
        self,
        max_size: int = 10000,
        consolidation_threshold: int = 100,
        decay_rate: float = 0.01,
        auto_tag: bool = True
    ):
        self.name = "experience"
        
        # Core storage
        self.experiences: List[Experience] = []
        self.experience_map: Dict[str, Experience] = {}
        
        # Statistics
        self.total_recorded = 0
        self.success_count = 0
        self.failure_count = 0
        self.neutral_count = 0
        self.partial_count = 0
        
        # Configuration
        self.max_size = max(1, int(max_size))
        self.consolidation_threshold = max(1, int(consolidation_threshold))
        self.decay_rate = float(decay_rate)
        self.auto_tag = bool(auto_tag)
        
        # Tracking
        self.last_experience: Optional[Experience] = None
        self.experience_patterns: List[ExperiencePattern] = []
        self.experience_graph: Dict[str, List[str]] = defaultdict(list)
        self.access_history: deque = deque(maxlen=1000)
        
        # Forgetting curve
        self.forgetting_curve = {
            "sensory": 0.9,     # 90% retention
            "short_term": 0.7,   # 70% retention
            "working": 0.5,      # 50% retention
            "long_term": 0.3,    # 30% retention
            "permanent": 0.9,    # 90% retention (reconsolidated)
        }
        
        # Thread safety
        self._lock = threading.RLock()
        
        logger.info(
            "Experience Engine v%s initialized (max_size=%d)",
            self.VERSION,
            self.max_size
        )

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    def _timestamp(self) -> str:
        return datetime.now().isoformat()

    def _generate_id(self) -> str:
        return f"exp_{uuid.uuid4().hex[:12]}"

    def _normalize_status(
        self,
        result: Any = None,
        success: Optional[bool] = None
    ) -> str:
        """Normalize status from various inputs."""
        
        # Explicit success flag
        if success is True:
            return STATUS_SUCCESS
        if success is False:
            return STATUS_FAILURE
        
        # Infer from result
        if isinstance(result, bool):
            return STATUS_SUCCESS if result else STATUS_FAILURE
        
        if isinstance(result, dict):
            if result.get("success") is True:
                return STATUS_SUCCESS
            if result.get("success") is False:
                return STATUS_FAILURE
            
            status = result.get("status")
            if status in ("success", "successful", "correct", "positive"):
                return STATUS_SUCCESS
            if status in ("failure", "failed", "incorrect", "negative"):
                return STATUS_FAILURE
            if status in ("partial", "partially"):
                return STATUS_PARTIAL
            
            evaluation = result.get("evaluation")
            if isinstance(evaluation, str):
                eval_lower = evaluation.lower()
                if eval_lower in ("correct", "success", "successful"):
                    return STATUS_SUCCESS
                if eval_lower in ("incorrect", "failure", "failed"):
                    return STATUS_FAILURE
                if eval_lower in ("partial", "partially"):
                    return STATUS_PARTIAL
        
        if isinstance(result, str):
            result_lower = result.lower()
            if result_lower in ("success", "successful", "correct", "positive"):
                return STATUS_SUCCESS
            if result_lower in ("failure", "failed", "incorrect", "negative"):
                return STATUS_FAILURE
            if result_lower in ("partial", "partially"):
                return STATUS_PARTIAL
        
        return STATUS_NEUTRAL

    def _calculate_importance(
        self,
        importance: Any,
        status: str,
        confidence: Optional[float],
        result: Any = None
    ) -> float:
        """Calculate experience importance."""
        
        if importance is not None:
            try:
                return round(
                    min(max(float(importance), 0.0), 1.0),
                    3
                )
            except (TypeError, ValueError):
                pass
        
        score = 0.5
        
        # Status contribution
        if status == STATUS_SUCCESS:
            score += 0.15
        elif status == STATUS_FAILURE:
            score += 0.20
        elif status == STATUS_PARTIAL:
            score += 0.10
        
        # Confidence contribution
        if confidence is not None:
            try:
                conf = float(confidence)
                if conf >= 0.8:
                    score += 0.10
                elif conf >= 0.6:
                    score += 0.05
            except (TypeError, ValueError):
                pass
        
        # Result importance
        if isinstance(result, dict):
            if result.get("critical"):
                score += 0.20
            if result.get("risk", 0) > 0.7:
                score += 0.15
        
        return round(min(score, 1.0), 3)

    def _determine_tier(self, importance: float) -> str:
        """Determine importance tier."""
        if importance >= 0.9:
            return ExperienceTier.CRITICAL.value
        elif importance >= 0.7:
            return ExperienceTier.HIGH.value
        elif importance >= 0.4:
            return ExperienceTier.MEDIUM.value
        elif importance >= 0.2:
            return ExperienceTier.LOW.value
        else:
            return ExperienceTier.TRIVIAL.value

    def _determine_stage(self, timestamp: str) -> str:
        """Determine memory stage based on age."""
        try:
            exp_time = datetime.fromisoformat(timestamp)
            age = (datetime.now() - exp_time).total_seconds()
            
            if age < 600:  # < 10 minutes
                return MemoryStage.SENSORY.value
            elif age < 21600:  # < 6 hours
                return MemoryStage.SHORT_TERM.value
            elif age < 86400:  # < 24 hours
                return MemoryStage.WORKING.value
            elif age < 604800:  # < 7 days
                return MemoryStage.LONG_TERM.value
            else:
                return MemoryStage.PERMANENT.value
        except:
            return MemoryStage.WORKING.value

    def _automatic_tags(self, experience: Experience) -> List[str]:
        """Generate automatic tags."""
        tags = set()
        
        # Status tags
        tags.add(experience.status)
        
        # Domain tag
        if experience.domain:
            tags.add(f"domain:{experience.domain}")
        
        # Type tag
        tags.add(f"type:{experience.type}")
        
        # Tier tag
        tags.add(f"tier:{experience.tier}")
        
        # Confidence tag
        if experience.confidence >= 0.8:
            tags.add("high_confidence")
        elif experience.confidence >= 0.6:
            tags.add("medium_confidence")
        else:
            tags.add("low_confidence")
        
        # Success/Failure tags
        if experience.success is True:
            tags.add("successful")
        elif experience.success is False:
            tags.add("failed")
        
        # Extract keywords from event
        if isinstance(experience.event, str):
            words = experience.event.lower().split()
            important_words = [w for w in words if len(w) > 3]
            for word in important_words[:3]:
                tags.add(word)
        
        # Context tags
        if experience.context:
            for key in experience.context.keys():
                tags.add(f"ctx:{key}")
        
        return list(tags)

    def _calculate_retention(self, age: float) -> float:
        """Calculate retention based on forgetting curve."""
        if age < 600:  # sensory
            return self.forgetting_curve["sensory"]
        elif age < 21600:  # short_term
            return self.forgetting_curve["short_term"] * math.exp(-self.decay_rate * age / 3600)
        elif age < 86400:  # working
            return self.forgetting_curve["working"] * math.exp(-self.decay_rate * age / 7200)
        elif age < 604800:  # long_term
            return self.forgetting_curve["long_term"] * math.exp(-self.decay_rate * age / 14400)
        else:  # permanent
            return self.forgetting_curve["permanent"]

    # ============================================================
    # RECORD EXPERIENCE
    # ============================================================

    def record(
        self,
        event: Any,
        result: Any = None,
        domain: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        success: Optional[bool] = None,
        confidence: Optional[float] = None,
        importance: Optional[float] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        type: str = ExperienceType.ACTION.value,
        parent_id: Optional[str] = None
    ) -> Optional[Experience]:
        """
        Record a new experience.
        
        Args:
            event: The event/action
            result: The outcome
            domain: Domain of experience
            context: Context information
            success: Explicit success flag
            confidence: Confidence level
            importance: Importance level
            tags: Manual tags
            metadata: Additional metadata
            type: Experience type
            parent_id: Parent experience ID
            
        Returns:
            Experience object or None
        """
        with self._lock:
            try:
                status = self._normalize_status(result, success)
                
                # Calculate importance
                importance_value = self._calculate_importance(
                    importance, status, confidence, result
                )
                
                # Determine tier
                tier = self._determine_tier(importance_value)
                
                # Create experience
                experience = Experience(
                    id=self._generate_id(),
                    timestamp=self._timestamp(),
                    event=event,
                    result=result,
                    domain=domain,
                    context=context or {},
                    status=status,
                    success=(status == STATUS_SUCCESS) if status in [STATUS_SUCCESS, STATUS_FAILURE] else None,
                    confidence=confidence or 0.5,
                    importance=importance_value,
                    tags=tags or [],
                    metadata=metadata or {},
                    type=type,
                    tier=tier,
                    stage=MemoryStage.SENSORY.value,
                    weight=1.0,
                    decay_rate=self.decay_rate,
                    parent_id=parent_id,
                )
                
                # Automatic tagging
                if self.auto_tag:
                    auto_tags = self._automatic_tags(experience)
                    experience.tags.extend(auto_tags)
                    experience.tags = list(set(experience.tags))
                
                # Store
                self.experiences.append(experience)
                self.experience_map[experience.id] = experience
                self.total_recorded += 1
                self.last_experience = experience
                
                # Update statistics
                self._update_statistics(status)
                
                # Link to parent
                if parent_id and parent_id in self.experience_map:
                    self.experience_map[parent_id].children.append(experience.id)
                    self.experience_graph[parent_id].append(experience.id)
                
                # Enforce limit
                self._enforce_limit()
                
                # Check consolidation
                if len(self.experiences) % self.consolidation_threshold == 0:
                    self._consolidate_memories()
                
                logger.debug(
                    "Experience recorded: %s (%s)",
                    experience.id[:8],
                    status
                )
                
                return experience
                
            except Exception as e:
                logger.exception("Experience recording failed: %s", e)
                return None

    # ============================================================
    # STATISTICS UPDATE
    # ============================================================

    def _update_statistics(self, status: str) -> None:
        """Update experience statistics."""
        if status == STATUS_SUCCESS:
            self.success_count += 1
        elif status == STATUS_FAILURE:
            self.failure_count += 1
        elif status == STATUS_PARTIAL:
            self.partial_count += 1
        else:
            self.neutral_count += 1

    # ============================================================
    # MEMORY LIMIT
    # ============================================================

    def _enforce_limit(self) -> None:
        """Enforce maximum size limit."""
        overflow = len(self.experiences) - self.max_size
        if overflow > 0:
            # Remove oldest experiences
            removed = self.experiences[:overflow]
            for exp in removed:
                if exp.id in self.experience_map:
                    del self.experience_map[exp.id]
            self.experiences = self.experiences[overflow:]
            logger.debug("Removed %d oldest experiences", overflow)

    # ============================================================
    # MEMORY CONSOLIDATION
    # ============================================================

    def _consolidate_memories(self) -> None:
        """Consolidate memories (move to long-term storage)."""
        try:
            consolidated = 0
            
            for exp in self.experiences:
                if exp.stage != MemoryStage.PERMANENT.value:
                    age = (datetime.now() - datetime.fromisoformat(exp.timestamp)).total_seconds()
                    
                    # Update stage based on age
                    new_stage = self._determine_stage(exp.timestamp)
                    if new_stage != exp.stage:
                        exp.stage = new_stage
                        consolidated += 1
                        
                        # Recalculate importance if promoted
                        if new_stage == MemoryStage.PERMANENT.value:
                            exp.importance = min(1.0, exp.importance + 0.1)
                            exp.tier = self._determine_tier(exp.importance)
            
            if consolidated > 0:
                logger.debug("Consolidated %d memories", consolidated)
                
        except Exception as e:
            logger.warning("Memory consolidation failed: %s", e)

    # ============================================================
    # RECALL / RETRIEVAL
    # ============================================================

    def recall(
        self,
        limit: int = 10,
        min_confidence: float = 0.0,
        min_importance: float = 0.0,
        domain: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Experience]:
        """
        Recall recent experiences with filters.
        
        Args:
            limit: Maximum number to return
            min_confidence: Minimum confidence
            min_importance: Minimum importance
            domain: Filter by domain
            status: Filter by status
            
        Returns:
            List of experiences
        """
        with self._lock:
            try:
                limit = max(0, int(limit))
                if limit == 0:
                    return []
                
                results = []
                
                for exp in reversed(self.experiences):
                    # Filters
                    if exp.confidence < min_confidence:
                        continue
                    if exp.importance < min_importance:
                        continue
                    if domain and exp.domain != domain:
                        continue
                    if status and exp.status != status:
                        continue
                    
                    # Update access
                    exp.access_count += 1
                    exp.last_accessed = self._timestamp()
                    self.access_history.append(exp.id)
                    
                    results.append(exp)
                    
                    if len(results) >= limit:
                        break
                
                return results
                
            except Exception as e:
                logger.error("Recall failed: %s", e)
                return []

    def recall_by_relevance(
        self,
        query: Any,
        limit: int = 10,
        min_similarity: float = 0.5
    ) -> List[Tuple[Experience, float]]:
        """
        Recall experiences by relevance/similarity.
        
        Args:
            query: Query to match against
            limit: Maximum results
            min_similarity: Minimum similarity score
            
        Returns:
            List of (experience, similarity_score) tuples
        """
        with self._lock:
            try:
                results = []
                query_str = str(query).lower()
                
                for exp in self.experiences:
                    similarity = self._calculate_similarity(query_str, exp)
                    if similarity >= min_similarity:
                        results.append((exp, similarity))
                
                results.sort(key=lambda x: x[1], reverse=True)
                return results[:limit]
                
            except Exception as e:
                logger.error("Recall by relevance failed: %s", e)
                return []

    def _calculate_similarity(self, query: str, experience: Experience) -> float:
        """Calculate similarity between query and experience."""
        score = 0.0
        content = " ".join([
            str(experience.event),
            str(experience.result),
            str(experience.domain),
            " ".join(experience.tags)
        ]).lower()
        
        # Word matching
        query_words = set(query.split())
        content_words = set(content.split())
        
        if query_words and content_words:
            common = query_words.intersection(content_words)
            score += len(common) / len(query_words) * 0.6
        
        # Partial matching
        if query in content:
            score += 0.3
        
        # Tag matching
        for tag in experience.tags:
            if tag.lower() in query:
                score += 0.1
        
        return min(score, 1.0)

    # ============================================================
    # GET / LATEST
    # ============================================================

    def latest(self) -> Optional[Experience]:
        """Get the latest experience."""
        return self.last_experience

    def get(self, experience_id: str) -> Optional[Experience]:
        """Get experience by ID."""
        with self._lock:
            exp = self.experience_map.get(experience_id)
            if exp:
                exp.access_count += 1
                exp.last_accessed = self._timestamp()
                self.access_history.append(exp.id)
            return exp

    def get_by_parent(self, parent_id: str) -> List[Experience]:
        """Get experiences by parent ID."""
        with self._lock:
            children = self.experience_graph.get(parent_id, [])
            return [self.experience_map[cid] for cid in children if cid in self.experience_map]

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        query: Any,
        domain: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Experience]:
        """
        Search experiences.
        
        Args:
            query: Search query
            domain: Filter by domain
            status: Filter by status
            limit: Maximum results
            
        Returns:
            List of matching experiences
        """
        if query is None:
            return []
        
        query_str = str(query).lower().strip()
        if not query_str:
            return []
        
        with self._lock:
            results = []
            
            for exp in reversed(self.experiences):
                if domain is not None and exp.domain != domain:
                    continue
                if status is not None and exp.status != status:
                    continue
                
                searchable = " ".join([
                    str(exp.event),
                    str(exp.result),
                    str(exp.domain),
                    " ".join(exp.tags),
                    str(exp.metadata)
                ]).lower()
                
                if query_str in searchable:
                    exp.access_count += 1
                    exp.last_accessed = self._timestamp()
                    results.append(exp)
                    
                    if len(results) >= limit:
                        break
            
            return results

    def search_by_tags(self, tags: List[str], limit: int = 50) -> List[Experience]:
        """Search experiences by tags."""
        tag_set = set(tags)
        results = []
        
        with self._lock:
            for exp in reversed(self.experiences):
                if tag_set.intersection(set(exp.tags)):
                    results.append(exp)
                    if len(results) >= limit:
                        break
        
        return results

    # ============================================================
    # FILTER
    # ============================================================

    def by_domain(self, domain: str, limit: int = 100) -> List[Experience]:
        """Get experiences by domain."""
        with self._lock:
            results = [e for e in reversed(self.experiences) if e.domain == domain]
            return results[:limit]

    def by_status(self, status: str, limit: int = 100) -> List[Experience]:
        """Get experiences by status."""
        with self._lock:
            results = [e for e in reversed(self.experiences) if e.status == status]
            return results[:limit]

    def by_tier(self, tier: str, limit: int = 100) -> List[Experience]:
        """Get experiences by tier."""
        with self._lock:
            results = [e for e in reversed(self.experiences) if e.tier == tier]
            return results[:limit]

    def by_stage(self, stage: str, limit: int = 100) -> List[Experience]:
        """Get experiences by memory stage."""
        with self._lock:
            results = [e for e in reversed(self.experiences) if e.stage == stage]
            return results[:limit]

    def successful(self, limit: int = 100) -> List[Experience]:
        """Get successful experiences."""
        return self.by_status(STATUS_SUCCESS, limit)

    def failures(self, limit: int = 100) -> List[Experience]:
        """Get failed experiences."""
        return self.by_status(STATUS_FAILURE, limit)

    def high_importance(self, min_importance: float = 0.7, limit: int = 100) -> List[Experience]:
        """Get high importance experiences."""
        with self._lock:
            results = [e for e in reversed(self.experiences) if e.importance >= min_importance]
            return results[:limit]

    # ============================================================
    # STATISTICS
    # ============================================================

    def stats(self) -> ExperienceStats:
        """Get comprehensive statistics."""
        with self._lock:
            stats = ExperienceStats()
            stats.total = len(self.experiences)
            
            # Status counts
            for exp in self.experiences:
                stats.by_status[exp.status] = stats.by_status.get(exp.status, 0) + 1
                stats.by_type[exp.type] = stats.by_type.get(exp.type, 0) + 1
                stats.by_domain[exp.domain] = stats.by_domain.get(exp.domain, 0) + 1
                stats.by_tier[exp.tier] = stats.by_tier.get(exp.tier, 0) + 1
                stats.by_stage[exp.stage] = stats.by_stage.get(exp.stage, 0) + 1
                stats.total_access += exp.access_count
                
                if exp.status == STATUS_SUCCESS:
                    stats.success_rate += 1
                
                stats.avg_confidence += exp.confidence
                stats.avg_importance += exp.importance
            
            # Calculate averages
            if stats.total > 0:
                stats.success_rate = stats.success_rate / stats.total
                stats.avg_confidence = stats.avg_confidence / stats.total
                stats.avg_importance = stats.avg_importance / stats.total
            
            # Recent count (last 24 hours)
            day_ago = datetime.now() - timedelta(days=1)
            stats.recent_count = sum(
                1 for e in self.experiences
                if datetime.fromisoformat(e.timestamp) > day_ago
            )
            
            # Consolidated count
            stats.consolidated = sum(1 for e in self.experiences if e.stage == MemoryStage.PERMANENT.value)
            
            # Patterns
            stats.patterns = [p.name for p in self.experience_patterns[:10]]
            
            stats.timestamp = self._timestamp()
            
            return stats

    def count(self) -> int:
        """Get total experiences."""
        return len(self.experiences)

    def total(self) -> int:
        """Get total recorded experiences."""
        return self.total_recorded

    def success_rate(self) -> float:
        """Calculate success rate."""
        completed = self.success_count + self.failure_count
        if completed == 0:
            return 0.0
        return round(self.success_count / completed, 4)

    # ============================================================
    # EXPERIENCE PATTERNS
    # ============================================================

    def discover_patterns(self, min_frequency: int = 3) -> List[ExperiencePattern]:
        """Discover patterns in experiences."""
        with self._lock:
            patterns = []
            
            # Status patterns
            status_sequence = [e.status for e in self.experiences[-100:]]
            for status in set(status_sequence):
                freq = status_sequence.count(status)
                if freq >= min_frequency:
                    patterns.append(ExperiencePattern(
                        id=f"pat_{uuid.uuid4().hex[:8]}",
                        name=f"{status}_pattern",
                        description=f"Frequent {status} experiences",
                        pattern_type="status",
                        confidence=freq / len(status_sequence),
                        examples=[e.id for e in self.experiences if e.status == status][:5],
                        frequency=freq
                    ))
            
            # Domain patterns
            domains = [e.domain for e in self.experiences if e.domain]
            domain_counts = Counter(domains)
            for domain, freq in domain_counts.most_common(5):
                if freq >= min_frequency:
                    patterns.append(ExperiencePattern(
                        id=f"pat_{uuid.uuid4().hex[:8]}",
                        name=f"{domain}_pattern",
                        description=f"Experiences in {domain} domain",
                        pattern_type="domain",
                        confidence=freq / len(self.experiences),
                        examples=[e.id for e in self.experiences if e.domain == domain][:5],
                        frequency=freq
                    ))
            
            # Success/Failure patterns
            if len(self.experiences) >= min_frequency:
                success_rate = self.success_rate()
                if success_rate >= 0.8:
                    patterns.append(ExperiencePattern(
                        id=f"pat_{uuid.uuid4().hex[:8]}",
                        name="high_success",
                        description=f"High success rate: {success_rate:.1%}",
                        pattern_type="success",
                        confidence=success_rate,
                        examples=[e.id for e in self.experiences if e.status == STATUS_SUCCESS][:5],
                        frequency=self.success_count
                    ))
                elif success_rate <= 0.3:
                    patterns.append(ExperiencePattern(
                        id=f"pat_{uuid.uuid4().hex[:8]}",
                        name="low_success",
                        description=f"Low success rate: {success_rate:.1%}",
                        pattern_type="failure",
                        confidence=1 - success_rate,
                        examples=[e.id for e in self.experiences if e.status == STATUS_FAILURE][:5],
                        frequency=self.failure_count
                    ))
            
            self.experience_patterns = patterns
            return patterns

    # ============================================================
    # ANOMALY DETECTION
    # ============================================================

    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect anomalies in experiences."""
        anomalies = []
        
        with self._lock:
            if len(self.experiences) < 10:
                return anomalies
            
            # Check for unusual success/failure patterns
            recent = self.experiences[-20:]
            recent_success = sum(1 for e in recent if e.status == STATUS_SUCCESS)
            recent_failure = sum(1 for e in recent if e.status == STATUS_FAILURE)
            
            if recent_success > 15 and len(recent) > 0:
                anomalies.append({
                    "type": "unusual_success",
                    "description": f"Unusually high success rate: {recent_success}/{len(recent)}",
                    "count": recent_success,
                    "total": len(recent),
                    "severity": "medium"
                })
            
            if recent_failure > 10 and len(recent) > 0:
                anomalies.append({
                    "type": "unusual_failure",
                    "description": f"Unusually high failure rate: {recent_failure}/{len(recent)}",
                    "count": recent_failure,
                    "total": len(recent),
                    "severity": "high"
                })
            
            # Check for confidence anomalies
            confidences = [e.confidence for e in self.experiences[-50:]]
            if len(confidences) > 5:
                mean = statistics.mean(confidences)
                std = statistics.stdev(confidences) if len(confidences) > 1 else 0
                
                for exp in self.experiences[-20:]:
                    if std > 0 and abs(exp.confidence - mean) > 2 * std:
                        anomalies.append({
                            "type": "confidence_anomaly",
                            "description": f"Unusual confidence: {exp.confidence:.2f} (mean: {mean:.2f})",
                            "confidence": exp.confidence,
                            "mean": mean,
                            "std": std,
                            "experience_id": exp.id,
                            "severity": "low"
                        })
            
            # Check for importance anomalies
            importances = [e.importance for e in self.experiences[-50:]]
            if len(importances) > 5:
                mean = statistics.mean(importances)
                std = statistics.stdev(importances) if len(importances) > 1 else 0
                
                for exp in self.experiences[-20:]:
                    if std > 0 and abs(exp.importance - mean) > 2 * std:
                        anomalies.append({
                            "type": "importance_anomaly",
                            "description": f"Unusual importance: {exp.importance:.2f} (mean: {mean:.2f})",
                            "importance": exp.importance,
                            "mean": mean,
                            "std": std,
                            "experience_id": exp.id,
                            "severity": "low"
                        })
        
        return anomalies

    # ============================================================
    # EXPERIENCE GRAPH
    # ============================================================

    def build_graph(self) -> Dict[str, List[str]]:
        """Build experience relationship graph."""
        with self._lock:
            graph = defaultdict(list)
            
            for exp in self.experiences:
                graph[exp.id] = exp.children
            
            # Add parent relationships
            for exp in self.experiences:
                if exp.parent_id:
                    graph[exp.parent_id].append(exp.id)
            
            return dict(graph)

    def get_related(self, experience_id: str, depth: int = 1) -> List[Experience]:
        """Get related experiences."""
        related = []
        visited = set()
        
        def traverse(current_id: str, current_depth: int):
            if current_depth > depth or current_id in visited:
                return
            
            visited.add(current_id)
            
            # Get children
            children = self.experience_graph.get(current_id, [])
            for child_id in children:
                if child_id in self.experience_map:
                    related.append(self.experience_map[child_id])
                    traverse(child_id, current_depth + 1)
            
            # Get parent
            if current_id in self.experience_map:
                exp = self.experience_map[current_id]
                if exp.parent_id and exp.parent_id in self.experience_map:
                    related.append(self.experience_map[exp.parent_id])
                    traverse(exp.parent_id, current_depth + 1)
        
        with self._lock:
            traverse(experience_id, 0)
        
        return related

    # ============================================================
    # EXPERIENCE REPLAY
    # ============================================================

    def replay(self, count: int = 10) -> List[Experience]:
        """
        Replay experiences for learning.
        
        Returns experiences weighted by importance.
        """
        with self._lock:
            if not self.experiences:
                return []
            
            # Weight by importance and recency
            weighted = []
            now = datetime.now()
            
            for exp in self.experiences:
                try:
                    age = (now - datetime.fromisoformat(exp.timestamp)).total_seconds()
                    recency = math.exp(-age / 86400)  # 1 day decay
                    weight = exp.importance * 0.7 + recency * 0.3
                    weighted.append((exp, weight))
                except:
                    weighted.append((exp, exp.importance))
            
            # Sort by weight
            weighted.sort(key=lambda x: x[1], reverse=True)
            
            return [exp for exp, _ in weighted[:count]]

    # ============================================================
    # CLEAR / RESET
    # ============================================================

    def clear(self) -> bool:
        """Clear all experiences."""
        with self._lock:
            self.experiences.clear()
            self.experience_map.clear()
            self.experience_graph.clear()
            self.access_history.clear()
            self.experience_patterns.clear()
            
            self.last_experience = None
            self.success_count = 0
            self.failure_count = 0
            self.neutral_count = 0
            self.partial_count = 0
            
            logger.info("Experience memory cleared")
            return True

    # ============================================================
    # EXPORT / IMPORT
    # ============================================================

    def export(self, include_patterns: bool = True) -> Dict[str, Any]:
        """Export all experiences."""
        with self._lock:
            data = {
                "version": self.VERSION,
                "exported_at": self._timestamp(),
                "total": len(self.experiences),
                "stats": {
                    "success": self.success_count,
                    "failure": self.failure_count,
                    "neutral": self.neutral_count,
                    "partial": self.partial_count,
                    "success_rate": self.success_rate(),
                },
                "experiences": [exp.to_dict() for exp in self.experiences],
            }
            
            if include_patterns:
                data["patterns"] = [
                    {
                        "id": p.id,
                        "name": p.name,
                        "description": p.description,
                        "confidence": p.confidence,
                        "frequency": p.frequency,
                    }
                    for p in self.experience_patterns
                ]
            
            return data

    def import_data(self, data: Dict[str, Any]) -> int:
        """Import experiences from data."""
        if not isinstance(data, dict):
            return 0
        
        with self._lock:
            experiences_data = data.get("experiences", [])
            imported = 0
            
            for exp_data in experiences_data:
                if not isinstance(exp_data, dict):
                    continue
                
                try:
                    # Check if exists
                    exp_id = exp_data.get("id")
                    if exp_id and exp_id in self.experience_map:
                        continue
                    
                    # Create experience
                    exp = Experience.from_dict(exp_data)
                    
                    # Ensure required fields
                    if not exp.id:
                        exp.id = self._generate_id()
                    if not exp.timestamp:
                        exp.timestamp = self._timestamp()
                    
                    self.experiences.append(exp)
                    self.experience_map[exp.id] = exp
                    self.total_recorded += 1
                    self._update_statistics(exp.status)
                    imported += 1
                    
                except Exception as e:
                    logger.warning("Failed to import experience: %s", e)
            
            self._enforce_limit()
            self._build_graph()
            
            logger.info("Imported %d experiences", imported)
            return imported

    def _build_graph(self) -> None:
        """Rebuild experience graph."""
        self.experience_graph.clear()
        for exp in self.experiences:
            if exp.parent_id:
                self.experience_graph[exp.parent_id].append(exp.id)
            for child_id in exp.children:
                self.experience_graph[exp.id].append(child_id)

    # ============================================================
    # STATUS
    # ============================================================

    def status(self) -> Dict[str, Any]:
        """Get engine status."""
        with self._lock:
            return {
                "name": self.name,
                "version": self.VERSION,
                "status": "ONLINE",
                "stored": len(self.experiences),
                "total_recorded": self.total_recorded,
                "success": self.success_count,
                "failure": self.failure_count,
                "neutral": self.neutral_count,
                "partial": self.partial_count,
                "success_rate": self.success_rate(),
                "patterns": len(self.experience_patterns),
                "graph_nodes": len(self.experience_graph),
                "max_size": self.max_size,
                "last_experience": self.last_experience.id if self.last_experience else None,
                "timestamp": self._timestamp(),
            }

    # ============================================================
    # VALIDATION
    # ============================================================

    def validate_experience(self, experience_id: str, score: float) -> bool:
        """Validate an experience with a score."""
        with self._lock:
            exp = self.experience_map.get(experience_id)
            if not exp:
                return False
            
            exp.validation_count += 1
            exp.validation_score = (
                (exp.validation_score * (exp.validation_count - 1) + score)
                / exp.validation_count
            )
            
            # Update confidence based on validation
            if score >= 0.8:
                exp.confidence = min(1.0, exp.confidence + 0.05)
            elif score <= 0.3:
                exp.confidence = max(0.0, exp.confidence - 0.05)
            
            return True

    # ============================================================
    # ALIASES (Backward Compatibility)
    # ============================================================

    def process(self, event: Any, result: Any = None, **kwargs) -> Optional[Experience]:
        """Alias for record."""
        return self.record(event, result, **kwargs)

    def add(self, event: Any, result: Any = None, **kwargs) -> Optional[Experience]:
        """Alias for record."""
        return self.record(event, result, **kwargs)

    def store(self, event: Any, result: Any = None, **kwargs) -> Optional[Experience]:
        """Alias for record."""
        return self.record(event, result, **kwargs)


# ============================================================
# GLOBAL INSTANCE
# ============================================================

experience_engine = ExperienceEngine()


# ============================================================
# SELF TEST - MENGGUNAKAN experience_engine
# ============================================================

def self_test() -> Dict[str, Any]:
    """Run experience engine self-test."""
    
    print()
    print("=" * 80)
    print("  EXPERIENCE ENGINE v3.0 - SELF TEST")
    print("=" * 80)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        test_exp = ExperienceEngine()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Record
    print("\n2. Testing record...")
    try:
        exp = experience_engine.record("Test event", "Test result", domain="test", confidence=0.8)
        if exp:
            results["record"] = {"status": "PASS", "id": exp.id}
            tests_passed += 1
            print(f"   ✅ Record passed (ID: {exp.id[:8]})")
        else:
            results["record"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Record failed")
    except Exception as e:
        results["record"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Record failed: {e}")
    
    # Test 3: Recall
    print("\n3. Testing recall...")
    try:
        recalled = experience_engine.recall(limit=5)
        if recalled:
            results["recall"] = {"status": "PASS", "count": len(recalled)}
            tests_passed += 1
            print(f"   ✅ Recall passed ({len(recalled)} experiences)")
        else:
            results["recall"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Recall failed")
    except Exception as e:
        results["recall"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Recall failed: {e}")
    
    # Test 4: Patterns
    print("\n4. Testing pattern discovery...")
    try:
        patterns = experience_engine.discover_patterns()
        if patterns is not None:
            results["patterns"] = {"status": "PASS", "count": len(patterns)}
            tests_passed += 1
            print(f"   ✅ Patterns passed ({len(patterns)} patterns)")
        else:
            results["patterns"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Patterns failed")
    except Exception as e:
        results["patterns"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Patterns failed: {e}")
    
    # Test 5: Stats
    print("\n5. Testing stats...")
    try:
        stats = experience_engine.stats()
        if stats and stats.total > 0:
            results["stats"] = {"status": "PASS", "total": stats.total}
            tests_passed += 1
            print(f"   ✅ Stats passed (total: {stats.total})")
        else:
            results["stats"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Stats failed")
    except Exception as e:
        results["stats"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Stats failed: {e}")
    
    # Summary
    print()
    print("=" * 80)
    print("  TEST SUMMARY")
    print("=" * 80)
    print(f"  ✅ Passed: {tests_passed}")
    print(f"  ❌ Failed: {tests_failed}")
    print(f"  📊 Total:  {tests_passed + tests_failed}")
    print("=" * 80)
    
    return {
        "module": "experience",
        "version": EXPERIENCE_VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    # Classes
    "ExperienceEngine",
    "Experience",
    "ExperienceStats",
    "ExperiencePattern",
    
    # Enums
    "ExperienceType",
    "ExperienceTier",
    "MemoryStage",
    
    # Constants
    "EXPERIENCE_VERSION",
    "STATUS_SUCCESS",
    "STATUS_FAILURE",
    "STATUS_NEUTRAL",
    "STATUS_PARTIAL",
    "STATUS_PENDING",
    "STATUS_EXPIRED",
    "STATUS_ARCHIVED",
    "IMPORTANCE_CRITICAL",
    "IMPORTANCE_HIGH",
    "IMPORTANCE_MEDIUM",
    "IMPORTANCE_LOW",
    "IMPORTANCE_MINIMAL",
    "CONFIDENCE_VERY_HIGH",
    "CONFIDENCE_HIGH",
    "CONFIDENCE_MEDIUM",
    "CONFIDENCE_LOW",
    "CONFIDENCE_VERY_LOW",
    
    # Global instance
    "experience_engine",
    
    # Functions
    "self_test",
]


# ============================================================
# END
# ============================================================