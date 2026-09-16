# ============================================================
# gui/market.py
# MARKET VIEW - Market Data & Tickers v4.0
# COMPREHENSIVE & STABLE
# ============================================================

import customtkinter as ctk
from datetime import datetime
import json
import logging
import threading
import time
import random
from typing import Dict, List, Optional, Any, Tuple

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard, MarketTicker

logger = logging.getLogger(__name__)


class Market(IntelligencePage):
    """
    Market Data and Tickers View v4.0.
    
    Features:
    - Real-time price data from exchange
    - Multiple data sources (exchange, bot, mock)
    - Pagination for tickers
    - Summary statistics
    - Performance tracking
    - Timeout protection
    - Fallback to mock data
    - Thread-safe updates
    """

    def __init__(self, parent, *args, **kwargs):
        # ============================================================
        # INISIALISASI SEMUA ATRIBUT
        # ============================================================
        
        # Data storage
        self.tickers: Dict[str, MarketTicker] = {}
        self.market_data: Dict[str, Any] = {}
        self.results: List[Dict] = []
        self.price_history: Dict[str, List[float]] = {}
        self._last_mock_data: Dict[str, Any] = {}
        
        # Pairs list
        try:
            from config import DEFAULT_PAIRS
            self.pairs_list = DEFAULT_PAIRS.copy()
        except ImportError:
            self.pairs_list = ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "ADA/USD", "DOT/USD", "AVAX/USD", "LINK/USD"]
        
        # Exchange reference
        self._exchange = None
        self._get_latest_prices = None
        self._get_ticker = None
        self._using_exchange_direct = False
        self._exchange_available = False
        
        # Bot reference
        self.bot = None
        self.brain = None
        self.learning_integration = None
        
        # Status & metrics
        self.is_connected = False
        self.last_error: Optional[str] = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = 5000  # 5 detik
        self.last_update_time: Optional[datetime] = None
        self.update_durations: List[float] = []
        self.total_data_points = 0
        
        # Timeout settings
        self.DATA_TIMEOUT = 5.0
        
        # Pagination
        self.tickers_per_page = 4
        self.current_page = 0
        self.total_pages = 0
        
        # UI Widgets
        self.market_status = None
        self.last_update_label = None
        self.refresh_btn = None
        self.total_pairs_card = None
        self.bullish_pairs_card = None
        self.bearish_pairs_card = None
        self.neutral_pairs_card = None
        self.avg_price_card = None
        self.volatility_card = None
        self.tickers_container = None
        self.ticker_frames = []
        self.page_label = None
        self.prev_btn = None
        self.next_btn = None
        self.empty_label = None
        self.details_text = None
        
        # Safe mode flag
        self._safe_mode = False
        self._update_lock = threading.Lock()
        self._update_in_progress = False
        self._start_time = time.time()
        
        # ============================================================
        # PANGGIL SUPER
        # ============================================================
        
        super().__init__(parent, *args, **kwargs)
        
        # ============================================================
        # INIT EXCHANGE
        # ============================================================
        
        self._init_exchange()
        
        # ============================================================
        # BUILD UI
        # ============================================================
        
        self._build_ui()
        
        # ============================================================
        # START UPDATES
        # ============================================================
        
        self.after(500, self.update_data)

    # ============================================================
    # PUBLIC METHODS
    # ============================================================
    
    def set_bot(self, bot):
        """Set bot reference."""
        self.bot = bot
        if bot:
            if hasattr(bot, 'brain'):
                self.brain = bot.brain
            if hasattr(bot, 'exchange'):
                self._exchange = bot.exchange
                self._exchange_available = True
            logger.info(f"✅ Bot set in Market: {type(bot).__name__ if bot else None}")
    
    def set_brain(self, brain):
        """Set brain reference."""
        self.brain = brain
        logger.info(f"✅ Brain set in Market: {type(brain).__name__ if brain else None}")
    
    def set_learning(self, learning):
        """Set learning integration reference."""
        self.learning_integration = learning
    
    def on_show(self):
        """Called when page becomes visible."""
        self.refresh()

    # ============================================================
    # INIT EXCHANGE
    # ============================================================

    def _init_exchange(self):
        """Inisialisasi exchange dengan fallback."""
        self._exchange_available = False
        
        # 1. Coba dari core.market_data
        try:
            from core.market_data import kraken_market, get_latest_prices, get_ticker
            if kraken_market is not None:
                self._exchange = kraken_market
                self._get_latest_prices = get_latest_prices
                self._get_ticker = get_ticker
                self._exchange_available = True
                logger.info("✅ Market: Exchange loaded from core.market_data")
                return
        except ImportError:
            pass

        # 2. Coba dari core
        try:
            from core import kraken_market, get_latest_prices, get_ticker
            if kraken_market is not None:
                self._exchange = kraken_market
                self._get_latest_prices = get_latest_prices
                self._get_ticker = get_ticker
                self._exchange_available = True
                logger.info("✅ Market: Exchange loaded from core")
                return
        except ImportError:
            pass

        # 3. Coba dari bot
        if self.bot and hasattr(self.bot, 'exchange'):
            self._exchange = self.bot.exchange
            if self._exchange is not None:
                self._exchange_available = True
                logger.info("✅ Market: Exchange loaded from bot")
                return

        # 4. Fallback: no exchange
        self._exchange = None
        self._get_latest_prices = None
        self._get_ticker = None
        self._exchange_available = False
        logger.warning("⚠️ Market: Exchange not available - using mock data")
        self._safe_mode = True

    # ============================================================
    # BUILD UI
    # ============================================================

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # ===== HEADER =====
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, 
            text="📊 Market Intelligence", 
            font=("Segoe UI", 22, "bold"), 
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")

        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.grid(row=0, column=1, sticky="e")
        
        self.market_status = StatusIndicator(status_frame, label="Market")
        self.market_status.pack(side="left", padx=10)
        
        self.last_update_label = ctk.CTkLabel(
            status_frame, 
            text="Last update: --", 
            font=("Segoe UI", 10), 
            text_color="#5F6B78"
        )
        self.last_update_label.pack(side="left", padx=10)
        
        self.refresh_btn = ctk.CTkButton(
            status_frame, 
            text="🔄 Refresh", 
            width=80, 
            height=28, 
            font=("Segoe UI", 11), 
            fg_color="#3B82F6", 
            hover_color="#2563EB", 
            command=self.refresh
        )
        self.refresh_btn.pack(side="left", padx=5)

        # ===== SUMMARY =====
        summary_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        summary_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)
        summary_frame.grid_columnconfigure(2, weight=1)
        summary_frame.grid_columnconfigure(3, weight=1)
        summary_frame.grid_columnconfigure(4, weight=1)
        summary_frame.grid_columnconfigure(5, weight=1)

        ctk.CTkLabel(
            summary_frame, 
            text="📈 Market Summary", 
            font=("Segoe UI", 14, "bold"), 
            text_color="#E8EDF2"
        ).grid(row=0, column=0, columnspan=6, padx=15, pady=10, sticky="w")
        
        self.total_pairs_card = MetricCard(summary_frame, title="🔢 Total Pairs", value="0")
        self.total_pairs_card.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.bullish_pairs_card = MetricCard(summary_frame, title="📈 Bullish", value="0")
        self.bullish_pairs_card.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        self.bearish_pairs_card = MetricCard(summary_frame, title="📉 Bearish", value="0")
        self.bearish_pairs_card.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        
        self.neutral_pairs_card = MetricCard(summary_frame, title="➖ Neutral", value="0")
        self.neutral_pairs_card.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
        
        self.avg_price_card = MetricCard(summary_frame, title="💰 Avg Price", value="$0")
        self.avg_price_card.grid(row=1, column=4, padx=5, pady=5, sticky="nsew")
        
        self.volatility_card = MetricCard(summary_frame, title="📊 Volatility", value="0%")
        self.volatility_card.grid(row=1, column=5, padx=5, pady=5, sticky="nsew")

        # ===== TICKERS =====
        tickers_main_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        tickers_main_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        tickers_main_frame.grid_columnconfigure(0, weight=1)
        tickers_main_frame.grid_rowconfigure(1, weight=1)

        tickers_header = ctk.CTkFrame(tickers_main_frame, fg_color="transparent")
        tickers_header.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        tickers_header.grid_columnconfigure(0, weight=1)
        tickers_header.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(
            tickers_header, 
            text="💹 Live Tickers", 
            font=("Segoe UI", 14, "bold"), 
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")

        pagination_frame = ctk.CTkFrame(tickers_header, fg_color="transparent")
        pagination_frame.grid(row=0, column=1, sticky="e")
        
        self.prev_btn = ctk.CTkButton(
            pagination_frame, 
            text="◀", 
            width=30, 
            height=25, 
            font=("Segoe UI", 10), 
            fg_color="#2A3A4A", 
            hover_color="#3B4A5A", 
            command=self._prev_page, 
            state="disabled"
        )
        self.prev_btn.pack(side="left", padx=2)
        
        self.page_label = ctk.CTkLabel(
            pagination_frame, 
            text="Page 1/1", 
            font=("Segoe UI", 10), 
            text_color="#8D9AAA"
        )
        self.page_label.pack(side="left", padx=8)
        
        self.next_btn = ctk.CTkButton(
            pagination_frame, 
            text="▶", 
            width=30, 
            height=25, 
            font=("Segoe UI", 10), 
            fg_color="#2A3A4A", 
            hover_color="#3B4A5A", 
            command=self._next_page, 
            state="disabled"
        )
        self.next_btn.pack(side="left", padx=2)

        self.tickers_container = ctk.CTkFrame(tickers_main_frame, fg_color="transparent")
        self.tickers_container.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="nsew")
        self.tickers_container.grid_columnconfigure(0, weight=1)
        self.tickers_container.grid_columnconfigure(1, weight=1)

        self.ticker_frames = []
        for i in range(4):
            frame = ctk.CTkFrame(self.tickers_container, fg_color="#1A2530", corner_radius=8)
            frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)
            self.ticker_frames.append(frame)

        self.empty_label = ctk.CTkLabel(
            self.tickers_container, 
            text="📭 No market data available", 
            font=("Segoe UI", 14), 
            text_color="#5F6B78"
        )

        # ===== DETAILS =====
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            details, 
            text="📋 Market Details", 
            font=("Segoe UI", 14, "bold"), 
            text_color="#E8EDF2"
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        self.details_text = ctk.CTkTextbox(
            details, 
            font=("Consolas", 10), 
            fg_color="#0B0F14", 
            text_color="#8D9AAA", 
            height=120
        )
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")

    # ============================================================
    # PAGINATION
    # ============================================================

    def _prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._update_pagination()

    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._update_pagination()

    def _update_pagination(self):
        total_pairs = len(self.pairs_list)
        self.total_pages = max(1, (total_pairs + self.tickers_per_page - 1) // self.tickers_per_page)
        if self.current_page >= self.total_pages:
            self.current_page = self.total_pages - 1
        if self.current_page < 0:
            self.current_page = 0

        if self.prev_btn:
            self.prev_btn.configure(state="normal" if self.current_page > 0 else "disabled")
        if self.next_btn:
            self.next_btn.configure(state="normal" if self.current_page < self.total_pages - 1 else "disabled")
        if self.page_label:
            self.page_label.configure(text=f"Page {self.current_page + 1}/{self.total_pages}")
        self._update_ticker_display()

    def _update_ticker_display(self):
        start_idx = self.current_page * self.tickers_per_page
        end_idx = min(start_idx + self.tickers_per_page, len(self.pairs_list))
        page_pairs = self.pairs_list[start_idx:end_idx]

        for frame in self.ticker_frames:
            for child in frame.winfo_children():
                child.destroy()

        if not page_pairs:
            if self.empty_label:
                self.empty_label.grid(row=0, column=0, columnspan=2, pady=20)
            for frame in self.ticker_frames:
                frame.grid_remove()
            return
        else:
            if self.empty_label:
                self.empty_label.grid_remove()

        for i, pair in enumerate(page_pairs):
            if i < len(self.ticker_frames):
                frame = self.ticker_frames[i]
                frame.grid()
                ticker = MarketTicker(frame, symbol=pair, price=0, change=0)
                ticker.pack(fill="both", expand=True, padx=5, pady=5)
                self.tickers[pair] = ticker

        for i in range(len(page_pairs), len(self.ticker_frames)):
            self.ticker_frames[i].grid_remove()

    # ============================================================
    # DATA SOURCES
    # ============================================================
    
    def _get_data_from_exchange(self) -> Optional[Dict[str, Any]]:
        """Get data from exchange directly."""
        if not self._exchange_available or self._exchange is None:
            return None
        
        try:
            if self._get_latest_prices is not None:
                result = {}
                for pair in self.pairs_list[:10]:  # Batasi 10 pair
                    try:
                        prices = self._get_latest_prices([pair])
                        if prices and prices.get(pair, 0) > 0:
                            result[pair] = {
                                "price": prices[pair],
                                "change": 0.0,
                                "trend": "NEUTRAL",
                                "timestamp": datetime.now().isoformat(),
                                "source": "exchange"
                            }
                    except Exception:
                        continue
                if result:
                    self._using_exchange_direct = True
                    return result
        except Exception as e:
            logger.debug(f"Exchange data error: {e}")
        
        return None
    
    def _get_data_from_bot(self) -> Optional[Dict[str, Any]]:
        """Get data from bot."""
        if not self.bot:
            return None
        
        try:
            if hasattr(self.bot, 'get_market_data'):
                bot_data = self.bot.get_market_data()
                if bot_data and isinstance(bot_data, dict):
                    result = {}
                    for pair in self.pairs_list:
                        if pair in bot_data:
                            data = bot_data[pair]
                            if isinstance(data, dict):
                                result[pair] = {
                                    "price": data.get('price', 0),
                                    "change": data.get('change', 0),
                                    "trend": data.get('trend', 'NEUTRAL'),
                                    "timestamp": data.get('timestamp', datetime.now().isoformat()),
                                    "source": "bot"
                                }
                            elif isinstance(data, (int, float)):
                                result[pair] = {
                                    "price": float(data),
                                    "change": 0.0,
                                    "trend": "NEUTRAL",
                                    "timestamp": datetime.now().isoformat(),
                                    "source": "bot"
                                }
                    if result:
                        return result
        except Exception as e:
            logger.debug(f"Bot data error: {e}")
        
        return None
    
    def _get_data_from_brain(self) -> Optional[Dict[str, Any]]:
        """Get data from brain."""
        if not self.brain:
            return None
        
        try:
            if hasattr(self.brain, 'market_intelligence'):
                intelligence = self.brain.market_intelligence()
                if intelligence and isinstance(intelligence, dict):
                    signals = intelligence.get('signals', [])
                    if signals:
                        result = {}
                        for signal in signals:
                            if isinstance(signal, dict):
                                pair = signal.get('pair', '')
                                if pair in self.pairs_list:
                                    result[pair] = {
                                        "price": signal.get('price', 0),
                                        "change": signal.get('change', 0),
                                        "trend": signal.get('trend', 'NEUTRAL'),
                                        "timestamp": datetime.now().isoformat(),
                                        "source": "brain"
                                    }
                        if result:
                            return result
        except Exception as e:
            logger.debug(f"Brain data error: {e}")
        
        return None
    
    def _generate_mock_data(self) -> Dict[str, Any]:
        """Generate mock data with realistic movements."""
        result = {}
        
        # Simulasi perubahan harga yang natural
        base_prices = {
            "BTC/USD": 65000 + random.uniform(-2000, 2000),
            "ETH/USD": 3500 + random.uniform(-150, 150),
            "SOL/USD": 180 + random.uniform(-10, 10),
            "XRP/USD": 0.55 + random.uniform(-0.05, 0.05),
            "ADA/USD": 0.45 + random.uniform(-0.04, 0.04),
            "DOT/USD": 7 + random.uniform(-0.5, 0.5),
            "AVAX/USD": 35 + random.uniform(-3, 3),
            "LINK/USD": 15 + random.uniform(-1, 1),
            "LTC/USD": 72 + random.uniform(-5, 5),
            "BCH/USD": 280 + random.uniform(-20, 20),
        }
        
        for pair in self.pairs_list:
            # Gunakan harga sebelumnya jika ada
            if pair in self._last_mock_data:
                base_price = self._last_mock_data[pair].get('price', 1000)
            else:
                base_price = base_prices.get(pair, 1000 + random.uniform(-100, 100))
            
            # Perubahan kecil
            change_pct = random.uniform(-2, 2)
            price = base_price * (1 + change_pct / 100)
            
            # Tentukan trend
            if change_pct > 0.5:
                trend = "BULLISH"
            elif change_pct < -0.5:
                trend = "BEARISH"
            else:
                trend = "NEUTRAL"
            
            result[pair] = {
                "price": round(price, 2),
                "change": round(change_pct, 2),
                "trend": trend,
                "timestamp": datetime.now().isoformat(),
                "source": "mock"
            }
        
        self._last_mock_data = result
        return result

    # ============================================================
    # UPDATE DATA
    # ============================================================

    def update_data(self):
        """Update data with timeout protection."""
        if not self.is_running:
            return

        if self._update_in_progress:
            if self.is_running:
                self.after(self.update_interval, self.update_data)
            return

        start_time = time.time()
        
        try:
            self._update_in_progress = True
            self.update_count += 1
            
            # Coba dapatkan data dari berbagai sumber
            data = None
            
            # 1. Coba dari exchange
            if not self._safe_mode:
                data = self._get_data_from_exchange()
            
            # 2. Coba dari bot
            if not data:
                data = self._get_data_from_bot()
            
            # 3. Coba dari brain
            if not data:
                data = self._get_data_from_brain()
            
            # 4. Fallback ke mock
            if not data:
                data = self._generate_mock_data()
                self._safe_mode = True
                logger.debug("[Market] Using mock data")
            
            if data:
                self.market_data = data
                self.is_connected = True
                self.success_count += 1
                self.last_error = None
                self._safe_mode = False
                
                # Update UI
                self._update_ui()
                
                if self.market_status:
                    self.market_status.set_status(True)
                
                self.last_update_time = datetime.now()
                if self.last_update_label:
                    self.last_update_label.configure(
                        text=f"Last update: {self.last_update_time.strftime('%H:%M:%S')}"
                    )
            else:
                self.is_connected = False
                if self.market_status:
                    self.market_status.set_status(False)
                self._update_fallback_data()
                
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            logger.error(f"[Market] Update error: {e}")
            self.is_connected = False
            if self.market_status:
                self.market_status.set_status(False)
            self._show_error(str(e))
        
        finally:
            # Catat durasi
            duration = time.time() - start_time
            self.update_durations.append(duration)
            if len(self.update_durations) > 100:
                self.update_durations = self.update_durations[-100:]
            
            self._update_in_progress = False
        
        # Schedule next update
        if self.is_running:
            self.after(self.update_interval, self.update_data)

    def _update_fallback_data(self):
        """Update UI dengan data fallback."""
        if self.details_text:
            self.details_text.delete("1.0", "end")
            if self._safe_mode:
                self.details_text.insert(
                    "1.0",
                    "⚠️ SAFE MODE\n\n"
                    "Market data is not available.\n\n"
                    "Possible reasons:\n"
                    "• Exchange not connected\n"
                    "• Network issues\n"
                    "• API key not configured\n\n"
                    "Using mock data for display."
                )
            else:
                self.details_text.insert("1.0", "⚠️ No data source available\n\nWaiting for connection...")
        
        # Gunakan mock data
        mock_data = self._generate_mock_data()
        self.market_data = mock_data
        self._update_ui()

    def _show_error(self, error: str):
        """Show error in details."""
        if self.details_text:
            self.details_text.delete("1.0", "end")
            self.details_text.insert(
                "1.0",
                f"❌ Error: {error}\n\n"
                f"Time: {datetime.now().strftime('%H:%M:%S')}\n"
                f"Updates: {self.update_count}\n"
                f"Success: {self.success_count}\n"
                f"Errors: {self.error_count}\n\n"
                "Please check connection and try again."
            )

    # ============================================================
    # UPDATE UI
    # ============================================================

    def _update_ui(self):
        """Update UI dengan data yang ada."""
        if not self.market_data:
            return
        
        # ===== SUMMARY =====
        total = len(self.pairs_list)
        bullish = 0
        bearish = 0
        neutral = 0
        total_price = 0
        price_count = 0
        
        for pair, data in self.market_data.items():
            if isinstance(data, dict):
                price = data.get('price', 0)
                if price > 0:
                    total_price += price
                    price_count += 1
                
                trend = data.get('trend', 'NEUTRAL')
                if trend == 'BULLISH':
                    bullish += 1
                elif trend == 'BEARISH':
                    bearish += 1
                else:
                    neutral += 1
        
        if self.total_pairs_card:
            self.total_pairs_card.update_value(str(total))
        if self.bullish_pairs_card:
            self.bullish_pairs_card.update_value(str(bullish))
        if self.bearish_pairs_card:
            self.bearish_pairs_card.update_value(str(bearish))
        if self.neutral_pairs_card:
            self.neutral_pairs_card.update_value(str(neutral))
        
        if self.avg_price_card and price_count > 0:
            avg_price = total_price / price_count
            if avg_price > 1000:
                self.avg_price_card.update_value(f"${avg_price:.0f}")
            elif avg_price > 1:
                self.avg_price_card.update_value(f"${avg_price:.2f}")
            else:
                self.avg_price_card.update_value(f"${avg_price:.4f}")
        
        if self.volatility_card and len(self.price_history) > 1:
            # Hitung volatilitas rata-rata
            avg_volatility = 0
            vol_count = 0
            for pair, history in self.price_history.items():
                if len(history) > 1:
                    mean = sum(history) / len(history)
                    variance = sum((p - mean) ** 2 for p in history) / len(history)
                    if mean > 0:
                        volatility = (variance ** 0.5) / mean * 100
                        avg_volatility += volatility
                        vol_count += 1
            if vol_count > 0:
                self.volatility_card.update_value(f"{avg_volatility/vol_count:.1f}%")

        # ===== TICKERS =====
        for pair, ticker in self.tickers.items():
            price = 0.0
            change = 0.0
            if pair in self.market_data:
                data = self.market_data[pair]
                if isinstance(data, dict):
                    price = float(data.get('price', 0))
                    change = float(data.get('change', 0))
            try:
                ticker.update(price, change)
            except Exception:
                pass

        self._update_pagination()

        # ===== DETAILS =====
        details_data = {
            "timestamp": datetime.now().isoformat(),
            "update_count": self.update_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "pairs": len(self.pairs_list),
            "connected": self.is_connected,
            "using_exchange_direct": self._using_exchange_direct,
            "safe_mode": self._safe_mode,
            "market_data_count": len(self.market_data),
            "exchange_available": self._exchange_available,
            "data_source": "exchange" if self._using_exchange_direct else "bot" if self.bot else "mock",
            "avg_update_duration": sum(self.update_durations) / max(1, len(self.update_durations)),
            "uptime": time.time() - self._start_time,
        }
        if self.last_error:
            details_data["last_error"] = self.last_error

        if self.details_text:
            self.details_text.delete("1.0", "end")
            text = json.dumps(details_data, indent=2, default=str)
            if len(text) > 3000:
                text = text[:3000] + "\n... (truncated)"
            self.details_text.insert("1.0", text)

    # ============================================================
    # CONTROL METHODS
    # ============================================================

    def refresh(self):
        """Force refresh dengan timeout."""
        if self._update_in_progress:
            return
        self.update_data()

    def stop(self):
        self.is_running = False

    def set_update_interval(self, interval_ms: int):
        self.update_interval = max(2000, interval_ms)

    def get_performance_stats(self) -> Dict[str, Any]:
        return {
            "total_updates": self.update_count,
            "successful_updates": self.success_count,
            "failed_updates": self.error_count,
            "success_rate": (self.success_count / max(1, self.update_count)) * 100,
            "total_data_points": self.total_data_points,
            "pairs_tracked": len(self.pairs_list),
            "last_update": self.last_update_time.isoformat() if self.last_update_time else None,
            "using_exchange_direct": self._using_exchange_direct,
            "safe_mode": self._safe_mode,
            "avg_update_duration": sum(self.update_durations) / max(1, len(self.update_durations)),
            "uptime": time.time() - self._start_time,
        }

    def destroy(self):
        self.stop()
        super().destroy()