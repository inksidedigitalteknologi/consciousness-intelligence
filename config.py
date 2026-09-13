# ============================================================
# INKSIDEDIGITAL CONSCIOUSNESS INTELLIGENCE
# COGNITIVE MIRROR ENGINE v2.0.0
# ============================================================
# SEMUA KONFIGURASI SISTEM TERPUSAT DI SATU FILE
# ============================================================

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# ============================================================
# 1. BASE PATH & DIREKTORI
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# Direktori utama
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
DATABASE_DIR = BASE_DIR / "database"
CACHE_DIR = BASE_DIR / "cache"
BACKUP_DIR = BASE_DIR / "backups"
REPORTS_DIR = BASE_DIR / "reports"

# Buat semua direktori
for dir_path in [DATA_DIR, LOG_DIR, DATABASE_DIR, CACHE_DIR, BACKUP_DIR, REPORTS_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)

# ============================================================
# 2. APLIKASI & IDENTITAS
# ============================================================

APP_NAME = 'INKSIDEDIGITAL CONSCIOUSNESS INTELLIGENCE'
APP_VERSION = '2.0.0'
APP_AUTHOR = 'Inkside Digital'

# Versi komponen
COGNITIVE_ENGINE_VERSION = "4.4"
SIGNAL_ENGINE_VERSION = "2.2"

# ============================================================
# 3. FILE PATHS (Referensi file penting)
# ============================================================

SETTINGS_FILE = DATA_DIR / "settings.json"
WATCHLIST_FILE = DATA_DIR / "watchlist.json"
HISTORY_FILE = DATA_DIR / "signal_history.json"
TRADES_FILE = DATA_DIR / "trades.json"
PERFORMANCE_FILE = DATA_DIR / "performance.json"
LEARNING_STATE_FILE = DATABASE_DIR / "learning_state.json"
KNOWLEDGE_GRAPH_FILE = DATABASE_DIR / "knowledge_graph.json"
PATTERN_DATABASE_FILE = DATABASE_DIR / "patterns.db"

# Log files
LOG_FILE = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
ERROR_LOG_FILE = LOG_DIR / f"error_{datetime.now().strftime('%Y%m%d')}.log"
SIGNAL_LOG_FILE = LOG_DIR / f"signals_{datetime.now().strftime('%Y%m%d')}.log"

# ============================================================
# 4. EXCHANGE - KRAKEN
# ============================================================

EXCHANGE_NAME = 'Kraken'
EXCHANGE_TYPE = 'kraken'
KRAKEN_API_BASE = "https://api.kraken.com"

# Rate Limiting
REQUEST_DELAY = 2
REQUEST_TIMEOUT = 15
REQUEST_RETRY_COUNT = 3
REQUEST_RETRY_DELAY = 5
REQUEST_BACKOFF_MULTIPLIER = 2

# Cache
CACHE_TTL_SECONDS = 120
OHLCV_LIMIT = 100
MAX_MARKETS = 15

# ============================================================
# 5. MARKET & PAIRS
# ============================================================

DEFAULT_PAIRS = ['BTC/USD', 'ETH/USD', 'SOL/USD', 'XRP/USD', 'BNB/USD']

DEFAULT_TIMEFRAMES = ['1h', '4h', '1d']

MAIN_TIMEFRAME = '1h'
SCALP_TIMEFRAME = "15m"
SWING_TIMEFRAME = "4h"
LONG_TIMEFRAME = "1d"

# ============================================================
# 6. SCANNER SETTINGS
# ============================================================

SCAN_INTERVAL_SECONDS = 600
MAX_WORKERS = 2
MAX_RETRIES = 2
USE_CLOSED_CANDLE = True
CACHE_OHLCV = True

SCANNER_BATCH_SIZE = 2
SCANNER_BATCH_DELAY = 5
SCANNER_TIMEOUT = 60

# ============================================================
# 7. SIGNAL SETTINGS
# ============================================================

MIN_MTF_ALIGNMENT = 2
MIN_SIGNAL_STRENGTH = 60
MIN_SIGNAL_CONFIDENCE = 60
SEND_STARTUP_SIGNALS = False
SIGNAL_COOLDOWN_SECONDS = 7200
MAX_SIGNALS_PER_SCAN = 2
MIN_SIGNAL_QUALITY = 50

# Signal Quality Levels
QUALITY_WEAK = 40
QUALITY_NEUTRAL = 55
QUALITY_STRONG = 70
QUALITY_VERY_STRONG = 85

# Signal Types
SIGNAL_HOLD = "HOLD"
SIGNAL_BUY = "BUY"
SIGNAL_SELL = "SELL"
SIGNAL_MONITOR = "MONITOR"
SIGNAL_EXIT = "EXIT"

# ============================================================
# 8. TIMEFRAME WEIGHTS
# ============================================================

TIMEFRAME_WEIGHTS = {
    "1h": 2.5,
    "4h": 3.5,
    "1d": 5.0,
}

# ============================================================
# 9. INDICATOR SETTINGS
# ============================================================

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

MA_FAST = 9
MA_MEDIUM = 21
MA_SLOW = 50
MA_VERY_SLOW = 200

BB_PERIOD = 20
BB_STD_DEV = 2

ATR_PERIOD = 14
ATR_SL_MULTIPLIER = 1.5
TP1_ATR_MULTIPLIER = 1.0
TP2_ATR_MULTIPLIER = 2.0
TP3_ATR_MULTIPLIER = 3.0

VOLUME_MA_PERIOD = 20
VOLUME_SPIKE_MULTIPLIER = 1.5

# ============================================================
# 10. RISK MANAGEMENT
# ============================================================

DEFAULT_RISK_PERCENT = 1
DEFAULT_RISK_REWARD = 3
MAX_POSITION_SIZE = 10
MIN_POSITION_SIZE = 5
MAX_DAILY_TRADES = 10
MAX_OPEN_POSITIONS = 5
MAX_DRAWDOWN_PERCENT = 20
STOP_LOSS_PERCENT = 5
TAKE_PROFIT_PERCENT = 15

# ============================================================
# 11. TRADING MODE - PAPER TRADING (AMAN)
# ============================================================

TRADING_ENABLED = False
PAPER_TRADING = True
AUTO_TRADE = False

ORDER_TYPE = "market"
ORDER_TIF = "GTC"
ORDER_LEVERAGE = 1

# ============================================================
# 12. TELEGRAM CONFIGURATION
# ============================================================

TELEGRAM_ENABLED = False
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_TIMEOUT = 15
TELEGRAM_RETRY_COUNT = 3
TELEGRAM_RETRY_DELAY = 2

# ============================================================
# 13. LOGGING
# ============================================================

LOG_LEVEL = 'INFO'
LOG_FILE_LEVEL = "DEBUG"
CONSOLE_LEVEL = "INFO"
ENABLE_FILE_LOG = True
ENABLE_CONSOLE_LOG = True
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_SIZE_MB = 100
LOG_BACKUP_COUNT = 5

# ============================================================
# 14. LEARNING ENGINE
# ============================================================

LEARNING_ENABLED = True
LEARNING_INTERVAL_SECONDS = 600
LEARNING_AUTO_START = True
LEARNING_MAX_HISTORY = 500

# ============================================================
# 15. PREDICTION ENGINE
# ============================================================

PREDICTION_ENABLED = True
PREDICTION_HORIZON = [5, 15, 30, 60]
PREDICTION_MIN_CONFIDENCE = 0.6
PREDICTION_MAX_HISTORY = 1000

# ============================================================
# 16. HEALTH MONITOR
# ============================================================

HEALTH_CHECK_INTERVAL = 60
HEALTH_METRICS_PERSIST = True
HEALTH_ALERT_ON_DEGRADE = True
HEALTH_MIN_SCORE = 80
HEALTH_CRITICAL_SCORE = 50

# ============================================================
# 17. PERFORMANCE METRICS
# ============================================================

TRACK_PERFORMANCE = True
PERFORMANCE_UPDATE_INTERVAL = 60
PERFORMANCE_PERSIST_INTERVAL = 300
MAX_PERFORMANCE_HISTORY = 1000

METRICS_TRACKED = [
    "total_trades",
    "win_rate",
    "profit_factor",
    "sharpe_ratio",
    "max_drawdown",
    "average_win",
    "average_loss",
    "total_profit_loss",
]

# ============================================================
# 18. SYSTEM - PRODUCTION READY
# ============================================================

DEBUG_MODE = False
ENABLE_PROFILING = False
ENABLE_TRACING = False
ENABLE_METRICS = True

MAX_THREADS = 10
THREAD_POOL_SIZE = 5
QUEUE_SIZE = 50

GLOBAL_TIMEOUT = 120
API_TIMEOUT = 10
DB_TIMEOUT = 10

# ============================================================
# 19. AI CONFIGURATION (DeepSeek)
# ============================================================

DEEPSEEK_ENABLED = os.getenv("DEEPSEEK_ENABLED", "false").lower() == "true"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = "deepseek-chat"
DEEPSEEK_TEMPERATURE = 0.3
DEEPSEEK_MAX_TOKENS = 500

# ============================================================
# 20. KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_MAX_ITEMS = 100000
KNOWLEDGE_AUTO_SAVE = True
KNOWLEDGE_AI_ENHANCEMENT = True
KNOWLEDGE_MIN_CONFIDENCE = 0.5

# Auto-Crawl Sources
AUTO_CRAWL_SOURCES = [
    "https://id.wikipedia.org/wiki/Bitcoin",
    "https://id.wikipedia.org/wiki/Ethereum",
    "https://id.wikipedia.org/wiki/Kecerdasan_buatan",
    "https://id.wikipedia.org/wiki/Blockchain",
    "https://id.wikipedia.org/wiki/Investasi",
]

AUTO_CRAWL_INTERVAL_HOURS = 6

# ============================================================
# 21. ERROR DETECTION
# ============================================================

ERROR_DETECTION_ENABLED = True
ERROR_LOG_DIR = LOG_DIR / "errors"
ERROR_MAX_HISTORY = 1000
ERROR_NOTIFICATION_ENABLED = True

# Recovery
ERROR_AUTO_RECOVERY = True
ERROR_MAX_RECOVERY_ATTEMPTS = 3

# ============================================================
# 22. AI PROMPTS
# ============================================================

AI_PROMPT_ACTIVE = "knowledge_qa"
AI_PROMPTS_AVAILABLE = ["default", "knowledge_qa", "trading", "analysis"]

# ============================================================
# 23. COGNITIVE MIRROR
# ============================================================

COGNITIVE_MIRROR_ENABLED = True
COGNITIVE_MIRROR_REFRESH_INTERVAL = 30
COGNITIVE_MIRROR_MAX_REFLECTIONS = 50

# ============================================================
# 24. API ENDPOINTS (Referensi)
# ============================================================

API_PUBLIC_ENDPOINTS = {
    "/api/health": "Health check (no auth required)",
}

API_PROTECTED_ENDPOINTS = {
    "/api/status": "System status",
    "/api/performance": "Trading performance",
    "/api/brain/state": "Cognitive Brain state",
    "/api/signals": "Live signals",
    "/api/system/metrics": "CPU, RAM, uptime, health score",
    "/api/watchdog/status": "Watchdog status",
    "/api/telegram/status": "Telegram status",
    # AI Endpoints
    "/api/ai/status": "AI integration status",
    "/api/ai/ask": "Ask AI a question",
    "/api/ai/chat": "Chat with AI",
    "/api/ai/prompts": "List AI prompts",
    # Knowledge Endpoints
    "/api/knowledge/all": "Get all knowledge",
    "/api/knowledge/add": "Add knowledge",
    "/api/knowledge/search": "Search knowledge",
    "/api/knowledge/stats": "Knowledge statistics",
    # Cognitive Mirror
    "/api/cognitive-mirror/metrics": "Cognitive metrics",
    "/api/cognitive-mirror/reflections": "Neural reflections",
    "/api/cognitive-mirror/narrative": "Cognitive narrative",
}

# ============================================================
# 25. COLORS & EMOJIS
# ============================================================

COLORS = {
    "BUY": "#00C853",
    "SELL": "#FF1744",
    "HOLD": "#FFD600",
    "MONITOR": "#2979FF",
    "EXIT": "#FF6D00",
    "PROFIT": "#00C853",
    "LOSS": "#FF1744",
    "NEUTRAL": "#78909C",
    "STRONG": "#00E676",
    "WEAK": "#FFAB00",
    "VERY_STRONG": "#00E5FF",
    "CRITICAL": "#D50000",
    "WARNING": "#FF9100",
    "INFO": "#40C4FF",
    "SUCCESS": "#69F0AE",
}

EMOJIS = {
    "BUY": "🟢",
    "SELL": "🔴",
    "HOLD": "🟡",
    "MONITOR": "🔵",
    "EXIT": "🟠",
    "PROFIT": "💰",
    "LOSS": "💸",
    "STRONG": "💪",
    "WEAK": "🤏",
    "NEUTRAL": "⚖️",
    "ALERT": "🚨",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "WARNING": "⚠️",
    "TRADE": "📊",
    "BRAIN": "🧠",
    "LEARNING": "📚",
    "PATTERN": "🎯",
    "PREDICTION": "🔮",
    "HEALTH": "💚",
    "MEMORY": "🧩",
    "REFLECTION": "🪞",
    "CONSCIOUSNESS": "✨",
}

# ============================================================
# 26. INTELLIGENCE MODULES
# ============================================================

INTELLIGENCE_MODULES = {
    "Learning": [
        "Learning Engine",
        "Market Learning",
        "Pattern Engine",
        "Prediction",
        "Reasoning",
    ],
    "Decision": [
        "Decision Engine",
        "Strategy Generation",
        "Goal Manager",
    ],
    "Memory": [
        "Experience Engine",
        "Semantic Memory",
        "Knowledge Graph",
        "Archive Manager",
    ],
    "Analysis": [
        "Feature Extractor",
        "Entity Recognition",
        "Normalizer",
        "Data Cleaner",
    ],
    "Self": [
        "Self-Diagnostic",
        "Improvement Engine",
        "Behavior Learning",
        "Reflection",
    ],
}

# ============================================================
# 27. UTILITY FUNCTIONS
# ============================================================

def validate_config() -> List[str]:
    """Validasi semua konfigurasi dan kembalikan daftar masalah."""
    issues = []
    
    if TELEGRAM_ENABLED and not TELEGRAM_BOT_TOKEN:
        issues.append("TELEGRAM_ENABLED is True but TELEGRAM_BOT_TOKEN is empty")
    
    if TELEGRAM_ENABLED and not TELEGRAM_CHAT_ID:
        issues.append("TELEGRAM_ENABLED is True but TELEGRAM_CHAT_ID is empty")
    
    if not DEFAULT_PAIRS:
        issues.append("DEFAULT_PAIRS is empty")
    
    if not DEFAULT_TIMEFRAMES:
        issues.append("DEFAULT_TIMEFRAMES is empty")
    
    if SCAN_INTERVAL_SECONDS < 120:
        issues.append(f"SCAN_INTERVAL_SECONDS={SCAN_INTERVAL_SECONDS} too frequent (min 120s)")
    
    for dir_path in [DATA_DIR, LOG_DIR, DATABASE_DIR, CACHE_DIR]:
        if not dir_path.exists():
            issues.append(f"Directory does not exist: {dir_path}")
        elif not dir_path.is_dir():
            issues.append(f"Not a directory: {dir_path}")
    
    return issues


def get_config_summary() -> Dict[str, Any]:
    """Dapatkan ringkasan konfigurasi."""
    return {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "exchange": EXCHANGE_NAME,
        "pairs_count": len(DEFAULT_PAIRS),
        "timeframes": DEFAULT_TIMEFRAMES,
        "main_timeframe": MAIN_TIMEFRAME,
        "scan_interval": SCAN_INTERVAL_SECONDS,
        "telegram_enabled": TELEGRAM_ENABLED,
        "trading_enabled": TRADING_ENABLED,
        "paper_trading": PAPER_TRADING,
        "debug_mode": DEBUG_MODE,
        "log_level": LOG_LEVEL,
        "learning_enabled": LEARNING_ENABLED,
        "prediction_enabled": PREDICTION_ENABLED,
        "health_min_score": HEALTH_MIN_SCORE,
        "ai_enabled": DEEPSEEK_ENABLED,
    }


def apply_env_overrides() -> Dict[str, Any]:
    """Terapkan override dari environment variables."""
    overrides = {}
    
    # Telegram
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        overrides["TELEGRAM_BOT_TOKEN"] = os.getenv("TELEGRAM_BOT_TOKEN")
    if os.getenv("TELEGRAM_CHAT_ID"):
        overrides["TELEGRAM_CHAT_ID"] = os.getenv("TELEGRAM_CHAT_ID")
    
    # Trading
    if os.getenv("TRADING_ENABLED"):
        overrides["TRADING_ENABLED"] = os.getenv("TRADING_ENABLED").lower() == "true"
    if os.getenv("PAPER_TRADING"):
        overrides["PAPER_TRADING"] = os.getenv("PAPER_TRADING").lower() == "true"
    
    # Debug
    if os.getenv("DEBUG_MODE"):
        overrides["DEBUG_MODE"] = os.getenv("DEBUG_MODE").lower() == "true"
    if os.getenv("LOG_LEVEL"):
        overrides["LOG_LEVEL"] = os.getenv("LOG_LEVEL")
    
    # AI
    if os.getenv("DEEPSEEK_ENABLED"):
        overrides["DEEPSEEK_ENABLED"] = os.getenv("DEEPSEEK_ENABLED").lower() == "true"
    if os.getenv("DEEPSEEK_API_KEY"):
        overrides["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
    
    return overrides


# ============================================================
# TERAPKAN ENVIRONMENT OVERRIDES
# ============================================================

ENV_OVERRIDES = apply_env_overrides()
for key, value in ENV_OVERRIDES.items():
    if key in globals():
        globals()[key] = value


# ============================================================
# KONFIGURASI LOADED
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print("=" * 70)
    print(f"  Exchange    : {EXCHANGE_NAME}")
    print(f"  Pairs       : {len(DEFAULT_PAIRS)} pairs")
    print(f"  Timeframes  : {', '.join(DEFAULT_TIMEFRAMES)}")
    print(f"  Scan Interval: {SCAN_INTERVAL_SECONDS}s")
    print(f"  Request Delay: {REQUEST_DELAY}s")
    print(f"  Telegram    : {'ENABLED' if TELEGRAM_ENABLED else 'DISABLED'}")
    print(f"  Trading     : {'ENABLED' if TRADING_ENABLED else 'DISABLED'}")
    print(f"  Paper Trading: {PAPER_TRADING}")
    print(f"  Debug Mode  : {DEBUG_MODE}")
    print(f"  Log Level   : {LOG_LEVEL}")
    print(f"  AI Enabled  : {DEEPSEEK_ENABLED}")
    print(f"  Auto-Crawl  : {len(AUTO_CRAWL_SOURCES)} sources")
    print("=" * 70)
    
    issues = validate_config()
    if issues:
        print("\n⚠️ Configuration Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ Configuration validated successfully")
    
    print("=" * 70)
