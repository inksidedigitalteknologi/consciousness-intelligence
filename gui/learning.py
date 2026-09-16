#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# gui/intelligence/learning.py
# LEARNING - Learning Engine Status (VIEW ONLY)
# 
# Menampilkan status Learning Engine dan modul-modul terdaftar.
# TANPA tombol kontrol – semua dikendalikan oleh master engine.
# ============================================================

import customtkinter as ctk
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard, LearningProgress

# ============================================================
# IMPORT CONFIG DARI config.py
# ============================================================

from config import (
    LEARNING_UPDATE_INTERVAL,
    LEARNING_MAX_MODULES_DISPLAY,
    LEARNING_CYCLE_THRESHOLD,
    LEARNING_MODULE_THRESHOLD,
    LEARNING_STATUS_RUNNING,
    LEARNING_STATUS_IDLE,
    LEARNING_STATUS_UNAVAILABLE,
    LEARNING_STATUS_NOT_INSTALLED,
    LEARNING_MODULE_ENABLED_COLOR,
    LEARNING_MODULE_DISABLED_COLOR,
    LEARNING_MODULE_DEFAULT_COLOR,
    LEARNING_ICON_ENABLED,
    LEARNING_ICON_DISABLED,
    LEARNING_ICON_UNKNOWN,
    LEARNING_DETAILS_MAX_LENGTH,
)


class Learning(IntelligencePage):
    """
    Halaman Learning – Menampilkan status dan modul Learning Engine.
    VIEW ONLY – tidak ada tombol kontrol manual.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Data storage
        self.engine_status: Dict = {}
        self.module_specs: List[Any] = []   # ModuleSpec objects
        self.knowledge_stats: Dict = {}
        self.history: List[Dict] = []
        self.learning_integration = None

        # Status
        self.is_connected = False
        self.last_error: Optional[str] = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = LEARNING_UPDATE_INTERVAL
        self.bot = None

        # Cache untuk mencegah flashing
        self._last_module_hash = None

        # Build UI
        self._build_ui()
        self.update_data()

    # ============================================================
    # PUBLIC METHODS
    # ============================================================

    def set_bot(self, bot):
        self.bot = bot

    def set_learning(self, learning):
        self.learning_integration = learning

    # ============================================================
    # BUILD UI
    # ============================================================

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")

        ctk.CTkLabel(
            header,
            text="📚 Learning Engine",
            font=("Segoe UI", 22, "bold"),
            text_color="#E8EDF2"
        ).pack(side="left")

        self.learning_status = StatusIndicator(header, label="Learning")
        self.learning_status.pack(side="right", padx=10)

        self.last_update_label = ctk.CTkLabel(
            header,
            text="Last update: --",
            font=("Segoe UI", 10),
            text_color="#5F6B78"
        )
        self.last_update_label.pack(side="right", padx=10)

        self.refresh_btn = ctk.CTkButton(
            header,
            text="🔄 Refresh",
            width=80,
            height=28,
            font=("Segoe UI", 11),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.refresh
        )
        self.refresh_btn.pack(side="right", padx=10)

        # METRICS - Row 1
        metrics_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        metrics_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(2, weight=1)
        metrics_frame.grid_columnconfigure(3, weight=1)
        metrics_frame.grid_columnconfigure(4, weight=1)

        ctk.CTkLabel(
            metrics_frame,
            text="📊 Learning Metrics",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, columnspan=5, padx=15, pady=10, sticky="w")

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

        # PROGRESS - Row 2
        self.progress = LearningProgress(self)
        self.progress.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # MODULE LIST - Row 3
        modules_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        modules_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        modules_frame.grid_columnconfigure(0, weight=1)
        modules_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            modules_frame,
            text="📋 Registered Modules",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")

        self.modules_container = ctk.CTkScrollableFrame(
            modules_frame,
            fg_color="transparent",
            height=150
        )
        self.modules_container.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.modules_container.grid_columnconfigure(0, weight=1)
        self.modules_container.grid_columnconfigure(1, weight=1)

        self.module_labels: List[ctk.CTkFrame] = []

        # DETAILS - Row 4
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            details,
            text="📋 Learning Details",
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
    # UPDATE DATA
    # ============================================================

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

    # ============================================================
    # COLLECT DATA
    # ============================================================

    def _collect_data(self):
        self.engine_status = {}
        self.module_specs = []
        self.knowledge_stats = {}

        # 1. DARI LEARNING INTEGRATION
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

        # 2. DARI CORE LEARNING ENGINE
        try:
            from core.learning.engine import learning_engine
            if learning_engine:
                # Status
                if hasattr(learning_engine, 'status'):
                    status = learning_engine.status()
                    if status:
                        self.engine_status.update(status)
                elif hasattr(learning_engine, 'get_state'):
                    state = learning_engine.get_state()
                    if state:
                        self.engine_status.update(state)

                # Ambil daftar modul dari registry
                if hasattr(learning_engine, 'registry') and learning_engine.registry:
                    try:
                        self.module_specs = learning_engine.registry.all()
                    except Exception as e:
                        print(f"[Learning] Registry error: {e}")
        except ImportError:
            pass
        except Exception as e:
            print(f"[Learning] Core engine error: {e}")

        # 3. DARI KNOWLEDGE
        try:
            from core.knowledge import knowledge
            if knowledge and hasattr(knowledge, 'stats'):
                stats = knowledge.stats()
                if stats:
                    self.knowledge_stats = {
                        "total": getattr(stats, 'total', 0),
                        "states": getattr(stats, 'state_count', 0),
                        "avg_confidence": getattr(stats, 'avg_confidence', 0),
                        "active": getattr(stats, 'active', 0),
                        "archived": getattr(stats, 'archived', 0),
                    }
        except ImportError:
            pass
        except Exception as e:
            print(f"[Learning] Knowledge error: {e}")

    # ============================================================
    # UPDATE UI
    # ============================================================

    def _update_ui(self):
        # Status indicator
        running = self.engine_status.get('running', False)
        initialized = self.engine_status.get('initialized', False)
        available = self.engine_status.get('available', False)

        if available and initialized:
            self.learning_status.set_status(running)
        else:
            self.learning_status.set_status(False)

        # Metrics
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

        # Progress bars
        try:
            learning_progress = min(1.0, cycles / LEARNING_CYCLE_THRESHOLD) if cycles > 0 else 0
            if hasattr(self, 'progress') and self.progress:
                if hasattr(self.progress, 'progress_bars') and 'learning' in self.progress.progress_bars:
                    self.progress.progress_bars['learning'].set(learning_progress)
        except Exception:
            pass

        try:
            module_progress = min(1.0, module_count / LEARNING_MODULE_THRESHOLD) if module_count > 0 else 0
            if hasattr(self, 'progress') and self.progress:
                if hasattr(self.progress, 'progress_bars') and 'modules' in self.progress.progress_bars:
                    self.progress.progress_bars['modules'].set(module_progress)
        except Exception:
            pass

        # Module list
        self._update_modules()

        # Details
        details_data = {
            "timestamp": datetime.now().isoformat(),
            "update_count": self.update_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "engine_status": self.engine_status,
            "knowledge_stats": self.knowledge_stats,
            "module_count": module_count,
            "has_learning": self.learning_integration is not None,
            "has_core_engine": 'core.learning.engine' in str(self.engine_status),
        }
        if self.last_error:
            details_data["last_error"] = self.last_error

        if hasattr(self, 'details_text') and self.details_text:
            try:
                self.details_text.delete("1.0", "end")
                text = json.dumps(details_data, indent=2, default=str)
                if len(text) > LEARNING_DETAILS_MAX_LENGTH:
                    text = text[:LEARNING_DETAILS_MAX_LENGTH] + "\n... (truncated)"
                self.details_text.insert("1.0", text)
            except Exception as e:
                print(f"[Learning] Details update error: {e}")

        self.last_update_label.configure(
            text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
        )

    # ============================================================
    # MODULE LIST
    # ============================================================

    def _update_modules(self):
        # Cegah flashing dengan hash
        current_hash = hash(str(self.module_specs))
        if hasattr(self, '_last_module_hash') and self._last_module_hash == current_hash:
            return
        self._last_module_hash = current_hash

        # Clear existing
        for frame in self.module_labels:
            try:
                frame.destroy()
            except Exception:
                pass
        self.module_labels.clear()

        if self.module_specs:
            for i, spec in enumerate(self.module_specs[:LEARNING_MAX_MODULES_DISPLAY]):
                # spec bisa berupa ModuleSpec atau dict
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

                frame = ctk.CTkFrame(
                    self.modules_container,
                    fg_color="#1A2430" if i % 2 == 0 else "transparent",
                    corner_radius=4
                )
                row = i // 2
                col = i % 2
                frame.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
                frame.grid_columnconfigure(0, weight=1)

                status_icon = LEARNING_ICON_ENABLED if enabled else LEARNING_ICON_DISABLED
                status_color = LEARNING_MODULE_ENABLED_COLOR if enabled else LEARNING_MODULE_DISABLED_COLOR

                label = ctk.CTkLabel(
                    frame,
                    text=f"{status_icon} {name} v{version} (prio:{priority})",
                    font=("Segoe UI", 11),
                    text_color=status_color,
                    anchor="w"
                )
                label.grid(row=0, column=0, padx=10, pady=6, sticky="w")
                self.module_labels.append(frame)
        else:
            # Empty state dengan informasi yang lebih bermanfaat
            empty_frame = ctk.CTkFrame(self.modules_container, fg_color="transparent")
            empty_frame.grid(row=0, column=0, padx=10, pady=20)
            empty_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                empty_frame,
                text="📦",
                font=("Segoe UI", 32),
                text_color="#5F6B78"
            ).grid(row=0, column=0, pady=(0, 5))

            ctk.CTkLabel(
                empty_frame,
                text="No Modules Registered",
                font=("Segoe UI", 16, "bold"),
                text_color="#E8EDF2"
            ).grid(row=1, column=0)

            ctk.CTkLabel(
                empty_frame,
                text="Modules will appear here when registered by Learning Engine.",
                font=("Segoe UI", 12),
                text_color="#5F6B78"
            ).grid(row=2, column=0, pady=(5, 10))

            # Informasi tambahan
            tips = [
                "• Start the master engine to register modules.",
                "• Check 'Learning Details' above for engine status.",
            ]
            for i, tip in enumerate(tips):
                ctk.CTkLabel(
                    empty_frame,
                    text=tip,
                    font=("Segoe UI", 10),
                    text_color="#5F6B78"
                ).grid(row=3+i, column=0, pady=1, sticky="w")

            self.module_labels.append(empty_frame)

    # ============================================================
    # CONTROL METHODS
    # ============================================================

    def refresh(self):
        self.update_data()

    def stop(self):
        self.is_running = False

    def destroy(self):
        self.stop()
        super().destroy()