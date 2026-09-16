# ============================================================
# gui/__init__.py
# GUI PACKAGE - INTELLIGENCE PAGES
# ============================================================

from .page import IntelligencePage
from .widgets import (
    StatusIndicator, MetricCard, SignalBadge, ConfidenceBar,
    TimelineChart, PatternList, InsightCard, DecisionCard,
    MemoryStats, LearningProgress, MarketTicker, ProgressRing,
)

from .dashboard import DashboardPage
from .brain import Brain
from .market import Market
from .learning import Learning
from .memory import Memory
from .pattern import Pattern
from .prediction import Prediction
from .decision import Decision
from .reflection import Reflection
from .health import Health
from .knowledge import Knowledge
from .telegram import TelegramPage
from .trading import TradingPage
from .settings import SettingsPage

# ============================================================
# OPTIONAL / FALLBACK PAGES (dengan try/except)
# ============================================================

try:
    from .consciousness import Consciousness
except ImportError:
    Consciousness = None

try:
    from .scanner import Scanner
except ImportError:
    Scanner = None

try:
    from .signals import Signals
except ImportError:
    Signals = None

# --- Tambahan untuk sidebar ---
try:
    from .watchlist import Watchlist
except ImportError:
    Watchlist = None

try:
    from .analysis import Analysis
except ImportError:
    Analysis = None

try:
    from .signals import SignalsPage, SignalList, SignalDetails
except ImportError:
    SignalsPage = None
    SignalList = None
    SignalDetails = None

try:
    from .monitors import PerformanceMonitor, SystemMonitor, HealthMonitor
except ImportError:
    PerformanceMonitor = None
    SystemMonitor = None
    HealthMonitor = None

try:
    from .mirror import MirrorPage, CognitiveMirror
except ImportError:
    MirrorPage = None
    CognitiveMirror = None

try:
    from .logs import LogsPage, LogViewer
except ImportError:
    LogsPage = None
    LogViewer = None


# ============================================================
# EXPORT SEMUA VARIABLE YANG DIPERLUKAN app.py
# ============================================================

__all__ = [
    # Base
    "IntelligencePage",

    # Widgets
    "StatusIndicator", "MetricCard", "SignalBadge", "ConfidenceBar",
    "TimelineChart", "PatternList", "InsightCard", "DecisionCard",
    "MemoryStats", "LearningProgress", "MarketTicker", "ProgressRing",

    # Main pages
    "DashboardPage", "Brain", "Market", "Learning", "Memory",
    "Pattern", "Prediction", "Decision", "Reflection", "Health",
    "Knowledge", "TelegramPage", "TradingPage", "SettingsPage",

    # Optional / fallback
    "Consciousness", "Scanner", "Signals",
    "Watchlist", "Analysis",
    "SignalsPage", "SignalList", "SignalDetails",
    "PerformanceMonitor", "SystemMonitor", "HealthMonitor",
    "MirrorPage", "CognitiveMirror",
    "LogsPage", "LogViewer",
]