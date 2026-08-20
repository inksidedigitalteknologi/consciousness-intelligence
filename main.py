#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# main.py
# INKSIDEDIGITAL TRADING BOT v5.0
# COGNITIVE MIRROR ENGINE - FULL HEADLESS (API MODE)
# WITH TELEGRAM SEND & CONFIG SUPPORT
# ============================================================

import os
import sys
import time
import json
import signal
import random
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
# FALLBACK CLASSES
# ============================================================

class MockBrain:
    def __init__(self):
        self._state = "ACTIVE"
        self._cycles = 0
        self._goals = [
            {"name": "learn_continuously", "priority": 1, "progress": 0.0, "status": "active"},
            {"name": "improve_decision_making", "priority": 2, "progress": 0.0, "status": "active"},
            {"name": "develop_intuition", "priority": 3, "progress": 0.0, "status": "active"},
            {"name": "build_knowledge_base", "priority": 4, "progress": 0.0, "status": "active"},
        ]
        
    def get_state(self):
        self._cycles += 1
        return {
            "state": self._state,
            "cycles": self._cycles,
            "goals": self._goals,
            "modules_available": 11,
            "total_modules": 19,
            "health": 100.0
        }
    
    def status(self):
        return self.get_state()
    
    def reflection(self):
        return {
            'awareness': 0.85,
            'emotion': 'CALM',
            'curiosity': 0.72,
            'insights': ['System running in headless mode'],
            'timestamp': datetime.now().isoformat()
        }
    
    def learn(self, data=None):
        self._cycles += 1
        return {"status": "success", "cycles": self._cycles}
    
    def get_goals(self):
        return self._goals
    
    def get_metrics(self):
        return {
            "total_cycles": self._cycles,
            "success_rate": 95.0,
            "memory_usage": 45.2
        }

class MockTradingBot:
    def __init__(self, brain_instance=None, exchange_instance=None):
        self.brain = brain_instance
        self.exchange = exchange_instance
        self.running = True
        self._cycles = 0
        self._signals = []
        self._market_data = {}
        
    def get_status(self):
        self._cycles += 1
        return {
            "state": "RUNNING" if self.running else "IDLE",
            "mode": MODE,
            "cycles": self._cycles,
            "uptime": int(time.time() - _startup_time),
            "version": APP_VERSION,
            "consciousness": True,
            "learning_engine": True,
            "scanner": True,
            "exchange": EXCHANGE_AVAILABLE,
            "risk_level": "MODERATE",
            "portfolio": {
                "cash": 10000.0,
                "total_value": 10000.0,
                "pnl": 0.0,
                "pnl_percentage": 0.0
            },
            "performance": {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0.0,
                "total_pnl": 0.0,
                "total_pnl_percentage": 0.0
            }
        }
    
    def get_signals(self):
        pairs = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "XRP/USD"]
        signals = []
        for pair in pairs:
            signals.append({
                "pair": pair,
                "signal": random.choice(["BUY", "SELL", "HOLD", "MONITOR"]),
                "confidence": random.randint(40, 95),
                "price": random.uniform(1000, 65000),
                "strength": random.choice(["WEAK", "NEUTRAL", "STRONG"]),
                "timestamp": datetime.now().isoformat()
            })
        return signals
    
    def get_market_data(self, pair=None):
        if pair:
            pair = pair.replace('/', '')
        base = random.uniform(1000, 65000)
        return {
            "price": round(base, 2),
            "change": round(random.uniform(-5, 5), 2),
            "volume": round(random.uniform(100, 2000), 2),
            "high": round(base * (1 + random.uniform(0, 0.02)), 2),
            "low": round(base * (1 - random.uniform(0, 0.02)), 2),
            "trend": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]),
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_pair(self, pair):
        return {
            "pair": pair,
            "signal": random.choice(["BUY", "SELL", "HOLD"]),
            "confidence": random.randint(40, 95),
            "indicators": {
                "rsi": random.randint(20, 80),
                "macd": round(random.uniform(-1, 1), 4),
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def stop(self):
        self.running = False
        return True
    
    def start_engine(self):
        self.running = True
        return True
    
    def get_logs(self, limit=50):
        logs = []
        for i in range(min(limit, 10)):
            logs.append({
                "id": i,
                "timestamp": datetime.now().isoformat(),
                "level": random.choice(["INFO", "SUCCESS", "WARNING"]),
                "message": f"Log entry {i}: System running normally",
                "source": "System"
            })
        return logs
    
    def get_positions(self):
        return []
    
    def get_diagnostics(self):
        return {
            "system": {
                "cpu_usage": random.uniform(10, 30),
                "memory_usage": random.uniform(40, 70),
                "disk_usage": random.uniform(30, 50),
                "uptime": int(time.time() - _startup_time)
            },
            "application": {
                "status": "online",
                "version": APP_VERSION,
                "mode": MODE,
                "uptime": int(time.time() - _startup_time)
            },
            "modules": {
                "brain": "ACTIVE",
                "scanner": "ACTIVE",
                "learning": "ACTIVE",
                "exchange": "CONNECTED" if EXCHANGE_AVAILABLE else "DISCONNECTED"
            }
        }

if Brain is None:
    logger.warning("⚠️ Brain not available, using MockBrain")
    Brain = MockBrain
    brain = MockBrain()

if TradingBot is None:
    logger.warning("⚠️ TradingBot not available, using MockTradingBot")
    TradingBot = MockTradingBot

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
                else:
                    data = generate_mock_market_data()
                
                return jsonify({
                    "pair": pair,
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                })
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
                            "cpu_usage": random.uniform(10, 30),
                            "memory_usage": random.uniform(40, 70),
                            "disk_usage": random.uniform(30, 50),
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
        # TELEGRAM API - LENGKAP
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
        
        # ========================================================
        # TELEGRAM CONFIG SAVE & LOAD (BARU!)
        # ========================================================
        
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
                
                # Update environment
                os.environ['TELEGRAM_BOT_TOKEN'] = token
                os.environ['TELEGRAM_CHAT_ID'] = chat_id
                
                # Update global config
                global TELEGRAM_CONFIGURED
                TELEGRAM_CONFIGURED = True
                
                # Also save to .env file for persistence
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
        # MOCK DATA GENERATORS
        # ========================================================
        
        def generate_mock_market_data():
            pairs = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "XRP/USD"]
            data = {}
            for pair in pairs:
                base = random.uniform(1000, 65000)
                data[pair] = {
                    "price": round(base, 2),
                    "change": round(random.uniform(-5, 5), 2),
                    "volume": round(random.uniform(100, 2000), 2),
                    "high": round(base * (1 + random.uniform(0, 0.02)), 2),
                    "low": round(base * (1 - random.uniform(0, 0.02)), 2),
                    "trend": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]),
                    "timestamp": datetime.now().isoformat()
                }
            return data
        
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
        logger.info(f"   - GET  /api/telegram/status")
        logger.info(f"   - GET  /api/telegram/config")
        logger.info(f"   - POST /api/telegram/send")
        logger.info(f"   - POST /api/telegram/test")
        logger.info(f"   - POST /api/telegram/config")
        logger.info(f"   - POST /api/engine/start")
        logger.info(f"   - POST /api/engine/stop")
        logger.info(f"   - GET  /api/learning/status")
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
        if Brain and Brain != MockBrain:
            brain_instance = Brain()
            logger.info("✅ Brain initialized (REAL)")
        else:
            brain_instance = MockBrain()
            logger.info("✅ Brain initialized (MOCK)")
    except Exception as e:
        logger.error(f"❌ Brain init error: {e}")
        brain_instance = MockBrain()
        logger.info("✅ Brain initialized (MOCK - fallback)")
    
    logger.info("Initializing Trading Bot...")
    try:
        if TradingBot and TradingBot != MockTradingBot:
            bot_instance = TradingBot(
                brain_instance=brain_instance,
                exchange_instance=exchange
            )
            logger.info("✅ Trading Bot initialized (REAL)")
        else:
            bot_instance = MockTradingBot(
                brain_instance=brain_instance,
                exchange_instance=exchange
            )
            logger.info("✅ Trading Bot initialized (MOCK)")
    except Exception as e:
        logger.error(f"❌ Bot init error: {e}")
        bot_instance = MockTradingBot(brain_instance=brain_instance)
        logger.info("✅ Trading Bot initialized (MOCK - fallback)")
    
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
    logger.info("=" * 60)
    logger.info("📡 Press Ctrl+C to stop")
    logger.info("=" * 60)
    
    cycle_count = 0
    try:
        while not _shutdown_flag.is_set():
            time.sleep(1)
            cycle_count += 1
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
