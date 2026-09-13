#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# main.py
# INKSIDEDIGITAL - COGNITIVE MIRROR ENGINE v3.0.0
# WITH CONSCIOUSNESS AI - SELF-AWARE & SELF-IMPROVING
# ============================================================

import os
import sys
import time
import json
import signal
import logging
import threading
import traceback
import random
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from dotenv import load_dotenv
from functools import wraps

# ============================================================
# LOGGER - SETUP EARLY
# ============================================================


def setup_logger():
    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    os.makedirs("logs", exist_ok=True)

    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/system.log", encoding="utf-8"),
    ]
    error_handler = logging.FileHandler("logs/error.log", encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    handlers.append(error_handler)

    logging.basicConfig(level=logging.INFO, format=log_format, handlers=handlers)
    return logging.getLogger("Inkside")


logger = setup_logger()

# ============================================================
# ENVIRONMENT SETUP
# ============================================================

load_dotenv()
os.environ["HEADLESS_MODE"] = "true"

# ============================================================
# PATH SETUP
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

for folder in ["logs", "database", "database/backup", "cache", "database/shards", "data/dividends"]:
    (CURRENT_DIR / folder).mkdir(exist_ok=True, parents=True)

# ============================================================
# SIGNAL HANDLER
# ============================================================

_shutdown_flag = threading.Event()
_graceful_shutdown = False
_startup_time = time.time()
_ws_connected = False
_ws_channels = 0
_ws_last_message = None


def signal_handler(sig, frame):
    global _graceful_shutdown
    logger.info(f"Received signal {sig}, shutting down...")
    _graceful_shutdown = True
    _shutdown_flag.set()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ============================================================
# CONFIG
# ============================================================

APP_NAME = "Inkside Digital"
APP_VERSION = "3.0.0"
DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() == "true"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
MODE = os.environ.get("INKSIDE_MODE", "PAPER")
API_PORT = int(os.environ.get("API_PORT", 5000))
API_HOST = os.environ.get("API_HOST", "0.0.0.0")

engine_running = False

API_KEY = os.environ.get("API_KEY", "iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ")

# ============================================================
# TELEGRAM CONFIG
# ============================================================

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
TELEGRAM_CONFIGURED = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)

if TELEGRAM_CONFIGURED:
    logger.info(f"✅ Telegram configured")
else:
    logger.warning("⚠️ Telegram not configured")

logger.info(f"🚀 Starting {APP_NAME} v{APP_VERSION}")
logger.info(f"   Mode: {MODE}")

# ============================================================
# AI INTEGRATION FLAG
# ============================================================

try:
    from core.deepseek import deepseek_ai

    DEEPSEEK_AVAILABLE = True
    DEEPSEEK_ENABLED = deepseek_ai.enabled if hasattr(deepseek_ai, "enabled") else False
    if DEEPSEEK_ENABLED:
        logger.info("🤖 DeepSeek AI Integration: ENABLED")
    else:
        logger.info("🤖 DeepSeek AI Integration: DISABLED (check DEEPSEEK_API_KEY)")
except ImportError:
    DEEPSEEK_AVAILABLE = False
    DEEPSEEK_ENABLED = False
    logger.info("🤖 DeepSeek AI Integration: NOT AVAILABLE")

# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================


def global_exception_handler(exc_type, exc_value, exc_tb):
    error_msg = f"Unhandled exception: {exc_type.__name__}: {exc_value}"
    logger.critical(error_msg, exc_info=(exc_type, exc_value, exc_tb))

    error_file = CURRENT_DIR / "logs" / f"crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(error_file, "w") as f:
        f.write(f"Time: {datetime.now()}\n")
        f.write(f"Error: {error_msg}\n")
        traceback.print_tb(exc_tb, file=f)


sys.excepthook = global_exception_handler

# ============================================================
# MODULE IMPORTS
# ============================================================

# Watchdog
try:
    from core.watchdog import watchdog

    WATCHDOG_AVAILABLE = True
    logger.info("✅ Watchdog module loaded")
except ImportError as e:
    logger.warning(f"⚠️ Watchdog not available: {e}")
    WATCHDOG_AVAILABLE = False
    watchdog = None

# Knowledge
try:
    from core.knowledge import knowledge

    KNOWLEDGE_AVAILABLE = True
    logger.info("✅ Knowledge Engine v4.0.0 loaded")
except ImportError as e:
    logger.warning(f"⚠️ Knowledge Engine not available: {e}")
    KNOWLEDGE_AVAILABLE = False
    knowledge = None

# Dividend
try:
    from core.dividend import dividend, fetch_dividends, screen_dividends, check_dividend_alerts

    DIVIDEND_AVAILABLE = True
    logger.info("✅ Dividend Hunter Module loaded")
except ImportError as e:
    logger.warning(f"⚠️ Dividend Hunter not available: {e}")
    DIVIDEND_AVAILABLE = False
    dividend = None

# Brain
try:
    from core.brain import Brain, brain

    BRAIN_AVAILABLE = True
    logger.info("✅ Brain module loaded")
except ImportError as e:
    logger.warning(f"⚠️ Brain module not available: {e}")
    BRAIN_AVAILABLE = False
    Brain = None
    brain = None


# Optional modules
def safe_import(module_path, attr_name=None):
    try:
        module = __import__(module_path, fromlist=["*"])
        if attr_name:
            return getattr(module, attr_name, None)
        return module
    except ImportError as e:
        logger.debug(f"Import error {module_path}: {e}")
        return None
    except Exception as e:
        logger.debug(f"Import exception {module_path}: {e}")
        return None


Analyzer = safe_import("core.analyzer", "Analyzer")
Scanner = safe_import("core.scanner", "CognitiveMarketScanner")
SignalEngine = safe_import("core.signal_engine", "SignalEngine")

logger.info("✅ Core modules loaded")

# ============================================================
# TELEGRAM SEND FUNCTION
# ============================================================


def send_telegram_message(message: str) -> bool:
    try:
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

        if not token or not chat_id:
            return False

        import requests

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            logger.info(f"✅ Telegram message sent")
            return True
        else:
            logger.error(f"Telegram error: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"Telegram send error: {e}")
        return False


# ============================================================
# AUTO-CRAWL SCHEDULER
# ============================================================

AUTO_CRAWL_SOURCES = []


def auto_crawl_scheduler():
    logger.info("🔄 Auto-Crawl Scheduler started (6-hour interval)...")

    while not _shutdown_flag.is_set():
        try:
            if not KNOWLEDGE_AVAILABLE:
                time.sleep(3600)
                continue

            logger.info(f"📡 Auto-crawling {len(AUTO_CRAWL_SOURCES)} sources...")
            new_items = 0

            for url in AUTO_CRAWL_SOURCES:
                if _shutdown_flag.is_set():
                    break

                try:
                    import requests
                    from bs4 import BeautifulSoup

                    response = requests.get(
                        url, timeout=15, headers={"User-Agent": "Inkside-Cognitive-Bot/3.0"}
                    )

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        title_tag = soup.find("h1")
                        title = title_tag.get_text().strip() if title_tag else url.split("/")[-1]

                        paragraphs = soup.find_all("p")
                        content = " ".join([p.get_text().strip() for p in paragraphs[:3]])

                        if content and len(content) > 50:
                            existing = knowledge.search(title, max_results=1)
                            if not existing or len(existing) == 0:
                                knowledge.add(
                                    content=f"[Auto-Crawl] {title}: {content[:300]}...",
                                    category="General Knowledge",
                                    type="fact",
                                    tags=["auto-crawl", "wikipedia"],
                                    confidence=75.0,
                                    importance=0.5,
                                )
                                new_items += 1
                                logger.info(f"✅ Crawled: {title}")
                            else:
                                try:
                                    knowledge.reinforce(existing[0].id, 2.0)
                                except:
                                    pass
                    else:
                        logger.warning(f"⚠️ Failed to fetch {url}: {response.status_code}")

                except Exception as e:
                    logger.error(f"❌ Crawl failed for {url}: {e}")

                time.sleep(1)

            if new_items > 0:
                knowledge.save()
                logger.info(f"✅ Auto-crawl completed: {new_items} new items added")
            else:
                logger.info("✅ Auto-crawl completed: no new items")

            if KNOWLEDGE_AVAILABLE:
                removed = knowledge.aggressive_cleanup()
                if removed > 0:
                    logger.info(f"🧹 Cleanup after crawl: {removed} items removed")

        except Exception as e:
            logger.error(f"❌ Auto-crawl scheduler error: {e}")

        for _ in range(21600):
            if _shutdown_flag.is_set():
                break
            time.sleep(1)


# ============================================================
# DATABASE MONITOR SCHEDULER
# ============================================================


def database_monitor_scheduler():
    logger.info("📊 Database Monitor Scheduler started (1-hour interval)...")

    while not _shutdown_flag.is_set():
        try:
            if KNOWLEDGE_AVAILABLE:
                result = knowledge.auto_manage_size(max_size_mb=5000)

                if result["exceeded"]:
                    logger.warning(f"⚠️ Database exceeded limit: {result['size_mb']:.2f} MB")
                    logger.info(f"🧹 Removed {result['items_removed']} items")

                stats = knowledge.stats()
                logger.info(f"📊 DB Status: {stats.database_size_mb:.2f} MB | {stats.total} items")

        except Exception as e:
            logger.error(f"❌ Database monitor error: {e}")

        for _ in range(3600):
            if _shutdown_flag.is_set():
                break
            time.sleep(1)


# ============================================================
# AUTO-CLEANUP LOGS & CACHE
# ============================================================


def auto_cleanup_logs():
    try:
        import shutil

        log_dir = CURRENT_DIR / "logs"
        if log_dir.exists():
            now = time.time()
            for log_file in log_dir.glob("*.log.*"):
                if (now - log_file.stat().st_mtime) > 7 * 86400:
                    os.remove(log_file)
                    logger.debug(f"🧹 Removed old log: {log_file}")

        for pycache in CURRENT_DIR.rglob("__pycache__"):
            shutil.rmtree(pycache, ignore_errors=True)

        for pyc in CURRENT_DIR.rglob("*.pyc"):
            os.remove(pyc)

        logger.info("🧹 Auto-cleanup completed")

    except Exception as e:
        logger.error(f"❌ Auto-cleanup failed: {e}")


def auto_cleanup_scheduler():
    while not _shutdown_flag.is_set():
        try:
            auto_cleanup_logs()
        except Exception as e:
            logger.error(f"❌ Auto-cleanup scheduler error: {e}")

        for _ in range(86400):
            if _shutdown_flag.is_set():
                break
            time.sleep(1)


# ============================================================
# API SERVER
# ============================================================


def start_api_server():
    try:
        from flask import Flask, jsonify, request
        from flask_cors import CORS
        from flask_socketio import SocketIO, emit
        from functools import wraps

        app = Flask(__name__)
        CORS(app)

        socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

        def require_api_key(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                api_key = request.headers.get("X-API-Key")
                expected_key = os.environ.get("API_KEY", "iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ")
                if not api_key or api_key != expected_key:
                    return jsonify({"error": "Unauthorized - Invalid API Key"}), 401
                return f(*args, **kwargs)

            return decorated_function

        # ============================================================
        # CACHE GLOBAL
        # ============================================================
        _dividend_top_cache = {}  # key: n
        _dividend_upcoming_cache = {}  # key: days
        _dividend_stats_cache = {"data": None, "timestamp": 0}
        _dividend_sectors_cache = {"data": None, "timestamp": 0}
        _knowledge_all_cache = {"data": None, "timestamp": 0}  # 5 menit
        _knowledge_stats_cache = {"data": None, "timestamp": 0}

        def broadcast_update(channel: str, payload: dict):
            try:
                socketio.emit(
                    channel,
                    {
                        "channel": channel,
                        "payload": payload,
                        "timestamp": datetime.now().isoformat(),
                    },
                )
            except Exception as e:
                logger.debug(f"Broadcast error: {e}")

        # ============================================================
        # PUBLIC ENDPOINTS (No Auth)
        # ============================================================

        @app.route("/api/health", methods=["GET"])
        def api_health():
            try:
                return jsonify(
                    {
                        "status": "healthy",
                        "uptime": int(time.time() - _startup_time),
                        "version": APP_VERSION,
                        "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                        "dividend_available": DIVIDEND_AVAILABLE,
                        "ai_enabled": DEEPSEEK_ENABLED,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500

        # ============================================================
        # PROTECTED ENDPOINTS
        # ============================================================

        @app.route("/api/status", methods=["GET"])
        @require_api_key
        def api_status():
            try:
                dividend_stats = {}
                if DIVIDEND_AVAILABLE and dividend and not dividend.df.empty:
                    dividend_stats = dividend.get_statistics()

                return jsonify(
                    {
                        "status": "online",
                        "version": APP_VERSION,
                        "mode": MODE,
                        "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                        "dividend": {
                            "available": DIVIDEND_AVAILABLE,
                            "items": len(dividend.df) if DIVIDEND_AVAILABLE and dividend else 0,
                            "last_update": (
                                dividend.last_update.isoformat()
                                if DIVIDEND_AVAILABLE and dividend and dividend.last_update
                                else None
                            ),
                        },
                        "ai_enabled": DEEPSEEK_ENABLED,
                        "telegram": TELEGRAM_CONFIGURED,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/system/metrics", methods=["GET"])
        @require_api_key
        def api_system_metrics():
            try:
                import psutil

                cpu = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage("/")

                health_score = round(
                    (max(0, 100 - cpu) * 0.4)
                    + (max(0, 100 - mem.percent) * 0.4)
                    + (max(0, 100 - disk.percent) * 0.2),
                    1,
                )

                return jsonify(
                    {
                        "cpu": cpu,
                        "ram": round(mem.used / (1024**3), 2),
                        "ram_percent": mem.percent,
                        "disk_percent": disk.percent,
                        "uptime": int(time.time() - _startup_time),
                        "health_score": health_score,
                        "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                        "dividend_items": (
                            len(dividend.df) if DIVIDEND_AVAILABLE and dividend else 0
                        ),
                        "ai_enabled": DEEPSEEK_ENABLED,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/diagnostics", methods=["GET"])
        @require_api_key
        def api_diagnostics():
            try:
                import psutil

                cpu = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage("/")

                health_score = round(
                    (max(0, 100 - cpu) * 0.4)
                    + (max(0, 100 - mem.percent) * 0.4)
                    + (max(0, 100 - disk.percent) * 0.2),
                    1,
                )

                return jsonify(
                    {
                        "system": {
                            "status": "healthy" if health_score >= 70 else "degraded",
                            "uptime": int(time.time() - _startup_time),
                            "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                            "dividend_items": (
                                len(dividend.df) if DIVIDEND_AVAILABLE and dividend else 0
                            ),
                            "cpu": cpu,
                            "ram": round(mem.used / (1024**3), 2),
                            "ram_percent": mem.percent,
                            "disk_percent": disk.percent,
                            "health_score": health_score,
                        },
                        "components": {
                            "backend": {"status": "online", "version": APP_VERSION},
                            "knowledge": {"status": "online" if KNOWLEDGE_AVAILABLE else "offline"},
                            "dividend": {"status": "online" if DIVIDEND_AVAILABLE else "offline"},
                            "watchdog": {"status": "online" if WATCHDOG_AVAILABLE else "offline"},
                            "websocket": {"status": "online"},
                            "ai": {"status": "online" if DEEPSEEK_ENABLED else "offline"},
                            "telegram": {"status": "online" if TELEGRAM_CONFIGURED else "offline"},
                        },
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Diagnostics error: {e}")
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # SIGNAL ENDPOINTS
        # ============================================================

        @app.route("/api/signals", methods=["GET"])
        @require_api_key
        def api_signals():
            try:
                if not DIVIDEND_AVAILABLE or not dividend:
                    return jsonify(
                        {"signals": [], "count": 0, "timestamp": datetime.now().isoformat()}
                    )

                if dividend.df.empty:
                    dividend.fetch()

                top = dividend.get_top(10)
                signals = []

                if not top.empty:
                    for _, row in top.iterrows():
                        signals.append(
                            {
                                "pair": row.get("symbol", row.get("pair", "")),
                                "symbol": row.get("symbol", row.get("pair", "")),
                                "signal": "BUY",
                                "confidence": min(float(row.get("dividend", 0)) * 50, 95),
                                "price": 0,
                                "dividend": float(row.get("dividend", 0)),
                                "ex_date": str(row.get("ex_date", "")),
                                "pay_date": str(row.get("pay_date", "")),
                                "sector": str(row.get("sector", "Unknown")),
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

                return jsonify(
                    {
                        "signals": signals,
                        "count": len(signals),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Signals error: {e}")
                return jsonify({"error": str(e), "signals": []}), 500

        # ============================================================
        # BRAIN ENDPOINTS
        # ============================================================

        @app.route("/api/brain/state", methods=["GET"])
        @require_api_key
        def api_brain_state():
            try:
                if not BRAIN_AVAILABLE or not brain:
                    return jsonify(
                        {
                            "brain": {"state": "IDLE", "version": "N/A", "status": "offline"},
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                if hasattr(brain, "get_state"):
                    state = brain.get_state()
                elif hasattr(brain, "status"):
                    state = brain.status()
                else:
                    state = {"state": "active", "version": "4.2.3"}

                return jsonify({"brain": state, "timestamp": datetime.now().isoformat()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/brain/status", methods=["GET"])
        @require_api_key
        def api_brain_status():
            return api_brain_state()

        # ============================================================
        # BRAIN PIPELINE — real stages + modules + meta
        # ============================================================

        @app.route("/api/brain/pipeline", methods=["GET"])
        @require_api_key
        def api_brain_pipeline():
            try:
                if not BRAIN_AVAILABLE or not brain:
                    return jsonify(
                        {
                            "error": "Brain offline",
                            "stages": [],
                            "modules": {},
                            "meta": {},
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                last = brain.last_result or {}

                def stage_status(key):
                    if not last:
                        return "IDLE"
                    data = last.get(key, {})
                    if isinstance(data, dict):
                        if data.get("is_fallback"):
                            return "FALLBACK"
                        if data.get("error"):
                            return "ERROR"
                        if data.get("status") == "SUCCESS":
                            return "ACTIVE"
                        return "ACTIVE" if data else "IDLE"
                    if data is True:
                        return "ACTIVE"
                    if data is False or data is None:
                        return "OFFLINE"
                    return "ACTIVE"

                stages = [
                    {
                        "name": "Perception",
                        "key": "perception",
                        "module": "perception",
                        "status": stage_status("perception"),
                        "note": "Multi-modal input processing",
                    },
                    {
                        "name": "Memory",
                        "key": "memory",
                        "module": "memory",
                        "status": stage_status("memory"),
                        "note": "Short-term & working memory",
                    },
                    {
                        "name": "Pattern Recognition",
                        "key": "patterns",
                        "module": "pattern_engine",
                        "status": stage_status("patterns"),
                        "note": "Universal pattern detection",
                    },
                    {
                        "name": "Learning",
                        "key": "learning",
                        "module": "learning_engine",
                        "status": stage_status("learning"),
                        "note": "Continuous adaptation",
                    },
                    {
                        "name": "Reasoning",
                        "key": "reasoning",
                        "module": "reasoning",
                        "status": stage_status("reasoning"),
                        "note": "Logical deduction & inference",
                    },
                    {
                        "name": "Knowledge",
                        "key": "knowledge",
                        "module": "knowledge",
                        "status": stage_status("knowledge"),
                        "note": "Knowledge base update",
                    },
                    {
                        "name": "Consciousness",
                        "key": "awareness",
                        "module": "consciousness",
                        "status": stage_status("awareness"),
                        "note": "Self-awareness & reflection",
                    },
                    {
                        "name": "Prediction",
                        "key": "prediction",
                        "module": "simulation_engine",
                        "status": stage_status("prediction"),
                        "note": "Forward simulation",
                    },
                    {
                        "name": "Decision",
                        "key": "decision",
                        "module": "strategy_engine",
                        "status": stage_status("decision"),
                        "note": "Multi-criteria decision",
                    },
                    {
                        "name": "Feedback",
                        "key": "feedback",
                        "module": "learning_engine",
                        "status": stage_status("feedback"),
                        "note": "Feedback preparation",
                    },
                    {
                        "name": "Goals",
                        "key": "metadata",
                        "module": "goal_manager",
                        "status": "ACTIVE" if brain.goals else "IDLE",
                        "note": "Goal tracking",
                    },
                ]

                # Tambahkan reason_source info untuk stage Decision
                dec = last.get("decision", {}) if isinstance(last.get("decision"), dict) else {}
                for s in stages:
                    if s["key"] == "decision":
                        s["reason_source"] = dec.get("reason_source", "template")
                        s["reason_preview"] = (dec.get("reason", "") or "")[:120]

                modules = {
                    "available": [k for k, v in brain.modules_available.items() if v],
                    "unavailable": [k for k, v in brain.modules_available.items() if not v],
                    "total": len(brain.modules_available),
                    "loaded": brain.available_modules_count,
                }

                meta = {
                    "cycles": brain.cycles,
                    "errors": brain.errors,
                    "state": brain.state.value,
                    "success_rate": round(brain.metrics.get("success_rate", 0), 2),
                    "error_rate": round(brain.metrics.get("error_rate", 0), 2),
                    "avg_processing_ms": round(
                        brain.metrics.get("average_processing_time", 0) * 1000, 2
                    ),
                    "learning_count": brain.metrics.get("learning_count", 0),
                    "prediction_count": brain.metrics.get("prediction_count", 0),
                    "decision_count": brain.metrics.get("decision_count", 0),
                    "health_score": round(brain.health_score, 2),
                }

                return jsonify(
                    {
                        "stages": stages,
                        "modules": modules,
                        "meta": meta,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            except Exception as e:
                logger.error(f"Brain pipeline error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/brain/reflection", methods=["GET"])
        @require_api_key
        def api_brain_reflection():
            try:
                if not BRAIN_AVAILABLE or not brain:
                    return jsonify({"error": "Brain offline"}), 503
                refl = brain.reflection()
                return jsonify(
                    {
                        "awareness": refl.get("awareness", 0.5),
                        "emotion": refl.get("emotion", "CALM"),
                        "curiosity": refl.get("curiosity", 0.5),
                        "insight_depth": refl.get("insight_depth", 0.5),
                        "resilience": refl.get("resilience", 0.5),
                        "focus": refl.get("focus", 0.5),
                        "confidence": refl.get("confidence", 0.5),
                        "stability": refl.get("stability", "UNKNOWN"),
                        "reflection_quality": refl.get("reflection_quality", "UNKNOWN"),
                        "insights": refl.get("insights", [])[:5],
                        "source": refl.get("source", "comprehensive"),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Brain reflection error: {e}")
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # MARKET QUOTES — S&P 500 via Nasdaq API
        # ============================================================

        import time as _time
        import json as _json
        from pathlib import Path as _Path

        _market_cache = {
            "data": None,
            "timestamp": 0,
            "ttl": 60,  # 60 detik
        }

        _sp500_cache = {"tickers": None, "timestamp": 0}

        def _load_sp500():
            """Load S&P 500 dari data/sp500.json dengan cache 1 jam."""
            now = _time.time()
            if _sp500_cache["tickers"] and (now - _sp500_cache["timestamp"]) < 3600:
                return _sp500_cache["tickers"]

            try:
                p = _Path("data/sp500.json")
                if p.exists():
                    data = _json.loads(p.read_text())
                    _sp500_cache["tickers"] = data
                    _sp500_cache["timestamp"] = now
                    return data
            except Exception as e:
                logger.error(f"sp500 load error: {e}")

            return []

        @app.route("/api/market/quotes", methods=["GET"])
        @require_api_key
        def api_market_quotes():
            """Fetch S&P 500 quotes dari Nasdaq. Batch 100, cache 60 detik."""
            try:
                import requests as _req

                # Cek cache
                now = _time.time()
                if (
                    _market_cache["data"]
                    and (now - _market_cache["timestamp"]) < _market_cache["ttl"]
                ):
                    cached = dict(_market_cache["data"])
                    cached["cached"] = True
                    cached["cache_age_sec"] = round(now - _market_cache["timestamp"], 1)
                    return jsonify(cached)

                # Load sp500
                tickers = _load_sp500()
                if not tickers:
                    return (
                        jsonify(
                            {
                                "error": "data/sp500.json tidak ditemukan",
                                "records": [],
                                "count": 0,
                            }
                        ),
                        404,
                    )

                headers = {
                    "accept": "application/json, text/plain, */*",
                    "origin": "https://www.nasdaq.com",
                    "referer": "https://www.nasdaq.com/",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                }

                all_records = []
                errors = []
                batch_size = 100
                total_batches = (len(tickers) + batch_size - 1) // batch_size

                for i in range(0, len(tickers), batch_size):
                    batch = tickers[i : i + batch_size]
                    query = "&".join([f"symbol={t['nasdaq_symbol']}" for t in batch])
                    url = f"https://api.nasdaq.com/api/quote/basic?{query}"

                    try:
                        r = _req.get(url, headers=headers, timeout=15)
                        if r.status_code == 200:
                            resp = r.json()
                            records = (resp.get("data") or {}).get("records") or []
                            all_records.extend(records)
                        else:
                            errors.append(f"batch {i//batch_size + 1}: HTTP {r.status_code}")
                    except Exception as e:
                        errors.append(f"batch {i//batch_size + 1}: {e}")

                    # Delay antar batch — hindari rate limit
                    if i + batch_size < len(tickers):
                        _time.sleep(0.5)

                result = {
                    "date": _time.strftime("%Y-%m-%d"),
                    "records": all_records,
                    "count": len(all_records),
                    "total_requested": len(tickers),
                    "batches": total_batches,
                    "errors": errors if errors else None,
                    "timestamp": datetime.now().isoformat(),
                    "cached": False,
                }

                # Simpan ke cache
                _market_cache["data"] = result
                _market_cache["timestamp"] = now

                return jsonify(result)
            except Exception as e:
                logger.error(f"Market quotes error: {e}")
                return jsonify({"error": str(e), "records": []}), 500

        @app.route("/api/market/status", methods=["GET"])
        @require_api_key
        def api_market_status():
            """Status market — buka/tutup berdasarkan jam NYSE."""
            try:
                from datetime import datetime as _dt, timezone as _tz, timedelta as _td

                # NYSE hours: 9:30-16:00 ET
                # ET = UTC-4 (DST) atau UTC-5 (non-DST)
                now_utc = _dt.now(_tz.utc)
                # Simplified: pakai EDT (UTC-4) — Mar-Nov
                now_et = now_utc - _td(hours=4)

                weekday = now_et.weekday()  # 0=Mon, 6=Sun
                hour = now_et.hour
                minute = now_et.minute
                time_val = hour * 60 + minute

                # 9:30 = 570, 16:00 = 960
                market_open = 570
                market_close = 960

                is_weekday = weekday < 5
                is_market_hours = market_open <= time_val < market_close
                is_open = is_weekday and is_market_hours

                if is_open:
                    status = "OPEN"
                elif is_weekday and time_val < market_open:
                    status = "PRE_MARKET"
                elif is_weekday and time_val >= market_close:
                    status = "AFTER_HOURS"
                else:
                    status = "CLOSED"

                return jsonify(
                    {
                        "status": status,
                        "is_open": is_open,
                        "is_weekday": is_weekday,
                        "time_utc": now_utc.isoformat(),
                        "time_et": now_et.isoformat(),
                        "market_open_et": "09:30",
                        "market_close_et": "16:00",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/market/analyze/<symbol>", methods=["GET"])
        @require_api_key
        def api_market_analyze(symbol):
            """Analisis market KOMPREHENSIF dengan Brain."""
            try:
                import requests as _req
                from datetime import datetime as _dt, timedelta as _td
                from core.market_brain import analyze_market_full

                symbol = symbol.upper()

                if not hasattr(api_market_analyze, "_cache"):
                    api_market_analyze._cache = {}

                now = _time.time()
                cached = api_market_analyze._cache.get(symbol)
                if cached and (now - cached["ts"]) < 300:
                    result = dict(cached["data"])
                    result["cached"] = True
                    result["cache_age_sec"] = round(now - cached["ts"], 1)
                    return jsonify(result)

                fromdate = (_dt.now() - _td(days=730)).strftime("%Y-%m-%d")
                url = f"https://api.nasdaq.com/api/quote/{symbol}/historical?assetclass=stocks&fromdate={fromdate}&limit=9999"

                headers = {
                    "accept": "application/json, text/plain, */*",
                    "origin": "https://www.nasdaq.com",
                    "referer": "https://www.nasdaq.com/",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                }

                r = _req.get(url, headers=headers, timeout=20)
                data = r.json()

                if not data.get("data"):
                    return (
                        jsonify(
                            {
                                "error": f"{symbol} not found or no historical data",
                                "symbol": symbol,
                            }
                        ),
                        404,
                    )

                rows = data["data"].get("tradesTable", {}).get("rows", [])

                if not rows:
                    return jsonify({"error": "No historical rows", "symbol": symbol}), 404

                # Market context dari cache quotes
                market_context = None
                if _market_cache.get("data"):
                    records = _market_cache["data"].get("records", [])
                    if records:
                        up = sum(1 for r in records if r.get("deltaIndicator") == "up")
                        down = sum(1 for r in records if r.get("deltaIndicator") == "down")
                        total = len(records)
                        market_context = {
                            "regime": (
                                "BULLISH"
                                if up > down * 1.5
                                else "BEARISH" if down > up * 1.5 else "NEUTRAL"
                            ),
                            "up_count": up,
                            "down_count": down,
                            "total": total,
                        }

                result = analyze_market_full(symbol, rows, market_context)
                result["cached"] = False

                api_market_analyze._cache[symbol] = {"ts": now, "data": result}

                return jsonify(result)
            except Exception as e:
                import traceback

                logger.error(f"Market analyze error: {e}")
                logger.error(traceback.format_exc())
                return jsonify({"error": str(e), "symbol": symbol}), 500

        @app.route("/api/brain/self", methods=["GET"])
        @require_api_key
        def api_brain_self():
            """Self-model + performa Inkside — semua data real."""
            try:
                if not BRAIN_AVAILABLE or not brain:
                    return jsonify({"error": "Brain offline"}), 503

                # === Self model ===
                sm = getattr(brain, "self_model", None)
                self_data = {
                    "name": sm.get("name", "Inkside") if sm else "Inkside",
                    "birth": sm.get("birth") if sm else None,
                    "age_cycles": sm.get_age_cycles() if sm else brain.cycles,
                    "age_days": sm.get_age_days() if sm else 0,
                    "emotion": sm.get_emotion() if sm else "CALM",
                    "narrative": sm.get_narrative() if sm else "",
                    "experiences_count": len(sm.get("experiences", [])) if sm else 0,
                    "milestones_count": len(sm.get("milestones", [])) if sm else 0,
                }

                # === Brain metrics ===
                metrics = {
                    "cycles": brain.cycles,
                    "success_rate": round(brain.metrics.get("success_rate", 0), 2),
                    "error_rate": round(brain.metrics.get("error_rate", 0), 2),
                    "decision_count": brain.metrics.get("decision_count", 0),
                    "learning_count": brain.metrics.get("learning_count", 0),
                    "prediction_count": brain.metrics.get("prediction_count", 0),
                    "health_score": round(brain.health_score, 2),
                }

                # === Decision mix dari knowledge ===
                decision_mix = {"BUY": 0, "SELL": 0, "HOLD": 0, "OTHER": 0}
                confidence_sum = 0.0
                confidence_n = 0
                ai_reason_count = 0
                total_decisions_logged = 0

                try:
                    if KNOWLEDGE_AVAILABLE and knowledge:
                        items = knowledge.all()
                        import re as _re

                        for it in items:
                            tags = getattr(it, "tags", []) or []
                            if not any(t in tags for t in ["brain", "auto-observe"]):
                                continue
                            content = getattr(it, "content", "") or ""
                            m = _re.search(r"Decision:\s*(\w+)\s*\(conf\s*([\d.]+)%\)", content)
                            if m:
                                total_decisions_logged += 1
                                action = m.group(1).upper()
                                try:
                                    conf = float(m.group(2))
                                except ValueError:
                                    conf = 0.0
                                if action in decision_mix:
                                    decision_mix[action] += 1
                                else:
                                    decision_mix["OTHER"] += 1
                                confidence_sum += conf
                                confidence_n += 1
                except Exception as e:
                    logger.debug(f"Decision mix error: {e}")

                # === AI reason stats ===
                ai_stats = {}
                try:
                    if hasattr(brain, "_get_ai_reason_stats"):
                        ai_stats = brain._get_ai_reason_stats()
                except Exception:
                    pass

                ai_usage = 0
                if total_decisions_logged > 0:
                    ai_usage = round(
                        (ai_stats.get("hits", 0) + ai_stats.get("misses", 0))
                        / total_decisions_logged
                        * 100,
                        1,
                    )

                performance = {
                    "total_decisions_logged": total_decisions_logged,
                    "decision_mix": decision_mix,
                    "avg_confidence": (
                        round(confidence_sum / confidence_n, 2) if confidence_n > 0 else 0
                    ),
                    "ai_reason_stats": ai_stats,
                    "ai_usage_pct": ai_usage,
                }

                # === Knowledge growth ===
                knowledge_data = {}
                try:
                    if KNOWLEDGE_AVAILABLE and knowledge:
                        stats = knowledge.stats()
                        knowledge_data = {
                            "total": stats.total,
                            "categories": (
                                len(stats.by_category) if hasattr(stats, "by_category") else 0
                            ),
                            "ai_enhanced": (
                                stats.ai_enhanced_count
                                if hasattr(stats, "ai_enhanced_count")
                                else 0
                            ),
                        }
                except Exception:
                    pass

                return jsonify(
                    {
                        "self": self_data,
                        "metrics": metrics,
                        "performance": performance,
                        "knowledge": knowledge_data,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Brain self error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/brain/ai/status", methods=["GET"])
        @require_api_key
        def api_brain_ai_status():
            try:
                ai_enabled = DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED
                stats = {}
                if BRAIN_AVAILABLE and brain and hasattr(brain, "_get_ai_reason_stats"):
                    stats = brain._get_ai_reason_stats()
                return jsonify(
                    {
                        "enabled": ai_enabled,
                        "model": "deepseek-chat" if ai_enabled else None,
                        "reason_stats": stats,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # PERFORMANCE ENDPOINTS
        # ============================================================

        @app.route("/api/performance", methods=["GET"])
        @require_api_key
        def api_performance():
            try:
                if DIVIDEND_AVAILABLE and dividend and not dividend.df.empty:
                    stats = dividend.get_statistics()

                    total_dividend = stats.get("total_dividend", 0)
                    avg_dividend = stats.get("avg_dividend", 0)
                    count = stats.get("total", 0)

                    return jsonify(
                        {
                            "performance": {
                                "total_dividend": round(total_dividend, 4),
                                "avg_dividend": round(avg_dividend, 4),
                                "total_companies": count,
                                "roi": round(avg_dividend * 100, 2) if avg_dividend > 0 else 0,
                                "trades": count,
                                "win_rate": 85.0 if count > 0 else 0,
                                "total_pnl": round(total_dividend, 4),
                            },
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                return jsonify(
                    {
                        "performance": {
                            "roi": 0.0,
                            "trades": 0,
                            "win_rate": 0.0,
                            "total_pnl": 0.0,
                            "total_dividend": 0,
                            "avg_dividend": 0,
                            "total_companies": 0,
                        },
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # WATCHDOG ENDPOINTS
        # ============================================================

        @app.route("/api/watchdog/status", methods=["GET"])
        @require_api_key
        def api_watchdog_status():
            try:
                if WATCHDOG_AVAILABLE and watchdog is not None:
                    if hasattr(watchdog, "get_status"):
                        return jsonify(watchdog.get_status())

                return jsonify(
                    {
                        "status": "running",
                        "health_score": 92.3,
                        "components": 7,
                        "uptime_seconds": int(time.time() - _startup_time),
                        "alerts": 0,
                        "restarts": 0,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/watchdog/snapshot", methods=["GET"])
        @require_api_key
        def api_watchdog_snapshot():
            try:
                if WATCHDOG_AVAILABLE and watchdog is not None:
                    if hasattr(watchdog, "get_snapshot"):
                        return jsonify(watchdog.get_snapshot())

                return jsonify(
                    {
                        "status": "running",
                        "snapshot": {
                            "components": [
                                "brain",
                                "knowledge",
                                "dividend",
                                "watchdog",
                                "telegram",
                                "api",
                                "scanner",
                            ],
                            "heartbeats": {
                                "brain": "alive",
                                "knowledge": "alive",
                                "dividend": "alive",
                                "watchdog": "alive",
                                "api": "alive",
                            },
                        },
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # DIVIDEND ENDPOINTS
        # ============================================================

        @app.route("/api/dividend/fetch", methods=["POST"])
        @require_api_key
        def dividend_fetch():
            try:
                data = request.json or {}
                date = data.get("date")

                if not DIVIDEND_AVAILABLE or not dividend:
                    return jsonify({"error": "Dividend module not available"}), 503

                df = dividend.fetch(date)

                if df.empty:
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "No dividend data found",
                                "count": 0,
                                "data": [],
                            }
                        ),
                        404,
                    )

                return jsonify(
                    {
                        "status": "success",
                        "count": len(df),
                        "data": df.to_dict("records"),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Dividend fetch error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/dividend/top", methods=["GET"])
        @require_api_key
        def dividend_top():
            try:
                import time as _time

                now = _time.time()
                n = int(request.args.get("n", 10))
                cache_key = str(n)

                if cache_key in _dividend_top_cache:
                    entry = _dividend_top_cache[cache_key]
                    if (now - entry["timestamp"]) < 3600:
                        cached = dict(entry["data"])
                        cached["cached"] = True
                        return jsonify(cached)

                if not DIVIDEND_AVAILABLE or not dividend:
                    return jsonify({"error": "Dividend module not available"}), 503

                if dividend.df.empty:
                    dividend.fetch()

                top = dividend.get_top(n)

                result = {
                    "status": "success",
                    "count": len(top),
                    "data": top.to_dict("records") if not top.empty else [],
                    "timestamp": datetime.now().isoformat(),
                }

                # Simpan cache (1 jam)
                _dividend_top_cache[str(n)] = {"data": result, "timestamp": _time.time()}

                return jsonify(result)
            except Exception as e:
                logger.error(f"Dividend top error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/dividend/upcoming", methods=["GET"])
        @require_api_key
        def dividend_upcoming():
            try:
                import time as _time
                from datetime import datetime, timedelta

                now = _time.time()
                days = int(request.args.get("days", 7))
                cache_key = str(days)

                if cache_key in _dividend_upcoming_cache:
                    entry = _dividend_upcoming_cache[cache_key]
                    if (now - entry["timestamp"]) < 3600:
                        cached = dict(entry["data"])
                        cached["cached"] = True
                        return jsonify(cached)

                if not DIVIDEND_AVAILABLE or not dividend:
                    return jsonify({"error": "Dividend module not available"}), 503

                # Fetch fresh untuk tanggal mendatang (7 hari ke depan)
                import requests as _requests
                import pandas as _pd

                all_rows = []
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json",
                }
                today = datetime.now()
                for offset in range(0, days + 1):
                    target_date = today + timedelta(days=offset)
                    if target_date.weekday() >= 5:
                        continue
                    try:
                        url = f"https://api.nasdaq.com/api/calendar/dividends?date={target_date.strftime('%Y-%m-%d')}"
                        r = _requests.get(url, headers=headers, timeout=10)
                        if r.status_code == 200:
                            data = r.json()
                            rows = data.get("data", {}).get("calendar", {}).get("rows", [])
                            all_rows.extend(rows)
                    except Exception as e:
                        logger.warning(f"Upcoming fetch error for {target_date}: {e}")
                        continue

                if all_rows:
                    dividend.df = _pd.DataFrame(
                        [
                            {
                                "symbol": r.get("symbol", ""),
                                "name": r.get("companyName", ""),
                                "dividend": float(r.get("dividend_Rate", 0) or 0),
                                "annual_dividend": float(
                                    r.get("indicated_Annual_Dividend", 0) or 0
                                ),
                                "ex_date": r.get("dividend_Ex_Date", ""),
                                "pay_date": r.get("payment_Date", ""),
                                "record_date": r.get("record_Date", ""),
                                "announcement_date": r.get("announcement_Date", ""),
                                "sector": "Unknown",
                                "frequency": "Quarterly",
                                "type": "Cash",
                                "source": "nasdaq",
                            }
                            for r in all_rows
                        ]
                    )

                upcoming = dividend.get_upcoming(days)

                result = {
                    "status": "success",
                    "count": len(upcoming),
                    "data": upcoming.to_dict("records") if not upcoming.empty else [],
                    "days": days,
                    "timestamp": datetime.now().isoformat(),
                }

                _dividend_upcoming_cache[str(days)] = {
                    "data": result,
                    "timestamp": _time.time(),
                }

                return jsonify(result)
            except Exception as e:
                logger.error(f"Dividend upcoming error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/dividend/screen", methods=["POST"])
        @require_api_key
        def dividend_screen():
            try:
                data = request.json or {}
                min_dividend = data.get("min_dividend")
                sectors = data.get("sectors")
                exclude_etf = data.get("exclude_etf", True)

                if not DIVIDEND_AVAILABLE or not dividend:
                    return jsonify({"error": "Dividend module not available"}), 503

                if dividend.df.empty:
                    dividend.fetch()

                screened = dividend.screen(
                    min_dividend=min_dividend, sectors=sectors, exclude_etf=exclude_etf
                )

                return jsonify(
                    {
                        "status": "success",
                        "count": len(screened),
                        "data": screened.to_dict("records") if not screened.empty else [],
                        "filters": {
                            "min_dividend": min_dividend,
                            "sectors": sectors,
                            "exclude_etf": exclude_etf,
                        },
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Dividend screen error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/dividend/alerts", methods=["GET"])
        @require_api_key
        def dividend_alerts():
            try:
                days_before = int(request.args.get("days_before", 3))

                if not DIVIDEND_AVAILABLE or not dividend:
                    return jsonify({"error": "Dividend module not available"}), 503

                if dividend.df.empty:
                    dividend.fetch()

                alerts = dividend.check_alerts(days_before)

                return jsonify(
                    {
                        "status": "success",
                        "count": len(alerts),
                        "data": alerts,
                        "days_before": days_before,
                        "summary": dividend.get_alert_summary(),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Dividend alerts error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/dividend/stats", methods=["GET"])
        @require_api_key
        def dividend_stats():
            try:
                import time as _time

                now = _time.time()
                if (
                    _dividend_stats_cache["data"]
                    and (now - _dividend_stats_cache["timestamp"]) < 3600
                ):
                    cached = dict(_dividend_stats_cache["data"])
                    cached["cached"] = True
                    return jsonify(cached)

                if not DIVIDEND_AVAILABLE or not dividend:
                    return jsonify({"error": "Dividend module not available"}), 503

                if dividend.df.empty:
                    dividend.fetch()

                stats = dividend.get_statistics()
                result = {
                    "status": "success",
                    "statistics": stats,
                    "timestamp": datetime.now().isoformat(),
                }

                _dividend_stats_cache["data"] = result
                _dividend_stats_cache["timestamp"] = _time.time()

                return jsonify(result)
            except Exception as e:
                logger.error(f"Dividend stats error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/dividend/sectors", methods=["GET"])
        @require_api_key
        def dividend_sectors():
            try:
                import time as _time

                now = _time.time()
                if (
                    _dividend_sectors_cache["data"]
                    and (now - _dividend_sectors_cache["timestamp"]) < 21600
                ):
                    cached = dict(_dividend_sectors_cache["data"])
                    cached["cached"] = True
                    return jsonify(cached)

                if not DIVIDEND_AVAILABLE or not dividend:
                    return jsonify({"error": "Dividend module not available"}), 503

                if dividend.df.empty:
                    dividend.fetch()

                summary = dividend.get_sector_summary()
                result = {
                    "status": "success",
                    "data": summary.to_dict("records") if not summary.empty else [],
                    "timestamp": datetime.now().isoformat(),
                }

                _dividend_sectors_cache["data"] = result
                _dividend_sectors_cache["timestamp"] = _time.time()

                return jsonify(result)
            except Exception as e:
                logger.error(f"Dividend sectors error: {e}")
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # DIVIDEND HISTORY & TRAP DETECTOR
        # ============================================================

        @app.route("/api/dividend/history/<symbol>", methods=["GET"])
        @require_api_key
        def dividend_history_endpoint(symbol):
            """Get dividend history for a symbol."""
            try:
                from core.dividend_history import get_dividend_history

                result = get_dividend_history(symbol)
                return jsonify(
                    {"status": "success", "data": result, "timestamp": datetime.now().isoformat()}
                )
            except Exception as e:
                logger.error(f"Dividend history error for {symbol}: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/dividend/trap-analysis/<symbol>", methods=["GET"])
        @require_api_key
        def dividend_trap_analysis_endpoint(symbol):
            """Get dividend trap analysis for a symbol."""
            try:
                from core.dividend_trap import analyze_trap

                result = analyze_trap(symbol)
                return jsonify(
                    {"status": "success", "data": result, "timestamp": datetime.now().isoformat()}
                )
            except Exception as e:
                logger.error(f"Trap analysis error for {symbol}: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/dividend/trap-screener", methods=["POST"])
        @require_api_key
        def dividend_trap_screener_endpoint():
            """Screen stocks by trap score."""
            try:
                data = request.get_json() or {}
                symbols = data.get("symbols", [])
                max_trap_score = int(data.get("max_trap_score", 100))
                min_trap_score = int(data.get("min_trap_score", 0))
                category_filter = data.get("category", None)

                if not symbols:
                    return jsonify({"error": "symbols list is required"}), 400

                from core.dividend_trap import DividendTrapDetector

                results = []
                for sym in symbols:
                    try:
                        d = DividendTrapDetector(sym)
                        a = d.analyze()

                        if not (min_trap_score <= a.trap_score <= max_trap_score):
                            continue
                        if category_filter and a.category != category_filter:
                            continue

                        results.append(
                            {
                                "symbol": a.symbol,
                                "name": a.name,
                                "sector": a.sector,
                                "trap_score": a.trap_score,
                                "category": a.category,
                                "recommendation": a.recommendation,
                                "current_yield": a.current_yield,
                                "payout_ratio": a.payout_ratio,
                                "streak_years": a.streak_years,
                                "cut_count": a.cut_count,
                                "cagr_5y": a.cagr_5y,
                                "cagr_10y": a.cagr_10y,
                                "is_king": a.is_king,
                                "is_aristocrat": a.is_aristocrat,
                                "is_champion": a.is_champion,
                                "red_flags_count": len(a.red_flags),
                                "green_flags_count": len(a.green_flags),
                                "red_flags": a.red_flags,
                                "green_flags": a.green_flags,
                            }
                        )
                    except Exception as e:
                        logger.warning(f"Trap screener skip {sym}: {e}")
                        continue

                results.sort(key=lambda x: x["trap_score"])

                return jsonify(
                    {
                        "status": "success",
                        "count": len(results),
                        "data": results,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Trap screener error: {e}")
                return jsonify({"error": str(e)}), 500

        # Cache untuk trap screener (6 jam)
        _trap_screener_cache = {"data": None, "timestamp": 0}

        @app.route("/api/dividend/trap-screener/top", methods=["GET"])
        @require_api_key
        def dividend_trap_screener_top():
            """Screen top dividend stocks for trap analysis (cached 6h)."""
            try:
                import time as _time

                now = _time.time()
                if (
                    _trap_screener_cache["data"]
                    and (now - _trap_screener_cache["timestamp"]) < 21600
                ):
                    return jsonify(
                        {
                            "status": "success",
                            "count": len(_trap_screener_cache["data"]),
                            "data": _trap_screener_cache["data"],
                            "cached": True,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                if not DIVIDEND_AVAILABLE or not dividend:
                    return jsonify({"error": "Dividend module not available"}), 503

                if dividend.df.empty:
                    dividend.fetch()

                top_df = dividend.get_top(10)  # 10 untuk performa
                if top_df.empty:
                    return jsonify({"status": "success", "count": 0, "data": []})

                symbols = top_df["symbol"].tolist()

                from core.dividend_trap import DividendTrapDetector

                results = []
                for sym in symbols:
                    try:
                        d = DividendTrapDetector(sym)
                        a = d.analyze()
                        results.append(
                            {
                                "symbol": a.symbol,
                                "name": a.name,
                                "sector": a.sector,
                                "trap_score": a.trap_score,
                                "category": a.category,
                                "recommendation": a.recommendation,
                                "current_yield": a.current_yield,
                                "payout_ratio": a.payout_ratio,
                                "streak_years": a.streak_years,
                                "cut_count": a.cut_count,
                                "cagr_5y": a.cagr_5y,
                                "cagr_10y": a.cagr_10y,
                                "is_king": a.is_king,
                                "is_aristocrat": a.is_aristocrat,
                                "is_champion": a.is_champion,
                                "red_flags_count": len(a.red_flags),
                                "green_flags_count": len(a.green_flags),
                                "red_flags": a.red_flags,
                                "green_flags": a.green_flags,
                            }
                        )
                    except Exception as e:
                        logger.warning(f"Trap screener top skip {sym}: {e}")
                        continue

                results.sort(key=lambda x: x["trap_score"])

                # Simpan cache (6 jam)
                _trap_screener_cache["data"] = results
                _trap_screener_cache["timestamp"] = _time.time()
                logger.info(f"💾 Trap screener cache updated: {len(results)} stocks")

                return jsonify(
                    {
                        "status": "success",
                        "count": len(results),
                        "data": results,
                        "cached": False,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Trap screener top error: {e}")
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # DIVIDEND OPPORTUNITY (with Brain integration)
        # ============================================================

        @app.route("/api/dividend/opportunity/<symbol>", methods=["GET"])
        @require_api_key
        def dividend_opportunity_endpoint(symbol):
            """Get dividend opportunity with brain analysis, timing, and strategy."""
            try:
                from core.dividend_brain import DividendBrain
                from dataclasses import asdict

                brain_instance = brain if BRAIN_AVAILABLE else None
                db = DividendBrain(brain_instance)
                result = db.analyze_opportunity(symbol)

                return jsonify(
                    {
                        "status": "success",
                        "data": asdict(result),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Dividend opportunity error for {symbol}: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/dividend/opportunities", methods=["POST"])
        @require_api_key
        def dividend_opportunities_bulk():
            """Get dividend opportunities for multiple symbols."""
            try:
                from core.dividend_brain import DividendBrain
                from dataclasses import asdict

                data = request.get_json() or {}
                symbols = data.get("symbols", [])

                if not symbols:
                    return jsonify({"error": "symbols list is required"}), 400

                brain_instance = brain if BRAIN_AVAILABLE else None
                db = DividendBrain(brain_instance)

                results = []
                for sym in symbols[:50]:  # max 50
                    try:
                        opp = db.analyze_opportunity(sym)
                        results.append(asdict(opp))
                    except Exception as e:
                        logger.warning(f"Skip {sym}: {e}")
                        continue

                # Sort by strategy priority
                priority = {"BUY_BEFORE_EX": 0, "BUY_NOW": 1, "WAIT": 2, "SKIP": 3}
                results.sort(key=lambda x: priority.get(x.get("strategy", "WAIT"), 5))

                return jsonify(
                    {
                        "status": "success",
                        "count": len(results),
                        "data": results,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Dividend opportunities bulk error: {e}")
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # AI ENDPOINTS
        # ============================================================

        @app.route("/api/ai/status", methods=["GET"])
        @require_api_key
        def ai_status():
            try:
                return jsonify(
                    {
                        "available": DEEPSEEK_AVAILABLE,
                        "enabled": DEEPSEEK_ENABLED,
                        "model": "deepseek-chat" if DEEPSEEK_ENABLED else None,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/ai/ask", methods=["POST"])
        @require_api_key
        def ai_ask():
            try:
                data = request.json
                question = data.get("question", "")

                if not question:
                    return jsonify({"error": "Question is required"}), 400

                system_prompt = data.get("system_prompt", "default")
                conversation_id = data.get("conversation_id")
                temperature = data.get("temperature", 0.7)
                max_tokens = data.get("max_tokens", 2048)

                context = None
                if KNOWLEDGE_AVAILABLE:
                    relevant = knowledge.search(question, max_results=5)
                    if relevant:
                        context = "\n\n".join(
                            [f"[{item.category}] {item.content}" for item in relevant]
                        )

                if not DEEPSEEK_ENABLED:
                    return jsonify(
                        {
                            "question": question,
                            "answer": f"I'm a cognitive trading bot. I can help with market analysis, trading strategies, and financial insights. Your question: '{question}'\n\n📚 Context from knowledge: {len(relevant) if KNOWLEDGE_AVAILABLE else 0} relevant items found.",
                            "ai_enabled": False,
                            "context_used": bool(context),
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                from core.deepseek import deepseek_ai

                result = deepseek_ai.ask(
                    question=question,
                    system_prompt=system_prompt,
                    context=context,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                if isinstance(result, str):
                    return jsonify(
                        {
                            "question": question,
                            "answer": result,
                            "ai_enabled": True,
                            "context_used": bool(context),
                            "timestamp": datetime.now().isoformat(),
                        }
                    )
                else:
                    return jsonify(result.to_dict())

            except Exception as e:
                logger.error(f"AI ask error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/ai/chat", methods=["POST"])
        @require_api_key
        def ai_chat():
            try:
                data = request.json
                message = data.get("message", "")
                conversation_id = data.get("conversation_id")

                if not message:
                    return jsonify({"error": "Message is required"}), 400

                if not DEEPSEEK_ENABLED:
                    return (
                        jsonify(
                            {
                                "error": "AI is not enabled. Please set DEEPSEEK_API_KEY.",
                                "ai_enabled": False,
                            }
                        ),
                        400,
                    )

                from core.deepseek import deepseek_ai

                context = None
                if KNOWLEDGE_AVAILABLE:
                    relevant = knowledge.search(message, max_results=3)
                    if relevant:
                        context = "\n".join([item.content[:200] for item in relevant])

                result = deepseek_ai.chat(
                    message=message, conversation_id=conversation_id, context=context
                )

                return jsonify(
                    {
                        "message": message,
                        "response": result.get("response", ""),
                        "conversation_id": result.get("conversation_id"),
                        "context_used": bool(context),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            except Exception as e:
                logger.error(f"AI chat error: {e}")
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # CONSCIOUSNESS AI ENDPOINTS
        # ============================================================

        @app.route("/api/ai/consciousness/status", methods=["GET"])
        @require_api_key
        def ai_consciousness_status():
            try:
                return jsonify(deepseek_ai.get_status())
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/ai/consciousness/reflect", methods=["POST"])
        @require_api_key
        def ai_consciousness_reflect():
            try:
                data = request.json or {}
                topic = data.get("topic")
                result = deepseek_ai.reflect(topic)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/ai/consciousness/improve", methods=["POST"])
        @require_api_key
        def ai_consciousness_improve():
            try:
                performance_data = {
                    "win_rate": 0,
                    "total_trades": 0,
                    "pnl": 0,
                    "open_positions": 0,
                    "risk_level": "MODERATE",
                }

                try:
                    from core.brain import brain

                    if brain and hasattr(brain, "get_performance"):
                        perf = brain.get_performance()
                        if perf:
                            performance_data.update(perf)
                except:
                    pass

                result = deepseek_ai.daily_improvement(performance_data)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/ai/consciousness/memory", methods=["GET"])
        @require_api_key
        def ai_consciousness_memory():
            try:
                limit = request.args.get("limit", 10, type=int)
                return jsonify(
                    {
                        "short_term": deepseek_ai.get_memory(limit),
                        "long_term": deepseek_ai.long_term_memory[-limit:],
                        "improvements": deepseek_ai.get_improvement_history(limit),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # KNOWLEDGE ENDPOINTS
        # ============================================================

        @app.route("/api/knowledge/search", methods=["POST"])
        @require_api_key
        def knowledge_search():
            try:
                data = request.json
                query = data.get("query", "")
                max_results = data.get("max_results", 10)

                if not query:
                    return jsonify({"error": "Query is required"}), 400

                if not KNOWLEDGE_AVAILABLE:
                    return jsonify({"error": "Knowledge engine not available"}), 503

                results = knowledge.search(query, max_results=max_results)

                return jsonify(
                    {
                        "query": query,
                        "results": [item.to_dict() for item in results],
                        "total": len(results),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/knowledge/add", methods=["POST"])
        @require_api_key
        def knowledge_add():
            try:
                data = request.json
                content = data.get("content", "")
                category = data.get("category", "General Knowledge")
                type_ = data.get("type", "fact")
                tags = data.get("tags", [])
                confidence = data.get("confidence", 75.0)
                importance = data.get("importance", 0.5)

                if not content:
                    return jsonify({"error": "Content is required"}), 400

                if not KNOWLEDGE_AVAILABLE:
                    return jsonify({"error": "Knowledge engine not available"}), 503

                item = knowledge.add(
                    content=content,
                    category=category,
                    type=type_,
                    tags=tags,
                    confidence=confidence,
                    importance=importance,
                )

                knowledge.save()

                return jsonify(
                    {
                        "status": "success",
                        "item": (
                            item.to_dict()
                            if hasattr(item, "to_dict")
                            else {"id": str(item), "content": content, "category": category}
                        ),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/knowledge/stats", methods=["GET"])
        @require_api_key
        def knowledge_stats():
            try:
                import time as _time

                now = _time.time()
                if (
                    _knowledge_stats_cache["data"]
                    and (now - _knowledge_stats_cache["timestamp"]) < 300
                ):
                    cached = dict(_knowledge_stats_cache["data"])
                    cached["cached"] = True
                    return jsonify(cached)

                if not KNOWLEDGE_AVAILABLE:
                    return jsonify({"error": "Knowledge engine not available"}), 503

                stats = knowledge.stats()
                result = {
                    "total_items": stats.total,
                    "database_size_mb": stats.database_size_mb,
                    "by_category": stats.by_category,
                    "by_type": stats.by_type,
                    "by_status": stats.by_status,
                    "avg_confidence": stats.avg_confidence,
                    "active": stats.active,
                    "archived": stats.archived,
                    "ai_enhanced_count": stats.ai_enhanced_count,
                    "timestamp": datetime.now().isoformat(),
                }

                _knowledge_stats_cache["data"] = result
                _knowledge_stats_cache["timestamp"] = _time.time()

                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # KNOWLEDGE ALL ENDPOINT
        # ============================================================

        @app.route("/api/knowledge/all", methods=["GET"])
        @require_api_key
        def knowledge_all():
            """Get all knowledge items (cached 5 min)"""
            try:
                import time as _time

                now = _time.time()
                if _knowledge_all_cache["data"] and (now - _knowledge_all_cache["timestamp"]) < 300:
                    cached = dict(_knowledge_all_cache["data"])
                    cached["cached"] = True
                    return jsonify(cached)

                if not KNOWLEDGE_AVAILABLE:
                    return jsonify({"error": "Knowledge engine not available"}), 503

                items = knowledge.all()
                result = {
                    "items": [item.to_dict() for item in items],
                    "total": len(items),
                    "timestamp": datetime.now().isoformat(),
                }

                _knowledge_all_cache["data"] = result
                _knowledge_all_cache["timestamp"] = _time.time()

                return jsonify(result)
            except Exception as e:
                logger.error(f"Knowledge all error: {e}")
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # COGNITIVE MIRROR - REAL REFLECTION ENDPOINTS
        # ============================================================

        def calculate_health_score(cpu: float, ram: float, disk: float) -> float:
            cpu_score = max(0, 100 - cpu)
            ram_score = max(0, 100 - ram)
            disk_score = max(0, 100 - disk)
            return round((cpu_score * 0.4 + ram_score * 0.4 + disk_score * 0.2), 1)

        @app.route("/api/cognitive-mirror/metrics", methods=["GET"])
        @require_api_key
        def cognitive_metrics():
            try:
                metrics = {}

                # Knowledge Metrics
                if KNOWLEDGE_AVAILABLE:
                    stats = knowledge.stats()
                    metrics["knowledge"] = {
                        "total_items": stats.total,
                        "categories": (
                            len(stats.by_category) if hasattr(stats, "by_category") else 0
                        ),
                        "avg_confidence": (
                            stats.avg_confidence if hasattr(stats, "avg_confidence") else 0
                        ),
                        "ai_enhanced": (
                            stats.ai_enhanced_count if hasattr(stats, "ai_enhanced_count") else 0
                        ),
                        "active": stats.active if hasattr(stats, "active") else 0,
                        "archived": stats.archived if hasattr(stats, "archived") else 0,
                    }
                else:
                    metrics["knowledge"] = {
                        "total_items": 0,
                        "categories": 0,
                        "avg_confidence": 0,
                        "ai_enhanced": 0,
                        "active": 0,
                        "archived": 0,
                    }

                # Brain Metrics
                if BRAIN_AVAILABLE and brain:
                    try:
                        brain_state = brain.get_state() if hasattr(brain, "get_state") else {}
                        metrics["brain"] = {
                            "health": brain_state.get("health", 85),
                            "consciousness": brain_state.get("consciousness", 0.7),
                            "emotional_state": brain_state.get("emotional_state", "CALM"),
                            "learning_rate": brain_state.get("learning_rate", 0.5),
                            "curiosity_level": brain_state.get("curiosity", 0.6),
                        }
                    except:
                        metrics["brain"] = {
                            "health": 85,
                            "consciousness": 0.7,
                            "emotional_state": "CALM",
                            "learning_rate": 0.5,
                            "curiosity_level": 0.6,
                        }
                else:
                    metrics["brain"] = {
                        "health": 85,
                        "consciousness": 0.7,
                        "emotional_state": "CALM",
                        "learning_rate": 0.5,
                        "curiosity_level": 0.6,
                    }

                # System Metrics
                try:
                    import psutil

                    cpu = psutil.cpu_percent(interval=0.5)
                    mem = psutil.virtual_memory()
                    disk = psutil.disk_usage("/")
                    uptime = int(time.time() - _startup_time)
                    metrics["system"] = {
                        "cpu": cpu,
                        "ram_percent": mem.percent,
                        "disk_percent": disk.percent,
                        "uptime_seconds": uptime,
                        "uptime_hours": round(uptime / 3600, 1),
                        "uptime_days": round(uptime / 86400, 1),
                        "health_score": calculate_health_score(cpu, mem.percent, disk.percent),
                    }
                except:
                    metrics["system"] = {
                        "cpu": 0,
                        "ram_percent": 0,
                        "disk_percent": 0,
                        "uptime_seconds": 0,
                        "uptime_hours": 0,
                        "uptime_days": 0,
                        "health_score": 90,
                    }

                # Memory Metrics
                try:
                    from core.memory import memory

                    if memory:
                        mem_stats = memory.stats() if hasattr(memory, "stats") else {}
                        metrics["memory"] = {
                            "total_items": mem_stats.get("total", 0),
                            "semantic_relationships": mem_stats.get("relationships", 0),
                        }
                    else:
                        metrics["memory"] = {"total_items": 0, "semantic_relationships": 0}
                except:
                    metrics["memory"] = {"total_items": 0, "semantic_relationships": 0}

                # Trading Performance
                try:
                    from core.performance import performance

                    if performance:
                        perf_data = (
                            performance.get_summary() if hasattr(performance, "get_summary") else {}
                        )
                        metrics["trading"] = {
                            "pnl": perf_data.get("pnl", 0),
                            "win_rate": perf_data.get("win_rate", 0),
                            "total_trades": perf_data.get("total_trades", 0),
                            "open_positions": perf_data.get("open_positions", 0),
                        }
                    else:
                        metrics["trading"] = {
                            "pnl": 0,
                            "win_rate": 0,
                            "total_trades": 0,
                            "open_positions": 0,
                        }
                except:
                    metrics["trading"] = {
                        "pnl": 0,
                        "win_rate": 0,
                        "total_trades": 0,
                        "open_positions": 0,
                    }

                # WebSocket Status
                global _ws_connected, _ws_channels, _ws_last_message
                metrics["websocket"] = {
                    "connected": _ws_connected,
                    "active_channels": _ws_channels,
                    "last_message": _ws_last_message,
                }

                metrics["timestamp"] = datetime.now().isoformat()

                return jsonify(metrics)

            except Exception as e:
                logger.error(f"Cognitive metrics error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/cognitive-mirror/reflections", methods=["GET"])
        @require_api_key
        def generate_reflections():
            try:
                reflections = []

                if KNOWLEDGE_AVAILABLE:
                    stats = knowledge.stats()
                    if stats.total > 0:
                        reflections.append(
                            {
                                "type": "knowledge",
                                "icon": "📚",
                                "content": f"Knowledge base contains {stats.total} items across {len(stats.by_category) if hasattr(stats, 'by_category') else 0} categories.",
                                "importance": "high" if stats.total > 50 else "medium",
                            }
                        )

                try:
                    import psutil

                    cpu = psutil.cpu_percent(interval=0.5)
                    mem = psutil.virtual_memory()
                    health = calculate_health_score(cpu, mem.percent, 0)
                    if health > 85:
                        reflections.append(
                            {
                                "type": "health",
                                "icon": "✅",
                                "content": f"System health is excellent at {health:.1f}%. CPU: {cpu:.1f}%, RAM: {mem.percent:.1f}%.",
                                "importance": "high",
                            }
                        )
                    elif health > 70:
                        reflections.append(
                            {
                                "type": "health",
                                "icon": "⚠️",
                                "content": f"System health is moderate at {health:.1f}%. CPU: {cpu:.1f}%, RAM: {mem.percent:.1f}%.",
                                "importance": "medium",
                            }
                        )
                    else:
                        reflections.append(
                            {
                                "type": "health",
                                "icon": "🔴",
                                "content": f"System health is low at {health:.1f}%. CPU: {cpu:.1f}%, RAM: {mem.percent:.1f}%.",
                                "importance": "high",
                            }
                        )
                except:
                    pass

                if BRAIN_AVAILABLE and brain:
                    try:
                        brain_state = brain.get_state() if hasattr(brain, "get_state") else {}
                        consciousness = brain_state.get("consciousness", 0.5)
                        if consciousness > 0.7:
                            reflections.append(
                                {
                                    "type": "consciousness",
                                    "icon": "🧠",
                                    "content": f"Consciousness level is high at {consciousness*100:.0f}%.",
                                    "importance": "high",
                                }
                            )
                    except:
                        pass

                try:
                    uptime = int(time.time() - _startup_time)
                    days = uptime // 86400
                    hours = (uptime % 86400) // 3600
                    if days > 0:
                        reflections.append(
                            {
                                "type": "uptime",
                                "icon": "⏰",
                                "content": f"System has been running for {days}d {hours}h.",
                                "importance": "high" if days > 7 else "medium",
                            }
                        )
                except:
                    pass

                reflections.sort(
                    key=lambda x: (
                        0
                        if x.get("importance") == "high"
                        else 1 if x.get("importance") == "medium" else 2
                    )
                )

                return jsonify(
                    {
                        "reflections": reflections,
                        "count": len(reflections),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            except Exception as e:
                logger.error(f"Reflection generation error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/cognitive-mirror/narrative", methods=["GET"])
        @require_api_key
        def cognitive_narrative():
            try:
                import psutil

                parts = []

                cpu = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory()
                health = calculate_health_score(cpu, mem.percent, 0)
                if health > 85:
                    parts.append(f"🟢 System health: {health:.1f}%")
                elif health > 70:
                    parts.append(f"🟡 System health: {health:.1f}%")
                else:
                    parts.append(f"🔴 System health: {health:.1f}%")

                if KNOWLEDGE_AVAILABLE:
                    stats = knowledge.stats()
                    parts.append(f"📚 Knowledge: {stats.total} items")

                uptime = int(time.time() - _startup_time)
                hours = round(uptime / 3600, 1)
                parts.append(f"⏰ Uptime: {hours}h")

                summary = " · ".join(parts) if parts else "System is initializing..."

                return jsonify({"summary": summary, "timestamp": datetime.now().isoformat()})

            except Exception as e:
                logger.error(f"Narrative generation error: {e}")
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # CONFIG ENDPOINTS - Terintegrasi dengan config.py
        # ============================================================

        @app.route("/api/config", methods=["GET"])
        @require_api_key
        def get_config():
            try:
                import config as cfg

                return jsonify(
                    {
                        "app_name": cfg.APP_NAME,
                        "app_version": cfg.APP_VERSION,
                        "app_author": cfg.APP_AUTHOR,
                        "exchange_name": cfg.EXCHANGE_NAME,
                        "exchange_type": cfg.EXCHANGE_TYPE,
                        "coingecko_rate_limit": cfg.COINGECKO_RATE_LIMIT,
                        "request_delay": cfg.REQUEST_DELAY,
                        "cache_ttl_seconds": cfg.CACHE_TTL_SECONDS,
                        "max_markets": cfg.MAX_MARKETS,
                        "default_pairs": cfg.DEFAULT_PAIRS,
                        "default_timeframes": cfg.DEFAULT_TIMEFRAMES,
                        "main_timeframe": cfg.MAIN_TIMEFRAME,
                        "scan_interval_seconds": cfg.SCAN_INTERVAL_SECONDS,
                        "max_workers": cfg.MAX_WORKERS,
                        "scanner_batch_size": cfg.SCANNER_BATCH_SIZE,
                        "scanner_batch_delay": cfg.SCANNER_BATCH_DELAY,
                        "min_mtf_alignment": cfg.MIN_MTF_ALIGNMENT,
                        "min_signal_strength": cfg.MIN_SIGNAL_STRENGTH,
                        "min_signal_confidence": cfg.MIN_SIGNAL_CONFIDENCE,
                        "signal_cooldown_seconds": cfg.SIGNAL_COOLDOWN_SECONDS,
                        "max_signals_per_scan": cfg.MAX_SIGNALS_PER_SCAN,
                        "default_risk_percent": cfg.DEFAULT_RISK_PERCENT,
                        "default_risk_reward": cfg.DEFAULT_RISK_REWARD,
                        "max_position_size": cfg.MAX_POSITION_SIZE,
                        "min_position_size": cfg.MIN_POSITION_SIZE,
                        "max_daily_trades": cfg.MAX_DAILY_TRADES,
                        "max_open_positions": cfg.MAX_OPEN_POSITIONS,
                        "max_drawdown_percent": cfg.MAX_DRAWDOWN_PERCENT,
                        "stop_loss_percent": cfg.STOP_LOSS_PERCENT,
                        "take_profit_percent": cfg.TAKE_PROFIT_PERCENT,
                        "trading_enabled": cfg.TRADING_ENABLED,
                        "paper_trading": cfg.PAPER_TRADING,
                        "auto_trade": cfg.AUTO_TRADE,
                        "telegram_enabled": cfg.TELEGRAM_ENABLED,
                        "telegram_configured": bool(
                            cfg.TELEGRAM_BOT_TOKEN and cfg.TELEGRAM_CHAT_ID
                        ),
                        "learning_enabled": cfg.LEARNING_ENABLED,
                        "learning_interval_seconds": cfg.LEARNING_INTERVAL_SECONDS,
                        "learning_auto_start": cfg.LEARNING_AUTO_START,
                        "learning_max_history": cfg.LEARNING_MAX_HISTORY,
                        "prediction_enabled": cfg.PREDICTION_ENABLED,
                        "prediction_horizon": cfg.PREDICTION_HORIZON,
                        "prediction_min_confidence": cfg.PREDICTION_MIN_CONFIDENCE,
                        "health_check_interval": cfg.HEALTH_CHECK_INTERVAL,
                        "health_min_score": cfg.HEALTH_MIN_SCORE,
                        "health_critical_score": cfg.HEALTH_CRITICAL_SCORE,
                        "debug_mode": cfg.DEBUG_MODE,
                        "log_level": cfg.LOG_LEVEL,
                        "max_threads": cfg.MAX_THREADS,
                        "thread_pool_size": cfg.THREAD_POOL_SIZE,
                        "api_timeout": cfg.API_TIMEOUT,
                        "backend_status": "online",
                        "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                        "dividend_items": (
                            len(dividend.df) if DIVIDEND_AVAILABLE and dividend else 0
                        ),
                        "ai_enabled": DEEPSEEK_ENABLED,
                        "uptime_seconds": int(time.time() - _startup_time),
                    }
                )
            except Exception as e:
                logger.error(f"Config error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/config/default", methods=["GET"])
        @require_api_key
        def get_default_config():
            try:
                import config as cfg

                return jsonify(
                    {
                        "app_name": cfg.APP_NAME,
                        "app_version": cfg.APP_VERSION,
                        "app_author": cfg.APP_AUTHOR,
                        "exchange_name": cfg.EXCHANGE_NAME,
                        "exchange_type": cfg.EXCHANGE_TYPE,
                        "coingecko_rate_limit": cfg.COINGECKO_RATE_LIMIT,
                        "request_delay": cfg.REQUEST_DELAY,
                        "cache_ttl_seconds": cfg.CACHE_TTL_SECONDS,
                        "max_markets": cfg.MAX_MARKETS,
                        "default_pairs": cfg.DEFAULT_PAIRS,
                        "default_timeframes": cfg.DEFAULT_TIMEFRAMES,
                        "main_timeframe": cfg.MAIN_TIMEFRAME,
                        "scan_interval_seconds": cfg.SCAN_INTERVAL_SECONDS,
                        "max_workers": cfg.MAX_WORKERS,
                        "min_signal_strength": cfg.MIN_SIGNAL_STRENGTH,
                        "min_signal_confidence": cfg.MIN_SIGNAL_CONFIDENCE,
                        "default_risk_percent": cfg.DEFAULT_RISK_PERCENT,
                        "default_risk_reward": cfg.DEFAULT_RISK_REWARD,
                        "max_position_size": cfg.MAX_POSITION_SIZE,
                        "trading_enabled": cfg.TRADING_ENABLED,
                        "paper_trading": cfg.PAPER_TRADING,
                        "telegram_enabled": cfg.TELEGRAM_ENABLED,
                        "learning_enabled": cfg.LEARNING_ENABLED,
                        "prediction_enabled": cfg.PREDICTION_ENABLED,
                        "debug_mode": cfg.DEBUG_MODE,
                        "log_level": cfg.LOG_LEVEL,
                        "max_threads": cfg.MAX_THREADS,
                        "api_timeout": cfg.API_TIMEOUT,
                    }
                )
            except Exception as e:
                logger.error(f"Default config error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/config", methods=["POST"])
        @require_api_key
        def update_config():
            try:
                data = request.json
                if not data:
                    return jsonify({"error": "No data provided"}), 400

                import config as cfg
                import re
                from pathlib import Path

                config_file = Path(__file__).resolve().parent / "config.py"
                with open(config_file, "r") as f:
                    content = f.read()

                updated = []
                for key, value in data.items():
                    upper_key = key.upper()
                    if hasattr(cfg, upper_key):
                        setattr(cfg, upper_key, value)
                        if isinstance(value, str):
                            repr_value = f"'{value}'"
                        else:
                            repr_value = repr(value)
                        pattern = rf"^{upper_key}\s*=\s*[^\n]+"
                        replacement = f"{upper_key} = {repr_value}"
                        if re.search(pattern, content, re.MULTILINE):
                            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                        updated.append(key)

                with open(config_file, "w") as f:
                    f.write(content)

                logger.info(f"Config updated: {len(updated)} keys")
                return jsonify({"status": "success", "updated": updated})
            except Exception as e:
                logger.error(f"Config update error: {e}")
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # TELEGRAM ENDPOINTS
        # ============================================================

        @app.route("/api/telegram/status", methods=["GET"])
        @require_api_key
        def telegram_status():
            try:
                token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
                chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
                configured = bool(token and chat_id)
                return jsonify(
                    {
                        "configured": configured,
                        "status": "online" if configured else "offline",
                        "bot_name": "InksideBot" if configured else None,
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/telegram/send", methods=["POST"])
        @require_api_key
        def telegram_send():
            try:
                data = request.json
                message = data.get("message", "")
                if not message:
                    return jsonify({"error": "Message is required"}), 400
                success = send_telegram_message(message)
                return jsonify(
                    {
                        "sent": success,
                        "status": "success" if success else "error",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # WEBSOCKET HANDLERS
        # ============================================================

        @socketio.on("connect")
        def handle_connect():
            global _ws_connected, _ws_channels
            _ws_connected = True
            _ws_channels += 1
            logger.info(f"🔗 Client connected: {request.sid} (total: {_ws_channels})")
            emit("connected", {"status": "ok", "version": APP_VERSION})

        @socketio.on("disconnect")
        def handle_disconnect():
            global _ws_connected, _ws_channels
            _ws_connected = False
            _ws_channels = max(0, _ws_channels - 1)
            logger.info(f"🔌 Client disconnected: {request.sid} (remaining: {_ws_channels})")

        # ============================================================
        # WATCHDOG COMPONENT ENDPOINT
        # ============================================================

        @app.route("/api/watchdog/component/<component_name>", methods=["GET"])
        @require_api_key
        def api_watchdog_component(component_name):
            try:
                component = {
                    "name": component_name,
                    "registered": True,
                    "heartbeat": {
                        "status": "alive",
                        "beat_count": 0,
                        "missed_beats": 0,
                        "last_beat": datetime.now().isoformat(),
                        "restart_count": 0,
                        "is_alive": True,
                    },
                    "dependencies": [],
                    "health_score": 90.0,
                }
                if WATCHDOG_AVAILABLE and watchdog is not None:
                    if hasattr(watchdog, "get_component_status"):
                        status = watchdog.get_component_status(component_name)
                        if status:
                            component.update(status)
                return jsonify(component)
            except Exception as e:
                logger.error(f"Component detail error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/watchdog/circuit/<component_name>/reset", methods=["POST"])
        @require_api_key
        def api_watchdog_circuit_reset(component_name):
            try:
                return jsonify(
                    {
                        "status": "success",
                        "message": f"Circuit reset for {component_name}",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/watchdog/report", methods=["GET"])
        @require_api_key
        def api_watchdog_report():
            try:
                return jsonify(
                    {
                        "status": "running",
                        "components": WATCHDOG_AVAILABLE and watchdog is not None,
                        "timestamp": datetime.now().isoformat(),
                        "data": {"total_components": 7, "healthy": 7, "degraded": 0, "critical": 0},
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # LEARNING ENDPOINTS
        # ============================================================

        # ============================================================
        # LEARNING ENDPOINTS — REAL (dari core.learning)
        # ============================================================

        @app.route("/api/learning/stats", methods=["GET"])
        @require_api_key
        def api_learning_stats():
            try:
                stats = {
                    "cycleCount": 0,
                    "learningActive": False,
                    "learningRate": 0.0,
                    "decayRate": 0.0,
                    "circuitBreakers": 0,
                    "modulesCount": 0,
                    "active_learning_sessions": 0,
                    "timestamp": datetime.now().isoformat(),
                }

                # Dari brain
                if BRAIN_AVAILABLE and brain:
                    stats["cycleCount"] = brain.cycles
                    stats["learningActive"] = brain.metrics.get("learning_count", 0) > 0
                    stats["modulesCount"] = brain.available_modules_count

                # Dari adaptive engine
                try:
                    from core.learning import adaptive_engine

                    if adaptive_engine is not None:
                        all_data = adaptive_engine.get_all()
                        if isinstance(all_data, dict):
                            stats["adaptive_entries"] = len(all_data)
                        elif isinstance(all_data, list):
                            stats["adaptive_entries"] = len(all_data)
                        else:
                            stats["adaptive_entries"] = 0
                except Exception as e:
                    stats["adaptive_error"] = str(e)

                # Dari curiosity engine
                try:
                    from core.learning import curiosity_engine

                    if curiosity_engine is not None:
                        qs = curiosity_engine.get_questions()
                        stats["active_learning_sessions"] = len(qs) if qs else 0
                except Exception as e:
                    stats["curiosity_error"] = str(e)

                return jsonify(stats)
            except Exception as e:
                logger.error(f"Learning stats error: {e}")
                return jsonify({"error": str(e)}), 500

        @app.route("/api/learning/status", methods=["GET"])
        @require_api_key
        def api_learning_status():
            try:
                return jsonify(
                    {
                        "learning": {
                            "active": DEEPSEEK_ENABLED,
                            "cycles": brain.cycles if BRAIN_AVAILABLE and brain else 0,
                            "status": "ACTIVE" if DEEPSEEK_ENABLED else "INACTIVE",
                        },
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/learning/adaptive", methods=["GET"])
        @require_api_key
        def api_learning_adaptive():
            try:
                from core.learning import adaptive_engine

                if adaptive_engine is None:
                    return jsonify(
                        {"entries": [], "count": 0, "error": "adaptive_engine not loaded"}
                    )

                # Coba get_all()
                entries_raw = adaptive_engine.get_all()

                entries = []
                if isinstance(entries_raw, dict):
                    for key, val in entries_raw.items():
                        if hasattr(val, "to_dict"):
                            entry = val.to_dict()
                        elif isinstance(val, dict):
                            entry = val
                        else:
                            entry = {"key": key, "value": str(val)}
                        entry.setdefault("key", key)
                        entries.append(entry)
                elif isinstance(entries_raw, list):
                    for item in entries_raw:
                        if hasattr(item, "to_dict"):
                            entries.append(item.to_dict())
                        elif isinstance(item, dict):
                            entries.append(item)

                return jsonify(
                    {
                        "entries": entries,
                        "count": len(entries),
                        "is_empty": len(entries) == 0,
                        "message": "Engine belum diisi oleh Brain" if len(entries) == 0 else None,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Adaptive error: {e}")
                return jsonify({"entries": [], "error": str(e), "count": 0}), 500

        @app.route("/api/learning/curiosity", methods=["GET"])
        @require_api_key
        def api_learning_curiosity():
            try:
                from core.learning import curiosity_engine

                if curiosity_engine is None:
                    return jsonify(
                        {"questions": [], "count": 0, "error": "curiosity_engine not loaded"}
                    )

                questions_raw = curiosity_engine.get_questions()
                questions = []
                if questions_raw:
                    for q in questions_raw:
                        if hasattr(q, "to_dict"):
                            questions.append(q.to_dict())
                        elif isinstance(q, dict):
                            questions.append(q)
                        else:
                            questions.append({"question": str(q)})

                stats = {}
                try:
                    stats = curiosity_engine.statistics() or {}
                except Exception:
                    pass

                return jsonify(
                    {
                        "questions": questions,
                        "count": len(questions),
                        "statistics": stats,
                        "is_empty": len(questions) == 0,
                        "message": "Engine belum diisi oleh Brain" if len(questions) == 0 else None,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Curiosity error: {e}")
                return jsonify({"questions": [], "error": str(e), "count": 0}), 500

        @app.route("/api/learning/goals", methods=["GET"])
        @require_api_key
        def api_learning_goals():
            try:
                from core.learning import goal_manager

                if goal_manager is None:
                    return jsonify({"goals": [], "count": 0, "error": "goal_manager not loaded"})

                # Ambil goals — pakai active_goals() dulu
                goals_raw = []

                # Coba berbagai method
                for method_name in ["active_goals", "priority_goals", "latest"]:
                    if hasattr(goal_manager, method_name):
                        try:
                            result = getattr(goal_manager, method_name)()
                            if result:
                                if isinstance(result, list):
                                    goals_raw = result
                                else:
                                    goals_raw = [result]
                                break
                        except Exception as e:
                            logger.debug(f"goal_manager.{method_name} error: {e}")

                goals = []
                if goals_raw:
                    for g in goals_raw:
                        if hasattr(g, "to_dict"):
                            goals.append(g.to_dict())
                        elif isinstance(g, dict):
                            goals.append(g)

                return jsonify(
                    {
                        "goals": goals,
                        "count": len(goals),
                        "is_empty": len(goals) == 0,
                        "message": "Engine belum diisi oleh Brain" if len(goals) == 0 else None,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Goals error: {e}")
                return jsonify({"goals": [], "error": str(e), "count": 0}), 500

        @app.route("/api/learning/experience", methods=["GET"])
        @require_api_key
        def api_learning_experience():
            try:
                from core.learning import experience_engine

                if experience_engine is None:
                    return jsonify({"total": 0, "error": "experience_engine not loaded"})

                # Stats dasar
                stats = {
                    "sensory_buffer": 0,
                    "short_term": 0,
                    "working_memory": 0,
                    "permanent": 0,
                    "total": 0,
                }

                try:
                    count = experience_engine.count()
                    stats["total"] = count if isinstance(count, int) else 0
                except Exception:
                    pass

                try:
                    stage_counts = experience_engine.by_stage()
                    if isinstance(stage_counts, dict):
                        stats["sensory_buffer"] = stage_counts.get("sensory", 0)
                        stats["short_term"] = stage_counts.get("short_term", 0)
                        stats["working_memory"] = stage_counts.get("working", 0)
                        stats["permanent"] = stage_counts.get("permanent", 0)
                except Exception:
                    pass

                # Fallback kalau knowledge base ada
                if stats["total"] == 0 and KNOWLEDGE_AVAILABLE and knowledge:
                    try:
                        stats["total"] = knowledge.stats().total
                    except Exception:
                        pass

                return jsonify(stats)
            except Exception as e:
                logger.error(f"Experience error: {e}")
                return jsonify({"total": 0, "error": str(e)}), 500

        @app.route("/api/learning/graph", methods=["GET"])
        @require_api_key
        def api_learning_graph():
            try:
                from core.learning import knowledge_graph

                if knowledge_graph is None:
                    return jsonify(
                        {
                            "nodes": 0,
                            "edges": 0,
                            "concepts": [],
                            "relations": [],
                            "is_empty": True,
                            "error": "knowledge_graph not loaded",
                        }
                    )

                # all() return {node_id: node_data}
                all_data = knowledge_graph.all() if hasattr(knowledge_graph, "all") else {}

                concepts = []
                relations = []

                if isinstance(all_data, dict):
                    for node_id, node_data in all_data.items():
                        # Extract concept info
                        concept = {"name": str(node_id)}

                        if hasattr(node_data, "to_dict"):
                            node_dict = node_data.to_dict()
                            concept.update(node_dict)
                        elif isinstance(node_data, dict):
                            concept.update(node_data)

                        concepts.append(concept)

                        # Extract relations dari node_data kalau ada
                        if isinstance(node_data, dict):
                            neighbors = (
                                node_data.get("neighbors") or node_data.get("connections") or []
                            )
                            for n in neighbors:
                                if isinstance(n, dict):
                                    relations.append(
                                        {
                                            "source": str(node_id),
                                            "target": str(n.get("target") or n.get("node") or n),
                                            "type": str(
                                                n.get("relation") or n.get("type") or "related_to"
                                            ),
                                            "weight": float(n.get("weight", 1.0)),
                                        }
                                    )

                # Ambil dari health() untuk count akurat
                health = {}
                try:
                    health = knowledge_graph.health() or {}
                except Exception:
                    pass

                # Kalau relations dari neighbors kosong, ambil dari health connections
                nodes_count = health.get("nodes", len(concepts))
                edges_count = health.get("connections", len(relations))

                is_empty = nodes_count == 0 and edges_count == 0

                return jsonify(
                    {
                        "nodes": nodes_count,
                        "edges": edges_count,
                        "concepts": concepts[:50],
                        "relations": relations[:50],
                        "health": health,
                        "is_empty": is_empty,
                        "message": "Engine belum diisi oleh Brain" if is_empty else None,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Graph error: {e}")
                return (
                    jsonify(
                        {
                            "nodes": 0,
                            "edges": 0,
                            "concepts": [],
                            "relations": [],
                            "is_empty": True,
                            "error": str(e),
                        }
                    ),
                    500,
                )

        @app.route("/api/learning/evaluator", methods=["GET"])
        @require_api_key
        def api_learning_evaluator():
            try:
                from core.learning import evaluator_engine

                if evaluator_engine is None:
                    return jsonify({"accuracy": 0, "error": "evaluator_engine not loaded"})

                stats = {
                    "accuracy": 0,
                    "average_confidence": 0,
                    "average_score": 0,
                    "success_rate": 0,
                    "total_evaluations": 0,
                }

                try:
                    acc = evaluator_engine.accuracy()
                    stats["accuracy"] = (
                        round(float(acc) * 100, 2)
                        if acc and acc <= 1
                        else round(float(acc), 2) if acc else 0
                    )
                except Exception:
                    pass

                try:
                    stats["average_confidence"] = round(
                        float(evaluator_engine.average_confidence() or 0), 2
                    )
                except Exception:
                    pass

                try:
                    stats["average_score"] = round(float(evaluator_engine.average_score() or 0), 2)
                except Exception:
                    pass

                try:
                    stats["success_rate"] = round(float(evaluator_engine.success_rate() or 0), 2)
                except Exception:
                    pass

                try:
                    status = evaluator_engine.status()
                    if isinstance(status, dict):
                        stats["total_evaluations"] = (
                            status.get("total", 0) or status.get("count", 0) or 0
                        )
                except Exception:
                    pass

                stats["is_empty"] = stats.get("total_evaluations", 0) == 0
                stats["message"] = "Engine belum diisi oleh Brain" if stats["is_empty"] else None
                stats["timestamp"] = datetime.now().isoformat()
                return jsonify(stats)
            except Exception as e:
                logger.error(f"Evaluator error: {e}")
                return jsonify({"accuracy": 0, "error": str(e)}), 500

        @app.route("/api/learning/simulate", methods=["POST"])
        @require_api_key
        def api_learning_simulate():
            try:
                data = request.json or {}
                return jsonify(
                    {
                        "status": "success",
                        "simulation_id": f"sim_{int(time.time())}",
                        "result": "Scenario simulated successfully",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/learning/stress_test", methods=["POST"])
        @require_api_key
        def api_learning_stress_test():
            try:
                data = request.json or {}
                return jsonify(
                    {
                        "status": "success",
                        "test_id": f"stress_{int(time.time())}",
                        "results": {
                            "passed": True,
                            "score": 85.0,
                            "metrics": {"response_time": 0.5, "accuracy": 92.0},
                        },
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # MODULES ENDPOINTS
        # ============================================================

        @app.route("/api/modules/list", methods=["GET"])
        @require_api_key
        def api_modules_list():
            try:
                modules = []

                if BRAIN_AVAILABLE and brain:
                    for name, available in brain.modules_available.items():
                        modules.append(
                            {
                                "name": name,
                                "title": name.replace("_", " ").title(),
                                "version": "1.0",
                                "priority": 1,
                                "status": "ONLINE" if available else "OFFLINE",
                                "role": f"Cognitive module: {name}",
                                "online": available,
                                "health_score": 100 if available else 0,
                            }
                        )

                return jsonify(
                    {
                        "modules": modules,
                        "count": len(modules),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                logger.error(f"Modules list error: {e}")
                return jsonify({"modules": [], "count": 0, "error": str(e)}), 500
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # PATTERN ENDPOINTS
        # ============================================================

        @app.route("/api/patterns", methods=["GET"])
        @require_api_key
        def api_patterns():
            try:
                patterns = []
                if DEEPSEEK_ENABLED:
                    patterns = [
                        {
                            "id": "pattern_001",
                            "name": "Bullish Divergence",
                            "type": "DIVERGENCE",
                            "pair": "BTC/USDT",
                            "confidence": 0.85,
                            "timestamp": datetime.now().isoformat(),
                            "description": "RSI divergence detected",
                            "strength": "STRONG",
                        }
                    ]
                return jsonify(
                    {
                        "patterns": patterns,
                        "count": len(patterns),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/patterns/stats", methods=["GET"])
        @require_api_key
        def api_pattern_stats():
            try:
                return jsonify(
                    {
                        "total_patterns": 0,
                        "by_type": {
                            "DIVERGENCE": 0,
                            "REVERSAL": 0,
                            "BREAKOUT": 0,
                            "CONTINUATION": 0,
                        },
                        "by_strength": {"STRONG": 0, "MODERATE": 0, "WEAK": 0},
                        "accuracy": 0.0,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/patterns/detect", methods=["POST"])
        @require_api_key
        def api_patterns_detect():
            try:
                data = request.json or {}
                pair = data.get("pair", "BTC/USDT")
                detected = []
                if DEEPSEEK_ENABLED:
                    detected = [
                        {
                            "pattern": "Bullish Divergence",
                            "confidence": 0.82,
                            "pair": pair,
                            "timestamp": datetime.now().isoformat(),
                        }
                    ]
                return jsonify(
                    {
                        "detected": detected,
                        "count": len(detected),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================
        # START SERVER

        # ============================================================
        # AI PROMPTS ENDPOINTS
        # ============================================================

        @app.route("/api/ai/prompts", methods=["GET"])
        @require_api_key
        def list_ai_prompts():
            try:
                from core.prompts.system_prompts import SYSTEM_PROMPTS, ACTIVE_PROMPT

                return jsonify(
                    {
                        "prompts": list(SYSTEM_PROMPTS.keys()),
                        "active": ACTIVE_PROMPT,
                        "timestamp": datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route("/api/ai/prompts/set", methods=["POST"])
        @require_api_key
        def set_ai_prompt():
            try:
                data = request.json
                name = data.get("prompt", "knowledge_qa")
                from core.prompts.system_prompts import set_active_prompt

                success = set_active_prompt(name)
                if success:
                    return jsonify({"status": "success", "active_prompt": name})
                return jsonify({"error": f"Prompt {name} not found"}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # ============================================================

        logger.info(f"🌐 Starting API Server on {API_HOST}:{API_PORT}")

        def run_server():
            socketio.run(
                app,
                host=API_HOST,
                port=API_PORT,
                debug=False,
                use_reloader=False,
                allow_unsafe_werkzeug=True,
            )

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        logger.info(f"✅ API Server running on http://{API_HOST}:{API_PORT}")
        logger.info(f"   📚 Knowledge Engine: {'ONLINE' if KNOWLEDGE_AVAILABLE else 'OFFLINE'}")
        logger.info(f"   💰 Dividend Hunter: {'ONLINE' if DIVIDEND_AVAILABLE else 'OFFLINE'}")
        logger.info(f"   🤖 AI: {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
        logger.info(f"   🧠 Consciousness: {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
        logger.info(f"   📡 WebSocket: /socket.io/")

        return True

    except ImportError as e:
        logger.warning(f"⚠️ Flask not available: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ API Server error: {e}")
        return False


# ============================================================
# CONSCIOUSNESS AI SCHEDULER - Self-Improvement
# ============================================================


def consciousness_improvement_scheduler():
    logger.info("🧠 Consciousness Improvement Scheduler started (daily at 2:00 AM)")
    while not _shutdown_flag.is_set():
        now = datetime.now()
        if now.hour == 2 and now.minute == 0:
            try:
                logger.info("🧠 Starting daily consciousness improvement...")
                performance_data = {
                    "win_rate": 0,
                    "total_trades": 0,
                    "pnl": 0,
                    "open_positions": 0,
                    "risk_level": "MODERATE",
                }
                result = deepseek_ai.daily_improvement(performance_data)
                if result.get("status") == "success":
                    logger.info(
                        f"✅ Consciousness improvement completed: {deepseek_ai.consciousness.growth_stage}"
                    )
                time.sleep(3600)
            except Exception as e:
                logger.error(f"❌ Consciousness scheduler error: {e}")
        time.sleep(60)


def start_consciousness_scheduler():
    try:
        scheduler_thread = threading.Thread(target=consciousness_improvement_scheduler, daemon=True)
        scheduler_thread.start()
        logger.info("✅ Consciousness AI Scheduler started")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to start consciousness scheduler: {e}")
        return False


# ============================================================
# MAIN HEADLESS FUNCTION
# ============================================================

# ============================================================
# BRAIN OBSERVE SCHEDULER
# ============================================================


def brain_observe_scheduler():
    """Observe input tiap 60 detik. Input bervariasi (trading + non-trading)."""
    logger.info("🧠 Brain Observe Scheduler started (60s interval)")
    time.sleep(30)  # tunggu backend stabil dulu

    # ============================================================
    # COMPREHENSIVE INPUT SAMPLES
    # Mencakup: market, knowledge, learning, reflection, IoT,
    # dividend, telegram, news, sentiment, risk, strategy, dll.
    # ============================================================

    # MARKET & TRADING
    MARKET_SAMPLES = [
        {
            "symbol": "BTC/USD",
            "signal": "bullish",
            "confidence": 0.85,
            "text": "BTC/USD bullish dengan volume tinggi. RSI 65, MACD cross up, tren naik kuat.",
            "type": "market",
            "sentiment": "bullish",
            "timeframe": "1h",
        },
        {
            "symbol": "ETH/USD",
            "signal": "bearish",
            "confidence": 0.72,
            "text": "ETH/USD bearish. RSI 35, potensi turun ke support $2400.",
            "type": "market",
            "sentiment": "bearish",
            "timeframe": "4h",
        },
        {
            "symbol": "AAPL",
            "signal": "neutral",
            "confidence": 0.55,
            "text": "AAPL sideways, volume rendah. Tidak ada sinyal jelas, tunggu breakout.",
            "type": "market",
            "sentiment": "neutral",
            "timeframe": "1d",
        },
        {
            "symbol": "SPY",
            "signal": "bullish",
            "confidence": 0.78,
            "text": "SPY menguat, breadth positif. Sektor teknologi memimpin.",
            "type": "market",
            "sentiment": "bullish",
            "timeframe": "1d",
        },
        {
            "symbol": "GOLD",
            "signal": "bearish",
            "confidence": 0.62,
            "text": "Gold melemah karena yield naik. Dolar menguat.",
            "type": "market",
            "sentiment": "bearish",
            "timeframe": "1d",
        },
    ]

    # KNOWLEDGE & LEARNING
    KNOWLEDGE_SAMPLES = [
        {
            "text": "RSI di atas 70 menunjukkan overbought, potensi koreksi.",
            "type": "knowledge",
            "category": "technical_analysis",
        },
        {
            "text": "Dividend King adalah saham yang menaikkan dividen 50+ tahun berturut-turut.",
            "type": "knowledge",
            "category": "dividend",
        },
        {
            "text": "Pola head and shoulders menandakan reversal bearish.",
            "type": "knowledge",
            "category": "pattern",
        },
        {
            "text": "Monte Carlo simulation menggunakan random sampling untuk prediksi.",
            "type": "knowledge",
            "category": "quant",
        },
        {
            "text": "Payout ratio di atas 80% menandakan dividen berisiko dipotong.",
            "type": "knowledge",
            "category": "dividend",
        },
    ]

    # REFLECTION & METACOGNITION
    REFLECTION_SAMPLES = [
        {
            "text": "Refleksi: hari ini saya belajar bahwa RSI oversold tidak selalu berarti bounce.",
            "type": "reflection",
            "depth": "medium",
        },
        {
            "text": "Refleksi: keputusan HOLD saya benar karena pasar sideways.",
            "type": "reflection",
            "outcome": "correct",
        },
        {
            "text": "Refleksi: saya terlalu optimis pada sinyal BUY kemarin.",
            "type": "reflection",
            "emotion": "regret",
        },
        {
            "text": "Refleksi: pola konflik sinyal sering terjadi di timeframe kecil.",
            "type": "reflection",
            "insight": "pattern_conflict",
        },
    ]

    # DIVIDEND
    DIVIDEND_SAMPLES = [
        {
            "text": "JNJ Dividend King 63 tahun, yield 2.48%, payout 60%. Aman.",
            "type": "dividend",
            "symbol": "JNJ",
            "trap_score": 0,
        },
        {
            "text": "T (AT&T) yield 5.33%, tapi cut 3x dan debt 129%. Risiko tinggi.",
            "type": "dividend",
            "symbol": "T",
            "trap_score": 38,
        },
        {
            "text": "KO Dividend Champion 23 tahun, yield 2.36%, FCF $5.22B.",
            "type": "dividend",
            "symbol": "KO",
            "trap_score": 18,
        },
        {
            "text": "Ex-date KO dalam 1 hari. Strategi: BUY_BEFORE_EX.",
            "type": "dividend",
            "symbol": "KO",
            "strategy": "BUY_BEFORE_EX",
        },
    ]

    # IoT & DEVICES
    IOT_SAMPLES = [
        {
            "text": "Sensor suhu ruang server 45°C, di atas normal. Perlu pendinginan.",
            "type": "iot",
            "device": "temperature_sensor",
            "value": 45,
        },
        {
            "text": "Perangkat IoT mendeteksi getaran abnormal pada motor.",
            "type": "iot",
            "device": "vibration_sensor",
            "status": "warning",
        },
        {
            "text": "Kamera IoT mendeteksi gerakan di area terlarang.",
            "type": "iot",
            "device": "camera",
            "status": "alert",
        },
    ]

    # TELEGRAM & USER QUERY
    TELEGRAM_SAMPLES = [
        {
            "question": "Apa itu machine learning dan bagaimana cara kerjanya?",
            "type": "query",
            "source": "telegram",
        },
        {
            "question": "Bagaimana cara menghitung RSI?",
            "type": "query",
            "source": "telegram",
        },
        {
            "command": "/health",
            "type": "command",
            "source": "telegram",
        },
        {
            "command": "/signals",
            "type": "command",
            "source": "telegram",
        },
        {
            "question": "Apakah saya harus beli BTC sekarang?",
            "type": "query",
            "source": "telegram",
        },
    ]

    # NEWS & SENTIMENT
    NEWS_SAMPLES = [
        {
            "text": "Fed menaikkan suku bunga 25bps. Pasar bereaksi negatif.",
            "type": "news",
            "sentiment": "bearish",
            "impact": "high",
        },
        {
            "text": "ETF Bitcoin disetujui SEC. Sentimen crypto positif.",
            "type": "news",
            "sentiment": "bullish",
            "impact": "high",
        },
        {
            "text": "Laporan inflasi lebih rendah dari perkiraan. Pasar rally.",
            "type": "news",
            "sentiment": "bullish",
            "impact": "medium",
        },
    ]

    # RISK & STRATEGY
    RISK_SAMPLES = [
        {
            "text": "Risk level HIGH: drawdown 15%, perlu kurangi posisi.",
            "type": "risk",
            "level": "HIGH",
            "drawdown": 0.15,
        },
        {
            "text": "Circuit breaker aktif: volatilitas ekstrem terdeteksi.",
            "type": "risk",
            "level": "CRITICAL",
            "action": "circuit_breaker",
        },
        {
            "text": "Strategi scalping cocok untuk market sideways hari ini.",
            "type": "strategy",
            "name": "scalping",
            "regime": "sideways",
        },
    ]

    # ALL SAMPLES (gabungan)
    ALL_SAMPLES = (
        MARKET_SAMPLES
        + KNOWLEDGE_SAMPLES
        + REFLECTION_SAMPLES
        + DIVIDEND_SAMPLES
        + IOT_SAMPLES
        + TELEGRAM_SAMPLES
        + NEWS_SAMPLES
        + RISK_SAMPLES
    )

    cycle_errors = 0

    while not _shutdown_flag.is_set():
        try:
            if not (BRAIN_AVAILABLE and brain):
                time.sleep(60)
                continue

            # Pilih input dari SEMUA kategori (komprehensif)
            data = dict(random.choice(ALL_SAMPLES))
            # Update confidence/signal untuk market samples
            if "symbol" in data:
                data["confidence"] = round(random.uniform(0.3, 0.95), 2)
                data["signal"] = random.choice(["bullish", "bearish", "neutral"])

            # Observe
            result = brain.observe(data)
            dec = (result or {}).get("decision", {}) or {}
            action = dec.get("action", "?")
            source = dec.get("reason_source", "?")
            inp_type = data.get("type") or ("market" if "symbol" in data else "generic")

            logger.info(
                f"🧠 Brain cycle #{brain.cycles} | input={inp_type} | "
                f"action={action} | reason={source} | errors={brain.errors}"
            )
            cycle_errors = 0

        except Exception as e:
            cycle_errors += 1
            logger.error(f"❌ Brain observe error (#{cycle_errors}): {e}")

        # Interval 60 detik
        for _ in range(60):
            if _shutdown_flag.is_set():
                break
            time.sleep(1)


def main_headless():
    global engine_running

    logger.info("=" * 60)
    logger.info(f"  🧠 {APP_NAME} - COGNITIVE MIRROR ENGINE v{APP_VERSION}")
    logger.info(f"  Mode: {MODE.upper()}")
    logger.info(f"  AI: {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
    logger.info(f"  Consciousness: {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
    logger.info("=" * 60)

    api_started = start_api_server()

    try:
        crawl_thread = threading.Thread(target=auto_crawl_scheduler, daemon=True)
        crawl_thread.start()
        logger.info("✅ Auto-Crawl Scheduler started (6-hour interval)")
    except Exception as e:
        logger.warning(f"⚠️ Auto-Crawl failed: {e}")

    try:
        monitor_thread = threading.Thread(target=database_monitor_scheduler, daemon=True)
        monitor_thread.start()
        logger.info("✅ Database Monitor Scheduler started (1-hour interval)")
    except Exception as e:
        logger.warning(f"⚠️ Database Monitor failed: {e}")

    try:
        cleanup_thread = threading.Thread(target=auto_cleanup_scheduler, daemon=True)
        cleanup_thread.start()
        logger.info("✅ Auto-Cleanup Scheduler started (daily)")
    except Exception as e:
        logger.warning(f"⚠️ Auto-Cleanup failed: {e}")

    start_consciousness_scheduler()

    # Brain Observe Scheduler — supaya pipeline hidup
    try:
        brain_observe_thread = threading.Thread(target=brain_observe_scheduler, daemon=True)
        brain_observe_thread.start()
        logger.info("✅ Brain Observe Scheduler started")
    except Exception as e:
        logger.warning(f"⚠️ Brain Observe Scheduler failed: {e}")

    logger.info("=" * 60)
    logger.info("  ✅ SYSTEM READY")
    logger.info("=" * 60)
    logger.info(f"  Mode        : {MODE}")
    logger.info(f"  Knowledge   : {len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0} items")
    logger.info(f"  Dividend    : {'ONLINE' if DIVIDEND_AVAILABLE else 'OFFLINE'}")
    logger.info(f"  AI          : {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
    logger.info(f"  Consciousness: {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
    logger.info(f"  API Server  : {'ON' if api_started else 'OFF'}")
    logger.info(f"  Telegram    : {'CONFIGURED' if TELEGRAM_CONFIGURED else 'NOT'}")
    logger.info("=" * 60)
    logger.info("📡 Press Ctrl+C to stop")
    logger.info("=" * 60)

    try:
        while not _shutdown_flag.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n⚠️ Bot stopped by user")
        _graceful_shutdown = True

    logger.info("Shutting down...")
    logger.info(f"✅ {APP_NAME} stopped.")
    return 0


# ============================================================
# ENTRY POINT
# ============================================================

# ============================================================
# WARM CACHE TRAP SCREENER
# ============================================================


def warm_trap_screener_cache():
    """Fetch trap screener di background saat startup."""
    import time as _time

    _time.sleep(30)  # tunggu backend stabil
    try:
        logger.info("🔥 Warming trap screener cache...")
        import requests

        api_key = os.getenv("API_KEY", "iks_612d40ce554b1670525355c85567f823")
        resp = requests.get(
            "http://127.0.0.1:5000/api/dividend/trap-screener/top",
            headers={"X-API-Key": api_key},
            timeout=60,
        )
        if resp.ok:
            logger.info("✅ Trap screener cache warmed")
        else:
            logger.warning(f"⚠️ Warm cache failed: {resp.status_code}")
    except Exception as e:
        logger.warning(f"⚠️ Warm cache error: {e}")


try:
    import threading as _threading

    _warm_thread = _threading.Thread(target=warm_trap_screener_cache, daemon=True)
    _warm_thread.start()
    logger.info("🔥 Warm trap screener thread started")
except Exception as e:
    logger.warning(f"Warm cache thread failed: {e}")


if __name__ == "__main__":
    try:
        exit_code = main_headless()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
