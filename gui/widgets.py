# ============================================================
# gui/intelligence/widgets.py
# REUSABLE WIDGETS
# SUPER COMPREHENSIVE WIDGET COLLECTION
# ============================================================

import customtkinter as ctk
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime
import math


class StatusIndicator(ctk.CTkFrame):
    """Status indicator with dot and label."""
    
    def __init__(
        self,
        parent,
        label: str = "Status",
        online_text: str = "ONLINE",
        offline_text: str = "OFFLINE",
        **kwargs
    ):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.online_text = online_text
        self.offline_text = offline_text
        
        # Dot
        self.dot = ctk.CTkLabel(
            self,
            text="●",
            font=("Segoe UI", 16),
            text_color="#22C55E"
        )
        self.dot.pack(side="left", padx=(0, 5))
        
        # Label
        self.label = ctk.CTkLabel(
            self,
            text=label,
            font=("Segoe UI", 11, "bold"),
            text_color="#8D9AAA"
        )
        self.label.pack(side="left")
        
        # Status text
        self.status_label = ctk.CTkLabel(
            self,
            text=self.online_text,
            font=("Segoe UI", 10, "bold"),
            text_color="#22C55E"
        )
        self.status_label.pack(side="left", padx=(5, 0))
    
    def set_status(self, online: bool, status_text: Optional[str] = None):
        """Set status (online/offline)."""
        color = "#22C55E" if online else "#EF4444"
        self.dot.configure(text_color=color)
        
        if status_text is not None:
            self.status_label.configure(text=status_text, text_color=color)
        else:
            self.status_label.configure(
                text=self.online_text if online else self.offline_text,
                text_color=color
            )
    
    def set_text(self, label: str):
        """Set label text."""
        self.label.configure(text=label)
    
    def set_status_text(self, text: str, color: str = "#E8EDF2"):
        """Set status text directly."""
        self.status_label.configure(text=text, text_color=color)


class MetricCard(ctk.CTkFrame):
    """Metric card with title, value, and subtitle."""
    
    def __init__(
        self,
        parent,
        title: str = "",
        value: str = "--",
        subtitle: str = "",
        icon: str = "",
        value_color: str = "#E8EDF2",
        **kwargs
    ):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        # Title with icon
        title_text = f"{icon} {title}" if icon else title
        self.title_label = ctk.CTkLabel(
            self,
            text=title_text,
            font=("Segoe UI", 11),
            text_color="#8D9AAA"
        )
        self.title_label.grid(row=0, column=0, padx=15, pady=(12, 0), sticky="w")
        
        # Value
        self.value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            text_color=value_color
        )
        self.value_label.grid(row=1, column=0, padx=15, pady=(2, 0), sticky="w")
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self,
            text=subtitle,
            font=("Segoe UI", 10),
            text_color="#5F6B78"
        )
        self.subtitle_label.grid(row=2, column=0, padx=15, pady=(0, 12), sticky="w")
    
    def update_value(self, value: str, color: Optional[str] = None):
        """
        Update the value displayed.
        
        Args:
            value: New value string
            color: Optional color for the value (hex color code)
        """
        self.value_label.configure(text=str(value))
        if color:
            self.value_label.configure(text_color=color)
    
    def update_subtitle(self, subtitle: str):
        """Update subtitle."""
        self.subtitle_label.configure(text=subtitle)
    
    def set_icon(self, icon: str):
        """Set icon."""
        current_text = self.title_label.cget("text")
        # Remove existing icon if any
        if current_text.startswith(("✅", "❌", "📊", "📈", "📉", "🔄", "🧠", "💾", "📚", "🎯")):
            current_text = current_text.split(" ", 1)[-1] if " " in current_text else current_text
        self.title_label.configure(text=f"{icon} {current_text}" if icon else current_text)


class SignalBadge(ctk.CTkFrame):
    """Signal badge with color coding."""
    
    COLORS = {
        "BUY": "#22C55E",
        "SELL": "#EF4444",
        "HOLD": "#F59E0B",
        "STRONG BUY": "#16A34A",
        "STRONG SELL": "#DC2626",
        "MONITOR": "#3B82F6",
        "WAIT": "#8D9AAA",
        "NEUTRAL": "#6B7280",
        "BULLISH": "#22C55E",
        "BEARISH": "#EF4444",
    }
    
    def __init__(
        self,
        parent,
        signal: str = "HOLD",
        confidence: float = 0,
        show_confidence: bool = True,
        **kwargs
    ):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.signal = signal
        self.confidence = confidence
        self.show_confidence = show_confidence
        
        color = self.COLORS.get(signal.upper(), "#8D9AAA")
        
        # Badge
        self.badge = ctk.CTkFrame(
            self,
            fg_color=color,
            corner_radius=4
        )
        self.badge.pack(side="left", padx=(0, 5))
        
        self.label = ctk.CTkLabel(
            self.badge,
            text=signal.upper(),
            font=("Segoe UI", 10, "bold"),
            text_color="white"
        )
        self.label.pack(padx=8, pady=2)
        
        # Confidence
        if show_confidence and confidence > 0:
            self.conf_label = ctk.CTkLabel(
                self,
                text=f"{confidence:.0f}%",
                font=("Segoe UI", 9),
                text_color="#8D9AAA"
            )
            self.conf_label.pack(side="left", padx=5)
    
    def update(self, signal: str, confidence: float = 0):
        """Update badge."""
        self.signal = signal
        self.confidence = confidence
        
        color = self.COLORS.get(signal.upper(), "#8D9AAA")
        self.badge.configure(fg_color=color)
        self.label.configure(text=signal.upper())
        
        if self.show_confidence and confidence > 0:
            if hasattr(self, 'conf_label'):
                self.conf_label.configure(text=f"{confidence:.0f}%")
            else:
                self.conf_label = ctk.CTkLabel(
                    self,
                    text=f"{confidence:.0f}%",
                    font=("Segoe UI", 9),
                    text_color="#8D9AAA"
                )
                self.conf_label.pack(side="left", padx=5)


class ConfidenceBar(ctk.CTkFrame):
    """Confidence progress bar with label."""
    
    def __init__(
        self,
        parent,
        label: str = "Confidence",
        value: float = 0,
        max_value: float = 100,
        color: str = "#3B82F6",
        **kwargs
    ):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.max_value = max_value
        
        self.grid_columnconfigure(1, weight=1)
        
        # Label
        self.label = ctk.CTkLabel(
            self,
            text=label,
            font=("Segoe UI", 10),
            text_color="#8D9AAA"
        )
        self.label.grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(
            self,
            width=100,
            height=8,
            corner_radius=4,
            progress_color=color
        )
        self.progress.grid(row=0, column=1, padx=5, sticky="ew")
        self.progress.set(value / max_value if max_value > 0 else 0)
        
        # Value label
        self.value_label = ctk.CTkLabel(
            self,
            text=f"{value:.0f}%",
            font=("Segoe UI", 10, "bold"),
            text_color="#E8EDF2"
        )
        self.value_label.grid(row=0, column=2, padx=(5, 0), sticky="e")
    
    def set_value(self, value: float, max_value: Optional[float] = None):
        """Set value."""
        if max_value is not None:
            self.max_value = max_value
        normalized = value / self.max_value if self.max_value > 0 else 0
        self.progress.set(min(1.0, max(0.0, normalized)))
        self.value_label.configure(text=f"{value:.0f}%")
    
    def set_color(self, color: str):
        """Set progress bar color."""
        self.progress.configure(progress_color=color)


class InsightCard(ctk.CTkFrame):
    """Insight card for displaying insights."""
    
    def __init__(
        self,
        parent,
        title: str = "",
        content: str = "",
        category: str = "general",
        confidence: float = 0,
        **kwargs
    ):
        super().__init__(parent, fg_color="#18212B", corner_radius=8, **kwargs)
        
        self.category = category
        self.confidence = confidence
        
        self.grid_columnconfigure(0, weight=1)
        
        # Title with category
        title_text = f"[{category.upper()}] {title}" if category else title
        self.title_label = ctk.CTkLabel(
            self,
            text=title_text,
            font=("Segoe UI", 11, "bold"),
            text_color="#E8EDF2"
        )
        self.title_label.grid(row=0, column=0, padx=12, pady=(8, 0), sticky="w")
        
        # Content
        self.content_label = ctk.CTkLabel(
            self,
            text=content,
            font=("Segoe UI", 10),
            text_color="#8D9AAA",
            wraplength=300,
            justify="left"
        )
        self.content_label.grid(row=1, column=0, padx=12, pady=(4, 8), sticky="w")
        
        # Confidence
        if confidence > 0:
            self.conf_label = ctk.CTkLabel(
                self,
                text=f"Confidence: {confidence:.0f}%",
                font=("Segoe UI", 9),
                text_color="#5F6B78"
            )
            self.conf_label.grid(row=2, column=0, padx=12, pady=(0, 8), sticky="w")
    
    def update(self, title: str, content: str, category: str = None, confidence: float = None):
        """Update insight."""
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
                    self.conf_label = ctk.CTkLabel(
                        self,
                        text=f"Confidence: {confidence:.0f}%",
                        font=("Segoe UI", 9),
                        text_color="#5F6B78"
                    )
                    self.conf_label.grid(row=2, column=0, padx=12, pady=(0, 8), sticky="w")


class TimelineChart(ctk.CTkFrame):
    """Simple timeline chart with data points."""
    
    def __init__(
        self,
        parent,
        title: str = "Timeline",
        data: List[float] = None,
        labels: List[str] = None,
        color: str = "#3B82F6",
        **kwargs
    ):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        
        self.data = data or []
        self.labels = labels or []
        self.color = color
        
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 11, "bold"),
            text_color="#E8EDF2"
        )
        self.title_label.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")
        
        # Chart area
        self.chart_area = ctk.CTkFrame(
            self,
            fg_color="#0B0F14",
            corner_radius=6,
            height=100
        )
        self.chart_area.grid(row=1, column=0, padx=15, pady=(5, 12), sticky="ew")
        self.chart_area.grid_propagate(False)
        
        # Labels
        self.labels_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.labels_frame.grid(row=2, column=0, padx=15, pady=(0, 12), sticky="ew")
        
        self._update_chart()
    
    def _update_chart(self):
        """Update chart display."""
        # Clear chart area
        for widget in self.chart_area.winfo_children():
            widget.destroy()
        
        if not self.data:
            ctk.CTkLabel(
                self.chart_area,
                text="📊 No data available",
                font=("Segoe UI", 10),
                text_color="#5F6B78"
            ).place(relx=0.5, rely=0.5, anchor="center")
            return
        
        # Simple bar chart
        max_val = max(self.data) if self.data else 1
        if max_val == 0:
            max_val = 1
        
        width = self.chart_area.winfo_width() - 20
        if width < 50:
            width = 200
        
        bar_width = max(10, (width / len(self.data)) - 4)
        total_width = len(self.data) * (bar_width + 4)
        start_x = (width - total_width) // 2 if total_width < width else 0
        
        for i, value in enumerate(self.data):
            height = max(5, (value / max_val) * 70)
            bar = ctk.CTkFrame(
                self.chart_area,
                fg_color=self.color,
                corner_radius=2,
                width=bar_width,
                height=height
            )
            bar.place(x=start_x + i * (bar_width + 4), y=80 - height)
    
    def update_data(self, data: List[float], labels: List[str] = None):
        """Update chart data."""
        self.data = data
        if labels:
            self.labels = labels
        self._update_chart()


class PatternList(ctk.CTkScrollableFrame):
    """List of detected patterns."""
    
    def __init__(
        self,
        parent,
        title: str = "🔍 Detected Patterns",
        **kwargs
    ):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 11, "bold"),
            text_color="#E8EDF2"
        )
        self.title_label.grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")
        
        # Pattern container
        self.pattern_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.pattern_container.grid(row=1, column=0, padx=15, pady=(5, 12), sticky="ew")
        self.pattern_container.grid_columnconfigure(0, weight=1)
        
        self.pattern_labels = []
        self.pattern_count_label = ctk.CTkLabel(
            self,
            text="Total: 0 patterns",
            font=("Segoe UI", 9),
            text_color="#5F6B78"
        )
        self.pattern_count_label.grid(row=2, column=0, padx=15, pady=(0, 12), sticky="w")
    
    def update_patterns(self, patterns: List[Dict]):
        """Update pattern list."""
        # Clear existing
        for label in self.pattern_labels:
            label.destroy()
        self.pattern_labels.clear()
        
        # Add new patterns
        for i, pattern in enumerate(patterns[:20]):
            if isinstance(pattern, dict):
                name = pattern.get('name', pattern.get('type', 'Unknown'))
                confidence = pattern.get('confidence', 0)
                description = pattern.get('description', '')
            else:
                name = str(pattern)
                confidence = 0
                description = ''
            
            # Pattern item
            frame = ctk.CTkFrame(
                self.pattern_container,
                fg_color="#1A2430" if i % 2 == 0 else "transparent",
                corner_radius=4
            )
            frame.grid(row=i, column=0, padx=2, pady=2, sticky="ew")
            frame.grid_columnconfigure(0, weight=1)
            
            label_text = f"• {name}"
            if confidence > 0:
                label_text += f" ({confidence:.0f}%)"
            if description:
                label_text += f" - {description[:50]}"
            
            label = ctk.CTkLabel(
                frame,
                text=label_text,
                font=("Segoe UI", 10),
                text_color="#8D9AAA",
                anchor="w"
            )
            label.grid(row=0, column=0, padx=8, pady=4, sticky="w")
            self.pattern_labels.append(label)
        
        self.pattern_count_label.configure(text=f"Total: {len(patterns)} patterns")


class DecisionCard(ctk.CTkFrame):
    """Decision display card."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Title
        ctk.CTkLabel(
            self,
            text="🎯 Latest Decision",
            font=("Segoe UI", 11, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=(12, 5), sticky="w")
        
        # Action
        self.action_label = ctk.CTkLabel(
            self,
            text="HOLD",
            font=("Segoe UI", 24, "bold"),
            text_color="#F59E0B"
        )
        self.action_label.grid(row=1, column=0, padx=15, pady=5, sticky="w")
        
        # Confidence
        self.confidence_display = ctk.CTkLabel(
            self,
            text="Confidence: 0%",
            font=("Segoe UI", 12),
            text_color="#8D9AAA"
        )
        self.confidence_display.grid(row=2, column=0, padx=15, pady=(0, 5), sticky="w")
        
        # Reason
        self.reason_label = ctk.CTkLabel(
            self,
            text="Reason: Waiting for signal",
            font=("Segoe UI", 10),
            text_color="#5F6B78",
            wraplength=200
        )
        self.reason_label.grid(row=1, column=1, rowspan=2, padx=15, pady=5, sticky="w")
        
        # Timestamp
        self.timestamp_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 8),
            text_color="#5F6B78"
        )
        self.timestamp_label.grid(row=3, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="w")
    
    def update(self, action: str, confidence: float, reason: str, timestamp: str = None):
        """Update decision."""
        colors = {
            "BUY": "#22C55E",
            "STRONG BUY": "#16A34A",
            "SELL": "#EF4444",
            "STRONG SELL": "#DC2626",
            "HOLD": "#F59E0B",
            "MONITOR": "#3B82F6",
            "WAIT": "#8D9AAA",
            "NEUTRAL": "#6B7280",
        }
        self.action_label.configure(
            text=action,
            text_color=colors.get(action.upper(), "#8D9AAA")
        )
        self.confidence_display.configure(text=f"Confidence: {confidence:.0f}%")
        self.reason_label.configure(text=f"Reason: {reason}")
        
        if timestamp:
            self.timestamp_label.configure(text=f"Updated: {timestamp}")
        else:
            self.timestamp_label.configure(text=f"Updated: {datetime.now().strftime('%H:%M:%S')}")


class MemoryStats(ctk.CTkFrame):
    """Memory statistics display."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        # Title
        ctk.CTkLabel(
            self,
            text="💾 Memory Statistics",
            font=("Segoe UI", 11, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, columnspan=4, padx=15, pady=(12, 5), sticky="w")
        
        self.stats_labels = {}
        stat_items = [
            ("short_term", "Short Term"),
            ("long_term", "Long Term"),
            ("working", "Working"),
            ("semantic", "Semantic"),
            ("episodic", "Episodic"),
            ("procedural", "Procedural"),
            ("emotional", "Emotional"),
            ("associative", "Associative"),
        ]
        
        for i, (key, label) in enumerate(stat_items):
            row = 1 + i // 4
            col = i % 4
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
            
            ctk.CTkLabel(
                frame,
                text=f"{label}:",
                font=("Segoe UI", 9),
                text_color="#8D9AAA"
            ).pack(side="left")
            
            self.stats_labels[key] = ctk.CTkLabel(
                frame,
                text="0",
                font=("Segoe UI", 10, "bold"),
                text_color="#E8EDF2"
            )
            self.stats_labels[key].pack(side="left", padx=5)
    
    def update_stats(self, stats: Dict):
        """Update statistics."""
        if isinstance(stats, dict):
            for key, label in self.stats_labels.items():
                if key in stats:
                    label.configure(text=str(stats[key]))


class LearningProgress(ctk.CTkFrame):
    """Learning progress display."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#131A22", corner_radius=10, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        ctk.CTkLabel(
            self,
            text="📚 Learning Progress",
            font=("Segoe UI", 11, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")
        
        self.progress_bars = {}
        
        progress_items = [
            ("learning", "Learning", "#3B82F6"),
            ("reasoning", "Reasoning", "#8B5CF6"),
            ("pattern", "Pattern Recognition", "#EC4899"),
            ("memory", "Memory", "#06B6D4"),
            ("consciousness", "Consciousness", "#22C55E"),
            ("knowledge", "Knowledge", "#F59E0B"),
        ]
        
        for i, (key, label, color) in enumerate(progress_items):
            row = 1 + i
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=row, column=0, padx=15, pady=3, sticky="ew")
            frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(
                frame,
                text=f"{label}:",
                font=("Segoe UI", 9),
                text_color="#8D9AAA"
            ).grid(row=0, column=0, padx=(0, 10), sticky="w")
            
            bar = ctk.CTkProgressBar(
                frame,
                width=100,
                height=6,
                corner_radius=3,
                progress_color=color
            )
            bar.grid(row=0, column=1, sticky="ew")
            bar.set(0)
            
            self.progress_bars[key] = bar


class MarketTicker(ctk.CTkFrame):
    """Market ticker with price and change."""
    
    def __init__(
        self,
        parent,
        symbol: str = "BTC/USD",
        price: float = 0,
        change: float = 0,
        volume: float = 0,
        **kwargs
    ):
        super().__init__(
            parent,
            fg_color="#1A2530",
            corner_radius=8,
            **kwargs
        )
        
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
        
        # Symbol
        self.symbol_label = ctk.CTkLabel(
            self,
            text=self.symbol,
            font=("Segoe UI", 13, "bold"),
            text_color="#E8EDF2"
        )
        self.symbol_label.grid(row=0, column=0, padx=12, pady=10, sticky="w")
        
        # Price
        self.price_label = ctk.CTkLabel(
            self,
            text=f"${self.price:,.2f}" if self.price else "--",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        )
        self.price_label.grid(row=0, column=1, padx=12, sticky="e")
        
        # Change
        color = "#22C55E" if self.change >= 0 else "#EF4444"
        sign = "+" if self.change >= 0 else ""
        self.change_label = ctk.CTkLabel(
            self,
            text=f"{sign}{self.change:.2f}%",
            font=("Segoe UI", 12, "bold"),
            text_color=color
        )
        self.change_label.grid(row=0, column=2, padx=12, sticky="e")
        
        # Volume
        self.volume_label = ctk.CTkLabel(
            self,
            text=f"Vol: {self.volume:,.0f}" if self.volume else "",
            font=("Segoe UI", 9),
            text_color="#5F6B78"
        )
        self.volume_label.grid(row=0, column=3, padx=12, sticky="e")
    
    def update(self, price: float, change: float, volume: float = None):
        """Update ticker."""
        self.price = price
        self.change = change
        if volume is not None:
            self.volume = volume
        
        self.price_label.configure(
            text=f"${price:,.2f}" if price else "--"
        )
        
        color = "#22C55E" if change >= 0 else "#EF4444"
        sign = "+" if change >= 0 else ""
        self.change_label.configure(
            text=f"{sign}{change:.2f}%",
            text_color=color
        )
        
        if volume is not None or self.volume:
            self.volume_label.configure(
                text=f"Vol: {self.volume:,.0f}" if self.volume else ""
            )


class ProgressRing(ctk.CTkFrame):
    """Circular progress indicator."""
    
    def __init__(
        self,
        parent,
        value: float = 0,
        max_value: float = 100,
        size: int = 80,
        color: str = "#3B82F6",
        label: str = "",
        **kwargs
    ):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.value = value
        self.max_value = max_value
        self.size = size
        self.color = color
        self.label = label
        
        self._build_ui()
    
    def _build_ui(self):
        # Placeholder for circular progress
        # Using progress bar as fallback
        self.frame = ctk.CTkFrame(
            self,
            fg_color="#131A22",
            corner_radius=10,
            width=self.size,
            height=self.size
        )
        self.frame.pack()
        self.frame.grid_propagate(False)
        
        # Value label
        self.value_label = ctk.CTkLabel(
            self.frame,
            text=f"{self.value:.0f}%",
            font=("Segoe UI", 20, "bold"),
            text_color="#E8EDF2"
        )
        self.value_label.place(relx=0.5, rely=0.4, anchor="center")
        
        # Label
        if self.label:
            self.label_label = ctk.CTkLabel(
                self.frame,
                text=self.label,
                font=("Segoe UI", 9),
                text_color="#5F6B78"
            )
            self.label_label.place(relx=0.5, rely=0.7, anchor="center")
        
        # Progress bar (as ring replacement)
        self.progress = ctk.CTkProgressBar(
            self.frame,
            width=self.size - 20,
            height=6,
            corner_radius=3,
            progress_color=self.color
        )
        self.progress.place(relx=0.5, rely=0.85, anchor="center")
        self.progress.set(self.value / self.max_value if self.max_value > 0 else 0)
    
    def set_value(self, value: float):
        """Set progress value."""
        self.value = value
        self.value_label.configure(text=f"{value:.0f}%")
        self.progress.set(value / self.max_value if self.max_value > 0 else 0)


__all__ = [
    "StatusIndicator",
    "MetricCard",
    "SignalBadge",
    "ConfidenceBar",
    "TimelineChart",
    "PatternList",
    "InsightCard",
    "DecisionCard",
    "MemoryStats",
    "LearningProgress",
    "MarketTicker",
    "ProgressRing",
]