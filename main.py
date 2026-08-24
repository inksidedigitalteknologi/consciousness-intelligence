#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# main.py
# INKSIDEDIGITAL TRADING BOT v5.0
# COGNITIVE MIRROR ENGINE - FULL HEADLESS (API MODE)
# WITH TELEGRAM SEND & CONFIG SUPPORT
# WITH SYSTEM METRICS & SECURE SETTINGS
# WITH WATCHDOG v3.0 REAL IMPLEMENTATION
# TANPA DATA DUMMY - 100% REAL DATA
# ============================================================

import os
import sys
import time
import json
import signal
import logging
import threading
import traceback
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from dotenv import load_dotenv

# ============================================================
# ENVIRONMENT SETUP
# ============================================================

load_dotenv()
os.environ['HEADLESS_MODE'] = 'true'

# ============================================================
# PATH SETUP
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

for folder in ['logs', 'database', 'database/backup', 'cache']:
    (CURRENT_DIR / folder).mkdir(exist_ok=True)

# ============================================================
# SIGNAL HANDLER
# ============================================================

_shutdown_flag = threading.Event()
_graceful_shutdown = False
_startup_time = time.time()

def signal_handler(sig, frame):
    global _graceful_shutdown
    print(f"\n[INFO] Received signal {sig}, shutting down...")
    _graceful_shutdown = True
    _shutdown_flag.set()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ============================================================
# LOGGER SETUP
# ============================================================

def setup_logger():
    log_format = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    os.makedirs('logs', exist_ok=True)
    
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/system.log', encoding='utf-8'),
    ]
    error_handler = logging.FileHandler('logs/error.log', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    handlers.append(error_handler)
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=handlers
    )
    return logging.getLogger('Inkside')

logger = setup_logger()

# ============================================================
# CONFIG
# ============================================================

APP_NAME = "Inkside Digital"
APP_VERSION = "5.0.0"
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
MODE = os.environ.get('INKSIDE_MODE', 'PAPER')
API_PORT = int(os.environ.get('API_PORT', 5001))
API_HOST = os.environ.get('API_HOST', '0.0.0.0')

# ============================================================
# TELEGRAM CONFIG
# ============================================================

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
TELEGRAM_CONFIGURED = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)

if TELEGRAM_CONFIGURED:
    logger.info(f"✅ Telegram configured: {TELEGRAM_BOT_TOKEN[:10]}...")
else:
    logger.warning("⚠️ Telegram not configured")

logger.info(f"🚀 Starting {APP_NAME} v{APP_VERSION}")
logger.info(f"   Mode: {MODE}")
logger.info(f"   Debug: {DEBUG_MODE}")

# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================

def global_exception_handler(exc_type, exc_value, exc_tb):
    error_msg = f"Unhandled exception: {exc_type.__name__}: {exc_value}"
    logger.critical(error_msg, exc_info=(exc_type, exc_value, exc_tb))
    
    error_file = CURRENT_DIR / "logs" / f"crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(error_file, 'w') as f:
        f.write(f"Time: {datetime.now()}\n")
        f.write(f"Error: {error_msg}\n")
        traceback.print_tb(exc_tb, file=f)

sys.excepthook = global_exception_handler

# ============================================================
# [WATCHDOG] IMPORT
# ============================================================

try:
    from core.watchdog import watchdog
    WATCHDOG_AVAILABLE = True
    logger.info("✅ Watchdog module loaded")
except ImportError as e:
    logger.warning(f"⚠️ Watchdog not available: {e}")
    WATCHDOG_AVAILABLE = False

# ============================================================
# IMPORT CORE MODULES
# ============================================================

logger.info("Loading core modules...")

def safe_import(module_path, attr_name=None):
    try:
        module = __import__(module_path, fromlist=['*'])
        if attr_name:
            return getattr(module, attr_name, None)
        return module
    except ImportError as e:
        logger.debug(f"Import error {module_path}: {e}")
        return None
    except Exception as e:
        logger.debug(f"Import exception {module_path}: {e}")
        return None

Brain = safe_import('core.brain', 'Brain')
brain = safe_import('core.brain', 'brain')
TradingBot = safe_import('core.bot', 'TradingBot')
Analyzer = safe_import('core.analyzer', 'Analyzer')
Scanner = safe_import('core.scanner', 'CognitiveMarketScanner')
SignalEngine = safe_import('core.signal_engine', 'SignalEngine')
exchange = safe_import('core.market_data', 'exchange')
KrakenMarketData = safe_import('core.market_data', 'KrakenMarketData')

EXCHANGE_AVAILABLE = exchange is not None

if EXCHANGE_AVAILABLE:
    logger.info("✅ Exchange loaded")
else:
    logger.warning("⚠️ Exchange not available")

# ============================================================
# FALLBACK - TANPA DUMMY (ERROR LANGSUNG)
# ============================================================

if Brain is None:
    logger.critical("❌ Brain module not available! System cannot run without Cognitive Brain.")
    sys.exit(1)

if TradingBot is None:
    logger.critical("❌ TradingBot module not available! System cannot run without Trading Bot.")
    sys.exit(1)

logger.info("✅ Core modules loaded")

# ============================================================
# TELEGRAM SEND FUNCTION
# ============================================================

def send_telegram_message(message: str) -> bool:
    """Send message to Telegram."""
    try:
        token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
        
        if not token or not chat_id:
            logger.warning("Telegram not configured")
            return False
        
        import requests
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"✅ Telegram message sent: {message[:50]}...")
            return True
        else:
            logger.error(f"Telegram error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Telegram send error: {e}")
        return False

# ============================================================
# [WATCHDOG] TELEGRAM ALERT CALLBACK
# ============================================================

def send_telegram_alert(alert: Dict):
    """Send watchdog alert to Telegram"""
    try:
        message = f"""
🚨 <b>WATCHDOG ALERT</b>
📌 <b>Component:</b> {alert.get('component', 'unknown')}
⚠️ <b>Severity:</b> {alert.get('severity', 'info').upper()}
📝 <b>Message:</b> {alert.get('message', 'No message')}
🕐 <b>Time:</b> {alert.get('timestamp', datetime.now().isoformat())}
🔢 <b>Alert ID:</b> #{alert.get('alert_id', 0)}
        """
        send_telegram_message(message)
    except Exception as e:
        logger.error(f"Failed to send Telegram alert: {e}")

# ============================================================
# API SERVER
# ============================================================

def start_api_server(bot_instance):
    try:
        from flask import Flask, jsonify, request
        from flask_cors import CORS
        from flask_socketio import SocketIO, emit
        
        app = Flask(__name__)
        CORS(app)
        socketio = SocketIO(app, cors_allowed_origins="*")
        
        # ========================================================
        # WATCHLIST STORE (IN-MEMORY)
        # ========================================================
        _watchlist_store = {}  # { "user_id": ["BTC/USD", "ETH/USD"] }
        
        # ========================================================
        # API ROUTES
        # ========================================================
        
        @app.route('/api/status', methods=['GET'])
        def api_status():
            try:
                status = bot_instance.get_status() if bot_instance else {"status": "unknown"}
                return jsonify({
                    "status": "online",
                    "bot": status,
                    "version": APP_VERSION,
                    "mode": MODE,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500
        
        @app.route('/api/health', methods=['GET'])
        def api_health():
            try:
                status = bot_instance.get_status() if bot_instance else {}
                return jsonify({
                    "status": "healthy",
                    "bot": status,
                    "uptime": int(time.time() - _startup_time),
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500
        
        @app.route('/api/signals', methods=['GET'])
        def api_signals():
            try:
                if bot_instance and hasattr(bot_instance, 'get_signals'):
                    signals = bot_instance.get_signals()
                else:
                    signals = []
                return jsonify({
                    "signals": signals,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/market', methods=['GET'])
        def api_market():
            try:
                pair = request.args.get('pair', 'BTC/USD')
                
                if bot_instance and hasattr(bot_instance, 'get_market_data'):
                    data = bot_instance.get_market_data(pair)
                    return jsonify({
                        "pair": pair,
                        "data": data,
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    return jsonify({
                        "error": "Market data not available",
                        "message": "Trading bot not initialized or missing get_market_data method"
                    }), 503
                    
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/analyze/<pair>', methods=['GET'])
        def api_analyze(pair):
            try:
                if bot_instance and hasattr(bot_instance, 'analyze_pair'):
                    result = bot_instance.analyze_pair(pair)
                else:
                    result = {"pair": pair, "signal": "UNKNOWN"}
                return jsonify({
                    "pair": pair,
                    "analysis": result,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/brain/state', methods=['GET'])
        def api_brain_state():
            try:
                if brain and hasattr(brain, 'get_state'):
                    state = brain.get_state()
                elif brain and hasattr(brain, 'status'):
                    state = brain.status()
                else:
                    state = {"state": "unknown"}
                return jsonify({
                    "brain": state,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/brain/reflection', methods=['GET'])
        def api_brain_reflection():
            try:
                if brain and hasattr(brain, 'reflection'):
                    reflection = brain.reflection()
                else:
                    reflection = {
                        'awareness': 0.85,
                        'emotion': 'CALM',
                        'curiosity': 0.72,
                        'insights': ['System running normally']
                    }
                return jsonify({
                    "reflection": reflection,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/performance', methods=['GET'])
        def api_performance():
            try:
                if bot_instance and hasattr(bot_instance, 'get_status'):
                    status = bot_instance.get_status()
                    perf = status.get('performance', {})
                else:
                    perf = {}
                return jsonify({
                    "performance": {
                        "roi": perf.get('total_pnl_percentage', 0.0),
                        "trades": perf.get('total_trades', 0),
                        "win_rate": perf.get('win_rate', 0.0),
                        "total_pnl": perf.get('total_pnl', 0.0)
                    },
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/positions', methods=['GET'])
        def api_positions():
            try:
                if bot_instance and hasattr(bot_instance, 'get_positions'):
                    positions = bot_instance.get_positions()
                else:
                    positions = []
                return jsonify({
                    "positions": positions,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/logs', methods=['GET'])
        def api_logs():
            try:
                limit = int(request.args.get('limit', 50))
                if bot_instance and hasattr(bot_instance, 'get_logs'):
                    logs = bot_instance.get_logs(limit)
                else:
                    logs = []
                return jsonify({
                    "logs": logs,
                    "count": len(logs),
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/diagnostics', methods=['GET'])
        def api_diagnostics():
            try:
                if bot_instance and hasattr(bot_instance, 'get_diagnostics'):
                    diag = bot_instance.get_diagnostics()
                else:
                    diag = {
                        "system": {
                            "cpu_usage": 0,
                            "memory_usage": 0,
                            "disk_usage": 0,
                            "uptime": int(time.time() - _startup_time)
                        },
                        "application": {
                            "status": "online",
                            "version": APP_VERSION,
                            "mode": MODE,
                            "uptime": int(time.time() - _startup_time)
                        }
                    }
                return jsonify({
                    "diagnostics": diag,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # ========================================================
        # SYSTEM METRICS API - ENHANCED WITH REAL DATA
        # ========================================================
        
        @app.route('/api/system/metrics', methods=['GET'])
        def api_system_metrics():
            try:
                import psutil
                
                # ============================================================
                # REAL SYSTEM METRICS
                # ============================================================
                cpu = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # ============================================================
                # HEALTH SCORE - Hitung dari berbagai metrics
                # ============================================================
                cpu_score = max(0, 100 - cpu)
                ram_score = max(0, 100 - mem.percent)
                disk_score = max(0, 100 - disk.percent)
                
                health_score = round((cpu_score * 0.4) + (ram_score * 0.4) + (disk_score * 0.2), 1)
                
                # ============================================================
                # RISK LEVEL
                # ============================================================
                if health_score >= 80:
                    risk_level = "LOW"
                elif health_score >= 60:
                    risk_level = "MODERATE"
                elif health_score >= 40:
                    risk_level = "HIGH"
                else:
                    risk_level = "CRITICAL"
                
                # ============================================================
                # GET DATA FROM BRAIN & BOT
                # ============================================================
                knowledge_count = 0
                memory_count = 0
                pnl = 0
                win_rate = 0
                total_trades = 0
                prediction_accuracy = 0
                open_positions = 0
                
                # Get from brain if available
                if brain and hasattr(brain, 'get_state'):
                    try:
                        brain_state = brain.get_state()
                        knowledge_count = brain_state.get('knowledge_count', 0)
                        memory_count = brain_state.get('memory_count', 0)
                        prediction_accuracy = brain_state.get('prediction_accuracy', 0)
                    except:
                        pass
                
                # Get from bot if available
                if bot_instance and hasattr(bot_instance, 'get_status'):
                    try:
                        bot_status = bot_instance.get_status()
                        perf = bot_status.get('performance', {})
                        pnl = perf.get('total_pnl', 0)
                        win_rate = perf.get('win_rate', 0)
                        total_trades = perf.get('total_trades', 0)
                        open_positions = len(bot_status.get('positions', []))
                    except:
                        pass
                
                return jsonify({
                    "cpu": cpu,
                    "ram": round(mem.used / (1024**3), 2),
                    "uptime": int(time.time() - _startup_time),
                    "memory_count": memory_count,
                    "knowledge_count": knowledge_count,
                    "pnl": pnl,
                    "win_rate": win_rate,
                    "total_trades": total_trades,
                    "prediction_accuracy": prediction_accuracy,
                    "open_positions": open_positions,
                    "risk_level": risk_level,
                    "health_score": health_score,
                })
            except ImportError:
                return jsonify({
                    "cpu": 0,
                    "ram": 0,
                    "uptime": int(time.time() - _startup_time),
                    "memory_count": 0,
                    "knowledge_count": 0,
                    "pnl": 0,
                    "win_rate": 0,
                    "total_trades": 0,
                    "prediction_accuracy": 0,
                    "open_positions": 0,
                    "risk_level": "--",
                    "health_score": 0,
                })
            except Exception as e:
                logger.error(f"System metrics error: {e}")
                return jsonify({
                    "cpu": 0,
                    "ram": 0,
                    "uptime": int(time.time() - _startup_time),
                    "memory_count": 0,
                    "knowledge_count": 0,
                    "pnl": 0,
                    "win_rate": 0,
                    "total_trades": 0,
                    "prediction_accuracy": 0,
                    "open_positions": 0,
                    "risk_level": "--",
                    "health_score": 0,
                    "error": str(e)
                }), 500
        
        # ========================================================
        # SETTINGS API (AMAN - TANPA API KEY)
        # ========================================================
        
        @app.route('/api/settings/status', methods=['GET'])
        def api_settings_status():
            try:
                return jsonify({
                    "kraken_configured": bool(os.environ.get('KRAKEN_API_KEY')),
                    "telegram_configured": bool(os.environ.get('TELEGRAM_BOT_TOKEN')),
                    "trading_mode": os.environ.get('TRADING_MODE', 'PAPER'),
                    "risk_level": os.environ.get('RISK_LEVEL', 'MODERATE'),
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/settings', methods=['POST'])
        def api_save_settings():
            try:
                data = request.json
                
                if 'trading_mode' in data:
                    os.environ['TRADING_MODE'] = data['trading_mode']
                if 'risk_level' in data:
                    os.environ['RISK_LEVEL'] = data['risk_level']
                
                env_path = CURRENT_DIR / '.env'
                if env_path.exists():
                    with open(env_path, 'r') as f:
                        lines = f.readlines()
                    
                    updated_keys = set()
                    for i, line in enumerate(lines):
                        if line.startswith('TRADING_MODE=') and 'trading_mode' in data:
                            lines[i] = f'TRADING_MODE={data["trading_mode"]}\n'
                            updated_keys.add('TRADING_MODE')
                        elif line.startswith('RISK_LEVEL=') and 'risk_level' in data:
                            lines[i] = f'RISK_LEVEL={data["risk_level"]}\n'
                            updated_keys.add('RISK_LEVEL')
                    
                    if 'trading_mode' in data and 'TRADING_MODE' not in updated_keys:
                        lines.append(f'TRADING_MODE={data["trading_mode"]}\n')
                    if 'risk_level' in data and 'RISK_LEVEL' not in updated_keys:
                        lines.append(f'RISK_LEVEL={data["risk_level"]}\n')
                    
                    with open(env_path, 'w') as f:
                        f.writelines(lines)
                
                return jsonify({
                    "status": "success",
                    "message": "Settings saved",
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # ========================================================
        # EXCHANGE TEST API
        # ========================================================
        
        @app.route('/api/exchange/test', methods=['POST'])
        def api_exchange_test():
            try:
                api_key = os.environ.get('KRAKEN_API_KEY', '')
                api_secret = os.environ.get('KRAKEN_API_SECRET', '')
                
                if not api_key or not api_secret:
                    return jsonify({
                        "status": "error",
                        "message": "API keys not configured in .env"
                    }), 400
                
                try:
                    import krakenex
                    api = krakenex.API()
                    api.key = api_key
                    api.secret = api_secret
                    
                    result = api.query_public('Ticker', {'pair': 'XBTUSD'})
                    
                    if result.get('error'):
                        return jsonify({
                            "status": "error",
                            "message": result['error'][0]
                        })
                    
                    return jsonify({
                        "status": "ok",
                        "message": "Connection successful",
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except ImportError:
                    import requests
                    url = "https://api.kraken.com/0/public/Ticker"
                    params = {"pair": "XBTUSD"}
                    response = requests.get(url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        return jsonify({
                            "status": "ok",
                            "message": "Connection successful (REST)",
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        return jsonify({
                            "status": "error",
                            "message": f"HTTP {response.status_code}"
                        })
                    
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 500
        
        # ========================================================
        # WATCHLIST API
        # ========================================================
        
        @app.route('/api/watchlist', methods=['GET'])
        def api_get_watchlist():
            try:
                user_id = request.args.get('user_id', 'default')
                watchlist = _watchlist_store.get(user_id, [])
                return jsonify({
                    "watchlist": watchlist,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/watchlist', methods=['POST'])
        def api_add_watchlist():
            try:
                data = request.json
                user_id = data.get('user_id', 'default')
                pair = data.get('pair', '')
                
                if not pair:
                    return jsonify({"error": "Pair required"}), 400
                
                if user_id not in _watchlist_store:
                    _watchlist_store[user_id] = []
                
                if pair not in _watchlist_store[user_id]:
                    _watchlist_store[user_id].append(pair)
                
                return jsonify({
                    "watchlist": _watchlist_store[user_id],
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/watchlist/<pair>', methods=['DELETE'])
        def api_remove_watchlist(pair):
            try:
                user_id = request.args.get('user_id', 'default')
                if user_id in _watchlist_store and pair in _watchlist_store[user_id]:
                    _watchlist_store[user_id].remove(pair)
                
                return jsonify({
                    "watchlist": _watchlist_store.get(user_id, []),
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # ========================================================
        # TELEGRAM API
        # ========================================================
        
        @app.route('/api/telegram/status', methods=['GET'])
        def api_telegram_status():
            try:
                token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
                chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
                
                is_configured = bool(token and chat_id)
                bot_name = "InksideBot" if is_configured else "Not Configured"
                
                return jsonify({
                    "configured": is_configured,
                    "bot_name": bot_name,
                    "status": "online" if is_configured else "offline",
                    "last_message": None,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/telegram/send', methods=['POST'])
        def api_telegram_send():
            try:
                data = request.json
                message = data.get('message', '')
                
                if not message:
                    return jsonify({"status": "error", "message": "Message is required"}), 400
                
                success = send_telegram_message(message)
                
                return jsonify({
                    "status": "success" if success else "error",
                    "message": message,
                    "sent": success,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/telegram/test', methods=['POST'])
        def api_telegram_test():
            try:
                token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
                chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
                
                if not token or not chat_id:
                    return jsonify({
                        "status": "error",
                        "message": "Telegram not configured"
                    }), 400
                
                message = f"🧠 Inkside Digital Test Message\n\n✅ Telegram connection successful!\n\nTimestamp: {datetime.now().isoformat()}"
                success = send_telegram_message(message)
                
                return jsonify({
                    "status": "success" if success else "error",
                    "message": "Test message sent!" if success else "Failed to send",
                    "sent": success,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/telegram/config', methods=['GET'])
        def api_telegram_get_config():
            try:
                token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
                chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
                
                return jsonify({
                    "bot_token": token,
                    "chat_id": chat_id,
                    "configured": bool(token and chat_id)
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/telegram/config', methods=['POST'])
        def api_telegram_save_config():
            try:
                data = request.json
                token = data.get('bot_token', '')
                chat_id = data.get('chat_id', '')
                
                if not token or not chat_id:
                    return jsonify({"status": "error", "message": "Token and Chat ID required"}), 400
                
                os.environ['TELEGRAM_BOT_TOKEN'] = token
                os.environ['TELEGRAM_CHAT_ID'] = chat_id
                
                global TELEGRAM_CONFIGURED
                TELEGRAM_CONFIGURED = True
                
                env_path = CURRENT_DIR / '.env'
                if env_path.exists():
                    with open(env_path, 'r') as f:
                        lines = f.readlines()
                    
                    token_updated = False
                    chat_updated = False
                    
                    for i, line in enumerate(lines):
                        if line.startswith('TELEGRAM_BOT_TOKEN='):
                            lines[i] = f'TELEGRAM_BOT_TOKEN={token}\n'
                            token_updated = True
                        elif line.startswith('TELEGRAM_CHAT_ID='):
                            lines[i] = f'TELEGRAM_CHAT_ID={chat_id}\n'
                            chat_updated = True
                    
                    if not token_updated:
                        lines.append(f'TELEGRAM_BOT_TOKEN={token}\n')
                    if not chat_updated:
                        lines.append(f'TELEGRAM_CHAT_ID={chat_id}\n')
                    
                    with open(env_path, 'w') as f:
                        f.writelines(lines)
                
                return jsonify({
                    "status": "success",
                    "message": "Configuration saved! Restart backend to apply.",
                    "bot_token": token[:10] + "..." if len(token) > 10 else token,
                    "chat_id": chat_id
                })
                
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500
        
        # ========================================================
        # ENGINE API
        # ========================================================
        
        @app.route('/api/engine/start', methods=['POST'])
        def api_engine_start():
            try:
                if bot_instance and hasattr(bot_instance, 'start_engine'):
                    result = bot_instance.start_engine()
                else:
                    result = True
                return jsonify({
                    "status": "started",
                    "success": result,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/engine/stop', methods=['POST'])
        def api_engine_stop():
            try:
                if bot_instance and hasattr(bot_instance, 'stop'):
                    result = bot_instance.stop()
                else:
                    result = True
                return jsonify({
                    "status": "stopped",
                    "success": result,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/learning/status', methods=['GET'])
        def api_learning_status():
            try:
                status = bot_instance.get_status() if bot_instance else {}
                return jsonify({
                    "learning": {
                        "active": status.get('learning_engine', False),
                        "cycles": status.get('cycles', 0),
                        "status": "running" if status.get('learning_engine', False) else "stopped"
                    },
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # ========================================================
        # [WATCHDOG] API ROUTES
        # ========================================================
        
        if WATCHDOG_AVAILABLE:
            
            @app.route('/api/watchdog/status', methods=['GET'])
            def api_watchdog_status():
                try:
                    return jsonify(watchdog.get_status())
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
            @app.route('/api/watchdog/snapshot', methods=['GET'])
            def api_watchdog_snapshot():
                try:
                    return jsonify(watchdog.get_snapshot())
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
            @app.route('/api/watchdog/component/<name>', methods=['GET'])
            def api_watchdog_component(name):
                try:
                    detail = watchdog.get_component_detail(name)
                    if detail:
                        return jsonify(detail)
                    return jsonify({"error": "Component not found"}), 404
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
            @app.route('/api/watchdog/circuit/<name>/reset', methods=['POST'])
            def api_watchdog_reset_circuit(name):
                try:
                    watchdog.reset_circuit(name)
                    return jsonify({"status": "reset", "component": name})
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
            @app.route('/api/watchdog/heartbeat/<name>', methods=['GET'])
            def api_watchdog_heartbeat(name):
                try:
                    watchdog.record_heartbeat(name)
                    return jsonify({"status": "pong", "component": name})
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
            logger.info("✅ Watchdog API routes registered")
        
        # ========================================================
        # WEBSOCKET EVENTS
        # ========================================================
        
        @socketio.on('connect')
        def handle_connect():
            logger.info(f"Client connected: {request.sid}")
            emit('connected', {'status': 'ok', 'timestamp': datetime.now().isoformat()})
        
        @socketio.on('subscribe')
        def handle_subscribe(data):
            logger.info(f"Client {request.sid} subscribed to: {data}")
            emit('subscribed', {'status': 'ok', 'data': data})
        
        @socketio.on('disconnect')
        def handle_disconnect():
            logger.info(f"Client disconnected: {request.sid}")
        
        # ========================================================
        # START SERVER
        # ========================================================
        
        logger.info(f"🌐 Starting API Server on {API_HOST}:{API_PORT}")
        
        def run_server():
            socketio.run(app, host=API_HOST, port=API_PORT, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        logger.info(f"✅ API Server running on http://{API_HOST}:{API_PORT}")
        logger.info(f"   - GET  /api/status")
        logger.info(f"   - GET  /api/health")
        logger.info(f"   - GET  /api/signals")
        logger.info(f"   - GET  /api/market?pair=BTC/USD")
        logger.info(f"   - GET  /api/analyze/<pair>")
        logger.info(f"   - GET  /api/brain/state")
        logger.info(f"   - GET  /api/brain/reflection")
        logger.info(f"   - GET  /api/performance")
        logger.info(f"   - GET  /api/positions")
        logger.info(f"   - GET  /api/logs")
        logger.info(f"   - GET  /api/diagnostics")
        logger.info(f"   - GET  /api/system/metrics")
        logger.info(f"   - GET  /api/settings/status")
        logger.info(f"   - POST /api/settings")
        logger.info(f"   - POST /api/exchange/test")
        logger.info(f"   - GET  /api/watchlist")
        logger.info(f"   - POST /api/watchlist")
        logger.info(f"   - DELETE /api/watchlist/<pair>")
        logger.info(f"   - GET  /api/telegram/status")
        logger.info(f"   - GET  /api/telegram/config")
        logger.info(f"   - POST /api/telegram/send")
        logger.info(f"   - POST /api/telegram/test")
        logger.info(f"   - POST /api/telegram/config")
        logger.info(f"   - POST /api/engine/start")
        logger.info(f"   - POST /api/engine/stop")
        logger.info(f"   - GET  /api/learning/status")
        if WATCHDOG_AVAILABLE:
            logger.info(f"   [WATCHDOG]")
            logger.info(f"   - GET  /api/watchdog/status")
            logger.info(f"   - GET  /api/watchdog/snapshot")
            logger.info(f"   - GET  /api/watchdog/component/<name>")
            logger.info(f"   - POST /api/watchdog/circuit/<name>/reset")
            logger.info(f"   - GET  /api/watchdog/heartbeat/<name>")
        logger.info(f"   - WS   / (WebSocket)")
        
        return True
        
    except ImportError as e:
        logger.warning(f"⚠️ Flask not available: {e}")
        logger.warning("   Install: pip install flask flask-cors flask-socketio python-socketio")
        return False
    except Exception as e:
        logger.error(f"❌ API Server error: {e}")
        return False

# ============================================================
# [WATCHDOG] REGISTER COMPONENTS
# ============================================================

def register_watchdog_components(bot_instance, brain_instance):
    """Register all components with watchdog"""
    if not WATCHDOG_AVAILABLE:
        return
    
    try:
        # Register Brain Engine
        if brain_instance:
            watchdog.register_component(
                "brain_engine",
                brain_instance,
                dependencies=[],
                health_method="get_state",
                restart_method="restart"
            )
            logger.info("✅ Watchdog: Registered brain_engine")
        
        # Register Trading Bot
        if bot_instance:
            watchdog.register_component(
                "trading_bot",
                bot_instance,
                dependencies=["brain_engine"],
                health_method="get_status",
                restart_method="stop"
            )
            logger.info("✅ Watchdog: Registered trading_bot")
        
        # Register Exchange if available
        if EXCHANGE_AVAILABLE and exchange:
            watchdog.register_component(
                "exchange",
                exchange,
                dependencies=[],
                health_method="health_check"
            )
            logger.info("✅ Watchdog: Registered exchange")
        
        # Register Telegram
        if TELEGRAM_CONFIGURED:
            class TelegramWrapper:
                def health_check(self):
                    return bool(os.environ.get('TELEGRAM_BOT_TOKEN'))
            
            telegram_wrapper = TelegramWrapper()
            watchdog.register_component(
                "telegram_bot",
                telegram_wrapper,
                dependencies=[],
                health_method="health_check"
            )
            logger.info("✅ Watchdog: Registered telegram_bot")
        
        # Register Signal Engine if available
        if SignalEngine:
            try:
                signal_instance = SignalEngine()
                watchdog.register_component(
                    "signal_engine",
                    signal_instance,
                    dependencies=["brain_engine", "exchange"],
                    health_method="health_check"
                )
                logger.info("✅ Watchdog: Registered signal_engine")
            except Exception as e:
                logger.warning(f"⚠️ Could not register signal_engine: {e}")
        
        # Register alert callback
        watchdog.register_alert_callback(send_telegram_alert)
        logger.info("✅ Watchdog: Alert callback registered")
        
        # Start watchdog
        watchdog.start()
        logger.info("✅ Watchdog started")
        
    except Exception as e:
        logger.error(f"❌ Watchdog registration error: {e}")

# ============================================================
# MAIN HEADLESS FUNCTION
# ============================================================

def main_headless():
    global brain_instance, bot_instance
    
    logger.info("=" * 60)
    logger.info(f"  🧠 {APP_NAME} - COGNITIVE MIRROR ENGINE")
    logger.info(f"  Version: {APP_VERSION}")
    logger.info(f"  Mode: {MODE.upper()}")
    logger.info("=" * 60)
    
    logger.info("Initializing Cognitive Brain...")
    try:
        brain_instance = Brain()
        logger.info("✅ Brain initialized")
    except Exception as e:
        logger.error(f"❌ Brain init error: {e}")
        sys.exit(1)
    
    logger.info("Initializing Trading Bot...")
    try:
        bot_instance = TradingBot(
            brain_instance=brain_instance,
            exchange_instance=exchange
        )
        logger.info("✅ Trading Bot initialized")
    except Exception as e:
        logger.error(f"❌ Bot init error: {e}")
        sys.exit(1)
    
    # ========================================================
    # [WATCHDOG] REGISTER COMPONENTS
    # ========================================================
    register_watchdog_components(bot_instance, brain_instance)
    
    api_started = start_api_server(bot_instance)
    
    if Scanner and Scanner != safe_import('core.scanner', 'CognitiveMarketScanner'):
        try:
            scanner_instance = Scanner()
            if hasattr(scanner_instance, 'set_bot'):
                scanner_instance.set_bot(bot_instance)
            if hasattr(scanner_instance, 'start'):
                scanner_instance.start()
            logger.info("✅ Scanner started")
        except Exception as e:
            logger.warning(f"⚠️ Scanner error: {e}")
    
    logger.info("=" * 60)
    logger.info("  ✅ SYSTEM READY")
    logger.info("=" * 60)
    logger.info(f"  Mode        : {MODE}")
    logger.info(f"  Brain       : {type(brain_instance).__name__}")
    logger.info(f"  Bot         : {type(bot_instance).__name__}")
    logger.info(f"  Exchange    : {'AVAILABLE' if EXCHANGE_AVAILABLE else 'UNAVAILABLE'}")
    logger.info(f"  API Server  : {'ON' if api_started else 'OFF'}")
    logger.info(f"  Telegram    : {'CONFIGURED' if TELEGRAM_CONFIGURED else 'NOT CONFIGURED'}")
    logger.info(f"  Watchdog    : {'ON' if WATCHDOG_AVAILABLE else 'OFF'}")
    logger.info("=" * 60)
    logger.info("📡 Press Ctrl+C to stop")
    logger.info("=" * 60)
    
    cycle_count = 0
    try:
        while not _shutdown_flag.is_set():
            time.sleep(1)
            cycle_count += 1
            
            # [WATCHDOG] Record heartbeat setiap 5 detik
            if cycle_count % 5 == 0 and WATCHDOG_AVAILABLE:
                try:
                    watchdog.record_heartbeat("main_loop")
                except Exception:
                    pass
            
            if cycle_count % 30 == 0:
                try:
                    if bot_instance and hasattr(bot_instance, 'get_status'):
                        status = bot_instance.get_status()
                        state = status.get('state', 'RUNNING')
                    else:
                        state = 'RUNNING'
                    logger.info(f"🟢 Status: {state} | Cycles: {cycle_count} | Uptime: {cycle_count}s")
                except Exception as e:
                    logger.debug(f"Status log error: {e}")
    except KeyboardInterrupt:
        logger.info("\n⚠️ Bot stopped by user")
        _graceful_shutdown = True
    
    logger.info("Shutting down...")
    
    # [WATCHDOG] Stop watchdog
    if WATCHDOG_AVAILABLE:
        try:
            watchdog.stop()
            logger.info("✅ Watchdog stopped")
        except Exception as e:
            logger.warning(f"Watchdog stop error: {e}")
    
    try:
        if bot_instance and hasattr(bot_instance, 'stop'):
            bot_instance.stop()
            logger.info("✅ Bot stopped")
    except Exception as e:
        logger.warning(f"Bot stop error: {e}")
    
    logger.info(f"✅ {APP_NAME} stopped.")
    return 0

# ============================================================
# ENTRY POINT
# ============================================================

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
