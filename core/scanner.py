#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# INKSIDE DIGITAL TRADING BOT
# COGNITIVE MARKET SCANNER ENGINE
#
# Version: 5.2 COGNITIVE AWARENESS - FIXED
#
# FIXES:
# - Fixed record_health import (safe import)
# - Fixed scanning flag reset on error
# - Added safe interval check in scan loop
# - Added proper ThreadPoolExecutor cleanup
# - Better error handling
# ============================================================

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Optional, Dict, Any, List, Callable, Union

from config import (
    DEFAULT_PAIRS,
    MAIN_TIMEFRAME
)

from core.health import set_status, health_monitor

# ============================================================
# FIX: Safe import for record_health
# ============================================================

try:
    from core.health import record_health
    RECORD_HEALTH_AVAILABLE = True
except ImportError:
    RECORD_HEALTH_AVAILABLE = False
    def record_health(*args, **kwargs):
        pass

from core.market_data import KrakenMarketData
from core.analyzer import MarketAnalyzer
from core.signal_engine import SignalEngine

logger = logging.getLogger(__name__)

# ============================================================
# TIMEFRAME CONFIG
# ============================================================

TIMEFRAME_MAP = {
    "1m": 1,
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "1h": 60,
    "4h": 240,
    "1d": 1440
}

DEFAULT_TIMEFRAMES = ["5m", "15m", "1h", "4h", "1d"]

TIMEFRAME_WEIGHT = {
    "5m": 1.0,
    "15m": 1.5,
    "1h": 2.0,
    "4h": 2.5,
    "1d": 3.0
}


# ============================================================
# HELPER: SAFE CANDLE ACCESS
# ============================================================

def safe_candle_value(candle: Any, index: int, default: Any = 0) -> Any:
    """
    Safely get value from candle regardless of format.
    
    Supports:
    - List/tuple: candle[index]
    - Dict: candle.get(key)
    - Other: default
    """
    if candle is None:
        return default
    
    if isinstance(candle, (list, tuple)):
        try:
            return candle[index] if len(candle) > index else default
        except (IndexError, TypeError):
            return default
    
    if isinstance(candle, dict):
        keys = ["timestamp", "open", "high", "low", "close", "volume"]
        key = keys[index] if index < len(keys) else None
        if key:
            return candle.get(key, default)
        return default
    
    return default


def safe_candle_price(candle: Any) -> float:
    """Safely get price from candle."""
    if candle is None:
        return 0.0
    
    if isinstance(candle, (list, tuple)):
        return float(candle[4]) if len(candle) > 4 else 0.0
    
    if isinstance(candle, dict):
        return float(candle.get("close", candle.get("price", 0)))
    
    return 0.0


def safe_candle_volume(candle: Any) -> float:
    """Safely get volume from candle."""
    if candle is None:
        return 0.0
    
    if isinstance(candle, (list, tuple)):
        return float(candle[5]) if len(candle) > 5 else 0.0
    
    if isinstance(candle, dict):
        return float(candle.get("volume", 0))
    
    return 0.0


# ============================================================
# COGNITIVE SCANNER
# ============================================================

class CognitiveMarketScanner:
    """
    Market Scanner with Cognitive Awareness.
    Integrated with Consciousness, Brain, and Learning Engine.
    """
    
    VERSION = "5.2 COGNITIVE AWARENESS - FIXED"
    
    def __init__(
        self,
        market_data=None,
        analyzer=None,
        signal_engine=None,
        consciousness=None,
        brain=None,
        learning_engine=None,
        semantic_memory=None
    ):
        # Core components
        self.market_data = market_data or KrakenMarketData()
        self.analyzer = analyzer or MarketAnalyzer()
        self.signal_engine = signal_engine or SignalEngine()
        
        # Cognitive components
        self.consciousness = consciousness
        self.brain = brain
        self.learning_engine = learning_engine
        self.semantic_memory = semantic_memory
        
        # Runtime
        self.running = False
        self.scanning = False
        self.scan_thread = None
        self._stop_requested = False
        
        # Result storage
        self.last_results: List[Dict] = []
        self.results_by_pair: Dict[str, Dict] = {}
        
        # Market data cache
        self.market_cache: Dict[str, Dict] = {}
        self.candle_cache: Dict[str, List] = {}
        self.price_cache: Dict[str, float] = {}
        self.volume_cache: Dict[str, float] = {}
        
        # Consciousness state
        self.consciousness_state: Dict[str, Any] = {}
        self.market_awareness: Dict[str, Any] = {}
        self.sentiment_memory: List[Dict] = []
        
        # Statistics
        self.last_scan_time = None
        self.last_scan_duration = 0
        self.total_scans = 0
        self.successful_scans = 0
        self.failed_scans = 0
        self.signals_generated = 0
        self.learning_cycles = 0
        
        # Thread lock
        self.lock = threading.RLock()
        
        # Callbacks
        self.on_scan_complete = None
        self.on_pair_complete = None
        self.on_signal_generated = None
        self.on_status_change = None
        self.on_consciousness_update = None
        
        logger.info(
            "CognitiveMarketScanner %s initialized",
            self.VERSION
        )
        
        # Register to health monitor
        try:
            if health_monitor and hasattr(health_monitor, 'register'):
                health_monitor.register("scanner")
            set_status("scanner", "INITIALIZED")
        except Exception:
            pass
    
    # ============================================================
    # STATUS CALLBACK
    # ============================================================
    
    def _notify_status(self, status: str) -> None:
        """Notify status change."""
        if self.on_status_change:
            try:
                self.on_status_change(status)
            except Exception:
                pass
    
    def _notify_signal(self, signal: Dict) -> None:
        """Notify signal generated."""
        if self.on_signal_generated:
            try:
                self.on_signal_generated(signal)
            except Exception:
                pass
    
    # ============================================================
    # CONSCIOUSNESS INTEGRATION
    # ============================================================
    
    def _update_consciousness(self, market_state: Dict) -> None:
        """Update consciousness with market state."""
        if not self.consciousness:
            return
        
        try:
            awareness = {
                "timestamp": datetime.now().isoformat(),
                "market": market_state.get("pair", "UNKNOWN"),
                "price": market_state.get("price", 0),
                "trend": market_state.get("trend", "NEUTRAL"),
                "signal": market_state.get("signal", "HOLD"),
                "confidence": market_state.get("confidence", 0),
                "volume": market_state.get("volume", 0),
                "source": "market_scanner"
            }
            
            if hasattr(self.consciousness, 'update_awareness'):
                self.consciousness.update_awareness(awareness)
            
            self.consciousness_state = awareness
            self.market_awareness[market_state.get("pair", "")] = awareness
            
            if self.on_consciousness_update:
                self.on_consciousness_update(awareness)
                
        except Exception as e:
            logger.debug(f"Consciousness update error: {e}")
    
    # ============================================================
    # BRAIN INTEGRATION
    # ============================================================
    
    def _update_brain(self, market_data: Dict) -> None:
        """Update brain with market data."""
        if not self.brain:
            return
        
        try:
            if hasattr(self.brain, 'observe'):
                if hasattr(market_data, 'to_dict'):
                    data = market_data.to_dict()
                elif isinstance(market_data, dict):
                    data = market_data
                else:
                    data = {"data": str(market_data)}
                
                self.brain.observe({
                    "type": "market_scan",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                })
        except Exception as e:
            logger.debug(f"Brain update error: {e}")
    
    # ============================================================
    # LEARNING ENGINE INTEGRATION
    # ============================================================
    
    def _learn_from_scan(self, result: Dict) -> None:
        """Learn from scan results."""
        if not self.learning_engine:
            return
        
        try:
            learning_data = {
                "pair": result.get("pair"),
                "price": result.get("price"),
                "trend": result.get("analysis", {}).get("trend"),
                "signal": result.get("signal", {}).get("signal"),
                "confidence": result.get("signal", {}).get("confidence"),
                "mtf_alignment": result.get("mtf", {}),
                "timestamp": datetime.now().isoformat()
            }
            
            if hasattr(self.learning_engine, 'learn'):
                self.learning_engine.learn(learning_data)
                self.learning_cycles += 1
                
        except Exception as e:
            logger.debug(f"Learning error: {e}")
    
    # ============================================================
    # SEMANTIC MEMORY INTEGRATION
    # ============================================================
    
    def _store_in_memory(self, pattern: Dict) -> None:
        """Store pattern in semantic memory."""
        if not self.semantic_memory:
            return
        
        try:
            if hasattr(self.semantic_memory, 'store'):
                meaning = (
                    f"{pattern.get('pair', 'Market')} - "
                    f"{pattern.get('trend', 'NEUTRAL')} trend "
                    f"with {pattern.get('signal', 'HOLD')} signal "
                    f"({pattern.get('confidence', 0)}% confidence)"
                )
                
                self.semantic_memory.store(
                    meaning=meaning,
                    category="market_pattern",
                    metadata=pattern
                )
                
        except Exception as e:
            logger.debug(f"Memory storage error: {e}")
    
    # ============================================================
    # TIMEFRAME HELPER
    # ============================================================
    
    def _get_interval(self, timeframe: str) -> int:
        """Get interval in minutes from timeframe string."""
        value = TIMEFRAME_MAP.get(timeframe)
        if value is None:
            logger.warning(f"Unknown timeframe {timeframe}, using 1h")
            return 60
        return value
    
    # ============================================================
    # MULTI TIMEFRAME ANALYSIS
    # ============================================================
    
    def scan_multi_timeframe(
        self,
        pair: str,
        timeframes: Optional[List[str]] = None
    ) -> Dict:
        """Scan multiple timeframes for a pair."""
        if timeframes is None:
            timeframes = DEFAULT_TIMEFRAMES
        
        result = {}
        
        for tf in timeframes:
            try:
                candles = self.market_data.get_ohlc(
                    pair,
                    self._get_interval(tf)
                )
                
                if not candles:
                    continue
                
                analysis = self.analyzer.analyze(pair, candles)
                
                last_candle = candles[-1] if candles else None
                price = safe_candle_price(last_candle)
                volume = safe_candle_volume(last_candle)
                
                result[tf] = {
                    "trend": analysis.get("trend", "NEUTRAL"),
                    "confidence": analysis.get("confidence", 0),
                    "signal": analysis.get("signal", "HOLD"),
                    "price": price,
                    "volume": volume
                }
                
            except Exception as e:
                logger.debug(f"MTF failed {pair} {tf}: {e}")
        
        return result
    
    # ============================================================
    # MTF ALIGNMENT
    # ============================================================
    
    def calculate_mtf_alignment(self, mtf_data: Dict) -> Dict:
        """Calculate alignment across timeframes."""
        bullish = 0
        bearish = 0
        total = 0
        
        for tf, data in mtf_data.items():
            weight = TIMEFRAME_WEIGHT.get(tf, 1)
            total += weight
            
            trend = str(data.get("trend", "")).upper()
            
            if trend == "BULLISH":
                bullish += weight
            elif trend == "BEARISH":
                bearish += weight
        
        if total == 0:
            return {"bullish": 0, "bearish": 0, "alignment": "NEUTRAL", "strength": 0}
        
        bull = round(bullish / total * 100, 2)
        bear = round(bearish / total * 100, 2)
        
        if bull > bear:
            alignment = "BULLISH"
        elif bear > bull:
            alignment = "BEARISH"
        else:
            alignment = "NEUTRAL"
        
        return {
            "bullish": bull,
            "bearish": bear,
            "alignment": alignment,
            "strength": abs(bull - bear)
        }
    
    # ============================================================
    # PREPARE SIGNAL DATA
    # ============================================================
    
    def _prepare_signal_data(self, analysis: Dict, mtf_data: Dict) -> Dict:
        """Prepare data for signal engine."""
        data = dict(analysis)
        indicators = data.get("indicators", {})
        
        if not isinstance(indicators, dict):
            indicators = {}
        
        for key, value in indicators.items():
            if isinstance(value, (int, float)):
                data[key] = value
        
        macd = indicators.get("macd", {})
        if isinstance(macd, dict):
            data["macd"] = macd.get("macd")
            data["macd_signal"] = macd.get("signal")
            data["macd_histogram"] = macd.get("histogram")
        
        bb = indicators.get("bollinger", {})
        if isinstance(bb, dict):
            data["bb_upper"] = bb.get("upper")
            data["bb_middle"] = bb.get("middle")
            data["bb_lower"] = bb.get("lower")
        
        rsi = indicators.get("rsi", {})
        if isinstance(rsi, dict):
            data["rsi"] = rsi.get("value")
        
        data["timeframes"] = {}
        for tf, item in mtf_data.items():
            data["timeframes"][tf] = item.get("trend", "NEUTRAL")
        
        data["mtf_alignment"] = self.calculate_mtf_alignment(mtf_data)
        
        return data
    
    # ============================================================
    # SCAN SINGLE PAIR
    # ============================================================
    
    def scan_pair(self, pair: str, timeframe: str = MAIN_TIMEFRAME) -> Dict:
        """Scan a single pair with cognitive awareness."""
        start = time.time()
        
        try:
            interval = self._get_interval(timeframe)
            candles = self.market_data.get_ohlc(pair, interval)
            
            if not candles:
                return {
                    "pair": pair,
                    "status": "NO_DATA",
                    "signal": {"signal": "HOLD", "confidence": 0},
                    "price": None
                }
            
            last_candle = candles[-1]
            price = safe_candle_price(last_candle)
            volume = safe_candle_volume(last_candle)
            
            ohlc = {}
            if isinstance(last_candle, dict):
                ohlc = {
                    "open": last_candle.get("open"),
                    "high": last_candle.get("high"),
                    "low": last_candle.get("low"),
                    "close": last_candle.get("close"),
                    "volume": last_candle.get("volume")
                }
            elif isinstance(last_candle, (list, tuple)):
                ohlc = {
                    "timestamp": last_candle[0] if len(last_candle) > 0 else None,
                    "open": last_candle[1] if len(last_candle) > 1 else None,
                    "high": last_candle[2] if len(last_candle) > 2 else None,
                    "low": last_candle[3] if len(last_candle) > 3 else None,
                    "close": last_candle[4] if len(last_candle) > 4 else None,
                    "volume": last_candle[5] if len(last_candle) > 5 else None
                }
            
            analysis = self.analyzer.analyze(pair, candles)
            if not analysis:
                analysis = {"trend": "NEUTRAL"}
            
            mtf_data = self.scan_multi_timeframe(pair)
            
            signal_input = self._prepare_signal_data(analysis, mtf_data)
            signal = self.signal_engine.generate_signal(signal_input)
            
            if not signal:
                signal = {"signal": "HOLD", "confidence": 0}
            
            result = {
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat(),
                "pair": pair,
                "symbol": pair,
                "timeframe": timeframe,
                "price": price,
                "ohlc": ohlc,
                "candles": candles[-100:],
                "volume": volume,
                "analysis": analysis,
                "mtf": mtf_data,
                "signal": signal,
                "candles_count": len(candles),
                "status": "OK",
                "execution_time": round(time.time() - start, 4)
            }
            
            with self.lock:
                self.results_by_pair[pair] = result
                self.market_cache[pair] = result
                self.candle_cache[pair] = candles[-100:]
                self.price_cache[pair] = price
                self.volume_cache[pair] = volume
            
            market_state = {
                "pair": pair,
                "price": price,
                "trend": analysis.get("trend", "NEUTRAL"),
                "signal": signal.get("signal", "HOLD"),
                "confidence": signal.get("confidence", 0),
                "volume": volume
            }
            
            self._update_consciousness(market_state)
            self._update_brain(result)
            self._learn_from_scan(result)
            
            if signal.get("signal") in ["BUY", "SELL", "STRONG_BUY", "STRONG_SELL"]:
                self._store_in_memory({
                    "pair": pair,
                    "trend": analysis.get("trend", "NEUTRAL"),
                    "signal": signal.get("signal"),
                    "confidence": signal.get("confidence"),
                    "price": price
                })
            
            self._notify_signal({
                "pair": pair,
                "signal": signal.get("signal"),
                "confidence": signal.get("confidence"),
                "price": price,
                "timestamp": datetime.now().isoformat()
            })
            
            if RECORD_HEALTH_AVAILABLE:
                try:
                    record_health(
                        "scanner",
                        duration=time.time() - start,
                        success=True
                    )
                except Exception:
                    pass
            
            return result
            
        except Exception as e:
            logger.warning(f"Scan pair failed {pair}: {e}")
            
            with self.lock:
                self.failed_scans += 1
            
            if RECORD_HEALTH_AVAILABLE:
                try:
                    record_health(
                        "scanner",
                        duration=time.time() - start,
                        success=False,
                        error=str(e)
                    )
                except Exception:
                    pass
            
            return {
                "pair": pair,
                "status": "ERROR",
                "error": str(e),
                "signal": {"signal": "HOLD", "confidence": 0},
                "price": None
            }
    
    # ============================================================
    # SCAN ALL PAIRS - FIXED
    # ============================================================
    
    def scan_all(
        self,
        pairs: Optional[List[str]] = None,
        timeframe: str = MAIN_TIMEFRAME,
        max_workers: int = 10
    ) -> List[Dict]:
        """Scan all pairs with parallel processing."""
        # FIX: Reset scanning flag with proper lock
        with self.lock:
            if self.scanning:
                return list(self.last_results)
            self.scanning = True
        
        start = time.time()
        
        if pairs is None:
            pairs = DEFAULT_PAIRS
        
        pairs = list(pairs)
        results = []
        
        self._notify_status("SCANNING")
        
        try:
            workers = min(max_workers, max(1, len(pairs)))
            
            # FIX: Proper ThreadPoolExecutor usage
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {
                    executor.submit(self.scan_pair, pair, timeframe): pair
                    for pair in pairs
                }
                
                for future in as_completed(futures):
                    try:
                        result = future.result(timeout=30)
                        if result:
                            results.append(result)
                            if result.get("signal", {}).get("signal") not in ["HOLD", "NEUTRAL"]:
                                self.signals_generated += 1
                    except Exception as e:
                        pair = futures[future]
                        logger.warning(f"Future error for {pair}: {e}")
                        results.append({
                            "pair": pair,
                            "status": "ERROR",
                            "error": str(e),
                            "signal": {"signal": "HOLD", "confidence": 0}
                        })
        
        except Exception as e:
            logger.error(f"Scan all failed: {e}")
            self._notify_status("ERROR")
        
        results.sort(key=lambda x: x.get("pair", ""))
        
        elapsed = round(time.time() - start, 2)
        
        # FIX: Reset scanning flag with lock
        with self.lock:
            if results:
                self.last_results = list(results)
            self.last_scan_time = datetime.now()
            self.last_scan_duration = elapsed
            self.total_scans += 1
            self.successful_scans += 1
            self.scanning = False
        
        self._notify_status("READY")
        
        signal_count = sum(1 for r in results if r.get("signal", {}).get("signal") not in ["HOLD", "NEUTRAL"])
        
        logger.info(
            "Scanner finished | Pairs: %d | Duration: %.2fs | Signals: %d",
            len(results),
            elapsed,
            signal_count
        )
        
        if self.on_scan_complete:
            try:
                self.on_scan_complete(list(self.last_results))
            except Exception:
                pass
        
        return list(self.last_results)
    
    # ============================================================
    # CONTINUOUS SCAN - FIXED
    # ============================================================
    
    def start(
        self,
        pairs: Optional[List[str]] = None,
        timeframe: str = MAIN_TIMEFRAME,
        interval_seconds: int = 60
    ) -> bool:
        """Start continuous scanning."""
        if self.running:
            logger.warning("Scanner already running.")
            return False
        
        # FIX: Ensure minimum interval
        interval_seconds = max(5, interval_seconds)
        
        self.running = True
        self._stop_requested = False
        self._notify_status("STARTING")
        
        self.scan_thread = threading.Thread(
            target=self._scan_loop,
            args=(pairs, timeframe, interval_seconds),
            daemon=True,
            name="CognitiveScannerThread"
        )
        self.scan_thread.start()
        
        logger.info(f"Cognitive scanner started (interval={interval_seconds}s)")
        return True
    
    def _scan_loop(self, pairs, timeframe, interval_seconds):
        """Main scan loop - FIXED."""
        while self.running and not self._stop_requested:
            try:
                self.scan_all(pairs=pairs, timeframe=timeframe)
            except Exception as e:
                logger.error(f"Scanner loop error: {e}")
                self._notify_status("ERROR")
            
            # FIX: Use time.sleep with proper interval
            if self.running and not self._stop_requested:
                time.sleep(interval_seconds)
        
        self._notify_status("STOPPED")
    
    def stop(self) -> bool:
        """Stop continuous scanning."""
        if not self.running:
            return False
        
        logger.info("Stopping scanner...")
        self._stop_requested = True
        self.running = False
        
        # FIX: Wait for thread to finish
        if self.scan_thread and self.scan_thread.is_alive():
            try:
                self.scan_thread.join(timeout=3.0)
            except Exception:
                pass
        
        try:
            set_status("scanner", "STOPPED")
        except Exception:
            pass
        
        return True
    
    # ============================================================
    # RESULT ACCESS
    # ============================================================
    
    def get_results(self) -> List[Dict]:
        """Get last scan results."""
        with self.lock:
            return list(self.last_results)
    
    def get_pair_result(self, pair: str) -> Optional[Dict]:
        """Get result for specific pair."""
        with self.lock:
            return self.results_by_pair.get(pair)
    
    def get_market_price(self, pair: str) -> Optional[float]:
        """Get latest market price."""
        with self.lock:
            return self.price_cache.get(pair)
    
    def get_candles(self, pair: str) -> List:
        """Get cached candles."""
        with self.lock:
            return list(self.candle_cache.get(pair, []))
    
    def get_signals(self) -> List[Dict]:
        """Get all active signals."""
        signals = []
        for result in self.get_results():
            signal = result.get("signal", {})
            if signal.get("signal") not in ["HOLD", "NEUTRAL"]:
                signals.append({
                    "pair": result.get("pair"),
                    "signal": signal.get("signal"),
                    "confidence": signal.get("confidence"),
                    "price": result.get("price"),
                    "timestamp": result.get("datetime")
                })
        return signals
    
    # ============================================================
    # CONSCIOUSNESS QUERY
    # ============================================================
    
    def get_market_awareness(self) -> Dict:
        """Get current market awareness from consciousness."""
        if not self.consciousness:
            return {"status": "consciousness_not_available"}
        
        try:
            if hasattr(self.consciousness, 'get_state'):
                return self.consciousness.get_state()
        except Exception:
            pass
        
        return self.consciousness_state
    
    def get_sentiment(self) -> Dict:
        """Get market sentiment from consciousness."""
        if not self.consciousness:
            return {"status": "consciousness_not_available"}
        
        try:
            if hasattr(self.consciousness, 'get_sentiment'):
                return self.consciousness.get_sentiment()
        except Exception:
            pass
        
        return {"sentiment": "NEUTRAL", "confidence": 0}
    
    # ============================================================
    # STATUS
    # ============================================================
    
    def get_status(self) -> Dict:
        """Get scanner status."""
        with self.lock:
            return {
                "version": self.VERSION,
                "running": self.running,
                "scanning": self.scanning,
                "total_scans": self.total_scans,
                "successful_scans": self.successful_scans,
                "failed_scans": self.failed_scans,
                "signals_generated": self.signals_generated,
                "learning_cycles": self.learning_cycles,
                "last_scan_time": (
                    self.last_scan_time.isoformat()
                    if self.last_scan_time
                    else None
                ),
                "last_scan_duration": self.last_scan_duration,
                "pairs_scanned": len(self.last_results),
                "consciousness_connected": self.consciousness is not None,
                "brain_connected": self.brain is not None,
                "learning_connected": self.learning_engine is not None,
                "memory_connected": self.semantic_memory is not None
            }
    
    def get_summary(self) -> Dict:
        """Get scan summary."""
        results = self.get_results()
        
        summary = {
            "total": len(results),
            "buy": 0,
            "sell": 0,
            "hold": 0,
            "strong_buy": 0,
            "strong_sell": 0,
            "bullish": 0,
            "bearish": 0,
            "neutral": 0,
            "errors": 0,
            "avg_confidence": 0
        }
        
        confidences = []
        
        for result in results:
            if result.get("status") != "OK":
                summary["errors"] += 1
                continue
            
            signal = result.get("signal", {})
            analysis = result.get("analysis", {})
            
            name = str(signal.get("signal", "HOLD")).upper()
            trend = str(analysis.get("trend", "NEUTRAL")).upper()
            confidence = signal.get("confidence", 0)
            
            if name in ["BUY", "STRONG_BUY"]:
                summary["buy"] += 1
            elif name in ["SELL", "STRONG_SELL"]:
                summary["sell"] += 1
            else:
                summary["hold"] += 1
            
            if trend == "BULLISH":
                summary["bullish"] += 1
            elif trend == "BEARISH":
                summary["bearish"] += 1
            else:
                summary["neutral"] += 1
            
            if confidence > 0:
                confidences.append(confidence)
        
        if confidences:
            summary["avg_confidence"] = round(sum(confidences) / len(confidences), 2)
        
        return summary
    
    # ============================================================
    # CLEAR
    # ============================================================
    
    def clear_results(self) -> None:
        """Clear all cached results."""
        with self.lock:
            self.last_results = []
            self.results_by_pair = {}
            self.market_cache = {}
            self.candle_cache = {}
            self.price_cache = {}
            self.volume_cache = {}
            self.last_scan_time = None
            self.last_scan_duration = 0
        
        logger.info("Scanner cache cleared.")
    
    def clear_memory(self) -> None:
        """Clear semantic memory of market patterns."""
        if self.semantic_memory:
            try:
                if hasattr(self.semantic_memory, 'clear'):
                    self.semantic_memory.clear(category="market_pattern")
                    logger.info("Market patterns cleared from semantic memory")
            except Exception as e:
                logger.warning(f"Failed to clear memory: {e}")
    
    # ============================================================
    # SHUTDOWN
    # ============================================================
    
    def shutdown(self) -> bool:
        """Complete shutdown."""
        try:
            self.stop()
            self.clear_results()
            logger.info("Scanner shutdown completed.")
            return True
        except Exception as e:
            logger.error(f"Shutdown error: {e}")
            return False


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

MarketScanner = CognitiveMarketScanner
MarketScannerEngine = CognitiveMarketScanner