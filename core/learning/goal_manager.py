# ============================================================
# core/learning/goal_manager.py
# GOAL MANAGER v3.0
# SUPER COMPREHENSIVE GOAL MANAGEMENT
#
# FITUR LENGKAP:
# 1. Create, update, delete goals
# 2. Track progress (0-100%)
# 3. Priority management (LOW, NORMAL, HIGH, CRITICAL)
# 4. Deadline & overdue detection
# 5. Milestones & sub-goals
# 6. Learning objectives integration
# 7. Source problem tracking
# 8. Tags & categorization
# 9. History & audit trail
# 10. Search & filtering
# 11. Statistics & analytics
# 12. Auto-generate from problems/learning
# 13. Pause, resume, cancel, reopen
# 14. Progress history tracking
# 15. Completion rate analysis
# 16. Priority-based ranking
# ============================================================

from __future__ import annotations  # <-- FIXED!

import logging
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)  # <-- FIXED!

# ============================================================
# VERSION
# ============================================================

GOAL_MANAGER_VERSION = "3.0.0"
API_VERSION = "1.0"

# ============================================================
# CONSTANTS
# ============================================================

PRIORITY_LOW = "LOW"
PRIORITY_NORMAL = "NORMAL"
PRIORITY_HIGH = "HIGH"
PRIORITY_CRITICAL = "CRITICAL"

STATUS_ACTIVE = "ACTIVE"
STATUS_COMPLETED = "COMPLETED"
STATUS_PAUSED = "PAUSED"
STATUS_CANCELLED = "CANCELLED"
STATUS_ARCHIVED = "ARCHIVED"

PRIORITY_WEIGHTS = {
    PRIORITY_LOW: 1,
    PRIORITY_NORMAL: 2,
    PRIORITY_HIGH: 3,
    PRIORITY_CRITICAL: 4,
}

PRIORITY_COLORS = {
    PRIORITY_LOW: "#8D9AAA",
    PRIORITY_NORMAL: "#3B82F6",
    PRIORITY_HIGH: "#F59E0B",
    PRIORITY_CRITICAL: "#EF4444",
}

PRIORITY_NAMES = {
    PRIORITY_LOW: "Low",
    PRIORITY_NORMAL: "Normal",
    PRIORITY_HIGH: "High",
    PRIORITY_CRITICAL: "Critical",
}

STATUS_NAMES = {
    STATUS_ACTIVE: "Active",
    STATUS_COMPLETED: "Completed",
    STATUS_PAUSED: "Paused",
    STATUS_CANCELLED: "Cancelled",
    STATUS_ARCHIVED: "Archived",
}

STATUS_COLORS = {
    STATUS_ACTIVE: "#22C55E",
    STATUS_COMPLETED: "#3B82F6",
    STATUS_PAUSED: "#F59E0B",
    STATUS_CANCELLED: "#EF4444",
    STATUS_ARCHIVED: "#8D9AAA",
}

# ============================================================
# TIME HELPER
# ============================================================

def utc_now() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ============================================================
# GOAL MANAGER v3.0
# ============================================================

class GoalManager:
    """
    Super Comprehensive Goal Management System.
    
    Features:
    - Create, update, delete goals
    - Track progress with history
    - Priority management (4 levels)
    - Milestones & sub-goals
    - Learning objectives integration
    - Source problem tracking
    - Tags & categorization
    - Search & filtering
    - Statistics & analytics
    - Auto-generation
    """
    
    VERSION = GOAL_MANAGER_VERSION
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.goals: List[Dict[str, Any]] = []
        self.completed: List[Dict[str, Any]] = []
        self.archived: List[Dict[str, Any]] = []
        
        self.goal_count = 0
        self.total_created = 0
        self.total_completed = 0
        self.total_cancelled = 0
        self.total_paused = 0
        self.total_resumed = 0
        self.total_progress_updates = 0
        self.total_milestones = 0
        self.total_milestones_completed = 0
        
        self.last_goal: Optional[Dict[str, Any]] = None
        self.last_action: Optional[str] = None
        
        self.max_history = self.config.get("max_history", 500)
        
        logger.info("Goal Manager v%s initialized.", self.VERSION)
    
    # ========================================================
    # INTERNAL HELPERS
    # ========================================================
    
    def _normalize_priority(self, priority: Any) -> str:
        """Normalize priority string."""
        if priority is None:
            return PRIORITY_NORMAL
        
        value = str(priority).strip().upper()
        
        aliases = {
            "URGENT": PRIORITY_CRITICAL,
            "CRITICAL": PRIORITY_CRITICAL,
            "IMPORTANT": PRIORITY_HIGH,
            "HIGH": PRIORITY_HIGH,
            "NORMAL": PRIORITY_NORMAL,
            "MEDIUM": PRIORITY_NORMAL,
            "LOW": PRIORITY_LOW,
        }
        
        return aliases.get(value, PRIORITY_NORMAL)
    
    def _normalize_progress(self, progress: Any) -> float:
        """Normalize progress to 0-100."""
        try:
            value = float(progress)
        except (TypeError, ValueError):
            value = 0.0
        return max(0.0, min(100.0, value))
    
    def _normalize_text(self, value: Any, default: str = "") -> str:
        """Normalize text value."""
        if value is None:
            return default
        return str(value).strip()
    
    def _goal_snapshot(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Create a deep copy of a goal."""
        return deepcopy(goal)
    
    def _find_index(self, goal_id: Any) -> int:
        """Find goal index by ID."""
        if goal_id is None:
            return -1
        
        goal_id = str(goal_id)
        for index, goal in enumerate(self.goals):
            if str(goal.get("id")) == goal_id:
                return index
        return -1
    
    def _record_history(self, goal: Dict[str, Any], action: str, 
                       note: str = "", extra: Optional[Dict[str, Any]] = None) -> None:
        """Record goal history entry."""
        entry = {
            "time": utc_now(),
            "action": action,
            "progress": goal.get("progress", 0),
            "status": goal.get("status"),
            "note": self._normalize_text(note),
        }
        
        if extra:
            entry.update(deepcopy(extra))
        
        goal.setdefault("history", []).append(entry)
        
        # Trim history
        if len(goal["history"]) > self.max_history:
            goal["history"] = goal["history"][-self.max_history:]
    
    # ========================================================
    # CREATE GOAL
    # ========================================================
    
    def create_goal(
        self,
        title: str,
        description: str = "",
        priority: str = "NORMAL",
        target: Optional[float] = None,
        deadline: Optional[str] = None,
        learning_objective: Optional[str] = None,
        source_problem: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        auto_start: bool = True
    ) -> Dict[str, Any]:
        """
        Create and register a new goal.
        
        Args:
            title: Goal title (required)
            description: Goal description
            priority: LOW, NORMAL, HIGH, CRITICAL
            target: Target value to achieve
            deadline: ISO date string
            learning_objective: Associated learning objective
            source_problem: Problem this goal addresses
            tags: List of tags
            metadata: Additional metadata
            auto_start: Start immediately
            
        Returns:
            Created goal dictionary
        """
        title = self._normalize_text(title)
        if not title:
            raise ValueError("Goal title cannot be empty.")
        
        normalized_priority = self._normalize_priority(priority)
        
        goal = {
            "id": str(uuid.uuid4()),
            "created": utc_now(),
            "updated": utc_now(),
            "title": title,
            "description": self._normalize_text(description),
            "priority": normalized_priority,
            "priority_score": PRIORITY_WEIGHTS.get(normalized_priority, 2),
            "target": target,
            "progress": 0.0,
            "status": STATUS_ACTIVE if auto_start else STATUS_PAUSED,
            "deadline": deadline,
            "learning_objective": learning_objective,
            "source_problem": source_problem,
            "tags": list(tags) if isinstance(tags, (list, tuple, set)) else [],
            "metadata": deepcopy(metadata) if isinstance(metadata, dict) else {},
            "history": [],
            "milestones": [],
            "completed_at": None,
            "cancelled_at": None,
            "paused_at": None,
            "resumed_at": None,
            "archived_at": None,
            "completion_count": 0,
            "progress_history": [],
        }
        
        self._record_history(goal, "CREATED", "Goal created.")
        
        self.goals.append(goal)
        self.goal_count += 1
        self.total_created += 1
        self.last_goal = goal
        self.last_action = "CREATED"
        
        logger.info("Goal created: %s [%s]", title, goal["id"])
        return goal
    
    # ========================================================
    # UPDATE PROGRESS
    # ========================================================
    
    def update_progress(
        self,
        goal_id: str,
        progress: float,
        note: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Update goal progress (0-100).
        
        Args:
            goal_id: Goal ID
            progress: Progress value (0-100)
            note: Optional note
            
        Returns:
            Updated goal or None
        """
        goal = self.get_goal(goal_id)
        if goal is None:
            return None
        
        if goal.get("status") in {STATUS_CANCELLED, STATUS_COMPLETED, STATUS_ARCHIVED}:
            return goal
        
        old_progress = goal.get("progress", 0)
        new_progress = self._normalize_progress(progress)
        
        goal["progress"] = new_progress
        goal["updated"] = utc_now()
        
        self.total_progress_updates += 1
        
        # Record progress history
        goal.setdefault("progress_history", []).append({
            "time": utc_now(),
            "old": old_progress,
            "new": new_progress,
            "note": self._normalize_text(note),
        })
        
        self._record_history(
            goal,
            "PROGRESS_UPDATED",
            note,
            {"previous_progress": old_progress, "new_progress": new_progress}
        )
        
        if new_progress >= 100:
            self.complete_goal(goal_id, note=note or "Goal reached 100% progress.")
        
        self.last_goal = goal
        self.last_action = "PROGRESS_UPDATED"
        
        return goal
    
    def increment_progress(
        self,
        goal_id: str,
        amount: float,
        note: str = ""
    ) -> Optional[Dict[str, Any]]:
        """Increase progress by a relative amount."""
        goal = self.get_goal(goal_id)
        if goal is None:
            return None
        
        current = goal.get("progress", 0)
        return self.update_progress(goal_id, current + float(amount), note=note)
    
    # ========================================================
    # COMPLETE GOAL
    # ========================================================
    
    def complete_goal(
        self,
        goal_id: str,
        note: str = "",
        achieved_value: Optional[Any] = None
    ) -> bool:
        """
        Mark a goal as completed.
        
        Args:
            goal_id: Goal ID
            note: Completion note
            achieved_value: Value achieved
            
        Returns:
            True if completed
        """
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        
        if goal.get("status") == STATUS_COMPLETED:
            return True
        
        if goal.get("status") == STATUS_CANCELLED:
            return False
        
        goal["progress"] = 100.0
        goal["status"] = STATUS_COMPLETED
        goal["completed_at"] = utc_now()
        goal["updated"] = utc_now()
        goal["completion_count"] = goal.get("completion_count", 0) + 1
        goal["achieved_value"] = achieved_value
        
        self.completed.append(goal)
        self.total_completed += 1
        
        self._record_history(goal, "COMPLETED", note or "Goal completed.")
        
        self.last_goal = goal
        self.last_action = "COMPLETED"
        
        logger.info("Goal completed: %s", goal.get("title"))
        return True
    
    # ========================================================
    # PAUSE / RESUME
    # ========================================================
    
    def pause_goal(self, goal_id: str, note: str = "") -> bool:
        """Pause an active goal."""
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        
        if goal.get("status") != STATUS_ACTIVE:
            return False
        
        goal["status"] = STATUS_PAUSED
        goal["paused_at"] = utc_now()
        goal["updated"] = utc_now()
        
        self.total_paused += 1
        self._record_history(goal, "PAUSED", note)
        
        self.last_goal = goal
        self.last_action = "PAUSED"
        
        return True
    
    def resume_goal(self, goal_id: str, note: str = "") -> bool:
        """Resume a paused goal."""
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        
        if goal.get("status") != STATUS_PAUSED:
            return False
        
        goal["status"] = STATUS_ACTIVE
        goal["resumed_at"] = utc_now()
        goal["updated"] = utc_now()
        
        self.total_resumed += 1
        self._record_history(goal, "RESUMED", note)
        
        self.last_goal = goal
        self.last_action = "RESUMED"
        
        return True
    
    # ========================================================
    # CANCEL / REOPEN
    # ========================================================
    
    def cancel_goal(self, goal_id: str, reason: str = "") -> bool:
        """Cancel a goal."""
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        
        if goal.get("status") == STATUS_COMPLETED:
            return False
        
        if goal.get("status") == STATUS_CANCELLED:
            return True
        
        goal["status"] = STATUS_CANCELLED
        goal["cancelled_at"] = utc_now()
        goal["updated"] = utc_now()
        goal["cancel_reason"] = self._normalize_text(reason)
        
        self.total_cancelled += 1
        self._record_history(goal, "CANCELLED", reason)
        
        self.last_goal = goal
        self.last_action = "CANCELLED"
        
        logger.info("Goal cancelled: %s", goal.get("title"))
        return True
    
    def reopen_goal(self, goal_id: str, note: str = "") -> bool:
        """Reopen a completed or cancelled goal."""
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        
        if goal.get("status") not in {STATUS_COMPLETED, STATUS_CANCELLED}:
            return False
        
        goal["status"] = STATUS_ACTIVE
        goal["updated"] = utc_now()
        goal["completed_at"] = None
        goal["cancelled_at"] = None
        goal["progress"] = max(0.0, goal.get("progress", 0))
        
        self._record_history(goal, "REOPENED", note)
        
        self.last_goal = goal
        self.last_action = "REOPENED"
        
        return True
    
    def archive_goal(self, goal_id: str, note: str = "") -> bool:
        """Archive a completed goal."""
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        
        if goal.get("status") != STATUS_COMPLETED:
            return False
        
        goal["status"] = STATUS_ARCHIVED
        goal["archived_at"] = utc_now()
        goal["updated"] = utc_now()
        
        self._record_history(goal, "ARCHIVED", note)
        self.archived.append(goal)
        
        self.last_goal = goal
        self.last_action = "ARCHIVED"
        
        return True
    
    # ========================================================
    # MILESTONES
    # ========================================================
    
    def add_milestone(
        self,
        goal_id: str,
        title: str,
        target: float = 100,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Add a milestone to a goal."""
        goal = self.get_goal(goal_id)
        if goal is None:
            return None
        
        title = self._normalize_text(title)
        if not title:
            raise ValueError("Milestone title cannot be empty.")
        
        milestone = {
            "id": str(uuid.uuid4()),
            "title": title,
            "target": self._normalize_progress(target),
            "progress": 0.0,
            "status": STATUS_ACTIVE,
            "created": utc_now(),
            "completed_at": None,
            "metadata": deepcopy(metadata) if isinstance(metadata, dict) else {},
        }
        
        goal.setdefault("milestones", []).append(milestone)
        goal["updated"] = utc_now()
        
        self.total_milestones += 1
        self._record_history(goal, "MILESTONE_ADDED", title)
        
        return milestone
    
    def update_milestone(
        self,
        goal_id: str,
        milestone_id: str,
        progress: float,
        note: str = ""
    ) -> Optional[Dict[str, Any]]:
        """Update milestone progress."""
        goal = self.get_goal(goal_id)
        if goal is None:
            return None
        
        value = self._normalize_progress(progress)
        
        for milestone in goal.get("milestones", []):
            if str(milestone.get("id")) != str(milestone_id):
                continue
            
            milestone["progress"] = value
            milestone["updated"] = utc_now()
            
            if value >= 100:
                milestone["progress"] = 100.0
                milestone["status"] = STATUS_COMPLETED
                milestone["completed_at"] = utc_now()
                self.total_milestones_completed += 1
            
            goal["updated"] = utc_now()
            self._record_history(goal, "MILESTONE_UPDATED", note or milestone.get("title", ""))
            
            return milestone
        
        return None
    
    # ========================================================
    # GET GOALS
    # ========================================================
    
    def get_goal(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """Get a goal by ID."""
        index = self._find_index(goal_id)
        if index < 0:
            return None
        return self.goals[index]
    
    def get_goal_copy(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """Get a copy of a goal."""
        goal = self.get_goal(goal_id)
        if goal is None:
            return None
        return self._goal_snapshot(goal)
    
    def active_goals(self) -> List[Dict[str, Any]]:
        """Get all active goals."""
        return [g for g in self.goals if g.get("status") == STATUS_ACTIVE]
    
    def paused_goals(self) -> List[Dict[str, Any]]:
        """Get all paused goals."""
        return [g for g in self.goals if g.get("status") == STATUS_PAUSED]
    
    def completed_goals(self) -> List[Dict[str, Any]]:
        """Get all completed goals."""
        return [g for g in self.goals if g.get("status") == STATUS_COMPLETED]
    
    def cancelled_goals(self) -> List[Dict[str, Any]]:
        """Get all cancelled goals."""
        return [g for g in self.goals if g.get("status") == STATUS_CANCELLED]
    
    def archived_goals(self) -> List[Dict[str, Any]]:
        """Get all archived goals."""
        return list(self.archived)
    
    def priority_goals(self) -> List[Dict[str, Any]]:
        """Get goals sorted by priority."""
        return sorted(
            self.active_goals(),
            key=lambda g: (
                PRIORITY_WEIGHTS.get(g.get("priority", PRIORITY_NORMAL), 0),
                g.get("progress", 0),
                g.get("created", "")
            ),
            reverse=True
        )
    
    def overdue_goals(self) -> List[Dict[str, Any]]:
        """Get overdue goals."""
        now = datetime.now(timezone.utc)
        result = []
        
        for goal in self.active_goals():
            deadline = goal.get("deadline")
            if not deadline:
                continue
            
            try:
                deadline_text = str(deadline).replace("Z", "+00:00")
                deadline_dt = datetime.fromisoformat(deadline_text)
                if deadline_dt.tzinfo is None:
                    deadline_dt = deadline_dt.replace(tzinfo=timezone.utc)
                if deadline_dt < now:
                    result.append(goal)
            except (TypeError, ValueError):
                continue
        
        return result
    
    def goals_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Filter goals by priority."""
        normalized = self._normalize_priority(priority)
        return [g for g in self.goals if g.get("priority") == normalized]
    
    def goals_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Filter goals by status."""
        status = self._normalize_text(status).upper()
        return [g for g in self.goals if g.get("status") == status]
    
    def goals_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Filter goals by tag."""
        tag = self._normalize_text(tag).lower()
        return [g for g in self.goals if tag in [t.lower() for t in g.get("tags", [])]]
    
    # ========================================================
    # SEARCH
    # ========================================================
    
    def search(self, keyword: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search goals by keyword."""
        keyword = self._normalize_text(keyword).lower()
        if not keyword:
            return []
        
        results = []
        for goal in reversed(self.goals):
            searchable = " ".join([
                str(goal.get("title", "")),
                str(goal.get("description", "")),
                str(goal.get("learning_objective", "")),
                str(goal.get("source_problem", "")),
                " ".join(goal.get("tags", [])),
            ]).lower()
            
            if keyword in searchable:
                results.append(goal)
                if limit is not None and len(results) >= int(limit):
                    break
        
        return results
    
    # ========================================================
    # AUTO-GENERATE
    # ========================================================
    
    def generate_from_problem(self, problem: str) -> Dict[str, Any]:
        """Auto-generate a goal from a system problem."""
        problem = self._normalize_text(problem)
        if not problem:
            raise ValueError("Problem cannot be empty.")
        
        return self.create_goal(
            title=f"Improve {problem}",
            description="Automatically generated from system weakness detection.",
            priority=PRIORITY_HIGH,
            source_problem=problem,
            learning_objective=f"Learn how to improve {problem}.",
            tags=["automatic", "diagnostic", "learning"]
        )
    
    def generate_from_learning(self, objective: str, priority: str = PRIORITY_NORMAL) -> Dict[str, Any]:
        """Auto-generate a goal from a learning objective."""
        objective = self._normalize_text(objective)
        if not objective:
            raise ValueError("Learning objective cannot be empty.")
        
        return self.create_goal(
            title=f"Learn {objective}",
            description="Learning goal generated from an intelligence objective.",
            priority=priority,
            learning_objective=objective,
            tags=["learning", "automatic"]
        )
    
    # ========================================================
    # STATISTICS
    # ========================================================
    
    def summary(self) -> Dict[str, Any]:
        """Get goal summary."""
        active = self.active_goals()
        completed = self.completed_goals()
        paused = self.paused_goals()
        cancelled = self.cancelled_goals()
        overdue = self.overdue_goals()
        
        progress_values = [float(g.get("progress", 0)) for g in self.goals]
        avg_progress = sum(progress_values) / len(progress_values) if progress_values else 0.0
        
        return {
            "total": len(self.goals),
            "active": len(active),
            "completed": len(completed),
            "paused": len(paused),
            "cancelled": len(cancelled),
            "overdue": len(overdue),
            "average_progress": round(avg_progress, 2),
            "completion_rate": round((len(completed) / max(1, len(self.goals))) * 100, 2),
        }
    
    def statistics(self) -> Dict[str, Any]:
        """Get detailed statistics."""
        summary = self.summary()
        
        priority_counts = {
            PRIORITY_LOW: 0,
            PRIORITY_NORMAL: 0,
            PRIORITY_HIGH: 0,
            PRIORITY_CRITICAL: 0,
        }
        
        for goal in self.goals:
            priority = goal.get("priority", PRIORITY_NORMAL)
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        return {
            **summary,
            "priority": priority_counts,
            "total_created": self.total_created,
            "total_completed": self.total_completed,
            "total_cancelled": self.total_cancelled,
            "total_paused": self.total_paused,
            "total_resumed": self.total_resumed,
            "total_progress_updates": self.total_progress_updates,
            "total_milestones": self.total_milestones,
            "total_milestones_completed": self.total_milestones_completed,
            "avg_progress": summary["average_progress"],
        }
    
    def latest(self) -> Optional[Dict[str, Any]]:
        """Get the latest goal."""
        return self.last_goal
    
    def latest_action(self) -> Optional[str]:
        """Get the latest action."""
        return self.last_action
    
    def history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get goal history."""
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = 20
        
        if limit <= 0:
            return []
        
        return self.goals[-limit:]
    
    # ========================================================
    # CLEAR & RESET
    # ========================================================
    
    def clear(self) -> bool:
        """Clear all goals."""
        self.goals.clear()
        self.completed.clear()
        self.archived.clear()
        
        self.goal_count = 0
        self.total_created = 0
        self.total_completed = 0
        self.total_cancelled = 0
        self.total_paused = 0
        self.total_resumed = 0
        self.total_progress_updates = 0
        self.total_milestones = 0
        self.total_milestones_completed = 0
        
        self.last_goal = None
        self.last_action = None
        
        logger.info("Goal Manager cleared.")
        return True
    
    # ========================================================
    # STATUS
    # ========================================================
    
    def status(self) -> Dict[str, Any]:
        """Get system status."""
        summary = self.summary()
        
        return {
            "module": "goal_manager",
            "version": self.VERSION,
            "api_version": API_VERSION,
            "status": "ONLINE",
            "goals": len(self.goals),
            "active": summary["active"],
            "completed": summary["completed"],
            "paused": summary["paused"],
            "cancelled": summary["cancelled"],
            "overdue": summary["overdue"],
            "average_progress": summary["average_progress"],
            "completion_rate": summary["completion_rate"],
            "total_created": self.total_created,
            "total_progress_updates": self.total_progress_updates,
            "has_latest": self.last_goal is not None,
            "timestamp": utc_now(),
        }


# ============================================================
# GLOBAL INSTANCE
# ============================================================

goal_manager = GoalManager()


# ============================================================
# COMPATIBILITY FUNCTIONS
# ============================================================

def create_goal(title, description="", priority="NORMAL", target=None,
                deadline=None, learning_objective=None, source_problem=None,
                tags=None, metadata=None):
    return goal_manager.create_goal(
        title=title, description=description, priority=priority,
        target=target, deadline=deadline, learning_objective=learning_objective,
        source_problem=source_problem, tags=tags, metadata=metadata
    )


def update_progress(goal_id, progress, note=""):
    return goal_manager.update_progress(goal_id, progress, note)


def complete_goal(goal_id, note=""):
    return goal_manager.complete_goal(goal_id, note)


def active_goals():
    return goal_manager.active_goals()


def priority_goals():
    return goal_manager.priority_goals()


def get_goal(goal_id):
    return goal_manager.get_goal(goal_id)


def search(keyword, limit=None):
    return goal_manager.search(keyword, limit)


def status():
    return goal_manager.status()


# ============================================================
# SELF TEST
# ============================================================

def self_test() -> Dict[str, Any]:
    """Run comprehensive self-test."""
    print()
    print("=" * 70)
    print("  GOAL MANAGER v3.0 - SELF TEST")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_failed = 0
    results = {}
    
    # Test 1: Initialization
    print("1. Testing initialization...")
    try:
        manager = GoalManager()
        results["initialization"] = {"status": "PASS"}
        tests_passed += 1
        print("   ✅ Initialization passed")
    except Exception as e:
        results["initialization"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Initialization failed: {e}")
    
    # Test 2: Create Goal
    print("\n2. Testing create_goal...")
    try:
        goal = goal_manager.create_goal(
            title="Test Goal",
            description="Test description",
            priority="HIGH",
            tags=["test", "demo"]
        )
        if goal and goal.get("id"):
            results["create_goal"] = {"status": "PASS", "id": goal["id"]}
            tests_passed += 1
            print(f"   ✅ Create goal passed (ID: {goal['id']})")
        else:
            results["create_goal"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Create goal failed")
    except Exception as e:
        results["create_goal"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Create goal failed: {e}")
    
    # Test 3: Update Progress
    print("\n3. Testing update_progress...")
    try:
        goal_id = goal_manager.active_goals()[0]["id"]
        result = goal_manager.update_progress(goal_id, 50)
        if result and result.get("progress") == 50:
            results["update_progress"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Update progress passed")
        else:
            results["update_progress"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Update progress failed")
    except Exception as e:
        results["update_progress"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Update progress failed: {e}")
    
    # Test 4: Complete Goal
    print("\n4. Testing complete_goal...")
    try:
        goal_id = goal_manager.active_goals()[0]["id"]
        result = goal_manager.complete_goal(goal_id)
        if result:
            results["complete_goal"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Complete goal passed")
        else:
            results["complete_goal"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Complete goal failed")
    except Exception as e:
        results["complete_goal"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Complete goal failed: {e}")
    
    # Test 5: Statistics
    print("\n5. Testing statistics...")
    try:
        stats = goal_manager.statistics()
        if stats and "total" in stats:
            results["statistics"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Statistics passed")
        else:
            results["statistics"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Statistics failed")
    except Exception as e:
        results["statistics"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Statistics failed: {e}")
    
    # Test 6: Status
    print("\n6. Testing status...")
    try:
        status_result = goal_manager.status()
        if status_result and "status" in status_result:
            results["status"] = {"status": "PASS"}
            tests_passed += 1
            print("   ✅ Status passed")
        else:
            results["status"] = {"status": "FAIL"}
            tests_failed += 1
            print("   ❌ Status failed")
    except Exception as e:
        results["status"] = {"status": "FAIL", "error": str(e)}
        tests_failed += 1
        print(f"   ❌ Status failed: {e}")
    
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
        "module": "goal_manager",
        "version": GOAL_MANAGER_VERSION,
        "status": "PASS" if tests_failed == 0 else "FAIL",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "details": results,
    }


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "GoalManager",
    "goal_manager",
    "create_goal",
    "update_progress",
    "complete_goal",
    "active_goals",
    "priority_goals",
    "get_goal",
    "search",
    "status",
    "self_test",
    "GOAL_MANAGER_VERSION",
    "API_VERSION",
    "PRIORITY_LOW",
    "PRIORITY_NORMAL",
    "PRIORITY_HIGH",
    "PRIORITY_CRITICAL",
    "STATUS_ACTIVE",
    "STATUS_COMPLETED",
    "STATUS_PAUSED",
    "STATUS_CANCELLED",
    "STATUS_ARCHIVED",
]


# ============================================================
# END
# ============================================================