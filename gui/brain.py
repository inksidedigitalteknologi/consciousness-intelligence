# gui/intelligence/brain.py
# ============================================================
# BRAIN - Brain Status & Insights (VIEW ONLY)
# Menampilkan status, kesehatan, dan insight dari Cognitive Brain
# TANPA TOMBOL KONTROL MANUAL – SEMUA OTOMATIS DARI ENGINE
# ============================================================

import random
import json
import traceback
from datetime import datetime
from typing import Dict, Optional, Any, List

import customtkinter as ctk

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard, InsightCard


class Brain(IntelligencePage):
    """
    Halaman Brain – Menampilkan status, kesehatan, dan insight dari Cognitive Brain.
    TANPA tombol kontrol manual karena semua dikontrol oleh Engine.
    """

    def __init__(self, parent, *args, **kwargs):
        # ============================================================
        # ATRIBUT
        # ============================================================
        self.brain_data: Dict[str, Any] = {}
        self.brain_instances: Dict[str, Any] = {}
        self.active_brain_name: str = "default"
        self.last_error: Optional[str] = None
        self.last_error_time: Optional[datetime] = None

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

        # UI components
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
        self.after(100, self.update_data)

    # ============================================================
    # PUBLIC METHODS
    # ============================================================

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

    # ============================================================
    # BRAIN SELECTOR
    # ============================================================

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
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)

        ctk.CTkLabel(
            header,
            text="🧠 Brain Status & Insights",
            font=("Segoe UI", 22, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")

        self.status_indicator = StatusIndicator(header, label="Brain")
        self.status_indicator.grid(row=0, column=1, padx=10)

        self.last_update_label = ctk.CTkLabel(
            header,
            text="Last update: --",
            font=("Segoe UI", 10),
            text_color="#5F6B78"
        )
        self.last_update_label.grid(row=0, column=2, padx=10)

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
        self.refresh_btn.grid(row=0, column=3, padx=10)

        # BRAIN SELECTOR
        self.selector_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        self.selector_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.selector_frame.grid_columnconfigure(0, weight=0)
        self.selector_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.selector_frame,
            text="Active Brain:",
            font=("Segoe UI", 12),
            text_color="#8D9AAA"
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.brain_selector = ctk.CTkOptionMenu(
            self.selector_frame,
            values=["default"],
            command=self._on_brain_selected,
            width=200,
            height=32,
            fg_color="#1A2530",
            button_color="#2A3A4A",
            button_hover_color="#3B4A5A",
            text_color="#E8EDF2"
        )
        self.brain_selector.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        self.brain_selector.set("default")

        # METRICS CARDS
        metrics_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        metrics_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(2, weight=1)
        metrics_frame.grid_columnconfigure(3, weight=1)
        metrics_frame.grid_columnconfigure(4, weight=1)

        ctk.CTkLabel(
            metrics_frame,
            text="📊 Brain Metrics",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, columnspan=5, padx=15, pady=10, sticky="w")

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

        # INSIGHTS
        insights_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        insights_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        insights_frame.grid_rowconfigure(0, weight=0)
        insights_frame.grid_rowconfigure(1, weight=1)
        insights_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            insights_frame,
            text="💡 Brain Insights",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.insight_container = ctk.CTkFrame(insights_frame, fg_color="transparent")
        self.insight_container.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.insight_container.grid_columnconfigure(0, weight=1)
        self.insight_container.grid_columnconfigure(1, weight=1)

        self.insight_cards = []
        for i in range(4):
            card = InsightCard(
                self.insight_container,
                title="--",
                content="No insight available"
            )
            row = i // 2
            col = i % 2
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.insight_cards.append(card)

        # DETAILS
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        details.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            details,
            text="📋 Raw Brain Data",
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
                self.last_update_label.configure(
                    text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
                )

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

    def _get_brain_status(self) -> Optional[Dict[str, Any]]:
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

    def _generate_fallback_data(self) -> Dict[str, Any]:
        states = ["ACTIVE", "IDLE", "DEGRADED", "ERROR"]
        return {
            "state": random.choice(states),
            "cycles": random.randint(0, 100),
            "errors": random.randint(0, 20),
            "success_rate": random.randint(40, 95),
            "health_score": random.randint(50, 100),
            "version": "4.2.3",
            "is_fallback": True,
            "timestamp": datetime.now().isoformat()
        }

    # ============================================================
    # UPDATE UI
    # ============================================================

    def _update_ui(self):
        data = self.brain_data
        if not data:
            return

        state = data.get("state", "UNKNOWN")
        cycles = data.get("cycles", 0)
        errors = data.get("errors", 0)
        success_rate = data.get("success_rate", 0)
        is_fallback = data.get("is_fallback", False)

        # ============================================================
        # FIX: HITUNG HEALTH SCORE SECARA OTOMATIS
        # ============================================================
        health_score = data.get("health_score")
        if health_score is None:
            # Mulai dari 100
            score = 100.0
            # Kurangi error (masing-masing -2%, maks -30%)
            score -= min(errors * 2, 30)
            # Kurangi jika state error/degraded
            if state in ["ERROR", "STOPPED"]:
                score -= 30
            elif state == "DEGRADED":
                score -= 15
            # Tambah bonus dari success rate (jika > 50%)
            if success_rate > 50:
                score += (success_rate - 50) * 0.2
            health_score = max(0, min(100, round(score, 2)))
            data["health_score"] = health_score

        # State card
        if self.state_card:
            color = self._get_state_color(state)
            self.state_card.update_value(state, color=color)
            self.state_card.update_subtitle("Brain state")

        # Cycles
        if self.cycles_card:
            self.cycles_card.update_value(str(cycles))

        # Errors
        if self.errors_card:
            color = "#EF4444" if errors > 0 else "#22C55E"
            self.errors_card.update_value(str(errors), color=color)

        # Success rate
        if self.success_card:
            color = self._get_score_color(success_rate)
            self.success_card.update_value(f"{success_rate:.1f}%", color=color)

        # Health score
        if self.health_card:
            color = self._get_score_color(health_score)
            self.health_card.update_value(f"{health_score:.1f}%", color=color)
            subtitle = "Brain health"
            if is_fallback:
                subtitle += " (fallback)"
            self.health_card.update_subtitle(subtitle)

        # Status indicator
        if self.status_indicator:
            self.status_indicator.set_status(state not in ["ERROR", "STOPPED"])

        # Insights
        insights = self._generate_insights(data)
        for i, card in enumerate(self.insight_cards):
            if i < len(insights):
                insight = insights[i]
                card.update(insight.get("title", "---"), insight.get("content", "No data available"))
            else:
                card.update("---", "No data available")

        # Details textbox
        if self.details_text:
            details_data = {
                "timestamp": datetime.now().isoformat(),
                "brain_data": data,
                "update_count": self.update_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
                "is_fallback": is_fallback,
                "brain_available": self._brain_available,
                "active_instance": self.active_brain_name,
                "instances": list(self.brain_instances.keys())
            }
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

        # Insight 1: Aktivitas
        if cycles > 0:
            insights.append({
                "title": "🧠 Activity",
                "content": f"Brain has processed {cycles} cycles with {success_rate:.1f}% success rate.",
                "category": "activity",
                "confidence": 90
            })
        else:
            insights.append({
                "title": "🧠 Activity",
                "content": "Brain is idle or has not processed any cycles yet.",
                "category": "activity",
                "confidence": 50
            })

        # Insight 2: Status
        if state in ["ACTIVE", "RUNNING"]:
            insights.append({
                "title": "✅ Status",
                "content": "Brain is active and operational.",
                "category": "status",
                "confidence": 95
            })
        elif state == "DEGRADED":
            insights.append({
                "title": "⚠️ Status",
                "content": "Brain is degraded. Some modules may be unavailable.",
                "category": "status",
                "confidence": 70
            })
        elif state == "ERROR":
            insights.append({
                "title": "❌ Status",
                "content": "Brain is in error state. Check logs for details.",
                "category": "status",
                "confidence": 90
            })
        else:
            insights.append({
                "title": "⏸️ Status",
                "content": f"Brain is in {state} state.",
                "category": "status",
                "confidence": 60
            })

        # Insight 3: Kesehatan
        if health_score >= 80:
            insights.append({
                "title": "❤️ Health",
                "content": f"Brain health score is {health_score:.1f}% – excellent condition.",
                "category": "health",
                "confidence": health_score
            })
        elif health_score >= 50:
            insights.append({
                "title": "❤️ Health",
                "content": f"Brain health score is {health_score:.1f}% – moderate condition. Monitor closely.",
                "category": "health",
                "confidence": health_score
            })
        else:
            insights.append({
                "title": "❤️ Health",
                "content": f"Brain health score is {health_score:.1f}% – critical condition. Immediate attention required.",
                "category": "health",
                "confidence": health_score
            })

        # Insight 4: Error
        if errors > 0:
            insights.append({
                "title": "🐛 Errors",
                "content": f"Brain has {errors} errors. Recommended to check logs and restart if necessary.",
                "category": "errors",
                "confidence": 70
            })
        else:
            insights.append({
                "title": "✅ Errors",
                "content": "No errors detected. Brain is running cleanly.",
                "category": "errors",
                "confidence": 90
            })

        insights.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        return insights[:4]

    def _update_error_display(self, error: Exception):
        try:
            if self.details_text:
                self.details_text.delete("1.0", "end")
                self.details_text.insert(
                    "1.0",
                    f"❌ ERROR\n\n"
                    f"Error: {error}\n"
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Updates: {self.update_count}\n"
                    f"Success: {self.success_count}\n"
                    f"Errors: {self.error_count}\n\n"
                    f"Traceback:\n{traceback.format_exc()}"
                )
            if self.status_indicator:
                self.status_indicator.set_status(False)
        except Exception:
            pass

    # ============================================================
    # CONTROL METHODS
    # ============================================================

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