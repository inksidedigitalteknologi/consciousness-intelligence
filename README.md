#  Inkside Digital - Cognitive Mirror Engine v5.1.0

**The Future of Algorithmic Trading | AI-Powered Market Intelligence with Self-Learning Capabilities**

[![Version](https://img.shields.io/badge/version-5.1.0-blue.svg)](https://github.com/yourusername/consciousness-intelligence)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-18.3.1-61dafb.svg)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/flask-2.3.3-black.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Production_Ready-brightgreen.svg)]()

---

##  Overview

**Inkside Digital - Cognitive Mirror Engine** is an advanced algorithmic trading system that combines:

-  **Cognitive Computing** - Self-learning AI that adapts to market conditions
-  **Multi-Timeframe Analysis** - Scans 6 different timeframes simultaneously
-  **Predictive Analytics** - 16 prediction methods working in parallel
-  **Pattern Recognition** - Identifies complex market patterns
-  **Autonomous Learning** - Continuous improvement from market data
-  **Self-Healing** - Watchdog system with circuit breaker protection
-  **Telegram Integration** - 11 real-time commands for monitoring
-  **Permanent Memory** - Knowledge base with state management

---

## Features

### Core Intelligence
| Feature | Description |
|---------|-------------|
| **Cognitive Brain** | Self-aware decision engine with state management and reflection |
| **Adaptive Learning** | Self-improving weights with confidence calibration |
| **Pattern Recognition** | Candlestick & wave pattern detection across multiple timeframes |
| **Prediction Engine** | Monte Carlo & ML-based forecasting with confidence scoring |
| **Knowledge Engine** | Permanent memory storage with semantic search and relationships |

### Trading & Analysis
| Feature | Description |
|---------|-------------|
| **Multi-Timeframe Analysis** | 5m, 15m, 1h, 4h, 1d, 1w alignment filters |
| **Signal Generation** | Real-time signals with confidence and success rate |
| **Position Management** | Open position tracking with PnL monitoring |
| **Risk Management** | Circuit breaker protection and risk scoring |
| **Paper Trading** | Test strategies without real capital |

### Monitoring & Control
| Feature | Description |
|---------|-------------|
| **Watchdog v3.0** | Health monitoring, auto-restart, circuit breaker |
| **Telegram Bridge** | 11 commands: /start, /health, /signals, /performance, /pnl, /brain, /modules, /daily, /risk, /trade, /refresh |
| **Web Dashboard** | Real-time UI with HealthView, LearningView, KnowledgeView |
| **System Metrics** | CPU, RAM, uptime, health score, risk level |

### Intelligence Modules (30+ Subsystems)
| Category | Modules |
|----------|---------|
| **Learning** | Learning Engine, Market Learning, Pattern Engine, Prediction, Reasoning |
| **Decision** | Decision Engine, Strategy Generation, Goal Manager |
| **Memory** | Experience Engine, Semantic Memory, Knowledge Graph, Archive Manager |
| **Analysis** | Feature Extractor, Entity Recognition, Normalizer, Data Cleaner |
| **Self** | Self-Diagnostic, Improvement Engine, Behavior Learning, Reflection |



## Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| Node.js | 18+ |
| Git | Latest |
| pip | Latest |
| npm | Latest |

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/consciousness-intelligence.git
cd consciousness-intelligence

# 2. Backend setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Frontend setup
cd frontend
npm install

# 4. Configuration
cp .env.example .env
# Edit .env with your Telegram Bot Token and Chat ID

## Architecture

# Trading Mode
INKSIDE_MODE=PAPER              # PAPER or LIVE
API_PORT=5001
API_HOST=0.0.0.0

# Telegram (Required for bot commands)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Exchange (Optional - for live trading)
KRAKEN_API_KEY=your_api_key
KRAKEN_API_SECRET=your_api_secret

# Risk Management
RISK_LEVEL=MODERATE
TRADING_MODE=PAPER


# Terminal 1: Backend
cd ~/consciousness-intelligence
source venv/bin/activate
python main.py

# Terminal 2: Frontend
cd ~/consciousness-intelligence/frontend
npm run dev -- --host 0.0.0.0 --port 3000
