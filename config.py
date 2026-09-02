# ============================================================
# INKSIDEDIGITAL TRADING BOT
# CONFIGURATION - PRODUCTION READY
#
# Version: 3.2.1 - REAL DATA MODE
#
# Perubahan:
# - DEBUG_MODE = False (matikan mock data)
# - DEMO_MODE = False (matikan demo)
# - Signal threshold dinaikkan untuk stabilitas
# - Scan interval diperpanjang
# - Learning engine dioptimalkan
# - Telegram dinonaktifkan (kecuali diisi token)
# ============================================================

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# ============================================================
# BASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
DATABASE_DIR = BASE_DIR / "database"
CACHE_DIR = BASE_DIR / "cache"
BACKUP_DIR = BASE_DIR / "backups"
REPORTS_DIR = BASE_DIR / "reports"

# Create directories
for dir_path in [DATA_DIR, LOG_DIR, DATABASE_DIR, CACHE_DIR, BACKUP_DIR, REPORTS_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)

# ============================================================
# APPLICATION
# ============================================================

APP_NAME = "INKSIDEDIGITAL TRADING BOT"
APP_VERSION = "3.2.1"
SIGNAL_ENGINE_VERSION = "3.2"
COGNITIVE_ENGINE_VERSION = "4.4"
BUILD_DATE = "2026-08-14"
APP_AUTHOR = "Inkside Digital"

# ============================================================
# FILE PATHS
# ============================================================

SETTINGS_FILE = DATA_DIR / "settings.json"
WATCHLIST_FILE = DATA_DIR / "watchlist.json"
HISTORY_FILE = DATA_DIR / "signal_history.json"
TRADES_FILE = DATA_DIR / "trades.json"
PERFORMANCE_FILE = DATA_DIR / "performance.json"
LEARNING_STATE_FILE = DATABASE_DIR / "learning_state.json"
KNOWLEDGE_GRAPH_FILE = DATABASE_DIR / "knowledge_graph.json"
PATTERN_DATABASE_FILE = DATABASE_DIR / "patterns.db"
LOG_FILE = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
ERROR_LOG_FILE = LOG_DIR / f"error_{datetime.now().strftime('%Y%m%d')}.log"
SIGNAL_LOG_FILE = LOG_DIR / f"signals_{datetime.now().strftime('%Y%m%d')}.log"

# ============================================================
# TELEGRAM CONFIGURATION
# ============================================================

TELEGRAM_ENABLED = False  # Set ke True hanya jika token valid
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_TIMEOUT = 15
TELEGRAM_RETRY_COUNT = 3
TELEGRAM_RETRY_DELAY = 2

# ============================================================
# EXCHANGE CONFIGURATION - PRODUCTION
# ============================================================

EXCHANGE_NAME = "Kraken"
EXCHANGE_ID = "kraken"
KRAKEN_API_URL = "https://api.kraken.com/0/public"
KRAKEN_PRIVATE_API_URL = "https://api.kraken.com/0/private"

# API Keys (from environment variables for security)
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY", "")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET", "")
KRAKEN_OTP_SECRET = os.getenv("KRAKEN_OTP_SECRET", "")

# Rate Limiting
KRAKEN_RATE_LIMIT = 15
KRAKEN_RATE_LIMIT_PUBLIC = 20
KRAKEN_RATE_LIMIT_PRIVATE = 10
REQUEST_TIMEOUT = 30
REQUEST_RETRY_COUNT = 3
REQUEST_RETRY_DELAY = 1
REQUEST_BACKOFF_MULTIPLIER = 2

# ============================================================
# MARKET SETTINGS
# ============================================================

DEFAULT_PAIRS = [
    # Major Cryptocurrencies
    "BTC/USD",
    "ETH/USD",
    "SOL/USD",
    "XRP/USD",
    "ADA/USD",
    # Layer 1
    "AVAX/USD",
    "LINK/USD",
    "DOT/USD",
    "LTC/USD",
    "BCH/USD",
    # DeFi & Smart Contracts
    "ATOM/USD",
    "UNI/USD",
    "AAVE/USD",
    "ETC/USD",
    "FIL/USD",
    # Layer 2 & Emerging
    "NEAR/USD",
    "ARB/USD",
    "OP/USD",
    "TRX/USD",
    "XLM/USD",
]

DEFAULT_TIMEFRAMES = [
    "5m",   # Short-term
    "15m",  # Medium-short
    "1h",   # Medium (primary)
    "4h",   # Medium-long
    "1d",   # Long-term
    "1w",   # Very long-term
]

MAIN_TIMEFRAME = "1h"
SCALP_TIMEFRAME = "15m"
SWING_TIMEFRAME = "4h"
LONG_TIMEFRAME = "1d"

# ============================================================
# SCANNER SETTINGS - STABIL
# ============================================================

SCAN_INTERVAL_SECONDS = 300     # 5 minutes (tidak terlalu cepat)
OHLCV_LIMIT = 500               # Cukup untuk analisis
MAX_MARKETS = 30                # Fokus pada pair utama
MAX_WORKERS = 8                 # Optimal
REQUEST_DELAY = 0.2
MAX_RETRIES = 5
USE_CLOSED_CANDLE = True
CACHE_OHLCV = True
CACHE_TTL_SECONDS = 120         # 2 menit cache

SCANNER_BATCH_SIZE = 5
SCANNER_BATCH_DELAY = 0.5
SCANNER_TIMEOUT = 60

# ============================================================
# SIGNAL SETTINGS - STABIL & SELEKTIF
# ============================================================

# Core Signal Parameters - DIPERKETAT
MIN_MTF_ALIGNMENT = 4           # Minimal 4 timeframe align
MIN_SIGNAL_STRENGTH = 70        # Minimal 70% strength
MIN_SIGNAL_CONFIDENCE = 70      # Minimal 70% confidence
SEND_STARTUP_SIGNALS = False    # Jangan kirim sinyal startup
SIGNAL_COOLDOWN_SECONDS = 7200  # 2 jam cooldown per pair
MAX_SIGNALS_PER_SCAN = 3        # Maksimal 3 sinyal per scan
MIN_SIGNAL_QUALITY = 60         # Minimal 60% quality

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
# TIMEFRAME WEIGHTS - TIME FRAME BESAR LEBIH BERPENGARUH
# ============================================================

TIMEFRAME_WEIGHTS = {
    "5m": 0.8,      # Kurangi noise
    "15m": 1.5,     # Medium
    "1h": 2.5,      # Primary (dinaikkan)
    "4h": 3.0,      # Penting
    "1d": 4.0,      # Sangat penting
    "1w": 5.0,      # Paling penting
}

# ============================================================
# INDICATOR SETTINGS
# ============================================================

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
RSI_OVERBOUGHT_EXTREME = 80
RSI_OVERSOLD_EXTREME = 20

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
# RISK MANAGEMENT
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
TRAILING_STOP_PERCENT = 2.0

# ============================================================
# TRADING MODE - PAPER TRADING (AMAN)
# ============================================================

TRADING_ENABLED = False         # Tetap False untuk paper
PAPER_TRADING = True            # Paper trading (aman)
AUTO_TRADE = False              # Manual dulu
DEMO_MODE = False               # Matikan demo (pakai real data)
TEST_MODE = False               # Matikan test

ORDER_TYPE = "market"
ORDER_TIF = "GTC"
ORDER_LEVERAGE = 1

# ============================================================
# GUI SETTINGS
# ============================================================

WINDOW_SIZE = "1500x900"
MIN_WINDOW_WIDTH = 1100
MIN_WINDOW_HEIGHT = 700
THEME = "dark"
COLOR_THEME = "blue"
FONT_SIZE = 12
FONT_FAMILY = "Segoe UI"

SHOW_DASHBOARD = True
SHOW_CHARTS = True
SHOW_SIGNALS = True
SHOW_PORTFOLIO = True
SHOW_LEARNING = True
SHOW_KNOWLEDGE = True
SHOW_HEALTH = True

# ============================================================
# LEARNING ENGINE - OPTIMAL
# ============================================================

LEARNING_ENABLED = True
LEARNING_INTERVAL_SECONDS = 300
LEARNING_AUTO_START = True
LEARNING_MAX_HISTORY = 1000
LEARNING_MODULE_TIMEOUT = 30
LEARNING_RETRY_COUNT = 3
LEARNING_BACKOFF_MULTIPLIER = 1.5
LEARNING_MAX_WORKERS = 4
LEARNING_CONTINUE_ON_ERROR = True

KNOWLEDGE_MAX_NODES = 10000
KNOWLEDGE_MAX_EDGES = 50000
KNOWLEDGE_PERSIST_INTERVAL = 60

SEMANTIC_MEMORY_SIZE = 1000
SEMANTIC_EMBEDDING_DIM = 128

PATTERN_MIN_CONFIDENCE = 0.75
PATTERN_MAX_LIFETIME = 3600
PATTERN_MIN_OCCURRENCES = 3

# ============================================================
# PREDICTION ENGINE
# ============================================================

PREDICTION_ENABLED = True
PREDICTION_HORIZON = [5, 15, 30, 60, 120]  # Minutes
PREDICTION_MIN_CONFIDENCE = 0.6            # Naikkan threshold
PREDICTION_MAX_HISTORY = 5000

# ============================================================
# HEALTH MONITOR
# ============================================================

HEALTH_CHECK_INTERVAL = 60
HEALTH_METRICS_PERSIST = True
HEALTH_ALERT_ON_DEGRADE = True
HEALTH_MIN_SCORE = 80.0
HEALTH_CRITICAL_SCORE = 50.0

# ============================================================
# LOGGING - INFO LEVEL (kurangi noise)
# ============================================================

LOG_LEVEL = "INFO"              # DEBUG -> INFO (kurangi noise)
LOG_FILE_LEVEL = "DEBUG"        # Tetap debug di file
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
# PERFORMANCE METRICS
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
# SYSTEM - PRODUCTION READY
# ============================================================

DEBUG_MODE = False              # 🔴 False = disable mock data
ENABLE_PROFILING = False        
ENABLE_TRACING = False
ENABLE_METRICS = True
AUTO_RESTART = False
RESTART_DELAY = 10

MAX_THREADS = 20
THREAD_POOL_SIZE = 10
QUEUE_SIZE = 100

GLOBAL_TIMEOUT = 120
API_TIMEOUT = 30
DB_TIMEOUT = 10

# ============================================================
# EXCHANGE PAIRS MAPPING (Kraken format)
# ============================================================

PAIRS_MAPPING = {
    "BTC/USD": "XBTUSD",
    "ETH/USD": "ETHUSD",
    "SOL/USD": "SOLUSD",
    "XRP/USD": "XRPUSD",
    "ADA/USD": "ADAUSD",
    "AVAX/USD": "AVAXUSD",
    "LINK/USD": "LINKUSD",
    "DOT/USD": "DOTUSD",
    "LTC/USD": "LTCUSD",
    "BCH/USD": "BCHUSD",
    "ATOM/USD": "ATOMUSD",
    "UNI/USD": "UNIUSD",
    "AAVE/USD": "AAVEUSD",
    "ETC/USD": "ETCUSD",
    "FIL/USD": "FILUSD",
    "NEAR/USD": "NEARUSD",
    "ARB/USD": "ARBUSD",
    "OP/USD": "OPUSD",
    "TRX/USD": "TRXUSD",
    "XLM/USD": "XLMUSD",
}

PAIRS_REVERSE_MAPPING = {v: k for k, v in PAIRS_MAPPING.items()}

# ============================================================
# COLORS
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

# ============================================================
# EMOJI MAPPING
# ============================================================

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
    "INFO": "ℹ️",
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
# UTILITY FUNCTIONS
# ============================================================

def merge_configs(base_config: Dict, override_config: Dict) -> Dict:
    result = base_config.copy()
    for key, value in override_config.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result


def validate_config() -> List[str]:
    issues = []
    
    if TELEGRAM_ENABLED and not TELEGRAM_BOT_TOKEN:
        issues.append("TELEGRAM_ENABLED is True but TELEGRAM_BOT_TOKEN is empty")
    
    if TELEGRAM_ENABLED and not TELEGRAM_CHAT_ID:
        issues.append("TELEGRAM_ENABLED is True but TELEGRAM_CHAT_ID is empty")
    
    if not DEFAULT_PAIRS:
        issues.append("DEFAULT_PAIRS is empty")
    
    if not DEFAULT_TIMEFRAMES:
        issues.append("DEFAULT_TIMEFRAMES is empty")
    
    if MIN_SIGNAL_CONFIDENCE < 0 or MIN_SIGNAL_CONFIDENCE > 100:
        issues.append(f"MIN_SIGNAL_CONFIDENCE={MIN_SIGNAL_CONFIDENCE} out of range (0-100)")
    
    if MIN_MTF_ALIGNMENT < 1:
        issues.append(f"MIN_MTF_ALIGNMENT={MIN_MTF_ALIGNMENT} should be at least 1")
    
    if SCAN_INTERVAL_SECONDS < 60:
        issues.append(f"SCAN_INTERVAL_SECONDS={SCAN_INTERVAL_SECONDS} too frequent (min 60s)")
    
    for dir_path in [DATA_DIR, LOG_DIR, DATABASE_DIR, CACHE_DIR]:
        if not dir_path.exists():
            issues.append(f"Directory does not exist: {dir_path}")
        elif not dir_path.is_dir():
            issues.append(f"Not a directory: {dir_path}")
    
    return issues


def get_config_summary() -> Dict[str, Any]:
    return {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "signal_engine_version": SIGNAL_ENGINE_VERSION,
        "exchange": EXCHANGE_NAME,
        "pairs_count": len(DEFAULT_PAIRS),
        "timeframes": DEFAULT_TIMEFRAMES,
        "main_timeframe": MAIN_TIMEFRAME,
        "scan_interval": SCAN_INTERVAL_SECONDS,
        "telegram_enabled": TELEGRAM_ENABLED,
        "trading_enabled": TRADING_ENABLED,
        "paper_trading": PAPER_TRADING,
        "auto_trade": AUTO_TRADE,
        "debug_mode": DEBUG_MODE,
        "log_level": LOG_LEVEL,
        "learning_enabled": LEARNING_ENABLED,
    }


def load_config_from_file(config_path: Path) -> Optional[Dict]:
    try:
        import json
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None


def save_config_to_file(config: Dict, config_path: Path) -> bool:
    try:
        import json
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False


def apply_env_overrides() -> Dict[str, Any]:
    overrides = {}
    
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        overrides["TELEGRAM_BOT_TOKEN"] = os.getenv("TELEGRAM_BOT_TOKEN")
    if os.getenv("TELEGRAM_CHAT_ID"):
        overrides["TELEGRAM_CHAT_ID"] = os.getenv("TELEGRAM_CHAT_ID")
    
    if os.getenv("KRAKEN_API_KEY"):
        overrides["KRAKEN_API_KEY"] = os.getenv("KRAKEN_API_KEY")
    if os.getenv("KRAKEN_API_SECRET"):
        overrides["KRAKEN_API_SECRET"] = os.getenv("KRAKEN_API_SECRET")
    
    if os.getenv("TRADING_ENABLED"):
        overrides["TRADING_ENABLED"] = os.getenv("TRADING_ENABLED").lower() == "true"
    if os.getenv("PAPER_TRADING"):
        overrides["PAPER_TRADING"] = os.getenv("PAPER_TRADING").lower() == "true"
    
    if os.getenv("DEBUG_MODE"):
        overrides["DEBUG_MODE"] = os.getenv("DEBUG_MODE").lower() == "true"
    if os.getenv("LOG_LEVEL"):
        overrides["LOG_LEVEL"] = os.getenv("LOG_LEVEL")
    
    return overrides


# ============================================================
# APPLY ENVIRONMENT OVERRIDES
# ============================================================

ENV_OVERRIDES = apply_env_overrides()
for key, value in ENV_OVERRIDES.items():
    if key in globals():
        globals()[key] = value

# ============================================================
# EXPOSE CONFIGURATION
# ============================================================

__all__ = [
    'APP_NAME', 'APP_VERSION', 'SIGNAL_ENGINE_VERSION', 
    'COGNITIVE_ENGINE_VERSION', 'BUILD_DATE', 'APP_AUTHOR',
    'BASE_DIR', 'DATA_DIR', 'LOG_DIR', 'DATABASE_DIR', 
    'CACHE_DIR', 'BACKUP_DIR', 'REPORTS_DIR',
    'SETTINGS_FILE', 'WATCHLIST_FILE', 'HISTORY_FILE',
    'TRADES_FILE', 'PERFORMANCE_FILE', 'LOG_FILE',
    'ERROR_LOG_FILE', 'SIGNAL_LOG_FILE',
    'LEARNING_STATE_FILE', 'KNOWLEDGE_GRAPH_FILE', 'PATTERN_DATABASE_FILE',
    'TELEGRAM_ENABLED', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID',
    'TELEGRAM_TIMEOUT', 'TELEGRAM_RETRY_COUNT', 'TELEGRAM_RETRY_DELAY',
    'EXCHANGE_NAME', 'EXCHANGE_ID', 'KRAKEN_API_URL',
    'KRAKEN_PRIVATE_API_URL', 'KRAKEN_API_KEY', 'KRAKEN_API_SECRET',
    'KRAKEN_OTP_SECRET', 'KRAKEN_RATE_LIMIT', 'KRAKEN_RATE_LIMIT_PUBLIC',
    'KRAKEN_RATE_LIMIT_PRIVATE', 'REQUEST_TIMEOUT', 'REQUEST_RETRY_COUNT',
    'REQUEST_RETRY_DELAY', 'REQUEST_BACKOFF_MULTIPLIER',
    'DEFAULT_PAIRS', 'DEFAULT_TIMEFRAMES', 'MAIN_TIMEFRAME',
    'SCALP_TIMEFRAME', 'SWING_TIMEFRAME', 'LONG_TIMEFRAME',
    'SCAN_INTERVAL_SECONDS', 'OHLCV_LIMIT', 'MAX_MARKETS',
    'MAX_WORKERS', 'REQUEST_DELAY', 'MAX_RETRIES',
    'USE_CLOSED_CANDLE', 'CACHE_OHLCV', 'CACHE_TTL_SECONDS',
    'SCANNER_BATCH_SIZE', 'SCANNER_BATCH_DELAY', 'SCANNER_TIMEOUT',
    'MIN_MTF_ALIGNMENT', 'MIN_SIGNAL_STRENGTH', 'MIN_SIGNAL_CONFIDENCE',
    'SEND_STARTUP_SIGNALS', 'SIGNAL_COOLDOWN_SECONDS', 'MAX_SIGNALS_PER_SCAN',
    'MIN_SIGNAL_QUALITY', 'QUALITY_WEAK', 'QUALITY_NEUTRAL',
    'QUALITY_STRONG', 'QUALITY_VERY_STRONG',
    'SIGNAL_HOLD', 'SIGNAL_BUY', 'SIGNAL_SELL', 'SIGNAL_MONITOR', 'SIGNAL_EXIT',
    'TIMEFRAME_WEIGHTS',
    'RSI_PERIOD', 'RSI_OVERBOUGHT', 'RSI_OVERSOLD',
    'RSI_OVERBOUGHT_EXTREME', 'RSI_OVERSOLD_EXTREME',
    'MACD_FAST', 'MACD_SLOW', 'MACD_SIGNAL',
    'MA_FAST', 'MA_MEDIUM', 'MA_SLOW', 'MA_VERY_SLOW',
    'BB_PERIOD', 'BB_STD_DEV',
    'ATR_PERIOD', 'ATR_SL_MULTIPLIER',
    'TP1_ATR_MULTIPLIER', 'TP2_ATR_MULTIPLIER', 'TP3_ATR_MULTIPLIER',
    'VOLUME_MA_PERIOD', 'VOLUME_SPIKE_MULTIPLIER',
    'DEFAULT_RISK_PERCENT', 'DEFAULT_RISK_REWARD',
    'MAX_POSITION_SIZE', 'MIN_POSITION_SIZE',
    'MAX_DAILY_TRADES', 'MAX_OPEN_POSITIONS',
    'MAX_DRAWDOWN_PERCENT', 'STOP_LOSS_PERCENT',
    'TAKE_PROFIT_PERCENT', 'TRAILING_STOP_PERCENT',
    'TRADING_ENABLED', 'PAPER_TRADING', 'AUTO_TRADE',
    'DEMO_MODE', 'TEST_MODE',
    'ORDER_TYPE', 'ORDER_TIF', 'ORDER_LEVERAGE',
    'WINDOW_SIZE', 'MIN_WINDOW_WIDTH', 'MIN_WINDOW_HEIGHT',
    'THEME', 'COLOR_THEME', 'FONT_SIZE', 'FONT_FAMILY',
    'SHOW_DASHBOARD', 'SHOW_CHARTS', 'SHOW_SIGNALS',
    'SHOW_PORTFOLIO', 'SHOW_LEARNING', 'SHOW_KNOWLEDGE', 'SHOW_HEALTH',
    'LEARNING_ENABLED', 'LEARNING_INTERVAL_SECONDS',
    'LEARNING_AUTO_START', 'LEARNING_MAX_HISTORY',
    'LEARNING_MODULE_TIMEOUT', 'LEARNING_RETRY_COUNT',
    'LEARNING_BACKOFF_MULTIPLIER', 'LEARNING_MAX_WORKERS',
    'LEARNING_CONTINUE_ON_ERROR',
    'KNOWLEDGE_MAX_NODES', 'KNOWLEDGE_MAX_EDGES',
    'KNOWLEDGE_PERSIST_INTERVAL',
    'SEMANTIC_MEMORY_SIZE', 'SEMANTIC_EMBEDDING_DIM',
    'PATTERN_MIN_CONFIDENCE', 'PATTERN_MAX_LIFETIME',
    'PATTERN_MIN_OCCURRENCES',
    'PREDICTION_ENABLED', 'PREDICTION_HORIZON',
    'PREDICTION_MIN_CONFIDENCE', 'PREDICTION_MAX_HISTORY',
    'HEALTH_CHECK_INTERVAL', 'HEALTH_METRICS_PERSIST',
    'HEALTH_ALERT_ON_DEGRADE', 'HEALTH_MIN_SCORE', 'HEALTH_CRITICAL_SCORE',
    'LOG_LEVEL', 'LOG_FILE_LEVEL', 'CONSOLE_LEVEL',
    'ENABLE_FILE_LOG', 'ENABLE_CONSOLE_LOG',
    'LOG_FORMAT', 'LOG_DATE_FORMAT', 'LOG_MAX_SIZE_MB',
    'LOG_BACKUP_COUNT', 'ENABLE_SIGNAL_LOGGING',
    'ENABLE_TRADE_LOGGING', 'ENABLE_ERROR_LOGGING',
    'ENABLE_PERFORMANCE_LOGGING',
    'TRACK_PERFORMANCE', 'PERFORMANCE_UPDATE_INTERVAL',
    'PERFORMANCE_PERSIST_INTERVAL', 'MAX_PERFORMANCE_HISTORY',
    'METRICS_TRACKED',
    'DEBUG_MODE', 'ENABLE_PROFILING', 'ENABLE_TRACING',
    'ENABLE_METRICS', 'AUTO_RESTART', 'RESTART_DELAY',
    'MAX_THREADS', 'THREAD_POOL_SIZE', 'QUEUE_SIZE',
    'GLOBAL_TIMEOUT', 'API_TIMEOUT', 'DB_TIMEOUT',
    'PAIRS_MAPPING', 'PAIRS_REVERSE_MAPPING',
    'COLORS', 'EMOJIS',
    'merge_configs', 'validate_config',
    'get_config_summary', 'load_config_from_file',
    'save_config_to_file', 'apply_env_overrides',
]

# ============================================================
# AUTONOMOUS LEARNING ENGINE CONFIGURATION
# ============================================================

# ============================================================
# KEYWORD INDONESIA UNTUK FILTER
# ============================================================

INDONESIA_KEYWORDS = [
    'indonesia', 'jakarta', 'jokowi', 'prabowo', 'megawati',
    'rupiah', 'bali', 'jaksel', 'indonesian', 'indonesi',
    'ekonomi indonesia', 'pasar modal indonesia', 'idx',
    'banten', 'jawa', 'sumatra', 'kalimantan', 'papua',
    'kpu', 'pemilu', 'presiden', 'menteri', 'kabinet',
    'saham indonesia', 'obligasi indonesia', 'bi rate',
    'bank indonesia', 'lq45', 'kompas100', 'idx composite',
    'jakarta composite', 'indonesia stock exchange',
]

# ============================================================
# RSS FEED SOURCES — STABIL & TERVERIFIKASI
# ============================================================

AUTONOMOUS_RSS_FEEDS = [
    # ----------------------------------------------------------
    # 1. CRYPTO (International) — STABIL
    # ----------------------------------------------------------
    {
        "url": "https://cointelegraph.com/rss",
        "category": "crypto",
        "source": "CoinTelegraph",
        "enabled": True,
        "max_items": 10,
        "confidence_base": 35.0,
    },
    {
        "url": "https://cryptoslate.com/feed/",
        "category": "crypto",
        "source": "CryptoSlate",
        "enabled": True,
        "max_items": 10,
        "confidence_base": 35.0,
    },
    {
        "url": "https://news.bitcoin.com/feed/",
        "category": "crypto",
        "source": "Bitcoin.com",
        "enabled": True,
        "max_items": 10,
        "confidence_base": 35.0,
    },
    {
        "url": "https://decrypt.co/feed",
        "category": "crypto",
        "source": "Decrypt",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 35.0,
    },
    {
        "url": "https://blockworks.co/feed",
        "category": "crypto",
        "source": "Blockworks",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 35.0,
    },
    {
        "url": "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "category": "crypto",
        "source": "CoinDesk",
        "enabled": True,
        "max_items": 10,
        "confidence_base": 40.0,
    },
    {
        "url": "https://cryptobriefing.com/feed/",
        "category": "crypto",
        "source": "CryptoBriefing",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 35.0,
    },
    {
        "url": "https://dailyhodl.com/feed/",
        "category": "crypto",
        "source": "Daily Hodl",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 30.0,
    },
    {
        "url": "https://u.today/rss",
        "category": "crypto",
        "source": "U.Today",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 30.0,
    },
    {
        "url": "https://cryptopotato.com/feed/",
        "category": "crypto",
        "source": "CryptoPotato",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 30.0,
    },
    {
        "url": "https://beincrypto.com/feed/",
        "category": "crypto",
        "source": "BeInCrypto",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 35.0,
    },
    {
        "url": "https://ambcrypto.com/feed/",
        "category": "crypto",
        "source": "AMBCrypto",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 30.0,
    },

    # ----------------------------------------------------------
    # 2. GLOBAL ECONOMY & MARKETS — STABIL
    # ----------------------------------------------------------
    {
        "url": "https://www.ft.com/markets?format=rss",
        "category": "global_economy",
        "source": "Financial Times",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 45.0,
    },
    {
        "url": "https://www.cnbc.com/id/10001164/device/rss/rss.html",
        "category": "global_economy",
        "source": "CNBC US",
        "enabled": True,
        "max_items": 10,
        "confidence_base": 40.0,
    },
    {
        "url": "https://finance.yahoo.com/news/rssindex",
        "category": "global_economy",
        "source": "Yahoo Finance",
        "enabled": True,
        "max_items": 10,
        "confidence_base": 40.0,
    },

    # ----------------------------------------------------------
    # 3. INVESTING & STOCKS — STABIL
    # ----------------------------------------------------------
    {
        "url": "https://www.marketwatch.com/rss/topstories",
        "category": "investing",
        "source": "MarketWatch",
        "enabled": True,
        "max_items": 10,
        "confidence_base": 40.0,
    },
    {
        "url": "https://seekingalpha.com/feed.xml",
        "category": "investing",
        "source": "Seeking Alpha",
        "enabled": True,
        "max_items": 8,
        "confidence_base": 40.0,
    },
    {
        "url": "https://www.investing.com/rss/news.rss",
        "category": "investing",
        "source": "Investing.com",
        "enabled": True,
        "max_items": 10,
        "confidence_base": 40.0,
    },

    # ----------------------------------------------------------
    # 4. INDONESIA — EKONOMI & BISNIS (STABIL)
    # ----------------------------------------------------------
    {
        "url": "https://www.kontan.co.id/feed",
        "category": "market_idn",
        "source": "Kontan",
        "enabled": False,
        "max_items": 8,
        "confidence_base": 40.0,
    },
    {
        "url": "https://bisnis.tempo.co/feed",
        "category": "market_idn",
        "source": "Tempo Bisnis",
        "enabled": False,
        "max_items": 8,
        "confidence_base": 40.0,
    },
    {
        "url": "https://www.republika.co.id/feed/ekonomi",
        "category": "market_idn",
        "source": "Republika Ekonomi",
        "enabled": False,
        "max_items": 6,
        "confidence_base": 35.0,
    },

    # ----------------------------------------------------------
    # 5. INDONESIA — KRIPTO & TEKNOLOGI (STABIL)
    # ----------------------------------------------------------
    {
        "url": "https://www.dailysocial.id/feed",
        "category": "crypto_idn",
        "source": "DailySocial",
        "enabled": True,
        "max_items": 6,
        "confidence_base": 35.0,
    },

    # ----------------------------------------------------------
    # 6. ANALYSIS & BLOGS — STABIL
    # ----------------------------------------------------------
    {
        "url": "https://unchainedcrypto.com/feed/",
        "category": "analysis",
        "source": "Unchained Crypto",
        "enabled": True,
        "max_items": 6,
        "confidence_base": 45.0,
    },
    {
        "url": "https://messari.io/feed",
        "category": "analysis",
        "source": "Messari",
        "enabled": True,
        "max_items": 6,
        "confidence_base": 50.0,
    },
    
    # ----------------------------------------------------------
    # 7. INDONESIA — TAMBAHAN (STABIL)
    # ----------------------------------------------------------
    {
        "url": "https://www.cnbcindonesia.com/rss/news",
        "category": "market_idn",
        "source": "CNBC Indonesia",
        "enabled": False,
        "max_items": 10,
        "confidence_base": 45.0,
    },
    {
        "url": "https://money.kompas.com/feed",
        "category": "market_idn",
        "source": "Kompas Money",
        "enabled": False,
        "max_items": 8,
        "confidence_base": 40.0,
    },
    {
        "url": "https://www.detik.com/feed/news",
        "category": "market_idn",
        "source": "Detik News",
        "enabled": False,
        "max_items": 8,
        "confidence_base": 40.0,
    },
]

# ============================================================
# AUTONOMOUS INTERVAL SETTINGS
# ============================================================

AUTONOMOUS_RSS_INTERVAL = 3600          # 1 jam
AUTONOMOUS_REANALYSIS_INTERVAL = 7200   # 2 jam
AUTONOMOUS_HEALTH_CHECK_INTERVAL = 300  # 5 menit

# ============================================================
# AUTONOMOUS CACHE & LIMITS
# ============================================================

AUTONOMOUS_CACHE_DIR = "data/autonomous_cache"
AUTONOMOUS_SEEN_IDS_FILE = "seen_ids.json"
AUTONOMOUS_STATS_FILE = "stats.json"

AUTONOMOUS_MAX_RSS_ITEMS = 10
AUTONOMOUS_MAX_KNOWLEDGE_LENGTH = 5000
AUTONOMOUS_CONFIDENCE_BASE = 35.0
AUTONOMOUS_REQUEST_TIMEOUT = 15

# ============================================================
# USER-AGENT (Untuk Menghindari Blokir)
# ============================================================

AUTONOMOUS_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# ============================================================
# GUI CONFIGURATION
# ============================================================

# ============================================================
# WINDOW
# ============================================================

GUI_APP_NAME = "INKSIDEDIGITAL TRADING BOT"
GUI_APP_SUBTITLE = "ALGORITHMIC MARKET INTELLIGENCE TERMINAL"

GUI_WINDOW_WIDTH = 1600
GUI_WINDOW_HEIGHT = 950
GUI_SIDEBAR_WIDTH = 260
GUI_TOPBAR_HEIGHT = 70
GUI_STATUSBAR_HEIGHT = 32

# ============================================================
# GUI COLORS
# ============================================================

GUI_COLORS = {
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
# LEARNING ENGINE CONFIGURATION
# ============================================================

# ============================================================
# LEARNING UPDATE INTERVAL
# ============================================================

LEARNING_UPDATE_INTERVAL = 3000  # 3 detik

# ============================================================
# LEARNING MODULE DISPLAY LIMITS
# ============================================================

LEARNING_MAX_MODULES_DISPLAY = 20  # Maksimal modul yang ditampilkan

# ============================================================
# LEARNING PROGRESS THRESHOLDS
# ============================================================

LEARNING_CYCLE_THRESHOLD = 100     # Target cycles untuk progress 100%
LEARNING_MODULE_THRESHOLD = 30     # Target modules untuk progress 100%

# ============================================================
# LEARNING STATUS TEXT
# ============================================================

LEARNING_STATUS_RUNNING = "🔄 Learning: ACTIVE"
LEARNING_STATUS_IDLE = "⏸️ Learning: IDLE"
LEARNING_STATUS_UNAVAILABLE = "❌ Learning: UNAVAILABLE"
LEARNING_STATUS_NOT_INSTALLED = "⚠️ Learning: NOT INSTALLED"

# ============================================================
# LEARNING MODULE COLORS
# ============================================================

LEARNING_MODULE_ENABLED_COLOR = "#22C55E"   # Hijau
LEARNING_MODULE_DISABLED_COLOR = "#EF4444"  # Merah
LEARNING_MODULE_DEFAULT_COLOR = "#8D9AAA"   # Abu-abu

# ============================================================
# LEARNING MODULE STATUS ICONS
# ============================================================

LEARNING_ICON_ENABLED = "✅"
LEARNING_ICON_DISABLED = "❌"
LEARNING_ICON_UNKNOWN = "❓"

# ============================================================
# LEARNING DETAILS TRUNCATE LIMIT
# ============================================================

LEARNING_DETAILS_MAX_LENGTH = 3000  # Karakter maksimal di details text

# ============================================================
# GUI FONTS
# ============================================================

GUI_FONT_FAMILY = "Segoe UI"
GUI_FONT_TITLE = (GUI_FONT_FAMILY, 22, "bold")
GUI_FONT_BUTTON = (GUI_FONT_FAMILY, 11, "bold")
GUI_FONT_SMALL = (GUI_FONT_FAMILY, 9)

# ============================================================
# GUI STATUS TEXT
# ============================================================

GUI_STATUS_ONLINE = "● SYSTEM ONLINE"
GUI_STATUS_OFFLINE = "● SYSTEM OFFLINE"
GUI_STATUS_READY = "● SYSTEM READY"

# ============================================================
# GUI EXCHANGE
# ============================================================

GUI_EXCHANGE_NAME = "KRAKEN"
GUI_EXCHANGE_LABEL = f"● {GUI_EXCHANGE_NAME}"

# ============================================================
# GUI TELEGRAM
# ============================================================

GUI_TELEGRAM_LABEL = "● TELEGRAM"
GUI_TELEGRAM_ACTIVE = "● TELEGRAM ACTIVE"
GUI_TELEGRAM_INACTIVE = "● TELEGRAM INACTIVE"

# ============================================================
# GUI ENGINE
# ============================================================

GUI_ENGINE_LABEL = "⚡ ENGINE: AUTO"

# ============================================================
# GUI INTELLIGENCE
# ============================================================

GUI_INTELLIGENCE_LABEL = "🧠"
GUI_INTELLIGENCE_ONLINE = "🧠 Intelligence: ONLINE"
GUI_INTELLIGENCE_OFFLINE = "🧠 Intelligence: N/A"

# ============================================================
# KNOWLEDGE BASE CONFIGURATION
# ============================================================

# ============================================================
# KNOWLEDGE DISPLAY
# ============================================================

KNOWLEDGE_ITEMS_PER_PAGE = 10
KNOWLEDGE_MAX_ITEMS_DISPLAY = 50
KNOWLEDGE_DETAILS_MAX_LENGTH = 3000
KNOWLEDGE_INSIGHTS_MAX_DISPLAY = 4

# ============================================================
# KNOWLEDGE UPDATE INTERVAL
# ============================================================

KNOWLEDGE_UPDATE_INTERVAL = 5000  # 5 detik

# ============================================================
# KNOWLEDGE DEFAULT CATEGORIES
# ============================================================

KNOWLEDGE_CATEGORIES = [
    "All", "Trading", "Market", "Pattern", "Insight",
    "Strategy", "Rule", "Fact",
    "General Knowledge", "Technology", "Finance",
    "Health", "Science", "Education", "Custom"
]

KNOWLEDGE_DEFAULT_CATEGORY = "General Knowledge"

# ============================================================
# KNOWLEDGE ICONS
# ============================================================

KNOWLEDGE_CATEGORY_ICONS = {
    'pattern': '🔍',
    'market': '📊',
    'trading': '📈',
    'insight': '💡',
    'strategy': '🎯',
    'rule': '📋',
    'general': '📄',
    'fact': '✅',
    'tech': '💻',
    'finance': '💰',
    'health': '❤️',
    'science': '🔬',
    'education': '📚',
    'custom': '📌'
}

# ============================================================
# KNOWLEDGE STATUS TEXT
# ============================================================

KNOWLEDGE_STATUS_ONLINE = "✅ Knowledge Base: ONLINE"
KNOWLEDGE_STATUS_OFFLINE = "❌ Knowledge Base: OFFLINE"
KNOWLEDGE_STATUS_LOADING = "⏳ Knowledge Base: LOADING..."

# ============================================================
# KNOWLEDGE UI TEXT
# ============================================================

KNOWLEDGE_QA_PLACEHOLDER = "Tulis pertanyaan di sini... (contoh: apa itu bitcoin?)"
KNOWLEDGE_TEXT_PLACEHOLDER = "Tempel teks pengetahuan di sini..."
KNOWLEDGE_URL_PLACEHOLDER = "https://example.com/article"
KNOWLEDGE_RAW_PLACEHOLDER = "Tempel JSON, CSV, atau data mentah lainnya di sini..."

KNOWLEDGE_URL_STATUS_DEFAULT = "💡 Masukkan URL, sistem akan mengambil konten dan membersihkannya."
KNOWLEDGE_RAW_STATUS_DEFAULT = "💡 Sistem akan mendeteksi JSON, CSV, atau teks secara otomatis."

# ============================================================
# KNOWLEDGE PLACEHOLDER TEXT
# ============================================================

KNOWLEDGE_EMPTY_TEXT = "📭 Belum ada data knowledge.\n\nTambahkan pengetahuan melalui 3 metode di atas,\natau tunggu sistem belajar secara otomatis."

KNOWLEDGE_NO_RESULTS_TEXT = "📭 Tidak ada item yang sesuai dengan filter."

# ============================================================
# KNOWLEDGE SCRAPING
# ============================================================

KNOWLEDGE_FETCH_TIMEOUT = 15  # detik
KNOWLEDGE_MIN_CONTENT_LENGTH = 100
KNOWLEDGE_MAX_CONTENT_LENGTH = 5000
KNOWLEDGE_MAX_SENTENCES = 5
KNOWLEDGE_MIN_SENTENCE_LENGTH = 60

# ============================================================
# KNOWLEDGE SKIP PATTERNS (Boilerplate)
# ============================================================

KNOWLEDGE_SKIP_PATTERNS = [
    # JavaScript & CSS (STRUKTUR, BUKAN KONTEN)
    r'window\.', r'document\.', r'function\s*\(', r'<script', r'</script>',
    r'<style', r'</style>', r'<link', r'meta', r'\.css', r'\.js',
    r'GTM-', r'dataLayer', r'insertBefore', r'addEventListener',
    r'querySelector', r'getElementById', r'console\.log',
    r'const\s+', r'let\s+', r'var\s+', r'setTimeout', r'setInterval',
    r'debugger', r'console\.error', r'console\.warn',
    
    # HTML Structure
    r'<header', r'<footer', r'<nav', r'<aside', r'<main', r'<article',
    r'<section', r'<div\s+class=', r'<div\s+id=', r'<span', r'<p>',
    r'<h1', r'<h2', r'<h3', r'<h4', r'<ul>', r'<ol>', r'<li>',
    r'<table', r'<tr>', r'<td>', r'<th>',
    r'<\/header>', r'<\/footer>', r'<\/nav>', r'<\/aside>',
    r'<\/main>', r'<\/article>', r'<\/section>',
    r'<\/div>', r'<\/span>', r'<\/p>',
    
    # Social Media & Share
    r'Share on', r'Share to', r'Share this', r'Follow us',
    r'Twitter', r'Facebook', r'Instagram', r'LinkedIn', r'YouTube',
    r'Telegram', r'Discord', r'Reddit', r'Medium', r'@\w+', r'#\w+',
    
    # Footer & Legal
    r'©', r'Copyright', r'All rights reserved', r'All Rights Reserved',
    r'Privacy Policy', r'Terms of Service', r'Terms and Conditions',
    r'Cookie Policy', r'Cookies', r'GDPR', r'CCPA',
    r'Disclaimer', r'Legal', r'Compliance', r'Data Protection',
    
    # Subscription & Newsletter
    r'Subscribe', r'Newsletter', r'Sign up', r'Signup',
    r'Join our', r'Get updates', r'Stay informed',
    r'Email Address', r'Enter your email',
    
    # Advertisement
    r'Advertisement', r'Advert', r'Sponsored', r'Promoted',
    r'AdChoices', r'Google Ads', r'Affiliate',
    
    # Navigation & UI
    r'Loading', r'Please wait', r'Back to top', r'Go to top',
    r'Menu', r'Home', r'About', r'Contact', r'Sitemap',
    r'Search', r'Search for', r'Type to search',
    r'Categories', r'Archives', r'Recent Posts',
    
    # Whitepaper Section Headers
    r'^Introduction$', r'^Executive Summary$', r'^Abstract$',
    r'^Background$', r'^Methodology$', r'^Conclusion$',
    r'^References$', r'^Appendix$',
    
    # Numbered/Section Headers
    r'^\d+\.\s+[A-Z]', r'^[A-Z][a-z]+\s+\d+',
    r'^\s*\d+\.\s+', r'^\s*[A-Z]\)\s+', r'^\s*[a-z]\)\s+',
    r'^\s*[IVXLCDM]+\.\s+',
    
    # Email & Phone
    r'[\w\.-]+@[\w\.-]+\.\w+',
    r'\+\d{1,3}\s*\d{3,}',
    r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    
    # URL Shortener & Tracking
    r'bit\.ly/', r'tinyurl\.com/', r'goo\.gl/',
    r'utm_source=', r'utm_medium=', r'utm_campaign=',
    r'ref=', r'source=', r'campaign=',
    
    # Menu Items
    r'Homepage', r'Newsroom', r'Press Release',
    r'Careers', r'Join Us', r'Work With Us',
    r'Events', r'Webinar', r'Podcast', r'Blog', r'Articles',
    r'Insights', r'Resources', r'Help Center', r'FAQ',
    r'Support', r'Contact Us',
    
    # Empty/Single Word Fragments
    r'^\s*[A-Z][a-z]{1,3}\s+$', r'^\s*[0-9]+\s*$',
    r'^\s*[^\w\s]{1,3}\s*$',
]

# ============================================================
# CONFIGURATION LOADED MESSAGE
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print(f"Exchange: {EXCHANGE_NAME}")
    print(f"Pairs: {len(DEFAULT_PAIRS)} pairs")
    print(f"Timeframes: {', '.join(DEFAULT_TIMEFRAMES)}")
    print(f"Scan Interval: {SCAN_INTERVAL_SECONDS}s")
    print(f"Telegram: {'ENABLED' if TELEGRAM_ENABLED else 'DISABLED'}")
    print(f"Trading: {'ENABLED' if TRADING_ENABLED else 'DISABLED'}")
    print(f"Paper Trading: {PAPER_TRADING}")
    print(f"Debug Mode: {DEBUG_MODE}")
    print(f"Log Level: {LOG_LEVEL}")
    print("=" * 60)
    
    issues = validate_config()
    if issues:
        print("\n⚠️ Configuration Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ Configuration validated successfully")
    
    print("=" * 60)
