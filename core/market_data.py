# ============================================================
# core/market_data.py
# KRAKEN MARKET DATA - REAL EXCHANGE INTEGRATION
# 
# COGNITIVE MIRROR ENGINE v5.0 - ULTIMATE
# 
# Provides real-time and historical market data from Kraken exchange.
# Robust with retries, timeouts, caching, and error handling.
# ============================================================

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

# ============================================================
# VERSION
# ============================================================

KRAKEN_VERSION = "2.1.2"

# ============================================================
# ENUMS
# ============================================================

class Interval(Enum):
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    HOUR_12 = "12h"
    DAY_1 = "1d"
    WEEK_1 = "1w"


class DataSource(Enum):
    CACHE = "cache"
    API = "api"
    FALLBACK = "fallback"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class TickerData:
    pair: str
    price: float
    bid: float
    ask: float
    high_24h: float
    low_24h: float
    volume_24h: float
    change_24h: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    source: DataSource = DataSource.API


@dataclass
class Candle:
    pair: str
    interval: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class OrderBookLevel:
    price: float
    volume: float


@dataclass
class OrderBook:
    pair: str
    bids: List[OrderBookLevel]
    asks: List[OrderBookLevel]
    timestamp: str


@dataclass
class Trade:
    pair: str
    price: float
    volume: float
    side: str
    timestamp: datetime


# ============================================================
# SAFE HTTP REQUEST
# ============================================================

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

try:
    import krakenex
    KRAKENEX_AVAILABLE = True
except ImportError:
    KRAKENEX_AVAILABLE = False
    krakenex = None


# ============================================================
# PAIR MAPPING (Kraken format)
# ============================================================

PAIR_MAP = {
    "BTC/USD": "XXBTZUSD",
    "ETH/USD": "XETHZUSD",
    "SOL/USD": "SOLUSD",
    "XRP/USD": "XXRPZUSD",
    "ADA/USD": "ADAUSD",
    "DOT/USD": "DOTUSD",
    "LINK/USD": "LINKUSD",
    "AVAX/USD": "AVAXUSD",
    "MATIC/USD": "MATICUSD",
    "UNI/USD": "UNIUSD",
    "BTC/USDT": "XBTUSDT",
    "ETH/USDT": "ETHUSDT",
    "SOL/USDT": "SOLUSDT",
    "XRP/USDT": "XRPUSDT",
    "ADA/USDT": "ADAUSDT",
    "BTC/EUR": "XBTEUR",
    "ETH/EUR": "ETHEUR",
}

REVERSE_PAIR_MAP = {v: k for k, v in PAIR_MAP.items()}


# ============================================================
# KRAKEN MARKET DATA CLASS
# ============================================================

class KrakenMarketData:
    BASE_URL = "https://api.kraken.com/0/public/"
    TIMEOUT = 10
    RETRIES = 3
    BACKOFF = 0.5
    CACHE_TTL = 5
    MAX_CACHE_SIZE = 100
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self._cache: Dict[str, Dict] = {}
        self._cache_time: Dict[str, float] = {}
        self._last_request_time = 0
        self._request_count = 0
        
        if KRAKENEX_AVAILABLE:
            self._api = krakenex.API()
            logger.debug("Kraken Market Data initialized with krakenex")
        else:
            self._api = None
            logger.debug("Kraken Market Data initialized with requests")
        
        self.pairs = list(PAIR_MAP.keys())
        logger.debug(f"Kraken Market Data v{KRAKEN_VERSION} ready. {len(self.pairs)} pairs configured.")
    
    def _map_pair(self, pair: str) -> str:
        return PAIR_MAP.get(pair, pair)
    
    def _unmap_pair(self, kraken_pair: str) -> str:
        return REVERSE_PAIR_MAP.get(kraken_pair, kraken_pair)
    
    def _should_cache(self, key: str) -> bool:
        if key not in self._cache_time:
            return False
        return (time.time() - self._cache_time[key]) < self.CACHE_TTL
    
    def _cache_get(self, key: str) -> Optional[Any]:
        if self._should_cache(key):
            return self._cache.get(key)
        return None
    
    def _cache_set(self, key: str, value: Any) -> None:
        if len(self._cache) > self.MAX_CACHE_SIZE:
            oldest = sorted(self._cache_time.items(), key=lambda x: x[1])[:10]
            for k, _ in oldest:
                self._cache.pop(k, None)
                self._cache_time.pop(k, None)
        self._cache[key] = value
        self._cache_time[key] = time.time()
    
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        if not REQUESTS_AVAILABLE:
            raise RuntimeError("requests library not available")
        
        elapsed = time.time() - self._last_request_time
        if elapsed < 0.5:
            time.sleep(0.5 - elapsed)
        
        url = f"{self.BASE_URL}{endpoint}"
        self._last_request_time = time.time()
        self._request_count += 1
        
        last_error = None
        for attempt in range(self.RETRIES):
            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=self.TIMEOUT,
                    headers={"User-Agent": "InksideIntelligence/5.0"}
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get("error"):
                    error_msg = "; ".join(data["error"])
                    if "EAPI:Rate limit exceeded" in error_msg:
                        time.sleep(1 * (attempt + 1))
                        continue
                    raise Exception(f"Kraken API error: {error_msg}")
                
                return data
            
            except requests.exceptions.Timeout:
                last_error = f"Timeout after {self.TIMEOUT}s"
                logger.warning(f"Kraken request timeout (attempt {attempt+1}/{self.RETRIES})")
            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error: {e}"
                logger.warning(f"Kraken connection error (attempt {attempt+1}/{self.RETRIES})")
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Kraken request error: {e} (attempt {attempt+1}/{self.RETRIES})")
            
            if attempt + 1 < self.RETRIES:
                time.sleep(self.BACKOFF * (2 ** attempt))
        
        raise Exception(f"Kraken request failed after {self.RETRIES} attempts: {last_error}")
    
    def _find_ticker_key(self, result: Dict, pair: str) -> Optional[str]:
        """Find the correct ticker key in Kraken result with fallbacks."""
        mapped_key = self._map_pair(pair)
        if mapped_key in result:
            return mapped_key
        
        if pair in result:
            return pair
        
        base = pair.split('/')[0]
        quote = pair.split('/')[1]
        
        variations = []
        if quote == 'USD':
            variations.append(f"X{base}ZUSD")
            if base == 'BTC':
                variations.append('XXBTZUSD')
            elif base == 'ETH':
                variations.append('XETHZUSD')
            elif base == 'XRP':
                variations.append('XXRPZUSD')
        variations.append(f"{base}{quote}")
        variations.append(pair)
        variations.append(f"{base.lower()}{quote.lower()}")
        variations.append(f"X{base}{quote}")
        
        for key in result:
            if key.startswith(mapped_key):
                return key
        
        for var in variations:
            if var in result:
                return var
        
        lower_result = {k.lower(): k for k in result}
        for var in variations:
            if var.lower() in lower_result:
                return lower_result[var.lower()]
        
        return None
    
    def get_ticker(self, pair: str) -> Optional[TickerData]:
        cache_key = f"ticker_{pair}"
        cached = self._cache_get(cache_key)
        if cached:
            return cached
        
        try:
            kraken_pair = pair
            data = self._request("Ticker", {"pair": kraken_pair})
            
            if not data.get("result"):
                logger.warning(f"No result in ticker response for {pair}")
                return None
            
            result = data["result"]
            ticker_key = self._find_ticker_key(result, pair)
            if ticker_key is None:
                logger.warning(f"No ticker data for {pair} (available keys: {list(result.keys())})")
                return None
            
            ticker = result[ticker_key]
            
            ask = float(ticker["a"][0])
            bid = float(ticker["b"][0])
            last = float(ticker["c"][0])
            high = float(ticker["h"][1])
            low = float(ticker["l"][1])
            volume = float(ticker["v"][1])
            change = ((last - low) / low * 100) if low > 0 else 0
            
            ticker_data = TickerData(
                pair=pair,
                price=last,
                bid=bid,
                ask=ask,
                high_24h=high,
                low_24h=low,
                volume_24h=volume,
                change_24h=change,
                source=DataSource.API
            )
            
            self._cache_set(cache_key, ticker_data)
            return ticker_data
        
        except Exception as e:
            logger.error(f"Failed to get ticker for {pair}: {e}")
            return None
    
    def get_latest_prices(self, pairs: Optional[List[str]] = None) -> Dict[str, float]:
        if pairs is None:
            pairs = self.pairs
        
        result = {}
        for pair in pairs:
            ticker = self.get_ticker(pair)
            if ticker:
                result[pair] = ticker.price
            else:
                result[pair] = 0.0
        
        return result
    
    def get_ohlc(
        self,
        pair: str,
        interval: Union[Interval, str] = Interval.HOUR_1,
        limit: int = 250
    ) -> List[Candle]:
        if isinstance(interval, Interval):
            interval = interval.value
        
        if interval not in [e.value for e in Interval]:
            raise ValueError(f"Invalid interval: {interval}")
        
        kraken_pair = self._map_pair(pair)
        
        try:
            data = self._request("OHLC", {
                "pair": kraken_pair,
                "interval": self._interval_to_kraken(interval),
                "since": None
            })
            
            if not data.get("result") or kraken_pair not in data["result"]:
                logger.warning(f"No OHLC data for {pair}")
                return []
            
            candles = data["result"][kraken_pair]
            result = []
            for c in candles[-limit:]:
                timestamp = datetime.fromtimestamp(c[0])
                result.append(Candle(
                    pair=pair,
                    interval=interval,
                    timestamp=timestamp,
                    open=float(c[1]),
                    high=float(c[2]),
                    low=float(c[3]),
                    close=float(c[4]),
                    volume=float(c[6])
                ))
            
            return result
        
        except Exception as e:
            logger.error(f"Failed to get OHLC for {pair}: {e}")
            return []
    
    def _interval_to_kraken(self, interval: str) -> int:
        mapping = {
            "1m": 1,
            "5m": 5,
            "15m": 15,
            "30m": 30,
            "1h": 60,
            "4h": 240,
            "12h": 720,
            "1d": 1440,
            "1w": 10080,
        }
        return mapping.get(interval, 60)
    
    def get_order_book(self, pair: str, depth: int = 10) -> Optional[OrderBook]:
        kraken_pair = self._map_pair(pair)
        try:
            data = self._request("Depth", {"pair": kraken_pair, "count": depth})
            if not data.get("result") or kraken_pair not in data["result"]:
                return None
            book = data["result"][kraken_pair]
            bids = [OrderBookLevel(price=float(b[0]), volume=float(b[1])) for b in book["bids"][:depth]]
            asks = [OrderBookLevel(price=float(a[0]), volume=float(a[1])) for a in book["asks"][:depth]]
            return OrderBook(pair=pair, bids=bids, asks=asks, timestamp=datetime.now().isoformat())
        except Exception as e:
            logger.error(f"Failed to get order book for {pair}: {e}")
            return None
    
    def get_trades(self, pair: str, limit: int = 50) -> List[Trade]:
        kraken_pair = self._map_pair(pair)
        try:
            data = self._request("Trades", {"pair": kraken_pair, "count": limit})
            if not data.get("result") or kraken_pair not in data["result"]:
                return []
            trades = data["result"][kraken_pair]
            result = []
            for t in trades[:limit]:
                side = "buy" if t[3] == "b" else "sell"
                result.append(Trade(
                    pair=pair,
                    price=float(t[0]),
                    volume=float(t[1]),
                    side=side,
                    timestamp=datetime.fromtimestamp(t[2])
                ))
            return result
        except Exception as e:
            logger.error(f"Failed to get trades for {pair}: {e}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        try:
            ticker = self.get_ticker("BTC/USD")
            if ticker and ticker.price > 0:
                return {
                    "status": "ONLINE",
                    "health_score": 100.0,
                    "version": KRAKEN_VERSION,
                    "last_check": datetime.now().isoformat(),
                    "price": ticker.price,
                    "timestamp": ticker.timestamp,
                }
            else:
                return {
                    "status": "DEGRADED",
                    "health_score": 50.0,
                    "version": KRAKEN_VERSION,
                    "last_check": datetime.now().isoformat(),
                    "message": "Ticker request returned no data",
                }
        except Exception as e:
            return {
                "status": "OFFLINE",
                "health_score": 0.0,
                "version": KRAKEN_VERSION,
                "last_check": datetime.now().isoformat(),
                "error": str(e),
            }
    
    def get_pairs(self) -> List[str]:
        return self.pairs.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "request_count": self._request_count,
            "cache_size": len(self._cache),
            "pairs_configured": len(self.pairs),
            "last_request_time": datetime.fromtimestamp(self._last_request_time).isoformat() if self._last_request_time > 0 else None,
        }
    
    def clear_cache(self) -> None:
        self._cache.clear()
        self._cache_time.clear()
        logger.debug("Cache cleared")
    
    def self_test(self) -> Dict[str, Any]:
        results = {
            "exchange": "Kraken",
            "version": KRAKEN_VERSION,
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "passed": 0,
            "failed": 0,
        }
        
        try:
            health = self.health_check()
            results["tests"]["health"] = health
            if health.get("status") == "ONLINE":
                results["passed"] += 1
            else:
                results["failed"] += 1
        except Exception as e:
            results["tests"]["health"] = {"error": str(e)}
            results["failed"] += 1
        
        try:
            ticker = self.get_ticker("BTC/USD")
            if ticker and ticker.price > 0:
                results["tests"]["ticker"] = {"status": "PASS", "price": ticker.price}
                results["passed"] += 1
            else:
                results["tests"]["ticker"] = {"status": "FAIL", "message": "No ticker data"}
                results["failed"] += 1
        except Exception as e:
            results["tests"]["ticker"] = {"status": "ERROR", "error": str(e)}
            results["failed"] += 1
        
        try:
            candles = self.get_ohlc("BTC/USD", Interval.HOUR_1, limit=10)
            if candles and len(candles) > 0:
                results["tests"]["ohlc"] = {"status": "PASS", "count": len(candles)}
                results["passed"] += 1
            else:
                results["tests"]["ohlc"] = {"status": "FAIL", "message": "No OHLC data"}
                results["failed"] += 1
        except Exception as e:
            results["tests"]["ohlc"] = {"status": "ERROR", "error": str(e)}
            results["failed"] += 1
        
        results["success"] = results["failed"] == 0
        return results


# ============================================================
# GLOBAL INSTANCE
# ============================================================

kraken_market = KrakenMarketData()
exchange = kraken_market


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def get_exchange() -> KrakenMarketData:
    return kraken_market


def get_market_data() -> KrakenMarketData:
    return kraken_market


def get_ticker(pair: str) -> Optional[TickerData]:
    return kraken_market.get_ticker(pair)


def get_latest_prices(pairs: Optional[List[str]] = None) -> Dict[str, float]:
    return kraken_market.get_latest_prices(pairs)


def get_ohlc(pair: str, interval: str = '1h', limit: int = 250) -> List[Candle]:
    return kraken_market.get_ohlc(pair, interval, limit)


def test_connection() -> bool:
    return kraken_market.health_check().get('status') == 'ONLINE'


def self_test() -> Dict[str, Any]:
    return kraken_market.self_test()


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "KrakenMarketData",
    "kraken_market",
    "exchange",
    "TickerData",
    "Candle",
    "OrderBook",
    "OrderBookLevel",
    "Trade",
    "Interval",
    "DataSource",
    "get_exchange",
    "get_market_data",
    "get_ticker",
    "get_latest_prices",
    "get_ohlc",
    "test_connection",
    "self_test",
    "KRAKEN_VERSION",
    "PAIR_MAP",
]


# ============================================================
# SELF-TEST
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("=" * 70)
    print("  KRAKEN MARKET DATA v" + KRAKEN_VERSION + " - SELF-TEST")
    print("=" * 70)
    print()
    market = KrakenMarketData()
    result = market.self_test()
    print("Test Results:")
    for name, test in result["tests"].items():
        status = test.get("status", "UNKNOWN")
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"  {icon} {name}: {status}")
        if "price" in test:
            print(f"      Price: ${test['price']}")
        if "count" in test:
            print(f"      Count: {test['count']}")
        if "error" in test:
            print(f"      Error: {test['error']}")
    print()
    print(f"Passed: {result['passed']}, Failed: {result['failed']}")
    print(f"Overall: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
    print("=" * 70)


# ============================================================
# END
# ============================================================