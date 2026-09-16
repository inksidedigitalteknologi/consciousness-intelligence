# gui/telegram.py
# ============================================================
# TELEGRAM PAGE — Minimal & Elegant
# ============================================================

import logging
import threading
import customtkinter as ctk

logger = logging.getLogger(__name__)


class TelegramPage(ctk.CTkFrame):
    """
    Telegram Control Interface.
    Otomatis mengambil konfigurasi dari bot.
    """

    def __init__(self, parent, bot=None, telegram_service=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.bot = bot
        self.telegram_service = telegram_service

        # 🔥 Jika telegram_service tidak diberikan, coba ambil dari bot
        if self.telegram_service is None and self.bot is not None:
            if hasattr(self.bot, 'telegram'):
                self.telegram_service = self.bot.telegram
                logger.info("✅ Telegram service loaded from bot")
            elif hasattr(self.bot, 'telegram_service'):
                self.telegram_service = self.bot.telegram_service
                logger.info("✅ Telegram service loaded from bot")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_ui()
        self._refresh_status()

    # ... sisanya sama seperti kode sebelumnya ...

    def _refresh_status(self):
        """Refresh status — otomatis dari bot."""
        if not self.telegram_service:
            # Coba ambil dari bot sekali lagi
            if self.bot and hasattr(self.bot, 'telegram'):
                self.telegram_service = self.bot.telegram
            elif self.bot and hasattr(self.bot, 'telegram_service'):
                self.telegram_service = self.bot.telegram_service

        if not self.telegram_service:
            self._set_status(
                "NOT AVAILABLE", "N/A", "N/A",
                "●  SERVICE UNAVAILABLE", ("#7f1d1d", "#991b1b")
            )
            return

        try:
            # Cek apakah token & chat_id ada (dari environment atau config)
            token = getattr(self.telegram_service, 'token', None)
            chat_id = getattr(self.telegram_service, 'chat_id', None)

            if token and chat_id:
                # Token ada, cek apakah valid (test connection)
                self._set_status(
                    "CONFIGURED", "✅ SET", "✅ SET",
                    "●  CONFIGURED", ("#1f6f43", "#14532d")
                )
            elif token:
                self._set_status(
                    "PARTIAL", "✅ SET", "❌ MISSING",
                    "●  PARTIAL CONFIG", ("#854d0e", "#a16207")
                )
            elif chat_id:
                self._set_status(
                    "PARTIAL", "❌ MISSING", "✅ SET",
                    "●  PARTIAL CONFIG", ("#854d0e", "#a16207")
                )
            else:
                self._set_status(
                    "NOT CONFIGURED", "❌ MISSING", "❌ MISSING",
                    "●  NOT CONFIGURED", ("#7f1d1d", "#991b1b")
                )

            # Isi field dengan token yang sudah ada (tapi jangan tampilkan full)
            if token:
                masked = token[:8] + "..." + token[-4:] if len(token) > 12 else "***"
                self.token_entry.delete(0, "end")
                self.token_entry.insert(0, masked)

            if chat_id:
                self.chat_id_entry.delete(0, "end")
                self.chat_id_entry.insert(0, str(chat_id))

        except Exception as e:
            logger.exception(f"Telegram status error: {e}")
            self._set_status(
                "ERROR", "ERROR", "ERROR",
                "●  ERROR", ("#7f1d1d", "#991b1b")
            )

    def test_connection(self):
        """Test connection — otomatis dari bot."""
        if not self.telegram_service:
            # Coba ambil dari bot
            if self.bot and hasattr(self.bot, 'telegram'):
                self.telegram_service = self.bot.telegram
            elif self.bot and hasattr(self.bot, 'telegram_service'):
                self.telegram_service = self.bot.telegram_service

            if not self.telegram_service:
                self._show_status("❌ Telegram service not available.", error=True)
                return

        # Coba test
        self.test_btn.configure(state="disabled", text="⏳ Testing...")
        self.status_badge.configure(text="●  CONNECTING", fg_color=("#854d0e", "#a16207"))

        def worker():
            try:
                if hasattr(self.telegram_service, 'test_connection'):
                    result = self.telegram_service.test_connection()
                elif hasattr(self.telegram_service, 'send_message'):
                    # Kirim test message
                    result = self.telegram_service.send_message(
                        "✅ Telegram test message from INKSIDEDIGITAL Bot."
                    )
                else:
                    result = False

                if result:
                    self.after(0, lambda: self._show_status("✅ Connection successful."))
                    self.after(0, lambda: self.status_badge.configure(
                        text="●  CONNECTED", fg_color=("#1f6f43", "#14532d")
                    ))
                    self.after(0, lambda: self.connection_value.configure(text="CONNECTED"))
                else:
                    self.after(0, lambda: self._show_status("❌ Connection failed.", error=True))
                    self.after(0, lambda: self.status_badge.configure(
                        text="●  FAILED", fg_color=("#7f1d1d", "#991b1b")
                    ))
            except Exception as e:
                self.after(0, lambda: self._show_status(f"❌ Error: {e}", error=True))
                self.after(0, lambda: self.status_badge.configure(
                    text="●  ERROR", fg_color=("#7f1d1d", "#991b1b")
                ))
            finally:
                self.after(0, lambda: self.test_btn.configure(state="normal", text="✈  Test Connection"))

        threading.Thread(target=worker, daemon=True).start()

    def save_configuration(self):
        """Save configuration — hanya untuk update, token dari bot sudah ada."""
        token = self.token_entry.get().strip()
        chat_id = self.chat_id_entry.get().strip()

        # Jika token masih masked, jangan overwrite
        if token and "..." in token:
            # Token masih masked, ambil dari service
            if self.telegram_service and hasattr(self.telegram_service, 'token'):
                token = self.telegram_service.token

        if not token or not chat_id:
            # Coba ambil dari service
            if self.telegram_service:
                if hasattr(self.telegram_service, 'token') and self.telegram_service.token:
                    token = self.telegram_service.token
                if hasattr(self.telegram_service, 'chat_id') and self.telegram_service.chat_id:
                    chat_id = self.telegram_service.chat_id

            if not token or not chat_id:
                self._show_status("⚠️ Token & Chat ID already set in bot. No manual entry needed.", error=True)
                return

        try:
            if self.telegram_service:
                self.telegram_service.token = token
                self.telegram_service.chat_id = chat_id
                self._show_status("✅ Configuration updated successfully.")
                self._refresh_status()
            else:
                self._show_status("❌ Service not available.", error=True)
        except Exception as e:
            logger.exception(f"Save error: {e}")
            self._show_status(f"Error: {e}", error=True)