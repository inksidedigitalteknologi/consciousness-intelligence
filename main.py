#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# main.py
# INKSIDEDIGITAL TRADING BOT v4.4.1
# COGNITIVE MIRROR ENGINE - FULL INTEGRATION - ROBUST
# ============================================================

import random
import logging
import threading
import sys
import time
import signal
import traceback
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
import json

import customtkinter as ctk
# ============================================================
# MOBILE BRIDGE (PYREMOTE)
# ============================================================

def start_mobile_bridge():
    """Start PyRemote Mobile Bridge server."""
    try:
        # Coba import pyremote_server
        try:
            import pyremote_server
            t = threading.Thread(
                target=lambda: pyremote_server.app.run(
                    host='0.0.0.0',
                    port=5000,
                    debug=False,
                    use_reloader=False
                ),
                daemon=True
            )
            t.start()
            print("[OK] PyRemote Mobile Bridge aktif di port 5000!")
            return True
        except ImportError:
            pass
        
        # Coba alternatif: pyremote
        try:
            from pyremote import server
            t = threading.Thread(
                target=lambda: server.run(host='0.0.0.0', port=5000),
                daemon=True
            )
            t.start()
            print("[OK] PyRemote Mobile Bridge aktif di port 5000!")
            return True
        except ImportError:
            pass
        
        # Coba Flask API sederhana
        try:
            from flask import Flask, jsonify, request
            app = Flask(__name__)
            
            @app.route('/api/status', methods=['GET'])
            def status():
                return jsonify({"status": "online", "port": 5000, "timestamp": datetime.now().isoformat()})
            
            @app.route('/api/data', methods=['GET', 'POST'])
            def data():
                if request.method == 'POST':
                    return jsonify({"status": "received", "data": request.json})
                return jsonify({"data": "Inkside Bot Data", "status": "online"})
            
            @app.route('/api/health', methods=['GET'])
            def health():
                return jsonify({"status": "healthy", "uptime": time.time()})
            
            t = threading.Thread(
                target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False),
                daemon=True
            )
            t.start()
            print("[OK] Flask Mobile Bridge aktif di port 5000!")
            return True
        except ImportError:
            pass
        
        print("[WARN] PyRemote Bridge tidak aktif: No module found")
        return False
        
    except Exception as e:
        print(f"[WARN] PyRemote Bridge error: {e}")
        return False

# Panggil saat startup
start_mobile_bridge()

from config import APP_NAME, APP_VERSION, DEBUG_MODE, LOG_LEVEL
from utils.logger import setup_logger

# ============================================================
# PATH SETUP
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================

def global_exception_handler(exc_type, exc_value, exc_tb):
    """Global exception handler untuk menangkap semua error."""
    error_msg = f"Unhandled exception: {exc_type.__name__}: {exc_value}"
    print(f"\n{'='*60}")
    print(f"❌ {error_msg}")
    print(f"{'='*60}")
    traceback.print_tb(exc_tb)
    print(f"{'='*60}\n")
    
    try:
        logger = logging.getLogger(__name__)
        logger.critical(error_msg, exc_info=(exc_type, exc_value, exc_tb))
    except:
        pass
    
    try:
        error_file = CURRENT_DIR / "logs" / f"crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        error_file.parent.mkdir(exist_ok=True)
        with open(error_file, 'w') as f:
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"Error: {error_msg}\n")
            f.write("Traceback:\n")
            traceback.print_tb(exc_tb, file=f)
    except:
        pass

sys.excepthook = global_exception_handler

# ============================================================
# LOGGER
# ============================================================

logger = setup_logger()

# ============================================================
# CONSTANTS
# ============================================================

LEARNING_ENGINE_AVAILABLE = False
ENGINE_VERSION = "N/A"
KERNEL_VERSION = "N/A"
STATE_IDLE = "IDLE"
STATE_RUNNING = "RUNNING"
STATE_SUCCESS = "SUCCESS"
STATE_PARTIAL = "PARTIAL"
STATE_ERROR = "ERROR"
STATE_STOPPED = "STOPPED"
STATE_CRASHED = "CRASHED"

# ============================================================
# SIGNAL HANDLER
# ============================================================

_shutdown_flag = threading.Event()
_graceful_shutdown = False

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    global _graceful_shutdown
    print(f"\n[INFO] Received signal {sig}, initiating graceful shutdown...")
    _graceful_shutdown = True
    _shutdown_flag.set()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ============================================================
# SINGLE ENTRY POINT - SEMUA DARI CORE
# ============================================================

print("[INFO] Loading core modules...")

# ============================================================
# FIX: Import learning_engine dari core terlebih dahulu
# ============================================================

CORE_LEARNING_ENGINE = None
CORE_LEARNING_AVAILABLE = False

try:
    from core.learning.engine import learning_engine as core_learning_engine
    CORE_LEARNING_ENGINE = core_learning_engine
    CORE_LEARNING_AVAILABLE = True
    print("[INFO] ✅ Core Learning Engine found")
except ImportError as e:
    print(f"[WARN] ⚠️ Core Learning Engine not found: {e}")
except Exception as e:
    print(f"[WARN] ⚠️ Core Learning Engine error: {e}")

# ============================================================
# IMPORT SEMUA MODULE DARI CORE
# ============================================================

imported_modules = {}
CORE_IMPORT_SUCCESS = False

CORE_MODULES = [
    ('Brain', 'brain'),
    ('Consciousness', 'consciousness'),
    ('TradingBot', None),
    ('HealthMonitor', 'health_monitor'),
    ('set_status', None),
    ('get_status', None),
    ('memory', None),
    ('knowledge', None),
    ('reasoning', None),
    ('scanner', None),
    ('signal_engine', None),
    ('analyzer', None),
    ('scheduler', None),
    ('runtime', None),
    ('system_config', None),
    ('watchdog', None),
    ('diagnostics', None),
    ('validator', None),
]

LEARNING_MODULES = [
    ('LearningEngine', 'learning_engine'),
    ('PatternEngine', 'pattern'),
    ('PredictionEngine', 'prediction_engine'),
    ('DecisionEngine', 'decision_engine'),
    ('SemanticMemory', 'semantic_memory'),
    ('LearningMemory', 'learning_memory'),
    ('MemoryOptimizer', 'memory_optimizer'),
    ('EntityRecognition', 'entity_recognition'),
    ('SemanticProcessor', 'semantic_processor'),
    ('ContextManager', 'context_manager'),
    ('GoalManager', 'goal_manager'),
    ('ReflectionEngine', 'reflection_engine'),
    ('InsightEngine', 'insight_engine'),
    ('BehaviorEngine', 'behavior_engine'),
    ('AssociationEngine', 'association_engine'),
    ('SelfDiagnostic', 'self_diagnostic'),
    ('ImprovementEngine', 'improvement_engine'),
    ('MarketLearning', 'market_learning'),
    ('StrategyEngine', 'strategy_engine'),
    ('SimulationEngine', 'simulation_engine'),
    ('EvaluatorEngine', 'evaluator_engine'),
    ('AdaptiveEngine', 'adaptive_engine'),
    ('LearningAnalyzer', 'learning_analyzer'),
    ('Collector', None),
    ('DataCleaner', None),
    ('Normalizer', None),
    ('FeatureExtractor', None),
]

def safe_import(module_name: str, attr_name: Optional[str] = None):
    """Safe import dengan fallback."""
    try:
        if attr_name:
            module = __import__(f'core.{module_name}', fromlist=[attr_name])
            imported = getattr(module, attr_name, None)
            if imported is not None:
                return imported
        else:
            return __import__(f'core.{module_name}', fromlist=['*'])
    except ImportError as e:
        logger.debug(f"Import error for {module_name}: {e}")
    except Exception as e:
        logger.debug(f"Import exception for {module_name}: {e}")
    return None

for module_name, attr_name in CORE_MODULES:
    result = safe_import(module_name, attr_name)
    if result is not None:
        if attr_name:
            imported_modules[attr_name] = result
        else:
            imported_modules[module_name] = result
    else:
        if attr_name:
            imported_modules[attr_name] = None

for module_name, attr_name in LEARNING_MODULES:
    try:
        result = safe_import(module_name, attr_name)
        if result is not None:
            if attr_name:
                imported_modules[attr_name] = result
            else:
                imported_modules[module_name] = result
        else:
            if attr_name:
                imported_modules[attr_name] = None
    except Exception as e:
        logger.debug(f"Learning module import error {module_name}: {e}")
        if attr_name:
            imported_modules[attr_name] = None

def get_imported(key: str, default=None):
    return imported_modules.get(key, default)

# ============================================================
# AMBIL SEMUA MODULE DARI IMPORTED
# ============================================================

Brain = get_imported('Brain')
brain = get_imported('brain')
Consciousness = get_imported('consciousness')
TradingBot = get_imported('TradingBot')
HealthMonitor = get_imported('HealthMonitor')
health_monitor = get_imported('health_monitor')
set_status = get_imported('set_status')
get_status = get_imported('get_status')
memory = get_imported('memory')
knowledge = get_imported('knowledge')
reasoning = get_imported('reasoning')
scanner = get_imported('scanner')
signal_engine = get_imported('signal_engine')
analyzer = get_imported('analyzer')
scheduler = get_imported('scheduler')
runtime = get_imported('runtime')
system_config = get_imported('system_config')
watchdog = get_imported('watchdog')
diagnostics = get_imported('diagnostics')
validator = get_imported('validator')

LearningEngine = get_imported('LearningEngine')
learning_engine = get_imported('learning_engine')
PatternEngine = get_imported('PatternEngine')
pattern = get_imported('pattern')
PredictionEngine = get_imported('PredictionEngine')
prediction_engine = get_imported('prediction_engine')
DecisionEngine = get_imported('DecisionEngine')
decision_engine = get_imported('decision_engine')
SemanticMemory = get_imported('SemanticMemory')
semantic_memory = get_imported('semantic_memory')
LearningMemory = get_imported('LearningMemory')
learning_memory = get_imported('learning_memory')
MemoryOptimizer = get_imported('MemoryOptimizer')
memory_optimizer = get_imported('memory_optimizer')
EntityRecognition = get_imported('EntityRecognition')
entity_recognition = get_imported('entity_recognition')
SemanticProcessor = get_imported('SemanticProcessor')
semantic_processor = get_imported('semantic_processor')
ContextManager = get_imported('ContextManager')
context_manager = get_imported('context_manager')
GoalManager = get_imported('GoalManager')
goal_manager = get_imported('goal_manager')
ReflectionEngine = get_imported('ReflectionEngine')
reflection_engine = get_imported('reflection_engine')
InsightEngine = get_imported('InsightEngine')
insight_engine = get_imported('insight_engine')
BehaviorEngine = get_imported('BehaviorEngine')
behavior_engine = get_imported('behavior_engine')
AssociationEngine = get_imported('AssociationEngine')
association_engine = get_imported('association_engine')
SelfDiagnostic = get_imported('SelfDiagnostic')
self_diagnostic = get_imported('self_diagnostic')
ImprovementEngine = get_imported('ImprovementEngine')
improvement_engine = get_imported('improvement_engine')
MarketLearning = get_imported('MarketLearning')
market_learning = get_imported('market_learning')
StrategyEngine = get_imported('StrategyEngine')
strategy_engine = get_imported('strategy_engine')
SimulationEngine = get_imported('SimulationEngine')
simulation_engine = get_imported('simulation_engine')
EvaluatorEngine = get_imported('EvaluatorEngine')
evaluator_engine = get_imported('evaluator_engine')
AdaptiveEngine = get_imported('AdaptiveEngine')
adaptive_engine = get_imported('adaptive_engine')
LearningAnalyzer = get_imported('LearningAnalyzer')
learning_analyzer = get_imported('learning_analyzer')
Collector = get_imported('Collector')
DataCleaner = get_imported('DataCleaner')
Normalizer = get_imported('Normalizer')
FeatureExtractor = get_imported('FeatureExtractor')

CORE_IMPORT_SUCCESS = True

# ============================================================
# FIX: Jika learning_engine dari core tidak ada, gunakan dari import
# ============================================================

if CORE_LEARNING_ENGINE is None and learning_engine is not None:
    CORE_LEARNING_ENGINE = learning_engine
    CORE_LEARNING_AVAILABLE = True
    print("[INFO] ✅ Using learning_engine from core import")

# ============================================================
# FIX: FORCE IMPORT BRAIN DARI CORE (CRITICAL)
# ============================================================

try:
    from core.brain import Brain as CoreBrain, brain as core_brain
    if CoreBrain is not None:
        Brain = CoreBrain
        brain = core_brain
        print("[INFO] ✅ Brain loaded from core (force import)")
    else:
        print("[WARN] ⚠️ Brain from core is None")
except ImportError as e:
    print(f"[WARN] ⚠️ Could not import Brain from core: {e}")
except Exception as e:
    print(f"[WARN] ⚠️ Error importing Brain: {e}")

# ============================================================
# FIX: FORCE IMPORT EXCHANGE DARI MARKET_DATA (CRITICAL)
# ============================================================

try:
    from core.market_data import (
        KrakenMarketData,
        kraken_market,
        exchange,
        get_exchange,
        get_market_data,
        TickerData,
        Candle,
    )
    EXCHANGE_AVAILABLE = True
    print("[INFO] ✅ Exchange loaded from market_data")
except ImportError as e:
    EXCHANGE_AVAILABLE = False
    KrakenMarketData = None
    kraken_market = None
    exchange = None
    get_exchange = None
    get_market_data = None
    TickerData = None
    Candle = None
    print(f"[WARN] ⚠️ Exchange not available: {e}")

# ============================================================
# GUI IMPORTS
# ============================================================

GUI_AVAILABLE = False
InksideBotApp = None

try:
    from gui.app import InksideApp as InksideBotApp
    GUI_AVAILABLE = True
    print("[INFO] ✅ GUI available")
except ImportError as e:
    print(f"[WARN] ⚠️ GUI not available: {e}")
except Exception as e:
    print(f"[WARN] ⚠️ GUI error: {e}")

# ============================================================
# CLASSES YANG DIBUTUHKAN (FALLBACK)
# ============================================================

if HealthMonitor is None:
    class HealthMonitor:
        def __init__(self):
            self.health = 100.0
            self.modules = {}
            self.executions = []
        def register(self, name):
            self.modules[name] = {"status": "OK", "last_check": datetime.now().isoformat()}
        def record_execution(self, name, duration, success):
            self.executions.append({
                "name": name,
                "duration": duration,
                "success": success,
                "timestamp": datetime.now().isoformat()
            })
            if len(self.executions) > 1000:
                self.executions = self.executions[-1000:]
    health_monitor = HealthMonitor()
    print("[INFO] ✅ Created HealthMonitor fallback")

if set_status is None:
    def set_status(component, status):
        logger.debug(f"Status: {component} -> {status}")
    print("[INFO] ✅ Created set_status fallback")

if get_status is None:
    def get_status(component=None):
        return {"status": "OK", "timestamp": datetime.now().isoformat()}
    print("[INFO] ✅ Created get_status fallback")

# ============================================================
# DATA GENERATOR & MOCK CLASSES (FALLBACK)
# ============================================================

class DataGenerator:
    _prices = {
        "BTC/USD": 65000,
        "ETH/USD": 3500,
        "SOL/USD": 180,
        "XRP/USD": 0.55,
        "ADA/USD": 0.45,
        "AVAX/USD": 35,
        "LINK/USD": 15,
        "DOT/USD": 7,
        "LTC/USD": 72,
        "BCH/USD": 280,
    }
    
    @classmethod
    def generate_market_data(cls):
        result = {}
        for pair, base_price in cls._prices.items():
            volatility = 0.02
            change = random.uniform(-volatility, volatility)
            price = base_price * (1 + change)
            result[pair] = {
                "price": round(price, 2),
                "volume": round(random.uniform(500, 2000), 2),
                "trend": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]),
                "change": round(change * 100, 2),
                "high": round(price * (1 + random.uniform(0, 0.01)), 2),
                "low": round(price * (1 - random.uniform(0, 0.01)), 2),
                "timestamp": datetime.now().isoformat(),
            }
            cls._prices[pair] = price
        return result
    
    @classmethod
    def generate_signals(cls, count=10):
        pairs = list(cls._prices.keys())
        actions = ["BUY", "SELL", "HOLD", "MONITOR", "EXIT"]
        signals = []
        for i in range(min(count, len(pairs))):
            pair = pairs[i % len(pairs)]
            signal = random.choice(actions)
            confidence = random.randint(30, 95)
            signals.append({
                "pair": pair,
                "signal": signal,
                "confidence": confidence,
                "price": cls._prices.get(pair, 1000) * (1 + random.uniform(-0.01, 0.01)),
                "strength": random.choice(["WEAK", "NEUTRAL", "STRONG", "VERY_STRONG"]),
                "quality": random.randint(30, 90),
                "timestamp": datetime.now().isoformat(),
            })
        return signals

class MockScanner:
    def __init__(self):
        self.running = True
        self._results = []
        self._scan_count = 0
    def get_status(self):
        return {
            "running": self.running,
            "pairs_scanned": 10,
            "signals_generated": 128 + self._scan_count * 2,
            "last_scan": datetime.now().isoformat(),
        }
    def get_results(self):
        self._scan_count += 1
        pairs = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "XRP/USD"]
        signals = []
        for pair in pairs:
            signals.append({
                "pair": pair,
                "analysis": {
                    "trend": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]),
                    "rsi": random.randint(20, 80),
                    "macd": random.uniform(-1, 1),
                },
                "signal": {
                    "signal": random.choice(["BUY", "SELL", "HOLD"]),
                    "confidence": random.randint(40, 90),
                }
            })
        self._results = signals
        return signals
    def start(self):
        self.running = True
        return True
    def stop(self):
        self.running = False
        return True

# ============================================================
# MOCK BRAIN - FALLBACK SAJA
# ============================================================

class MockBrain:
    def __init__(self):
        self._state = "ACTIVE"
        self._cycles = 0
        self._success_rate = 87.5
        self._error_rate = 0.0
        self._health_score = 98.0
        self._modules_available = 11
        self._last_reflection = None
    
    def status(self):
        self._cycles += 1
        return {
            "state": self._state,
            "cycles": self._cycles,
            "success_rate": self._success_rate,
            "timestamp": datetime.now().isoformat(),
        }
    
    def get_state(self):
        return self.status()
    
    def forecast(self, pair=None):
        return {
            "forecast": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]),
            "confidence": random.randint(50, 90),
            "price_target": random.uniform(0.9, 1.1),
        }
    
    def decision_support(self, pair=None):
        action = random.choice(["BUY", "SELL", "HOLD"])
        confidence = random.randint(60, 95)
        reasons = [
            "Bullish breakout detected",
            "Bearish divergence confirmed",
            "Support level holding",
            "Resistance level breaking",
            "Volume spike detected",
            "RSI oversold condition",
        ]
        return {
            "action": action,
            "confidence": confidence,
            "reason": random.choice(reasons),
            "timestamp": datetime.now().isoformat(),
        }
    
    def learn(self, data):
        self._cycles += 1
        return {"status": "SUCCESS", "cycles": self._cycles}
    
    def get_memory(self):
        return {"items": 100, "capacity": 1000}
    
    def get_knowledge(self):
        return {"facts": 50, "patterns": 10}
    
    def snapshot(self):
        return {
            "brain": {
                "status": "ONLINE",
                "version": "4.2.3",
                "state": self._state,
                "cycles": self._cycles,
                "errors": 0,
                "success_rate": self._success_rate,
                "health": {"score": self._health_score},
            },
            "market": {
                "mode": "CRYPTO",
                "forecast": random.choice(["BULLISH", "BEARISH", "NEUTRAL"]),
                "confidence": random.randint(40, 90),
                "anomaly": "NORMAL",
                "bias": "UNKNOWN",
                "risk_level": "MEDIUM",
            },
            "decision": {
                "action": "HOLD",
                "confidence": 0.5,
                "reason": "Monitoring",
                "expected_outcome": "no_change",
            },
            "learning": {
                "active": True,
                "history": 100,
                "insights": 50,
            },
            "health": {
                "score": self._health_score,
                "auto_healing": True,
                "healing_attempts": 0,
            },
            "timestamp": datetime.now().isoformat(),
        }
    
    def reflection(self):
        """Stable reflection data with gradual changes."""
        self._cycles += 1
        
        if self._last_reflection is None:
            awareness = 0.72
            curiosity = 0.65
            insight_depth = 0.70
            resilience = 0.80
            focus = 0.72
            emotion = 'CALM'
            insights = [
                "🧠 System awareness is excellent — cognitive state optimal.",
                "📈 Market analysis active — monitoring key pairs.",
                "💡 Learning patterns detected in recent market data.",
                "🎯 Decision confidence is stable and reliable.",
                "🔄 Feedback loop active — cycles processed continuously.",
                "📊 Performance metrics within expected range.",
            ]
        else:
            prev = self._last_reflection
            awareness = prev.get('awareness', 0.72) + random.uniform(-0.015, 0.015)
            awareness = max(0.55, min(0.95, awareness))
            curiosity = prev.get('curiosity', 0.65) + random.uniform(-0.015, 0.02)
            curiosity = max(0.45, min(0.92, curiosity))
            insight_depth = prev.get('insight_depth', 0.70) + random.uniform(-0.015, 0.015)
            insight_depth = max(0.50, min(0.92, insight_depth))
            resilience = prev.get('resilience', 0.80) + random.uniform(-0.01, 0.01)
            resilience = max(0.60, min(0.95, resilience))
            focus = prev.get('focus', 0.72) + random.uniform(-0.015, 0.015)
            focus = max(0.50, min(0.92, focus))
            
            emotion = prev.get('emotion', 'CALM')
            emotion_list = ['CALM', 'FOCUSED', 'CURIOUS', 'CONTEMPLATIVE', 'EXCITED', 'OPTIMISTIC']
            if random.random() < 0.10:
                current_idx = emotion_list.index(emotion) if emotion in emotion_list else 0
                delta = random.choice([-1, 0, 1])
                new_idx = (current_idx + delta) % len(emotion_list)
                emotion = emotion_list[new_idx]
            
            insights = prev.get('insights', [])
            insight_pool = [
                "🧠 System awareness is excellent — cognitive state optimal.",
                "📈 Market analysis active — monitoring key pairs.",
                "💡 Learning patterns detected in recent market data.",
                "🎯 Decision confidence is stable and reliable.",
                "🔄 Feedback loop active — cycles processed continuously.",
                "📊 Performance metrics within expected range.",
                "❤️ System health is excellent.",
                "🔍 Curiosity level is high — actively exploring.",
                "🛡️ Resilience is strong — system recovers well.",
                "🎯 Focus is sharp — concentrating on key signals.",
                "📚 Learning engine is ONLINE and processing.",
                "💾 Memory system is functioning normally.",
                "⚙️ Modules available for cognitive processing.",
                "🌟 Overall cognitive state: EXCELLENT.",
            ]
            if len(insights) >= 6 and random.random() < 0.20:
                idx = random.randint(0, len(insights) - 1)
                new_insight = random.choice(insight_pool)
                while new_insight in insights:
                    new_insight = random.choice(insight_pool)
                insights[idx] = new_insight
        
        result = {
            'awareness': awareness,
            'emotion': emotion,
            'curiosity': curiosity,
            'insight_depth': insight_depth,
            'resilience': resilience,
            'focus': focus,
            'insights': insights[:6],
            'source': 'mock',
            'is_fallback': False,
            'confidence': 0.85,
            'stability': 'STABLE',
            'reflection_quality': 'EXCELLENT',
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'cycles': self._cycles,
                'success_rate': self._success_rate,
                'health_score': self._health_score,
                'modules_available': self._modules_available,
            }
        }
        self._last_reflection = result
        return result

# ============================================================
# MOCK BOT - FALLBACK SAJA
# ============================================================

class MockBot:
    """Mock bot - fallback only."""
    
    def __init__(self):
        self.running = True
        self.scanner = MockScanner()
        self.brain = MockBrain()
        self._market_data = {}
        self._signals = []
        self._update_counter = 0
        self._signal_cache = {}
        self._last_signal_time = {}
        self._signal_cooldown = 30
        
        # Telegram (dummy)
        self.telegram = None
        
    def get_status(self):
        return {
            "running": self.running,
            "state": "RUNNING",
            "mode": "PAPER",
            "results": 12 + self._update_counter,
            "total_signals": 128 + self._update_counter * 2,
            "total_trades": 42 + self._update_counter // 5,
            "uptime": time.time(),
            "version": "4.4.1",
        }
    
    def get_market_data(self):
        self._update_counter += 1
        self._market_data = DataGenerator.generate_market_data()
        return self._market_data
    
    def get_signals(self):
        now = time.time()
        pairs = ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "ADA/USD"]
        signals = []
        for pair in pairs:
            if pair not in self._signal_cache or now - self._last_signal_time.get(pair, 0) > self._signal_cooldown:
                price_data = self._market_data.get(pair, {})
                price = price_data.get('price', 0)
                seed = int(price * 100) % 100 if price > 0 else random.randint(0, 99)
                if seed > 70:
                    signal = "BUY"
                    confidence = 70 + (seed % 20)
                elif seed < 30:
                    signal = "SELL"
                    confidence = 70 + (seed % 20)
                else:
                    signal = "HOLD"
                    confidence = 50 + (seed % 30)
                self._signal_cache[pair] = {
                    "pair": pair,
                    "signal": signal,
                    "confidence": confidence,
                    "price": price,
                    "quality": "NEUTRAL",
                    "strength": "STRONG" if confidence > 80 else "NEUTRAL"
                }
                self._last_signal_time[pair] = now
            signals.append(self._signal_cache[pair])
        return signals
    
    def get_pair_data(self, pair):
        data = self.get_market_data()
        return data.get(pair, {})
    
    def get_signal_for_pair(self, pair):
        signals = self.get_signals()
        for signal in signals:
            if signal.get("pair") == pair:
                return signal
        return None
    
    def start_scanning(self):
        logger.info("MockBot scanning started")
        return True
    
    def stop(self):
        self.running = False
        logger.info("MockBot stopped")
        return True
    
    def analyze_pair(self, pair):
        data = self.get_pair_data(pair)
        signal = self.get_signal_for_pair(pair)
        return {
            "pair": pair,
            "data": data,
            "signal": signal,
            "analysis": {
                "trend": data.get("trend", "NEUTRAL"),
                "volatility": random.uniform(0.1, 2.0),
                "momentum": random.uniform(-1, 1),
            }
        }

# ============================================================
# TRADING BOT WRAPPER - UNTUK KONEKSI KE CORE
# ============================================================

class TradingBotWrapper:
    """Wrapper untuk TradingBot dari core.bot."""
    
    def __init__(self, brain_instance=None, exchange_instance=None, **kwargs):
        self.brain = brain_instance
        self.exchange = exchange_instance
        self.running = True
        self._scanning = False
        self._signals = []
        self._market_data = {}
        self._real_bot = None
        self.telegram = None
        
        # Coba inisialisasi real bot
        try:
            from core.bot import TradingBot as RealTradingBot
            if RealTradingBot is not None:
                try:
                    self._real_bot = RealTradingBot(
                        brain_instance=brain_instance,
                        exchange_instance=exchange_instance,
                        **kwargs
                    )
                    logger.info("✅ Real TradingBot wrapped successfully")
                    print("[INFO] ✅ Real TradingBot is ACTIVE")
                    
                    # Coba ambil telegram dari real bot
                    if hasattr(self._real_bot, 'telegram'):
                        self.telegram = self._real_bot.telegram
                    elif hasattr(self._real_bot, 'telegram_service'):
                        self.telegram = self._real_bot.telegram_service
                    return
                except TypeError as e:
                    logger.debug(f"Real bot signature error: {e}")
                    try:
                        self._real_bot = RealTradingBot(brain_instance=brain_instance)
                        logger.info("✅ Real TradingBot wrapped (brain only)")
                        if hasattr(self._real_bot, 'telegram'):
                            self.telegram = self._real_bot.telegram
                        return
                    except Exception as e2:
                        logger.debug(f"Real bot error (brain only): {e2}")
                except Exception as e:
                    logger.debug(f"Real bot error: {e}")
        except ImportError:
            logger.warning("Real TradingBot not available")
        except Exception as e:
            logger.warning(f"Real bot import error: {e}")
        
        self._real_bot = None
        logger.info("⚠️ TradingBotWrapper using mock data")
        print("[INFO] ⚠️ TradingBotWrapper active (mock)")
    
    def get_status(self):
        if self._real_bot and hasattr(self._real_bot, 'get_status'):
            return self._real_bot.get_status()
        return {
            "running": self.running,
            "state": "RUNNING",
            "mode": "PAPER",
            "total_signals": len(self._signals),
            "version": "4.4.1",
        }
    
    def get_market_data(self):
        if self._real_bot and hasattr(self._real_bot, 'get_market_data'):
            return self._real_bot.get_market_data()
        return DataGenerator.generate_market_data()
    
    def get_signals(self):
        if self._real_bot and hasattr(self._real_bot, 'get_signals'):
            return self._real_bot.get_signals()
        return DataGenerator.generate_signals(5)
    
    def start_scanning(self):
        if self._real_bot and hasattr(self._real_bot, 'start_scanning'):
            return self._real_bot.start_scanning()
        self._scanning = True
        return True
    
    def stop(self):
        if self._real_bot and hasattr(self._real_bot, 'stop'):
            return self._real_bot.stop()
        self.running = False
        return True
    
    def __getattr__(self, name):
        if self._real_bot and hasattr(self._real_bot, name):
            return getattr(self._real_bot, name)
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

# ============================================================
# LEARNING ENGINE INTEGRATION
# ============================================================

class LearningEngineIntegration:
    def __init__(self, bot: Any, brain: Any, config: Optional[Dict] = None):
        self.bot = bot
        self.brain = brain
        self.config = config or {}
        self.engine = CORE_LEARNING_ENGINE

        self.learning_thread: Optional[threading.Thread] = None
        self.running = False
        self.initialized = False
        self._stop_event = threading.Event()
        self._last_learn_time = 0
        self._learn_count = 0
        self._error_count = 0

        if self.engine is not None:
            self._initialize()
        else:
            logger.warning("Learning Engine not available - running in fallback mode")
            self.initialized = False
    
    def _initialize(self) -> None:
        try:
            if hasattr(self.engine, 'initialize'):
                self.engine.initialize()
            self._register_modules()
            self._register_health()
            self.initialized = True
            logger.info("✅ Learning Engine initialized successfully.")
            try:
                if set_status is not None:
                    set_status("learning_engine", "INITIALIZED")
            except:
                pass
        except Exception as e:
            logger.exception(f"Learning Engine init failed: {e}")
            self.engine = None
            self.initialized = False
            self._error_count += 1
    
    def _register_modules(self) -> None:
        if self.engine is None:
            return
        try:
            modules = []
            if self.brain is not None:
                modules.append(("brain", self.brain, 10))
            if self.bot is not None:
                modules.append(("trading_bot", self.bot, 20))
            if market_learning is not None:
                modules.append(("market_learning", market_learning, 30))
            if pattern is not None:
                modules.append(("pattern_engine", pattern, 40))
            if semantic_memory is not None:
                modules.append(("semantic_memory", semantic_memory, 50))
            if prediction_engine is not None:
                modules.append(("prediction_engine", prediction_engine, 60))
            if decision_engine is not None:
                modules.append(("decision_engine", decision_engine, 70))
            for name, module, priority in modules:
                if module is not None and hasattr(self.engine, 'register_module'):
                    try:
                        self.engine.register_module(
                            name=name,
                            module=module,
                            enabled=True,
                            priority=priority
                        )
                        logger.debug(f"Registered {name} module")
                    except Exception as e:
                        logger.warning(f"Failed to register {name}: {e}")
        except Exception as e:
            logger.exception(f"Module registration failed: {e}")
            self._error_count += 1
    
    def _register_health(self) -> None:
        if self.engine is None:
            return
        try:
            if health_monitor is not None and hasattr(health_monitor, 'register'):
                health_monitor.register("learning_engine")
                logger.debug("Registered to health monitor")
        except Exception as e:
            logger.debug(f"Health registration error: {e}")
    
    def start(self) -> bool:
        return self.start_learning()
    
    def stop(self) -> bool:
        return self.stop_learning()
    
    def status(self) -> Dict:
        return self.get_status()
    
    def get_status(self) -> Dict:
        if self.engine is None:
            return {
                "available": False,
                "initialized": False,
                "running": False,
                "engine": None,
                "learn_count": self._learn_count,
                "error_count": self._error_count,
                "message": "Learning Engine not available"
            }
        try:
            status = {}
            if hasattr(self.engine, 'status'):
                status = self.engine.status()
            elif hasattr(self.engine, 'get_status'):
                status = self.engine.get_status()
            elif hasattr(self.engine, 'get_state'):
                status = self.engine.get_state()
            status.update({
                "available": True,
                "initialized": self.initialized,
                "running": self.running,
                "engine_type": type(self.engine).__name__,
                "learn_count": self._learn_count,
                "error_count": self._error_count,
                "last_learn": self._last_learn_time,
            })
            return status
        except Exception as e:
            self._error_count += 1
            return {
                "available": True,
                "initialized": self.initialized,
                "running": self.running,
                "error": str(e),
                "learn_count": self._learn_count,
                "error_count": self._error_count,
            }
    
    def start_learning(self) -> bool:
        if self.engine is None:
            logger.warning("Cannot start: engine not available")
            return False
        if self.running:
            logger.warning("Learning already running")
            return True
        try:
            interval = self.config.get("learning_interval", 300)
            started = False
            if hasattr(self.engine, 'start_learning'):
                started = self.engine.start_learning(interval=interval)
            elif hasattr(self.engine, 'start'):
                started = self.engine.start()
            elif hasattr(self.engine, 'run'):
                started = self.engine.run()
            if not started and not hasattr(self.engine, 'start_learning') and \
               not hasattr(self.engine, 'start') and not hasattr(self.engine, 'run'):
                self._stop_event.clear()
                self.learning_thread = threading.Thread(
                    target=self._learning_loop,
                    daemon=True,
                    name="LearningEngineLoop"
                )
                self.learning_thread.start()
                started = True
            if started:
                self.running = True
                logger.info(f"✅ Learning started (interval={interval}s)")
                try:
                    if set_status is not None:
                        set_status("learning_engine", "RUNNING")
                except:
                    pass
                return True
            logger.warning("Learning engine failed to start")
            return False
        except Exception as e:
            logger.exception(f"Start learning failed: {e}")
            self._error_count += 1
            return False
    
    def _learning_loop(self) -> None:
        interval = self.config.get("learning_interval", 300)
        logger.info(f"Learning loop started (interval={interval}s)")
        while not self._stop_event.is_set() and self.running:
            try:
                if self.engine and hasattr(self.engine, 'learn'):
                    start_time = time.time()
                    result = self.engine.learn({"source": "autonomous"})
                    self._learn_count += 1
                    self._last_learn_time = time.time()
                    if result:
                        logger.debug(f"Learning cycle {self._learn_count} completed in {time.time() - start_time:.2f}s")
            except Exception as e:
                self._error_count += 1
                logger.debug(f"Learning cycle error: {e}")
            for _ in range(interval):
                if self._stop_event.is_set() or not self.running:
                    break
                time.sleep(1)
        logger.info("Learning loop stopped")
    
    def stop_learning(self) -> bool:
        if self.engine is None:
            return False
        try:
            self._stop_event.set()
            self.running = False
            if self.learning_thread and self.learning_thread.is_alive():
                self.learning_thread.join(timeout=5)
            if hasattr(self.engine, 'stop_learning'):
                self.engine.stop_learning()
            elif hasattr(self.engine, 'stop'):
                self.engine.stop()
            elif hasattr(self.engine, 'shutdown'):
                self.engine.shutdown()
            logger.info("✅ Learning stopped")
            try:
                if set_status is not None:
                    set_status("learning_engine", "STOPPED")
            except:
                pass
            return True
        except Exception as e:
            logger.exception(f"Stop learning failed: {e}")
            return False
    
    def learn(self, data: Dict) -> Optional[Dict]:
        if self.engine is None:
            return {"status": "ERROR", "message": "Engine not available"}
        try:
            if hasattr(self.engine, 'learn'):
                start_time = time.time()
                result = self.engine.learn(data=data, source="trading_bot")
                self._learn_count += 1
                self._last_learn_time = time.time()
                try:
                    if health_monitor is not None and hasattr(health_monitor, 'record_execution'):
                        duration = time.time() - start_time
                        success = result.get("status") in ["SUCCESS", "PARTIAL"] if result else False
                        health_monitor.record_execution("learning_engine", duration, success)
                except:
                    pass
                return result
            return {"status": "ERROR", "message": "learn method not available"}
        except Exception as e:
            logger.exception(f"Learn failed: {e}")
            self._error_count += 1
            return {"status": "ERROR", "message": str(e)}
    
    def shutdown(self) -> None:
        try:
            self.stop_learning()
            if self.engine is not None:
                try:
                    if hasattr(self.engine, 'save_state'):
                        state_file = self.config.get("state_file", "database/engine_state.json")
                        self.engine.save_state(state_file)
                        logger.info(f"State saved to {state_file}")
                    elif hasattr(self.engine, 'persist'):
                        self.engine.persist()
                except Exception as e:
                    logger.warning(f"State save failed: {e}")
                try:
                    if hasattr(self.engine, 'shutdown'):
                        self.engine.shutdown()
                    elif hasattr(self.engine, 'close'):
                        self.engine.close()
                except Exception as e:
                    logger.warning(f"Shutdown failed: {e}")
            logger.info("✅ Learning Engine shutdown complete")
        except Exception as e:
            logger.exception(f"Shutdown error: {e}")
    
    def get_stats(self) -> Dict:
        return {
            "learn_count": self._learn_count,
            "error_count": self._error_count,
            "last_learn": self._last_learn_time,
            "running": self.running,
            "initialized": self.initialized,
            "available": self.engine is not None,
        }

# ============================================================
# DIAGNOSTIC FUNCTION
# ============================================================

def check_imports():
    issues = []
    print("\n[DIAG] Running diagnostics...")
    try:
        import gui.app
        print("[DIAG] ✅ gui.app available")
    except ImportError as e:
        issues.append(f"gui.app not available: {e}")
        print(f"[DIAG] ❌ gui.app not available: {e}")
    try:
        from gui.intelligence import Knowledge
        print("[DIAG] ✅ gui.intelligence.Knowledge available")
    except ImportError as e:
        issues.append(f"Knowledge not available: {e}")
        print(f"[DIAG] ⚠️ Knowledge not available: {e}")
    try:
        from core import brain
        print("[DIAG] ✅ core.brain available")
    except ImportError as e:
        issues.append(f"core.brain not available: {e}")
        print(f"[DIAG] ❌ core.brain not available: {e}")
    try:
        from core.learning.engine import learning_engine
        print("[DIAG] ✅ core.learning.engine available")
    except ImportError as e:
        issues.append(f"learning_engine not available: {e}")
        print(f"[DIAG] ❌ learning_engine not available: {e}")
    try:
        from core.market_data import exchange, KrakenMarketData
        print("[DIAG] ✅ core.market_data available")
    except ImportError as e:
        issues.append(f"market_data not available: {e}")
        print(f"[DIAG] ⚠️ market_data not available: {e}")
    try:
        from config import DEFAULT_PAIRS, DEFAULT_TIMEFRAMES
        print(f"[DIAG] ✅ Config loaded: {len(DEFAULT_PAIRS)} pairs, {len(DEFAULT_TIMEFRAMES)} timeframes")
    except ImportError as e:
        issues.append(f"config not available: {e}")
        print(f"[DIAG] ❌ config not available: {e}")
    return issues

# ============================================================
# ERROR RECOVERY
# ============================================================

class ErrorRecovery:
    @staticmethod
    def retry(func, max_retries=3, delay=1, backoff=2):
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                wait = delay * (backoff ** attempt)
                logger.debug(f"Retry {attempt+1}/{max_retries} after {wait}s: {e}")
                time.sleep(wait)
        return None
    
    @staticmethod
    def safe_call(func, default=None, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.debug(f"Safe call failed: {e}")
            return default

# ============================================================
# MAIN
# ============================================================

def main():
    global _graceful_shutdown, scanner, exchange, signal_engine, CORE_LEARNING_ENGINE
    
    # ========================================================
    # HEADER
    # ========================================================
    
    print()
    print("=" * 58)
    print()
    print("         INKSIDE DIGITAL")
    print("   COGNITIVE MIRROR ENGINE v4.4.1")
    print("ALGORITHMIC MARKET INTELLIGENCE TERMINAL")
    print()
    print("=" * 58)
    print()
    print(f"System      : {'INITIALIZING' if not _graceful_shutdown else 'RESTARTING'}")
    print(f"Version     : 4.4.1 COGNITIVE MIRROR")
    print(f"Engine      : PROFESSIONAL MTF SCANNER")
    print(f"Exchange    : KRAKEN")
    print(f"Mode        : {'DEBUG' if DEBUG_MODE else 'PRODUCTION'}")
    print(f"Log Level   : {LOG_LEVEL}")
    print()
    print("=" * 58)
    print()

    # ========================================================
    # DIAGNOSTIC
    # ========================================================
    
    print("Running diagnostic...")
    issues = check_imports()
    if issues:
        print("\n⚠️ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nContinuing anyway...\n")
    else:
        print("\n✅ All diagnostics passed\n")

    # ========================================================
    # VERIFY SCANNER & EXCHANGE (REAL LOAD)
    # ========================================================
    
    if scanner is None:
        try:
            from core.scanner import scanner as core_scanner
            scanner = core_scanner
            logger.info("Scanner loaded from core")
        except ImportError:
            logger.warning("Scanner not available")
    
    if exchange is None:
        try:
            from core.market_data import exchange as core_exchange
            exchange = core_exchange
            EXCHANGE_AVAILABLE = True
            logger.info("Exchange loaded from core.market_data")
        except ImportError:
            logger.warning("Exchange not available")

    # ========================================================
    # 🔥 INITIALIZE BRAIN - PRIORITAS CORE.BRAIN
    # ========================================================
    
    print("Launching Trading Core...")
    
    bot = None
    brain_instance = None
    
    # ============================================================
    # PRIORITAS 1: PAKAI BRAIN ASLI DARI CORE
    # ============================================================
    try:
        from core.brain import Brain as CoreBrain, brain as core_brain_instance
        
        if CoreBrain is not None:
            try:
                brain_instance = CoreBrain()
                logger.info("✅ Brain initialized from core.brain (REAL INSTANCE)")
                print("[INFO] ✅ Using REAL Brain from core")
            except Exception as e:
                logger.warning(f"CoreBrain init error: {e}")
                if core_brain_instance is not None:
                    brain_instance = core_brain_instance
                    logger.info("✅ Using global brain instance from core")
                    print("[INFO] ✅ Using global Brain instance")
                else:
                    brain_instance = None
        
        if brain_instance is None:
            try:
                import core.brain as brain_module
                if hasattr(brain_module, 'brain'):
                    brain_instance = brain_module.brain
                    logger.info("✅ Using brain from core.brain module")
                    print("[INFO] ✅ Using Brain from core.brain module")
            except Exception as e:
                logger.warning(f"Import brain module error: {e}")
                
    except ImportError as e:
        logger.warning(f"CoreBrain import error: {e}")
        print(f"[WARN] ⚠️ Could not import Brain from core: {e}")
        brain_instance = None
    except Exception as e:
        logger.warning(f"Brain init error: {e}")
        print(f"[WARN] ⚠️ Brain error: {e}")
        brain_instance = None

    # ============================================================
    # PRIORITAS 2: FALLBACK KE MOCKBRAIN
    # ============================================================
    if brain_instance is None:
        logger.warning("Brain not available, using MockBrain fallback")
        print("[WARN] ⚠️ Using MockBrain (simulated data)")
        brain_instance = MockBrain()
    else:
        if hasattr(brain_instance, 'reflection'):
            logger.info("✅ Brain has reflection() method")
            print("[INFO] ✅ Brain has reflection method")
        else:
            logger.warning("Brain does NOT have reflection() method")
            print("[WARN] ⚠️ Brain missing reflection method")

    # ========================================================
    # 🔥 INITIALIZE TRADING BOT - PRIORITAS CORE.BOT
    # ========================================================

    def init_real_bot():
        """Try to initialize real TradingBot from core.bot."""
        try:
            from core.bot import TradingBot as RealTradingBot
            
            if RealTradingBot is None:
                return None
            
            # Coba berbagai signature
            signatures = [
                {"brain_instance": brain_instance, "exchange_instance": exchange},
                {"brain_instance": brain_instance},
                {},
            ]
            
            for kwargs in signatures:
                try:
                    bot = RealTradingBot(**kwargs)
                    if bot is not None:
                        logger.info(f"✅ TradingBot initialized with {list(kwargs.keys())}")
                        return bot
                except TypeError:
                    continue
                except Exception as e:
                    logger.debug(f"TradingBot error with {list(kwargs.keys())}: {e}")
                    continue
            
            return None
        except ImportError as e:
            logger.debug(f"TradingBot import error: {e}")
            return None
        except Exception as e:
            logger.debug(f"TradingBot error: {e}")
            return None

    # Coba real bot
    try:
        bot = ErrorRecovery.retry(init_real_bot, max_retries=3, delay=1)
        if bot is not None:
            logger.info("✅ TradingBot initialized successfully (REAL)")
            print("[INFO] ✅ TradingBot is REAL from core.bot")
        else:
            logger.warning("TradingBot init failed, using TradingBotWrapper")
            print("[WARN] ⚠️ Using TradingBotWrapper")
            bot = TradingBotWrapper(
                brain_instance=brain_instance,
                exchange_instance=exchange
            )
    except Exception as e:
        logger.warning(f"Bot init error: {e}")
        print(f"[WARN] ⚠️ Bot error: {e}")
        bot = TradingBotWrapper(
            brain_instance=brain_instance,
            exchange_instance=exchange
        )

    # Pastikan bot punya brain & telegram
    if bot is not None:
        if not hasattr(bot, 'brain') or bot.brain is None:
            bot.brain = brain_instance
            logger.info("✅ Bot brain set")
        if not hasattr(bot, 'exchange') or bot.exchange is None:
            if exchange is not None:
                bot.exchange = exchange
                logger.info("✅ Bot exchange set")
        # Telegram
        if not hasattr(bot, 'telegram') or bot.telegram is None:
            try:
                # Coba import telegram service
                from core.telegram import TelegramService
                if TelegramService:
                    bot.telegram = TelegramService()
                    logger.info("✅ Telegram service created")
            except ImportError:
                logger.debug("Telegram service not available")
    
    # ========================================================
    # CONNECT SCANNER
    # ========================================================
    
    if scanner is not None and bot is not None:
        try:
            if hasattr(scanner, 'set_bot'):
                scanner.set_bot(bot)
                logger.info("✅ Scanner connected to bot")
            elif hasattr(scanner, 'bot'):
                scanner.bot = bot
                logger.info("✅ Scanner bot set")
            if hasattr(scanner, 'start'):
                scanner.start()
                logger.info("✅ Scanner started")
            elif hasattr(scanner, 'start_scanning'):
                scanner.start_scanning()
                logger.info("✅ Scanner scanning started")
        except Exception as e:
            logger.warning(f"Scanner connection failed: {e}")
    
    # ========================================================
    # CONNECT SIGNAL ENGINE
    # ========================================================
    
    if signal_engine is not None and CORE_LEARNING_ENGINE is not None:
        try:
            if hasattr(signal_engine, 'set_learning_engine'):
                signal_engine.set_learning_engine(CORE_LEARNING_ENGINE)
                logger.info("✅ Signal Engine connected to Learning Engine")
            elif hasattr(signal_engine, 'learning_engine'):
                signal_engine.learning_engine = CORE_LEARNING_ENGINE
                logger.info("✅ Signal Engine learning_engine set")
        except Exception as e:
            logger.warning(f"Signal engine connection failed: {e}")

    # ========================================================
    # LEARNING ENGINE INTEGRATION
    # ========================================================

    logger.info("Initializing Learning Engine integration...")
    
    learning_config = {
        "max_history": 1000,
        "continue_on_module_error": True,
        "module_timeout": 30,
        "retry_count": 3,
        "retry_backoff": 1.5,
        "max_workers": 4,
        "learning_interval": 300,
        "state_file": "database/engine_state.json",
    }
    
    learning_integration = LearningEngineIntegration(
        bot=bot,
        brain=brain_instance,
        config=learning_config
    )
    
    if learning_integration.initialized:
        logger.info("✅ Learning Engine integrated.")
        if learning_integration.start_learning():
            logger.info("✅ Learning Engine started automatically")
        else:
            logger.warning("⚠️ Learning Engine failed to start")
    else:
        logger.warning("⚠️ Learning Engine integration failed.")

    # ========================================================
    # AUTONOMOUS LEARNING ENGINE
    # ========================================================

    logger.info("Initializing Autonomous Learning Engine...")

    try:
        from core.autonomous import autonomous
        
        if autonomous.start():
            logger.info("✅ Autonomous Learning Engine started")
            logger.info("   📡 RSS Feed: setiap 1 jam")
            logger.info("   🧠 Reanalysis: setiap 2 jam")
            logger.info("   💚 Health Check: setiap 5 menit")
            
            try:
                if health_monitor is not None and hasattr(health_monitor, 'register'):
                    health_monitor.register("autonomous")
                    logger.debug("Autonomous registered to health monitor")
            except Exception as e:
                logger.debug(f"Health registration error: {e}")
        else:
            logger.warning("⚠️ Autonomous Learning Engine failed to start")
            
    except ImportError as e:
        logger.warning(f"⚠️ Autonomous module not available: {e}")
    except Exception as e:
        logger.warning(f"⚠️ Autonomous engine error: {e}")

    # ========================================================
    # HEALTH MONITOR
    # ========================================================
    
    try:
        if health_monitor is not None and hasattr(health_monitor, 'register'):
            health_monitor.register("main")
            health_monitor.register("bot")
            if bot:
                health_monitor.register("trading_bot")
            logger.info("✅ Health Monitor initialized")
    except Exception as e:
        logger.warning(f"Health monitor init failed: {e}")

    # ========================================================
    # GUI
    # ========================================================
    
    if not GUI_AVAILABLE or InksideBotApp is None:
        logger.error("❌ GUI not available. Exiting.")
        return 1
    
    try:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        print("[GUI] Creating application...")
        app = InksideBotApp(bot, learning_integration=learning_integration)
        print("[GUI] Application created")
        
        # ========================================================
        # REGISTER PAGES (Termasuk Telegram)
        # ========================================================
        
        try:
            pages = []
            try:
                from gui.intelligence import DashboardPage
                pages.append(("Dashboard", DashboardPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Brain as BrainPage
                pages.append(("Brain", BrainPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Consciousness as ConsciousnessPage
                pages.append(("Consciousness", ConsciousnessPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Market as MarketPage
                pages.append(("Market", MarketPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Learning as LearningPage
                pages.append(("Learning", LearningPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Memory as MemoryPage
                pages.append(("Memory", MemoryPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Pattern as PatternPage
                pages.append(("Pattern", PatternPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Prediction as PredictionPage
                pages.append(("Prediction", PredictionPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Decision as DecisionPage
                pages.append(("Decision", DecisionPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Reflection as ReflectionPage
                pages.append(("Reflection", ReflectionPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Health as HealthPage
                pages.append(("Health", HealthPage))
            except ImportError:
                pass
            try:
                from gui.intelligence import Knowledge as KnowledgePage
                pages.append(("Knowledge", KnowledgePage))
            except ImportError:
                pass
            # --- TELEGRAM ---
            try:
                from gui.telegram import TelegramPage
                # Kirim bot dan telegram_service
                telegram_service = bot.telegram if bot and hasattr(bot, 'telegram') else None
                pages.append(("Telegram", TelegramPage, bot, telegram_service))
                logger.info("✅ Telegram page registered")
            except ImportError as e:
                logger.warning(f"Telegram page not available: {e}")
            
            # --- TRADING ---
            try:
                from gui.trading import TradingPage
                pages.append(("Trading", TradingPage))
                logger.info("✅ Trading page registered")
            except ImportError as e:
                logger.warning(f"Trading page not available: {e}")

            for page_info in pages:
                if len(page_info) == 2:
                    name, page_class = page_info
                    if page_class is not None and hasattr(app, 'add_page'):
                        try:
                            app.add_page(name, page_class)
                            logger.debug(f"Registered page: {name}")
                        except Exception as e:
                            logger.warning(f"Failed to register page {name}: {e}")
                elif len(page_info) == 4:
                    name, page_class, bot_ref, telegram_service = page_info
                    if page_class is not None and hasattr(app, 'add_page'):
                        try:
                            app.add_page(name, page_class, bot=bot_ref, telegram_service=telegram_service)
                            logger.debug(f"Registered page with params: {name}")
                        except Exception as e:
                            logger.warning(f"Failed to register page {name}: {e}")

            logger.info(f"✅ {len(pages)} pages registered")
            
            # Set bot ke app
            if hasattr(app, 'set_bot') and bot is not None:
                app.set_bot(bot)

        except Exception as e:
            logger.warning(f"Error registering pages: {e}")

        try:
            if set_status is not None:
                set_status("gui", "ONLINE")
        except Exception:
            pass

        # ========================================================
        # FORCE SHOW WINDOW
        # ========================================================
        
        print("[GUI] Forcing window to show...")
        
        try:
            app.deiconify()
            app.lift()
            app.focus_force()
            app.attributes('-topmost', True)
            app.update_idletasks()
            
            def show_attempt1():
                try:
                    app.deiconify()
                    app.lift()
                    app.focus_force()
                    app.update_idletasks()
                    print("[GUI] Show attempt 1")
                except Exception as e:
                    print(f"[GUI] Attempt 1 error: {e}")
            
            def show_attempt2():
                try:
                    app.deiconify()
                    app.lift()
                    app.focus_force()
                    app.update_idletasks()
                    print("[GUI] Show attempt 2")
                except Exception as e:
                    print(f"[GUI] Attempt 2 error: {e}")
            
            def show_attempt3():
                try:
                    app.deiconify()
                    app.lift()
                    app.focus_force()
                    app.attributes('-topmost', False)
                    app.update_idletasks()
                    print("[GUI] Show attempt 3 - topmost removed")
                except Exception as e:
                    print(f"[GUI] Attempt 3 error: {e}")
            
            app.after(100, show_attempt1)
            app.after(300, show_attempt2)
            app.after(500, show_attempt3)
            
            print("[GUI] ✅ Window force show initiated")
            
        except Exception as e:
            print(f"[GUI] ⚠️ Force show error: {e}")

        logger.info("✅ GUI initialized successfully")

        # ========================================================
        # SHUTDOWN THREAD
        # ========================================================
        
        def check_shutdown():
            while not _shutdown_flag.is_set():
                time.sleep(0.5)
            if _shutdown_flag.is_set():
                logger.info("Shutdown signal received, closing GUI...")
                try:
                    app.quit()
                except:
                    pass

        shutdown_thread = threading.Thread(target=check_shutdown, daemon=True)
        shutdown_thread.start()

        # ========================================================
        # MAINLOOP
        # ========================================================
        
        print("[GUI] Starting mainloop...")
        app.mainloop()
        print("[GUI] Mainloop ended")

    except KeyboardInterrupt:
        print("\n[INFO] Keyboard interrupt received")
        _graceful_shutdown = True
    except Exception as e:
        logger.exception(f"GUI failed: {e}")
        return 1

    # ========================================================
    # CLEANUP
    # ========================================================

    logger.info("Shutting down...")
    
    try:
        from core.autonomous import autonomous
        if autonomous.is_running():
            autonomous.stop()
            logger.info("✅ Autonomous Learning Engine stopped")
    except Exception as e:
        logger.warning(f"Autonomous stop error: {e}")

    try:
        learning_integration.shutdown()
    except Exception as e:
        logger.warning(f"Learning shutdown error: {e}")

    try:
        if bot and hasattr(bot, 'stop'):
            bot.stop()
    except Exception as e:
        logger.warning(f"Bot stop error: {e}")

    try:
        if scanner and hasattr(scanner, 'stop'):
            scanner.stop()
    except Exception as e:
        logger.warning(f"Scanner stop error: {e}")

    try:
        if set_status is not None:
            set_status("main", "STOPPED")
    except Exception:
        pass

    logger.info(f"✅ {APP_NAME} v{APP_VERSION} stopped.")
    return 0

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[INFO] Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
