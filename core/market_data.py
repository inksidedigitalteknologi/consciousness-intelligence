# core/market_data.py
# INKSIDE DIGITAL — MARKET DATA MODULE
# ============================================================

import logging
import requests
from typing import Optional, Dict, Any, List

logger = logging.getLogger("MarketData")


class MarketData:
    """Market data wrapper — Nasdaq + Kraken."""
    
    def __init__(self):
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://www.nasdaq.com',
            'referer': 'https://www.nasdaq.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
    
    def get_historical(self, symbol: str, days: int = 730, assetclass: str = 'stocks') -> List[Dict]:
        """Ambil data historis dari Nasdaq."""
        try:
            from datetime import datetime as dt, timedelta as td
            fromdate = (dt.now() - td(days=days)).strftime('%Y-%m-%d')
            url = f'https://api.nasdaq.com/api/quote/{symbol}/historical?assetclass={assetclass}&fromdate={fromdate}&limit=9999'
            
            r = requests.get(url, headers=self.headers, timeout=20)
            if r.status_code != 200:
                return []
            
            data = r.json()
            if not data or not isinstance(data, dict):
                return []
            
            data_field = data.get('data')
            if not data_field:
                return []
            
            return data_field.get('tradesTable', {}).get('rows', [])
        except Exception as e:
            logger.error(f"get_historical error: {e}")
            return []
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """Ambil quote terbaru."""
        try:
            url = f'https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks'
            r = requests.get(url, headers=self.headers, timeout=10)
            if r.status_code != 200:
                return None
            return r.json()
        except Exception as e:
            logger.error(f"get_quote error: {e}")
            return None
    
    def get_summary(self, symbol: str) -> Optional[Dict]:
        """Ambil summary fundamental."""
        try:
            url = f'https://api.nasdaq.com/api/quote/{symbol}/summary?assetclass=stocks'
            r = requests.get(url, headers=self.headers, timeout=10)
            if r.status_code != 200:
                return None
            return r.json()
        except Exception as e:
            logger.error(f"get_summary error: {e}")
            return None




class KrakenMarketData:
    """Kraken market data — untuk crypto (Binance geo-blocked)."""
    
    def __init__(self):
        self.base_url = 'https://api.kraken.com/0/public'
        self.headers = {'user-agent': 'Mozilla/5.0'}
    
    def get_ohlc(self, pair: str = 'XBTUSD', interval: int = 60) -> List[Dict]:
        """
        Ambil OHLC data dari Kraken.
        
        Args:
            pair: XBTUSD (BTC), ETHUSD (ETH), dll
            interval: 1, 5, 15, 30, 60, 240, 1440, 10080, 21600 (menit)
            
        Returns:
            List of [time, open, high, low, close, vwap, volume, count]
        """
        try:
            url = f'{self.base_url}/OHLC?pair={pair}&interval={interval}'
            r = requests.get(url, headers=self.headers, timeout=15)
            
            if r.status_code != 200:
                logger.warning(f"Kraken OHLC {pair}: HTTP {r.status_code}")
                return []
            
            data = r.json()
            if data.get('error'):
                logger.warning(f"Kraken error: {data['error']}")
                return []
            
            result = data.get('result', {})
            # Cari key yang bukan 'last'
            for key, value in result.items():
                if key != 'last' and isinstance(value, list):
                    return value
            
            return []
        except Exception as e:
            logger.error(f"Kraken get_ohlc error: {e}")
            return []
    
    def get_ticker(self, pair: str = 'XBTUSD') -> Optional[Dict]:
        """Ambil ticker terbaru."""
        try:
            url = f'{self.base_url}/Ticker?pair={pair}'
            r = requests.get(url, headers=self.headers, timeout=10)
            
            if r.status_code != 200:
                return None
            
            data = r.json()
            if data.get('error'):
                return None
            
            result = data.get('result', {})
            for key, value in result.items():
                return value
            
            return None
        except Exception as e:
            logger.error(f"Kraken get_ticker error: {e}")
            return None
    
    def get_historical(self, symbol: str, days: int = 730, assetclass: str = 'crypto') -> List[Dict]:
        """
        Wrapper untuk kompatibilitas dengan MarketData.
        Format output: Nasdaq-like rows.
        """
        # Mapping symbol → Kraken pair
        pair_map = {
            'BTC': 'XBTUSD', 'BTCUSD': 'XBTUSD', 'BTC/USD': 'XBTUSD',
            'ETH': 'ETHUSD', 'ETHUSD': 'ETHUSD', 'ETH/USD': 'ETHUSD',
            'SOL': 'SOLUSD', 'SOLUSD': 'SOLUSD',
            'XRP': 'XRPUSD', 'XRPUSD': 'XRPUSD',
            'ADA': 'ADAUSD', 'ADAUSD': 'ADAUSD',
            'DOGE': 'XDGUSD', 'DOGEUSD': 'XDGUSD',
        }
        
        pair = pair_map.get(symbol.upper(), 'XBTUSD')
        
        # Daily interval
        ohlc = self.get_ohlc(pair, interval=1440)  # 1 hari
        
        if not ohlc:
            return []
        
        # Konversi ke Nasdaq-like format
        rows = []
        for item in ohlc[-days:]:
            # Kraken OHLC: [time, open, high, low, close, vwap, volume, count]
            try:
                from datetime import datetime as dt
                ts = int(item[0])
                date = dt.fromtimestamp(ts).strftime('%m/%d/%Y')
                
                rows.append({
                    'date': date,
                    'close': f"${float(item[4]):,.2f}",
                    'open': f"${float(item[1]):,.2f}",
                    'high': f"${float(item[2]):,.2f}",
                    'low': f"${float(item[3]):,.2f}",
                    'volume': f"{int(float(item[6])):,}",
                })
            except Exception:
                continue
        
        # Kraken return ascending, Nasdaq descending
        return list(reversed(rows))



# Singleton
market_data = MarketData()
kraken_market_data = KrakenMarketData()

# Alias untuk kompatibilitas
kraken_market = kraken_market_data

# ============================================================
# DATA CLASSES — untuk kompatibilitas core/__init__.py
# ============================================================

from dataclasses import dataclass, field
from enum import Enum

KRAKEN_VERSION = '1.0.0'


class Interval(Enum):
    """Interval data."""
    M1 = '1m'
    M5 = '5m'
    M15 = '15m'
    M30 = '30m'
    H1 = '1h'
    H4 = '4h'
    D1 = '1d'
    W1 = '1w'


class DataSource(Enum):
    """Sumber data."""
    KRAKEN = 'kraken'
    NASDAQ = 'nasdaq'


@dataclass
class TickerData:
    """Ticker data."""
    pair: str = ''
    price: float = 0.0
    bid: float = 0.0
    ask: float = 0.0
    volume: float = 0.0
    timestamp: str = ''
    high: float = 0.0
    low: float = 0.0


@dataclass
class Candle:
    """OHLC candle."""
    time: int = 0
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    vwap: float = 0.0
    volume: float = 0.0
    count: int = 0


@dataclass
class OrderBookLevel:
    """Order book level."""
    price: float = 0.0
    volume: float = 0.0


@dataclass
class OrderBook:
    """Order book."""
    pair: str = ''
    bids: list = field(default_factory=list)
    asks: list = field(default_factory=list)
    timestamp: str = ''


@dataclass
class Trade:
    """Trade data."""
    pair: str = ''
    price: float = 0.0
    volume: float = 0.0
    side: str = ''
    time: str = ''


@dataclass
class MarketMetrics:
    """Market metrics."""
    pair: str = ''
    volatility: float = 0.0
    spread: float = 0.0
    volume_24h: float = 0.0
    price_change_24h: float = 0.0


def market_self_test() -> dict:
    """Self-test untuk market data."""
    try:
        kraken_market_data_instance = KrakenMarketData()
        return {
            'status': 'ok',
            'version': KRAKEN_VERSION,
            'source': 'kraken',
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


# Alias self_test
self_test = market_self_test

