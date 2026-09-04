# core/logger.py
# INKSIDE DIGITAL - CUSTOM LOGGER WITH COLORS & EMOJIS

import logging
import sys
from datetime import datetime

# ============================================================
# ANSI COLOR CODES
# ============================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ORANGE = '\033[91m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    # Background
    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_PURPLE = '\033[45m'
    BG_CYAN = '\033[46m'

# ============================================================
# EMOJI MAP
# ============================================================

EMOJIS = {
    'INFO': '📘',
    'WARNING': '⚠️',
    'ERROR': '❌',
    'CRITICAL': '🚨',
    'DEBUG': '🐛',
    'SUCCESS': '✅',
    'START': '🚀',
    'STOP': '🛑',
    'LOADING': '⏳',
    'DONE': '🎯',
    'BRAIN': '🧠',
    'KNOWLEDGE': '📚',
    'WATCHDOG': '🛡️',
    'API': '🌐',
    'WEBSOCKET': '🔌',
    'DATABASE': '🗄️',
    'CACHE': '💾',
    'NETWORK': '📡',
    'TRADING': '📊',
    'SIGNAL': '📈',
    'MARKET': '🏦',
    'TELEGRAM': '✈️',
    'EXCHANGE': '🔄',
    'MEMORY': '🧩',
    'PATTERN': '🔍',
    'PREDICTION': '🔮',
    'DECISION': '⚖️',
    'REFLECTION': '🪞',
}

# ============================================================
# CUSTOM LOGGER CLASS
# ============================================================

class CustomLogger:
    def __init__(self, name='Inkside'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.CustomFormatter())
        self.logger.addHandler(console_handler)
        
        # File handler (no colors)
        file_handler = logging.FileHandler('logs/system.log', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(file_handler)
    
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            level = record.levelname
            emoji = EMOJIS.get(level, '📌')
            color = Colors.WHITE
            
            if level == 'INFO':
                color = Colors.CYAN
                emoji = '📘'
            elif level == 'WARNING':
                color = Colors.YELLOW
                emoji = '⚠️'
            elif level == 'ERROR':
                color = Colors.RED
                emoji = '❌'
            elif level == 'CRITICAL':
                color = Colors.RED + Colors.BOLD
                emoji = '🚨'
            elif level == 'DEBUG':
                color = Colors.DIM
                emoji = '🐛'
            
            # Ambil custom emoji dari pesan jika ada
            msg = record.msg
            for key, emoji_char in EMOJIS.items():
                if f'[{key}]' in msg:
                    emoji = emoji_char
                    break
            
            # Format waktu
            time_str = datetime.now().strftime('%H:%M:%S')
            
            # Format pesan dengan warna
            formatted = (
                f"{Colors.DIM}{time_str}{Colors.RESET} "
                f"{color}{emoji} {record.getMessage()}{Colors.RESET}"
            )
            
            return formatted

# ============================================================
# SIMPLE FUNCTIONS
# ============================================================

def get_logger(name='Inkside'):
    return CustomLogger().logger

# ============================================================
# BEAUTIFUL STARTUP LOG
# ============================================================

def print_banner():
    """Print beautiful startup banner"""
    banner = f"""
{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                                  ║
║   {Colors.GREEN}🧠 INKSIDE DIGITAL{Colors.CYAN} - COGNITIVE MIRROR ENGINE          ║
║   {Colors.WHITE}🚀 Autonomous Intelligence Trading System{Colors.CYAN}              ║
║                                                                  ║
║   {Colors.DIM}⚡ Version: {Colors.WHITE}2.0.0{Colors.DIM}          {Colors.DIM}🔧 Mode: {Colors.WHITE}PAPER{Colors.DIM}          {Colors.DIM}📡 API: {Colors.WHITE}PORT 5000{Colors.DIM}    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def print_status(status, message):
    """Print status with beautiful format"""
    icon = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': '📘',
        'loading': '⏳',
        'done': '🎯',
    }.get(status, '📌')
    
    color = {
        'success': Colors.GREEN,
        'error': Colors.RED,
        'warning': Colors.YELLOW,
        'info': Colors.CYAN,
        'loading': Colors.YELLOW,
        'done': Colors.GREEN,
    }.get(status, Colors.WHITE)
    
    print(f"{Colors.DIM}{datetime.now().strftime('%H:%M:%S')}{Colors.RESET} {color}{icon} {message}{Colors.RESET}")

def print_section(title):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}═══ {title} ═══{Colors.RESET}\n")
