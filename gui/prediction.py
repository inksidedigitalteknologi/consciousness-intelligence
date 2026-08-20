# ============================================================
# gui/intelligence/prediction.py
# PREDICTION - Predictions & Forecasts
# SUPER COMPREHENSIVE v2.1 - FIXED & ENHANCED
# ============================================================

import random
import json
import traceback
from datetime import datetime
from typing import Dict, Optional, Any

import customtkinter as ctk

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard, ConfidenceBar


class Prediction(IntelligencePage):
    """
    Super Comprehensive Predictions and Forecasts View v2.1.
    
    Features:
    - Real-time forecast display
    - Confidence analysis with bars
    - Auto-refresh with fallback data
    - Brain integration with safety checks
    - Error handling and recovery
    - Manual refresh button
    - Detailed forecast JSON view
    - Status indicators
    - Last update timestamp
    - Dual brain compatibility (brain_instance + brain)
    - Random fallback data generator
    """
    
    def __init__(self, parent, *args, **kwargs):
        # ============================================================
        # FIX: Set all attributes BEFORE calling super()
        # ============================================================
        
        # Data storage
        self.forecast_data: Dict[str, Any] = {}
        self.fallback_mode = False
        self.last_error: Optional[str] = None
        self.last_error_time: Optional[datetime] = None
        
        # Brain references (dual compatibility)
        self.brain_instance = None
        self.brain = None
        self._brain_available = False
        
        # Bot reference
        self.bot = None
        self.learning_integration = None
        
        # Status
        self.is_running = True
        self.update_interval = 3000  # 3 seconds
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_connected = False
        
        # UI components storage
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
        
        # Call super
        super().__init__(parent, *args, **kwargs)
        
        # Build UI
        self._build_ui()
        
        # Start updates
        self.after(100, self.update_data)  # Delay initial update
    
    # ============================================================
    # PUBLIC METHODS
    # ============================================================
    
    def set_bot(self, bot):
        """Set bot reference."""
        self.bot = bot
        self._update_brain_reference()
    
    def set_learning(self, learning):
        """Set learning integration reference."""
        self.learning_integration = learning
        self._update_brain_reference()
    
    def set_brain(self, brain):
        """Set brain reference directly."""
        self.brain_instance = brain
        self.brain = brain
        self._brain_available = brain is not None
        self._update_brain_reference()
    
    def _update_brain_reference(self):
        """Update brain from bot or brain attribute."""
        # From bot
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
        
        # From learning integration
        if not self.brain and self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                self.brain = self.learning_integration.brain
                self.brain_instance = self.learning_integration.brain
            elif hasattr(self.learning_integration, 'get_brain'):
                brain = self.learning_integration.get_brain()
                if brain:
                    self.brain = brain
                    self.brain_instance = brain
        
        # Global fallback
        if not self.brain:
            try:
                from core.brain import brain
                if brain:
                    self.brain = brain
                    self.brain_instance = brain
            except ImportError:
                pass
        
        self._brain_available = self.brain is not None
    
    # ============================================================
    # BUILD UI
    # ============================================================
    
    def _build_ui(self):
        """Build the prediction view UI with enhanced controls."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        
        # ====================================================
        # HEADER
        # ====================================================
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)
        
        ctk.CTkLabel(
            header,
            text="🔮 Predictions & Forecasts",
            font=("Segoe UI", 22, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")
        
        self.prediction_status = StatusIndicator(header, label="Prediction")
        self.prediction_status.grid(row=0, column=1, padx=10)
        
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
        
        # ====================================================
        # FORECAST CARDS - Row 1
        # ====================================================
        
        self.forecast_card = MetricCard(
            self,
            title="📊 Forecast",
            value="NEUTRAL",
            subtitle="Direction"
        )
        self.forecast_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.confidence_card = MetricCard(
            self,
            title="🎯 Confidence",
            value="0%",
            subtitle="Accuracy"
        )
        self.confidence_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # ====================================================
        # CONFIDENCE BARS - Row 2
        # ====================================================
        
        bars = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        bars.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        bars.grid_columnconfigure(0, weight=1)
        bars.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            bars,
            text="📈 Confidence Analysis",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")
        
        self.bullish_conf = ConfidenceBar(
            bars,
            label="Bullish Confidence",
            value=0
        )
        self.bullish_conf.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        
        self.bearish_conf = ConfidenceBar(
            bars,
            label="Bearish Confidence",
            value=0
        )
        self.bearish_conf.grid(row=1, column=1, padx=15, pady=5, sticky="ew")
        
        self.neutral_conf = ConfidenceBar(
            bars,
            label="Neutral Confidence",
            value=0
        )
        self.neutral_conf.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew")
        
        # ====================================================
        # DETAILS - Row 3
        # ====================================================
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        details.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            details,
            text="📋 Prediction Details",
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
        """Update prediction data with robust error handling."""
        if not self.is_running:
            return
        
        try:
            self.update_count += 1
            self._update_brain_reference()
            
            # Try to get forecast from brain
            forecast = self._get_forecast_safely()
            
            if forecast:
                self.forecast_data = forecast
                self.is_connected = True
                self.success_count += 1
                self.fallback_mode = False
                self.last_error = None
            else:
                # Generate fallback data
                self.forecast_data = self._generate_fallback_data()
                self.is_connected = False
                self.fallback_mode = True
                self.error_count += 1
                self.last_error = "Brain unavailable, using fallback data"
                self.last_error_time = datetime.now()
            
            # Update UI
            self._update_ui()
            
            # Update timestamp
            if self.last_update_label:
                self.last_update_label.configure(
                    text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
                )
            
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            print(f"[Prediction] Update error: {e}")
            traceback.print_exc()
            self._update_error_display(e)
            if self.prediction_status:
                self.prediction_status.set_status(False)
        
        # Schedule next update
        if self.is_running:
            try:
                self._after_id = self.after(self.update_interval, self.update_data)
            except Exception as e:
                print(f"[Prediction] Schedule error: {e}")
    
    # ============================================================
    # FORECAST RETRIEVAL
    # ============================================================
    
    def _get_forecast_safely(self) -> Optional[Dict[str, Any]]:
        """Safely get forecast from brain with multiple fallback attempts."""
        if not self.brain:
            return None
        
        # Try brain.forecast()
        if hasattr(self.brain, 'forecast'):
            try:
                result = self.brain.forecast()
                if result and isinstance(result, dict):
                    # Ensure required keys exist
                    if 'forecast' in result and 'confidence' in result:
                        return result
            except Exception as e:
                print(f"[Prediction] forecast() error: {e}")
        
        # Try brain.get_forecast() (alternative method)
        if hasattr(self.brain, 'get_forecast'):
            try:
                result = self.brain.get_forecast()
                if result and isinstance(result, dict):
                    if 'forecast' in result and 'confidence' in result:
                        return result
            except Exception as e:
                print(f"[Prediction] get_forecast() error: {e}")
        
        # Try brain.snapshot() and extract market data
        if hasattr(self.brain, 'snapshot'):
            try:
                snapshot = self.brain.snapshot()
                if snapshot and isinstance(snapshot, dict):
                    market = snapshot.get('market', {})
                    if market and isinstance(market, dict):
                        forecast = market.get('forecast', 'NEUTRAL')
                        confidence = market.get('confidence', 0)
                        if forecast and confidence is not None:
                            return {
                                'forecast': forecast,
                                'confidence': confidence,
                                'timestamp': datetime.now().isoformat(),
                                'source': 'snapshot'
                            }
            except Exception as e:
                print(f"[Prediction] snapshot() error: {e}")
        
        # Try brain.market_intelligence()
        if hasattr(self.brain, 'market_intelligence'):
            try:
                intelligence = self.brain.market_intelligence()
                if intelligence and isinstance(intelligence, dict):
                    forecast = intelligence.get('forecast', 'NEUTRAL')
                    confidence = intelligence.get('confidence', 0)
                    if forecast and confidence is not None:
                        return {
                            'forecast': forecast,
                            'confidence': confidence,
                            'timestamp': datetime.now().isoformat(),
                            'source': 'market_intelligence'
                        }
            except Exception as e:
                print(f"[Prediction] market_intelligence() error: {e}")
        
        return None
    
    # ============================================================
    # FALLBACK DATA GENERATOR
    # ============================================================
    
    def _generate_fallback_data(self) -> Dict[str, Any]:
        """Generate random but realistic forecast data."""
        directions = ["BULLISH", "BEARISH", "NEUTRAL"]
        direction = random.choice(directions)
        confidence = random.randint(30, 85)
        
        # For realistic distribution
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
        
        # Ensure percentages add up to 100
        total = bullish + bearish + neutral
        if total != 100:
            neutral += (100 - total)
            neutral = max(0, min(100, neutral))
        
        reasons = [
            "Bullish breakout detected",
            "Bearish divergence confirmed",
            "Support level holding strong",
            "Resistance level breaking",
            "Volume spike indicates momentum",
            "RSI oversold condition",
            "MACD crossover bullish",
            "Price above moving averages",
            "Market sentiment improving",
            "Technical indicators aligned"
        ]
        
        return {
            "forecast": direction,
            "confidence": confidence,
            "bullish_probability": bullish,
            "bearish_probability": bearish,
            "neutral_probability": neutral,
            "reason": random.choice(reasons),
            "timestamp": datetime.now().isoformat(),
            "is_fallback": True,
            "source": "fallback_generator"
        }
    
    # ============================================================
    # UI UPDATE
    # ============================================================
    
    def _update_ui(self):
        """Update all UI components with current forecast data."""
        if not self.forecast_data:
            return
        
        forecast = self.forecast_data
        direction = forecast.get("forecast", "NEUTRAL")
        confidence = forecast.get("confidence", 0)
        is_fallback = forecast.get("is_fallback", False)
        
        # ----- Update forecast card -----
        if self.forecast_card:
            color = self._get_direction_color(direction)
            self.forecast_card.update_value(direction, color=color)
            subtitle = f"Confidence: {confidence:.0f}%"
            if is_fallback:
                subtitle += " (fallback)"
            self.forecast_card.update_subtitle(subtitle)
        
        # ----- Update confidence card -----
        if self.confidence_card:
            color = "#22C55E" if confidence >= 60 else "#F59E0B" if confidence >= 40 else "#EF4444"
            self.confidence_card.update_value(f"{confidence:.0f}%", color=color)
        
        # ----- Update status indicator -----
        if self.prediction_status:
            self.prediction_status.set_status(confidence > 50 and not is_fallback)
        
        # ----- Update confidence bars -----
        bullish = forecast.get("bullish_probability", 0)
        bearish = forecast.get("bearish_probability", 0)
        neutral = forecast.get("neutral_probability", 0)
        
        # If probabilities not provided, derive from direction
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
        
        # Ensure values are ints and sum to 100
        try:
            bullish = int(bullish)
            bearish = int(bearish)
            neutral = int(neutral)
            total = bullish + bearish + neutral
            if total != 100:
                # Normalize
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
        
        # ----- Update details text -----
        if self.details_text:
            details_data = {
                "timestamp": datetime.now().isoformat(),
                "forecast": forecast,
                "update_count": self.update_count,
                "success_count": self.success_count,
                "error_count": self.error_count,
                "is_fallback": is_fallback,
                "brain_available": self._brain_available,
                "connected": self.is_connected
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
                print(f"[Prediction] Details update error: {e}")
    
    def _get_direction_color(self, direction: str) -> str:
        """Get color for forecast direction."""
        upper = direction.upper()
        if upper == "BULLISH":
            return "#22C55E"
        elif upper == "BEARISH":
            return "#EF4444"
        else:
            return "#F59E0B"
    
    def _update_error_display(self, error: Exception):
        """Update UI to show error state."""
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
            if self.prediction_status:
                self.prediction_status.set_status(False)
        except Exception:
            pass
    
    # ============================================================
    # CONTROL METHODS
    # ============================================================
    
    def refresh(self):
        """Force a manual refresh."""
        if self.refresh_btn:
            self.refresh_btn.configure(state="disabled", text="⏳ Refreshing...")
            self.update_idletasks()
        
        try:
            self.update_data()
        finally:
            if self.refresh_btn:
                self.refresh_btn.configure(state="normal", text="🔄 Refresh")
    
    def stop(self):
        """Stop periodic updates."""
        self.is_running = False
        if self._after_id:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
    
    def destroy(self):
        """Clean up resources."""
        self.stop()
        super().destroy()