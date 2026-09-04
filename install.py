#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# INKSIDE DIGITAL - BEAUTIFUL INSTALLER
# ============================================================

import subprocess
import sys
import time
import os
from datetime import datetime

# ============================================================
# ANSI COLORS
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
    DIM = '\033[2m'
    RESET = '\033[0m'
    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

# ============================================================
# BEAUTIFUL PRINT FUNCTIONS
# ============================================================

def print_banner():
    """Print beautiful installation banner"""
    banner = f"""
{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   {Colors.GREEN}🧠 INKSIDE DIGITAL{Colors.CYAN} - COGNITIVE MIRROR ENGINE          ║
║   {Colors.WHITE}🚀 Autonomous Intelligence Trading System{Colors.CYAN}              ║
║                                                                      ║
║   {Colors.DIM}📦 Installing Dependencies...{Colors.CYAN}                              ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def print_step(step, message, status='info'):
    """Print installation step with status"""
    icons = {
        'info': '📘',
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'loading': '⏳',
        'done': '🎯',
        'package': '📦',
        'install': '🔧',
        'check': '🔍',
        'build': '🏗️',
    }
    
    colors = {
        'info': Colors.CYAN,
        'success': Colors.GREEN,
        'error': Colors.RED,
        'warning': Colors.YELLOW,
        'loading': Colors.YELLOW,
        'done': Colors.GREEN,
        'package': Colors.PURPLE,
        'install': Colors.BLUE,
        'check': Colors.CYAN,
        'build': Colors.ORANGE,
    }
    
    icon = icons.get(status, '📌')
    color = colors.get(status, Colors.WHITE)
    
    print(f"{Colors.DIM}{datetime.now().strftime('%H:%M:%S')}{Colors.RESET} "
          f"{color}{icon} [{step}] {message}{Colors.RESET}")

def print_separator():
    print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")

def print_progress_bar(current, total, prefix='', suffix='', length=40):
    """Print progress bar"""
    percent = current / total
    filled = int(length * percent)
    bar = '█' * filled + '░' * (length - filled)
    
    color = Colors.GREEN if percent >= 0.7 else Colors.YELLOW if percent >= 0.3 else Colors.ORANGE
    
    print(f"\r{prefix} [{color}{bar}{Colors.RESET}] {current}/{total} {suffix}", end='', flush=True)
    if current == total:
        print()

# ============================================================
# MAIN INSTALLATION
# ============================================================

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print_banner()
    print_separator()
    
    # Step 1: Check Python
    print_step('1/5', 'Checking Python version...', 'check')
    python_version = sys.version_info
    print(f"   {Colors.WHITE}✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}{Colors.RESET}")
    print_separator()
    
    # Step 2: Upgrade pip
    print_step('2/5', 'Upgrading pip...', 'install')
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"   {Colors.GREEN}✅ pip upgraded{Colors.RESET}")
    print_separator()
    
    # Step 3: Install dependencies with progress
    print_step('3/5', 'Installing dependencies from requirements.txt...', 'package')
    print()
    
    # Read requirements
    with open('requirements.txt', 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    total = len(packages)
    installed = 0
    
    for i, package in enumerate(packages, 1):
        # Parse package name
        pkg_name = package.split('==')[0] if '==' in package else package
        pkg_name = pkg_name.split('>=')[0] if '>=' in pkg_name else pkg_name
        
        print_progress_bar(i, total, prefix=f'📦 {pkg_name[:25]:<25}', 
                          suffix=f'({i}/{total})', length=30)
        
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package, '--quiet'],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            installed += 1
        except:
            print(f"\n   {Colors.RED}❌ Failed: {pkg_name}{Colors.RESET}")
    
    print()
    print_separator()
    
    # Step 4: Summary
    print_step('4/5', 'Installation Summary', 'done')
    print(f"   {Colors.GREEN}✅ Successfully installed: {installed}/{total} packages{Colors.RESET}")
    
    if installed == total:
        print(f"   {Colors.GREEN}🎉 All dependencies installed successfully!{Colors.RESET}")
    else:
        print(f"   {Colors.YELLOW}⚠️ {total - installed} package(s) failed. Check logs.{Colors.RESET}")
    
    print_separator()
    
    # Step 5: Final
    print_step('5/5', 'Setup Complete!', 'success')
    print(f"""
{Colors.BOLD}{Colors.GREEN}╔════════════════════════════════════════════════════════════╗
║                                                                    ║
║   🎉 INKSIDE DIGITAL is ready to run!                             ║
║                                                                    ║
║   {Colors.CYAN}🚀 Run: {Colors.WHITE}python main.py{Colors.GREEN}                             ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

if __name__ == "__main__":
    main()
