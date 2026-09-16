#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# INKSIDE DIGITAL
# COGNITIVE MIRROR ENGINE v1.0.0
# CORE BOT ENGINE
# ============================================================

from __future__ import annotations

import logging
import threading
import time
import json
import os
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import deque, Counter

# ============================================================
# CONFIGURATION
# ============================================================

from config import (
    DEFAULT_PAIRS,
    MAIN_TIMEFRAME,
    SCAN_INTERVAL_SECONDS
)

logger = logging.getLogger(__name__)

# ============================================================
# AI INTEGRATION
# ============================================================

try:
    from core.deepseek import deepseek_ai
    DEEPSEEK_AVAILABLE = True
    DEEPSEEK_ENABLED = deepseek_ai.enabled if hasattr(deepseek_ai, 'enabled') else False
except ImportError:
    DEEPSEEK_AVAILABLE = False
    DEEPSEEK_ENABLED = False
    deepseek_ai = None

logger.info(f"🤖 DeepSeek AI Integration: {'ENABLED' if DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED else 'DISABLED'}")

# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class BotState(Enum):
    INITIALIZING = "INITIALIZING"
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    SCANNING = "SCANNING"
    ANALYZING = "ANALYZING"
    TRADING = "TRADING"
    LEARNING = "LEARNING"
    DEGRADED = "DEGRADED"
    ERROR = "ERROR"
    RECOVERING = "RECOVERING"
    STOPPED = "STOPPED"

class TradingMode(Enum):
    PAPER = "PAPER"
    LIVE = "LIVE"
    HYBRID = "HYBRID"

class RiskLevel(Enum):
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"

class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    WAIT = "WAIT"
    MONITOR = "MONITOR"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"
    EXIT = "EXIT"

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class TradeResult:
    symbol: str
    side: str
    quantity: float
    entry_price: float
    exit_price: float
    pnl: float
    pnl_percentage: float
    fee: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    strategy: str = "default"
    metadata: Dict[str, Any] = field(default_factory=dict)
    ai_enhanced: bool = False
    ai_confidence: float = 0.0

@dataclass
class PerformanceMetrics:
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    total_pnl: float = 0.0
    total_pnl_percentage: float = 0.0
    best_trade: float = 0.0
    worst_trade: float = 0.0
    average_win: float = 0.0
    average_loss: float = 0.0
    profit_factor: float = 0.0
    total_fees: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

# ============================================================
# IMPORTS - WITH FALLBACKS
# ============================================================

try:
    from core.health import set_status as health_set_status, health_monitor
    HEALTH_AVAILABLE = True
except ImportError:
    HEALTH_AVAILABLE = False
    health_set_status = None
    health_monitor = None

def set_status(component: str, status: str) -> None:
    if health_set_status is not None:
        try:
            if hasattr(health_set_status, '__code__'):
                import inspect
                sig = inspect.signature(health_set_status)
                if len(sig.parameters) == 2:
                    health_set_status(component, status)
                elif len(sig.parameters) == 1:
                    health_set_status(f"{component}:{status}")
                else:
                    health_set_status(status)
            else:
                health_set_status(status)
            return
        except Exception as e:
            logger.debug(f"Health set_status error: {e}")
    logger.debug(f"Status: {component} -> {status}")

try:
    from core.brain import Brain, brain
    BRAIN_AVAILABLE = True
except ImportError:
    BRAIN_AVAILABLE = False
    Brain = None
    brain = None

try:
    from core.market_data import (
        KrakenMarketData, kraken_market, exchange,
        get_exchange, get_market_data, TickerData, Candle
    )
    EXCHANGE_AVAILABLE = True
    logger.info("✅ Exchange loaded from market_data")
except ImportError:
    EXCHANGE_AVAILABLE = False
    KrakenMarketData = None
    kraken_market = None
    exchange = None
    get_exchange = None
    get_market_data = None
    TickerData = None
    Candle = None
    logger.debug("Exchange not available")

try:
    from core.scanner import MarketScanner
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False
    MarketScanner = None

try:
    from core.cognitive_scanner import CognitiveMarketScanner
    COGNITIVE_SCANNER_AVAILABLE = True
except ImportError:
    COGNITIVE_SCANNER_AVAILABLE = False
    CognitiveMarketScanner = None

try:
    from core.consciousness import consciousness
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False
    consciousness = None

try:
    from core.learning.engine import learning_engine
    LEARNING_ENGINE_AVAILABLE = True
except ImportError:
    LEARNING_ENGINE_AVAILABLE = False
    learning_engine = None

try:
    from services.notification_service import NotificationService
    NOTIFICATION_AVAILABLE = True
except ImportError:
    NOTIFICATION_AVAILABLE = False
    NotificationService = None

# ============================================================
# TRADING BOT - SUPER COMPREHENSIVE - WITH AI
# ============================================================

class TradingBot:
    """
    Trading Bot Core v5.0.0 - Super Comprehensive Trading Intelligence with AI.
    Integrated with Cognitive Brain, Exchange, Scanner, Consciousness, Learning Engine, and DeepSeek AI.
    """
    
    VERSION = "5.0.0"
    
    def __init__(
        self,
        scanner=None,
        notifications=None,
        brain_instance=None,
        exchange_instance=None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.lock = threading.RLock()
        self.config = config or {}
        
        # Version & Identity
        self.version = self.VERSION
        self.name = "Cognitive Mirror Trading Bot"
        self.identity = {
            "name": self.name,
            "version": self.version,
            "type": "Cognitive Trading Intelligence",
            "created_at": datetime.now().isoformat(),
        }
        
        # AI Status
        self.ai_enabled = DEEPSEEK_AVAILABLE and DEEPSEEK_ENABLED
        
        # Core Components
        self.scanner = scanner
        if self.scanner is None and SCANNER_AVAILABLE:
            try:
                self.scanner = MarketScanner()
            except Exception as e:
                logger.warning(f"Scanner creation failed: {e}")
        
        if self.scanner is None and COGNITIVE_SCANNER_AVAILABLE:
            try:
                self.scanner = CognitiveMarketScanner(
                    consciousness=consciousness if CONSCIOUSNESS_AVAILABLE else None,
                    brain=brain if BRAIN_AVAILABLE else None,
                    learning_engine=learning_engine if LEARNING_ENGINE_AVAILABLE else None
                )
                logger.info("CognitiveMarketScanner initialized")
            except Exception as e:
                logger.warning(f"Cognitive scanner creation failed: {e}")
        
        self.notifications = notifications
        if self.notifications is None and NOTIFICATION_AVAILABLE:
            try:
                self.notifications = NotificationService()
            except Exception as e:
                logger.warning(f"Notification creation failed: {e}")
        
        # Unified AI Brain
        self.brain = brain_instance
        if self.brain is None and BRAIN_AVAILABLE:
            try:
                self.brain = Brain()
            except Exception as e:
                logger.warning(f"Brain creation failed: {e}")
        
        if self.brain is not None:
            logger.info("✅ Cognitive Brain integrated successfully.")
        else:
            logger.warning("⚠️ Running without Cognitive Brain.")
        
        # Exchange Integration
        self.exchange = exchange_instance
        if self.exchange is None and EXCHANGE_AVAILABLE:
            try:
                self.exchange = get_exchange()
                logger.info("✅ Exchange integrated successfully.")
            except Exception as e:
                logger.warning(f"Exchange integration failed: {e}")
        
        if self.exchange is not None:
            try:
                if hasattr(self.exchange, 'test_connection'):
                    if self.exchange.test_connection():
                        logger.info("✅ Exchange connection successful.")
                    else:
                        logger.warning("⚠️ Exchange connection failed - using mock data.")
            except Exception as e:
                logger.warning(f"Exchange connection test failed: {e}")
        else:
            logger.warning("⚠️ Running without exchange - using mock data.")
        
        # Consciousness
        self.consciousness = consciousness
        if CONSCIOUSNESS_AVAILABLE and self.consciousness is not None:
            logger.info("Consciousness integrated successfully.")
        
        # Learning Engine
        self.learning_engine = learning_engine
        if LEARNING_ENGINE_AVAILABLE and self.learning_engine is not None:
            logger.info("Learning Engine integrated successfully.")
        
        # State
        self.state = BotState.INITIALIZING
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.pause_event = threading.Event()
        self.shutdown_event = threading.Event()
        
        self.scan_count = 0
        self.errors = 0
        self.recovery_attempts = 0
        self._stop_requested = False
        
        self.started_at: Optional[str] = None
        self.last_scan_time: Optional[datetime] = None
        self.last_scan_duration: float = 0.0
        self.last_error: Optional[str] = None
        self.last_update: Optional[str] = None
        
        # Trading Configuration
        self.trading_mode = TradingMode.PAPER
        self.risk_level = RiskLevel.MODERATE
        self.market_mode = self.config.get("market_mode", "CRYPTO")
        
        self.current_pairs = list(self.config.get("pairs", DEFAULT_PAIRS))
        self.current_timeframe = self.config.get("timeframe", MAIN_TIMEFRAME)
        self.current_interval = self.config.get("interval", SCAN_INTERVAL_SECONDS)
        
        self.min_confidence = self.config.get("min_confidence", 60.0)
        self.max_positions = self.config.get("max_positions", 5)
        self.max_risk_per_trade = self.config.get("max_risk_per_trade", 2.0)
        self.default_stop_loss = self.config.get("default_stop_loss", 5.0)
        self.default_take_profit = self.config.get("default_take_profit", 10.0)
        self.order_size = self.config.get("order_size", 100.0)
        
        # Balance & Portfolio
        self.initial_balance = self.config.get("balance", 10000.0)
        self.balance = self.initial_balance
        self.portfolio = {
            "cash": self.balance,
            "holdings": {},
            "total_value": self.balance,
            "pnl": 0.0,
            "pnl_percentage": 0.0,
            "initial_balance": self.initial_balance,
        }
        
        # Data Caches
        self.market_data_cache: Dict[str, List[Dict]] = {}
        self.price_cache: Dict[str, float] = {}
        self.last_results: List[Dict] = []
        self.latest_results: List[Dict] = []
        self.signal_snapshot: List[Dict] = []
        self.results: List[Dict] = []
        self.memory: Dict[str, Any] = {}
        
        # AI Cache
        self.ai_analysis_cache: Dict[str, Dict] = {}
        self.ai_insights_cache: Dict[str, List[str]] = {}
        
        # Statistics
        self.total_buy_signals = 0
        self.total_sell_signals = 0
        self.total_hold_signals = 0
        self.total_errors = 0
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.ai_validated_trades = 0
        
        # History
        self.trade_history: List[TradeResult] = []
        self.signal_history: List[Dict] = []
        self.ai_analysis_history: List[Dict] = []
        self.performance_history: List[Dict] = []
        self.daily_pnl: Dict[str, float] = {}
        
        # Brain State
        self.anomaly_status = "NORMAL"
        self.market_forecast = "NEUTRAL"
        self.brain_confidence = 0.0
        self.brain_state: Optional[Dict] = None
        
        # Performance
        self.performance = PerformanceMetrics()
        
        # Callbacks
        self.on_scan_complete: Optional[callable] = None
        self.on_pair_update: Optional[callable] = None
        self.on_signal: Optional[callable] = None
        self.on_status_change: Optional[callable] = None
        self.on_brain_update: Optional[callable] = None
        self.on_trade: Optional[callable] = None
        self.on_error: Optional[callable] = None
        self.on_ai_analysis: Optional[callable] = None
        
        # Initialize
        self._connect_scanner()
        self._initialize_cache()
        self._initialize_exchange_data()
        
        self.state = BotState.IDLE
        
        set_status("core", "ONLINE")
        
        logger.info(
            "TradingBot v%s Cognitive Mirror initialized. Mode: %s, Exchange: %s, AI: %s",
            self.version,
            self.trading_mode.value,
            "ONLINE" if self.exchange is not None else "OFFLINE",
            "ENABLED" if self.ai_enabled else "DISABLED"
        )
        
        if HEALTH_AVAILABLE and health_monitor is not None:
            try:
                if hasattr(health_monitor, 'register'):
                    health_monitor.register("trading_bot")
            except Exception as e:
                logger.debug(f"Health register error: {e}")
    
    # ============================================================
    # EXCHANGE DATA INITIALIZATION
    # ============================================================
    
    def _initialize_exchange_data(self) -> None:
        if self.exchange is None:
            return
        
        try:
            if hasattr(self.exchange, 'get_latest_prices'):
                prices = self.exchange.get_latest_prices(self.current_pairs)
                for pair, price in prices.items():
                    if price is not None:
                        self.price_cache[pair] = price
                        logger.debug(f"Initial price {pair}: ${price:.2f}")
            
            if hasattr(self.exchange, 'get_ohlc'):
                for pair in self.current_pairs[:5]:
                    candles = self.exchange.get_ohlc(pair, self.current_timeframe, 100)
                    if candles:
                        self.market_data_cache[pair] = candles
                        logger.debug(f"Initial OHLC {pair}: {len(candles)} candles")
        
        except Exception as e:
            logger.warning(f"Exchange data initialization failed: {e}")
    
    def get_real_time_price(self, pair: str) -> Optional[float]:
        if self.exchange is None:
            return None
        
        try:
            if hasattr(self.exchange, 'get_ticker'):
                ticker = self.exchange.get_ticker(pair)
                if ticker:
                    price = ticker.price if hasattr(ticker, 'price') else ticker.get('price')
                    if price:
                        self.price_cache[pair] = price
                        return price
            return None
        except Exception as e:
            logger.debug(f"Real-time price error for {pair}: {e}")
            return None
    
    # ============================================================
    # INITIALIZATION HELPERS
    # ============================================================
    
    def _connect_scanner(self) -> None:
        if self.scanner is None:
            return
        
        try:
            if hasattr(self.scanner, "set_callback"):
                self.scanner.set_callback(self.on_scanner_update)
            elif hasattr(self.scanner, "callback"):
                self.scanner.callback = self.on_scanner_update
            logger.info("Scanner callbacks connected.")
        except Exception as e:
            logger.exception(f"Scanner callback error: {e}")
    
    def _initialize_cache(self) -> None:
        for pair in self.current_pairs:
            self.market_data_cache[pair] = []
            self.price_cache[pair] = None
    
    # ============================================================
    # SCANNER LIVE UPDATE
    # ============================================================
    
    def on_scanner_update(self, data: Dict) -> None:
        if not isinstance(data, dict):
            return
        
        with self.lock:
            self.latest_results.append(data)
            if len(self.latest_results) > 100:
                self.latest_results = self.latest_results[-100:]
        
        if self.brain is not None:
            threading.Thread(
                target=self._update_brain_async,
                args=([data]),
                daemon=True
            ).start()
        
        if self.on_pair_update:
            try:
                self.on_pair_update(data)
            except Exception:
                pass
    
    def _update_brain_async(self, data: List[Dict]) -> None:
        try:
            state = self.brain.observe(data)
            self.update_brain(state)
        except Exception as e:
            logger.warning(f"Brain observe failed: {e}")
    
    # ============================================================
    # AI INTEGRATION - STRATEGY GENERATION
    # ============================================================
    
    def generate_strategy_with_ai(
        self,
        pair: str,
        market_data: Dict[str, Any],
        risk_level: str = "moderate",
        timeframe: str = "1h"
    ) -> Dict[str, Any]:
        """Generate trading strategy with AI using DeepSeek."""
        try:
            if not self.ai_enabled:
                return {
                    'status': 'disabled',
                    'message': 'AI is disabled',
                    'pair': pair
                }
            
            context = f"""
Pair: {pair}
Risk Level: {risk_level}
Timeframe: {timeframe}

Market Data:
- Price: {market_data.get('price', 0)}
- 24h Change: {market_data.get('change_24h', 0)}%
- Volume: {market_data.get('volume', 0)}
- High: {market_data.get('high', 0)}
- Low: {market_data.get('low', 0)}
- Trend: {market_data.get('trend', 'NEUTRAL')}
- RSI: {market_data.get('rsi', 0)}
- MACD: {market_data.get('macd', 0)}
- Volatility: {market_data.get('volatility', 0)}
"""
            
            prompt = f"""Kembangkan strategi trading komprehensif untuk {pair}:

1. ENTRY: Kondisi entry spesifik dengan harga target
2. EXIT: Take profit level 1, 2, 3
3. STOP LOSS: Level stop loss dengan rasio risk/reward
4. POSITION SIZING: Ukuran posisi berdasarkan risk level {risk_level}
5. TIMEFRAME: Timeframe terbaik untuk eksekusi
6. RISK MANAGEMENT: Risk management rules
7. CONFIRMATION: Konfirmasi tambahan yang diperlukan
8. CONTINGENCY: Skenario alternatif

Beri strategi yang actionable dan berbasis data.
"""
            
            result = deepseek_ai.ask(
                question=prompt,
                context=context,
                system_prompt="strategist",
                temperature=0.7,
                max_tokens=1024
            )
            
            strategy = self._parse_ai_strategy(result)
            
            from core.knowledge import knowledge
            knowledge.add(
                content=f"AI Strategy for {pair}: {result[:300]}...",
                category="strategy",
                type="ai_strategy",
                tags=["ai", "strategy", pair.replace('/', '_')],
                confidence=75.0,
                importance=0.8,
                metadata={
                    'pair': pair,
                    'risk_level': risk_level,
                    'timeframe': timeframe,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            self.ai_analysis_history.append({
                'type': 'strategy',
                'pair': pair,
                'risk_level': risk_level,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'status': 'success',
                'pair': pair,
                'strategy': result,
                'entry': strategy.get('entry'),
                'take_profit': strategy.get('take_profit'),
                'stop_loss': strategy.get('stop_loss'),
                'risk_reward': strategy.get('risk_reward'),
                'position_size': strategy.get('position_size'),
                'recommendation': strategy.get('recommendation'),
                'risk_level': risk_level,
                'timeframe': timeframe,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AI strategy generation error: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'pair': pair
            }
    
    def _parse_ai_strategy(self, response: str) -> Dict[str, Any]:
        import re
        strategy = {}
        
        entry_match = re.search(r'entry[:\s]+(?:price|level)?[:\s]*([\d.]+)', response, re.IGNORECASE)
        if entry_match:
            strategy['entry'] = float(entry_match.group(1))
        
        tp_matches = re.findall(r'take\s*profit[:\s]+(?:level\s*)?(\d+)?[:\s]*([\d.]+)', response, re.IGNORECASE)
        if tp_matches:
            strategy['take_profit'] = [float(tp[1]) for tp in tp_matches]
        else:
            tp_single = re.search(r'tp[:\s]+([\d.]+)', response, re.IGNORECASE)
            if tp_single:
                strategy['take_profit'] = [float(tp_single.group(1))]
        
        sl_match = re.search(r'stop\s*loss[:\s]+(?:level)?[:\s]*([\d.]+)', response, re.IGNORECASE)
        if sl_match:
            strategy['stop_loss'] = float(sl_match.group(1))
        
        rr_match = re.search(r'risk[/-]?reward[:\s]*([\d.]+)', response, re.IGNORECASE)
        if rr_match:
            strategy['risk_reward'] = float(rr_match.group(1))
        
        size_match = re.search(r'position\s*size[:\s]*([\d.]+)', response, re.IGNORECASE)
        if size_match:
            strategy['position_size'] = float(size_match.group(1))
        
        rec_match = re.search(r'recommendation[:\s]*(.+?)(?:\n|$)', response, re.IGNORECASE)
        if rec_match:
            strategy['recommendation'] = rec_match.group(1).strip()
        
        return strategy
    
    def enhance_trade_with_ai(self, trade: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance trade decision with AI."""
        try:
            if not self.ai_enabled:
                return {
                    **trade,
                    'ai_enhanced': False,
                    'ai_status': 'disabled'
                }
            
            context = f"""
Trade Details:
- Pair: {trade.get('pair', 'Unknown')}
- Side: {trade.get('side', 'BUY')}
- Entry: ${trade.get('entry', 0)}
- Stop Loss: ${trade.get('stop_loss', 0)}
- Take Profit: ${trade.get('take_profit', 0)}
- Position Size: {trade.get('size', 0)}
- Risk/Reward: {trade.get('risk_reward', 0)}
"""
            
            prompt = f"""Analisis dan tingkatkan trade ini:

1. VALIDASI: Apakah trade ini baik? Mengapa?
2. OPTIMASI: Bagaimana bisa dioptimalkan?
3. RISIKO: Apa risiko terbesar?
4. INSIGHT: Insight berharga untuk trade ini
5. ALTERNATIF: Skenario alternatif

Berikan analisis kritis dan actionable.
"""
            
            result = deepseek_ai.ask(
                question=prompt,
                context=context,
                system_prompt="analyst",
                temperature=0.5,
                max_tokens=512
            )
            
            is_good = "good" in result.lower() and "not" not in result.lower()
            
            self.ai_validated_trades += 1
            
            return {
                **trade,
                'ai_enhanced': True,
                'ai_status': 'success',
                'ai_analysis': result,
                'ai_is_good': is_good,
                'ai_confidence': 80 if is_good else 40,
                'ai_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AI trade enhancement error: {e}")
            return {
                **trade,
                'ai_enhanced': False,
                'ai_status': 'error',
                'ai_error': str(e)
            }
    
    def get_ai_insights(self, pair: str) -> List[str]:
        """Get AI insights for a pair."""
        try:
            if not self.ai_enabled:
                return ["AI is disabled"]
            
            cache_key = f"insights_{pair}"
            if cache_key in self.ai_insights_cache:
                return self.ai_insights_cache[cache_key]
            
            prompt = f"Berikan 3 insight trading untuk {pair} berdasarkan market conditions terkini."
            
            result = deepseek_ai.ask(
                question=prompt,
                system_prompt="analyst",
                temperature=0.6,
                max_tokens=256
            )
            
            insights = [line.strip() for line in result.split('\n') if len(line.strip()) > 10]
            insights = insights[:3]
            
            self.ai_insights_cache[cache_key] = insights
            
            return insights
            
        except Exception as e:
            logger.error(f"AI insights error: {e}")
            return ["AI insights unavailable"]
    
    # ============================================================
    # MAIN SCAN CYCLE
    # ============================================================
    
    def run_once(
        self,
        pairs: Optional[List[str]] = None,
        timeframe: Optional[str] = None
    ) -> List[Dict]:
        start_time = time.time()
        
        if pairs is None:
            pairs = self.current_pairs
        
        if timeframe is None:
            timeframe = self.current_timeframe
        
        try:
            self.state = BotState.SCANNING
            
            if self.exchange is not None:
                for pair in pairs:
                    price = self.get_real_time_price(pair)
                    if price:
                        self.price_cache[pair] = price
            
            results = []
            if self.scanner is not None:
                try:
                    results = self.scanner.scan_all(
                        pairs=list(pairs),
                        timeframe=timeframe
                    )
                except Exception as e:
                    logger.warning(f"Scanner error: {e}")
                    results = []
            
            if not isinstance(results, list):
                results = []
            
            if results and self.brain is not None:
                try:
                    threading.Thread(
                        target=self._analyze_with_brain,
                        args=(results,),
                        daemon=True
                    ).start()
                except Exception as e:
                    logger.warning(f"Brain analysis failed: {e}")
            
            with self.lock:
                self.last_results = list(results)
                self.latest_results = list(results)
                self.signal_snapshot = list(results)
                self.results = list(results)
                
                for item in results:
                    if not isinstance(item, dict):
                        continue
                    
                    pair = item.get("pair", item.get("symbol"))
                    if not pair:
                        continue
                    
                    candles = item.get("ohlcv", item.get("candles", []))
                    if candles:
                        self.market_data_cache[pair] = list(candles)
                    
                    price = item.get("price", item.get("close"))
                    if price is not None:
                        self.price_cache[pair] = price
                
                self.scan_count += 1
                self.last_scan_time = datetime.now()
                self.last_scan_duration = time.time() - start_time
                self.last_update = self.last_scan_time.isoformat()
            
            self.process_signals(results)
            self._update_performance()
            self._update_daily_pnl()
            
            if self.on_scan_complete:
                try:
                    self.on_scan_complete(results)
                except Exception:
                    pass
            
            self.state = BotState.RUNNING
            
            logger.debug(
                "Scan complete | Results=%s | %.2fs",
                len(results),
                self.last_scan_duration
            )
            
            return results
            
        except Exception as e:
            self.total_errors += 1
            self.errors += 1
            self.last_error = str(e)
            self.state = BotState.ERROR
            
            logger.exception(f"Scan cycle failed: {e}")
            
            if self.on_error:
                try:
                    self.on_error(e)
                except Exception:
                    pass
            
            return []
    
    def _analyze_with_brain(self, results: List[Dict]) -> None:
        try:
            state = self.brain.observe(results)
            self.update_brain(state)
            
            if self.on_brain_update:
                self.on_brain_update(state)
        except Exception as e:
            logger.warning(f"Brain analysis failed: {e}")
    
    def update_brain(self, state: Dict) -> None:
        if not isinstance(state, dict):
            return
        
        try:
            self.anomaly_status = state.get("anomaly", self.anomaly_status)
            self.market_forecast = state.get("forecast", self.market_forecast)
            self.brain_confidence = state.get("confidence", self.brain_confidence)
            self.brain_state = state
            self.memory.update(state)
        except Exception as e:
            logger.warning(f"Brain state update error: {e}")
    
    # ============================================================
    # SIGNAL PROCESSING
    # ============================================================
    
    def process_signals(self, results: List[Dict]) -> None:
        buy = 0
        sell = 0
        hold = 0
        
        try:
            for item in results:
                if not isinstance(item, dict):
                    continue
                
                signal = item.get("signal", "HOLD")
                
                if isinstance(signal, dict):
                    action = str(signal.get("signal", "HOLD")).upper()
                    confidence = signal.get("confidence", 0.0)
                else:
                    action = str(signal).upper()
                    confidence = item.get("confidence", 0.0)
                
                if action in ["BUY", "STRONG_BUY"]:
                    buy += 1
                elif action in ["SELL", "STRONG_SELL"]:
                    sell += 1
                else:
                    hold += 1
                
                signal_data = {
                    "timestamp": datetime.now().isoformat(),
                    "pair": item.get("pair", item.get("symbol")),
                    "signal": action,
                    "confidence": confidence,
                    "price": item.get("price", item.get("close")),
                    "ai_enhanced": item.get("ai_validated", False),
                }
                self.signal_history.append(signal_data)
                if len(self.signal_history) > 1000:
                    self.signal_history = self.signal_history[-1000:]
                
                if self.on_signal:
                    try:
                        self.on_signal(item)
                    except Exception:
                        pass
                
                if action in ["BUY", "SELL", "STRONG_BUY", "STRONG_SELL"]:
                    self.send_notification(item)
            
            self.total_buy_signals += buy
            self.total_sell_signals += sell
            self.total_hold_signals += hold
            
        except Exception as e:
            logger.exception(f"Signal processing error: {e}")
    
    def send_notification(self, data: Dict) -> None:
        if self.notifications is None:
            return
        
        try:
            if hasattr(self.notifications, "send_signal"):
                self.notifications.send_signal(data)
            elif hasattr(self.notifications, "send"):
                self.notifications.send(data)
        except Exception as e:
            logger.warning(f"Notification error: {e}")
    
    # ============================================================
    # TRADING EXECUTION
    # ============================================================
    
    def execute_trade(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        strategy: str = "default",
        use_ai: bool = True
    ) -> Optional[TradeResult]:
        try:
            if self.trading_mode == TradingMode.PAPER:
                result = self._execute_paper_trade(symbol, side, quantity, price, strategy)
                if result and use_ai and self.ai_enabled:
                    result = self._enhance_trade_result_with_ai(result)
                return result
            else:
                return self._execute_paper_trade(symbol, side, quantity, price, strategy)
        except Exception as e:
            logger.exception(f"Trade execution failed: {e}")
            return None
    
    def _execute_paper_trade(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        strategy: str
    ) -> Optional[TradeResult]:
        if side == "BUY":
            cost = quantity * price
            if cost > self.portfolio["cash"]:
                logger.warning(f"Insufficient balance for {symbol}: {cost:.2f} > {self.portfolio['cash']:.2f}")
                return None
            self.portfolio["cash"] -= cost
            self.portfolio["holdings"][symbol] = self.portfolio["holdings"].get(symbol, 0) + quantity
            
        elif side == "SELL":
            if symbol not in self.portfolio["holdings"] or self.portfolio["holdings"][symbol] < quantity:
                logger.warning(f"Insufficient holdings for {symbol}")
                return None
            revenue = quantity * price
            self.portfolio["cash"] += revenue
            self.portfolio["holdings"][symbol] -= quantity
            if self.portfolio["holdings"][symbol] <= 0:
                del self.portfolio["holdings"][symbol]
        
        self._update_portfolio()
        
        trade = TradeResult(
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=price if side == "BUY" else 0,
            exit_price=price if side == "SELL" else 0,
            pnl=0,
            pnl_percentage=0,
            fee=price * quantity * 0.001,
            strategy=strategy,
            ai_enhanced=False,
            ai_confidence=0.0
        )
        
        self.trade_history.append(trade)
        self.total_trades += 1
        
        if self.on_trade:
            try:
                self.on_trade(trade)
            except Exception:
                pass
        
        logger.info(f"PAPER {side}: {quantity:.4f} {symbol} @ {price:.2f}")
        return trade
    
    def _enhance_trade_result_with_ai(self, trade: TradeResult) -> TradeResult:
        try:
            if not self.ai_enabled:
                return trade
            
            prompt = f"Analisis trade ini: {trade.symbol} {trade.side} {trade.quantity} @ {trade.entry_price}"
            result = deepseek_ai.ask(
                question=prompt,
                system_prompt="analyst",
                temperature=0.3,
                max_tokens=200
            )
            
            trade.ai_enhanced = True
            trade.ai_confidence = 75.0
            trade.metadata['ai_analysis'] = result
            
            return trade
            
        except Exception as e:
            logger.warning(f"AI trade enhancement failed: {e}")
            return trade
    
    def _update_portfolio(self) -> None:
        total_value = self.portfolio["cash"]
        for symbol, quantity in self.portfolio["holdings"].items():
            price = self.price_cache.get(symbol)
            if price:
                total_value += quantity * price
        
        self.portfolio["total_value"] = total_value
        self.portfolio["pnl"] = total_value - self.initial_balance
        self.portfolio["pnl_percentage"] = (self.portfolio["pnl"] / self.initial_balance) * 100
    
    def _update_performance(self) -> None:
        total = self.total_trades
        if total > 0:
            self.performance.total_trades = total
            self.performance.winning_trades = self.winning_trades
            self.performance.losing_trades = self.losing_trades
            self.performance.win_rate = (self.winning_trades / total) * 100
            self.performance.total_pnl = self.portfolio["pnl"]
            self.performance.total_pnl_percentage = self.portfolio["pnl_percentage"]
    
    def _update_daily_pnl(self) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        self.daily_pnl[today] = self.portfolio["pnl"]
        if len(self.daily_pnl) > 365:
            oldest = sorted(self.daily_pnl.keys())[0]
            del self.daily_pnl[oldest]
    
    # ============================================================
    # BOT CONTROL
    # ============================================================
    
    def start(self) -> bool:
        if self.running:
            logger.warning("Bot already running.")
            return False
        
        self.running = True
        self._stop_requested = False
        self.started_at = datetime.now().isoformat()
        self.shutdown_event.clear()
        self.pause_event.clear()
        self.state = BotState.RUNNING
        
        if self.brain is not None:
            try:
                threading.Thread(
                    target=self._start_brain_safe,
                    daemon=True
                ).start()
            except Exception as e:
                logger.warning(f"Brain start failed: {e}")
        
        self.thread = threading.Thread(
            target=self._worker_loop,
            daemon=True,
            name="TradingBotWorker"
        )
        self.thread.start()
        
        set_status("core", "RUNNING")
        
        logger.info("TradingBot started.")
        
        if self.on_status_change:
            try:
                self.on_status_change("RUNNING")
            except Exception:
                pass
        
        return True
    
    def _start_brain_safe(self) -> None:
        try:
            if hasattr(self.brain, 'start'):
                self.brain.start()
        except Exception as e:
            logger.warning(f"Brain start error: {e}")
    
    def stop(self) -> bool:
        if not self.running:
            return False
        
        logger.info("Stopping TradingBot...")
        
        self._stop_requested = True
        self.running = False
        self.shutdown_event.set()
        self.state = BotState.STOPPED
        
        if self.brain is not None:
            try:
                threading.Thread(
                    target=self._stop_brain_safe,
                    daemon=True
                ).start()
            except Exception as e:
                logger.warning(f"Brain stop failed: {e}")
        
        if self.thread:
            try:
                self.thread.join(timeout=3.0)
                if self.thread.is_alive():
                    logger.warning("Worker thread still alive, forcing stop.")
            except Exception:
                pass
            self.thread = None
        
        set_status("core", "STOPPED")
        
        logger.info("TradingBot stopped.")
        
        if self.on_status_change:
            try:
                self.on_status_change("STOPPED")
            except Exception:
                pass
        
        return True
    
    def _stop_brain_safe(self) -> None:
        try:
            if hasattr(self.brain, 'stop'):
                self.brain.stop()
        except Exception as e:
            logger.warning(f"Brain stop error: {e}")
    
    def pause(self) -> bool:
        if not self.running:
            return False
        
        self.pause_event.set()
        self.state = BotState.PAUSED
        logger.info("TradingBot paused.")
        return True
    
    def resume(self) -> bool:
        if not self.running:
            return False
        
        self.pause_event.clear()
        self.state = BotState.RUNNING
        logger.info("TradingBot resumed.")
        return True
    
    # ============================================================
    # WORKER LOOP
    # ============================================================
    
    def _worker_loop(self) -> None:
        logger.info("Worker thread started.")
        
        interval = max(1, int(self.current_interval))
        
        while self.running and not self.shutdown_event.is_set():
            try:
                if self.pause_event.is_set():
                    time.sleep(1)
                    continue
                
                results = self.run_once()
                
                if results and self.learning_engine is not None:
                    threading.Thread(
                        target=self._learn_safe,
                        args=(results,),
                        daemon=True
                    ).start()
                
                # AI Insights refresh
                if self.ai_enabled and len(results) > 0:
                    threading.Thread(
                        target=self._refresh_ai_insights,
                        args=(results,),
                        daemon=True
                    ).start()
                
            except Exception as e:
                self.total_errors += 1
                self.errors += 1
                self.last_error = str(e)
                logger.exception(f"Worker error: {e}")
                
                if self.errors > 10:
                    self._attempt_recovery()
            
            for _ in range(interval):
                if not self.running or self.shutdown_event.is_set():
                    break
                time.sleep(1)
        
        logger.info("Worker thread stopped.")
    
    def _learn_safe(self, results: List[Dict]) -> None:
        try:
            if self.learning_engine is not None:
                if hasattr(self.learning_engine, 'learn'):
                    self.learning_engine.learn({"results": results})
        except Exception:
            pass
    
    def _refresh_ai_insights(self, results: List[Dict]) -> None:
        try:
            for item in results[:3]:
                pair = item.get('pair')
                if pair:
                    self.get_ai_insights(pair)
        except Exception:
            pass
    
    def _attempt_recovery(self) -> bool:
        self.recovery_attempts += 1
        self.state = BotState.RECOVERING
        
        logger.warning(f"Recovery attempt #{self.recovery_attempts} started...")
        
        try:
            if self.errors > 20:
                self.errors = 0
            
            if self.scanner is None and SCANNER_AVAILABLE:
                self.scanner = MarketScanner()
                self._connect_scanner()
            
            if self.exchange is not None and EXCHANGE_AVAILABLE:
                try:
                    if hasattr(self.exchange, 'test_connection'):
                        if self.exchange.test_connection():
                            logger.info("Exchange reconnected.")
                except Exception:
                    pass
            
            self.last_error = None
            self.state = BotState.RUNNING
            
            logger.info("Recovery completed successfully.")
            return True
            
        except Exception as e:
            logger.exception(f"Recovery failed: {e}")
            self.state = BotState.ERROR
            return False
    
    # ============================================================
    # DATA ACCESS
    # ============================================================
    
    def get_results(self) -> List[Dict]:
        with self.lock:
            return list(self.last_results)
    
    def get_snapshot(self) -> List[Dict]:
        with self.lock:
            return list(self.signal_snapshot)
    
    def get_market_data(self, pair: str) -> List[Dict]:
        with self.lock:
            return list(self.market_data_cache.get(pair, []))
    
    def get_price(self, pair: str) -> Optional[float]:
        if self.exchange is not None:
            price = self.get_real_time_price(pair)
            if price is not None:
                return price
        
        with self.lock:
            return self.price_cache.get(pair)
    
    def get_trade_history(self, limit: int = 50) -> List[TradeResult]:
        return self.trade_history[-limit:] if self.trade_history else []
    
    def get_signal_history(self, limit: int = 50) -> List[Dict]:
        return self.signal_history[-limit:] if self.signal_history else []
    
    def get_ai_history(self, limit: int = 20) -> List[Dict]:
        return self.ai_analysis_history[-limit:] if self.ai_analysis_history else []
    
    # ============================================================
    # STATUS & HEALTH
    # ============================================================
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "state": self.state.value,
            "running": self.running,
            "mode": self.market_mode,
            "trading_mode": self.trading_mode.value,
            "risk_level": self.risk_level.value,
            "brain": self.brain is not None,
            "exchange": self.exchange is not None,
            "scanner": self.scanner is not None,
            "consciousness": CONSCIOUSNESS_AVAILABLE,
            "learning_engine": LEARNING_ENGINE_AVAILABLE,
            "ai_enabled": self.ai_enabled,
            "ai_validated_trades": self.ai_validated_trades,
            "anomaly": self.anomaly_status,
            "forecast": self.market_forecast,
            "confidence": self.brain_confidence,
            "scan_count": self.scan_count,
            "results": len(self.last_results),
            "errors": self.total_errors,
            "recovery_attempts": self.recovery_attempts,
            "started_at": self.started_at,
            "last_update": self.last_update,
            "performance": {
                "total_trades": self.total_trades,
                "winning_trades": self.winning_trades,
                "losing_trades": self.losing_trades,
                "win_rate": (self.winning_trades / max(1, self.total_trades)) * 100,
                "total_pnl": self.portfolio["pnl"],
                "total_pnl_percentage": self.portfolio["pnl_percentage"],
            },
            "portfolio": {
                "cash": self.portfolio["cash"],
                "holdings": len(self.portfolio["holdings"]),
                "total_value": self.portfolio["total_value"],
                "pnl": self.portfolio["pnl"],
                "pnl_percentage": self.portfolio["pnl_percentage"],
            },
            "timestamp": datetime.now().isoformat(),
        }
    
    def health_check(self) -> Dict[str, Any]:
        exchange_status = "OFFLINE"
        if self.exchange is not None:
            try:
                if hasattr(self.exchange, 'health_check'):
                    exchange_status = self.exchange.health_check().get("status", "UNKNOWN")
                elif hasattr(self.exchange, 'test_connection'):
                    exchange_status = "ONLINE" if self.exchange.test_connection() else "OFFLINE"
            except Exception:
                exchange_status = "ERROR"
        
        return {
            "status": "ONLINE" if self.running else "OFFLINE",
            "state": self.state.value,
            "scanner": self.scanner is not None,
            "brain": self.brain is not None,
            "exchange": exchange_status,
            "consciousness": CONSCIOUSNESS_AVAILABLE,
            "learning_engine": LEARNING_ENGINE_AVAILABLE,
            "ai": "ONLINE" if self.ai_enabled else "OFFLINE",
            "cache_size": len(self.market_data_cache),
            "results": len(self.last_results),
            "errors": self.total_errors,
            "recovery_attempts": self.recovery_attempts,
            "last_error": self.last_error,
            "timestamp": datetime.now().isoformat(),
        }
    
    def get_ai_status(self) -> Dict[str, Any]:
        return {
            'ai_enabled': self.ai_enabled,
            'ai_available': DEEPSEEK_AVAILABLE,
            'ai_model': deepseek_ai.model if DEEPSEEK_AVAILABLE else None,
            'ai_validated_trades': self.ai_validated_trades,
            'total_trades': self.total_trades,
            'validation_ratio': round(self.ai_validated_trades / max(1, self.total_trades) * 100, 2),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_mobile_snapshot(self) -> Dict[str, Any]:
        try:
            signals = self.get_snapshot()
            
            buy = sum(1 for s in signals if s.get("signal") in ["BUY", "STRONG_BUY"])
            sell = sum(1 for s in signals if s.get("signal") in ["SELL", "STRONG_SELL"])
            hold = len(signals) - buy - sell
            
            return {
                "bot": {
                    "name": "INKSIDE DIGITAL",
                    "version": self.version,
                    "status": "RUNNING" if self.running else "STOPPED",
                    "state": self.state.value,
                    "ai": "ON" if self.ai_enabled else "OFF",
                },
                "market": {
                    "mode": self.market_mode,
                    "trading_mode": self.trading_mode.value,
                    "pairs": len(self.current_pairs),
                    "exchange": self.exchange is not None,
                },
                "signals": {
                    "total": len(signals),
                    "buy": buy,
                    "sell": sell,
                    "hold": hold,
                },
                "brain": {
                    "anomaly": self.anomaly_status,
                    "forecast": self.market_forecast,
                    "confidence": self.brain_confidence,
                },
                "performance": {
                    "total_trades": self.total_trades,
                    "win_rate": (self.winning_trades / max(1, self.total_trades)) * 100,
                    "pnl": self.portfolio["pnl"],
                    "pnl_percentage": self.portfolio["pnl_percentage"],
                },
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.exception(f"Mobile snapshot error: {e}")
            return {"error": str(e)}
    
    # ============================================================
    # CLEAR & SHUTDOWN
    # ============================================================
    
    def clear_results(self) -> None:
        with self.lock:
            self.last_results.clear()
            self.latest_results.clear()
            self.signal_snapshot.clear()
            self.results.clear()
            self.signal_history.clear()
            self.trade_history.clear()
            self.ai_analysis_history.clear()
            self.ai_insights_cache.clear()
            self.ai_analysis_cache.clear()
            self.performance_history.clear()
        
        logger.info("Results cleared.")
    
    def shutdown(self) -> bool:
        try:
            self.stop()
            self.clear_results()
            self._save_state()
            logger.info("TradingBot shutdown completed.")
            return True
        except Exception as e:
            logger.exception(f"Shutdown error: {e}")
            return False
    
    def _save_state(self) -> None:
        try:
            state_file = self.config.get("state_file", "database/bot_state.json")
            
            portfolio_safe = {
                "cash": float(self.portfolio.get("cash", 0)),
                "holdings": {},
                "total_value": float(self.portfolio.get("total_value", 0)),
                "pnl": float(self.portfolio.get("pnl", 0)),
                "pnl_percentage": float(self.portfolio.get("pnl_percentage", 0)),
                "initial_balance": float(self.portfolio.get("initial_balance", 0)),
            }
            
            for symbol, quantity in self.portfolio.get("holdings", {}).items():
                if isinstance(symbol, (int, float, bool)):
                    symbol = str(symbol)
                portfolio_safe["holdings"][str(symbol)] = float(quantity) if quantity else 0
            
            state_data = {
                "version": self.version,
                "portfolio": portfolio_safe,
                "total_trades": int(self.total_trades),
                "scan_count": int(self.scan_count),
                "exchange_available": self.exchange is not None,
                "ai_enabled": self.ai_enabled,
                "ai_validated_trades": self.ai_validated_trades,
                "timestamp": datetime.now().isoformat(),
            }
            
            os.makedirs(os.path.dirname(state_file), exist_ok=True)
            
            with open(state_file, 'w') as f:
                json.dump(state_data, f, indent=2, default=str)
            
            logger.debug("State saved to %s", state_file)
        except Exception as e:
            logger.warning(f"State save failed: {e}")

# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

BotEngine = TradingBot
TradingEngine = TradingBot

__all__ = [
    "TradingBot",
    "BotEngine",
    "TradingEngine",
    "BotState",
    "TradingMode",
    "RiskLevel",
    "SignalType",
    "TradeResult",
    "PerformanceMetrics",
    "set_status",
]
