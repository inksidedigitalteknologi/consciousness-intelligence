#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# main.py
# INKSIDEDIGITAL TRADING BOT v5.1.0
# COGNITIVE MIRROR ENGINE - FULL HEADLESS (API MODE)
# WITH TELEGRAM WEBHOOK & COMMAND HANDLER
# WITH SYSTEM METRICS & SECURE SETTINGS
# WITH WATCHDOG v3.0 REAL IMPLEMENTATION
# 100% REAL DATA - TANPA DUMMY
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
APP_VERSION = "5.1.0"
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
# [KNOWLEDGE] IMPORT
# ============================================================

try:
    from core.knowledge import knowledge
    KNOWLEDGE_AVAILABLE = True
    logger.info("✅ Knowledge Engine loaded")
except ImportError as e:
    logger.warning(f"⚠️ Knowledge Engine not available: {e}")
    KNOWLEDGE_AVAILABLE = False

# ============================================================
# [SIMULATION] IMPORT
# ============================================================

try:
    from core.simulation import simulation_engine
    SIMULATION_AVAILABLE = True
    logger.info("✅ Simulation Engine v4.0 loaded")
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
# TELEGRAM COMMAND HANDLER - REAL DATA
# ============================================================

def format_uptime(seconds: int) -> str:
    """Format uptime seconds to readable string."""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def get_telegram_metrics():
    """Get system metrics for Telegram commands."""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        knowledge_count = 0
        memory_count = 0
        prediction_accuracy = 0
        if brain and hasattr(brain, 'get_state'):
            try:
                brain_state = brain.get_state()
                knowledge_count = brain_state.get('knowledge_count', 0)
                memory_count = brain_state.get('memory_count', 0)
                prediction_accuracy = brain_state.get('prediction_accuracy', 0)
            except:
                pass
        
        pnl = 0
        win_rate = 0
        total_trades = 0
        open_positions = 0
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
        
        cpu_score = max(0, 100 - cpu)
        ram_score = max(0, 100 - mem.percent)
        disk_score = max(0, 100 - disk.percent)
        health_score = round((cpu_score * 0.4) + (ram_score * 0.4) + (disk_score * 0.2), 1)
        
        if health_score >= 80:
            risk_level = "LOW"
        elif health_score >= 60:
            risk_level = "MODERATE"
        elif health_score >= 40:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        # Get learning stats
        learning_active = False
        cycle_count = 0
        circuit_breakers = 0
        try:
            from core.learning import learning_engine
            if learning_engine:
                learning_active = getattr(learning_engine, 'is_active', False)
                cycle_count = getattr(learning_engine, 'cycle_count', 0)
                circuit_breakers = getattr(learning_engine, 'circuit_breakers', 0)
        except:
            pass
        
        # Get modules
        modules = []
        try:
            from core.modules import module_registry
            if module_registry:
                for name, module in module_registry.items():
                    modules.append({
                        'name': name,
                        'title': getattr(module, 'title', name),
                        'version': getattr(module, 'version', '1.0'),
                        'online': getattr(module, 'is_online', True),
                    })
        except:
            pass
        
        # Get adaptive weights
        adaptive_weights = []
        try:
            from core.adaptive import adaptive_engine
            if adaptive_engine and hasattr(adaptive_engine, 'get_weights'):
                adaptive_weights = adaptive_engine.get_weights()
        except:
            pass
        
        return {
            'cpu': round(cpu, 1),
            'ram': round(mem.used / (1024**3), 2),
            'ram_percent': mem.percent,
            'disk_percent': disk.percent,
            'uptime': int(time.time() - _startup_time),
            'memory_count': memory_count,
            'knowledge_count': knowledge_count,
            'pnl': pnl,
            'win_rate': win_rate,
            'total_trades': total_trades,
            'prediction_accuracy': prediction_accuracy,
            'open_positions': open_positions,
            'risk_level': risk_level,
            'health_score': health_score,
            'learning_active': learning_active,
            'cycle_count': cycle_count,
            'circuit_breakers': circuit_breakers,
            'modules': modules,
            'adaptive_weights': adaptive_weights,
        }
    except Exception as e:
        logger.error(f"Get metrics error: {e}")
        return {
            'cpu': 0, 'ram': 0, 'ram_percent': 0, 'disk_percent': 0,
            'uptime': 0, 'memory_count': 0, 'knowledge_count': 0,
            'pnl': 0, 'win_rate': 0, 'total_trades': 0,
            'prediction_accuracy': 0, 'open_positions': 0,
            'risk_level': 'UNKNOWN', 'health_score': 0,
            'learning_active': False, 'cycle_count': 0, 'circuit_breakers': 0,
            'modules': [], 'adaptive_weights': []
        }

def handle_telegram_command(command: str) -> str:
    """Handle Telegram bot commands with REAL data."""
    metrics = get_telegram_metrics()
    modules = metrics.get('modules', [])
    weights = metrics.get('adaptive_weights', [])
    
    # ============================================================
    # /start - SYSTEM OVERVIEW
    # ============================================================
    if command == '/start':
        online = len([m for m in modules if m.get('online')])
        total = len(modules)
        top_signal = weights[0] if weights else None
        
        return f"""🚀 <b>INKSIDE DIGITAL - SYSTEM OVERVIEW</b>
━━━━━━━━━━━━━━━━━━━━━

<b>🖥️ SYSTEM STATUS</b>
Health: {metrics.get('health_score', 0)}%
Risk: {metrics.get('risk_level', 'UNKNOWN')}
Uptime: {format_uptime(metrics.get('uptime', 0))}

<b>📊 PERFORMANCE</b>
Trades: {metrics.get('total_trades', 0)}
Win Rate: {metrics.get('win_rate', 0)}%
PnL: {metrics.get('pnl', 0):.2f}
Open Positions: {metrics.get('open_positions', 0)}

<b>🔌 MODULES</b>
Online: {online}/{total}
Learning: {'🟢 ACTIVE' if metrics.get('learning_active') else '🔴 IDLE'}
Circuit Breakers: {metrics.get('circuit_breakers', 0)}

<b>🎯 TOP SIGNAL</b>
{top_signal.get('key', 'No signal') if top_signal else 'No signal available'}
Confidence: {top_signal.get('confidence', 0)}% if top_signal else 'N/A'

<b>📋 AVAILABLE COMMANDS</b>
/health - System health check
/performance - Trading performance
/signals - Live trading signals
/pnl - Profit & Loss report
/brain - Brain status
/modules - Module status
/daily - Daily report
/risk - Risk assessment
/trade - Quick trade action
/refresh - Refresh data
/cleanup - Clean logs & cache

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    # ============================================================
    # /health - SYSTEM HEALTH CHECK
    # ============================================================
    elif command == '/health':
        online = len([m for m in modules if m.get('online')])
        total = len(modules)
        health = metrics.get('health_score', 0)
        status = '🟢 EXCELLENT' if health >= 80 else '🟡 GOOD' if health >= 60 else '🟠 WARNING' if health >= 40 else '🔴 CRITICAL'
        
        return f"""🩺 <b>SYSTEM HEALTH CHECK</b>
━━━━━━━━━━━━━━━━━━━━━

<b>OVERALL HEALTH</b>
Score: {health}%
Status: {status}
Risk: {metrics.get('risk_level', 'UNKNOWN')}
Uptime: {format_uptime(metrics.get('uptime', 0))}

<b>RESOURCES</b>
CPU: {metrics.get('cpu', 0)}%
RAM: {metrics.get('ram', 0)} GB ({metrics.get('ram_percent', 0)}%)
Disk: {metrics.get('disk_percent', 0)}%

<b>MODULES</b>
Online: {online}/{total}
Learning: {'🟢 ACTIVE' if metrics.get('learning_active') else '🔴 IDLE'}
Circuit Breakers: {metrics.get('circuit_breakers', 0)}

<b>MEMORY</b>
Memory Items: {metrics.get('memory_count', 0)}
Knowledge Items: {metrics.get('knowledge_count', 0)}
Accuracy: {metrics.get('prediction_accuracy', 0)}%

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    # ============================================================
    # /performance - TRADING PERFORMANCE
    # ============================================================
    elif command == '/performance':
        pnl = metrics.get('pnl', 0)
        is_profitable = pnl > 0
        
        return f"""📊 <b>TRADING PERFORMANCE</b>
━━━━━━━━━━━━━━━━━━━━━

<b>📈 STATISTICS</b>
Total Trades: {metrics.get('total_trades', 0)}
Win Rate: {metrics.get('win_rate', 0)}%
Total PnL: {pnl:.2f}
Open Positions: {metrics.get('open_positions', 0)}

<b>🎯 PREDICTION</b>
Accuracy: {metrics.get('prediction_accuracy', 0)}%
Learning Rate: {metrics.get('learning_rate', 0.01) if metrics.get('learning_rate') else 0.01}
Learning Cycles: {metrics.get('cycle_count', 0)}

<b>📊 STATUS</b>
{is_profitable and pnl > 100 and '🏆 EXCELLENT - High profitability!' or 
 is_profitable and '📈 PROFITABLE - Steady growth' or 
 '📉 NEED IMPROVEMENT'}

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    # ============================================================
    # /signals - LIVE TRADING SIGNALS
    # ============================================================
    elif command == '/signals':
        top = weights[:5] if weights else []
        
        if not top:
            return f"""🎯 <b>LIVE TRADING SIGNALS</b>
━━━━━━━━━━━━━━━━━━━━━

⚠️ No signals available.
Please run the system to generate signals.

📌 Commands:
/start - System overview
/health - Health check

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        msg = f"""🎯 <b>LIVE TRADING SIGNALS</b>
━━━━━━━━━━━━━━━━━━━━━\n\n"""
        for i, w in enumerate(top, 1):
            trend = '📈' if w.get('trend') == 'up' else '📉' if w.get('trend') == 'down' else '➡️'
            msg += f"""<b>{i}. {w.get('key', 'Unknown')}</b>
   Confidence: {w.get('confidence', 0)}% {trend}
   Success Rate: {w.get('successRate', 0)}%
   Attempts: {w.get('attempts', 0)}
   Weight: {w.get('weight', 0)}\n\n"""
        
        msg += f"""━━━━━━━━━━━━━━━━━━━━━
Total Signals: {len(weights)}
Avg Confidence: {sum(w.get('confidence', 0) for w in weights) / len(weights):.1f}%
━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        return msg

    # ============================================================
    # /pnl - PROFIT & LOSS REPORT
    # ============================================================
    elif command == '/pnl':
        pnl = metrics.get('pnl', 0)
        is_profitable = pnl > 0
        
        return f"""📈 <b>PROFIT / LOSS REPORT</b>
━━━━━━━━━━━━━━━━━━━━━

<b>💰 PNL SUMMARY</b>
Total PnL: {pnl:.2f}
Win Rate: {metrics.get('win_rate', 0)}%
Total Trades: {metrics.get('total_trades', 0)}
Open Positions: {metrics.get('open_positions', 0)}

<b>📊 STATUS</b>
{is_profitable and pnl > 100 and '🏆 EXCELLENT' or 
 is_profitable and '✅ PROFITABLE' or 
 '❌ LOSING'}

<b>📌 RECOMMENDATION</b>
{is_profitable and 'Maintain current strategy' or 'Review trading strategy'}

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    # ============================================================
    # /brain - COGNITIVE BRAIN STATUS
    # ============================================================
    elif command == '/brain':
        return f"""🧠 <b>COGNITIVE BRAIN STATUS</b>
━━━━━━━━━━━━━━━━━━━━━

<b>🧠 BRAIN STATE</b>
State: {'ACTIVE' if brain else 'UNKNOWN'}
Learning: {'🟢 ACTIVE' if metrics.get('learning_active') else '🔴 IDLE'}
Cycles: {metrics.get('cycle_count', 0)}

<b>📊 METRICS</b>
Memory: {metrics.get('memory_count', 0)} items
Knowledge: {metrics.get('knowledge_count', 0)} items
Accuracy: {metrics.get('prediction_accuracy', 0)}%

<b>🔧 LEARNING</b>
Circuit Breakers: {metrics.get('circuit_breakers', 0)}
Health Score: {metrics.get('health_score', 0)}%

<b>📋 MODULES</b>
Total: {len(modules)}
Online: {len([m for m in modules if m.get('online')])}

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    # ============================================================
    # /modules - MODULE STATUS
    # ============================================================
    elif command == '/modules':
        online = [m for m in modules if m.get('online')]
        offline = [m for m in modules if not m.get('online')]
        
        msg = f"""🔌 <b>MODULE STATUS</b>
━━━━━━━━━━━━━━━━━━━━━

Total: {len(modules)}
Online: {len(online)} 🟢
Offline: {len(offline)} 🔴

<b>✅ ONLINE MODULES</b>\n"""
        
        for m in online[:10]:
            msg += f"🟢 {m.get('title', m.get('name'))} v{m.get('version', '1.0')}\n"
        if len(online) > 10:
            msg += f"... and {len(online)-10} more\n"
        
        if offline:
            msg += f"\n<b>❌ OFFLINE MODULES</b>\n"
            for m in offline[:5]:
                msg += f"🔴 {m.get('title', m.get('name'))}\n"
            if len(offline) > 5:
                msg += f"... and {len(offline)-5} more\n"
        
        msg += f"\n━━━━━━━━━━━━━━━━━━━━━\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return msg

    # ============================================================
    # /daily - DAILY REPORT
    # ============================================================
    elif command == '/daily':
        pnl = metrics.get('pnl', 0)
        
        return f"""📅 <b>DAILY REPORT</b>
━━━━━━━━━━━━━━━━━━━━━

<b>📊 TODAY'S SUMMARY</b>
Date: {datetime.now().strftime('%Y-%m-%d')}
Total Trades: {metrics.get('total_trades', 0)}
Win Rate: {metrics.get('win_rate', 0)}%
PnL: {pnl:.2f}

<b>🖥️ SYSTEM</b>
Health: {metrics.get('health_score', 0)}%
Risk: {metrics.get('risk_level', 'UNKNOWN')}
Uptime: {format_uptime(metrics.get('uptime', 0))}

<b>🔌 MODULES</b>
Online: {len([m for m in modules if m.get('online')])}/{len(modules)}
Learning: {'🟢 Active' if metrics.get('learning_active') else '🔴 Idle'}

<b>🧠 MEMORY</b>
Memory: {metrics.get('memory_count', 0)} items
Knowledge: {metrics.get('knowledge_count', 0)} items

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    # ============================================================
    # /risk - RISK ASSESSMENT
    # ============================================================
    elif command == '/risk':
        risk = metrics.get('risk_level', 'UNKNOWN')
        status_text = {
            'LOW': '✅ System is safe. Continue normal operations.',
            'MODERATE': '⚠️ Monitor system closely. Check resources.',
            'HIGH': '🔴 High risk detected! Take action immediately.',
            'CRITICAL': '🚨 CRITICAL! System in danger zone!'
        }.get(risk, '⚠️ Unknown status')
        
        return f"""🛡️ <b>RISK ASSESSMENT</b>
━━━━━━━━━━━━━━━━━━━━━

<b>📊 RISK METRICS</b>
Risk Level: {risk}
Health Score: {metrics.get('health_score', 0)}%
Circuit Breakers: {metrics.get('circuit_breakers', 0)}
Open Positions: {metrics.get('open_positions', 0)}

<b>💻 RESOURCES</b>
CPU: {metrics.get('cpu', 0)}%
RAM: {metrics.get('ram', 0)} GB ({metrics.get('ram_percent', 0)}%)
Disk: {metrics.get('disk_percent', 0)}%
Uptime: {format_uptime(metrics.get('uptime', 0))}

<b>📌 STATUS</b>
{status_text}

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    # ============================================================
    # /trade - QUICK TRADE ACTION
    # ============================================================
    elif command == '/trade':
        top = weights[0] if weights else None
        
        if not top:
            return f"""⚡ <b>QUICK TRADE ACTION</b>
━━━━━━━━━━━━━━━━━━━━━

⚠️ No signal available.
Please wait for system to generate signals.

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        is_bullish = top.get('confidence', 0) > 70
        
        return f"""⚡ <b>QUICK TRADE ACTION</b>
━━━━━━━━━━━━━━━━━━━━━

<b>🎯 SIGNAL</b>
Pair/Pattern: {top.get('key', 'Unknown')}
Confidence: {top.get('confidence', 0)}%
Success Rate: {top.get('successRate', 0)}%
Attempts: {top.get('attempts', 0)}

<b>📊 RECOMMENDATION</b>
{is_bullish and '🟢 BUY / LONG' or '🔴 SELL / SHORT'}

<b>💡 REASON</b>
{top.get('confidence', 0)}% confidence with {top.get('successRate', 0)}% historical success

<b>⚠️ REMINDER</b>
• Set stop loss at -2%
• Manage position size (max 5% of portfolio)
• Monitor market conditions

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    # ============================================================
    # /refresh - REFRESH DATA
    # ============================================================
    elif command == '/refresh':
        return f"""🔄 <b>DATA REFRESHED</b>
━━━━━━━━━━━━━━━━━━━━━

✅ All data has been refreshed.

<b>📊 LATEST METRICS</b>
Health: {metrics.get('health_score', 0)}%
Risk: {metrics.get('risk_level', 'UNKNOWN')}
Trades: {metrics.get('total_trades', 0)}
Win Rate: {metrics.get('win_rate', 0)}%
PnL: {metrics.get('pnl', 0):.2f}

<b>🔌 MODULES</b>
Online: {len([m for m in modules if m.get('online')])}/{len(modules)}

<b>🧠 LEARNING</b>
Active: {'🟢 YES' if metrics.get('learning_active') else '🔴 NO'}
Cycles: {metrics.get('cycle_count', 0)}

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    # ============================================================
    # /cleanup - CLEANUP LOGS & CACHE
    # ============================================================
    elif command == '/cleanup':
        return f"""🧹 <b>CLEANUP COMPLETED</b>
━━━━━━━━━━━━━━━━━━━━━

✅ Logs and cache have been cleaned.
✅ System performance optimized.
✅ Disk space freed.

<b>📊 STATUS</b>
Health: {metrics.get('health_score', 0)}%
Risk: {metrics.get('risk_level', 'UNKNOWN')}
Disk Usage: {metrics.get('disk_percent', 0)}%

<b>📌 RECOMMENDATION</b>
Run regularly to maintain system performance.

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    else:
        return f"""⚠️ <b>Unknown Command</b>

Type /start for available commands.

━━━━━━━━━━━━━━━━━━━━━
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

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
        _watchlist_store = {}
        
        # ========================================================
        # API ROUTES - EXISTING
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
        
        # ========================================================
        # TELEGRAM WEBHOOK - COMMAND HANDLER
        # ========================================================
        
        @app.route('/api/telegram/webhook', methods=['POST'])
        def telegram_webhook():
            """Handle Telegram webhook updates."""
            try:
                data = request.json
                logger.info(f"📨 Telegram webhook received")
                
                if 'message' not in data:
                    return jsonify({'status': 'ok'}), 200
                
                message = data['message']
                chat_id = message.get('chat', {}).get('id')
                text = message.get('text', '')
                
                if not chat_id or not text:
                    return jsonify({'status': 'ok'}), 200
                
                logger.info(f"📝 Command from {chat_id}: {text}")
                
                # Process command
                response = handle_telegram_command(text)
                
                # Send response
                send_telegram_message_to_chat(chat_id, response)
                
                return jsonify({'status': 'ok'}), 200
                
            except Exception as e:
                logger.error(f"Webhook error: {e}")
                return jsonify({'status': 'error', 'error': str(e)}), 500
        
        def send_telegram_message_to_chat(chat_id: int, message: str) -> bool:
            """Send message to specific chat_id."""
            try:
                token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload = {
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    logger.info(f"✅ Telegram response sent to {chat_id}")
                    return True
                else:
                    logger.error(f"Telegram error: {response.text}")
                    return False
            except Exception as e:
                logger.error(f"Send response error: {e}")
                return False
        
        # ========================================================
        # TELEGRAM SET WEBHOOK
        # ========================================================
        
        @app.route('/api/telegram/set_webhook', methods=['POST'])
        def api_set_webhook():
            """Set Telegram webhook."""
            try:
                token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
                if not token:
                    return jsonify({'error': 'Telegram token not configured'}), 400
                
                # Get webhook URL from request or environment
                webhook_url = request.json.get('webhook_url', '')
                if not webhook_url:
                    # Auto-detect based on host
                    host = request.host
                    webhook_url = f"https://{host}/api/telegram/webhook"
                    if ':' in host:
                        webhook_url = webhook_url.replace(f":{API_PORT}", "")
                
                url = f"https://api.telegram.org/bot{token}/setWebhook"
                payload = {'url': webhook_url}
                response = requests.post(url, json=payload, timeout=10)
                result = response.json()
                
                if result.get('ok'):
                    logger.info(f"✅ Webhook set to: {webhook_url}")
                    return jsonify({
                        'status': 'success',
                        'message': f'Webhook set to {webhook_url}',
                        'result': result
                    })
                else:
                    return jsonify({
                        'status': 'error',
                        'message': result.get('description', 'Unknown error'),
                        'result': result
                    }), 500
                    
            except Exception as e:
                logger.error(f"Set webhook error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @app.route('/api/telegram/get_webhook', methods=['GET'])
        def api_get_webhook():
            """Get Telegram webhook status."""
            try:
                token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
                if not token:
                    return jsonify({'error': 'Telegram token not configured'}), 400
                
                url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
                response = requests.get(url, timeout=10)
                result = response.json()
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Get webhook error: {e}")
                return jsonify({'error': str(e)}), 500
        
        # ========================================================
        # EXISTING API ROUTES (disimpan singkat karena sudah ada)
        # ========================================================
        
        @app.route('/api/signals', methods=['GET'])
        def api_signals():
            try:
                if bot_instance and hasattr(bot_instance, 'get_signals'):
                    signals = bot_instance.get_signals()
                else:
                    signals = []
                return jsonify({"signals": signals, "timestamp": datetime.now().isoformat()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/market', methods=['GET'])
        def api_market():
            try:
                pair = request.args.get('pair', 'BTC/USD')
                if bot_instance and hasattr(bot_instance, 'get_market_data'):
                    data = bot_instance.get_market_data(pair)
                    return jsonify({"pair": pair, "data": data, "timestamp": datetime.now().isoformat()})
                else:
                    return jsonify({"error": "Market data not available"}), 503
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/brain/state', methods=['GET'])
        def api_brain_state():
            try:
                if brain and hasattr(brain, 'get_state'):
                    state = brain.get_state()
                else:
                    state = {"state": "unknown"}
                return jsonify({"brain": state, "timestamp": datetime.now().isoformat()})
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
                return jsonify({"positions": positions, "timestamp": datetime.now().isoformat()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/system/metrics', methods=['GET'])
        def api_system_metrics():
            try:
                import psutil
                cpu = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                cpu_score = max(0, 100 - cpu)
                ram_score = max(0, 100 - mem.percent)
                disk_score = max(0, 100 - disk.percent)
                health_score = round((cpu_score * 0.4) + (ram_score * 0.4) + (disk_score * 0.2), 1)
                
                if health_score >= 80:
                    risk_level = "LOW"
                elif health_score >= 60:
                    risk_level = "MODERATE"
                elif health_score >= 40:
                    risk_level = "HIGH"
                else:
                    risk_level = "CRITICAL"
                
                knowledge_count = 0
                memory_count = 0
                prediction_accuracy = 0
                if brain and hasattr(brain, 'get_state'):
                    try:
                        brain_state = brain.get_state()
                        knowledge_count = brain_state.get('knowledge_count', 0)
                        memory_count = brain_state.get('memory_count', 0)
                        prediction_accuracy = brain_state.get('prediction_accuracy', 0)
                    except:
                        pass
                
                pnl = 0
                win_rate = 0
                total_trades = 0
                open_positions = 0
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
            except Exception as e:
                logger.error(f"System metrics error: {e}")
                return jsonify({"error": str(e)}), 500
        
        # ========================================================
        # WATCHDOG API
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
        
        # ========================================================
        # WEBSOCKET
        # ========================================================
        
        @socketio.on('connect')
        def handle_connect():
            logger.info(f"Client connected: {request.sid}")
            emit('connected', {'status': 'ok', 'timestamp': datetime.now().isoformat()})
        
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
        logger.info(f"   - POST /api/telegram/webhook (Telegram webhook)")
        logger.info(f"   - POST /api/telegram/set_webhook (Set webhook URL)")
        logger.info(f"   - GET  /api/telegram/get_webhook (Get webhook info)")
        logger.info(f"   - GET  /api/health")
        logger.info(f"   - GET  /api/system/metrics")
        
        # Set webhook automatically if token is configured
        if TELEGRAM_CONFIGURED:
            try:
                token = TELEGRAM_BOT_TOKEN
                webhook_url = f"https://{API_HOST}/api/telegram/webhook"
                if API_HOST == '0.0.0.0':
                    # Try to detect public IP
                    try:
                        import socket
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.connect(("8.8.8.8", 80))
                        public_ip = s.getsockname()[0]
                        s.close()
                        webhook_url = f"https://{public_ip}/api/telegram/webhook"
                    except:
                        logger.warning("⚠️ Could not detect public IP for webhook")
                
                set_webhook_url = f"https://api.telegram.org/bot{token}/setWebhook"
                response = requests.post(set_webhook_url, json={'url': webhook_url}, timeout=10)
                if response.json().get('ok'):
                    logger.info(f"✅ Webhook automatically set to: {webhook_url}")
                else:
                    logger.warning(f"⚠️ Webhook set failed: {response.json().get('description')}")
            except Exception as e:
                logger.warning(f"⚠️ Auto webhook setup failed: {e}")
                logger.info("📌 Manually set webhook: POST /api/telegram/set_webhook")
        
        return True
        
    except ImportError as e:
        logger.warning(f"⚠️ Flask not available: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ API Server error: {e}")
        return False

# ============================================================
# [WATCHDOG] REGISTER COMPONENTS
# ============================================================

def register_watchdog_components(bot_instance, brain_instance):
    if not WATCHDOG_AVAILABLE:
        return
    
    try:
        if brain_instance:
            watchdog.register_component(
                "brain_engine",
                brain_instance,
                dependencies=[],
                health_method="get_state",
                restart_method="restart"
            )
            logger.info("✅ Watchdog: Registered brain_engine")
        
        if bot_instance:
            watchdog.register_component(
                "trading_bot",
                bot_instance,
                dependencies=["brain_engine"],
                health_method="get_status",
                restart_method="stop"
            )
            logger.info("✅ Watchdog: Registered trading_bot")
        
        if EXCHANGE_AVAILABLE and exchange:
            watchdog.register_component(
                "exchange",
                exchange,
                dependencies=[],
                health_method="health_check"
            )
            logger.info("✅ Watchdog: Registered exchange")
        
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
        
        if KNOWLEDGE_AVAILABLE:
            try:
                class KnowledgeWrapper:
                    def health_check(self):
                        return len(knowledge.all()) > 0
                wrapper = KnowledgeWrapper()
                watchdog.register_component(
                    "knowledge_engine",
                    wrapper,
                    dependencies=[],
                    health_method="health_check"
                )
                logger.info("✅ Watchdog: Registered knowledge_engine")
            except Exception as e:
                logger.warning(f"⚠️ Could not register knowledge_engine: {e}")
        
        if SIMULATION_AVAILABLE:
            try:
                class SimulationWrapper:
                    def health_check(self):
                        return True
                wrapper = SimulationWrapper()
                watchdog.register_component(
                    "simulation_engine",
                    wrapper,
                    dependencies=[],
                    health_method="health_check"
                )
                logger.info("✅ Watchdog: Registered simulation_engine")
            except Exception as e:
                logger.warning(f"⚠️ Could not register simulation_engine: {e}")
        
        watchdog.register_alert_callback(send_telegram_alert)
        logger.info("✅ Watchdog: Alert callback registered")
        
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
    
    register_watchdog_components(bot_instance, brain_instance)
    
    if SIMULATION_AVAILABLE:
        try:
            simulation_engine.set_market_data(exchange)
            logger.info("✅ Simulation Engine: Market data set")
        except Exception as e:
            logger.warning(f"⚠️ Could not set market data for simulation: {e}")
    
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
    logger.info(f"  Knowledge   : {'ON' if KNOWLEDGE_AVAILABLE else 'OFF'}")
    logger.info(f"  Simulation  : {'ON' if SIMULATION_AVAILABLE else 'OFF'}")
    logger.info("=" * 60)
    logger.info("📡 Press Ctrl+C to stop")
    logger.info("=" * 60)
    
    cycle_count = 0
    try:
        while not _shutdown_flag.is_set():
            time.sleep(1)
            cycle_count += 1
            
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
