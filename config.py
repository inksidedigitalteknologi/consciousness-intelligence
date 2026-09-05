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

APP_NAME = "INKSIDEDIGITAL CONSCIOUSNESS INTELLIGENCE"
APP_VERSION = "2.0.0"
APP_AUTHOR = "Inkside Digital"
BUILD_DATE = "2026-09-05"

# Versi komponen
COGNITIVE_ENGINE_VERSION = "4.4"
SIGNAL_ENGINE_VERSION = "2.2"
COINGECKO_VERSION = "1.0.0"

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
# 4. EXCHANGE - COINGECKO (FREE, NO API KEY)
# ============================================================

EXCHANGE_NAME = "CoinGecko"
EXCHANGE_TYPE = "coingecko"
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")

# Rate Limiting - AMAN
COINGECKO_RATE_LIMIT = 30        # Max 30 requests per minute (free tier)
COINGECKO_RATE_LIMIT_SECONDS = 60
REQUEST_DELAY = 2.0              # Delay antar request (detik) - AMAN
REQUEST_TIMEOUT = 15
REQUEST_RETRY_COUNT = 3
REQUEST_RETRY_DELAY = 5
REQUEST_BACKOFF_MULTIPLIER = 2

# Cache
CACHE_TTL_SECONDS = 120          # 2 menit cache
OHLCV_LIMIT = 100                # Kurangi jumlah candle
MAX_MARKETS = 15                 # Maksimum pair

# ============================================================
# 5. MARKET & PAIRS (DIKURANGI UNTUK HINDARI RATE LIMIT)
# ============================================================

DEFAULT_PAIRS = [
    "BTC/USD",
    "ETH/USD",
    "SOL/USD",
    "XRP/USD",
    "BNB/USD",
    # Tambahkan sesuai kebutuhan, tapi hati-hati rate limit
]

DEFAULT_TIMEFRAMES = [
    "1h",   # Primary
    "4h",   # Medium-long
    "1d",   # Long-term
]

MAIN_TIMEFRAME = "1h"
SCALP_TIMEFRAME = "15m"
SWING_TIMEFRAME = "4h"
LONG_TIMEFRAME = "1d"

# ============================================================
# 6. SCANNER SETTINGS - OPTIMAL UNTUK RATE LIMIT
# ============================================================

SCAN_INTERVAL_SECONDS = 600      # 10 menit
MAX_WORKERS = 2                  # Kurangi parallel request
MAX_RETRIES = 2
USE_CLOSED_CANDLE = True
CACHE_OHLCV = True

SCANNER_BATCH_SIZE = 2           # Batch kecil
SCANNER_BATCH_DELAY = 5.0        # Delay antar batch (detik)
SCANNER_TIMEOUT = 60

# ============================================================
# 7. SIGNAL SETTINGS - SELEKTIF & STABIL
# ============================================================

MIN_MTF_ALIGNMENT = 2            # Minimal 2 timeframe align
MIN_SIGNAL_STRENGTH = 60
MIN_SIGNAL_CONFIDENCE = 60
SEND_STARTUP_SIGNALS = False
SIGNAL_COOLDOWN_SECONDS = 7200   # 2 jam cooldown per pair
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

DEFAULT_RISK_PERCENT = 1.0
DEFAULT_RISK_REWARD = 3.0
MAX_POSITION_SIZE = 10.0
MIN_POSITION_SIZE = 5.0
MAX_DAILY_TRADES = 10
MAX_OPEN_POSITIONS = 5
MAX_DRAWDOWN_PERCENT = 20.0
STOP_LOSS_PERCENT = 5.0
TAKE_PROFIT_PERCENT = 15.0

# ============================================================
# 11. TRADING MODE - PAPER TRADING (AMAN)
# ============================================================

TRADING_ENABLED = False
PAPER_TRADING = True
AUTO_TRADE = False
DEMO_MODE = False
TEST_MODE = False

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

# Telegram Commands (dari repositori)
TELEGRAM_COMMANDS = {
    "/start": "System overview",
    "/health": "Health check",
    "/performance": "Trading performance",
    "/signals": "Live signals",
    "/pnl": "Profit/Loss report",
    "/brain": "Brain status",
    "/modules": "Module status",
    "/daily": "Daily report",
    "/risk": "Risk assessment",
    "/trade": "Quick trade action",
    "/refresh": "Refresh data",
}

# ============================================================
# 13. LOGGING
# ============================================================

LOG_LEVEL = "INFO"
LOG_FILE_LEVEL = "DEBUG"
CONSOLE_LEVEL = "INFO"
ENABLE_FILE_LOG = True
ENABLE_CONSOLE_LOG = True
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_SIZE_MB = 100
LOG_BACKUP_COUNT = 5

ENABLE_SIGNAL_LOGGING = True
ENABLE_TRADE_LOGGING = True
ENABLE_ERROR_LOGGING = True
ENABLE_PERFORMANCE_LOGGING = True

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
PREDICTION_HORIZON = [5, 15, 30, 60]  # Minutes
PREDICTION_MIN_CONFIDENCE = 0.6
PREDICTION_MAX_HISTORY = 1000

# ============================================================
# 16. HEALTH MONITOR
# ============================================================

HEALTH_CHECK_INTERVAL = 60
HEALTH_METRICS_PERSIST = True
HEALTH_ALERT_ON_DEGRADE = True
HEALTH_MIN_SCORE = 80.0
HEALTH_CRITICAL_SCORE = 50.0

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
AUTO_RESTART = False
RESTART_DELAY = 10

MAX_THREADS = 10
THREAD_POOL_SIZE = 5
QUEUE_SIZE = 50

GLOBAL_TIMEOUT = 120
API_TIMEOUT = 15
DB_TIMEOUT = 10

# ============================================================
# 19. API ENDPOINTS (Referensi dari repositori)
# ============================================================

API_PUBLIC_ENDPOINTS = {
    "/api/health": "Health check (no auth required)",
}

API_PROTECTED_ENDPOINTS = {
    "/api/status": "System status",
    "/api/performance": "Trading performance",
    "/api/brain/state": "Cognitive Brain state",
    "/api/signals": "Live signals",
    "/api/predictions": "Real predictions",
    "/api/predictions/metrics": "Prediction metrics",
    "/api/predictions/monte_carlo": "Monte Carlo simulation",
    "/api/engine/start": "Start trading engine",
    "/api/engine/stop": "Stop trading engine",
    "/api/engine/status": "Engine status",
    "/api/system/metrics": "CPU, RAM, uptime, health score",
    "/api/watchdog/status": "Watchdog status",
    "/api/watchdog/snapshot": "Watchdog snapshot",
    "/api/telegram/webhook": "Webhook receiver",
    "/api/telegram/set_webhook": "Set webhook URL",
    "/api/telegram/get_webhook": "Webhook info",
    # AI Endpoints
    "/api/ai/status": "AI integration status",
    "/api/ai/ask": "Ask AI a question",
    "/api/ai/analyze": "Market analysis with AI",
    "/api/ai/strategy": "Generate trading strategy with AI",
    "/api/ai/brain/reflection": "Brain reflection with AI",
    "/api/ai/signal/validate": "Validate signal with AI",
    "/api/ai/chat": "Chat with AI",
}

# ============================================================
# 20. COINGECKO PAIR MAPPING
# ============================================================

PAIR_TO_COINGECKO = {
    "BTC/USD": "bitcoin",
    "ETH/USD": "ethereum",
    "SOL/USD": "solana",
    "XRP/USD": "ripple",
    "ADA/USD": "cardano",
    "LTC/USD": "litecoin",
    "BNB/USD": "binancecoin",
    "DOT/USD": "polkadot",
    "LINK/USD": "chainlink",
    "AVAX/USD": "avalanche-2",
    "MATIC/USD": "matic-network",
}

COINGECKO_TO_PAIR = {v: k for k, v in PAIR_TO_COINGECKO.items()}

# ============================================================
# 21. COLORS & EMOJIS
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
# 22. INTELLIGENCE MODULES (Referensi dari repositori)
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
# 23. UTILITY FUNCTIONS
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
    }


def load_config_from_file(config_path: Path) -> Optional[Dict]:
    """Load konfigurasi dari file JSON."""
    try:
        import json
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None


def save_config_to_file(config: Dict, config_path: Path) -> bool:
    """Simpan konfigurasi ke file JSON."""
    try:
        import json
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False


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
    print("=" * 70)
    
    issues = validate_config()
    if issues:
        print("\n⚠️ Configuration Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ Configuration validated successfully")
    
    print("=" * 70)


# ============================================================
# EXPORTS - SEMUA KONFIGURASI TERSEDIA
# ============================================================

__all__ = [
    # App
    'APP_NAME', 'APP_VERSION', 'APP_AUTHOR', 'BUILD_DATE',
    'COGNITIVE_ENGINE_VERSION', 'SIGNAL_ENGINE_VERSION', 'COINGECKO_VERSION',
    
    # Path
    'BASE_DIR', 'DATA_DIR', 'LOG_DIR', 'DATABASE_DIR', 'CACHE_DIR',
    'BACKUP_DIR', 'REPORTS_DIR',
    
    # Files
    'SETTINGS_FILE', 'WATCHLIST_FILE', 'HISTORY_FILE', 'TRADES_FILE',
    'PERFORMANCE_FILE', 'LEARNING_STATE_FILE', 'KNOWLEDGE_GRAPH_FILE',
    'PATTERN_DATABASE_FILE', 'LOG_FILE', 'ERROR_LOG_FILE', 'SIGNAL_LOG_FILE',
    
    # Exchange
    'EXCHANGE_NAME', 'EXCHANGE_TYPE', 'COINGECKO_API_BASE',
    'COINGECKO_RATE_LIMIT', 'COINGECKO_RATE_LIMIT_SECONDS',
    'REQUEST_DELAY', 'REQUEST_TIMEOUT', 'REQUEST_RETRY_COUNT',
    'REQUEST_RETRY_DELAY', 'REQUEST_BACKOFF_MULTIPLIER',
    'CACHE_TTL_SECONDS', 'OHLCV_LIMIT', 'MAX_MARKETS',
    
    # Market
    'DEFAULT_PAIRS', 'DEFAULT_TIMEFRAMES', 'MAIN_TIMEFRAME',
    'SCALP_TIMEFRAME', 'SWING_TIMEFRAME', 'LONG_TIMEFRAME',
    
    # Scanner
    'SCAN_INTERVAL_SECONDS', 'MAX_WORKERS', 'MAX_RETRIES',
    'USE_CLOSED_CANDLE', 'CACHE_OHLCV', 'SCANNER_BATCH_SIZE',
    'SCANNER_BATCH_DELAY', 'SCANNER_TIMEOUT',
    
    # Signal
    'MIN_MTF_ALIGNMENT', 'MIN_SIGNAL_STRENGTH', 'MIN_SIGNAL_CONFIDENCE',
    'SEND_STARTUP_SIGNALS', 'SIGNAL_COOLDOWN_SECONDS',
    'MAX_SIGNALS_PER_SCAN', 'MIN_SIGNAL_QUALITY',
    'QUALITY_WEAK', 'QUALITY_NEUTRAL', 'QUALITY_STRONG', 'QUALITY_VERY_STRONG',
    'SIGNAL_HOLD', 'SIGNAL_BUY', 'SIGNAL_SELL', 'SIGNAL_MONITOR', 'SIGNAL_EXIT',
    
    # Timeframes
    'TIMEFRAME_WEIGHTS',
    
    # Indicators
    'RSI_PERIOD', 'RSI_OVERBOUGHT', 'RSI_OVERSOLD',
    'MACD_FAST', 'MACD_SLOW', 'MACD_SIGNAL',
    'MA_FAST', 'MA_MEDIUM', 'MA_SLOW', 'MA_VERY_SLOW',
    'BB_PERIOD', 'BB_STD_DEV',
    'ATR_PERIOD', 'ATR_SL_MULTIPLIER',
    'TP1_ATR_MULTIPLIER', 'TP2_ATR_MULTIPLIER', 'TP3_ATR_MULTIPLIER',
    'VOLUME_MA_PERIOD', 'VOLUME_SPIKE_MULTIPLIER',
    
    # Risk
    'DEFAULT_RISK_PERCENT', 'DEFAULT_RISK_REWARD',
    'MAX_POSITION_SIZE', 'MIN_POSITION_SIZE',
    'MAX_DAILY_TRADES', 'MAX_OPEN_POSITIONS',
    'MAX_DRAWDOWN_PERCENT', 'STOP_LOSS_PERCENT', 'TAKE_PROFIT_PERCENT',
    
    # Trading
    'TRADING_ENABLED', 'PAPER_TRADING', 'AUTO_TRADE',
    'DEMO_MODE', 'TEST_MODE', 'ORDER_TYPE', 'ORDER_TIF', 'ORDER_LEVERAGE',
    
    # Telegram
    'TELEGRAM_ENABLED', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID',
    'TELEGRAM_TIMEOUT', 'TELEGRAM_RETRY_COUNT', 'TELEGRAM_RETRY_DELAY',
    'TELEGRAM_COMMANDS',
    
    # Logging
    'LOG_LEVEL', 'LOG_FILE_LEVEL', 'CONSOLE_LEVEL',
    'ENABLE_FILE_LOG', 'ENABLE_CONSOLE_LOG',
    'LOG_FORMAT', 'LOG_DATE_FORMAT', 'LOG_MAX_SIZE_MB', 'LOG_BACKUP_COUNT',
    'ENABLE_SIGNAL_LOGGING', 'ENABLE_TRADE_LOGGING',
    'ENABLE_ERROR_LOGGING', 'ENABLE_PERFORMANCE_LOGGING',
    
    # Learning
    'LEARNING_ENABLED', 'LEARNING_INTERVAL_SECONDS',
    'LEARNING_AUTO_START', 'LEARNING_MAX_HISTORY',
    
    # Prediction
    'PREDICTION_ENABLED', 'PREDICTION_HORIZON',
    'PREDICTION_MIN_CONFIDENCE', 'PREDICTION_MAX_HISTORY',
    
    # Health
    'HEALTH_CHECK_INTERVAL', 'HEALTH_METRICS_PERSIST',
    'HEALTH_ALERT_ON_DEGRADE', 'HEALTH_MIN_SCORE', 'HEALTH_CRITICAL_SCORE',
    
    # Performance
    'TRACK_PERFORMANCE', 'PERFORMANCE_UPDATE_INTERVAL',
    'PERFORMANCE_PERSIST_INTERVAL', 'MAX_PERFORMANCE_HISTORY',
    'METRICS_TRACKED',
    
    # System
    'DEBUG_MODE', 'ENABLE_PROFILING', 'ENABLE_TRACING',
    'ENABLE_METRICS', 'AUTO_RESTART', 'RESTART_DELAY',
    'MAX_THREADS', 'THREAD_POOL_SIZE', 'QUEUE_SIZE',
    'GLOBAL_TIMEOUT', 'API_TIMEOUT', 'DB_TIMEOUT',
    
    # API
    'API_PUBLIC_ENDPOINTS', 'API_PROTECTED_ENDPOINTS',
    
    # CoinGecko Mapping
    'PAIR_TO_COINGECKO', 'COINGECKO_TO_PAIR',
    
    # Colors & Emojis
    'COLORS', 'EMOJIS',
    
    # Intelligence Modules
    'INTELLIGENCE_MODULES',
    
    # Utilities
    'validate_config', 'get_config_summary',
    'load_config_from_file', 'save_config_to_file',
    'apply_env_overrides',
]
