
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# main.py
# INKSIDEDIGITAL TRADING BOT v5.0
# COGNITIVE MIRROR ENGINE - FULL HEADLESS (API MODE)
# WITH COLORED OUTPUT
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
# COLORAMA SETUP
# ============================================================

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    # Fallback jika colorama tidak terinstall
    class Fore:
        BLACK = ''; RED = ''; GREEN = ''; YELLOW = ''; BLUE = ''
        MAGENTA = ''; CYAN = ''; WHITE = ''; RESET = ''
        LIGHTBLACK_EX = ''; LIGHTRED_EX = ''; LIGHTGREEN_EX = ''
        LIGHTYELLOW_EX = ''; LIGHTBLUE_EX = ''; LIGHTMAGENTA_EX = ''
        LIGHTCYAN_EX = ''; LIGHTWHITE_EX = ''
    class Back:
        BLACK = ''; RED = ''; GREEN = ''; YELLOW = ''; BLUE = ''
        MAGENTA = ''; CYAN = ''; WHITE = ''; RESET = ''
    class Style:
        BRIGHT = ''; DIM = ''; NORMAL = ''; RESET_ALL = ''
    COLOR_ENABLED = False

# ============================================================
# COLOR FUNCTIONS
# ============================================================

def ctext(text, color='white', bold=False, bg=None):
    """Color text with fallback."""
    if not COLOR_ENABLED:
        return text
    
    color_map = {
        'black': Fore.BLACK, 'red': Fore.RED, 'green': Fore.GREEN,
        'yellow': Fore.YELLOW, 'blue': Fore.BLUE, 'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN, 'white': Fore.WHITE,
        'lightred': Fore.LIGHTRED_EX, 'lightgreen': Fore.LIGHTGREEN_EX,
        'lightyellow': Fore.LIGHTYELLOW_EX, 'lightblue': Fore.LIGHTBLUE_EX,
        'lightmagenta': Fore.LIGHTMAGENTA_EX, 'lightcyan': Fore.LIGHTCYAN_EX,
        'lightwhite': Fore.LIGHTWHITE_EX,
    }
    
    bg_map = {
        'black': Back.BLACK, 'red': Back.RED, 'green': Back.GREEN,
        'yellow': Back.YELLOW, 'blue': Back.BLUE, 'magenta': Back.MAGENTA,
        'cyan': Back.CYAN, 'white': Back.WHITE,
    }
    
    result = ''
    if bg and bg in bg_map:
        result += bg_map[bg]
    if color in color_map:
        result += color_map[color]
    if bold:
        result += Style.BRIGHT
    result += text
    result += Style.RESET_ALL
    return result

def cprint(text, color='white', bold=False, bg=None, end='\n'):
    """Print colored text."""
    print(ctext(text, color, bold, bg), end=end)

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

def signal_handler(sig, frame):
    global _graceful_shutdown
    cprint(f"\n[INFO] Received signal {sig}, shutting down...", 'yellow')
    _graceful_shutdown = True
    _shutdown_flag.set()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ============================================================
# LOGGER SETUP
# ============================================================

class ColoredFormatter(logging.Formatter):
    """Custom formatter dengan warna."""
    
    COLORS = {
        'DEBUG': Fore.LIGHTCYAN_EX,
        'INFO': Fore.LIGHTGREEN_EX,
        'WARNING': Fore.LIGHTYELLOW_EX,
        'ERROR': Fore.LIGHTRED_EX,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    
    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
        
        # Timestamp dim
        record.asctime = f"{Fore.LIGHTBLACK_EX}{self.formatTime(record)}{Style.RESET_ALL}"
        
        # Name dim
        record.name = f"{Fore.LIGHTBLACK_EX}{record.name}{Style.RESET_ALL}"
        
        return super().format(record)

def setup_logger():
    """Setup logger dengan warna."""
    log_format = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    
    os.makedirs('logs', exist_ok=True)
    
    # Console handler dengan warna
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter(log_format))
    
    # File handler tanpa warna
    file_handler = logging.FileHandler('logs/system.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Error file handler
    error_handler = logging.FileHandler('logs/error.log', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_format))
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler, error_handler]
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
# BANNER
# ============================================================

def print_banner():
    """Print colored banner."""
    cprint("\n" + "=" * 60, 'magenta', bold=True)
    cprint("", 'white')
    cprint("         🧠 INKSIDE DIGITAL", 'cyan', bold=True)
    cprint("   COGNITIVE MIRROR ENGINE v5.0", 'lightcyan')
    cprint("      HEADLESS SERVER MODE", 'lightcyan')
    cprint("", 'white')
    cprint("=" * 60, 'magenta', bold=True)
    cprint("", 'white')
    cprint(f"  System      : INITIALIZING", 'white')
    cprint(f"  Version     : {APP_VERSION}", 'lightmagenta')
    cprint(f"  Engine      : COGNITIVE MIRROR", 'white')
    cprint(f"  Exchange    : KRAKEN", 'yellow')
    cprint(f"  Mode        : {MODE.upper()}", 'green' if MODE == 'PAPER' else 'red')
    cprint(f"  Debug       : {DEBUG_MODE}", 'yellow')
    cprint("", 'white')
    cprint("=" * 60, 'magenta', bold=True)
    cprint("", 'white')

# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================

def global_exception_handler(exc_type, exc_value, exc_tb):
    error_msg = f"Unhandled exception: {exc_type.__name__}: {exc_value}"
    cprint(f"\n❌ {error_msg}", 'red', bold=True)
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

cprint("📡 Loading core modules...", 'cyan')

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
    cprint("✅ Exchange loaded", 'green')
else:
    cprint("⚠️ Exchange not available", 'yellow')

# ============================================================
# FALLBACK CLASSES
# ============================================================

class MockBrain:
    def __init__(self):
        self._state = "ACTIVE"
        self._cycles = 0
    def get_state(self):
        self._cycles += 1
        return {"state": self._state, "cycles": self._cycles}
    def status(self):
        return self.get_state()
    def reflection(self):
        return {'awareness': 0.85, 'emotion': 'CALM', 'curiosity': 0.72, 'insights': ['Headless mode'], 'timestamp': datetime.now().isoformat()}
    def learn(self, data=None):
        self._cycles += 1
        return {"status": "success", "cycles": self._cycles}

class MockTradingBot:
    def __init__(self, brain_instance=None, exchange_instance=None):
        self.brain = brain_instance
        self.exchange = exchange_instance
        self.running = True
        self._cycles = 0
    def get_status(self):
        self._cycles += 1
        return {"state": "RUNNING", "mode": MODE, "cycles": self._cycles, "uptime": int(time.time()), "version": APP_VERSION}
    def get_signals(self):
        pairs = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "XRP/USD"]
        signals = []
        for pair in pairs:
            signals.append({"pair": pair, "signal": random.choice(["BUY", "SELL", "HOLD"]), "confidence": random.randint(40, 95), "price": random.uniform(1000, 65000), "timestamp": datetime.now().isoformat()})
        return signals
    def get_market_data(self):
        pairs = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "XRP/USD"]
        data = {}
        for pair in pairs:
            base = random.uniform(1000, 65000)
            data[pair] = {"price": round(base, 2), "change": round(random.uniform(-5, 5), 2), "volume": round(random.uniform(100, 2000), 2), "trend": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]), "timestamp": datetime.now().isoformat()}
        return data
    def analyze_pair(self, pair):
        return {"pair": pair, "signal": random.choice(["BUY", "SELL", "HOLD"]), "confidence": random.randint(40, 95), "indicators": {"rsi": random.randint(20, 80), "macd": round(random.uniform(-1, 1), 4)}, "timestamp": datetime.now().isoformat()}
    def stop(self):
        self.running = False
        return True

if Brain is None:
    cprint("⚠️ Brain not available, using MockBrain", 'yellow')
    Brain = MockBrain
    brain = MockBrain()

if TradingBot is None:
    cprint("⚠️ TradingBot not available, using MockTradingBot", 'yellow')
    TradingBot = MockTradingBot

cprint("✅ Core modules loaded", 'green')

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
        
        @app.route('/api/status', methods=['GET'])
        def api_status():
            try:
                status = bot_instance.get_status() if bot_instance else {"status": "unknown"}
                return jsonify({"status": "online", "bot": status, "version": APP_VERSION, "mode": MODE, "timestamp": datetime.now().isoformat()})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500
        
        @app.route('/api/health', methods=['GET'])
        def api_health():
            return jsonify({"status": "healthy", "uptime": int(time.time()), "timestamp": datetime.now().isoformat()})
        
        @app.route('/api/signals', methods=['GET'])
        def api_signals():
            try:
                signals = bot_instance.get_signals() if bot_instance and hasattr(bot_instance, 'get_signals') else []
                return jsonify({"signals": signals, "timestamp": datetime.now().isoformat()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/market', methods=['GET'])
        def api_market():
            try:
                data = bot_instance.get_market_data() if bot_instance and hasattr(bot_instance, 'get_market_data') else {}
                return jsonify({"data": data, "timestamp": datetime.now().isoformat()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/analyze/<pair>', methods=['GET'])
        def api_analyze(pair):
            try:
                result = bot_instance.analyze_pair(pair) if bot_instance and hasattr(bot_instance, 'analyze_pair') else {"pair": pair, "signal": "UNKNOWN"}
                return jsonify({"pair": pair, "analysis": result, "timestamp": datetime.now().isoformat()})
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
                return jsonify({"brain": state, "timestamp": datetime.now().isoformat()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/performance', methods=['GET'])
        def api_performance():
            return jsonify({"performance": {"roi": 0.0, "trades": 0, "win_rate": 0.0, "total_pnl": 0.0}, "timestamp": datetime.now().isoformat()})
        
        @socketio.on('connect')
        def handle_connect():
            logger.info(f"Client connected: {request.sid}")
            emit('connected', {'status': 'ok', 'timestamp': datetime.now().isoformat()})
        
        @socketio.on('disconnect')
        def handle_disconnect():
            logger.info(f"Client disconnected: {request.sid}")
        
        cprint(f"🌐 Starting API Server on {API_HOST}:{API_PORT}", 'cyan')
        
        def run_server():
            socketio.run(app, host=API_HOST, port=API_PORT, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        cprint(f"✅ API Server running on http://{API_HOST}:{API_PORT}", 'green')
        cprint("   - GET  /api/status", 'lightblue')
        cprint("   - GET  /api/health", 'lightblue')
        cprint("   - GET  /api/signals", 'lightblue')
        cprint("   - GET  /api/market", 'lightblue')
        cprint("   - GET  /api/analyze/<pair>", 'lightblue')
        cprint("   - GET  /api/brain/state", 'lightblue')
        cprint("   - GET  /api/performance", 'lightblue')
        cprint("   - WS   / (WebSocket)", 'lightblue')
        
        return True
        
    except ImportError as e:
        cprint(f"⚠️ Flask not available: {e}", 'yellow')
        cprint("   Install: pip install flask flask-cors flask-socketio python-socketio", 'lightyellow')
        return False
    except Exception as e:
        cprint(f"❌ API Server error: {e}", 'red')
        return False

# ============================================================
# MAIN HEADLESS FUNCTION
# ============================================================

def main_headless():
    global brain_instance, bot_instance
    
    # Print banner
    print_banner()
    
    cprint("🚀 Initializing Cognitive Brain...", 'cyan')
    try:
        if Brain and Brain != MockBrain:
            brain_instance = Brain()
            cprint("✅ Brain initialized (REAL)", 'green')
        else:
            brain_instance = MockBrain()
            cprint("✅ Brain initialized (MOCK)", 'yellow')
    except Exception as e:
        cprint(f"❌ Brain init error: {e}", 'red')
        brain_instance = MockBrain()
        cprint("✅ Brain initialized (MOCK - fallback)", 'yellow')
    
    cprint("🤖 Initializing Trading Bot...", 'cyan')
    try:
        if TradingBot and TradingBot != MockTradingBot:
            bot_instance = TradingBot(brain_instance=brain_instance, exchange_instance=exchange)
            cprint("✅ Trading Bot initialized (REAL)", 'green')
        else:
            bot_instance = MockTradingBot(brain_instance=brain_instance, exchange_instance=exchange)
            cprint("✅ Trading Bot initialized (MOCK)", 'yellow')
    except Exception as e:
        cprint(f"❌ Bot init error: {e}", 'red')
        bot_instance = MockTradingBot(brain_instance=brain_instance)
        cprint("✅ Trading Bot initialized (MOCK - fallback)", 'yellow')
    
    api_started = start_api_server(bot_instance)
    
    cprint("\n" + "=" * 60, 'magenta', bold=True)
    cprint("  ✅ SYSTEM READY", 'green', bold=True)
    cprint("=" * 60, 'magenta', bold=True)
    cprint(f"  Mode        : {MODE}", 'lightgreen' if MODE == 'PAPER' else 'lightred')
    cprint(f"  Brain       : {type(brain_instance).__name__}", 'lightcyan')
    cprint(f"  Bot         : {type(bot_instance).__name__}", 'lightcyan')
    cprint(f"  Exchange    : {'AVAILABLE' if EXCHANGE_AVAILABLE else 'UNAVAILABLE'}", 'green' if EXCHANGE_AVAILABLE else 'red')
    cprint(f"  API Server  : {'ON' if api_started else 'OFF'}", 'green' if api_started else 'red')
    cprint("=" * 60, 'magenta', bold=True)
    cprint("📡 Press Ctrl+C to stop", 'yellow')
    cprint("=" * 60, 'magenta', bold=True)
    cprint("")
    
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
                    cprint(f"🟢 Status: {state} | Cycles: {cycle_count} | Uptime: {cycle_count}s", 'lightgreen')
                except Exception as e:
                    logger.debug(f"Status log error: {e}")
    except KeyboardInterrupt:
        cprint("\n⚠️ Bot stopped by user", 'yellow')
        _graceful_shutdown = True
    
    cprint("🔄 Shutting down...", 'cyan')
    try:
        if bot_instance and hasattr(bot_instance, 'stop'):
            bot_instance.stop()
            cprint("✅ Bot stopped", 'green')
    except Exception as e:
        cprint(f"⚠️ Bot stop error: {e}", 'yellow')
    
    cprint(f"✅ {APP_NAME} stopped.", 'green')
    return 0

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    try:
        exit_code = main_headless()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        cprint("👋 Bot stopped by user", 'yellow')
        sys.exit(0)
    except Exception as e:
        cprint(f"❌ Fatal error: {e}", 'red', bold=True)
        traceback.print_exc()
        sys.exit(1)
