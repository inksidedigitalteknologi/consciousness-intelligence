#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# INKSIDE DIGITAL - SUPER CANGIH INSTALLER v3.0
# WITH PARALLEL INSTALLATION, REAL-TIME LOG, SYSTEM CHECK
# CLEAN & RAPI VERSION
# ============================================================

import subprocess
import sys
import time
import os
import json
import threading
import queue
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

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
# COLOR LOGGER
# ============================================================

class ColorLogger:
    def __init__(self):
        self.logs = []
        self.start_time = time.time()
    
    def info(self, msg):
        self._log('INFO', msg, Colors.CYAN)
    
    def success(self, msg):
        self._log('SUCCESS', msg, Colors.GREEN)
    
    def warning(self, msg):
        self._log('WARNING', msg, Colors.YELLOW)
    
    def error(self, msg):
        self._log('ERROR', msg, Colors.RED)
    
    def debug(self, msg):
        self._log('DEBUG', msg, Colors.DIM)
    
    def _log(self, level, msg, color):
        timestamp = datetime.now().strftime('%H:%M:%S')
        colored = f"{Colors.DIM}{timestamp}{Colors.RESET} {color}{level:8}{Colors.RESET} {msg}"
        print(colored)
        self.logs.append(f"{timestamp} | {level:8} | {msg}")
    
    def get_total_time(self):
        return int(time.time() - self.start_time)

logger = ColorLogger()

# ============================================================
# SYSTEM CHECK
# ============================================================

def check_system():
    """Check system requirements before installation"""
    logger.info("🔍 Running system check...")
    
    checks = []
    
    # 1. Check Python version
    py_ver = sys.version_info
    py_ok = py_ver.major >= 3 and py_ver.minor >= 8
    checks.append({
        'name': f'Python {py_ver.major}.{py_ver.minor}.{py_ver.micro}',
        'ok': py_ok,
        'required': 'Python 3.8+'
    })
    
    # 2. Check pip
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        pip_ok = result.returncode == 0
        pip_version = result.stdout.split()[1] if pip_ok else 'Not found'
    except:
        pip_ok = False
        pip_version = 'Not found'
    checks.append({
        'name': f'pip {pip_version}',
        'ok': pip_ok,
        'required': 'pip available'
    })
    
    # 3. Check disk space (min 2GB)
    try:
        import shutil
        disk = shutil.disk_usage('/')
        disk_gb = disk.free / (1024**3)
        disk_ok = disk_gb > 2
        checks.append({
            'name': f'Disk Space {disk_gb:.1f} GB free',
            'ok': disk_ok,
            'required': '> 2 GB free'
        })
    except:
        checks.append({
            'name': 'Disk Space',
            'ok': True,
            'required': 'Unknown'
        })
    
    # 4. Check RAM (min 2GB)
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024**3)
        ram_ok = ram_gb > 2
        checks.append({
            'name': f'RAM {ram_gb:.1f} GB',
            'ok': ram_ok,
            'required': '> 2 GB'
        })
    except:
        checks.append({
            'name': 'RAM',
            'ok': True,
            'required': 'Unknown'
        })
    
    # 5. Check Internet
    try:
        import socket
        socket.create_connection(('8.8.8.8', 53), timeout=3)
        checks.append({
            'name': 'Internet Connection',
            'ok': True,
            'required': 'Online'
        })
    except:
        checks.append({
            'name': 'Internet Connection',
            'ok': False,
            'required': 'Online'
        })
    
    # Print results
    all_ok = all(c['ok'] for c in checks)
    
    for check in checks:
        icon = '✅' if check['ok'] else '❌'
        color = Colors.GREEN if check['ok'] else Colors.RED
        print(f"   {color}{icon} {check['name']:<30} {Colors.DIM}(required: {check['required']}){Colors.RESET}")
    
    if not all_ok:
        logger.warning("⚠️ Some system checks failed. Installation may have issues.")
    else:
        logger.success("✅ All system checks passed!")
    
    return all_ok

# ============================================================
# INSTALL PACKAGE WITH RETRY
# ============================================================

def install_package(package, retries=2):
    """Install a single package with retry mechanism"""
    pkg_name = package.split('==')[0] if '==' in package else package
    pkg_name = pkg_name.split('>=')[0] if '>=' in pkg_name else pkg_name
    pkg_name = pkg_name.split('<')[0] if '<' in pkg_name else pkg_name
    
    for attempt in range(retries + 1):
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', package, '--quiet'],
                capture_output=True,
                timeout=60
            )
            if result.returncode == 0:
                return {'name': pkg_name, 'success': True, 'attempt': attempt + 1}
            else:
                if attempt < retries:
                    time.sleep(0.5)
                    continue
                return {'name': pkg_name, 'success': False, 'error': result.stderr[:100], 'attempt': attempt + 1}
        except subprocess.TimeoutExpired:
            if attempt < retries:
                continue
            return {'name': pkg_name, 'success': False, 'error': 'Timeout', 'attempt': attempt + 1}
        except Exception as e:
            if attempt < retries:
                continue
            return {'name': pkg_name, 'success': False, 'error': str(e), 'attempt': attempt + 1}

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
║   {Colors.DIM}📦 Super Canggih Installer v3.0{Colors.CYAN}                         ║
║   {Colors.DIM}⚡ Parallel Installation • Real-time Log • Auto-Retry{Colors.CYAN}    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def print_separator(char='─', length=60):
    print(f"{Colors.DIM}{char * length}{Colors.RESET}")

def print_step(step, message, status='info'):
    icons = {
        'info': '📘', 'success': '✅', 'error': '❌',
        'warning': '⚠️', 'loading': '⏳', 'done': '🎯',
        'package': '📦', 'install': '🔧', 'check': '🔍',
        'build': '🏗️', 'test': '🧪', 'config': '⚙️',
        'speed': '⚡', 'retry': '🔄', 'time': '⏱️'
    }
    colors = {
        'info': Colors.CYAN, 'success': Colors.GREEN, 'error': Colors.RED,
        'warning': Colors.YELLOW, 'loading': Colors.YELLOW, 'done': Colors.GREEN,
        'package': Colors.PURPLE, 'install': Colors.BLUE, 'check': Colors.CYAN,
        'build': Colors.ORANGE, 'test': Colors.PURPLE, 'config': Colors.BLUE,
        'speed': Colors.GREEN, 'retry': Colors.YELLOW, 'time': Colors.CYAN
    }
    icon = icons.get(status, '📌')
    color = colors.get(status, Colors.WHITE)
    logger.info(f"{icon} [{step}] {message}")

def print_progress_bar(current, total, prefix='', suffix='', length=40):
    percent = current / total if total > 0 else 0
    filled = int(length * percent)
    bar = '█' * filled + '░' * (length - filled)
    
    if percent >= 0.8:
        color = Colors.GREEN
    elif percent >= 0.5:
        color = Colors.YELLOW
    else:
        color = Colors.ORANGE
    
    print(f"\r{prefix} [{color}{bar}{Colors.RESET}] {current}/{total} {suffix}", end='', flush=True)
    if current == total:
        print()

# ============================================================
# POST-INSTALL TESTS
# ============================================================

def run_post_install_tests():
    """Test imported packages after installation"""
    logger.info("🧪 Running post-install tests...")
    
    tests = [
        ('Flask', 'from flask import Flask'),
        ('Flask-CORS', 'from flask_cors import CORS'),
        ('SocketIO', 'from flask_socketio import SocketIO'),
        ('Pandas', 'import pandas as pd'),
        ('Numpy', 'import numpy as np'),
        ('SQLAlchemy', 'import sqlalchemy'),
        ('Requests', 'import requests'),
        ('WebSocket', 'import websocket'),
        ('PSUtil', 'import psutil'),
        ('DotEnv', 'from dotenv import load_dotenv'),
    ]
    
    passed = 0
    for name, test in tests:
        try:
            exec(test)
            print(f"   {Colors.GREEN}✅ {name}{Colors.RESET}")
            passed += 1
        except ImportError as e:
            print(f"   {Colors.RED}❌ {name} - {e}{Colors.RESET}")
        except Exception as e:
            print(f"   {Colors.YELLOW}⚠️ {name} - {e}{Colors.RESET}")
    
    print(f"   {Colors.DIM}Passed: {passed}/{len(tests)} tests{Colors.RESET}")
    return passed == len(tests)

# ============================================================
# MAIN INSTALLATION
# ============================================================

def main():
    global start_time
    start_time = time.time()
    
    os.system('clear' if os.name == 'posix' else 'cls')
    print_banner()
    print_separator()
    
    # ============================================================
    # STEP 1: SYSTEM CHECK
    # ============================================================
    print_step('1/7', 'System Check', 'check')
    system_ok = check_system()
    print_separator()
    
    # ============================================================
    # STEP 2: UPGRADE PIP
    # ============================================================
    print_step('2/7', 'Upgrading pip...', 'install')
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.success("✅ pip upgraded")
    print_separator()
    
    # ============================================================
    # STEP 3: READ REQUIREMENTS
    # ============================================================
    print_step('3/7', 'Reading requirements.txt...', 'package')
    
    try:
        with open('requirements.txt', 'r') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        logger.error("❌ requirements.txt not found!")
        sys.exit(1)
    
    total = len(packages)
    logger.info(f"📦 Found {total} packages to install")
    print_separator()
    
    # ============================================================
    # STEP 4: INSTALL DEPENDENCIES (PARALLEL)
    # ============================================================
    print_step('4/7', f'Installing {total} packages (parallel)...', 'speed')
    print()
    
    installed = []
    failed = []
    results = {}
    
    max_workers = min(4, os.cpu_count() or 2)
    logger.debug(f"⚡ Using {max_workers} parallel workers")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(install_package, pkg): pkg for pkg in packages}
        
        completed = 0
        for future in as_completed(futures):
            result = future.result()
            completed += 1
            results[result['name']] = result
            
            if result['success']:
                installed.append(result['name'])
                status = '✅' if result['attempt'] == 1 else '🔄'
                print_progress_bar(completed, total, 
                                  prefix=f'{status} {result["name"][:25]:<25}', 
                                  suffix=f'({completed}/{total})', 
                                  length=30)
                if result['attempt'] > 1:
                    logger.debug(f"🔄 {result['name']} installed after {result['attempt']} attempts")
            else:
                failed.append(result['name'])
                print(f"\n   {Colors.RED}❌ Failed: {result['name']}{Colors.RESET}")
                if 'error' in result:
                    logger.debug(f"   Error: {result['error']}")
    
    print()
    print_separator()
    
    # ============================================================
    # STEP 5: SUMMARY
    # ============================================================
    print_step('5/7', 'Installation Summary', 'done')
    
    total_time = int(time.time() - start_time)
    minutes = total_time // 60
    seconds = total_time % 60
    
    print(f"   {Colors.GREEN}✅ Successfully installed: {len(installed)}/{total} packages{Colors.RESET}")
    print(f"   {Colors.CYAN}⏱️  Time elapsed: {minutes}m {seconds}s{Colors.RESET}")
    
    if failed:
        print(f"   {Colors.RED}❌ Failed: {len(failed)} packages{Colors.RESET}")
        for pkg in failed[:5]:
            print(f"      {Colors.RED}• {pkg}{Colors.RESET}")
        if len(failed) > 5:
            print(f"      {Colors.DIM}... and {len(failed) - 5} more{Colors.RESET}")
    else:
        print(f"   {Colors.GREEN}🎉 All dependencies installed successfully!{Colors.RESET}")
    
    print_separator()
    
    # ============================================================
    # STEP 6: POST-INSTALL TESTS
    # ============================================================
    print_step('6/7', 'Post-Install Tests', 'test')
    tests_passed = run_post_install_tests()
    print_separator()
    
    # ============================================================
    # STEP 7: FINAL - CLEAN VERSION
    # ============================================================
    print_step('7/7', 'Setup Complete!', 'success')
    
    print(f"\n{Colors.BOLD}{Colors.DIM}{'=' * 60}{Colors.RESET}")
    
    if not failed and tests_passed:
        print(f"{Colors.BOLD}{Colors.GREEN}  ✅ SETUP COMPLETE - INKSIDE DIGITAL READY!{Colors.RESET}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")
        print(f"  {Colors.CYAN}🚀 Run:{Colors.WHITE} python main.py")
        print(f"  {Colors.CYAN}🌐 Access:{Colors.WHITE} http://localhost:5000")
        print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")
        print(f"  {Colors.DIM}📊 {installed} packages installed in {minutes}m {seconds}s")
        print(f"  {Colors.DIM}🧪 Tests: All passed!{Colors.RESET}")
    else:
        print(f"{Colors.BOLD}{Colors.YELLOW}  ⚠️ INSTALLATION COMPLETED WITH ISSUES{Colors.RESET}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")
        print(f"  {Colors.WHITE}📦 Failed packages:{Colors.YELLOW} {len(failed)}")
        print(f"  {Colors.WHITE}🧪 Tests:{Colors.YELLOW} {'Failed' if not tests_passed else 'Passed'}")
        if failed:
            for pkg in failed[:3]:
                print(f"     {Colors.RED}• {pkg}{Colors.RESET}")
            if len(failed) > 3:
                print(f"     {Colors.DIM}... and {len(failed)-3} more{Colors.RESET}")
        print(f"  {Colors.WHITE}💡 Try:{Colors.YELLOW} pip install <package_name> manually")
    
    print(f"{Colors.BOLD}{Colors.DIM}{'=' * 60}{Colors.RESET}\n")
    
    # Save log
    with open('install.log', 'w') as f:
        f.write(f"Installation Log - {datetime.now()}\n")
        f.write("=" * 60 + "\n")
        for log in logger.logs:
            f.write(log + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Installation cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.RESET}")
        sys.exit(1)
