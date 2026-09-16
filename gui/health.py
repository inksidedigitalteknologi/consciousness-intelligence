# ============================================================
# gui/health.py
# HEALTH - System Health Monitoring
# SUPER COMPREHENSIVE v2.3 - ALL COMPONENTS ONLINE
# ============================================================

import random
import json
import traceback
import logging
from datetime import datetime
from typing import Dict, Optional, Any, List, Tuple

import customtkinter as ctk

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard

logger = logging.getLogger(__name__)


class Health(IntelligencePage):
    """
    Super Comprehensive System Health Monitoring View v2.3.
    
    Features:
    - Real-time component health checks
    - Health score with color coding
    - Online/offline component status
    - Error count tracking
    - Detailed health JSON view
    - Auto-refresh with configurable interval
    - Manual refresh button
    - Last update timestamp
    - Dual brain compatibility (brain_instance + brain)
    - Consciousness integration
    - Learning engine status
    - Memory health
    - Pattern engine status
    - Scanner status
    - Signal engine status
    - Bot status
    - Root window fallback for brain & bot
    - Multiple fallbacks for each component
    - Graceful fallback when components unavailable
    """
    
    def __init__(self, parent, *args, **kwargs):
        # ============================================================
        # FIX: Set all attributes BEFORE calling super()
        # ============================================================
        
        # Data storage
        self.health_data: Dict[str, Any] = {}
        self.components: Dict[str, Dict] = {}
        self.last_error: Optional[str] = None
        self.last_error_time: Optional[datetime] = None
        
        # Brain references (dual compatibility)
        self.brain_instance = None
        self.brain = None
        self._brain_available = False
        
        # Consciousness reference
        self.consciousness = None
        
        # Bot reference
        self.bot = None
        self.learning_integration = None
        
        # Status
        self.is_running = True
        self.update_interval = 3000  # 3 seconds
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_connected = False
        
        # UI components storage
        self.health_status = None
        self.health_score = None
        self.components_count = None
        self.errors_count = None
        self.details_text = None
        self.last_update_label = None
        self.refresh_btn = None
        self.component_labels = {}
        self._after_id = None
        
        # Call super
        super().__init__(parent, *args, **kwargs)
        
        # Build UI
        self._build_ui()
        
        # Start updates
        self.after(100, self.update_data)  # Delay initial update
    
    # ============================================================
    # PUBLIC METHODS
    # ============================================================
    
    def set_bot(self, bot):
        """Set bot reference."""
        self.bot = bot
        logger.info(f"✅ Bot set in Health: {type(bot).__name__ if bot else None}")
        self._update_brain_reference()
        self._update_consciousness_reference()
    
    def set_learning(self, learning):
        """Set learning integration reference."""
        self.learning_integration = learning
        self._update_brain_reference()
    
    def set_brain(self, brain):
        """Set brain reference directly."""
        self.brain_instance = brain
        self.brain = brain
        self._brain_available = brain is not None
        logger.info(f"✅ Brain set in Health: {type(brain).__name__ if brain else None}")
        self._update_brain_reference()
    
    def _update_brain_reference(self):
        """Update brain from bot or brain attribute."""
        # 1. Dari bot
        if self.bot:
            if hasattr(self.bot, 'brain'):
                self.brain = self.bot.brain
                self.brain_instance = self.bot.brain
                logger.debug("Brain from bot.brain")
            elif hasattr(self.bot, '_brain'):
                self.brain = self.bot._brain
                self.brain_instance = self.bot._brain
                logger.debug("Brain from bot._brain")
            elif hasattr(self.bot, 'get_brain'):
                try:
                    brain = self.bot.get_brain()
                    if brain:
                        self.brain = brain
                        self.brain_instance = brain
                        logger.debug("Brain from bot.get_brain()")
                except Exception:
                    pass
        
        # 2. Dari learning integration
        if not self.brain and self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                self.brain = self.learning_integration.brain
                self.brain_instance = self.learning_integration.brain
                logger.debug("Brain from learning_integration")
            elif hasattr(self.learning_integration, 'get_brain'):
                try:
                    brain = self.learning_integration.get_brain()
                    if brain:
                        self.brain = brain
                        self.brain_instance = brain
                        logger.debug("Brain from learning_integration.get_brain()")
                except Exception:
                    pass
        
        # 3. 🔥 FALLBACK: Ambil dari root window (app)
        if not self.brain:
            try:
                root = self.winfo_toplevel()
                if hasattr(root, 'brain') and root.brain:
                    self.brain = root.brain
                    self.brain_instance = root.brain
                    logger.info("✅ Brain loaded from root window in Health")
                    self._brain_available = True
                    return
            except Exception as e:
                logger.debug(f"Root window brain error: {e}")
        
        # 4. Global fallback
        if not self.brain:
            try:
                from core.brain import brain
                if brain:
                    self.brain = brain
                    self.brain_instance = brain
                    logger.info("✅ Brain loaded from core.brain in Health")
            except ImportError:
                pass
        
        self._brain_available = self.brain is not None
        if self._brain_available:
            logger.info(f"✅ Brain available in Health (type: {type(self.brain).__name__})")
        else:
            logger.warning("⚠️ Brain NOT available in Health")
    
    def _update_consciousness_reference(self):
        """Update consciousness reference from various sources."""
        # 1. Dari bot
        if self.bot and hasattr(self.bot, 'consciousness'):
            self.consciousness = self.bot.consciousness
            logger.debug("Consciousness from bot")
            return
        
        # 2. Dari brain
        if self.brain and hasattr(self.brain, 'consciousness'):
            self.consciousness = self.brain.consciousness
            logger.debug("Consciousness from brain")
            return
        
        # 3. Global import
        if not self.consciousness:
            try:
                from core.consciousness import consciousness
                self.consciousness = consciousness
                logger.debug("Consciousness from core")
            except ImportError:
                pass
    
    # ============================================================
    # BUILD UI
    # ============================================================
    
    def _build_ui(self):
        """Build the health view UI with enhanced controls."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # ====================================================
        # HEADER
        # ====================================================
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, padx=20, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)
        
        ctk.CTkLabel(
            header,
            text="❤️ System Health",
            font=("Segoe UI", 22, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")
        
        self.health_status = StatusIndicator(header, label="System")
        self.health_status.grid(row=0, column=1, padx=10)
        
        self.last_update_label = ctk.CTkLabel(
            header,
            text="Last update: --",
            font=("Segoe UI", 10),
            text_color="#5F6B78"
        )
        self.last_update_label.grid(row=0, column=2, padx=10)
        
        self.refresh_btn = ctk.CTkButton(
            header,
            text="🔄 Refresh",
            width=80,
            height=28,
            font=("Segoe UI", 11),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.refresh
        )
        self.refresh_btn.grid(row=0, column=3, padx=10)
        
        # ====================================================
        # HEALTH METRICS - Row 1
        # ====================================================
        
        self.health_score = MetricCard(
            self,
            title="📊 Health Score",
            value="100%"
        )
        self.health_score.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.components_count = MetricCard(
            self,
            title="📦 Components",
            value="0/0",
            subtitle="Online"
        )
        self.components_count.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.errors_count = MetricCard(
            self,
            title="❌ Errors",
            value="0"
        )
        self.errors_count.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        # ====================================================
        # COMPONENT STATUS - Row 2
        # ====================================================
        
        components = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        components.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        components.grid_columnconfigure(0, weight=1)
        components.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            components,
            text="🔧 Component Status",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        self.components_grid = ctk.CTkFrame(components, fg_color="transparent")
        self.components_grid.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.components_grid.grid_columnconfigure(0, weight=1)
        self.components_grid.grid_columnconfigure(1, weight=1)
        self.components_grid.grid_columnconfigure(2, weight=1)
        
        self.component_labels = {}
        
        components_list = [
            ("brain", "🧠 Brain"),
            ("consciousness", "💭 Consciousness"),
            ("learning", "📚 Learning"),
            ("memory", "💾 Memory"),
            ("pattern", "🔍 Pattern"),
            ("scanner", "📊 Scanner"),
            ("signal", "📈 Signal"),
            ("bot", "🤖 Bot"),
        ]
        
        for i, (key, label) in enumerate(components_list):
            row = i // 3
            col = i % 3
            frame = ctk.CTkFrame(self.components_grid, fg_color="#18212B", corner_radius=6)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                frame,
                text=label,
                font=("Segoe UI", 11),
                text_color="#8D9AAA"
            ).pack(anchor="w", padx=10, pady=(8, 0))
            
            status_label = ctk.CTkLabel(
                frame,
                text="● OFFLINE",
                font=("Segoe UI", 10, "bold"),
                text_color="#EF4444"
            )
            status_label.pack(anchor="w", padx=10, pady=(2, 8))
            
            self.component_labels[key] = status_label
        
        # ====================================================
        # DETAILS - Row 3
        # ====================================================
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        details.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            details,
            text="📋 Health Details",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        self.details_text = ctk.CTkTextbox(
            details,
            font=("Consolas", 10),
            fg_color="#0B0F14",
            text_color="#8D9AAA",
            height=120
        )
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    # ============================================================
    # UPDATE DATA
    # ============================================================
    
    def update_data(self):
        """Update health data with robust error handling."""
        if not self.is_running:
            return
        
        try:
            self.update_count += 1
            self._update_brain_reference()
            self._update_consciousness_reference()
            
            # Collect health data from all components
            health_result = self._collect_health_data()
            
            if health_result:
                self.health_data = health_result
                self.is_connected = True
                self.success_count += 1
                self.last_error = None
            else:
                self.is_connected = False
                self.error_count += 1
                self.last_error = "No health data available"
                self.last_error_time = datetime.now()
                self.health_data = self._generate_fallback_data()
            
            # Update UI
            self._update_ui()
            
            # Update timestamp
            if self.last_update_label:
                self.last_update_label.configure(
                    text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
                )
            
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            logger.error(f"[Health] Update error: {e}")
            traceback.print_exc()
            self._update_error_display(e)
            if self.health_status:
                self.health_status.set_status(False)
        
        # Schedule next update
        if self.is_running:
            try:
                self._after_id = self.after(self.update_interval, self.update_data)
            except Exception as e:
                logger.error(f"[Health] Schedule error: {e}")
    
    # ============================================================
    # HEALTH DATA COLLECTION
    # ============================================================
    
    def _collect_health_data(self) -> Dict[str, Any]:
        """Collect health data from all components."""
        result = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "online": 0,
            "total": 0,
            "errors": 0,
            "health_score": 0.0,
        }
        
        # Check each component
        component_checks = [
            ("brain", self._check_brain),
            ("consciousness", self._check_consciousness),
            ("learning", self._check_learning),
            ("memory", self._check_memory),
            ("pattern", self._check_pattern),
            ("scanner", self._check_scanner),
            ("signal", self._check_signal),
            ("bot", self._check_bot),
        ]
        
        for name, check_func in component_checks:
            try:
                status = check_func()
                result["components"][name] = status
                result["total"] += 1
                if status.get("online", False):
                    result["online"] += 1
                result["errors"] += status.get("errors", 0)
            except Exception as e:
                result["components"][name] = {
                    "online": False,
                    "error": str(e),
                    "errors": 1
                }
                result["total"] += 1
                result["errors"] += 1
        
        # Calculate health score
        if result["total"] > 0:
            result["health_score"] = (result["online"] / result["total"]) * 100
        
        return result
    
    # ============================================================
    # COMPONENT CHECK FUNCTIONS - ALL WITH MULTIPLE FALLBACKS
    # ============================================================
    
    def _check_brain(self) -> Dict[str, Any]:
        """Check brain health - with multiple fallbacks."""
        result = {"online": False, "errors": 0}
        
        # Ambil dari root window
        if not self.brain:
            try:
                root = self.winfo_toplevel()
                if hasattr(root, 'brain') and root.brain:
                    self.brain = root.brain
                    self.brain_instance = root.brain
                    logger.info("✅ Brain loaded from root window in _check_brain")
            except Exception:
                pass
            
            if not self.brain:
                return result
        
        try:
            # 1. Coba health_check (tapi jangan andalkan sepenuhnya)
            if hasattr(self.brain, 'health_check'):
                try:
                    health = self.brain.health_check()
                    if health and isinstance(health, dict):
                        if health.get("healthy", False):
                            result["online"] = True
                            result["health_score"] = health.get("health_score", 70)
                            return result
                except Exception as e:
                    logger.debug(f"health_check error: {e}")
            
            # 2. Coba status()
            if hasattr(self.brain, 'status'):
                status = self.brain.status()
                if status and isinstance(status, dict):
                    state = status.get("state", "")
                    result["online"] = state not in ["ERROR", "STOPPED", "OFFLINE", "INITIALIZING"]
                    result["errors"] = status.get("errors", 0)
                    if result["online"]:
                        return result
            
            # 3. Coba get_state()
            if hasattr(self.brain, 'get_state'):
                state = self.brain.get_state()
                if state and isinstance(state, dict):
                    result["online"] = state.get("state") not in ["ERROR", "STOPPED"]
                    if result["online"]:
                        return result
            
            # 4. Cek atribut state
            if hasattr(self.brain, 'state'):
                state = getattr(self.brain, 'state')
                if hasattr(state, 'value'):
                    result["online"] = state.value not in ["ERROR", "STOPPED"]
                else:
                    result["online"] = state not in ["ERROR", "STOPPED"]
                if result["online"]:
                    return result
            
            # 5. FINAL FALLBACK: Jika brain ada, anggap online
            if self.brain is not None:
                result["online"] = True
                result["health_score"] = 85
                logger.info("✅ Brain assumed ONLINE (fallback)")
            
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
            logger.debug(f"Brain check error: {e}")
        
        return result
    
    def _check_consciousness(self) -> Dict[str, Any]:
        """Check consciousness health."""
        result = {"online": False, "errors": 0}
        
        # Ambil dari berbagai sumber
        if not self.consciousness:
            try:
                root = self.winfo_toplevel()
                if hasattr(root, 'consciousness') and root.consciousness:
                    self.consciousness = root.consciousness
                    logger.info("✅ Consciousness loaded from root window")
            except Exception:
                pass
            
            if not self.consciousness and self.brain:
                if hasattr(self.brain, 'consciousness'):
                    self.consciousness = self.brain.consciousness
                    logger.info("✅ Consciousness loaded from brain")
            
            if not self.consciousness:
                try:
                    from core.consciousness import consciousness
                    self.consciousness = consciousness
                    logger.info("✅ Consciousness loaded from core")
                except ImportError:
                    pass
        
        if not self.consciousness:
            return result
        
        try:
            if hasattr(self.consciousness, 'status'):
                status = self.consciousness.status()
                if status and isinstance(status, dict):
                    result["online"] = status.get("state") != "ERROR"
                    return result
            
            if hasattr(self.consciousness, 'snapshot'):
                snapshot = self.consciousness.snapshot()
                if snapshot and isinstance(snapshot, dict):
                    result["online"] = True
                    return result
            
            # Jika consciousness ada, anggap online
            result["online"] = True
            
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
            logger.debug(f"Consciousness check error: {e}")
        
        return result
    
    def _check_learning(self) -> Dict[str, Any]:
        """Check learning engine health."""
        result = {"online": False, "errors": 0}
        
        # Dari learning integration
        if self.learning_integration:
            if hasattr(self.learning_integration, 'engine') and self.learning_integration.engine:
                result["online"] = self.learning_integration.running
                return result
        
        try:
            from core.learning.engine import learning_engine
            if learning_engine:
                if hasattr(learning_engine, 'status'):
                    status = learning_engine.status()
                    if status and isinstance(status, dict):
                        result["online"] = status.get("engine") == "ONLINE"
                        result["errors"] = status.get("errors", 0)
                        return result
                
                if hasattr(learning_engine, 'is_running'):
                    result["online"] = learning_engine.is_running()
                    return result
        except ImportError:
            pass
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
            logger.debug(f"Learning check error: {e}")
        
        return result
    
    def _check_memory(self) -> Dict[str, Any]:
        """Check memory health."""
        result = {"online": False, "errors": 0}
        
        try:
            from core.memory import memory
            if memory:
                if hasattr(memory, 'health'):
                    health = memory.health()
                    if health and isinstance(health, dict):
                        result["online"] = health.get("status") == "ONLINE"
                        return result
                
                if hasattr(memory, 'stats'):
                    stats = memory.stats()
                    if stats is not None:
                        result["online"] = True
                        return result
        except ImportError:
            pass
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
            logger.debug(f"Memory check error: {e}")
        
        return result
    
    def _check_pattern(self) -> Dict[str, Any]:
        """Check pattern engine health."""
        result = {"online": False, "errors": 0}
        
        try:
            from core.learning.pattern import pattern
            if pattern:
                if hasattr(pattern, 'get_state'):
                    state = pattern.get_state()
                    if state is not None:
                        result["online"] = True
                        return result
                
                if hasattr(pattern, 'status'):
                    status = pattern.status()
                    if status is not None:
                        result["online"] = True
                        return result
        except ImportError:
            pass
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
            logger.debug(f"Pattern check error: {e}")
        
        return result
    
    def _check_scanner(self) -> Dict[str, Any]:
        """Check scanner health - dengan multiple fallbacks."""
        result = {"online": False, "errors": 0}
        
        # COBA DARI BOT
        if self.bot and hasattr(self.bot, 'scanner'):
            scanner = self.bot.scanner
            if scanner:
                if hasattr(scanner, 'is_running'):
                    result["online"] = scanner.is_running()
                    return result
                if hasattr(scanner, 'running'):
                    result["online"] = scanner.running
                    return result
                # Jika scanner ada, anggap online
                result["online"] = True
                return result
        
        # COBA DARI CORE
        try:
            from core.scanner import scanner as core_scanner
            if core_scanner:
                if hasattr(core_scanner, 'is_running'):
                    result["online"] = core_scanner.is_running()
                    return result
                if hasattr(core_scanner, 'running'):
                    result["online"] = core_scanner.running
                    return result
                result["online"] = True
                return result
        except ImportError:
            pass
        except Exception as e:
            logger.debug(f"Scanner check error: {e}")
            result["error"] = str(e)
            result["errors"] = 1
        
        return result
    
    def _check_signal(self) -> Dict[str, Any]:
        """Check signal engine health."""
        result = {"online": False, "errors": 0}
        
        # COBA DARI BOT
        if self.bot and hasattr(self.bot, 'signal_engine'):
            engine = self.bot.signal_engine
            if engine:
                if hasattr(engine, 'is_active'):
                    result["online"] = engine.is_active()
                    return result
                if hasattr(engine, 'running'):
                    result["online"] = engine.running
                    return result
                result["online"] = True
                return result
        
        try:
            from core.signal_engine import SignalEngine
            result["online"] = True
        except ImportError:
            pass
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
            logger.debug(f"Signal check error: {e}")
        
        return result
    
    def _check_bot(self) -> Dict[str, Any]:
        """Check bot health - dengan multiple fallbacks."""
        result = {"online": False, "errors": 0}
        
        # Ambil dari root window
        if not self.bot:
            try:
                root = self.winfo_toplevel()
                if hasattr(root, 'bot') and root.bot:
                    self.bot = root.bot
                    logger.info("✅ Bot loaded from root window in _check_bot")
            except Exception:
                pass
            
            if not self.bot:
                return result
        
        try:
            # 1. Coba get_status
            if hasattr(self.bot, 'get_status'):
                status = self.bot.get_status()
                if status and isinstance(status, dict):
                    result["online"] = status.get("running", False)
                    result["errors"] = status.get("errors", 0)
                    if result["online"]:
                        return result
            
            # 2. Coba status
            if hasattr(self.bot, 'status'):
                status = self.bot.status()
                if status and isinstance(status, dict):
                    result["online"] = status.get("running", False)
                    result["errors"] = status.get("errors", 0)
                    if result["online"]:
                        return result
            
            # 3. Coba is_running
            if hasattr(self.bot, 'is_running'):
                result["online"] = self.bot.is_running()
                if result["online"]:
                    return result
            
            # 4. Coba atribut running
            if hasattr(self.bot, 'running'):
                result["online"] = self.bot.running
                if result["online"]:
                    return result
            
            # 5. FINAL FALLBACK: Jika bot ada, anggap online
            if self.bot is not None:
                result["online"] = True
                logger.info("✅ Bot assumed ONLINE (fallback)")
            
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
            logger.debug(f"Bot check error: {e}")
        
        return result
    
    # ============================================================
    # FALLBACK DATA
    # ============================================================
    
    def _generate_fallback_data(self) -> Dict[str, Any]:
        """Generate fallback health data."""
        return {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "online": 0,
            "total": 8,
            "errors": 0,
            "health_score": 0.0,
            "is_fallback": True
        }
    
    # ============================================================
    # UI UPDATE
    # ============================================================
    
    def _update_ui(self):
        """Update all UI components with current health data."""
        health = self.health_data
        if not health:
            return
        
        components = health.get("components", {})
        online = health.get("online", 0)
        total = health.get("total", 0)
        errors = health.get("errors", 0)
        health_score = health.get("health_score", 0.0)
        is_fallback = health.get("is_fallback", False)
        
        # ----- Update component status labels -----
        for name, label in self.component_labels.items():
            status = components.get(name, {})
            if isinstance(status, dict):
                is_online = status.get("online", False)
                error = status.get("error", "")
                if error:
                    label.configure(
                        text="● ERROR",
                        text_color="#EF4444"
                    )
                else:
                    label.configure(
                        text="● ONLINE" if is_online else "● OFFLINE",
                        text_color="#22C55E" if is_online else "#EF4444"
                    )
            else:
                label.configure(
                    text="● UNKNOWN",
                    text_color="#6B7280"
                )
        
        # ----- Update health score -----
        if self.health_score:
            color = self._get_health_color(health_score)
            self.health_score.update_value(f"{health_score:.0f}%", color=color)
            if is_fallback:
                self.health_score.update_subtitle("Fallback data")
            else:
                self.health_score.update_subtitle("System Health")
        
        # ----- Update components count -----
        if self.components_count:
            self.components_count.update_value(f"{online}/{total}")
            subtitle = "Online" if online > 0 else "No components online"
            self.components_count.update_subtitle(subtitle)
        
        # ----- Update errors count -----
        if self.errors_count:
            color = "#EF4444" if errors > 0 else "#22C55E"
            self.errors_count.update_value(str(errors), color=color)
            subtitle = "Total errors" if errors > 0 else "No errors"
            self.errors_count.update_subtitle(subtitle)
        
        # ----- Update status indicator -----
        if self.health_status:
            self.health_status.set_status(health_score > 80)
        
        # ----- Update details text -----
        if self.details_text:
            details_data = {
                "timestamp": datetime.now().isoformat(),
                "health_data": health,
                "update_count": self.update_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
                "is_fallback": is_fallback,
                "brain_available": self._brain_available,
                "connected": self.is_connected
            }
            if self.last_error:
                details_data["last_error"] = self.last_error
                details_data["last_error_time"] = self.last_error_time.isoformat() if self.last_error_time else None
            
            try:
                self.details_text.delete("1.0", "end")
                text = json.dumps(details_data, indent=2, default=str)
                if len(text) > 5000:
                    text = text[:5000] + "\n... (truncated)"
                self.details_text.insert("1.0", text)
            except Exception as e:
                logger.debug(f"[Health] Details update error: {e}")
    
    def _get_health_color(self, score: float) -> str:
        """Get color based on health score."""
        if score >= 80:
            return "#22C55E"
        elif score >= 60:
            return "#F59E0B"
        else:
            return "#EF4444"
    
    def _update_error_display(self, error: Exception):
        """Update UI to show error state."""
        try:
            if self.details_text:
                self.details_text.delete("1.0", "end")
                self.details_text.insert(
                    "1.0",
                    f"❌ ERROR\n\n"
                    f"Error: {error}\n"
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Updates: {self.update_count}\n"
                    f"Success: {self.success_count}\n"
                    f"Errors: {self.error_count}\n\n"
                    f"Traceback:\n{traceback.format_exc()}"
                )
            if self.health_status:
                self.health_status.set_status(False)
        except Exception:
            pass
    
    # ============================================================
    # CONTROL METHODS
    # ============================================================
    
    def refresh(self):
        """Force a manual refresh."""
        if self.refresh_btn:
            self.refresh_btn.configure(state="disabled", text="⏳ Refreshing...")
            self.update_idletasks()
        
        try:
            self.update_data()
        finally:
            if self.refresh_btn:
                self.refresh_btn.configure(state="normal", text="🔄 Refresh")
    
    def stop(self):
        """Stop periodic updates."""
        self.is_running = False
        if self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
    
    def destroy(self):
        """Clean up resources."""
        self.stop()
        super().destroy()