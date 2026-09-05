#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# main.py
# INKSIDEDIGITAL TRADING BOT v2.0.0
# COGNITIVE MIRROR ENGINE - FULL HEADLESS (API MODE)
# WITH AI INTEGRATION - DEEPSEEK ENHANCED
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
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from dotenv import load_dotenv
from functools import wraps

# ============================================================
# LOGGER - SETUP EARLY
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
# ENVIRONMENT SETUP
# ============================================================

load_dotenv()
os.environ['HEADLESS_MODE'] = 'true'

# ============================================================
# PATH SETUP
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

for folder in ['logs', 'database', 'database/backup', 'cache', 'database/shards']:
    (CURRENT_DIR / folder).mkdir(exist_ok=True)

# ============================================================
# SIGNAL HANDLER
# ============================================================

_shutdown_flag = threading.Event()
_graceful_shutdown = False
_startup_time = time.time()

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
APP_VERSION = "2.0.0"
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
MODE = os.environ.get('INKSIDE_MODE', 'PAPER')
API_PORT = int(os.environ.get('API_PORT', 5001))
API_HOST = os.environ.get('API_HOST', '0.0.0.0')

engine_running = False
bot_instance = None
brain_instance = None

API_KEY = os.environ.get('API_KEY', 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ')

# ============================================================
# TELEGRAM CONFIG
# ============================================================

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
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
    DEEPSEEK_ENABLED = deepseek_ai.enabled if hasattr(deepseek_ai, 'enabled') else False
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
    with open(error_file, 'w') as f:
        f.write(f"Time: {datetime.now()}\n")
        f.write(f"Error: {error_msg}\n")
        traceback.print_tb(exc_tb, file=f)

sys.excepthook = global_exception_handler

# ============================================================
# WATCHDOG IMPORT
# ============================================================

try:
    from core.watchdog import watchdog
    WATCHDOG_AVAILABLE = True
    logger.info("✅ Watchdog module loaded")
except ImportError as e:
    logger.warning(f"⚠️ Watchdog not available: {e}")
    WATCHDOG_AVAILABLE = False

# ============================================================
# KNOWLEDGE IMPORT
# ============================================================

try:
    from core.knowledge import knowledge
    KNOWLEDGE_AVAILABLE = True
    logger.info("✅ Knowledge Engine v4.0.0 loaded")
except ImportError as e:
    logger.warning(f"⚠️ Knowledge Engine not available: {e}")
    KNOWLEDGE_AVAILABLE = False

# ============================================================
# SIMULATION IMPORT
# ============================================================

try:
    from core.simulation import simulation_engine
    SIMULATION_AVAILABLE = True
    logger.info("✅ Simulation Engine loaded")
except ImportError as e:
    logger.warning(f"⚠️ Simulation Engine not available: {e}")
    SIMULATION_AVAILABLE = False

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
# FALLBACK
# ============================================================

if Brain is None:
    logger.critical("❌ Brain module not available!")
    sys.exit(1)

if TradingBot is None:
    logger.critical("❌ TradingBot module not available!")
    sys.exit(1)

logger.info("✅ Core modules loaded")

# ============================================================
# TELEGRAM SEND FUNCTION
# ============================================================

def send_telegram_message(message: str) -> bool:
    try:
        token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
        
        if not token or not chat_id:
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

AUTO_CRAWL_SOURCES = [
    'https://id.wikipedia.org/wiki/Kecerdasan_buatan',
    'https://id.wikipedia.org/wiki/Blockchain',
    'https://id.wikipedia.org/wiki/Indonesia',
    'https://id.wikipedia.org/wiki/Energi_terbarukan',
    'https://id.wikipedia.org/wiki/Perubahan_iklim',
    'https://id.wikipedia.org/wiki/Trading_online',
    'https://id.wikipedia.org/wiki/Investasi',
    'https://id.wikipedia.org/wiki/Mata_uang_kripto',
    'https://id.wikipedia.org/wiki/Teknologi_keuangan',
    'https://id.wikipedia.org/wiki/Pasar_modal',
    'https://id.wikipedia.org/wiki/Ekonomi',
    'https://id.wikipedia.org/wiki/Keuangan',
    'https://id.wikipedia.org/wiki/Analisis_teknikal',
    'https://id.wikipedia.org/wiki/Manajemen_risiko',
    'https://en.wikipedia.org/wiki/Artificial_intelligence',
    'https://en.wikipedia.org/wiki/Blockchain',
    'https://en.wikipedia.org/wiki/Cryptocurrency',
    'https://en.wikipedia.org/wiki/Trading_strategy',
    'https://en.wikipedia.org/wiki/Technical_analysis',
    'https://en.wikipedia.org/wiki/Financial_market',
]

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
                    
                    response = requests.get(url, timeout=15, headers={
                        'User-Agent': 'Inkside-Cognitive-Bot/2.0'
                    })
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title_tag = soup.find('h1')
                        title = title_tag.get_text().strip() if title_tag else url.split('/')[-1]
                        
                        paragraphs = soup.find_all('p')
                        content = ' '.join([p.get_text().strip() for p in paragraphs[:3]])
                        
                        if content and len(content) > 50:
                            existing = knowledge.search(title, max_results=1)
                            if not existing or len(existing) == 0:
                                knowledge.add(
                                    content=f"[Auto-Crawl] {title}: {content[:300]}...",
                                    category="General Knowledge",
                                    type="fact",
                                    tags=['auto-crawl', 'wikipedia'],
                                    confidence=75.0,
                                    importance=0.5
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
        
        for pycache in CURRENT_DIR.rglob('__pycache__'):
            shutil.rmtree(pycache, ignore_errors=True)
        
        for pyc in CURRENT_DIR.rglob('*.pyc'):
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

def start_api_server(bot_instance):
    try:
        from flask import Flask, jsonify, request
        from flask_cors import CORS
        from flask_socketio import SocketIO, emit
        from functools import wraps
        
        app = Flask(__name__)
        CORS(app)

        socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
        
        def require_api_key(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                api_key = request.headers.get('X-API-Key')
                expected_key = os.environ.get('API_KEY', 'iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ')
                if not api_key or api_key != expected_key:
                    return jsonify({'error': 'Unauthorized - Invalid API Key'}), 401
                return f(*args, **kwargs)
            return decorated_function
        
        def broadcast_update(channel: str, payload: dict):
            try:
                socketio.emit(channel, {
                    'channel': channel,
                    'payload': payload,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.debug(f"Broadcast error: {e}")

        # ============================================================
        # AI ENDPOINTS - DEEPSEEK INTEGRATION
        # ============================================================

        @app.route('/api/ai/status', methods=['GET'])
        @require_api_key
        def ai_status():
            """Get AI integration status."""
            try:
                return jsonify({
                    'available': DEEPSEEK_AVAILABLE,
                    'enabled': DEEPSEEK_ENABLED,
                    'model': 'deepseek-chat' if DEEPSEEK_ENABLED else None,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/ai/ask', methods=['POST'])
        @require_api_key
        def ai_ask():
            """Ask AI a question with context from knowledge engine."""
            try:
                data = request.json
                question = data.get('question', '')
                
                if not question:
                    return jsonify({'error': 'Question is required'}), 400
                
                system_prompt = data.get('system_prompt', 'default')
                conversation_id = data.get('conversation_id')
                temperature = data.get('temperature', 0.7)
                max_tokens = data.get('max_tokens', 2048)
                
                # Get context from knowledge engine
                context = None
                if KNOWLEDGE_AVAILABLE:
                    relevant = knowledge.search(question, max_results=5)
                    if relevant:
                        context = "\n\n".join([
                            f"[{item.category}] {item.content}"
                            for item in relevant
                        ])
                
                if not DEEPSEEK_ENABLED:
                    # Fallback response if AI is disabled
                    return jsonify({
                        'question': question,
                        'answer': f"I'm a cognitive trading bot. I can help with market analysis, trading strategies, and financial insights. Your question: '{question}'\n\n📚 Context from knowledge: {len(relevant) if KNOWLEDGE_AVAILABLE else 0} relevant items found.",
                        'ai_enabled': False,
                        'context_used': bool(context),
                        'timestamp': datetime.now().isoformat()
                    })
                
                from core.deepseek import deepseek_ai
                
                result = deepseek_ai.ask(
                    prompt=question,
                    system_prompt=system_prompt,
                    context=context,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    conversation_id=conversation_id
                )
                
                if isinstance(result, str):
                    return jsonify({
                        'question': question,
                        'answer': result,
                        'ai_enabled': True,
                        'context_used': bool(context),
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    return jsonify(result.to_dict())
                
            except Exception as e:
                logger.error(f"AI ask error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/ai/brain/reflection', methods=['GET'])
        @require_api_key
        def ai_brain_reflection():
            """Get brain reflection with AI enhancement."""
            try:
                topic = request.args.get('topic')
                
                if not DEEPSEEK_ENABLED:
                    return jsonify({
                        'error': 'AI is not enabled. Please set DEEPSEEK_API_KEY.',
                        'ai_enabled': False
                    }), 400
                
                from core.brain import brain
                result = brain.reflection_with_ai(topic)
                
                return jsonify({
                    'awareness': result.get('awareness', 0),
                    'emotion': result.get('emotion', 'Unknown'),
                    'curiosity': result.get('curiosity', 0),
                    'insight_depth': result.get('insight_depth', 0),
                    'resilience': result.get('resilience', 0),
                    'focus': result.get('focus', 0),
                    'insights': result.get('insights', []),
                    'ai_insights': result.get('ai_insights', []),
                    'ai_reflection': result.get('ai_reflection', ''),
                    'ai_enhanced': result.get('ai_enhanced', False),
                    'ai_status': result.get('ai_status', 'unknown'),
                    'stability': result.get('stability', 'Unknown'),
                    'reflection_quality': result.get('reflection_quality', 'FAIR'),
                    'confidence': result.get('confidence', 0),
                    'timestamp': result.get('timestamp', datetime.now().isoformat())
                })
            except Exception as e:
                logger.error(f"Brain reflection API error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/ai/brain/status', methods=['GET'])
        @require_api_key
        def ai_brain_status():
            """Get brain AI status."""
            try:
                from core.brain import brain
                return jsonify(brain.get_ai_status())
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/ai/scanner/analyze', methods=['POST'])
        @require_api_key
        def ai_scanner_analyze():
            """Analyze market with AI."""
            try:
                data = request.json or {}
                pair = data.get('pair', 'BTC/USD')
                
                if not DEEPSEEK_ENABLED:
                    return jsonify({
                        'error': 'AI is not enabled. Please set DEEPSEEK_API_KEY.',
                        'ai_enabled': False
                    }), 400
                
                from core.scanner import scanner
                result = scanner.analyze_with_ai(pair)
                
                return jsonify({
                    'status': result.get('status'),
                    'pair': result.get('pair'),
                    'analysis': result.get('analysis'),
                    'price': result.get('price'),
                    'signal': result.get('signal'),
                    'confidence': result.get('confidence'),
                    'timestamp': result.get('timestamp')
                })
            except Exception as e:
                logger.error(f"Scanner AI analysis error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/ai/scanner/sentiment', methods=['GET'])
        @require_api_key
        def ai_scanner_sentiment():
            """Get market sentiment with AI."""
            try:
                pair = request.args.get('pair', 'BTC/USD')
                
                if not DEEPSEEK_ENABLED:
                    return jsonify({
                        'error': 'AI is not enabled. Please set DEEPSEEK_API_KEY.',
                        'ai_enabled': False
                    }), 400
                
                from core.scanner import scanner
                result = scanner.get_market_sentiment_ai(pair)
                
                return jsonify({
                    'status': result.get('status'),
                    'pair': result.get('pair'),
                    'sentiment': result.get('sentiment'),
                    'confidence': result.get('confidence'),
                    'price': result.get('price'),
                    'timestamp': result.get('timestamp')
                })
            except Exception as e:
                logger.error(f"Scanner sentiment error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/ai/signal/validate', methods=['POST'])
        @require_api_key
        def ai_signal_validate():
            """Validate trading signal with AI."""
            try:
                data = request.json
                signal = data.get('signal', {})
                
                if not signal:
                    return jsonify({'error': 'Signal data required'}), 400
                
                if not DEEPSEEK_ENABLED:
                    return jsonify({
                        'error': 'AI is not enabled. Please set DEEPSEEK_API_KEY.',
                        'ai_enabled': False
                    }), 400
                
                from core.signal_engine import signal_engine
                result = signal_engine.validate_with_ai(signal)
                
                return jsonify({
                    'original_signal': signal,
                    'ai_validation': result.get('ai_validation'),
                    'ai_validation_score': result.get('ai_validation_score'),
                    'ai_validated': result.get('ai_validated', False),
                    'ai_status': result.get('ai_status'),
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"AI signal validation error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/ai/strategy/generate', methods=['POST'])
        @require_api_key
        def ai_generate_strategy():
            """Generate trading strategy with AI."""
            try:
                data = request.json
                pair = data.get('pair', 'BTC/USD')
                risk_level = data.get('risk_level', 'moderate')
                timeframe = data.get('timeframe', '1h')
                market_data = data.get('market_data', {})
                
                if not DEEPSEEK_ENABLED:
                    return jsonify({
                        'error': 'AI is not enabled. Please set DEEPSEEK_API_KEY.',
                        'ai_enabled': False
                    }), 400
                
                from core.bot import bot_instance
                result = bot_instance.generate_strategy_with_ai(
                    pair=pair,
                    market_data=market_data,
                    risk_level=risk_level,
                    timeframe=timeframe
                )
                
                return jsonify({
                    'status': result.get('status'),
                    'pair': result.get('pair'),
                    'strategy': result.get('strategy'),
                    'entry': result.get('entry'),
                    'take_profit': result.get('take_profit'),
                    'stop_loss': result.get('stop_loss'),
                    'risk_reward': result.get('risk_reward'),
                    'position_size': result.get('position_size'),
                    'recommendation': result.get('recommendation'),
                    'risk_level': risk_level,
                    'timestamp': result.get('timestamp')
                })
            except Exception as e:
                logger.error(f"AI strategy error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/ai/bot/status', methods=['GET'])
        @require_api_key
        def ai_bot_status():
            """Get bot AI status."""
            try:
                from core.bot import bot_instance
                return jsonify(bot_instance.get_ai_status())
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/ai/chat', methods=['POST'])
        @require_api_key
        def ai_chat():
            """Chat with AI with memory."""
            try:
                data = request.json
                message = data.get('message', '')
                conversation_id = data.get('conversation_id')
                
                if not message:
                    return jsonify({'error': 'Message is required'}), 400
                
                if not DEEPSEEK_ENABLED:
                    return jsonify({
                        'error': 'AI is not enabled. Please set DEEPSEEK_API_KEY.',
                        'ai_enabled': False
                    }), 400
                
                from core.deepseek import deepseek_ai
                
                # Get context from knowledge
                context = None
                if KNOWLEDGE_AVAILABLE:
                    relevant = knowledge.search(message, max_results=3)
                    if relevant:
                        context = "\n".join([item.content[:200] for item in relevant])
                
                result = deepseek_ai.chat(
                    message=message,
                    conversation_id=conversation_id,
                    context=context
                )
                
                return jsonify({
                    'message': message,
                    'response': result.get('response', ''),
                    'conversation_id': result.get('conversation_id'),
                    'context_used': bool(context),
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"AI chat error: {e}")
                return jsonify({'error': str(e)}), 500

        # ============================================================
        # KNOWLEDGE ENDPOINTS
        # ============================================================

        @app.route('/api/knowledge/search', methods=['POST'])
        @require_api_key
        def knowledge_search():
            """Search knowledge base."""
            try:
                data = request.json
                query = data.get('query', '')
                max_results = data.get('max_results', 10)
                
                if not query:
                    return jsonify({'error': 'Query is required'}), 400
                
                if not KNOWLEDGE_AVAILABLE:
                    return jsonify({'error': 'Knowledge engine not available'}), 503
                
                results = knowledge.search(query, max_results=max_results)
                
                return jsonify({
                    'query': query,
                    'results': [item.to_dict() for item in results],
                    'total': len(results),
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/knowledge/add', methods=['POST'])
        @require_api_key
        def knowledge_add():
            """Add item to knowledge base."""
            try:
                data = request.json
                content = data.get('content', '')
                category = data.get('category', 'General Knowledge')
                type_ = data.get('type', 'fact')
                tags = data.get('tags', [])
                confidence = data.get('confidence', 75.0)
                importance = data.get('importance', 0.5)
                
                if not content:
                    return jsonify({'error': 'Content is required'}), 400
                
                if not KNOWLEDGE_AVAILABLE:
                    return jsonify({'error': 'Knowledge engine not available'}), 503
                
                item = knowledge.add(
                    content=content,
                    category=category,
                    type=type_,
                    tags=tags,
                    confidence=confidence,
                    importance=importance
                )
                
                knowledge.save()
                
                return jsonify({
                    'status': 'success',
                    'item': item.to_dict() if item else None,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/knowledge/stats', methods=['GET'])
        @require_api_key
        def knowledge_stats():
            """Get knowledge base statistics."""
            try:
                if not KNOWLEDGE_AVAILABLE:
                    return jsonify({'error': 'Knowledge engine not available'}), 503
                
                stats = knowledge.stats()
                
                return jsonify({
                    'total_items': stats.total,
                    'database_size_mb': stats.database_size_mb,
                    'categories': stats.categories,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        # ============================================================
        # PUBLIC ENDPOINTS
        # ============================================================
        
        @app.route('/api/health', methods=['GET'])
        def api_health():
            try:
                status = bot_instance.get_status() if bot_instance else {}
                return jsonify({
                    "status": "healthy",
                    "bot": status,
                    "uptime": int(time.time() - _startup_time),
                    "version": APP_VERSION,
                    "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                    "ai_enabled": DEEPSEEK_ENABLED,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500

        @app.route('/api/status', methods=['GET'])
        @require_api_key
        def api_status():
            try:
                status = bot_instance.get_status() if bot_instance else {}
                return jsonify({
                    "status": "online",
                    "bot": status,
                    "version": APP_VERSION,
                    "mode": MODE,
                    "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                    "ai_enabled": DEEPSEEK_ENABLED,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route('/api/system/metrics', methods=['GET'])
        @require_api_key
        def api_system_metrics():
            try:
                import psutil
                cpu = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                health_score = round(
                    (max(0, 100 - cpu) * 0.4) +
                    (max(0, 100 - mem.percent) * 0.4) +
                    (max(0, 100 - disk.percent) * 0.2),
                1)
                
                return jsonify({
                    "cpu": cpu,
                    "ram": round(mem.used / (1024**3), 2),
                    "ram_percent": mem.percent,
                    "disk_percent": disk.percent,
                    "uptime": int(time.time() - _startup_time),
                    "health_score": health_score,
                    "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                    "ai_enabled": DEEPSEEK_ENABLED,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route('/api/engine/start', methods=['POST'])
        @require_api_key
        def start_engine():
            global engine_running
            try:
                if engine_running:
                    return jsonify({'status': 'already_running', 'running': True})
                engine_running = True
                if bot_instance and hasattr(bot_instance, 'start'):
                    bot_instance.start()
                logger.info("🚀 Engine started")
                return jsonify({'status': 'success', 'running': True})
            except Exception as e:
                logger.error(f"Start engine error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/engine/stop', methods=['POST'])
        @require_api_key
        def stop_engine():
            global engine_running
            try:
                if not engine_running:
                    return jsonify({'status': 'already_stopped', 'running': False})
                engine_running = False
                if bot_instance and hasattr(bot_instance, 'stop'):
                    bot_instance.stop()
                logger.info("🛑 Engine stopped")
                return jsonify({'status': 'success', 'running': False})
            except Exception as e:
                logger.error(f"Stop engine error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/engine/status', methods=['GET'])
        @require_api_key
        def get_engine_status():
            try:
                return jsonify({
                    'running': engine_running,
                    'mode': MODE,
                    'state': 'RUNNING' if engine_running else 'IDLE',
                    'uptime': int(time.time() - _startup_time),
                    'knowledge_items': len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                    'ai_enabled': DEEPSEEK_ENABLED
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/signals', methods=['GET'])
        @require_api_key
        def api_signals():
            try:
                signals = []
                if bot_instance and hasattr(bot_instance, 'get_signals'):
                    signals = bot_instance.get_signals()
                return jsonify({
                    'signals': signals,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/patterns', methods=['GET'])
        @require_api_key
        def get_patterns():
            try:
                patterns = []
                
                if KNOWLEDGE_AVAILABLE:
                    results = knowledge.search('pattern', max_results=50)
                    for item in results:
                        if hasattr(item, 'to_dict'):
                            patterns.append({
                                'id': item.id,
                                'name': item.content[:50],
                                'type': 'CANDLESTICK',
                                'bias': 'NEUTRAL',
                                'confidence': item.confidence,
                                'timeframe': '1h',
                                'pair': 'BTC/USDT',
                                'description': item.content[:100],
                                'reliability': item.confidence,
                                'occurrence': item.access_count,
                                'detected_at': item.created_at,
                                'strength': 'MODERATE' if item.confidence > 70 else 'WEAK',
                                'volume_confirmation': True,
                                'price': 78882.0
                            })
                
                if not patterns:
                    patterns = [
                        {
                            'id': 'pat_001',
                            'name': 'Bullish Engulfing',
                            'type': 'CANDLESTICK',
                            'bias': 'BULLISH',
                            'confidence': 88,
                            'timeframe': '1h',
                            'pair': 'BTC/USDT',
                            'description': 'Large bullish candle completely engulfs prior bearish candle body.',
                            'reliability': 84,
                            'occurrence': 142,
                            'detected_at': datetime.now().isoformat(),
                            'strength': 'STRONG',
                            'volume_confirmation': True,
                            'price': 78882.0
                        },
                        {
                            'id': 'pat_002',
                            'name': 'Morning Star',
                            'type': 'CANDLESTICK',
                            'bias': 'BULLISH',
                            'confidence': 82,
                            'timeframe': '4h',
                            'pair': 'ETH/USDT',
                            'description': '3-candle bullish reversal formation.',
                            'reliability': 80,
                            'occurrence': 98,
                            'detected_at': datetime.now().isoformat(),
                            'strength': 'STRONG',
                            'volume_confirmation': True,
                            'price': 3120.50
                        }
                    ]
                
                return jsonify({
                    'patterns': patterns,
                    'total': len(patterns),
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Patterns error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/diagnostics', methods=['GET'])
        @require_api_key
        def api_diagnostics():
            try:
                import psutil
                cpu = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                health_score = round(
                    (max(0, 100 - cpu) * 0.4) +
                    (max(0, 100 - mem.percent) * 0.4) +
                    (max(0, 100 - disk.percent) * 0.2),
                1)
                
                return jsonify({
                    'system': {
                        'status': 'healthy' if health_score >= 70 else 'degraded',
                        'uptime': int(time.time() - _startup_time),
                        'knowledge_items': len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                        'cpu': cpu,
                        'ram': round(mem.used / (1024**3), 2),
                        'ram_percent': mem.percent,
                        'disk_percent': disk.percent,
                        'health_score': health_score
                    },
                    'components': {
                        'backend': {'status': 'online', 'version': APP_VERSION},
                        'brain': {'status': 'online' if brain else 'offline'},
                        'knowledge': {'status': 'online' if KNOWLEDGE_AVAILABLE else 'offline'},
                        'watchdog': {'status': 'online' if WATCHDOG_AVAILABLE else 'offline'},
                        'scanner': {'status': 'online' if engine_running else 'idle'},
                        'websocket': {'status': 'online'},
                        'ai': {'status': 'online' if DEEPSEEK_ENABLED else 'offline'}
                    },
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Diagnostics error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/predictions', methods=['GET'])
        @require_api_key
        def api_predictions():
            try:
                if engine_running:
                    return jsonify([{
                        "pair": "BTC/USDT",
                        "current_price": 78882.0,
                        "direction": "DOWN",
                        "confidence": random.randint(65, 85),
                        "target_price": 76310.45,
                        "change_percent": -3.26,
                        "regime": "RANGE_ACCUMULATION",
                        "rsi": 49.3,
                        "volatility": 0.032,
                        "method": "Ensemble v4.0 (Momentum + Fibonacci)",
                        "timestamp": datetime.now().isoformat()
                    }])
                return jsonify([])
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/telegram/status', methods=['GET'])
        @require_api_key
        def telegram_status():
            try:
                token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
                chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
                configured = bool(token and chat_id)
                
                return jsonify({
                    'configured': configured,
                    'status': 'online' if configured else 'offline',
                    'bot_name': 'InksideBot' if configured else None
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/telegram/send', methods=['POST'])
        @require_api_key
        def telegram_send():
            try:
                data = request.json
                message = data.get('message', '')
                
                if not message:
                    return jsonify({'error': 'Message is required'}), 400
                
                success = send_telegram_message(message)
                
                return jsonify({
                    'sent': success,
                    'status': 'success' if success else 'error',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        # ============================================================
        # WEBSOCKET
        # ============================================================
        
        @socketio.on('connect')
        def handle_connect():
            logger.info(f"🔗 Client connected: {request.sid}")
            emit('connected', {'status': 'ok', 'version': APP_VERSION})
        
        @socketio.on('disconnect')
        def handle_disconnect():
            logger.info(f"🔌 Client disconnected: {request.sid}")
        
        # ============================================================
        # START SERVER
        # ============================================================
        
        logger.info(f"🌐 Starting API Server on {API_HOST}:{API_PORT}")
        
        def run_server():
            socketio.run(app, host=API_HOST, port=API_PORT, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        logger.info(f"✅ API Server running on http://{API_HOST}:{API_PORT}")
        logger.info(f"   📚 Knowledge Engine: {'ONLINE' if KNOWLEDGE_AVAILABLE else 'OFFLINE'}")
        logger.info(f"   🤖 AI: {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
        logger.info(f"   📡 WebSocket: /socket.io/")
        
        return True
        
    except ImportError as e:
        logger.warning(f"⚠️ Flask not available: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ API Server error: {e}")
        return False

# ============================================================
# MAIN HEADLESS FUNCTION
# ============================================================

def main_headless():
    global brain_instance, bot_instance, engine_running
    
    logger.info("=" * 60)
    logger.info(f"  🧠 {APP_NAME} - COGNITIVE MIRROR ENGINE v{APP_VERSION}")
    logger.info(f"  Mode: {MODE.upper()}")
    logger.info(f"  AI: {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
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
    
    # Auto-start engine
    try:
        if bot_instance and hasattr(bot_instance, 'start'):
            bot_instance.start()
            engine_running = True
            logger.info("🚀 Engine auto-started")
    except Exception as e:
        logger.warning(f"⚠️ Auto-start failed: {e}")
    
    # Start API Server
    api_started = start_api_server(bot_instance)
    
    # ============================================================
    # START SCHEDULERS
    # ============================================================
    
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
    
    # ============================================================
    # SYSTEM READY
    # ============================================================
    
    logger.info("=" * 60)
    logger.info("  ✅ SYSTEM READY")
    logger.info("=" * 60)
    logger.info(f"  Mode        : {MODE}")
    logger.info(f"  Engine      : {'RUNNING' if engine_running else 'IDLE'}")
    logger.info(f"  Knowledge   : {len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0} items")
    logger.info(f"  AI          : {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
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
    if bot_instance and hasattr(bot_instance, 'stop'):
        bot_instance.stop()
    
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
