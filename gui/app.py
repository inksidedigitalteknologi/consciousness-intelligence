#!/usr/bin/env python3
# gui/app.py - Main GUI Application
# FIXED: Menerima bot dan learning_integration, kompatibel dengan main.py

import sys
import time
import gc
import logging
import threading
from typing import Optional, Dict, Any, Type

try:
    import customtkinter as ctk
    from tkinter import messagebox
except ImportError:
    print("❌ CustomTkinter not installed. Run: pip install customtkinter")
    sys.exit(1)

import config

logger = logging.getLogger(__name__)


class InksideBotApp(ctk.CTk):
    """
    Main Inkside Trading Bot GUI Application
    """
    
    def __init__(
        self,
        bot=None,
        learning_integration=None
    ):
        super().__init__()
        
        # ============================================================
        # BOT & LEARNING ENGINE
        # ============================================================
        self.bot = bot
        self.learning = learning_integration
        
        # ============================================================
        # APPLICATION CONFIG
        # ============================================================
        self.title("INKSIDEDIGITAL TRADING BOT")
        self.geometry("1400x800")
        self.minsize(1200, 700)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # ============================================================
        # STATE
        # ============================================================
        self.pages = {}
        self.navigation_buttons = {}
        self.current_page = None
        self.is_running = True
        self.engine_running = False
        self.engine_thread = None
        
        # ============================================================
        # BRAIN
        # ============================================================
        self.brain = None
        self._get_brain()
        
        # ============================================================
        # UPDATE CONTROL
        # ============================================================
        self.update_interval = 3000
        self.update_enabled = True
        self._update_thread = None
        self._stop_event = threading.Event()
        
        # ============================================================
        # BUILD UI
        # ============================================================
        self._create_ui()
        self._start_updates()
        
        # Bind events
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Configure>", self._on_resize)
        
        # ============================================================
        # SHOW DEFAULT PAGE
        # ============================================================
        self._switch_page("dashboard")
        
        logger.info("🚀 GUI initialized successfully")
    
    # ============================================================
    # BRAIN HELPER
    # ============================================================
    
    def _get_brain(self):
        """Get brain from various sources."""
        if self.bot:
            if hasattr(self.bot, 'brain'):
                self.brain = self.bot.brain
                return
            elif hasattr(self.bot, '_brain'):
                self.brain = self.bot._brain
                return
            elif hasattr(self.bot, 'get_brain'):
                try:
                    self.brain = self.bot.get_brain()
                    return
                except Exception:
                    pass
        
        if self.learning and hasattr(self.learning, 'brain'):
            self.brain = self.learning.brain
            return
        
        try:
            from core.brain import brain
            self.brain = brain
        except ImportError:
            pass
    
    # ============================================================
    # CREATE UI
    # ============================================================
    
    def _create_ui(self):
        """Create user interface"""
        # Create sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#0F141B")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(
            logo_frame,
            text="INKSIDE",
            font=("Segoe UI", 22, "bold"),
            text_color="#E8EDF2"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            logo_frame,
            text="DIGITAL",
            font=("Segoe UI", 12, "bold"),
            text_color="#3B82F6"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            logo_frame,
            text="COGNITIVE MIRROR ENGINE",
            font=("Segoe UI", 9),
            text_color="#5F6B78"
        ).pack(anchor="w", pady=(2, 0))
        
        # Learning status
        self.learning_status_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        self.learning_status_frame.pack(anchor="w", pady=(5, 0))
        
        self.learning_status_indicator = ctk.CTkLabel(
            self.learning_status_frame,
            text="◉",
            font=("Segoe UI", 10),
            text_color="#5F6B78"
        )
        self.learning_status_indicator.pack(side="left", padx=(0, 5))
        
        self.learning_status_label = ctk.CTkLabel(
            self.learning_status_frame,
            text="LEARNING: IDLE",
            font=("Segoe UI", 8, "bold"),
            text_color="#5F6B78"
        )
        self.learning_status_label.pack(side="left")
        
        # Navigation buttons
        nav_buttons = [
            ("📊 OVER", None),
            ("⌂ Dashboard", "dashboard"),
            ("🧠 INTELLIGENCE", None),
            ("🧠 Brain", "brain"),
            ("💭 Consciousness", "consciousness"),
            ("📚 Learning", "learning"),
            ("💾 Memory", "memory"),
            ("🔍 Pattern", "pattern"),
            ("📊 MARKET", None),
            ("📈 Market", "market"),
            ("🔍 Scanner", "scanner"),
            ("◆ Signals", "signals"),
            ("🔬 ANALYSIS", None),
            ("🔮 Prediction", "prediction"),
            ("🎯 Decision", "decision"),
            ("💭 Reflection", "reflection"),
            ("📊 MONITORS", None),
            ("❤️ Health", "health"),
            ("⚙️ SYSTEM", None),
            ("↗ Trading", "trading"),
            ("≡ Logs", "logs"),
        ]
        
        self.nav_buttons = {}
        nav_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        for label, page_name in nav_buttons:
            if page_name is None:
                ctk.CTkLabel(
                    nav_frame,
                    text=label,
                    font=("Segoe UI", 9, "bold"),
                    text_color="#5F6B78"
                ).pack(fill="x", padx=12, pady=(15, 5))
                continue
            
            btn = ctk.CTkButton(
                nav_frame,
                text=label,
                command=lambda p=page_name: self._switch_page(p),
                height=38,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#1A2530",
                text_color="#8D9AAA",
                font=("Segoe UI", 11),
                anchor="w"
            )
            btn.pack(pady=2, fill="x")
            self.nav_buttons[page_name] = btn
        
        # Footer
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=50)
        footer.pack(side="bottom", fill="x", padx=15, pady=15)
        
        self.status_indicator = ctk.CTkLabel(
            footer,
            text="●",
            font=("Segoe UI", 14),
            text_color="#22C55E"
        )
        self.status_indicator.pack(side="left", padx=(5, 8))
        
        self.status_label = ctk.CTkLabel(
            footer,
            text="SYSTEM ONLINE",
            font=("Segoe UI", 9, "bold"),
            text_color="#8D9AAA"
        )
        self.status_label.pack(side="left")
        
        # Main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#0B0F14")
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        # Top bar
        self.topbar = ctk.CTkFrame(
            self.main_frame,
            height=60,
            corner_radius=0,
            fg_color="#131A22",
            border_width=1,
            border_color="#26313D"
        )
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)
        
        # Page title
        self.page_title = ctk.CTkLabel(
            self.topbar,
            text="Dashboard",
            font=("Segoe UI", 22, "bold"),
            text_color="#E8EDF2"
        )
        self.page_title.pack(side="left", padx=25, pady=10)
        
        # Top right status
        status_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        status_frame.pack(side="right", padx=15)
        
        self.exchange_status = ctk.CTkLabel(
            status_frame,
            text="● KRAKEN",
            font=("Segoe UI", 10, "bold"),
            text_color="#22C55E"
        )
        self.exchange_status.pack(side="left", padx=10)
        
        self.clock_label = ctk.CTkLabel(
            status_frame,
            text="00:00:00",
            font=("Segoe UI", 11, "bold"),
            text_color="#E8EDF2"
        )
        self.clock_label.pack(side="left", padx=15)
        
        # Content container
        self.content_container = ctk.CTkFrame(self.main_frame, fg_color="#0B0F14")
        self.content_container.pack(fill="both", expand=True)
        
        # Create pages
        self._create_pages()
    
    # ============================================================
    # CREATE PAGES
    # ============================================================
    
    def _create_pages(self):
        """Create all page instances"""
        self.page_classes = {}
        
        # Try to import pages
        try:
            from gui.intelligence import (
                DashboardPage, Brain, Consciousness, Learning,
                Memory, Pattern, Prediction, Decision,
                Reflection, Health, Market, Scanner,
                Signals, Trading
            )
            
            # Register pages with their names
            page_mapping = {
                "dashboard": DashboardPage,
                "brain": Brain,
                "consciousness": Consciousness,
                "learning": Learning,
                "memory": Memory,
                "pattern": Pattern,
                "prediction": Prediction,
                "decision": Decision,
                "reflection": Reflection,
                "health": Health,
                "market": Market,
                "scanner": Scanner,
                "signals": Signals,
                "trading": Trading,
            }
            
            for name, page_class in page_mapping.items():
                if page_class is not None:
                    self.page_classes[name] = page_class
            
            logger.info(f"✅ {len(self.page_classes)} intelligence pages registered")
            
        except ImportError as e:
            logger.warning(f"⚠️ Intelligence pages not available: {e}")
            self.page_classes = {}
        
        # Create placeholders for missing pages
        self.page_instances = {}
        for name in self.page_classes:
            self.page_instances[name] = None
    
    # ============================================================
    # SWITCH PAGE
    # ============================================================
    
    def _switch_page(self, page_name: str):
        """Switch to a specific page"""
        # Hide all pages
        for instance in self.page_instances.values():
            if instance:
                try:
                    if hasattr(instance, 'on_hide'):
                        instance.on_hide()
                    instance.pack_forget()
                    instance.grid_forget()
                except:
                    pass
        
        # Update nav buttons
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.configure(fg_color="#3B82F6", text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color="#8D9AAA")
        
        # Update page title
        title_map = {
            "dashboard": "Dashboard",
            "brain": "Brain",
            "consciousness": "Consciousness",
            "learning": "Learning",
            "memory": "Memory",
            "pattern": "Pattern",
            "prediction": "Prediction",
            "decision": "Decision",
            "reflection": "Reflection",
            "health": "Health",
            "market": "Market",
            "scanner": "Scanner",
            "signals": "Signals",
            "trading": "Trading",
        }
        self.page_title.configure(text=title_map.get(page_name, page_name.capitalize()))
        
        # Create page if not exists
        if page_name not in self.page_instances:
            self.page_instances[page_name] = None
        
        if self.page_instances[page_name] is None:
            try:
                page_class = self.page_classes.get(page_name)
                if page_class:
                    # Try different constructor patterns
                    try:
                        instance = page_class(self.content_container)
                    except TypeError:
                        try:
                            instance = page_class(self.content_container, bot=self.bot)
                        except TypeError:
                            try:
                                instance = page_class(self.content_container, bot=self.bot, learning_integration=self.learning)
                            except TypeError:
                                try:
                                    instance = page_class(self.content_container, self.bot)
                                except TypeError:
                                    instance = page_class(self.content_container, bot=self.bot, learning=self.learning)
                    
                    # Set references
                    if instance:
                        if hasattr(instance, 'set_bot') and self.bot is not None:
                            try:
                                instance.set_bot(self.bot)
                            except Exception:
                                pass
                        
                        if hasattr(instance, 'set_learning') and self.learning is not None:
                            try:
                                instance.set_learning(self.learning)
                            except Exception:
                                pass
                        
                        if hasattr(instance, 'set_brain') and self.brain is not None:
                            try:
                                instance.set_brain(self.brain)
                            except Exception:
                                pass
                        
                        if hasattr(instance, 'brain') and self.brain is not None:
                            instance.brain = self.brain
                        
                        self.page_instances[page_name] = instance
                        logger.info(f"✅ Page loaded: {page_name}")
            except Exception as e:
                logger.error(f"❌ Failed to create page {page_name}: {e}")
                import traceback
                traceback.print_exc()
                self.page_instances[page_name] = self._create_placeholder(page_name)
        
        # Show page
        instance = self.page_instances[page_name]
        if instance:
            instance.pack(fill="both", expand=True)
            if hasattr(instance, 'on_show'):
                try:
                    instance.on_show()
                except Exception:
                    pass
            self.current_page = page_name
    
    def _create_placeholder(self, page_name: str):
        """Create placeholder for unavailable page"""
        placeholder = ctk.CTkFrame(self.content_container, fg_color="transparent")
        
        ctk.CTkLabel(
            placeholder,
            text=f"📄 {page_name.title()}\n\nPage under construction...",
            font=("Segoe UI", 18),
            text_color="#5F6B78"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        return placeholder
    
    # ============================================================
    # UPDATE LOOP
    # ============================================================
    
    def _start_updates(self):
        """Start background updates"""
        self._stop_event.clear()
        self._update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self._update_thread.start()
        self.update_clock()
    
    def _update_loop(self):
        """Background update loop"""
        while not self._stop_event.is_set():
            try:
                if self.update_enabled and self.current_page:
                    page = self.page_instances.get(self.current_page)
                    if page and hasattr(page, 'update_data'):
                        page.update_data()
            except Exception as e:
                logger.error(f"Update error: {e}")
            
            time.sleep(self.update_interval / 1000.0)
    
    def update_clock(self):
        """Update clock display"""
        if not self.is_running:
            return
        from datetime import datetime
        self.clock_label.configure(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self.update_clock)
    
    def _on_resize(self, event):
        """Handle window resize"""
        pass
    
    # ============================================================
    # CLOSE
    # ============================================================
    
    def on_closing(self):
        """Handle window closing"""
        self.is_running = False
        self.update_enabled = False
        self._stop_event.set()
        
        if self._update_thread and self._update_thread.is_alive():
            self._update_thread.join(timeout=2.0)
        
        # Cleanup pages
        for instance in self.page_instances.values():
            if instance and hasattr(instance, 'destroy'):
                try:
                    instance.destroy()
                except:
                    pass
        
        gc.collect()
        self.destroy()
        logger.info("👋 Application closed")


# ============================================================
# MAIN
# ============================================================

def main():
    """Main entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )
    
    app = InksideBotApp()
    app.mainloop()


if __name__ == '__main__':
    main()
