# gui/trading.py
# ============================================================
# TRADING PAGE
# Clean & Lightweight Trading Control Interface
# ============================================================

import logging
import threading
from datetime import datetime

import customtkinter as ctk

logger = logging.getLogger(__name__)


class TradingPage(ctk.CTkFrame):
    """
    Trading Control Interface.
    Start/Stop trading engine with paper/auto modes.
    Lightweight — no heavy background threads.
    """

    def __init__(self, parent, bot=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.bot = bot
        self.is_running = False
        self._activity_counter = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_ui()
        self._update_status()

    # ============================================================
    # BUILD UI
    # ============================================================

    def _build_ui(self):
        """Build entire trading interface."""
        self._build_header()
        self._build_status_panel()
        self._build_main_content()
        self._build_activity_log()

    def _build_header(self):
        """Build header with title and status badge."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            title_frame,
            text="📈 Trading Control",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Manage automated trading execution and risk controls",
            font=ctk.CTkFont(size=13),
            text_color=("gray55", "gray65")
        ).pack(anchor="w", pady=(2, 0))

        # Status Badge
        self.status_badge = ctk.CTkLabel(
            header,
            text="●  READY",
            height=34,
            corner_radius=17,
            fg_color=("#1f6f43", "#14532d"),
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            padx=18
        )
        self.status_badge.grid(row=0, column=1, sticky="e")

    def _build_status_panel(self):
        """Build 4-column status metrics."""
        panel = ctk.CTkFrame(
            self,
            corner_radius=14,
            border_width=1,
            border_color=("gray85", "gray20")
        )
        panel.grid(row=1, column=0, sticky="ew", padx=28, pady=8)

        for i in range(4):
            panel.grid_columnconfigure(i, weight=1)

        self.bot_status = self._create_metric(panel, "🤖 BOT STATUS", "READY", 0)
        self.position_count = self._create_metric(panel, "📊 POSITIONS", "0", 1)
        self.pnl_value = self._create_metric(panel, "💰 TODAY PNL", "$0.00", 2)
        self.last_action = self._create_metric(panel, "🔄 LAST ACTION", "Waiting", 3)

    def _create_metric(self, parent, title, value, column):
        """Create a single status metric."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, sticky="ew", padx=16, pady=12)

        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=("gray50", "gray60")
        ).pack(anchor="w")

        label = ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(size=17, weight="bold")
        )
        label.pack(anchor="w", pady=(4, 0))

        return label

    def _build_main_content(self):
        """Build main content: controls + activity."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=2, column=0, sticky="nsew", padx=28, pady=(10, 16))
        container.grid_columnconfigure(0, weight=3)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)

        # ----- LEFT: Trading Controls -----
        self._build_controls_panel(container)

        # ----- RIGHT: Activity Log -----
        self._build_activity_panel(container)

    def _build_controls_panel(self, container):
        """Build trading controls (left side)."""
        panel = ctk.CTkFrame(
            container,
            corner_radius=14,
            border_width=1,
            border_color=("gray85", "gray20")
        )
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        panel.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            panel,
            text="⚙️ Trading Engine",
            font=ctk.CTkFont(size=17, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 4))

        ctk.CTkLabel(
            panel,
            text="Configure and control automated execution",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray65")
        ).grid(row=1, column=0, sticky="w", padx=24)

        # Settings container
        settings = ctk.CTkFrame(panel, fg_color="transparent")
        settings.grid(row=2, column=0, sticky="nsew", padx=24, pady=16)
        settings.grid_columnconfigure(0, weight=1)

        # ----- Switch: Automated Trading -----
        self.auto_switch = self._create_switch(
            settings,
            "🤖 Automated Trading",
            "Allow bot to execute trades automatically",
            0
        )

        # ----- Switch: Paper Trading -----
        self.paper_switch = self._create_switch(
            settings,
            "📄 Paper Trading",
            "Simulate trades without real funds",
            1
        )
        self.paper_switch.select()  # Default: enabled

        # ----- Control Buttons -----
        btn_frame = ctk.CTkFrame(settings, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="▶  Start Engine",
            height=44,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.start_engine
        )
        self.start_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text="⏹  Stop Engine",
            height=44,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#64748b", "#475569"),
            hover_color=("#475569", "#334155"),
            command=self.stop_engine,
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def _create_switch(self, parent, title, description, row):
        """Create a single toggle switch."""
        frame = ctk.CTkFrame(
            parent,
            corner_radius=10,
            border_width=1,
            border_color=("gray90", "gray15")
        )
        frame.grid(row=row, column=0, sticky="ew", pady=5)

        text_frame = ctk.CTkFrame(frame, fg_color="transparent")
        text_frame.pack(side="left", padx=16, pady=10)

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60")
        ).pack(anchor="w", pady=(1, 0))

        switch = ctk.CTkSwitch(frame, text="", command=self._on_switch_toggle)
        switch.pack(side="right", padx=16)

        return switch

    def _build_activity_panel(self, container):
        """Build activity log panel (right side)."""
        panel = ctk.CTkFrame(
            container,
            corner_radius=14,
            border_width=1,
            border_color=("gray85", "gray20")
        )
        panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(2, weight=1)

        # Title
        ctk.CTkLabel(
            panel,
            text="📋 Activity Log",
            font=ctk.CTkFont(size=17, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 4))

        ctk.CTkLabel(
            panel,
            text="Real-time trading engine events",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray65")
        ).grid(row=1, column=0, sticky="w", padx=24)

        # Activity text box
        self.activity_log = ctk.CTkTextbox(
            panel,
            corner_radius=10,
            border_width=0,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=("gray95", "gray10")
        )
        self.activity_log.grid(row=2, column=0, sticky="nsew", padx=20, pady=(12, 20))

        # Initial message
        self._log_activity("SYSTEM  | Trading engine initialized.")
        self._log_activity("SYSTEM  | Paper trading mode enabled.")
        self._log_activity("SYSTEM  | Waiting for activation...")

    def _build_activity_log(self):
        """Activity log is built inside _build_activity_panel."""
        pass  # Already built

    # ============================================================
    # SWITCH HANDLERS
    # ============================================================

    def _on_switch_toggle(self):
        """Handle switch toggle events."""
        if self.auto_switch.get():
            self._log_activity("CONFIG  | Automated trading ENABLED")
        else:
            self._log_activity("CONFIG  | Automated trading DISABLED")

        if self.paper_switch.get():
            self._log_activity("CONFIG  | Paper trading ENABLED")
        else:
            self._log_activity("CONFIG  | Paper trading DISABLED (LIVE MODE)")

    # ============================================================
    # ENGINE CONTROLS
    # ============================================================

    def start_engine(self):
        """Start the trading engine."""
        if self.is_running:
            return

        self.is_running = True

        # Update UI
        self.bot_status.configure(text="RUNNING")
        self.status_badge.configure(
            text="●  ENGINE RUNNING",
            fg_color=("#1f6f43", "#14532d")
        )
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.last_action.configure(text="Engine Started")

        self._log_activity("ENGINE  | Trading engine STARTED")

        # Start bot in background
        if self.bot and hasattr(self.bot, "start"):
            try:
                threading.Thread(target=self.bot.start, daemon=True).start()
            except Exception as e:
                logger.exception(f"Bot start error: {e}")
                self._log_activity(f"ERROR   | {e}")

    def stop_engine(self):
        """Stop the trading engine."""
        if not self.is_running:
            return

        self.is_running = False

        # Update UI
        self.bot_status.configure(text="STOPPED")
        self.status_badge.configure(
            text="●  ENGINE STOPPED",
            fg_color=("#7f1d1d", "#991b1b")
        )
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.last_action.configure(text="Engine Stopped")

        self._log_activity("ENGINE  | Trading engine STOPPED")

        # Stop bot in background
        if self.bot and hasattr(self.bot, "stop"):
            try:
                threading.Thread(target=self.bot.stop, daemon=True).start()
            except Exception as e:
                logger.exception(f"Bot stop error: {e}")
                self._log_activity(f"ERROR   | {e}")

    # ============================================================
    # ACTIVITY LOG
    # ============================================================

    def _log_activity(self, message):
        """Log activity with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"

        # Limit log size (keep last 200 lines)
        self._activity_counter += 1

        try:
            self.activity_log.configure(state="normal")
            self.activity_log.insert("end", line)

            # Keep log size manageable
            if self._activity_counter > 200:
                self.activity_log.delete("1.0", "50.end")
                self._activity_counter = 150

            self.activity_log.see("end")
            self.activity_log.configure(state="disabled")
        except Exception as e:
            logger.debug(f"Activity log error: {e}")

    # ============================================================
    # PUBLIC UPDATE METHODS
    # ============================================================

    def update_positions(self, count):
        """Update active positions count."""
        try:
            self.position_count.configure(text=str(int(count)))
        except Exception:
            self.position_count.configure(text=str(count))

    def update_pnl(self, pnl):
        """Update today's PnL."""
        try:
            self.pnl_value.configure(text=f"${float(pnl):,.2f}")
        except Exception:
            self.pnl_value.configure(text=str(pnl))

    def update_status(self, status):
        """Update bot status."""
        self.bot_status.configure(text=str(status).upper())

    def update_last_action(self, action):
        """Update last action text."""
        self.last_action.configure(text=str(action)[:20])

    def add_activity(self, message):
        """Add custom activity message."""
        self._log_activity(message)

    def _update_status(self):
        """Initial status update."""
        # Placeholder for future auto-refresh if needed
        pass

    # ============================================================
    # LIFECYCLE
    # ============================================================

    def set_bot(self, bot):
        """Set bot reference."""
        self.bot = bot

    def on_show(self):
        """Called when page becomes visible."""
        # Refresh status
        if self.bot and hasattr(self.bot, "get_status"):
            try:
                status = self.bot.get_status()
                if status:
                    self.update_status(status.get("state", "UNKNOWN"))
            except Exception:
                pass

    def destroy(self):
        """Clean up resources."""
        self.is_running = False
        super().destroy()