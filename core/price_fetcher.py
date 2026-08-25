# core/price_fetcher.py
"""
Simple Price Fetcher from CoinGecko Public API
No API Key Required - Free Public Endpoints
Dengan Caching untuk menghindari Rate Limit
HANYA USDT (Tether) - Tidak menggunakan USD
"""

import requests
import logging
import time
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class PriceFetcher:
    """
    Simple price fetcher from CoinGecko Public API.
    No authentication required - uses public endpoints only.
    Dengan caching 60 detik untuk menghindari rate limit.
    HANYA menggunakan USDT (Tether).
    """
    
    # CoinGecko Public API URLs
    BASE_URL = "https://api.coingecko.com/api/v3"
    PRICE_URL = f"{BASE_URL}/simple/price"
    MARKET_URL = f"{BASE_URL}/coins/markets"
    
    # Cache
    _cache: Dict[str, float] = {}
    _cache_time: Dict[str, float] = {}
    CACHE_DURATION = 60  # Cache selama 60 detik
    
    # Pair mapping (Standard → CoinGecko ID)
    # HANYA USDT PAIRS
    PAIR_MAP = {
        'BTC/USDT': 'bitcoin',
        'ETH/USDT': 'ethereum',
        'SOL/USDT': 'solana',
        'XRP/USDT': 'ripple',
        'ADA/USDT': 'cardano',
        'DOT/USDT': 'polkadot',
        'DOGE/USDT': 'dogecoin',
        'AVAX/USDT': 'avalanche-2',
        'MATIC/USDT': 'matic-network',
        'LINK/USDT': 'chainlink',
        'UNI/USDT': 'uniswap',
        'ATOM/USDT': 'cosmos',
        'BCH/USDT': 'bitcoin-cash',
        'LTC/USDT': 'litecoin',
        'NEAR/USDT': 'near',
        'APT/USDT': 'aptos',
        'ARB/USDT': 'arbitrum',
        'OP/USDT': 'optimism',
        'SUI/USDT': 'sui',
    }
    
    @classmethod
    def _get_coingecko_id(cls, pair: str) -> str:
        """Convert standard pair to CoinGecko ID."""
        return cls.PAIR_MAP.get(pair, pair.split('/')[0].lower())
    
    @classmethod
    def get_price(cls, pair: str = 'BTC/USDT') -> Optional[float]:
        """
        Get current price from CoinGecko dengan caching.
        HANYA untuk USDT pairs.
        
        Args:
            pair: Trading pair (e.g., 'BTC/USDT', 'ETH/USDT')
            
        Returns:
            Current price as float, or None if failed
        """
        # === CEK CACHE ===
        if pair in cls._cache:
            cache_age = time.time() - cls._cache_time.get(pair, 0)
            if cache_age < cls.CACHE_DURATION:
                logger.debug(f"✅ Cache hit for {pair}: ${cls._cache[pair]:,.2f} (age: {cache_age:.1f}s)")
                return cls._cache[pair]
            else:
                logger.debug(f"⏰ Cache expired for {pair} (age: {cache_age:.1f}s)")
        
        # === AMBIL DARI API ===
        try:
            coin_id = cls._get_coingecko_id(pair)
            vs_currency = 'usd'  # CoinGecko menggunakan USD, tapi kita pakai USDT
            
            url = f"{cls.PRICE_URL}?ids={coin_id}&vs_currencies={vs_currency}"
            
            logger.info(f"📊 Fetching price from CoinGecko: {pair}")
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                data = response.json()
                price = data.get(coin_id, {}).get(vs_currency)
                if price:
                    price = float(price)
                    # === SIMPAN KE CACHE ===
                    cls._cache[pair] = price
                    cls._cache_time[pair] = time.time()
                    logger.info(f"✅ Price fetched: {pair} = ${price:,.2f} USDT")
                    return price
                else:
                    logger.error(f"Price not found for {pair}")
                    return None
            elif response.status_code == 429:
                logger.warning(f"⚠️ Rate limit hit for {pair}. Using cached value if available.")
                if pair in cls._cache:
                    logger.info(f"🔄 Using stale cache for {pair}: ${cls._cache[pair]:,.2f}")
                    return cls._cache[pair]
                return None
            else:
                logger.error(f"CoinGecko error: {response.status_code} - {response.text[:200]}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching price for {pair}")
            if pair in cls._cache:
                return cls._cache[pair]
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching price for {pair}: {e}")
            if pair in cls._cache:
                return cls._cache[pair]
            return None
        except Exception as e:
            logger.error(f"Failed to fetch price for {pair}: {e}")
            if pair in cls._cache:
                return cls._cache[pair]
            return None
    
    @classmethod
    def get_prices(cls, pairs: List[str] = None) -> Dict[str, float]:
        """
        Get prices for multiple pairs.
        
        Args:
            pairs: List of trading pairs (default: semua USDT pairs)
            
        Returns:
            Dict of pair → price
        """
        if pairs is None:
            pairs = list(cls.PAIR_MAP.keys())
        
        prices = {}
        for pair in pairs:
            price = cls.get_price(pair)
            if price is not None:
                prices[pair] = price
        
        return prices
    
    @classmethod
    def get_market_data(cls, vs_currency: str = 'usd', limit: int = 10) -> List[Dict]:
        """
        Get market data for top coins.
        
        Args:
            vs_currency: Currency (usd, eur, etc.)
            limit: Number of coins
            
        Returns:
            List of market data
        """
        try:
            url = f"{cls.MARKET_URL}?vs_currency={vs_currency}&order=market_cap_desc&per_page={limit}&page=1&sparkline=false"
            
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"CoinGecko market error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Failed to fetch market data: {e}")
            return []
    
    @classmethod
    def check_connection(cls) -> bool:
        """Check if CoinGecko API is accessible."""
        try:
            response = requests.get(f"{cls.PRICE_URL}?ids=bitcoin&vs_currencies=usd", timeout=5)
            return response.status_code == 200 and 'bitcoin' in response.json()
        except Exception:
            return False
    
    @classmethod
    def clear_cache(cls) -> None:
        """Clear the cache."""
        cls._cache.clear()
        cls._cache_time.clear()
        logger.info("🧹 Cache cleared")
    
    @classmethod
    def get_cache_info(cls) -> Dict:
        """Get cache information."""
        info = {}
        for pair in cls._cache:
            age = time.time() - cls._cache_time.get(pair, 0)
            info[pair] = {
                'price': cls._cache[pair],
                'age_seconds': round(age, 1),
                'expired': age > cls.CACHE_DURATION
            }
        return info


# ============================================================
# GLOBAL INSTANCE
# ============================================================

price_fetcher = PriceFetcher()


# ============================================================
# TEST FUNCTION
# ============================================================

def self_test():
    """Test the price fetcher."""
    print("\n" + "=" * 60)
    print("  PRICE FETCHER - CoinGecko PUBLIC API TEST")
    print("  HANYA USDT PAIRS")
    print("=" * 60)
    
    # Test connection
    connected = PriceFetcher.check_connection()
    print(f"\n🔗 Connection: {'✅ OK' if connected else '❌ FAILED'}")
    
    if not connected:
        print("\n⚠️ Cannot connect to CoinGecko API. Please check internet.")
        return
    
    # Clear cache untuk test
    PriceFetcher.clear_cache()
    
    # Test single price - HANYA USDT
    print("\n📊 Fetching USDT prices from CoinGecko...")
    pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT', 'DOT/USDT']
    
    for pair in pairs:
        price = PriceFetcher.get_price(pair)
        if price:
            print(f"  ✅ {pair}: ${price:,.2f} USDT")
        else:
            print(f"  ❌ {pair}: Failed")
    
    # Test cache
    print("\n📊 Testing cache (second call should be instant)...")
    for pair in pairs[:3]:
        price = PriceFetcher.get_price(pair)
        if price:
            print(f"  ✅ {pair}: ${price:,.2f} USDT (from cache)")
    
    # Cache info
    print("\n📊 Cache Info:")
    cache_info = PriceFetcher.get_cache_info()
    for pair, info in cache_info.items():
        status = "✅" if not info['expired'] else "⏰"
        print(f"  {status} {pair}: ${info['price']:,.2f} USDT (age: {info['age_seconds']}s)")
    
    print("\n" + "=" * 60)
    print("  ✅ TEST COMPLETE")
    print("=" * 60)


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "PriceFetcher",
    "price_fetcher",
    "self_test",
]


# ============================================================
# END
# ============================================================
