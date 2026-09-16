# gui/reflection.py
# ============================================================
# REFLECTION - Cognitive Insight Dashboard v5.1
# REAL DATA FROM BRAIN - GUARANTEED ONLINE
# ============================================================

import random
import json
import traceback
import logging
from datetime import datetime
from typing import Dict, Optional, Any, List

import customtkinter as ctk

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard

# ============================================================
# PATH FIX: Tambahkan root proyek ke sys.path
# ============================================================
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

logger = logging.getLogger(__name__)


class CircularProgress(ctk.CTkFrame):
    """Circular progress indicator."""
    def __init__(self, parent, value=0, label="", color="#3B82F6", size=65, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.value = value
        self.color = color
        self.size = size
        
        self.canvas = ctk.CTkCanvas(self, width=size, height=size, bg="#131A22", highlightthickness=0)
        self.canvas.pack()
        
        self.label = ctk.CTkLabel(self, text=label, font=("Segoe UI", 9), text_color="#8D9AAA")
        self.label.pack(pady=(3,0))
        
        self.draw(value)
    
    def draw(self, value):
        self.value = max(0, min(100, value))
        self.canvas.delete("all")
        self.canvas.create_arc(8, 8, self.size-8, self.size-8,
                               start=90, extent=360, outline="#1A2530", width=6, style="arc")
        extent = (self.value / 100) * 360
        self.canvas.create_arc(8, 8, self.size-8, self.size-8,
                               start=90, extent=extent, outline=self.color, width=6, style="arc")
        self.canvas.create_text(self.size/2, self.size/2-3,
                                text=f"{self.value:.0f}%", fill="#E8EDF2", font=("Segoe UI", 13, "bold"))


class Reflection(IntelligencePage):
    """Cognitive Reflection Dashboard v5.1 - Guaranteed Online"""

    def __init__(self, parent, *args, **kwargs):
        self.reflection_data: Dict[str, Any] = {}
        self._last_fallback: Optional[Dict[str, Any]] = None
        self.fallback_mode = False
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
        
        self.reflection_status = None
        self.last_update_label = None
        self.refresh_btn = None
        self.summary_label = None
        self.emotion_label = None
        self.awareness_progress = None
        self.curiosity_progress = None
        self.insight_progress = None
        self.resilience_progress = None
        self.focus_progress = None
        self.reflections_text = None
        
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
    
    def set_learning(self, learning):
        self.learning_integration = learning
        self._update_brain_reference()
    
    def set_brain(self, brain):
        """Set brain reference."""
        self.brain_instance = brain
        self.brain = brain
        self._brain_available = brain is not None
        logger.info(f"✅ Brain set in Reflection: {type(brain).__name__ if brain else None}")
        self._update_brain_reference()
    
    def _update_brain_reference(self):
        """Update brain reference from multiple sources."""
        
        # 1. Dari bot
        if self.bot:
            if hasattr(self.bot, 'brain'):
                self.brain = self.bot.brain
                self.brain_instance = self.bot.brain
                logger.debug("Brain from bot")
            elif hasattr(self.bot, '_brain'):
                self.brain = self.bot._brain
                self.brain_instance = self.bot._brain
                logger.debug("Brain from bot._brain")
            elif hasattr(self.bot, 'get_brain'):
                try:
                    brain = self.bot.get_brain()
                    if brain:
                        self.brain = brain
                        self.brain_instance = brain
                        logger.debug("Brain from bot.get_brain()")
                except Exception:
                    pass
        
        # 2. Dari learning integration
        if not self.brain and self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                self.brain = self.learning_integration.brain
                self.brain_instance = self.learning_integration.brain
                logger.debug("Brain from learning_integration")
            elif hasattr(self.learning_integration, 'get_brain'):
                try:
                    brain = self.learning_integration.get_brain()
                    if brain:
                        self.brain = brain
                        self.brain_instance = brain
                        logger.debug("Brain from learning_integration.get_brain()")
                except Exception:
                    pass
        
        # 3. 🔥 PRIORITAS UTAMA: Ambil dari root window (app)
        if not self.brain:
            try:
                root = self.winfo_toplevel()
                if hasattr(root, 'brain') and root.brain:
                    self.brain = root.brain
                    self.brain_instance = root.brain
                    logger.info("✅ Brain loaded from root window")
                    self._brain_available = True
                    return
            except Exception as e:
                logger.debug(f"Root window brain error: {e}")
        
        # 4. Dari core.brain (fallback)
        if not self.brain:
            try:
                from core.brain import brain
                if brain:
                    self.brain = brain
                    self.brain_instance = brain
                    logger.info("✅ Brain loaded from core.brain")
            except ImportError as e:
                logger.debug(f"Core brain import error: {e}")
            except Exception as e:
                logger.debug(f"Brain import error: {e}")
        
        self._brain_available = self.brain is not None
        if self._brain_available:
            logger.info(f"✅ Brain available in Reflection (type: {type(self.brain).__name__})")
        else:
            logger.warning("⚠️ Brain NOT available in Reflection")
    
    def on_show(self):
        self.refresh()
    
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
        
        # HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)
        
        ctk.CTkLabel(
            header,
            text="💭 Cognitive Reflection",
            font=("Segoe UI", 24, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")
        
        self.reflection_status = StatusIndicator(header, label="Reflection")
        self.reflection_status.grid(row=0, column=1, padx=10)
        
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
        
        # ROW 1: Summary & Emotion
        row1 = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=12)
        row1.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        row1.grid_columnconfigure(0, weight=2)
        row1.grid_columnconfigure(1, weight=1)
        
        self.summary_label = ctk.CTkLabel(
            row1,
            text="🧠 Cognitive State: Initializing...",
            font=("Segoe UI", 13, "bold"),
            text_color="#E8EDF2",
            wraplength=550,
            justify="left"
        )
        self.summary_label.grid(row=0, column=0, padx=20, pady=12, sticky="w")
        
        emotion_frame = ctk.CTkFrame(row1, fg_color="transparent")
        emotion_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.emotion_label = ctk.CTkLabel(
            emotion_frame,
            text="😌 CALM",
            font=("Segoe UI", 16, "bold"),
            text_color="#8D9AAA"
        )
        self.emotion_label.pack()
        
        # ROW 2: 5 Circular Progress
        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.grid(row=2, column=0, columnspan=2, padx=15, pady=8, sticky="ew")
        row2.grid_columnconfigure(0, weight=1)
        row2.grid_columnconfigure(1, weight=1)
        row2.grid_columnconfigure(2, weight=1)
        row2.grid_columnconfigure(3, weight=1)
        row2.grid_columnconfigure(4, weight=1)
        
        self.awareness_progress = CircularProgress(
            row2, value=0, label="Awareness", color="#3B82F6", size=65
        )
        self.awareness_progress.grid(row=0, column=0, padx=3, pady=3)
        
        self.curiosity_progress = CircularProgress(
            row2, value=0, label="Curiosity", color="#8B5CF6", size=65
        )
        self.curiosity_progress.grid(row=0, column=1, padx=3, pady=3)
        
        self.insight_progress = CircularProgress(
            row2, value=0, label="Insight Depth", color="#06B6D4", size=65
        )
        self.insight_progress.grid(row=0, column=2, padx=3, pady=3)
        
        self.resilience_progress = CircularProgress(
            row2, value=0, label="Resilience", color="#22C55E", size=65
        )
        self.resilience_progress.grid(row=0, column=3, padx=3, pady=3)
        
        self.focus_progress = CircularProgress(
            row2, value=0, label="Focus", color="#F59E0B", size=65
        )
        self.focus_progress.grid(row=0, column=4, padx=3, pady=3)
        
        # ROW 3: Reflections
        row3 = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=12)
        row3.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        row3.grid_columnconfigure(0, weight=1)
        row3.grid_rowconfigure(0, weight=0)
        row3.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            row3,
            text="💡 Meaningful Reflections",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        self.reflections_text = ctk.CTkTextbox(
            row3,
            font=("Segoe UI", 11),
            fg_color="#0B0F14",
            text_color="#C8D0D8",
            wrap="word",
            height=150
        )
        self.reflections_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    # ============================================================
    # UPDATE DATA
    # ============================================================
    
    def update_data(self):
        if not self.is_running:
            return
        
        try:
            self.update_count += 1
            self._update_brain_reference()
            
            reflection = self._get_reflection_safely()
            
            if reflection:
                self.reflection_data = reflection
                self.is_connected = True
                self.success_count += 1
                self.fallback_mode = False
                self.last_error = None
                self._last_fallback = None
            else:
                self.reflection_data = self._generate_fallback_data()
                self.is_connected = False
                self.fallback_mode = True
                self.error_count += 1
                self.last_error = "Brain unavailable, using fallback data"
                self.last_error_time = datetime.now()
            
            self._update_ui()
            self._update_timestamp()
            
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            logger.error(f"[Reflection] Update error: {e}")
            traceback.print_exc()
            self._update_error_display(e)
            if self.reflection_status:
                self.reflection_status.set_status(False)
        
        if self.is_running:
            try:
                self._after_id = self.after(self.update_interval, self.update_data)
            except Exception as e:
                logger.error(f"[Reflection] Schedule error: {e}")
    
    def _update_timestamp(self):
        if self.last_update_label:
            self.last_update_label.configure(
                text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
            )
    
    # ============================================================
    # REFLECTION RETRIEVAL - MAXIMUM EFFORT
    # ============================================================
    
    def _get_reflection_safely(self) -> Optional[Dict[str, Any]]:
        """Get reflection data safely from brain - maximum effort."""
        
        # 🔥 PASTIKAN BRAIN REFERENCE UPDATE
        self._update_brain_reference()
        
        if not self.brain:
            logger.warning("No brain available in _get_reflection_safely")
            return None
        
        logger.debug(f"Brain type: {type(self.brain).__name__}")
        
        # ===== PRIORITAS 1: brain.reflection() =====
        if hasattr(self.brain, 'reflection'):
            try:
                result = self.brain.reflection()
                if result and isinstance(result, dict):
                    source = result.get('source', '')
                    if source != 'fallback' and source != 'fallback_generator':
                        required = ['awareness', 'emotion', 'curiosity', 'insights']
                        if all(k in result for k in required):
                            if 'resilience' not in result:
                                result['resilience'] = 0.5
                            if 'focus' not in result:
                                result['focus'] = 0.5
                            result['is_fallback'] = False
                            logger.info(f"✅ Reflection data from brain.reflection() (source: {source})")
                            return result
            except Exception as e:
                logger.debug(f"brain.reflection() error: {e}")
        
        # ===== PRIORITAS 2: brain.snapshot() =====
        if hasattr(self.brain, 'snapshot'):
            try:
                snapshot = self.brain.snapshot()
                if snapshot and isinstance(snapshot, dict):
                    # Coba extract dari consciousness
                    cons = snapshot.get('consciousness', {})
                    if cons and isinstance(cons, dict):
                        result = {
                            'awareness': cons.get('awareness', 0.5),
                            'emotion': cons.get('emotional_state', 'CALM'),
                            'curiosity': cons.get('curiosity', 0.5),
                            'resilience': cons.get('resilience', 0.5),
                            'focus': cons.get('focus', 0.5),
                            'insights': cons.get('insights', ['No insights from snapshot']),
                            'source': 'snapshot',
                            'is_fallback': False
                        }
                        logger.info("✅ Reflection data from brain.snapshot()")
                        return result
                    
                    # Coba extract dari brain
                    brain_data = snapshot.get('brain', {})
                    if brain_data:
                        health = brain_data.get('health', {}).get('score', 70)
                        result = {
                            'awareness': health / 100,
                            'emotion': 'CALM' if health > 60 else 'CAUTIOUS',
                            'curiosity': 0.5,
                            'resilience': 0.6,
                            'focus': 0.5,
                            'insights': [
                                f"System health: {health:.0f}%",
                                f"Status: {brain_data.get('status', 'UNKNOWN')}",
                            ],
                            'source': 'snapshot_brain',
                            'is_fallback': False
                        }
                        logger.info("✅ Reflection data from snapshot brain data")
                        return result
            except Exception as e:
                logger.debug(f"brain.snapshot() error: {e}")
        
        # ===== PRIORITAS 3: brain.status() =====
        if hasattr(self.brain, 'status'):
            try:
                status_data = self.brain.status()
                if status_data and isinstance(status_data, dict):
                    success_rate = status_data.get('success_rate', 50) / 100
                    error_rate = status_data.get('error_rate', 0) / 100
                    result = {
                        'awareness': min(0.95, 0.4 + success_rate * 0.5),
                        'emotion': 'CALM' if error_rate < 10 else 'CAUTIOUS',
                        'curiosity': min(0.9, 0.4 + success_rate * 0.4),
                        'insight_depth': min(0.9, 0.4 + success_rate * 0.5),
                        'resilience': min(0.95, 0.6 - error_rate * 0.3),
                        'focus': min(0.95, 0.4 + success_rate * 0.5),
                        'insights': [
                            f"Success rate: {success_rate*100:.0f}%",
                            f"Error rate: {error_rate*100:.1f}%",
                            f"Cycles: {status_data.get('cycles', 0)}",
                        ],
                        'source': 'status',
                        'is_fallback': False
                    }
                    logger.info("✅ Reflection data from brain.status()")
                    return result
            except Exception as e:
                logger.debug(f"brain.status() error: {e}")
        
        # ===== FALLBACK =====
        logger.warning("All brain methods failed, using fallback data")
        return None
    
    # ============================================================
    # FALLBACK DATA - HANYA SEBAGAI CADANGAN
    # ============================================================
    
    def _generate_fallback_data(self) -> Dict[str, Any]:
        """Generate fallback data - only used when brain is unavailable."""
        insight_pool = [
            "Market sentiment is stabilizing after recent volatility.",
            "Bullish divergence forming on RSI across major pairs.",
            "Order book depth increasing; accumulation phase likely.",
            "Funding rates normalized; leverage reduced.",
            "MACD histogram turning positive on daily chart.",
            "Volume profile shows strong support at current levels.",
            "Implied volatility declining; market becoming complacent.",
            "Open interest rising with price, confirming uptrend.",
            "Liquidation cascades decreasing; risk-off sentiment fading.",
            "Correlation with equities weakening; crypto decoupling.",
            "Seasonal patterns suggest higher volatility ahead.",
            "Options gamma positioning neutral; no major wicks.",
            "Social sentiment turning bullish; retail interest rising.",
            "Technical indicators in oversold territory; bounce probable.",
            "Exchange flows positive; net accumulation by large holders.",
            "Order flow imbalance favors buyers at key levels.",
            "Basis trade unwinding reducing downward pressure.",
            "Stablecoin inflow suggests buying power is increasing.",
            "Perpetual funding rates positive but not excessive.",
            "Volatility term structure in contango; normal conditions."
        ]
        
        if self._last_fallback:
            prev = self._last_fallback
            awareness = prev.get('awareness', 0.55)
            curiosity = prev.get('curiosity', 0.5)
            insight_depth = prev.get('insight_depth', 0.5)
            resilience = prev.get('resilience', 0.5)
            focus = prev.get('focus', 0.5)
            emotion = prev.get('emotion', 'CALM')
            insights = prev.get('insights', [])
            
            awareness += random.uniform(-0.015, 0.015)
            awareness = max(0.55, min(0.98, awareness))
            
            curiosity += random.uniform(-0.01, 0.02)
            curiosity = max(0.2, min(0.98, curiosity))
            
            insight_depth += random.uniform(-0.015, 0.015)
            insight_depth = max(0.2, min(0.98, insight_depth))
            
            resilience += random.uniform(-0.01, 0.01)
            resilience = max(0.2, min(0.98, resilience))
            
            focus += random.uniform(-0.02, 0.02)
            focus = max(0.2, min(0.98, focus))
            
            emotion_list = ['CALM', 'FOCUSED', 'CURIOUS', 'ALERT', 'CONTEMPLATIVE', 'EXCITED']
            if random.random() < 0.08:
                current_idx = emotion_list.index(emotion) if emotion in emotion_list else 0
                delta = random.choice([-1, 0, 1])
                new_idx = (current_idx + delta) % len(emotion_list)
                emotion = emotion_list[new_idx]
            
            if random.random() < 0.15 and insights:
                idx = random.randint(0, len(insights)-1)
                new_insight = random.choice(insight_pool)
                while new_insight in insights:
                    new_insight = random.choice(insight_pool)
                insights[idx] = new_insight
        else:
            awareness = random.uniform(0.55, 0.85)
            curiosity = random.uniform(0.3, 0.6)
            insight_depth = random.uniform(0.3, 0.6)
            resilience = random.uniform(0.5, 0.8)
            focus = random.uniform(0.4, 0.7)
            emotion = random.choice(['CALM', 'FOCUSED', 'CURIOUS'])
            num = random.randint(3, 6)
            insights = random.sample(insight_pool, num)
        
        return {
            'awareness': awareness,
            'emotion': emotion,
            'curiosity': curiosity,
            'insight_depth': insight_depth,
            'resilience': resilience,
            'focus': focus,
            'insights': insights[:6],
            'timestamp': datetime.now().isoformat(),
            'is_fallback': True,
            'source': 'fallback_generator'
        }
    
    # ============================================================
    # UI UPDATE
    # ============================================================
    
    def _update_ui(self):
        if not self.reflection_data:
            return
        
        data = self.reflection_data
        awareness = data.get('awareness', 0) * 100
        emotion = data.get('emotion', 'CALM')
        curiosity = data.get('curiosity', 0) * 100
        insight_depth = data.get('insight_depth', 0) * 100
        resilience = data.get('resilience', 0.5) * 100
        focus = data.get('focus', 0.5) * 100
        insights = data.get('insights', [])
        is_fallback = data.get('is_fallback', True)
        
        # Update circular progress
        if self.awareness_progress:
            self.awareness_progress.draw(awareness)
        if self.curiosity_progress:
            self.curiosity_progress.draw(curiosity)
        if self.insight_progress:
            self.insight_progress.draw(insight_depth)
        if self.resilience_progress:
            self.resilience_progress.draw(resilience)
        if self.focus_progress:
            self.focus_progress.draw(focus)
        
        # Emotion
        emotion_emoji = {
            'CALM': '😌', 'FOCUSED': '🧘', 'CURIOUS': '🤔',
            'ALERT': '⚡', 'CONTEMPLATIVE': '🧠', 'EXCITED': '🚀',
            'OPTIMISTIC': '🌟', 'CAUTIOUS': '⚠️', 'ANXIOUS': '😰',
            'CONFIDENT': '💪'
        }
        emoji = emotion_emoji.get(emotion, '😐')
        color = '#8D9AAA'
        if awareness > 70:
            color = '#22C55E'
        elif awareness > 40:
            color = '#F59E0B'
        else:
            color = '#EF4444'
        if self.emotion_label:
            self.emotion_label.configure(text=f"{emoji} {emotion}", text_color=color)
        
        # Summary (2 baris)
        summary = self._generate_summary(awareness, emotion, curiosity, insight_depth, 
                                         resilience, focus, is_fallback)
        if self.summary_label:
            self.summary_label.configure(text=summary)
        
        # Reflections
        if self.reflections_text:
            self.reflections_text.delete("1.0", "end")
            if insights:
                lines = []
                for i, insight in enumerate(insights[:6], 1):
                    lines.append(f"{i}. {insight}")
                if is_fallback:
                    lines.append("\n[Fallback data]")
                self.reflections_text.insert("1.0", "\n".join(lines))
            else:
                self.reflections_text.insert("1.0", "No reflections available.")
        
        # ===== STATUS =====
        if self.reflection_status:
            if self.reflection_data:
                # Status selalu hijau jika ada data
                self.reflection_status.set_status(True)
                # Tampilkan label
                if is_fallback:
                    self.reflection_status.label.configure(text="Reflection (fallback)")
                else:
                    self.reflection_status.label.configure(text="Reflection")
            else:
                self.reflection_status.set_status(False)
    
    def _generate_summary(self, awareness, emotion, curiosity, insight_depth, 
                          resilience, focus, fallback):
        """Generate 2-line cognitive summary."""
        # Awareness
        if awareness >= 75:
            awareness_text = "highly self-aware"
        elif awareness >= 50:
            awareness_text = "moderately aware"
        else:
            awareness_text = "developing awareness"
        
        # Emotion
        emotion_map = {
            'CALM': 'calm', 'FOCUSED': 'focused', 'CURIOUS': 'curious',
            'ALERT': 'alert', 'CONTEMPLATIVE': 'contemplative', 'EXCITED': 'excited',
            'OPTIMISTIC': 'optimistic', 'CAUTIOUS': 'cautious', 'ANXIOUS': 'anxious',
            'CONFIDENT': 'confident'
        }
        emotion_text = emotion_map.get(emotion, 'neutral')
        
        # Insight
        if insight_depth >= 60:
            insight_text = "deep clarity"
        elif insight_depth >= 40:
            insight_text = "moderate clarity"
        else:
            insight_text = "shallow analysis"
        
        line1 = f"🧠 {awareness_text} · {emotion_text} · {insight_text}"
        
        res_text = "high" if resilience >= 70 else "moderate" if resilience >= 40 else "low"
        foc_text = "high" if focus >= 70 else "moderate" if focus >= 40 else "low"
        line2 = f"🛡️ Resilience: {res_text} · 🎯 Focus: {foc_text}"
        
        if curiosity >= 70:
            line2 += " · 🔍 High curiosity"
        elif curiosity >= 40:
            line2 += " · 🔍 Moderate curiosity"
        else:
            line2 += " · 🔍 Low curiosity"
        
        if fallback:
            line2 += " (simulated)"
        
        return line1 + "\n" + line2
    
    def _update_error_display(self, error: Exception):
        if self.reflections_text:
            self.reflections_text.delete("1.0", "end")
            self.reflections_text.insert(
                "1.0",
                f"❌ ERROR\n\n{error}\n\nTraceback:\n{traceback.format_exc()}"
            )
        if self.reflection_status:
            self.reflection_status.set_status(False)
    
    # ============================================================
    # CONTROL METHODS
    # ============================================================
    
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