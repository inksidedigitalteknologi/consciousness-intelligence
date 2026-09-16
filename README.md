# 🧠 Inkside Digital - Cognitive Mirror Engine v3.0.0

**The Future of Algorithmic Trading & Dividend Intelligence | 32-Aspek Analysis | AI-Powered Market Intelligence**

---

## 📋 Overview

**Inkside Digital - Cognitive Mirror Engine v3.0.0** is an advanced algorithmic trading and dividend intelligence system.

- 🧠 **Cognitive Computing** — Self-learning AI
- 📊 **32-Aspek Analysis** — Technical + Fundamental + Correlation + Sentiment
- 🎯 **Direction Engine** — Actionable BUY/SELL/WAIT recommendations
- 💰 **Dividend Hunter** — Auto-fetch from Nasdaq
- 📈 **Multi-Timeframe** — 1M, 3M, 6M, 1Y
- 🔮 **Monte Carlo** — 1,000 iterations, 30-day forecast
- 🧬 **Self-Learning** — Brain learns from outcomes
- 🛡️ **Self-Healing** — Watchdog with circuit breaker
- 💾 **Permanent Memory** — 1,400+ items
- 📊 **Decision Logger** — 4,000+ records
- 🎯 **Outcome Tracker** — Win/loss after 1/7/30 days
- ⚙️ **Learning Engine** — Aspect accuracy, weights

---

## 📊 32 Aspects

### Technical (13)

1. RSI - balanced (3,7,14)
2. Trend SMA
3. SMA Cross - threshold 0.5%
4. Volume - signal + ratio
5. Momentum
6. Volatility
7. Support/Resistance
8. Distance to S/R
9. Range 20d
10. EMA 12/26
11. Multi-Timeframe
12. Monte Carlo
13. Market Regime

### Advanced Technical (8)

14. MACD
15. Bollinger Bands
16. ATR
17. Stochastic
18. OBV
19. VWAP
20. Fibonacci
21. Volume Profile

### Fundamental (4)

22. Market Cap
23. 1Y Target Upside
24. 52W Position
25. Dividend Yield

### Correlation (2)

26. Correlation S&P 500
27. Beta

### Sentiment (1)

28. Sentiment

### Advanced (4)

29. Candlestick
30. Seasonality
31. Analyst Rating
32. Elliott Wave

---

## 🎯 Direction Engine

| Score | Direction |
|-------|-----------|
| >= +50 | BUY NOW |
| >= +30 | BUY GRADUALLY |
| -30..+30 | WAIT |
| <= -30 | SELL GRADUALLY |
| <= -50 | SELL NOW |

---

## 🧬 Self-Learning System (4 Phases)

### Fase 1 - Decision Logger

- brain.log_market_decision()
- brain.get_decisions()
- brain.get_decision_stats()

### Fase 2 - Outcome Tracker

- brain.track_outcome()
- brain.evaluate_pending_decisions()
- Cron: scripts/track_outcomes.py

### Fase 3 - Learning Engine

- brain.calculate_aspect_accuracy()
- brain.update_weights()
- brain.get_learned_weights()
- brain.learn_from_outcomes()
- Cron: scripts/learn.py

### Fase 4 - Direction Engine

- brain.get_direction()
- brain.explain_direction()

---

## 🔌 API Endpoints

### Core

| Endpoint | Method |
|----------|--------|
| /api/health | GET |
| /api/status | GET |
| /api/system/metrics | GET |
| /api/diagnostics | GET |

### Market

| Endpoint | Method |
|----------|--------|
| /api/market/quotes | GET |
| /api/market/analyze/symbol | GET |
| /api/predictions | GET |

### AI

| Endpoint | Method |
|----------|--------|
| /api/ai/status | GET |
| /api/ai/ask | POST |

### Knowledge

| Endpoint | Method |
|----------|--------|
| /api/knowledge/search | POST |
| /api/knowledge/add | POST |
| /api/knowledge/all | GET |

### Brain

| Endpoint | Method |
|----------|--------|
| /api/brain/state | GET |
| /api/brain/reflection | GET |

---

## 🚀 Setup

### Backend

cd ~/consciousness-intelligence
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nohup python3 main.py > logs/main.log 2>&1 &

### Frontend

cd frontend
npm install
npm run build
rm -rf /var/www/inkside/*
cp -r dist/* /var/www/inkside/
nginx -t && systemctl reload nginx

### Cron

0 */6 * * * /root/consciousness-intelligence/scripts/backup.sh
0 16 * * * cd /root/consciousness-intelligence && ./venv/bin/python3 scripts/track_outcomes.py
0 17 * * * cd /root/consciousness-intelligence && ./venv/bin/python3 scripts/learn.py

---

## 📊 Module Status

**Health: 100% (54/54 modules active)**

---

## 🛠️ Technologies

| Category | Technology |
|----------|-----------|
| Backend | Python 3.12, Flask 3.0 |
| Frontend | React 19, TypeScript, Vite 8 |
| AI | DeepSeek API |
| Database | SQLite |
| Monitoring | psutil, watchdog |
| Deployment | Git, GitHub, VPS, systemd |

---

## 📝 Changelog

### v3.0.0 (2026-09-16)

- 32 aspects market analysis
- RSI balanced (3,7,14)
- SMA cross threshold 0.5%
- Threshold sempit - Bollinger, Stochastic, ATR
- Correlation align by date
- Target risk/reward 1:2
- Fase 1-4 - Decision Logger, Outcome Tracker, Learning Engine, Direction Engine
- systemd watchdog + log rotation + backup cron
- Rate limiting - 10 endpoints
- Health 100% - 54/54 modules

### v2.0.0 (2026-09-11)

- Initial release

---

## 📞 Contact

- **Server**: 45.41.204.21
- **Project**: /root/consciousness-intelligence
- **GitHub**: https://github.com/inksidedigitalteknologi/consciousness-intelligence

---

## 📄 License

MIT License

---

**Made with love by Inkside Digital**
