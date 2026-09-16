# ============================================================
# INKSIDE DIGITAL TRADING BOT
# SETTINGS PAGE
# Version: 3.0 Professional Terminal
# ============================================================

import customtkinter as ctk
import logging


logger = logging.getLogger(__name__)


class SettingsPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        bot=None,
        **kwargs
    ):

        super().__init__(
            parent,
            fg_color="transparent",
            **kwargs
        )

        self.bot = bot

        # ====================================================
        # GRID CONFIGURATION
        # ====================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        # ====================================================
        # BUILD PAGE
        # ====================================================

        self._build_header()

        self._build_status_panel()

        self._build_settings_panel()

    # ========================================================
    # HEADER
    # ========================================================

    def _build_header(
        self
    ):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(24, 10)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_frame.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            title_frame,
            text="System Settings",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_frame,
            text=(
                "Configure trading engine behavior, "
                "market scanning and application preferences"
            ),
            font=ctk.CTkFont(
                size=13
            ),
            text_color=(
                "gray45",
                "gray65"
            )
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        # ----------------------------------------------------
        # STATUS BADGE
        # ----------------------------------------------------

        self.status_badge = ctk.CTkLabel(
            header,
            text="●  SYSTEM READY",
            height=34,
            corner_radius=17,
            fg_color=(
                "#1f6f43",
                "#14532d"
            ),
            text_color="white",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            padx=18
        )

        self.status_badge.grid(
            row=0,
            column=1,
            sticky="e"
        )

    # ========================================================
    # STATUS PANEL
    # ========================================================

    def _build_status_panel(
        self
    ):

        panel = ctk.CTkFrame(
            self,
            corner_radius=16,
            border_width=1,
            border_color=(
                "gray80",
                "gray25"
            )
        )

        panel.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=28,
            pady=10
        )

        for column in range(4):

            panel.grid_columnconfigure(
                column,
                weight=1
            )

        # ----------------------------------------------------
        # BOT
        # ----------------------------------------------------

        self.bot_status_value = self._create_metric(
            panel,
            "BOT STATUS",
            "READY",
            0
        )

        # ----------------------------------------------------
        # MODE
        # ----------------------------------------------------

        self.mode_value = self._create_metric(
            panel,
            "TRADING MODE",
            "PAPER",
            1
        )

        # ----------------------------------------------------
        # SCAN INTERVAL
        # ----------------------------------------------------

        self.interval_value = self._create_metric(
            panel,
            "SCAN INTERVAL",
            "60 SEC",
            2
        )

        # ----------------------------------------------------
        # CONFIGURATION
        # ----------------------------------------------------

        self.config_value = self._create_metric(
            panel,
            "CONFIGURATION",
            "READY",
            3
        )

    # ========================================================
    # METRIC
    # ========================================================

    def _create_metric(
        self,
        parent,
        title,
        value,
        column
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=20,
            pady=18
        )

        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=(
                "gray50",
                "gray60"
            )
        ).pack(
            anchor="w"
        )

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        value_label.pack(
            anchor="w",
            pady=(5, 0)
        )

        return value_label

    # ========================================================
    # MAIN SETTINGS PANEL
    # ========================================================

    def _build_settings_panel(
        self
    ):

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(10, 28)
        )

        container.grid_columnconfigure(
            0,
            weight=3
        )

        container.grid_columnconfigure(
            1,
            weight=2
        )

        container.grid_rowconfigure(
            0,
            weight=1
        )

        # ====================================================
        # LEFT PANEL
        # ====================================================

        left_panel = ctk.CTkFrame(
            container,
            corner_radius=16,
            border_width=1,
            border_color=(
                "gray80",
                "gray25"
            )
        )

        left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        left_panel.grid_columnconfigure(
            0,
            weight=1
        )

        left_panel.grid_rowconfigure(
            2,
            weight=1
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        ctk.CTkLabel(
            left_panel,
            text="Trading Configuration",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=24,
            pady=(22, 4)
        )

        ctk.CTkLabel(
            left_panel,
            text=(
                "Configure the behavior of the trading engine"
            ),
            font=ctk.CTkFont(
                size=12
            ),
            text_color=(
                "gray50",
                "gray65"
            )
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=24
        )

        settings_frame = ctk.CTkFrame(
            left_panel,
            fg_color="transparent"
        )

        settings_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=24,
            pady=20
        )

        settings_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # PAPER TRADING
        # ====================================================

        self.paper_mode = ctk.BooleanVar(
            value=True
        )

        self._create_switch(
            settings_frame,
            title="Paper Trading Mode",
            description=(
                "Simulate trades without using real funds"
            ),
            variable=self.paper_mode,
            row=0
        )

        # ====================================================
        # AUTO TRADING
        # ====================================================

        self.auto_trading = ctk.BooleanVar(
            value=False
        )

        self._create_switch(
            settings_frame,
            title="Automated Trading",
            description=(
                "Allow the trading engine to execute trades automatically"
            ),
            variable=self.auto_trading,
            row=1
        )

        # ====================================================
        # TELEGRAM NOTIFICATIONS
        # ====================================================

        self.telegram_notifications = ctk.BooleanVar(
            value=True
        )

        self._create_switch(
            settings_frame,
            title="Telegram Notifications",
            description=(
                "Send trading signals and system events to Telegram"
            ),
            variable=self.telegram_notifications,
            row=2
        )

        # ====================================================
        # LOGGING
        # ====================================================

        self.extended_logging = ctk.BooleanVar(
            value=True
        )

        self._create_switch(
            settings_frame,
            title="Extended Logging",
            description=(
                "Enable detailed application and trading logs"
            ),
            variable=self.extended_logging,
            row=3
        )

        # ====================================================
        # SCAN INTERVAL
        # ====================================================

        interval_frame = ctk.CTkFrame(
            settings_frame,
            corner_radius=12
        )

        interval_frame.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=6
        )

        interval_frame.grid_columnconfigure(
            0,
            weight=1
        )

        interval_text = ctk.CTkFrame(
            interval_frame,
            fg_color="transparent"
        )

        interval_text.grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=12
        )

        ctk.CTkLabel(
            interval_text,
            text="Market Scan Interval",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            interval_text,
            text=(
                "Time interval between automatic market scans"
            ),
            font=ctk.CTkFont(
                size=11
            ),
            text_color=(
                "gray50",
                "gray65"
            )
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        self.interval_entry = ctk.CTkEntry(
            interval_frame,
            width=100,
            height=38,
            corner_radius=8,
            placeholder_text="60"
        )

        self.interval_entry.grid(
            row=0,
            column=1,
            padx=16
        )

        self.interval_entry.insert(
            0,
            "60"
        )

        # ====================================================
        # SAVE BUTTON
        # ====================================================

        self.save_button = ctk.CTkButton(
            settings_frame,
            text="SAVE SETTINGS",
            height=44,
            corner_radius=10,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.save_settings
        )

        self.save_button.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(20, 5)
        )

        # ====================================================
        # RIGHT PANEL
        # ====================================================

        right_panel = ctk.CTkFrame(
            container,
            corner_radius=16,
            border_width=1,
            border_color=(
                "gray80",
                "gray25"
            )
        )

        right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        right_panel.grid_columnconfigure(
            0,
            weight=1
        )

        right_panel.grid_rowconfigure(
            2,
            weight=1
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        ctk.CTkLabel(
            right_panel,
            text="System Information",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=24,
            pady=(22, 4)
        )

        ctk.CTkLabel(
            right_panel,
            text=(
                "Current application configuration and runtime information"
            ),
            font=ctk.CTkFont(
                size=12
            ),
            text_color=(
                "gray50",
                "gray65"
            )
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=24,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # INFORMATION BOX
        # ----------------------------------------------------

        info_box = ctk.CTkFrame(
            right_panel,
            corner_radius=12
        )

        info_box.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )

        info_box.grid_columnconfigure(
            1,
            weight=1
        )

        self._create_info_row(
            info_box,
            "Application",
            "INKSIDEDIGITAL TRADING BOT",
            0
        )

        self._create_info_row(
            info_box,
            "Version",
            "3.0 Professional Terminal",
            1
        )

        self._create_info_row(
            info_box,
            "Trading Engine",
            "Connected"
            if self.bot
            else "GUI Mode",
            2
        )

        self._create_info_row(
            info_box,
            "Market Data",
            "Kraken",
            3
        )

        self._create_info_row(
            info_box,
            "Interface",
            "CustomTkinter",
            4
        )

        self._create_info_row(
            info_box,
            "Environment",
            "Python",
            5
        )

        # ----------------------------------------------------
        # STATUS MESSAGE
        # ----------------------------------------------------

        self.status_message = ctk.CTkLabel(
            right_panel,
            text="Ready to configure system settings.",
            font=ctk.CTkFont(
                size=11
            ),
            text_color=(
                "gray50",
                "gray65"
            ),
            wraplength=400
        )

        self.status_message.grid(
            row=3,
            column=0,
            sticky="w",
            padx=24,
            pady=(0, 20)
        )

    # ========================================================
    # SWITCH CREATOR
    # ========================================================

    def _create_switch(
        self,
        parent,
        title,
        description,
        variable,
        row
    ):

        frame = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        frame.grid(
            row=row,
            column=0,
            sticky="ew",
            pady=6
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        text_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        text_frame.grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=12
        )

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            text_frame,
            text=description,
            font=ctk.CTkFont(
                size=11
            ),
            text_color=(
                "gray50",
                "gray65"
            )
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        switch = ctk.CTkSwitch(
            frame,
            text="",
            variable=variable
        )

        switch.grid(
            row=0,
            column=1,
            padx=18
        )

        if variable.get():

            switch.select()

        else:

            switch.deselect()

        return switch

    # ========================================================
    # INFORMATION ROW
    # ========================================================

    def _create_info_row(
        self,
        parent,
        label,
        value,
        row
    ):

        ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=(
                "gray50",
                "gray65"
            ),
            anchor="w"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=18,
            pady=10
        )

        ctk.CTkLabel(
            parent,
            text=value,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            anchor="e"
        ).grid(
            row=row,
            column=1,
            sticky="e",
            padx=18,
            pady=10
        )

    # ========================================================
    # SAVE SETTINGS
    # ========================================================

    def save_settings(
        self
    ):

        try:

            interval_text = (
                self.interval_entry
                .get()
                .strip()
            )

            # ------------------------------------------------
            # VALIDATE INTERVAL
            # ------------------------------------------------

            if not interval_text:

                interval_text = "60"

            interval = int(
                interval_text
            )

            if interval < 5:

                self._show_status(
                    "Scan interval must be at least 5 seconds.",
                    error=True
                )

                return

            # ------------------------------------------------
            # UPDATE BOT IF AVAILABLE
            # ------------------------------------------------

            if self.bot is not None:

                try:

                    if hasattr(
                        self.bot,
                        "scan_interval"
                    ):

                        self.bot.scan_interval = interval

                    if hasattr(
                        self.bot,
                        "paper_mode"
                    ):

                        self.bot.paper_mode = (
                            self.paper_mode.get()
                        )

                    if hasattr(
                        self.bot,
                        "auto_trading"
                    ):

                        self.bot.auto_trading = (
                            self.auto_trading.get()
                        )

                except Exception as e:

                    logger.warning(
                        "Unable to apply settings to bot: %s",
                        e
                    )

            # ------------------------------------------------
            # UPDATE UI
            # ------------------------------------------------

            mode = (
                "PAPER"
                if self.paper_mode.get()
                else "LIVE"
            )

            self.mode_value.configure(
                text=mode
            )

            self.interval_value.configure(
                text=f"{interval} SEC"
            )

            self.bot_status_value.configure(
                text=(
                    "READY"
                    if not self.auto_trading.get()
                    else "AUTO"
                )
            )

            self.config_value.configure(
                text="SAVED"
            )

            self.status_badge.configure(
                text="●  SETTINGS SAVED",
                fg_color=(
                    "#1f6f43",
                    "#14532d"
                )
            )

            self._show_status(
                "System settings saved successfully."
            )

            logger.info(
                "Settings saved: paper_mode=%s, auto_trading=%s, "
                "telegram=%s, extended_logging=%s, interval=%s",
                self.paper_mode.get(),
                self.auto_trading.get(),
                self.telegram_notifications.get(),
                self.extended_logging.get(),
                interval
            )

        except ValueError:

            self._show_status(
                "Scan interval must be a valid number.",
                error=True
            )

        except Exception as e:

            logger.exception(
                "Unable to save settings: %s",
                e
            )

            self._show_status(
                f"Unable to save settings: {e}",
                error=True
            )

    # ========================================================
    # STATUS MESSAGE
    # ========================================================

    def _show_status(
        self,
        message,
        error=False
    ):

        try:

            self.status_message.configure(
                text=message,
                text_color=(
                    "#ef4444"
                    if error
                    else "#22c55e"
                )
            )

        except Exception as e:

            logger.warning(
                "Unable to update settings status: %s",
                e
            )

    # ========================================================
    # PUBLIC METHODS
    # ========================================================

    def update_bot_status(
        self,
        status
    ):

        try:

            self.bot_status_value.configure(
                text=str(
                    status
                ).upper()
            )

        except Exception:

            pass

    def set_scan_interval(
        self,
        interval
    ):

        try:

            self.interval_entry.delete(
                0,
                "end"
            )

            self.interval_entry.insert(
                0,
                str(interval)
            )

            self.interval_value.configure(
                text=f"{interval} SEC"
            )

        except Exception:

            pass