"""
IDX Market Data - Indonesia Stock Exchange
Menggunakan iTick API (free tier) - api-free.itick.org
"""

import json
import logging
import time
import threading
import requests
from typing import Dict, List, Optional, Callable
from datetime import datetime

logger = logging.getLogger(__name__)


class IDXProvider:
    """Provider untuk data saham IDX (Indonesia Stock Exchange)"""
    
    BASE_URL = "https://api-free.itick.org"
    
    # Daftar saham populer IDX
    POPULAR_STOCKS = [
        "BBCA", "BBRI", "TLKM", "BMRI", "ASII", 
        "GOTO", "UNVR", "BBNI", "ADRO", "ICBP", 
        "INKP", "CPIN", "PGAS", "ANTM", "MDKA",
        "TOWR", "EXCL", "ISAT", "TELK", "PGEO",
        "ARTO", "BBYB", "BRIS", "BTPS", "AMMN",
        "BYAN", "ITMG", "HRUM", "DSSA", "ADMR"
    ]
    
    STOCK_NAMES = {
        "BBCA": "Bank Central Asia",
        "BBRI": "Bank Rakyat Indonesia",
        "TLKM": "Telkom Indonesia",
        "BMRI": "Bank Mandiri",
        "ASII": "Astra International",
        "GOTO": "GoTo Gojek Tokopedia",
        "UNVR": "Unilever Indonesia",
        "BBNI": "Bank Negara Indonesia",
        "ADRO": "Adaro Energy",
        "ICBP": "Indofood CBP",
        "INKP": "Indah Kiat Pulp",
        "CPIN": "Charoen Pokphand",
        "PGAS": "Perusahaan Gas Negara",
        "ANTM": "Aneka Tambang",
        "MDKA": "Merdeka Copper Gold",
        "TOWR": "Sarana Menara Nusantara",
        "EXCL": "XL Axiata",
        "ISAT": "Indosat Ooredoo",
        "TELK": "Telkom",
        "PGEO": "Pertamina Geothermal",
        "ARTO": "Bank Jago",
        "BBYB": "Bank Neo Commerce",
        "BRIS": "Bank Syariah Indonesia",
        "BTPS": "Bank Tabungan Pensiunan",
        "AMMN": "Amman Mineral",
        "BYAN": "Bayan Resources",
        "ITMG": "Indo Tambangraya Megah",
        "HRUM": "Harum Energy",
        "DSSA": "Dian Swastatika",
        "ADMR": "Adaro Minerals"
    }
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.prices: Dict[str, float] = {}
        self.quotes: Dict[str, dict] = {}
        self._callbacks: List[Callable] = []
        self.ws = None
        self._running = False
        self._last_request_time = 0
        self._cache: Dict[str, dict] = {}
        self._cache_time: Dict[str, float] = {}
        self.CACHE_TTL = 5  # 5 detik
        
    def is_configured(self) -> bool:
        """Cek apakah API key sudah dikonfigurasi"""
        return bool(self.api_key)
    
    def _should_cache(self, key: str) -> bool:
        if key not in self._cache_time:
            return False
        return (time.time() - self._cache_time[key]) < self.CACHE_TTL
    
    def _cache_get(self, key: str) -> Optional[dict]:
        if self._should_cache(key):
            return self._cache.get(key)
        return None
    
    def _cache_set(self, key: str, value: dict) -> None:
        self._cache[key] = value
        self._cache_time[key] = time.time()
    
    def _request(self, endpoint: str, params: dict = None) -> dict:
        """Melakukan request ke API dengan rate limiting"""
        if not self.is_configured():
            return {"error": "IDX_API_KEY not configured"}
        
        # Rate limiting: 2 request per detik
        elapsed = time.time() - self._last_request_time
        if elapsed < 0.5:
            time.sleep(0.5 - elapsed)
        self._last_request_time = time.time()
        
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            headers = {"token": self.api_key}
            
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()
            
            if data.get("code") == 0 and "data" in data:
                return data
            return {"error": f"API error: {data}"}
            
        except requests.exceptions.Timeout:
            return {"error": "Timeout"}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection error"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_quote(self, code: str) -> dict:
        """Ambil data saham via REST API"""
        cache_key = f"quote_{code.upper()}"
        cached = self._cache_get(cache_key)
        if cached:
            return cached
        
        result = self._request("stock/quote", {"region": "ID", "code": code.upper()})
        
        if "error" in result:
            return result
        
        if result.get("code") == 0 and "data" in result:
            d = result["data"]
            quote = {
                "code": code.upper(),
                "name": self.STOCK_NAMES.get(code.upper(), d.get("n", code)),
                "price": d.get("ld", 0),
                "change": d.get("chp", 0),
                "change_abs": d.get("ch", 0),
                "high": d.get("hi", 0),
                "low": d.get("lo", 0),
                "volume": d.get("vo", 0),
                "open": d.get("op", 0),
                "previous": d.get("pc", 0),
                "timestamp": datetime.now().isoformat(),
                "source": "api"
            }
            self._cache_set(cache_key, quote)
            self.quotes[code.upper()] = quote
            return quote
        
        return {"error": f"No data for {code}"}
    
    def get_all_prices(self) -> Dict[str, float]:
        """Ambil semua harga saham"""
        if not self.is_configured():
            return {}
        
        result = {}
        # Gunakan data dari cache/quote terbaru
        for code in self.POPULAR_STOCKS:
            if code in self.quotes:
                price = self.quotes[code].get("price", 0)
                if price > 0:
                    result[code] = price
            else:
                # Ambil dari API
                quote = self.get_quote(code)
                if "price" in quote and quote["price"] > 0:
                    result[code] = quote["price"]
        
        return result
    
    def get_all_quotes(self) -> Dict[str, dict]:
        """Ambil semua data quote lengkap"""
        if not self.is_configured():
            return {}
        
        result = {}
        for code in self.POPULAR_STOCKS:
            quote = self.get_quote(code)
            if "price" in quote and quote["price"] > 0:
                result[code] = quote
        
        return result
    
    def get_top_gainers(self, limit: int = 5) -> List[dict]:
        """Ambil saham dengan kenaikan tertinggi"""
        quotes = self.get_all_quotes()
        sorted_quotes = sorted(
            [q for q in quotes.values() if q.get("change", 0) > 0],
            key=lambda x: x.get("change", 0),
            reverse=True
        )
        return sorted_quotes[:limit]
    
    def get_top_losers(self, limit: int = 5) -> List[dict]:
        """Ambil saham dengan penurunan terbesar"""
        quotes = self.get_all_quotes()
        sorted_quotes = sorted(
            [q for q in quotes.values() if q.get("change", 0) < 0],
            key=lambda x: x.get("change", 0)
        )
        return sorted_quotes[:limit]
    
    def get_most_active(self, limit: int = 5) -> List[dict]:
        """Ambil saham paling aktif (volume tertinggi)"""
        quotes = self.get_all_quotes()
        sorted_quotes = sorted(
            [q for q in quotes.values() if q.get("volume", 0) > 0],
            key=lambda x: x.get("volume", 0),
            reverse=True
        )
        return sorted_quotes[:limit]
    
    def start_websocket(self, symbols: List[str] = None):
        """Mulai WebSocket streaming IDX"""
        if not self.is_configured():
            logger.warning("IDX_API_KEY not configured, skipping WebSocket")
            return self
        
        if symbols is None:
            symbols = self.POPULAR_STOCKS[:10]
        
        try:
            import websocket
            
            ws_symbols = [f"{s.upper()}$ID" for s in symbols]
            
            def on_message(ws, message):
                try:
                    data = json.loads(message)
                    if "data" in data and data["data"].get("type") == "quote":
                        md = data["data"]
                        code = md.get("s", "").replace("$ID", "")
                        
                        quote = {
                            "code": code,
                            "name": self.STOCK_NAMES.get(code, code),
                            "price": md.get("ld", 0),
                            "change": md.get("chp", 0),
                            "change_abs": md.get("ch", 0),
                            "high": md.get("hi", 0),
                            "low": md.get("lo", 0),
                            "volume": md.get("vo", 0),
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        self.prices[code] = quote["price"]
                        self.quotes[code] = quote
                        
                        # Panggil callbacks
                        for cb in self._callbacks:
                            try:
                                cb(quote)
                            except Exception as e:
                                logger.debug(f"Callback error: {e}")
                except Exception as e:
                    logger.debug(f"IDX WS parse error: {e}")
            
            def on_open(ws):
                ws.send(json.dumps({
                    "action": "subscribe",
                    "symbols": ws_symbols
                }))
                logger.info(f"✅ IDX WebSocket connected: {len(symbols)} symbols")
                self._running = True
            
            def on_close(ws, close_status_code, close_msg):
                logger.info("❌ IDX WebSocket disconnected")
                self._running = False
                # Auto-reconnect after 5 seconds
                if self.api_key and not close_status_code == 1000:
                    threading.Timer(5.0, self.start_websocket, args=[symbols]).start()
            
            self.ws = websocket.WebSocketApp(
                f"{self.BASE_URL}/stock",
                header={"token": self.api_key},
                on_open=on_open,
                on_message=on_message,
                on_close=on_close
            )
            
            threading.Thread(target=self.ws.run_forever, daemon=True).start()
            
        except ImportError:
            logger.warning("websocket library not installed, IDX WebSocket disabled")
        except Exception as e:
            logger.error(f"IDX WebSocket error: {e}")
        
        return self
    
    def stop(self):
        """Stop WebSocket"""
        self._running = False
        if self.ws:
            try:
                self.ws.close()
            except:
                pass
    
    def get_price(self, code: str) -> float:
        """Get single price by code"""
        return self.prices.get(code.upper(), 0)
    
    def get_stock_info(self, code: str) -> dict:
        """Get stock info"""
        return {
            "code": code.upper(),
            "name": self.STOCK_NAMES.get(code.upper(), code)
        }
    
    def on_update(self, callback: Callable):
        """Register callback for price updates"""
        self._callbacks.append(callback)
        return self
    
    def health_check(self) -> dict:
        """Check API health"""
        if not self.is_configured():
            return {
                "status": "NOT_CONFIGURED",
                "message": "IDX_API_KEY not set",
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            test = self.get_quote("BBCA")
            if "error" in test:
                return {
                    "status": "ERROR",
                    "message": test["error"],
                    "timestamp": datetime.now().isoformat()
                }
            return {
                "status": "ONLINE",
                "price": test.get("price", 0),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def clear_cache(self):
        """Clear cache"""
        self._cache.clear()
        self._cache_time.clear()
        logger.info("IDX cache cleared")


# ============================================================
# GLOBAL INSTANCE
# ============================================================

idx_provider = None


def init_idx(api_key: str):
    """Initialize IDX provider with API key"""
    global idx_provider
    idx_provider = IDXProvider(api_key)
    return idx_provider


def get_idx():
    """Get IDX provider instance"""
    return idx_provider


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def get_idx_price(code: str) -> float:
    """Get IDX price by code"""
    if idx_provider:
        return idx_provider.get_price(code)
    return 0


def get_idx_quote(code: str) -> dict:
    """Get IDX quote by code"""
    if idx_provider:
        return idx_provider.get_quote(code)
    return {"error": "IDX not initialized"}


def get_idx_all_prices() -> Dict[str, float]:
    """Get all IDX prices"""
    if idx_provider:
        return idx_provider.get_all_prices()
    return {}


def get_idx_health() -> dict:
    """Get IDX health status"""
    if idx_provider:
        return idx_provider.health_check()
    return {"status": "NOT_INITIALIZED"}


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "IDXProvider",
    "idx_provider",
    "init_idx",
    "get_idx",
    "get_idx_price",
    "get_idx_quote",
    "get_idx_all_prices",
    "get_idx_health"
]
