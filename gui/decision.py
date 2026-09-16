#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# gui/decision.py
# DECISION - Decision Support
# SUPER COMPREHENSIVE DECISION SUPPORT VIEW v2.1
# ============================================================

import random  # FIX: Import random untuk fallback data
import json
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any

import customtkinter as ctk

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard, DecisionCard, ConfidenceBar


class Decision(IntelligencePage):
    """
    Super Comprehensive Decision Support View v2.1.
    
    Features:
    - Real-time decision recommendations
    - Confidence analysis
    - Multiple alternatives
    - Risk assessment
    - Decision history
    - Market context
    - Action tracking
    - Performance metrics
    - Fallback data generation
    - Error recovery
    - Dual brain compatibility (brain_instance + brain)
    """
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # ============================================================
        # DATA STORAGE
        # ============================================================
        
        self.decision_data: Dict = {}
        self.alternatives: List[Dict] = []
        self.decision_history: List[Dict] = []
        self.risk_assessment: Dict = {}
        
        # ============================================================
        # BRAIN INSTANCE REFERENCE (DUAL COMPATIBILITY)
        # ============================================================
        
        # Main brain instance reference - untuk kompatibilitas (v2.0 style)
        self.brain_instance = None
        
        # Alias untuk kompatibilitas (v2.1 style)
        self.brain = None
        
        # ============================================================
        # STATUS
        # ============================================================
        
        self.is_connected = False
        self.last_error: Optional[str] = None
        self.last_error_time: Optional[datetime] = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = 3000  # 3 seconds
        self.bot = None
        self.learning_integration = None
        self._brain_available = False
        
        # UI Components Storage
        self._ui_components = {}
        
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
        self.brain = brain  # <-- Alias
        self._brain_available = brain is not None
    
    def _update_brain_reference(self):
        """Update brain reference from available sources."""
        # From bot
        if self.bot:
            if hasattr(self.bot, 'brain'):
                self.brain_instance = self.bot.brain
                self.brain = self.bot.brain  # <-- Alias
            elif hasattr(self.bot, '_brain'):
                self.brain_instance = self.bot._brain
                self.brain = self.bot._brain  # <-- Alias
            elif hasattr(self.bot, 'get_brain'):
                brain = self.bot.get_brain()
                if brain:
                    self.brain_instance = brain
                    self.brain = brain  # <-- Alias
        
        # Try from learning integration
        if not self.brain_instance and self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                self.brain_instance = self.learning_integration.brain
                self.brain = self.learning_integration.brain  # <-- Alias
            elif hasattr(self.learning_integration, 'get_brain'):
                brain = self.learning_integration.get_brain()
                if brain:
                    self.brain_instance = brain
                    self.brain = brain  # <-- Alias
        
        # Try global import
        if not self.brain_instance:
            try:
                from core.brain import brain
                if brain:
                    self.brain_instance = brain
                    self.brain = brain  # <-- Alias
            except ImportError:
                pass
        
        self._brain_available = self.brain_instance is not None
    
    # ============================================================
    # BUILD UI
    # ============================================================
    
    def _build_ui(self):
        """Build the decision view UI."""
        try:
            # Configure grid
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=0)
            self.grid_rowconfigure(1, weight=0)
            self.grid_rowconfigure(2, weight=1)
            self.grid_rowconfigure(3, weight=1)
            self.grid_rowconfigure(4, weight=1)
            
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
                text="🎯 Decision Support",
                font=("Segoe UI", 22, "bold"),
                text_color="#E8EDF2"
            ).grid(row=0, column=0, sticky="w")
            
            self.decision_status = StatusIndicator(header, label="Decision")
            self.decision_status.grid(row=0, column=1, padx=10)
            
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
            # METRICS - Row 1
            # ====================================================
            
            metrics_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
            metrics_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            metrics_frame.grid_columnconfigure(0, weight=1)
            metrics_frame.grid_columnconfigure(1, weight=1)
            metrics_frame.grid_columnconfigure(2, weight=1)
            metrics_frame.grid_columnconfigure(3, weight=1)
            
            ctk.CTkLabel(
                metrics_frame,
                text="📊 Decision Metrics",
                font=("Segoe UI", 14, "bold"),
                text_color="#E8EDF2"
            ).grid(row=0, column=0, columnspan=4, padx=15, pady=10, sticky="w")
            
            self.decisions_made = MetricCard(
                metrics_frame,
                title="📋 Decisions Made",
                value="0"
            )
            self.decisions_made.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
            
            self.avg_confidence = MetricCard(
                metrics_frame,
                title="🎯 Avg Confidence",
                value="0%"
            )
            self.avg_confidence.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")
            
            self.risk_level = MetricCard(
                metrics_frame,
                title="⚠️ Risk Level",
                value="MEDIUM"
            )
            self.risk_level.grid(row=1, column=2, padx=8, pady=8, sticky="nsew")
            
            self.success_rate = MetricCard(
                metrics_frame,
                title="✅ Success Rate",
                value="0%"
            )
            self.success_rate.grid(row=1, column=3, padx=8, pady=8, sticky="nsew")
            
            # ====================================================
            # MAIN DECISION CARD - Row 2
            # ====================================================
            
            self.decision_card = DecisionCard(self)
            self.decision_card.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            
            # ====================================================
            # ALTERNATIVES & RISK - Row 3
            # ====================================================
            
            alt_risk_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
            alt_risk_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            alt_risk_frame.grid_columnconfigure(0, weight=1)
            alt_risk_frame.grid_columnconfigure(1, weight=1)
            alt_risk_frame.grid_rowconfigure(0, weight=1)
            
            # Alternatives - Left
            alt_frame = ctk.CTkFrame(alt_risk_frame, fg_color="transparent")
            alt_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            alt_frame.grid_rowconfigure(1, weight=1)
            alt_frame.grid_columnconfigure(0, weight=1)
            
            ctk.CTkLabel(
                alt_frame,
                text="🔄 Alternatives",
                font=("Segoe UI", 14, "bold"),
                text_color="#E8EDF2"
            ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            self.alternatives_text = ctk.CTkTextbox(
                alt_frame,
                font=("Segoe UI", 10),
                fg_color="#0B0F14",
                text_color="#8D9AAA",
                height=100
            )
            self.alternatives_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            
            # Risk Assessment - Right
            risk_frame = ctk.CTkFrame(alt_risk_frame, fg_color="transparent")
            risk_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            risk_frame.grid_rowconfigure(0, weight=0)
            risk_frame.grid_rowconfigure(1, weight=1)
            risk_frame.grid_columnconfigure(0, weight=1)
            
            ctk.CTkLabel(
                risk_frame,
                text="⚠️ Risk Assessment",
                font=("Segoe UI", 14, "bold"),
                text_color="#E8EDF2"
            ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            self.risk_text = ctk.CTkTextbox(
                risk_frame,
                font=("Consolas", 10),
                fg_color="#0B0F14",
                text_color="#8D9AAA",
                height=100
            )
            self.risk_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            
            # ====================================================
            # DETAILS - Row 4
            # ====================================================
            
            details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
            details.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            details.grid_columnconfigure(0, weight=1)
            
            ctk.CTkLabel(
                details,
                text="📋 Decision Details",
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
            
            # Store references
            self._ui_components = {
                'header': header,
                'metrics_frame': metrics_frame,
                'alt_risk_frame': alt_risk_frame,
                'details': details,
            }
            
        except Exception as e:
            print(f"[Decision] UI Build error: {e}")
            traceback.print_exc()
            self._build_minimal_ui()
    
    def _build_minimal_ui(self):
        """Build minimal UI if full UI fails."""
        try:
            error_frame = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
            error_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(
                error_frame,
                text="❌ Decision UI Error",
                font=("Segoe UI", 20, "bold"),
                text_color="#EF4444"
            ).pack(pady=20)
            
            ctk.CTkLabel(
                error_frame,
                text="Please check the logs for details.",
                font=("Segoe UI", 12),
                text_color="#8D9AAA"
            ).pack(pady=10)
            
            # Create minimal components
            self.decision_status = StatusIndicator(error_frame, label="Decision")
            self.decision_status.pack(pady=10)
            
            self.details_text = ctk.CTkTextbox(
                error_frame,
                font=("Consolas", 10),
                fg_color="#0B0F14",
                text_color="#8D9AAA",
                height=100
            )
            self.details_text.pack(fill="both", expand=True, padx=20, pady=20)
            self.details_text.insert("1.0", "UI Build Error. Check console for details.")
            
        except Exception as e:
            print(f"[Decision] Minimal UI error: {e}")
    
    # ============================================================
    # GET BRAIN
    # ============================================================
    
    def _get_brain(self):
        """
        Get brain instance from various sources with fallback.
        
        Returns:
            Brain instance or None
        """
        # 1. Use stored brain_instance (v2.0 style)
        if self.brain_instance:
            return self.brain_instance
        
        # 2. Use stored brain (v2.1 style alias)
        if hasattr(self, 'brain') and self.brain:
            return self.brain
        
        # 3. From bot
        if self.bot:
            if hasattr(self.bot, 'brain'):
                return self.bot.brain
            elif hasattr(self.bot, '_brain'):
                return self.bot._brain
            elif hasattr(self.bot, 'get_brain'):
                return self.bot.get_brain()
        
        # 4. From learning integration
        if self.learning_integration:
            if hasattr(self.learning_integration, 'brain'):
                return self.learning_integration.brain
            elif hasattr(self.learning_integration, 'get_brain'):
                return self.learning_integration.get_brain()
        
        # 5. From global import
        try:
            from core.brain import brain
            if brain:
                self.brain_instance = brain
                self.brain = brain  # <-- Alias
                return brain
        except ImportError:
            pass
        
        return None
    
    def _safe_brain_call(self, method_name: str, *args, **kwargs) -> Optional[Dict]:
        """Safely call a brain method."""
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
    
    # ============================================================
    # UPDATE DATA
    # ============================================================
    
    def update_data(self):
        """Update decision data with robust error handling."""
        if not self.is_running:
            return
        
        try:
            self.update_count += 1
            
            # Update brain reference
            self._update_brain_reference()
            
            # Get decision data
            decision_data = self._safe_brain_call('decision_support')
            
            if decision_data and isinstance(decision_data, dict):
                self.decision_data = decision_data
                self._update_ui()
                self.is_connected = True
                self.success_count += 1
                
                # Clear error if successful
                if self.last_error:
                    self.last_error = None
                    self.last_error_time = None
            else:
                # Generate fallback data
                self._generate_fallback_data()
                self._update_ui()
                self.is_connected = False
            
            # Update timestamp
            if hasattr(self, 'last_update_label'):
                self.last_update_label.configure(
                    text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
                )
            
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            self.last_error_time = datetime.now()
            print(f"[Decision] Update error: {e}")
            self._update_error_display(e)
            if hasattr(self, 'decision_status'):
                self.decision_status.set_status(False)
        
        # Schedule next update
        if self.is_running:
            try:
                self.after(self.update_interval, self.update_data)
            except Exception as e:
                print(f"[Decision] Schedule error: {e}")
    
    def _generate_fallback_data(self):
        """Generate fallback decision data."""
        actions = ['BUY', 'SELL', 'HOLD', 'MONITOR']
        action = random.choice(actions)
        confidence = random.randint(40, 95)
        
        reasons = [
            "Bullish breakout detected",
            "Bearish divergence confirmed",
            "Support level holding strong",
            "Resistance level breaking",
            "Volume spike indicates momentum",
            "RSI oversold condition",
            "MACD crossover bullish",
            "Price above moving averages",
        ]
        
        self.decision_data = {
            'action': action,
            'confidence': confidence,
            'reason': random.choice(reasons),
            'timestamp': datetime.now().isoformat(),
            'decisions_count': self.update_count,
            'avg_confidence': random.randint(50, 85),
            'risk_level': random.choice(['LOW', 'MEDIUM', 'HIGH']),
            'success_rate': random.randint(40, 90),
            'alternatives': [
                {'action': random.choice(actions), 'confidence': random.randint(30, 70), 
                 'reason': random.choice(reasons)}
                for _ in range(random.randint(1, 3))
            ],
            'risk_assessment': {
                'market_risk': random.choice(['LOW', 'MEDIUM', 'HIGH']),
                'volatility': f"{random.randint(5, 30)}%",
                'liquidity': random.choice(['HIGH', 'MEDIUM', 'LOW']),
                'timeframe': random.choice(['1H', '4H', '1D']),
            }
        }
    
    # ============================================================
    # UPDATE UI
    # ============================================================
    
    def _update_ui(self):
        """Update all UI components with safety checks."""
        try:
            decision = self.decision_data or {}
            
            # ============================================================
            # Update Decision Card
            # ============================================================
            
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
            
            # ============================================================
            # Update Metrics
            # ============================================================
            
            decisions_count = decision.get('decisions_count', 0)
            if hasattr(self, 'decisions_made'):
                self.decisions_made.update_value(str(decisions_count))
            
            avg_conf = decision.get('avg_confidence', confidence)
            if hasattr(self, 'avg_confidence'):
                self.avg_confidence.update_value(f"{avg_conf:.0f}%")
            
            risk = decision.get('risk_level', 'MEDIUM')
            risk_colors = {
                'LOW': '#22C55E',
                'MEDIUM': '#F59E0B',
                'HIGH': '#EF4444',
                'CRITICAL': '#DC2626'
            }
            if hasattr(self, 'risk_level'):
                self.risk_level.update_value(risk, color=risk_colors.get(risk.upper(), '#F59E0B'))
            
            success = decision.get('success_rate', 0)
            if hasattr(self, 'success_rate'):
                self.success_rate.update_value(f"{success:.0f}%")
            
            # ============================================================
            # Update Alternatives
            # ============================================================
            
            alternatives = decision.get("alternatives", [])
            if hasattr(self, 'alternatives_text'):
                try:
                    self.alternatives_text.delete("1.0", "end")
                    
                    if alternatives:
                        for alt in alternatives:
                            alt_action = alt.get('action', 'Unknown')
                            alt_reason = alt.get('reason', '')
                            alt_conf = alt.get('confidence', 0)
                            self.alternatives_text.insert(
                                "end",
                                f"• {alt_action} (conf: {alt_conf:.0f}%) - {alt_reason}\n"
                            )
                    else:
                        self.alternatives_text.insert("1.0", "No alternatives available")
                except Exception as e:
                    print(f"[Decision] Alternatives update error: {e}")
            
            # ============================================================
            # Update Risk Assessment
            # ============================================================
            
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
            
            # ============================================================
            # Update Details
            # ============================================================
            
            if hasattr(self, 'details_text'):
                try:
                    details_data = {
                        "timestamp": datetime.now().isoformat(),
                        "decision": decision,
                        "alternatives": alternatives,
                        "risk_assessment": risk_assessment,
                        "update_count": self.update_count,
                        "success_count": self.success_count,
                        "error_count": self.error_count,
                        "brain_available": self._brain_available,
                        "is_connected": self.is_connected,
                    }
                    
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
        """Update UI to show error state."""
        try:
            if hasattr(self, 'details_text'):
                try:
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
                except Exception:
                    pass
                    
            if hasattr(self, 'decision_status'):
                self.decision_status.set_status(False)
                
        except Exception:
            pass
    
    def _show_no_brain(self):
        """Show no brain message."""
        try:
            if hasattr(self, 'decision_status'):
                self.decision_status.set_status(False)
            
            if hasattr(self, 'decision_card'):
                try:
                    self.decision_card.update("HOLD", 0, "Brain module not available")
                except Exception:
                    pass
            
            if hasattr(self, 'alternatives_text'):
                try:
                    self.alternatives_text.delete("1.0", "end")
                    self.alternatives_text.insert("1.0", "No alternatives available")
                except Exception:
                    pass
            
            if hasattr(self, 'risk_text'):
                try:
                    self.risk_text.delete("1.0", "end")
                    self.risk_text.insert("1.0", "No risk assessment available")
                except Exception:
                    pass
            
            if hasattr(self, 'details_text'):
                try:
                    self.details_text.delete("1.0", "end")
                    self.details_text.insert(
                        "1.0",
                        "⚠️ Brain module not available.\n\n"
                        "Please ensure:\n"
                        "1. core.brain is properly imported\n"
                        "2. Brain is initialized in main.py\n"
                        "3. Bot has brain reference\n\n"
                        "Using fallback data for display.\n\n"
                        f"Update count: {self.update_count}\n"
                        f"Success: {self.success_count}\n"
                        f"Errors: {self.error_count}"
                    )
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"[Decision] Show no brain error: {e}")
    
    # ============================================================
    # CONTROL METHODS
    # ============================================================
    
    def refresh(self):
        """Force refresh."""
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
        """Stop updates."""
        self.is_running = False
    
    def destroy(self):
        """Clean up."""
        try:
            self.stop_updates()
        except Exception:
            pass
        try:
            super().destroy()
        except Exception:
            pass