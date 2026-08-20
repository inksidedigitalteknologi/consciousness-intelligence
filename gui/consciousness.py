# ============================================================
# INKSIDE DIGITAL TRADING BOT
# GUI APPLICATION SHELL
#
# COGNITIVE MIRROR ENGINE v5.5
# ALGORITHMIC MARKET INTELLIGENCE TERMINAL
# ============================================================

import logging
import threading
import sys
import traceback
from pathlib import Path

from datetime import datetime

import customtkinter as ctk

logger = logging.getLogger(__name__)

# ============================================================
# APPLICATION CONFIG
# ============================================================

APP_NAME = "INKSIDEDIGITAL TRADING BOT"
APP_SUBTITLE = "ALGORITHMIC MARKET INTELLIGENCE TERMINAL"

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 950
SIDEBAR_WIDTH = 260
TOPBAR_HEIGHT = 70
STATUSBAR_HEIGHT = 32

# ============================================================
# COLOR SYSTEM
# ============================================================

COLORS = {
    "background": "#0B0F14",
    "sidebar": "#0F141B",
    "panel": "#131A22",
    "panel_light": "#18212B",
    "border": "#26313D",
    "text": "#E8EDF2",
    "text_secondary": "#8D9AAA",
    "text_muted": "#5F6B78",
    "accent": "#3B82F6",
    "accent_hover": "#2563EB",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#06B6D4"
}

# ============================================================
# FONT
# ============================================================

FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 22, "bold")
FONT_BUTTON = (FONT_FAMILY, 11, "bold")
FONT_SMALL = (FONT_FAMILY, 9)

# ============================================================
# INTELLIGENCE PAGES IMPORT - PER MODUL (TOLERAN)
# ============================================================

# --- IMPOR PER MODUL (AGAR SATU GAGAL TIDAK MEMATIKAN SEMUA) ---

# Dashboard
try:
    from gui.dashboard import DashboardPage
except ImportError:
    DashboardPage = None

# Brain
try:
    from gui.brain import Brain
except ImportError:
    Brain = None

# Market
try:
    from gui.market import Market
except ImportError:
    Market = None

# Learning
try:
    from gui.learning import Learning
except ImportError:
    Learning = None

# Memory
try:
    from gui.memory import Memory
except ImportError:
    Memory = None

# Pattern
try:
    from gui.pattern import Pattern
except ImportError:
    Pattern = None

# Prediction
try:
    from gui.prediction import Prediction
except ImportError:
    Prediction = None

# Decision
try:
    from gui.decision import Decision
except ImportError:
    Decision = None

# Reflection
try:
    from gui.reflection import Reflection
except ImportError:
    Reflection = None

# Health
try:
    from gui.health import Health
except ImportError:
    Health = None

# Knowledge
try:
    from gui.knowledge import Knowledge
except ImportError:
    Knowledge = None

# Telegram
try:
    from gui.telegram import TelegramPage
except ImportError:
    TelegramPage = None

# Trading
try:
    from gui.trading import TradingPage
except ImportError:
    TradingPage = None

# Settings
try:
    from gui.settings import SettingsPage
except ImportError:
    SettingsPage = None

# Consciousness
try:
    from gui.consciousness import Consciousness
except ImportError:
    Consciousness = None

# Scanner
try:
    from gui.scanner import Scanner
except ImportError:
    Scanner = None

# Signals
try:
    from gui.signals import Signals
except ImportError:
    Signals = None

# Watchlist
try:
    from gui.watchlist import Watchlist
except ImportError:
    Watchlist = None

# Analysis
try:
    from gui.analysis import Analysis
except ImportError:
    Analysis = None

# --- WIDGETS ---
try:
    from gui.widgets import (
        StatusIndicator,
        MetricCard,
        SignalBadge,
        ConfidenceBar,
        InsightCard,
        DecisionCard,
        MemoryStats,
        LearningProgress,
        MarketTicker,
        PatternList,
    )
    WIDGETS_AVAILABLE = True
except ImportError:
    WIDGETS_AVAILABLE = False
    StatusIndicator = MetricCard = SignalBadge = ConfidenceBar = None
    InsightCard = DecisionCard = MemoryStats = LearningProgress = None
    MarketTicker = PatternList = None

# Tentukan status ketersediaan intelijen
INTELLIGENCE_AVAILABLE = (
    DashboardPage is not None or
    Brain is not None or
    Market is not None or
    Learning is not None
)
if INTELLIGENCE_AVAILABLE:
    logger.info("✅ Intelligence pages loaded from gui/ folder.")
else:
    logger.warning("⚠️ No intelligence pages loaded from gui/ folder.")

# ============================================================
# TRY TO LOAD OTHER FOLDERS (SIGNALS, MONITORS, MIRROR, LOGS) - FALLBACK
# ============================================================

# Signals components
try:
    from gui.signals import SignalsPage, SignalList, SignalDetails
    SIGNALS_AVAILABLE = True
except ImportError:
    SIGNALS_AVAILABLE = False
    SignalsPage = None
    SignalList = None
    SignalDetails = None

# Monitors
try:
    from gui.monitors import PerformanceMonitor, SystemMonitor, HealthMonitor
    MONITORS_AVAILABLE = True
except ImportError:
    MONITORS_AVAILABLE = False
    PerformanceMonitor = None
    SystemMonitor = None
    HealthMonitor = None

# Mirror
try:
    from gui.mirror import MirrorPage, CognitiveMirror
    MIRROR_AVAILABLE = True
except ImportError:
    MIRROR_AVAILABLE = False
    MirrorPage = None
    CognitiveMirror = None

# Logs
try:
    from gui.logs import LogsPage, LogViewer
    LOGS_AVAILABLE = True
except ImportError:
    LOGS_AVAILABLE = False
    LogsPage = None
    LogViewer = None

# ============================================================
# LEARNING ENGINE INTEGRATION
# ============================================================

try:
    from core.learning.engine import (
        LearningEngine,
        learning_engine as global_learning_engine,
        KERNEL_VERSION,
        ENGINE_VERSION,
        STATE_IDLE,
        STATE_RUNNING,
        STATE_SUCCESS,
        STATE_PARTIAL,
        STATE_ERROR,
    )
    LEARNING_ENGINE_AVAILABLE = True
    logger.info("Learning Engine v%s loaded.", ENGINE_VERSION)
except ImportError as e:
    LEARNING_ENGINE_AVAILABLE = False
    logger.warning("Learning Engine not available: %s", e)
    LearningEngine = None
    global_learning_engine = None
    KERNEL_VERSION = "N/A"
    ENGINE_VERSION = "N/A"
    STATE_IDLE = "IDLE"
    STATE_RUNNING = "RUNNING"
    STATE_SUCCESS = "SUCCESS"
    STATE_PARTIAL = "PARTIAL"
    STATE_ERROR = "ERROR"

# ============================================================
# GET BRAIN HELPER
# ============================================================

def get_brain_from_sources(bot=None, learning=None):
    brain = None
    if bot:
        if hasattr(bot, 'brain'):
            brain = bot.brain
        elif hasattr(bot, '_brain'):
            brain = bot._brain
        elif hasattr(bot, 'get_brain'):
            try:
                brain = bot.get_brain()
            except Exception:
                pass
    if not brain and learning:
        if hasattr(learning, 'brain'):
            brain = learning.brain
        elif hasattr(learning, 'get_brain'):
            try:
                brain = learning.get_brain()
            except Exception:
                pass
    if not brain:
        try:
            from core.brain import brain as global_brain
            brain = global_brain
        except ImportError:
            pass
    return brain

# ============================================================
# MAIN APPLICATION
# ============================================================

class InksideBotApp(ctk.CTk):
    """
    Inkside Digital Trading Bot GUI Application.
    """

    def __init__(self, bot=None, learning_integration=None):
        print("[DEBUG] InksideBotApp.__init__ START")
        
        try:
            super().__init__()
            print("[DEBUG] super().__init__() DONE")
        except Exception as e:
            print(f"[ERROR] super().__init__() failed: {e}")
            traceback.print_exc()
            raise

        try:
            self.bot = bot
            self.learning = learning_integration
            self.engine_running = False
            self.engine_thread = None
            
            self.pages = {}
            self.navigation_buttons = {}
            self.current_page = None
            self.is_running = True
            
            self.brain = get_brain_from_sources(bot, learning_integration)
            self.brain_instances = {}
            self.active_brain_name = "default"
            
            if self.brain:
                self.brain_instances["default"] = self.brain
                logger.info("✅ Brain available in GUI application")
            else:
                logger.warning("⚠️ Brain not available in GUI application")

            # WINDOW
            self.title(APP_NAME)
            self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
            self.minsize(1200, 700)
            self.configure(fg_color=COLORS["background"])

            # GRID
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=0)
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1)

            # BUILD UI
            self.create_sidebar()
            self.create_main_area()
            self.create_status_bar()

            # LOAD PAGES - LAZY LOAD
            self.load_pages_lazy()

            # SHOW DEFAULT PAGE
            self.show_page("Dashboard")

            # UPDATE LOOP - DELAY
            self.after(1000, self._start_update_loops)

            # CLOSE EVENT
            self.protocol("WM_DELETE_WINDOW", self.on_close)

            # FORCE SHOW WINDOW
            self._force_show_window()
            self.after(200, self._force_show_window)
            self.after(500, self._force_show_window)

            print("[DEBUG] InksideBotApp.__init__ COMPLETE")

        except Exception as e:
            logger.exception(f"GUI initialization failed: {e}")
            print(f"[ERROR] GUI initialization failed: {e}")
            traceback.print_exc()
            raise

    def _force_show_window(self):
        try:
            self.deiconify()
            self.lift()
            self.focus_force()
            self.attributes('-topmost', True)
            self.update_idletasks()
            self.after(300, lambda: self.attributes('-topmost', False))
        except Exception as e:
            print(f"[DEBUG] Force show error: {e}")

    def _start_update_loops(self):
        try:
            self.update_clock()
            self.update_system_status()
            self.update_learning_status()
        except Exception as e:
            print(f"[DEBUG] Update loops error: {e}")

    # ============================================================
    # SIDEBAR
    # ============================================================

    def create_sidebar(self):
        try:
            self.sidebar = ctk.CTkFrame(
                self,
                width=SIDEBAR_WIDTH,
                corner_radius=0,
                fg_color=COLORS["sidebar"]
            )
            self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
            self.sidebar.grid_propagate(False)
            self.sidebar.grid_rowconfigure(1, weight=1)

            # LOGO
            logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            logo_frame.grid(row=0, column=0, padx=20, pady=22, sticky="ew")

            ctk.CTkLabel(logo_frame, text="INKSIDE", font=(FONT_FAMILY, 22, "bold"), text_color=COLORS["text"]).pack(anchor="w")
            ctk.CTkLabel(logo_frame, text="DIGITAL", font=(FONT_FAMILY, 12, "bold"), text_color=COLORS["accent"]).pack(anchor="w")
            ctk.CTkLabel(logo_frame, text="COGNITIVE MIRROR ENGINE", font=(FONT_FAMILY, 9), text_color=COLORS["text_muted"]).pack(anchor="w", pady=(2, 0))
            ctk.CTkLabel(logo_frame, text="ALGORITHMIC MARKET INTELLIGENCE", font=(FONT_FAMILY, 8), text_color=COLORS["text_muted"]).pack(anchor="w")

            # LEARNING STATUS
            self.learning_status_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
            self.learning_status_frame.pack(anchor="w", pady=(5, 0))
            
            self.learning_status_indicator = ctk.CTkLabel(
                self.learning_status_frame,
                text="◉",
                font=(FONT_FAMILY, 10),
                text_color=COLORS["text_muted"]
            )
            self.learning_status_indicator.pack(side="left", padx=(0, 5))
            
            self.learning_status_label = ctk.CTkLabel(
                self.learning_status_frame,
                text="LEARNING: IDLE",
                font=(FONT_FAMILY, 8, "bold"),
                text_color=COLORS["text_muted"]
            )
            self.learning_status_label.pack(side="left")

            # NAVIGATION
            self.navigation_frame = ctk.CTkScrollableFrame(
                self.sidebar,
                fg_color="transparent"
            )
            self.navigation_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

            # OVER
            self.create_navigation_group("📊 OVER", [("Dashboard", "⌂")])

            # INTELLIGENCE
            intelligence_pages = []
            if Brain is not None: intelligence_pages.append(("Brain", "🧠"))
            if Consciousness is not None: intelligence_pages.append(("Consciousness", "💭"))
            if Learning is not None: intelligence_pages.append(("Learning", "📚"))
            if Memory is not None: intelligence_pages.append(("Memory", "💾"))
            if Pattern is not None: intelligence_pages.append(("Pattern", "🔍"))
            if intelligence_pages:
                self.create_navigation_group("🧠 INTELLIGENCE", intelligence_pages)

            # MARKET
            market_pages = []
            if Market is not None: market_pages.append(("Market", "📈"))
            if Scanner is not None: market_pages.append(("Scanner", "◈"))
            if Signals is not None or SignalsPage is not None: market_pages.append(("Signals", "◆"))
            if Watchlist is not None: market_pages.append(("Watchlist", "☆"))
            if market_pages:
                self.create_navigation_group("📊 MARKET", market_pages)

            # ANALYSIS
            analysis_pages = []
            if Prediction is not None: analysis_pages.append(("Prediction", "🔮"))
            if Decision is not None: analysis_pages.append(("Decision", "🎯"))
            if Reflection is not None: analysis_pages.append(("Reflection", "💭"))
            if Analysis is not None: analysis_pages.append(("Analysis", "◎"))
            if analysis_pages:
                self.create_navigation_group("🔬 ANALYSIS", analysis_pages)

            # MONITORS
            monitor_pages = []
            if Health is not None: monitor_pages.append(("Health", "❤️"))
            if PerformanceMonitor is not None: monitor_pages.append(("Performance", "📊"))
            if SystemMonitor is not None: monitor_pages.append(("System Monitor", "🖥️"))
            if monitor_pages:
                self.create_navigation_group("📊 MONITORS", monitor_pages)

            # KNOWLEDGE
            if Knowledge is not None:
                self.create_navigation_group("📚 KNOWLEDGE", [("Knowledge", "📚")])

            # CONTROL
            control_pages = []
            if TelegramPage is not None: control_pages.append(("Telegram", "✈"))
            if TradingPage is not None: control_pages.append(("Trading", "↗"))
            if SettingsPage is not None: control_pages.append(("Settings", "⚙"))
            if control_pages:
                self.create_navigation_group("⚙️ CONTROL", control_pages)

            # MIRROR
            mirror_pages = []
            if MirrorPage is not None: mirror_pages.append(("Mirror", "🪞"))
            if CognitiveMirror is not None: mirror_pages.append(("Cognitive Mirror", "🧠"))
            if mirror_pages:
                self.create_navigation_group("🪞 MIRROR", mirror_pages)

            # SYSTEM
            if LogsPage is not None or LogViewer is not None:
                self.create_navigation_group("⚙️ SYSTEM", [("Logs", "≡")])

            # FOOTER
            footer = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=50)
            footer.grid(row=2, column=0, padx=15, pady=15, sticky="ew")

            self.sidebar_status_indicator = ctk.CTkLabel(
                footer,
                text="●",
                font=(FONT_FAMILY, 14),
                text_color=COLORS["success"]
            )
            self.sidebar_status_indicator.pack(side="left", padx=(5, 8))

            self.sidebar_status_label = ctk.CTkLabel(
                footer,
                text="SYSTEM ONLINE",
                font=(FONT_FAMILY, 9, "bold"),
                text_color=COLORS["text_secondary"]
            )
            self.sidebar_status_label.pack(side="left")
            
        except Exception as e:
            logger.error(f"create_sidebar error: {e}")
            traceback.print_exc()
            raise

    def create_navigation_group(self, title, items):
        try:
            title_label = ctk.CTkLabel(
                self.navigation_frame,
                text=title,
                font=(FONT_FAMILY, 9, "bold"),
                text_color=COLORS["text_muted"]
            )
            title_label.pack(fill="x", padx=12, pady=(18, 6))

            for name, icon in items:
                button = ctk.CTkButton(
                    self.navigation_frame,
                    text=f"{icon}   {name}",
                    height=42,
                    corner_radius=8,
                    anchor="w",
                    fg_color="transparent",
                    hover_color=COLORS["panel_light"],
                    text_color=COLORS["text_secondary"],
                    font=FONT_BUTTON,
                    command=lambda n=name: self.show_page(n)
                )
                button.pack(fill="x", padx=4, pady=3)
                self.navigation_buttons[name] = button
        except Exception as e:
            logger.error(f"create_navigation_group error: {e}")
            raise

    # ============================================================
    # MAIN AREA
    # ============================================================

    def create_main_area(self):
        try:
            self.main_container = ctk.CTkFrame(
                self,
                fg_color=COLORS["background"],
                corner_radius=0
            )
            self.main_container.grid(row=0, column=1, sticky="nsew")
            self.main_container.grid_rowconfigure(1, weight=1)
            self.main_container.grid_columnconfigure(0, weight=1)

            # TOP BAR
            self.topbar = ctk.CTkFrame(
                self.main_container,
                height=TOPBAR_HEIGHT,
                corner_radius=0,
                fg_color=COLORS["panel"],
                border_width=1,
                border_color=COLORS["border"]
            )
            self.topbar.grid(row=0, column=0, sticky="ew")
            self.topbar.grid_propagate(False)
            self.topbar.grid_columnconfigure(0, weight=1)

            # PAGE TITLE
            self.page_title = ctk.CTkLabel(
                self.topbar,
                text="Dashboard",
                font=FONT_TITLE,
                text_color=COLORS["text"]
            )
            self.page_title.grid(row=0, column=0, padx=25, sticky="w")

            # TOP RIGHT STATUS
            self.top_status_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
            self.top_status_frame.grid(row=0, column=1, padx=10, sticky="e")

            self.exchange_status = ctk.CTkLabel(
                self.top_status_frame,
                text="● KRAKEN",
                font=(FONT_FAMILY, 10, "bold"),
                text_color=COLORS["success"]
            )
            self.exchange_status.pack(side="left", padx=10)

            self.telegram_status = ctk.CTkLabel(
                self.top_status_frame,
                text="● TELEGRAM",
                font=(FONT_FAMILY, 10, "bold"),
                text_color=COLORS["text_muted"]
            )
            self.telegram_status.pack(side="left", padx=10)

            # ENGINE BUTTONS
            self.engine_frame = ctk.CTkFrame(self.top_status_frame, fg_color="transparent")
            self.engine_frame.pack(side="left", padx=10)

            self.start_engine_button = ctk.CTkButton(
                self.engine_frame,
                text="▶ START ENGINE",
                width=130,
                height=34,
                corner_radius=8,
                font=FONT_BUTTON,
                fg_color=COLORS["success"],
                hover_color="#16A34A",
                command=self.start_engine
            )
            self.start_engine_button.pack(side="left", padx=4)

            self.stop_engine_button = ctk.CTkButton(
                self.engine_frame,
                text="■ STOP ENGINE",
                width=130,
                height=34,
                corner_radius=8,
                font=FONT_BUTTON,
                fg_color=COLORS["danger"],
                hover_color="#DC2626",
                command=self.stop_engine,
                state="disabled"
            )
            self.stop_engine_button.pack(side="left", padx=4)

            self.intelligence_status = ctk.CTkLabel(
                self.top_status_frame,
                text="🧠",
                font=(FONT_FAMILY, 16),
                text_color=COLORS["text_muted"]
            )
            self.intelligence_status.pack(side="left", padx=8)

            # CLOCK
            self.clock_label = ctk.CTkLabel(
                self.top_status_frame,
                text="00:00:00",
                font=(FONT_FAMILY, 11, "bold"),
                text_color=COLORS["text"]
            )
            self.clock_label.pack(side="left", padx=15)

            # CONTENT AREA
            self.content_container = ctk.CTkFrame(
                self.main_container,
                fg_color=COLORS["background"]
            )
            self.content_container.grid(row=1, column=0, sticky="nsew")
            self.content_container.grid_rowconfigure(0, weight=1)
            self.content_container.grid_columnconfigure(0, weight=1)
            
        except Exception as e:
            logger.error(f"create_main_area error: {e}")
            traceback.print_exc()
            raise

    # ============================================================
    # STATUS BAR
    # ============================================================

    def create_status_bar(self):
        try:
            self.statusbar = ctk.CTkFrame(
                self,
                height=STATUSBAR_HEIGHT,
                corner_radius=0,
                fg_color=COLORS["panel"],
                border_width=1,
                border_color=COLORS["border"]
            )
            self.statusbar.grid(row=1, column=1, sticky="ew")
            self.statusbar.grid_propagate(False)

            self.system_status = ctk.CTkLabel(
                self.statusbar,
                text="● SYSTEM READY",
                font=(FONT_FAMILY, 9, "bold"),
                text_color=COLORS["success"]
            )
            self.system_status.pack(side="left", padx=15)

            self.scanner_status = ctk.CTkLabel(
                self.statusbar,
                text="Scanner: READY",
                font=(FONT_FAMILY, 9),
                text_color=COLORS["text_secondary"]
            )
            self.scanner_status.pack(side="left", padx=30)

            self.intelligence_status_bar = ctk.CTkLabel(
                self.statusbar,
                text="🧠 Intelligence: ONLINE" if INTELLIGENCE_AVAILABLE else "🧠 Intelligence: N/A",
                font=(FONT_FAMILY, 9),
                text_color=COLORS["text_muted"]
            )
            self.intelligence_status_bar.pack(side="left", padx=30)

            self.last_update_label = ctk.CTkLabel(
                self.statusbar,
                text="Last Update: --",
                font=(FONT_FAMILY, 9),
                text_color=COLORS["text_muted"]
            )
            self.last_update_label.pack(side="right", padx=15)
            
        except Exception as e:
            logger.error(f"create_status_bar error: {e}")
            traceback.print_exc()
            raise

    # ============================================================
    # LOAD PAGES - LAZY LOADING
    # ============================================================

    def load_pages_lazy(self):
        """Load pages as placeholders only - actual loading on demand."""
        
        all_pages = []
        
        # ============================================================
        # FIX: Dashboard - TIDAK support learning_integration
        # ============================================================
        if DashboardPage is not None:
            all_pages.append(("Dashboard", DashboardPage, False))
        
        # Intelligence - SUPPORT learning_integration
        intelligence_pages = [
            ("Brain", Brain),
            ("Consciousness", Consciousness),
            ("Learning", Learning),
            ("Memory", Memory),
            ("Pattern", Pattern),
            ("Prediction", Prediction),
            ("Decision", Decision),
            ("Reflection", Reflection),
            ("Health", Health),
            ("Market", Market),
        ]
        for name, page_class in intelligence_pages:
            if page_class is not None:
                all_pages.append((name, page_class, True))
        
        # Knowledge - SUPPORT learning_integration
        if Knowledge is not None:
            all_pages.append(("Knowledge", Knowledge, True))
        
        # Control Pages - TIDAK support learning_integration
        if TelegramPage is not None:
            all_pages.append(("Telegram", TelegramPage, False))
        if TradingPage is not None:
            all_pages.append(("Trading", TradingPage, False))
        if SettingsPage is not None:
            all_pages.append(("Settings", SettingsPage, False))
        
        # Signals - TIDAK support learning_integration
        if SignalsPage is not None:
            all_pages.append(("Signals", SignalsPage, False))
        if SignalDetails is not None:
            all_pages.append(("Signal Details", SignalDetails, False))
        
        # Monitors
        if PerformanceMonitor is not None:
            all_pages.append(("Performance", PerformanceMonitor, False))
        if SystemMonitor is not None:
            all_pages.append(("System Monitor", SystemMonitor, False))
        if HealthMonitor is not None:
            all_pages.append(("Health Monitor", HealthMonitor, False))
        
        # Mirror
        if MirrorPage is not None:
            all_pages.append(("Mirror", MirrorPage, False))
        if CognitiveMirror is not None:
            all_pages.append(("Cognitive Mirror", CognitiveMirror, False))
        
        # Logs
        if LogsPage is not None:
            all_pages.append(("Logs", LogsPage, False))
        if LogViewer is not None:
            all_pages.append(("Log Viewer", LogViewer, False))
        
        # ============================================================
        # CREATE PLACEHOLDER FOR EACH PAGE
        # ============================================================
        
        self._page_meta = {}
        
        for name, page_class, supports_learning in all_pages:
            if page_class is None:
                continue
            
            placeholder = self._create_placeholder(name)
            self.pages[name] = placeholder
            
            self._page_meta[name] = {
                'class': page_class,
                'supports_learning': supports_learning,
                'loaded': False
            }
            
            logger.debug(f"Page placeholder created: {name}")

    def _create_placeholder(self, page_name: str) -> ctk.CTkFrame:
        placeholder = ctk.CTkFrame(self.content_container, fg_color="transparent")
        ctk.CTkLabel(
            placeholder,
            text=f"📄 {page_name}\n\nLoading...",
            font=("Segoe UI", 18),
            text_color=COLORS["text_muted"]
        ).place(relx=0.5, rely=0.5, anchor="center")
        return placeholder

    # ============================================================
    # SHOW PAGE - DENGAN LAZY LOADING
    # ============================================================

    def show_page(self, page_name):
        try:
            # Clear content container
            for widget in self.content_container.winfo_children():
                try:
                    widget.pack_forget()
                    widget.grid_forget()
                except:
                    pass

            # Update navigation buttons
            for name, button in self.navigation_buttons.items():
                if name == page_name:
                    button.configure(fg_color=COLORS["accent"], text_color="white")
                else:
                    button.configure(fg_color="transparent", text_color=COLORS["text_secondary"])

            self.page_title.configure(text=page_name)

            page = self.pages.get(page_name)
            
            meta = self._page_meta.get(page_name)
            if meta and not meta.get('loaded', False):
                try:
                    page_class = meta['class']
                    supports_learning = meta.get('supports_learning', False)
                    
                    page_instance = None
                    
                    if supports_learning:
                        try:
                            page_instance = page_class(
                                self.content_container,
                                bot=self.bot,
                                learning_integration=self.learning
                            )
                        except TypeError:
                            pass
                    
                    if page_instance is None:
                        try:
                            page_instance = page_class(self.content_container, self.bot)
                        except TypeError:
                            pass
                    
                    if page_instance is None:
                        try:
                            page_instance = page_class(self.content_container)
                        except TypeError:
                            pass
                    
                    if page_instance is None:
                        try:
                            page_instance = page_class()
                        except Exception:
                            pass
                    
                    if page_instance is not None:
                        self._setup_page_references(page_instance, page_name)
                        self.pages[page_name] = page_instance
                        page = page_instance
                        meta['loaded'] = True
                        logger.info(f"✅ Lazy loaded: {page_name}")
                    else:
                        logger.warning(f"Failed to lazy load: {page_name}")
                        
                except Exception as e:
                    logger.warning(f"Lazy load error for {page_name}: {e}")
                    traceback.print_exc()
            
            if page:
                try:
                    page.pack(fill="both", expand=True)
                    self.current_page = page_name
                    if hasattr(page, "on_show"):
                        try:
                            page.on_show()
                        except Exception:
                            pass
                except Exception as e:
                    logger.warning(f"Error showing page {page_name}: {e}")
            else:
                placeholder = self._create_placeholder(page_name)
                placeholder.pack(fill="both", expand=True)
                
        except Exception as e:
            logger.error(f"show_page error: {e}")
            traceback.print_exc()

    def _setup_page_references(self, page_instance, page_name):
        try:
            if hasattr(page_instance, 'set_bot') and callable(page_instance.set_bot):
                try:
                    page_instance.set_bot(self.bot)
                except Exception as e:
                    logger.debug(f"Set bot error for {page_name}: {e}")
            
            if hasattr(page_instance, 'set_learning') and callable(page_instance.set_learning):
                try:
                    page_instance.set_learning(self.learning)
                except Exception as e:
                    logger.debug(f"Set learning error for {page_name}: {e}")
            
            if hasattr(page_instance, 'set_brain') and callable(page_instance.set_brain):
                try:
                    if self.brain:
                        page_instance.set_brain(self.brain)
                except Exception as e:
                    logger.debug(f"Set brain error for {page_name}: {e}")
            
            if hasattr(page_instance, 'set_brain_instance') and callable(page_instance.set_brain_instance):
                try:
                    if self.brain:
                        page_instance.set_brain_instance(self.brain)
                except Exception as e:
                    logger.debug(f"Set brain_instance error for {page_name}: {e}")
            
            if self.brain:
                if hasattr(page_instance, 'brain'):
                    page_instance.brain = self.brain
                if hasattr(page_instance, 'brain_instance'):
                    page_instance.brain_instance = self.brain
                    
        except Exception as e:
            logger.warning(f"Setup references error for {page_name}: {e}")

    # ============================================================
    # CLOCK
    # ============================================================

    def update_clock(self):
        if not self.is_running:
            return
        try:
            self.clock_label.configure(text=datetime.now().strftime("%H:%M:%S"))
        except Exception:
            pass
        self.after(1000, self.update_clock)

    # ============================================================
    # HEALTH MONITOR
    # ============================================================

    def update_system_status(self):
        if not self.is_running:
            return
        try:
            from core.health import get_status
            status = get_status()
            core = status.get("core", "OFFLINE")
            scanner = status.get("scanner", "OFFLINE")
            if core == "ONLINE":
                self.system_status.configure(text="● SYSTEM ONLINE", text_color=COLORS["success"])
            else:
                self.system_status.configure(text="● SYSTEM OFFLINE", text_color=COLORS["danger"])
            self.scanner_status.configure(text=f"Scanner: {scanner}")
            self.last_update_label.configure(text="Last Update: " + datetime.now().strftime("%H:%M:%S"))
        except Exception as e:
            logger.debug(f"Health update error {e}")
        self.after(5000, self.update_system_status)

    # ============================================================
    # LEARNING STATUS UPDATE
    # ============================================================

    def update_learning_status(self):
        if not self.is_running:
            return
        try:
            if self.learning is not None:
                status = self.learning.get_status()
                if status.get("available") and status.get("initialized"):
                    running = status.get("running", False)
                    cycles = status.get("cycles", 0)
                    if running:
                        self.learning_status_indicator.configure(text_color=COLORS["success"])
                        self.learning_status_label.configure(text=f"LEARNING: ACTIVE ({cycles})", text_color=COLORS["success"])
                    else:
                        self.learning_status_indicator.configure(text_color=COLORS["text_muted"])
                        self.learning_status_label.configure(text=f"LEARNING: IDLE ({cycles})", text_color=COLORS["text_muted"])
                else:
                    self.learning_status_indicator.configure(text_color=COLORS["warning"])
                    self.learning_status_label.configure(text="LEARNING: UNAVAILABLE", text_color=COLORS["warning"])
            else:
                self.learning_status_label.configure(text="LEARNING: NOT INSTALLED", text_color=COLORS["text_muted"])
        except Exception as e:
            logger.debug(f"Learning status update error: {e}")
        self.after(2000, self.update_learning_status)

    # ============================================================
    # ENGINE CONTROL
    # ============================================================

    def start_engine(self):
        if self.engine_running:
            return
        self.engine_running = True
        logger.info("Trading Engine START requested from GUI.")
        self.start_engine_button.configure(state="disabled")
        self.stop_engine_button.configure(state="normal")
        self.system_status.configure(text="● ENGINE RUNNING", text_color=COLORS["success"])
        self.sidebar_status_label.configure(text="ENGINE ONLINE")
        try:
            if self.bot and hasattr(self.bot, "start"):
                self.engine_thread = threading.Thread(target=self.bot.start, daemon=True)
                self.engine_thread.start()
            if self.learning is not None:
                self.learning.start()
                logger.info("Learning Engine started")
        except Exception as e:
            logger.exception("Engine start failed: %s", e)

    def stop_engine(self):
        if not self.engine_running:
            return
        self.engine_running = False
        logger.info("Trading Engine STOP requested from GUI.")
        self.start_engine_button.configure(state="normal")
        self.stop_engine_button.configure(state="disabled")
        self.system_status.configure(text="● SYSTEM READY", text_color=COLORS["warning"])
        self.sidebar_status_label.configure(text="SYSTEM READY")
        try:
            if self.bot and hasattr(self.bot, "stop"):
                self.bot.stop()
            if self.learning is not None:
                self.learning.stop()
                logger.info("Learning Engine stopped")
        except Exception as e:
            logger.warning("Engine stop failed: %s", e)

    # ============================================================
    # CLOSE APPLICATION
    # ============================================================

    def on_close(self):
        logger.info("Closing INKSIDEDIGITAL Trading Bot.")
        self.is_running = False
        try:
            if self.bot and hasattr(self.bot, "stop"):
                self.bot.stop()
            if self.learning is not None:
                self.learning.shutdown()
                logger.info("Learning Engine shut down")
        except Exception as e:
            logger.warning("Bot stop error: %s", e)
        self.destroy()


# ============================================================
# END
# ============================================================