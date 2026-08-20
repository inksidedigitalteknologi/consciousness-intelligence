#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# main.py
# INKSIDEDIGITAL TRADING BOT v5.0
# COGNITIVE MIRROR ENGINE - BINANCE INTEGRATION
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

# Binance Config
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY', '')
BINANCE_SECRET = os.environ.get('BINANCE_SECRET', '')
BINANCE_SANDBOX = os.environ.get('BINANCE_SANDBOX', 'true').lower() == 'true'

logger.info(f"🚀 Starting {APP_NAME} v{APP_VERSION}")
logger.info(f"   Mode: {MODE}")
logger.info(f"   Binance Sandbox: {BINANCE_SANDBOX}")

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

# ============================================================
# BINANCE EXCHANGE INTEGRATION
# ============================================================

try:
    import ccxt
    CCXT_AVAILABLE = True
    logger.info("✅ CCXT loaded")
except ImportError as e:
    CCXT_AVAILABLE = False
    logger.warning(f"⚠️ CCXT not available: {e}")
    logger.warning("   Install: pip install ccxt")

class BinanceExchange:
    """Binance exchange wrapper using CCXT."""
    
    def __init__(self, api_key: str = '', secret: str = '', sandbox: bool = True):
        self.api_key = api_key
        self.secret = secret
        self.sandbox = sandbox
        self.exchange = None
        self._initialized = False
        self._pairs = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "XRP/USD"]
        
        if not CCXT_AVAILABLE:
            logger.warning("⚠️ CCXT not available, Binance disabled")
            return
        
        try:
            self.exchange = ccxt.binance({
                'apiKey': api_key,
                'secret': secret,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                }
            })
            
            if sandbox:
                self.exchange.set_sandbox_mode(True)
                logger.info("🔧 Binance Sandbox mode enabled")
            
            self._initialized = True
            logger.info("✅ Binance exchange initialized successfully")
            
            # Test connection
            try:
                self.exchange.fetch_ticker('BTCUSDT')
                logger.info("✅ Binance connection test passed")
            except Exception as e:
                logger.warning(f"⚠️ Binance connection test failed: {e}")
                
        except Exception as e:
            logger.error(f"❌ Binance init error: {e}")
            self.exchange = None
            self._initialized = False
    
    def is_ready(self) -> bool:
        return self._initialized and self.exchange is not None
    
    def get_ticker(self, symbol: str) -> Optional[Dict]:
        """Get ticker data from Binance."""
        if not self.is_ready():
            return None
        
        try:
            symbol_clean = symbol.replace('/', '')
            ticker = self.exchange.fetch_ticker(symbol_clean)
            
            return {
                'symbol': ticker['symbol'],
                'price': ticker.get('last', 0),
                'change': ticker.get('percentage', 0),
                'high': ticker.get('high', 0),
                'low': ticker.get('low', 0),
                'volume': ticker.get('baseVolume', 0),
                'timestamp': ticker.get('timestamp', int(time.time() * 1000))
            }
        except Exception as e:
            logger.debug(f"Binance ticker error for {symbol}: {e}")
            return None
    
    def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List:
        """Get OHLCV data from Binance."""
        if not self.is_ready():
            return []
        
        try:
            symbol_clean = symbol.replace('/', '')
            ohlcv = self.exchange.fetch_ohlcv(symbol_clean, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            logger.debug(f"Binance OHLCV error for {symbol}: {e}")
            return []
    
    def get_balance(self) -> Dict:
        """Get account balance from Binance."""
        if not self.is_ready():
            return {}
        
        try:
            return self.exchange.fetch_balance()
        except Exception as e:
            logger.debug(f"Binance balance error: {e}")
            return {}
    
    def create_order(self, symbol: str, side: str, order_type: str, amount: float, price: float = None) -> Dict:
        """Create order on Binance."""
        if not self.is_ready():
            return {}
        
        try:
            symbol_clean = symbol.replace('/', '')
            return self.exchange.create_order(symbol_clean, order_type, side, amount, price)
        except Exception as e:
            logger.error(f"Binance order error: {e}")
            return {}
    
    def get_pairs(self) -> List[str]:
        return self._pairs
    
    def generate_signal(self, pair: str) -> Dict:
        """Generate trading signal based on Binance data."""
        ticker = self.get_ticker(pair)
        
        if not ticker:
            return {
                "pair": pair,
                "signal": "HOLD",
                "confidence": 0,
                "price": 0,
                "strength": "NEUTRAL",
                "timestamp": datetime.now().isoformat()
            }
        
        price = ticker.get('price', 0)
        change = ticker.get('change', 0)
        
        if change > 2.0:
            signal = "BUY"
            confidence = min(95, 70 + abs(change) * 3)
            strength = "STRONG" if abs(change) > 4 else "MODERATE"
        elif change < -2.0:
            signal = "SELL"
            confidence = min(95, 70 + abs(change) * 3)
            strength = "STRONG" if abs(change) > 4 else "MODERATE"
        elif abs(change) < 0.5:
            signal = "HOLD"
            confidence = 50
            strength = "NEUTRAL"
        else:
            signal = "MONITOR"
            confidence = 60 + abs(change) * 5
            strength = "WEAK"
        
        return {
            "pair": pair,
            "signal": signal,
            "confidence": int(confidence),
            "price": round(price, 2),
            "strength": strength,
            "timestamp": datetime.now().isoformat()
        }

# Initialize Binance
binance_exchange = BinanceExchange(
    api_key=BINANCE_API_KEY,
    secret=BINANCE_SECRET,
    sandbox=BINANCE_SANDBOX
)

if binance_exchange.is_ready():
    EXCHANGE_AVAILABLE = True
    logger.info("✅ Binance Exchange is READY")
else:
    EXCHANGE_AVAILABLE = False
    logger.warning("⚠️ Binance Exchange is NOT available")

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

class MockTradingBot:
    def __init__(self, brain_instance=None, exchange_instance=None):
        self.brain = brain_instance
        self.exchange = exchange_instance
        self.running = True
        self._cycles = 0
        
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
        if binance_exchange.is_ready():
            signals = []
            for pair in binance_exchange.get_pairs():
                signal = binance_exchange.generate_signal(pair)
                signals.append(signal)
            return signals
        
        # Fallback mock
        pairs = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "XRP/USD"]
        signals = []
        for pair in pairs:
            signals.append({
                "pair": pair,
                "signal": random.choice(["BUY", "SELL", "HOLD", "MONITOR"]),
                "confidence": random.randint(40, 95),
                "price": round(random.uniform(1000, 65000), 2),
                "strength": random.choice(["WEAK", "NEUTRAL", "STRONG"]),
                "timestamp": datetime.now().isoformat()
            })
        return signals
    
    def get_market_data(self, pair=None):
        if binance_exchange.is_ready() and pair:
            ticker = binance_exchange.get_ticker(pair)
            if ticker:
                return ticker
        
        # Fallback mock
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

if Brain is None:
    logger.warning("⚠️ Brain not available, using MockBrain")
    Brain = MockBrain
    brain = MockBrain()

if TradingBot is None:
    logger.warning("⚠️ TradingBot not available, using MockTradingBot")
    TradingBot = MockTradingBot

logger.info("✅ Core modules loaded")

# ============================================================
# API SERVER
# ============================================================

def start_api_server(bot_instance):
    try:
        from flask import Flask, jsonify, request
        from flask_cors import CORS
        from flask_socketio import SocketIO, emit
        
        app = Flask(__name__)
        CORS(app, origins="*")
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
                    "exchange": "binance",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/health', methods=['GET'])
        def api_health():
            return jsonify({
                "status": "healthy",
                "uptime": int(time.time() - _startup_time),
                "exchange": "binance",
                "sandbox": BINANCE_SANDBOX,
                "timestamp": datetime.now().isoformat()
            })
        
        @app.route('/api/signals', methods=['GET'])
        def api_signals():
            try:
                signals = bot_instance.get_signals() if bot_instance else []
                return jsonify({
                    "signals": signals,
                    "source": "binance",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"API signals error: {e}")
                return jsonify({
                    "signals": [],
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }), 200
        
        @app.route('/api/market', methods=['GET'])
        def api_market():
            try:
                pair = request.args.get('pair', 'BTC/USD')
                
                if bot_instance and hasattr(bot_instance, 'get_market_data'):
                    data = bot_instance.get_market_data(pair)
                else:
                    data = {"price": random.uniform(1000, 65000), "trend": "NEUTRAL"}
                
                return jsonify({
                    "pair": pair,
                    "data": data,
                    "source": "binance" if binance_exchange.is_ready() else "mock",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/analyze/<pair>', methods=['GET'])
        def api_analyze(pair):
            try:
                result = bot_instance.analyze_pair(pair) if bot_instance else {"pair": pair}
                return jsonify({
                    "pair": pair,
                    "analysis": result,
                    "source": "binance",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/brain/state', methods=['GET'])
        def api_brain_state():
            try:
                if brain and hasattr(brain, 'get_state'):
                    state = brain.get_state()
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
                        'insights': ['System running in headless mode']
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
                    "exchange": "binance",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/positions', methods=['GET'])
        def api_positions():
            return jsonify({
                "positions": [],
                "timestamp": datetime.now().isoformat()
            })
        
        @app.route('/api/logs', methods=['GET'])
        def api_logs():
            return jsonify({
                "logs": [],
                "timestamp": datetime.now().isoformat()
            })
        
        @app.route('/api/diagnostics', methods=['GET'])
        def api_diagnostics():
            return jsonify({
                "diagnostics": {
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
                        "exchange": "binance",
                        "sandbox": BINANCE_SANDBOX
                    }
                },
                "timestamp": datetime.now().isoformat()
            })
        
        @app.route('/api/telegram/status', methods=['GET'])
        def api_telegram_status():
            return jsonify({
                "configured": False,
                "bot_name": "Not Configured",
                "status": "offline",
                "timestamp": datetime.now().isoformat()
            })
        
        @app.route('/api/exchange/status', methods=['GET'])
        def api_exchange_status():
            return jsonify({
                "exchange": "binance",
                "available": EXCHANGE_AVAILABLE,
                "sandbox": BINANCE_SANDBOX,
                "api_key_configured": bool(BINANCE_API_KEY),
                "timestamp": datetime.now().isoformat()
            })
        
        @app.route('/api/engine/start', methods=['POST'])
        def api_engine_start():
            if bot_instance and hasattr(bot_instance, 'start_engine'):
                bot_instance.start_engine()
            return jsonify({
                "status": "started",
                "timestamp": datetime.now().isoformat()
            })
        
        @app.route('/api/engine/stop', methods=['POST'])
        def api_engine_stop():
            if bot_instance and hasattr(bot_instance, 'stop'):
                bot_instance.stop()
            return jsonify({
                "status": "stopped",
                "timestamp": datetime.now().isoformat()
            })
        
        @app.route('/api/learning/status', methods=['GET'])
        def api_learning_status():
            return jsonify({
                "learning": {
                    "active": True,
                    "cycles": 0,
                    "status": "ready"
                },
                "timestamp": datetime.now().isoformat()
            })
        
        # ========================================================
        # WEBSOCKET
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
        logger.info(f"   Exchange: BINANCE")
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
        logger.info(f"   - GET  /api/exchange/status")
        logger.info(f"   - POST /api/engine/start")
        logger.info(f"   - POST /api/engine/stop")
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
    logger.info(f"  Exchange: BINANCE")
    logger.info("=" * 60)
    
    # Initialize Brain
    logger.info("Initializing Cognitive Brain...")
    try:
        if Brain and Brain != MockBrain:
            brain_instance = Brain()
            logger.info("✅ Brain initialized (REAL)")
        else:
            brain_instance = MockBrain()
            logger.info("✅ Brain initialized (MOCK)")
    except Exception as e:
        brain_instance = MockBrain()
        logger.info("✅ Brain initialized (MOCK - fallback)")
    
    # Initialize Trading Bot
    logger.info("Initializing Trading Bot...")
    try:
        if TradingBot and TradingBot != MockTradingBot:
            bot_instance = TradingBot(
                brain_instance=brain_instance,
                exchange_instance=binance_exchange
            )
            logger.info("✅ Trading Bot initialized (REAL)")
        else:
            bot_instance = MockTradingBot(
                brain_instance=brain_instance,
                exchange_instance=binance_exchange
            )
            logger.info("✅ Trading Bot initialized (MOCK)")
    except Exception as e:
        bot_instance = MockTradingBot(brain_instance=brain_instance)
        logger.info("✅ Trading Bot initialized (MOCK - fallback)")
    
    # Start API Server
    api_started = start_api_server(bot_instance)
    
    # Start Scanner
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
    logger.info(f"  Exchange    : BINANCE {'(SANDBOX)' if BINANCE_SANDBOX else '(LIVE)'}")
    logger.info(f"  Status      : {'AVAILABLE' if EXCHANGE_AVAILABLE else 'UNAVAILABLE'}")
    logger.info(f"  API Server  : {'ON' if api_started else 'OFF'}")
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
                except:
                    pass
    except KeyboardInterrupt:
        logger.info("\n⚠️ Bot stopped by user")
        _graceful_shutdown = True
    
    logger.info("Shutting down...")
    try:
        if bot_instance and hasattr(bot_instance, 'stop'):
            bot_instance.stop()
            logger.info("✅ Bot stopped")
    except:
        pass
    
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
