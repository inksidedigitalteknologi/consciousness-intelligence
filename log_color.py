#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inkside Digital - Log Colorizer
Menampilkan log dengan warna yang jelas
"""

import sys
import re
import time
import os
from datetime import datetime

# ============================================================
# ANSI COLOR CODES
# ============================================================

class Colors:
    """ANSI color codes untuk terminal."""
    # Style
    BOLD = '\033[1m'
    DIM = '\033[2m'
    NORMAL = '\033[22m'
    RESET = '\033[0m'
    
    # Foreground
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright Foreground
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

# ============================================================
# LOG COLORIZER
# ============================================================

class LogColorizer:
    """Colorize log output."""
    
    # Pola untuk dikenali dan diwarnai
    PATTERNS = {
        # Status icons
        (r'\[✓\]', Colors.BRIGHT_GREEN): '✅',
        (r'\[✅\]', Colors.BRIGHT_GREEN): '✅',
        (r'\[✗\]', Colors.BRIGHT_RED): '❌',
        (r'\[❌\]', Colors.BRIGHT_RED): '❌',
        (r'\[⚠\]', Colors.BRIGHT_YELLOW): '⚠️',
        (r'\[⚠️\]', Colors.BRIGHT_YELLOW): '⚠️',
        (r'\[INFO\]', Colors.BRIGHT_CYAN): 'ℹ️',
        (r'\[WARN\]', Colors.BRIGHT_YELLOW): '⚠️',
        (r'\[ERROR\]', Colors.BRIGHT_RED): '❌',
        (r'\[SUCCESS\]', Colors.BRIGHT_GREEN): '✅',
        
        # Keywords
        (r'RUNNING', Colors.BRIGHT_GREEN): 'RUNNING',
        (r'ONLINE', Colors.BRIGHT_GREEN): 'ONLINE',
        (r'AVAILABLE', Colors.BRIGHT_GREEN): 'AVAILABLE',
        (r'OFFLINE', Colors.BRIGHT_RED): 'OFFLINE',
        (r'UNAVAILABLE', Colors.BRIGHT_RED): 'UNAVAILABLE',
        (r'ERROR', Colors.BRIGHT_RED): 'ERROR',
        (r'WARNING', Colors.BRIGHT_YELLOW): 'WARNING',
        (r'CRITICAL', Colors.BRIGHT_RED): 'CRITICAL',
        
        # Headers
        (r'={10,}', Colors.BRIGHT_MAGENTA): '═',
        (r'-{10,}', Colors.BRIGHT_BLUE): '─',
        
        # Module names
        (r'\[✓\] \w+', Colors.BRIGHT_GREEN): '✓',
        (r'\[✗\] \w+', Colors.BRIGHT_RED): '✗',
    }
    
    @classmethod
    def colorize(cls, text):
        """Colorize text based on patterns."""
        result = text
        
        # Special coloring for specific patterns
        # Timestamp (dim)
        result = re.sub(
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})',
            f'{Colors.DIM}\\1{Colors.RESET}',
            result
        )
        
        # Level badges
        result = re.sub(
            r'(\| INFO \|)',
            f'{Colors.BRIGHT_CYAN}\\1{Colors.RESET}',
            result
        )
        result = re.sub(
            r'(\| WARNING \|)',
            f'{Colors.BRIGHT_YELLOW}\\1{Colors.RESET}',
            result
        )
        result = re.sub(
            r'(\| ERROR \|)',
            f'{Colors.BRIGHT_RED}\\1{Colors.RESET}',
            result
        )
        result = re.sub(
            r'(\| CRITICAL \|)',
            f'{Colors.BRIGHT_RED}{Colors.BOLD}\\1{Colors.RESET}',
            result
        )
        
        # ✅ Success markers
        result = re.sub(
            r'(✅)',
            f'{Colors.BRIGHT_GREEN}\\1{Colors.RESET}',
            result
        )
        
        # ❌ Error markers
        result = re.sub(
            r'(❌)',
            f'{Colors.BRIGHT_RED}\\1{Colors.RESET}',
            result
        )
        
        # ⚠️ Warning markers
        result = re.sub(
            r'(⚠️)',
            f'{Colors.BRIGHT_YELLOW}\\1{Colors.RESET}',
            result
        )
        
        # ℹ️ Info markers
        result = re.sub(
            r'(ℹ️)',
            f'{Colors.BRIGHT_CYAN}\\1{Colors.RESET}',
            result
        )
        
        # Status: SUCCESS, OK, etc.
        result = re.sub(
            r'\b(SUCCESS|OK|ACTIVE|ONLINE|RUNNING|AVAILABLE|READY)\b',
            f'{Colors.BRIGHT_GREEN}\\1{Colors.RESET}',
            result
        )
        
        # Status: ERROR, FAILED, etc.
        result = re.sub(
            r'\b(ERROR|FAILED|OFFLINE|UNAVAILABLE|CRASHED)\b',
            f'{Colors.BRIGHT_RED}\\1{Colors.RESET}',
            result
        )
        
        # Status: WARNING
        result = re.sub(
            r'\b(WARNING|WARN|DEGRADED)\b',
            f'{Colors.BRIGHT_YELLOW}\\1{Colors.RESET}',
            result
        )
        
        # Version numbers
        result = re.sub(
            r'(v\d+\.\d+\.\d+)',
            f'{Colors.BRIGHT_MAGENTA}\\1{Colors.RESET}',
            result
        )
        
        # Port numbers
        result = re.sub(
            r'(:\d{4,5})',
            f'{Colors.BRIGHT_CYAN}\\1{Colors.RESET}',
            result
        )
        
        # HTTP/HTTPS
        result = re.sub(
            r'(http[s]?://)',
            f'{Colors.BRIGHT_BLUE}\\1{Colors.RESET}',
            result
        )
        
        # EXCHANGE
        result = re.sub(
            r'(Exchange)',
            f'{Colors.BRIGHT_YELLOW}\\1{Colors.RESET}',
            result
        )
        
        return result

# ============================================================
# MAIN - Live Log Viewer
# ============================================================

def view_log(filepath='logs/main.log', follow=True):
    """View log with colors."""
    if not os.path.exists(filepath):
        print(f"{Colors.BRIGHT_RED}❌ Log file not found: {filepath}{Colors.RESET}")
        return
    
    print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}")
    print("=" * 70)
    print("  🎨 INKSIDE DIGITAL - COLORED LOG VIEWER")
    print("  Press Ctrl+C to exit")
    print("=" * 70)
    print(f"{Colors.RESET}")
    print(f"{Colors.DIM}  File: {filepath}{Colors.RESET}\n")
    
    try:
        if follow:
            # Live tail
            with open(filepath, 'r') as f:
                # Go to end
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        print(LogColorizer.colorize(line.rstrip()))
                    else:
                        time.sleep(0.1)
        else:
            # Show all
            with open(filepath, 'r') as f:
                for line in f:
                    print(LogColorizer.colorize(line.rstrip()))
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}👋 Exiting...{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.BRIGHT_RED}❌ Error: {e}{Colors.RESET}")

# ============================================================
# COMMAND LINE
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Colored log viewer for Inkside Digital')
    parser.add_argument('-f', '--file', default='logs/main.log', help='Log file path')
    parser.add_argument('-n', '--no-follow', action='store_true', help='Don\'t follow (show all)')
    
    args = parser.parse_args()
    
    view_log(args.file, not args.no_follow)
