# core/nonkyc.py
# INKSIDE DIGITAL - NONKYC.IO INTEGRATION v1.0
# PRIVACY-FOCUSED EXCHANGE CONNECTOR

import os
import time
import json
import hmac
import hashlib
import base64
import logging
import requests
import threading
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

# ============================================================
# CONSTANTS
# ============================================================

BASE_URL = "https://api.nonkyc.io/api/v2"
WS_URL = "wss://ws.nonkyc.io"
REST_URL = BASE_URL

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class TickerData:
    """Ticker data from NonKYC."""
    pair: str
    price: float
    bid: float
    ask: float
    high_24h: float
    low_24h: float
    volume_24h: float
    change_24h: float
    timestamp: str
    source: str = "nonkyc"

@dataclass
class BalanceData:
    """Balance data from NonKYC."""
    asset: str
    free: float
    locked: float
    total: float
    timestamp: str

@dataclass
class OrderData:
    """Order data from NonKYC."""
    order_id: str
    pair: str
    side: str  # 'BUY' or 'SELL'
    type: str  # 'LIMIT' or 'MARKET'
    price: float
    amount: float
    filled: float
    status: str  # 'OPEN', 'CLOSED', 'CANCELED'
    timestamp: str

# ============================================================
# NONKYC CLIENT
# ============================================================

class NonKycClient:
    """
    NonKYC.io Exchange Client v1.0
    No KYC required - privacy-focused trading.
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.api_key = os.getenv('NONKYC_API_KEY', '')
        self.api_secret = os.getenv('NONKYC_API_SECRET', '')
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Inkside-Digital-Bot/2.0',
            'Content-Type': 'application/json'
        })
        
        # Cache
        self._ticker_cache: Dict[str, TickerData] = {}
        self._balance_cache: Dict[str, BalanceData] = {}
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "last_request": None
        }
        
        self._configured = bool(self.api_key and self.api_secret)
        
        if self._configured:
            logger.info(f"🔄 NonKYC client initialized (API Key: {self.api_key[:8]}...)")
        else:
            logger.warning("⚠️ NonKYC API keys not configured. Public methods only.")
        
        # Register in health monitor
        try:
            from core.health import set_status
            set_status("nonkyc", "INITIALIZED")
        except:
            pass
    
    # ============================================================
    # AUTHENTICATION
    # ============================================================
    
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """Generate HMAC-SHA256 signature for NonKYC API."""
        if not self.api_secret:
            return ""
        
        # NonKYC uses HMAC-SHA256 with timestamp
        # Format: timestamp + params sorted by key
        sorted_params = sorted(params.items())
        query_string = urlencode(sorted_params)
        
        # Add timestamp to signature
        timestamp = params.get('timestamp', str(int(time.time() * 1000)))
        message = f"{timestamp}{query_string}"
        
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        private: bool = False
    ) -> Dict:
        """Make authenticated request to NonKYC API."""
        url = f"{self.base_url}{endpoint}"
        
        # Add timestamp for authentication
        if private:
            if not self._configured:
                return {"error": "API keys not configured"}
            
            params = params or {}
            params['timestamp'] = str(int(time.time() * 1000))
            params['signature'] = self._generate_signature(params)
        
        headers = {}
        if private and self.api_key:
            headers['X-API-KEY'] = self.api_key
        
        # Update stats
        self.stats["total_requests"] += 1
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=15)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=params, headers=headers, timeout=15)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            self.stats["last_request"] = datetime.now().isoformat()
            
            if response.status_code == 200:
                self.stats["successful_requests"] += 1
                return response.json()
            else:
                self.stats["failed_requests"] += 1
                logger.error(f"NonKYC API error: {response.status_code} - {response.text}")
                return {
                    "error": f"HTTP {response.status_code}",
                    "message": response.text
                }
                
        except Exception as e:
            self.stats["failed_requests"] += 1
            logger.error(f"NonKYC request error: {e}")
            return {"error": str(e)}
    
    # ============================================================
    # PUBLIC METHODS
    # ============================================================
    
    def get_ticker(self, pair: str) -> TickerData:
        """
        Get ticker data for a pair.
        
        Args:
            pair: Trading pair (e.g., 'BTC/USD', 'BTC/USDT')
        """
        # Try cache first (5 second TTL)
        cache_key = pair
        if cache_key in self._ticker_cache:
            cached = self._ticker_cache[cache_key]
            # Check if cache is still valid (5 seconds)
            try:
                if (datetime.now() - datetime.fromisoformat(cached.timestamp)).seconds < 5:
                    return cached
            except:
                pass
        
        # Normalize pair format
        pair_formatted = pair.replace('/', '')
        
        # Try with pair in URL
        result = self._request('GET', f'/public/ticker/{pair_formatted}')
        
        if result and not result.get('error'):
            try:
                ticker = TickerData(
                    pair=pair,
                    price=float(result.get('last', result.get('price', 0))),
                    bid=float(result.get('bid', 0)),
                    ask=float(result.get('ask', 0)),
                    high_24h=float(result.get('high', 0)),
                    low_24h=float(result.get('low', 0)),
                    volume_24h=float(result.get('volume', 0)),
                    change_24h=float(result.get('change', 0)),
                    timestamp=datetime.now().isoformat()
                )
                self._ticker_cache[cache_key] = ticker
                return ticker
            except Exception as e:
                logger.error(f"Error parsing ticker: {e}")
        
        # Fallback: try public/tickers
        result = self._request('GET', '/public/tickers')
        
        if result and not result.get('error'):
            for tick in result:
                if tick.get('pair') == pair_formatted:
                    try:
                        ticker = TickerData(
                            pair=pair,
                            price=float(tick.get('last', 0)),
                            bid=float(tick.get('bid', 0)),
                            ask=float(tick.get('ask', 0)),
                            high_24h=float(tick.get('high', 0)),
                            low_24h=float(tick.get('low', 0)),
                            volume_24h=float(tick.get('volume', 0)),
                            change_24h=float(tick.get('change', 0)),
                            timestamp=datetime.now().isoformat()
                        )
                        self._ticker_cache[cache_key] = ticker
                        return ticker
                    except Exception as e:
                        logger.error(f"Error parsing ticker: {e}")
        
        # Last fallback
        return TickerData(
            pair=pair,
            price=0,
            bid=0,
            ask=0,
            high_24h=0,
            low_24h=0,
            volume_24h=0,
            change_24h=0,
            timestamp=datetime.now().isoformat()
        )
    
    def get_ohlc(self, pair: str, timeframe: str = '1h', limit: int = 100) -> List[List[Any]]:
        """
        Get OHLC data for a pair.
        
        Args:
            pair: Trading pair
            timeframe: 1m, 5m, 15m, 1h, 4h, 1d, 1w
            limit: Number of candles
        """
        pair_formatted = pair.replace('/', '')
        
        # Map timeframe to NonKYC format
        timeframe_map = {
            '1m': '1m',
            '5m': '5m',
            '15m': '15m',
            '30m': '30m',
            '1h': '1h',
            '4h': '4h',
            '1d': '1d',
            '1w': '1w'
        }
        
        result = self._request('GET', f'/public/klines/{pair_formatted}/{timeframe_map.get(timeframe, "1h")}')
        
        candles = []
        if result and not result.get('error'):
            for candle in result:
                try:
                    candles.append([
                        candle.get('time', 0),
                        float(candle.get('open', 0)),
                        float(candle.get('high', 0)),
                        float(candle.get('low', 0)),
                        float(candle.get('close', 0)),
                        float(candle.get('volume', 0))
                    ])
                except:
                    continue
        
        return candles[-limit:] if candles else []
    
    def get_orderbook(self, pair: str, limit: int = 100) -> Dict:
        """Get orderbook for a pair."""
        pair_formatted = pair.replace('/', '')
        result = self._request('GET', f'/public/orderbook/{pair_formatted}')
        
        if result and not result.get('error'):
            return {
                'bids': result.get('bids', [])[:limit],
                'asks': result.get('asks', [])[:limit],
                'timestamp': datetime.now().isoformat()
            }
        return {'bids': [], 'asks': [], 'timestamp': datetime.now().isoformat()}
    
    def get_pairs(self) -> List[str]:
        """Get all available trading pairs."""
        result = self._request('GET', '/public/tickers')
        pairs = []
        
        if result and not result.get('error'):
            for tick in result:
                if tick.get('pair'):
                    # Convert XRP/USD to XRP/USD
                    pairs.append(tick['pair'])
        
        return pairs
    
    # ============================================================
    # PRIVATE METHODS (Require API Key)
    # ============================================================
    
    def get_balances(self) -> Dict[str, BalanceData]:
        """Get account balances."""
        if not self._configured:
            return {"error": "API keys not configured"}
        
        result = self._request('GET', '/balances', private=True)
        
        balances = {}
        if result and not result.get('error'):
            for asset, balance in result.items():
                if isinstance(balance, dict):
                    balances[asset] = BalanceData(
                        asset=asset,
                        free=float(balance.get('free', 0)),
                        locked=float(balance.get('locked', 0)),
                        total=float(balance.get('total', 0)),
                        timestamp=datetime.now().isoformat()
                    )
                else:
                    # Simple balance format
                    balances[asset] = BalanceData(
                        asset=asset,
                        free=float(balance) if isinstance(balance, (int, float)) else 0,
                        locked=0,
                        total=float(balance) if isinstance(balance, (int, float)) else 0,
                        timestamp=datetime.now().isoformat()
                    )
        
        return balances
    
    def create_order(
        self,
        pair: str,
        side: str,  # 'BUY' or 'SELL'
        order_type: str,  # 'LIMIT' or 'MARKET'
        amount: float,
        price: Optional[float] = None
    ) -> Dict:
        """Create a new order."""
        if not self._configured:
            return {"error": "API keys not configured"}
        
        pair_formatted = pair.replace('/', '')
        
        params = {
            'pair': pair_formatted,
            'side': side.upper(),
            'type': order_type.upper(),
            'amount': str(amount)
        }
        
        if price and order_type.upper() == 'LIMIT':
            params['price'] = str(price)
        
        result = self._request('POST', '/order', params, private=True)
        return result
    
    def cancel_order(self, order_id: str) -> Dict:
        """Cancel an existing order."""
        if not self._configured:
            return {"error": "API keys not configured"}
        
        result = self._request('POST', f'/order/cancel/{order_id}', private=True)
        return result
    
    def get_orders(self, pair: Optional[str] = None) -> List[OrderData]:
        """Get all orders."""
        if not self._configured:
            return []
        
        params = {}
        if pair:
            params['pair'] = pair.replace('/', '')
        
        result = self._request('GET', '/orders', params, private=True)
        
        orders = []
        if result and not result.get('error'):
            for order in result:
                try:
                    orders.append(OrderData(
                        order_id=order.get('id', ''),
                        pair=order.get('pair', ''),
                        side=order.get('side', 'BUY'),
                        type=order.get('type', 'MARKET'),
                        price=float(order.get('price', 0)),
                        amount=float(order.get('amount', 0)),
                        filled=float(order.get('filled', 0)),
                        status=order.get('status', 'OPEN'),
                        timestamp=order.get('timestamp', datetime.now().isoformat())
                    ))
                except:
                    continue
        
        return orders
    
    # ============================================================
    # WEBSOCKET (Simplified)
    # ============================================================
    
    def get_websocket_url(self, private: bool = False) -> str:
        """Get WebSocket URL."""
        base = WS_URL
        if private:
            # Private WebSocket requires authentication
            # NonKYC uses query parameters for auth
            timestamp = str(int(time.time() * 1000))
            signature = self._generate_signature({'timestamp': timestamp})
            return f"{base}?X-API-KEY={self.api_key}&timestamp={timestamp}&signature={signature}"
        return base
    
    # ============================================================
    # STATUS
    # ============================================================
    
    def get_status(self) -> Dict:
        """Get client status."""
        return {
            "version": self.VERSION,
            "configured": self._configured,
            "exchange": "nonkyc",
            "public_methods": ["get_ticker", "get_ohlc", "get_orderbook", "get_pairs"],
            "private_methods": ["get_balances", "create_order", "cancel_order", "get_orders"] if self._configured else [],
            "stats": self.stats,
            "timestamp": datetime.now().isoformat()
        }
    
    def test_connection(self) -> bool:
        """Test connection to NonKYC API."""
        try:
            ticker = self.get_ticker('BTC/USD')
            if ticker.price > 0:
                logger.info("✅ NonKYC connection successful")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ NonKYC connection failed: {e}")
            return False

# ============================================================
# SINGLETON INSTANCE
# ============================================================

nonkyc = NonKycClient()

# ============================================================
# BACKWARD COMPATIBILITY (Replace Kraken)
# ============================================================

# For compatibility with existing code that uses 'exchange'
exchange = nonkyc
market_data = nonkyc
KrakenMarketData = NonKycClient

# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "NonKycClient",
    "nonkyc",
    "exchange",
    "market_data",
    "TickerData",
    "BalanceData",
    "OrderData"
]
