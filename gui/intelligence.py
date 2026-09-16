# ============================================================
# INKSIDE DIGITAL TRADING BOT
# GUI INTELLIGENCE PAGES
# COGNITIVE MIRROR ENGINE v5.0
# ============================================================
# 
# FILE INI ADALAH GABUNGAN DARI:
# - page.py, widgets.py, dashboard.py, brain.py, market.py
# - learning.py, memory.py, pattern.py, prediction.py
# - decision.py, reflection.py, health.py, knowledge.py
# - telegram.py, trading.py, settings.py, monitor.py
#
# ============================================================

import logging
import random
import json
import threading
import time
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Callable
from pathlib import Path

import customtkinter as ctk

logger = logging.getLogger(__name__)

# ============================================================
# CONSTANTS
# ============================================================

COLORS = {
    "background": "#0B0F14",
    "sidebar": "#0F141B",
    "panel": "#131A22",
    "panel_light": "#18212B",
    "border": "#26313D",
    "text": "#E8EDF2",
    "text_secondary": "#8D9AAA",
    "text_muted": "#5F6B78",
    "accent": "#3B82F6",
    "accent_hover": "#2563EB",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#06B6D4"
}

FONT_FAMILY = "Segoe UI"


# ============================================================
# WIDGETS
# ============================================================

class StatusIndicator(ctk.CTkFrame):
    """Status indicator with dot and label."""
    
    def __init__(self, parent, label: str = "Status", online_text: str = "ONLINE", offline_text: str = "OFFLINE", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.online_text = online_text
        self.offline_text = offline_text
        
        self.dot = ctk.CTkLabel(self, text="●", font=("Segoe UI", 16), text_color="#22C55E")
        self.dot.pack(side="left", padx=(0, 5))
        
        self.label = ctk.CTkLabel(self, text=label, font=("Segoe UI", 11, "bold"), text_color="#8D9AAA")
        self.label.pack(side="left")
        
        self.status_label = ctk.CTkLabel(self, text=self.online_text, font=("Segoe UI", 10, "bold"), text_color="#22C55E")
        self.status_label.pack(side="left", padx=(5, 0))
    
    def set_status(self, online: bool, status_text: Optional[str] = None):
        color = "#22C55E" if online else "#EF4444"
        self.dot.configure(text_color=color)
        if status_text is not None:
            self.status_label.configure(text=status_text, text_color=color)
        else:
            self.status_label.configure(text=self.online_text if online else self.offline_text, text_color=color)


class MetricCard(ctk.CTkFrame):
    """Metric card with title, value, and subtitle."""
    
    def __init__(self, parent, title: str = "", value: str = "--", subtitle: str = "", icon: str = "", value_color: str = "#E8EDF2", **kwargs):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        
        title_text = f"{icon} {title}" if icon else title
        self.title_label = ctk.CTkLabel(self, text=title_text, font=("Segoe UI", 11), text_color="#8D9AAA")
        self.title_label.grid(row=0, column=0, padx=15, pady=(12, 0), sticky="w")
        
        self.value_label = ctk.CTkLabel(self, text=str(value), font=("Segoe UI", 28, "bold"), text_color=value_color)
        self.value_label.grid(row=1, column=0, padx=15, pady=(2, 0), sticky="w")
        
        self.subtitle_label = ctk.CTkLabel(self, text=subtitle, font=("Segoe UI", 10), text_color="#5F6B78")
        self.subtitle_label.grid(row=2, column=0, padx=15, pady=(0, 12), sticky="w")
    
    def update_value(self, value: str, color: Optional[str] = None):
        self.value_label.configure(text=str(value))
        if color:
            self.value_label.configure(text_color=color)
    
    def update_subtitle(self, subtitle: str):
        self.subtitle_label.configure(text=subtitle)


class SignalBadge(ctk.CTkFrame):
    """Signal badge with color coding."""
    
    COLORS = {
        "BUY": "#22C55E", "SELL": "#EF4444", "HOLD": "#F59E0B",
        "STRONG BUY": "#16A34A", "STRONG SELL": "#DC2626",
        "MONITOR": "#3B82F6", "WAIT": "#8D9AAA", "NEUTRAL": "#6B7280",
        "BULLISH": "#22C55E", "BEARISH": "#EF4444",
    }
    
    def __init__(self, parent, signal: str = "HOLD", confidence: float = 0, show_confidence: bool = True, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.signal = signal
        self.confidence = confidence
        self.show_confidence = show_confidence
        
        color = self.COLORS.get(signal.upper(), "#8D9AAA")
        self.badge = ctk.CTkFrame(self, fg_color=color, corner_radius=4)
        self.badge.pack(side="left", padx=(0, 5))
        
        self.label = ctk.CTkLabel(self.badge, text=signal.upper(), font=("Segoe UI", 10, "bold"), text_color="white")
        self.label.pack(padx=8, pady=2)
        
        if show_confidence and confidence > 0:
            self.conf_label = ctk.CTkLabel(self, text=f"{confidence:.0f}%", font=("Segoe UI", 9), text_color="#8D9AAA")
            self.conf_label.pack(side="left", padx=5)
    
    def update(self, signal: str, confidence: float = 0):
        self.signal = signal
        self.confidence = confidence
        color = self.COLORS.get(signal.upper(), "#8D9AAA")
        self.badge.configure(fg_color=color)
        self.label.configure(text=signal.upper())
        if self.show_confidence and confidence > 0:
            if hasattr(self, 'conf_label'):
                self.conf_label.configure(text=f"{confidence:.0f}%")
            else:
                self.conf_label = ctk.CTkLabel(self, text=f"{confidence:.0f}%", font=("Segoe UI", 9), text_color="#8D9AAA")
                self.conf_label.pack(side="left", padx=5)


class ConfidenceBar(ctk.CTkFrame):
    """Confidence progress bar with label."""
    
    def __init__(self, parent, label: str = "Confidence", value: float = 0, max_value: float = 100, color: str = "#3B82F6", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.max_value = max_value
        self.grid_columnconfigure(1, weight=1)
        
        self.label = ctk.CTkLabel(self, text=label, font=("Segoe UI", 10), text_color="#8D9AAA")
        self.label.grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.progress = ctk.CTkProgressBar(self, width=100, height=8, corner_radius=4, progress_color=color)
        self.progress.grid(row=0, column=1, padx=5, sticky="ew")
        self.progress.set(value / max_value if max_value > 0 else 0)
        
        self.value_label = ctk.CTkLabel(self, text=f"{value:.0f}%", font=("Segoe UI", 10, "bold"), text_color="#E8EDF2")
        self.value_label.grid(row=0, column=2, padx=(5, 0), sticky="e")
    
    def set_value(self, value: float, max_value: Optional[float] = None):
        if max_value is not None:
            self.max_value = max_value
        normalized = value / self.max_value if self.max_value > 0 else 0
        self.progress.set(min(1.0, max(0.0, normalized)))
        self.value_label.configure(text=f"{value:.0f}%")
    
    def set_color(self, color: str):
        self.progress.configure(progress_color=color)


class InsightCard(ctk.CTkFrame):
    """Insight card for displaying insights."""
    
    def __init__(self, parent, title: str = "", content: str = "", category: str = "general", confidence: float = 0, **kwargs):
        super().__init__(parent, fg_color="#18212B", corner_radius=8, **kwargs)
        self.category = category
        self.confidence = confidence
        self.grid_columnconfigure(0, weight=1)
        
        title_text = f"[{category.upper()}] {title}" if category else title
        self.title_label = ctk.CTkLabel(self, text=title_text, font=("Segoe UI", 11, "bold"), text_color="#E8EDF2")
        self.title_label.grid(row=0, column=0, padx=12, pady=(8, 0), sticky="w")
        
        self.content_label = ctk.CTkLabel(self, text=content, font=("Segoe UI", 10), text_color="#8D9AAA", wraplength=300, justify="left")
        self.content_label.grid(row=1, column=0, padx=12, pady=(4, 8), sticky="w")
        
        if confidence > 0:
            self.conf_label = ctk.CTkLabel(self, text=f"Confidence: {confidence:.0f}%", font=("Segoe UI", 9), text_color="#5F6B78")
            self.conf_label.grid(row=2, column=0, padx=12, pady=(0, 8), sticky="w")
    
    def update(self, title: str, content: str, category: str = None, confidence: float = None):
        if category is not None:
            self.category = category
            self.title_label.configure(text=f"[{category.upper()}] {title}")
        else:
            self.title_label.configure(text=title)
        self.content_label.configure(text=content)
        if confidence is not None:
            self.confidence = confidence
            if confidence > 0:
                if hasattr(self, 'conf_label'):
                    self.conf_label.configure(text=f"Confidence: {confidence:.0f}%")
                else:
                    self.conf_label = ctk.CTkLabel(self, text=f"Confidence: {confidence:.0f}%", font=("Segoe UI", 9), text_color="#5F6B78")
                    self.conf_label.grid(row=2, column=0, padx=12, pady=(0, 8), sticky="w")


class DecisionCard(ctk.CTkFrame):
    """Decision display card."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self, text="🎯 Latest Decision", font=("Segoe UI", 11, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=2, padx=15, pady=(12, 5), sticky="w")
        
        self.action_label = ctk.CTkLabel(self, text="HOLD", font=("Segoe UI", 24, "bold"), text_color="#F59E0B")
        self.action_label.grid(row=1, column=0, padx=15, pady=5, sticky="w")
        
        self.confidence_display = ctk.CTkLabel(self, text="Confidence: 0%", font=("Segoe UI", 12), text_color="#8D9AAA")
        self.confidence_display.grid(row=2, column=0, padx=15, pady=(0, 5), sticky="w")
        
        self.reason_label = ctk.CTkLabel(self, text="Reason: Waiting for signal", font=("Segoe UI", 10), text_color="#5F6B78", wraplength=200)
        self.reason_label.grid(row=1, column=1, rowspan=2, padx=15, pady=5, sticky="w")
        
        self.timestamp_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 8), text_color="#5F6B78")
        self.timestamp_label.grid(row=3, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="w")
    
    def update(self, action: str, confidence: float, reason: str, timestamp: str = None):
        colors = {"BUY": "#22C55E", "STRONG BUY": "#16A34A", "SELL": "#EF4444", "STRONG SELL": "#DC2626", "HOLD": "#F59E0B", "MONITOR": "#3B82F6", "WAIT": "#8D9AAA", "NEUTRAL": "#6B7280"}
        self.action_label.configure(text=action, text_color=colors.get(action.upper(), "#8D9AAA"))
        self.confidence_display.configure(text=f"Confidence: {confidence:.0f}%")
        self.reason_label.configure(text=f"Reason: {reason}")
        self.timestamp_label.configure(text=f"Updated: {timestamp or datetime.now().strftime('%H:%M:%S')}")


class MemoryStats(ctk.CTkFrame):
    """Memory statistics display."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        ctk.CTkLabel(self, text="💾 Memory Statistics", font=("Segoe UI", 11, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=4, padx=15, pady=(12, 5), sticky="w")
        
        self.stats_labels = {}
        stat_items = [("short_term", "Short Term"), ("long_term", "Long Term"), ("working", "Working"), ("semantic", "Semantic"), ("episodic", "Episodic"), ("procedural", "Procedural"), ("emotional", "Emotional"), ("associative", "Associative")]
        
        for i, (key, label) in enumerate(stat_items):
            row = 1 + i // 4
            col = i % 4
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
            ctk.CTkLabel(frame, text=f"{label}:", font=("Segoe UI", 9), text_color="#8D9AAA").pack(side="left")
            self.stats_labels[key] = ctk.CTkLabel(frame, text="0", font=("Segoe UI", 10, "bold"), text_color="#E8EDF2")
            self.stats_labels[key].pack(side="left", padx=5)
    
    def update_stats(self, stats: Dict):
        if isinstance(stats, dict):
            for key, label in self.stats_labels.items():
                if key in stats:
                    label.configure(text=str(stats[key]))


class LearningProgress(ctk.CTkFrame):
    """Learning progress display."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self, text="📚 Learning Progress", font=("Segoe UI", 11, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")
        
        self.progress_bars = {}
        progress_items = [("learning", "Learning", "#3B82F6"), ("reasoning", "Reasoning", "#8B5CF6"), ("pattern", "Pattern Recognition", "#EC4899"), ("memory", "Memory", "#06B6D4"), ("consciousness", "Consciousness", "#22C55E"), ("knowledge", "Knowledge", "#F59E0B")]
        
        for i, (key, label, color) in enumerate(progress_items):
            row = 1 + i
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=row, column=0, padx=15, pady=3, sticky="ew")
            frame.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(frame, text=f"{label}:", font=("Segoe UI", 9), text_color="#8D9AAA").grid(row=0, column=0, padx=(0, 10), sticky="w")
            bar = ctk.CTkProgressBar(frame, width=100, height=6, corner_radius=3, progress_color=color)
            bar.grid(row=0, column=1, sticky="ew")
            bar.set(0)
            self.progress_bars[key] = bar


class MarketTicker(ctk.CTkFrame):
    """Market ticker with price and change."""
    
    def __init__(self, parent, symbol: str = "BTC/USD", price: float = 0, change: float = 0, volume: float = 0, **kwargs):
        super().__init__(parent, fg_color="#1A2530", corner_radius=8, **kwargs)
        self.symbol = symbol
        self.price = price
        self.change = change
        self.volume = volume
        self._build_ui()
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        
        self.symbol_label = ctk.CTkLabel(self, text=self.symbol, font=("Segoe UI", 13, "bold"), text_color="#E8EDF2")
        self.symbol_label.grid(row=0, column=0, padx=12, pady=10, sticky="w")
        
        self.price_label = ctk.CTkLabel(self, text=f"${self.price:,.2f}" if self.price else "--", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2")
        self.price_label.grid(row=0, column=1, padx=12, sticky="e")
        
        color = "#22C55E" if self.change >= 0 else "#EF4444"
        sign = "+" if self.change >= 0 else ""
        self.change_label = ctk.CTkLabel(self, text=f"{sign}{self.change:.2f}%", font=("Segoe UI", 12, "bold"), text_color=color)
        self.change_label.grid(row=0, column=2, padx=12, sticky="e")
        
        self.volume_label = ctk.CTkLabel(self, text=f"Vol: {self.volume:,.0f}" if self.volume else "", font=("Segoe UI", 9), text_color="#5F6B78")
        self.volume_label.grid(row=0, column=3, padx=12, sticky="e")
    
    def update(self, price: float, change: float, volume: float = None):
        self.price = price
        self.change = change
        if volume is not None:
            self.volume = volume
        self.price_label.configure(text=f"${price:,.2f}" if price else "--")
        color = "#22C55E" if change >= 0 else "#EF4444"
        sign = "+" if change >= 0 else ""
        self.change_label.configure(text=f"{sign}{change:.2f}%", text_color=color)
        if volume is not None or self.volume:
            self.volume_label.configure(text=f"Vol: {self.volume:,.0f}" if self.volume else "")


class PatternList(ctk.CTkScrollableFrame):
    """List of detected patterns."""
    
    def __init__(self, parent, title: str = "🔍 Detected Patterns", **kwargs):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text=title, font=("Segoe UI", 11, "bold"), text_color="#E8EDF2")
        self.title_label.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")
        
        self.pattern_container = ctk.CTkFrame(self, fg_color="transparent")
        self.pattern_container.grid(row=1, column=0, padx=15, pady=(5, 12), sticky="ew")
        self.pattern_container.grid_columnconfigure(0, weight=1)
        
        self.pattern_labels = []
        self.pattern_count_label = ctk.CTkLabel(self, text="Total: 0 patterns", font=("Segoe UI", 9), text_color="#5F6B78")
        self.pattern_count_label.grid(row=2, column=0, padx=15, pady=(0, 12), sticky="w")
    
    def update_patterns(self, patterns: List[Dict]):
        for label in self.pattern_labels:
            label.destroy()
        self.pattern_labels.clear()
        for i, pattern in enumerate(patterns[:20]):
            if isinstance(pattern, dict):
                name = pattern.get('name', pattern.get('type', 'Unknown'))
                confidence = pattern.get('confidence', 0)
                description = pattern.get('description', '')
            else:
                name = str(pattern)
                confidence = 0
                description = ''
            frame = ctk.CTkFrame(self.pattern_container, fg_color="#1A2430" if i % 2 == 0 else "transparent", corner_radius=4)
            frame.grid(row=i, column=0, padx=2, pady=2, sticky="ew")
            frame.grid_columnconfigure(0, weight=1)
            label_text = f"• {name}"
            if confidence > 0:
                label_text += f" ({confidence:.0f}%)"
            if description:
                label_text += f" - {description[:50]}"
            label = ctk.CTkLabel(frame, text=label_text, font=("Segoe UI", 10), text_color="#8D9AAA", anchor="w")
            label.grid(row=0, column=0, padx=8, pady=4, sticky="w")
            self.pattern_labels.append(label)
        self.pattern_count_label.configure(text=f"Total: {len(patterns)} patterns")


# ============================================================
# BASE PAGE
# ============================================================

def get_default_font(size=20):
    try:
        return ctk.CTkFont(size=size)
    except RuntimeError:
        return None


class IntelligencePage(ctk.CTkFrame):
    """Base class for all Intelligence pages."""
    
    def __init__(self, parent, bot=None, learning_integration=None, **kwargs):
        self._initialized = False
        self._is_destroyed = False
        
        self.bot = bot
        self.learning_integration = learning_integration
        self.brain = None
        if bot:
            if hasattr(bot, 'brain'):
                self.brain = bot.brain
            elif hasattr(bot, '_brain'):
                self.brain = bot._brain
        
        self.consciousness = None
        try:
            from core.consciousness import consciousness
            self.consciousness = consciousness
        except ImportError:
            pass
        
        self.is_connected = False
        self.last_error = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = 3000
        self.last_update_time = None
        self.update_durations = []
        self.health_score = 100.0
        self.performance_metrics = {}
        self.page_status = "INITIALIZING"
        
        super().__init__(parent, **kwargs)
        self._build_ui()
        self._start_updates()
        self._initialized = True
        logger.debug(f"[{self.__class__.__name__}] Initialized")
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._create_empty_page()
    
    def _create_empty_page(self):
        font = get_default_font(20) or ("Segoe UI", 20)
        label = ctk.CTkLabel(self, text=f"📄 {self.__class__.__name__}\n\nPage under construction...", font=font, text_color="#5F6B78")
        label.place(relx=0.5, rely=0.5, anchor="center")
    
    def _start_updates(self):
        if self.is_running and not self._is_destroyed:
            self.update_data()
    
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
        
        start_time = datetime.now()
        try:
            self.update_count += 1
            self._update_health()
            self._update_performance_metrics()
            self._update_connection_status()
            self.success_count += 1
            self.is_connected = True
            self.page_status = "ONLINE"
            self.on_update()
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.is_connected = False
            self.page_status = "ERROR"
            logger.error(f"[{self.__class__.__name__}] Update error: {e}")
        
        duration = (datetime.now() - start_time).total_seconds()
        self.update_durations.append(duration)
        if len(self.update_durations) > 100:
            self.update_durations = self.update_durations[-100:]
        self.last_update_time = datetime.now()
        
        if self.is_running and not self._is_destroyed:
            try:
                self.after(self.update_interval, self.update_data)
            except Exception:
                pass
    
    def _update_health(self):
        health = 100.0
        if self.error_count > 0:
            health -= min(30, self.error_count * 2)
        if not self.is_connected:
            health -= 20
        if self.update_count > 0:
            success_rate = (self.success_count / max(1, self.update_count)) * 100
            health += (success_rate - 50) * 0.2
        self.health_score = max(0.0, min(100.0, health))
    
    def _update_performance_metrics(self):
        avg_duration = 0
        if self.update_durations:
            avg_duration = sum(self.update_durations) / len(self.update_durations)
        self.performance_metrics = {
            "total_updates": self.update_count,
            "successful_updates": self.success_count,
            "failed_updates": self.error_count,
            "success_rate": (self.success_count / max(1, self.update_count)) * 100,
            "avg_update_duration_ms": round(avg_duration * 1000, 2),
            "health_score": self.health_score,
            "status": self.page_status,
        }
    
    def _update_connection_status(self):
        if self.bot is not None:
            try:
                if hasattr(self.bot, 'is_running'):
                    self.is_connected = self.bot.is_running()
                elif hasattr(self.bot, 'running'):
                    self.is_connected = self.bot.running
            except Exception:
                pass
        if self.brain is not None and self.is_connected:
            try:
                if hasattr(self.brain, 'is_healthy'):
                    self.is_connected = self.brain.is_healthy()
            except Exception:
                pass
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "page": self.__class__.__name__,
            "status": self.page_status,
            "connected": self.is_connected,
            "update_count": self.update_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "health_score": self.health_score,
            "last_update": self.last_update_time.isoformat() if self.last_update_time else None,
            "last_error": self.last_error,
            "performance": self.performance_metrics,
            "has_bot": self.bot is not None,
            "has_brain": self.brain is not None,
            "has_consciousness": self.consciousness is not None,
            "has_learning": self.learning_integration is not None,
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        avg_duration = 0
        if self.update_durations:
            avg_duration = sum(self.update_durations) / len(self.update_durations)
        return {
            "total_updates": self.update_count,
            "successful_updates": self.success_count,
            "failed_updates": self.error_count,
            "success_rate": (self.success_count / max(1, self.update_count)) * 100,
            "avg_update_duration": avg_duration,
            "update_interval": self.update_interval,
            "health_score": self.health_score,
            "page_status": self.page_status,
        }
    
    def get_health(self) -> Dict[str, Any]:
        return {
            "page": self.__class__.__name__,
            "health_score": self.health_score,
            "status": self.page_status,
            "connected": self.is_connected,
            "errors": self.error_count,
            "last_error": self.last_error,
            "last_update": self.last_update_time.isoformat() if self.last_update_time else None,
            "components": {
                "bot": self.bot is not None,
                "brain": self.brain is not None,
                "consciousness": self.consciousness is not None,
                "learning": self.learning_integration is not None,
            }
        }
    
    def set_bot(self, bot):
        self.bot = bot
        if bot:
            if hasattr(bot, 'brain'):
                self.brain = bot.brain
            elif hasattr(bot, '_brain'):
                self.brain = bot._brain
        self._on_reference_changed()
    
    def set_learning(self, learning):
        self.learning_integration = learning
        self._on_reference_changed()
    
    def set_update_interval(self, interval_ms: int):
        self.update_interval = max(500, interval_ms)
    
    def _on_reference_changed(self):
        pass
    
    def on_show(self):
        self.page_status = "ACTIVE"
        logger.debug(f"[{self.__class__.__name__}] Shown")
    
    def on_hide(self):
        self.page_status = "HIDDEN"
        logger.debug(f"[{self.__class__.__name__}] Hidden")
    
    def on_update(self):
        pass
    
    def show_error(self, error: str):
        self.last_error = error
        self.error_count += 1
        self.is_connected = False
    
    def clear_error(self):
        self.last_error = None
    
    def safe_execute(self, func: Callable, *args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.show_error(str(e))
            logger.error(f"[{self.__class__.__name__}] Execute error: {e}")
            return None
    
    def is_healthy(self) -> bool:
        return self.health_score > 50 and self.is_connected
    
    def refresh(self):
        if not self._is_destroyed:
            self.update_data()
    
    def stop(self):
        self.is_running = False
        self.page_status = "STOPPED"
        logger.debug(f"[{self.__class__.__name__}] Stopped")
    
    def start(self):
        if not self.is_running and not self._is_destroyed:
            self.is_running = True
            self.page_status = "ACTIVE"
            self._start_updates()
            logger.debug(f"[{self.__class__.__name__}] Started")
    
    def reset_metrics(self):
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.health_score = 100.0
        self.last_error = None
        self.update_durations = []
        logger.debug(f"[{self.__class__.__name__}] Metrics reset")
    
    def destroy(self):
        if self._is_destroyed:
            return
        self._is_destroyed = True
        self.is_running = False
        self.page_status = "DESTROYED"
        self.update_durations.clear()
        self.bot = None
        self.brain = None
        self.consciousness = None
        self.learning_integration = None
        logger.debug(f"[{self.__class__.__name__}] Destroyed")
        try:
            super().destroy()
        except Exception:
            pass


# ============================================================
# DASHBOARD PAGE
# ============================================================

class DashboardPage(IntelligencePage):
    """Cognitive Intelligence Dashboard."""
    
    def __init__(self, parent, *args, **kwargs):
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
        self.exchange_status = "UNKNOWN"
        self.bot = None
        self.learning_integration = None
        self.is_running = True
        self.update_interval = 3000
        self._after_id = None
        self._data_thread = None
        self._thread_running = False
        self._error_count = 0
        self._exchange_connected = False
        self._is_destroyed = False
        self.signals_per_page = 4
        self.current_page = 0
        self.total_pages = 0
        
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
        self.after(500, self.update_data)
    
    def _build_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.main_scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.main_scrollable_frame.grid_columnconfigure(1, weight=1)
        self.main_scrollable_frame.grid_columnconfigure(2, weight=1)
        row = 0
        
        # HEADER
        header = ctk.CTkFrame(self.main_scrollable_frame, fg_color="transparent")
        header.grid(row=row, column=0, columnspan=3, padx=10, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="🧠 Cognitive Intelligence Dashboard", font=("Segoe UI", 24, "bold"), text_color="#E8EDF2").grid(row=0, column=0, sticky="w")
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.grid(row=0, column=1, sticky="e")
        self.data_source_label = ctk.CTkLabel(status_frame, text="📡 SOURCE: --", font=("Segoe UI", 10, "bold"), text_color="#8D9AAA")
        self.data_source_label.pack(side="left", padx=5)
        self.live_indicator = ctk.CTkLabel(status_frame, text="● CONNECTING", font=("Segoe UI", 12, "bold"), text_color="#FFAA00")
        self.live_indicator.pack(side="left", padx=10)
        self.status_indicator = StatusIndicator(status_frame, label="System")
        self.status_indicator.pack(side="left", padx=5)
        self.status_indicator.set_status(False)
        self.clock_label = ctk.CTkLabel(header, text=datetime.now().strftime("%H:%M:%S"), font=("Segoe UI", 12), text_color="#8D9AAA")
        self.clock_label.grid(row=0, column=2, padx=10)
        row += 1
        
        # SYSTEM STATUS
        self.brain_card = MetricCard(self.main_scrollable_frame, title="🧠 Brain", value="WAITING", subtitle="Cycles: -- | Success: --")
        self.brain_card.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")
        self.consciousness_card = MetricCard(self.main_scrollable_frame, title="💭 Consciousness", value="WAITING", subtitle="Awareness: -- | State: --")
        self.consciousness_card.grid(row=row, column=1, padx=10, pady=10, sticky="nsew")
        self.learning_card = MetricCard(self.main_scrollable_frame, title="📚 Learning", value="WAITING", subtitle="Cycles: -- | Modules: --")
        self.learning_card.grid(row=row, column=2, padx=10, pady=10, sticky="nsew")
        row += 1
        
        # EXCHANGE & SIGNALS
        self.exchange_card = MetricCard(self.main_scrollable_frame, title="🔄 Exchange", value="UNKNOWN", subtitle="Status: --")
        self.exchange_card.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")
        self.signal_card = MetricCard(self.main_scrollable_frame, title="📈 Signal", value="WAITING", subtitle="Confidence: -- | Quality: --")
        self.signal_card.grid(row=row, column=1, padx=10, pady=10, sticky="nsew")
        self.scanner_card = MetricCard(self.main_scrollable_frame, title="🔍 Scanner", value="WAITING", subtitle="Pairs: -- | Signals: --")
        self.scanner_card.grid(row=row, column=2, padx=10, pady=10, sticky="nsew")
        row += 1
        
        # KNOWLEDGE, MEMORY, PERFORMANCE
        self.knowledge_card = MetricCard(self.main_scrollable_frame, title="📚 Knowledge", value="0", subtitle="Items: 0 | Confidence: 0%")
        self.knowledge_card.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")
        self.memory_card = MetricCard(self.main_scrollable_frame, title="💾 Memory", value="0", subtitle="Short: 0 | Long: 0")
        self.memory_card.grid(row=row, column=1, padx=10, pady=10, sticky="nsew")
        self.performance_card = MetricCard(self.main_scrollable_frame, title="⚡ Performance", value="0%", subtitle="Success: 0% | Errors: 0")
        self.performance_card.grid(row=row, column=2, padx=10, pady=10, sticky="nsew")
        row += 1
        
        # SIGNALS
        signals_main_frame = ctk.CTkFrame(self.main_scrollable_frame, fg_color="#131A22", corner_radius=10)
        signals_main_frame.grid(row=row, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        signals_main_frame.grid_columnconfigure(0, weight=1)
        signals_header = ctk.CTkFrame(signals_main_frame, fg_color="transparent")
        signals_header.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        signals_header.grid_columnconfigure(0, weight=1)
        signals_header.grid_columnconfigure(1, weight=0)
        ctk.CTkLabel(signals_header, text="📈 Live Signals", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, sticky="w")
        pagination_controls = ctk.CTkFrame(signals_header, fg_color="transparent")
        pagination_controls.grid(row=0, column=1, sticky="e")
        self.prev_btn = ctk.CTkButton(pagination_controls, text="◀", width=30, height=25, font=("Segoe UI", 10), fg_color="#2A3A4A", hover_color="#3B4A5A", command=self._prev_page, state="disabled")
        self.prev_btn.pack(side="left", padx=2)
        self.page_label = ctk.CTkLabel(pagination_controls, text="Page 1/1", font=("Segoe UI", 10), text_color="#8D9AAA")
        self.page_label.pack(side="left", padx=8)
        self.next_btn = ctk.CTkButton(pagination_controls, text="▶", width=30, height=25, font=("Segoe UI", 10), fg_color="#2A3A4A", hover_color="#3B4A5A", command=self._next_page, state="disabled")
        self.next_btn.pack(side="left", padx=2)
        self.signal_container = ctk.CTkFrame(signals_main_frame, fg_color="transparent")
        self.signal_container.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        for i in range(4):
            self.signal_container.grid_columnconfigure(i, weight=1)
        self.signal_cards = []
        for i in range(4):
            card = ctk.CTkFrame(self.signal_container, fg_color="#1A2530", corner_radius=8)
            card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)
            badge = SignalBadge(card, signal="WAITING")
            badge.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
            pair_label = ctk.CTkLabel(card, text="---", font=("Segoe UI", 11), text_color="#8D9AAA")
            pair_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="w")
            price_label = ctk.CTkLabel(card, text="--", font=("Segoe UI", 10), text_color="#5F6B78")
            price_label.grid(row=2, column=0, padx=10, pady=(2, 0), sticky="w")
            conf_bar = ConfidenceBar(card, label="Confidence", value=0)
            conf_bar.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")
            self.signal_cards.append({"frame": card, "badge": badge, "pair": pair_label, "price": price_label, "confidence": conf_bar, "data": None, "index": i})
        self.signal_empty_label = ctk.CTkLabel(self.signal_container, text="📭 No signals available", font=("Segoe UI", 14), text_color="#5F6B78")
        row += 1
        
        # INSIGHTS
        insights_frame = ctk.CTkFrame(self.main_scrollable_frame, fg_color="#131A22", corner_radius=10)
        insights_frame.grid(row=row, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        insights_frame.grid_rowconfigure(0, weight=0)
        insights_frame.grid_rowconfigure(1, weight=1)
        insights_frame.grid_columnconfigure(0, weight=1)
        insights_frame.grid_columnconfigure(1, weight=1)
        insights_header = ctk.CTkFrame(insights_frame, fg_color="transparent")
        insights_header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
        insights_header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(insights_header, text="💡 Cognitive Insights", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, sticky="w")
        self.insight_count_label = ctk.CTkLabel(insights_header, text="0 insights", font=("Segoe UI", 11), text_color="#8D9AAA")
        self.insight_count_label.grid(row=0, column=1, sticky="e", padx=10)
        self.insights_container = ctk.CTkFrame(insights_frame, fg_color="transparent")
        self.insights_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(0, 10))
        self.insights_container.grid_rowconfigure(0, weight=1)
        self.insights_container.grid_rowconfigure(1, weight=1)
        self.insights_container.grid_columnconfigure(0, weight=1)
        self.insights_container.grid_columnconfigure(1, weight=1)
        self.insight_cards = []
        for i in range(4):
            card = InsightCard(self.insights_container, title="Waiting for data...", content="System initializing...")
            row_ins = i // 2
            col_ins = i % 2
            card.grid(row=row_ins, column=col_ins, padx=5, pady=5, sticky="nsew")
            self.insight_cards.append(card)
    
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
                    card_data['badge'].update(signal.get('signal', 'HOLD'))
                    card_data['pair'].configure(text=signal.get('pair', '---'))
                    price = signal.get('price', 0)
                    card_data['price'].configure(text=f"${price:,.2f}" if price else "--")
                    card_data['confidence'].set_value(signal.get('confidence', 0))
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
    
    def _collect_data(self):
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
        
        try:
            from core import brain
            if brain:
                if hasattr(brain, 'status'):
                    self.brain_status = brain.status()
                elif hasattr(brain, 'get_state'):
                    self.brain_status = brain.get_state()
        except Exception:
            pass
        
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
            pass
        
        try:
            from core import learning_engine
            if learning_engine:
                if hasattr(learning_engine, 'status'):
                    self.learning_status = learning_engine.status()
                elif hasattr(learning_engine, 'get_state'):
                    self.learning_status = learning_engine.get_state()
        except Exception:
            pass
        
        try:
            from core import knowledge
            if knowledge and hasattr(knowledge, 'stats'):
                stats = knowledge.stats()
                if stats:
                    self.knowledge_stats = {"total": getattr(stats, 'total', 0), "states": getattr(stats, 'state_count', 0), "avg_confidence": getattr(stats, 'avg_confidence', 0), "active": getattr(stats, 'active', 0)}
        except Exception:
            pass
        
        try:
            from core import memory
            if memory and hasattr(memory, 'get_stats'):
                stats = memory.get_stats()
                if stats:
                    self.memory_stats = {"short_term": stats.get('short_term', 0), "long_term": stats.get('long_term', 0), "total": stats.get('total', 0)}
        except Exception:
            pass
        
        if self.bot:
            try:
                if hasattr(self.bot, 'get_signals'):
                    self.signals = self.bot.get_signals()
            except Exception:
                pass
            try:
                if hasattr(self.bot, 'scanner') and self.bot.scanner:
                    if hasattr(self.bot.scanner, 'get_status'):
                        self.scanner_status = self.bot.scanner.get_status()
            except Exception:
                pass
        
        success_rate = self.brain_status.get('success_rate', 0) if self.brain_status else 0
        errors = self.brain_status.get('errors', 0) if self.brain_status else 0
        self.performance_metrics = {"success_rate": success_rate, "errors": errors, "error_count": self._error_count}
        self._generate_insights()
    
    def _generate_insights(self):
        self.insights = []
        if self.brain_status:
            state = self.brain_status.get('state', 'Unknown')
            cycles = self.brain_status.get('cycles', 0)
            success = self.brain_status.get('success_rate', 0)
            self.insights.append({"title": "🧠 Brain Status", "content": f"State: {state} | Cycles: {cycles} | Success: {success:.1f}%", "category": "brain", "confidence": success})
        if self.exchange_status == 'ONLINE':
            self.insights.append({"title": "🔄 Exchange", "content": "Kraken is ONLINE and connected.", "category": "exchange", "confidence": 90})
        elif self.exchange_status == 'DEGRADED':
            self.insights.append({"title": "⚠️ Exchange", "content": "Kraken is DEGRADED. Some data may be unavailable.", "category": "exchange", "confidence": 50})
        else:
            self.insights.append({"title": "❌ Exchange", "content": f"Kraken is {self.exchange_status}. Check connection.", "category": "exchange", "confidence": 0})
        if self.consciousness_state:
            mood = self.consciousness_state.get('emotional_state', self.consciousness_state.get('state', 'CALM'))
            awareness = self.consciousness_state.get('awareness', self.consciousness_state.get('awareness_level', 0))
            curiosity = self.consciousness_state.get('curiosity', 0)
            self.insights.append({"title": "💭 Consciousness", "content": f"State: {mood} | Awareness: {awareness*100:.0f}% | Curiosity: {curiosity*100:.0f}%", "category": "consciousness", "confidence": awareness * 100})
        if self.learning_status:
            cycles = self.learning_status.get('cycles', 0)
            modules = self.learning_status.get('module_count', 0)
            running = self.learning_status.get('running', False)
            self.insights.append({"title": "📚 Learning", "content": f"Status: {'ACTIVE' if running else 'IDLE'} | Cycles: {cycles} | Modules: {modules}", "category": "learning", "confidence": 80 if running else 50})
        if self.knowledge_stats:
            total = self.knowledge_stats.get('total', 0)
            avg_conf = self.knowledge_stats.get('avg_confidence', 0)
            self.insights.append({"title": "📚 Knowledge", "content": f"Items: {total} | Avg Confidence: {avg_conf:.1f}%", "category": "knowledge", "confidence": avg_conf})
        self.insights.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        self.insights = self.insights[:4]
    
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
            if self.clock_label:
                self.clock_label.configure(text=datetime.now().strftime("%H:%M:%S"))
            if self.data_source_label:
                if self._exchange_connected:
                    self.data_source_label.configure(text="📡 SOURCE: KRAKEN LIVE", text_color="#22C55E")
                else:
                    self.data_source_label.configure(text="📡 SOURCE: NO DATA", text_color="#EF4444")
            
            if self.brain_status and self.brain_card:
                state = self.brain_status.get('state', 'UNKNOWN')
                cycles = self.brain_status.get('cycles', 0)
                success = self.brain_status.get('success_rate', 0)
                self.brain_card.update_value(state)
                self.brain_card.update_subtitle(f"Cycles: {cycles} | Success: {success:.1f}%")
            
            if self.consciousness_state and self.consciousness_card:
                mood = self.consciousness_state.get('emotional_state', self.consciousness_state.get('state', 'IDLE'))
                awareness = self.consciousness_state.get('awareness', self.consciousness_state.get('awareness_level', 0))
                self.consciousness_card.update_value(mood)
                self.consciousness_card.update_subtitle(f"Awareness: {awareness*100:.0f}%")
            
            if self.learning_status and self.learning_card:
                running = self.learning_status.get('running', False)
                cycles = self.learning_status.get('cycles', 0)
                modules = self.learning_status.get('module_count', 0)
                self.learning_card.update_value("RUNNING" if running else "IDLE")
                self.learning_card.update_subtitle(f"Cycles: {cycles} | Modules: {modules}")
            
            if self.exchange_card:
                status_text = self.exchange_status
                color = "#22C55E" if status_text == "ONLINE" else "#EF4444" if status_text in ["ERROR", "OFFLINE"] else "#F59E0B"
                self.exchange_card.update_value(status_text, color=color)
                self.exchange_card.update_subtitle(f"Status: {'Connected' if status_text == 'ONLINE' else 'Disconnected'}")
            
            if self.scanner_status and self.scanner_card:
                running = self.scanner_status.get('running', False)
                pairs = self.scanner_status.get('pairs_scanned', 0)
                signals = self.scanner_status.get('signals_generated', 0)
                self.scanner_card.update_value("SCANNING" if running else "IDLE")
                self.scanner_card.update_subtitle(f"Pairs: {pairs} | Signals: {signals}")
            
            if self.knowledge_stats and self.knowledge_card:
                total = self.knowledge_stats.get('total', 0)
                avg_conf = self.knowledge_stats.get('avg_confidence', 0)
                self.knowledge_card.update_value(str(total))
                self.knowledge_card.update_subtitle(f"Confidence: {avg_conf:.1f}%")
            
            if self.memory_stats and self.memory_card:
                short = self.memory_stats.get('short_term', 0)
                long = self.memory_stats.get('long_term', 0)
                self.memory_card.update_value(str(short + long))
                self.memory_card.update_subtitle(f"Short: {short} | Long: {long}")
            
            if self.performance_metrics and self.performance_card:
                success_rate = self.performance_metrics.get('success_rate', 0)
                errors = self.performance_metrics.get('errors', 0)
                self.performance_card.update_value(f"{success_rate:.1f}%")
                self.performance_card.update_subtitle(f"Errors: {errors}")
            
            if self.signals and self.signal_card:
                signal = self.signals[0] if self.signals else {}
                if isinstance(signal, dict):
                    action = signal.get('signal', 'HOLD')
                    confidence = signal.get('confidence', 0)
                    self.signal_card.update_value(action)
                    self.signal_card.update_subtitle(f"Confidence: {confidence:.0f}%")
                    color = "#FFAA00"
                    if action in ['BUY', 'STRONG_BUY']:
                        color = "#22C55E"
                    elif action in ['SELL', 'STRONG_SELL']:
                        color = "#EF4444"
                    self.signal_card.value_label.configure(text_color=color)
            
            for i, card in enumerate(self.insight_cards):
                if i < len(self.insights):
                    insight = self.insights[i]
                    card.update(insight.get("title", "---"), insight.get("content", "No data available"))
                else:
                    card.update("---", "No data available")
            
            if self.insight_count_label:
                self.insight_count_label.configure(text=f"{len(self.insights)} insights")
            
            if self._exchange_connected:
                self.live_indicator.configure(text="● LIVE", text_color="#00FF88")
                self.status_indicator.set_status(True)
            else:
                self.live_indicator.configure(text="● NO DATA", text_color="#FF4444")
                self.status_indicator.set_status(False)
            
            self._update_pagination()
            
        except Exception as e:
            self._error_count += 1
            logger.error(f"[Dashboard] Update error: {e}")
        
        if self.is_running and not self._is_destroyed:
            try:
                self._after_id = self.after(self.update_interval, self.update_data)
            except Exception:
                pass
    
    def set_bot(self, bot):
        self.bot = bot
    
    def set_learning(self, learning):
        self.learning_integration = learning
    
    def refresh(self):
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
        try:
            super().destroy()
        except Exception:
            pass


# ============================================================
# BRAIN PAGE
# ============================================================

class Brain(IntelligencePage):
    """Brain Status & Insights."""
    
    def __init__(self, parent, *args, **kwargs):
        self.brain_data = {}
        self.brain_instances = {}
        self.active_brain_name = "default"
        self.last_error = None
        self.last_error_time = None
        self.brain_instance = None
        self.brain = None
        self._brain_available = False
        self.bot = None
        self.learning_integration = None
        self.is_running = True
        self.update_interval = 3000
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_connected = False
        
        self.brain_selector = None
        self.selector_frame = None
        self.status_indicator = None
        self.state_card = None
        self.cycles_card = None
        self.errors_card = None
        self.success_card = None
        self.health_card = None
        self.insight_cards = []
        self.details_text = None
        self.last_update_label = None
        self.refresh_btn = None
        self.insight_container = None
        self._after_id = None
        
        super().__init__(parent, *args, **kwargs)
        self._build_ui()
        self.after(500, self.update_data)
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)
        
        ctk.CTkLabel(header, text="🧠 Brain Status & Insights", font=("Segoe UI", 22, "bold"), text_color="#E8EDF2").grid(row=0, column=0, sticky="w")
        self.status_indicator = StatusIndicator(header, label="Brain")
        self.status_indicator.grid(row=0, column=1, padx=10)
        self.last_update_label = ctk.CTkLabel(header, text="Last update: --", font=("Segoe UI", 10), text_color="#5F6B78")
        self.last_update_label.grid(row=0, column=2, padx=10)
        self.refresh_btn = ctk.CTkButton(header, text="🔄 Refresh", width=80, height=28, font=("Segoe UI", 11), fg_color="#3B82F6", hover_color="#2563EB", command=self.refresh)
        self.refresh_btn.grid(row=0, column=3, padx=10)
        
        self.selector_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        self.selector_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.selector_frame.grid_columnconfigure(0, weight=0)
        self.selector_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.selector_frame, text="Active Brain:", font=("Segoe UI", 12), text_color="#8D9AAA").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.brain_selector = ctk.CTkOptionMenu(self.selector_frame, values=["default"], command=self._on_brain_selected, width=200, height=32, fg_color="#1A2530", button_color="#2A3A4A", button_hover_color="#3B4A5A", text_color="#E8EDF2")
        self.brain_selector.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        self.brain_selector.set("default")
        
        metrics_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        metrics_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(2, weight=1)
        metrics_frame.grid_columnconfigure(3, weight=1)
        metrics_frame.grid_columnconfigure(4, weight=1)
        ctk.CTkLabel(metrics_frame, text="📊 Brain Metrics", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=5, padx=15, pady=10, sticky="w")
        
        self.state_card = MetricCard(metrics_frame, title="State", value="--", subtitle="Current state")
        self.state_card.grid(row=1, column=0, padx=6, pady=8, sticky="nsew")
        self.cycles_card = MetricCard(metrics_frame, title="🔄 Cycles", value="0")
        self.cycles_card.grid(row=1, column=1, padx=6, pady=8, sticky="nsew")
        self.errors_card = MetricCard(metrics_frame, title="❌ Errors", value="0")
        self.errors_card.grid(row=1, column=2, padx=6, pady=8, sticky="nsew")
        self.success_card = MetricCard(metrics_frame, title="✅ Success Rate", value="0%")
        self.success_card.grid(row=1, column=3, padx=6, pady=8, sticky="nsew")
        self.health_card = MetricCard(metrics_frame, title="❤️ Health Score", value="0%", subtitle="Brain health")
        self.health_card.grid(row=1, column=4, padx=6, pady=8, sticky="nsew")
        
        insights_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        insights_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        insights_frame.grid_rowconfigure(0, weight=0)
        insights_frame.grid_rowconfigure(1, weight=1)
        insights_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(insights_frame, text="💡 Brain Insights", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.insight_container = ctk.CTkFrame(insights_frame, fg_color="transparent")
        self.insight_container.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.insight_container.grid_columnconfigure(0, weight=1)
        self.insight_container.grid_columnconfigure(1, weight=1)
        self.insight_cards = []
        for i in range(4):
            card = InsightCard(self.insight_container, title="--", content="No insight available")
            row_i = i // 2
            col_i = i % 2
            card.grid(row=row_i, column=col_i, padx=5, pady=5, sticky="nsew")
            self.insight_cards.append(card)
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        details.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(details, text="📋 Raw Brain Data", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.details_text = ctk.CTkTextbox(details, font=("Consolas", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=120)
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def set_bot(self, bot):
        self.bot = bot
        self._update_brain_reference()
        self._update_selector()
    
    def set_learning(self, learning):
        self.learning_integration = learning
        self._update_brain_reference()
    
    def set_brain(self, brain):
        self.brain_instance = brain
        self.brain = brain
        self._brain_available = brain is not None
        self._update_brain_reference()
        self._update_selector()
    
    def _update_brain_reference(self):
        if self.bot:
            if hasattr(self.bot, 'brain'):
                self.brain = self.bot.brain
                self.brain_instance = self.bot.brain
            elif hasattr(self.bot, '_brain'):
                self.brain = self.bot._brain
                self.brain_instance = self.bot._brain
            elif hasattr(self.bot, 'get_brain'):
                try:
                    brain = self.bot.get_brain()
                    if brain:
                        self.brain = brain
                        self.brain_instance = brain
                except Exception:
                    pass
        if not self.brain and self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                self.brain = self.learning_integration.brain
                self.brain_instance = self.learning_integration.brain
            elif hasattr(self.learning_integration, 'get_brain'):
                try:
                    brain = self.learning_integration.get_brain()
                    if brain:
                        self.brain = brain
                        self.brain_instance = brain
                except Exception:
                    pass
        if not self.brain:
            try:
                from core.brain import brain
                if brain:
                    self.brain = brain
                    self.brain_instance = brain
            except ImportError:
                pass
        self._brain_available = self.brain is not None
        if self.brain and hasattr(self.brain, 'get_instances'):
            try:
                self.brain_instances = self.brain.get_instances()
                if not self.brain_instances:
                    self.brain_instances = {"default": self.brain}
            except Exception:
                self.brain_instances = {"default": self.brain}
        else:
            self.brain_instances = {"default": self.brain} if self.brain else {}
        self._update_selector()
    
    def _update_selector(self):
        if not hasattr(self, 'brain_selector') or self.brain_selector is None:
            return
        if not hasattr(self.brain_selector, 'configure'):
            return
        instances = list(self.brain_instances.keys()) if self.brain_instances else ["default"]
        if not instances:
            instances = ["default"]
        try:
            self.brain_selector.configure(values=instances)
            if self.active_brain_name in instances:
                self.brain_selector.set(self.active_brain_name)
            elif instances:
                self.brain_selector.set(instances[0])
                self.active_brain_name = instances[0]
        except Exception as e:
            print(f"[Brain GUI] Selector update error: {e}")
    
    def _on_brain_selected(self, choice: str):
        if not choice:
            return
        if choice in self.brain_instances:
            self.brain = self.brain_instances[choice]
            self.brain_instance = self.brain
            self.active_brain_name = choice
            self._brain_available = True
            self._update_selector()
    
    def update_data(self):
        if not self.is_running:
            return
        try:
            self.update_count += 1
            self._update_brain_reference()
            status = self._get_brain_status()
            if status:
                self.brain_data = status
                self.is_connected = True
                self.success_count += 1
                self.last_error = None
            else:
                self.brain_data = self._generate_fallback_data()
                self.is_connected = False
                self.error_count += 1
                self.last_error = "Brain unavailable, using fallback"
                self.last_error_time = datetime.now()
            self._update_ui()
            if self.last_update_label:
                self.last_update_label.configure(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            print(f"[Brain GUI] Update error: {e}")
            traceback.print_exc()
            self._update_error_display(e)
        if self.is_running:
            try:
                self._after_id = self.after(self.update_interval, self.update_data)
            except Exception as e:
                print(f"[Brain GUI] Schedule error: {e}")
    
    def _get_brain_status(self):
        if not self.brain:
            return None
        methods = ['status', 'get_state', 'snapshot', 'health_check']
        for method in methods:
            if hasattr(self.brain, method):
                try:
                    result = getattr(self.brain, method)()
                    if result and isinstance(result, dict):
                        return result
                except Exception:
                    continue
        return None
    
    def _generate_fallback_data(self):
        states = ["ACTIVE", "IDLE", "DEGRADED", "ERROR"]
        return {"state": random.choice(states), "cycles": random.randint(0, 100), "errors": random.randint(0, 20), "success_rate": random.randint(40, 95), "health_score": random.randint(50, 100), "version": "4.2.3", "is_fallback": True, "timestamp": datetime.now().isoformat()}
    
    def _update_ui(self):
        data = self.brain_data
        if not data:
            return
        state = data.get("state", "UNKNOWN")
        cycles = data.get("cycles", 0)
        errors = data.get("errors", 0)
        success_rate = data.get("success_rate", 0)
        is_fallback = data.get("is_fallback", False)
        
        health_score = data.get("health_score")
        if health_score is None:
            score = 100.0
            score -= min(errors * 2, 30)
            if state in ["ERROR", "STOPPED"]:
                score -= 30
            elif state == "DEGRADED":
                score -= 15
            if success_rate > 50:
                score += (success_rate - 50) * 0.2
            health_score = max(0, min(100, round(score, 2)))
            data["health_score"] = health_score
        
        if self.state_card:
            self.state_card.update_value(state, color=self._get_state_color(state))
            self.state_card.update_subtitle("Brain state")
        if self.cycles_card:
            self.cycles_card.update_value(str(cycles))
        if self.errors_card:
            self.errors_card.update_value(str(errors), color="#EF4444" if errors > 0 else "#22C55E")
        if self.success_card:
            self.success_card.update_value(f"{success_rate:.1f}%", color=self._get_score_color(success_rate))
        if self.health_card:
            self.health_card.update_value(f"{health_score:.1f}%", color=self._get_score_color(health_score))
            self.health_card.update_subtitle("Brain health" + (" (fallback)" if is_fallback else ""))
        if self.status_indicator:
            self.status_indicator.set_status(state not in ["ERROR", "STOPPED"])
        
        insights = self._generate_insights(data)
        for i, card in enumerate(self.insight_cards):
            if i < len(insights):
                insight = insights[i]
                card.update(insight.get("title", "---"), insight.get("content", "No data available"))
            else:
                card.update("---", "No data available")
        
        if self.details_text:
            details_data = {"timestamp": datetime.now().isoformat(), "brain_data": data, "update_count": self.update_count, "success_count": self.success_count, "error_count": self.error_count, "is_fallback": is_fallback, "brain_available": self._brain_available, "active_instance": self.active_brain_name, "instances": list(self.brain_instances.keys())}
            if self.last_error:
                details_data["last_error"] = self.last_error
                details_data["last_error_time"] = self.last_error_time.isoformat() if self.last_error_time else None
            try:
                self.details_text.delete("1.0", "end")
                text = json.dumps(details_data, indent=2, default=str)
                if len(text) > 5000:
                    text = text[:5000] + "\n... (truncated)"
                self.details_text.insert("1.0", text)
            except Exception as e:
                print(f"[Brain GUI] Details update error: {e}")
    
    def _get_state_color(self, state: str) -> str:
        upper = state.upper()
        if upper in ["ACTIVE", "RUNNING", "ONLINE"]:
            return "#22C55E"
        elif upper in ["IDLE", "STANDBY"]:
            return "#F59E0B"
        elif upper in ["DEGRADED", "WARNING"]:
            return "#F97316"
        elif upper in ["ERROR", "STOPPED"]:
            return "#EF4444"
        else:
            return "#8D9AAA"
    
    def _get_score_color(self, score: float) -> str:
        if score >= 80:
            return "#22C55E"
        elif score >= 50:
            return "#F59E0B"
        else:
            return "#EF4444"
    
    def _generate_insights(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        insights = []
        state = data.get("state", "UNKNOWN")
        cycles = data.get("cycles", 0)
        errors = data.get("errors", 0)
        success_rate = data.get("success_rate", 0)
        health_score = data.get("health_score", 0)
        
        if cycles > 0:
            insights.append({"title": "🧠 Activity", "content": f"Brain has processed {cycles} cycles with {success_rate:.1f}% success rate.", "category": "activity", "confidence": 90})
        else:
            insights.append({"title": "🧠 Activity", "content": "Brain is idle or has not processed any cycles yet.", "category": "activity", "confidence": 50})
        
        if state in ["ACTIVE", "RUNNING"]:
            insights.append({"title": "✅ Status", "content": "Brain is active and operational.", "category": "status", "confidence": 95})
        elif state == "DEGRADED":
            insights.append({"title": "⚠️ Status", "content": "Brain is degraded. Some modules may be unavailable.", "category": "status", "confidence": 70})
        elif state == "ERROR":
            insights.append({"title": "❌ Status", "content": "Brain is in error state. Check logs for details.", "category": "status", "confidence": 90})
        else:
            insights.append({"title": "⏸️ Status", "content": f"Brain is in {state} state.", "category": "status", "confidence": 60})
        
        if health_score >= 80:
            insights.append({"title": "❤️ Health", "content": f"Brain health score is {health_score:.1f}% – excellent condition.", "category": "health", "confidence": health_score})
        elif health_score >= 50:
            insights.append({"title": "❤️ Health", "content": f"Brain health score is {health_score:.1f}% – moderate condition. Monitor closely.", "category": "health", "confidence": health_score})
        else:
            insights.append({"title": "❤️ Health", "content": f"Brain health score is {health_score:.1f}% – critical condition. Immediate attention required.", "category": "health", "confidence": health_score})
        
        if errors > 0:
            insights.append({"title": "🐛 Errors", "content": f"Brain has {errors} errors. Recommended to check logs and restart if necessary.", "category": "errors", "confidence": 70})
        else:
            insights.append({"title": "✅ Errors", "content": "No errors detected. Brain is running cleanly.", "category": "errors", "confidence": 90})
        
        insights.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        return insights[:4]
    
    def _update_error_display(self, error: Exception):
        try:
            if self.details_text:
                self.details_text.delete("1.0", "end")
                self.details_text.insert("1.0", f"❌ ERROR\n\nError: {error}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nUpdates: {self.update_count}\nSuccess: {self.success_count}\nErrors: {self.error_count}\n\nTraceback:\n{traceback.format_exc()}")
            if self.status_indicator:
                self.status_indicator.set_status(False)
        except Exception:
            pass
    
    def refresh(self):
        if self.refresh_btn:
            self.refresh_btn.configure(state="disabled", text="⏳ Refreshing...")
            self.update_idletasks()
        try:
            self.update_data()
            self._update_selector()
        finally:
            if self.refresh_btn:
                self.refresh_btn.configure(state="normal", text="🔄 Refresh")
    
    def stop(self):
        self.is_running = False
        if self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
    
    def destroy(self):
        self.stop()
        super().destroy()


# ============================================================
# LEARNING PAGE
# ============================================================

class Learning(IntelligencePage):
    """Learning Engine Status."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.engine_status = {}
        self.module_specs = []
        self.knowledge_stats = {}
        self.history = []
        self.learning_integration = None
        self.is_connected = False
        self.last_error = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = 3000
        self.bot = None
        self._last_module_hash = None
        
        self.learning_status = None
        self.last_update_label = None
        self.refresh_btn = None
        self.cycles_card = None
        self.modules_card = None
        self.errors_card = None
        self.knowledge_card = None
        self.confidence_card = None
        self.progress = None
        self.modules_container = None
        self.module_labels = []
        self.details_text = None
        
        self._build_ui()
        self.after(500, self.update_data)
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        ctk.CTkLabel(header, text="📚 Learning Engine", font=("Segoe UI", 22, "bold"), text_color="#E8EDF2").pack(side="left")
        self.learning_status = StatusIndicator(header, label="Learning")
        self.learning_status.pack(side="right", padx=10)
        self.last_update_label = ctk.CTkLabel(header, text="Last update: --", font=("Segoe UI", 10), text_color="#5F6B78")
        self.last_update_label.pack(side="right", padx=10)
        self.refresh_btn = ctk.CTkButton(header, text="🔄 Refresh", width=80, height=28, font=("Segoe UI", 11), fg_color="#3B82F6", hover_color="#2563EB", command=self.refresh)
        self.refresh_btn.pack(side="right", padx=10)
        
        metrics_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        metrics_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(2, weight=1)
        metrics_frame.grid_columnconfigure(3, weight=1)
        metrics_frame.grid_columnconfigure(4, weight=1)
        ctk.CTkLabel(metrics_frame, text="📊 Learning Metrics", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=5, padx=15, pady=10, sticky="w")
        
        self.cycles_card = MetricCard(metrics_frame, title="🔄 Learning Cycles", value="0")
        self.cycles_card.grid(row=1, column=0, padx=6, pady=8, sticky="nsew")
        self.modules_card = MetricCard(metrics_frame, title="📦 Modules", value="0")
        self.modules_card.grid(row=1, column=1, padx=6, pady=8, sticky="nsew")
        self.errors_card = MetricCard(metrics_frame, title="❌ Errors", value="0")
        self.errors_card.grid(row=1, column=2, padx=6, pady=8, sticky="nsew")
        self.knowledge_card = MetricCard(metrics_frame, title="📚 Knowledge", value="0")
        self.knowledge_card.grid(row=1, column=3, padx=6, pady=8, sticky="nsew")
        self.confidence_card = MetricCard(metrics_frame, title="🎯 Avg Confidence", value="0%")
        self.confidence_card.grid(row=1, column=4, padx=6, pady=8, sticky="nsew")
        
        self.progress = LearningProgress(self)
        self.progress.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        modules_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        modules_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        modules_frame.grid_columnconfigure(0, weight=1)
        modules_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(modules_frame, text="📋 Registered Modules", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")
        self.modules_container = ctk.CTkScrollableFrame(modules_frame, fg_color="transparent", height=150)
        self.modules_container.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.modules_container.grid_columnconfigure(0, weight=1)
        self.modules_container.grid_columnconfigure(1, weight=1)
        self.module_labels = []
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(details, text="📋 Learning Details", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.details_text = ctk.CTkTextbox(details, font=("Consolas", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=120)
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def set_bot(self, bot):
        self.bot = bot
    
    def set_learning(self, learning):
        self.learning_integration = learning
    
    def update_data(self):
        if not self.is_running:
            return
        try:
            self.update_count += 1
            self._collect_data()
            self._update_ui()
            self.is_connected = True
            self.success_count += 1
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            print(f"[Learning] Update error: {e}")
            self.learning_status.set_status(False)
        if self.is_running:
            self.after(self.update_interval, self.update_data)
    
    def _collect_data(self):
        self.engine_status = {}
        self.module_specs = []
        self.knowledge_stats = {}
        if self.learning_integration is not None:
            try:
                if hasattr(self.learning_integration, 'get_status'):
                    status = self.learning_integration.get_status()
                    if status:
                        self.engine_status.update(status)
                        self.is_connected = True
                elif hasattr(self.learning_integration, 'status'):
                    status = self.learning_integration.status()
                    if status:
                        self.engine_status.update(status)
                        self.is_connected = True
            except Exception as e:
                print(f"[Learning] Integration status error: {e}")
        try:
            from core.learning.engine import learning_engine
            if learning_engine:
                if hasattr(learning_engine, 'status'):
                    status = learning_engine.status()
                    if status:
                        self.engine_status.update(status)
                elif hasattr(learning_engine, 'get_state'):
                    state = learning_engine.get_state()
                    if state:
                        self.engine_status.update(state)
                if hasattr(learning_engine, 'registry') and learning_engine.registry:
                    try:
                        self.module_specs = learning_engine.registry.all()
                    except Exception as e:
                        print(f"[Learning] Registry error: {e}")
        except ImportError:
            pass
        except Exception as e:
            print(f"[Learning] Core engine error: {e}")
        try:
            from core.knowledge import knowledge
            if knowledge and hasattr(knowledge, 'stats'):
                stats = knowledge.stats()
                if stats:
                    self.knowledge_stats = {"total": getattr(stats, 'total', 0), "states": getattr(stats, 'state_count', 0), "avg_confidence": getattr(stats, 'avg_confidence', 0), "active": getattr(stats, 'active', 0), "archived": getattr(stats, 'archived', 0)}
        except ImportError:
            pass
        except Exception as e:
            print(f"[Learning] Knowledge error: {e}")
    
    def _update_ui(self):
        running = self.engine_status.get('running', False)
        initialized = self.engine_status.get('initialized', False)
        available = self.engine_status.get('available', False)
        if available and initialized:
            self.learning_status.set_status(running)
        else:
            self.learning_status.set_status(False)
        
        cycles = self.engine_status.get('cycles', 0)
        module_count = len(self.module_specs)
        errors = self.engine_status.get('errors', 0)
        self.cycles_card.update_value(str(cycles))
        self.modules_card.update_value(str(module_count))
        self.errors_card.update_value(str(errors))
        knowledge_total = self.knowledge_stats.get('total', 0)
        self.knowledge_card.update_value(str(knowledge_total))
        avg_conf = self.knowledge_stats.get('avg_confidence', 0)
        self.confidence_card.update_value(f"{avg_conf:.1f}%")
        
        try:
            learning_progress = min(1.0, cycles / 100) if cycles > 0 else 0
            if hasattr(self, 'progress') and self.progress and hasattr(self.progress, 'progress_bars') and 'learning' in self.progress.progress_bars:
                self.progress.progress_bars['learning'].set(learning_progress)
        except Exception:
            pass
        try:
            module_progress = min(1.0, module_count / 30) if module_count > 0 else 0
            if hasattr(self, 'progress') and self.progress and hasattr(self.progress, 'progress_bars') and 'modules' in self.progress.progress_bars:
                self.progress.progress_bars['modules'].set(module_progress)
        except Exception:
            pass
        
        self._update_modules()
        
        details_data = {"timestamp": datetime.now().isoformat(), "update_count": self.update_count, "success_count": self.success_count, "error_count": self.error_count, "engine_status": self.engine_status, "knowledge_stats": self.knowledge_stats, "module_count": module_count, "has_learning": self.learning_integration is not None, "has_core_engine": 'core.learning.engine' in str(self.engine_status)}
        if self.last_error:
            details_data["last_error"] = self.last_error
        if hasattr(self, 'details_text') and self.details_text:
            try:
                self.details_text.delete("1.0", "end")
                text = json.dumps(details_data, indent=2, default=str)
                if len(text) > 3000:
                    text = text[:3000] + "\n... (truncated)"
                self.details_text.insert("1.0", text)
            except Exception as e:
                print(f"[Learning] Details update error: {e}")
        self.last_update_label.configure(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
    
    def _update_modules(self):
        current_hash = hash(str(self.module_specs))
        if hasattr(self, '_last_module_hash') and self._last_module_hash == current_hash:
            return
        self._last_module_hash = current_hash
        for frame in self.module_labels:
            try:
                frame.destroy()
            except Exception:
                pass
        self.module_labels.clear()
        if self.module_specs:
            for i, spec in enumerate(self.module_specs[:20]):
                if hasattr(spec, 'name'):
                    name = spec.name
                    enabled = getattr(spec, 'enabled', False)
                    version = getattr(spec, 'version', '1.0')
                    priority = getattr(spec, 'priority', 0)
                elif isinstance(spec, dict):
                    name = spec.get('name', 'Unknown')
                    enabled = spec.get('enabled', False)
                    version = spec.get('version', '1.0')
                    priority = spec.get('priority', 0)
                else:
                    continue
                frame = ctk.CTkFrame(self.modules_container, fg_color="#1A2430" if i % 2 == 0 else "transparent", corner_radius=4)
                row = i // 2
                col = i % 2
                frame.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
                frame.grid_columnconfigure(0, weight=1)
                status_icon = "✅" if enabled else "❌"
                status_color = "#22C55E" if enabled else "#EF4444"
                label = ctk.CTkLabel(frame, text=f"{status_icon} {name} v{version} (prio:{priority})", font=("Segoe UI", 11), text_color=status_color, anchor="w")
                label.grid(row=0, column=0, padx=10, pady=6, sticky="w")
                self.module_labels.append(frame)
        else:
            empty_frame = ctk.CTkFrame(self.modules_container, fg_color="transparent")
            empty_frame.grid(row=0, column=0, padx=10, pady=20)
            empty_frame.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(empty_frame, text="📦", font=("Segoe UI", 32), text_color="#5F6B78").grid(row=0, column=0, pady=(0, 5))
            ctk.CTkLabel(empty_frame, text="No Modules Registered", font=("Segoe UI", 16, "bold"), text_color="#E8EDF2").grid(row=1, column=0)
            ctk.CTkLabel(empty_frame, text="Modules will appear here when registered by Learning Engine.", font=("Segoe UI", 12), text_color="#5F6B78").grid(row=2, column=0, pady=(5, 10))
            tips = ["• Start the master engine to register modules.", "• Check 'Learning Details' above for engine status."]
            for i, tip in enumerate(tips):
                ctk.CTkLabel(empty_frame, text=tip, font=("Segoe UI", 10), text_color="#5F6B78").grid(row=3+i, column=0, pady=1, sticky="w")
            self.module_labels.append(empty_frame)
    
    def refresh(self):
        self.update_data()
    
    def stop(self):
        self.is_running = False
    
    def destroy(self):
        self.stop()
        super().destroy()


# ============================================================
# MEMORY PAGE
# ============================================================

class Memory(IntelligencePage):
    """Memory systems status view."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.memory_stats_data = {}
        self.bot = None
        self.memory_status = None
        self.last_update_label = None
        self.short_term_card = None
        self.long_term_card = None
        self.memory_stats = None
        self.details_text = None
        self._build_ui()
        self.after(500, self.update_data)
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        ctk.CTkLabel(header, text="💾 Memory Systems", font=("Segoe UI", 22, "bold"), text_color="#E8EDF2").pack(side="left")
        self.memory_status = StatusIndicator(header, label="Memory")
        self.memory_status.pack(side="right", padx=10)
        self.last_update_label = ctk.CTkLabel(header, text="Last update: --", font=("Segoe UI", 10), text_color="#5F6B78")
        self.last_update_label.pack(side="right", padx=10)
        
        self.short_term_card = MetricCard(self, title="⚡ Short-term Memory", value="0", subtitle="Items")
        self.short_term_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.long_term_card = MetricCard(self, title="📚 Long-term Memory", value="0", subtitle="Items")
        self.long_term_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.memory_stats = MemoryStats(self)
        self.memory_stats.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(details, text="📋 Memory Details", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.details_text = ctk.CTkTextbox(details, font=("Consolas", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=120)
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def update_data(self):
        if not self.is_running:
            return
        try:
            memory_data = self._get_memory_data()
            if memory_data:
                total, categories = self._parse_memory_data(memory_data)
                self._update_ui(total, categories, memory_data)
            else:
                self._show_no_data()
        except Exception as e:
            print(f"[Memory] Update error: {e}")
            if self.details_text:
                self.details_text.delete("1.0", "end")
                self.details_text.insert("1.0", f"Error: {e}\n\n{traceback.format_exc()}")
            if self.memory_status:
                self.memory_status.set_status(False)
        if self.is_running:
            self.after(self.update_interval, self.update_data)
    
    def _parse_memory_data(self, memory_data: Dict):
        total = 0
        categories = {}
        raw_categories = memory_data.get('categories', {})
        if isinstance(raw_categories, dict):
            categories = raw_categories
            for key, value in categories.items():
                if isinstance(value, (int, float)):
                    total += value
                elif isinstance(value, dict):
                    total += len(value)
                elif isinstance(value, (list, tuple)):
                    total += len(value)
                elif value is not None:
                    try:
                        total += int(value)
                    except (ValueError, TypeError):
                        pass
        elif isinstance(raw_categories, (list, tuple)):
            total = len(raw_categories)
            categories = {'items': total}
        else:
            total_from_data = memory_data.get('total', 0)
            if isinstance(total_from_data, (int, float)):
                total = int(total_from_data)
            categories = {'total': total}
        try:
            total = int(total)
        except (ValueError, TypeError):
            total = 0
        if not isinstance(categories, dict):
            categories = {'items': total}
        return total, categories
    
    def _update_ui(self, total: int, categories: dict, memory_data: dict):
        if self.short_term_card:
            self.short_term_card.update_value(str(total))
        if self.long_term_card:
            self.long_term_card.update_value(str(len(categories) if categories else 0))
        if self.memory_status:
            self.memory_status.set_status(total > 0)
        if hasattr(self.memory_stats, 'update_stats'):
            self.memory_stats.update_stats(categories)
        if self.details_text:
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", json.dumps({"timestamp": datetime.now().isoformat(), "total": total, "categories": categories, "source": memory_data.get('source', 'unknown')}, indent=2, default=str)[:3000])
        if self.last_update_label:
            self.last_update_label.configure(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
    
    def _show_no_data(self):
        if self.memory_status:
            self.memory_status.set_status(False)
        if self.details_text:
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", "⚠️ Memory data not available.\n\nPlease ensure:\n1. core.memory is properly imported\n2. Memory engine is initialized\n3. Memory data is accessible")
    
    def _get_memory_data(self) -> Dict[str, Any]:
        sources = [self._get_from_core_memory, self._get_from_learning_memory, self._get_from_semantic_memory, self._get_from_bot, self._get_from_brain]
        for source_func in sources:
            try:
                result = source_func()
                if result:
                    return result
            except Exception as e:
                print(f"[Memory] Source error: {e}")
                continue
        return {}
    
    def _get_from_core_memory(self) -> Dict:
        try:
            from core.memory import memory
            if memory is not None:
                if hasattr(memory, 'stats'):
                    stats = memory.stats()
                    if stats is not None:
                        return self._parse_memory_stats(stats, 'core.memory')
                if hasattr(memory, 'get_stats'):
                    stats = memory.get_stats()
                    if stats is not None:
                        return self._parse_memory_stats(stats, 'core.memory')
                if hasattr(memory, 'status'):
                    status = memory.status()
                    if status and isinstance(status, dict):
                        mem_stats = status.get('stats', {})
                        if mem_stats:
                            return self._parse_memory_stats(mem_stats, 'core.memory(status)')
        except ImportError:
            pass
        return {}
    
    def _get_from_learning_memory(self) -> Dict:
        try:
            from core.learning.learning_memory import learning_memory
            if learning_memory is not None and hasattr(learning_memory, 'stats'):
                stats = learning_memory.stats()
                if stats is not None:
                    return self._parse_memory_stats(stats, 'learning_memory')
        except ImportError:
            pass
        return {}
    
    def _get_from_semantic_memory(self) -> Dict:
        try:
            from core.learning.semantic_memory import semantic_memory
            if semantic_memory is not None:
                if hasattr(semantic_memory, 'count'):
                    count = semantic_memory.count()
                    if count is not None:
                        try:
                            count_int = int(count)
                            return {'total': count_int, 'categories': {'semantic': count_int}, 'source': 'semantic_memory(count)'}
                        except (ValueError, TypeError):
                            pass
                if hasattr(semantic_memory, 'get_all'):
                    items = semantic_memory.get_all()
                    if items is not None:
                        if isinstance(items, (list, tuple)):
                            return {'total': len(items), 'categories': {'semantic': len(items)}, 'source': 'semantic_memory(get_all)'}
                        elif isinstance(items, dict):
                            return {'total': len(items), 'categories': {'semantic': len(items)}, 'source': 'semantic_memory(get_all)'}
        except ImportError:
            pass
        return {}
    
    def _get_from_bot(self) -> Dict:
        if self.bot is not None:
            try:
                if hasattr(self.bot, 'get_memory_stats'):
                    stats = self.bot.get_memory_stats()
                    if stats is not None:
                        return self._parse_memory_stats(stats, 'bot')
                if hasattr(self.bot, 'get_status'):
                    status = self.bot.get_status()
                    if status and isinstance(status, dict):
                        memory_keys = ['memory', 'mem', 'memory_stats', 'mem_stats']
                        for key in memory_keys:
                            if key in status:
                                mem_data = status[key]
                                if mem_data is not None:
                                    return self._parse_memory_stats(mem_data, 'bot(status)')
            except Exception:
                pass
        return {}
    
    def _get_from_brain(self) -> Dict:
        if self.bot is not None and hasattr(self.bot, 'brain'):
            brain = self.bot.brain
            if brain is not None:
                try:
                    if hasattr(brain, 'get_state'):
                        state = brain.get_state()
                        if state and isinstance(state, dict):
                            memory_keys = ['memory', 'short_term_memory', 'long_term_memory']
                            for key in memory_keys:
                                if key in state:
                                    mem_data = state[key]
                                    if mem_data is not None:
                                        if isinstance(mem_data, (list, tuple)):
                                            return {'total': len(mem_data), 'categories': {key: len(mem_data)}, 'source': f'brain({key})'}
                except Exception:
                    pass
        return {}
    
    def _parse_memory_stats(self, stats: Any, source: str) -> Dict[str, Any]:
        result = {'source': source}
        if stats is None:
            return {}
        if isinstance(stats, dict):
            if 'total' in stats:
                total = stats['total']
                if isinstance(total, (int, float)):
                    result['total'] = int(total)
                else:
                    result['total'] = 0
            categories = {}
            for key, value in stats.items():
                if key == 'total':
                    continue
                if isinstance(value, (int, float)):
                    categories[key] = int(value)
                elif isinstance(value, (list, tuple)):
                    categories[key] = len(value)
                elif isinstance(value, dict):
                    if value:
                        if all(isinstance(v, (int, float)) for v in value.values()):
                            categories[key] = int(sum(value.values()))
                        else:
                            categories[key] = len(value)
                    else:
                        categories[key] = 0
            if not categories:
                for key, value in stats.items():
                    if isinstance(value, (int, float)):
                        categories[key] = int(value)
            if not categories and 'total' in result:
                categories['items'] = result['total']
            result['categories'] = categories
            if 'total' not in result:
                total = 0
                for value in categories.values():
                    if isinstance(value, (int, float)):
                        total += value
                result['total'] = total
            return result
        if isinstance(stats, (list, tuple)):
            total = len(stats)
            return {'total': total, 'categories': {'items': total}, 'source': source}
        if isinstance(stats, (int, float)):
            return {'total': int(stats), 'categories': {'items': int(stats)}, 'source': source}
        return {}
    
    def set_bot(self, bot):
        self.bot = bot
    
    def refresh(self):
        self.update_data()
    
    def stop(self):
        self.is_running = False
    
    def destroy(self):
        self.stop()
        super().destroy()


# ============================================================
# PATTERN PAGE
# ============================================================

class Pattern(IntelligencePage):
    """Pattern recognition status view."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pattern_data = {}
        self.bot = None
        self.pattern_status = None
        self.last_update_label = None
        self.total_patterns = None
        self.unique_patterns = None
        self.pattern_list = None
        self.details_text = None
        self._build_ui()
        self.after(500, self.update_data)
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        ctk.CTkLabel(header, text="🔍 Pattern Recognition", font=("Segoe UI", 22, "bold"), text_color="#E8EDF2").pack(side="left")
        self.pattern_status = StatusIndicator(header, label="Pattern")
        self.pattern_status.pack(side="right", padx=10)
        self.last_update_label = ctk.CTkLabel(header, text="Last update: --", font=("Segoe UI", 10), text_color="#5F6B78")
        self.last_update_label.pack(side="right", padx=10)
        
        self.total_patterns = MetricCard(self, title="📊 Total Patterns", value="0", subtitle="Detected patterns")
        self.total_patterns.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.unique_patterns = MetricCard(self, title="🔐 Unique Patterns", value="0", subtitle="Unique fingerprints")
        self.unique_patterns.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.pattern_list = PatternList(self)
        self.pattern_list.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(details, text="📋 Pattern Details", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.details_text = ctk.CTkTextbox(details, font=("Consolas", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=120)
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def update_data(self):
        if not self.is_running:
            return
        try:
            pattern_data = self._get_pattern_data()
            if pattern_data:
                total = pattern_data.get('patterns', 0)
                unique = pattern_data.get('unique_fingerprints', 0)
                self.total_patterns.update_value(str(total))
                self.unique_patterns.update_value(str(unique))
                self.pattern_status.set_status(True)
                top_patterns = pattern_data.get('top_tokens', {})
                if top_patterns:
                    sorted_patterns = sorted(top_patterns.items(), key=lambda x: x[1], reverse=True)
                    pattern_names = [p[0] for p in sorted_patterns[:10]]
                    self.pattern_list.update_patterns(pattern_names)
                else:
                    self.pattern_list.update_patterns([])
                self.details_text.delete("1.0", "end")
                self.details_text.insert("1.0", json.dumps({"timestamp": datetime.now().isoformat(), "total_patterns": total, "unique_patterns": unique, "top_patterns": top_patterns, "raw_data": pattern_data}, indent=2, default=str)[:3000])
                self.last_update_label.configure(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
            else:
                self.pattern_status.set_status(False)
                self.details_text.delete("1.0", "end")
                self.details_text.insert("1.0", "⚠️ Pattern data not available.\n\nPlease ensure:\n1. core.learning.pattern is properly imported\n2. Pattern Engine is initialized")
                self.pattern_list.update_patterns([])
        except Exception as e:
            print(f"[PatternView] Update error: {e}")
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", f"Error: {e}")
            self.pattern_status.set_status(False)
        if self.is_running:
            self.after(self.update_interval, self.update_data)
    
    def _get_pattern_data(self) -> dict:
        result = {}
        try:
            from core.learning.pattern import pattern
            if pattern and hasattr(pattern, 'get_state'):
                state = pattern.get_state()
                if state:
                    result = state
                    result['source'] = 'core.learning.pattern'
                    return result
        except ImportError:
            pass
        if self.bot:
            try:
                if hasattr(self.bot, 'get_patterns'):
                    patterns = self.bot.get_patterns()
                    if patterns:
                        if isinstance(patterns, dict):
                            result = patterns
                        else:
                            result = {'patterns': len(patterns), 'data': patterns}
                        result['source'] = 'bot'
                        return result
            except Exception:
                pass
        if self.bot and hasattr(self.bot, 'scanner'):
            try:
                scanner = self.bot.scanner
                if scanner and hasattr(scanner, 'get_summary'):
                    summary = scanner.get_summary()
                    if summary:
                        result = {'patterns': summary.get('total', 0), 'top_tokens': {}, 'source': 'scanner'}
                        return result
            except Exception:
                pass
        return result
    
    def set_bot(self, bot):
        self.bot = bot
    
    def refresh(self):
        self.update_data()
    
    def stop(self):
        self.is_running = False
    
    def destroy(self):
        self.stop()
        super().destroy()


# ============================================================
# PREDICTION PAGE
# ============================================================

class Prediction(IntelligencePage):
    """Predictions & Forecasts."""
    
    def __init__(self, parent, *args, **kwargs):
        self.forecast_data = {}
        self.fallback_mode = False
        self.last_error = None
        self.last_error_time = None
        self.brain_instance = None
        self.brain = None
        self._brain_available = False
        self.bot = None
        self.learning_integration = None
        self.is_running = True
        self.update_interval = 3000
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_connected = False
        
        self.prediction_status = None
        self.forecast_card = None
        self.confidence_card = None
        self.bullish_conf = None
        self.bearish_conf = None
        self.neutral_conf = None
        self.details_text = None
        self.last_update_label = None
        self.refresh_btn = None
        self._after_id = None
        
        super().__init__(parent, *args, **kwargs)
        self._build_ui()
        self.after(500, self.update_data)
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)
        ctk.CTkLabel(header, text="🔮 Predictions & Forecasts", font=("Segoe UI", 22, "bold"), text_color="#E8EDF2").grid(row=0, column=0, sticky="w")
        self.prediction_status = StatusIndicator(header, label="Prediction")
        self.prediction_status.grid(row=0, column=1, padx=10)
        self.last_update_label = ctk.CTkLabel(header, text="Last update: --", font=("Segoe UI", 10), text_color="#5F6B78")
        self.last_update_label.grid(row=0, column=2, padx=10)
        self.refresh_btn = ctk.CTkButton(header, text="🔄 Refresh", width=80, height=28, font=("Segoe UI", 11), fg_color="#3B82F6", hover_color="#2563EB", command=self.refresh)
        self.refresh_btn.grid(row=0, column=3, padx=10)
        
        self.forecast_card = MetricCard(self, title="📊 Forecast", value="NEUTRAL", subtitle="Direction")
        self.forecast_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.confidence_card = MetricCard(self, title="🎯 Confidence", value="0%", subtitle="Accuracy")
        self.confidence_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        bars = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        bars.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        bars.grid_columnconfigure(0, weight=1)
        bars.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(bars, text="📈 Confidence Analysis", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")
        self.bullish_conf = ConfidenceBar(bars, label="Bullish Confidence", value=0)
        self.bullish_conf.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        self.bearish_conf = ConfidenceBar(bars, label="Bearish Confidence", value=0)
        self.bearish_conf.grid(row=1, column=1, padx=15, pady=5, sticky="ew")
        self.neutral_conf = ConfidenceBar(bars, label="Neutral Confidence", value=0)
        self.neutral_conf.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew")
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        details.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(details, text="📋 Prediction Details", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.details_text = ctk.CTkTextbox(details, font=("Consolas", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=120)
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
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
    
    def update_data(self):
        if not self.is_running:
            return
        try:
            self.update_count += 1
            self._update_brain_reference()
            forecast = self._get_forecast_safely()
            if forecast:
                self.forecast_data = forecast
                self.is_connected = True
                self.success_count += 1
                self.fallback_mode = False
                self.last_error = None
            else:
                self.forecast_data = self._generate_fallback_data()
                self.is_connected = False
                self.fallback_mode = True
                self.error_count += 1
                self.last_error = "Brain unavailable, using fallback data"
                self.last_error_time = datetime.now()
            self._update_ui()
            if self.last_update_label:
                self.last_update_label.configure(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            print(f"[Prediction] Update error: {e}")
            traceback.print_exc()
            self._update_error_display(e)
            if self.prediction_status:
                self.prediction_status.set_status(False)
        if self.is_running:
            try:
                self._after_id = self.after(self.update_interval, self.update_data)
            except Exception as e:
                print(f"[Prediction] Schedule error: {e}")
    
    def _get_forecast_safely(self):
        if not self.brain:
            return None
        if hasattr(self.brain, 'forecast'):
            try:
                result = self.brain.forecast()
                if result and isinstance(result, dict) and 'forecast' in result and 'confidence' in result:
                    return result
            except Exception as e:
                print(f"[Prediction] forecast() error: {e}")
        if hasattr(self.brain, 'get_forecast'):
            try:
                result = self.brain.get_forecast()
                if result and isinstance(result, dict) and 'forecast' in result and 'confidence' in result:
                    return result
            except Exception as e:
                print(f"[Prediction] get_forecast() error: {e}")
        if hasattr(self.brain, 'snapshot'):
            try:
                snapshot = self.brain.snapshot()
                if snapshot and isinstance(snapshot, dict):
                    market = snapshot.get('market', {})
                    if market and isinstance(market, dict):
                        forecast = market.get('forecast', 'NEUTRAL')
                        confidence = market.get('confidence', 0)
                        if forecast and confidence is not None:
                            return {'forecast': forecast, 'confidence': confidence, 'timestamp': datetime.now().isoformat(), 'source': 'snapshot'}
            except Exception as e:
                print(f"[Prediction] snapshot() error: {e}")
        if hasattr(self.brain, 'market_intelligence'):
            try:
                intelligence = self.brain.market_intelligence()
                if intelligence and isinstance(intelligence, dict):
                    forecast = intelligence.get('forecast', 'NEUTRAL')
                    confidence = intelligence.get('confidence', 0)
                    if forecast and confidence is not None:
                        return {'forecast': forecast, 'confidence': confidence, 'timestamp': datetime.now().isoformat(), 'source': 'market_intelligence'}
            except Exception as e:
                print(f"[Prediction] market_intelligence() error: {e}")
        return None
    
    def _generate_fallback_data(self):
        directions = ["BULLISH", "BEARISH", "NEUTRAL"]
        direction = random.choice(directions)
        confidence = random.randint(30, 85)
        if direction == "BULLISH":
            bullish = confidence
            bearish = random.randint(5, 40)
            neutral = 100 - bullish - bearish
        elif direction == "BEARISH":
            bearish = confidence
            bullish = random.randint(5, 40)
            neutral = 100 - bullish - bearish
        else:
            bullish = random.randint(20, 50)
            bearish = random.randint(20, 50)
            neutral = 100 - bullish - bearish
        total = bullish + bearish + neutral
        if total != 100:
            neutral += (100 - total)
            neutral = max(0, min(100, neutral))
        reasons = ["Bullish breakout detected", "Bearish divergence confirmed", "Support level holding strong", "Resistance level breaking", "Volume spike indicates momentum", "RSI oversold condition", "MACD crossover bullish", "Price above moving averages", "Market sentiment improving", "Technical indicators aligned"]
        return {"forecast": direction, "confidence": confidence, "bullish_probability": bullish, "bearish_probability": bearish, "neutral_probability": neutral, "reason": random.choice(reasons), "timestamp": datetime.now().isoformat(), "is_fallback": True, "source": "fallback_generator"}
    
    def _update_ui(self):
        if not self.forecast_data:
            return
        forecast = self.forecast_data
        direction = forecast.get("forecast", "NEUTRAL")
        confidence = forecast.get("confidence", 0)
        is_fallback = forecast.get("is_fallback", False)
        if self.forecast_card:
            color = self._get_direction_color(direction)
            self.forecast_card.update_value(direction, color=color)
            subtitle = f"Confidence: {confidence:.0f}%"
            if is_fallback:
                subtitle += " (fallback)"
            self.forecast_card.update_subtitle(subtitle)
        if self.confidence_card:
            color = "#22C55E" if confidence >= 60 else "#F59E0B" if confidence >= 40 else "#EF4444"
            self.confidence_card.update_value(f"{confidence:.0f}%", color=color)
        if self.prediction_status:
            self.prediction_status.set_status(confidence > 50 and not is_fallback)
        bullish = forecast.get("bullish_probability", 0)
        bearish = forecast.get("bearish_probability", 0)
        neutral = forecast.get("neutral_probability", 0)
        if bullish == 0 and bearish == 0 and neutral == 0:
            if direction == "BULLISH":
                bullish = confidence
                bearish = max(0, 100 - confidence - 10)
                neutral = 10
            elif direction == "BEARISH":
                bearish = confidence
                bullish = max(0, 100 - confidence - 10)
                neutral = 10
            else:
                bullish = 20
                bearish = 20
                neutral = 60
        try:
            bullish = int(bullish)
            bearish = int(bearish)
            neutral = int(neutral)
            total = bullish + bearish + neutral
            if total != 100:
                if total > 0:
                    bullish = int(bullish * 100 / total)
                    bearish = int(bearish * 100 / total)
                    neutral = 100 - bullish - bearish
                else:
                    bullish = 33
                    bearish = 33
                    neutral = 34
        except Exception:
            bullish = 33
            bearish = 33
            neutral = 34
        if self.bullish_conf:
            self.bullish_conf.set_value(bullish)
        if self.bearish_conf:
            self.bearish_conf.set_value(bearish)
        if self.neutral_conf:
            self.neutral_conf.set_value(neutral)
        if self.details_text:
            details_data = {"timestamp": datetime.now().isoformat(), "forecast": forecast, "update_count": self.update_count, "success_count": self.success_count, "error_count": self.error_count, "is_fallback": is_fallback, "brain_available": self._brain_available, "connected": self.is_connected}
            if self.last_error:
                details_data["last_error"] = self.last_error
                details_data["last_error_time"] = self.last_error_time.isoformat() if self.last_error_time else None
            try:
                self.details_text.delete("1.0", "end")
                text = json.dumps(details_data, indent=2, default=str)
                if len(text) > 5000:
                    text = text[:5000] + "\n... (truncated)"
                self.details_text.insert("1.0", text)
            except Exception as e:
                print(f"[Prediction] Details update error: {e}")
    
    def _get_direction_color(self, direction: str) -> str:
        upper = direction.upper()
        if upper == "BULLISH":
            return "#22C55E"
        elif upper == "BEARISH":
            return "#EF4444"
        else:
            return "#F59E0B"
    
    def _update_error_display(self, error: Exception):
        try:
            if self.details_text:
                self.details_text.delete("1.0", "end")
                self.details_text.insert("1.0", f"❌ ERROR\n\nError: {error}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nUpdates: {self.update_count}\nSuccess: {self.success_count}\nErrors: {self.error_count}\n\nTraceback:\n{traceback.format_exc()}")
            if self.prediction_status:
                self.prediction_status.set_status(False)
        except Exception:
            pass
    
    def refresh(self):
        if self.refresh_btn:
            self.refresh_btn.configure(state="disabled", text="⏳ Refreshing...")
            self.update_idletasks()
        try:
            self.update_data()
        finally:
            if self.refresh_btn:
                self.refresh_btn.configure(state="normal", text="🔄 Refresh")
    
    def stop(self):
        self.is_running = False
        if self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
    
    def destroy(self):
        self.stop()
        super().destroy()


# ============================================================
# DECISION PAGE
# ============================================================

class Decision(IntelligencePage):
    """Decision Support."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.decision_data = {}
        self.alternatives = []
        self.decision_history = []
        self.risk_assessment = {}
        self.brain_instance = None
        self.brain = None
        self._brain_available = False
        self.is_connected = False
        self.last_error = None
        self.last_error_time = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = 3000
        self.bot = None
        self.learning_integration = None
        self._ui_components = {}
        
        self.decision_status = None
        self.last_update_label = None
        self.refresh_btn = None
        self.decisions_made = None
        self.avg_confidence = None
        self.risk_level = None
        self.success_rate = None
        self.decision_card = None
        self.alternatives_text = None
        self.risk_text = None
        self.details_text = None
        
        self._build_ui()
        self.after(500, self.update_data)
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)
        ctk.CTkLabel(header, text="🎯 Decision Support", font=("Segoe UI", 22, "bold"), text_color="#E8EDF2").grid(row=0, column=0, sticky="w")
        self.decision_status = StatusIndicator(header, label="Decision")
        self.decision_status.grid(row=0, column=1, padx=10)
        self.last_update_label = ctk.CTkLabel(header, text="Last update: --", font=("Segoe UI", 10), text_color="#5F6B78")
        self.last_update_label.grid(row=0, column=2, padx=10)
        self.refresh_btn = ctk.CTkButton(header, text="🔄 Refresh", width=80, height=28, font=("Segoe UI", 11), fg_color="#3B82F6", hover_color="#2563EB", command=self.refresh)
        self.refresh_btn.grid(row=0, column=3, padx=10)
        
        metrics_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        metrics_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(2, weight=1)
        metrics_frame.grid_columnconfigure(3, weight=1)
        ctk.CTkLabel(metrics_frame, text="📊 Decision Metrics", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=4, padx=15, pady=10, sticky="w")
        self.decisions_made = MetricCard(metrics_frame, title="📋 Decisions Made", value="0")
        self.decisions_made.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
        self.avg_confidence = MetricCard(metrics_frame, title="🎯 Avg Confidence", value="0%")
        self.avg_confidence.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")
        self.risk_level = MetricCard(metrics_frame, title="⚠️ Risk Level", value="MEDIUM")
        self.risk_level.grid(row=1, column=2, padx=8, pady=8, sticky="nsew")
        self.success_rate = MetricCard(metrics_frame, title="✅ Success Rate", value="0%")
        self.success_rate.grid(row=1, column=3, padx=8, pady=8, sticky="nsew")
        
        self.decision_card = DecisionCard(self)
        self.decision_card.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        alt_risk_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        alt_risk_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        alt_risk_frame.grid_columnconfigure(0, weight=1)
        alt_risk_frame.grid_columnconfigure(1, weight=1)
        alt_risk_frame.grid_rowconfigure(0, weight=1)
        
        alt_frame = ctk.CTkFrame(alt_risk_frame, fg_color="transparent")
        alt_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        alt_frame.grid_rowconfigure(1, weight=1)
        alt_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(alt_frame, text="🔄 Alternatives", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.alternatives_text = ctk.CTkTextbox(alt_frame, font=("Segoe UI", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=100)
        self.alternatives_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        risk_frame = ctk.CTkFrame(alt_risk_frame, fg_color="transparent")
        risk_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        risk_frame.grid_rowconfigure(0, weight=0)
        risk_frame.grid_rowconfigure(1, weight=1)
        risk_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(risk_frame, text="⚠️ Risk Assessment", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.risk_text = ctk.CTkTextbox(risk_frame, font=("Consolas", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=100)
        self.risk_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(details, text="📋 Decision Details", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.details_text = ctk.CTkTextbox(details, font=("Consolas", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=120)
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
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
    
    def _update_brain_reference(self):
        if self.bot:
            if hasattr(self.bot, 'brain'):
                self.brain_instance = self.bot.brain
                self.brain = self.bot.brain
            elif hasattr(self.bot, '_brain'):
                self.brain_instance = self.bot._brain
                self.brain = self.bot._brain
            elif hasattr(self.bot, 'get_brain'):
                brain = self.bot.get_brain()
                if brain:
                    self.brain_instance = brain
                    self.brain = brain
        if not self.brain_instance and self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                self.brain_instance = self.learning_integration.brain
                self.brain = self.learning_integration.brain
            elif hasattr(self.learning_integration, 'get_brain'):
                brain = self.learning_integration.get_brain()
                if brain:
                    self.brain_instance = brain
                    self.brain = brain
        if not self.brain_instance:
            try:
                from core.brain import brain
                if brain:
                    self.brain_instance = brain
                    self.brain = brain
            except ImportError:
                pass
        self._brain_available = self.brain_instance is not None
    
    def _get_brain(self):
        if self.brain_instance:
            return self.brain_instance
        if hasattr(self, 'brain') and self.brain:
            return self.brain
        if self.bot:
            if hasattr(self.bot, 'brain'):
                return self.bot.brain
            elif hasattr(self.bot, '_brain'):
                return self.bot._brain
            elif hasattr(self.bot, 'get_brain'):
                return self.bot.get_brain()
        if self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                return self.learning_integration.brain
            elif hasattr(self.learning_integration, 'get_brain'):
                return self.learning_integration.get_brain()
        try:
            from core.brain import brain
            if brain:
                self.brain_instance = brain
                self.brain = brain
                return brain
        except ImportError:
            pass
        return None
    
    def _safe_brain_call(self, method_name: str, *args, **kwargs):
        brain = self._get_brain()
        if not brain:
            return None
        try:
            if hasattr(brain, method_name):
                result = getattr(brain, method_name)(*args, **kwargs)
                return result
            return None
        except Exception as e:
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            print(f"[Decision] {method_name} error: {e}")
            return None
    
    def update_data(self):
        if not self.is_running:
            return
        try:
            self.update_count += 1
            self._update_brain_reference()
            decision_data = self._safe_brain_call('decision_support')
            if decision_data and isinstance(decision_data, dict):
                self.decision_data = decision_data
                self._update_ui()
                self.is_connected = True
                self.success_count += 1
                if self.last_error:
                    self.last_error = None
                    self.last_error_time = None
            else:
                self._generate_fallback_data()
                self._update_ui()
                self.is_connected = False
            if hasattr(self, 'last_update_label'):
                self.last_update_label.configure(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            print(f"[Decision] Update error: {e}")
            self._update_error_display(e)
            if hasattr(self, 'decision_status'):
                self.decision_status.set_status(False)
        if self.is_running:
            try:
                self.after(self.update_interval, self.update_data)
            except Exception as e:
                print(f"[Decision] Schedule error: {e}")
    
    def _generate_fallback_data(self):
        actions = ['BUY', 'SELL', 'HOLD', 'MONITOR']
        action = random.choice(actions)
        confidence = random.randint(40, 95)
        reasons = ["Bullish breakout detected", "Bearish divergence confirmed", "Support level holding strong", "Resistance level breaking", "Volume spike indicates momentum", "RSI oversold condition", "MACD crossover bullish", "Price above moving averages"]
        self.decision_data = {'action': action, 'confidence': confidence, 'reason': random.choice(reasons), 'timestamp': datetime.now().isoformat(), 'decisions_count': self.update_count, 'avg_confidence': random.randint(50, 85), 'risk_level': random.choice(['LOW', 'MEDIUM', 'HIGH']), 'success_rate': random.randint(40, 90), 'alternatives': [{'action': random.choice(actions), 'confidence': random.randint(30, 70), 'reason': random.choice(reasons)} for _ in range(random.randint(1, 3))], 'risk_assessment': {'market_risk': random.choice(['LOW', 'MEDIUM', 'HIGH']), 'volatility': f"{random.randint(5, 30)}%", 'liquidity': random.choice(['HIGH', 'MEDIUM', 'LOW']), 'timeframe': random.choice(['1H', '4H', '1D'])}}
    
    def _update_ui(self):
        try:
            decision = self.decision_data or {}
            action = decision.get("action", "HOLD")
            confidence = decision.get("confidence", 0)
            reason = decision.get("reason", "Waiting for signal")
            if hasattr(self, 'decision_card'):
                try:
                    self.decision_card.update(action, confidence, reason)
                except Exception as e:
                    print(f"[Decision] Card update error: {e}")
            if hasattr(self, 'decision_status'):
                self.decision_status.set_status(confidence > 50)
            
            decisions_count = decision.get('decisions_count', 0)
            if hasattr(self, 'decisions_made'):
                self.decisions_made.update_value(str(decisions_count))
            avg_conf = decision.get('avg_confidence', confidence)
            if hasattr(self, 'avg_confidence'):
                self.avg_confidence.update_value(f"{avg_conf:.0f}%")
            risk = decision.get('risk_level', 'MEDIUM')
            risk_colors = {'LOW': '#22C55E', 'MEDIUM': '#F59E0B', 'HIGH': '#EF4444', 'CRITICAL': '#DC2626'}
            if hasattr(self, 'risk_level'):
                self.risk_level.update_value(risk, color=risk_colors.get(risk.upper(), '#F59E0B'))
            success = decision.get('success_rate', 0)
            if hasattr(self, 'success_rate'):
                self.success_rate.update_value(f"{success:.0f}%")
            
            alternatives = decision.get("alternatives", [])
            if hasattr(self, 'alternatives_text'):
                try:
                    self.alternatives_text.delete("1.0", "end")
                    if alternatives:
                        for alt in alternatives:
                            alt_action = alt.get('action', 'Unknown')
                            alt_reason = alt.get('reason', '')
                            alt_conf = alt.get('confidence', 0)
                            self.alternatives_text.insert("end", f"• {alt_action} (conf: {alt_conf:.0f}%) - {alt_reason}\n")
                    else:
                        self.alternatives_text.insert("1.0", "No alternatives available")
                except Exception as e:
                    print(f"[Decision] Alternatives update error: {e}")
            
            risk_assessment = decision.get('risk_assessment', {})
            if hasattr(self, 'risk_text'):
                try:
                    self.risk_text.delete("1.0", "end")
                    if risk_assessment:
                        risk_lines = []
                        for key, value in risk_assessment.items():
                            if isinstance(value, dict):
                                risk_lines.append(f"{key}:")
                                for sub_key, sub_val in value.items():
                                    risk_lines.append(f"  {sub_key}: {sub_val}")
                            else:
                                risk_lines.append(f"{key}: {value}")
                        self.risk_text.insert("1.0", "\n".join(risk_lines))
                    else:
                        self.risk_text.insert("1.0", "No risk assessment available")
                except Exception as e:
                    print(f"[Decision] Risk update error: {e}")
            
            if hasattr(self, 'details_text'):
                try:
                    details_data = {"timestamp": datetime.now().isoformat(), "decision": decision, "alternatives": alternatives, "risk_assessment": risk_assessment, "update_count": self.update_count, "success_count": self.success_count, "error_count": self.error_count, "brain_available": self._brain_available, "is_connected": self.is_connected}
                    if self.last_error:
                        details_data["last_error"] = self.last_error
                        details_data["last_error_time"] = self.last_error_time.isoformat() if self.last_error_time else None
                    text = json.dumps(details_data, indent=2, default=str)
                    if len(text) > 5000:
                        text = text[:5000] + "\n... (truncated)"
                    self.details_text.delete("1.0", "end")
                    self.details_text.insert("1.0", text)
                except Exception as e:
                    print(f"[Decision] Details update error: {e}")
        except Exception as e:
            print(f"[Decision] UI update error: {e}")
            self._update_error_display(e)
    
    def _update_error_display(self, error: Exception):
        try:
            if hasattr(self, 'details_text'):
                try:
                    self.details_text.delete("1.0", "end")
                    self.details_text.insert("1.0", f"❌ ERROR\n\nError: {error}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nUpdates: {self.update_count}\nSuccess: {self.success_count}\nErrors: {self.error_count}\n\nTraceback:\n{traceback.format_exc()}")
                except Exception:
                    pass
            if hasattr(self, 'decision_status'):
                self.decision_status.set_status(False)
        except Exception:
            pass
    
    def refresh(self):
        try:
            if hasattr(self, 'refresh_btn'):
                self.refresh_btn.configure(state="disabled", text="⏳ Refreshing...")
                self.update_idletasks()
            self.update_data()
            if hasattr(self, 'refresh_btn'):
                self.refresh_btn.configure(state="normal", text="🔄 Refresh")
        except Exception as e:
            print(f"[Decision] Refresh error: {e}")
            if hasattr(self, 'refresh_btn'):
                self.refresh_btn.configure(state="normal", text="🔄 Refresh")
    
    def stop_updates(self):
        self.is_running = False
    
    def destroy(self):
        try:
            self.stop_updates()
        except Exception:
            pass
        try:
            super().destroy()
        except Exception:
            pass


# ============================================================
# REFLECTION PAGE
# ============================================================

class Reflection(IntelligencePage):
    """Cognitive Reflection."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.insight_cards = []
        self.insight_data = []
        self.reflections_data = []
        self.learning_summaries = []
        self.brain_instance = None
        self.brain = None
        self._brain_available = False
        self.is_connected = False
        self.last_error = None
        self.last_error_time = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = 10000
        self.bot = None
        self.learning_integration = None
        self._ui_components = {}
        
        self.reflection_status = None
        self.last_update_label = None
        self.refresh_btn = None
        self.total_insights = None
        self.total_reflections = None
        self.learning_count = None
        self.avg_confidence = None
        self.insights_container = None
        self.details_text = None
        
        self._build_ui()
        self.after(500, self.update_data)
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)
        ctk.CTkLabel(header, text="💭 Cognitive Reflection", font=("Segoe UI", 22, "bold"), text_color="#E8EDF2").grid(row=0, column=0, sticky="w")
        self.reflection_status = StatusIndicator(header, label="Reflection")
        self.reflection_status.grid(row=0, column=1, padx=10)
        self.last_update_label = ctk.CTkLabel(header, text="Last update: --", font=("Segoe UI", 10), text_color="#5F6B78")
        self.last_update_label.grid(row=0, column=2, padx=10)
        self.refresh_btn = ctk.CTkButton(header, text="🔄 Refresh", width=80, height=28, font=("Segoe UI", 11), fg_color="#3B82F6", hover_color="#2563EB", command=self.refresh)
        self.refresh_btn.grid(row=0, column=3, padx=10)
        
        summary_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        summary_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)
        summary_frame.grid_columnconfigure(2, weight=1)
        summary_frame.grid_columnconfigure(3, weight=1)
        ctk.CTkLabel(summary_frame, text="📊 Reflection Summary", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=4, padx=15, pady=10, sticky="w")
        
        self.total_insights = MetricCard(summary_frame, title="💡 Total Insights", value="0")
        self.total_insights.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
        self.total_reflections = MetricCard(summary_frame, title="🔄 Reflections", value="0")
        self.total_reflections.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")
        self.learning_count = MetricCard(summary_frame, title="📚 Learning Events", value="0")
        self.learning_count.grid(row=1, column=2, padx=8, pady=8, sticky="nsew")
        self.avg_confidence = MetricCard(summary_frame, title="🎯 Avg Confidence", value="0%")
        self.avg_confidence.grid(row=1, column=3, padx=8, pady=8, sticky="nsew")
        
        insights_frame = ctk.CTkScrollableFrame(self, fg_color="#131A22", corner_radius=10)
        insights_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        insights_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(insights_frame, text="💡 Recent Insights", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.insights_container = ctk.CTkFrame(insights_frame, fg_color="transparent")
        self.insights_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.insights_container.grid_columnconfigure(0, weight=1)
        self.insight_cards = []
        for i in range(8):
            try:
                card = InsightCard(self.insights_container, title="---", content="No insights yet. Waiting for data...")
                card.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
                self.insight_cards.append(card)
            except Exception as e:
                print(f"[Reflection] Card creation error: {e}")
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(details, text="📋 Reflection Details", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.details_text = ctk.CTkTextbox(details, font=("Consolas", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=120)
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
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
    
    def _update_brain_reference(self):
        if self.bot:
            if hasattr(self.bot, 'brain'):
                self.brain_instance = self.bot.brain
                self.brain = self.bot.brain
            elif hasattr(self.bot, '_brain'):
                self.brain_instance = self.bot._brain
                self.brain = self.bot._brain
            elif hasattr(self.bot, 'get_brain'):
                brain = self.bot.get_brain()
                if brain:
                    self.brain_instance = brain
                    self.brain = brain
        if not self.brain_instance and self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                self.brain_instance = self.learning_integration.brain
                self.brain = self.learning_integration.brain
            elif hasattr(self.learning_integration, 'get_brain'):
                brain = self.learning_integration.get_brain()
                if brain:
                    self.brain_instance = brain
                    self.brain = brain
        if not self.brain_instance:
            try:
                from core.brain import brain
                if brain:
                    self.brain_instance = brain
                    self.brain = brain
            except ImportError:
                pass
        self._brain_available = self.brain_instance is not None
    
    def _get_brain(self):
        if self.brain_instance:
            return self.brain_instance
        if hasattr(self, 'brain') and self.brain:
            return self.brain
        if self.bot:
            if hasattr(self.bot, 'brain'):
                return self.bot.brain
            elif hasattr(self.bot, '_brain'):
                return self.bot._brain
            elif hasattr(self.bot, 'get_brain'):
                return self.bot.get_brain()
        if self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                return self.learning_integration.brain
            elif hasattr(self.learning_integration, 'get_brain'):
                return self.learning_integration.get_brain()
        try:
            from core.brain import brain
            if brain:
                self.brain_instance = brain
                self.brain = brain
                return brain
        except ImportError:
            pass
        return None
    
    def _safe_get_data(self, obj, method_name: str, default=None):
        try:
            if obj and hasattr(obj, method_name):
                result = getattr(obj, method_name)()
                return result
            return default
        except Exception as e:
            print(f"[Reflection] {method_name} error: {e}")
            return default
    
    def update_data(self):
        if not self.is_running:
            return
        try:
            self.update_count += 1
            if not hasattr(self, 'reflections_data'):
                self.reflections_data = []
            if not hasattr(self, 'learning_summaries'):
                self.learning_summaries = []
            if not hasattr(self, 'insight_data'):
                self.insight_data = []
            self._update_brain_reference()
            insights = self._collect_insights()
            if insights and len(insights) > 0:
                self.is_connected = True
                self.success_count += 1
                self.insight_data = insights
            else:
                self.is_connected = False
                self.insight_data = self._generate_default_insights()
            self._update_summary()
            self._update_insights()
            self._update_details()
            if hasattr(self, 'reflection_status') and self.reflection_status:
                self.reflection_status.set_status(self.is_connected)
            if hasattr(self, 'last_update_label') and self.last_update_label:
                self.last_update_label.configure(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
            if self.last_error:
                self.last_error = None
                self.last_error_time = None
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            print(f"[Reflection] Update error: {e}")
            self._update_error_display(e)
            if hasattr(self, 'reflection_status') and self.reflection_status:
                self.reflection_status.set_status(False)
        if self.is_running:
            try:
                self.after(self.update_interval, self.update_data)
            except Exception as e:
                print(f"[Reflection] Schedule error: {e}")
    
    def _collect_insights(self) -> List[Dict]:
        insights = []
        if not hasattr(self, 'reflections_data'):
            self.reflections_data = []
        if not hasattr(self, 'learning_summaries'):
            self.learning_summaries = []
        brain = self._get_brain()
        if brain:
            brain_insights = self._get_brain_insights(brain)
            insights.extend(brain_insights)
        consciousness_insights = self._get_consciousness_insights()
        insights.extend(consciousness_insights)
        learning_insights = self._get_learning_insights()
        insights.extend(learning_insights)
        scanner_insights = self._get_scanner_insights()
        insights.extend(scanner_insights)
        bot_insights = self._get_bot_insights()
        insights.extend(bot_insights)
        memory_insights = self._get_memory_insights()
        insights.extend(memory_insights)
        knowledge_insights = self._get_knowledge_insights()
        insights.extend(knowledge_insights)
        if not insights:
            insights = self._generate_default_insights()
        return insights
    
    def _get_brain_insights(self, brain) -> List[Dict]:
        insights = []
        try:
            status = self._safe_get_data(brain, 'status')
            if status and isinstance(status, dict):
                state = status.get('state', 'UNKNOWN')
                cycles = status.get('cycles', 0)
                errors = status.get('errors', 0)
                success_rate = status.get('success_rate', 0)
                if hasattr(self, 'reflections_data'):
                    self.reflections_data.append({"type": "brain_status", "state": state, "cycles": cycles, "errors": errors, "timestamp": datetime.now().isoformat()})
                insights.append({"title": "🧠 Brain Status", "content": f"State: {state} | Cycles: {cycles} | Success Rate: {success_rate:.1f}% | Errors: {errors}", "category": "system", "confidence": 85 if errors == 0 else 50})
            snapshot = self._safe_get_data(brain, 'snapshot')
            if snapshot and isinstance(snapshot, dict):
                market_data = snapshot.get('market', {})
                if market_data:
                    insights.append({"title": "📊 Market Intelligence", "content": f"Forecast: {market_data.get('forecast', 'NEUTRAL')} | Confidence: {market_data.get('confidence', 0):.0f}% | Risk: {market_data.get('risk_level', 'MEDIUM')}", "category": "market", "confidence": market_data.get('confidence', 50)})
                decision_data = snapshot.get('decision', {})
                if decision_data:
                    insights.append({"title": "🎯 Decision Support", "content": f"Action: {decision_data.get('action', 'HOLD')} | Confidence: {decision_data.get('confidence', 0):.0f}%", "category": "decision", "confidence": decision_data.get('confidence', 50)})
            forecast = self._safe_get_data(brain, 'forecast')
            if forecast and isinstance(forecast, dict):
                insights.append({"title": "🔮 Market Forecast", "content": f"Direction: {forecast.get('forecast', 'NEUTRAL')} | Confidence: {forecast.get('confidence', 0):.0f}%", "category": "forecast", "confidence": forecast.get('confidence', 50)})
            health = self._safe_get_data(brain, 'health_check')
            if health and isinstance(health, dict):
                health_score = health.get('health_score', 0)
                insights.append({"title": "🏥 System Health", "content": f"Score: {health_score:.1f}% | Healthy: {health.get('healthy', False)}", "category": "health", "confidence": health_score})
        except Exception as e:
            print(f"[Reflection] Brain insight error: {e}")
        return insights
    
    def _get_consciousness_insights(self) -> List[Dict]:
        insights = []
        try:
            from core.consciousness import consciousness
            if consciousness and hasattr(consciousness, 'snapshot'):
                c_snapshot = consciousness.snapshot()
                if c_snapshot and isinstance(c_snapshot, dict):
                    emotional = c_snapshot.get('emotional', {})
                    if emotional:
                        state = emotional.get('state', 'CALM')
                        intensity = emotional.get('intensity', 0.5)
                        stability = emotional.get('stability', 0.5)
                        insights.append({"title": "💭 Emotional State", "content": f"State: {state} | Intensity: {intensity*100:.0f}% | Stability: {stability*100:.0f}%", "category": "consciousness", "confidence": stability * 100})
                    awareness = c_snapshot.get('awareness', {})
                    if awareness:
                        level = awareness.get('level', 0)
                        insights.append({"title": "🌊 Awareness Level", "content": f"Level: {level*100:.0f}%", "category": "consciousness", "confidence": level * 100})
        except ImportError:
            pass
        except Exception as e:
            print(f"[Reflection] Consciousness insight error: {e}")
        return insights
    
    def _get_learning_insights(self) -> List[Dict]:
        insights = []
        try:
            from core.learning.engine import learning_engine
            if learning_engine and hasattr(learning_engine, 'status'):
                status = learning_engine.status()
                if status and isinstance(status, dict):
                    cycles = status.get('cycles', 0)
                    module_count = status.get('module_count', 0)
                    errors = status.get('errors', 0)
                    if hasattr(self, 'learning_summaries'):
                        self.learning_summaries.append({"type": "learning_status", "cycles": cycles, "modules": module_count, "errors": errors, "timestamp": datetime.now().isoformat()})
                    insights.append({"title": "📚 Learning Engine", "content": f"Cycles: {cycles} | Modules: {module_count} | Errors: {errors}", "category": "learning", "confidence": 90 if errors == 0 else 50})
        except ImportError:
            pass
        except Exception as e:
            print(f"[Reflection] Learning insight error: {e}")
        return insights
    
    def _get_scanner_insights(self) -> List[Dict]:
        insights = []
        try:
            scanner = None
            if self.bot:
                if hasattr(self.bot, 'scanner'):
                    scanner = self.bot.scanner
                elif hasattr(self.bot, 'market_scanner'):
                    scanner = self.bot.market_scanner
            if scanner and hasattr(scanner, 'get_summary'):
                summary = scanner.get_summary()
                if summary and isinstance(summary, dict):
                    total = summary.get('total', 0)
                    bullish = summary.get('bullish', 0)
                    bearish = summary.get('bearish', 0)
                    neutral = summary.get('neutral', 0)
                    insights.append({"title": "📊 Market Summary", "content": f"Total: {total} | 📈 Bullish: {bullish} | 📉 Bearish: {bearish} | ➖ Neutral: {neutral}", "category": "market", "confidence": 75})
        except Exception as e:
            print(f"[Reflection] Scanner insight error: {e}")
        return insights
    
    def _get_bot_insights(self) -> List[Dict]:
        insights = []
        if not self.bot:
            return insights
        try:
            if hasattr(self.bot, 'get_status'):
                status = self.bot.get_status()
                if status and isinstance(status, dict):
                    mode = status.get('mode', 'UNKNOWN')
                    state = status.get('state', 'UNKNOWN')
                    insights.append({"title": "🤖 Bot Status", "content": f"Mode: {mode} | State: {state}", "category": "system", "confidence": 90})
        except Exception as e:
            print(f"[Reflection] Bot insight error: {e}")
        return insights
    
    def _get_memory_insights(self) -> List[Dict]:
        insights = []
        try:
            from core.memory import memory
            if memory and hasattr(memory, 'get_stats'):
                stats = memory.get_stats()
                if stats and isinstance(stats, dict):
                    total = stats.get('total', 0)
                    insights.append({"title": "🧠 Memory Status", "content": f"Total items: {total}", "category": "memory", "confidence": 85})
        except ImportError:
            pass
        except Exception as e:
            print(f"[Reflection] Memory insight error: {e}")
        return insights
    
    def _get_knowledge_insights(self) -> List[Dict]:
        insights = []
        try:
            from core.knowledge import knowledge
            if knowledge and hasattr(knowledge, 'stats'):
                stats = knowledge.stats()
                if stats:
                    total = getattr(stats, 'total', 0)
                    avg_conf = getattr(stats, 'avg_confidence', 0)
                    insights.append({"title": "📚 Knowledge Base", "content": f"Items: {total} | Avg Confidence: {avg_conf:.1f}%", "category": "knowledge", "confidence": avg_conf})
        except ImportError:
            pass
        except Exception as e:
            print(f"[Reflection] Knowledge insight error: {e}")
        return insights
    
    def _generate_default_insights(self) -> List[Dict]:
        return [{"title": "🧠 System Initialized", "content": "Cognitive Reflection engine is running. Insights will appear as learning progresses.", "category": "system", "confidence": 50}, {"title": "📡 Waiting for Data", "content": "Reflection engine is waiting for market data to generate insights.", "category": "system", "confidence": 50}, {"title": "🔄 Learning Active", "content": "Learning engine is running. Check back for new insights.", "category": "system", "confidence": 50}]
    
    def _update_summary(self):
        try:
            if not hasattr(self, 'insight_data'):
                self.insight_data = []
            if not hasattr(self, 'reflections_data'):
                self.reflections_data = []
            if not hasattr(self, 'learning_summaries'):
                self.learning_summaries = []
            insights = self.insight_data or []
            total = len(insights)
            if hasattr(self, 'total_insights') and self.total_insights:
                self.total_insights.update_value(str(total))
            if hasattr(self, 'total_reflections') and self.total_reflections:
                self.total_reflections.update_value(str(len(self.reflections_data)))
            if hasattr(self, 'learning_count') and self.learning_count:
                self.learning_count.update_value(str(len(self.learning_summaries)))
            if insights and hasattr(self, 'avg_confidence') and self.avg_confidence:
                total_conf = 0
                count = 0
                for item in insights:
                    if isinstance(item, dict):
                        conf = item.get('confidence', 0)
                        if isinstance(conf, (int, float)):
                            total_conf += conf
                            count += 1
                if count > 0:
                    avg = total_conf / count
                    self.avg_confidence.update_value(f"{avg:.0f}%")
                else:
                    self.avg_confidence.update_value("0%")
            elif hasattr(self, 'avg_confidence') and self.avg_confidence:
                self.avg_confidence.update_value("0%")
        except Exception as e:
            print(f"[Reflection] Summary update error: {e}")
    
    def _update_insights(self):
        try:
            if not hasattr(self, 'insight_data'):
                self.insight_data = []
            if not hasattr(self, 'insight_cards'):
                self.insight_cards = []
            insights = self.insight_data or []
            if not self.insight_cards:
                return
            for i in range(min(len(insights), 8)):
                if i < len(self.insight_cards):
                    card = self.insight_cards[i]
                    insight = insights[i]
                    try:
                        if card and hasattr(card, 'update'):
                            title = insight.get('title', 'Insight')
                            content = insight.get('content', 'No content')
                            card.update(title, content)
                    except Exception as e:
                        print(f"[Reflection] Card update error for index {i}: {e}")
            for i in range(len(insights), len(self.insight_cards)):
                try:
                    if self.insight_cards[i]:
                        self.insight_cards[i].grid_remove()
                except Exception:
                    pass
        except Exception as e:
            print(f"[Reflection] Insights update error: {e}")
    
    def _update_details(self):
        try:
            if not hasattr(self, 'details_text') or not self.details_text:
                return
            if not hasattr(self, 'insight_data'):
                self.insight_data = []
            if not hasattr(self, 'reflections_data'):
                self.reflections_data = []
            if not hasattr(self, 'learning_summaries'):
                self.learning_summaries = []
            details_data = {"timestamp": datetime.now().isoformat(), "update_count": self.update_count, "success_count": self.success_count, "error_count": self.error_count, "insights_count": len(self.insight_data), "reflections_count": len(self.reflections_data), "learning_summaries_count": len(self.learning_summaries), "connected": self.is_connected, "brain_available": self._brain_available}
            if self.last_error:
                details_data["last_error"] = self.last_error
                details_data["last_error_time"] = self.last_error_time.isoformat() if self.last_error_time else None
            text = json.dumps(details_data, indent=2, default=str)
            if len(text) > 5000:
                text = text[:5000] + "\n... (truncated)"
            try:
                self.details_text.delete("1.0", "end")
                self.details_text.insert("1.0", text)
            except Exception as e:
                print(f"[Reflection] Details insert error: {e}")
        except Exception as e:
            print(f"[Reflection] Details update error: {e}")
    
    def _update_error_display(self, error: Exception):
        try:
            if hasattr(self, 'details_text') and self.details_text:
                try:
                    self.details_text.delete("1.0", "end")
                    self.details_text.insert("1.0", f"❌ ERROR\n\nError: {error}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nUpdates: {self.update_count}\nSuccess: {self.success_count}\nErrors: {self.error_count}\n\nTraceback:\n{traceback.format_exc()}")
                except Exception:
                    pass
            if hasattr(self, 'reflection_status') and self.reflection_status:
                self.reflection_status.set_status(False)
        except Exception:
            pass
    
    def refresh(self):
        try:
            if hasattr(self, 'refresh_btn') and self.refresh_btn:
                self.refresh_btn.configure(state="disabled", text="⏳ Refreshing...")
                self.update_idletasks()
            self.update_data()
            if hasattr(self, 'refresh_btn') and self.refresh_btn:
                self.refresh_btn.configure(state="normal", text="🔄 Refresh")
        except Exception as e:
            print(f"[Reflection] Refresh error: {e}")
            if hasattr(self, 'refresh_btn') and self.refresh_btn:
                self.refresh_btn.configure(state="normal", text="🔄 Refresh")
    
    def stop_updates(self):
        self.is_running = False
    
    def destroy(self):
        try:
            self.stop_updates()
        except Exception:
            pass
        try:
            super().destroy()
        except Exception:
            pass


# ============================================================
# HEALTH PAGE
# ============================================================

class Health(IntelligencePage):
    """System Health Monitoring."""
    
    def __init__(self, parent, *args, **kwargs):
        self.health_data = {}
        self.components = {}
        self.last_error = None
        self.last_error_time = None
        self.brain_instance = None
        self.brain = None
        self._brain_available = False
        self.consciousness = None
        self.bot = None
        self.learning_integration = None
        self.is_running = True
        self.update_interval = 3000
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_connected = False
        
        self.health_status = None
        self.health_score = None
        self.components_count = None
        self.errors_count = None
        self.details_text = None
        self.last_update_label = None
        self.refresh_btn = None
        self.component_labels = {}
        self._after_id = None
        
        super().__init__(parent, *args, **kwargs)
        self._build_ui()
        self.after(500, self.update_data)
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, padx=20, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)
        ctk.CTkLabel(header, text="❤️ System Health", font=("Segoe UI", 22, "bold"), text_color="#E8EDF2").grid(row=0, column=0, sticky="w")
        self.health_status = StatusIndicator(header, label="System")
        self.health_status.grid(row=0, column=1, padx=10)
        self.last_update_label = ctk.CTkLabel(header, text="Last update: --", font=("Segoe UI", 10), text_color="#5F6B78")
        self.last_update_label.grid(row=0, column=2, padx=10)
        self.refresh_btn = ctk.CTkButton(header, text="🔄 Refresh", width=80, height=28, font=("Segoe UI", 11), fg_color="#3B82F6", hover_color="#2563EB", command=self.refresh)
        self.refresh_btn.grid(row=0, column=3, padx=10)
        
        self.health_score = MetricCard(self, title="📊 Health Score", value="100%")
        self.health_score.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.components_count = MetricCard(self, title="📦 Components", value="0/0", subtitle="Online")
        self.components_count.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.errors_count = MetricCard(self, title="❌ Errors", value="0")
        self.errors_count.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        components = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        components.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        components.grid_columnconfigure(0, weight=1)
        components.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(components, text="🔧 Component Status", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.components_grid = ctk.CTkFrame(components, fg_color="transparent")
        self.components_grid.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.components_grid.grid_columnconfigure(0, weight=1)
        self.components_grid.grid_columnconfigure(1, weight=1)
        self.components_grid.grid_columnconfigure(2, weight=1)
        self.component_labels = {}
        components_list = [("brain", "🧠 Brain"), ("consciousness", "💭 Consciousness"), ("learning", "📚 Learning"), ("memory", "💾 Memory"), ("pattern", "🔍 Pattern"), ("scanner", "📊 Scanner"), ("signal", "📈 Signal"), ("bot", "🤖 Bot")]
        for i, (key, label) in enumerate(components_list):
            row = i // 3
            col = i % 3
            frame = ctk.CTkFrame(self.components_grid, fg_color="#18212B", corner_radius=6)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            ctk.CTkLabel(frame, text=label, font=("Segoe UI", 11), text_color="#8D9AAA").pack(anchor="w", padx=10, pady=(8, 0))
            status_label = ctk.CTkLabel(frame, text="● OFFLINE", font=("Segoe UI", 10, "bold"), text_color="#EF4444")
            status_label.pack(anchor="w", padx=10, pady=(2, 8))
            self.component_labels[key] = status_label
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        details.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(details, text="📋 Health Details", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.details_text = ctk.CTkTextbox(details, font=("Consolas", 10), fg_color="#0B0F14", text_color="#8D9AAA", height=120)
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def set_bot(self, bot):
        self.bot = bot
        self._update_brain_reference()
        self._update_consciousness_reference()
    
    def set_learning(self, learning):
        self.learning_integration = learning
        self._update_brain_reference()
    
    def set_brain(self, brain):
        self.brain_instance = brain
        self.brain = brain
        self._brain_available = brain is not None
        self._update_brain_reference()
    
    def _update_brain_reference(self):
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
    
    def _update_consciousness_reference(self):
        if self.bot and hasattr(self.bot, 'consciousness'):
            self.consciousness = self.bot.consciousness
            return
        if not self.consciousness:
            try:
                from core.consciousness import consciousness
                self.consciousness = consciousness
            except ImportError:
                pass
    
    def update_data(self):
        if not self.is_running:
            return
        try:
            self.update_count += 1
            self._update_brain_reference()
            self._update_consciousness_reference()
            health_result = self._collect_health_data()
            if health_result:
                self.health_data = health_result
                self.is_connected = True
                self.success_count += 1
                self.last_error = None
            else:
                self.is_connected = False
                self.error_count += 1
                self.last_error = "No health data available"
                self.last_error_time = datetime.now()
                self.health_data = self._generate_fallback_data()
            self._update_ui()
            if self.last_update_label:
                self.last_update_label.configure(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            print(f"[Health] Update error: {e}")
            traceback.print_exc()
            self._update_error_display(e)
            if self.health_status:
                self.health_status.set_status(False)
        if self.is_running:
            try:
                self._after_id = self.after(self.update_interval, self.update_data)
            except Exception as e:
                print(f"[Health] Schedule error: {e}")
    
    def _collect_health_data(self) -> Dict[str, Any]:
        result = {"timestamp": datetime.now().isoformat(), "components": {}, "online": 0, "total": 0, "errors": 0, "health_score": 0.0}
        component_checks = [("brain", self._check_brain), ("consciousness", self._check_consciousness), ("learning", self._check_learning), ("memory", self._check_memory), ("pattern", self._check_pattern), ("scanner", self._check_scanner), ("signal", self._check_signal), ("bot", self._check_bot)]
        for name, check_func in component_checks:
            try:
                status = check_func()
                result["components"][name] = status
                result["total"] += 1
                if status.get("online", False):
                    result["online"] += 1
                result["errors"] += status.get("errors", 0)
            except Exception as e:
                result["components"][name] = {"online": False, "error": str(e), "errors": 1}
                result["total"] += 1
                result["errors"] += 1
        if result["total"] > 0:
            result["health_score"] = (result["online"] / result["total"]) * 100
        return result
    
    def _check_brain(self):
        result = {"online": False, "errors": 0}
        if not self.brain:
            return result
        try:
            if hasattr(self.brain, 'health_check'):
                health = self.brain.health_check()
                if health and isinstance(health, dict):
                    result["online"] = health.get("healthy", False)
                    result["errors"] = health.get("errors", 0)
                    result["health_score"] = health.get("health_score", 0)
                    return result
            if hasattr(self.brain, 'status'):
                status = self.brain.status()
                if status and isinstance(status, dict):
                    state = status.get("state", "")
                    result["online"] = state not in ["ERROR", "STOPPED"]
                    result["errors"] = status.get("errors", 0)
                    return result
            if hasattr(self.brain, 'state'):
                state = getattr(self.brain, 'state')
                if hasattr(state, 'value'):
                    result["online"] = state.value not in ["ERROR", "STOPPED"]
                else:
                    result["online"] = state not in ["ERROR", "STOPPED"]
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
        return result
    
    def _check_consciousness(self):
        result = {"online": False, "errors": 0}
        if not self.consciousness:
            return result
        try:
            if hasattr(self.consciousness, 'status'):
                status = self.consciousness.status()
                if status and isinstance(status, dict):
                    result["online"] = status.get("state") != "ERROR"
                    return result
            if hasattr(self.consciousness, 'snapshot'):
                snapshot = self.consciousness.snapshot()
                if snapshot and isinstance(snapshot, dict):
                    result["online"] = True
                    return result
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
        return result
    
    def _check_learning(self):
        result = {"online": False, "errors": 0}
        try:
            from core.learning.engine import learning_engine
            if learning_engine:
                if hasattr(learning_engine, 'status'):
                    status = learning_engine.status()
                    if status and isinstance(status, dict):
                        result["online"] = status.get("engine") == "ONLINE"
                        result["errors"] = status.get("errors", 0)
                        return result
                if hasattr(learning_engine, 'is_running'):
                    result["online"] = learning_engine.is_running()
                    return result
        except ImportError:
            pass
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
        return result
    
    def _check_memory(self):
        result = {"online": False, "errors": 0}
        try:
            from core.memory import memory
            if memory:
                if hasattr(memory, 'health'):
                    health = memory.health()
                    if health and isinstance(health, dict):
                        result["online"] = health.get("status") == "ONLINE"
                        return result
                if hasattr(memory, 'stats'):
                    stats = memory.stats()
                    if stats is not None:
                        result["online"] = True
                        return result
        except ImportError:
            pass
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
        return result
    
    def _check_pattern(self):
        result = {"online": False, "errors": 0}
        try:
            from core.learning.pattern import pattern
            if pattern:
                if hasattr(pattern, 'get_state'):
                    state = pattern.get_state()
                    if state is not None:
                        result["online"] = True
                        return result
                if hasattr(pattern, 'status'):
                    status = pattern.status()
                    if status is not None:
                        result["online"] = True
                        return result
        except ImportError:
            pass
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
        return result
    
    def _check_scanner(self):
        result = {"online": False, "errors": 0}
        try:
            from core.scanner import MarketScanner
            result["online"] = True
            if self.bot and hasattr(self.bot, 'scanner'):
                scanner = self.bot.scanner
                if scanner and hasattr(scanner, 'is_running'):
                    result["online"] = scanner.is_running()
        except ImportError:
            pass
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
        return result
    
    def _check_signal(self):
        result = {"online": False, "errors": 0}
        try:
            from core.signal_engine import SignalEngine
            result["online"] = True
            if self.bot and hasattr(self.bot, 'signal_engine'):
                engine = self.bot.signal_engine
                if engine and hasattr(engine, 'is_active'):
                    result["online"] = engine.is_active()
        except ImportError:
            pass
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
        return result
    
    def _check_bot(self):
        result = {"online": False, "errors": 0}
        if not self.bot:
            return result
        try:
            if hasattr(self.bot, 'get_status'):
                status = self.bot.get_status()
                if status and isinstance(status, dict):
                    result["online"] = status.get("running", False)
                    result["errors"] = status.get("errors", 0)
                    return result
            if hasattr(self.bot, 'status'):
                status = self.bot.status()
                if status and isinstance(status, dict):
                    result["online"] = status.get("running", False)
                    result["errors"] = status.get("errors", 0)
                    return result
            if hasattr(self.bot, 'is_running'):
                result["online"] = self.bot.is_running()
                return result
        except Exception as e:
            result["error"] = str(e)
            result["errors"] = 1
        return result
    
    def _generate_fallback_data(self):
        return {"timestamp": datetime.now().isoformat(), "components": {}, "online": 0, "total": 8, "errors": 0, "health_score": 0.0, "is_fallback": True}
    
    def _update_ui(self):
        health = self.health_data
        if not health:
            return
        components = health.get("components", {})
        online = health.get("online", 0)
        total = health.get("total", 0)
        errors = health.get("errors", 0)
        health_score = health.get("health_score", 0.0)
        is_fallback = health.get("is_fallback", False)
        
        for name, label in self.component_labels.items():
            status = components.get(name, {})
            if isinstance(status, dict):
                is_online = status.get("online", False)
                error = status.get("error", "")
                if error:
                    label.configure(text="● ERROR", text_color="#EF4444")
                else:
                    label.configure(text="● ONLINE" if is_online else "● OFFLINE", text_color="#22C55E" if is_online else "#EF4444")
            else:
                label.configure(text="● UNKNOWN", text_color="#6B7280")
        
        if self.health_score:
            color = self._get_health_color(health_score)
            self.health_score.update_value(f"{health_score:.0f}%", color=color)
            self.health_score.update_subtitle("Fallback data" if is_fallback else "System Health")
        if self.components_count:
            self.components_count.update_value(f"{online}/{total}")
            self.components_count.update_subtitle("Online" if online > 0 else "No components online")
        if self.errors_count:
            color = "#EF4444" if errors > 0 else "#22C55E"
            self.errors_count.update_value(str(errors), color=color)
            self.errors_count.update_subtitle("Total errors" if errors > 0 else "No errors")
        if self.health_status:
            self.health_status.set_status(health_score > 80)
        if self.details_text:
            details_data = {"timestamp": datetime.now().isoformat(), "health_data": health, "update_count": self.update_count, "success_count": self.success_count, "error_count": self.error_count, "is_fallback": is_fallback, "brain_available": self._brain_available, "connected": self.is_connected}
            if self.last_error:
                details_data["last_error"] = self.last_error
                details_data["last_error_time"] = self.last_error_time.isoformat() if self.last_error_time else None
            try:
                self.details_text.delete("1.0", "end")
                text = json.dumps(details_data, indent=2, default=str)
                if len(text) > 5000:
                    text = text[:5000] + "\n... (truncated)"
                self.details_text.insert("1.0", text)
            except Exception as e:
                print(f"[Health] Details update error: {e}")
    
    def _get_health_color(self, score: float) -> str:
        if score >= 80:
            return "#22C55E"
        elif score >= 60:
            return "#F59E0B"
        else:
            return "#EF4444"
    
    def _update_error_display(self, error: Exception):
        try:
            if self.details_text:
                self.details_text.delete("1.0", "end")
                self.details_text.insert("1.0", f"❌ ERROR\n\nError: {error}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nUpdates: {self.update_count}\nSuccess: {self.success_count}\nErrors: {self.error_count}\n\nTraceback:\n{traceback.format_exc()}")
            if self.health_status:
                self.health_status.set_status(False)
        except Exception:
            pass
    
    def refresh(self):
        if self.refresh_btn:
            self.refresh_btn.configure(state="disabled", text="⏳ Refreshing...")
            self.update_idletasks()
        try:
            self.update_data()
        finally:
            if self.refresh_btn:
                self.refresh_btn.configure(state="normal", text="🔄 Refresh")
    
    def stop(self):
        self.is_running = False
        if self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
    
    def destroy(self):
        self.stop()
        super().destroy()


# ============================================================
# KNOWLEDGE PAGE
# ============================================================

class Knowledge(IntelligencePage):
    """Knowledge Base View."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.knowledge_items = []
        self.knowledge_stats = {}
        self.search_results = []
        self.categories = []
        self.knowledge_count = 0
        self.is_connected = False
        self.last_error = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = 5000
        self.bot = None
        self.selected_category = "All"
        
        self.knowledge_status = None
        self.last_update_label = None
        self.refresh_btn = None
        self.total_items = None
        self.total_states = None
        self.avg_confidence = None
        self.active_items = None
        self.search_entry = None
        self.category_menu = None
        self.add_entry = None
        self.add_category = None
        self.list_container = None
        self.knowledge_labels = []
        self.count_label = None
        
        self._build_ui()
        self.after(500, self.update_data)
    
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        ctk.CTkLabel(header, text="📚 Knowledge Base", font=("Segoe UI", 22, "bold"), text_color="#E8EDF2").pack(side="left")
        self.knowledge_status = StatusIndicator(header, label="Knowledge")
        self.knowledge_status.pack(side="right", padx=10)
        self.last_update_label = ctk.CTkLabel(header, text="Last update: --", font=("Segoe UI", 10), text_color="#5F6B78")
        self.last_update_label.pack(side="right", padx=10)
        self.refresh_btn = ctk.CTkButton(header, text="🔄 Refresh", width=80, height=28, font=("Segoe UI", 11), fg_color="#3B82F6", hover_color="#2563EB", command=self.refresh)
        self.refresh_btn.pack(side="right", padx=10)
        
        stats_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        stats_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
        stats_frame.grid_columnconfigure(3, weight=1)
        ctk.CTkLabel(stats_frame, text="📊 Knowledge Statistics", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=4, padx=15, pady=10, sticky="w")
        self.total_items = MetricCard(stats_frame, title="📄 Total Items", value="0")
        self.total_items.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
        self.total_states = MetricCard(stats_frame, title="🧠 States", value="0")
        self.total_states.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")
        self.avg_confidence = MetricCard(stats_frame, title="🎯 Avg Confidence", value="0%")
        self.avg_confidence.grid(row=1, column=2, padx=8, pady=8, sticky="nsew")
        self.active_items = MetricCard(stats_frame, title="✅ Active", value="0")
        self.active_items.grid(row=1, column=3, padx=8, pady=8, sticky="nsew")
        
        search_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        search_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        search_frame.grid_columnconfigure(0, weight=3)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)
        search_frame.grid_rowconfigure(1, weight=0)
        search_frame.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(search_frame, text="🔍 Search & Add Knowledge", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, columnspan=3, padx=15, pady=10, sticky="w")
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search knowledge...", height=35)
        self.search_entry.grid(row=1, column=0, padx=(15, 5), pady=5, sticky="ew")
        self.category_menu = ctk.CTkOptionMenu(search_frame, values=["All"], command=self._filter_category, height=35, width=120)
        self.category_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        search_btn = ctk.CTkButton(search_frame, text="Search", width=80, height=35, fg_color="#3B82F6", hover_color="#2563EB", command=self._search_knowledge)
        search_btn.grid(row=1, column=2, padx=(5, 15), pady=5)
        add_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        add_frame.grid(row=2, column=0, columnspan=3, padx=15, pady=(5, 15), sticky="ew")
        add_frame.grid_columnconfigure(0, weight=3)
        add_frame.grid_columnconfigure(1, weight=0)
        add_frame.grid_columnconfigure(2, weight=0)
        self.add_entry = ctk.CTkEntry(add_frame, placeholder_text="Add new knowledge...", height=35)
        self.add_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.add_category = ctk.CTkOptionMenu(add_frame, values=["general", "market", "trading", "pattern", "strategy", "insight", "fact", "rule"], height=35, width=100)
        self.add_category.grid(row=0, column=1, padx=5)
        add_btn = ctk.CTkButton(add_frame, text="Add", width=60, height=35, fg_color="#22C55E", hover_color="#16A34A", command=self._add_knowledge)
        add_btn.grid(row=0, column=2, padx=(5, 0))
        
        list_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        list_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(list_frame, text="📋 Knowledge Items", font=("Segoe UI", 14, "bold"), text_color="#E8EDF2").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.list_container = ctk.CTkScrollableFrame(list_frame, fg_color="transparent", height=250)
        self.list_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.list_container.grid_columnconfigure(0, weight=1)
        self.knowledge_labels = []
        
        count_frame = ctk.CTkFrame(self, fg_color="transparent")
        count_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.count_label = ctk.CTkLabel(count_frame, text="Total: 0 items", font=("Segoe UI", 11), text_color="#5F6B78")
        self.count_label.pack(side="right")
    
    def set_bot(self, bot):
        self.bot = bot
    
    def update_data(self):
        if not self.is_running:
            return
        try:
            self.update_count += 1
            self._collect_data()
            self._update_ui()
            self.is_connected = True
            self.success_count += 1
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            print(f"[Knowledge] Update error: {e}")
            self.knowledge_status.set_status(False)
        if self.is_running:
            self.after(self.update_interval, self.update_data)
    
    def _collect_data(self):
        self.knowledge_items = []
        self.knowledge_stats = {}
        self.categories = ["All"]
        self.knowledge_count = 0
        try:
            from core.knowledge import knowledge
            if knowledge:
                if hasattr(knowledge, 'stats'):
                    stats = knowledge.stats()
                    if stats:
                        self.knowledge_stats = {"total": getattr(stats, 'total', 0), "states": getattr(stats, 'state_count', 0), "avg_confidence": getattr(stats, 'avg_confidence', 0), "active": getattr(stats, 'active', 0), "archived": getattr(stats, 'archived', 0), "expired": getattr(stats, 'expired', 0), "deprecated": getattr(stats, 'deprecated', 0)}
                        self.knowledge_count = self.knowledge_stats.get('total', 0)
                if hasattr(knowledge, 'all'):
                    items = knowledge.all()
                    if items:
                        self.knowledge_items = []
                        for item in items[:50]:
                            try:
                                self.knowledge_items.append({"id": getattr(item, 'id', ''), "content": getattr(item, 'content', '')[:200], "category": getattr(item, 'category', 'general'), "type": getattr(item, 'type', 'fact'), "confidence": getattr(item, 'confidence', 0), "importance": getattr(item, 'importance', 0.5), "status": getattr(item, 'status', 'active'), "created_at": getattr(item, 'created_at', ''), "tags": getattr(item, 'tags', [])})
                            except Exception:
                                continue
                if hasattr(knowledge, 'get_categories'):
                    cats = knowledge.get_categories()
                    if cats:
                        self.categories = ["All"] + cats
        except ImportError:
            try:
                from core.learning.contracts import knowledge
                if knowledge:
                    self.knowledge_stats = {"total": len(getattr(knowledge, '_knowledge', {})), "states": 0, "avg_confidence": 0, "active": 0, "archived": 0}
                    self.knowledge_count = self.knowledge_stats.get('total', 0)
            except ImportError:
                pass
        except Exception as e:
            print(f"[Knowledge] Collect error: {e}")
        if len(self.categories) > 1:
            current = self.category_menu.get()
            self.category_menu.configure(values=self.categories)
            if current in self.categories:
                self.category_menu.set(current)
            else:
                self.category_menu.set("All")
    
    def _update_ui(self):
        total = self.knowledge_stats.get('total', 0)
        self.knowledge_status.set_status(total > 0)
        self.total_items.update_value(str(self.knowledge_stats.get('total', 0)))
        self.total_states.update_value(str(self.knowledge_stats.get('states', 0)))
        avg_conf = self.knowledge_stats.get('avg_confidence', 0)
        self.avg_confidence.update_value(f"{avg_conf:.1f}%")
        self.active_items.update_value(str(self.knowledge_stats.get('active', 0)))
        self._update_list()
        total_items = len(self.knowledge_items) if self.knowledge_items else 0
        total_all = self.knowledge_stats.get('total', 0)
        self.count_label.configure(text=f"Showing: {total_items} / Total: {total_all} items")
        self.last_update_label.configure(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
    
    def _update_list(self):
        for frame in self.knowledge_labels:
            frame.destroy()
        self.knowledge_labels.clear()
        items = self.knowledge_items
        search_text = self.search_entry.get().strip().lower()
        if search_text:
            items = [i for i in items if search_text in i.get('content', '').lower()]
        category = self.category_menu.get()
        if category != "All":
            items = [i for i in items if i.get('category') == category]
        if items:
            for i, item in enumerate(items):
                try:
                    frame = ctk.CTkFrame(self.list_container, fg_color="#1A2430" if i % 2 == 0 else "#131A22", corner_radius=6)
                    frame.grid(row=i, column=0, padx=5, pady=3, sticky="ew")
                    frame.grid_columnconfigure(1, weight=1)
                    status = item.get('status', '')
                    status_text = "✅" if status == 'active' else "📦" if status == 'archived' else "📄"
                    content = item.get('content', 'No content')
                    if len(content) > 80:
                        content = content[:80] + "..."
                    category_name = item.get('category', 'general')
                    confidence = item.get('confidence', 0)
                    conf_str = f"{confidence:.0f}%" if confidence > 0 else "N/A"
                    label = ctk.CTkLabel(frame, text=f"{status_text} [{category_name.upper()}] {content} (conf: {conf_str})", font=("Segoe UI", 11), text_color="#E8EDF2", anchor="w")
                    label.grid(row=0, column=0, padx=10, pady=8, sticky="w")
                    detail_btn = ctk.CTkButton(frame, text="📄", width=30, height=24, font=("Segoe UI", 9), fg_color="#3B82F6", hover_color="#2563EB", command=lambda idx=i: self._show_details(idx))
                    detail_btn.grid(row=0, column=1, padx=10, pady=5, sticky="e")
                    self.knowledge_labels.append(frame)
                except Exception as e:
                    print(f"[Knowledge] List item error: {e}")
                    continue
        else:
            label = ctk.CTkLabel(self.list_container, text="No knowledge items found", font=("Segoe UI", 12), text_color="#5F6B78")
            label.grid(row=0, column=0, padx=10, pady=20)
            self.knowledge_labels.append(label)
    
    def _search_knowledge(self):
        self._update_list()
    
    def _filter_category(self, category):
        self._update_list()
    
    def _add_knowledge(self):
        content = self.add_entry.get().strip()
        if not content:
            return
        category = self.add_category.get()
        try:
            from core.knowledge import knowledge
            if knowledge and hasattr(knowledge, 'add'):
                item_id = knowledge.add(content=content, category=category, type="fact", tags=[category, "manual"], confidence=50.0, importance=0.5)
                if item_id:
                    self.add_entry.delete(0, "end")
                    print(f"[Knowledge] Added: {item_id}")
                    self.update_data()
                else:
                    print("[Knowledge] Add returned None")
        except ImportError:
            try:
                from core.learning.contracts import knowledge
                if knowledge and hasattr(knowledge, 'add'):
                    knowledge.add(content=content, category=category, tags=[category, "manual"])
                    self.add_entry.delete(0, "end")
                    self.update_data()
            except ImportError:
                print("[Knowledge] Cannot add: knowledge module not available")
        except Exception as e:
            print(f"[Knowledge] Add error: {e}")
    
    def _show_details(self, index):
        if index >= len(self.knowledge_items):
            return
        item = self.knowledge_items[index]
        popup = ctk.CTkToplevel(self)
        popup.title("Knowledge Details")
        popup.geometry("600x450")
        popup.configure(fg_color="#0B0F14")
        popup.minsize(400, 300)
        details_text = ctk.CTkTextbox(popup, font=("Consolas", 11), fg_color="#0B0F14", text_color="#E8EDF2")
        details_text.pack(fill="both", expand=True, padx=20, pady=20)
        details_text.insert("1.0", json.dumps(item, indent=2, default=str))
        details_text.configure(state="disabled")
    
    def refresh(self):
        self.update_data()
    
    def stop(self):
        self.is_running = False
    
    def destroy(self):
        self.stop()
        super().destroy()


# ============================================================
# TELEGRAM PAGE
# ============================================================

class TelegramPage(ctk.CTkFrame):
    """Telegram Control Page."""
    
    def __init__(self, parent, bot=None, telegram_service=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.bot = bot
        self.telegram_service = telegram_service
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build_header()
        self._build_status_panel()
        self._build_main_panel()
        self._refresh_status()
    
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 10))
        header.grid_columnconfigure(0, weight=1)
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_frame, text="Telegram Control", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Manage Telegram notifications and bot communication", font=ctk.CTkFont(size=13), text_color=("gray45", "gray65")).pack(anchor="w", pady=(4, 0))
        self.status_badge = ctk.CTkLabel(header, text="●  CHECKING", height=34, corner_radius=17, fg_color=("#475569", "#334155"), text_color="white", font=ctk.CTkFont(size=12, weight="bold"), padx=18)
        self.status_badge.grid(row=0, column=1, sticky="e")
    
    def _build_status_panel(self):
        panel = ctk.CTkFrame(self, corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        panel.grid(row=1, column=0, sticky="ew", padx=28, pady=10)
        for i in range(3):
            panel.grid_columnconfigure(i, weight=1)
        self.connection_value = self._create_metric(panel, "CONNECTION", "Checking...", 0)
        self.bot_token_value = self._create_metric(panel, "BOT TOKEN", "Not checked", 1)
        self.chat_id_value = self._create_metric(panel, "CHAT ID", "Not checked", 2)
    
    def _create_metric(self, parent, title, value, column):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, sticky="ew", padx=20, pady=18)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=11, weight="bold"), text_color=("gray50", "gray60")).pack(anchor="w")
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(anchor="w", pady=(5, 0))
        return label
    
    def _build_main_panel(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=2, column=0, sticky="nsew", padx=28, pady=(10, 28))
        container.grid_columnconfigure(0, weight=3)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)
        
        config_panel = ctk.CTkFrame(container, corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        config_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        config_panel.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(config_panel, text="Telegram Configuration", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=24, pady=(22, 4))
        ctk.CTkLabel(config_panel, text="Configure Telegram connection for trading alerts", font=ctk.CTkFont(size=12), text_color=("gray50", "gray65")).grid(row=1, column=0, sticky="w", padx=24)
        form = ctk.CTkFrame(config_panel, fg_color="transparent")
        form.grid(row=2, column=0, sticky="ew", padx=24, pady=24)
        form.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(form, text="Bot Token", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.token_entry = ctk.CTkEntry(form, height=42, corner_radius=10, placeholder_text="Enter Telegram Bot Token", show="•")
        self.token_entry.grid(row=1, column=0, sticky="ew", pady=(0, 18))
        ctk.CTkLabel(form, text="Chat ID", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, sticky="w", pady=(0, 6))
        self.chat_id_entry = ctk.CTkEntry(form, height=42, corner_radius=10, placeholder_text="Enter Telegram Chat ID")
        self.chat_id_entry.grid(row=3, column=0, sticky="ew", pady=(0, 22))
        
        button_frame = ctk.CTkFrame(form, fg_color="transparent")
        button_frame.grid(row=4, column=0, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        self.test_button = ctk.CTkButton(button_frame, text="✈  TEST CONNECTION", height=44, corner_radius=10, font=ctk.CTkFont(size=12, weight="bold"), command=self.test_connection)
        self.test_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.save_button = ctk.CTkButton(button_frame, text="SAVE CONFIGURATION", height=44, corner_radius=10, font=ctk.CTkFont(size=12, weight="bold"), fg_color=("gray70", "gray30"), hover_color=("gray60", "gray40"), command=self.save_configuration)
        self.save_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        notification_panel = ctk.CTkFrame(container, corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        notification_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        notification_panel.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(notification_panel, text="Notification Events", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=24, pady=(22, 4))
        ctk.CTkLabel(notification_panel, text="Choose which events should be sent to Telegram", font=ctk.CTkFont(size=12), text_color=("gray50", "gray65")).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 20))
        self.signal_switch = self._create_notification_switch(notification_panel, "Trading Signals", "Send BUY / SELL signal alerts", 2)
        self.trade_switch = self._create_notification_switch(notification_panel, "Trade Execution", "Send trade execution notifications", 3)
        self.error_switch = self._create_notification_switch(notification_panel, "System Errors", "Send critical bot errors", 4)
        self.system_switch = self._create_notification_switch(notification_panel, "System Status", "Send startup and shutdown notifications", 5)
        self.signal_switch.select()
        self.trade_switch.select()
        self.error_switch.select()
        self.system_switch.select()
    
    def _create_notification_switch(self, parent, title, description, row):
        frame = ctk.CTkFrame(parent, corner_radius=12)
        frame.grid(row=row, column=0, sticky="ew", padx=20, pady=6)
        text_frame = ctk.CTkFrame(frame, fg_color="transparent")
        text_frame.pack(side="left", padx=16, pady=12)
        ctk.CTkLabel(text_frame, text=title, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(text_frame, text=description, font=ctk.CTkFont(size=11), text_color=("gray50", "gray65")).pack(anchor="w", pady=(2, 0))
        switch = ctk.CTkSwitch(frame, text="")
        switch.pack(side="right", padx=18)
        return switch
    
    def _refresh_status(self):
        if not self.telegram_service:
            self.connection_value.configure(text="NOT AVAILABLE")
            self.bot_token_value.configure(text="NOT LOADED")
            self.chat_id_value.configure(text="NOT LOADED")
            self.status_badge.configure(text="●  NOT CONFIGURED", fg_color=("#7f1d1d", "#991b1b"))
            return
        try:
            configured = self.telegram_service.is_configured()
            if configured:
                self.connection_value.configure(text="CONFIGURED")
                self.bot_token_value.configure(text="AVAILABLE")
                self.chat_id_value.configure(text="AVAILABLE")
                self.status_badge.configure(text="●  CONFIGURED", fg_color=("#1f6f43", "#14532d"))
            else:
                self.connection_value.configure(text="NOT CONFIGURED")
                self.bot_token_value.configure(text="MISSING")
                self.chat_id_value.configure(text="MISSING")
                self.status_badge.configure(text="●  NOT CONFIGURED", fg_color=("#7f1d1d", "#991b1b"))
        except Exception as e:
            logger.exception("Unable to refresh Telegram status: %s", e)
            self.connection_value.configure(text="ERROR")
            self.status_badge.configure(text="●  ERROR", fg_color=("#7f1d1d", "#991b1b"))
    
    def save_configuration(self):
        token = self.token_entry.get().strip()
        chat_id = self.chat_id_entry.get().strip()
        if not token or not chat_id:
            self._show_status("Please enter Bot Token and Chat ID.", error=True)
            return
        try:
            if self.telegram_service:
                self.telegram_service.token = token
                self.telegram_service.chat_id = chat_id
                self._show_status("Telegram configuration updated successfully.")
                self._refresh_status()
            else:
                self._show_status("Telegram service is not available.", error=True)
        except Exception as e:
            logger.exception("Unable to save Telegram configuration: %s", e)
            self._show_status(f"Configuration error: {e}", error=True)
    
    def test_connection(self):
        if not self.telegram_service:
            self._show_status("Telegram service is not available.", error=True)
            return
        token = self.token_entry.get().strip()
        chat_id = self.chat_id_entry.get().strip()
        if token:
            self.telegram_service.token = token
        if chat_id:
            self.telegram_service.chat_id = chat_id
        if not self.telegram_service.is_configured():
            self._show_status("Please enter Bot Token and Chat ID first.", error=True)
            return
        self.test_button.configure(state="disabled", text="TESTING...")
        self.status_badge.configure(text="●  CONNECTING", fg_color=("#854d0e", "#a16207"))
        threading.Thread(target=self._test_connection_worker, daemon=True).start()
    
    def _test_connection_worker(self):
        try:
            result = self.telegram_service.test_connection()
            if result:
                self.after(0, lambda: self._show_status("Telegram connection successful."))
                self.after(0, lambda: self.status_badge.configure(text="●  CONNECTED", fg_color=("#1f6f43", "#14532d")))
                self.after(0, lambda: self.connection_value.configure(text="CONNECTED"))
            else:
                self.after(0, lambda: self._show_status("Telegram connection failed.", error=True))
                self.after(0, lambda: self.status_badge.configure(text="●  CONNECTION FAILED", fg_color=("#7f1d1d", "#991b1b")))
                self.after(0, lambda: self.connection_value.configure(text="FAILED"))
        except Exception as e:
            logger.exception("Telegram test failed: %s", e)
            error_message = str(e)
            self.after(0, lambda: self._show_status(f"Connection error: {error_message}", error=True))
            self.after(0, lambda: self.status_badge.configure(text="●  ERROR", fg_color=("#7f1d1d", "#991b1b")))
        finally:
            self.after(0, lambda: self.test_button.configure(state="normal", text="✈  TEST CONNECTION"))
    
    def _show_status(self, message, error=False):
        try:
            if hasattr(self, "status_message"):
                self.status_message.configure(text=message, text_color="#ef4444" if error else "#22c55e")
            else:
                self.status_message = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=12, weight="bold"), text_color="#ef4444" if error else "#22c55e")
                self.status_message.grid(row=3, column=0, sticky="w", padx=28, pady=(0, 15))
        except Exception as e:
            logger.exception("Unable to display Telegram status: %s", e)
    
    def send_test_message(self, message="✅ INKSIDEDIGITAL BOT\n\nTelegram connection test successful."):
        if not self.telegram_service:
            return False
        try:
            return self.telegram_service.send_message(message)
        except Exception as e:
            logger.exception("Unable to send Telegram message: %s", e)
            return False
    
    def set_telegram_service(self, telegram_service):
        self.telegram_service = telegram_service
        self._refresh_status()
    
    def get_notification_settings(self):
        return {"signals": bool(self.signal_switch.get()), "trades": bool(self.trade_switch.get()), "errors": bool(self.error_switch.get()), "system": bool(self.system_switch.get())}


# ============================================================
# TRADING PAGE
# ============================================================

class TradingPage(ctk.CTkFrame):
    """Trading Control Page."""
    
    def __init__(self, parent, bot=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.bot = bot
        self.is_running = False
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build_header()
        self._build_control_panel()
        self._build_trading_panel()
    
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 10))
        header.grid_columnconfigure(0, weight=1)
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_frame, text="Trading Control", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Manage automated trading execution and risk controls", font=ctk.CTkFont(size=13), text_color=("gray45", "gray65")).pack(anchor="w", pady=(4, 0))
        self.status_badge = ctk.CTkLabel(header, text="●  SYSTEM READY", height=34, corner_radius=17, fg_color=("#1f6f43", "#14532d"), text_color="white", font=ctk.CTkFont(size=12, weight="bold"), padx=18)
        self.status_badge.grid(row=0, column=1, sticky="e")
    
    def _build_control_panel(self):
        panel = ctk.CTkFrame(self, corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        panel.grid(row=1, column=0, sticky="ew", padx=28, pady=10)
        for i in range(4):
            panel.grid_columnconfigure(i, weight=1)
        self.bot_status_value = self._create_metric(panel, "BOT STATUS", "READY", 0)
        self.position_value = self._create_metric(panel, "ACTIVE POSITIONS", "0", 1)
        self.pnl_value = self._create_metric(panel, "TODAY PNL", "$0.00", 2)
        self.last_action_value = self._create_metric(panel, "LAST ACTION", "Waiting", 3)
    
    def _create_metric(self, parent, title, value, column):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, sticky="ew", padx=20, pady=18)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=11, weight="bold"), text_color=("gray50", "gray60")).pack(anchor="w")
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(anchor="w", pady=(5, 0))
        return label
    
    def _build_trading_panel(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=2, column=0, sticky="nsew", padx=28, pady=(10, 28))
        container.grid_columnconfigure(0, weight=3)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)
        
        left = ctk.CTkFrame(container, corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(left, text="Trading Engine", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=24, pady=(22, 4))
        ctk.CTkLabel(left, text="Configure and control automated execution", font=ctk.CTkFont(size=12), text_color=("gray50", "gray65")).grid(row=1, column=0, sticky="w", padx=24)
        settings = ctk.CTkFrame(left, fg_color="transparent")
        settings.grid(row=2, column=0, sticky="nsew", padx=24, pady=20)
        settings.grid_columnconfigure(0, weight=1)
        
        auto_frame = ctk.CTkFrame(settings, corner_radius=12)
        auto_frame.pack(fill="x", pady=6)
        auto_text = ctk.CTkFrame(auto_frame, fg_color="transparent")
        auto_text.pack(side="left", padx=16, pady=12)
        ctk.CTkLabel(auto_text, text="Automated Trading", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(auto_text, text="Allow bot to execute trades automatically", font=ctk.CTkFont(size=11), text_color=("gray50", "gray65")).pack(anchor="w")
        self.auto_switch = ctk.CTkSwitch(auto_frame, text="", command=self._toggle_auto_trading)
        self.auto_switch.pack(side="right", padx=18)
        
        paper_frame = ctk.CTkFrame(settings, corner_radius=12)
        paper_frame.pack(fill="x", pady=6)
        paper_text = ctk.CTkFrame(paper_frame, fg_color="transparent")
        paper_text.pack(side="left", padx=16, pady=12)
        ctk.CTkLabel(paper_text, text="Paper Trading", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(paper_text, text="Simulate trades without real funds", font=ctk.CTkFont(size=11), text_color=("gray50", "gray65")).pack(anchor="w")
        self.paper_switch = ctk.CTkSwitch(paper_frame, text="")
        self.paper_switch.select()
        self.paper_switch.pack(side="right", padx=18)
        
        button_frame = ctk.CTkFrame(settings, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 5))
        self.start_button = ctk.CTkButton(button_frame, text="▶  START ENGINE", height=44, corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"), command=self.start_engine)
        self.start_button.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.stop_button = ctk.CTkButton(button_frame, text="■  STOP ENGINE", height=44, corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"), fg_color=("gray70", "gray30"), hover_color=("gray60", "gray40"), command=self.stop_engine, state="disabled")
        self.stop_button.pack(side="left", fill="x", expand=True, padx=(6, 0))
        
        right = ctk.CTkFrame(container, corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(right, text="Execution Activity", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=24, pady=(22, 4))
        ctk.CTkLabel(right, text="Real-time trading engine events", font=ctk.CTkFont(size=12), text_color=("gray50", "gray65")).grid(row=1, column=0, sticky="w", padx=24)
        self.activity_box = ctk.CTkTextbox(right, corner_radius=10, border_width=0, font=ctk.CTkFont(family="Consolas", size=11))
        self.activity_box.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.activity_box.insert("end", "[SYSTEM] Trading engine initialized.\n[SYSTEM] Paper trading mode enabled.\n[SYSTEM] Waiting for activation...\n")
        self.activity_box.configure(state="disabled")
    
    def _toggle_auto_trading(self):
        if self.auto_switch.get():
            self._log_activity("[TRADING] Automated trading enabled.")
        else:
            self._log_activity("[TRADING] Automated trading disabled.")
    
    def start_engine(self):
        if self.is_running:
            return
        self.is_running = True
        self.bot_status_value.configure(text="RUNNING")
        self.status_badge.configure(text="●  ENGINE RUNNING", fg_color=("#1f6f43", "#14532d"))
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.last_action_value.configure(text="Engine Started")
        self._log_activity("[ENGINE] Trading engine started.")
        if self.bot:
            try:
                if hasattr(self.bot, "start"):
                    threading.Thread(target=self.bot.start, daemon=True).start()
            except Exception as e:
                logger.exception("Unable to start bot: %s", e)
                self._log_activity(f"[ERROR] {e}")
    
    def stop_engine(self):
        if not self.is_running:
            return
        self.is_running = False
        self.bot_status_value.configure(text="STOPPED")
        self.status_badge.configure(text="●  ENGINE STOPPED", fg_color=("#7f1d1d", "#991b1b"))
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.last_action_value.configure(text="Engine Stopped")
        self._log_activity("[ENGINE] Trading engine stopped.")
        if self.bot:
            try:
                if hasattr(self.bot, "stop"):
                    threading.Thread(target=self.bot.stop, daemon=True).start()
            except Exception as e:
                logger.exception("Unable to stop bot: %s", e)
                self._log_activity(f"[ERROR] {e}")
    
    def _log_activity(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        self.activity_box.configure(state="normal")
        self.activity_box.insert("end", line)
        self.activity_box.see("end")
        self.activity_box.configure(state="disabled")
    
    def update_positions(self, count):
        self.position_value.configure(text=str(count))
    
    def update_pnl(self, pnl):
        try:
            self.pnl_value.configure(text=f"${float(pnl):,.2f}")
        except Exception:
            self.pnl_value.configure(text=str(pnl))
    
    def update_status(self, status):
        self.bot_status_value.configure(text=str(status).upper())
    
    def add_activity(self, message):
        self._log_activity(message)


# ============================================================
# SETTINGS PAGE
# ============================================================

class SettingsPage(ctk.CTkFrame):
    """System Settings Page."""
    
    def __init__(self, parent, bot=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.bot = bot
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build_header()
        self._build_status_panel()
        self._build_settings_panel()
    
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 10))
        header.grid_columnconfigure(0, weight=1)
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(title_frame, text="System Settings", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Configure trading engine behavior, market scanning and application preferences", font=ctk.CTkFont(size=13), text_color=("gray45", "gray65")).pack(anchor="w", pady=(4, 0))
        self.status_badge = ctk.CTkLabel(header, text="●  SYSTEM READY", height=34, corner_radius=17, fg_color=("#1f6f43", "#14532d"), text_color="white", font=ctk.CTkFont(size=12, weight="bold"), padx=18)
        self.status_badge.grid(row=0, column=1, sticky="e")
    
    def _build_status_panel(self):
        panel = ctk.CTkFrame(self, corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        panel.grid(row=1, column=0, sticky="ew", padx=28, pady=10)
        for column in range(4):
            panel.grid_columnconfigure(column, weight=1)
        self.bot_status_value = self._create_metric(panel, "BOT STATUS", "READY", 0)
        self.mode_value = self._create_metric(panel, "TRADING MODE", "PAPER", 1)
        self.interval_value = self._create_metric(panel, "SCAN INTERVAL", "60 SEC", 2)
        self.config_value = self._create_metric(panel, "CONFIGURATION", "READY", 3)
    
    def _create_metric(self, parent, title, value, column):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, sticky="ew", padx=20, pady=18)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=11, weight="bold"), text_color=("gray50", "gray60")).pack(anchor="w")
        value_label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=19, weight="bold"))
        value_label.pack(anchor="w", pady=(5, 0))
        return value_label
    
    def _build_settings_panel(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=2, column=0, sticky="nsew", padx=28, pady=(10, 28))
        container.grid_columnconfigure(0, weight=3)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)
        
        left_panel = ctk.CTkFrame(container, corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(left_panel, text="Trading Configuration", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=24, pady=(22, 4))
        ctk.CTkLabel(left_panel, text="Configure the behavior of the trading engine", font=ctk.CTkFont(size=12), text_color=("gray50", "gray65")).grid(row=1, column=0, sticky="w", padx=24)
        settings_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        settings_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=20)
        settings_frame.grid_columnconfigure(0, weight=1)
        
        self.paper_mode = ctk.BooleanVar(value=True)
        self._create_switch(settings_frame, title="Paper Trading Mode", description="Simulate trades without using real funds", variable=self.paper_mode, row=0)
        self.auto_trading = ctk.BooleanVar(value=False)
        self._create_switch(settings_frame, title="Automated Trading", description="Allow the trading engine to execute trades automatically", variable=self.auto_trading, row=1)
        self.telegram_notifications = ctk.BooleanVar(value=True)
        self._create_switch(settings_frame, title="Telegram Notifications", description="Send trading signals and system events to Telegram", variable=self.telegram_notifications, row=2)
        self.extended_logging = ctk.BooleanVar(value=True)
        self._create_switch(settings_frame, title="Extended Logging", description="Enable detailed application and trading logs", variable=self.extended_logging, row=3)
        
        interval_frame = ctk.CTkFrame(settings_frame, corner_radius=12)
        interval_frame.grid(row=4, column=0, sticky="ew", pady=6)
        interval_frame.grid_columnconfigure(0, weight=1)
        interval_text = ctk.CTkFrame(interval_frame, fg_color="transparent")
        interval_text.grid(row=0, column=0, sticky="w", padx=16, pady=12)
        ctk.CTkLabel(interval_text, text="Market Scan Interval", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(interval_text, text="Time interval between automatic market scans", font=ctk.CTkFont(size=11), text_color=("gray50", "gray65")).pack(anchor="w", pady=(2, 0))
        self.interval_entry = ctk.CTkEntry(interval_frame, width=100, height=38, corner_radius=8, placeholder_text="60")
        self.interval_entry.grid(row=0, column=1, padx=16)
        self.interval_entry.insert(0, "60")
        
        self.save_button = ctk.CTkButton(settings_frame, text="SAVE SETTINGS", height=44, corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"), command=self.save_settings)
        self.save_button.grid(row=5, column=0, sticky="ew", pady=(20, 5))
        
        right_panel = ctk.CTkFrame(container, corner_radius=16, border_width=1, border_color=("gray80", "gray25"))
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(right_panel, text="System Information", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=24, pady=(22, 4))
        ctk.CTkLabel(right_panel, text="Current application configuration and runtime information", font=ctk.CTkFont(size=12), text_color=("gray50", "gray65")).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 20))
        
        info_box = ctk.CTkFrame(right_panel, corner_radius=12)
        info_box.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        info_box.grid_columnconfigure(1, weight=1)
        self._create_info_row(info_box, "Application", "INKSIDEDIGITAL TRADING BOT", 0)
        self._create_info_row(info_box, "Version", "3.0 Professional Terminal", 1)
        self._create_info_row(info_box, "Trading Engine", "Connected" if self.bot else "GUI Mode", 2)
        self._create_info_row(info_box, "Market Data", "Kraken", 3)
        self._create_info_row(info_box, "Interface", "CustomTkinter", 4)
        self._create_info_row(info_box, "Environment", "Python", 5)
        
        self.status_message = ctk.CTkLabel(right_panel, text="Ready to configure system settings.", font=ctk.CTkFont(size=11), text_color=("gray50", "gray65"), wraplength=400)
        self.status_message.grid(row=3, column=0, sticky="w", padx=24, pady=(0, 20))
    
    def _create_switch(self, parent, title, description, variable, row):
        frame = ctk.CTkFrame(parent, corner_radius=12)
        frame.grid(row=row, column=0, sticky="ew", pady=6)
        frame.grid_columnconfigure(0, weight=1)
        text_frame = ctk.CTkFrame(frame, fg_color="transparent")
        text_frame.grid(row=0, column=0, sticky="w", padx=16, pady=12)
        ctk.CTkLabel(text_frame, text=title, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(text_frame, text=description, font=ctk.CTkFont(size=11), text_color=("gray50", "gray65")).pack(anchor="w", pady=(2, 0))
        switch = ctk.CTkSwitch(frame, text="", variable=variable)
        switch.grid(row=0, column=1, padx=18)
        if variable.get():
            switch.select()
        else:
            switch.deselect()
        return switch
    
    def _create_info_row(self, parent, label, value, row):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=11, weight="bold"), text_color=("gray50", "gray65"), anchor="w").grid(row=row, column=0, sticky="w", padx=18, pady=10)
        ctk.CTkLabel(parent, text=value, font=ctk.CTkFont(size=11, weight="bold"), anchor="e").grid(row=row, column=1, sticky="e", padx=18, pady=10)
    
    def save_settings(self):
        try:
            interval_text = self.interval_entry.get().strip()
            if not interval_text:
                interval_text = "60"
            interval = int(interval_text)
            if interval < 5:
                self._show_status("Scan interval must be at least 5 seconds.", error=True)
                return
            if self.bot is not None:
                try:
                    if hasattr(self.bot, "scan_interval"):
                        self.bot.scan_interval = interval
                    if hasattr(self.bot, "paper_mode"):
                        self.bot.paper_mode = self.paper_mode.get()
                    if hasattr(self.bot, "auto_trading"):
                        self.bot.auto_trading = self.auto_trading.get()
                except Exception as e:
                    logger.warning("Unable to apply settings to bot: %s", e)
            mode = "PAPER" if self.paper_mode.get() else "LIVE"
            self.mode_value.configure(text=mode)
            self.interval_value.configure(text=f"{interval} SEC")
            self.bot_status_value.configure(text="READY" if not self.auto_trading.get() else "AUTO")
            self.config_value.configure(text="SAVED")
            self.status_badge.configure(text="●  SETTINGS SAVED", fg_color=("#1f6f43", "#14532d"))
            self._show_status("System settings saved successfully.")
            logger.info("Settings saved: paper_mode=%s, auto_trading=%s, telegram=%s, extended_logging=%s, interval=%s", self.paper_mode.get(), self.auto_trading.get(), self.telegram_notifications.get(), self.extended_logging.get(), interval)
        except ValueError:
            self._show_status("Scan interval must be a valid number.", error=True)
        except Exception as e:
            logger.exception("Unable to save settings: %s", e)
            self._show_status(f"Unable to save settings: {e}", error=True)
    
    def _show_status(self, message, error=False):
        try:
            self.status_message.configure(text=message, text_color="#ef4444" if error else "#22c55e")
        except Exception as e:
            logger.warning("Unable to update settings status: %s", e)
    
    def update_bot_status(self, status):
        try:
            self.bot_status_value.configure(text=str(status).upper())
        except Exception:
            pass
    
    def set_scan_interval(self, interval):
        try:
            self.interval_entry.delete(0, "end")
            self.interval_entry.insert(0, str(interval))
            self.interval_value.configure(text=f"{interval} SEC")
        except Exception:
            pass


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    # Base
    "IntelligencePage",
    
    # Widgets
    "StatusIndicator", "MetricCard", "SignalBadge", "ConfidenceBar",
    "InsightCard", "DecisionCard", "MemoryStats", "LearningProgress",
    "MarketTicker", "PatternList",
    
    # Pages
    "DashboardPage", "Brain", "Learning", "Memory", "Pattern",
    "Prediction", "Decision", "Reflection", "Health", "Knowledge",
    "TelegramPage", "TradingPage", "SettingsPage",
]