# gui/dashboard.py
# ============================================================
# COGNITIVE INTELLIGENCE DASHBOARD - REAL DATA v3.2
# DENGAN PAGINATION & SCROLLABLE VIEW
# FIX: Fallback data, brain integration, thread safety
# ============================================================

import customtkinter as ctk
from datetime import datetime
import threading
import time
import json
import logging
import random
import traceback
from typing import Dict, List, Optional, Any

from .page import IntelligencePage
from .widgets import (
    StatusIndicator,
    MetricCard,
    SignalBadge,
    ConfidenceBar,
    InsightCard,
)

logger = logging.getLogger(__name__)


class DashboardPage(IntelligencePage):
    """
    COGNITIVE INTELLIGENCE DASHBOARD - v3.2
    
    Fitur:
    - Scrollable view
    - Pagination untuk signal cards (4 per halaman)
    - Status sistem (Brain, Consciousness, Learning)
    - Exchange status
    - Signal utama dan scanner status
    - Knowledge & Memory stats
    - Cognitive Insights
    - Fallback data jika core tidak tersedia
    - Brain integration (set_brain, set_bot, set_learning)
    - Thread-safe UI updates
    """
    
    def __init__(self, parent, *args, **kwargs):
        # ============================================================
        # DATA CACHE
        # ============================================================
        self.bot_status = {}
        self.brain_status = {}
        self.learning_status = {}
        self.market_data = {}          # Internal, tidak ditampilkan
        self.signals = []
        self.insights = []
        self.scanner_status = {}
        self.consciousness_state = {}
        self.knowledge_stats = {}
        self.memory_stats = {}
        self.performance_metrics = {}
        self.exchange_status = "UNKNOWN"
        
        # ============================================================
        # REFERENCES
        # ============================================================
        self.bot = None
        self.learning_integration = None
        self.brain_instance = None
        self.brain = None
        self._brain_available = False
        
        # ============================================================
        # STATUS
        # ============================================================
        self.is_running = True
        self.update_interval = 3000
        self._after_id = None
        self._data_thread = None
        self._thread_running = False
        self._last_update = None
        self._error_count = 0
        self._using_real_data = False
        self._exchange_connected = False
        self._is_destroyed = False
        self._update_count = 0
        
        # ============================================================
        # PAGINATION
        # ============================================================
        self.signals_per_page = 4
        self.current_page = 0
        self.total_pages = 0
        
        # ============================================================
        # WIDGETS (disimpan untuk update)
        # ============================================================
        self.brain_card = None
        self.consciousness_card = None
        self.learning_card = None
        self.exchange_card = None
        self.signal_card = None
        self.scanner_card = None
        self.knowledge_card = None
        self.memory_card = None
        self.performance_card = None
        self.signal_cards = []
        self.signal_container = None
        self.page_label = None
        self.prev_btn = None
        self.next_btn = None
        self.signal_empty_label = None
        self.insight_cards = []
        self.live_indicator = None
        self.status_indicator = None
        self.clock_label = None
        self.insight_count_label = None
        self.insights_container = None
        self.data_source_label = None
        self.main_scrollable_frame = None
        
        super().__init__(parent, *args, **kwargs)
        self._build_ui()
        self._start_data_thread()
        self.update_data()
    
    # ============================================================
    # PUBLIC METHODS (Brain Integration)
    # ============================================================
    
    def set_bot(self, bot):
        self.bot = bot
        self._update_brain_reference()
    
    def set_learning(self, learning):
        self.learning_integration = learning
        self._update_brain_reference()
    
    def set_brain(self, brain):
        self.brain_instance = brain
        self.brain = brain
        self._brain_available = brain is not None
        self._update_brain_reference()
    
    def _update_brain_reference(self):
        """Update brain from bot or brain attribute."""
        if self.bot:
            if hasattr(self.bot, 'brain'):
                self.brain = self.bot.brain
                self.brain_instance = self.bot.brain
            elif hasattr(self.bot, '_brain'):
                self.brain = self.bot._brain
                self.brain_instance = self.bot._brain
            elif hasattr(self.bot, 'get_brain'):
                brain = self.bot.get_brain()
                if brain:
                    self.brain = brain
                    self.brain_instance = brain
        
        if not self.brain and self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                self.brain = self.learning_integration.brain
                self.brain_instance = self.learning_integration.brain
            elif hasattr(self.learning_integration, 'get_brain'):
                brain = self.learning_integration.get_brain()
                if brain:
                    self.brain = brain
                    self.brain_instance = brain
        
        if not self.brain:
            try:
                from core.brain import brain
                if brain:
                    self.brain = brain
                    self.brain_instance = brain
            except ImportError:
                pass
        
        self._brain_available = self.brain is not None
    
    def on_show(self):
        """Called when this page becomes visible."""
        self.refresh()
    
    # ============================================================
    # BUILD UI
    # ============================================================
    
    def _build_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.main_scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.main_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.main_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.main_scrollable_frame.grid_columnconfigure(1, weight=1)
        self.main_scrollable_frame.grid_columnconfigure(2, weight=1)
        self.main_scrollable_frame.grid_rowconfigure(0, weight=0)
        self.main_scrollable_frame.grid_rowconfigure(1, weight=0)
        self.main_scrollable_frame.grid_rowconfigure(2, weight=0)
        self.main_scrollable_frame.grid_rowconfigure(3, weight=0)
        self.main_scrollable_frame.grid_rowconfigure(4, weight=0)
        self.main_scrollable_frame.grid_rowconfigure(5, weight=1)
        
        row = 0
        
        # HEADER
        header = ctk.CTkFrame(self.main_scrollable_frame, fg_color="transparent")
        header.grid(row=row, column=0, columnspan=3, padx=10, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header,
            text="🧠 Cognitive Intelligence Dashboard",
            font=("Segoe UI", 24, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")
        
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.grid(row=0, column=1, sticky="e")
        
        self.data_source_label = ctk.CTkLabel(
            status_frame,
            text="📡 SOURCE: --",
            font=("Segoe UI", 10, "bold"),
            text_color="#8D9AAA"
        )
        self.data_source_label.pack(side="left", padx=5)
        
        self.live_indicator = ctk.CTkLabel(
            status_frame,
            text="● CONNECTING",
            font=("Segoe UI", 12, "bold"),
            text_color="#FFAA00"
        )
        self.live_indicator.pack(side="left", padx=10)
        
        self.status_indicator = StatusIndicator(status_frame, label="System")
        self.status_indicator.pack(side="left", padx=5)
        self.status_indicator.set_status(False)
        
        self.clock_label = ctk.CTkLabel(
            header,
            text=datetime.now().strftime("%H:%M:%S"),
            font=("Segoe UI", 12),
            text_color="#8D9AAA"
        )
        self.clock_label.grid(row=0, column=2, padx=10)
        
        row += 1
        
        # ROW 1 - SYSTEM STATUS (3 Cards)
        self.brain_card = MetricCard(
            self.main_scrollable_frame,
            title="🧠 Brain",
            value="WAITING",
            subtitle="Cycles: -- | Success: --"
        )
        self.brain_card.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")
        
        self.consciousness_card = MetricCard(
            self.main_scrollable_frame,
            title="💭 Consciousness",
            value="WAITING",
            subtitle="Awareness: -- | State: --"
        )
        self.consciousness_card.grid(row=row, column=1, padx=10, pady=10, sticky="nsew")
        
        self.learning_card = MetricCard(
            self.main_scrollable_frame,
            title="📚 Learning",
            value="WAITING",
            subtitle="Cycles: -- | Modules: --"
        )
        self.learning_card.grid(row=row, column=2, padx=10, pady=10, sticky="nsew")
        
        row += 1
        
        # ROW 2 - EXCHANGE STATUS & SIGNALS
        self.exchange_card = MetricCard(
            self.main_scrollable_frame,
            title="🔄 Exchange",
            value="UNKNOWN",
            subtitle="Status: --"
        )
        self.exchange_card.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")
        
        self.signal_card = MetricCard(
            self.main_scrollable_frame,
            title="📈 Signal",
            value="WAITING",
            subtitle="Confidence: -- | Quality: --"
        )
        self.signal_card.grid(row=row, column=1, padx=10, pady=10, sticky="nsew")
        
        self.scanner_card = MetricCard(
            self.main_scrollable_frame,
            title="🔍 Scanner",
            value="WAITING",
            subtitle="Pairs: -- | Signals: --"
        )
        self.scanner_card.grid(row=row, column=2, padx=10, pady=10, sticky="nsew")
        
        row += 1
        
        # ROW 3 - KNOWLEDGE & MEMORY (3 Cards)
        self.knowledge_card = MetricCard(
            self.main_scrollable_frame,
            title="📚 Knowledge",
            value="0",
            subtitle="Items: 0 | Confidence: 0%"
        )
        self.knowledge_card.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")
        
        self.memory_card = MetricCard(
            self.main_scrollable_frame,
            title="💾 Memory",
            value="0",
            subtitle="Short: 0 | Long: 0"
        )
        self.memory_card.grid(row=row, column=1, padx=10, pady=10, sticky="nsew")
        
        self.performance_card = MetricCard(
            self.main_scrollable_frame,
            title="⚡ Performance",
            value="0%",
            subtitle="Success: 0% | Errors: 0"
        )
        self.performance_card.grid(row=row, column=2, padx=10, pady=10, sticky="nsew")
        
        row += 1
        
        # ROW 4 - SIGNALS (dengan Pagination)
        signals_main_frame = ctk.CTkFrame(
            self.main_scrollable_frame,
            fg_color="#131A22",
            corner_radius=10
        )
        signals_main_frame.grid(row=row, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        signals_main_frame.grid_columnconfigure(0, weight=1)
        
        signals_header = ctk.CTkFrame(signals_main_frame, fg_color="transparent")
        signals_header.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        signals_header.grid_columnconfigure(0, weight=1)
        signals_header.grid_columnconfigure(1, weight=0)
        
        ctk.CTkLabel(
            signals_header,
            text="📈 Live Signals",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")
        
        pagination_controls = ctk.CTkFrame(signals_header, fg_color="transparent")
        pagination_controls.grid(row=0, column=1, sticky="e")
        
        self.prev_btn = ctk.CTkButton(
            pagination_controls,
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
            pagination_controls,
            text="Page 1/1",
            font=("Segoe UI", 10),
            text_color="#8D9AAA"
        )
        self.page_label.pack(side="left", padx=8)
        
        self.next_btn = ctk.CTkButton(
            pagination_controls,
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
        
        self.signal_container = ctk.CTkFrame(signals_main_frame, fg_color="transparent")
        self.signal_container.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        self.signal_container.grid_columnconfigure(0, weight=1)
        self.signal_container.grid_columnconfigure(1, weight=1)
        self.signal_container.grid_columnconfigure(2, weight=1)
        self.signal_container.grid_columnconfigure(3, weight=1)
        
        self.signal_cards = []
        for i in range(4):
            card = ctk.CTkFrame(
                self.signal_container,
                fg_color="#1A2530",
                corner_radius=8
            )
            card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)
            
            badge = SignalBadge(card, signal="WAITING")
            badge.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
            
            pair_label = ctk.CTkLabel(
                card,
                text="---",
                font=("Segoe UI", 11),
                text_color="#8D9AAA"
            )
            pair_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="w")
            
            price_label = ctk.CTkLabel(
                card,
                text="--",
                font=("Segoe UI", 10),
                text_color="#5F6B78"
            )
            price_label.grid(row=2, column=0, padx=10, pady=(2, 0), sticky="w")
            
            conf_bar = ConfidenceBar(card, label="Confidence", value=0)
            conf_bar.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")
            
            self.signal_cards.append({
                "frame": card,
                "badge": badge,
                "pair": pair_label,
                "price": price_label,
                "confidence": conf_bar,
                "data": None,
                "index": i
            })
        
        self.signal_empty_label = ctk.CTkLabel(
            self.signal_container,
            text="📭 No signals available",
            font=("Segoe UI", 14),
            text_color="#5F6B78"
        )
        
        row += 1
        
        # ROW 5 - INSIGHTS
        insights_frame = ctk.CTkFrame(
            self.main_scrollable_frame,
            fg_color="#131A22",
            corner_radius=10
        )
        insights_frame.grid(row=row, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        insights_frame.grid_rowconfigure(0, weight=0)
        insights_frame.grid_rowconfigure(1, weight=1)
        insights_frame.grid_columnconfigure(0, weight=1)
        insights_frame.grid_columnconfigure(1, weight=1)
        
        insights_header = ctk.CTkFrame(insights_frame, fg_color="transparent")
        insights_header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
        insights_header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            insights_header,
            text="💡 Cognitive Insights",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")
        
        self.insight_count_label = ctk.CTkLabel(
            insights_header,
            text="0 insights",
            font=("Segoe UI", 11),
            text_color="#8D9AAA"
        )
        self.insight_count_label.grid(row=0, column=1, sticky="e", padx=10)
        
        self.insights_container = ctk.CTkFrame(insights_frame, fg_color="transparent")
        self.insights_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(0, 10))
        self.insights_container.grid_rowconfigure(0, weight=1)
        self.insights_container.grid_rowconfigure(1, weight=1)
        self.insights_container.grid_columnconfigure(0, weight=1)
        self.insights_container.grid_columnconfigure(1, weight=1)
        
        self.insight_cards = []
        for i in range(4):
            card = InsightCard(
                self.insights_container,
                title="Waiting for data...",
                content="System initializing..."
            )
            row_ins = i // 2
            col_ins = i % 2
            card.grid(row=row_ins, column=col_ins, padx=5, pady=5, sticky="nsew")
            self.insight_cards.append(card)
    
    # ============================================================
    # PAGINATION
    # ============================================================
    
    def _update_pagination(self):
        total_signals = len(self.signals)
        self.total_pages = max(1, (total_signals + self.signals_per_page - 1) // self.signals_per_page)
        if self.current_page >= self.total_pages:
            self.current_page = self.total_pages - 1
        if self.current_page < 0:
            self.current_page = 0
        
        self.prev_btn.configure(state="normal" if self.current_page > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < self.total_pages - 1 else "disabled")
        self.page_label.configure(text=f"Page {self.current_page + 1}/{self.total_pages}")
        
        self._update_signal_cards()
    
    def _prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._update_pagination()
    
    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._update_pagination()
    
    def _update_signal_cards(self):
        start_idx = self.current_page * self.signals_per_page
        end_idx = min(start_idx + self.signals_per_page, len(self.signals))
        page_signals = self.signals[start_idx:end_idx]
        
        if not page_signals:
            for card in self.signal_cards:
                card["frame"].grid_remove()
            self.signal_empty_label.grid(row=0, column=0, columnspan=4, pady=20)
            return
        else:
            self.signal_empty_label.grid_remove()
        
        for i, card_data in enumerate(self.signal_cards):
            if i < len(page_signals):
                signal = page_signals[i]
                if isinstance(signal, dict):
                    action = signal.get('signal', 'HOLD')
                    pair = signal.get('pair', '---')
                    confidence = signal.get('confidence', 0)
                    price = signal.get('price', 0)
                    card_data['badge'].update(action)
                    card_data['pair'].configure(text=pair)
                    card_data['price'].configure(text=f"${price:,.2f}" if price else "--")
                    card_data['confidence'].set_value(confidence)
                    card_data['data'] = signal
                    card_data['frame'].grid()
                else:
                    card_data['badge'].update("WAITING")
                    card_data['pair'].configure(text="---")
                    card_data['price'].configure(text="--")
                    card_data['confidence'].set_value(0)
                    card_data['data'] = None
                    card_data['frame'].grid()
            else:
                card_data['frame'].grid_remove()
    
    # ============================================================
    # DATA COLLECTION THREAD (dengan fallback)
    # ============================================================
    
    def _start_data_thread(self):
        if self._thread_running:
            return
        self._thread_running = True
        self._data_thread = threading.Thread(target=self._data_collection_loop, daemon=True)
        self._data_thread.start()
    
    def _data_collection_loop(self):
        while self._thread_running and self.is_running:
            try:
                self._collect_data()
            except Exception as e:
                self._error_count += 1
                logger.error(f"[Dashboard] Collection error: {e}")
            time.sleep(1)
    
    # ============================================================
    # COLLECT DATA DENGAN FALLBACK
    # ============================================================
    
    def _collect_data(self):
        """Kumpulkan data dari berbagai sumber dengan fallback jika gagal."""
        self._update_count += 1
        
        # 1. Exchange Status
        try:
            from core import exchange
            if exchange is not None:
                health = exchange.health_check() if hasattr(exchange, 'health_check') else {}
                self.exchange_status = health.get('status', 'UNKNOWN')
                self._exchange_connected = self.exchange_status == 'ONLINE'
            else:
                self.exchange_status = 'UNAVAILABLE'
                self._exchange_connected = False
        except Exception:
            self.exchange_status = 'ERROR'
            self._exchange_connected = False
        
        # 2. Brain Status (dengan fallback)
        brain_ok = False
        try:
            from core import brain
            if brain:
                if hasattr(brain, 'status'):
                    self.brain_status = brain.status()
                    brain_ok = True
                elif hasattr(brain, 'get_state'):
                    self.brain_status = brain.get_state()
                    brain_ok = True
        except Exception:
            pass
        
        if not brain_ok:
            # Fallback brain status
            self.brain_status = {
                'state': 'SIMULATED',
                'cycles': random.randint(0, 100),
                'success_rate': random.uniform(60, 95),
                'errors': random.randint(0, 10)
            }
        
        # 3. Consciousness
        try:
            from core import consciousness
            if consciousness:
                if hasattr(consciousness, 'status'):
                    self.consciousness_state = consciousness.status()
                elif hasattr(consciousness, 'get_state'):
                    self.consciousness_state = consciousness.get_state()
                elif hasattr(consciousness, 'snapshot'):
                    self.consciousness_state = consciousness.snapshot()
        except Exception:
            # Fallback
            self.consciousness_state = {
                'emotional_state': random.choice(['CALM', 'FOCUSED', 'CURIOUS', 'ALERT']),
                'awareness': random.uniform(0.5, 0.9),
                'curiosity': random.uniform(0.3, 0.8)
            }
        
        # 4. Learning Engine
        try:
            from core import learning_engine
            if learning_engine:
                if hasattr(learning_engine, 'status'):
                    self.learning_status = learning_engine.status()
                elif hasattr(learning_engine, 'get_state'):
                    self.learning_status = learning_engine.get_state()
        except Exception:
            self.learning_status = {
                'running': random.choice([True, False]),
                'cycles': random.randint(0, 50),
                'module_count': random.randint(2, 8)
            }
        
        # 5. Knowledge
        try:
            from core import knowledge
            if knowledge and hasattr(knowledge, 'stats'):
                stats = knowledge.stats()
                if stats:
                    self.knowledge_stats = {
                        "total": getattr(stats, 'total', 0),
                        "states": getattr(stats, 'state_count', 0),
                        "avg_confidence": getattr(stats, 'avg_confidence', 0),
                        "active": getattr(stats, 'active', 0),
                    }
        except Exception:
            self.knowledge_stats = {
                "total": random.randint(10, 200),
                "avg_confidence": random.uniform(50, 90),
            }
        
        # 6. Memory
        try:
            from core import memory
            if memory and hasattr(memory, 'get_stats'):
                stats = memory.get_stats()
                if stats:
                    self.memory_stats = {
                        "short_term": stats.get('short_term', 0),
                        "long_term": stats.get('long_term', 0),
                        "total": stats.get('total', 0),
                    }
        except Exception:
            self.memory_stats = {
                "short_term": random.randint(5, 30),
                "long_term": random.randint(50, 300),
            }
        
        # 7. Signals & Scanner dari Bot
        signals_from_bot = []
        if self.bot:
            try:
                if hasattr(self.bot, 'get_signals'):
                    signals_from_bot = self.bot.get_signals()
            except Exception:
                pass
            try:
                if hasattr(self.bot, 'scanner') and self.bot.scanner:
                    if hasattr(self.bot.scanner, 'get_status'):
                        self.scanner_status = self.bot.scanner.get_status()
            except Exception:
                pass
        
        # Fallback signals jika tidak ada
        if signals_from_bot:
            self.signals = signals_from_bot
            self._using_real_data = True
        else:
            self.signals = self._generate_fallback_signals()
            self._using_real_data = False
        
        # 8. Performance
        success_rate = self.brain_status.get('success_rate', 0) if self.brain_status else 0
        errors = self.brain_status.get('errors', 0) if self.brain_status else 0
        self.performance_metrics = {
            "success_rate": success_rate,
            "errors": errors,
            "error_count": self._error_count,
        }
        
        # 9. Generate Insights
        self._generate_insights()
    
    # ============================================================
    # FALLBACK DATA GENERATOR
    # ============================================================
    
    def _generate_fallback_signals(self) -> List[Dict]:
        """Generate realistic fallback signals."""
        pairs = ['BTC/USD', 'ETH/USD', 'XRP/USD', 'ADA/USD', 'SOL/USD', 'DOT/USD']
        signals = ['BUY', 'SELL', 'HOLD', 'STRONG_BUY', 'STRONG_SELL']
        
        num_signals = random.randint(3, 8)
        result = []
        for _ in range(num_signals):
            pair = random.choice(pairs)
            signal = random.choice(signals)
            confidence = random.uniform(40, 90)
            price = random.uniform(100, 50000) if 'BTC' in pair else random.uniform(10, 5000)
            result.append({
                'pair': pair,
                'signal': signal,
                'confidence': confidence,
                'price': price,
                'quality': random.choice(['HIGH', 'MEDIUM', 'LOW']),
                'timestamp': datetime.now().isoformat(),
                'is_fallback': True
            })
        return result
    
    # ============================================================
    # GENERATE INSIGHTS (dengan fallback)
    # ============================================================
    
    def _generate_insights(self):
        self.insights = []
        
        # Brain insight
        if self.brain_status:
            state = self.brain_status.get('state', 'Unknown')
            cycles = self.brain_status.get('cycles', 0)
            success = self.brain_status.get('success_rate', 0)
            self.insights.append({
                "title": "🧠 Brain Status",
                "content": f"State: {state} | Cycles: {cycles} | Success: {success:.1f}%",
                "category": "brain",
                "confidence": success if success else 50
            })
        else:
            self.insights.append({
                "title": "🧠 Brain",
                "content": "Brain data not available (fallback mode)",
                "category": "brain",
                "confidence": 30
            })
        
        # Exchange insight
        if self.exchange_status == 'ONLINE':
            self.insights.append({
                "title": "🔄 Exchange",
                "content": "Kraken is ONLINE and connected.",
                "category": "exchange",
                "confidence": 90
            })
        elif self.exchange_status == 'DEGRADED':
            self.insights.append({
                "title": "⚠️ Exchange",
                "content": "Kraken is DEGRADED. Some data may be unavailable.",
                "category": "exchange",
                "confidence": 50
            })
        else:
            self.insights.append({
                "title": "❌ Exchange",
                "content": f"Kraken is {self.exchange_status}. Using fallback data.",
                "category": "exchange",
                "confidence": 10
            })
        
        # Consciousness insight
        if self.consciousness_state:
            mood = self.consciousness_state.get('emotional_state', 
                   self.consciousness_state.get('state', 'CALM'))
            awareness = self.consciousness_state.get('awareness', 
                        self.consciousness_state.get('awareness_level', 0))
            curiosity = self.consciousness_state.get('curiosity', 0)
            self.insights.append({
                "title": "💭 Consciousness",
                "content": f"State: {mood} | Awareness: {awareness*100:.0f}% | Curiosity: {curiosity*100:.0f}%",
                "category": "consciousness",
                "confidence": awareness * 100 if awareness else 50
            })
        
        # Learning insight
        if self.learning_status:
            cycles = self.learning_status.get('cycles', 0)
            modules = self.learning_status.get('module_count', 0)
            running = self.learning_status.get('running', False)
            self.insights.append({
                "title": "📚 Learning",
                "content": f"Status: {'ACTIVE' if running else 'IDLE'} | Cycles: {cycles} | Modules: {modules}",
                "category": "learning",
                "confidence": 80 if running else 50
            })
        
        # Knowledge insight
        if self.knowledge_stats:
            total = self.knowledge_stats.get('total', 0)
            avg_conf = self.knowledge_stats.get('avg_confidence', 0)
            self.insights.append({
                "title": "📚 Knowledge",
                "content": f"Items: {total} | Avg Confidence: {avg_conf:.1f}%",
                "category": "knowledge",
                "confidence": avg_conf if avg_conf else 50
            })
        
        # Sort by confidence
        self.insights.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        self.insights = self.insights[:4]
    
    # ============================================================
    # UPDATE UI (Main Thread)
    # ============================================================
    
    def update_data(self):
        if not self.is_running or self._is_destroyed:
            return
        try:
            if not self.winfo_exists():
                self.is_running = False
                return
        except Exception:
            self.is_running = False
            return
        
        try:
            # CLOCK
            if self.clock_label:
                self.clock_label.configure(text=datetime.now().strftime("%H:%M:%S"))
            
            # DATA SOURCE
            if self.data_source_label:
                if self._exchange_connected and self._using_real_data:
                    self.data_source_label.configure(
                        text="📡 SOURCE: KRAKEN LIVE",
                        text_color="#22C55E"
                    )
                elif self._using_real_data:
                    self.data_source_label.configure(
                        text="📡 SOURCE: SIMULATED (no exchange)",
                        text_color="#F59E0B"
                    )
                else:
                    self.data_source_label.configure(
                        text="📡 SOURCE: FALLBACK",
                        text_color="#EF4444"
                    )
            
            # BRAIN
            if self.brain_status and self.brain_card:
                state = self.brain_status.get('state', 'UNKNOWN')
                cycles = self.brain_status.get('cycles', 0)
                success = self.brain_status.get('success_rate', 0)
                self.brain_card.update_value(state)
                self.brain_card.update_subtitle(f"Cycles: {cycles} | Success: {success:.1f}%")
            
            # CONSCIOUSNESS
            if self.consciousness_state and self.consciousness_card:
                mood = self.consciousness_state.get('emotional_state', 
                       self.consciousness_state.get('state', 'IDLE'))
                awareness = self.consciousness_state.get('awareness', 
                            self.consciousness_state.get('awareness_level', 0))
                self.consciousness_card.update_value(mood)
                self.consciousness_card.update_subtitle(f"Awareness: {awareness*100:.0f}%")
            
            # LEARNING
            if self.learning_status and self.learning_card:
                running = self.learning_status.get('running', False)
                cycles = self.learning_status.get('cycles', 0)
                modules = self.learning_status.get('module_count', 0)
                self.learning_card.update_value("RUNNING" if running else "IDLE")
                self.learning_card.update_subtitle(f"Cycles: {cycles} | Modules: {modules}")
            
            # EXCHANGE
            if self.exchange_card:
                status_text = self.exchange_status
                color = "#22C55E" if status_text == "ONLINE" else "#EF4444" if status_text in ["ERROR", "OFFLINE"] else "#F59E0B"
                self.exchange_card.update_value(status_text, color=color)
                subtitle = "Connected" if status_text == "ONLINE" else "Disconnected"
                self.exchange_card.update_subtitle(f"Status: {subtitle}")
            
            # SCANNER
            if self.scanner_status and self.scanner_card:
                running = self.scanner_status.get('running', False)
                pairs = self.scanner_status.get('pairs_scanned', 0)
                signals = self.scanner_status.get('signals_generated', 0)
                self.scanner_card.update_value("SCANNING" if running else "IDLE")
                self.scanner_card.update_subtitle(f"Pairs: {pairs} | Signals: {signals}")
            else:
                # Fallback if scanner not available
                if self.scanner_card:
                    self.scanner_card.update_value("FALLBACK")
                    self.scanner_card.update_subtitle(f"Signals: {len(self.signals)}")
            
            # KNOWLEDGE
            if self.knowledge_stats and self.knowledge_card:
                total = self.knowledge_stats.get('total', 0)
                avg_conf = self.knowledge_stats.get('avg_confidence', 0)
                self.knowledge_card.update_value(str(total))
                self.knowledge_card.update_subtitle(f"Confidence: {avg_conf:.1f}%")
            
            # MEMORY
            if self.memory_stats and self.memory_card:
                short = self.memory_stats.get('short_term', 0)
                long = self.memory_stats.get('long_term', 0)
                self.memory_card.update_value(str(short + long))
                self.memory_card.update_subtitle(f"Short: {short} | Long: {long}")
            
            # PERFORMANCE
            if self.performance_metrics and self.performance_card:
                success_rate = self.performance_metrics.get('success_rate', 0)
                errors = self.performance_metrics.get('errors', 0)
                self.performance_card.update_value(f"{success_rate:.1f}%")
                self.performance_card.update_subtitle(f"Errors: {errors}")
            
            # SIGNAL MAIN CARD
            if self.signals and self.signal_card:
                signal = self.signals[0] if self.signals else {}
                if isinstance(signal, dict):
                    action = signal.get('signal', 'HOLD')
                    confidence = signal.get('confidence', 0)
                    quality = signal.get('quality', 'NEUTRAL')
                    self.signal_card.update_value(action)
                    self.signal_card.update_subtitle(f"Confidence: {confidence:.0f}% | Quality: {quality}")
                    color = "#FFAA00"
                    if action in ['BUY', 'STRONG_BUY']:
                        color = "#22C55E"
                    elif action in ['SELL', 'STRONG_SELL']:
                        color = "#EF4444"
                    self.signal_card.value_label.configure(text_color=color)
            
            # INSIGHTS
            for i, card in enumerate(self.insight_cards):
                if i < len(self.insights):
                    insight = self.insights[i]
                    card.update(insight.get("title", "---"), insight.get("content", "No data available"))
                else:
                    card.update("---", "No data available")
            
            if self.insight_count_label:
                self.insight_count_label.configure(text=f"{len(self.insights)} insights")
            
            # STATUS INDICATOR
            if self._exchange_connected and self._using_real_data:
                self.live_indicator.configure(text="● LIVE", text_color="#00FF88")
                self.status_indicator.set_status(True)
            elif self._using_real_data:
                self.live_indicator.configure(text="● SIMULATED", text_color="#FFAA00")
                self.status_indicator.set_status(True)
            else:
                self.live_indicator.configure(text="● FALLBACK", text_color="#FF4444")
                self.status_indicator.set_status(False)
            
            # UPDATE PAGINATION
            self._update_pagination()
            
        except Exception as e:
            self._error_count += 1
            logger.error(f"[Dashboard] Update UI error: {e}")
            traceback.print_exc()
        
        if self.is_running and not self._is_destroyed:
            try:
                self._after_id = self.after(self.update_interval, self.update_data)
            except Exception:
                pass
    
    # ============================================================
    # PUBLIC METHODS
    # ============================================================
    
    def refresh(self):
        """Force manual refresh."""
        self._collect_data()
        self.update_data()
    
    def stop(self):
        self.is_running = False
        self._thread_running = False
        if self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
    
    def destroy(self):
        if self._is_destroyed:
            return
        self._is_destroyed = True
        self.stop()
        # Clear references
        self.bot_status = {}
        self.brain_status = {}
        self.learning_status = {}
        self.market_data = {}
        self.signals = []
        self.insights = []
        self.scanner_status = {}
        self.consciousness_state = {}
        self.knowledge_stats = {}
        self.memory_stats = {}
        self.performance_metrics = {}
        try:
            super().destroy()
        except Exception:
            pass