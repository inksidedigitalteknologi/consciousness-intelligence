# 🧠 Inkside Digital - Cognitive Mirror Engine v2.0.0

**The Future of Algorithmic Trading & Dividend Intelligence | AI-Powered Market Intelligence with Self-Learning Capabilities | Real-time Signals • Pattern Recognition • Autonomous Execution • Dividend Hunting**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/inksidedigitalteknologi/consciousness-intelligence)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-18.3.1-61dafb.svg)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/flask-2.3.3-black.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Production_Ready-brightgreen.svg)]()
[![Data](https://img.shields.io/badge/data-100%25_REAL-success.svg)]()
[![Focus](https://img.shields.io/badge/focus-Dividend_Hunter_&_IDX-orange.svg)]()

---

## 📋 Overview

**Inkside Digital - Cognitive Mirror Engine v2.0.0** is an advanced algorithmic trading and dividend intelligence system that combines:

- 🧠 **Cognitive Computing** - Self-learning AI that adapts to market conditions
- 💰 **Dividend Hunter** - Auto-fetch, screen, and analyze dividend stocks from Nasdaq API
- 📊 **IDX Market Data** - Real-time Indonesia Stock Exchange data from Google Sheets
- 📈 **Multi-Timeframe Analysis** - Scans multiple timeframes simultaneously
- 🔮 **Predictive Analytics** - Multiple prediction methods working in parallel
- 🎯 **Autonomous Learning** - Continuous improvement from market data
- 🛡️ **Self-Healing** - Watchdog system with circuit breaker protection
- 🤖 **Telegram Integration** - Real-time commands for monitoring
- 💾 **Permanent Memory** - Knowledge base with state management
- 🔐 **API Key Authentication** - Secure access to all endpoints
- 📡 **WebSocket Real-time Updates** - Live data streaming via Socket.IO
- 📊 **Portfolio Simulation** - Dividend portfolio projection with reinvestment

---

## ✨ Features

### 🧠 Core Intelligence
| Feature | Description |
|---------|-------------|
| **Cognitive Brain** | Self-aware decision engine with state management and reflection |
| **Adaptive Learning** | Self-improving weights with confidence calibration |
| **Pattern Recognition** | 20+ candlestick & wave pattern detection across multiple timeframes |
| **Prediction Engine** | Monte Carlo & ML-based forecasting with confidence scoring |
| **Knowledge Engine** | Permanent memory storage with semantic search and relationships |
| **Autonomous Learning** | RSS feed auto-learning with Indonesia content filter |

### 💰 Dividend Intelligence
| Feature | Description |
|---------|-------------|
| **Dividend Fetch** | Auto-fetch dividend data from Nasdaq API |
| **Dividend Analysis** | Yield, growth rate, payout ratio, safety score |
| **Multi-Criteria Screening** | Filter by dividend, yield, safety, sector, quality |
| **Dividend Calendar** | Monthly/Yearly dividend calendar |
| **Portfolio Simulation** | Simulate dividend portfolio with reinvestment |
| **Alert System** | Ex-date approaching alerts with priority levels |
| **Export** | Export to Excel (multi-sheet), CSV, JSON |
| **Quality Rating** | EXCELLENT, GOOD, FAIR, POOR ratings |

### 📈 Trading & Analysis
| Feature | Description |
|---------|-------------|
| **Multi-Timeframe Analysis** | 5m, 15m, 1h, 4h, 1d, 1w alignment filters |
| **Signal Generation** | Real-time signals with confidence and success rate |
| **Position Management** | Open position tracking with PnL monitoring |
| **Risk Management** | Circuit breaker protection and risk scoring |
| **Paper Trading** | Test strategies without real capital |

### 🛡️ Monitoring & Control
| Feature | Description |
|---------|-------------|
| **Watchdog v3.2** | Health monitoring, auto-restart, circuit breaker, latency tracking, component heartbeat |
| **Telegram Bridge** | 11 commands: /start, /health, /signals, /performance, /pnl, /brain, /modules, /daily, /risk, /trade, /refresh |
| **Web Dashboard** | Real-time UI with DashboardView, HealthView, LearningView, PredictionView, TradingControlView |
| **System Metrics** | CPU, RAM, uptime, health score, risk level |
| **Component Health** | Per-component health tracking with circuit breaker |

### 🧬 Intelligence Modules (32+ Subsystems)
| Category | Modules |
|----------|---------|
| **Learning** | Learning Engine, Market Learning, Pattern Engine, Prediction, Reasoning |
| **Decision** | Decision Engine, Strategy Generation, Goal Manager |
| **Memory** | Experience Engine, Semantic Memory, Knowledge Graph, Archive Manager |
| **Analysis** | Feature Extractor, Entity Recognition, Normalizer, Data Cleaner |
| **Self** | Self-Diagnostic, Improvement Engine, Behavior Learning, Reflection |

---

## 🔌 API Endpoints

### Public Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check (no auth required) |

### Protected Endpoints (API Key Required)

#### System
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | System status |
| `/api/performance` | GET | Trading performance |
| `/api/system/metrics` | GET | CPU, RAM, uptime, health score |
| `/api/diagnostics` | GET | System diagnostics |
| `/api/engine/start` | POST | Start trading engine |
| `/api/engine/stop` | POST | Stop trading engine |
| `/api/engine/status` | GET | Engine status |

#### Brain & Signals
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/brain/state` | GET | Cognitive Brain state |
| `/api/brain/status` | GET | Brain status (alias) |
| `/api/signals` | GET | Live signals |

#### Watchdog
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/watchdog/status` | GET | Watchdog status |
| `/api/watchdog/snapshot` | GET | Watchdog snapshot |

#### Dividend
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dividend/fetch` | POST | Fetch dividend data for a date |
| `/api/dividend/top` | GET | Top N dividends |
| `/api/dividend/upcoming` | GET | Upcoming dividends in X days |
| `/api/dividend/screen` | POST | Multi-criteria screening |
| `/api/dividend/alerts` | GET | Dividend alerts |
| `/api/dividend/stats` | GET | Dividend statistics |
| `/api/dividend/sectors` | GET | Sector summary |
| `/api/dividend/analysis` | GET | Comprehensive analysis |
| `/api/dividend/best-yield` | GET | Highest yield stocks |
| `/api/dividend/safest` | GET | Highest safety score |
| `/api/dividend/calendar` | GET | Dividend calendar |
| `/api/dividend/portfolio-simulate` | POST | Portfolio simulation |

#### AI
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ai/status` | GET | AI integration status |
| `/api/ai/ask` | POST | Ask AI a question |
| `/api/ai/chat` | POST | Chat with AI with memory |
| `/api/ai/brain/reflection` | GET | Brain reflection with AI |
| `/api/ai/brain/status` | GET | Brain AI status |

#### Knowledge
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/knowledge/search` | POST | Search knowledge base |
| `/api/knowledge/add` | POST | Add item to knowledge base |
| `/api/knowledge/stats` | GET | Knowledge base statistics |

#### Telegram
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/telegram/status` | GET | Telegram status |
| `/api/telegram/send` | POST | Send Telegram message |

---

## 🤖 Telegram Commands

| Command | Description |
|---------|-------------|
| `/start` | System overview |
| `/health` | Health check |
| `/performance` | Trading performance |
| `/signals` | Live signals |
| `/pnl` | Profit/Loss report |
| `/brain` | Brain status |
| `/modules` | Module status |
| `/daily` | Daily report |
| `/risk` | Risk assessment |
| `/trade` | Quick trade action |
| `/refresh` | Refresh data |

---

## 📊 Data Sources

| Data | Source | Status |
|------|--------|--------|
| **Dividend Data** | Nasdaq API | ✅ REAL |
| **IDX Stock Prices** | Google Sheets | ✅ REAL |
| **System Metrics** | psutil | ✅ REAL |
| **Health Score** | Weighted metrics | ✅ REAL |
| **Risk Level** | Health score | ✅ REAL |
| **Market Regime** | Regime detection | ✅ REAL |
| **Trading Signals** | Signal Engine | ✅ REAL |
| **Knowledge Base** | Local Database | ✅ REAL |

**100% REAL DATA - No Dummy Data!**


### Installation

```bash
# Clone repository
git clone https://github.com/inksidedigitalteknologi/consciousness-intelligence.git
cd consciousness-intelligence

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Run server
python main.py
Using Manage Script
bash
# Start server
./manage.sh start

# Stop server
./manage.sh stop

# Restart server
./manage.sh restart

# Check status
./manage.sh status

# View logs
./manage.sh logs

# Health check
./manage.sh health
📋 Environment Variables
Variable	Description	Default
API_KEY	API authentication key	iks_7x9mK2wP5vN8qR3tY6uA1eF4cH0jL9oZ
API_PORT	API server port	5000
API_HOST	API server host	0.0.0.0
INKSIDE_MODE	Trading mode (PAPER/LIVE)	PAPER
DEEPSEEK_ENABLED	Enable DeepSeek AI	false
DEEPSEEK_API_KEY	DeepSeek API key	-
TELEGRAM_BOT_TOKEN	Telegram bot token	-
TELEGRAM_CHAT_ID	Telegram chat ID	-
GOOGLE_SHEETS_API_KEY	Google Sheets API key	-
IDX_SHEET_ID	IDX Google Sheet ID	-
📊 Module Status
Module	Status	Description
adaptive	✅	Adaptive learning engine
analyzer	✅	Market analyzer
archive	✅	Archive manager
association	✅	Association engine
autonomous	⚠️	Autonomous learning (needs feedparser)
behavior	✅	Behavior engine
bootstrap	✅	Bootstrap loader
bot	✅	Trading bot
brain	⚠️	Cognitive brain (11/19 modules)
consciousness	✅	Consciousness module
context_manager	✅	Context manager
contracts	✅	Smart contracts
curiosity	✅	Curiosity engine
data_pipeline	✅	Data pipeline
decision_engine	✅	Decision engine
deepseek	⚠️	AI integration (needs openai)
diagnostics	✅	System diagnostics
dividend	✅	Dividend hunter
entity_recognition	✅	Entity recognition
evaluator	✅	Evaluation engine
event	✅	Event bus
experience	✅	Experience engine
goal_manager	✅	Goal manager
health	✅	Health monitor
improvement	✅	Improvement engine
insight	✅	Insight engine
knowledge	✅	Knowledge engine
knowledge_builder	✅	Knowledge builder
knowledge_graph	✅	Knowledge graph
learning_analyzer	✅	Learning analyzer
learning_engine	✅	Learning engine
learning_memory	✅	Learning memory
market_learning	✅	Market learning
memory	✅	Memory engine
memory_optimizer	✅	Memory optimizer
module_manager	✅	Module manager
module_registry	✅	Module registry
pattern	✅	Pattern engine
prediction	✅	Prediction engine
reasoning	✅	Reasoning engine
reflection	✅	Reflection engine
runtime	✅	Runtime manager
scanner	⚠️	Market scanner
scheduler	✅	Task scheduler
self_diagnostic	✅	Self diagnostic
semantic_memory	✅	Semantic memory
semantic_processor	✅	Semantic processor
signal	✅	Signal engine
simulation	✅	Simulation engine
strategy	✅	Strategy engine
system_config	✅	System config
validator	✅	Module validator
watchdog	⚠️	System watchdog
Health: 88.9% (48/54 modules active)

🛠️ Technologies Used
Category	Technology
Backend	Python 3.10+, Flask, Flask-SocketIO, Flask-CORS
Frontend	React 18, TypeScript, Vite
AI/ML	DeepSeek API, scikit-learn, pandas, numpy
Data	requests, BeautifulSoup4, feedparser
Database	SQLite (local), Google Sheets API
Monitoring	psutil, custom watchdog
Messaging	python-telegram-bot
WebSocket	Socket.IO
Deployment	Git, GitHub, VPS
📝 License
MIT License - see LICENSE file for details.

🤝 Contributing
Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📞 Contact
GitHub: inksidedigitalteknologi

Project: consciousness-intelligence

🙏 Acknowledgments
Nasdaq API for dividend data

CoinGecko for crypto price data

DeepSeek for AI capabilities

All open-source libraries used

Made with ❤️ by Inkside Digital
## 🏗️ Architecture

### Core Components
