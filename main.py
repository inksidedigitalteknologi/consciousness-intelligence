#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# main.py
# INKSIDEDIGITAL - COGNITIVE MIRROR ENGINE v2.0.0
# FOCUS: DIVIDEND HUNTER + AI INTELLIGENCE
# NO EXCHANGE (CoinGecko, Kraken, NonKYC removed)
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

for folder in ['logs', 'database', 'database/backup', 'cache', 'database/shards', 'data/dividends']:
    (CURRENT_DIR / folder).mkdir(exist_ok=True, parents=True)

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
API_PORT = int(os.environ.get('API_PORT', 5000))
API_HOST = os.environ.get('API_HOST', '0.0.0.0')

engine_running = False

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
# DIVIDEND IMPORT
# ============================================================

try:
    from core.dividend import dividend, fetch_dividends, screen_dividends, check_dividend_alerts
    DIVIDEND_AVAILABLE = True
    logger.info("✅ Dividend Hunter Module loaded")
except ImportError as e:
    logger.warning(f"⚠️ Dividend Hunter not available: {e}")
    DIVIDEND_AVAILABLE = False

# ============================================================
# BRAIN IMPORT (Optional - untuk AI)
# ============================================================

try:
    from core.brain import Brain, brain
    BRAIN_AVAILABLE = True
    logger.info("✅ Brain module loaded")
except ImportError as e:
    logger.warning(f"⚠️ Brain module not available: {e}")
    BRAIN_AVAILABLE = False
    Brain = None
    brain = None

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

# Optional modules (tidak wajib)
Analyzer = safe_import('core.analyzer', 'Analyzer')
Scanner = safe_import('core.scanner', 'CognitiveMarketScanner')
SignalEngine = safe_import('core.signal_engine', 'SignalEngine')

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
# AUTO-CRAWL SCHEDULER (Untuk Knowledge)
# ============================================================

AUTO_CRAWL_SOURCES = []  # Kosongkan, fokus ke dividen

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

def start_api_server():
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
        # DIVIDEND ENDPOINTS - FOKUS UTAMA
        # ============================================================

        @app.route('/api/dividend/fetch', methods=['POST'])
        @require_api_key
        def dividend_fetch():
            """Fetch dividend data for a date."""
            try:
                data = request.json or {}
                date = data.get('date')  # Optional: YYYY-MM-DD
                
                if not DIVIDEND_AVAILABLE:
                    return jsonify({'error': 'Dividend module not available'}), 503
                
                df = dividend.fetch(date)
                
                if df.empty:
                    return jsonify({
                        'status': 'error',
                        'message': 'No dividend data found',
                        'count': 0,
                        'data': []
                    }), 404
                
                return jsonify({
                    'status': 'success',
                    'count': len(df),
                    'data': df.to_dict('records'),
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Dividend fetch error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/dividend/top', methods=['GET'])
        @require_api_key
        def dividend_top():
            """Get top N dividends."""
            try:
                n = int(request.args.get('n', 10))
                
                if not DIVIDEND_AVAILABLE:
                    return jsonify({'error': 'Dividend module not available'}), 503
                
                if dividend.df.empty:
                    dividend.fetch()
                
                top = dividend.get_top(n)
                
                return jsonify({
                    'status': 'success',
                    'count': len(top),
                    'data': top.to_dict('records') if not top.empty else [],
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Dividend top error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/dividend/upcoming', methods=['GET'])
        @require_api_key
        def dividend_upcoming():
            """Get upcoming dividends."""
            try:
                days = int(request.args.get('days', 7))
                
                if not DIVIDEND_AVAILABLE:
                    return jsonify({'error': 'Dividend module not available'}), 503
                
                if dividend.df.empty:
                    dividend.fetch()
                
                upcoming = dividend.get_upcoming(days)
                
                return jsonify({
                    'status': 'success',
                    'count': len(upcoming),
                    'data': upcoming.to_dict('records') if not upcoming.empty else [],
                    'days': days,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Dividend upcoming error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/dividend/screen', methods=['POST'])
        @require_api_key
        def dividend_screen():
            """Screen dividends by criteria."""
            try:
                data = request.json or {}
                min_dividend = data.get('min_dividend')
                sectors = data.get('sectors')
                exclude_etf = data.get('exclude_etf', True)
                
                if not DIVIDEND_AVAILABLE:
                    return jsonify({'error': 'Dividend module not available'}), 503
                
                if dividend.df.empty:
                    dividend.fetch()
                
                screened = dividend.screen(
                    min_dividend=min_dividend,
                    sectors=sectors,
                    exclude_etf=exclude_etf
                )
                
                return jsonify({
                    'status': 'success',
                    'count': len(screened),
                    'data': screened.to_dict('records') if not screened.empty else [],
                    'filters': {
                        'min_dividend': min_dividend,
                        'sectors': sectors,
                        'exclude_etf': exclude_etf,
                    },
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Dividend screen error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/dividend/alerts', methods=['GET'])
        @require_api_key
        def dividend_alerts():
            """Get dividend alerts."""
            try:
                days_before = int(request.args.get('days_before', 3))
                
                if not DIVIDEND_AVAILABLE:
                    return jsonify({'error': 'Dividend module not available'}), 503
                
                if dividend.df.empty:
                    dividend.fetch()
                
                alerts = dividend.check_alerts(days_before)
                
                return jsonify({
                    'status': 'success',
                    'count': len(alerts),
                    'data': alerts,
                    'days_before': days_before,
                    'summary': dividend.get_alert_summary(),
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Dividend alerts error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/dividend/stats', methods=['GET'])
        @require_api_key
        def dividend_stats():
            """Get dividend statistics."""
            try:
                if not DIVIDEND_AVAILABLE:
                    return jsonify({'error': 'Dividend module not available'}), 503
                
                if dividend.df.empty:
                    dividend.fetch()
                
                stats = dividend.get_statistics()
                
                return jsonify({
                    'status': 'success',
                    'statistics': stats,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Dividend stats error: {e}")
                return jsonify({'error': str(e)}), 500

        @app.route('/api/dividend/sectors', methods=['GET'])
        @require_api_key
        def dividend_sectors():
            """Get dividend summary by sector."""
            try:
                if not DIVIDEND_AVAILABLE:
                    return jsonify({'error': 'Dividend module not available'}), 503
                
                if dividend.df.empty:
                    dividend.fetch()
                
                summary = dividend.get_sector_summary()
                
                return jsonify({
                    'status': 'success',
                    'data': summary.to_dict('records') if not summary.empty else [],
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Dividend sectors error: {e}")
                return jsonify({'error': str(e)}), 500

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
                
                context = None
                if KNOWLEDGE_AVAILABLE:
                    relevant = knowledge.search(question, max_results=5)
                    if relevant:
                        context = "\n\n".join([
                            f"[{item.category}] {item.content}"
                            for item in relevant
                        ])
                
                if not DEEPSEEK_ENABLED:
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
                if not BRAIN_AVAILABLE:
                    return jsonify({'error': 'Brain module not available'}), 503
                
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
                if not BRAIN_AVAILABLE:
                    return jsonify({'error': 'Brain module not available'}), 503
                
                from core.brain import brain
                return jsonify(brain.get_ai_status())
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
                return jsonify({
                    "status": "healthy",
                    "uptime": int(time.time() - _startup_time),
                    "version": APP_VERSION,
                    "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                    "dividend_available": DIVIDEND_AVAILABLE,
                    "ai_enabled": DEEPSEEK_ENABLED,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500

        @app.route('/api/status', methods=['GET'])
        @require_api_key
        def api_status():
            try:
                dividend_stats = {}
                if DIVIDEND_AVAILABLE and not dividend.df.empty:
                    dividend_stats = dividend.get_statistics()
                
                return jsonify({
                    "status": "online",
                    "version": APP_VERSION,
                    "mode": MODE,
                    "knowledge_items": len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0,
                    "dividend": {
                        "available": DIVIDEND_AVAILABLE,
                        "items": len(dividend.df) if DIVIDEND_AVAILABLE else 0,
                        "last_update": dividend.last_update.isoformat() if DIVIDEND_AVAILABLE and dividend.last_update else None,
                    },
                    "ai_enabled": DEEPSEEK_ENABLED,
                    "telegram": TELEGRAM_CONFIGURED,
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
                    "dividend_items": len(dividend.df) if DIVIDEND_AVAILABLE else 0,
                    "ai_enabled": DEEPSEEK_ENABLED,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500

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
                        'dividend_items': len(dividend.df) if DIVIDEND_AVAILABLE else 0,
                        'cpu': cpu,
                        'ram': round(mem.used / (1024**3), 2),
                        'ram_percent': mem.percent,
                        'disk_percent': disk.percent,
                        'health_score': health_score
                    },
                    'components': {
                        'backend': {'status': 'online', 'version': APP_VERSION},
                        'knowledge': {'status': 'online' if KNOWLEDGE_AVAILABLE else 'offline'},
                        'dividend': {'status': 'online' if DIVIDEND_AVAILABLE else 'offline'},
                        'watchdog': {'status': 'online' if WATCHDOG_AVAILABLE else 'offline'},
                        'websocket': {'status': 'online'},
                        'ai': {'status': 'online' if DEEPSEEK_ENABLED else 'offline'},
                        'telegram': {'status': 'online' if TELEGRAM_CONFIGURED else 'offline'}
                    },
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Diagnostics error: {e}")
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
        logger.info(f"   💰 Dividend Hunter: {'ONLINE' if DIVIDEND_AVAILABLE else 'OFFLINE'}")
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
    global engine_running
    
    logger.info("=" * 60)
    logger.info(f"  🧠 {APP_NAME} - COGNITIVE MIRROR ENGINE v{APP_VERSION}")
    logger.info(f"  Mode: {MODE.upper()}")
    logger.info(f"  AI: {'ENABLED' if DEEPSEEK_ENABLED else 'DISABLED'}")
    logger.info("=" * 60)
    
    # Start API Server
    api_started = start_api_server()
    
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
    logger.info(f"  Knowledge   : {len(knowledge.all()) if KNOWLEDGE_AVAILABLE else 0} items")
    logger.info(f"  Dividend    : {'ONLINE' if DIVIDEND_AVAILABLE else 'OFFLINE'}")
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
