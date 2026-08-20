#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# INKSIDE DIGITAL
# COGNITIVE MIRROR ENGINE v4.4.1
# CORE BOT ENGINE - SUPER COMPREHENSIVE - FIXED
# ============================================================

from __future__ import annotations

import logging
import threading
import time
import json
import os
import random  # <-- FIX: Untuk mock data
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field, asdict
from enum import Enum

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
# ENUMS & CONSTANTS
# ============================================================

class BotState(Enum):
    """Bot operational states."""
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
    """Trading modes."""
    PAPER = "PAPER"
    LIVE = "LIVE"
    HYBRID = "HYBRID"


class RiskLevel(Enum):
    """Risk levels."""
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"


class SignalType(Enum):
    """Signal types."""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    WAIT = "WAIT"
    MONITOR = "MONITOR"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class TradeResult:
    """Trade result data."""
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


@dataclass
class PerformanceMetrics:
    """Performance metrics."""
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

# Health Monitor
try:
    from core.health import set_status as health_set_status, health_monitor
    HEALTH_AVAILABLE = True
except ImportError:
    HEALTH_AVAILABLE = False
    health_set_status = None
    health_monitor = None

# ============================================================
# FIX: set_status wrapper untuk kompatibilitas
# ============================================================

def set_status(component: str, status: str) -> None:
    """
    Safe wrapper untuk set_status dengan kompatibilitas.
    
    Args:
        component: Nama komponen (core, gui, learning, dll)
        status: Status (ONLINE, RUNNING, STOPPED, dll)
    """
    # Coba gunakan health_set_status dari core
    if health_set_status is not None:
        try:
            # Coba dengan 2 argumen
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
    
    # Fallback: log saja
    logger.debug(f"Status: {component} -> {status}")

# Brain
try:
    from core.brain import Brain, brain
    BRAIN_AVAILABLE = True
except ImportError:
    BRAIN_AVAILABLE = False
    Brain = None
    brain = None

# ============================================================
# FIX: EXCHANGE IMPORT (CRITICAL)
# ============================================================

try:
    from core.market_data import (
        KrakenMarketData,
        kraken_market,
        exchange,
        get_exchange,
        get_market_data,
        TickerData,
        Candle,
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

# Scanner
try:
    from core.scanner import MarketScanner
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False
    MarketScanner = None

# Cognitive Scanner
try:
    from core.cognitive_scanner import CognitiveMarketScanner
    COGNITIVE_SCANNER_AVAILABLE = True
except ImportError:
    COGNITIVE_SCANNER_AVAILABLE = False
    CognitiveMarketScanner = None

# Consciousness
try:
    from core.consciousness import consciousness
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False
    consciousness = None

# Learning Engine
try:
    from core.learning.engine import learning_engine
    LEARNING_ENGINE_AVAILABLE = True
except ImportError:
    LEARNING_ENGINE_AVAILABLE = False
    learning_engine = None

# Notification
try:
    from services.notification_service import NotificationService
    NOTIFICATION_AVAILABLE = True
except ImportError:
    NOTIFICATION_AVAILABLE = False
    NotificationService = None


# ============================================================
# TRADING BOT - SUPER COMPREHENSIVE - FIXED
# ============================================================

class TradingBot:
    """
    Trading Bot Core v4.4.1 - Super Comprehensive Trading Intelligence - FIXED.
    
    Features:
    - Integrated with Cognitive Brain
    - Exchange integration (Kraken)
    - Real-time market data
    - Paper trading
    - Auto-recovery
    - Performance tracking
    """
    
    def __init__(
        self,
        scanner=None,
        notifications=None,
        brain_instance=None,
        exchange_instance=None,  # <-- NEW: Exchange instance
        config: Optional[Dict[str, Any]] = None
    ):
        # ====================================================
        # LOCK & CONFIG
        # ====================================================
        
        self.lock = threading.RLock()
        self.config = config or {}
        
        # ====================================================
        # VERSION & IDENTITY
        # ====================================================
        
        self.version = "4.4.1"
        self.name = "Cognitive Mirror Trading Bot"
        self.identity = {
            "name": self.name,
            "version": self.version,
            "type": "Cognitive Trading Intelligence",
            "created_at": datetime.now().isoformat(),
        }
        
        # ====================================================
        # CORE ENGINE
        # ====================================================
        
        self.scanner = scanner
        if self.scanner is None and SCANNER_AVAILABLE:
            try:
                self.scanner = MarketScanner()
            except Exception as e:
                logger.warning(f"Scanner creation failed: {e}")
        
        # Try cognitive scanner if available
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
        
        # ====================================================
        # UNIFIED AI BRAIN
        # ====================================================
        
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
        
        # ====================================================
        # EXCHANGE INTEGRATION (NEW)
        # ====================================================
        
        self.exchange = exchange_instance
        if self.exchange is None and EXCHANGE_AVAILABLE:
            try:
                self.exchange = get_exchange()
                logger.info("✅ Exchange integrated successfully.")
            except Exception as e:
                logger.warning(f"Exchange integration failed: {e}")
        
        if self.exchange is not None:
            # Test connection
            try:
                if hasattr(self.exchange, 'test_connection'):
                    if self.exchange.test_connection():
                        logger.info("✅ Kraken connection successful.")
                    else:
                        logger.warning("⚠️ Kraken connection failed - using mock data.")
            except Exception as e:
                logger.warning(f"Exchange connection test failed: {e}")
        else:
            logger.warning("⚠️ Running without exchange - using mock data.")
        
        # ====================================================
        # CONSCIOUSNESS
        # ====================================================
        
        self.consciousness = consciousness
        if CONSCIOUSNESS_AVAILABLE and self.consciousness is not None:
            logger.info("Consciousness integrated successfully.")
        
        # ====================================================
        # LEARNING ENGINE
        # ====================================================
        
        self.learning_engine = learning_engine
        if LEARNING_ENGINE_AVAILABLE and self.learning_engine is not None:
            logger.info("Learning Engine integrated successfully.")
        
        # ====================================================
        # STATE
        # ====================================================
        
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
        
        # ====================================================
        # TRADING CONFIGURATION
        # ====================================================
        
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
        
        # ====================================================
        # BALANCE & PORTFOLIO
        # ====================================================
        
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
        
        # ====================================================
        # DATA CACHES
        # ====================================================
        
        self.market_data_cache: Dict[str, List[Dict]] = {}
        self.price_cache: Dict[str, float] = {}
        self.last_results: List[Dict] = []
        self.latest_results: List[Dict] = []
        self.signal_snapshot: List[Dict] = []
        self.results: List[Dict] = []
        self.memory: Dict[str, Any] = {}
        
        # ====================================================
        # STATISTICS
        # ====================================================
        
        self.total_buy_signals = 0
        self.total_sell_signals = 0
        self.total_hold_signals = 0
        self.total_errors = 0
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        
        self.trade_history: List[TradeResult] = []
        self.signal_history: List[Dict] = []
        
        # ====================================================
        # BRAIN STATE
        # ====================================================
        
        self.anomaly_status = "NORMAL"
        self.market_forecast = "NEUTRAL"
        self.brain_confidence = 0.0
        self.brain_state: Optional[Dict] = None
        
        # ====================================================
        # PERFORMANCE
        # ====================================================
        
        self.performance = PerformanceMetrics()
        self.performance_history: List[Dict] = []
        self.daily_pnl: Dict[str, float] = {}
        
        # ====================================================
        # CALLBACKS
        # ====================================================
        
        self.on_scan_complete: Optional[callable] = None
        self.on_pair_update: Optional[callable] = None
        self.on_signal: Optional[callable] = None
        self.on_status_change: Optional[callable] = None
        self.on_brain_update: Optional[callable] = None
        self.on_trade: Optional[callable] = None
        self.on_error: Optional[callable] = None
        
        # ====================================================
        # INITIALIZE
        # ====================================================
        
        self._connect_scanner()
        self._initialize_cache()
        
        # Initialize exchange data
        self._initialize_exchange_data()
        
        self.state = BotState.IDLE
        
        # ============================================================
        # FIX: Safe set_status dengan 2 argumen (component, status)
        # ============================================================
        
        try:
            set_status("core", "ONLINE")
        except Exception as e:
            logger.debug(f"Set status error: {e}")
        
        logger.info(
            "TradingBot v%s Cognitive Mirror initialized. Mode: %s, Exchange: %s",
            self.version,
            self.trading_mode.value,
            "ONLINE" if self.exchange is not None else "OFFLINE"
        )
        
        # Register to health monitor
        if HEALTH_AVAILABLE and health_monitor is not None:
            try:
                if hasattr(health_monitor, 'register'):
                    health_monitor.register("trading_bot")
            except Exception as e:
                logger.debug(f"Health register error: {e}")
    
    # ========================================================
    # EXCHANGE DATA INITIALIZATION
    # ========================================================
    
    def _initialize_exchange_data(self) -> None:
        """Initialize exchange data for all pairs."""
        if self.exchange is None:
            return
        
        try:
            # Get latest prices for all pairs
            if hasattr(self.exchange, 'get_latest_prices'):
                prices = self.exchange.get_latest_prices(self.current_pairs)
                for pair, price in prices.items():
                    if price is not None:
                        self.price_cache[pair] = price
                        logger.debug(f"Initial price {pair}: ${price:.2f}")
            
            # Get OHLC data for all pairs
            if hasattr(self.exchange, 'get_ohlc'):
                for pair in self.current_pairs[:5]:  # Limit initial load
                    candles = self.exchange.get_ohlc(pair, self.current_timeframe, 100)
                    if candles:
                        self.market_data_cache[pair] = candles
                        logger.debug(f"Initial OHLC {pair}: {len(candles)} candles")
        
        except Exception as e:
            logger.warning(f"Exchange data initialization failed: {e}")
    
    # ========================================================
    # GET REAL-TIME PRICE FROM EXCHANGE
    # ========================================================
    
    def get_real_time_price(self, pair: str) -> Optional[float]:
        """Get real-time price from exchange."""
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
    
    # ========================================================
    # INITIALIZATION HELPERS
    # ========================================================
    
    def _connect_scanner(self) -> None:
        """Connect scanner callbacks."""
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
        """Initialize market data cache."""
        for pair in self.current_pairs:
            self.market_data_cache[pair] = []
            self.price_cache[pair] = None
    
    # ========================================================
    # SCANNER LIVE UPDATE
    # ========================================================
    
    def on_scanner_update(self, data: Dict) -> None:
        """Handle live scanner updates."""
        if not isinstance(data, dict):
            return
        
        with self.lock:
            self.latest_results.append(data)
            if len(self.latest_results) > 100:
                self.latest_results = self.latest_results[-100:]
        
        # FIX: Update brain di background thread
        if self.brain is not None:
            threading.Thread(
                target=self._update_brain_async,
                args=([data]),
                daemon=True
            ).start()
        
        # Pair update callback
        if self.on_pair_update:
            try:
                self.on_pair_update(data)
            except Exception:
                pass
    
    def _update_brain_async(self, data: List[Dict]) -> None:
        """Update brain in background thread."""
        try:
            state = self.brain.observe(data)
            self.update_brain(state)
        except Exception as e:
            logger.warning(f"Brain observe failed: {e}")
    
    # ========================================================
    # MAIN SCAN CYCLE - FIXED
    # ========================================================
    
    def run_once(
        self,
        pairs: Optional[List[str]] = None,
        timeframe: Optional[str] = None
    ) -> List[Dict]:
        """Run one complete scan cycle."""
        start_time = time.time()
        
        if pairs is None:
            pairs = self.current_pairs
        
        if timeframe is None:
            timeframe = self.current_timeframe
        
        try:
            self.state = BotState.SCANNING
            
            # ============================================
            # UPDATE REAL-TIME PRICES FROM EXCHANGE
            # ============================================
            
            if self.exchange is not None:
                for pair in pairs:
                    price = self.get_real_time_price(pair)
                    if price:
                        self.price_cache[pair] = price
            
            # ============================================
            # MARKET SCAN
            # ============================================
            
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
            
            # ============================================
            # BRAIN ANALYSIS - FIXED: Pakai thread
            # ============================================
            
            if results and self.brain is not None:
                try:
                    threading.Thread(
                        target=self._analyze_with_brain,
                        args=(results,),
                        daemon=True
                    ).start()
                except Exception as e:
                    logger.warning(f"Brain analysis failed: {e}")
            
            # ============================================
            # SAVE SNAPSHOT
            # ============================================
            
            with self.lock:
                self.last_results = list(results)
                self.latest_results = list(results)
                self.signal_snapshot = list(results)
                self.results = list(results)
                
                # Cache market data
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
            
            # ============================================
            # PROCESS SIGNALS
            # ============================================
            
            self.process_signals(results)
            
            # ============================================
            # UPDATE PERFORMANCE
            # ============================================
            
            self._update_performance()
            
            # ============================================
            # CALLBACK
            # ============================================
            
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
        """Analyze results with brain in background."""
        try:
            state = self.brain.observe(results)
            self.update_brain(state)
            
            if self.on_brain_update:
                self.on_brain_update(state)
        except Exception as e:
            logger.warning(f"Brain analysis failed: {e}")
    
    # ========================================================
    # BRAIN STATE UPDATE
    # ========================================================
    
    def update_brain(self, state: Dict) -> None:
        """Update brain state."""
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
    
    # ========================================================
    # SIGNAL PROCESSING
    # ========================================================
    
    def process_signals(self, results: List[Dict]) -> None:
        """Process signals from scan results."""
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
                
                # Store signal
                signal_data = {
                    "timestamp": datetime.now().isoformat(),
                    "pair": item.get("pair", item.get("symbol")),
                    "signal": action,
                    "confidence": confidence,
                    "price": item.get("price", item.get("close")),
                }
                self.signal_history.append(signal_data)
                if len(self.signal_history) > 1000:
                    self.signal_history = self.signal_history[-1000:]
                
                # GUI callback
                if self.on_signal:
                    try:
                        self.on_signal(item)
                    except Exception:
                        pass
                
                # Notification
                if action in ["BUY", "SELL", "STRONG_BUY", "STRONG_SELL"]:
                    self.send_notification(item)
            
            self.total_buy_signals += buy
            self.total_sell_signals += sell
            self.total_hold_signals += hold
            
        except Exception as e:
            logger.exception(f"Signal processing error: {e}")
    
    # ========================================================
    # NOTIFICATION
    # ========================================================
    
    def send_notification(self, data: Dict) -> None:
        """Send notification."""
        if self.notifications is None:
            return
        
        try:
            if hasattr(self.notifications, "send_signal"):
                self.notifications.send_signal(data)
            elif hasattr(self.notifications, "send"):
                self.notifications.send(data)
        except Exception as e:
            logger.warning(f"Notification error: {e}")
    
    # ========================================================
    # TRADING EXECUTION
    # ========================================================
    
    def execute_trade(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        strategy: str = "default"
    ) -> Optional[TradeResult]:
        """Execute a trade."""
        try:
            if self.trading_mode == TradingMode.PAPER:
                return self._execute_paper_trade(symbol, side, quantity, price, strategy)
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
        """Execute paper trade."""
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
    
    def _update_portfolio(self) -> None:
        """Update portfolio value."""
        total_value = self.portfolio["cash"]
        for symbol, quantity in self.portfolio["holdings"].items():
            price = self.price_cache.get(symbol)
            if price:
                total_value += quantity * price
        
        self.portfolio["total_value"] = total_value
        self.portfolio["pnl"] = total_value - self.initial_balance
        self.portfolio["pnl_percentage"] = (self.portfolio["pnl"] / self.initial_balance) * 100
    
    def _update_performance(self) -> None:
        """Update performance metrics."""
        total = self.total_trades
        if total > 0:
            self.performance.total_trades = total
            self.performance.winning_trades = self.winning_trades
            self.performance.losing_trades = self.losing_trades
            self.performance.win_rate = (self.winning_trades / total) * 100
            self.performance.total_pnl = self.portfolio["pnl"]
            self.performance.total_pnl_percentage = self.portfolio["pnl_percentage"]
    
    # ========================================================
    # BOT CONTROL - FIXED
    # ========================================================
    
    def start(self) -> bool:
        """Start the bot."""
        if self.running:
            logger.warning("Bot already running.")
            return False
        
        self.running = True
        self._stop_requested = False
        self.started_at = datetime.now().isoformat()
        self.shutdown_event.clear()
        self.pause_event.clear()
        self.state = BotState.RUNNING
        
        # FIX: Start brain di background thread
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
        
        # ============================================================
        # FIX: Safe set_status dengan 2 argumen (component, status)
        # ============================================================
        
        try:
            set_status("core", "RUNNING")
        except Exception as e:
            logger.debug(f"Set status error: {e}")
        
        logger.info("TradingBot started.")
        
        if self.on_status_change:
            try:
                self.on_status_change("RUNNING")
            except Exception:
                pass
        
        return True
    
    def _start_brain_safe(self) -> None:
        """Start brain in background."""
        try:
            if hasattr(self.brain, 'start'):
                self.brain.start()
        except Exception as e:
            logger.warning(f"Brain start error: {e}")
    
    def stop(self) -> bool:
        """Stop the bot."""
        if not self.running:
            return False
        
        logger.info("Stopping TradingBot...")
        
        self._stop_requested = True
        self.running = False
        self.shutdown_event.set()
        self.state = BotState.STOPPED
        
        # FIX: Stop brain di background
        if self.brain is not None:
            try:
                threading.Thread(
                    target=self._stop_brain_safe,
                    daemon=True
                ).start()
            except Exception as e:
                logger.warning(f"Brain stop failed: {e}")
        
        # FIX: Join thread dengan timeout
        if self.thread:
            try:
                self.thread.join(timeout=3.0)
                if self.thread.is_alive():
                    logger.warning("Worker thread still alive, forcing stop.")
            except Exception:
                pass
            self.thread = None
        
        # ============================================================
        # FIX: Safe set_status dengan 2 argumen (component, status)
        # ============================================================
        
        try:
            set_status("core", "STOPPED")
        except Exception as e:
            logger.debug(f"Set status error: {e}")
        
        logger.info("TradingBot stopped.")
        
        if self.on_status_change:
            try:
                self.on_status_change("STOPPED")
            except Exception:
                pass
        
        return True
    
    def _stop_brain_safe(self) -> None:
        """Stop brain in background."""
        try:
            if hasattr(self.brain, 'stop'):
                self.brain.stop()
        except Exception as e:
            logger.warning(f"Brain stop error: {e}")
    
    def pause(self) -> bool:
        """Pause the bot."""
        if not self.running:
            return False
        
        self.pause_event.set()
        self.state = BotState.PAUSED
        logger.info("TradingBot paused.")
        return True
    
    def resume(self) -> bool:
        """Resume the bot."""
        if not self.running:
            return False
        
        self.pause_event.clear()
        self.state = BotState.RUNNING
        logger.info("TradingBot resumed.")
        return True
    
    # ========================================================
    # WORKER LOOP - FIXED
    # ========================================================
    
    def _worker_loop(self) -> None:
        """Background worker thread - FIXED."""
        logger.info("Worker thread started.")
        
        # FIX: Gunakan interval yang aman
        interval = max(1, int(self.current_interval))
        
        while self.running and not self.shutdown_event.is_set():
            try:
                if self.pause_event.is_set():
                    time.sleep(1)
                    continue
                
                results = self.run_once()
                
                # Learn from results (di background)
                if results and self.learning_engine is not None:
                    threading.Thread(
                        target=self._learn_safe,
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
            
            # FIX: Sleep dengan interval yang aman
            for _ in range(interval):
                if not self.running or self.shutdown_event.is_set():
                    break
                time.sleep(1)
        
        logger.info("Worker thread stopped.")
    
    def _learn_safe(self, results: List[Dict]) -> None:
        """Learn from results in background."""
        try:
            if self.learning_engine is not None:
                if hasattr(self.learning_engine, 'learn'):
                    self.learning_engine.learn({"results": results})
        except Exception:
            pass
    
    def _attempt_recovery(self) -> bool:
        """Attempt to recover from errors."""
        self.recovery_attempts += 1
        self.state = BotState.RECOVERING
        
        logger.warning(f"Recovery attempt #{self.recovery_attempts} started...")
        
        try:
            if self.errors > 20:
                self.errors = 0
            
            if self.scanner is None and SCANNER_AVAILABLE:
                self.scanner = MarketScanner()
                self._connect_scanner()
            
            # Reconnect exchange if available
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
    
    # ========================================================
    # DATA ACCESS
    # ========================================================
    
    def get_results(self) -> List[Dict]:
        """Get latest scan results."""
        with self.lock:
            return list(self.last_results)
    
    def get_snapshot(self) -> List[Dict]:
        """Get signal snapshot."""
        with self.lock:
            return list(self.signal_snapshot)
    
    def get_market_data(self, pair: str) -> List[Dict]:
        """Get market data for pair."""
        with self.lock:
            return list(self.market_data_cache.get(pair, []))
    
    def get_price(self, pair: str) -> Optional[float]:
        """Get current price for pair."""
        # Try exchange first
        if self.exchange is not None:
            price = self.get_real_time_price(pair)
            if price is not None:
                return price
        
        # Fallback to cache
        with self.lock:
            return self.price_cache.get(pair)
    
    def get_trade_history(self, limit: int = 50) -> List[TradeResult]:
        """Get trade history."""
        return self.trade_history[-limit:] if self.trade_history else []
    
    def get_signal_history(self, limit: int = 50) -> List[Dict]:
        """Get signal history."""
        return self.signal_history[-limit:] if self.signal_history else []
    
    # ========================================================
    # STATUS & HEALTH
    # ========================================================
    
    def get_status(self) -> Dict[str, Any]:
        """Get bot status."""
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
        """Comprehensive health check."""
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
            "cache_size": len(self.market_data_cache),
            "results": len(self.last_results),
            "errors": self.total_errors,
            "recovery_attempts": self.recovery_attempts,
            "last_error": self.last_error,
            "timestamp": datetime.now().isoformat(),
        }
    
    # ========================================================
    # MOBILE SNAPSHOT
    # ========================================================
    
    def get_mobile_snapshot(self) -> Dict[str, Any]:
        """Get mobile-friendly snapshot."""
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
    
    # ========================================================
    # CLEAR & SHUTDOWN
    # ========================================================
    
    def clear_results(self) -> None:
        """Clear all cached results."""
        with self.lock:
            self.last_results.clear()
            self.latest_results.clear()
            self.signal_snapshot.clear()
            self.results.clear()
            self.signal_history.clear()
            self.trade_history.clear()
            self.performance_history.clear()
        
        logger.info("Results cleared.")
    
    def shutdown(self) -> bool:
        """Complete shutdown with cleanup."""
        try:
            self.stop()
            self.clear_results()
            self._save_state()
            logger.info("TradingBot shutdown completed.")
            return True
        except Exception as e:
            logger.exception(f"Shutdown error: {e}")
            return False
    
    # ============================================================
    # FIX: _save_state - Safe JSON serialization
    # ============================================================
    
    def _save_state(self) -> None:
        """Save bot state to file."""
        try:
            state_file = self.config.get("state_file", "database/bot_state.json")
            
            # ============================================================
            # FIX: Buat data yang JSON-safe
            # ============================================================
            
            # Convert portfolio ke safe dict
            portfolio_safe = {
                "cash": float(self.portfolio.get("cash", 0)),
                "holdings": {},
                "total_value": float(self.portfolio.get("total_value", 0)),
                "pnl": float(self.portfolio.get("pnl", 0)),
                "pnl_percentage": float(self.portfolio.get("pnl_percentage", 0)),
                "initial_balance": float(self.portfolio.get("initial_balance", 0)),
            }
            
            # Convert holdings ke string keys
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