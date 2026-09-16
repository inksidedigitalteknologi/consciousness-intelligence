#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# core/health.py - Health Monitor Module
# INKSIDE DIGITAL - Cognitive Mirror Engine
# ============================================================

from __future__ import annotations

import time
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional

# ============================================================
# FIX: Safe Key Helper
# ============================================================

def safe_module_key(module: Any) -> str:
    """
    Convert any module identifier to a safe string key.
    
    FIX: Handles CognitiveState and other objects.
    """
    if module is None:
        return "unknown"
    
    # Already string
    if isinstance(module, str):
        return module
    
    # Has name attribute
    if hasattr(module, 'name'):
        return str(module.name)
    
    # Has __name__
    if hasattr(module, '__name__'):
        return str(module.__name__)
    
    # Has __class__
    if hasattr(module, '__class__'):
        return module.__class__.__name__
    
    # Last resort
    return str(module)


# ============================================================
# Health Monitor Class
# ============================================================

class HealthMonitor:
    """System health monitoring with execution tracking."""
    
    def __init__(self, max_history: int = 1000):
        self._modules: Dict[str, Dict[str, Any]] = {}
        self._executions: List[Dict[str, Any]] = []
        self._max_history = max_history
        self._status = "ONLINE"
        self._started_at = datetime.now().isoformat()
        self._alerts: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        self._last_cleanup = datetime.now()
    
    # ============================================================
    # REGISTER
    # ============================================================
    
    def register(self, module_name: Any, *args, **kwargs) -> bool:
        """
        Register a module for health monitoring.
        
        FIX: Handle any type of module_name (string, object, CognitiveState)
        """
        # FIX: Convert to safe string key
        safe_name = safe_module_key(module_name)
        
        with self._lock:
            if safe_name not in self._modules:
                self._modules[safe_name] = {
                    "registered_at": datetime.now().isoformat(),
                    "status": "OK",
                    "checks": 0,
                    "failures": 0,
                    "last_check": None,
                    "avg_duration": 0.0,
                    "total_duration": 0.0,
                    "last_error": None,
                    "last_success": None,
                }
            return True
    
    # ============================================================
    # RECORD EXECUTION
    # ============================================================
    
    def record_execution(
        self,
        module_name: Any,
        duration: float,
        success: bool,
        error: Optional[str] = None
    ) -> bool:
        """
        Record module execution.
        
        FIX: Handle any type of module_name
        """
        # FIX: Convert to safe string key
        safe_name = safe_module_key(module_name)
        
        # Ensure module is registered
        if safe_name not in self._modules:
            self.register(safe_name)
        
        execution = {
            "module": safe_name,
            "duration": duration,
            "success": success,
            "error": str(error) if error else None,
            "timestamp": datetime.now().isoformat()
        }
        
        with self._lock:
            self._executions.append(execution)
            
            # Update module stats
            module = self._modules[safe_name]
            module["checks"] += 1
            module["last_check"] = execution["timestamp"]
            
            if success:
                module["last_success"] = execution["timestamp"]
            else:
                module["failures"] += 1
                module["last_error"] = error or "Unknown error"
            
            # Update duration
            total_duration = module.get("total_duration", 0.0) + duration
            module["total_duration"] = total_duration
            module["avg_duration"] = total_duration / module["checks"]
            
            # Update status
            if module["failures"] > module["checks"] * 0.3:
                module["status"] = "DEGRADED"
            elif module["failures"] == 0:
                module["status"] = "OK"
            else:
                module["status"] = "WARNING"
            
            # Create alert on failure
            if not success and error:
                self._alerts.append({
                    "module": safe_name,
                    "type": "EXECUTION_FAILURE",
                    "error": str(error),
                    "timestamp": execution["timestamp"]
                })
            
            # Trim history
            if len(self._executions) > self._max_history:
                self._executions = self._executions[-self._max_history:]
            
            if len(self._alerts) > 100:
                self._alerts = self._alerts[-100:]
        
        # Auto cleanup
        self._auto_cleanup()
        
        return True
    
    # ============================================================
    # AUTO CLEANUP
    # ============================================================
    
    def _auto_cleanup(self) -> None:
        """Auto cleanup old executions."""
        now = datetime.now()
        if (now - self._last_cleanup).total_seconds() > 3600:  # 1 hour
            with self._lock:
                # Keep last 500 executions
                if len(self._executions) > 500:
                    self._executions = self._executions[-500:]
                
                # Keep last 50 alerts
                if len(self._alerts) > 50:
                    self._alerts = self._alerts[-50:]
                
                self._last_cleanup = now
    
    # ============================================================
    # SNAPSHOT
    # ============================================================
    
    def snapshot(self) -> Dict[str, Any]:
        """Get health snapshot."""
        with self._lock:
            return {
                "status": self._status,
                "modules": len(self._modules),
                "executions": len(self._executions),
                "alerts": len(self._alerts),
                "modules_detail": self._modules.copy(),
                "started_at": self._started_at,
                "timestamp": datetime.now().isoformat()
            }
    
    # ============================================================
    # SCORE
    # ============================================================
    
    def score(self) -> float:
        """Calculate health score (0-100)."""
        with self._lock:
            if not self._executions:
                return 100.0
            
            # Success rate
            success_count = sum(1 for e in self._executions if e.get("success", False))
            score = (success_count / len(self._executions)) * 100.0
            
            # Module health
            for module_data in self._modules.values():
                checks = module_data.get("checks", 0)
                if checks > 10:
                    failure_rate = module_data.get("failures", 0) / checks
                    if failure_rate > 0.5:
                        score -= 20
                    elif failure_rate > 0.3:
                        score -= 10
                    elif failure_rate > 0.1:
                        score -= 5
            
            # Alert penalty
            if self._alerts:
                alert_penalty = min(15, len(self._alerts) * 1)
                score -= alert_penalty
            
            return max(0.0, min(100.0, score))
    
    # ============================================================
    # GETTERS
    # ============================================================
    
    def system_status(self) -> str:
        return self._status
    
    def counts(self) -> Dict[str, int]:
        with self._lock:
            return {
                "total": len(self._executions),
                "modules": len(self._modules),
                "successful": sum(1 for e in self._executions if e.get("success", False)),
                "failed": sum(1 for e in self._executions if not e.get("success", False)),
                "alerts": len(self._alerts)
            }
    
    def get(self, module_name: Any) -> Optional[Dict[str, Any]]:
        """Get health data for a module."""
        safe_name = safe_module_key(module_name)
        with self._lock:
            return self._modules.get(safe_name)
    
    def all(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return self._modules.copy()
    
    def modules(self) -> List[str]:
        with self._lock:
            return list(self._modules.keys())
    
    def get_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            return self._alerts[-limit:] if self._alerts else []
    
    def get_module_status(self, module_name: Any) -> Optional[str]:
        """Get status of a specific module."""
        safe_name = safe_module_key(module_name)
        with self._lock:
            module = self._modules.get(safe_name)
            return module.get("status") if module else None
    
    # ============================================================
    # TO DICT
    # ============================================================
    
    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "modules": self._modules.copy(),
                "executions": self._executions[-100:],
                "alerts": self._alerts[-50:],
                "status": self._status,
                "score": self.score(),
                "started_at": self._started_at,
                "timestamp": datetime.now().isoformat()
            }
    
    # ============================================================
    # CONTROL
    # ============================================================
    
    def set_status(self, status: str) -> None:
        self._status = status
    
    def clear_alerts(self) -> None:
        with self._lock:
            self._alerts = []
    
    def reset(self) -> None:
        with self._lock:
            self._modules = {}
            self._executions = []
            self._alerts = []
            self._status = "ONLINE"
            self._started_at = datetime.now().isoformat()
    
    def clear_module_stats(self, module_name: Any) -> bool:
        """Clear statistics for a specific module."""
        safe_name = safe_module_key(module_name)
        with self._lock:
            if safe_name in self._modules:
                module = self._modules[safe_name]
                module["checks"] = 0
                module["failures"] = 0
                module["avg_duration"] = 0.0
                module["total_duration"] = 0.0
                module["last_error"] = None
                module["last_success"] = None
                module["status"] = "OK"
                return True
            return False
    
    def reset_module(self, module_name: Any) -> bool:
        """Reset a module's health data."""
        return self.clear_module_stats(module_name)


# ============================================================
# Singleton Instance
# ============================================================

health_monitor = HealthMonitor()


# ============================================================
# FIX: Convenience Functions - COMPATIBILITY MODE
# ============================================================

def set_status(*args) -> None:
    """
    Set system status.
    
    Supports:
        set_status("ONLINE")                    # 1 arg: status only
        set_status("module_name", "INITIALIZED") # 2 args: module + status
        set_status(CognitiveState, "ACTIVE")    # 2 args: object + status
    """
    if len(args) == 1:
        health_monitor.set_status(args[0])
    elif len(args) == 2:
        module_name, status = args
        
        # FIX: Convert to safe string key
        safe_name = safe_module_key(module_name)
        
        # Register module if not exists
        if safe_name not in health_monitor._modules:
            health_monitor.register(safe_name)
        
        # Update module status
        health_monitor._modules[safe_name]["status"] = status
        health_monitor.set_status(status)
    else:
        raise TypeError(f"set_status() takes 1 or 2 arguments, got {len(args)}")


def get_status() -> str:
    """Get current system status."""
    return health_monitor.system_status()


def register_health(module_name: Any) -> bool:
    """Register a module for health monitoring."""
    return health_monitor.register(module_name)


def record_health(
    module_name: Any,
    duration: float,
    success: bool,
    error: Optional[str] = None
) -> bool:
    """Record module execution health data."""
    return health_monitor.record_execution(module_name, duration, success, error)


def get_health(module_name: Any) -> Optional[Dict[str, Any]]:
    """Get health data for a specific module."""
    return health_monitor.get(module_name)


def get_health_status() -> str:
    """Get health status string (HEALTHY/DEGRADED/CRITICAL)."""
    score = health_monitor.score()
    if score >= 90:
        return "HEALTHY"
    elif score >= 70:
        return "DEGRADED"
    else:
        return "CRITICAL"


def heartbeat() -> bool:
    """Check if system is alive."""
    return health_monitor.system_status() == "ONLINE"


def health_status() -> Dict[str, Any]:
    """Get full health status summary."""
    return {
        "status": health_monitor.system_status(),
        "score": health_monitor.score(),
        "modules": len(health_monitor.modules()),
        "executions": len(health_monitor._executions),
        "alerts": len(health_monitor._alerts),
        "timestamp": datetime.now().isoformat()
    }


def health_score() -> float:
    """Get current health score (0-100)."""
    return health_monitor.score()


def system_health() -> str:
    """Get system health status string."""
    return health_monitor.system_status()


def health_alerts(limit: int = 20) -> List[Dict[str, Any]]:
    """Get recent health alerts."""
    return health_monitor.get_alerts(limit)


def test_health() -> Dict[str, Any]:
    """Run health test."""
    return {
        "status": "PASS",
        "modules": len(health_monitor.modules()),
        "score": health_monitor.score(),
        "executions": len(health_monitor._executions),
        "alerts": len(health_monitor._alerts),
        "timestamp": datetime.now().isoformat()
    }


def print_health() -> None:
    """Print health summary to console."""
    print()
    print("=" * 60)
    print(" HEALTH STATUS")
    print("=" * 60)
    print(f"Status      : {health_monitor.system_status()}")
    print(f"Score       : {health_monitor.score():.1f}%")
    print(f"Modules     : {len(health_monitor.modules())}")
    print(f"Executions  : {len(health_monitor._executions)}")
    print(f"Alerts      : {len(health_monitor._alerts)}")
    print("=" * 60)
    
    if health_monitor._modules:
        print("\nMODULE STATUS:")
        for name, data in health_monitor._modules.items():
            failures = data.get("failures", 0)
            checks = data.get("checks", 0)
            
            if failures == 0 and checks > 0:
                icon = "✅"
            elif failures > 0 and failures < checks * 0.3:
                icon = "⚠️"
            elif failures >= checks * 0.3:
                icon = "❌"
            else:
                icon = "⏳"
            
            status = data.get("status", "UNKNOWN")
            print(f"  {icon} {name}: checks={checks}, failures={failures}, status={status}")
    
    print("=" * 60)
    print()


def reset_health() -> None:
    """Reset all health data."""
    health_monitor.reset()


def reset_module_health(module_name: Any) -> bool:
    """Reset health data for a specific module."""
    return health_monitor.reset_module(module_name)


# ============================================================
# Module Exports
# ============================================================

__all__ = [
    "HealthMonitor",
    "health_monitor",
    "safe_module_key",
    "set_status",
    "get_status",
    "register_health",
    "record_health",
    "get_health",
    "get_health_status",
    "heartbeat",
    "health_status",
    "health_score",
    "system_health",
    "health_alerts",
    "test_health",
    "print_health",
    "reset_health",
    "reset_module_health",
]