# ============================================================
# gui/page.py
# BASE INTELLIGENCE PAGE
# SUPER COMPREHENSIVE BASE CLASS
# ============================================================

import customtkinter as ctk
from typing import Optional, Any, Dict, List, Callable
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# ============================================================
# FIX: Lazy font loading
# ============================================================

def get_default_font(size=20):
    try:
        return ctk.CTkFont(size=size)
    except RuntimeError:
        return None


class IntelligencePage(ctk.CTkFrame):
    """
    Super Comprehensive Base class for all Intelligence pages.
    
    Features:
    - Automatic update loop with configurable interval
    - Bot, Brain, Consciousness, Learning integration
    - Status tracking (connected, errors, updates)
    - Error handling and logging
    - Lifecycle hooks (on_show, on_hide, on_update)
    - Performance metrics
    - Health status
    - Safe font loading
    """
    
    def __init__(
        self,
        parent,
        bot=None,
        learning_integration=None,
        **kwargs
    ):
        # ============================================================
        # FIX: Set attributes BEFORE calling super()
        # ============================================================
        
        self._initialized = False
        self._is_destroyed = False
        
        # ============================================================
        # REFERENCES
        # ============================================================
        
        self.bot = bot
        self.learning_integration = learning_integration
        
        # Try to get brain from various sources
        self.brain = None
        if bot:
            if hasattr(bot, 'brain'):
                self.brain = bot.brain
            elif hasattr(bot, '_brain'):
                self.brain = bot._brain
        
        # Try to get consciousness
        self.consciousness = None
        try:
            from core.consciousness import consciousness
            self.consciousness = consciousness
        except ImportError:
            pass
        
        # ============================================================
        # STATUS & METRICS
        # ============================================================
        
        self.is_connected = False
        self.last_error: Optional[str] = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = 3000  # 3 seconds default
        self.last_update_time: Optional[datetime] = None
        self.update_durations: List[float] = []
        
        # ============================================================
        # HEALTH & PERFORMANCE
        # ============================================================
        
        self.health_score = 100.0
        self.performance_metrics: Dict[str, Any] = {}
        self.page_status = "INITIALIZING"
        
        # ============================================================
        # CALL SUPER
        # ============================================================
        
        super().__init__(parent, **kwargs)
        
        # ============================================================
        # BUILD UI
        # ============================================================
        
        self._build_ui()
        
        # ============================================================
        # START UPDATES
        # ============================================================
        
        self._start_updates()
        
        self._initialized = True
        logger.debug(f"[{self.__class__.__name__}] Initialized")
    
    # ============================================================
    # UI BUILDING
    # ============================================================
    
    def _build_ui(self):
        """
        Build page UI - override in child classes.
        """
        # Configure grid for all pages
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Default: empty page
        self._create_empty_page()
    
    def _create_empty_page(self):
        """Create empty page placeholder."""
        # FIX: Safe font loading
        font = get_default_font(20) or ("Segoe UI", 20)
        
        label = ctk.CTkLabel(
            self,
            text=f"📄 {self.__class__.__name__}\n\nPage under construction...",
            font=font,
            text_color="#5F6B78"
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
    
    # ============================================================
    # UPDATE LOOP
    # ============================================================
    
    def _start_updates(self):
        """Start periodic updates."""
        if self.is_running and not self._is_destroyed:
            self.update_data()
    
    def update_data(self):
        """
        Update page data - override in child classes.
        """
        # FIX: Check if destroyed before updating
        if not self.is_running or self._is_destroyed:
            return
        
        try:
            # Check if widget still exists
            if not self.winfo_exists():
                self.is_running = False
                return
        except Exception:
            self.is_running = False
            return
        
        start_time = datetime.now()
        
        try:
            # Update metrics
            self.update_count += 1
            
            # Update health
            self._update_health()
            
            # Update performance metrics
            self._update_performance_metrics()
            
            # Update connection status
            self._update_connection_status()
            
            self.success_count += 1
            self.is_connected = True
            self.page_status = "ONLINE"
            
            # Call on_update hook
            self.on_update()
            
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.is_connected = False
            self.page_status = "ERROR"
            logger.error(f"[{self.__class__.__name__}] Update error: {e}")
        
        # Track duration
        duration = (datetime.now() - start_time).total_seconds()
        self.update_durations.append(duration)
        if len(self.update_durations) > 100:
            self.update_durations = self.update_durations[-100:]
        
        self.last_update_time = datetime.now()
        
        # Schedule next update
        if self.is_running and not self._is_destroyed:
            try:
                self.after(self.update_interval, self.update_data)
            except Exception:
                pass
    
    def _update_health(self):
        """Update health score."""
        # Start with 100
        health = 100.0
        
        # Deduct for errors
        if self.error_count > 0:
            health -= min(30, self.error_count * 2)
        
        # Deduct for disconnection
        if not self.is_connected:
            health -= 20
        
        # Add for success rate
        if self.update_count > 0:
            success_rate = (self.success_count / max(1, self.update_count)) * 100
            health += (success_rate - 50) * 0.2
        
        # Ensure range
        self.health_score = max(0.0, min(100.0, health))
    
    def _update_performance_metrics(self):
        """Update performance metrics."""
        avg_duration = 0
        if self.update_durations:
            avg_duration = sum(self.update_durations) / len(self.update_durations)
        
        self.performance_metrics = {
            "total_updates": self.update_count,
            "successful_updates": self.success_count,
            "failed_updates": self.error_count,
            "success_rate": (self.success_count / max(1, self.update_count)) * 100,
            "avg_update_duration_ms": round(avg_duration * 1000, 2),
            "health_score": self.health_score,
            "status": self.page_status,
        }
    
    def _update_connection_status(self):
        """Update connection status."""
        # Check bot connection
        if self.bot is not None:
            try:
                if hasattr(self.bot, 'is_running'):
                    self.is_connected = self.bot.is_running()
                elif hasattr(self.bot, 'running'):
                    self.is_connected = self.bot.running
            except Exception:
                pass
        
        # Check brain connection
        if self.brain is not None and self.is_connected:
            try:
                if hasattr(self.brain, 'is_healthy'):
                    self.is_connected = self.brain.is_healthy()
            except Exception:
                pass
    
    # ============================================================
    # GETTERS
    # ============================================================
    
    def get_status(self) -> Dict[str, Any]:
        """Get page status."""
        return {
            "page": self.__class__.__name__,
            "status": self.page_status,
            "connected": self.is_connected,
            "update_count": self.update_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "health_score": self.health_score,
            "last_update": self.last_update_time.isoformat() if self.last_update_time else None,
            "last_error": self.last_error,
            "performance": self.performance_metrics,
            "has_bot": self.bot is not None,
            "has_brain": self.brain is not None,
            "has_consciousness": self.consciousness is not None,
            "has_learning": self.learning_integration is not None,
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        avg_duration = 0
        if self.update_durations:
            avg_duration = sum(self.update_durations) / len(self.update_durations)
        
        return {
            "total_updates": self.update_count,
            "successful_updates": self.success_count,
            "failed_updates": self.error_count,
            "success_rate": (self.success_count / max(1, self.update_count)) * 100,
            "avg_update_duration": avg_duration,
            "update_interval": self.update_interval,
            "health_score": self.health_score,
            "page_status": self.page_status,
        }
    
    def get_health(self) -> Dict[str, Any]:
        """Get health status."""
        return {
            "page": self.__class__.__name__,
            "health_score": self.health_score,
            "status": self.page_status,
            "connected": self.is_connected,
            "errors": self.error_count,
            "last_error": self.last_error,
            "last_update": self.last_update_time.isoformat() if self.last_update_time else None,
            "components": {
                "bot": self.bot is not None,
                "brain": self.brain is not None,
                "consciousness": self.consciousness is not None,
                "learning": self.learning_integration is not None,
            }
        }
    
    # ============================================================
    # SETTERS
    # ============================================================
    
    def set_bot(self, bot):
        """Set bot reference."""
        self.bot = bot
        if bot:
            if hasattr(bot, 'brain'):
                self.brain = bot.brain
            elif hasattr(bot, '_brain'):
                self.brain = bot._brain
        self._on_reference_changed()
    
    def set_learning(self, learning):
        """Set learning integration reference."""
        self.learning_integration = learning
        self._on_reference_changed()
    
    def set_brain(self, brain):
        """Set brain reference directly."""
        self.brain = brain
    
    def set_brain_instance(self, brain):
        """Set brain instance reference (alias)."""
        self.brain = brain
    
    def set_update_interval(self, interval_ms: int):
        """Set update interval in milliseconds."""
        self.update_interval = max(500, interval_ms)
    
    def _on_reference_changed(self):
        """Called when references are updated."""
        pass
    
    # ============================================================
    # LIFECYCLE HOOKS
    # ============================================================
    
    def on_show(self):
        """
        Called when page is shown.
        Override in child classes.
        """
        self.page_status = "ACTIVE"
        logger.debug(f"[{self.__class__.__name__}] Shown")
    
    def on_hide(self):
        """
        Called when page is hidden.
        Override in child classes.
        """
        self.page_status = "HIDDEN"
        logger.debug(f"[{self.__class__.__name__}] Hidden")
    
    def on_update(self):
        """
        Called after each update cycle.
        Override in child classes.
        """
        pass
    
    # ============================================================
    # ERROR HANDLING
    # ============================================================
    
    def show_error(self, error: str):
        """Show error in UI."""
        self.last_error = error
        self.error_count += 1
        self.is_connected = False
        
        # Override in child to show error in UI
        pass
    
    def clear_error(self):
        """Clear last error."""
        self.last_error = None
    
    # ============================================================
    # UTILITY METHODS
    # ============================================================
    
    def safe_execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Safely execute a function with error handling.
        
        Args:
            func: Function to execute
            *args, **kwargs: Arguments to pass
            
        Returns:
            Function result or None if error
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.show_error(str(e))
            logger.error(f"[{self.__class__.__name__}] Execute error: {e}")
            return None
    
    def is_healthy(self) -> bool:
        """Check if page is healthy."""
        return self.health_score > 50 and self.is_connected
    
    # ============================================================
    # CONTROL METHODS
    # ============================================================
    
    def refresh(self):
        """Force refresh."""
        if not self._is_destroyed:
            self.update_data()
    
    def stop(self):
        """Stop updates."""
        self.is_running = False
        self.page_status = "STOPPED"
        logger.debug(f"[{self.__class__.__name__}] Stopped")
    
    def start(self):
        """Start updates."""
        if not self.is_running and not self._is_destroyed:
            self.is_running = True
            self.page_status = "ACTIVE"
            self._start_updates()
            logger.debug(f"[{self.__class__.__name__}] Started")
    
    def reset_metrics(self):
        """Reset all metrics."""
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.health_score = 100.0
        self.last_error = None
        self.update_durations = []
        logger.debug(f"[{self.__class__.__name__}] Metrics reset")
    
    # ============================================================
    # CLEANUP
    # ============================================================
    
    def destroy(self):
        """Cleanup on destroy."""
        if self._is_destroyed:
            return
        
        self._is_destroyed = True
        self.is_running = False
        self.page_status = "DESTROYED"
        
        # Clear update durations
        self.update_durations.clear()
        
        # Clear references
        self.bot = None
        self.brain = None
        self.consciousness = None
        self.learning_integration = None
        
        logger.debug(f"[{self.__class__.__name__}] Destroyed")
        
        try:
            super().destroy()
        except Exception:
            pass